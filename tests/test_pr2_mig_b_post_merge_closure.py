# Executable validation for the historical PR2-MIG-B post-merge closure.
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

CLOSURE_MERGE = "02d63b38e83000099e2654d74db0d0454bf97346"
CLOSURE_TREE = "031d38ec2ec973cb5812dde11824b4e838cf752e"

PR = 419
HEAD = "8e33ade1bc7f1346401131394b3de2327802d882"
MERGE = "2b9e1a690bb567dfa3fda8c1982179e86106860b"
TREE = "cef6740107d345a8ff97c6b06b0eb777aaf158a9"
CI_RUN = 238
CI_RUN_ID = 35405934205

AUTH = "owner_directive_2026-09-18_pr2_mig_b_post_merge_closure"
EFFECT = "bounded_rs_0030_post_merge_lifecycle_reconciliation_only"


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


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def rows(data):
    return {
        row["workstream_id"]: row
        for row in data["workstreams"]
    }


def rev_parse(ref):
    return subprocess.check_output(
        [
            "git",
            "rev-parse",
            ref,
        ],
        cwd=ROOT,
        text=True,
    ).strip()


def closure_manifest():
    return load_at(
        CLOSURE_MERGE,
        MAN,
    )


def test_closure_snapshot_identity_is_exact():
    assert (
        rev_parse(
            f"{CLOSURE_MERGE}^{{tree}}"
        )
        == CLOSURE_TREE
    )


def test_pr2_mig_is_terminal_and_inventory_is_empty_at_closure():
    manifest = closure_manifest()
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


def test_pr2_test_was_blocked_at_accepted_closure_snapshot():
    manifest = closure_manifest()
    by = rows(manifest)

    assert by["PR2-TEST"]["status"] == "blocked"
    assert (
        by["PR2-TEST"]["authorization_reference"]
        is None
    )

    assert by["PR2-IMPL"]["status"] == "blocked"
    assert (
        by["PR2-IMPL"]["authorization_reference"]
        is None
    )

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

    assert (
        manifest["r3_conformance_target"][
            "runtime_promotion_clear"
        ]
        is False
    )


def test_accepted_pr419_merge_metadata_is_exact_at_closure():
    mig = rows(
        closure_manifest()
    )["PR2-MIG"]

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
    assert (
        mig["post_merge_closure_recorded_from"]
        == MERGE
    )
    assert (
        mig["post_merge_closure_tree"]
        == TREE
    )


def test_completed_tranche_inventory_contains_a_and_b_at_closure():
    mig = rows(
        closure_manifest()
    )["PR2-MIG"]

    assert len(
        mig["completed_tranches"]
    ) == 2

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


def test_closure_changed_no_runtime_candidate():
    assert (
        read_at(
            CLOSURE_MERGE,
            RS0028_RUNTIME,
        )
        == read_at(
            MERGE,
            RS0028_RUNTIME,
        )
    )

    assert (
        read_at(
            CLOSURE_MERGE,
            RS0030_RUNTIME,
        )
        == read_at(
            MERGE,
            RS0030_RUNTIME,
        )
    )


def test_terminal_closure_validation_evidence_is_exact():
    mig = rows(
        closure_manifest()
    )["PR2-MIG"]

    assert mig["validation_evidence"][-5:] == [
        "PR2-MIG-B post-merge closure bounded regression:"
        "442 passed, 3 skipped",
        "PR2-MIG-B post-merge closure full local repository suite:"
        "9273 passed, 10 skipped, 2 xfailed, 1 warning",
        "PR2-MIG-B post-merge closure focused post-suite certification:"
        "80 passed, 1 skipped",
        "PR2-MIG-B post-merge closure exact five-file footprint:PASS",
        "PR2-MIG-B post-merge closure runtime/schema noninterference:PASS",
    ]


def test_program_and_decision_log_record_terminal_closure_snapshot():
    program = read_at(
        CLOSURE_MERGE,
        PROG,
    )
    decisions = read_at(
        CLOSURE_MERGE,
        DEC,
    )

    assert (
        "**Artifact version:** `0.4.58`"
        in program
    )

    assert (
        "### 5.53 PR2-MIG-B post-merge closure recording"
        in program
    )

    for value in (
        AUTH,
        EFFECT,
        HEAD,
        MERGE,
        TREE,
    ):
        assert value in program
        assert value in decisions

    assert (
        "PR2-MIG-B is terminal `merged`."
        in program
    )
    assert (
        "The migration-required count is now `0`."
        in program
    )

    assert (
        "PR2-MIG-B-POST-MERGE-CLOSURE-007"
        in decisions
    )
    assert (
        "PR2-MIG-B-POST-MERGE-CLOSURE-VALIDATION-008"
        in decisions
    )
