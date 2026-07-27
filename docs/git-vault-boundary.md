# Git/Vault Boundary

## Policy

Prajnavex has one local knowledge core but two storage roles:

1. The local Vault is the complete human and Agent workbench.
2. Git is the curated, reviewable, reproducible knowledge and governance set.

Therefore, import volume must not determine Git volume. Raw captures and
intermediate notes can remain local while still being indexed and retrievable
by Obsidian and the local Agent APIs.

## Storage layers

| Layer | Typical contents | Default Git policy |
| --- | --- | --- |
| Capture | `00_inbox`, raw PDFs, images, OCR output, temporary notes | local-only |
| Workbench | unreviewed Sources, Cards, Skills, Bundles, research drafts | local-first |
| Product | reviewed and stable Sources, Cards, Skills, Bundles, Maps | explicit promotion |
| Governance | schemas, templates, scripts, rules, decision records | tracked |

The `.gitignore` protects the local-first layers. Existing tracked notes remain
tracked until a deliberate cleanup or migration; `.gitignore` does not rewrite
Git history.

## Promotion gate

Promote a note to Git only when all applicable checks pass:

1. The note has stable frontmatter and an appropriate lifecycle `stage`.
2. Provenance is recorded; Cards have valid Source links and semantic links.
3. Duplicate candidates have been reviewed or explicitly accepted.
4. The note is useful beyond the current import session and its scope is clear.
5. Sensitive data and unnecessary raw binaries are absent.
6. The batch is small enough to review as one coherent change.

Run checks before staging:

```bash
python3 scripts/knowledge_index.py --check
python3 scripts/knowledge_audit.py
```

Then stage only the approved files. Because stable Vault directories are
ignored by default, use explicit force-add:

```bash
git add -f vault/10_sources/source-YYYYMMDD-slug.md
git add -f vault/20_cards/card-YYYYMMDD-slug.md
git diff --cached --name-only
git diff --cached --check
git commit -m "Promote reviewed knowledge batch"
```

Do not use `git add -f vault/` for bulk promotion. Promote a coherent batch,
review the staged diff, and leave the rest of the local workbench untouched.

## Agent behavior

The local index and Knowledge API may read ignored local notes. They should
still prefer approved, curated notes when authority and maturity are equal,
and should label unreviewed material as working knowledge. Git status is not a
knowledge-quality signal: local-only notes can be valid retrieval candidates,
while tracked notes can still require review.
