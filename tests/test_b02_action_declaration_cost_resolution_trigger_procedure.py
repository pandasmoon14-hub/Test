from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

B02_PATH = ROOT / "docs" / "doctrine" / "operations" / "batch_b" / "B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B02 owns",
    "## 4. What B02 must not own",
    "## 5. Non-collapse rule",
    "## 6. Action declaration grammar",
    "## 7. Intent, method, target, and scope framing",
    "## 8. Feasibility and boundary triage",
    "## 9. No-roll decision procedure",
    "## 10. Resolution trigger procedure",
    "## 11. Cost and risk preview procedure",
    "## 12. Declared cost commitment procedure",
    "## 13. Overreach, overinvestment, and success-at-cost routing",
    "## 14. Contested, opposed, defense, and resistance trigger routing",
    "## 15. Action-to-delta routing",
    "## 16. Owner-file handoff rules",
    "## 17. Batch B to C00/C-family handoff rules",
    "## 18. Missing-schema fallback and quarantine/escalation",
    "## 19. Source-local donor action/cost/resolution handling",
    "## 20. Runtime boundary",
    "## 21. Canon boundary",
    "## 22. Live-play/training boundary",
    "## 23. Examples of good and bad B02 usage",
    "## 24. Minimum tests or assertions",
    "## 25. Acceptance criteria",
    "## 26. Follow-up handoff to B03",
]


def b02_text() -> str:
    return read_utf8(B02_PATH)


def test_b02_file_exists_at_expected_path() -> None:
    assert B02_PATH.exists()
    assert B02_PATH.is_file()


def test_b02_required_sections_are_present() -> None:
    text = b02_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b02_declares_ownership_and_non_ownership() -> None:
    lowered = b02_text().lower()
    for phrase in [
        "declared-action intake procedure",
        "actor/intent/method/target framing",
        "action scope clarification",
        "action feasibility triage",
        "no-roll vs roll-trigger decision procedure",
        "visible cost/risk preview procedure",
        "hidden-risk boundary handling without exposing hidden truth",
        "declared cost commitment procedure",
        "resolution-owner trigger procedure",
        "action-to-delta routing requirements",
    ]:
        assert phrase in lowered

    for phrase in [
        "final d20 math",
        "exact difficulty numbers",
        "exact dn values",
        "dice/rng implementation",
        "final action economy",
        "initiative/round/turn procedure",
        "final resource economy math",
        "final cost math",
        "final combat math",
        "c-family schema fields",
        "c01-c14 schema contents",
        "runtime entity/component/event/state schemas",
        "persistent campaign state",
        "command lifecycle implementation",
        "live-play narration behavior",
        "final canon promotion",
        "accepted lexicon terms",
        "sourcebook prose",
    ]:
        assert phrase in lowered


def test_b02_references_b01_as_upstream_batch_b_context() -> None:
    lowered = b02_text().lower()
    assert "b01_scene_encounter_and_activity_procedure.md" in lowered
    assert "treats b01 as upstream batch b context" in lowered
    assert "upstream batch b scene, activity, encounter" in lowered


def test_b02_includes_c00_handoff_language_and_block() -> None:
    text = b02_text()
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


def test_b02_includes_action_declaration_routing_note_as_doctrine_facing_only() -> None:
    text = b02_text()
    lowered = text.lower()
    for marker in [
        "action_declaration_routing_note",
        "action_state: declared_action | clarified_action | freeform_resolution | no_roll_required | roll_triggered | owner_handoff_required | declared_cost_pending | declared_cost_committed | hidden_risk_marked | impossible_action | blocked_action | source_local_action_procedure | quarantined_action_gap",
        "actor_ref: string | null",
        "visible_cost_or_risk_present: boolean",
        "hidden_risk_boundary_present: boolean",
        "declared_cost_status: none | previewed | pending_commitment | committed | refused | escalated",
        "delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation",
    ]:
        assert marker in text
    for phrase in [
        "b02-specific lightweight doctrine-facing block",
        "not a runtime schema",
        "not a backend event",
        "not a command object",
        "not a c-family record",
        "not a sourcebook statblock",
        "not final mechanics",
    ]:
        assert phrase in lowered


def test_b02_rejects_final_math_and_dice_implementation() -> None:
    lowered = b02_text().lower()
    for phrase in [
        "must not define final resolution math",
        "final d20 math",
        "exact difficulty numbers",
        "exact dn values",
        "dice/rng implementation",
        "final cost math",
        "final combat math",
        "final overinvestment formulas",
        "final success-at-cost tables",
        "final cost prices",
    ]:
        assert phrase in lowered


def test_b02_rejects_runtime_state_event_command_lifecycle_ownership() -> None:
    lowered = b02_text().lower()
    for phrase in [
        "runtime entity/component/event/state schemas",
        "runtime state/event/command lifecycle ownership",
        "event-sourced state model",
        "state delta validator",
        "command lifecycle implementation",
        "runtime command lifecycle",
        "context packet compiler",
        "persistence",
        "backend validation",
        "hidden-information runtime state",
        "live-play behavior must not consume b02 procedure as runtime authority",
    ]:
        assert phrase in lowered


def test_b02_rejects_c_family_field_invention_and_schema_content_ownership() -> None:
    lowered = b02_text().lower()
    for phrase in [
        "must not invent c-family fields",
        "b02 must never add astra-sounding fields to c01-c14",
        "define c01-c14 schema contents",
        "does not require creation of c01-c14 files",
        "missing schema coverage must not produce improvised schema",
        "route to c00 governance rather than inventing c-family fields",
    ]:
        assert phrase in lowered


def test_b02_rejects_donor_action_cost_resolution_formats_as_astra_defaults() -> None:
    lowered = b02_text().lower()
    for phrase in [
        "donor action formats",
        "donor skill check formats",
        "donor spell/action/cost/slot/usage formats",
        "are donor evidence only",
        "do not become astra defaults through b02",
        "repeated donor action/cost/resolution patterns do not promote donor procedure to astra law",
    ]:
        assert phrase in lowered


def test_b02_includes_no_roll_and_resolution_trigger_logic() -> None:
    lowered = b02_text().lower()
    for phrase in [
        "a declared action is not automatically a roll",
        "a roll is not automatically a combat action",
        "no-roll decision procedure",
        "b02 chooses `no_roll_required` when all of the following are true",
        "resolution trigger procedure",
        "uncertainty_present",
        "meaningful_consequence_present",
        "opposition_present",
        "contested_timing_present",
        "defense_or_resistance_needed",
        "roll_triggered",
    ]:
        assert phrase in lowered


def test_b02_includes_cost_risk_preview_and_hidden_risk_boundary_language() -> None:
    lowered = b02_text().lower()
    for phrase in [
        "cost and risk preview procedure",
        "visible costs and visible risks must be previewed",
        "a visible cost/risk preview must not reveal hidden truth",
        "hidden-risk boundary handling",
        "hidden_risk_boundary_present",
        "hidden_risk_marked",
        "a cost is not automatically a resource spend",
        "time, position, exposure, obligation, attention, opportunity, instability, material, social standing, information, or source-local constraint",
    ]:
        assert phrase in lowered


def test_b02_includes_state_delta_routing_and_quarantine_escalation() -> None:
    text = b02_text()
    lowered = text.lower()
    for marker in [
        "state_delta_required",
        "Action-to-delta routing",
        "pending_schema",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
        "quarantined_action_gap",
        "quarantined_unresolved_delta",
        "owner_file_escalation",
    ]:
        assert marker in text
    assert "every meaningful action must route at least one delta to a recognized owner" in lowered


def test_b02_references_d_series_only_as_draft_source_pack_reference_material() -> None:
    text = b02_text()
    lowered = text.lower()
    for marker in [
        "D00-03_state_delta_commit_protocol.md",
        "D02-00_resolution_architecture_and_owner_boundaries.md",
        "D02-03_cost_commitment_overinvestment_and_success_at_cost.md",
        "D03_01_power_economy_lattice.md",
        "D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
    ]:
        assert marker in text
    assert "d00, d02, d03, d12, and d19 source-pack files are referenced only as draft source-pack/reference material" in lowered
    assert "not current doctrine authority" in lowered
    assert "must not promote d02 to final current doctrine" in lowered


def test_b02_does_not_require_or_define_later_batch_b_files() -> None:
    lowered = b02_text().lower()
    for phrase in [
        "b02 hands the next batch b slot to b03",
        "b02 does not create b03-b11",
        "does not predefine b03 content",
        "does not treat future batch b files as current authority",
    ]:
        assert phrase in lowered


def test_b02_does_not_require_c01_c14_creation_or_define_family_schemas() -> None:
    lowered = b02_text().lower()
    for phrase in [
        "b02 must never add astra-sounding fields to c01-c14",
        "define c01-c14 schema contents",
        "does not require creation of c01-c14 files",
        "missing schema coverage must not produce improvised schema",
        "route to c00 governance rather than inventing c-family fields",
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
    assert "- file_id: B02\n" not in registry_text

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
