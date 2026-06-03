# D12-09 — Integration Checklists, DDR Register, and Acceptance Criteria

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Owner file: D12 timing and cadence doctrine

## 1. Purpose

This file provides D12's final integration controls: dependency checklist, owner-file handoff checklist, donor-family pressure checklist, source-local boundary checklist, anti-drift rules, escalation triggers, DDR register, risk queue, and acceptance criteria.

## 2. Dependency checklist

D12 must preserve these upstream dependencies:

- D00: meaningful action commits deltas; power costs; context matters; world remembers.
- D01: attribute pressure axes; Insight/Reason split; Pneuma hidden protection.
- D02: resolution procedure and outcome grammar.
- D03: resources, costs, overdraw, recharge, backlash pressure.
- D04: breakthrough, transformation, evolution, advancement pressure.
- D05: methods, skills, competency, research, procedure ownership.
- D06: Techniques, Principles, oaths, domains, route expression.
- D07: harm, conditions, corruption, injury, environmental danger.
- D08: actors, personhood, form-state, companions, AI, substrate.
- D09: objects, relics, platforms, implants, tools, crafting/salvage state.
- D10: world memory, factions, law, economy, information, unresolved pressure.
- D11: presentation, hidden-state boundaries, assessment presentation, consequence surfacing.

D12 must hand off later procedures to:

- D13 for downtime, projects, recovery, crafting, research, training, repair;
- D14 for travel, navigation, exploration, discovery, site entry, watches, ambush;
- D15 for faction, institution, relationship, diplomacy, pressure operations;
- D17 for economy, acquisition, inventory, requisition, reward, maintenance timing;
- D18 for arcs, seasons, pacing, state aging, state pruning, long-horizon progression.

## 3. Owner-file handoff checklist

Before D12 resolves a structured action or exchange, verify:

```yaml
handoff_checklist:
  cadence_known: true | false
  action_window_needed: true | false
  declaration_clear: true | false
  method_target_owner_identified: true | false
  visible_cost_risk_previewed_when_knowable: true | false
  commitment_timing_recorded: true | false
  D02_called_only_if_needed: true | false
  consequence_owners_identified: true | false
  state_delta_checkpoint_completed: true | false
  reaction_or_interruption_window_checked: true | false
  transition_or_continuation_recorded: true | false
```

## 4. Donor-family pressure checklist

When converting donor timing, check for:

- fixed action categories;
- fixed round duration;
- initiative method;
- reaction allowance;
- movement/action split;
- exploration turn;
- random encounter interval;
- clock or countdown;
- faction turn;
- downtime turn;
- hacking round;
- ritual phase;
- chase round;
- vehicle/platform turn;
- boss phase;
- recharge timing;
- morale/reaction phase;
- hidden timer.

Each must be mapped by function, source-local retained, quarantined, or escalated. Do not use fixed equivalency tables.

## 5. Source-local boundary checklist

A source-local timing construct must state:

- source or campaign boundary;
- donor timing label;
- donor timing function;
- why it is useful locally;
- why it is not generalized;
- stripped donor assumptions;
- owner-file handoffs;
- whether it creates canon candidate pressure;
- review requirement for reuse.

## 6. Anti-drift rules

D12 must not:

- become combat doctrine;
- make martial conflict the default structured-scene model;
- import fixed donor action categories;
- turn Action Windows into donor turns;
- give universal reactions;
- make Finesse the only initiative axis;
- force all simultaneous action into initiative order;
- collapse actor, platform, environment, and faction action into one clock;
- adopt universal clocks or countdowns;
- define D02 outcome math;
- define D03 resource pools or recharge;
- define D07 harm math;
- define D10 world-state contents;
- let D11 presentation decide timing;
- expose hidden state;
- let source-local timing auto-promote;
- create final runtime schemas;
- become final live-play GM adapter behavior.

## 7. Escalation triggers

Escalate timing doctrine when:

- repeated donor pressure exposes a missing Astra timing distinction;
- simultaneous multi-scale timing cannot be resolved by primary/secondary profiles;
- clock-like systems mutate state without owner support;
- morale/reaction timing recurs across unrelated donor families;
- stealth alert-state timing exceeds profile support;
- causality, rewind, time loop, retroactive action, or prophetic timing appears repeatedly;
- platform/crew command cycles require more doctrine than D12 provides;
- faction-turn pressure cannot wait for D15;
- ritual/power phase timing repeatedly interacts with D03, D04, D06, and D07;
- source-local timing repeats across unrelated donors and may deserve canon candidate review.

Escalation must name likely owner file or proposed future file.

## 8. Risk queue and embedded fixes

| Risk | Embedded fix |
|---|---|
| Combat-centered D12 | Martial conflict is one cadence profile among many. |
| Action Window becomes donor turn | Defined as bounded opportunity, not fixed action category. |
| Reactions become universal freebies | Require trigger plus permission source. |
| Universal clock creep | Clock-like systems route by function. |
| D13–D18 ownership theft | D12 owns handoff timing only. |
| Record shapes mistaken for runtime schemas | All records labeled not final schema. |
| Hidden-state leakage | Hidden pressure markers do not reveal hidden truth. |
| Multi-scale underdefinition | Different scales coexist without sharing one mandatory clock. |
| D02/D12 blur | D12 calls D02; D02 resolves. |
| Source-local overuse | Bounded retention plus escalation/canon review for repeated pressure. |

## 9. DDR register

### DDR-D12-001 — Layered cadence architecture

Decision: D12 uses layered cadence states rather than universal turns.  
Rationale: supports many scene families without combat overfit.  
Risk: may feel abstract without profiles.  
Mitigation: D12-05 cadence profiles.

### DDR-D12-002 — Six-state cadence ladder

Decision: Free Play, Focused Scene, Structured Exchange, Conflict Cadence, Extended Task Cadence, Transition / Time-Scale Shift.  
Rationale: gives enough structure without megafile scope.  
Risk: D13–D18 overlap.  
Mitigation: D12 owns handoff timing only.

### DDR-D12-003 — Action Window model

Decision: Action Windows are bounded opportunities, not fixed turns.  
Rationale: prevents donor action economy leakage.  
Risk: conversion models may equate with turns.  
Mitigation: repeated anti-drift language and record shapes.

### DDR-D12-004 — Context-derived initiative

Decision: initiative is sequencing authority derived from context, with D02 used only when order is uncertain or contested.  
Rationale: supports stealth, social, ritual, platform, and technical scenes.  
Risk: less familiar than fixed initiative.  
Mitigation: method-dependent attribute guidance.

### DDR-D12-005 — Triggered reactions and interruptions

Decision: reactions require trigger plus permission source; interruptions are timing-valid reactions that may alter sequencing.  
Rationale: prevents universal reaction economies.  
Risk: permission source ambiguity.  
Mitigation: reaction/interruption record.

### DDR-D12-006 — Neutral timing containers

Decision: use Beat, Action Window, Exchange, Interval, and Time-Scale Shift.  
Rationale: avoids fixed donor durations.  
Risk: donor timing conversion may over-normalize.  
Mitigation: functional mapping ladder.

### DDR-D12-007 — Ten-checkpoint procedure grammar

Decision: D12 defines cadence, declaration, method/target, preview, commitment, resolution, consequence routing, state delta, reaction, transition.  
Rationale: preserves cost and consequence timing discipline.  
Risk: procedure may feel heavy.  
Mitigation: used when meaningful structure is needed, not every free-play action.

### DDR-D12-008 — Cadence profiles

Decision: define eight core profiles as timing templates.  
Rationale: gives conversion support without creating full subsystems.  
Risk: profile list may grow too quickly.  
Mitigation: new profiles require escalation or later file ownership.

### DDR-D12-009 — Functional donor timing mapping

Decision: donor timing is mapped by function and lawful outcome, not label.  
Rationale: prevents false equivalency.  
Risk: requires careful conversion review.  
Mitigation: donor timing mapping record.

### DDR-D12-010 — Not-final-schema records

Decision: include lightweight control records but mark them not final runtime schemas.  
Rationale: supports audit and conversion.  
Risk: premature schema authority.  
Mitigation: explicit non-authority labels.

## 10. Acceptance criteria

D12 is accepted if it can:

- classify cadence state;
- explain when Free Play becomes Focused Scene or Structured Exchange;
- sequence action without donor action economy;
- handle reactions and interruptions without universal freebies;
- support simultaneous and multi-scale action;
- define neutral timing containers;
- call D02 only when resolution is needed;
- commit visible costs before resolution when knowable;
- route consequences to correct owner files;
- preserve hidden-state boundaries;
- support martial, social, stealth, chase, ritual, technical, exploration, platform, and mixed scenes;
- map donor timing by function;
- retain source-local timing safely;
- route clocks/countdowns by owner file;
- record transitions and unresolved pressure;
- avoid stealing D13–D18 procedures;
- avoid final runtime schema claims.

## 11. Minimum test prompts

D12 should be tested against:

1. a simple combat ambush with simultaneous reaction risk;
2. a social trial with faction pressure;
3. a stealth infiltration with hidden patrol timing;
4. a chase with environmental hazards;
5. a ritual and counter-ritual with overdraw risk;
6. a platform crew emergency with actor-scale and platform-scale action;
7. an exploration hazard using a donor dungeon turn;
8. a source-local boss phase script;
9. a donor clock that should route to D10, D13, D14, D15, or D18 depending function;
10. a malformed timing table that must quarantine.

## 12. Final status

D12 is doctrine-ready as a timing and cadence pack. It should be integrated only as doctrine, not as final runtime implementation or live-play behavior.
