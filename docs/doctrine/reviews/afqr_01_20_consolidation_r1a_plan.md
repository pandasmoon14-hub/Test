# AFQR-01–20 Consolidation R1A Plan

## Classification

- Artifact ID: `AFQR-CONSOLIDATION-R1A-PLAN-001`
- Milestone: `MILESTONE-AFQR-CONSOLIDATION-AND-RUNTIME-REENTRY`
- Gate: `R1 — AFQR-01–20 consolidated`
- Step: `R1A — accepted-selection registration and consolidation planning`
- Status: `planning-current`
- Authority level: tracking and consolidation planning
- Implementation authority: none
- Canon authority: none
- Conversion authority: none
- Live-play/model authority: none

## Baseline

R0 is complete at merge commit `ff4de6d8c68e4251a110ac0c6c0b2c2495ad2ab0`, the merge of PR #329. The repository baseline is green. R1 is now the active milestone gate.

This artifact does not declare R1 complete. It establishes the lawful work package required to consolidate the twenty accepted Astra Foundational Question Resolution selections without collapsing doctrine, conversion, canon, runtime, or play-facing behavior.

## Why R1A exists

The project has twenty accepted architectural selections, but they are not yet present in the repository as one coherent, cross-referenced authority set. Treating the selected titles alone as complete doctrine would create fake certainty. Proceeding directly to RT-002G would allow narrow RT fixtures to continue evolving without the typed identity, time, dependency, epistemic, settlement, embodiment, topology, capability, and signal contracts that those fixtures will eventually need.

R1A therefore registers what has been accepted, records what remains absent, defines the first dependency and collision-control model, and specifies the acceptance tests for the complete R1 gate.

## R1A deliverables

1. `afqr_01_20_authority_index.yaml`
   - registers exactly twenty accepted selections;
   - identifies the owning architectural cluster for each selection;
   - states what each architecture owns and must not own;
   - records that the source dossier is pending repository consolidation;
   - grants no runtime implementation authority.

2. `afqr_01_20_dependency_matrix.yaml`
   - records consolidation inputs rather than pretending to define a final implementation DAG;
   - names the principal cross-AFQR cycles;
   - assigns a cycle breaker and type owner for each collision seam;
   - prevents generic graph, state, relation, or event types from absorbing domain-specific meaning.

3. Focused repository tests
   - require all twenty IDs and selections;
   - require R0 complete and R1 active;
   - require R2–R6 and RT-002G to remain blocked;
   - validate dependency references and collision owners;
   - prevent this planning package from claiming implementation, canon, conversion, or model authority.

## Consolidation clusters

### Substrate and coordination

- AFQR-01 transition and invariant journal
- AFQR-04 logical-time causal scheduler
- AFQR-05 interface-and-bridge hypergraph
- AFQR-08 identity, continuity, and lineage
- AFQR-09 dependency and obligation hypergraph

These files provide shared typed substrate. They must remain small and explicit. They may not become one universal object, one universal graph, or one universal event schema.

### Command, action, claim, and settlement

- AFQR-02 command fast path and durable attempt escalation
- AFQR-03 typed action gateway
- AFQR-06 typed claim arbitration
- AFQR-07 balance-domain flow ledger and atomic settlement
- AFQR-19 capability, opportunity, targeting, and resolution

These architectures must preserve the difference between command intake, action semantics, capability, opportunity, legality, resolution, reservation, settlement, and event commitment. Donor action economies, initiative models, currencies, and resource pools are not Astra defaults.

### Truth, agency, behavior, and social interpretation

- AFQR-10 bitemporal truth and epistemic provenance
- AFQR-11 purpose-scoped agency and personhood
- AFQR-12 motivational and behavioral state
- AFQR-13 multiplex social state
- AFQR-14 communication and interpretation
- AFQR-15 institutions and jurisdiction

These architectures must permit contradictory beliefs, asymmetric information, social multiplicity, institutional conflict, nonhuman or distributed agency, and communication failure. Model context remains a projection and never becomes truth authority.

### World, body, place, and sensing

- AFQR-16 embodiment and integrity
- AFQR-17 environment and process
- AFQR-18 spatiotemporal topology
- AFQR-20 signal, sensing, and acquisition

These architectures must survive fantasy, science-fiction, hybrid, cultivation, cyberware, biotech, psionic, horror, vehicle, mech, ship, companion, swarm, distributed-body, non-Euclidean, virtual, metaphysical, and source-local subsystem pressure. No single anatomy, space model, sensor family, damage model, or cosmology becomes universal law.

## Corpus-scale donor pressures

R1 consolidation must test every ownership boundary against at least these donor families:

- class, archetype, profession, occupation, point-buy, tag, aspect, and freeform character systems;
- fantasy magic, cultivation, psionics, cyberware, biotech, relic, tool, ritual, contract, and technique systems;
- combat, social conflict, investigation, horror, stealth, chase, downtime, crafting, salvage, requisition, and domain play;
- companions, summons, familiars, vehicles, mechs, ships, platforms, factions, institutions, settlements, and distributed organizations;
- deterministic, dice-pool, step-die, percentile, card, oracle, token, bidding, narrative, and mixed resolution systems;
- local, global, asynchronous, simultaneous, reaction-heavy, interrupt-heavy, turnless, and clock-driven time models;
- ordinary geometry, layered planes, networks, dream spaces, conceptual spaces, nested worlds, moving frames, and non-Euclidean topology.

Outliers are expected. A donor construct must map directly, normalize, remain source-local, enter quarantine, or escalate a doctrine problem. R1 must not solve missing framework through decorative Astra terminology.

## R1 work sequence

### R1A — Register and plan

This package. Records selections, boundaries, dependencies, collision seams, manifest, and completion criteria.

### R1B — Reconstruct or import the twenty source dossiers

Each AFQR requires a repository-resident decision dossier containing definitions, ownership, invariants, rejected alternatives, donor-family pressure tests, outliers, implementation handoffs, conversion handoffs, and unresolved escalation points. Accepted titles alone are insufficient.

### R1C — Consolidate shared vocabulary and invariant register

Produce a controlled vocabulary with one owner for every shared term. Build the cross-AFQR invariant register covering authority, identity, time, provenance, hidden information, deterministic transition, transaction atomicity, replay, phase separation, and the conversion-runtime origin firewall.

### R1D — Consolidate handoff contracts

Define typed handoffs among the twenty architectures. Produce the doctrine-to-runtime handoff map, doctrine-to-conversion handoff map, and reserved canon/play-facing boundaries. Identify every fixture that cannot be generalized without R4 substrate.

### R1E — R1 completion review

Audit all R1 artifacts against the acceptance criteria below. Only this review may declare R1 complete and authorize R2 doctrine-drift resolution.

## Acceptance criteria for R1 completion

R1 is complete only when all of the following are true:

1. Exactly twenty repository-resident AFQR decision dossiers exist and identify their accepted selection.
2. Every dossier states what it owns, what it must not own, its authority level, its dependencies, donor-family pressures, collapse risks, outliers, escalation routes, and phase handoffs.
3. The shared vocabulary assigns one controlling owner to every cross-AFQR term and records aliases without silently merging unlike concepts.
4. The dependency model distinguishes substrate dependency, runtime invocation, evidence handoff, authority handoff, and bidirectional integration.
5. Every dependency cycle has an explicit cycle breaker or shared lower-level substrate.
6. The invariant register covers backend authority, deterministic mutation, bitemporal truth, hidden-information containment, provenance, replay, atomicity, phase separation, and donor-origin isolation.
7. The conflict ledger has no unresolved contradiction lacking an owner, quarantine route, or scheduled doctrine decision.
8. The runtime handoff map distinguishes current fixtures from generalized contracts and grants no implementation authority by implication.
9. The conversion handoff map preserves lawful outcomes and prevents donor metaphysics, packages, progressions, economies, and action assumptions from becoming Astra baseline law.
10. Canon consolidation and play-facing/model behavior remain separate later phases.
11. Automated tests verify the authority index, dependency references, collision ownership, phase gates, and non-authority boundaries.
12. A formal R1E review records either `R1_COMPLETE` or `R1_BLOCKED`; no intermediate artifact may self-promote the gate.

## Current gate posture

- R0 baseline green: complete
- R1 AFQR consolidation: active, incomplete
- R2 doctrine drift resolution: blocked by R1
- R3 repository conformance audit: blocked by R2
- R4 common amendment substrate: blocked by R3
- R5 RT-002A–F retrofit: blocked by R4
- R6 RT-002G re-entry decision: blocked by R5
- RT-002G implementation: unauthorized

## Explicit non-authority boundaries

This R1A package does not:

- implement or alter runtime behavior;
- alter RT-002A–F;
- authorize RT-002G;
- define final shared schemas;
- promote any converted material to canon;
- modify conversion behavior;
- create sourcebook content;
- create model prompts, narration, training examples, or live-play behavior;
- make the AFQR titles substitutes for their full decision dossiers.

## Next allowed step

`R1B — repository-resident AFQR source-dossier reconstruction/import plan and first bounded dossier batch.`

R1B should be split into reviewable batches rather than one megafile or one twenty-dossier PR.