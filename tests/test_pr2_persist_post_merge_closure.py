# Executable validation for PR2-PERSIST post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_persistence_snapshot_replay_recovery_contract.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_persist_persistence_recovery_contract.py"

PR = 405
HEAD = "814476c63d5ee65701f1abfff19db5b347c1dd05"
MERGE = "e53e64f92fe2639d68c96bfa70825c6f6ec39f03"
TREE = "9171db95438dfc75460ed7c340f3be5d84813825"
AUTH = "owner_directive_2026-09-15_pr2_persist_post_merge_closure"
EFFECT = "runtime_persistence_governance_post_merge_lifecycle_reconciliation_only"
ACCEPTED_MERGE = "bc79bc629f3cc6bff220c8e71c37d9df515b9f8c"


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


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def test_persist_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load_at(ACCEPTED_MERGE, MAN)
    persist = rows(manifest)["PR2-PERSIST"]

    assert manifest["artifact_version"] == "0.4.36"
    assert persist["status"] == "merged"
    assert persist["completion_state"] == "merged"
    assert persist["pull_request"] == PR
    assert persist["branch_head"] == HEAD
    assert persist["merge_commit"] == MERGE
    assert persist["post_merge_closure_authorization_reference"] == AUTH
    assert persist["post_merge_closure_authority_effect"] == EFFECT
    assert persist["post_merge_closure_recorded_from"] == MERGE
    assert persist["post_merge_closure_tree"] == TREE

    evidence = set(persist["validation_evidence"])

    assert (
        "PR2-PERSIST full local repository suite:"
        "9156 passed, 10 skipped, 2 xfailed, 1 warning"
    ) in evidence

    assert "PR2-PERSIST GitHub Actions CI #209:success" in evidence
    assert "PR2-PERSIST git diff --check:clean" in evidence
    assert (
        "PR2-PERSIST exact seven-file activation footprint:PASS"
        in evidence
    )
    assert "PR2-PERSIST structural authority audit:PASS" in evidence


def test_closure_activates_no_successor_and_preserves_r3():
    manifest = load_at(ACCEPTED_MERGE, MAN)
    by = rows(manifest)

    assert {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    } == set()

    for wid in (
        "PR2-FID",
        "PR2-BP",
        "PR2-AUDIT",
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    ):
        assert by[wid]["status"] == "blocked"
        assert by[wid]["authorization_reference"] is None
        assert by[wid]["starting_baseline"] is None

    assert (
        manifest["r2_gate_state"]["R3"]
        == "ready_pending_authorization"
    )
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert (
        manifest["r3_conformance_target"]["execution_authorized"]
        is False
    )


def test_closure_does_not_change_persistence_contract():
    assert (
        read_at(ACCEPTED_MERGE, CONTRACT)
        == read_at(MERGE, CONTRACT)
    )


def test_activation_test_is_frozen_against_accepted_merge():
    text = read_at(ACCEPTED_MERGE, ACTIVATION_TEST)

    assert f'MERGE = "{MERGE}"' in text
    assert "load_at(MERGE, MAN)" in text
    assert "read_at(MERGE, CONTRACT)" in text
    assert "read_at(MERGE, EVENT_CLOSURE)" in text
    assert "read_at(MERGE, PROG)" in text
    assert "read_at(MERGE, DEC)" in text


def test_program_and_decisions_record_bounded_closure():
    program = read_at(ACCEPTED_MERGE, PROG)
    decisions = read_at(ACCEPTED_MERGE, DEC)

    assert "**Artifact version:** `0.4.36`" in program
    assert (
        "### 5.33 PR2-PERSIST post-merge closure recording"
        in program
    )
    assert AUTH in program
    assert EFFECT in program
    assert HEAD in program
    assert MERGE in program
    assert TREE in program
    assert "PR2-PERSIST is terminal `merged`." in program
    assert (
        "No successor is active after PR2-PERSIST closure."
        in program
    )
    assert "PR2-FID remains `blocked` and unauthorized." in program
    assert "PR2-BP remains `blocked` and unauthorized." in program
    assert (
        "PART -> CONC -> EVENT -> PERSIST -> FID -> BP -> R3"
        in program
    )

    assert "PR2-PERSIST-POST-MERGE-CLOSURE-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert HEAD in decisions
    assert MERGE in decisions
    assert TREE in decisions
    assert (
        "No successor is activated by the PR2-PERSIST closure."
        in decisions
    )
