from tests.helpers import ROOT, read_utf8

B08_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "operations"
    / "batch_b"
    / "B08_travel_exploration_navigation_and_discovery_procedure.md"
)

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B08 owns",
    "## 4. What B08 must not own",
    "## 5. Non-collapse rule",
    "## 6. Travel, exploration, navigation, discovery, route, map-state, and site-entry definitions",
    "## 7. Travel/exploration intake procedure",
    "## 8. Intent, posture, route/area, known-state, and risk/handoff checkpoints",
    "## 9. Route-state and known-state classification",
    "## 10. Travel/exploration interval setup",
    "## 11. Navigation and orientation trigger procedure",
    "## 12. Posture pressure and environmental PCR routing",
    "## 13. Resource, exposure, and support-pressure trigger routing",
    "## 14. Scouting procedure",
    "## 15. Mapping and map-state update procedure",
    "## 16. Discovery opportunity and discovery-confidence procedure",
    "## 17. Exploration context profile classification",
    "## 18. Site approach and site entry procedure",
    "## 19. Watch, monitoring, and ambush exposure procedure",
    "## 20. Hazard, encounter, contact, and opposition trigger routing",
    "## 21. Travel/exploration progress, delay, lost-route, blocked-route, discovery, and transition routing",
    "## 22. Owner-file handoff rules",
    "## 23. Batch B to C00/C-family handoff rules",
    "## 24. Missing-schema fallback and quarantine/escalation",
    "## 25. Source-local donor travel/exploration/map/random-table handling",
    "## 26. Runtime boundary",
    "## 27. Canon boundary",
    "## 28. Live-play/training boundary",
    "## 29. Examples of good and bad B08 usage",
    "## 30. Minimum tests or assertions",
    "## 31. Acceptance criteria",
    "## 32. Follow-up handoff to B09",
]


def b08_text() -> str:
    return read_utf8(B08_PATH)


def test_b08_file_exists_at_expected_path() -> None:
    assert B08_PATH.exists()
    assert B08_PATH.is_file()


def test_b08_required_sections_are_present() -> None:
    text = b08_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b08_declares_ownership_and_non_ownership() -> None:
    lowered = b08_text().lower()
    for phrase in [
        "travel/exploration intake after b01-b07 produce route, area, movement, navigation, discovery, site-entry, or travel-pressure questions",
        "posture declaration and posture-pressure routing",
        "route/area declaration and route-state classification",
        "party-facing known-state review",
        "protected-hidden route, map, and world-state handling without revealing truth",
        "travel/exploration interval setup",
        "navigation/orientation trigger routing",
        "scouting procedure",
        "mapping procedure and map-state update routing",
        "discovery opportunity classification and discovery-confidence routing",
        "site approach and site entry procedure",
        "watch and monitoring procedure",
        "ambush exposure procedure",
        "hazard/encounter/contact trigger identification as routing, not construction",
    ]:
        assert phrase in lowered

    for phrase in [
        "final travel schema",
        "final exploration schema",
        "final map schema",
        "final location schema",
        "final route schema",
        "final discovery schema",
        "final hazard schema",
        "final encounter schema",
        "final world-state schema",
        "c-family schema fields",
        "c01-c14 schema contents",
        "final map geometry",
        "final hex rules",
        "final grid rules",
        "final zone/node rules",
        "final dungeon-turn procedure",
        "final watch-shift system",
        "final travel-day procedure",
        "final travel pace math",
        "final navigation dcs",
        "final scouting check math",
        "final random encounter tables",
        "final weather tables",
        "final hazard tables",
        "final supply attrition math",
        "final fuel economy",
        "final exposure/harm math",
        "final encounter construction",
        "final opposition statblocks",
        "final site keys",
        "boxed text",
        "final world truth",
        "final hidden-state reveal rules",
        "final presentation/narration behavior",
        "final faction clocks",
        "final campaign-scale journey pacing",
        "final time-skip procedure",
        "runtime travel state",
        "runtime location state",
        "runtime map state",
        "runtime world-state database",
        "runtime encounter generation",
    ]:
        assert phrase in lowered


def test_b08_references_b01_through_b07_as_upstream_batch_b_context() -> None:
    lowered = b08_text().lower()
    for marker in [
        "b01_scene_encounter_and_activity_procedure.md",
        "b02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md",
        "b03_item_gear_equipment_and_asset_use_procedure.md",
        "b04_inventory_storage_custody_and_burden_procedure.md",
        "b05_acquisition_reward_requisition_and_value_flow_procedure.md",
        "b06_project_crafting_salvage_repair_and_upgrade_procedure.md",
        "b07_recovery_training_research_and_preparation_project_procedure.md",
        "upstream batch b context",
        "must build on them, not rewrite them",
    ]:
        assert marker in lowered


def test_b08_includes_c00_handoff_language_and_block() -> None:
    text = b08_text()
    for marker in [
        "C00 remains the schema handoff control surface",
        "batch_b_to_c_handoff",
        "target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema",
        "schema_status: not_started | stub_index_only | minimum_unlock_draft | tested_minimum | stable_for_family | stable_cross_family | superseded | deprecated",
        "required_c00_base_fields: true",
        "source_evidence_refs_required: true",
        "construct_refs_required: true",
        "outcome_refs_required: true",
        "provenance_refs_required: true",
        "source_local_boundary_required_if_applicable: true",
        "rejected_donor_elements_required_if_applicable: true",
        "canon_eligibility_required: true",
        "review_routing_required: true",
        "unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists",
    ]:
        assert marker in text


def test_b08_includes_routing_note_as_doctrine_facing_only() -> None:
    lowered = b08_text().lower()
    for phrase in [
        "travel_exploration_routing_note",
        "doctrine-facing only",
        "not runtime schema",
        "not backend event",
        "not command object",
        "not c-family record",
        "not travel database row",
        "not map database row",
        "not location-state record",
        "not encounter table",
        "not random table",
        "not travel table",
        "not sourcebook map key",
        "not final mechanics",
        "not canon",
        "not player-facing rule text",
    ]:
        assert phrase in lowered


def test_b08_routing_note_uses_requested_field_shape() -> None:
    text = b08_text()
    for marker in [
        "travel_exploration_intent:",
        "posture_family:",
        "route_state:",
        "known_state_category:",
        "interval_scale:",
        "discovery_category:",
        "discovery_confidence:",
        "map_state_category:",
        "exploration_context_profile:",
        "pressure_families:",
        "progress_state:",
        "owner_handoff_required: boolean",
        "owner_handoff_reason:",
        "delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation",
        "note: string",
    ]:
        assert marker in text
    assert "  intent:" not in text
    assert "  context_profile:" not in text
    assert "  pressure_family:" not in text


def test_b08_includes_required_vocabularies() -> None:
    text = b08_text()
    for marker in [
        "route_travel",
        "area_exploration",
        "site_approach",
        "platform_navigation",
        "realm_crossing",
        "unknown_intent",
        "Posture families:",
        "speed",
        "stealth",
        "sensor_sweep",
        "source_local_posture",
        "Route states:",
        "partially_known",
        "dangerous",
        "watched",
        "unmapped",
        "Known-state categories:",
        "mapped_but_unverified",
        "protected_hidden",
        "Interval scales:",
        "momentary_approach",
        "wilderness_leg",
        "realm_crossing_stage",
        "Discovery categories:",
        "route_discovery",
        "hidden_boundary_hint",
        "Discovery confidence states:",
        "high_confidence",
        "false_or_compromised",
        "Map-state categories:",
        "partially_mapped",
        "unreachable",
        "Exploration context profiles:",
        "urban_social_dense",
        "space_vehicle_platform",
        "Pressure families:",
        "resource_pressure",
        "encounter_pressure",
        "hidden_state_pressure",
        "Progress states:",
        "advanced_with_discovery",
        "encounter_triggered",
        "pressure_escalated",
    ]:
        assert marker in text


def test_b08_separates_core_concepts() -> None:
    lowered = b08_text().lower()
    for phrase in [
        "travel is not automatic time passage",
        "exploration is not automatic map reveal",
        "navigation is not always a roll",
        "a route is not necessarily geometric",
        "a map is not truth",
        "party-facing known-state is not actual world-state",
        "a discovery is not automatically actual truth",
        "scouting is not hidden-truth revelation",
        "mapping is not canon creation",
        "site entry is not boxed-text reveal",
        "a watch is not a universal shift system",
        "ambush exposure is not automatic surprise",
        "hazard pressure is not hazard construction",
        "encounter pressure is not encounter generation",
        "environmental pcr may shape travel pressure but must not expose hidden pneuma, hidden cosmic modifiers, hidden truth, or protected-hidden state",
        "runtime boundary",
        "canon boundary",
    ]:
        assert phrase in lowered


def test_b08_includes_required_procedure_topics() -> None:
    lowered = b08_text().lower()
    for phrase in [
        "travel/exploration intake procedure",
        "intent, posture, route/area, known-state, and risk/handoff checkpoints",
        "route-state and known-state classification",
        "travel/exploration interval setup",
        "navigation and orientation trigger procedure",
        "posture pressure",
        "environmental pcr routing",
        "resource, exposure, and support-pressure trigger routing",
        "scouting procedure",
        "mapping and map-state update procedure",
        "discovery opportunity and discovery-confidence procedure",
        "exploration context profile classification",
        "site approach and site entry procedure",
        "watch, monitoring, and ambush exposure procedure",
        "hazard, encounter, contact, and opposition trigger routing",
        "transition handoff",
    ]:
        assert phrase in lowered


def test_b08_rejects_runtime_state_event_and_command_lifecycle_ownership() -> None:
    lowered = b08_text().lower()
    for phrase in [
        "runtime entity/component/event/state schemas",
        "persistent campaign state",
        "command lifecycle implementation",
        "context packet compiler",
        "hidden-information runtime state",
        "b08 is not runtime authority",
    ]:
        assert phrase in lowered


def test_b08_rejects_c_family_field_invention_and_schema_content_ownership() -> None:
    lowered = b08_text().lower()
    for phrase in [
        "must not invent c-family fields",
        "c01-c14 schema contents",
        "b08 does not require, define, create, or promote c01-c14",
    ]:
        assert phrase in lowered


def test_b08_rejects_donor_defaults() -> None:
    lowered = b08_text().lower()
    for phrase in [
        "donor travel/exploration/map/hexcrawl/dungeon/ship/realm/random-table systems as astra defaults",
        "random encounters are not default astra law",
        "donor hexcrawl as universal map law",
        "donor dungeon turns as universal exploration cadence",
        "donor random-table world truth",
    ]:
        assert phrase in lowered


def test_b08_includes_state_delta_routing() -> None:
    lowered = b08_text().lower()
    for phrase in [
        "state-delta routing",
        "every meaningful travel/exploration/navigation/discovery event must route at least one delta",
        "delta_routing_status",
        "owner_routed",
        "transition_note",
        "source_local_retained_effect",
        "quarantined_unresolved_delta",
        "owner_file_escalation",
    ]:
        assert phrase in lowered


def test_b08_includes_source_local_quarantine_escalation_fallbacks() -> None:
    lowered = b08_text().lower()
    for phrase in [
        "source-local donor travel/exploration/map/random-table handling",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
        "source-local retention",
    ]:
        assert phrase in lowered


def test_b08_references_d_series_only_as_draft_reference_material() -> None:
    text = b08_text()
    for marker in [
        "D00-03_state_delta_commit_protocol.md",
        "D02-00_resolution_architecture_and_owner_boundaries.md",
        "D03_01_power_economy_lattice.md",
        "D05-03_relevance_handling_for_checks.md",
        "D07-02_corruption_contamination_and_instability.md",
        "D09-05_vehicles_platforms_ships_mechs_drones_and_external_bodies.md",
        "D10-02_territory_location_hazard_control_environment_register.md",
        "D11-03_hidden_state_rumor_secrecy_misinformation_presentation.md",
        "D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md",
        "D13-02_project_creation_requirement_discovery_commitment_and_interval_setup.md",
        "D14-00` through `D14-07",
        "D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md",
        "D16-00_opposition_creature_encounter_and_hazard_construction_owner_boundaries.md",
        "D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md",
        "D18-00_structural_time_campaign_continuity_arc_season_and_horizon_owner_boundaries.md",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
        "D00-D19 source-pack files are referenced only as draft source-pack/reference material",
        "They are not current doctrine authority, final mechanics, runtime authority, canon, sourcebook prose, or Astra defaults.",
    ]:
        assert marker in text


def test_b08_does_not_require_define_create_or_promote_future_files_or_schemas() -> None:
    lowered = b08_text().lower()
    assert "b08 does not require, define, create, or promote b09-b11" in lowered
    assert "b08 must not create b09-b11" in lowered
    assert "b08 does not require, define, create, or promote c01-c14" in lowered


def test_b08_does_not_promote_registry_status_to_current() -> None:
    lowered = b08_text().lower()
    assert "status: current" not in lowered
    assert "registry_status: current" not in lowered
    assert "current doctrine authority" in lowered
    assert "not current doctrine authority" in lowered
