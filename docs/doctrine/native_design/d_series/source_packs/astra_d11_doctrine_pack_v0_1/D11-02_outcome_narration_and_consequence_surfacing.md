# D11-02 Outcome Narration and Consequence Surfacing

## Purpose

This file defines how D11 presents D02 outcomes and D03–D10 deltas without collapsing them into generic success/failure or raw register dumps. D11 remains interface doctrine and does not own D02 resolution math, D03 costs, D07 harm, D09 object-state, or D10 world-state.

## Core rule

D11 must present outcomes in a way that reflects the D02 result, shows declared costs and visible consequences, preserves player agency, hides backend-only information unless lawfully revealed, and records or signals owner-file deltas without turning narration into a raw register dump.

## Outcome ladder

| D02 outcome | Margin guide | D11 presentation |
|---|---:|---|
| Ascendant | +10 or higher | Exceptional control, added benefit, improved position, reduced fallout if lawful. |
| Clear | 0 to +9 | Intended result succeeds; declared cost commits. |
| Fractured | -1 to -4 | Success/progress with cost, flaw, exposure, complication, or extra delta. |
| Receded | -5 to -9 | Goal fails or recedes, but information, exposure, cost, weak progress, or position change occurs. |
| Sundered | -10 or lower | Severe failure or rupture with proportional consequence and owner-file routing. |

## Outcome principles

Ascendant should feel like strong control, not arbitrary overkill. It does not bypass impossible gates, invent unrelated benefits, create new powers, erase declared cost automatically, or solve unrelated problems.

Clear presents the intended result and ordinary footprint. It is not bland; it is competence expressed cleanly.

Fractured is success or progress with cost. It must not be narrated as pure failure.

Receded is failure or retreat from the goal, but something still changes: information, exposure, partial cost, lost position, weak progress, revealed risk, or delayed pressure. It must not default to “nothing happens” if the roll was meaningful.

Sundered is severe failure or rupture. It must remain proportional to declared stakes, visible risk, PCR pressure, source-local context, and owner-file doctrine.

## Cost and consequence separation

D11 separates declared cost, over-investment cost, outcome consequence, hidden consequence, delayed consequence, and historical consequence. Declared cost should not be framed as surprise punishment.

## Consequence visibility

Visible consequences may be narrated directly. Hidden/backend consequences remain GM-facing unless lawfully revealed. Hidden consequences may surface as omens, symptoms, subtle reactions, ambiguous marks, strange absences, tone changes, or incomplete clues, but not as direct hidden facts.

## Delta presentation by owner

D03 appears as resource spend, strain, fuel loss, instability, or overdraw symptoms. D04 appears as threshold pressure, proof gained/lost, breakthrough instability, or blocked progress. D05 appears as method progress, research clue, crafting step, or expertise limit. D06 appears as Technique effect, Route strain, Principle resonance, or oath pressure. D07 appears as harm, injury, corruption, backlash, or condition. D08 appears as form-state stress, companion reaction, AI/personhood signal, or body issue. D09 appears as object wear, relic reaction, platform damage, implant strain, or salvage quality. D10 appears as law pressure, faction memory, rumor, reputation, territory change, scarcity, or information-state.

Raw owner deltas belong in GM-facing or state-audit mode.

## Follow-up choices

D11 may present follow-up choices when doctrine supports them: accept cost, push, retreat, stabilize, spend, reveal, conceal, sacrifice object durability, call in a favor, or contest a claim. D11 must not choose for the player.

## Record shape

```yaml
d11_outcome_presentation_record:
  source_resolution_ref: string
  d02_outcome: string
  declared_costs_to_present: []
  visible_consequences_to_present: []
  hidden_backend_consequences_not_to_reveal: []
  delayed_consequences: []
  owner_deltas:
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  unresolved_pressures_created_or_updated: []
  follow_up_choices: []
  escalation_flags: []
  gm_facing_summary: []
  player_facing_summary: string
```
