# Myravant Performance Budget, Overload, and Backpressure Contract — PR2-BP

```yaml
artifact_id: PR2-BP-PERFORMANCE-BUDGET-OVERLOAD-BACKPRESSURE-001
status: active_control_doctrine
layer: 0_control
workstream: PR2-BP
authority_reference: owner_directive_2026-09-16_pr2_bp_activation
authority_effect: runtime_performance_contract_only
starting_baseline: 59520af5f2a68a5979091c00bb632f0cb5d2600e
inherits:
  - POST-R2A-TRANSITION-PROGRAM-001
  - PR2-SCALE-RUNTIME-SCALABILITY-EXECUTION-TOPOLOGY-001
  - PR2-FID-RELEVANCE-FIDELITY-AGGREGATION-RECONSTITUTION-001
  - PR2-PART
  - PR2-CONC
  - PR2-EVENT
  - PR2-PERSIST
runtime_implementation_authority: none
production_schema_authority: none
semantic_commitment_authority: none
command_identity_authority: none
logical_time_authority: none
identity_authority: none
truth_knowledge_sensing_authority: none
persistence_authority: none
fidelity_authority: none
partitioning_authority: none
concurrency_authority: none
canon_authority: none
live_play_authority: none
```

## 1. Purpose

PR2-BP defines how Myravant remains bounded and authority-safe when demand
exceeds available execution capacity.

It governs:

- workload-envelope declaration;
- performance-budget semantics;
- overload detection;
- admission pressure;
- bounded buffering;
- backpressure;
- prioritization of operational work;
- lawful degradation;
- deferred work;
- hotspot pressure;
- overload containment;
- overload recovery;
- evidence required for performance claims.

It does not implement those mechanisms.

Its central rule is:

> Performance pressure may change how and when lawful work is serviced, but may not silently change authoritative world meaning.

## 2. Existing owners remain authoritative

PR2-BP coordinates existing owners and does not absorb them.

- AFQR-01 retains commitment, replay, recovery, receipts, and qualified
  authoritative mutation.
- AFQR-02 retains command identity, attempts, retries, suspension,
  escalation, and progress.
- AFQR-04 retains logical time, causality, scheduling meaning, and
  authoritative temporal placement.
- AFQR-08 retains identity and continuity.
- AFQR-09 retains governed relations and dependency lifecycle.
- AFQR-10 retains truth, knowledge, belief, memory, uncertainty, and
  projection semantics.
- AFQR-20 retains sensing and detection.
- R2B-CORE retains proposal nonauthority and committed-randomness
  preservation.
- R2B-CROSS-PHASE retains version identity, applicability, pinning,
  and effectivity.
- R2B-CONTINUITY retains timeline, branch, canonicality, and correction.
- PR2-PART retains authority partitioning and migration semantics.
- PR2-CONC retains deterministic concurrency and commitment ordering.
- PR2-EVENT retains command/event/message/projection distinctions.
- PR2-PERSIST retains durable storage, replay, recovery, and
  reconstruction.
- PR2-FID retains relevance, fidelity, aggregation, reconstitution,
  and materialization boundaries.

PR2-BP may constrain operational service behavior around those owners.

It may not redefine them.

## 3. Definitions

**workload envelope** means the declared conditions inside which a
performance or capacity claim is valid.

**performance budget** means a measurable operational target or bound
associated with a declared workload envelope.

**capacity** means the bounded operational ability to service work under
declared conditions.

**pressure** means demand approaching or consuming material portions of
available capacity.

**overload** means a condition in which current or reasonably expected
demand cannot be serviced within the declared operational envelope without
invoking an explicit bounded response.

**backpressure** means an explicit signal or constraint that causes an
upstream producer, caller, scheduler, or workload source to reduce, delay,
redirect, or stop additional demand.

**admission control** means deciding whether work may enter a bounded
operational service path.

**degradation** means substituting a lower-cost behavior that remains lawful
under all applicable semantic owners.

**deferred work** means work intentionally postponed without pretending
that it completed or disappeared.

**hotspot** means concentrated demand whose local interaction density,
contention, or service cost materially exceeds the surrounding workload.

## 4. Performance is not authority

Performance is not authority.


Faster completion does not make an outcome more authoritative.

Slower completion does not make an outcome less authoritative.

Queue position does not create world priority.

Worker availability does not create legality.

Resource scarcity in the host environment does not become an in-world rule.

Operational pressure may not silently alter:

- committed state;
- identity;
- causality;
- version applicability;
- randomness provenance;
- ownership;
- governed relations;
- hidden information;
- committed consequences.

## 5. Budget profiles require declared envelopes

A performance budget is meaningful only relative to a declared workload
envelope.

A budget profile should identify enough context to interpret its claim,
such as:

```text
budget_profile_id
workload_envelope_id
metric_or_resource_dimension
measurement_unit
observation_window_or_sample_basis
applicable_environment
applicable_execution_form
applicable_fidelity_context
threshold_or_target
response_when_exceeded
semantic_protections
evidence_reference
version_or_revision
```

This is a conceptual evidence surface, not a mandated runtime schema.

## 6. Numeric budgets are profile-specific

PR2-BP owns the semantics of numeric performance budgets.

This activation does not invent universal production numbers without
measured evidence.

A threshold valid on one machine, topology, workload mix, fidelity profile,
or release target does not become universal Myravant doctrine.

Numeric values must retain their measurement context.

## 7. Performance numbers are not correctness proofs

Meeting a latency, throughput, memory, CPU, queue, or cost budget does not
prove semantic correctness.

Missing a performance target does not authorize semantic corruption.

Correctness and performance evidence are distinct.

Both may be required.

## 8. Workload envelopes are multidimensional

Relevant dimensions may include:

- active actor count;
- background process count;
- command rate;
- committed event rate;
- scheduled-work rate;
- interaction density;
- hotspot intensity;
- cross-partition interaction;
- persistence volume;
- recovery activity;
- fidelity mix;
- projection demand;
- AI-assisted workload;
- player-facing latency sensitivity;
- hardware and memory envelope;
- storage or network pressure;
- burst shape and duration.

A single player count or entity count is insufficient when other material
dimensions differ.

## 9. No infinite-capacity assumption

Every operational service path must be allowed to acknowledge finite
capacity.

Myravant doctrine does not assume:

- infinite memory;
- infinite queues;
- infinite workers;
- infinite storage bandwidth;
- infinite network bandwidth;
- infinite AI-provider capacity;
- zero-cost retries;
- zero-cost persistence;
- zero-cost reconstruction.

An implementation may choose very large bounds.

It may not rely on infinity as its overload policy.

## 10. Bounded buffering law

If work may queue, the queue or equivalent retained backlog must have a
bounded operational envelope.

The exact implementation may be a queue, scheduler, database, log, heap,
mailbox, work list, or another mechanism.

PR2-BP mandates none of them.

What happens when the bound is reached must be explicit.

## 11. Overflow cannot mean silent disappearance

A full queue or saturated service path may not silently discard work whose
disappearance would change authoritative meaning.

Overflow responses may include, where lawful:

- reject before acceptance;
- defer;
- apply backpressure;
- reduce optional work;
- invoke a lawful cheaper fidelity mode;
- isolate a hotspot;
- surface an explicit failure;
- escalate.

The exact response depends on existing semantic ownership.

## 12. Admission is not commitment

Operational admission and semantic commitment are distinct.

Accepting work into an operational path does not itself commit a world fact.

Conversely, a committed fact does not become uncommitted merely because
downstream service capacity is exhausted.

PR2-BP must preserve that distinction.

## 13. Rejection must occur at a lawful boundary

A system may reject new operational work before an existing owner considers
it durably accepted.

PR2-BP does not redefine where command acceptance occurs.

Once existing doctrine says an attempt, command, obligation, or committed
effect exists, overload may not pretend it never existed.

## 14. Deferred work remains attributable

Deferral must not masquerade as success or disappearance.

Where semantic correctness depends on it, deferred work must remain
attributable to the relevant identity, command, consequence, schedule, or
other existing owner.

PR2-BP does not create new identity semantics for deferred work.

## 15. Backpressure is operational, not world truth

A backpressure signal may say:

- not currently admitted;
- retry later;
- capacity unavailable;
- service degraded;
- producer must slow down.

Such a signal does not itself establish:

- an in-world fact;
- a game rule;
- logical time;
- character capability;
- world priority;
- canonical truth.

## 16. Wall-clock delay is not logical time

Queue delay, throttling, retry delay, provider latency, or overload recovery
time must not silently advance or rewind authoritative world time.

A `retry-after` style operational hint is wall-clock service metadata unless
an existing temporal owner explicitly says otherwise.

AFQR-04 retains logical-time authority.

## 17. Physical queue order is not authoritative order

FIFO, LIFO, priority heaps, worker-local queues, packet order, scheduler
order, or completion order are physical mechanisms.

None automatically defines authoritative causal or commitment order.

If ordering matters semantically, PR2-CONC and the applicable semantic owner
remain authoritative.

## 18. Prioritization requires attributable rationale

Operational work may have different service priority.

Priority must be attributable to an operational or semantic protection need,
rather than silently inventing a new gameplay ranking.

Examples of potentially protected work include work required to preserve:

- already-committed consequences;
- recovery obligations;
- durable receipts;
- required reconciliation;
- integrity of authoritative persistence;
- currently blocking player-facing resolution.

Whether a particular operation belongs to such a class remains governed by
its existing owner.

## 19. Operational priority is not gameplay value

A high-priority queue class does not mean an actor, player, item, location,
or action is more important in the fiction.

A low-priority background task does not lose canonical status merely because
it can be serviced later.

Service priority and world meaning remain distinct.

## 20. Lawful degradation

Degradation is permitted only when the degraded form preserves applicable
semantics.

Potential lower-cost responses may include:

- suppressing optional diagnostics;
- reducing speculative computation;
- postponing derivative projections;
- reducing optional AI-assisted narration or enrichment;
- using an already-lawful lower-cost fidelity mode;
- deferring nonblocking background evaluation.

These are examples, not a universal degradation ladder.

## 21. Degradation cannot manufacture permission

Performance pressure does not authorize:

- illegal aggregation;
- loss of committed facts;
- rerolling committed randomness;
- changing version context;
- bypassing costs or consequences;
- inventing hidden state;
- skipping required reconciliation;
- broadening disclosure;
- changing ownership;
- rewriting history.

If no lawful degraded mode exists, the system must backpressure, defer,
reject at a lawful boundary, fail safely, or escalate.

## 22. FID remains the fidelity owner

PR2-BP may request or prefer a lower-cost fidelity mode.

PR2-FID determines whether that transition is semantically lawful.

BP does not acquire authority to aggregate, omit, materialize, or
reconstitute detail merely because a cheaper representation would help
performance.

## 23. Optional AI assistance is degradable before authority

AI-assisted narration, summarization, dialogue support, planning support,
retrieval assistance, or other non-authoritative enhancement may be
delayed, reduced, replaced, or unavailable under resource pressure where
the product can lawfully continue without it.

Such degradation may not change authoritative outcomes.

Campaign continuity must not depend on one external AI provider remaining
available.

## 24. Hotspots are scoped pressure, not semantic regions

A hotspot may be spatial, social, economic, computational, or otherwise
interaction-dense.

Hotspot status does not create:

- a new world region;
- semantic ownership;
- a partition by itself;
- special gameplay authority.

PR2-PART retains partition semantics.

## 25. Hotspot containment

A localized overload should be capable of being contained rather than
silently corrupting unrelated scopes.

Possible responses include bounded admission, local deferral, lawful
fidelity reduction, work isolation, or additional execution capacity.

No specific mechanism is mandated.

## 26. Burst handling

Temporary bursts and sustained overload are different workload shapes.

A system may absorb a bounded burst that it could not sustain indefinitely.

Evidence must state which case was measured.

A burst buffer must still have a bound.

## 27. Overload state transitions require explicit criteria

An implementation may distinguish normal, pressured, overloaded, recovering,
or other operational states.

These labels are illustrative, not a mandatory universal state machine.

Entry and exit behavior must be explicit enough to avoid accidental
semantic changes.

## 28. Recovery from overload

Recovery must not create a second semantic event merely because delayed work
resumes.

Recovery must preserve applicable:

- command/attempt identity;
- idempotency boundaries;
- commitment history;
- causal ordering;
- version context;
- randomness provenance;
- persistence obligations;
- fidelity reconciliation requirements.

Existing owners define those semantics.

## 29. Backlog replay is not semantic replay

Processing a backlog after overload is an operational act.

It does not automatically mean historical semantic replay.

PR2-PERSIST retains replay/recovery meaning.

PR2-EVENT retains message and delivery-attempt meaning.

## 30. Retry storms must be bounded

Retrying failed or deferred work consumes capacity.

A failure mode in which overload causes retries, which cause more overload,
must be representable and bounded.

This contract does not mandate exponential backoff, token buckets, circuit
breakers, or any particular algorithm.

## 31. Backpressure must not leak hidden information

Capacity responses exposed to a client must respect existing disclosure,
sensing, knowledge, and hidden-information boundaries.

Operational detail must not reveal protected world state merely because that
state influenced internal workload.

## 32. Player freedom under overload

Operational overload must not be hidden behind a permanently reduced command
vocabulary.

A fictionally coherent attempt does not become fictionally incoherent
because the runtime is busy.

The service may lawfully defer, reject before acceptance, degrade optional
presentation, or fail safely.

It may not invent a gameplay prohibition solely to conceal capacity limits.

## 33. Local and offline operation remain first-class

Performance profiles may differ between local, offline, hosted, networked,
or later distributed execution.

A hosted budget does not invalidate local operation.

A cloud service is not required for campaign continuity.

Different environments may legitimately have different measured envelopes
while preserving the same authoritative semantics.

## 34. Observability is evidence, not authority

Metrics, traces, counters, profiles, logs, benchmarks, and telemetry may
provide evidence about performance pressure.

They do not acquire ownership of world truth.

Missing telemetry does not authorize invention of authoritative facts.

## 35. Performance evidence requires context

A material performance claim should identify, where applicable:

- software revision;
- workload envelope;
- dataset or campaign scale;
- hardware/resource envelope;
- operating environment;
- topology;
- fidelity context;
- measurement duration;
- warm/cold state where relevant;
- metric definition;
- percentile or aggregation method where relevant;
- observed failures or saturation;
- uncertainty or known limits.

## 36. Cost budgets remain operational

Compute, storage, bandwidth, model-provider, or hosting cost may be included
in a performance budget.

Cost pressure may influence implementation choices.

It does not become semantic authority.

Ordinary play should not require several independent AI subscriptions to
preserve campaign continuity.

## 37. Representative pressure cases

PR2-BP must survive at least:

- ordinary load inside budget;
- short burst above steady-state capacity;
- sustained overload;
- full bounded queue;
- hotspot concentration;
- many independent background tasks;
- highly interacting foreground actors;
- persistence pressure;
- recovery while new work continues;
- message retry pressure;
- retry storm;
- AI-provider slowdown or outage;
- legal lower-fidelity degradation;
- requested but illegal fidelity degradation;
- hidden-information-sensitive workload;
- post-commit delivery failure;
- pre-acceptance rejection;
- deferred accepted work;
- local/offline constrained hardware;
- worker-count change;
- cross-partition hotspot;
- backlog drain after overload.

## 38. Overload equivalence obligation

For a bounded case where overload handling is claimed semantically safe,
normal-load and overloaded/degraded execution must preserve the declared
authoritative invariant surface.

Performance may differ.

Presentation may differ where lawful.

Authoritative meaning must not differ merely because capacity was scarce.

## 39. Explicit unsupported envelopes are lawful

Myravant may declare a workload envelope unsupported.

Lawful outcomes include:

- supported within budget;
- supported with bounded degradation;
- supported with backpressure;
- experimental/non-authoritative;
- blocked pending implementation;
- unsupported at the current resource envelope.

Falsely claiming unlimited capacity is not required.

## 40. Technology neutrality

PR2-BP mandates none of the following:

- queue implementation;
- load balancer;
- scheduler;
- token bucket;
- leaky bucket;
- semaphore;
- circuit breaker;
- autoscaler;
- Kubernetes;
- service mesh;
- database;
- cache;
- broker;
- cloud provider;
- distributed topology;
- AI provider;
- fixed tick rate.

## 41. Implementation follows evidence

The preferred evolution remains:

```text
simple deterministic runtime
-> measured bottleneck
-> bounded operational response
-> evidence
-> implementation change where justified
-> equivalence validation
```

PR2-BP must not manufacture infrastructure merely because eventual scale is
ambitious.

## 42. Failure and escalation

BP handling must fail safely or escalate when:

- work cannot be dropped without semantic loss;
- no lawful degraded mode exists;
- queue/backlog bounds are unknown;
- a priority policy would create semantic authority;
- overload handling would alter committed history;
- capacity pressure would leak hidden information;
- measurement context is insufficient to justify a claimed threshold;
- recovery cannot preserve required identity or ordering.

A failure does not automatically justify a new manager, owner, queue family,
or infrastructure layer.

## 43. R3 and later work remain separate

PR2-BP does not execute R3.

R3 remains separately authorized against its exact 34-record target.

PR2-TEST remains separately unauthorized.

Runtime implementation remains separately unauthorized.

## 44. Completion condition

PR2-BP is complete when repository doctrine and executable tests establish
that:

- performance budgets are scoped to declared workload envelopes;
- numeric values retain measurement context;
- queues/backlogs cannot rely on infinite capacity;
- overload cannot silently discard semantically required work;
- admission remains distinct from commitment;
- backpressure remains operational rather than authoritative;
- wall-clock delay cannot silently become logical time;
- physical queue order cannot become authoritative ordering;
- prioritization cannot silently create gameplay value;
- degradation must remain lawful under existing semantic owners;
- FID retains authority over fidelity transitions;
- hotspot handling does not create semantic ownership;
- retries and overload recovery remain bounded;
- backpressure respects hidden-information boundaries;
- local/offline operation remains first-class;
- performance evidence retains workload/environment context;
- no specific queue, scheduler, deployment, or cloud technology is mandated;
- PR2-TEST, R3, and implementation remain unauthorized pending separate owner authorization.

This contract is architecture governance only.

Implementation remains unauthorized pending separate owner authorization.
