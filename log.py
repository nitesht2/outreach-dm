"""
log.py — Append-only outreach record.

Every message Nitesh actually sends is appended to ~/.outreach/sent.jsonl.
This file is the dedupe authority: it answers "have I contacted this person,
and with which angle" before any research work happens.

Append-only by design. Nothing here edits or deletes history.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ANGLES = ("shared-build", "recent-thing", "direct-ask")

# Why Nitesh is reaching out. Distinct from angle: intent is what he wants,
# angle is how the message opens. Intent decides whether there is an ask at all.
INTENTS = (
    "job",      # a role or a referral to whoever owns one
    "network",  # relationship only, no ask
    "advice",   # one specific question, explicitly not a job ask
    "collab",   # build or partner on something
    "pitch",    # sell a service or product
)


def outreach_home() -> Path:
    """Return the data directory, honoring OUTREACH_HOME for tests."""
    return Path(os.environ.get("OUTREACH_HOME", Path.home() / ".outreach"))


def sent_path() -> Path:
    """Return the path to the append-only sent log."""
    return outreach_home() / "sent.jsonl"


def append_contact(
    person_key: str,
    channel: str,
    angle: str,
    message: str,
    hook_url: str | None = None,
    intent: str = "job",
) -> dict:
    """Record one sent message. Returns the row that was written.

    Raises ValueError on an unknown angle or intent so a typo cannot silently
    create a value the dedupe logic would never match against.
    """
    if angle not in ANGLES:
        raise ValueError(f"unknown angle {angle!r}, expected one of {ANGLES}")
    if channel not in ("linkedin", "x"):
        raise ValueError(f"unknown channel {channel!r}, expected 'linkedin' or 'x'")
    if intent not in INTENTS:
        raise ValueError(f"unknown intent {intent!r}, expected one of {INTENTS}")

    row = {
        "person_key": person_key,
        "channel": channel,
        "angle": angle,
        "intent": intent,
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "message": message,
        "hook_url": hook_url,
    }

    path = sent_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def contacts_for(person_key: str) -> list[dict]:
    """Return every prior contact for a person, oldest first."""
    path = sent_path()
    if not path.exists():
        return []

    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            # A corrupt line must not hide the rest of the history.
            continue
        if row.get("person_key") == person_key:
            rows.append(row)
    return rows


def used_angles(person_key: str, intent: str | None = None) -> set[str]:
    """Return the angles already used on this person, optionally scoped to one intent.

    A row with no intent predates the field. It counts against every intent,
    because the safe assumption about an unlabeled past message is that it might
    have used this angle.
    """
    used = set()
    for row in contacts_for(person_key):
        if not row.get("angle"):
            continue
        row_intent = row.get("intent")
        if intent is None or row_intent is None or row_intent == intent:
            used.add(row["angle"])
    return used


def available_angles(person_key: str, intent: str | None = None) -> list[str]:
    """Return angles not yet used on this person for this intent, in canonical order.

    Scoped per intent on purpose: connecting to network in March and asking about
    a role in July are different conversations, and the second should not be
    blocked by the first.
    """
    used = used_angles(person_key, intent)
    return [angle for angle in ANGLES if angle not in used]
