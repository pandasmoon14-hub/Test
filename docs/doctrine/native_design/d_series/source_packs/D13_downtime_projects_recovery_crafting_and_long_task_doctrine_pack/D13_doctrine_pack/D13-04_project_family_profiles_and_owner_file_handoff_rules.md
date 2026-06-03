# D13-04 — Project Family Profiles and Owner-File Handoff Rules

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra give each Project family enough procedural identity to be useful without turning D13 into a megafile that owns recovery math, crafting recipes, research truth, faction operations, or economy rules?

D13-04 defines Project Family Profiles. A Project Family Profile is a routing and procedure template. It identifies the usual goal, requirements, progress signals, complications, partial outcomes, and owner-file handoffs for a type of long task. It is not a full subsystem.

## Profile structure

Each Project Family Profile should include:

- purpose;
- usual goals;
- common requirements;
- usual interval scale;
- typical progress signals;
- common complications;
- partial completion examples;
- failure risks;
- primary owner-file handoffs;
- source-local retention risks;
- quarantine / escalation triggers.

Profiles support conversion and doctrine routing. They do not define final mechanics.

## Recovery Project Profile

Family key: `recovery`

Used for recovery from injury, condition, corruption, fatigue, backlash, instability, exposure, disease-like affliction, poison-like affliction, or other actor-state impairment.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D07 harm, conditions, corruption, recovery limits;
- D08 actor/substrate/form-state when body continuity or personhood matters;
- D03 resource/backlash if recovery interacts with instability, overdraw, or recharge;
- D10 world-state if recovery creates debt, scrutiny, relationship pressure, or institutional consequence;
- D11 presentation;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not import long rest, short rest, hit point reset, sanity recovery, cultivation stabilization, or cyberware recovery rules as Astra defaults.

## Training Project Profile

Family key: `training`

Used for learning, drilling, mentorship, competency improvement, access preparation, route refinement, Technique practice, profession development, or institutional instruction.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D04 advancement, breakthrough, gates, proof;
- D05 methods, skill, competency, training procedure;
- D06 route, Technique, Principle, oath, domain relevance;
- D10 institutions, mentors, obligations, reputation;
- D15 faction/institution operations later;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not allow training to bypass advancement gates or grant competencies, Techniques, access, or advancement payloads without owner-file support.

## Research Project Profile

Family key: `research`

Used for study, investigation over time, clue synthesis, text analysis, experimentation, doctrine reconstruction, cultural study, technical analysis, relic interpretation, or hidden-truth inquiry.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D05 research methods and procedure;
- D10 information-state, hidden truth, rumors, public belief, unresolved pressure;
- D11 hidden-state presentation;
- D09 object/relic/tool state when studying objects;
- D06 route/domain/Technique interpretation if power expression is involved;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not reveal hidden state simply because a research interval completed.

## Crafting Project Profile

Family key: `crafting`

Used for making objects, tools, consumables, gear, relic housings, materials, components, mundane items, special devices, or source-local crafted assets.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D09 objects, relics, tools, materials, object-state;
- D17 economy, acquisition, ownership, market, scarcity, reward/requisition;
- D05 crafting method and competency relevance;
- D03 resource costs if crafting uses pools, charges, overdraw, or instability;
- D06 if crafting embeds Technique/domain/power expression;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not invent recipes, item powers, enhancement rules, material grades, or donor crafting formulas.

## Salvage Project Profile

Family key: `salvage`

Used for extracting useful material, parts, relic fragments, information, fuel, components, biological samples, platform systems, battlefield remains, wreckage, dungeon remnants, or source-local resources.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D09 salvage state, object fragments, materials;
- D17 ownership, salvage rights, legality, market value, requisition;
- D07 hazards or contamination if salvage is dangerous;
- D10 faction/law/world pressure if salvage has claims or witnesses;
- D14 location/exploration handoff when salvage depends on site procedure;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not let salvage become free loot generation.

## Repair Project Profile

Family key: `repair`

Used for restoring, stabilizing, patching, rebuilding, maintaining, or refitting objects, platforms, facilities, tools, implants, armor, vehicles, ships, mechs, or damaged infrastructure.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D09 object/platform state;
- D17 materials, cost, acquisition, requisition;
- D05 repair method and competency;
- D03 resource strain or recharge if applicable;
- D07 harm/safety if unsafe repair threatens actors;
- D14/D15/D18 if repair affects travel, faction infrastructure, or long-horizon state;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not collapse repair into automatic object reset after downtime.

## Installation Preparation Project Profile

Family key: `installation_preparation`

Used for preparing an implant, relic socket, platform module, ship upgrade, cybernetic modification, biotech procedure, attunement housing, hardpoint, or body/object integration.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D09 installable assets, object/platform integration;
- D08 actor substrate, body/form-state, personhood risk;
- D07 harm, rejection, corruption, recovery, condition risk;
- D03 cost/backlash/instability;
- D06 power expression compatibility if relevant;
- D17 acquisition, legality, scarcity;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not import donor essence, humanity, attunement, implant slot, hardpoint, or augmentation metaphysics as Astra defaults.

## Resource-Gathering Project Profile

Family key: `resource_gathering`

Used for acquiring materials, cultivation resources, rare reagents, supplies, data, fuel, contacts, favors, licenses, salvage rights, labor, or infrastructure access.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D17 acquisition, scarcity, requisition, market, legality, ownership;
- D10 relationships, factions, law, economy pressure;
- D14 exploration/travel if resources require field activity;
- D05 method/competency;
- D09 material or object-state when resources are physical;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not make resources appear merely because downtime was spent.

## Social Project Profile

Family key: `social_project`

Used for reputation repair, relationship cultivation, trust rebuilding, rumor management, obligation negotiation, patron work, contact development, public image, or influence preparation.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D10 relationships, reputation, rumors, public belief, hidden truth, law, trace;
- D15 faction/relationship/institution operations later;
- D05 methods and social competency relevance;
- D11 presentation and hidden-state boundaries;
- D17 favors, debts, obligations, payment, requisition if relevant;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not treat social projects as mind control or automatic loyalty, belief, emotion, or obedience changes.

## Faction-Support Project Profile

Family key: `faction_support`

Used for helping, hindering, preparing, infiltrating, organizing, funding, recruiting for, repairing ties with, or executing support work for institutions and organized groups.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D10 faction state, unresolved pressure, reputation, law, information;
- D15 faction and institutional operations later;
- D17 resources, requisition, obligations, economy pressure;
- D05 methods;
- D14 if activity requires travel or site work;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not turn D13 into arbitrary faction AI or a universal faction-turn system.

## Preparation Project Profile

Family key: `preparation`

Used for preparing a future scene, ritual, expedition, defense, infiltration, public action, platform operation, legal case, negotiation, or breakthrough attempt.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D03 resources;
- D04 advancement/breakthrough if preparation supports transformation;
- D05 methods;
- D06 Techniques/domain expression;
- D09 objects/platforms/tools;
- D10 information/world-state;
- D14 travel/exploration;
- D15 factions;
- D17 acquisition;
- D18 campaign pacing if long horizon;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not turn preparation into unlimited future advantage.

## Maintenance Project Profile

Family key: `maintenance`

Used for upkeep, stabilization, recurring repair, supply preservation, facility operation, platform service, implant care, companion care, domain support, or ongoing burden.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- D09 objects/platforms/facilities;
- D17 economy, supply, requisition, upkeep;
- D08 actors/companions/substrate when living or semi-living support is involved;
- D10 institutional/world pressure;
- D18 long-horizon continuity and state aging;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not ignore maintenance burden or make it punitive bookkeeping without purpose.

## Special / Source-Local Project Profile

Family key: `special_source_local`

Used for bounded donor project systems that are useful inside a converted source but unsafe to generalize.

Typical requirements may include time, safe location, method, access, materials, facility support, assistants, information, permission, resource cost, and source-local prerequisites as appropriate.

Typical progress signals may include requirement satisfaction, stage completion, stabilization, useful partial outcome, reduced future cost, improved access, recovered function, better posture, or owner-file state handoff.

Common complications may include delay, cost increase, material loss, hidden pressure surfacing, assistant risk, facility strain, social scrutiny, object instability, injury setback, legal exposure, faction attention, or source-local threat.

Primary owner-file handoffs:

- source-local boundary;
- the relevant owner files by function;
- canon review only if later promoted;
- lexicon review for donor terms;
- D10/D11 if hidden information is involved;

Boundary rule: D13 owns the Project interval and routing; the listed owner files own their own state content and mechanics.

Anti-drift rule: Do not generalize a source-local project system through polish, repetition, or donor familiarity.


## Profile-level source-local rule

Special donor project systems may be retained source-locally when useful, bounded, and unsafe to generalize. The retained procedure must record:

- source-local boundary;
- preserved elements;
- stripped donor assumptions;
- rejected imports;
- owner-file handoffs;
- confidence;
- canon review condition if reuse is proposed later.

## Mixed Project rule

A mixed Project declares one primary Project family and secondary pressure families. If the Project includes distinct goals with different owners, split it into linked Projects. Do not create a single mega-Project that hides multiple lawful outcomes.

## Anti-drift controls

- Recovery profile does not import rest/reset mechanics.
- Training profile does not grant advancement by itself.
- Research profile does not reveal hidden truth.
- Crafting profile does not create unsupported powers.
- Salvage profile does not generate free rewards.
- Installation preparation does not import donor body/soul/essence metaphysics.
- Social projects do not decide loyalty, belief, emotion, or speech.
- Faction-support projects do not become faction AI.
- Preparation does not create unlimited future advantage.
- Maintenance remains purposeful support-burden doctrine, not incidental bookkeeping.
