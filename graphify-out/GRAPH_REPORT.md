# Graph Report - /Users/nitesh/Projects/outreach-dm  (2026-07-25)

## Corpus Check
- 4 files · ~7,375 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 129 nodes · 190 edges · 39 communities detected
- Extraction: 62% EXTRACTED · 38% INFERRED · 0% AMBIGUOUS · INFERRED: 73 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]

## God Nodes (most connected - your core abstractions)
1. `append_contact()` - 18 edges
2. `build_dossier()` - 16 edges
3. `resolve_identity()` - 15 edges
4. `record_source()` - 14 edges
5. `main()` - 12 edges
6. `available_angles()` - 10 edges
7. `check_seen()` - 9 edges
8. `choose_channel()` - 9 edges
9. `TestResolveIdentity` - 9 edges
10. `contacts_for()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `outreach_home()` --calls--> `dossier_path()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/log.py → /Users/nitesh/Projects/outreach-dm/engine.py
- `append_contact()` --calls--> `main()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/log.py → /Users/nitesh/Projects/outreach-dm/engine.py
- `append_contact()` --calls--> `test_append_creates_file_and_parent_dir()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/log.py → /Users/nitesh/Projects/outreach-dm/tests/test_log.py
- `append_contact()` --calls--> `test_append_is_append_only()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/log.py → /Users/nitesh/Projects/outreach-dm/tests/test_log.py
- `append_contact()` --calls--> `test_bad_channel_rejected()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/log.py → /Users/nitesh/Projects/outreach-dm/tests/test_log.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.19
Nodes (11): build_dossier(), choose_channel(), Store one fetched source into the dossier and return the updated dossier.      A, Merge stored sources into the payload the skill drafts from.      `usable` is Fa, Decide the send channel, or defer to Nitesh when it is a real choice.      Resea, record_source(), A gap must stay visible so drafting never fills it silently., The channel shapes the tone, so a real choice is never guessed. (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.18
Nodes (8): Identity, Everything known about who the target is, before any research., Lowercase ASCII slug, collapsing anything non-alphanumeric to a hyphen., Derive a stable person_key from a LinkedIn URL, X handle, or "Name, Company"., resolve_identity(), slugify(), Priority is fixed so one person always resolves to one key., TestResolveIdentity

### Community 2 - "Community 2"
Cohesion: 0.23
Nodes (9): dossier_path(), load_dossier(), engine.py — Deterministic half of outreach-dm.  Handles identity resolution, the, Return the on-disk path for a person's dossier., Load a dossier, returning an empty skeleton if none exists yet., Write a dossier to disk and return its path., Persist the resolved identity into the dossier., save_dossier() (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.24
Nodes (6): check_seen(), Dedupe gate. Runs before any fetching.      Returns prior contacts plus the angl, isolated_home(), Tests for identity resolution, the dedupe gate, and dossier merge., Point every test at a throwaway ~/.outreach so real data is never touched., TestDedupeGate

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (9): append_contact(), Record one sent message. Returns the row that was written.      Raises ValueErro, Tests for the append-only outreach record., Typos must fail loudly, or dedupe would never match the row later., test_append_creates_file_and_parent_dir(), test_bad_angle_rejected_at_write(), test_bad_channel_rejected(), test_bad_intent_rejected() (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (8): available_angles(), Return angles not yet used on this person for this intent, in canonical order., Networking in March must not block a role ask in July., An unlabeled past message might have used this angle. Assume it did., test_angles_are_scoped_per_intent(), test_exhausting_one_intent_leaves_others_open(), test_legacy_row_without_intent_blocks_every_intent(), test_missing_file_returns_empty()

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (5): _emit(), main(), Print a payload as JSON for the skill to read., CLI entry point. Every subcommand prints JSON on stdout., TestCli

### Community 7 - "Community 7"
Cohesion: 0.4
Nodes (5): outreach_home(), log.py — Append-only outreach record.  Every message Nitesh actually sends is ap, Return the data directory, honoring OUTREACH_HOME for tests., Return the path to the append-only sent log., sent_path()

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (4): contacts_for(), Return every prior contact for a person, oldest first., test_append_is_append_only(), test_corrupt_line_does_not_hide_history()

### Community 9 - "Community 9"
Cohesion: 0.5
Nodes (4): Return the angles already used on this person, optionally scoped to one intent., used_angles(), test_unscoped_query_counts_every_intent(), test_used_and_available_are_complementary()

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Return the data directory, honoring OUTREACH_HOME for tests.

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): Return the path to the append-only sent log.

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): Record one sent message. Returns the row that was written.      Raises ValueErro

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): Return every prior contact for a person, oldest first.

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Return the angles already used on this person.

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): Return angles not yet used on this person, in canonical order.

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): Return the on-disk path for a person's dossier.

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): Load a dossier, returning an empty skeleton if none exists yet.

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Write a dossier to disk and return its path.

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Store one fetched source into the dossier and return the updated dossier.      A

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Persist the resolved identity into the dossier.

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Merge stored sources into the payload the skill drafts from.      `usable` is Fa

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Decide the send channel, or defer to Nitesh when it is a real choice.      Resea

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Print a payload as JSON for the skill to read.

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): CLI entry point. Every subcommand prints JSON on stdout.

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Everything known about who the target is, before any research.

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Lowercase ASCII slug, collapsing anything non-alphanumeric to a hyphen.

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Derive a stable person_key from a LinkedIn URL, X handle, or "Name, Company".

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Dedupe gate. Runs before any fetching.      Returns prior contacts plus the angl

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Return the on-disk path for a person's dossier.

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Load a dossier, returning an empty skeleton if none exists yet.

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Write a dossier to disk and return its path.

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Store one fetched source into the dossier and return the updated dossier.      A

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Persist the resolved identity into the dossier.

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Merge stored sources into the payload the skill drafts from.      `usable` is Fa

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Print a payload as JSON for the skill to read.

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Print a payload as JSON for the skill to read.

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): CLI entry point. Every subcommand prints JSON on stdout.

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): CLI entry point. Every subcommand prints JSON on stdout.

## Knowledge Gaps
- **60 isolated node(s):** `log.py — Append-only outreach record.  Every message Nitesh actually sends is ap`, `Return the data directory, honoring OUTREACH_HOME for tests.`, `Return the path to the append-only sent log.`, `Record one sent message. Returns the row that was written.      Raises ValueErro`, `Return every prior contact for a person, oldest first.` (+55 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (1 nodes): `Return the data directory, honoring OUTREACH_HOME for tests.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `Return the path to the append-only sent log.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `Record one sent message. Returns the row that was written.      Raises ValueErro`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `Return every prior contact for a person, oldest first.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Return the angles already used on this person.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `Return angles not yet used on this person, in canonical order.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `Return the on-disk path for a person's dossier.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `Load a dossier, returning an empty skeleton if none exists yet.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `Write a dossier to disk and return its path.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `Store one fetched source into the dossier and return the updated dossier.      A`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `Persist the resolved identity into the dossier.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Merge stored sources into the payload the skill drafts from.      `usable` is Fa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Decide the send channel, or defer to Nitesh when it is a real choice.      Resea`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Print a payload as JSON for the skill to read.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `CLI entry point. Every subcommand prints JSON on stdout.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Everything known about who the target is, before any research.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Lowercase ASCII slug, collapsing anything non-alphanumeric to a hyphen.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Derive a stable person_key from a LinkedIn URL, X handle, or "Name, Company".`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Dedupe gate. Runs before any fetching.      Returns prior contacts plus the angl`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Return the on-disk path for a person's dossier.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Load a dossier, returning an empty skeleton if none exists yet.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `Write a dossier to disk and return its path.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Store one fetched source into the dossier and return the updated dossier.      A`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Persist the resolved identity into the dossier.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Merge stored sources into the payload the skill drafts from.      `usable` is Fa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Print a payload as JSON for the skill to read.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `Print a payload as JSON for the skill to read.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `CLI entry point. Every subcommand prints JSON on stdout.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `CLI entry point. Every subcommand prints JSON on stdout.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Community 6` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.184) - this node is a cross-community bridge._
- **Why does `append_contact()` connect `Community 4` to `Community 3`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `resolve_identity()` connect `Community 1` to `Community 2`, `Community 6`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `append_contact()` (e.g. with `main()` and `.test_prior_contact_removes_its_angle()`) actually correct?**
  _`append_contact()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `build_dossier()` (e.g. with `available_angles()` and `.test_record_and_merge()`) actually correct?**
  _`build_dossier()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `resolve_identity()` (e.g. with `.test_linkedin_url_wins()` and `.test_bare_x_handle()`) actually correct?**
  _`resolve_identity()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `record_source()` (e.g. with `.test_record_and_merge()` and `.test_failed_source_is_visible_not_dropped()`) actually correct?**
  _`record_source()` has 9 INFERRED edges - model-reasoned connections that need verification._