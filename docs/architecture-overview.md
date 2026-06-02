# Prajnavex Architecture Overview

Prajnavex | 般若维 is a local-first knowledge system for turning messy reading material into structured sources, cards, synthesis, skills, and reusable workflows.

Subtitle: A structured knowledge base for clear seeing.

中文副标题：以般若照见，以结构成维

## System Map

```mermaid
flowchart TD
    User["User"] --> UI["Prajnavex Web UI"]
    User --> Obsidian["Obsidian Vault Editor"]
    User --> Codex["Codex / LLM Assistant"]

    UI --> API["Local Python Web API"]
    API --> Scripts["Prajnavex Scripts"]
    Scripts --> Vault["Markdown Vault"]
    Obsidian --> Vault
    Codex --> Vault

    Vault --> Inbox["00_inbox"]
    Vault --> Sources["10_sources"]
    Vault --> Cards["20_cards"]
    Vault --> Maps["30_maps"]
    Vault --> Skills["40_skills"]
    Vault --> Bundles["50_bundles"]
    Vault --> Archive["90_archive"]

    Scripts --> OCR["Windows OCR Adapter"]
    Scripts --> Index["JSON Index"]
    Codex --> Vision["Vision Understanding"]
    Codex --> Extraction["Semantic Extraction"]
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
| Obsidian | Read, edit, and manually review Markdown vault content. |
| Prajnavex Web UI | Browse inbox, drafts, sources, cards, and skills. |
| Python API | Serve local UI and call project scripts. |
| Scripts | OCR, source draft creation, approval, indexing, and validation. |
| Codex / LLM | High-quality semantic extraction, vision understanding, card synthesis, and skill evolution proposals. |
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
