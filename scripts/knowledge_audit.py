import argparse
from datetime import date

from knowledge_index import as_list, build_index, scalar

STALE_FIELDS = {"updated", "last_verified", "review_after", "confidence", "staleness"}


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def audit_records(records, today=None):
    today = today or date.today()
    issues = []
    by_id = {scalar(record.get("id")): record for record in records if scalar(record.get("id"))}
    referenced = set()
    for record in records:
        audit_staleness_fields(record, issues, today)
        for field in ("source_id", "related_cards", "promoted_skills", "source_cards", "skills"):
            referenced.update(str(item) for item in as_list(record.get(field)))
    audit_orphans(records, by_id, referenced, issues)
    return issues


def audit_staleness_fields(record, issues, today):
    path = record["path"]
    missing = sorted(field for field in STALE_FIELDS if not scalar(record.get(field)))
    if missing:
        issues.append(("warning", path, f"missing audit fields: {', '.join(missing)}"))
    if scalar(record.get("stage")) == "archived":
        return
    review_after = scalar(record.get("review_after"))
    if review_after:
        review_date = parse_date(review_after)
        if review_date and review_date < today:
            issues.append(("warning", path, f"review_after passed: {review_after}"))
    if scalar(record.get("staleness")) == "stale":
        issues.append(("warning", path, "marked stale"))


def audit_orphans(records, by_id, referenced, issues):
    for record in records:
        note_id = scalar(record.get("id"))
        note_type = scalar(record.get("type"))
        if note_type == "card" and not scalar(record.get("source_id")):
            issues.append(("error", record["path"], "card has no source_id"))
        if note_type == "skill" and not as_list(record.get("source_cards")):
            issues.append(("warning", record["path"], "skill has no source_cards"))
        if note_type in {"card", "skill"} and note_id not in referenced:
            issues.append(("warning", record["path"], "not referenced by any higher-level note"))
    for ref_id in sorted(referenced - set(by_id)):
        issues.append(("error", ref_id, "referenced id is missing"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="exit non-zero on warnings as well as errors")
    args = parser.parse_args()
    records, validation_errors, validation_warnings = build_index()
    issues = [("error", "validation", error) for error in validation_errors]
    issues.extend(("warning", "validation", warning) for warning in validation_warnings)
    issues.extend(audit_records(records))
    for severity, target, message in issues:
        print(f"{severity}: {target}: {message}")
    errors = sum(1 for severity, _, _ in issues if severity == "error")
    warnings = sum(1 for severity, _, _ in issues if severity == "warning")
    print(f"audit issues={len(issues)} warnings={warnings} errors={errors}")
    if errors or (args.strict and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
