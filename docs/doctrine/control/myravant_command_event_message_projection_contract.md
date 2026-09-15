# Myravant Command, Event, Message, and Projection Contract — PR2-EVENT

```yaml
artifact_id: PR2-EVENT-COMMAND-EVENT-MESSAGE-PROJECTION-001
status: active_control_doctrine
layer: 0_control
workstream: PR2-EVENT
authority_reference: owner_directive_2026-09-15_pr2_event_activation
authority_effect: runtime_message_contract_only
starting_baseline: e765d00e57e3a444ecd16078a3390eb49958f5b2
inherits:
  - POST-R2A-TRANSITION-PROGRAM-001
  - PR2-SCALE-RUNTIME-SCALABILITY-EXECUTION-TOPOLOGY-001
  - PR2-PART-AUTHORITY-PARTITIONING-MIGRATION-001
  - PR2-CONC-DETERMINISTIC-CONCURRENCY-SCHEDULING-001
  - AFQR-01-09-R1D-CORE-TRANSACTION-IDENTITY-RELATION-001
  - AFQR-R2B-CORE-QUALIFICATIONS-001
  - AFQR-R2B-CROSS-PHASE-VERSION-IDENTITY-EFFECTIVITY-001
  - AFQR-R2B-CONTINUITY-QUALIFICATIONS-001
runtime_implementation_authority: none
production_schema_authority: none
semantic_commitment_owner_authority: none
semantic_event_identity_authority: none
command_identity_authority: none
command_attempt_identity_authority: none
logical_time_authority: none
causal_order_authority: none
scheduler_authority: none
partition_identity_authority: none
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

PR2-EVENT defines the runtime-architecture contract for separating **commands,
requests, proposals, committed facts, transport messages, deltas,
notifications, acknowledgements, and projections** without allowing transport
or derived representations to acquire semantic authority.

It answers the bounded questions deliberately left by PR2-SCALE, PR2-PART, and
PR2-CONC:

- which runtime representations may carry authoritative references without
  becoming authoritative themselves;
- how a transport attempt differs from an AFQR-02 command attempt;
- how duplicate, delayed, missing, reordered, or repeated delivery is handled
  without duplicating semantic commitment;
- what causal and ordering context a message may carry while leaving logical
  time and causal law with AFQR-04;
- how projections and notifications remain derivative and nonauthoritative;
- how a committed fact can be represented to multiple consumers without
  multiplying that fact;
- how projection rebuilding is bounded without pre-empting PR2-PERSIST;
- when missing semantic identity, ordering, visibility, persistence, or domain
  doctrine must fail closed or escalate.

The governing flow is:

```text
accepted Myravant semantics
-> AFQR command / commitment / logical-time owners
-> PR2-SCALE topology-independence law
-> PR2-PART authority-boundary law
-> PR2-CONC scheduler-nonauthority law
-> PR2-EVENT representation and delivery contract
-> later PR2-PERSIST / PR2-FID / PR2-BP contracts as applicable
-> later authorized implementation
-> message / projection conformance evidence
```

PR2-EVENT owns only this bounded message-and-projection contract layer.

## 2. Why this owner exists

Without an explicit boundary, runtime plumbing can silently become game law.
The project must reject assumptions such as:

```text
message arrival makes a fact true
queue order becomes world order
publish success means commitment succeeded
acknowledgement means the world changed
notification receipt means the recipient lawfully knows the fact
projection state is canonical because it is convenient to query
re-delivery means re-execution
timeout means semantic cancellation
cache state defines truth
broker offset defines causal priority
```

These are prohibited unless a separately authoritative semantic owner explicitly
establishes the relevant meaning.

## 3. Existing owners retained

### AFQR-01 — commitment, replay, and transition receipts

AFQR-01 retains qualified state/write ownership, owner-specific reducers,
semantic commitment, replay, recovery, and transition receipts.

PR2-EVENT may transport or reference an AFQR-01 committed event receipt. It does
not create commitment merely by publishing, storing, acknowledging, consuming,
or projecting a representation of that receipt.

### AFQR-02 — command, attempt, retry, and durable progress identity

AFQR-02 retains command identity, command-attempt identity, retry identity,
suspension, escalation, and durable command progress.

PR2-EVENT may define **transport-attempt identity** for delivery behavior. A
transport attempt is not an AFQR-02 command attempt and cannot decide whether a
semantic retry, replacement, or resumed operation is the same command.

### AFQR-04 — logical time, causality, simultaneity, and scheduling

AFQR-04 retains logical time, causal ordering, simultaneity, scheduling,
deterministic resolution groups, and bounded cascades.

PR2-EVENT may carry AFQR-04-owned causal or ordering context. It does not derive
world order from arrival time, queue position, broker offset, wall-clock time,
or consumer completion order.

### PR2-SCALE

PR2-SCALE retains the invariant that logical simulation semantics are
independent of physical execution topology.

A message contract must therefore work for in-process calls, one process, many
workers, many hosts, partitioned execution, or later deployment topologies
without changing semantic truth.

### PR2-PART

PR2-PART retains logical authority partition identity, responsibility,
migration, transfer, and cutover boundaries.

Sending a message across a partition boundary does not transfer semantic
ownership.

### PR2-CONC

PR2-CONC retains physical-concurrency nonauthority, scheduler nonauthority,
conflict qualification, and deterministic authoritative-commitment
qualification.

Message arrival order, queue timing, delivery completion, or consumer race
cannot become a hidden scheduler-based winner rule.

### R2B qualifications

R2B-CORE retains committed randomness preservation and correction/replacement
qualification. R2B-CROSS-PHASE retains version identity, pinning,
applicability, and effective intervals. R2B-CONTINUITY retains the bounded
continuity and correction qualifications already assigned there.

PR2-EVENT transports these identities and qualifications when needed; it does
not redefine them.

## 4. What PR2-EVENT owns

PR2-EVENT owns only:

- command/request/event/message/projection separation at runtime boundaries;
- representation-class authority effects;
- transport-envelope nonauthority;
- transport-message identity qualification;
- transport-attempt identity qualification;
- correlation and causation-reference carriage boundaries;
- delivery-attempt and redelivery semantics;
- duplicate-delivery handling obligations;
- idempotent consumption obligations where repeated delivery is possible;
- delivery acknowledgement semantics;
- late, missing, duplicated, and out-of-order delivery classification;
- carriage of separately owned logical-time / causality / version context;
- committed-fact representation boundaries;
- delta-message nonauthority;
- notification nonauthority;
- projection derivation boundaries;
- projection lag / staleness declaration obligations;
- projection rebuilding boundaries short of persistence ownership;
- visibility-preserving delivery boundaries;
- cross-partition message nonauthority;
- message/projection evidence envelopes;
- bounded downstream handoffs.

## 5. What PR2-EVENT must not own

PR2-EVENT must not define or implement:

- semantic state ownership;
- qualified write ownership;
- semantic commitment ownership;
- semantic committed-event identity;
- command identity;
- command-attempt identity;
- semantic retry or replacement identity;
- action legality;
- gameplay resolution;
- logical time;
- causal-order law;
- simultaneity law;
- scheduling law;
- deterministic resolution-group law;
- concurrency conflict semantics;
- scheduler winner rules;
- partition identity;
- partition migration or cutover semantics;
- durable persistence;
- snapshot semantics;
- authoritative replay/recovery;
- corruption recovery;
- durable reconstruction;
- fidelity/aggregation semantics;
- overload/backpressure policy;
- universal stale-command doctrine;
- universal knowledge or epistemic doctrine;
- universal visibility doctrine;
- universal delivery guarantee;
- universal exactly-once transport requirement;
- event-sourcing requirement;
- CQRS requirement;
- actor-model requirement;
- pub/sub requirement;
- queue requirement;
- replicated-log requirement;
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

## 6. Core nonauthority law

A runtime representation can carry authority-bearing references without
becoming the authority it represents.

```text
message delivery
!= semantic commitment

publish success
!= semantic commitment

transport acknowledgement
!= transition receipt

message arrival order
!= causal order

projection state
!= authoritative state

notification receipt
!= lawful knowledge acquisition

redelivery
!= semantic re-execution
```

## 7. Representation classes

PR2-EVENT recognizes the following bounded classes. These are semantic roles,
not mandatory production types or schemas.

### 7.1 Request envelope

Carries a request or reference to an AFQR-02-owned command context.

Transporting the request does not create command identity, prove legality,
reserve resources, commit an action, or establish success.

### 7.2 Proposal envelope

Carries a noncommitted candidate, preview, plan, speculative result, or proposed
effect.

A proposal remains nonauthoritative until a separately lawful transition occurs
under the appropriate owner.

### 7.3 Committed-fact representation

Carries or references a fact already committed under AFQR-01 or another lawful
semantic owner.

The representation is not a second commitment and does not replace the original
transition receipt or audit identity.

### 7.4 Delta message

Carries a change representation useful to a consumer or projection.

A delta message is not by itself qualified state ownership or semantic truth.
If authoritative state and the delta disagree, the delta does not silently win.

### 7.5 Notification message

Carries information intended to inform a consumer that something occurred or
changed.

Notification is not commitment, permission, obligation, knowledge, visibility,
or canonicality by itself.

### 7.6 Projection update

Carries information used to derive or update a read model, display model,
search index, cache, summary, observer view, or other derivative representation.

A projection is derivative unless separate doctrine explicitly grants another
role.

### 7.7 Transport acknowledgement

Reports a transport/process fact such as accepted, delivered, observed,
consumed, rejected, expired, or failed within a declared transport envelope.

It does not substitute for an AFQR-01 transition receipt.

### 7.8 Control or diagnostic message

Carries runtime-control, health, retry, cancellation-request, diagnostic, or
operational information.

Operational control does not create semantic truth merely because it affects
physical execution.

## 8. The term “event” must be qualified

`event` is too overloaded to be self-authenticating.

A **semantic committed event/fact** belongs to its semantic owner and commitment
law.

An **event message** is a runtime representation carrying or referencing such a
fact or another declared event-like signal.

An **operational event** may describe infrastructure behavior without any world
semantic effect.

No implementation may collapse these categories merely because a framework or
vendor calls all three “events.”

## 9. Semantic identity and transport identity are distinct

A committed fact can be represented by zero, one, or many transport messages.
One transport message can also reference multiple already-governed facts when a
lawful envelope permits it.

Therefore:

```text
semantic_fact_identity
!= transport_message_identity
!= transport_attempt_identity
```

PR2-EVENT may require these identities to be distinguishable when ambiguity
would affect duplicate handling, audit, projection, or delivery evidence.

It does not prescribe UUIDs, offsets, hashes, database keys, or another concrete
identifier technology.

## 10. Transport attempts are not command attempts

A message may be attempted, retried, redirected, delayed, or re-delivered by
transport infrastructure.

Those are transport attempts.

They cannot silently increment, replace, resume, or otherwise redefine an
AFQR-02 command attempt.

If transport failure requires semantic command retry, replacement, or
resumption, AFQR-02 remains the owner of that identity decision.

## 11. Delivery guarantees are declared, not assumed

A future implementation may use at-most-once-like, at-least-once-like,
best-effort, durable, transient, replayable, local synchronous, or another
qualified delivery mechanism.

PR2-EVENT does not declare one mechanism universally correct.

The chosen implementation must instead demonstrate that its declared delivery
envelope preserves Myravant semantic authority and failure behavior.

## 12. Exactly-once transport is not a semantic shortcut

A vendor or framework claim of “exactly once” does not prove exactly-once
semantic commitment.

Conversely, repeated physical delivery does not imply repeated semantic
commitment.

Semantic uniqueness is established by the relevant semantic owner, not by a
transport marketing label.

## 13. Duplicate delivery

Duplicate transport delivery must not automatically duplicate semantic effects.

Where repeated delivery is possible, the consumer boundary must have a lawful
way to distinguish:

- the same transport message re-delivered;
- a new transport message representing the same committed fact;
- a distinct committed fact with similar content;
- a corrected or superseding fact;
- a command retry or replacement whose identity belongs to AFQR-02.

If those cannot be distinguished safely, processing must fail closed or
escalate rather than guess.

## 14. Idempotent consumption

Idempotency is qualified to a declared consumer operation and identity envelope.

It is not a universal statement that two similar payloads are the same event.

A consumer may suppress repeated processing only when the identity basis is
lawful for that operation. Content equality alone is insufficient when distinct
facts can share content.

## 15. Acknowledgements

Transport acknowledgements may report physical/runtime progress.

They must not be interpreted as semantic success unless the referenced semantic
owner separately establishes that relationship.

An acknowledgement can be lost after successful semantic processing or emitted
before downstream projection completion. Those cases must not manufacture or
erase semantic truth.

## 16. Missing delivery

A missing message does not erase an already committed fact.

A missing request message does not prove that a command never existed.

A missing projection update means the projection may be incomplete or stale; it
does not transfer authority to the projection.

Durable recovery and reconstruction of missing information is handed to
PR2-PERSIST where persistence semantics are required.

## 17. Late delivery

Late arrival cannot retroactively redefine AFQR-04 logical ordering.

A late message may still be processable when its semantic context remains
applicable. It may be rejected, quarantined, reconciled, or require
reconstruction when separately governed law says so.

PR2-EVENT does not invent a universal stale-message or stale-command policy.

## 18. Out-of-order delivery

Physical arrival order is nonauthoritative.

If a consumer requires semantic order, that order must come from separately
owned causal/logical/version context rather than queue arrival or wall-clock
completion.

When required ordering context is unavailable, the consumer must not guess.

## 19. Causality metadata carriage

A message may carry references such as:

```text
semantic_fact_ref
command_ref
command_attempt_ref
causal_parent_ref
logical_time_context
resolution_group_context
version_or_effectivity_context
partition_context
correlation_ref
projection_source_ref
visibility_context
```

These are evidence-shape examples, not mandatory production fields.

Carrying a reference does not transfer ownership of its meaning to PR2-EVENT.

## 20. Correlation is not causation

Correlation identifiers may group runtime activity for tracing or workflow
coordination.

They do not by themselves establish causal parentage, command identity,
semantic dependency, ownership, or world chronology.

## 21. Queue order, broker offset, and wall clock are physical facts

Queue position, broker partition offset, insertion order, receive timestamp,
wall-clock timestamp, socket order, process sequence, and consumer completion
may be useful evidence.

They are not automatically AFQR-04 logical time or causality.

A domain may explicitly map some physical fact into semantics, but that mapping
must come from the lawful semantic owner rather than from PR2-EVENT by default.

## 22. Request and proposal boundaries

A request may ask for a transition.

A proposal may describe a possible transition.

Neither is the transition itself.

Persistence of a request or proposal does not make it committed. Delivery of a
proposal does not promote it. Projection of a proposal does not make it
canonical.

## 23. Committed-fact representation boundaries

Once a semantic fact is lawfully committed, EVENT may distribute
representations of that fact.

Consumers must be able to preserve the distinction between:

```text
original semantic fact / receipt
transport representation of that fact
consumer-side processing record
projection derived from that fact
notification about that fact
```

These may have different identities and lifecycles.

## 24. Deltas are representations, not owners

A state delta may be an efficient representation of change.

It does not become authoritative solely because applying it is convenient.

If a delta is incomplete, duplicated, reordered, or incompatible with its
version context, a consumer must not silently create a new authoritative state.

## 25. Projections are derivative

A projection may serve queries, UI, search, analytics, summaries, AI context,
observer views, or other read-oriented purposes.

Unless separately authorized, a projection:

- does not own the underlying semantic state;
- cannot commit changes by being edited;
- cannot override the source authority because it is fresher to read;
- cannot infer missing committed facts as canonical truth;
- may lag behind authoritative state;
- may be rebuilt or replaced without rewriting authoritative history.

## 26. Projection freshness and lag

Projection consumers that depend on freshness must operate under a declared
freshness or applicability envelope.

`latest received` is not necessarily `latest authoritative`.

A stale projection can remain useful for nonauthoritative purposes if the use is
lawful. It cannot silently satisfy an authority-sensitive precondition that
requires fresher evidence.

## 27. Projection rebuilding boundary

PR2-EVENT owns the rule that projections are rebuildable derivative products
when their source contract declares them so.

PR2-EVENT does **not** own the durable source, snapshot strategy, replay log,
recovery procedure, corruption handling, or reconstruction algorithm needed to
perform that rebuild.

Those durable semantics belong to PR2-PERSIST.

## 28. Notifications are not knowledge doctrine

Delivery to a player, NPC subsystem, AI process, client, observer, or service
does not automatically establish in-world knowledge, perception, evidence,
consent, notice, responsibility, or legal effect.

Those meanings require their existing domain owners.

Transport visibility must not broaden semantic visibility.

## 29. Hidden information and disclosure

A message/projection path must preserve declared visibility and disclosure
boundaries.

A cache, queue, worker, analytics sink, projection builder, or debug consumer
having physical access to data does not imply that every semantic actor may
observe it.

PR2-EVENT does not define the underlying visibility doctrine; it prevents
transport from bypassing it.

## 30. Corrections, compensation, supersession, and retcon pressure

A correction or superseding committed fact must remain distinguishable from the
original fact under existing continuity/correction law.

Delivery retries must not mutate the original committed record into the correction.

Projections may update to reflect lawful correction while preserving whatever
audit/history boundary the semantic owner requires.

## 31. Randomness and choice preservation

Delivery, redelivery, projection rebuilding, or notification retry must not reroll or replace randomness already committed under R2B-CORE.

Transport retry must not silently re-execute a semantic resolution merely to
recreate a message.

If a genuinely new semantic resolution is authorized, its identity and
randomness provenance remain governed outside EVENT.

## 32. Version identity and effectivity

Messages and projections may need to carry version/effectivity context when
interpretation depends on ruleset identity, content-package identity, campaign
override identity, schema identity, or effective interval.

R2B-CROSS-PHASE owns those identities and applicability rules.

EVENT carries or requires the relevant context; it does not invent replacement
version law.

## 33. Cross-partition messaging

A message crossing a partition boundary does not transfer semantic ownership,
create a new authority partition, or complete migration.

PR2-PART remains owner of partition responsibility and migration/cutover law.

EVENT governs only the representation and delivery boundary.

## 34. Concurrency and messages

Concurrent producers or consumers must not use race timing, first arrival,
consumer speed, or worker identity to decide truth unless existing semantic law
explicitly establishes the decision rule.

PR2-CONC remains owner of scheduler nonauthority and deterministic
commitment qualification.

## 35. Local calls are also message-boundary pressure

PR2-EVENT is not only for distributed systems.

An in-process callback, function call, observer hook, internal queue, or local
subscription can create the same category errors as a network message.

The contract therefore applies to semantic representation boundaries, not only
to network transport.

## 36. External service and webhook pressure

A future external integration may deliver repeated, delayed, missing, reordered,
or provider-generated notifications.

Provider receipt IDs, timestamps, webhook retry rules, or API response codes do
not become Myravant semantic law merely because the provider exposes them.

The integration must translate them into a lawful EVENT envelope or escalate a
missing doctrine problem.

## 37. Event sourcing is optional

PR2-EVENT does not require an event-sourced runtime.

A future implementation may lawfully use direct state ownership with transition
receipts, logs, journals, event streams, snapshots, databases, files, in-memory
structures, or another substrate if later authorized and if the semantic
contract is preserved.

## 38. CQRS is optional

The distinction between authoritative state and projections resembles concerns
found in CQRS architectures, but PR2-EVENT does not adopt CQRS as Myravant law.

The contract is about authority separation, not a named software pattern.

## 39. Pub/sub is optional

Publish/subscribe may be one implementation technique.

Publication does not define truth, subscriber count does not define authority,
and subscription topology does not define semantic ownership.

## 40. Actor/mailbox patterns are optional

Actor mailboxes, channels, streams, queues, futures, callbacks, and other
message-processing styles may satisfy this contract.

None is privileged doctrine.

## 41. Failure before semantic commitment

A failed request or proposal delivery creates no semantic commitment merely
because transport work occurred.

The runtime may retry transport subject to transport-attempt identity. If it
needs a new command attempt, AFQR-02 governs that change.

## 42. Failure after semantic commitment but before notification

A committed fact remains committed even if downstream publication,
notification, projection update, or acknowledgement fails.

EVENT may require retry/reconciliation evidence for the delivery layer.
PR2-PERSIST later governs durable reconstruction where necessary.

## 43. Consumer failure after processing

A consumer may process a message and fail before recording or emitting its
transport acknowledgement.

Redelivery must not automatically duplicate semantic effects.

This pressure is one reason EVENT distinguishes transport processing from
semantic commitment.

## 44. Cancellation and timeout

Cancelling a delivery attempt or timing out a consumer does not undo an already committed fact.

A timeout does not define AFQR-04 logical time or AFQR-02 semantic retry by
itself.

## 45. Backpressure handoff

PR2-BP will later define overload, prioritization, admission pressure, queue
bounds, lawful degradation, and backpressure behavior.

EVENT may classify delivery states, but it does not decide which work to drop,
delay, degrade, or prioritize under overload.

## 46. PERSIST handoff

PR2-PERSIST must define durable persistence, snapshot, replay, recovery,
reconstruction, and corruption-handling semantics for authoritative state and
required evidence.

EVENT defines which message/projection distinctions must survive that work; it
does not define the durable mechanism.

## 47. FID handoff

PR2-FID must define lawful aggregation/detail transitions and reconstitution.

EVENT projections cannot use reduced fidelity as permission to invent or erase
authoritative facts.

## 48. R3 boundary

The frozen 34-record R3 conformance target may be inspected as pressure evidence
when checking whether message/runtime-schema constructs lack a lawful owner.

PR2-EVENT does not:

- execute R3;
- disposition R3 records;
- change the selector;
- change the record count;
- promote a transport schema or implementation assumption into doctrine.

R3 remains separately authorized.

## 49. Message evidence envelope

A material EVENT conformance case should eventually be able to preserve:

```text
message_case_id
semantic_fact_or_command_ref
representation_class
transport_message_identity
transport_attempt_identity
producer_context
consumer_context
causal_or_logical_context_ref
version_effectivity_context_ref
partition_context_ref
visibility_context_ref
delivery_guarantee_envelope
arrival_observation
duplicate_or_redelivery_classification
acknowledgement_result
consumer_processing_result
semantic_commitment_ref_if_any
projection_ref_if_any
projection_freshness_context
failure_or_constraint_reason
```

This is an evidence shape, not a mandatory production schema.

## 50. Projection evidence envelope

A material projection case should eventually be able to preserve:

```text
projection_case_id
projection_identity
projection_purpose
source_authority_ref
source_semantic_fact_refs
version_effectivity_context
visibility_context
last_applied_semantic_context
freshness_or_lag_envelope
rebuildability_classification
rebuild_source_ref_if_lawful
rebuild_result
semantic_equivalence_or_constraint_result
```

This is also evidence shape only.

## 51. Result vocabulary

A bounded EVENT evaluation may lawfully conclude:

- `delivery_preserves_semantic_authority`;
- `duplicate_delivery_is_semantically_idempotent`;
- `delivery_order_is_nonauthoritative`;
- `semantic_order_preserved_from_existing_owner`;
- `projection_is_lawfully_derivative`;
- `projection_is_lawfully_stale_within_declared_envelope`;
- `notification_is_nonauthoritative`;
- `request_or_proposal_remains_uncommitted`;
- `transport_acknowledgement_only`;
- `inconclusive_missing_semantic_identity`;
- `inconclusive_missing_causal_context`;
- `inconclusive_missing_version_context`;
- `inconclusive_missing_visibility_context`;
- `inconclusive_missing_persistence_contract`;
- `not_authority_safe`;
- `unsupported_message_case`.

Unknown does not become pass.

## 52. Corpus-scale pressure families

PR2-EVENT must survive pressure from at least:

- synchronous local TTRPG-like resolution;
- asynchronous multiplayer commands;
- turn-based queues;
- simultaneous-action systems;
- interrupt/reaction chains;
- deterministic and stochastic resolutions;
- dice/cards/bags/oracle/random-table systems;
- MMO-style world updates;
- chat/social/relation notifications;
- market, auction, crafting, and reservation updates;
- institution/government workflows;
- ecological/world-process updates;
- vehicles, ships, mechs, crews, and platforms;
- companions, summons, swarms, and distributed embodiment;
- multi-body or distributed actors;
- hidden-information games;
- spectator and observer projections;
- AI/NPC read models;
- search/index projections;
- analytics projections;
- client prediction and reconciliation pressure;
- offline/deferred clients;
- intermittent connectivity;
- unreliable or duplicated delivery;
- reordered delivery;
- local single-process runtimes;
- multi-worker runtimes;
- cross-partition messaging;
- external webhook/service integrations;
- event-sourced implementations;
- non-event-sourced implementations;
- CQRS-like implementations;
- non-CQRS implementations;
- pub/sub, queues, logs, callbacks, mailboxes, and direct-call implementations.

No donor family or software pattern establishes universal EVENT law.

## 53. Important outliers

Escalate rather than invent when a case requires:

- new semantic commitment ownership;
- new command/retry identity doctrine;
- new logical-time or causality doctrine;
- new knowledge/perception doctrine;
- new visibility/disclosure doctrine;
- new correction/retcon doctrine;
- new branch/canonicality doctrine;
- new persistence/reconstruction law;
- new cross-world or transformed-time semantics;
- source-local metaphysics in which observation or message receipt itself changes
  ontology;
- a universal stale-command rule;
- a universal mandatory consensus, transaction, or transport algorithm.

PR2-EVENT is not a semantic super-owner.

## 54. Anti-collapse rules

PR2-EVENT must not collapse:

- request into command identity;
- request into commitment;
- proposal into commitment;
- event message into semantic committed event;
- publish into commit;
- acknowledgement into transition receipt;
- message identity into semantic fact identity;
- transport attempt into command attempt;
- redelivery into semantic retry;
- duplicate payload into duplicate semantic fact;
- queue order into causal order;
- arrival time into logical time;
- correlation into causation;
- delta into authoritative state;
- notification into knowledge;
- projection into truth;
- cache into authority;
- subscriber topology into ownership;
- partition crossing into authority transfer;
- projection rebuild into authoritative replay;
- transport technology into doctrine.

## 55. Completion condition

PR2-EVENT is complete when the repository contains a machine-testable contract
that explicitly bounds representation classes, transport-message identity,
transport-attempt identity, delivery/redelivery, duplicate handling,
idempotent consumption, acknowledgement, carried causality/order/version
context, committed-fact representation, delta/notification nonauthority,
projection derivation/freshness/rebuilding boundaries, visibility preservation,
cross-partition delivery, failure behavior, corpus-scale pressure, and
escalation.

It must preserve AFQR-01 commitment/replay ownership, AFQR-02 command/attempt/
retry identity, AFQR-04 logical time/causality/scheduling ownership, PR2-SCALE
topology independence, PR2-PART partition/migration ownership, PR2-CONC
scheduler nonauthority, R2B randomness/version/continuity qualifications,
separate PERSIST/FID/BP ownership, R3 authorization boundaries, and no runtime
implementation or technology mandate.

Completion of PR2-EVENT does not prove that a message bus, event stream,
projection store, distributed runtime, or durable recovery system exists. It
proves only that future message and projection implementations have a lawful
semantic contract to satisfy.
