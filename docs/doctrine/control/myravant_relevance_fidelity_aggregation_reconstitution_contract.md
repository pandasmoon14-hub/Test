# Myravant Relevance, Fidelity, Aggregation, and Reconstitution Contract — PR2-FID

```yaml
artifact_id: PR2-FID-RELEVANCE-FIDELITY-AGGREGATION-RECONSTITUTION-001
status: active_control_doctrine
layer: 0_control
workstream: PR2-FID
authority_reference: owner_directive_2026-09-15_pr2_fid_activation
authority_effect: runtime_fidelity_contract_only
starting_baseline: bc79bc629f3cc6bff220c8e71c37d9df515b9f8c
inherits:
  - POST-R2A-TRANSITION-PROGRAM-001
  - PR2-SCALE-RUNTIME-SCALABILITY-EXECUTION-TOPOLOGY-001
  - AFQR-R2B-CORE-QUALIFICATIONS
  - AFQR-R2B-CROSS-PHASE
  - AFQR-R2B-CONTINUITY-QUALIFICATIONS-001
  - PR2-PERSIST
runtime_implementation_authority: none
production_schema_authority: none
performance_budget_authority: none
persistence_authority: none
commitment_authority: none
identity_authority: none
truth_or_knowledge_authority: none
sensing_authority: none
canon_authority: none
live_play_authority: none
```

## 1. Purpose

PR2-FID defines how Myravant may vary simulation detail without allowing
simulation resolution to change authoritative meaning.

It exists so the world does not require equal computational detail
everywhere while preserving persistent-world consistency, deterministic
authority, player freedom, and lawful reconstruction.

The core problem is not merely level of detail.

It is:

```text
what must remain semantically exact
+ what may be represented more coarsely
+ what detail is merely unresolved
+ what detail is already committed
+ when omitted detail must be restored or lawfully resolved
```

PR2-FID owns that boundary only.

## 2. Existing semantic owners remain authoritative

PR2-FID coordinates existing owners and does not absorb them.

- AFQR-01 retains commitment, qualified mutation, replay, recovery,
  receipts, and committed-history boundaries.
- AFQR-04 retains logical time, causality, simultaneity, scheduling,
  and temporal placement.
- AFQR-08 retains identity and continuity.
- AFQR-09 retains governed relations, dependency lifecycle,
  revocation, migration, orphaning, and cascading consequences.
- AFQR-10 retains authoritative world truth, observer-relative truth,
  knowledge, belief, memory, uncertainty, and projection semantics.
- AFQR-20 retains sensing, acquisition, detection, recognition,
  concealment, and tracking.
- R2B-CORE retains proposal nonauthority and committed-randomness
  preservation.
- R2B-CROSS-PHASE retains version identity, applicability, pinning,
  and effective intervals.
- R2B-CONTINUITY retains timeline, branch, canonicality, correction,
  and continuity distinctions.
- PR2-PART retains partition and migration semantics.
- PR2-CONC retains deterministic concurrency and commitment-ordering
  semantics.
- PR2-EVENT retains command/event/message/projection semantics.
- PR2-PERSIST retains durable representation, snapshot, replay,
  recovery, and reconstruction architecture.
- PR2-BP owns performance budgets, overload, and backpressure.

## 3. Definitions

For this contract:

**relevance** means the scoped determination of which semantic dimensions
require which simulation resolution for a bounded situation.

**fidelity** means the resolution at which a governed aspect is represented
or simulated.

**aggregation** means a lawful reduction in represented detail while
retaining the authoritative basis required by the declared invariants.

**reconstitution** means restoration of detail from sufficient retained
authoritative basis.

**materialization** means a separately lawful resolution that creates
previously unresolved detail when that detail becomes necessary.

Reconstitution and materialization are not synonyms.

## 4. Core nonauthority laws

Relevance is multidimensional and scoped.

Camera distance, player proximity, visibility, and render presence are not authority.

Fidelity is not truth rank.

Fidelity is not identity rank.

Fidelity is not canon rank.

Fidelity is not commitment rank.

Fidelity is not a permission tier.

A fidelity transition is not a commitment event.

An aggregate representation does not acquire ownership of the semantics it
summarizes.

## 5. Relevance is not distance

Spatial distance may be one relevance input where a domain legitimately
uses it.

It is never the universal relevance function.

Relevant dimensions may include, where already semantically meaningful:

- active causal interaction;
- pending consequences;
- scheduled obligations;
- relationship or dependency pressure;
- ownership or resource effects;
- player-directed attention;
- imminent interaction opportunity;
- environmental coupling;
- hidden-information constraints;
- unresolved authoritative decisions;
- continuity or identity sensitivity;
- recovery or reconstruction needs.

The presence of one dimension does not automatically dictate a universal
fidelity level.

## 6. Relevance is not visibility or knowledge

Something may be highly relevant while unseen.

Something may be visible while requiring little simulation detail.

Sensing does not create truth.

Knowledge does not create world state.

Hidden information does not become irrelevant merely because a player
cannot currently observe it.

PR2-FID therefore consumes AFQR-10 and AFQR-20 rather than redefining them.

## 7. Fidelity is scoped by aspect

There is no universal fidelity-tier list.

One entity, place, institution, process, or region may legitimately have
different resolution for different aspects at the same time.

Examples include:

- detailed combat state with coarse economic context;
- persistent individual identity with aggregated routine labor;
- exact contractual obligations with aggregated travel progress;
- exact inventory ownership with coarse ambient ecology;
- exact scheduled consequence with coarse intervening activity.

A global `low`, `medium`, `high` label may exist as an implementation
convenience, but it does not by itself define semantic obligations.

## 8. No full-fidelity-everywhere requirement

Persistent existence does not require continuous full-detail execution.

Myravant may use:

- event-driven processes;
- delayed consequences;
- aggregate state;
- dormant state;
- scoped summaries;
- lawful reconstitution;
- other future implementation techniques.

None is mandatory.

The requirement is semantic preservation, not a specific simulation
architecture.

## 9. Committed detail and unresolved detail are distinct

Previously committed detail may be omitted from an active representation but is not thereby erased.

Unresolved detail is not committed detail.

A coarse representation must not silently convert:

```text
detail not currently represented
```

into:

```text
detail that never existed
```

or convert:

```text
detail never authoritatively resolved
```

into:

```text
a supposedly recovered historical fact
```

## 10. Fidelity reduction cannot erase history

Lowering fidelity must not silently erase or rewrite:

- committed outcomes;
- identity continuity;
- ownership;
- governed relations;
- unresolved obligations;
- active conditions;
- scheduled consequences;
- committed randomness provenance;
- version applicability;
- correction/supersession history;
- required knowledge or hidden-information distinctions;
- required receipts or causal ancestry.

Physical omission is not semantic deletion.

## 11. Aggregation qualification

Aggregation is lawful only when its retained basis is sufficient for the
declared invariants of the bounded scope.

If the proposed aggregate state cannot preserve a required semantic
invariant, that aggregation is unsupported for that scope.

The correct response is to retain more detail, use another lawful
representation, or escalate.

Performance pressure does not authorize illegal aggregation.

## 12. Aggregate state has explicit semantic scope

An aggregate fact may be authoritative for its declared scope when produced
and committed through lawful existing authority.

That does not imply arbitrary individual facts beneath it.

Aggregation must not manufacture a microstate merely because an aggregate value exists.

For example, an authoritative population count does not by itself identify
which particular individuals died, moved, reproduced, or changed status.

A treasury total does not by itself identify a fictional transaction
history.

A production total does not by itself identify which worker performed each
action.

## 13. Aggregation cannot create illegal states

A lower-resolution representation must respect the same applicable
authoritative constraints as the detailed state it represents.

Aggregation may not:

- create resources from nowhere;
- duplicate ownership;
- erase debts or obligations;
- bypass dependency constraints;
- ignore committed injuries or conditions;
- violate identity continuity;
- discard pending authoritative consequences;
- bypass version applicability;
- silently reroll randomness;
- grant knowledge or sensing.

Approximation is not permission to violate rules.

## 14. Conservation and invariant surfaces

A fidelity profile must identify the invariant surface that survives any
supported reduction or expansion.

The exact surface is domain-specific.

It may include, where material:

- quantities or conserved resources;
- ownership;
- identity;
- relationship obligations;
- condition state;
- causal ancestry;
- scheduled consequences;
- historical commitments;
- version context;
- randomness provenance;
- hidden-information boundaries;
- other domain invariants.

PR2-FID does not create one universal invariant schema.

## 15. Materialization is separate from reconstitution

Reconstitution restores detail that can be supported by retained
authoritative basis.

Materialization lawfully resolves previously unresolved detail.

Reconstitution must not claim to recover detail that was never retained or committed.

A fidelity increase alone grants no authority to materialize new facts.

When new detail must be materialized, the relevant existing semantic owners
govern legality, resolution, commitment, time, randomness, version context,
identity, knowledge, and consequences.

## 16. No invented history during promotion

Promotion to greater detail must distinguish:

1. retained committed detail being restored;
2. deterministic derivation already implied by committed state;
3. previously unresolved detail requiring lawful materialization.

Category 3 must never be disguised as category 1.

The system must not generate a detailed past merely because a player has
arrived and detailed rendering is now desirable.

## 17. Reconstitution basis

Reconstitution must have sufficient attributable basis for the detail it
claims to restore.

Depending on the case, that basis may include:

- committed aggregate state;
- retained exact facts;
- applicable version context;
- causal history;
- scheduled obligations;
- identity and relationship state;
- randomness provenance;
- other lawfully retained information.

PR2-PERSIST owns durable recovery of that basis.

PR2-FID owns whether the basis is semantically sufficient for the requested
fidelity transition.

## 18. Deterministic and reproducible promotion

Where a fidelity transition is claimed to be pure reconstitution, equivalent
authoritative basis must not produce arbitrary semantic differences merely
because of worker count, wall-clock timing, machine placement, or repeated
loading.

If lawful materialization includes randomness, R2B-CORE governs preservation
and provenance.

If rules/packages/overrides differ across time, R2B-CROSS-PHASE governs
applicable version identity and effectivity.

## 19. Cross-fidelity interaction barrier

If omitted detail is material to an authoritative decision, the required scope must be lawfully reconstituted or materialized before commitment.

A low-fidelity approximation must not silently decide an outcome that
requires unavailable higher-resolution facts.

A domain may possess an explicitly lawful aggregate-resolution rule.

If so, that rule may commit only the facts within its authorized output
scope.

PR2-FID does not invent such domain rules.

## 20. Background processes

Lower fidelity does not authorize time passage.

AFQR-04 and existing process/domain semantics determine whether a background
process is eligible to advance.

PR2-FID only governs the resolution at which an already lawful process may
be represented or evaluated.

Background execution may not silently outrun, skip, or rewrite committed
causal consequences.

## 21. Background-to-foreground reconciliation

Foreground promotion must reconcile all semantically relevant background
consequences before an authoritative interaction depends on the promoted
state.

Reconciliation may need to preserve:

- committed state changes;
- scheduled consequences;
- relationships and obligations;
- resources and ownership;
- conditions;
- causal order;
- version context;
- randomness provenance;
- continuity distinctions.

Reconciliation is not permission to rewrite history for narrative
convenience.

## 22. Foreground-to-background reduction

Moving a scope out of immediate attention may reduce simulation resolution
only after the required invariant surface has been retained.

The transition must not discard state merely because no player is currently
looking at it.

Player absence is not semantic deletion.

## 23. Player freedom across fidelity boundaries

Fidelity reduction is not a lawful reason to reject a fictionally coherent player attempt.

When a player unexpectedly interacts with a lower-fidelity person, place,
object, institution, or process, the system should lawfully promote the
necessary scope, resolve genuinely unresolved detail where authorized, or
fail/escalate for an actual semantic reason.

A closed command menu must not be introduced merely to protect an
aggregation shortcut.

Promotion does not guarantee success.

## 24. Persistent NPCs and entities

Off-screen entities need not execute at full detail continuously.

But lowering fidelity must not silently erase persistent identity or
authoritative state that remains relevant to future interaction.

Examples include:

- enduring relationships;
- obligations;
- ownership;
- injuries or conditions;
- institutional roles;
- memories or knowledge where already authoritative;
- pending plans only where those plans have authoritative representation;
- other committed consequences.

PR2-FID does not define NPC psychology or gameplay content.

## 25. Fidelity-cycle equivalence

A supported cycle such as:

```text
detailed
-> aggregate
-> detailed
```

with no intervening semantic input must preserve the declared authoritative
invariant surface.

A cycle must not create:

- free resources;
- lost obligations;
- identity changes;
- rerolled committed outcomes;
- hidden-information leaks;
- new historical facts;
- deleted consequences.

This is the FID contribution to PR2-SCALE equivalence testing.

## 26. Partial and heterogeneous fidelity

Myravant does not require an entire world, region, entity, or subsystem to
move between fidelity states as one indivisible block.

Different governed aspects may transition independently when their semantic
dependencies permit it.

Coupled aspects must not be separated when doing so would invalidate a
required invariant.

## 27. Persistence does not choose fidelity semantics

PR2-PERSIST may durably store exact state, aggregate state, transition
metadata, or reconstruction basis.

Storage format does not decide whether an aggregation is lawful.

Snapshot existence does not prove sufficient reconstitution basis.

Replay does not convert unresolved detail into committed history.

## 28. Messages and projections do not choose fidelity semantics

PR2-EVENT may represent messages, notifications, projections, or committed
event records related to fidelity transitions.

Delivery does not make a fidelity transition lawful.

A projection may display coarse or detailed information only within its
lawful truth, knowledge, sensing, continuity, and disclosure basis.

## 29. Partitioning and concurrency remain separate

Fidelity boundaries are not automatically partition boundaries.

Aggregate scopes are not automatically workers, shards, processes, or
services.

Parallel computation does not determine fidelity authority.

PR2-PART and PR2-CONC retain those concerns.

## 30. Performance and overload remain PR2-BP

PR2-BP owns performance budgets, overload, and backpressure.

PR2-BP may later request or prefer a lower-cost fidelity mode.

It may not force an illegal fidelity transition.

FID determines what reductions are semantically lawful.

BP determines how performance pressure is handled within those lawful
options.

## 31. Representative pressure cases

This contract must survive at least:

- a distant but causally critical actor;
- a nearby irrelevant ambient object;
- an off-screen NPC with a pending obligation;
- a dormant institution with exact debts but coarse daily activity;
- a large population represented statistically;
- a population aggregate where individual casualties were never resolved;
- an individual casualty already committed before aggregation;
- a hidden actor relevant to an imminent event;
- a visible crowd whose individual histories are not all material;
- an unexpected player visit to an aggregated settlement;
- a player targeting one member of an aggregate population;
- a background journey with scheduled consequences;
- aggregate resource production with exact ownership constraints;
- detailed-to-aggregate-to-detailed cycling;
- crash/recovery while a scope is aggregated;
- version change across a background interval;
- randomness-bearing materialization;
- branch/correction pressure;
- cross-partition interaction;
- overload pressure requesting lower fidelity;
- local/offline play without network services.

## 32. Failure and escalation

A fidelity transition must fail closed or escalate when:

- required invariants cannot be identified;
- retained basis is insufficient;
- committed and unresolved detail cannot be distinguished;
- reconstruction would require invented history;
- aggregate resolution would exceed its lawful output scope;
- a transition would violate identity, ownership, relation, knowledge,
  sensing, version, randomness, or causal constraints;
- performance pressure is the only justification for semantic loss.

Failure is evidence.

It does not automatically justify a new semantic owner or generalized
subsystem.

## 33. Technology neutrality

PR2-FID mandates none of the following:

- ECS;
- LOD framework;
- spatial partitioning;
- interest-management algorithm;
- simulation tick rate;
- database;
- cache;
- message bus;
- streaming engine;
- job scheduler;
- distributed runtime;
- cloud provider;
- AI provider.

A future implementation may use such techniques only under separately
authorized implementation work.

## 34. R3 remains separate

PR2-FID does not execute R3.

R3 remains separately authorized against its exact accepted candidate set.

Fidelity doctrine may later be part of conformance evidence.

It does not pre-answer that review.

## 35. Completion condition

PR2-FID is complete when the repository explicitly establishes and
executable tests verify that:

- relevance is multidimensional and scoped rather than camera-distance
  authority;
- fidelity is not truth, identity, or commitment rank;
- aggregation preserves declared authoritative invariants;
- committed detail cannot be erased by lowering fidelity;
- unresolved detail cannot be disguised as recovered history;
- reconstitution and materialization remain distinct;
- cross-fidelity interactions cannot silently commit from insufficient
  detail;
- background/foreground transitions preserve causal continuity;
- player freedom is not restricted merely to protect aggregation;
- performance pressure remains subordinate to lawful fidelity semantics;
- no universal fidelity tiers or implementation technology are mandated;
- PR2-BP, PR2-TEST, R3, and implementation remain separately authorized.

This contract is architecture governance only.

Implementation remains separately authorized.
