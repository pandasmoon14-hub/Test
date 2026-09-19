# Myravant PR2 Implementation Handoff Contract

Artifact ID: `MYRAVANT-PR2-IMPLEMENTATION-HANDOFF-CONTRACT-001`

Artifact version: `0.1.0`

Status: `active`

Workstream: `PR2-IMPL`

Authorization reference:

`owner_directive_2026-09-19_pr2_impl_activation`

Authority effect:

`bounded_implementation_handoff_definition_only`

Starting baseline:

`a429b4a65e7118a5b102ef9357a83bf236d4b1cd`

Starting tree:

`956ced445741ebe6e12e48f212eb3085943b97f8`

## 1. Purpose

PR2-IMPL is the bounded implementation-handoff gate between accepted
Myravant doctrine, architecture, evaluation evidence, and separately
authorized implementation packages.

PR2-IMPL does not itself implement runtime mechanics.

PR2-IMPL does not itself authorize runtime edits, production-schema
edits, content implementation, live play, canon promotion, R4-B,
R4 activation, or runtime promotion.

Its purpose is to make implementation work concrete enough that later
owner authorization can identify an exact package rather than grant
broad or ambiguous implementation authority.

## 2. Authority boundary

Activation authorizes only:

- recording bounded implementation packages;
- identifying concrete playable needs;
- routing existing accepted semantic ownership into those packages;
- recording implementation dependencies;
- recording exact acceptance criteria;
- recording prohibited authority transfers;
- determining whether a package is ready for separate owner authorization.

A package being defined, prioritized, dependency-complete, or ready does
not mean that package is authorized.

Infrastructure that stores, serializes, schedules, indexes, transports,
displays, or commits another subsystem's data does not gain semantic
ownership by doing so.

## 3. Carried PR2-TEST handoffs

The five nonblocking future-implementation handoffs are:

- `PR2-TEST-HANDOFF-TOPOLOGY-001`
- `PR2-TEST-HANDOFF-PERSIST-001`
- `PR2-TEST-HANDOFF-FIDELITY-001`
- `PR2-TEST-HANDOFF-BP-001`
- `PR2-TEST-HANDOFF-FAILURE-001`

These obligations remain preserved.

No carried handoff becomes a prerequisite merely because it exists.

A handoff blocks a concrete implementation package only when that
package actually depends on the missing capability or its acceptance
criteria cannot lawfully be satisfied without it.

## 4. Game-led implementation rule

Implementation sequencing follows:

playable need -> bounded capability -> executable evidence -> sustained play

PR2-IMPL must not manufacture infrastructure dependencies merely because
a more general capability may be useful later.

Real dependencies must be explicit and evidence-backed.

## 5. First playable implementation candidate

Package:

`R4-B`

Candidate:

`persistent_world_entity_location_representation_implementation`

Selected capability:

`persistent_world_entity_and_location_relation_representation`

Source:

`docs/doctrine/reviews/r4_a_myravant_native_substrate_design.yaml`

R4-B remains not ready pending authorization while PR2-IMPL is active.

R4-B remains unauthorized.

PR2-IMPL completion may make R4-B ready for a separate owner decision,
but PR2-IMPL completion may not itself authorize R4-B.

## 6. Preserved R4-A constraints

Any later R4-B package must preserve:

- campaign-local stable identity;
- character or creature, place, and object identity coverage;
- open-ended classification rather than a closed universal entity enum;
- typed relation representation;
- initial `located_at` relation semantics;
- `AFQR-18` as semantic owner of the initial location relation;
- canonical serialization;
- stable deterministic ordering;
- reuse of existing record-identity and state-owner surfaces where
  compatible;
- no model-generated identity authority;
- no model-generated relation authority;
- no universal world-state manager;
- no generalized governed-relation registry;
- no combined spatial, sensing, embodiment, institutional, and social
  owner.

A relation record may not imply control, agency, ownership, social state,
institutional authority, knowledge, visibility, or other semantics that
belong to separate owners.

## 7. Required package shape

Before an implementation package may be separately authorized, it must
record:

1. the concrete playable need;
2. the exact bounded capability being added or repaired;
3. the accepted semantic owners involved;
4. the exact implementation owner;
5. explicit dependencies;
6. exact runtime and production-schema paths that may be edited;
7. prohibited paths and authority;
8. deterministic acceptance criteria;
9. replay, recovery, or equivalence requirements where applicable;
10. failure behavior and fail-closed requirements;
11. performance evidence where materially relevant;
12. regression evidence required before merge;
13. downstream lifecycle transition after merge.

A package must not invent a broad manager, registry, generalized
substrate, or semantic owner merely to avoid representing the narrower
playable capability directly.

## 8. Model boundary

Models may assist with interpretation, narration, dialogue, planning,
retrieval, summarization, and proposals.

Models do not directly own:

- committed authoritative state;
- RNG outcomes;
- persistence authority;
- hidden truth;
- canon;
- ruleset authority;
- entity identity authority;
- relation authority.

Generated content becomes authoritative only through lawful validation,
compatibility, provenance, and commitment.

## 9. Failure routing

Implementation failure follows:

failure -> preserve evidence -> reproduce -> classify -> route to existing
owner -> separately authorize repair -> regression test

A failing test does not create missing doctrine or a new semantic owner.

## 10. Completion

PR2-IMPL completes when:

- the bounded package model is executable and tested;
- implementation ownership boundaries are explicit;
- all five future-implementation handoffs remain lawfully routed;
- speculative infrastructure cannot become an automatic prerequisite;
- acceptance criteria are explicit;
- prohibited authority transfers are explicit;
- R4-B is lawfully routed for a separate owner authorization decision.

Completion does not itself authorize R4-B, R4 activation, runtime
promotion, runtime edits, or production-schema edits.
