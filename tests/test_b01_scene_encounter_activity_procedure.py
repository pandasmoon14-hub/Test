from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

B01_PATH = ROOT / "docs" / "doctrine" / "operations" / "batch_b" / "B01_scene_encounter_and_activity_procedure.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B01 owns",
    "## 4. What B01 must not own",
    "## 5. Non-collapse rule",
    "## 6. Scene, activity, and encounter definitions",
    "## 7. Scene entry procedure",
    "## 8. Scene purpose and pressure declaration",
    "## 9. Activity classification procedure",
    "## 10. Encounter trigger logic",
    "## 11. Cadence escalation and de-escalation rules",
    "## 12. Checkpoint sequence for cost, resolution, consequence, and state-delta routing",
    "## 13. Owner-file handoff rules",
    "## 14. Batch B to C00/C-family handoff rules",
    "## 15. Missing-schema fallback and quarantine/escalation",
    "## 16. Source-local donor procedure handling",
    "## 17. Runtime boundary",
    "## 18. Canon boundary",
    "## 19. Live-play/training boundary",
    "## 20. Examples of good and bad B01 usage",
    "## 21. Minimum tests or assertions",
    "## 22. Acceptance criteria",
    "## 23. Follow-up handoff to B02",
]


def b01_text() -> str:
    return read_utf8(B01_PATH)


def test_b01_file_exists_at_expected_path() -> None:
    assert B01_PATH.exists()
    assert B01_PATH.is_file()


def test_b01_required_sections_are_present() -> None:
    text = b01_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b01_declares_ownership_and_non_ownership() -> None:
    lowered = b01_text().lower()
    for phrase in [
        "scene entry and scene exit procedure",
        "scene purpose declaration",
        "activity classification",
        "encounter trigger logic",
        "transition from freeform play to focused activity",
        "transition from focused activity to structured encounter",
        "transition from structured encounter back to scene/freeform play",
        "checkpoint logic for declared cost, resolution, consequence, state-delta routing, and handoff",
    ]:
        assert phrase in lowered

    for phrase in [
        "c-family schema fields",
        "c01-c14 schema contents",
        "final mechanics",
        "exact math",
        "dice/rng rules",
        "combat math",
        "runtime entity/component/event/state schemas",
        "persistent campaign state",
        "command lifecycle implementation",
        "live-play narration behavior",
        "final canon promotion",
        "accepted lexicon terms",
        "sourcebook prose",
    ]:
        assert phrase in lowered


def test_b01_includes_c00_handoff_language() -> None:
    text = b01_text()
    for marker in [
        "C00 remains the schema handoff control surface",
        "batch_b_to_c_handoff",
        "target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema",
        "required_c00_base_fields: true",
        "source_evidence_refs_required: true",
        "construct_refs_required: true",
        "outcome_refs_required: true",
        "provenance_refs_required: true",
        "source_local_boundary_required_if_applicable: true",
        "rejected_donor_elements_required_if_applicable: true",
        "canon_eligibility_required: true",
        "review_routing_required: true",
    ]:
        assert marker in text


def test_b01_rejects_c_family_field_invention() -> None:
    lowered = b01_text().lower()
    for phrase in [
        "must not invent c-family fields",
        "must never add astra-sounding fields to c01-c14",
        "route to c00 governance rather than inventing c-family fields",
        "missing schema coverage must not produce improvised schema",
    ]:
        assert phrase in lowered


def test_b01_rejects_runtime_state_event_command_lifecycle_ownership() -> None:
    lowered = b01_text().lower()
    for phrase in [
        "runtime entity/component/event/state schemas",
        "event-sourced state model",
        "state delta validator",
        "command lifecycle implementation",
        "runtime command lifecycle",
        "context packet compiler",
        "persistence",
        "backend validation",
        "hidden-information runtime state",
        "live-play behavior must not consume b01 procedure as runtime authority",
    ]:
        assert phrase in lowered


def test_b01_rejects_donor_cadence_and_scripts_as_astra_defaults() -> None:
    lowered = b01_text().lower()
    for phrase in [
        "donor rounds, turns, watches, initiative formats",
        "encounter budgets",
        "adventure scenes",
        "adventure scripts",
        "are donor evidence only",
        "do not become astra defaults through b01",
        "repeated donor pressure does not promote donor procedure to astra law",
    ]:
        assert phrase in lowered


def test_b01_includes_quarantine_and_escalation_for_missing_schema() -> None:
    text = b01_text()
    lowered = text.lower()
    for marker in [
        "pending_schema",
        "unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists",
        "quarantined_procedure_gap",
        "Missing-schema fallback",
        "defer_until_schema_exists",
        "human_review",
    ]:
        assert marker in text
    assert "unclassifiable records are quarantined or escalated, not normalized by invention" in lowered


def test_b01_references_d_series_only_as_draft_source_pack_reference_material() -> None:
    text = b01_text()
    lowered = text.lower()
    for marker in ["D00-03_state_delta_commit_protocol.md", "D12-00_time_action_cadence_encounter_procedure_and_owner_boundaries.md", "D12-01_cadence_states_transition_triggers_and_scene_flow.md", "D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md", "D12-07_records_not_final_schema_and_conversion_handoff_shapes.md", "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md"]:
        assert marker in text
    assert "d00, d12, and d19 source-pack files are referenced only as draft source-pack/reference material" in lowered
    assert "not current doctrine authority" in lowered


def test_b01_does_not_require_c01_c14_creation_or_define_family_schemas() -> None:
    lowered = b01_text().lower()
    for phrase in [
        "b01 does not require creation of c01-c14 files",
        "must not invent c-family fields",
        "must not invent c-family fields, donor field names, donor record formats, or c01-c14 schema contents",
        "b01 must never add astra-sounding fields to c01-c14",
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


def _registry_scalar(file_id: str, key: str) -> str:
    prefix = f"  {key}: "
    for line in _registry_record_block(file_id).splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip().strip("'\"")
    raise AssertionError(f"Missing {key} for {file_id}")


def test_registry_status_is_not_promoted_to_current() -> None:
    registry_text = read_utf8(REGISTRY_PATH)
    assert "- file_id: B01\n" not in registry_text

    forbidden_promoted_statuses = {
        "current",
        "tested_minimum",
        "stable_for_family",
        "stable_cross_family",
    }
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        assert _registry_scalar(file_id, "status") not in forbidden_promoted_statuses
        assert _registry_scalar(file_id, "test_status") not in forbidden_promoted_statuses
        assert _registry_scalar(file_id, "authority_level") not in {"canon-current", "runtime-ready", "schema-current"}
        assert "canon-current" not in block
        assert "runtime-ready" not in block

    assert _registry_scalar("C00", "status") == "draft"
    assert _registry_scalar("C01", "status") == "draft"
    assert _registry_scalar("C01", "authority_level") == "schema-draft"
    assert _registry_scalar("C01", "test_status") == "designed"
    assert _registry_scalar("C01", "review_status") == "not_reviewed"

    for number in range(2, 15):
        file_id = f"C{number:02d}"
        assert _registry_scalar(file_id, "status") not in forbidden_promoted_statuses
        assert _registry_scalar(file_id, "test_status") not in forbidden_promoted_statuses
