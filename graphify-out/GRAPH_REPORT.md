# Graph Report - /Users/nitesh/Projects/outreach-dm  (2026-07-25)

## Corpus Check
- 4 files · ~5,139 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 84 nodes · 146 edges · 10 communities detected
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 47 edges (avg confidence: 0.8)
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

## God Nodes (most connected - your core abstractions)
1. `resolve_identity()` - 15 edges
2. `append_contact()` - 13 edges
3. `main()` - 11 edges
4. `build_dossier()` - 10 edges
5. `check_seen()` - 9 edges
6. `record_source()` - 9 edges
7. `TestResolveIdentity` - 9 edges
8. `contacts_for()` - 8 edges
9. `available_angles()` - 7 edges
10. `set_identity()` - 7 edges

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
Cohesion: 0.21
Nodes (10): build_dossier(), load_dossier(), Load a dossier, returning an empty skeleton if none exists yet., Store one fetched source into the dossier and return the updated dossier.      A, Persist the resolved identity into the dossier., Merge stored sources into the payload the skill drafts from.      `usable` is Fa, record_source(), set_identity() (+2 more)

### Community 1 - "Community 1"
Cohesion: 0.18
Nodes (11): choose_channel(), dossier_path(), Identity, engine.py — Deterministic half of outreach-dm.  Handles identity resolution, the, Write a dossier to disk and return its path., Print a payload as JSON for the skill to read., Everything known about who the target is, before any research., Lowercase ASCII slug, collapsing anything non-alphanumeric to a hyphen. (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.27
Nodes (4): Derive a stable person_key from a LinkedIn URL, X handle, or "Name, Company"., resolve_identity(), Priority is fixed so one person always resolves to one key., TestResolveIdentity

### Community 3 - "Community 3"
Cohesion: 0.2
Nodes (8): _emit(), main(), Print a payload as JSON for the skill to read., CLI entry point. Every subcommand prints JSON on stdout., isolated_home(), Tests for identity resolution, the dedupe gate, and dossier merge., Point every test at a throwaway ~/.outreach so real data is never touched., TestCli

### Community 4 - "Community 4"
Cohesion: 0.28
Nodes (7): append_contact(), Record one sent message. Returns the row that was written.      Raises ValueErro, Tests for the append-only outreach record., Typos must fail loudly, or dedupe would never match the row later., test_append_creates_file_and_parent_dir(), test_bad_angle_rejected_at_write(), test_bad_channel_rejected()

### Community 5 - "Community 5"
Cohesion: 0.43
Nodes (3): check_seen(), Dedupe gate. Runs before any fetching.      Returns prior contacts plus the angl, TestDedupeGate

### Community 6 - "Community 6"
Cohesion: 0.4
Nodes (6): available_angles(), Return the angles already used on this person., Return angles not yet used on this person, in canonical order., used_angles(), test_missing_file_returns_empty(), test_used_and_available_are_complementary()

### Community 7 - "Community 7"
Cohesion: 0.4
Nodes (5): outreach_home(), log.py — Append-only outreach record.  Every message Nitesh actually sends is ap, Return the data directory, honoring OUTREACH_HOME for tests., Return the path to the append-only sent log., sent_path()

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (4): contacts_for(), Return every prior contact for a person, oldest first., test_append_is_append_only(), test_corrupt_line_does_not_hide_history()

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): CLI entry point. Every subcommand prints JSON on stdout.

## Knowledge Gaps
- **28 isolated node(s):** `log.py — Append-only outreach record.  Every message Nitesh actually sends is ap`, `Return the data directory, honoring OUTREACH_HOME for tests.`, `Return the path to the append-only sent log.`, `Record one sent message. Returns the row that was written.      Raises ValueErro`, `Return every prior contact for a person, oldest first.` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 9`** (1 nodes): `CLI entry point. Every subcommand prints JSON on stdout.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.296) - this node is a cross-community bridge._
- **Why does `append_contact()` connect `Community 4` to `Community 3`, `Community 5`, `Community 6`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.252) - this node is a cross-community bridge._
- **Why does `resolve_identity()` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`?**
  _High betweenness centrality (0.236) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `resolve_identity()` (e.g. with `.test_linkedin_url_wins()` and `.test_bare_x_handle()`) actually correct?**
  _`resolve_identity()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `append_contact()` (e.g. with `main()` and `.test_prior_contact_removes_its_angle()`) actually correct?**
  _`append_contact()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `main()` (e.g. with `append_contact()` and `.test_resolve_prints_json()`) actually correct?**
  _`main()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `build_dossier()` (e.g. with `available_angles()` and `.test_record_and_merge()`) actually correct?**
  _`build_dossier()` has 6 INFERRED edges - model-reasoned connections that need verification._