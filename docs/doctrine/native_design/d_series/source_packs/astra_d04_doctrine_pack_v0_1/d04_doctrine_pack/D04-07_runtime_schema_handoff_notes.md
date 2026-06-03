# D04-07 — Runtime and Schema Handoff Notes

Status: `doctrine-draft / accepted D04 design decisions`  
Layer: D04 runtime/schema handoff  
Owner: advancement architecture / runtime handoff boundary  
Depends on: D04-00 through D04-06  
Feeds: runtime progression schema, UI advancement screen, Batch C schemas, D03/D05-D10 doctrine

## 1. Purpose

This file defines what D04 needs runtime and schema layers to track later. It does not implement runtime.

D04 can identify required fields, state deltas, validation gates, and UI surfaces. Runtime owns authoritative state, dice, validation, events, and commits.

## 2. Runtime boundary

D04 must not mutate state by narration. Any advancement outcome must eventually become a validated state delta and committed event.

The model may propose, explain, narrate, and summarize advancement. Backend/runtime must validate and commit advancement state.

## 3. Core actor progression fields

```yaml
actor_progression_state:
  actor_id: string
  level: integer
  tier: integer
  tier_status: mortal | ascendant | capstone | post_capstone | source_local
  unspent_development_picks: [development_pick_id]
  held_pick_pressure: none | low | moderate | high | capstone
  proof_ledger_refs: [proof_event_id]
  proof_bundle_refs: [proof_bundle_id]
  active_axes: [advancement_axis_id]
  hidden_axes: [advancement_axis_id]
  route_ledger_refs: [route_id]
  awakening_status: none | pending | eligible | delayed | accepted | forced | coerced | corrupted | resolved | source_local
  breakthrough_states: [breakthrough_state_id]
  capstone_status: none | threshold_entry | axis_consolidation | contradiction_cost | recognition_proof | final_integration | final_resolution | resolved
  ascension_access_status: none | eligible | delayed | suppressed | refused | attempted | partial | failed | worldbound | externalized | source_local
```

## 4. Proof ledger fields

```yaml
proof_ledger:
  proof_events: [proof_event]
  proof_handling_records: [proof_handling]
  proof_bundles: [proof_bundle]
  proof_cluster_index:
    - cluster_id: string
      actor_ref: string
      cluster_theme: string
      proof_refs: [string]
      sufficiency_estimate: trace | seed | credible | established | weighty | defining | mythic | capstone
      route_candidates: [string]
      axis_candidates: [string]
      contradiction_refs: [string]
  proof_binding_records:
    - binding_id: string
      proof_refs: [string]
      bound_to: title | route | axis | breakthrough | expression | economy | external_anchor | capstone | source_local
      binding_status: referenced | bound | transformed | corrupted | rejected | spent
```

## 5. Development Pick fields

```yaml
development_pick:
  pick_id: string
  actor_ref: string
  pick_type: axis | skill_profession | expression | capacity | route | repair | project | proof | breakthrough_prep | bond_companion | item_relic | world_faction | drift_fusion | capstone | source_local
  pick_shape: open_typed | proof_shaped | axis_shaped | route_shaped | recovery_shaped | tier_shaped | capstone_shaped | source_local
  pick_band: mortal | ascendant | advanced | apex | mythic | capstone
  grant_source: level | tier | proof | title | achievement | breakthrough | source_local | capstone
  granted_at_level: integer | null
  granted_at_tier: integer | null
  proof_basis: [string]
  hold_state: fresh | held | focused | stale | pressurized | converted | expired
  target_ref: string | null
  owner_file: string | null
  validation_status: unspent | authorized | pending | dangerous | source_local | spent | blocked
```

## 6. Tier transition fields

```yaml
tier_transition:
  transition_id: string
  actor_ref: string
  from_tier: integer
  to_tier: integer
  proof_bundle_ref: string
  transition_status: pending | authorized | delayed | dangerous | blocked | resolved
  scale_authorization_applied: boolean
  direct_tier_benefit_ref: string | null
  visibility_change_ref: string | null
  future_unlock_notice_refs: [string]
  pending_benefit_state: none | pending_proof | pending_owner_file | pending_route | pending_structure | pending_choice | pending_project | deferred
```

## 7. Awakening fields

```yaml
awakening_record:
  awakening_id: string
  actor_ref: string
  threshold_level: integer
  proof_bundle_ref: string
  catalyst_refs: [string]
  route_refs: [string]
  anchor_refs: [string]
  triadic_options:
    - option_id: string
      route_name: string
      presentation_role: string
      proof_cluster_refs: [string]
      risk_notes: [string]
      access_vector_candidates: [string]
  selected_option_ref: string | null
  selected_route_state: stable | unstable | scarred | coerced | forced | corrupted | externalized | source_local | dormant_secondary
  initial_access_vector: string
  initial_carrier_state: string
  starter_method_ref: string | null
  awakening_pick_ref: string | null
  unselected_option_ledger_refs: [string]
  visibility_change_ref: string | null
  constraints: [string]
  safety_scope_limits: [string]
  status: pending | delayed | accepted | resolved | source_local | blocked
```

## 8. Breakthrough fields

```yaml
breakthrough_state:
  breakthrough_id: string
  actor_ref: string
  vector_type: attribute | economy | expression | carrier | route | skill | profession | item | bond | territory | corruption | whole_character | capstone | source_local
  vector_ref: string
  threshold_state: stable | pressured | eligible | delayed | focused | overripe | blocked | unstable | corrupted | coerced | forced | contested | lethal_risk | resolved | shattered
  proof_bundle_ref: string | null
  risk_posture: safe | strained | unstable | dangerous | catastrophic
  warning_required: boolean
  warning_presented: boolean
  player_response: proceed | delay | stabilize | redirect | seek_anchor | accept_scar | externalize | resist | sever | purify | quarantine | bargain | bind | split | fuse | sacrifice | convert | revert | integrate | push | none
  resolution_mode: formal | choice_gated | project_clock | d20_threshold_test | contested | coerced | dangerous_push | source_local
  d02_result_ref: string | null
  payload_refs: [string]
  state_delta_refs: [string]
  status: pending | resolved | failed | shattered | source_local
```

## 9. Breakthrough payload fields

```yaml
breakthrough_payload:
  payload_id: string
  breakthrough_ref: string
  payload_categories:
    - capacity
    - access
    - expression
    - route
    - attribute
    - economy
    - carrier_slot
    - resistance_recovery
    - title_achievement
    - bond_anchor
    - world_state
    - scar_cost
    - corruption_purification
    - actor_state
    - capstone
  quality_band: null | residual | reduced | partial | fragile | scarred | clean | reinforced | enhanced | rare | defining | mythic | capstone
  benefit_summary: string
  cost_summary: string | null
  consequence_summary: string | null
  owner_file_handoffs: [string]
  validation_status: authorized | pending_owner | dangerous | source_local | blocked
```

## 10. Advancement axis fields

```yaml
advancement_axis:
  axis_id: string
  actor_ref: string
  axis_family: string
  axis_name: string
  axis_status: hidden | seed | visible | active | capped | blocked | source_local | retired | transformed
  owner_file: D04 | D05 | D06 | D07 | D08 | D09 | D10 | source_local
  proof_refs: [string]
  current_band: trace | seed | credible | established | weighty | defining | mythic | capstone | owner_defined
  tier_authorization_required: integer | null
  cap_state: below_cap | at_cap | cap_raise_available | cap_blocked
  access_requirements: [string]
  development_pick_types_allowed: [string]
  linked_routes: [string]
  linked_expressions: [string]
  linked_power_economies: [string]
  linked_anchors: [string]
  source_local_boundary: string | null
```

## 11. Capstone fields

```yaml
capstone_record:
  capstone_id: string
  actor_ref: string
  current_capstone_level: 95 | 96 | 97 | 98 | 99 | 100 | null
  capstone_function: threshold_entry | axis_consolidation | contradiction_cost | recognition_proof | final_integration | final_resolution | resolved
  capstone_proof_bundle_refs: [string]
  capstone_pick_refs: [string]
  capstone_axes: [string]
  contradiction_refs: [string]
  cost_confrontation_refs: [string]
  recognition_refs: [string]
  irreversible_choice_refs: [string]
  final_payload_refs: [string]
  failure_posture: none | dangerous | catastrophic | lethal_risk
  status: none | pending | active | delayed | resolved | failed | transformed | source_local
```

## 12. Ascension Access fields

```yaml
ascension_access:
  ascension_access_id: string
  actor_ref: string
  level_100_ref: string
  capstone_resolution_ref: string
  access_status: none | eligible | delayed | suppressed | refused | attempted | full | partial | failed | worldbound | externalized | corrupted | purified | loose_incomplete | source_local
  posture: attempt | delay | suppress | refuse | externalize | redirect | worldbind | source_local | undecided
  proof_requirements_met: boolean
  unresolved_consequences: [string]
  owner_file_handoffs: [D03, D06, D07, D08, D09, D10]
  notes: string
```

## 13. Required state delta types

D04-related state deltas may include level gained, tier transition authorized/resolved, Development Pick granted/held/spent/converted/pressurized, proof event recorded, proof handling recorded, proof bundle authorized, proof bound/transformed/corrupted/rejected/spent, axis revealed/advanced/capped/transformed, Awakening options generated, Awakening option selected, route initialized, unselected route ledger updated, starter method granted, carrier initialized, breakthrough threshold updated/resolved, payload applied, scar/cost/debt/constraint recorded, capstone level function entered, capstone pick granted/spent, capstone final resolution, Ascension Access gained, and Ascension posture selected.

## 14. UI surfaces

D04 implies these eventual UI screens or panels:

1. Advancement Overview
2. Proof Ledger
3. Legal Option Presentation
4. Development Pick Menu
5. Axis Registry
6. Awakening Screen
7. Tier Transition Screen
8. Breakthrough Screen
9. Capstone Screen
10. Ascension Access Screen

UI may simplify labels, but backend records must preserve doctrine distinctions.

## 15. Legal Option Presentation UI

When a Development Pick or tier benefit is available, UI should show valid options, why each option is valid, proof supporting it, owner file/system, state delta produced, unavailable examples if useful, and what is missing for unavailable/pending options.

| UI category | Backend sources |
|---|---|
| Improve | Axis, Skill, Profession, Capacity |
| Refine | Expression, Mastery, Item, Route |
| Stabilize | Repair, Recovery, Route, Carrier |
| Expand | Scope, Economy, Carrier, Axis Cap |
| Prepare | Breakthrough Prep, Project, Awakening, Capstone |
| Formalize | Proof, Title, Achievement, Recognition |
| Redirect | Drift, Fusion, Conversion, Reversion |

## 16. Downstream owner handoffs

D02 owns d20 roll, advantage/disadvantage/modifiers, outcome lanes, critical success/failure, and resolution procedure. D04 maps D02 outcomes into breakthrough outcomes.

D03 owns Power Economy math, Expression cost, resource partition, carrier burden, confluence, overdraw/backlash, and expression re-authoring details.

D05 owns skills, professions, training, research, knowledge, language, synthesis, and competency rank mechanics.

D06 owns Path/Class/Dao, domain, route feature mechanics, technique access, route fusion/severance, and archetype/profession relations.

D07 owns harm, injury, recovery, crippling, death, unmaking, corruption recovery, and survival states.

D08 owns actor model, nonphysical actors, spirits, AIs, swarms, companions, summons, avatars, and actor-state transformation.

D09 owns items, relics, tools, implants, vehicles, ships, platforms, external anchors, and installable assets.

D10 owns factions, territory, law, standing, travel/exploration, economy, settlement, world-state, and recognition.

## 17. Batch C schema handoff

D04 may require future schema records for actor progression state, proof ledger, Development Pick records, advancement axes, route ledger, awakening package, breakthrough state, payloads, capstone record, and Ascension Access.

These are runtime/progression schema needs, not conversion-stage content schemas unless converted donor material specifically produces such records.

## 18. Conversion intake implications

Donor progression constructs should map into D04 using lawful outcomes: direct Astra mapping only if D04 already owns function cleanly; normalized Astra mapping if donor function can translate without donor law; source-local retained construct if bounded; quarantine if missing D04/D03/D05-D10 owner support; escalation if recurring pressure exposes missing doctrine.

Donor level tables, realms, class features, feats, titles, achievements, capstones, ascensions, skill ranks, and item-growth tracks are evidence, not Astra law.

## 19. Validation gates

D04 advancement output is unsafe if it lacks proof refs, owner file, tier authorization check, route/access check, state delta, warning for dangerous/irreversible/lethal-risk advancement, source-local boundary where needed, separation between authorization and mastery, or distinction between proposed narration and committed state.

## 20. Runtime non-implementation clause

This file does not define database tables, code, API endpoints, or final runtime services. It defines required semantics for later schema and runtime implementation.
