import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ingest_document
from model_runtime import ModelRuntimeError, OllamaRuntime

GOLDEN = ROOT / "tests" / "golden"


class FakeRuntime:
    def __init__(self):
        self.analysis = json.loads(
            (GOLDEN / "document_ingest_response.json").read_text(
                encoding="utf-8"
            )
        )

    def generate_structured(self, prompt, schema, role="reasoner"):
        if schema is ingest_document.FINAL_SCHEMA:
            return self.analysis
        if schema is ingest_document.DUPLICATE_SCHEMA:
            return {"matches": [{
                "card_index": 0,
                "existing_card_id":
                    "card-20260602-infographic-to-structured-source",
                "relationship": "related",
                "reason": "Both define review boundaries for structured notes.",
                "confidence": "medium",
            }]}
        raise AssertionError("unexpected schema")


class FailingRuntime:
    def generate_structured(self, prompt, schema, role="reasoner"):
        raise ModelRuntimeError("local model unavailable")


class DocumentIngestTests(unittest.TestCase):
    def test_tags_are_safe_for_inline_frontmatter(self):
        self.assertEqual(
            ingest_document.normalize_tags(
                ["AI Governance", "risk:policy", "evidence,review"]
            ),
            ["ai-governance", "risk-policy", "evidence-review"],
        )

    def test_split_chunks_preserves_content(self):
        text = "alpha\n\n" + ("beta " * 100)
        chunks = ingest_document.split_chunks(text, limit=80)
        self.assertGreater(len(chunks), 1)
        self.assertIn("alpha", chunks[0])

    def test_golden_ingest_creates_source_cards_and_duplicate_warning(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            vault = temp / "vault"
            source_drafts = vault / "00_inbox" / "_source_drafts"
            card_drafts = vault / "00_inbox" / "_card_drafts"
            extracted = vault / "00_inbox" / "_extracted"
            sample = temp / "sample.txt"
            sample.write_text(
                (GOLDEN / "document_ingest_sample.txt").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            with patch.multiple(
                ingest_document,
                ROOT=temp,
                VAULT=vault,
                INBOX=vault / "00_inbox",
                SOURCE_DRAFTS=source_drafts,
                CARD_DRAFTS=card_drafts,
                EXTRACTED=extracted,
                SOURCES=vault / "10_sources",
                CARDS=vault / "20_cards",
            ):
                result = ingest_document.ingest(
                    sample, runtime=FakeRuntime()
                )
                source = temp / result["source_draft"]
                cards = [temp / path for path in result["card_drafts"]]
                self.assertEqual(result["ingest_status"], "semantic-draft")
                self.assertEqual(len(cards), 2)
                self.assertIn(
                    "Human-reviewed knowledge drafting",
                    source.read_text(encoding="utf-8"),
                )
                self.assertIn(
                    "card-20260602-infographic-to-structured-source",
                    cards[0].read_text(encoding="utf-8"),
                )

    def test_source_only_does_not_require_model(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            vault = temp / "vault"
            sample = temp / "sample.txt"
            sample.write_text("Evidence only.", encoding="utf-8")
            with patch.multiple(
                ingest_document,
                ROOT=temp,
                VAULT=vault,
                SOURCE_DRAFTS=vault / "00_inbox" / "_source_drafts",
                CARD_DRAFTS=vault / "00_inbox" / "_card_drafts",
                EXTRACTED=vault / "00_inbox" / "_extracted",
                SOURCES=vault / "10_sources",
                CARDS=vault / "20_cards",
            ):
                result = ingest_document.ingest(sample, source_only=True)
            self.assertEqual(result["ingest_status"], "text-only")
            self.assertEqual(result["card_drafts"], [])

    def test_model_failure_preserves_pending_source_draft(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            vault = temp / "vault"
            sample = temp / "sample.txt"
            sample.write_text("Evidence survives failure.", encoding="utf-8")
            with patch.multiple(
                ingest_document,
                ROOT=temp,
                VAULT=vault,
                SOURCE_DRAFTS=vault / "00_inbox" / "_source_drafts",
                CARD_DRAFTS=vault / "00_inbox" / "_card_drafts",
                EXTRACTED=vault / "00_inbox" / "_extracted",
                SOURCES=vault / "10_sources",
                CARDS=vault / "20_cards",
            ):
                result = ingest_document.ingest(
                    sample, runtime=FailingRuntime()
                )
                source = temp / result["source_draft"]
            self.assertEqual(result["ingest_status"], "pending-model")
            self.assertIn("local model unavailable", result["warning"])
            self.assertTrue(source.exists())

    def test_review_status_can_mark_rework_or_rejection(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            vault = temp / "vault"
            sample = temp / "sample.txt"
            sample.write_text("Needs review.", encoding="utf-8")
            with patch.multiple(
                ingest_document,
                ROOT=temp,
                VAULT=vault,
                SOURCE_DRAFTS=vault / "00_inbox" / "_source_drafts",
                CARD_DRAFTS=vault / "00_inbox" / "_card_drafts",
                EXTRACTED=vault / "00_inbox" / "_extracted",
                SOURCES=vault / "10_sources",
                CARDS=vault / "20_cards",
            ):
                result = ingest_document.ingest(sample, source_only=True)
                source = temp / result["source_draft"]
                ingest_document.set_review_status(source, "needs-rework")
                self.assertIn(
                    "review_status: needs-rework",
                    source.read_text(encoding="utf-8"),
                )
                ingest_document.set_review_status(source, "rejected")
                self.assertIn(
                    "review_status: rejected",
                    source.read_text(encoding="utf-8"),
                )

    def test_approval_requires_source_before_card_and_updates_backlink(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            vault = temp / "vault"
            paths = {
                "ROOT": temp,
                "VAULT": vault,
                "INBOX": vault / "00_inbox",
                "SOURCE_DRAFTS": vault / "00_inbox" / "_source_drafts",
                "CARD_DRAFTS": vault / "00_inbox" / "_card_drafts",
                "EXTRACTED": vault / "00_inbox" / "_extracted",
                "SOURCES": vault / "10_sources",
                "CARDS": vault / "20_cards",
            }
            sample = temp / "sample.txt"
            sample.write_text(
                (GOLDEN / "document_ingest_sample.txt").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            with patch.multiple(ingest_document, **paths):
                result = ingest_document.ingest(
                    sample, runtime=FakeRuntime()
                )
                card_draft = temp / result["card_drafts"][0]
                with self.assertRaisesRegex(ValueError, "linked Source"):
                    ingest_document.approve_card(card_draft)
                source = ingest_document.approve_source(
                    temp / result["source_draft"]
                )
                card = ingest_document.approve_card(card_draft)
                card_id = ingest_document.read_frontmatter(card)["id"]
                self.assertTrue(source.exists())
                self.assertTrue(card.exists())
                self.assertIn(
                    card_id, source.read_text(encoding="utf-8")
                )


class ModelRuntimeTests(unittest.TestCase):
    def test_missing_role_model_is_actionable(self):
        runtime = OllamaRuntime(config={
            "base_url": "http://127.0.0.1:11434",
            "roles": {"reasoner": "missing"},
            "fallback_roles": {},
        })
        with patch.object(runtime, "available_models", return_value=set()):
            with self.assertRaisesRegex(ModelRuntimeError, "ollama list"):
                runtime.resolve_role("reasoner")


if __name__ == "__main__":
    unittest.main()
