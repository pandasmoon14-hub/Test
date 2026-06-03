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
