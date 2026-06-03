# D04-00 — Advancement Architecture Overview

Status: `doctrine-draft / accepted D04 design decisions`  
Layer: Native Design Phase / D04 advancement doctrine  
Owner: advancement architecture  
Depends on: D00 Core Play Experience, D01 Attributes, D02 Resolution, D03 Power Economy and Expression Doctrine  
Feeds: D05 Skills/Professions/Knowledge, D06 Path/Class/Dao/Domain, D07 Harm/Recovery, D08 Actor/Bond/Companion, D09 Item/Relic/Platform, D10 World/Faction/Territory, runtime progression schema

## 1. Purpose

D04 defines how entities advance in Astra Ascension.

Advancement is not only level gain. Advancement includes proof, experience, training, transformation, consequences, achievements, titles, axes, routes, breakthroughs, Awakening, tier authorization, Development Picks, world recognition, capstone finality, and eventual Ascension Access.

D04 must support a long campaign structure with 100 levels and 10 tiers while also allowing advancement outside level/tier progression. A mundane farmer, blacksmith, fisherman, hunter, scholar, ruler, healer, spirit, AI, relic-bound actor, platform-linked actor, companion, faction, territory, or world-facing entity must have lawful advancement routes if its proof and owner files support them.

## 2. Core advancement principle

Astra advancement is proof-shaped transformation.

A level is cadence.  
A tier is authorization.  
A proof bundle is eligibility.  
A Development Pick is a lawful opportunity.  
A breakthrough is transformation.  
A Path/Class/Dao route is identity pressure.  
An axis is focused growth.  
A capstone is final proof.  
Ascension Access is a post-capstone opportunity, not mandatory exile.

No single advancement layer owns the whole character.

## 3. What D04 owns

D04 owns:

- the advancement philosophy;
- the 100-level / 10-tier advancement frame;
- Tier 0 as Mortal / grounded pre-awakening play;
- level 5 as the Mortal Threshold / Awakening soft cap;
- levels 95–100 as the Capstone Band;
- levels and tiers as separate but interacting structures;
- proof events and proof handling;
- Proof Bundles and sufficiency bands;
- contextual proof weight;
- Awakening Proof;
- Catalyst / Route / Anchor logic;
- Dynamic Triadic Awakening;
- Structured Variable Awakening Package;
- typed Development Picks;
- Development Pick cadence, hold states, and validation gates;
- tier authorization table;
- tier direct benefit menu;
- advancement axis registration and owner routing;
- breakthrough threshold states;
- breakthrough resolution procedure;
- breakthrough payload categories and quality bands;
- capstone procedure;
- Level 100 Ascension Access as a reserved post-capstone opportunity;
- runtime and schema handoff requirements for advancement.

## 4. What D04 must not own

D04 must not own:

- final dice architecture or outcome lane naming; D02 owns resolution procedure;
- exact Expression formulas, cost math, scope flags, or Power Economy math; D03 owns these;
- final skill lists, profession rank tables, knowledge taxonomies, or research/training procedures; D05 owns these;
- final Path/Class/Dao feature tables, domain mechanics, technique access, or route feature design; D06 owns these;
- exact harm, injury, death, crippling, recovery, corruption-purge, or unmaking mechanics; D07 owns these;
- full actor-state schema for spirits, AIs, swarms, companions, platforms, or nonstandard entities; D08 owns these;
- item, relic, implant, tool, vehicle, ship, platform, installable asset, or soulbound object schema; D09 owns these;
- faction, settlement, territory, law, economy, standing, exploration, travel, world-state, or recognition systems; D10 owns these;
- canonical sourcebook acceptance;
- runtime implementation code;
- live-play narration behavior;
- donor-specific final conversions.

When D04 needs another file, it names the handoff rather than absorbing that file.

## 5. Level and tier structure

Astra uses 100 levels and 10 tiers, with Tier 0 as the mortal/pre-awakening band.

| Tier | Level band | Function |
|---:|---|---|
| 0 | 1–5 | Mortal / grounded / pre-awakening. Level 5 is a soft cap and Awakening threshold. |
| 1 | 5–15 | Initial ascendant authorization after Awakening or equivalent route access. |
| 2 | 16–25 | Stabilized ascendant authorization. |
| 3 | 26–35 | Structural development authorization; Tier 2→3 requires Standard + Structural Proof. |
| 4 | 36–45 | Advanced authorization. |
| 5 | 46–55 | Major ascendant authorization. |
| 6 | 56–65 | Superior authorization. |
| 7 | 66–75 | Apex-band authorization. |
| 8 | 76–85 | Transcendent-band authorization. |
| 9 | 86–95 | Mythic-band authorization. |
| 10 | 95–100 | Capstone authorization. Levels 95–100 are the hardest proof band. |

Level 5 and level 95 are boundary levels. A level 5 character may remain Tier 0 until Awakening or equivalent access is resolved. A level 95 character may remain in Tier 9 until Capstone Threshold Entry is resolved.

## 6. Level function versus tier function

Levels provide cadence and Development Picks.

Tiers provide authorization ceilings and transition packages.

Breakthroughs provide transformation.

A character may have enough numerical level cadence to approach a threshold but still lack lawful proof to cross. Conversely, a character may perform extraordinary proof before the threshold; that proof is not wasted. It may become a stronger Awakening option, title seed, axis seed, rare route, future Development Pick target, or capstone-relevant history.

## 7. Tier 0 and mundane viability

Tier 0 must support mundane play without treating it as defective.

A farmer, baker, hunter, fisherman, healer, scholar, guard, merchant, smith, cook, sailor, shepherd, clerk, guide, or other grounded actor can remain mundane as long as the campaign supports it. Tier 0 advancement may include profession axes, relationships, community standing, tool familiarity, physical conditioning, exploration records, skills, title seeds, achievements, proof records, and route seeds.

A Tier 0 actor is not blocked from future ascendant play. If a mundane character decides many sessions later to seek more, the system should identify lawful route-seeking projects, mentors, exposure, trials, relics, factions, experiments, domain contacts, or other access vectors. The character's prior mundane proof may become powerful contextual proof.

## 8. Awakening as threshold, not railroading

A character does not need a preplanned ascendant path. At level 5 or equivalent threshold, the system may identify lawful Awakening routes based on proof. It must warn the player that progression beyond the Mortal Threshold may assign or formalize a contextually appropriate Path/Class/Dao route if they proceed.

The player may:

- accept an Awakening option;
- delay Awakening;
- gather more proof;
- redirect toward a different route;
- seek an anchor, teacher, faction, relic, domain, or method;
- remain at the threshold as a grounded actor;
- enter a forced/coerced/corrupted route if the fiction supports it and warnings are handled.

## 9. Advancement is multi-axis

Astra advancement includes many axes beyond level, tier, class, and breakthrough. D04 reserves and routes these axes without finalizing every subsystem.

Advancement axes may include attributes, skills, professions, techniques, Expressions, mastery specializations, kinform/bloodline evolution, soul/core development, Dao/concept comprehension, affinities, bonds, swarms, avatars, equipment, soulbound items, crafting professions, territories, settlements, reputation, titles, achievements, karma/causal weight, corruption, power reservoir depth, regeneration, channeling speed, range/scope extension, multi-target capacity, senses, mental fortress, insight/comprehension, language/lexicon unlock, leadership, body tempering, personal realm, sigil/rune comprehension, map/exploration completion, bestiary/codex mastery, mythic imprint, devotion/favor, skill fusion, and seal unlocking.

D04 registers these as possible advancement families. Owner files define exact mechanics.

## 10. Advancement layer separation

D04 distinguishes advancement layers as follows:

| Layer | Function | D04 role |
|---|---|---|
| Level | Long-form cadence and Development Pick grant. | Defines cadence, not exact feature tables. |
| Tier | Authorization ceiling and transition package. | Defines scale, not mastery. |
| Proof | Eligibility and context. | Defines bundles and handling. |
| Axis | Focused advancement track. | Defines registry and routing. |
| Development Pick | Legal advancement opportunity. | Defines pick taxonomy and validation. |
| Breakthrough | Transformative threshold event. | Defines procedure and payload logic. |
| Awakening | Tier 0→1 formal route threshold. | Defines Dynamic Triadic Awakening and package. |
| Route | Path/Class/Dao identity pressure. | Initializes and routes to D06. |
| Title/Achievement | Formalized history or recognition. | Defines proof relation and handoff. |
| Capstone | Final proof band. | Defines levels 95–100 and Capstone Picks. |
| Ascension Access | Post-level-100 opportunity. | Reserves access rule and handoffs. |

## 11. Advancement cannot be purely combat-shaped

Combat is only one proof family. D04 must support advancement through:

- craft;
- service;
- governance;
- exploration;
- discovery;
- study;
- teaching;
- healing;
- survival;
- sacrifice;
- oathkeeping;
- oathbreaking;
- corruption;
- purification;
- settlement building;
- territory defense;
- relic development;
- bond deepening;
- profession mastery;
- monster study;
- social transformation;
- world repair;
- world harm;
- impossible repeated labor.

A baker killing wolves, a fisherman pursuing impossible fish, a blacksmith making 10,000 swords, or a healer rebuilding a plague-struck town can all create advancement proof if the proof has sufficient contextual weight and owner-file support.

## 12. Anti-breakage rule

A creative desired outcome is not automatically a valid attempted Expression or breakthrough.

The player may describe a desired outcome. To become a valid attempted action or advancement, the character must have a lawful route or action vector, such as proof, route access, training, economy contact, Expression basis, carrier, external anchor, teacher, faction, relic, source-local mechanism, forced pressure, or dangerous push posture.

If no lawful vector exists, the system should not authorize a roll that speaks power into existence. It should route the desire into a project, research question, training goal, route-seeking objective, source-local request, or dangerous self-harm attempt if the character tries to force it.

## 13. Corpus-scale donor pressure

D04 must survive donors that use:

- d20 levels and classes;
- point-buy advancement;
- lifepath/career growth;
- classless build budgets;
- skill ranks;
- narrative tags/aspects;
- dice-pool advancement;
- cyberware/body modification;
- cultivation realms;
- spell levels;
- tech trees;
- item rarity;
- faction rank;
- settlement tier;
- companion bond;
- mech/frame licenses;
- vehicle upgrade paths;
- divine favor;
- sanity/corruption;
- epic destinies;
- apotheosis;
- realm ascension.

All donor structures are evidence. Their function may map into D04 layers, but their packaging and math do not become Astra law.

## 14. D04 minimum doctrine rule

D04 is minimally usable when it can answer these questions without inventing final downstream mechanics:

1. What kind of advancement is being requested?
2. What proof supports it?
3. What tier authorizes it?
4. What axis or route owns it?
5. What Development Pick or breakthrough procedure applies?
6. What owner file must validate the details?
7. What state deltas must eventually be recorded?
8. What donor assumptions must be rejected, source-localized, quarantined, or escalated?

## 15. Reserved open areas

D04 deliberately leaves the following to later files:

- exact numeric Expression Grade ceilings;
- exact scope/range/duration values;
- exact Development Pick count modifiers from optional subsystems;
- exact skill rank names;
- exact Path/Class/Dao feature designs;
- exact Power Economy cost math;
- exact injury, crippling, and death tables;
- exact capstone harm tables;
- exact Ascension Access procedure beyond eligibility and posture;
- final player-facing sourcebook terminology for every UI label.
