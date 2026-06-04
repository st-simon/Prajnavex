# Prajnavex | 般若维

A structured knowledge base for clear seeing.

以般若照见，以结构成维

MVP architecture for turning reading material into structured notes, reusable skills, and tool-ready workflows.

## Pipeline

```text
raw input -> inbox -> source -> knowledge card -> skill -> bundle -> tool/workflow
```

## Architecture

See [docs/architecture-overview.md](docs/architecture-overview.md) for the full project map and Mermaid diagrams.

## First Use

Open `vault/` as an Obsidian vault. Capture freely in `vault/00_inbox`, then structure items before moving them into sources, cards, skills, or bundles.

## Verification

Windows PowerShell:

```powershell
python scripts\knowledge_index.py --check
python scripts\knowledge_index.py --write-index
python scripts\knowledge_audit.py
```

macOS/Linux:

```bash
python3 scripts/knowledge_index.py --check
python3 scripts/knowledge_index.py --write-index
python3 scripts/knowledge_audit.py
```

Validation checks structural correctness. Audit surfaces review and staleness work without blocking normal use.

## Local Web UI

Windows PowerShell:

```powershell
python scripts\prajnavex_web.py
```

macOS/Linux:

```bash
python3 scripts/prajnavex_web.py
```

Open:

```text
http://127.0.0.1:8765
```

Keep the terminal running while using the UI.

Optional launchers:

```text
Windows: Start Prajnavex.cmd
macOS: scripts/start-prajnavex-web.command
```

## Bundle Workflow Drafts

Windows PowerShell:

```powershell
python scripts\bundle_tool_draft.py --list
python scripts\bundle_tool_draft.py --bundle-id bundle-YYYYMMDD-slug
```

macOS/Linux:

```bash
python3 scripts/bundle_tool_draft.py --list
python3 scripts/bundle_tool_draft.py --bundle-id bundle-YYYYMMDD-slug
```

See [docs/portability.md](docs/portability.md) and [PRIVACY.md](PRIVACY.md) before sharing or publishing a vault.
