"""Stable local read-only interface for Prajnavex knowledge clients."""

import argparse
import json
from pathlib import Path

from context_pack import _candidate_score, _match, _pack_item, build_context_pack
from knowledge_index import as_list, build_index, read_frontmatter

ROOT = Path(__file__).resolve().parents[1]


class KnowledgeApiError(ValueError):
    """Raised when the knowledge index cannot safely answer a request."""


def _text(value):
    if value is None or isinstance(value, list):
        return ""
    return str(value).strip()


def _load_index():
    records, errors, warnings = build_index()
    if errors:
        raise KnowledgeApiError("knowledge index has errors: " + "; ".join(errors))
    return records, warnings


def _agent_allowed(record):
    allowed = {str(item).lower() for item in as_list(record.get("allowed_consumers"))}
    return not allowed or "agent" in allowed or "both" in allowed


def _matches_filters(record, note_type=None, tags=None, domain=None, stage=None):
    if note_type and _text(record.get("type")) != note_type:
        return False
    if domain and _text(record.get("domain")) != domain:
        return False
    if stage and _text(record.get("stage")) != stage:
        return False
    wanted_tags = {tag.lower() for tag in (tags or [])}
    actual_tags = {str(tag).lower() for tag in as_list(record.get("tags"))}
    return wanted_tags.issubset(actual_tags)


def search(query="", *, note_type=None, tags=None, domain=None, stage=None, limit=20):
    """Return frontmatter-first candidate records for an agent client."""
    if limit < 1 or limit > 100:
        raise KnowledgeApiError("limit must be between 1 and 100")
    records, warnings = _load_index()
    candidates = [
        record
        for record in records
        if _agent_allowed(record)
        and _matches_filters(record, note_type, tags, domain, stage)
        and (not query or _match(record, query))
    ]
    candidates.sort(key=lambda record: (-_candidate_score(record, query), record["path"]))
    return {"query": query, "records": candidates[:limit], "warnings": warnings}


def _record_by_id(note_id):
    records, warnings = _load_index()
    for record in records:
        if _text(record.get("id")) == note_id:
            if not _agent_allowed(record):
                raise KnowledgeApiError(f"note is not available to agent clients: {note_id}")
            return record, warnings
    raise KnowledgeApiError(f"note not found: {note_id}")


def get(note_id, *, include_body=True):
    """Return one stable note by ID, optionally including its full body."""
    record, warnings = _record_by_id(note_id)
    item = _pack_item(record)
    if not include_body:
        item.pop("body", None)
        item.pop("body_truncated", None)
    else:
        path = ROOT / record["path"]
        text = path.read_text(encoding="utf-8")
        marker = text.find("\n---\n", 4)
        item["body"] = text[marker + 5 :].strip() if marker >= 0 else text.strip()
        item.pop("body_truncated", None)
    item["warnings"] = warnings
    return item


def context_pack(query, *, note_type=None, limit=5):
    """Return the bounded context-pack contract."""
    pack = build_context_pack(query, note_type, limit)
    pack["consumer"] = "agent"
    return pack


def cite(note_id):
    """Return the minimum provenance object needed for an agent citation."""
    item = get(note_id, include_body=False)
    return {
        "id": item["id"],
        "type": item["type"],
        "title": item["title"],
        "summary": item["summary"],
        "path": item["path"],
        "source_ids": item["source_ids"],
        "authority": item["authority"],
        "authority_path": item["citation"]["authority_path"],
        "last_verified": item["citation"]["last_verified"],
        "confidence": item["confidence"],
        "staleness": item["staleness"],
        "evidence": item["evidence"],
    }


def _json_command(args):
    if args.command == "search":
        return search(args.query, note_type=args.type, tags=args.tag, domain=args.domain, stage=args.stage, limit=args.limit)
    if args.command == "get":
        return get(args.id, include_body=not args.metadata_only)
    if args.command == "context-pack":
        return context_pack(args.query, note_type=args.type, limit=args.limit)
    if args.command == "cite":
        return cite(args.id)
    raise KnowledgeApiError(f"unknown command: {args.command}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--query", default="")
    search_parser.add_argument("--type", choices=("source", "card", "skill", "bundle"))
    search_parser.add_argument("--tag", action="append", default=[])
    search_parser.add_argument("--domain")
    search_parser.add_argument("--stage")
    search_parser.add_argument("--limit", type=int, default=20)

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("id")
    get_parser.add_argument("--metadata-only", action="store_true")

    pack_parser = subparsers.add_parser("context-pack")
    pack_parser.add_argument("--query", required=True)
    pack_parser.add_argument("--type", choices=("source", "card", "skill", "bundle"))
    pack_parser.add_argument("--limit", type=int, default=5)

    cite_parser = subparsers.add_parser("cite")
    cite_parser.add_argument("id")

    args = parser.parse_args()
    try:
        print(json.dumps(_json_command(args), ensure_ascii=False, indent=2))
    except KnowledgeApiError as exc:
        parser.exit(1, f"error: {exc}\n")


if __name__ == "__main__":
    main()
