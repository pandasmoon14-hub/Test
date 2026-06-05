# RT-001 Command Lifecycle / Action Legality Owner Scaffold

Date prepared: 2026-06-05
Status: owner scaffold only
Tracking ID: REMEDIATION-RT001-COMMAND-LIFECYCLE-OWNER-SCAFFOLD-001
Remediation track: RT-001-command-lifecycle-action-legality
Owner: Astra Doctrine Council / future command lifecycle control owner

## 1. Purpose and scope

This file creates the documentation/control owner scaffold for RT-001, the command lifecycle, legality, and cost commitment spine identified by `REMEDIATION-PRIORITY-LEDGER-001`. It exists to name the future owner boundary that must separate player intent, backend legality checks, cost commitment, resolution triggering, state-delta validation, event commitment, context-packet handoff, and narration.

This scaffold is planning/control only. It is owner scaffold only: no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no persistence writer implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

This scaffold is planning/control only. It does not define final command IR, final schemas, validators, math, runtime code, generators, persistence writers, context-packet compilers, live-play behavior, training data, donor-content audit results, or canon promotion.

## 2. Remediation ledger linkage

`docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` ranks RT-001 as P0 because command declaration, legality, committed costs, resolution triggers, rollback/cancel/interrupt handling, and state-delta commits are the central runtime seam. The ledger recommends PR-A as the first safe remediation step: create owner-file scaffolds for RT-001 and RT-011 only, without final IR, schemas, validators, math, runtime, or generators.

RT-001 remains blocked by the future command IR owner, runtime state/event owner, cost/resource math owner, command-context handoff owner, and RT-011 validation/readiness tooling owner.

## 3. Audit-source linkage

This scaffold links to these accepted audit sources without expanding or changing their findings:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, which establishes the backend-first audit protocol and the no-implementation boundary.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, which records backend-first and model-interchangeability pressure.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`, which records the B02 action declaration/cost commitment lifecycle boundary, the A10 resource/cost/backlash boundary, and the D02 cost-commitment draft-source-material boundary.

## 4. Source pressure

The future RT-001 owner must account for pressure from actual repo sources while preserving their current authority limits:

- B02: `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` supplies action declaration, cost commitment, and resolution-trigger procedure pressure.
- A10: `docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md` supplies resource cost, backlash, corruption, strain, and recovery pressure.
- D02 draft-source material: `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-03_cost_commitment_overinvestment_and_success_at_cost.md` may exert design pressure only; it is not current runtime authority, canon, sourcebook prose, live-play behavior, or training data.
- C03: `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` supplies ability/power/technique cost, prerequisite, cooldown, and effect-binding pressure.
- C10: `docs/doctrine/schema/C10_table_oracle_record_schema.md` supplies table/oracle/RNG ownership pressure and reinforces that narration cannot select random outcomes.

## 5. Owner responsibilities

The future RT-001 owner is responsible for planning and later coordinating, in separately authorized PRs, the owner decomposition for:

- command lifecycle ownership from player intent through backend event commitment;
- backend legality checks and clarification routing;
- cost declaration, cost commitment, refund/rollback routing, and resolution-trigger boundaries;
- backend-owned dice/RNG trigger handoff and replay/audit expectations;
- state-delta validation before event commitment;
- narration packet handoff after backend commitment;
- tests that prove the LLM cannot act as the authority for legality, costs, random outcomes, hidden modifiers, consequences, state changes, file writes, or canon changes.

## 6. Must-not-own boundaries

This scaffold and the future RT-001 owner must not own or claim to complete:

- final command IR fields;
- final JSON schemas, database schemas, or backend schemas;
- executable validators;
- runtime implementation or state-machine code;
- generators or generator prompts;
- persistence writer implementation;
- context-packet compiler implementation;
- final resource/cost math;
- donor-content audit;
- D-series promotion;
- live-play authorization;
- training-data authorization;
- canon promotion.

## 7. Conceptual lifecycle placeholders only

The following names are planning placeholders for discussion and test targeting only:

- player_intent_received
- intent_parsed_or_clarification_needed
- candidate_command_proposed
- legality_checked_by_backend
- costs_declared
- costs_committed
- resolution_triggered
- state_delta_validated
- event_committed
- narration_packet_prepared
- narration_rendered

These names are not final command IR, not a schema, not runtime implementation, not executable state machine code, not validator logic, and not live-play authorization. They only mark seams that later owners must resolve.

## 8. Required future outputs

Future PRs, after this scaffold, must separately authorize and produce:

- command IR ownership doctrine;
- runtime state/event ownership doctrine;
- cost/resource math ownership doctrine;
- legality and state-delta validator specifications;
- context-packet handoff specification;
- narration contract updates;
- replay/audit test expectations;
- reviewer decision records for any promotion beyond planning.

## 9. Dependency relationships

RT-001 depends on RT-011 for validation/readiness boundary discipline and on future resource/cost math, runtime event, command-context handoff, RNG/table/oracle, ability/effect binding, and hidden-information owners. Later remediation tracks must not consume RT-001 as implemented runtime authority until separately approved outputs exist.

## 10. LLM non-authority rules

The LLM is not the authority for RT-001. It must not:

- validate action legality;
- spend or refund costs;
- roll dice or select random results;
- decide hidden modifiers;
- commit state deltas;
- invent consequences;
- write files;
- alter canon;
- treat narration as event commit.

The LLM may only draft proposals, ask clarifying questions, or render narration from backend-authorized facts when a future backend/context handoff permits it.

## 11. Context-packet and narration handoff expectations

Future context packets must expose only backend-authorized command status, visible costs, visible outcomes, and narration-safe facts. Hidden modifiers, uncommitted state, unresolved legality, backend-only audit data, and unavailable consequences must remain withheld. Narration may describe an already committed event, but narration is not event commitment and cannot mutate state.

## 12. First-test expectations

The first RT-001 tests should remain focused and non-brittle. They should verify that this owner scaffold exists, references RT-001 and `REMEDIATION-PRIORITY-LEDGER-001`, links B02/A10/D02/C03/C10 pressure, states the non-implementation guardrails, and prohibits LLM authority over legality, costs, RNG/dice, hidden modifiers, consequences, state deltas, file writing, and canon.

## 13. Explicit non-implementation statement

This RT-001 owner scaffold is documentation/control planning only. It implements no command IR, schemas, runtime, validators, generators, persistence writers, context-packet compilers, cost math, dice/RNG engine, state machine, live-play adapter, training data, donor-content audit, or canon promotion.
