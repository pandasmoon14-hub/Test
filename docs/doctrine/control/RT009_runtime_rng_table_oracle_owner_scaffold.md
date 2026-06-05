# RT-009 Runtime RNG / Table / Oracle Owner Scaffold

Date prepared: 2026-06-05
Status: owner scaffold only
Tracking ID: REMEDIATION-RT009-RUNTIME-RNG-TABLE-ORACLE-OWNER-SCAFFOLD-001
Remediation track: RT-009-runtime-rng-table-oracle
Owner: Astra Doctrine Council / future runtime RNG, table, oracle, seed, replay, and hidden-result boundary owner

## 1. Purpose and scope

This file creates the documentation/control owner scaffold for RT-009, the runtime RNG, table, oracle, seed/replay, hidden-result, and narration-projection track identified by `REMEDIATION-PRIORITY-LEDGER-001`. It exists to name the future owner boundary that must separate table/oracle records, invocation eligibility, deterministic RNG authority, seed references, replay references, hidden-result redaction, result commitment, validation, and narration projection.

This scaffold is planning/control only. It is owner scaffold only: no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no mission generation, no reward commitment, no clue reveal, no hidden-truth database implementation, no RNG implementation, no oracle/table roll implementation, no random table data creation, no persistence writer implementation, no replay verifier implementation, no retrieval index implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

This scaffold does not implement remediation. It does not define RNG implementation, dice roller behavior, oracle registry data, random table data, table validators, event models, replay verifiers, context-packet compilers, runtime code, live-play authorization, training behavior, donor-content audit results, or canon promotion.

## 2. Remediation ledger linkage

`docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` recommends PR-F as mission/reward/clue and RNG/table/oracle owner scaffolds. The ledger states that RT-006 and RT-009 should be added after context/provenance and command/event scaffolds exist and that this work must not roll tables, generate missions, reveal clues, or commit rewards.

RT-009 is therefore a planning owner boundary only. It records that RNG/table/oracle outcomes must be backend-owned, deterministic, seedable/replayable, auditable, and redacted when hidden.

## 3. Dependency on existing and adjacent remediation tracks

RT-009 depends on `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` because random or oracle outcomes can become state only through backend-owned command/event/state commitment, not through narration or model assertion.

RT-009 depends on `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md` because hidden results must route through RT-005 before projection. Redacted random outcomes, secret rolls, oracle truths, hidden rows, and delayed reveals cannot be exposed by the LLM.

RT-009 depends on `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` because prose readiness is not executable validation and future table weight, result-domain, seed/replay, hidden-result, and invocation paths require validators and reviewer gates.

RT-009 must coordinate with `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` where costs, rewards, losses, penalties, value, backlash, strain, corruption, or consequence math depend on tables. RT-009 must coordinate with `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md` where hazard, opposition, damage, recovery, exposure, or active-threat tables matter. RT-009 must coordinate with future RT-006 where missions, clues, objectives, branches, rewards, and scenario consequences depend on tables/oracles. RT-009 must coordinate with `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md` where generated content, recurrence, durable table results, and provenance matter.

Mission/hazard/reward uses of tables must not bypass RT-006, RT-003, or RT-002 as applicable.

## 4. Audit-source linkage

This scaffold links to accepted audit sources without expanding, correcting, or implementing their findings:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, which establishes backend-first audit procedure, non-implementation boundaries, and LLM non-authority over backend truth.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, which records hazard/environment, hidden information, generated-content, and runtime ownership pressure.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`, which records C10 table/oracle, C07 mission/scenario, generated/provenance, and adjacent runtime seams.

## 5. Source pressure and actual-file posture

The future RT-009 owner must account for pressure from actual repo sources while preserving each source's current authority limits:

- README/backend-first invariant: `README.md` and the roadmap posture require backend-first control; model output is an adapter/projection layer and not RNG authority.
- C10: `docs/doctrine/schema/C10_table_oracle_record_schema.md` owns table/oracle/generator record conversion pressure, but table/oracle records are not executable RNG systems by themselves.
- B10: `docs/doctrine/operations/batch_b/B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md` pressures opposition, hazard contact, active-threat triggers, and possible random/triggered escalation without making the LLM a dice roller or table owner.
- C09: `docs/doctrine/schema/C09_hazard_environment_record_schema.md` pressures hazard/environment table or oracle generation, exposure events, weather, travel complications, and trap results while preserving hazard ownership and provenance boundaries.
- C07 where relevant: `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` pressures random mission tables, scenario hooks, objective routing, reward/clue links, and table/oracle dependencies while preserving RT-006 ownership for mission/reward/clue routing.
- Roadmap: `docs/doctrine/astra_doctrine_roadmap_v0_1.md` supplies roadmap RNG/runtime language, backend-first language, hidden-info language, and the backend-first model-interchangeability invariant: the model is interchangeable and cannot be treated as randomness, oracle, replay, or backend event authority.

## 6. Owner responsibilities

The future RT-009 owner is responsible for defining, in a later implementation-authorized PR, how table/oracle invocation eligibility, deterministic RNG authority, seed references, replay references, table record references, table weight validation, result-domain validation, hidden result redaction, random result commitment, audit trails, and narration projection route to backend owners.

RNG/table/oracle outcomes must be backend-owned, deterministic, seedable/replayable, auditable, and redacted when hidden. Narration may only describe backend-selected and context-approved results.

## 7. Must-not-own boundaries

RT-009 must not own runtime implementation, dice roller behavior, oracle registry data, random table data, table validators, final schemas, event models, replay verifier behavior, context-packet compiler behavior, command IR, math formulas, mission runtime, reward economy, clue schema, hidden-truth database, hazard damage, faction standing, persistence writers, retrieval indexes, live-play prompts, training behavior, donor-content audit results, or canon promotion.

Table/oracle records are not executable RNG systems by themselves. Hidden results must route through RT-005 before projection. Mission/hazard/reward uses of tables must not bypass RT-006, RT-003, or RT-002 as applicable.

## 8. Conceptual RNG/table/oracle seams only

The following names are conceptual placeholders only: `rng_authority_required`, `seed_reference_pending`, `table_record_reference`, `table_weight_validation_pending`, `oracle_invocation_candidate`, `hidden_result_redaction_required`, `replay_reference_required`, `random_result_commit_pending`, `table_result_domain_pending`, and `narration_result_projection`.

These planning placeholders are not RNG implementation, not dice roller, not oracle registry, not random table data, not table validator, not event model, not replay verifier, not context-packet compiler, and not live-play authorization. They do not create seeds, replay records, table rows, oracle records, hidden random results, validators, event commits, runtime rolls, or backend randomness.

## 9. Required future outputs

Future RT-009 work, if separately authorized, must produce owner specifications for RNG authority, seed/replay requirements, table/oracle invocation rules, table weight and result-domain validation, hidden-result redaction through RT-005, result commitment through RT-001, cost/reward/consequence handoff through RT-002, hazard handoff through RT-003, mission/reward/clue handoff through RT-006, generated/provenance handoff through RT-008, validation gates through RT-011, and context-packet/narration projection rules.

## 10. Dependency relationships

- RT-001 controls command/event/state commitment for random or oracle outcomes.
- RT-002 controls cost, reward, penalty, loss, value, backlash, strain, corruption, and consequence math that may depend on tables.
- RT-003 controls hazard, combat, damage, exposure, recovery, and active-threat effects that may depend on tables.
- RT-005 controls hidden random results, redaction, context-packet projection, and hidden-info exposure.
- RT-006 controls mission, reward, clue, objective, branch, hidden-truth, and scenario-consequence use of table/oracle outcomes.
- RT-008 controls generated content provenance, recurrence, durable-record eligibility, and canon separation for table/oracle outputs.
- RT-011 controls validation/readiness gates and reviewer-approved movement from prose to executable controls.

## 11. LLM non-authority rules

The LLM must not roll dice, choose random results, select oracle/table outcomes, alter table weights, invent rows or result domains as truth, decide hidden random results, commit oracle outcomes, create replay references, use model randomness as RNG authority, treat narrated chance as backend randomness, or bypass backend validation/reviewer approval.

The LLM may only draft proposals, summaries, or player-facing narration from backend-selected and context-approved results. It may not convert colorful chance narration, generated rows, model sampling, oracle suggestions, or summaries into backend randomness.

## 12. Context-packet and narration handoff expectations

Context packets must carry only backend-selected results, approved visible result domains, authorized redactions, and context-approved narration posture. Hidden results must route through RT-005 before projection. Narration may describe only backend-selected and context-approved results and must not imply dice rolls, table outcomes, oracle commitments, hidden result decisions, replay references, validation, or event commitment.

## 13. First-test expectations

Initial tests should verify file presence, `REMEDIATION-PRIORITY-LEDGER-001` linkage, RT-009 dependency references, audit-source references, README/backend-first invariant, C10/B10/C09/C07/roadmap source-pressure references, RNG/runtime language, backend-first model-interchangeability invariant language, LLM non-authority guardrails, explicit non-implementation guardrails, registry tracking, and absence of implementation claims.

## 14. Explicit non-implementation statement

This RT-009 scaffold is not remediation implementation. It creates no RNG implementation, no dice roller, no oracle registry, no random table data, no table validator, no runtime implementation, no event model, no replay verifier, no persistence writer, no retrieval index, no context-packet compiler, no command IR, no math implementation, no mission runtime, no reward economy, no clue schema, no hidden-truth database, no live-play prompt, no training behavior, no donor-content audit, and no canon promotion.
