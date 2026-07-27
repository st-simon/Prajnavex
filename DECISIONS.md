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

## 2026-07-08: Prajnavex Is A Model-Neutral Knowledge Core

Status: accepted

Prajnavex should evolve as an independent, structured knowledge core rather
than as an attachment to one assistant, editor, or chat surface.

The core owns:

- the Markdown vault and frontmatter schema;
- validation, indexing, and audit rules;
- knowledge lifecycle state;
- local APIs for ingestion, retrieval, review, and export;
- recall and context-pack contracts for external clients.

Client roles are separate:

- Obsidian is the human workbench for reading, editing, linking, judgment, and
  review.
- Codex, Claude, and other models are model clients for ingestion,
  transformation, reasoning, and reuse.
- The Web UI and CLI are operational clients for review flows, batch actions,
  and local automation.

Rationale:

- A model-neutral core allows multi-channel knowledge ingestion.
- Stable APIs and context contracts allow multi-channel knowledge reuse.
- Obsidian remains valuable as the human operation window without becoming the
  system foundation.

## 2026-07-08: Recall And Context Contracts Shape v0.4+

Status: accepted

Use the referenced IT knowledge-system structure as inspiration for
Prajnavex's next architecture layer, but do not copy its client-specific
folder model.

Adopt the concepts:

- `surface`: lightweight records safe to show at session start or in menus.
- `trigger`: records recommended when task keywords, tags, or scenarios match.
- `load`: full note bodies, evidence, or workflow packs read only on demand.
- `maturity`: review and reuse readiness beyond physical folder location.
- `usage`: signals that show which knowledge is actually recalled or applied.

Keep the current vault folders stable:

```text
00_inbox -> 10_sources -> 20_cards -> 40_skills -> 50_bundles
```

Express the new structure through frontmatter, index data, API behavior, and
context-pack contracts before considering any physical directory migration.

## 2026-07-26: One Knowledge Core, Two Consumers

Status: accepted

Prajnavex serves both human and agent consumers from one Markdown/frontmatter
knowledge core. Obsidian and the Web UI optimize for reading, editing,
linking, review, and approval. Codex, Claude, and other agents use
frontmatter-first recall and bounded context packs for retrieval, citation,
and task application.

Agent clients must receive stable IDs, provenance, confidence, staleness, and
citation metadata. A context pack is read-only: it cannot promote, merge,
delete, or rewrite knowledge. Authority paths remain stronger than derived
Cards, Skills, or Bundles.

Rationale:

- One source of truth prevents divergence between human and agent libraries.
- Bounded packs reduce context waste and accidental exposure of raw Vault data.
- Explicit provenance makes agent reuse auditable.
- Human approval remains the boundary for durable knowledge changes.

## 2026-07-26: AI Collaboration Governance Domain

Status: accepted

Prajnavex contains an `ai-collaboration-governance` knowledge domain. It
organizes the principles, rules, permissions, workflows, agent roles,
experience, audit, and upgrade knowledge used across AI-assisted work.

This domain is not the workspace governance authority. The workspace
governance repository and its project/workspace rule files remain the
authoritative execution layer. Prajnavex records, explains, indexes, cites,
and packages that governance knowledge for human and agent consumers.

Codex governance is the first and currently most complete subdomain. Codex,
Claude, and other agents are represented as roles or clients within the wider
AI collaboration model rather than as the owner of the whole domain.

Rationale:

- A model-neutral name remains valid as more agents and tools are added.
- Separating authority from knowledge prevents policy drift and duplicate rule
  ownership.
- Distinguishing normative rules from descriptive knowledge and experience
  makes review and promotion safer.

## 2026-07-28: Card System v0.1 Direction

Status: accepted-for-implementation

Prajnavex keeps `type: card` as the storage envelope and adds `card_type` for
semantic classification. The initial taxonomy is `entity`, `event`, `period`,
`concept`, `mechanism`, `claim`, `work`, `comparison`, and `method`.

`method` is reusable knowledge and is not automatically a Skill. A method may
become a Skill candidate only after repeated use, stable scope, explicit
inputs/outputs, validation, and documented failure handling.

Use `sources` as the future multi-source provenance field while retaining
`source_id` during migration. Use `relations` as the canonical semantic link
map while retaining `related_cards` for compatibility. Use `stage` for
workflow lifecycle and `epistemic_status` for knowledge posture; do not add a
second generic status field.

Migration is backward-compatible: templates, validators, indexes, and existing
Cards are upgraded before expanding the taxonomy across new source material.

## 2026-07-28: Local Vault, Curated Git Boundary

Status: accepted-for-implementation

Prajnavex keeps the complete working Vault available to Obsidian and local
Agents, but Git stores only the governance framework, system code, and reviewed
knowledge products. Raw captures, attachments, drafts, archives, and
unreviewed bulk imports are local-first and ignored by default.

Stable Sources, Cards, Skills, Bundles, and Maps enter Git through an explicit
promotion gate: validate structure, audit provenance and links, review
duplicates and sensitivity, then force-add only the approved files. Existing
tracked notes are not silently untracked by this policy; cleanup is a separate
decision.

Rationale:

- prevents high-volume ingestion from turning Git history into a raw archive;
- preserves local human and Agent retrieval over the complete Vault;
- makes durable knowledge promotion reviewable and reversible;
- keeps governance and schema changes versioned independently of data volume.
