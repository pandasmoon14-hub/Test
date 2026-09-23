from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "docs/doctrine/reviews/r4_e_persistent_world_object_custody_transfer_package.yaml"
MANIFEST = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROGRAM = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_r4_e_identity_and_authorization_boundary_are_exact():
    package = load(PACKAGE)
    assert package["artifact_version"] == "0.1.5"
    assert package["status"] == "merged_complete"
    assert package["package_id"] == "R4-E"
    assert package["package_name"] == "persistent_world_object_custody_transfer"
    assert package["implementation_authorized"] is True
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False
    assert package["production_schema_implementation_authorized"] is False


def test_r4_e_predecessor_is_merged_r4_d_without_historical_rewrite():
    predecessor = load(PACKAGE)["predecessor"]
    assert predecessor["package_id"] == "R4-D"
    assert predecessor["required_status"] == "merged_complete"
    assert predecessor["required_implementation_state"] == "merged_complete"
    assert predecessor["post_merge_closure_merge_commit"] == "c9810357d4367a78771e083d3978913799d292d5"
    assert predecessor["historical_self_referential_lifecycle_values_rewritten"] is False


def test_r4_e_carried_by_is_rt010_asset_placement_not_ownership():
    package = load(PACKAGE)
    custody = package["custody_semantics"]
    assert custody["authoritative_relation_type"] == "carried_by"
    assert custody["semantic_owner"] == "RT-010"
    assert custody["subject_required_classification"] == "object"
    assert custody["carrier_required_classification"] == "character_or_creature"
    assert custody["generalized_relation_registry_created"] is False
    forbidden = set(custody["does_not_establish"])
    assert {"ownership", "legal entitlement", "agency", "knowledge", "visibility"} <= forbidden


def test_r4_e_rt007_afqr09_and_storage_boundaries_remain_separate():
    owners = load(PACKAGE)["semantic_owner_boundary"]
    assert "RT-010" in owners
    assert "RT-007" in owners
    assert "AFQR-09" in owners
    assert "social, factional, institutional, disputed" in owners["RT-007"]
    assert "no ownership" in owners["AFQR-09"]
    assert owners["storage_or_serialization_transfers_semantic_ownership"] is False


def test_r4_e_immediate_placement_invariant_is_bounded():
    invariant = load(PACKAGE)["immediate_placement_invariant"]
    assert invariant["direct_mode"] == "O located_at P"
    assert invariant["carried_mode"] == "O carried_by A"
    assert invariant["simultaneous_direct_and_carried_allowed"] is False
    assert invariant["multiple_active_carried_by_allowed"] is False
    assert invariant["universal_all_objects_requirement_created"] is False
    assert invariant["drop_destination"] == "derive P from carrier A current located_at relation"


def test_r4_e_state_composition_is_minimum_and_owner_separated():
    state = load(PACKAGE)["state_composition"]
    assert state["proposed_state_type"] == "PersistentWorldObjectCustodyRuntimeState"
    assert state["movement_semantics_remain_r4_c_owned"] is True
    assert state["custody_evidence_separate_from_movement_evidence"] is True
    assert state["movement_storage_acquires_custody_semantics"] is False
    assert state["persistence_storage_acquires_custody_semantics"] is False
    assert state["universal_world_state_manager_created"] is False


def test_r4_e_command_routing_reuses_inventory_without_closed_menu():
    routing = load(PACKAGE)["command_routing"]
    assert routing["required_existing_family"] == "inventory"
    assert routing["candidate_command_types"] == ["pickup_object", "drop_object"]
    assert routing["existing_prefixes_reused"] == ["pickup", "drop"]
    assert routing["generic_inventory_default_owner_route_is_not_custody_semantic_ownership"] is True
    assert routing["closed_action_menu_created"] is False
    assert routing["freeform_interpretation_preserved"] is True


def test_r4_e_checkpoint_plan_preserves_r4_d_v1_meaning():
    checkpoint = load(PACKAGE)["checkpoint_compatibility_plan"]
    assert checkpoint["existing_r4_d_format_identity"] == "myravant.r4d.persistent_world_movement_checkpoint"
    assert checkpoint["existing_r4_d_format_version"] == 1
    assert checkpoint["existing_r4_d_format_meaning_changes"] is False
    assert checkpoint["existing_r4_d_reader_remains_available"] is True
    assert checkpoint["proposed_r4_e_format_identity"] == "myravant.r4e.persistent_world_object_custody_checkpoint"
    assert checkpoint["movement_only_r4_d_checkpoint_remains_readable"] is True
    assert checkpoint["silent_unknown_format_upgrade_allowed"] is False
    assert checkpoint["generalized_migration_framework_created"] is False


def test_r4_e_acceptance_sequence_and_final_state_are_exact():
    package = load(PACKAGE)
    assert len(package["acceptance_sequence"]) == 20
    assert package["acceptance_sequence"][0] == "initial:A located_at P1"
    assert package["acceptance_sequence"][1] == "initial:O located_at P1"
    assert package["acceptance_sequence"][-1] == "final:O located_at P2 and O not carried_by A"
    final_state = package["required_final_authoritative_state"]
    assert final_state["actor_location"] == "A located_at P2"
    assert final_state["object_location"] == "O located_at P2"
    assert final_state["object_carried_by_actor"] is False
    assert final_state["deterministic_reproducibility_required"] is True


def test_r4_e_definition_edit_allowlist_is_exact():
    assert set(load(PACKAGE)["definition_edit_allowlist"]) == {
        "docs/decisions/current_decisions_log.md",
        "docs/doctrine/control/post_r2a_transition_manifest.yaml",
        "docs/doctrine/control/post_r2a_transition_program.md",
        "docs/doctrine/reviews/r4_e_persistent_world_object_custody_transfer_package.yaml",
        "tests/test_post_r2a_transition_program.py",
        "tests/test_r4_c_persistent_world_playable_movement_integration_package.py",
        "tests/test_r4_d_persistent_world_local_checkpoint_restore_package.py",
        "tests/test_r4_e_persistent_world_object_custody_transfer_package.py",
    }


def test_r4_e_proposed_runtime_scope_is_bounded():
    allowlist = load(PACKAGE)["proposed_implementation_edit_allowlist"]
    assert allowlist["runtime_paths"] == [
        "src/astra_runtime/domain/persistent_world_entity_location_representation.py",
        "src/astra_runtime/domain/persistent_world_object_custody_transfer.py",
        "src/astra_runtime/domain/persistent_world_local_checkpoint_restore.py",
    ]
    assert allowlist["production_schema_paths"] == []
    assert "src/astra_runtime/domain/persistent_world_movement_integration.py" in allowlist["explicitly_not_required_on_current_evidence"]
    assert "src/astra_runtime/domain/command_kind_routing_skeleton.py" in allowlist["explicitly_not_required_on_current_evidence"]


def test_r4_e_definition_authorization_and_implementation_are_merged_before_closure_commit():
    package = load(PACKAGE)
    assert package["definition_regression_certified"] is True
    assert package["definition_recording_state"] == "merged_complete"
    assert package["definition_post_merge_closure_complete"] is True
    assert package["definition_post_merge_closure_regression_certified"] is True
    assert package["definition_post_merge_closure_recording_state"] == "merged_complete"
    assert package["definition_post_merge_closure_record_pull_request"] == 441
    assert package["definition_post_merge_closure_record_merge_commit"] == "55461eb5ab9ac373cca9fa7b978ce71d0a11669c"
    assert package["implementation_authorized"] is True
    assert package["implementation_authorization_recording_state"] == "merged_complete"
    assert package["implementation_regression_certified"] is True
    assert package["status"] == "merged_complete"
    assert package["implementation_state"] == "merged_complete"
    assert package["implementation_certification_recording_state"] == "merged_complete"
    assert package["implementation_cross_platform_ci_certified"] is True
    assert package["post_merge_closure_complete"] is True

def test_r4_e_manifest_target_matches_package_and_control_version():
    package = load(PACKAGE)
    manifest = load(MANIFEST)
    assert manifest["artifact_version"] == "0.4.90"
    target = manifest["r4_e_object_custody_transfer_target"]
    assert target["package_id"] == package["package_id"]
    assert target["package_name"] == package["package_name"]
    assert target["status"] == "merged_complete"
    assert target["definition_recording_state"] == "merged_complete"
    assert target["definition_post_merge_closure_complete"] is True
    assert target["definition_post_merge_closure_recording_state"] == "merged_complete"
    assert target["implementation_authorized"] is True
    assert target["implementation_state"] == "merged_complete"
    assert target["implementation_certification_recording_state"] == "merged_complete"
    assert target["implementation_cross_platform_ci_certified"] is True
    assert target["post_merge_closure_complete"] is True
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False
    assert target["custody_relation_type"] == "carried_by"
    assert target["bounded_asset_placement_owner"] == "RT-010"
    assert target["social_or_disputed_custody_handoff"] == "RT-007"
    assert target["custody_implies_ownership"] is False
    assert target["definition_regression_certified"] == package["definition_regression_certified"]
    assert target["next_gate"] == package["next_gate"]
    assert target["next_gate_authorized"] == package["next_gate_authorized"]

def test_r4_e_program_and_decision_log_record_definition_boundary():
    program = PROGRAM.read_text(encoding="utf-8")
    decisions = DECISIONS.read_text(encoding="utf-8")
    assert "**Artifact version:** `0.4.90`" in program
    assert "### 5.92 R4-E persistent-world object custody transfer package definition" in program
    assert "R4-E-DEFINITION-001" in decisions
    assert "R4-E-DEFINITION-POST-MERGE-CLOSURE-004" in decisions
    assert "### 5.94 R4-E definition post-merge lifecycle closure" in program
    assert "R4-E implementation remains unauthorized." in program
    assert "General R4 activation remains unauthorized." in program


def test_r4_e_definition_post_merge_evidence_is_exact():
    package = load(PACKAGE)
    assert package["definition_post_merge_closure_recorded_from"] == "5111b8dd8e60fbbb44d07695e68863bf943320e9"
    assert package["definition_post_merge_closure_tree"] == "27f43e88eacd8a4626b1746118b46e97d811ae43"
    assert package["definition_post_merge_closure_pull_request"] == 439
    assert package["definition_post_merge_closure_branch_head"] == "b21cc58c16d1146a003b383ff759cfd8495ff5e4"
    assert package["definition_post_merge_closure_ci_run"] == 279
    assert package["definition_post_merge_closure_ci_run_id"] == 35687577058
    ci = package["definition_post_merge_closure_ci_verification"]
    assert ci["core_linux"]["job_id"] == 106617609047
    assert ci["core_linux"]["conclusion"] == "success"
    assert ci["core_windows"]["job_id"] == 106617609189
    assert ci["core_windows"]["conclusion"] == "success"
    assert ci["cross_platform_ci_certified"] is True


def test_r4_e_implementation_authorization_boundary_is_exact():
    package = load(PACKAGE)
    assert package["implementation_authorized"] is True
    assert package["implementation_state"] == "merged_complete"
    assert package["implementation_authorization_recording_state"] == "merged_complete"
    assert package["implementation_certification_recording_state"] == "merged_complete"
    assert package["production_schema_implementation_authorized"] is False
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False
    assert len(package["definition_post_merge_closure_edit_allowlist"]) == 8
    assert package["implementation_authority_effect"] == "bounded_persistent_world_object_custody_transfer_implementation_only"

def test_r4_e_authorized_implementation_allowlist_and_validation_bar_are_exact():
    package = load(PACKAGE)
    allow = package["authorized_implementation_edit_allowlist"]
    assert allow["runtime_paths"] == [
        "src/astra_runtime/domain/persistent_world_entity_location_representation.py",
        "src/astra_runtime/domain/persistent_world_object_custody_transfer.py",
        "src/astra_runtime/domain/persistent_world_local_checkpoint_restore.py",
    ]
    assert allow["production_schema_paths"] == []
    requirements = package["implementation_validation_requirements"]
    assert len(requirements) == 18
    assert [x["requirement_id"] for x in requirements] == [f"R4E-IV-{i:03d}" for i in range(1, 19)]
    names = {x["name"] for x in requirements}
    assert {"pickup_authoritative_transition","movement_preserves_custody","drop_authoritative_transition","custody_checkpoint_round_trip","post_restore_continue_play","second_checkpoint_final_state","semantic_noncollapse","no_generalized_inventory_or_world_manager"} <= names


def test_r4_e_implementation_post_merge_closure_lifecycle_is_exact():
    package = load(PACKAGE)
    assert package["implementation_authorization_regression_certified"] is True
    assert package["implementation_authorization_recording_state"] == "merged_complete"
    assert package["implementation_authorization_pull_request"] == 444
    assert package["implementation_regression_certified"] is True
    assert package["implementation_state"] == "merged_complete"
    assert package["implementation_certification_recording_state"] == "merged_complete"
    assert package["implementation_cross_platform_ci_certified"] is True
    assert package["implementation_branch_head"] == "0b80245b8eb051642bac6fea21950c0dd831e227"
    assert package["implementation_merge_commit"] == "f5a6f94615045649fd29881223512dd88ee9b170"
    assert package["implementation_merge_tree"] == "63daaf63055d947756f51b4402aae96262424886"
    assert package["implementation_ci_run"] == 293
    assert package["implementation_ci_run_id"] == 35777626182
    assert package["post_merge_closure_complete"] is True
    assert package["post_merge_closure_pull_request"] == 445
    assert package["post_merge_closure_branch_head"] == "0b80245b8eb051642bac6fea21950c0dd831e227"
    assert package["post_merge_closure_recorded_from"] == "f5a6f94615045649fd29881223512dd88ee9b170"
    assert package["post_merge_closure_tree"] == "63daaf63055d947756f51b4402aae96262424886"
    if package["post_merge_closure_regression_certified"] is False:
        assert package["post_merge_closure_recording_state"] == "pending_regression_certification"
        assert package["next_gate"] == "r4_e_post_merge_closure_regression_certification"
        assert package["next_gate_authorized"] is True
    else:
        assert package["post_merge_closure_recording_state"] == "regression_certified_pending_commit"
        assert package["next_gate"] == "r4_e_post_merge_closure_commit_push"
        assert package["next_gate_authorized"] is False
        cert = package["post_merge_closure_regression_certification"]
        assert cert["focused_closure"]["result"] == "pass"
        assert cert["broader_pr2_r4"]["result"] == "pass"
        assert cert["full_repository"]["result"] == "pass"
        assert cert["runtime_implementation_path_count"] == 0
        assert cert["production_schema_path_count"] == 0

def test_r4_e_implementation_completion_proof_is_bounded():
    package = load(PACKAGE)
    proof = package["implementation_completion_proof"]
    assert proof["pickup_removes_direct_location_and_adds_carried_by"] is True
    assert proof["r4_c_movement_preserves_custody_relation"] is True
    assert proof["true_process_boundary_restore"] is True
    assert proof["continued_drop_after_restore"] is True
    assert proof["second_checkpoint_second_restore"] is True
    assert proof["r4d_v1_meaning_preserved"] is True
    assert proof["generalized_inventory_created"] is False
    assert proof["ownership_semantics_created"] is False
    assert proof["production_schema_changed"] is False


def test_r4_e_implementation_post_merge_ci_evidence_is_exact():
    package = load(PACKAGE)
    ci = package["implementation_cross_platform_ci_certification"]
    assert ci["pull_request"] == 445
    assert ci["implementation_head"] == "0b80245b8eb051642bac6fea21950c0dd831e227"
    assert ci["workflow_run_number"] == 293
    assert ci["workflow_run_id"] == 35777626182
    assert ci["core_linux"] == {
        "job_id": 106914739340,
        "conclusion": "success",
    }
    assert ci["core_windows"] == {
        "job_id": 106914739707,
        "conclusion": "success",
    }
    assert ci["cross_platform_ci_certified"] is True
    assert ci["result"] == "pass"

def test_r4_e_post_merge_closure_initial_recording_recovery_is_preserved():
    package = load(PACKAGE)
    manifest = load(MANIFEST)
    target = manifest["r4_e_object_custody_transfer_target"]
    for obj in (package, target):
        evidence = obj["post_merge_closure_failure_recovery_evidence"]
        recovery = evidence["initial_recording_eof_whitespace"]
        assert recovery["classification"] == "r4_e_post_merge_closure_initial_recording_eof_whitespace_defect"
        assert recovery["behavioral_execution_reached"] is False
        assert recovery["runtime_behavioral_defect_detected"] is False
        assert recovery["runtime_semantic_defect_detected"] is False
        assert recovery["runtime_scope_expanded"] is False
        assert recovery["production_schema_scope_expanded"] is False
        assert recovery["semantic_authority_expanded"] is False
        assert recovery["result"] == "recovered"

def test_r4_e_post_merge_closure_focused_lifecycle_recovery_is_preserved():
    package = load(PACKAGE)
    manifest = load(MANIFEST)
    target = manifest["r4_e_object_custody_transfer_target"]
    for obj in (package, target):
        evidence = obj["post_merge_closure_failure_recovery_evidence"]
        recovery = evidence["focused_current_lifecycle_expectation_alignment"]
        assert recovery["failed_focused_closure_certification"] == {
            "passed": 81,
            "failed": 2,
            "result": "fail",
        }
        assert recovery["classification"] == "r4_e_post_merge_closure_stale_current_lifecycle_expectations"
        assert recovery["stale_current_assertion_count"] == 4
        assert recovery["authoritative_status"] == "merged_complete"
        assert recovery["stale_status"] == "implementation_authorized"
        assert recovery["authoritative_implementation_state"] == "merged_complete"
        assert recovery["stale_implementation_state"] == "regression_certified_pending_commit"
        assert recovery["historical_lifecycle_evidence_rewritten"] is False
        assert recovery["runtime_behavioral_defect_detected"] is False
        assert recovery["runtime_semantic_defect_detected"] is False
        assert recovery["cross_platform_ci_invalidated"] is False
        assert recovery["runtime_scope_expanded"] is False
        assert recovery["production_schema_scope_expanded"] is False
        assert recovery["semantic_authority_expanded"] is False
        assert recovery["regression_certification_restart_required"] is True
        assert recovery["result"] == "recovered"

def test_r4_e_post_merge_closure_post_recording_eof_recovery_is_preserved():
    package = load(PACKAGE)
    manifest = load(MANIFEST)
    target = manifest["r4_e_object_custody_transfer_target"]
    for obj in (package, target):
        recovery = obj["post_merge_closure_failure_recovery_evidence"]["post_recording_eof_whitespace"]
        assert recovery["classification"] == "r4_e_post_merge_closure_post_recording_eof_whitespace_defect"
        assert recovery["full_repository_certification_completed"] is True
        assert recovery["full_repository_result"] == {
            "passed": 9586,
            "skipped": 10,
            "xfailed": 2,
            "warnings": 1,
            "result": "pass",
        }
        assert recovery["certification_invalidated"] is False
        assert recovery["full_repository_rerun_required"] is False
        assert recovery["post_recording_validation_required"] is True
        assert recovery["runtime_behavioral_defect_detected"] is False
        assert recovery["runtime_semantic_defect_detected"] is False
        assert recovery["cross_platform_ci_invalidated"] is False
        assert recovery["runtime_scope_expanded"] is False
        assert recovery["production_schema_scope_expanded"] is False
        assert recovery["semantic_authority_expanded"] is False
        assert recovery["result"] == "recovered"
