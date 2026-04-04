# batchC_04_item_relic_resource_and_asset_content_schema.md

## Purpose and authority

This file is the **item/resource/asset-content family schema authority** for Batch C.

Its job is to define the Astra-native entry structure for atomic non-actor content objects: gear, relics, consumables, resources, crafting inputs, natural treasures, economic assets, and item-based exceptional content. It is the family file that turns the common record grammar from C01 into a reusable item-family schema that can survive mixed donor pressure at corpus scale without collapsing into a gear chapter, stealth economy chapter, frame-module file, or reward-parcel system.

C04 is not an equipment procedure file. It is not a shopping chapter. It is not a crafting-flow file. It is not a legality-enforcement file. It is not a reward-parcel file. It is not a frame-subsystem family by default.

It owns:
- item/resource/asset-content record structure
- itemhood and assethood doctrine for Batch C
- item-family payload blocks on top of C01
- item-mode and routing-class doctrine
- resource-versus-asset distinction inside the item family
- form, embodiment, and custody posture fields
- use, depletion, persistence, and item-state doctrine
- host-interface and compatibility doctrine for item-family records
- value, claim, exchange, legality, and permission hooks at entry-shape level
- processing, activation, salvage, transformation, and transitional-content posture fields
- transferability and portability doctrine for item-family records
- institutional-recognition dependence hooks for asset-facing entries
- item-specific derivative-threshold and boundary-control doctrine
- item-family relationship expectations
- item-family anti-collapse rules
- minimal abstract item/resource/asset template

It does **not** own:
- item/equipment procedure doctrine already owned by B03
- value/exchange procedure doctrine already owned by B04
- crafting/repair/requisition procedure doctrine already owned by B05
- overlay/template doctrine already owned by C03
- frame/platform entry structure already owned by C05
- faction/institution entry structure already owned by C07
- reward parcel packaging already owned by C11
- live-play presentation behavior
- donor conversion instances as doctrine

## Why this file exists

Large donor corpora do not present item-family content as one uniform category. Some donors pressure toward ordinary held gear. Others pressure toward installed components, bonded relics, abstract spendable resources, harvested monster inputs, legal permits, service rights, trade assets, account-backed holdings, or claim-bearing titles.

Those constructs are neither:
- all simple objects,
- all abstract currencies,
- nor all reducible to player equipment.

C04 exists because Astra requires one lawful family schema for atomic non-actor content entries that can:
- distinguish objects, resources, assets, and inputs without splitting too early,
- preserve host-interface and custody differences,
- expose legality/value/crafting hooks without re-owning Batch B procedure doctrine,
- distinguish ready-use content from transitional content,
- and route correctly when a content object is actually an overlay, frame subsystem, organizational permission structure, or packaged reward parcel.

This file therefore treats the family center as **itemhood and assethood**, not as donor labels like equipment, treasure, cyberware, warrant, reagent, or relic.

## Scope boundaries and exclusions

C04 covers content entries whose dominant doctrinal function is to exist as an atomic non-actor object, resource, component, claim-bearing asset, or item-centered content unit that can be possessed, carried, worn, installed, embedded, consumed, spent, transformed, traded, claimed, bonded, processed, or otherwise handled as an item-family record.

That includes, where they remain item-family content rather than overlays, frames, institutions, or parcels:
- held gear
- worn gear
- consumables
- relics and artifacts
- reagents and abstract spendable resources
- crafting inputs and refined components
- harvested organic or occult materials
- natural treasures
- embedded or installable components
- licenses, permits, warrants, claim tokens, and comparable asset-like records when they are treated as atomic entries
- service-enabling or access-enabling tokens when handled as item-family records
- facility or infrastructure support assets when treated as atomic entries
- item-based exceptional content

C04 excludes:
- pure modifier layers or templates that primarily alter another host -> C03
- full frame/platform records -> C05
- institutional offices, organizations, or polity records -> C07
- packaged reward/parcels and post-pressure bundles -> C11
- procedural value/exchange logic -> B04
- procedural equipment-use logic -> B03
- procedural crafting/repair/requisition logic -> B05

## Itemhood and assethood doctrine

An **item-family record** is a content record whose primary job is to represent an atomic non-actor object, resource, component, claim-bearing asset, or item-centered entry that can participate in possession, custody, use, consumption, installation, valuation, exchange, processing, salvage, or transformation while remaining a reusable content object.

Itemhood does not require hand-held physicality.

Item-family records may include:
- discrete physical objects
- stackable object units
- consumables
- bonded or attuned objects
- installed or embedded components
- abstract spendable resources
- claim-bearing assets
- permission-bearing assets
- service-bearing assets
- harvested inputs
- processed components
- exceptional relics or artifacts

Itemhood is established by dominant function, not by donor naming convention.

### Resource-versus-asset distinction

C04 must distinguish **resource records** from **asset records** even though both remain inside the same item family.

- A **resource** is primarily a spendable, convertible, stackable, processable, or transformation-facing value/input state.
- An **asset** is primarily a claim, right, entitlement, title, durable support relation, recognized holding, or institution-facing value-bearing object.

These are not identical merely because both may have value.

A reagent pool, salvage mass, inventory reserve, credit bundle, teleporter warrant, deed, service right, and bonded permit token do not all behave the same way. C04 therefore keeps them in one family while requiring that the distinction remain explicit.

## Item modes and routing classes

C04 must support different item-family modes without splitting them into unrelated families.

### Core item modes

An item-family record may declare one or more item modes, with one marked primary where needed:
- `discrete_object`
- `stackable_object`
- `consumable_object`
- `bonded_or_attuned_object`
- `embedded_or_installable_component`
- `abstract_spendable_resource`
- `economic_or_claim_bearing_asset`
- `harvested_input`
- `processed_crafting_component`
- `exceptional_relic_or_artifact`
- `service_enabling_token_or_permit`
- `facility_or_infrastructure_support_asset`

`economic_or_claim_bearing_asset` is a primary item mode. The more specific asset subclasses later in this file are secondary sub-classifications inside that asset-facing side of the family rather than competing primary modes.

### Mode guidance

- **discrete_object**: a bounded object entry with ordinary item identity.
- **stackable_object**: a bounded object entry whose normal handling expects quantity bundling.
- **consumable_object**: an item principally defined by spend, use, depletion, or single-cycle activation.
- **bonded_or_attuned_object**: an object whose use, custody, transfer, or potency depends on bond, attunement, or keyed relationship.
- **embedded_or_installable_component**: an item record that interfaces with a host body, frame, weapon, site-service channel, or comparable host.
- **abstract_spendable_resource**: a resource-facing item-family record that is not best modeled as a single physical object instance.
- **economic_or_claim_bearing_asset**: an item-family record that materially represents value, claim, entitlement, title, or exchange-backed holding.
- **harvested_input**: a raw recovered input obtained from creatures, locales, relic sites, or comparable sources.
- **processed_crafting_component**: a refined or intermediate component intended for later repair, construction, infusion, or similar use.
- **exceptional_relic_or_artifact**: a significance-bearing item-family record with exceptional continuity, activation, or derivative pressure.
- **service_enabling_token_or_permit**: an atomic record that enables access, service use, authorization, or permit-bearing activity while still functioning as item-family content.
- **facility_or_infrastructure_support_asset**: a support-facing item-family record that serves logistical, operational, or infrastructure contexts without becoming a site or institution in its own right.

## Not all item-family content is character inventory

This file must not drift back into a donor-shaped assumption that all item-family content is character inventory content.

Some item-family records are carried or equipped.
Others are harvested, stored, registered, installed, escrowed, site-held, institution-recognized, or kept as abstract reserves, claims, or support assets.

Industrial stock, institutional warrants, field supplies, salvage lots, natural treasures, repair materials, mission-locked access objects, and comparable entries remain fully within C04 even when they are not best represented as personal inventory objects.

## Form, embodiment, and custody doctrine

C04 must distinguish what an item **is like**, where it **resides**, and how it is **held or controlled**.

### Form and embodiment fields

Item-family records should support:
- `form_factor`
- `embodiment_profile`
- `host_dependence_profile`
- `portability_profile`

### Custody and holding fields

Item-family records should support:
- `custody_posture`
- `access_posture`
- `removability_profile`
- `claim_lock_profile`

### Custody, access, and claim-lock distinction

- `custody_posture` answers who presently holds, stores, controls, or physically/administratively possesses the entry.
- `access_posture` answers who may lawfully use, invoke, activate, redeem, or benefit from it.
- `claim_lock_profile` answers what ownership, recognition, legal, bond, or assignment constraints prevent free reassignment or ordinary use.

These fields are related but should not be collapsed into one possession concept.

### Useful embodiment and custody classes

Useful categories may include:
- held
- worn
- implanted
- installed
- bonded
- socketed
- stored
- stowed
- account_backed
- leased
- escrowed
- site_anchored
- faction_issued
- claim_held
- abstractly_reserved

### Doctrine note

A bonded relic, an implanted deck, a tradable warrant, and a reagent bundle are not merely different “forms.” They differ in portability, removability, host dependence, claim logic, and transfer behavior. Those distinctions must therefore remain explicit rather than being flattened into a single possession bucket.

## Use, depletion, persistence, and lifecycle doctrine

C04 must support more than a binary usable/unusable distinction.

### Use and depletion fields

Item-family records should support:
- `use_profile`
- `depletion_profile`
- `persistence_class`
- `recovery_or_refresh_profile`
- `post_use_state_shift`

### Item-state and lifecycle fields

Item-family records should support:
- `item_state_profile`
- `integrity_state`
- `activation_state`
- `claim_state`
- `processing_state`
- `state_typing_profile`

### Useful state classes

Useful states may include:
- pristine
- damaged
- broken
- inert
- charged
- depleted
- exhausted
- consumed
- dormant
- awakened
- compromised
- counterfeit
- claimed
- contested
- voided
- stabilized_for_processing
- partially_recovered

### State-typing doctrine

Not all states belong to the same doctrinal family.

C04 should be able to distinguish whether a state is primarily:
- physical or integrity-facing
- energetic or activation-facing
- legal or claim-facing
- processing-facing
- authentication-facing
- transfer-facing

This prevents states such as `broken`, `charged`, `voided`, `counterfeit`, `claimed`, and `stabilized_for_processing` from being treated as though they were one homogeneous state set.

### Lifecycle doctrine

Item-family records may persist, be spent, be partially depleted, be recoverable, transform into downstream entries, or lose value/state without ceasing to be relevant. C04 therefore needs lifecycle/state grammar broad enough for relics, salvageables, embedded tech, permits, claim-tokens, and transformation inputs.

## Host-interface and compatibility doctrine

This is one of the most important C04 ownership zones.

Many item-family entries are not merely “owned.” They interface with hosts, sockets, body slots, frame channels, weapon channels, ritual receptacles, site services, or institutional access layers.

### Host-interface fields

Item-family records should support:
- `valid_host_classes`
- `required_interface_class`
- `slot_or_channel_usage`
- `install_or_removal_class`
- `attachment_permanence`
- `host_dependency_threshold`
- `exclusivity_limits`
- `compatibility_notes`

### Interface doctrine note

A frame-mounted module, cyber implant, body-slot item, weapon mod, bonded gem, ritual focus, faction permit, and summoned control token all interface differently. C04 must preserve that difference structurally without absorbing frame, body, or institutional doctrine.

### Host-interface versus host-dependence note

- `required_interface_class`, `slot_or_channel_usage`, and related interface fields answer how the entry connects to a host or channel.
- `host_dependence_profile` and later host-dependent identity-risk fields answer how much the entry’s identity, function, or continuity depends on remaining attached to that host.

A thing may interface with a host without depending on that host for identity. Conversely, it may become so host-dependent that derivative or rerouting pressure appears.

### Overlay-versus-item threshold note

When a thing’s primary content identity is **an object or asset that can exist independently**, it remains in C04 even if donors call it a mod, upgrade, attachment, implant, or keyed module.

When a thing’s primary content identity is **a reusable alteration layer applied to a host**, it should route pressure to C03 even if donors present it as a piece of gear.

This distinction should be enforced aggressively. It is one of the highest-friction seams in large mixed donor corpora.

### Boundary-control note

If the content is best understood as:
- a reusable alteration layer -> route pressure to C03
- a frame/platform subsystem whose dominant identity is platform definition -> route pressure to C05
- an organizational office or authority state -> route pressure to C07/B12
- a packaged reward/output bundle -> route pressure to C11/B16

C04 must make those routing pressures visible rather than silently absorbing them.

## Value, claim, exchange, legality, and permission hooks

C04 does not own value/exchange or legality procedure. It does need strong entry-shape hooks for them.

### Value and claim fields

Item-family records should support:
- `value_expression_profile`
- `exchange_posture`
- `claim_profile`
- `permission_profile`
- `legal_or_regulatory_hooks`
- `institutional_recognition_hooks`
- `recognition_dependence_profile`

### Economic asset subclasses

Economic and asset-facing item records should distinguish at least:
- `exchange_media`
- `claim_bearing_asset`
- `permission_bearing_asset`
- `service_bearing_asset`

### Recognition-dependence doctrine

Some assets are meaningful only because an institution recognizes them.
Others remain materially valid even when recognition is absent, delayed, contested, or lost.

C04 should therefore allow records to declare whether institutional recognition is:
- constitutive
- enabling
- optional
- contested
- absent

C04 does not own enforcement. It does need to expose whether recognition is what makes the asset meaningful in the first place.

### Doctrine note

A trade bar, a land claim, a teleporter warrant, and a bonded service right all belong to the broad asset family, but they do not do the same doctrinal job. C04 should distinguish them at the entry-shape level while still handing off actual exchange, enforcement, or institutional procedure to B04 and B12.

## Processing, activation, salvage, and transformation doctrine

Not every item-family record is ready to use on acquisition.

### Processing and readiness fields

Item-family records should support:
- `processing_posture`
- `activation_or_processing_requirements`
- `salvage_or_refinement_hooks`
- `crafting_or_transformation_hooks`
- `authentication_or_registration_hooks`
- `authentication_posture`
- `ritual_or_special_activation_hooks`
- `content_readiness_profile`

### Transitional-content doctrine

C04 must distinguish ready-use content, ready-claim content, and ready-process content rather than flattening all readiness into one state.

- **ready-use content** is primarily acquired in order to be used, equipped, spent, activated, or invoked directly.
- **ready-claim content** is primarily acquired in order to be recognized, registered, redeemed, validated, assigned, or otherwise made operatively meaningful through claim or authorization posture.
- **ready-process content** is primarily acquired in order to become something else through refinement, validation, registration, ritual, crafting, decryption, salvage processing, or other conversion posture.

This distinction matters for harvested inputs, processed components, warrants pending validation, ritual catalysts, dormant relics, unstable salvage, permits awaiting registration, and comparable entries that are structurally about becoming later outputs or rights.

### Doctrine note

Some records are ready-to-use. Others only become useful after refinement, crafting, ritual activation, decryption, authentication, sanctification, disassembly, legal registration, or equivalent processing. C04 must expose that distinction directly.

## Transferability and portability doctrine

At corpus scale, one of the most common pressures will be whether a thing is transferable at all, and under what conditions.

### Transferability fields

Item-family records should support:
- `transferability_profile`
- `transfer_requirements`
- `value_preservation_on_transfer`
- `identity_preservation_on_transfer`
- `transfer_routing_pressure_notes`

### Useful transferability classes

Useful classes may include:
- freely_transferable
- physically_transferable_but_claim_locked
- legally_transferable_only
- non_transferable
- transferable_only_by_extraction_or_removal
- transferable_only_by_organizational_action
- transfer_degrades_value
- transfer_preserves_value

### Transferability doctrine

Transfer is not merely a value issue.
It is also a custody, embodiment, host-interface, institutional-recognition, identity-continuity, and functional-continuity issue.

- `identity_preservation_on_transfer` answers whether the entry remains recognizably the same record-object after transfer.
- `functional_continuity_on_transfer` answers whether the entry preserves its practical operation, privileges, or keyed use-state after transfer.

An implanted system may be physically transferable only by extraction. A permit may be legally transferable only through institutional action. A bonded relic may preserve value and identity but lose bond-specific functions under transfer. A claim-bearing title may transfer legally while preserving neither local access nor social legitimacy.

For that reason, transferability should be treated as a first-class routing pressure inside C04 rather than a minor subnote.

## Item outputs and transformation-result doctrine

Many item-family records do not do anything meaningful until used, claimed, processed, traded, awakened, installed, or legally recognized.

### Output posture fields

Item-family records should support:
- `direct_use_outputs`
- `depletion_outputs`
- `salvage_outputs`
- `processing_outputs`
- `claim_validation_outputs`
- `activation_outputs`
- `legal_or_standing_outputs`
- `transformation_result_outputs`

### Processing-output interaction note

Some item-family entries primarily exist in order to become later outputs. In those cases, processing posture and output posture should be interpreted together rather than as separate incidental notes.

That is especially important for harvested inputs, processed components, dormant relics, ritual catalysts, permits awaiting validation, and other transitional content.

### Doctrine note

C04 does not own downstream reward parceling or broader inflow doctrine. It does need lawful ways to describe what kinds of outputs an item-family entry can generate and under what handling posture those outputs emerge.

## Variability, modularity, and derivative-threshold doctrine

Item-family records vary in how fixed, modular, stateful, or identity-fragile they are.

### Variability fields

Item-family records should support:
- `variability_posture`
- `modularity_profile`
- `upgrade_or_refinement_profile`
- `stateful_identity_risk`
- `host_dependent_identity_risk`
- `derivative_threshold_notes`

### Host-dependent identity-risk doctrine

One of the hardest corpus-scale seams is when an installed, embedded, bonded, or institution-linked item stops behaving like an independent item-family record and begins behaving like a host-bound subsystem or host-bearing identity state.

C04 should therefore preserve explicit risk around host-dependent identity drift.

This matters especially for:
- body-integrated systems
- frame-integrated systems
- relics fused to hosts
- institution-linked licenses or titles whose meaning now depends on organizational identity rather than atomic entry shape

### Derivative-threshold doctrine

An item-family record should be reviewed for derivative promotion when one or more of the following become true:
- the modified or awakened form requires independent reuse
- the item now carries durable continuity distinct from the base record
- the installed or embedded form is now inseparable from host identity in a way C04 cannot lawfully express as an item entry
- the asset has become an institutional or organizational identity rather than an atomic entry
- the item’s overlay or state stack now carries most of the relevant content payload

This matters especially for:
- awakening relics
- living weapons
- smart tools with durable continuity
- claim-bearing titles that become institutional identities
- installed systems that effectively become frame/body subsystems

## Required relationship patterns

C04 inherits C01 relationship grammar and must use explicit relationship structure rather than prose-only implication.

### Item-family relationship guidance

Item-family records should be prepared to use relationships such as:
- `requires`
- `member_of`
- `variant_of`
- `anchored_to`
- `located_in`
- `gated_by`
- `emitted_by`
- `assembled_from`
- `rewards_with`
- `instance_of`
- and other C01-governed relationship forms as needed for host interfaces, processing chains, claim-validation chains, or institutional recognition links

These should be represented using C01 relationship structure, not invented locally as ad hoc prose logic.

## Required lower-doctrine handoffs

C04 must hand off to lower doctrine rather than rewriting it.

At minimum, item-family entries should compose or reference:
- `C01` common record grammar
- `B03` item/equipment doctrine
- `B04` value/exchange doctrine
- `B05` crafting/repair/requisition doctrine
- `B12` organized access / legality doctrine where relevant
- `B13` auxiliary entity doctrine where items interface with auxiliaries
- `B14` frame doctrine where items interface with frames or frame-side channels
- `B16` post-pressure inflow doctrine where item-family records are common outputs or salvage endpoints
- the appropriate Batch C family file when the item interfaces with actors, frames, sites, factions, or reward parcels

C04 may define entry-shape hooks for these interfaces. It may not restate the governing doctrine as if C04 owns it.

## Anti-collapse rules specific to item-family records

C04 must not:
- become a shop or economy chapter
- become a crafting procedure file
- become a legality-enforcement file
- become a frame module file by default
- become a reward parcel family
- treat all licenses, rights, and permits as ordinary objects without routing tests
- restate use procedure, value exchange procedure, legality enforcement, or post-encounter parceling as local family doctrine
- flatten discrete objects, abstract resources, economic assets, and embedded components into one undifferentiated item bucket
- absorb neighboring family ownership merely because a donor calls something gear or treasure

### Precision-enforcement note

Where donor material blurs item, resource, asset, permission, upgrade, installed subsystem, and parcelized reward behavior, C04 should slow down and route deliberately rather than accepting donor shorthand as authoritative.

That is one of the main jobs of this file.

## Reserved split note

Do not split C04 now.

If later corpus pressure proves the file genuinely unwieldy, the preferred reserved split pattern would be:
- `C04a_item_core_and_object_mode_schema`
- `C04b_resource_asset_and_claim_mode_schema`
- `C04c_host_interface_processing_and_transfer_schema`

That split is reserved, not active.

## Minimal abstract item/resource/asset template

The following template extends the C01 grammar with item-family payload blocks. It is a family abstract template, not a converted instance.

```yaml
record:
  identity:
    canonical_id: ""
    record_name: ""
    display_name: ""
    record_class: "atomic_record"
    family_owner: "C04"
    alias_set: []
    visibility_stratum: ""
    field_visibility_overrides: []

  classification:
    ontology_state: "instantiated_record"
    lifecycle_state: "draft"
    dominant_function: "item_content"
    secondary_functions: []
    content_family: "item"

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
    primary_owner: "C04"
    secondary_dependencies: []
    authority_rank: "family_schema"
    governing_files: ["C01", "C04"]
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
    family_tags: ["item"]
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

  item_profile:
    item_modes: []
    item_family_center: ""
    form_factor: ""
    embodiment_profile: ""
    host_dependence_profile: ""
    portability_profile: ""
    custody_posture: ""
    access_posture: ""
    removability_profile: ""
    claim_lock_profile: ""

  lifecycle_and_state:
    use_profile: ""
    depletion_profile: ""
    persistence_class: ""
    recovery_or_refresh_profile: ""
    post_use_state_shift: []
    item_state_profile: ""
    integrity_state: ""
    activation_state: ""
    claim_state: ""
    processing_state: ""
    state_typing_profile: []

  host_interface_profile:
    valid_host_classes: []
    required_interface_class: ""
    slot_or_channel_usage: []
    install_or_removal_class: ""
    attachment_permanence: ""
    host_dependency_threshold: ""
    exclusivity_limits: []
    compatibility_notes: []

  value_claim_and_permission:
    value_expression_profile: ""
    exchange_posture: ""
    claim_profile: ""
    permission_profile: ""
    legal_or_regulatory_hooks: []
    institutional_recognition_hooks: []
    recognition_dependence_profile: ""
    economic_asset_subclasses: []

  processing_and_transformation:
    processing_posture: ""
    activation_or_processing_requirements: []
    salvage_or_refinement_hooks: []
    crafting_or_transformation_hooks: []
    authentication_or_registration_hooks: []
    authentication_posture: ""
    ritual_or_special_activation_hooks: []
    content_readiness_profile: ""

  transferability_profile:
    transferability_profile: ""
    transfer_requirements: []
    value_preservation_on_transfer: ""
    identity_preservation_on_transfer: ""
    functional_continuity_on_transfer: ""
    transfer_routing_pressure_notes: []

  output_posture:
    direct_use_outputs: []
    depletion_outputs: []
    salvage_outputs: []
    processing_outputs: []
    claim_validation_outputs: []
    activation_outputs: []
    legal_or_standing_outputs: []
    transformation_result_outputs: []

  variability_and_derivative_risk:
    variability_posture: ""
    modularity_profile: ""
    upgrade_or_refinement_profile: []
    stateful_identity_risk: ""
    host_dependent_identity_risk: ""
    derivative_threshold_notes: []
```

## Final doctrine statement

C04 is the item/resource/asset-family constitutional schema for Batch C.

It does not reduce the family to ordinary gear.
It does not flatten objects, resources, assets, and components into one mushy bucket.
It does not become a stealth economy file, crafting file, or reward file.
It does not absorb neighboring ownership merely because donor material calls something equipment or treasure.

Its purpose is to let Astra represent atomic item/resource/asset entries lawfully across a mixed donor corpus while preserving boundary control, processing posture, transfer logic, recognition dependence, host-interface clarity, and cross-file interoperability.

