# D19-03 — Record-Shape Registry, Not-Final-Schema Governance, and Schema-Handoff Control

> **Status:** Phase 1 capstone doctrine. This file is a control-layer artifact for Astra Ascension doctrine integration. It is not final sourcebook prose, not a live-play GM adapter, not a runtime/backend schema, and not a donor conversion output. Any record shapes in this pack are lightweight doctrine-facing / conversion-facing / audit-facing shapes only and may be replaced or formalized later by Batch C schema doctrine, Runtime Gate B, canon consolidation, or playtest calibration.


## Core question

How does Astra inventory, govern, and harmonize the lightweight record shapes created across D00–D18 so they remain useful for doctrine, conversion, audit, and future runtime planning without being mistaken for final backend schemas?

## Record Registry and Schema-Handoff Model

D19 uses this procedure:

```text
1. Identify each record shape.
2. Identify owning doctrine file.
3. Identify record purpose.
4. Identify facing: doctrine, conversion, audit, canon, runtime handoff, or mixed.
5. Identify dependent owner files.
6. Identify whether it is a duplicate, subtype, handoff companion, or unique record.
7. Mark not-final-schema status.
8. Identify likely future schema home.
9. Identify misuse risks.
10. Assign registry status.
```

## Facing classifications

Records may be classified as:

```text
doctrine_facing
conversion_facing
audit_facing
canon_consolidation_facing
runtime_handoff_facing
source_local_governance_facing
mixed_facing
```

A record may have multiple facings. A mixed-facing record must still preserve phase separation.

## Mandatory warning on every registry entry

Every registry entry must mark:

```text
not final schema
not backend-ready
not player-facing rule text
not a database contract
not a runtime context-packet format
not a sourcebook statblock
may be replaced or formalized by later Batch C / Runtime Gate B schema doctrine
```

## Likely future schema homes

Registry entries should name one likely future home or explicitly mark no expected schema:

```text
Batch_C_resolution_schema
Batch_C_resource_schema
Batch_C_advancement_schema
Batch_C_actor_schema
Batch_C_object_item_platform_schema
Batch_C_world_state_schema
Batch_C_project_schema
Batch_C_travel_exploration_schema
Batch_C_faction_relationship_schema
Batch_C_opposition_encounter_schema
Batch_C_economy_inventory_reward_schema
Batch_C_campaign_state_schema
Runtime_Gate_B_context_packet_schema
Runtime_Gate_B_save_state_schema
Runtime_Gate_B_event_log_schema
Canon_sourcebook_consolidation
Conversion_pipeline_IR
Source_local_registry
No_schema_expected
Unknown_future_schema
```

## Duplicate and overlap relationships

Record overlap is not automatically a conflict. D19 classifies relationships as:

```text
unique_record
companion_record
subtype_record
superset_record
overlaps_with_record
possible_duplicate
duplicate_requires_patch
handoff_pair
source_local_variant
schema_phase_merge_candidate
```

Examples:

- D16 Donor Opposition Mapping Record and D17 Donor Value Mapping Record are companion records.
- D17 Ownership / Custody Record and future D09 object-state schema may overlap, but they own different domains.
- D18 Structural Time State Record and D10 world-state records are companion records.
- D18 Runtime Persistence Handoff Note and future Runtime Gate B context-packet schema are handoff-related, not the same artifact.

## Misuse-risk flags

D19 records misuse risks, including:

```text
may_be_mistaken_for_final_schema
may_be_mistaken_for_player_rule
may_duplicate_owner_file_schema
may_steal_owner_authority
may_overfit_to_donor
may_hide_source_local_boundary
may_expose_hidden_state
may_create_runtime_assumption
may_create_canon_assumption
may_be_too_vague_for_conversion
may_be_too_detailed_for_doctrine
```

## Registry status

Each registry entry receives one status:

```text
accepted_doctrine_record
accepted_with_handoff_note
needs_minor_clarification
possible_duplicate_review
needs_owner_boundary_review
needs_future_schema_owner
source_local_only
quarantined_record_shape
escalated_schema_gap
retired_record_shape
```

## Minimum registry coverage

D19 must cover record families from D12–D18 and any available D00–D11 record shapes. At minimum, D19 tracks D16–D18 and D19 records.

### D16 families

```text
Opposition Profile
Opposition Pressure Profile
Capability Pressure
Constraint / Vulnerability / Resistance Routing
Threat Weight Review
Encounter Composition
Behavior / Morale / Posture
Recurrence / Continuity
Donor Opposition Mapping
Owner-file handoff / unresolved opposition pressure
```

### D17 families

```text
Value State
Access Channel
Acquisition / Exchange
Value Entry
Ownership / Custody
Inventory / Burden
Loss / Confiscation / Recovery
Sink / Requisition / Upkeep
Debt / Obligation Value
Donor Value Mapping
Owner-file handoff / unresolved value pressure
```

### D18 families

```text
Structural Time State
Continuity Lifecycle
Arc Promise / Question
Pacing / Contrast / Payoff Budget
Season Throughline / Seam
Long-Horizon Trajectory / Phase / Rotation
Transformation / Breakthrough / Major Change Spacing
Time Skip / State Aging / Pruning
Donor Structural-Time Mapping
Runtime Persistence Handoff Note
Owner-file handoff / unresolved structural-time pressure
```

### D19 families

```text
Owner Boundary Audit Entry
Cross-Pack Handoff Entry
Record Shape Registry Entry
Deferred Work Ledger Entry
Mixed Donor Routing Stress Test Entry
Capstone Readiness Entry
Capstone DDR Entry
```

## Record governance principles

- A doctrine record is not a runtime schema.
- A doctrine record is not a player-facing rule.
- A doctrine record is not a sourcebook statblock.
- A record shape can be useful even if later replaced.
- Record overlap may be a handoff pair or companion record.
- A record is dangerous if it silently claims owner-file authority.
- A record is dangerous if it hides source-local boundaries.
- A record is dangerous if it exposes hidden state to the wrong facing.
- Future schema work must consult this registry before inventing new structures.

## Acceptance criteria

D19-03 is accepted if it governs record identities, facings, warnings, dependencies, future schema homes, overlaps, misuse risks, and registry statuses without treating doctrine records as final schemas.
