# C00 Shared Content Record Base and Schema Registry Doctrine

## 1. Purpose and status

C00 defines Batch C schema-layer doctrine for shared conversion-stage content record grammar, schema-family registry behavior, and corpus-scale governance controls used by downstream C01-C14 families. It hardens the shared base for broad conversion pressure from a mixed donor corpus without allowing donor assumptions to become Astra schema authority.

Status posture:
- This file is schema-todo fulfillment drafted as schema-draft material.
- This file is not marked current canon.
- C00 records are conversion and canon-review artifacts; they are not sourcebook prose, final mechanics, runtime state, or live-play authority.
- Status labels do not promote canon; `record_status`, `review_status`, `validation_status`, and registry health labels only route work until the appropriate owner completes review.
- This file does not define runtime event schemas, command lifecycle, event-sourced state model, state delta validator, context packet compiler, hidden-information runtime state, live-play behavior, canon promotion procedure, final mechanics, accepted lexicon terms, final sourcebook prose, or donor record formats as Astra defaults.

Authority hierarchy for C00 interpretation:
1. Current Astra doctrine/project source files.
2. Accepted canon/sourcebook material if formalized.
3. Converted Astra-native donor content.
4. Examples/training materials.
5. Original donor assumptions.

Phase boundary posture:
- doctrine design, extraction/handoff, conversion intake, conversion output, canon review, runtime/backend, live-play behavior, and training/evaluation examples remain separate phases;
- C00 owns Batch C shared schema doctrine only;
- C00 must not own Batch A mechanics, Batch B operational procedure, C01-C14 family-specific schema details, canon promotion decisions, runtime entity/event/state schemas, live-play GM behavior, training examples, final mechanics, or sourcebook prose.

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
- `AstraContentRecordBase` fields that every C-family conversion-stage record must inherit or include;
- provenance grammar and provenance-lock posture;
- source-local boundary records;
- rejected imports and rejected donor element records;
- canon eligibility routing signals;
- confidence, review, lineage, composition, validation, and coverage-gap routing;
- versioning and cross-reference fields;
- schema-registry behavior and inheritance rules for C01-C14.

## 3. What this file must not own

C00 must not define:
- final mechanics;
- exact math;
- canon acceptance;
- canon promotion procedure;
- runtime state schema;
- runtime state fields;
- runtime event schema;
- runtime state/schema/event/command lifecycle;
- command lifecycle;
- event-sourced state model;
- state delta validator;
- context packet compiler;
- hidden-information runtime state;
- live-play behavior;
- Batch B operational procedure;
- C01-C14 family-specific fields;
- donor field names as Astra defaults;
- donor record shapes;
- donor record formats as Astra defaults;
- donor statblocks as Astra combat schema;
- donor currencies as Astra economy;
- donor class structures as Astra advancement schema;
- donor cosmology as Astra setting doctrine;
- donor proper nouns as Astra canon;
- accepted lexicon terms;
- training examples as schema authority;
- final sourcebook prose.

C00 does not draft C01-C14, K-layer, B-layer, R-layer, or T-layer files and does not redefine A-layer ownership. C00 does not define C01-C14; it defines only their shared base expectations and registry governance.

## 4. AstraContentRecordBase

Every durable C-family conversion-stage record must inherit or include this shared semantic base before any family-specific shaping. The block is a YAML-like doctrine shape, not a runtime schema implementation:

```yaml
AstraContentRecordBase:
  record_id: string
  record_type: string
  schema_family: C00 | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema
  schema_version: string
  doctrine_version: string
  record_status: conversion_stage | source_local | canon_candidate | accepted_canon | accepted_with_limits | quarantined | rejected_import | deprecated | superseded
  source_status: extracted_packet | conversion_intake | converted_output | canon_review | manual_review
  packet_refs: [string]
  source_evidence_refs: [string]
  construct_refs: [string]
  outcome_refs: [string]
  primary_scope: string
  candidate_scopes: [string]
  scope_priority_decision_ref: string | null
  boundary_confidence: high | medium | low | blocked
  extraction_confidence: high | medium | low | blocked
  conversion_confidence: high | medium | low | blocked
  provenance_refs: [string]
  parent_record_refs: [string]
  child_record_refs: [string]
  cross_reference_records:
    - record_ref: string
      relation_type: contains | references | depends_on | modifies | grants_access_to | costs | produces | located_in | owned_by | opposes | source_local_context | other
      inheritance_allowed: false
      note: string
  owner_layer: Batch_C
  supporting_owner_layers: [Batch_A | Batch_B | canon_review | lexicon_review | runtime_review | extraction_repair | human_review]
  source_local_boundary: string | null
  canon_eligibility:
    eligible: boolean
    status: not_reviewed | candidate | accepted | accepted_with_limits | rejected | quarantined
    reason: string
    required_review: none | lexicon | doctrine | canon | runtime | legal | human
  rejected_donor_elements:
    - element: string
      rejection_type: donor_math | donor_term | donor_cosmology | proper_noun | exact_economy | exact_class_structure | exact_statline | table_roll_assumption | adventure_script | legal_or_ip_risk | other
      reason: string
      preserved_as_evidence: boolean
  lexicon_refs: [string]
  donor_terms_preserved: [string]
  retrieval_tags: [string]
  doctrine_tags: [string]
  donor_tags: [string]
  access_tags: [string]
  ip_legal_flags:
    ip_risk_class: license_verified | srd_safe | copyright_unclear | verbatim_risk | trademark_risk | do_not_reproduce | unknown
    legal_review_required: boolean
    proper_noun_or_trademark_refs: [string]
    verbatim_similarity_risk: low | medium | high | unknown
  source_reliability:
    reliability_tier: tier_1_verified | tier_2_community | tier_3_unverified | tier_4_synthetic_or_adversarial | unknown
    reliability_basis: string
    canon_eligibility_limit: candidate_allowed | candidate_with_limits | source_local_only | prohibited | unknown
  record_lineage:
    schema_version_at_creation: string
    schema_version_at_last_validation: string
    batch_id_at_creation: string | null
    referenced_by_records: [string]
    downstream_invalidation_risk:
      status: none | low | medium | high
      reason: string | null
      revalidation_required: boolean
  composition_metadata:
    composition_id: string | null
    primary_record_ref: string | null
    satellite_record_refs: [string]
    composition_role: primary | satellite | standalone | unresolved
  review_required: boolean
  reviewer_notes: string | null
  validation_status: pending | passed | failed | quarantined
  validation_errors: [string]
```

Supporting rules:
- `owner_layer: Batch_C` means the record grammar is governed here; supporting owner layers may review, block, or consume but do not silently rewrite the C00 base.
- `schema_family: pending_schema` is allowed only when no C-family owner is stable enough; it is not a license to invent family-specific fields.
- `candidate_scopes`, confidence fields, review fields, and validation fields route uncertainty; they do not become canon, runtime authority, or final mechanics.
- Donor terms may be preserved in `donor_terms_preserved`, `donor_tags`, evidence, or rejected-element records, but donor field names are not Astra schema labels.
- Tag separation remains mandatory: `doctrine_tags` classify doctrine-domain meaning, `retrieval_tags` classify indexing metadata, `donor_tags` preserve donor-native descriptors without promotion, and `access_tags` classify visibility/access posture.

## 5. Record-status rules

`record_status` is distinct from `canon_eligibility`, `validation_status`, and registry readiness.

- `conversion_stage` is not canon.
- `source_local` is bounded to a source/campaign/context; source-local records do not become canon through C00.
- `canon_candidate` is only a proposal for later review; canon_candidate is not accepted canon.
- `accepted_canon` and `accepted_with_limits` may only be assigned after canon review by the canon owner.
- `quarantined` records cannot be normalized by invention.
- `rejected_import` records preserve refusal rationale and evidence.
- `deprecated` and `superseded` records require lineage, migration notes, and downstream invalidation review.
- Status labels do not promote canon, do not create accepted lexicon terms, and do not authorize runtime import.

## 6. Schema-family registry governance

C00 governs shared base rules for these Batch C schema families only; it does not define the family-specific fields for C01-C14.

- C00: shared content record base and schema registry doctrine.
- C01: creature/NPC.
- C02: item/gear.
- C03: ability/power/technique.
- C04: relic/implant/installable asset.
- C05: faction/institution.
- C06: location/site/region.
- C07: mission/scenario/adventure.
- C08: vehicle/ship/platform.
- C09: hazard/environment.
- C10: table/oracle.
- C11: companion/summon.
- C12: crafting/salvage/recipe.
- C13: map/diagram annotation.
- C14: source-local setting/cosmology.
- pending_schema: constructs blocked by missing schema doctrine or unstable ownership.

Required schema registry entry shape:

```yaml
CFamilyRegistryEntry:
  file_id: C00 | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14
  filename: string
  proposed_path: string
  schema_family_name: string
  owned_scopes: [string]
  non_owned_scopes: [string]
  current_status: not_started | stub_index_only | minimum_unlock_draft | tested_minimum | stable_for_family | stable_cross_family | superseded | deprecated
  schema_version: string
  last_validated_at: string | null
  supported_packet_types: [string]
  deferred_packet_types: [string]
  related_batch_a_files: [string]
  related_batch_b_files: [string]
  related_c_files: [string]
  open_escalation_refs: [string]
  open_quarantine_refs: [string]
  active_waiver_refs: [string]
  legal_ip_flag_count: integer
  canonical_test_corpus_refs: [string]
  ci_validation_status: pending | passed | failed | not_applicable
  audit_log_refs: [string]
  health_score: integer | null
```

Registry rules:
- No C-family record may claim stable coverage without a registry entry.
- Registry drift is a validation failure.
- Missing registry coverage produces quarantine or escalation, not invented schema fields.
- Static file existence is not the same as schema readiness.
- The schema registry records readiness and owner fit; it does not promote canon or define downstream runtime import procedures.

## 7. Provenance chain and evidence lock posture

Every durable C-family record preserves this provenance chain:

`source file -> extraction run -> packet id -> page/range -> SourceEvidenceIR -> ConstructIR -> OutcomeIR -> Batch C record -> canon/review status`

Required references:
- `packet_refs`;
- `source_evidence_refs`;
- `construct_refs`;
- `outcome_refs`;
- `provenance_refs`.

A record with a broken provenance chain cannot be promoted, compared, used as stable conversion output, or handed to runtime without review.

Optional but preferred hash/provenance-lock fields:

```yaml
provenance_lock:
  source_evidence_hash: string | null
  hash_algorithm: string | null
  extraction_run_id: string | null
  packet_hash: string | null
  sidecar_hashes: [string]
  hash_lock_status: locked | changed | unavailable_early_pilot | not_applicable
```

Invalidation triggers:
- `source_evidence_hash_changed`;
- `packet_hash_changed`;
- `repaired_sidecar_hash_changed`;
- `extraction_run_reprocessed_without_supersession_record`.

When hash locks are unavailable in early pilots, records must state `hash_lock_status: unavailable_early_pilot` and require manual review before canon or runtime handoff.

## 8. Inheritance and composition rules

- `inheritance_allowed: false` is the default for cross-record relations.
- A child record does not inherit canon status.
- A child record does not inherit source-local boundary.
- A child record does not inherit mechanical authority.
- A child record does not inherit runtime ownership.
- A parent record may contain child records without owning their doctrine.
- Complex constructs must compose through `parent_record_refs`, `child_record_refs`, `cross_reference_records`, and `composition_metadata`.
- Satellite records are allowed for abilities, effects, costs, hazards, map notes, loot, factions, or other components that cannot be merged safely into a parent record.
- Schema Frankensteins are prohibited: one record must not merge cost, effect, item host, faction unlock, map state, runtime state, and canon decision authority merely because a donor source presented them together.

## 9. Source-local boundary object rules

`source_local_boundary` is a structured containment concept. A compact string reference may appear in `AstraContentRecordBase`, but every `source_local` record must resolve that reference to this object shape:

```yaml
source_local_boundary:
  boundary_id: string
  source_id: string
  packet_refs: [string]
  local_context_type: adventure | campaign | sourcebook | faction | location | setting | encounter | table | other
  preserved_elements: [string]
  non_generalized_elements: [string]
  prohibited_promotions: [string]
  canon_review_required_for_reuse: boolean
```

Rules:
- Every `source_local` record must define a `source_local_boundary`.
- Proper nouns must be source-local, rejected, or routed to legal/IP review unless canon review later accepts a stripped pattern.
- A named faction, place, relic, deity, planet, adventure script, timeline, or cosmology remains bounded unless promoted through canon review.
- Source-local records may generate canon candidates only for reusable Astra functions, not for the named local wrapper.
- Source-local record terms do not become accepted lexicon terms through C00.

## 10. Rejected donor element rules

Rejected donor elements are explicit records, not silent deletions. The base field `rejected_donor_elements` may summarize the refusal, and a durable `rejected_donor_element_record` preserves full routing:

```yaml
rejected_donor_element_record:
  rejection_id: string
  record_ref: string
  source_evidence_refs: [string]
  donor_element: string
  rejection_type: donor_math | donor_term | donor_cosmology | proper_noun | exact_economy | exact_class_structure | exact_statline | table_roll_assumption | adventure_script | legal_or_ip_risk | other
  reason: string
  preserved_as_evidence: boolean
  replacement_handling: preserve_as_evidence | normalize_later_under_doctrine | source_local_only | quarantine | escalate | discard_after_review
  reviewer_notes: string | null
```

Rules:
- Rejection is not silent deletion.
- Donor field names are not Astra schema labels.
- Donor math is preserved as evidence or normalized later under doctrine; C00 does not adopt it.
- Donor stat values are not Astra combat math.
- Donor currency/prices are not Astra economy.
- Donor spell levels, class structures, challenge ratings, point costs, and table roll ranges are not Astra defaults.
- Donor cosmology and proper nouns are source-local or rejected unless promoted.
- Rejected-import records preserve refusal rationale and provenance.

## 11. Canon eligibility rules

`record_status` and `canon_eligibility` are separate. A record can be valid conversion output and still be ineligible for canon.

Rules:
- `record_status: accepted_canon` may only appear after canon review.
- `canon_candidate` is not accepted canon.
- Single-source usefulness is not canon pressure by itself.
- Repeated donor pressure is evidence, not law.
- Proper nouns, exact donor math, exact statlines, exact currencies, exact class structures, adventure scripts, and donor cosmology are not eligible without stripping, scoping, and review.
- Canon eligibility requires owner, scope, conflict awareness, lexicon review as needed, and sufficient evidence.
- Canon eligibility flags do not define canon promotion procedure; they only route later K-layer/canon review.

## 12. Legal/IP and source reliability routing

C00 records include legal/IP and reliability routing signals:
- `ip_risk_class`;
- `legal_review_required`;
- `proper_noun_or_trademark_refs`;
- `verbatim_similarity_risk`;
- `reliability_tier`;
- `reliability_basis`;
- `canon_eligibility_limit`.

Rules:
- These fields are risk-routing signals, not legal determinations.
- Raw donor text should not be embedded unnecessarily in schema records.
- Proper nouns and trademarks must be bounded, rejected, or reviewed.
- Synthetic/unverified sources may be useful for stress tests but may limit canon eligibility.
- Legal/IP flags do not grant reuse rights, canon status, or sourcebook publication authority.

## 13. Missing-schema fallback policy

When no C-family schema exists or no owner is stable enough, C00 permits missing-schema fallback routing only through these outcomes:
- `pending_schema`;
- quarantine;
- escalation;
- human_review;
- defer_until_schema_exists;
- source_local containment if safely bounded.

Forbidden fallback behavior:
- inventing new schema fields inside conversion output;
- using donor record shape as fallback schema;
- routing to the nearest familiar C-file without owner fit;
- treating C00 as a family-specific schema.

Unclassifiable records are quarantined or escalated, not normalized by invention. Missing-schema fallback exists to expose coverage gaps, not to erase them.

## 14. Batch B handoff boundary

- Batch B owns operational/world-interaction procedure.
- Batch C owns content-family record grammar.
- B files may reference C00 for shared record handoff requirements.
- B files must not define C-family record shapes.
- C00 must not define B operational procedures.
- A B-to-C handoff should name the target C-family or `pending_schema` plus quarantine/escalation if no schema exists.
- Batch B handoff records may carry packet, construct, outcome, and review references, but the target Batch C schema family remains responsible for content-family record grammar.

## 15. Runtime boundary

Runtime is a downstream consumer boundary, not C00 ownership.

- C00 records are conversion/canon-review artifacts, not runtime state.
- Runtime state, event sourcing, command lifecycle, deterministic dice, state delta validation, context packet compilation, hidden information, replay, persistence, and live-play command authority belong to R-layer/runtime doctrine.
- Runtime may later consume accepted or validated schema records, but only through runtime-owned validation and import procedures.
- A C00 record cannot mutate campaign state.
- A runtime-event record placeholder may exist only as a boundary marker and may not define runtime event schemas, command lifecycle, event sourcing, context packet assembly, hidden-information state, live-play state, or state mutation behavior.

## 16. Training and evaluation boundary

Training and evaluation artifacts may test compliance, but they do not own schema doctrine.

- Training examples do not create schema authority.
- Evaluation examples can test C00 compliance but cannot promote records.
- Live-play examples must not bypass runtime state validation.
- Model confidence is not schema status.
- Training or evaluation examples must not convert donor record formats, donor math, donor proper nouns, or donor cosmology into Astra defaults.

## 17. Coverage-gap reporting

Coverage gaps must be named and routed through review instead of hidden by invented fields.

```yaml
SchemaCoverageGap:
  gap_id: string
  blocked_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | unknown
  affected_construct_refs: [string]
  affected_packet_types: [string]
  affected_donor_families: [string]
  severity: low | medium | high | blocking
  current_handling: pending_schema | quarantine | escalation | human_review | source_local
  required_next_action: draft_schema | repair_extraction | doctrine_review | lexicon_review | canon_review | runtime_review | human_review
  reviewer_notes: string
```

Rules:
- Coverage gaps must be named, not vague.
- No broad conversion pilot may claim coverage where blocking schema gaps remain without quarantine/escalation plan.
- Coverage-gap records are not canon candidates.
- A `SchemaCoverageGap` record is a governance signal, not a substitute C-family schema.

## 18. Conversion mapping rules

- Map donor evidence into `AstraContentRecordBase` before any family-specific shaping.
- Preserve ambiguous or conflicting donor evidence through `source_local_boundary`, `rejected_donor_elements`, `canon_eligibility`, `record_lineage`, `validation_errors`, review queues, and escalation paths instead of forced normalization.
- Keep `canon_eligibility` and status fields as routing signals only; they do not grant canon acceptance.
- Never normalize by inventing mechanics, runtime state behavior, lexicon acceptance, sourcebook prose, or donor-derived schema shapes.
- Conversion output may preserve donor math only as evidence unless later doctrine normalizes an Astra-native representation.

## 19. Donor pressure absorbed

C00 is designed to absorb donor pressure from fantasy, science fiction, science fantasy, cultivation, tactical, narrative/tag/aspect, point-buy, class-level, lifepath, horror/investigation, cyberware/biotech, vehicle/ship/platform, companion/summon, crafting/salvage, random-table/oracle, bestiary/statblock, adventure-path, map/diagram, faction, setting/cosmology, and mixed/outlier material.

C00 absorbs pressure from:
- donor statblock/table/item/ability/location/faction formats;
- proper-noun leakage;
- incomplete provenance;
- conflicting donor naming and structure conventions;
- mixed-confidence extraction artifacts;
- donor currencies, donor class structures, donor adventure scripts, donor cosmology, and donor terms.

Absorption means auditable classification/routing, not donor-default adoption.

## 20. Escalation triggers

Escalate or quarantine when:
- record structure requires unsupported fields outside the C00 base grammar;
- schema interpretation conflicts with A-layer doctrine boundaries;
- provenance cannot be preserved across a required mapping;
- record classification cannot be completed without inventing runtime or mechanics behavior;
- cross-reference/dependency relations become contradictory or non-auditable;
- a proper noun, trademark, exact donor statline, donor economy, donor class structure, donor table procedure, adventure script, or donor cosmology cannot be safely bounded;
- registry coverage is missing, drifting, or not ready for stable conversion output.

## 21. Dependencies

C00 dependency posture (registry source of truth):
- depends on A01-A15;
- is blocked by A01-A15 during pre-draft staging, then cleared for this draft record state;
- unlocks C01-C14 and K03 per registry sequencing.

C00 does not redefine A-layer ownership and does not bypass hard locks. Batch A mechanics remain separate from Batch C schema grammar.

## 22. Handoff to downstream layers

C00 hands off base grammar constraints to:
- C01-C14 for content-family-specific schemas;
- K03 and registry-listed canon/candidate review files for canon promotion decision routing;
- K01 for accepted lexicon and reserved-term control;
- R-layer files for runtime event schemas, runtime state, command lifecycle, context packet compiler, hidden information, and live-play state behavior;
- Batch B handoff procedures for operational routing references, not C-family shape definitions;
- conversion-intake and aggregation tooling for record validation and reporting.

Phase boundary rule: C00 hands off constraints only. C00 does not define downstream files and does not define runtime behavior.

Downstream consumers must include all C00 base fields and preserve source-local, rejected-import, provenance, legal/IP, reliability, lineage, composition, and validation audit traces.

## 23. Examples and pressure cases

- Good source-local faction: a named donor faction is stored as `record_status: source_local`, has a `source_local_boundary` tied to its source packet, routes the proper noun through `ip_legal_flags`, and proposes only a stripped reusable faction function for later C05/canon review.
- Bad source-local faction: a named faction is promoted as Astra canon through a schema record because it appears useful in one donor adventure.
- Good statblock handling: a donor statblock preserves exact donor values as evidence in `source_evidence_refs` and `rejected_donor_elements`, then maps unresolved creature, ability, and hazard questions to pending C01/C03/C09 refs.
- Bad statblock handling: a donor statline is copied as Astra combat schema, combat math, challenge rating, or default NPC format.
- Good random table handling: a donor random table is retained source-locally with a C10 target, row-level provenance, and table roll assumptions marked as evidence rather than universal procedure.
- Bad random table handling: donor d100 table roll ranges are treated as Astra universal table procedure.
- Good ability composition: an ability record references cost, effect, damage, and host constraints through satellite records and `composition_metadata`.
- Bad ability composition: an ability record merges cost, damage, item host, faction unlock, and runtime state into one schema Frankenstein.
- Provenance retention example: a donor record with partial extraction still retains `packet_refs`, `source_evidence_refs`, `construct_refs`, `outcome_refs`, and `provenance_refs`.
- Rejected-import example: donor-shaped runtime-state payload is captured as `rejected_import` with refusal rationale and provenance.
- Quarantine/escalation example: contradictory donor claims that cannot be classified without invention are quarantined or escalated.
- Canon-candidate boundary example: a high-confidence record labeled `canon_candidate` remains non-canon pending K-layer/canon review.

## 24. Versioning and review protocol

- C00 remains draft/not-current until registry promotion requirements are satisfied.
- Substantive C00 edits require versioned registry changelog updates and re-review when the registry convention requires it.
- `reviewer_notes`, `validation_status`, and `validation_errors` track review workflow posture and do not themselves promote canon.
- Deprecated and superseded records require lineage/migration notes through `record_lineage` and downstream invalidation review.
- C00 governance remains schema-layer only and does not authorize runtime behavior, live-play behavior, accepted lexicon terms, final mechanics, or sourcebook prose.
