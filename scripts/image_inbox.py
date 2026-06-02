import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
INBOX = VAULT / "00_inbox"
SOURCE_DRAFTS = INBOX / "_source_drafts"
SOURCES = VAULT / "10_sources"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def iter_images():
    for path in INBOX.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            yield path


def resolve_path(value):
    path = Path(value)
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def slugify(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "image"


def run_ocr(path):
    script = ROOT / "scripts" / "ocr_image.ps1"
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script), "-Path", str(path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def draft_source(image_path):
    image_path = resolve_path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(image_path)
    ocr_text = run_ocr(image_path)
    slug = slugify(image_path.stem)
    source_id = f"source-draft-{slug}"
    draft_path = SOURCE_DRAFTS / f"{source_id}.md"
    SOURCE_DRAFTS.mkdir(parents=True, exist_ok=True)
    if draft_path.exists():
        raise FileExistsError(draft_path)
    local_image = image_path.relative_to(VAULT).as_posix()
    body = make_draft_body(source_id, image_path, local_image, ocr_text)
    draft_path.write_text(body, encoding="utf-8")
    return draft_path


def make_draft_body(source_id, image_path, local_image, ocr_text):
    lines = [
        "---",
        f"id: {source_id}",
        "type: source",
        f'title: "{image_path.stem}"',
        'summary: "TODO: review OCR output and write a concise summary."',
        "tags: [image, inbox, needs-review]",
        "stage: source-draft",
        "source_type: image",
        "image_kind: unknown",
        "ocr_quality: unknown",
        "vision_required: true",
        "extraction_strategy: vision-first",
        "review_status: needs-human-review",
        'source_url: ""',
        'author: ""',
        "created: 2026-06-02",
        "usefulness: medium",
        "related_cards: []",
        "promoted_skills: []",
        f'local_image: "../{local_image}"',
        "---",
    ]
    body = [
        f"# {image_path.stem}",
        "",
        "## Review Checklist",
        "",
        "- Confirm title.",
        "- Replace summary.",
        "- Classify image_kind.",
        "- Rate ocr_quality.",
        "- Add Vision Summary.",
        "- Add Cleaned Text.",
        "- Decide whether to approve into `10_sources`.",
        "- Decide whether cards should be extracted.",
        "",
        "## Vision Summary",
        "",
        "TODO: describe the visual structure, key entities, relationships, and meaning.",
        "",
        "## Cleaned Text",
        "",
        "TODO: synthesize OCR Text and Vision Summary into reliable source text.",
        "",
        "## OCR Text",
        "",
        ocr_text,
        "",
    ]
    return "\n".join(lines + body)


def approve_draft(draft_path):
    draft_path = resolve_path(draft_path)
    text = draft_path.read_text(encoding="utf-8")
    if "stage: source-draft" not in text:
        raise ValueError("draft must contain stage: source-draft")
    approved = text.replace("stage: source-draft", "stage: source", 1)
    approved = approved.replace("source-draft-", "source-", 1)
    dest = SOURCES / draft_path.name.replace("source-draft-", "source-", 1)
    if dest.exists():
        raise FileExistsError(dest)
    SOURCES.mkdir(parents=True, exist_ok=True)
    dest.write_text(approved, encoding="utf-8")
    draft_path.unlink()
    return dest








def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="List inbox images.")
    parser.add_argument("--ocr", help="Run Windows OCR for one image path.")
    parser.add_argument("--draft", help="Create a source draft for one inbox image.")
    parser.add_argument("--approve", help="Approve a source draft into 10_sources.")
    args = parser.parse_args()
    if args.draft:
        path = draft_source(args.draft)
        print(path.relative_to(ROOT).as_posix())
        return
    if args.approve:
        path = approve_draft(args.approve)
        print(path.relative_to(ROOT).as_posix())
        return
    if args.ocr:
        print(run_ocr(resolve_path(args.ocr)))
        return
    if args.list:
        for path in iter_images():
            rel = path.relative_to(ROOT).as_posix()
            print(rel)
        return
    parser.print_help()


if __name__ == "__main__":
    main()
