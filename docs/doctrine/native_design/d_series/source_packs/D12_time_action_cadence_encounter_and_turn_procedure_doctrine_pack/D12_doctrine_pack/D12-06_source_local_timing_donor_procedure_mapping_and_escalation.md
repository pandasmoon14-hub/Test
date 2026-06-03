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
