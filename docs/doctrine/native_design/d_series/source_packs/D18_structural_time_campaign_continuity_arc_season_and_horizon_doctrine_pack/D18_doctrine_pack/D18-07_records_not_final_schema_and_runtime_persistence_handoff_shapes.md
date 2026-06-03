# D18-07 — Records, Integration Checklists, Anti-Drift Rules, and Runtime Persistence Handoff Shapes

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18-07 defines lightweight **not-final-schema** record shapes and final integration controls so campaign continuity, arc promises, seasons, state aging, progression horizons, source-local campaign structures, time skips, payoff scale, dimensional rotation, and donor structural-time systems remain auditable during conversion, canon review, future runtime design, and eventual play.

These are doctrine-facing and conversion-facing controls. They are not final runtime schemas, save-state schemas, context-packet formats, campaign calendar implementations, or live-play GM procedures.

## Record family list
```text
Structural Time State Record
Continuity Lifecycle Record
Arc Promise / Question Record
Pacing / Contrast / Payoff Budget Record
Season Throughline / Seam Record
Long-Horizon Trajectory / Phase / Rotation Record
Transformation / Breakthrough / Major Change Spacing Record
Time Skip / State Aging / Pruning Record
Donor Structural-Time Mapping Record
Runtime Persistence Handoff Note Record
Owner-file handoff / unresolved structural-time pressure
```

## 1. Structural Time State Record
```yaml
structural_time_state_record:
  record_type: structural_time_state
  state_id: string
  state_summary: string
  owner_file_primary: D04 | D07 | D08 | D09 | D10 | D13 | D15 | D16 | D17 | D18 | source_local | unknown
  owner_file_handoffs: []
  half_life: permanent | durable_mutable | active_transient | ephemeral | source_local_half_life | quarantined_half_life | escalated_half_life
  salience: critical | high | medium | low | background | hidden | source_local | quarantined
  continuity_layer: foreground | background | hidden | source_local | mixed
  activity_status: active | dormant | archived | retired | source_local | quarantined | escalated
  capture_reason: identity | advancement | transformation | persistent_harm | relationship | obligation | faction | law | world_state | domain | object_state | recurring_threat | arc_promise | season_throughline | source_local_continuity | canon_candidate | other
  retrieval_triggers: []
  reactivation_triggers: []
  hidden_state_boundary: player_visible | gm_visible | backend_hidden | source_local_hidden | mixed
  notes: string
```

## 2. Continuity Lifecycle Record
```yaml
continuity_lifecycle_record:
  record_type: continuity_lifecycle
  lifecycle_id: string
  state_ref: string
  capture_status: captured | not_captured | promoted_after_initial_omission | disputed_capture | source_local_capture | quarantined
  storage_status: stored_in_owner_file | stored_in_D18_index | missing_owner_storage | source_local_storage | quarantined_storage
  retrieval_status: not_yet_retrieved | retrieved_for_arc | retrieved_for_season | retrieved_for_horizon | retrieved_for_reconciliation | retrieved_for_runtime_handoff | retrieval_blocked | source_local_retrieval
  reconciliation_status: none_required | confirmed_old_state | confirmed_new_state | merged_states | reinterpreted_ambiguous_state | promoted | downgraded | marked_source_local | quarantined | escalated | retired_with_reason | continuity_repair_note_created
  aging_status: unchanged | progressed | decayed | intensified | stabilized | resolved | partially_resolved | transformed | split | merged | dormant | archived | retired | lost | expired | evolved_offscreen | source_local_closed | source_local_continues | quarantined | escalated
  last_review_context: arc | season | time_skip | phase_transition | contradiction | source_local_boundary | canon_candidate_review | runtime_handoff | other
  notes: string
```

## 3. Arc Promise / Question Record
```yaml
arc_promise_question_record:
  record_type: arc_promise_question
  arc_id: string
  arc_title_or_label: string
  arc_promise: []
  central_question_or_pressure: string
  question_state: opened | active | complicated | partially_answered | answered | deferred_to_season | deferred_to_horizon | transformed_into_new_question | retired | archived | source_local | quarantined | escalated
  primary_pressure_type: threat_pressure | mystery_pressure | faction_pressure | relationship_pressure | domain_pressure | resource_pressure | time_pressure | travel_pressure | legal_pressure | identity_pressure | breakthrough_pressure | recovery_pressure | source_local_pressure | mixed
  payoff_scale: scene_payoff | arc_payoff | season_payoff | campaign_phase_payoff | long_horizon_payoff | canon_candidate_payoff | source_local_payoff
  required_continuity_refs: []
  useful_amplifier_refs: []
  background_texture_refs: []
  hidden_retrieval_refs: []
  crisis_type: combat_crisis | social_crisis | legal_crisis | faction_crisis | mystery_reveal | resource_collapse | identity_test | breakthrough_attempt | domain_claim | platform_failure | project_deadline | escape_window | moral_decision | source_local_crisis | mixed
  closure_outcome: unresolved | resolved | resolved_with_cost | partially_resolved | transformed | deferred_to_season | deferred_to_horizon | opened_new_arc | retired_pressure | archived_pressure | dormant_pressure | failed_forward | quarantined | escalated | source_local_closure
  owner_file_handoffs: []
  notes: string
```

## 4. Pacing / Contrast / Payoff Budget Record
```yaml
pacing_contrast_payoff_budget_record:
  record_type: pacing_contrast_payoff_budget
  pacing_id: string
  arc_or_season_ref: string
  escalation_state: escalating | consolidating | breathing_room | crisis_approaching | crisis_active | denouement | stagnant | fatigued | source_local
  consolidation_modes: []
  payoff_scale_budgeted: scene_payoff | arc_payoff | season_payoff | campaign_phase_payoff | long_horizon_payoff | canon_candidate_payoff | source_local_payoff
  payoff_status: unspent | partially_spent | spent | deferred | transformed | overdrawn | misallocated | quarantined | escalated
  fatigue_risk: none | low | medium | high | active
  stagnation_risk: none | low | medium | high | active
  wrong_scale_repair_risk: none | low | medium | high | active
  notes: string
```

## 5. Season Throughline / Seam Record
```yaml
season_throughline_seam_record:
  record_type: season_throughline_seam
  season_id: string
  season_label: string
  season_throughline: survival_under_pressure | territory_or_domain_stabilization | faction_entanglement | settlement_or_platform_recovery | mystery_or_hidden_truth_exposure | war_or_campaign_conflict | relationship_network_realignment | economic_or_resource_crisis | training_and_breakthrough_preparation | identity_transformation | realm_or_route_transition | institutional_ascension | exploration_of_new_region | recovery_after_catastrophe | source_local_throughline | mixed
  season_promise: string
  active_arc_refs: []
  season_payoff_state: season_throughline_unresolved | season_throughline_resolved | season_throughline_resolved_with_cost | season_throughline_partially_resolved | season_throughline_transformed | season_throughline_deferred_to_horizon | season_throughline_failed_forward | season_throughline_retired | season_throughline_archived | season_throughline_split_into_new_season | season_throughline_quarantined | season_throughline_escalated | source_local_season_payoff
  active_state_refs: []
  dormant_state_refs: []
  archive_state_refs: []
  retirement_state_refs: []
  carry_forward_refs: []
  closure_list: []
  continuation_list: []
  reset_type: none | soft_reset | active_state_reset | premise_shift | location_shift | faction_landscape_shift | resource_baseline_shift | power_envelope_review | time_skip_reset | cast_or_spotlight_shift | source_local_reset | hard_reset_explicit_authority_only
  continuity_laundering_review: passed | failed | requires_reconciliation | quarantined | escalated
  false_reset_review: passed | failed | requires_new_baseline | source_local | quarantined
  seam_status: not_reached | pending | completed | incomplete_closure | incomplete_continuation | overloaded | quarantined | escalated
  owner_file_handoffs: []
  notes: string
```

## 6. Long-Horizon Trajectory / Phase / Rotation Record
```yaml
long_horizon_trajectory_phase_rotation_record:
  record_type: long_horizon_trajectory_phase_rotation
  horizon_id: string
  long_horizon_trajectory: survival_to_stability | local_actor_to_regional_force | wanderer_to_domain_holder | apprentice_to_master | mortal_to_ascendant | isolated_party_to_institutional_power | crew_to_platform_power | fugitive_to_legitimate_authority | ignorance_to_cosmic_understanding | broken_world_to_rebuilt_order | sect_member_to_sect_founder | scavenger_to_artificer_power | source_local_trajectory | mixed
  campaign_phase: local_survival | local_stability | regional_emergence | faction_entanglement | institutional_recognition | domain_responsibility | settlement_or_platform_stewardship | inter_realm_or_interstellar_access | mythic_or_apex_pressure | ascendant_conflict | legacy_or_succession | post_apex_transformation | source_local_phase
  power_envelope: below_pressure | near_pressure | above_old_pressure | new_axis_required | consolidation_needed | overinflated | source_local_envelope
  foreground_axes: []
  supporting_axes: []
  resting_axes: []
  saturated_axes: []
  emerging_axes: []
  blocked_axes: []
  source_local_axes: []
  dimensional_rotation_state: not_needed | recommended | active | overdue | blocked | source_local | quarantined | escalated
  escalation_consolidation_posture: escalation | consolidation | mixed | wrong_scale_escalation | stagnation | inflation_risk | source_local
  horizon_promise_state: undefined_open_sandbox | emerging_horizon | declared_horizon | phase_horizon | seasonal_horizon | long_horizon_apex | post_apex_continuation | source_local_horizon | quarantined_horizon
  long_middle_status: not_in_long_middle | healthy | busy_but_stagnant | overloaded | payoff_starved | dimensionally_collapsed | retrieval_failure | continuity_overload | source_local | quarantined | escalated
  owner_file_handoffs: []
  notes: string
```

## 7. Transformation / Breakthrough / Major Change Spacing Record
```yaml
transformation_breakthrough_spacing_record:
  record_type: transformation_breakthrough_spacing
  spacing_id: string
  major_change_kind: major_breakthrough | realm_tier_phase_transition | identity_altering_transformation | route_defining_oath_or_principle_shift | domain_claim | platform_acquisition_or_major_upgrade | settlement_or_domain_founding | faction_rank_change | institutional_legitimacy_shift | major_relationship_reconfiguration | recurring_threat_retirement | long_horizon_truth_reveal | legacy_transition | source_local_phase_change
  owner_file_primary: D04 | D06 | D08 | D09 | D10 | D15 | D16 | D17 | D18 | source_local | unknown
  spacing_state: too_soon | well_timed | delayed_for_consolidation | reserved_for_season_payoff | reserved_for_phase_payoff | reserved_for_horizon_payoff | blocked_by_owner_file | source_local_spacing | quarantined | escalated
  payoff_scale: arc_payoff | season_payoff | campaign_phase_payoff | long_horizon_payoff | source_local_payoff
  consolidation_required_before: true | false | unknown
  consolidation_required_after: true | false | unknown
  notes: string
```

## 8. Time Skip / State Aging / Pruning Record
```yaml
time_skip_state_aging_pruning_record:
  record_type: time_skip_state_aging_pruning
  time_advance_id: string
  time_advance_trigger: end_of_arc | end_of_season | downtime_interval | downtime_season | large_time_skip | travel_span | recovery_period | training_period | project_interval_sequence | faction_operation_cycle | domain_evolution_cycle | settlement_growth_period | platform_refit_period | campaign_phase_transition | source_local_phase_transition | continuity_overload_review | runtime_context_pruning_review | canon_candidate_review
  time_advance_scale: scene_to_scene | session_to_session | arc_interval | downtime_interval | season_interval | months | years | generation | realm_or_route_transition | interstellar_or_interrealm_span | post_catastrophe_span | source_local_span | unknown_span
  affected_state_refs: []
  aging_outcomes: []
  pressure_decay_states: []
  pressure_intensification_states: []
  retirement_refs: []
  archive_refs: []
  reactivation_triggers: []
  new_campaign_baseline: string
  hidden_state_boundary_review: passed | required | blocked | source_local | quarantined
  continuity_laundering_review: passed | failed | requires_reconciliation | quarantined | escalated
  owner_file_handoffs: []
  notes: string
```

## 9. Donor Structural-Time Mapping Record
```yaml
donor_structural_time_mapping_record:
  record_type: donor_structural_time_mapping
  donor_label: string
  donor_evidence_type: adventure_path | campaign_chapter | scenario_sequence | quest_chain | front | clock | countdown | faction_turn | domain_turn | kingdom_turn | downtime_cycle | travel_calendar | hexcrawl_calendar | season_framework | episode_framework | campaign_phase | level_band | tier_band | realm_ladder | rank_ladder | prestige_cycle | reincarnation_cycle | generational_play | legacy_system | endgame_structure | recurring_villain_procedure | campaign_event_table | random_campaign_event_table | timeline | metaplot | source_local_campaign_script | mixed_structural_time_system
  donor_function_summary: string
  structural_time_function: []
  scale_classification: scene_scale | arc_scale | season_scale | campaign_phase_scale | long_horizon_scale | campaign_calendar_scale | domain_or_institution_scale | generation_scale | metaplot_scale | source_local_scale | mixed_scale | unclear_scale
  lifecycle_effects: []
  mapped_d18_element: continuity_lifecycle | arc_promise | season_throughline | long_horizon_trajectory | transformation_spacing | time_skip_aging_pruning | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  rejected_import_notes: []
  source_local_boundary: string | null
  structural_time_guardrail_flags:
    - payoff_deferral_risk
    - continuity_overload_risk
    - dimensional_collapse_risk
    - long_middle_failure_risk
    - wrong_scale_repair_risk
    - continuity_laundering_risk
    - donor_campaign_law_leakage_risk
  owner_file_handoffs: []
  confidence: high | medium | low | blocked
```

## 10. Runtime Persistence Handoff Note Record
This is not implementation. It is a doctrine-facing handoff control.

```yaml
runtime_persistence_handoff_note_record:
  record_type: runtime_persistence_handoff_note
  handoff_id: string
  state_refs: []
  capture_required: true | false | unknown
  owner_file_storage_required: true | false | unknown
  retrieval_trigger_required: true | false | unknown
  salience_filter_required: true | false | unknown
  hidden_state_boundary_required: true | false | unknown
  context_packet_candidate: true | false | unknown
  over_surface_risk: none | low | medium | high
  under_surface_risk: none | low | medium | high
  not_final_runtime_schema: true
  notes: string
```

## Record posture rules
```text
Every record here is not final schema.
Every record is doctrine-facing and conversion-facing.
D18 records structural-time relevance, not all owner-file detail.
Runtime Gate B or later schema doctrine may replace or formalize these shapes.
Do not implement these directly as save schemas without later schema review.
```
