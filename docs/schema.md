# Metadata Schema

Required frontmatter fields for `source`, `card`, `skill`, and `bundle` notes:

- `id`: stable unique identifier, such as `source-20260601-example`.
- `type`: one of `source`, `card`, `skill`, or `bundle`.
- `title`: human-readable title.
- `summary`: one or two sentence summary.
- `tags`: topic tags.
- `stage`: lifecycle state.
- `created`: creation date in `YYYY-MM-DD`.

Recommended lifecycle:

```text
inbox -> source -> extracted -> promotable -> skill-draft -> skill-active -> archived
```

The frontmatter exists for indexing. The Markdown body exists for reading and editing.

## Image Source Fields

Image source drafts and approved image sources should include:

- `image_kind`: one of `screenshot`, `infographic`, `table`, `slide`, `chart`, `document_scan`, `social_post`, or `unknown`.
- `ocr_quality`: one of `low`, `medium`, `high`, or `unknown`.
- `vision_required`: `true` when OCR alone is not enough.
- `extraction_strategy`: one of `ocr-first`, `vision-first`, or `hybrid`.
- `review_status`: one of `needs-human-review`, `approved`, `rejected`, or `needs-rework`.

For screenshots, information graphics, tables, slides, charts, and social posts, prefer `vision-first` or `hybrid`. For clean document scans, `ocr-first` is acceptable.
