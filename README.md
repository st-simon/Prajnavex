# Prajnavex | 般若维

A structured knowledge base for clear seeing.

以般若照见，以结构成维

MVP architecture for turning reading material into structured notes, reusable skills, and tool-ready workflows.

## Pipeline

```text
raw input -> inbox -> source -> knowledge card -> skill -> bundle -> tool/workflow
```

## First Use

Open `vault/` as an Obsidian vault. Capture freely in `vault/00_inbox`, then structure items before moving them into sources, cards, skills, or bundles.

## Verification

```powershell
python scripts\knowledge_index.py --check
python scripts\knowledge_index.py --write-index
```

## Local Web UI

```powershell
python scripts\prajnavex_web.py
```

Open:

```text
http://127.0.0.1:8765
```

Keep the terminal running while using the UI.

Windows desktop launcher:

```text
C:\Users\夏骏\Desktop\Prajnavex.lnk
```
