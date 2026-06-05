# Runtime Boundary + Generator Ownership Audit — Wave 2

Date prepared: 2026-06-05
Status: Wave 2 audit report only
Owner: Astra Doctrine Council / Runtime Boundary Reviewers
Decision ID: AUDIT-WAVE2-001

## Purpose and scope

This report applies the Runtime Boundary + Generator Ownership Audit protocol to a larger but still bounded Wave 2 slice of high-risk adjacent subsystem seams. This is Wave 2 only. It expands horizontal audit coverage after AUDIT-WAVE1-001 and does not remediate, rewrite, implement, validate, generate, persist, compile context packets, authorize live play, create training data, audit donor content directly, or promote canon.

Wave 2 inspected 14 subsystem records selected from actual repo files:

- Batch A skill/competency/synthesis and resource/cost/backlash/corruption pressure.
- Batch B scene/action/item/social operational seams.
- Batch C item/location/mission/vehicle/table schema seams.
- SM validation/readiness workstream files.
- One D-series/native-design source-pack sample treated as draft source material only.

## Relationship to AUDIT-001 and AUDIT-WAVE1-001

AUDIT-001 is the controlling protocol for this report: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`. Wave 2 reuses the canonical audit record schema, allowed classification labels, risk levels, D-series draft-source rule, and non-goal boundaries from AUDIT-001.

AUDIT-WAVE1-001 is the prior limited report: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`. Wave 1 validated the method across 10 representative records and recommended expanding horizontally into adjacent A09/A10, B01/B02/B03/B09, C02/C06/C07/C08/C10, SM readiness, and D-series source-pack seams. Wave 2 follows that recommendation without changing Wave 1 findings.

## Files inspected

- `README.md`
- `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`
- `docs/doctrine/astra_doctrine_roadmap_v0_1.md`
- `docs/doctrine/astra_doctrine_registry_v0_1.yaml`
- `docs/operations/current_decisions_log_v0_1.md`
- `docs/doctrine/advancement/A09_skill_competency_and_synthesis_doctrine.md`
- `docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md`
- `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md`
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md`
- `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md`
- `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md`
- `docs/doctrine/schema/C02_item_gear_record_schema.md`
- `docs/doctrine/schema/C06_location_site_region_record_schema.md`
- `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`
- `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md`
- `docs/doctrine/schema/C10_table_oracle_record_schema.md`
- `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`
- `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`
- `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-03_cost_commitment_overinvestment_and_success_at_cost.md`

## Substitutions

No requested Wave 2 scope item required substitution. A10 exists as `docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md`; SM01 and SM02 were selected from the available SM01-SM04 readiness files; the D-series/native-design sample uses the actual D02 cost-commitment source-pack file and is treated as draft source material only, not current runtime authority.

## Non-remediation and non-implementation statement

This is Wave 2 only. This report performs no doctrine rewrite, no runtime implementation, no generator implementation, no validator implementation, no persistence writer implementation, no command IR implementation, no context-packet compiler implementation, no live-play/training authorization, no donor-content audit, and no canon promotion. It does not create runtime code, database schemas, command IR, generators, validators, persistence writers, context-packet compilers, live-play adapters, training material, or canonical content.

## Audit records

### Record 1 — A09.skill_competency_synthesis_boundary

```yaml
subsystem_id: A09.skill_competency_synthesis_boundary
source_area: Batch A
source_files:
  - docs/doctrine/advancement/A09_skill_competency_and_synthesis_doctrine.md
classification:
  - doctrine_only
  - blocked_pending_schema
  - blocked_pending_math
doctrine_owner: docs/doctrine/advancement/A09_skill_competency_and_synthesis_doctrine.md
backend_truth_owner: pending skill/competency runtime owner
missing_backend_pieces:
  - skill record schema
  - competency rating and prerequisite mechanics
  - synthesis attempt lifecycle
  - backend validation for combining competencies
required_schemas:
  - skill competency record schema
  - synthesis candidate and result schema
  - actor capability state schema
required_math_mechanics:
  - competency thresholds
  - synthesis costs, failure bands, and advancement rules
  - conflict and prerequisite resolution rules
required_generators_templates:
  - constrained synthesis proposal template after schema and provenance exist
required_command_ir:
  - declare-skill-use and attempt-synthesis command IR
required_state_event_fields:
  - actor_skill_state
  - competency_progress_state
  - synthesis_attempt_event
  - synthesis_result_state
required_context_packet_projection:
  - actor-visible skills, known prerequisites, and eligible synthesis options only
required_narration_contract:
  - narration may describe training or attempt flavor but cannot award skills, invent synthesis outputs, or set persistent competency state
required_tests:
  - no-LLM-skill-award tests
  - synthesis validation and provenance tests
  - context packet skill visibility tests
llm_overreach_risk: high
blocked_by:
  - skill schema owner
  - SM math/mechanics workstream
  - future runtime command/state/event owner
recommended_next_action: Route A09 to schema and math owners before allowing any live synthesis or persistent skill changes.
notes: The doctrine creates strong skill/synthesis design pressure but not enough backend-owned mechanics to prevent LLM invention of capabilities or progression.
```

### Record 2 — A10.resource_cost_backlash_corruption_boundary

```yaml
subsystem_id: A10.resource_cost_backlash_corruption_boundary
source_area: Batch A
source_files:
  - docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md
classification:
  - doctrine_only
  - blocked_pending_math
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md
backend_truth_owner: pending resource/cost/backlash runtime owner
missing_backend_pieces:
  - canonical resource pool and reserve schemas
  - cost commitment and backlash math
  - corruption/strain state lifecycle
  - deterministic consequence routing
required_schemas:
  - resource pool state schema
  - cost commitment ledger schema
  - backlash/corruption/strain condition schema
required_math_mechanics:
  - spend, reserve, overcommit, and recovery rules
  - backlash severity and escalation bands
  - corruption and strain thresholds
required_generators_templates:
  - none until costs and consequences are backend-owned
required_command_ir:
  - commit-cost, resolve-backlash, recover-resource, and apply-strain command IR
required_state_event_fields:
  - resource_pool_state
  - cost_commitment_event
  - backlash_event
  - corruption_strain_state
required_context_packet_projection:
  - actor-visible resources, committed costs, and visible consequences without hidden threshold leakage
required_narration_contract:
  - narration may describe committed cost/backlash outcomes but cannot invent resource loss, corruption, or recovery
required_tests:
  - no-LLM-resource-spend tests
  - backlash math ownership tests
  - state delta persistence tests
llm_overreach_risk: critical
blocked_by:
  - SM math/mechanics workstream
  - future runtime state/event owner
recommended_next_action: Prioritize backend math and event ownership for resources before ability, action, or advancement subsystems consume A10.
notes: This seam repeats Wave 1's consequence-risk pattern because missing backend math would force the LLM to decide costs, backlash, and persistent harm.
```

### Record 3 — B01.scene_encounter_activity_orchestration_boundary

```yaml
subsystem_id: B01.scene_encounter_activity_orchestration_boundary
source_area: Batch B
source_files:
  - docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md
classification:
  - doctrine_only
  - blocked_pending_runtime
  - context_packet_ready
doctrine_owner: docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md
backend_truth_owner: pending scene/activity runtime orchestrator
missing_backend_pieces:
  - scene lifecycle state model
  - encounter/activity transition rules
  - participant and visibility partition ownership
  - backend event ordering and commit rules
required_schemas:
  - scene record schema
  - encounter/activity state schema
  - participant visibility schema
required_math_mechanics:
  - time/turn/phase advancement rules where scenes invoke mechanics
  - escalation and exit criteria
required_generators_templates:
  - scene framing template only after generated content provenance and visibility rules exist
required_command_ir:
  - open-scene, update-scene, declare-activity, transition-scene, and close-scene command IR
required_state_event_fields:
  - scene_id
  - activity_state
  - participant_roster
  - visibility_partition
  - scene_event_log
required_context_packet_projection:
  - active scene state, visible participants, available actions, and hidden-state redactions
required_narration_contract:
  - narration may frame committed scene state but cannot create hidden facts, participants, stakes, exits, or consequences
required_tests:
  - scene lifecycle event ordering tests
  - hidden participant/context redaction tests
  - no-LLM-scene-state-mutation tests
llm_overreach_risk: high
blocked_by:
  - future scene runtime owner
  - command IR owner
  - context packet compiler owner
recommended_next_action: Treat B01 as an orchestration seam requiring runtime/event ownership before live-play use.
notes: B01 is central to many later procedures; without runtime orchestration, the LLM would own pacing, hidden facts, activity state, and transitions.
```

### Record 4 — B02.action_declaration_cost_commitment_lifecycle_boundary

```yaml
subsystem_id: B02.action_declaration_cost_commitment_lifecycle_boundary
source_area: Batch B
source_files:
  - docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md
classification:
  - doctrine_only
  - blocked_pending_math
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md
backend_truth_owner: pending command lifecycle runtime owner
missing_backend_pieces:
  - canonical command IR
  - cost commitment validation
  - action legality checks
  - backend resolution trigger routing
required_schemas:
  - command/action declaration schema
  - cost commitment schema
  - resolution trigger schema
required_math_mechanics:
  - action cost validation rules
  - trigger conditions and outcome routing rules
  - rollback/cancel/interrupt mechanics
required_generators_templates:
  - none until command lifecycle is backend-owned
required_command_ir:
  - full intent-to-command-to-resolution-to-state-delta IR
required_state_event_fields:
  - actor_id
  - declared_intent
  - committed_costs
  - legality_status
  - resolution_trigger
  - command_event
required_context_packet_projection:
  - legal available actions, committed costs, and pending resolution state
required_narration_contract:
  - narration may restate declared intent and committed outcomes but cannot validate legality, spend costs, or trigger resolution
required_tests:
  - command lifecycle state machine tests
  - no-LLM-cost-commit tests
  - invalid action rejection tests
llm_overreach_risk: critical
blocked_by:
  - command IR owner
  - cost/resource math owner
  - runtime event owner
recommended_next_action: Make B02 a Wave 3 priority for command/state/event decomposition, without implementing it in this audit.
notes: This is a core runtime seam; if unresolved, nearly every player action would require LLM-owned legality, cost, dice, and state mutation.
```

### Record 5 — B03.item_gear_equipment_asset_use_boundary

```yaml
subsystem_id: B03.item_gear_equipment_asset_use_boundary
source_area: Batch B
source_files:
  - docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md
classification:
  - doctrine_only
  - blocked_pending_schema
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md
backend_truth_owner: pending inventory/equipment runtime owner
missing_backend_pieces:
  - item instance and equipment state schema linkage
  - use/activate/equip/unequip command rules
  - charges, durability, custody, and cooldown mechanics
  - item effect validation routing
required_schemas:
  - item instance schema
  - equipment slot/loadout schema
  - item use event schema
required_math_mechanics:
  - durability, charge, burden, and cooldown rules
  - item effect and cost resolution rules
required_generators_templates:
  - item-use narration templates after C02 schema and provenance controls exist
required_command_ir:
  - equip, unequip, use-item, activate-asset, consume-charge command IR
required_state_event_fields:
  - item_id
  - owner_or_custodian_id
  - equipped_state
  - charge_durability_state
  - item_use_event
required_context_packet_projection:
  - actor-visible inventory, equipped items, usable actions, costs, and restrictions
required_narration_contract:
  - narration may describe committed item use but cannot invent item effects, ownership transfer, charges, or breakage
required_tests:
  - item use legality tests
  - inventory state mutation tests
  - no-LLM-item-effect tests
llm_overreach_risk: high
blocked_by:
  - C02 item schema owner
  - inventory/equipment runtime owner
  - command IR owner
recommended_next_action: Pair B03 with C02 and B04/B05 in a later ownership decomposition wave.
notes: Gear use creates persistent-state and effect-routing risk when item records, inventory, and command lifecycle are not backend-owned.
```

### Record 6 — B09.social_faction_contact_interaction_boundary

```yaml
subsystem_id: B09.social_faction_contact_interaction_boundary
source_area: Batch B
source_files:
  - docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md
classification:
  - doctrine_only
  - blocked_pending_schema
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md
backend_truth_owner: pending social/faction relationship runtime owner
missing_backend_pieces:
  - relationship and standing state schemas
  - NPC/faction knowledge and belief partitions
  - social action command lifecycle
  - institutional consequence routing
required_schemas:
  - relationship state schema
  - faction standing schema
  - NPC contact knowledge/belief schema
  - social interaction event schema
required_math_mechanics:
  - standing shift rules
  - influence, favor, obligation, and reputation mechanics
  - social consequence thresholds
required_generators_templates:
  - constrained social scene and faction response templates with provenance and state binding
required_command_ir:
  - persuade, negotiate, request, threaten, socialize, and faction-operation command IR
required_state_event_fields:
  - actor_id
  - contact_or_faction_id
  - relationship_state
  - standing_delta
  - knowledge_claim_delta
  - social_event
required_context_packet_projection:
  - actor-known relationship facts, visible stance, authorized rumors, and hidden-belief redactions
required_narration_contract:
  - narration may voice committed social outcomes but cannot invent relationship changes, faction actions, secrets, or obligations
required_tests:
  - no-LLM-relationship-mutation tests
  - hidden knowledge partition tests
  - faction standing delta tests
llm_overreach_risk: critical
blocked_by:
  - relationship schema owner
  - faction runtime owner
  - knowledge/dialogue memory owner
recommended_next_action: Include B09 and C05/D15-adjacent seams in Wave 3 for relationship and institutional state ownership.
notes: This repeats Wave 1 faction/generated-content recurrence concerns and adds actor knowledge, belief, and social consequence risks.
```

### Record 7 — C02.item_gear_record_schema_boundary

```yaml
subsystem_id: C02.item_gear_record_schema_boundary
source_area: Batch C
source_files:
  - docs/doctrine/schema/C02_item_gear_record_schema.md
classification:
  - schema_ready
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/schema/C02_item_gear_record_schema.md
backend_truth_owner: pending item/gear schema owner and runtime item instance owner
missing_backend_pieces:
  - runtime item instance persistence model
  - equipment slot/loadout integration
  - item effect execution and validation hooks
  - provenance handling for generated items
required_schemas:
  - item base record schema
  - item instance state schema
  - equipment/loadout linkage schema
required_math_mechanics:
  - item effect, durability, charge, cost, and burden mechanics
required_generators_templates:
  - backend-owned item generator/template with source/provenance fields and validator gates
required_command_ir:
  - item create/import/use/equip/transfer command IR
required_state_event_fields:
  - item_record_id
  - item_instance_id
  - provenance
  - ownership_state
  - mechanical_effect_refs
required_context_packet_projection:
  - player-visible item traits, restrictions, current state, and hidden provenance redactions where applicable
required_narration_contract:
  - narration may describe validated item traits but cannot create durable items or mechanical effects
required_tests:
  - item schema shape tests
  - generated item provenance tests
  - item instance persistence tests
llm_overreach_risk: high
blocked_by:
  - runtime item instance owner
  - generator provenance owner
  - mechanics owner
recommended_next_action: Keep C02 schema pressure separate from B03 runtime remediation until item instances and generators are owned.
notes: The record-shape direction is useful, but schema readiness is not runtime readiness for item effects, custody, or generated gear recurrence.
```

### Record 8 — C06.location_site_region_record_schema_boundary

```yaml
subsystem_id: C06.location_site_region_record_schema_boundary
source_area: Batch C
source_files:
  - docs/doctrine/schema/C06_location_site_region_record_schema.md
classification:
  - schema_ready
  - generator_ready
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/schema/C06_location_site_region_record_schema.md
backend_truth_owner: pending location/site/region record owner
missing_backend_pieces:
  - runtime location state and discovery persistence
  - hidden fact and access partition model
  - generated location provenance and recurrence controls
  - travel/scene integration hooks
required_schemas:
  - location/site/region record schema
  - discovery state schema
  - hidden feature and access schema
required_math_mechanics:
  - travel, access, hazard, and discovery mechanics from runtime owners
required_generators_templates:
  - backend-owned location/site generator template with stable IDs, provenance, tags, and validator gates
required_command_ir:
  - discover-location, enter-site, inspect-region, update-location-state command IR
required_state_event_fields:
  - location_id
  - discovered_by
  - access_state
  - hidden_feature_state
  - location_event
required_context_packet_projection:
  - visible location description, known exits, authorized secrets, and discovery state
required_narration_contract:
  - narration may describe visible locations but cannot invent durable sites, exits, hidden features, hazards, or canon geography
required_tests:
  - location provenance tests
  - hidden feature redaction tests
  - generated location recurrence tests
llm_overreach_risk: high
blocked_by:
  - runtime location/discovery owner
  - generator provenance owner
  - context packet compiler owner
recommended_next_action: Route location generation and discovery persistence to backend-owned generated-content and runtime state planning.
notes: Location records are relatively routeable for generator templates, but backend recurrence and hidden-state ownership remain mandatory.
```

### Record 9 — C07.mission_scenario_adventure_record_schema_boundary

```yaml
subsystem_id: C07.mission_scenario_adventure_record_schema_boundary
source_area: Batch C
source_files:
  - docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md
classification:
  - schema_ready
  - blocked_pending_runtime
  - blocked_pending_schema
doctrine_owner: docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md
backend_truth_owner: pending mission/scenario runtime and content record owner
missing_backend_pieces:
  - objective, branch, reward, and consequence state schemas
  - mission progress and completion mechanics
  - scenario hidden-truth and clue partitioning
  - durable adventure content provenance
required_schemas:
  - mission/scenario record schema
  - objective state schema
  - reward/consequence schema
  - clue and hidden-truth schema
required_math_mechanics:
  - objective progress, failure, timeout, and reward rules
  - branch and consequence resolution mechanics
required_generators_templates:
  - mission/scenario generator template with provenance, validation, and no-canon-promotion gates
required_command_ir:
  - accept-mission, update-objective, reveal-clue, complete/fail-mission command IR
required_state_event_fields:
  - mission_id
  - objective_state
  - clue_reveal_state
  - reward_commit_event
  - consequence_event
required_context_packet_projection:
  - accepted objectives, known clues, visible timers, and hidden branch redactions
required_narration_contract:
  - narration may frame committed objectives and clues but cannot invent rewards, hidden truths, mission branches, or canon outcomes
required_tests:
  - objective state transition tests
  - hidden clue redaction tests
  - no-LLM-reward-commit tests
llm_overreach_risk: critical
blocked_by:
  - mission runtime owner
  - reward/consequence owner
  - generated-content provenance owner
recommended_next_action: Defer generator use until mission state, clue partitions, reward commitment, and consequence routing are backend-owned.
notes: Scenario records combine hidden facts, recurrence, reward, and consequence risks, making schema prose insufficient for runtime use.
```

### Record 10 — C08.vehicle_ship_platform_record_schema_boundary

```yaml
subsystem_id: C08.vehicle_ship_platform_record_schema_boundary
source_area: Batch C
source_files:
  - docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md
classification:
  - schema_ready
  - blocked_pending_math
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md
backend_truth_owner: pending vehicle/platform runtime owner
missing_backend_pieces:
  - vehicle instance state schema
  - crew/cargo/capacity and integrity mechanics
  - movement, damage, repair, and platform action rules
  - custody and access control integration
required_schemas:
  - vehicle/platform base record schema
  - vehicle instance state schema
  - crew/cargo/capacity schema
required_math_mechanics:
  - movement, endurance, integrity, repair, damage, and burden/capacity rules
required_generators_templates:
  - vehicle/platform generator template after effect, capacity, and provenance validators exist
required_command_ir:
  - board, operate, move, damage, repair, load-cargo, and transfer-custody command IR
required_state_event_fields:
  - platform_id
  - location_state
  - crew_roster
  - cargo_state
  - integrity_state
  - platform_event
required_context_packet_projection:
  - visible platform status, crew permissions, cargo visibility, and operational options
required_narration_contract:
  - narration may describe committed platform status but cannot invent movement, cargo, damage, passengers, or repairs
required_tests:
  - vehicle state transition tests
  - platform capacity validation tests
  - no-LLM-damage-or-cargo tests
llm_overreach_risk: high
blocked_by:
  - platform runtime owner
  - movement/damage/capacity mechanics owner
  - command IR owner
recommended_next_action: Treat C08 as schema pressure for later runtime/mechanics decomposition, not as a usable vehicle runtime.
notes: Vehicles/platforms are persistent compound entities; item-style schema readiness does not cover movement, crew, cargo, or damage state.
```

### Record 11 — C10.table_oracle_record_schema_boundary

```yaml
subsystem_id: C10.table_oracle_record_schema_boundary
source_area: Batch C
source_files:
  - docs/doctrine/schema/C10_table_oracle_record_schema.md
classification:
  - schema_ready
  - generator_ready
  - validator_ready
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/schema/C10_table_oracle_record_schema.md
backend_truth_owner: pending table/oracle registry and RNG owner
missing_backend_pieces:
  - runtime RNG/dice ownership
  - table invocation event model
  - oracle result provenance and persistence rules
  - validation for table weights and result domains
required_schemas:
  - table/oracle record schema
  - weighted result schema
  - oracle invocation event schema
required_math_mechanics:
  - RNG, dice, weighting, replacement, and result-selection rules
required_generators_templates:
  - backend-owned table/oracle templates with weight validation and source/provenance fields
required_command_ir:
  - invoke-table, roll-oracle, select-result, commit-oracle-result command IR
required_state_event_fields:
  - table_id
  - seed_or_rng_ref
  - roll_result
  - selected_entry
  - oracle_event
required_context_packet_projection:
  - visible table result and provenance only when authorized; hidden oracle outputs remain redacted
required_narration_contract:
  - narration may describe committed oracle results but cannot roll dice, select entries, or alter table contents
required_tests:
  - table weight validation tests
  - deterministic RNG ownership tests
  - no-LLM-oracle-roll tests
llm_overreach_risk: medium
blocked_by:
  - runtime RNG owner
  - oracle invocation event owner
recommended_next_action: Convert C10 into a backend table/oracle registry candidate after RNG and invocation events are owned.
notes: C10 is comparatively routeable because table shapes can be validated, but runtime invocation cannot rely on LLM-selected results.
```

### Record 12 — SM01.validation_schema_inventory_readiness_boundary

```yaml
subsystem_id: SM01.validation_schema_inventory_readiness_boundary
source_area: schema/math/mechanics
source_files:
  - docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md
classification:
  - validator_ready
  - doctrine_only
doctrine_owner: docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md
backend_truth_owner: Astra Schema/Validation Workstream
missing_backend_pieces:
  - executable validator implementations for doctrine record families
  - schema coverage matrix tied to runtime consumers
  - automated readiness status registry for every schema family
required_schemas:
  - schema inventory status schema
  - validation readiness record schema
required_math_mechanics:
  - none except readiness scoring criteria if later formalized
required_generators_templates:
  - none; generator output should depend on validated schemas defined elsewhere
required_command_ir:
  - none
required_state_event_fields:
  - validation_status
  - schema_family_id
  - blocking_gap
  - readiness_gate
required_context_packet_projection:
  - validator/readiness status summaries for reviewers, not player-facing runtime packets
required_narration_contract:
  - report prose may summarize readiness but cannot imply schemas or validators have been implemented
required_tests:
  - schema inventory presence tests
  - allowed status/readiness label tests
  - no-runtime-implementation assertion tests
llm_overreach_risk: medium
blocked_by:
  - future executable validators
  - complete schema coverage mapping
recommended_next_action: Use SM01 as validation planning input for Wave 3, but do not treat it as implemented validation runtime.
notes: SM01 lowers audit ambiguity by naming readiness controls, but missing executable validators still leave risk if reports are mistaken for enforcement.
```

### Record 13 — SM02.minimum_pilot_conversion_readiness_boundary

```yaml
subsystem_id: SM02.minimum_pilot_conversion_readiness_boundary
source_area: schema/math/mechanics
source_files:
  - docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md
classification:
  - validator_ready
  - doctrine_only
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md
backend_truth_owner: Astra Schema/Validation Workstream and pilot readiness reviewers
missing_backend_pieces:
  - executable pilot packet validator
  - runtime-safe conversion packet state model
  - authoritative approval/rejection event logging
  - dependency checks across schema/math/runtime owners
required_schemas:
  - pilot packet readiness schema
  - validation finding schema
  - approval/rejection decision record schema
required_math_mechanics:
  - pass/fail gate criteria and severity thresholds
required_generators_templates:
  - none; pilot packets must not be generated into authority without validation and reviewer approval
required_command_ir:
  - none for live play; optional review-workflow command records if future tooling requires them
required_state_event_fields:
  - packet_id
  - validation_result
  - reviewer_decision
  - blocking_dependency
  - approval_event
required_context_packet_projection:
  - reviewer-facing readiness summaries only; no live-play context packet authority
required_narration_contract:
  - summaries may report validation posture but cannot authorize conversion, live play, training, or canon promotion
required_tests:
  - pilot readiness gate tests
  - no-live-play-authorization tests
  - no-training-material-creation tests
llm_overreach_risk: medium
blocked_by:
  - executable validator tooling
  - owner approval workflow
  - runtime state/event implementation if later connected to runtime
recommended_next_action: Keep SM02 as a readiness gate and include pilot authorization packet controls in Wave 3 if audit scope expands to SM03-SM04.
notes: SM02 is a control file, not runtime authority; the risk is governance overreach if readiness prose is treated as executable validation or approval.
```

### Record 14 — D02.cost_commitment_success_at_cost_source_material_boundary

```yaml
subsystem_id: D02.cost_commitment_success_at_cost_source_material_boundary
source_area: D00-D19
source_files:
  - docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-03_cost_commitment_overinvestment_and_success_at_cost.md
classification:
  - doctrine_only
  - blocked_pending_math
  - blocked_pending_runtime
doctrine_owner: docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-03_cost_commitment_overinvestment_and_success_at_cost.md
backend_truth_owner: none current; draft source material only unless later promoted by explicit repo authority
missing_backend_pieces:
  - promotion decision linking D02 pressure to current runtime doctrine
  - backend cost commitment math
  - command lifecycle integration
  - state/event persistence rules
required_schemas:
  - draft-to-doctrine handoff record if promoted
  - cost commitment and overinvestment schema if adopted
required_math_mechanics:
  - success-at-cost and overinvestment thresholds only after doctrine promotion
required_generators_templates:
  - none; D-series source material must not directly drive generators
required_command_ir:
  - none current; possible future B02/A10 command IR input after explicit adoption
required_state_event_fields:
  - draft_source_ref
  - promotion_status
  - adopted_rule_ref
  - cost_commitment_event if later adopted
required_context_packet_projection:
  - none for live play; reviewer-facing source pressure only
required_narration_contract:
  - narration must not treat this D-series draft source as current runtime authority or canon
required_tests:
  - D-series draft-source boundary tests
  - no-canon-promotion tests
  - no-direct-generator-use tests
llm_overreach_risk: high
blocked_by:
  - explicit doctrine promotion decision
  - A10/B02 runtime and math owners
recommended_next_action: Use D02 only as design pressure for future owner review; do not mark it runtime authority in audit findings.
notes: The file is valuable pressure for cost lifecycle design, but AUDIT-001 requires D-series material to remain draft source material unless the repo explicitly promotes it.
```

## Summary of LLM-overreach risks found

Wave 2 found persistent medium-to-critical LLM-overreach risk across the inspected seams:

- Critical risk appears where the LLM would otherwise decide costs, resource loss, command legality, relationship/faction state, hidden scenario facts, rewards, or consequences.
- High risk appears where the LLM would otherwise create or mutate durable skills, items, locations, vehicles, scenes, generated content recurrence, or D-series-derived mechanics without backend provenance and validators.
- Medium risk appears in validator/readiness and table/oracle seams where doctrine is more structured, but executable validators, RNG ownership, or runtime invocation events are still absent.
- No audited Wave 2 subsystem should be interpreted as live-play ready. Schema-ready or validator-ready labels identify routeability for future owner work, not runtime implementation.

## Comparison to Wave 1 patterns

Wave 2 confirms and broadens Wave 1 patterns:

- Wave 1's combat/consequence and ability/effect risks recur in A10, B02, B03, C07, and C08 because backend math and event ownership are still missing.
- Wave 1's advancement and technique risks recur in A09 through skill progression and synthesis outputs.
- Wave 1's faction/generated-content recurrence risks recur in B09 and C06/C07 through relationship state, hidden facts, generated locations, and mission recurrence.
- Wave 1's table/oracle and schema-readiness observations are refined by C10, SM01, and SM02: structured records and readiness controls help, but runtime RNG, invocation events, and executable validators remain separate owners.
- Wave 1's D-series caution remains mandatory: D-series material may exert design pressure but must not become current runtime authority, generator input, live-play content, or canon without explicit promotion.

## Recommended Wave 3 scope

Recommended Wave 3 scope should remain an audit-only expansion and should not remediate findings. Priorities:

1. Command lifecycle and runtime state/event seams: B02 plus adjacent B04 inventory custody, B05 acquisition/reward/value flow, and B10 hazard/opposition triggers.
2. Relationship, faction, and institutional state: B09 with C05 faction/institution and a D15 source-pack sample as draft-only pressure.
3. Mission/consequence/reward recurrence: C07 with C09 hazards, C10 oracles, and A13 consequence routing.
4. Schema/math/readiness controls: SM03-SM04 and later SM files if present, focusing on pilot packet boundaries and benchmark/evaluation controls.
5. Generated-content provenance and context packet seams: C06 locations, C02 items, C11 companions, and any actual future control files for generated-content records or narration validation.

## Registry and decision-log note

AUDIT-WAVE2-001 should be tracked as a concise registry/changelog entry if registry tracking is required. The tracking entry must state: Wave 2 audit report only; no doctrine rewrite; no runtime implementation; no generator implementation; no validator implementation; no persistence writer implementation; no command IR implementation; no context-packet compiler implementation; no canon promotion; and no live-play/training authorization.

A short decision-log entry is consistent with recent repo practice and records the same non-remediation boundaries.
