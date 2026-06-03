# D16-07 — Records, Not-Final Schema, and Conversion Handoff Shapes

Status: `doctrine-pack`
Version: `v0.1`
Layer: D16 / operational procedure doctrine
Primary scope: Opposition, creature, encounter, and hazard construction
Authority posture: Doctrine-facing and conversion-facing. Not final runtime schema, not final statblock schema, not encounter-balance math.

D16 is part of the D12–D18 operational procedure layer. It assumes D00–D15 are active doctrine dependencies and must preserve their owner boundaries.


## Purpose

D16 records are lightweight, doctrine-facing and conversion-facing control shapes. They are **not final schema**. Runtime Gate B or later schema doctrine may replace or formalize them.

## Record posture

These shapes exist to keep opposition construction auditable. They must not be treated as runtime database tables, final statblocks, final creature schemas, final hazard schemas, final encounter budgets, or final combat math.

## Opposition Profile Record

```yaml
opposition_profile_record:
  record_type: opposition_profile
  opposition_id: string
  source_kind: creature | npc | rival | social_antagonist | hazard | environmental_threat | security_system | object_system | vehicle | ship | mech | platform | swarm | horde | elite | boss | summon | companion_under_opposition_role | institutional_proxy | legal_pressure | territorial_pressure | source_local | mixed
  threat_functions: []
  opposition_scale: individual | pair_or_small_group | group | swarm | horde | elite | boss | environmental | site | object_system | platform | vehicle_ship_mech | institutional_proxy | territorial | regional | source_local | mixed
  threat_roles: []
  objective_summary: string | null
  threat_posture: string
  pressure_profile_refs: []
  capability_pressure_refs: []
  constraint_vulnerability_refs: []
  threat_weight_ref: string | null
  readiness_state: ready_for_scene_use | ready_with_owner_file_handoffs | source_local_ready | requires_schema_support | requires_harm_support | requires_actor_support | requires_object_or_platform_support | requires_world_state_support | requires_economy_or_reward_support | quarantined_pending_doctrine_or_evidence | escalated_owner_file_problem
  owner_file_handoffs: []
  source_local_boundary: string | null
  rejected_donor_assumption_refs: []
  notes: string
```

## Opposition Pressure Profile Record

```yaml
opposition_pressure_profile_record:
  record_type: opposition_pressure_profile
  pressure_profile_id: string
  opposition_ref: string
  primary_pressure: harm_pressure | control_pressure | mobility_pressure | area_denial | resource_pressure | time_pressure | social_pressure | legal_pressure | fear_or_dread_pressure | corruption_pressure | condition_pressure | exposure_pressure | terrain_pressure | information_pressure | object_pressure | platform_pressure | domain_pressure | summon_pressure | reinforcement_pressure | source_local_pressure
  secondary_pressures: []
  affected_state_targets: []
  owner_file_handoffs: []
  final_effect_defined_by_owner_files: true
  notes: string
```

## Capability Pressure Record

```yaml
capability_pressure_record:
  record_type: capability_pressure
  capability_id: string
  opposition_ref: string
  capability_family: direct_harm_capability | area_control_capability | mobility_capability | defense_or_survival_capability | support_capability | summon_or_reinforcement_capability | social_leverage_capability | legal_or_institutional_capability | information_capability | stealth_or_ambush_capability | resource_drain_capability | corruption_or_instability_capability | object_disruption_capability | platform_system_capability | terrain_or_environment_capability | domain_or_power_pressure_capability | source_local_capability
  capability_summary: string
  not_a_final_ability_list: true
  owner_file_handoffs: []
  unsupported_mechanics_quarantined: true | false
  notes: string
```

## Constraint / Vulnerability / Resistance Routing Record

```yaml
constraint_vulnerability_resistance_routing_record:
  record_type: constraint_vulnerability_resistance_routing
  routing_id: string
  opposition_ref: string
  interaction_kind: constraint | vulnerability | resistance | immunity_pressure | protection | threshold | bypass_condition | morale_limit | access_condition | source_local_interaction
  interaction_summary: string
  exact_mechanics_owner: D06 | D07 | D08 | D09 | D10 | D11 | source_local | unknown
  donor_math_preserved_as_evidence_only: true | false
  mechanical_finality_claimed: false
  quarantine_or_escalation_required: true | false
  notes: string
```

## Threat Weight Review Record

```yaml
threat_weight_review_record:
  record_type: threat_weight_review
  threat_weight_id: string
  opposition_or_encounter_ref: string
  threat_weight: incidental | minor | standard | major | severe | dominant | apex_source_local
  review_basis:
    - actor_capability
    - number_of_opposition_elements
    - primary_pressure
    - secondary_pressures
    - location_tier
    - environmental_pcr
    - domain_alignment
    - resource_state
    - surprise_or_preparedness
    - route_or_site_constraints
    - objective_difficulty
    - hidden_information
    - support_or_reinforcement
    - resistance_or_vulnerability_pressure
    - platform_or_object_support
    - institutional_backing
    - source_local_context
  not_cr_level_or_budget: true
  owner_file_handoffs: []
  notes: string
```

## Encounter Composition Record

```yaml
encounter_composition_record:
  record_type: encounter_composition
  encounter_id: string
  encounter_purpose: block_route | guard_resource | test_intruders | create_cost | force_choice | delay_party | reveal_pressure | escalate_faction_response | threaten_harm | threaten_exposure | create_negotiation | trigger_pursuit | consume_time | protect_secret | contest_claim | deny_access | defend_site | collapse_environment | advance_source_local_script | source_local_purpose | mixed
  primary_pressure_ref: string
  secondary_pressure_refs: []
  opposition_profile_refs: []
  context_pressure_refs: []
  objective_structure: single_objective | competing_objectives | layered_objectives | escape_objective | defense_objective | negotiation_objective | exposure_objective | resource_objective | source_local_objective | mixed
  primary_cadence_profile: martial_conflict | social_conflict | stealth_infiltration | chase_pursuit | ritual_power_contest | technical_system_standoff | exploration_hazard | platform_crew | mixed | source_local
  state_delta_targets: []
  readiness_state: string
  owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

## Behavior / Morale / Posture Record

```yaml
behavior_morale_posture_record:
  record_type: behavior_morale_posture
  behavior_id: string
  opposition_ref: string
  current_behavior_state: unaware | watching | probing | warning | negotiating | holding_position | pressing_attack | seeking_capture | protecting_target | calling_support | retreating | routing | surrendering | hiding | regrouping | escalating | deescalating | controlled | frenzied | bound_by_command | source_local
  morale_as_persistence_pressure: irrelevant | fragile | ordinary | disciplined | fanatical | programmed | bound | desperate | territorial | professional | source_local
  posture_change_triggers: []
  universal_morale_score_used: false
  owner_file_handoffs: []
  notes: string
```

## Recurrence / Continuity Record

```yaml
recurrence_continuity_record:
  record_type: recurrence_continuity
  recurrence_id: string
  opposition_ref: string
  recurrence_kind: rival | faction_agent | hunt_threat | boss_survivor | legal_adversary | social_antagonist | territorial_guardian | institutional_proxy | platform_threat | persistent_hazard | source_local_recurring_threat | other
  continuity_support:
    - escape_route
    - survival_condition
    - institutional_replacement
    - source_local_return_condition
    - unresolved_pressure
    - offscreen_continuity_support
    - hazard_persistence
    - platform_repair_or_rebuild_path
    - D18_campaign_arc_handoff
  D10_state_record_required: true
  D15_handoff_required: true | false | unknown
  D18_handoff_required: true | false | unknown
  recurrence_by_fiat_allowed: false
  notes: string
```

## Donor Opposition Mapping Record

```yaml
donor_opposition_mapping_record:
  record_type: donor_opposition_mapping
  donor_label: string
  donor_evidence_type: statblock | hazard | trap | npc | encounter | table | vehicle | ship | mech | platform | boss | social_antagonist | security_system | mixed
  donor_function_summary: string
  donor_stat_fields_present: []
  donor_action_economy_present: true | false | unknown
  donor_budget_or_rating_present: true | false | unknown
  donor_resistance_or_vulnerability_present: true | false | unknown
  donor_reward_or_loot_link_present: true | false | unknown
  mapped_d16_element: opposition_profile | pressure_profile | capability_pressure | encounter_composition | behavior_morale | recurrence_continuity | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```
