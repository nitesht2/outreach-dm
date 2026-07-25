# outreach-dm

Person-research + outreach drafting. `/dm-person <linkedin-url | @handle | "Name, Company">`

## Split
- `engine.py` / `log.py` — deterministic, network-free: identity, dedupe, storage, merge. Fully unit-tested.
- `SKILL.md` — all fetching (via MCP tools) and all judgment (hook ranking, voice, drafting).

Rule: Python for anything that must be identical every run. Prompt for anything needing judgment.
Voice rules in Python produce mad-libs. Dedupe in a prompt produces silent duplicates.

## Data
`~/.outreach/` — dossiers + `sent.jsonl`. Outside the repo. Third-party personal data. Never commit.
Override with `OUTREACH_HOME` (tests do this).

## Dependencies
- Voice: `~/.voice/` layers 01-03 + channel file 04/05.
- Validator: `voice_rules.py` imported from `~/Projects/Twitter-NiteshTechAI-Post/`, not copied.
  That repo stays the single source of truth for banned words.

## Rules
- Never sends. Drafts only.
- Never automates LinkedIn. Nitesh opens the page, agent reads it.
- No evidence -> abort. Never fabricate a hook.

## Test
```bash
python3 -m pytest tests/ -q
```
