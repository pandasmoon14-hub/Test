# Executable validation for PR2-AUDIT post-merge closure.
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE = "720ee27248aac46e8f4e39492d51fda331778209"
AUDIT_D_HEAD = "21916c30eb96dbeb2b84c6b056709339ec31048d"
AUDIT_D_TREE = "04c094a41eda056b58f59bb5553ab718535d1f41"
AUTH = "owner_directive_2026-09-18_pr2_audit_post_merge_closure"
EFFECT = "repository_wide_post_r2_audit_post_merge_lifecycle_reconciliation_only"

MAN = (
    ROOT
    / "docs/doctrine/control/"
    "post_r2a_transition_manifest.yaml"
)

REVIEW = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_audit_completion_synthesis.yaml"
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_audit_is_terminal_merged_after_accepted_audit_d():
    manifest = load(MAN)

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    audit = by_id["PR2-AUDIT"]

    assert audit["status"] == "merged"
    assert audit["pull_request"] == 415
    assert audit["branch_head"] == AUDIT_D_HEAD
    assert audit["merge_commit"] == BASE

    assert audit["current_tranche"] == "PR2-AUDIT-D"
    assert audit["current_tranche_state"] == "merged"
    assert (
        audit["current_tranche_repository_wide_audit_complete"]
        is True
    )
    assert audit["current_tranche_completion_state"] == (
        "merged_repository_wide_audit_complete"
    )

    assert audit["completed_tranches"][-1] == {
        "tranche_id": "PR2-AUDIT-D",
        "alias": "AUDIT-CLOSE",
        "state": "merged",
        "authorization_reference":
            "owner_directive_2026-09-17_"
            "pr2_audit_d_completion_synthesis",
        "pull_request": 415,
        "branch_head": AUDIT_D_HEAD,
        "merge_commit": BASE,
        "merge_tree": AUDIT_D_TREE,
        "review_artifact": (
            "docs/doctrine/reviews/"
            "pr2_audit_completion_synthesis.yaml"
        ),
        "validation_state": "validated",
    }


def test_post_merge_closure_metadata_is_exact():
    manifest = load(MAN)

    audit = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }["PR2-AUDIT"]

    assert (
        audit["post_merge_closure_authorization_reference"]
        == AUTH
    )
    assert audit["post_merge_closure_authority_effect"] == EFFECT
    assert audit["post_merge_closure_recorded_from"] == BASE
    assert audit["post_merge_closure_tree"] == AUDIT_D_TREE


def test_repository_wide_completion_target_is_closed():
    manifest = load(MAN)
    target = manifest["pr2_audit_completion_target"]

    assert target["status"] == "merged"
    assert target["repository_wide_audit_complete"] is True
    assert target["completion_state"] == (
        "merged_repository_wide_audit_complete"
    )

    assert target["current_migration_required_count"] == 2
    assert target["migration_required_candidate_ids"] == [
        "R2A-DISPOSITION-RS-0028",
        "R2A-DISPOSITION-RS-0030",
    ]

    assert target["pr2_mig_ready_now"] is True
    assert target["pr2_mig_authorized"] is False

    assert target["runtime_promotion_clear"] is False
    assert target["r4_activation_authorized"] is False


def test_pr2_mig_is_ready_but_not_authorized():
    manifest = load(MAN)

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    mig = by_id["PR2-MIG"]

    assert mig["status"] == "ready_pending_authorization"
    assert mig["authorization_reference"] is None
    assert mig["starting_baseline"] is None

    assert mig["readiness_source"] == "PR2-AUDIT"
    assert mig["readiness_recorded_from"] == BASE
    assert mig["readiness_candidate_ids"] == [
        "R2A-DISPOSITION-RS-0028",
        "R2A-DISPOSITION-RS-0030",
    ]
    assert mig["readiness_execution_order"] == [
        "R2A-DISPOSITION-RS-0028",
        "R2A-DISPOSITION-RS-0030",
    ]
    assert mig["migration_execution_authorized"] is False


def test_no_later_gate_is_silently_advanced():
    manifest = load(MAN)

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    assert by_id["PR2-TEST"]["status"] == "blocked"
    assert by_id["PR2-TEST"]["authorization_reference"] is None

    assert by_id["PR2-IMPL"]["status"] == "blocked"
    assert by_id["PR2-IMPL"]["authorization_reference"] is None

    r4 = manifest["r4_native_substrate_design_target"]

    assert r4["r4_b_ready_pending_authorization"] is False
    assert r4["r4_b_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

    assert (
        manifest["r3_conformance_target"]["runtime_promotion_clear"]
        is False
    )
    assert (
        manifest["r3_conformance_target"]["r4_activation_authorized"]
        is False
    )


def test_audit_d_review_remains_historical_validation_evidence():
    review = load(REVIEW)

    assert review["artifact_version"] == "0.1.1"
    assert review["status"] == "validated_complete"
    assert review["validation_state"] == "validated"

    assert (
        review["completion_findings"]
        ["repository_wide_audit_complete"]
        is False
    )

    assert (
        review["completion_findings"]
        ["reason_audit_complete_is_false"]
        == (
            "Audit-D is validated but repository-wide PR2-AUDIT "
            "closure requires merge of this certified tranche."
        )
    )
