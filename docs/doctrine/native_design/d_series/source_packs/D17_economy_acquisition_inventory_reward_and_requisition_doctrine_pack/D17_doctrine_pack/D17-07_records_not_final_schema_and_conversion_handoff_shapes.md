# D17-07 — Records, Not-Final Schema, and Conversion Handoff Shapes

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Record scope
The following records are **not final schema**. They are doctrine-facing and conversion-facing control shapes. Runtime Gate B or later schema doctrine may replace or formalize them.

## Value State Record
```yaml
value_state_record:
  record_type: value_state
  value_id: string
  value_form: currency | barter_good | material | component | crafted_good | consumable | fuel | ammunition | supply | relic_fragment | cultivation_resource | biological_sample | data_or_information_asset | service | labor | favor | debt | obligation_value | license | permit | reputation_access | faction_credit | contribution_point | reward_claim | salvage_right | ownership_claim | storage_access | transport_access | market_access | requisition_authority | source_local_currency | source_local_value | mixed
  access_channel_refs: []
  scarcity_state: abundant | common | available | limited | scarce | rare | unique | restricted | illegal | rationed | monopolized | seasonal | unstable | contested | depleted | unknown | hidden | post_scarcity | source_local
  legality_permission_state: legal | licensed | permit_required | restricted | controlled | rationed | black_market_only | contraband | stolen | claimed_by_faction | claimed_by_law | claimed_by_domain_authority | salvage_disputed | use_allowed_sale_forbidden | possession_allowed_transport_forbidden | unknown | source_local
  ownership_custody_ref: string | null
  burden_refs: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

## Access Channel Record
```yaml
access_channel_record:
  record_type: access_channel
  access_channel_id: string
  value_ref: string
  channel_type: purchase | sale | barter | trade | gift | reward | loot | salvage | resource_gathering | crafting_output | requisition | license_grant | faction_store | patron_grant | auction | black_market | market_board | institutional_access | domain_income | quest_payment | bounty | inheritance | loan | debt_settlement | theft | confiscation | tax_collection | tribute | ration_distribution | post_scarcity_access | source_local_channel
  channel_status: available_now | available_with_delay | available_with_requirement | available_at_cost | available_with_risk | available_only_through_project | available_only_through_faction | available_only_through_travel | available_only_through_black_market | available_only_through_source_local_procedure | unavailable | unknown | protected_hidden | quarantined | escalated
  required_permissions: []
  required_costs_or_sinks: []
  required_owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

## Acquisition / Exchange Record
```yaml
acquisition_exchange_record:
  record_type: acquisition_exchange
  transaction_id: string
  initiating_actor_or_group_ref: string
  value_refs: []
  access_channel_ref: string
  acquisition_intent: obtain | sell | trade | barter | request | requisition | borrow | lease | convert | claim | store | move | fabricate | source_local
  availability_outcome: available_now | available_with_delay | available_with_requirement | available_at_cost | available_with_risk | available_only_through_project | available_only_through_faction | available_only_through_travel | available_only_through_black_market | available_only_through_source_local_procedure | unavailable | unknown | protected_hidden | quarantined | escalated
  permission_custody_review_required: true | false | unknown
  exchange_conversion_friction: [transaction_cost, tax, tariff, delay, spoilage, loss_rate, exchange_rate, standing_requirement, broker_requirement, black_market_risk, requisition_approval, material_waste, custody_dispute, source_local_rule]
  outcome_state: acquired | acquired_with_cost | acquired_with_burden | acquired_with_dispute | acquired_with_trace | access_granted | access_limited | access_denied | exchange_completed | exchange_partial | exchange_delayed | exchange_failed | custody_changed | ownership_changed | claim_created | claim_contested | requisition_approved | requisition_denied | reward_delivered | loot_pending_review | salvage_pending_claim | black_market_trace_created | unavailable | quarantined | escalated | source_local_result
  owner_file_handoffs: []
  notes: string
```

## Value Entry Record
```yaml
value_entry_record:
  record_type: value_entry
  value_entry_id: string
  trigger_source: D13_project_completion | D14_discovery | D15_operation | D16_encounter_or_opposition | quest_completion | bounty_completion | loot_from_opposition | salvage_from_site | salvage_from_vehicle_platform | faction_grant | patron_payment | auction_result | inheritance | domain_income | resource_gathering | crafting_output | D18_milestone_handoff | source_local_reward
  source_authority: direct_possession | contract | bounty_issuer | quest_giver | faction_authority | law_authority | domain_authority | salvage_law | market_agreement | patron_promise | source_local_system | world_state_discovery | encounter_context | project_output | campaign_milestone | unknown_authority
  value_entry_category: reward_payment | reward_item | reward_access | reward_license | reward_claim | reward_favor | reward_information_asset | loot_currency | loot_item | loot_material | loot_component | loot_consumable | loot_relic_fragment | loot_source_local | salvage_component | salvage_material | salvage_data | salvage_platform_part | salvage_biological_sample | salvage_resource | bounty_payment | faction_grant | requisition_grant | domain_income | project_output | crafting_output | source_local_reward
  eligibility_state: eligible | eligible_with_condition | shared_eligibility | contested_eligibility | ineligible | unknown | protected_hidden | source_local
  custody_ownership_outcome_ref: string | null
  burden_sink_consequence_refs: []
  delivery_outcome: delivered | delivered_with_burden | delivered_with_cost | delivered_with_trace | delivered_with_claim | delivered_as_custody_only | delivered_as_access_only | delivered_as_source_local | split_required | escrow_required | claim_review_required | salvage_pending | reward_delayed | reward_denied | reward_partially_delivered | reward_converted | reward_quarantined | escalated_owner_file_problem
  owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

## Ownership / Custody Record
```yaml
ownership_custody_record:
  record_type: ownership_custody
  ownership_custody_id: string
  value_ref: string
  ownership_state: owned | borrowed | leased | licensed | loaned | rented | faction_held | escrowed | impounded | requisitioned | claimed | contested | stolen | salvage_pending | salvage_awarded | bound | soul_bound_source_local | lost | abandoned | unclaimed | unknown | source_local
  custody_state: possessed | held_in_custody | carried | stored | hidden | vehicle_stored | platform_stored | facility_stored | banked | vaulted | cached | escrowed | faction_held | impounded | requisition_held | lost | unknown | source_local
  owner_ref: string | null
  custodian_ref: string | null
  claimant_refs: []
  transfer_allowed: true | false | unknown | source_local
  sale_allowed: true | false | unknown | source_local
  use_allowed: true | false | unknown | source_local
  transport_allowed: true | false | unknown | source_local
  D10_state_owner: true
  D15_claim_or_enforcement_handoff_required: true | false | unknown
  notes: string
```

## Inventory / Burden Record
```yaml
inventory_burden_record:
  record_type: inventory_burden
  burden_id: string
  value_ref: string
  holding_mode: carried_on_person | equipped | worn | quick_access | packed | container_stored | vehicle_stored | platform_stored | facility_stored | banked | vaulted | cached | hidden | escrowed | faction_held | requisition_held | impounded | leased_storage | digital_or_pattern_stored | bound_to_actor | source_local_holding | unknown
  burden_types: [weight, bulk, volume, slot, quick_access_limit, container_capacity, transport_capacity, storage_capacity, security_burden, concealment_burden, legal_visibility, social_visibility, faction_trace, custody_risk, maintenance_burden, decay_or_spoilage, fuel_or_power_support, crew_or_labor_support, platform_cargo_burden, access_delay, retrieval_risk, source_local_burden]
  access_state: immediate_access | quick_access | scene_access | interval_access | safe_location_access | facility_access | vehicle_or_platform_access | faction_permission_access | licensed_access | locked_access | hidden_cache_access | delayed_access | blocked_access | source_local_access | unknown_access
  stability_state: stable | fragile | perishable | decaying | spoiling | unstable | contaminated | degrading | maintenance_required | expired | source_local_decay
  possession_scope: individual | party_shared | crew_shared | faction_shared | vehicle_or_platform | facility | domain | escrow | source_local_scope
  loss_risk_present: true | false | unknown
  owner_file_handoffs: []
  notes: string
```

## Loss / Confiscation / Recovery Record
```yaml
loss_confiscation_recovery_record:
  record_type: loss_confiscation_recovery
  loss_event_id: string
  value_ref: string
  trigger: overburden | flight | defeat | confiscation | tax_seizure | faction_claim | legal_inspection | theft | container_damage | platform_destruction | hazard_exposure | decay | spoilage | abandonment | failed_transport | source_local_trigger
  outcome: lost | damaged | impounded | stolen | abandoned | claimed_by_other | converted_to_unresolved_pressure | recoverable | recoverable_with_cost | recoverable_with_project | recoverable_with_operation | destroyed | quarantined | source_local_result
  lawful_trigger_confirmed: true | false | unknown
  owner_file_handoffs: []
  recovery_path_available: true | false | unknown
  notes: string
```

## Sink / Requisition / Upkeep Record
```yaml
sink_requisition_upkeep_record:
  record_type: sink_requisition_upkeep
  sink_id: string
  value_ref: string
  sink_type: consumption | upkeep | maintenance | repair_cost | fuel_use | ammo_use | component_use | license_fee | permit_renewal | tax | tariff | toll | dues | tribute | tithe | rent | storage_fee | broker_fee | auction_fee | transaction_fee | bribe | debt_payment | interest | faction_contribution | requisition_reservation | rationing | decay | spoilage | degradation | confiscation | seizure | sacrifice | cultivation_consumption | ritual_consumption | source_local_sink
  sink_timing: immediate | on_acquisition | on_exchange | on_use | on_damage | on_repair | on_storage | on_transport | on_maintenance_interval | on_license_interval | on_project_interval | on_scene_transition | on_travel_interval | on_faction_operation | on_campaign_interval | on_failure | on_success | on_overuse | ambient | scheduled | source_local_timing
  obligation_level: mandatory | required_for_access | required_for_legality | required_for_safety | required_for_maintenance | required_for_quality | optional_upgrade | optional_convenience | avoidable_with_risk | deferable_with_consequence | waived_by_standing | waived_by_license | source_local_obligation
  sink_effect: removed_from_circulation | consumed | reserved | locked | degraded | spoiled | transformed | converted_to_debt | converted_to_obligation | converted_to_trace | transferred_to_faction | transferred_to_law_authority | transferred_to_market_actor | sacrificed | destroyed | held_in_escrow | source_local_effect
  anti_poverty_trap_review_required: true | false | unknown
  owner_file_handoffs: []
  notes: string
```

## Debt / Obligation Value Record
```yaml
debt_obligation_value_record:
  record_type: debt_obligation_value
  debt_value_id: string
  debtor_ref: string
  creditor_ref: string
  debt_form: currency_debt | favor_debt | resource_debt | service_debt | requisition_debt | salvage_debt | patron_debt | faction_debt | legal_debt | source_local_debt
  debt_state: owed | current | deferred | partially_paid | defaulted | renegotiated | transferred | forgiven | converted_to_obligation | converted_to_pressure | source_local_debt_state
  value_side_owner: D17
  obligation_enforcement_owner: D15
  world_state_owner: D10
  payment_or_settlement_refs: []
  recovery_or_default_path: string | null
  notes: string
```

## Donor Value Mapping Record
```yaml
donor_value_mapping_record:
  record_type: donor_value_mapping
  donor_label: string
  donor_evidence_type: price_list | shop_inventory | loot_table | reward_table | treasure_parcel | currency | wealth_rating | inventory_rule | encumbrance_rule | requisition_list | contribution_chart | resource_grade | salvage_table | repair_durability_rule | fuel_ammo_rule | tax_upkeep_rule | debt_rule | post_scarcity_rule | market_rule | black_market_rule | license_rule | mixed
  donor_function_summary: string
  mapped_value_form: string | null
  mapped_access_channel: string | null
  mapped_d17_element: value_state | access_channel | acquisition_exchange | value_entry | ownership_custody | inventory_burden | sink_requisition_upkeep | debt_obligation_value | source_local | quarantine | escalation
  donor_price_or_currency_assumption_present: true | false | unknown
  donor_inventory_or_burden_assumption_present: true | false | unknown
  donor_reward_or_loot_assumption_present: true | false | unknown
  donor_requisition_or_sink_assumption_present: true | false | unknown
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  research_guardrail_flags: [inflation_risk, poverty_trap_risk, hoarding_risk, reward_collapse_risk, inventory_paralysis_risk, grind_wall_risk, uncontrolled_salvage_risk, post_scarcity_erasure_risk, donor_value_law_leakage_risk]
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```
