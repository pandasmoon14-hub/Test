# batchC_10_mission_scenario_arc_and_adventure_path_conversion_schema.md

## Purpose and authority

This file defines the **macro-playable composition schema** for Astra Ascension.

Its job is to define how Astra represents and composes **missions, scenarios, investigation structures, heists, crawls, trial sequences, operation chains, campaign arcs, adventure-path style continuities, and bounded open procedural shells** out of lower-level content schemas already owned elsewhere in Batch C.

This file is doctrine for **playable structure at and above mission scale**.
It does **not** define atomic content entries.
It does **not** define local encounter packets.
It does **not** define sourcebook packaging.
It does **not** define live-play adjudication behavior.

C10 exists because a 200–400 donor pipeline, and especially a 500+ donor pipeline, will contain many different forms of playable composition that cannot be safely collapsed into one generic “adventure” schema without structural loss, conversion drift, or donor-family overfitting.

C10 therefore owns the schema grammar for:
- objective-bearing macro structures
- progression-bearing macro structures
- branch-capable macro structures
- state-bearing macro structures
- successor-bearing macro structures
- reusable scenario templates and instantiated scenario structures
- authored, normalized, archetypal, and generated structure-form distinctions
- bounded open shells that are still scenario-scale rather than campaign-overlay scale

C10 remains **schema doctrine**, not converted output, not canon, and not a play-facing scenario generator.

## Relationship to Batch C authority

This file inherits:
- `batchC_00_manifest.md`
- `batchC_01_common_content_schema_conventions_and_record_grammar.md`

This file must remain consistent with the established Batch C family boundaries for:
- `batchC_02_actor_creature_npc_and_adversary_schema.md`
- `batchC_03_template_variant_overlay_and_modifier_schema.md`
- `batchC_04_item_relic_resource_and_asset_content_schema.md`
- `batchC_05_mount_vehicle_mech_ship_and_platform_entry_schema.md`
- `batchC_06_site_region_settlement_and_locale_schema.md`
- `batchC_07_faction_institution_polity_and_social_body_schema.md`
- `batchC_08_traps_hazards_puzzles_trials_and_setpiece_challenge_schema.md`
- `batchC_09_encounter_scene_packet_and_composition_schema.md`
- `batchC_11_reward_loot_salvage_claim_and_inflow_parcel_schema.md`
- `batchC_12_random_tables_events_oracles_and_generator_schema.md`
- `batchC_13_sourcebook_bundle_gazetteer_and_reference_container_schema.md`

If a donor structure cannot be represented cleanly as a normal C10 macro-composition without smuggling in a distinct campaign subsystem or overlay engine, that strain should be escalated toward the reserved `batchC_14_subsystem_packet_and_campaign_overlay_schema.md` rather than hidden inside C10.

C10 must also remain consistent with C01 identity, revision, derivative, and pinned-history discipline. Because mission/scenario/arc/path entries are especially vulnerable to quiet revision drift, this file must explicitly preserve distinctions such as:
- template identity vs instance identity
- scenario identity vs path-segment identity
- revision-in-place vs derivative continuity line
- pinned historical variant vs current normalized variant
- merged continuity structure vs split continuity structure

## Why C10 must exist

Packet-scale schema is not enough for corpus-scale conversion.

Astra must be able to convert, normalize, and later organize donor material such as:
- one-shot adventures
- multi-part modules
- mission chains
- adventure paths
- campaign arcs
- investigations
- heists
- crawls
- military operations
- political scenarios
- trial sequences
- survival structures
- procedural sandboxes
- table-assisted scenario shells
- blended narrative/operational supplements

These donor structures are not interchangeable.
A one-site crawl is not the same as a patron-issued mission.
A patron-issued mission is not the same as an investigation lattice.
An investigation lattice is not the same as a multi-scenario arc.
A campaign arc is not the same as a sourcebook bundle.
A repeatable mission board is not the same as one authored scenario.
A bounded open shell is not the same as an overlay-scale campaign engine.

Without C10, later conversion work will tend to fail in one of six ways:
1. treat local packets as full scenarios
2. treat sites as if they were adventures
3. treat campaign bundles as if they were one mission record
4. improvise donor-specific progression logic without doctrine ownership
5. mistake generator-backed intake shells for authored scenario structures
6. smuggle overlay-scale engines into ordinary mission fields

C10 exists to stop those failures.

## Core doctrinal center

The doctrinal center of C10 is:

**C10 owns the schema by which Astra represents larger playable content compositions that organize, sequence, gate, branch, loop lightly, reuse, and resolve lower-level content records over time.**

In Astra terms, C10 owns the structure of:
- what the playable macro-unit is
- what structural family it belongs to
- what function it serves
- what posture it takes toward openness, direction, and continuity
- what objectives or pressures govern it
- how it progresses
- where it branches
- what conditions gate movement through it
- what local packets and lower content records it assembles
- what states, burdens, and consequences it produces
- what successor structures it unlocks, alters, blocks, or hands off into

C10 is therefore about **macro-composition logic**.
It is not about the detailed content of the components being composed.

## What C10 owns

C10 owns:
- mission-scale and scenario-scale composition grammar
- arc-scale and path-scale continuity grammar
- composition family, composition function, and composition posture distinctions
- objective architecture above packet scale
- objective topology above packet scale
- stage, phase, and lightweight macro-loop architecture above packet scale
- branch, route-variant, state-divergence, and successor-divergence architecture
- entry, continuation, interruption, suspension, and termination condition grammar
- visibility and knowledge-posture grammar at macro scale
- macro pressure-source grammar
- successor-state and continuity-burden grammar
- reusable macro templates
- normalized archetypal structures
- instantiated scenario structures
- authored vs normalized vs generated structure distinctions
- local-to-macro linkage rules
- mission/scenario/arc/path family routing discipline

## What C10 does not own

C10 does **not** own:
- actor definitions
- adversary definitions
- site ontology
- locale topology details
- faction or institution ontology
- item or asset definitions
- challenge-object definitions
- encounter or scene packet definitions
- reward parcel definitions
- generator logic or random table procedure
- sourcebook, gazetteer, or bundle packaging
- campaign-level overlay subsystems that require their own packet architecture
- live-play pacing advice
- storywriting guidance
- module prose style
- adventure text formatting as publication output

## Scale ladder and macro-composition place in Batch C

For Batch C routing discipline, Astra should recognize the following scale ladder:

1. **Atomic content object**
   One actor, site, item, challenge object, faction entry, frame entry, or similar content unit.

2. **Overlay content object**
   A modifier package that alters another content object.

3. **Local composition object**
   An encounter, scene packet, or bounded local packet owned by C09.

4. **Mission-scale macro composition**
   A bounded operational playable unit with declared objective structure and outcome states.

5. **Scenario-scale macro composition**
   A larger playable structure whose flow may include multiple missions, multiple packets, open routing, investigation logic, or sustained state progression.

6. **Arc-scale macro composition**
   A persistent linked structure of multiple scenarios or missions with carry-forward continuity and successor-state logic.

7. **Adventure-path scale macro composition**
   A directed authored continuity structure made of multiple scenarios and/or arcs with explicit progression spine and branch handling.

8. **Container content object**
   A packaging object such as a bundle, gazetteer, dossier, compendium, or converted sourcebook grouping owned by C13.

C10 owns levels 4 through 7.
C10 may reference levels 1 through 3 and may be packaged by level 8, but it does not own them.

## Dominant-function routing rules

All candidate C10 content must be routed by **dominant structural job**, not by donor presentation style.

A record belongs in C10 when its main job is to define:
- macro progression
- objective flow
- branch logic
- stage logic
- phase or loop logic at lightweight macro scale
- scenario state
- continuity burden
- successor-state routing
- multi-packet composition

A record does **not** belong in C10 merely because it appears inside an adventure chapter.

If the dominant job is local packet composition, route to C09.
If the dominant job is site definition, route to C06.
If the dominant job is faction definition, route to C07.
If the dominant job is challenge-object definition, route to C08.
If the dominant job is reward packaging, route to C11.
If the dominant job is generator procedure, route to C12.
If the dominant job is content packaging or book-scale grouping, route to C13.
If the dominant job is a distinct subsystem overlay that ordinary scenario grammar cannot safely hold, escalate toward C14 reserve.

## Composition family, function, and posture

C10 must distinguish three different kinds of classification that donor texts often blur together.

### Composition family

Composition family identifies **what kind of macro structure** the record is.
Examples include mission, investigation scenario, crawl scenario, arc, or adventure path.

### Composition function

Composition function identifies **what the macro structure is for**.
Examples include:
- retrieval
- infiltration
- exploration
- survival
- qualification
- adjudication
- diplomacy
- suppression
- escort
- extraction
- legitimacy repair
- succession conflict
- ritual completion
- evacuation
- defense or hold
- search or revelation
- punitive operation
- claim or occupation

A crawl can serve retrieval, exploration, ritual completion, or survival.
A political scenario can serve diplomacy, adjudication, coercive leverage, or legitimacy repair.
A trial sequence can serve qualification, inheritance transfer, rank filtering, or access gating.

### Composition posture

Composition posture identifies **how the structure behaves** with respect to openness, direction, continuity, and boundedness.
Examples include:
- tightly bounded
- bounded-open
- semi-open operational shell
- continuity-bearing segment
- directed path segment
- revisitable lattice
- generator-fed intake shell
- state-reactive structure

Family, function, and posture must not be collapsed into one label.

Composition function and macro pressure source must also remain separate. Function explains what the structure is trying to accomplish. Pressure source explains what drives the structure forward, deforms it, constrains it, or escalates it while play moves through that structure. Retrieval, escort, qualification, or legitimacy repair are functions. Time pressure, exposure escalation, route collapse, reinforcement arrival, information scarcity, or access decay are pressure sources.

## Macro boundedness doctrine

C10 must preserve boundedness explicitly.
Many donor structures are neither fully linear nor fully open-world.

### Boundedness classes
- tightly bounded mission
- bounded open scenario
- semi-open operational shell
- continuity-bearing arc segment
- directed path segment
- open but jurisdictionally bounded sandbox shell

### Boundedness principles

1. Boundedness describes the outer limit of the structure, not whether internal routing is linear.
2. A bounded-open scenario may still have highly permissive internal routing.
3. A mission board shell may be bounded by jurisdiction, sponsor, region, or operation frame without being one single authored mission.
4. Open posture does not automatically imply overlay escalation.
5. Unbounded campaign governance belongs beyond normal C10 unless the donor still presents a bounded scenario shell.

## Key distinction set

### Mission

A **mission** is a bounded macro-playable structure organized around one operational purpose or one primary objective cluster.

A mission may:
- use one or more sites
- contain one or more local packets
- involve one or more organizations or stakeholders
- produce multiple outcomes
- branch locally
- persist across multiple sessions

A mission is still one mission if it remains one bounded operational ask.

### Scenario

A **scenario** is a larger playable flow structure that organizes one or more missions, one or more packet clusters, one or more loops, or one open progression shell into a coherent playable whole.

A scenario may be:
- one mission with strong internal branching
- multiple linked missions
- one investigation lattice
- one crawl structure
- one operation shell with multiple phases
- one open procedural shell with bounded scenario identity

Scenario is the broader structural class.
Mission is the more specific operational class.

### Arc

An **arc** is a persistent macro continuity structure linking multiple missions and/or scenarios through carry-forward state, recurrent pressures, continuity burdens, successor-state logic, and continuity-bearing consequences.

An arc is not merely “several missions in sequence.”
An arc requires persistence and cumulative continuity.

### Adventure path

An **adventure path** is a directed authored macro continuity structure that links multiple scenarios and/or arcs through an intended progression spine, successor logic, branch controls, fallback handling, and durable state handoffs.

Adventure path is more prescriptive than a loose arc and more structurally unified than a general campaign bundle.

### Module

A **module** is a donor publication or authored presentation form, not automatically a distinct Astra schema family.

A donor module may normalize into:
- one mission
- one scenario
- one arc
- one path segment
- several linked instances
- one template plus one or more instances
- a mixed structure containing several C10 units and container-facing C13 packaging

Module is therefore a provenance/presentation notion, not a primary Astra structural class.

### Macro-structure granularity

Macro-structure granularity is structural, not presentational. A donor chapter boundary is not authoritative merely because the book prints content that way. Depending on actual structure, Astra may need to normalize material as a segment, chapter-scale macro unit, operation package, path node, or scenario cluster. Those are granularity judgments about functional structure, not permissions to mirror donor layout one-to-one.

### Packet vs mission

A **packet** is a bounded local composition object.
A **mission** is a macro composition object that sequences, conditions, loops, clusters, and resolves one or more packets.

A packet may be one insertion scene, one negotiation scene, one hazard gauntlet, one fight cluster, or one debrief scene.
It is not automatically a mission.

### Site vs mission

A **site** is a place record.
A **mission** may use sites as theaters, nodes, destinations, approaches, fallback locations, contested spaces, or objective locations.

A site is not automatically a scenario because play occurs there.

### Challenge mesh vs scenario structure

A **challenge mesh** is the local arrangement of trials, hazards, puzzles, traps, obstacles, and pressure objects.
A **scenario structure** is the macro arrangement of objective flow, branch logic, progression conditions, and successor states.

### Organization/job source vs mission structure

The mission issuer, sponsor, patron, command body, or requesting authority is not the mission structure itself.
C10 may reference issuer roles and stakeholder roles, but institutional definition remains outside C10.

### Objective vs beat vs stage vs phase vs loop vs branch

An **objective** is a goal state or operational requirement.
A **beat** is an inflection point, revelation point, or notable moment.
A **stage** is a structured segment of macro progression with entry and exit conditions.
A **phase** is a broader operating mode or structural period that may contain multiple stages.
A **loop** is a repeating macro pattern that recurs without becoming a separate overlay engine.
A **branch** is a divergence in route, objective relation, consequence, or successor-state outcome.

These terms are not interchangeable.

### Route variant vs branch vs state divergence vs successor divergence

A **route variant** changes pathing or order without necessarily changing structure identity.
A **branch** changes local available content, access, or objective relation.
A **state divergence** changes later behavior or conditions inside the same broader continuity line.
A **successor divergence** changes what later structures become available, blocked, altered, or replaced.

### Success vs failure vs fallout vs successor-state

**Success** and **failure** apply first to objectives, stages, phases, or loops.
**Fallout** covers collateral changes, costs, losses, exposures, and escalations.
**Successor-state** is the durable post-resolution state that later content inherits or references.

### Resolution class

A **resolution class** identifies how a macro structure closes or transitions. Possible classes include:
- completion
- partial completion
- negotiated closure
- substitution
- timeout
- abandonment
- forced redirection
- external interruption
- absorption into successor structure
- unresolved continuation

### Template vs normalized archetypal structure vs instance

A **template** is a reusable macro-structure pattern.
A **normalized archetypal structure** is Astra’s stable doctrinal skeleton for a recurring donor family without yet being one specific converted mission/scenario.
An **instance** is a specific mission, scenario, arc, or path entry.

### Authored vs normalized vs generated structure

**Authored structure** is the donor-presented structure.
**Normalized structure** is Astra’s doctrinally stabilized representation of that structure.
**Generated structure** is a structure created by generator logic, tables, or procedural engines.

These statuses must remain explicitly marked.

### Local branch vs arc divergence

A **local branch** changes route, pressure, or resolution inside one mission or scenario.
An **arc divergence** changes which future structures become available, blocked, altered, or canonically continuing.

## Core C10 structure families

C10 should support the following major structure families.
These are not all interchangeable and should not be flattened into one generic adventure schema.

### 1. Mission structure

A bounded operational unit with clear objective architecture and explicit completion or termination states.

### 2. Open scenario structure

A bounded but open macro-playable shell with multiple routes, revisitable nodes, or non-linear packet access.

### 3. Investigation scenario structure

A scenario whose progression depends substantially on information state, revelation state, evidence state, witness/contact access, or truth-resolution thresholds.

### 4. Crawl scenario structure

A scenario whose progression depends substantially on site traversal, node discovery, area access, location pressure, persistence, and local challenge sequencing.

### 5. Heist or operation structure

A scenario or mission whose progression depends on prep, access, insertion, execution, exposure, contingency, and extraction.

### 6. Trial sequence structure

A scenario or mission chain centered on successive tests, ordeals, ritualized contests, gate conditions, or qualifying stages.

### 7. Survival or endurance structure

A scenario whose progression is governed by sustained pressure, attrition, route selection, scarcity, time, or environmental persistence thresholds.

### 8. Political or social leverage structure

A scenario whose key progression depends on stakeholder posture, reputation state, leverage state, social access, negotiation thresholds, allegiance shifts, or public consequence.

### 9. Military or campaign-operation structure

A scenario or mission chain whose progression depends on command objectives, strategic staging, force deployment, contested zones, or operational sequencing.

### 10. Procedural sandbox shell

A bounded macro-playable structure where generator-fed missions, events, nodes, routes, or escalation pulses create repeatable or semi-open play inside a defined shell.

C10 owns the shell structure.
C12 owns the generator procedures.

### 11. Arc structure

A persistent linked continuity made of multiple missions and/or scenarios with durable state carry-forward and continuity burden.

### 12. Adventure-path structure

A directed, authored, multi-scenario or multi-arc continuity with progression spine, branch control, and successor-state handoff discipline.

## Open-structure doctrine

C10 must recognize that many donors present structures that are neither cleanly linear nor truly campaign-unbounded.

### Open-structure subfamilies
- bounded open scenario
- bounded revisitable lattice
- stateful mission board shell
- bounded regional operation shell
- bounded clue-web scenario
- bounded trial field
- bounded procedural hub loop

### Open-structure principles

1. Open structure is not a synonym for sandbox rhetoric.
2. Open structures may still have strong boundedness and explicit closure conditions.
3. Open structures may still preserve objective clusters, stage clusters, and successor-state logic.
4. Open structures should not be over-normalized into artificial clean linear progression.
5. Directed structures should not be loosened into faux-open shells merely for aesthetic symmetry.

## Common macro-record grammar for C10

All C10 records should inherit common Batch C record grammar from C01 and then add the following macro-composition groups as needed.

### A. Structural identity group
- composition_family
- composition_function_profile
- composition_posture
- composition_scale
- structure_mode
- template_status
- archetypal_normalization_status
- authored_normalized_generated_status
- boundedness_status
- continuity_scope
- structure_identity_line
- derivative_or_revision_status
- pinned_variant_status

### B. Provenance and normalization group
- donor_presented_form
- donor_publication_unit_relation
- normalization_basis
- compression_or_expansion_notes
- omitted_or_externalized_components
- unresolved_conversion_strains

### C. Entry-state group
- mission_source_type
- entry_mode
- start_trigger_profile
- issuer_or_trigger_refs
- discovery_trigger_refs
- escalation_trigger_refs
- survival_trigger_refs
- invitation_or_claim_trigger_refs
- qualification_trigger_refs
- route_or_arrival_trigger_refs
- generator_emission_trigger_refs
- faction_or_site_state_trigger_refs
- predecessor_packet_or_structure_trigger_refs

### D. Stakeholder group
- stakeholder_refs
- issuer_refs
- sponsor_refs
- beneficiary_refs
- claimant_refs
- supervising_or_auditing_body_refs
- gatekeeper_refs
- neutral_forum_refs
- opposition_refs
- covert_meddler_refs
- legitimacy_source_refs
- protected_population_refs
- successor_claimant_refs

### E. Lower-schema composition group
- site_refs_by_role
- locale_cluster_refs
- packet_refs_by_role
- packet_aggregation_profile
- challenge_refs_by_role
- actor_or_force_cluster_refs
- item_asset_or_frame_refs_when_structurally_relevant
- reward_trigger_refs
- generator_attachment_refs

### F. Objective architecture group
- primary_objectives
- secondary_objectives
- optional_objectives
- hidden_or_discoverable_objectives
- opposition_objectives
- timed_or_threshold_objectives
- persistence_or_hold_objectives
- truth_or_discovery_objectives
- reversible_objectives
- shifting_objective_rules
- support_objective_relations
- competing_objective_relations
- obligation_bindings

### G. Progression group
- stage_set
- phase_set
- macro_loop_set
- stage_order_model
- phase_transition_model
- loop_exit_conditions
- route_topology
- route_variants
- branch_points
- convergence_points
- revisit_rules
- fallback_routes
- interruption_rules
- collapse_or_abort_routes

### H. State, visibility, and pressure group
- tracked_state_variables
- visibility_and_knowledge_posture
- revelation_state_hooks
- access_state_hooks
- faction_posture_hooks
- site_state_hooks
- exposure_or_detection_hooks
- attrition_or_pressure_hooks
- macro_pressure_sources
- unresolved_thread_hooks
- continuity_burden_profile
- successor_state_map

### I. Entry and exit condition group
- entry_conditions
- continuation_conditions
- pause_or_suspend_conditions
- termination_conditions
- closure_conditions
- resolution_class
- carry_forward_conditions

### J. Continuity and successor group
- predecessor_refs
- sibling_structure_refs
- successor_refs
- unlock_conditions
- block_conditions
- alternate_successor_routes
- state_divergence_flags
- successor_divergence_flags
- arc_divergence_flags

C10 does not require every record to fill every field group.
It does require every record to use only the field groups justified by its structure family.

## Entry-state doctrine

C10 must preserve how a macro structure is entered.
Many donor structures do not begin with patron assignment.

### Entry-state classes
A macro structure may begin through:
- patron or authority assignment
- discovery
- escalation from another structure
- survival necessity
- claim or invitation
- qualification or ritual access
- environmental or route arrival
- generator emission
- factional trigger
- site-state trigger
- packet successor trigger

### Entry-state principles

1. Entry-state helps define how the structure is activated, not just how it is described.
2. Entry-state affects both posture and continuity burden.
3. A triggered structure should not be rewritten as patron-issued merely because a patron later becomes involved.
4. Generator emission may create instances inside a shell without making the shell itself one authored scenario.

## Objective architecture

C10 objective logic must remain more rigorous than casual donor summary prose.

### Objective classes

At minimum, Astra should recognize the following objective classes when relevant:
- primary objective
- secondary objective
- optional objective
- hidden objective
- discoverable objective
- opposition objective
- timed objective
- threshold objective
- extraction objective
- hold or endurance objective
- denial or disruption objective
- truth or revelation objective
- escort or protection objective
- acquisition or retrieval objective
- access or infiltration objective
- survival objective
- reversible objective
- obligation without clean win-state closure

### Objective topology patterns

At minimum, Astra should preserve when objectives are:
- central with support objectives
- parallel
- sequential
- gated
- competing and simultaneous
- collision-bearing with opposition objectives
- hidden and later revealed
- tiered or qualifying
- reversible
- state-shifting after revelation, exposure, loss, or escalation
- misdirecting or false-front when donor-supported

### Objective principles

1. Objectives are not the same thing as beats.
2. Objectives may be parallel, sequential, gated, or mutually exclusive.
3. Objectives may change mid-structure when revelation, failure, exposure, or branching alters the macro state.
4. Objective success does not automatically imply clean success for the whole structure.
5. Objective failure does not automatically imply termination.
6. Objectives may be inherited upward into arc logic or downward into packet roles.
7. Obligations may remain structurally binding even when they are not victory conditions.

## Stage, phase, and loop architecture

C10 must support structured progression without enforcing one donor-family sequence.

### Stage roles

When stage architecture is useful, stages may include roles such as:
- briefing or intake
- acceptance or trigger
- preparation or legwork
- transit or approach
- insertion or initial contact
- execution
- complication or escalation
- climax or decisive phase
- extraction or escape
- aftermath or debrief
- successor handoff

These are **role labels**, not universal required stages.

### Phase role examples

Phases may include broader operating modes such as:
- pre-contact phase
- active operation phase
- exposed or contested phase
- emergency recovery phase
- endgame phase
- occupation or aftermath phase

### Lightweight macro-loop examples

Loops that may remain in ordinary C10 if they do not become distinct overlay engines include:
- repeated patrol-and-extraction cycles
- iterative clue-and-contact loops
- repeated trial rounds
- return-to-hub and redeploy loops
- limited survival maintenance loops
- bounded mission-board intake loops

### Loop types

When loops materially affect conversion, loop type should be declared. Relevant loop types include:
- progress-bearing loops
- maintenance-bearing loops
- intake-bearing loops
- attrition-bearing loops
- escalation-bearing loops

Loop type explains what the repetition is doing structurally, not merely that repetition exists.

### Progression principles

1. Stages are macro-structural segments.
2. Phases are broader operating modes that may contain multiple stages.
3. Loops are repeating macro patterns that remain subordinate to the structure rather than becoming the dominant subsystem.
4. A stage may contain multiple packets.
5. Some scenarios are open enough that stage sets are loose rather than ordered.
6. Some scenarios have hard stage gates.
7. Stage or phase transition may depend on state change, not only completion.
8. Stage failure may still permit continuation under fallout.
9. Repeating macro loops that dominate the whole structure should be escalated toward C14 rather than hidden here.

## Route topology and branch architecture

C10 must preserve route shape explicitly.
Different donor families imply different route topologies.

### Supported route topology families
- linear
- branching
- hub-and-spoke
- lattice
- node network
- gated-open
- cyclic or revisitable
- convergent branch
- divergent branch
- shell with generated inserts

### Branch classes
- tactical branch
- access branch
- objective branch
- revelation branch
- consequence branch
- successor branch
- arc-divergence branch

### Branch principles

1. Not every choice is a branch of equal schema significance.
2. A route variant changes pathing or order without necessarily changing structure identity.
3. A local branch changes local access, objective relation, or immediate consequence.
4. A state divergence changes later behavior within the same continuity line.
5. A successor divergence changes what later structures become available or blocked.
6. Local route deviation is not automatically arc divergence.
7. Branches must specify what actually changes:
   - packet access
   - site access
   - objective set
   - stakeholder posture
   - successor route
   - reward trigger exposure
   - continuity state
8. Branches may reconverge.
9. Reconvergence must not erase meaningful successor-state differences.

## Packet aggregation doctrine

C10 must be explicit about how macro structures use packets without absorbing C09.

### Packet aggregation profiles
- fixed ordered packet chain
- partially ordered chain
- optional packet cluster
- branch-gated packet cluster
- revisitable packet lattice
- state-reactive packet family
- failure-emitted packet set
- success-emitted packet set
- escalation-emitted packet set

### Packet aggregation principles

1. Packet aggregation describes macro use patterns, not packet content.
2. Reusing a packet family under different state conditions does not collapse the structure into packet-scale schema.
3. A packet chain is not automatically a mission unless macro objective, state, and resolution logic are present.
4. Strong packet aggregation doctrine protects C10 from collapsing back into C09.

## Site-role doctrine

C10 may reference sites only by structural role.
It must not absorb placehood.

### Site roles
- intake site
- theater site
- route node
- choke or gate site
- sanctuary or regroup site
- escalation site
- information-bearing site
- objective site
- extraction site
- successor-state site
- control or legitimacy site
- service hub dependency site

### Site-role principles

1. Site roles explain macro structural use, not site ontology.
2. Site temporality, service output, nested placehood, and wider place doctrine remain outside C10 except where directly necessary for macro progression notes.
3. A site chapter is not a scenario record merely because many packets occur there.

## Organization-role doctrine

C10 may reference organizations only by structural role.
It must not absorb organizationhood.

### Organization roles
- issuer
- sponsor
- beneficiary
- claimant
- supervising or auditing body
- gatekeeper organization
- neutral forum
- opposition bloc
- covert meddler
- successor claimant
- legitimacy source
- patron or protected population

### Organization-role principles

1. Structural role is not ontology.
2. Mission source, sponsor, and claimant relations may matter to scenario flow without converting the structure into a C07 record.
3. Institutional hierarchy, mandate, jurisdiction, and dependent-body doctrine remain outside C10.

## Challenge-role doctrine

C10 may reference challenge objects only by macro structural role.
It must not absorb challenge-objecthood.

### Challenge roles
- qualification challenge
- access-gate challenge
- environmental endurance mesh
- alarm or exposure challenge
- route-control challenge
- trial-node challenge
- verification or authorization challenge
- climax setpiece challenge
- recurring pressure challenge
- optional mastery challenge

### Challenge-role principles

1. Macro role is not challenge definition.
2. A major ordeal may still remain one challenge object or one packet rather than a whole scenario.
3. C10 only owns how challenges are positioned, sequenced, and conditioned in a larger structure.

## Visibility and knowledge-posture doctrine

C10 must preserve macro-scale knowledge posture without stealing Batch B information procedure.

### Visibility and knowledge-posture concerns
- what is known at structure start
- what is hidden but discoverable
- whether route knowledge is public, partial, or concealed
- whether sponsor intent is visible or concealed
- whether opposition identity is known or masked
- whether success criteria are fully visible, partially visible, or misleading
- whether hidden branches exist

### Visibility principles

1. Visibility posture affects structure behavior even when the lower information procedure lives elsewhere.
2. Concealed intent, partial maps, and hidden criteria must not be erased when donor structure depends on them.
3. Knowledge posture is a macro structural property when it changes objective handling, route choice, or consequence exposure.

## State, macro pressure, consequence, and successor-state architecture

C10 must carry more than a binary success/failure summary.

### Tracked state classes
When relevant, a C10 record may track:
- objective resolution state
- revelation or truth state
- site access state
- site condition state
- faction posture state
- ally/enemy availability state
- detection or exposure state
- pressure or alert state
- attrition or scarcity state
- political consequence state
- legitimacy or public-order state
- timer or threshold state
- unresolved thread state

### Macro pressure sources
When relevant, macro structures may be driven by:
- time pressure
- route collapse
- exposure or alarm escalation
- environmental degradation
- political fallout
- access decay
- reinforcement or response clocks
- information scarcity
- legitimacy crisis
- extraction windows
- repeated return-loop pressure

Macro pressure source explains what pushes or deforms the structure while it is being traversed. It does not replace composition function. A retrieval mission under time pressure is still a retrieval function structure; time pressure is the pressure source, not the function.

### Continuity burden classes
When relevant, a structure may carry forward burdens such as:
- unresolved factions
- unresolved site states
- unresolved challenge states
- unresolved entity custody
- legitimacy or political aftermath
- timer or escalation carry-forward
- resource depletion
- route closure or opening
- reward availability change
- public narrative consequences
- knowledge or revelation carry-forward

### Consequence classes
When relevant, consequences may include:
- fallout
- escalation
- collateral change
- exposure
- denial of access
- changed opposition posture
- changed ally posture
- resource burden handoff
- altered successor availability
- partial continuation
- forced retreat or regroup
- latent unresolved threat

### Successor-state principles

1. Successor-state is the durable output of structure resolution.
2. Successor-state may differ from immediate narrative tone.
3. Successor-state is not the same thing as carry-forward burden. Successor-state describes what structural condition comes next. Carry-forward burden describes what unresolved load, liability, damage, scarcity, exposure, custody problem, legitimacy problem, or lingering consequence persists into that next condition.
4. Multiple local outcomes may collapse into one successor-state only when that loss of distinction is doctrinally acceptable.
5. Arc and path structures must carry successor-state explicitly rather than relying on prose implication.
6. Continuity burden should be preserved explicitly whenever later structures mutate because of unresolved consequences rather than because of simple linear sequencing.

## Resolution classes

Macro structures may resolve through more than clean completion.

### Resolution classes
- completion
- partial completion
- negotiated closure
- substitution
- timeout
- abandonment
- forced redirection
- external interruption
- absorption into successor structure
- unresolved continuation

### Resolution principles

1. Resolution class is separate from objective success state.
2. A structure may achieve partial objective success yet end in forced redirection.
3. A structure may fail a central objective but continue through unresolved continuation.
4. A structure absorbed into a successor should not be falsely reported as clean closure.

## Templates, archetypes, instances, and normalization discipline

C10 must support both reusable structural patterns and specific converted structures.

### Reusable macro templates
Examples of template-level structural patterns include:
- patron-issued job with briefing, legwork, insertion, objective execution, and extraction
- investigation lattice with clue gates and suspect/contact node progression
- open crawl with site-node access progression and revelation-based unlocks
- endurance route with attrition pressure and extraction threshold
- trial ladder with escalating gate conditions
- faction operation chain with persistent posture shifts

These are templates, not converted scenarios.

### Normalized archetypal structures
A normalized archetypal structure is Astra’s stable doctrinal skeleton for a recurring donor family.
It is broader than one instance and narrower than an abstract template when Astra needs a durable family-normal form for repeated conversion.

### Instantiated structures
An instantiated structure is a specific mission, scenario, arc, or path entry created during donor conversion using one or more Astra template grammars or archetypal normal forms.

### Instantiation density
C10 must tolerate both sparse shells and dense authored structures. Some donor structures provide only a few fixed packet anchors, broad site roles, and light state hooks. Others specify dense packet sequencing, many fixed site roles, narrow branch conditions, and explicit state changes. Sparse shell and dense authored structure are both valid C10 situations and must not be mistaken for incompleteness or overdesign simply because their density differs.

### Generated structure posture
Generated content may enter C10 in two distinct ways:
- as instantiated mission or scenario content produced by an external generator or table procedure
- as a persistent shell that repeatedly accepts generated inserts over time

These are not the same schema situation. A generated instance is still one instance. A persistent shell that repeatedly accepts generated inserts is a posture and intake structure that must be marked separately.

### Donor publication units
A donor publication unit may normalize into:
- zero C10 records
- one instance
- several linked instances
- one template plus one or more instances
- one arc segment
- one path segment
- one scenario cluster
- mixed C10 and C13 structures

One donor chapter or publication unit may normalize into zero, one, or many C10 records, and may also normalize partly into C13 packaging without any one-to-one correspondence. Publication layout is evidence, not authority.

### Normalization rules

1. Preserve donor structural distinctions whenever Astra can represent them lawfully.
2. Normalize donor presentation into Astra structure only as far as needed for cross-corpus stability.
3. Do not invent extra branching, staging, or arc continuity merely to make a donor look richer.
4. Do not erase genuine donor complexity simply to force everything into one clean skeleton.
5. Mark authored structure and normalized structure separately when they differ materially.
6. Do not confuse a donor presentation unit with one Astra instance unless that equivalence is structurally justified.

## Special family notes

### Investigation structures

Investigation structures must preserve:
- clue or revelation dependency
- uncertainty state
- contact or witness access
- false lead or ambiguity tolerance when donor-supported
- information-based branch logic

Investigation structures must not be flattened into simple kill-or-fetch mission chains.

### Crawl structures

Crawl structures must preserve:
- traversal significance
- area or node progression
- revisitation logic when relevant
- local packet clustering
- site-state change when it affects macro progression

Crawl structures must not collapse into site records.

### Heist and operation structures

These structures must preserve:
- preparation significance when donor-supported
- access path differences
- exposure or alert escalation
- contingency and extraction logic

### Trial sequences

Trial structures must preserve:
- successive gate logic
- qualification or advancement conditions
- failure branch or repetition logic when present

### Survival structures

Survival structures must preserve:
- endurance pressure
- scarcity or attrition state
- route viability change
- threshold-based continuation or collapse

### Political and social leverage structures

These structures must preserve:
- stakeholder posture relevance
- influence or legitimacy consequences
- non-combat route viability
- access and alliance changes

### Military and campaign-operation structures

These structures must preserve:
- command objective hierarchy
- contested-zone or force-disposition significance
- staging and operational sequencing
- successor operation conditions

### Procedural sandbox shells

These structures must preserve:
- bounded shell identity
- repeatable mission or event intake points
- escalation framework
- revisit and persistence rules

C10 owns the shell.
C12 owns the procedures that populate it.

## Cross-file composition discipline

### C06 site handoff

C10 may reference sites by structural role such as:
- intake site
- theater site
- route node
- choke or gate site
- sanctuary or regroup site
- escalation site
- information-bearing site
- objective site
- extraction site
- successor-state site
- control or legitimacy site
- service hub dependency site

C10 must not restate site ontology, district breakdown, ecology, services, or spatial detail already owned by C06 except where directly required for macro progression notes.

### C07 faction handoff

C10 may reference organizations by structural role such as:
- issuer
- sponsor
- beneficiary
- claimant
- supervising or auditing body
- gatekeeper organization
- neutral forum
- opposition bloc
- covert meddler
- successor claimant
- legitimacy source
- patron or protected population

C10 must not absorb organizational doctrine, hierarchy, social body definition, or polity structure already owned by C07.

### C08 challenge handoff

C10 may reference challenge objects by structural role such as:
- qualification challenge
- access-gate challenge
- environmental endurance mesh
- alarm or exposure challenge
- route-control challenge
- trial-node challenge
- verification or authorization challenge
- climax setpiece challenge
- recurring pressure challenge
- optional mastery challenge

C10 must not redefine the challenge object itself.

### C09 local packet handoff

C10 may sequence, gate, branch, cluster, loop lightly, or condition packets.
C10 must not absorb packet-level scene scripting or local encounter detail.

### C11 reward handoff

C10 may define:
- reward triggers
- conditional reward exposure
- success-state reward relations
- failure-state reward loss or alteration

C10 must not define parcel contents.

### C12 generator handoff

C10 may define where generated content enters a macro structure.
C10 must not define roll logic, oracle logic, event table content, or generator procedure.

### C13 container handoff

C10 may be packaged inside larger containers.
C10 must not define publication packaging, sourcebook chapter grouping, compendium organization, or gazetteer semantics.

## Anti-collapse rules

C10 must not:
- treat a site as a scenario merely because play happens there
- treat a packet as a mission merely because it contains combat and dialogue
- treat a mission patron as a faction record
- treat a major hazard or trial as a whole scenario unless macro progression actually exists
- treat reward promises as reward parcels
- treat random mission seeds as a scenario definition
- treat a bundle of chapters as one path structure without explicit continuity logic
- treat donor publication form as equivalent to Astra structure family
- smuggle subsystem overlays into ordinary mission fields
- flatten all macro-play into one generic “adventure schema”
- mistake a repeatable generator-backed mission board for one authored scenario when it is only a content-intake shell
- mistake a recurrent site-state crisis loop for a mission family when the dominant structure is actually site-state emission or campaign overlay behavior

## Anti-hallucination rules for future conversion

Future conversion working from C10 must obey the following:

1. Do not infer mission structure from local packet content alone.
2. Do not infer arc continuity merely because several donor chapters share a cast or location.
3. Do not invent branch paths that the donor does not support or strongly imply.
4. Do not erase genuine branch paths simply to make a donor fit a linear structure.
5. Do not confuse a site chapter, district chapter, or dungeon chapter with the structure actually governing play.
6. Do not convert mission issue source, patron notes, or employer notes into full organization ontology.
7. Do not convert one major hazard, puzzle, ritual, or ordeal into a scenario when it is structurally one challenge object or one packet.
8. Do not mistake publication packaging for scenario topology.
9. Do not present generated content shells as authored scenario flow.
10. Do not treat partial objective failure as automatic scenario termination unless the donor or normalized structure actually requires that.
11. Do not confuse fallout with successor-state.
12. Do not confuse local branch with arc divergence.
13. Do not confuse route variant with state divergence or successor divergence.
14. Do not fabricate a clean objective hierarchy when the donor clearly presents a looser open structure; instead mark the structure as open and normalize only what is supported.
15. Do not fabricate an open sandbox when the donor clearly presents a directed path structure.
16. Do not hide subsystem strain inside freeform notes; escalate distinct subsystem pressure toward C14 when ordinary C10 grammar cannot carry it safely.
17. Do not mistake a donor publication unit for one Astra instance unless the structural mapping is explicit and justified.
18. Do not rewrite triggered, discovery-based, or survival-driven entry into patron-issued entry for convenience.

## C10 reserve-trigger rules

The following conditions indicate that ordinary C10 schema may be insufficient and that a later subsystem packet or campaign overlay file may be needed:
- scenario progression depends on a dedicated investigation engine rather than ordinary clue or state hooks
- scenario progression depends on kingdom, domain, or warfare turns as primary structure
- scenario progression depends on a distinct heist, infiltration, or faction-war subsystem that ordinary C10 fields only imitate badly
- scenario continuity depends on a campaign overlay loop more than on mission/scenario composition
- the donor’s playable macro structure is driven by a repeatable overlay packet rather than by scenario instances

### What may still remain in ordinary C10

The following may remain in C10 so long as they do not become the dominant controlling engine:
- light preparation phases
- light clue gating
- light resource or time pressure
- light faction posture interaction
- light route-generation or insertion logic
- light repeating mission-board structures
- lightweight macro loops subordinate to one bounded structure

When these conditions remain subordinate, C10 should represent them directly rather than escalating too aggressively.
When they become the dominant governing engine, escalate toward C14.

## Conversion-facing durability principles

1. Prefer a family of compatible macro-composition schemas over one universal adventure blob.
2. Preserve difference between operational ask, playable flow, continuity chain, and publication package.
3. Preserve difference between family, function, and posture.
4. Preserve difference between authored structure, archetypal normalized structure, instantiated structure, and generated structure.
5. Prefer cross-file reference to field duplication.
6. Preserve route topology explicitly whenever it materially affects conversion.
7. Preserve successor-state explicitly whenever later structures depend on it.
8. Preserve continuity burden explicitly whenever later structures mutate because of unresolved consequences.
9. Treat investigation, crawl, operation, trial, survival, political, and bounded-open structures as first-class donor pressures, not decorative subcases.
10. Do not allow one donor family to silently define the universal mission model.
11. Keep C10 doctrine-first, conversion-stable, and modular enough to survive a large mixed corpus.

## Validation stress list

C10 validation should repeatedly pressure-test the following failure modes:
- site chapter mistaken for scenario structure
- packet chain mistaken for mission or scenario without macro logic
- mission source or patron mistaken for organization record
- trial mesh mistaken for whole scenario
- donor book chapter grouping mistaken for path structure
- reward promises mistaken for reward records
- generator intake shell mistaken for authored scenario
- open structure over-normalized into clean objectives
- directed structure over-loosened into sandbox rhetoric
- subsystem strain hidden inside freeform notes
- publication unit mistaken for one Astra instance without justification
- route variant mistaken for successor divergence
- lightweight macro loop mistaken for overlay-scale engine or vice versa

## File outcome

If C10 is functioning correctly, Astra should be able to do all of the following without collapse:
- represent one-shot missions
- represent open scenarios
- represent bounded-open shells
- represent investigation structures
- represent multi-stage operations
- represent crawl shells without turning them into place files
- represent light macro loops without falsely escalating them into overlay files
- represent campaign arcs without turning them into sourcebook bundles
- represent authored path progression without erasing branches or successor states
- distinguish templates, archetypal normal forms, and converted instances
- distinguish authored, normalized, and generated macro structures
- route subsystem-heavy edge cases toward later overlay handling when needed

That is the doctrinal job of this file.
