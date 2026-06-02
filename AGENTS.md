# Prajnavex Agent Rules

Project name: Prajnavex | 般若维

Subtitle: A structured knowledge base for clear seeing.

Chinese subtitle: 以般若照见，以结构成维

This project follows the workspace rules in `E:\codex projects\AGENTS.md` and `E:\codex projects\_workspace`.

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
