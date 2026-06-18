# Prajnavex Agent Rules

Project name: Prajnavex | 般若维

Subtitle: A structured knowledge base for clear seeing.

Chinese subtitle: 以般若照见，以结构成维

This project follows the workspace rules in `<workspace-root>/AGENTS.md` and `<workspace-root>/_workspace`.

## Session Start

Run `python scripts/discover.py` before broader project discovery. It reports
Git status, PDF providers, Vault layout, templates, schema paths, and index
state without changing project or Git configuration.

For Vault writes, read `docs/schema.md` and `vault/_README.md` first. Treat
those files as canonical instead of deriving rules from existing notes.

## Known Environment Friction

- Git ownership mismatch: use command-scoped
  `git -c safe.directory="<project-root>" ...`; do not write `safe.directory`
  to repository-local configuration.
- PDF extraction: use `python scripts/extract_pdf.py <pdf>`. It checks the
  environment and project `.deps`; if no text is found, use OCR.
- Sandbox command rejection: use the discovery script instead of rebuilding
  the same report through compound shell pipelines.

## Project Scope

Build and maintain a personal knowledge pipeline:

```text
capture -> source -> card -> skill -> bundle -> tool/workflow
```

## MVP Constraints

- Input can be messy; stored knowledge must be structured.
- `vault/00_inbox` is the only intentionally messy area.
- `vault/10_sources`, `vault/20_cards`, `vault/40_skills`, and `vault/50_bundles` require frontmatter.
- Frontmatter is the machine index layer; Markdown body is the human reading layer.
- Search and automation should inspect frontmatter first, then read body content only for candidates.
- Obsidian links support human navigation; stable IDs and frontmatter support scripts and agents.
- CLI tools are adapters, not the system foundation.

## Data Boundaries

- Do not store credentials, API keys, private tokens, or sensitive personal records in this vault.
- Large binary files should live outside Git unless intentionally tracked.
- Preserve original source URLs whenever possible.
