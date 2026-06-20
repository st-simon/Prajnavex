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
python scripts\discover.py
python scripts\setup_pdf_deps.py
python scripts\setup_pdf_deps.py --check
python scripts\knowledge_index.py --check
python scripts\knowledge_index.py --write-index
python scripts\knowledge_audit.py
python -m unittest discover -s tests -v
```

macOS/Linux:

```bash
python3 scripts/setup_pdf_deps.py
python3 scripts/setup_pdf_deps.py --check
python3 scripts/knowledge_index.py --check
python3 scripts/knowledge_index.py --write-index
python3 scripts/knowledge_audit.py
python3 -m unittest discover -s tests -v
```

Validation checks structural correctness. Audit surfaces review and staleness work without blocking normal use.

## PDF Text Extraction

Install the pinned PDF dependency into the project-local `.deps` directory:

```powershell
python scripts\setup_pdf_deps.py
python scripts\setup_pdf_deps.py --check
```

macOS/Linux:

```bash
python3 scripts/setup_pdf_deps.py
python3 scripts/setup_pdf_deps.py --check
```

Then extract a text PDF:

```powershell
python scripts\extract_pdf.py path\to\source.pdf -o extracted.txt
```

The setup command installs the version pinned in `requirements.txt` without
modifying the system Python environment. Extraction prefers project
`.deps/pypdf` or another supported environment provider.
If the PDF contains only scanned images, run OCR before ingestion.

## Guided Document Ingestion

Create a Source draft, Card candidates, evidence links, and advisory semantic
duplicate warnings:

```powershell
python scripts\ingest_document.py ingest path\to\document.pdf
```

```bash
python3 scripts/ingest_document.py ingest path/to/document.pdf
```

If Ollama is unavailable, the command preserves the extracted evidence and
creates a text-only Source draft with Card generation marked pending.

Review drafts under:

```text
vault/00_inbox/_source_drafts
vault/00_inbox/_card_drafts
```

Validate draft structure and evidence links:

```bash
python3 scripts/ingest_document.py validate
```

Approve the Source before approving its Cards:

```bash
python3 scripts/ingest_document.py approve-source <source-draft>
python3 scripts/ingest_document.py approve-card <card-draft>
```

No draft is promoted automatically.

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
