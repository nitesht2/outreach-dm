# outreach-dm

Research a person across LinkedIn, X, and the open web, then draft three
differently-angled outreach messages in your own voice. Built as a Claude Code skill.

It never sends anything. Output is a markdown file you copy from.

## How it works

Two layers, split on one rule: **Python does anything that must be identical every
run; the prompt does anything requiring judgment.**

- `engine.py` + `log.py` — identity resolution, dedupe, dossier storage and merge.
  Network-free, so every function is unit-testable with no mocks.
- `SKILL.md` — fetching via MCP tools, hook ranking, voice, drafting.

## Design notes

**The dedupe gate runs before any fetching.** Checking after research wastes a full
research pass on someone you already contacted. Cheap gates go first.

**LinkedIn is human-in-the-loop on purpose.** You open the profile in your own
logged-in browser and the agent reads the page you already have open. No automated
navigation, no scraping — that would violate LinkedIn's ToS and put your own account
at risk.

**Failed sources are recorded, not dropped.** If every source fails the run aborts
instead of drafting. A message built from no evidence invents its hook, and a
fabricated hook does more damage than sending nothing.

## Setup

```bash
pip install -r requirements.txt
ln -s ~/Projects/outreach-dm ~/.claude/skills/dm-person
```

Expects a voice system at `~/.voice/` and a `voice_rules.py` validator to import.
Both paths are configurable in `SKILL.md`.

## Test

```bash
python3 -m pytest tests/ -q
```

MIT
