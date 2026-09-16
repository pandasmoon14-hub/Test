# Executable validation for PR2-BP post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_performance_budget_overload_backpressure_contract.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_bp_performance_overload_backpressure_contract.py"

PR = 409
HEAD = "001a46a543fc83bd6032ea0605cc28d7627ca0d9"
MERGE = "7ef7b6df93936f3dbedefe1dcc362f50fb4f482f"
TREE = "b76f92c664fa51fe25a2fe5df8923cef7efc1611"
AUTH = "owner_directive_2026-09-16_pr2_bp_post_merge_closure"
EFFECT = "runtime_performance_governance_post_merge_lifecycle_reconciliation_only"


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


def test_bp_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load(MAN)
    bp = rows(manifest)["PR2-BP"]

    assert manifest["artifact_version"] == "0.4.40"
    assert bp["status"] == "merged"
    assert bp["completion_state"] == "merged"

    assert bp["pull_request"] == PR
    assert bp["branch_head"] == HEAD
    assert bp["merge_commit"] == MERGE

    assert bp["post_merge_closure_authorization_reference"] == AUTH
    assert bp["post_merge_closure_authority_effect"] == EFFECT
    assert bp["post_merge_closure_recorded_from"] == MERGE
    assert bp["post_merge_closure_tree"] == TREE

    evidence = set(bp["validation_evidence"])

    assert (
        "PR2-BP full local repository suite:"
        "9196 passed, 10 skipped, 2 xfailed, 1 warning"
    ) in evidence

    assert "PR2-BP GitHub Actions CI #217:success" in evidence
    assert "PR2-BP git diff --check:clean" in evidence
    assert (
        "PR2-BP exact seven-file activation footprint:PASS"
        in evidence
    )
    assert "PR2-BP structural authority audit:PASS" in evidence


def test_closure_activates_no_successor_and_preserves_r3():
    manifest = load(MAN)
    by = rows(manifest)

    assert {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    } == set()

    for wid in (
        "PR2-AUDIT",
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    ):
        assert by[wid]["status"] == "blocked"
        assert by[wid]["authorization_reference"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_closure_does_not_change_bp_contract():
    assert (
        CONTRACT.read_text(encoding="utf-8")
        == read_at(MERGE, CONTRACT)
    )


def test_activation_test_is_frozen_at_accepted_merge():
    text = ACTIVATION_TEST.read_text(encoding="utf-8")

    assert f'ACCEPTED_MERGE = "{MERGE}"' in text
    assert "load_at(ACCEPTED_MERGE, MAN)" in text
    assert "read_at(ACCEPTED_MERGE, CONTRACT)" in text
    assert "read_at(ACCEPTED_MERGE, FID_CLOSURE)" in text
    assert "read_at(ACCEPTED_MERGE, PROG)" in text
    assert "read_at(ACCEPTED_MERGE, DEC)" in text


def test_program_and_decision_record_bounded_closure():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.40`" in program
    assert "### 5.37 PR2-BP post-merge closure recording" in program

    for required in (
        AUTH,
        EFFECT,
        HEAD,
        MERGE,
        TREE,
        "PR2-BP is terminal `merged`.",
        "No successor is active after PR2-BP closure.",
        "`PR2-TEST` remains `blocked` and unauthorized.",
        "`R3` remains `ready_pending_authorization`",
    ):
        assert required in program

    assert "PR2-BP-POST-MERGE-CLOSURE-001" in decisions

    for required in (
        AUTH,
        EFFECT,
        HEAD,
        MERGE,
        TREE,
        "No successor is activated by the PR2-BP closure.",
    ):
        assert required in decisions


def test_closure_preserves_bp_nonauthority_boundaries():
    flat = " ".join(
        CONTRACT.read_text(encoding="utf-8").split()
    )

    for required in (
        "Performance is not authority.",
        "Queue position does not create world priority.",
        "Admission is not commitment",
        "Backpressure is operational, not world truth",
        "Wall-clock delay is not logical time",
        "Physical queue order is not authoritative order",
        "Operational priority is not gameplay value",
        "PR2-FID determines whether that transition is semantically lawful.",
        "Backpressure must not leak hidden information",
        "Local and offline operation remain first-class",
        "Implementation remains unauthorized pending separate owner authorization.",
    ):
        assert required in flat
