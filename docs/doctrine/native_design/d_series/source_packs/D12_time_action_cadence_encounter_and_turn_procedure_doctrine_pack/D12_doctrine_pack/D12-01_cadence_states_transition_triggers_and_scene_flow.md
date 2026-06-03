# D12-01 — Cadence States, Transition Triggers, and Scene Procedure Flow

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Owner file: D12 timing and cadence doctrine

## 1. Purpose

This file defines Astra's six-state cadence ladder and the triggers that move play between ordinary freeform action, focused pressure, structured sequencing, conflict cadence, extended task handoff, and time-scale transitions.

## 2. Cadence principle

Astra does not start every scene in turns. Structure appears when timing matters. D12 should increase or reduce procedural weight as pressure changes.

## 3. The six cadence states

D12 uses these cadence states:

```yaml
cadence_states:
  - free_play
  - focused_scene
  - structured_exchange
  - conflict_cadence
  - extended_task_cadence
  - transition_time_scale_shift
```

### 3.1 Free Play

Free Play covers ordinary description, conversation, movement, examination, low-pressure preparation, simple interaction, and actions that are possible, uncontested, and consequence-light.

Free Play does not require formal action windows. It does not automatically call D02. It does not automatically commit D03 costs. It does not automatically surface D10 pressure.

Free Play exits when any of the following appear:

- risk;
- uncertainty;
- contested timing;
- resource or cost commitment;
- hidden-state probing;
- meaningful opposition;
- consequence pressure;
- a player requests assessment or preparation that could change risk;
- source-local procedure requires structure.

### 3.2 Focused Scene

Focused Scene is the default pressure state before strict sequencing. It is used when attention narrows around a meaningful choice, but actor order does not yet require formal turns.

Examples:

- entering an unstable chamber;
- negotiating with a guarded official;
- studying a dangerous relic;
- approaching a patrol;
- preparing a ritual under risk;
- deciding how to cross a hazard;
- evaluating whether to spend scarce power.

Focused Scene can call D02, D03, D05, D06, D07, D09, D10, and D11, but it does not create a full structured exchange unless sequencing becomes important.

### 3.3 Structured Exchange

Structured Exchange begins when action order, interruption risk, simultaneous declarations, or opportunity timing matters.

Structured Exchange uses Action Windows. It is not limited to combat.

Triggers include:

- multiple actors attempting incompatible actions;
- opportunity windows opening or closing;
- ambush, breach, pursuit, or urgent rescue;
- contested social timing;
- stealth exposure risk;
- active countermeasure;
- platform crew operation;
- ritual channeling and counter-ritual;
- environmental pressure pulse.

### 3.4 Conflict Cadence

Conflict Cadence is a structured exchange with repeated opposition. The opposition may be martial, social, stealth-based, technical, environmental, ritual, vehicular, platform-scale, psychic, legal, institutional, or mixed.

Conflict Cadence does not mean combat by default. Combat is the Martial Conflict profile under D12-05.

Conflict Cadence continues until:

- the objective is resolved;
- one side disengages;
- consequence forces transition;
- the cadence shifts to another profile;
- unresolved pressure is handed to D10 or another owner file;
- source-local procedure ends or escalates.

### 3.5 Extended Task Cadence

Extended Task Cadence begins when the active goal requires repeated intervals, accumulated progress, persistent cost, staged risk, recovery, crafting, research, training, repair, social project work, surveillance, or long-form preparation.

D12 owns the handoff into Extended Task Cadence. D13 owns downtime, project progress, recovery, crafting, research, repairs, assistants, facilities, costs, interruption, failure, and concurrent work.

D12 must not define D13's project mechanics.

### 3.6 Transition / Time-Scale Shift

Transition / Time-Scale Shift records movement between cadence states or time scales.

Examples:

```text
free_play -> focused_scene
focused_scene -> structured_exchange
structured_exchange -> conflict_cadence
conflict_cadence -> focused_scene
focused_scene -> extended_task_cadence
scene_time -> travel
travel -> site_entry
scene_time -> downtime
faction_pressure -> active_scene
campaign_season -> downtime_block
```

Transitions must preserve unresolved pressure. They may carry pressure forward, retire it, escalate it, quarantine it, or hand it to another owner file.

## 4. Transition trigger table

| From | To | Trigger | Required note |
|---|---|---|---|
| Free Play | Focused Scene | risk, uncertainty, hidden pressure, meaningful choice | pressure source and visible cues |
| Focused Scene | Structured Exchange | actor order or interruption matters | action-window trigger |
| Structured Exchange | Conflict Cadence | repeated opposition emerges | primary cadence profile |
| Conflict Cadence | Focused Scene | immediate sequence pressure drops | unresolved pressure handling |
| Any Scene | Extended Task Cadence | repeated intervals or accumulated progress needed | D13 handoff note |
| Scene | Travel/Exploration | movement through space becomes procedure | D14 handoff note |
| Scene | Faction/Institution | institutional pressure becomes procedural | D15 handoff note |
| Scene | Economy/Acquisition | acquisition, reward, requisition, scarcity becomes procedure | D17 handoff note |
| Scene | Campaign Scale | arc/season/time skip/state aging required | D18 handoff note |

## 5. Hidden-state control

Cadence records may mark hidden pressure as present, absent, or unknown. They must not reveal protected hidden truth to the player. D11 controls hidden-state presentation, and relevant owner files decide what may be known.

Pneuma remains protected. D12 may recognize that hidden cosmic pressure affects timing, but it must not expose Pneuma as a stat, score, modifier, or player-visible timing mechanic.

## 6. Source-local procedure interaction

A source-local timing procedure may force a cadence transition inside its bounded source. The transition must still be recorded and must state the source-local boundary.

## 7. Acceptance criteria

This file is acceptable if it can explain when play moves from freeform to structured procedure, when structure reduces, and which owner file receives longer-scale procedure without D12 absorbing that procedure.
