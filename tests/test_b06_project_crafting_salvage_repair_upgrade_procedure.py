from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

B06_PATH = ROOT / "docs" / "doctrine" / "operations" / "batch_b" / "B06_project_crafting_salvage_repair_and_upgrade_procedure.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B06 owns",
    "## 4. What B06 must not own",
    "## 5. Non-collapse rule",
    "## 6. Project, interval, requirement, commitment, and output definitions",
    "## 7. Project/long-task intake procedure",
    "## 8. Intent, goal, family, and scope classification",
    "## 9. Requirement discovery and protected-hidden requirement handling",
    "## 10. Cost/risk preview and commitment procedure",
    "## 11. Interval setup and progress-trigger procedure",
    "## 12. Crafting project procedure",
    "## 13. Salvage processing project procedure",
    "## 14. Repair and maintenance project procedure",
    "## 15. Modification and upgrade project procedure",
    "## 16. Facilities, tools, schematics, recipes, contributors, materials, and support-burden procedure",
    "## 17. Progress, partial completion, complication, failure, interruption, and abandonment routing",
    "## 18. Concurrent project and project-load routing",
    "## 19. Project output, ownership, custody, value-flow, and object-state handoff rules",
    "## 20. Owner-file handoff rules",
    "## 21. Batch B to C00/C-family handoff rules",
    "## 22. Missing-schema fallback and quarantine/escalation",
    "## 23. Source-local donor downtime/crafting/project handling",
    "## 24. Runtime boundary",
    "## 25. Canon boundary",
    "## 26. Live-play/training boundary",
    "## 27. Examples of good and bad B06 usage",
    "## 28. Minimum tests or assertions",
    "## 29. Acceptance criteria",
    "## 30. Follow-up handoff to B07",
]


def b06_text() -> str:
    return read_utf8(B06_PATH)


def test_b06_file_exists_at_expected_path() -> None:
    assert B06_PATH.exists()
    assert B06_PATH.is_file()


def test_b06_required_sections_are_present() -> None:
    text = b06_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b06_declares_ownership_and_non_ownership() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "project/long-task intake after b01-b05 produce interval-scale work pressure",
        "project intent, goal, family, scope, requirement, cost/risk, commitment, and interval setup routing",
        "crafting as project routing, not final crafting rules",
        "salvage processing as project routing, not automatic wealth/material generation",
        "repair and maintenance as project routing, not final repair math",
        "modification and upgrade as project routing",
        "requirement discovery and protected-hidden requirement handling",
        "interval commitment and committed-cost handling",
        "project pause, resume, interruption, abandonment, archival, and follow-up handoff procedure",
        "concurrent project, contributor, facility, material, and support-burden routing",
    ]:
        assert phrase in lowered

    for phrase in [
        "final project schema",
        "final crafting schema",
        "final object schema",
        "final inventory schema",
        "final economy schema",
        "c-family schema fields",
        "c01-c14 schema contents",
        "final crafting math",
        "final repair math",
        "final salvage yield tables",
        "final upgrade math",
        "final item stats",
        "runtime project state",
        "runtime entity/component/event/state schemas",
        "command lifecycle implementation",
        "context packet compiler",
        "sourcebook prose",
        "donor crafting/downtime/project systems as astra defaults",
    ]:
        assert phrase in lowered


def test_b06_references_b01_b02_b03_b04_and_b05_as_upstream_batch_b_context() -> None:
    lowered = b06_text().lower()
    for marker in [
        "b01_scene_encounter_and_activity_procedure.md",
        "b02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md",
        "b03_item_gear_equipment_and_asset_use_procedure.md",
        "b04_inventory_storage_custody_and_burden_procedure.md",
        "b05_acquisition_reward_requisition_and_value_flow_procedure.md",
        "upstream batch b context",
        "must build on them, not rewrite them",
    ]:
        assert marker in lowered


def test_b06_includes_c00_handoff_language_and_block() -> None:
    text = b06_text()
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


def test_b06_includes_project_work_routing_note_as_doctrine_facing_only() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "project_work_routing_note",
        "doctrine-facing only",
        "not a runtime schema",
        "not runtime project state",
        "not a backend event",
        "not a command object",
        "not a c-family record",
        "not a project database row",
        "not an inventory ledger entry",
        "not an object statblock",
        "not an item recipe",
        "not a crafting table",
        "not final mechanics",
        "not canon",
        "not player-facing rule text",
    ]:
        assert phrase in lowered
    assert "project_routing_note" not in lowered


def test_b06_includes_project_vocabularies() -> None:
    text = b06_text()
    for marker in [
        "crafting",
        "salvage",
        "repair",
        "maintenance",
        "modification",
        "upgrade",
        "installation_preparation",
        "resource_gathering",
        "facility_work",
        "contributor_supported_work",
        "source_local_project",
        "unknown_project",
        "minor",
        "standard",
        "major",
        "extended",
        "transformational",
        "source_local_scope",
        "unknown_scope",
        "met",
        "missing",
        "unknown",
        "protected_hidden",
        "blocked_by_owner_file",
        "deferred_until_schema_exists",
        "time_block",
        "materials_reserved",
        "value_committed",
        "facility_claimed",
        "toolchain_committed",
        "contributor_assigned",
        "object_placed_under_work",
        "advanced",
        "advanced_with_cost",
        "partial",
        "stalled",
        "blocked",
        "complicated",
        "damaged",
        "interrupted",
        "completed_with_complication",
        "failed",
        "abandoned",
        "cost_increase",
        "material_loss",
        "tool_or_facility_damage",
        "contributor_risk",
        "object_instability",
        "contamination",
        "schematic_error",
        "recipe_mismatch",
        "incompatible_component",
        "legal_exposure",
        "source_local_threat",
        "object_created",
        "object_repaired",
        "object_maintained",
        "object_modified",
        "object_upgraded",
        "salvage_recovered",
        "salvage_contaminated",
        "material_gathered",
        "partial_output",
        "flawed_output",
        "dangerous_output",
        "quarantined_unresolved_delta",
        "owner_file_escalation",
    ]:
        assert marker in text


def test_b06_separates_project_and_related_concepts() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "a project is not automatically downtime",
        "downtime is not automatically safe time",
        "crafting is not a recipe table",
        "repair is not automatic restoration",
        "maintenance is not invisible bookkeeping",
        "salvage is not free material or wealth",
        "modification is not always improvement",
        "upgrade is not universal item leveling",
        "an `interval` is a bounded work window",
        "progress is not always numeric",
        "partial completion is not failure by default",
        "failure does not automatically erase all progress",
        "project outputs must be routed by owner, not treated as automatic inventory, wealth, object stats, canon, or runtime state",
        "custody_routed",
        "value_committed",
        "object-state questions",
        "b06 is not runtime authority",
    ]:
        assert phrase in lowered


def test_b06_includes_required_project_procedures() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "project/long-task intake procedure",
        "intent, goal, family, and scope classification",
        "requirement discovery and protected-hidden requirement handling",
        "cost/risk preview and commitment procedure",
        "interval setup and progress-trigger procedure",
        "crafting project procedure",
        "salvage processing project procedure",
        "repair and maintenance project procedure",
        "modification and upgrade project procedure",
        "facilities, tools, schematics, recipes, contributors, materials, and support-burden procedure",
        "progress, partial completion, complication, failure, interruption, and abandonment routing",
        "concurrent project and project-load routing",
    ]:
        assert phrase in lowered


def test_b06_rejects_final_project_crafting_and_runtime_mechanics() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "final project schema",
        "final crafting schema",
        "final object schema",
        "final inventory schema",
        "final economy schema",
        "final crafting math",
        "final repair math",
        "final salvage yield tables",
        "final upgrade math",
        "final item stats",
        "final recipe system",
        "final downtime activity menu",
        "final project-clock system",
        "final universal progress-point system",
        "final crafting dcs",
        "final crafting costs per day",
        "final runtime project state",
        "runtime project state",
        "final sourcebook crafting/repair/salvage/upgrade/downtime rules",
    ]:
        assert phrase in lowered


def test_b06_rejects_runtime_state_event_command_lifecycle_ownership() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "b06 rejects runtime state/event/command lifecycle ownership",
        "runtime entity/component/event/state schemas",
        "persistent campaign state",
        "command lifecycle implementation",
        "context packet compiler",
        "hidden-information runtime state",
        "live-play behavior must not consume b06 procedure as runtime authority",
    ]:
        assert phrase in lowered


def test_b06_rejects_c_family_field_invention_and_schema_content_ownership() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "must not invent c-family fields",
        "c-family schema fields",
        "c01-c14 schema contents",
        "c-family field invention",
        "c01-c14 schema-content ownership",
        "batch b procedure may identify that a c-family handoff is needed, but it must not invent c-family fields",
        "target_schema_family: c01 | c02 | c03 | c04 | c05 | c06 | c07 | c08 | c09 | c10 | c11 | c12 | c13 | c14 | pending_schema",
    ]:
        assert phrase in lowered


def test_b06_rejects_donor_downtime_crafting_project_systems_as_astra_defaults() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "donor crafting/downtime/project systems as astra defaults",
        "source-local donor downtime/crafting/project handling",
        "source-local donor downtime, crafting, salvage, repair, maintenance, modification, upgrade, requisition, project, or long-task systems are not astra defaults",
        "do not import donor timing, dcs, item levels, crafting prices, repair formulas, salvage tables, facility bonuses, tool proficiency bonuses, rest procedures, downtime menus, requisition ratings, or sourcebook prose",
    ]:
        assert phrase in lowered


def test_b06_includes_project_work_state_delta_routing() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "project/crafting/salvage/repair/upgrade state-delta routing event",
        "must route at least one delta to a recognized owner",
        "no_delta_required",
        "owner_routed",
        "transition_note",
        "source_local_retained_effect",
        "quarantined_unresolved_delta",
        "owner_file_escalation",
        "delta_routing_status",
    ]:
        assert phrase in lowered


def test_b06_includes_source_local_quarantine_escalation_and_review() -> None:
    text = b06_text()
    lowered = text.lower()
    for marker in [
        "Source-local donor downtime/crafting/project handling",
        "pending_schema",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
        "source_local_review",
        "source-local boundary",
    ]:
        assert marker in text
    assert "missing-schema fallback and quarantine/escalation" in lowered
    assert "source-local handling procedure" in lowered


def test_b06_references_d_series_only_as_draft_source_pack_reference_material() -> None:
    text = b06_text()
    lowered = text.lower()
    for marker in [
        "D00-03_state_delta_commit_protocol.md",
        "D02-00_resolution_architecture_and_owner_boundaries.md",
        "D03_01_power_economy_lattice.md",
        "D05-04_training_practice_teachers_and_downtime.md",
        "D05-05_research_experimentation_and_theorycraft.md",
        "D09-06_crafting_repair_salvage_modification_upgrade_and_requisition_interface.md",
        "D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md",
        "D13-00",
        "D13-07",
        "D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
    ]:
        assert marker in text
    assert "d00, d02, d03, d05, d09, d12, d13, d17, and d19 source-pack files are referenced only as draft source-pack/reference material" in lowered
    assert "not current doctrine authority" in lowered


def test_b06_does_not_require_define_create_or_promote_b07_b11() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "b06 does not require, define, create, or promote b07-b11",
        "does not make b07-b11 current doctrine",
        "b06 does not create b07-b11",
    ]:
        assert phrase in lowered


def test_b06_does_not_require_define_create_or_promote_c01_c14() -> None:
    lowered = b06_text().lower()
    for phrase in [
        "b06 does not require, define, create, or promote c01-c14",
        "does not make c01-c14 current doctrine",
        "future c01-c14 schema families may receive conversion handoffs but b06 must not invent their fields",
    ]:
        assert phrase in lowered


def _registry_record_block(file_id: str) -> str:
    registry_text = read_utf8(REGISTRY_PATH)
    marker = f"- file_id: {file_id}\n"
    start = registry_text.index(marker)
    next_record = registry_text.find("\n- file_id:", start + len(marker))
    if next_record == -1:
        return registry_text[start:]
    return registry_text[start:next_record]


def test_registry_status_is_not_promoted_to_current() -> None:
    registry_text = read_utf8(REGISTRY_PATH)
    assert "- file_id: B06\n" not in registry_text
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        assert "  status: current" not in block
    assert "  status: draft" in _registry_record_block("C00")
    for number in range(1, 15):
        assert "  status: todo" in _registry_record_block(f"C{number:02d}")
