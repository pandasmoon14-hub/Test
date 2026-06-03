# B06 Project, Crafting, Salvage, Repair, and Upgrade Procedure

## 1. Purpose and status

B06 is the sixth Batch B operational doctrine draft for Astra project-centered interval work: crafting, salvage processing, repair, maintenance, modification, upgrade, object work, facility-supported work, material requirement handling, contributors, partial completion, complications, interruption, pause/resume, abandonment, and project output routing. It sits after B01 scene/activity/encounter procedure, B02 action declaration/cost commitment/resolution trigger procedure, B03 item/gear/equipment/object-system construct and asset-use procedure, B04 inventory/storage/custody/burden procedure, and B05 acquisition/reward/requisition/value-flow procedure.

Status posture:
- This file is Batch B operational-procedure draft material.
- This file is not current canon, not final mechanics, not runtime authority, not sourcebook prose, and not player-facing rule text.
- C00 remains the schema handoff control surface for Batch B to C-family routing.
- B06 treats B01, B02, B03, B04, and B05 as upstream Batch B context and must build on them, not rewrite them.
- D00, D02, D03, D05, D09, D12, D13, D17, and D19 source-pack files are referenced only as draft source-pack/reference material. They are not current doctrine authority, final mechanics, runtime authority, canon, sourcebook prose, or Astra defaults.
- B06 records, examples, and handoff blocks are doctrine-facing only; they are not runtime state, backend contracts, sourcebook statblocks, canon entries, player-facing rule text, accepted lexicon, final project schemas, final crafting rules, final repair math, final salvage yield tables, final upgrade rules, or final mechanics.

Required reference boundaries preserved by B06:
- `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md` for upstream scene, activity, encounter, transition, checkpoint, and owner-file handoff procedure.
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` for upstream action declaration, feasibility, cost commitment, resolution trigger, no-roll/roll-trigger, and action-to-delta procedure.
- `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md` for item, gear, equipment, object-system construct, object readiness, object use, object-state handoff, and asset-use routing procedure.
- `docs/doctrine/operations/batch_b/B04_inventory_storage_custody_and_burden_procedure.md` for inventory, storage, custody, possession, access, burden, lawful loss, recovery, and inventory/custody routing procedure.
- `docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md` for acquisition, reward, requisition, scarcity, upkeep, value sink, value commitment, market access, and value-flow routing procedure.
- `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` for shared Batch C base fields, `pending_schema`, source-local boundary, rejected donor element, canon eligibility, review routing, provenance, and missing-schema fallback language.
- `docs/doctrine/native_design/d_series/source_packs/astra_d00_doctrine_pack_v0_1/D00-03_state_delta_commit_protocol.md` for the draft source-pack principle that every meaningful action commits at least one delta to a recognized owner, while B06 does not own every delta format.
- `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-00_resolution_architecture_and_owner_boundaries.md` for draft resolution owner boundaries, while B06 must not define final resolution mechanics.
- `docs/doctrine/native_design/d_series/source_packs/astra_d03_doctrine_pack_v0_1/astra_d03_doctrine_pack_v0_1/D03_01_power_economy_lattice.md` for draft power/economy pressure source material, while B06 must not define final power, rarity, tier, progression, or economy law.
- `docs/doctrine/native_design/d_series/source_packs/astra_d05_doctrine_pack_v0_1/D05-04_training_practice_teachers_and_downtime.md` and `D05-05_research_experimentation_and_theorycraft.md` for draft competency, practice, research, experimentation, and downtime source material, while B06 must not define final training advancement or research truth procedure.
- `docs/doctrine/native_design/d_series/source_packs/astra_d09_doctrine_pack_v0_1/D09-06_crafting_repair_salvage_modification_upgrade_and_requisition_interface.md` for draft crafting, repair, salvage, modification, upgrade, maintenance, and requisition interface source material, while B06 must not define final crafting, repair, salvage, upgrade, modification, item, or requisition mechanics.
- `docs/doctrine/native_design/d_series/source_packs/D12_time_action_cadence_encounter_and_turn_procedure_doctrine_pack/D12_doctrine_pack/D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md` for draft checkpoint, cost commitment, consequence timing, and handoff source material, while B06 must not define final cadence or runtime timing state.
- D13 source-pack files `D13-00` through `D13-07` for draft downtime project, project anatomy, requirement discovery, interval setup, progress outcomes, project families, owner handoffs, concurrent contributors, materials, support burden, source-local project mapping, and not-final record source material, while B06 must not promote D13 records to final schema or donor downtime systems.
- `docs/doctrine/native_design/d_series/source_packs/D17_economy_acquisition_inventory_reward_and_requisition_doctrine_pack/D17_doctrine_pack/D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md` for draft upkeep, requisition, consumption, value sink, and economic pressure source material, while B06 must not define final economy law.
- `docs/doctrine/native_design/d_series/source_packs/D19_cross_pack_integration_conflict_audit_and_conversion_readiness_capstone_pack/D19_capstone_doctrine_pack/D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md` for draft record-shape governance warnings, while B06 must not invent final record shapes.

## 2. Owner layer

B06 belongs to Batch B operational doctrine. It routes procedure between upstream Batch B operational files, the C00 schema handoff control surface, future C01-C14 schema families, project/crafting owner files, source-local donor procedure quarantine, and later runtime/canon/training owners.

B06 may identify that project work exists, classify project-facing pressure, preview requirement/cost/risk categories, set up doctrine-facing interval handling, and route outputs. B06 must not perform final schema, final math, final item-stat, final economy, final facility, final recipe, final downtime, runtime-state, canon, or player-facing rule work. If B06 cannot identify a valid owner or schema family, it must mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` instead of inventing authority.

## 3. What B06 owns

B06 owns doctrine-level operational procedure for:
- project/long-task intake after B01-B05 produce interval-scale work pressure;
- project intent, goal, family, scope, requirement, cost/risk, commitment, and interval setup routing;
- project-family classification for crafting, salvage, repair, maintenance, modification, upgrade, preparation, resource gathering, facility work, contributor-supported work, and source-local long-task work;
- crafting as project routing, not final crafting rules;
- salvage processing as project routing, not automatic wealth/material generation;
- repair and maintenance as project routing, not final repair math;
- modification and upgrade as project routing, not item-level hardpoint law, final item stats, or universal item leveling;
- requirement discovery and protected-hidden requirement handling;
- material, component, schematic, recipe, blueprint, toolchain, facility, assistant, crew, license, permission, and source-local requirement routing;
- interval commitment and committed-cost handling;
- progress, partial completion, stalled, blocked, complicated, damaged, interrupted, completed, failed, abandoned, quarantined, and escalated outcome routing;
- project complication classification and owner-file routing;
- project pause, resume, interruption, abandonment, archival, and follow-up handoff procedure;
- concurrent project, contributor, facility, material, and support-burden routing;
- project output routing to B03 object owners, B04 inventory/custody owners, B05 value-flow owners, D05 competency/research owners, D07 harm owners, D10 world/faction/law owners, D13-style project owners, and later runtime/canon/schema owners;
- B06-to-C00/C-family handoff references when project/crafting/salvage/repair/upgrade handling produces conversion records;
- source-local donor downtime/crafting/salvage/repair/upgrade/project-system quarantine and escalation rules;
- examples of good and bad B06 usage;
- minimum assertions and acceptance criteria for B06.

## 4. What B06 must not own

B06 must not define or promote:
- final project schema;
- final crafting schema;
- final object schema;
- final inventory schema;
- final economy schema;
- C-family schema fields;
- C01-C14 schema contents;
- final crafting math;
- final repair math;
- final salvage yield tables;
- final upgrade math;
- final modification rules;
- final item stats;
- final item rarity/tier law;
- final material economy;
- final recipe system;
- final schematic/blueprint rules;
- final facility rules;
- final tool proficiency rules;
- final downtime activity menu;
- final project-clock system;
- final universal progress-point system;
- final recovery rules;
- final training advancement;
- final research truth procedure;
- final crafting DCs;
- final crafting costs per day;
- final donor downtime turns;
- final donor long-rest/short-rest procedures;
- final sourcebook crafting, repair, salvage, upgrade, or downtime rules;
- final requisition authority;
- final market/economy law;
- final advancement/progression reward pacing;
- runtime project state;
- final runtime project state;
- runtime inventory state;
- runtime object state;
- runtime economy ledger;
- runtime entity/component/event/state schemas;
- persistent campaign state;
- command lifecycle implementation;
- context packet compiler;
- hidden-information runtime state;
- live-play narration behavior;
- final canon promotion;
- accepted lexicon terms;
- sourcebook prose;
- donor crafting/downtime/project systems as Astra defaults.

## 5. Non-collapse rule

A project is not automatically downtime. Downtime is not automatically safe time. Crafting is not a recipe table. Repair is not automatic restoration. Maintenance is not invisible bookkeeping. Salvage is not free material or wealth. Modification is not always improvement. Upgrade is not universal item leveling.

B06 keeps these categories separate:
- a B01 `freeform_scene`, `focused_activity`, or `structured_encounter` may produce project pressure, but B06 does not rewrite scene or encounter procedure;
- a B02 action declaration may commit a cost or trigger resolution, but B06 does not rewrite action feasibility, roll triggers, or no-roll routing;
- a B03 object may be crafted, damaged, altered, upgraded, dismantled, maintained, or placed under work, but B06 does not define object schema, item stats, hardpoints, or object-state math;
- a B04 inventory/custody/burden issue may constrain a project, but B06 does not define inventory schema or runtime inventory state;
- a B05 value, reward, requisition, scarcity, upkeep, or value sink may feed a project, but B06 does not define final economy law, price, market, requisition, or value-conversion math;
- a D05-style training or research activity may become a handoff, but B06 does not own training advancement, research truth, or donor downtime menus.

Every meaningful project/crafting/salvage/repair/upgrade state-delta routing event must route at least one delta to a recognized owner or explicitly produce a no-delta, quarantine, escalation, transition, source-local, `pending_schema`, `human_review`, or `defer_until_schema_exists` result. Missing requirement coverage does not authorize invention, and hidden requirement pressure may be marked without revealing hidden truth.

## 6. Project, interval, requirement, commitment, and output definitions

For B06 purposes:
- A `project` is a doctrine-facing container for work that cannot be safely resolved as a single B01/B02 action without losing interval, requirement, owner, cost, risk, contributor, facility, custody, object-state, or output-routing pressure.
- An `interval` is a bounded work window used to route commitment, progress triggers, interruption windows, and output handoffs. It is not a final downtime turn, final project clock, final universal progress-point unit, or runtime timer.
- A `requirement` is a condition, resource, permission, prerequisite, owner approval, hidden condition, source-local condition, or schema dependency that must be checked or routed before or during work.
- A `commitment` is a doctrine-facing declaration that time, material, value, facility access, toolchain access, contributor labor, object custody, license, permission, exposure, opportunity cost, obligation, or source-local cost is reserved or accepted for project work.
- An `output` is a result of project routing: an object-state handoff, custody handoff, value-flow handoff, requirement update, partial output, transition note, owner-file escalation, quarantine note, or no-delta result. It is not automatically a new item, value, schema row, canon entry, or player-facing reward.

B06 uses the following vocabulary as doctrine-facing labels only. These labels are not final schemas, accepted lexicon, runtime state, or sourcebook terms.

Project families:
- `crafting`
- `salvage`
- `repair`
- `maintenance`
- `modification`
- `upgrade`
- `installation_preparation`
- `resource_gathering`
- `preparation`
- `facility_work`
- `contributor_supported_work`
- `recovery_handoff`
- `training_handoff`
- `research_handoff`
- `faction_support_handoff`
- `social_handoff`
- `source_local_project`
- `mixed_project`
- `unknown_project`

Project scope bands:
- `minor`
- `standard`
- `major`
- `extended`
- `transformational`
- `source_local_scope`
- `unknown_scope`

Requirement states:
- `met`
- `missing`
- `unknown`
- `protected_hidden`
- `blocked_by_owner_file`
- `source_local`
- `quarantined`
- `deferred_until_schema_exists`

Commitment types:
- `time_block`
- `materials_reserved`
- `value_committed`
- `facility_claimed`
- `toolchain_committed`
- `schematic_committed`
- `contributor_assigned`
- `crew_assigned`
- `license_or_permission_committed`
- `object_placed_under_work`
- `exposure_accepted`
- `opportunity_cost_accepted`
- `obligation_accepted`
- `source_local_commitment`
- `unknown_commitment`

Interval outcome states:
- `advanced`
- `advanced_with_cost`
- `partial`
- `stalled`
- `blocked`
- `complicated`
- `damaged`
- `interrupted`
- `completed`
- `completed_with_complication`
- `failed`
- `abandoned`
- `quarantined`
- `escalated`

Complication families:
- `cost_increase`
- `delay`
- `material_loss`
- `tool_or_facility_damage`
- `contributor_risk`
- `injury_or_condition_setback`
- `corruption_or_instability_pressure`
- `object_instability`
- `contamination`
- `schematic_error`
- `recipe_mismatch`
- `incompatible_component`
- `legal_exposure`
- `social_scrutiny`
- `faction_attention`
- `scarcity_pressure`
- `value_sink_triggered`
- `information_false_lead`
- `hidden_pressure_surface`
- `active_scene_trigger`
- `source_local_threat`
- `owner_file_gap`

Project output states:
- `no_delta_required`
- `requirement_identified`
- `requirement_satisfied`
- `object_created`
- `object_repaired`
- `object_maintained`
- `object_modified`
- `object_upgraded`
- `object_field_patched`
- `salvage_recovered`
- `salvage_contaminated`
- `material_gathered`
- `schematic_created`
- `schematic_interpreted`
- `recipe_discovered`
- `facility_prepared`
- `contributor_committed`
- `value_committed`
- `value_spent`
- `obligation_created`
- `ownership_disputed`
- `custody_routed`
- `partial_output`
- `flawed_output`
- `dangerous_output`
- `project_archived`
- `owner_routed`
- `transition_note`
- `source_local_retained_effect`
- `quarantined_unresolved_delta`
- `owner_file_escalation`

## 7. Project/long-task intake procedure

B06 intake begins only after upstream procedure produces interval-scale work pressure. Common triggers include:
- B01 identifies an extended activity, project-like scene goal, interruption window, facility scene, preparation phase, or owner-file handoff that exceeds scene procedure.
- B02 identifies a declared action whose cost, uncertainty, risk, resolution trigger, or required setup cannot be safely resolved as one action.
- B03 identifies object construction, repair, maintenance, dismantling, alteration, installation, upgrade, object instability, missing readiness, or object-state work.
- B04 identifies custody, storage, access, burden, possession, transport, lawful loss, or recovery pressure that constrains interval work.
- B05 identifies acquisition, reward, salvage, requisition, upkeep, scarcity, value sink, value commitment, or market-access pressure that requires project routing.
- D05-style competency or research pressure appears but must be handed to training/research owners rather than resolved by B06.
- A source-local donor system presents downtime, crafting, salvage, repair, upgrade, or project rules that must be quarantined, mapped, or escalated.

Intake procedure:
1. Identify the upstream trigger and preserve the upstream owner boundary.
2. State the project-facing intent in plain doctrine-facing language.
3. Classify the project family and provisional scope band.
4. Identify known, unknown, missing, protected-hidden, source-local, and schema-blocked requirements.
5. Identify likely commitments and whether any commitment has already been made under B02, B04, or B05.
6. Preview cost/risk categories without setting final math.
7. Identify output owners before resolving progress.
8. If safe owner coverage exists, set an interval setup note; if not, mark quarantine, escalation, `pending_schema`, `human_review`, or `defer_until_schema_exists`.

A project may begin inside a scene, during travel, during a recovery period, during institutional service, during an active threat, or during downtime. None of those contexts automatically makes the project safe, quiet, complete, legal, affordable, or invisible.

## 8. Intent, goal, family, and scope classification

B06 classifies a project by intent, goal, family, and scope before selecting procedure.

Intent classification asks:
- What is the actor trying to make, restore, maintain, alter, improve, dismantle, prepare, gather, learn, support, or route?
- Is the desired result an object, material, facility state, contributor assignment, value outcome, research/training handoff, custody transition, faction support, social arrangement, or source-local retained effect?
- Does the work target an existing object, a missing object, an abstract resource, a facility, a contributor group, a legal permission, or an unknown owner file?

Goal classification asks:
- Is the goal measurable enough for a doctrine-facing output state?
- Does the goal require hidden information, protected requirements, owner-file truth, source-local retained mechanics, or later schema?
- Is the goal compatible with the actor's known permissions, custody, access, facilities, materials, and obligations?

Family classification uses the vocabulary in section 6. Use `mixed_project` when multiple family procedures are materially involved. Use `unknown_project` when the intent cannot be safely classified. Use `source_local_project` when the source's own downtime/crafting/project system must be retained only as quarantined source-local evidence.

Scope classification uses the vocabulary in section 6. Scope is not a numeric time/cost rule. Scope describes doctrine-facing magnitude and owner pressure:
- `minor`: limited work with low owner surface and likely simple handoff.
- `standard`: ordinary project work with clear requirements and at least one output owner.
- `major`: project work with multiple requirements, meaningful costs, or multiple owners.
- `extended`: project work spanning multiple intervals, locations, contributors, facilities, or obligations.
- `transformational`: project work that may alter object identity, social/legal status, capabilities, canon eligibility, power pacing, world state, or owner-file truths.
- `source_local_scope`: scope is retained from donor/source procedure and cannot be safely converted yet.
- `unknown_scope`: insufficient doctrine or schema coverage exists.

## 9. Requirement discovery and protected-hidden requirement handling

Requirement discovery identifies what must be present, known, owned, permitted, committed, reserved, safe, legal, or routed before project progress can be recognized. A requirement is not automatically visible. A missing requirement does not authorize invention. A hidden requirement may be marked without revealing hidden truth.

Requirement categories may include:
- material, component, consumable, fuel, power source, salvage feedstock, stable workspace, environmental condition, or safety condition;
- schematic, recipe, blueprint, procedure note, source-local instruction, research result, or expert interpretation;
- toolchain, specialized apparatus, facility, workshop, lab, forge, dock, medical bay, hangar, containment, storage, or transport support;
- assistant, contributor, crew, teacher, supervisor, sponsor, faction support, institutional authority, license, permit, warrant, or permission;
- object custody, ownership, access, lawful claim, burden capacity, security, storage, or recovery route;
- value commitment, upkeep, scarcity exposure, opportunity cost, obligation, requisition approval, ration, market access, or value sink;
- hidden incompatibility, contamination, instability, legal exposure, faction attention, injury risk, active threat, or owner-file truth;
- schema coverage, conversion record need, canon eligibility, source-local boundary, or rejected donor element tracking.

Requirement state procedure:
1. Mark each known requirement as `met`, `missing`, `unknown`, `protected_hidden`, `blocked_by_owner_file`, `source_local`, `quarantined`, or `deferred_until_schema_exists`.
2. Do not reveal protected-hidden facts. It is sufficient to mark that a protected-hidden requirement exists, that progress is blocked or risky, or that an owner-file review is required.
3. Route object requirements to B03/object owners; custody/access/burden requirements to B04; value/scarcity/requisition/upkeep requirements to B05; training/research requirements to D05-style owners; harm/condition requirements to D07-style owners; world/faction/law requirements to D10-style owners; project lifecycle requirements to D13-style owners; schema requirements to C00/C-family owners.
4. If a requirement is missing and no owner can define it, use quarantine, escalation, `pending_schema`, `human_review`, or `defer_until_schema_exists`.
5. If a donor/source-local rule supplies a requirement, mark the source-local boundary and rejected donor elements instead of promoting it.

## 10. Cost/risk preview and commitment procedure

B06 previews cost and risk before interval work is committed. This preview is doctrine-facing and must not define final costs, final DCs, final prices, final crafting rates, final repair math, final salvage yield, final upgrade math, or final value conversion.

Cost/risk preview may identify:
- time exposure and interruption windows;
- material reservation, material loss, contaminated material, incompatible components, or opportunity cost;
- value commitment, value spent, upkeep, scarcity, rationing, requisition conditions, debt, obligation, or value sink;
- facility claim, toolchain commitment, storage needs, transport burden, safety setup, or access control;
- contributor assignment, crew risk, assistant availability, labor compensation, social scrutiny, or faction attention;
- object custody, object instability, object damage risk, degraded function, unsafe modification, or identity change;
- legal permission, license, permit, restricted work, property claim, liability, or illicit exposure;
- injury, condition setback, contamination, corruption, instability, or active-scene trigger;
- schema gap, owner-file gap, protected-hidden requirement, source-local retained effect, or donor-system quarantine.

Commitment procedure:
1. Identify which commitment types apply: `time_block`, `materials_reserved`, `value_committed`, `facility_claimed`, `toolchain_committed`, `schematic_committed`, `contributor_assigned`, `crew_assigned`, `license_or_permission_committed`, `object_placed_under_work`, `exposure_accepted`, `opportunity_cost_accepted`, `obligation_accepted`, `source_local_commitment`, or `unknown_commitment`.
2. Confirm whether the actor can make the commitment under B02 cost commitment, B04 custody/access/burden, and B05 value/requisition/scarcity procedure.
3. Record committed costs only as doctrine-facing routing facts, not runtime ledgers.
4. If acceleration is requested, require owner-supported cost/risk exposure. Acceleration is not free, not automatic, and not a universal progress rule.
5. If commitment is blocked, mark `blocked`, `quarantined`, `escalated`, `human_review`, or `defer_until_schema_exists`.

## 11. Interval setup and progress-trigger procedure

Interval setup defines when project work can be checked or routed. It does not define a final downtime turn, final project clock, universal progress-point system, runtime timer, or sourcebook schedule.

Interval setup procedure:
1. Name the project-facing intent, family, and scope.
2. Identify the interval context: scene-adjacent, travel-adjacent, downtime-adjacent, facility-supported, contributor-supported, recovery-linked, faction-supported, source-local, or unknown.
3. Confirm requirement states and committed-cost states.
4. Identify interruption windows and unsafe-time pressure. Downtime is not automatically safe time.
5. Identify progress triggers: completion of a work interval, resolution of a blocked requirement, arrival of materials, facility access, contributor availability, object inspection, value commitment, owner-file approval, research/training handoff, or source-local escalation.
6. Identify likely output owners before progress is recognized.
7. If no safe progress trigger exists, route to `blocked`, `quarantined`, `owner_file_escalation`, `pending_schema`, or `defer_until_schema_exists`.

Progress may be qualitative, staged, owner-routed, partial, blocked, complicated, or no-delta. Progress is not always numeric.

## 12. Crafting project procedure

Crafting under B06 means project routing toward creating or assembling an object, component, consumable, preparation, facility state, or other output. Crafting is not a recipe table, final crafting math, final crafting schema, final crafting DC, final cost-per-day rule, sourcebook crafting rule, or donor downtime system.

Crafting procedure:
1. Confirm that the intent is creation, assembly, preparation, or fabrication rather than repair, maintenance, modification, upgrade, salvage, training, research, acquisition, or pure object use.
2. Classify the family as `crafting`, `preparation`, `facility_work`, `resource_gathering`, `mixed_project`, `source_local_project`, or `unknown_project` as appropriate.
3. Identify requirements: materials, components, schematic, recipe, blueprint, toolchain, facility, contributor, license/permission, custody, value, safety condition, source-local rule, and schema coverage.
4. Route object identity, object capabilities, object readiness, object damage, item stats, and object-state outcomes to B03/object owners.
5. Route inventory, storage, possession, custody, burden, access, and lawful recovery to B04.
6. Route material acquisition, requisition, scarcity, value spent, value committed, upkeep, and market access to B05.
7. Route competency, instruction, theorycraft, experimentation, and research truth to D05-style owners when crafting depends on knowledge or learning.
8. Mark output as `object_created`, `partial_output`, `flawed_output`, `dangerous_output`, `requirement_identified`, `owner_routed`, `quarantined_unresolved_delta`, or another B06 output state.

A schematic is not final permission. A recipe is not final mechanics. A toolchain is not a skill bonus. A facility is not automatic success.

## 13. Salvage processing project procedure

Salvage under B06 means project routing for identifying, extracting, stabilizing, decontaminating, sorting, repurposing, claiming, transporting, or processing remains, wreckage, leftovers, failed projects, battlefield remnants, recovered parts, or source-local material. Salvage is not free material or wealth and does not automatically generate value, components, crafting inputs, ownership, legality, or safe use.

Salvage processing procedure:
1. Confirm whether the trigger is B03 object state, B04 custody/recovery, B05 salvage/value-flow, B01 scene aftermath, B02 declared dismantling, or source-local donor salvage.
2. Identify what is being processed and whether it is object, material, value, hazard, evidence, property, contamination, faction claim, or unknown residue.
3. Classify requirements: access, ownership claim, lawful permission, safe handling, toolchain, facility, containment, transport, appraisal, decontamination, contributor risk, value commitment, and schema coverage.
4. Route object damage, dismantling, function, instability, contamination, and reuse questions to B03/object owners.
5. Route custody, possession, storage, transport burden, legal recovery, and disputed holding to B04.
6. Route value, claim, acquisition channel, scarcity, market access, requisition, reward, and value sink pressure to B05.
7. Route harm, contamination, corruption, infection, injury, or condition pressure to D07-style harm owners.
8. Route law, faction claim, restricted material, evidence, liability, or social scrutiny to D10-style world/faction/law owners.
9. Mark output as `salvage_recovered`, `salvage_contaminated`, `material_gathered`, `ownership_disputed`, `custody_routed`, `value_committed`, `partial_output`, `dangerous_output`, `owner_routed`, or `quarantined_unresolved_delta`.

B06 must not define salvage yield tables, salvage prices, final material economy, automatic loot conversion, or donor salvage systems as Astra defaults.

## 14. Repair and maintenance project procedure

Repair under B06 means project routing for restoring, stabilizing, replacing, patching, or making an object usable after damage, wear, failure, contamination, loss of readiness, or faulty construction. Maintenance under B06 means project routing for preventing degradation, preserving readiness, servicing, inspecting, refitting, cleaning, calibrating, restocking, or sustaining object/facility function. Repair is not automatic restoration. Maintenance is not invisible bookkeeping.

Repair and maintenance procedure:
1. Confirm whether the project is `repair`, `maintenance`, `facility_work`, `recovery_handoff`, `mixed_project`, `source_local_project`, or `unknown_project`.
2. Identify the object, facility, component, or custody target placed under work.
3. Route current object condition, readiness, damage, function, instability, and object-state outcomes to B03/object owners.
4. Route possession, access, custody, storage, transport, quick-access removal, burden, and lawful recovery to B04.
5. Route parts, consumables, upkeep, value sinks, requisition, scarcity, and market access to B05.
6. Route injury, contamination, safety, hazard, or condition pressure to D07-style harm owners.
7. Route license, warrant, restricted repair, faction property, and legal liability to D10-style world/faction/law owners.
8. Identify whether repair/maintenance output is `object_repaired`, `object_maintained`, `object_field_patched`, `partial_output`, `flawed_output`, `dangerous_output`, `blocked`, `complicated`, or `owner_file_escalation`.

B06 must not define final repair math, final maintenance formula, final object condition schema, final tool rules, or final item stats.

## 15. Modification and upgrade project procedure

Modification under B06 means project routing for changing an object, facility, component, preparation, or system from its prior form or use. Upgrade under B06 means project routing for an intended improvement, expansion, enhancement, replacement, refit, installation, or capability change. Modification is not always improvement. Upgrade is not universal item leveling.

Modification and upgrade procedure:
1. Confirm the intended change and classify the family as `modification`, `upgrade`, `installation_preparation`, `facility_work`, `mixed_project`, `source_local_project`, or `unknown_project`.
2. Identify whether the target is an object, facility, component, vehicle, toolchain, consumable, preparation, source-local artifact, or unknown construct.
3. Identify requirements: schematic, recipe, blueprint, compatibility, component, material, license, permission, facility, toolchain, contributor, safe storage, value commitment, protected-hidden condition, and schema coverage.
4. Route object identity, hardpoint-like pressure, function, balance, stats, compatibility, damage, and object-state questions to B03/object owners without defining final item-level law.
5. Route custody/access/burden to B04 and value/scarcity/requisition/value sink to B05.
6. Route power-pacing, advancement, progression, or reward-as-power pressure to advancement/power owners; B06 does not define final advancement or item tier law.
7. Route legal, faction, restricted-tech, prohibited-work, or social scrutiny to D10-style world/faction/law owners.
8. Mark output as `object_modified`, `object_upgraded`, `object_field_patched`, `partial_output`, `flawed_output`, `dangerous_output`, `owner_routed`, `owner_file_escalation`, or `quarantined_unresolved_delta`.

A successful modification may trade off reliability, legality, maintenance load, custody burden, scarcity exposure, instability, or social risk. An upgrade may be blocked, partial, flawed, dangerous, or owner-routed rather than a clean improvement.

## 16. Facilities, tools, schematics, recipes, contributors, materials, and support-burden procedure

Facility/toolchain/support procedure exists to keep support inputs visible without creating final facility rules, tool proficiency rules, recipe systems, schematic rules, material economy, assistant rules, or crew labor systems.

Support input rules:
- A facility is not automatic success. It may be a requirement, cost, risk container, access constraint, owner handoff, legal exposure, support burden, or source-local retained element.
- A toolchain is not a skill bonus. It may be required, missing, damaged, claimed, incompatible, source-local, or owner-routed.
- A schematic is not final permission. It may identify a possibility, requirement, hidden gap, source-local claim, legal problem, or owner-file question.
- A recipe is not final mechanics. It may guide routing but cannot define final costs, DCs, yields, timing, or outputs.
- A contributor is not free labor. Contributors may require commitment, compensation, safety routing, custody/access permission, faction approval, training/research handoff, support burden, or obligation tracking.
- Materials are not automatically fungible. Material identity, contamination, scarcity, ownership, burden, source, and lawful claim may matter.

Support-burden procedure:
1. List each support input and classify its requirement state.
2. Route facility condition, tool damage, and object/facility work to B03/object owners.
3. Route storage, transport, custody, access, burden, and lawful holding to B04.
4. Route value commitment, acquisition, requisition, upkeep, scarcity, and consumption to B05.
5. Route contributor risk, injury, fatigue, condition setback, or recovery to D07-style harm/recovery owners where applicable.
6. Route contributor knowledge, instruction, practice, research, or theorycraft to D05-style owners.
7. Route permission, license, faction support, restricted facility, and social/legal scrutiny to D10-style world/faction/law owners.
8. If support burden cannot be safely routed, mark `owner_file_gap`, `quarantined_unresolved_delta`, `owner_file_escalation`, or `pending_schema`.

## 17. Progress, partial completion, complication, failure, interruption, and abandonment routing

Progress routing evaluates interval outcomes without defining final project clocks or universal progress points. Progress is not always numeric. Partial completion is not failure by default. Failure does not automatically erase all progress.

Interval outcomes may be: `advanced`, `advanced_with_cost`, `partial`, `stalled`, `blocked`, `complicated`, `damaged`, `interrupted`, `completed`, `completed_with_complication`, `failed`, `abandoned`, `quarantined`, or `escalated`.

Routing procedure:
1. Identify the interval trigger and whether committed costs were consumed, reserved, returned, transformed, or owner-routed.
2. Determine whether progress produced an output, requirement update, complication, no-delta result, or handoff.
3. For `partial`, identify which output or requirement changed and which owner must preserve the partial state. Do not treat partial completion as automatic failure.
4. For `stalled` or `blocked`, identify the blocking requirement, owner-file gap, protected-hidden requirement, source-local issue, or schema gap.
5. For `complicated` or `damaged`, classify complication family and route damage, cost, law, harm, custody, value, facility, contributor, object, or source-local pressure to owners.
6. For `interrupted`, route the interruption to B01/B02 if an active scene or action window opens, preserve committed-cost handling, and decide whether the project is paused, resumed, exposed, damaged, or abandoned.
7. For `completed` or `completed_with_complication`, route final output ownership, custody, value, object state, canon/schema review, and follow-up obligations.
8. For `failed`, identify surviving progress, consumed costs, recoverable material, harm, object damage, value loss, legal exposure, or knowledge gained. Do not erase all progress unless an owner supports that outcome.
9. For `abandoned`, archive the project-facing note, route recoverable commitments, unresolved custody/value/object pressure, and follow-up obligations.
10. For `quarantined` or `escalated`, stop conversion and route to source-local, schema, owner-file, or human review.

Complication classification uses the section 6 families and may produce multiple owner handoffs.

Pause/resume procedure:
- Pause when work cannot safely continue but should not be abandoned.
- Preserve commitments and unresolved requirements as doctrine-facing routing notes only.
- Resume only after requirement states, commitments, facility access, contributor availability, object custody, and interruption consequences are reviewed.
- If resumed under changed conditions, update scope, family, cost/risk preview, and output owners.

Abandonment procedure:
- Identify whether abandonment is actor-declared, forced by interruption, forced by missing requirement, caused by failure, caused by source-local quarantine, or caused by schema/owner gap.
- Route recoverable materials, object state, custody, ownership, value, obligation, contributor, facility, harm, law, and source-local effects to owners.
- Mark `project_archived`, `partial_output`, `quarantined_unresolved_delta`, or `owner_file_escalation` as appropriate.

## 18. Concurrent project and project-load routing

Concurrent projects are allowed only as doctrine-facing routing pressure, not as final downtime slots, final action economy, final progress clocks, or runtime state. B06 identifies when multiple projects compete for time, materials, tools, facilities, contributors, custody, value, attention, licenses, storage, safety, or owner-file review.

Concurrent project procedure:
1. List active project-facing commitments and unresolved outputs.
2. Identify shared resources: time, material, value, facility, toolchain, contributor, crew, storage, transport, object custody, legal permission, and source-local constraints.
3. Identify conflicts, support burdens, scarcity pressure, social scrutiny, contributor risk, maintenance/upkeep load, and interruption exposure.
4. Route resource conflicts to B04/B05 as custody, burden, access, value, scarcity, upkeep, or requisition pressure.
5. Route object conflicts to B03/object owners and legal/faction conflicts to D10-style world/faction/law owners.
6. If concurrency would require final project-load math or runtime project state, mark `pending_schema`, `human_review`, or `defer_until_schema_exists`.

A contributor or facility assigned to one project is not automatically available for another. A project-load note is not a runtime scheduler.

## 19. Project output, ownership, custody, value-flow, and object-state handoff rules

Project outputs must be routed by owner, not treated as automatic inventory, wealth, object stats, canon, or runtime state.

Output routing rules:
- `object_created`, `object_repaired`, `object_maintained`, `object_modified`, `object_upgraded`, `object_field_patched`, `flawed_output`, `dangerous_output`, and object instability route to B03/object owners.
- `custody_routed`, possession, access, storage, transport, burden, quick-access removal, recovery, lawful loss, and ownership/custody separation route to B04.
- `value_committed`, `value_spent`, material acquisition, salvage claim, scarcity, market access, requisition, upkeep, value sink, and obligation pressure route to B05.
- `schematic_created`, `schematic_interpreted`, `recipe_discovered`, research dependency, experimentation, teacher, practice, and competency pressure route to D05-style training/research owners.
- injury, condition setback, contamination, corruption, instability, recovery, and harm pressure route to D07-style harm/recovery owners.
- license, permit, claim, faction attention, social scrutiny, legality, restricted facility, institutional authority, and world-state consequences route to D10-style world/faction/law owners.
- project lifecycle, interval outcome, partial completion, abandonment, pause/resume, contributors, facilities, and source-local project mapping route to D13-style project owners until later Batch C/runtime owners exist.
- conversion records, missing schema, source evidence, rejected donor elements, canon eligibility, provenance, and review routing route to C00/C-family owners.
- runtime, canon, and sourcebook-facing use requires later validation; B06 output notes are not themselves runtime state, canon, or player-facing text.

If no output delta is required, mark `no_delta_required` and explain why the project event remains non-mutating. If output ownership is uncertain, mark `owner_routed`, `quarantined_unresolved_delta`, `owner_file_escalation`, `pending_schema`, or `human_review`.

## 20. Owner-file handoff rules

B06 handoff rules are:
- B01 owns scene/activity/encounter containers, transitions, active-scene triggers, interruption scenes, and checkpoint routing that generated or interrupts project pressure.
- B02 owns action declaration, feasibility, cost commitment, resolution trigger, no-roll/roll-trigger, and action-to-delta procedure that generated or consumes project pressure.
- B03 owns item/gear/equipment/object-system construct, object readiness, object use, object damage, object identity, object function, object state, object work, and asset-use routing.
- B04 owns inventory, storage, custody, possession, access, quick-access, burden, concealment, lawful loss, recovery, and inventory/custody routing.
- B05 owns acquisition, reward, loot, salvage claim, requisition, exchange, market access, availability, scarcity, value conversion routing, upkeep, consumption, economic pressure, and value-sink routing.
- B06 owns project/long-task intake, project family/scope/requirement/commitment/interval/output routing, crafting/salvage/repair/maintenance/modification/upgrade project routing, complication routing, pause/resume, abandonment, and project-output handoffs.
- C00 owns the shared schema handoff control surface and missing-schema fallback language.
- Future C01-C14 schema families may receive conversion handoffs but B06 must not invent their fields. B06 does not require, define, create, or promote C01-C14 and does not make C01-C14 current doctrine.
- D05-style competency/research owners receive training, practice, teacher, experimentation, theorycraft, and research-truth pressure.
- D07-style harm/recovery owners receive injury, condition, contamination, corruption, instability, and recovery pressure.
- D10-style world/faction/law owners receive license, permit, property claim, legal status, social scrutiny, faction attention, restricted facility, institutional authority, and world-state pressure.
- D13-style project owners receive deeper project lifecycle, downtime, concurrent project, source-local project mapping, and not-final record-shape pressure until later owners supersede them.
- Advancement/power/canon owners receive progression pacing, reward-as-power, item-tier pressure, accepted lexicon, canon eligibility, and sourcebook promotion pressure.
- Runtime/training owners receive later validation tasks only; B06 is not runtime authority and not live-play behavior.

If the correct owner is unknown, B06 must mark `pending_schema`, `source_local_review`, `schema_review`, `human_review`, `quarantined_unresolved_delta`, or `owner_file_escalation` rather than inventing ownership.

## 21. Batch B to C00/C-family handoff rules

Batch B procedure may identify that a C-family handoff is needed, but it must not invent C-family fields. B06 uses C00 as the schema handoff control surface when project/crafting/salvage/repair/maintenance/modification/upgrade handling produces conversion records, record-shape pressure, source-local evidence, rejected donor elements, canon eligibility questions, provenance needs, or missing-schema gaps.

The following lightweight doctrine-facing block may be used for B06-to-C00/C-family handoff notes. It is not a runtime schema, not a backend contract, not C-family schema content, not a context packet format, not a database row, not player-facing rule text, not sourcebook prose, and not final mechanics. `project_work_routing_note` is doctrine-facing only: it is not a runtime schema, not runtime project state, not a backend event, not a command object, not a C-family record, not a project database row, not an inventory ledger entry, not an object statblock, not an item recipe, not a crafting table, not final mechanics, not canon, and not player-facing rule text.

```yaml
batch_b_to_c_handoff:
  target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema
  schema_status: not_started | stub_index_only | minimum_unlock_draft | tested_minimum | stable_for_family | stable_cross_family | superseded | deprecated
  required_c00_base_fields: true
  source_evidence_refs_required: true
  construct_refs_required: true
  outcome_refs_required: true
  provenance_refs_required: true
  source_local_boundary_required_if_applicable: true
  rejected_donor_elements_required_if_applicable: true
  canon_eligibility_required: true
  review_routing_required: true
  unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists

project_work_routing_note:
  project_family: crafting | salvage | repair | maintenance | modification | upgrade | installation_preparation | resource_gathering | preparation | facility_work | contributor_supported_work | recovery_handoff | training_handoff | research_handoff | faction_support_handoff | social_handoff | source_local_project | mixed_project | unknown_project
  project_scope: minor | standard | major | extended | transformational | source_local_scope | unknown_scope
  requirement_state: met | missing | unknown | protected_hidden | blocked_by_owner_file | source_local | quarantined | deferred_until_schema_exists
  commitment_type: time_block | materials_reserved | value_committed | facility_claimed | toolchain_committed | schematic_committed | contributor_assigned | crew_assigned | license_or_permission_committed | object_placed_under_work | exposure_accepted | opportunity_cost_accepted | obligation_accepted | source_local_commitment | unknown_commitment
  interval_outcome_state: advanced | advanced_with_cost | partial | stalled | blocked | complicated | damaged | interrupted | completed | completed_with_complication | failed | abandoned | quarantined | escalated
  complication_family: cost_increase | delay | material_loss | tool_or_facility_damage | contributor_risk | injury_or_condition_setback | corruption_or_instability_pressure | object_instability | contamination | schematic_error | recipe_mismatch | incompatible_component | legal_exposure | social_scrutiny | faction_attention | scarcity_pressure | value_sink_triggered | information_false_lead | hidden_pressure_surface | active_scene_trigger | source_local_threat | owner_file_gap | none
  project_output_state: no_delta_required | requirement_identified | requirement_satisfied | object_created | object_repaired | object_maintained | object_modified | object_upgraded | object_field_patched | salvage_recovered | salvage_contaminated | material_gathered | schematic_created | schematic_interpreted | recipe_discovered | facility_prepared | contributor_committed | value_committed | value_spent | obligation_created | ownership_disputed | custody_routed | partial_output | flawed_output | dangerous_output | project_archived | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  owner_handoff_required: boolean
  owner_handoff_reason:
    - scene_or_activity_transition
    - action_cost_or_resolution
    - object_state
    - inventory_custody_burden
    - economy_value_requisition
    - competency_training
    - research_theorycraft
    - harm_recovery_condition
    - world_law_faction
    - project_lifecycle
    - source_local_review
    - schema_review
    - canon_review
    - runtime_review
    - human_review
  delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  note: string
```

Supporting rules:
- `target_schema_family: pending_schema` is allowed only when no C-family owner is stable enough; it is not a license to invent family-specific fields.
- `schema_status` reports the receiving family posture; B06 must not promote registry status.
- `source_evidence_refs_required`, `construct_refs_required`, `outcome_refs_required`, and `provenance_refs_required` preserve traceability.
- `source_local_boundary_required_if_applicable` and `rejected_donor_elements_required_if_applicable` prevent donor project/crafting/downtime import by accident.
- `review_routing_required` means unresolved project, crafting, salvage, repair, maintenance, modification, upgrade, schema, source-local, canon, and runtime questions must route to owners.

## 22. Missing-schema fallback and quarantine/escalation

When B06 lacks schema coverage, owner coverage, or safe doctrine vocabulary, it must use one of the following instead of improvising schema:
- `pending_schema`
- quarantine
- escalation
- `human_review`
- `defer_until_schema_exists`
- `source_local_review`
- `schema_review`
- `quarantined_unresolved_delta`
- `owner_file_escalation`

Missing schema coverage must not produce invented C-family fields, runtime project state, runtime inventory state, runtime object state, runtime economy ledger entries, backend contracts, command objects, hidden-information state, final schemas, final math, sourcebook rules, or canon.

Quarantine is required when:
- a donor downtime/crafting/salvage/repair/upgrade/project system is present but cannot be safely mapped;
- hidden requirements would be exposed by conversion;
- source-local mechanics are doing non-Astra work;
- output routing would require final object, inventory, economy, project, facility, recipe, or crafting schemas;
- owner files conflict or no owner can accept the delta;
- the proposed output would silently promote canon, accepted lexicon, player-facing rules, runtime state, or donor defaults.

Escalation is required when the unresolved gap affects safety, legality, harm, faction/world consequences, major value, transformational object changes, source-local truth, canon eligibility, or cross-family schema governance.

## 23. Source-local donor downtime/crafting/project handling

Source-local donor downtime, crafting, salvage, repair, maintenance, modification, upgrade, requisition, project, or long-task systems are not Astra defaults. B06 may inspect them as source evidence, but must quarantine or map them through owner procedure.

Source-local handling procedure:
1. Identify the donor/source-local project rule, currency, interval, clock, recipe, cost, yield, upgrade path, salvage result, downtime turn, long-rest/short-rest dependency, facility rule, contributor rule, or item stat rule.
2. Mark which elements are retained as source-local evidence and which are rejected donor elements.
3. Convert only safe doctrine-facing pressure: intent, family, scope, requirement state, commitment type, interval outcome, complication family, output state, and owner handoff.
4. Do not import donor timing, DCs, item levels, crafting prices, repair formulas, salvage tables, facility bonuses, tool proficiency bonuses, rest procedures, downtime menus, requisition ratings, or sourcebook prose.
5. If conversion would expose hidden information, alter canon, create runtime state, or invent schema, mark `source_local_review`, quarantine, escalation, `human_review`, or `defer_until_schema_exists`.

A source-local retained effect may remain as `source_local_retained_effect` only when its boundary is explicit and owner review is routed.

## 24. Runtime boundary

B06 is not runtime authority. B06 rejects runtime state/event/command lifecycle ownership. It must not create runtime project state, runtime inventory state, runtime object state, runtime economy ledger entries, runtime entity/component/event/state schemas, persistent campaign state, command lifecycle implementation, context packet compiler output, hidden-information runtime state, or live-play narration behavior.

Runtime systems may later consume owner-validated outputs, but B06 procedure itself remains doctrine-facing. Live-play behavior must not consume B06 procedure as runtime authority without later runtime validation.

## 25. Canon boundary

B06 does not promote canon. It may identify canon eligibility pressure, provenance needs, source evidence, rejected donor elements, owner-file disputes, source-local boundaries, or project outputs that might later be canon-reviewed. It must not decide final canon, accepted lexicon, sourcebook text, final item identities, final facility facts, final faction law, final market law, final historical outcomes, or final world truth.

If a project output appears canon-relevant, B06 routes the output to canon owners and C00/C-family handoff review rather than treating the doctrine note as a canon entry.

## 26. Live-play/training boundary

B06 does not define live-play GM behavior, player-facing rules, training scripts, tutorial text, or sourcebook prose. It may route training, practice, teacher, competency, research, theorycraft, recovery, or downtime-adjacent pressure to appropriate owners, but it must not define final training advancement, research truth procedure, recovery rules, long-rest/short-rest rules, or donor downtime systems.

Examples and records in B06 are doctrine-facing only and must not be copied into live-play narration or player-facing instructions without later owner validation.

## 27. Examples of good and bad B06 usage

Good B06 usage:
- A crew wants to build a field antenna from scavenged parts. B06 classifies `crafting` with `standard` scope, marks materials and toolchain requirements, routes object identity and readiness to B03, storage/burden to B04, material acquisition and value commitment to B05, and uses `object_created` only as an owner-routed output rather than defining antenna stats.
- A mechanic tries to salvage a damaged drone after an encounter. B06 classifies `salvage`, marks ownership and contamination as requirements, routes object instability to B03, custody and transport burden to B04, salvage claim/value pressure to B05, possible harm to D07-style owners, and avoids creating a salvage yield table.
- A vehicle needs maintenance before a dangerous journey. B06 classifies `maintenance`, previews time, parts, facility, upkeep, and interruption risk, routes readiness and damage to B03, parts and upkeep to B05, and treats the interval outcome as `advanced_with_cost` or `partial` without creating maintenance math.
- A player wants to upgrade a weapon using a found schematic. B06 classifies `upgrade`, marks the schematic as not final permission, routes compatibility and item stats to B03, material/value requirements to B05, legality to D10-style owners, and schema gaps to C00 without defining final upgrade rules.
- A sourcebook offers a downtime crafting table. B06 marks it as `source_local_project`, records source-local evidence and rejected donor elements, converts only safe project pressure, and quarantines donor timing, DCs, recipes, costs, and output stats.

Bad B06 usage:
- Defining final crafting DCs, final costs per day, final repair math, final salvage yield tables, final upgrade math, final modification rules, final item stats, final item rarity/tier law, final material economy, final recipe system, final schematic/blueprint rules, final facility rules, or final tool proficiency rules.
- Treating a project as automatically downtime, downtime as safe time, salvage as free wealth, repair as automatic restoration, maintenance as invisible bookkeeping, a facility as automatic success, a toolchain as a skill bonus, a contributor as free labor, a recipe as final mechanics, or an upgrade as universal item leveling.
- Creating runtime project state, runtime inventory state, runtime object state, runtime economy ledger entries, command objects, event schemas, backend contracts, context packet formats, hidden-information state, persistent campaign state, live-play narration behavior, player-facing rules, sourcebook prose, final canon, or accepted lexicon.
- Importing donor downtime turns, rest procedures, crafting tables, salvage rules, upgrade paths, facility bonuses, requisition ratings, market prices, sourcebook recipes, or item-level systems as Astra defaults.
- Inventing C-family fields, final project schemas, final object schemas, final inventory schemas, final economy schemas, final crafting schemas, or final C01-C14 schema contents.

## 28. Minimum tests or assertions

Minimum B06 tests or assertions should verify that:
- B06 exists at `docs/doctrine/operations/batch_b/B06_project_crafting_salvage_repair_and_upgrade_procedure.md`;
- all required B06 sections are present;
- B06 declares ownership and non-ownership;
- B06 references B01, B02, B03, B04, and B05 as upstream Batch B context;
- B06 includes C00 handoff language and `batch_b_to_c_handoff`;
- B06 includes `project_work_routing_note` and marks it as doctrine-facing only;
- B06 includes project families, scope bands, requirement states, commitment types, interval outcome states, complication families, and project output states;
- B06 includes project/long-task intake procedure;
- B06 includes intent, goal, family, and scope classification;
- B06 includes requirement discovery and protected-hidden requirement handling;
- B06 includes cost/risk preview, commitment, interval setup, and progress-trigger procedure;
- B06 includes crafting, salvage processing, repair/maintenance, and modification/upgrade project procedures;
- B06 includes facilities, tools, schematics, recipes, contributors, materials, and support-burden procedure;
- B06 includes progress, partial completion, complication, failure, interruption, pause/resume, abandonment, archival, and follow-up routing;
- B06 includes concurrent project and project-load routing;
- B06 routes project outputs to B03 object owners, B04 inventory/custody owners, B05 value-flow owners, D05 competency/research owners, D07 harm owners, D10 world/faction/law owners, D13-style project owners, and later runtime/canon/schema owners;
- B06 includes Batch B to C00/C-family handoff rules;
- B06 includes missing-schema fallback, quarantine, escalation, `pending_schema`, `human_review`, and `defer_until_schema_exists`;
- B06 includes source-local donor downtime/crafting/salvage/repair/upgrade/project quarantine and escalation rules;
- B06 rejects final project schema, final crafting schema, final object schema, final inventory schema, final economy schema, C-family field invention, C01-C14 schema-content ownership, final crafting math, final repair math, final salvage yield tables, final upgrade math, final modification rules, final item stats, final item rarity/tier law, final material economy, final recipe system, final schematic/blueprint rules, final facility rules, final tool proficiency rules, final downtime activity menu, final project-clock system, final universal progress-point system, final recovery rules, final training advancement, final research truth procedure, final crafting DCs, final crafting costs per day, final donor downtime turns, final donor long-rest/short-rest procedures, final sourcebook crafting/repair/salvage/upgrade/downtime rules, final requisition authority, final market/economy law, final advancement/progression reward pacing, runtime project state, runtime inventory state, runtime object state, runtime economy ledger, runtime schemas, persistent campaign state, command lifecycle implementation, context packet compiler, hidden-information runtime state, live-play behavior, canon promotion, accepted lexicon, sourcebook prose, and donor crafting/downtime/project systems as Astra defaults;
- every meaningful project/crafting/salvage/repair/upgrade event routes at least one delta to a recognized owner or explicitly produces a no-delta, quarantine, escalation, transition, source-local, `pending_schema`, `human_review`, or `defer_until_schema_exists` result.

## 29. Acceptance criteria

B06 is acceptable if it:
- sits after B01, B02, B03, B04, and B05 and builds on them without rewriting them;
- defines project-centered interval routing for crafting, salvage processing, repair, maintenance, modification, upgrade, object work, facility-supported work, material requirements, contributors, partial completion, complications, interruption, pause/resume, abandonment, and output routing;
- preserves the distinction between scene/action/object-use/inventory/economy/project procedure;
- treats crafting, salvage, repair, maintenance, modification, and upgrade as project-routing domains rather than final mechanics;
- preserves hidden requirement handling without exposing hidden truth;
- routes commitments and outputs to recognized owners;
- includes the required C00/C-family handoff block without creating runtime schema;
- uses missing-schema fallback and source-local quarantine instead of improvising schema or importing donor systems;
- states runtime, canon, live-play, training, sourcebook, and final-mechanics boundaries clearly;
- includes good and bad usage examples, minimum assertions, and this acceptance checklist.

## 30. Follow-up handoff to B07

B06 hands off to B07 only at the boundary of later Batch B operational doctrine. B06 does not require, define, create, or promote B07-B11, does not pre-author their scope, and does not make B07-B11 current doctrine. B06 does not create B07-B11. Any future B07 work should receive unresolved operational pressure only as owner-routed notes, such as:
- project outputs requiring a later operational owner;
- interruption or active-scene transitions that exceed B06;
- schema gaps marked through C00;
- source-local donor project systems quarantined for later review;
- runtime/canon/training questions that require later validation;
- owner-file escalations that B06 identified but could not resolve.

Until B07 exists, B06 must end unresolved follow-up as `owner_routed`, `owner_file_escalation`, `pending_schema`, `human_review`, `defer_until_schema_exists`, `source_local_retained_effect`, or `quarantined_unresolved_delta` rather than inventing new Batch B authority.
