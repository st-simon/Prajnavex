import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
INDEX = ROOT / "index" / "knowledge-index.json"
REQUIRED = {"id", "type", "title", "summary", "tags", "stage", "created"}
CHECK_DIRS = {"10_sources", "20_cards", "40_skills", "50_bundles"}


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    data = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def iter_notes():
    for path in VAULT.rglob("*.md"):
        rel = path.relative_to(VAULT)
        if rel.parts and rel.parts[0] in CHECK_DIRS:
            yield path


def build_index():
    records = []
    errors = []
    for path in iter_notes():
        rel = path.relative_to(ROOT).as_posix()
        meta = read_frontmatter(path)
        if meta is None:
            errors.append(f"{rel}: missing frontmatter")
            continue
        missing = sorted(REQUIRED - set(meta))
        if missing:
            errors.append(f"{rel}: missing {', '.join(missing)}")
        records.append({"path": rel, **meta})
    return records, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-index", action="store_true")
    args = parser.parse_args()
    records, errors = build_index()
    for error in errors:
        print(error)
    print(f"notes={len(records)} errors={len(errors)}")
    if args.write_index:
        INDEX.parent.mkdir(exist_ok=True)
        INDEX.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {INDEX.relative_to(ROOT)}")
    if args.check and errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
