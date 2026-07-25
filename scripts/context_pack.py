"""Build bounded context packs for human and agent clients.

The pack builder deliberately uses the existing frontmatter-first index. It is
an adapter, not a second knowledge store and not an autonomous writer.
"""

import argparse
import json
from datetime import date
from pathlib import Path

from knowledge_index import as_list, build_index, read_frontmatter

ROOT = Path(__file__).resolve().parents[1]
MAX_BODY_CHARS = 4000


def _text(value):
    if value is None or isinstance(value, list):
        return ""
    return str(value).strip()


def _match(record, query):
    haystack = " ".join(
        [_text(record.get(field)) for field in ("id", "title", "summary", "domain", "applicability")]
        + [str(item) for field in ("tags", "trigger") for item in as_list(record.get(field))]
    ).lower()
    return all(term.lower() in haystack for term in query.split() if term.strip())


def _candidate_score(record, query):
    terms = [term.lower() for term in query.split() if term.strip()]
    exact_fields = ("title", "summary", "domain", "applicability")
    score = 0
    for term in terms:
        if any(term in _text(record.get(field)).lower() for field in exact_fields):
            score += 3
        if any(term in str(item).lower() for field in ("tags", "trigger") for item in as_list(record.get(field))):
            score += 2
        if term in _text(record.get("id")).lower():
            score += 1
    if _text(record.get("staleness")) == "fresh":
        score += 1
    if _text(record.get("stage")) == "archived":
        score -= 5
    return score


def _body(path):
    text = path.read_text(encoding="utf-8")
    marker = text.find("\n---\n", 4)
    return text[marker + 5 :].strip() if marker >= 0 else text.strip()


def _pack_item(record):
    path = ROOT / record["path"]
    meta = read_frontmatter(path) or {}
    item = {
        "id": _text(record.get("id")),
        "type": _text(record.get("type")),
        "title": _text(record.get("title")),
        "summary": _text(record.get("summary")),
        "path": record["path"],
        "tags": as_list(record.get("tags")),
        "stage": _text(record.get("stage")),
        "confidence": _text(record.get("confidence")) or "unknown",
        "staleness": _text(record.get("staleness")) or "unknown",
        "applicability": _text(record.get("applicability")),
        "authority": _text(record.get("authority")),
        "authority_path": _text(record.get("authority_path")),
        "source_ids": as_list(record.get("source_cards")) or as_list(record.get("source_id")),
        "evidence": as_list(record.get("evidence")),
    }
    item["citation"] = {
        "id": item["id"],
        "path": item["path"],
        "authority_path": item["authority_path"] or item["path"],
        "last_verified": _text(record.get("last_verified")),
    }
    item["body"] = _body(path)[:MAX_BODY_CHARS]
    if len(_body(path)) > MAX_BODY_CHARS:
        item["body_truncated"] = True
    return item


def build_context_pack(query, note_type=None, limit=5):
    records, errors, warnings = build_index()
    if errors:
        raise ValueError("knowledge index has errors: " + "; ".join(errors))
    candidates = [record for record in records if (not note_type or _text(record.get("type")) == note_type) and _match(record, query)]
    candidates.sort(key=lambda record: (-_candidate_score(record, query), record["path"]))
    items = [_pack_item(record) for record in candidates[:limit]]
    return {
        "pack_type": "bounded_context_pack",
        "query": query,
        "generated": date.today().isoformat(),
        "recall": {"strategy": "frontmatter-first", "candidate_count": len(candidates), "limit": limit},
        "items": items,
        "warnings": warnings,
        "limitations": [
            "This pack is read-only and does not promote or modify notes.",
            "Authority paths and citations should be checked before making consequential claims.",
            "Only bounded note bodies are included; the raw Vault is not exposed as a whole.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--type", choices=("source", "card", "skill", "bundle"))
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 50:
        parser.error("--limit must be between 1 and 50")
    print(json.dumps(build_context_pack(args.query, args.type, args.limit), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
