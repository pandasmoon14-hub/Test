# D11-01 Scene Framing from Registered State

## Purpose

This file defines how D11 builds scene frames from registered state without inventing unsupported persistent facts. D11 remains interface doctrine. It frames scenes from D00–D10 state; it does not create full world simulation, encounter generation, faction AI, or final live-play behavior.

## Core rule

A D11 scene frame must be grounded in known or lawfully provisional state. The narrator may add sensory color, pacing, and framing, but may not create persistent facts, hidden truths, mechanical costs, object powers, faction actions, legal consequences, or world-state changes unless supported by D00–D10 records or explicitly marked provisional.

## Scene-frame inputs

A scene frame may draw from D00 core play purpose, D01 attribute signals, D02 resolution posture, D03 active resources, D04 advancement pressure, D05 method/research posture, D06 route/Technique context, D07 harm/hazard state, D08 actor/form state, D09 object/platform state, D10 location/faction/law/economy/reputation/information/unresolved pressure, and source-local boundaries.

## Scene frame structure

A useful scene frame identifies where the scene is happening, what is immediately perceivable, what pressure is active, what the player knows, what remains uncertain, what options appear available, and what hidden backend state must not be revealed.

## Scene purpose

D11 should identify scene purpose before framing. Purposes include orientation, choice point, consequence surfacing, assessment opportunity, conflict setup, recovery/downtime, discovery, transition, and source-local procedure. Scene purpose prevents pressure overload and scene drift.

## Visibility layers

Player-visible state can be stated directly. Player-inferable state can be hinted or framed as uncertainty. Hidden backend state must not be revealed unless lawfully discovered.

Examples of hidden backend state include hidden faction controller, concealed culprit, hidden object power, false-rumor origin, suppressed-record cause, and exact hidden Pneuma/cosmic modifier.

## Low-impact color

Low-impact color is allowed when it does not create persistent state. Rain on metal, distant crowd noise, worn stone, lantern shadows, ordinary clutter, background travelers, dust, smoke, weather, and texture are allowed. Named faction symbols, law notices, relic sigils with mechanics, new map routes, prophecy marks, market shortages, and public accusations are not low-impact color.

## Provisional detail

Provisional details may be used for scene flow when low-risk, non-contradictory, mechanically non-defining, not hidden-truth-bearing, and promotable. Examples include unnamed guards, ordinary shopkeepers, passersby, minor witnesses, routine clerks, ordinary doors, and generic furniture. If consequential, route to the relevant owner: D08 for recurring actors, D09 for objects, D10 for faction/law/location/rumor/relationship, D07 for hazards, D05 for methods, and D06 for routes/Techniques.

## Missing-state escalation

Escalate rather than invent when framing requires new faction doctrine, law/economy/world-state, object power, Technique behavior, actor substrate, harm/corruption rule, major map/territory creation, hidden truth not present in records, or unbounded source-local conversion.

## Player agency

D11 may present pressure and options. It must not decide the player’s response, intent, emotion, loyalty, belief, or action.

## Record shape

```yaml
d11_scene_frame:
  scene_ref: string
  scene_purpose: string
  grounded_inputs:
    D00: []
    D01: []
    D02: []
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  player_visible_state: []
  player_inferable_state: []
  hidden_backend_state_not_to_reveal: []
  unresolved_pressures_to_surface: []
  low_impact_color_allowed: []
  provisional_details: []
  available_choices: []
  escalation_flags: []
```
