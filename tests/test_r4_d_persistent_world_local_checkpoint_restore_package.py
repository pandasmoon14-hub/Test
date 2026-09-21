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

    assert package["artifact_version"] == "0.1.0"
    assert package["package_id"] == "R4-D"

    assert (
        package["package_name"]
        == "persistent_world_local_checkpoint_restore"
    )

    assert (
        package["status"]
        == "package_defined"
    )


def test_r4_d_is_definition_only():
    package = load(PACKAGE)

    assert package["implementation_authorized"] is False
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

    assert len(criteria) == 20

    ids = [row["criterion_id"] for row in criteria]

    assert len(ids) == len(set(ids))
    assert ids[0] == "R4D-AC-001"
    assert ids[-1] == "R4D-AC-020"


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

    assert manifest["artifact_version"] == "0.4.78"

    target = manifest[
        "r4_d_local_checkpoint_restore_target"
    ]

    assert target["package_id"] == package["package_id"]
    assert target["package_name"] == package["package_name"]
    assert target["implementation_authorized"] is False

    assert (
        target["next_gate"]
        == "r4_d_definition_commit_push"
    )

    assert target["next_gate_authorized"] is False



def test_r4_d_definition_regression_certification_is_exact():
    package = load(PACKAGE)

    assert package["artifact_version"] == "0.1.0"
    assert package["status"] == "package_defined"

    assert package["definition_regression_certified"] is True

    assert (
        package["definition_recording_state"]
        == "regression_certified_pending_commit"
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

    assert package["implementation_authorized"] is False
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

    assert package["implementation_authorized"] is False
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
