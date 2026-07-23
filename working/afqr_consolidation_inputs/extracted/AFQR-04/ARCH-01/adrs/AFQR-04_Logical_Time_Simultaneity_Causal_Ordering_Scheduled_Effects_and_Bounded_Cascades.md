# AFQR-04 - Logical Time, Simultaneity, Causal Ordering, Scheduled Effects, and Bounded Cascades

**Selected architecture:** Profiled Logical-Time Causal Scheduler with Deterministic Resolution Groups and Bounded Cascade Microsteps  
**Ratification status:** `ratified_architecture_not_implementation_authority`  
**Repository baseline:** `main@928bb79ce00a2de749d127dcc5cb8299de788a15`

## Owned question
Defines temporal authority and causal ordering without relying on wall-clock arrival, worker scheduling, file order, or one donor action economy.

## Central law
> Semantic time is backend-owned logical time governed by registered scheduler profiles. Operations declared simultaneous resolve against a common prestate inside deterministic resolution groups. Causal consequences use typed edges and bounded microsteps. Operational yielding persists a frontier and never changes or truncates semantics.

## Universal components
- Logical-time and timeline references.
- Scheduler-profile registry.
- Typed timing checkpoints and effective-time records.
- Resolution-group definitions with common-prestate semantics.
- Causal edge and dependency ordering contracts.
- Scheduled command and expiry records.
- Bounded cascade microstep budgets.
- Persisted yield and resume frontier.
- Late-evidence invalidation rules around RNG and commit.
- Timeline-branch and source-local temporal handoffs.

## Core contracts
- `LogicalTimeReference`
- `TimelineReference`
- `SchedulerProfile`
- `TimingCheckpoint`
- `ResolutionGroup`
- `CausalEdge`
- `ScheduledCommand`
- `MicrostepBudget`
- `SchedulerFrontier`
- `TemporalConflictReceipt`

## Determination or execution pipeline
1. classify timing profile
2. assign logical time and timing checkpoint
3. discover common-prestate peers
4. freeze the resolution group
5. resolve registered ordering or simultaneity semantics
6. advance bounded causal microsteps
7. persist frontier on operational yield
8. commit authoritative effects through AFQR-01
9. schedule future commands using pinned policy versions

## Ratified constraints and amendments
- Wall-clock duration and network arrival are nonsemantic unless a domain explicitly imports them as evidence.
- Initiative or numeric priority is not universal law.
- A resolution group cannot expand after its common prestate is frozen without invalidation and replanning.
- Late evidence after semantic RNG cannot silently change the selected branch.
- Budget exhaustion yields and persists; it does not truncate consequences.
- Worker order, batch order, and callback order cannot decide outcomes.
- Time travel and closed loops require explicit source-local or later temporal doctrine.

## Guarantees
- Deterministic logical ordering.
- Explicit simultaneity.
- Common-prestate resolution.
- Bounded cascade progress.
- Replayable scheduled work.

## Non-guarantees
- One universal turn or round structure.
- Universal real-time simulation.
- Final time-travel metaphysics.
- Authority to define dependency consequences or state mutation.

## Required non-mutating prototype
A scheduler dry run covering sequential actions, common-prestate groups, conflicting timing claims, expiry, grace, delayed effects, bounded cascades, crash/resume, late evidence, and source-local temporal quarantine.

## Required artifacts
- AFQR-04 ADR
- logical-time doctrine
- scheduler-profile registry
- resolution-group contract
- scheduled-command schema
- microstep frontier and replay fixture pack

## Blocked work
- wall-clock race semantics
- unbounded recursive effects
- silent cascade truncation
- unregistered initiative law

## Work unlocked
- AFQR-06 timed applicability
- AFQR-07 reservation and expiry
- AFQR-09 revocation and cascade timing

## Cross-question handoff
AFQR-04 supplies semantic time and causal grouping to every later validity, settlement, identity, and dependency decision.

## Authority posture
This ADR is architectural doctrine. It does not create runtime state, authorize mutation, promote donor content to canon, or permit model adjudication.
