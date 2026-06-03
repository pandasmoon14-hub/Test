# D11-05 Unresolved Pressure Surfacing

## Purpose

This file defines how D11 surfaces D10 unresolved pressure queues and related D03–D09 consequence pressure without forcing every pressure into the next scene or forgetting it. D11 remains interface doctrine. D10 owns unresolved pressure records. D11 controls presentation and surfacing.

## Core rule

D11 should surface unresolved pressure when it is contextually relevant, visible or inferable, proximate, escalating, triggered by player action, or needed to preserve continuity. It should not force every active pressure into the next scene, and it should not leave future-facing consequences inert.

## Surfacing inputs

Pressure surfacing considers severity, scope, visibility, proximity, timing, trigger, owner substrate, player knowledge, fairness, and source-local boundary.

## Surfacing intensity

Intensity ranges from background signal to soft pressure, choice pressure, complication, direct confrontation, escalation event, and historical reminder. D11 should choose the minimum sufficient intensity that makes pressure matter without overforcing it.

## Pressure types

Legal pressure includes warrants, bounties, sanctions, exile, docking denial, contraband flags, personhood disputes, and salvage conflicts. It may surface as checkpoint tension, posted notice, clerk hesitation, docking refusal, guard recognition, summons, confiscation threat, or public accusation. A warrant does not automatically mean immediate arrest.

Faction pressure includes grudges, retaliation, alliance strain, debts, obligations, hidden infiltration, patron demand, and local faction clocks. Hidden factions surface through traces before identification.

Relationship pressure includes debt, favor, betrayal, resentment, kinship, loyalty, jealousy, and reconciliation opportunity. It presents social consequence and choice, not player emotion.

Economy/scarcity pressure includes shortage, rationing, market closure, embargo, black-market demand, requisition pressure, and supply-chain disruption. Scarcity appears as access, supply, social, or strategic pressure, not just price.

Hazard/corruption pressure includes corruption zones, plague, curse spread, disaster aftermath, unstable region, and local doom clocks. Hidden hazards require fairness support before severe consequence.

Object/claim pressure includes stolen relics, sacred claims, salvage disputes, platform impoundment, implant legality, object instability, and black-market interest. D11 must not invent object powers or ownership facts.

Information pressure includes rumors, false attribution, propaganda, suppressed records, leaked secrets, disputed accounts, witness memory, and altered maps. D11 does not certify false belief as truth.

## Surfacing triggers

Pressure may surface when the player enters affected territory, interacts with an involved faction, uses a contested object, seeks restricted goods, repeats a risky method, triggers a source-local clock, receives assessment signal, causes public knowledge change, or creates an opening.

## Dormant and historical pressure

Dormant pressure requires trigger before reactivation. Historical pressure may appear through memorials, records, ruins, myths, scars, legal precedent, or old grudge, but should not reactivate without cause.

## Pacing

When multiple pressures are active, prioritize by immediate relevance, location/proximity, severity, visibility, recent player action, unresolved queue age, thematic fit, source-local trigger, and contradiction risk. Do not dump all active pressures into every scene unless the scene is explicitly a convergence event.

## Record shape

```yaml
d11_pressure_surfacing_record:
  pressure_ref: string
  pressure_type: string
  source_records:
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  severity: string
  scope: string
  visibility: string
  surfacing_intensity: string
  surfacing_vector: string
  fairness_support: []
  player_facing_signal: string
  gm_facing_state_update: []
  escalation_conditions: []
  decay_conditions: []
  resolution_conditions: []
  agency_preserving_choices: []
```
