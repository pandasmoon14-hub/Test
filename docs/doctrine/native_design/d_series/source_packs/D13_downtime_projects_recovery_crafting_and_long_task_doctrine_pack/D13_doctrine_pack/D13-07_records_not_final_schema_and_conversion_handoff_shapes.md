# D13-07 — Records, Not-Final Schema, and Conversion Handoff Shapes

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

What minimum records and control checks does D13 need so downtime, Projects, recovery, crafting, repair, salvage, research, training, maintenance, and source-local long-task systems remain auditable during conversion, canon review, future runtime design, and eventual live play?

D13-07 defines lightweight not-final-schema record shapes. These are doctrine-facing and conversion-facing controls. They are not final runtime schemas, database tables, crafting schemas, recovery schemas, economy schemas, faction schemas, or campaign-state schemas.

## Record posture

Every record shape in this file is:

```text
not final schema
doctrine-facing / conversion-facing control shape
runtime Gate B or later schema doctrine may replace or formalize this
```

Record shapes exist to prevent ambiguity during conversion and doctrine review.

## Project Record

```yaml
project_record:
  record_type: project
  project_id: string
  project_goal: string
  project_family: recovery | training | research | crafting | salvage | repair | installation_preparation | resource_gathering | social_project | faction_support | preparation | maintenance | special_source_local | mixed
  secondary_families: []
  scope_band: minor | standard | major | extended | transformational
  interval_scale: hours | days | weeks | months | season | travel_leg | recovery_block | facility_cycle | source_local_interval | other
  current_status: not_started | ready | active | progressing | blocked | complicated | paused | interrupted | completed | completed_with_complication | failed | abandoned | quarantined | escalated | archived
  primary_actor_ref: string
  contributor_refs: []
  requirement_refs: []
  support_asset_refs: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  hidden_requirement_present: true | false | unknown
  notes: string
```

## Project Requirement Record

```yaml
project_requirement_record:
  record_type: project_requirement
  requirement_id: string
  project_ref: string
  requirement_type: time | safe_location | materials | tools | facility | assistant | access_tag | method_competency | resource_cost | information | permission_license | reputation_standing | body_condition | object_condition | route_technique_domain | source_local_prerequisite | other
  status: met | missing | unknown | protected_hidden | blocked_by_owner_file | source_local | quarantined
  owner_file: D03 | D04 | D05 | D06 | D07 | D08 | D09 | D10 | D13 | D15 | D17 | D18 | source_local | unknown
  visible_to_player: true | false | partial
  commitment_required: true | false
  notes: string
```

## Project Interval Record

```yaml
project_interval_record:
  record_type: project_interval
  interval_id: string
  project_ref: string
  interval_scale: string
  committed_time: string
  committed_costs: []
  committed_exposures: []
  active_method: string
  active_contributors: []
  facility_or_location_ref: string | null
  progress_check_required: true | false
  progress_check_reason: uncertainty | opposition | risk | unstable_requirement | hidden_pressure | acceleration | interruption | source_local_procedure | none
  resolution_owner: D02 | source_local | none
  notes: string
```

## Project Progress Event Record

```yaml
project_progress_event_record:
  record_type: project_progress_event
  progress_event_id: string
  project_ref: string
  interval_ref: string
  interval_outcome: advanced | advanced_with_cost | partial | stalled | blocked | complicated | damaged | interrupted | completed | completed_with_complication | failed | abandoned | quarantined | escalated
  completion_state: none | partial | complete | failed | terminal | unknown
  owner_file_handoffs: []
  state_delta_refs: []
  unresolved_pressure_refs: []
  notes: string
```

## Project Complication Record

```yaml
project_complication_record:
  record_type: project_complication
  complication_id: string
  project_ref: string
  complication_family: cost_increase | delay | material_loss | tool_or_facility_damage | assistant_risk | injury_or_condition_setback | corruption_or_instability_pressure | object_instability | social_scrutiny | faction_attention | legal_exposure | information_false_lead | hidden_pressure_surface | source_local_threat | active_scene_trigger | owner_file_gap | other
  severity: low | medium | high | blocking
  owner_file: D03 | D07 | D08 | D09 | D10 | D12 | D15 | D17 | D18 | source_local | unknown
  immediate_scene_trigger: true | false
  quarantine_or_escalation_required: true | false
  notes: string
```

## Contributor / Support Record

```yaml
project_contributor_support_record:
  record_type: project_contributor_support
  support_id: string
  project_ref: string
  support_type: contributor | facility | material | tool | platform | license | access_tag | favor | funding | crew | automated_system | source_local_support
  support_role: primary_worker | assistant | mentor | specialist | crew | guard | sponsor | supplier | research_aide | ritual_participant | patient | test_subject | faction_representative | facility_operator | companion_summon | automated_system | other
  support_function: method_support | access_permission | labor | protection | materials | knowledge | facility_operation | social_cover | faction_authorization | risk_absorption | acceleration | stability | other
  burden_or_risk: []
  owner_file: D05 | D08 | D09 | D10 | D15 | D17 | D18 | source_local | unknown
  notes: string
```

## Interruption / Abandonment Record

```yaml
project_interruption_abandonment_record:
  record_type: project_interruption_or_abandonment
  event_id: string
  project_ref: string
  event_type: interruption | abandonment | pause | resume | archive
  trigger: active_scene | resource_loss | facility_loss | assistant_withdrawal | injury | travel | attack | legal_action | faction_pressure | hidden_threat | material_spoilage | object_instability | relationship_rupture | campaign_time_skip | source_local_event | other
  outcome: pause_without_loss | pause_with_decay | delay | cost_increase | progress_loss | requirement_change | complication_added | active_scene_triggered | project_split_required | project_abandoned | project_quarantined | project_escalated | archived
  lost_elements: []
  preserved_elements: []
  exposed_elements: []
  recoverable_elements: []
  unresolved_pressure_refs: []
  owner_file_handoffs: []
  notes: string
```

## Donor Project Mapping Record

```yaml
donor_project_mapping_record:
  record_type: donor_project_mapping
  donor_label: string
  donor_function_summary: string
  donor_interval_assumption: string | null
  state_changed_by_donor_procedure: []
  mapped_project_family: string | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```

## Owner-file handoff expectations

A D13 record may point to owner-file handoff. It must not mutate or define the other file's state.

Examples:

- D13 Project Progress Event says a repair Project completed with complication. D09 decides the object-state result.
- D13 Research Project says a partial result occurred. D10/D11 decide what information can be known and surfaced.
- D13 Recovery Project says an interval advanced. D07 decides condition or injury changes.
- D13 Social Project says relationship repair progressed. D10/D15 decide actual relationship or faction-state updates.

## Hidden-state control

Records may mark hidden requirements, hidden pressure, or protected owner-file content as present, unknown, or protected. They must not expose hidden truth in player-facing form.

## Anti-drift controls

- Do not treat record fields as final runtime schema.
- Do not add final mechanics to record shapes.
- Do not use record completeness as canon promotion.
- Do not omit source-local boundaries when donor systems are retained.
- Do not omit rejected imports from donor project mappings.
