# Executable validation for PR2-SCALE post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_runtime_scalability_execution_topology_contract.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_scale_runtime_scalability_contract.py"

PR = 397
HEAD = "01f82d331792e266e44b59ffc261e9b55f15decf"
MERGE = "862ee41369ec8cba5768cb13aa59ecd853a7f8c4"
TREE = "77717680ea254bb81043a7109b4842164834c925"
AUTH = "owner_directive_2026-09-14_pr2_scale_post_merge_closure"
EFFECT = "runtime_scalability_governance_post_merge_lifecycle_reconciliation_only"


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


def test_scale_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load(MAN)
    scale = rows(manifest)["PR2-SCALE"]
    assert manifest["artifact_version"] == "0.4.28"
    assert scale["status"] == "merged"
    assert scale["completion_state"] == "merged"
    assert scale["pull_request"] == PR
    assert scale["branch_head"] == HEAD
    assert scale["merge_commit"] == MERGE
    assert scale["post_merge_closure_authorization_reference"] == AUTH
    assert scale["post_merge_closure_authority_effect"] == EFFECT
    assert scale["post_merge_closure_recorded_from"] == MERGE
    assert scale["post_merge_closure_tree"] == TREE
    evidence = set(scale["validation_evidence"])
    assert "PR2-SCALE full local repository suite:9087 passed, 10 skipped, 2 xfailed, 1 warning" in evidence
    assert "PR2-SCALE GitHub Actions CI #193:success" in evidence
    assert "PR2-SCALE git diff --check:clean" in evidence
    assert "PR2-SCALE exact seven-file activation footprint:PASS" in evidence
    assert "PR2-SCALE structural authority audit:PASS" in evidence


def test_closure_activates_no_successor_and_preserves_r3():
    manifest = load(MAN)
    by = rows(manifest)
    assert {row["workstream_id"] for row in manifest["workstreams"] if row["status"] == "active"} == set()
    for wid in (
        "PR2-PART", "PR2-CONC", "PR2-FID", "PR2-EVENT", "PR2-PERSIST",
        "PR2-BP", "PR2-AUDIT", "PR2-MIG", "PR2-TEST", "PR2-IMPL",
    ):
        assert by[wid]["status"] == "blocked"
        assert by[wid]["authorization_reference"] is None
        assert by[wid]["starting_baseline"] is None
    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_closure_does_not_change_scale_contract():
    assert CONTRACT.read_text(encoding="utf-8") == read_at(MERGE, CONTRACT)


def test_activation_test_is_frozen_against_merge_snapshot():
    text = ACTIVATION_TEST.read_text(encoding="utf-8")
    assert f'MERGE = "{MERGE}"' in text
    assert "load_at(MERGE, MAN)" in text
    assert "read_at(MERGE, CONTRACT)" in text
    assert "read_at(MERGE, PROG)" in text
    assert "read_at(MERGE, DEC)" in text
    assert "read_at(MERGE, SIMEX_CLOSURE_TEST)" in text


def test_program_and_decisions_record_bounded_closure():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")
    assert "**Artifact version:** `0.4.28`" in program
    assert "### 5.25 PR2-SCALE post-merge closure recording" in program
    assert AUTH in program and EFFECT in program and HEAD in program and MERGE in program and TREE in program
    assert "PR2-SCALE is terminal `merged`." in program
    assert "No successor is active after PR2-SCALE closure." in program
    assert "PR2-PART, PR2-CONC, PR2-FID, PR2-EVENT, PR2-PERSIST, and PR2-BP remain `blocked` and unauthorized." in program
    assert "PR2-SCALE-POST-MERGE-CLOSURE-001" in decisions
    assert AUTH in decisions and EFFECT in decisions and HEAD in decisions and MERGE in decisions and TREE in decisions
    assert "No successor is activated by the PR2-SCALE closure." in decisions
