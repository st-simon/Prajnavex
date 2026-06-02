# Image Ingest Workflow

## Current MVP

For an image already in `vault/00_inbox`, generate a source draft first. Drafts live in `vault/00_inbox/_source_drafts` and are not part of the formal source index.

Image ingestion is a dual-track process:

```text
OCR Text -> evidence
Vision Summary -> semantic structure
Cleaned Text -> reviewed usable knowledge
Source Draft -> human approval -> Source / Cards
```

The source draft should include:

- `source_type: image`
- `image_kind`
- `ocr_quality`
- `vision_required`
- `extraction_strategy`
- `review_status`
- `local_image`
- title
- summary
- extracted visible structure
- possible cards
- follow-up action

## Image Kinds

- `document_scan`: clean document photo or scanned page.
- `screenshot`: app, browser, chat, or desktop screenshot.
- `infographic`: designed visual explanation or long image.
- `table`: table-like image where row/column relations matter.
- `slide`: presentation page or slide screenshot.
- `chart`: chart, graph, market visual, or diagram.
- `social_post`: post screenshot from social platforms.
- `unknown`: use only before review.

## Extraction Strategy

- `ocr-first`: use for clean document scans where text order is reliable.
- `vision-first`: use for infographics, slides, charts, and dense screenshots.
- `hybrid`: use when both exact text and layout meaning matter.

OCR is evidence, not the final knowledge layer. Vision Summary is the semantic layer. Cleaned Text is the reviewed synthesis used to create sources and cards.

## Automation Levels

The OCR adapter lives in Prajnavex scripts, not inside Obsidian. Obsidian remains the editor and review surface.

Level 1: create a source draft from image file metadata.

Level 2: use OCR or vision extraction to fill title, summary, visible text, and structured observations.

Level 3: compare the extracted content against existing cards and propose new cards, synthesis notes, or skill updates.

## Human Review Boundary

Image extraction can be noisy. Prajnavex lets automation propose source/card/skill drafts, but human review approves promotions into stable cards or active skills.

Review a source draft before approval:

- confirm the title
- replace the summary
- set `image_kind`
- set `ocr_quality`
- choose `extraction_strategy`
- fill `Vision Summary`
- fill `Cleaned Text`
- decide whether the image is worth keeping
- decide whether cards should be extracted

## Commands

List inbox images:

```powershell
python scripts\image_inbox.py --list
```

Run OCR on one image:

```powershell
python scripts\image_inbox.py --ocr "vault\00_inbox\path\image.png"
```

Create a source draft:

```powershell
python scripts\image_inbox.py --draft "vault\00_inbox\path\image.png"
```

Approve a reviewed draft into `vault\10_sources`:

```powershell
python scripts\image_inbox.py --approve "vault\00_inbox\_source_drafts\source-draft-example.md"
```
