import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge_audit import audit_records
from knowledge_index import build_backlinks, parse_value, validate_records


class KnowledgeIndexTests(unittest.TestCase):
    def test_parse_inline_list(self):
        self.assertEqual(parse_value("[a, b, c]"), ["a", "b", "c"])

    def test_missing_link_is_error(self):
        records = [
            {"path": "vault/20_cards/card.md", "id": "card-x", "type": "card", "title": "X", "summary": "X", "tags": [], "stage": "extracted", "created": "2026-06-04", "source_id": "source-missing"},
        ]
        errors, _ = validate_records(records)
        self.assertTrue(any("references missing id" in error for error in errors))

    def test_backlinks_include_card_to_source(self):
        records = [
            {"path": "vault/10_sources/source.md", "id": "source-x", "type": "source", "title": "S", "summary": "S", "tags": [], "stage": "source", "created": "2026-06-04", "source_type": "article"},
            {"path": "vault/20_cards/card.md", "id": "card-x", "type": "card", "title": "C", "summary": "C", "tags": [], "stage": "extracted", "created": "2026-06-04", "source_id": "source-x"},
        ]
        backlinks = build_backlinks(records)
        self.assertEqual(backlinks["source-x"]["cards"], ["card-x"])

    def test_audit_reports_missing_staleness_fields(self):
        records = [
            {"path": "vault/10_sources/source.md", "id": "source-x", "type": "source", "title": "S", "summary": "S", "tags": [], "stage": "source", "created": "2026-06-04", "source_type": "article"},
        ]
        issues = audit_records(records)
        self.assertTrue(any("missing audit fields" in message for _, _, message in issues))


if __name__ == "__main__":
    unittest.main()
