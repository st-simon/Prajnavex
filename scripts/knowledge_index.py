import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
INDEX = ROOT / "index" / "knowledge-index.json"
CHECK_DIRS = {"10_sources", "20_cards", "40_skills", "50_bundles"}

COMMON_REQUIRED = {"id", "type", "title", "summary", "tags", "stage", "created"}
TYPE_REQUIRED = {
    "source": {"source_type"},
    "card": {"source_id"},
    "skill": {"source_cards", "maturity"},
    "bundle": {"skills"},
}
TYPE_DIR = {
    "source": "10_sources",
    "card": "20_cards",
    "skill": "40_skills",
    "bundle": "50_bundles",
}
TYPE_STAGES = {
    "source": {"source-draft", "source", "archived"},
    "card": {"extracted", "promotable", "archived"},
    "skill": {"skill-draft", "skill-active", "archived"},
    "bundle": {"bundle-draft", "bundle-active", "archived"},
}
ENUMS = {
    "type": set(TYPE_DIR),
    "source_type": {"article", "pdf", "image", "book", "video", "audio", "web", "manual", "other"},
    "maturity": {"experimental", "working", "stable", "deprecated"},
    "usefulness": {"low", "medium", "high"},
    "confidence": {"low", "medium", "high", "unknown"},
    "staleness": {"fresh", "watch", "stale", "unknown"},
    "image_kind": {"screenshot", "infographic", "table", "slide", "chart", "document_scan", "social_post", "diagram", "photo", "document", "unknown"},
    "ocr_quality": {"low", "medium", "high", "unknown"},
    "extraction_strategy": {"ocr-first", "vision-first", "hybrid"},
    "review_status": {"needs-human-review", "approved", "rejected", "needs-rework"},
}
DATE_FIELDS = {"created", "updated", "last_verified", "review_after"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_FIELDS = {
    "source_id": "source",
    "related_cards": "card",
    "promoted_skills": "skill",
    "source_cards": "card",
    "skills": "skill",
}
LIST_FIELDS = {"tags", "related_cards", "promoted_skills", "source_cards", "skills", "trigger"}


def parse_value(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_value(part) for part in inner.split(",")]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    data = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = parse_value(value)
    return data


def iter_notes():
    for path in VAULT.rglob("*.md"):
        rel = path.relative_to(VAULT)
        if rel.parts and rel.parts[0] in CHECK_DIRS:
            yield path


def as_list(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [item for item in value if item != ""]
    return [value]


def scalar(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return ""
    return str(value).strip()


def record_for(path, meta):
    record = {"path": path.relative_to(ROOT).as_posix()}
    record.update(meta)
    return record


def validate_records(records):
    errors = []
    warnings = []
    by_id = {}
    counts = Counter(scalar(record.get("id")) for record in records if scalar(record.get("id")))
    for duplicated in sorted(note_id for note_id, count in counts.items() if count > 1):
        paths = [record["path"] for record in records if scalar(record.get("id")) == duplicated]
        errors.append(f"{duplicated}: duplicate id in {', '.join(paths)}")
    for record in records:
        note_id = scalar(record.get("id"))
        if note_id and note_id not in by_id:
            by_id[note_id] = record
    for record in records:
        validate_record(record, by_id, errors, warnings)
    warn_duplicate_titles(records, warnings)
    return errors, warnings


def validate_record(record, by_id, errors, warnings):
    path = record["path"]
    note_type = scalar(record.get("type"))
    missing = sorted((COMMON_REQUIRED | TYPE_REQUIRED.get(note_type, set())) - set(record))
    if missing:
        errors.append(f"{path}: missing {', '.join(missing)}")
    if note_type and note_type not in TYPE_DIR:
        errors.append(f"{path}: invalid type '{note_type}'")
        return
    expected_dir = TYPE_DIR.get(note_type)
    if expected_dir and Path(path).parts[1] != expected_dir:
        errors.append(f"{path}: type '{note_type}' belongs in vault/{expected_dir}")
    validate_stage(record, errors)
    validate_enums(record, errors)
    validate_lists(record, warnings)
    validate_dates(record, errors)
    validate_links(record, by_id, errors)


def validate_stage(record, errors):
    note_type = scalar(record.get("type"))
    stage = scalar(record.get("stage"))
    if note_type in TYPE_STAGES and stage and stage not in TYPE_STAGES[note_type]:
        allowed = ", ".join(sorted(TYPE_STAGES[note_type]))
        errors.append(f"{record['path']}: invalid stage '{stage}' for {note_type}; allowed: {allowed}")


def validate_enums(record, errors):
    for field, allowed in ENUMS.items():
        value = scalar(record.get(field))
        if field in record and value and value not in allowed:
            errors.append(f"{record['path']}: invalid {field} '{value}'")


def validate_lists(record, warnings):
    for field in LIST_FIELDS:
        if field in record and not isinstance(record[field], list):
            warnings.append(f"{record['path']}: {field} should be a list")


def validate_dates(record, errors):
    for field in DATE_FIELDS:
        value = scalar(record.get(field))
        if value and not DATE_RE.match(value):
            errors.append(f"{record['path']}: {field} must be YYYY-MM-DD")


def validate_links(record, by_id, errors):
    for field, target_type in LINK_FIELDS.items():
        for linked_id in as_list(record.get(field)):
            linked_record = by_id.get(str(linked_id))
            if not linked_record:
                errors.append(f"{record['path']}: {field} references missing id '{linked_id}'")
                continue
            if scalar(linked_record.get("type")) != target_type:
                found = scalar(linked_record.get("type"))
                errors.append(f"{record['path']}: {field} expects {target_type}, got {found} '{linked_id}'")


def warn_duplicate_titles(records, warnings):
    titles = Counter(scalar(record.get("title")).lower() for record in records if scalar(record.get("title")))
    for title, count in sorted(titles.items()):
        if count > 1:
            warnings.append(f"title '{title}' appears {count} times; check for near-duplicate notes")


def build_backlinks(records):
    backlinks = defaultdict(lambda: {"sources": [], "cards": [], "skills": [], "bundles": []})
    for record in records:
        source_id = scalar(record.get("id"))
        source_type = scalar(record.get("type"))
        if not source_id or source_type not in TYPE_DIR:
            continue
        bucket = f"{source_type}s"
        for field in LINK_FIELDS:
            for target_id in as_list(record.get(field)):
                backlinks[str(target_id)][bucket].append(source_id)
    return {key: value for key, value in sorted(backlinks.items())}


def build_index():
    records = []
    errors = []
    for path in iter_notes():
        meta = read_frontmatter(path)
        if meta is None:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: missing frontmatter")
            continue
        records.append(record_for(path, meta))
    validation_errors, warnings = validate_records(records)
    return records, errors + validation_errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-index", action="store_true")
    args = parser.parse_args()

    records, errors, warnings = build_index()
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(error)
    print(f"notes={len(records)} warnings={len(warnings)} errors={len(errors)}")

    if args.write_index:
        INDEX.parent.mkdir(exist_ok=True)
        payload = {"records": records, "backlinks": build_backlinks(records)}
        INDEX.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {INDEX.relative_to(ROOT)}")
    if args.check and errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
