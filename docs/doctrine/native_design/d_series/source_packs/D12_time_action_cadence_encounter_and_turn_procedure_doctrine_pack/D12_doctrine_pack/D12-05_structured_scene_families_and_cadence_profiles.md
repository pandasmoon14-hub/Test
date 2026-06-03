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
