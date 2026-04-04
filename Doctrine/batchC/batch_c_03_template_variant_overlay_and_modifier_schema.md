# batchC_03_template_variant_overlay_and_modifier_schema.md

## Purpose and authority

This file is the **overlay-content family schema authority** for Batch C.

Its job is to define the Astra-native schema for overlays, templates, variants, and modifier records that alter existing content entries without automatically becoming new atomic records. It is the family file that turns the common record grammar from C01 into a reusable overlay schema that can survive large donor pressure without collapsing into a second actor file, second item file, or a generic garbage chute for “anything changed.”

C03 is not a second actor schema. It is not a second item schema. It is not a second site-state system. It is not an encounter packet. It is not a mission wrapper. It is not a faction convenience blob. It is not a local scenario note pretending to be doctrine.

It owns:
- overlay-content record structure
- overlay doctrine for Batch C
- overlay-specific payload blocks on top of C01
- modification-state doctrine and routing classes
- overlay schema / record / application / host-state distinction
- host-target doctrine
- target eligibility and host-readiness doctrine
- overlay locality doctrine
- overlay payload-family grammar
- overlay application model
- stacking, exclusivity, and precedence doctrine
- overlay chain auditability doctrine
- host-identity preservation doctrine
- overlay promotion, demotion, and derivative-escalation doctrine
- overlay lifecycle and revision doctrine
- overlay-side host-readiness and intake doctrine
- container and bundle interaction doctrine for overlays
- overlay output posture doctrine
- overlay-specific anti-collapse rules
- minimal abstract overlay template

It does **not** own:
- full actor-content payloads already owned by C02
- item/resource/asset payloads already owned by C04
- frame payloads already owned by C05
- site payloads already owned by C06
- faction payloads already owned by C07
- challenge-object payloads already owned by C08
- encounter composition already owned by C09
- mission/scenario composition already owned by C10
- reward-parcel doctrine already owned by C11 and B16
- donor conversion instances as doctrine
- live-play presentation behavior

## Why this file exists

Large donor corpora repeatedly express lawful variation through templates, status overlays, role packages, elite upgrades, corruption states, faction skins, biome conditioning, mounted forms, summoned states, advanced forms, and other recurring modifier structures.

Those constructs are neither:
- full atomic records in their own right,
- merely casual prose notes,
- nor always derivative new identities.

C03 exists because Astra requires a lawful overlay family that can:
- modify hosts without re-owning host identity,
- target different host classes without becoming freeform prose,
- support repeatable modifier patterns across many donors,
- distinguish reusable overlay doctrine from application events and resulting host states,
- and escalate correctly when a modifier has ceased to be an overlay and should become a derivative record, composition concern, or purely local override.

This file therefore treats the family center as **reusable modification with host identity preservation**, not as donor labels like template, elite form, corruption state, or variant block.

## Scope boundaries and exclusions

C03 covers modifier records whose dominant doctrinal function is to alter an existing host record or class of host records while preserving host authority unless derivative threshold is crossed.

That includes, where they remain overlays rather than derivatives or compositions:
- elite and weak forms
- corruption or contamination overlays
- rank or tier variants
- faction or institution skins
- mounted or paired-state overlays
- summoned-state overlays
- emitted-state overlays
- environmental conditioning overlays
- advanced-form overlays
- role or package overlays
- conditionally active variant layers
- context-bound modifier structures with lawful overlay-like behavior

C03 excludes:
- full host records that now carry independent identity -> route to the correct atomic family
- composition packets made from multiple records -> C09 or C10
- mission-local prose exceptions that do not warrant reusable structure -> local override under C01/C09/C10 handling
- host payload redefinitions that belong to the host family itself -> C02/C04/C05/C06/C07/C08 as appropriate
- container-only grouping behavior that does not actually modify a host -> C13

## Overlay doctrine

An **overlay record** is a content record whose primary job is to alter the interpretation, state, applicability, access, relationships, capability expression, ingress/egress posture, lifecycle state, or similar structural aspects of another record or host class while preserving the host’s underlying authority and identity unless derivative threshold is crossed.

An overlay may:
- add,
- suppress,
- condition,
- restyle,
- shift,
- gate,
- qualify,
- or temporarily reinterpret host content.

An overlay does **not** automatically become a new host record merely because it changes something important.

An overlay also does **not** own the host. The host remains authoritative unless derivative escalation is triggered.

## Overlay schema, record, application, and host-state distinction

C03 must distinguish four different doctrinal objects that donor material often blurs together:

1. **overlay schema** — the reusable structural doctrine for a kind of overlay
2. **overlay record** — a concrete overlay entry using that schema
3. **overlay application** — the attachment, emission, inheritance, or application event by which the overlay affects a host
4. **overlay-bearing host state** — the resulting host condition after one or more overlays are applied

These are not the same thing.

A reusable corruption overlay, a specific corruption record, a mission step that applies it, and the corrupted host state are doctrinally different objects and should not be silently collapsed into one record or one prose note.

C03 owns the overlay schema and overlay record side directly, and it provides the grammar by which overlay applications and overlay-bearing host states remain distinguishable from them.

## Modification states and routing classes

C03 must distinguish overlay-like modification states more precisely than “overlay versus derivative.”

### Core modification states

An overlay record or overlay-like modifier should route into one of these primary modification states:
- `local_temporary_override`
- `reusable_overlay_schema`
- `host_bound_overlay_instance`
- `source_emitted_overlay`
- `container_facing_contextual_modifier`
- `derivative_rebuild`

### Modification-state guidance

- **local_temporary_override**: a one-off, local, context-bound modification not yet promoted into reusable overlay doctrine.
- **reusable_overlay_schema**: a reusable overlay structure intended for repeated application across multiple hosts or recurring cases.
- **host_bound_overlay_instance**: a concrete applied overlay instance tied to one host or one pinned host revision.
- **source_emitted_overlay**: an overlay generated, emitted, granted, or imposed by another record, process, or state.
- **container_facing_contextual_modifier**: an overlay-like modifier that primarily operates within a mission, scenario, region, packet, or bundle context and should not automatically be generalized into a host-wide reusable overlay.
- **derivative_rebuild**: a former modifier case whose changes now exceed overlay logic and require a new derivative identity.

### Routing doctrine

Not every modification-worthy construct should become a reusable overlay.

C03 exists partly to stop three different things from being blurred together:
- a mission-local elite version,
- a reusable elite template,
- and an advanced-form host that really should be its own derivative record.

## Host-target doctrine

C03 must not merely say overlays can target actors, items, frames, sites, factions, and challenge objects. It must define **how** targeting is declared.

### Host classes

Overlay targets may include:
- actors
- items/assets
- frames/platforms
- sites/locales
- factions/institutions
- challenge objects
- selected composition records only when later doctrine explicitly allows it

### Target-declaration classes

Overlay target declarations should support:
- `concrete_record_target`
- `schema_family_target`
- `trait_matching_target`
- `context_matching_target`
- `host_class_target`

### Target-declaration guidance

- **concrete_record_target**: applies to one specific host record.
- **schema_family_target**: applies to hosts belonging to a declared schema family.
- **trait_matching_target**: applies to hosts matching declared tags, traits, or structural conditions.
- **context_matching_target**: applies when the host is in a declared environment, mission state, region, faction context, or comparable situational condition.
- **host_class_target**: applies to a broad class such as actor, item, frame, site, or faction.

This allows lawful handling of donor patterns such as:
- apply to undead
- apply to armored targets
- apply to operatives of this faction
- apply to hosts in this region
- apply to any summoned being

## Target eligibility and host-readiness doctrine

Allowed or restricted host class is not by itself precise enough for corpus-scale overlay handling.

### Eligibility distinction

Astra must distinguish at least four target-eligibility states:
- `structurally_eligible`
- `conditionally_eligible`
- `unstable_but_possible`
- `prohibited`

### Eligibility doctrine

- **structurally_eligible** means the host type is a normal lawful target.
- **conditionally_eligible** means the overlay may apply only when declared conditions are satisfied.
- **unstable_but_possible** means application is not forbidden, but the host may be fragile, unsafe, or likely to require special handling.
- **prohibited** means the overlay should not apply to that host class or target condition.

Eligible is not the same as safe, and safe is not the same as normative. A host may technically accept an overlay while still being unstable under it, legally disallowed from it, or unsuitable as a normal application target.

## Host-facing versus container-facing overlays

Most overlays are **host-facing**: they modify a host directly.

Some donor constructs, however, behave more like **container-facing overlays**: they primarily modify how a host functions within a mission, scenario, region, packet, or bundle context.

### Distinction doctrine

- **host-facing overlays** are intended to travel with or target hosts directly.
- **container-facing overlays** are primarily contextual and should not automatically become general reusable overlays.

This distinction exists so Astra does not promote every temporary scenario condition into permanent overlay doctrine.

### Container-facing scope classes

Container-facing contextual modifiers should support finer scope classes such as:
- `packet_scoped`
- `mission_scoped`
- `region_scoped`
- `sourcebook_bundle_scoped`
- `anthology_scoped`

These scopes should not be flattened into one vague contextual category because their promotion, reuse, and pinning expectations are different.

## Overlay locality doctrine

Overlay temporality alone is not enough. Astra also needs locality.

### Locality classes

Overlay records should support locality classes such as:
- `host_local`
- `scene_local`
- `encounter_local`
- `mission_local`
- `site_local`
- `region_local`
- `bundle_local`
- `canon_wide_reusable`

### Locality doctrine

A mission-local elite state is not the same as a site-conditioned hostility overlay or a region-wide corruption layer. Locality should therefore be declared explicitly rather than inferred indirectly from context matching, persistence, or application class alone.

## Host-identity preservation doctrine

This is the core of C03.

An overlay may alter:
- interpretation,
- state,
- applicability,
- access,
- outputs,
- posture,
- capability expression,
- or relationship structure.

It does **not** own host identity.

The host remains authoritative unless derivative threshold is crossed.

### Derivative-threshold triggers

A modifier should be reviewed for promotion into a derivative record when one or more of the following become true:
- the modified form now requires independent reuse
- the modified form now has stable continuity apart from the base host
- the overlay now carries most of the relevant content payload
- the modified form must coexist with the base as a peer record
- the overlay chain becomes identity-bearing rather than optional
- the modified form can no longer be adequately understood as “host plus modifier”

If those conditions are met, C03 should say **promote to derivative**, not **keep layering**.

## Overlay payload families

C03 should not treat elite, corrupted, faction variant, mounted, or summoned-state overlays as isolated named mini-systems. It should normalize them into compositional payload families.

### Core overlay payload families

Overlay records may declare one or more payload families such as:
- `scalar_modulation`
- `tag_or_trait_modulation`
- `access_or_legality_modulation`
- `capability_attachment_or_suppression`
- `loadout_or_profile_modulation`
- `relationship_modulation`
- `ingress_or_egress_modulation`
- `lifecycle_or_state_modulation`
- `environmental_conditioning`
- `faction_or_institution_skinning`
- `mount_or_pairing_linkage`
- `emitted_or_summoned_state_modulation`
- `transformation_or_advanced_form_modulation`

### Payload-family doctrine

These families are structural, not flavor-only.

They exist so recurring donor patterns resolve through shared payload grammar rather than each becoming a local special case.

### Payload-family ownership note

Payload families declare **what category of change is being made**, not the governing meaning of that category.

For example:
- `access_or_legality_modulation` may alter access posture, but does not own legality doctrine
- `lifecycle_or_state_modulation` may alter host state posture, but does not own host survivability doctrine or site lifecycle doctrine
- `relationship_modulation` may alter host relationships, but does not redefine relationship grammar
- `capability_attachment_or_suppression` may affect capability expression, but does not own A07 or host-family payload doctrine

This distinction is intentionally repetitive because it prevents C03 from mutating into second copies of the host families it modifies.

## Overlay application model

C03 must define how overlays attach and what kind of attachment they are.

### Application classes

Overlay records should support application classes such as:
- `direct_attached_overlay`
- `conditionally_active_overlay`
- `emitted_overlay`
- `inherited_overlay`
- `container_applied_overlay`
- `local_override_application`

### Application guidance

- **direct_attached_overlay**: attached directly to the host.
- **conditionally_active_overlay**: present but only active when declared conditions are met.
- **emitted_overlay**: imposed by another source, state, or process.
- **inherited_overlay**: carried forward from another record, source state, or lineage of application.
- **container_applied_overlay**: applied through a mission, scenario, bundle, packet, or container context.
- **local_override_application**: a non-generalized local modification using overlay-like handling.

## Activation, persistence, suppression, and removal doctrine

Overlays must declare not only how they attach, but how they behave over time.

### Activation and persistence fields

Overlay records should support:
- `activation_mode`
- `persistence_class`
- `suppression_state`
- `removal_mode`
- `reversibility_profile`

### Useful activation and persistence values

Examples include:
- always_on
- trigger_bound
- scene_bound
- encounter_bound
- mission_bound
- persistent
- suppressed
- exhausted
- consumed
- detached
- reversible
- irreversible

These are not local mechanics in themselves. They are overlay-state doctrine that later host and container use can reference lawfully.

## Stacking, exclusivity, and precedence doctrine

C03 must define how overlays interact with one another.

### Overlay conflict-model fields

Overlay records should support:
- `stackability`
- `mutually_exclusive_families`
- `application_order_mode`
- `precedence_level`
- `derivative_threshold_risk`

### Conflict-model guidance

- `stackability` answers whether the overlay can stack with peers.
- `mutually_exclusive_families` identifies overlay classes that cannot lawfully coexist.
- `application_order_mode` distinguishes ordered versus unordered application.
- `precedence_level` clarifies which overlay governs in conflict.
- `derivative_threshold_risk` signals whether repeated composition is likely to force derivative escalation.

This is especially important for chains such as:
elite + faction skin + corruption + mounted + environment-conditioned + summoned-state.

Astra should not wait until later to decide whether those compose lawfully.

### Identity-bearing risk classes

`derivative_threshold_risk` should not remain vague. Useful risk classes include:
- `low_risk`
- `moderate_risk`
- `high_risk`
- `identity_bearing_by_default`

The last class is especially important for donor constructs that look like overlays on the surface but frequently become new records in practice, such as permanent ascensions, corrupted evolutions, stable transformed mounts, or advanced forms with durable continuity.

## Overlay chain auditability doctrine

At corpus scale, one overlay is rarely the problem. The problem is accumulated overlay stacks whose origin and precedence become opaque.

### Chain-audit doctrine

Overlay-capable systems should preserve chain intelligibility. At minimum, Astra should be able to report:
- active overlays
- suppressed overlays
- historical overlays when pinned or historically relevant
- emitted or inherited overlays
- context-only overlays
- overlay order or precedence interpretation

This does not require a giant new subsystem. It requires that C03 reserve lawful audit grammar for overlay chains rather than forcing that logic into prose later.

## Overlay lifecycle and revision doctrine

Overlays need their own lifecycle treatment parallel to hosts.

### Overlay lifecycle classes

Overlay records should support distinctions such as:
- `overlay_schema`
- `overlay_record`
- `overlay_application`
- `overlay_bearing_host_state`
- `deprecated_overlay`
- `superseded_overlay`
- `pinned_overlay_revision`

### Lifecycle doctrine

An overlay may evolve independently from its hosts.

Examples:
- a faction skin may be revised,
- a corruption layer may be deprecated,
- a mission-local modifier may be promoted into a reusable overlay,
- a canon overlay may supersede an older converted one.

C03 must specialize C01’s revision grammar enough that overlay history remains intelligible.

## Promotion, demotion, and derivative-escalation doctrine

C03 must govern not only escalation upward to derivative identity, but also movement between contextual and reusable overlay status.

### Promotion and demotion rules

- repeated local override behavior may justify promotion into reusable overlay schema
- reusable overlay behavior that never stabilizes outside one context may be reconsidered as contextual modifier rather than permanent overlay doctrine
- overlay chains that become identity-bearing should escalate to derivative review
- derivative records must never be silently reduced back to overlay status without explicit review

This gives Astra both directions of motion rather than treating overlay status as a one-way ratchet.

## Host-overlay relationship grammar

C03 inherits C01 relationship grammar and should normalize a core overlay-side relationship set.

### Core overlay relationship verbs

Overlay records should be prepared to use relationship forms such as:
- `overlays`
- `modifies`
- `emitted_by`
- `applied_to`
- `suppressed_by`
- `incompatible_with`
- `supersedes`
- `variant_of`
- `pinned_in`

These relationship forms should be represented through C01 relationship structure, not buried in prose.

## Container and bundle interaction doctrine

Overlay behavior inside containers must be explicit.

### Container interaction rules

1. A bundle may pin a host and an overlay together without making that pair a new atomic record.
2. A mission packet may locally apply an overlay without automatically promoting it into reusable overlay doctrine.
3. A canon anthology may include the same host with different overlay states in different contexts.
4. A converted sourcebook may preserve donor-local overlay behavior that later canon declines to generalize.
5. A pinned host-overlay pairing should preserve both host revision identity and overlay revision identity.

C03 must support those distinctions so bundle history does not mutate silently and local variants are not promoted accidentally.

## Selected composition targets note

Selected composition records may be legal overlay targets only when later doctrine explicitly stabilizes that relationship.

Even then, composition-target overlays should usually be treated as exceptional and should ordinarily be container-facing rather than host-facing unless a later family file explicitly says otherwise.

This rule exists to keep C03 from smuggling composition logic into the overlay family by convenience.

## Host-readiness and overlay-intake doctrine

Not every host should accept overlays in the same way.

### Host-readiness fields

Overlay records should support:
- `expected_host_readiness`
- `overlay_intake_requirements`
- `fragility_or_resistance_profile`
- `allowed_host_classes`
- `restricted_host_classes`

### Host-readiness doctrine

Some hosts should accept overlays easily.
Some should be fragile.
Some should only accept particular overlay families.

This matters especially for frames, sites, and challenge objects, which often should not accept the same overlay families as actors or items.

C03 defines the overlay-side half of that relationship. Host families may define the host-side intake half.

## Overlay output posture

Some overlays change only current state. Others also change outputs.

### Output-posture fields

Overlay records should support:
- `output_modulation_posture`
- `output_presence_profile`
- `affected_output_classes`
- `output_type_profile`
- `output_timing_shift_profile`
- `output_conditionality_profile`

### Output-posture doctrine

Examples:
- a corruption overlay may alter salvage, social fallout, faction reaction, or emitted hazards
- a mounted overlay may change ingress/egress and defeat outputs
- a summoned-state overlay may change what remains after dissipation

C03 does not own downstream reward, fallout, or inflow systems. It gives overlays a lawful way to declare whether they can alter host outputs, whether outputs are added or suppressed, what output classes are affected, when those effects occur, and whether that modulation is conditional on particular host states or resolutions.

## Required lower-doctrine handoffs

C03 must hand off to lower doctrine rather than rewriting it.

At minimum, overlay entries should compose or reference:
- `C01` common record grammar
- the appropriate host family file such as `C02`, `C04`, `C05`, `C06`, `C07`, or `C08`
- `A16` translation pattern library and edge-case discipline where relevant
- `B02` survivability doctrine when overlays alter survivability-facing posture
- `B10` and `B12` when overlays alter social leverage, legitimacy, or access-facing posture
- `B14` when overlays alter frame-facing operation posture
- `B15` when overlays alter civic or site-service posture
- `B16` when overlays alter post-pressure outputs

C03 may define overlay-entry interface slots for these effects. It may not restate the governing doctrine as if C03 owns it.

## Anti-collapse rules specific to overlays

C03 must not:
- restate the full host payload locally
- become a second actor file, second item file, second site-state system, or second faction-state system
- smuggle encounter composition into itself
- treat repeated mission-local variants as reusable doctrine without review
- treat overlay chains as permanent identity by local convenience
- replace derivative escalation with ever-thicker overlay layering
- promote every contextual modifier into the permanent overlay family
- redefine host identity merely because a modifier is interesting

### Review-trigger rules

The following patterns should trigger review rather than silent continuation:
- repeated mission-local variants -> review for overlay promotion
- repeated reusable overlays that become identity-bearing -> review for derivative escalation
- overlay chains that now carry most of the content payload -> review for derivative escalation
- container-facing modifiers reused across many containers -> review for reusable overlay or schema escalation

### Declaration-over-duplication rule

If an overlay can declare a host-facing modulation through payload families, relationships, intake rules, and state posture, it should do that rather than restating the altered host payload as though it were a full host record.

This is one of the main anti-bloat rules for C03.

These rules are intentionally boring. They exist to keep C03 from bloating later.

## Reserved split note

Do not split C03 now.

If later corpus pressure proves the file genuinely unwieldy, the preferred reserved split pattern would be:
- `C03a_overlay_core_and_modification_state_schema`
- `C03b_host_targeting_and_application_schema`
- `C03c_overlay_payload_and_conflict_schema`

That split is reserved, not active.

## Minimal abstract overlay template

The following template extends the C01 grammar with overlay-family payload blocks. It is a family abstract template, not a converted instance.

```yaml
record:
  identity:
    canonical_id: ""
    record_name: ""
    display_name: ""
    record_class: "overlay_record"
    family_owner: "C03"
    alias_set: []
    visibility_stratum: ""
    field_visibility_overrides: []

  classification:
    ontology_state: "instantiated_record"
    lifecycle_state: "draft"
    dominant_function: "overlay_content"
    secondary_functions: []
    content_family: "overlay"

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
    primary_owner: "C03"
    secondary_dependencies: []
    authority_rank: "family_schema"
    governing_files: ["C01", "C03"]
    forbidden_owner_drift: []
    escalation_flags: []

  dependencies:
    structural_dependencies: ["C01"]
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
    family_tags: ["overlay"]
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

  overlay_profile:
    modification_state: ""
    overlay_payload_families: []
    host_facing_or_container_facing: ""
    overlay_locality_class: ""
    host_authority_note: ""
    host_identity_preservation_status: ""
    derivative_threshold_notes: []

  target_declaration:
    target_declaration_class: ""
    target_resolution_notes: []
    concrete_target_ids: []
    schema_family_targets: []
    trait_matching_targets: []
    context_matching_targets: []
    host_class_targets: []
    allowed_host_classes: []
    restricted_host_classes: []
    target_eligibility_profile: ""

  application_model:
    application_class: ""
    activation_mode: ""
    persistence_class: ""
    suppression_state: ""
    removal_mode: ""
    reversibility_profile: ""
    source_emission_links: []

  compatibility_and_conflict:
    stackability: ""
    mutually_exclusive_families: []
    application_order_mode: ""
    precedence_level: ""
    derivative_threshold_risk: ""
    expected_host_readiness: ""
    overlay_intake_requirements: []
    fragility_or_resistance_profile: ""

  chain_audit:
    active_overlay_reporting_mode: ""
    suppressed_overlay_reporting_mode: ""
    historical_overlay_reporting_mode: ""
    inherited_overlay_reporting_mode: ""
    context_only_overlay_reporting_mode: ""
    precedence_reporting_mode: ""

  output_posture:
    output_modulation_posture: ""
    output_presence_profile: ""
    affected_output_classes: []
    output_type_profile: ""
    output_timing_shift_profile: ""
    output_conditionality_profile: ""

  container_behavior:
    pinning_behavior: ""
    local_application_behavior: ""
    contextual_scope_class: ""
    bundle_pairing_rules: []
    contextual_modifier_notes: []
```

## Final doctrine statement

C03 is the overlay-family constitutional schema for Batch C.

It does not turn every modification into a new record.
It does not let every temporary condition become permanent overlay doctrine.
It does not let overlays quietly replace host identity.
It does not become a second copy of the host families it modifies.

Its purpose is to let Astra represent reusable modifier structures lawfully across a mixed donor corpus while preserving host authority, derivative escalation discipline, container stability, auditability, and cross-file interoperability.

