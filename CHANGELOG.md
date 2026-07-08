# Changelog

## Unreleased

## 0.3.0 - 2026-07-09

- Added guided PDF/Markdown/text ingestion into reviewable Source and Card drafts.
- Added local Ollama role configuration, structured-output logging, and safe
  text-only fallback.
- Added advisory semantic duplicate detection with no automatic merging.
- Added explicit Source/Card approval gates, draft validation, and golden
  regression fixtures.
- Added pinned, project-local PDF dependency setup with readiness checks.
- Added actionable PDF setup guidance to discovery and extraction failures.
- Added the first real Bundle and rendered its input/output workflow contract.
- Added single-call, read-only project discovery with command-scoped Git trust.
- Added deterministic PDF text extraction using environment or project-local providers.
- Documented recurring Git, PDF, and sandbox handling for agent sessions.
- Added v0.2 roadmap for schema integrity, staleness audit, and portable execution.
- Strengthened knowledge index validation with enum, date, type-directory, duplicate ID, and link checks.
- Added bidirectional backlink output to the generated knowledge index.
- Added `knowledge_audit.py` for staleness and operational review warnings.
- Added privacy and portability documentation.
- Updated templates with audit fields.
- Backfilled audit fields on existing notes and archived the duplicate coffee infographic test source.

## 0.1.0 - 2026-06-02

- Established Prajnavex as a structured knowledge base project.
- Added Obsidian-compatible vault layout for inbox, sources, cards, maps, skills, bundles, and archive.
- Added source, card, skill, and bundle templates.
- Added metadata schema, image ingest workflow, and product plan.
- Added OCR-backed image draft workflow with human approval before source indexing.
- Added local Web UI MVP for inbox images, source drafts, sources, cards, and skills.
- Added Windows desktop launcher for the local Web UI.
