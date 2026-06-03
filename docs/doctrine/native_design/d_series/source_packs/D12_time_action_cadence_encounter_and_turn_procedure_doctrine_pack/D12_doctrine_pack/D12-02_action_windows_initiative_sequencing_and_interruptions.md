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
