---
name: dm-person
description: >
  Research one person across LinkedIn, X, and the open web, then draft three
  differently-angled outreach messages in Nitesh's voice. Use when the user asks
  to research someone, write a DM or cold message to a specific person, prep
  outreach to a hiring manager, founder, or builder, or says "/dm-person".
  Produces an evidence-backed dossier plus drafts. Never sends anything.
---

# dm-person

Usage: `/dm-person <linkedin-url | @xhandle | "Name, Company">` with optional
`--channel x|linkedin`.

Repo: `~/Projects/outreach-dm`. Data: `~/.outreach` (outside the repo, holds
third-party personal data, never commit it).

The engine is deterministic and network-free. You do the fetching with your MCP
tools and hand the content to the engine. You also do all judgment: which hook
matters, and how to say it in Nitesh's voice.

## Hard rules

- **Never send a message.** Output is a markdown file Nitesh copies from. No
  posting, no DM automation, no Postiz.
- **Never automate LinkedIn.** Do not navigate to or scrape linkedin.com. Nitesh
  opens the profile himself; you read the page he already has open. Automated
  LinkedIn access violates their ToS and risks a ban on his own account.
- **Never invent a hook.** Every claim in a draft traces to a source URL. If no
  source succeeded, abort instead of drafting.
- **Never write to `sent.jsonl` without explicit confirmation.**

## Step 1 — Dedupe gate (before any fetching)

```bash
cd ~/Projects/outreach-dm
python3 engine.py resolve "<raw input>"      # -> person_key
python3 engine.py seen <person_key>
```

Cheap gates run first. Researching before checking is a wasted pass on someone
already contacted.

- `contacted_before: true` → show Nitesh the prior message, date, and angle, then
  restrict this run to `available_angles`.
- `exhausted: true` → **stop.** Tell him every angle is used and ask what he
  wants to do. Do not invent a fourth angle.

## Step 2 — LinkedIn (Nitesh drives)

Ask him to open the profile in his logged-in Chrome, then wait for confirmation.
Once he confirms, read it:

- `mcp__claude-in-chrome__get_page_text` (or `read_page` if the text is thin)

Scroll for About, Experience, and recent activity — recent activity is usually
where the live hook is, not the job title.

```bash
python3 engine.py record <person_key> linkedin --file /path/to/text
```

If Chrome is unavailable, ask him to paste the profile text instead. If he skips
LinkedIn entirely, record it as failed and continue:

```bash
python3 engine.py record <person_key> linkedin --status failed < /dev/null
```

## Step 3 — X (automated)

Fetch `https://x.com/<handle>` with `mcp__scrapling__stealthy_fetch`. Keep the
bio, the pinned post, and the highest-engagement recent posts. If scrapling
fails, fall back to the funded X API via `xurl`. If both fail, record `failed`
and continue — a partial dossier is fine, a fabricated one is not.

```bash
python3 engine.py record <person_key> x --file /path/to/json
```

## Step 4 — Open web

`WebSearch` for the name plus company. Look for a personal site, GitHub, talks,
podcast appearances, newsletter. This is often the strongest hook precisely
because the target does not expect anyone to have found it.

```bash
python3 engine.py record <person_key> web --file /path/to/hits
```

## Step 5 — Build and check

```bash
python3 engine.py dossier <person_key>
```

If `usable: false`, **abort.** Report which sources failed. A message built from
no evidence invents its hook, and a fabricated hook does more damage than sending
nothing at all.

## Step 6 — Rank hooks (judgment)

Score each candidate on:

- **Recency** — this month beats last year. Stale hooks read as automated.
- **Specificity** — a named project or a claim they argued beats "your work in AI".
- **Overlap** — something Nitesh has genuinely also built, hit, or debugged.

Keep the top 3, one per angle. Every hook carries its source URL. Drop hooks you
cannot source; never soften them into vagueness.

## Step 7 — Load voice

Always read, in order:

1. `~/.voice/01-identity-core.md`
2. `~/.voice/02-target-voice.md`
3. `~/.voice/03-universal-rules.md`

Then the channel file: `~/.voice/04-linkedin-voice.md` or `~/.voice/05-x-voice.md`.
The platform file changes format only, never identity or the anti-slop rules.

Channel selection: `engine.choose_channel(dossier, override)`.

## Step 8 — Draft three angles

- **shared-build** — a thing both he and they have built or shipped
- **recent-thing** — a specific recent post, release, or talk
- **direct-ask** — states the ask plainly, minimal preamble

Constraints: short, no filler, no em dashes, contractions on, no emoji opener, no
link in the body. A DM is not a tweet and not a cover letter. If the message
would work verbatim on a different person, it is not personalized — rewrite it.

Show each draft with the hook and source URL it was built from, so Nitesh can
judge the evidence separately from the writing.

## Step 9 — Validate

Run every draft through the existing voice validator. That file is the single
authority for banned words; do not restate its rules here.

```bash
python3 -c "
import sys; sys.path.insert(0, '/Users/nitesh/Projects/Twitter-NiteshTechAI-Post')
import voice_rules
ok, violations = voice_rules.validate(open('draft.txt').read())
print(ok, violations)
"
```

Fix and re-validate. After two failed attempts, surface the violations to Nitesh
rather than shipping a draft that trips his own rules.

## Step 10 — Output and log

Write `~/.outreach/drafts/<person_key>_<MMDDYYYY>.md`: dossier summary, ranked
hooks with sources, then the three drafts.

Only after Nitesh confirms he actually sent one:

```bash
python3 engine.py log-sent <person_key> <channel> <angle> --message "..." --hook-url "..."
```
