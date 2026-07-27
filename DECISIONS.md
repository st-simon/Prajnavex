# Decisions

## 2026-06-01: Project Naming

Status: accepted

Official name: Prajnavex | 般若维

English subtitle: A structured knowledge base for clear seeing.

Chinese subtitle: 以般若照见，以结构成维

## 2026-06-01: MVP Knowledge Architecture

Status: accepted

Use a layered knowledge pipeline inspired by Hermes-style skills, without importing third-party skill content directly.

```text
inbox -> source -> card -> skill -> bundle
```

Rationale:

- Obsidian is the editing and browsing surface.
- Markdown with frontmatter remains portable.
- Stable metadata lets scripts and agents search before reading long note bodies.
- Skills represent repeatable procedures, not every useful article.

## 2026-06-01: Frontmatter First

Status: accepted

Every source, card, skill, and bundle must carry a small stable frontmatter block. Frontmatter is the machine-readable index layer; Markdown body is the human reading layer.

## 2026-06-02: Image Ingest Is Vision-First

Status: accepted

For images, Prajnavex uses a dual-track ingest model:

```text
OCR Text -> evidence
Vision Summary -> semantic structure
Cleaned Text -> reviewed usable knowledge
```

OCR is not the primary knowledge extraction layer for screenshots, information graphics, slides, charts, tables, or social posts. For those image types, use `vision-first` or `hybrid` extraction and require human approval before source indexing.


## 2026-07-28: Card System v0.1 Direction

Status: accepted-for-design

Prajnavex will keep `type: card` as the storage envelope and add `card_type` for semantic classification. The initial taxonomy is `entity`, `event`, `period`, `concept`, `mechanism`, `claim`, `work`, `comparison`, and `method`.

`method` is a first-class knowledge card and is not automatically a Skill. A method may become a Skill candidate only after repeated use, stable scope, validation, explicit inputs/outputs, and failure handling. `sources` will become the future multi-source provenance field, while `source_id` remains backward-compatible during migration. `relations` will be the canonical semantic link structure; `related_cards` remains a compatibility field until the validator and index are upgraded.

See `proposals/active/20260728-prajnavex-card-system-v01.md` for the scoped design record.
