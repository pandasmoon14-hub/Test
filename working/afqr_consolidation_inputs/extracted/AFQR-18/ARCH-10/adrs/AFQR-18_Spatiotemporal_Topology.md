# ADR AFQR-18 — Federated Spatiotemporal Topology

## Status

Accepted for architectural ratification.

## Context

Astra must absorb 200–400 donor sources using incompatible coordinate systems, grids, zones, graphs, range bands, movement points, moving platforms, portals, navigation systems and source-local spaces. Current repository fields are conversion or fixture surfaces and do not provide authoritative spatial state.

## Decision

Adopt **Registered Federated Spatiotemporal Topology Architecture with Typed Domain–Frame–Support Ownership, Plural Metric–Reachability Profiles, Atomic Movement–Occupancy Transitions, and Bitemporal Map–Materialization Continuity** (`RFSTA-DFS-PMR-AMO-MMC`).

No place name, location field, coordinate tuple, map feature, route plan, range label, movement declaration, portal description, travel summary, donor rule, sensor estimate, public report, or model narration possesses spatial mutation authority by itself. Every authoritative spatial result is a purpose-scoped, version-pinned, bitemporal determination over frozen spatial-domain, reference-frame, transform, support, extent, topology, metric, occupancy, movement, portal, environmental, embodiment, identity, epistemic, agency, behavioral, social, communication, institutional, governed-relation, quantity, and scheduler bases. Only owner-prepared AFQR-01 transitions may change position, topology, occupancy, transit, or arrival; maps, observations, estimates, route beliefs, plans, and model wording remain separate append-only records.

## Consequences

- Spatial domains, frames, positions, supports, topology, metrics, movement, occupancy, portals, navigation and partitions receive federated owners.
- Coordinates, maps and route beliefs cannot mutate position.
- Reachability is purpose-, movement-, embodiment-, environment-, time- and resource-specific.
- Movement is an atomic occupancy transition with lawful transit and rollback.
- AFQR-17's provisional spatial references are closed architecturally.
- Authoritative runtime spatial mutation remains blocked until implementation and certification.
- The language model remains a renderer and candidate-wording layer only.

## Rejected alternatives

Universal coordinates, universal grids, universal zones, pure graphs, continuous physics alone, source-local adapters alone, navigation-centric state, and LLM-owned spatial interpretation were rejected as insufficient for corpus-scale mixed-source coherence.
