# Astra Ascension — D03-08 Runtime and UI State Requirements

Status: design-draft / runtime and UI handoff  
Layer: Native Design Phase / D03  
File ID: D03-08  
Version: v0.1  
Date: 2026-05-29

---

## 1. Purpose

This file collects runtime and UI state requirements created by the D03 doctrine pack.

It is not implementation code. It is a bridge so future runtime/schema work can support D03 without collapsing doctrine, UI, runtime state, and narration.

---

## 2. Runtime principle

The backend owns truth.

D03 state must be tracked in structured records, not inferred from narration.

The model may explain, summarize, narrate, and ask questions, but it must not secretly mutate resource pools, reservoir partitions, Expression ledgers, slot conditions, overdraw, corruption, or recovery states without backend validation.

---

## 3. Required actor state groups

Astra runtime should eventually track:

| State group | Contents |
|---|---|
| Baseline embodiment | Health/Vital State reference, Endura state, fatigue/overexertion hooks. |
| Power Economy access | Accessed, studied, temporary, external, integrated, fused, overlimit economies. |
| Vessel economy tolerance | Current stable economy capacity, integrated economy count, overlimit pressure. |
| Power Reservoir | Total capacity, partition values, recovery state, partition conditions. |
| Economy roles | Dominant, Secondary, Tertiary, external, overlimit. |
| Expression Ledger | Known, theorized, learned, retained, inscribed, refined, mastered, lost Expressions. |
| Expression carriers | Vessel, Animus, Cognitive, Economy, Scrypta, Relic, Tool/Tech, Domain, Companion/Platform, External Anchor. |
| Carrier tolerance | Tolerance rating, current burden, capacity state. |
| Slot conditions | Stable, strained, damaged, transformative condition counts/records. |
| Overdraw and instability | Current overdraw events, instability load, overlimit effects. |
| Backlash/corruption | Triggered events, Vitia/corruption states, scars, contamination. |
| Recovery hooks | Current recovery permissions, cooldowns, scene/rest/domain/action recovery state. |
| Expression projects | Desired outcomes, theories, research vectors, unsafe attempts, prototypes. |

---

## 4. Suggested actor D03 schema sketch

```yaml
actor_d03_state:
  actor_id: string
  baseline:
    has_physical_vessel: boolean
    health_state_ref: string
    endura:
      current: integer | band
      max: integer | band
      fatigue_state: string | null
  power_economies:
    integrated:
      - economy_id: string
        role: dominant | secondary | tertiary | overlimit
        access_state: integrated | overlimit | dormant | degraded
    external_access:
      - economy_id: string
        source_ref: string
        access_duration: string
        counts_against_limit: boolean
    vessel_tolerance:
      stable_limit: integer
      integrated_count: integer
      overlimit_state: none | pressured | unstable | fracturing | collapsed
  reservoir:
    exists: boolean
    total_capacity: integer | band | formula_ref
    partitions:
      - economy_id: string
        role: dominant | secondary | tertiary | external | overlimit
        current: integer | band
        max: integer | band
        condition: stable | strained | leaking | burned | sealed | corrupted | other
    partition_shift_permission:
      allowed_now: boolean
      required_procedure: string | null
  expression_profile_ref: string
  instability:
    current: integer | band
    sources: [string]
  corruption:
    current_states: [string]
    vitia_tags: [string]
  recovery:
    active_recovery_modes: [string]
    blocked_recovery_modes: [string]
```

---

## 5. Expression Ledger state

Known Expressions and Inscribed Expressions must be separate.

```yaml
actor_expression_ledger:
  actor_id: string
  known_expressions:
    - expression_id: string
      display_name: string
      knowledge_state: known_of | observed | understood | theorized | studied | copied | learned | retained | inscribed | functional | refined | mastered | lost
      current_legality: valid | overreach | prototype | unstable | unanchored | uncontained | restricted | invalid
      expression_grade: integer
      origin_type: canon | converted | player_created | source_local | experimental
      project_ref: string | null
  inscribed_expressions:
    - expression_id: string
      carrier_ref: string
      burden_rating: integer | band | formula_ref
      inscription_condition: string
      retention_state: theoretical | prototype | experimental | unstable | functional | refined | integrated | mastered | restricted | rejected
      economy_routes: [string]
      lawful_routes: [string]
      replacement_count: integer
      degradation_risk: none | low | medium | high
```

---

## 6. UI requirements

The intended Astra UI can support deep state through tabs/pages.

Recommended UI areas:

| UI area | Purpose |
|---|---|
| Known Expressions | Observed, theorized, studied, copied, learned, lost, mastered Expressions. |
| Inscribed Expressions | Currently retained Expressions with carrier, burden, legality, and condition. |
| Expression Projects | Desired outcomes, theories, research, experiments, re-authoring attempts. |
| Expression Summary Cards | Compact player-facing expression references. |
| Carriers & Slots | Vessel, Animus, Cognitive, Economy, Scrypta, Relic, Domain, External, etc. |
| Slot Condition | Healthy, strained, degraded, scarred, externalized, transformed, etc. |
| Power Economies | Integrated/accessed economies and availability. |
| Reservoir | Total, partitions, recovery, overdraw, overlimit pressure. |
| Costs & Recovery | Current cost channels, recovery options, blocked recovery states. |
| Hidden/Backend Notes | Pneuma, hidden cosmic modifiers, sealed fields, GM/runtime-only constraints. |

Known Expressions and Inscribed Expressions should not be collapsed.

---

## 7. Expression Summary Card format

A player-facing Expression Summary Card should be compact but Astra-native.

```text
Expression Name — [Family; Grade; Route; Status]
Use: [what it does in plain language]
Route: [Power Economy route and lawful method]
Scope: [range / area / target / duration / control]
Cost: [partition cost, Endura, strain, reserve, risk, or external cost]
Risk: [main backlash, instability, failure, trace, or consequence]
Flags: [key effect flags]
Retention: [slot/carrier and inscription condition]
Current legality: [valid / overreach / prototype / unstable / restricted / invalid]
```

The card summarizes. It is not the full backend record.

---

## 8. Example summary: Earthen Wisp

```text
Earthen Wisp — [Material Control; Grade 1; Mistra; Experimental]
Use: Shape and guide a one-foot sphere of loose earth or similar material within close range.
Route: Mistra shaping through earth-domain familiarity; requires active control.
Scope: Close range, one small material mass, sustained while maintained, direct control.
Cost: Minor Mistra partition spend; sustain cost if held across pressure.
Risk: On poor outcomes, the sphere may scatter, deform, expose your position, or strain the inscription.
Flags: material_control, sustained, earth, close_control.
Retention: Internal Expression slot, healthy, prototype inscription.
Current legality: Valid as a low-grade experimental Expression.
```

---

## 9. Example summary: Wisp of Steel

```text
Wisp of Steel — [Material Control / Densification; Grade 2–3; Mistra + Pressa; Unstable]
Use: Condense and guide an earthen or mineral sphere into a steel-like mobile mass with suppressive weight.
Route: Mistra provides shaping; Pressa provides density, pressure, and cohesion.
Scope: Close range, one small object-scale construct, sustained, guided control.
Cost: Split Mistra and Pressa partition cost; higher sustain burden than Earthen Wisp.
Risk: Pressure recoil, control loss, partition strain, or localized distortion on poor outcomes.
Flags: material_control, densifying, steel_like, suppressive_weight, sustained.
Retention: Internal slot, strained until stabilized through training.
Current legality: Valid if actor has Pressa access and sufficient training; otherwise prototype or overreach.
```

---

## 10. Valid action vector output

When a player declares an action and a lawful route exists, the system should produce a concise action framing, not just "roll."

Example:

```text
You have a lawful route.
Expression: Earthen Wisp
Action Vector: Mistra-shaped material control through earth familiarity.
Roll Basis: Reason or Insight depending on whether you are calculating structure or sensing material response.
Scope: Close, one-foot sphere, sustained direct control.
Cost: Minor Mistra partition spend; optional overcommit may improve control or stability.
Risk: On Mixed or worse, the sphere may scatter, deform, expose your position, or strain the inscription.
Roll Posture: Favorable with loose natural earth; adverse with refined, warded, living, or hostile material.
```

---

## 11. No-route output

When a desired supernatural outcome lacks lawful route, the system should not offer a roll.

Example:

```text
You do not yet have a lawful route.
The desired outcome can be recorded as a theory, research vector, or training goal. To attempt it as an Expression, you would need a route such as sound affinity, command authority, Volith pressure, Pressa suppression, Phasma name-binding, Scrypta speech-inscription, a relic, an entity contract, or a prior condition on the target.
```

Narrative equivalent:

```text
The idea has shape, but not a path. Your voice can carry intent, threat, rhythm, and fear; it cannot yet carry law. This can become a study vector, but it is not a valid Expression attempt as you are now.
```

---

## 12. Runtime boundaries

The runtime must own:

- current D03 state;
- resource values;
- reservoir partitions;
- Expression ledger;
- carrier and slot conditions;
- lawful route validation;
- cost payment;
- overdraw/overlimit;
- recovery state;
- event commits.

The model may not secretly grant Expressions, modify slots, alter reservoir partitions, erase corruption, or create lawful routes without backend validation.

---

## 13. Conversion implications

D03 records should support both converted and player-created content.

Converted donor abilities should become Expression records, not unstructured prose.

Player-created content should use the same schema and validation route.

No separate “homebrew exception” should bypass D03.
