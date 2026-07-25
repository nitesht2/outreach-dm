"""
engine.py — Deterministic half of outreach-dm.

Handles identity resolution, the dedupe gate, and dossier storage/merge.
Deliberately network-free: fetching is done by the skill through MCP tools
(claude-in-chrome for LinkedIn, scrapling for X, WebSearch for the open web),
which keeps every function here unit-testable without mocks.

Nothing in this file ranks, interprets, or writes prose. That is the skill's job.
"""

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

import log

SOURCES = ("linkedin", "x", "web")

_LINKEDIN_RE = re.compile(r"linkedin\.com/in/([A-Za-z0-9\-_%]+)", re.IGNORECASE)
_X_URL_RE = re.compile(r"(?:twitter|x)\.com/([A-Za-z0-9_]{1,15})", re.IGNORECASE)
_X_HANDLE_RE = re.compile(r"^@([A-Za-z0-9_]{1,15})$")


@dataclass
class Identity:
    """Everything known about who the target is, before any research."""

    person_key: str
    linkedin_url: str | None = None
    x_handle: str | None = None
    name: str | None = None
    company: str | None = None


def slugify(text: str) -> str:
    """Lowercase ASCII slug, collapsing anything non-alphanumeric to a hyphen."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", ascii_only.lower())).strip("-")


def resolve_identity(raw_input: str) -> Identity:
    """Derive a stable person_key from a LinkedIn URL, X handle, or "Name, Company".

    Key priority is LinkedIn slug, then X handle, then name-company. The priority
    is fixed so the same person resolves to the same key across runs even when
    the input form differs.
    """
    raw = raw_input.strip()
    if not raw:
        raise ValueError("empty input, expected a LinkedIn URL, @handle, or \"Name, Company\"")

    linkedin_match = _LINKEDIN_RE.search(raw)
    if linkedin_match:
        slug = slugify(linkedin_match.group(1))
        return Identity(person_key=slug, linkedin_url=f"https://www.linkedin.com/in/{slug}")

    handle_match = _X_HANDLE_RE.match(raw) or _X_URL_RE.search(raw)
    if handle_match:
        handle = handle_match.group(1).lower()
        return Identity(person_key=handle, x_handle=handle)

    name, _, company = raw.partition(",")
    name = name.strip()
    company = company.strip() or None
    if not name:
        raise ValueError(f"could not resolve an identity from {raw_input!r}")

    key = slugify(f"{name}-{company}") if company else slugify(name)
    return Identity(person_key=key, name=name, company=company)


def check_seen(person_key: str) -> dict:
    """Dedupe gate. Runs before any fetching.

    Returns prior contacts plus the angles still available. When every angle is
    used the caller must stop rather than repeat one.
    """
    prior = log.contacts_for(person_key)
    available = log.available_angles(person_key)
    return {
        "person_key": person_key,
        "contacted_before": bool(prior),
        "prior_contacts": prior,
        "available_angles": available,
        "exhausted": not available,
    }


def dossier_path(person_key: str) -> Path:
    """Return the on-disk path for a person's dossier."""
    return log.outreach_home() / "dossiers" / f"{person_key}.json"


def load_dossier(person_key: str) -> dict:
    """Load a dossier, returning an empty skeleton if none exists yet."""
    path = dossier_path(person_key)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"person_key": person_key, "identity": {}, "sources": {}}


def save_dossier(dossier: dict) -> Path:
    """Write a dossier to disk and return its path."""
    path = dossier_path(dossier["person_key"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dossier, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def record_source(person_key: str, source: str, content, status: str = "ok") -> dict:
    """Store one fetched source into the dossier and return the updated dossier.

    A failed source is recorded explicitly rather than omitted, so gaps stay
    visible instead of being silently filled by the drafting step.
    """
    if source not in SOURCES:
        raise ValueError(f"unknown source {source!r}, expected one of {SOURCES}")
    if status not in ("ok", "failed"):
        raise ValueError(f"unknown status {status!r}, expected 'ok' or 'failed'")

    dossier = load_dossier(person_key)
    dossier["sources"][source] = {
        "status": status,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "content": content,
    }
    save_dossier(dossier)
    return dossier


def set_identity(identity: Identity) -> dict:
    """Persist the resolved identity into the dossier."""
    dossier = load_dossier(identity.person_key)
    dossier["identity"] = {k: v for k, v in asdict(identity).items() if v is not None}
    save_dossier(dossier)
    return dossier


def build_dossier(person_key: str) -> dict:
    """Merge stored sources into the payload the skill drafts from.

    `usable` is False when no source succeeded. The skill must abort in that
    case: a message built from no evidence invents its hook, and a fabricated
    hook does more damage than sending nothing.
    """
    dossier = load_dossier(person_key)
    sources = dossier.get("sources", {})

    ok = [name for name in SOURCES if sources.get(name, {}).get("status") == "ok"]
    failed = [name for name in SOURCES if sources.get(name, {}).get("status") == "failed"]
    missing = [name for name in SOURCES if name not in sources]

    return {
        "person_key": person_key,
        "identity": dossier.get("identity", {}),
        "sources": {name: sources[name]["content"] for name in ok},
        "sources_ok": ok,
        "sources_failed": failed,
        "sources_missing": missing,
        "usable": bool(ok),
        "available_angles": log.available_angles(person_key),
    }


def choose_channel(dossier: dict, override: str | None = None) -> str:
    """Pick 'linkedin' or 'x' as the channel to send on.

    The design doc says: default to whichever platform produced the strongest
    ranked hook, tie-break to LinkedIn for work-related and X for build-related.
    That tie-break rule is a judgment call about how Nitesh wants to be seen, so
    it lives here as an explicit, testable rule rather than buried in a prompt.

    `dossier` is the output of build_dossier(). `override` comes from --channel.

    TODO(nitesh): implement the selection rule.
    """
    raise NotImplementedError("choose_channel not implemented yet")


def _emit(payload) -> None:
    """Print a payload as JSON for the skill to read."""
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Every subcommand prints JSON on stdout."""
    parser = argparse.ArgumentParser(description="outreach-dm deterministic engine")
    sub = parser.add_subparsers(dest="command", required=True)

    p_resolve = sub.add_parser("resolve", help="resolve an input to a person_key")
    p_resolve.add_argument("input")

    p_seen = sub.add_parser("seen", help="dedupe gate: prior contacts and open angles")
    p_seen.add_argument("person_key")

    p_record = sub.add_parser("record", help="store one fetched source")
    p_record.add_argument("person_key")
    p_record.add_argument("source", choices=SOURCES)
    p_record.add_argument("--status", default="ok", choices=("ok", "failed"))
    p_record.add_argument("--file", help="read content from a file instead of stdin")

    p_dossier = sub.add_parser("dossier", help="merge sources into the drafting payload")
    p_dossier.add_argument("person_key")

    p_logged = sub.add_parser("log-sent", help="append a sent message to sent.jsonl")
    p_logged.add_argument("person_key")
    p_logged.add_argument("channel", choices=("linkedin", "x"))
    p_logged.add_argument("angle", choices=log.ANGLES)
    p_logged.add_argument("--message", required=True)
    p_logged.add_argument("--hook-url")

    args = parser.parse_args(argv)

    if args.command == "resolve":
        identity = resolve_identity(args.input)
        set_identity(identity)
        _emit(asdict(identity))
    elif args.command == "seen":
        _emit(check_seen(args.person_key))
    elif args.command == "record":
        content = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
        record_source(args.person_key, args.source, content, status=args.status)
        _emit({"recorded": args.source, "status": args.status, "chars": len(content)})
    elif args.command == "dossier":
        _emit(build_dossier(args.person_key))
    elif args.command == "log-sent":
        _emit(log.append_contact(
            args.person_key, args.channel, args.angle, args.message, args.hook_url
        ))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
