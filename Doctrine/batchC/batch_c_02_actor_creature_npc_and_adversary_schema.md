# batchC_02_actor_creature_npc_and_adversary_schema.md

## Purpose and authority

This file is the **actor-content family schema authority** for Batch C.

Its job is to define the Astra-native entry structure for actor-content records: creatures, NPCs, named adversaries, squads, swarms, elite units, and actor-content entries generally. It is the family file that turns the common record grammar from C01 into a reusable actor schema that can survive mixed donor pressure at corpus scale.

C02 is not a bestiary. It is not a roster. It is not a lore encyclopedia. It is not an encounter-builder. It is not a mission file. It is not a site file. It is not a reward file.

It owns:
- actor-content record structure
- actorhood doctrine for Batch C
- actor-specific payload blocks on top of C01
- actor modes and routing classes
- actor identity/significance/persistence fields
- actor body/presence/scale fields
- actor agency and command posture fields
- actor cognition/communication/social-tractability fields
- actor pressure, survivability, and resolution-state interface fields
- actor ability attachment doctrine
- actor-specific dependency hooks to frames, auxiliaries, items, sites, factions, and inflow structures
- actor ingress/egress/transformation fields
- actor-specific relationship expectations
- actor-specific anti-collapse rules
- minimal abstract actor template

It does **not** own:
- overlay/template doctrine already owned by C03
- item ontology already owned by C04 and B03/B04/B05
- frame entry structure already owned by C05
- site or locale entry structure already owned by C06
- faction or polity entry structure already owned by C07
- challenge-object schema already owned by C08
- encounter composition already owned by C09
- mission/scenario structure already owned by C10
- reward parcel packaging already owned by C11
- generator or table structures already owned by C12
- live-play presentation behavior
- donor conversion instances as doctrine

## Why this file exists

Batch C must provide a lawful schema for actor-content because donor corpora do not present actors in one uniform shape. Some donors pressure toward solo creatures, some toward structured NPCs, some toward battle groups or swarms, some toward remotes and summons, some toward bonded pairs, and some toward edge cases that straddle site, faction, challenge, or frame logic.

C02 exists so those different donor-side actor constructs can be translated into one Astra-native family grammar without collapsing unlike constructs into flat "monster stat blocks" or pushing actor-like entries into the wrong Batch C families.

This file therefore treats the family center as **actorhood**, not as donor labels like monster, beast, NPC, or unit.

## Scope boundaries and exclusions

C02 covers content entries whose dominant doctrinal function is **agency-bearing participation** in conflict, perception, pressure exchange, social interaction, escort, command, service-bearing agency, pursuit, defense, or comparable actor-like action.

That includes, where they remain actor-content rather than overlays or compositions:
- creatures
- animals and fauna
- humanoid NPCs
- hostile or neutral adversaries
- allies and retainers
- named villains and recurring rivals
- squads, mobs, swarms, and battle groups represented as one acting entity
- summons, projections, remotes, companions, and proxy bodies
- support actors and auxiliary actors
- abstracted or reduced actor forms that still function as actors

C02 excludes:
- purely modifying templates, rank upgrades, faction skins, environment skins, corruption layers, mounted packages, and similar overlays -> C03
- vehicles, mechs, ships, stations, and operational platforms as entries in their own right -> C05
- places, settlements, districts, habitats, and civic locales even when they present actor-like traits -> C06 unless routed here by dominant function
- organizations, institutions, guilds, agencies, houses, and polities -> C07
- hazards, traps, puzzles, trials, and challenge-objects that are not primarily actor-content -> C08
- assembled encounter rosters and scene packets -> C09
- mission/scenario containers -> C10
- reward parcels and packaged inflows -> C11

## Actorhood doctrine

An **actor record** is a content record whose primary job is to represent an entity, unitized group, proxy, or actor-like construct that can:
- take actions or impose pressure
- receive pressure or be targeted
- occupy or traverse context
- participate in perception or information exchange
- participate in social or command relationships where relevant
- exist as a reusable content object across encounters, sites, missions, and bundles without losing identity

Actorhood is not limited to biological life or to humanoid sapience.

Actorhood may include:
- biological beings
- supernatural beings
- synthetic beings
- remote bodies
- summoned presences
- distributed or networked presences
- group abstractions represented as one entity
- actorized service or support entities

Actorhood is established by dominant function, not by donor naming convention.

Actorhood does not require humanoid communication, ordinary sociality, or biological life. Those are actor traits that may or may not be present, not prerequisites for actor-family routing.

## Actor modes and routing classes

C02 must support different actor modes without splitting them into unrelated families.

### Core actor modes

An actor record may declare one or more actor modes, with one marked primary where needed:
- `solo_actor`
- `paired_actor`
- `group_actor`
- `distributed_actor`
- `support_actor`
- `auxiliary_actor`
- `proxy_actor`
- `exceptional_named_actor`
- `abstracted_actor`

### Mode guidance

- **solo_actor**: one discrete acting entity.
- **paired_actor**: a bonded or functionally inseparable pair such as rider-mount, pilot-frame-linked body, handler-beast pair, symbiote pair, or twin-entity pair.
- **group_actor**: many similar or coordinated units represented as one acting entity, such as swarms, squads, mobs, or battle groups.
- **distributed_actor**: an actor whose functioning identity spans multiple nodes, bodies, projections, or linked parts.
- **support_actor**: an actor whose primary role is support, aid, service, logistics, or enabling activity rather than standalone frontline action.
- **auxiliary_actor**: an actor structurally linked to another actor, faction, frame, site, or controller but still requiring actor-record representation.
- **proxy_actor**: an actor body or presence serving as a remote, projected, summoned, duplicated, or intermediary manifestation.
- **exceptional_named_actor**: a recurring or identity-heavy actor with stronger continuity, significance, and reuse expectations.
- **abstracted_actor**: an actor still functioning as actor-content but represented in reduced, unusual, or heavily abstracted form.

### Support, auxiliary, and proxy distinction note

These three modes may overlap in practice, but they do not do the same doctrinal job.

- `support_actor` is role-defined.
- `auxiliary_actor` is structurally linked as a dependent, adjunct, or attached secondary actor.
- `proxy_actor` is a substitute, remote, projected, duplicated, summoned, or intermediary presence standing in for another actor or source.

C02 must support these modes without forcing separate files unless repeated strain later proves that a reserved split is necessary.

## Actor identity, significance, and persistence

C02 extends C01 identity grammar with actor-specific identity strata.

### Actor identity strata

Every actor record should support these distinct classificatory dimensions:
- `ontological_posture`
- `operational_role`
- `narrative_significance_tier`
- `allegiance_posture`

These do different jobs.

- `ontological_posture` answers what kind of being or thing the actor is in structural terms.
- `operational_role` answers what the actor does in play.
- `narrative_significance_tier` answers how much recurrence, continuity, and narrative weight the actor is expected to carry.
- `allegiance_posture` answers how the actor is currently situated relative to sides, authorities, obligations, alignments, or environmental hostility.

A bodyguard and a raider may share operational-role traits while having very different allegiance postures. These fields must therefore remain distinct.

### Ontological-posture doctrine note

`ontological_posture` should be treated as a governed structural field rather than a flavor bucket. It is expected to distinguish posture classes such as biological, synthetic, supernatural, projected, distributed, hybrid, constructed, site-emitted, service-emergent, or equivalent corpus-scale categories that materially affect routing and dependency logic.

### Operational-role doctrine note

`operational_role` should identify what the actor primarily does in play terms rather than what it is called in donor flavor. Useful role families may include combatant, controller, support, scout, service agent, intermediary, escort, hazard-bearing pursuer, civilian pressure source, authority node, mission gate actor, or comparable Astra-native functions.

### Significance versus persistence doctrine

`narrative_significance_tier` and persistence fields are independent axes. An actor may be high-significance but mission-local, highly persistent but low-significance, low in both, or high in both. Later conversions must not collapse those ideas into one label.

### Persistence and continuity doctrine

Actor records should support:
- `persistence_class`
- `operational_temporality`
- `replacement_logic`
- `resummonability`
- `identity_stability`
- `container_reuse_expectation`
- `reuse_portability_class`

Useful persistence classes may include:
- disposable
- replaceable
- resummonable
- recurring
- unique
- canon_anchor
- mission_local
- environment_bound
- site_bound
- frame_bound
- service_bound

Useful operational temporality classes may include:
- scene_limited
- encounter_limited
- mission_limited
- persistent_resident
- long_term_companion
- wave_based
- on_call
- duration_bound

### Reuse portability doctrine

Not every actor record should be equally portable across containers. Some are intended to be reused as-is. Others are thin shells expected to be localized by overlays, mission wrappers, sites, or faction context. Portability should therefore be declared rather than inferred.

- `reuse_portability_class` answers how broadly the record is intended to travel across contexts.
- `container_reuse_expectation` answers how much continuity stability the record expects when it does.

C02 must not leave these continuity assumptions implicit, because actor reuse behavior matters for revisions, bundles, conversions, and later canon consolidation.

## Body, presence, and scale profile

Actor entries need lawful places to declare what kind of embodied or manifested presence they have without re-owning movement or survivability doctrine from other files.

### Body and presence fields

Actor records should support:
- `body_configuration`
- `presence_profile`
- `occupancy_profile`
- `locomotion_basis`
- `targetability_profile`
- `materiality_state`
- `manifestation_mode`

### Scale doctrine

Actor scale should not be treated as one single undifferentiated measure.

Actor records should support at least:
- `body_scale`
- `occupancy_footprint`
- `operational_scale`
- `threat_scale`
- `social_or_institutional_scale` where relevant

This allows the schema to represent cases such as:
- a physically small actor with large information or command leverage
- a small actor with broad space-claiming or area-denial presence
- a large battle group with reduced individual identity
- a support familiar with low bodily presence but strong operational relevance
- an official or intermediary with low combat weight but high institutional consequence

These are declarative fields, not local mechanics definitions.

### Occupancy distinction note

`occupancy_profile` and `occupancy_footprint` are intentionally distinct.

- `occupancy_profile` describes how the actor occupies, shares, saturates, overlays, or otherwise uses space.
- `occupancy_footprint` describes the actor’s scale-oriented spatial claim or reach as a declarative footprint field.

This distinction is useful for swarms, clouds, diffuse entities, escort wings, giant bodies, and actor forms that are physically small but operationally space-claiming.

### Materiality and manifestation note

`materiality_state` and `manifestation_mode` should not be treated as duplicates. Materiality addresses embodiedness, tangibility, and targetability posture. Manifestation mode addresses how the actor is presently present, projected, anchored, phased, emitted, co-present, or conditionally present. These fields should remain distinct because some actors are embodied but conditionally targetable, while others are projected yet operationally persistent.

## Agency, autonomy, and command posture

A large donor pipeline will contain actors with radically different degrees of autonomy. C02 must represent that explicitly.

### Agency fields

Actor records should support:
- `agency_class`
- `command_dependency`
- `decision_bandwidth`
- `override_conditions`
- `control_channel`
- `bond_or_command_link`

Useful agency classes may include:
- fully_autonomous
- commanded
- partially_autonomous
- instinct_driven
- scripted
- hivemind_mediated
- rider_controlled
- faction_directed
- conditionally_sapient
- temporarily_overridden

### Control-channel versus bond-link note

`control_channel` and `bond_or_command_link` are related but not interchangeable.

- `control_channel` identifies the medium, pathway, mechanism, or interface by which control, guidance, or coordination is transmitted.
- `bond_or_command_link` identifies the underlying relationship, dependency basis, authority structure, or bond logic that makes that control meaningful.

### Controller-relationship doctrine

Controller relationships must not be flattened into one undifferentiated dependency. A controller link may be commanded, delegated, possessed, contract-bound, ritually bound, remote-piloted, bureaucratically assigned, AI-network directed, socially subordinate, or otherwise mediated. C02 does not need to solve controller mechanics, but it must preserve those distinctions structurally where they matter.

This is critical for:
- drones
- familiars
- summons
- charmed entities
- remotes
- battle groups
- bonded beasts
- linked constructs
- AI assistants

## Awareness, cognition, communication, and social tractability

C02 must not flatten all actors into humanoid assumptions.

### Awareness and cognition fields

Actor records should support:
- `sensory_profile`
- `awareness_profile`
- `cognition_profile`
- `uncertainty_handling_hooks`

### Communication fields

Actor records should support:
- `communicative_profile`
- `communication_channels`
- `signal_recognition_profile`
- `translation_or_symbolic_limits`

### Social tractability fields

Actor records should support:
- `social_tractability_profile`
- `negotiability_profile`
- `influenceability_profile`
- `standing_or_reputation_hooks` where relevant

### Communication versus social-tractability note

Communication answers whether and how the actor can exchange signals. Social tractability answers whether and how social pressure can meaningfully alter its behavior. These are related but not identical.

This separation matters because an actor may:
- perceive intelligently but be nonverbal
- communicate but not negotiate
- be socially legible but not socially influenceable
- recognize commands without possessing meaningful social posture
- calm or surrender without being a normal reasoning agent

### Standing and reputation note

`standing_or_reputation_hooks` are actor-entry hooks only. C02 does not own standing, reputation, leverage, or legitimacy procedure as such. Those logics remain governed by B10, B12, and any later relevant doctrine.

Authority, legitimacy, office, and formal standing that materially affect deployment, clearance, or legal posture should be hooked through the legality/access block below rather than duplicated here.

## Pressure, survivability, defeat, and resolution-state interface

C02 does not own survivability doctrine. B02 remains the governing survivability layer. C02 owns the actor-entry interface to that doctrine.

### Pressure and survivability interface fields

Actor records should support:
- `survivability_profile`
- `pressure_interface_hooks`
- `resistance_and_vulnerability_hooks`
- `condition_interface_hooks`
- `damage_family_hooks`
- `pressure_response_profile`
- `morale_commitment_discipline_hooks`
- `nonstandard_defeat_logic`
- `rout_or_break_logic` where relevant

### Pressure-response doctrine

Not every actor breaks the same way under pressure. Some rout, some surrender, some escalate, some disperse, and some become more dangerous. C02 should therefore preserve actor commitment, discipline, morale, or equivalent pressure-response posture where those distinctions matter.

### Resolution-state doctrine

Actor records must support more than a simple alive/dead assumption.

Useful actor resolution states may include:
- active
- impaired
- incapacitated
- routed
- dispersed
- surrendered
- broken
- destroyed
- banished
- deactivated
- dismissed
- captured
- scattered
- neutralized_recoverable
- escaped
- transformed_on_defeat

These states are especially important for:
- battle groups and swarms
- summoned entities
- remote or proxy actors
- constructs and drones
- capture-oriented encounters
- actors whose defeat changes site, mission, or faction state rather than simply ending in death

`possible_resolution_states` declares the actor-relevant reachable states that matter for this record. It does not redefine the underlying survivability or defeat doctrine owned elsewhere.

## Action, ability, and capability attachment doctrine

C02 does not redefine ability-object doctrine from A07. It defines how ability-bearing content attaches to actor entries.

### Capability attachment fields

Actor records should support:
- `ability_loadout`
- `action_expression_profile`
- `triggered_capabilities`
- `reaction_or_response_capabilities`
- `innate_capabilities`
- `contextual_capabilities`
- `capability_restriction_hooks`

C02 must allow actors to carry ability objects, action packages, trigger logic, and contextual capabilities without rewriting the lower doctrine those objects use.

## Equipment, frame, auxiliary, and dependency hooks

Some actors are inseparable from items, auxiliaries, mounts, remotes, or operational frames. C02 must support those links without absorbing neighboring families.

### Dependency hook fields

Actor records should support:
- `equipment_hooks`
- `item_dependency_hooks`
- `frame_dependency_hooks`
- `mount_or_platform_hooks`
- `auxiliary_links`
- `service_links`
- `controller_links`
- `site_dependency_hooks`
- `faction_dependency_hooks`

This lets an actor say, for example:
- it carries or requires certain items
- it depends on a frame or platform
- it is mounted on something else
- it commands auxiliaries or is commanded by them
- it is site-bound or institution-bound
without forcing C02 to own item, frame, or site doctrine.

## Ecology, support context, and environment hooks

Actor records are not just isolated stat-bodies. C02 therefore needs thin but explicit ecology and support-context hooks.

### Ecology and context fields

Actor records should support:
- `habitat_or_context`
- `support_context`
- `common_associations`
- `dependency_environment`
- `institutional_affiliation_hooks`
- `emission_or_spawn_context`
- `sustainment_requirements`

These fields are not lore bloat. They are structural hooks that help C02 interoperate with C06, C07, C10, and C12.

## Actor ingress, egress, and transformation states

C02 must support lawful representation of how actors enter, leave, and change state across scenarios, sites, encounters, generators, and transformations.

### Ingress/egress fields

Actor records should support:
- `starting_presence_state`
- `initial_operational_posture`
- `ingress_modes`
- `egress_modes`
- `deployment_hooks`
- `spawn_or_emission_hooks`
- `release_or_dismissal_hooks`
- `transformation_class`
- `transformation_paths`
- `source_state_links`
- `result_state_links`

Useful ingress/egress categories may include:
- resident
- wandering
- triggered
- spawned
- called
- deployed
- mounted
- released
- attached_to_frame
- emitted_by_site_or_hazard
- instantiated_by_generator
- promoted_from_group_state
- dissolved_to_source_state

Useful starting-presence or initial-posture categories may include:
- visible
- concealed
- dormant
- embedded
- patrolling
- socially_present
- summoned_ready
- inactive
- mounted
- delegated

### Transformation-class doctrine

Transformation handling should distinguish whether the transformation is primarily:
- a state shift
- a mode shift
- overlay-bearing
- derivative-producing
- output-producing

This distinction matters because some actors transform while preserving identity, while others transform into a new reusable content object or produce downstream output consequences.

This prevents later schemas from hiding entry and exit logic inside prose-only description.

## Group actors versus compositions

This is one of the most important routing boundaries in Batch C.

### Group actor rule

A group, mob, swarm, squad, or battle group remains a **C02 actor record** when it is represented and manipulated as **one acting entity with one stable record identity**.

### Composition rule

A scene roster, encounter roster, patrol roster, or packaged set of multiple distinct actors belongs to **C09 composition** when it is an assembly of distinct records rather than one actor identity.

### Practical distinction

- one swarm represented as one target/entity -> C02
- one battle group represented as one acting unit -> C02
- three different enemy records arranged into a fight packet -> C09
- one officer plus one escort group plus one hazard packaged together -> C09

C02 must preserve this boundary so actor abstractions do not collapse into encounter packet doctrine.

## Named adversaries versus generic actors

C02 must support both generic reusable actors and identity-heavy recurring actors without splitting them into different families.

### Generic actor expectations

Generic actors may be:
- lighter in provenance density
- lower in relationship density
- lower in continuity burden
- more overlay-friendly
- more generator-friendly

### Named or exceptional actor expectations

Named or exceptional actors may require:
- stronger identity stability
- richer relationship matrices
- stronger persistence and reuse assumptions
- stronger bundle pinning sensitivity
- stronger transformation or continuity tracking

The difference is not family ownership. It is schema depth and continuity expectation inside the same family.

## Actor versus site, faction, object, challenge, and frame boundary control

Large donor libraries will repeatedly pressure this boundary. C02 must therefore make it explicit.

### High-risk actor-adjacent edge classes

Examples of edge cases include:
- sentient site
- living environment
- actorized faction symbol
- personified object
- mobile city organism
- frame-bound intelligence
- projected avatar
- swarm-cloud hazard
- challenge-object with agency cues
- civic organism or site-mind
- environment-emitted actor
- actorized service system

### Routing rule

If the construct’s dominant function is **agency-bearing participation** in conflict, perception, social exchange, command, escort, pursuit, service-bearing agency, or direct pressure exchange, it may route to C02.

If the construct’s dominant function is primarily:
- place
- service environment
- governance body
- hazard/challenge structure
- infrastructure
- operational platform

then it should remain in C06, C07, C08, B15, or C05 as appropriate even if it presents actor-like traits.

Secondary dependencies may still be recorded, but dominant-function routing remains authoritative.

### Routing watch flags

Where a record sits near a family boundary, the actor entry may declare `routing_watch_flags` to indicate that conversion or review should pay special attention to site, frame, faction, challenge, infrastructure, or service-environment overlap.

This is not a second routing system. It is an audit-friendly caution field for high-pressure edge cases.

## Actor output and post-pressure hooks

C02 does not own reward parcel doctrine or post-pressure doctrine in the abstract. B16 and later C11 remain the governing files there. C02 owns the actor-entry hooks by which actors connect to those outputs.

### Actor-derived output fields

Actor records should support:
- `immediate_output_hooks`
- `deferred_output_hooks`
- `conditional_output_hooks`
- `post_pressure_output_hooks`
- `salvage_hooks`
- `capture_or_claim_hooks`
- `information_output_hooks`
- `social_leverage_hooks`
- `route_or_access_change_hooks`
- `evidence_or_proof_hooks`
- `contamination_or_escalation_hooks`
- `faction_fallout_hooks`
- `site_change_hooks`
- `auxiliary_release_hooks`
- `transformation_output_hooks`

Actors do not only output loot. They may output:
- salvage
- captives
- information
- leverage
- access changes
- contamination
- mission state changes
- faction consequences
- transformation into another state or record

Immediate, deferred, and conditional outputs should be distinguishable wherever timing materially affects later handling, interrogation, salvage, legal claim, ritual processing, or faction response.

## Required lower-doctrine handoffs

C02 must hand off to lower doctrine rather than rewriting it.

At minimum, actor entries should compose or reference:
- `C01` common record grammar
- `A04` stat architecture
- `A07` ability objects
- `A08` condition references
- `A09` damage families
- `A16` translation pattern library and edge-case discipline where relevant
- `B02` survivability framework
- `B08` uncertain perception and awareness doctrine
- `B10` social pressure/posture doctrine
- `B12` organized access / legality doctrine where relevant
- `B13` auxiliary entity doctrine where relevant
- `B14` operational frame doctrine where relevant
- `B15` civic environment doctrine where relevant
- `B16` post-pressure inflow doctrine

C02 may define actor-entry slots for these interfaces. It may not restate the governing doctrine as if C02 owns it.

## Required relationship patterns

C02 inherits C01 relationship grammar and must use explicit relationship structure rather than prose-only implication.

### Actor relationship matrix guidance

Actor records should be prepared to use relationships such as:
- `located_in`
- `controlled_by`
- `member_of`
- `emitted_by`
- `anchored_to`
- `variant_of`
- `opposed_by`
- `rewards_with`
- and other C01-governed relationship forms as needed for mount/platform linkage, command linkage, escort linkage, patrol linkage, inhabitation, event ties, or generator ties

These should be represented using C01 relationship structure, not invented locally as ad hoc prose logic.

## Variability, portability, and derivative thresholds

Actor records will vary in how fixed, modular, or overlay-friendly they are. C02 must support that explicitly.

### Variability fields

Actor records should support:
- `presentation_layer`
- `payload_density`
- `variability_posture`
- `overlay_intake_profile`
- `local_override_tolerance`
- `derivative_threshold_notes`
- `loadout_flexibility`
- `advancement_or_upgrade_hooks`

Useful presentation layers may include:
- minimal_actor_form
- standard_actor_form
- expanded_actor_form

Useful payload density categories may include:
- minimal
- standard
- dense

Useful variability categories may include:
- fixed
- modular
- selectable_loadout
- faction_skinned
- mission_skinned
- generator_driven
- upgrade_bearing
- advancement_bearing
- overlay_friendly
- local_only_variant

### Payload-density note

`payload_density` is a schema-expression choice, not a statement of narrative importance, threat, or boss status. A dense record is not automatically more important than a minimal one; it is simply carrying more structured schema expression.

### Overlay versus derivative rule

If a recurring change is better represented as a modifier or variant that preserves actor identity, it should hand off to C03 overlay logic.

If the change produces a new independently reusable actor with distinct continuity expectations, it may require derivative-record treatment under C01 revision doctrine.

C02 must support that distinction without swallowing overlay doctrine into the actor family itself.

## Actor legality, legitimacy, and access hooks

C02 does not own legality or access doctrine. It must still provide explicit entry hooks when those issues materially affect actor use, deployment, control, office, or relation status.

### Legality and access fields

Actor records should support:
- `access_requirements`
- `ownership_state`
- `bond_state`
- `legal_or_social_status`
- `restricted_use_class`
- `faction_or_clearance_dependency`
- `authority_or_legitimacy_hooks`

This matters not only for companions and drones, but also for retainers, contracted aid, controlled constructs, bound entities, restricted service actors, office-bearing actors, and similar donor constructs.

`authority_or_legitimacy_hooks` is authoritative here as the legal, institutional, office-bearing, or clearance-bearing side of authority posture. Social standing, reputation, and influence hooks remain actor-entry references in the social block above.

## Anti-collapse rules specific to actor records

C02 must not:
- become a generic bestiary or catalog
- restate B02 survivability law as if actor entries own it
- restate A07 ability doctrine as if actor entries own it
- absorb overlay logic that belongs to C03
- absorb encounter composition that belongs to C09
- absorb site logic that belongs to C06
- absorb faction logic that belongs to C07
- absorb challenge-object logic that belongs to C08
- flatten group actors and encounter packets into the same structure
- flatten named recurring actors and disposable generic actors into identical continuity assumptions
- force all actors into humanoid communication or social assumptions
- bury ingress, egress, transformation, or output logic in prose-only notes when those links are structurally important

## Reserved split note

Do not split C02 now.

If later corpus pressure proves the file genuinely unwieldy, the preferred reserved split pattern would be:
- `C02a_actor_core_and_solo_actor_schema`
- `C02b_group_swarm_and_battle_group_schema`
- `C02c_named_narrative_and_exceptional_actor_schema`

That split is reserved, not active.

## Minimal abstract actor template

The following template extends the C01 grammar with actor-family payload blocks. It is a family abstract template, not a converted instance.

```yaml
record:
  identity:
    canonical_id: ""
    record_name: ""
    display_name: ""
    record_class: "atomic_record"
    family_owner: "C02"
    alias_set: []
    visibility_stratum: ""
    field_visibility_overrides: []

  classification:
    ontology_state: "instantiated_record"
    lifecycle_state: "draft"
    dominant_function: "actor_content"
    secondary_functions: []
    content_family: "actor"

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
    primary_owner: "C02"
    secondary_dependencies: []
    authority_rank: "family_schema"
    governing_files: ["C01", "C02"]
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
    applicability_scope: ["actor_scale"]
    domains_of_use: []
    accepted_overlays: []
    emitted_overlays: []
    compatible_containers: []
    incompatible_contexts: []

  tags_and_indexing:
    family_tags: ["actor"]
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

  actor_profile:
    actor_modes: []
    ontological_posture: ""
    operational_role: ""
    narrative_significance_tier: ""
    allegiance_posture: ""
    persistence_class: ""
    operational_temporality: ""
    replacement_logic: ""
    resummonability: ""
    identity_stability: ""
    container_reuse_expectation: ""
    reuse_portability_class: ""
    routing_watch_flags: []

  body_presence_scale:
    body_configuration: ""
    presence_profile: ""
    occupancy_profile: ""
    locomotion_basis: []
    targetability_profile: ""
    materiality_state: ""
    manifestation_mode: ""
    body_scale: ""
    occupancy_footprint: ""
    operational_scale: ""
    threat_scale: ""
    social_or_institutional_scale: ""

  agency_command:
    agency_class: ""
    command_dependency: []
    decision_bandwidth: ""
    override_conditions: []
    control_channel: []
    bond_or_command_link: []

  cognition_communication_social:
    sensory_profile: []
    awareness_profile: ""
    cognition_profile: ""
    uncertainty_handling_hooks: []
    communicative_profile: ""
    communication_channels: []
    signal_recognition_profile: ""
    translation_or_symbolic_limits: []
    social_tractability_profile: ""
    negotiability_profile: ""
    influenceability_profile: ""
    standing_or_reputation_hooks: []

  pressure_survivability_resolution:
    survivability_profile: ""
    pressure_interface_hooks: []
    resistance_and_vulnerability_hooks: []
    condition_interface_hooks: []
    damage_family_hooks: []
    pressure_response_profile: ""
    morale_commitment_discipline_hooks: []
    nonstandard_defeat_logic: []
    rout_or_break_logic: []
    possible_resolution_states: []

  capability_attachment:
    ability_loadout: []
    action_expression_profile: ""
    triggered_capabilities: []
    reaction_or_response_capabilities: []
    innate_capabilities: []
    contextual_capabilities: []
    capability_restriction_hooks: []

  dependency_hooks:
    equipment_hooks: []
    item_dependency_hooks: []
    frame_dependency_hooks: []
    mount_or_platform_hooks: []
    auxiliary_links: []
    service_links: []
    controller_links: []
    site_dependency_hooks: []
    faction_dependency_hooks: []

  ecology_context:
    habitat_or_context: []
    support_context: []
    common_associations: []
    dependency_environment: []
    institutional_affiliation_hooks: []
    emission_or_spawn_context: []
    sustainment_requirements: []

  ingress_egress_transformation:
    starting_presence_state: ""
    initial_operational_posture: ""
    ingress_modes: []
    egress_modes: []
    deployment_hooks: []
    spawn_or_emission_hooks: []
    release_or_dismissal_hooks: []
    transformation_class: ""
    transformation_paths: []
    source_state_links: []
    result_state_links: []

  outputs_and_followons:
    immediate_output_hooks: []
    deferred_output_hooks: []
    conditional_output_hooks: []
    post_pressure_output_hooks: []
    salvage_hooks: []
    capture_or_claim_hooks: []
    information_output_hooks: []
    social_leverage_hooks: []
    route_or_access_change_hooks: []
    evidence_or_proof_hooks: []
    contamination_or_escalation_hooks: []
    faction_fallout_hooks: []
    site_change_hooks: []
    auxiliary_release_hooks: []
    transformation_output_hooks: []

  variability_profile:
    presentation_layer: ""
    payload_density: ""
    variability_posture: ""
    overlay_intake_profile: []
    local_override_tolerance: ""
    derivative_threshold_notes: []
    loadout_flexibility: ""
    advancement_or_upgrade_hooks: []

  legality_access_profile:
    access_requirements: []
    ownership_state: ""
    bond_state: ""
    legal_or_social_status: ""
    restricted_use_class: ""
    faction_or_clearance_dependency: []
    authority_or_legitimacy_hooks: []
```

## Final doctrine statement

C02 is the actor-family constitutional schema for Batch C.

It does not reduce actors to monster blocks.
It does not flatten group actors into encounter packets.
It does not absorb overlays, sites, factions, or missions.

Its purpose is to let Astra represent actor-content lawfully across a mixed donor corpus while preserving composition, routing discipline, revision stability, and cross-file interoperability.
