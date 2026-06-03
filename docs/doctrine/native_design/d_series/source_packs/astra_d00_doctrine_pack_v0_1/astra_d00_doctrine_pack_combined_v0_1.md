# D00 Core Play Experience, Cost, Context, and World-Memory Doctrine v0.1

Generated: 2026-06-02

This combined export contains the full doctrine pack in file order.


---

<!-- FILE: D00-README_manifest.md -->

# D00 Core Play Experience, Cost, Context, and World-Memory Doctrine — Manifest

Version: v0.1  
Phase: Astra Ascension native design doctrine  
Status: Doctrine pack generated from accepted D00 decisions  
Primary owner: D00

## Purpose

D00 defines the core experience contract for Astra Ascension. It establishes what a session is supposed to produce, why power must carry cost, why context changes the meaning of power, why assessment matters before commitment, and why the world must remember significant action.

D00 is not a complete rules engine. It is the top-level play contract that later doctrine must obey.

## Core experience contract

After a meaningful session, the player should have:

1. made meaningful resource decisions with real costs and partial outcomes;
2. left the character measurably different, the world measurably different, or both;
3. produced at least one tracked delta to resource/pool/instability, character condition/injury/threshold, world state, faction state, object state, or relationship state.

The minimum viable session loop is:

- meaningful action;
- visible or inferable risk/cost;
- consequence-bearing resolution;
- at least one committed delta.

## Primary tensions

D00 locks three layered tensions.

| Tension | Function |
|---|---|
| Power vs. Cost | No meaningful power should be free of pressure. |
| Identity vs. Pressure | Character identity changes, resists, fractures, adapts, or deepens under pressure. |
| Competence vs. Consequence | Skilled action matters, but the world still records outcomes. |

## File order

1. `D00-00_core_play_experience_contract.md`
2. `D00-01_power_cost_context_and_world_memory.md`
3. `D00-02_power_context_register_and_assessment_baseline.md`
4. `D00-03_state_delta_commit_protocol.md`
5. `D00-04_campaign_loop_and_long_form_durability.md`
6. `D00-05_source_local_and_conversion_boundaries.md`
7. `D00-06_integration_checklists_and_ddr_register.md`
8. `D00_pack_manifest.json`

## Ownership boundary

D00 owns the core play contract, not subsystem implementation.

D00 does not own final resource formulas, advancement math, skill lists, route powers, damage systems, actor substrate, object-state, world-state records, or live-play narrator behavior. It establishes the requirements those later files must satisfy.


---

<!-- FILE: D00-00_core_play_experience_contract.md -->

# D00-00 Core Play Experience Contract

## Purpose

This file defines what Astra Ascension is trying to make happen at the table or runtime level before any subsystem expands. It is the design contract for play.

## Core rule

Astra play is consequence-bearing progression under contextual pressure. The player should make decisions where power, cost, identity, competence, and world memory interact.

## Session success condition

A session is successful when the player has:

1. made at least one meaningful decision with a real cost or risk;
2. produced a measurable change in character, world, object, faction, relationship, or resource state;
3. learned something actionable about context, pressure, opposition, self, power, or consequence.

D00 does not require every session to include combat, advancement, treasure, faction politics, or exploration. It requires meaningful commitment and state change.

## Minimum viable loop

The minimum loop is:

1. **Assess** — identify or infer context, risk, opportunity, opposition, or cost.
2. **Commit** — choose an action and accept a declared cost/risk profile.
3. **Resolve** — determine outcome with partial results possible.
4. **Delta** — commit at least one state change.
5. **Remember** — preserve future-facing consequences where relevant.

Later doctrine files implement this loop through resources, advancement, skills, routes, harm, actors, objects, and world-state.

## What counts as meaningful

An action is meaningful when it can alter:

- a resource, pool, instability, corruption, charge, fuel, or reserve;
- a condition, injury, threshold, form-state, or identity pressure;
- an advancement state, proof, breakthrough, transformation, or route expression;
- a relationship, favor, grudge, debt, reputation, or faction memory;
- a location, hazard, route, law, economy, information-state, or public record;
- an object, relic, platform, implant, material, or source-local construct.

An action that cannot alter anything may still be color, but it is not a core Astra action.

## Partial outcomes

Astra assumes partial outcomes are normal. Success and failure are not binary by default. Partial success, mixed consequence, delayed harm, hidden cost, misread information, collateral effect, and future pressure are valid play outputs when supported by the resolution file.

## Player-facing clarity

The player should usually understand:

- what they are trying to do;
- what they are risking;
- what cost is known before commitment;
- what uncertainty remains;
- what kind of consequence could occur.

Hidden information is allowed. Arbitrary hidden punishment is not.

## Corpus-scale requirement

This contract must survive fantasy, sci-fi, cultivation, cyberware, psionics, horror, ships, mechs, companions, crafting, salvage, politics, dungeon, hexcrawl, faction, and narrative donor systems. It cannot assume one donor genre’s default loop.

## Acceptance criteria

A downstream rule satisfies D00 when it:

1. supports meaningful commitment;
2. permits partial outcomes;
3. creates trackable deltas;
4. respects context;
5. avoids free power;
6. preserves future-facing consequences;
7. distinguishes doctrine design from runtime narration.


---

<!-- FILE: D00-01_power_cost_context_and_world_memory.md -->

# D00-01 Power, Cost, Context, and World Memory

## Purpose

This file locks Astra’s highest-level power doctrine: power has cost, context changes power, and the world remembers meaningful consequences.

## Power vs. Cost

Power in Astra must carry cost, limit, risk, requirement, opportunity cost, exposure, debt, instability, depletion, consequence, or identity pressure.

Cost may appear as:

- spent resource;
- instability or corruption load;
- injury or condition;
- attention drawn;
- faction consequence;
- relationship strain;
- object wear or depletion;
- legal exposure;
- strategic resource loss;
- time pressure;
- route or identity strain;
- source-local cost.

D00 does not define cost formulas. D03, D04, D05, D06, D07, D08, D09, and D10 own specific cost implementation.

## Context determines what power means

Power is not absolute. Its meaning changes by location, opposition, scale, domain alignment, resource environment, law, faction, object access, and hidden conditions.

Examples:

- a fire Technique is decisive in one place and dangerous in a fuel-rich station;
- a relic is sacred in one jurisdiction and contraband in another;
- an undead form is survival tool in a corrupted marsh and illegal inside a sanctified city;
- a ship reactor is ordinary infrastructure until a blockade makes fuel strategic;
- a social favor is minor locally but decisive inside a faction hierarchy.

## Contextual power model

D00 accepts contextual power:

| Power context | Meaning |
|---|---|
| Scarce / Precious | Power is limited, rationed, expensive, or socially controlled. |
| Abundant / Unstable | Power is available but risky, volatile, or consequence-heavy. |
| Dramatically Scaling | Power changes qualitative scale at thresholds. |
| Domain-contextual | Power strengthens, weakens, mutates, or becomes unsafe depending on environment and opposition. |

## World memory

The world remembers when consequences are meaningful.

World memory may be carried by:

- resource depletion;
- scars, injuries, corruption, or form-state;
- faction records;
- public rumor;
- legal warrants;
- object history;
- territory damage;
- relationship debts or grudges;
- hidden intelligence;
- source-local clocks or local systems;
- historical records.

D10 later owns world-facing memory records. D00 establishes that those records must exist.

## No decorative consequence

Consequences should not be only prose when they create future pressure. If a consequence can affect future action, access, legality, reputation, faction behavior, object state, territory condition, or actor continuity, it should have a record owner.

## Acceptance criteria

This doctrine is satisfied when later files:

1. tie meaningful power to cost or pressure;
2. make context mechanically and narratively relevant;
3. prevent universal power assumptions from one donor system;
4. preserve consequential change through appropriate records;
5. keep hidden state lawful rather than arbitrary.


---

<!-- FILE: D00-02_power_context_register_and_assessment_baseline.md -->

# D00-02 Power Context Register and Assessment Baseline

## Purpose

This file defines the baseline need for a Power Context Register and makes assessment/reconnaissance part of the core action loop.

## Power Context Register

The Power Context Register, or PCR, is the minimum context layer used to interpret action difficulty, risk, power meaning, and consequence pressure.

Minimum runtime fields:

```yaml
power_context_register:
  location_tier: string
  location_tags: []
  opposition_modifier: string
  domain_alignment: []
  hidden_cosmic_modifier: string
```

D00 establishes the need for these fields. D02 owns resolution use. D10 later records persistent place/world context.

## Location tier

Location tier is a broad signal of environmental pressure.

Example tiers may include mundane, elevated, charged, apex, transcendent, or source-local equivalents. D00 does not lock exact numeric bands; D02 may do that.

## Location tags

Location tags describe context that changes action meaning.

Examples:

- sanctified;
- corrupted;
- unstable;
- low-resource;
- high-resource;
- watched;
- contested;
- lawful;
- lawless;
- hidden;
- source-local;
- domain-aligned;
- domain-hostile.

## Opposition modifier

Opposition modifier records how local opposition changes pressure. It may represent relative tier, faction preparedness, environmental advantage, hidden defenses, social authority, or source-local pressure.

D02 owns resolution effect.

## Domain alignment

Domain alignment records whether the declared method aligns with, conflicts with, or is neutral to the location, opposition, route, Principle, object, faction law, or source-local context.

Domain alignment is not only elemental. It may involve death, law, oath, machine, spirit, territory, corruption, scarcity, lineage, route, or faction context.

## Hidden cosmic modifier

The hidden cosmic modifier is a backend-only pressure axis for rare fate/cosmic/Pneuma-like conditions. It should never become an ordinary player-visible luck score.

D01 owns Pneuma doctrine. D02 owns how hidden modifier affects resolution if used. D10 may record world-facing cosmic consequence only when it becomes visible.

## Assessment baseline

Assessment is a core action family. It rewards probing before commitment.

Assessment may attempt to learn:

- location tier;
- location tags;
- opposition pressure;
- approximate difficulty band;
- domain alignment;
- resource risks;
- hidden dangers;
- source-local constraints.

D00 requires assessment to exist. D02 owns resolution procedure. D05 owns competence/method if assessment depends on skills. D10 owns persistent information state when discovered knowledge matters.

## Visibility principle

Players should not always know all context. They should usually have enough visible or discoverable signal to make informed risk choices.

Visible context may include:

- apparent location tier;
- obvious tags;
- known law/faction constraints;
- visible hazards;
- public reputation;
- known object state.

Hidden context may include:

- concealed opposition;
- suppressed records;
- secret route effects;
- hidden Pneuma/cosmic modifier;
- source-local secrets.

## Acceptance criteria

PCR doctrine is satisfied when later files:

1. use context to affect resolution without arbitrary GM fiat;
2. keep hidden state lawful and discoverable where appropriate;
3. support assessment before commitment;
4. avoid forcing all context into visible UI;
5. preserve D01 Pneuma as backend-only.


---

<!-- FILE: D00-03_state_delta_commit_protocol.md -->

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


---

<!-- FILE: D00-04_campaign_loop_and_long_form_durability.md -->

# D00-04 Campaign Loop and Long-Form Durability

## Purpose

This file defines how D00 supports long campaigns without forcing a single genre loop.

## Long-form campaign premise

Astra should support campaigns where the player’s power, identity, relationships, faction standing, objects, territory access, information-state, and world consequences accumulate across long arcs.

D00 does not require campaigns to last years, but its architecture must survive campaigns that do.

## Durable campaign loops

Astra supports multiple recurring loops:

| Loop | Meaning |
|---|---|
| Power Loop | Gain, spend, risk, stabilize, transform, and contextualize power. |
| Identity Loop | Actor changes under pressure and must integrate or resist change. |
| Competence Loop | Methods improve and choices become more precise. |
| Object Loop | Objects, relics, implants, platforms, and materials gain consequence. |
| World Loop | Factions, law, territories, markets, rumors, and relationships remember action. |
| Discovery Loop | Hidden truth becomes known, misreported, suppressed, or weaponized. |
| Cost Loop | Short-term power produces long-term pressure. |
| Recovery Loop | Consequences can be repaired, reconciled, resolved, or historically retained. |

## Campaign durability risks

D00 identifies these major risks:

1. power becomes free escalation;
2. character changes are only cosmetic;
3. world consequences are forgotten;
4. hidden state becomes arbitrary;
5. donor assumptions become default canon;
6. relationships flatten into simple reputation;
7. resources, objects, factions, and information-state are not linked;
8. live-play narration invents consequences unsupported by doctrine.

Later files must address these.

## Character and world co-evolution

Astra should support both:

- character changes affecting the world;
- world changes affecting the character.

Examples:

- a transformation changes legal status;
- a faction grudge changes market access;
- a relic theft changes sacred law and object history;
- a corruption zone creates form-state pressure;
- a hidden rumor affects reputation before truth is known.

## Source-local campaign structures

Donor adventure paths, faction clocks, kingdom turns, reputation tracks, hexcrawls, downtime events, war fronts, treasure economies, and domain systems may be retained source-locally. D00 does not import any as universal campaign loop.

## Acceptance criteria

A long-form campaign loop satisfies D00 when it:

1. allows cumulative change without record overload;
2. supports multiple genres and donor families;
3. records state through owner files;
4. permits consequence resolution and recovery;
5. avoids turning one donor campaign structure into Astra default.


---

<!-- FILE: D00-05_source_local_and_conversion_boundaries.md -->

# D00-05 Source-local and Conversion Boundaries

## Purpose

This file defines how D00 protects Astra’s core experience from donor-system leakage.

## Core rule

Donor systems may inform Astra but do not become Astra law by vocabulary, familiarity, or mechanical completeness. Every donor construct must be mapped, normalized, retained source-locally, quarantined, or escalated through the correct owner.

## D00-level conversion risk

The most dangerous donor leakage at D00 level is not a specific mechanic. It is a hidden play contract.

Examples:

- all power comes from one cosmology;
- all play centers on combat;
- all progress is level-up;
- all items are treasure;
- all faction systems are reputation points;
- all world-state is GM prose;
- all consequences are temporary;
- all advancement is personal rather than world-facing;
- all rules assume one genre’s economy, law, map, or action loop.

D00 blocks these assumptions.

## Source-local retention

A donor play structure may be retained locally when it is useful but not generalizable.

Examples:

- adventure-path clocks;
- donor hexcrawl procedure;
- domain turns;
- faction favor points;
- cyberpunk heat;
- horror clue nodes;
- star-sector travel;
- cultivation tribulation sequence;
- kingdom unrest;
- source-local reputation ladder.

Retention requires a boundary record in the appropriate owner file.

## Quarantine and escalation

If donor pressure exposes a missing Astra framework, do not invent decorative doctrine.

Quarantine when:
- the construct is unsafe to normalize now;
- it bundles too many owner domains;
- it requires missing doctrine;
- it contradicts current core doctrine;
- it would force a donor assumption into canon.

Escalate when:
- the gap is repeated across donor families;
- the construct cannot be handled source-locally without damaging conversion;
- the construct reveals a missing core architecture.

## Acceptance criteria

D00 conversion boundaries are satisfied when:

1. donor play contracts are identified;
2. donor assumptions are not imported silently;
3. source-local systems are bounded;
4. missing frameworks are quarantined or escalated;
5. Astra’s core loop remains source-agnostic.


---

<!-- FILE: D00-06_integration_checklists_and_ddr_register.md -->

# D00-06 Integration Checklists and DDR Register

## Purpose

This file records accepted D00 decisions and provides validation checklists for later doctrine.

## Accepted decision register

### D00-CPEC — Core Play Experience Contract

Accepted:
- A session should produce meaningful resource decisions, measurable character/world change, and a tracked delta.
- MVP loop requires meaningful action plus character or world change.
- Partial outcomes are normal.
- Assessment before commitment is rewarded.

### D00-PCCWM — Power, Cost, Context, World Memory

Accepted:
- Primary tension: Power vs. Cost.
- Secondary tension: Identity vs. Pressure.
- Tertiary tension: Competence vs. Consequence.
- Power is contextual, not absolute.
- The world remembers meaningful action.

### D00-PCR — Power Context Register

Accepted:
- PCR includes location tier, location tags, opposition modifier, domain alignment, and hidden cosmic/Pneuma-style backend modifier.
- PCR is partially visible.
- Assessment/reconnaissance is a core action family and is formalized downstream.

### D00-SDCP — State-Delta Commit Protocol

Accepted:
- Every meaningful action commits a tracked delta to at least one owner family.
- Declared cost, emergent consequence, delayed consequence, hidden consequence, and historical consequence are distinct.

## D00 ownership checklist

D00 owns:
- core play contract;
- play-experience success condition;
- power/cost/context/world-memory premise;
- state-delta requirement;
- assessment as a required action family;
- source-local play-contract boundaries.

D00 does not own:
- resource formulas;
- advancement math;
- skill methods;
- route powers;
- harm mechanics;
- actor substrate;
- object-state;
- world-state records;
- live-play narrator behavior;
- final schemas.

## Validation checklist

For any later doctrine file, ask:

1. Does it support meaningful commitment?
2. Does it allow partial outcomes where appropriate?
3. Does it produce trackable deltas?
4. Does it preserve power/cost pressure?
5. Does it account for context?
6. Does it protect hidden state from arbitrariness?
7. Does it prevent donor assumptions from becoming default?
8. Does it distinguish doctrine from live-play narration?
9. Does it identify the owner file for consequences?
10. Does it preserve long-form campaign durability?

## Handoff matrix

| D00 pressure | Owner |
|---|---|
| Resource cost, instability, fuel, charges | D03 |
| Advancement proof, thresholds, breakthroughs | D04 |
| Assessment method, research, competence | D05 |
| Route powers, Techniques, Principles | D06 |
| Harm, injury, corruption, backlash | D07 |
| Actor identity, form, body, companions, AI | D08 |
| Objects, relics, implants, platforms | D09 |
| World memory, factions, law, economy, information | D10 |
| Narration and player-facing presentation | D11 / later runtime |

## Pre-generation risk queue

1. D00 becomes generic design prose. Fix: keep owner handoffs and delta logic explicit.
2. D00 imports one donor play loop. Fix: preserve source-agnostic core loop.
3. Power becomes free escalation. Fix: require cost/pressure.
4. Context becomes flavor only. Fix: preserve PCR requirement.
5. World memory is deferred too far. Fix: require state-delta owners.
6. Hidden state becomes arbitrary. Fix: require assessment and lawful hidden-state handling.
7. D00 starts implementing later mechanics. Fix: keep D00 as contract layer only.


---

<!-- FILE: D00_pack_manifest.json -->

```json
{
  "pack": "D00 Core Play Experience, Cost, Context, and World-Memory Doctrine",
  "version": "v0.1",
  "generated_date": "2026-06-02",
  "status": "generated",
  "phase": "Astra Ascension native design doctrine",
  "primary_owner": "D00",
  "manifest_filename": "D00_pack_manifest.json",
  "doctrine_files": [
    "D00-README_manifest.md",
    "D00-00_core_play_experience_contract.md",
    "D00-01_power_cost_context_and_world_memory.md",
    "D00-02_power_context_register_and_assessment_baseline.md",
    "D00-03_state_delta_commit_protocol.md",
    "D00-04_campaign_loop_and_long_form_durability.md",
    "D00-05_source_local_and_conversion_boundaries.md",
    "D00-06_integration_checklists_and_ddr_register.md"
  ],
  "owner_boundaries": {
    "D00_owns": [
      "core play contract",
      "power/cost/context/world-memory premise",
      "state-delta commitment requirement",
      "minimum viable session loop",
      "assessment as core action family",
      "source-local play-contract boundaries"
    ],
    "D00_does_not_own": {
      "D03": "resource formulas and Power Economy",
      "D04": "advancement math and breakthrough mechanics",
      "D05": "skills, research, and assessment methods",
      "D06": "routes, techniques, and principles",
      "D07": "harm, injury, corruption, backlash",
      "D08": "actor substrate, form, body, companions, AI",
      "D09": "object-state",
      "D10": "world-state records",
      "D11": "narration and player-facing presentation"
    }
  }
}
```
