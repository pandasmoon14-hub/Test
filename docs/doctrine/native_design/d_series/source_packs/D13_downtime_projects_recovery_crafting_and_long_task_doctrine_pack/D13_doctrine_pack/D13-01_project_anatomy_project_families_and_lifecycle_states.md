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
