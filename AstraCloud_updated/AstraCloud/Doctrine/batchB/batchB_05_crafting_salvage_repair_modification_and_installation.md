# batchB_05_crafting_salvage_repair_modification_and_installation.md

## Purpose

This file defines Astra Ascension’s doctrine for **crafting, salvage, repair, modification, refinement, and installation**.

Its role is to provide Astra with a **universal transformation-procedure grammar** for item, material, and host-state change.
It exists so donor systems with very different assumptions about making, fixing, breaking down, upgrading, socketing, embedding, calibrating, harvesting, refining, and reusing things can be absorbed into Astra without being flattened into a single donor-shaped “crafting” loop.

This file is not merely a make-items chapter.
It is the procedure layer for **lawful transformation of material and item states**.

In Astra terms, this file governs how:
- inputs become outputs,
- damaged objects become restored objects,
- existing objects become altered objects,
- source objects become salvage or components,
- modules become installed into hosts,
- and project work proceeds under time, labor, tool, facility, and risk constraints.

## Authority and scope

This file is authoritative for:
- transformation-project doctrine,
- fabrication doctrine,
- repair doctrine,
- salvage and deconstruction doctrine,
- refinement doctrine,
- modification doctrine,
- installation and integration doctrine,
- project input classes,
- project gate classes,
- project progress-model classes,
- project risk and failure doctrine,
- output and yield semantics,
- reversibility and recoverability classes,
- lawful incomplete project mapping,
- and mandatory handoff boundaries to adjacent systems.

This file is **not** authoritative for:
- item ontology, item profiles, or item instances,
- value, price, requisition, or economic exchange law,
- encounter timing for using or interrupting projects under pressure,
- health-state effects of medicines or restorative outputs,
- faction clearance, institutional permissions, or legal access in the broader sense,
- starting equipment or starting kit package law,
- platform-scale engineering doctrine,
- or settlement-scale industrial, civic, and infrastructure operations.

## Core design stance

Astra must be able to absorb donor systems where transformation work is expressed as:
- downtime fabrication,
- workshop throughput,
- formula-based creation,
- recipe-based creation,
- field repair,
- maintenance cycles,
- salvage harvesting,
- monster-part extraction,
- modular upgrades,
- host-slot installation,
- infusion or rune attachment,
- disassembly and reclamation,
- long-term projects,
- progress clocks,
- deterministic time-value throughput,
- check-gated progress,
- and highly abstract narrative project work.

Astra must therefore treat transformation as a doctrine layer rather than as a minor subsection under gear or wealth.

## Core doctrine terms

### Transformation project
A **transformation project** is any structured process that changes the material, functional, relational, or installed state of an item, material set, host, or system.

A transformation project always has:
- a starting state,
- a target state,
- required or optional inputs,
- one or more project gates,
- a progress model,
- one or more failure states,
- and an output state.

### Fabrication
**Fabrication** is the creation of a new object or object set from inputs that do not already constitute that completed object.

### Repair
**Repair** is the restoration of an extant but degraded object toward a more functional state without changing the identity of the host object into a different class of object.

### Salvage
**Salvage** is the recovery of reusable value, components, materials, or modules from an existing source object, creature, wreck, site, or failed project.

### Deconstruction
**Deconstruction** is intentional breakdown of an object into reusable inputs or a partial reconstitution state.
Deconstruction is a structured subtype of salvage rather than a separate unrelated doctrine.

### Refinement
**Refinement** is the transformation of one input class into a more usable, stable, purified, categorized, standardized, or application-ready input class.

### Modification
**Modification** is the alteration of an existing host such that its identity remains substantially continuous, but one or more capabilities, traits, profiles, tolerances, interfaces, or compatibilities change.

### Installation
**Installation** is the integration of a module, augment, upgrade, seal, component, toolhead, payload, rune, implant, or other sub-object into or onto a compatible host.

### Host
A **host** is the item, body, chassis, shell, frame, platform, or system that receives a modification or installation.

### Module
A **module** is a sub-object intended to be installed into, onto, or through a host relation.

### Project input
A **project input** is any material, component, formula, plan, tool, facility, labor contribution, catalyst, host, access right, or prerequisite object consumed, reserved, required, or referenced by a transformation project.

### Project gate
A **project gate** is any condition that must be satisfied before a project can begin or proceed.

### Progress model
A **progress model** is the rule family that determines how a project advances toward completion.

### Yield
**Yield** is the amount and quality of useful output obtained from a project.
Yield may include completed objects, partial outputs, recovered inputs, byproducts, residue, or failed remnants.

### Recoverability
**Recoverability** is the extent to which invested inputs, hosts, or progress can be restored, reclaimed, salvaged, or resumed after interruption, failure, or abandonment.

### Project state
A **project state** is the current status of a project in procedure.
At minimum, projects may be unstarted, staged, active, paused, blocked, failed, partially completed, completed, exhausted, or quarantined.

## Doctrine commitments

### 1. Transformation is broader than fabrication
Astra must not treat all project work as “make a new item.”
Repair, salvage, refinement, modification, and installation are distinct project families with different pressures, risks, and outputs.

### 2. Host continuity matters
Astra must preserve the difference between:
- changing an existing host,
- creating a replacement host,
- repairing an existing host,
- and extracting value from a failed or obsolete host.

### 3. Project grammar must be plural
Astra must not assume one universal progress model.
Different donor systems express project work as throughput, setup-plus-check, clock-based progress, staged advancement, repeated checks, one-step installation, or other lawful structures.

### 4. Inputs are broader than money
Astra must not assume every project consumes only generic value.
Projects may require raw materials, refined materials, salvage, formulas, recipes, plans, tools, workshops, catalysts, skill ranks, permission, host capacity, environmental conditions, labor, or special opportunities.

### 5. Project consequence must be preserved
Failure, interruption, haste, scarcity, partial completion, host damage, and reclaimability are real doctrine concerns.
Astra must not silently remove those pressures from donor systems where they materially matter.

### 6. Transformation pressure must be preserved
Conversion must preserve donor transformation pressure.
Astra must not normalize systems centered on harvesting, field repair, modular upgrades, long-term projects, or scarcity-gated fabrication into one generic “pay materials and wait” loop.
Astra must also not inflate lightweight or convenience-based systems into bookkeeping-heavy workshop simulations unless the donor truly relies on that pressure.

## Transformation doctrine

Every transformation project must be expressible as:
- **source state**,
- **target state**,
- **required inputs**,
- **optional inputs**,
- **gate classes**,
- **progress model**,
- **risk profile**,
- **output classes**,
- **recoverability profile**,
- **completion condition**.

This grammar is the stable Astra-native core.
Donor systems may vary in terminology, cost expression, pacing, or thematic dressing, but conversion work should map them into this structure whenever possible.

## Project families

### Fabrication doctrine
Fabrication covers projects that produce a new object, item instance, batch, dose set, module, component, structure element, or comparable output from inputs.

Fabrication may include:
- mundane gear creation,
- alchemical or consumable creation,
- ritual object creation,
- formula-based manufacture,
- engineered fabrication,
- assembly from prefabricated parts,
- and donor-specific object generation procedures.

Fabrication does **not** automatically imply full workshop downtime.
A donor may permit field fabrication, rapid fabrication, ritual fabrication, assisted fabrication, or abstract asset creation.

Fabrication should always classify:
- output identity class,
- output scale,
- whether the output is batch, single-copy, or modular,
- whether the project consumes a host,
- whether the project can be resumed,
- whether the project can be partially completed,
- whether the project generates scrap or residue,
- and whether the project creates a profile-known output or a novel/experimental output.

### Repair doctrine
Repair covers projects that restore a degraded but extant host toward functionality.

Repair must preserve the difference between:
- superficial restoration,
- operational restoration,
- structural restoration,
- temporary patching,
- field stabilization,
- and full restoration.

Repair must not be collapsed into fabrication.
A repaired object remains substantially the same host identity unless donor material explicitly treats the result as replacement or reconstruction.

Repair projects should classify:
- current host damage state,
- target restored state,
- whether patching is temporary or durable,
- whether functionality is partial or full,
- whether the repair introduces compromise, stress, or quality loss,
- and whether the host is still repairable or has crossed into rebuild-or-salvage territory.

### Salvage doctrine
Salvage covers projects that recover reusable value from an extant source.

Salvage sources may include:
- damaged or destroyed items,
- hostile entities or harvested bodies,
- wrecks,
- ruins,
- supply caches,
- environmental resources,
- failed projects,
- obsolete gear,
- or donor-specific extractable sources.

Salvage must classify:
- source class,
- extraction method,
- recoverable output class,
- recoverable quantity or tier,
- contamination or degradation risk,
- whether the source is consumed,
- whether the salvage is direct-use or requires refinement,
- and whether the result is deterministic, table-driven, profile-driven, or context-adjudicated.

Salvage is not loot generation.
Loot generation asks what enters play as reward.
Salvage asks what can be **recovered through procedure** from a given source.

### Deconstruction doctrine
Deconstruction is the deliberate breakdown of an item or host into parts, modules, scrap, ingredients, or transferable value.

Deconstruction is often similar to salvage, but its procedural emphasis is different:
- it may target a specific output,
- it may preserve specific modules,
- it may support rebuilding into a related host,
- and it may reclaim only a fraction of the original investment.

When useful, conversion may classify a salvage project as deconstruction-focused.

### Refinement doctrine
Refinement covers transformation from raw or unstable inputs into standardized, purified, classified, stabilized, or processed inputs.

Refinement may include:
- ore to ingots,
- herbs to reagent doses,
- harvested tissues to treated components,
- scrap to standardized fabrication media,
- residue to catalysts,
- raw essence to stable charge media,
- or donor-specific treatment, curing, distillation, purification, and preparation processes.

Refinement is often a precursor family.
Astra must preserve that some systems make refinement a meaningful project instead of assuming all inputs are immediately workshop-ready.

### Modification doctrine
Modification covers changes to an existing host that preserve host identity while altering properties.

Modification may include:
- tuning,
- reinforcing,
- resizing,
- recalibrating,
- adapting for a new bearer,
- changing compatibility,
- grafting new functions,
- applying enhancement layers,
- changing output profile,
- or donor-specific upgrade and personalization procedures.

Modification must be distinguished from fabrication of a new host and from one-time installation of a module.
A modified object remains the same host unless the donor meaningfully treats it as a new object identity.

### Installation doctrine
Installation covers projects where a module, augment, upgrade, seal, component, or other sub-object is integrated into a host.

Installation may include:
- socketing,
- mounting,
- embedding,
- plating,
- affixing,
- integrating,
- calibrating,
- linking,
- wiring,
- infusing,
- attuning,
- and donor-specific host-subhost procedures.

Installation must classify:
- module class,
- host class,
- compatibility requirements,
- slot or capacity usage,
- install time or install model,
- whether activation is immediate, delayed, staged, or conditioned,
- whether removal is possible,
- whether removal has cost or cooldown,
- and whether installation changes host identity, host statistics, host permissions, or host obligations.

Installation is not ordinary item use.
It is a structured transformation procedure.

## Project input grammar

A transformation project may depend on one or more of the following input classes.

### Material inputs
Physical or metaphysical substances consumed or reserved by the project.
Examples include raw materials, refined materials, reagents, cores, salvage stock, universal fabrication media, treated alloys, biological substrates, catalysts, and donor-specific essence-bearing matter.

### Component inputs
Discrete parts or subassemblies required to complete the output or alteration.

### Host inputs
Existing items, bodies, frames, shells, weapons, armor, or other hosts that are modified, repaired, installed into, or deconstructed.

### Knowledge inputs
Recipes, formulae, plans, patterns, blueprints, schematics, ritual sequences, calibration files, donor-specific know-how, or recognized exemplar references.

### Tool inputs
Required toolkits, instruments, rigs, interfaces, labs, forges, software suites, ritual kits, or donor-specific implements.

### Facility inputs
Workshops, stations, labs, bays, shrines, fabrication arrays, foundries, med-beds, drydocks, field benches, or other location-bound support environments.

### Labor inputs
Additional workers, assistants, specialists, summoned labor, automated systems, crew labor, or background support.

### Permission inputs
Clearances, legal rights, guild authority, faction approval, ritual sanction, donor-specific licenses, or restricted access conditions.

### Environmental inputs
Temperature bands, terrain context, biome access, celestial alignment, pressure, vacuum tolerance, mana field, power availability, local hazard conditions, or donor-specific environmental prerequisites.

### Access-right inputs
Keys, passes, trial rights, station access, docking access, or other bounded claims necessary to initiate or finish the project.

## Project gate doctrine

Astra recognizes the following project-gate families.
A donor project may use one or many.

### Competency gate
Whether the acting party possesses the required competency, training, proficiency, profession, tradition, or comparable ability basis.

### Knowledge gate
Whether the acting party possesses the needed formula, recipe, pattern, design, or equivalent knowledge permission.

### Tool gate
Whether the needed tools are available.

### Facility gate
Whether the needed workshop, bench, lab, forge, bay, station, shrine, or equivalent environment is available.

### Material gate
Whether required inputs are present in required form and quantity.

### Host gate
Whether the target host exists and is compatible, repairable, modifiable, install-capable, or otherwise valid for the project.

### Capacity gate
Whether the host or project context has sufficient slots, mount points, volume, tolerance, integrity margin, install room, or throughput room.

### Access gate
Whether the acting party has the right to perform the project on the host, at the location, or with the restricted materials involved.

### Legitimacy gate
Whether the project is lawful, sanctioned, tolerated, prohibited, or risky from a social or institutional perspective.

### Condition gate
Whether the project requires certain project-state, host-state, or environmental-state conditions before proceeding.

## Project progress-model doctrine

Astra must support multiple lawful progress models.
No one model is hidden default law.

### Throughput model
Project progress is measured as deterministic production or value throughput over time.
This model is common when workdays, labor contribution, or value-equivalent progress are primary.

### Setup-plus-check model
Project progress is measured through a setup period followed by one or more decisive checks.
Additional time may reduce final cost, increase yield, or improve stability.

### Clock or track model
Project progress is measured through discrete progress segments, clocks, milestones, or stages.
This model is common when long-term projects are abstracted into intermittent advancement.

### Repeated-check model
Project progress is made through recurring work checks where each successful contribution advances completion and failed contributions produce no progress or introduce risk.

### One-step install model
Project progress is effectively resolved in a short bounded procedure, often with compatibility or delay rules.
This is common for modular installation, transfer, swapping, and field servicing.

### Threshold model
Project progress is achieved once specific threshold conditions are satisfied, such as sufficient inputs, sufficient heat, sufficient charge, enough helper labor, or accumulated donor-specific readiness.

### Hybrid model
Some donor procedures combine two or more models.
Astra conversion may classify them as hybrid rather than forcing them into a single track.

## Project time doctrine

Project time must be expressible without hardcoding one donor pacing model.
Projects may use:
- encounter-scale time,
- scene-scale time,
- short field-work time,
- watch-scale time,
- downtime days,
- nonconsecutive workdays,
- campaign-clock advancement,
- or abstract progress windows.

Every project should classify:
- minimum working interval,
- whether work must be consecutive,
- whether interruption preserves progress,
- whether helpers can contribute,
- whether parallel work is possible,
- and whether reduced time increases risk or reduces quality.

## Labor and assistance doctrine

Astra must support:
- solo project work,
- cooperative work,
- assisted work,
- specialist contribution,
- hired labor,
- institutional support,
- automated support,
- and host-embedded self-calibration or self-repair where donor systems allow it.

Assistance may affect:
- project speed,
- material efficiency,
- success chance,
- yield,
- stability,
- or recoverability.

Assistance should not be assumed to help all projects equally.
Some projects scale by labor.
Some scale by expertise.
Some scale poorly at all.

## Host-state doctrine

Transformation procedure must preserve host-state distinctions.
At minimum, hosts may be classified as:
- pristine,
- functional,
- worn,
- degraded,
- damaged,
- impaired,
- unstable,
- broken,
- destroyed,
- salvageable,
- unrecoverable.

These states are doctrinal categories.
Donor systems may express them via durability tracks, hit points, usage dice, tags, quality bands, or narrative conditions.

### Key distinction: repair versus rebuild versus salvage
Astra must preserve the difference between:
- a host that can be repaired into functionality,
- a host that must be rebuilt or replaced,
- and a host that can only be broken down for salvage.

Repairable is not identical to intact.
Broken is not identical to destroyed.
Destroyed is not identical to unrecoverable.

## Output doctrine

Project outputs may be:
- completed host or object,
- partially completed host or object,
- temporary or unstable output,
- repaired output,
- improved output,
- installed host state,
- refined materials,
- reclaimed materials,
- reusable modules,
- byproducts,
- residue,
- scrap,
- waste,
- contamination,
- or failed remnants.

Astra must preserve whether a donor system treats outputs as:
- deterministic,
- yield-variable,
- check-variable,
- table-variable,
- source-profile-based,
- or GM/context adjudicated.

## Failure, risk, and consequence doctrine

Transformation projects may fail in different ways.
Astra must distinguish among at least the following failure classes.

### No-progress failure
The project does not advance, but invested inputs and host state remain largely preserved.

### Efficiency loss
The project advances poorly or expends extra inputs.

### Yield loss
The output is reduced in quantity, quality, stability, or reclaim value.

### Host damage
The host is worsened, stressed, downgraded, misaligned, contaminated, or rendered temporarily unusable.

### Input loss
Some or all reserved materials are consumed, spoiled, contaminated, or otherwise lost.

### Hazardous failure
The project creates danger, backlash, contamination, exposure, noise, attention, instability, or donor-specific negative fallout.

### Lockout or cooldown
The project cannot be retried immediately, or the host/module relation is temporarily blocked.

### Catastrophic failure
The project causes severe loss, destruction, curse, hostile activation, dangerous release, or other donor-significant collapse outcome.

Astra conversion must preserve which failure classes are materially possible in the donor procedure.

## Recoverability doctrine

Every project should classify what can be recovered after interruption, abandonment, or failure.

Recoverability may include:
- full progress preservation,
- partial progress preservation,
- host preservation without progress,
- reclaimed materials,
- reclaimed modules,
- scrap conversion,
- donor-specific salvage fractions,
- or total loss.

Astra must preserve the difference between:
- resumable projects,
- restart-only projects,
- salvageable failures,
- and terminal failures.

## Fabrication doctrine details

Fabrication projects should classify the following field families whenever relevant:
- output profile known / output profile experimental,
- single output / batch output,
- consumable / persistent output,
- ordinary / exceptional output,
- whether formulas or recipes are required,
- whether helper labor changes throughput,
- whether facility quality changes results,
- whether environmental sourcing matters,
- and whether fabrication can occur in field conditions.

Astra must not assume that all fabrication requires static workshop downtime.
Some donors emphasize camp craft, battle prep, modular assembly, or one-day production.
Others emphasize long laboratory or forge time.

## Repair doctrine details

Repair projects should classify:
- patch repair versus full repair,
- whether the repair restores only function or also quality,
- whether repeated repair degrades future performance,
- whether repair can be performed under field conditions,
- whether destroyed hosts are excluded,
- whether repair consumes standardized media or source-matched materials,
- whether repair restores durability fully or partially,
- and whether specific tool/facility kits are mandatory.

Repair should also support temporary stabilization, which restores usability or prevents further degradation without constituting full restoration.

## Salvage and harvest doctrine details

Astra must support both **object salvage** and **source harvest**.

### Object salvage
Object salvage extracts useful value from gear, wreckage, failed devices, broken modules, structures, or comparable non-creature sources.

### Source harvest
Source harvest extracts useful value from creatures, biological remains, botanical sources, elemental sources, environmental nodes, natural treasures, or other harvestable source classes.

Source harvest should classify:
- source class,
- extraction method,
- harvest time,
- usable-part scaling,
- deterministic versus rolled output,
- edible/useful/hazardous distinctions,
- refinement requirement,
- and whether special success thresholds unlock unusual treasure or premium yield.

Astra must preserve donor systems where harvesting is a meaningful gameplay loop rather than treating it as generic loot conversion.

## Refinement doctrine details

Refinement projects should classify:
- raw source class,
- refined output class,
- purity or stability change,
- batch size,
- spoilage or contamination risk,
- whether refinement is reversible,
- whether refinement unlocks new project families,
- and whether waste or byproduct is generated.

Refinement often functions as the bridge between salvage/harvest and fabrication.
Astra must leave room for that bridge explicitly.

## Modification doctrine details

Modification must support changes to an existing host without forcing host replacement.

Modification may affect:
- trait profile,
- compatibility profile,
- capacity profile,
- output performance,
- durability,
- ergonomics,
- concealment,
- elemental or damage interface,
- bearer permissions,
- modularity,
- or donor-specific special behavior.

Modification should classify:
- reversible / irreversible,
- additive / substitutive,
- cosmetic / functional / transformational,
- whether the modification occupies capacity,
- whether multiple modifications stack,
- whether the host must be stripped or stabilized first,
- and whether the project can preserve the host during interruption.

## Installation doctrine details

Installation must support host-subhost relations as a first-class Astra pattern.

### Installation fields
An installation-capable project should classify:
- host class,
- module class,
- compatibility rule,
- slot or mount usage,
- install duration,
- activation delay,
- removal time,
- removal conditions,
- removal penalties or cooldown,
- whether the host continues to function if over-capacity,
- whether the host must be inactive, stripped, powered down, sedated, sanctified, or otherwise prepared,
- and whether installation changes future repair or modification rules.

### Installation versus attunement
Installation is not identical to attunement, tuning, or permissions binding.
A donor may combine these, but Astra should keep them analytically distinct.
A module may be physically installed yet not tuned, attuned, authorized, or bonded.

### Installation versus use
A module may be installed without becoming active immediately.
Installation procedure and operational use procedure are separate layers.

## Knowledge doctrine

Astra must support multiple knowledge regimes.
Projects may be:
- common and generally known,
- recipe or formula gated,
- blueprint or schematic gated,
- reverse-engineered,
- invented or innovated,
- learned from a teacher or institution,
- donor-specifically inherited or bonded,
- or unknown and research-gated.

Knowledge does not have to be binary.
Projects may be:
- fully known,
- partially known,
- inferred,
- experimentally approximated,
- mis-specified,
- or quarantined pending doctrine.

## Experimental and novel project doctrine

Some donor systems explicitly support invention, tinkering, prototype work, or improvised project definition.
Astra must not force all projects to be pre-cataloged.

A novel project should be classifiable by:
- target function,
- intended output class,
- precedent class,
- required innovation level,
- adjudication burden,
- uncertainty class,
- and whether it becomes a reusable known profile if completed.

This file does not define the content catalog for such projects.
It defines the lawful project shape so later content can do so without hallucinated structure.

## Progress-pressure doctrine

Progress should preserve donor-facing pressure in at least these dimensions:
- time burden,
- material burden,
- knowledge burden,
- access burden,
- failure burden,
- scarcity burden,
- host-risk burden,
- and opportunity-cost burden.

Astra conversion must preserve whichever of these are materially central to the donor construct.
It should not fabricate extra burdens merely for flavor.
It also must not erase important burdens simply because they are inconvenient.

## Quality and result-grade doctrine

Projects may produce outputs of different result grade.
Astra should support, when relevant:
- failed output,
- compromised output,
- standard output,
- high-quality output,
- critical or exceptional output,
- and unstable or cursed output.

Quality grade may affect:
- durability,
- performance,
- value,
- compatibility,
- backlash risk,
- install tolerance,
- and downstream recoverability.

## Project relation to downtime and scene play

B05 defines transformation procedure.
It does not decide by itself whether a project is:
- encounter-scale,
- scene-scale,
- downtime-scale,
- background-scale,
- institution-scale,
- or platform-scale.

Those relations are determined through handoff to B01, B11, B12, B14, and B15 as appropriate.

B05 should therefore define project structure in a time-scale-neutral way unless a specific conversion explicitly maps a donor procedure to a specific pacing frame.

## Transformation preservation invariants

### Invariant 1: preserve donor project family
Do not collapse salvage, repair, modification, refinement, and installation into generic crafting if the donor distinguishes them.

### Invariant 2: preserve donor host continuity
Do not treat a donor modification or repair as new fabrication unless the donor meaningfully treats it that way.

### Invariant 3: preserve donor progress logic
Do not replace a donor long-term project, repeated-check process, throughput model, or instant-install model with a different model merely for convenience.

### Invariant 4: preserve donor reclaimability
Do not erase differences between recoverable failure, salvageable loss, and catastrophic total loss.

### Invariant 5: preserve donor gating pressure
Do not collapse formulas, facilities, competencies, host compatibility, rarity access, or legality into one generic skill gate.

### Invariant 6: preserve donor transformation pressure
Do not turn a transformation-heavy donor ecosystem into generic shopping-by-another-name.
Do not turn a light-touch donor ecosystem into a burdensome industrial simulator.

## Lawful incomplete mapping

For a corpus of this size, B05 must explicitly allow incomplete but lawful mappings.
A project conversion may be classified as:

### Directly mapped
The donor project cleanly maps to an Astra project family, input set, gate set, progress model, and output structure.

### Normalized
The donor project is translated into Astra terms with minor abstraction, but its core pressure and family remain intact.

### Family-assigned
The donor construct clearly belongs to a project family, but some input, timing, or failure specifics remain open.

### Profile-assigned
The output or host relation is clear, but the full project procedure is not yet fully specified.

### Placeholder-procedural
The donor clearly implies a lawful project, but Astra lacks enough current doctrine detail to complete a fully confident mapping.

### Quarantined
The donor construct cannot yet be converted without inventing unsupported law or violating current doctrine boundaries.

No false certainty should be introduced merely to fill an incomplete project mapping.

## Mandatory subsystem handoff map

This handoff map is mandatory.
If a rule question primarily belongs to one of the following files, B05 must defer accordingly.

- **Item ontology, item profiles, item instances, host/module schema, install relation fields** -> `batchB_03_equipment_item_and_gear_object_model.md`
- **Value, price, requisition, trade, access-right economics, scarcity, market regime** -> `batchB_04_wealth_currency_requisition_trade_and_value_framework.md`
- **Encounter timing, interruptions, action windows, scene pressure during active project work** -> `batchB_01_scene_conflict_action_and_encounter_procedure.md`
- **Health consequences, treatment outputs, restoration meaning, bodily survivability effects** -> `batchB_02_health_injury_healing_death_and_recovery_framework.md`
- **Travel, expedition pacing, route-based field project context** -> `batchB_06_exploration_travel_navigation_time_and_distance.md`
- **Environmental hazards, radiation, weather, contamination sources, regional afflictive context** -> `batchB_07_environment_hazards_weather_regions_and_afflictions.md`
- **Downtime scheduling, long recovery intervals, service cycles, project time allocation** -> `batchB_11_downtime_rest_training_projects_and_services.md`
- **Faction access, guild support, institutional work orders, restricted facilities, sanctioned project access** -> `batchB_12_factions_institutions_clearance_and_service_access.md`
- **Companions, drones, summons, auxiliary entities as project participants or hosts** -> `batchB_13_companions_retinues_summons_drones_and_auxiliary_entities.md`
- **Mounts, vehicles, mechs, ships, and platform-scale module operations** -> `batchB_14_mounts_vehicles_mechs_ships_and_platform_operations.md`
- **Settlement-scale workshops, industrial districts, civic processing, and infrastructure-level fabrication** -> `batchB_15_settlements_bases_capitals_and_infrastructure_operations.md`
- **Post-encounter inflow, loot intake, salvage opportunities after conflict, reward distribution** -> `batchB_16_loot_rewards_salvage_and_post_encounter_inflows.md`
- **Competency and skill translation architecture** -> `batchA_05_competency_and_skill_translation_architecture.md`
- **Permissions, access tags, bearer gates, compatibility rights, proficiency gates** -> `batchA_06_access_tags_permissions_and_proficiency_gates.md`
- **Ability payloads granted by completed projects or installed modules** -> `batchA_07_ability_object_model.md`
- **Charges, recharge, fuel, heat, backlash, recovery cycles, consumptive resource law** -> `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`
- **Condition meanings, ongoing effect definitions, contamination tags, status semantics** -> `batchA_08_status_condition_and_effect_architecture.md`
- **Damage-family meanings and interaction law** -> `batchA_09_damage_family_and_resistance_taxonomy.md` and `batchA_09b_damage_fusion_and_compound_interactions.md`
- **Starting loadouts and entry packages** -> `batchA_14_starting_loadout_and_kit_framework.md`
- **Cross-conversion guardrails and doctrine preservation constraints** -> `batchA_15_conversion_invariants.md`

## Anti-drift rule

If B05 begins absorbing:
- a market system,
- a loot table system,
- a full downtime calendar,
- a vehicle engineering chapter,
- a settlement production chapter,
- a medical consequences chapter,
- or a giant content catalog of recipes and blueprints,
that is doctrinal drift.

B05 is the **transformation-procedure doctrine file**.
It defines lawful project families and project grammar.
It does not replace content catalogs, economy doctrine, or platform operations.

## Outcome

When used correctly, this file allows Astra conversion to represent donor project systems in a stable, non-hallucinatory way by answering the following questions cleanly:
- what kind of transformation is this,
- what is the source state,
- what is the target state,
- what inputs and gates matter,
- how does progress occur,
- what can fail and how,
- what can be recovered,
- what outputs are created,
- and which adjacent doctrine file owns the next layer of meaning.

That is the core Astra-native job of B05.
