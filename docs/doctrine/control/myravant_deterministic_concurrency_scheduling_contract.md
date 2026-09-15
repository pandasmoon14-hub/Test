# Myravant Deterministic Concurrency and Scheduling Contract — PR2-CONC

```yaml
artifact_id: PR2-CONC-DETERMINISTIC-CONCURRENCY-SCHEDULING-001
status: active_control_doctrine
layer: 0_control
workstream: PR2-CONC
authority_reference: owner_directive_2026-09-14_pr2_conc_activation
authority_effect: runtime_concurrency_contract_only
starting_baseline: 0c24b4dad5e2f8e35b93cfb38632c5d3fb92b96a
inherits:
  - POST-R2A-TRANSITION-PROGRAM-001
  - PR2-SCALE-RUNTIME-SCALABILITY-EXECUTION-TOPOLOGY-001
  - PR2-PART-AUTHORITY-PARTITIONING-MIGRATION-001
  - AFQR-01-09-R1D-CORE-TRANSACTION-IDENTITY-RELATION-001
  - AFQR-R2B-CORE-QUALIFICATIONS-001
runtime_implementation_authority: none
production_schema_authority: none
semantic_commitment_owner_authority: none
command_identity_authority: none
logical_time_authority: none
event_delivery_semantics_authority: none
persistence_recovery_semantics_authority: none
fidelity_semantics_authority: none
performance_budget_authority: none
database_selection_authority: none
message_bus_selection_authority: none
cloud_provider_selection_authority: none
native_content_authoring_authority: none
canon_authority: none
model_training_authority: none
live_play_authority: none
```

## 1. Purpose

PR2-CONC defines the runtime-architecture contract for **deterministic
authoritative behavior under concurrent execution**.

It answers the bounded questions deliberately left by PR2-SCALE and PR2-PART:

- what may be computed concurrently;
- why physical execution order is nonauthoritative;
- how authoritative commitment is insulated from scheduler timing;
- how competing candidate effects are classified before commitment;
- how explicit semantic ordering or simultaneity is consumed;
- how speculative, repeated, abandoned, or recomputed work remains
  nonauthoritative until lawfully committed;
- how cross-partition concurrent work preserves one lawful semantic outcome;
- when missing conflict/order doctrine must fail closed or escalate.

The governing flow is:

```text
accepted Myravant semantics
-> AFQR logical-time / commitment / command owners
-> PR2-SCALE topology-independence law
-> PR2-PART responsibility-boundary law
-> PR2-CONC concurrency qualification and deterministic-commitment contract
-> later EVENT / PERSIST / FID / BP contracts as applicable
-> later authorized implementation
-> concurrency-equivalence evidence
```

PR2-CONC owns only this runtime concurrency-contract layer.

## 2. Why this owner exists

Parallel work can improve throughput and latency, but physical concurrency can
silently become hidden game law if the project accepts rules such as:

```text
first thread to finish wins
first worker to respond commits
first packet to arrive becomes earlier in world time
last database write becomes canonical
worker count changes conflict winners
race timing decides randomness
```

Those are prohibited.

Physical execution may be concurrent.

Authoritative semantics must remain governed by explicit Myravant owners.

## 3. Existing owners retained

### AFQR-01

AFQR-01 retains qualified state/write ownership, owner-specific reducers,
commitment, recovery, replay, and transition receipts.

PR2-CONC may define how concurrent candidate work is qualified and ordered for
submission to lawful commitment. It does not become the semantic commitment
owner.

### AFQR-02

AFQR-02 retains command identity, attempt identity, retry identity, suspension,
escalation, and durable command progress.

PR2-CONC may distinguish technical recomputation from authoritative commitment.
It does not decide whether a retry, recomputation, replacement, or resumed
operation is the same command or attempt.

### AFQR-04

AFQR-04 retains logical time, causal ordering, simultaneity, scheduling,
deterministic resolution groups, and bounded cascades.

PR2-CONC consumes those semantic ordering structures. It does not replace them
with thread, worker, queue, lock, or message order.

### Other domain owners

Reservation, settlement, conservation, relations, legality, identity,
visibility, correction, and other domain semantics remain with their existing
owners.

Concurrency coordinates their lawful effects. It does not redefine them.

## 4. What PR2-CONC owns

PR2-CONC owns only:

- physical-concurrency nonauthority;
- runtime scheduler nonauthority;
- independently computable work qualification;
- concurrency dependency declaration;
- concurrency-conflict classification;
- deterministic authoritative-commitment qualification;
- authoritative order consumption;
- simultaneous-group execution preservation;
- speculative-computation boundaries;
- recomputation/cancellation boundaries;
- worker-count equivalence obligations;
- cross-partition concurrent-commitment preservation;
- fail-closed missing-order/conflict handling;
- concurrency evaluation envelopes and evidence;
- bounded downstream handoffs.

## 5. What PR2-CONC must not own

PR2-CONC must not define or implement:

- gameplay action economies;
- universal initiative;
- universal rounds, turns, ticks, phases, or frames;
- logical-time doctrine;
- simultaneity doctrine;
- source-local timing metaphysics;
- command or attempt identity;
- retry identity;
- semantic state ownership;
- qualified write ownership;
- semantic commitment ownership;
- event/message delivery semantics;
- durable replay/recovery;
- snapshotting;
- persistence reconstruction;
- fidelity tiers or aggregation;
- performance budgets;
- overload/backpressure policy;
- partition identity or migration semantics;
- branch/canon identity;
- correction taxonomy;
- universal conflict-resolution policy;
- universal lock model;
- universal transaction model;
- consensus protocols;
- distributed locks;
- two-phase commit;
- sagas;
- actor protocols;
- replication algorithms;
- leader election;
- database choice;
- message-bus choice;
- cloud-provider choice;
- production runtime code;
- production schemas;
- native content;
- canon promotion;
- source/corpus execution;
- model training;
- conversion execution;
- live-play/GM behavior;
- R3 execution.

## 6. Core concurrency nonauthority law

Concurrent execution is a physical execution strategy.

It is not automatically world simultaneity, causal priority, commitment
priority, conflict priority, ownership, authority, truth, or game-time order.

```text
physical concurrency
!= semantic simultaneity

physical completion order
!= authoritative order

scheduler choice
!= conflict resolution

worker assignment
!= state ownership
```

## 7. Determinism means runtime-authority determinism

PR2-CONC does not require every Myravant mechanic to be deterministic.

A lawful mechanic may include dice, cards, oracle draws, source-local
randomness, explicit player choice, GM-authorized choice, branch-qualified
choice, or another separately governed uncertainty source.

For PR2-CONC, determinism means:

> Holding constant the authoritative semantic inputs, applicable version
> context, declared ordering/simultaneity basis, and required randomness or
> choice provenance, physical concurrency must not invent an additional outcome
> difference.

Concurrency must not become a hidden randomizer.

## 8. Reference-concurrency law

A bounded concurrent execution may be compared against a simpler lawful
reference execution.

The reference role may be serial, single-worker, single-process, deliberately
inspectable, or otherwise simplified.

The reference does not become permanent production architecture.

## 9. Independently computable work

Work is **independently computable for the declared envelope** only when
executing it concurrently cannot by itself determine a semantically material
difference.

Independence may depend on authoritative input dependencies, state-read
dependencies, candidate-write dependencies, logical-time relations,
resolution-group membership, resource/reservation interactions,
identity/relation constraints, version context, randomness provenance, and
hidden-information boundaries.

Independence is a qualified claim, not a universal property of an operation
name.

## 10. Independence is not permanent commutativity

Two operations that are independent in one state or workload may conflict in
another.

Examples include two movements that later target one exclusive location, two
purchases competing for the final unit, two crafting jobs sharing a reservation,
two social updates touching one governed relation, or two world processes
affecting the same ecological stock.

## 11. Candidate computation is not commitment

A worker may calculate, simulate, prefetch, predict, pathfind, evaluate legality,
build a candidate delta, compute an AI option, or prepare a stochastic candidate
where separately lawful.

None of that makes the result authoritative.

Only an existing lawful commitment route can create authoritative consequence.

## 12. Scheduler nonauthority

Thread scheduling, coroutine scheduling, worker scheduling, OS scheduling,
executor scheduling, queue polling order, process completion order, host
response order, and accelerator completion order must not select authoritative
truth merely by happening first.

A scheduler may choose computational order. It may not invent semantic priority.

## 13. Message arrival nonauthority

Network or transport arrival order does not automatically establish logical
time, causality, command priority, conflict priority, or commitment priority.

PR2-EVENT will later define command/event/message delivery boundaries.

PR2-CONC only establishes that transport timing is not the conflict oracle.

## 14. Wall-clock nonauthority

Wall-clock timestamps, CPU time, network latency, or elapsed execution time do
not automatically become logical world time.

A timeout may have semantic meaning only when an existing semantic owner
explicitly gives it such meaning.

## 15. Authoritative ordering must have an explicit basis

When order matters to authoritative outcome, the ordering basis must be
attributable to an existing lawful semantic source.

Examples may include AFQR-04 causal order, scheduled-effect order, deterministic
resolution-group rules, explicit source-local priority retained by doctrine, a
lawfully versioned domain rule, a lawfully committed choice, or a separately
governed randomness result.

Worker timing is never an acceptable substitute.

## 16. Semantic simultaneity may execute sequentially

Operations that are semantically simultaneous do not have to execute on CPU
cores at literally the same instant.

A runtime may evaluate them serially, in parallel, in batches, or through staged
candidate computation, but it must preserve the authoritative semantics of the
declared simultaneous or resolution-group envelope.

Implementation sequence must not silently become semantic sequence.

## 17. Physical concurrency may represent semantic sequence

A runtime may compute later-semantic work early or concurrently when doing so is
safe.

Early computation does not move that work earlier in logical time.

Its authoritative effect remains governed by the explicit semantic order.

## 18. Concurrency conflict classification

Before competing candidate effects are committed, a bounded concurrency case
must be classifiable into a lawful category such as:

- `independent_for_declared_envelope`;
- `explicitly_ordered_by_existing_semantics`;
- `simultaneous_under_existing_resolution_group`;
- `exclusive_or_conflicting_under_existing_domain_rule`;
- `speculative_only`;
- `missing_required_order_or_conflict_doctrine`;
- `unsupported_concurrency_case`.

These are runtime-contract classifications. They do not replace domain-specific
conflict semantics.

## 19. Independent work may be freely scheduled computationally

Where work is proven independent for the relevant envelope, the runtime may
change worker assignment, thread count, batch shape, execution order, host
placement, or accelerator use.

Those changes must not alter authoritative result.

## 20. Ordered work must preserve authoritative order

If existing semantics require A before B, physical execution may speculate on B
early only when B cannot commit as though it preceded A.

The authoritative result must remain equivalent to the declared order.

## 21. Simultaneous groups require group-law preservation

When AFQR-04 or another lawful owner establishes a resolution group, the runtime
must preserve the group's declared semantics.

A loop that evaluates members one by one must not leak first-iteration privilege
unless the semantic owner explicitly allows it.

Likewise, parallel evaluation must not manufacture equality where the semantic
owner establishes priority.

## 22. Conflicting work needs a semantic resolution basis

When candidate effects cannot all be lawfully committed together, the runtime
must not let implementation timing choose the winner.

A lawful case requires an existing ordering rule, existing conflict-resolution
rule, existing reservation/settlement rule, existing explicit choice or
randomness route, a fail-closed outcome, or escalation for missing doctrine.

PR2-CONC does not invent a universal winner rule.

## 23. Missing conflict doctrine fails closed

If a material concurrent case requires a winner/order and no accepted semantic
owner supplies one, the runtime must not improvise from thread ID, worker ID,
database order, wall-clock timestamp, queue position, hash order, or network
arrival.

The lawful result is nonauthoritative, unsupported, inconclusive pending
doctrine, or escalated to the relevant owner.

## 24. Commitment remains owner-qualified

PR2-CONC may define a deterministic concurrency gate before commitment.

It does not redefine AFQR-01 commitment.

A concurrency gate may determine that candidate work is independent and
commit-eligible, ordered and commit-eligible only in a declared sequence,
group-qualified, conflicted and awaiting semantic resolution, invalidated,
nonauthoritative, or unsupported.

The actual state transition remains subject to the qualified state/write owner.

## 25. One concurrent attempt must not manufacture duplicate commitment

Multiple workers may compute or submit equivalent candidate work.

That does not authorize duplicated authoritative consequences.

Duplicate-commit prevention consumes AFQR-01 commitment/replay law, AFQR-02
command/attempt identity, later PR2-EVENT delivery identity where applicable,
and later PR2-PERSIST recovery where applicable.

## 26. Speculation is nonauthoritative

Speculative concurrent work may be useful for AI planning, pathfinding,
forecasts, candidate legality, predictive simulation, rendering support, cache
warming, or branch-local evaluation.

Speculation remains nonauthoritative until a lawful commitment path explicitly
accepts a result.

## 27. Recompute is not retry identity

A runtime may recompute an uncommitted deterministic candidate because a cache
was lost, a worker failed, an optimization was abandoned, an input dependency
changed, or a validation pass is repeated.

That physical recomputation does not by itself answer whether a command or
attempt was retried.

AFQR-02 retains command/attempt/retry identity.

## 28. Recompute cannot reroll committed randomness

Technical recomputation, worker replacement, concurrent duplication, or
scheduler changes must not reroll an already committed randomness-bearing
outcome.

R2B-CORE remains authoritative.

## 29. Uncommitted stochastic candidates require explicit qualification

If a system computes stochastic candidates before commitment, the project must
know whether the randomness itself is already authoritative evidence or only
speculative computation.

PR2-CONC does not mandate one RNG architecture.

If the distinction cannot be established from existing doctrine, the case must
escalate rather than silently letting worker order consume randomness.

## 30. Worker-count equivalence

Changing worker count must not silently change conflict winners, semantic
ordering, committed RNG outcomes, command identity, legality, reservation
settlement, relation outcomes, version applicability, logical time, correction
history, or visibility.

A case that changes those outcomes solely because worker count changed is not
concurrency-equivalent.

## 31. Process- and host-count equivalence

Moving concurrent work from one process/host to many processes/hosts creates
cost, latency, transport, failure, and coordination pressure.

It does not create new world semantics.

If the implementation cannot preserve the required concurrency contract, that
topology is unsupported for the affected envelope.

## 32. Cross-partition concurrency consumes PR2-PART

PR2-PART retains logical partition identity, runtime responsibility,
migration/cutover semantics, and partition failure exposure.

PR2-CONC owns competing schedules and deterministic authoritative commitment
across those responsibility boundaries.

Partition placement does not choose a conflict winner.

## 33. Cross-partition interaction still requires one lawful outcome

A bounded interaction spanning partitions must resolve according to the same
semantic rules that would apply if colocated.

PR2-CONC does not require distributed transactions, two-phase commit, consensus,
locks, sagas, actors, or event sourcing.

These are possible implementation techniques, not doctrine.

## 34. Split-brain cannot be resolved by fastest response

If multiple execution placements temporarily believe they may perform the same
work, whichever responds first does not thereby gain semantic priority.

PR2-PART owns responsibility ambiguity.

PR2-CONC requires that competing schedules not create divergent authoritative
commitment.

## 35. Reservation and settlement remain domain-owned

Concurrent resource pressure is common in inventories, markets, crafting,
requisition, action costs, vehicle capacity, and institutions.

PR2-CONC must preserve existing reservation/settlement/conservation semantics.

It must not invent a universal optimistic or pessimistic reservation model.

## 36. Version context is part of the concurrency envelope

Concurrent work must not mix incompatible ruleset/package/override contexts
merely because workers began at different times.

R2B-CROSS-PHASE retains version identity, pinning, applicability, and effective
intervals.

## 37. Logical-time context is part of the concurrency envelope

A candidate computed from one logical-time or causal context cannot silently
commit under another if the difference is semantically material.

PR2-CONC does not define stale-command semantics.

If a case requires general expected-version/stale-command doctrine not already
owned, it follows the existing escalation route rather than being invented here.

## 38. Visibility and hidden information survive concurrency

Concurrent execution must not broaden access merely because another worker,
process, or cache has the data.

Speculation must not expose hidden authoritative inputs to an unauthorized
consumer.

## 39. Cancellation of computation is not cancellation of committed fact

A worker can abandon uncommitted computation without world consequence.

A committed consequence cannot disappear because the worker is cancelled, the
process exits, a future/promise is dropped, a task queue is cleared, or a client
disconnects.

Durable reconstruction belongs to PR2-PERSIST.

## 40. Failure before commitment

If computation fails before authoritative commitment, the runtime may recompute,
reassign, abandon, or report unsupported/inconclusive, subject to existing
command/attempt/randomness semantics.

Failure itself does not create an authoritative result.

## 41. Failure during or after commitment

A failure boundary must not manufacture partial semantic truth, duplicate
commitment, arbitrary winner selection, lost committed consequence, or rerolled
committed randomness.

AFQR-01 remains commitment/replay owner.

PR2-PERSIST will later own durable reconstruction.

PR2-EVENT will later own delivery/retry boundaries.

## 42. EVENT handoff

PR2-EVENT must define command/event/message separation, transport-attempt
identity, delivery/retry semantics, causality metadata carried by messages, and
projection rebuilding boundaries.

PR2-CONC establishes that message arrival cannot define authoritative ordering.

PR2-CONC does not activate PR2-EVENT.

## 43. PERSIST handoff

PR2-PERSIST must define how authoritative state and concurrency-relevant evidence
survive snapshots, restart, replay, recovery, reconstruction, and corruption
handling.

PR2-CONC does not activate PR2-PERSIST.

## 44. FID handoff

PR2-FID must define aggregate/detail transitions and reconstitution.

Concurrency must not become an excuse for lower-fidelity representations to
create different committed semantics.

PR2-CONC does not activate PR2-FID.

## 45. BP handoff

PR2-BP must define overload, backpressure, prioritization, and lawful
degradation.

Overload may delay or reject work under later law. It must not silently let
scheduler pressure decide truth.

PR2-CONC does not activate PR2-BP.

## 46. R3 boundary

The frozen 34-record R3 conformance target may be inspected as pressure evidence
when checking whether the concurrency contract leaves runtime/schema constructs
without a lawful owner.

PR2-CONC does not:

- execute R3;
- disposition R3 records;
- change the selector;
- change the record count;
- promote runtime implementation assumptions into doctrine.

R3 remains separately authorized.

## 47. Concurrency evidence envelope

A material concurrency-equivalence case should eventually be able to preserve:

```text
concurrency_case_id
reference_execution_id
candidate_execution_id
semantic_version_context
initial_authoritative_state_ref
authoritative_input_ref
logical_time_or_resolution_group_context
command_attempt_context
randomness_or_choice_provenance
dependency_set
conflict_classification
authoritative_order_basis
worker_process_host_envelope
candidate_effects
commitment_result
equivalence_result
constraint_or_failure_reason
```

This is an evidence shape, not a mandatory production schema.

## 48. Result vocabulary

A bounded concurrency evaluation may lawfully conclude:

- `equivalent_within_declared_concurrency_envelope`;
- `equivalent_with_declared_constraints`;
- `lawfully_ordered_by_existing_semantics`;
- `lawfully_simultaneous_under_existing_semantics`;
- `nonauthoritative_speculation_only`;
- `not_equivalent`;
- `inconclusive_missing_domain_resolution`;
- `inconclusive_missing_event_contract`;
- `inconclusive_missing_persistence_contract`;
- `inconclusive_missing_evidence`;
- `unsupported_concurrency_case`.

Unknown does not become pass.

## 49. Corpus-scale pressure families

PR2-CONC must survive pressure from at least:

- turn-based tactical systems;
- simultaneous-turn systems;
- interrupt/reaction systems;
- initiative systems;
- phase-based systems;
- tick-based systems;
- continuous-time-like source systems;
- asynchronous command systems;
- high-density combat;
- mass combat;
- global markets;
- auctions and limited stock;
- crafting/reservation contention;
- institution and government processes;
- ecological competition;
- social/relation updates;
- distributed or swarm embodiment;
- multi-body actors;
- crew-dependent vehicles/ships;
- companion/summon systems;
- background populations;
- large batches of independent processes;
- small sets of heavily coupled processes;
- deterministic procedures;
- stochastic procedures;
- mixed deterministic/stochastic procedures;
- correction/replacement pressure;
- cross-partition interaction;
- migration-adjacent concurrent work;
- client prediction/speculation;
- offline or deferred computation.

No donor family establishes universal concurrency law.

## 50. Important outliers

Escalate rather than invent when a case requires new domain conflict semantics,
new simultaneity doctrine, new logical-time doctrine, new command identity law,
new commitment ownership, new reservation/settlement law, new personhood or
identity law, source-local metaphysics where concurrency changes ontology, a
universal stale-command rule, or a mandatory consensus/transaction algorithm.

PR2-CONC is not a semantic super-owner.

## 51. Anti-collapse rules

PR2-CONC must not collapse:

- computation into commitment;
- physical order into causal order;
- physical concurrency into semantic simultaneity;
- scheduler choice into conflict resolution;
- worker identity into semantic ownership;
- retry/recompute into command identity;
- queue order into world order;
- transport arrival into causality;
- timeout into logical time;
- database transaction order into game law;
- worker failure into world consequence;
- concurrent execution into a requirement for distributed infrastructure.

## 52. Completion condition

PR2-CONC is complete when the repository contains a machine-testable contract
that explicitly bounds independent computation, scheduler nonauthority,
physical-versus-authoritative order, conflict classification, deterministic
commitment qualification, semantic simultaneity preservation,
speculation/recompute/cancellation, worker/process/host-count equivalence,
cross-partition concurrent commitment, and downstream ownership.

It must preserve AFQR-01 commitment ownership, AFQR-02 command/attempt/retry
identity, AFQR-04 logical time/simultaneity/scheduling ownership, PR2-SCALE
topology independence, PR2-PART partition/migration ownership, R2B randomness
preservation, separate EVENT/PERSIST/FID/BP ownership, R3 authorization
boundaries, and no runtime implementation or technology mandate.

Completion of PR2-CONC does not prove that a parallel or distributed production
runtime exists. It proves only that future concurrent implementations have a
lawful semantic contract to satisfy.
