# D02-01 D20 Action Check, Difficulty, and Modifiers

## Purpose

This file defines the standard d20 action check, Difficulty Number ladder, modifier sources, advantage/disadvantage, and bounded modifier guidance.

## Standard check

```text
d20 + Resolution Modifier vs Difficulty Number
```

If the final total is equal to or greater than the Difficulty Number, the action at least reaches Clear unless a natural 1 complication, source-local rule, or impossibility gate applies.

Outcome quality is determined by margin.

```text
Margin = Final Check Total - Difficulty Number
```

## Difficulty Number ladder

| DN | Descriptor | Use |
|---:|---|---|
| 5 | Trivial under pressure | Usually no roll unless pressure, secrecy, harm, opposition, or consequence exists. |
| 8 | Easy | Basic task under mild pressure. |
| 12 | Standard | Typical meaningful task. |
| 16 | Hard | Requires competence, favorable method, or resource investment. |
| 20 | Severe | High-risk, expert, hostile, dangerous, or heavily opposed. |
| 24 | Apex | Beyond ordinary competence; requires strong setup, route, resource, or favorable context. |
| 28 | Transcendent | Supernormal or high-tier action under major pressure. |
| 32+ | Mythic / Cosmic / Source-local Extreme | Requires exceptional route, resource, transformation, context, or source-local authorization. |

These are doctrine bands, not universal physics. Some actions are impossible until a necessary fictional, doctrinal, object, route, actor, or world-state condition is present.

## Modifier source rule

A modifier must come from an authorized owner-file source.

| Modifier source | Owner |
|---|---|
| Attribute contribution | D01 |
| Skill, method, training, research, tool operation | D05 |
| Power/resource investment, fuel, overdraw, charges | D03 |
| Advancement/tier/proof relevance | D04 |
| Route, Technique, Principle, oath, domain expression | D06 |
| Injury, condition, corruption, backlash pressure | D07 |
| Form-state, body, companion, AI, kinform, actor substrate | D08 |
| Tool, relic, platform, implant, material, object quality | D09 |
| Faction, law, territory, economy, reputation, information-state | D10 |
| Source-local resolution modifier | Source-local boundary |

D02 may define how modifiers are applied but should not invent their source.

## Bounded modifier guidance

Recommended modifier scale:

| Modifier | Meaning |
|---:|---|
| ±2 | Minor but meaningful factor. |
| ±5 | Major factor, strong setup, serious injury, strong tool, significant hazard. |
| ±10 | Extreme factor, usually a tier-scale shift or specialized condition. |

Avoid uncontrolled stacking. If many factors accumulate, consider DN shift, advantage/disadvantage, consequence severity, or source-local boundary instead of arithmetic pileup.

## Advantage and disadvantage

Advantage and disadvantage are context-compression tools.

```text
Advantage: roll 2d20 and keep the higher.
Disadvantage: roll 2d20 and keep the lower.
```

Use advantage for a dominant favorable condition. Use disadvantage for a dominant adverse condition.

Rules:

- advantage and disadvantage cancel;
- do not stack ordinary advantage into three or more d20s by default;
- multiple minor factors should usually become modifiers or DN shifts;
- severe layered pressure should usually raise DN, increase cost, worsen consequence severity, or require owner-file validation;
- source-local systems may retain different procedures under boundary.

## Difficulty vs modifier

Use DN changes when task/environment/opposition itself is harder.

Use modifiers when the actor, method, tool, condition, or preparation changes performance.

Use advantage/disadvantage when a major situational factor changes uncertainty without changing maximum possible result.

Use consequence severity when the action remains possible but failure or partial success is more dangerous.

## Impossibility gates

Do not use high DN as the only way to express impossibility.

An action may require:

- route access;
- correct tool;
- correct scale;
- domain compatibility;
- legal/permission state;
- object interface;
- actor form-state;
- source-local condition;
- prior research/discovery;
- advancement threshold.

A natural 20 can reveal a path through an impossibility gate, but it does not automatically break the gate.

## Acceptance criteria

A difficulty/modifier ruling is valid when it:

1. uses the d20 DN ladder;
2. identifies owner-file modifier sources;
3. avoids donor math import;
4. keeps modifiers bounded;
5. distinguishes DN, modifier, advantage/disadvantage, and consequence severity;
6. protects impossibility gates.
