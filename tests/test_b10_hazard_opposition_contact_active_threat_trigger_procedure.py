from tests.helpers import ROOT, read_utf8

B10_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "operations"
    / "batch_b"
    / "B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md"
)

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B10 owns",
    "## 4. What B10 must not own",
    "## 5. Non-collapse rule",
    "## 6. Hazard contact, opposition contact, active threat, trigger, posture, and threat-pressure definitions",
    "## 7. Hazard/opposition/contact intake procedure",
    "## 8. Threat-contact and hazard-contact classification",
    "## 9. Active-threat trigger identification",
    "## 10. Immediate danger, latent pressure, hidden threat, protected-hidden threat, and false-threat handling",
    "## 11. Threat source, posture, scale, and engagement-scope review",
    "## 12. Ambush, pursuit, patrol, enforcement, security response, and alarm trigger routing",
    "## 13. Environmental, terrain, contamination, corruption, unstable-object, and platform-threat trigger routing",
    "## 14. Creature, rival, social-antagonist, institutional-proxy, and faction/enforcement threat routing",
    "## 15. Hidden-state, rumor, signal, warning, and safe-presentation handoff rules",
    "## 16. Active-scene, action-window, resolution, and encounter-trigger transition routing",
    "## 17. Hazard/opposition construction handoff to D16-style owners",
    "## 18. Harm, actor, object/platform, social/faction, travel/site-entry, economy/reward, and campaign-horizon handoff rules",
    "## 19. Threat escalation, de-escalation, bypass, avoidance, containment, retreat, and fallout routing",
    "## 20. Hazard/opposition/contact state-delta routing",
    "## 21. Owner-file handoff rules",
    "## 22. Batch B to C00/C-family handoff rules",
    "## 23. Missing-schema fallback and quarantine/escalation",
    "## 24. Source-local donor monster/trap/hazard/encounter/security/threat handling",
    "## 25. Runtime boundary",
    "## 26. Canon boundary",
    "## 27. Live-play/training boundary",
    "## 28. Examples of good and bad B10 usage",
    "## 29. Minimum tests or assertions",
    "## 30. Acceptance criteria",
    "## 31. Follow-up handoff to B11",
]


def b10_text() -> str:
    return read_utf8(B10_PATH)


def test_b10_file_exists_at_expected_path() -> None:
    assert B10_PATH.exists()
    assert B10_PATH.is_file()


def test_b10_required_sections_are_present() -> None:
    text = b10_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b10_declares_ownership_and_non_ownership() -> None:
    lowered = b10_text().lower()
    for phrase in [
        "hazard/opposition/contact/active-threat intake after b01-b09 produce danger",
        "threat-contact classification",
        "hazard-contact classification",
        "opposition-contact classification",
        "active-threat trigger identification",
        "immediate danger vs latent pressure separation",
        "known, suspected, hidden, protected-hidden, source-local, and false-threat boundary handling",
        "threat scale and engagement-scope routing as procedure, not math",
        "encounter-trigger routing without encounter construction",
        "hazard/opposition/contact state-delta routing",
    ]:
        assert phrase in lowered

    for phrase in [
        "final hazard schema",
        "final opposition schema",
        "final creature schema",
        "final encounter schema",
        "final threat schema",
        "final statblock schema",
        "final actor schema",
        "final object schema",
        "final world-state schema",
        "c-family schema fields",
        "c01-c14 schema contents",
    ]:
        assert phrase in lowered


def test_b10_references_b01_through_b09_as_upstream_batch_b_context() -> None:
    lowered = b10_text().lower()
    for marker in [
        "b01_scene_encounter_and_activity_procedure.md",
        "b02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md",
        "b03_item_gear_equipment_and_asset_use_procedure.md",
        "b04_inventory_storage_custody_and_burden_procedure.md",
        "b05_acquisition_reward_requisition_and_value_flow_procedure.md",
        "b06_project_crafting_salvage_repair_and_upgrade_procedure.md",
        "b07_recovery_training_research_and_preparation_project_procedure.md",
        "b08_travel_exploration_navigation_and_discovery_procedure.md",
        "b09_social_faction_contact_and_institutional_interaction_procedure.md",
        "upstream batch b context",
        "must build on them, not rewrite them",
    ]:
        assert marker in lowered


def test_b10_includes_c00_handoff_language_and_blocks() -> None:
    text = b10_text()
    for marker in [
        "C00 remains the schema handoff control surface",
        "batch_b_to_c_handoff",
        "target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema",
        "unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists",
        "The following block is lightweight and doctrine-facing only. It must not be treated as a runtime schema.",
        "hazard_opposition_threat_routing_note",
        "`hazard_opposition_threat_routing_note` is doctrine-facing only",
        "not a runtime schema",
        "not a backend event",
        "not a command object",
        "not a C-family record",
        "not a threat-state database row",
        "not a hazard-state row",
        "not an encounter-state row",
        "not a creature statblock",
        "not a trap statblock",
        "not a security-system backend row",
        "not an encounter table",
        "not a random table",
        "not a patrol generator",
        "not a faction clock",
        "not an action-window implementation",
        "not final mechanics",
        "not a database contract",
        "not an event log",
        "not a context packet format",
        "not persistent campaign state",
        "not canon",
        "not player-facing rule text",
    ]:
        assert marker in text


def test_b10_includes_vocabularies() -> None:
    text = b10_text()
    for marker in [
        "hazard_contact", "opposition_contact", "creature_contact", "rival_contact",
        "social_antagonist_contact", "institutional_proxy_contact", "faction_enforcement_contact",
        "legal_enforcement_contact", "patrol_contact", "pursuit_contact", "ambush_contact",
        "security_system_contact", "trap_contact", "environmental_threat_contact",
        "terrain_threat_contact", "corruption_contact", "contamination_contact",
        "unstable_object_contact", "platform_enemy_contact", "vehicle_enemy_contact",
        "swarm_contact", "boss_or_elite_contact", "minion_or_horde_contact",
        "hidden_threat_contact", "false_threat_contact", "source_local_threat_contact",
        "unknown_threat_contact", "environmental", "terrain", "creature", "rival",
        "social_antagonist", "institutional_proxy", "faction_enforcement",
        "legal_enforcement", "security_system", "object_or_platform", "vehicle_or_ship",
        "corruption_or_contamination", "information_hazard", "hidden_state",
        "resource_pressure", "territorial_pressure", "campaign_horizon",
        "source_local_source", "unknown_source", "passive", "warning", "watchful",
        "stalking", "pursuing", "blocking", "attacking", "negotiating_against",
        "enforcing", "contaminating", "escalating", "retreating", "contained",
        "dormant", "source_local_posture", "unknown_posture",
        "immediate_harm_possible", "meaningful_consequence_possible",
        "opposition_response_possible", "timing_matters", "location_compromised",
        "route_blocked", "watch_failed_or_bypassed", "ambush_exposure",
        "pursuit_pressure", "patrol_intercept", "alarm_triggered", "security_response",
        "trap_triggered", "hazard_surface", "contamination_exposure",
        "corruption_pressure", "unstable_object_or_platform", "enforcement_arrival",
        "faction_response", "social_antagonist_pressure", "hidden_threat_signal",
        "false_threat_pressure", "resource_or_exposure_pressure", "owner_file_gap",
        "source_local_trigger", "visible", "partially_visible", "signaled", "suspected",
        "protected_hidden", "rumor_claim", "misinformation_claim", "source_local_visibility",
        "unknown_visibility", "no_active_engagement", "warning_only", "obstacle",
        "avoidance", "containment", "active_scene", "structured_encounter",
        "project_pressure", "travel_pressure", "faction_operation_pressure",
        "campaign_horizon_pressure", "source_local_scope", "unknown_scope",
        "no_delta_required", "threat_identified", "threat_signaled", "threat_misread",
        "threat_avoided", "threat_bypassed", "threat_contained", "threat_delayed",
        "threat_escalated", "threat_deescalated", "active_scene_triggered",
        "action_window_triggered", "resolution_triggered", "encounter_triggered",
        "hazard_construction_routed", "opposition_construction_routed",
        "harm_consequence_routed", "corruption_consequence_routed",
        "actor_substrate_routed", "object_platform_routed", "social_faction_routed",
        "travel_site_entry_routed", "campaign_horizon_routed", "owner_routed",
        "transition_note", "source_local_retained_effect", "quarantined_unresolved_delta",
        "owner_file_escalation", "harm_exposure", "instability_exposure",
        "detection_exposure", "alarm_exposure", "social_or_legal_exposure",
        "resource_exposure", "object_or_platform_failure", "terrain_exposure",
        "environmental_exposure", "hidden_state_exposure", "faction_enforcement_exposure",
        "campaign_horizon_exposure", "source_local_risk",
    ]:
        assert marker in text


def test_b10_separates_core_non_collapse_concepts() -> None:
    text = b10_text()
    for marker in [
        "A hazard is not automatically an encounter.",
        "Opposition is not automatically combat.",
        "A creature is not automatically a statblock.",
        "A threat is not automatically a roll.",
        "A warning is not automatically truth.",
        "A signal is not hidden-state reveal.",
        "A hidden threat is not player-facing truth.",
        "A false threat can still create real pressure.",
        "Ambush exposure is not automatic surprise.",
        "Pursuit is not automatic combat.",
        "A patrol is not a random encounter table.",
        "A security system is not a creature by default.",
        "A faction enforcement response is not automatically a faction clock.",
        "A social antagonist is not automatically a social-combat subsystem.",
        "A platform enemy is not automatically vehicle-combat rules.",
        "A corruption or contamination threat is not automatically moral evil or free power.",
        "Active threat trigger identification is not threat construction.",
        "Encounter pressure is not encounter construction.",
        "Hazard pressure is not hazard construction.",
        "Opposition contact is not final opposition profile.",
        "false threat can still create real pressure",
        "rumor claim",
        "runtime state",
        "canon",
    ]:
        assert marker in text


def test_b10_includes_required_procedure_coverage() -> None:
    lowered = b10_text().lower()
    for marker in [
        "hazard/opposition/contact intake procedure",
        "threat-contact classification",
        "hazard-contact classification",
        "active-threat trigger identification",
        "immediate danger",
        "latent pressure",
        "hidden threat",
        "protected-hidden threat",
        "false-threat handling",
        "threat source, posture, scale, and engagement-scope review",
        "ambush, pursuit, patrol, enforcement, security response, and alarm trigger routing",
        "environmental, terrain, contamination, corruption, unstable-object, and platform-threat trigger routing",
        "creature, rival, social-antagonist, institutional-proxy, and faction/enforcement threat routing",
        "hidden-state, rumor, signal, warning, and safe-presentation handoff",
        "active-scene, action-window, resolution, and encounter-trigger transition routing",
        "hazard/opposition construction handoff to d16-style owners",
        "hazard/opposition/contact state-delta routing",
    ]:
        assert marker in lowered


def test_b10_rejects_final_mechanics_and_runtime_generation() -> None:
    lowered = b10_text().lower()
    for phrase in [
        "final hazard schema", "final opposition schema", "final creature schema",
        "final encounter schema", "final threat schema", "final statblock schema",
        "final actor schema", "final object schema", "final world-state schema",
        "final hazard construction", "final opposition construction", "final creature construction",
        "final encounter construction", "final statblocks", "final creature stats",
        "final hazard stats", "final trap stats", "final security-system stats",
        "final patrol generation", "final wandering monster procedure", "final random encounter tables",
        "final encounter balance math", "final encounter budgets", "final cr/level/tier equivalence",
        "final hp/ac/defense/attack/damage/save math", "final action economy",
        "final initiative rules", "final surprise rules", "final ambush rules",
        "final morale rules", "final reaction rolls", "final boss/elite/minion/swarm/horde rules",
        "final lair/legendary/action rules", "final resistance/vulnerability/immunity math",
        "final harm, injury, corruption, contamination, instability, or recovery mechanics",
        "final npc motivation/personhood", "final creature ontology", "final security-system backend",
        "final platform/vehicle/mech/starship combat rules",
        "final faction enforcement/war/army/raid rules", "final social-antagonist mechanics",
        "final hidden-state reveal rules", "final presentation/narration behavior",
        "runtime threat state", "runtime encounter state", "runtime hazard state",
        "runtime opposition generation", "runtime creature generation", "runtime patrol generation",
        "runtime alarm/security backend", "runtime entity/component/event/state schemas",
    ]:
        assert phrase in lowered


def test_b10_rejects_runtime_c_family_and_donor_defaults() -> None:
    lowered = b10_text().lower()
    for marker in [
        "runtime state/event/command lifecycle ownership",
        "command lifecycle implementation",
        "c-family schema fields",
        "c01-c14 schema contents",
        "must not invent c-family fields",
        "rejects donor monster/trap/hazard/encounter/security/threat systems as astra defaults",
        "source-local donor monster",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
    ]:
        assert marker in lowered


def test_b10_references_d_series_only_as_draft_reference_material() -> None:
    text = b10_text()
    for marker in [
        "D00-D19 source packs are referenced only as draft source-pack/reference material",
        "not final current doctrine authority",
        "D00-03_state_delta_commit_protocol.md",
        "D02-00_resolution_architecture_and_owner_boundaries.md",
        "D05-03_relevance_handling_for_checks.md",
        "D07-02_corruption_contamination_and_instability.md",
        "D07-07_recovery_treatment_stabilization_and_adaptation.md",
        "D08-00_layered_actor_state_architecture.md",
        "D08-01_identity_continuity_personhood_and_agency.md",
        "D09-05_vehicles_platforms_ships_mechs_drones_and_external_bodies.md",
        "D10-02_territory_location_hazard_control_environment_register.md",
        "D10-07_information_state_public_knowledge_rumor_secrecy_records_register.md",
        "D11-03_hidden_state_rumor_secrecy_misinformation_presentation.md",
        "D12-02_action_windows_initiative_sequencing_and_interruptions.md",
        "D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md",
        "D14-05_travel_risk_resource_pressure_hazards_encounters_and_transition_handoffs.md",
        "D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md",
        "D16-00_opposition_creature_encounter_and_hazard_construction_owner_boundaries.md",
        "D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md",
        "D18-00_structural_time_campaign_continuity_arc_season_and_horizon_owner_boundaries.md",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
    ]:
        assert marker in text


def test_b10_durable_future_file_boundaries_and_registry_status() -> None:
    text = b10_text()
    for marker in [
        "B10 does not require, define, create, or promote B11.",
        "B10 does not require, define, create, or promote C01-C14.",
        "No registry status is promoted to current by B10.",
    ]:
        assert marker in text
