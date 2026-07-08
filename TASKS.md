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

- Start v0.4 Knowledge API Kernel design and implementation from
  `docs/v0.4-v0.6-roadmap.md`.
- Use `docs/v0.4-v0.6-roadmap.md` as the next architecture direction:
  v0.4 Knowledge API Kernel, v0.5 Model Connector Layer, and v0.6 Knowledge
  Reuse Protocol.
- For v0.4, keep the current vault folders stable while adding recall stages,
  maturity signals, usage signals, and bounded context-pack exports through
  frontmatter, index data, and API behavior.

## Completed

- Added Jack D. Schwager's Unknown Market Wizards / 《不为人知的金融怪杰》 as the first official book source for the investment knowledge base, with four extracted research cards.
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
- Added pinned, project-local PDF dependency setup and verified real text
  extraction on macOS without modifying system Python.
- Added the first real Bundle with input/output contracts and verified its
  bundle-to-workflow draft.
- Verified the complete v0.2 operating model with clean validation, audit, and
  unit tests.
- Added a formal document ingestion command that creates Source drafts, atomic
  Card candidates, evidence links, and advisory semantic duplicate warnings.
- Added explicit Source-before-Card approval gates and model-failure fallback.
- Verified v0.3 against a real generated text PDF and a real semantic duplicate
  comparison using the local Ollama models.
- Released the cumulative v0.3.0 baseline, including v0.2 integrity/audit work,
  v0.3 guided Source/Card drafting, and the model-neutral v0.4-v0.6 roadmap.

## Known Gaps

- No browser capture extension is wired yet.
- No embedding or semantic search index exists yet.
- No stable Knowledge API Kernel exists yet.
- No Codex/Claude/model connector layer exists yet.
- No standardized context-pack protocol exists yet.
- No direct Obsidian plugin dependency has been selected.
- Audit is clean on the current vault; future warnings should be treated as review work.
