# Prajnavex v0.3 Build Architecture

## Product Priority

Make document-to-Card drafting reliable before adding more capture surfaces.
The accepted workflow ends at reviewable drafts; stable Vault writes remain a
human decision.

## Environment

- Python 3.13 with standard-library orchestration.
- Project-local `pypdf` for text PDFs.
- Local Ollama for structured semantic analysis.
- Markdown and frontmatter remain the storage contract.

## Model Policy

Model names live in `config/model_roles.json`, not application logic.

| Role | Purpose | Fallback |
| --- | --- | --- |
| `fast` | Chunk extraction and duplicate checks | none |
| `general` | Ordinary synthesis | `fast` |
| `reasoner` | Source and Card synthesis | `general` |

If Ollama is unavailable, ingestion still creates a text-only Source draft and
records that Card generation is pending. No cloud fallback is implicit.

## Pipeline

```text
PDF/TXT/MD
  -> local extraction
  -> ignored evidence text
  -> structured Source draft
  -> structured Card drafts
  -> semantic duplicate warnings
  -> explicit approve/rework/reject
  -> stable Source/Card folders
```

## Observability

Each model call appends JSON to `logs/document-ingest.jsonl`, including role,
resolved model, token counts, latency, status, and fallback use. Logs and
extracted evidence are local and ignored by Git.

## Testing

- Smoke: parsers, rendering, approval gates, and schema shape.
- Quality: one generated PDF completes the real local-model workflow.
- Regression: golden fixtures assert required concepts and draft structure.

## Phase 1

Implement PDF/TXT/MD ingestion, Source/Card drafts, advisory duplicate
detection, and explicit approval commands. Web UI integration is deferred
until the CLI workflow is verified.
