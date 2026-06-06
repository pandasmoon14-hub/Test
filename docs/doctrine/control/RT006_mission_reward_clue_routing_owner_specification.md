# RT-006 Mission / Reward / Clue Routing Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification; non-executable planning artifact only
Tracking ID: REMEDIATION-STAGE2-RT006-MISSION-REWARD-CLUE-ROUTING-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-G3
Parent Stage 2 PR ID: STAGE2-PR-G
Track: RT-006
Owner: Astra Doctrine Council / future mission, scenario, objective, branch, clue, hidden-truth, reward, penalty, success, failure, route, escalation, and consequence-routing boundary owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-006 mission/reward/clue routing ownership. It upgrades the RT-006 owner scaffold into a specification-level planning artifact, but it remains non-executable and non-implementation. It does not implement mission systems, quest systems, scenario engines, adventure runtime, objective state machines, branch engines, clue reveal algorithms, investigation rules, hidden-truth reveal procedures, reward economies, mission reward tables, failure/success tables, route planners, escalation clocks, campaign clocks, schemas, validators, command IR, runtime code, generators, RNG/table logic, event ledgers, persistence writers, retrieval indexes, context-packet compilers, live-play prompts, training data, donor-content audits, sourcebook inclusion authorization, pilot conversion authorization, or canon promotion.

This owner specification is split from the original STAGE2-PR-G downstream-domain bundle for review safety. STAGE2-PR-G1 handled RT-003, STAGE2-PR-G2 handled RT-004, and this STAGE2-PR-G3 artifact handles only RT-006.

Required authority and planning links:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- RT006 owner scaffold: `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md`.
- RT001 owner specification: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- RT002 owner specification: `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`.
- RT003 owner specification: `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md`.
- RT004 owner specification: `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md`.
- RT005 owner specification: `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md`.
- RT008 owner specification: `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md`.
- RT009 owner specification: `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md`.
- RT011 owner specification: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.

## 2. Source availability disclosure

The Stage 2 RT-006 drafting pass inspected actual repository paths and used only existing files. Planning and audit sources inspected were `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`, `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`, `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, and `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.

Current RT owner files inspected were the RT-006 owner scaffold, the RT-001, RT-002, RT-003, RT-004, RT-005, RT-008, RT-009, and RT-011 owner specifications, and the RT-007, RT-010, and RT-012 owner scaffolds listed in Section 1 and Section 11.

Mission/reward/clue/source pressure files confirmed present and inspected include `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`, `docs/doctrine/schema/C05_faction_institution_record_schema.md`, `docs/doctrine/schema/C06_location_site_region_record_schema.md`, `docs/doctrine/schema/C09_hazard_environment_record_schema.md`, `docs/doctrine/schema/C10_table_oracle_record_schema.md`, `docs/doctrine/schema/C01_creature_npc_record_schema.md`, `docs/doctrine/schema/C02_item_gear_record_schema.md`, `docs/doctrine/schema/C03_ability_power_technique_record_schema.md`, `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md`, `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md`, `docs/doctrine/operations/batch_b/B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md`, `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md`, `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`, and `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`.

The requested optional paths `docs/doctrine/operations/batch_b/B01_scene_activity_orchestration_and_runtime_authority_procedure.md`, `docs/doctrine/operations/batch_b/B07_mission_objective_reward_and_failure_routing_procedure.md`, and `docs/doctrine/operations/batch_b/B08_clue_revelation_information_routing_and_investigation_procedure.md` were absent. The nearest actual equivalents confirmed present are `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md`, `docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md`, and `docs/doctrine/operations/batch_b/B08_travel_exploration_navigation_and_discovery_procedure.md`; this owner specification treats them only as source-pressure evidence and does not rewrite or extend them.

Runtime/project authority sources inspected include `docs/doctrine/astra_doctrine_roadmap_v0_1.md`, `docs/doctrine/astra_doctrine_registry_v0_1.yaml`, `docs/decisions/current_decisions_log.md`, and `README.md`. README.md reaffirms backend-first and model-interchangeability posture: the LLM is not the game engine, backend runtime owns truth, and mature live play requires backend-owned state, dice, validation, persistence, context packets, and event commits.

## 3. Scope: what RT-006 owns

RT-006 owns Stage 2 owner-specification planning for mission/reward/clue routing ownership boundaries. At this stage, ownership means semantic requirement boundaries and downstream handoff obligations, not mechanics, state machines, schemas, validators, or runtime code.

RT-006 owns planning boundaries for:

- mission/reward/clue routing ownership boundaries;
- mission, scenario, adventure, objective, branch, route, escalation, reward, penalty, success, failure, clue, and hidden-truth routing requirement boundaries;
- objective-state and scenario-branch requirement boundaries without implementing objective state machines or branch engines;
- clue visibility, clue routing, clue-cost, hidden-truth reveal, and investigation handoff requirements;
- reward, penalty, loss, compensation, debt, obligation, reputation, item, asset, ability, and faction consequence routing requirements;
- mission-to-command handoff requirements through RT-001;
- mission reward/cost/loss/consequence handoff requirements through RT-002;
- hazard/opposition/active-threat mission consequence handoff requirements through RT-003;
- ability/effect/skill reward or gated-effect handoff requirements through RT-004;
- hidden clue, hidden truth, redacted objective, rumor, false clue, and narrator visibility handoff through RT-005;
- generated mission/scenario/clue/provenance handoff through RT-008;
- random mission, clue, reward, penalty, branch, or oracle dependency handoff through RT-009;
- item/relic/vehicle/asset reward or loss handoff through RT-010;
- social/faction/reputation/institutional consequence handoff through RT-007;
- validation/readiness handoff through RT-011;
- D-series/native-design pressure handoff through RT-012;
- auditability requirements.

## 4. Must-not-own boundaries

RT-006 must not own or claim to complete:

- final mission system;
- final quest system;
- final scenario engine;
- final adventure runtime;
- final objective state machine;
- final branch engine;
- final clue reveal algorithm;
- final investigation rules;
- final hidden-truth reveal procedure;
- final reward economy;
- final mission reward tables;
- final failure/success tables;
- final route planner;
- final escalation clocks;
- final campaign clocks;
- final mission schema;
- final clue schema;
- final reward schema;
- final objective schema;
- final scenario state schema;
- schema implementation;
- command IR implementation;
- runtime code;
- validator implementation;
- generator implementation;
- RNG/dice/table implementation;
- event ledger implementation;
- persistence writer implementation;
- retrieval index implementation;
- context-packet compiler implementation;
- live-play prompt implementation;
- training data;
- donor-content audits;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion.

## 5. Authority model

- RT-001 owns command/action timing, legality, mission action declaration, rejection/quarantine, resolution-trigger handoff, and event-commit boundaries.
- RT-002 owns resource costs, mission rewards, penalties, losses, compensation, debt, obligation-as-cost pressure, recovery costs, reward/loss math, and consequence math.
- RT-003 owns combat, hazard, damage, opposition, active-threat, exposure, and recovery consequences inside missions/scenarios.
- RT-004 owns ability, effect, skill, clue-gated capability, reward-granted capability, and prerequisite interactions.
- RT-005 owns hidden clues, hidden truths, redacted objectives, false clues, rumors, player-known facts, character-known facts, NPC/faction-known facts, and narrator projection.
- RT-007 owns social/faction/reputation/institutional consequences, relationship effects, actor knowledge, and faction response.
- RT-008 owns generated mission/scenario/clue/provenance, source-local status, durable eligibility, and recurrence.
- RT-009 owns random table/oracle dependencies for mission branches, clue selection, reward selection, penalties, encounters, or complications.
- RT-010 owns item, vehicle, relic, asset, cargo, salvage, requisition, inventory reward, and asset-loss handoffs.
- RT-011 owns validation/readiness requirements.
- Future backend runtime must own mission/scenario state, objective state, branch state, reveal state, reward/loss state, event commits, and persistence if separately authorized.
- The LLM may only narrate backend-approved visible mission/clue/reward outcomes and may not reveal hidden truths, assign rewards, decide objective completion, select clues, choose branches, or commit scenario consequences.

## 6. Mission/reward/clue routing contract

The following conceptual routing placeholders are planning terms only:

- mission_route_required;
- scenario_state_pending;
- objective_state_pending;
- objective_completion_pending;
- branch_resolution_pending;
- escalation_dependency_pending;
- clue_route_required;
- clue_visibility_required;
- clue_cost_dependency;
- hidden_truth_reveal_pending;
- false_clue_or_rumor_partition_required;
- reward_route_pending;
- penalty_or_loss_route_pending;
- failure_outcome_pending;
- success_outcome_pending;
- complication_dependency_pending;
- faction_response_dependency;
- reputation_consequence_dependency;
- item_or_asset_reward_dependency;
- ability_or_effect_reward_dependency;
- random_mission_or_clue_dependency;
- generated_mission_provenance_required;
- scenario_consequence_event_pending;
- mission_resolution_quarantined.

These routing terms are planning placeholders only. They are not final schemas, not database fields, not mission rules, not quest rules, not clue reveal algorithms, not reward tables, not branch engines, not objective state machines, not clocks, not runtime state, not event records, not validators, and not live-play prompts.

## 7. Clue, hidden-truth, and investigation routing contract

Planning-level clue, hidden-truth, and investigation requirements are:

- clues are not automatically revealed by narration;
- clue candidates are not player-known facts until backend visibility authorizes them;
- hidden truths require backend-owned reveal authorization and RT-005 projection;
- false clues, rumors, and unverified claims must remain distinct from verified facts;
- investigation procedures cannot rely on LLM inference or model memory;
- clue costs or clue-risk consequences route through RT-002 and RT-005;
- clue revelation tied to hazards routes through RT-003;
- clue revelation tied to abilities/effects/routes/prerequisites routes through RT-004;
- clue revelation tied to social/faction knowledge routes through RT-007;
- generated clues require RT-008 provenance;
- random clues or oracle-derived clues require RT-009 authority;
- validation/readiness requires RT-011.

This contract does not define final clue schema, reveal algorithm, investigation procedure, actor-knowledge schema, or hidden-truth database.

## 8. Reward, penalty, success, and failure routing contract

Planning-level reward, penalty, success, and failure requirements are:

- reward labels are not reward economy;
- penalty labels are not consequence math;
- objective completion is not reward commitment;
- mission success/failure declaration is not event commitment;
- rewards involving resources, costs, debt, obligation, reputation, losses, or compensation route through RT-002 and RT-007 as applicable;
- rewards involving abilities/effects/skills route through RT-004;
- rewards involving items, vehicles, relics, assets, cargo, salvage, or requisition route through RT-010;
- random rewards, penalties, branches, complications, or oracle outputs route through RT-009;
- generated missions or recurring scenario content route through RT-008;
- hidden reward/penalty information routes through RT-005;
- event/state/persistence commitment requires future separately authorized backend systems.

This contract does not define final reward values, tables, economy, failure tables, success tables, branch rules, or persistence fields.

## 9. Mission/scenario commitment contract

- Mission declaration is not mission creation.
- Objective declaration is not objective completion.
- Branch proposal is not branch resolution.
- Clue candidate is not revealed clue.
- Reward proposal is not reward commitment.
- Penalty proposal is not penalty commitment.
- Random mission/clue/reward dependency is not random outcome selection.
- Generated mission proposal is not durable generated content.
- Narration is not event commitment.
- Rejected/quarantined mission/scenario/clue/reward actions must not mutate state.
- Event/state/persistence commitment requires future separately authorized backend systems.

This contract does not define final event schemas, runtime state machines, mission state machines, clue reveal state machines, or executable mission procedures.

## 10. Future mission/reward/clue artifact inventory

The following future artifact families are semantic requirements only, not implemented schemas, records, validators, services, formulas, generators, or runtime code. They do not define final fields, formulas, JSON schema, database schema, Pydantic models, validator code, RNG code, mission code, clue code, reward code, branch code, event code, persistence code, retrieval code, context-packet compiler code, or runtime code.

| Future artifact family | Purpose | Owner | LLM allowed interaction, if any | Downstream handoff | Implementation status |
| --- | --- | --- | --- | --- | --- |
| MissionRoutingRequirement | Require mission route ownership before mission truth is claimed. | RT-006 | Narrate backend-approved visible route summaries only. | RT-001, RT-011 | future_required_not_implemented |
| ScenarioStateRequirement | Require scenario-state ownership before scenario state is mutated. | Future backend runtime / RT-006 planning | Summarize visible scenario status only. | RT-001, RT-011 | future_required_not_implemented |
| ObjectiveStateRequirement | Require objective-state ownership before objective state is mutated. | Future backend runtime / RT-006 planning | Describe visible objective labels only. | RT-001, RT-011 | future_required_not_implemented |
| ObjectiveCompletionRequirement | Require completion authority separate from narration. | RT-006 with future backend runtime | Report backend-approved completion only. | RT-001, RT-002 | future_required_not_implemented |
| ScenarioBranchRequirement | Require branch routing before branch resolution. | RT-006 | Present backend-approved branch choices only. | RT-001, RT-009 | future_required_not_implemented |
| EscalationRequirement | Require escalation dependency ownership without clocks. | RT-006 | Narrate visible escalation pressure only. | RT-003, RT-011 | future_required_not_implemented |
| ClueRoutingRequirement | Require clue route ownership before clue movement. | RT-006 | Narrate visible clue context only. | RT-005, RT-011 | future_required_not_implemented |
| ClueVisibilityRequirement | Require visibility authorization before clue projection. | RT-005 / RT-006 | Project only backend-approved visible clues. | RT-005, RT-011 | future_required_not_implemented |
| HiddenTruthRevealRequirement | Require reveal authority for hidden truths. | RT-005 / RT-006 | No hidden truth narration unless approved. | RT-005, RT-001 | future_required_not_implemented |
| FalseClueRumorRequirement | Require false clue, rumor, and unverified-claim separation. | RT-005 / RT-006 | Label only backend-approved visibility categories. | RT-005, RT-007 | future_required_not_implemented |
| InvestigationBoundaryRequirement | Require investigation handoff boundaries. | RT-006 | Interpret player intent into non-authoritative proposals. | RT-001, RT-005 | future_required_not_implemented |
| RewardRoutingRequirement | Require reward route ownership before reward commitment. | RT-006 | Narrate backend-approved reward proposals only. | RT-002, RT-010 | future_required_not_implemented |
| PenaltyLossRoutingRequirement | Require penalty/loss routing before consequences. | RT-006 | Narrate backend-approved visible losses only. | RT-002, RT-003 | future_required_not_implemented |
| SuccessFailureOutcomeRequirement | Require success/failure outcome routing before event commitment. | RT-006 | Report backend-approved visible outcomes only. | RT-001, RT-002 | future_required_not_implemented |
| ComplicationRequirement | Require complication dependency routing. | RT-006 | Narrate backend-approved complications only. | RT-003, RT-009 | future_required_not_implemented |
| FactionResponseRequirement | Require faction response routing. | RT-007 / RT-006 | Narrate backend-approved social consequences only. | RT-007, RT-005 | future_required_not_implemented |
| ReputationConsequenceRequirement | Require reputation consequence routing. | RT-007 / RT-006 | Narrate visible reputation changes only if approved. | RT-007, RT-002 | future_required_not_implemented |
| ItemAssetRewardRequirement | Require item/asset reward and loss routing. | RT-010 / RT-006 | Narrate visible item/asset outcomes only. | RT-010, RT-002 | future_required_not_implemented |
| AbilityEffectRewardRequirement | Require ability/effect reward routing. | RT-004 / RT-006 | Narrate visible capability outcomes only. | RT-004, RT-002 | future_required_not_implemented |
| RandomMissionClueRequirement | Require random mission/clue/reward dependency routing. | RT-009 / RT-006 | Describe random dependency only after backend approval. | RT-009, RT-011 | future_required_not_implemented |
| GeneratedMissionProvenanceRequirement | Require generated mission/clue provenance. | RT-008 / RT-006 | Narrate visible generated content only as source-local/provenance-approved. | RT-008, RT-011 | future_required_not_implemented |
| ScenarioConsequenceEventRequirement | Require event-boundary routing for scenario consequences. | RT-001 / RT-006 | Narrate committed visible events only. | RT-001, RT-002 | future_required_not_implemented |
| MissionRewardClueValidationRequirement | Require validation/readiness governance. | RT-011 / RT-006 | No validator authority; may summarize validation status. | RT-011 | future_required_not_implemented |

## 11. Validation and readiness requirements

These validation and readiness requirements are future requirements only and coordinate with RT-011. This PR does not implement validators.

- source linkage validation;
- mission/reward/clue owner-boundary validation;
- objective/branch/route coverage validation;
- clue visibility and hidden-truth routing validation;
- rumor/false-clue/unverified-claim separation validation;
- reward/penalty/success/failure routing validation;
- cost/consequence handoff validation;
- combat/hazard/opposition handoff validation;
- ability/effect/skill reward handoff validation;
- social/faction/reputation handoff validation;
- generated-mission provenance validation;
- random mission/clue/reward dependency validation;
- item/asset reward/loss handoff validation;
- command/event boundary validation;
- LLM non-authority validation;
- non-implementation guardrail validation.

## 12. Downstream handoffs

- RT-001 for command lifecycle, action legality, objective action declarations, mission action timing, rejection/quarantine, and event/state commitment boundaries.
- RT-002 for resource rewards, costs, penalties, compensation, losses, debt, obligation, recovery costs, reward/loss math, and consequence math.
- RT-003 for combat, hazard, active-threat, exposure, damage, injury, recovery, and opposition consequences inside missions/scenarios.
- RT-004 for mission abilities, clue-gated effects, scenario branch effects, reward-granting effects, penalty effects, hidden-truth interactions, and prerequisite-linked mission actions.
- RT-005 for hidden clues, hidden truths, false clues, rumors, redacted objectives, visible facts, player-known facts, character-known facts, narrator fact-set limits, and context-packet projection.
- RT-006 for mission, scenario, adventure, objective, branch, route, escalation, reward, penalty, success, failure, clue, hidden-truth, clue-cost, scenario consequence, clue visibility, mission-state, and reward-routing owner-spec planning.
- RT-007 for social/faction/reputation/institutional consequences, faction response, relationship effects, actor knowledge, witness state, and mission patron/contact state.
- RT-008 for generated missions, generated clues, generated objectives, generated scenario branches, generated rewards/penalties, source-local scenario content, durable eligibility, recurrence eligibility, and provenance.
- RT-009 for random missions, random clues, random objectives, random rewards, random penalties, complications, encounter tables, oracle-derived branches, and table dependencies.
- RT-010 for item, gear, relic, implant, vehicle, platform, cargo, salvage, requisition, asset rewards, asset losses, and inventory handoffs.
- RT-011 for validation/readiness governance.
- RT-012 for D-series/native-design mission, scenario, clue, reward, or investigation patterns that cannot become runtime/canon/sourcebook authority without promotion.

## 13. LLM non-authority rules

The LLM is explicitly prohibited from:

- creating missions as backend truth;
- deciding objective completion;
- choosing scenario branches;
- selecting clues;
- revealing hidden truths;
- revealing hidden clues;
- converting rumors or false clues into verified facts;
- deciding player-known, character-known, NPC-known, or faction-known mission facts;
- assigning rewards;
- assigning penalties;
- determining mission success or failure as mechanical truth;
- creating reward values;
- creating reward tables;
- choosing random mission, clue, reward, or penalty outcomes;
- creating generated missions, clues, or scenario branches as durable backend truth;
- mutating mission state;
- mutating objective state;
- mutating scenario state;
- committing reward/loss events;
- treating mission narration as event commitment;
- treating summaries as mission memory authority;
- inventing schemas, fields, state machines, clocks, routes, tables, or formulas;
- bypassing RT-001, RT-002, RT-005, RT-008, RT-009, or RT-011;
- authorizing canon/sourcebook/training/live-play use.

## 14. Non-implementation reaffirmation

This PR adds no sourcebook inclusion authorization, no pilot conversion authorization, no canon promotion, and no:

- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- generator implementation;
- mission system;
- quest system;
- scenario engine;
- adventure runtime;
- objective state machine;
- branch engine;
- clue reveal algorithm;
- investigation rules;
- hidden-truth reveal procedure;
- reward economy;
- mission reward tables;
- failure/success tables;
- route planner;
- escalation clocks;
- campaign clocks;
- mission schema;
- clue schema;
- reward schema;
- objective schema;
- scenario state schema;
- RNG/dice/table implementation;
- event ledger implementation;
- database schema;
- persistence writer;
- retrieval index;
- context-packet compiler;
- live-play prompt;
- training data;
- donor-content audit;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion.

## 15. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-G3
  parent_stage2_pr_id: STAGE2-PR-G
  track: RT-006
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_validator_implementation: false
  authorizes_generator_implementation: false
  authorizes_mission_system: false
  authorizes_quest_system: false
  authorizes_scenario_engine: false
  authorizes_objective_state_machine: false
  authorizes_branch_engine: false
  authorizes_clue_reveal_algorithm: false
  authorizes_investigation_rules: false
  authorizes_reward_economy: false
  authorizes_reward_tables: false
  authorizes_mission_clocks: false
  authorizes_rng_implementation: false
  authorizes_event_ledger: false
  authorizes_context_packet_compiler: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  authorizes_pilot_conversion: false
  next_allowed_step: RT-007 owner specification, pending review
```
