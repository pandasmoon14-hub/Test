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
