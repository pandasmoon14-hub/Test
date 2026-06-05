# RT-006 Mission / Reward / Clue Routing Owner Scaffold

Date prepared: 2026-06-05
Status: owner scaffold only
Tracking ID: REMEDIATION-RT006-MISSION-REWARD-CLUE-ROUTING-OWNER-SCAFFOLD-001
Remediation track: RT-006-mission-reward-clue-routing
Owner: Astra Doctrine Council / future mission, reward, clue, hidden-truth, and consequence-routing boundary owner

## 1. Purpose and scope

This file creates the documentation/control owner scaffold for RT-006, the mission, reward, clue, hidden-truth, objective, branch, and consequence-routing track identified by `REMEDIATION-PRIORITY-LEDGER-001`. It exists to name the future owner boundary that must separate mission/scenario record evidence, objective-state candidates, clue visibility, hidden-truth partitions, reward/consequence commits, hazard/social consequence links, oracle dependencies, provenance, validation, and backend event authority.

This scaffold is planning/control only. It is owner scaffold only: no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no mission generation, no reward commitment, no clue reveal, no hidden-truth database implementation, no RNG implementation, no oracle/table roll implementation, no random table data creation, no persistence writer implementation, no replay verifier implementation, no retrieval index implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

This scaffold does not implement remediation. It does not define final schemas, mission runtime, reward economy, clue schema, hidden-truth database, branch runtime, generators, validators, event models, persistence writers, replay verifiers, retrieval indexes, context-packet compilers, live-play prompts, training behavior, donor-content audit results, or canon promotion.

## 2. Remediation ledger linkage

`docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` recommends PR-F as mission/reward/clue and RNG/table/oracle owner scaffolds. The ledger states that RT-006 and RT-009 should be added after context/provenance and command/event scaffolds exist and that this work must not roll tables, generate missions, reveal clues, or commit rewards.

RT-006 is therefore a planning owner boundary only. It records that mission/scenario records are not runtime missions until backend-owned state, event, reward, clue, hidden-truth, provenance, and validation paths exist.

## 3. Dependency on existing and later remediation tracks

RT-006 depends on `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` because objective completion, branch acceptance, mission failure, and scenario consequences require backend-owned command/event/state commitment rather than narration or model assertion.

RT-006 depends on `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` because reward and consequence commits are downstream of RT-002. RT-006 may route reward or loss candidates, but it cannot commit reward, penalty, loss, value flow, harm, debt, corruption, strain, or other consequence math.

RT-006 depends on `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md` because clue/hidden-truth exposure is downstream of RT-005. Context packets and narration may project only backend-authorized visible mission facts, clue states, redactions, and hidden-info partitions.

RT-006 depends on `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md` because generated missions require RT-008 provenance/recurrence controls before persistence. Repeated narration, model memory, or scenario usefulness is not durable generated content authority.

RT-006 depends on `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` because prose readiness is not executable validation and future mission, clue, reward, hidden-truth, event, provenance, and persistence paths require validators and reviewer gates.

RT-006 must coordinate with `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md` where hazards, active threats, exposure, recovery, injury, or disaster consequences matter. RT-006 must coordinate with `docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md` where social/faction state, standing, relationship knowledge, obligations, or institutional consequences matter. RT-006 must coordinate with future RT-009 runtime RNG/table/oracle ownership where table/oracle outcomes matter; table/oracle dependencies must route through RT-009 before results can be committed.

## 4. Audit-source linkage

This scaffold links to accepted audit sources without expanding, correcting, or implementing their findings:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, which establishes backend-first audit procedure, non-implementation boundaries, and LLM non-authority over backend truth.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, which records mission, hazard, social, hidden-information, generated-content, backend ownership, and recurrence pressure.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`, which records C07 mission/scenario/adventure, C10 table/oracle, generated/provenance, and adjacent procedure seams.

## 5. Source pressure and actual-file posture

The future RT-006 owner must account for pressure from actual repo sources while preserving each source's current authority limits:

- C07: `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` owns mission/scenario/adventure structure and states that C07 records do not define final adventure design, runtime quest state, objective state, branch state, event logs, reward economy, live-play scripts, canon events, or hidden reveal procedure.
- A13: `docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md` pressures harm, consequence, damage, injury, danger, and recovery routing that may become mission failure or hazard consequence candidates without giving RT-006 authority to commit them.
- C09: `docs/doctrine/schema/C09_hazard_environment_record_schema.md` pressures hazard/environment placement, timed danger, scripted hazard role, disaster scenario, and C09-to-C07 routing while preserving C09/RT-003 ownership for hazard mechanics.
- B09: `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md` pressures faction, patron, contact, obligation, reward, rumor, hidden agenda, and institutional consequence routing while preserving RT-007 and RT-002 boundaries.
- C10: `docs/doctrine/schema/C10_table_oracle_record_schema.md` pressures random mission tables, oracle outputs, table-generated hooks, hidden results, and conversion provenance while preserving RT-009 ownership of table/oracle outcomes.
- Roadmap: `docs/doctrine/astra_doctrine_roadmap_v0_1.md` supplies backend-first language, hidden-info language, and the backend-first model-interchangeability invariant: the LLM is an interchangeable narration/proposal adapter, not the mission, reward, clue, event, or hidden-truth authority.

## 6. Owner responsibilities

The future RT-006 owner is responsible for defining, in a later implementation-authorized PR, how mission/scenario structure, objective state, branch candidates, clue visibility, hidden-truth partitions, reward candidates, failure consequence candidates, hazard/social consequence links, oracle dependencies, provenance requirements, event requirements, validation gates, and context-packet projections are routed to their proper backend owners.

The owner must preserve backend-first control: mission narration, scenario prose, summaries, generated hooks, and model suggestions can be proposal material only until backend-owned state/event/reward/clue/hidden-truth/provenance/validation paths accept them.

## 7. Must-not-own boundaries

RT-006 must not own final schemas, mission runtime, reward economy, clue schema, hidden-truth database, branch runtime, generator behavior, validator behavior, event models, command IR, math formulas, hazard damage, faction standing, RNG/table/oracle selection, persistence writers, replay verifiers, retrieval indexes, context-packet compilers, live-play prompts, training behavior, donor-content audit results, or canon promotion.

Reward and consequence commits remain downstream of RT-002. Clue/hidden-truth exposure remains downstream of RT-005. Generated missions require RT-008 provenance/recurrence controls before persistence. Table/oracle dependencies must route through RT-009 before results can be committed.

## 8. Conceptual routing seams only

The following names are conceptual placeholders only: `mission_record_reference`, `objective_state_pending`, `branch_state_candidate`, `clue_visibility_pending`, `hidden_truth_partition`, `reward_commit_pending`, `failure_consequence_candidate`, `hazard_or_social_consequence_link`, `oracle_result_dependency`, `mission_completion_event_required`, and `scenario_generator_prohibited`.

These planning placeholders are not final schemas, not mission runtime, not reward economy, not clue schema, not hidden-truth database, not branch runtime, not generator, not validator, not event model, and not live-play authorization. They do not create persistent mission records, objective states, clue records, hidden-truth stores, reward ledgers, branch resolution, scenario canon, oracle outcomes, validators, or runtime events.

## 9. Required future outputs

Future RT-006 work, if separately authorized, must produce owner specifications for mission-state authority, objective completion events, branch candidate review, reward/consequence routing to RT-002, clue/hidden-truth exposure routing to RT-005, generated-mission provenance routing to RT-008, table/oracle dependency routing to RT-009, hazard/social handoffs to RT-003/RT-007, validation gates through RT-011, and context-packet/narration projection rules.

## 10. Dependency relationships

- RT-001 controls command/event/state commitment for mission completion and branch/failure events.
- RT-002 controls reward, penalty, loss, value, harm, backlash, strain, corruption, and consequence math commits.
- RT-003 controls hazard, combat, damage, exposure, injury, recovery, and active-threat consequence ownership.
- RT-005 controls hidden-info, redaction, context-packet projection, clue exposure, and hidden-truth visibility.
- RT-007 controls social/faction knowledge, standing, obligations, reputation, and institutional state.
- RT-008 controls generated mission provenance, recurrence, durable-record eligibility, and canon separation.
- RT-009 controls RNG/table/oracle invocation, result authority, seed/replay posture, and hidden random results.
- RT-011 controls validation/readiness gates and reviewer-approved movement from prose to executable controls.

## 11. LLM non-authority rules

The LLM must not generate missions as backend truth, complete objectives, reveal clues or hidden truths, select branches, commit rewards, penalties, or losses, decide mission failure consequences, mutate scenario state, select oracle/table outcomes, create persistent mission records, promote scenario canon, bypass backend validation/reviewer approval, or treat mission narration as backend event commitment.

The LLM may only draft proposals, summaries, or player-facing narration from backend-approved and context-approved inputs. It may not convert mission narration, generated hooks, dialogue, scene descriptions, oracle suggestions, or summaries into backend facts.

## 12. Context-packet and narration handoff expectations

Context packets must carry only backend-approved visible mission facts, authorized objective state, permitted clue visibility, approved redactions, and context-approved consequence/reward status. Hidden truth must stay partitioned until RT-005 authorizes exposure. Narration may describe only backend-approved mission state and must not imply objective completion, clue reveal, hidden-truth exposure, reward commitment, branch selection, random result commitment, or canon promotion.

## 13. First-test expectations

Initial tests should verify file presence, `REMEDIATION-PRIORITY-LEDGER-001` linkage, RT-006 dependency references, audit-source references, C07/A13/C09/B09/C10/roadmap source-pressure references, backend-first language, hidden-info language, backend-first model-interchangeability invariant language, LLM non-authority guardrails, explicit non-implementation guardrails, registry tracking, and absence of implementation claims.

## 14. Explicit non-implementation statement

This RT-006 scaffold is not remediation implementation. It creates no mission runtime, no reward economy, no clue schema, no hidden-truth database, no branch runtime, no scenario generator, no validator, no event model, no command IR, no math implementation, no RNG/table/oracle implementation, no persistence writer, no replay verifier, no retrieval index, no context-packet compiler, no live-play prompt, no training behavior, no donor-content audit, and no canon promotion.
