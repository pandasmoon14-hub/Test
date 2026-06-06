# Runtime Boundary Remediation Scaffold Completion Review & Stage 2 Plan

Date prepared: 2026-06-06
Status: scaffold completion review and Stage 2 planning ledger only
Tracking ID: SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001
Owner: Astra Doctrine Council / Runtime Boundary Reviewers

## 1. Purpose and scope

This is a scaffold completion review and second-stage remediation planning ledger only. It verifies owner-scaffold coverage for RT-001 through RT-012, identifies remaining gaps/overlaps/dependency risks, and recommends the next safe PR sequence.

This review does not implement remediation, owner specifications, schemas, command IR, runtime code, validators, generators, persistence writers, context-packet compilers, RNG, inventory systems, asset systems, live-play adapters, training material, donor-content audits, or canon promotion.

This review confirms that all twelve remediation tracks from `REMEDIATION-PRIORITY-LEDGER-001` now have owner-scaffold files in place. It plans Stage 2 (owner-specification PRs) while preserving all non-implementation guardrails from AUDIT-001, AUDIT-WAVE1-001, AUDIT-WAVE2-001, and the remediation priority ledger.

## 2. Inputs reviewed

This review read and used these actual repo files:

### Core audit/remediation inputs
- `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` (AUDIT-001)
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md` (AUDIT-WAVE1-001)
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md` (AUDIT-WAVE2-001)
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` (REMEDIATION-PRIORITY-LEDGER-001)
- `docs/doctrine/astra_doctrine_registry_v0_1.yaml`
- `docs/doctrine/astra_doctrine_roadmap_v0_1.md`
- `docs/decisions/current_decisions_log.md`
- `docs/operations/current_decisions_log_v0_1.md`

### All RT-001 through RT-012 owner scaffolds
- `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md`
- `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md`
- `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md`
- `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md`
- `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md`
- `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md`
- `docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md`
- `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md`
- `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md`
- `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md`
- `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md`
- `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md`

All twelve scaffold files exist and were inspected for this review.

## 3. Scaffold coverage matrix

| track_id | scaffold_file | tracking_id | exists | priority_from_ledger | risk_level_from_ledger | primary_owner_boundary | major_dependencies | major_downstream_consumers | llm_non_authority_coverage | non_implementation_guardrails | registry_tracking | decision_log_tracking | stage2_readiness | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RT-001 | docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md | REMEDIATION-RT001-COMMAND-LIFECYCLE-OWNER-SCAFFOLD-001 | true | P0 | critical | command lifecycle/action legality/cost commitment | RT-011, future command IR owner, future runtime event owner, future cost/resource math owner | RT-002, RT-003, RT-004, RT-005, RT-006, RT-007, RT-009, RT-010 | complete | complete | complete (v0.1.38) | complete (REMEDIATION-PR-A-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | Central runtime seam; all action/command paths depend on this |
| RT-002 | docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md | REMEDIATION-RT002-RESOURCE-CONSEQUENCE-MATH-OWNER-SCAFFOLD-001 | true | P0 | critical | resource/backlash/corruption/strain/consequence math | RT-001, RT-011, SM math/mechanics workstream | RT-003, RT-004, RT-006, RT-010 | complete | complete | complete (v0.1.39) | complete (REMEDIATION-PR-B-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | Cost/consequence math required before abilities, combat, missions, assets |
| RT-003 | docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md | REMEDIATION-RT003-COMBAT-HAZARD-DAMAGE-RECOVERY-OWNER-SCAFFOLD-001 | true | P0 | critical | combat/hazard/damage/injury/recovery | RT-001, RT-002, RT-009 | RT-010 (vehicle damage), RT-006 (mission consequences) | complete | complete | complete (v0.1.39) | complete (REMEDIATION-PR-B-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | Follows RT-001/RT-002; hazard/combat are critical-risk improvisation seams |
| RT-004 | docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md | REMEDIATION-RT004-ABILITY-EFFECT-SKILL-BINDING-OWNER-SCAFFOLD-001 | true | P0 | critical | ability/effect/cost/cooldown/skill synthesis | RT-001, RT-002, RT-008 | RT-006 (mission rewards may grant abilities) | complete | complete | complete (v0.1.42) | complete (REMEDIATION-PR-E-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | Ability generation/use affects persistent player power |
| RT-005 | docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md | REMEDIATION-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SCAFFOLD-001 | true | P0 | high | scene/activity orchestration/hidden-information/context packets | RT-001, RT-007, RT-006 | RT-006, RT-007, RT-009, RT-010 | complete | complete | complete (v0.1.40) | complete (REMEDIATION-PR-C-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | Hidden-state redaction enables later live-play safety |
| RT-006 | docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md | REMEDIATION-RT006-MISSION-REWARD-CLUE-ROUTING-OWNER-SCAFFOLD-001 | true | P1 | critical | mission/reward/clue/hidden-truth/consequence routing | RT-001, RT-002, RT-005, RT-008 | RT-010 (rewards/assets) | complete | complete | complete (v0.1.43) | complete (REMEDIATION-PR-F-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | P1 because it depends on P0 command/cost/context/provenance scaffolds |
| RT-007 | docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md | REMEDIATION-RT007-SOCIAL-FACTION-KNOWLEDGE-STATE-OWNER-SCAFFOLD-001 | true | P1 | critical | social/faction/relationship/actor-knowledge/institutional state | RT-001, RT-005, RT-008 | RT-006 (faction missions) | complete | complete | complete (v0.1.42) | complete (REMEDIATION-PR-E-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | Critical-risk but follows shared context/provenance scaffolds |
| RT-008 | docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md | REMEDIATION-RT008-GENERATED-CONTENT-PROVENANCE-RECURRENCE-OWNER-SCAFFOLD-001 | true | P1 | high | generated-content recurrence/provenance/canon-separation | RT-011, repo canon-promotion gate | RT-004, RT-006, RT-007, RT-010 | complete | complete | complete (v0.1.41) | complete (REMEDIATION-PR-D-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | Must precede any generator template PR |
| RT-009 | docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md | REMEDIATION-RT009-RUNTIME-RNG-TABLE-ORACLE-OWNER-SCAFFOLD-001 | true | P1 | high | runtime RNG/table/oracle ownership | RT-001, RT-005 | RT-003 (hazard triggers), RT-006 (random missions/rewards) | complete | complete | complete (v0.1.43) | complete (REMEDIATION-PR-F-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | P1 because it supports hazards/missions/rewards after command/context boundaries |
| RT-010 | docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md | REMEDIATION-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SCAFFOLD-001 | true | P2 | high | inventory/item/gear/vehicle/persistent asset state | RT-001, RT-002, RT-008 | RT-003 (vehicle damage), RT-006 (mission rewards) | complete | complete | complete (v0.1.44) | complete (REMEDIATION-PR-G-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | P2 because item/vehicle assets depend on command/cost/provenance scaffolds |
| RT-011 | docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md | REMEDIATION-RT011-VALIDATION-READINESS-OWNER-SCAFFOLD-001 | true | P0 | medium | validation/readiness tooling versus prose-only governance | repo no-prose-implies-implementation gate | All other RT tracks (validation discipline) | complete | complete | complete (v0.1.38) | complete (REMEDIATION-PR-A-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | P0 as planning infrastructure; prevents owner files from being mistaken for enforcement |
| RT-012 | docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md | REMEDIATION-RT012-D-SERIES-PROMOTION-BOUNDARY-OWNER-SCAFFOLD-001 | true | P1 | high | D-series/native-design source-material promotion boundary | RT-011, repo D-series-draft-source gate | All tracks consuming D-series design pressure | complete | complete | complete (v0.1.41) | complete (REMEDIATION-PR-D-OWNER-SCAFFOLDS-001) | ready_for_owner_spec | Protects remediation from accidentally importing D-series as runtime authority |

### Coverage summary
- All 12 RT tracks have owner-scaffold files present.
- All scaffolds include explicit non-implementation statements.
- All scaffolds include LLM non-authority rules.
- All scaffolds are tracked in the registry (v0.1.38 through v0.1.44).
- All scaffolds have corresponding decision-log entries.
- All scaffolds are rated `ready_for_owner_spec` for Stage 2.

## 4. Cross-track dependency review

The following dependency order is derived from the actual scaffold files and the remediation priority ledger:

### Foundational dependencies (must come first)

**RT-001 (command lifecycle)** is a dependency for most runtime-facing tracks:
- RT-002, RT-003, RT-004, RT-005, RT-006, RT-007, RT-009, RT-010 all require command lifecycle semantics for action declaration, cost commitment, legality checks, and state-delta commits.
- Without RT-001, nearly every player action would require LLM-owned legality, cost spending, dice/RNG triggers, and state mutation.

**RT-011 (validation/readiness)** is a gating dependency:
- RT-011 provides validation discipline that prevents prose owner files from being mistaken for executable enforcement.
- RT-008 and RT-012 explicitly depend on RT-011 for validation/readiness boundary discipline.
- All other tracks benefit from RT-011's no-implementation assertion patterns.

### Math/consequence dependencies

**RT-002 (resource/consequence math)** is a dependency for combat, abilities, missions, assets, rewards, repairs, and damage:
- RT-003 (combat/hazard) depends on RT-002 for damage severity, mitigation, recovery, and consequence routing.
- RT-004 (ability/effect) depends on RT-002 for cost/cooldown/backlash mechanics.
- RT-006 (mission/reward) depends on RT-002 for reward/consequence deltas.
- RT-010 (inventory/asset) depends on RT-002 for durability, charge, and damage mechanics.

### Hidden-information/context dependencies

**RT-005 (context-packet/hidden-information)** is a dependency for scenes, missions, social/faction state, RNG hidden results, and asset visibility:
- RT-006 (mission routing) depends on RT-005 for clue/hidden-truth partition and context projection.
- RT-007 (social/faction) depends on RT-005 for actor knowledge/belief partitions and hidden agenda redaction.
- RT-009 (RNG/table/oracle) depends on RT-005 for hidden-result redaction.
- RT-010 (inventory/asset) depends on RT-005 for visible equipment state and hidden capacity/modifier facts.

### Generated-content/provenance dependencies

**RT-008 (generated-content provenance/recurrence)** is a dependency for generated content across NPCs, factions, missions, assets, hazards, vehicles, and tables:
- RT-004 (ability/effect) depends on RT-008 for generated ability provenance.
- RT-006 (mission/reward) depends on RT-008 for generated scenario provenance.
- RT-007 (social/faction) depends on RT-008 for faction generated-content provenance.
- RT-010 (inventory/asset) depends on RT-008 for item/vehicle instance provenance.

### RNG/table dependencies

**RT-009 (RNG/table/oracle)** is a dependency for random mission, hazard, loot, oracle, and generated-output pathways:
- RT-003 (combat/hazard) depends on RT-009 for hazard triggers and threat escalation randomness.
- RT-006 (mission/reward) depends on RT-009 for random tables, oracle results, and reward selection.

### Guardrail dependencies

**RT-012 (D-series promotion boundary)** is a continuing guardrail, not an implementation dependency:
- RT-012 protects all tracks from accidentally treating D-series draft source material as current runtime authority.
- RT-012 depends on RT-011 for validation discipline around promotion gates.

### Recommended dependency order for Stage 2

1. RT-001 (command lifecycle) — foundational spine
2. RT-011 (validation/readiness) — gating discipline
3. RT-002 (resource/consequence math) — math foundation
4. RT-005 (context-packet/hidden-information) — hidden-state boundaries
5. RT-009 (RNG/table/oracle) — deterministic randomness
6. RT-008 (generated-content provenance) — recurrence/canon separation
7. RT-003 (combat/hazard/damage/recovery) — consumes RT-001/RT-002/RT-009
8. RT-004 (ability/effect/skill binding) — consumes RT-001/RT-002/RT-008
9. RT-006 (mission/reward/clue routing) — consumes RT-001/RT-002/RT-005/RT-008
10. RT-007 (social/faction/knowledge) — consumes RT-001/RT-005/RT-008
11. RT-010 (inventory/item/vehicle/asset) — consumes RT-001/RT-002/RT-008
12. RT-012 (D-series promotion boundary) — guardrail throughout

## 5. Overlap and conflict review

The following overlapping ownership seams must be preserved in future owner-specification PRs to avoid collapsing critical boundaries:

### RT-001 versus RT-002: command cost commitment versus resource/consequence math
- **Overlap seam**: RT-001 handles cost declaration and commitment; RT-002 handles the math for what those costs mean (resource pools, backlash bands, corruption thresholds).
- **Risk**: Collapsing these would conflate lifecycle protocol with numeric mechanics.
- **Preservation rule**: RT-001 specifies when costs are committed; RT-002 specifies how costs are calculated and what consequences follow.

### RT-002 versus RT-003: consequence math versus combat/hazard damage/recovery
- **Overlap seam**: RT-002 defines general consequence math; RT-003 applies it to combat harm, injury clocks, hazard exposure, and recovery.
- **Risk**: RT-003 might duplicate RT-002's general consequence rules or RT-002 might over-specify combat-specific formulas.
- **Preservation rule**: RT-002 remains abstract across all consequence types; RT-003 specializes for combat/hazard without redefining general cost/backlash mechanics.

### RT-004 versus RT-010: item-granted effects versus item/asset state
- **Overlap seam**: RT-004 handles ability/effect binding; RT-010 handles item instances that may grant effects.
- **Risk**: Item effects could be specified in RT-010 (duplicating RT-004) or RT-004 might assume item ownership.
- **Preservation rule**: RT-004 owns effect taxonomy and binding; RT-010 owns item custody/durability and routes effect resolution to RT-004.

### RT-005 versus RT-007: actor knowledge/relationship state versus context projection/redaction
- **Overlap seam**: RT-005 compiles context packets with visible/hidden partitions; RT-007 stores actor knowledge, beliefs, and relationship state.
- **Risk**: RT-007 might duplicate context-packet logic or RT-005 might over-specify social state storage.
- **Preservation rule**: RT-005 owns packet compilation and redaction rules; RT-007 owns relationship/standing/knowledge state and consumes RT-005 packets for projection.

### RT-006 versus RT-009: mission table dependencies versus RNG/table/oracle authority
- **Overlap seam**: RT-006 uses tables for mission selection, rewards, and clues; RT-009 owns RNG and table invocation.
- **Risk**: RT-006 might implement table rolls or RT-009 might over-specify mission logic.
- **Preservation rule**: RT-009 owns RNG invocation and table weight validation; RT-006 owns mission structure and consumes RT-009 results.

### RT-008 versus RT-012: generated-content persistence versus canon/source-pack promotion
- **Overlap seam**: RT-008 handles generated-record provenance and default non-canon status; RT-012 handles D-series promotion gates.
- **Risk**: RT-008 might define promotion workflows or RT-012 might over-specify generated-content recurrence.
- **Preservation rule**: RT-008 owns generated-content lifecycle and default non-canon posture; RT-012 owns draft-source promotion decisions and escalation triggers.

### RT-010 versus RT-003: vehicle/platform damage versus asset ownership
- **Overlap seam**: RT-010 owns vehicle integrity and damage state; RT-003 owns damage math and recovery clocks.
- **Risk**: RT-010 might duplicate damage formulas or RT-003 might assume vehicle ownership.
- **Preservation rule**: RT-003 owns damage severity and recovery mechanics; RT-010 owns vehicle instance state and consumes RT-003 for damage resolution.

### RT-010 versus RT-006: mission rewards/assets versus inventory/asset persistence
- **Overlap seam**: RT-006 handles reward grants; RT-010 handles inventory persistence and custody.
- **Risk**: RT-006 might implement inventory mutations or RT-010 might duplicate reward logic.
- **Preservation rule**: RT-006 owns reward definition and grant events; RT-010 owns inventory state and consumes RT-006 reward events for custody transfer.

## 6. Remaining gap inventory

This section identifies remaining gaps as planning rows only. No remediation is performed here.

| gap_id | related_tracks | gap_type | problem | why_it_matters | blocked_by | recommended_stage | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GAP-001 | RT-001 | owner_spec_needed | Command lifecycle owner specification defining IR fields, state machine, and handoff contracts | Without owner spec, command lifecycle remains planning-only and cannot guide schema/validator work | RT-011 owner spec, scaffold completeness | STAGE2-A | First priority; all runtime paths consume command lifecycle |
| GAP-002 | RT-011 | owner_spec_needed | Validation/readiness executable tooling specification defining validator families and coverage matrices | Without owner spec, readiness remains prose assertion rather than enforceable gate | Scaffold completeness | STAGE2-B | Gates all later owner specs from being mistaken for enforcement |
| GAP-003 | RT-002 | owner_spec_needed | Resource/consequence math owner specification defining cost/backlash/corruption/strain/consequence families | Without owner spec, cost and consequence mechanics remain undefined for downstream tracks | RT-001 owner spec | STAGE2-C | Required before ability, combat, mission, asset effects |
| GAP-004 | RT-005 | owner_spec_needed | Context-packet/hidden-information owner specification defining visible/hidden/redacted contracts | Without owner spec, hidden-state fairness and live-play safety remain unenforceable | RT-001 owner spec | STAGE2-D | Enables scene, social, mission, RNG hidden-result safety |
| GAP-005 | RT-009 | owner_spec_needed | RNG/table/oracle owner specification defining backend RNG authority and table invocation events | Without owner spec, randomness remains LLM-improvisable | RT-001, RT-005 owner specs | STAGE2-E | Required for hazards, missions, rewards, encounters |
| GAP-006 | RT-008 | owner_spec_needed | Generated-content provenance/recurrence owner specification defining stable IDs, provenance fields, and default non-canon posture | Without owner spec, generated records lack durability and canon-separation | RT-011 owner spec | STAGE2-F | Precedes any generator template work |
| GAP-007 | RT-003 | owner_spec_needed | Combat/hazard/damage/recovery owner specification defining threat detection, exposure, harm, and recovery | Without owner spec, combat/hazard remain critical-risk improvisation seams | RT-001, RT-002, RT-009 owner specs | STAGE2-G | High-risk but follows foundational specs |
| GAP-008 | RT-004 | owner_spec_needed | Ability/effect/skill binding owner specification defining prerequisites, effect taxonomy, and cost/cooldown state | Without owner spec, ability generation/use affects player power without boundaries | RT-001, RT-002, RT-008 owner specs | STAGE2-H | Affects persistent capability |
| GAP-009 | RT-006 | owner_spec_needed | Mission/reward/clue routing owner specification defining objectives, branches, clues, rewards, and consequences | Without owner spec, mission progression lacks backend commitment | RT-001, RT-002, RT-005, RT-008 owner specs | STAGE2-I | Drives campaign progression |
| GAP-010 | RT-007 | owner_spec_needed | Social/faction/actor-knowledge owner specification defining relationship state, standing, and knowledge partitions | Without owner spec, social consequences lack consistency | RT-001, RT-005, RT-008 owner specs | STAGE2-J | Affects faction/institutional memory |
| GAP-011 | RT-010 | owner_spec_needed | Inventory/item/vehicle/asset owner specification defining instance persistence, custody, and effect routing | Without owner spec, assets lack durable state | RT-001, RT-002, RT-008 owner specs | STAGE2-K | Affects player possessions and vehicles |
| GAP-012 | RT-012 | owner_spec_needed | D-series promotion-boundary enforcement specification defining draft-source status and adoption workflow | Without owner spec, D-series material may leak into runtime | RT-011 owner spec | STAGE2-L | Guardrail throughout Stage 2 |
| GAP-013 | All RT tracks | test_needed | No-LLM-authority regression tests across all scaffolds | Without tests, non-authority guardrails are unenforceable | Owner specs | STAGE2-A through STAGE2-L | Each stage needs focused tests |
| GAP-014 | Registry/decision log | decision_needed | Registry/decision-log consistency checks for new owner specs | Without checks, tracking may drift from actual files | Owner specs | Each stage | Ensure registry and decision log stay synchronized |

## 7. Second-stage remediation plan

This section creates a ranked sequence of owner-specification PRs. The order follows the dependency review above and preserves all non-implementation guardrails.

| stage_id | target_tracks | title | why_next | allowed_outputs | must_not_do | dependencies | acceptance_tests_needed | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STAGE2-A | RT-001 | Command lifecycle owner specification | Foundational spine for all runtime action paths; all other tracks consume command lifecycle semantics | Owner specification document defining lifecycle states, legality checks, cost commitment handoff, resolution triggers, state-delta validation expectations, context-packet handoff contracts, narration contracts, and test expectations | Define final IR fields, implement runtime code, create schemas, choose cost math, authorize live play | Scaffold RT001 complete, RT-011 scaffold complete | Owner spec file exists, references RT-001 scaffold, cites AUDIT-001/AUDIT-WAVE1-001/AUDIT-WAVE2-001/LEDGER-001, includes non-implementation statement, includes LLM non-authority rules, includes test expectations | First priority; enables all downstream specs |
| STAGE2-B | RT-011 | Validation/readiness executable-tooling specification | Gating discipline that prevents prose owner files from being mistaken for enforcement; required by RT-008/RT-012 | Owner specification defining validator families, schema coverage matrices, readiness registry expectations, reviewer decision event models, and test expectations | Implement validators, create final JSON schemas, approve pilot conversion, authorize live play | Scaffold RT011 complete, STAGE2-A complete or concurrent | Owner spec file exists, references RT-011 scaffold, includes no-executable-validator assertion, includes readiness-label planning | Enables validation discipline for all later specs |
| STAGE2-C | RT-002 | Resource/consequence math owner specification | Math foundation for cost, backlash, corruption, strain, harm, reward, and consequence across all subsystems | Owner specification defining resource pool families, cost commitment ledgers, backlash/corruption/strain condition families, consequence event models, and test expectations | Set final numeric values, set final damage/backlash formulas, implement state deltas, create schemas | STAGE2-A, STAGE2-B complete | Owner spec file exists, references RT-002 scaffold, includes no-final-formula assertion, includes dependency references for B02/C03/A13/C09/C07 | Required before ability, combat, mission, asset effects |
| STAGE2-D | RT-005 | Context-packet/hidden-information owner specification | Hidden-state boundaries enable scene, social, mission, RNG hidden-result, and asset visibility safety | Owner specification defining visible/hidden/redacted contracts, scene state expectations, participant visibility partitions, context-packet compiler responsibilities, narration downstream contracts, and test expectations | Build context-packet compiler, create scene runtime, create live-play prompts, reveal hidden information rules as final schema | STAGE2-A, STAGE2-B complete | Owner spec file exists, references RT-005 scaffold, includes hidden-state redaction posture, includes no-LLM-scene-state mutation assertion | Enables later live-play safety |
| STAGE2-E | RT-009 | RNG/table/oracle owner specification | Deterministic randomness required for hazards, missions, rewards, encounters, and generated outputs | Owner specification defining backend RNG authority, seeded/replayable invocation events, table weight validation expectations, oracle result domains, hidden-result redaction, and test expectations | Implement RNG, create oracle registry data, create random tables, commit oracle outcomes | STAGE2-A, STAGE2-B, STAGE2-D complete | Owner spec file exists, references RT-009 scaffold, includes no-LLM-oracle-roll assertion, includes RNG owner-boundary assertion | Supports hazards, missions, rewards after command/context boundaries |
| STAGE2-F | RT-008 | Generated-content provenance/recurrence owner specification | Recurrence, provenance, and canon-separation required before any generator template work | Owner specification defining stable ID requirements, provenance field families, source-local status, recurrence expectations, default non-canon posture, canon-promotion separation, and test expectations | Create generator code, create durable generated records, write canon-promotion rules as final workflow, create retrieval indexes | STAGE2-B complete, STAGE2-A complete | Owner spec file exists, references RT-008 scaffold, includes generated-content no-canon-promotion assertion, includes provenance field expectation | Precedes any generator template PR |
| STAGE2-G | RT-003 | Combat/hazard/damage/recovery owner specification | Combat/hazard are critical-risk improvisation seams requiring backend ownership | Owner specification defining threat detection, exposure intervals, damage severity families, mitigation expectations, injury/condition clocks, recovery rules, active-threat queues, event models, context-packet projections, and test expectations | Implement combat runtime, create damage tables, create hazard generators, authorize live encounter play | STAGE2-A, STAGE2-B, STAGE2-C, STAGE2-E complete | Owner spec file exists, references RT-003 scaffold, includes no-LLM-damage-commit assertion, includes hazard exposure owner-boundary | High-risk but follows foundational specs |
| STAGE2-H | RT-004 | Ability/effect/skill binding owner specification | Ability generation/use directly affects persistent player power | Owner specification defining prerequisites, acquisition/mastery expectations, effect taxonomy, cost/cooldown state families, skill synthesis validation, action timing, persistence expectations, and test expectations | Generate abilities or techniques, award skills or mastery, set final progression thresholds, implement use-ability commands | STAGE2-A, STAGE2-B, STAGE2-C, STAGE2-F complete | Owner spec file exists, references RT-004 scaffold, includes no-LLM-ability-invention assertion, includes ability-cost dependency | Affects persistent capability |
| STAGE2-I | RT-006 | Mission/reward/clue routing owner specification | Mission progression drives durable campaign state | Owner specification defining objective structures, branch/clue/reward families, hidden-truth partitions, consequence routing, provenance expectations, context-packet projections, generator template planning, validators, and test expectations | Generate missions, commit rewards, define final clue schema, promote scenario canon | STAGE2-A, STAGE2-B, STAGE2-C, STAGE2-D, STAGE2-F complete | Owner spec file exists, references RT-006 scaffold, includes no-LLM-reward-commit assertion, includes hidden clue redaction posture | Drives campaign progression |
| STAGE2-J | RT-007 | Social/faction/actor-knowledge owner specification | Social consequences and faction memory require consistency | Owner specification defining relationship state, standing deltas, NPC/faction knowledge and belief partitions, institutional actions, faction recurrence, hidden agenda redaction, and test expectations | Implement social commands, create relationship schemas, generate faction actions, promote faction canon | STAGE2-A, STAGE2-B, STAGE2-D, STAGE2-F complete | Owner spec file exists, references RT-007 scaffold, includes no-LLM-relationship-mutation assertion, includes actor knowledge partition posture | Affects faction/institutional memory |
| STAGE2-K | RT-010 | Inventory/item/vehicle/asset owner specification | Assets require durable state for custody, durability, charges, cargo, crew, movement, damage, and repairs | Owner specification defining item instance persistence, equipment/loadout integration, charges/durability/cooldowns, cargo/crew/capacity, vehicle movement/damage/capacity mechanics, effect validation routing, and test expectations | Implement inventory runtime, create item instance schemas, generate items or vehicles, resolve item effects | STAGE2-A, STAGE2-B, STAGE2-C, STAGE2-F complete | Owner spec file exists, references RT-010 scaffold, includes no-LLM-item-effect assertion, includes item instance non-implementation assertion | Affects player possessions and vehicles |
| STAGE2-L | RT-012 | D-series promotion-boundary enforcement specification | Guardrail preventing accidental import of D-series source-pack material as runtime authority | Owner specification defining draft-source status, adoption prerequisites, prohibited uses, escalation triggers, no-direct-generator-use validators, and test expectations | Promote D02 or any D-series material, define final cost commitment math from D02, feed D-series material into generators, create canon or live-play content | STAGE2-B complete, STAGE2-A complete | Owner spec file exists, references RT-012 scaffold, includes D-series draft-source boundary assertion, includes no-direct-generator-use assertion | Guardrail throughout Stage 2 |

## 8. Recommended next PR

Based on the dependency review and scaffold completeness findings, the recommended next PR is:

### STAGE2-A — RT-001 Command Lifecycle Owner Specification

**Title**: RT-001 Command Lifecycle Owner Specification

**Purpose**: Create the owner specification for RT-001 command lifecycle, action legality, and cost commitment. This specification defines lifecycle states, legality checks, cost commitment handoff, resolution triggers, state-delta validation expectations, context-packet handoff contracts, narration contracts, and test expectations without implementing final IR fields, runtime code, schemas, or math.

**Files to read**:
- `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md`
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`
- `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md`
- `docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md`
- `docs/doctrine/schema/C03_ability_power_technique_record_schema.md`
- `docs/doctrine/schema/C10_table_oracle_record_schema.md`

**File to create**:
- `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`

**Allowed scope**:
- Owner specification document defining conceptual lifecycle states (player_intent_received, intent_parsed_or_clarification_needed, candidate_command_proposed, legality_checked_by_backend, costs_declared, costs_committed, resolution_triggered, state_delta_validated, event_committed, narration_packet_prepared, narration_rendered) as planning placeholders only
- Owner boundary definitions separating backend authority from LLM narration/proposal
- Legality check expectations and clarification routing
- Cost declaration and commitment handoff expectations
- Resolution trigger expectations
- State-delta validation expectations
- Context-packet handoff expectations
- Narration contract expectations
- Replay/audit test expectations
- Explicit non-implementation statement
- LLM non-authority rules

**Forbidden scope**:
- Final command IR field definitions
- Final JSON/database/backend schemas
- Executable validators
- Runtime implementation or state-machine code
- Generators or generator prompts
- Persistence writer implementation
- Context-packet compiler implementation
- Final resource/cost math
- Donor-content audit
- D-series promotion
- Live-play authorization
- Training-data authorization
- Canon promotion

**Tests to add**:
- `tests/test_rt001_command_lifecycle_owner_specification.py`
- Tests verifying owner specification file exists
- Tests verifying references to RT-001 scaffold and REMEDIATION-PRIORITY-LEDGER-001
- Tests verifying links to B02/A10/D02/C03/C10 pressure sources
- Tests verifying non-implementation guardrails
- Tests verifying LLM non-authority prohibitions (legality, costs, RNG/dice, hidden modifiers, consequences, state deltas, file writing, canon)

**Acceptance conditions**:
- Owner specification file created at correct path
- File references RT-001 scaffold tracking ID (REMEDIATION-RT001-COMMAND-LIFECYCLE-OWNER-SCAFFOLD-001)
- File references REMEDIATION-PRIORITY-LEDGER-001
- File includes explicit non-implementation statement
- File includes LLM non-authority rules
- File includes test expectations
- Registry updated with new tracking entry
- Decision log updated with STAGE2-A decision entry
- Tests pass verifying file presence and key guardrail phrases

## 9. Registry and decision log updates

### Registry update

Add the following changelog entry to `docs/doctrine/astra_doctrine_registry_v0_1.yaml`:

```yaml
- date: '2026-06-06'
  version: 0.1.45
  action: scaffold_completion_review_stage2_plan
  actor: Astra Doctrine Council / synthesis assistant
  note: Added SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001 tracking for docs/doctrine/reviews/runtime_boundary_remediation_scaffold_completion_review_stage2_plan.md. This record is scaffold completion review and Stage 2 planning only; no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no owner specification implementation, no live-play/training authorization, no donor-content audit, and no canon promotion was performed. All twelve RT-001 through RT-012 owner scaffolds verified present. Stage 2 owner-specification sequence planned.
```

### Decision log update

Add the following entry to `docs/decisions/current_decisions_log.md`:

```markdown
## 2026-06-06 decision log - Scaffold Completion Review and Stage 2 Plan

- Decision ID: SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001
- Decision date: 2026-06-06
- Decision type: scaffold completion review and Stage 2 planning

### Summary
- Added `docs/doctrine/reviews/runtime_boundary_remediation_scaffold_completion_review_stage2_plan.md` as scaffold completion review and Stage 2 planning ledger.
- Verified all twelve RT-001 through RT-012 owner scaffolds are present and complete.
- Identified cross-track dependencies, overlap/conflict seams, and remaining gaps.
- Planned Stage 2 owner-specification sequence (STAGE2-A through STAGE2-L).
- Recommended STAGE2-A (RT-001 command lifecycle owner specification) as next PR.

### Governance effect
- Confirms scaffold phase complete; transitions to owner-specification phase.
- Keeps Stage 2 planning separate from implementation; each stage requires separate PR.
- Preserves all non-implementation guardrails from AUDIT-001, AUDIT-WAVE1-001, AUDIT-WAVE2-001, and REMEDIATION-PRIORITY-LEDGER-001.

### Guardrails reaffirmed
- Scaffold completion review and Stage 2 planning only.
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No math implementation.
- No validator implementation.
- No generator implementation.
- No persistence writer implementation.
- No retrieval index implementation.
- No context-packet compiler implementation.
- No owner specification implementation.
- No live-play/training authorization.
- No donor-content audit.
- No canon promotion.
- Future owner specifications require separate PRs.
```

## 10. Explicit non-implementation statement

This scaffold completion review and Stage 2 plan is documentation/control planning only. It implements no owner specifications, no schemas, no command IR, no runtime code, no validators, no generators, no persistence writers, no retrieval indexes, no context-packet compilers, no live-play adapters, no training data, no donor-content audits, and no canon promotion.

All twelve RT-001 through RT-012 owner scaffolds are verified present. Stage 2 owner-specification sequence is planned. Each stage requires separate PR approval.
