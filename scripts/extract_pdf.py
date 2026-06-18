"""Extract text from a PDF with a supported environment or project provider."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPS = ROOT / ".deps"


class ExtractionError(RuntimeError):
    pass


def enable_project_deps():
    if DEPS.is_dir() and str(DEPS) not in sys.path:
        sys.path.insert(0, str(DEPS))


def extract_with_pypdf(path):
    try:
        from pypdf import PdfReader
        provider = "pypdf"
    except ImportError:
        try:
            from PyPDF2 import PdfReader
            provider = "PyPDF2"
        except ImportError:
            return None
    reader = PdfReader(str(path))
    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    return provider, pages


def extract_with_pdfplumber(path):
    try:
        import pdfplumber
    except ImportError:
        return None
    with pdfplumber.open(path) as pdf:
        pages = [(page.extract_text() or "").strip() for page in pdf.pages]
    return "pdfplumber", pages


def extract_with_fitz(path):
    try:
        import fitz
    except ImportError:
        return None
    document = fitz.open(path)
    try:
        pages = [page.get_text().strip() for page in document]
    finally:
        document.close()
    return "fitz", pages


def extract_pdf(path):
    enable_project_deps()
    for extractor in (
        extract_with_pypdf, extract_with_pdfplumber, extract_with_fitz
    ):
        result = extractor(path)
        if result:
            provider, pages = result
            if not any(pages):
                raise ExtractionError(
                    "No text was extracted. The PDF may be scanned; run OCR first."
                )
            return provider, pages
    raise ExtractionError(
        "No supported PDF provider found. Add pypdf to .deps or the environment."
    )


def format_text(pages):
    sections = []
    for number, text in enumerate(pages, 1):
        sections.append(f"--- Page {number} ---\n{text}")
    return "\n\n".join(sections) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.pdf.is_file():
        parser.error(f"PDF not found: {args.pdf}")
    try:
        provider, pages = extract_pdf(args.pdf)
    except ExtractionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    text = format_text(pages)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    if args.json:
        print(json.dumps({
            "provider": provider,
            "pages": len(pages),
            "output": str(args.output) if args.output else None,
        }, ensure_ascii=False))
    elif not args.output:
        print(text, end="")
    else:
        print(f"provider: {provider}; pages: {len(pages)}; output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
