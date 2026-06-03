# D00-03 State-Delta Commit Protocol

## Purpose

This file defines the rule that meaningful actions commit tracked deltas. It is the bridge from play action to system memory.

## Core rule

Every meaningful action commits at least one delta to a recognized state owner.

A delta is a recorded change that persists long enough to matter to future play, doctrine, conversion, or runtime state.

## Delta families

| Delta family | Owner |
|---|---|
| Resource, pool, charge, fuel, instability, corruption load | D03 |
| Advancement, proof, threshold, breakthrough, transformation progress | D04 |
| Skill, method, research, crafting discovery, competence record | D05 |
| Route, Technique, Principle, feature, oath, domain expression | D06 |
| Harm, injury, condition, curse, backlash, disaster, corruption injury | D07 |
| Actor, form, body, companion, AI, personhood, identity continuity | D08 |
| Object, relic, implant, platform, material, salvage, source-local object | D09 |
| World, faction, law, economy, reputation, information, territory | D10 |
| Scene presentation, narration, player-facing summary | D11 / later runtime |

D00 owns the requirement to commit deltas. It does not own all delta formats.

## Delta commitment timing

A delta may commit:

- before the roll/action as declared cost;
- during resolution as resource spend or exposure;
- after resolution as consequence;
- later as delayed or hidden consequence;
- when discovered as information-state;
- when promoted from trivial event to persistent consequence.

## Declared cost and emergent consequence

D00 distinguishes:

- declared cost: cost accepted before commitment;
- emergent consequence: result of outcome, failure, partial success, overreach, environment, opposition, or hidden context;
- delayed consequence: consequence recorded now but surfaced later;
- hidden consequence: consequence not yet known to player-facing view;
- historical consequence: no longer active but retained to prevent contradiction.

D02 owns outcome-specific handling.

## State-delta minimum

At least one of the following must change for a meaningful action:

- resource/pool/instability state;
- character condition/injury/threshold state;
- object/platform/material state;
- relationship/reputation/faction state;
- territory/location/hazard/law/economy/information state;
- source-local state.

## Avoiding false deltas

Not all description is a delta. A delta should be tracked when it can affect later play.

Examples of false deltas:

- flavor-only dust;
- one-line NPC mood with no future effect;
- routine purchase of common supplies;
- travel description with no persistent hazard, cost, route, or information change;
- ordinary background weather.

## Acceptance criteria

A state-delta ruling is valid when it:

1. identifies the owner file;
2. records declared costs separately from consequences;
3. permits delayed and hidden consequences;
4. avoids turning every description into permanent state;
5. preserves significant consequences for D10 or another owner.
