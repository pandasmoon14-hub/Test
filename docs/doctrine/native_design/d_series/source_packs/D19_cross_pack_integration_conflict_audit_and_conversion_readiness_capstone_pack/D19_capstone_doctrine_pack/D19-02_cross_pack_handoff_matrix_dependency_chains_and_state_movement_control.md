# D19-02 — Cross-Pack Handoff Matrix, Dependency Chains, and State Movement Control

> **Status:** Phase 1 capstone doctrine. This file is a control-layer artifact for Astra Ascension doctrine integration. It is not final sourcebook prose, not a live-play GM adapter, not a runtime/backend schema, and not a donor conversion output. Any record shapes in this pack are lightweight doctrine-facing / conversion-facing / audit-facing shapes only and may be replaced or formalized later by Batch C schema doctrine, Runtime Gate B, canon consolidation, or playtest calibration.


## Core question

How does Astra track state movement across D00–D18 so that outcomes, costs, harm, discoveries, projects, faction actions, object changes, rewards, campaign-state changes, and source-local constructs flow to the right owner files without being dropped, duplicated, or resolved by the wrong file?

## Trigger–Owner–Payload–Receiver Matrix

Every cross-pack handoff must identify:

```text
trigger type
initiating owner file
payload type
receiver files
lawful receiver decisions
prohibited leakage
hidden-state boundary
relevant record shapes
blocked-handoff outcome
handoff status
```

The matrix tracks state movement. It is not a final state-transition schema.

## Trigger categories

D19 recognizes triggers including:

```text
resolution outcome
cost commitment
resource overdraw
breakthrough attempt
Technique expression
harm event
actor-state change
object/platform state change
world-state delta
scene transition
Project start / progress / completion
travel discovery
faction operation
opposition encounter
reward / loot / salvage event
time skip
season seam
source-local construct
donor mapping issue
mixed trigger
```

## Payload categories

Payloads may include:

```text
cost
resource state
harm pressure
condition pressure
advancement pressure
Technique / route expression pressure
actor-state change
object-state change
world-state delta
relationship-state change
law / faction / claim pressure
Project state
travel / discovery state
opposition / threat state
value / reward / salvage / custody state
campaign continuity state
source-local state
quarantine / escalation note
```

## Core handoff chains

### Chain 1 — Resolution-to-state

```text
D02 resolution outcome
  -> D03 cost / resource pressure
  -> D07 harm / condition / backlash if relevant
  -> D10 world-state if world changes
  -> D17 value if reward/cost/property changes
  -> D18 arc/continuity if campaign-relevant
```

Control: D02 identifies outcome state. Owner files define final state changes.

### Chain 2 — Power use / overdraw / backlash

```text
D06 Technique / route expression
  -> D03 resource cost / overdraw / instability
  -> D02 resolution if a check is required
  -> D07 backlash / harm / corruption / condition
  -> D10 world-state if visible or consequential
  -> D18 continuity if lasting
```

Control: power expression, resource cost, resolution, and harm remain separate owner layers.

### Chain 3 — Advancement / breakthrough

```text
D04 breakthrough / transformation
  -> D03 costs / catalysts / resource pressure
  -> D06 route / Technique / domain expression if relevant
  -> D07 backlash / scar / corruption / injury if relevant
  -> D08 actor identity / form-state if relevant
  -> D10 world-state if public or factionally meaningful
  -> D18 spacing / horizon / continuity
```

Control: D04 owns payload; D18 owns placement and continuity.

### Chain 4 — Project output

```text
D13 Project
  -> D05 method / competency if procedural expertise matters
  -> D09 object/material/platform state if created/repaired
  -> D17 value / cost / custody / reward / sink
  -> D10 world-state if public or environmental impact
  -> D15 institutional claim if faction/legal/domain involvement
  -> D18 continuity if long-horizon relevant
```

Control: D13 owns interval procedure; receiver files own final state.

### Chain 5 — Exploration / discovery

```text
D14 exploration / travel / discovery
  -> D10 map / location / hidden truth / world-state
  -> D16 hazard / opposition if encountered
  -> D17 access / acquisition / salvage / value if discovered
  -> D13 Project if study, repair, extraction, or mapping is needed
  -> D18 continuity if campaign-relevant
```

Control: discovery creates access to state; owner files resolve what the state means.

### Chain 6 — Faction / institution

```text
D15 faction / institution / law / domain operation
  -> D10 world-state / public belief / relationship / law record
  -> D17 debt / requisition / license / value / reward / claim
  -> D16 institutional opposition if encounter-facing
  -> D13 Project if long task, repair, training, construction, or negotiation is interval-scale
  -> D18 season / arc / horizon state if campaign-scale
```

Control: D15 owns institutional operation; D18 only classifies structural-time relevance.

### Chain 7 — Opposition / encounter

```text
D16 opposition / encounter / hazard
  -> D12 cadence if structured scene occurs
  -> D02 resolution if checks occur
  -> D07 harm / condition / corruption / exposure
  -> D08 actor/personhood if creature/NPC/substrate matters
  -> D09 object/platform state if platform/security/object threat
  -> D17 reward / loot / salvage / custody if value appears
  -> D10 world-state if consequence persists
  -> D18 recurrence / arc closure if campaign-relevant
```

Control: D16 constructs opposition pressure and hands off final effects.

### Chain 8 — Economy / value

```text
D17 value / acquisition / reward / inventory / requisition
  -> D09 object/material/platform state
  -> D10 market/world/law/public belief state
  -> D13 Project if extraction, repair, crafting, maintenance, or acquisition is interval-scale
  -> D15 claim, license, obligation, enforcement, requisition authority
  -> D18 continuity / archive / horizon if campaign-relevant
```

Control: D17 owns value-flow, not all consequences of value.

### Chain 9 — Structural time / time-skip

```text
D18 time skip / season seam / state aging
  -> D10 world-state aging
  -> D13 Project progress / interruption / completion
  -> D15 faction/domain operations
  -> D17 economy/value/debt/upkeep/scarcity changes
  -> D09 object/platform aging or maintenance need
  -> D07 persistent harm/recovery if relevant
  -> D16 recurring threat status
```

Control: D18 identifies affected state and required owner-file updates; owners resolve their own mechanics.

### Chain 10 — Source-local construct

```text
source-local donor construct
  -> identify owner files affected
  -> decide direct / normalized / source-local / quarantine / escalation
  -> record boundary
  -> prevent generalization
  -> route owner-file state
```

Control: source-local boundary and rejected-import notes are required.

## Blocked handoff outcomes

A blocked handoff must route to one lawful control outcome:

```text
source_local_retention
quarantine_pending_owner_file
escalation_required
deferred_to_schema_phase
deferred_to_runtime_phase
owner_patch_required
canon_review_required
no_action
```

## Acceptance criteria

D19-02 is accepted if it tracks actual state movement, not merely file references, and if every handoff identifies what moves, who receives it, what each receiver may decide, what must not leak, and what happens if the handoff is blocked.
