# RT-002 Resource / Consequence Math Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification only
Tracking ID: REMEDIATION-STAGE2-RT002-RESOURCE-CONSEQUENCE-MATH-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-C
Remediation track: RT-002-resource-backlash-consequence-math
Owner: Astra Doctrine Council / future resource and consequence math control owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-002. It upgrades `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` into a specification-level planning artifact for resource, cost, backlash, corruption, strain, reward/loss, recovery-cost, repair-cost, and consequence-math governance.

This specification remains non-executable and non-implementation. It does not create formulas, values, resource pools, damage tables, reward economies, schemas, command IR, runtime code, validators, generators, persistence writers, retrieval indexes, context-packet compilers, live-play prompts, training data, donor-content audits, sourcebook authorization, pilot conversion authorization, or canon promotion.

This specification links to and relies on the following actual repo artifacts:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- RT002 owner scaffold: `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md`.
- RT001 owner specification: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- RT011 owner specification: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.

### Source availability disclosure

All requested planning, audit, current RT owner, resource/math/source pressure, and runtime/project authority source files were present at drafting time. No requested path was absent, and no substitute path was used.

## 2. Scope

RT-002 owns planning-level governance for resource/consequence math boundaries. Ownership means defining future math artifact requirements, authority seams, handoff obligations, validation requirements, and LLM non-authority rules. Ownership does not mean implementing any formula, value, pool, event, validator, schema, or runtime system.

RT-002 owns the following planning boundaries:

- resource/cost/consequence math ownership boundaries;
- cost-family classification requirements;
- the cost declaration versus cost commitment handoff received from RT-001;
- failed-command cost outcome requirements;
- optional overcommitment math boundary requirements;
- resource spend, refund, loss, recovery, and repair math requirements;
- backlash, corruption, strain, instability, exhaustion, debt, obligation, and consequence pressure boundaries;
- reward, loss, and economy pressure boundaries;
- recovery-cost and repair-cost math boundaries;
- damage/injury resource pressure handoff to RT-003;
- ability/effect cost handoff to RT-004;
- mission reward/consequence handoff to RT-006;
- social/faction obligation and debt handoff to RT-007;
- generated-content cost/provenance handoff to RT-008;
- RNG/table dependency handoff to RT-009;
- inventory/item/vehicle spend and asset-loss handoff to RT-010;
- validation/readiness handoff to RT-011;
- auditability requirements for future cost, resource, consequence, reward/loss, and recovery decisions.

The owner specification must preserve pressure from A10, A13, B02, C03, C07, C09, C12, SM00, SM01, SM02, the registry, current decisions log, and README backend-first/model-interchangeability posture without converting those sources into final mechanics.

## 3. Must-not-own boundaries

RT-002 must not own, create, imply, or claim completion of:

- final resource formulas;
- final resource names or final resource pool list;
- final cost values;
- final refund rules;
- final backlash, corruption, or strain formulas;
- final damage tables;
- final healing or recovery formulas;
- final reward economy;
- final item prices or crafting values;
- final mission rewards;
- final social/faction obligation mechanics;
- final RNG implementation;
- schema implementation;
- command IR implementation;
- runtime code;
- validator implementation;
- generator implementation;
- persistence writer implementation;
- context-packet compiler implementation;
- retrieval index implementation;
- live-play prompts;
- training data;
- donor-content audits;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion.

Any future PR that attempts those outputs must receive separate authorization and must not cite this owner specification as implementation authority.

## 4. Authority model

RT-002 authority is semantic planning authority only:

- RT-001 owns when costs are declared, previewed, accepted, committed, rejected, cancelled, interrupted, or handed into resolution/state-delta routing.
- RT-002 owns what future math families are required to make costs, consequences, refunds, rewards, losses, recovery, repair, and resource-state deltas lawful.
- RT-011 owns validation/readiness requirements, readiness labels, non-implementation guardrail checks, reviewer decision records, and future validator requirement governance.
- Future backend runtime owners, once separately authorized, must own all cost calculation, resource spend/refund/loss/recovery, consequence math, reward/loss math, repair math, recovery math, and durable state/event commitment.
- The LLM may only summarize visible backend-approved cost/consequence outcomes. It may not decide, calculate, commit, refund, repair, recover, reward, penalize, remember, or persist resource/consequence state.

## 5. Resource/consequence family contract

The following conceptual families are planning placeholders only. They are future semantic requirement labels, not formulas, not final resource pools, not schema fields, not runtime state, not event records, not validators, not database rows, not table implementations, and not live-play rules.

| Conceptual family | Planning purpose | Implementation posture |
|---|---|---|
| `resource_pool_pressure` | Identifies pressure that a future resource pool or state dimension may be needed. | Planning placeholder only. |
| `committed_cost_pressure` | Identifies pressure for auditable cost commitment after RT-001 timing authority. | Planning placeholder only. |
| `failed_command_cost_outcome` | Identifies the need for explicit future rules when a command fails, is rejected, interrupted, cancelled, or partially resolves. | Planning placeholder only. |
| `optional_overcommitment_pressure` | Identifies pressure for future overcommitment, overinvestment, overload, or success-at-cost decisions. | Planning placeholder only. |
| `refund_or_no_refund_pressure` | Identifies pressure for future refund/no-refund policy without assuming refunds. | Planning placeholder only. |
| `backlash_pressure` | Identifies pressure for future backlash severity, timing, stacking, and recovery decisions. | Planning placeholder only. |
| `corruption_pressure` | Identifies pressure for future corruption progression, thresholds, visibility, clearing, and recovery decisions. | Planning placeholder only. |
| `strain_pressure` | Identifies pressure for future strain, fatigue, exhaustion, stress, or load accumulation decisions. | Planning placeholder only. |
| `instability_pressure` | Identifies pressure for future instability, overload, volatility, misfire, or cascading consequence decisions. | Planning placeholder only. |
| `debt_or_obligation_pressure` | Identifies pressure for future social/faction/economic obligation or debt mechanics routed to RT-007. | Planning placeholder only. |
| `reward_pressure` | Identifies pressure for future reward, payout, clue, salvage, mission, or advancement reward requirements. | Planning placeholder only. |
| `loss_pressure` | Identifies pressure for future penalty, asset loss, item loss, mission loss, opportunity loss, or degradation requirements. | Planning placeholder only. |
| `recovery_cost_pressure` | Identifies pressure for future healing, recovery, downtime, clearing, or mitigation cost requirements. | Planning placeholder only. |
| `repair_cost_pressure` | Identifies pressure for future item, vehicle, platform, relic, implant, or asset repair cost requirements. | Planning placeholder only. |
| `crafting_or_salvage_cost_pressure` | Identifies pressure for future crafting, salvage, modification, upgrade, and conversion costs routed to RT-010. | Planning placeholder only. |
| `damage_or_injury_cost_pressure` | Identifies pressure for future damage, injury, harm, recovery, mitigation, and exposure costs routed to RT-003. | Planning placeholder only. |
| `asset_spend_or_degradation_pressure` | Identifies pressure for future ammo, charge, fuel, durability, cargo, crew, custody, requisition, or asset degradation requirements routed to RT-010. | Planning placeholder only. |
| `economy_pressure` | Identifies pressure for future prices, value, requisition, market, faction, crafting, salvage, or reward economy requirements. | Planning placeholder only. |
| `consequence_event_pressure` | Identifies pressure for future event/state-delta representation for consequences without implementing an event ledger. | Planning placeholder only. |

These family labels may be used in future planning prose and inventories to keep ownership seams visible. They must not be treated as final controlled vocabulary for schemas, JSON, database records, runtime state, validators, dice tables, prompts, or sourcebook rules.

## 6. Cost outcome contract

Future cost outcomes must satisfy the following planning-level requirements before runtime readiness can be claimed:

- declared costs must be distinguishable from committed costs;
- committed costs must be auditable and attributable to a backend-owned command lifecycle/state-delta path;
- failed commands must have an explicit future cost-outcome rule rather than relying on narration or implicit refund assumptions;
- rejection, cancellation, interruption, rollback, partial success, success-at-cost, failure-at-cost, and overcommitment must each be routed to future RT-002 math decisions where cost/resource effects are possible;
- refunds must never be assumed by narration, summary text, LLM memory, or source prose;
- costs attached to hidden information require RT-005 redaction and visibility handling before any player-facing summary;
- costs driven by random tables, dice, oracles, loot rolls, encounter tables, or hidden random results require RT-009 authority;
- durable resource changes require future state/event/persistence owners before they can become runtime facts;
- visible cost previews are not resource-state mutations until the authorized backend owner commits the state delta;
- future cost artifacts must preserve source linkage and decision lineage for auditability.

This contract does not define final refund rules, final success-at-cost formulas, final overcommitment math, final rollback behavior, final cost values, final resource pools, or final command IR.

## 7. Backlash/corruption/strain/consequence contract

Backlash, corruption, strain, instability, exhaustion, debt, obligation, reward, loss, recovery, repair, and consequence outcomes are backend-owned when they affect runtime state.

Planning-level consequence requirements:

- qualitative consequence labels are not enough for runtime readiness;
- consequence severity, thresholds, duration, stacking, recovery, clearing, escalation, decay, visibility, persistence, and audit lineage require future math/spec work;
- conditions or persistent effects must route to RT-003, RT-004, or RT-010 as applicable;
- combat, hazard, damage, injury, exposure, recovery, mitigation, and healing pressures route to RT-003;
- ability, effect, skill, cooldown, prerequisite, advancement-linked, and activation pressures route to RT-004;
- inventory, item, vehicle, asset, ammo, charge, fuel, durability, repair, salvage, crafting, requisition, and asset-loss pressures route to RT-010;
- social/faction obligations, debts, reputation costs, relationship consequences, and institutional consequences route to RT-007;
- mission rewards, mission penalties, clue costs, loss states, scenario escalation, and scenario consequences route to RT-006;
- hidden consequences route through RT-005 visibility/redaction/context-packet boundaries;
- generated consequences require RT-008 if they create durable generated content, recurrence, provenance, identifiers, or promotion pressure;
- random consequence outcomes require RT-009 table/oracle/RNG authority;
- validators and readiness claims route through RT-011.

This contract does not define final thresholds, final tables, final formulas, final duration rules, final stacking rules, final clearing rules, final damage models, final recovery models, final reward models, or final event schemas.

## 8. Future math artifact inventory

The following future math artifact families are semantic requirements only. They are not implemented formulas, not final fields, not JSON schema, not database schema, not Pydantic models, not validator code, not runtime code, not prompts, and not sourcebook rules. Every listed artifact family has implementation status `future_required_not_implemented`.

| Future artifact family | Purpose | Owner | LLM allowed interaction | Downstream handoff | Implementation status |
|---|---|---|---|---|---|
| `CostFamilyInventory` | Inventory future cost/consequence families that must be classified before runtime use. | RT-002 owner with RT-011 readiness review. | May draft non-authoritative inventories from visible sources. | RT-001, RT-003, RT-004, RT-006, RT-007, RT-009, RT-010, RT-011. | `future_required_not_implemented` |
| `ResourcePoolRequirementInventory` | Identify where future resource pools or state dimensions may be required without naming final pools. | RT-002 owner. | May summarize pressure only. | Future backend state owner and RT-011. | `future_required_not_implemented` |
| `CostDeclarationRequirement` | Require declared costs to remain separable from committed costs. | RT-001 timing owner and RT-002 math owner. | May describe the boundary. | RT-001 and future command/state-delta owners. | `future_required_not_implemented` |
| `CostCommitmentRequirement` | Require committed costs to be auditable backend-owned state changes. | RT-001 and RT-002. | May summarize backend-approved outcomes only. | Future event/persistence owner and RT-011. | `future_required_not_implemented` |
| `FailedCommandCostOutcomeRequirement` | Require explicit future handling for failed, rejected, cancelled, interrupted, or partially resolved commands. | RT-002 with RT-001 lifecycle handoff. | May flag missing policy; may not choose outcome. | RT-001, future command IR, future runtime owner. | `future_required_not_implemented` |
| `OvercommitmentRequirement` | Require future math decisions for overcommitment, overinvestment, overload, or success-at-cost. | RT-002. | May identify source pressure; may not choose effects. | RT-001, RT-004, RT-009, RT-011. | `future_required_not_implemented` |
| `RefundPolicyRequirement` | Require explicit refund/no-refund policy rather than narrative assumption. | RT-002 with RT-001 timing. | May state that no refund is authorized absent backend approval. | Future runtime/event/persistence owner. | `future_required_not_implemented` |
| `BacklashSeverityRequirement` | Require future severity, timing, duration, stacking, and clearing semantics for backlash. | RT-002. | May summarize approved backend-visible outcome only. | RT-003, RT-004, RT-005, RT-011. | `future_required_not_implemented` |
| `CorruptionProgressionRequirement` | Require future progression, threshold, visibility, recovery, and clearing semantics for corruption. | RT-002. | May summarize visible approved state only. | RT-003, RT-004, RT-005, RT-007, RT-011. | `future_required_not_implemented` |
| `StrainAccumulationRequirement` | Require future strain/fatigue/exhaustion accumulation and recovery semantics. | RT-002. | May summarize visible approved state only. | RT-003, RT-004, RT-010, RT-011. | `future_required_not_implemented` |
| `InstabilityPressureRequirement` | Require future overload, volatility, cascade, misfire, or instability semantics. | RT-002. | May identify pressure; may not choose consequence. | RT-003, RT-004, RT-009, RT-011. | `future_required_not_implemented` |
| `RewardLossRequirement` | Require future reward, penalty, loss, economy, clue, mission, and asset-loss semantics. | RT-002 with domain owners. | May summarize backend-approved visible results. | RT-006, RT-007, RT-009, RT-010, RT-011. | `future_required_not_implemented` |
| `RecoveryCostRequirement` | Require future recovery, healing, clearing, downtime, mitigation, and restoration cost semantics. | RT-002 and RT-003. | May summarize visible approved recovery state. | RT-003, RT-004, RT-010, RT-011. | `future_required_not_implemented` |
| `RepairCostRequirement` | Require future repair, restoration, replacement, requisition, and maintenance cost semantics. | RT-002 and RT-010. | May summarize visible approved repair state. | RT-010 and RT-011. | `future_required_not_implemented` |
| `CraftingSalvageCostRequirement` | Require future crafting, salvage, modification, upgrade, material, and output cost semantics. | RT-002 and RT-010. | May identify pressure; may not set outputs or values. | RT-009, RT-010, RT-011. | `future_required_not_implemented` |
| `ConsequenceSeverityRequirement` | Require future severity, threshold, duration, stacking, recovery, clearing, and persistence semantics. | RT-002 with applicable RT domain owner. | May summarize approved visible consequences only. | RT-003, RT-005, RT-006, RT-007, RT-008, RT-011. | `future_required_not_implemented` |
| `ResourceStateDeltaRequirement` | Require future representation of durable resource deltas without implementing event ledgers or persistence. | RT-002 with future state/event/persistence owners. | May not commit state; may summarize backend-approved visible deltas. | RT-001, future event/persistence owner, RT-011. | `future_required_not_implemented` |
| `CostValidationRequirement` | Require future validation coverage for cost-family, declaration/commitment, failed-command, refund, and overcommitment boundaries. | RT-011 with RT-002 domain input. | May draft requirement prose only. | RT-011 and future validator owner. | `future_required_not_implemented` |
| `ConsequenceValidationRequirement` | Require future validation coverage for backlash, corruption, strain, reward/loss, recovery, repair, handoff, and non-authority boundaries. | RT-011 with RT-002 domain input. | May draft requirement prose only. | RT-011 and future validator owner. | `future_required_not_implemented` |

## 9. Validation and readiness requirements

RT-002 validation requirements are future requirements only. RT-011 coordinates readiness governance; this specification does not implement validators, test code, schemas, CI checks, Pydantic models, JSON schema, database schema, or runtime validation.

Future validation/readiness requirement families:

- source linkage validation: confirm RT-002 cost/consequence claims link to actual source files or disclose absences/substitutions;
- cost-family coverage validation: confirm every cost/consequence pressure routes to a conceptual family or is explicitly deferred/blocked;
- cost declaration/commitment boundary validation: confirm declared, previewed, accepted, committed, rejected, cancelled, interrupted, and rolled-back costs do not collapse into one state;
- failed-command outcome validation: confirm failed/rejected/cancelled/interrupted/partial commands have explicit future outcome requirements and do not assume refunds;
- refund/overcommitment boundary validation: confirm refunds and overcommitment effects are future math decisions, not narrative assumptions;
- backlash/corruption/strain/consequence coverage validation: confirm severity, duration, stacking, recovery, clearing, visibility, persistence, and handoff requirements are recorded as future work;
- reward/loss/recovery/repair coverage validation: confirm reward, penalty, loss, economy, recovery, repair, salvage, crafting, and asset-loss pressures route to the right owners;
- downstream handoff validation: confirm RT-001 through RT-012 handoffs are explicit and unresolved dependencies are labeled;
- LLM non-authority validation: confirm LLM outputs are not treated as cost/resource/consequence authority;
- non-implementation guardrail validation: confirm the artifact does not implement math, schemas, validators, runtime code, generators, persistence, retrieval, context packets, live-play prompts, training data, donor-content audits, sourcebook inclusion, pilot conversion, or canon promotion.

Readiness labels for unresolved RT-002 items must remain planning labels such as `future_required_not_implemented`, `blocked_pending_dependency`, `blocked_pending_review`, `deferred_to_runtime_phase`, `deferred_to_schema_or_validator_phase`, `deferred_to_canon_or_sourcebook_phase`, or `implementation_authorized_separately_only`.

## 10. Downstream handoffs

RT-002 must hand downstream pressure to the following owners without taking over their domain authority:

- RT-001: declaration/commitment timing, cost preview/acceptance, command lifecycle, rejection, cancellation, interruption, rollback, resolution trigger, and command/event handoff.
- RT-003: combat, hazard, damage, injury, recovery, healing, mitigation, exposure, active threat, and persistent harm consequences.
- RT-004: ability, effect, skill, prerequisite, activation, cost, cooldown, advancement-linked resource pressure, and effect binding.
- RT-005: hidden cost/consequence visibility, redaction, derived/withheld state, context-packet projection, narrator visibility, and hidden-truth boundaries.
- RT-006: mission reward, mission penalty, clue-cost, objective status, scenario progress, mission loss, and scenario consequence routing.
- RT-007: social/faction obligations, debts, reputation costs, relationship consequences, favor/disfavor, institutional consequences, and actor knowledge/standing effects.
- RT-008: generated-content cost, provenance, recurrence, durable-record eligibility, generated consequence persistence, stable identifiers, and promotion implications.
- RT-009: random cost, reward, loss, oracle, loot, table, dice, seed, replay, hidden random result, and table outcome dependencies.
- RT-010: inventory, item, vehicle, asset, ammo, charge, fuel, durability, cargo, crew, repair, salvage, crafting, requisition, custody, loadout, and asset-loss pressures.
- RT-011: validation/readiness governance, future validator requirements, readiness classifications, registry/file tracking, reviewer decision records, and non-implementation guardrails.
- RT-012: D-series/native-design pressure that proposes resource, cost, backlash, corruption, strain, consequence, reward, loss, recovery, repair, or economy mechanics.

## 11. LLM non-authority rules

The LLM is explicitly prohibited from:

- choosing resource costs;
- spending resources;
- refunding resources;
- deciding failed-command cost outcomes;
- choosing overcommitment effects;
- deciding backlash severity;
- applying corruption, strain, instability, exhaustion, debt, obligation, reward, or loss;
- determining damage, healing, recovery, repair, or crafting costs;
- setting prices, item values, mission rewards, or salvage outputs;
- treating narration as resource state;
- treating summaries as memory/resource authority;
- inventing formulas;
- overriding backend validators;
- committing consequence events;
- authorizing canon/sourcebook/training/live-play use.

The LLM may draft non-authoritative planning prose, summarize visible backend-approved outcomes, list actual source paths, identify apparent handoff gaps, and propose review questions. Those interactions are advisory only and do not become cost/resource/consequence authority.

## 12. Non-implementation reaffirmation

This PR adds no:

- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- generator implementation;
- persistence writer;
- retrieval index;
- context-packet compiler;
- RNG/dice/table implementation;
- event ledger implementation;
- database schema;
- resource formula;
- resource pool list;
- cost table;
- damage table;
- consequence table;
- recovery formula;
- repair formula;
- reward economy;
- item price list;
- crafting value list;
- mission reward table;
- live-play prompt;
- training data;
- donor-content audit;
- canon promotion;
- sourcebook inclusion authorization;
- pilot conversion authorization.

## 13. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-C
  track: RT-002
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_validator_implementation: false
  authorizes_math_implementation: false
  authorizes_resource_formula: false
  authorizes_cost_table: false
  authorizes_reward_economy: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_canon_promotion: false
  authorizes_pilot_conversion: false
  next_allowed_step: RT-005 owner specification or RT-003 owner specification, pending review
```
