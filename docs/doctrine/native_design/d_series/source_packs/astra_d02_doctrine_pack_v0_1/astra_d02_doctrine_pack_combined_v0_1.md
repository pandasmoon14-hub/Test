# D02 D20 Resolution Doctrine Pack v0.1

Generated: 2026-06-02

This combined export contains the full D02 doctrine pack in file order.


---

<!-- FILE: D02-README_manifest.md -->

# D02 D20 Resolution, Cost Commitment, PCR Difficulty, Assessment, and Delta Routing Doctrine — Manifest

Version: v0.1  
Phase: Astra Ascension native design doctrine  
Status: Doctrine pack generated from locked d20-first D02 architecture  
Primary owner: D02

## Purpose

D02 defines Astra’s primary resolution architecture. It replaces the earlier recovered 2d6 model with a d20-first model that can support Astra’s larger scope: partial outcomes, cost commitment, PCR-derived difficulty, contested checks, defense/resistance checks, group action, extended tasks, assessment/reconnaissance, and D03–D10 delta routing.

D02 is not an imported donor d20 system. It does not import donor proficiency, class math, action economy, armor conventions, spell assumptions, saving throw categories, or binary pass/fail behavior.

## Core resolution expression

```text
d20 + Resolution Modifier vs Difficulty Number
```

Where:

- `d20` is Astra’s primary uncertainty die.
- `Resolution Modifier` is assembled only from authorized owner-file sources.
- `Difficulty Number` is set through task pressure, PCR context, opposition, source-local boundary, or owner-file state.
- Outcome is interpreted through Astra’s margin-based five-state ladder.

## Five outcome states

| Outcome | Margin guide | Meaning |
|---|---:|---|
| Ascendant | +10 or higher | Exceptional success, strong control, added benefit, reduced consequence, or superior positioning. |
| Clear | 0 to +9 | Goal achieved; declared cost commits; normal consequence footprint if relevant. |
| Fractured | -1 to -4 | Partial success, success at cost, compromised success, or extra delta. |
| Receded | -5 to -9 | Goal not achieved or minimal progress; partial cost, exposure, information, or position shift may occur. |
| Sundered | -10 or lower | Severe failure, backlash, harm, false read, escalation, or serious consequence. |

## File order

1. `D02-00_resolution_architecture_and_owner_boundaries.md`
2. `D02-01_d20_action_check_difficulty_and_modifiers.md`
3. `D02-02_margin_outcome_ladder_natural_20_natural_1.md`
4. `D02-03_cost_commitment_overinvestment_and_success_at_cost.md`
5. `D02-04_power_context_register_resolution_integration.md`
6. `D02-05_opposed_defense_resistance_and_contested_checks.md`
7. `D02-06_group_extended_and_dramatic_tasks.md`
8. `D02-07_assessment_reconnaissance_and_information_quality.md`
9. `D02-08_state_delta_routing_and_source_local_resolution_boundaries.md`
10. `D02-09_integration_checklists_and_ddr_register.md`
11. `D02_pack_manifest.json`

## Ownership boundary

D02 owns the resolution grammar, not the contents of every modifier, pool, injury, object, actor, world-state, or live-play scene. D02 determines how uncertain actions resolve and how outcomes route deltas to the correct owner files.


---

<!-- FILE: D02-00_resolution_architecture_and_owner_boundaries.md -->

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


---

<!-- FILE: D02-01_d20_action_check_difficulty_and_modifiers.md -->

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


---

<!-- FILE: D02-02_margin_outcome_ladder_natural_20_natural_1.md -->

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


---

<!-- FILE: D02-03_cost_commitment_overinvestment_and_success_at_cost.md -->

# D02-03 Cost Commitment, Over-Investment, and Success at Cost

## Purpose

This file defines how cost is declared, committed, increased, and converted into outcome pressure.

## Core rule

Meaningful action requires commitment. Before rolling, the actor should declare intent, method, known cost, optional over-investment, and visible risk.

Declared cost usually commits regardless of outcome unless a specific owner-file rule says otherwise.

## Pre-roll declaration

Before the roll, identify:

1. intent;
2. method;
3. target;
4. relevant attribute/method/power/object/world-state;
5. known base cost;
6. optional over-investment;
7. known risk;
8. relevant source-local boundary.

This keeps player agency intact and prevents hidden arbitrary cost.

## Cost types

Cost may include:

| Cost | Owner |
|---|---|
| resource, pool, charge, fuel, reserve, overdraw, instability | D03 |
| proof, threshold, advancement opportunity, transformation pressure | D04 |
| time, tool use, research exposure, professional risk | D05 |
| route strain, Technique risk, Principle conflict, oath pressure | D06 |
| harm, injury, corruption, curse, backlash, condition | D07 |
| form-state pressure, identity strain, companion risk, AI/body consequence | D08 |
| object wear, relic depletion, platform stress, implant strain | D09 |
| faction attention, law risk, reputation shift, rumor, economic exposure | D10 |
| local cost retained from donor system | Source-local |

## Over-investment

Over-investment is optional additional commitment before resolution.

It may provide:

- flat modifier;
- advantage;
- lowered DN;
- improved effect scale;
- reduced consequence severity;
- increased progress units;
- broader target;
- better information quality;
- preservation against failure.

Over-investment may also increase risk:

- larger backlash;
- greater resource loss;
- higher public visibility;
- object damage;
- corruption pressure;
- faction/legal escalation;
- source-local consequence.

Over-investment is never free.

## Success at cost

Fractured is the standard success-at-cost band.

A Fractured result can mean:

- the goal succeeds but extra cost is imposed;
- the goal partially succeeds;
- the goal succeeds but creates D10 consequence;
- the goal succeeds but damages an object;
- the goal succeeds but worsens relationship or reputation;
- the goal succeeds but exposes hidden information;
- the actor gains progress but not completion;
- the actor must choose between success and avoiding consequence.

The player may sometimes be offered a choice:

- accept Fractured success with cost;
- decline success and take cleaner failure;
- push/escalate with additional risk.

D02 defines the grammar. Owner files define the allowable costs.

## Pushing and retries

No free rerolls.

A push or retry must change at least one of:

- cost;
- method;
- context;
- time;
- tool;
- risk;
- resource investment;
- owner-file state;
- source-local state.

Push costs may include:

- disadvantage;
- increased DN;
- extra declared cost;
- D03 overdraw;
- D07 strain/harm;
- D09 object wear;
- D10 exposure;
- time loss;
- source-local escalation.

## Cost visibility

Astra permits hidden costs only when lawful.

Valid hidden costs include:

- unknown hazard;
- hidden opposition;
- suppressed information;
- concealed world-state;
- source-local secret;
- failed assessment;
- Pneuma/cosmic backend pressure.

Invalid hidden costs include arbitrary punishment that the player had no way to assess, discover, infer, or accept within the action context.

## Cost after outcome

After outcome, commit:

1. declared cost;
2. over-investment cost;
3. outcome consequence;
4. hidden/delayed consequence if warranted;
5. owner-file deltas.

## Acceptance criteria

A cost ruling is valid when it:

1. separates declared cost from consequence;
2. makes over-investment optional and non-free;
3. supports success at cost;
4. blocks free retries;
5. routes cost to owner files;
6. preserves player-facing clarity where appropriate.


---

<!-- FILE: D02-04_power_context_register_resolution_integration.md -->

# D02-04 Power Context Register Resolution Integration

## Purpose

This file defines how the Power Context Register affects d20 resolution.

## PCR fields

Minimum PCR fields:

```yaml
power_context_register:
  location_tier: string
  location_tags: []
  opposition_modifier: string
  domain_alignment: []
  hidden_cosmic_modifier: string
```

D00 establishes PCR need. D02 uses PCR in resolution. D10 may record persistent world-state that feeds PCR.

## PCR-to-DN bands

| PCR tier | DN band |
|---|---|
| Mundane | 5–12 |
| Elevated | 8–16 |
| Charged | 12–20 |
| Apex | 16–24 |
| Transcendent | 20–28 |
| Mythic / Cosmic / Source-local | 24–32+ |

PCR tier is not the same as character level or donor challenge rating. It is contextual pressure.

## Location tags

Location tags can alter DN, advantage/disadvantage, cost, consequence severity, assessment output, or owner-file routing.

Examples:

- corrupted;
- sanctified;
- unstable;
- depleted;
- resource-rich;
- watched;
- contested;
- lawful;
- lawless;
- domain-aligned;
- domain-hostile;
- source-local.

## Opposition modifier

Opposition can be static or active.

Opposition may:

- set a DN;
- shift DN;
- trigger active contested check;
- impose disadvantage;
- increase consequence severity;
- require defense/resistance check;
- create D10 attention or memory.

## Domain alignment

Domain alignment can express compatibility or friction between action method and context.

Favorable alignment may:

- lower DN;
- grant advantage;
- reduce cost;
- reduce consequence severity;
- improve assessment quality;
- improve progress units.

Hostile alignment may:

- raise DN;
- impose disadvantage;
- increase cost;
- worsen consequence severity;
- trigger D07/D08/D10 pressure;
- produce source-local restriction.

Domain alignment may involve elements, death, law, machine, spirit, oath, route, faction, object, territory, corruption, scarcity, lineage, or source-local metaphysics.

## Hidden cosmic modifier

Hidden cosmic/Pneuma-style pressure is backend-only.

It may:

- subtly shift DN;
- affect consequence severity;
- alter coincidence or timing;
- influence relic resonance;
- create D10 world-facing myth only after surfacing.

It must not be displayed as ordinary luck, spendable currency, or player-visible modifier.

## PCR and impossible actions

A high PCR tier may indicate that ordinary methods cannot work. In that case, D02 should require a condition, resource, route, object, advancement threshold, or assessment discovery rather than assigning an arbitrarily high DN.

## PCR and consequence

PCR can affect not only success probability but also what failure means.

Examples:

- failed fire Technique in fuel-rich station may trigger D03/D07/D10 pressure;
- failed undead-form use in sanctified zone may trigger D07/D08/D10 pressure;
- failed relic use in sacred site may trigger D09/D10 pressure;
- failed stealth in watched district may trigger D10 information/law pressure.

## Acceptance criteria

A PCR resolution ruling is valid when it:

1. uses PCR as a real resolution input;
2. does not reveal hidden Pneuma as ordinary stat;
3. distinguishes DN shifts from consequence shifts;
4. respects domain alignment;
5. routes persistent effects to owner files.


---

<!-- FILE: D02-05_opposed_defense_resistance_and_contested_checks.md -->

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


---

<!-- FILE: D02-06_group_extended_and_dramatic_tasks.md -->

# D02-06 Group, Extended, and Dramatic Tasks

## Purpose

This file defines how D02 resolves group actions and tasks that cannot be fairly handled by a single roll.

## Group check types

| Type | Use |
|---|---|
| Lead + support | One actor rolls; allies help through modifier, advantage, DN reduction, progress units, or risk-sharing. |
| Majority | Group succeeds if most members succeed. |
| Weakest link | One failure can compromise the group. Use sparingly. |
| Best link | One qualified actor can solve the task for the group. |
| Accumulated | Each actor contributes progress toward a shared threshold. |

D02 should choose the group model based on the fiction and consequence.

## Lead + support

Use when one actor is clearly primary.

Support may provide:

- +2 or +5 modifier;
- advantage;
- lowered DN;
- extra progress unit;
- consequence mitigation;
- information rider.

Support can create risk for helpers if the action fails or Fractures.

## Majority checks

Use when group competence generally matters but individual failure can be absorbed.

Examples:

- group stealth through moderate risk;
- coordinated social effort;
- group endurance over a journey segment;
- crowd containment;
- broad research team effort.

## Weakest-link checks

Use only when one failure genuinely compromises the whole group.

Examples:

- crossing a fragile bridge as linked party;
- synchronized ritual where every participant must maintain role;
- group stealth through direct line-of-sight guard post.

Weakest-link checks should not be the default, because they punish party size.

## Best-link checks

Use when only one competent success is needed.

Examples:

- someone remembers a fact;
- one engineer identifies the fault;
- one scout spots the safe path;
- one diplomat knows the protocol.

## Accumulated group checks

Use when effort stacks.

Examples:

- repairing a platform;
- researching a mystery;
- fortifying a settlement;
- evacuating civilians;
- containing corruption;
- negotiating a broad alliance;
- salvaging a wreck.

## Extended tasks

Use extended tasks for goals requiring accumulated progress across time, scenes, or intervals.

Recommended structure:

```yaml
extended_task:
  task_ref: string
  goal: string
  progress_required: int
  current_progress: int
  roll_interval: string
  consequence_pressure: []
  cost_profile: []
  failure_pressure: []
  owner_handoffs: []
```

## Progress units

Recommended progress conversion:

| Outcome | Progress |
|---|---:|
| Ascendant | +3 |
| Clear | +2 |
| Fractured | +1 plus complication/cost |
| Receded | 0, but information/cost/exposure may occur |
| Sundered | -1 or complication/escalation |

Progress units are a D02 resolution tool. D05, D09, D10, and other owner files define what progress represents.

## Dramatic tasks

Dramatic tasks are extended tasks under acute pressure.

They may include:

- limited number of rounds;
- rising DN;
- escalating consequence;
- resource depletion;
- opposition progress;
- hazard clock retained source-locally;
- public or hidden D10 pressure.

D02 does not require physical dice timers or metacurrency.

## Race against opposition

For opposing extended tasks, track each side’s progress.

Possible end conditions:

- first to threshold wins;
- threshold before time expires;
- compare final progress at deadline;
- decisive margin creates Ascendant/Severe consequence;
- source-local ending condition.

## Acceptance criteria

A group/extended ruling is valid when it:

1. chooses the correct group model;
2. avoids punishing group size by default;
3. uses progress for extended work;
4. routes method to D05;
5. routes object/platform work to D09;
6. routes persistent world consequences to D10;
7. avoids physical dice or metacurrency requirements.


---

<!-- FILE: D02-07_assessment_reconnaissance_and_information_quality.md -->

# D02-07 Assessment, Reconnaissance, and Information Quality

## Purpose

This file defines assessment as a formal D02 action family.

## Core rule

Assessment allows an actor to spend time, focus, method, resource, risk, or opportunity to improve understanding before commitment.

Assessment is not guaranteed full truth. It is resolved through the outcome ladder.

## Standard assessment check

```text
d20 + assessment modifier vs Assessment DN
```

Likely attribute relationship:

- Insight probes or detects.
- Reason interprets or explains.
- D05 supplies method and expertise.
- D10 records persistent information-state if discovery matters.

D02 does not define final assessment skill list.

## What assessment can target

Assessment may seek:

- location tier;
- location tags;
- opposition bracket;
- approximate DN band;
- domain alignment;
- hazard type;
- resource risk;
- legal/faction risk;
- object-state clue;
- actor-state clue;
- route/Technique risk;
- hidden pressure;
- source-local constraint.

## Information quality by outcome

| Outcome | Information quality |
|---|---|
| Ascendant | Clear read, extra question, hidden relevant tag, risk forecast, or high-confidence interpretation. |
| Clear | Accurate actionable read. |
| Fractured | Partial but useful read; missing tag, cost, exposure, or ambiguity. |
| Receded | Vague risk sense, incomplete read, or confirmation of uncertainty. |
| Sundered | False, distorted, outdated, misattributed, or dangerously incomplete read. |

## Sundered assessment default

Default rule:

A Sundered assessment may be silently false unless a safeguard applies.

Safeguards may include:

- specialized method;
- high-quality tool;
- route feature;
- prior research;
- protective Technique;
- source-local doctrine;
- owner-file ability;
- high-tier expertise.

When a safeguard applies, Sundered may instead reveal that the reading feels wrong without revealing the truth.

## Assessment cost

Assessment may cost:

- action/time;
- D03 focus/resource;
- D05 method opportunity;
- D09 tool charge/wear;
- D10 exposure;
- source-local cost.

Assessment should be worthwhile but not free when the information materially changes risk.

## Assessment and PCR

Assessment can reveal parts of PCR:

- location tier;
- readable location tags;
- opposition bracket;
- domain alignment;
- approximate DN band;
- consequence severity cues.

Assessment should not reveal hidden Pneuma/cosmic modifier directly.

## Assessment and information-state

When assessment discovers, misreads, reveals, suppresses, or publicizes information that can matter later, route to D10 information-state.

Examples:

- true hidden fact discovered;
- false rumor believed;
- hidden route mapped;
- object identity identified;
- corruption zone detected;
- faction surveillance noticed;
- source-local secret exposed.

## Passive noticing

D02 may support passive awareness as static DN comparison when owner files define the value. Active assessment should usually provide more control, but can still fail or misread.

## Acceptance criteria

An assessment ruling is valid when it:

1. treats assessment as formal action;
2. uses Insight/Reason split appropriately;
3. permits partial and false reads;
4. protects Pneuma from direct exposure;
5. routes persistent knowledge to D10;
6. avoids turning D02 into investigation procedure.


---

<!-- FILE: D02-08_state_delta_routing_and_source_local_resolution_boundaries.md -->

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


---

<!-- FILE: D02-09_integration_checklists_and_ddr_register.md -->

# D02-09 Integration Checklists and DDR Register

## Purpose

This file records accepted D02 decisions, validation checklists, owner handoffs, and risk fixes.

## Accepted decision register

### D02-D20 — D20-first resolution architecture

Accepted:
- D02 uses `d20 + Resolution Modifier vs Difficulty Number` as the primary model.
- 2d6 is rejected as primary resolution.
- D20 is Astra-native and does not import donor d20 math.

### D02-DN — Difficulty Number ladder

Accepted:
- D02 uses a DN ladder from 5 to 32+.
- PCR tier, opposition, domain alignment, owner-file state, and source-local boundaries can shape DN.
- Some actions require gates rather than merely high DN.

### D02-OUTCOME — Margin outcome ladder

Accepted:
- Ascendant: +10 or higher.
- Clear: 0 to +9.
- Fractured: -1 to -4.
- Receded: -5 to -9.
- Sundered: -10 or lower.
- Meaningful rolls should avoid “nothing happens” as default.

### D02-CRIT — Natural 20 and natural 1

Accepted:
- Natural 20 is a critical opportunity, not automatic impossible success.
- Natural 1 is a complication flag, not automatic failure.

### D02-COST — Cost commitment

Accepted:
- Intent, method, known cost, optional over-investment, and visible risk are declared before rolling.
- Declared cost usually commits.
- Over-investment is never free.
- Fractured is the primary success-at-cost band.

### D02-PCR — PCR integration

Accepted:
- PCR affects DN, advantage/disadvantage, consequence severity, assessment output, hidden risk, and owner-file routing.
- Pneuma/cosmic pressure remains backend-only.

### D02-CONTEST — Opposition and resistance

Accepted:
- D02 supports static opposition, active contested checks, defense checks, and resistance checks.
- Defense/resistance outcomes are graduated, not binary by default.

### D02-GROUP — Group and extended tasks

Accepted:
- D02 supports lead/support, majority, weakest-link, best-link, and accumulated group checks.
- D02 supports extended progress tasks without physical timers or metacurrency.

### D02-ASSESS — Assessment

Accepted:
- Assessment is a formal action family.
- Insight probes; Reason interprets.
- Sundered assessment may be silently false by default.
- Persistent knowledge changes route to D10.

### D02-SLC — Source-local resolution

Accepted:
- Donor resolution systems receive lawful outcomes.
- Donor resolution math does not become Astra default.

## D02 ownership checklist

D02 owns:
- d20 check procedure;
- DN ladder;
- margin outcome interpretation;
- natural 20/natural 1 handling;
- cost commitment grammar;
- opposed/contested checks;
- defense/resistance check grammar;
- group and extended task grammar;
- assessment resolution grammar;
- outcome-to-delta routing;
- source-local resolution boundaries.

D02 does not own:
- attribute meanings;
- final modifier formulas;
- pools/resources;
- advancement;
- skill lists/methods;
- route powers;
- harm mechanics;
- actor substrate;
- object-state;
- world-state record formats;
- narration.

## Resolution checklist

For any roll, ask:

1. Is a roll needed?
2. What is the intent?
3. What is the method?
4. What is the target?
5. What is the known cost?
6. What is the visible risk?
7. Is over-investment declared?
8. What owner-file states contribute?
9. What DN or opposition applies?
10. What PCR pressure applies?
11. Is the action gated by missing requirements?
12. What is the margin?
13. Which outcome state applies?
14. What declared costs commit?
15. What consequence deltas route to D03–D10?
16. Is source-local boundary relevant?

## D03–D10 handoff matrix

| Trigger | Required handoff |
|---|---|
| pool/resource/fuel/charge/reserve/overdraw/instability | D03 |
| proof/threshold/breakthrough/tier/transformation progress | D04 |
| skill/method/research/crafting/investigation/competence | D05 |
| route/Technique/Principle/oath/domain expression | D06 |
| harm/injury/condition/curse/corruption/backlash/disaster | D07 |
| actor/form/body/companion/AI/spirit/clone/personhood substrate | D08 |
| object/relic/platform/implant/tool/material/salvage | D09 |
| faction/law/economy/reputation/relationship/information/territory | D10 |

## Pre-generation risk fixes embedded

### Risk 1 — D20 becomes donor d20 clone

Fix:
- D02 explicitly blocks donor proficiency, class math, spell assumptions, armor conventions, saving throw categories, critical damage rules, and action economy.

### Risk 2 — D20 swinginess overwhelms competence

Fix:
- no-roll principle, bounded modifiers, advantage/disadvantage, assessment, over-investment, group/extended tasks, and margin-based partial outcomes.

### Risk 3 — Natural 20 breaks gates

Fix:
- natural 20 is opportunity, not automatic impossible success.

### Risk 4 — Natural 1 makes experts incompetent

Fix:
- natural 1 is complication flag, not automatic failure.

### Risk 5 — Partial outcomes disappear

Fix:
- Fractured and Receded remain core outcome states.

### Risk 6 — Cost becomes optional

Fix:
- declared cost commits; over-investment routes to owner files.

### Risk 7 — PCR becomes flavor

Fix:
- PCR affects DN, roll state, consequence severity, information quality, and hidden risk.

### Risk 8 — Defense becomes binary saving throw

Fix:
- defense/resistance use full outcome ladder.

### Risk 9 — Group checks punish parties

Fix:
- support multiple group-check types and reserve weakest-link for true weakest-link fiction.

### Risk 10 — Source-local resolution leaks

Fix:
- donor systems receive lawful outcomes and source-local boundaries.

## Acceptance criteria

D02 is doctrine-ready when it:

1. uses d20-first resolution;
2. keeps Astra’s five outcome states;
3. uses declared cost and over-investment lawfully;
4. integrates PCR;
5. supports contested, defense, group, extended, and assessment checks;
6. routes deltas to D03–D10;
7. blocks donor resolution leakage.


---

<!-- FILE: D02_pack_manifest.json -->

```json
{
  "pack": "D02 D20 Resolution, Cost Commitment, PCR Difficulty, Assessment, and Delta Routing Doctrine",
  "version": "v0.1",
  "generated_date": "2026-06-02",
  "status": "generated",
  "phase": "Astra Ascension native design doctrine",
  "primary_owner": "D02",
  "manifest_filename": "D02_pack_manifest.json",
  "primary_resolution_model": "d20 + Resolution Modifier vs Difficulty Number",
  "outcome_states": {
    "Ascendant": "+10 or higher",
    "Clear": "0 to +9",
    "Fractured": "-1 to -4",
    "Receded": "-5 to -9",
    "Sundered": "-10 or lower"
  },
  "critical_handling": {
    "natural_20": "critical opportunity, not automatic impossible success",
    "natural_1": "complication flag, not automatic failure"
  },
  "doctrine_files": [
    "D02-README_manifest.md",
    "D02-00_resolution_architecture_and_owner_boundaries.md",
    "D02-01_d20_action_check_difficulty_and_modifiers.md",
    "D02-02_margin_outcome_ladder_natural_20_natural_1.md",
    "D02-03_cost_commitment_overinvestment_and_success_at_cost.md",
    "D02-04_power_context_register_resolution_integration.md",
    "D02-05_opposed_defense_resistance_and_contested_checks.md",
    "D02-06_group_extended_and_dramatic_tasks.md",
    "D02-07_assessment_reconnaissance_and_information_quality.md",
    "D02-08_state_delta_routing_and_source_local_resolution_boundaries.md",
    "D02-09_integration_checklists_and_ddr_register.md"
  ],
  "owner_boundaries": {
    "D02_owns": [
      "d20 check procedure",
      "Difficulty Number ladder",
      "margin outcome interpretation",
      "natural 20/natural 1 handling",
      "cost commitment grammar",
      "opposed and contested check grammar",
      "defense and resistance check grammar",
      "group and extended task grammar",
      "assessment resolution grammar",
      "outcome-to-delta routing",
      "source-local resolution boundaries"
    ],
    "D02_does_not_own": {
      "D01": "attribute meanings",
      "D03": "Power Economy, pools, fuels, charges, overdraw",
      "D04": "advancement gates and breakthrough procedure",
      "D05": "skills, methods, research, investigation procedures",
      "D06": "routes, techniques, principles, powers",
      "D07": "harm, injury, corruption, death, damage families",
      "D08": "actor body/personhood/form substrate",
      "D09": "object-state, relics, platforms, implants",
      "D10": "world-state records",
      "D11": "live-play narration and presentation"
    }
  },
  "blocked_imports": [
    "2d6 primary resolution",
    "donor d20 proficiency math",
    "donor action economy",
    "donor saving throw categories",
    "donor armor/hit conventions",
    "donor spell assumptions",
    "step dice primary resolution",
    "metacurrency-driven core resolution",
    "physical dice timers as requirement"
  ]
}
```
