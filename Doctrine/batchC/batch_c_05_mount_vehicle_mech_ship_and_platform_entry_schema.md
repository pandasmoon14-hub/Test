# batchC_05_mount_vehicle_mech_ship_and_platform_entry_schema.md

## Purpose and authority

This file is the **frame/platform-content family schema authority** for Batch C.

Its job is to define the Astra-native entry structure for operational frames: mounts, vehicles, mechs, ships, stations, mobile platforms, and platform-scale entries generally. It is the family file that turns the common record grammar from C01 into a reusable frame/platform schema that can survive mixed donor pressure at corpus scale without collapsing into a driving chapter, combat subsystem file, item-module catalog, or stealth site schema.

C05 is not a procedure file for how frames operate. It is not a vehicular combat chapter. It is not a garage or hangar catalog. It is not a second actor file. It is not a second item file. It is not a site/settlement file in disguise.

It owns:
- frame/platform-content record structure
- framehood/platformhood doctrine for Batch C
- frame-family payload blocks on top of C01
- frame modes and routing classes
- frame presentation-layer and payload-density doctrine
- frame-class versus operational-role distinction
- chassis/body/platform profile doctrine
- occupancy, pilot, crew, passenger, and autonomy posture fields
- station/staffing topology doctrine
- internal topology and compartment-hook doctrine
- integrated intelligence posture fields for frame entries
- system topology and mount/interface doctrine for frame entries
- scale, deployment, environment, and environment-transition profile fields
- protective-envelope, life-support, and habitation-shell posture hooks
- movement/travel/deployment posture hooks at entry-shape level
- frame readiness, damage-state, repair-facing, sustainment-facing, and operational-state hooks
- carried/hosted actor, item, auxiliary, cargo, payload, and service dependency hooks
- frame-specific derivative-threshold and boundary-control doctrine
- frame-family relationship expectations
- frame-family anti-collapse rules
- minimal abstract frame/platform template

It does **not** own:
- frame operation procedure doctrine already owned by B14
- civic/site-shell doctrine already owned by B15 and C06
- overlay/template doctrine already owned by C03
- ordinary item/component entry structure already owned by C04
- actor-content entry structure already owned by C02
- faction/institution entry structure already owned by C07
- encounter composition already owned by C09
- reward parcel packaging already owned by C11
- live-play presentation behavior
- donor conversion instances as doctrine

## Why this file exists

Large donor corpora do not present platform-scale content as one uniform category. Some donors pressure toward mounts and riding bodies. Others pressure toward ground vehicles, aircraft, ships, stations, modular mechs, mobile bases, deployable artillery platforms, crewed transports, or semi-fixed operational shells.

Those constructs are neither:
- all ordinary items,
- all ordinary actors,
- nor all ordinary places.

C05 exists because Astra requires one lawful family schema for operational frames that can:
- distinguish platforms from carried gear and installable components,
- preserve separation between frame identity and occupant identity,
- distinguish mobile operational platforms from locales and civic shells,
- expose B14-facing operation hooks without re-owning B14 procedure,
- and route correctly when a thing is actually an item, overlay, actor proxy, or site record instead of a frame.

This file therefore treats the family center as **framehood and platformhood**, not as donor labels like vehicle, mount, mech, ship, or station.

## Scope boundaries and exclusions

C05 covers content entries whose dominant doctrinal function is to exist as an operational platform or frame-scale host body with chassis-level identity, crew/pilot or autonomy posture, system topology, deployment relevance, and frame-scale handling.

That includes, where they remain frame-family content rather than items, actors, sites, or overlays:
- riding mounts treated as operational host frames rather than simple creatures or gear
- civilian or military vehicles
- walkers, mechs, and exoshell platforms
- aircraft and atmospheric craft
- voidcraft and ships
- stations and station-scale operational platforms
- mobile batteries, transports, siege rigs, or equivalent platforms
- semi-fixed or anchored platforms whose dominant function remains operational framehood rather than sitehood
- research, medical, industrial, logistical, diplomatic, utility, or habitat-support platforms when operational framehood remains primary
- frame-based exceptional content

C05 excludes:
- ordinary carried, installable, or socketed items whose dominant identity remains atomic itemhood -> C04
- pure modifier layers, upgrades, or status packages that primarily alter a frame -> C03
- actor entries merely because they occupy or pilot a frame -> C02
- locales, settlements, habitats, or civic shells whose dominant identity is place -> C06
- organizations or fleets as social/institutional bodies -> C07
- encounter packets containing several frames and occupants -> C09
- frame operation procedure, travel procedure, or repair/requisition procedure -> B14/B05

## Framehood and platformhood doctrine

A **frame-family record** is a content record whose primary job is to represent an operational platform, chassis, or frame-scale host body that can:
- be piloted, crewed, remotely operated, inhabited, mounted, or otherwise occupied
- host systems, mounts, bays, channels, subsystems, or compartments
- participate in movement, transport, conflict, deployment, service, or platform-scale operation
- persist as a reusable content object independent from any one occupant
- exist at a scale or systems-density that exceeds ordinary item-family treatment

Framehood does not require full autonomy.
Framehood does not require full sitehood.
Framehood does not require that the platform be purely mobile.
Framehood does not require combat primacy.

Framehood is established by dominant function, not by donor naming convention.

## Frame presentation layers and payload density

C05 must support both lightweight frame records and dense platform records without forcing every mount, skiff, walker, corvette, station, or mobile shell into the same depth of expression.

### Presentation layers

Useful presentation layers include:
- `minimal_frame_form`
- `standard_frame_form`
- `expanded_frame_form`

### Payload-density doctrine

`payload_density` is a schema-expression choice, not a statement of narrative importance, power, or prestige.

A simple rideable vehicle, courier skiff, or field buggy may legitimately use a minimal expression.
A systems-dense mech, warship, carrier, station, or civic-pressure shell may legitimately require an expanded expression.

This distinction exists so C05 can absorb both light vehicle donors and heavily systems-rich frame donors without architectural distortion.

## Frame modes and routing classes

C05 must support different platform types without splitting them into unrelated families.

### Core frame modes

A frame-family record may declare one or more frame modes, with one marked primary where needed:
- `mount_frame`
- `ground_vehicle`
- `air_vehicle`
- `water_or_submersible_vessel`
- `voidcraft_or_ship`
- `mech_or_walker_frame`
- `station_or_fixed_platform`
- `mobile_platform`
- `semi_fixed_operational_shell`
- `exceptional_frame_or_platform`

### Mode guidance

- **mount_frame**: a riding or carried operational host body whose dominant role is to host movement, carriage, or mounted action.
- **ground_vehicle**: a surface-going vehicle platform.
- **air_vehicle**: an aircraft or aerial platform.
- **water_or_submersible_vessel**: a waterborne or submerged platform.
- **voidcraft_or_ship**: a spacefaring vessel or comparable void-operational platform.
- **mech_or_walker_frame**: a chassis-focused combat or utility frame with occupant or systems-rich operation.
- **station_or_fixed_platform**: a platform whose primary identity is operational hosting rather than locale identity, despite partial fixity.
- **mobile_platform**: a transport, siege, industrial, support, or mission platform whose dominant identity is operational carriage or projection.
- **semi_fixed_operational_shell**: a borderline case that is partly anchored or place-like but remains primarily a frame.
- **exceptional_frame_or_platform**: a significance-bearing platform record with unusual continuity, scale, or derivative pressure.

## Frame class versus operational role doctrine

Frame mode answers **what kind of operational frame this is**.
Operational role answers **what function this frame is built or assigned to perform**.

A `voidcraft_or_ship` may serve as a courier, carrier, gunship, colony shell, survey vessel, prison transport, hospital platform, diplomatic ship, or refinery barge.
A `station_or_fixed_platform` may serve as a relay, port, archive, habitat-support shell, defense lattice, refinery, fortress, or medical platform.

These are not the same classification axis and should not be collapsed.

### Operational-role families

Useful operational-role families include:
- `transport`
- `combat`
- `logistics`
- `industrial`
- `survey_or_research`
- `medical_or_support`
- `command_or_control`
- `carrier_or_deployment`
- `diplomatic_or_ceremonial`
- `habitat_or_support_shell`
- `siege_or_emplacement`
- `utility_or_construction`

These are frame-role families, not operational procedures.

## Frame identity, continuity, and occupancy doctrine

C05 must keep frame identity separate from occupant identity.

### Identity and continuity fields

Frame-family records should support:
- `frame_identity_class`
- `continuity_profile`
- `occupancy_relation_profile`
- `pilotability_profile`
- `crew_dependency_profile`
- `autonomy_profile`
- `integrated_intelligence_posture`

### Doctrine note

A frame may persist across many pilots, crews, passengers, or mission contexts. A platform record is therefore not identical to its current occupant roster.

A mount is not merely its rider.
A mech is not merely its pilot.
A ship is not merely its crew.
A station is not merely its current staff.

Those relationships must stay explicit rather than collapsing frame and actor identity together.

### Integrated-intelligence posture

Some frames are only inert platforms. Others contain advisory systems, bonded intelligence, expert systems, ritual guidance minds, proxy-capable onboard intelligences, or linked independent minds.

`integrated_intelligence_posture` should therefore distinguish at least:
- `none`
- `tool_level_assistance`
- `advisory_intelligence`
- `proxy_capable_intelligence`
- `independent_linked_intelligence`

This does not convert the frame into a second actor record. It gives the frame a lawful way to declare when actor-side dependencies become structurally important.

## Chassis, body, and platform profile doctrine

C05 needs lawful places to describe what kind of platform a frame actually is.

### Chassis/body fields

Frame-family records should support:
- `chassis_profile`
- `body_configuration`
- `structural_profile`
- `platform_signature`
- `operational_role_profile`
- `environment_profile`

### Doctrine note

These are entry-shape fields, not local B14 procedure replacements. Their purpose is to let Astra represent the frame’s chassis identity, configuration, and intended operational role without restating the full operational rules that govern platform use.

Some donors will express extremely light frame records and some will express highly dense chassis records. C05 should allow both without implying that one is more canonically important than the other.

## Occupancy, pilot, crew, passenger, and autonomy doctrine

A large donor corpus will repeatedly pressure the distinction between:
- who a platform is,
- who is inside it,
- who is required to run it,
- and whether it can operate without them.

### Occupancy and staffing fields

Frame-family records should support:
- `minimum_operational_staffing`
- `preferred_staffing_profile`
- `maximum_occupancy_profile`
- `pilot_role_hooks`
- `crew_role_hooks`
- `passenger_or_embarked_capacity`
- `remote_operation_hooks`
- `autonomous_operation_hooks`
- `occupancy_change_posture`

### Station topology fields

Frame-family records should support:
- `required_operational_stations`
- `optional_stations`
- `exclusive_station_constraints`
- `shareable_station_rules`
- `role_clustered_station_groups`
- `automated_or_absent_station_profiles`

### Doctrine note

A frame may be:
- single-pilot,
- crew-dependent,
- remote-capable,
- semi-autonomous,
- passenger-carrying,
- actor-deploying,
- or staff-optional for some functions and staff-required for others.

C05 must preserve those distinctions at schema level without becoming a full operation procedure file.

## System topology and mount/interface doctrine

This is one of the most important C05 ownership zones.

Frame-family entries are often defined by what they can host and how those hosted systems are arranged.

### Topology and systems fields

Frame-family records should support:
- `system_topology_profile`
- `internal_layout_or_compartment_hooks`
- `mount_or_hardpoint_profile`
- `channel_or_bay_profile`
- `core_system_hooks`
- `capacity_hooks`
- `subsystem_intake_profile`
- `power_or_energy_hooks`
- `heat_stress_or_load_hooks`
- `repair_or_maintenance_hooks`
- `payload_or_cargo_hooks`

### Internal-topology doctrine

`system_topology_profile` covers systems arrangement, hardpoints, bays, channels, and major operational topology.

`internal_layout_or_compartment_hooks` exists for donor pressure where internal frame space matters structurally: bridges, decks, hangars, crew sections, exposed modules, breachable compartments, infirmaries, cargo sections, docking cells, or other operationally meaningful internal zones.

This does not make C05 an encounter-map file. It gives later content a lawful place to say that internal topology matters.

### Doctrine note

These fields do not replace C04 item/component entries or B14 operational rules. They define the frame-side grammar by which a platform says what kinds of subsystems, mounts, bays, power burdens, or payloads it can lawfully host.

## Scale, deployment, and environment profile doctrine

Frame-family records should not be forced into one undifferentiated size bucket.

### Scale and deployment fields

Frame-family records should support:
- `platform_scale`
- `deployment_scale`
- `crew_scale`
- `hosted_payload_scale`
- `mobility_envelope`
- `environmental_operating_band`
- `environment_transition_hooks`

### Doctrine note

A riding mount, a tank, a mech, a corvette, a station, and a mobile city-battery may all be frames, but they do not occupy the same operational scale. C05 needs lawful places for those distinctions without turning them into local rules prose.

### Environment-transition doctrine

Many frames are defined not only by where they can operate, but by how they change operational state between environments or deployment bands.

Examples include:
- docked to launched
- carrier-borne to independent
- atmosphere to orbit
- orbit to void
- surface to submersed
- sheltered berth to hostile medium
- anchored shell to mobile deployment

`environment_transition_hooks` exists so those transitions can be declared structurally rather than buried in prose.

### Protective-envelope and habitation-shell doctrine

Many frame records are also defined by whether they create or maintain a survivable operating envelope for their occupants, cargo, or hosted systems.

Frame-family records should therefore support:
- `protective_envelope_profile`
- `habitation_or_life_support_posture`
- `occupant_environmental_safety_hooks`

This is especially important for:
- voidcraft
- sealed crawlers
- submarine or pressure-bound shells
- walking city-shells
- station platforms
- breathable-sphere or shelter-generating platforms

These are frame-side entry hooks, not a replacement for site-service doctrine or full civic environment procedure.

## Movement, travel, and deployment posture hooks

C05 does not own movement or travel procedure in the abstract. It does need strong entry-shape hooks for movement and deployment posture.

### Movement and deployment fields

Frame-family records should support:
- `locomotion_profile`
- `travel_profile`
- `deployment_posture`
- `launch_dock_or_berth_hooks`
- `terrain_or_environment_constraints`
- `entry_exit_transfer_hooks`

### Doctrine note

This section exists so a frame can declare whether it is surface-bound, atmospheric, void-capable, docking-dependent, carrier-dependent, launch-dependent, terrain-limited, or otherwise deployment-conditioned without C05 absorbing full procedure ownership from B14 or neighboring files.

## Frame readiness, damage-state, repair-facing, sustainment-facing, and operational-state hooks

C05 must support broad platform-state expression without restating B14 operations.

### State and readiness fields

Frame-family records should support:
- `frame_readiness_profile`
- `operational_state_profile`
- `integrity_or_structure_state`
- `mobility_state`
- `system_availability_state`
- `power_state`
- `maintenance_state`
- `sustainment_posture`
- `repair_recovery_hooks`

### Frame-state families

C05 should expect at least these state families:
- readiness state
- structural/integrity state
- mobility state
- system state
- power state
- sustainment/support state
- docked/berthed/anchored state
- boarded/contested state where relevant

These do not all need separate procedures here. They do need lawful recognition at schema level.

### Sustainment doctrine

Some frames are defined as much by support burden as by chassis design.

`sustainment_posture` may need to expose pressures such as:
- fuel or consumable dependency
- crew support burden
- environmental shielding burden
- rearm or resupply burden
- sortie or mission endurance
- docking or service dependency

This helps distinguish, for example, short-range craft, long-endurance carriers, industrial crawlers, hospital platforms, and walking city-shells without turning C05 into an operation procedure file.

### Doctrine note

A frame may be operational, docked, disabled, partially functional, out of power, combat-damaged, maintenance-locked, sustainment-starved, or otherwise degraded without ceasing to exist as a frame record. C05 therefore needs state posture broad enough for vehicles, mechs, ships, mounts, and stations without becoming a repair procedure file.

## Carried, hosted, embarked, and serviced content doctrine

Frames often host more than one type of content.

### Hosted-content fields

Frame-family records should support:
- `embarked_actor_hooks`
- `hosted_item_or_subsystem_hooks`
- `auxiliary_or_drone_hooks`
- `service_function_hooks`
- `cargo_or_storage_hooks`
- `deployed_payload_hooks`

### Payload versus cargo versus deployed-payload distinction

- `payload_or_cargo_hooks` in the topology section addresses what kinds of payload or cargo burdens the frame is structurally built to host.
- `cargo_or_storage_hooks` here addresses goods, passengers, stock, supplies, reserves, or general carried/storage capacity.
- `deployed_payload_hooks` addresses entities, modules, craft, teams, batteries, pods, or mission components the frame can field, release, or deploy outward.

These fields are related but should not be collapsed. That distinction will matter heavily for carriers, drop ships, artillery transports, mobile labs, logistics shells, and support platforms.

### Doctrine note

A frame may carry actors, host items, deploy auxiliaries, provide services, carry cargo, or serve as a mission platform. These relationships should be explicit at entry shape level rather than improvised later inside encounter or mission prose.

## Frame versus actor, item, site, and overlay boundary control

This is the most important routing section in the file.

### Frame versus item rule

If the content’s dominant identity is an atomic object, component, upgrade, or installable entry that can meaningfully exist independently from one platform, route pressure first to C04.

If the content’s dominant identity is the operational chassis/platform that hosts systems, staffing, or deployment posture, route pressure to C05.

### Frame versus actor rule

If the content’s dominant identity is agency-bearing participation as an entity in its own right, route pressure first to C02.

If the content’s dominant identity is a platform that hosts, enables, or scales the action of occupants or onboard systems, route pressure to C05 even if the platform is tactically represented on the field.

### Frame versus site rule

If the content’s dominant identity is place, locale, district, habitat, or civic shell, route pressure first to C06/B15.

If the content’s dominant identity remains operational platformhood, deployment, transport, carriage, docking, launch, or frame-hosting function, it may remain in C05 even if it is large, semi-fixed, or partially habitat-like.

### Fixed-platform, semi-fixed-shell, and site-drift doctrine

A fixed or semi-fixed platform remains in C05 when operational hosting, deployment, carriage, docking, launch, mission-platform function, or platform-scale service function remains primary.

A record should drift toward C06/B15 when habitat persistence, districting, civilian persistence, civic service layering, place-based navigation, or locale identity become primary.

This is the main purpose of `site_drift_risk`. It is one of the most important long-term pressure seams in the file.

### Paired frame-site record doctrine

Some constructs are best represented not by forcing a single winner between C05 and C06, but by using paired linked records:
- a **frame/platform shell record** in C05
- and a **locale/civic shell record** in C06/B15

This paired-record approach is appropriate when:
- operational platformhood is independently load-bearing,
- locale/civic shell identity is also independently load-bearing,
- and either side would be distorted if reduced to a thin secondary note.

This is not an excuse for multi-owner collapse. It is a controlled paired-representation pattern for civic-platform hybrids, mobile capitals, habitat-stations, moving city-shells, and comparable donor constructs.

When used, the paired records should be linked explicitly through stable relationships and should each retain their own dominant-function ownership.

### Frame versus overlay rule

If the content’s primary identity is a reusable modification layer applied to a frame, route pressure to C03.

If the content’s primary identity is the frame itself, with modifications handled as overlays or subsystem dependencies, keep it in C05.

### High-risk edge classes

Examples of frame-adjacent edge cases include:
- living vehicle organism
- sentient ship
- city-crawler platform
- station-habitat hybrid
- frame-bound intelligence
- weaponized service shell
- mobile fortress
- deployable site-shell
- platform emitted by a site or hazard
- organization-owned command carrier

C05 should preserve routing discipline for these cases rather than accepting donor labels at face value.

## Hierarchical frame relationship doctrine

Large donor corpora will repeatedly pressure frame-on-frame and platform-network relationships.

### Hierarchical relationship note

C05 should expect relationships such as:
- docking relationships
- carrier or carriage relationships
- deployment relationships
- escort relationships
- towing or dragging relationships
- mounted-on relationships
- detachable section relationships
- section-of relationships
- port-or-station hosting relationships

These do not all need new C01 verbs immediately, but C05 should treat hierarchical frame relationships as normal pressure rather than exceptional edge cases.

## Frame-derived outputs and transition hooks

Frames can generate downstream consequences without C05 owning parcel doctrine.

### Output and transition fields

Frame-family records should support:
- `deployment_outputs`
- `transport_or_disembark_outputs`
- `salvage_or_recovery_outputs`
- `service_outputs`
- `hazard_or_disruption_outputs`
- `access_or_state_change_outputs`
- `destruction_or_disable_outputs`
- `transition_result_hooks`

### Output-class doctrine

Frames may generate:
- deployment outputs
- transport or embark/disembark outputs
- salvage outputs
- service disruption outputs
- hazard outputs
- access/state change outputs
- successor-state outputs

This helps distinguish wrecks, abandoned platforms, disabled stations, breached shells, scuttled ships, evacuated transports, and similar downstream states without converting C05 into C11.

### Doctrine note

A destroyed mech, scuttled ship, disabled transport, abandoned mount, or decommissioned station may yield salvage, evacuation states, mission changes, service disruption, or successor states. C05 should expose those possibilities without becoming C11.

## Variability, modularity, and derivative-threshold doctrine

Frame-family records vary in how fixed, modular, upgradable, and identity-stable they are.

### Variability fields

Frame-family records should support:
- `presentation_layer`
- `payload_density`
- `variability_posture`
- `modularity_profile`
- `upgrade_or_refit_profile`
- `occupant_dependence_risk`
- `site_drift_risk`
- `derivative_threshold_notes`

### Derivative-threshold doctrine

A frame-family record should be reviewed for derivative promotion or neighboring-family rerouting when one or more of the following become true:
- the modified form requires independent reuse apart from the base platform
- the frame now carries durable continuity distinct from the base record
- the platform has become primarily a locale or habitat rather than an operational frame
- the installed/system stack now defines a new independently meaningful frame identity
- occupant or organizational identity has become primary over platform identity
- the platform’s overlay/state chain now carries most of the relevant content payload

This matters especially for:
- awakened or living ships
- modular battle platforms that stabilize into new frame classes
- station-shells that become places first and platforms second
- body/frame fusions with inseparable pilot identity
- mobile city organisms or fortress-crawlers at the frame/site boundary

## Required relationship patterns

C05 inherits C01 relationship grammar and must use explicit relationship structure rather than prose-only implication.

### Frame-family relationship guidance

Frame-family records should be prepared to use relationships such as:
- `requires`
- `contains`
- `anchored_to`
- `located_in`
- `member_of`
- `gated_by`
- `emitted_by`
- `assembled_from`
- `variant_of`
- `instance_of`
- `rewards_with`
- and other C01-governed relationship forms as needed for embarkation, docking, subsystem hosting, service carriage, deployment chains, or hierarchical frame relationships

These should be represented using C01 relationship structure, not invented locally as ad hoc prose logic.

## Required lower-doctrine handoffs

C05 must hand off to lower doctrine rather than rewriting it.

At minimum, frame-family entries should compose or reference:
- `C01` common record grammar
- `B14` operational frame doctrine
- `B15` civic/service-shell doctrine where platform records pressure sitehood
- `B05` repair/requisition/crafting doctrine where frame records interface with maintenance or refit chains
- `B12` organized access / legality doctrine where ownership, docking, registration, or licensed operation materially matter
- `B13` auxiliary entity doctrine where frames host or deploy auxiliaries
- `B16` post-pressure inflow doctrine where frames become salvage or output sources
- the appropriate Batch C family file when the frame interfaces with actors, items, overlays, sites, factions, or encounter packets

C05 may define entry-shape hooks for these interfaces. It may not restate the governing doctrine as if C05 owns it.

## Anti-collapse rules specific to frame-family records

C05 must not:
- become a driving or vehicular combat chapter
- become a hangar catalog or sourcebook chapter
- become a second actor file because pilots act through frames
- become a second item file because frames host components
- become a site file because some platforms are large or semi-fixed
- restate B14 frame operation doctrine as if C05 owned it
- treat every upgrade, mount, or subsystem as local frame doctrine instead of routing to C03/C04 where appropriate
- flatten mounts, vehicles, mechs, ships, stations, and mobile platforms into one undifferentiated vehicle blob
- absorb neighboring family ownership merely because donor material uses the same noun for object, platform, and place

### Non-combat-facing doctrine note

Not all frame-family records are combat-facing. Research stations, carriers, transport shells, siege rigs, hospital ships, industrial crawlers, refinery barges, port platforms, and support shells all belong here when operational framehood remains primary.

## Reserved split note

Do not split C05 now.

If later corpus pressure proves the file genuinely unwieldy, the preferred reserved split pattern would be:
- `C05a_frame_core_and_mobile_platform_schema`
- `C05b_ship_station_and_large_platform_schema`
- `C05c_occupancy_system_topology_and_boundary_control_schema`

That split is reserved, not active.

### Civic-shell warning

The frame/site seam is expected to be the most likely long-term pressure point for future splitting or extra doctrine. Large platforms that increasingly behave like places should receive special scrutiny rather than being allowed to drift silently.

## Minimal abstract frame/platform template

The following template extends the C01 grammar with frame-family payload blocks. It is a family abstract template, not a converted instance.

```yaml
record:
  identity:
    canonical_id: ""
    record_name: ""
    display_name: ""
    record_class: "atomic_record"
    family_owner: "C05"
    alias_set: []
    visibility_stratum: ""
    field_visibility_overrides: []

  classification:
    ontology_state: "instantiated_record"
    lifecycle_state: "draft"
    dominant_function: "frame_content"
    secondary_functions: []
    content_family: "frame"

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
    primary_owner: "C05"
    secondary_dependencies: []
    authority_rank: "family_schema"
    governing_files: ["C01", "C05"]
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
    family_tags: ["frame"]
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

  frame_profile:
    frame_modes: []
    presentation_layer: ""
    payload_density: ""
    frame_identity_class: ""
    continuity_profile: ""
    occupancy_relation_profile: ""
    pilotability_profile: ""
    crew_dependency_profile: ""
    autonomy_profile: ""
    integrated_intelligence_posture: ""
    frame_site_interlock_profile: ""
    paired_locale_shell_hooks: []

  chassis_and_platform:
    chassis_profile: ""
    body_configuration: ""
    structural_profile: ""
    platform_signature: ""
    operational_role_profile: []
    environment_profile: []

  occupancy_and_staffing:
    minimum_operational_staffing: ""
    preferred_staffing_profile: ""
    maximum_occupancy_profile: ""
    pilot_role_hooks: []
    crew_role_hooks: []
    passenger_or_embarked_capacity: ""
    remote_operation_hooks: []
    autonomous_operation_hooks: []
    occupancy_change_posture: ""
    required_operational_stations: []
    optional_stations: []
    exclusive_station_constraints: []
    shareable_station_rules: []
    role_clustered_station_groups: []
    automated_or_absent_station_profiles: []

  system_topology:
    system_topology_profile: ""
    internal_layout_or_compartment_hooks: []
    mount_or_hardpoint_profile: []
    channel_or_bay_profile: []
    core_system_hooks: []
    capacity_hooks: []
    subsystem_intake_profile: []
    power_or_energy_hooks: []
    heat_stress_or_load_hooks: []
    repair_or_maintenance_hooks: []
    payload_or_cargo_hooks: []

  scale_and_deployment:
    platform_scale: ""
    deployment_scale: ""
    crew_scale: ""
    hosted_payload_scale: ""
    mobility_envelope: ""
    environmental_operating_band: []
    environment_transition_hooks: []
    protective_envelope_profile: ""
    habitation_or_life_support_posture: ""
    occupant_environmental_safety_hooks: []

  movement_and_travel:
    locomotion_profile: []
    travel_profile: ""
    deployment_posture: ""
    launch_dock_or_berth_hooks: []
    terrain_or_environment_constraints: []
    entry_exit_transfer_hooks: []

  readiness_and_state:
    frame_readiness_profile: ""
    operational_state_profile: ""
    integrity_or_structure_state: ""
    mobility_state: ""
    system_availability_state: ""
    power_state: ""
    maintenance_state: ""
    sustainment_posture: ""
    repair_recovery_hooks: []

  hosted_content:
    embarked_actor_hooks: []
    hosted_item_or_subsystem_hooks: []
    auxiliary_or_drone_hooks: []
    service_function_hooks: []
    cargo_or_storage_hooks: []
    deployed_payload_hooks: []

  outputs_and_transitions:
    deployment_outputs: []
    transport_or_disembark_outputs: []
    salvage_or_recovery_outputs: []
    service_outputs: []
    hazard_or_disruption_outputs: []
    access_or_state_change_outputs: []
    destruction_or_disable_outputs: []
    transition_result_hooks: []

  variability_and_derivative_risk:
    presentation_layer: ""
    payload_density: ""
    variability_posture: ""
    modularity_profile: ""
    upgrade_or_refit_profile: []
    occupant_dependence_risk: ""
    site_drift_risk: ""
    derivative_threshold_notes: []
```

## Final doctrine statement

C05 is the frame/platform-family constitutional schema for Batch C.

It does not reduce the family to ordinary vehicles.
It does not collapse platforms into actors, items, or places.
It does not become a stealth operation-procedure file.
It does not absorb neighboring ownership merely because donor material uses one label for a chassis, a crewed body, and a locale.

Its purpose is to let Astra represent operational frame/platform entries lawfully across a mixed donor corpus while preserving boundary control, occupant separation, chassis identity, subsystem topology, internal topology, sustainment posture, environment transitions, and cross-file interoperability.

