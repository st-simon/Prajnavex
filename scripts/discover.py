"""Read-only, single-call project discovery for Prajnavex."""

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from importlib.machinery import PathFinder
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
DEPS = ROOT / ".deps"
VAULT_DIRS = (
    "00_inbox", "10_sources", "20_cards", "30_maps",
    "40_skills", "50_bundles", "90_archive", "assets",
)
PDF_MODULES = ("pypdf", "pdfplumber", "fitz", "PyPDF2")
MODEL_CONFIG = ROOT / "config" / "model_roles.json"


def find_pdf_providers():
    providers = []
    for name in PDF_MODULES:
        spec = importlib.util.find_spec(name)
        if spec:
            providers.append({"module": name, "source": "environment"})
        elif DEPS.is_dir() and PathFinder.find_spec(name, [str(DEPS)]):
            providers.append({"module": name, "source": "project .deps"})
    return providers


def git_status():
    command = [
        "git", "-c", f"safe.directory={ROOT.as_posix()}",
        "-C", str(ROOT), "status", "--porcelain",
    ]
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=10
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "clean": None, "error": str(exc)}
    return {
        "available": result.returncode == 0,
        "clean": result.returncode == 0 and not result.stdout.strip(),
        "changed_paths": len(result.stdout.splitlines()),
        "error": result.stderr.strip() or None,
        "trust": "command-scoped safe.directory; no config changed",
    }


def vault_layout():
    report = {}
    for name in VAULT_DIRS:
        path = VAULT / name
        report[name] = {
            "exists": path.is_dir(),
            "markdown_files": sum(1 for _ in path.rglob("*.md"))
            if path.is_dir() else 0,
        }
    return report


def template_state():
    expected = {"source.md", "card.md", "skill.md", "bundle.md"}
    found = {path.name for path in (ROOT / "templates").glob("*.md")}
    return {"present": sorted(found), "missing": sorted(expected - found)}


def model_state():
    if not MODEL_CONFIG.is_file():
        return {"configured": False, "server": False, "models": [], "roles": {}}
    config = json.loads(MODEL_CONFIG.read_text(encoding="utf-8"))
    if not shutil.which("ollama"):
        return {
            "configured": True,
            "server": False,
            "models": [],
            "roles": config.get("roles", {}),
            "error": "ollama CLI not found",
        }
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=10
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "configured": True,
            "server": False,
            "models": [],
            "roles": config.get("roles", {}),
            "error": str(exc),
        }
    models = [
        line.split()[0] for line in result.stdout.splitlines()[1:]
        if line.strip()
    ]
    return {
        "configured": True,
        "server": result.returncode == 0,
        "models": models,
        "roles": config.get("roles", {}),
        "error": result.stderr.strip() or None,
    }


def discover():
    providers = find_pdf_providers()
    return {
        "project_root": str(ROOT),
        "python": sys.version.split()[0],
        "git": git_status(),
        "pdf": {
            "providers": providers,
            "status": "ready" if providers else "install-required",
            "asset_dir": "vault/assets/source-pdfs",
            "extract_command": "python scripts/extract_pdf.py <pdf>",
            "install_command": "python scripts/setup_pdf_deps.py",
            "dependency_file": "requirements.txt",
            "fallback": "Use OCR when extracted text is empty.",
        },
        "vault": vault_layout(),
        "templates": template_state(),
        "models": model_state(),
        "schema": "docs/schema.md",
        "vault_rules": "vault/_README.md",
        "index_exists": (ROOT / "index" / "knowledge-index.json").exists(),
    }


def render(report):
    git = report["git"]
    providers = report["pdf"]["providers"]
    lines = [
        f"project_root: {report['project_root']}",
        f"python: {report['python']}",
        f"git: {'clean' if git.get('clean') else 'has changes'} "
        f"({git.get('changed_paths', 0)} paths)",
        f"git_trust: {git.get('trust', git.get('error'))}",
        "pdf_providers: " + (
            ", ".join(f"{p['module']} ({p['source']})" for p in providers)
            if providers else "none"
        ),
        f"pdf_status: {report['pdf']['status']}",
        f"pdf_setup: {report['pdf']['install_command']}",
        f"schema: {report['schema']}",
        f"vault_rules: {report['vault_rules']}",
        f"index_exists: {report['index_exists']}",
    ]
    missing = report["templates"]["missing"]
    lines.append(f"templates_missing: {missing or 'none'}")
    model_report = report["models"]
    lines.append(
        "ollama_status: " + (
            "ready" if model_report.get("server") else "unavailable"
        )
    )
    lines.append(
        "ollama_models: " + (
            ", ".join(model_report.get("models", [])) or "none"
        )
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = discover()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render(report))


if __name__ == "__main__":
    main()
