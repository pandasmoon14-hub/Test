# Executable validation for PR2-EVENT post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_command_event_message_projection_contract.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_event_message_projection_contract.py"

PR = 403
HEAD = "a70cca1310e3a8a70fef40c325c850c69202c6b2"
MERGE = "e9a41cc7b144ffab0ca8fa91c4a9b3a9a1a56214"
TREE = "201998a6eb39814e75e0bd696886eabd6bd0e66e"
AUTH = "owner_directive_2026-09-15_pr2_event_post_merge_closure"
EFFECT = "runtime_message_projection_governance_post_merge_lifecycle_reconciliation_only"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def read_at(ref, path):
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        text=True,
    )


def test_event_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load(MAN)
    event = rows(manifest)["PR2-EVENT"]

    assert manifest["artifact_version"] == "0.4.34"
    assert event["status"] == "merged"
    assert event["completion_state"] == "merged"
    assert event["pull_request"] == PR
    assert event["branch_head"] == HEAD
    assert event["merge_commit"] == MERGE
    assert event["post_merge_closure_authorization_reference"] == AUTH
    assert event["post_merge_closure_authority_effect"] == EFFECT
    assert event["post_merge_closure_recorded_from"] == MERGE
    assert event["post_merge_closure_tree"] == TREE

    evidence = set(event["validation_evidence"])
    assert "PR2-EVENT full local repository suite:9142 passed, 10 skipped, 2 xfailed, 1 warning" in evidence
    assert "PR2-EVENT GitHub Actions CI #205:success" in evidence
    assert "PR2-EVENT git diff --check:clean" in evidence
    assert "PR2-EVENT exact seven-file activation footprint:PASS" in evidence
    assert "PR2-EVENT structural authority audit:PASS" in evidence


def test_closure_activates_no_successor_and_preserves_r3():
    manifest = load(MAN)
    by = rows(manifest)

    assert {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    } == set()

    for wid in (
        "PR2-PERSIST",
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

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_closure_does_not_change_event_contract():
    assert CONTRACT.read_text(encoding="utf-8") == read_at(MERGE, CONTRACT)


def test_activation_test_is_frozen_against_accepted_merge():
    text = ACTIVATION_TEST.read_text(encoding="utf-8")

    assert f'MERGE = "{MERGE}"' in text
    assert "load_at(MERGE, MAN)" in text
    assert "read_at(MERGE, CONTRACT)" in text
    assert "read_at(MERGE, CONC_CLOSURE_TEST)" in text
    assert "read_at(MERGE, PROG)" in text
    assert "read_at(MERGE, DEC)" in text


def test_program_and_decisions_record_bounded_closure():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.34`" in program
    assert "### 5.31 PR2-EVENT post-merge closure recording" in program
    assert AUTH in program
    assert EFFECT in program
    assert HEAD in program
    assert MERGE in program
    assert TREE in program
    assert "PR2-EVENT is terminal `merged`." in program
    assert "No successor is active after PR2-EVENT closure." in program
    assert "PR2-PERSIST remains `blocked` and unauthorized." in program
    assert "PART -> CONC -> EVENT -> PERSIST -> FID -> BP -> R3" in program

    assert "PR2-EVENT-POST-MERGE-CLOSURE-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert HEAD in decisions
    assert MERGE in decisions
    assert TREE in decisions
    assert "No successor is activated by the PR2-EVENT closure." in decisions
