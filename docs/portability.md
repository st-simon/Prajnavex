# Portability

Use placeholders in shared documentation:

- `<workspace-root>` for the parent Codex workspace.
- `<project-root>` for this repository.
- `<vault-root>` for `<project-root>/vault`.

Avoid committing user-specific paths such as desktop folders, drive letters, or machine usernames unless the file is explicitly local setup documentation.

## Local Setup

Open `<vault-root>` as the Obsidian vault.

Start the Web UI from `<project-root>`:

Windows PowerShell:

```powershell
python scripts\prajnavex_web.py
```

macOS/Linux:

```bash
python3 scripts/prajnavex_web.py
```

Convenience launchers are machine-specific adapters. They are not part of the portable knowledge contract:

```text
Windows: Start Prajnavex.cmd
macOS: scripts/start-prajnavex-web.command
```

## PDF Dependencies

PDF extraction uses the version pinned in `<project-root>/requirements.txt`.
Install it into the ignored project-local dependency directory:

```text
Windows: python scripts\setup_pdf_deps.py
macOS/Linux: python3 scripts/setup_pdf_deps.py
```

Check readiness without changing the environment:

```text
Windows: python scripts\setup_pdf_deps.py --check
macOS/Linux: python3 scripts/setup_pdf_deps.py --check
```

The `.deps` directory is a replaceable local adapter and must not be committed.
Scanned PDFs still require OCR; successful dependency installation does not
turn image-only pages into text.

## Git Hygiene

The repository keeps framework code and curated knowledge products. The local
Vault may contain much more: raw captures, drafts, attachments, and
unreviewed notes remain searchable by Obsidian and local Agent APIs but are
ignored by default. Promote reviewed notes explicitly with `git add -f` after
validation and audit. See [git-vault-boundary.md](git-vault-boundary.md).
