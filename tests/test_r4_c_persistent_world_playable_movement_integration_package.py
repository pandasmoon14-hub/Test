from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PACKAGE = ROOT / (
    "docs/doctrine/reviews/"
    "r4_c_persistent_world_playable_movement_integration_package.yaml"
)
MANIFEST = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROGRAM = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"

EXPECTED_BASELINE = "cb3cee39c3aabce8cf0525e0d227618bf13b5d85"
EXPECTED_TREE = "e363b37401e0ff28bdec665a0eb59f72e0b91ce5"

PROPOSED_RUNTIME = (
    ROOT
    / "src/astra_runtime/domain/"
    "persistent_world_movement_integration.py"
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_r4_c_package_identity_and_definition_authority_are_exact():
    package = load(PACKAGE)

    assert package["artifact_version"] == "0.1.6"
    assert package["status"] == "merged_complete"
    assert package["package_id"] == "R4-C"
    assert (
        package["package_name"]
        == "persistent_world_playable_movement_integration"
    )
    assert (
        package["definition_authorization_reference"]
        == "owner_directive_2026-09-20_r4_c_package_definition"
    )
    assert (
        package["definition_authority_effect"]
        == "bounded_r4_c_package_definition_only"
    )
    assert package["definition_starting_baseline"] == EXPECTED_BASELINE
    assert package["definition_starting_tree"] == EXPECTED_TREE

    assert package["implementation_authorized"] is True
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False
    assert (
        package["durable_persistence_implementation_authorized"]
        is False
    )


def test_r4_c_predecessor_is_terminal_r4_b():
    package = load(PACKAGE)
    predecessor = package["predecessor"]

    assert predecessor["package_id"] == "R4-B"
    assert predecessor["required_state"] == "merged_complete"


def test_r4_c_semantic_owner_routing_is_explicit_and_nontransferring():
    package = load(PACKAGE)

    owner_refs = {
        row["owner_ref"]
        for row in package["semantic_owners"]
    }

    assert owner_refs == {
        "AFQR-01",
        "AFQR-02",
        "AFQR-03",
        "AFQR-09",
        "AFQR-18",
        "AFQR-19",
    }

    owner = package["implementation_owner"]

    assert (
        owner["proposed_runtime_path"]
        == "src/astra_runtime/domain/"
        "persistent_world_movement_integration.py"
    )
    assert owner["semantic_authority_acquired"] is False


def test_r4_c_transition_is_single_location_atomic_and_not_generalized():
    package = load(PACKAGE)
    semantics = package["transition_semantics"]

    assert semantics["command_family"] == "movement"
    assert semantics["state_delta_change_type"] == "relationship_update"
    assert semantics["narration_may_create_or_override_state"] is False
    assert (
        semantics["model_call_required_for_authoritative_resolution"]
        is False
    )

    postcondition = semantics["atomic_postcondition"]

    assert "exactly one authoritative" in postcondition
    assert "located_at(A,P2)" in postcondition
    assert "located_at(A,P1)" in postcondition

    relation_rule = semantics["relation_identity_rule"]

    assert "does not generalize relation lineage" in relation_rule
    assert "AFQR-09" in relation_rule


def test_r4_c_acceptance_criteria_are_complete_and_deterministic():
    package = load(PACKAGE)
    criteria = package["deterministic_acceptance_criteria"]

    ids = [row["criterion_id"] for row in criteria]

    assert ids == [
        f"R4C-AC-{index:03d}"
        for index in range(1, 19)
    ]

    joined = "\n".join(
        row["requirement"]
        for row in criteria
    )

    assert "movement command family" in joined
    assert "exactly one active source located_at" in joined
    assert "stale" in joined
    assert "atomically" in joined
    assert "replay" in joined
    assert "technical retry" in joined
    assert "narration" in joined
    assert "unchanged" in joined


def test_r4_c_durable_persistence_is_not_an_initial_blocker():
    package = load(PACKAGE)
    replay = package["replay_retry_recovery"]

    assert replay["bounded_deterministic_replay_required"] is True
    assert replay["durable_replay_engine_required"] is False
    assert replay["durable_persistence_required"] is False
    assert replay["technical_retry_idempotence_required"] is True
    assert (
        replay["fresh_model_interpretation_on_replay_allowed"]
        is False
    )
    assert (
        replay["committed_retry_may_duplicate_state_change"]
        is False
    )


def test_r4_c_authorized_implementation_uses_exact_runtime_allowlist():
    package = load(PACKAGE)

    allowlist = package["proposed_implementation_edit_allowlist"]

    assert allowlist["runtime_paths"] == [
        "src/astra_runtime/domain/"
        "persistent_world_movement_integration.py"
    ]
    assert allowlist["production_schema_paths"] == []

    # Authorized implementation stage: exact runtime path now exists.
    assert PROPOSED_RUNTIME.exists()


def test_r4_c_manifest_program_and_decision_log_track_same_gate():
    package = load(PACKAGE)
    manifest = load(MANIFEST)

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert manifest["artifact_version"] == "0.4.80"
    assert target["package_id"] == package["package_id"]
    assert target["package_name"] == package["package_name"]

    assert target["status"] == "merged_complete"
    assert target["implementation_authorized"] is True

    assert (
        target["implementation_state"]
        == "merged_complete"
    )

    assert target["implementation_regression_certified"] is True
    assert target["next_gate"] == "r4_c_post_merge_closure_commit_push"
    assert target["next_gate_authorized"] is False

    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

    program = PROGRAM.read_text(encoding="utf-8")
    decisions = DECISIONS.read_text(encoding="utf-8")

    assert (
        "### 5.67 R4-C persistent-world playable movement "
        "integration package definition"
        in program
    )

    assert (
        "### 5.69 R4-C playable movement implementation "
        "authorization"
        in program
    )

    assert (
        "### 5.70 R4-C implementation guardrail recovery"
        in program
    )

    assert (
        "### 5.71 R4-C implementation regression certification"
        in program
    )

    assert (
        "## 2026-09-20 decision — R4-C implementation "
        "regression certification"
        in decisions
    )

def test_r4_c_definition_regression_certification_is_exact():
    package = load(PACKAGE)

    assert package["artifact_version"] == "0.1.6"
    assert package["status"] == "merged_complete"
    assert package["definition_regression_certified"] is True

    assert (
        package["definition_recording_state"]
        == "merged_complete"
    )

    assert package["implementation_authorized"] is True
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False

    cert = package["definition_regression_certification"]

    assert cert["focused_pre_certification"] == {
        "passed": 63,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 468,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9393,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
        "result": "pass",
    }

    assert cert["focused_post_suite_certification"] == {
        "passed": 63,
        "result": "pass",
    }

    assert cert["git_diff_check"] == "clean"
    assert cert["changed_path_count"] == 6
    assert cert["production_runtime_path_count"] == 0
    assert cert["production_schema_path_count"] == 0

    lifecycle = package["downstream_lifecycle_transition"]

    assert (
        lifecycle[
            "implementation_requires_separate_owner_authorization"
        ]
        is True
    )

    assert (
        lifecycle[
            "implementation_authorization_currently_granted"
        ]
        is True
    )
def test_r4_c_implementation_authorization_is_exact_and_bounded():
    package = load(PACKAGE)
    manifest = load(MANIFEST)

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert package["artifact_version"] == "0.1.6"
    assert package["status"] == "merged_complete"
    assert package["implementation_authorized"] is True

    assert (
        package["implementation_authorization_reference"]
        == "owner_directive_2026-09-20_r4_c_implementation_authorization"
    )

    assert (
        package["implementation_authority_effect"]
        == "bounded_persistent_world_playable_movement_"
        "integration_implementation_only"
    )

    assert (
        package["implementation_starting_baseline"]
        == "9118ec2af6d4afcbf6d597186200f3fb11243776"
    )

    assert (
        package["implementation_starting_tree"]
        == "2d380f53245192a95049c607f6a66d3b634df348"
    )

    assert package["definition_pull_request"] == 431
    assert (
        package["definition_recording_state"]
        == "merged_complete"
    )

    assert (
        package["implementation_state"]
        == "merged_complete"
    )

    assert package["implementation_regression_certified"] is True

    assert (
        package["implementation_runtime_path"]
        == "src/astra_runtime/domain/"
        "persistent_world_movement_integration.py"
    )

    assert (
        package["implementation_test_path"]
        == "tests/"
        "test_r4_c_persistent_world_movement_integration.py"
    )

    assert PROPOSED_RUNTIME.exists()

    assert manifest["artifact_version"] == "0.4.80"

    assert target["implementation_authorized"] is True
    assert target["implementation_regression_certified"] is True

    assert (
        target["implementation_state"]
        == "merged_complete"
    )

    assert target["next_gate"] == "r4_c_post_merge_closure_commit_push"
    assert target["next_gate_authorized"] is False

    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False
    assert (
        package[
            "durable_persistence_implementation_authorized"
        ]
        is False
    )

    lifecycle = package[
        "downstream_lifecycle_transition"
    ]

    assert (
        lifecycle[
            "implementation_requires_separate_owner_authorization"
        ]
        is True
    )

    assert (
        lifecycle[
            "implementation_authorization_currently_granted"
        ]
        is True
    )

def test_r4_c_guardrail_recovery_scope_is_exact():
    package = load(PACKAGE)
    manifest = load(MANIFEST)

    assert package["artifact_version"] == "0.1.6"
    assert manifest["artifact_version"] == "0.4.80"

    assert (
        package["proposed_implementation_edit_allowlist"]
        ["test_infrastructure_paths_if_required"]
        == [
            "tests/runtime_domain_package_manifest.py",
            "tests/"
            "test_runtime_domain_rt_001e_"
            "action_legality_service_interface_contract_skeleton.py",
        ]
    )

    recovery = package[
        "implementation_guardrail_recovery"
    ]

    assert recovery["failed_suite_result"] == {
        "failed": 16,
        "passed": 9411,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
    }

    assert (
        recovery["repair_path"]
        == "tests/"
        "test_runtime_domain_rt_001e_"
        "action_legality_service_interface_contract_skeleton.py"
    )

    assert recovery["runtime_scope_expanded"] is False
    assert recovery["production_schema_scope_expanded"] is False
    assert recovery["semantic_authority_expanded"] is False

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert (
        target[
            "implementation_test_infrastructure_allowlist"
        ]
        == [
            "tests/runtime_domain_package_manifest.py",
            "tests/"
            "test_runtime_domain_rt_001e_"
            "action_legality_service_interface_contract_skeleton.py",
        ]
    )

    assert target["implementation_regression_certified"] is True

    assert (
        target["implementation_state"]
        == "merged_complete"
    )

    assert target["next_gate"] == "r4_c_post_merge_closure_commit_push"
    assert target["next_gate_authorized"] is False

def test_r4_c_final_implementation_certification_is_exact():
    package = load(PACKAGE)
    manifest = load(MANIFEST)

    assert package["artifact_version"] == "0.1.6"
    assert package["implementation_regression_certified"] is True

    assert (
        package["implementation_state"]
        == "merged_complete"
    )

    cert = package[
        "implementation_regression_certification"
    ]

    assert cert["repaired_rt001e_root_guardrail"] == {
        "passed": 68,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 506,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9428,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
        "result": "pass",
    }

    assert cert["focused_post_suite_certification"] == {
        "passed": 445,
        "result": "pass",
    }

    assert cert["git_diff_check"] == "clean"
    assert cert["changed_path_count"] == 10
    assert cert["production_runtime_path_count"] == 1
    assert cert["production_schema_path_count"] == 0
    assert cert["test_infrastructure_path_count"] == 2

    recovery = package["implementation_guardrail_recovery"]

    assert recovery["failed_suite_result"] == {
        "failed": 16,
        "passed": 9411,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
    }

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert target["implementation_regression_certified"] is True
    assert target["next_gate_authorized"] is False

    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False


def test_r4_c_post_merge_closure_metadata_is_exact():
    package = load(PACKAGE)
    manifest = load(MANIFEST)

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert package["artifact_version"] == "0.1.6"
    assert package["status"] == "merged_complete"
    assert package["implementation_state"] == "merged_complete"

    assert package["post_merge_closure_complete"] is True
    assert (
        package["post_merge_closure_authorization_reference"]
        == "owner_directive_2026-09-20_r4_c_post_merge_closure"
    )
    assert (
        package["post_merge_closure_authority_effect"]
        == "bounded_r4_c_post_merge_lifecycle_reconciliation_only"
    )
    assert (
        package["post_merge_closure_recorded_from"]
        == "8cb6da94894d2b8142d72c4a61fb5335135fe97e"
    )
    assert (
        package["post_merge_closure_tree"]
        == "91b486771ba2e0c85a847fe0f71e37b3c551bd32"
    )
    assert package["post_merge_closure_pull_request"] == 432
    assert (
        package["post_merge_closure_branch_head"]
        == "92e4a198b160101a188dee67f85e284ba9bd85c9"
    )
    assert package["post_merge_closure_ci_run"] == 264
    assert package["post_merge_closure_ci_run_id"] == 35553516783

    assert (
        package["post_merge_closure_regression_certified"]
        is True
    )
    assert (
        package["post_merge_closure_recording_state"]
        == "regression_certified_pending_commit"
    )

    assert manifest["artifact_version"] == "0.4.80"
    assert target["status"] == "merged_complete"
    assert target["implementation_state"] == "merged_complete"
    assert target["post_merge_closure_complete"] is True
    assert (
        target["post_merge_closure_regression_certified"]
        is True
    )
    assert (
        target["next_gate"]
        == "r4_c_post_merge_closure_commit_push"
    )
    assert target["next_gate_authorized"] is False

    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False
    assert (
        package["durable_persistence_implementation_authorized"]
        is False
    )


def test_r4_c_post_merge_closure_regression_certification_is_exact():
    package = load(PACKAGE)
    manifest = load(MANIFEST)

    assert package["artifact_version"] == "0.1.6"
    assert package["status"] == "merged_complete"
    assert package["implementation_state"] == "merged_complete"

    assert package["post_merge_closure_complete"] is True
    assert (
        package["post_merge_closure_regression_certified"]
        is True
    )

    assert (
        package["post_merge_closure_recording_state"]
        == "regression_certified_pending_commit"
    )

    cert = package[
        "post_merge_closure_regression_certification"
    ]

    assert cert["focused_pre_certification"] == {
        "passed": 446,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 507,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9432,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
        "result": "pass",
    }

    assert cert["focused_post_suite_regression"] == {
        "passed": 67,
        "result": "pass",
    }

    assert cert["git_diff_check"] == "clean"
    assert cert["changed_path_count"] == 6
    assert cert["runtime_implementation_path_count"] == 0
    assert cert["production_schema_path_count"] == 0

    recovery = package[
        "post_merge_closure_failure_recovery_evidence"
    ]

    assert recovery[
        "failed_focused_closure_certification"
    ] == {
        "failed": 4,
        "passed": 445,
        "result": "fail",
    }

    assert (
        recovery["classification"]
        == "stale_control_artifact_version_expectations"
    )

    assert recovery["r4_c_behavioral_defect_detected"] is False
    assert recovery["runtime_scope_expanded"] is False
    assert recovery["production_schema_scope_expanded"] is False
    assert recovery["semantic_authority_expanded"] is False

    second = recovery["post_recording_validation_recovery"]

    assert second[
        "failed_focused_post_recording_validation"
    ] == {
        "failed": 4,
        "passed": 65,
        "result": "fail",
    }

    assert (
        second["classification"]
        == "stale_control_artifact_version_expectations_"
        "after_certification_recording"
    )

    assert second["r4_c_behavioral_defect_detected"] is False
    assert second["runtime_scope_expanded"] is False
    assert second["production_schema_scope_expanded"] is False
    assert second["semantic_authority_expanded"] is False
    assert second["full_repository_rerun_required"] is False

    target = manifest[
        "r4_c_playable_movement_integration_target"
    ]

    assert manifest["artifact_version"] == "0.4.80"

    assert target["post_merge_closure_complete"] is True
    assert (
        target["post_merge_closure_regression_certified"]
        is True
    )

    assert (
        target["post_merge_closure_recording_state"]
        == "regression_certified_pending_commit"
    )

    assert (
        target["next_gate"]
        == "r4_c_post_merge_closure_commit_push"
    )

    assert target["next_gate_authorized"] is False

    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False

    assert (
        package["durable_persistence_implementation_authorized"]
        is False
    )
