# B08 Travel, Exploration, Navigation, and Discovery Procedure

## 1. Purpose and status

B08 is the eighth Batch B operational doctrine draft for Astra travel, exploration, navigation, route posture, route or area declaration, party-facing known-state review, scouting, mapping, discovery opportunities, travel/exploration intervals, site approach, site entry, watches, ambush exposure, travel pressure, resource and exposure triggers, hazard/encounter/contact trigger identification, and transition handoffs. It sits after B01 scene/activity/encounter procedure, B02 action declaration/cost commitment/resolution trigger procedure, B03 item/gear/equipment/object-system construct and asset-use procedure, B04 inventory/storage/custody/burden procedure, B05 acquisition/reward/requisition/value-flow procedure, B06 project-centered interval work, and B07 recovery/training/research/preparation procedure.

Status posture:
- This file is Batch B operational-procedure draft material.
- This file is not current canon, not final mechanics, not runtime authority, not sourcebook prose, and not player-facing rule text.
- C00 remains the schema handoff control surface for Batch B to C-family routing.
- B08 treats B01-B07 as upstream Batch B context and must build on them, not rewrite them.
- D00-D19 source-pack files are referenced only as draft source-pack/reference material. They are not current doctrine authority, final mechanics, runtime authority, canon, sourcebook prose, or Astra defaults.
- B08 records, examples, and handoff blocks are doctrine-facing only; they are not runtime state, backend contracts, sourcebook statblocks, canon entries, player-facing rule text, accepted lexicon, final travel schemas, final exploration schemas, final map schemas, final location schemas, final route schemas, final discovery schemas, final hazard schemas, final encounter schemas, final world-state schemas, travel tables, encounter tables, map database rows, or final mechanics.

Required reference boundaries preserved by B08:
- `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md` for upstream scene, activity, encounter, transition, checkpoint, and owner-file handoff procedure.
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` for upstream action declaration, feasibility, cost commitment, resolution trigger, no-roll/roll-trigger, and action-to-delta procedure.
- `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md` for item, gear, equipment, object-system construct, object readiness, object use, object-state handoff, platform/object pressure, and asset-use routing procedure.
- `docs/doctrine/operations/batch_b/B04_inventory_storage_custody_and_burden_procedure.md` for inventory, storage, custody, possession, access, burden, lawful loss, recovery, and inventory/custody routing procedure.
- `docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md` for acquisition, reward, requisition, scarcity, upkeep, value sink, value commitment, market access, supply pressure, and value-flow routing procedure.
- `docs/doctrine/operations/batch_b/B06_project_crafting_salvage_repair_and_upgrade_procedure.md` for project-centered interval work, project intake, requirement discovery, protected-hidden requirement handling, cost/risk preview, interval setup, progress routing, complications, concurrent support, output routing, source-local project quarantine, and not-final C00/C-family handoff posture.
- `docs/doctrine/operations/batch_b/B07_recovery_training_research_and_preparation_project_procedure.md` for recovery, training, research, preparation, readiness, proof routing, desired-outcome routing, and non-object project output boundaries.
- `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` for shared Batch C base fields, `pending_schema`, source-local boundary, rejected donor element, canon eligibility, review routing, provenance, and missing-schema fallback language.
- `docs/doctrine/native_design/d_series/source_packs/astra_d00_doctrine_pack_v0_1/D00-03_state_delta_commit_protocol.md` for the draft source-pack principle that every meaningful operational event commits at least one delta to a recognized owner, while B08 does not own every delta format.
- `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-00_resolution_architecture_and_owner_boundaries.md` and `docs/doctrine/native_design/d_series/source_packs/astra_d05_doctrine_pack_v0_1/D05-03_relevance_handling_for_checks.md` for draft resolution and relevance boundaries, while B08 must not define final resolution math, final navigation DCs, or final scouting check math.
- `docs/doctrine/native_design/d_series/source_packs/astra_d03_doctrine_pack_v0_1/astra_d03_doctrine_pack_v0_1/D03_01_power_economy_lattice.md`, `docs/doctrine/native_design/d_series/source_packs/astra_d07_doctrine_pack_v0_1/D07-02_corruption_contamination_and_instability.md`, and `docs/doctrine/native_design/d_series/source_packs/astra_d07_doctrine_pack_v0_1/D07-07_recovery_treatment_stabilization_and_adaptation.md` for draft power, environmental, corruption, contamination, instability, recovery, treatment, stabilization, and adaptation pressure source material, while B08 must not expose hidden Pneuma, hidden cosmic modifiers, protected-hidden truth, final harm, final exposure math, or final recovery rules.
- `docs/doctrine/native_design/d_series/source_packs/astra_d09_doctrine_pack_v0_1/D09-05_vehicles_platforms_ships_mechs_drones_and_external_bodies.md` for draft vehicle, platform, ship, mech, drone, and external-body source material, while B08 must not define final platform state or fuel economy.
- `docs/doctrine/native_design/d_series/source_packs/astra_d10_doctrine_pack_v0_1/D10-02_territory_location_hazard_control_environment_register.md`, `docs/doctrine/native_design/d_series/source_packs/astra_d10_doctrine_pack_v0_1/D10-07_information_state_public_knowledge_rumor_secrecy_records_register.md`, and `docs/doctrine/native_design/d_series/source_packs/astra_d11_doctrine_pack_v0_1/D11-03_hidden_state_rumor_secrecy_misinformation_presentation.md` for draft world-state, territory, location, hazard-control, information-state, rumor, secrecy, misinformation, and safe-presentation source material, while B08 must not decide actual world truth or hidden-state reveal rules.
- `docs/doctrine/native_design/d_series/source_packs/D12_time_action_cadence_encounter_and_turn_procedure_doctrine_pack/D12_doctrine_pack/D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md` for draft checkpoint, cost commitment, consequence timing, and active-procedure handoff source material, while B08 must not define final active-scene cadence or sequencing.
- `docs/doctrine/native_design/d_series/source_packs/D13_downtime_projects_recovery_crafting_and_long_task_doctrine_pack/D13_doctrine_pack/D13-02_project_creation_requirement_discovery_commitment_and_interval_setup.md` for draft project interval source material, while B08 must not redefine B06/B07 project procedure.
- D14 source-pack files `D14-00` through `D14-07` for draft travel, exploration, navigation, discovery, posture, route, known-state, interval, scouting, mapping, context-profile, site-entry, watch, ambush-exposure, pressure, source-local donor, and not-final record source material, while B08 must convert those ideas into Batch B boundaries rather than promote D14 as current doctrine authority.
- `docs/doctrine/native_design/d_series/source_packs/D15_faction_relationship_domain_and_institutional_operations_doctrine_pack/D15_doctrine_pack/D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md`, `docs/doctrine/native_design/d_series/source_packs/D16_opposition_creature_encounter_and_hazard_construction_doctrine_pack/D16_doctrine_pack/D16-00_opposition_creature_encounter_and_hazard_construction_owner_boundaries.md`, `docs/doctrine/native_design/d_series/source_packs/D17_economy_acquisition_inventory_reward_and_requisition_doctrine_pack/D17_doctrine_pack/D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md`, and `docs/doctrine/native_design/d_series/source_packs/D18_structural_time_campaign_continuity_arc_season_and_horizon_doctrine_pack/D18_doctrine_pack/D18-00_structural_time_campaign_continuity_arc_season_and_horizon_owner_boundaries.md` for draft faction, opposition/hazard, economy/supply, and campaign-scale journey-pacing owner boundaries, while B08 must not define faction clocks, encounter construction, supply attrition, or campaign-scale time-skip procedure.
- `docs/doctrine/native_design/d_series/source_packs/D19_cross_pack_integration_conflict_audit_and_conversion_readiness_capstone_pack/D19_capstone_doctrine_pack/D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md` for draft record-shape governance and schema handoff source material, while B08 must not invent final schema fields.

## 2. Owner layer

B08 belongs to Batch B operational doctrine. It routes travel/exploration/navigation/discovery procedure between upstream Batch B procedure, C00 schema handoff controls, future C-family schema families, source-local donor quarantine, and later world, information, presentation, faction, opposition/hazard, economy/supply, platform, campaign-time, runtime, canon, and training owners.

B08 may identify that a handoff is needed to a likely owner, but it must not perform that owner's work. When B08 cannot identify a valid owner or schema family, it must mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` instead of inventing Astra schema, mechanics, runtime state, hidden truth, canon geography, sourcebook prose, map rows, travel tables, encounter tables, or live-play narration.

## 3. What B08 owns

B08 owns doctrine-level operational procedure for:
- travel/exploration intake after B01-B07 produce route, area, movement, navigation, discovery, site-entry, or travel-pressure questions;
- travel/exploration intent checkpoint;
- posture declaration and posture-pressure routing;
- route/area declaration and route-state classification;
- party-facing known-state review;
- protected-hidden route, map, and world-state handling without revealing truth;
- travel/exploration interval setup;
- navigation/orientation trigger routing;
- scouting procedure;
- mapping procedure and map-state update routing;
- discovery opportunity classification and discovery-confidence routing;
- exploration context profile classification;
- site approach and site entry procedure;
- watch and monitoring procedure;
- ambush exposure procedure;
- environmental PCR travel-pressure routing without leaking hidden cosmic truth;
- travel resource/exposure pressure trigger identification;
- hazard/encounter/contact trigger identification as routing, not construction;
- transition handoff to B01/B02/D12 when travel becomes active scene procedure or structured encounter procedure;
- transition handoff to B03/B04/B05/B06/B07 where object, custody, value, project, recovery, training, research, or preparation pressure dominates;
- transition handoff to D10/D11-style world-state/information/presentation owners where actual truth or safe presentation matters;
- transition handoff to D15/D16/D17/D18-style owners where faction, opposition/hazard, economy/supply, or campaign-scale journey pacing matters;
- B08-to-C00/C-family handoff references when travel/exploration/navigation/discovery handling produces conversion records;
- source-local donor travel/exploration/hexcrawl/dungeon-turn/random-encounter/scouting/mapping/ship-travel/realm-travel systems quarantine and escalation rules;
- examples of good and bad B08 usage; and
- minimum acceptance criteria for B08.

## 4. What B08 must not own

B08 must not define or promote:
- final travel schema, final exploration schema, final map schema, final location schema, final route schema, final discovery schema, final hazard schema, final encounter schema, final world-state schema, C-family schema fields, or C01-C14 schema contents;
- final map geometry, final hex rules, final grid rules, final zone/node rules, final dungeon-turn procedure, final watch-shift system, final travel-day procedure, final travel pace math, final navigation DCs, final scouting check math, final random encounter tables, final weather tables, final hazard tables, final supply attrition math, final fuel economy, final exposure/harm math, final encounter construction, final opposition statblocks, final site keys, or boxed text;
- final world truth, final hidden-state reveal rules, final presentation/narration behavior, final faction clocks, final territory-control systems, final campaign-scale journey pacing, or final time-skip procedure;
- runtime travel state, runtime location state, runtime map state, runtime world-state database, runtime encounter generation, runtime entity/component/event/state schemas, persistent campaign state, command lifecycle implementation, context packet compiler, hidden-information runtime state, or live-play narration behavior;
- final canon promotion, accepted lexicon terms, sourcebook prose, or donor travel/exploration/map/hexcrawl/dungeon/ship/realm/random-table systems as Astra defaults.

## 5. Non-collapse rule

B08 keeps these categories separate:
- Travel is not automatic time passage.
- Exploration is not automatic map reveal.
- Navigation is not always a roll.
- A route is not necessarily geometric.
- A map is not truth.
- Party-facing known-state is not actual world-state.
- A discovery is not automatically actual truth.
- Scouting is not hidden-truth revelation.
- Mapping is not canon creation.
- Site entry is not boxed-text reveal.
- A watch is not a universal shift system.
- Ambush exposure is not automatic surprise.
- Hazard pressure is not hazard construction.
- Encounter pressure is not encounter generation.
- Random encounters are not default Astra law.
- Environmental PCR may shape travel pressure but must not expose hidden Pneuma, hidden cosmic modifiers, hidden truth, or protected-hidden state.
- Posture is not a flat modifier.
- Route progress is not universal travel pace.
- Travel intervals are not universal travel turns, dungeon turns, watches, hex moves, jumps, phases, rounds, or travel days.

Every meaningful travel/exploration/navigation/discovery event must route at least one delta to a recognized owner or explicitly produce a no-delta, quarantine, escalation, transition, source-local, `pending_schema`, `human_review`, or `defer_until_schema_exists` result.

## 6. Travel, exploration, navigation, discovery, route, map-state, and site-entry definitions

For B08 purposes:
- `travel` is operational movement through a declared route, vector, corridor, district sequence, lane, platform route, realm crossing, threshold, or source-local movement construct. It is not automatic time passage, universal travel pace, or campaign-scale journey pacing.
- `exploration` is operational investigation of uncertain space, area, route, site, terrain, platform, social district, hazardous zone, realm boundary, or unknown context. It is not automatic map reveal or canon creation.
- `navigation` is orientation, route maintenance, route correction, vector control, threshold control, landmark use, chart reading, sensor interpretation, social wayfinding, ritual/survey alignment, or source-local direction handling. It is not always a roll and does not define final DCs.
- `discovery` is a doctrine-facing opportunity, result, clue, correction, trace, location lead, hazard indication, resource lead, boundary hint, route update, or source-local find. It is not automatically actual truth.
- `route` is a functional travel path, vector, corridor, lane, trail, road, district sequence, jump line, platform route, realm crossing, approach path, pursuit path, or evasion path. It need not be geometric.
- `area` is a region, district, ruin, site, wilderness, platform section, city sector, plane-local region, battlefield, hazardous zone, search space, or source-local exploration unit.
- `map-state` is party-facing or doctrine-facing representation of known, surveyed, suspected, false, compromised, blocked, hidden, or source-local spatial/information confidence. A map is not truth.
- `site approach` is the operational process of reaching, observing, probing, positioning around, negotiating access to, or testing the boundary of a site before entry.
- `site entry` is the transition from outside/boundary posture into an interior, thresholded, restricted, hidden, unstable, guarded, social, platform, realm, or source-local site context. It is not boxed-text reveal.

B08 uses the following vocabulary as doctrine-facing labels only. These labels are not final schemas, accepted lexicon, runtime state, sourcebook terms, map records, encounter tables, or final mechanics.

Travel/exploration intents:
- `route_travel`
- `area_exploration`
- `site_approach`
- `site_entry`
- `pursuit`
- `evasion`
- `scouting`
- `mapping`
- `tracking`
- `resource_search`
- `survey_analysis`
- `social_blending`
- `platform_navigation`
- `vehicle_travel`
- `ship_travel`
- `realm_crossing`
- `threshold_crossing`
- `hazardous_zone_crossing`
- `unknown_space_exploration`
- `source_local_exploration`
- `mixed_exploration`
- `unknown_intent`

Posture families:
- `speed`
- `safety`
- `stealth`
- `scouting`
- `mapping`
- `tracking`
- `foraging_resource_search`
- `concealment`
- `diplomatic_approach`
- `survey_analysis`
- `ritual_sensing`
- `sensor_sweep`
- `platform_caution`
- `resource_conservation`
- `pursuit`
- `evasion`
- `combat_readiness`
- `social_blending`
- `source_local_posture`

Route states:
- `known`
- `partially_known`
- `suspected`
- `rumored`
- `hidden`
- `false`
- `blocked`
- `dangerous`
- `contested`
- `watched`
- `restricted`
- `unstable`
- `unmapped`
- `source_local`

Known-state categories:
- `confirmed_known`
- `party_believes`
- `rumored`
- `suspected`
- `mapped_but_unverified`
- `false_or_compromised`
- `hidden_from_party`
- `protected_hidden`
- `source_local`

Interval scales:
- `momentary_approach`
- `scene_segment`
- `site_segment`
- `district_leg`
- `wilderness_leg`
- `watch_period`
- `platform_vector`
- `stealth_segment`
- `site_survey_pass`
- `realm_crossing_stage`
- `search_sweep`
- `source_local_interval`
- `unknown_interval`

Discovery categories:
- `route_discovery`
- `location_discovery`
- `site_entry_discovery`
- `hazard_discovery`
- `resource_discovery`
- `clue_or_lead_discovery`
- `faction_presence_discovery`
- `opposition_trace_discovery`
- `environmental_condition_discovery`
- `object_or_salvage_discovery`
- `map_correction`
- `false_route_exposure`
- `hidden_boundary_hint`
- `source_local_discovery`

Discovery confidence states:
- `confirmed`
- `high_confidence`
- `partial`
- `ambiguous`
- `rumored`
- `suspected`
- `false_or_compromised`
- `protected_hidden`
- `source_local`

Map-state categories:
- `known`
- `surveyed`
- `partially_mapped`
- `suspected`
- `rumored`
- `false`
- `compromised`
- `hidden`
- `blocked`
- `unreachable`
- `source_local`

Exploration context profiles:
- `urban_social_dense`
- `wilderness_open_region`
- `site_dungeon_interior`
- `space_vehicle_platform`
- `dimensional_realm_threshold`
- `hazardous_anomalous_zone`
- `pursuit_evasion`
- `tactical_terrain`
- `horror_hidden_site`
- `source_local_context`
- `mixed_context`
- `unknown_context`

Pressure families:
- `resource_pressure`
- `exposure_pressure`
- `hazard_pressure`
- `encounter_pressure`
- `navigation_pressure`
- `map_state_pressure`
- `ambush_exposure`
- `social_or_legal_pressure`
- `faction_or_territory_pressure`
- `object_or_platform_pressure`
- `hidden_state_pressure`
- `time_pressure`
- `source_local_pressure`

Progress states:
- `advanced`
- `advanced_with_cost`
- `advanced_with_discovery`
- `advanced_with_exposure`
- `delayed`
- `misdirected`
- `lost`
- `blocked`
- `hazard_triggered`
- `encounter_triggered`
- `site_entry_triggered`
- `map_state_updated`
- `pressure_escalated`
- `transitioned`
- `quarantined`
- `escalated`

## 7. Travel/exploration intake procedure

Use B08 when upstream Batch B procedure produces a travel, route, area, movement, navigation, discovery, scouting, mapping, site-approach, site-entry, watch, ambush-exposure, travel-pressure, or exploration-pressure question that is not already dominated by another owner.

Intake sequence:
1. Identify the upstream source: B01 scene/activity pressure, B02 declared action, B03 object/platform use, B04 custody/burden/access, B05 value/supply/requisition, B06 project interval, B07 preparation/research/scouting support, source-local donor procedure, or human design note.
2. Ask whether the dominant question is travel/exploration/navigation/discovery rather than scene cadence, action resolution, object state, custody, value, project output, recovery/training/research, world truth, hidden presentation, hazard construction, encounter construction, or campaign-scale time.
3. If B08 is dominant, open the B08 checkpoints in section 8.
4. If another owner is dominant, route there and preserve only a B08 transition note if travel/exploration pressure remains.
5. If the source procedure is donor-specific and cannot be cleanly normalized, mark source-local, quarantine, escalation, `human_review`, or `pending_schema` instead of importing the donor system as Astra default.

## 8. Intent, posture, route/area, known-state, and risk/handoff checkpoints

B08 front-end checkpoint order:
1. Intent checkpoint: classify the declared travel/exploration intent using section 6 labels or `unknown_intent`.
2. Posture checkpoint: identify one or more posture families and the pressures they imply. Posture is a priority declaration, not a flat modifier.
3. Route/area checkpoint: declare whether the party is following a route, exploring an area, approaching a site, crossing a threshold, pursuing, evading, mapping, scouting, or using a source-local construct.
4. Known-state checkpoint: review party-facing known-state without deciding actual world truth or revealing protected-hidden state.
5. Risk/handoff checkpoint: identify likely navigation, resource, exposure, hazard, encounter, faction, object/platform, hidden-state, time, schema, source-local, or active-scene handoffs before the interval proceeds.

A checkpoint may produce `no_delta_required` only when no meaningful route, risk, resource, exposure, map, discovery, owner, or transition change exists. Otherwise it must route at least one delta or mark quarantine/escalation/transition.

## 9. Route-state and known-state classification

Route-state classification:
- Classify route or area as one or more route states from section 6.
- Do not convert route state into final geometry, hex occupancy, grid position, node graph, location schema, travel pace, or map truth.
- A route may be `known` to the party while still carrying hidden, contested, watched, restricted, unstable, dangerous, or source-local pressure owned elsewhere.
- A route may be `false` or `rumored` without proving the actual world truth. D10-style owners handle actual truth; D11-style owners handle safe presentation.

Known-state classification:
- `confirmed_known` means the party-facing record has owner-supported confirmation; it does not mean B08 writes final world-state.
- `party_believes`, `rumored`, and `suspected` are belief/information categories, not truth claims.
- `mapped_but_unverified` means the map exists as an artifact or note but remains non-truth.
- `false_or_compromised` routes information, map, rumor, or deception pressure to world/information/presentation owners.
- `hidden_from_party` and `protected_hidden` must not be disclosed as hidden truth. B08 may mark protected handling for doctrine review only.
- `source_local` keeps donor-specific state bounded to its source-local context unless later converted by the appropriate owner.

## 10. Travel/exploration interval setup

A travel/exploration interval is the local doctrine-facing unit needed to ask one travel/exploration question. It is not a universal travel turn, dungeon turn, watch, hex move, jump, phase, round, travel day, time skip, or campaign journey segment.

Interval setup steps:
1. Choose an interval scale from section 6 or mark `unknown_interval`.
2. State the active intent, posture, route/area declaration, context profile, and known-state review reference.
3. Identify whether navigation/orientation pressure is present and whether B02/D02-style resolution routing might be needed.
4. Identify posture, environmental PCR, resource, exposure, support, hazard, encounter, contact, ambush, map-state, discovery, faction, object/platform, hidden-state, source-local, or time pressure.
5. State the expected result family: progress, delay, discovery, map update, lost-route, blocked-route, active-scene transition, owner-file handoff, quarantine, escalation, or no-delta.

B08 may structure an interval, but it must not define final interval duration, final travel-day cadence, final dungeon-turn cadence, final watch shifts, final movement rates, final progress clocks, or final pacing math.

## 11. Navigation and orientation trigger procedure

Navigation/orientation routing is triggered when the route, area, approach, pursuit, evasion, platform vector, threshold, or search space is uncertain, contested, distorted, false, hidden, unstable, watched, restricted, unmapped, source-local, or materially affected by posture/resource/environmental pressure.

Procedure:
1. Identify the navigation source: landmarks, map, memory, guide, rumor, trail, sensor, ritual sensing, social wayfinding, platform system, vehicle controls, ship course, realm threshold, tracking, scouting report, source-local rule, or unknown source.
2. Decide whether no-roll handling is sufficient because the route is currently clear and no meaningful uncertainty exists.
3. If uncertainty matters, route declaration and resolution trigger handling through B02 and D02-style resolution owners without defining final DCs, dice, navigation tables, or automatic failure modes.
4. If environmental PCR or hidden state shapes navigation pressure, route visible pressure without exposing hidden Pneuma, hidden cosmic modifiers, hidden truth, or protected-hidden state.
5. Convert outcomes into B08 progress states, map-state pressure, discovery pressure, active-scene transition, owner handoff, quarantine, escalation, or no-delta as appropriate.

## 12. Posture pressure and environmental PCR routing

Posture pressure is the effect of declared travel priorities on what becomes easier, harder, visible, missed, exposed, delayed, protected, depleted, escalated, or handed off. B08 may identify posture pressure but must not convert posture into a universal bonus/penalty.

Examples of posture-pressure routing:
- `speed` may route progress pressure plus exposure, hazard, or ambush pressure.
- `safety` may route delay, scouting, mapping, or resource pressure.
- `stealth` may route detection, time, pursuit/evasion, and ambush-exposure pressure.
- `mapping` may route map-state updates, discovery opportunities, exposure, or delay.
- `sensor_sweep` may route object/platform use to B03, signal/contact pressure to D10/D11-style owners, and possible opposition/hazard routing to D16-style owners.
- `ritual_sensing` may route D03/D07-style strain or corruption/instability pressure without revealing hidden cosmic truth.

Environmental PCR travel routing:
- B08 may mark visible environmental pressure affecting navigation, discovery, exposure, resources, or site approach.
- B08 must not expose hidden Pneuma, hidden cosmic modifiers, hidden truth, protected-hidden state, or hidden owner notes.
- If environmental pressure needs truth validation, route to D10-style owners.
- If environmental pressure needs safe presentation, route to D11-style owners.
- If environmental pressure creates active risk, route to B01/B02/D12, D16-style hazard/opposition owners, B03/B04/B05 owners, or B07 recovery/preparation owners as appropriate.

## 13. Resource, exposure, and support-pressure trigger routing

B08 may identify that travel/exploration creates resource, exposure, or support-pressure triggers, but it must not define resource loss, supply attrition, harm, fuel economy, weather damage, exposure math, upkeep math, or recovery math.

Trigger examples:
- `resource_pressure`: supplies, fuel, ammunition-like stores, charge, water, shelter, tools, guides, access tokens, permits, bribes, maps, medicine, power reserves, or source-local consumables may matter. Route custody/access to B04, value/supply/requisition/upkeep to B05/D17-style owners, object/tool/platform state to B03, project preparation to B06/B07, and final resource math elsewhere.
- `exposure_pressure`: heat, cold, vacuum, contamination, corruption, instability, radiation-like pressure, weather, fatigue, disease-like pressure, poison-like pressure, social exposure, surveillance, or source-local hazard pressure may matter. Route harm/exposure/recovery to D07/B07-style owners and active-scene handling to B01/B02/D12 when needed.
- `support-pressure`: guides, scouts, mounts, vehicles, ships, drones, companions, local permits, faction escorts, safehouses, routes, charts, or prepared camps may matter. Route object/platform issues to B03, custody/burden to B04, value/upkeep/access to B05, preparation/project work to B06/B07, and faction/social access to D15-style owners.

## 14. Scouting procedure

Scouting is the operational attempt to learn, test, observe, probe, listen, track, sweep, infiltrate, watch, or preview route/area/site pressure. Scouting is not hidden-truth revelation.

Scouting steps:
1. Declare scouting intent, method, scope, posture, range, and risk tolerance using B02 declaration grammar when action-level detail matters.
2. Identify what can be learned safely as party-facing known-state, what is uncertain, and what remains protected-hidden.
3. Route object/tool/sensor/platform use to B03, custody/access/burden issues to B04, cost/value/support issues to B05, project/preparation/research support to B06/B07, and resolution uncertainty to B02/D02-style owners.
4. Classify any discovery opportunity and confidence state without treating discovery as actual truth.
5. Route hazard/contact/opposition pressure to D16-style owners when construction is needed, but do not build hazard math, encounter math, or statblocks.
6. Return one of: discovery opportunity, map-state pressure, route-state update, ambush-exposure note, active-scene transition, source-local retention, quarantine, escalation, or no-delta.

## 15. Mapping and map-state update procedure

Mapping is the operational attempt to record, correct, survey, compare, chart, tag, sketch, scan, remember, annotate, or reconcile route/area/site information. Mapping is not canon creation and a map is not truth.

Mapping steps:
1. Identify the mapping source: prior map, memory, guide, scouting, sensor sweep, survey analysis, ritual sensing, social directions, platform navigation, route travel, site approach, discovery, donor map, or source-local procedure.
2. Classify current map-state and proposed update using section 6 categories.
3. Identify whether the update improves, degrades, confirms, contradicts, complicates, invalidates, or quarantines the party-facing map-state.
4. Route actual truth questions to D10-style owners and safe-presentation questions to D11-style owners.
5. Route map-object custody to B04, map-object use/state to B03, acquisition/value/access to B05, preparation/research mapping projects to B06/B07, and schema conversion to C00/C-family handoff when appropriate.
6. Do not define final map geometry, hexes, grids, zones, nodes, sourcebook maps, canonical locations, or runtime map state.

## 16. Discovery opportunity and discovery-confidence procedure

A discovery opportunity is a doctrine-facing chance or result indicating that travel/exploration may produce a route, location, site-entry, hazard, resource, clue/lead, faction-presence, opposition-trace, environmental-condition, object/salvage, map-correction, false-route exposure, hidden-boundary hint, or source-local discovery.

Procedure:
1. Identify the discovery source: posture, navigation, scouting, mapping, tracking, survey analysis, ritual sensing, sensor sweep, social blending, resource search, environmental PCR, site approach, owner-supported pressure, failed/partial result, hazard proximity, faction movement, object/platform sensor, source-local procedure, or scenario design.
2. Classify the discovery category and confidence state using section 6.
3. State whether discovery is party-facing information, a hypothesis, a lead, a map update, a route update, a site-entry trigger, an active-scene transition, or owner-file pressure.
4. Route actual truth to D10-style owners and presentation/secrecy/misinformation to D11-style owners.
5. If the discovery is object/salvage/resource/value-facing, route to B03/B04/B05/B06 as needed.
6. If the discovery creates recovery/research/preparation pressure, route to B07.
7. Do not reveal protected-hidden state, write canon, create sourcebook geography, or turn ambiguous discovery into actual truth.

## 17. Exploration context profile classification

Classify exploration context before selecting interval and pressure handling:
- `urban_social_dense`: emphasizes social/legal pressure, restricted access, surveillance, crowds, rumors, routes through districts, and faction/territory handoffs.
- `wilderness_open_region`: emphasizes route uncertainty, exposure, resource pressure, hazards, weather-like pressure, and mapping uncertainty without adopting hexcrawl defaults.
- `site_dungeon_interior`: emphasizes boundaries, site segments, watches, ambush exposure, route blockage, hidden/false map-state, and active-scene transitions without adopting dungeon-turn procedure.
- `space_vehicle_platform`: emphasizes platform/ship/vehicle vectors, systems, fuel/support pressure, sensor posture, and object/platform handoffs without defining fuel economy or ship-travel law.
- `dimensional_realm_threshold`: emphasizes threshold crossing, realm-stage pressure, hidden-state handling, protected environmental PCR pressure, and D10/D11/D03/D07-style handoffs without defining realm metaphysics.
- `hazardous_anomalous_zone`: emphasizes exposure, contamination, instability, hazard pressure, navigation distortion, and protected-hidden truth routing without constructing hazards.
- `pursuit_evasion`: emphasizes posture conflict, tracking, concealment, speed, route choice, contact pressure, and active-scene transition without final chase rules.
- `tactical_terrain`: emphasizes approach, line-of-contact, cover-like pressure, ambush exposure, and B01/B02/D12 transition without final tactical map law.
- `horror_hidden_site`: emphasizes rumor, suspicion, false/compromised map-state, protected-hidden truth, site-entry pressure, and D11-style presentation routing without boxed text.
- `source_local_context`, `mixed_context`, and `unknown_context` require explicit boundary notes, quarantine/escalation if unsupported, and no donor default adoption.

## 18. Site approach and site entry procedure

Site approach procedure:
1. Identify approach intent, posture, route/area declaration, known-state, map-state, and context profile.
2. Identify visible boundaries, access points, restrictions, watched/contested/unstable pressure, environmental pressure, social/legal pressure, object/platform pressure, and source-local procedure.
3. Route scouting, mapping, resource, exposure, hazard, contact, and hidden-state pressure to the appropriate sections and owners.
4. Decide whether approach remains a B08 interval, transitions to B01 focused scene/freeform scene, triggers B02 action declaration, or escalates to D12-style structured timing.

Site entry procedure:
1. Classify entry as known, discovered, forced, hidden, restricted, unstable, social, platform, realm/threshold, source-local, or unknown.
2. Confirm what is party-facing known-state without using entry as boxed-text reveal.
3. Identify whether site entry triggers map-state update, discovery, watch/ambush exposure, hazard/contact/opposition pressure, object/custody/value pressure, or active-scene transition.
4. Route active procedure to B01/B02/D12 when entry becomes a scene, activity, or encounter.
5. Route truth/presentation to D10/D11-style owners, hazards/opposition to D16-style owners, faction/social access to D15-style owners, and campaign-scale entry/travel pacing to D18-style owners when needed.

## 19. Watch, monitoring, and ambush exposure procedure

A watch is a monitoring posture or assignment for a travel/exploration interval. It is not a universal shift system. B08 may identify watch pressure but must not define final watch-shift rules, final rest cadence, final detection math, or final surprise rules.

Watch/monitoring procedure:
1. Identify watch type: guard, scout, sensor, ritual, social, rear, platform systems, faction surveillance, source-local, or none.
2. Identify assigned actor/tool/platform/support only as doctrine-facing refs; route actor state elsewhere, object/platform use to B03, custody to B04, value/support to B05, and recovery/rest conflicts to B07.
3. Identify what the watch is trying to notice or protect: route change, contact, hazard, map-state contradiction, ambush exposure, resource/exposure pressure, social/legal pressure, or hidden-state pressure.
4. Route uncertainty through B02/D02-style owners without defining final detection math.

Ambush exposure procedure:
1. Identify exposure source: posture, route state, map-state error, environmental PCR, scouting gap, watch gap, pursuit/evasion, restricted area, opposition movement, hazard proximity, source-local procedure, or protected-hidden owner pressure.
2. Classify ambush exposure as none, possible, elevated, active, hidden, source-local, quarantined, or escalated.
3. Ambush exposure is not automatic surprise. If active procedure begins, hand off sequencing to B01/B02/D12 and opposition construction to D16-style owners.

## 20. Hazard, encounter, contact, and opposition trigger routing

B08 identifies hazard, encounter, contact, and opposition triggers as routing, not construction.

Trigger routing:
- `hazard_pressure` means a travel/exploration condition may become harmful, obstructive, unstable, costly, revealing, or active. Route construction to D16-style hazard owners and harm/exposure/recovery to D07/B07-style owners as needed.
- `encounter_pressure` means travel/exploration may transition into a focused scene, structured encounter, social contact, chase, negotiation, confrontation, hazard scene, or source-local encounter. Route scene/encounter handling to B01/B02/D12 and construction to D16-style owners.
- `contact_pressure` means another actor, faction, authority, creature, vehicle, sensor, rumor network, witness, scout, or hidden presence may matter. Route faction/institution/territory to D15-style owners, opposition profiles to D16-style owners, information/presentation to D10/D11-style owners, and active procedure to B01/B02/D12.
- Random encounters are not default Astra law. Random-table output from a donor source is source-local evidence at most and must be normalized, quarantined, escalated, or routed; it must not become runtime encounter generation.

## 21. Travel/exploration progress, delay, lost-route, blocked-route, discovery, and transition routing

B08 progress routing converts interval outcomes into owner-facing results:
- `advanced`: route/area progress occurred without additional meaningful pressure or with owner-routed no-delta support.
- `advanced_with_cost`: progress occurred with cost pressure routed to B02/B04/B05/D17-style owners or another valid owner; B08 does not define cost math.
- `advanced_with_discovery`: progress occurred and a discovery opportunity or map-state update is routed.
- `advanced_with_exposure`: progress occurred and exposure pressure is routed without defining harm math.
- `delayed`: progress slowed; route cause to posture, resource, map-state, hazard, social/legal, faction, object/platform, or time owner.
- `misdirected` or `lost`: route navigation/map-state/known-state pressure to D10/D11-style owners and B02/D02-style resolution owners without inventing map truth.
- `blocked`: route blockage to world/location, hazard, faction, object/platform, value/access, source-local, or active-scene owners.
- `hazard_triggered`, `encounter_triggered`, or `site_entry_triggered`: hand off to B01/B02/D12 and D16/D10/D11-style owners as needed.
- `map_state_updated`: route mapping update without canon creation.
- `pressure_escalated`: route to the relevant owner or human review.
- `transitioned`: record the receiving owner and stop B08 handling.
- `quarantined` or `escalated`: preserve donor/source/schema boundary and stop unsupported conversion.

## 22. Owner-file handoff rules

B08 handoffs must identify owner responsibility rather than inventing content. Use these routing rules:
- B01 receives active scene, focused activity, structured encounter, scene transition, or encounter-pressure handling.
- B02 receives action declaration, feasibility, cost commitment, resolution trigger, no-roll/roll-trigger, and action-to-delta handling.
- B03 receives object, gear, tool, map-object, vehicle, ship, platform, sensor, drone, external-body, or equipment-use pressure.
- B04 receives inventory, custody, storage, possession, access, burden, lawful loss, retrieval, and map/object custody pressure.
- B05 receives value, acquisition, requisition, market access, scarcity, upkeep, obligation, supply, fuel-as-value, support, permit, guide, bribe, or economic pressure.
- B06 receives project-centered interval work, crafting/salvage/repair/modification/upgrade, route-preparation project, map-making project, vehicle repair project, or material support pressure.
- B07 receives recovery, training, research, preparation, readiness, scouting-as-preparation, map study, route rehearsal, survey analysis, or non-object long-task pressure.
- D10-style owners receive actual world-state, territory, location, hazard-control, environmental-register, information-state, rumor, secrecy, and public-knowledge truth questions.
- D11-style owners receive protected hidden state, misinformation, secrecy presentation, safe player-facing presentation, and non-leaking revelation boundaries.
- D12-style owners receive active cadence, timing checkpoints, consequence timing, and structured active-procedure handoffs.
- D15-style owners receive faction, institution, domain, social/legal, territory-control, patrol, permit, and political route pressure.
- D16-style owners receive hazard construction, opposition construction, encounter composition, creature profile, contact opposition, and statblock/math pressure.
- D17-style owners receive supply/economy/requisition/upkeep/consumption/value-sink economic pressure beyond B05 procedure.
- D18-style owners receive long journeys, campaign-scale pacing, horizon/season/arc pressure, time skips, and structural journey consequences.
- C00/C-family owners receive conversion-record handoff pressure; B08 must not invent C-family fields.
- Runtime, canon, sourcebook, and live-play/training owners receive only flagged handoffs, not B08 authority.

## 23. Batch B to C00/C-family handoff rules

B08 may identify that a C00/C-family handoff is needed, but it must not invent C-family fields, final travel schema, final exploration schema, final map schema, final location schema, final route schema, final discovery schema, final hazard schema, final encounter schema, final world-state schema, or runtime state. The following block is lightweight, doctrine-facing, and not a runtime schema. `batch_b_to_c_handoff` is not a backend contract, not a database row, not an event object, not a map database row, not an encounter table, and not sourcebook text. `travel_exploration_routing_note` is doctrine-facing only: it is not runtime schema, not backend event, not command object, not C-family record, not travel state, not location state, not map state, not world-state truth, not hidden-state truth, not encounter generation, not final mechanics, not canon, and not player-facing rule text.

```yaml
batch_b_to_c_handoff:
  target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema
  schema_status: not_started | stub_index_only | minimum_unlock_draft | tested_minimum | stable_for_family | stable_cross_family | superseded | deprecated
  required_c00_base_fields: true
  source_evidence_refs_required: true
  construct_refs_required: true
  outcome_refs_required: true
  provenance_refs_required: true
  source_local_boundary_required_if_applicable: true
  rejected_donor_elements_required_if_applicable: true
  canon_eligibility_required: true
  review_routing_required: true
  unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists

travel_exploration_routing_note:
  intake_source: B01 | B02 | B03 | B04 | B05 | B06 | B07 | D_series_source_pack | source_local_donor | human_design_note | unknown
  intent: route_travel | area_exploration | site_approach | site_entry | pursuit | evasion | scouting | mapping | tracking | resource_search | survey_analysis | social_blending | platform_navigation | vehicle_travel | ship_travel | realm_crossing | threshold_crossing | hazardous_zone_crossing | unknown_space_exploration | source_local_exploration | mixed_exploration | unknown_intent
  posture_family: speed | safety | stealth | scouting | mapping | tracking | foraging_resource_search | concealment | diplomatic_approach | survey_analysis | ritual_sensing | sensor_sweep | platform_caution | resource_conservation | pursuit | evasion | combat_readiness | social_blending | source_local_posture | mixed | none
  route_state: known | partially_known | suspected | rumored | hidden | false | blocked | dangerous | contested | watched | restricted | unstable | unmapped | source_local | mixed | unknown
  known_state_category: confirmed_known | party_believes | rumored | suspected | mapped_but_unverified | false_or_compromised | hidden_from_party | protected_hidden | source_local | mixed | unknown
  interval_scale: momentary_approach | scene_segment | site_segment | district_leg | wilderness_leg | watch_period | platform_vector | stealth_segment | site_survey_pass | realm_crossing_stage | search_sweep | source_local_interval | unknown_interval
  context_profile: urban_social_dense | wilderness_open_region | site_dungeon_interior | space_vehicle_platform | dimensional_realm_threshold | hazardous_anomalous_zone | pursuit_evasion | tactical_terrain | horror_hidden_site | source_local_context | mixed_context | unknown_context
  navigation_trigger: none | no_roll_clear | route_uncertain | route_contested | route_hidden | route_distorted | route_false | route_unstable | pursuit_evasion | platform_vector | realm_threshold | source_local | owner_routed
  map_state_category: known | surveyed | partially_mapped | suspected | rumored | false | compromised | hidden | blocked | unreachable | source_local | none | unknown
  discovery_category: route_discovery | location_discovery | site_entry_discovery | hazard_discovery | resource_discovery | clue_or_lead_discovery | faction_presence_discovery | opposition_trace_discovery | environmental_condition_discovery | object_or_salvage_discovery | map_correction | false_route_exposure | hidden_boundary_hint | source_local_discovery | none | unknown
  discovery_confidence: confirmed | high_confidence | partial | ambiguous | rumored | suspected | false_or_compromised | protected_hidden | source_local | none | unknown
  pressure_family: resource_pressure | exposure_pressure | hazard_pressure | encounter_pressure | navigation_pressure | map_state_pressure | ambush_exposure | social_or_legal_pressure | faction_or_territory_pressure | object_or_platform_pressure | hidden_state_pressure | time_pressure | source_local_pressure | mixed | none
  progress_state: advanced | advanced_with_cost | advanced_with_discovery | advanced_with_exposure | delayed | misdirected | lost | blocked | hazard_triggered | encounter_triggered | site_entry_triggered | map_state_updated | pressure_escalated | transitioned | quarantined | escalated | no_delta_required
  protected_hidden_handling: not_applicable | protected_without_reveal | D10_truth_owner_routed | D11_presentation_owner_routed | quarantine | escalation | human_review
  owner_file_handoffs: []
  source_local_boundary: string | null
  rejected_donor_elements: []
```

Record-use rules:
- The block above is an audit aid and doctrine-facing routing note only.
- It may mark protected-hidden handling without exposing hidden truth.
- It must use `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` when C-family coverage is missing.
- It must not be consumed as runtime travel state, location state, map state, world-state database state, encounter generation, backend contract, command lifecycle object, or sourcebook text.

## 24. Missing-schema fallback and quarantine/escalation

If B08 handling needs schema coverage that C00/C-family files do not yet provide, B08 must not improvise fields or donor record formats. Use one of:
- `pending_schema` when the target family is likely but not available or mature enough;
- `quarantine` when a donor/source-local procedure carries unsupported assumptions or unsafe hidden-state behavior;
- `escalation` when doctrine ownership is unclear or conflicts across owners;
- `human_review` when conversion judgment, safety, canon, hidden-state, or source-local authority requires explicit review;
- `defer_until_schema_exists` when the content cannot be responsibly converted until later schema work exists.

Quarantine/escalation triggers include donor hex math, donor dungeon turns, donor random encounter tables, donor weather attrition, donor supply/fuel economy, donor automatic map reveal, donor boxed text as truth, donor passive hidden-state reveal, donor ship/realm travel law, donor watch-shift systems, donor random oracle world truth, unsupported geometry, unsupported runtime map state, protected-hidden leakage, and owner-file ambiguity.

## 25. Source-local donor travel/exploration/map/random-table handling

Source-local donor handling uses a functional mapping ladder:
1. Direct Astra mapping is allowed only when a donor element maps cleanly to B08 doctrine vocabulary without importing donor mechanics or assumptions.
2. Normalized Astra mapping may preserve the function while stripping donor timing, geometry, table, math, or hidden-reveal assumptions.
3. Source-local retention keeps the donor construct bounded to its source context and marks a source-local boundary.
4. Quarantine is required for unsupported or unsafe donor assumptions.
5. Escalation is required for cross-owner conflicts, hidden-state leakage, canon risk, schema gaps, or mechanics that would become Astra defaults if imported.

Rejected imports include donor hexcrawl as universal map law, donor dungeon turns as universal exploration cadence, donor watches as universal shift law, donor travel days as universal journey procedure, donor travel pace math, donor navigation DCs, donor scouting checks, donor random encounter tables, donor weather tables, donor hazard tables, donor supply attrition, donor fuel economy, donor realm metaphysics, donor ship travel law, donor boxed room text, donor site keys, donor random-table world truth, and donor encounter generation as runtime law.

## 26. Runtime boundary

B08 is not runtime authority. It must not define runtime travel state, runtime location state, runtime map state, runtime world-state database, runtime encounter generation, runtime hidden-information state, runtime entity/component/event/state schemas, persistent campaign state, command lifecycle implementation, context packet compiler, backend contracts, database rows, API contracts, telemetry, UI behavior, or live-play narration.

Runtime implementations may later validate or consume doctrine-derived concepts only through separate runtime specifications, tests, schema contracts, and safety review. Until then, B08 outputs are doctrine-facing notes, owner handoffs, quarantine/escalation markers, or C00/C-family handoff candidates.

## 27. Canon boundary

B08 does not create canon geography, canon routes, canon locations, canon maps, canon discoveries, canon hazards, canon encounters, canon factions, canon world truth, canon hidden truth, canon site keys, canon boxed text, canon realm rules, canon travel tables, canon random encounters, or canon sourcebook prose.

Any B08 result that appears canon-relevant must route through canon-eligibility review under C00/C-family controls and the appropriate world, information, presentation, faction, hazard, economy, campaign-time, or sourcebook owner. A party-facing map, rumor, discovery, or route note is not canon truth by itself.

## 28. Live-play/training boundary

B08 is not live-play narration behavior, player-facing rule text, GM script, boxed text, training simulator authority, tactical procedure, or runtime adjudication code. Live-play behavior must not consume B08 procedure as runtime authority without later runtime validation.

Training examples may use B08 only to illustrate doctrine-facing routing, owner handoffs, protected-hidden handling, quarantine, escalation, and C00/C-family handoff posture. They must not present B08 vocabulary as accepted player-facing lexicon or final mechanics.

## 29. Examples of good and bad B08 usage

Good usage examples:
- A party wants to cross a rumored marsh quickly. B08 classifies `route_travel`, posture `speed`, route state `rumored` and `dangerous`, known-state `rumored`, interval `wilderness_leg`, and pressure `navigation_pressure` plus `exposure_pressure`; it routes uncertainty to B02/D02-style owners and exposure/resource pressure to B05/B07/D07-style owners without defining travel pace, weather damage, or actual marsh truth.
- A scout circles a ruin before entry. B08 classifies `site_approach`, posture `scouting`, context `site_dungeon_interior`, and possible `ambush_exposure`; it routes the declared scouting method through B02, tool use to B03, map-state updates to D10/D11-style owners, and possible encounter pressure to B01/D16-style owners without revealing hidden occupants.
- A ship follows a damaged beacon line. B08 classifies `ship_travel` and `platform_navigation`, route state `partially_known` and `unstable`, posture `platform_caution`, and pressure `object_or_platform_pressure`; it routes ship/platform state to B03, support/fuel-as-value pressure to B05/D17-style owners, and navigation uncertainty to B02/D02-style owners without defining fuel economy or ship travel law.
- A research-prepared expedition maps an anomalous threshold. B08 routes preparation/readiness back to B07, map-state handling to section 15, environmental PCR pressure to D10/D11-style owners, and corruption/instability pressure to D07-style owners without exposing hidden cosmic modifiers.
- A donor module says to roll on a random encounter table every dungeon turn. B08 identifies donor dungeon-turn/random-table pressure, strips it from Astra defaults, and either maps the function to `encounter_pressure`/`source_local_interval` or quarantines/escalates it.

Bad usage examples:
- Treating a day of travel as automatically elapsed with no intent, posture, route, known-state, pressure, owner handoff, or no-delta result. This violates the rule that travel is not automatic time passage.
- Revealing the true map because the party explored an area. This violates map-state, world-truth, and hidden-state boundaries.
- Calling for a navigation roll every time the party moves. This violates the rule that navigation is not always a roll.
- Giving a flat stealth bonus because the party chose a stealth posture. This collapses posture into a modifier.
- Treating an ambiguous clue as actual truth. This violates discovery-confidence and D10/D11 owner boundaries.
- Importing hex movement, dungeon turns, watches, travel days, random encounter tables, weather tables, supply attrition, or fuel economy as Astra defaults. This violates source-local donor quarantine.
- Deciding hazard statblocks, opposition numbers, surprise, or encounter sequencing inside B08. This violates D16 and B01/B02/D12 handoff boundaries.
- Using environmental PCR to tell players hidden Pneuma modifiers or protected cosmic truth. This violates protected-hidden handling.

## 30. Minimum tests or assertions

A B08 doctrine review must assert:
- B08 sits after B01-B07 and builds on them without rewriting them.
- Travel is not automatic time passage.
- Exploration is not automatic map reveal.
- Navigation is not always a roll.
- A route is not necessarily geometric.
- A map is not truth.
- Party-facing known-state is not actual world-state.
- A discovery is not automatically actual truth.
- Scouting is not hidden-truth revelation.
- Mapping is not canon creation.
- Site entry is not boxed-text reveal.
- A watch is not a universal shift system.
- Ambush exposure is not automatic surprise.
- Hazard pressure is not hazard construction.
- Encounter pressure is not encounter generation.
- Random encounters are not default Astra law.
- Environmental PCR may shape travel pressure but must not expose hidden Pneuma, hidden cosmic modifiers, hidden truth, or protected-hidden state.
- Posture is not a flat modifier.
- Route progress is not universal travel pace.
- Travel intervals are not universal travel turns, dungeon turns, watches, hex moves, jumps, phases, rounds, or travel days.
- B08 identifies resource/exposure pressure without defining resource loss, supply attrition, harm, fuel economy, weather damage, or exposure math.
- B08 routes active travel scenes to B01/B02/D12 without owning final active-scene cadence or sequencing.
- B08 routes truth and presentation to D10/D11-style owners without deciding actual world truth or presentation.
- B08 routes hazards/opposition/encounter construction to D16-style owners without building encounter math or opposition statblocks.
- B08 routes long journeys and campaign-scale time to D18-style owners without defining final campaign-scale journey pacing or time-skip procedure.
- Every meaningful event routes at least one delta to a recognized owner or explicitly produces no-delta/quarantine/escalation/transition.
- C00/C-family handoff language is present and does not invent C-family fields.
- Missing schema coverage produces `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists`.
- B08 examples and records are doctrine-facing only and not runtime state, sourcebook prose, canon entries, backend contracts, travel tables, encounter tables, map rows, or final mechanics.

## 31. Acceptance criteria

B08 is acceptable when:
- It defines focused procedure for travel, exploration, navigation, route posture, route/area declaration, known-state review, scouting, mapping, discovery opportunities, travel/exploration intervals, site approach, site entry, watches, ambush exposure, travel pressure, resource/exposure triggers, hazard/encounter/contact trigger identification, and transition handoffs.
- It preserves B01-B07 boundaries and routes to those files rather than reopening scene cadence, action resolution, object use, inventory/custody, value flow, projects, recovery, training, research, or preparation procedure.
- It includes clear owned/not-owned lists covering final schemas, final map math, final travel math, final hazard/encounter construction, runtime state, canon, sourcebook, hidden-state, presentation, and source-local donor boundaries.
- It includes doctrine-facing vocabularies for intents, posture families, route states, known-state categories, interval scales, discovery categories, discovery confidence states, map-state categories, exploration context profiles, pressure families, and progress states.
- It includes protected-hidden route/map/world-state handling without revealing hidden truth.
- It includes navigation/orientation, posture pressure, environmental PCR, resource/exposure/support pressure, scouting, mapping, discovery, context-profile, site-entry, watch, ambush-exposure, hazard/encounter/contact, progress, and transition routing procedure.
- It includes the required lightweight C00/C-family handoff block and explicitly states that the block is not runtime schema.
- It uses `travel_exploration_routing_note` consistently for the B08-specific routing block.
- It quarantines donor travel/exploration/hexcrawl/dungeon-turn/random-encounter/scouting/mapping/ship-travel/realm-travel systems instead of importing them as Astra defaults.
- It includes good and bad usage examples, minimum assertions, and acceptance criteria.

## 32. Follow-up handoff to B09

B08 intentionally stops before any B09 topic. If later Batch B work needs to address social projects, faction operations, world-state operations, information operations, hazard/encounter construction, campaign-scale journey structures, runtime travel state, or another operational family, B08 should hand off only the unresolved travel/exploration/navigation/discovery pressure relevant to that future owner.

B08 does not require, define, create, or promote B09-B11. B08 must not create B09-B11, reserve their final subjects, or pre-authorize their mechanics. Follow-up notes should remain `transition_note`, `owner_routed`, `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` until the appropriate owner file exists.
