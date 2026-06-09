# RUNTIME-DOMAIN-PR-3: Transaction Lifecycle and Event Commitment Service Plan

## 1. Purpose and status

This document is **RUNTIME-DOMAIN-PR-3**, a planning-only service plan for the future Transaction Lifecycle and Event Commitment service within the Astra Ascension runtime domain-service layer.

It follows **RUNTIME-DOMAIN-PR-2B** (State Store / State Projection Skeleton Review, merged as PR #260), which confirmed:

- PR-2A state store / state projection skeleton stayed within scope.
- The second domain package guardrail transition is safe.
- State store and state projection skeletons are stable enough for later domain-service planning.
- No PR-2C hardening is required before transaction lifecycle / event commitment planning.
- The next allowed step is RUNTIME-DOMAIN-PR-3.
- RUNTIME-DOMAIN-PR-3 must be planning-only.

**This PR authorizes only a future narrow implementation PR (RUNTIME-DOMAIN-PR-3A) after review.**

**This PR does not implement code.**

**Plan ID:** RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001

---

## 2. Source ledger

All source artifacts consulted for this plan:

| Artifact | ID | Role |
|---|---|---|
| RUNTIME-DOMAIN-PR-2B | RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001 | Gate source — authorized PR-3 |
| RUNTIME-DOMAIN-PR-2A | RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001 | State store / state projection skeleton implementation |
| RUNTIME-DOMAIN-PR-2 | RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001 | State store / state projection service plan |
| RUNTIME-DOMAIN-PR-1B | RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001 | Command lifecycle / action legality skeleton review |
| RUNTIME-DOMAIN-PR-1A | RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001 | Command lifecycle / action legality skeleton implementation |
| RUNTIME-DOMAIN-PR-1 | RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001 | Command lifecycle / action legality service plan |
| RUNTIME-DOMAIN-PR-0 | RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001 | Domain service implementation sequencing plan |
| RUNTIME-IMPL-PR-8 | RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001 | Post-kernel skeleton review / domain service readiness gate |

### Kernel skeleton modules consulted

| Module | Path |
|--------|------|
| schema_registry | `src/astra_runtime/kernel/schema_registry.py` |
| record_identity | `src/astra_runtime/kernel/record_identity.py` |
| command_envelope | `src/astra_runtime/kernel/command_envelope.py` |
| transaction_preview | `src/astra_runtime/kernel/transaction_preview.py` |
| state_delta | `src/astra_runtime/kernel/state_delta.py` |
| event_ledger | `src/astra_runtime/kernel/event_ledger.py` |
| rng_interface | `src/astra_runtime/kernel/rng_interface.py` |
| table_oracle | `src/astra_runtime/kernel/table_oracle.py` |
| validation_pipeline | `src/astra_runtime/kernel/validation_pipeline.py` |
| hidden_information | `src/astra_runtime/kernel/hidden_information.py` |
| context_projection | `src/astra_runtime/kernel/context_projection.py` |
| persistence_boundary | `src/astra_runtime/kernel/persistence_boundary.py` |
| replay_audit | `src/astra_runtime/kernel/replay_audit.py` |
| runtime_trace | `src/astra_runtime/kernel/runtime_trace.py` |

### Domain skeleton modules consulted

| Module | Path |
|--------|------|
| command_lifecycle | `src/astra_runtime/domain/command_lifecycle.py` |
| action_legality | `src/astra_runtime/domain/action_legality.py` |
| state_store | `src/astra_runtime/domain/state_store.py` |
| state_projection | `src/astra_runtime/domain/state_projection.py` |

### Runtime skeleton tests consulted

| Test | Path |
|------|------|
| test_domain_command_lifecycle_skeleton | `tests/runtime/test_domain_command_lifecycle_skeleton.py` |
| test_domain_action_legality_skeleton | `tests/runtime/test_domain_action_legality_skeleton.py` |
| test_domain_state_store_skeleton | `tests/runtime/test_domain_state_store_skeleton.py` |
| test_domain_state_projection_skeleton | `tests/runtime/test_domain_state_projection_skeleton.py` |

### Owner specifications consulted

| Spec ID | Title |
|---------|-------|
| RT-001 | Command lifecycle and action legality owner specification |
| RT-002 | Resource / consequence math owner specification |
| RT-003 | Combat / hazard / damage / recovery owner specification |
| RT-004 | Ability / effect / skill binding owner specification |
| RT-005 | Context packet and hidden information owner specification |
| RT-006 | Mission / reward / clue routing owner specification |
| RT-007 | Social / faction / actor knowledge owner specification |
| RT-008 | Generated content provenance and recurrence owner specification |
| RT-009 | Runtime RNG and table/oracle owner specification |
| RT-010 | Inventory / item / vehicle / asset owner specification |
| RT-011 | Validation readiness and tooling owner specification |
| RT-012 | D-series promotion boundary owner specification |

### Additional governance sources

| Source | Path |
|--------|------|
| Doctrine registry | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` |
| Decision log | `docs/decisions/current_decisions_log.md` |

---

## 3. Backend-first invariant

**Astra Ascension must be model-interchangeable.** The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

### Service implication

The Transaction Lifecycle and Event Commitment service is the future backend-owned boundary where validated command outcomes become committed runtime facts. It is the gate between "a command was accepted and a delta was proposed" and "a committed event exists in the ledger that downstream systems may treat as authoritative."

This service must never allow any of the following to directly mutate state or commit events:

- Model text, narration, or generated prose
- Model summaries or model-facing candidate projections
- Donor assumptions, donor-sourced terminology, or donor-local mechanics
- Source-local converted content that has not passed through the full command-lifecycle/action-legality/state-projection pipeline
- UI declarations, client-side state, or player-submitted state assertions
- Prompt template output or context-packet content
- Any external system that is not the backend runtime kernel

Every committed event must trace back to a validated command envelope that traversed the full lifecycle. Every state delta referenced by a committed event must have been proposed by a backend-owned resolution service and validated by the validation pipeline. No shortcut paths exist.

---

## 4. Service ownership

### Primary ownership

The Transaction Lifecycle and Event Commitment service owns the following future concerns:

1. **Transaction boundary** — defining and enforcing the boundary between "command accepted for transaction planning" (the terminal output of command lifecycle) and "event committed" (the input to downstream event-driven systems).

2. **Transaction lifecycle state** — tracking the progression of a transaction from request through resolution, validation, commitment readiness, and final commitment/rejection/quarantine/cancellation.

3. **Commit readiness** — evaluating whether a fully-resolved, fully-validated transaction has met all invariants required to produce a committed event.

4. **Event commitment boundary** — the decision point where a commit-ready transaction produces an authoritative committed event or is rejected/quarantined.

5. **Event rejection/quarantine/cancellation** — declaring and recording the reasons why a transaction did not produce a committed event.

6. **Validated handoff from upstream domain services** — accepting validated outputs from command lifecycle, action legality, state store, and state projection and coordinating their convergence toward a committable transaction.

7. **Trace/audit decision declaration** — declaring trace and audit references for every transaction lifecycle decision and every event commitment decision, to be consumed by runtime_trace and replay_audit.

### Dependency ownership

The Transaction Lifecycle and Event Commitment service depends on but does not own the following:

| Dependency | Owner | Relationship |
|---|---|---|
| command_envelope | Kernel (command_envelope.py) | Provides the validated command envelope that initiated the transaction. PR-3 service reads command_id and command_type; it does not create or modify envelopes. |
| command_lifecycle | Domain (command_lifecycle.py) | Provides the accepted command lifecycle result. PR-3 service accepts only commands at the `accepted_for_transaction_planning` terminal stage. It does not evaluate lifecycle stages. |
| action_legality | Domain (action_legality.py) | Provides the legality result and any block reasons. PR-3 service reads the legality decision and dependency declarations; it does not make legality decisions. |
| state_store | Domain (state_store.py) | Provides immutable state record references and snapshot references. PR-3 service reads state refs for commit-readiness checks; it does not create, modify, or delete state records. |
| state_projection | Domain (state_projection.py) | Provides materialized state projections. PR-3 service reads projection results to verify state context was available; it does not create projections. |
| state_delta | Kernel (state_delta.py) | Provides the future delta payload shape (StateDeltaEnvelope). PR-3 service references delta IDs and change types for commit-readiness; it must not apply deltas to state. |
| event_ledger | Kernel (event_ledger.py) | Provides the future event record surface (EventLedgerEntry). PR-3 service declares that a transaction is commit-ready and references the event shape; it must not directly append events to any ledger. |
| validation_pipeline | Kernel (validation_pipeline.py) | Provides the future invariant result boundary (ValidationResult, InvariantPrecheck). PR-3 service reads validation results to gate commit readiness; it does not define domain validation rules. |
| hidden_information | Kernel (hidden_information.py) | Provides visibility tier constraints. PR-3 service checks that no committed event would leak hidden information; it does not create or modify hidden-information records. |
| context_projection | Kernel (context_projection.py) | Provides visibility safety constraints. PR-3 service verifies context-projection safety before commitment; it does not compile context packets. |
| persistence_boundary | Kernel (persistence_boundary.py) | Provides the future durability handoff (PersistenceBoundaryRequest/Result). PR-3 service declares persistence-readiness; it does not perform durable persistence. |
| replay_audit | Kernel (replay_audit.py) | Provides the future replay/audit handoff (ReplayAuditRecord, HashAuditRecord). PR-3 service declares audit references; it does not run replay or enforce hash chains. |
| runtime_trace | Kernel (runtime_trace.py) | Provides the future trace reference surface (RuntimeTraceEntry). PR-3 service declares trace entries; it does not manage a trace store or telemetry backend. |

### Explicit non-ownership

The Transaction Lifecycle and Event Commitment service must **not** own, implement, or assume ownership of any of the following:

- Command execution or command interpretation
- Action legality evaluation or legality rules
- State mutation, state application, or state write-back
- State projection materialization or state query execution
- Domain resolution (resource math, combat resolution, ability resolution, inventory calculation, mission routing, social/faction evaluation)
- Event ledger append, event store persistence, or event replay
- Delta application to mutable state
- Validation rule authorship or invariant definition (it consumes validation results, it does not define validation logic)
- Hidden-information record creation, modification, or deletion
- Context-packet compilation or model-facing projection assembly
- Persistence engine, database schema, or durable write operations
- Replay engine, hash-chain enforcement, or audit verification
- RNG invocation or table/oracle resolution
- Schema definition or schema registry mutation
- Record identity creation or identity format changes
- Prompt template authorship or model routing
- Model evaluation, model selection, or structured-output parsing
- Live-play adapter, UI/client adapter, or network transport
- Generated-content provenance or recurrence tracking (owned by RT-008)
- D-series promotion boundary enforcement (owned by RT-012)
- Donor conversion, sourcebook inclusion, or canon promotion

---

## 5. Future service responsibilities

### Allowed future responsibilities

The Transaction Lifecycle and Event Commitment service is planned to perform the following in a future implementation (not in this PR):

1. Accept a validated command lifecycle result at the `accepted_for_transaction_planning` stage and open a transaction request.
2. Bind the transaction to the originating command envelope reference (command_id, command_type, source_actor_id).
3. Bind the transaction to actor references from the state store.
4. Bind the transaction to state projection results that were materialized for this command.
5. Declare transaction dependencies (which downstream domain services must resolve before commitment is possible).
6. Declare transaction preconditions (invariants that must hold true at commitment time).
7. Accept a proposed state delta envelope reference from a future domain resolution service and record it as the transaction's proposed outcome.
8. Request validation of the proposed delta against declared preconditions and commit-readiness invariants.
9. Evaluate commit readiness: all dependencies resolved, all preconditions met, validation passed, no hidden-information leaks, no idempotency conflicts, no persistence-boundary rejections.
10. Declare the transaction as commit-ready, rejected, quarantined, cancelled, or superseded.
11. Emit an event commitment request referencing the commit-ready transaction.
12. Emit an event commitment result (committed, rejected, or quarantined) with full trace/audit references.
13. Declare persistence-boundary readiness for downstream persistence handoff.
14. Declare replay-audit references for downstream audit handoff.
15. Declare runtime-trace entries for every lifecycle stage transition and every commitment decision.
16. Report transaction status to upstream callers (command lifecycle service, action legality service) for feedback loops.

### Forbidden responsibilities

The Transaction Lifecycle and Event Commitment service must never:

1. Execute commands or interpret command semantics.
2. Make legality decisions or override action legality results.
3. Apply state deltas to mutable state or write state records.
4. Append events to any event ledger or event store.
5. Perform durable persistence, database writes, or file I/O.
6. Run replay, enforce hash chains, or verify audit trails.
7. Compile context packets or assemble model-facing projections.
8. Define validation rules or invariant logic (it consumes validation results).
9. Invoke RNG or resolve table/oracle lookups.
10. Create, modify, or delete hidden-information records.
11. Create, modify, or delete schema registry entries.
12. Create or modify record identities.
13. Route commands to models, evaluate model output, or parse structured model responses.
14. Serve UI/client requests or manage network transport.
15. Perform domain resolution for any RT-002 through RT-010 concern.
16. Promote donor content, source-local content, or design documents to canon or runtime authority.

---

## 6. Transaction lifecycle model

The following 18 transaction lifecycle stages are planned for the future Transaction Lifecycle service. Each stage is defined with its meaning, allowed inputs, allowed outputs, owning service, kernel dependency, forbidden behavior, and downstream handoff. These are planning-only definitions and must not be implemented in PR-3.

### 6.1 transaction_requested

- **Meaning:** A validated command has reached the `accepted_for_transaction_planning` terminal stage in command lifecycle, and the transaction lifecycle service has been asked to open a transaction for it.
- **Allowed inputs:** CommandLifecycleResult at stage `accepted_for_transaction_planning` with status `accepted`.
- **Allowed outputs:** TransactionRequest with stage `transaction_requested`, referencing the source command_id.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** command_envelope (read command_id), record_identity (validate record IDs).
- **Forbidden behavior:** Must not evaluate legality, must not read or mutate state, must not invoke RNG.
- **Downstream handoff:** Proceeds to `command_reference_bound`.

### 6.2 command_reference_bound

- **Meaning:** The transaction has been bound to the originating command envelope. The command_id, command_type, and source_actor_id are recorded as immutable references on the transaction.
- **Allowed inputs:** TransactionRequest at stage `transaction_requested`.
- **Allowed outputs:** TransactionPlan with command reference fields populated.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** command_envelope (read fields), record_identity (validate source_actor_id format).
- **Forbidden behavior:** Must not re-evaluate the command envelope. Must not create a new command.
- **Downstream handoff:** Proceeds to `actor_reference_bound`.

### 6.3 actor_reference_bound

- **Meaning:** The transaction has been bound to actor state references from the state store. The acting entity's state record ref and visibility descriptor have been captured.
- **Allowed inputs:** TransactionPlan at stage `command_reference_bound`, plus StateRecordRef for the acting entity.
- **Allowed outputs:** TransactionPlan with actor_ref_id and actor visibility fields populated.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** record_identity (validate actor record ID), hidden_information (visibility tier check).
- **Forbidden behavior:** Must not create actor records. Must not modify actor state. Must not query state store directly (receives references from upstream).
- **Downstream handoff:** Proceeds to `state_projection_bound`.

### 6.4 state_projection_bound

- **Meaning:** The transaction has been bound to a materialized state projection result. The projection provides the state context against which the transaction's proposed delta will be evaluated.
- **Allowed inputs:** TransactionPlan at stage `actor_reference_bound`, plus StateProjectionResult at status `materialized`.
- **Allowed outputs:** TransactionPlan with projection_id and projection state ref IDs populated.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** None directly; reads from domain state_projection result shapes.
- **Forbidden behavior:** Must not materialize projections. Must not modify projections. Must not expose backend-hidden state refs through the projection binding.
- **Downstream handoff:** Proceeds to `dependencies_declared`.

### 6.5 dependencies_declared

- **Meaning:** The transaction has declared which downstream domain services (RT-002 through RT-010) must resolve before the transaction's delta can be proposed. Dependencies are typed references, not execution calls.
- **Allowed inputs:** TransactionPlan at stage `state_projection_bound`, plus a sequence of TransactionDependency declarations.
- **Allowed outputs:** TransactionPlan with dependencies tuple populated.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** None directly; dependency types reference future domain service owners.
- **Forbidden behavior:** Must not resolve dependencies. Must not call domain resolution services. Must not assume dependency resolution order.
- **Downstream handoff:** Proceeds to `preconditions_declared`.

### 6.6 preconditions_declared

- **Meaning:** The transaction has declared invariant preconditions that must hold true at commitment time. Preconditions reference validation pipeline invariant IDs and expected outcomes.
- **Allowed inputs:** TransactionPlan at stage `dependencies_declared`, plus a sequence of TransactionPrecondition declarations.
- **Allowed outputs:** TransactionPlan with preconditions tuple populated.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** validation_pipeline (InvariantPrecheck shape reference).
- **Forbidden behavior:** Must not evaluate preconditions. Must not define validation rules. Must not bypass declared preconditions.
- **Downstream handoff:** Proceeds to `domain_resolution_required`.

### 6.7 domain_resolution_required

- **Meaning:** The transaction has declared its dependencies and preconditions and is now waiting for domain resolution services to compute the proposed outcome. This is a blocking wait stage.
- **Allowed inputs:** TransactionPlan at stage `preconditions_declared`.
- **Allowed outputs:** TransactionPlan at stage `domain_resolution_required` with status `waiting`.
- **Owning service:** Transaction Lifecycle Service (stage tracking only).
- **Kernel dependency:** None.
- **Forbidden behavior:** Must not perform domain resolution. Must not compute resource math, combat outcomes, ability effects, inventory changes, or any RT-002 through RT-010 concern. Must not skip this stage.
- **Downstream handoff:** Proceeds to `proposed_delta_referenced` when a domain resolution service provides a StateDeltaEnvelope reference.

### 6.8 proposed_delta_referenced

- **Meaning:** A domain resolution service has provided a proposed StateDeltaEnvelope reference. The transaction now has a proposed outcome but has not yet been validated.
- **Allowed inputs:** TransactionPlan at stage `domain_resolution_required`, plus a StateDeltaEnvelope reference (delta_id, change_type, affected_record_ids).
- **Allowed outputs:** TransactionPlan with delta_ref_id and delta_change_type populated.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** state_delta (read StateDeltaEnvelope shape), record_identity (validate affected record IDs).
- **Forbidden behavior:** Must not apply the delta. Must not modify the delta. Must not create the delta (it is provided by a domain resolution service).
- **Downstream handoff:** Proceeds to `validation_requested`.

### 6.9 validation_requested

- **Meaning:** The transaction has requested validation of its proposed delta against declared preconditions and commit-readiness invariants. The validation pipeline will produce a ValidationResult.
- **Allowed inputs:** TransactionPlan at stage `proposed_delta_referenced`.
- **Allowed outputs:** TransactionPlan at stage `validation_requested`, with a validation_request_id.
- **Owning service:** Transaction Lifecycle Service (request coordination only).
- **Kernel dependency:** validation_pipeline (ValidationResult shape, InvariantPrecheck shape).
- **Forbidden behavior:** Must not define validation rules. Must not evaluate invariants directly. Must not bypass validation.
- **Downstream handoff:** Proceeds to `validation_passed` or `validation_failed`.

### 6.10 validation_passed

- **Meaning:** The validation pipeline returned a ValidationResult with `passed=True`. All declared preconditions and commit-readiness invariants have been satisfied.
- **Allowed inputs:** TransactionPlan at stage `validation_requested`, plus ValidationResult with `passed=True`.
- **Allowed outputs:** TransactionPlan with validation_id populated, validation_passed=True.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** validation_pipeline (read ValidationResult).
- **Forbidden behavior:** Must not override a failed validation. Must not ignore validation issues with severity `error` or `critical`.
- **Downstream handoff:** Proceeds to `ready_for_event_commitment`.

### 6.11 validation_failed

- **Meaning:** The validation pipeline returned a ValidationResult with `passed=False`. One or more declared preconditions or commit-readiness invariants were not satisfied.
- **Allowed inputs:** TransactionPlan at stage `validation_requested`, plus ValidationResult with `passed=False`.
- **Allowed outputs:** TransactionResult with stage `validation_failed`, referencing the failing ValidationResult and its issues.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** validation_pipeline (read ValidationResult, ValidationIssue).
- **Forbidden behavior:** Must not retry validation without a new proposed delta. Must not promote a failed validation to passed. Must not suppress error/critical issues.
- **Downstream handoff:** Terminal for this transaction attempt. May proceed to `rejected` or `quarantined` depending on issue severity and policy.

### 6.12 ready_for_event_commitment

- **Meaning:** The transaction has passed all commit-readiness checks: validation passed, no hidden-information leaks detected, no idempotency conflicts, no persistence-boundary rejections. The transaction is eligible for event commitment.
- **Allowed inputs:** TransactionPlan at stage `validation_passed`, plus successful commit-readiness invariant evaluation.
- **Allowed outputs:** TransactionPlan with commit_ready=True.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** hidden_information (visibility tier check), persistence_boundary (prepare check), replay_audit (audit reference declaration).
- **Forbidden behavior:** Must not commit the event. Must not apply the delta. Must not skip any commit-readiness invariant.
- **Downstream handoff:** Proceeds to `commitment_requested`.

### 6.13 commitment_requested

- **Meaning:** The transaction lifecycle service has emitted an EventCommitmentRequest to the event commitment boundary. The request is pending.
- **Allowed inputs:** TransactionPlan at stage `ready_for_event_commitment`.
- **Allowed outputs:** EventCommitmentRequest referencing the transaction_id, delta_ref_id, command_id, validation_id.
- **Owning service:** Event Commitment Service (receives the request); Transaction Lifecycle Service (emits the request).
- **Kernel dependency:** event_ledger (EventLedgerEntry shape reference), state_delta (StateDeltaEnvelope shape reference).
- **Forbidden behavior:** Must not append to the event ledger. Must not apply deltas. Must not bypass the event commitment boundary.
- **Downstream handoff:** Proceeds to `committed`, `rejected`, or `quarantined` based on event commitment result.

### 6.14 committed

- **Meaning:** The event commitment boundary has accepted the commitment request and declared the event as committed. A committed event is an authoritative runtime fact.
- **Allowed inputs:** EventCommitmentResult with decision `committed`.
- **Allowed outputs:** TransactionResult with stage `committed`, event_id, commitment_id, trace_id, audit references.
- **Owning service:** Transaction Lifecycle Service (records the result); Event Commitment Service (makes the commitment decision).
- **Kernel dependency:** event_ledger (committed event shape), runtime_trace (trace entry), replay_audit (audit record).
- **Forbidden behavior:** Must not reverse a committed event within the transaction lifecycle (reversal is a new command). Must not modify the committed event after commitment.
- **Downstream handoff:** Terminal. Downstream consumers (state application, persistence, replay) receive the committed event through their own boundaries.

### 6.15 rejected

- **Meaning:** The transaction or event commitment was rejected. The command did not produce a committed event.
- **Allowed inputs:** Any non-terminal stage where a rejection condition is detected, or EventCommitmentResult with any `rejected_by_*` decision.
- **Allowed outputs:** TransactionResult with stage `rejected`, rejection reason, trace references.
- **Owning service:** Transaction Lifecycle Service (declares rejection) or Event Commitment Service (declares commitment rejection).
- **Kernel dependency:** runtime_trace (trace entry), validation_pipeline (if rejection due to validation failure).
- **Forbidden behavior:** Must not silently discard a rejection. Must record rejection reason and trace. Must not re-attempt without a new transaction request.
- **Downstream handoff:** Terminal. Rejection reason is available to command lifecycle for player-facing feedback.

### 6.16 quarantined

- **Meaning:** The transaction or event commitment was quarantined for audit review. The command did not produce a committed event but is preserved for inspection.
- **Allowed inputs:** Any stage where a quarantine condition is detected (validation issues with severity `critical`, hidden-information leak risk, idempotency anomaly), or EventCommitmentResult with decision `quarantined_for_audit`.
- **Allowed outputs:** TransactionResult with stage `quarantined`, quarantine reason, audit references.
- **Owning service:** Transaction Lifecycle Service (declares quarantine) or Event Commitment Service (declares commitment quarantine).
- **Kernel dependency:** runtime_trace (trace entry), replay_audit (quarantine audit record).
- **Forbidden behavior:** Must not release from quarantine without explicit audit review. Must not allow quarantined transactions to produce committed events.
- **Downstream handoff:** Terminal. Quarantine record is available to audit systems.

### 6.17 cancelled

- **Meaning:** The transaction was cancelled before commitment, either by explicit upstream cancellation (e.g., player cancelled the command after confirmation prompt) or by timeout/supersession.
- **Allowed inputs:** Any non-terminal, non-committed stage, plus an explicit cancellation signal.
- **Allowed outputs:** TransactionResult with stage `cancelled`, cancellation reason, trace references.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** runtime_trace (trace entry).
- **Forbidden behavior:** Must not cancel a committed transaction (committed events are irreversible within the transaction boundary). Must not cancel without recording the reason.
- **Downstream handoff:** Terminal. Cancellation reason is available to command lifecycle for player-facing feedback.

### 6.18 superseded

- **Meaning:** The transaction was superseded by a newer transaction for the same command or same actor/target combination, according to idempotency or conflict-resolution policy.
- **Allowed inputs:** Any non-terminal, non-committed stage, plus detection of a superseding transaction.
- **Allowed outputs:** TransactionResult with stage `superseded`, superseding_transaction_id, trace references.
- **Owning service:** Transaction Lifecycle Service.
- **Kernel dependency:** runtime_trace (trace entry).
- **Forbidden behavior:** Must not supersede a committed transaction. Must not allow the superseded transaction to continue toward commitment. Must record the superseding transaction ID.
- **Downstream handoff:** Terminal. Supersession reason is available to command lifecycle for player-facing feedback.

---

## 7. Event commitment model

The following 12 event commitment decisions are planned for the future Event Commitment service. Each decision is defined with its meaning, when it applies, required dependencies, whether it allows committed event authority, whether state mutation remains blocked, downstream handoff, and required trace/audit data. These are planning-only definitions and must not be implemented in PR-3.

### 7.1 commit_ready

- **Meaning:** The event commitment boundary has determined that all commit-readiness invariants are satisfied and the event may be committed. This is a pre-commitment gate, not a final commitment.
- **When it applies:** After the transaction reaches `ready_for_event_commitment` and an EventCommitmentRequest is received.
- **Required dependencies:** ValidationResult with `passed=True`, no hidden-information leak flags, no idempotency conflicts, persistence boundary prepare status `prepared`.
- **Allows committed event authority:** No. This is a gate decision, not a commitment.
- **State mutation remains blocked:** Yes. No state may be mutated at this stage.
- **Downstream handoff:** Proceeds to commitment evaluation.
- **Required trace/audit data:** Trace entry with operation_type referencing transaction lifecycle, commit-readiness invariant results, timestamp.

### 7.2 committed

- **Meaning:** The event has been committed. It is now an authoritative runtime fact. Downstream systems may treat the committed event and its associated delta as truth.
- **When it applies:** After commit_ready evaluation passes and no blocking conditions are detected.
- **Required dependencies:** commit_ready gate passed, EventLedgerEntry shape valid, StateDeltaEnvelope referenced and valid, all trace/audit references declared.
- **Allows committed event authority:** Yes. This is the only decision that produces authoritative committed events.
- **State mutation remains blocked:** Yes at the event commitment service level. State mutation is the responsibility of a downstream state-application service that consumes committed events. The event commitment service itself never mutates state.
- **Downstream handoff:** Committed event is available to downstream consumers (future state application, persistence boundary, replay audit).
- **Required trace/audit data:** Trace entry, replay audit record, hash audit record (SHA-256 of committed event payload), commitment timestamp, command_id, transaction_id, delta_id, event_id.

### 7.3 rejected_by_validation

- **Meaning:** The event commitment was rejected because the validation pipeline returned `passed=False` for the transaction's proposed delta or preconditions.
- **When it applies:** When ValidationResult.passed is False, or when validation issues include severity `error` or `critical`.
- **Required dependencies:** ValidationResult with `passed=False` and associated ValidationIssue entries.
- **Allows committed event authority:** No.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Rejection reason is returned to transaction lifecycle service for recording as a `rejected` or `quarantined` transaction result.
- **Required trace/audit data:** Trace entry, validation_id, failing issue codes, issue severities.

### 7.4 rejected_by_scope

- **Meaning:** The event commitment was rejected because the proposed delta's scope (affected record IDs, change types) falls outside the boundaries allowed for the originating command type.
- **When it applies:** When the proposed StateDeltaEnvelope references record IDs or change types that the originating command's declared scope does not cover.
- **Required dependencies:** CommandEnvelope.command_type scope declaration, StateDeltaEnvelope.affected_record_ids, StateDeltaEnvelope.change_type.
- **Allows committed event authority:** No.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Rejection reason is returned to transaction lifecycle service.
- **Required trace/audit data:** Trace entry, command_type, declared scope, actual delta scope, affected record IDs.

### 7.5 rejected_by_missing_state_reference

- **Meaning:** The event commitment was rejected because the transaction references state record IDs or snapshot IDs that do not exist in the state store or have become stale.
- **When it applies:** When the transaction's bound state projection references state_ref_ids that cannot be validated against the current state store.
- **Required dependencies:** StateRecordRef validation, StateSnapshotRef validation.
- **Allows committed event authority:** No.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Rejection reason is returned to transaction lifecycle service.
- **Required trace/audit data:** Trace entry, missing state_ref_ids, transaction_id, projection_id.

### 7.6 rejected_by_missing_delta_reference

- **Meaning:** The event commitment was rejected because the transaction's proposed delta reference (delta_id) is missing, malformed, or does not correspond to a valid StateDeltaEnvelope.
- **When it applies:** When the transaction's delta_ref_id is null, empty, or fails StateDeltaEnvelope validation.
- **Required dependencies:** StateDeltaEnvelope validation.
- **Allows committed event authority:** No.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Rejection reason is returned to transaction lifecycle service.
- **Required trace/audit data:** Trace entry, delta_ref_id (if present), transaction_id, validation failure details.

### 7.7 rejected_by_hidden_information_risk

- **Meaning:** The event commitment was rejected because committing the event would risk leaking hidden information to an unauthorized visibility tier.
- **When it applies:** When the proposed delta or event references records with visibility tiers (`backend_hidden`, `restricted`) that would become visible through the committed event's downstream projection surface.
- **Required dependencies:** HiddenInformationRecord visibility tier, ContextProjection allowed_visibility_tiers, StateVisibilityDescriptor on affected records.
- **Allows committed event authority:** No.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Rejection reason is returned to transaction lifecycle service. Transaction may be quarantined rather than rejected if the risk requires audit review.
- **Required trace/audit data:** Trace entry, affected record IDs, visibility tiers involved, hidden_information record_ids at risk.

### 7.8 rejected_by_idempotency_conflict

- **Meaning:** The event commitment was rejected because a committed event with the same idempotency key (command_id + delta scope) already exists.
- **When it applies:** When the event commitment boundary detects that a previous transaction for the same command_id and same affected_record_ids has already been committed.
- **Required dependencies:** Previously committed event references (event_id, command_id, affected_record_ids).
- **Allows committed event authority:** No.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Rejection reason is returned to transaction lifecycle service. The transaction may be marked `superseded` rather than `rejected`.
- **Required trace/audit data:** Trace entry, conflicting event_id, conflicting transaction_id, command_id.

### 7.9 rejected_by_persistence_boundary

- **Meaning:** The event commitment was rejected because the persistence boundary prepare step returned status `rejected` or `quarantined`.
- **When it applies:** When PersistenceBoundaryResult.status is not `prepared` for the event_append_prepare operation.
- **Required dependencies:** PersistenceBoundaryResult for operation_type `event_append_prepare`.
- **Allows committed event authority:** No.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Rejection reason is returned to transaction lifecycle service.
- **Required trace/audit data:** Trace entry, persistence_boundary request_id, rejection status, subject_ref.

### 7.10 quarantined_for_audit

- **Meaning:** The event commitment was quarantined rather than outright rejected because the detected issue requires manual audit review before the event can be definitively rejected or released.
- **When it applies:** When validation issues include severity `critical`, when hidden-information risk is ambiguous, when idempotency conflicts involve complex supersession chains, or when the persistence boundary returns `quarantined`.
- **Required dependencies:** The triggering issue (validation, hidden information, idempotency, or persistence boundary result).
- **Allows committed event authority:** No. Quarantined events are not committed.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Quarantine record is available to audit systems. The transaction is recorded as `quarantined`.
- **Required trace/audit data:** Trace entry, quarantine reason code, replay audit record, all triggering issue details, transaction_id, command_id.

### 7.11 cancelled_before_commit

- **Meaning:** The event commitment was cancelled before the commitment decision was finalized, typically because the upstream transaction was cancelled.
- **When it applies:** When the transaction lifecycle service signals cancellation after the EventCommitmentRequest was emitted but before the committed decision was made.
- **Required dependencies:** Cancellation signal from transaction lifecycle service.
- **Allows committed event authority:** No.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Cancellation is recorded in the transaction result. No committed event is produced.
- **Required trace/audit data:** Trace entry, cancellation reason, transaction_id, command_id.

### 7.12 unsupported_event_type

- **Meaning:** The event commitment was rejected because the proposed event type is not recognized by the event commitment service.
- **When it applies:** When the EventLedgerEntry.event_type is not one of the allowed event types (`command_event`, `transaction_event`, `state_delta_event`, `validation_event`, `system_audit_event`).
- **Required dependencies:** EventLedgerEntry.event_type validation against the allowed set.
- **Allows committed event authority:** No.
- **State mutation remains blocked:** Yes.
- **Downstream handoff:** Rejection reason is returned to transaction lifecycle service.
- **Required trace/audit data:** Trace entry, unsupported event_type value, transaction_id, command_id.

---

## 8. Transaction vs event boundary

This section clarifies the distinction between four related but separate concerns: transaction lifecycle, event commitment, state delta, and event ledger. These boundaries must not be collapsed.

### Transaction lifecycle vs event commitment

The **transaction lifecycle** tracks the progression of a command from `accepted_for_transaction_planning` through resolution, validation, and commit-readiness. It is a coordination service that binds together command references, actor references, state projections, dependencies, preconditions, and proposed deltas. It owns the question: "Is this transaction ready to be committed?" The transaction lifecycle does not mutate state, does not append events, and does not persist.

The **event commitment** boundary is the decision point that answers: "Should this commit-ready transaction produce an authoritative committed event?" Event commitment is a gate, not a lifecycle. It evaluates a single commitment request and returns a single commitment result. It does not track multi-stage progression. Future event commitment must be append-only, deterministic, and auditable. It must not itself calculate domain outcomes. It must not skip validation.

The transaction lifecycle may reject, quarantine, cancel, or supersede a transaction at any stage before commitment. The event commitment boundary may only reject, quarantine, or commit an event commitment request that has already been declared commit-ready by the transaction lifecycle.

### State delta vs committed event

A **state delta** (StateDeltaEnvelope) is a proposed mutation payload. It describes what would change if the transaction is committed. It has a delta_id, a source_command_id, a source_preview_id, affected_record_ids, a change_type, and a payload. A state delta is inert until it is referenced by a committed event.

A **committed event** (EventLedgerEntry) is an authoritative runtime fact. It has an event_id, event_type, sequence number, source_command_id, source_preview_id, and references to state_delta_ids. A committed event is the boundary between "proposed" and "authoritative."

State deltas are produced by domain resolution services (RT-002 through RT-010). Committed events are produced by the event commitment boundary. The transaction lifecycle service coordinates between them but produces neither.

### Event ledger vs event commitment

The **event ledger** (event_ledger.py) is a kernel-level data shape for event entries. It defines the EventLedgerEntry frozen dataclass and its validation. It does not own event storage, event ordering, event append, or event query.

**Event commitment** is a domain-level service that decides whether a proposed event entry should become authoritative. It reads event ledger entry shapes but does not append entries to any ledger. The actual append operation is a future concern owned by a persistence/event-store service that does not yet exist.

### State delta vs state mutation

A **state delta** is a proposed change description. **State mutation** is the actual application of that change to mutable state. The transaction lifecycle and event commitment services never perform state mutation. State mutation is a future concern that will consume committed events and apply their referenced deltas to the authoritative state store. This separation ensures that no state changes occur without a committed event trail.

---

## 9. Kernel interface consumption plan

The following matrix defines how each of the 14 kernel skeleton modules is consumed by the future Transaction Lifecycle and Event Commitment service. Each module is classified as required, optional, forbidden, later (deferred to a future PR), or not_applicable for PR-3A skeleton implementation.

| Kernel Module | PR-3A Position | Allowed Future Use | Forbidden Use | Risk If Used Too Early | Expected Future Tests |
|---|---|---|---|---|---|
| schema_registry | optional | Read schema IDs to validate record type references on transaction requests. Verify that proposed delta affected_record_ids reference known schema types. | Must not register new schemas. Must not modify schema entries. Must not use schema registry as a runtime type system. | Premature schema coupling could lock transaction shapes to schema versions before schema stability is confirmed. | Test that transaction requests referencing unknown schema IDs are rejected. |
| record_identity | required | Validate record ID format (`astra:type:local_id`) on command_id, actor references, state_ref_ids, delta affected_record_ids. Use `is_valid_record_id` for all ID validation. | Must not create new record IDs. Must not modify the record ID format. | Minimal risk; record_identity is already stable and used by all upstream domain services. | Test that transaction requests with malformed record IDs are rejected. Test that `build_record_id`/`parse_record_id` round-trip correctly for transaction-related IDs. |
| command_envelope | required | Read CommandEnvelope fields (command_id, command_type, source_actor_id) to bind transactions to their originating command. Validate envelope integrity via `validate_command_envelope`. | Must not create command envelopes. Must not modify command envelopes. Must not execute commands. | Minimal risk; command_envelope is stable and already consumed by command_lifecycle and action_legality. | Test that transaction binding rejects invalid command envelopes. Test that command_id propagation is correct. |
| transaction_preview | required | Read TransactionPreview fields (preview_id, command_id, status) to verify that a transaction preview was created before commitment is allowed. Reference preview_id in transaction plans. | Must not create transaction previews. Must not modify preview status. Must not bypass preview requirement. | Coupling to preview status could create circular dependency if preview creation requires transaction lifecycle input. Keep dependency unidirectional. | Test that transactions without a valid preview reference are rejected. Test that preview status `preview_rejected` blocks commitment. |
| state_delta | required | Read StateDeltaEnvelope fields (delta_id, source_command_id, source_preview_id, affected_record_ids, change_type) to bind proposed deltas to transactions. Validate delta shape. | Must not create state deltas. Must not apply deltas to state. Must not modify delta payloads. | Premature delta application would violate the "no state mutation" invariant. Reading delta shapes only is safe. | Test that transactions with missing or invalid delta references are rejected. Test that change_type values are validated against the allowed set. |
| event_ledger | required | Read EventLedgerEntry shape (event_id, event_type, sequence, source_command_id, source_preview_id, state_delta_ids) to declare commitment-ready event shapes. Validate event type against allowed set. | Must not append events to any ledger. Must not assign sequence numbers (sequence assignment is a future event-store concern). Must not modify existing events. | Premature event append would create committed events without proper validation and audit trail. Shape reading only is safe. | Test that event commitment requests with unsupported event types are rejected. Test that committed event references are structurally valid. |
| rng_interface | not_applicable | No planned use. Transaction lifecycle and event commitment do not involve random number generation. | Must not invoke RNG for any transaction or commitment decision. Determinism must come from the command pipeline, not from transaction-level randomness. | RNG invocation at the transaction level would make commitment non-deterministic and break replay audit. | No transaction-specific RNG tests. Verify that no RNG imports exist in transaction_lifecycle.py or event_commitment.py. |
| table_oracle | not_applicable | No planned use. Transaction lifecycle and event commitment do not involve table/oracle resolution. | Must not invoke table/oracle lookups for transaction or commitment decisions. | Table/oracle invocation at the transaction level would introduce domain resolution logic into the coordination layer. | No transaction-specific table_oracle tests. Verify that no table_oracle imports exist in transaction_lifecycle.py or event_commitment.py. |
| validation_pipeline | required | Read ValidationResult (validation_id, subject_ref, passed, issues) and ValidationIssue (code, message, severity, source) to gate commit readiness. Read InvariantPrecheck shapes for precondition declaration. Use `run_validation_checks` for transaction-internal shape validation only. | Must not define domain validation rules. Must not author invariant logic. Must not bypass validation failures. | Premature invariant authorship would embed domain rules in the coordination layer. Reading validation results and running shape checks only is safe. | Test that commit readiness requires ValidationResult.passed=True. Test that validation issues with severity error/critical block commitment. Test that transaction shape validation catches malformed inputs. |
| hidden_information | required | Read HiddenInformationRecord visibility_tier and use `is_visible_to_tiers` to verify that committed events do not leak hidden information. Check visibility tier constraints on affected records. | Must not create hidden-information records. Must not modify visibility tiers. Must not redact records (redaction is owned by context_projection). | Incorrect visibility checks could allow hidden-information leaks through committed events. Conservative approach: reject if any affected record has `backend_hidden` or `restricted` tier and the event would make it downstream-visible. | Test that events affecting `backend_hidden` records are rejected or quarantined. Test visibility tier validation on all affected record IDs. |
| context_projection | optional | Read ContextProjection and ContextProjectionItem shapes to verify that committed events are safe relative to the visibility projection surface. Cross-check event affected records against projection allowed_visibility_tiers. | Must not create context projections. Must not compile context packets. Must not modify projection items. | Over-coupling to context projection could make transaction lifecycle dependent on projection materialization timing. Keep as optional safety check, not hard dependency. | Test that events with affected records outside allowed_visibility_tiers trigger rejection or quarantine. |
| persistence_boundary | required | Create PersistenceBoundaryRequest with operation_type `event_append_prepare` to check persistence readiness before commitment. Read PersistenceBoundaryResult status. | Must not perform durable persistence. Must not write to databases or file systems. Must not bypass persistence boundary prepare step. | Premature persistence would bypass the event commitment gate. Prepare-only is safe. | Test that PersistenceBoundaryResult with status `rejected` blocks commitment. Test that status `quarantined` quarantines the transaction. Test that status `prepared` allows commitment to proceed. |
| replay_audit | required | Create ReplayAuditRecord and HashAuditRecord references for committed events. Use `canonical_payload_hash` to compute SHA-256 hashes of committed event payloads. | Must not run replay. Must not enforce hash chains. Must not verify audit trails (verification is a future concern). | Premature replay execution would require an event store that does not yet exist. Hash computation and record creation is safe. | Test that committed events produce valid ReplayAuditRecord references. Test that canonical_payload_hash produces deterministic SHA-256 for the same event payload. Test that HashAuditRecord uses hash_algorithm `sha256`. |
| runtime_trace | required | Create RuntimeTraceEntry references for every transaction lifecycle stage transition and every event commitment decision. Use operation_type values referencing the appropriate kernel module. | Must not manage a trace store. Must not implement telemetry backends. Must not query trace history. | Trace creation without a trace store means traces are emitted but not persisted. This is the correct skeleton behavior. | Test that every lifecycle stage transition produces a RuntimeTraceEntry. Test that every commitment decision produces a RuntimeTraceEntry. Test that operation_type values are valid. |

---

## 10. Domain service handoff boundaries

This section defines the handoff boundaries between the future Transaction Lifecycle and Event Commitment service and all 16 related services (4 existing domain services, 12 RT owner specifications). For each service, the table specifies what the PR-3 future service may accept, what it may emit, what it must not decide, and what remains blocked until downstream owner exists.

### 10.1 command_lifecycle (existing domain service)

- **Accepts from:** CommandLifecycleResult at terminal stage `accepted_for_transaction_planning` with status `accepted`. The command_id, lifecycle_id, validation_id (if present), and downstream_dependencies.
- **Emits to:** Transaction status updates (rejected, quarantined, cancelled, committed) for command lifecycle feedback loops. Transaction_id for cross-reference.
- **Must not decide:** Whether a command should reach `accepted_for_transaction_planning`. Whether a command should be rejected, quarantined, or cancelled at the lifecycle level.
- **Blocked until downstream owner exists:** Full bidirectional lifecycle feedback (currently unidirectional: lifecycle -> transaction).

### 10.2 action_legality (existing domain service)

- **Accepts from:** ActionLegalityResult with decision `legal` or `requires_confirmation`. The legality_id, decision, lifecycle_stage, dependency declarations, block reasons (if any), confirmation requirements (if any).
- **Emits to:** Transaction rejection/quarantine reasons if legality blocks are discovered after transaction opening (should not occur in normal flow, but must be handled defensively).
- **Must not decide:** Whether an action is legal. Whether an action is blocked. Whether confirmation is required.
- **Blocked until downstream owner exists:** Legality re-evaluation during transaction lifecycle (e.g., if state changes between legality check and commitment).

### 10.3 state_store (existing domain service)

- **Accepts from:** StateRecordRef for actor binding and affected record validation. StateSnapshotRef for snapshot-scoped transactions. StateVisibilityDescriptor for visibility tier checks.
- **Emits to:** State reference validation results (valid/invalid/stale). Committed event references for downstream state application.
- **Must not decide:** Whether a state record exists. Whether a state record is authoritative. What the current value of any state field is.
- **Blocked until downstream owner exists:** State freshness validation (requires a state query service that does not yet exist). State write-back after commitment.

### 10.4 state_projection (existing domain service)

- **Accepts from:** StateProjectionResult at status `materialized` with projection_id, projection_type, state_ref_ids, visible_state_ref_ids, redacted_state_ref_ids.
- **Emits to:** Projection validation feedback (projection was sufficient/insufficient for the transaction's scope). Committed event references.
- **Must not decide:** What projection type to materialize. Which state refs to include. Which refs to redact.
- **Blocked until downstream owner exists:** Projection re-materialization during transaction lifecycle (if state changes between projection and commitment).

### 10.5 RT-001 command lifecycle / action legality (owner specification)

- **Accepts from:** Owner-level authorization that the command pipeline has completed and the transaction may proceed.
- **Emits to:** Transaction outcome for RT-001 reporting and monitoring.
- **Must not decide:** RT-001 lifecycle or legality policy.
- **Blocked until downstream owner exists:** Full RT-001 integration testing (requires live command pipeline).

### 10.6 RT-002 resource / consequence math

- **Accepts from:** Future resource calculation result (proposed delta for resource changes). Dependency resolution signal.
- **Emits to:** Dependency request (transaction declares RT-002 dependency). Transaction outcome.
- **Must not decide:** Resource math calculations. Consequence severity. Resource availability.
- **Blocked until downstream owner exists:** RT-002 domain resolution service does not exist. Transaction lifecycle can declare the dependency but cannot resolve it.

### 10.7 RT-003 combat / hazard / damage / recovery

- **Accepts from:** Future combat resolution result (proposed delta for combat state changes). Dependency resolution signal.
- **Emits to:** Dependency request. Transaction outcome.
- **Must not decide:** Combat resolution. Damage calculation. Recovery timing. Hazard effects.
- **Blocked until downstream owner exists:** RT-003 domain resolution service does not exist.

### 10.8 RT-004 ability / effect / skill binding

- **Accepts from:** Future ability resolution result (proposed delta for ability effects). Dependency resolution signal.
- **Emits to:** Dependency request. Transaction outcome.
- **Must not decide:** Ability effects. Skill binding. Effect duration. Power cost.
- **Blocked until downstream owner exists:** RT-004 domain resolution service does not exist.

### 10.9 RT-005 context packet / hidden information

- **Accepts from:** Visibility tier constraints for commit-readiness checks. Hidden-information risk assessment results.
- **Emits to:** Committed event visibility metadata for downstream context packet compilation.
- **Must not decide:** Context packet contents. Hidden-information record creation. Visibility tier assignment.
- **Blocked until downstream owner exists:** Full hidden-information risk assessment pipeline (PR-3 service performs basic tier checks only).

### 10.10 RT-006 mission / reward / clue routing

- **Accepts from:** Future mission resolution result (proposed delta for mission state changes). Dependency resolution signal.
- **Emits to:** Dependency request. Transaction outcome.
- **Must not decide:** Mission state. Reward distribution. Clue routing. Progress tracking.
- **Blocked until downstream owner exists:** RT-006 domain resolution service does not exist.

### 10.11 RT-007 social / faction / actor knowledge

- **Accepts from:** Future social/faction resolution result (proposed delta for social state changes). Dependency resolution signal.
- **Emits to:** Dependency request. Transaction outcome.
- **Must not decide:** Social standing. Faction relations. Actor knowledge state. Reputation effects.
- **Blocked until downstream owner exists:** RT-007 domain resolution service does not exist.

### 10.12 RT-008 generated-content provenance / recurrence

- **Accepts from:** Provenance declarations for generated content referenced by the transaction's proposed delta.
- **Emits to:** Committed event provenance metadata for downstream provenance tracking.
- **Must not decide:** Content provenance. Recurrence policy. Whether generated content is reusable.
- **Blocked until downstream owner exists:** RT-008 provenance tracking service does not exist.

### 10.13 RT-009 runtime RNG / table oracle

- **Accepts from:** RNG result references and table oracle result references from upstream domain resolution services (these are inputs to the delta, not inputs to the transaction lifecycle itself).
- **Emits to:** Committed event metadata referencing RNG/table oracle invocations for replay audit.
- **Must not decide:** RNG seeds. RNG results. Table oracle lookups. Randomness policy.
- **Blocked until downstream owner exists:** RT-009 integration is passive (metadata pass-through only). No active dependency.

### 10.14 RT-010 inventory / item / vehicle / asset

- **Accepts from:** Future inventory resolution result (proposed delta for inventory state changes). Dependency resolution signal.
- **Emits to:** Dependency request. Transaction outcome.
- **Must not decide:** Inventory state. Item availability. Vehicle status. Asset ownership.
- **Blocked until downstream owner exists:** RT-010 domain resolution service does not exist.

### 10.15 RT-011 validation readiness / tooling

- **Accepts from:** Validation tool integration (ValidationResult, InvariantPrecheck shapes). Validation readiness confirmation.
- **Emits to:** Validation requests for transaction-level invariant checking. Transaction outcome for validation reporting.
- **Must not decide:** Validation rule content. Invariant definitions. Validation tooling architecture.
- **Blocked until downstream owner exists:** Full validation pipeline integration (PR-3 service reads validation results but does not define domain rules).

### 10.16 RT-012 D-series promotion boundary

- **Accepts from:** Promotion boundary enforcement signals (blocks if a transaction attempts to promote design-document content to runtime authority).
- **Emits to:** Transaction rejection if promotion boundary is violated.
- **Must not decide:** What constitutes a D-series document. What promotion policy applies. Whether a promotion is safe.
- **Blocked until downstream owner exists:** RT-012 promotion boundary enforcement service does not exist. PR-3 service cannot enforce promotion boundaries until RT-012 is implemented.

---

## 11. Future implementation architecture

The following future implementation shape is planned for the Transaction Lifecycle and Event Commitment service. These are proposed file paths and public API symbols only. They must not be created in PR-3. They will be implemented in a future RUNTIME-DOMAIN-PR-3A skeleton implementation PR after this plan is reviewed and approved.

### Proposed future files

- `src/astra_runtime/domain/transaction_lifecycle.py` — Transaction lifecycle service, stage definitions, request/plan/result shapes, commit-readiness evaluation.
- `src/astra_runtime/domain/event_commitment.py` — Event commitment service, commitment decisions, commitment request/result shapes, commitment evaluation.

### Proposed future public API symbols (transaction_lifecycle.py)

These are proposed future symbols only and must not be created in PR-3:

- `TRANSACTION_LIFECYCLE_STAGES` — frozenset of 18 stage strings
- `TRANSACTION_LIFECYCLE_TERMINAL_STAGES` — frozenset of terminal stages (`committed`, `rejected`, `quarantined`, `cancelled`, `superseded`)
- `TRANSACTION_DEPENDENCY_TYPES` — frozenset of allowed dependency types
- `TRANSACTION_PRECONDITION_TYPES` — frozenset of allowed precondition types
- `TransactionLifecycleError` — base exception
- `InvalidTransactionRequestError` — request validation error
- `InvalidTransactionPlanError` — plan validation error
- `InvalidTransactionResultError` — result validation error
- `InvalidTransactionDependencyError` — dependency validation error
- `InvalidTransactionPreconditionError` — precondition validation error
- `TransactionDependency` — frozen dataclass for dependency declarations
- `TransactionPrecondition` — frozen dataclass for precondition declarations
- `TransactionRequest` — frozen dataclass for transaction opening requests
- `TransactionPlan` — frozen dataclass for in-progress transaction plans
- `TransactionResult` — frozen dataclass for terminal transaction results
- `create_transaction_dependency` — validated factory function
- `create_transaction_precondition` — validated factory function
- `create_transaction_request` — validated factory function
- `create_transaction_plan` — validated factory function
- `create_transaction_result` — validated factory function
- `validate_transaction_dependency` — validation predicate
- `validate_transaction_precondition` — validation predicate
- `validate_transaction_request` — validation predicate
- `validate_transaction_plan` — validation predicate
- `validate_transaction_result` — validation predicate
- `evaluate_commit_readiness` — commit-readiness evaluation function
- `TransactionLifecycleService` — stateless service wrapper class

### Proposed future public API symbols (event_commitment.py)

These are proposed future symbols only and must not be created in PR-3:

- `EVENT_COMMITMENT_DECISIONS` — frozenset of 12 decision strings
- `EVENT_COMMITMENT_BLOCKING_DECISIONS` — frozenset of decisions that prevent commitment
- `EVENT_COMMITMENT_TERMINAL_DECISIONS` — frozenset of terminal decisions (`committed`, plus all rejection/quarantine/cancellation decisions)
- `EventCommitmentError` — base exception
- `InvalidEventCommitmentRequestError` — request validation error
- `InvalidEventCommitmentResultError` — result validation error
- `InvalidEventCommitmentRejectionError` — rejection validation error
- `EventCommitmentRequest` — frozen dataclass for commitment requests
- `EventCommitmentResult` — frozen dataclass for commitment results
- `EventCommitmentRejection` — frozen dataclass for commitment rejection reasons
- `create_event_commitment_request` — validated factory function
- `create_event_commitment_result` — validated factory function
- `create_event_commitment_rejection` — validated factory function
- `validate_event_commitment_request` — validation predicate
- `validate_event_commitment_result` — validation predicate
- `validate_event_commitment_rejection` — validation predicate
- `evaluate_event_commitment` — commitment evaluation function
- `EventCommitmentService` — stateless service wrapper class

---

## 12. Future data shapes

The following data shapes are planned for the future Transaction Lifecycle and Event Commitment service. These are structural definitions only and must not be implemented in PR-3.

### 12.1 TransactionDependency

A frozen dataclass declaring a dependency that must be resolved before the transaction can be committed.

- `dependency_id: str` — unique identifier for this dependency declaration
- `dependency_type: str` — type of dependency, from TRANSACTION_DEPENDENCY_TYPES (e.g., `resource_math`, `combat_resolution`, `ability_resolution`, `inventory_service`, `mission_service`, `social_faction_service`, `generated_content_provenance`, `context_projection`, `model_evaluation`, `live_play_gate`, `validation_integration`, `state_projection`, `transaction_lifecycle`)
- `required: bool` — whether this dependency is required for commitment (True) or optional (False)
- `resolved: bool` — whether this dependency has been resolved (set by the resolution callback, not by the transaction lifecycle service)
- `resolution_ref: str | None` — reference to the resolution result (e.g., delta_id, validation_id)
- `metadata: Mapping[str, Any]` — immutable metadata mapping

### 12.2 TransactionPrecondition

A frozen dataclass declaring an invariant precondition that must hold true at commitment time.

- `precondition_id: str` — unique identifier for this precondition
- `invariant_id: str` — reference to a validation pipeline InvariantPrecheck
- `description: str` — human-readable precondition description
- `severity: str` — severity level if violated (from validation pipeline: `info`, `warning`, `error`, `critical`)
- `required: bool` — whether this precondition is required (True) or advisory (False)
- `metadata: Mapping[str, Any]` — immutable metadata mapping

### 12.3 TransactionRequest

A frozen dataclass representing the initial request to open a transaction.

- `transaction_id: str` — unique transaction identifier
- `command_id: str` — reference to the originating command envelope
- `lifecycle_id: str` — reference to the command lifecycle result that authorized this transaction
- `legality_id: str` — reference to the action legality result
- `source_actor_id: str` — the actor who initiated the command
- `command_type: str` — the type of command being transacted
- `requested_stage: str` — always `transaction_requested`
- `metadata: Mapping[str, Any]` — immutable metadata mapping

### 12.4 TransactionPlan

A frozen dataclass representing the in-progress state of a transaction as it moves through lifecycle stages.

- `transaction_id: str` — unique transaction identifier
- `command_id: str` — reference to originating command
- `lifecycle_id: str` — reference to command lifecycle result
- `legality_id: str` — reference to action legality result
- `source_actor_id: str` — the acting entity
- `command_type: str` — the command type
- `stage: str` — current lifecycle stage (from TRANSACTION_LIFECYCLE_STAGES)
- `actor_ref_id: str | None` — bound actor state record reference
- `projection_id: str | None` — bound state projection reference
- `projection_state_ref_ids: tuple[str, ...] | None` — state ref IDs from the bound projection
- `dependencies: tuple[TransactionDependency, ...]` — declared dependencies
- `preconditions: tuple[TransactionPrecondition, ...]` — declared preconditions
- `delta_ref_id: str | None` — proposed state delta reference
- `delta_change_type: str | None` — change type from the proposed delta
- `delta_affected_record_ids: tuple[str, ...] | None` — affected record IDs from the proposed delta
- `validation_id: str | None` — validation result reference
- `validation_passed: bool | None` — whether validation passed
- `preview_id: str | None` — reference to the transaction preview
- `commit_ready: bool` — whether commit-readiness invariants are all satisfied
- `trace_ids: tuple[str, ...]` — accumulated trace entry references
- `metadata: Mapping[str, Any]` — immutable metadata mapping

### 12.5 TransactionResult

A frozen dataclass representing the terminal result of a transaction.

- `transaction_id: str` — unique transaction identifier
- `command_id: str` — reference to originating command
- `stage: str` — terminal stage (from TRANSACTION_LIFECYCLE_TERMINAL_STAGES)
- `status: str` — terminal status (`committed`, `rejected`, `quarantined`, `cancelled`, `superseded`)
- `event_id: str | None` — committed event ID (only if stage is `committed`)
- `commitment_id: str | None` — event commitment result ID (only if stage is `committed`)
- `rejection_reason: str | None` — rejection reason code (if rejected)
- `quarantine_reason: str | None` — quarantine reason code (if quarantined)
- `cancellation_reason: str | None` — cancellation reason (if cancelled)
- `superseding_transaction_id: str | None` — superseding transaction ID (if superseded)
- `validation_id: str | None` — final validation result reference
- `trace_ids: tuple[str, ...]` — all trace entry references from the transaction lifecycle
- `audit_ids: tuple[str, ...]` — all audit record references
- `metadata: Mapping[str, Any]` — immutable metadata mapping

### 12.6 EventCommitmentRequest

A frozen dataclass representing a request to commit an event at the event commitment boundary.

- `commitment_request_id: str` — unique commitment request identifier
- `transaction_id: str` — reference to the commit-ready transaction
- `command_id: str` — reference to the originating command
- `delta_ref_id: str` — reference to the proposed state delta
- `event_type: str` — proposed event type (from EventLedgerEntry allowed types)
- `affected_record_ids: tuple[str, ...]` — record IDs affected by this event
- `validation_id: str` — reference to the passing validation result
- `preview_id: str` — reference to the transaction preview
- `hidden_info_safe: bool` — whether hidden-information safety has been confirmed
- `persistence_boundary_request_id: str | None` — reference to the persistence boundary prepare request
- `metadata: Mapping[str, Any]` — immutable metadata mapping

### 12.7 EventCommitmentResult

A frozen dataclass representing the result of an event commitment evaluation.

- `commitment_id: str` — unique commitment result identifier
- `commitment_request_id: str` — reference to the commitment request
- `transaction_id: str` — reference to the transaction
- `command_id: str` — reference to the originating command
- `decision: str` — commitment decision (from EVENT_COMMITMENT_DECISIONS)
- `event_id: str | None` — committed event ID (only if decision is `committed`)
- `rejection: EventCommitmentRejection | None` — rejection details (if rejected or quarantined)
- `replay_audit_id: str | None` — reference to replay audit record (if committed)
- `hash_audit_id: str | None` — reference to hash audit record (if committed)
- `trace_id: str | None` — reference to trace entry for this commitment decision
- `metadata: Mapping[str, Any]` — immutable metadata mapping

### 12.8 EventCommitmentRejection

A frozen dataclass representing the reason an event commitment was rejected or quarantined.

- `rejection_id: str` — unique rejection identifier
- `reason_code: str` — machine-readable rejection reason code (e.g., `validation_failed`, `scope_violation`, `missing_state_reference`, `missing_delta_reference`, `hidden_information_risk`, `idempotency_conflict`, `persistence_boundary_rejected`, `unsupported_event_type`)
- `message: str` — human-readable rejection message
- `severity: str` — severity level (from validation pipeline severities: `info`, `warning`, `error`, `critical`)
- `hidden_info_safe: bool` — whether the rejection reason itself is safe to expose to players (some rejections reference hidden state)
- `player_visible: bool` — whether the rejection should be communicated to the player
- `triggering_issue_ids: tuple[str, ...]` — references to ValidationIssue codes or other issue identifiers that triggered the rejection
- `metadata: Mapping[str, Any]` — immutable metadata mapping

---

## 13. Commit-readiness invariants

The following commit-readiness invariants must all be satisfied before a transaction may be declared `ready_for_event_commitment`. These are planning-only invariant definitions. The validation rules themselves will be implemented in a future PR.

1. **Accepted command reference required:** No transaction may proceed without an accepted command reference. The transaction must have a valid, non-empty command_id that references a validated CommandEnvelope.

2. **Lifecycle stage terminal and accepted:** The originating CommandLifecycleResult must be at terminal stage `accepted_for_transaction_planning` with status `accepted`.

3. **Legality decision non-blocking:** The originating ActionLegalityResult must have decision `legal` or `requires_confirmation` (with confirmation received). No blocking decisions may be present.

4. **Actor reference valid:** The transaction must have a valid actor_ref_id that references an existing StateRecordRef with a valid record identity format.

5. **State projection materialized:** The transaction must reference a StateProjectionResult at status `materialized` that covers the affected scope.

6. **All required dependencies resolved:** Every TransactionDependency with `required=True` must have `resolved=True` and a non-null `resolution_ref`.

7. **All required preconditions satisfied:** Every TransactionPrecondition with `required=True` and severity `error` or `critical` must be satisfied by a passing ValidationResult.

8. **Proposed delta present and valid:** The transaction must have a non-null delta_ref_id referencing a valid StateDeltaEnvelope with at least one affected_record_id.

9. **Validation reference required:** No event may be committed without a validation reference. The transaction must have a non-null validation_id referencing a ValidationResult with `passed=True` and no issues with severity `error` or `critical`.

10. **Transaction preview valid:** The transaction must reference a valid TransactionPreview with status `preview_created` (not `preview_rejected` or `preview_quarantined`).

11. **Hidden-information safety confirmed:** No affected_record_id in the proposed delta may reference a record with visibility tier `backend_hidden` or `restricted` unless the event commitment request explicitly declares `hidden_info_safe=True` with supporting justification.

12. **No idempotency conflict:** No previously committed event for the same command_id and same affected_record_ids scope may exist.

13. **Persistence boundary prepared:** The persistence boundary prepare step for operation_type `event_append_prepare` must have returned status `prepared` for the proposed event.

14. **Trace references declared:** At least one RuntimeTraceEntry reference must exist for the current transaction lifecycle.

---

## 14. Corpus-scale transaction pressure review

The following 22 categories represent expected transaction and event pressure from the Astra Ascension corpus. For each category, this section reviews whether the transaction lifecycle service coordinates it, whether event commitment can commit it, which downstream domain owner must calculate it, what remains blocked, and what future tests are required.

| Category | Transaction Lifecycle Coordinates | Event Commitment Can Commit | Downstream Domain Owner | Blocked Until | Required Future Tests |
|---|---|---|---|---|---|
| Basic player actions (move, look, talk, use) | Yes — binds command, actor, state projection | Yes — after action delta passes validation | RT-001 command lifecycle | None (skeleton exists) | Basic player actions commitment test |
| Melee attack resolution | Yes — binds command, actor, target, combat context | Yes — after combat resolution delta passes validation | RT-003 combat / hazard / damage / recovery | RT-003 domain resolution service exists | Combat transaction round-trip test |
| Ranged attack resolution | Yes | Yes | RT-003 | RT-003 exists | Ranged combat transaction test |
| Spell/power invocation | Yes — binds ability reference, resource cost, target | Yes — after ability resolution delta passes validation | RT-004 ability / effect / skill binding | RT-004 exists | Spell invocation transaction test |
| Ability activation (non-spell) | Yes | Yes | RT-004 | RT-004 exists | Ability activation transaction test |
| Resource consumption (HP, mana, stamina) | Yes — declares RT-002 dependency | Yes — after resource math delta | RT-002 resource / consequence math | RT-002 exists | Resource consumption transaction test |
| Resource recovery (rest, healing) | Yes | Yes | RT-002 + RT-003 | RT-002 and RT-003 exist | Recovery transaction test |
| Item pickup / drop / equip | Yes — declares RT-010 dependency | Yes — after inventory delta | RT-010 inventory / item / vehicle / asset | RT-010 exists | Inventory transaction test |
| Item use (consumable) | Yes — declares RT-010 + RT-002 | Yes | RT-010 + RT-002 | Both exist | Consumable use transaction test |
| Crafting / salvage | Yes | Yes | RT-010 + RT-002 | Both exist | Crafting transaction test |
| Vehicle boarding / operation | Yes | Yes | RT-010 | RT-010 exists | Vehicle transaction test |
| Mission acceptance / progress / completion | Yes — declares RT-006 dependency | Yes — after mission delta | RT-006 mission / reward / clue routing | RT-006 exists | Mission progress transaction test |
| Clue discovery / clue routing | Yes | Yes | RT-006 | RT-006 exists | Clue discovery transaction test |
| Reward distribution | Yes | Yes | RT-006 + RT-002 | Both exist | Reward distribution transaction test |
| Social interaction / persuasion | Yes — declares RT-007 dependency | Yes — after social delta | RT-007 social / faction / actor knowledge | RT-007 exists | Social interaction transaction test |
| Faction standing change | Yes | Yes | RT-007 | RT-007 exists | Faction standing transaction test |
| Knowledge/lore acquisition | Yes | Yes | RT-007 + RT-005 | Both exist | Knowledge acquisition transaction test |
| Environmental hazard encounter | Yes | Yes — after hazard delta | RT-003 + RT-009 (if random) | RT-003 exists | Hazard encounter transaction test |
| Random table resolution | Yes — declares RT-009 dependency | Yes — after table oracle result feeds into domain delta | RT-009 runtime RNG / table oracle | RT-009 exists | Random table transaction test |
| Generated content introduction | Yes — declares RT-008 dependency | Yes — with provenance metadata | RT-008 generated-content provenance | RT-008 exists | Generated content transaction test |
| Map/location transition | Yes — declares RT-010 (vehicle) or RT-006 (mission) | Yes | RT-006 or RT-010 | Respective owner exists | Location transition transaction test |
| Hidden information reveal | Yes — special handling for visibility tier changes | Yes — with hidden-info safety confirmation | RT-005 context packet / hidden information | RT-005 exists | Hidden reveal transaction test |
| D-series design promotion attempt | Yes — must detect and block | No — must reject | RT-012 D-series promotion boundary | RT-012 exists | Promotion rejection transaction test |

---

## 15. Risk review

The following 16 risks have been identified for the Transaction Lifecycle and Event Commitment service plan. For each risk, the affected RT owner(s), mitigation strategy, future test family, and whether PR-3A may proceed without hardening are documented.

### Risk 1: Transaction service becomes universal rule engine

- **Affected RT owners:** All (RT-001 through RT-012).
- **Mitigation:** Transaction service coordinates but never resolves domain outcomes. Each domain service (RT-002 through RT-010) owns its own resolution logic. Transaction service must not contain resource formulas, combat rules, ability resolution, or any domain-specific calculation. Skeleton tests must verify no domain logic paths exist.
- **Future test family:** `test_no_domain_rule_engine`
- **PR-3A may proceed without hardening:** Yes, provided skeleton contains no domain-specific logic.

### Risk 2: Premature state mutation through delta application — transaction service mutates state directly

- **Affected RT owners:** All (RT-001 through RT-012).
- **Mitigation:** Transaction lifecycle and event commitment services must never import mutable state operations. All delta references must be read-only. Skeleton tests must verify that no state write paths exist.
- **Future test family:** `test_no_state_mutation_paths`
- **PR-3A may proceed without hardening:** Yes, provided skeleton implementation contains no state write imports.

### Risk 2: Event ledger append bypass

- **Affected RT owners:** RT-001, RT-011.
- **Mitigation:** Event commitment service must not call `create_event_ledger_entry` to append entries. It must only reference EventLedgerEntry shapes for validation. Actual append is a future event-store concern.
- **Future test family:** `test_no_event_append_paths`
- **PR-3A may proceed without hardening:** Yes, provided skeleton implementation contains no event append calls.

### Risk 3: Hidden information leak through committed events

- **Affected RT owners:** RT-005, RT-001.
- **Mitigation:** Commit-readiness invariant #11 requires explicit hidden_info_safe confirmation. Default behavior is rejection if any affected record has `backend_hidden` or `restricted` tier.
- **Future test family:** `test_hidden_information_leak_prevention`
- **PR-3A may proceed without hardening:** Yes, provided skeleton implements conservative rejection for hidden-tier records.

### Risk 4: Event commitment bypasses validation through malformed commit-readiness check

- **Affected RT owners:** RT-011, RT-001.
- **Mitigation:** Commit-readiness evaluation must require ValidationResult.passed=True. No shortcut path that skips validation. Skeleton tests must verify that missing or failing validation blocks commitment.
- **Future test family:** `test_validation_required_for_commitment`
- **PR-3A may proceed without hardening:** Yes.

### Risk 5: Idempotency conflict resolution failure

- **Affected RT owners:** RT-001, all consumers.
- **Mitigation:** Idempotency check based on command_id + affected_record_ids scope. Duplicate detection at the event commitment boundary. Skeleton can declare the check; actual duplicate detection requires event history query which is a future concern.
- **Future test family:** `test_idempotency_conflict_detection`
- **PR-3A may proceed without hardening:** Yes, provided skeleton declares the idempotency check shape without requiring event history access.

### Risk 6: Persistence boundary prepare failure

- **Affected RT owners:** RT-001, RT-011.
- **Mitigation:** Commit-readiness invariant #13 requires persistence boundary prepare status `prepared`. Skeleton tests must verify that non-prepared status blocks commitment.
- **Future test family:** `test_persistence_boundary_gate`
- **PR-3A may proceed without hardening:** Yes.

### Risk 7: Circular dependency between transaction lifecycle and command lifecycle

- **Affected RT owners:** RT-001.
- **Mitigation:** Dependency direction is strictly command_lifecycle -> transaction_lifecycle. Transaction lifecycle does not import from command_lifecycle for stage evaluation; it only reads CommandLifecycleResult as input data. No import cycles.
- **Future test family:** `test_no_circular_imports`
- **PR-3A may proceed without hardening:** Yes, provided import graph is verified.

### Risk 8: Transaction preview coupling creates circular dependency

- **Affected RT owners:** RT-001.
- **Mitigation:** Transaction lifecycle reads TransactionPreview shapes but does not create previews. Preview creation is a kernel concern. Dependency is unidirectional: kernel transaction_preview -> domain transaction_lifecycle (reads), not the reverse.
- **Future test family:** `test_preview_dependency_direction`
- **PR-3A may proceed without hardening:** Yes.

### Risk 9: Domain resolution service does not exist at transaction time

- **Affected RT owners:** RT-002 through RT-010.
- **Mitigation:** Transaction lifecycle declares dependencies but cannot resolve them until downstream domain services exist. Skeleton implementation must handle the case where no domain resolution service is available by keeping the transaction at `domain_resolution_required` stage indefinitely (no timeout in skeleton).
- **Future test family:** `test_unresolved_dependency_handling`
- **PR-3A may proceed without hardening:** Yes, provided skeleton handles missing resolution gracefully.

### Risk 10: Replay audit record without event store

- **Affected RT owners:** RT-011.
- **Mitigation:** Skeleton creates ReplayAuditRecord and HashAuditRecord references but does not persist them. Audit records are emitted as return values; actual storage is a future concern.
- **Future test family:** `test_audit_record_creation_without_persistence`
- **PR-3A may proceed without hardening:** Yes.

### Risk 11: Trace entry overflow from verbose lifecycle tracking

- **Affected RT owners:** RT-011.
- **Mitigation:** Skeleton creates trace entries for every stage transition. In production, trace volume will need throttling or sampling. Skeleton does not implement throttling; it simply accumulates trace_ids as a tuple.
- **Future test family:** `test_trace_entry_accumulation`
- **PR-3A may proceed without hardening:** Yes.

### Risk 12: Model output bypasses transaction boundary

- **Affected RT owners:** All.
- **Mitigation:** Transaction lifecycle and event commitment services do not accept model output as input. All inputs must be structured kernel/domain shapes. No string-to-state conversion paths.
- **Future test family:** `test_no_model_output_inputs`
- **PR-3A may proceed without hardening:** Yes.

### Risk 13: Transaction stage regression (going backward in lifecycle)

- **Affected RT owners:** RT-001.
- **Mitigation:** Transaction lifecycle stages must be monotonically forward-progressing. Skeleton implementation must reject stage transitions that move backward. Allowed transitions must be explicitly enumerated.
- **Future test family:** `test_stage_monotonicity`
- **PR-3A may proceed without hardening:** Yes, provided stage transitions are validated.

### Risk 14: Supersession chain without limit

- **Affected RT owners:** RT-001.
- **Mitigation:** Skeleton declares `superseded` as a terminal stage. Supersession chains are bounded by the fact that each superseding transaction must also complete the full lifecycle. No recursive supersession in a single evaluation.
- **Future test family:** `test_supersession_chain_termination`
- **PR-3A may proceed without hardening:** Yes.

### Risk 15: Donor mechanics become runtime law through events — D-series promotion through transaction bypass

- **Affected RT owners:** RT-012, RT-001.
- **Mitigation:** Source-local/canon boundary: donor mechanics are pressure/variants, never hidden law. Event commitment must track provenance. Transaction lifecycle must check RT-012 promotion boundary before commitment. Skeleton can declare the check; actual enforcement requires RT-012 service which does not yet exist. Conservative behavior: if RT-012 check cannot be performed, reject the transaction.
- **Future test family:** `test_promotion_boundary_enforcement`, `test_no_donor_authority`
- **PR-3A may proceed without hardening:** Yes, provided skeleton includes promotion-boundary check placeholder.

### Risk 16: Commitment decision without trace/audit trail

- **Affected RT owners:** RT-011.
- **Mitigation:** Commit-readiness invariant #14 requires at least one trace entry. Event commitment result must include trace_id and audit references. Skeleton tests must verify that commitment without trace is rejected.
- **Future test family:** `test_commitment_requires_trace`
- **PR-3A may proceed without hardening:** Yes.

---

## 16. Required future hardening ledger

The following hardening items are tracked for the Transaction Lifecycle and Event Commitment service. Each item's current status, risk level, whether it is required before PR-3A, future owner, and recommended PR are documented.

| # | Hardening Item | Current Status | Risk Level | Required Before PR-3A | Future Owner | Recommended PR |
|---|---|---|---|---|---|---|
| 1 | No-state-mutation import guard | Not implemented | High | Yes | PR-3A skeleton | PR-3A |
| 2 | No-event-append import guard | Not implemented | High | Yes | PR-3A skeleton | PR-3A |
| 3 | Hidden-information leak rejection default | Not implemented | High | Yes | PR-3A skeleton | PR-3A |
| 4 | Validation-required-for-commitment gate | Not implemented | High | Yes | PR-3A skeleton | PR-3A |
| 5 | Record identity format validation on all IDs | Not implemented | Medium | Yes | PR-3A skeleton | PR-3A |
| 6 | Command envelope read-only consumption | Not implemented | Medium | Yes | PR-3A skeleton | PR-3A |
| 7 | Transaction preview reference validation | Not implemented | Medium | Yes | PR-3A skeleton | PR-3A |
| 8 | State delta shape-only consumption | Not implemented | Medium | Yes | PR-3A skeleton | PR-3A |
| 9 | Event ledger shape-only consumption | Not implemented | Medium | Yes | PR-3A skeleton | PR-3A |
| 10 | Persistence boundary prepare gate | Not implemented | Medium | Yes | PR-3A skeleton | PR-3A |
| 11 | Replay audit record creation | Not implemented | Medium | Yes | PR-3A skeleton | PR-3A |
| 12 | Runtime trace entry creation | Not implemented | Medium | Yes | PR-3A skeleton | PR-3A |
| 13 | Stage monotonicity enforcement | Not implemented | Medium | Yes | PR-3A skeleton | PR-3A |
| 14 | Idempotency conflict detection placeholder | Not implemented | Low | No | Future event-store PR | PR-3B or later |
| 15 | D-series promotion boundary check placeholder | Not implemented | Low | No | Future RT-012 PR | PR-3B or later |
| 16 | Supersession chain depth guard | Not implemented | Low | No | Future transaction hardening PR | PR-3B or later |
| 17 | Context projection cross-check | Not implemented | Low | No | Future RT-005 integration PR | PR-3B or later |
| 18 | Domain resolution service integration stubs | Not implemented | Low | No | Future RT-002 through RT-010 PRs | PR-4+ |
| 19 | Full corpus-scale transaction pressure tests | Not implemented | Low | No | Future integration test PR | PR-5+ |

---

## 17. Implementation PR authorization boundary

### RUNTIME-DOMAIN-PR-3A authorization

Upon review and approval of this plan (RUNTIME-DOMAIN-PR-3), the following narrow implementation PR is authorized:

**PR name:** RUNTIME-DOMAIN-PR-3A — Transaction Lifecycle and Event Commitment Skeleton Implementation

**What PR-3A may create:**

1. `src/astra_runtime/domain/transaction_lifecycle.py` — frozen dataclass shapes for TransactionDependency, TransactionPrecondition, TransactionRequest, TransactionPlan, TransactionResult. Validated factory functions. Validation predicate functions. Stage constants. Stateless TransactionLifecycleService wrapper. Commit-readiness evaluation function (returns bool/result, does not execute).
2. `src/astra_runtime/domain/event_commitment.py` — frozen dataclass shapes for EventCommitmentRequest, EventCommitmentResult, EventCommitmentRejection. Validated factory functions. Validation predicate functions. Decision constants. Stateless EventCommitmentService wrapper. Commitment evaluation function (returns decision, does not execute).
3. Updates to `src/astra_runtime/domain/__init__.py` to export new public symbols.
4. `tests/runtime/test_domain_transaction_lifecycle_skeleton.py` — comprehensive skeleton tests.
5. `tests/runtime/test_domain_event_commitment_skeleton.py` — comprehensive skeleton tests.

**What PR-3A must not do:**

- Must not execute commands or interpret command semantics.
- Must not apply state deltas or mutate state.
- Must not append events to any ledger or event store.
- Must not perform durable persistence or database operations.
- Must not run replay or enforce hash chains.
- Must not compile context packets or model-facing projections.
- Must not define domain validation rules (may use `run_validation_checks` for shape validation only).
- Must not invoke RNG or table/oracle lookups.
- Must not create hidden-information records.
- Must not import from or couple to domain resolution services (RT-002 through RT-010).
- Must not import mutable state operations from any module.
- Must not bypass the persistence boundary prepare step.
- Must not create non-skeleton business logic (no conditional domain routing, no resolution orchestration, no commitment execution).

---

## 18. Future implementation test requirements

The following test categories are required for the PR-3A skeleton implementation. All tests must be deterministic, must not require external services, and must not mutate state.

### Transaction lifecycle skeleton tests (test_domain_transaction_lifecycle_skeleton.py)

1. **Stage constant coverage** — verify TRANSACTION_LIFECYCLE_STAGES contains all 18 stages, TRANSACTION_LIFECYCLE_TERMINAL_STAGES contains the 5 terminal stages.
2. **TransactionDependency creation and validation** — valid creation, invalid dependency_type rejection, empty dependency_id rejection, metadata immutability.
3. **TransactionPrecondition creation and validation** — valid creation, invalid severity rejection, empty invariant_id rejection, metadata immutability.
4. **TransactionRequest creation and validation** — valid creation, missing command_id rejection, invalid source_actor_id format rejection, metadata immutability.
5. **TransactionPlan creation and validation** — valid creation, invalid stage rejection, stage monotonicity enforcement, metadata immutability, to_dict round-trip.
6. **TransactionResult creation and validation** — valid creation, terminal stage enforcement, non-terminal stage rejection, event_id only when committed, metadata immutability.
7. **Commit-readiness evaluation** — returns True only when all 14 invariants are satisfied, returns False with specific failure reasons for each missing invariant.
8. **TransactionLifecycleService wrapper** — all service methods delegate correctly.
9. **Frozen immutability** — all dataclasses reject attribute assignment.
10. **No state mutation paths** — verify no imports from mutable state modules.
11. **No event append paths** — verify no imports that could append events.
12. **Import graph verification** — verify no circular imports with command_lifecycle, action_legality, state_store, state_projection.

### Event commitment skeleton tests (test_domain_event_commitment_skeleton.py)

1. **Decision constant coverage** — verify EVENT_COMMITMENT_DECISIONS contains all 12 decisions, blocking and terminal decision sets are correct subsets.
2. **EventCommitmentRequest creation and validation** — valid creation, missing transaction_id rejection, invalid event_type rejection, metadata immutability.
3. **EventCommitmentResult creation and validation** — valid creation, event_id only when decision is `committed`, rejection only when decision is rejection/quarantine, metadata immutability.
4. **EventCommitmentRejection creation and validation** — valid creation, invalid severity rejection, empty reason_code rejection, metadata immutability, to_dict round-trip.
5. **Commitment evaluation** — returns `committed` only when all conditions met, returns appropriate rejection decision for each failure mode.
6. **EventCommitmentService wrapper** — all service methods delegate correctly.
7. **Frozen immutability** — all dataclasses reject attribute assignment.
8. **Hidden-information safety gate** — commitment rejected when hidden_info_safe is False and affected records include hidden-tier records.
9. **Persistence boundary gate** — commitment rejected when persistence boundary status is not `prepared`.
10. **Replay audit record creation** — committed events produce valid audit references.
11. **Hash audit record creation** — committed events produce valid SHA-256 hash audit references.
12. **Trace entry creation** — every commitment decision produces a trace entry reference.

---

## 19. Gate finding

```yaml
gate_finding:
  transaction_lifecycle_event_commitment_plan_defined: true
  ready_for_transaction_lifecycle_event_commitment_skeleton_implementation_pr: true
  requires_pr_3b_hardening_before_pr_3a: false
  transaction_lifecycle_code_authorized_by_this_pr: false
  event_commitment_code_authorized_by_this_pr: false
  event_sourcing_authorized_by_this_pr: false
  mutable_runtime_state_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  state_delta_application_authorized_by_this_pr: false
  event_ledger_append_authorized_by_this_pr: false
  durable_persistence_authorized_by_this_pr: false
  database_schema_authorized_by_this_pr: false
  replay_engine_authorized_by_this_pr: false
  command_execution_authorized_by_this_pr: false
  command_parser_authorized_by_this_pr: false
  resource_math_authorized_by_this_pr: false
  combat_resolution_authorized_by_this_pr: false
  ability_resolution_authorized_by_this_pr: false
  inventory_mutation_authorized_by_this_pr: false
  mission_mutation_authorized_by_this_pr: false
  social_faction_mutation_authorized_by_this_pr: false
  generated_content_persistence_authorized_by_this_pr: false
  context_packet_compiler_authorized_by_this_pr: false
  prompt_templates_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  ui_client_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-3A transaction lifecycle and event commitment skeleton implementation
  next_step_status: narrow_skeleton_implementation_pending_review
```

---

## 20. Recommended next PR

The recommended next PR is **RUNTIME-DOMAIN-PR-3A: Transaction Lifecycle and Event Commitment Skeleton Implementation**.

PR-3A should:

1. Implement the frozen dataclass shapes defined in section 12.
2. Implement the validated factory functions and validation predicates defined in section 11.
3. Implement the stage constants and decision constants defined in sections 6 and 7.
4. Implement the commit-readiness evaluation function that checks all 14 invariants from section 13.
5. Implement the commitment evaluation function that returns one of the 12 decisions from section 7.
6. Implement stateless service wrapper classes (TransactionLifecycleService, EventCommitmentService).
7. Update `src/astra_runtime/domain/__init__.py` to export all new public symbols.
8. Create comprehensive skeleton tests per section 18.
9. Verify all 13 hardening items marked "Required Before PR-3A" in section 16.
10. Pass the full existing test suite without regressions.

PR-3A should not exceed the authorization boundary defined in section 17.

After PR-3A is merged, a RUNTIME-DOMAIN-PR-3B review should be conducted to verify the skeleton stayed within scope, similar to the PR-1B and PR-2B review pattern.

---

## 21. Non-implementation reaffirmation

This document reaffirms the following non-implementation constraints:

1. **No code is implemented by this PR.** This is a planning-only document.
2. **No state mutation is authorized.** The transaction lifecycle and event commitment service must never mutate state.
3. **No event append is authorized.** The service must never append events to any ledger or event store.
4. **No durable persistence is authorized.** The service must never write to databases, files, or durable storage.
5. **No replay or hash-chain enforcement is authorized.** The service declares audit references but does not run replay or verify chains.
6. **No domain resolution logic is authorized.** The service coordinates domain resolution dependencies but does not perform resource math, combat resolution, ability resolution, inventory calculation, mission routing, social/faction evaluation, or any RT-002 through RT-010 concern.
7. **No model integration is authorized.** The service does not accept model output, generate prompts, evaluate model responses, or route to models.
8. **No context-packet compilation is authorized.** The service does not compile context packets or assemble model-facing projections.
9. **No validation rule authorship is authorized.** The service consumes validation results but does not define domain validation rules.
10. **No RNG or table/oracle invocation is authorized.** The service does not invoke RNG or resolve table/oracle lookups.
11. **No hidden-information record creation is authorized.** The service reads visibility tiers but does not create or modify hidden-information records.
12. **No donor conversion, sourcebook inclusion, or canon promotion is authorized.** The service does not interact with the conversion pipeline or canon authority.
13. **No D-series promotion is authorized.** The service blocks promotion attempts but does not define promotion policy.
14. **No schema registry mutation is authorized.** The service reads schema IDs but does not register or modify schemas.
15. **No live-play adapter, UI/client adapter, or network transport is authorized.** The service is backend-only.

---

## 22. Classification block

```yaml
runtime_domain_pr_3:
  plan_id: RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001
  artifact_type: transaction_lifecycle_event_commitment_service_plan
  implementation_status: non_executable_plan
  derives_from:
    - RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001
    - RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001
    - RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001
    - RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001
    - RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001
    - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
    - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
    - RT-001
    - RT-005
    - RT-011
  defines_transaction_lifecycle_model: true
  defines_event_commitment_model: true
  defines_transaction_event_boundary: true
  defines_kernel_interface_consumption_plan: true
  defines_domain_service_handoffs: true
  defines_future_implementation_architecture: true
  defines_future_data_shapes: true
  defines_commit_readiness_invariants: true
  defines_corpus_scale_transaction_pressure_review: true
  defines_future_hardening_ledger: true
  authorizes_transaction_lifecycle_code_by_this_pr: false
  authorizes_event_commitment_code_by_this_pr: false
  authorizes_event_sourcing_by_this_pr: false
  authorizes_mutable_runtime_state_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_state_delta_application_by_this_pr: false
  authorizes_event_ledger_append_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_database_schema_by_this_pr: false
  authorizes_replay_engine_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
  authorizes_action_legality_expansion_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_resolution_by_this_pr: false
  authorizes_ability_resolution_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_mutation_by_this_pr: false
  authorizes_social_faction_mutation_by_this_pr: false
  authorizes_generated_content_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-3A transaction lifecycle and event commitment skeleton implementation, pending review
```
