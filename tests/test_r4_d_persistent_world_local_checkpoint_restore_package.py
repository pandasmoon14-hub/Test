from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PACKAGE = (
    ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "r4_d_persistent_world_local_checkpoint_restore_package.yaml"
)

MANIFEST = (
    ROOT
    / "docs"
    / "doctrine"
    / "control"
    / "post_r2a_transition_manifest.yaml"
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_r4_d_identity_baseline_and_status_are_exact():
    package = load(PACKAGE)

    assert package["artifact_version"] == "0.1.2"
    assert package["package_id"] == "R4-D"

    assert (
        package["package_name"]
        == "persistent_world_local_checkpoint_restore"
    )

    assert (
        package["status"]
        == "implementation_authorized"
    )


def test_r4_d_implementation_authorization_does_not_activate_r4():
    package = load(PACKAGE)

    assert package["implementation_authorized"] is True
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False

    assert (
        package[
            "production_schema_implementation_authorized"
        ]
        is False
    )


def test_r4_d_consumes_existing_persistence_authority():
    package = load(PACKAGE)

    contract = package["persistence_contract"]

    assert contract["contract_ref"] == "PR2-PERSIST"

    assert (
        contract["carried_handoff"]
        == "PR2-TEST-HANDOFF-PERSIST-001"
    )

    assert (
        contract["storage_acquires_semantic_ownership"]
        is False
    )

    assert (
        contract["checkpoint_materialization_is_commitment"]
        is False
    )

    assert (
        contract["restore_is_new_semantic_execution"]
        is False
    )


def test_r4_d_state_store_remains_non_dependency():
    package = load(PACKAGE)

    dependency = next(
        row
        for row in package["dependencies"]
        if row["ref"] == "astra_runtime.domain.state_store"
    )

    assert dependency["kind"] == "explicit_non_dependency"

    assert (
        package["implementation_owner"][
            "semantic_authority_acquired"
        ]
        is False
    )


def test_r4_d_proposed_implementation_surface_is_exact():
    package = load(PACKAGE)

    allowlist = package[
        "proposed_implementation_edit_allowlist"
    ]

    assert allowlist["runtime"] == [
        (
            "src/astra_runtime/domain/"
            "persistent_world_local_checkpoint_restore.py"
        )
    ]

    assert allowlist["production_schema"] == []


def test_r4_d_checkpoint_boundary_is_fail_closed():
    package = load(PACKAGE)

    semantics = package["checkpoint_semantics"]

    assert (
        semantics[
            "checkpoint_requires_explicit_afqr01_qualification"
        ]
        is True
    )

    assert semantics["caller_supplies_storage_path"] is True
    assert semantics["global_save_directory_defined"] is False
    assert semantics["canonical_serialization_required"] is True
    assert semantics["integrity_digest_required"] is True

    assert (
        semantics[
            "failed_write_may_replace_prior_valid_checkpoint"
        ]
        is False
    )

    assert (
        semantics[
            "model_or_narration_may_reconstruct_missing_state"
        ]
        is False
    )

    assert (
        semantics[
            "uncheckpointed_state_claimed_crash_recoverable"
        ]
        is False
    )


def test_r4_d_acceptance_criteria_are_complete_and_unique():
    package = load(PACKAGE)

    criteria = package["deterministic_acceptance_criteria"]

    assert len(criteria) == 21

    ids = [row["criterion_id"] for row in criteria]

    assert len(ids) == len(set(ids))
    assert ids[0] == "R4D-AC-001"
    assert ids[-1] == "R4D-AC-021"


def test_r4_d_broader_persistence_authority_is_prohibited():
    package = load(PACKAGE)

    prohibited = set(package["prohibited_scope"])

    required = {
        "modify state_store.py into a mutable persistence service",
        "create a generalized persistence manager",
        "create a generalized event journal",
        "create generalized replay infrastructure",
        "mandate a database",
        "define timeline identity from checkpoint identity",
        "define branch identity from checkpoint identity",
        "define canonicality from newest checkpoint",
        "claim recovery of state that was never checkpointed",
        "allow a model to repair missing authoritative state",
        "authorize R4 activation",
        "authorize runtime promotion",
    }

    assert required <= prohibited


def test_r4_d_manifest_matches_package_definition():
    package = load(PACKAGE)
    manifest = load(MANIFEST)

    assert manifest["artifact_version"] == "0.4.80"

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert target["package_id"] == package["package_id"]
    assert target["package_name"] == package["package_name"]
    assert target["implementation_authorized"] is True

    assert (
        target["next_gate"]
        == "r4_d_implementation_authorization_commit_push"
    )

    assert target["next_gate_authorized"] is False

def test_r4_d_definition_regression_certification_is_exact():
    package = load(PACKAGE)

    assert package["artifact_version"] == "0.1.2"
    assert package["status"] == "implementation_authorized"

    assert package["definition_regression_certified"] is True

    assert (
        package["definition_recording_state"]
        == "merged_complete"
    )

    evidence = package[
        "definition_regression_certification"
    ]

    assert evidence["focused_pre_certification"] == {
        "passed": 123,
        "result": "pass",
    }

    assert evidence["broader_pr2_r4_regression"] == {
        "passed": 519,
        "result": "pass",
    }

    assert evidence["full_repository_suite"] == {
        "passed": 9444,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": (
            "existing_nonblocking_deprecation"
        ),
        "result": "pass",
    }

    assert (
        evidence["focused_post_suite_certification"]
        == {
            "passed": 49,
            "result": "pass",
        }
    )

    assert evidence["git_diff_check"] == "clean"
    assert evidence["changed_path_count"] == 7
    assert evidence["production_runtime_path_count"] == 0
    assert evidence["production_schema_path_count"] == 0

    assert package["implementation_authorized"] is True
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False



def test_r4_d_definition_recording_recovery_evidence_is_exact():
    package = load(PACKAGE)

    recovery = package[
        "definition_recording_failure_recovery_evidence"
    ]

    assert recovery[
        "failed_focused_post_recording_validation"
    ] == {
        "failed": 1,
        "passed": 50,
        "result": "fail",
    }

    assert (
        recovery["classification"]
        == (
            "stale_r4_d_next_gate_expectation_"
            "after_certification_recording"
        )
    )

    assert recovery[
        "r4_d_behavioral_defect_detected"
    ] is False

    assert recovery["runtime_scope_expanded"] is False

    assert (
        recovery["production_schema_scope_expanded"]
        is False
    )

    assert (
        recovery["semantic_authority_expanded"]
        is False
    )

    assert (
        recovery["full_repository_rerun_required"]
        is False
    )

    assert package["implementation_authorized"] is True
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False



def test_r4_d_secondary_authorization_recovery_evidence_is_exact():
    package = load(PACKAGE)

    recovery = package[
        "definition_recording_failure_recovery_evidence"
    ]["secondary_root_seam_failure"]

    assert recovery["failed"] == 1
    assert recovery["passed"] == 2
    assert recovery["result"] == "fail"

    assert (
        recovery["classification"]
        == (
            "stale_r4_d_next_gate_authorization_expectation_"
            "after_certification_recording"
        )
    )

    assert recovery["observed_authoritative_value"] is False
    assert recovery["stale_expected_value"] is True
    assert recovery["r4_d_behavioral_defect_detected"] is False
    assert recovery["runtime_scope_expanded"] is False
    assert recovery["production_schema_scope_expanded"] is False
    assert recovery["semantic_authority_expanded"] is False
    assert recovery["full_repository_rerun_required"] is False



def test_r4_d_definition_post_merge_closure_is_exact_and_bounded():
    package = load(PACKAGE)
    manifest = load(MANIFEST)

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert package["artifact_version"] == "0.1.2"
    assert manifest["artifact_version"] == "0.4.80"

    assert package["status"] == "implementation_authorized"
    assert target["status"] == "implementation_authorized"

    assert package["definition_recording_state"] == "merged_complete"
    assert target["definition_recording_state"] == "merged_complete"

    assert (
        package["definition_post_merge_closure_complete"]
        is True
    )

    assert (
        target["definition_post_merge_closure_complete"]
        is True
    )

    assert (
        target["definition_post_merge_closure_recorded_from"]
        == "3cf57fb816e51610c98258399ae11267abd2c1f5"
    )

    assert (
        target["definition_post_merge_closure_tree"]
        == "5674c05bd8d216373925ac5151a965acec6e72ec"
    )

    assert target["definition_post_merge_closure_pull_request"] == 434

    assert (
        target["definition_post_merge_closure_branch_head"]
        == "f453dde3ae2046a88048291f2f9b79c6b3406f52"
    )

    assert target["definition_post_merge_closure_ci_run"] == 268

    assert (
        target["definition_post_merge_closure_ci_run_id"]
        == 35608929257
    )

    assert (
        target[
            "definition_post_merge_closure_regression_certified"
        ]
        is True
    )

    assert (
        target[
            "definition_post_merge_closure_recording_state"
        ]
        == "merged_complete"
    )

    assert (
        target["next_gate"]
        == "r4_d_implementation_authorization_commit_push"
    )

    assert target["next_gate_authorized"] is False

    assert target["implementation_authorized"] is True
    assert target["implementation_state"] == "authorized_pending_implementation"
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_authorized"] is False

def test_r4_d_definition_closure_key_recovery_evidence_is_exact():
    package = load(PACKAGE)

    recovery = package[
        "definition_post_merge_closure_failure_recovery_evidence"
    ]

    assert recovery[
        "failed_focused_closure_certification"
    ] == {
        "failed": 1,
        "passed": 64,
        "result": "fail",
    }

    assert (
        recovery["classification"]
        == (
            "accidental_test_key_rewrite_during_"
            "definition_closure_lifecycle_alignment"
        )
    )

    assert (
        recovery[
            "authoritative_persistent_boolean_key"
        ]
        == "package_defined"
    )

    assert (
        recovery["lifecycle_status"]
        == "definition_merged_complete"
    )

    assert recovery[
        "r4_d_behavioral_defect_detected"
    ] is False

    assert recovery["runtime_scope_expanded"] is False

    assert (
        recovery[
            "production_schema_scope_expanded"
        ]
        is False
    )

    assert (
        recovery["semantic_authority_expanded"]
        is False
    )

    assert (
        recovery[
            "closure_certification_restart_required"
        ]
        is True
    )



def test_r4_d_definition_post_merge_closure_certification_is_exact():
    package = load(PACKAGE)

    assert (
        package[
            "definition_post_merge_closure_regression_certified"
        ]
        is True
    )

    assert (
        package[
            "definition_post_merge_closure_recording_state"
        ]
        == "merged_complete"
    )

    cert = package[
        "definition_post_merge_closure_regression_certification"
    ]

    assert cert[
        "certification_restart_after_test_key_recovery"
    ] is True

    assert cert["focused_pre_certification"] == {
        "passed": 67,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 528,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9453,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": (
            "existing_nonblocking_deprecation"
        ),
        "result": "pass",
    }

    assert cert["focused_post_suite_regression"] == {
        "passed": 58,
        "result": "pass",
    }

    assert cert["git_diff_check"] == "clean"
    assert cert["changed_path_count"] == 7
    assert cert["runtime_implementation_path_count"] == 0
    assert cert["production_schema_path_count"] == 0

    assert (
        package["next_gate"]
        == "r4_d_implementation_authorization_commit_push"
    )

    assert package["next_gate_authorized"] is False
    assert package["implementation_authorized"] is True
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False



def test_r4_d_closure_post_recording_recovery_evidence_is_exact():
    package = load(PACKAGE)

    recovery = package[
        "definition_post_merge_closure_failure_recovery_evidence"
    ]["post_recording_validation_recovery"]

    assert recovery[
        "failed_focused_post_recording_validation"
    ] == {
        "failed": 6,
        "passed": 54,
        "result": "fail",
    }

    assert (
        recovery["classification"]
        == (
            "stale_closure_certification_state_expectations_"
            "after_evidence_recording"
        )
    )

    assert (
        recovery["authoritative_next_gate"]
        == "r4_d_definition_post_merge_closure_commit_push"
    )

    assert (
        recovery["authoritative_next_gate_authorized"]
        is False
    )

    assert (
        recovery[
            "authoritative_closure_regression_certified"
        ]
        is True
    )

    assert recovery[
        "r4_d_behavioral_defect_detected"
    ] is False

    assert recovery["runtime_scope_expanded"] is False
    assert recovery["production_schema_scope_expanded"] is False
    assert recovery["semantic_authority_expanded"] is False
    assert recovery["full_repository_rerun_required"] is False



def test_r4_d_implementation_authorization_is_exact():
    package = load(PACKAGE)

    assert package["artifact_version"] == "0.1.2"
    assert package["status"] == "implementation_authorized"
    assert package["implementation_authorized"] is True

    assert (
        package["implementation_state"]
        == "authorized_pending_implementation"
    )

    assert (
        package[
            "implementation_authorization_regression_certified"
        ]
        is True
    )

    assert (
        package[
            "implementation_authorization_recording_state"
        ]
        == "regression_certified_pending_commit"
    )

    assert package["implementation_regression_certified"] is False

    assert (
        package["next_gate"]
        == "r4_d_implementation_authorization_commit_push"
    )

    assert package["next_gate_authorized"] is False
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False

def test_r4_d_continue_play_after_restore_is_explicit():
    package = load(PACKAGE)

    criteria = {
        row["criterion_id"]: row
        for row in package["deterministic_acceptance_criteria"]
    }

    assert "R4D-AC-021" in criteria

    requirement = criteria[
        "R4D-AC-021"
    ]["requirement"]

    assert "original in-memory runtime state discarded" in requirement
    assert "completely new lawful movement transition" in requirement
    assert "checkpoint again" in requirement
    assert "restore again" in requirement


def test_r4_d_implementation_validation_matrix_is_exact():
    package = load(PACKAGE)

    rows = package["implementation_validation_requirements"]

    ids = [row["requirement_id"] for row in rows]

    assert ids == [
        "R4D-IV-001",
        "R4D-IV-002",
        "R4D-IV-003",
        "R4D-IV-004",
        "R4D-IV-005",
        "R4D-IV-006",
        "R4D-IV-007",
        "R4D-IV-008",
        "R4D-IV-009",
        "R4D-IV-010",
        "R4D-IV-011",
        "R4D-IV-012",
        "R4D-IV-013",
    ]

    names = {
        row["name"]
        for row in rows
    }

    assert {
        "continue_play_after_restore",
        "true_process_boundary_round_trip",
        "complete_r4_c_authoritative_evidence_preservation",
        "strict_checkpoint_envelope_validation",
        "atomic_checkpoint_replacement",
        "corruption_fail_closed_matrix",
        "post_restore_retry_identity",
        "multiple_committed_transition_preservation",
        "restore_then_checkpoint_determinism",
        "storage_order_is_not_causal_order",
        "bounded_replay_claim",
        "operational_local_durability_boundary",
        "offline_no_model_dependency",
    } == names


def test_r4_d_envelope_and_corruption_matrix_are_exact():
    package = load(PACKAGE)

    assert package["required_checkpoint_envelope_fields"] == [
        "format_identity",
        "format_version",
        "campaign_identity",
        "authoritative_payload",
        "integrity_digest",
        "qualification_provenance",
    ]

    assert package["required_corruption_cases"] == [
        "truncated_file",
        "malformed_serialization",
        "integrity_digest_mismatch",
        "unsupported_format_version",
        "incorrect_campaign_identity",
        "missing_committed_transition",
        "altered_command_fingerprint",
        "altered_movement_receipt",
        "altered_state_delta",
        "receipt_state_delta_disagreement",
        "duplicate_command_identity",
        "invalid_entity_or_location_reference",
    ]



def test_r4_d_implementation_authorization_certification_is_exact():
    package = load(PACKAGE)

    assert (
        package[
            "implementation_authorization_regression_certified"
        ]
        is True
    )

    assert (
        package[
            "implementation_authorization_recording_state"
        ]
        == "regression_certified_pending_commit"
    )

    cert = package[
        "implementation_authorization_regression_certification"
    ]

    assert cert[
        "focused_authorization_certification"
    ] == {
        "passed": 76,
        "result": "pass",
    }

    assert cert["broader_pr2_r4_regression"] == {
        "passed": 537,
        "result": "pass",
    }

    assert cert["full_repository_suite"] == {
        "passed": 9462,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": (
            "existing_nonblocking_deprecation"
        ),
        "result": "pass",
    }

    assert cert[
        "focused_post_suite_confirmation"
    ] == {
        "passed": 67,
        "result": "pass",
    }

    assert cert["git_diff_check"] == "clean"
    assert cert["changed_path_count"] == 7
    assert cert["production_runtime_path_count"] == 0
    assert cert["production_schema_path_count"] == 0

    assert (
        cert["deterministic_acceptance_criteria_count"]
        == 21
    )

    assert (
        cert[
            "implementation_validation_requirement_count"
        ]
        == 13
    )

    assert (
        package["next_gate"]
        == "r4_d_implementation_authorization_commit_push"
    )

    assert package["next_gate_authorized"] is False

    # Authorization is certified; implementation is not.
    assert package["implementation_authorized"] is True
    assert package["implementation_regression_certified"] is False

    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False



def test_r4_d_partial_authorization_recording_recovery_is_exact():
    package = load(PACKAGE)

    recovery = package[
        "implementation_authorization_recording_failure_recovery_evidence"
    ]

    assert recovery["failed_recording_attempt"] == {
        "exception": "AssertionError",
        "result": "fail",
    }

    assert (
        recovery["classification"]
        == (
            "partial_implementation_authorization_"
            "certification_recording_before_late_assertion"
        )
    )

    assert recovery["certification_state_already_written"] is True
    assert recovery["certification_evidence_remains_valid"] is True
    assert recovery["r4_d_behavioral_defect_detected"] is False
    assert recovery["runtime_scope_expanded"] is False
    assert recovery["production_schema_scope_expanded"] is False
    assert recovery["semantic_authority_expanded"] is False
    assert recovery["full_repository_rerun_required"] is False
