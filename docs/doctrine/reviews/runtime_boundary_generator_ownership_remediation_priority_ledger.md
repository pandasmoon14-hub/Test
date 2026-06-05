# Runtime Boundary + Generator Ownership Remediation Priority Ledger

Date prepared: 2026-06-05
Status: remediation-priority planning ledger only
Tracking ID: AUDIT-REMEDIATION-LEDGER-001
Inputs: AUDIT-001, AUDIT-WAVE1-001, AUDIT-WAVE2-001
Owner: Astra Doctrine Council / Runtime Boundary Reviewers

## 1. Purpose and scope

This ledger pauses audit expansion after AUDIT-WAVE1-001 and AUDIT-WAVE2-001 and consolidates accepted Runtime Boundary + Generator Ownership Audit findings into ordered remediation tracks. Its purpose is to rank repeated critical/high-risk seams, group them under future owner workstreams, describe dependency ordering, and recommend the next safe PR sequence.

This is a remediation-priority planning ledger only. It does not implement remediation, rewrite doctrine, create runtime code, create schemas, create command IR, create generators, create validators, create persistence writers, create context-packet compilers, authorize live play, create training data, audit donor content, or promote canon.

This ledger intentionally does not perform Wave 3. It treats Waves 1-2 as accepted inputs and converts their findings into planning order only.

## 2. Inputs

Controlling and accepted inputs:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.

Additional governance and tracking inputs used for boundary checks:

- `docs/doctrine/astra_doctrine_registry_v0_1.yaml`.
- `docs/doctrine/astra_doctrine_roadmap_v0_1.md`.
- `docs/decisions/current_decisions_log.md`.
- `docs/operations/current_decisions_log_v0_1.md`.

Source files were inspected only as needed to avoid misclassifying accepted audit findings. D-series/native-design material is treated as draft source material only, not current runtime authority.

## 3. Consolidated risk themes from Waves 1-2

Waves 1-2 repeatedly found that Astra cannot rely on an LLM to improvise missing backend ownership at these seams:

1. **Command lifecycle / action legality / cost commitment.** B02, A10, D02, B03, C03, and C10 all require backend-owned intent parsing, legality checks, committed costs, rollback/interrupt rules, resolution triggers, and event commits before narration can describe outcomes.
2. **Resource, backlash, corruption, strain, and consequence math.** A10, A13, C03, C09, C07, and D02 expose critical risk when resource spend, overinvestment, backlash, corruption, strain, reward, or consequence deltas are left to prose.
3. **Combat, damage, injury, hazard exposure, and recovery.** A13, B10, C09, C07, and C08 require damage severity, injury/condition clocks, mitigation, recovery, exposure intervals, active-threat queues, and persistent event models.
4. **Ability/effect/cost/cooldown/action binding.** A08, A09, A10, B02, B03, and C03 require backend-owned ability records, prerequisites, effect taxonomy, cost/cooldown state, skill synthesis validation, and command binding.
5. **Mission, reward, clue, hidden-truth, and consequence routing.** C07, C09, A13, B09, and C10 combine hidden information, clues, branches, rewards, failure, and consequence routing that must be committed by backend events rather than generated narration.
6. **Social, faction, relationship, actor knowledge, and institutional state.** B09, C05, and C01 require relationship/standing state, contact memory, belief/knowledge partitions, faction/institution consequence routing, and hidden agenda redaction.
7. **Generated-content recurrence/provenance.** C01, C02, C05, C06, C07, C08, C09, C10, B03, and B09 require durable IDs, provenance, source-local boundaries, validation, recurrence, and canon-promotion separation for NPCs, items, factions, locations, missions, hazards, vehicles, and tables.
8. **Runtime RNG/table/oracle ownership.** C10 and the backend-first control invariant require backend-owned RNG, seeded/replayable invocation events, table weight validation, and no LLM-selected oracle outcomes.
9. **Scene/activity orchestration and hidden-information/context-packet boundaries.** B01, B09, C06, C07, C09, and C10 require scene state, participant rosters, visibility partitions, redaction, context-packet compilation, and event ordering before live-play use.
10. **Validation/readiness tooling versus prose-only governance.** AUDIT-001, SM00, SM01, and SM02 can structure reviews, but they are not executable validators, runtime state models, database schemas, or authorization gates until future tooling exists.
11. **D-series/native-design material promotion boundaries.** D02 and other D-series source-pack material may exert design pressure only. They must not become runtime authority, generator inputs, live-play content, or canon without explicit promotion.

## 4. Remediation dependency order

Recommended dependency order before any implementation PR claims runtime readiness:

1. Establish control/readiness and owner-file scaffolds that preserve non-implementation boundaries.
2. Define command lifecycle and state/event owner decomposition before subsystem-specific commands.
3. Define resource/cost/backlash/consequence math owners before ability, combat, hazard, mission, item, or vehicle effects consume those costs.
4. Define context-packet and hidden-information owner decomposition before scene, social, location, clue, and mission runtime claims.
5. Define generated-content provenance/recurrence owner decomposition before enabling NPC, item, faction, location, mission, hazard, vehicle, or table generators.
6. Define RNG/table/oracle ownership before any table result, oracle output, random encounter, clue, hazard, or reward can be committed.
7. Define D-series promotion gates before using source-pack material as design input to current doctrine or runtime work.
8. Only after the above owner scaffolds exist should later PRs draft schemas, command IR, validators, generators, persistence writers, context-packet compilers, or runtime code.

## 5. Ranked remediation tracks

### Track RT-001 — Command lifecycle and action legality spine

```yaml
track_id: RT-001-command-lifecycle-action-legality
priority: P0
title: Command lifecycle, legality, and cost commitment spine
risk_level: critical
source_audit_records:
  - AUDIT-WAVE1-001 README.backend_first_model_interchangeability
  - AUDIT-WAVE2-001 B02.action_declaration_cost_commitment_lifecycle_boundary
  - AUDIT-WAVE2-001 A10.resource_cost_backlash_corruption_boundary
  - AUDIT-WAVE2-001 D02.cost_commitment_success_at_cost_source_material_boundary
affected_source_files:
  - README.md
  - docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md
  - docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md
  - docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-03_cost_commitment_overinvestment_and_success_at_cost.md
problem_summary: Waves 1-2 identify command declaration, legality, committed costs, resolution triggers, rollback/cancel/interrupt, and state-delta commits as the central runtime seam. Without this spine, nearly every action path delegates legality, cost spending, consequence routing, and persistence to the narrator.
why_backend_owned: The LLM cannot be the authority for legality, resource spend, dice/RNG triggers, rollback, interrupts, or state deltas because those decisions must be validated, replayable, auditable, and persisted.
required_owner_files_or_workstreams:
  - future command lifecycle control owner
  - future runtime state/event owner
  - future cost/resource math owner
  - future command-context handoff owner
required_outputs:
  - command_ir
  - runtime_state
  - event_model
  - validator
  - context_packet
  - tests
dependencies:
  - repo gate: AUDIT-001 non-implementation boundary remains active
  - RT-011-validation-readiness-tooling
blocked_by:
  - missing command IR owner
  - missing runtime event owner
  - missing cost/resource math owner
recommended_first_pr: Create a command-lifecycle owner-file scaffold that names lifecycle states, owner boundaries, prohibited LLM authorities, dependency links, and test expectations without defining final IR fields or runtime code.
must_not_do_in_first_pr:
  - implement command IR
  - define final schemas
  - create runtime code
  - choose cost math
  - authorize live play
acceptance_tests_needed:
  - command lifecycle owner-file presence test
  - no-runtime-implementation assertion test
  - no-LLM-legality/cost authority phrasing test
notes: This is the first remediation track because every other runtime-facing subsystem consumes command lifecycle semantics.
```

### Track RT-002 — Resource, backlash, corruption, strain, and consequence math

```yaml
track_id: RT-002-resource-backlash-consequence-math
priority: P0
title: Resource, backlash, corruption, strain, and consequence math ownership
risk_level: critical
source_audit_records:
  - AUDIT-WAVE1-001 A13.combat_hazard_damage_consequence_boundary
  - AUDIT-WAVE1-001 C03.ability_power_technique_generator_inputs
  - AUDIT-WAVE1-001 C09.hazard_environment_record_boundary
  - AUDIT-WAVE1-001 SM00.runtime_gate_dependency_and_math_gap_inventory
  - AUDIT-WAVE2-001 A10.resource_cost_backlash_corruption_boundary
  - AUDIT-WAVE2-001 B02.action_declaration_cost_commitment_lifecycle_boundary
  - AUDIT-WAVE2-001 C07.mission_scenario_adventure_record_schema_boundary
  - AUDIT-WAVE2-001 D02.cost_commitment_success_at_cost_source_material_boundary
affected_source_files:
  - docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md
  - docs/doctrine/schema/C03_ability_power_technique_record_schema.md
  - docs/doctrine/schema/C09_hazard_environment_record_schema.md
  - docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md
  - docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md
  - docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md
  - docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md
  - docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-03_cost_commitment_overinvestment_and_success_at_cost.md
problem_summary: Resource pools, overcommitment, backlash, corruption, strain, harm, reward, and consequence outputs recur across combat, abilities, hazards, missions, and command lifecycle findings. Existing doctrine names pressure but does not finalize math or event ownership.
why_backend_owned: Resource loss, corruption, strain, harm, rewards, and consequence events alter persistent player/campaign state and therefore require deterministic backend math, validation, and audit trails.
required_owner_files_or_workstreams:
  - future resource/cost mechanics owner
  - future consequence event model owner
  - future SM math/mechanics workstream owners
  - future runtime persistence owner
required_outputs:
  - math
  - runtime_state
  - event_model
  - validator
  - tests
dependencies:
  - RT-001-command-lifecycle-action-legality
  - RT-011-validation-readiness-tooling
blocked_by:
  - missing final resource/cost math
  - missing consequence event model
  - missing runtime state persistence owner
recommended_first_pr: Create a resource-and-consequence math owner-file scaffold that inventories cost/backlash/corruption/strain/consequence families and records dependency boundaries without choosing numeric formulas.
must_not_do_in_first_pr:
  - set final resource values
  - set final damage or backlash formulas
  - implement state deltas
  - create schemas or validators
acceptance_tests_needed:
  - math-owner boundary presence test
  - no-final-formula assertion test
  - dependency reference test for B02/C03/A13/C09/C07
notes: This track is P0 because cost and consequence math must exist before abilities, hazards, combat, missions, and assets can be runtime-safe.
```

### Track RT-003 — Combat, hazard exposure, damage, injury, and recovery

```yaml
track_id: RT-003-combat-hazard-damage-recovery
priority: P0
title: Combat, hazard exposure, damage, injury, and recovery ownership
risk_level: critical
source_audit_records:
  - AUDIT-WAVE1-001 A13.combat_hazard_damage_consequence_boundary
  - AUDIT-WAVE1-001 B10.hazard_opposition_contact_trigger
  - AUDIT-WAVE1-001 C09.hazard_environment_record_boundary
  - AUDIT-WAVE2-001 C08.vehicle_ship_platform_record_schema_boundary
  - AUDIT-WAVE2-001 C07.mission_scenario_adventure_record_schema_boundary
affected_source_files:
  - docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md
  - docs/doctrine/operations/batch_b/B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md
  - docs/doctrine/schema/C09_hazard_environment_record_schema.md
  - docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md
  - docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md
problem_summary: Combat and hazard findings require ownership for active threat detection, exposure intervals, damage severity, mitigation, injury/condition clocks, recovery, vehicle/platform integrity, and mission-linked consequences.
why_backend_owned: The LLM cannot decide harm, death, injury, exposure, recovery, or threat escalation because those outcomes affect player agency, risk, persistence, replayability, and hidden-state fairness.
required_owner_files_or_workstreams:
  - future combat/consequence mechanics owner
  - future hazard runtime owner
  - future recovery/condition owner
  - future threat trigger/event owner
required_outputs:
  - math
  - command_ir
  - runtime_state
  - event_model
  - context_packet
  - tests
dependencies:
  - RT-001-command-lifecycle-action-legality
  - RT-002-resource-backlash-consequence-math
  - RT-009-runtime-rng-table-oracle
blocked_by:
  - missing damage/injury math
  - missing hazard exposure state model
  - missing active threat queue/event owner
recommended_first_pr: Draft a combat-hazard owner-boundary scaffold that separates threat detection, exposure, harm, recovery, and narration contracts while deferring final formulas.
must_not_do_in_first_pr:
  - implement combat runtime
  - create damage tables
  - create hazard generators
  - authorize live encounter play
acceptance_tests_needed:
  - no-LLM-damage-commit test family
  - hazard exposure owner-boundary test
  - hidden hazard redaction expectation test
notes: This track should follow RT-001/RT-002 scaffolding but remain P0 because combat/hazard improvisation is critical-risk.
```

### Track RT-004 — Ability, effect, cost, cooldown, skill, and advancement binding

```yaml
track_id: RT-004-ability-effect-skill-binding
priority: P0
title: Ability/effect/cost/cooldown and skill synthesis binding
risk_level: critical
source_audit_records:
  - AUDIT-WAVE1-001 A08.path_domain_technique_mastery_boundary
  - AUDIT-WAVE1-001 C03.ability_power_technique_generator_inputs
  - AUDIT-WAVE2-001 A09.skill_competency_synthesis_boundary
  - AUDIT-WAVE2-001 A10.resource_cost_backlash_corruption_boundary
  - AUDIT-WAVE2-001 B02.action_declaration_cost_commitment_lifecycle_boundary
affected_source_files:
  - docs/doctrine/advancement/A08_path_domain_and_technique_mastery_doctrine.md
  - docs/doctrine/schema/C03_ability_power_technique_record_schema.md
  - docs/doctrine/advancement/A09_skill_competency_and_synthesis_doctrine.md
  - docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md
  - docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md
problem_summary: Ability, power, technique, skill, and synthesis findings all require backend ownership for prerequisites, acquisition, mastery, effect taxonomy, cost/cooldown state, scaling, backlash, action timing, and persistence.
why_backend_owned: The LLM cannot invent abilities, costs, cooldowns, mastery, skill synthesis outputs, or effect resolution because these alter player capability and mechanical balance.
required_owner_files_or_workstreams:
  - future ability/effect mechanics owner
  - future skill/competency schema owner
  - future advancement/progression math owner
  - future command binding owner
required_outputs:
  - schema
  - math
  - command_ir
  - runtime_state
  - generator_template
  - validator
  - tests
dependencies:
  - RT-001-command-lifecycle-action-legality
  - RT-002-resource-backlash-consequence-math
  - RT-008-generated-content-provenance
blocked_by:
  - missing ability effect taxonomy
  - missing skill/competency record schema
  - missing cost/cooldown mechanics
recommended_first_pr: Create an ability/effect/skill owner-boundary scaffold that states prerequisites, effect routing, cost/cooldown dependencies, and generator prohibitions without enabling ability generation.
must_not_do_in_first_pr:
  - generate abilities or techniques
  - award skills or mastery
  - set final progression thresholds
  - implement use-ability commands
acceptance_tests_needed:
  - no-LLM-ability-invention test family
  - ability-cost dependency test
  - synthesis-output non-persistence assertion test
notes: This track is P0 because ability generation and use directly affect persistent player power.
```

### Track RT-005 — Scene/activity orchestration and context-packet boundaries

```yaml
track_id: RT-005-scene-activity-context-packets
priority: P0
title: Scene/activity orchestration and hidden-information context packets
risk_level: high
source_audit_records:
  - AUDIT-WAVE2-001 B01.scene_encounter_activity_orchestration_boundary
  - AUDIT-WAVE2-001 B09.social_faction_contact_interaction_boundary
  - AUDIT-WAVE2-001 C06.location_site_region_record_schema_boundary
  - AUDIT-WAVE2-001 C07.mission_scenario_adventure_record_schema_boundary
  - AUDIT-WAVE1-001 C09.hazard_environment_record_boundary
  - AUDIT-WAVE2-001 C10.table_oracle_record_schema_boundary
affected_source_files:
  - docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md
  - docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md
  - docs/doctrine/schema/C06_location_site_region_record_schema.md
  - docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md
  - docs/doctrine/schema/C09_hazard_environment_record_schema.md
  - docs/doctrine/schema/C10_table_oracle_record_schema.md
problem_summary: Scene, social, location, mission, hazard, and oracle records all require backend-owned active scene state, participant rosters, visibility partitions, hidden facts, redactions, and context-packet projections.
why_backend_owned: Hidden facts, available actions, participant visibility, and context packets cannot be held in model memory because leakage or hallucination breaks fairness, replay, and consistency.
required_owner_files_or_workstreams:
  - future scene/activity runtime owner
  - future context-packet compiler owner
  - future hidden-information partition owner
  - future narration contract owner
required_outputs:
  - runtime_state
  - event_model
  - context_packet
  - narration_contract
  - validator
  - tests
dependencies:
  - RT-001-command-lifecycle-action-legality
  - RT-007-social-faction-knowledge-state
  - RT-006-mission-reward-clue-routing
blocked_by:
  - missing scene lifecycle state model
  - missing context-packet compiler owner
  - missing hidden-information partition schema
recommended_first_pr: Draft a context-packet and hidden-information owner-boundary scaffold that defines visible/hidden/redacted responsibility and prohibits narrator-owned hidden state.
must_not_do_in_first_pr:
  - build context-packet compiler
  - create scene runtime
  - create live-play adapter prompts
  - reveal hidden information rules as final schema
acceptance_tests_needed:
  - hidden-state redaction posture test
  - no-LLM-scene-state mutation test
  - narration downstream-of-backend assertion test
notes: This track enables later live-play safety but should remain planning-only until command and state/event owners exist.
```

### Track RT-006 — Mission, reward, clue, hidden-truth, and consequence routing

```yaml
track_id: RT-006-mission-reward-clue-routing
priority: P1
title: Mission, reward, clue, hidden-truth, and consequence routing
risk_level: critical
source_audit_records:
  - AUDIT-WAVE2-001 C07.mission_scenario_adventure_record_schema_boundary
  - AUDIT-WAVE1-001 A13.combat_hazard_damage_consequence_boundary
  - AUDIT-WAVE1-001 C09.hazard_environment_record_boundary
  - AUDIT-WAVE2-001 B09.social_faction_contact_interaction_boundary
  - AUDIT-WAVE2-001 C10.table_oracle_record_schema_boundary
affected_source_files:
  - docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md
  - docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md
  - docs/doctrine/schema/C09_hazard_environment_record_schema.md
  - docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md
  - docs/doctrine/schema/C10_table_oracle_record_schema.md
problem_summary: Mission/scenario records combine objectives, branches, clues, rewards, hidden truths, hazards, social consequences, oracle results, and canon pressure. Schema readiness is not sufficient for mission runtime use.
why_backend_owned: The LLM cannot invent rewards, complete objectives, reveal clues, mutate branches, or commit consequences because these drive durable campaign progression and hidden-state fairness.
required_owner_files_or_workstreams:
  - future mission/scenario runtime owner
  - future reward/consequence event owner
  - future clue/hidden-truth partition owner
  - future generated scenario provenance owner
required_outputs:
  - schema
  - command_ir
  - runtime_state
  - event_model
  - context_packet
  - generator_template
  - validator
  - tests
dependencies:
  - RT-001-command-lifecycle-action-legality
  - RT-002-resource-backlash-consequence-math
  - RT-005-scene-activity-context-packets
  - RT-008-generated-content-provenance
blocked_by:
  - missing mission state model
  - missing reward/consequence schema
  - missing clue/hidden-truth partition owner
recommended_first_pr: Create a mission-routing owner-boundary scaffold that lists objective, clue, reward, branch, consequence, provenance, and context dependencies without creating mission schemas or generators.
must_not_do_in_first_pr:
  - generate missions
  - commit rewards
  - define final clue schema
  - promote scenario canon
acceptance_tests_needed:
  - no-LLM-reward-commit test family
  - hidden clue redaction posture test
  - mission generator disabled-until-provenance test
notes: This is P1 because it depends on P0 command, cost, consequence, context, and provenance scaffolds.
```

### Track RT-007 — Social, faction, relationship, actor knowledge, and institutional state

```yaml
track_id: RT-007-social-faction-knowledge-state
priority: P1
title: Social, faction, relationship, actor knowledge, and institutional state
risk_level: critical
source_audit_records:
  - AUDIT-WAVE2-001 B09.social_faction_contact_interaction_boundary
  - AUDIT-WAVE1-001 C05.faction_institution_generated_content_boundary
  - AUDIT-WAVE1-001 C01.creature_npc_record_runtime_boundary
affected_source_files:
  - docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md
  - docs/doctrine/schema/C05_faction_institution_record_schema.md
  - docs/doctrine/schema/C01_creature_npc_record_schema.md
problem_summary: Social and faction findings require relationship state, standing deltas, NPC/contact knowledge and belief partitions, institutional actions, faction recurrence, and hidden agenda redaction.
why_backend_owned: Relationship mutations, faction standing, NPC knowledge, secrets, obligations, and institutional consequences must be consistent and durable; narration cannot safely store or mutate them.
required_owner_files_or_workstreams:
  - future social/faction runtime owner
  - future relationship/standing schema owner
  - future actor knowledge and belief partition owner
  - future faction generated-content provenance owner
required_outputs:
  - schema
  - command_ir
  - runtime_state
  - event_model
  - context_packet
  - generator_template
  - validator
  - tests
dependencies:
  - RT-001-command-lifecycle-action-legality
  - RT-005-scene-activity-context-packets
  - RT-008-generated-content-provenance
blocked_by:
  - missing relationship schema owner
  - missing faction runtime owner
  - missing knowledge/dialogue memory owner
recommended_first_pr: Draft a social/faction/knowledge owner-boundary scaffold that separates dialogue narration from relationship, standing, knowledge, belief, and institutional state commits.
must_not_do_in_first_pr:
  - implement social commands
  - create relationship schemas
  - generate faction actions
  - promote faction canon
acceptance_tests_needed:
  - no-LLM-relationship-mutation test family
  - actor knowledge partition posture test
  - faction standing non-authority assertion test
notes: This track is critical-risk but should follow shared context/provenance owner scaffolds to avoid duplicate hidden-state rules.
```

### Track RT-008 — Generated-content recurrence and provenance

```yaml
track_id: RT-008-generated-content-provenance
priority: P1
title: Generated-content recurrence, provenance, and canon-separation ownership
risk_level: high
source_audit_records:
  - AUDIT-WAVE1-001 C01.creature_npc_record_runtime_boundary
  - AUDIT-WAVE1-001 C05.faction_institution_generated_content_boundary
  - AUDIT-WAVE1-001 C09.hazard_environment_record_boundary
  - AUDIT-WAVE2-001 C02.item_gear_record_schema_boundary
  - AUDIT-WAVE2-001 C06.location_site_region_record_schema_boundary
  - AUDIT-WAVE2-001 C07.mission_scenario_adventure_record_schema_boundary
  - AUDIT-WAVE2-001 C08.vehicle_ship_platform_record_schema_boundary
  - AUDIT-WAVE2-001 C10.table_oracle_record_schema_boundary
  - AUDIT-WAVE2-001 B03.item_gear_equipment_asset_use_boundary
affected_source_files:
  - docs/doctrine/schema/C01_creature_npc_record_schema.md
  - docs/doctrine/schema/C05_faction_institution_record_schema.md
  - docs/doctrine/schema/C09_hazard_environment_record_schema.md
  - docs/doctrine/schema/C02_item_gear_record_schema.md
  - docs/doctrine/schema/C06_location_site_region_record_schema.md
  - docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md
  - docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md
  - docs/doctrine/schema/C10_table_oracle_record_schema.md
  - docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md
problem_summary: Waves 1-2 repeatedly find that NPCs, items, factions, locations, missions, hazards, vehicles, and tables may be routeable for future templates, but durable recurrence, provenance, source-local status, validation, and canon-promotion separation are still missing.
why_backend_owned: The LLM cannot make generated facts durable or canonical by repetition; recurrence requires stable IDs, provenance fields, validation, event commits, retrieval indexes, and explicit canon workflow separation.
required_owner_files_or_workstreams:
  - future generated-content lifecycle owner
  - future provenance/source-local schema owner
  - future generator-template owner
  - future canon-promotion separation owner
required_outputs:
  - schema
  - generator_template
  - validator
  - runtime_state
  - event_model
  - tests
  - other
dependencies:
  - RT-011-validation-readiness-tooling
  - repo gate: canon promotion remains separate from persistence
blocked_by:
  - missing generated-content lifecycle owner
  - missing persistence commit path for generated records
  - missing canon-promotion workflow binding
recommended_first_pr: Create a generated-content lifecycle owner-boundary scaffold covering stable IDs, provenance, source-local status, recurrence, default non-canon state, and disabled generator posture.
must_not_do_in_first_pr:
  - create generator code
  - create durable generated records
  - write canon-promotion rules as final workflow
  - create retrieval indexes
acceptance_tests_needed:
  - generated-content no-canon-promotion test family
  - provenance field expectation test
  - no-direct-LLM-durable-record assertion test
notes: This track should precede any generator template PR for NPCs, items, factions, locations, missions, hazards, vehicles, or tables.
```

### Track RT-009 — Runtime RNG, table, and oracle ownership

```yaml
track_id: RT-009-runtime-rng-table-oracle
priority: P1
title: Runtime RNG, table, and oracle ownership
risk_level: high
source_audit_records:
  - AUDIT-WAVE1-001 README.backend_first_model_interchangeability
  - AUDIT-WAVE2-001 C10.table_oracle_record_schema_boundary
  - AUDIT-WAVE1-001 B10.hazard_opposition_contact_trigger
  - AUDIT-WAVE1-001 C09.hazard_environment_record_boundary
affected_source_files:
  - README.md
  - docs/doctrine/schema/C10_table_oracle_record_schema.md
  - docs/doctrine/operations/batch_b/B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md
  - docs/doctrine/schema/C09_hazard_environment_record_schema.md
problem_summary: Table/oracle records are comparatively structured, but runtime RNG, table invocation events, weights, result domains, replay references, and hidden result redaction remain unowned.
why_backend_owned: Randomness and oracle selection must be deterministic, auditable, seedable/replayable, and hidden where necessary; the LLM cannot roll, choose, or alter results.
required_owner_files_or_workstreams:
  - future RNG/dice authority owner
  - future table/oracle registry owner
  - future oracle invocation event owner
  - future hidden-result context projection owner
required_outputs:
  - schema
  - math
  - command_ir
  - runtime_state
  - event_model
  - validator
  - context_packet
  - tests
dependencies:
  - RT-001-command-lifecycle-action-legality
  - RT-005-scene-activity-context-packets
blocked_by:
  - missing runtime RNG owner
  - missing table invocation event owner
  - missing table weight/result validator
recommended_first_pr: Draft an RNG/table/oracle owner-boundary scaffold that states backend RNG authority, invocation event requirements, replay references, and no-LLM-roll prohibitions.
must_not_do_in_first_pr:
  - implement RNG
  - create oracle registry data
  - create random tables
  - commit oracle outcomes
acceptance_tests_needed:
  - no-LLM-oracle-roll test family
  - RNG owner-boundary assertion test
  - table weight validation planning test
notes: This track is P1 because it supports hazards, missions, rewards, and encounters after command/context boundaries are established.
```

### Track RT-010 — Inventory, item, gear, vehicle, and persistent asset state

```yaml
track_id: RT-010-inventory-item-vehicle-assets
priority: P2
title: Inventory, item, gear, vehicle, and persistent asset state
risk_level: high
source_audit_records:
  - AUDIT-WAVE2-001 B03.item_gear_equipment_asset_use_boundary
  - AUDIT-WAVE2-001 C02.item_gear_record_schema_boundary
  - AUDIT-WAVE2-001 C08.vehicle_ship_platform_record_schema_boundary
affected_source_files:
  - docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md
  - docs/doctrine/schema/C02_item_gear_record_schema.md
  - docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md
problem_summary: Items, gear, equipment, and vehicles require instance persistence, custody, slots/loadouts, charges, durability, cooldowns, cargo, crew, movement, damage, repair, and effect validation.
why_backend_owned: The LLM cannot invent item effects, ownership transfers, cargo, charges, vehicle movement, damage, or repairs because these are durable assets and mechanical commitments.
required_owner_files_or_workstreams:
  - future inventory/equipment runtime owner
  - future item instance schema owner
  - future vehicle/platform runtime owner
  - future asset effect validation owner
required_outputs:
  - schema
  - math
  - command_ir
  - runtime_state
  - event_model
  - validator
  - context_packet
  - tests
dependencies:
  - RT-001-command-lifecycle-action-legality
  - RT-002-resource-backlash-consequence-math
  - RT-008-generated-content-provenance
blocked_by:
  - missing item instance persistence model
  - missing equipment/loadout integration
  - missing vehicle movement/damage/capacity mechanics
recommended_first_pr: Create an inventory/asset owner-boundary scaffold that separates base records from runtime instances and lists custody/effect/durability/vehicle dependencies.
must_not_do_in_first_pr:
  - implement inventory runtime
  - create item instance schemas
  - generate items or vehicles
  - resolve item effects
acceptance_tests_needed:
  - no-LLM-item-effect test family
  - item instance non-implementation assertion test
  - vehicle cargo/damage non-authority test
notes: This is P2 because item/vehicle assets depend on command, cost/consequence, and generated-content provenance scaffolds.
```

### Track RT-011 — Validation and readiness tooling ownership

```yaml
track_id: RT-011-validation-readiness-tooling
priority: P0
title: Validation/readiness tooling versus prose-only governance
risk_level: medium
source_audit_records:
  - AUDIT-WAVE1-001 AUDIT-001.output_schema_and_no_implementation_gate
  - AUDIT-WAVE1-001 SM00.runtime_gate_dependency_and_math_gap_inventory
  - AUDIT-WAVE2-001 SM01.validation_schema_inventory_readiness_boundary
  - AUDIT-WAVE2-001 SM02.minimum_pilot_conversion_readiness_boundary
affected_source_files:
  - docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md
  - docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md
  - docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md
  - docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md
problem_summary: AUDIT-001, SM00, SM01, and SM02 provide governance structure and readiness controls, but executable validators, coverage matrices, approval/rejection event logs, and runtime-safe readiness checks remain future work.
why_backend_owned: Readiness, validation, and approval cannot be prose-only or model-asserted because runtime, generator, conversion, live-play, and canon gates require deterministic checks and reviewer-auditable decisions.
required_owner_files_or_workstreams:
  - future executable validator workstream
  - future schema coverage matrix owner
  - future readiness registry owner
  - future reviewer decision event owner
required_outputs:
  - schema
  - validator
  - event_model
  - tests
  - other
dependencies:
  - repo gate: no prose report may imply implementation
blocked_by:
  - missing executable validators
  - missing complete schema coverage mapping
  - missing approval/rejection event model
recommended_first_pr: Create a validation/readiness tooling owner-boundary scaffold that maps prose controls to future executable validator families without implementing validators.
must_not_do_in_first_pr:
  - implement validators
  - create final JSON schemas
  - approve pilot conversion outputs
  - authorize live play or training
acceptance_tests_needed:
  - owner-boundary file existence test
  - no-executable-validator assertion test
  - readiness-label/required-field planning test
notes: Although risk is medium, this track is P0 as planning infrastructure because it prevents future owner files from being mistaken for enforcement.
```

### Track RT-012 — D-series/native-design promotion boundary

```yaml
track_id: RT-012-d-series-promotion-boundary
priority: P1
title: D-series/native-design source-material promotion boundary
risk_level: high
source_audit_records:
  - AUDIT-WAVE2-001 D02.cost_commitment_success_at_cost_source_material_boundary
  - AUDIT-WAVE2-001 SM02.minimum_pilot_conversion_readiness_boundary
affected_source_files:
  - docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-03_cost_commitment_overinvestment_and_success_at_cost.md
  - docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md
  - docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md
problem_summary: D02 cost-commitment material and broader D-series source packs may inform design pressure, but they are draft source material only. Direct promotion to runtime authority, generators, live-play content, or canon would bypass audit and doctrine gates.
why_backend_owned: Source-material promotion changes authority boundaries and must be explicit, reviewed, traceable, and testable; the LLM cannot silently adopt draft source-pack material as current rules.
required_owner_files_or_workstreams:
  - future D-series promotion gate owner
  - future draft-source handoff record owner
  - future doctrine adoption decision owner
  - future no-direct-generator-use validator owner
required_outputs:
  - schema
  - validator
  - event_model
  - tests
  - other
dependencies:
  - RT-011-validation-readiness-tooling
  - repo gate: D-series remains draft source material unless explicitly promoted
blocked_by:
  - missing promotion decision workflow
  - missing draft-to-doctrine handoff record
  - missing no-direct-generator-use tests
recommended_first_pr: Create a D-series promotion-boundary owner-file scaffold that defines draft-source status, adoption prerequisites, prohibited uses, and escalation triggers.
must_not_do_in_first_pr:
  - promote D02 or any D-series material
  - define final cost commitment math from D02
  - feed D-series material into generators
  - create canon or live-play content
acceptance_tests_needed:
  - D-series draft-source boundary test family
  - no-direct-generator-use assertion test
  - no-canon-promotion assertion test
notes: This track protects later remediation from accidentally importing D-series source-pack material as runtime authority.
```

## 6. Recommended next safe PR sequence

This sequence replaces Wave 3 expansion with bounded remediation-planning PRs. Each PR should remain documentation/control-only unless a later explicit approval changes scope.

1. **PR-A: Remediation owner scaffolding and validation/readiness boundaries.** Create owner-file scaffolds for RT-001 and RT-011 only. Do not define final IR, schemas, validators, math, runtime, or generators.
2. **PR-B: Resource/consequence and combat/hazard owner scaffolds.** Add RT-002 and RT-003 boundary files after PR-A lands. Do not choose formulas, damage tables, recovery rules, or encounter runtime.
3. **PR-C: Context-packet and hidden-information owner scaffolds.** Add RT-005 with redaction, visibility, scene-state, and narration downstream-of-backend guardrails. Do not build packet compilers or live-play prompts.
4. **PR-D: Generated-content lifecycle and D-series promotion gates.** Add RT-008 and RT-012 boundary scaffolds. Do not create generators, generated records, retrieval indexes, canon promotion decisions, or D-series adoption.
5. **PR-E: Ability/skill and social/faction owner scaffolds.** Add RT-004 and RT-007 after command/cost/context/provenance scaffolds exist. Do not generate powers, mutate relationships, or commit faction actions.
6. **PR-F: Mission/reward/clue and RNG/table/oracle owner scaffolds.** Add RT-006 and RT-009 after context/provenance and command/event scaffolds exist. Do not roll tables, generate missions, reveal clues, or commit rewards.
7. **PR-G: Inventory/item/vehicle persistent asset owner scaffold.** Add RT-010 after command, cost, provenance, and consequence scaffolds exist. Do not implement inventory, item effects, vehicle movement, cargo, or damage.

## 7. Global guardrails for all first remediation PRs

- Keep first PRs small, owner-boundary oriented, and non-runtime.
- Cite accepted audit record IDs and source files.
- Preserve backend-first model interchangeability.
- Keep the LLM limited to narration, summary, clarification, and constrained proposals downstream of backend contracts.
- Do not treat `schema_ready`, `generator_ready`, `validator_ready`, or `context_packet_ready` audit labels as runtime readiness.
- Do not perform donor-content audits or import donor rules directly.
- Do not treat D-series/native-design source material as current authority.
- Do not create live-play, training, canon, generator, validator, persistence, context-packet, command IR, or runtime artifacts in first PRs.
