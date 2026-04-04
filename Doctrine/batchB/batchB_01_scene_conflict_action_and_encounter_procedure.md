# batchB_01_scene_conflict_action_and_encounter_procedure.md

## Purpose

This file defines Astra Ascension’s **operational scene shell** for structured play. It governs how scenes are framed, how they escalate into encounters, how encounters enter structured procedure, how priority and action timing are expressed, and how structured play exits or hands off to more specialized subsystem doctrine.

This file is not the combat chapter in disguised form. It is the **encounter chassis** for Batch B.

Its purpose is to provide a conversion-stable operational framework capable of absorbing donor procedures for combat, pursuit, breach, hazard pressure, timed operations, contested social pressure, investigative pressure, and mixed encounters without collapsing them into a single donor-shaped combat loop.

## Authority and dependency position

This file is authoritative for:
- scene framing in structured play,
- encounter-state escalation,
- conflict-state escalation,
- procedural modes and encounter modes,
- participant sequencing and priority procedure,
- action timing windows,
- action-budget doctrine,
- encounter initialization and termination,
- handoff rules between this file and specialized Batch B subsystems.

This file depends on Batch A doctrine, especially:
- `batchA_03_resolution_framework.md`,
- `batchA_04_attribute_and_derived_stat_architecture.md`,
- `batchA_05_competency_and_skill_translation_architecture.md`,
- `batchA_06_access_tags_permissions_and_proficiency_gates.md`,
- `batchA_07_ability_object_model.md`,
- `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`,
- `batchA_08_status_condition_and_effect_architecture.md`,
- `batchA_09_damage_family_and_resistance_taxonomy.md`,
- `batchA_09b_damage_fusion_and_compound_interactions.md`,
- `batchA_15_conversion_invariants.md`.

This file must not silently re-own any of those systems.

## Ownership boundary

This file owns **procedure**, not substantive content law.

This file must define:
- what a scene is in operational terms,
- what an encounter is,
- what a conflict is,
- what procedural modes exist,
- what causes escalation into structured procedure,
- how structured procedure is initialized,
- how priority is established,
- what kinds of procedural expenditures exist during structured play,
- when declarations become commitments,
- when interruption and trigger windows occur,
- how rounds, exchanges, turns, and checkpoints are expressed,
- how an encounter exits, pauses, or hands off.

This file must not define or re-explain:
- generic success resolution, target numbers, or core check law,
- damage law or resistance law,
- condition meaning,
- injury, death, healing, or recovery specifics,
- stealth or detection math,
- clue, evidence, and information architecture,
- social leverage or influence architecture,
- vehicle, ship, mech, or mount operation specifics,
- item schemas, loot schemas, or post-encounter reward rules,
- creature stat construction,
- adventure, trap, puzzle, or random table schemas.

If this file begins absorbing the job of a specialized subsystem, that is doctrinal drift and must be corrected by redirection or later split.

## Core doctrine terms

### Scene
A **scene** is the broadest bounded unit of active play. A scene exists when the current fiction is organized around a distinct place, situation, or developing problem with identifiable participants and unresolved stakes.

A scene must track at minimum:
- current location or spatial context,
- present participants and materially relevant entities,
- current objective state,
- declared procedural mode,
- active carriers of pressure,
- current unresolved stakes,
- current escalation state,
- known or inferred exit conditions.

A scene is not defined by combat. A scene may be exploratory, social, investigative, hazardous, logistical, ritual, violent, or mixed.

### Encounter
An **encounter** is a scene-localized operational problem that requires explicit procedural handling beyond ordinary freeform scene flow.

An encounter exists when one or more of the following are true:
- timing order materially matters,
- multiple participants may act in meaningful opposition or interference,
- pressure must be tracked across successive procedural beats,
- objective progress must be measured under stress,
- risk, hazard, or opposition requires a declared procedure state.

Not every scene is an encounter. Not every encounter is a fight.

### Conflict
A **conflict** is an encounter in which opposition between forces is active enough that priority, action windows, and procedural commitments must be tracked explicitly.

Combat is one form of conflict. Conflict may also include pursuit, contested breach, timed sabotage under pressure, extraction under fire, defensive holding actions, coercive standoffs, and other opposed operations.

### Action
An **action** is a procedural expenditure made by a participant during structured play.

An action is not synonymous with every meaningful contribution. Structured play must distinguish between:
- major actions,
- movement or repositioning,
- incidental interactions,
- triggered responses,
- held or readied commitments,
- sustained commitments,
- subordinate or directed activity,
- passive or persistent effects.

### Participant
A **participant** is any entity that can materially affect the scene’s stakes, timing, opposition, or progress.

### Side
A **side** is a provisional or stable alignment grouping for encounter procedure. Sides may be formal teams, temporary alliances, independent actors, neutral-but-reactive parties, or asymmetrical stakeholders.

### Pressure
**Pressure** is any active force that pushes a scene toward loss, escalation, complication, exhaustion, exposure, failure, or forced transition.

Pressure may come from enemies, hazards, clocks, unstable environments, social dynamics, deadlines, spreading conditions, collapsing infrastructure, incomplete information, or resource drain.

### Carrier of pressure
A **carrier of pressure** is the specific source through which pressure enters the scene, such as a hostile actor, pursuing force, burning structure, failing shield, ticking ritual, unstable reactor, fragile hostage situation, or closing political window.

### Objective state
**Objective state** is the current tracked condition of what the participants are trying to achieve, prevent, preserve, obtain, escape, complete, or survive.

### Exit condition
An **exit condition** is the state change that ends or transforms the current scene or encounter. Exit conditions are not limited to elimination of opposition.

## Design principle: scene shell first, donor expression second

Astra must define its own operational shell before any donor combat loop, chase loop, clock loop, or exchange loop is translated into it.

Donor procedures may map into Astra encounter procedure, but no donor sequencing model is hidden law by default. This includes fixed initiative, rerolled initiative, side initiative, fast/slow turns, action points, clock-based exchanges, zone-based pacing, or donor-specific surprise models.

## Procedural modes

A scene must always declare its current **procedural mode**.

### 1. Open scene mode
Open scene mode is the default state of active play. Actions are resolved in conversational order according to the fiction and the Batch A resolution framework. No formal turn order is required.

Open scene mode is appropriate when:
- simultaneity is not a major problem,
- pressure does not need beat-by-beat tracking,
- participants are not materially competing for timing control,
- the scene can be advanced without structured sequencing.

### 2. Structured encounter mode
Structured encounter mode is used when the scene has entered a condition where order, repeated pressure, explicit objectives, or procedural beats matter, but full conflict sequencing may not yet be necessary.

This mode is appropriate for:
- tense negotiations with ticking consequences,
- hazardous navigation,
- pursuit setup,
- infiltration under active risk,
- ritual stabilization,
- technical operations under deadline,
- investigative progress under threat,
- mixed scenes where violence may erupt but is not yet the sole driver.

### 3. Structured conflict mode
Structured conflict mode is used when opposition is active enough that priority procedure, commitment windows, and per-beat participant expenditures must be tracked explicitly.

This mode is appropriate for:
- combat,
- pursuit/evasion where adversaries directly interfere,
- extraction under pursuit,
- breach/hold/defend operations,
- coordinated suppression or containment,
- multi-party contested standoffs,
- mixed tactical scenes where hazards and enemies act within the same timing frame.

## Escalation ladder

A scene may escalate or de-escalate between modes.

The normal doctrinal ladder is:
- open scene mode,
- structured encounter mode,
- structured conflict mode.

Astra does not require every scene to pass through every rung, but conversion work should preserve the difference between lightly structured pressure and fully turn-sensitive conflict wherever donor procedures meaningfully distinguish them.

Escalation into a higher mode occurs when at least one of the following becomes materially true:
- immediate hostile action or credible threat of hostile action,
- contested simultaneity,
- active attempts to prevent or interrupt an objective,
- hazard or deadline pressure that must tick procedurally,
- uncertainty over who acts first or who can intervene,
- multiple participants making nontrivial commitments in the same operational window,
- objective-state changes that must be tracked beat by beat.

De-escalation occurs when structured tracking is no longer necessary, such as when:
- active opposition ends,
- a time-critical phase resolves,
- control stabilizes,
- the scene narrows to ordinary freeform handling,
- a specialized subsystem concludes and no further structured shell is required.

## Encounter modes

Whenever a scene enters structured encounter mode or structured conflict mode, the encounter should declare one or more **encounter modes**.

Encounter modes are not full subsystems. They are classification labels that describe the pressure pattern being handled so donor material can map into Astra cleanly.

Core encounter modes include:
- **violent conflict**,
- **pursuit / evasion**,
- **hazard pressure**,
- **timed operation**,
- **contested social pressure**,
- **investigative pressure**,
- **breach / infiltration**,
- **defensive hold / containment**,
- **escape / extraction**,
- **mixed encounter**.

A mixed encounter may carry multiple modes at once. Example: a violent conflict inside a collapsing structure during an extraction is violent conflict + hazard pressure + timed operation + escape/extraction.

Encounter modes exist to improve translation discipline. They do not, by themselves, create rules beyond classification and handoff expectations.

## Scene frame requirements

At the moment structured procedure begins, the scene frame must be made explicit enough to support lawful adjudication.

The minimum required scene frame is:
- declared procedural mode,
- declared encounter mode or modes,
- current participants,
- provisional or stable sides,
- objective state,
- active carriers of pressure,
- current spatial model,
- current temporal model,
- known or implied exit conditions,
- special operating constraints already in force.

Special operating constraints may include darkness, silence discipline, limited atmosphere, unstable footing, fragile cargo, anti-magic zones, crowd density, communication delay, vacuum exposure, or similar environment-shaping facts. The specific law for those constraints belongs to the relevant subsystem, but their presence must be declared here because they affect procedure.

## Encounter initialization

When structured procedure begins, initialization must answer the following questions:

1. Who is present and materially relevant?
2. Which entities count as active participants?
3. What sides or temporary alignments exist?
4. What is each side trying to achieve right now?
5. What is the initial objective state?
6. What pressures are already active, and what carries them?
7. What spatial model is being used?
8. What temporal model is being used?
9. What priority procedure will govern order?
10. Are there any readiness, ambush, concealment, alertness, or interrupted-entry issues to resolve?
11. Which specialized subsystems are expected to receive handoff during the encounter?
12. What states will end, transform, pause, or suspend the encounter?

Initialization should be explicit enough to prevent hidden assumptions but lean enough to remain reusable across donor systems.

## Readiness, surprise, and contested entry

This file owns the procedural concept of contested entry into structured play.

This includes:
- readiness advantage,
- interrupted entry,
- partial readiness,
- ambush posture,
- unready exposure,
- delayed recognition of threat,
- staggered arrival into the encounter frame.

This file does **not** own the underlying stealth, concealment, visibility, sensory, or detection math. Those belong to `batchB_08_stealth_detection_visibility_and_sensory_procedure.md`.

B01 only establishes that contested entry must be resolved before normal priority begins whenever:
- one or more participants were not equally prepared to act,
- one side gained first-position advantage through concealment or deception,
- threat recognition occurred unevenly,
- arrival into the conflict is staggered.

The result of contested entry must feed into priority procedure and opening commitments without redefining stealth law inside this file.

## Spatial expression doctrine

Spatial expression is a first-class doctrinal concern in Astra. It must not be treated as a donor-specific afterthought.

Every structured encounter must declare the spatial model it uses. Astra supports multiple valid spatial expressions so donor conversions do not silently hardcode one style as universal truth.

Supported spatial models include:
- **exact measurement**,
- **zones**,
- **range bands**,
- **abstract adjacency**,
- **non-spatial or partially spatial framing**.

### Exact measurement
Used when precise distances, geometry, trajectories, or placement matter enough to justify direct measurement.

### Zones
Used when relative location matters but exact distances do not need constant fine-grain tracking.

### Range bands
Used when practical reach, engagement range, and line-of-effect matter more than map precision.

### Abstract adjacency
Used when the scene can be resolved through relation states such as engaged, nearby, separated, elevated, blocked, exposed, concealed, or in control of an objective.

### Non-spatial or partially spatial framing
Used when the main pressure is informational, social, symbolic, procedural, or internal, or when spatial detail only matters in limited ways.

A conversion may map donor material into whichever spatial model best preserves its operational logic. No donor map scale, meter count, or miniature standard is universally binding on Astra doctrine.

## Temporal expression doctrine

Every structured encounter must also declare the temporal model it uses.

Temporal expression may use one or more of the following:
- **scene-time**,
- **rounds or exchanges**,
- **turns**,
- **phase segments**,
- **checkpoints**,
- **timers, clocks, or deadlines**.

### Scene-time
Used for broader development where fine turn order is unnecessary.

### Rounds or exchanges
Used when each cycle of active participation must be tracked across all participants.

### Turns
Used when individual participant contribution windows must be separated.

### Phase segments
Used when an encounter has distinct recurring sub-states, such as approach, breach, execution, fallout, or hazard tick windows.

### Checkpoints
Used when persistent effects, pressure ticks, status updates, environmental pulses, or objective progression must resolve at known intervals.

### Timers, clocks, or deadlines
Used when procedural loss, escalation, or failure advances independently of participant turns.

This file establishes the doctrine that structured encounters must declare where periodic effects resolve, but it does not define the substantive law for those effects.

## Priority procedure

Astra uses **priority procedure** as the general doctrine term for determining who may declare, commit, respond, interrupt, or resolve first during structured play.

Priority procedure is broader than “initiative.” Initiative is one family within this layer.

Supported priority families include:
- rolled individual order,
- rolled side order,
- static order,
- alternating side order,
- phased fast/slow order,
- point-spend or bid-driven order,
- narrative priority constrained by declared procedure,
- other donor-consistent lawful orderings.

Each encounter must declare the priority family it uses.

Priority procedure must be capable of expressing:
- opening order,
- repeated order across later cycles,
- tie handling,
- entry of late participants,
- delayed commitments,
- readied or held responses,
- interruption windows,
- order changes caused by effects or subsystem rules.

This file does not require a single universal initiative formula. It requires that every structured encounter have a lawful priority method.

## Action-budget doctrine

Structured play must declare not only order, but also what kinds of contributions a participant can make within a procedural cycle.

Astra therefore defines an **action budget** as the total structured opportunity available to a participant during a turn, exchange, phase, or checkpoint window.

Action budgets may be expressed differently across donor conversions, but must be decomposable into intelligible procedural units.

At minimum, B01 recognizes the following expenditure classes:
- **major action**,
- **movement or repositioning expenditure**,
- **incidental interaction**,
- **triggered response**,
- **held or readied expenditure**,
- **sustained commitment**,
- **subordinate direction expenditure**,
- **passive or persistent effect resolution**.

A donor conversion may collapse or expand these classes, but should not erase them when the donor system materially distinguishes them.

This doctrine exists so Astra can absorb systems with:
- fixed one-action structures,
- multiple-action structures,
- bonus or minor actions,
- action-point systems,
- free-action economies,
- reactions and interrupts,
- multi-step casts or operations,
- sustained effects and concentration-like commitments,
- directed minions, drones, companions, or summons.

## Declaration, commitment, interruption, and resolution windows

Every structured encounter must respect four procedural windows.

### 1. Declaration window
The participant states what they are attempting, enough for the encounter to know intent, method, scale, and relevant target or objective.

### 2. Commitment window
The attempted action becomes locked enough that costs, exposure, opportunity use, or triggered responses may attach. Not all declarations become commitments; aborted or invalid declarations may fail before commitment.

### 3. Interruption window
Before the declared commitment fully resolves, lawful triggers, reactions, counters, defensive clauses, or timing-based substitutions may occur according to the encounter’s priority procedure and the attached subsystem law.

### 4. Resolution window
The commitment resolves. Outcomes, consequences, state changes, movement, objective progress, status application, damage application, and follow-on checks are processed according to relevant subsystem law.

This section is crucial because later subsystem files must not invent incompatible timing assumptions.

## Universal structured-play actions

This file defines only shell-level universal action categories. It does not define attack formulas, healing formulas, stealth formulas, or influence formulas.

Universal categories include:
- **reposition**,
- **engage or disengage procedurally**,
- **use ability**,
- **use item or device**,
- **interact with scene element**,
- **assist or support**,
- **defend, brace, or protect**,
- **ready or hold**,
- **withdraw or retreat**,
- **recover posture or functional position**,
- **direct subordinate entity**,
- **pursue objective progress directly**.

Any of these may resolve through Batch A or a specialized Batch B subsystem. The point of this section is not to define outcomes, but to guarantee that structured procedure has a common vocabulary of participant intent.

## Sustained and persistent commitments

Some actions do not end cleanly in a single resolution window.

This file therefore recognizes:
- **sustained commitments**, which continue to occupy procedural attention after initial use,
- **persistent effects**, which continue producing consequences after the original action resolves,
- **conditional standing states**, which remain in force until interrupted, broken, discharged, or completed.

The actual law for cost, upkeep, recharge, status, or effect persistence belongs to Batch A and later subsystem files. B01 only defines that the encounter shell must know when these commitments begin, when they are checked, and when they end.

## Objective-state tracking

Encounters are not defined only by attrition. They are defined by what is being pursued or prevented under pressure.

Every structured encounter must identify one or more objective states such as:
- reach the exit,
- hold the gate,
- extract the target,
- stop the ritual,
- keep the reactor stable,
- prevent alarm spread,
- gather enough evidence before exposure,
- force a concession,
- survive until transport arrives.

Objective-state tracking should answer:
- what success looks like,
- what failure looks like,
- what partial progress looks like,
- what events change the state,
- whether the objective can split, stall, or reverse.

## Pressure-state tracking

Structured encounters should also declare pressure-state logic wherever pressure can accumulate, pulse, escalate, or transform.

Pressure-state tracking may include:
- clocks,
- threshold bands,
- stage transitions,
- repeating hazard pulses,
- morale or cohesion degradation,
- exposure buildup,
- alarm escalation,
- countdowns,
- destabilization tracks,
- pursuit gain/loss bands.

This file authorizes such structures but does not prescribe one universal implementation.

## Participants that are not simple single actors

This file must support encounters involving:
- groups,
- swarms,
- formations,
- linked entities,
- directed auxiliaries,
- summons,
- drones,
- companions,
- vehicles or platforms,
- large environmental actors.

B01 only defines that the encounter shell must know whether these act:
- independently,
- on a shared priority slot,
- through a controller’s action budget,
- by triggered behavior,
- by automated standing procedure.

Detailed law for companions and auxiliary entities belongs to `batchB_13_companions_retinues_summons_drones_and_auxiliary_entities.md`.
Detailed law for mounts, vehicles, mechs, ships, and platforms belongs to `batchB_14_mounts_vehicles_mechs_ships_and_platform_operations.md`.

## Encounter transitions and exit states

An encounter ends, pauses, or transforms when its operative state no longer requires the current procedure shell.

Recognized exit-state patterns include:
- objective completion,
- objective failure,
- elimination or incapacitation of decisive opposition,
- surrender or negotiated stand-down,
- rout or loss of will to continue,
- escape or loss of contact,
- extraction or evacuation,
- containment stabilization,
- subsystem transition,
- scene fracture into multiple new encounters,
- de-escalation back to open scene mode.

An exit condition must be declared as early as practical. “Fight until one side is gone” is only one possible exit pattern and must not be treated as universal.

## Pause, suspend, split, and merge behavior

Structured encounters may pause, suspend, split, or merge.

### Pause
The encounter remains the same encounter, but procedure is temporarily not advancing.

### Suspend
The encounter is temporarily interrupted by another procedure layer and may resume later.

### Split
A single encounter divides into multiple linked or separate encounter frames because participants, objectives, or spatial realities have meaningfully separated.

### Merge
Previously separate encounter frames are combined because their pressures, participants, or objective states have become operationally inseparable.

This doctrine is necessary for large-scale, multipart, and mixed-mode donor scenes.

## Mandatory subsystem handoff map

The following handoff map is mandatory and not optional.

- **Generic resolution logic** -> `batchA_03_resolution_framework.md`
- **Attributes and derived stats** -> `batchA_04_attribute_and_derived_stat_architecture.md`
- **Skills / competencies as translated capabilities** -> `batchA_05_competency_and_skill_translation_architecture.md`
- **Access tags, permissions, proficiencies, and gates** -> `batchA_06_access_tags_permissions_and_proficiency_gates.md`
- **Ability structure and ability metadata** -> `batchA_07_ability_object_model.md`
- **Costs, recharge, upkeep, and backlash** -> `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`
- **Statuses, conditions, and effect architecture** -> `batchA_08_status_condition_and_effect_architecture.md`
- **Damage, resistance, immunity, and related taxonomies** -> `batchA_09_damage_family_and_resistance_taxonomy.md`
- **Compound damage interactions** -> `batchA_09b_damage_fusion_and_compound_interactions.md`
- **Health, injury, healing, death, and recovery** -> `batchB_02_health_injury_healing_death_and_recovery_framework.md`
- **Equipment, items, and gear schemas** -> `batchB_03_equipment_item_and_gear_object_model.md`
- **Exploration travel cadence, time, and distance outside encounter procedure** -> `batchB_06_exploration_travel_navigation_time_and_distance.md`
- **Environmental hazards, weather, afflictions, and regional exposure specifics** -> `batchB_07_environment_hazards_weather_regions_and_afflictions.md`
- **Stealth, concealment, visibility, detection, and sensory contests** -> `batchB_08_stealth_detection_visibility_and_sensory_procedure.md`
- **Investigation, research, clues, and information-state procedure** -> `batchB_09_investigation_research_discovery_clues_and_information_procedure.md`
- **Social conflict, influence, negotiation, and reputation** -> `batchB_10_social_conflict_influence_reputation_and_negotiation.md`
- **Downtime, rest, training, projects, and services** -> `batchB_11_downtime_rest_training_projects_and_services.md`
- **Factions, institutions, clearance, and service access** -> `batchB_12_factions_institutions_clearance_and_service_access.md`
- **Companions, retinues, summons, drones, and auxiliaries** -> `batchB_13_companions_retinues_summons_drones_and_auxiliary_entities.md`
- **Mounts, vehicles, mechs, ships, and platform operation** -> `batchB_14_mounts_vehicles_mechs_ships_and_platform_operations.md`
- **Settlements, bases, capitals, and infrastructure operations** -> `batchB_15_settlements_bases_capitals_and_infrastructure_operations.md`
- **Loot, rewards, salvage, and post-encounter inflows** -> `batchB_16_loot_rewards_salvage_and_post_encounter_inflows.md`

If B01 needs substantive law from one of these, it must hand off rather than absorb that file’s job.

## Conversion doctrine notes

When converting donor procedures into Astra under this file:
- do not assume encounter equals combat,
- do not assume initiative equals one universal formula,
- do not assume a single spatial model,
- do not assume a single action economy,
- do not assume objective completion is equivalent to enemy elimination,
- do not assume surprise is only a stealth mini-rule,
- do not hardcode donor terminology as Astra doctrine,
- do not import donor metaphysics just because a donor encounter loop is mechanically useful.

Instead, determine:
- what the donor scene is structurally doing,
- what pressures it is tracking,
- what its actual encounter mode is,
- what its priority procedure is,
- what its action-budget expression is,
- what its exit conditions are,
- what specialized Astra subsystems must receive handoff.

## Anti-drift rules

This file must actively resist the following failure modes:
- turning B01 into a combat-only file,
- turning B01 into a second copy of the Batch A resolution framework,
- turning B01 into a stealth, social, or hazard subsystem by accident,
- hardcoding exact-distance tactical mapping as universal law,
- hardcoding one donor initiative system as universal law,
- treating encounter exit as attrition-only,
- omitting objective-state and pressure-state tracking,
- failing to declare timing windows clearly enough for later files to build on.

## Doctrine summary

`batchB_01_scene_conflict_action_and_encounter_procedure.md` defines Astra Ascension’s operational encounter shell.

It exists to answer five core procedural questions:
- what state the scene is currently in,
- when and why it escalates into structured procedure,
- how structured participation is sequenced,
- what kinds of procedural expenditures exist and when they resolve,
- when the encounter exits or hands off.

It is therefore the first and most central operational file in Batch B, but only so long as it remains a shell file and does not attempt to swallow the jobs of the files that follow.
