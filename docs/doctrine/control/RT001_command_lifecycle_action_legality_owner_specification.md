# RT-001 Command Lifecycle / Action Legality / Cost Commitment Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification only
Tracking ID: REMEDIATION-STAGE2-RT001-COMMAND-LIFECYCLE-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-A
Remediation track: RT-001-command-lifecycle-action-legality
Owner: Astra Doctrine Council / future command lifecycle control owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-001. It upgrades `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` from owner scaffold into a specification-level planning artifact for command lifecycle, action legality, and cost commitment ownership.

This artifact remains non-executable and non-implementation. It defines planning-level ownership seams, handoffs, and guardrails only; it does not authorize runtime implementation, schema implementation, command IR implementation, validator implementation, generator implementation, persistence writer implementation, context-packet compiler implementation, live-play prompt implementation, training authorization, donor-content audit, or canon promotion.

This specification follows the Stage 2 plan in `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`, which tracks `REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001` and recommends exactly one next PR: `STAGE2-PR-A` for RT-001 owner-specification planning. It also preserves the remediation priority ordering in `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` (`REMEDIATION-PRIORITY-LEDGER-001`) and the accepted audit-source guardrails in `AUDIT-001`, `AUDIT-WAVE1-001`, and `AUDIT-WAVE2-001`.

## 2. Source basis and actual-file posture

This specification was prepared from actual repo sources only. The source set includes:

- `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` (`AUDIT-001`).
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md` (`AUDIT-WAVE1-001`).
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md` (`AUDIT-WAVE2-001`).
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` (`REMEDIATION-PRIORITY-LEDGER-001`).
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md` (`REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001`).
- `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md`.
- `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` through `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md`.
- `docs/doctrine/astra_doctrine_roadmap_v0_1.md` and `docs/doctrine/astra_doctrine_registry_v0_1.yaml`.
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md`, present at review time.
- `docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md`, present at review time.
- `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md`, present at review time.
- `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`, present at review time.
- `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`, present at review time.
- `README.md` for backend-first, deterministic runtime, and model-interchangeability posture.

No referenced required source path was found absent during this Stage 2 PR-A pass. This file does not rewrite B02, A10, SM00, SM01, SM02, the RT-001 scaffold, or any downstream owner scaffold.

## 3. Scope: what RT-001 owns

RT-001 owns the planning-level command lifecycle spine from player intent through backend handoff for validation, event commitment, context update, and narration. Specifically, RT-001 owns these boundaries:

1. player intent intake boundary: recognizing that a player has expressed an intent while preserving that the player provides intent, not direct state mutation;
2. raw input capture boundary: requiring a later backend-owned record of received input before any parser, proposal, or narration can claim command provenance;
3. LLM intent-proposal boundary: allowing the LLM to parse, summarize, or propose intent only as non-authoritative candidate material;
4. clarification-needed boundary: routing ambiguity to clarification instead of allowing narration to invent missing authority, target, cost, or timing facts;
5. candidate command proposal boundary: separating a proposed command from legality, cost commitment, resolution, validation, event commit, and narration;
6. backend action-legality decision boundary: preserving backend ownership of legal/illegal command decisions;
7. target, scope, authority, and capability check requirements: requiring later explicit checks for actor authority, target legality, scene scope, timing, subsystem jurisdiction, capability, access, prerequisites, and hidden-state constraints;
8. cost-declaration timing: defining when knowable costs or risk/cost options must be declared before commitment;
9. cost-commitment timing: defining the lifecycle point at which the backend commits accepted costs while leaving formulas and values to RT-002;
10. rollback, cancel, and interrupt requirement boundaries: requiring future owner decisions for cancellation, refund, rollback, interruption, partial resolution, and failed-command cost outcomes;
11. resolution-trigger boundary: separating cost commitment from later combat, hazard, ability, mission, social, inventory, RNG, table, or oracle resolution;
12. state-delta validation handoff: requiring proposed state deltas to route to future validation/readiness controls before acceptance;
13. event-commit handoff: requiring backend-owned event commitment after validation and before authoritative narration;
14. context-packet and narration handoff: requiring downstream visible context and narration packets after backend commitment, except for clearly labeled proposals or clarifications;
15. command rejection and quarantine handoff: requiring illegal, ambiguous, unsupported, or doctrine/runtime-blocked commands to reject, clarify, or quarantine without mutating state;
16. auditability requirements: preserving traceability from raw input through proposals, legality checks, cost decisions, validation, event commitment, rejection, quarantine, context updates, and narration packets.

## 4. Must-not-own boundaries

RT-001 must not own or claim to complete:

- final resource formulas;
- backlash, corruption, or strain math;
- combat damage math;
- ability effect math;
- final item or inventory state;
- final RNG implementation;
- final mission, social, or faction state;
- final generated-content persistence;
- final hidden-information redaction algorithm;
- final validation executable implementation;
- database schema;
- command IR implementation;
- runtime code;
- live-play prompts;
- training data;
- canon promotion.

RT-001 also must not create final schemas, final fields, final state-machine code, database tables, persistence writers, retrieval indexes, context-packet compilers, event ledger implementation, RNG/dice/table logic, donor-content audit results, or sourcebook/canon promotion decisions.

## 5. Authority model

The authority split for RT-001 is backend-first and model-interchangeable:

- The player provides intent, choices, and clarifications; the player does not directly mutate authoritative runtime state through free text.
- The LLM may parse intent, propose candidate commands, ask clarification questions, and narrate visible results only within backend-provided packets or clearly labeled non-authoritative proposal/clarification contexts.
- The backend owns action legality, target legality, cost commitment, RNG/table/oracle trigger authority, resolution trigger selection, validation routing, state-delta acceptance, event commitment, rejection/quarantine status, and handoff packets.
- Narration is downstream of backend commitment unless explicitly labeled as proposal or clarification. Narration cannot turn an uncommitted proposal into an event, cannot silently refund or spend costs, and cannot mutate state.

## 6. Conceptual lifecycle contract

The following lifecycle terms are conceptual placeholders only. They are not final IR, not a final runtime state machine, not executable code, not schema, not command IR implementation, not validator logic, and not runtime code. They exist to define semantic coverage that later owner specifications, schemas, validators, and runtime code must address only after separate authorization.

- `raw_input_received`: player input or other authorized input has been captured for later provenance.
- `intent_parse_proposed`: a non-authoritative parser or LLM proposal has described possible intent.
- `clarification_required`: ambiguity or missing required information prevents safe candidate-command preparation.
- `candidate_command_prepared`: a candidate command exists but is not legal, committed, validated, or event-backed.
- `command_scope_declared`: proposed command scope, actor, timing, target class, subsystem, and authority surface have been identified for backend review.
- `actor_authority_checked`: backend-owned actor authority review is required or has conceptually occurred.
- `target_legality_checked`: backend-owned target/scope/timing legality review is required or has conceptually occurred.
- `capability_or_access_checked`: backend-owned capability, access, prerequisite, cooldown, permission, tool, or environmental access review is required or has conceptually occurred.
- `cost_options_declared`: knowable costs, risk/cost options, or overcommitment options have been exposed before commitment where applicable.
- `cost_commitment_pending`: a backend-owned cost decision is pending and narration may not imply that costs are spent, refunded, or waived.
- `costs_committed`: backend authority has committed accepted costs or explicit failed-command cost outcomes for later validation and event handling.
- `resolution_trigger_selected`: backend authority has selected the appropriate downstream resolution path.
- `rng_or_table_dependency_declared`: RNG/table/oracle dependency has been declared for RT-009 handoff without implementing random selection.
- `proposed_state_delta_prepared`: a non-accepted proposed state delta exists for future validation handoff.
- `state_delta_validation_required`: proposed state change must be checked by future RT-011 validation/readiness controls before acceptance.
- `event_commit_required`: a backend-owned event commit is required before authoritative narration or durable state claim.
- `context_packet_update_required`: committed outcome visibility must be routed through RT-005 context-packet and hidden-information controls.
- `narration_packet_prepared`: visible, committed, backend-packeted outcome can be narrated without becoming state authority itself.
- `command_rejected`: illegal or unsupported command path ends without state mutation or event commitment, except for explicit backend-owned rejection records in future work.
- `command_quarantined_pending_doctrine_or_runtime`: command cannot be resolved safely because doctrine, runtime, validation, schema, or owner boundaries are missing; it remains non-mutating until separately resolved.

A future implementation may rename, split, combine, or replace these placeholders, but it must preserve the backend-first command/event boundary, LLM non-authority, cost-commitment boundary, validation handoff, and context/narration handoff described here.

## 7. Cost commitment contract

At planning level, RT-001 owns the lifecycle point at which cost commitment happens, while RT-002 owns cost math, resource formulas, consequence math, backlash, corruption, strain, refund math, and related quantitative doctrine.

The RT-001 cost commitment contract is:

1. costs must be declared before commitment when knowable;
2. optional overcommitment must be backend-authorized before commitment and may not be invented by narration;
3. committed costs cannot be silently refunded, waived, re-priced, or re-spent by narration;
4. failed commands require explicit cost outcome handling instead of implicit refund, implicit spend, or narrative erasure;
5. cancellation, rollback, interruption, partial-resolution, and refund behavior require future owner decisions and may not be assumed here;
6. cost commitment must occur before downstream resolution claims that depend on committed cost, unless a future owner explicitly defines a safe exception;
7. cost-related state deltas must route to future validation and event-commit handoffs before becoming authoritative.

This specification does not define final cost formulas, final resource names, final values, final refund mechanics, final consequence math, or executable cost validators.

## 8. Action legality contract

At planning level, RT-001 owns the legality decision boundary and the required handoff points; it does not implement legality checks.

The RT-001 action legality contract is:

1. action legality must be backend-owned;
2. target legality must be backend-owned;
3. legality requires actor authority, target identity or target class, command timing, capability/access/prerequisite status, scene state, hidden-state constraints, and subsystem handoff checks;
4. legality checks must account for downstream owners when the command pressures resources, combat, abilities, context packets, missions, social state, generated content, RNG/table/oracle use, inventory/assets, validation, or D-series/native-design promotion boundaries;
5. illegal commands produce rejection, clarification, or quarantine rather than state mutation;
6. unsupported commands produce quarantine or clarification when doctrine/runtime/validation ownership is missing;
7. the LLM may not “make it work” through narration, invented permission, invented targets, hidden modifiers, uncommitted costs, uncommitted random outcomes, or unvalidated state deltas.

## 9. Command/event boundary

RT-001 defines the planning boundary between command proposal and event commitment:

- command proposal is not event commitment;
- validation is not commitment;
- narration is not commitment;
- cost declaration is not cost commitment;
- cost commitment is not complete event commitment unless later backend event logging accepts it;
- event commitment requires future backend-owned event logging, replay/audit expectations, and persistence routing;
- rejected commands must not mutate state;
- quarantined commands must not mutate state;
- future state, event, validation, persistence, and context-packet work must consume this boundary;
- this specification does not define final event schema, event ledger implementation, database schema, or persistence writer behavior.

## 10. Future IR inventory: semantic requirements only

The following future IR families are semantic requirements only. They are not implemented schemas, not final fields, not classes, not JSON schema, not database schema, not Pydantic models, not executable validators, not runtime code, and not final CommandIR.

| Future IR family | Purpose | Backend owner | LLM allowed interaction | Downstream owner handoff | Implementation status |
|---|---|---|---|---|---|
| RawInputRecord | Preserve received input provenance before parsing or proposal. | Backend command lifecycle owner. | May provide the visible text it received but cannot declare provenance authority. | RT-011 for validation/readiness; future persistence/event owner. | future_required_not_implemented |
| IntentProposal | Represent a non-authoritative parse or interpretation of player intent. | Backend command lifecycle owner. | May draft or revise as proposal only. | RT-005 for visible clarification context; RT-011 for non-authority validation. | future_required_not_implemented |
| ClarificationRequest | Ask for missing or ambiguous information before command preparation. | Backend command lifecycle owner. | May phrase the question inside backend constraints. | RT-005 for visible context; RT-007 if actor/social knowledge matters. | future_required_not_implemented |
| CandidateCommand | Hold proposed actor/action/target/scope/timing before legality or commitment. | Backend command lifecycle owner. | May propose candidate content only as non-authoritative draft. | RT-002 through RT-010 according to subsystem pressure; RT-011 for readiness. | future_required_not_implemented |
| ActorAuthorityCheck | Determine whether the actor may attempt or declare the command. | Backend command lifecycle owner. | No authority; may restate visible result after backend packet. | RT-007 for actor knowledge/social authority; RT-011 for validation. | future_required_not_implemented |
| TargetLegalityCheck | Determine whether target, timing, scope, and scene constraints allow the action. | Backend command lifecycle owner. | No authority; may ask clarification if backend requests. | RT-003, RT-005, RT-006, RT-007, RT-010 as applicable. | future_required_not_implemented |
| CapabilityAccessCheck | Determine capability, prerequisite, access, cooldown, permission, and tool availability. | Backend command lifecycle owner. | No authority; may summarize visible blockers after backend packet. | RT-004 for abilities/skills; RT-010 for assets; RT-011 for validation. | future_required_not_implemented |
| CostCommitmentRecord | Mark the lifecycle point for declared and accepted costs or failed-command cost outcomes. | Backend command lifecycle owner for timing; RT-002 for math. | No spending/refunding authority; may narrate committed visible outcome. | RT-002 for resource/consequence math; RT-011 for validation. | future_required_not_implemented |
| ResolutionTriggerRecord | Route committed commands to the appropriate downstream resolution owner. | Backend command lifecycle owner. | No resolution authority; may narrate only after backend result. | RT-003, RT-004, RT-006, RT-007, RT-009, RT-010 as applicable. | future_required_not_implemented |
| RandomnessDependencyRecord | Declare that RNG/table/oracle authority is needed without selecting the result. | Backend command lifecycle owner for trigger; RT-009 for RNG/table/oracle. | No random-result authority; may not roll or choose as authority. | RT-009 for seed/table/oracle authority; RT-005 for hidden-result visibility. | future_required_not_implemented |
| ProposedStateDelta | Represent non-accepted state changes pending validation. | Backend command lifecycle owner until handoff. | May not prepare or accept as authority; may only describe backend-visible proposal if allowed. | RT-011 for validation; future state/event/persistence owners. | future_required_not_implemented |
| ValidationResult | Represent validation outcome before event commitment. | RT-011 validation/readiness owner. | No validation authority; may summarize visible validation result after backend packet. | RT-001 for command continuation; future event owner. | future_required_not_implemented |
| EventCommitReference | Link accepted command resolution to future backend event logging. | Future backend event/state owner with RT-001 boundary requirements. | No event authority; may narrate committed result after backend packet. | Future persistence/event owner; RT-005 for context update. | future_required_not_implemented |
| RejectionRecord | Preserve non-mutating illegal or unsupported command rejection reason. | Backend command lifecycle owner. | May explain visible rejection reason within backend packet. | RT-011 for validation; RT-005 for player-facing context. | future_required_not_implemented |
| QuarantineRecord | Preserve non-mutating unresolved command pressure pending doctrine/runtime review. | Backend command lifecycle owner. | May explain that resolution is pending, not invent outcome. | RT-011 for readiness; RT-012 if source-pack pressure exists; relevant RT owner. | future_required_not_implemented |
| NarrationPacketReference | Link committed visible outcome to narration without making narration authority. | Backend context/narration handoff owner with RT-005 coordination. | May render visible narration exactly within backend packet constraints. | RT-005 for context packet/hidden information; future narration validators. | future_required_not_implemented |

## 11. Validation and readiness requirements

The following are future validation requirements only. They coordinate with RT-011 but do not implement validators, executable checks, schema tests, runtime state-machine checks, or command IR validators in this PR.

- file/registry tracking validation must verify that this owner specification, registry entry, and decision-log entry stay aligned;
- lifecycle-state coverage validation must verify that future implementations cover required RT-001 lifecycle seams or explicitly replace them;
- LLM non-authority validation must fail any flow where LLM prose decides legality, spends/refunds resources, commits costs, commits state, reveals hidden information, or treats narration as memory authority;
- cost-commitment boundary validation must distinguish cost declaration, cost commitment, failed-command cost outcome, and downstream math ownership;
- command/event boundary validation must distinguish proposal, validation, event commit, context update, and narration;
- downstream dependency validation must ensure RT-002 through RT-012 handoffs are present when their subsystem pressure appears;
- non-implementation guardrail validation must detect claims that this planning artifact provides runtime, schema, command IR, validator, generator, persistence writer, retrieval index, context-packet compiler, RNG/dice/table system, event ledger, database schema, live-play prompt, training behavior, donor-content audit, or canon authority.

## 12. Downstream handoffs

RT-001 must hand off ownership pressure as follows:

- RT-002: resource, cost, backlash, strain, corruption, refund, overcommitment consequence, reward/loss, and consequence math.
- RT-003: combat, hazard, damage, injury, recovery, active-threat, and tactical/encounter resolution.
- RT-004: abilities, effects, skills, capabilities, prerequisites, cooldowns, bindings, and capability/access semantics.
- RT-005: context-packet visibility, hidden-information partitioning, narration handoff, and player-visible packet constraints.
- RT-006: mission, reward, clue, hidden-truth, scenario, and progress-routing consequences.
- RT-007: social, faction, relationship, actor knowledge, institutional state, and authority/standing checks.
- RT-008: generated content persistence, provenance, recurrence eligibility, generated-record durability, and generated-content status.
- RT-009: RNG, dice, table, oracle, seed, replay, hidden-result, and random-dependency authority.
- RT-010: inventory, item, gear, vehicle, platform, asset, custody, loadout, charge, durability, cargo, crew, and persistent asset state.
- RT-011: validation, readiness controls, registry/file tracking checks, non-authority assertions, and future executable validators.
- RT-012: D-series/native-design promotion boundaries when source-pack material pressures runtime behavior, costs, command legality, narration, sourcebook inclusion, training use, or canon status.

## 13. LLM non-authority rules

The LLM is explicitly prohibited from:

- deciding action legality;
- deciding target legality;
- deciding hidden modifiers;
- spending or refunding resources;
- committing costs;
- triggering RNG, dice, table, or oracle results as authority;
- resolving combat, hazards, abilities, missions, social state, or inventory as mechanical truth;
- preparing or accepting state deltas as authority;
- committing events;
- writing persistence records;
- compiling context packets;
- revealing hidden information;
- treating narration as backend commitment;
- treating summaries as memory authority;
- authorizing canon, sourcebook, donor-content, or training use.

The LLM may only parse, propose, ask clarification, and narrate within backend packets or clearly labeled proposal/clarification contexts.

## 14. Non-implementation reaffirmation

This Stage 2 PR-A owner specification adds no:

Guardrail phrase summary: no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no RNG/dice/table implementation, no event ledger implementation, no database schema, no live-play prompt implementation, no training authorization, no donor-content audit, and no canon promotion.

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
- live-play prompt;
- training data;
- donor-content audit;
- canon promotion.

It also adds no final CommandIR, final schema fields, database tables, state-machine code, executable legality checks, cost formulas, random table data, event ledger, persistence writer, context-packet compiler, retrieval index, live-play prompts, training examples, donor PDF/book audit, sourcebook promotion, or canon promotion.

## 15. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-A
  track: RT-001
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_canon_promotion: false
  next_allowed_step: RT-011 owner specification or RT-002 owner specification, pending review
```
