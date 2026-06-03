# D13 Combined Doctrine Pack — Downtime, Projects, Recovery, Crafting, and Long-Task Procedure

Generated: 2026-06-02



---

<!-- BEGIN D13-README_manifest.md -->

# D13 — Downtime, Projects, Recovery, Crafting, and Long-Task Doctrine Pack

**README manifest**

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Purpose

D13 defines Astra's interval-scale procedure for meaningful work that takes more than a single action window, exchange, or scene. It covers Project creation, requirement discovery, cost and risk commitment, progress, complications, interruption, abandonment, concurrent work, contributors, facilities, materials, maintenance, source-local donor long-task systems, and owner-file handoff.

D13 builds directly on D12. D12 determines when scene time becomes interval handling. D13 determines what happens inside that interval. D13 must not expand backward into D12 scene cadence and must not expand forward into D14 travel, D15 faction operations, D17 economy/requisition, or D18 campaign pacing.

## Locked architecture summary

D13 uses **Project-Centered Interval Architecture**.

A Project is any goal requiring interval-scale commitment, requirements, progress, risk, or delayed state consequence. Project families are routing categories, not fixed downtime menu actions.

Core Project families:

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

Core progress model: **Interval Outcome States**, not universal project clocks. Numeric progress is allowed only when an owner file, source-local procedure, or later schema supports it.

Core concurrency model: **Project Load**, not universal Project slots.

## Pack contents

1. `D13-00_downtime_projects_recovery_crafting_and_long_task_owner_boundaries.md`
2. `D13-01_project_anatomy_project_families_and_lifecycle_states.md`
3. `D13-02_project_creation_requirement_discovery_commitment_and_interval_setup.md`
4. `D13-03_progress_interval_outcomes_complications_and_partial_completion.md`
5. `D13-04_project_family_profiles_and_owner_file_handoff_rules.md`
6. `D13-05_concurrent_projects_contributors_facilities_materials_and_support_burden.md`
7. `D13-06_source_local_downtime_donor_project_mapping_quarantine_and_escalation.md`
8. `D13-07_records_not_final_schema_and_conversion_handoff_shapes.md`
9. `D13-09_integration_checklists_ddr_register_and_acceptance_criteria.md`
10. `D13_pack_manifest.json`
11. `D13_combined_downtime_projects_recovery_crafting_and_long_task_doctrine.md`

## Authority and phase separation

D13 obeys the Astra authority hierarchy:

1. current Astra doctrine files;
2. canonical Astra sourcebook material once formalized;
3. converted Astra-native donor content;
4. example packs / training examples;
5. original donor assumptions.

D13 does not make donor downtime systems canon. It does not treat conversion output as canon. It does not authorize runtime state mutation. It does not replace D11 presentation or a later play-facing adapter.

## Minimum use rule

During conversion intake, a donor long-task construct must be handled through one lawful outcome:

- direct Astra mapping;
- normalized Astra mapping;
- source-local retained construct;
- quarantined construct pending later doctrine;
- escalated doctrine problem.

D13 provides routing doctrine for long-task constructs. It does not create a sixth outcome.

## Embedded risk controls

This pack embeds the D13 risk audit directly into owner boundaries, progress rules, project profiles, donor mapping, records, and final control checklists. The main controls are:

- Project families are routing categories, not a downtime menu.
- Project clocks are not universal.
- Recovery does not import rest/reset assumptions.
- Training does not bypass D04/D05/D06.
- Research does not reveal protected hidden truth automatically.
- Crafting does not create unsupported powers or objects.
- Salvage does not generate free rewards.
- Contributors, facilities, and materials require role/function and may create burden.
- Concurrent Projects require capacity support through Project Load.
- D13 does not become D15 faction AI, D17 economy doctrine, or D18 campaign pacing.
- Source-local donor downtime systems do not generalize without review.
- Record shapes are not final runtime schemas.


<!-- END D13-README_manifest.md -->


---

<!-- BEGIN D13-00_downtime_projects_recovery_crafting_and_long_task_owner_boundaries.md -->

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


<!-- END D13-00_downtime_projects_recovery_crafting_and_long_task_owner_boundaries.md -->


---

<!-- BEGIN D13-01_project_anatomy_project_families_and_lifecycle_states.md -->

# D13-01 — Project Anatomy, Project Families, and Lifecycle States

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra define a Project clearly enough that recovery, research, training, crafting, repair, salvage, faction work, social campaigns, and special long tasks all use one stable interval grammar without collapsing into one generic downtime action?

D13-01 defines the parts of a Project and the lifecycle states a Project can occupy. It does not define final crafting recipes, healing values, training progression, research truth, faction actions, economy prices, or campaign pacing.

## Project anatomy

A Project has these minimum elements:

1. Goal
2. Project family
3. Scope
4. Interval scale
5. Requirements
6. Method
7. Contributors
8. Support assets
9. Costs and exposure
10. Progress state
11. Complication state
12. Outcome handoff
13. Source-local boundary, if any

These elements are doctrine-facing. Later schema files or runtime Gate B may formalize them differently, but the semantic controls remain required.

## 1. Goal

The goal is the intended delayed result. A valid Project goal identifies an intended state change or delayed consequence.

Examples:

- recover from a severe wound;
- stabilize corruption after backlash;
- train a new competency;
- study a sealed doctrine fragment;
- repair a damaged ship drive;
- craft a relic housing;
- salvage usable materials from a wreck;
- rebuild trust with a faction;
- prepare a ritual site;
- gather cultivation resources;
- maintain a platform through a hostile season.

If the goal has no possible state change or delayed consequence, it may be ordinary free play or narration rather than a Project.

## 2. Project family

The project family is the routing category that identifies likely owner-file handoffs. It is not a fixed activity menu.

Core families:

- `recovery`
- `training`
- `research`
- `crafting`
- `salvage`
- `repair`
- `installation_preparation`
- `resource_gathering`
- `social_project`
- `faction_support`
- `preparation`
- `maintenance`
- `special_source_local`
- `mixed`

A mixed Project declares one primary family and secondary pressure families. If a mixed Project contains distinct goals requiring different owners, split it into linked Projects.

## 3. Scope

Scope describes the size, risk, complexity, and consequence level of the Project.

Use these bands:

| Scope band | Meaning |
|---|---|
| `minor` | Short, bounded, low-risk, limited consequence. |
| `standard` | Meaningful cost or progress across one or more intervals. |
| `major` | Significant resource, facility, risk, or owner-file handoff. |
| `extended` | Multi-stage, high-impact, or campaign-relevant. |
| `transformational` | Alters identity, route, faction, world-state, object-state, or campaign posture. |

Scope is not a fixed duration formula. Scope controls review depth, required support, and owner-file involvement.

## 4. Interval scale

Interval scale is the time unit at which progress is checked or maintained.

Allowed interval scales include:

- hours;
- days;
- weeks;
- months;
- season;
- travel leg;
- recovery block;
- facility cycle;
- source-local interval;
- other declared interval.

D13 supports flexible interval scale. It does not set universal downtime lengths. D18 later owns campaign-scale pacing, seasons, state aging, and long-horizon time compression.

## 5. Requirements

Requirements are what the Project needs before it can begin, continue, accelerate, or complete.

Requirement categories:

- time;
- safe location;
- materials;
- tools;
- facility;
- assistant;
- access tag;
- method / competency;
- resource cost;
- information;
- permission / license;
- reputation / standing;
- body condition;
- object condition;
- route / Technique / domain prerequisite;
- source-local prerequisite;
- other.

Requirements are identified before commitment when knowable. Hidden requirements may be marked protected rather than revealed.

## 6. Method

Method describes how the Project is pursued. D05 owns skills, methods, research, procedure, training, and competency relevance. D13 only requires a method when method affects progress, risk, requirements, or outcome.

A method may affect:

- whether the Project is feasible;
- which requirement matters;
- which attribute or competency applies if a D02 check is needed;
- whether complications are likely;
- whether source-local procedure can be retained;
- which owner file receives the outcome.

## 7. Contributors

Contributors are actors or organized supports that participate in the Project.

Contributor roles may include:

- primary worker;
- assistant;
- mentor;
- specialist;
- crew;
- guard;
- sponsor;
- supplier;
- research aide;
- ritual participant;
- patient;
- test subject;
- faction representative;
- facility operator;
- companion / summon;
- automated system;
- source-local contributor.

Contributors are not free progress multipliers. A contributor must have a valid role and may create cost, obligation, scrutiny, risk, coordination burden, safety exposure, loyalty risk, or information leakage.

## 8. Support assets

Support assets include materials, tools, facilities, platforms, licenses, access tags, funding, favors, stored resources, legal permissions, and automated systems.

D13 records these as Project requirements, commitments, risks, or outputs. D09 and D17 own their object/economy state.

## 9. Costs and exposure

Costs and exposure may include:

- time;
- materials;
- resource pools;
- wealth / requisition / favors;
- risk exposure;
- instability;
- fatigue;
- injury risk;
- scrutiny;
- relationship strain;
- opportunity cost;
- facility occupation;
- maintenance burden;
- source-local cost.

D03, D07, D10, and D17 own the content of those costs where relevant. D13 owns the commitment checkpoint and Project record.

## 10. Progress state

D13 uses lifecycle/progress states rather than universal clocks by default.

Progress states:

- `not_started`
- `ready`
- `active`
- `progressing`
- `blocked`
- `complicated`
- `paused`
- `interrupted`
- `completed`
- `completed_with_complication`
- `failed`
- `abandoned`
- `quarantined`
- `escalated`
- `archived`

Numeric progress may be used only when an owner file, source-local procedure, or later schema supports it.

## 11. Complication state

Complications may include:

- cost increase;
- delay;
- material loss;
- tool or facility damage;
- assistant risk;
- injury or condition setback;
- corruption or instability pressure;
- object instability;
- social scrutiny;
- faction attention;
- legal exposure;
- information false lead;
- hidden pressure surface;
- source-local threat;
- active scene trigger;
- owner-file gap.

D13 classifies complications and routes them. It does not invent final state outside its ownership.

## 12. Outcome handoff

Project outcomes must route to the correct owner file. Examples:

- D07 for recovery, injury, condition, corruption, relapse, and healing-state changes;
- D04/D05/D06 for training, advancement gates, competency posture, route or Technique development;
- D05/D10/D11 for research, information-state, hidden truth, public belief, rumor, and presentation;
- D09 for crafted, repaired, salvaged, installed, modified, or unstable objects;
- D17 for acquisition, value, ownership, market, scarcity, requisition, and legality;
- D10/D15 for relationship, reputation, faction, law, institutional, trace, and social-state effects;
- D18 for long-horizon continuity, aging, archive, pressure retirement, and season/campaign state.

D13 records the handoff and does not decide the downstream content.

## 13. Source-local boundary

A source-local Project system may be retained only with explicit boundary notes.

Source-local boundary notes should state:

- what source/campaign/location/faction/object/ritual bounds the procedure;
- what elements are preserved;
- what elements are not generalized;
- which donor assumptions are rejected;
- what would be required for later canon review.

## Examples

### Example: Repairing a damaged skiff

- Goal: restore skiff function enough for travel.
- Family: repair.
- Scope: standard or major depending damage.
- Requirements: safe location, tools, parts, method, time.
- Owner handoffs: D09 object/platform state, D17 parts/acquisition, D14 if travel is blocked.

### Example: Secluded cultivation preparation

- Goal: prepare body and route posture for a later breakthrough attempt.
- Family: training or preparation; possible special/source-local.
- Scope: major, extended, or transformational.
- Requirements: safe site, mentor, resource, method, route prerequisite.
- Owner handoffs: D04, D06, D07, D10, D18 as needed.
- Donor seclusion timings do not become universal Astra pacing.

## Anti-drift controls

- Do not treat a project family as a fixed activity option.
- Do not allow a Project with no intended state change or delayed consequence.
- Do not make scope equal exact time.
- Do not let contributors or support assets grant generic bonuses without role and burden.
- Do not treat progress state as final owner-file content.


<!-- END D13-01_project_anatomy_project_families_and_lifecycle_states.md -->


---

<!-- BEGIN D13-02_project_creation_requirement_discovery_commitment_and_interval_setup.md -->

# D13-02 — Project Creation, Requirement Discovery, Commitment, and Interval Setup

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra start a Project lawfully?

D13-02 defines the procedure for turning actor or world intent into a valid interval-scale Project without guessing missing requirements, skipping costs, revealing hidden state, or letting donor downtime procedure decide Astra law.

## Project setup procedure

A Project begins through eight setup checkpoints:

1. Intent checkpoint
2. Goal checkpoint
3. Project family checkpoint
4. Scope checkpoint
5. Requirement discovery checkpoint
6. Cost / risk preview checkpoint
7. Commitment checkpoint
8. Interval setup checkpoint

This setup procedure applies to all Project families, including recovery, training, research, crafting, salvage, repair, social work, faction support, maintenance, and special/source-local Projects.

## 1. Intent checkpoint

The actor declares what they want to accomplish over interval-scale time.

Examples:

- “I want to repair the damaged skiff.”
- “I want to recover from the corruption backlash.”
- “I want to study the relic inscriptions.”
- “I want to train under the sect’s blade elder.”
- “I want to craft a stabilizing housing for this core.”
- “I want to rebuild my reputation with the harbor guild.”
- “I want to salvage the crashed platform.”

At this checkpoint, D13 captures intent. It does not yet decide feasibility or success.

## 2. Goal checkpoint

The goal must be clarified enough to know what success would change.

A valid goal identifies at least one intended state change or delayed consequence:

- actor state;
- condition / injury / corruption state;
- competency / training posture;
- information state;
- object state;
- resource/material state;
- relationship state;
- faction or institutional state;
- location/facility state;
- campaign pressure state;
- source-local state.

If the goal has no possible state change, it may remain ordinary narration or free play.

## 3. Project family checkpoint

D13 assigns one primary Project family and any secondary pressure families.

Example:

```yaml
project_family_classification:
  primary_family: repair
  secondary_families:
    - salvage
    - resource_gathering
    - technical_research
  likely_owner_files:
    - D05
    - D09
    - D17
```

A mixed Project should not be flattened. If it contains distinct goals requiring different owner files, D13 should split it into linked Projects.

## 4. Scope checkpoint

Assign a provisional scope band:

- minor;
- standard;
- major;
- extended;
- transformational.

Scope is based on:

- intended state change;
- risk;
- rarity of requirements;
- number of owner files involved;
- source-local complexity;
- campaign impact;
- whether identity, faction, object, route, or world-state changes are possible.

Scope may change after requirement discovery.

## 5. Requirement discovery checkpoint

Determine what is known, unknown, missing, blocked, or protected.

Requirement status vocabulary:

| Status | Meaning |
|---|---|
| `met` | Requirement is available and usable. |
| `missing` | Requirement is known but absent. |
| `unknown` | Requirement may exist but has not been discovered. |
| `protected_hidden` | Requirement exists or may exist, but revealing it would violate hidden-state boundaries. |
| `blocked_by_owner_file` | Requirement cannot be resolved without another doctrine owner. |
| `source_local` | Requirement is valid only inside a bounded source-local procedure. |
| `quarantined` | Requirement cannot be handled safely with current evidence or doctrine. |

D13 may mark a requirement as `protected_hidden` without revealing it. Discovery of protected requirements requires appropriate D05/D10/D11-supported procedure.

## 6. Cost / risk preview checkpoint

Before commitment, the actor should receive visible costs and risks when knowable.

Possible visible previews:

- time required;
- materials likely required;
- resource or wealth pressure;
- facility occupation;
- assistant or crew requirement;
- risk of worsening condition;
- risk of object damage;
- risk of social scrutiny;
- risk of faction attention;
- risk of corruption / instability;
- chance of incomplete result;
- need for further owner-file review.

Hidden risks remain protected by D10/D11 or the relevant owner file.

## 7. Commitment checkpoint

The actor commits to the Project.

Commitment may include:

- time block;
- materials reserved;
- facility claimed;
- assistant assigned;
- resource cost paid or reserved;
- exposure accepted;
- opportunity cost accepted;
- relationship/faction obligation accepted;
- object placed under work;
- actor enters recovery/training/research posture.

Time, materials, facility claims, assistant assignment, resource cost, exposure, and opportunity cost commit before interval progress begins unless an owner file or source-local rule says otherwise.

D13 should not allow “wait to see if the Project succeeds before paying” unless another owner file explicitly permits it.

## 8. Interval setup checkpoint

The Project enters its first interval.

D13 records:

- interval scale;
- next progress check or condition for progress check;
- active requirements;
- open unknowns;
- owner-file handoffs;
- interruption risks;
- Project status;
- state affected if abandoned;
- source-local boundaries.

## Setup outcomes

Requirement discovery and setup produce one of five outcomes.

| Outcome | Meaning |
|---|---|
| `ready_to_begin` | Requirements, cost preview, and owner-file support are sufficient to enter interval handling. |
| `ready_with_risk` | Project can begin, but incomplete information, unstable conditions, poor facilities, insufficient materials, scrutiny, or similar risk is declared. |
| `blocked_pending_requirement` | Project cannot begin until a missing requirement is satisfied. |
| `quarantined_pending_doctrine_or_evidence` | Project cannot begin because evidence or doctrine cannot support it safely. |
| `escalated_owner_file_problem` | Project exposes a missing doctrine area requiring owner-file action. |

## Blocked pending requirement examples

- no safe recovery location;
- missing material;
- no relevant access tag;
- facility unavailable;
- object too damaged to work safely;
- information insufficient;
- faction permission absent;
- assistant required but unavailable.

## Quarantine examples

- donor cyberware surgery system before installation doctrine exists;
- broken crafting table with missing material rows;
- ritual Project dependent on unsupported metaphysics;
- time-loop training procedure with no causality doctrine;
- unclear donor recovery procedure from damaged extraction.

## Escalation examples

- D07 lacks recovery distinction needed for repeated donor injury systems;
- D09 lacks object-state rules for repair/refit conversion;
- D15 lacks institutional Project operation needed for faction-scale work;
- D17 lacks requisition/access procedure for recurring military, sect, or corporate supply systems;
- D18 lacks long-horizon state-aging rules for decade-scale cultivation Projects.

## Hidden requirement rule

D13 may record that a hidden requirement is present, suspected, or protected without revealing it. A player-facing view should not receive hidden backend facts simply because a Project setup procedure exists.

D11 presentation and D10 information-state boundaries control what is surfaced.

## Anti-drift controls

- Do not start vague Projects that lack intended state change.
- Do not reveal protected hidden requirements.
- Do not bypass owner-file prerequisites.
- Do not commit only after success unless permitted.
- Do not normalize donor setup costs into Astra without owner-file support.


<!-- END D13-02_project_creation_requirement_discovery_commitment_and_interval_setup.md -->


---

<!-- BEGIN D13-03_progress_interval_outcomes_complications_and_partial_completion.md -->

# D13-03 — Progress, Interval Outcomes, Complications, and Partial Completion

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra determine what happens during each Project interval without forcing every Project into a universal progress clock, fixed downtime table, or binary success/failure result?

D13-03 defines how Projects advance, stall, complicate, partially complete, fail, accelerate, or hand off across intervals. It does not define final recovery values, item crafting math, research truth, training advancement, faction operations, market acquisition, or campaign-season pacing.

## Core progress model

D13 uses **Interval Outcome States** rather than universal progress points or clocks.

Each interval can produce one of these outcomes:

- `advanced`
- `advanced_with_cost`
- `partial`
- `stalled`
- `blocked`
- `complicated`
- `damaged`
- `interrupted`
- `completed`
- `completed_with_complication`
- `failed`
- `abandoned`
- `quarantined`
- `escalated`

Owner files decide what each outcome means for the state they own.

## Progress is not always numeric

A Project may advance by:

- stage completion;
- requirement satisfaction;
- risk reduction;
- evidence discovery;
- object-state improvement;
- condition stabilization;
- relationship repair;
- material accumulation;
- facility preparation;
- training posture improvement;
- route/principle refinement;
- faction access improvement;
- source-local milestone.

Numeric progress is allowed only when an owner file, source-local procedure, or later schema supports it.

## Interval check trigger

An interval check occurs only when uncertainty, opposition, risk, consequence, or source-local procedure requires it.

Triggers include:

- committed interval ends and outcome is uncertain;
- risky method is used;
- requirement is unstable;
- hidden pressure may surface;
- resource or material may be consumed;
- external pressure interrupts;
- progress is contested;
- actor attempts to accelerate;
- actor works under poor conditions;
- source-local procedure calls for a check.

Not every interval requires a roll. D13 calls D02 only when uncertainty, opposition, risk, or consequence exists. D02 owns the roll and outcome math.

## Interval outcome routing

D13 routes interval outcomes by Project family.

| Project family | Likely owner-file routing |
|---|---|
| recovery | D07 for injury, condition, corruption, relapse, recovery limits; D08 if substrate/form-state matters; D03 if backlash/recharge interacts. |
| training | D04/D05/D06 for advancement gate, competency, method, access, route, Technique, or domain implications. |
| research | D05/D10/D11 for methods, information-state, clue handling, hidden truth, rumor, public belief, and presentation. |
| crafting | D09/D17 for object state, material use, ownership, scarcity, and economy; D03/D06 if resource or power expression matters. |
| salvage | D09/D17 for recovered components, legality, scarcity, ownership, and salvage rights. |
| repair | D09 for object/platform state; D07 if unsafe repair threatens actors; D17 for parts/cost. |
| social | D10/D15 for relationship, reputation, standing, law, institution, and faction pressure. |
| faction-support | D10/D15 for faction status, pressure, trace, obligations, and institutional response. |
| preparation | D03/D04/D05/D06/D09/D10/D14/D15/D17/D18 depending target. |
| resource gathering | D17/D10/D14/D09 depending source, location, and ownership. |
| special/source-local | source-local boundary plus owner-file review. |

## Partial completion

Partial completion is a first-class outcome.

It may produce:

- usable but flawed object;
- temporary recovery;
- limited clue;
- reduced cost for later attempt;
- improved requirement status;
- new access route;
- smaller material yield;
- progress toward a later stage;
- relationship thaw but not trust;
- facility prepared but not completed;
- salvage recovered but damaged;
- ritual site stabilized but exposed.

Partial completion should not be treated as failure unless the Project goal specifically required all-or-nothing completion.

## Complication classification

Complications are classified and routed to owner files.

Complication families:

- `cost_increase`
- `delay`
- `material_loss`
- `tool_or_facility_damage`
- `assistant_risk`
- `injury_or_condition_setback`
- `corruption_or_instability_pressure`
- `object_instability`
- `social_scrutiny`
- `faction_attention`
- `legal_exposure`
- `information_false_lead`
- `hidden_pressure_surface`
- `source_local_threat`
- `active_scene_trigger`
- `owner_file_gap`

A complication may trigger a D12 transition into an active scene if immediate response matters.

## Failure handling

D13 distinguishes failure types:

| Failure type | Meaning |
|---|---|
| clean failure | Project does not advance but no extra harm occurs. |
| costly failure | Project fails and consumes cost/material/time. |
| reversible failure | Project can retry after a requirement changes. |
| damaging failure | Project worsens actor, object, world, faction, or source-local state. |
| revealing failure | Project fails but exposes useful information. |
| terminal failure | Project cannot continue without new doctrine, major requirement, or source-local event. |

Failure does not automatically erase all progress unless the Project structure or owner file says it does.

## Acceleration and overcommitment

A player may attempt to accelerate a Project by spending more resources, accepting more exposure, using unsafe methods, invoking Techniques, calling in favors, overworking contributors, using unstable facilities, or compressing interval time.

Acceleration is allowed only when supported by owner files and explicit cost/risk exposure.

Acceleration may produce:

- shorter interval;
- extra progress;
- higher complication risk;
- material waste;
- fatigue or injury;
- object instability;
- social scrutiny;
- resource overdraw;
- backlash;
- source-local consequences.

D03, D07, D09, D10, and D17 own the actual consequences where relevant.

## Donor clock warning

D13 does not use universal project clocks. A donor clock, progress track, faction clock, or downtime track must be mapped by function. It may become source-local, route to D10/D14/D15/D18, or quarantine/escalate if unsupported.

## Anti-drift controls

- Do not reduce every Project to one check.
- Do not make every Project a clock.
- Do not treat partial completion as failure by default.
- Do not invent generic complications without owner-file routing.
- Do not let acceleration bypass cost and risk.
- Do not let failure erase all state unless owner-file support exists.


<!-- END D13-03_progress_interval_outcomes_complications_and_partial_completion.md -->


---

<!-- BEGIN D13-04_project_family_profiles_and_owner_file_handoff_rules.md -->

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


<!-- END D13-04_project_family_profiles_and_owner_file_handoff_rules.md -->


---

<!-- BEGIN D13-05_concurrent_projects_contributors_facilities_materials_and_support_burden.md -->

# D13-05 — Concurrent Projects, Contributors, Facilities, Materials, and Support Burden

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra prevent long-task work from becoming unlimited background progress?

D13-05 defines how many Projects can proceed at once, who can contribute, what facilities and materials do, when support assets matter, and how burden, upkeep, access, and interruption constrain progress.

This file does not define exact carrying capacity, prices, crafting values, facility construction rules, assistant statblocks, or faction labor economies. Those belong to D09, D10, D15, D17, D18, and later runtime/schema files.

## Project Load model

D13 uses **Project Load**, not universal Project slots.

A Project creates load when it occupies or requires:

- actor attention;
- time;
- safe location;
- materials;
- tools;
- facility capacity;
- assistant labor;
- specialist access;
- resource cost;
- object availability;
- social/institutional permission;
- legal exposure;
- maintenance burden;
- opportunity cost;
- world-state vulnerability.

A character, group, facility, faction, or platform may maintain multiple Projects only if each Project has clear capacity support.

Unsupported concurrency causes one or more of:

- blocked setup;
- delayed progress;
- increased cost;
- complication;
- Project split;
- Project pause;
- abandonment pressure;
- quarantine;
- escalation.

D13 does not define numeric load values by default. Later owner files or source-local systems may define them if justified.

## Contributor rule

Contributors can assist Projects only when they have a valid role.

Contributor roles:

- primary worker;
- assistant;
- mentor;
- specialist;
- crew;
- guard;
- sponsor;
- supplier;
- research aide;
- ritual participant;
- patient;
- test subject;
- faction representative;
- facility operator;
- companion / summon;
- automated system;
- source-local contributor.

Contributors may provide:

- method support;
- access permission;
- labor;
- protection;
- materials;
- knowledge;
- facility operation;
- social cover;
- faction authorization;
- risk absorption;
- progress acceleration;
- stability.

Contributors may also create:

- cost;
- obligation;
- scrutiny;
- coordination burden;
- safety risk;
- loyalty risk;
- information leak;
- injury exposure;
- facility strain;
- source-local complication.

D13 rejects “assistant equals free bonus” as default law.

## Facility rule

A Facility is any place or infrastructure that enables, improves, stabilizes, or constrains a Project.

Facility examples:

- workshop;
- forge;
- laboratory;
- library;
- clinic;
- meditation chamber;
- ritual site;
- shipyard;
- dock;
- garage;
- hangar;
- sect training hall;
- guild office;
- data vault;
- safehouse;
- salvage bay;
- hospital venue;
- court chamber;
- source-local site.

D13 classifies facilities by function, not donor label.

Facility functions may include:

- safe recovery;
- controlled experimentation;
- fabrication;
- repair;
- storage;
- containment;
- training;
- research access;
- social legitimacy;
- ritual anchoring;
- platform service;
- material processing;
- legal authorization;
- hidden operation.

Facility status may be:

- available;
- adequate;
- strained;
- unsafe;
- occupied;
- damaged;
- source-local;
- unavailable;
- protected hidden;
- unknown.

D09/D10/D15/D17/D18 own the actual facility record, ownership, legality, cost, faction control, and long-term state.

## Materials and support assets

Materials are not generic currency unless D17 later defines them that way.

Material categories include:

- common material;
- scarce material;
- specialized component;
- relic fragment;
- cultivation resource;
- biological sample;
- salvaged part;
- platform component;
- fuel / charge medium;
- data / information resource;
- social favor;
- legal permit;
- faction authorization;
- source-local material.

Support assets may include tools, kits, vehicles, platforms, assistants, licenses, access tags, facilities, or stored resources.

D13 records materials and support assets as requirements, commitments, risks, or outputs. D09/D17 own object and economy state.

## Maintenance and upkeep

Maintenance is a first-class Project family. Some Projects prevent decay, failure, debt, exposure, injury relapse, object degradation, social collapse, faction deterioration, or platform malfunction.

Maintenance may apply to:

- actor recovery;
- implants / relics;
- ships / vehicles / mechs;
- facilities;
- companions / summons;
- social relationships;
- faction obligations;
- legal status;
- resource stockpiles;
- domain stability;
- source-local burdens.

D13 owns the interval and burden procedure. D17 and D18 later own broader support burden, economy pressure, and long-horizon state aging.

## Interruption and abandonment

A Project may be interrupted by:

- active scene trigger;
- resource loss;
- facility loss;
- assistant withdrawal;
- injury;
- travel;
- attack;
- legal action;
- faction pressure;
- hidden threat;
- material spoilage;
- object instability;
- relationship rupture;
- campaign time skip;
- source-local event.

Interruption outcomes:

- `pause_without_loss`
- `pause_with_decay`
- `delay`
- `cost_increase`
- `progress_loss`
- `requirement_change`
- `complication_added`
- `active_scene_triggered`
- `project_split_required`
- `project_abandoned`
- `project_quarantined`
- `project_escalated`

Abandoned Projects must record what is lost, preserved, exposed, recoverable, archived, or converted into unresolved pressure.

## Examples

### Supported concurrency

A character maintains a long-term research Project requiring weekly check-ins while a workshop handles a repair Project under a specialist. The two Projects can coexist if the actor's attention, facility use, and materials do not conflict.

### Unsupported concurrency

A character attempts severe recovery, intensive training, relic crafting, faction diplomacy, and ship repair during the same short interval. D13 should block, delay, split, complicate, or require support burden rather than allow all Projects to progress freely.

## Anti-drift controls

- Do not create universal project-slot counts.
- Do not ignore attention, facility, material, legal, social, or maintenance burden.
- Do not let support assets provide generic bonuses without function.
- Do not let abandonment erase evidence of unresolved pressure.


<!-- END D13-05_concurrent_projects_contributors_facilities_materials_and_support_burden.md -->


---

<!-- BEGIN D13-06_source_local_downtime_donor_project_mapping_quarantine_and_escalation.md -->

# D13-06 — Source-Local Downtime Systems, Donor Project Mapping, Quarantine, and Escalation

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra convert donor downtime, crafting, recovery, training, Project, clock, faction-turn, and long-task systems without letting donor procedure become Astra default law?

D13-06 defines the conversion-facing rule for donor long-task procedures such as:

- long rests;
- short rests;
- downtime activities;
- crafting by gold/day;
- training periods;
- research checks;
- healing days;
- carousing tables;
- business operation turns;
- faction clocks;
- stronghold turns;
- kingdom turns;
- ship repair cycles;
- cyberware surgery and recovery;
- cultivation seclusion;
- ritual preparation phases;
- travel downtime;
- salvage tables;
- maintenance cycles.

The donor label is evidence only. D13 maps function.

## Functional donor project mapping ladder

Every donor long-task system must pass through this ladder:

1. Identify the donor procedure's function.
2. Identify the interval scale it assumes.
3. Identify what state it changes.
4. Identify what costs, requirements, risks, and interruptions it uses.
5. Identify which Astra owner files are affected.
6. Decide lawful handling:
   - direct Astra mapping;
   - normalized Astra Project mapping;
   - source-local retained procedure;
   - quarantine;
   - escalation.
7. Record rejected donor assumptions.

## Direct Astra mapping

Use direct mapping only when the donor procedure already fits D13 without importing donor-specific timing, cost, advancement, recovery, economy, or metaphysical assumptions.

Example:

A donor rule says a damaged tool can be repaired over a safe interval if the actor has the right tools and materials. This can map directly to a D13 Repair Project, with D09 owning object-state result and D17 owning material/economy pressure if relevant.

## Normalized Astra Project mapping

Use normalized mapping when the donor procedure has a reusable function but donor packaging must be stripped.

Examples:

- A donor long rest becomes a Recovery Project or ordinary rest interval, not an Astra universal recovery reset.
- A donor crafting-by-gold rule becomes a Crafting Project with material, facility, method, and D17 economy handoff.
- A donor research activity becomes a Research Project with D05 method and D10/D11 hidden-information boundaries.
- A donor ship refit cycle becomes a Repair or Maintenance Project with D09/D17/D14 handoffs.

The function survives. The donor math does not become Astra law.

## Source-local retained procedure

Use source-local retention when the donor long-task procedure is useful inside a converted source but unsafe to generalize.

Examples:

- a named sect's seven-stage seclusion method;
- a specific adventure's ritual preparation countdown;
- a local stronghold construction table;
- a donor campaign's faction-turn procedure;
- a specific shipyard refit cycle;
- a local corruption recovery rite;
- a carousing table tied to one city or culture.

The retained system must have a boundary. It cannot become general Astra downtime doctrine by polish, repetition, or familiarity.

## Quarantine

Use quarantine when the donor procedure cannot be mapped safely yet.

Quarantine triggers include:

- extraction damage blocks procedure understanding;
- missing Project requirements;
- missing owner-file support;
- unsupported healing/recovery mechanics;
- unsupported crafting/material schema;
- unsupported faction operation procedure;
- unsupported economy/requisition model;
- unsupported installation/body-modification doctrine;
- unsupported time manipulation or causality procedure;
- unsupported donor metaphysics;
- unclear state mutation;
- unclear source-local boundary.

Quarantine should preserve visible evidence and identify the blocked owner file.

## Escalation

Escalate only when repeated or high-impact donor pressure exposes a real missing Astra distinction.

Escalation examples:

- repeated donors require formal maintenance/upkeep pressure beyond D13's current burden model;
- repeated cultivation sources require staged seclusion and bottleneck-preparation doctrine that cannot be handled as ordinary Training or Preparation Projects;
- repeated cyberware/biotech donors require a dedicated installation/rejection/recovery procedure crossing D07/D08/D09/D17;
- repeated faction/domain donors require institutional Project doctrine before D15 is complete;
- repeated crafting-heavy donors require material-grade and recipe-schema doctrine beyond D09/D17 readiness;
- repeated campaign systems require long-horizon Project aging and retirement doctrine owned by D18.

Escalation is preferable to Astra-sounding invention.

## Clock-like project systems

D13 must not adopt a universal Project clock by implication.

Clock-like systems route by function:

| Function | Likely owner |
|---|---|
| long-task completion | D13 Project progress, if supported |
| world/faction/social consequence | D10 unresolved pressure |
| travel or site risk | D14 travel/exploration risk |
| institutional action | D15 faction operation |
| campaign arc pressure | D18 campaign arc pressure |
| bounded local procedure | source-local retained procedure |
| unsupported owner | quarantine |
| repeated/high-impact missing doctrine | escalation |

A clock is a shape, not an authority.

## Rejected donor assumptions

D13 requires rejected-import notes for unsupported donor assumptions including:

- fixed rest recovery;
- automatic full healing after rest;
- crafting by exact donor currency/time math;
- training as automatic advancement;
- research as automatic truth reveal;
- assistant labor as free progress;
- facility labels as universal capabilities;
- faction clocks as universal procedure;
- Project clocks as default law;
- kingdom turns as Astra campaign time;
- cyberware essence/humanity costs as Astra metaphysics;
- cultivation seclusion timing as universal advancement pacing;
- salvage tables as automatic loot generation;
- business income as automatic passive wealth;
- source-local ritual phases as general ritual law.

## Donor label rule

Donor labels such as rest, downtime, clock, Project, training, crafting, faction turn, stronghold turn, seclusion, or maintenance cycle are evidence only. D13 maps their function, not their label.

## Lawful outcome reminders

Every donor long-task construct receives exactly one lawful outcome:

- direct Astra mapping;
- normalized Astra mapping;
- source-local retained construct;
- quarantined construct pending later doctrine;
- escalated doctrine problem.

Do not create hybrid outcomes such as “mostly canon,” “probably normalized,” or “source-local but generally true.”

## Anti-drift controls

- Do not use fixed equivalency tables such as “long rest = recovery” or “clock = Project progress.”
- Do not preserve donor downtime systems exactly by default.
- Do not normalize unsupported donor metaphysics.
- Do not treat repeated source-local use as canon promotion.


<!-- END D13-06_source_local_downtime_donor_project_mapping_quarantine_and_escalation.md -->


---

<!-- BEGIN D13-07_records_not_final_schema_and_conversion_handoff_shapes.md -->

# D13-07 — Records, Not-Final Schema, and Conversion Handoff Shapes

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

What minimum records and control checks does D13 need so downtime, Projects, recovery, crafting, repair, salvage, research, training, maintenance, and source-local long-task systems remain auditable during conversion, canon review, future runtime design, and eventual live play?

D13-07 defines lightweight not-final-schema record shapes. These are doctrine-facing and conversion-facing controls. They are not final runtime schemas, database tables, crafting schemas, recovery schemas, economy schemas, faction schemas, or campaign-state schemas.

## Record posture

Every record shape in this file is:

```text
not final schema
doctrine-facing / conversion-facing control shape
runtime Gate B or later schema doctrine may replace or formalize this
```

Record shapes exist to prevent ambiguity during conversion and doctrine review.

## Project Record

```yaml
project_record:
  record_type: project
  project_id: string
  project_goal: string
  project_family: recovery | training | research | crafting | salvage | repair | installation_preparation | resource_gathering | social_project | faction_support | preparation | maintenance | special_source_local | mixed
  secondary_families: []
  scope_band: minor | standard | major | extended | transformational
  interval_scale: hours | days | weeks | months | season | travel_leg | recovery_block | facility_cycle | source_local_interval | other
  current_status: not_started | ready | active | progressing | blocked | complicated | paused | interrupted | completed | completed_with_complication | failed | abandoned | quarantined | escalated | archived
  primary_actor_ref: string
  contributor_refs: []
  requirement_refs: []
  support_asset_refs: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  hidden_requirement_present: true | false | unknown
  notes: string
```

## Project Requirement Record

```yaml
project_requirement_record:
  record_type: project_requirement
  requirement_id: string
  project_ref: string
  requirement_type: time | safe_location | materials | tools | facility | assistant | access_tag | method_competency | resource_cost | information | permission_license | reputation_standing | body_condition | object_condition | route_technique_domain | source_local_prerequisite | other
  status: met | missing | unknown | protected_hidden | blocked_by_owner_file | source_local | quarantined
  owner_file: D03 | D04 | D05 | D06 | D07 | D08 | D09 | D10 | D13 | D15 | D17 | D18 | source_local | unknown
  visible_to_player: true | false | partial
  commitment_required: true | false
  notes: string
```

## Project Interval Record

```yaml
project_interval_record:
  record_type: project_interval
  interval_id: string
  project_ref: string
  interval_scale: string
  committed_time: string
  committed_costs: []
  committed_exposures: []
  active_method: string
  active_contributors: []
  facility_or_location_ref: string | null
  progress_check_required: true | false
  progress_check_reason: uncertainty | opposition | risk | unstable_requirement | hidden_pressure | acceleration | interruption | source_local_procedure | none
  resolution_owner: D02 | source_local | none
  notes: string
```

## Project Progress Event Record

```yaml
project_progress_event_record:
  record_type: project_progress_event
  progress_event_id: string
  project_ref: string
  interval_ref: string
  interval_outcome: advanced | advanced_with_cost | partial | stalled | blocked | complicated | damaged | interrupted | completed | completed_with_complication | failed | abandoned | quarantined | escalated
  completion_state: none | partial | complete | failed | terminal | unknown
  owner_file_handoffs: []
  state_delta_refs: []
  unresolved_pressure_refs: []
  notes: string
```

## Project Complication Record

```yaml
project_complication_record:
  record_type: project_complication
  complication_id: string
  project_ref: string
  complication_family: cost_increase | delay | material_loss | tool_or_facility_damage | assistant_risk | injury_or_condition_setback | corruption_or_instability_pressure | object_instability | social_scrutiny | faction_attention | legal_exposure | information_false_lead | hidden_pressure_surface | source_local_threat | active_scene_trigger | owner_file_gap | other
  severity: low | medium | high | blocking
  owner_file: D03 | D07 | D08 | D09 | D10 | D12 | D15 | D17 | D18 | source_local | unknown
  immediate_scene_trigger: true | false
  quarantine_or_escalation_required: true | false
  notes: string
```

## Contributor / Support Record

```yaml
project_contributor_support_record:
  record_type: project_contributor_support
  support_id: string
  project_ref: string
  support_type: contributor | facility | material | tool | platform | license | access_tag | favor | funding | crew | automated_system | source_local_support
  support_role: primary_worker | assistant | mentor | specialist | crew | guard | sponsor | supplier | research_aide | ritual_participant | patient | test_subject | faction_representative | facility_operator | companion_summon | automated_system | other
  support_function: method_support | access_permission | labor | protection | materials | knowledge | facility_operation | social_cover | faction_authorization | risk_absorption | acceleration | stability | other
  burden_or_risk: []
  owner_file: D05 | D08 | D09 | D10 | D15 | D17 | D18 | source_local | unknown
  notes: string
```

## Interruption / Abandonment Record

```yaml
project_interruption_abandonment_record:
  record_type: project_interruption_or_abandonment
  event_id: string
  project_ref: string
  event_type: interruption | abandonment | pause | resume | archive
  trigger: active_scene | resource_loss | facility_loss | assistant_withdrawal | injury | travel | attack | legal_action | faction_pressure | hidden_threat | material_spoilage | object_instability | relationship_rupture | campaign_time_skip | source_local_event | other
  outcome: pause_without_loss | pause_with_decay | delay | cost_increase | progress_loss | requirement_change | complication_added | active_scene_triggered | project_split_required | project_abandoned | project_quarantined | project_escalated | archived
  lost_elements: []
  preserved_elements: []
  exposed_elements: []
  recoverable_elements: []
  unresolved_pressure_refs: []
  owner_file_handoffs: []
  notes: string
```

## Donor Project Mapping Record

```yaml
donor_project_mapping_record:
  record_type: donor_project_mapping
  donor_label: string
  donor_function_summary: string
  donor_interval_assumption: string | null
  state_changed_by_donor_procedure: []
  mapped_project_family: string | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```

## Owner-file handoff expectations

A D13 record may point to owner-file handoff. It must not mutate or define the other file's state.

Examples:

- D13 Project Progress Event says a repair Project completed with complication. D09 decides the object-state result.
- D13 Research Project says a partial result occurred. D10/D11 decide what information can be known and surfaced.
- D13 Recovery Project says an interval advanced. D07 decides condition or injury changes.
- D13 Social Project says relationship repair progressed. D10/D15 decide actual relationship or faction-state updates.

## Hidden-state control

Records may mark hidden requirements, hidden pressure, or protected owner-file content as present, unknown, or protected. They must not expose hidden truth in player-facing form.

## Anti-drift controls

- Do not treat record fields as final runtime schema.
- Do not add final mechanics to record shapes.
- Do not use record completeness as canon promotion.
- Do not omit source-local boundaries when donor systems are retained.
- Do not omit rejected imports from donor project mappings.


<!-- END D13-07_records_not_final_schema_and_conversion_handoff_shapes.md -->


---

<!-- BEGIN D13-09_integration_checklists_ddr_register_and_acceptance_criteria.md -->

# D13-09 — Integration Checklists, DDR Register, and Acceptance Criteria

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Purpose

D13-09 is the final control file for the D13 doctrine pack. It consolidates integration requirements, anti-drift rules, source-local boundaries, escalation triggers, acceptance criteria, and the design decision register.

## Integration checklist

A D13 Project procedure is valid only if the following are checked where relevant:

- Project goal identifies intended state change or delayed consequence.
- Project family is a routing category, not a fixed downtime menu option.
- Mixed Projects declare one primary family and secondary pressure families.
- Distinct goals requiring different owner files are split into linked Projects.
- Scope band is declared: minor, standard, major, extended, or transformational.
- Interval scale is declared and not assumed from donor procedure.
- Requirements are identified before commitment when knowable.
- Hidden requirements may be protected without revealing hidden truth.
- Visible costs and risks are previewed when knowable.
- Time, material, facility, assistant, resource, exposure, and opportunity commitments occur before progress when applicable.
- Interval checks occur only when uncertainty, opposition, risk, hidden pressure, acceleration, interruption, or source-local procedure requires them.
- Progress uses Interval Outcome States, not universal clocks by default.
- Numeric progress is supported only by owner file, source-local procedure, or later schema.
- Partial completion is treated as meaningful.
- Complications are classified and routed to owner files.
- Interruption and abandonment record lost, preserved, exposed, recoverable, archived, or unresolved pressure.
- Concurrent Projects are checked for Project Load.
- Contributors and facilities have valid roles/functions and possible burden.
- Source-local procedures have boundaries.
- Donor assumptions rejected by D13 are recorded.
- Record shapes are treated as not-final schema.

## Owner-file handoff checklist

D13 must hand off rather than absorb ownership:

| Concern | Owner |
|---|---|
| resolution math and outcome bands | D02 |
| resource pool definitions, overdraw, recharge, resource-side backlash | D03 |
| advancement, proof, breakthroughs, transformations | D04 |
| skills, methods, competency, research/training relevance | D05 |
| route, Technique, Principle, oath, domain expression | D06 |
| harm, injury, conditions, corruption, recovery content | D07 |
| actor substrate, body/form-state, personhood | D08 |
| object, relic, platform, material, salvage, repair, installation state | D09 |
| world-state, relationship, reputation, information, law, faction pressure | D10 |
| presentation and hidden-state surfacing | D11 |
| cadence and active scene transitions | D12 |
| travel, navigation, exploration, discovery | D14 |
| faction and institutional operations | D15 |
| economy, acquisition, ownership, value, scarcity, requisition | D17 |
| campaign arcs, seasons, state aging, archive/active state, long-horizon pacing | D18 |

## Source-local boundary checklist

A retained source-local downtime or Project system must state:

- source/campaign/location/faction/object/ritual boundary;
- preserved procedure;
- non-generalized elements;
- stripped donor assumptions;
- rejected imports;
- owner-file handoffs;
- confidence;
- whether canon review is required for later reuse.

Source-local retention is valid. Source-local promotion is not automatic.

## Quarantine triggers

Quarantine donor long-task systems when:

- extraction damage blocks procedure understanding;
- requirements are missing and cannot be inferred;
- owner-file support is absent;
- recovery/healing/corruption procedure is unsupported;
- crafting/material schema is unsupported;
- faction operation procedure is unsupported;
- economy/requisition model is unsupported;
- installation/body modification/substrate doctrine is unsupported;
- time manipulation or causality procedure is unsupported;
- donor metaphysics are required but unadopted;
- state mutation is unclear;
- source-local boundary is unclear.

## Escalation triggers

Escalate only repeated or high-impact missing doctrine that cannot be safely normalized, retained source-locally, or quarantined as a one-off.

Examples:

- formal maintenance/upkeep pressure beyond current D13 burden model;
- staged cultivation seclusion/bottleneck-preparation doctrine;
- cyberware/biotech installation/rejection/recovery crossing D07/D08/D09/D17;
- institutional Project doctrine needed before D15 is complete;
- material-grade or recipe-schema doctrine beyond D09/D17 readiness;
- long-horizon Project aging and retirement doctrine owned by D18.

## Required rejected-import notes

Record rejected imports for unsupported donor:

- long rest / short rest reset assumptions;
- fixed recovery by day;
- crafting by exact donor currency/time math;
- training as automatic advancement;
- research as automatic truth reveal;
- assistant labor as free progress;
- facility labels as universal capabilities;
- Project clocks as default law;
- faction clocks or kingdom turns as universal procedure;
- cyberware essence/humanity metaphysics;
- cultivation seclusion as universal advancement pacing;
- salvage tables as automatic reward generation;
- passive business income as automatic wealth;
- source-local ritual phases as general ritual law.

## Embedded risk queue and fixes

### R1 — Fixed downtime activity menu drift

Fix: Project families are routing categories, not fixed actions. Validity comes from interval-scale commitment, requirements, risk, progress, or delayed state consequence.

### R2 — Universal project clocks

Fix: D13 uses Interval Outcome States by default. Clocks/tracks require owner-file, source-local, or later-schema support.

### R3 — Rest/reset recovery import

Fix: D13 owns recovery interval procedure only. D07 owns actual recovery-state changes.

### R4 — Training bypass

Fix: D04/D05/D06 own advancement gates, competency, method, access, route, and Technique implications.

### R5 — Research hidden-state leakage

Fix: D05/D10/D11 own research methods, information-state, hidden truth, and presentation. D13 records progress only.

### R6 — Crafting unsupported powers

Fix: D09/D17 own object state, materials, value, ownership, scarcity, and acquisition. D03/D06/D07/D08 are invoked when resource, power, harm, or substrate implications exist.

### R7 — Salvage free rewards

Fix: D13 records salvage work and outcome. D09/D17 decide what exists, who owns it, and whether it is legal or scarce.

### R8 — Generic support bonuses

Fix: contributors, facilities, materials, licenses, and support assets require role/function and may create burden.

### R9 — Unlimited concurrent Projects

Fix: Project Load blocks, delays, complicates, splits, abandons, quarantines, or escalates unsupported concurrency.

### R10 — D15/D17/D18 ownership theft

Fix: D13 owns intervals and Projects. D15 owns faction operations; D17 owns economy/acquisition; D18 owns campaign continuity.

### R11 — Source-local generalization

Fix: source-local donor long-task systems remain bounded. Repetition creates canon candidate review or doctrine escalation, not automatic adoption.

### R12 — Record shapes mistaken for final schemas

Fix: all record shapes are explicitly not-final schema and doctrine-facing/conversion-facing only.

## Acceptance criteria

D13 is accepted if it can:

- create a Project from interval-scale intent;
- classify Project family and scope;
- identify requirements before commitment when knowable;
- protect hidden requirements;
- commit time, materials, facility claims, assistants, resources, exposure, and opportunity cost before progress when applicable;
- advance Projects without universal clocks;
- handle partial completion;
- classify and route complications;
- handle interruption, abandonment, pause, resume, and archive;
- support recovery, training, research, crafting, salvage, repair, installation preparation, resource gathering, social, faction-support, preparation, maintenance, and source-local Projects;
- prevent unlimited concurrent background progress through Project Load and support burden;
- map donor downtime systems by function, not label;
- preserve source-local systems safely;
- quarantine unsupported long-task systems;
- escalate repeated or high-impact missing doctrine;
- route outcomes to owner files without stealing ownership.

## DDR register

| Decision | Locked option | Result |
|---|---|---|
| D13-00-1 | Option A | Project-Centered Interval Architecture. |
| D13-00-2 | Option A | Project = any interval-scale goal with commitment, requirement, progress, risk, or delayed outcome. |
| D13-00-3 | Option A | Project families are named routing categories. |
| D13-00-4 | Option A | Flexible progress states and interval outcomes, not universal clocks. |
| D13-00-5 | Option A | Requirements identified before commitment when knowable. |
| D13-00-6 | Option A | Projects can interrupt, pause, resume, abandon, escalate, or transition to D12 active scenes. |
| D13-00-7 | Option A | Donor downtime systems map/source-local/quarantine/escalate; never adopted by label. |
| D13-01-1 | Option A | Shared Project anatomy. |
| D13-01-2 | Option A | Project families route owner handoffs, not fixed menu actions. |
| D13-01-3 | Option A | Scope bands: minor, standard, major, extended, transformational. |
| D13-01-4 | Option A | Flexible interval scale. |
| D13-01-5 | Option A | Shared requirement categories. |
| D13-01-6 | Option A | Lifecycle/progress states. |
| D13-01-7 | Option A | Outcomes route to owner files. |
| D13-02-1 | Option A | Eight-checkpoint setup. |
| D13-02-2 | Option A | Goal must identify intended state change or delayed consequence. |
| D13-02-3 | Option A | Mixed Projects declare primary/secondary families and split when needed. |
| D13-02-4 | Option A | Requirement statuses include hidden/protected/blocking states. |
| D13-02-5 | Option A | Setup outcomes: ready, ready with risk, blocked, quarantined, escalated. |
| D13-02-6 | Option A | Costs and commitments happen before progress when applicable. |
| D13-02-7 | Option A | Hidden requirements may be protected. |
| D13-03-1 | Option A | Interval Outcome States. |
| D13-03-2 | Option A | Numeric progress only with support. |
| D13-03-3 | Option A | Interval checks only when trigger exists. |
| D13-03-4 | Option A | Partial completion is first-class. |
| D13-03-5 | Option A | Complications route to owner files. |
| D13-03-6 | Option A | Failure types distinguished. |
| D13-03-7 | Option A | Acceleration requires cost/risk support. |
| D13-04-1 | Option A | Project Family Profiles. |
| D13-04-2 | Option A | Core family list accepted. |
| D13-04-3 | Option A | Recovery interval belongs to D13; recovery content to D07. |
| D13-04-4 | Option A | Training/research interval belongs to D13; implications to D04/D05/D06/D10/D11. |
| D13-04-5 | Option A | Craft/salvage/repair/install interval belongs to D13; content to D09/D17/D08/D07/D03/D06. |
| D13-04-6 | Option A | Social/faction/resource intervals belong to D13; state to D10/D15/D17. |
| D13-04-7 | Option A | Special/source-local Projects retained with boundaries. |
| D13-05-1 | Option A | Project Load, not fixed slots. |
| D13-05-2 | Option A | Contributors require valid role and may create burden. |
| D13-05-3 | Option A | Facilities classified by function/status. |
| D13-05-4 | Option A | Materials/support assets are requirements/commitments/risks/outputs. |
| D13-05-5 | Option A | Maintenance is first-class. |
| D13-05-6 | Option A | Interruption outcomes are explicit. |
| D13-05-7 | Option A | Abandonment records loss/preservation/exposure/recoverability. |
| D13-06-1 | Option A | Functional donor project mapping ladder. |
| D13-06-2 | Option A | Donor labels are evidence only. |
| D13-06-3 | Option A | Source-local donor systems valid when bounded. |
| D13-06-4 | Option A | Clock-like systems route by function. |
| D13-06-5 | Option A | Quarantine triggers include extraction/doctrine/metaphysics/mutation/boundary blockers. |
| D13-06-6 | Option A | Escalate only repeated/high-impact missing doctrine. |
| D13-06-7 | Option A | Rejected donor assumptions required. |
| D13-07-1 | Option A | Lightweight not-final record pack. |
| D13-07-2 | Option A | Project Record included. |
| D13-07-3 | Option A | Requirement and Interval Records included. |
| D13-07-4 | Option A | Progress and Complication Records included. |
| D13-07-5 | Option A | Contributor/Support Record included. |
| D13-07-6 | Option A | Interruption/Abandonment Record included. |
| D13-07-7 | Option A | Final integration checklist and DDR register included. |

## Next handoff

After D13, proceed to D14 — Exploration, Travel, Navigation, and Discovery. D14 should consume D12 cadence handoffs and D13 interval/project boundaries but must not redefine D13 Projects.


<!-- END D13-09_integration_checklists_ddr_register_and_acceptance_criteria.md -->
