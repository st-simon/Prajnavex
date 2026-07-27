# Prajnavex | 般若维

A structured knowledge base for clear seeing.

以般若照见，以结构成维

Open this folder as an Obsidian vault.

MVP rule:

```text
Capture freely in 00_inbox. Structure before moving into sources, cards, skills, or bundles.
```

## Local Vault, Curated Git

The Vault serves two purposes: it is the complete local workbench for Obsidian
and Agents, and it contains a smaller set of curated knowledge products that
are suitable for Git versioning. Git is a release and audit boundary, not a
requirement that every imported file be committed.

Use these layers:

- `00_inbox`, raw attachments, draft notes, and exploratory material are local
  capture/work files.
- Unreviewed notes under `10_sources`, `20_cards`, `40_skills`, and
  `50_bundles` may remain local and are still searchable by the local index and
  Agent APIs.
- Reviewed, stable, de-duplicated Sources, Cards, Skills, Bundles, Maps, and
  governance documents are curated knowledge products and may be promoted to
  Git explicitly.

Before promotion, run the structural and operational checks, inspect the
staged file list, then force-add only the reviewed files because the working
Vault paths are ignored by default:

```bash
python3 scripts/knowledge_index.py --check
python3 scripts/knowledge_audit.py
git add -f vault/20_cards/<reviewed-card>.md
git diff --cached --name-only
```

Do not commit credentials, private records, large raw binaries, or an entire
batch merely because it was imported. The full policy is in
`docs/git-vault-boundary.md`.
