# RT-003 Combat / Hazard / Damage / Recovery Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification only
Tracking ID: REMEDIATION-STAGE2-RT003-COMBAT-HAZARD-DAMAGE-RECOVERY-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-G1
Parent Stage 2 PR ID: STAGE2-PR-G
Remediation track: RT-003-combat-hazard-damage-recovery
Owner: Astra Doctrine Council / future combat, hazard, damage, injury, recovery, mitigation, exposure, and active-threat boundary owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-003. It upgrades `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md` into a specification-level planning artifact for combat/hazard/damage/recovery ownership boundaries, active-threat and hazard-contact boundary requirements, damage-family and injury-family requirement boundaries, recovery/mitigation/exposure/ongoing-harm requirement boundaries, combat/hazard consequence handoff requirements, encounter-state pressure boundaries, and downstream owner handoffs.

This specification remains non-executable and non-implementation. It defines planning-level ownership seams, future semantic requirements, authority boundaries, handoff obligations, validation/readiness expectations, and LLM non-authority rules only. It does not authorize combat rules, hazard rules, damage formulas, injury tables, condition system implementation, healing/recovery formulas, mitigation math, exposure clocks, active-threat runtime, initiative/action economy, encounter runtime, vehicle/platform damage system implementation, item durability system implementation, armor/resistance/soak rules, death/dying rules, monster/NPC combat schema implementation, hazard schema implementation, schema implementation, command IR implementation, runtime code, validator implementation, generator implementation, RNG/dice/table implementation, event ledger implementation, persistence writer implementation, retrieval index implementation, context-packet compiler implementation, live-play prompt implementation, training authorization, donor-content audit, sourcebook inclusion authorization, pilot conversion authorization, or canon promotion.

This specification links to and relies on the following actual repo artifacts:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- RT003 owner scaffold: `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md`.
- RT001 owner specification: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- RT002 owner specification: `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`.
- RT005 owner specification: `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md`.
- RT008 owner specification: `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md`.
- RT009 owner specification: `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md`.
- RT011 owner specification: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.

### Source availability disclosure

This Stage 2 PR-G1 pass used actual repo files only. All requested planning and audit sources, current RT owner files, combat/hazard/source pressure files, schema/math/readiness files, and `README.md` were present at drafting time. The following source-pressure files were confirmed present and consulted: `docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md`, `docs/doctrine/operations/batch_b/B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md`, `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md`, `docs/doctrine/schema/C01_creature_npc_record_schema.md`, `docs/doctrine/schema/C02_item_gear_record_schema.md`, `docs/doctrine/schema/C03_ability_power_technique_record_schema.md`, `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md`, `docs/doctrine/schema/C09_hazard_environment_record_schema.md`, `docs/doctrine/schema/C10_table_oracle_record_schema.md`, `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md`, `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`, `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`, `docs/doctrine/astra_doctrine_roadmap_v0_1.md`, `docs/doctrine/astra_doctrine_registry_v0_1.yaml`, `docs/decisions/current_decisions_log.md`, and `README.md`. No requested source path was absent. This specification does not rewrite A13, B10, B02, C01, C02, C03, C08, C09, C10, SM00, SM01, SM02, the RT scaffolds, RT001 owner specification, RT002 owner specification, RT005 owner specification, RT008 owner specification, RT009 owner specification, RT011 owner specification, or source doctrine.

## 2. Scope

RT-003 owns planning-level governance for combat/hazard/damage/recovery ownership boundaries. Ownership means defining future semantic requirements for how combat resolution, active-threat contact, hazard contact, damage families, injury families, recovery, mitigation, exposure, ongoing harm, encounter-state pressure, and consequence events must remain backend-owned, validated, auditable, and commitment-bounded. Ownership does not mean implementing combat rules, hazard rules, damage formulas, injury tables, condition systems, healing/recovery formulas, mitigation math, exposure clocks, active-threat runtime, initiative/action economy, encounter runtime, vehicle/platform damage systems, item durability systems, armor/resistance/soak rules, death/dying rules, monster/NPC combat schemas, hazard schemas, schemas, command IR, validators, generators, persistence writers, retrieval indexes, context-packet compilers, event ledgers, database schemas, or runtime code.

RT-003 owns the following planning boundaries:

- combat/hazard/damage/recovery ownership boundaries;
- active-threat and hazard-contact boundary requirements;
- damage-family and injury-family requirement boundaries;
- recovery, mitigation, exposure, and ongoing-harm requirement boundaries;
- combat/hazard consequence handoff requirements;
- encounter-state pressure boundaries without implementing encounter runtime;
- combat/hazard visibility handoff to RT-005;
- cost/consequence math handoff to RT-002;
- action legality and command/event timing handoff to RT-001;
- generated hazard/threat provenance handoff to RT-008;
- random hazard/combat/table/oracle dependency handoff to RT-009;
- item/vehicle/platform damage and repair handoff to RT-010;
- ability/effect/skill handoff to RT-004;
- mission/scenario consequence handoff to RT-006;
- social/faction consequence handoff to RT-007;
- validation/readiness handoff to RT-011;
- D-series/native-design pressure handoff to RT-012;
- auditability requirements.

RT-003 preserves the audit waves' pressure that combat, hazard, damage, injury, recovery, mitigation, exposure, active-threat, encounter-state, vehicle/platform damage, item durability, and consequence events need backend-owned authority before later owners consume them. It also preserves the README's backend-first/model-interchangeability posture: model output may be useful narration, but no LLM is the holder of combat resolution, hazard contact, damage application, injury assignment, recovery commitment, mitigation selection, exposure timing, active-threat mutation, or consequence event authority.

## 3. Must-not-own boundaries

RT-003 must not own, create, imply, or claim completion of:

- final combat rules;
- final hazard rules;
- final damage formulas;
- final injury tables;
- final condition system;
- final healing/recovery formulas;
- final mitigation math;
- final exposure clocks;
- final active-threat runtime;
- final initiative/action economy;
- final encounter runtime;
- final vehicle/platform damage system;
- final item durability system;
- final armor/resistance/soak rules;
- final death/dying rules;
- final monster/NPC combat schema;
- final hazard schema;
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

RT-003 also must not decide final schemas for A13, B10, B02, C01, C02, C03, C08, C09, or C10. It defines combat/hazard/damage/recovery authority, active-threat, hazard-contact, damage-family, injury-family, recovery, mitigation, exposure, ongoing-harm, encounter-state, consequence, and narration projection requirements that future combat systems, hazard systems, validators, persistence owners, and runtime code must obey if separately authorized.

## 4. Authority model

The RT-003 authority model is deliberately split across owners:

- RT-001 owns command/action timing, legality, resolution-trigger handoff, rejection/quarantine, and event-commit boundaries;
- RT-002 owns resource, cost, damage-as-resource-pressure, recovery cost, mitigation cost, consequence math, reward/loss pressure, and failed-command cost outcomes;
- RT-005 owns hidden/visible hazard, threat, damage, consequence, and recovery visibility;
- RT-009 owns RNG/table/oracle dependency authority for random damage, random hazards, random encounters, random exposure, and random recovery outcomes;
- RT-011 owns validation/readiness requirements;
- future backend runtime must own combat/hazard resolution, state deltas, event commits, and persistence if separately authorized;
- the LLM may only narrate backend-approved visible outcomes and may not resolve combat, apply damage, reveal hidden hazards, or commit recovery.

RT-004 owns ability/effect/skill binding when combat or hazard events involve capabilities, prerequisites, cooldowns, techniques, defensive effects, damage-causing effects, healing effects, resistance/vulnerability effects, or mitigation effects. RT-006 owns mission/reward/clue routing when combat or hazard events produce mission consequences, objective pressure, reward/penalty outcomes, clue-risk outcomes, or scenario failure. RT-007 owns social/faction/actor-knowledge when combat or hazard events produce reputation changes, faction standing shifts, institutional responses, witness state, or actor knowledge. RT-008 owns generated-content provenance/recurrence when combat or hazard events involve generated hazards, generated threats, generated creatures, or generated environmental dangers. RT-010 owns inventory/item/vehicle/asset when combat or hazard events involve item damage, vehicle/platform damage, armor, weapon, durability, repair, salvage, fuel, ammo, or cargo pressure. RT-012 owns D-series/native-design promotion boundaries when source-pack material proposes combat, hazard, damage, or recovery patterns that cannot become runtime/canon/sourcebook authority without promotion.

## 5. Combat/hazard state-pressure contract

The following combat/hazard state-pressure terms are conceptual pressure states as planning placeholders only. They are not final schemas, not database fields, not combat rules, not damage formulas, not injury tables, not conditions, not encounter runtime, not event records, not validators, not runtime state, and not live-play prompts.

| Conceptual pressure placeholder | Planning meaning | Boundary note |
|---|---|---|
| `combat_resolution_required` | A combat action, attack, defense, or opposed check requires backend-owned resolution before outcome commitment. | No LLM resolving combat. Backend must own resolution. |
| `active_threat_contact_pending` | An active threat has been identified or contacted but resolution has not occurred. | No active-threat runtime implementation. Contact identification only. |
| `hazard_contact_pending` | A hazard contact, exposure, or environmental danger has been identified but resolution has not occurred. | No hazard runtime implementation. Contact identification only. |
| `damage_family_required` | A damage event requires classification into a damage family before application. | No damage formulas. Family classification requirement only. |
| `injury_family_required` | An injury event requires classification into an injury family before application. | No injury tables. Family classification requirement only. |
| `mitigation_requirement_pending` | A mitigation opportunity (armor, resistance, soak, cover, shield, evasion) requires backend-owned resolution. | No mitigation math. Requirement identification only. |
| `recovery_requirement_pending` | A recovery opportunity (healing, rest, repair, clearing, stabilization) requires backend-owned resolution. | No recovery formulas. Requirement identification only. |
| `exposure_tick_pending` | An exposure interval (poison, radiation, environmental, ongoing effect) requires backend-owned tick/clock resolution. | No exposure clocks. Tick requirement only. |
| `ongoing_harm_pending` | An ongoing harm effect (bleed, burn, drain, corruption, decay) requires backend-owned persistence and resolution. | No condition system. Ongoing-harm requirement only. |
| `resistance_or_vulnerability_dependency` | A damage or hazard event requires resistance/vulnerability lookup before outcome determination. | No armor/resistance/soak rules. Dependency identification only. |
| `armor_or_soak_dependency` | A damage event requires armor/soak/protection lookup before outcome determination. | No armor/resistance/soak rules. Dependency identification only. |
| `condition_dependency_pending` | A combat or hazard outcome may produce, modify, or clear a condition that requires backend-owned state. | No condition system. Dependency identification only. |
| `vehicle_or_asset_damage_dependency` | A combat or hazard event involves vehicle, platform, item, or asset damage that requires RT-010 handoff. | No vehicle/platform damage system. Handoff requirement only. |
| `hidden_hazard_visibility_required` | A hazard, threat, or damage consequence has hidden components that must route through RT-005 before projection. | No hidden-state implementation. Routing requirement only. |
| `random_damage_or_hazard_dependency` | A combat, hazard, damage, or recovery outcome requires RT-009 backend-owned random authority. | No RNG implementation. Dependency identification only. |
| `consequence_event_pending` | A combat or hazard outcome produces a consequence event that requires backend-owned commitment. | No event ledger implementation. Consequence requirement only. |
| `encounter_state_quarantined` | An encounter state cannot be resolved because doctrine, runtime, validation, or owner boundaries are missing. | No encounter runtime. Quarantine is non-mutating. |

These planning placeholders are not final schemas, not database fields, not combat rules, not damage formulas, not injury tables, not conditions, not encounter runtime, not event records, not validators, not runtime state, and not live-play prompts. A future implementation may rename, split, combine, or replace these placeholders, but it must preserve the backend-owned combat/hazard/damage/recovery authority, active-threat boundaries, hazard-contact boundaries, damage-family requirements, injury-family requirements, recovery/mitigation/exposure boundaries, consequence commitment boundaries, and narration projection semantics described here.

## 6. Damage, injury, recovery, and mitigation contract

The RT-003 damage/injury/recovery/mitigation contract is planning-level only:

- damage-family labels are not formulas;
- injury-family labels are not injury tables;
- recovery requirements are not healing formulas;
- mitigation requirements are not armor/resistance/soak rules;
- persistent harm requires future state/event/persistence ownership;
- hidden harm or hidden hazard information must route through RT-005;
- cost-bearing damage/recovery/mitigation must route through RT-002;
- random damage/hazard/recovery requires RT-009;
- generated hazards or threats require RT-008 provenance;
- item/vehicle/platform damage or repair requires RT-010;
- abilities/effects that cause or prevent damage require RT-004;
- mission/scenario consequences require RT-006;
- social/faction consequences require RT-007;
- validation/readiness requires RT-011.

This contract does not define final damage formulas, injury tables, recovery formulas, mitigation math, condition durations, or clearing rules. Damage-family labels (such as physical, elemental, spiritual, dimensional, psychic, corruption, or environmental) are planning vocabulary only and are not final damage types, not schema fields, not database columns, and not runtime enums. Injury-family labels (such as wound, fracture, burn, drain, corruption, madness, or transformation) are planning vocabulary only and are not final injury types, not condition system entries, not database records, and not runtime state. Recovery and mitigation labels are planning vocabulary only and are not final healing spells, rest mechanics, armor values, or soak formulas.

## 7. Combat/hazard commitment contract

The RT-003 combat/hazard commitment contract is planning-level only:

- combat/hazard contact is not resolution;
- damage declaration is not damage commitment;
- mitigation declaration is not mitigation commitment;
- recovery declaration is not recovery commitment;
- random damage or hazard dependency is not random outcome selection;
- narration is not event commitment;
- rejected/quarantined combat or hazard actions must not mutate state;
- event/state/persistence commitment requires future separately authorized backend systems.

Combat or hazard outcomes that affect resources, costs, rewards, losses, or consequence math must route to RT-002 before commitment. Combat or hazard outcomes that involve random authority must route to RT-009 before outcome selection. Combat or hazard outcomes that involve hidden state must route to RT-005 before projection. Combat or hazard outcomes that produce generated content must route to RT-008 for provenance. Combat or hazard outcomes that affect items, vehicles, platforms, or assets must route to RT-010 before commitment. Combat or hazard outcomes that produce mission consequences must route to RT-006. Combat or hazard outcomes that produce social/faction consequences must route to RT-007. Combat or hazard outcomes that involve abilities, effects, or skills must route to RT-004. Validation and readiness routes through RT-011.

This contract does not define final event schemas, runtime state machines, combat resolution algorithms, hazard resolution algorithms, damage application protocols, injury assignment protocols, recovery protocols, mitigation protocols, encounter state machines, or persistence writer behavior.

## 8. Future combat/hazard artifact inventory

The following future combat/hazard artifact families are semantic requirements only. They are not implemented schemas, not records, not validators, not services, not final fields, not formulas, not JSON schema, not database schema, not Pydantic models, not validator code, not RNG code, not combat code, not hazard code, not event code, not persistence code, not retrieval code, not context-packet compiler code, and not runtime code. Every listed family has implementation status `future_required_not_implemented`.

| Future artifact family | Purpose | Owner | LLM allowed interaction | Downstream handoff | Implementation status |
|---|---|---|---|---|---|
| `CombatResolutionRequirement` | Define future requirements for backend-owned combat resolution authority over all combat actions, attacks, defenses, and opposed checks. | RT-003 with RT-001 command lifecycle. | No combat resolution authority; may not resolve attacks, defenses, or opposed checks. | RT-001 for command lifecycle; backend runtime for resolution. | `future_required_not_implemented` |
| `HazardContactRequirement` | Define future requirements for backend-owned hazard contact, exposure, and environmental danger identification and resolution. | RT-003 with RT-001 command lifecycle. | No hazard contact authority; may describe visible hazard status after backend packet. | RT-001 for command lifecycle; RT-005 for hidden hazards; RT-009 for random hazards. | `future_required_not_implemented` |
| `ActiveThreatRequirement` | Define future requirements for backend-owned active-threat detection, tracking, escalation, and de-escalation. | RT-003 with RT-005 hidden-state owner. | No active-threat authority; may not detect, escalate, or de-escalate threats. | RT-005 for hidden threats; RT-001 for event commitment. | `future_required_not_implemented` |
| `DamageFamilyRequirement` | Define future requirements for damage-family classification, routing, and backend-owned application. | RT-003 with RT-002 resource/consequence math. | No damage authority; may not apply, calculate, or invent damage. | RT-002 for cost/consequence math; RT-010 for item/vehicle damage. | `future_required_not_implemented` |
| `InjuryFamilyRequirement` | Define future requirements for injury-family classification, severity, duration, and backend-owned assignment. | RT-003 with future condition/state owner. | No injury authority; may not assign, clear, or invent injuries. | RT-002 for recovery costs; RT-011 for validation. | `future_required_not_implemented` |
| `MitigationRequirement` | Define future requirements for mitigation (armor, resistance, soak, cover, shield, evasion) backend-owned resolution. | RT-003 with RT-002 cost/consequence math. | No mitigation authority; may not apply armor, resistance, or soak values. | RT-002 for mitigation costs; RT-010 for equipment/armor state. | `future_required_not_implemented` |
| `RecoveryRequirement` | Define future requirements for recovery (healing, rest, repair, clearing, stabilization) backend-owned resolution. | RT-003 with RT-002 recovery cost math. | No recovery authority; may not heal, clear injuries, or commit recovery. | RT-002 for recovery costs; RT-011 for validation. | `future_required_not_implemented` |
| `ExposureRequirement` | Define future requirements for exposure intervals (poison, radiation, environmental, ongoing effects) backend-owned tick/clock resolution. | RT-003 with future state/event owner. | No exposure authority; may not tick clocks, advance intervals, or determine exposure outcomes. | RT-001 for event timing; RT-009 for random exposure. | `future_required_not_implemented` |
| `OngoingHarmRequirement` | Define future requirements for ongoing harm (bleed, burn, drain, corruption, decay) backend-owned persistence and resolution. | RT-003 with future state/persistence owner. | No ongoing-harm authority; may not apply, tick, clear, or invent ongoing harm. | RT-002 for harm costs; future persistence owner. | `future_required_not_implemented` |
| `ResistanceVulnerabilityRequirement` | Define future requirements for resistance/vulnerability lookup and backend-owned application to damage/hazard outcomes. | RT-003 with RT-004 ability/effect binding. | No resistance/vulnerability authority; may not apply or invent resistances or vulnerabilities. | RT-004 for ability-granted resistances; RT-010 for equipment-granted resistances. | `future_required_not_implemented` |
| `ArmorSoakRequirement` | Define future requirements for armor/soak/protection lookup and backend-owned damage reduction. | RT-003 with RT-010 inventory/item/vehicle owner. | No armor/soak authority; may not apply or calculate damage reduction. | RT-010 for armor/equipment state; RT-002 for math. | `future_required_not_implemented` |
| `ConditionDependencyRequirement` | Define future requirements for condition production, modification, clearing, stacking, and backend-owned state management. | RT-003 with future condition/state owner. | No condition authority; may not apply, clear, stack, or invent conditions. | RT-004 for ability-caused conditions; RT-011 for validation. | `future_required_not_implemented` |
| `VehicleAssetDamageRequirement` | Define future requirements for vehicle, platform, item, and asset damage routing through RT-010. | RT-003 with RT-010 inventory/item/vehicle owner. | No vehicle/asset damage authority; may not apply or invent vehicle/asset damage. | RT-010 for vehicle/asset state; RT-002 for repair costs. | `future_required_not_implemented` |
| `HiddenHazardVisibilityRequirement` | Define future requirements for hidden hazard, threat, damage, and consequence information routing through RT-005 before any projection. | RT-003 with RT-005 context-packet/hidden-information owner. | No hidden-hazard authority; may not reveal hidden hazards or hidden damage. | RT-005 for redaction and context-packet projection. | `future_required_not_implemented` |
| `RandomDamageHazardRequirement` | Define future requirements for random damage, random hazards, random encounters, random exposure, and random recovery outcomes through RT-009. | RT-003 with RT-009 RNG/table/oracle owner. | No random authority; may not roll, choose, or infer random combat/hazard outcomes. | RT-009 for random authority; RT-001 for event commitment. | `future_required_not_implemented` |
| `ConsequenceEventRequirement` | Define future requirements for combat/hazard consequence events requiring backend-owned commitment. | RT-003 with RT-001 event commitment. | No consequence authority; may not commit consequence events. | RT-001 for event commitment; RT-002 for consequence math; RT-006 for mission consequences. | `future_required_not_implemented` |
| `CombatHazardValidationRequirement` | Define future requirements for combat/hazard owner-boundary, damage-family, injury-family, recovery/mitigation coverage, hidden-hazard routing, random-dependency routing, and LLM non-authority validation. | RT-011 validation/readiness owner with RT-003 requirements. | May draft validation checklists but may not run nonexistent validators. | RT-011 and future validator implementation if separately authorized. | `future_required_not_implemented` |

## 9. Validation and readiness requirements

RT-003 validation and readiness requirements are future requirements only. They coordinate with RT-011 and do not implement validators, test fixtures, CI jobs, schemas, databases, combat systems, hazard systems, damage formulas, injury tables, condition systems, recovery formulas, encounter runtime, context-packet compilers, or runtime code.

Future validation/readiness coverage must include:

- source linkage validation;
- combat/hazard owner-boundary validation;
- damage-family coverage validation;
- injury-family coverage validation;
- recovery/mitigation coverage validation;
- hidden-hazard routing validation;
- random-dependency routing validation;
- cost/consequence handoff validation;
- generated-hazard provenance validation;
- item/vehicle/platform damage handoff validation;
- command/event boundary validation;
- LLM non-authority validation;
- non-implementation guardrail validation.

RT-011 owns validation/readiness governance for these requirements. RT-003 supplies the combat/hazard/damage/recovery authority, active-threat, hazard-contact, damage-family, injury-family, recovery/mitigation/exposure, consequence commitment, and narration projection semantics that future RT-011 validators or reviewer checklists would need if separately authorized.

## 10. Downstream handoffs

RT-003 handoffs must remain explicit and auditable:

- RT-001 for command lifecycle, action legality, resolution trigger, rejection/quarantine, and event/state commitment boundaries;
- RT-002 for resource costs, damage pressure, recovery costs, mitigation costs, backlash/strain/corruption/consequence pressure, reward/loss pressure, and failed-command cost outcomes;
- RT-004 for abilities, effects, techniques, skills, prerequisites, cooldowns, defensive effects, damage-causing effects, healing effects, resistance/vulnerability effects, and mitigation effects;
- RT-005 for hidden/visible hazards, hidden threat state, hidden damage information, redacted consequences, context-packet projection, and narrator fact-set limits;
- RT-006 for mission/scenario hazard consequences, objective pressure, reward/penalty consequences, clue-risk consequences, and scenario failure outcomes;
- RT-007 for social/faction consequences from combat or hazards, reputation pressure, institutional response, witness state, and actor knowledge;
- RT-008 for generated hazards, threats, creatures, environmental dangers, generated encounter pressure, source-local danger, and recurrence/provenance;
- RT-009 for random damage, random hazards, random encounter pressure, random exposure, random injury/recovery outcomes, and table/oracle dependencies;
- RT-010 for item, gear, vehicle, platform, cargo, armor, weapon, durability, repair, salvage, fuel, ammo, and asset damage pressure;
- RT-011 for validation/readiness governance;
- RT-012 for D-series/native-design combat, hazard, damage, or recovery patterns that cannot become runtime/canon/sourcebook authority without promotion.

Downstream consumers must not treat RT-003 planning language as combat rules, hazard rules, damage formulas, injury tables, condition systems, recovery formulas, mitigation math, exposure clocks, encounter runtime, vehicle/platform damage systems, item durability systems, armor/resistance/soak rules, death/dying rules, persistence authorization, sourcebook authorization, or canon. They must preserve backend-owned combat/hazard/damage/recovery authority, active-threat boundaries, hazard-contact boundaries, damage-family requirements, injury-family requirements, recovery/mitigation/exposure boundaries, consequence commitment boundaries, and narration projection limits in their future owner specifications.

## 11. LLM non-authority rules

The LLM is explicitly prohibited from:

- resolving combat;
- deciding hazard contact;
- applying damage;
- assigning injuries;
- clearing injuries;
- healing characters;
- choosing mitigation outcomes;
- applying resistance, vulnerability, armor, or soak as mechanical truth;
- applying conditions as mechanical truth;
- ticking exposure clocks;
- mutating active threat state;
- selecting random damage or hazard results;
- revealing hidden hazards;
- deciding hidden damage or hidden consequences;
- mutating item, vehicle, or platform damage state;
- committing recovery;
- committing consequence events;
- treating combat narration as event commitment;
- inventing formulas, tables, thresholds, or state fields;
- bypassing RT-001, RT-002, RT-005, RT-009, or RT-011;
- authorizing canon/sourcebook/training/live-play use.

The LLM may describe backend-approved visible combat and hazard outcomes only when bounded context allows it and may narrate visible outcomes within backend-provided packets or clearly labeled non-authoritative contexts. Such interaction remains advisory and may not become combat resolution, hazard resolution, damage application, injury assignment, recovery commitment, mitigation selection, exposure timing, active-threat mutation, consequence commitment, persistence, sourcebook material, or canon.

## 12. Non-implementation reaffirmation

This PR adds no:

- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- generator implementation;
- combat rules;
- hazard rules;
- damage formulas;
- injury tables;
- condition system;
- healing/recovery formulas;
- mitigation math;
- exposure clocks;
- active-threat runtime;
- initiative/action economy;
- encounter runtime;
- vehicle/platform damage system;
- item durability system;
- armor/resistance/soak rules;
- death/dying rules;
- monster/NPC combat schema;
- hazard schema;
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

This specification is Stage 2 owner-specification planning only. It cannot be used as runtime readiness, schema readiness, validator readiness, combat readiness, hazard readiness, damage readiness, injury readiness, condition readiness, recovery readiness, mitigation readiness, exposure readiness, encounter readiness, vehicle/platform damage readiness, item durability readiness, armor/resistance/soak readiness, death/dying readiness, generated-record authorization, durable-record authorization, sourcebook authorization, pilot-conversion authorization, live-play authorization, training authorization, donor-content audit, or canon-promotion evidence.

## 13. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-G1
  parent_stage2_pr_id: STAGE2-PR-G
  track: RT-003
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_validator_implementation: false
  authorizes_generator_implementation: false
  authorizes_combat_rules: false
  authorizes_hazard_rules: false
  authorizes_damage_formulas: false
  authorizes_injury_tables: false
  authorizes_condition_system: false
  authorizes_recovery_formulas: false
  authorizes_encounter_runtime: false
  authorizes_rng_implementation: false
  authorizes_event_ledger: false
  authorizes_context_packet_compiler: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  authorizes_pilot_conversion: false
  next_allowed_step: RT-004 owner specification, pending review
```
