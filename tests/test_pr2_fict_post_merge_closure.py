# Executable validation for PR2-FICT post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_fiction_litrpg_experience_pressure_contract.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_fict_experience_pressure_contract.py"

MERGE = "6a768616166d35fcf51dd8345895847e0554ed28"
HEAD = "31e5c4f71eef200ee7ad43c0c9f76ec6995ed806"
TREE = "105b51247673fc7941491bc743e4100d7d317701"
PR = 393
AUTH = "owner_directive_2026-09-12_pr2_fict_post_merge_closure"
EFFECT = "fiction_pressure_governance_post_merge_lifecycle_reconciliation_only"


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


def test_fict_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load(MAN)
    by = rows(manifest)
    fict = by["PR2-FICT"]

    assert manifest["artifact_version"] == "0.4.24"
    assert fict["status"] == "merged"
    assert fict["completion_state"] == "merged"
    assert fict["pull_request"] == PR
    assert fict["branch_head"] == HEAD
    assert fict["merge_commit"] == MERGE
    assert fict["post_merge_closure_authorization_reference"] == AUTH
    assert fict["post_merge_closure_authority_effect"] == EFFECT
    assert fict["post_merge_closure_recorded_from"] == MERGE
    assert fict["post_merge_closure_tree"] == TREE

    evidence = set(fict["validation_evidence"])
    assert "PR2-FICT full local repository suite:9057 passed, 10 skipped, 2 xfailed, 1 warning" in evidence
    assert "PR2-FICT GitHub Actions CI #185:success" in evidence
    assert "PR2-FICT git diff --check:clean" in evidence
    assert "PR2-FICT exact seven-file activation footprint:PASS" in evidence
    assert "PR2-FICT adversarial structural audit:PASS" in evidence


def test_closure_activates_no_successor_and_preserves_execution_boundaries():
    manifest = load(MAN)
    by = rows(manifest)

    active = {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    }
    assert active == set()

    simex = by["PR2-SIMEX"]
    assert simex["status"] == "ready_pending_authorization"
    assert simex["authorization_reference"] is None
    assert simex["starting_baseline"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_closure_does_not_change_fict_contract():
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

    assert "**Artifact version:** `0.4.24`" in program
    assert "### 5.21 PR2-FICT post-merge closure recording" in program
    assert AUTH in program
    assert EFFECT in program
    assert HEAD in program
    assert MERGE in program
    assert TREE in program
    assert "PR2-FICT is terminal `merged`" in program
    assert "No successor is active." in program
    assert "PR2-SIMEX` remains `ready_pending_authorization`" in program
    assert "corpus execution" in program
    assert "R3 remains `ready_pending_authorization`" in program

    assert "PR2-FICT-POST-MERGE-CLOSURE-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert HEAD in decisions
    assert MERGE in decisions
    assert TREE in decisions
    assert "No successor is activated by this closure." in decisions
    assert "corpus execution" in decisions
    assert "R3 remains" in decisions
