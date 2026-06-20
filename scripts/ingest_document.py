"""Create and review Source/Card drafts from PDF, Markdown, or text documents."""

import argparse
import hashlib
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from extract_pdf import extract_pdf, format_text
from knowledge_index import build_index, read_frontmatter
from model_runtime import ModelRuntimeError, OllamaRuntime

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
INBOX = VAULT / "00_inbox"
SOURCE_DRAFTS = INBOX / "_source_drafts"
CARD_DRAFTS = INBOX / "_card_drafts"
EXTRACTED = INBOX / "_extracted"
SOURCES = VAULT / "10_sources"
CARDS = VAULT / "20_cards"
SUPPORTED_TEXT = {".txt", ".md", ".markdown"}

FINAL_SCHEMA = {
    "type": "object",
    "properties": {
        "source": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "author": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "why_save": {"type": "string"},
                "useful_ideas": {
                    "type": "array", "items": {"type": "string"}
                },
            },
            "required": [
                "title", "summary", "author", "tags",
                "why_save", "useful_ideas",
            ],
        },
        "cards": {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "core_idea": {"type": "string"},
                    "when_useful": {"type": "string"},
                    "how_to_apply": {
                        "type": "array", "items": {"type": "string"}
                    },
                    "evidence_excerpt": {"type": "string"},
                    "evidence_location": {"type": "string"},
                    "confidence": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                    },
                    "promotable": {"type": "boolean"},
                },
                "required": [
                    "title", "summary", "tags", "core_idea",
                    "when_useful", "how_to_apply", "evidence_excerpt",
                    "evidence_location", "confidence", "promotable",
                ],
            },
        },
    },
    "required": ["source", "cards"],
}

CHUNK_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "ideas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "statement": {"type": "string"},
                    "evidence_excerpt": {"type": "string"},
                    "evidence_location": {"type": "string"},
                },
                "required": [
                    "title", "statement",
                    "evidence_excerpt", "evidence_location",
                ],
            },
        },
    },
    "required": ["summary", "ideas"],
}

DUPLICATE_SCHEMA = {
    "type": "object",
    "properties": {
        "matches": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "card_index": {"type": "integer"},
                    "existing_card_id": {"type": "string"},
                    "relationship": {
                        "type": "string",
                        "enum": ["duplicate", "overlap", "related"],
                    },
                    "reason": {"type": "string"},
                    "confidence": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                    },
                },
                "required": [
                    "card_index", "existing_card_id",
                    "relationship", "reason", "confidence",
                ],
            },
        },
    },
    "required": ["matches"],
}


def quoted(value):
    return json.dumps(str(value), ensure_ascii=False)


def inline_list(values):
    return "[" + ", ".join(str(value) for value in values) + "]"


def normalize_tags(values):
    normalized = []
    for value in values or []:
        tag = re.sub(r"\s+", "-", str(value).strip().lower())
        tag = re.sub(r"[,:[\]{}]+", "-", tag)
        tag = re.sub(r"-+", "-", tag).strip("-")
        if tag and tag not in normalized:
            normalized.append(tag)
    return normalized


def single_line(value):
    return re.sub(r"\s+", " ", str(value)).strip()


def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if slug:
        return slug[:70]
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
    return f"document-{digest}"


def resolve_path(value):
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def read_document(path):
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        provider, pages = extract_pdf(path)
        return format_text(pages), "pdf", provider
    if suffix in SUPPORTED_TEXT:
        source_type = "markdown" if suffix in {".md", ".markdown"} else "text"
        return path.read_text(encoding="utf-8"), source_type, "text-reader"
    raise ValueError("supported document types: .pdf, .txt, .md, .markdown")


def split_chunks(text, limit=14000):
    paragraphs = text.split("\n\n")
    chunks = []
    current = []
    size = 0
    for paragraph in paragraphs:
        addition = len(paragraph) + 2
        if current and size + addition > limit:
            chunks.append("\n\n".join(current))
            current = []
            size = 0
        if len(paragraph) > limit:
            for start in range(0, len(paragraph), limit):
                if current:
                    chunks.append("\n\n".join(current))
                    current = []
                    size = 0
                chunks.append(paragraph[start:start + limit])
            continue
        current.append(paragraph)
        size += addition
    if current:
        chunks.append("\n\n".join(current))
    return chunks or [text]


def existing_card_catalog():
    records, errors, _ = build_index()
    if errors:
        raise ValueError("knowledge index has errors; fix them before ingestion")
    return [
        {
            "id": record["id"],
            "title": record["title"],
            "summary": record["summary"],
        }
        for record in records if record.get("type") == "card"
    ]


def analyze_document(runtime, text, title_hint, author_hint, role="reasoner"):
    chunks = split_chunks(text)
    if len(chunks) == 1:
        evidence = chunks[0]
    else:
        chunk_results = []
        for number, chunk in enumerate(chunks, 1):
            prompt = (
                "Extract only claims supported by this document chunk. "
                "Keep evidence excerpts short and exact. "
                f"Label locations as chunk {number} or preserve page labels.\n\n"
                f"JSON schema:\n{json.dumps(CHUNK_SCHEMA, ensure_ascii=False)}"
                f"\n\nDOCUMENT CHUNK {number}:\n{chunk}"
            )
            chunk_results.append(runtime.generate_structured(
                prompt, CHUNK_SCHEMA, role="fast"
            ))
        evidence = json.dumps(chunk_results, ensure_ascii=False)
    prompt = (
        "You are drafting structured knowledge for Prajnavex. "
        "Use the document's language. Create one Source and 2-8 Cards. "
        "Each Card must contain exactly one reusable idea, method, warning, "
        "or pattern. Do not invent facts. Evidence excerpts must be short and "
        "traceable to the supplied evidence. Prefer fewer strong Cards over "
        "many weak Cards. Return only data matching the JSON schema.\n\n"
        f"Title hint: {title_hint}\nAuthor hint: {author_hint or 'unknown'}\n"
        f"JSON schema:\n{json.dumps(FINAL_SCHEMA, ensure_ascii=False)}\n\n"
        f"DOCUMENT EVIDENCE:\n{evidence}"
    )
    result = runtime.generate_structured(prompt, FINAL_SCHEMA, role=role)
    validate_analysis(result)
    return result


def validate_analysis(result):
    source = result.get("source")
    cards = result.get("cards")
    if not isinstance(source, dict) or not isinstance(cards, list):
        raise ValueError("model output must contain source and cards")
    if not source.get("title") or not source.get("summary"):
        raise ValueError("model output source is missing title or summary")
    if not 1 <= len(cards) <= 8:
        raise ValueError("model output must contain 1-8 card candidates")
    source["title"] = single_line(source["title"])
    source["summary"] = single_line(source["summary"])
    source["author"] = single_line(source.get("author", ""))
    source["tags"] = normalize_tags(source.get("tags", []))
    source["useful_ideas"] = [
        single_line(item) for item in source.get("useful_ideas", [])
        if single_line(item)
    ]
    for card in cards:
        if not card.get("title") or not card.get("core_idea"):
            raise ValueError("card candidate is missing title or core idea")
        for field in (
            "title", "summary", "core_idea", "when_useful",
            "evidence_excerpt", "evidence_location",
        ):
            card[field] = single_line(card.get(field, ""))
        card["tags"] = normalize_tags(card.get("tags", []))
        card["how_to_apply"] = [
            single_line(item) for item in card.get("how_to_apply", [])
            if single_line(item)
        ]


def detect_duplicates(runtime, cards):
    catalog = existing_card_catalog()
    if not catalog:
        return []
    proposed = [
        {
            "card_index": index,
            "title": card["title"],
            "summary": card["summary"],
            "core_idea": card["core_idea"],
        }
        for index, card in enumerate(cards)
    ]
    prompt = (
        "Compare proposed knowledge Cards with the existing catalog by meaning, "
        "not only wording. Report only plausible duplicate, overlap, or related "
        "matches. A duplicate expresses substantially the same reusable claim; "
        "overlap shares an important claim but adds material scope; related is "
        "useful context but should remain separate. Never merge anything. "
        "Return only the JSON schema.\n\n"
        f"JSON schema:\n{json.dumps(DUPLICATE_SCHEMA, ensure_ascii=False)}\n\n"
        f"EXISTING CARDS:\n{json.dumps(catalog, ensure_ascii=False)}\n\n"
        f"PROPOSED CARDS:\n{json.dumps(proposed, ensure_ascii=False)}"
    )
    result = runtime.generate_structured(
        prompt, DUPLICATE_SCHEMA, role="fast"
    )
    valid_ids = {item["id"] for item in catalog}
    return [
        match for match in result.get("matches", [])
        if match.get("existing_card_id") in valid_ids
        and isinstance(match.get("card_index"), int)
        and 0 <= match["card_index"] < len(cards)
    ]


def all_note_ids():
    records, _, _ = build_index()
    ids = {record.get("id") for record in records}
    for directory in (SOURCE_DRAFTS, CARD_DRAFTS):
        if not directory.exists():
            continue
        for path in directory.rglob("*.md"):
            meta = read_frontmatter(path) or {}
            ids.add(meta.get("id"))
    return {item for item in ids if item}


def unique_id(prefix, title, used=None):
    used = used if used is not None else all_note_ids()
    base = f"{prefix}-{date.today():%Y%m%d}-{slugify(title)}"
    candidate = base
    number = 2
    while candidate in used:
        candidate = f"{base}-{number}"
        number += 1
    used.add(candidate)
    return candidate


def review_date():
    return date.today() + timedelta(days=90)


def render_source_draft(meta, evidence_path, card_ids):
    source = meta["source"]
    useful_ideas = source.get("useful_ideas", [])
    lines = [
        "---",
        f"id: {meta['source_id']}",
        "type: source",
        f"title: {quoted(source['title'])}",
        f"summary: {quoted(source['summary'])}",
        f"tags: {inline_list(source.get('tags', []))}",
        "stage: source-draft",
        f"source_type: {meta['source_type']}",
        f"source_url: {quoted(meta['source_url'])}",
        f"author: {quoted(source.get('author') or meta['author'])}",
        f"created: {date.today().isoformat()}",
        f"updated: {date.today().isoformat()}",
        f"last_verified: {date.today().isoformat()}",
        f"review_after: {review_date().isoformat()}",
        "confidence: medium",
        "staleness: fresh",
        "usefulness: high",
        "related_cards: []",
        "promoted_skills: []",
        "review_status: needs-human-review",
        f"ingest_status: {meta['ingest_status']}",
        f"source_file: {quoted(meta['source_file'])}",
        f"local_evidence: {quoted(evidence_path.relative_to(VAULT).as_posix())}",
        "---",
        "",
        f"# {source['title']}",
        "",
        "## Review Checklist",
        "",
        "- Confirm title, author, summary, tags, and source URL.",
        "- Read the evidence file and verify all claims.",
        "- Review each Card candidate and duplicate warning.",
        "- Approve this Source before approving its Cards.",
        "",
        "## Why Save",
        "",
        source.get("why_save", ""),
        "",
        "## Useful Ideas",
        "",
    ]
    lines.extend(f"- {idea}" for idea in useful_ideas)
    lines.extend([
        "",
        "## Card Candidates",
        "",
    ])
    lines.extend(f"- [[{card_id}]]" for card_id in card_ids)
    lines.extend([
        "",
        "## Evidence",
        "",
        f"Local extracted text: `{evidence_path.relative_to(VAULT).as_posix()}`",
        "",
    ])
    return "\n".join(lines)


def render_card_draft(card, card_id, source_id, source_url, matches):
    duplicate_ids = [match["existing_card_id"] for match in matches]
    apply_steps = card.get("how_to_apply", [])
    lines = [
        "---",
        f"id: {card_id}",
        "type: card",
        f"title: {quoted(card['title'])}",
        f"summary: {quoted(card['summary'])}",
        f"tags: {inline_list(card.get('tags', []))}",
        "stage: extracted",
        f"source_id: {quoted(source_id)}",
        f"source_url: {quoted(source_url)}",
        f"created: {date.today().isoformat()}",
        f"updated: {date.today().isoformat()}",
        f"last_verified: {date.today().isoformat()}",
        f"review_after: {review_date().isoformat()}",
        f"confidence: {card.get('confidence', 'medium')}",
        "staleness: fresh",
        "usefulness: high",
        "actionability: reference",
        f"promotable: {str(bool(card.get('promotable'))).lower()}",
        "review_status: needs-human-review",
        f"duplicate_candidates: {inline_list(duplicate_ids)}",
        "---",
        "",
        f"# {card['title']}",
        "",
        "## Core Idea",
        "",
        card["core_idea"],
        "",
        "## When Useful",
        "",
        card["when_useful"],
        "",
        "## How To Apply",
        "",
    ]
    lines.extend(f"- {step}" for step in apply_steps)
    lines.extend([
        "",
        "## Evidence",
        "",
        f"> {card['evidence_excerpt']}",
        "",
        f"Location: {card['evidence_location']}",
        "",
        "## Duplicate Review",
        "",
    ])
    if matches:
        for match in matches:
            lines.append(
                f"- `{match['existing_card_id']}` — "
                f"{match['relationship']} / {match['confidence']}: "
                f"{match['reason']}"
            )
    else:
        lines.append("- No likely semantic duplicate was reported.")
    lines.append("")
    return "\n".join(lines)


def placeholder_analysis(title, author):
    return {
        "source": {
            "title": title,
            "summary": "TODO: run semantic analysis or write a reviewed summary.",
            "author": author,
            "tags": ["document", "needs-review"],
            "why_save": "TODO: explain why this source belongs in Prajnavex.",
            "useful_ideas": [],
        },
        "cards": [],
    }


def ingest(path, title=None, author="", source_url="", source_only=False,
           role="reasoner", runtime=None):
    path = resolve_path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    text, source_type, provider = read_document(path)
    if not text.strip():
        raise ValueError("document extraction returned no text")
    title_hint = title or path.stem
    source_id = unique_id("source", title_hint)
    SOURCE_DRAFTS.mkdir(parents=True, exist_ok=True)
    CARD_DRAFTS.mkdir(parents=True, exist_ok=True)
    EXTRACTED.mkdir(parents=True, exist_ok=True)
    evidence_path = EXTRACTED / f"{source_id}.txt"
    evidence_path.write_text(text, encoding="utf-8")

    warning = None
    ingest_status = "text-only"
    analysis = placeholder_analysis(title_hint, author)
    duplicates = []
    if not source_only:
        runtime = runtime or OllamaRuntime()
        try:
            analysis = analyze_document(
                runtime, text, title_hint, author, role=role
            )
            duplicates = detect_duplicates(runtime, analysis["cards"])
            ingest_status = "semantic-draft"
        except (ModelRuntimeError, ValueError) as exc:
            ingest_status = "pending-model"
            warning = str(exc)

    used = all_note_ids()
    card_ids = [
        unique_id("card", card["title"], used)
        for card in analysis["cards"]
    ]
    meta = {
        "source_id": source_id,
        "source_type": source_type,
        "source_url": source_url,
        "author": author,
        "source_file": path.name,
        "provider": provider,
        "ingest_status": ingest_status,
        "source": analysis["source"],
    }
    source_path = SOURCE_DRAFTS / f"{source_id}.md"
    source_path.write_text(
        render_source_draft(meta, evidence_path, card_ids),
        encoding="utf-8",
    )

    matches_by_index = {}
    for match in duplicates:
        matches_by_index.setdefault(match["card_index"], []).append(match)
    card_directory = CARD_DRAFTS / source_id
    card_paths = []
    if analysis["cards"]:
        card_directory.mkdir(parents=True, exist_ok=True)
    for index, (card, card_id) in enumerate(zip(analysis["cards"], card_ids)):
        card_path = card_directory / f"{card_id}.md"
        card_path.write_text(
            render_card_draft(
                card, card_id, source_id, source_url,
                matches_by_index.get(index, []),
            ),
            encoding="utf-8",
        )
        card_paths.append(card_path)
    return {
        "source_draft": source_path.relative_to(ROOT).as_posix(),
        "card_drafts": [
            item.relative_to(ROOT).as_posix() for item in card_paths
        ],
        "evidence": evidence_path.relative_to(ROOT).as_posix(),
        "provider": provider,
        "ingest_status": ingest_status,
        "warning": warning,
    }


def ensure_within(path, directory):
    path = resolve_path(path)
    directory = directory.resolve()
    if directory not in path.parents:
        raise ValueError(f"draft must be inside {directory.relative_to(ROOT)}")
    return path


def set_frontmatter_field(text, key, value):
    rendered = str(value)
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(f"{key}: {rendered}", text, count=1)
    marker = text.find("\n---\n", 4)
    if marker == -1:
        raise ValueError("draft has no valid frontmatter")
    return text[:marker] + f"\n{key}: {rendered}" + text[marker:]


def validate_draft(path, expected_type, for_approval=False):
    meta = read_frontmatter(path)
    if not meta:
        raise ValueError("draft has no frontmatter")
    required = {
        "id", "type", "title", "summary", "tags", "stage", "created",
        "updated", "last_verified", "review_after", "confidence", "staleness",
    }
    missing = sorted(field for field in required if not meta.get(field))
    if missing:
        raise ValueError(f"draft missing fields: {', '.join(missing)}")
    if meta.get("type") != expected_type:
        raise ValueError(f"expected {expected_type} draft")
    if for_approval and str(meta.get("summary", "")).startswith("TODO:"):
        raise ValueError("replace the TODO summary before approval")
    return meta


def approve_source(path):
    path = ensure_within(path, SOURCE_DRAFTS)
    meta = validate_draft(path, "source", for_approval=True)
    if meta.get("stage") != "source-draft":
        raise ValueError("Source draft must have stage: source-draft")
    text = path.read_text(encoding="utf-8")
    text = set_frontmatter_field(text, "stage", "source")
    text = set_frontmatter_field(text, "review_status", "approved")
    destination = SOURCES / f"{meta['id']}.md"
    if destination.exists():
        raise FileExistsError(destination)
    SOURCES.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    path.unlink()
    return destination


def add_related_card(source_path, card_id):
    text = source_path.read_text(encoding="utf-8")
    meta = read_frontmatter(source_path) or {}
    related = meta.get("related_cards") or []
    if not isinstance(related, list):
        related = [related]
    if card_id not in related:
        related.append(card_id)
    text = set_frontmatter_field(
        text, "related_cards", inline_list(related)
    )
    source_path.write_text(text, encoding="utf-8")


def approve_card(path):
    path = ensure_within(path, CARD_DRAFTS)
    meta = validate_draft(path, "card", for_approval=True)
    if meta.get("stage") not in {"extracted", "promotable"}:
        raise ValueError("Card draft must have stage: extracted or promotable")
    source_id = meta.get("source_id")
    source_path = SOURCES / f"{source_id}.md"
    if not source_path.exists():
        raise ValueError("approve the linked Source before approving this Card")
    text = path.read_text(encoding="utf-8")
    text = set_frontmatter_field(text, "review_status", "approved")
    destination = CARDS / f"{meta['id']}.md"
    if destination.exists():
        raise FileExistsError(destination)
    CARDS.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    add_related_card(source_path, meta["id"])
    path.unlink()
    return destination


def set_review_status(path, status):
    allowed = {"needs-human-review", "needs-rework", "rejected"}
    if status not in allowed:
        raise ValueError(f"status must be one of: {', '.join(sorted(allowed))}")
    path = resolve_path(path)
    if not any(
        directory.resolve() in path.parents
        for directory in (SOURCE_DRAFTS, CARD_DRAFTS)
    ):
        raise ValueError("review status applies only to Inbox drafts")
    text = set_frontmatter_field(
        path.read_text(encoding="utf-8"), "review_status", status
    )
    path.write_text(text, encoding="utf-8")
    return path


def list_drafts():
    source_paths = sorted(SOURCE_DRAFTS.glob("*.md")) \
        if SOURCE_DRAFTS.exists() else []
    card_paths = sorted(CARD_DRAFTS.rglob("*.md")) \
        if CARD_DRAFTS.exists() else []
    return {
        "sources": [path.relative_to(ROOT).as_posix() for path in source_paths],
        "cards": [path.relative_to(ROOT).as_posix() for path in card_paths],
    }


def validate_all_drafts():
    errors = []
    drafts = list_drafts()
    for value in drafts["sources"]:
        path = ROOT / value
        try:
            meta = validate_draft(path, "source")
            if meta.get("stage") != "source-draft":
                raise ValueError("Source draft stage must be source-draft")
            evidence = meta.get("local_evidence")
            if evidence and not (VAULT / evidence).is_file():
                raise ValueError(f"missing local evidence: {evidence}")
        except (OSError, ValueError) as exc:
            errors.append(f"{value}: {exc}")
    for value in drafts["cards"]:
        path = ROOT / value
        try:
            meta = validate_draft(path, "card")
            if meta.get("stage") not in {"extracted", "promotable"}:
                raise ValueError("Card draft stage must be extracted or promotable")
            if not meta.get("source_id"):
                raise ValueError("Card draft is missing source_id")
        except (OSError, ValueError) as exc:
            errors.append(f"{value}: {exc}")
    return {"drafts": drafts, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser(
        "ingest", help="Create Source and Card drafts from a document."
    )
    ingest_parser.add_argument("document")
    ingest_parser.add_argument("--title")
    ingest_parser.add_argument("--author", default="")
    ingest_parser.add_argument("--source-url", default="")
    ingest_parser.add_argument(
        "--source-only", action="store_true",
        help="Extract text and create a Source draft without model calls.",
    )
    ingest_parser.add_argument(
        "--role", default="reasoner",
        choices=["fast", "general", "reasoner"],
    )

    approve_source_parser = subparsers.add_parser("approve-source")
    approve_source_parser.add_argument("draft")

    approve_card_parser = subparsers.add_parser("approve-card")
    approve_card_parser.add_argument("draft")

    status_parser = subparsers.add_parser("set-status")
    status_parser.add_argument("draft")
    status_parser.add_argument(
        "status",
        choices=["needs-human-review", "needs-rework", "rejected"],
    )

    subparsers.add_parser("list", help="List pending Source and Card drafts.")
    subparsers.add_parser(
        "validate", help="Validate pending draft structure and evidence links."
    )
    args = parser.parse_args()

    try:
        if args.command == "ingest":
            result = ingest(
                args.document,
                title=args.title,
                author=args.author,
                source_url=args.source_url,
                source_only=args.source_only,
                role=args.role,
            )
        elif args.command == "approve-source":
            path = approve_source(args.draft)
            result = {"approved_source": path.relative_to(ROOT).as_posix()}
        elif args.command == "approve-card":
            path = approve_card(args.draft)
            result = {"approved_card": path.relative_to(ROOT).as_posix()}
        elif args.command == "set-status":
            path = set_review_status(args.draft, args.status)
            result = {
                "draft": path.relative_to(ROOT).as_posix(),
                "review_status": args.status,
            }
        elif args.command == "list":
            result = list_drafts()
        else:
            result = validate_all_drafts()
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if result["errors"] else 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
