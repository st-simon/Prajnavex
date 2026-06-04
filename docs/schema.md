# Metadata Schema

Required frontmatter fields for `source`, `card`, `skill`, and `bundle` notes:

- `id`: stable unique identifier, such as `source-20260601-example`.
- `type`: one of `source`, `card`, `skill`, or `bundle`.
- `title`: human-readable title.
- `summary`: one or two sentence summary.
- `tags`: topic tags.
- `stage`: lifecycle state.
- `created`: creation date in `YYYY-MM-DD`.
- `updated`: last meaningful edit date in `YYYY-MM-DD`.
- `last_verified`: last date the claim, source, or workflow was checked.
- `review_after`: date when the note should be reviewed again.
- `confidence`: one of `low`, `medium`, `high`, or `unknown`.
- `staleness`: one of `fresh`, `watch`, `stale`, or `unknown`.

Recommended lifecycle:

```text
inbox -> source -> extracted -> promotable -> skill-draft -> skill-active -> archived
```

Allowed stage values are type-specific:

- `source`: `source-draft`, `source`, `archived`
- `card`: `extracted`, `promotable`, `archived`
- `skill`: `skill-draft`, `skill-active`, `archived`
- `bundle`: `bundle-draft`, `bundle-active`, `archived`

The frontmatter exists for indexing. The Markdown body exists for reading and editing.

## Link Fields

These fields must resolve to existing note `id` values:

- `source_id`: a `card` points to one `source`.
- `related_cards`: a `source` points to extracted `card` notes.
- `promoted_skills`: a `source` points to derived `skill` notes.
- `source_cards`: a `skill` points to the cards it depends on.
- `skills`: a `bundle` points to the skills it combines.

`scripts/knowledge_index.py --check` treats missing or wrong-type links as errors.

## Image Source Fields

Image source drafts and approved image sources should include:

- `image_kind`: one of `screenshot`, `infographic`, `table`, `slide`, `chart`, `document_scan`, `social_post`, or `unknown`.
- `ocr_quality`: one of `low`, `medium`, `high`, or `unknown`.
- `vision_required`: `true` when OCR alone is not enough.
- `extraction_strategy`: one of `ocr-first`, `vision-first`, or `hybrid`.
- `review_status`: one of `needs-human-review`, `approved`, `rejected`, or `needs-rework`.

For screenshots, information graphics, tables, slides, charts, and social posts, prefer `vision-first` or `hybrid`. For clean document scans, `ocr-first` is acceptable.

## Validation and Audit

Use validation for structural correctness:

```powershell
python scripts\knowledge_index.py --check
```

Use audit for operational risk:

```powershell
python scripts\knowledge_audit.py
```

Validation errors should be fixed before committing. Audit warnings are a work queue for review, refresh, merge, or archive decisions.
