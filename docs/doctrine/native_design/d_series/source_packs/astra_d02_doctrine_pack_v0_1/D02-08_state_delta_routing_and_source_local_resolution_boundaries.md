# D02-08 State-Delta Routing and Source-local Resolution Boundaries

## Purpose

This file defines how D02 routes outcomes to owner files and handles donor resolution systems.

## Core rule

D02 owns resolution grammar. It does not own all consequences.

After every meaningful resolution, identify which owner files receive deltas.

## Delta routing matrix

| Delta family | Owner |
|---|---|
| resource, pool, charge, fuel, reserve, overdraw, instability | D03 |
| advancement, proof, threshold, breakthrough, transformation progress | D04 |
| skill, method, research, crafting discovery, competence, investigation method | D05 |
| route, Technique, Principle, feature, oath, domain expression | D06 |
| harm, injury, condition, curse, backlash, corruption injury, disaster | D07 |
| actor, body, form, kinform, companion, AI, spirit, clone, personhood substrate | D08 |
| object, relic, implant, platform, tool, material, salvage | D09 |
| world, territory, faction, law, economy, reputation, relationship, information-state | D10 |
| narration, scene presentation, player-facing summary | D11 / later runtime |
| retained donor-local result | Source-local boundary |

## Outcome-to-delta guidance

| Outcome | Likely delta behavior |
|---|---|
| Ascendant | declared cost, strong benefit, reduced consequence, improved state, extra progress. |
| Clear | declared cost, intended result, normal state update. |
| Fractured | declared cost plus partial success or extra cost/consequence. |
| Receded | partial cost, exposure, weak progress, information, positional loss, delayed pressure. |
| Sundered | full consequence, backlash, harm, object damage, world/faction escalation, false information, source-local rupture. |

## Health and Power Economy preservation

D02 does not replace health or Power Economy with pure narrative consequence.

Resolution may:

- spend D03 pools;
- threaten D03 overdraw;
- produce D07 injury or conditions;
- create D07 corruption/backlash;
- damage D09 objects;
- trigger D10 world-state pressure.

D02 should preserve pool and health relevance where owner files require it.

## Source-local resolution systems

Donor systems may include:

- roll-under;
- percentile;
- dice pools;
- step dice;
- success-count pools;
- narrative tag resolution;
- fixed target numbers;
- proprietary subsystems;
- specialty dice;
- metacurrency-driven resolution.

D02 lawful outcomes:

| Outcome | Meaning |
|---|---|
| Direct d20 mapping | Donor check maps cleanly into d20 + modifier vs DN. |
| Normalized d20 margin mapping | Donor degrees/successes map into Astra five-state margin ladder. |
| Source-local retained resolution | Donor subsystem remains bounded to its source/campaign context. |
| Quarantined construct | Unsafe or underspecified until later doctrine. |
| Escalated doctrine problem | Repeated pressure reveals missing Astra framework. |

## Conversion mapping examples

### Percentile skill

A donor percentile skill may normalize to:
- D05 method competence;
- d20 modifier or DN adjustment;
- source-local retained percentile if exact probability matters.

Do not import percentile math as Astra default.

### Dice pool successes

A donor dice pool may normalize to:
- d20 modifier;
- advantage/disadvantage;
- progress units;
- outcome band;
- source-local retained pool if subsystem depends on success allocation.

### Step dice

Step dice may normalize to:
- tiered modifier;
- source-local retained subsystem;
- D03/D09 resource die only if later doctrine authorizes.

Step dice are not D02’s primary resolution model.

### Metacurrency

Metacurrency-driven donor systems do not import as Astra default. They may map to D03 resources, source-local retention, or quarantine.

## Source-local boundary record

Retained source-local resolution needs:

```yaml
source_local_resolution_boundary:
  source_ref: string
  donor_resolution_label: string
  retained_rule: string
  allowed_scope: string
  prohibited_generalizations: []
  normalized_outputs: []
  owner_handoffs: []
  promotion_requirements: []
```

## Acceptance criteria

A routing/conversion ruling is valid when it:

1. identifies owner-file deltas;
2. preserves D03/D07 pool and harm relevance;
3. maps donor systems by function;
4. blocks donor resolution from becoming Astra default;
5. uses quarantine/escalation when missing doctrine appears.
