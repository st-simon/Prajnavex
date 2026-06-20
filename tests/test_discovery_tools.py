import contextlib
import io
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
import setup_pdf_deps


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
        self.assertIn(report["pdf"]["status"], {"ready", "install-required"})
        self.assertEqual(
            report["pdf"]["install_command"], "python scripts/setup_pdf_deps.py"
        )
        self.assertIn("models", report)
        self.assertTrue(report["models"]["configured"])


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
            extract_pdf.ExtractionError, "setup_pdf_deps.py"
        ):
            extract_pdf.extract_pdf(Path("missing.pdf"))


class PdfDependencySetupTests(unittest.TestCase):
    def test_requirements_pin_pypdf(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertRegex(requirements.strip(), r"^pypdf==\d+\.\d+\.\d+$")

    @patch("setup_pdf_deps.project_pypdf_version", return_value=None)
    @patch("setup_pdf_deps.environment_pypdf_version", return_value=None)
    def test_check_reports_missing_dependency(self, *_):
        output = io.StringIO()
        with patch.object(
            sys, "argv", ["setup_pdf_deps.py", "--check"]
        ), contextlib.redirect_stdout(output):
            self.assertEqual(setup_pdf_deps.main(), 1)
        self.assertIn("not ready", output.getvalue())

    @patch("setup_pdf_deps.project_pypdf_version", return_value="6.13.3")
    @patch("setup_pdf_deps.environment_pypdf_version", return_value=None)
    def test_check_accepts_project_dependency(self, *_):
        output = io.StringIO()
        with patch.object(
            sys, "argv", ["setup_pdf_deps.py", "--check"]
        ), contextlib.redirect_stdout(output):
            self.assertEqual(setup_pdf_deps.main(), 0)
        self.assertIn("project .deps", output.getvalue())


if __name__ == "__main__":
    unittest.main()
