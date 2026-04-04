# batchC_06_site_region_settlement_and_locale_schema.md

## Purpose and authority

This file is the **site/place-content family schema authority** for Batch C.

Its job is to define the Astra-native entry structure for places: regions, sites, dungeons, settlements, districts, capitals, habitats, forts, enclaves, hunting grounds, trial locations, and locale-content entries generally. It is the family file that turns the common record grammar from C01 into a reusable place-family schema that can survive mixed donor pressure at corpus scale without collapsing into a lore chapter, mission file, faction file, or encounter packet.

C06 is not a setting encyclopedia. It is not a mission structure file. It is not a faction dossier. It is not an encounter-builder. It is not a civic-procedure file. It is not a travel-procedure file.

It owns:
- place/site-content record structure
- sitehood/placehood doctrine for Batch C
- place-family payload blocks on top of C01
- site modes and routing classes
- site mode versus site function versus site posture distinction
- place scale and partition doctrine
- nested-site and district/subsite doctrine
- site temporality doctrine
- site visibility and legibility posture
- topology and partition-type doctrine
- traversal and adjacency posture fields
- environmental-state and condition-facing hooks at entry-shape level
- service, infrastructure, support-shell, and survivability-envelope posture fields
- access, permission, and site-availability posture fields
- occupancy and linked-presence posture for sites
- control, contestation, lifecycle, and successor-state posture fields
- site origin/generation posture
- site output posture
- site memory and information-density posture
- place-specific boundary-control doctrine
- place-family relationship expectations
- place-family anti-collapse rules
- minimal abstract site/region/settlement/locale template

It does **not** own:
- traversal procedure doctrine already owned by B06
- environmental pressure/state doctrine already owned by B07
- service-availability procedure doctrine already owned by B11
- organized-access doctrine already owned by B12
- civic environment and infrastructure procedure already owned by B15
- actor-content entry structure already owned by C02
- frame/platform entry structure already owned by C05
- faction/institution entry structure already owned by C07
- challenge-object schema already owned by C08
- encounter composition already owned by C09
- mission/scenario structure already owned by C10
- live-play presentation behavior
- donor conversion instances as doctrine

## Why this file exists

Large donor corpora do not present place content as one uniform category. Some donors pressure toward wilderness regions and travel zones. Others pressure toward capitals, district-based cities, forts, dungeons, habitats, guild facilities, trial grounds, hunting ranges, hidden sanctums, quarantined sectors, or civic-platform hybrids.

Those constructs are neither:
- all simple map nodes,
- all mere atmosphere text,
- nor all reducible to actors, factions, or missions.

C06 exists because Astra requires one lawful family schema for place entries that can:
- distinguish place records from the people, missions, hazards, and organizations associated with them,
- preserve nested partitions and internal subsite structure,
- expose traversal, environmental, service, access, and civic hooks without re-owning Batch B procedures,
- distinguish permanent, temporary, hidden, emergent, cyclical, and successor-bearing locales,
- and route correctly when a construct is actually a frame/platform shell, faction body, challenge object, or scenario packet instead of a place record.

This file therefore treats the family center as **placehood and sitehood**, not as donor labels like city, dungeon, fort, district, wilderness, or habitat.

## Scope boundaries and exclusions

C06 covers content entries whose dominant doctrinal function is to exist as a place, locale, region, district, bounded subsite, habitat shell, or place-like environment that can be traversed, occupied, partitioned, serviced, controlled, accessed, conditioned, or linked to other places while remaining a reusable content object.

That includes, where they remain place-family content rather than actors, frames, factions, missions, or challenge objects:
- regions
- wilderness zones
- sites and locales
- dungeons and internal site complexes
- settlements and capitals
- districts, wards, quarters, sectors, and partitions
- habitats and support shells
- forts, enclaves, outposts, and bastions
- guild facilities, halls, depots, archives, and service sites
- hunting grounds and trial locations
- civic-platform hybrids when placehood remains primary
- place-based exceptional content

C06 excludes:
- organizations or institutions merely because they occupy or govern a place -> C07
- encounter packets or room-level fight assemblies -> C09
- missions or investigation structures that reference a place -> C10
- hazards/challenge objects even when embedded in a place -> C08
- operational platforms whose dominant identity remains framehood -> C05
- pure environmental overlays or local modifier layers -> C03

## Sitehood and placehood doctrine

A **place-family record** is a content record whose primary job is to represent a place, locale, or place-scale environment that can:
- be traversed, entered, exited, linked, or approached
- contain districts, subsites, sectors, or partitions
- host services, infrastructure, access channels, or local conditions
- persist as a reusable content object independent from any one mission, faction, or encounter
- support occupancy, control, contestation, or transformation without ceasing to be a place

Placehood does not require civilization.
Placehood does not require permanent settlement.
Placehood does not require neutrality.
Placehood does not require that the place be static in all respects.

Placehood is established by dominant function, not by donor naming convention.

## Site modes, functions, and posture doctrine

C06 must distinguish what kind of place something is from what it is primarily for and how it currently behaves.

### Core site modes

A place-family record may declare one or more site modes, with one marked primary where needed:
- `region`
- `wilderness_or_travel_zone`
- `bounded_site`
- `dungeon_or_internal_complex`
- `settlement`
- `capital_or_major_city`
- `district_or_partition`
- `habitat_or_support_shell`
- `fort_or_enclave`
- `facility_or_service_site`
- `hunting_ground_or_trial_site`
- `civic_platform_hybrid`
- `exceptional_locale`

### Mode guidance

- **region**: a broad place-scale record containing linked sites, settlements, or environmental bands.
- **wilderness_or_travel_zone**: a place record defined by movement, exposure, encounter pressure, or environmental traversal.
- **bounded_site**: a discrete locale with a meaningful boundary or identity.
- **dungeon_or_internal_complex**: a nested place record defined by internal partitions, sectors, rooms, levels, or linked subzones.
- **settlement**: an inhabited locale with place identity.
- **capital_or_major_city**: a settlement with major districting, service layering, and multi-body place pressure.
- **district_or_partition**: a subsite or internal place division that is independently meaningful.
- **habitat_or_support_shell**: a place-like shell that supports residence, services, or survivability.
- **fort_or_enclave**: a bounded defended or intentionally partitioned place.
- **facility_or_service_site**: a place record defined heavily by site-bound services or institutional operations without becoming the institution itself.
- **hunting_ground_or_trial_site**: a place record defined by challenge, testing, pursuit, ritual, or bounded pressure use.
- **civic_platform_hybrid**: a place whose locale identity is entangled with platform or shell logic but remains primarily place-owned.
- **exceptional_locale**: a significance-bearing place record with unusual continuity, scale, or boundary pressure.

### Dominant site functions

A place-family record should also support a `dominant_site_function` or `site_role_profile` distinction so mode does not have to carry every burden of meaning.

Useful site-function families include:
- `habitation`
- `trade_or_exchange`
- `transit_or_transfer`
- `administration_or_governance`
- `ritual_or_sanctity`
- `trial_or_testing`
- `extraction_or_harvest`
- `military_or_defense`
- `archive_or_knowledge`
- `medical_or_recovery`
- `industry_or_processing`
- `shelter_or_support`
- `secrecy_or_covert_operation`
- `research_or_observation`

### Site posture doctrine

Mode answers what broad kind of place this is.
Function answers what the place is primarily for.
Posture answers how the place is currently behaving or presented, such as open, hidden, quarantined, contested, ceremonial, active-service, abandoned, decaying, or emergent.

These axes should not be collapsed.

## Place scale, partition, containment, and scale-interoperability doctrine

This is one of the most important ownership zones in C06.

Astra must support place records at multiple scales without flattening regions, cities, facilities, districts, dungeons, and subsites into one undifferentiated location bucket.

### Scale and partition fields

Place-family records should support:
- `place_scale`
- `partition_profile`
- `partition_type_profile`
- `containment_profile`
- `internal_site_layers`
- `district_or_subsite_count_posture`
- `boundary_profile`

### Scale-interoperability doctrine

A place record may be both:
- a reusable atomic place entry in its own right,
- and a parent site or child subsite relative to other place entries.

This is not an edge case. It is a normal condition of large place hierarchies.

### Doctrine note

A region containing a city, a city containing districts, a district containing facilities, and a facility containing internal subsections are not optional edge cases. They are normal donor pressure.

C06 must therefore preserve partition and containment as first-class schema concerns rather than prose conveniences.

## Nested sites and district/subsite doctrine

The manifest explicitly requires support for nested sites and district partitions. C06 must therefore treat nested place structure as load-bearing rather than incidental.

### Nested-place fields

Place-family records should support:
- `parent_site_hooks`
- `child_site_hooks`
- `adjacent_partition_hooks`
- `cross_site_linkage_hooks`
- `districting_or_sectorization_profile`
- `internal_partition_navigation_hooks`

### Doctrine note

A place may be:
- a parent container for smaller places,
- a child site inside a larger region or city,
- a district among siblings,
- or a layered complex with internal sectors, decks, rings, rooms, wards, levels, or environmental bands.

Nested place records should remain linked by explicit relationships rather than being flattened into one giant lore block or scattered across unrelated mission notes.

## Site temporality doctrine

Large donor corpora contain places that are real enough to be records but not all present in the same way.

### Temporality fields

Place-family records should support:
- `site_temporality_profile`
- `appearance_cycle_hooks`
- `instancing_or_event_bound_hooks`
- `decay_or_recurrence_hooks`

### Useful temporality classes

Useful classes may include:
- `persistent`
- `periodic`
- `event_bound`
- `emergent`
- `decaying`
- `migratory`
- `instanced`
- `seasonal`
- `conditionally_manifest`

### Doctrine note

A shifting dungeon, summoned sanctum, trial ground that opens on a cycle, emergency shelter zone, reclaimed ruin, or anomaly pocket is still a place-family pressure. Temporality should therefore be explicit rather than hidden in notes.

## Site visibility and legibility posture

C06 does not own perception or investigation procedure, but it does need site-side declaration that a place may be obvious, hidden, mapped, obscured, rumor-known, or only legible under certain conditions.

### Visibility and legibility fields

Place-family records should support:
- `site_visibility_profile`
- `site_legibility_profile`
- `mapping_or_charting_posture`
- `knowledge_gating_hooks`
- `concealment_or_false_front_hooks`

### Doctrine note

This supports hidden districts, covert installations, undercities, occult sanctums, encrypted facilities, phased locales, and false sanctuary sites without forcing those behaviors into mission or hazard files.

## Topology and partition-type doctrine

Traversal and adjacency are necessary, but for a donor corpus this large Astra also needs a thin doctrine for what kind of topology a site has.

### Topology fields

Place-family records should support:
- `site_topology_class`
- `flow_profile`
- `verticality_or_layering_profile`
- `recursive_or_shifted_topology_hooks`

### Useful topology classes

Useful classes may include:
- `mesh_like`
- `branch_like`
- `ring_like`
- `depth_layered`
- `open_region`
- `compartmental`
- `phase_shifted`
- `access_keyed`
- `recursive`

### Partition-type doctrine

Partitions may be civic, environmental, security-based, ritual, functional, topological, vertical, concentric, ownership-based, or condition-based. C06 should preserve that difference explicitly rather than treating all districting as one category.

## Traversal and adjacency posture hooks

C06 does not own traversal procedure. It does need entry-shape hooks for traversal and adjacency.

### Traversal fields

Place-family records should support:
- `traversal_profile`
- `approach_or_entry_posture`
- `exit_or_departure_posture`
- `adjacency_profile`
- `route_link_hooks`
- `local_mobility_constraints`

### Doctrine note

A place may be easy to enter but hard to leave, easy to traverse but hard to approach, navigable only through gates or portals, or linked to neighboring places through restricted or hazardous routes. C06 should expose those postures without becoming B06 procedure doctrine.

## Environmental-state and condition-facing hooks

C06 does not own environmental procedure. It must still provide lawful site-side hooks.

### Environmental fields

Place-family records should support:
- `environmental_state_hooks`
- `hazard_pressure_hooks`
- `ambient_condition_profile`
- `stability_or_volatility_profile`
- `environmental_transition_hooks`

### Doctrine note

A place may be flooded, corrupted, sealed, irradiated, sanctified, blighted, storm-active, unstable, breathable, hostile, or otherwise conditioned without ceasing to be a place record. C06 should expose those site-side conditions without absorbing B07 or C08.

## Service, infrastructure, support-shell, and survivability-envelope posture

Many places matter structurally because of what they provide, not only because of where they are.

### Service and infrastructure fields

Place-family records should support:
- `service_availability_hooks`
- `infrastructure_profile`
- `support_shell_posture`
- `survivability_envelope_profile`
- `lodging_or_respite_hooks`
- `transport_or_transfer_service_hooks`
- `trade_or_supply_hooks`
- `mission_or_task_board_hooks`
- `repair_or_processing_service_hooks`
- `civic_support_output_hooks`

### Site service versus institutional service doctrine

C06 should answer what services are materially present or reachable here.
C07 and B12 should answer who controls them, who may use them, and under what legitimacy or permission.

This distinction must remain explicit so guild halls, ports, shrines, clinics, archives, embassies, and corporate campuses do not collapse site-side service presence into institution-side authority logic.

### Survivability-envelope doctrine

Some sites are defined partly by creating the conditions that make ordinary life, activity, or survival possible.

This may include:
- breathable atmosphere
- pressure shielding
- radiation protection
- thermal stability
- ritual sanctity
- contamination exclusion
- structural sheltering

These are place-side hooks, not a replacement for B15 or C05 shell doctrine.

### Doctrine note

A guild hall, port district, shrine complex, archive, hospital, fort, or city district may be structurally important because it provides lodging, portal transfer, mission intake, trade, repair, registration, or civic support. These functions should be explicit site-side hooks, not decorative prose.

## Access, permission, and site-availability posture

C06 does not own organized-access doctrine. It must still expose site-bound access posture.

### Access and permission fields

Place-family records should support:
- `access_channel_hooks`
- `entry_restriction_profile`
- `permission_or_clearance_hooks`
- `public_private_contested_posture`
- `availability_profile`

### Doctrine note

A place may be public, restricted, licensed, faction-gated, conditionally open, sealed, quarantine-bound, mission-gated, or politically contested. These are place-entry hooks, not replacements for B12 access logic.

## Occupancy classes and linked presence posture

Places contain presences, but they are not identical to those presences.

### Occupancy fields

Place-family records should support:
- `persistent_population_hooks`
- `transient_traffic_hooks`
- `mission_scale_presence_hooks`
- `embedded_institution_hooks`
- `garrison_or_defense_presence_hooks`
- `auxiliary_or_service_presence_hooks`
- `quarantine_or_exclusion_presence_hooks`
- `hidden_or_latent_presence_hooks`
- `linked_actor_faction_challenge_hooks`

### Doctrine note

A fortress, city district, ruin, port, hunting ground, undercity, and shrine complex may all be occupied, but not in the same way. Occupancy class should therefore be explicit rather than flattened into a generic resident/transient split.

## Control posture, persistence, lifecycle, and successor-state doctrine

A place can change state without ceasing to be itself.

### Control and lifecycle fields

Place-family records should support:
- `site_persistence_profile`
- `site_control_posture`
- `control_or_contestation_hooks`
- `occupation_or_clearance_state`
- `development_or_ruin_posture`
- `site_lifecycle_posture`
- `transformation_or_successor_state_hooks`

### Control-posture doctrine

Useful control postures may include:
- `sovereign`
- `neutral`
- `leased`
- `occupied`
- `besieged`
- `quarantined`
- `abandoned`
- `watched`
- `sacred`
- `disputed`
- `franchised`
- `faction_zoned`
- `partially_controlled`

### Lifecycle and successor-state doctrine

Useful lifecycle or successor pressures may include:
- renovation
- downgrade
- collapse
- corruption
- evacuation
- sanctification
- reclamation
- repurposing
- partition loss
- service outage
- merger into a larger locale
- reduction into challenge- or mission-facing residue

### Doctrine note

A city district can be occupied, evacuated, fortified, quarantined, or burned.
A dungeon can be cleared, collapsed, flooded, sanctified, or resealed.
A region can be opened, blighted, pacified, cut off, or reclaimed.

C06 therefore needs place-state and transformation posture broad enough to survive later donor pressure without becoming a mission or challenge file.

## Site origin and generation posture

Some places are natural, some built, some reclaimed, some emitted, some grown, some maintained by machines, and some are the stable residue of a process or event.

### Origin fields

Place-family records should support:
- `site_origin_profile`
- `generation_or_maintenance_hooks`
- `residue_or_event_origin_hooks`

### Doctrine note

This helps Astra represent natural wilderness zones, constructed forts, grown habitats, machine-maintained cities, sanctified shrines, emitted challenge zones, crashed stations reused as locales, and similar mixed-origin sites without relying on prose.

## Site output posture

Places can matter not only because they contain things, but because they emit services, opportunities, pressures, and downstream state changes.

### Output posture fields

Place-family records should support:
- `service_outputs`
- `access_outputs`
- `mission_intake_outputs`
- `extraction_or_harvest_outputs`
- `hazard_or_risk_outputs`
- `successor_state_outputs`

### Doctrine note

C06 should not cannibalize C10 or C11. It should still provide lawful place-side hooks for support, access, mission intake, extraction opportunity, risk, and successor-state pressures that naturally emerge from sites.

## Site memory and information-density posture

C06 should not become an investigation file. It does, however, help to declare what kinds of information pressure a place naturally supports.

### Memory and information fields

Place-family records should support:
- `site_memory_profile`
- `information_density_profile`
- `archive_or_record_hooks`
- `rumor_or_signage_hooks`
- `historical_layering_hooks`

### Doctrine note

This is useful for ruins, archives, capitals, laboratories, faction hubs, and mystery-heavy sites without pulling B09-style investigation behavior into C06.

## Place versus frame, faction, mission, encounter, and challenge boundary control

This is the most important routing section in the file.

### Place versus faction rule

If the content’s dominant identity is an organization, institution, guild, sect, polity, embassy, or social body, route pressure first to C07 even if that body is strongly associated with a place.

A guild hall is a site.
The guild that runs it is not.

### Place versus mission rule

If the content’s dominant identity is an operational objective structure, investigation flow, heist plan, crawl structure, or scenario container, route pressure first to C10.

A mission may reference a site.
A site does not become a mission because objectives happen there.

### Place versus encounter rule

If the content’s dominant identity is a packaged scene, fight, roster assembly, or encounter composition, route pressure first to C09.

A room, district, or hunting ground may host encounters.
It is not itself an encounter packet.

### Place versus challenge rule

If the content’s dominant identity is a trap, hazard object, puzzle, trial mechanism, or setpiece challenge object, route pressure first to C08 even if it is embedded in a place.

### Place versus frame rule

If the content’s dominant identity is operational platformhood, carriage, deployment, docking, launch, or chassis-scale hosting, route pressure first to C05.

If the content’s dominant identity is locale identity, districting, place-based navigation, civic layering, habitat persistence, or site-scale service shell, route pressure first to C06.

### Paired place-frame doctrine

Some constructs are best represented through paired linked records:
- a **place/locale shell** in C06
- and a **platform/frame shell** in C05

This paired-record approach is appropriate when:
- placehood is independently load-bearing,
- platformhood is also independently load-bearing,
- and either side would be distorted if reduced to a thin secondary note.

This is not multi-owner collapse and not a sign that Astra is confused. It is a controlled paired-representation pattern for civic-platform hybrids, moving city-shells, habitat-stations, fortress-platforms, or similar edge cases whose donor construction genuinely carries two independently load-bearing identities.

### High-risk edge classes

Examples of site-adjacent edge cases include:
- mobile capital
- station-habitat hybrid
- sentient city shell
- living environment
- civic organism or site-mind
- ritualized trial-zone that behaves like a challenge-object mesh
- organization-owned command complex
- frame-platform that functions as a districted habitat
- service shell emitted or maintained by another platform or hazard

C06 should preserve routing discipline for these cases rather than accepting donor labels at face value.

## Required relationship patterns

C06 inherits C01 relationship grammar and must use explicit relationship structure rather than prose-only implication.

### Place-family relationship guidance

Place-family records should be prepared to use relationships such as:
- `contains`
- `located_in`
- `anchored_to`
- `gated_by`
- `member_of`
- `emitted_by`
- `variant_of`
- `rewards_with`
- and other C01-governed relationship forms as needed for parent/child sites, district adjacency, route links, service links, control links, or paired place-frame relationships

These should be represented using C01 relationship structure, not invented locally as ad hoc prose logic.

## Required lower-doctrine handoffs

C06 must hand off to lower doctrine rather than rewriting it.

At minimum, place-family entries should compose or reference:
- `C01` common record grammar
- `B06` traversal doctrine
- `B07` environmental pressure/state doctrine
- `B11` service availability doctrine
- `B12` organized access / legality doctrine where site access materially matters
- `B15` civic environment and infrastructure doctrine
- the appropriate Batch C family file when the place interfaces with actors, frames, factions, challenge objects, encounter packets, or missions

C06 may define entry-shape hooks for these interfaces. It may not restate the governing doctrine as if C06 owns it.

## Anti-collapse rules specific to place-family records

C06 must not:
- become a lore encyclopedia or setting chapter
- become a faction dossier because organizations are associated with places
- become a mission file because objectives happen there
- become an encounter packet because fights happen there
- become a challenge file because hazards are embedded in a location
- become a stealth civic-procedure file by restating B15
- flatten region, city, district, facility, dungeon, and subsite into one undifferentiated location blob
- absorb neighboring family ownership merely because donor material uses one noun for a place, a government, and a mission hub

### Setting-chapter-by-accumulation warning

Repeated historical, cultural, political, or atmospheric notes should not silently become place ontology unless they materially affect partitioning, traversal, access, service posture, occupancy, control, persistence, or other schema-owned place behavior.

This warning exists to stop lore gravity from slowly bloating the family.

## Reserved split note

Do not split C06 now.

If later corpus pressure proves the file genuinely unwieldy, the preferred reserved split pattern would be:
- `C06a_place_core_and_scale_partition_schema`
- `C06b_service_access_and_infrastructure_schema`
- `C06c_nested_complex_and_place_boundary_control_schema`

That split is reserved, not active.

## Minimal abstract site/region/settlement/locale template

The following template extends the C01 grammar with place-family payload blocks. It is a family abstract template, not a converted instance.

```yaml
record:
  identity:
    canonical_id: ""
    record_name: ""
    display_name: ""
    record_class: "atomic_record"
    family_owner: "C06"
    alias_set: []
    visibility_stratum: ""
    field_visibility_overrides: []

  classification:
    ontology_state: "instantiated_record"
    lifecycle_state: "draft"
    dominant_function: "place_content"
    secondary_functions: []
    content_family: "site"

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
    primary_owner: "C06"
    secondary_dependencies: []
    authority_rank: "family_schema"
    governing_files: ["C01", "C06"]
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
    applicability_scope: ["site_scale"]
    domains_of_use: []
    accepted_overlays: []
    emitted_overlays: []
    compatible_containers: []
    incompatible_contexts: []

  tags_and_indexing:
    family_tags: ["site"]
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

  place_profile:
    site_modes: []
    dominant_site_function: ""
    site_posture_profile: ""
    place_scale: ""
    partition_profile: ""
    partition_type_profile: []
    containment_profile: ""
    internal_site_layers: []
    district_or_subsite_count_posture: ""
    boundary_profile: ""
    site_temporality_profile: ""
    appearance_cycle_hooks: []
    instancing_or_event_bound_hooks: []
    decay_or_recurrence_hooks: []

  nested_structure:
    parent_site_hooks: []
    child_site_hooks: []
    adjacent_partition_hooks: []
    cross_site_linkage_hooks: []
    districting_or_sectorization_profile: ""
    internal_partition_navigation_hooks: []
    site_topology_class: ""
    flow_profile: ""
    verticality_or_layering_profile: ""
    recursive_or_shifted_topology_hooks: []

  traversal_and_adjacency:
    traversal_profile: ""
    approach_or_entry_posture: ""
    exit_or_departure_posture: ""
    adjacency_profile: ""
    route_link_hooks: []
    local_mobility_constraints: []
    site_visibility_profile: ""
    site_legibility_profile: ""
    mapping_or_charting_posture: ""
    knowledge_gating_hooks: []
    concealment_or_false_front_hooks: []

  environment_and_condition:
    environmental_state_hooks: []
    hazard_pressure_hooks: []
    ambient_condition_profile: ""
    stability_or_volatility_profile: ""
    environmental_transition_hooks: []

  service_and_infrastructure:
    service_availability_hooks: []
    infrastructure_profile: ""
    support_shell_posture: ""
    survivability_envelope_profile: ""
    lodging_or_respite_hooks: []
    transport_or_transfer_service_hooks: []
    trade_or_supply_hooks: []
    mission_or_task_board_hooks: []
    repair_or_processing_service_hooks: []
    civic_support_output_hooks: []

  access_and_permission:
    access_channel_hooks: []
    entry_restriction_profile: ""
    permission_or_clearance_hooks: []
    public_private_contested_posture: ""
    availability_profile: ""

  occupancy_and_linked_presence:
    persistent_population_hooks: []
    transient_traffic_hooks: []
    mission_scale_presence_hooks: []
    embedded_institution_hooks: []
    garrison_or_defense_presence_hooks: []
    auxiliary_or_service_presence_hooks: []
    quarantine_or_exclusion_presence_hooks: []
    hidden_or_latent_presence_hooks: []
    linked_actor_faction_challenge_hooks: []

  persistence_and_control:
    site_persistence_profile: ""
    site_control_posture: ""
    control_or_contestation_hooks: []
    occupation_or_clearance_state: ""
    development_or_ruin_posture: ""
    site_lifecycle_posture: ""
    transformation_or_successor_state_hooks: []

  origin_and_generation:
    site_origin_profile: ""
    generation_or_maintenance_hooks: []
    residue_or_event_origin_hooks: []

  output_posture:
    service_outputs: []
    access_outputs: []
    mission_intake_outputs: []
    extraction_or_harvest_outputs: []
    hazard_or_risk_outputs: []
    successor_state_outputs: []

  memory_and_information:
    site_memory_profile: ""
    information_density_profile: ""
    archive_or_record_hooks: []
    rumor_or_signage_hooks: []
    historical_layering_hooks: []
```

## Final doctrine statement

C06 is the place/site-family constitutional schema for Batch C.

It does not reduce the family to map nodes or settlements.
It does not collapse places into factions, missions, encounters, or hazards.
It does not become a stealth lore chapter or civic procedure file.
It does not absorb neighboring ownership merely because donor material uses one noun for a place, a government, and a mission hub.

Its purpose is to let Astra represent regions, sites, settlements, districts, dungeons, habitats, and locale-content entries lawfully across a mixed donor corpus while preserving nested structure, function, temporality, topology, service/access posture, place-state continuity, and cross-file interoperability.

