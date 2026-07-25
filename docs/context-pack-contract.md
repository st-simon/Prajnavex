# Context Pack Contract

Prajnavex serves two consumers from one knowledge core:

- Human clients read, edit, link, review, and approve Markdown notes.
- Agent clients recall, retrieve, cite, and apply bounded knowledge packs.

The storage contract remains Markdown plus frontmatter. Agents must use the
index and context-pack adapter instead of reading the whole Vault directly.

## Recall stages

```text
surface -> trigger -> load
```

- `surface`: IDs, titles, summaries, tags, stage, confidence, and freshness.
- `trigger`: candidates selected by query terms, tags, domain, or applicability.
- `load`: bounded body text plus provenance and citation metadata.

## Minimum pack shape

```json
{
  "pack_type": "bounded_context_pack",
  "query": "coding preflight",
  "generated": "YYYY-MM-DD",
  "recall": {"strategy": "frontmatter-first", "candidate_count": 1, "limit": 5},
  "items": [
    {
      "id": "stable-note-id",
      "type": "card",
      "title": "...",
      "summary": "...",
      "path": "vault/20_cards/example.md",
      "confidence": "high",
      "staleness": "fresh",
      "authority_path": "path/to/authoritative/file",
      "source_ids": ["source-id"],
      "citation": {
        "id": "stable-note-id",
        "path": "vault/20_cards/example.md",
        "authority_path": "path/to/authoritative/file",
        "last_verified": "YYYY-MM-DD"
      },
      "body": "bounded note body"
    }
  ],
  "limitations": []
}
```

## Citation and trust rules

1. Prefer an `authority_path` over a derived Card when stating a mandatory rule.
2. Treat `confidence` and `staleness` as part of the answer, not decoration.
3. Distinguish approved knowledge from drafts and discussions.
4. Do not promote, merge, delete, or rewrite notes through this read-only pack.
5. Do not include secrets or sensitive personal records in a pack.

## Local Knowledge API Kernel

The stable read-only operations are:

- `search(query, filters)`: frontmatter-first candidate records.
- `get(note_id)`: one note by stable ID.
- `context_pack(query, filters)`: bounded body plus provenance.
- `cite(note_id)`: minimum citation and trust metadata.

The CLI adapter exposes the same operations:

```bash
python3 scripts/knowledge_api.py search --query "coding" --type card --limit 5
python3 scripts/knowledge_api.py cite card-20260726-prajnavex-dual-consumer-model
```

The Python module is the first stable seam. HTTP, MCP, and model-specific
connectors remain later adapters and must consume the same contract.
