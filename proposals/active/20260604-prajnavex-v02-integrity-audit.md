# Prajnavex v0.2 Integrity and Audit

Status: verified

Release status: verified-uncommitted

Approved: 2026-06-04
Portable PDF extension approved: 2026-06-20

## Scope

Build v0.2 around schema integrity, staleness audit, bidirectional indexes, portability, privacy discipline, and the first real bundle-to-workflow contract.

The 2026-06-20 extension adds reproducible project-local PDF dependency setup.
It does not add Source or Card generation; that work is deferred to v0.3.

## Deliverables

- Stronger `knowledge_index.py` validation.
- New `knowledge_audit.py` operational audit.
- Updated metadata schema and templates.
- v0.2 roadmap documentation.
- Portability and privacy documentation.
- Focused tests.
- Pinned PDF dependency and project-local setup command.
- Discovery readiness status and actionable OCR fallback.

## Acceptance

- Validation has zero errors on the current vault.
- Audit reports warnings without blocking normal use.
- Index output includes forward records and backlinks.
- Tests pass with the standard library test runner.
- A clean machine can install PDF support into `.deps` and pass the readiness
  check without modifying system Python.

## Verification

Verified on 2026-06-20:

- Project-local `pypdf 6.13.3` is ready.
- A generated text PDF completed real extraction through `extract_pdf.py`.
- The first Bundle renders a workflow draft with contracts and linked Skills.
- Knowledge validation reports 33 notes, zero warnings, and zero errors.
- Knowledge audit reports zero issues, warnings, and errors.
- All 15 unit tests pass.
