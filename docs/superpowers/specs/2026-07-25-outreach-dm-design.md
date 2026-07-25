# outreach-dm — Design Spec

Date: 2026-07-25
Status: Approved

## Problem

Writing a genuinely personalized outreach message to one person takes 20-30 minutes of
manual research across LinkedIn, X, and the open web, and the result still often reads
like an enrichment tool produced it. At any volume there is also no record of who was
contacted or with what angle, so people get messaged twice with the same hook.

## Goal

One command produces an evidence-backed dossier on a person plus three differently-angled
message drafts in Nitesh's voice, and records the outreach so it never repeats.

Non-goal: sending. The tool never sends a message. Output is a markdown file to copy from.

## Scope

General purpose. The target may be a hiring manager, an X builder, a prospect, or anyone
else. The agent infers the appropriate angle from the evidence rather than being told the
category up front.

One person per run, with Nitesh present. Batch/unattended operation is explicitly out of
scope for v1 (see Deferred).

## Interface

```
/dm-person <linkedin-url | @xhandle | "Name, Company">
```

`person_key` derivation, in priority order:

1. LinkedIn vanity slug (`linkedin.com/in/<slug>` -> `<slug>`)
2. X handle, lowercased, no `@`
3. slugified `name-company`

The key is stable across runs so the dedupe log works even when the input form differs
between runs.

## Architecture

Two layers, split on one rule: **Python does anything that must be byte-identical every
run; the prompt does anything requiring judgment.** Putting voice rules in Python yields
mad-libs output. Putting dedupe in a prompt yields silent duplicates.

```
~/Projects/outreach-dm/
├── SKILL.md              # orchestration + judgment; symlinked to ~/.claude/skills/dm-person/
├── engine.py             # fetch, cache, dedupe, evidence assembly
├── log.py                # sent.jsonl append + query
├── requirements.txt
├── CLAUDE.md
├── .gitignore
└── .venv/                # Python 3.10+ required (system python3 is 3.9)

~/.outreach/              # data, outside the repo, never committed
├── dossiers/<person_key>.json
└── sent.jsonl
```

`voice_rules.py` and `voice_rules.md` are NOT copied. `engine.py` imports the validator
from `~/Projects/Twitter-NiteshTechAI-Post/` via a path insert, keeping that file the
single source of truth for banned words and anti-slop checks.

### engine.py responsibilities

| Function | Purpose |
|---|---|
| `resolve_identity(raw_input)` | Produce `person_key` plus whatever URLs/handles are known |
| `check_seen(person_key)` | Read `sent.jsonl`, return prior contacts (angle, date, message) |
| `fetch_x(handle)` | Profile bio + recent posts; scrapling `stealthy_fetch`, xurl fallback |
| `search_web(name, company)` | WebSearch-backed hits: personal site, GitHub, talks, podcasts |
| `cache_linkedin(person_key, text)` | Persist the Chrome-read page text into the dossier |
| `build_dossier(person_key)` | Merge all sources into one JSON, write to `dossiers/` |

`engine.py` never ranks, interprets, or writes prose. It only gathers and stores.

### SKILL.md responsibilities

Ranking evidence, choosing angles, and writing the drafts. All judgment lives here.

## Flow

**1. Dedupe gate (first, before any fetching).**
`check_seen(person_key)`. If prior contact exists, print it with its date and angle, and
constrain the run to an angle not yet used. Cheap gates run before expensive work; a
dedupe check after research wastes an entire research pass on someone already burned.

**2. LinkedIn — human in the loop.**
The skill instructs Nitesh to open the profile in his logged-in Chrome, then waits. It
reads the rendered page via `claude-in-chrome` `get_page_text` and passes the text to
`cache_linkedin`. There is no automated navigation to linkedin.com and no scraping of it.
This is deliberate: automated LinkedIn access violates their ToS and risks a ban on
Nitesh's own account. Reading a page he already has open carries neither risk.

If Chrome is unavailable, the skill falls back to asking him to paste the profile text.

**3. X — automated.**
`fetch_x` pulls bio, pinned post, and recent posts, preferring highest-engagement ones.
Primary path is scrapling `stealthy_fetch`; fallback is the funded X API via xurl.
Failure here is non-fatal — the run continues with whatever sources succeeded.

**4. Public web.**
`search_web` finds personal sites, GitHub, conference talks, podcast appearances. This
often yields the strongest hook precisely because the target does not expect anyone to
have found it.

**5. Rank evidence — prompt.**
Score each candidate hook on recency x specificity x overlap with Nitesh's actual work.
Every surviving hook must carry its source URL. Hooks that cannot be tied to a source are
dropped, never softened into vagueness. Target: 3 hooks, one per draft.

**6. Load voice.**
Always `~/.voice/01-identity-core.md`, `02-target-voice.md`, `03-universal-rules.md`.
Then the channel file: `04-linkedin-voice.md` for a LinkedIn DM, `05-x-voice.md` for an X
DM. The platform file changes format only, never identity or anti-slop rules.

Channel is chosen by the skill, not asked: it defaults to whichever platform produced the
strongest ranked hook, since a message referencing an X post reads naturally as an X DM.
If both platforms are equally strong, LinkedIn wins for anything work-related and X for
anything build-related. Nitesh can override with a trailing `--channel x|linkedin`.

**7. Draft three angles.**
- **A. Shared-build** — something both parties have built or shipped
- **B. Their recent thing** — a specific recent post, release, or talk
- **C. Direct ask** — states the ask plainly, minimal preamble

Each draft displays the hook and source URL it was built from, so the evidence can be
judged independently of the writing.

**8. Validate and log.**
Every draft passes through `validate()` from the existing `voice_rules.py`. Violations are
fixed and re-validated before anything is shown. Output goes to a dated markdown file.
Only on Nitesh's explicit confirmation does `log.py` append to `sent.jsonl`:
`{person_key, channel, angle, date, message, hook_url}`.

## Error handling

- **Any single source fails** — continue with the rest; the dossier records which sources
  were unavailable so gaps are visible rather than silently filled.
- **All sources fail** — abort before drafting. Never write a message from no evidence;
  a fabricated hook is worse than no message.
- **`validate()` fails after two fix attempts** — surface the violations to Nitesh rather
  than shipping a draft that trips his own voice rules.
- **Voice files missing** — hard failure. Drafting without them defeats the entire point.

## Testing

pytest, per-file, in the project venv.

- `resolve_identity` produces a stable key across all three input forms for one person
- `check_seen` correctly matches a prior contact and returns its angle
- `check_seen` returns empty for an unknown person
- `build_dossier` merges partial sources and records which ones failed
- `validate()` integration: a draft containing a banned word is caught
- Dedupe gate runs before any network call (assert with mocked fetchers)

Network fetchers are mocked. No test hits LinkedIn, X, or the live web.

## Safety

- Never sends a message on any channel. Drafts only.
- Never automates LinkedIn navigation or scraping.
- Never enters credentials anywhere.
- `~/.outreach/` holds personal data about third parties. It lives outside the repo and is
  never committed.

## Deferred (not v1)

- Batch/unattended runs. Requires Apollo or Bright Data for LinkedIn data; both MCP
  servers need OAuth authorization in an interactive session first. The `engine.py`
  source interface is designed so a provider can be added behind it without changing
  the flow.
- Follow-up sequencing (message 2, message 3 after no reply).
- Reply-rate tracking to learn which angle actually performs.
