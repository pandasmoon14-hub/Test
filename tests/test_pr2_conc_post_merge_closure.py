# Executable validation for accepted PR2-CONC post-merge closure snapshot.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_deterministic_concurrency_scheduling_contract.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_conc_deterministic_concurrency_contract.py"

PR = 401
HEAD = "684740e41ab3ae10759d6b999c23e8cc6ff9c470"
CONC_MERGE = "5752de38f432c59f9e603ffd1ef38384e621a407"
TREE = "f5cdf3282132537088088ee6aa0592a82354b063"
ACCEPTED_MERGE = "e765d00e57e3a444ecd16078a3390eb49958f5b2"
AUTH = "owner_directive_2026-09-14_pr2_conc_post_merge_closure"
EFFECT = "runtime_concurrency_governance_post_merge_lifecycle_reconciliation_only"


def read_at(ref, path):
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        text=True,
    )


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def test_conc_closure_snapshot_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load_at(ACCEPTED_MERGE, MAN)
    conc = rows(manifest)["PR2-CONC"]
    assert manifest["artifact_version"] == "0.4.32"
    assert conc["status"] == "merged"
    assert conc["completion_state"] == "merged"
    assert conc["pull_request"] == PR
    assert conc["branch_head"] == HEAD
    assert conc["merge_commit"] == CONC_MERGE
    assert conc["post_merge_closure_authorization_reference"] == AUTH
    assert conc["post_merge_closure_authority_effect"] == EFFECT
    assert conc["post_merge_closure_recorded_from"] == CONC_MERGE
    assert conc["post_merge_closure_tree"] == TREE
    evidence = set(conc["validation_evidence"])
    assert "PR2-CONC full local repository suite:9119 passed, 10 skipped, 2 xfailed, 1 warning" in evidence
    assert "PR2-CONC GitHub Actions CI #201:success" in evidence
    assert "PR2-CONC git diff --check:clean" in evidence
    assert "PR2-CONC exact seven-file activation footprint:PASS" in evidence
    assert "PR2-CONC structural authority audit:PASS" in evidence


def test_conc_closure_snapshot_activated_no_successor_and_preserved_r3():
    manifest = load_at(ACCEPTED_MERGE, MAN)
    by = rows(manifest)
    assert {row["workstream_id"] for row in manifest["workstreams"] if row["status"] == "active"} == set()
    for wid in (
        "PR2-EVENT", "PR2-PERSIST", "PR2-FID", "PR2-BP",
        "PR2-AUDIT", "PR2-MIG", "PR2-TEST", "PR2-IMPL",
    ):
        assert by[wid]["status"] == "blocked"
        assert by[wid]["authorization_reference"] is None
        assert by[wid]["starting_baseline"] is None
    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_conc_closure_snapshot_did_not_change_conc_contract():
    assert read_at(ACCEPTED_MERGE, CONTRACT) == read_at(CONC_MERGE, CONTRACT)


def test_conc_activation_test_snapshot_is_frozen_against_accepted_activation_merge():
    text = read_at(ACCEPTED_MERGE, ACTIVATION_TEST)
    assert f'MERGE = "{CONC_MERGE}"' in text
    assert "load_at(MERGE, MAN)" in text
    assert "read_at(MERGE, CONTRACT)" in text
    assert "read_at(MERGE, PART_CLOSURE_TEST)" in text
    assert "read_at(MERGE, PROG)" in text
    assert "read_at(MERGE, DEC)" in text


def test_conc_closure_snapshot_program_and_decisions_are_bounded():
    program = read_at(ACCEPTED_MERGE, PROG)
    decisions = read_at(ACCEPTED_MERGE, DEC)
    assert "**Artifact version:** `0.4.32`" in program
    assert "### 5.29 PR2-CONC post-merge closure recording" in program
    assert AUTH in program and EFFECT in program and HEAD in program and CONC_MERGE in program and TREE in program
    assert "PR2-CONC is terminal `merged`." in program
    assert "No successor is active after PR2-CONC closure." in program
    assert "PR2-EVENT remains `blocked` and unauthorized." in program
    assert "PART -> CONC -> EVENT -> PERSIST -> FID -> BP -> R3" in program
    assert "PR2-CONC-POST-MERGE-CLOSURE-001" in decisions
    assert AUTH in decisions and EFFECT in decisions and HEAD in decisions and CONC_MERGE in decisions and TREE in decisions
    assert "No successor is activated by the PR2-CONC closure." in decisions
