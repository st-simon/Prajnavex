# Proposal: Prajnavex Card System v0.1

Status: accepted-for-design; implementation pending

## Goal

Build an extensible, cross-source card system for Prajnavex. Cards should support entities, events, periods, concepts, mechanisms, claims, works, comparisons, and methods, while preserving Obsidian readability and frontmatter-first indexing.

## Decisions

- Keep `type: card` as the storage envelope.
- Add `card_type` as the semantic card category.
- Use `entity_kind` for `person`, `group`, `institution`, and `place`.
- Treat `method` as a first-class card type.
- Keep `method` separate from `skill`: a method is reusable knowledge; a skill is a validated executable workflow.
- Prefer `sources` as the future multi-source provenance field; keep `source_id` during migration.
- Make `relations` the canonical semantic link structure; keep `related_cards` only for compatibility during migration.
- Use `stage` for workflow lifecycle and `epistemic_status` for knowledge status; do not add a second generic `status` field.
- Use YAML relation maps in v0.1; do not create standalone relation notes yet.

## Card types

```
entity, event, period, concept, mechanism, claim, work, comparison, method
```

## Method-to-skill promotion

A method card may become a skill candidate only after repeated use, stable scope, explicit inputs/outputs, validation, and documented failure handling. A relation or repeated application may trigger review, but must not automatically create an active skill.

## Migration order

1. Define templates and validator rules with backward compatibility.
2. Add `card_type`, `evidence_level`, and `epistemic_status` to existing cards.
3. Normalize provenance from `source_id` toward `sources`.
4. Seed a small set of entity and event cards from the China history sources.
5. Extract technology methods as method cards before considering skill promotion.
6. Validate the model across multiple sources before expanding the taxonomy.

## Non-goals

No graph database, full-vault automatic entity extraction, mass splitting of historical facts, or automatic promotion to active skills in v0.1.
