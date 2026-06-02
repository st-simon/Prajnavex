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
