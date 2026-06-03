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
