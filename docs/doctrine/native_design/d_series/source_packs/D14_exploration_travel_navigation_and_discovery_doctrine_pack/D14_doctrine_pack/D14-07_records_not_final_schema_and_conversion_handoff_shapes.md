# D14-07 — Records, Not-Final-Schema, and Conversion Handoff Shapes

Status: doctrine-draft / Phase 1 native doctrine continuation  
Version: `0.1.0-d14-generated`  
Generated: 2026-06-02  
Layer: D14 operational procedure doctrine  
Owner: Astra doctrine architecture / exploration and discovery procedure layer

## Purpose

This file defines lightweight doctrine-facing and conversion-facing record shapes for D14. These records are **not final schema**. Runtime Gate B, Batch C location/map schema doctrine, or later sourcebook consolidation may replace or formalize them.

## Travel / Exploration Procedure Record

```yaml
travel_exploration_procedure_record:
  record_type: travel_exploration_procedure
  procedure_id: string
  intent_summary: string
  procedure_kind: route_travel | area_exploration | site_approach | site_entry | scouting | mapping | pursuit_evasion | resource_search | platform_navigation | realm_crossing | source_local | mixed
  primary_actor_or_group_ref: string
  primary_context_profile: urban_social_dense | wilderness_open_region | site_dungeon_interior | space_vehicle_platform | dimensional_realm_threshold | hazardous_anomalous_zone | pursuit_evasion | mixed | source_local
  secondary_context_profiles: []
  declared_posture_refs: []
  route_or_area_refs: []
  known_state_review_ref: string | null
  active_interval_refs: []
  discovery_refs: []
  pressure_refs: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  current_status: active | completed | transitioned | blocked | quarantined | escalated | archived
```

## Travel Posture Record

```yaml
travel_posture_record:
  posture_family: speed | safety | stealth | scouting | mapping | tracking | foraging_resource_search | concealment | diplomatic_approach | survey_analysis | ritual_sensing | sensor_sweep | platform_caution | resource_conservation | pursuit | evasion | combat_readiness | social_blending | source_local | mixed
  declared_priority: string
  likely_benefits: []
  likely_exposures: []
  likely_blind_spots: []
  owner_file_handoffs: []
  not_a_generic_bonus: true
```

## Route / Area Record

```yaml
route_area_record:
  route_or_area_kind: route | area | vector | corridor | trail | district_sequence | jump_line | realm_crossing | platform_section | site_region | source_local | unknown
  player_facing_description: string
  route_states: [known | partially_known | suspected | rumored | hidden | false | blocked | dangerous | contested | watched | restricted | unstable | source_local | unmapped]
  map_state_refs: []
  actual_truth_owner: D10
  geometry_required: true | false | unknown
  source_local_boundary: string | null
```

## Known-State Review Record

```yaml
known_state_review_record:
  known_state_entries:
    - subject_ref: string
      party_facing_status: confirmed_known | party_believes | rumored | suspected | mapped_but_unverified | false_or_compromised | hidden_from_party | protected_hidden | source_local
      actual_truth_owner: D10
      presentation_owner: D11
      visible_to_player: true | false | partial
  hidden_pressure_present: true | false | unknown
  protected_hidden_not_revealed: true
```

## Travel / Exploration Interval Record

```yaml
travel_exploration_interval_record:
  interval_scale: momentary_approach | scene_segment | site_segment | district_leg | wilderness_leg | travel_watch | day_journey | ship_platform_vector | realm_crossing_stage | survey_pass | source_local_interval | other
  active_posture_refs: []
  active_route_area_ref: string
  navigation_check_required: true | false
  navigation_check_reason: uncertain | contested | hidden | distorted | false | risky | pursuit | none
  environmental_pcr_ref: string | null
  resource_exposure_check_required: true | false
  discovery_hazard_encounter_check_required: true | false
  progress_outcome: advanced | advanced_with_cost | advanced_with_discovery | advanced_with_exposure | delayed | misdirected | lost | blocked | hazard_triggered | encounter_triggered | site_entry_triggered | map_state_updated | pressure_escalated | transitioned | quarantined | escalated | pending
  owner_file_handoffs: []
```

## Environmental PCR Travel Record

```yaml
environmental_pcr_travel_record:
  location_tier: string
  visible_location_tags: []
  domain_alignment_visible: []
  opposition_modifier_visible: string | unknown
  hidden_cosmic_modifier_status: protected
  environmental_pressure_visible: []
  environmental_pressure_hidden_present: true | false | unknown
  affects_navigation: true | false | unknown
  affects_discovery: true | false | unknown
  affects_resource_or_exposure: true | false | unknown
  D02_resolution_owner: true
  D10_truth_owner: true
  D11_presentation_owner: true
```

## Discovery Opportunity Record

```yaml
discovery_opportunity_record:
  discovery_source: posture | navigation | scouting | mapping | tracking | survey_analysis | ritual_sensing | sensor_sweep | social_blending | resource_search | environmental_pcr | site_approach | D10_unresolved_pressure | source_local_procedure | scenario_design | failed_or_partial_result | hazard_proximity | faction_movement | object_platform_sensor | other
  discovery_category: route_discovery | location_discovery | site_entry_discovery | hazard_discovery | resource_discovery | clue_or_lead_discovery | faction_presence_discovery | opposition_trace_discovery | environmental_condition_discovery | object_or_salvage_discovery | map_correction | false_route_exposure | hidden_boundary_hint | source_local_discovery
  confidence_state: confirmed | high_confidence | partial | ambiguous | rumored | suspected | false_or_compromised | protected_hidden | source_local
  actual_truth_owner: D10
  presentation_owner: D11
  hidden_truth_revealed: false
```

## Map-State Update Record

```yaml
map_state_update_record:
  previous_map_state: known | surveyed | partially_mapped | suspected | rumored | false | compromised | hidden | blocked | unreachable | source_local | unknown
  new_map_state: known | surveyed | partially_mapped | suspected | rumored | false | compromised | hidden | blocked | unreachable | source_local
  update_direction: improved | degraded | contradicted | complicated | confirmed | invalidated
  actual_truth_owner: D10
  presentation_owner: D11
  geometry_required: true | false | unknown
  source_local_boundary: string | null
```

## Exploration Pressure Record

```yaml
exploration_pressure_record:
  pressure_family: resource_pressure | exposure_pressure | hazard_pressure | encounter_pressure | navigation_pressure | map_state_pressure | ambush_exposure | social_or_legal_pressure | faction_or_territory_pressure | object_or_platform_pressure | hidden_state_pressure | time_pressure | source_local_pressure
  trigger_source: posture | route_state | environmental_pcr | known_hazard | owner_supported_hidden_pressure | D10_unresolved_pressure | opposition_movement | resource_scarcity | site_design | source_local_procedure | prior_state_delta | failed_or_partial_result | acceleration_unsafe_method | owner_file_clock | other
  severity: low | medium | high | blocking
  owner_file_handoffs: []
  immediate_transition_required: true | false
  hidden_state_protected: true | false
```

## Site Entry Record

```yaml
site_entry_record:
  entry_kind: known_entry | discovered_entry | forced_entry | hidden_entry | restricted_entry | unstable_entry | source_local_entry
  entry_posture_refs: []
  known_state_review_ref: string | null
  map_state_update_refs: []
  hazard_scan_required: true | false
  ambush_exposure_ref: string | null
  D12_transition_ref: string | null
  D10_pressure_refs: []
  source_local_boundary: string | null
```

## Watch / Ambush Exposure Record

```yaml
watch_ambush_exposure_record:
  record_kind: watch_assignment | ambush_exposure | both
  watch_type: guard_watch | scout_watch | sensor_watch | ritual_watch | social_watch | rear_watch | platform_systems_watch | faction_surveillance_watch | source_local_watch | none
  assigned_actor_refs: []
  exposure_sources: []
  ambush_exposure_state: none | possible | elevated | active | hidden | source_local
  automatic_surprise_granted: false
  sequencing_owner: D12
  resolution_owner: D02
```

## Donor Exploration Mapping Record

```yaml
donor_exploration_mapping_record:
  donor_label: string
  donor_function_summary: string
  donor_spatial_assumption: string | null
  donor_timing_assumption: string | null
  state_changed_or_revealed: []
  mapped_d14_element: posture | route_area | interval | discovery | map_state | pressure | site_entry | watch | context_profile | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```

## Record-use rules

Records are audit aids, not runtime authority. They may mark hidden pressure as present or unknown but must not reveal protected truth. Every donor mapping record uses exactly one lawful outcome. Source-local records require boundaries. Blocking confidence routes to quarantine or escalation.
