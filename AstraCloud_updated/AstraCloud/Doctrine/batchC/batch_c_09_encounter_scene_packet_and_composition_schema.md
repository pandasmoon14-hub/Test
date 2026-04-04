# batchC_09_encounter_scene_packet_and_composition_schema.md

## Purpose and authority

This file is the **encounter/scene composition family schema authority** for Batch C.

Its job is to define the Astra-native entry structure for packaged encounters, scene packets, roster packets, and other bounded composite play structures assembled from lower-level Batch C records. It is the family file that turns the common record grammar from C01 into a reusable composition schema that can survive mixed donor pressure at corpus scale without collapsing into actor files, site files, challenge files, or full mission/scenario structures.

C09 is not a campaign file. It is not a mission tree. It is not a bestiary chapter. It is not a site chapter. It is not a challenge catalog. It is not a container anthology.

It owns:
- packaged encounter/scene composition structure
- composition-object doctrine for bounded play packets
- encounter/scene packet payload blocks on top of C01
- composition modes and routing classes
- packet mode versus packet function versus packet posture distinction
- packet identity, reuse, portability, and pinning doctrine
- packet scale, topology, presentation-layer, and payload-density doctrine
- packet embodiment doctrine
- packet temporality, recurrence, persistence, and reset/reseed doctrine
- roster assembly and role-slot doctrine
- local composition-only placement, staging, and scene-state doctrine
- site-slice, faction-slice, challenge-slice, and frame-slice integration hooks
- ingress, egress, reinforcement, withdrawal, staged presence, and packet legality/access posture
- packet trigger, escalation, timer, attention-state, and scene-pressure hooks
- bounded social packet doctrine
- objective, exit-condition, chaining, and successor-state posture at packet level
- packet-local override versus derivative-instance doctrine
- encounter output, source-emission, and handoff hooks
- composition-specific derivative-threshold and boundary-control doctrine
- composition-family relationship expectations
- composition-family validation-stress doctrine
- composition-family anti-collapse rules
- minimal abstract encounter/scene packet template

It does **not** own:
- actor-content identity already owned by C02
- overlay/template doctrine already owned by C03
- item/resource/asset identity already owned by C04
- frame/platform identity already owned by C05
- site/place identity already owned by C06
- organization/social-body identity already owned by C07
- challenge-object identity already owned by C08
- mission/scenario/adventure-path structure already owned by C10
- reward/inflow parcel packaging already owned by C11
- sourcebook bundle/container packaging already owned by C13
- live-play presentation behavior
- donor conversion instances as doctrine

## Why this file exists

Large donor corpora do not stop at atomic records. They also contain bounded play structures that assemble actors, sites, challenge objects, organizations, overlays, timers, entry states, reinforcements, and objectives into one local packet.

Those structures are neither:
- atomic records,
- merely loose references to component parts,
- nor full mission/scenario containers.

C09 exists because Astra requires one lawful family schema for bounded encounter/scene composition that can:
- assemble lower-level records without re-owning them,
- preserve packet-local staging, placement, visibility, legality, and trigger logic,
- distinguish a bounded scene packet from a whole scenario,
- and support pinning, local composition overrides, and packet-specific state logic without mutating the underlying atomic records.

This file therefore treats the family center as **bounded scene composition**, not as donor labels like encounter, fight, room, wave, skirmish, scene, or event packet.

## Scope boundaries and exclusions

C09 covers content entries whose dominant doctrinal function is to exist as a bounded assembled play packet composed from lower-level records for use as one encounter, scene, skirmish, standoff, infiltration node, hazard packet, trial slice, checkpoint packet, negotiation packet, or similarly local play structure.

That includes, where they remain encounter/scene composition rather than missions or bundles:
- roster packets
- encounter packets
- scene packets
- staged scene packets
- linked local wave packets
- bounded hazard/actor/site/challenge assemblies
- local traversal or infiltration scene packets
- local defense or breach packets
- bounded social, witness, tribunal, or standoff packets
- packet-based exceptional content

C09 excludes:
- whole missions, investigations, heists, crawls, trial arcs, modules, or scenario trees -> C10
- atomic actors, sites, factions, frames, or challenge objects merely because they are scene-relevant -> C02/C05/C06/C07/C08
- sourcebook bundles, gazetteers, bestiary packs, or anthology containers -> C13
- generator tables and encounter tables as such -> C12
- reward/inflow parcels -> C11

## Composition-object doctrine

An **encounter/scene packet** is a composite record whose primary job is to assemble lower-level records into one bounded local play structure without re-owning those lower records.

A composition packet may:
- include or reference actors, sites, challenge objects, organizations, frames, and overlays
- declare which revisions are pinned
- define local placement, staging, presence, entry, exit, and timing posture
- define packet-level scene objectives, triggers, escalation, and successor hooks
- apply lawful packet-local overrides without silently changing atomic identity

A composition packet does **not** automatically create new atomic identities for its contents.

## Composition modes, packet functions, and packet posture doctrine

C09 must distinguish what broad kind of packet this is from what the packet is primarily for and how it is currently behaving.

### Core composition modes

A composition-family record may declare one or more composition modes, with one marked primary where needed:
- `roster_packet`
- `encounter_packet`
- `scene_packet`
- `staged_scene_packet`
- `wave_or_reinforcement_packet`
- `hazard_pressure_packet`
- `infiltration_or_breach_packet`
- `social_or_standoff_packet`
- `setpiece_scene_packet`
- `exceptional_composite_packet`

### Mode guidance

- **roster_packet**: a bounded assembly focused primarily on included bodies, roles, and presence rather than richer scene logic.
- **encounter_packet**: a bounded local play structure focused on active opposition, contact, conflict, or immediate pressure.
- **scene_packet**: a broader bounded local scene that may include conflict, negotiation, traversal, hazard, or mixed local pressure.
- **staged_scene_packet**: a bounded scene with explicit internal phase or stage logic but not yet a full mission/scenario structure.
- **wave_or_reinforcement_packet**: a local composition where staged arrivals or changing presence are structurally central.
- **hazard_pressure_packet**: a scene packet where challenge objects, environmental pressure, and bounded response states dominate.
- **infiltration_or_breach_packet**: a local packet built around access, stealth, breach, security, or route-control pressure.
- **social_or_standoff_packet**: a bounded packet centered on confrontation, negotiation, brinkmanship, or controlled audience pressure.
- **setpiece_scene_packet**: a bounded composite with unusually dense multi-part structure still below scenario scale.
- **exceptional_composite_packet**: a significance-bearing composition record with unusual continuity, scale, or boundary pressure.

### Packet function profile

Mode answers what kind of packet this is.
`packet_function_profile` answers what the packet is primarily for.

Useful packet functions include:
- `hold_or_defend`
- `breach_or_enter`
- `escape_or_extract`
- `escort_or_preserve`
- `survive_or_endure`
- `negotiate_or_de_escalate`
- `retrieve_or_reconstruct`
- `witness_or_verify`
- `delay_or_stall`
- `route_through_or_cross`
- `trigger_or_prevent_trigger`
- `secure_or_deny_site_slice`
- `checkpoint_or_clearance`
- `investigate_local_slice`
- `ritual_completion_or_interruption`

### Packet posture doctrine

Packet posture answers how the bounded packet is currently behaving or meant to be read, such as:
- `hostile`
- `guarded`
- `contested`
- `ceremonial`
- `training_or_tutorial`
- `public_but_tense`
- `covert`
- `degraded`
- `improvised`
- `official_or_lawful`
- `illicit_or_denied`

Mode, function, and posture must not be collapsed.

## Packet identity, reuse, portability, and pinning doctrine

C09 must distinguish packet identity from the identity of the records it includes.

### Packet identity fields

Encounter/scene packets should support:
- `packet_identity_class`
- `packet_reuse_profile`
- `packet_portability_profile`
- `pinning_policy`
- `local_revision_scope`
- `identity_preservation_note`

### Pinning doctrine

A packet may:
- reference live lower records,
- pin specific lower-record revisions,
- or pin a mixed set of revisions where packet stability requires that choice.

Packet identity does not overwrite atomic identity.
Pinned packet use does not silently rewrite lower records.
A packet may be revised while preserving packet identity, and it may also be superseded by a new packet when the bounded scene itself materially changes.

### Portability doctrine

Useful packet portability classes include:
- `reusable_across_many_sites`
- `site_bound_reusable`
- `mission_bound_but_reusable`
- `one_off_authored`
- `converted_appendix_packet`
- `canon_anchor_packet`
- `training_or_example_packet`
- `generative_seed_packet`

## Packet scale, topology, presentation layers, and payload density

C09 must support both light roster assemblies and dense local scene structures without forcing them into one depth.

### Presentation layers

Useful presentation layers include:
- `minimal_packet_form`
- `standard_packet_form`
- `expanded_packet_form`

### Payload-density doctrine

`payload_density` is a schema-expression choice, not a statement of narrative prestige.

A small guard-post packet or travel-checkpoint packet may legitimately use minimal expression.
A breach scene, ritual chamber confrontation, or layered reinforcement packet may require expanded expression.

### Packet scale doctrine

Useful packet scales include:
- `micro_contact_packet`
- `room_scale_packet`
- `district_slice_packet`
- `site_slice_packet`
- `local_route_packet`
- `bounded_setpiece_packet`

Packet scale is about the bounded local play footprint, not about long-form mission scope.

### Packet topology doctrine

Useful packet topology classes include:
- `pointlike_contact`
- `chamber_or_room_packet`
- `corridor_or_path_packet`
- `node_and_branch_packet`
- `ring_or_perimeter_defense_packet`
- `layered_slice_packet`
- `split_front_packet`
- `moving_localized_field_packet`
- `multi_anchor_local_packet`

Topology is about local scene arrangement, not long-form scenario flow.

## Packet embodiment doctrine

A large donor corpus will include packets that are made real by different kinds of things.

### Embodiment fields

Encounter/scene packets should support:
- `packet_embodiment_profile`
- `primary_pressure_carriers`
- `bounded_scene_anchor_hooks`

### Useful embodiment classes

Useful classes include:
- `roster_embodied`
- `site_slice_embodied`
- `challenge_mesh_embodied`
- `social_audience_embodied`
- `route_embodied`
- `mixed_embodiment`

This keeps checkpoint scenes, breach scenes, negotiation chambers, ritual lattices, and labyrinth slices from being flattened into one encounter shape.

## Packet temporality, recurrence, persistence, and reset/reseed doctrine

Scene packets are not all used the same way over time.

### Temporality fields

Encounter/scene packets should support:
- `packet_temporality_profile`
- `packet_persistence_profile`
- `repeatability_profile`
- `reset_or_reseed_hooks`
- `context_dependency_profile`

### Temporality doctrine

These dimensions must remain distinct:
- **temporality**: how the packet exists once active
- **recurrence**: whether it can appear again
- **persistence**: whether it remains altered after resolution
- **reset/reseed**: how it returns, if it returns

### Useful temporality classes

Useful classes include:
- `one_use_scripted_packet`
- `repeatable_packet`
- `site_reusable_packet`
- `generator_seed_packet`
- `tutorial_or_training_packet`
- `conditional_return_packet`
- `campaign_recurring_packet`
- `persistent_local_state_packet`
- `reseeded_variant_packet`

## Assembly and inclusion doctrine

C09 is first and foremost an assembly schema.

### Assembly fields

Encounter/scene packets should support:
- `included_record_hooks`
- `pinned_record_hooks`
- `role_slot_profile`
- `required_component_classes`
- `optional_component_classes`
- `packet_composition_notes`

### Assembly doctrine

A packet may include:
- actors
- sites or site slices
- challenge objects or challenge slices
- local organizations or representation slices
- frames or hosted platforms
- local overlays or packet-bound modifiers

A packet may summarize included content, but it must not silently re-own it.
That anti-duplication rule is one of the main constitutional protections of C09.

## Roster assembly, role-slot, and roster-semantics doctrine

Not every packet is just an untyped list of included records.

### Roster fields

Encounter/scene packets should support:
- `roster_profile`
- `role_slot_profile`
- `presence_priority_profile`
- `replacement_or_fill_rules`
- `roster_semantics_profile`

### Role-slot doctrine

Useful packet role slots may include:
- `primary_pressure_actor`
- `support_actor`
- `site_anchor`
- `challenge_anchor`
- `authority_anchor`
- `escape_or_exit_anchor`
- `reinforcement_slot`
- `objective_anchor`
- `hazard_source`
- `witness_or_bystander_slot`

These are packet-local composition roles, not replacements for lower-level role doctrine inside the included records.

### Roster-semantics doctrine

Useful roster semantics include:
- `fixed_unique_roster`
- `repeatable_template_roster`
- `scalable_roster`
- `anchor_plus_filler_roster`
- `role_balanced_roster`
- `leader_core_with_latent_additions`
- `witness_or_bystander_heavy_roster`
- `authority_backed_roster`
- `challenge_dominated_minimal_roster`

## Placement, site-slice, and locality doctrine

Packets often need local place context without re-owning a whole site record.

### Placement fields

Encounter/scene packets should support:
- `site_slice_hooks`
- `site_slice_aspect_profile`
- `locality_profile`
- `relative_placement_hooks`
- `entry_vector_hooks`
- `exit_vector_hooks`
- `terrain_or_layout_notes`

### Site-slice doctrine

A packet may anchor to:
- a whole site,
- a district slice,
- a room/chamber slice,
- a corridor/path slice,
- a support-shell slice,
- a partition slice,
- a visibility_or_legibility slice,
- a hazard-conditioned slice,
- a platform slice,
- or a moving/localized environmental pocket.

This does not turn C09 into a site file. It allows local place context to be compositionally meaningful.

## Challenge-slice, organization-slice, and frame-slice integration doctrine

Packets often need limited slices of neighboring families rather than full family ownership.

### Slice-integration fields

Encounter/scene packets should support:
- `challenge_slice_hooks`
- `challenge_slice_aspect_profile`
- `organization_slice_hooks`
- `frame_slice_hooks`
- `service_or_access_slice_hooks`
- `visibility_or_information_slice_hooks`

### Challenge-slice doctrine

A packet may include challenge slices such as:
- `trigger_bearing_object`
- `linked_challenge_cluster`
- `setpiece_mesh_slice`
- `route_gate`
- `hazard_field`
- `trial_object`
- `security_or_alarm_structure`
- `puzzle_bearing_barrier`

This keeps challenge identity in C08 while allowing packet-local challenge use to be precise.

### Doctrine note

A packet may include only the relevant local slice of a larger site, organization, or frame context. That does not create a new atomic site, organization, or frame identity. It is bounded composition.

## Ingress, egress, staged presence, reinforcement, withdrawal, and packet legality/access posture

Many packets are defined by who is present at start, who enters later, and under what kind of access posture the packet begins.

### Presence and staging fields

Encounter/scene packets should support:
- `starting_presence_hooks`
- `latent_presence_hooks`
- `reinforcement_hooks`
- `withdrawal_or_escape_hooks`
- `arrival_condition_hooks`
- `departure_condition_hooks`
- `staging_profile`
- `staging_topology_profile`
- `packet_legality_or_access_posture`

### Staging-topology doctrine

Useful staging profiles include:
- `hidden_at_start`
- `delayed_reveal`
- `timed_reinforcement`
- `threshold_triggered_arrival`
- `offsite_support`
- `dormant_until_disturbed`
- `conditional_witness_or_bystander_reveal`
- `collapse_or_withdrawal_cascade`
- `escalation_wave`
- `replacement_slot_refill`

### Packet legality/access doctrine

Useful local entry postures include:
- `ordinary_lawful_entry`
- `contested_entry`
- `covert_or_unauthorized_entry`
- `sponsored_or_escorted_entry`
- `triggered_entry`
- `claim_based_participation`
- `captive_or_forced_entry`
- `open_public_access`

### Doctrine note

A packet may begin with only part of its eventual roster visible.
Some entries may start hidden, delayed, offsite, dormant, called in, released, or conditional.
These are packet-level truths and should not be forced into the atomic records themselves.

## Triggers, clocks, escalation, visibility, and scene-pressure doctrine

C09 must support bounded scene logic without becoming C10.

### Scene-pressure fields

Encounter/scene packets should support:
- `packet_trigger_hooks`
- `clock_or_timer_profile`
- `escalation_hooks`
- `pressure_shift_hooks`
- `alert_state_hooks`
- `visibility_pressure_profile`
- `information_asymmetry_profile`
- `fail_forward_or_fail_closed_profile`

### Visibility and information pressure doctrine

A packet may be structured around:
- uncertain visibility
- hidden roster elements
- knowledge asymmetry
- route ignorance
- audience ignorance
- false certainty
- clue-bearing witnesses
- evidence release after a trigger

C09 does not own stealth or investigation procedure. It does need lawful places to declare bounded information posture at the packet level.

### Doctrine note

This section covers local scene pacing and escalation: alarms, reinforcements, wave clocks, collapse countdowns, extraction windows, local lockdowns, social deadlines, and similar bounded scene pressures.

Once branching operational structure becomes primary, reroute pressure to C10.

## Packet-local state versus included-record state doctrine

This is one of the main anti-drift rules in the file.

### Local scene-state fields

Encounter/scene packets should support:
- `local_visibility_state`
- `local_hostility_posture`
- `local_staging_state`
- `local_alert_state`
- `local_access_state`
- `local_objective_state`
- `local_time_or_pressure_state`

### Doctrine note

C09 may declare packet-local scene state without rewriting the underlying actor, site, challenge, organization, or frame identity. This distinction must remain explicit or packet schemas will begin mutating lower-family records by convenience.

## Packet-bound overlay doctrine and derivative-instance watch

This is one of the most important C09 safeguards.

### Override fields

Encounter/scene packets should support:
- `local_override_profile`
- `packet_bound_overlay_hooks`
- `packet_bound_overlay_class`
- `derivative_instance_watch_flags`
- `identity_mutation_prohibition_notes`

### Packet-bound overlay doctrine

C09 should distinguish between:
- packet-local disposable overlays,
- packet-bound overlays stable within this packet identity,
- and overlays or local variants that have become reusable enough to deserve promotion into C03 or explicit derivative records elsewhere.

### Doctrine note

A packet may locally alter starting conditions, placement, visibility, timing, local hostility posture, temporary service access, or reinforcement logic.

But if packet-local adjustments begin to create a new independently reusable actor, site, challenge object, or frame identity, that is no longer a mere packet-local override. It is derivative pressure and should be routed explicitly rather than hidden inside the packet.

## Bounded social packet doctrine

Social packets are legitimate C09 content so long as they remain bounded local scenes rather than whole scenario structures.

### Social packet fields

Encounter/scene packets should support:
- `bounded_social_pressure_profile`
- `audience_structure_hooks`
- `witness_management_hooks`
- `compliance_or_surrender_hooks`
- `clearance_or_permission_resolution_hooks`

### Useful social packet classes

Useful bounded social packets include:
- `brinkmanship_scene`
- `audience_management_scene`
- `guarded_negotiation`
- `checkpoint_clearance`
- `ritual_hearing`
- `tribunal_slice`
- `accusation_or_revelation_scene`
- `escort_with_witness_scene`
- `surrender_or_compliance_scene`

This keeps C09 from overfitting all packets to combat pressure.

## Wave and reinforcement doctrine

Reinforcement is not all one kind of event.

### Reinforcement fields

Encounter/scene packets should support:
- `wave_structure_profile`
- `reinforcement_source_profile`
- `reinforcement_trigger_profile`

### Useful reinforcement classes

Useful wave/reinforcement classes include:
- `timed`
- `threshold_based`
- `site_emitted`
- `challenge_emitted`
- `organization_backed`
- `frame_deployed`
- `morale_driven`
- `alarm_driven`
- `objective_triggered`

This is useful for combat packets, evacuations, social escalation, site lockdown, ritual release, and pursuit packets.

## Objectives, exit conditions, packet chaining, and successor-state hooks

C09 needs bounded scene goals without becoming a scenario file.

### Objective and chaining fields

Encounter/scene packets should support:
- `packet_objective_profile`
- `success_condition_hooks`
- `failure_condition_hooks`
- `exit_condition_hooks`
- `predecessor_packet_hooks`
- `successor_packet_hooks`
- `optional_branch_handoff_hooks`
- `failure_branch_handoff_hooks`
- `successor_state_hooks`
- `handoff_to_mission_hooks`

### Doctrine note

A packet may have immediate local goals such as survive, breach, extract, hold, negotiate, escape, disable, endure, escort, or witness. These are bounded local scene objectives, not whole mission structures.

C09 may support forward references and bounded chaining so long as the record’s dominant identity remains one local packet rather than a scenario tree.

## Output posture, source-emission posture, and downstream handoffs

C09 must support scene-local outputs without swallowing C11 or C10.

### Output fields

Encounter/scene packets should support:
- `packet_source_emission_profile`
- `scene_output_hooks`
- `reward_or_inflow_handoff_hooks`
- `site_state_change_hooks`
- `organization_state_change_hooks`
- `actor_state_change_hooks`
- `challenge_state_change_hooks`
- `evidence_or_information_handoff_hooks`

### Source-emission doctrine

Useful source-emission classes include:
- `site_emitted`
- `organization_emitted`
- `challenge_emitted`
- `mission_instantiated`
- `generator_instantiated`
- `free_standing_reusable_packet`

### Doctrine note

A packet may change local access, site status, actor disposition, challenge state, evidence availability, or reward eligibility. C09 should expose those handoffs while leaving parcel packaging to C11 and longer operational chaining to C10.

## Composition versus mission, container, and generator boundary control

This is the most important routing section in the file.

### C09 versus C10 rule

If the dominant identity is a bounded local scene or encounter assembly, route pressure to C09.

If the dominant identity is a larger operational or narrative container with branching flow, linked objectives across multiple packets, investigation/heist/crawl structure, or module-scale progression, route pressure to C10.

A single encounter packet is not the same thing as a whole scenario.

### C09 versus C13 rule

If the dominant identity is packaging, anthology, sourcebook grouping, dossier format, bestiary pack, or reference bundle, route pressure to C13.

A packet may appear inside many containers without changing identity.
That does not make it a container-family record.

### C09 versus C12 rule

If the dominant identity is generative output logic, table structure, oracle procedure, or encounter-table machinery, route pressure to C12.

A packet may be a generator output target.
It is not itself the generator.

### High-risk edge classes

Examples of composition-adjacent edge cases include:
- mission packets that look like scene packets but contain branching multi-scene flow
- encounter tables whose outputs embed partial packet logic
- site slices mistaken for whole packets
- heavily overlaid actor groups mistaken for full encounter composition
- packets whose local overrides silently create derivative atomic records
- setpiece scenes swollen with enough clocks, branches, and states to function as mini-scenarios

C09 should preserve routing discipline for these cases rather than accepting donor shorthand at face value.

## Required relationship patterns and relationship-discipline doctrine

C09 inherits C01 relationship grammar and must use explicit relationship structure rather than prose-only implication.

### Composition-family relationship guidance

Encounter/scene packets should be prepared to use relationships such as:
- `contains`
- `instantiates`
- `references`
- `located_in`
- `gated_by`
- `emitted_by`
- `requires`
- `tied_to_event`
- `rewards_with`
- `supersedes`
- and other C01-governed relationship forms as needed for packet assembly, staging, site slices, successor states, or mission handoffs

### Relationship-discipline rule

If packet work repeatedly wants relationship verbs beyond current C01 structure, the answer is an upstream constitutional update, not local relationship sprawl inside C09.

## Required lower-doctrine handoffs

C09 must hand off to lower doctrine rather than rewriting it.

At minimum, encounter/scene packets should compose or reference:
- `C01` common record grammar
- the lower Batch C family files whose content the packet assembles
- relevant Batch A/B doctrine through those lower schemas where packet behavior depends on conflict, traversal, perception, access, frame operation, or inflow logic

C09 may define packet-level assembly and scene-state hooks. It may not restate full lower-family payloads as if C09 owned them.

## Composition-family validation stress list

The most common routing and interpretation failure modes for this family include:
- packet versus site confusion
- packet versus mission confusion
- packet versus challenge mesh confusion
- packet versus actor-group confusion
- packet-local override mutating lower-record identity
- setpiece packet swelling into scenario tree
- generator output mistaken for packet family record
- bundle grouping mistaken for packet composition

These should be treated as recurring validation checks rather than rare exceptions.

## Anti-collapse rules specific to composition-family records

C09 must not:
- become a bestiary chapter with local stat blocks copied in
- become a site file with local place identity re-owned
- become a challenge catalog with trigger logic duplicated wholesale
- become a mission/scenario tree because the scene has multiple moving parts
- become a sourcebook bundle because packets are grouped together in donor appendices
- flatten roster packets, scene packets, staged packets, and setpiece packets into one undifferentiated encounter blob
- silently mutate atomic record identity through packet-local overrides
- replace lower-record references with duplicated local payloads unless C09 explicitly owns that packet-local field

### Anti-duplication doctrine

A packet may summarize linked content, but it must not silently re-own it.
A packet may include content, but it must not rewrite atomic identity unless a derivative record is explicitly created elsewhere.
A composition schema may constrain local packet behavior, but it must not restate upstream doctrine unless it is defining a packet-owned local value space.

## Reserved split note

Do not split C09 now.

If later corpus pressure proves the file genuinely unwieldy, the preferred reserved split pattern would be:
- `C09a_packet_core_and_identity_schema`
- `C09b_roster_staging_and_scene_pressure_schema`
- `C09c_boundary_control_and_downstream_handoff_schema`

That split is reserved, not active.

## Minimal abstract encounter/scene packet template

The following template extends the C01 grammar with composition-family payload blocks. It is a family abstract template, not a converted instance.

```yaml
record:
  identity:
    canonical_id: ""
    record_name: ""
    display_name: ""
    record_class: "composite_record"
    family_owner: "C09"
    alias_set: []
    visibility_stratum: ""
    field_visibility_overrides: []

  classification:
    ontology_state: "instantiated_record"
    lifecycle_state: "draft"
    dominant_function: "encounter_scene_composition"
    secondary_functions: []
    content_family: "composition"

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
    primary_owner: "C09"
    secondary_dependencies: []
    authority_rank: "family_schema"
    governing_files: ["C01", "C09"]
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
    applicability_scope: ["scene_scale"]
    domains_of_use: ["encounter_packeting"]
    accepted_overlays: []
    emitted_overlays: []
    compatible_containers: []
    incompatible_contexts: []

  tags_and_indexing:
    family_tags: ["composition", "encounter_packet"]
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

  packet_profile:
    composition_modes: []
    packet_function_profile: []
    packet_posture_profile: []
    packet_identity_class: ""
    packet_reuse_profile: ""
    packet_portability_profile: ""
    pinning_policy: ""
    local_revision_scope: ""
    presentation_layer: ""
    payload_density: ""
    packet_scale: ""
    packet_topology_class: ""
    packet_embodiment_profile: ""
    primary_pressure_carriers: []
    bounded_scene_anchor_hooks: []
    packet_temporality_profile: ""
    packet_persistence_profile: ""
    repeatability_profile: ""
    reset_or_reseed_hooks: []
    context_dependency_profile: ""

  assembly:
    included_record_hooks: []
    pinned_record_hooks: []
    role_slot_profile: []
    required_component_classes: []
    optional_component_classes: []
    packet_composition_notes: []

  roster_and_semantics:
    roster_profile: ""
    presence_priority_profile: ""
    replacement_or_fill_rules: []
    roster_semantics_profile: ""

  placement_and_locality:
    site_slice_hooks: []
    site_slice_aspect_profile: []
    locality_profile: ""
    relative_placement_hooks: []
    entry_vector_hooks: []
    exit_vector_hooks: []
    terrain_or_layout_notes: []

  slice_integration:
    challenge_slice_hooks: []
    challenge_slice_aspect_profile: []
    organization_slice_hooks: []
    frame_slice_hooks: []
    service_or_access_slice_hooks: []
    visibility_or_information_slice_hooks: []

  presence_and_staging:
    starting_presence_hooks: []
    latent_presence_hooks: []
    reinforcement_hooks: []
    withdrawal_or_escape_hooks: []
    arrival_condition_hooks: []
    departure_condition_hooks: []
    staging_profile: ""
    staging_topology_profile: []
    packet_legality_or_access_posture: ""

  scene_pressure:
    packet_trigger_hooks: []
    clock_or_timer_profile: ""
    escalation_hooks: []
    pressure_shift_hooks: []
    alert_state_hooks: []
    visibility_pressure_profile: ""
    information_asymmetry_profile: ""
    fail_forward_or_fail_closed_profile: ""

  local_scene_state:
    local_visibility_state: ""
    local_hostility_posture: ""
    local_staging_state: ""
    local_alert_state: ""
    local_access_state: ""
    local_objective_state: ""
    local_time_or_pressure_state: ""

  overrides_and_mutation_watch:
    local_override_profile: ""
    packet_bound_overlay_hooks: []
    packet_bound_overlay_class: ""
    derivative_instance_watch_flags: []
    identity_mutation_prohibition_notes: []

  social_and_wave_pressure:
    bounded_social_pressure_profile: []
    audience_structure_hooks: []
    witness_management_hooks: []
    compliance_or_surrender_hooks: []
    clearance_or_permission_resolution_hooks: []
    wave_structure_profile: []
    reinforcement_source_profile: []
    reinforcement_trigger_profile: []

  objectives_and_handoffs:
    packet_objective_profile: []
    success_condition_hooks: []
    failure_condition_hooks: []
    exit_condition_hooks: []
    predecessor_packet_hooks: []
    successor_packet_hooks: []
    optional_branch_handoff_hooks: []
    failure_branch_handoff_hooks: []
    successor_state_hooks: []
    handoff_to_mission_hooks: []

  output_posture:
    packet_source_emission_profile: ""
    scene_output_hooks: []
    reward_or_inflow_handoff_hooks: []
    site_state_change_hooks: []
    organization_state_change_hooks: []
    actor_state_change_hooks: []
    challenge_state_change_hooks: []
    evidence_or_information_handoff_hooks: []
```

## Final doctrine statement

C09 is the encounter/scene composition-family constitutional schema for Batch C.

It does not reduce the family to combat encounters only.
It does not collapse composition into actors, sites, challenges, or missions.
It does not become a stealth scenario file.
It does not absorb neighboring ownership merely because donor material groups many components together in one local section.

Its purpose is to let Astra represent bounded encounter and scene packets lawfully across a mixed donor corpus while preserving packet identity, lower-record integrity, local staging, scene pressure, bounded objectives, packet chaining, and cross-file interoperability.

