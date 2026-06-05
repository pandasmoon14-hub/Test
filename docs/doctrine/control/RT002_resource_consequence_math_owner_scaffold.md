# RT-002 Resource / Consequence Math Owner Scaffold

Date prepared: 2026-06-05
Status: owner scaffold only
Tracking ID: REMEDIATION-RT002-RESOURCE-CONSEQUENCE-MATH-OWNER-SCAFFOLD-001
Remediation track: RT-002-resource-backlash-consequence-math
Owner: Astra Doctrine Council / future resource and consequence math control owner

## 1. Purpose and scope

This file creates the documentation/control owner scaffold for RT-002, the resource, backlash, corruption, strain, and consequence math ownership track identified by `REMEDIATION-PRIORITY-LEDGER-001`. It exists to name the future owner boundary that must separate resource-state visibility, cost commitment, overcommitment pressure, backlash/corruption/strain routing, consequence events, reward/loss events, recovery events, backend validation, persistence, context-packet handoff, and narration.

This scaffold is planning/control only. It is owner scaffold only: no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no damage table implementation, no validator implementation, no generator implementation, no persistence writer implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

This scaffold does not choose final resource values, final cost formulas, final backlash severity rules, final corruption or strain rules, final recovery rules, final reward/loss rules, final event models, final schemas, validators, runtime code, generators, persistence writers, context-packet compilers, live-play behavior, training data, donor-content audit results, or canon promotion.

## 2. Remediation ledger linkage

`docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` ranks RT-002 as P0 because resource pools, overcommitment, backlash, corruption, strain, harm, reward, and consequence outputs recur across combat, abilities, hazards, missions, and command lifecycle findings. The ledger recommends PR-B as the safe next owner-scaffold step: create resource/consequence and combat/hazard owner scaffolds after PR-A lands, without choosing formulas, damage tables, recovery rules, or encounter runtime.

RT-002 remains blocked by missing final resource/cost math, missing consequence event model, missing runtime state persistence owner, and future validator readiness. It depends on RT-001 command lifecycle/action legality/cost commitment boundaries and RT-011 validation/readiness tooling boundaries.

## 3. Dependency on RT-001 and RT-011

RT-002 depends on `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` because resource spending, refunding, overcommitment, rollback, and consequence commitment must be tied to a backend-owned command lifecycle and cannot be narrated into existence.

RT-002 depends on `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` because prose readiness is not executable validation. Any later resource math, consequence event model, schema, or validator must pass separately authorized readiness controls before runtime, live-play, training, canon, generator, persistence, or context-packet claims are made.

## 4. Audit-source linkage

This scaffold links to these accepted audit sources without expanding, correcting, or implementing their findings:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, which establishes backend-first audit procedure, no-implementation boundaries, and the requirement that LLM narration/proposal remain separate from backend authority.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, which records A13, C03, C09, and SM00 pressure around consequence, ability/effect, hazard, and math/runtime gaps.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`, which records A10 resource/cost/backlash/corruption pressure, B02 cost commitment lifecycle pressure, C07 mission consequence pressure, and D02 draft-source cost-commitment pressure.

## 5. Source pressure

The future RT-002 owner must account for pressure from actual repo sources while preserving each source's current authority limits:

- A10: `docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md` supplies resource taxonomy, cost/constraint, reserve/cooldown/recharge/regeneration, backlash, corruption, overload, heat/stress, strain/fatigue, debt, sacrifice, favor/disfavor, and recovery pressure. A10 is doctrine-draft material and does not define runtime resource values, runtime cooldown state, or runtime corruption state.
- A13: `docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md` supplies damage, injury, death, recovery, hazard, consequence propagation, corruption consequence, and cascading consequence pressure. A13 is doctrine-draft material and does not define runtime conflict, injury, hazard, hidden-information, or event-commit state.
- B02: `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` supplies action declaration, visible cost/risk preview, cost acceptance, cost commitment, resolution triggering, rollback/cancel/interrupt, and action-to-delta handoff pressure without final mechanical implementation.
- C03: `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` supplies ability/power/technique cost, prerequisite, cooldown, effect-binding, and activation pressure without final runtime schema authority.
- C07: `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` supplies mission/scenario/adventure reward, loss, consequence, hidden fact, objective, escalation, and scenario-state pressure without runtime consequence authority.
- C09: `docs/doctrine/schema/C09_hazard_environment_record_schema.md` supplies hazard/environment exposure, mitigation, consequence, visibility, and record-shape pressure without hazard runtime or final damage math.
- SM00: `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` supplies schema/math/mechanics sequencing pressure and explicitly separates planning from final schemas, exact math, runtime schemas, backend/database contracts, entity/component/event schemas, command lifecycles, context packets, and save-state shapes.
- D02 draft-source material: `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-03_cost_commitment_overinvestment_and_success_at_cost.md` exists in the repo and may exert design pressure on cost commitment, over-investment, and success-at-cost discussions only. It is not current runtime authority, canon, live-play behavior, training data, or promoted D-series doctrine.

## 6. Owner responsibilities

The future RT-002 owner is responsible for planning and later coordinating, in separately authorized PRs, owner decomposition for:

- resource/cost math ownership and the conditions under which any numeric formula can be proposed;
- resource pool, reserve/buffer, cooldown/recharge/regeneration, overcommitment, and refund/rollback boundaries;
- backlash, corruption, strain, overload, heat/stress, debt, sacrifice, favor/disfavor, harm, reward, loss, and recovery consequence-family routing;
- consequence event model ownership and event commitment boundaries;
- backend-owned validation before persistent state changes;
- context-packet contents after backend resource/consequence decisions are committed;
- narration handoff rules that permit describing committed outcomes but not deciding or mutating state;
- tests proving the LLM cannot choose costs, spend/refund resources, determine severity, apply corruption/strain, apply damage/healing/recovery, grant rewards/losses, commit consequences, convert narration to state deltas, invent formulas, or override validators.

## 7. Must-not-own boundaries

This scaffold and the future RT-002 owner must not own or claim to complete:

- final resource values;
- final resource/cost formulas;
- final backlash, corruption, strain, damage, healing, recovery, reward, or loss rules;
- final consequence event model;
- final command IR fields;
- final JSON schemas, database schemas, backend schemas, or condition schemas;
- executable validators;
- runtime implementation or state-machine code;
- combat runtime, hazard runtime, or encounter runtime;
- generators or generator prompts;
- persistence writer implementation;
- context-packet compiler implementation;
- donor-content audit;
- D-series source-material promotion;
- live-play authorization;
- training-data authorization;
- canon promotion.

## 8. Resource/consequence families as conceptual placeholders only

The following names are planning placeholders for discussion and test targeting only:

- resource_pool_state
- reserve_or_buffer_state
- cost_commitment_event
- overcommitment_marker
- backlash_event
- corruption_state
- strain_state
- consequence_event
- recovery_event
- reward_or_loss_event

These names are conceptual placeholders only. They are not final schemas, not final formulas, not runtime state, not event model implementation, not executable validation, not command IR, not persistence contracts, not context-packet compiler output, and not live-play authorization. They only identify seams that later owner work must resolve through separately authorized PRs.

## 9. Required future outputs

Future PRs, after this scaffold, must separately authorize and produce:

- resource/cost owner specification;
- consequence event owner specification;
- resource, reserve, overcommitment, backlash, corruption, strain, consequence, recovery, reward, and loss terminology matrix;
- math-readiness and benchmark plan before formulas are selected;
- schema/readiness handoff plan for any future record or state shape;
- validator family specification for cost, resource, and consequence transitions;
- persistence/event audit expectations;
- context-packet and narration handoff contract;
- tests proving backend authority over every resource and consequence state change;
- decision records for any movement from owner-scaffold planning to implementation.

## 10. Dependency relationships

RT-002 consumes RT-001 command lifecycle boundaries for cost commitment, refund/rollback, resolution triggering, and event commitment. RT-002 supports RT-003 combat/hazard/damage/recovery by providing future resource, consequence, damage-adjacent, strain, recovery, reward, and loss ownership once separately authorized. RT-002 relies on RT-011 so that future prose controls are not mistaken for validators or runtime gates. RT-002 also coordinates with future runtime state/event, persistence, schema/math/mechanics, context-packet, and generator-readiness owners without implementing those workstreams in this file.

## 11. LLM non-authority rules

RT-002 prohibits the LLM from:

- choosing resource costs;
- spending or refunding resources;
- deciding backlash severity;
- applying corruption or strain;
- determining damage, healing, or recovery;
- granting rewards or losses;
- committing consequence events;
- converting narration into state deltas;
- inventing formulas;
- overriding backend validators.

The LLM may only propose phrasing, ask clarifying questions, or narrate backend-committed outcomes when a future authorized context packet supplies those outcomes. It cannot be the authority for resource, cost, consequence, or recovery state.

## 12. Context-packet and narration handoff expectations

Future RT-002 context packets must be backend-produced after validation and event commitment. They must distinguish visible committed facts, pending clarifications, redacted hidden state, allowed narration emphasis, prohibited inference, and audit/event identifiers. Narration may describe committed resource or consequence outcomes but must not calculate costs, add refunds, change severity, apply corruption/strain, grant rewards/losses, invent recovery, or turn prose into state deltas.

This scaffold does not create a context-packet compiler, packet schema, event schema, validator, persistence writer, or narration generator.

## 13. First-test expectations

The first RT-002 tests should remain focused and non-brittle. They should verify this owner scaffold exists, references RT-002 and `REMEDIATION-PRIORITY-LEDGER-001`, links AUDIT-001/AUDIT-WAVE1-001/AUDIT-WAVE2-001, references RT-001 and RT-011, records source pressure from A10/A13/B02/C03/C07/C09/SM00/D02, includes explicit non-implementation guardrails, names only conceptual placeholders, and prohibits LLM authority over costs, spend/refund, backlash, corruption/strain, damage/healing/recovery, rewards/losses, consequences, narration-to-state conversion, formulas, and backend validators.

## 14. Explicit non-implementation statement

This RT-002 owner scaffold is documentation/control planning only. It implements no doctrine rewrite, runtime, schema, command IR, math, damage table, recovery formula, consequence event model, validator, generator, persistence writer, context-packet compiler, live-play adapter, training data, donor-content audit, D-series promotion, or canon promotion.
