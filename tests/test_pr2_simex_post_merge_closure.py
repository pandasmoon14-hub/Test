# Executable validation for PR2-SIMEX post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_simulation_infrastructure_exemplar_pressure_contract.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_simex_exemplar_pressure_contract.py"

MERGE = "5c48a8e4393374dba3f9f2edc5541c1bb75906f4"
HEAD = "1c0fafaa862f01b623baa51d8e557dd0a3095414"
TREE = "99955d4b9fb54abc494c254fb2364bbfc75d4049"
PR = 395
AUTH = "owner_directive_2026-09-13_pr2_simex_post_merge_closure"
EFFECT = "simulation_infrastructure_exemplar_pressure_governance_post_merge_lifecycle_reconciliation_only"
CLOSURE_SNAPSHOT = "5268f85135b9ad5d67719b37305b204554729bed"


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


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def test_simex_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load_at(CLOSURE_SNAPSHOT, MAN)
    simex = rows(manifest)["PR2-SIMEX"]
    assert manifest["artifact_version"] == "0.4.26"
    assert simex["status"] == "merged"
    assert simex["completion_state"] == "merged"
    assert simex["pull_request"] == PR
    assert simex["branch_head"] == HEAD
    assert simex["merge_commit"] == MERGE
    assert simex["post_merge_closure_authorization_reference"] == AUTH
    assert simex["post_merge_closure_authority_effect"] == EFFECT
    assert simex["post_merge_closure_recorded_from"] == MERGE
    assert simex["post_merge_closure_tree"] == TREE
    evidence = set(simex["validation_evidence"])
    assert "PR2-SIMEX full local repository suite:9072 passed, 10 skipped, 2 xfailed, 1 warning" in evidence
    assert "PR2-SIMEX GitHub Actions CI #189:success" in evidence
    assert "PR2-SIMEX git diff --check:clean" in evidence
    assert "PR2-SIMEX exact seven-file activation footprint:PASS" in evidence
    assert "PR2-SIMEX structural authority audit:PASS" in evidence


def test_closure_activates_no_successor_and_preserves_boundaries():
    manifest = load_at(CLOSURE_SNAPSHOT, MAN)
    by = rows(manifest)
    assert {r["workstream_id"] for r in manifest["workstreams"] if r["status"] == "active"} == set()
    assert by["PR2-SCALE"]["status"] == "blocked"
    assert by["PR2-SCALE"]["authorization_reference"] is None
    assert by["PR2-SCALE"]["starting_baseline"] is None
    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_closure_does_not_change_simex_contract():
    assert CONTRACT.read_text(encoding="utf-8") == read_at(MERGE, CONTRACT)


def test_activation_test_is_frozen_against_merge_snapshot():
    text = ACTIVATION_TEST.read_text(encoding="utf-8")
    assert f'MERGE = "{MERGE}"' in text
    assert "load_at(MERGE, MAN)" in text
    assert "read_at(MERGE, PROG)" in text
    assert "read_at(MERGE, DEC)" in text


def test_program_and_decisions_record_bounded_closure():
    program = read_at(CLOSURE_SNAPSHOT, PROG)
    decisions = read_at(CLOSURE_SNAPSHOT, DEC)
    assert "**Artifact version:** `0.4.26`" in program
    assert "### 5.23 PR2-SIMEX post-merge closure recording" in program
    assert AUTH in program and EFFECT in program and HEAD in program and MERGE in program and TREE in program
    assert "PR2-SIMEX is terminal `merged`" in program
    assert "No successor is active." in program
    assert "PR2-SCALE remains `blocked` and unauthorized." in program
    assert "PR2-SIMEX-POST-MERGE-CLOSURE-001" in decisions
    assert AUTH in decisions and EFFECT in decisions and HEAD in decisions and MERGE in decisions and TREE in decisions
    assert "No successor is activated by this closure." in decisions
