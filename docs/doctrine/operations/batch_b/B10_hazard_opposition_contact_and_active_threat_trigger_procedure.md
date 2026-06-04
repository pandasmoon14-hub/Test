# B10 Hazard, Opposition Contact, and Active Threat Trigger Procedure

## 1. Purpose and status

B10 is the tenth Batch B operational doctrine draft for Astra hazard contact, opposition contact, and active threat trigger handling. It sits after `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md`, `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md`, `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md`, `docs/doctrine/operations/batch_b/B04_inventory_storage_custody_and_burden_procedure.md`, `docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md`, `docs/doctrine/operations/batch_b/B06_project_crafting_salvage_repair_and_upgrade_procedure.md`, `docs/doctrine/operations/batch_b/B07_recovery_training_research_and_preparation_project_procedure.md`, `docs/doctrine/operations/batch_b/B08_travel_exploration_navigation_and_discovery_procedure.md`, and `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md` as upstream Batch B context and must build on them, not rewrite them.

B10 defines doctrine-facing procedure for recognizing hazard/opposition/contact/active-threat pressure after B01-B09 produce danger, resistance, contest, obstruction, pursuit, ambush, enforcement, hazard, security-system, hostile environment, rival, creature, social-antagonist, institutional proxy, platform enemy, corruption pressure, contamination pressure, or active threat pressure. B10 classifies threat contact, separates immediate danger from latent pressure, reviews visibility/posture/source/scale/scope, routes active-scene and action-window transitions, and sends deltas to owner files without defining final hazard construction, final opposition construction, final statblocks, combat math, encounter balance, runtime threat generation, hidden-truth presentation, or sourcebook bestiary prose.

Status posture:
- This file is Batch B operational-procedure draft material.
- This file is not current canon, not final mechanics, not runtime authority, not sourcebook prose, and not player-facing rule text.
- C00 remains the schema handoff control surface for Batch B to C-family routing.
- D00-D19 source packs are referenced only as draft source-pack/reference material, not final current doctrine authority, final mechanics, runtime authority, canon, live-play GM behavior, or sourcebook prose.
- B10 records, examples, and handoff blocks are doctrine-facing only; they are not runtime state, backend contracts, database contracts, event logs, command lifecycle artifacts, context packet formats, threat-state database rows, hazard-state rows, encounter-state rows, creature statblocks, trap statblocks, security-system backend rows, encounter tables, random tables, patrol generators, faction clocks, canon entries, or live-play scripts.
- B10 does not require, define, create, or promote B11. B10 does not require, define, create, or promote C01-C14.
- No registry status is promoted to current by B10.

Required reference boundaries preserved by B10:
- `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md` for upstream Batch B scene, activity, encounter, pressure, transition, and owner-handoff context; B10 may route active-scene transition trigger routing to B01 but must not reopen scene cadence.
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` for upstream Batch B action declaration, cost commitment, feasibility, and resolution-trigger context; B10 may route action resolution needs to B02 but must not define final action resolution.
- `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md` for upstream Batch B item, gear, equipment, object-system construct, and asset-use procedure; B10 may route object, trap, security system, unstable object, and platform questions to B03/D09-style owners but must not redefine object use.
- `docs/doctrine/operations/batch_b/B04_inventory_storage_custody_and_burden_procedure.md` for upstream Batch B inventory, storage, custody, access, burden, lawful loss, and recovery procedure; B10 may route custody/access/loss pressure but must not redefine inventory or custody.
- `docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md` for upstream Batch B acquisition, reward, requisition, value flow, market access, scarcity, upkeep, and value-sink procedure; B10 may route economy/reward/requisition fallout but must not define value math.
- `docs/doctrine/operations/batch_b/B06_project_crafting_salvage_repair_and_upgrade_procedure.md` for upstream Batch B project-centered interval work, crafting, salvage, repair, modification, upgrade, requirements, progress, complications, and project outputs; B10 may route containment, repair, salvage, or mitigation projects but must not redefine projects.
- `docs/doctrine/operations/batch_b/B07_recovery_training_research_and_preparation_project_procedure.md` for upstream Batch B recovery, training, research, preparation, readiness, proof routing, desired-outcome routing, and non-object project outputs; B10 may route recovery, research, preparation, proof, or readiness consequences but must not define recovery/training/research.
- `docs/doctrine/operations/batch_b/B08_travel_exploration_navigation_and_discovery_procedure.md` for upstream Batch B travel, exploration, navigation, discovery, scouting, mapping, site entry, watches, ambush exposure, travel pressure, and transition handoffs; B10 may route travel/site-entry discovered hazards, pursuit, route danger, and ambush exposure but must not define travel/exploration procedure.
- `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md` for upstream Batch B social contact, faction contact, institutional interaction, standing, obligations, claims, authority, permits, licenses, law/social pressure, negotiation routing, and institutional operation handoffs; B10 may route social antagonist, faction enforcement, legal enforcement, and institutional proxy threats but must not define faction operation or social mechanics.
- `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` for shared Batch C base fields, `pending_schema`, source-local boundary, rejected donor element, canon eligibility, review routing, provenance, and missing-schema fallback language.
- `docs/doctrine/native_design/d_series/source_packs/astra_d00_doctrine_pack_v0_1/D00-03_state_delta_commit_protocol.md` for draft state-delta commit protocol source material.
- `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-00_resolution_architecture_and_owner_boundaries.md` for draft resolution architecture and owner-boundary source material.
- `docs/doctrine/native_design/d_series/source_packs/astra_d05_doctrine_pack_v0_1/D05-03_relevance_handling_for_checks.md` for draft relevance handling for checks source material.
- `docs/doctrine/native_design/d_series/source_packs/astra_d07_doctrine_pack_v0_1/D07-02_corruption_contamination_and_instability.md` and `docs/doctrine/native_design/d_series/source_packs/astra_d07_doctrine_pack_v0_1/D07-07_recovery_treatment_stabilization_and_adaptation.md` for draft corruption, contamination, instability, harm, recovery, treatment, stabilization, and adaptation source material.
- `docs/doctrine/native_design/d_series/source_packs/astra_d08_doctrine_pack_v0_1/D08-00_layered_actor_state_architecture.md` and `docs/doctrine/native_design/d_series/source_packs/astra_d08_doctrine_pack_v0_1/D08-01_identity_continuity_personhood_and_agency.md` for draft actor substrate, personhood, identity, agency, control, AI, spirit, clone, companion, summon, and creature ontology source material.
- `docs/doctrine/native_design/d_series/source_packs/astra_d09_doctrine_pack_v0_1/D09-05_vehicles_platforms_ships_mechs_drones_and_external_bodies.md` for draft vehicle, platform, ship, mech, drone, hardpoint, and external-body source material.
- `docs/doctrine/native_design/d_series/source_packs/astra_d10_doctrine_pack_v0_1/D10-02_territory_location_hazard_control_environment_register.md` and `docs/doctrine/native_design/d_series/source_packs/astra_d10_doctrine_pack_v0_1/D10-07_information_state_public_knowledge_rumor_secrecy_records_register.md` for draft territory, location, hazard-control, environment, information-state, rumor, secrecy, and record source material.
- `docs/doctrine/native_design/d_series/source_packs/astra_d11_doctrine_pack_v0_1/D11-03_hidden_state_rumor_secrecy_misinformation_presentation.md` for draft hidden-state, rumor, secrecy, misinformation, and presentation source material.
- `docs/doctrine/native_design/d_series/source_packs/D12_time_action_cadence_encounter_and_turn_procedure_doctrine_pack/D12_doctrine_pack/D12-02_action_windows_initiative_sequencing_and_interruptions.md` and `docs/doctrine/native_design/d_series/source_packs/D12_time_action_cadence_encounter_and_turn_procedure_doctrine_pack/D12_doctrine_pack/D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md` for draft action windows, timing, sequencing, interruption, checkpoint, cost commitment, consequence timing, and handoff source material.
- `docs/doctrine/native_design/d_series/source_packs/D14_exploration_travel_navigation_and_discovery_doctrine_pack/D14_doctrine_pack/D14-05_travel_risk_resource_pressure_hazards_encounters_and_transition_handoffs.md` for draft travel risk, route pressure, hazards, encounters, and transition handoff source material.
- `docs/doctrine/native_design/d_series/source_packs/D15_faction_relationship_domain_and_institutional_operations_doctrine_pack/D15_doctrine_pack/D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md` for draft faction, relationship, domain, legal, enforcement, institutional, and social-antagonist owner-boundary source material.
- `docs/doctrine/native_design/d_series/source_packs/D16_opposition_creature_encounter_and_hazard_construction_doctrine_pack/D16_doctrine_pack/D16-00_opposition_creature_encounter_and_hazard_construction_owner_boundaries.md` for draft opposition, creature, encounter, hazard, patrol, lair, boss, swarm, minion, horde, trap, and construction owner-boundary source material.
- `docs/doctrine/native_design/d_series/source_packs/D17_economy_acquisition_inventory_reward_and_requisition_doctrine_pack/D17_doctrine_pack/D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md` for draft requisition, upkeep, consumption, value-sink, scarcity, and economic-pressure source material.
- `docs/doctrine/native_design/d_series/source_packs/D18_structural_time_campaign_continuity_arc_season_and_horizon_doctrine_pack/D18_doctrine_pack/D18-00_structural_time_campaign_continuity_arc_season_and_horizon_owner_boundaries.md` for draft campaign continuity, arc, season, recurring threat, horizon, long-horizon escalation, and structural-time source material.
- `docs/doctrine/native_design/d_series/source_packs/D19_cross_pack_integration_conflict_audit_and_conversion_readiness_capstone_pack/D19_capstone_doctrine_pack/D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md` for draft record-shape registry, conflict audit, conversion readiness, and schema handoff control source material.

## 2. Owner layer

B10 belongs to Batch B operational doctrine. It routes procedure between upstream B01-B09 operational procedure, C00 schema handoff control, future C-family schema families, source-local donor quarantine, and later hazard, opposition, encounter, actor, object/platform, travel, faction, information, hidden-state presentation, economy, campaign-horizon, runtime, canon, and training owners.

B10 may identify active threat pressure, but it must not perform the owner work of final hazards, statblocks, encounter balance, creature construction, threat generation, patrol systems, random encounter tables, harm math, action economy, initiative, surprise, morale, runtime threat state, or sourcebook bestiary prose. When B10 cannot identify a valid owner or schema family, it must mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` rather than inventing schema or mechanics.

## 3. What B10 owns

B10 owns doctrine-level operational procedure for:
- hazard/opposition/contact/active-threat intake after B01-B09 produce danger, resistance, contest, obstruction, pursuit, ambush, enforcement, hazard, security-system, hostile environment, rival, creature, social-antagonist, institutional proxy, platform enemy, corruption pressure, or active threat pressure;
- threat-contact classification;
- hazard-contact classification;
- opposition-contact classification;
- active-threat trigger identification;
- immediate danger vs latent pressure separation;
- known, suspected, hidden, protected-hidden, source-local, and false-threat boundary handling;
- threat posture review: passive, warning, watchful, stalking, pursuing, blocking, attacking, negotiating-against, enforcing, contaminating, escalating, retreating, source-local;
- threat source classification: environmental, creature, rival, social antagonist, security system, institutional proxy, platform enemy, corruption/contamination, object/system, terrain, information hazard, legal/enforcement, faction/institution, source-local;
- threat scale and engagement-scope routing as procedure, not math;
- hazard/opposition escalation to B01 focused scene, B02 action resolution, D12 action windows, or D16-style construction owners when appropriate;
- active-scene transition trigger routing;
- encounter-trigger routing without encounter construction;
- ambush, pursuit, patrol, enforcement, security response, alarm, containment breach, hostile terrain, unstable object/platform, contamination, corruption, hidden hazard, and environmental pressure trigger routing;
- threat-reveal and hidden-state presentation handoff to D10/D11-style owners without revealing hidden truth;
- harm/corruption/recovery handoff to D07-style owners without defining harm math;
- actor/personhood/substrate handoff to D08-style owners without deciding creature ontology or NPC personhood;
- object/platform/security-system handoff to B03/D09-style owners without defining object stats or platform mechanics;
- social/faction/enforcement handoff to B09/D15-style owners without defining faction operation or social mechanics;
- travel/site-entry/hazard handoff to B08/D14-style owners when threat is discovered through exploration/travel;
- campaign-horizon threat handoff to D18-style owners without defining long-horizon threat pacing;
- B10-to-C00/C-family handoff references when hazard/opposition/threat handling produces conversion records;
- source-local donor monster, trap, hazard, wandering monster, random encounter, patrol, reaction, morale, lair, legendary, boss, swarm, minion, horde, vehicle enemy, security system, faction enemy, heat/wanted, and active-threat systems quarantine and escalation rules;
- examples of good and bad B10 usage; and
- minimum acceptance criteria for B10.

## 4. What B10 must not own

B10 must not define, create, require, or promote:
- final hazard schema, final opposition schema, final creature schema, final encounter schema, final threat schema, final statblock schema, final actor schema, final object schema, final world-state schema, C-family schema fields, or C01-C14 schema contents;
- final hazard construction, final opposition construction, final creature construction, final encounter construction, final statblocks, final creature stats, final hazard stats, final trap stats, final security-system stats, final patrol generation, final wandering monster procedure, final random encounter tables, final encounter balance math, final encounter budgets, final CR/level/tier equivalence, final HP/AC/defense/attack/damage/save math, final action economy, final initiative rules, final surprise rules, final ambush rules, final morale rules, final reaction rolls, final boss/elite/minion/swarm/horde rules, final lair/legendary/action rules, or final resistance/vulnerability/immunity math;
- final harm, injury, corruption, contamination, instability, or recovery mechanics; final NPC motivation/personhood; final creature ontology; final security-system backend; final platform/vehicle/mech/starship combat rules; final faction enforcement/war/army/raid rules; final social-antagonist mechanics; final hidden-state reveal rules; final presentation/narration behavior; final sourcebook bestiary prose; final encounter-site key; accepted lexicon terms; final canon promotion; or sourcebook prose;
- runtime threat state, runtime encounter state, runtime hazard state, runtime opposition generation, runtime creature generation, runtime patrol generation, runtime alarm/security backend, runtime entity/component/event/state schemas, persistent campaign state, command lifecycle implementation, context packet compiler, hidden-information runtime state, runtime state/event/command lifecycle ownership, or live-play narration behavior;
- donor monster/trap/hazard/encounter/security/threat systems as Astra defaults.

## 5. Non-collapse rule

B10 preserves these non-collapse rules:
- A hazard is not automatically an encounter.
- Opposition is not automatically combat.
- A creature is not automatically a statblock.
- A threat is not automatically a roll.
- A warning is not automatically truth.
- A signal is not hidden-state reveal.
- A hidden threat is not player-facing truth.
- A false threat can still create real pressure.
- Ambush exposure is not automatic surprise.
- Pursuit is not automatic combat.
- A patrol is not a random encounter table.
- A security system is not a creature by default.
- A faction enforcement response is not automatically a faction clock.
- A social antagonist is not automatically a social-combat subsystem.
- A platform enemy is not automatically vehicle-combat rules.
- A corruption or contamination threat is not automatically moral evil or free power.
- Active threat trigger identification is not threat construction.
- Encounter pressure is not encounter construction.
- Hazard pressure is not hazard construction.
- Opposition contact is not final opposition profile.

## 6. Hazard contact, opposition contact, active threat, trigger, posture, and threat-pressure definitions

B10 definitions are doctrine vocabulary, not accepted lexicon terms and not final mechanics.

- Hazard contact: operational contact with an environmental, terrain, object/system, trap, contamination, corruption, information, platform, or source-local condition that can create meaningful pressure. Hazard contact is not final hazard construction.
- Opposition contact: operational contact with a creature, rival, social antagonist, institutional proxy, patrol, security response, faction enforcement, legal enforcement, vehicle enemy, swarm, boss_or_elite, minion_or_horde, or source-local opponent. Opposition contact is not final opposition profile and is not automatically combat.
- Active threat: a contacted or signaled pressure where immediate harm, timing, opposition response, location compromise, route blockage, alarm, pursuit, enforcement, contamination, corruption, or another meaningful consequence can matter now. Active threat trigger identification is not threat construction.
- Trigger: a condition that routes attention to an owner, transition, no-delta result, quarantine, escalation, `human_review`, or `defer_until_schema_exists`; a threat trigger is not a roll.
- Posture: the current doctrine-facing stance of the pressure, such as passive, warning, watchful, stalking, pursuing, blocking, attacking, negotiating-against, enforcing, contaminating, escalating, retreating, contained, dormant, source-local, or unknown.
- Threat-pressure: danger, resistance, obstruction, exposure, risk, hidden-state pressure, resource pressure, enforcement pressure, campaign-horizon pressure, or source-local retained effect that may require routing.

## 7. Hazard/opposition/contact intake procedure

Hazard/opposition/contact intake begins only after B01-B09 produce danger, resistance, contest, obstruction, pursuit, ambush, enforcement, hazard, security-system, hostile environment, rival, creature, social-antagonist, institutional proxy, platform enemy, corruption pressure, or active threat pressure.

Procedure:
1. Name the incoming pressure source from the upstream file and preserve its upstream boundary.
2. Decide whether the intake is hazard contact, opposition contact, both, unknown contact, source-local threat contact, false threat contact, or no_delta_required.
3. Separate immediate danger from latent pressure before deciding active-scene or action-window routing.
4. Preserve known, suspected, hidden, protected-hidden, source-local, rumor claim, misinformation claim, and false-threat boundaries.
5. Identify at least one owner handoff, transition note, no-delta result, source-local retained effect, quarantine, escalation, `human_review`, or `defer_until_schema_exists`.

## 8. Threat-contact and hazard-contact classification

Threat-contact type vocabulary: `hazard_contact`, `opposition_contact`, `creature_contact`, `rival_contact`, `social_antagonist_contact`, `institutional_proxy_contact`, `faction_enforcement_contact`, `legal_enforcement_contact`, `patrol_contact`, `pursuit_contact`, `ambush_contact`, `security_system_contact`, `trap_contact`, `environmental_threat_contact`, `terrain_threat_contact`, `corruption_contact`, `contamination_contact`, `unstable_object_contact`, `platform_enemy_contact`, `vehicle_enemy_contact`, `swarm_contact`, `boss_or_elite_contact`, `minion_or_horde_contact`, `hidden_threat_contact`, `false_threat_contact`, `source_local_threat_contact`, `unknown_threat_contact`.

Hazard-contact classification separates environmental_threat_contact, terrain_threat_contact, trap_contact, security_system_contact, corruption_contact, contamination_contact, unstable_object_contact, platform-threat contact, hidden_threat_contact, false_threat_contact, source_local_threat_contact, and unknown_threat_contact from final hazard construction. Threat-contact classification separates opposition_contact, creature_contact, rival_contact, social_antagonist_contact, institutional_proxy_contact, faction_enforcement_contact, legal_enforcement_contact, patrol_contact, pursuit_contact, ambush_contact, platform_enemy_contact, vehicle_enemy_contact, swarm_contact, boss_or_elite_contact, and minion_or_horde_contact from final opposition construction, final creature schema, final statblocks, and final encounter construction.

## 9. Active-threat trigger identification

Active-threat trigger vocabulary: `immediate_harm_possible`, `meaningful_consequence_possible`, `opposition_response_possible`, `timing_matters`, `location_compromised`, `route_blocked`, `watch_failed_or_bypassed`, `ambush_exposure`, `pursuit_pressure`, `patrol_intercept`, `alarm_triggered`, `security_response`, `trap_triggered`, `hazard_surface`, `contamination_exposure`, `corruption_pressure`, `unstable_object_or_platform`, `enforcement_arrival`, `faction_response`, `social_antagonist_pressure`, `hidden_threat_signal`, `false_threat_pressure`, `resource_or_exposure_pressure`, `owner_file_gap`, `source_local_trigger`.

Trigger identification asks: is harm or consequence possible, does timing matter, has location or route changed, has a watch failed or been bypassed, is there pursuit/ambush/patrol/security/alarm/enforcement pressure, has a hazard surfaced, is contamination or corruption exposure present, did a platform/object become unstable, did a hidden signal or false threat create real pressure, or is there an owner-file gap. If yes, route; do not build the threat.

## 10. Immediate danger, latent pressure, hidden threat, protected-hidden threat, and false-threat handling

Threat visibility states: `visible`, `partially_visible`, `signaled`, `suspected`, `hidden`, `protected_hidden`, `false`, `rumor_claim`, `misinformation_claim`, `source_local_visibility`, `unknown_visibility`.

Handling rules:
- Immediate danger routes to B01 active scene, B02 resolution trigger, D12 action-window/timing owner, B08 travel/site-entry owner, B09 enforcement owner, D16-style construction owner, D07-style harm/corruption owner, or another recognized owner.
- Latent pressure remains warning_only, obstacle, avoidance, project_pressure, travel_pressure, faction_operation_pressure, campaign_horizon_pressure, no_delta_required, transition_note, or owner_routed as appropriate.
- Hidden threat and protected-hidden threat must not reveal hidden truth; route signals to D10/D11-style information and presentation owners.
- False threat can still create real pressure through resource_exposure, alarm_exposure, social_or_legal_exposure, route_blocked, or faction_enforcement_exposure; route the pressure without declaring falsehood as player-facing truth.
- Source-local threat retains donor-local behavior only under source-local quarantine until an owner accepts, rejects, or transforms it.

## 11. Threat source, posture, scale, and engagement-scope review

Threat-source families: `environmental`, `terrain`, `creature`, `rival`, `social_antagonist`, `institutional_proxy`, `faction_enforcement`, `legal_enforcement`, `security_system`, `object_or_platform`, `vehicle_or_ship`, `corruption_or_contamination`, `information_hazard`, `hidden_state`, `resource_pressure`, `territorial_pressure`, `campaign_horizon`, `source_local_source`, `unknown_source`.

Threat postures: `passive`, `warning`, `watchful`, `stalking`, `pursuing`, `blocking`, `attacking`, `negotiating_against`, `enforcing`, `contaminating`, `escalating`, `retreating`, `contained`, `dormant`, `source_local_posture`, `unknown_posture`.

Engagement scopes: `no_active_engagement`, `warning_only`, `obstacle`, `avoidance`, `pursuit`, `containment`, `negotiation_against`, `active_scene`, `structured_encounter`, `project_pressure`, `travel_pressure`, `faction_operation_pressure`, `campaign_horizon_pressure`, `source_local_scope`, `unknown_scope`.

Threat scale review is procedural, not math: decide whether the pressure is personal, group, site, route, platform, institution, territory, region, campaign_horizon, source-local, or unknown; then route to the owner that can construct or preserve the scale. B10 does not define encounter budgets, CR/level/tier equivalence, HP/AC/defense/attack/damage/save math, or balance math.

## 12. Ambush, pursuit, patrol, enforcement, security response, and alarm trigger routing

Ambush exposure routes to B08/D14-style travel/site-entry or scouting owners and to D12 only if timing or action windows matter; ambush exposure is not automatic surprise and B10 does not define final ambush rules. Pursuit pressure routes to B01 for active scene transition, B08/D14 for travel pressure, D18 for recurring pursuit, or D16 for construction if opposition needs construction; pursuit is not automatic combat. Patrol contact routes owner review and is not a random encounter table, final patrol generation, wandering monster procedure, or runtime patrol generation.

Enforcement arrival, faction response, legal enforcement contact, and institutional proxy pressure route to B09/D15-style owners; B10 does not define faction enforcement/war/army/raid rules or faction clocks. Security response, alarm_triggered, security_system_contact, and trap_triggered route to B03/D09-style object/platform/security owners, D16-style construction owners, D12 timing owners, or B01 active scene owners without defining security-system backend, alarm/security backend, trap stats, or action-window implementation.

## 13. Environmental, terrain, contamination, corruption, unstable-object, and platform-threat trigger routing

Environmental_threat_contact and terrain_threat_contact route to B08/D14 when discovered by travel, exploration, route danger, site entry, watches, scouting, mapping, or navigation; they route to D10-style environment/hazard records when conversion records are needed; they route to D16-style construction owners when final hazard construction is needed. Hazard pressure is not hazard construction.

Contamination_contact, corruption_contact, contamination_exposure, corruption_pressure, instability_exposure, and corruption_or_contamination source families route to D07-style owners for harm, corruption, contamination, instability, recovery, treatment, stabilization, and adaptation consequences. B10 does not define harm, injury, corruption, contamination, instability, or recovery mechanics.

Unstable_object_contact, object_or_platform failure, unstable_object_or_platform, platform_enemy_contact, vehicle_enemy_contact, vehicle_or_ship source family, security system pressure, and hardpoint/platform questions route to B03/D09-style owners. B10 does not define object stats, final object schema, platform mechanics, vehicle/mech/starship combat rules, or security-system backend.

## 14. Creature, rival, social-antagonist, institutional-proxy, and faction/enforcement threat routing

Creature_contact routes to D08-style actor/personhood/substrate owners when identity, personhood, agency, companion, summon, AI, spirit, clone, or creature ontology is in question, and to D16-style owners when opposition/creature construction is needed; a creature is not automatically a statblock. Rival_contact, social_antagonist_contact, institutional_proxy_contact, faction_enforcement_contact, legal_enforcement_contact, and enforcement_arrival route to B09/D15-style owners when standing, authority, legal pressure, institutional response, social antagonist mechanics, sanctions, patrol authority, or social consequences dominate.

Swarm_contact, boss_or_elite_contact, minion_or_horde_contact, lair, legendary, morale, reaction, raid, army, faction enemy, heat/wanted, source-local patrol, and donor encounter labels are quarantined as source-local until D16-style or B09/D15-style owners accept or transform them. B10 does not define boss/elite/minion/swarm/horde rules, lair/legendary/action rules, morale rules, reaction rolls, or final sourcebook bestiary prose.

## 15. Hidden-state, rumor, signal, warning, and safe-presentation handoff rules

Warning, signal, rumor claim, misinformation claim, hidden threat, protected-hidden threat, source-local visibility, and information hazard handling route to D10/D11-style information and presentation owners. A warning is not automatically truth, a signal is not hidden-state reveal, a hidden threat is not player-facing truth, and a rumor claim or misinformation claim must not become canon or hidden-state reveal by B10 wording.

Safe-presentation handoff means B10 may say that something is visible, partially_visible, signaled, suspected, hidden, protected_hidden, false, rumor_claim, misinformation_claim, source_local_visibility, or unknown_visibility for owner routing. B10 must not define final hidden-state reveal rules, final presentation/narration behavior, hidden-information runtime state, or live-play narration behavior.

## 16. Active-scene, action-window, resolution, and encounter-trigger transition routing

Active-scene transition trigger routing occurs when immediate danger, timing, opposition response, route_blocked, location_compromised, pursuit_pressure, patrol_intercept, alarm_triggered, security_response, enforcement_arrival, hazard_surface, contamination_exposure, corruption_pressure, or unstable_object_or_platform requires focused attention under B01. B10 routes the transition but does not own scene cadence.

Action-window routing occurs when timing, interruption, sequencing, cost commitment, or consequence timing matters; route to D12 action windows and B02 action declaration/cost/resolution trigger owners. B10 does not define action economy, final initiative rules, final surprise rules, final action resolution, or live-play sequencing.

Encounter-trigger routing marks encounter pressure, encounter_triggered, structured_encounter, or opposition response pressure without encounter construction. Encounter pressure is not encounter construction, and B10 does not build final encounter schema, final encounter construction, encounter balance math, encounter budgets, or runtime encounter state.

## 17. Hazard/opposition construction handoff to D16-style owners

When threat intake identifies a need for final hazard construction, final opposition construction, final creature construction, final encounter construction, final statblocks, final creature stats, final hazard stats, final trap stats, final security-system stats, final patrol generation, final wandering monster procedure, final random encounter tables, encounter balance math, encounter budgets, CR/level/tier equivalence, HP/AC/defense/attack/damage/save math, final boss/elite/minion/swarm/horde rules, final lair/legendary/action rules, final resistance/vulnerability/immunity math, or final sourcebook bestiary prose, B10 must stop and route to D16-style owners or quarantine until a current owner exists.

B10 may produce `hazard_construction_routed` or `opposition_construction_routed`; it must not produce construction content.

## 18. Harm, actor, object/platform, social/faction, travel/site-entry, economy/reward, and campaign-horizon handoff rules

Handoff rules:
- Harm, injury, corruption, contamination, instability, recovery, treatment, stabilization, and adaptation consequences route to D07-style owners; B10 does not define harm/corruption/recovery mechanics.
- Actor substrate, personhood, companion identity, summon identity, control boundaries, AI, spirits, clones, agency, and creature ontology route to D08-style owners; B10 does not define final NPC motivation/personhood or creature ontology.
- Objects, vehicles, platforms, ships, mechs, drones, security systems, hardpoints, tools, weapons, armor, object-state questions, unstable objects, platform enemy pressure, and security-system contact route to B03/D09-style owners; B10 does not define final object/platform mechanics.
- Social antagonist, faction enforcement, legal threats, institutional proxies, sanctions, patrol authority, social consequences, faction response, legal enforcement, and enforcement arrival route to B09/D15-style owners; B10 does not define social mechanics or faction operations.
- Travel/site-entry discovered hazards, route danger, pursuit, watches, scouting, mapping, ambush exposure, hostile terrain, environmental pressure, and exploration pressure route to B08/D14-style owners; B10 does not define travel/exploration procedure.
- Economy/reward/requisition, resource_exposure, scarcity, upkeep, consumption, requisition, reward, cost, and value-sink fallout route to B05/D17-style owners; B10 does not define economy math.
- Recurring threats, long-horizon escalation, campaigns, seasons, arcs, active threat continuity, campaign_horizon_pressure, and campaign_horizon_exposure route to D18-style owners; B10 does not define final campaign-scale threat pacing.

## 19. Threat escalation, de-escalation, bypass, avoidance, containment, retreat, and fallout routing

Outcome states: `no_delta_required`, `threat_identified`, `threat_signaled`, `threat_misread`, `threat_avoided`, `threat_bypassed`, `threat_contained`, `threat_delayed`, `threat_escalated`, `threat_deescalated`, `active_scene_triggered`, `action_window_triggered`, `resolution_triggered`, `encounter_triggered`, `hazard_construction_routed`, `opposition_construction_routed`, `harm_consequence_routed`, `corruption_consequence_routed`, `actor_substrate_routed`, `object_platform_routed`, `social_faction_routed`, `travel_site_entry_routed`, `campaign_horizon_routed`, `owner_routed`, `transition_note`, `source_local_retained_effect`, `quarantined_unresolved_delta`, `owner_file_escalation`.

Escalation/de-escalation procedure:
1. If pressure escalates, route to active_scene_triggered, action_window_triggered, resolution_triggered, encounter_triggered, construction routed, harm/corruption routed, object_platform_routed, social_faction_routed, travel_site_entry_routed, campaign_horizon_routed, or owner_file_escalation.
2. If pressure de-escalates, route to threat_deescalated, threat_avoided, threat_bypassed, threat_contained, threat_delayed, retreating, contained, dormant, transition_note, or no_delta_required.
3. If bypass, avoidance, containment, retreat, or fallout creates resource, legal, social, travel, object, harm, hidden-state, or campaign pressure, route that fallout to the proper owner.

## 20. Hazard/opposition/contact state-delta routing

Every meaningful hazard/opposition/contact/active-threat event must route at least one delta to a recognized owner or explicitly produce `no_delta_required`, `transition_note`, `source_local_retained_effect`, `quarantined_unresolved_delta`, `owner_file_escalation`, quarantine, escalation, `human_review`, or `defer_until_schema_exists`. B10 uses D00-style state-delta commit protocol only as draft source-pack/reference material and does not define runtime state, event schema, command lifecycle, context packet, persistence, hazard backend, threat backend, encounter generator, creature generator, patrol generator, alarm/security backend, faction AI, or live-play GM behavior.

Risk/exposure families: `harm_exposure`, `corruption_exposure`, `contamination_exposure`, `instability_exposure`, `detection_exposure`, `ambush_exposure`, `pursuit_exposure`, `alarm_exposure`, `social_or_legal_exposure`, `resource_exposure`, `object_or_platform_failure`, `terrain_exposure`, `environmental_exposure`, `hidden_state_exposure`, `faction_enforcement_exposure`, `campaign_horizon_exposure`, `source_local_risk`, `owner_file_gap`.

## 21. Owner-file handoff rules

Owner-file handoff rules:
- Route scene/activity/encounter attention to B01; do not reopen scene cadence.
- Route action declaration, cost commitment, feasibility, and resolution trigger questions to B02; do not define action resolution.
- Route object, gear, equipment, and asset-use questions to B03; do not define final object schema.
- Route custody/access/loss/recovery of things to B04; do not define inventory/custody.
- Route acquisition/reward/requisition/value-flow pressure to B05/D17; do not define value math.
- Route containment, repair, salvage, mitigation, and modification projects to B06; do not define project procedure.
- Route recovery, training, research, preparation, readiness, proof, and desired-outcome pressure to B07; do not define recovery/training/research.
- Route travel, exploration, navigation, discovery, watches, ambush exposure, route pressure, and site entry to B08/D14; do not define travel/exploration.
- Route social antagonist, faction, institution, legal enforcement, authority, permit, license, and sanction pressure to B09/D15; do not define social/faction mechanics.
- Route schema records to C00/C-family control; do not invent fields.
- Route hidden-state presentation to D10/D11-style owners; do not reveal hidden truth.
- Route hazard/opposition/creature/encounter construction to D16-style owners; do not construct.
- Route campaign horizon to D18-style owners; do not set long-horizon pacing.

## 22. Batch B to C00/C-family handoff rules

Batch B procedure may identify that a C-family handoff is needed, but it must not invent C-family fields. C00 remains the schema handoff control surface. The following block is lightweight and doctrine-facing only. It must not be treated as a runtime schema.

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
```

B10-specific lightweight doctrine-facing note:

```yaml
hazard_opposition_threat_routing_note:
  threat_contact_type: hazard_contact | opposition_contact | creature_contact | rival_contact | social_antagonist_contact | institutional_proxy_contact | faction_enforcement_contact | legal_enforcement_contact | patrol_contact | pursuit_contact | ambush_contact | security_system_contact | trap_contact | environmental_threat_contact | terrain_threat_contact | corruption_contact | contamination_contact | unstable_object_contact | platform_enemy_contact | vehicle_enemy_contact | swarm_contact | boss_or_elite_contact | minion_or_horde_contact | hidden_threat_contact | false_threat_contact | source_local_threat_contact | unknown_threat_contact
  threat_source_family: environmental | terrain | creature | rival | social_antagonist | institutional_proxy | faction_enforcement | legal_enforcement | security_system | object_or_platform | vehicle_or_ship | corruption_or_contamination | information_hazard | hidden_state | resource_pressure | territorial_pressure | campaign_horizon | source_local_source | unknown_source
  threat_posture: passive | warning | watchful | stalking | pursuing | blocking | attacking | negotiating_against | enforcing | contaminating | escalating | retreating | contained | dormant | source_local_posture | unknown_posture
  active_threat_trigger: immediate_harm_possible | meaningful_consequence_possible | opposition_response_possible | timing_matters | location_compromised | route_blocked | watch_failed_or_bypassed | ambush_exposure | pursuit_pressure | patrol_intercept | alarm_triggered | security_response | trap_triggered | hazard_surface | contamination_exposure | corruption_pressure | unstable_object_or_platform | enforcement_arrival | faction_response | social_antagonist_pressure | hidden_threat_signal | false_threat_pressure | resource_or_exposure_pressure | owner_file_gap | source_local_trigger | none
  threat_visibility_state: visible | partially_visible | signaled | suspected | hidden | protected_hidden | false | rumor_claim | misinformation_claim | source_local_visibility | unknown_visibility
  engagement_scope: no_active_engagement | warning_only | obstacle | avoidance | pursuit | containment | negotiation_against | active_scene | structured_encounter | project_pressure | travel_pressure | faction_operation_pressure | campaign_horizon_pressure | source_local_scope | unknown_scope
  risk_exposure_families:
    - harm_exposure
    - corruption_exposure
    - contamination_exposure
    - instability_exposure
    - detection_exposure
    - ambush_exposure
    - pursuit_exposure
    - alarm_exposure
    - social_or_legal_exposure
    - resource_exposure
    - object_or_platform_failure
    - terrain_exposure
    - environmental_exposure
    - hidden_state_exposure
    - faction_enforcement_exposure
    - campaign_horizon_exposure
    - source_local_risk
    - owner_file_gap
  outcome_state: no_delta_required | threat_identified | threat_signaled | threat_misread | threat_avoided | threat_bypassed | threat_contained | threat_delayed | threat_escalated | threat_deescalated | active_scene_triggered | action_window_triggered | resolution_triggered | encounter_triggered | hazard_construction_routed | opposition_construction_routed | harm_consequence_routed | corruption_consequence_routed | actor_substrate_routed | object_platform_routed | social_faction_routed | travel_site_entry_routed | campaign_horizon_routed | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  hidden_state_handling: public | visible_signal | partial_signal | suspected | protected_hidden | hidden_not_revealed | rumor_claim | misinformation_claim | source_local | owner_routed | unknown
  owner_handoff_required: boolean
  owner_handoff_reason:
    - scene_or_activity_transition
    - action_cost_or_resolution
    - action_window_or_timing
    - hazard_or_opposition_construction
    - harm_or_recovery
    - corruption_or_contamination
    - actor_personhood_or_substrate
    - object_platform_or_security_system
    - information_truth_or_record
    - hidden_state_presentation
    - travel_site_entry_or_route
    - social_faction_or_enforcement
    - economy_reward_or_requisition
    - campaign_horizon_or_recurring_threat
    - source_local_review
    - schema_review
    - canon_review
    - runtime_review
    - human_review
  delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  note: string
```

`hazard_opposition_threat_routing_note` is doctrine-facing only. It is not a runtime schema, not a backend event, not a command object, not a C-family record, not a threat-state database row, not a hazard-state row, not an encounter-state row, not a creature statblock, not a trap statblock, not a security-system backend row, not an encounter table, not a random table, not a patrol generator, not a faction clock, not an action-window implementation, not final mechanics, not a database contract, not an event log, not a context packet format, not persistent campaign state, not canon, and not player-facing rule text.

## 23. Missing-schema fallback and quarantine/escalation

Missing schema coverage must produce `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` rather than improvised schema. If a contact cannot be represented without inventing C-family fields, final hazard schema, final opposition schema, final creature schema, final encounter schema, final threat schema, final actor schema, final object schema, final world-state schema, runtime entity/component/event/state schemas, or source-local defaults, B10 quarantines the unresolved delta and routes owner_file_escalation.

## 24. Source-local donor monster/trap/hazard/encounter/security/threat handling

Source-local donor monster, trap, hazard, wandering monster, random encounter, patrol, reaction, morale, lair, legendary, boss, swarm, minion, horde, vehicle enemy, security system, faction enemy, heat/wanted, and active-threat systems remain source-local donor material unless a current Astra owner transforms them. B10 rejects donor monster/trap/hazard/encounter/security/threat systems as Astra defaults and rejects donor patrol systems, random encounter tables, encounter generators, threat generators, security backend, faction clocks, reaction rolls, morale rules, lair rules, legendary actions, boss mechanics, swarm mechanics, minion mechanics, horde mechanics, vehicle-combat rules, and heat/wanted systems as direct imports.

Allowed results are `source_local_retained_effect`, quarantine, escalation, `human_review`, `defer_until_schema_exists`, owner_routed, construction_routed, or rejected donor elements documented for C00/C-family handoff if applicable.

## 25. Runtime boundary

B10 is not runtime authority. It does not define runtime threat state, runtime encounter state, runtime hazard state, runtime opposition generation, runtime creature generation, runtime patrol generation, runtime alarm/security backend, runtime entity/component/event/state schemas, runtime state/event/command lifecycle ownership, persistent campaign state, command lifecycle implementation, context packet compiler, hidden-information runtime state, backend events, database contracts, context packet formats, threat backend, hazard backend, encounter generator, creature generator, patrol generator, alarm/security backend, faction AI, or live-play GM behavior.

## 26. Canon boundary

B10 does not create canon, accepted lexicon terms, sourcebook prose, sourcebook bestiary prose, final creature profiles, final hazard profiles, final opposition profiles, encounter-site keys, player-facing rule text, public truth, rumor truth, hidden truth, hidden-state reveal, final presentation/narration behavior, or final canon promotion. B10 examples are doctrine-facing only and cannot promote source-local donor content.

## 27. Live-play/training boundary

Live-play behavior must not consume B10 procedure as runtime authority without later runtime validation. B10 does not prescribe GM narration, player-facing reveal timing, hidden truth presentation, live-play sequencing, initiative, surprise, action windows, action economy, checks, rolls, morale, reaction behavior, encounter balance, patrol generation, security responses, or combat math. Training material may cite B10 only as a draft doctrine boundary and owner-routing pattern.

## 28. Examples of good and bad B10 usage

Good usage:
- Good: “A failed watch creates `ambush_exposure`; B10 routes to B08/D14 for travel pressure and to D12 only if timing matters. Ambush exposure is not automatic surprise.”
- Good: “A sealed chamber emits a warning signal; B10 marks `hidden_threat_signal` and routes to D10/D11 for safe presentation without revealing hidden truth.”
- Good: “A security turret activates; B10 classifies `security_system_contact`, routes object/platform questions to B03/D09 and construction to D16 if needed, and does not treat the system as a creature.”
- Good: “A faction patrol blocks a route; B10 marks `patrol_contact`, `route_blocked`, `faction_enforcement_contact`, routes to B08 and B09/D15, and does not create a random encounter table.”
- Good: “A contamination exposure creates possible harm; B10 routes D07-style consequences and does not define harm math.”

Bad usage:
- Bad: “B10 assigns HP, AC, damage, saves, CR, encounter budget, initiative, surprise, morale, and reaction rolls.”
- Bad: “B10 reveals the protected-hidden assassin because a warning signal exists.”
- Bad: “B10 imports a donor wandering monster table, faction clock, heat/wanted track, trap statblock, lair action, legendary action, boss rule, swarm rule, minion rule, horde rule, security backend, or random encounter table as an Astra default.”
- Bad: “B10 defines runtime threat state, runtime hazard state, runtime encounter state, a command object, backend event, entity/component schema, database row, or context packet format.”
- Bad: “B10 promotes B11, C01-C14, D-series material, sourcebook prose, canon, or final mechanics.”

## 29. Minimum tests or assertions

Minimum tests or assertions for B10:
- The B10 file exists at `docs/doctrine/operations/batch_b/B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md`.
- Required sections 1-31 are present.
- B10 declares ownership and non-ownership.
- B10 references B01, B02, B03, B04, B05, B06, B07, B08, and B09 as upstream Batch B context.
- B10 includes C00 handoff language, `batch_b_to_c_handoff`, `hazard_opposition_threat_routing_note`, and doctrine-facing-only boundaries.
- B10 includes threat-contact types, threat-source families, threat postures, active-threat triggers, threat visibility states, engagement scopes, outcome states, and risk/exposure families.
- B10 separates hazard, opposition, contact, active threat, threat trigger, active scene, encounter pressure, encounter construction, hazard pressure, hazard construction, opposition contact, opposition profile, creature, statblock, trap, security system, platform enemy, social antagonist, faction enforcement, hidden state, false threat, rumor claim, runtime state, and canon.
- B10 includes intake, classification, trigger identification, immediate danger/latent pressure/hidden/protected-hidden/false-threat handling, source/posture/scale/scope review, trigger routing, owner handoffs, state-delta routing, source-local quarantine, `human_review`, and `defer_until_schema_exists`.

## 30. Acceptance criteria

B10 is acceptable when it remains after B01-B09, preserves their boundaries, owns only hazard/opposition/contact/active-threat intake and routing, includes the C00 and B10-specific doctrine-facing blocks, rejects final schema/mechanics/runtime/canon/sourcebook ownership, references D00/D02/D05/D07/D08/D09/D10/D11/D12/D14/D15/D16/D17/D18/D19 only as draft source-pack/reference material, and passes the focused B10 test plus the Batch B/C00/registry regression tests without promoting any registry status to current.

## 31. Follow-up handoff to B11

B10 does not require, define, create, or promote B11. This section is only a forward-handoff placeholder stating that any later B11 must preserve B10 boundaries, must not treat B10 as final mechanics or runtime authority, and must not retroactively turn B10 threat routing notes into C-family schema fields, runtime state, encounter generators, hazard generators, sourcebook prose, or canon.
