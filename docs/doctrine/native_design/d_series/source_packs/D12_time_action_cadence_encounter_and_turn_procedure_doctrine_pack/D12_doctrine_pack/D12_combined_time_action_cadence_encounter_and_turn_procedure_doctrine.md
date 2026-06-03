<!-- BEGIN D12-README_manifest.md -->


# D12 — Time, Action Cadence, Encounter, and Turn Procedure Doctrine Pack

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Layer: Phase 1 native doctrine / operational procedure layer  
Owner: D12 timing and cadence doctrine  
Primary downstream users: D13–D18 doctrine drafting, conversion intake, canon review, runtime Gate B design, later play-facing adapter design

## Purpose

D12 defines how Astra Ascension advances from moment to moment. It governs cadence states, action windows, initiative, sequencing, reactions, interruptions, exchanges, intervals, time-scale shifts, timing checkpoints, structured scene profiles, donor timing mapping, and owner-file handoffs.

D12 is not combat doctrine. Combat is one structured cadence profile among many. D12 must support martial conflict, social conflict, stealth and infiltration, chase and pursuit, ritual and power contests, technical and system standoffs, exploration and hazards, platform and crew cadence, mixed scenes, source-local timing procedures, and future runtime handoff without importing donor action economies as Astra defaults.

## Core question

How does Astra decide when play is freeform, when it becomes structured, how actors receive meaningful action opportunities, how sequencing and interruption work, and when outcomes, costs, consequences, transitions, and owner-file handoffs occur?

## Doctrine files in this pack

1. `D12-00_time_action_cadence_encounter_procedure_and_owner_boundaries.md`
2. `D12-01_cadence_states_transition_triggers_and_scene_flow.md`
3. `D12-02_action_windows_initiative_sequencing_and_interruptions.md`
4. `D12-03_round_exchange_beat_interval_and_time_scale_grammar.md`
5. `D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md`
6. `D12-05_structured_scene_families_and_cadence_profiles.md`
7. `D12-06_source_local_timing_donor_procedure_mapping_and_escalation.md`
8. `D12-07_records_not_final_schema_and_conversion_handoff_shapes.md`
9. `D12-09_integration_checklists_ddr_register_and_acceptance_criteria.md`
10. `D12_pack_manifest.json`

## Locked decisions embedded in this pack

D12 uses a layered cadence architecture. The primary timing unit is cadence state, not a universal combat round or donor turn. Structure begins when sequencing, risk, contested timing, cost commitment, hidden pressure, or consequence timing matters. Structured exchanges use action windows. Initiative is context-derived and calls D02 only when order is uncertain or contested. Reactions require bounded triggers and permission sources. Simultaneous and multi-scale action is supported through declaration windows, priority resolution, and owner-file handoff. Donor timing systems are evidence only and remain source-local, normalized, quarantined, or escalated unless explicitly promoted later.

## Authority and phase separation

D12 belongs to doctrine and framework design. It does not perform donor conversion, canon promotion, runtime state mutation, live-play narration, or training-example authoring. It must preserve the project authority hierarchy:

1. Current Astra doctrine files.
2. Canonical Astra sourcebook material once formalized.
3. Converted Astra-native donor content.
4. Example packs and training examples.
5. Original donor assumptions.

Donor procedures are evidence, not law. A donor round, turn, phase, watch, clock, or initiative pass does not become Astra vocabulary or procedure by appearing often.

## Integration summary

D12 provides timing hooks for D02, D03, D04, D05, D06, D07, D08, D09, D10, and D11. It also defines handoff timing to D13, D14, D15, D17, and D18. It does not define those files' internal procedures.

## Risk fixes embedded

This pack embeds the D12 pre-generation risk audit fixes directly into the doctrine:

- combat is not the default structured scene;
- action windows are not donor turns;
- reactions are not universal freebies;
- clocks and countdowns are routed by function, not universalized;
- D12 owns handoff timing, not D13–D18 procedures;
- record shapes are not final schemas;
- hidden pressure markers do not reveal hidden facts;
- simultaneous and multi-scale actions do not share one mandatory clock;
- D12 does not own D02 resolution math;
- source-local timing is bounded and cannot auto-promote.

## Acceptance posture

D12 is accepted when it can classify cadence, explain when structure begins, sequence action without donor economy, handle reactions and simultaneous action, route owner-file consequences, map donor timing by function, preserve source-local timing, record transitions, and support multiple scene families without making combat or any donor procedure universal.



<!-- END D12-README_manifest.md -->


<!-- BEGIN D12-00_time_action_cadence_encounter_procedure_and_owner_boundaries.md -->


# D12-00 — Time, Action Cadence, Encounter Procedure, and Owner Boundaries

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Owner file: D12 timing and cadence doctrine

## 1. Purpose

This file defines D12's core purpose, owner boundaries, non-ownership rules, dependency logic, donor-family pressures, source-local boundaries, and anti-drift posture.

D12 answers the procedural question: how does Astra decide when play is freeform, when it becomes structured, how actors receive meaningful opportunities, and when timing triggers owner-file handoff?

D12 is not a combat chapter. It is the timing and cadence layer for all meaningful scene procedure.

## 2. Core doctrine

Astra uses a layered cadence architecture. Scene structure increases only when play requires sequencing, risk handling, contested timing, cost commitment, hidden pressure management, or consequence timing.

The primary D12 timing unit is a cadence state, not a universal round. Turns, rounds, watches, phases, clocks, initiative passes, exploration turns, and faction turns are donor evidence unless normalized, retained source-locally, quarantined, or escalated.

## 3. What D12 owns

D12 owns:

- scene time;
- cadence state classification;
- transition from free play to focused or structured play;
- action windows;
- initiative as sequencing authority;
- reactions and interruptions as bounded timing permissions;
- simultaneous declaration windows;
- multi-actor sequencing;
- exchange and interval timing grammar;
- structured scene cadence profiles;
- donor timing mapping rules;
- timing checkpoints for cost, resolution, consequence, state delta, reaction, and transition;
- source-local timing boundaries;
- timing-related conversion escalation rules;
- lightweight, not-final-schema timing records.

## 4. What D12 must not own

D12 must not own:

- D02 difficulty numbers, outcome bands, natural 20/natural 1 rules, opposed check math, or margin interpretation;
- D03 resource pools, recharge, overdraw math, or resource-side backlash content;
- D04 advancement, breakthrough, evolution, or transformation outcomes;
- D05 skill lists, methods, research, training, or competency definitions;
- D06 Technique mechanics, Principle definitions, route strain, oaths, or domain expression effects;
- D07 damage math, harm values, injury procedure, condition content, corruption tracks, or death rules;
- D08 actor substrate, personhood, companion rules, AI personhood, summon records, or body/form-state consequences;
- D09 item, relic, platform, implant, tool, or salvage state;
- D10 world-state contents, faction decisions, reputation changes, relationship states, economy state, or pressure queue contents;
- D11 player-facing presentation, hidden-state prose, rumor presentation, summary style, or live-play narration;
- D13 project, recovery, crafting, training, or downtime progress;
- D14 travel, navigation, exploration, mapping, route, watch, ambush, or discovery procedures;
- D15 faction/institutional operation, diplomacy systems, faction conflict, or relationship operation;
- D17 economy, acquisition, requisition, inventory, storage, maintenance, or reward procedure;
- D18 campaign arcs, seasons, long-horizon pacing, state pruning, or campaign memory aging;
- runtime Gate B schemas, command lifecycle implementation, event sourcing, state mutation, dice services, or backend validation;
- final live-play or GM-facing adapter behavior.

D12 may identify when those files should be invoked. It must not perform their work.

## 5. Dependency logic

D12 depends on D00–D11 for the following:

- D00: meaningful action commits tracked deltas; power costs something; context matters; world remembers; probing before committing is rewarded.
- D01: method-dependent attribute relevance; hidden Pneuma protection.
- D02: resolution grammar, outcome bands, cost commitment compatibility, opposed and extended check grammar.
- D03: resource and cost systems.
- D04: breakthrough and transformation pressure when timing matters.
- D05: methods, skills, competency, research, training, and procedure ownership.
- D06: Techniques, Principles, oaths, domains, and route expression.
- D07: harm, conditions, corruption, backlash consequences, and environmental danger.
- D08: actors, companions, AI, body/form-state, and substrate.
- D09: objects, platforms, relics, implants, tools, crafting/salvage state.
- D10: world memory, factions, law, economy, reputation, information-state, unresolved pressure.
- D11: presentation, hidden-state boundaries, state-audit output, player-facing and GM-facing summaries.

D12 feeds D13–D18 by defining when play leaves scene cadence and enters downtime, travel, faction, economy, or campaign-scale procedure.

## 6. Donor-family pressures

D12 must survive donor pressure from:

- d20/class-level action economies, initiative, actions, reactions, bonus actions, lair actions, legendary actions, challenge pacing;
- OSR exploration turns, dungeon turns, random encounter checks, morale and reaction phases, watches, supply timing;
- tactical frame/mech/squad initiative passes, activations, heat cycles, hardpoints, overwatch, grid timing;
- narrative/tag/aspect scenes, exchanges, spotlight order, compels, invokes, player-authored scene truths;
- horror/investigation clue pacing, hidden clocks, dread escalation, sanity/stress timers, revelation structure;
- cyberpunk/skill-pool simultaneous action, hacking turns, legality response windows, surveillance cadence, initiative passes;
- vehicle/ship/platform crew turns, command cycles, travel ticks, pursuit exchanges, platform-scale versus actor-scale timing;
- cultivation/LitRPG ritual duels, breakthrough windows, tribulation phases, domain clashes, aura contests, pressure accumulation;
- faction/domain/kingdom turns, institution cycles, social campaigns, law response, debt/favor timing;
- random-table/oracle interval triggers, encounter intervals, travel events, reaction rolls, table-driven time pressure.

No donor family may define Astra's default action economy.

## 7. Source-local boundaries

A timing procedure may be retained source-locally when it is useful within a bounded converted source but unsafe to generalize.

Examples include a specific alarm countdown, a boss phase script, a local ritual sequence, a campaign-specific faction clock, a dungeon's watch cycle, a donor adventure's timed collapse, or a source-specific travel hazard interval.

Source-local timing requires a declared boundary. Repetition of source-local timing does not promote it to Astra law. Repeated cross-donor pressure may create canon candidate review or doctrine escalation, but not automatic adoption.

## 8. Anti-drift rules

D12 must obey these rules:

- Do not treat combat as the default structured scene.
- Do not import donor action categories.
- Do not treat “round,” “turn,” “phase,” “watch,” “clock,” or “initiative pass” as automatic Astra terms.
- Do not define D02 outcome math or D03 resource rules.
- Do not define D07 harm math or D10 world-state contents.
- Do not let D11 presentation decide mechanical timing.
- Do not let source-local timing become universal through frequency alone.
- Do not make every meaningful action require a roll.
- Do not require all scales to share one action clock.
- Do not resolve missing timing doctrine with Astra-sounding invention.
- Do not become final GM adapter behavior.

## 9. Minimal conversion guidance

When conversion intake sees a donor timing construct, it must ask:

1. What function does this timing rule perform?
2. Which D12 container or cadence profile does it resemble?
3. What donor assumptions must be stripped?
4. Which owner files are affected?
5. Can it map directly, normalize, remain source-local, quarantine, or escalate?
6. What rejected timing assumptions must be recorded?

## 10. Acceptance criteria for this file

This file is acceptable if it prevents donor action economy leakage, gives D12 clear timing ownership, preserves owner-file boundaries, and makes combat one structured profile among many rather than the default model.



<!-- END D12-00_time_action_cadence_encounter_procedure_and_owner_boundaries.md -->


<!-- BEGIN D12-01_cadence_states_transition_triggers_and_scene_flow.md -->


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



<!-- END D12-01_cadence_states_transition_triggers_and_scene_flow.md -->


<!-- BEGIN D12-02_action_windows_initiative_sequencing_and_interruptions.md -->


# D12-02 — Action Windows, Initiative, Sequencing, and Interruptions

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Owner file: D12 timing and cadence doctrine

## 1. Purpose

This file defines how Astra assigns structured opportunities, determines sequencing, handles context-derived initiative, permits reactions, supports interruptions, and resolves simultaneous or multi-scale timing.

## 2. Action Window doctrine

An Action Window is a bounded opportunity for an actor, group, platform crew, environmental force, or opposition element to attempt something meaningful within a structured cadence.

An Action Window is not automatically:

- a combat turn;
- a six-second round;
- an action plus movement;
- a bonus action;
- one attack;
- an initiative pass;
- a grid activation;
- a narrative spotlight with no procedure;
- a universal timing allowance.

It is simply the procedural point where a participant may declare intent, commit risk or cost, call resolution if needed, and route consequences.

## 3. Default Action Window steps

A standard Action Window uses this ten-step sequence:

```yaml
action_window_steps:
  1: situation_update
  2: active_actor_declaration
  3: method_and_target_clarification
  4: cost_and_risk_preview
  5: commitment_point
  6: resolution_call_if_needed
  7: owner_file_handoff
  8: state_delta_checkpoint
  9: reaction_or_interruption_window_if_triggered
  10: continuation_or_transition_check
```

These steps are procedural order, not final runtime implementation.

## 4. Declaration requirements

A declaration is sufficient when D12 can identify:

- acting entity or force;
- desired intent;
- method or approach;
- target, area, object, actor, pressure, or abstract aim;
- whether timing matters;
- whether cost, risk, or exposure is involved;
- whether another actor or force may respond.

If the declaration lacks essential procedural clarity, D11 may ask a clarifying question, but D12 remains the timing owner.

## 5. Initiative as sequencing authority

Initiative means sequencing authority. It does not mean a universal roll.

D12 asks:

1. Is order obvious from posture, preparation, ambush, declared readiness, position, domain advantage, environmental trigger, or prior state?
2. If yes, use contextual sequencing.
3. If no, and order matters, call D02 to resolve sequencing uncertainty.
4. If multiple actors act at once, use simultaneous declaration and priority resolution.

## 6. Attribute relevance for sequencing

The relevant axis depends on declared method and scene pressure:

| Pressure | Possible axis |
|---|---|
| speed, reflex, precision | Finesse |
| noticing, sensing, hidden-state reading | Insight |
| planning, tactical interpretation, technical timing | Reason |
| forceful breach or bodily dominance | Vessel |
| social opening, presence, command, performance | Glamour |
| power pressure, aura, channeling, spiritual force | Animus |
| concealed cosmic timing | hidden owner-file pressure; Pneuma never exposed |

No single attribute is universal initiative.

## 7. Reactions

A Reaction is a bounded response opportunity created by a valid trigger.

Reactions require both:

1. a trigger; and
2. a permission source.

Valid permission sources include:

- declared posture;
- prepared action;
- guard, watch, overwatch, or readiness posture;
- Technique;
- Principle;
- oath;
- condition;
- access tag;
- object, relic, tool, implant, or platform system;
- domain advantage;
- environmental position;
- source-local retained procedure.

Astra does not grant every actor a generic reaction per round as default law.

## 8. Interruptions

An Interruption is a reaction that may alter sequencing before the triggering action fully resolves.

An interruption is valid only when:

- the trigger is visible or otherwise accessible to the responding entity;
- the permission source grants timing authority;
- the response can plausibly occur before or during the triggering action;
- the relevant owner file supports the attempted effect;
- D02 is called if timing or contest is uncertain.

Interruptions may:

- prevent an action;
- modify an action;
- create a contest;
- force a cost change;
- alter target or position;
- trigger harm or condition routing;
- shift cadence.

D12 defines timing permission. Owner files define effect content.

## 9. Simultaneous declaration

Simultaneous action is supported when actors act at the same time, ambushes collide, chase maneuvers overlap, platform crew actions occur in parallel, ritual and counter-ritual unfold together, social actors interject, or environmental pressure triggers during an actor's window.

Resolution priority may be determined by:

- context;
- preparedness;
- declared posture;
- D02 contest;
- domain alignment;
- cost overcommitment;
- relevant owner-file hook;
- source-local timing rule.

Simultaneous action must not be forced into a donor initiative order unless retained source-locally or explicitly supported.

## 10. Multi-scale action

Different scales may interact in the same scene, but they do not automatically share one identical action clock.

Scales include:

```yaml
acting_scales:
  - actor
  - group
  - platform
  - environment
  - faction
  - mixed
```

D12 resolves coexistence through primary cadence profile, secondary pressure profiles, declaration windows, priority resolution, and owner-file handoff.

Actor-scale actions, platform-scale operations, environmental pulses, and faction-scale pressure may overlap, but later owner files decide their actual state effects.

## 11. Anti-drift rules

- Do not treat Action Windows as donor turns.
- Do not give universal reactions.
- Do not force simultaneous action into initiative order by default.
- Do not make Finesse the only initiative axis.
- Do not collapse platform, actor, and environmental timing into one clock.
- Do not let D12 decide the mechanical effect of a Technique, item, condition, or faction response.

## 12. Acceptance criteria

This file is acceptable if it supports structured sequencing, context-derived initiative, trigger-based reactions, lawful interruptions, simultaneous action, and multi-scale coexistence without importing a donor action economy.



<!-- END D12-02_action_windows_initiative_sequencing_and_interruptions.md -->


<!-- BEGIN D12-03_round_exchange_beat_interval_and_time_scale_grammar.md -->


# D12-03 — Round, Exchange, Beat, Interval, and Time-Scale Grammar

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Owner file: D12 timing and cadence doctrine

## 1. Purpose

This file defines Astra's neutral timing language so donor terms such as round, turn, phase, watch, interval, clock, countdown, and faction turn do not become default Astra law.

## 2. Timing principle

Astra uses neutral timing containers. Specific procedures may define local durations, but D12 does not establish universal fixed durations for all structured play.

## 3. Core timing containers

D12 uses five timing containers:

```yaml
timing_containers:
  - beat
  - action_window
  - exchange
  - interval
  - time_scale_shift
```

## 4. Beat

A Beat is the smallest meaningful procedural moment.

A Beat may be:

- a warning sign;
- a glance;
- an opportunity cue;
- a reaction opening;
- a trigger;
- a reveal;
- a cost preview;
- a consequence cue;
- a hidden pressure pulse;
- a preparation window;
- a source-local timing signal.

A Beat is not necessarily a full action. D12 defines the procedural timing role of Beats. D11 presents them. Owner files decide whether a Beat carries mechanical effect.

## 5. Action Window

An Action Window is a bounded opportunity to act meaningfully. Its structure is defined in D12-02.

Action Window is not an Astra synonym for turn, action, movement, attack, initiative pass, or spotlight.

## 6. Exchange

An Exchange is one complete pass through the relevant action windows or pressure events needed to determine the next meaningful state of a structured scene.

An Exchange is not automatically:

- six seconds;
- one combat round;
- one full initiative pass;
- one dungeon turn;
- one chase round;
- one faction turn;
- one watch;
- one downtime unit.

Examples of an Exchange include:

- one clash and counter-movement;
- one round of social claim and response;
- one chase maneuver sequence;
- one stealth breach response;
- one ritual surge and counter-surge;
- one platform crew command cycle;
- one environmental hazard pulse.

The actual duration may vary by profile, owner file, source-local rule, or runtime implementation.

## 7. Interval

An Interval is a larger operational duration used when effort, pressure, or consequences accumulate over more than one exchange.

Intervals may apply to:

- extended tasks;
- recovery;
- research;
- crafting;
- repairs;
- surveillance;
- travel;
- environmental exposure;
- faction operations;
- acquisition;
- downtime;
- campaign arc pacing.

D12 defines when play shifts into interval handling. D13, D14, D15, D17, and D18 own the relevant interval procedures.

## 8. Time-Scale Shift

A Time-Scale Shift occurs when play moves from one timing container or cadence state to another.

Examples:

```text
Beat -> Action Window
Action Window -> Exchange
Exchange -> Interval
Exchange -> Free Play
Focused Scene -> Structured Exchange
Scene -> Travel
Downtime Interval -> Focused Scene
Faction Pressure -> Active Scene
Campaign Season -> Downtime Block
```

Every Time-Scale Shift should record unresolved pressure carried forward, retired, escalated, quarantined, or handed to another owner file.

## 9. Fixed duration policy

D12 does not set universal fixed durations for Beats, Action Windows, Exchanges, or Intervals.

Durations may come from:

- owner-file procedure;
- scene pressure;
- source-local retained timing;
- explicit canon promotion later;
- runtime implementation after doctrine is formalized.

Familiar donor durations are not defaults.

## 10. Donor timing terms

Donor terms are evidence, not Astra timing terms.

| Donor term | Possible D12 handling |
|---|---|
| round | exchange, source-local round, hazard pulse, quarantine |
| turn | action window, exchange, source-local turn, quarantine |
| phase | beat, exchange, source-local phase, escalation |
| watch | interval, travel handoff, source-local timing |
| clock | D10 pressure, D13 project, D14 travel risk, D15 faction operation, D18 arc pressure, source-local, escalation |
| initiative pass | action window sequence, source-local procedure, quarantine |
| downtime turn | D13 interval procedure, source-local procedure |
| faction turn | D15 operation, D18 campaign pacing, source-local procedure |

This table is not an equivalency table. It is a reminder that function must be identified first.

## 11. Pressure persistence

Pressure does not vanish because time scale changes. Time-scale shifts must state whether pressure is:

- carried forward;
- retired;
- escalated;
- quarantined;
- transferred to D10 unresolved pressure;
- transferred to D13/D14/D15/D17/D18;
- retained source-locally.

## 12. Acceptance criteria

This file is acceptable if it gives Astra a neutral timing grammar and prevents donor time units from becoming default doctrine.



<!-- END D12-03_round_exchange_beat_interval_and_time_scale_grammar.md -->


<!-- BEGIN D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md -->


# D12-04 — Checkpoints, Cost Commitment, Consequence Timing, and Handoffs

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Owner file: D12 timing and cadence doctrine

## 1. Purpose

This file defines the procedural checkpoints that determine when Astra calls resolution, previews cost and risk, commits costs, routes consequences, records state deltas, opens reactions, and transitions cadence.

D12 owns timing order. It does not own the content of resolution, resources, harm, world-state, or narration.

## 2. Checkpoint principle

Every meaningful structured action should pass through enough checkpoints to avoid hidden donor assumptions such as “costs happen after success,” “harm applies whenever narration says so,” “failed actions stop play,” or “world pressure appears without owner-file authority.”

## 3. Ten-checkpoint sequence

```yaml
structured_action_checkpoints:
  1: cadence_checkpoint
  2: declaration_checkpoint
  3: method_target_checkpoint
  4: cost_risk_preview_checkpoint
  5: commitment_checkpoint
  6: resolution_checkpoint
  7: consequence_routing_checkpoint
  8: state_delta_checkpoint
  9: reaction_interruption_checkpoint
  10: continuation_transition_checkpoint
```

The sequence is a doctrine grammar, not final runtime code.

## 4. Cadence checkpoint

Identify the current cadence state:

- Free Play;
- Focused Scene;
- Structured Exchange;
- Conflict Cadence;
- Extended Task Cadence;
- Transition / Time-Scale Shift.

This determines whether formal action windows, sequencing, exchanges, or transitions are needed.

## 5. Declaration checkpoint

Clarify the action enough to identify:

- actor;
- intent;
- method;
- target;
- timing pressure;
- potential responders;
- likely owner files.

D12 does not decide success at this checkpoint.

## 6. Method / target checkpoint

Identify which owner files are implicated:

- D05 for method, competency, skill, research, or procedure;
- D06 for Techniques, Principles, oaths, domains, and route expression;
- D08 for actor, form, substrate, companion, AI, or personhood issues;
- D09 for objects, tools, platforms, relics, implants, salvage, or repair targets;
- D10 for world-state, faction, relationship, economy, law, information, or pressure targets.

## 7. Cost / risk preview checkpoint

Visible costs and risks should be previewed before commitment when the acting character could plausibly know them.

This preview may include:

- visible resource cost;
- exposure;
- overdraw risk;
- likely harm risk;
- known time cost;
- known social or legal risk;
- likely object or platform strain;
- visible consequence pressure.

Hidden risks remain protected by owner files and D11 hidden-state presentation. D12 may mark hidden pressure as present or unknown, but it must not reveal hidden truth by default.

## 8. Commitment checkpoint

Declared costs, exposure, positioning commitments, overdraw, preparation expenditure, and action-window use commit before resolution unless a specific owner file or source-local rule says otherwise.

D03 is invoked when resource, reserve, overdraw, recharge, carrier, or resource-side backlash is involved.

D12 must not default to “pay only on success.”

## 9. Resolution checkpoint

D12 calls D02 only when uncertainty, opposition, risk, contested timing, hidden pressure, or consequence requires resolution.

D12 does not own:

- DN ladder;
- outcome bands;
- natural 20/natural 1 handling;
- opposed-check math;
- margin interpretation;
- defense/resistance check grammar.

If no roll is needed, the action may proceed to consequence routing or declared no-delta result.

## 10. Consequence routing checkpoint

Route outcomes to correct owner files:

| Owner | Routed consequence type |
|---|---|
| D03 | cost, overdraw, recharge, resource strain, resource-side backlash |
| D04 | breakthrough, transformation, advancement pressure |
| D05 | method, research, skill, training, procedural learning |
| D06 | Technique, Principle, oath, domain, route expression |
| D07 | harm, injury, condition, corruption, backlash consequence |
| D08 | actor, form, substrate, companion, AI, body continuity |
| D09 | object, relic, platform, implant, tool, salvage, repair state |
| D10 | world-state, faction, law, economy, reputation, relationship, information, pressure |
| D11 | player-facing and GM-facing presentation |
| D13–D18 | extended timing handoff where applicable |

D12 routes. It does not resolve content owned elsewhere.

## 11. State-delta checkpoint

Every meaningful action must produce at least one of:

```yaml
state_delta_checkpoint_outcome:
  - committed_delta
  - declared_no_delta_result
  - quarantined_unresolved_delta
  - owner_file_escalation
  - source_local_retained_effect
  - transition_note
```

This prevents meaningful actions from disappearing into narration without consequence tracking.

## 12. Reaction / interruption checkpoint

If the action creates a valid trigger, eligible entities may use reactions or interruptions under D12-02.

A reaction requires a trigger and permission source. An interruption must be timing-valid and may call D02 if sequencing or contest is uncertain.

## 13. Continuation / transition checkpoint

After each resolved action or exchange, decide whether:

- the same cadence continues;
- next action window opens;
- exchange completes;
- conflict continues;
- scene returns to Focused Scene or Free Play;
- scene escalates;
- scene transitions to D13, D14, D15, D17, or D18;
- unresolved pressure is recorded in D10;
- source-local timing persists;
- escalation or quarantine is required.

## 14. Anti-drift rules

- Do not call D02 when no uncertainty, risk, opposition, contested timing, hidden pressure, or consequence exists.
- Do not allow D12 to define outcome math.
- Do not allow D11 narration to skip cost or state-delta commitment.
- Do not allow costs to wait until after success by default.
- Do not resolve consequences inside D12 when another file owns them.

## 15. Acceptance criteria

This file is acceptable if D12 can define procedural order across structured scenes while preserving owner-file authority and preventing hidden donor timing assumptions.



<!-- END D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md -->


<!-- BEGIN D12-05_structured_scene_families_and_cadence_profiles.md -->


# D12-05 — Structured Scene Families and Cadence Profiles

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Owner file: D12 timing and cadence doctrine

## 1. Purpose

This file defines cadence profiles for major structured scene families. Cadence profiles are timing templates, not full subsystems.

A cadence profile identifies what timing usually matters, which participants may act, which checkpoints are emphasized, which owner files are likely invoked, and which donor assumptions must not become Astra law.

## 2. Cadence profile principle

D12 profiles support conversion without creating separate donor-shaped procedures for every scene type. A profile is not final mechanics, not balance math, not action economy, and not encounter construction.

## 3. Core profile record shape — not final schema

```yaml
cadence_profile_record:
  record_type: cadence_profile
  profile_name: string
  profile_status: doctrine_timing_template_not_final_schema
  scene_pressure: string
  usual_participants: []
  primary_timing_concern: string
  common_action_window_triggers: []
  likely_D02_roll_triggers: []
  likely_D03_cost_triggers: []
  likely_D07_consequence_hooks: []
  likely_D10_pressure_hooks: []
  likely_D11_presentation_needs: []
  source_local_retention_risks: []
  owner_file_handoffs: []
  rejected_donor_assumptions: []
```

Runtime Gate B or later schema doctrine may replace this shape.

## 4. Martial Conflict Profile

Used for combat, duels, ambushes, skirmishes, battles, monster attacks, and direct violence.

Primary timing concern: attack opportunity, movement pressure, defense timing, harm routing, interruption windows, and escalation.

Likely owner files:

- D02 resolution;
- D03 cost/backlash;
- D06 Techniques/domain expression;
- D07 harm/conditions;
- D08 actors;
- D09 weapons/tools/platforms;
- D10 world/faction response;
- D11 presentation;
- D16 opposition construction later.

Rejected donor assumptions:

- fixed combat rounds;
- fixed action categories;
- armor math;
- attack economy;
- challenge rating math;
- grid law;
- universal reaction allowance.

Martial conflict is one cadence profile among many. It is not D12's baseline for all structured scenes.

## 5. Social Conflict Profile

Used for debate, negotiation, intimidation, diplomacy, interrogation, trial, public persuasion, influence contest, and social standoff.

Primary timing concern: claim and counterclaim, leverage reveal, commitment, exposure, reputation pressure, relationship deltas, institutional response.

Likely owner files:

- D02 resolution;
- D05 methods;
- D06 Principles, oaths, domains where relevant;
- D10 relationships, factions, law, reputation;
- D11 presentation;
- D15 faction/relationship operations later.

Rejected donor assumptions:

- social hit points as default law;
- attitude tracks as universal;
- combat reskinning;
- automatic persuasion after one roll;
- donor status systems as Astra society.

## 6. Stealth / Infiltration Profile

Used for sneaking, hiding, surveillance, infiltration, evasion, ambush approach, tailing, security bypass, concealment, and escape from observation.

Primary timing concern: detection windows, exposure risk, patrol/environment beats, hidden-state protection, reaction triggers.

Likely owner files:

- D02 resolution;
- D05 methods;
- D07 conditions/harm if exposed;
- D09 tools/security objects;
- D10 hidden information/world response;
- D11 hidden-state presentation;
- D14 exploration/navigation later.

Rejected donor assumptions:

- passive perception law;
- grid hiding law;
- universal alert clock;
- donor stealth turns;
- automatic binary hidden/not-hidden states.

## 7. Chase / Pursuit Profile

Used for foot chases, mounted pursuit, vehicle pursuit, ship pursuit, escape sequences, hunting, interception, and pursuit through hostile terrain.

Primary timing concern: distance or position pressure, route choice, hazard beats, momentum, resource strain, and transition into capture, escape, or conflict.

Likely owner files:

- D02 resolution;
- D03 resource strain;
- D07 harm/hazards;
- D09 vehicles/platforms;
- D10 world response;
- D14 travel/navigation later;
- D16 opposition/hazard construction later.

Rejected donor assumptions:

- exact chase rounds;
- fixed zones;
- vehicle speed tables as Astra law;
- grid distances;
- automatic escape thresholds.

## 8. Ritual / Power Contest Profile

Used for rites, counter-rites, breakthroughs under pressure, domain clashes, summoning, sealing, large Techniques, psychic contests, and unstable power procedures.

Primary timing concern: preparation, channeling windows, interruption risk, overdraw, backlash, instability, breakthrough pressure, hidden pressure.

Likely owner files:

- D02 resolution;
- D03 cost, overdraw, backlash;
- D04 breakthrough/transformation where relevant;
- D06 route, Technique, domain expression;
- D07 corruption, backlash, harm;
- D10 world-state effects;
- D11 hidden/cosmic presentation.

Rejected donor assumptions:

- cultivation tribulation law as Astra default;
- spellcasting rounds;
- universal ritual clocks;
- donor metaphysics;
- automatic power scaling by scene phase.

## 9. Technical / System Standoff Profile

Used for hacking, engineering emergencies, lock bypass, device control, repair under pressure, countermeasures, sabotage, decoding, surveillance systems, and platform control.

Primary timing concern: access windows, countermeasure beats, tool/object state, progress under risk, interruption, system failure consequences.

Likely owner files:

- D02 resolution;
- D05 methods/research/procedure;
- D09 objects/platforms/tools;
- D10 information/security/world-state;
- D13 projects/repairs later;
- D17 acquisition/legality later.

Rejected donor assumptions:

- donor hacking rounds;
- netrunning action economies;
- tool DC tables as default;
- exact repair intervals;
- universal security alert tracks.

## 10. Exploration / Hazard Profile

Used for dangerous site navigation, room-by-room exploration, environmental exposure, trap approach, unstable terrain, unknown zones, watch/ambush tension, and discovery under risk.

Primary timing concern: scouting, approach posture, hazard pulses, discovery beats, resource pressure, site transitions.

Likely owner files:

- D02 resolution;
- D05 methods;
- D07 hazard/harm;
- D09 objects/tools;
- D10 information/world memory;
- D14 exploration/travel later;
- D16 hazards later.

Rejected donor assumptions:

- universal hex turns;
- dungeon turns;
- random encounter checks as core law;
- OSR exploration procedure as default;
- automatic mapping scale.

## 11. Platform / Crew Cadence Profile

Used for vehicles, ships, mechs, bases, mobile fortresses, stations, large companions, crewed constructs, or other multi-actor platforms.

Primary timing concern: crew role windows, platform-scale action, actor-scale action, system strain, command sequencing, simultaneous operation.

Likely owner files:

- D02 resolution;
- D03 resource/heat/strain;
- D07 platform harm if relevant;
- D08 actors/crew;
- D09 platform/object state;
- D10 faction/world response;
- D14 travel later;
- D16 platform opposition later;
- D17 maintenance/requisition later.

Rejected donor assumptions:

- platform turns equal actor turns;
- tactical frame action economy;
- license timing as default;
- hardpoint timing as universal;
- crew roles as fixed Astra classes.

## 12. Mixed scenes

Mixed scenes may combine cadence profiles. One profile should be declared primary for cadence, while secondary profiles identify pressure and owner-file handoffs.

Examples:

- stealth infiltration becomes martial conflict after exposure;
- chase includes platform and environmental hazard pressure;
- social conflict includes ritual power contest pressure;
- technical standoff occurs during platform combat;
- exploration hazard becomes rescue conflict.

Mixed scenes should not apply all profiles equally without priority. If no primary profile can be chosen, the scene should be split, quarantined, or escalated.

## 13. Acceptance criteria

This file is acceptable if D12 can classify structured scene families and route timing concerns without defining full subsystems or making combat universal.



<!-- END D12-05_structured_scene_families_and_cadence_profiles.md -->


<!-- BEGIN D12-06_source_local_timing_donor_procedure_mapping_and_escalation.md -->


# D12-06 — Source-Local Timing, Donor Procedure Mapping, and Escalation

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Owner file: D12 timing and cadence doctrine

## 1. Purpose

This file defines how Astra handles donor timing systems without importing donor procedure as default law.

D12 must convert timing by function, not by label.

## 2. Donor timing principle

A donor timing label is evidence only. Labels such as round, turn, phase, watch, shift, interval, clock, countdown, faction turn, downtime turn, initiative pass, reaction phase, morale phase, boss phase, travel turn, and hacking round do not become Astra timing terms by default.

## 3. Functional donor timing mapping ladder

Use this ladder for every donor timing construct:

```yaml
donor_timing_mapping_ladder:
  1: identify_donor_timing_function
  2: identify_affected_cadence_state
  3: identify_controlled_feature
  4: identify_owner_files_affected
  5: choose_lawful_handling
  6: record_rejected_donor_assumptions
```

Controlled features may include sequencing, interval, pressure, recharge, countdown, transition, hazard pulse, opportunity window, faction operation, project progress, or source-local pacing.

## 4. Lawful handling outcomes

Every donor timing construct must receive one lawful handling:

1. direct Astra mapping;
2. normalized Astra mapping;
3. source-local retained construct;
4. quarantined construct pending later doctrine;
5. escalated doctrine problem.

No timing construct receives hidden sixth handling.

## 5. Direct Astra mapping

Use direct mapping only when the donor timing construct already matches D12 grammar without importing donor law.

Example: a donor procedure states that each side has one meaningful opportunity before the next danger pulse. If no fixed donor action economy, duration, or balance assumption is imported, this may map directly to an Exchange plus hazard pulse.

## 6. Normalized Astra mapping

Use normalized mapping when the donor procedure has a reusable timing function, but donor labels, durations, math, action economy, recharge assumptions, or pacing must be stripped.

Examples:

- donor chase round -> Exchange inside Chase / Pursuit profile;
- donor hacking round -> Technical / System Standoff exchange;
- donor boss phase -> source-local phase or normalized transition pressure depending scope;
- donor exploration turn -> D14 handoff or source-local timing, not D12 default law.

## 7. Source-local retained timing

Use source-local retention when a timing procedure is valuable inside a converted source but unsafe as core Astra doctrine.

Valid source-local timing examples:

- a named ritual's seven-phase collapse;
- a specific dungeon alarm countdown;
- a boss script used only in one converted adventure;
- a source-specific faction clock;
- a local travel hazard interval;
- a campaign-specific doom track;
- a donor adventure's timed rescue sequence.

Source-local timing must declare:

- source boundary;
- preserved timing function;
- stripped or rejected donor assumptions;
- whether it can interact with D12 containers;
- what cannot be generalized;
- review requirement for reuse.

## 8. Quarantined timing constructs

Quarantine when safe mapping is blocked by:

- extraction damage;
- missing rows in a timing table;
- collapsed statblock or procedure text;
- unsupported action economy;
- unsupported resource/recharge cycle;
- missing owner file;
- unsupported donor metaphysics;
- unclear state mutation;
- unclear player-facing versus GM-facing timing;
- hidden information leakage risk;
- multi-scale timing conflict that cannot be resolved by existing profiles.

Quarantine is better than fake certainty.

## 9. Escalated doctrine problems

Escalate when repeated or high-impact pressure exposes a missing Astra timing distinction.

Examples:

- repeated need for formal countdown pressure doctrine;
- repeated simultaneous actor/platform/faction timing conflict;
- repeated morale/reaction timing across bestiary and encounter packets;
- repeated stealth alert-state timing beyond profile support;
- repeated time-loop, rewind, causality, or retroactive action procedure;
- repeated faction-turn pressure that cannot wait for D15;
- repeated long ritual phase timing that interacts with D03, D04, D06, and D07.

Escalation must name the likely owner file or proposed future file.

## 10. Clock and countdown routing

Clock-like systems must be routed by function:

| Donor function | Likely owner |
|---|---|
| unresolved world pressure | D10 |
| project progress | D13 |
| travel or exploration risk | D14 |
| faction or institution operation | D15 |
| economy scarcity/acquisition pressure | D17 |
| campaign arc, season, state aging | D18 |
| scene transition pressure | D12 |
| bounded source procedure | source-local retention |
| unsupported state mutation | quarantine or escalation |

D12 does not adopt a universal clock system.

## 11. Rejected timing assumptions

Conversion must record rejected timing assumptions, including:

- donor fixed round duration;
- donor action economy;
- donor initiative method;
- donor recharge interval;
- donor encounter pacing;
- donor exploration turn structure;
- donor faction turn law;
- donor clock mechanics;
- donor boss phase script;
- donor random encounter interval;
- donor travel time scale;
- donor platform action economy.

Rejected does not mean erased. It means not adopted as Astra law.

## 12. Donor timing mapping record — not final schema

```yaml
donor_timing_mapping_record:
  record_type: donor_timing_mapping
  record_status: doctrine_control_shape_not_final_schema
  donor_label: string
  donor_function_summary: string
  affected_cadence_state: string
  controlled_feature: sequencing | interval | pressure | recharge | countdown | transition | hazard_pulse | opportunity_window | faction_operation | project_progress | source_local_pacing | other
  mapped_d12_container: beat | action_window | exchange | interval | time_scale_shift | cadence_profile | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```

Runtime Gate B or later schema doctrine may replace this shape.

## 13. Acceptance criteria

This file is acceptable if donor timing systems can be mapped, normalized, retained source-locally, quarantined, or escalated without treating donor labels as Astra timing law.



<!-- END D12-06_source_local_timing_donor_procedure_mapping_and_escalation.md -->


<!-- BEGIN D12-07_records_not_final_schema_and_conversion_handoff_shapes.md -->


# D12-07 — Records, Not-Final Schema, and Conversion Handoff Shapes

Status: doctrine-pack draft  
Version: v0_1_draft  
Generated: 2026-06-02  
Owner file: D12 timing and cadence doctrine

## 1. Purpose

This file defines lightweight record shapes for D12 doctrine and conversion handoff. These records are not final runtime schemas. They exist to make cadence, action windows, exchanges, reactions, transitions, profiles, donor timing mappings, unresolved pressure, and owner-file handoffs auditable.

## 2. Record posture

All record shapes in this file are:

```yaml
record_posture:
  schema_status: not_final_schema
  purpose: doctrine_facing_and_conversion_facing_control_shape
  runtime_status: Gate_B_may_replace_or_formalize_later
  canon_status: not_canon_by_record_existence
```

A record appearing in D12 does not create canon, runtime state, sourcebook prose, or live-play authority.

## 3. Cadence State Record

```yaml
cadence_state_record:
  record_type: cadence_state
  record_status: doctrine_control_shape_not_final_schema
  current_state: free_play | focused_scene | structured_exchange | conflict_cadence | extended_task_cadence | transition_time_scale_shift
  primary_profile: martial_conflict | social_conflict | stealth_infiltration | chase_pursuit | ritual_power_contest | technical_system_standoff | exploration_hazard | platform_crew | mixed | none
  secondary_profiles: []
  trigger_for_state: string
  active_owner_files: []
  hidden_pressure_present: true | false | unknown
  source_local_timing_present: true | false
  source_local_boundary: string | null
  notes: string
```

Hidden pressure may be marked but not revealed. D11 and owner files govern hidden-state presentation.

## 4. Action Window Record

```yaml
action_window_record:
  record_type: action_window
  record_status: doctrine_control_shape_not_final_schema
  acting_entity_ref: string
  acting_scale: actor | group | platform | environment | faction | mixed
  declared_intent: string
  method_or_approach: string
  target_refs: []
  visible_cost_risk_preview: string
  hidden_pressure_marker: present | absent | unknown | protected
  commitment_made: true | false
  resolution_required: true | false
  resolution_owner: D02 | none | source_local
  consequence_owner_files: []
  reaction_window_opened: true | false
  transition_check_required: true
  notes: string
```

Action Window records must not be treated as fixed donor turns.

## 5. Exchange Record

```yaml
exchange_record:
  record_type: exchange
  record_status: doctrine_control_shape_not_final_schema
  exchange_id: string
  cadence_profile: martial_conflict | social_conflict | stealth_infiltration | chase_pursuit | ritual_power_contest | technical_system_standoff | exploration_hazard | platform_crew | mixed
  action_window_refs: []
  pressure_event_refs: []
  exchange_result: continued | shifted | escalated | resolved | interrupted | quarantined
  unresolved_pressure_refs: []
  owner_file_handoffs: []
  source_local_boundary: string | null
```

An Exchange Record is not a universal round record.

## 6. Reaction / Interruption Record

```yaml
reaction_interruption_record:
  record_type: reaction_or_interruption
  record_status: doctrine_control_shape_not_final_schema
  responding_entity_ref: string
  trigger_event_ref: string
  permission_source: posture | prepared_action | technique | principle | oath | condition | access_tag | object | platform | domain_advantage | source_local_rule | other
  timing_effect: before_resolution | during_resolution | after_resolution | prevents_action | modifies_action | creates_contest | other
  valid: true | false | needs_review
  resolution_owner: D02 | D06 | D07 | D09 | D10 | source_local | none
  notes: string
```

This record prevents reactions from becoming universal freebies.

## 7. Transition Record

```yaml
transition_record:
  record_type: cadence_transition
  record_status: doctrine_control_shape_not_final_schema
  from_cadence: string
  to_cadence: string
  transition_trigger: string
  pressure_carried_forward: []
  pressure_retired: []
  pressure_escalated: []
  pressure_quarantined: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

Transitions must preserve unresolved pressure rather than silently erasing it.

## 8. Cadence Profile Record

```yaml
cadence_profile_record:
  record_type: cadence_profile
  record_status: doctrine_control_shape_not_final_schema
  profile_name: martial_conflict | social_conflict | stealth_infiltration | chase_pursuit | ritual_power_contest | technical_system_standoff | exploration_hazard | platform_crew | mixed
  scene_pressure: string
  usual_participants: []
  primary_timing_concern: string
  common_action_window_triggers: []
  likely_roll_triggers: []
  likely_cost_triggers: []
  likely_consequence_hooks: []
  likely_world_pressure_hooks: []
  owner_file_handoffs: []
  rejected_donor_assumptions: []
```

Profiles are timing templates, not full scene subsystems.

## 9. Donor Timing Mapping Record

```yaml
donor_timing_mapping_record:
  record_type: donor_timing_mapping
  record_status: doctrine_control_shape_not_final_schema
  donor_label: string
  donor_function_summary: string
  mapped_d12_container: beat | action_window | exchange | interval | time_scale_shift | cadence_profile | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```

This record prevents false equivalency tables.

## 10. Owner-File Handoff Record

```yaml
owner_file_handoff_record:
  record_type: owner_file_handoff
  record_status: doctrine_control_shape_not_final_schema
  source_d12_checkpoint: cadence | declaration | method_target | cost_risk_preview | commitment | resolution | consequence_routing | state_delta | reaction_interruption | continuation_transition
  owner_file: D02 | D03 | D04 | D05 | D06 | D07 | D08 | D09 | D10 | D11 | D13 | D14 | D15 | D17 | D18 | source_local | escalation
  handoff_reason: string
  timing_context: string
  hidden_state_boundary: string | null
  source_local_boundary: string | null
  notes: string
```

D12 records timing handoff. It does not perform the owner file's procedure.

## 11. Unresolved Timing Pressure Record

```yaml
unresolved_timing_pressure_record:
  record_type: unresolved_timing_pressure
  record_status: doctrine_control_shape_not_final_schema
  pressure_summary: string
  originating_cadence: string
  pressure_type: countdown | delayed_consequence | opportunity_window | environmental_pulse | faction_response | ritual_instability | platform_strain | hidden_pressure | source_local | other
  current_owner: D10 | D13 | D14 | D15 | D17 | D18 | source_local | quarantine | escalation
  visibility_scope: player_visible | gm_visible | hidden | mixed
  next_review_trigger: string
  notes: string
```

This record helps prevent pressure from disappearing during time-scale shifts.

## 12. Hidden-state safeguards

Any record may state that hidden pressure exists or is unknown. Records must not reveal protected hidden truth unless the relevant owner file and D11 presentation doctrine allow it.

## 13. Acceptance criteria

This file is acceptable if it provides enough control shapes for conversion and future runtime handoff while clearly preventing those shapes from becoming final schemas or runtime authority.



<!-- END D12-07_records_not_final_schema_and_conversion_handoff_shapes.md -->


<!-- BEGIN D12-09_integration_checklists_ddr_register_and_acceptance_criteria.md -->


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



<!-- END D12-09_integration_checklists_ddr_register_and_acceptance_criteria.md -->
