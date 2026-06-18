# Session Discovery and PDF Ingestion

Status: archived
Approved: 2026-06-18

## Background and Purpose

Repeated discovery and environment troubleshooting add avoidable round trips.
Add stable read-only discovery and deterministic PDF extraction.

## Scope and Non-goals

Add two scripts, focused tests, and documentation. Do not change Git
configuration, install dependencies, implement a custom PDF parser, or modify
Vault content.

## Approach and Alternatives

Use Python adapters, command-scoped Git trust, and supported PDF libraries.
Repository-local `safe.directory` and manual PDF stream parsing were rejected.

## Implementation, Risks, and Validation

Change `scripts/discover.py`, `scripts/extract_pdf.py`, focused tests,
`AGENTS.md`, `README.md`, and `CHANGELOG.md`. Preserve unrelated changes.
Report provider availability and fail with OCR guidance. Run discovery, tests,
index validation, audit, and Git whitespace checks.

## Done Criteria and State Transition

Discovery is single-call, ownership mismatch does not block read-only status,
project `pypdf` works, failures are actionable, and validation passes.

`proposed -> approved -> in_progress -> implemented -> verified -> archived`
