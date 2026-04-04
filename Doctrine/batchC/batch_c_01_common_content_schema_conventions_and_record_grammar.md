# batchC_01_common_content_schema_conventions_and_record_grammar.md

## Purpose and authority

This file is the **common record-grammar authority** for all Batch C content schemas.

Its job is to define the shared structural language by which Astra Ascension represents content records, overlays, compositions, and containers. It exists so later Batch C files do not invent incompatible record shapes, naming habits, dependency styles, lifecycle labels, provenance blocks, validation meanings, or packaging logic on the fly.

This file is therefore constitutional rather than family-specific.

It owns:
- shared Batch C record ontology
- universal record anatomy
- canonical identity and revision conventions
- provenance and normalization fields
- governance and authority references
- dependency and relationship grammar
- content-class distinctions
- scaling, applicability, and compatibility fields
- tag and indexing doctrine
- container and bundle semantics
- null-state and unresolved-state handling
- revision and supersession doctrine
- validation and audit fields
- minimal abstract record template inherited by later Batch C files

It does **not** own:
- actor-specific fields
- item-specific fields
- site-specific fields
- faction-specific fields
- mission-specific fields
- reward-specific fields
- generator-specific fields
- sourcebook-bundle specifics beyond common container law
- donor conversion outputs as such
- canon decisions
- live-play presentation behavior

Later Batch C files must inherit this record grammar and then define the family-specific payloads they own.

## Why this file exists

Batch C is the doctrine layer where Batch A and Batch B become instantiable content structure. That means Batch C cannot survive corpus-scale conversion pressure unless it begins with a stable shared record grammar.

Without a common record grammar, later conversion work will drift into:
- ad hoc record headers
- inconsistent relationship language
- unstable record identity
- provenance loss
- schema/instance/canon confusion
- container duplication
- silent ownership drift
- incompatible bundles and packets
- misleading validation labels

This file exists to stop that drift before it begins.

## Core constitutional principles

1. **Schema is not instance.**
   A schema defines allowable structure. An instance is one populated record using that structure.

2. **Instance is not converted output.**
   A converted donor entry may instantiate a schema, but the conversion result does not become doctrine merely by existing.

3. **Converted output is not canon.**
   Canon requires explicit consolidation elsewhere.

4. **Record identity must remain stable across reuse.**
   Repackaging a record into a new bundle or packet does not automatically create a new record.

5. **Revision identity must remain distinct from record identity.**
   The system must be able to distinguish “same record, newer revision” from “new derivative record.”

6. **Relationships must be explicit.**
   Cross-record logic must be declared through normalized relationship grammar rather than implied through prose.

7. **Dominant-function routing remains mandatory.**
   Hybrid records must declare their primary doctrinal job and secondary dependencies without re-owning outside doctrine.

8. **Common grammar must stay common.**
   This file must not become a disguised actor, item, site, mission, or bundle file.

9. **Inherited common fields may be constrained but not redefined.**
   Later family files may extend this grammar, require additional local subfields, or narrow local usage, but they may not silently change the meaning of inherited common fields.

10. **Unknown is lawful.**
    Missing, ambiguous, withheld, fragmentary, or quarantined information must be represented explicitly rather than invented decoratively.

11. **Containers package content; they do not redefine atomic identity.**

12. **Every reusable content record must remain auditable.**
    The system must be able to tell what a record is, where it came from, what authorized it, what changed, how confident the mapping is, and what remains unresolved.

## Record ontology

All Batch C records must declare their record class and ontology state.

### Record classes

A Batch C record must declare one of the following high-level classes:

- **atomic_record** — a single content object with stable identity
- **overlay_record** — a modifier or specialization applied to another record
- **composite_record** — a bounded assembly of lower records into a reusable structure
- **container_record** — a packaging structure that groups records for reference, conversion output, anthology use, or sourcebook-style delivery
- **abstract_template** — a non-final reusable structural scaffold not yet representing a specific content record

### Ontology states

A Batch C record must declare one ontology state from the following controlled set:

- **doctrine_schema**
- **family_schema**
- **abstract_template**
- **instantiated_record**
- **converted_donor_record**
- **normalized_astra_record**
- **canonized_record**
- **example_record**
- **deprecated_record**
- **superseded_record**
- **quarantined_record**
- **fragmentary_placeholder_record**

### Ontology distinction note

- **doctrine_schema** is reserved for cross-family structural or doctrinal schema authority whose meanings govern other schemas.
- **family_schema** is reserved for a specific content-family schema file that inherits doctrine_schema meanings and adds family-owned payload structure.

These states are not flavor labels. They are governance labels with authority implications.

## Record lifecycle states

Ontology answers what kind of record something is. Lifecycle answers where it is in work history.

All non-schema records must support lifecycle state declaration.

Controlled lifecycle values:
- **draft**
- **validated**
- **converted**
- **normalized**
- **provisionally_accepted**
- **quarantined**
- **deprecated**
- **superseded**
- **merged**
- **split**
- **canonized**
- **archived**

A record may change lifecycle state without changing identity, but some changes require new identity. That distinction must be declared explicitly under revision doctrine.

## Universal record anatomy

Every Batch C record must expose the same top-level structural blocks, even when some blocks are empty or marked not_applicable.

Required top-level blocks:
- `identity`
- `classification`
- `provenance`
- `governance`
- `dependencies`
- `relationships`
- `state`
- `scale_and_applicability`
- `tags_and_indexing`
- `container_placement`
- `audit_and_validation`

Family-specific Batch C files may add payload blocks beneath this shared spine, but they must not remove the spine.

## Identity doctrine

The identity block defines what the record is and how it remains recognizable across reuse, revision, bundling, or conversion history.

### Required identity fields

Every Batch C record must support:
- `canonical_id`
- `record_name`
- `record_class`
- `family_owner`
- `display_name`
- `alias_set`
- `visibility_stratum`
- `field_visibility_overrides`

### Canonical ID rules

A canonical ID must:
- be Astra-native rather than donor-native
- remain stable for the life of the record identity
- not be rewritten merely because the record appears in a new packet or bundle
- distinguish the record from overlays, derivatives, and pinned bundle inclusions
- support future retrieval, deduplication, and training use

### Alias doctrine

A record may support multiple names without losing identity. Alias categories should be controlled rather than freeform.

Recommended alias categories:
- Astra-native preferred name
- donor-native name
- donor transliteration or translation variant
- common-use alias
- deprecated name
- classified or internal alias where relevant

Aliases are descriptive, not identity-bearing. They do not replace canonical ID.

### Record-name and display-name distinction

- `record_name` is the stable internal human-readable label for the record.
- `display_name` is the preferred context-facing presentation label for a given exposed form.

These fields may coincide, but they do not perform the same doctrinal job.

## Revision identity doctrine

Revision identity must be represented separately from record identity.

### Required revision-identity fields

Every Batch C record must support:
- `record_revision_id`
- `version_line`
- `revision_status`

### Revision doctrine

- `canonical_id` is the immutable identity anchor for the record.
- `record_revision_id` identifies a specific revision state of that record.
- `version_line` identifies continuity across revisions when such lineage tracking is needed.
- A revision may preserve canonical identity while changing revision identity.
- A derivative, split, or other identity-breaking change must receive a new canonical ID.

This distinction is mandatory because corpus-scale conversion must be able to answer whether two entries are the same object in different revisions or two different objects.

## Classification doctrine

The classification block identifies what kind of thing the record is within the common grammar without collapsing into payload-specific doctrine.

Required classification support:
- `ontology_state`
- `lifecycle_state`
- `dominant_function`
- `secondary_functions`
- `content_family`

`content_family` is classificatory. `family_owner` is governance. They often align, but they are not identical concepts.

## Provenance and donor-trace doctrine

Every record must preserve how it entered Astra and how aggressively it was normalized.

### Required provenance dimensions

Every Batch C record must support:
- `source_origin`
- `source_reference`
- `donor_construct_type`
- `conversion_method`
- `normalization_level`
- `authority_basis`
- `fragment_aggregation_status`
- `conversion_confidence`
- `interpretation_confidence`
- `evidence_completeness`

### Source-origin examples

Allowed source-origin types may include:
- Astra doctrine
- donor sourcebook
- converted donor bundle
- canon sourcebook
- internal example pack
- merged fragment set
- synthetic abstract template

### Conversion method examples

Controlled values may include:
- direct_mapping
- normalized_mapping
- source_local_retention
- composite_rebuild
- doctrine_escalation_required
- provisional_placeholder

### Normalization level examples

Controlled values may include:
- near_direct
- moderate_normalization
- high_normalization
- Astra_reframed
- unresolved

### Confidence doctrine

The confidence fields exist so uncertainty remains standardized rather than buried in notes.

- `conversion_confidence` expresses confidence in the conversion outcome as a whole.
- `interpretation_confidence` expresses confidence in how the source material was interpreted.
- `evidence_completeness` expresses how complete the supporting material is.

These fields should use controlled values appropriate for later workflow, such as high, moderate, low, fragmentary, or provisional.

### Provenance law

Provenance must answer at least eight questions:
1. Where did this come from?
2. What kind of donor thing was it?
3. How was it converted or formed?
4. How normalized is it?
5. Which Astra authority authorized the result?
6. How complete is the evidence base?
7. How confident is the mapping?
8. Were multiple fragments congruent, partial, or conflicting?

If one Astra record is assembled from multiple donor fragments, the record must preserve fragment provenance rather than flattening it into a single vague source note.

## Fragment aggregation and conflict doctrine

Large donor libraries will frequently require aggregation across core rules, errata, supplements, setting books, tables, and adventure-path material. Aggregation therefore must distinguish assembly from conflict handling.

Recommended fragment aggregation statuses:
- `single_source`
- `congruent_fragment_merge`
- `partial_fragment_merge`
- `conflicting_fragment_merge`
- `unresolved_fragment_conflict`
- `superseded_fragment_source`
- `fragmentary_reconstruction`

Where fragments disagree, the record must preserve the disagreement or its resolution path rather than collapsing the conflict into silent certainty.

## Governance and authority references

Every record must declare how it is governed inside Astra doctrine.

Required governance fields:
- `primary_owner`
- `secondary_dependencies`
- `authority_rank`
- `governing_files`
- `forbidden_owner_drift`
- `escalation_flags`

### Authority-rank note

`authority_rank` should use a controlled vocabulary rather than freeform prose. This file does not lock the final enumeration, but later Batch C files and conversion workflows must treat it as a governed field whose values distinguish structural authority levels such as doctrine, schema, converted output, canon review state, or analogous governance strata.

### Primary owner

The primary owner is the Batch C family file that structurally owns the record type.

Examples:
- actor entries -> C02
- overlays -> C03
- items/assets -> C04
- frames -> C05
- sites -> C06
- factions -> C07
- challenge objects -> C08
- encounters -> C09
- missions -> C10
- reward parcels -> C11
- generators -> C12
- sourcebook containers -> C13

### Secondary dependencies

A record may depend on Batch A or Batch B files without re-owning them. Secondary dependencies must name the external files whose doctrine is being composed.

### Inheritance discipline

Common grammar fields are inherited, not reinterpreted. Later family files may:
- require additional local subfields
- constrain local usage
- add family-owned payload blocks

Later family files may not:
- silently change the meaning of inherited common fields
- redefine shared relationship verbs to mean something new
- convert common provenance fields into family-specific mechanics fields
- treat shared container semantics as optional unless this file explicitly allows it

The following inherited fields or field groups should also use controlled vocabularies rather than freeform prose unless a later file explicitly governs a narrower local enumeration:
- `revision_status`
- `multi_anchor_status`
- `local_override_status`
- `field_visibility_overrides`
- `escalation_flags`
- `authority_rank`

### Forbidden owner drift

A record must not silently absorb doctrine owned by another file. Where spillover risk is high, the governance block should note that risk explicitly.

## Dependency doctrine

Dependencies declare what a record needs in order to be interpreted or used correctly.

Dependency categories may include:
- structural dependency
- doctrinal dependency
- payload dependency
- overlay dependency
- scaling dependency
- container dependency
- validation dependency

Dependencies are not the same as relationships. A dependency says what the record requires. A relationship says how one record stands relative to another.

Dependencies may target doctrine files, schema files, or concrete records, provided the dependency category is explicit.

## Relationship grammar

Batch C records must use normalized relationship grammar. A record must not merely point to another record; it must declare the nature of the link.

### Controlled relationship verbs

Core relationship verbs:
- `contains`
- `requires`
- `references`
- `instantiates`
- `inherits`
- `derives_from`
- `overlays`
- `modifies`
- `scales_with`
- `gated_by`
- `emitted_by`
- `located_in`
- `controlled_by`
- `opposed_by`
- `rewards_with`
- `sourced_from`
- `supersedes`
- `duplicated_by`
- `incompatible_with`
- `member_of`
- `anchored_to`
- `assembled_from`
- `variant_of`
- `instance_of`
- `pinned_in`

Later Batch C files may refine usage guidance, but they must not casually proliferate new verbs unless repeated corpus pressure proves the current set insufficient.

### Relationship entry minimums

A relationship entry should support:
- `verb`
- `target_id`
- `target_kind`
- `target_family`
- `directionality`
- `cardinality`
- `scope`
- `notes`
- `strength_or_priority` where relevant

### Relationship target typing

`target_kind` should be used where useful to distinguish whether the relationship points to:
- a doctrine file
- a schema file
- a concrete record
- a container record
- an external source reference

This prevents later records from forcing target interpretation to be inferred indirectly from `target_family` alone.

### Relationship directionality and cardinality

- `directionality` distinguishes one-way, reciprocal, or contextually mirrored relationships.
- `cardinality` distinguishes one-to-one, one-to-many, many-to-one, many-to-many, exclusive, ordered, or bounded relationships where relevant.

These fields are optional when obvious, but they should be used wherever ambiguity would otherwise be pushed into prose.

### Relationship law

- Relationship prose must not replace relationship structure.
- Multiple different relationships to the same target must be represented distinctly.
- Relationship structure must support machine-legible retrieval later.
- Where reverse linkage is needed, it must be explicit rather than assumed.

## Atomic, overlay, composite, derivative, and container doctrine

### Atomic record

An atomic record is a single reusable content object with stable identity.

Examples include:
- one actor
- one item or relic
- one site
- one faction
- one hazard
- one reward parcel

### Overlay record

An overlay record modifies, specializes, skins, scales, or conditions another record without replacing the base identity outright.

Examples include:
- elite variant
- corruption layer
- faction skin
- biome variant
- mission-local modifier
- mounted package

### Composite record

A composite record is a bounded assembly of lower records into a reusable playable structure.

Examples include:
- encounter packet
- scene packet
- mission structure
- investigation lattice
- scenario packet

### Derivative record

A derivative record is a new record produced from another record when the changes exceed the threshold of simple overlay or local override.

Derivative use is appropriate when:
- stable identity no longer reasonably holds
- the new version is intended for independent reuse
- the modified state is no longer temporary or local
- the source and derivative must coexist as distinct valid records

### Container record

A container record packages records together for reference, bundle, sourcebook, or anthology purposes without necessarily changing the identity of included records.

Examples include:
- bestiary pack
- city guide
- faction dossier
- converted sourcebook bundle
- canon anthology

## Scaling, applicability, and compatibility doctrine

Every record must declare how it scales, where it applies, and what it can accept or emit.

These are generic declarative fields. They are not numerical mechanics definitions and must not be used to smuggle downstream mechanics into C01.

### Scaling fields

A record may declare scaling axes such as:
- threat band
- rank band
- tier band
- rarity band
- legality band
- influence band
- scope band

### Applicability fields

A record may declare scope of applicability such as:
- actor_scale
- squad_scale
- site_scale
- district_scale
- region_scale
- world_scale
- narrative_scale
- setting_scale

A record may also declare domain of use such as:
- combat
- traversal
- downtime
- research
- diplomacy
- mission_design
- encounter_composition
- reward_distribution
- generator_output

### Compatibility fields

Every record family should be able to declare:
- overlays accepted
- overlays emitted
- compatible containers
- incompatible contexts
- required support schemas

This allows later files to inherit compatibility grammar instead of inventing special one-off attachment rules.

## Tag and indexing doctrine

To remain searchable and deduplicable at corpus scale, every record must support disciplined indexing.

Required indexing support:
- `family_tags`
- `function_tags`
- `retrieval_tags`
- `donor_alias_tags`
- `setting_or_context_tags` where relevant
- `reserved_name_flags` where relevant

Tag doctrine must stay subordinate to canonical identity. Tags assist retrieval and grouping; they do not define authority.

## Container placement and cross-container persistence

A record must be able to exist in multiple containers without accidental identity drift.

### Placement fields

A record should support:
- `home_container`
- `additional_containers`
- `pinned_bundle_membership`
- `multi_anchor_status`
- `local_override_status`

`home_container` may be empty or `not_applicable` for freestanding atomic records that are not yet anchored to a canonical bundle, dossier, packet, or sourcebook-style container.

### Cross-container law

1. Inclusion in multiple containers does not by itself create a new record.
2. A bundle may pin a specific revision of a record.
3. Pinned bundle inclusion should reference both `canonical_id` and `record_revision_id`, not merely the record in general.
4. A later revision to the atomic record must not silently mutate a previously pinned bundle instance.
5. A local scenario override does not automatically create a derivative record.
6. If local override becomes reusable beyond its original container, it should be reviewed for overlay or derivative promotion.

### Container semantics decision rule

Batch C must distinguish four different operations:

- **inclusion** — the record appears inside a container while remaining the same record
- **instantiation** — the schema or abstract form is realized as a concrete record for use
- **pinning** — a container fixes a specific record revision for historical or bundle integrity reasons
- **local derivative use** — a container creates a temporary or context-bound modification that may later be promoted into overlay or derivative status

A container may include or pin a record without owning it. A local use-case may instantiate or temporarily modify a record without automatically generating a new atomic identity.

### Bundle immutability doctrine

Converted sourcebook bundles and anthology-style containers should support pinned inclusion so later revisions do not silently rewrite historical outputs.

## Required, optional, unknown, withheld, fragmentary, and quarantined values

Astra must support lawful incompleteness.

Controlled field-state values should include:
- `required`
- `optional`
- `not_applicable`
- `unknown`
- `withheld`
- `unresolved`
- `fragmentary`
- `quarantined`
- `redacted`

### Null-state law

- `unknown` means the value should exist but is presently not known.
- `withheld` means the value exists but is intentionally not exposed in this form.
- `not_applicable` means the field does not apply to this record.
- `unresolved` means interpretation remains under review.
- `fragmentary` means the available material is incomplete.
- `quarantined` means the value or construct is present but blocked pending doctrine review.
- `redacted` means the value is intentionally removed for visibility or release reasons.

These states are preferable to decorative completion.

## Visibility and redaction doctrine

Visibility may apply either to the whole record form or to selected fields within the record.

Suggested visibility strata:
- full_internal
- player_safe
- GM_restricted
- export_safe
- reference_only

### Visibility law

- Record-level visibility controls the default form of the record as exposed to a given audience or workflow.
- Field-level redaction controls selective suppression within an otherwise visible record.
- A record may therefore be player-safe in overall form while still redacting selected GM-only, spoiler, provenance-sensitive, or canon-sensitive fields.
- Field-level redaction must not be confused with nonexistence or unknown value.
- `field_visibility_overrides` should identify the affected field path or field block explicitly rather than falling back to vague prose.

This file does not define live-play presentation behavior, but it reserves the grammar necessary for downstream handling.

## Revision, supersession, split, merge, and versioning doctrine

Every record must support tracked change state.

Required revision support:
- `record_revision_id`
- `version_line`
- `revision_status`
- `revision_history`
- `supersedes`
- `superseded_by`
- `merged_from`
- `split_from`
- `identity_preservation_note`

### Identity-preserving changes

Examples that may remain identity-preserving:
- cleanup of indexing tags
- clearer provenance notes
- refined dependency references
- compatibility expansion that does not alter the underlying object
- overlay intake clarifications
- structural cleanup that leaves the underlying content object unchanged

### Identity-breaking changes

Examples that may require a new record:
- one record split into two reusable independent records
- local override promoted into a stable reusable variant
- heavily normalized reconstruction no longer meaningfully identical to the original converted record
- one bundle-specific packaged form becoming a general reusable object with distinct function

## Validation and audit doctrine

Every record must be auditable.

Required audit support:
- `validation_status`
- `structural_validation_status`
- `doctrinal_validation_status`
- `provenance_validation_status`
- `payload_completeness_status`
- `canon_review_status`
- `conversion_notes`
- `warnings`
- `unresolved_questions`
- `doctrine_conflict_flags`
- `review_log`

### Validation-status rollup note

`validation_status` may remain as a summary rollup field, but it is not a substitute for the tier-specific validation states below.

### Validation tier doctrine

A record can be:
- structurally valid but doctrinally weak
- doctrinally valid but provenance-fragmentary
- provenance-sound but payload-incomplete
- complete as converted output but not canonized

For that reason, broad undifferentiated uses of `validation_status` are insufficient on their own. Validation should distinguish at least structural validity, doctrinal validity, provenance sufficiency, payload completeness, and canon review state.

Audit fields exist so the corpus remains honest about uncertainty, provisional decisions, and doctrine strain.

## Anti-duplication and anti-collapse law

1. A record may summarize linked doctrine, but it must not silently re-own it.
2. A container may package content, but it must not redefine atomic record structure.
3. A schema may constrain local fields, but it must not restate unrelated upstream doctrine as if Batch C owns it.
4. A relationship must be represented through relationship grammar rather than prose-only implication.
5. An overlay must not be treated as a full atomic record unless it has crossed the derivative threshold.
6. A composite record must reference lower records rather than flattening them into bespoke one-off blobs wherever reusable identity should be preserved.
7. A converted entry must not be elevated to doctrine by repetition.
8. Cross-file references are preferred over local field duplication unless the local file truly owns the field.
9. A local convenience summary must not become the authoritative source if the linked record remains authoritative.

## Batch C inheritance and handoff rules

Later Batch C files must inherit this grammar and then define only the family-specific payloads they own.

That means:
- C02 adds actor-specific payload structure on top of this grammar.
- C03 adds overlay-specific payload structure on top of this grammar.
- C04 adds item/resource/asset payload structure on top of this grammar.
- C05 adds frame-specific payload structure on top of this grammar.
- C06 adds site/locale payload structure on top of this grammar.
- C07 adds faction/institution payload structure on top of this grammar.
- C08 adds challenge-object payload structure on top of this grammar.
- C09 adds encounter and scene composition payload structure on top of this grammar.
- C10 adds mission/scenario/arc composition payload structure on top of this grammar.
- C11 adds reward parcel payload structure on top of this grammar.
- C12 adds generator payload structure on top of this grammar.
- C13 adds container-specific payload structure on top of this grammar.

None of those files may discard the common grammar spine.

## Minimal abstract record template

The following is a doctrinal abstract template, not a finished family schema.

```yaml
record:
  identity:
    canonical_id: ""
    record_name: ""
    display_name: ""
    record_class: ""
    family_owner: ""
    alias_set: []
    visibility_stratum: ""
    field_visibility_overrides: []

  classification:
    ontology_state: ""
    lifecycle_state: ""
    dominant_function: ""
    secondary_functions: []
    content_family: ""

  provenance:
    source_origin: ""
    source_reference: []
    donor_construct_type: ""
    conversion_method: ""
    normalization_level: ""
    authority_basis: []
    fragment_aggregation_status: ""
    conversion_confidence: ""
    interpretation_confidence: ""
    evidence_completeness: ""

  governance:
    primary_owner: ""
    secondary_dependencies: []
    authority_rank: ""
    governing_files: []
    forbidden_owner_drift: []
    escalation_flags: []

  dependencies:
    structural_dependencies: []
    doctrinal_dependencies: []
    payload_dependencies: []
    overlay_dependencies: []
    scaling_dependencies: []
    container_dependencies: []
    validation_dependencies: []

  relationships: []

  state:
    record_revision_id: ""
    version_line: ""
    revision_status: ""
    validation_status: ""
    structural_validation_status: ""
    doctrinal_validation_status: ""
    provenance_validation_status: ""
    payload_completeness_status: ""
    canon_review_status: ""
    supersedes: []
    superseded_by: []
    merged_from: []
    split_from: []
    identity_preservation_note: ""

  scale_and_applicability:
    scaling_axes: []
    applicability_scope: []
    domains_of_use: []
    accepted_overlays: []
    emitted_overlays: []
    compatible_containers: []
    incompatible_contexts: []

  tags_and_indexing:
    family_tags: []
    function_tags: []
    retrieval_tags: []
    donor_alias_tags: []
    context_tags: []
    reserved_name_flags: []

  container_placement:
    home_container: ""
    additional_containers: []
    pinned_bundle_membership: []
    multi_anchor_status: ""
    local_override_status: ""

  audit_and_validation:
    conversion_notes: []
    warnings: []
    unresolved_questions: []
    doctrine_conflict_flags: []
    review_log: []
```

## Minimal relationship entry template

```yaml
relationship:
  verb: ""
  target_id: ""
  target_kind: ""
  target_family: ""
  directionality: ""
  cardinality: ""
  scope: ""
  notes: ""
  strength_or_priority: ""
```

## Final doctrine statement

C01 is the constitutional grammar layer for Batch C records.

It is not a convenience page.
It is not a formatting note.
It is not a hidden actor or mission file.

Its purpose is to ensure that every later Batch C schema speaks the same structural language, preserves authority hierarchy, remains auditable under corpus-scale donor pressure, and can support later conversion, consolidation, retrieval, revision tracking, and bundle stability without collapsing into incompatible handcrafted content objects.

