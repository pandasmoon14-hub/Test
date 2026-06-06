# RT-009 Runtime RNG / Table / Oracle Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification only
Tracking ID: REMEDIATION-STAGE2-RT009-RUNTIME-RNG-TABLE-ORACLE-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-F
Remediation track: RT-009-runtime-rng-table-oracle
Owner: Astra Doctrine Council / future runtime RNG, table, oracle, seed, replay, and hidden-result boundary owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-009. It upgrades `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md` into a specification-level planning artifact for backend-owned random authority, RNG/table/oracle invocation ownership, table/oracle record reference requirements, seed/replay reference requirements, result-domain validation requirements, table-weight validation requirements, hidden-result redaction handoff requirements, random-result commitment boundaries, oracle/table outcome narration projection requirements, random dependency disclosure requirements, downstream domain owner handoffs, auditability requirements, and LLM non-authority rules.

This specification remains non-executable and non-implementation. It defines planning-level ownership seams, future semantic requirements, authority boundaries, handoff obligations, validation/readiness expectations, and LLM non-authority rules only. It does not authorize RNG implementation, dice roller implementation, table roller implementation, oracle engine implementation, table data creation, table/oracle schema implementation, result-domain schema implementation, seed service implementation, replay verifier implementation, table-weight validator implementation, random-result event schema implementation, command IR implementation, validator implementation, generator implementation, persistence writer implementation, retrieval index implementation, context-packet compiler implementation, redaction algorithm implementation, event ledger implementation, database schema, runtime code, live-play prompt implementation, training data, donor-content audits, sourcebook inclusion authorization, pilot conversion authorization, or canon promotion.

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

This Stage 2 PR-F pass used actual repo files only. All requested planning and audit sources, current RT owner files, RNG/table/oracle/source pressure files, schema/math/readiness files, runtime/project authority sources, and `README.md` were present at drafting time. Specifically, the following source pressure files were confirmed present and their pressure is preserved: `docs/doctrine/schema/C10_table_oracle_record_schema.md`, `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`, `docs/doctrine/schema/C09_hazard_environment_record_schema.md`, `docs/doctrine/schema/C02_item_gear_record_schema.md`, `docs/doctrine/schema/C03_ability_power_technique_record_schema.md`, `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md`, `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md`, `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md`, `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`, `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`, `docs/doctrine/astra_doctrine_roadmap_v0_1.md`, `docs/doctrine/astra_doctrine_registry_v0_1.yaml`, `docs/decisions/current_decisions_log.md`, and `README.md`. No requested source path was absent. This specification does not rewrite C10, C07, C09, C02, C03, C08, C12, SM00, SM01, SM02, the RT-009 scaffold, or any downstream owner scaffold.

## 2. Scope

RT-009 owns planning-level governance for runtime RNG, table, oracle, seed/replay, and hidden-result boundaries. Ownership means defining future semantic requirements for how random authority must remain backend-owned, deterministic, seedable, replayable, auditable, result-domain-validated, table-weight-validated, and redacted when hidden. Ownership does not mean implementing RNG, dice rollers, table rollers, oracle engines, seed services, replay verifiers, table-weight validators, result-domain schemas, table data, random-result event schemas, validators, generators, persistence writers, retrieval indexes, context-packet compilers, redaction algorithms, event ledgers, databases, prompts, or runtime code.

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

RT-009 preserves the audit waves' pressure that table/oracle records (C10), hazard/environment tables (C09), mission/scenario tables (C07), item/gear tables (C02), ability/technique tables (C03), vehicle/platform tables (C08), and crafting/salvage tables (C12) all create random-result, table-invocation, oracle-invocation, hidden-result, and result-domain pressure that requires backend-owned authority before any runtime consumption. It also preserves the README's backend-first/model-interchangeability posture: model output may describe backend-selected visible results, but no LLM is the holder of random authority, table truth, oracle truth, seed authority, replay authority, or result commitment.

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

RT-009 also must not decide final schemas for C10, C07, C09, C02, C03, C08, or C12. It defines random-authority, table/oracle invocation, seed/replay, result-domain, table-weight, hidden-result, commitment, and narration-projection requirements that future RNG implementations, table rollers, oracle engines, seed services, replay verifiers, validators, persistence owners, and downstream domain owners must obey if separately authorized.

## 4. Authority model

The RT-009 authority model is deliberately split across owners:

- RT-001 owns command/event lifecycle and when an RNG/table/oracle dependency may be invoked, rejected, quarantined, or committed. Random invocation timing, cost commitment timing, and event commitment boundaries are RT-001 authority.
- RT-005 owns hidden-result visibility, redaction, and context/narration projection. Hidden random results, secret rolls, oracle truths, hidden rows, and delayed reveals must route through RT-005 before any model or player can see them.
- RT-008 owns generated-content provenance/recurrence implications when RNG/table/oracle output contributes to generated content. Durable table results, generated oracle output, and recurrence eligibility require RT-008 provenance controls.
- RT-011 owns validation/readiness requirements. Future table-weight validators, result-domain validators, seed/replay requirement validators, and random-authority boundary validators must route through RT-011 governance.
- Backend runtime, once separately implemented, must own all random authority, seed handling, replay references, outcome selection, result commitment, and audit trails. The backend is the sole source of random truth.
- The LLM may describe backend-selected visible results only and may not roll, choose, infer, or commit random outcomes. Model randomness is not RNG authority. Narrated chance is not backend randomness. Prose uncertainty is not outcome selection.

## 5. RNG/table/oracle dependency contract

The following dependency states are conceptual placeholders as planning terms only. They are not final schemas, not database fields, not RNG implementation, not dice rolls, not table data, not oracle output, not event records, not replay verifier output, not runtime state, and not live-play prompts.

| Conceptual state placeholder | Planning meaning | Boundary note |
|---|---|---|
| `rng_authority_required` | A command, event, or resolution path requires backend-owned random authority before an outcome can be selected. | Not an RNG call, not a dice roll, not a table lookup, not an oracle invocation. |
| `seed_reference_pending` | A random invocation requires a backend-owned seed reference for determinism and replay before outcome selection. | Not a seed service, not a seed database, not a seed format definition. |
| `replay_reference_pending` | A random invocation requires a backend-owned replay reference for auditability before outcome selection. | Not a replay verifier, not a replay database, not a replay format definition. |
| `table_record_reference_required` | A random invocation references a table/oracle record and requires that record to be validated and available before use. | Not a table lookup, not a table schema, not table data, not a table roller. |
| `table_weight_validation_pending` | A table record's weights, ranges, or probability distributions require backend-owned validation before random selection. | Not a table-weight validator, not weight calculation, not probability math. |
| `table_result_domain_pending` | A table record's result domain (the set of possible outcomes and their types) requires backend-owned validation before random selection. | Not a result-domain schema, not result-domain validation code, not outcome enumeration. |
| `oracle_invocation_candidate` | A command, event, or resolution path may require oracle-style authority (narrative-branching, fate-deciding, or interpretive randomness) pending backend review. | Not an oracle engine, not oracle output, not oracle data. |
| `random_dependency_declared` | A command, event, resolution, or generated-content path has declared its dependency on random authority and is awaiting backend routing. | Not outcome selection, not table execution, not oracle invocation. |
| `hidden_result_redaction_required` | A random outcome must be hidden from the player and/or the LLM and must route through RT-005 redaction before any projection. | Not a redaction algorithm, not a hidden-state database, not a context-packet compiler. |
| `visible_result_projection_pending` | A random outcome has been selected by the backend and is pending context-packet projection through RT-005 before narration. | Not a context-packet compiler, not a narration prompt, not a visibility algorithm. |
| `random_result_commit_pending` | A backend-selected random outcome is pending event/state/persistence commitment through RT-001 handoff. | Not an event commit, not a persistence write, not a database insert. |
| `random_result_rejected` | A random invocation or random outcome has been rejected by the backend due to legality, validation, doctrine, or authority failure. | Not state mutation, not a penalty, not a refund. |
| `random_result_quarantined` | A random invocation or random outcome cannot be resolved safely because doctrine, runtime, validation, schema, or owner boundaries are missing; it remains non-mutating until separately resolved. | Not persistence, not canon, not sourcebook eligibility. |
| `narration_result_projection` | A committed, backend-approved, visible random result may be narrated by the LLM within context-packet constraints only. | Not backend truth creation, not outcome authority, not RNG authority. |

These planning placeholders must not be copied into code, JSON schema, database fields, RNG systems, dice rollers, table rollers, oracle engines, seed services, replay verifiers, event records, persistence states, runtime state, context-packet compilers, or live-play prompts without separate implementation authorization.

## 6. Random-result commitment contract

The RT-009 random-result commitment contract is planning-level only:

- random dependency declaration is not outcome selection; declaring that a command or event requires random authority does not select the result;
- table/oracle record reference is not table execution; referencing a table record does not roll, look up, or produce an outcome;
- seed/replay reference requirement is not seed service implementation; requiring a seed or replay reference does not create a seed service, seed database, or replay verifier;
- validation requirement is not validator implementation; requiring table-weight, result-domain, or seed/replay validation does not create validators;
- hidden result preparation is not player/model visibility; routing a random result to hidden status does not expose it to the player or the LLM;
- random result commitment must be backend-owned and event/state/persistence handoff must be separately implemented; no random result becomes authoritative state without backend-owned event commitment through RT-001 and future persistence ownership;
- random outcomes that affect resources, rewards, hazards, missions, generated content, or assets must route to the proper downstream owner before commitment: RT-002 for resources/costs/rewards/consequences, RT-003 for combat/hazard/damage/recovery, RT-006 for missions/clues/objectives/rewards, RT-008 for generated-content provenance, RT-010 for inventory/items/vehicles/assets;
- narrated chance, model sampling, prose uncertainty, or LLM wording cannot serve as RNG authority; the LLM may describe visible backend-selected results but may not produce, imply, or commit random outcomes through narration.

This contract does not define final RNG algorithms, roll syntax, seed formats, replay formats, table row formats, result-domain schemas, event fields, persistence schemas, or database schemas.

## 7. Table/oracle record contract

The RT-009 table/oracle record contract is planning-level only:

- table/oracle records are evidence/record structures, not executable RNG systems by themselves; a table record describes possible outcomes, weights, ranges, result domains, source-local status, provenance, and visibility status but does not roll, select, or commit outcomes;
- table weights, ranges, result domains, visibility status, source-local status, and provenance require validation before use; unvalidated table records must not be consumed by downstream owners or the runtime;
- donor table formats are not Astra runtime law; donor-originated table structures, weight distributions, row formats, oracle patterns, and result sets are conversion-intake pressure that must be normalized, validated, and authority-separated before any runtime use;
- table/oracle outputs that create generated content require RT-008; durable table results, generated oracle output, recurrence-eligible random content, and provenance-required random output must route through RT-008 provenance controls;
- hidden table/oracle results require RT-005; secret rolls, hidden rows, delayed reveals, redacted outcomes, and hidden oracle truths must route through RT-005 redaction and context-packet projection before any model or player visibility;
- mission/reward/clue tables require RT-006 and RT-002 as applicable; random mission generation, reward selection, clue routing, objective branching, scenario hooks, and hidden-truth tables must route through RT-006 for mission/reward/clue ownership and RT-002 for cost/reward/consequence math;
- hazard/combat tables require RT-003; random hazard generation, combat encounter tables, damage tables, environmental exposure tables, active-threat trigger tables, and recovery tables must route through RT-003 for combat/hazard/damage/recovery ownership;
- loot/item/asset tables require RT-010 and RT-002 as applicable; random loot generation, item tables, vehicle tables, cargo tables, salvage tables, and asset-state tables must route through RT-010 for inventory/asset ownership and RT-002 for cost/value/consequence math;
- validation/readiness routes through RT-011; table-weight validation, result-domain validation, seed/replay requirement validation, hidden-result redaction validation, and random-authority boundary validation must coordinate with RT-011 governance.

This contract does not create final table/oracle schemas, row data, result-domain logic, validator code, table roller code, oracle engine code, or runtime code.

## 8. Future RNG/table/oracle artifact inventory

The following future RNG/table/oracle artifact families are semantic requirements only. They are not implemented schemas, not generated records, not durable records, not RNG systems, not dice rollers, not table rollers, not oracle engines, not seed services, not replay verifiers, not validators, not final fields, not formulas, not JSON schema, not database schema, not Pydantic models, not validator code, not RNG code, not dice code, not table roller code, not oracle engine code, not replay verifier code, not persistence code, not retrieval code, not context-packet compiler code, and not runtime code. Every listed family has implementation status `future_required_not_implemented`.

| Future artifact family | Purpose | Owner | LLM allowed interaction | Downstream handoff | Implementation status |
|---|---|---|---|---|---|
| `RandomAuthorityRequirement` | Define future requirements for backend-owned random authority boundaries before any outcome may be selected. | RT-009 with RT-001 invocation timing handoff. | None; the LLM may not claim random authority. | RT-001 for invocation timing; backend runtime for authority. | `future_required_not_implemented` |
| `RandomInvocationRequirement` | Define future requirements for when and how random invocations may be triggered within the command/event lifecycle. | RT-009 with RT-001 command lifecycle handoff. | None; the LLM may not trigger random invocations. | RT-001 for command/event timing; RT-011 for validation. | `future_required_not_implemented` |
| `SeedReferenceRequirement` | Define future requirements for backend-owned seed references that ensure determinism and reproducibility of random outcomes. | RT-009 with future backend seed service owner. | None; the LLM may not create, read, or modify seeds. | Future seed service; replay verifier; audit trail. | `future_required_not_implemented` |
| `ReplayReferenceRequirement` | Define future requirements for backend-owned replay references that ensure auditability and reproducibility of random outcomes. | RT-009 with future backend replay verifier owner. | None; the LLM may not create or verify replays. | Future replay verifier; audit trail; RT-011 validation. | `future_required_not_implemented` |
| `TableRecordReferenceRequirement` | Define future requirements for referencing validated table/oracle records before random selection may occur. | RT-009 with C10 record pressure and RT-011 validation. | None; the LLM may not select from tables. | RT-011 for record validation; relevant domain RT owner. | `future_required_not_implemented` |
| `TableWeightValidationRequirement` | Define future requirements for validating table weights, ranges, and probability distributions before random selection. | RT-009 with RT-011 validation handoff. | None; the LLM may not set or validate weights. | RT-011 for validation governance; future table-weight validator. | `future_required_not_implemented` |
| `TableResultDomainRequirement` | Define future requirements for validating table result domains (possible outcomes and their types) before random selection. | RT-009 with RT-011 validation handoff. | None; the LLM may not validate or define result domains. | RT-011 for validation governance; relevant domain RT owner. | `future_required_not_implemented` |
| `OracleInvocationRequirement` | Define future requirements for oracle-style invocations (narrative-branching, fate-deciding, interpretive randomness) that require backend authority. | RT-009 with RT-001 command lifecycle and RT-005 hidden-result handoff. | None; the LLM may not invoke oracles or select oracle outcomes. | RT-001 for invocation timing; RT-005 for hidden results; RT-008 for generated content. | `future_required_not_implemented` |
| `HiddenResultRedactionRequirement` | Define future requirements for routing hidden random results through RT-005 redaction before any model or player visibility. | RT-009 with RT-005 redaction handoff. | None; the LLM may not see, reveal, or infer hidden random results. | RT-005 for redaction and context-packet projection. | `future_required_not_implemented` |
| `VisibleResultProjectionRequirement` | Define future requirements for projecting backend-selected visible random results through RT-005 context-packet projection. | RT-009 with RT-005 context-packet handoff. | May narrate visible results only after backend selection and RT-005 projection. | RT-005 for context-packet projection; narration layer. | `future_required_not_implemented` |
| `RandomResultCommitmentRequirement` | Define future requirements for backend-owned random result commitment through RT-001 event/state/persistence handoff. | RT-009 with RT-001 event commitment handoff. | None; the LLM may not commit random results. | RT-001 for event commitment; future persistence owner; audit trail. | `future_required_not_implemented` |
| `RandomResultRejectionRequirement` | Define future requirements for rejecting random invocations or outcomes due to legality, validation, doctrine, or authority failure. | RT-009 with RT-001 rejection handoff. | May state visible rejection status supplied by backend context. | RT-001 for rejection; RT-011 for validation; audit trail. | `future_required_not_implemented` |
| `RandomResultQuarantineRequirement` | Define future requirements for quarantining random invocations or outcomes that cannot be resolved safely due to missing boundaries. | RT-009 with RT-001 quarantine handoff. | May state visible quarantine status supplied by backend context. | RT-001 for quarantine; RT-011 for readiness; relevant RT owner. | `future_required_not_implemented` |
| `RandomDependencyDisclosureRequirement` | Define future requirements for disclosing random dependencies so that downstream owners and audit trails can trace which commands, events, or generated content depend on randomization. | RT-009 with RT-001 and RT-008 handoffs. | None; the LLM may not certify dependency completeness. | RT-001 for command dependency; RT-008 for generated-content dependency; audit trail. | `future_required_not_implemented` |
| `RandomOutcomeValidationRequirement` | Define future requirements for validating random outcomes against result domains, table weights, seed references, replay references, and authority boundaries before commitment. | RT-009 with RT-011 validation handoff. | None; the LLM may not validate random outcomes. | RT-011 for validation governance; future outcome validators. | `future_required_not_implemented` |
| `RandomAuditTrailRequirement` | Define future requirements for audit trails that trace random invocations from command/event origin through seed, table/oracle reference, outcome selection, validation, hidden-result routing, commitment, and narration projection. | RT-009 with RT-001 and RT-011 handoffs. | None; the LLM may not create or modify audit trail records. | RT-001 for event lineage; RT-011 for validation; future audit/persistence owner. | `future_required_not_implemented` |

## 9. Validation and readiness requirements

RT-009 validation and readiness requirements are future requirements only. They coordinate with RT-011 and do not implement validators, test fixtures, CI jobs, schemas, databases, RNG systems, dice rollers, table rollers, oracle engines, seed services, replay verifiers, table-weight validators, result-domain validators, context-packet compilers, redaction algorithms, or runtime code.

Future validation/readiness coverage must include:

- RNG authority boundary validation: verify that random outcomes are backend-owned and that no narration, model sampling, or LLM output is treated as random authority;
- table/oracle record reference validation: verify that table/oracle records are validated and available before random selection references them;
- table weight/range/domain validation: verify that table weights, ranges, probability distributions, and result domains are valid and backend-approved before random selection;
- seed/replay requirement validation: verify that seed references and replay references are present and backend-owned before random outcome selection;
- hidden-result redaction routing validation: verify that hidden random results route through RT-005 before any model or player visibility;
- visible-result projection validation: verify that visible random results route through RT-005 context-packet projection before narration;
- random-result commitment boundary validation: verify that random result commitment routes through RT-001 event/state/persistence handoff and is backend-owned;
- generated-content random dependency validation: verify that random outcomes contributing to generated content route through RT-008 provenance controls;
- mission/reward/clue random dependency validation: verify that random outcomes affecting missions, rewards, clues, objectives, or scenario branches route through RT-006 and RT-002;
- hazard/combat random dependency validation: verify that random outcomes affecting combat, hazards, damage, recovery, exposure, or active threats route through RT-003;
- loot/item/asset random dependency validation: verify that random outcomes affecting inventory, items, vehicles, cargo, assets, loot, or salvage route through RT-010 and RT-002;
- donor table format non-authority validation: verify that donor-originated table formats, weight distributions, row formats, and result sets are not treated as Astra runtime law without normalization and authority separation;
- LLM non-authority validation: verify that no flow allows the LLM to roll dice, choose results, select table rows, select oracle outcomes, create hidden results, reveal hidden results, set weights, validate domains, invent rows as truth, commit events, create seeds/replays, or bypass downstream owner authority;
- non-implementation guardrail validation: verify that this planning artifact is not cited as runtime, schema, validator, generator, RNG, dice, table, oracle, seed, replay, event, persistence, retrieval, context-packet, redaction, live-play, training, donor-audit, sourcebook, pilot-conversion, or canon authority.

RT-011 owns validation/readiness governance for these requirements. RT-009 supplies the random-authority, table/oracle invocation, seed/replay, result-domain, table-weight, hidden-result, commitment, and narration-projection semantics that future RT-011 validators or reviewer checklists would need if separately authorized.

## 10. Downstream handoffs

RT-009 handoffs must remain explicit and auditable:

- RT-001: command lifecycle, event commitment, rejection/quarantine, and RNG/table/oracle invocation timing. RT-001 owns when a random invocation may be triggered, when a random result may be committed, and when a random invocation must be rejected or quarantined.
- RT-002: random costs, rewards, losses, consequence pressure, recovery pressure, economy pressure, and resource effects. Random outcomes that affect resource pools, cost commitments, reward values, loss calculations, consequence severity, recovery costs, or economy balance must route through RT-002.
- RT-003: random combat, hazard, damage, injury, recovery, exposure, and active-threat outcomes. Random encounter tables, hazard generation, damage rolls, environmental exposure, active-threat triggers, recovery tables, and combat consequence tables must route through RT-003.
- RT-004: random ability, effect, technique, skill, prerequisite, cooldown, mutation, and capability-output pressure. Random ability grants, technique mutations, effect variations, skill-check outcomes, prerequisite triggers, cooldown modifications, and capability-output tables must route through RT-004.
- RT-005: hidden random results, redaction, context-packet projection, narrator fact-set limits, and visible result presentation. All hidden random outcomes, secret rolls, hidden oracle truths, redacted table results, and delayed reveals must route through RT-005 before any model or player visibility.
- RT-006: random mission, clue, objective, branch, reward, penalty, scenario, and hidden-truth outcomes. Random mission generation, clue placement, objective routing, scenario branching, reward selection, penalty selection, and hidden-truth tables must route through RT-006.
- RT-007: random social/faction/contact/reputation/actor-knowledge/institutional pressure outcomes. Random social encounter tables, faction event tables, contact generation, reputation shifts, actor-knowledge reveals, and institutional pressure tables must route through RT-007.
- RT-008: random generated-content dependencies, provenance, durable eligibility, recurrence eligibility, and source-local generated outputs. Random outcomes that contribute to generated content, durable table results, generated oracle output, and recurrence-eligible random content must route through RT-008 provenance controls.
- RT-010: random inventory, item, vehicle, cargo, asset, loot, salvage, repair, requisition, fuel, ammo, charge, durability, and platform outcomes. Random loot tables, item generation, vehicle condition tables, cargo tables, salvage tables, repair outcome tables, asset-state tables, and equipment tables must route through RT-010.
- RT-011: validation/readiness governance. All RT-009 validation requirements, readiness claims, non-implementation guardrails, and future validator needs must coordinate with RT-011 governance.
- RT-012: D-series/native-design material that proposes random tables or oracle patterns but cannot become runtime/canon/sourcebook authority without promotion. D-series table proposals, native-design oracle patterns, and source-pack random structures must route through RT-012 promotion boundaries and may not become Astra runtime law without separate authorization.

Downstream consumers must not treat RT-009 planning language as RNG output, dice results, table results, oracle output, seed data, replay data, random-result events, persistence records, sourcebook authorization, or canon. They must preserve random-authority boundaries, table/oracle record reference requirements, seed/replay requirements, result-domain requirements, table-weight requirements, hidden-result routing, commitment boundaries, narration-projection limits, and backend/reviewer authority in their future owner specifications.

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

The LLM may draft an ephemeral narration of a backend-selected visible result, summarize visible backend-approved random-result status, or present visible options only when bounded context allows it. Such interaction remains advisory and downstream of backend selection. It may not convert colorful chance narration, generated rows, model sampling, oracle suggestions, prose uncertainty, or summaries into backend randomness, random authority, table truth, oracle truth, seed authority, replay authority, or committed outcomes.

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

This specification is Stage 2 owner-specification planning only. It cannot be used as runtime readiness, schema readiness, validator readiness, generator readiness, RNG readiness, dice roller readiness, table roller readiness, oracle engine readiness, seed service readiness, replay verifier readiness, table-weight validator readiness, result-domain schema readiness, random-result event schema readiness, persistence readiness, retrieval readiness, context-packet compiler readiness, redaction algorithm readiness, event ledger readiness, database readiness, live-play authorization, training authorization, donor-content audit, sourcebook inclusion authorization, pilot-conversion authorization, or canon-promotion evidence.

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
