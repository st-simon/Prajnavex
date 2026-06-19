# Prajnavex v0.3 Guided Source and Card Drafting

Status: approved

Approved: 2026-06-20
Start condition: Prajnavex v0.2 is verified.

## Goal

Turn raw documents into reviewable Source and Card drafts through a repeatable,
human-approved workflow.

## Scope

- Unified document intake after text extraction.
- Source draft generation.
- Card candidate generation with source evidence.
- Advisory semantic duplicate detection.
- Human approve, edit, reject, and rework states.
- Golden-set regression checks using existing representative sources.

## Non-goals

- No autonomous promotion into stable Sources, Cards, or Skills.
- No automatic semantic merging.
- No vector database requirement in the first v0.3 slice.
- No v0.3 implementation before v0.2 verification.

## Acceptance

- One real PDF completes the draft workflow.
- Drafts pass schema validation before approval.
- Each Card candidate traces to its Source and supporting evidence.
- Duplicate detection produces warnings without silently merging content.
- Existing golden examples do not materially regress.
