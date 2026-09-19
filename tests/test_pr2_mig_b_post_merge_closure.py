# Executable validation for PR2-MIG-B post-merge closure.
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

PR = 419
HEAD = "8e33ade1bc7f1346401131394b3de2327802d882"
MERGE = "2b9e1a690bb567dfa3fda8c1982179e86106860b"
TREE = "cef6740107d345a8ff97c6b06b0eb777aaf158a9"
CI_RUN = 238
CI_RUN_ID = 35405934205

AUTH = "owner_directive_2026-09-18_pr2_mig_b_post_merge_closure"
EFFECT = "bounded_rs_0030_post_merge_lifecycle_reconciliation_only"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


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


def test_pr2_mig_is_terminal_and_inventory_is_empty():
    manifest = load(MAN)
    mig = rows(manifest)["PR2-MIG"]

    assert manifest["artifact_version"] == "0.4.58"

    assert mig["status"] == "merged"
    assert mig["current_tranche"] == "PR2-MIG-B"
    assert (
        mig["current_tranche_candidate_id"]
        == "R2A-DISPOSITION-RS-0030"
    )
    assert mig["current_tranche_state"] == "merged"
    assert mig["current_tranche_completion_state"] == "merged"

    assert mig["migration_execution_authorized"] is False
    assert mig["migration_execution_scope"] == []
    assert mig["remaining_candidate_ids"] == []

    assert mig["next_candidate_id"] is None
    assert mig["next_tranche_id"] is None

    target = manifest["pr2_audit_completion_target"]

    assert target["current_migration_required_count"] == 0
    assert target["migration_required_candidate_ids"] == []

    assert (
        target["pr2_mig_last_completed_tranche"]
        == "PR2-MIG-B"
    )
    assert (
        target["pr2_mig_last_completed_candidate_id"]
        == "R2A-DISPOSITION-RS-0030"
    )


def test_accepted_pr419_merge_metadata_is_exact():
    mig = rows(load(MAN))["PR2-MIG"]

    assert mig["pull_request"] == PR
    assert mig["branch_head"] == HEAD
    assert mig["merge_commit"] == MERGE

    assert mig["current_tranche_pull_request"] == PR
    assert mig["current_tranche_branch_head"] == HEAD
    assert mig["current_tranche_merge_commit"] == MERGE
    assert mig["current_tranche_merge_tree"] == TREE

    assert (
        mig["post_merge_closure_authorization_reference"]
        == AUTH
    )
    assert (
        mig["post_merge_closure_authority_effect"]
        == EFFECT
    )
    assert mig["post_merge_closure_recorded_from"] == MERGE
    assert mig["post_merge_closure_tree"] == TREE


def test_completed_tranche_inventory_contains_a_and_b():
    mig = rows(load(MAN))["PR2-MIG"]

    assert len(mig["completed_tranches"]) == 2

    assert mig["completed_tranches"][-1] == {
        "tranche_id": "PR2-MIG-B",
        "candidate_id": "R2A-DISPOSITION-RS-0030",
        "state": "merged",
        "authorization_reference":
            "owner_directive_2026-09-18_pr2_mig_rs_0030",
        "authority_effect":
            "bounded_rs_0030_replay_audit_qualification_migration_only",
        "starting_baseline":
            "b4b52cab91916e050e20ad54ff3559153436a944",
        "target_path":
            "src/astra_runtime/domain/"
            "object_lever_replay_audit_check.py",
        "pull_request": PR,
        "branch_head": HEAD,
        "merge_commit": MERGE,
        "merge_tree": TREE,
        "validation_state": "validated",
        "ci_run": CI_RUN,
        "ci_run_id": CI_RUN_ID,
        "ci_result": "success",
    }


def test_closure_changes_no_runtime_candidate():
    assert read_at(
        MERGE,
        RS0028_RUNTIME,
    ) == RS0028_RUNTIME.read_text(
        encoding="utf-8"
    )

    assert read_at(
        MERGE,
        RS0030_RUNTIME,
    ) == RS0030_RUNTIME.read_text(
        encoding="utf-8"
    )


def test_downstream_authority_is_not_silently_advanced():
    manifest = load(MAN)
    by = rows(manifest)

    assert by["PR2-TEST"]["status"] == "blocked"
    assert by["PR2-TEST"]["authorization_reference"] is None

    assert by["PR2-IMPL"]["status"] == "blocked"
    assert by["PR2-IMPL"]["authorization_reference"] is None

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

    assert (
        manifest["r3_conformance_target"][
            "runtime_promotion_clear"
        ]
        is False
    )

    r4 = manifest["r4_native_substrate_design_target"]

    assert r4["r4_b_ready_pending_authorization"] is False
    assert r4["r4_b_authorized"] is False



def test_terminal_closure_validation_evidence_is_exact():
    mig = rows(load(MAN))["PR2-MIG"]

    assert mig["validation_evidence"][-5:] == ['PR2-MIG-B post-merge closure bounded regression:442 passed, 3 skipped', 'PR2-MIG-B post-merge closure full local repository suite:9273 passed, 10 skipped, 2 xfailed, 1 warning', 'PR2-MIG-B post-merge closure focused post-suite certification:80 passed, 1 skipped', 'PR2-MIG-B post-merge closure exact five-file footprint:PASS', 'PR2-MIG-B post-merge closure runtime/schema noninterference:PASS']

    assert mig["status"] == "merged"
    assert mig["migration_execution_authorized"] is False
    assert mig["migration_execution_scope"] == []


def test_program_and_decision_log_record_terminal_closure():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.58`" in program

    assert (
        "### 5.53 PR2-MIG-B post-merge closure recording"
        in program
    )

    assert AUTH in program
    assert EFFECT in program
    assert HEAD in program
    assert MERGE in program
    assert TREE in program

    assert "PR2-MIG-B is terminal `merged`." in program
    assert "The migration-required count is now `0`." in program

    assert "PR2-MIG-B-POST-MERGE-CLOSURE-007" in decisions
    assert (
        "PR2-MIG-B-POST-MERGE-CLOSURE-VALIDATION-008"
        in decisions
    )
    assert AUTH in decisions
    assert EFFECT in decisions
    assert HEAD in decisions
    assert MERGE in decisions
    assert TREE in decisions

    assert "442 passed, 3 skipped" in program
    assert "9273 passed" in program
    assert "80 passed" in program

    assert "442 passed, 3 skipped" in decisions
    assert "9273 passed, 10 skipped, 2 xfailed, 1 warning" in decisions
    assert "80 passed, 1 skipped" in decisions
