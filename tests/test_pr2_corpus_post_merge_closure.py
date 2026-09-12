# Executable validation for PR2-CORPUS post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_corpus_scale_coverage_governance.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_corpus_scale_coverage_governance.py"

MERGE = "e8e2c0cef0fb1d9b7fdf758fb221f9d9b9ad3bb1"
HEAD = "f9881379bbbd492674c938724349da41fcd55141"
TREE = "ae9949d1d34cb3208f7036d8bee74f6ca8c7e87b"
PR = 391
AUTH = "owner_directive_2026-09-12_pr2_corpus_post_merge_closure"
EFFECT = "corpus_governance_post_merge_lifecycle_reconciliation_only"


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


def test_corpus_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load(MAN)
    by = rows(manifest)
    corpus = by["PR2-CORPUS"]

    assert manifest["artifact_version"] == "0.4.22"
    assert corpus["status"] == "merged"
    assert corpus["completion_state"] == "merged"
    assert corpus["pull_request"] == PR
    assert corpus["branch_head"] == HEAD
    assert corpus["merge_commit"] == MERGE
    assert corpus["post_merge_closure_authorization_reference"] == AUTH
    assert corpus["post_merge_closure_authority_effect"] == EFFECT
    assert corpus["post_merge_closure_recorded_from"] == MERGE
    assert corpus["post_merge_closure_tree"] == TREE

    evidence = set(corpus["validation_evidence"])
    assert "PR2-CORPUS focused validation:77 passed" in evidence
    assert "PR2-CORPUS full local repository suite:9043 passed, 10 skipped, 2 xfailed, 1 warning" in evidence
    assert "PR2-CORPUS GitHub Actions CI #181:success" in evidence
    assert "PR2-CORPUS git diff --check:clean" in evidence
    assert "PR2-CORPUS semantic audit:PASS" in evidence


def test_closure_activates_no_successor_and_preserves_execution_boundaries():
    manifest = load(MAN)
    by = rows(manifest)

    active = {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    }
    assert active == set()

    for wid in ("PR2-FICT", "PR2-SIMEX"):
        assert by[wid]["status"] == "ready_pending_authorization"
        assert by[wid]["authorization_reference"] is None
        assert by[wid]["starting_baseline"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_closure_does_not_change_corpus_contract():
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

    assert "**Artifact version:** `0.4.22`" in program
    assert "### 5.19 PR2-CORPUS post-merge closure recording" in program
    assert AUTH in program
    assert EFFECT in program
    assert HEAD in program
    assert MERGE in program
    assert TREE in program
    assert "PR2-CORPUS is terminal `merged`" in program
    assert "No successor is active." in program
    assert "Corpus\nexecution remains unauthorized." in program

    assert "PR2-CORPUS-POST-MERGE-CLOSURE-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert HEAD in decisions
    assert MERGE in decisions
    assert TREE in decisions
    assert "No successor is activated by this\nclosure." in decisions
    assert "Corpus execution remains unauthorized." in decisions
