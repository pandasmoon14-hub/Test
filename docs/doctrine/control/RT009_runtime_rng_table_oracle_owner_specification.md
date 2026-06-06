# RT-009 Runtime RNG / Table / Oracle Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification only
Tracking ID: REMEDIATION-STAGE2-RT009-RNG-TABLE-ORACLE-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-F
Remediation track: RT-009-runtime-rng-table-oracle
Owner: Astra Doctrine Council / future runtime RNG, table, oracle, seed, replay, and hidden-result boundary owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-009. It upgrades `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md` into a specification-level planning artifact for backend-owned random authority, table/oracle invocation ownership, seed/replay reference requirements, result-domain validation, table-weight validation, hidden-result redaction handoffs, random-result commitment boundaries, oracle/table outcome narration projection, random dependency disclosure, and downstream owner obligations.

This specification remains non-executable and non-implementation. It defines planning-level ownership seams, future semantic requirements, authority boundaries, handoff obligations, validation/readiness expectations, and LLM non-authority rules only. It does not authorize RNG implementation, dice roller implementation, table roller implementation, oracle engine implementation, table data creation, table schema implementation, result-domain schema implementation, seed service implementation, replay verifier implementation, table-weight validator implementation, random-result event schema implementation, command IR implementation, runtime code, validator implementation, generator implementation, persistence writer implementation, retrieval index implementation, context-packet compiler implementation, redaction algorithm implementation, event ledger implementation, database schema, live-play prompt implementation, training authorization, donor-content audit, sourcebook inclusion authorization, pilot conversion authorization, or canon promotion.

This specification links to and relies on the following actual repo artifacts:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- RT009 owner scaffold: `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md`.
- RT001 owner specification: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- RT005 owner specification: `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md`.
- RT008 owner specification: `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md`.
- RT011 owner specification: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.

### Source availability disclosure

This Stage 2 PR-F pass used actual repo files only. All requested planning and audit sources, current RT owner files, RNG/table/oracle/source pressure files, schema/math/readiness files, and `README.md` were present at drafting time. The following source-pressure files were confirmed present and consulted: `docs/doctrine/schema/C10_table_oracle_record_schema.md`, `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`, `docs/doctrine/schema/C09_hazard_environment_record_schema.md`, `docs/doctrine/schema/C02_item_gear_record_schema.md`, `docs/doctrine/schema/C03_ability_power_technique_record_schema.md`, `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md`, `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md`, `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md`, `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`, `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`, `docs/doctrine/astra_doctrine_roadmap_v0_1.md`, `docs/doctrine/astra_doctrine_registry_v0_1.yaml`, `docs/decisions/current_decisions_log.md`, and `README.md`. No requested source path was absent. This specification does not rewrite C10, C07, C09, C02, C03, C08, C12, SM00, SM01, SM02, the RT scaffolds, RT001 owner specification, RT002 owner specification, RT005 owner specification, RT008 owner specification, RT011 owner specification, or source doctrine.

## 2. Scope

RT-009 owns planning-level governance for backend-owned random authority and table/oracle invocation ownership boundaries. Ownership means defining future semantic requirements for how random outcomes must remain backend-owned, deterministic, seedable/replayable, auditable, table/oracle-record-referenced, result-domain-validated, weight-validated, hidden-result-redacted, and commitment-bounded. Ownership does not mean implementing RNG, dice rollers, table rollers, oracle engines, table data, table schemas, result-domain schemas, seed services, replay verifiers, table-weight validators, random-result event schemas, validators, generators, persistence writers, retrieval indexes, context-packet compilers, redaction algorithms, event ledgers, database schemas, or runtime code.

RT-009 owns the following planning boundaries:

- backend-owned random authority boundary requirements;
- RNG/table/oracle invocation ownership boundaries;
- table/oracle record reference requirements;
- seed reference and replay reference requirement boundaries;
- result-domain validation requirements;
- table-weight validation requirements;
- hidden-result redaction handoff requirements;
- random-result commitment boundaries;
- oracle/table outcome narration projection requirements;
- random dependency disclosure requirements;
- generated-content random dependency handoff to RT-008;
- mission/reward/clue random dependency handoff to RT-006;
- combat/hazard/damage random dependency handoff to RT-003;
- resource/reward/loss random dependency handoff to RT-002;
- inventory/loot/item/asset random dependency handoff to RT-010;
- context-packet and hidden-result projection handoff to RT-005;
- validation/readiness handoff to RT-011;
- auditability requirements.

RT-009 preserves the audit waves' pressure that table/oracle records, random hazards, random missions, random loot, random encounters, random generation dependencies, hidden random results, and replay/seed requirements need backend-owned random authority before later owners consume them. It also preserves the README's backend-first/model-interchangeability posture: model output may be useful narration, but no LLM is the holder of random authority, table outcomes, oracle results, seed handling, replay references, or result commitment.

## 3. Must-not-own boundaries

RT-009 must not own, create, imply, or claim completion of:

- RNG implementation;
- dice roller implementation;
- table roller implementation;
- oracle engine implementation;
- final table/oracle schemas;
- table data creation;
- result-domain schema implementation;
- seed service;
- replay verifier;
- table-weight validator;
- random-result event schema;
- command IR implementation;
- runtime code;
- validator implementation;
- generator implementation;
- persistence writer implementation;
- retrieval index implementation;
- context-packet compiler implementation;
- redaction algorithm implementation;
- event ledger implementation;
- database schema;
- live-play prompt implementation;
- training data;
- donor-content audits;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion.

RT-009 also must not decide final schemas for C10, C07, C09, C02, C03, C08, or C12. It defines random authority, invocation, seed/replay, result-domain, table-weight, hidden-result, commitment, and narration projection requirements that future RNG systems, table rollers, oracle engines, validators, persistence owners, and runtime code must obey if separately authorized.

## 4. Authority model

The RT-009 authority model is deliberately split across owners:

- RT-001 owns command/event lifecycle and when an RNG/table/oracle dependency may be invoked, rejected, quarantined, or committed;
- RT-005 owns hidden-result visibility, redaction, and context/narration projection;
- RT-008 owns generated-content provenance/recurrence implications when RNG/table/oracle output contributes to generated content;
- RT-011 owns validation/readiness requirements;
- backend runtime, once separately implemented, must own all random authority, seed handling, replay references, outcome selection, result commitment, and audit trails;
- the LLM may describe backend-selected visible results only and may not roll, choose, infer, or commit random outcomes.

RT-002 owns resource/consequence math when random outcomes produce costs, rewards, losses, backlash, strain, corruption, or consequence effects. RT-003 owns combat/hazard/damage/recovery when random outcomes produce threat, damage, injury, recovery, exposure, or active-threat effects. RT-004 owns ability/effect/skill binding when random outcomes produce capability grants, prerequisites, cooldowns, techniques, or mutation effects. RT-006 owns mission/reward/clue routing when random outcomes produce mission hooks, clue reveals, objective branches, reward distributions, or scenario consequences. RT-007 owns social/faction/actor-knowledge when random outcomes produce relationship changes, faction standing, contact introduction, reputation shifts, or institutional pressure. RT-010 owns inventory/item/vehicle/asset when random outcomes produce loot, items, gear, vehicles, cargo, salvage, equipment, fuel, ammo, charges, durability changes, or platform effects. RT-012 owns D-series/native-design promotion boundaries when source-pack material proposes random tables or oracle patterns but cannot become runtime/canon/sourcebook authority without promotion.

## 5. RNG/table/oracle dependency contract

The following RNG/table/oracle dependency states are conceptual dependency states as planning placeholders only. They are not final schemas, not database fields, not RNG implementation, not dice rolls, not table data, not oracle output, not event records, not replay verifier output, not runtime state, and not live-play prompts.

| Conceptual dependency placeholder | Planning meaning | Boundary note |
|---|---|---|
| `rng_authority_required` | A command, event, or downstream resolution requires backend-owned random authority before outcome selection. | No LLM rolling, choosing, or inferring. Backend must own selection. |
| `seed_reference_pending` | A random invocation requires a seed reference for determinism and replay before outcome generation. | No seed service implementation. Planning requirement only. |
| `replay_reference_pending` | A random outcome requires replay reference capability for audit and verification. | No replay verifier implementation. Planning requirement only. |
| `table_record_reference_required` | A random invocation must reference a validated table/oracle record before outcome selection. | No table data creation. Record reference requirement only. |
| `table_weight_validation_pending` | Table weights, ranges, and probability distributions require validation before invocation. | No table-weight validator implementation. Validation requirement only. |
| `table_result_domain_pending` | The result domain of a table/oracle must be validated for completeness, legality, and downstream compatibility. | No result-domain schema implementation. Validation requirement only. |
| `oracle_invocation_candidate` | An oracle invocation has been identified as a candidate but is not yet authorized, invoked, or committed. | No oracle engine implementation. Candidate status only. |
| `random_dependency_declared` | A downstream owner has declared a random dependency that RT-009 must fulfill through backend authority. | Declaration is not outcome selection. |
| `hidden_result_redaction_required` | A random outcome has hidden components that must route through RT-005 before any projection. | No redaction algorithm implementation. Routing requirement only. |
| `visible_result_projection_pending` | A random outcome's visible portion is pending context-packet projection through RT-005. | No context-packet compiler implementation. Projection requirement only. |
| `random_result_commit_pending` | A random outcome is pending backend-owned commitment through RT-001 event/state lifecycle. | No event ledger implementation. Commitment boundary only. |
| `random_result_rejected` | A random invocation or outcome has been rejected by backend authority due to legality, validation, or doctrine failure. | Rejection is non-mutating. No state change occurs. |
| `random_result_quarantined` | A random invocation or outcome cannot be resolved because doctrine, runtime, validation, or owner boundaries are missing. | Quarantine is non-mutating. Pending future resolution. |
| `narration_result_projection` | A committed, visible random outcome has been packeted for narration projection. | Narration cannot become random authority. Projection only. |

These planning placeholders are not final schemas, not database fields, not RNG implementation, not dice rolls, not table data, not oracle output, not event records, not replay verifier output, not runtime state, and not live-play prompts. A future implementation may rename, split, combine, or replace these placeholders, but it must preserve the backend-owned random authority, seed/replay requirement, table/oracle record reference, result-domain validation, hidden-result redaction, commitment boundary, and narration projection semantics described here.

## 6. Random-result commitment contract

The RT-009 random-result commitment contract is planning-level only:

- random dependency declaration is not outcome selection;
- table/oracle record reference is not table execution;
- seed/replay reference requirement is not seed service implementation;
- validation requirement is not validator implementation;
- hidden result preparation is not player/model visibility;
- random result commitment must be backend-owned and event/state/persistence handoff must be separately implemented;
- random outcomes that affect resources, rewards, hazards, missions, generated content, or assets must route to the proper downstream owner before commitment;
- narrated chance, model sampling, prose uncertainty, or LLM wording cannot serve as RNG authority;
- committed random outcomes require backend-owned event records, audit trails, and persistence routing through future separately-authorized systems;
- failed or rejected random invocations must not mutate state;
- quarantined random invocations must remain non-mutating until separately resolved;
- cost/reward/loss outcomes from random results must route through RT-002;
- combat/hazard/damage outcomes from random results must route through RT-003;
- mission/clue/reward outcomes from random results must route through RT-006;
- generated-content outcomes from random results must route through RT-008;
- inventory/loot/asset outcomes from random results must route through RT-010.

This contract does not define final RNG algorithms, roll syntax, seed formats, replay formats, table row formats, result-domain schemas, event fields, commitment protocols, or persistence writer behavior.

## 7. Table/oracle record contract

The RT-009 table/oracle record contract is planning-level only:

- table/oracle records are evidence/record structures, not executable RNG systems by themselves;
- table weights, ranges, result domains, visibility status, source-local status, and provenance require validation before use;
- donor table formats are not Astra runtime law;
- table/oracle outputs that create generated content require RT-008;
- hidden table/oracle results require RT-005;
- mission/reward/clue tables require RT-006 and RT-002 as applicable;
- hazard/combat tables require RT-003;
- loot/item/asset tables require RT-010 and RT-002 as applicable;
- crafting/salvage/recipe tables require RT-010 and RT-002 as applicable;
- ability/effect/technique tables require RT-004;
- social/faction/contact tables require RT-007;
- validation/readiness routes through RT-011;
- source-local table/oracle records must preserve source-local boundaries and cannot become Astra-wide runtime law by repetition or narration;
- D-series/native-design table/oracle patterns must route through RT-012 before any promotion claim.

This contract does not create final table/oracle schemas, row data, result-domain logic, table-weight formulas, validator code, oracle engine code, table roller code, or persistence writer behavior.

## 8. Future RNG/table/oracle artifact inventory

The following future RNG/table/oracle artifact families are semantic requirements only. They are not implemented schemas, not records, not validators, not services, not final fields, not formulas, not JSON schema, not database schema, not Pydantic models, not validator code, not RNG code, not dice code, not table roller code, not oracle engine code, not replay verifier code, not persistence code, not retrieval code, not context-packet compiler code, and not runtime code. Every listed family has implementation status `future_required_not_implemented`.

| Future artifact family | Purpose | Owner | LLM allowed interaction | Downstream handoff | Implementation status |
|---|---|---|---|---|---|
| `RandomAuthorityRequirement` | Define future requirements for backend-owned random authority over all RNG/table/oracle invocations. | RT-009 with RT-001 invocation timing. | No random authority; may not roll, choose, or infer outcomes. | RT-001 for invocation timing; backend runtime for selection. | `future_required_not_implemented` |
| `RandomInvocationRequirement` | Require backend-owned invocation authorization before any random selection occurs. | RT-009 with RT-001 command lifecycle. | No invocation authority; may describe visible invocation status after backend packet. | RT-001 for command lifecycle; RT-011 for validation. | `future_required_not_implemented` |
| `SeedReferenceRequirement` | Require seed references for determinism and reproducibility of random outcomes. | RT-009 and future backend seed owner. | No seed authority; may not create, modify, or select seeds. | Future seed service only if separately authorized. | `future_required_not_implemented` |
| `ReplayReferenceRequirement` | Require replay reference capability for audit and verification of random outcomes. | RT-009 and future backend replay owner. | No replay authority; may not create or verify replay references. | Future replay verifier only if separately authorized. | `future_required_not_implemented` |
| `TableRecordReferenceRequirement` | Require validated table/oracle record references before outcome selection. | RT-009 with C10 record pressure. | No table authority; may cite visible table names or IDs from backend context. | RT-011 for validation; C10 for record structure. | `future_required_not_implemented` |
| `TableWeightValidationRequirement` | Require validation of table weights, ranges, and probability distributions before invocation. | RT-009 with RT-011 validation. | No weight authority; may not set, adjust, or validate weights. | RT-011 for validation governance. | `future_required_not_implemented` |
| `TableResultDomainRequirement` | Require validation of result domains for completeness, legality, and downstream compatibility. | RT-009 with RT-011 validation. | No domain authority; may not define or validate result domains. | RT-011 for validation; downstream RT owners for domain-specific checks. | `future_required_not_implemented` |
| `OracleInvocationRequirement` | Require backend-owned oracle invocation authorization and outcome selection. | RT-009 with RT-001 command lifecycle. | No oracle authority; may not choose oracle outcomes. | RT-001 for invocation timing; RT-005 for hidden results. | `future_required_not_implemented` |
| `HiddenResultRedactionRequirement` | Require hidden random results to route through RT-005 redaction before any projection. | RT-009 with RT-005 redaction owner. | No redaction authority; may not reveal hidden results. | RT-005 for redaction and context-packet projection. | `future_required_not_implemented` |
| `VisibleResultProjectionRequirement` | Require visible random results to route through RT-005 context-packet projection. | RT-009 with RT-005 projection owner. | May narrate only backend-approved visible results within context-packet constraints. | RT-005 for context-packet projection. | `future_required_not_implemented` |
| `RandomResultCommitmentRequirement` | Require backend-owned commitment of random outcomes through RT-001 event/state lifecycle. | RT-009 with RT-001 event commitment. | No commitment authority; may not commit random outcomes. | RT-001 for event commitment; future persistence owner. | `future_required_not_implemented` |
| `RandomResultRejectionRequirement` | Preserve non-mutating rejection status for illegal, invalid, or doctrine-blocked random invocations. | RT-009 with RT-001 rejection. | May explain visible rejection reason within backend packet. | RT-001 for rejection; RT-011 for validation. | `future_required_not_implemented` |
| `RandomResultQuarantineRequirement` | Preserve non-mutating quarantine for random invocations pending doctrine, runtime, or validation resolution. | RT-009 with RT-001 quarantine. | May explain that resolution is pending, not invent outcome. | RT-001 for quarantine; RT-011 for readiness. | `future_required_not_implemented` |
| `RandomDependencyDisclosureRequirement` | Require disclosure of random dependencies by downstream owners before invocation. | RT-009 coordinates with RT-002 through RT-012. | May enumerate visible dependencies but may not certify completeness. | Relevant RT owner and RT-011 validation. | `future_required_not_implemented` |
| `RandomOutcomeValidationRequirement` | Require future validation of random outcomes for legality, domain completeness, weight correctness, and downstream compatibility. | RT-011 validation/readiness owner with RT-009 requirements. | May draft validation checklists but may not run nonexistent validators. | RT-011 and future validator implementation if separately authorized. | `future_required_not_implemented` |
| `RandomAuditTrailRequirement` | Require audit trail preservation for all random invocations, seed references, replay references, outcome selections, commitments, rejections, and quarantines. | RT-009 with future backend audit owner. | No audit authority; may not create or modify audit records. | Future audit/persistence owner only if separately authorized. | `future_required_not_implemented` |

## 9. Validation and readiness requirements

RT-009 validation and readiness requirements are future requirements only. They coordinate with RT-011 and do not implement validators, test fixtures, CI jobs, schemas, databases, RNG systems, dice rollers, table rollers, oracle engines, replay verifiers, context-packet compilers, or runtime code.

Future validation/readiness coverage must include:

- RNG authority boundary validation;
- table/oracle record reference validation;
- table weight/range/domain validation;
- seed/replay requirement validation;
- hidden-result redaction routing validation;
- visible-result projection validation;
- random-result commitment boundary validation;
- generated-content random dependency validation;
- mission/reward/clue random dependency validation;
- hazard/combat random dependency validation;
- loot/item/asset random dependency validation;
- donor table format non-authority validation;
- LLM non-authority validation;
- non-implementation guardrail validation.

RT-011 owns validation/readiness governance for these requirements. RT-009 supplies the random authority, invocation, seed/replay, result-domain, table-weight, hidden-result, commitment, and narration projection semantics that future RT-011 validators or reviewer checklists would need if separately authorized.

## 10. Downstream handoffs

RT-009 handoffs must remain explicit and auditable:

- RT-001 for command lifecycle, event commitment, rejection/quarantine, and RNG/table/oracle invocation timing;
- RT-002 for random costs, rewards, losses, consequence pressure, recovery pressure, economy pressure, and resource effects;
- RT-003 for random combat, hazard, damage, injury, recovery, exposure, and active-threat outcomes;
- RT-004 for random ability, effect, technique, skill, prerequisite, cooldown, mutation, and capability-output pressure;
- RT-005 for hidden random results, redaction, context-packet projection, narrator fact-set limits, and visible result presentation;
- RT-006 for random mission, clue, objective, branch, reward, penalty, scenario, and hidden-truth outcomes;
- RT-007 for random social/faction/contact/reputation/actor-knowledge/institutional pressure outcomes;
- RT-008 for random generated-content dependencies, provenance, durable eligibility, recurrence eligibility, and source-local generated outputs;
- RT-010 for random inventory, item, vehicle, cargo, asset, loot, salvage, repair, requisition, fuel, ammo, charge, durability, and platform outcomes;
- RT-011 for validation/readiness governance;
- RT-012 for D-series/native-design material that proposes random tables or oracle patterns but cannot become runtime/canon/sourcebook authority without promotion.

Downstream consumers must not treat RT-009 planning language as RNG implementation, dice roller output, table roller output, oracle engine output, table data, table schemas, result-domain schemas, seed services, replay verifier output, random-result event records, persistence authorization, sourcebook authorization, or canon. They must preserve backend-owned random authority, seed/replay requirements, table/oracle record references, result-domain validation, hidden-result redaction, commitment boundaries, and narration projection limits in their future owner specifications.

## 11. LLM non-authority rules

The LLM is explicitly prohibited from:

- rolling dice;
- choosing random results;
- selecting table rows;
- selecting oracle outcomes;
- creating hidden random results;
- revealing hidden random results;
- setting table weights;
- validating result domains;
- inventing table rows as truth;
- using model randomness as RNG authority;
- treating narrated chance as backend randomness;
- committing random-result events;
- creating seed or replay references;
- treating donor table formats as Astra runtime law;
- generating loot/rewards/hazards/missions/items as committed outcomes;
- bypassing RT-005 redaction;
- bypassing RT-008 provenance for generated outcomes;
- bypassing RT-011 validation;
- authorizing canon/sourcebook/training/live-play use.

The LLM may describe backend-selected visible results only when bounded context allows it and may narrate visible outcomes within backend-provided packets or clearly labeled non-authoritative contexts. Such interaction remains advisory and may not become random authority, table execution, oracle commitment, seed/replay creation, hidden-result revelation, persistence, sourcebook material, or canon.

## 12. Non-implementation reaffirmation

This PR adds no:

- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- generator implementation;
- RNG implementation;
- dice roller;
- table roller;
- oracle engine;
- table data;
- table schema;
- result-domain schema;
- seed service;
- replay verifier;
- table-weight validator;
- random-result event schema;
- persistence writer;
- retrieval index;
- context-packet compiler;
- redaction algorithm;
- event ledger implementation;
- database schema;
- live-play prompt;
- training data;
- donor-content audit;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion.

This specification is Stage 2 owner-specification planning only. It cannot be used as runtime readiness, schema readiness, validator readiness, RNG readiness, dice roller readiness, table roller readiness, oracle engine readiness, seed service readiness, replay verifier readiness, table-weight validator readiness, result-domain schema readiness, random-result event schema readiness, generated-record authorization, durable-record authorization, sourcebook authorization, pilot-conversion authorization, live-play authorization, training authorization, donor-content audit, or canon-promotion evidence.

## 13. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-F
  track: RT-009
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_validator_implementation: false
  authorizes_generator_implementation: false
  authorizes_rng_implementation: false
  authorizes_dice_roller: false
  authorizes_table_roller: false
  authorizes_oracle_engine: false
  authorizes_seed_service: false
  authorizes_replay_verifier: false
  authorizes_event_ledger: false
  authorizes_context_packet_compiler: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  authorizes_pilot_conversion: false
  next_allowed_step: downstream domain owner-spec bundle for RT-003, RT-004, RT-006, and RT-007, pending review
```
