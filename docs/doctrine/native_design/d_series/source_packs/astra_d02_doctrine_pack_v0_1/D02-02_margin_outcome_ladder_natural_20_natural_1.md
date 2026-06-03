# D02-02 Margin Outcome Ladder, Natural 20, and Natural 1

## Purpose

This file defines D02’s five outcome states, margin bands, and natural d20 handling.

## Margin calculation

```text
Margin = Final Check Total - Difficulty Number
```

For opposed checks:

```text
Margin = Winner Total - Loser Total
```

## Five outcome states

| Margin | Outcome | Meaning |
|---:|---|---|
| +10 or higher | Ascendant | Goal achieved with exceptional control, added benefit, reduced consequence, superior positioning, or high-quality result. |
| 0 to +9 | Clear | Goal achieved; declared cost commits; normal consequence footprint if relevant. |
| -1 to -4 | Fractured | Partial success, success at cost, compromised result, goal achieved with added delta, or useful progress with complication. |
| -5 to -9 | Receded | Goal not achieved or only minimal progress; partial cost, exposure, positional loss, or information may occur. |
| -10 or lower | Sundered | Severe failure, backlash, harm, false read, escalation, major cost, or serious consequence. |

## Outcome doctrine

Astra should avoid “nothing happens” as the default result of a meaningful roll.

Even Receded or Sundered should usually produce at least one of:

- information;
- cost;
- exposure;
- position change;
- owner-file delta;
- hidden consequence;
- future pressure;
- source-local result.

## Ascendant

Ascendant may provide:

- additional benefit;
- clean completion;
- cost mitigation;
- improved quality;
- information rider;
- positional advantage;
- reduced fallout;
- progress multiplier;
- stronger object/world-state result.

Ascendant does not erase declared cost unless a rule or consequence explicitly allows it.

## Clear

Clear means the action works as intended. It may still create ordinary footprint or declared cost.

Examples:
- resource is spent;
- object is used;
- witness sees the act;
- time passes;
- normal risk remains.

## Fractured

Fractured is Astra’s main mixed-result state.

It may mean:

- success with extra cost;
- partial completion;
- compromised success;
- success with exposure;
- success with object wear;
- success with faction/legal/reputation consequence;
- progress but not completion;
- correct information but incomplete or costly.

## Receded

Receded means the action fails or retreats from goal-state, but the roll should still matter.

It may produce:

- limited information;
- partial cost;
- worsening position;
- lost opportunity;
- exposure;
- weak progress;
- delayed pressure;
- source-local consequence.

## Sundered

Sundered is severe failure or rupture.

It may produce:

- full consequence;
- backlash;
- harm;
- corruption;
- object damage;
- faction escalation;
- false or dangerously incomplete assessment;
- legal exposure;
- route strain;
- major resource loss;
- serious state-delta.

Sundered does not require punitive excess. Consequence should be proportional to stakes and owner-file doctrine.

## Natural 20

A natural 20 creates a critical opportunity.

If the action is possible, a natural 20 may:

- upgrade outcome by one step;
- add an Ascendant rider if already successful;
- reduce consequence severity;
- reveal extra information;
- improve position;
- prevent total failure when the final total is still low;
- create a source-local exceptional result if bounded.

A natural 20 does not automatically bypass:

- missing requirements;
- impossible scale;
- absent target;
- absent tool;
- invalid method;
- doctrine gate;
- route lock;
- actor-state impossibility;
- object incompatibility;
- source-local hard prohibition.

If the action is impossible, a natural 20 may reveal what would make it possible.

## Natural 1

A natural 1 creates a complication flag.

It may:

- prevent Ascendant outcome;
- add cost, exposure, instability, or misread risk;
- downgrade result by one step when context supports it;
- trigger owner-file complication;
- create D10 consequence if witnessed, illegal, public, or reputation-relevant.

A natural 1 is not automatic failure in all cases. If the total still clearly succeeds, the result may become Clear with complication or Fractured success.

## Critical boundaries

Critical outcomes should be exciting but not campaign-breaking or arbitrary.

D02 blocks:

- automatic impossible success on natural 20;
- automatic expert incompetence on natural 1;
- critical tables imported from donors as default;
- critical damage rules imported as default;
- critical failures that bypass proportionality.

## Acceptance criteria

A margin ruling is valid when it:

1. computes outcome by margin;
2. preserves the five Astra states;
3. avoids binary pass/fail default;
4. treats natural 20 as opportunity;
5. treats natural 1 as complication flag;
6. routes consequences to owner files.
