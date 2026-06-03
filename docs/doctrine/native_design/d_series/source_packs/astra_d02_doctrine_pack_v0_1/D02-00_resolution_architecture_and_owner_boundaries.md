# D02-00 Resolution Architecture and Owner Boundaries

## Purpose

This file defines D02’s role in Astra’s doctrine stack and locks the d20-first architecture.

## Core rule

Astra’s primary resolution model is:

```text
d20 + Resolution Modifier vs Difficulty Number
```

The d20 is the primary uncertainty engine for action checks, contested checks, defense/resistance checks, assessment, group checks, extended tasks, and source-local conversion unless a retained source-local subsystem is explicitly bounded.

## Why d20

Astra uses d20 because it supports:

- wide difficulty ladders;
- clear 5% probability increments;
- volatile but readable uncertainty;
- static opposition and active opposition;
- margin-based outcome bands;
- natural 20 and natural 1 handling;
- advantage/disadvantage;
- defense and resistance checks;
- group and extended tasks;
- conversion from many donor check systems.

D20 volatility is managed through Astra doctrine: no-roll rules, cost commitment, PCR pressure, bounded modifiers, advantage/disadvantage, assessment, partial outcomes, and owner-file delta routing.

## Not donor d20

D02 does not import any donor d20 assumptions by default.

Blocked imports include:

- proficiency progression;
- class-based bonus math;
- spell-slot assumptions;
- armor-class assumptions;
- hit-roll conventions;
- saving throw categories;
- advantage stacking rules from any donor game;
- critical hit damage rules;
- binary pass/fail defaults;
- donor action economy;
- donor bounded accuracy values;
- donor challenge-rating expectations.

D02 is Astra d20, not donor d20.

## What D02 owns

D02 owns:

- primary check procedure;
- Difficulty Number selection;
- margin-based outcome interpretation;
- natural 20 / natural 1 doctrine;
- cost commitment grammar;
- over-investment grammar;
- success-at-cost handling;
- opposed and contested check grammar;
- defense and resistance check grammar;
- group check grammar;
- extended and dramatic task grammar;
- assessment/reconnaissance resolution;
- state-delta routing to D03–D10;
- source-local resolution conversion boundaries.

## What D02 does not own

| Not owned by D02 | Owner |
|---|---|
| Attribute meanings | D01 |
| Power pools, fuel, charge, reserves, overdraw, resource behavior | D03 |
| Advancement gates, proof, tier progression, breakthroughs | D04 |
| Skills, methods, research, crafting procedure, investigation method | D05 |
| Routes, Techniques, Principles, oath mechanics, power expressions | D06 |
| Harm, injury, corruption, backlash, death, conditions | D07 |
| Actor body-state, form, kinform, companion, AI, personhood substrate | D08 |
| Object-state, relics, platforms, implants, tools, salvage objects | D09 |
| World-state, factions, law, economy, reputation, information-state | D10 |
| Live-play narration, scene framing, clue delivery, player-facing prose | D11 / later play adapter |

## Resolution sequence

A standard D02 resolution sequence is:

1. Confirm uncertainty and consequence justify a roll.
2. Identify intent.
3. Identify method.
4. Identify relevant owner-file states.
5. Establish known cost and risk.
6. Determine DN or opposition.
7. Apply PCR and situational pressure.
8. Declare optional over-investment.
9. Roll d20 and apply authorized modifier.
10. Compute margin.
11. Interpret outcome state.
12. Commit declared costs and consequence deltas.
13. Route records to owner files.

## No-roll principle

Do not roll when:

- there is no meaningful uncertainty;
- there is no meaningful consequence;
- failure would not matter;
- the character is clearly capable and time is not pressured;
- the action is background color;
- rolling would only create noise.

Roll when:

- consequence matters;
- opposition exists;
- cost is being risked;
- hidden state matters;
- time pressure exists;
- action can change owner-file state;
- source-local resolution requires it.

## Acceptance criteria

A D02 resolution ruling is valid when it:

1. uses d20-first procedure unless a lawful source-local exception applies;
2. preserves margin-based outcome states;
3. commits declared cost;
4. routes consequences to owner files;
5. respects PCR and context;
6. avoids donor d20 import.
