# Executable validation for PR2-FID post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_relevance_fidelity_aggregation_reconstitution_contract.md"
ACTIVATION_TEST = ROOT / "tests/test_pr2_fid_relevance_fidelity_contract.py"

PR = 407
HEAD = "6a3fd4de79fb421fc03352b311c1168faa71255a"
MERGE = "c077abf5a90e896ef535d4956c49803cbf8163b6"
TREE = "766d61cb47101f15eefb14db88607f3473c006e3"
AUTH = "owner_directive_2026-09-16_pr2_fid_post_merge_closure"
EFFECT = "runtime_fidelity_governance_post_merge_lifecycle_reconciliation_only"


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


def test_fid_is_terminal_merged_with_exact_acceptance_evidence():
    manifest = load(MAN)
    fid = rows(manifest)["PR2-FID"]

    assert manifest["artifact_version"] == "0.4.38"

    assert fid["status"] == "merged"
    assert fid["completion_state"] == "merged"

    assert fid["pull_request"] == PR
    assert fid["branch_head"] == HEAD
    assert fid["merge_commit"] == MERGE

    assert (
        fid["post_merge_closure_authorization_reference"]
        == AUTH
    )
    assert fid["post_merge_closure_authority_effect"] == EFFECT
    assert fid["post_merge_closure_recorded_from"] == MERGE
    assert fid["post_merge_closure_tree"] == TREE

    evidence = set(fid["validation_evidence"])

    assert (
        "PR2-FID full local repository suite:"
        "9175 passed, 10 skipped, 2 xfailed, 1 warning"
    ) in evidence

    assert "PR2-FID GitHub Actions CI #213:success" in evidence
    assert "PR2-FID git diff --check:clean" in evidence
    assert (
        "PR2-FID exact seven-file activation footprint:PASS"
        in evidence
    )
    assert "PR2-FID structural authority audit:PASS" in evidence


def test_closure_activates_no_successor_and_preserves_r3():
    manifest = load(MAN)
    by = rows(manifest)

    assert {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    } == set()

    for wid in (
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

    assert (
        manifest["r3_conformance_target"]["candidate_count"]
        == 34
    )

    assert (
        manifest["r3_conformance_target"]["execution_authorized"]
        is False
    )


def test_closure_does_not_change_fid_contract():
    assert (
        CONTRACT.read_text(encoding="utf-8")
        == read_at(MERGE, CONTRACT)
    )


def test_activation_test_is_frozen_at_accepted_merge():
    text = ACTIVATION_TEST.read_text(encoding="utf-8")

    assert f'ACCEPTED_MERGE = "{MERGE}"' in text
    assert "load_at(ACCEPTED_MERGE, MAN)" in text
    assert "read_at(ACCEPTED_MERGE, CONTRACT)" in text
    assert "read_at(ACCEPTED_MERGE, PERSIST_CLOSURE)" in text
    assert "read_at(ACCEPTED_MERGE, PROG)" in text
    assert "read_at(ACCEPTED_MERGE, DEC)" in text


def test_program_and_decision_record_bounded_closure():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.38`" in program
    assert (
        "### 5.35 PR2-FID post-merge closure recording"
        in program
    )

    assert AUTH in program
    assert EFFECT in program
    assert HEAD in program
    assert MERGE in program
    assert TREE in program

    assert "PR2-FID is terminal `merged`." in program
    assert (
        "No successor is active after PR2-FID closure."
        in program
    )
    assert "PR2-BP remains `blocked` and unauthorized." in program
    assert "PR2-TEST remains blocked and unauthorized." in program

    assert (
        "PART -> CONC -> EVENT -> PERSIST -> FID -> BP -> R3"
        in program
    )

    assert "PR2-FID-POST-MERGE-CLOSURE-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert HEAD in decisions
    assert MERGE in decisions
    assert TREE in decisions

    assert (
        "No successor is activated by the PR2-FID closure."
        in decisions
    )


def test_closure_preserves_fid_nonauthority_boundaries():
    text = CONTRACT.read_text(encoding="utf-8")

    flat = " ".join(text.split())

    for required in (
        "Relevance is multidimensional and scoped.",
        "Fidelity is not truth rank.",
        "Fidelity is not identity rank.",
        "Fidelity is not commitment rank.",
        "A fidelity transition is not a commitment event.",
        "Unresolved detail is not committed detail.",
        "There is no universal fidelity-tier list.",
        "Implementation remains separately authorized.",
    ):
        assert required in flat
