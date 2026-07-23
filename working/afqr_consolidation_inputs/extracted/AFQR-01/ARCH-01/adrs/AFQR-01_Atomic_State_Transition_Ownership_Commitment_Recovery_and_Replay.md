# AFQR-01 - Atomic State Transition, Ownership, Commitment, Recovery, and Replay

**Selected architecture:** Atomic Typed Transition Journal with Owner-Specific Reducers and Declared Saga Escape Hatches  
**Ratification status:** `ratified_architecture_not_implementation_authority`  
**Repository baseline:** `main@928bb79ce00a2de749d127dcc5cb8299de788a15`

## Owned question
Defines the only lawful route by which authoritative Astra runtime state may change across one or more state owners while preserving invariants, atomicity, idempotency, replay, and recovery.

## Central law
> Every authoritative state change is a typed transition committed through the journal. Each state component has one exclusive write owner, owner-specific reducers prepare local mutation fragments, and the coordinator may validate and assemble but may not mutate participant state. Inseparable effects commit atomically. A saga is permitted only when the operation is explicitly declared external, distributed, or long-running and cannot lawfully fit inside one atomic boundary.

## Universal components
- Typed transition proposal and immutable transition identity.
- Exclusive write-owner registry at component or record-family scope.
- Owner-mediated read projections and owner-specific reducer contracts.
- Precondition, constitutional-invariant, and owner-fragment feasibility gates.
- Frozen write set and composite transition validation.
- Atomic journal commit with append-only transition and event receipts.
- Idempotency keys for proposal, attempt, and commit delivery.
- Canonical pre-state and post-state hashes plus replay evidence.
- Compensation records rather than silent rollback of committed history.
- Declared saga escape hatches with durable progress and bounded authority.

## Core contracts
- `TransitionProposal`
- `OwnerReadProjection`
- `OwnerFragmentRequest`
- `OwnerPreparedFragment`
- `CompositeTransitionPlan`
- `InvariantValidationReceipt`
- `AtomicWriteSetCertificate`
- `TransitionCommitReceipt`
- `CompensationCommand`
- `SagaDefinition`
- `SagaFrontier`

## Determination or execution pipeline
1. receive a typed transition proposal
2. resolve exclusive state owners
3. freeze the relevant state basis
4. request owner-local projections and prepared fragments
5. validate constitutional invariants and cross-fragment coherence
6. freeze the atomic write set
7. commit journal entry and owner fragments atomically
8. emit private and visible receipts
9. schedule only declared separable descendants or compensation

## Ratified constraints and amendments
- No coordinator, model, adapter, bridge, or planner receives direct cross-owner mutation authority.
- One authoritative write owner exists for each mutable component at a given schema version.
- File order, callback order, database order, and worker order are nonsemantic.
- A failed proposal produces no partial authoritative mutation.
- Committed history is corrected through new transitions, not silent edits.
- Technical retries return the prior commit result rather than duplicating effects.
- Saga use is exceptional and must identify compensation, idempotency, durability, and completion policy.
- A transition journal records evidence of mutation; it does not substitute for domain doctrine.

## Guarantees
- Atomicity for inseparable local state effects.
- Exclusive writer discipline.
- Deterministic receipts and replay basis.
- Idempotent commit delivery.
- Explicit compensation and recovery.
- No model-owned mutation path.

## Non-guarantees
- Universal distributed transactions.
- Automatic domain consequence semantics.
- Automatic repair of missing doctrine.
- Rollback of already observed external effects.
- Permission for runtime implementation before gate approval.

## Required non-mutating prototype
A non-mutating transition-assembly dry run that validates owner routing, frozen write sets, fragment coherence, idempotency, invariant failure, compensation classification, and canonical receipt hashes for a small fixture corpus.

## Required artifacts
- AFQR-01 ADR
- exclusive state-owner registry contract
- owner reducer interface
- atomic write-set certificate
- transition journal and receipt schemas
- saga declaration doctrine
- idempotency and compensation fixture pack

## Blocked work
- general state mutation outside a typed transition
- direct owner callbacks that mutate other owners
- silent rollback or history editing
- unbounded saga orchestration

## Work unlocked
- AFQR-02 command attempts
- AFQR-04 resolution groups
- AFQR-07 atomic settlement
- AFQR-09 root cascade commits

## Cross-question handoff
All later AFQRs must produce evidence, plans, or owner fragments that terminate at AFQR-01 for authoritative mutation.

## Authority posture
This ADR is architectural doctrine. It does not create runtime state, authorize mutation, promote donor content to canon, or permit model adjudication.
