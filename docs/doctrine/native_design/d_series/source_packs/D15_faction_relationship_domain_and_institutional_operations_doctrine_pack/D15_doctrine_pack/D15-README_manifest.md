# D15 — Faction, Relationship, Domain, and Institutional Operations Doctrine Pack

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## Purpose

D15 defines how Astra Ascension handles organized social operation: factions, institutions, relationships, debts, favors, obligations, claims, law authorities, guilds, sects, corporations, kingdoms, domains, player organizations, institutional access, public pressure, and social campaigns.

D15 answers the question: how do organized social structures operate, respond, escalate, decay, negotiate, claim, punish, support, and change posture over time without turning factions into arbitrary AI, universal clocks, or donor kingdom-turn systems?

## Pack contents

1. `D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md`
2. `D15-01_organized_actors_standing_pressure_obligations_claims_and_operation_anatomy.md`
3. `D15-02_operation_creation_trigger_sources_scale_method_leverage_and_commitment.md`
4. `D15-03_operation_resolution_standing_shifts_pressure_lifecycle_and_consequence_routing.md`
5. `D15-04_operation_profiles_institutional_behavior_relationship_procedure_and_domain_operations.md`
6. `D15-05_institutional_capacity_concurrent_operations_pressure_movement_and_conflict.md`
7. `D15-06_source_local_faction_donor_institutional_mapping_quarantine_and_escalation.md`
8. `D15-07_records_not_final_schema_and_conversion_handoff_shapes.md`
9. `D15-09_integration_checklists_ddr_register_and_acceptance_criteria.md`
10. `D15_pack_manifest.json`

## Core architecture

D15 uses a Standing–Pressure–Operation Architecture:

```text
D10 records social/world state
  -> D15 identifies organized actor / relationship / domain pressure
  -> standing, pressure, obligation, claim, and capacity are reviewed
  -> Operation trigger is identified
  -> Operation scope, method, leverage, and cost are declared
  -> D12/D13/D17/D18/source-local handoff occurs when needed
  -> result changes standing, pressure, obligation, claim, access, treaty, law, territory, or domain posture
  -> D10 records resulting world-state delta
```

## Core D15 object families

- Organized Actor
- Standing
- Pressure
- Obligation / Claim
- Operation
- Operation Outcome
- Access Outcome
- Domain Posture
- Institutional Capacity / Operation Load
- Donor Institutional Mapping

## Binding non-ownership

D15 does not own D10 world-state storage, D17 economy procedure, D18 campaign pacing, D16 encounter/war construction, D12 immediate scene cadence, D13 Project intervals, D04/D05/D06 advancement/access/power implications, or final runtime schemas.

## Embedded risk controls

This pack embeds the full D15 pre-generation risk audit directly into the relevant files. The most important controls are:

- D15 does not become arbitrary faction AI.
- Organized actors are not giant NPCs.
- Standing is multi-axis, not a single reputation score.
- Faction clocks/tracks are not universal.
- Public belief is not actual truth.
- D15 domain control is not D06 domain expression.
- Player organizations are not free capability bundles.
- Contacts, favors, debts, obligations, ranks, guilds, sects, and patronage do not bypass owner-file doctrine.
- Source-local faction systems remain bounded unless reviewed.
- Record shapes are not final runtime schemas.
