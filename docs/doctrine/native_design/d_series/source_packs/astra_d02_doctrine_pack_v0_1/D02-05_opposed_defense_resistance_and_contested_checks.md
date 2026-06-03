# D02-05 Opposed, Defense, Resistance, and Contested Checks

## Purpose

This file defines how D02 handles active opposition, static opposition, defense, and resistance.

## Static opposition

Use static opposition when speed, simplicity, or passive resistance is appropriate.

```text
d20 + actor modifier vs Defense / Difficulty Number
```

Examples:

- attack against static defense;
- stealth against passive awareness;
- hacking against system security;
- persuasion against established resistance;
- ritual pressure against ward threshold;
- route action against environmental barrier.

Static defense values must be defined by owner files or source-local boundary. D02 does not invent armor, defense, or resistance math.

## Active contested checks

Use active contested checks when both sides meaningfully oppose.

```text
Actor A: d20 + modifier
Actor B: d20 + modifier
Higher total wins.
Margin = Winner Total - Loser Total
```

Recommended contested margin:

| Margin | Result |
|---:|---|
| 10+ | Decisive / Ascendant-equivalent win |
| 1–9 | Clear win |
| 0 | Clash, tie, stall, mutual cost, defender holds, or Fractured progress depending context |
| -1 to -9 | Opponent Clear win |
| -10 or lower | Opponent decisive / Ascendant-equivalent win |

## Tie handling

Ties should be resolved by action type.

Possible tie outcomes:

- status quo holds;
- both gain partial progress;
- both pay cost;
- active side gains Fractured progress;
- defender holds if defense-dominant;
- higher relevant attribute breaks tie;
- source-local rule applies.

D02 should not make “defender always wins” the universal rule.

## Defense checks

Defense checks are reactive attempts to avoid, block, parry, deflect, dodge, resist, shield, or reposition against a hostile action.

Formula:

```text
d20 + relevant defense modifier vs attacker total or effect DN
```

Defense checks can use the full outcome ladder.

Example:

| Outcome | Defense result |
|---|---|
| Ascendant | avoid effect and gain position/info/counter-pressure. |
| Clear | avoid or reduce effect cleanly. |
| Fractured | partial mitigation with cost or position loss. |
| Receded | effect applies with limited mitigation or warning. |
| Sundered | full effect plus added consequence. |

## Resistance checks

Resistance checks are reactive attempts to withstand or reduce effects.

Threat examples:

| Threat | Likely owner |
|---|---|
| physical harm | D07 |
| poison, disease, biological hazard | D07 |
| corruption, curse, backlash | D07/D08 |
| mental pressure, fear, morale, social shock | D05/D07/D10 |
| route/Technique effect | D06/D07 |
| object/platform hazard | D09/D07 |
| law/social enforcement pressure | D10 |
| source-local threat | Source-local |

Resistance should usually be graduated, not binary.

## Attack and damage boundary

D02 may define that an attack roll resolves accuracy or contested action, but D07 owns harm and damage consequences. D02 does not define final damage dice, hit point loss, injury tables, death, armor, or damage family behavior.

## Social contests

Social contests may use d20 opposition, but D02 does not own social method or reputation consequences.

D05 owns social method/skill. D10 owns reputation, relationship, law, faction, and information consequences.

## Multi-part contests

Complex contests may involve:

- initial approach;
- opposed check;
- defense/resistance response;
- consequence routing;
- extended task conversion if not resolved in one exchange.

Do not multiply rolls unnecessarily when one roll can carry the consequence.

## Acceptance criteria

An opposition ruling is valid when it:

1. distinguishes static and active opposition;
2. uses margin to interpret outcome;
3. supports non-binary defense/resistance;
4. routes harm to D07;
5. routes social/world consequence to D10;
6. avoids donor combat import.
