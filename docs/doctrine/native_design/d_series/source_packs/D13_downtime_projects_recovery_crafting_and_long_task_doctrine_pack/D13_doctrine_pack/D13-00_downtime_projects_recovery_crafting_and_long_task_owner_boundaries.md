# D13-00 — Downtime, Projects, Recovery, Crafting, and Long-Task Owner Boundaries

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra handle meaningful work that takes more than a single action window, exchange, or scene, while preserving cost, progress, interruption, consequence, and owner-file boundaries?

D13 is the doctrine layer for interval-scale work. It governs recovery, training, research, crafting, repair, salvage, social projects, faction-support projects, preparation, resource gathering, maintenance, and source-local long-task systems without importing donor downtime turns, crafting recipes, healing days, faction clocks, or project clocks as Astra defaults.

## Why D13 exists after D12

D12 defines cadence states, action windows, exchanges, intervals, and time-scale shifts. D12 determines when scene time becomes interval handling. D13 determines what happens after that handoff.

Without D13, long tasks drift into donor assumptions: long rest recovery, short rest recovery, fixed downtime activity menus, crafting by exact currency per day, research as one skill check, training as automatic advancement, project clocks as universal procedure, salvage as automatic reward generation, and maintenance as either invisible or punitive bookkeeping.

D13 prevents that drift through a Project-Centered Interval Architecture.

## What D13 owns

D13 owns:

- downtime intervals;
- Project creation;
- Project scope;
- Project progress;
- Project stages and lifecycle states;
- recovery interval handling;
- training interval handling;
- research interval handling;
- crafting Project handling;
- salvage Project handling;
- repair Project handling;
- installation-preparation Project handling;
- resource-gathering Project handling;
- social Project handling;
- faction-support Project handling;
- preparation and maintenance Projects;
- assistants and contributors as Project support;
- facilities as Project support;
- materials and support assets as Project requirements, commitments, risks, or outputs;
- costs and access requirements as Project inputs;
- Project interruption, pause, resume, abandonment, and archive;
- Project complication classification;
- concurrent Project capacity through Project Load;
- source-local downtime and long-task systems;
- conversion-facing mapping of donor long-task procedures.

D13 defines how a long task is created, what it needs, how intervals are committed, how progress is checked when needed, how partial progress works, how complications route, and when the Project hands off to another owner.

## What D13 must not own

D13 must not own:

- D02 resolution math, outcome bands, natural 20/natural 1 handling, or opposed-check procedure;
- D03 resource pool definitions, recharge rules, overdraw rules, or resource-side backlash content;
- D04 advancement gates, proof, breakthroughs, transformations, or advancement payloads;
- D05 full skill/method taxonomy, competency list, or research truth procedure;
- D06 Technique, Principle, oath, route, domain, or power-expression mechanics;
- D07 harm taxonomy, injury definitions, condition math, corruption model, healing limits, relapse, death risk, or recovery-state content;
- D08 actor/personhood/substrate doctrine;
- D09 final object, relic, platform, implant, material, salvage, crafting, repair, or installation state;
- D10 world-state contents, relationships, public belief, hidden truth, law, economy pressure, or unresolved pressure queues;
- D11 narration, hidden-state presentation, player-facing summaries, or GM-facing summaries;
- D12 scene cadence, action windows, initiative, exchanges, reactions, or interruptions;
- D14 travel, navigation, exploration, discovery, journey risk, or route procedure;
- D15 faction action, institutional operations, diplomacy, treaties, faction conflict, or faction AI;
- D17 acquisition, ownership, value, scarcity, licenses, markets, requisition, reward, inventory, or economy procedure;
- D18 campaign arcs, seasons, state aging, pressure retirement, archive vs active state, advancement pacing, or long-horizon campaign continuity;
- final runtime implementation or database schema;
- final sourcebook prose;
- live-play GM behavior.

D13 may call these files. It may not absorb their authority.

## Dependencies

D13 depends on:

- D00 for the principle that meaningful action commits tracked deltas;
- D02 for resolution when uncertainty, opposition, risk, or consequence exists;
- D03 for resource/cost/overdraw/backlash interfaces;
- D04 for advancement, breakthrough, and transformation gates;
- D05 for skills, methods, competency, research, and training relevance;
- D06 for route, Technique, Principle, oath, and domain expression boundaries;
- D07 for recovery, injury, harm, corruption, and condition consequences;
- D08 for actor/substrate/personhood and body/form-state implications;
- D09 for objects, relics, platforms, implants, crafting object-state, salvage, materials, and repairs;
- D10 for world-state, relationships, reputation, law, economy pressure, information-state, rumors, and unresolved pressure;
- D11 for presentation and hidden-state surfacing;
- D12 for interval handoff from scene cadence;
- D15/D17/D18 as downstream procedure owners for faction operations, economy/acquisition, and campaign continuity.

## Core architecture

D13 uses Project-Centered Interval Architecture:

```text
D12 time-scale shift into interval
  -> Project declaration
  -> Project scope and family classification
  -> requirement and cost identification
  -> interval commitment
  -> progress / complication / interruption resolution
  -> Project outcome
  -> owner-file state handoff
  -> active / archived / retired Project status
```

## Definition of Project

A Project is any goal requiring interval-scale commitment, requirements, progress, risk, or delayed state consequence.

A Project is not only a downtime activity. A Project may occur between adventures, during travel, during recovery, during faction work, during a siege, during a long ritual, while docked at a shipyard, inside a sect, across a campaign season, or inside a source-local procedure.

## Project families are routing categories

Project families identify the likely owner-file handoffs. They are not a fixed menu of allowed downtime actions.

The core D13 families are:

- recovery;
- training;
- research;
- crafting;
- salvage;
- repair;
- installation preparation;
- resource gathering;
- social projects;
- faction-support projects;
- preparation;
- maintenance;
- special / source-local projects.

A Project may have one primary family and secondary pressure families. If a proposed Project contains separate goals requiring different owner files, D13 should split it into linked Projects rather than flattening it.

## Donor-family pressure coverage

D13 is designed to absorb pressure from:

- d20/class-level rest, crafting, training, downtime activity, spell recovery, and gold-per-day systems;
- OSR recovery, hireling, expedition downtime, stronghold, disease, and treasure-development loops;
- lifepath/career service terms, aging, contacts, debts, institutional training, and asset work;
- skill-pool/cyberpunk surgery, cyberware installation, lifestyle maintenance, black-market legwork, stress recovery, and repair cycles;
- narrative/tag project clocks, montage rules, collaborative facts, and metacurrency-driven downtime;
- cultivation/LitRPG seclusion, breakthrough preparation, resource refinement, technique study, body tempering, sect training, and backlash recovery;
- crafting/salvage-heavy recipes, material grades, disassembly, repairs, upgrades, batch production, and item quality;
- vehicle/mech/ship repairs, refits, docking, maintenance, crew support, requisition, and salvage rights;
- faction/domain/kingdom construction, recruitment, treaties, propaganda, espionage preparation, and institutional Projects;
- horror/investigation research, hidden corruption, clue analysis, rest under pressure, and escalating threats.

## Anti-drift rules

D13 must not:

- treat downtime as a fixed activity menu;
- make project clocks universal;
- import rest recovery as Astra recovery;
- let training bypass D04/D05/D06 gates;
- let research reveal protected truth automatically;
- let crafting produce unsupported object powers;
- let salvage become free reward generation;
- treat assistants, facilities, or materials as generic free bonuses;
- allow unlimited concurrent background progress;
- become D15 faction AI, D17 economy doctrine, or D18 campaign pacing;
- generalize source-local donor long-task systems by repetition alone;
- treat its not-final record shapes as runtime schemas.

## Acceptance criteria for D13-00

D13-00 is successful if it clearly establishes:

- D13 owns interval-scale Project procedure;
- D13 does not own downstream mechanical content;
- D12 hands interval time to D13 but does not decide D13 progress;
- Project families are routing categories, not fixed actions;
- all donor long-task procedures require lawful outcome handling;
- no donor rest, crafting, training, recovery, faction, clock, cultivation, cyberware, or salvage procedure becomes Astra law by label.
