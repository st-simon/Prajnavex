# Tasks

## Milestone 1: Knowledge MVP

Status: verified

Done criteria:

- Project scaffold exists.
- Obsidian vault folders exist.
- Source, card, skill, and bundle templates exist.
- Metadata rules are documented.
- Validation/index script can inspect the vault.

## Next

- Add the first bundle note with input/output contract fields.
- Add semantic duplicate detection after the structural validator is stable.

## Completed

- Imported the WSJ AI economy PDF as the first structured source.
- Extracted five knowledge cards.
- Promoted one card cluster into a draft investment research skill.
- Added image OCR and source draft workflow with human approval before source indexing.
- Upgraded image ingest rules to dual-track OCR evidence plus vision-first semantic extraction.
- Added lightweight product plan and local Web UI MVP for inbox, drafts, sources, cards, and skills.
- Added Windows desktop launcher for the local Prajnavex Web UI.
- Started v0.2 integrity and audit workstream.
- Backfilled audit fields on existing sources, cards, and skills.
- Resolved the duplicate coffee infographic source by archiving the early test source and moving card links to the canonical source.

## Known Gaps

- No browser capture extension is wired yet.
- No embedding or semantic search index exists yet.
- No direct Obsidian plugin dependency has been selected.
- Audit is clean on the current vault; future warnings should be treated as review work.


## Card System v0.1 Workstream

Status: design accepted; implementation pending

- Add backward-compatible `card_type`, `sources`, `relations`, `evidence_level`, and `epistemic_status` validation.
- Add card templates for entity, event, method, mechanism, claim, and other approved types.
- Classify existing cards without mass rewriting their bodies.
- Seed cross-source entity/event cards from the China history material.
- Extract technology methods as cards first; review Skill promotion only after repeated validation.
