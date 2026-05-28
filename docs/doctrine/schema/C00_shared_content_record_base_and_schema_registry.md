# C00 Shared Content Record Base and Schema Registry Doctrine

## 1. Purpose and status

C00 defines schema-layer doctrine for shared conversion record grammar and schema-registry behavior used by downstream C01-C14 families.

Status posture:
- This file is schema-todo fulfillment drafted as schema-draft material.
- This file is not marked current canon.
- This file does not define runtime event schemas, command lifecycle, event-sourced state model, state delta validator, context packet compiler, hidden-information runtime state, live-play behavior, canon promotion procedure, final mechanics, accepted lexicon terms, final sourcebook prose, or donor record formats as Astra defaults.

Registry identity and governance anchors (source of truth):
- file_id: C00;
- filename: `C00_shared_content_record_base_and_schema_registry.md`;
- proposed_path: `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md`;
- layer: `4_schema_base`;
- phase: `2`;
- owner: Astra Doctrine Council - Schema Working Group.

## 2. What this file owns

C00 owns schema-layer doctrine for:
- shared conversion record grammar;
- provenance grammar;
- source-local records;
- rejected imports;
- canon eligibility routing;
- confidence and review routing;
- versioning and cross-reference fields;
- schema-registry behavior and inheritance rules for C01-C14.

## 3. What this file must not own

C00 must not define:
- final mechanics;
- canon acceptance;
- canon promotion procedure;
- runtime state schema;
- runtime state fields;
- runtime event schema;
- command lifecycle;
- event-sourced state model;
- state delta validator;
- context packet compiler;
- hidden-information runtime state;
- live-play behavior;
- donor field names as Astra defaults;
- donor record shapes;
- accepted lexicon terms;
- final sourcebook prose.

C00 does not draft C01-C14, K-layer, B-layer, R-layer, or T-layer files and does not redefine A-layer ownership.

## 4. Required definitions

Shared field grammar (required exact field set):
- `record_id`
- `schema_id`
- `schema_version`
- `doctrine_version`
- `authority_layer`
- `lifecycle_status`
- `review_status`
- `source_scope`
- `source_family`
- `provenance_block`
- `evidence_refs`
- `extraction_refs`
- `donor_refs`
- `source_local_status`
- `rejected_import_status`
- `lawful_outcome`
- `canon_eligibility`
- `promotion_gate`
- `confidence_score`
- `review_queue`
- `reviewer_notes`
- `conflict_refs`
- `dependency_refs`
- `cross_refs`
- `supersedes_refs`
- `retrieval_metadata`
- `doctrine_tags`
- `retrieval_tags`
- `donor_tags`
- `access_tags`

Tag separation requirement:
- `doctrine_tags` classify doctrine-domain meaning and governance context;
- `retrieval_tags` classify indexing and retrieval optimization metadata;
- `donor_tags` preserve donor-native descriptors without Astra-default promotion;
- `access_tags` classify access control and visibility posture.

Required lifecycle/status grammar (exact values):
- `draft`
- `designed`
- `not_reviewed`
- `reviewed`
- `source-local`
- `rejected-import`
- `canon-candidate`
- `quarantined`
- `escalated`
- `deprecated`
- `superseded`
- `current`

Status-label rule:
- status labels do not themselves promote anything to canon.

Required record-family separation:
- shared content record
- source-local record
- rejected-import record
- canon-candidate record
- review-queue record
- conflict-record
- schema-registry record
- retrieval-index record
- runtime-event record placeholder

## 5. Core schema rules

1. Classification-first rule: every conversion record must be typed into one required record family before downstream interpretation.
2. Provenance-preservation rule: provenance and evidence linkage fields are mandatory and must remain auditable.
3. Separation-of-authority rule: schema-layer fields govern conversion representation only, not canon authority or runtime authority.
4. Registry-alignment rule: schema ownership/path identity must match the doctrine registry before promotion gates are considered.
5. Non-collapse rule: C00 explicitly forbids runtime phase collapse from conversion/schema records into runtime behavior authority.
6. Placeholder boundary rule: a runtime-event record placeholder may exist only as a boundary marker and may not define runtime event schemas, command lifecycle, event sourcing, context packet assembly, hidden-information state, live-play state, or state mutation behavior.

## 6. Conversion mapping rules

- Map donor evidence into the C00 shared field grammar before any family-specific shaping.
- Preserve ambiguous or conflicting donor evidence through `source_local_status`, `rejected_import_status`, `conflict_refs`, `review_queue`, and escalation paths instead of forced normalization.
- Keep `canon_eligibility` and `promotion_gate` as routing signals only; they do not grant canon acceptance.
- Never normalize by inventing mechanics, runtime state behavior, lexicon acceptance, or sourcebook prose.

## 7. Source-local handling

- Source-local records preserve donor provenance but do not become Astra canon.
- Rejected-import records preserve refusal rationale and provenance.
- Unclassifiable records are quarantined or escalated, not normalized by invention.
- Donor proper nouns remain source-local unless later canon promotion accepts them.
- Source-local record terms do not become accepted lexicon terms through C00.
- Canon candidates remain candidates until later K-layer review.

## 8. Donor pressure absorbed

C00 is designed to absorb donor pressure from:
- donor statblock/table/item/ability/location/faction formats;
- proper-noun leakage;
- incomplete provenance;
- conflicting donor naming and structure conventions;
- mixed-confidence extraction artifacts.

Absorption means auditable classification/routing, not donor-default adoption.

## 9. Hard refusals / rejected imports

C00 refuses as Astra defaults:
- donor field names as Astra defaults;
- donor record shapes as Astra schema defaults;
- runtime state imports disguised as schema fields;
- canon promotion by schema-only status changes;
- silent drops of rejected or unclassifiable evidence.

## 10. Escalation triggers

Escalate when:
- record structure requires unsupported fields outside C00 base grammar;
- schema interpretation conflicts with A-layer doctrine boundaries;
- provenance cannot be preserved across a required mapping;
- record classification cannot be completed without inventing runtime or mechanics behavior;
- cross-reference/dependency relations become contradictory or non-auditable.

## 11. Dependencies

C00 dependency posture (registry source of truth):
- depends on A01-A15;
- is blocked by A01-A15 during pre-draft staging, then cleared for this draft record state;
- unlocks C01-C14 and K03 per registry sequencing.

C00 does not redefine A-layer ownership and does not bypass hard locks.

## 12. Handoff to downstream layers

C00 hands off base grammar constraints to:
- C01-C14 schema-family files;
- K03 canon-review integration points;
- conversion-intake and validation consumers listed in registry.

Downstream consumers must include all C00 base fields and preserve source-local/rejected-import audit traces.

## 13. Test cases / pressure examples

- Provenance retention example: a donor record with partial extraction still retains `provenance_block`, `evidence_refs`, and `extraction_refs`.
- Rejected-import example: donor-shaped runtime-state payload is captured as rejected-import with refusal rationale and provenance.
- Quarantine/escalation example: contradictory donor claims that cannot be classified without invention are quarantined or escalated.
- Canon-candidate boundary example: a high-confidence record labeled `canon-candidate` remains non-canon pending K-layer review.

## 14. Versioning and review protocol

- C00 remains draft/not-current until registry promotion requirements are satisfied.
- Substantive C00 edits require versioned registry changelog updates and re-review.
- `review_status` tracks review workflow posture and does not itself promote canon.
- C00 governance remains schema-layer only and does not authorize runtime behavior.
