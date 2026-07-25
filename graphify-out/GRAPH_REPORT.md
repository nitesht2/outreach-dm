# Graph Report - /Users/nitesh/Projects/outreach-dm  (2026-07-25)

## Corpus Check
- 2 files · ~2,346 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 40 nodes · 63 edges · 8 communities detected
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.8)
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

## God Nodes (most connected - your core abstractions)
1. `main()` - 9 edges
2. `load_dossier()` - 6 edges
3. `sent_path()` - 5 edges
4. `contacts_for()` - 5 edges
5. `available_angles()` - 5 edges
6. `resolve_identity()` - 5 edges
7. `check_seen()` - 5 edges
8. `dossier_path()` - 5 edges
9. `save_dossier()` - 5 edges
10. `record_source()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `dossier_path()` --calls--> `outreach_home()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/engine.py → /Users/nitesh/Projects/outreach-dm/log.py
- `main()` --calls--> `append_contact()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/engine.py → /Users/nitesh/Projects/outreach-dm/log.py
- `build_dossier()` --calls--> `available_angles()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/engine.py → /Users/nitesh/Projects/outreach-dm/log.py
- `check_seen()` --calls--> `contacts_for()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/engine.py → /Users/nitesh/Projects/outreach-dm/log.py
- `check_seen()` --calls--> `available_angles()`  [INFERRED]
  /Users/nitesh/Projects/outreach-dm/engine.py → /Users/nitesh/Projects/outreach-dm/log.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.32
Nodes (7): append_contact(), outreach_home(), log.py — Append-only outreach record.  Every message Nitesh actually sends is ap, Return the data directory, honoring OUTREACH_HOME for tests., Return the path to the append-only sent log., Record one sent message. Returns the row that was written.      Raises ValueErro, sent_path()

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (8): check_seen(), Dedupe gate. Runs before any fetching.      Returns prior contacts plus the angl, available_angles(), contacts_for(), Return every prior contact for a person, oldest first., Return the angles already used on this person., Return angles not yet used on this person, in canonical order., used_angles()

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (6): Identity, Everything known about who the target is, before any research., Lowercase ASCII slug, collapsing anything non-alphanumeric to a hyphen., Derive a stable person_key from a LinkedIn URL, X handle, or "Name, Company"., resolve_identity(), slugify()

### Community 3 - "Community 3"
Cohesion: 0.33
Nodes (6): build_dossier(), _emit(), main(), Merge stored sources into the payload the skill drafts from.      `usable` is Fa, Print a payload as JSON for the skill to read., CLI entry point. Every subcommand prints JSON on stdout.

### Community 4 - "Community 4"
Cohesion: 0.5
Nodes (4): Write a dossier to disk and return its path., Persist the resolved identity into the dossier., save_dossier(), set_identity()

### Community 5 - "Community 5"
Cohesion: 0.5
Nodes (4): dossier_path(), load_dossier(), Load a dossier, returning an empty skeleton if none exists yet., Return the on-disk path for a person's dossier.

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (1): engine.py — Deterministic half of outreach-dm.  Handles identity resolution, the

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (2): Store one fetched source into the dossier and return the updated dossier.      A, record_source()

## Knowledge Gaps
- **20 isolated node(s):** `log.py — Append-only outreach record.  Every message Nitesh actually sends is ap`, `Return the data directory, honoring OUTREACH_HOME for tests.`, `Return the path to the append-only sent log.`, `Record one sent message. Returns the row that was written.      Raises ValueErro`, `Return every prior contact for a person, oldest first.` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 6`** (2 nodes): `engine.py — Deterministic half of outreach-dm.  Handles identity resolution, the`, `engine.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (2 nodes): `Store one fetched source into the dossier and return the updated dossier.      A`, `record_source()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 4`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.240) - this node is a cross-community bridge._
- **Why does `check_seen()` connect `Community 1` to `Community 3`, `Community 6`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Why does `dossier_path()` connect `Community 5` to `Community 0`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `available_angles()` (e.g. with `check_seen()` and `build_dossier()`) actually correct?**
  _`available_angles()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `log.py — Append-only outreach record.  Every message Nitesh actually sends is ap`, `Return the data directory, honoring OUTREACH_HOME for tests.`, `Return the path to the append-only sent log.` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._