# Workflow

## Capture

Put raw links, pasted text, screenshots, and temporary thoughts into `vault/00_inbox`.

## Screen

Move only useful items into `vault/10_sources`. Add `source.md` frontmatter before moving.

## Extract

For PDF, Markdown, and text documents, use the guided draft command:

```text
python scripts/ingest_document.py ingest <document>
```

Review the Source and Card drafts in `vault/00_inbox`. Each Card should contain
one reusable idea, method, warning, or pattern. Semantic duplicate results are
review hints, not merge decisions.

Approve the Source first, then explicitly approve selected Cards into
`vault/20_cards`.

## Promote

When a card describes a repeatable procedure, create a draft skill in `vault/40_skills`.

## Bundle

When multiple skills naturally support one larger workflow, create a bundle in `vault/50_bundles`.

## Search Rule

Agents and scripts should search frontmatter first, then read note bodies only for candidate files.
