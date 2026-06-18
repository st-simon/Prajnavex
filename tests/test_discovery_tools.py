import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import discover
import extract_pdf


class DiscoveryTests(unittest.TestCase):
    def test_project_deps_provider_is_detected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            deps = Path(temp_dir)
            package = deps / "pypdf"
            package.mkdir()
            (package / "__init__.py").write_text("", encoding="utf-8")
            with patch.object(discover, "DEPS", deps), patch(
                "discover.importlib.util.find_spec", return_value=None
            ):
                providers = discover.find_pdf_providers()
        self.assertIn(
            {"module": "pypdf", "source": "project .deps"}, providers
        )

    @patch("discover.subprocess.run")
    def test_git_status_uses_command_scoped_trust(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, " M file\n", "")
        result = discover.git_status()
        command = run.call_args.args[0]
        self.assertIn(f"safe.directory={ROOT.as_posix()}", command)
        self.assertNotIn("config", command)
        self.assertFalse(result["clean"])

    def test_json_cli(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "discover.py"), "--json"],
            capture_output=True,
            text=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(Path(report["project_root"]), ROOT)
        self.assertEqual(report["schema"], "docs/schema.md")


class PdfExtractionTests(unittest.TestCase):
    def test_page_format_is_stable(self):
        text = extract_pdf.format_text(["first", "second"])
        self.assertIn("--- Page 1 ---\nfirst", text)
        self.assertIn("--- Page 2 ---\nsecond", text)

    @patch("extract_pdf.extract_with_fitz", return_value=None)
    @patch("extract_pdf.extract_with_pdfplumber", return_value=None)
    @patch("extract_pdf.extract_with_pypdf", return_value=None)
    def test_missing_provider_has_actionable_error(self, *_):
        with self.assertRaisesRegex(
            extract_pdf.ExtractionError, "Add pypdf"
        ):
            extract_pdf.extract_pdf(Path("missing.pdf"))


if __name__ == "__main__":
    unittest.main()
