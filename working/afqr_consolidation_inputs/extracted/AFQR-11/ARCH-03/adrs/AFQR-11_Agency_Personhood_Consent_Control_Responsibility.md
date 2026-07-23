# ADR AFQR-11 — Agency, Personhood, Consent, Control, and Responsibility

Status: Proposed for ratification  
Repository baseline: `928bb79ce00a2de749d127dcc5cb8299de788a15`

## Decision

Adopt **Registered Purpose-Scoped Agency and Personhood Architecture with Orthogonal Consent-Control Planes, Bitemporal Action-Origin Graphs, and Profiled Responsibility** (`RPSAP-OCC-BAOG-PR`).

## Context

Astra must absorb heterogeneous donor rules for actors, familiars, summons, possession, charm, domination, AI, collectives, offices, contracts, consent, and responsibility without importing a donor hierarchy or making the language model authoritative.

## Binding law

> No entity, actor, owner, creator, controller, command issuer, executor, beneficiary, or state owner is presumed to possess agency, personhood status, decision authority, valid consent, action authorship, or responsibility. Each is a separate purpose-scoped, versioned determination grounded in typed identity, epistemic, relation, capacity, consent, control, command, and causal records. Only owner-prepared AFQR-01 transitions may mutate runtime state, and later attribution or responsibility never rewrites historical action origin.

## Consequences

- Agency and personhood are profile-scoped.
- Capacity and consent are decision- and time-specific and orthogonal.
- Ownership, creation, authority, practical control, execution, authorship, causation, benefit, and responsibility are separate.
- Commands have issuance, interpretation, acceptance/refusal, and execution stages.
- Control is allocated by dimension.
- Collective action requires registered procedures.
- Causal graphs do not decide responsibility.
- Hidden agency data is projected through audience-scoped opaque tokens.
- Current RT-002 actor references remain identity-only fixtures.

## Rejected alternatives

- single actor/controller field
- capability plus permission as complete model
- legal-person/owner hierarchy
- BDI as foundational agency law
- causal graph alone
- principal-agent graph alone
- unbounded layered model without profile registries

## Ratification gate

Ratification requires all pack validators to pass, followed by the non-mutating dry run and RT-002A–RT-002F side-channel audit.
