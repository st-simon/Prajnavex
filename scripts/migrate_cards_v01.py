"""Migrate Card notes to the backward-compatible Card System v0.1 fields."""

import argparse
import re
from pathlib import Path

from knowledge_index import as_list, read_frontmatter, scalar

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "vault" / "20_cards"


def infer_card_type(meta):
    tags = {str(tag).lower() for tag in as_list(meta.get("tags"))}
    title = scalar(meta.get("title")).lower()
    kind = scalar(meta.get("knowledge_kind")).lower()
    if kind in {"procedural", "audit", "knowledge-lifecycle"} or tags & {"workflow", "checklist", "method"}:
        return "method"
    if tags & {"event", "war", "rebellion"} or "事件" in title:
        return "event"
    if tags & {"period", "periodization"} or "时期" in title:
        return "period"
    if tags & {"comparison", "contrast"} or "对比" in title:
        return "comparison"
    if tags & {"claim", "thesis", "hypothesis"}:
        return "claim"
    if tags & {"mechanism", "process", "feedback-loop"}:
        return "mechanism"
    return "concept"


def _render_ids(values):
    return "[" + ", ".join(str(value) for value in values) + "]"


def _render_relations(values):
    if not values:
        return "{}"
    return "{related_to: " + _render_ids(values) + "}"


def migrate(path, apply=False):
    text = path.read_text(encoding="utf-8")
    meta = read_frontmatter(path) or {}
    if not meta or meta.get("type") != "card":
        return False
    source_id = scalar(meta.get("source_id"))
    sources = as_list(meta.get("sources")) or ([source_id] if source_id else [])
    related_cards = as_list(meta.get("related_cards"))
    additions = {
        "card_type": scalar(meta.get("card_type")) or infer_card_type(meta),
        "sources": _render_ids(sources),
        "relations": _render_relations(related_cards),
        "evidence_level": scalar(meta.get("evidence_level")) or "derived",
        "epistemic_status": scalar(meta.get("epistemic_status")) or "working",
    }
    missing = {key: value for key, value in additions.items() if key not in meta}
    if not missing:
        return False
    marker = "\n---\n"
    end = text.find(marker, 4)
    if end < 0:
        raise ValueError(f"missing frontmatter terminator: {path}")
    frontmatter = text[4:end]
    insert_at = frontmatter.find("\ncreated:")
    if insert_at < 0:
        insert_at = len(frontmatter)
    rendered = "".join(f"\n{key}: {value}" for key, value in missing.items())
    updated = text[: 4 + insert_at] + rendered + text[4 + insert_at :]
    if apply:
        path.write_text(updated, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write migrated frontmatter")
    args = parser.parse_args()
    paths = sorted(CARDS.glob("*.md"))
    changed = sum(migrate(path, apply=args.apply) for path in paths)
    mode = "migrated" if args.apply else "would migrate"
    print(f"{mode}={changed} cards={len(paths)}")


if __name__ == "__main__":
    main()
