# Executable validation for PR2-MIG-A post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
RS0028_RUNTIME = (
    ROOT
    / "src/astra_runtime/domain/"
    "object_lever_event_commit_state_delta_path.py"
)
RS0030_RUNTIME = (
    ROOT
    / "src/astra_runtime/domain/"
    "object_lever_replay_audit_check.py"
)

PR = 417
HEAD = "f853830ff8b1f4a8f5fccba030fe66c796e03f21"
MERGE = "3d2125e91da1d6f687dd5d72805c39cafef9afb6"
TREE = "07c2c8f70d220f3b3e382bc2ad67e73d2c342eca"
CLOSURE_MERGE = "b4b52cab91916e050e20ad54ff3559153436a944"
CLOSURE_TREE = "c41322bc060fa77d0d447010c45c584e73764ee4"
AUTH = "owner_directive_2026-09-18_pr2_mig_a_post_merge_closure"
EFFECT = "bounded_rs_0028_post_merge_lifecycle_reconciliation_only"


def load(path):
    return json.loads(read_at(CLOSURE_MERGE, path))


def rows(manifest):
    return {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }


def read_at(ref, path):
    return subprocess.check_output(
        [
            "git",
            "show",
            f"{ref}:{path.relative_to(ROOT).as_posix()}",
        ],
        cwd=ROOT,
        text=True,
    )


def test_rs0028_is_merged_and_rs0030_is_only_remaining_candidate():
    manifest = load(MAN)
    mig = rows(manifest)["PR2-MIG"]

    assert manifest["artifact_version"] == "0.4.55"
    assert mig["status"] == "active"

    assert mig["current_tranche"] == "PR2-MIG-A"
    assert mig["current_tranche_candidate_id"] == "R2A-DISPOSITION-RS-0028"
    assert mig["current_tranche_state"] == "merged"
    assert mig["current_tranche_completion_state"] == "merged"

    assert mig["pull_request"] == PR
    assert mig["branch_head"] == HEAD
    assert mig["merge_commit"] == MERGE

    assert mig["remaining_candidate_ids"] == [
        "R2A-DISPOSITION-RS-0030"
    ]

    assert mig["migration_execution_authorized"] is False
    assert mig["migration_execution_scope"] == []


def test_post_merge_closure_metadata_is_exact():
    mig = rows(load(MAN))["PR2-MIG"]

    assert mig["post_merge_closure_authorization_reference"] == AUTH
    assert mig["post_merge_closure_authority_effect"] == EFFECT
    assert mig["post_merge_closure_recorded_from"] == MERGE
    assert mig["post_merge_closure_tree"] == TREE

    assert mig["completed_tranches"][-1] == {
        "tranche_id": "PR2-MIG-A",
        "candidate_id": "R2A-DISPOSITION-RS-0028",
        "state": "merged",
        "authorization_reference":
            "owner_directive_2026-09-18_pr2_mig_rs_0028",
        "authority_effect":
            "bounded_rs_0028_commitment_qualification_migration_only",
        "starting_baseline":
            "33e09250ef2d68946bd058044f15306c66bbefaf",
        "target_path":
            "src/astra_runtime/domain/"
            "object_lever_event_commit_state_delta_path.py",
        "pull_request": PR,
        "branch_head": HEAD,
        "merge_commit": MERGE,
        "merge_tree": TREE,
        "validation_state": "validated",
        "ci_run": 234,
        "ci_run_id": 35396966183,
        "ci_result": "success",
    }


def test_pr2_mig_b_is_ready_but_not_authorized():
    manifest = load(MAN)
    mig = rows(manifest)["PR2-MIG"]

    assert mig["next_candidate_id"] == "R2A-DISPOSITION-RS-0030"
    assert mig["next_candidate_authorized"] is False
    assert mig["next_tranche_id"] == "PR2-MIG-B"
    assert mig["next_tranche_state"] == "ready_pending_authorization"
    assert mig["next_tranche_candidate_id"] == "R2A-DISPOSITION-RS-0030"
    assert mig["next_tranche_authorized"] is False
    assert mig["next_tranche_authorization_reference"] is None
    assert mig["next_tranche_starting_baseline"] is None

    target = manifest["pr2_audit_completion_target"]
    assert target["current_migration_required_count"] == 1
    assert target["migration_required_candidate_ids"] == [
        "R2A-DISPOSITION-RS-0030"
    ]
    assert target["pr2_mig_last_completed_tranche"] == "PR2-MIG-A"
    assert (
        target["pr2_mig_last_completed_candidate_id"]
        == "R2A-DISPOSITION-RS-0028"
    )
    assert target["pr2_mig_next_tranche"] == "PR2-MIG-B"
    assert (
        target["pr2_mig_next_candidate_id"]
        == "R2A-DISPOSITION-RS-0030"
    )
    assert target["pr2_mig_next_ready_pending_authorization"] is True


def test_closure_does_not_modify_either_runtime_candidate():
    assert read_at(MERGE, RS0028_RUNTIME) == read_at(
        CLOSURE_MERGE,
        RS0028_RUNTIME,
    )
    assert read_at(MERGE, RS0030_RUNTIME) == read_at(
        CLOSURE_MERGE,
        RS0030_RUNTIME,
    )


def test_no_downstream_gate_is_silently_advanced():
    manifest = load(MAN)
    by = rows(manifest)

    assert by["PR2-TEST"]["status"] == "blocked"
    assert by["PR2-TEST"]["authorization_reference"] is None
    assert by["PR2-IMPL"]["status"] == "blocked"
    assert by["PR2-IMPL"]["authorization_reference"] is None

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"
    assert (
        manifest["r3_conformance_target"]["runtime_promotion_clear"]
        is False
    )

    r4 = manifest["r4_native_substrate_design_target"]
    assert r4["r4_b_ready_pending_authorization"] is False
    assert r4["r4_b_authorized"] is False


def test_program_and_decision_log_record_bounded_closure():
    program = read_at(CLOSURE_MERGE, PROG)
    decisions = read_at(CLOSURE_MERGE, DEC)

    assert "**Artifact version:** `0.4.55`" in program
    assert "### 5.50 PR2-MIG-A post-merge closure recording" in program
    assert AUTH in program
    assert EFFECT in program
    assert HEAD in program
    assert MERGE in program
    assert TREE in program
    assert "PR2-MIG-A is terminal `merged`." in program
    assert "PR2-MIG-B is `ready_pending_authorization`." in program

    assert "PR2-MIG-A-POST-MERGE-CLOSURE-004" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert HEAD in decisions
    assert MERGE in decisions
    assert TREE in decisions
