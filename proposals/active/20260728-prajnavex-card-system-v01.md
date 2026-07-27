# Proposal: Prajnavex Card System v0.1

Status: in_progress

## Goal

Build an extensible, cross-source Card system while preserving Obsidian
readability, frontmatter-first indexing, backward compatibility, and the
separation between reusable knowledge Cards and executable Skills.

## Accepted Decisions

- Keep `type: card` as the storage envelope.
- Add `card_type` with the initial taxonomy: `entity`, `event`, `period`,
  `concept`, `mechanism`, `claim`, `work`, `comparison`, and `method`.
- Use `entity_kind` for `person`, `group`, `institution`, and `place`.
- Treat `method` as a first-class Card type, not an automatic Skill.
- Prefer `sources` for future multi-source provenance while retaining
  `source_id` during migration.
- Use `relations` as the canonical semantic link map while retaining
  `related_cards` during migration.
- Use `stage` for lifecycle and `epistemic_status` for knowledge posture.
- Use YAML relation maps in frontmatter; do not create standalone relation
  notes in v0.1.

## Implemented Slice

- Extended the Card template, schema documentation, validator, index and
  backlink builder.
- Added `scripts/migrate_cards_v01.py`.
- Migrated all current Cards with conservative defaults:
  `evidence_level: derived` and `epistemic_status: working`.
- Derived `sources` from `source_id` and `relations.related_to` from existing
  `related_cards` without deleting compatibility fields.

## Remaining Scope

1. Refine semantic Card classifications by knowledge domain.
2. Seed cross-source entity and event Cards from the China history material.
3. Extract technology methods as method Cards before considering Skill
   promotion.
4. Validate the taxonomy across multiple sources before expanding it.

## Non-goals

- No graph database.
- No full-vault automatic entity extraction.
- No mass splitting of historical facts without review.
- No automatic promotion of method Cards to active Skills.
