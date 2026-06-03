# D15-07 — Records, Not-Final-Schema Shapes, and Conversion Handoff Controls

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Scope and warning

The record shapes in this file are **not final schema**. They are doctrine-facing and conversion-facing control shapes.

Runtime Gate B or later Batch C schema doctrine may replace or formalize them. These records do not create backend schemas, database tables, accepted canon, sourcebook prose, or live-play GM authority.

## 2. Organized Actor Operation Context Record

```yaml
organized_actor_operation_context_record:
  record_type: organized_actor_operation_context
  context_id: string
  organized_actor_ref: string
  actor_kind: faction | institution | guild | sect | corporation | polity | order | agency | movement | patron_network | law_authority | domain_authority | player_organization | source_local | mixed
  public_face_known: true | false | partial | unknown
  hidden_agenda_present: true | false | unknown
  capacity_summary: string
  jurisdiction_or_domain_refs: []
  standing_refs: []
  pressure_refs: []
  obligation_claim_refs: []
  source_local_boundary: string | null
  D10_state_owner: true
  D15_procedure_owner: true
  notes: string
```

## 3. Standing Record

```yaml
standing_record:
  record_type: standing
  standing_id: string
  subject_ref: string
  counterpart_ref: string
  standing_axes:
    - trust | respect | hostility | fear | debt | favor | scrutiny | legal_status | access | patronage | obligation | rivalry | alliance | neutrality | reputation | protection | license | source_local
  standing_state: trusted | favored | allied | patronized | neutral | watched | scrutinized | indebted | obligated | rivalrous | hostile | banned | wanted | protected | sponsored | licensed | recognized | source_local | mixed
  public_private_status: public | private | hidden | split | unknown
  subgroup_split_present: true | false | unknown
  temporary: true | false
  owner_file_handoffs: []
  D10_state_owner: true
  notes: string
```

## 4. Pressure Record

```yaml
pressure_record:
  record_type: institutional_pressure
  pressure_id: string
  pressure_family: debt | favor | legal_scrutiny | faction_suspicion | rumor | treaty_strain | sanction | territorial_claim | public_unrest | domain_instability | retaliation | patron_demand | source_local | other
  current_state: latent | active | escalating | decaying | suppressed | transferred | surfaced | converted_to_operation | converted_to_scene | converted_to_project | converted_to_conflict | resolved | retired | source_local
  origin_ref: string | null
  affected_refs: []
  trigger_conditions: []
  decay_conditions: []
  escalation_conditions: []
  owner_file_handoffs: []
  D10_state_owner: true
  notes: string
```

## 5. Obligation / Claim Record

```yaml
obligation_claim_record:
  record_type: obligation_or_claim
  record_id: string
  record_kind: obligation | claim | mixed
  obligation_state: owed | invoked | partially_paid | paid | deferred | contested | transferred | forgiven | defaulted | escalated | retired | source_local | not_applicable
  claim_state: asserted | recognized | contested | rejected | enforced | suspended | transferred | settled | violated | escalated | retired | source_local | not_applicable
  claimant_ref: string
  obligated_or_target_ref: string
  basis: favor | debt | contract | treaty | law | jurisdiction | territory | rank | license | patronage | resource_right | salvage_claim | source_local | other
  economic_component_present: true | false | unknown
  D17_handoff_required: true | false | unknown
  source_local_boundary: string | null
  notes: string
```

## 6. Operation Record

```yaml
operation_record:
  record_type: institutional_operation
  operation_id: string
  operation_profile: relationship_repair_degradation | debt_favor_obligation | access_license_permission | diplomacy_treaty_pact | law_sanction_enforcement | influence_rumor_propaganda | territorial_domain_claim | patronage_sponsorship_recruitment | retaliation_protection_conflict_posture | player_organization_growth | source_local | mixed
  initiator_ref: string
  target_refs: []
  goal_summary: string
  scale: personal | group | local | institutional | territorial | regional | campaign_scale | source_local
  method_summary: string
  leverage_or_authority_refs: []
  cost_risk_commitment_refs: []
  affected_standing_refs: []
  affected_pressure_refs: []
  affected_obligation_claim_refs: []
  affected_domain_posture_refs: []
  setup_outcome: ready_for_scene | ready_for_project | ready_for_operation_interval | ready_with_risk | blocked_pending_requirement | contested_before_start | source_local_retained | quarantined_pending_doctrine_or_evidence | escalated_owner_file_problem
  current_state: proposed | ready | active | contested | blocked | delayed | escalating | decaying | completed | completed_with_cost | partially_successful | failed | settled | retired | quarantined | escalated | source_local
  owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

## 7. Operation Outcome Record

```yaml
operation_outcome_record:
  record_type: operation_outcome
  outcome_id: string
  operation_ref: string
  outcome_state: accepted | accepted_with_cost | partially_accepted | contested | delayed | countered | escalated | deescalated | converted_to_project | converted_to_scene | converted_to_conflict | settled | settled_with_debt | claim_recognized | claim_rejected | claim_contested | standing_improved | standing_damaged | access_opened | access_restricted | obligation_created | obligation_reduced | obligation_transferred | pressure_decayed | pressure_escalated | pressure_surfaced | failed | failed_with_consequence | quarantined | escalated_owner_file_problem | source_local_result
  standing_shift_refs: []
  pressure_movement_refs: []
  obligation_claim_change_refs: []
  access_outcome_refs: []
  domain_posture_change_refs: []
  state_delta_owner: D10
  presentation_owner: D11
  owner_file_handoffs: []
  notes: string
```

## 8. Access Outcome Record

```yaml
access_outcome_record:
  record_type: access_outcome
  access_outcome_id: string
  operation_ref: string
  access_target_ref: string
  access_state: access_granted | access_granted_with_limit | access_denied | access_revoked | license_required | sponsor_required | debt_required | standing_required | restricted_access | black_market_access | temporary_access | source_local_access
  limit_or_condition_summary: string | null
  D17_handoff_required: true | false | unknown
  D10_state_owner: true
  source_local_boundary: string | null
  notes: string
```

## 9. Domain Posture Record

```yaml
domain_posture_record:
  record_type: domain_posture
  domain_posture_id: string
  domain_ref: string
  domain_kind: land | district | route | market | jurisdiction | station | ship | sect_territory | corporate_zone | resource_site | spiritual_domain | trade_lane | source_local | other
  posture_state: controlled | contested | claimed | occupied | restricted | protected | lawless | watched | unstable | hidden_control | shared_jurisdiction | source_local
  controlling_or_claiming_refs: []
  contested_by_refs: []
  D15_domain_control_not_D06_expression: true
  D14_route_or_territory_handoff_required: true | false | unknown
  D17_resource_or_market_handoff_required: true | false | unknown
  D18_long_horizon_handoff_required: true | false | unknown
  notes: string
```

## 10. Institutional Capacity / Operation Load Record

```yaml
institutional_capacity_operation_load_record:
  record_type: institutional_capacity_operation_load
  load_id: string
  organized_actor_ref: string
  operation_ref: string | null
  capacity_sources:
    - personnel | authority | jurisdiction | territory | wealth | resources | infrastructure | information_network | public_legitimacy | legal_status | military_force | specialists | transport | communication | patron_network | source_local_capacity
  capacity_constraints:
    - distance | limited_agents | internal_split | resource_shortage | legal_exposure | public_scrutiny | rival_pressure | domain_instability | poor_information | damaged_infrastructure | ongoing_obligation | campaign_disruption | source_local_limit
  operation_load_sources:
    - large_scale | multiple_targets | territorial_distance | hidden_operation | legal_risk | resource_commitment | public_exposure | military_mobilization | complex_treaty | domain_maintenance | counter_operation_pressure | specialist_need | source_local_burden
  concurrency_supported: true | false | unknown
  unsupported_concurrency_effect: delay | weakened_effect | cost_increase | pressure_exposure | internal_strain | relationship_damage | public_scrutiny | counter_opening | operation_split | operation_failure | quarantine | escalation | none
  notes: string
```

## 11. Donor Institutional Mapping Record

```yaml
donor_institutional_mapping_record:
  record_type: donor_institutional_mapping
  donor_label: string
  donor_function_summary: string
  donor_social_state_changed: []
  donor_scale_assumption: string | null
  donor_timing_assumption: string | null
  donor_track_or_clock_present: true | false
  mapped_d15_element: organized_actor | standing | pressure | obligation_claim | operation | domain_posture | operation_profile | capacity_load | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```

## 12. Record use rules

- These shapes are not final schemas.
- Every record that touches stored social/world state must show D10 as state owner.
- Every economy, market, payment, license, requisition, value, or acquisition implication must identify D17 handoff.
- Every domain posture record must explicitly distinguish D15 domain control from D06 domain expression.
- Every source-local record must define its boundary.
- Donor institutional mapping must include rejected imports and confidence.

## 13. Acceptance criteria

This file is acceptable if it gives conversion and future runtime design auditable control shapes without pretending to finalize schema or backend implementation.
