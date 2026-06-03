# D11-06 Player-Facing vs GM-Facing Summary Modes

## Purpose

This file defines how D11 separates player-safe presentation from GM/backend summaries, raw register inspection, state-audit output, and escalation notes. D11 remains interface doctrine. It controls presentation modes, not the state records themselves.

## Core rule

D11 must maintain strict separation between player-facing presentation, GM-facing summary, state-audit inspection, and escalation output. Player-facing summaries may contain only visible, known, inferable, or lawfully revealed information. GM-facing summaries may include hidden state, raw deltas, unresolved pressures, and backend notes, but must label them clearly.

## Summary modes

Player-facing narration is immersive and player-safe if filtered. Party-known summary is concise recap of player-safe information. GM-facing summary includes backend truth, hidden facts, deltas, pressures, and reveal paths. State-audit mode validates support. Escalation mode flags missing doctrine/state or unsafe narration.

## Player-facing narration

May include visible environment, sensory details, public information, party-known information, visible consequences, inferable signals, rumors framed as rumors, uncertainty language, available choices, and assessment results presented through D02/D11 rules.

Must not include backend truth not discovered, GM-only notes, raw hidden register data, exact hidden Pneuma/cosmic modifiers, hidden faction controller names, concealed object identity, unrevealed source-local clocks, or state-audit warnings.

## Party-known summary

May include confirmed discoveries, accepted rumors labeled as rumors, known debts/warrants/grudges/faction pressure, known object states, known injuries/resources, known unresolved pressures, map/location knowledge, and known false beliefs if the party believes them.

## GM-facing summary

May include backend truth, hidden facts, secret holders, unresolved pressures, owner-file deltas, source-local status, hidden consequence, delayed consequence, escalation conditions, and reveal paths. It must not be written so it can accidentally be pasted as player narration.

## State-audit mode

State-audit mode answers what records support narration, which owners are touched, whether hidden facts are revealed, whether source-local systems are being generalized, whether persistent canon is invented, whether D02 outcomes are presented correctly, and whether handoffs are missing.

## Escalation mode

Escalation activates when D11 cannot lawfully present a requested detail because owner state is missing, hidden truth lacks reveal path, source-local conflict exists, D02 outcome mismatches, donor assumptions are leaking, or Pneuma exposure risk exists.

## Raw register inspection

Raw register inspection belongs only in GM-facing or state-audit mode. Player-facing narration translates records into effects.

## Delta summaries

Player-facing summaries describe visible effects: reserve charge gone, wound bleeding, relic cracked, guild knows someone interfered. GM-facing summaries identify owner records: D03 reserve spent, D07 bleeding condition, D09 relic instability, D10 faction-known interference.

## Unresolved pressure dashboard

D11 may support GM-facing unresolved pressure dashboards showing pressure type, owner, severity, visibility, scope, surfacing intensity, escalation/decay/resolution conditions, and player-facing signal used or pending. Dashboards are not player-facing unless filtered.

## Source-local summaries

Source-local summaries must be labeled as local. Player-facing output translates the mechanic into visible effects.

## Contamination prevention

D11 blocks GM truth in player narration, rumor as narrator fact, raw register dump in player view, GM summary in immersive second person, source-local clocks as universal systems, hidden Pneuma as numbers, and state-audit warnings inside scene prose.

## Record shape

```yaml
d11_summary_mode_record:
  summary_ref: string
  mode: string
  player_safe: boolean
  source_records:
    D00: []
    D01: []
    D02: []
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  visible_content: []
  inferable_content: []
  hidden_content_not_player_safe: []
  raw_register_refs: []
  owner_deltas: []
  unresolved_pressures: []
  assessment_summaries: []
  source_local_status: []
  escalation_flags: []
  lawful_reveal_paths: []
```
