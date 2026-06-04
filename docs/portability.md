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

## Git Hygiene

The repository should keep framework code and curated notes. Large raw assets and private captures should stay ignored or outside Git.
