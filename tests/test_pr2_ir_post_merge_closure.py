# Executable validation for PR2-IR post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_source_design_information_barrier_contract.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_ir_information_barrier.py"

MERGE = "2b9c21fae92dd210a12e5f7e3d6c8d8931db0201"
HEAD = "ac48a9896840e5b9b236de8f7b4cc0febd9fdf5a"
TREE = "8e99389020a3626e32dc7cb17e62cec081d96e54"
PR = 389
AUTH = "owner_directive_2026-09-12_pr2_ir_post_merge_closure"
EFFECT = "information_barrier_post_merge_lifecycle_reconciliation_only"


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


def test_ir_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load(MAN)
    by = rows(manifest)
    ir = by["PR2-IR"]

    assert manifest["artifact_version"] == "0.4.20"
    assert ir["status"] == "merged"
    assert ir["completion_state"] == "merged"
    assert ir["pull_request"] == PR
    assert ir["branch_head"] == HEAD
    assert ir["merge_commit"] == MERGE
    assert ir["post_merge_closure_authorization_reference"] == AUTH
    assert ir["post_merge_closure_authority_effect"] == EFFECT
    assert ir["post_merge_closure_recorded_from"] == MERGE
    assert ir["post_merge_closure_tree"] == TREE

    evidence = set(ir["validation_evidence"])
    assert "PR2-IR focused validation:PASS" in evidence
    assert "PR2-IR full local repository suite:9029 passed, 10 skipped, 2 xfailed, 1 warning" in evidence
    assert "PR2-IR GitHub Actions CI #177:success" in evidence
    assert "PR2-IR git diff --check:clean" in evidence
    assert "PR2-IR semantic audit:PASS" in evidence


def test_closure_activates_no_successor_and_preserves_r3():
    manifest = load(MAN)
    by = rows(manifest)

    active = {row["workstream_id"] for row in manifest["workstreams"] if row["status"] == "active"}
    assert active == set()

    for wid in ("PR2-CORPUS", "PR2-FICT", "PR2-SIMEX"):
        assert by[wid]["status"] == "ready_pending_authorization"
        assert by[wid]["authorization_reference"] is None
        assert by[wid]["starting_baseline"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_closure_does_not_change_ir_contract():
    assert CONTRACT.read_text(encoding="utf-8") == read_at(MERGE, CONTRACT)


def test_activation_test_is_frozen_against_merge_snapshot():
    text = ACTIVATION_TEST.read_text(encoding="utf-8")
    assert f'MERGE = "{MERGE}"' in text
    assert "load_at(MERGE, MAN)" in text
    assert "read_at(MERGE, PROG)" in text
    assert "read_at(MERGE, DEC)" in text


def test_program_and_decisions_record_bounded_closure():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.20`" in program
    assert "### 5.17 PR2-IR post-merge closure recording" in program
    assert AUTH in program
    assert EFFECT in program
    assert HEAD in program
    assert MERGE in program
    assert TREE in program
    assert "PR2-IR is terminal `merged`" in program
    assert "No successor is\nactive." in program

    assert "PR2-IR-POST-MERGE-CLOSURE-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert HEAD in decisions
    assert MERGE in decisions
    assert TREE in decisions
    assert "No successor is\nactivated by this closure." in decisions
