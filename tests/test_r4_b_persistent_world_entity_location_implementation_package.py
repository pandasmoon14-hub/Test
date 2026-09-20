# Executable validation for the R4-B implementation package definition.
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PACKAGE = (
    ROOT
    / "docs/doctrine/reviews/"
    "r4_b_persistent_world_entity_location_implementation_package.yaml"
)

R4A = (
    ROOT
    / "docs/doctrine/reviews/"
    "r4_a_myravant_native_substrate_design.yaml"
)

CONTRACT = (
    ROOT
    / "docs/doctrine/control/"
    "myravant_pr2_implementation_handoff_contract.md"
)

HANDOFF_IDS = [
    "PR2-TEST-HANDOFF-TOPOLOGY-001",
    "PR2-TEST-HANDOFF-PERSIST-001",
    "PR2-TEST-HANDOFF-FIDELITY-001",
    "PR2-TEST-HANDOFF-BP-001",
    "PR2-TEST-HANDOFF-FAILURE-001",
]


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


def test_package_records_exact_thirteen_part_shape():
    package = load(PACKAGE)

    required = {
        "playable_need",
        "bounded_capability",
        "semantic_owners",
        "implementation_owner",
        "dependencies",
        "edit_allowlist",
        "prohibited_scope",
        "deterministic_acceptance_criteria",
        "replay_recovery_equivalence",
        "failure_behavior",
        "performance_evidence",
        "regression_evidence_before_merge",
        "downstream_lifecycle_transition",
    }

    assert required.issubset(package)
    assert len(required) == 13

    contract = " ".join(
        CONTRACT.read_text(
            encoding="utf-8",
        ).split()
    )

    assert (
        "Before an implementation package may be separately authorized"
        in contract
    )

    assert (
        "13. downstream lifecycle transition after merge."
        in contract
    )


def test_package_is_r4_a_derived_and_explicitly_authorized_for_bounded_implementation():
    package = load(PACKAGE)
    r4a = load(R4A)

    assert package["package_id"] == "R4-B"

    assert (
        package["status"]
        == "implemented_regression_certified_pending_commit"
    )

    assert package["implementation_authorized"] is True
    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False

    assert (
        package["bounded_capability"]["source_capability_id"]
        == "R4-A-CAP-001"
    )

    assert (
        r4a["selected_native_capability"]["name"]
        == package["bounded_capability"]["source_capability_name"]
    )


def test_semantic_owners_remain_distinct():
    package = load(PACKAGE)

    owners = {
        row["concern"]: row
        for row in package["semantic_owners"]
    }

    assert (
        owners["located_at_relation_semantics"]["owner_ref"]
        == "AFQR-18"
    )

    assert (
        owners["state_owner_transport_reference"]["owner_ref"]
        == "scene_location_owner"
    )

    implementation_owner = package["implementation_owner"]

    assert (
        implementation_owner["semantic_authority_acquired"]
        is False
    )

    assert (
        "AFQR-18 spatial semantics"
        in implementation_owner["does_not_own"]
    )

    assert (
        "record-identity semantics"
        in implementation_owner["does_not_own"]
    )

    assert (
        "persistence authority"
        in implementation_owner["does_not_own"]
    )


def test_edit_allowlist_is_narrow_and_has_no_schema_edit():
    package = load(PACKAGE)
    allow = package["edit_allowlist"]

    assert allow["runtime_paths"] == [
        (
            "src/astra_runtime/domain/"
            "persistent_world_entity_location_representation.py"
        )
    ]

    assert allow["production_schema_paths"] == []

    assert allow["test_paths"] == [
        (
            "tests/"
            "test_r4_b_persistent_world_entity_location_representation.py"
        )
    ]

    assert set(
        allow["existing_dependency_paths_read_only"]
    ) == {
        "src/astra_runtime/kernel/record_identity.py",
        (
            "src/astra_runtime/domain/"
            "state_owner_interface_contract_skeleton.py"
        ),
        (
            "src/astra_runtime/domain/"
            "read_only_vertical_slice_state_owner_facade.py"
        ),
        "src/astra_runtime/domain/tiny_vertical_slice.py",
    }


def test_all_five_carried_handoffs_are_assessed_nonblocking():
    package = load(PACKAGE)

    rows = package["dependencies"][
        "carried_handoff_dependency_assessment"
    ]

    assert [
        row["handoff_id"]
        for row in rows
    ] == HANDOFF_IDS

    assert all(
        row["blocks_r4_b"] is False
        for row in rows
    )


def test_acceptance_criteria_are_bounded_and_deterministic():
    package = load(PACKAGE)

    criteria = package["deterministic_acceptance_criteria"]

    assert len(criteria) == 12

    ids = [
        row["criterion_id"]
        for row in criteria
    ]

    assert ids == [
        f"R4B-AC-{number:03d}"
        for number in range(1, 13)
    ]

    flat = " ".join(
        row["requirement"]
        for row in criteria
    )

    for token in (
        "RecordId",
        "closed universal enum",
        "AFQR-18",
        "same campaign-scoped representation",
        "fail closed",
        "canonical serialization",
        "scene_location_owner",
        "no model call",
    ):
        assert token in flat


def test_no_generalized_world_manager_or_authority_transfer():
    package = load(PACKAGE)

    prohibited = " ".join(
        package["prohibited_scope"]
    )

    for token in (
        "universal world-state manager",
        "generalized governed-relation registry",
        "model-owned entity or relation authority",
        "authorize R4-B implementation implicitly",
        "authorize R4 activation implicitly",
        "authorize runtime promotion implicitly",
    ):
        assert token in prohibited

    transition = package["downstream_lifecycle_transition"]

    assert (
        transition[
            "implementation_requires_separate_owner_authorization"
        ]
        is True
    )

    assert (
        transition[
            "implementation_authorization_currently_granted"
        ]
        is True
    )

    assert transition["r4_activation_implied"] is False
    assert transition["runtime_promotion_implied"] is False



def test_r4_b_explicit_implementation_authorization_is_exact():
    package = load(PACKAGE)

    assert package["implementation_authorized"] is True

    assert (
        package["implementation_authorization_reference"]
        == "owner_directive_2026-09-20_r4_b_implementation_authorization"
    )

    assert (
        package["implementation_authority_effect"]
        == "bounded_persistent_world_entity_location_representation_implementation_only"
    )

    assert (
        package["implementation_starting_baseline"]
        == "a7d7f912254abeab5716d23d3dc2f7fc5d6c4e59"
    )

    assert (
        package["implementation_starting_tree"]
        == "4b49a8c0f7c2e6fafd1da975cec4ce083284ba8a"
    )

    assert package["implementation_runtime_path"] == (
        "src/astra_runtime/domain/"
        "persistent_world_entity_location_representation.py"
    )

    assert package["implementation_test_path"] == (
        "tests/"
        "test_r4_b_persistent_world_entity_location_representation.py"
    )

    assert (
        package["implementation_state"]
        == "implemented_regression_certified_pending_commit"
    )

    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False



def test_r4_b_regression_certification_evidence_is_exact():
    package = load(PACKAGE)

    assert package["artifact_version"] == "0.1.1"

    assert (
        package["status"]
        == "implemented_regression_certified_pending_commit"
    )

    assert (
        package["implementation_state"]
        == "implemented_regression_certified_pending_commit"
    )

    assert package["regression_certified"] is True

    expected = {
        "focused_pre_regression": {
            "passed": 241,
            "result": "pass",
        },
        "broader_pr2_regression": {
            "passed": 415,
            "result": "pass",
        },
        "full_repository_regression": {
            "passed": 9378,
            "skipped": 10,
            "xfailed": 2,
            "warnings": 1,
            "warning_class": "PytestRemovedIn10Warning",
            "warning_disposition": (
                "existing_nonblocking_deprecation"
            ),
            "result": "pass",
        },
        "focused_post_suite_regression": {
            "passed": 316,
            "result": "pass",
        },
        "git_diff_check": "clean",
        "changed_path_count": 13,
        "production_runtime_path_count": 1,
        "production_schema_path_count": 0,
    }

    assert package["regression_certification"] == expected

    recovery = package["failure_recovery_evidence"]

    assert recovery[
        "failed_full_repository_regression"
    ] == {
        "failed": 40,
        "passed": 9338,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "result": "fail",
    }

    assert (
        recovery["classification"]
        == "stale_runtime_domain_authorization_guardrails"
    )

    assert recovery["r4_b_behavioral_defect_detected"] is False

    assert (
        recovery["repair_scope"]
        == "test_infrastructure_and_historical_compatibility_only"
    )

    checkpoints = recovery["repair_checkpoints"]

    assert checkpoints[
        "shared_domain_package_guardrail"
    ] == {
        "passed": 3,
        "result": "pass",
    }

    assert checkpoints[
        "historical_guardrail_compatibility"
    ] == {
        "passed": 72,
        "result": "pass",
    }

    assert checkpoints[
        "representative_legacy_domain_guardrails"
    ] == {
        "passed": 342,
        "result": "pass",
    }

    assert checkpoints[
        "pr9_rt002_pass_through_seam"
    ] == {
        "passed": 511,
        "result": "pass",
    }

    assert checkpoints[
        "focused_r4_b_after_repair"
    ] == {
        "passed": 241,
        "result": "pass",
    }

    assert (
        recovery["production_runtime_scope_expanded_by_repair"]
        is False
    )

    assert (
        recovery["production_schema_scope_expanded_by_repair"]
        is False
    )

    assert package["r4_activation_authorized"] is False
    assert package["runtime_promotion_authorized"] is False
