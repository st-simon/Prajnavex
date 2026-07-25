import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge_audit import audit_records
from bundle_tool_draft import render_draft
from knowledge_index import build_backlinks, parse_value, validate_records
from context_pack import build_context_pack
from knowledge_api import cite, context_pack, get, search
from prajnavex_web import api_status


class KnowledgeIndexTests(unittest.TestCase):
    def test_bundle_draft_includes_contract_and_skills(self):
        draft = render_draft({
            "id": "bundle-x",
            "title": "Research workflow",
            "input_contract": "Company and market evidence.",
            "output_contract": "A thesis and risk checklist.",
            "skills": ["skill-a", "skill-b"],
        })
        self.assertIn("Company and market evidence.", draft)
        self.assertIn("A thesis and risk checklist.", draft)
        self.assertIn("`skill-a`", draft)
        self.assertIn("`skill-b`", draft)

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

    def test_audit_ignores_archived_stale_notes(self):
        records = [
            {"path": "vault/10_sources/source.md", "id": "source-x", "type": "source", "title": "S", "summary": "S", "tags": [], "stage": "archived", "created": "2026-06-04", "updated": "2026-06-04", "last_verified": "2026-06-04", "review_after": "2026-12-04", "confidence": "medium", "staleness": "stale", "source_type": "article"},
        ]
        self.assertEqual(audit_records(records), [])

    def test_web_status_reports_validation_warnings(self):
        status = api_status()
        self.assertIn("counts", status)
        self.assertIn("errors", status)
        self.assertIn("warnings", status)

    def test_context_pack_is_bounded_and_citable(self):
        pack = build_context_pack("coding agent", note_type="card", limit=2)
        self.assertEqual(pack["recall"]["strategy"], "frontmatter-first")
        self.assertLessEqual(len(pack["items"]), 2)
        if pack["items"]:
            item = pack["items"][0]
            self.assertIn("citation", item)
            self.assertIn("id", item["citation"])
            self.assertLessEqual(len(item["body"]), 4000)

    def test_knowledge_api_supports_search_get_and_cite(self):
        result = search("dual consumer", note_type="card", limit=3)
        self.assertEqual(result["records"][0]["id"], "card-20260726-prajnavex-dual-consumer-model")
        note = get(result["records"][0]["id"], include_body=False)
        self.assertNotIn("body", note)
        citation = cite(note["id"])
        self.assertEqual(citation["authority_path"], "DECISIONS.md")

    def test_knowledge_api_context_pack_marks_agent_consumer(self):
        pack = context_pack("dual consumer", note_type="card", limit=1)
        self.assertEqual(pack["consumer"], "agent")

if __name__ == "__main__":
    unittest.main()
