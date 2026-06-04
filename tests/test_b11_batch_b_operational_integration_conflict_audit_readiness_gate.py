from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

B11_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "operations"
    / "batch_b"
    / "B11_batch_b_operational_integration_conflict_audit_and_readiness_gate.md"
)

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B11 owns",
    "## 4. What B11 must not own",
    "## 5. Capstone non-collapse rule",
    "## 6. Batch B file inventory",
    "## 7. Batch B owner-boundary audit",
    "## 8. Cross-file dependency audit",
    "## 9. Operational handoff matrix",
    "## 10. Routing-chain verification procedure",
    "## 11. Conflict, overlap, duplicate, and owner-theft audit",
    "## 12. Missing-owner and missing-schema gap audit",
    "## 13. Source-local, quarantine, escalation, and human-review consistency audit",
    "## 14. C00/C-family handoff discipline audit",
    "## 15. Record-shape and doctrine-facing note governance audit",
    "## 16. Runtime, canon, sourcebook, and live-play boundary audit",
    "## 17. Durable test posture audit",
    "## 18. Mixed operational routing stress tests",
    "## 19. Batch C readiness gate",
    "## 20. Deferred patch ledger",
    "## 21. Batch B completion status",
    "## 22. Owner-file handoff rules",
    "## 23. Batch B to C00/C-family handoff rules",
    "## 24. Missing-schema fallback and quarantine/escalation",
    "## 25. Source-local donor-system containment audit",
    "## 26. Runtime boundary",
    "## 27. Canon boundary",
    "## 28. Live-play/training boundary",
    "## 29. Examples of good and bad B11 usage",
    "## 30. Minimum tests or assertions",
    "## 31. Acceptance criteria",
    "## 32. Follow-up handoff after Batch B",
]

BATCH_B_REFERENCES = [
    "B01_scene_encounter_and_activity_procedure.md",
    "B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md",
    "B03_item_gear_equipment_and_asset_use_procedure.md",
    "B04_inventory_storage_custody_and_burden_procedure.md",
    "B05_acquisition_reward_requisition_and_value_flow_procedure.md",
    "B06_project_crafting_salvage_repair_and_upgrade_procedure.md",
    "B07_recovery_training_research_and_preparation_project_procedure.md",
    "B08_travel_exploration_navigation_and_discovery_procedure.md",
    "B09_social_faction_contact_and_institutional_interaction_procedure.md",
    "B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md",
]

AUDIT_DIMENSIONS = [
    "owner_boundary",
    "dependency",
    "handoff",
    "routing_chain",
    "duplicate_overlap",
    "conflict",
    "missing_owner",
    "missing_schema",
    "source_local_boundary",
    "quarantine_escalation",
    "c00_handoff",
    "record_shape",
    "not_final_schema_warning",
    "runtime_boundary",
    "canon_boundary",
    "sourcebook_boundary",
    "live_play_boundary",
    "durable_test_posture",
    "mixed_routing_stress",
    "batch_c_readiness",
    "deferred_patch",
]

AUDIT_OUTCOMES = [
    "no_conflict",
    "overlap_allowed",
    "companion_records",
    "duplicate_review_needed",
    "owner_boundary_patch_needed",
    "handoff_patch_needed",
    "wording_patch_needed",
    "test_patch_needed",
    "pending_schema",
    "quarantine",
    "escalation",
    "human_review",
    "defer_until_schema_exists",
    "source_local_retained",
    "runtime_gate_needed",
    "canon_review_needed",
    "batch_c_ready",
    "batch_c_blocked",
    "batch_b_ready",
    "batch_b_not_ready",
]

READINESS_STATES = [
    "ready_for_batch_c_unlock",
    "ready_with_deferred_gaps",
    "blocked_by_owner_conflict",
    "blocked_by_missing_handoff",
    "blocked_by_schema_drift",
    "blocked_by_runtime_drift",
    "blocked_by_canon_drift",
    "blocked_by_source_local_leakage",
    "blocked_by_test_gap",
    "human_review_required",
]

ROUTING_STRESS_TEST_FAMILIES = [
    "scene_to_action_to_delta",
    "action_to_object_to_inventory",
    "object_to_value_to_project",
    "project_to_recovery_training_research",
    "travel_to_discovery_to_threat",
    "travel_to_social_access",
    "social_to_faction_to_value",
    "social_to_threat_to_scene",
    "threat_to_harm_to_recovery",
    "threat_to_actor_to_object",
    "hazard_to_travel_to_campaign_horizon",
    "source_local_to_quarantine_to_schema",
    "mixed_donor_construct_to_owner_chain",
    "runtime_boundary_pressure",
    "canon_boundary_pressure",
]

OWNER_PATCH_DESTINATIONS = [
    "B01",
    "B02",
    "B03",
    "B04",
    "B05",
    "B06",
    "B07",
    "B08",
    "B09",
    "B10",
    "C00",
    "C01_C14",
    "Batch_C_schema_family",
    "Runtime_Gate_B",
    "canon_consolidation",
    "source_local_registry",
    "human_review",
    "future_batch",
    "unknown_owner",
]


def b11_text() -> str:
    return read_utf8(B11_PATH)


def test_b11_file_exists_at_expected_path() -> None:
    assert B11_PATH.exists()
    assert B11_PATH.is_file()


def test_b11_required_sections_are_present() -> None:
    text = b11_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b11_declares_ownership_and_non_ownership() -> None:
    lowered = b11_text().lower()
    for phrase in [
        "batch b integration judgment across b01-b10",
        "owner-boundary audit across b01-b10",
        "cross-file dependency audit",
        "operational handoff matrix construction",
        "routing-chain verification",
        "duplicate/overlap classification",
        "conflict detection",
        "missing-owner gap detection",
        "missing-schema gap detection",
        "source-local, quarantine, escalation, and human-review consistency audit",
        "batch c readiness gate",
    ]:
        assert phrase in lowered

    for phrase in [
        "a new operational gameplay domain",
        "revised b01 scene/activity/encounter procedure",
        "revised b02 action/resolution procedure",
        "revised b03 object-use procedure",
        "revised b04 inventory/custody/burden procedure",
        "revised b05 acquisition/value-flow procedure",
        "revised b06 project/crafting procedure",
        "revised b07 recovery/training/research procedure",
        "revised b08 travel/exploration procedure",
        "revised b09 social/faction/contact procedure",
        "revised b10 hazard/opposition/threat procedure",
        "final mechanics",
        "final math",
        "final schemas",
        "new doctrine that belongs to an owner file",
    ]:
        assert phrase in lowered


def test_b11_references_b01_through_b10_as_upstream_batch_b_context() -> None:
    text = b11_text()
    for marker in BATCH_B_REFERENCES:
        assert marker in text
    lowered = text.lower()
    assert "b11 is the batch b capstone/readiness-gate doctrine draft for auditing b01-b10" in lowered
    assert "this file sits after b01-b10 and builds on them; it does not rewrite them" in lowered


def test_b11_includes_c00_handoff_language_and_batch_b_to_c_handoff() -> None:
    text = b11_text()
    for marker in [
        "C00 remains the schema handoff control surface",
        "C00/C-family handoff discipline audit",
        "batch_b_to_c_handoff:",
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
        "unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists",
    ]:
        assert marker in text


def test_b11_integration_readiness_note_is_doctrine_facing_audit_facing_only() -> None:
    lowered = b11_text().lower()
    for phrase in [
        "batch_b_integration_readiness_audit_note:",
        "b11 allows lightweight doctrine-facing audit notes only",
        "these notes support handoff and readiness review",
        "they are not runtime schemas",
        "database contracts",
        "event logs",
        "save-state formats",
        "command lifecycles",
        "context packets",
        "canon records",
        "sourcebook prose",
        "not-final-schema warning consistency requirement",
    ]:
        assert phrase in lowered


def test_b11_includes_required_audit_vocabularies() -> None:
    text = b11_text()
    for term in [*AUDIT_DIMENSIONS, *AUDIT_OUTCOMES, *READINESS_STATES, *ROUTING_STRESS_TEST_FAMILIES, *OWNER_PATCH_DESTINATIONS]:
        assert term in text


def test_b11_separates_required_doctrine_principles() -> None:
    lowered = b11_text().lower()
    for phrase in [
        "integration audit is not owner-file revision",
        "conflict detection is not automatic correction",
        "gap detection is not system invention",
        "readiness does not mean finality",
        "batch b readiness does not mean canon readiness",
        "runtime readiness",
        "sourcebook readiness",
        "or that c-family schemas already exist",
        "a handoff note is not a runtime schema",
        "a doctrine-facing record is not a database contract",
        "a routing chain is not a command lifecycle",
        "a stress test is not conversion output",
        "source-local retention is not canonization",
        "quarantine is not failure",
        "human review is a lawful outcome",
        "pending schema is a lawful outcome",
    ]:
        assert phrase in lowered


def test_b11_includes_required_audit_sections_and_capstone_artifacts() -> None:
    text = b11_text()
    for marker in [
        "## 6. Batch B file inventory",
        "## 7. Batch B owner-boundary audit",
        "## 8. Cross-file dependency audit",
        "## 9. Operational handoff matrix",
        "## 10. Routing-chain verification procedure",
        "## 11. Conflict, overlap, duplicate, and owner-theft audit",
        "## 12. Missing-owner and missing-schema gap audit",
        "## 13. Source-local, quarantine, escalation, and human-review consistency audit",
        "## 14. C00/C-family handoff discipline audit",
        "## 15. Record-shape and doctrine-facing note governance audit",
        "## 16. Runtime, canon, sourcebook, and live-play boundary audit",
        "## 17. Durable test posture audit",
        "## 18. Mixed operational routing stress tests",
        "## 19. Batch C readiness gate",
        "## 20. Deferred patch ledger",
        "## 21. Batch B completion status",
    ]:
        assert marker in text


def test_b11_rejects_prohibited_downstream_ownership() -> None:
    lowered = b11_text().lower()
    for phrase in [
        "a new operational gameplay domain",
        "final mechanics",
        "final math",
        "final schemas",
        "c-family schema fields",
        "c01-c14 schema contents",
        "final runtime implementation",
        "runtime state/event/command schemas",
        "context packet schemas",
        "backend database contracts",
        "event logs",
        "save-state formats",
        "player-facing rules",
        "live-play narration behavior",
        "canon promotion",
        "sourcebook prose",
        "donor conversion output",
        "source-local system normalization",
        "registry-current authority promotion",
    ]:
        assert phrase in lowered


def test_b11_rejects_runtime_c_family_and_donor_leakage() -> None:
    lowered = b11_text().lower()
    for phrase in [
        "runtime state/event/command schemas",
        "command lifecycle",
        "must not create c01-c14 fields",
        "avoid inventing c01-c14 fields",
        "must not create c01-c14 schema contents",
        "donor/source-local material has become astra baseline without lawful routing",
        "donor element does not leak into astra baseline",
        "must not convert it into canon, final mechanics, sourcebook prose, or astra default procedure",
        "source-local donor-system containment audit",
    ]:
        assert phrase in lowered


def test_b11_includes_source_local_containment_and_lawful_fallback_outcomes() -> None:
    text = b11_text()
    for marker in [
        "Source-local donor-system containment audit",
        "source_local_retained",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
        "source-local donor boundaries",
        "Source-local retention is not canonization",
    ]:
        assert marker in text


def test_b11_references_d19_only_as_draft_source_pack_reference_material() -> None:
    text = b11_text()
    lowered = text.lower()
    for marker in [
        "D19-00_cross_pack_integration_conflict_audit_and_conversion_readiness_owner_boundaries.md",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
        "D19-01_owner_boundary_audit_conflict_taxonomy_and_cross_pack_dependency_control.md",
        "D19-02_cross_pack_handoff_matrix_dependency_chains_and_state_movement_control.md",
        "D19-06_mixed_donor_routing_stress_tests_conversion_readiness_trials_and_corpus_scale_failure_detection.md",
        "D19-07_canon_separation_runtime_separation_repo_integration_readiness_and_final_capstone_control.md",
        "D19-09_final_integration_checklists_ddr_register_and_acceptance_criteria.md",
    ]:
        assert marker in text
    assert "d-series source packs are source material only" in lowered
    assert "not current doctrine authority" in lowered
    assert "not final mechanics" in lowered


def test_b11_does_not_require_define_create_or_promote_b12_or_c01_c14() -> None:
    lowered = b11_text().lower()
    for phrase in [
        "b11 does not require, define, create, or promote b12",
        "b11 does not require, define, create, or promote b12, c01-c14",
        "b11 does not require, define, create, or promote b12, c01-c14, runtime schemas",
        "does not require, define, create, or promote b12, c01-c14, runtime schemas, canon, sourcebook prose, donor conversion output, or future gameplay subsystems",
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
    assert "- file_id: B11\n" not in registry_text
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        assert "  status: current" not in block
