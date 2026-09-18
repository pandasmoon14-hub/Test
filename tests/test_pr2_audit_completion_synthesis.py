# Executable validation for PR2-AUDIT-D completion synthesis.
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE = "6455659b61bc0b56fa6c41f95e15f5b1b94d077a"
AUTH = "owner_directive_2026-09-17_pr2_audit_d_completion_synthesis"
EFFECT = "repository_wide_post_r2_audit_completion_synthesis_only"

REVIEW = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_audit_completion_synthesis.yaml"
)

MAN = (
    ROOT
    / "docs/doctrine/control/"
    "post_r2a_transition_manifest.yaml"
)

ID_REVIEW = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_id_identity_migration_completion_review.yaml"
)

SRC_REVIEW = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_src_source_research_completion_review.yaml"
)

SRC_C = (
    ROOT
    / "docs/doctrine/control/"
    "myravant_legacy_source_conversion_surface_disposition.yaml"
)

AUDIT_A = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_audit_r3_promotion_blocker_r4_entry_disposition.yaml"
)

R4_0 = (
    ROOT
    / "docs/doctrine/reviews/"
    "r4_0_substrate_reconciliation.yaml"
)

R4_A = (
    ROOT
    / "docs/doctrine/reviews/"
    "r4_a_myravant_native_substrate_design.yaml"
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_audit_d_is_completion_synthesis_only():
    review = load(REVIEW)

    assert review["artifact_version"] == "0.1.1"
    assert review["status"] == "validated_complete"
    assert review["workstream_id"] == "PR2-AUDIT"
    assert review["tranche_id"] == "PR2-AUDIT-D"
    assert review["tranche_alias"] == "AUDIT-CLOSE"
    assert review["authorization_reference"] == AUTH
    assert review["authority_effect"] == EFFECT
    assert review["starting_baseline"] == BASE

    method = review["method"]

    assert method["new_unbounded_repository_scan_performed"] is False
    assert method["silent_remediation_permitted"] is False
    assert method["historical_rewrite_permitted"] is False
    assert method["implementation_permitted"] is False


def test_all_six_audit_dependencies_are_merged_without_residuals():
    review = load(REVIEW)
    manifest = load(MAN)

    expected = {
        "PR2-ID",
        "PR2-SRC",
        "PR2-ORG",
        "PR2-CORPUS",
        "PR2-IR",
        "PR2-SCALE",
    }

    assert {
        row["workstream_id"]
        for row in review["dependency_completion"]
    } == expected

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    for wid in expected:
        assert by_id[wid]["status"] == "merged"
        assert by_id[wid]["residual_gaps"] == []


def test_identity_and_source_inputs_are_already_dispositioned():
    review = load(REVIEW)
    identity = load(ID_REVIEW)
    src_review = load(SRC_REVIEW)
    src_c = load(SRC_C)

    assert identity["review_result"] == "PASS"
    assert (
        identity["audit_findings"]
        ["unclassified_material_current_facing_identity_surfaces_found"]
        is False
    )
    assert len(identity["carried_forward_obligations"]) == 4
    assert len(review["identity_carried_forward_dispositions"]) == 4
    assert all(
        row["current_migration_required"] is False
        for row in review["identity_carried_forward_dispositions"]
    )

    assert src_review["review_result"] == "PASS"
    assert src_review["completion_findings"]["legacy_surfaces_disposed"]
    assert src_c["inventory_scope"]["surface_record_count"] == 6
    assert len(review["legacy_source_surface_dispositions"]) == 6
    assert all(
        row["current_migration_required"] is False
        for row in review["legacy_source_surface_dispositions"]
    )


def test_exact_current_migration_set_is_rs_0028_then_rs_0030():
    review = load(REVIEW)
    audit_a = load(AUDIT_A)

    source_rows = [
        row
        for row in audit_a["audit_dispositions"]
        if row["migration_required_now"]
    ]

    assert len(source_rows) == 2

    inventory = review["migration_inventory"]

    assert inventory["current_migration_required_count"] == 2
    assert inventory["required_execution_order"] == [
        "R2A-DISPOSITION-RS-0028",
        "R2A-DISPOSITION-RS-0030",
    ]
    assert inventory["migration_execution_authorized"] is False

    candidates = inventory["migration_candidates"]

    assert [row["candidate_file_id"] for row in candidates] == [
        "R2A-DISPOSITION-RS-0028",
        "R2A-DISPOSITION-RS-0030",
    ]

    assert [row["path"] for row in candidates] == [
        (
            "src/astra_runtime/domain/"
            "object_lever_event_commit_state_delta_path.py"
        ),
        (
            "src/astra_runtime/domain/"
            "object_lever_replay_audit_check.py"
        ),
    ]


def test_r4_inputs_are_complete_but_do_not_authorize_implementation():
    review = load(REVIEW)
    r4_0 = load(R4_0)
    r4_a = load(R4_A)

    assert r4_0["status"] == "validated_complete"
    assert r4_0["summary"]["candidate_count"] == 16
    assert (
        r4_0["summary"]["direct_runtime_substrate_candidate_count"]
        == 0
    )

    assert r4_a["status"] == "validated_complete"
    assert r4_a["summary"]["historical_substrate_class_count"] == 5
    assert r4_a["summary"]["selected_native_capability_count"] == 1
    assert (
        r4_a["implementation_handoff"]["ready_pending_authorization"]
        is False
    )

    assert (
        review["input_inventories"]
        ["r4_a_native_substrate_design"]
        ["implementation_authorized"]
        is False
    )


def test_completion_is_validated_but_not_claimed_before_merge():
    review = load(REVIEW)
    manifest = load(MAN)

    findings = review["completion_findings"]

    assert findings["undispositioned_input_group_count"] == 0
    assert findings["current_migration_required_count"] == 2
    assert (
        findings["repository_wide_audit_completion_recommended"]
        is True
    )
    assert findings["repository_wide_audit_complete"] is False

    assert review["validation_state"] == "validated"
    assert set(review["validation_evidence"]) == {
        "PR2-AUDIT-D focused pre-certification:42 passed",
        (
            "PR2-AUDIT-D full local repository suite:"
            "9239 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        (
            "PR2-AUDIT-D focused post-suite regression:"
            "42 passed"
        ),
        "PR2-AUDIT-D git diff --check:clean",
        "PR2-AUDIT-D exact seven-file footprint:PASS",
        "PR2-AUDIT-D runtime/schema noninterference audit:PASS",
    }

    target = manifest["pr2_audit_completion_target"]

    assert target["status"] == "validated"
    assert target["current_migration_required_count"] == 2
    assert target["undispositioned_input_group_count"] == 0
    assert target["repository_wide_audit_completion_recommended"] is True
    assert target["repository_wide_audit_complete"] is False
    assert target["pr2_mig_ready_after_validation_and_merge"] is True
    assert target["pr2_mig_ready_now"] is False
    assert target["pr2_mig_authorized"] is False
    assert target["runtime_promotion_clear"] is False
    assert target["r4_activation_authorized"] is False


def test_no_successor_is_activated_by_audit_d():
    manifest = load(MAN)

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    assert by_id["PR2-AUDIT"]["status"] == "active"
    assert by_id["PR2-AUDIT"]["current_tranche"] == "PR2-AUDIT-D"

    for wid in ("PR2-MIG", "PR2-TEST", "PR2-IMPL"):
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"
    assert (
        manifest["r3_conformance_target"]["runtime_promotion_clear"]
        is False
    )
