# Prajnavex Architecture Overview

Prajnavex | 般若维 is a local-first, model-neutral knowledge core for turning messy reading material into structured sources, cards, synthesis, skills, reusable workflows, and context packs.

Subtitle: A structured knowledge base for clear seeing.

中文副标题：以般若照见，以结构成维

## System Map

```mermaid
flowchart TD
    User["User"] --> UI["Prajnavex Web UI"]
    User --> Obsidian["Obsidian Workbench"]
    User --> Models["Codex / Claude / Model Clients"]

    UI --> Core["Prajnavex Core"]
    Obsidian --> Vault["Markdown Vault"]
    Models --> API["Knowledge API Kernel"]
    API --> Core
    Core --> Scripts["Prajnavex Scripts"]
    Core --> Vault

    Vault --> Inbox["00_inbox"]
    Vault --> Sources["10_sources"]
    Vault --> Cards["20_cards"]
    Vault --> Maps["30_maps"]
    Vault --> Skills["40_skills"]
    Vault --> Bundles["50_bundles"]
    Vault --> Archive["90_archive"]

    Scripts --> OCR["Windows OCR Adapter"]
    Scripts --> Index["JSON Index"]
    API --> Recall["Recall Protocol"]
    API --> Packs["Context Packs"]
    Models --> Vision["Vision Understanding"]
    Models --> Extraction["Semantic Extraction"]
```

## Knowledge Pipeline

```mermaid
flowchart LR
    Raw["Raw Material"] --> Inbox["Inbox"]
    Inbox --> Draft["Source Draft"]
    Draft --> Review["Human Review"]
    Review --> Source["Source"]
    Source --> Card["Knowledge Cards"]
    Card --> Skill["Skills"]
    Skill --> Bundle["Bundles"]
    Bundle --> Tool["Tools and Workflows"]
```

The pipeline separates capture from commitment. Inputs can be messy, but approved knowledge must be structured.

## Image Ingest

```mermaid
flowchart TD
    Image["Image in Inbox"] --> OCR["OCR Text"]
    Image --> Vision["Vision Summary"]
    OCR --> Cleaned["Cleaned Text"]
    Vision --> Cleaned
    Cleaned --> Draft["Source Draft"]
    Draft --> Approval["Human Approval"]
    Approval --> Source["Approved Source"]
    Source --> Cards["Cards"]
```

OCR is evidence. Vision Summary is semantic structure. Cleaned Text is the reviewed synthesis used for source and card creation.

## Component Boundaries

| Component | Responsibility |
| --- | --- |
| Prajnavex Core | Own the schema, lifecycle, validation, index, API contracts, and recall behavior. |
| Obsidian | Human workbench for reading, editing, linking, judgment, approval, and review. |
| Prajnavex Web UI | Operational client for inbox, drafts, sources, cards, skills, and approval flows. |
| Knowledge API Kernel | Stable local interface for ingestion, retrieval, review, and context-pack export. |
| Scripts | OCR, source draft creation, approval, indexing, and validation. |
| Codex / Claude / model clients | Semantic extraction, vision understanding, card synthesis, retrieval, and skill evolution proposals through stable interfaces. |
| GitHub | Public project showcase and version control. |

## Current MVP

- Markdown vault with structured folders.
- Source, card, skill, and bundle templates.
- OCR-backed image source draft workflow.
- Vision-first image ingest rules.
- Human approval before source indexing.
- Local Web UI and Windows desktop launcher.
- GitHub release tag `v0.1.0`.

## Knowledge Object Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Inbox
    Inbox --> SourceDraft
    SourceDraft --> Source: approve
    SourceDraft --> Inbox: rework
    SourceDraft --> Archive: reject
    Source --> Card: extract
    Card --> Synthesis: consolidate
    Card --> SkillDraft: promote
    SkillDraft --> SkillActive: approve
    SkillActive --> SkillRefined: update
    SkillRefined --> SkillActive: approve
    SkillActive --> Archive: supersede
```

The default rule is automation proposes, humans approve.

## Recall And Reuse Direction

The v0.4+ direction keeps the physical vault layout stable while adding a
model-neutral recall and reuse layer:

```text
surface -> trigger -> load
```

- `surface`: lightweight titles, summaries, tags, stages, and review metadata.
- `trigger`: candidate notes selected by task, tag, scenario, or query.
- `load`: full note bodies, evidence, Skills, or Bundles pulled only when
  needed.

Reusable outputs should be exported as bounded context packs rather than raw
folder reads:

- Source evidence packs.
- Card context packs.
- Skill execution packs.
- Bundle workflow packs.
