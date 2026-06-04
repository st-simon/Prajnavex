# Prajnavex v0.2 Integrity and Audit

Status: approved

Approved: 2026-06-04

## Scope

Build v0.2 around schema integrity, staleness audit, bidirectional indexes, portability, privacy discipline, and the first real bundle-to-workflow contract.

## Deliverables

- Stronger `knowledge_index.py` validation.
- New `knowledge_audit.py` operational audit.
- Updated metadata schema and templates.
- v0.2 roadmap documentation.
- Portability and privacy documentation.
- Focused tests.

## Acceptance

- Validation has zero errors on the current vault.
- Audit reports warnings without blocking normal use.
- Index output includes forward records and backlinks.
- Tests pass with the standard library test runner.
