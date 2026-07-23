# AFQR-02 - Command Identity, Attempts, Retries, Suspension, Escalation, and Durable Progress

**Selected architecture:** Synchronous Command Fast Path with Durable Attempt Escalation  
**Ratification status:** `ratified_architecture_not_implementation_authority`  
**Repository baseline:** `main@928bb79ce00a2de749d127dcc5cb8299de788a15`

## Owned question
Defines how player intent becomes immutable commands and execution attempts, how technical retries differ from semantic changes, and when an operation remains synchronous versus becoming durable or resumable.

## Central law
> A compiled command is immutable. Technical retries preserve command and attempt identity; a material change of method, target, cost, risk, timing, or expected effect requires a new attempt or command. Ordinary operations use the synchronous fast path. Only operations that cross an explicit durability boundary escalate into a persisted attempt with a resumable frontier.

## Universal components
- Raw-input capture separated from IntentIR, CommandIR, and AttemptRecord.
- Command identity, attempt identity, execution identity, and delivery identity separation.
- Synchronous fast-path state machine.
- Durable-attempt escalation criteria and persisted attempt frontier.
- Clarification and confirmation checkpoints.
- Frozen state basis and semantic RNG boundary.
- Cancellation, timeout, supersession, and stale-attempt handling.
- Idempotent technical retry and duplicate delivery handling.
- Child-command and descendant-attempt relationship.
- Visibility-safe attempt status projections.

## Core contracts
- `RawInputRecord`
- `IntentIR`
- `CommandEnvelope`
- `CommandAttempt`
- `AttemptStateBasis`
- `ClarificationRequest`
- `ConfirmationRequest`
- `RNGFreezeReceipt`
- `AttemptClosureReceipt`
- `DurableAttemptFrontier`
- `ChildCommandSpecification`

## Determination or execution pipeline
1. capture raw input
2. interpret non-authoritative intent candidates
3. compile one typed immutable command
4. create attempt and state basis
5. clarify or confirm when material information is missing
6. run synchronous validation and resolution where bounded
7. freeze RNG evidence when uncertainty is resolved
8. escalate only when persistence or external progress is required
9. close, commit, reject, or quarantine the attempt

## Ratified constraints and amendments
- A model may propose an intent but cannot create authoritative command meaning outside registered schemas.
- Technical delivery retries cannot generate new rolls, new costs, or duplicate state changes.
- A semantic alternative is not a retry.
- Late evidence before semantic RNG may invalidate and rebuild the attempt basis.
- Late evidence after RNG cannot silently alter the result or enable reroll shopping.
- A suspended attempt retains its exact versions, evidence, and frontier.
- A durable attempt is not a universal workflow engine; it remains bounded to one command family and policy.

## Guarantees
- Immutable command meaning.
- Retry safety.
- Explicit clarification and confirmation.
- No selective reroll after late changes.
- Durable resumption when lawfully required.

## Non-guarantees
- Every command can complete synchronously.
- Automatic doctrine for cancellation consequences.
- Automatic external-service compensation.
- Authority to mutate without AFQR-01.

## Required non-mutating prototype
A command-attempt dry run covering ordinary success, clarification, confirmation, technical retry, stale state, pre-RNG invalidation, post-RNG closure, durable escalation, cancellation, timeout, and child-command creation.

## Required artifacts
- AFQR-02 ADR
- command/attempt identity doctrine
- fast-path state machine
- durable-attempt escalation contract
- RNG checkpoint contract
- retry and closure fixture pack

## Blocked work
- mutable command envelopes
- semantic retries disguised as technical retries
- unbounded background work
- post-RNG reroll shopping

## Work unlocked
- AFQR-03 typed action compilation
- AFQR-04 scheduling
- AFQR-09 durable descendant commands

## Cross-question handoff
AFQR-02 owns command and attempt lifecycle; AFQR-01 owns authoritative commit, and AFQR-04 owns logical timing.

## Authority posture
This ADR is architectural doctrine. It does not create runtime state, authorize mutation, promote donor content to canon, or permit model adjudication.
