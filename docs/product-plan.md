# Prajnavex Lightweight Product Plan

## Product Shape

Prajnavex is a local-first, model-neutral knowledge core for turning messy
reading material into structured sources, cards, skills, bundles, and reusable
context packs.

Subtitle: A structured knowledge base for clear seeing.

Chinese subtitle: 以般若照见，以结构成维

## MVP Goal

Move daily interaction from ad hoc Codex chat commands toward a local web UI that exposes the review workflow directly.

## Next Product Direction

The next architecture phase moves Prajnavex from a local vault plus scripts to
an independent knowledge core with clients:

```text
Prajnavex Core -> API Kernel -> Model Connectors -> Reuse Protocol
```

Codex, Claude, Obsidian, the Web UI, and CLI tools should connect through
stable contracts rather than each making direct assumptions about vault files.

## Core Workflows

1. Review inbox materials.
2. Generate source drafts from images or files.
3. Review and approve source drafts.
4. Browse indexed sources, cards, and skills.
5. Inspect source/card metadata before deeper editing in Obsidian.
6. Retrieve bounded context packs for model clients and workflow reuse.

## Non-goals

- No full replacement for Obsidian editing in the MVP.
- No autonomous writes into active sources or skills without review.
- No cloud sync or user accounts.
- No investment advice engine.
- No model-specific structure in the Prajnavex core.

## MVP UI

- Dashboard counts.
- Inbox image list.
- Source draft review queue.
- Sources, cards, and skills browser.
- Markdown preview pane.
- Approve draft action.

## Technical Approach

- Python standard-library HTTP server.
- Static HTML/CSS/JavaScript frontend.
- Markdown vault remains the source of truth.
- Existing scripts remain the automation layer.
- Obsidian remains the human workbench for reading, editing, linking, and
  review.
- The Web UI and CLI are operational clients.
- Codex, Claude, and other assistants are model clients.
- v0.4 prioritizes a Knowledge API Kernel before expanding model-specific
  integrations.

## Done Criteria

- Local server starts from the project root.
- Browser UI shows inbox, drafts, sources, cards, and skills.
- User can approve a reviewed source draft from the UI.
- Knowledge index validation still passes.
