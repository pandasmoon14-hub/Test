# D02-06 Group, Extended, and Dramatic Tasks

## Purpose

This file defines how D02 resolves group actions and tasks that cannot be fairly handled by a single roll.

## Group check types

| Type | Use |
|---|---|
| Lead + support | One actor rolls; allies help through modifier, advantage, DN reduction, progress units, or risk-sharing. |
| Majority | Group succeeds if most members succeed. |
| Weakest link | One failure can compromise the group. Use sparingly. |
| Best link | One qualified actor can solve the task for the group. |
| Accumulated | Each actor contributes progress toward a shared threshold. |

D02 should choose the group model based on the fiction and consequence.

## Lead + support

Use when one actor is clearly primary.

Support may provide:

- +2 or +5 modifier;
- advantage;
- lowered DN;
- extra progress unit;
- consequence mitigation;
- information rider.

Support can create risk for helpers if the action fails or Fractures.

## Majority checks

Use when group competence generally matters but individual failure can be absorbed.

Examples:

- group stealth through moderate risk;
- coordinated social effort;
- group endurance over a journey segment;
- crowd containment;
- broad research team effort.

## Weakest-link checks

Use only when one failure genuinely compromises the whole group.

Examples:

- crossing a fragile bridge as linked party;
- synchronized ritual where every participant must maintain role;
- group stealth through direct line-of-sight guard post.

Weakest-link checks should not be the default, because they punish party size.

## Best-link checks

Use when only one competent success is needed.

Examples:

- someone remembers a fact;
- one engineer identifies the fault;
- one scout spots the safe path;
- one diplomat knows the protocol.

## Accumulated group checks

Use when effort stacks.

Examples:

- repairing a platform;
- researching a mystery;
- fortifying a settlement;
- evacuating civilians;
- containing corruption;
- negotiating a broad alliance;
- salvaging a wreck.

## Extended tasks

Use extended tasks for goals requiring accumulated progress across time, scenes, or intervals.

Recommended structure:

```yaml
extended_task:
  task_ref: string
  goal: string
  progress_required: int
  current_progress: int
  roll_interval: string
  consequence_pressure: []
  cost_profile: []
  failure_pressure: []
  owner_handoffs: []
```

## Progress units

Recommended progress conversion:

| Outcome | Progress |
|---|---:|
| Ascendant | +3 |
| Clear | +2 |
| Fractured | +1 plus complication/cost |
| Receded | 0, but information/cost/exposure may occur |
| Sundered | -1 or complication/escalation |

Progress units are a D02 resolution tool. D05, D09, D10, and other owner files define what progress represents.

## Dramatic tasks

Dramatic tasks are extended tasks under acute pressure.

They may include:

- limited number of rounds;
- rising DN;
- escalating consequence;
- resource depletion;
- opposition progress;
- hazard clock retained source-locally;
- public or hidden D10 pressure.

D02 does not require physical dice timers or metacurrency.

## Race against opposition

For opposing extended tasks, track each side’s progress.

Possible end conditions:

- first to threshold wins;
- threshold before time expires;
- compare final progress at deadline;
- decisive margin creates Ascendant/Severe consequence;
- source-local ending condition.

## Acceptance criteria

A group/extended ruling is valid when it:

1. chooses the correct group model;
2. avoids punishing group size by default;
3. uses progress for extended work;
4. routes method to D05;
5. routes object/platform work to D09;
6. routes persistent world consequences to D10;
7. avoids physical dice or metacurrency requirements.
