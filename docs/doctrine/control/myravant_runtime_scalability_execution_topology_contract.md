# Myravant Runtime Scalability and Execution-Topology Contract — PR2-SCALE

```yaml
artifact_id: PR2-SCALE-RUNTIME-SCALABILITY-EXECUTION-TOPOLOGY-001
status: active_control_doctrine
layer: 0_control
workstream: PR2-SCALE
authority_reference: owner_directive_2026-09-14_pr2_scale_activation
authority_effect: runtime_architecture_contract_only
starting_baseline: 5268f85135b9ad5d67719b37305b204554729bed
inherits:
  - POST-R2A-TRANSITION-PROGRAM-001
  - PR2-SIMEX-SIMULATION-INFRASTRUCTURE-EXEMPLAR-PRESSURE-001
runtime_implementation_authority: none
distributed_runtime_implementation_authority: none
production_schema_authority: none
database_selection_authority: none
message_bus_selection_authority: none
cloud_provider_selection_authority: none
partitioning_semantics_authority: none
concurrency_semantics_authority: none
fidelity_semantics_authority: none
event_delivery_semantics_authority: none
persistence_recovery_semantics_authority: none
performance_budget_authority: none
native_content_authoring_authority: none
canon_authority: none
model_training_authority: none
live_play_authority: none
```

## 1. Purpose

PR2-SCALE establishes the minimum runtime-architecture laws Myravant needs to
scale execution without allowing physical deployment choices to change
authoritative meaning.

Its central invariant is:

> **Logical simulation semantics must remain independent of physical execution topology.**

PR2-SCALE makes that invariant operational enough for later runtime-architecture
packages to consume without selecting technologies or implementing distributed
infrastructure.

The lawful flow is:

```text
accepted Myravant semantics
-> topology-independent scalability contract
-> separately owned runtime-architecture contracts
-> later authorized implementation
-> equivalence evidence
```

PR2-SCALE owns the second step only.

## 2. Why this owner exists

Execution pressure can silently turn a process, thread, worker, shard, service,
database, cache, machine, or region into a semantic owner.

That is prohibited.

Myravant must be able to evolve from a simple deterministic execution form
toward more parallel or distributed execution without quietly changing:

- authority;
- legality;
- commitment;
- causality;
- state meaning;
- identity;
- version applicability;
- randomness provenance;
- hidden-information boundaries;
- committed consequence settlement.

## 3. What PR2-SCALE owns

PR2-SCALE owns only:

- logical semantics versus physical topology;
- topology-independent semantic invariance;
- a deterministic reference-execution role for equivalence;
- top-level equivalence obligations;
- allowed implementation variance versus semantic variance;
- workload-envelope discipline for scalability claims;
- replaceability of physical execution mechanisms;
- bounded handoffs to `PR2-PART`, `PR2-CONC`, `PR2-FID`, `PR2-EVENT`,
  `PR2-PERSIST`, and `PR2-BP`;
- escalation when equivalence cannot be specified without downstream doctrine.

PR2-SCALE may define the questions downstream owners must answer.

It may not answer them on their behalf.

## 4. What PR2-SCALE must not own

PR2-SCALE must not define or implement:

- runtime code or production schemas;
- distributed infrastructure;
- thread, worker, process, host, shard, or region layout;
- microservices;
- Entity Component Systems;
- actor systems;
- event sourcing;
- database choice;
- message-bus choice;
- cloud-provider choice;
- programming-language choice;
- serialization or network protocol;
- GPU or accelerator mandates;
- exact authority partitioning or migration (`PR2-PART`);
- exact scheduling, ordering, conflicts, or concurrency commitment (`PR2-CONC`);
- exact relevance/fidelity/aggregation/reconstitution (`PR2-FID`);
- exact command/event/message/projection delivery (`PR2-EVENT`);
- exact persistence/snapshot/replay/recovery/reconstruction (`PR2-PERSIST`);
- numeric budgets, overload policy, or backpressure (`PR2-BP`);
- gameplay doctrine;
- canon or native content;
- source/corpus execution;
- model training;
- conversion execution;
- live-play/GM behavior.

## 5. Core topology-independence law

A physical execution boundary does not create semantic authority.

The following are execution details unless an existing semantic owner says
otherwise:

- thread;
- coroutine;
- worker;
- process;
- host;
- virtual machine;
- container;
- service;
- shard;
- partition;
- region;
- database;
- cache;
- queue;
- stream;
- file/object store;
- accelerator;
- client.

Changing one may change performance, placement, operational cost, or failure
exposure.

It must not silently change what the world means.

## 6. Semantic ownership does not follow placement

No semantic owner transfers merely because data or computation moves.

```text
data moves to another worker
!= identity or authority transfers automatically

rule evaluation runs elsewhere
!= the execution unit owns rule meaning

state is stored in a database
!= the database owns state semantics

events cross a transport
!= the transport owns event meaning

a projection is cached near a client
!= the cache becomes authoritative truth
```

Any actual semantic transfer must be authorized by the existing semantic owner
and the applicable later runtime contract.

## 7. Reference-execution role

Myravant requires a deterministic **reference-execution role**.

This is a semantic/evaluation role, not a permanent technology mandate.

A reference execution should be capable of serving as the simplest accepted
oracle for a bounded workload when later optimized implementations are compared
against it.

The role should favor:

- explicit authoritative inputs;
- deterministic commitment;
- inspectability;
- reproducibility;
- required provenance;
- minimal hidden execution behavior.

The reference role does not have to be:

- fastest;
- most scalable;
- distributed;
- production-hosted;
- the final data layout;
- the final scheduling model.

PR2-SCALE does not claim that a complete conforming reference runtime already exists.

## 8. Equivalence contract

A topology-equivalence case must identify the authoritative inputs held constant.

Where applicable:

```text
initial authoritative state
versioned rules/package/override context
authoritative input or command history
lawfully determined commitment decisions
logical-time inputs
randomness provenance
external authoritative inputs
other declared semantically relevant configuration
```

Two execution forms are equivalent only when physical execution differences do
not create an unauthorized difference in authoritative semantics.

PR2-SCALE consumes existing semantic owners; it does not redefine them.

## 9. Authoritative equivalence dimensions

Where material to a bounded case, topology changes must not silently alter:

- authoritative state;
- committed consequences;
- legality;
- identity continuity;
- causal ancestry;
- ruleset/package/override applicability;
- randomness identity and committed outcomes;
- ownership and governed relations;
- resource or condition settlement;
- logical-time consequences;
- correction/supersession history;
- hidden-information boundaries;
- lawful projection/disclosure;
- durable command/attempt identity.

A downstream owner may define a more precise rule for its own dimension.

## 10. Allowed implementation variance

The following may vary when the difference is not semantically exposed:

- wall-clock duration;
- CPU/core assignment;
- thread/worker/host assignment;
- memory layout;
- batching;
- caching;
- internal queue shape;
- physical message route;
- network latency;
- storage layout;
- compression;
- instrumentation;
- execution order of semantically independent computation;
- accelerator use.

If a physical difference changes authoritative results, it is not merely
implementation variance for that case.

## 11. No worker-count semantics

Authoritative meaning must not depend on how many workers happen to exist.

Changing worker count must not silently change:

- rules;
- committed RNG outcomes;
- conflict winners;
- event identity;
- settlement;
- scheduled consequences;
- identity;
- disclosure rights.

If concurrency creates multiple possible resolutions, `PR2-CONC` must define how
authoritative commitment becomes deterministic or otherwise lawfully bounded.

## 12. No machine-count semantics

Moving from one process to many processes, or one host to many hosts, must not by
itself create new world rules.

Network boundaries create cost and failure pressure, not semantic meaning.

If a topology cannot preserve a required semantic property, that topology is
unsupported for that property until a lawful architecture exists.

The correct result is not to weaken semantics silently.

## 13. Replaceability law

A physical execution mechanism should be replaceable without rewriting unrelated
semantic doctrine.

No technology may become the hidden definition of:

- state ownership;
- causality;
- persistence truth;
- event truth;
- world or actor identity;
- legality;
- commitment;
- logical time;
- hidden information.

Replaceability is a semantic boundary, not a procurement preference.

## 14. Scale is multidimensional

A single entity count, player count, event count, or throughput number is not a
complete scalability claim.

Material scale evidence should identify relevant dimensions such as:

```text
authoritative-state volume
active interacting actor count
background actor/process count
interaction density
event/command rate
scheduled-work rate
spatial concentration
hotspot intensity
persistence/history size
logical-time horizon
fidelity level
concurrent player count
cross-partition interaction rate
latency sensitivity
recovery requirements
hardware/resource envelope
```

`PR2-BP` owns later numeric performance budgets and overload thresholds.

## 15. Workload-envelope law

A scalability result is valid only inside its declared workload envelope.

```text
one million dormant records
!= one million actively interacting actors

one million independent updates
!= one million mutually interacting updates

high offline batch throughput
!= low-latency player-facing throughput
```

No extrapolation may erase those differences.

## 16. Scaling cannot outrank semantics

Performance pressure does not authorize corruption of higher-priority
invariants.

Scaling must not silently trade away:

- world consistency;
- deterministic/reproducible authority where required;
- ownership boundaries;
- hidden-information boundaries;
- committed consequences;
- version applicability;
- required auditability.

Performance is not a semantic super-owner.

## 17. Computation is not commitment

Later implementations may parallelize, prefetch, predict, cache, recompute, or
abandon computation.

That does not make the computation authoritative.

Authoritative commitment remains governed by existing doctrine and later
runtime contracts.

`PR2-CONC` owns exact concurrency/commitment semantics.

## 18. Physical ordering is not authoritative ordering

Physical completion order is not automatically world order.

Invalid implicit rules include:

- whichever thread finishes first wins;
- whichever packet arrives first wins;
- whichever worker responds first commits;
- whichever replica answers first becomes truth.

If ordering matters semantically, it must be governed explicitly.

## 19. Failure boundaries do not create semantic owners

A process, host, partition, or region may be a physical failure domain.

That does not grant semantic ownership.

Detailed partition failure/transfer belongs to `PR2-PART`.
Detailed recovery/reconstruction belongs to `PR2-PERSIST`.
Overload/degradation policy belongs to `PR2-BP`.

## 20. Topology transitions are semantic-risk events

Topology changes can expose semantic risk even when intended meaning is
unchanged.

Examples:

- worker-count changes;
- process migration;
- partition movement;
- host replacement;
- failover;
- scaling up/down;
- fidelity transitions;
- recovery after interruption.

PR2-SCALE requires explicit equivalence obligations before such transitions can
be claimed safe.

It does not define the algorithms.

## 21. Reference equivalence test families

Later executable assurance should be able to compare, where applicable:

- serial reference vs parallel execution;
- one worker count vs another;
- single-process vs multi-process;
- single-host vs multi-host;
- pre-migration vs post-migration results;
- normal-load vs hotspot handling;
- stable fidelity vs fidelity-cycle reconciliation;
- normal-load vs overload/degraded operation;
- uninterrupted vs failure/recovery execution.

These are test families, not v1 topology requirements.

## 22. Current equivalence limits

PR2-SCALE must not manufacture certainty before downstream contracts exist.

Until the applicable owner is accepted:

- partition migration is bounded by `PR2-PART`;
- competing schedules are bounded by `PR2-CONC`;
- fidelity-cycle behavior is bounded by `PR2-FID`;
- delivery/retry behavior is bounded by `PR2-EVENT`;
- persistence/recovery is bounded by `PR2-PERSIST`;
- overload/degraded operation is bounded by `PR2-BP`.

PR2-SCALE establishes the preservation obligation; it does not pre-solve the
missing semantics.

## 23. Downstream handoffs

### PR2-PART

Must define logical partition boundaries, authority transfer/migration, failure
exposure, and the distinction between physical location and semantic ownership.

PR2-SCALE does not activate PR2-PART.

### PR2-CONC

Must define independently computable work, authoritative commitment ordering,
conflict handling, scheduler nonauthority, and retry/recompute boundaries.

PR2-SCALE does not activate PR2-CONC.

### PR2-FID

Must define relevance, fidelity, aggregate/detail transitions, reconstitution,
preservation of committed facts, and background/foreground reconciliation.

PR2-SCALE does not activate PR2-FID.

### PR2-EVENT

Must define the runtime separation of commands, authoritative events, transport
messages, delivery attempts/retries, and projections.

PR2-SCALE does not activate PR2-EVENT.

### PR2-PERSIST

Must define durable state, snapshots, replay, recovery, reconstruction,
corruption boundaries, and applicable version context while consuming existing
R2 doctrine.

PR2-SCALE does not activate PR2-PERSIST.

### PR2-BP

Must define performance budgets, overload behavior, backpressure, lawful
degradation, hotspot behavior, and recovery from overload.

PR2-SCALE does not activate PR2-BP.

## 24. Topology classes are descriptive, not mandatory

Myravant may eventually encounter:

- one process;
- multiple threads;
- multiple workers;
- multiple processes;
- multiple machines;
- dynamically partitioned infrastructure.

These are descriptive pressure classes.

PR2-SCALE does not require all of them to exist.

The simplest lawful implementation remains acceptable when it meets current
product needs and preserves future migration seams.

## 25. No distributed-by-default law

Distribution is not inherently more scalable, correct, modern, or appropriate.

A centralized implementation may be preferable for determinism, debugging,
coordination cost, or sufficient measured performance.

A distributed implementation may become justified by measured need.

Neither form is doctrine by prestige.

## 26. No architecture-fashion voting

The following do not establish Myravant runtime requirements:

- many exemplars use microservices;
- many exemplars use ECS;
- many exemplars use actors;
- many exemplars use event sourcing;
- many exemplars use Kubernetes;
- many exemplars use a specific database;
- many exemplars use a specific cloud provider.

Exemplar frequency is evidence for investigation, not architecture authority.

## 27. Environment and client independence

An OS, CPU, GPU, model provider, developer machine, deployment platform, or
client does not own authoritative semantics.

Environment differences may affect performance or optional tooling.

Text, future 3D, future VR, and later clients remain interaction/projection
surfaces rather than owners of world truth.

Specific hardware/release thresholds remain evaluation/product controls, not
PR2-SCALE semantic doctrine.

## 28. Version, randomness, time, and disclosure independence

Topology-equivalence claims must use the same applicable semantic version
context unless a separately governed difference is under test.

A topology change must not silently reroll or replace committed randomness.

Wall-clock speed, queue delay, network delay, or machine speed must not silently
become logical world time.

Moving computation or caches closer to a client must not broaden lawful
visibility or hidden-information access.

PR2-SCALE consumes the existing owners of those semantics.

## 29. Unsupported topology is lawful

A topology may be unsupported.

The project must prefer an explicit unsupported boundary over false equivalence.

Lawful results include:

- supported and equivalence-proven;
- supported with declared constraints;
- experimental/non-authoritative;
- blocked pending downstream doctrine;
- rejected for the current semantic envelope.

"Scalable" must never mean "we assume every topology works."

## 30. Equivalence evidence

A material topology-equivalence claim should eventually preserve:

```text
equivalence_case_id
reference_execution_id
candidate_execution_id
semantic_version_context
initial_state_ref
authoritative_input_ref
workload_envelope
topology_envelope
declared_allowed_variances[]
authoritative_observations[]
state_digest_or_equivalent
commitment_evidence[]
randomness_provenance_refs[]
logical_time_evidence[]
projection_privacy_evidence[]
failure_or_transition_conditions[]
result
known_limits[]
downstream_contract_refs[]
```

This is an architecture/evaluation shape, not a production schema.

## 31. Equivalence result vocabulary

A bounded evaluation may end as:

- `equivalent_within_declared_envelope`;
- `equivalent_with_declared_constraints`;
- `not_equivalent`;
- `inconclusive_missing_downstream_contract`;
- `inconclusive_missing_evidence`;
- `unsupported_topology`.

These results preserve uncertainty; they do not authorize implementation.

## 32. Corpus-scale runtime pressure

Myravant must survive heterogeneous content and world models without assuming
one universal simulation style.

Runtime scaling must accommodate pressure from combinations such as:

- tactical high-interaction scenes;
- long-horizon processes;
- sparse background populations;
- dense social/economic interaction;
- vehicles/platforms;
- companions/summons;
- unusual embodiment;
- distributed identity;
- procedural systems;
- deterministic subsystems;
- stochastic subsystems;
- source-local mechanics with different update needs.

PR2-SCALE must not flatten these into one universal tick, physics, entity, or
resource model for optimization convenience.

## 33. No universal tick, entity, or locality law

PR2-SCALE does not establish one global simulation tick.

Lawful systems may be event-driven, turn-driven, scheduled, continuous within a
local profile, batched, demand-materialized, or hybrid.

PR2-SCALE does not require every simulated construct to become one universal
entity/component package.

Spatial proximity is not the only relevance relation; relevance may be social,
institutional, economic, communicative, ownership-based, causal, or otherwise
governed.

Detailed relevance/fidelity remains `PR2-FID`.

## 34. Scalability claim discipline

Statements such as these are invalid without bounded evidence:

```text
"supports one million entities"
"supports MMO scale"
"distributed means scalable"
"single process cannot scale"
"more workers always improve throughput"
"event sourcing guarantees replay"
"ECS guarantees performance"
"sharding guarantees horizontal scale"
```

A lawful claim must state what was measured, under which semantic/workload
envelope, and what remained invariant.

## 35. Escalation rules

Escalate rather than invent architecture when:

- topology equivalence needs missing concurrency doctrine;
- migration safety needs partition doctrine;
- aggregate/detail equivalence needs fidelity doctrine;
- delivery behavior needs event/message doctrine;
- recovery equivalence needs persistence doctrine;
- overload behavior needs budget/backpressure doctrine;
- an optimization would transfer semantic ownership;
- performance pressure would weaken an accepted invariant;
- an exemplar mechanism is being promoted directly into architecture;
- a scale claim lacks a meaningful workload envelope.

Escalation is preferable to fake scalability.

## 36. Completion condition

PR2-SCALE is complete when the repository can machine-test that:

1. logical semantics are explicitly independent of physical execution topology;
2. physical placement does not transfer semantic ownership;
3. a reference-execution role exists without a permanent technology mandate;
4. topology-equivalence obligations are explicit;
5. implementation variance is separated from semantic variance;
6. scale claims require workload/context envelopes;
7. worker count, machine count, and physical completion order cannot silently
   define authoritative outcomes;
8. unsupported topologies may fail closed;
9. each downstream runtime package has a bounded handoff;
10. no downstream package is activated by PR2-SCALE;
11. no distributed implementation or technology stack is mandated;
12. R3 and implementation authorities remain unchanged.

Completion does not mean Myravant is distributed, multi-host execution exists,
performance targets have been met, or any specific scaling topology is
supported.
