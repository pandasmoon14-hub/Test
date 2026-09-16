# Executable validation for PR2-FID activation.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_relevance_fidelity_aggregation_reconstitution_contract.md"
PERSIST_CLOSURE = ROOT / "tests/test_pr2_persist_post_merge_closure.py"

BASE = "bc79bc629f3cc6bff220c8e71c37d9df515b9f8c"
AUTH = "owner_directive_2026-09-15_pr2_fid_activation"
EFFECT = "runtime_fidelity_contract_only"
ACCEPTED_MERGE = "c077abf5a90e896ef535d4956c49803cbf8163b6"


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


def load_manifest():
    return load_at(ACCEPTED_MERGE, MAN)


def rows(data):
    return {
        row["workstream_id"]: row
        for row in data["workstreams"]
    }


def contract_text():
    return read_at(ACCEPTED_MERGE, CONTRACT)


def test_fid_is_only_active_workstream():
    data = load_manifest()
    by = rows(data)
    fid = by["PR2-FID"]

    assert data["artifact_version"] == "0.4.37"

    assert {
        row["workstream_id"]
        for row in data["workstreams"]
        if row["status"] == "active"
    } == {"PR2-FID"}

    assert fid["status"] == "active"
    assert fid["authorization_reference"] == AUTH
    assert fid["authority_effect"] == EFFECT
    assert fid["starting_baseline"] == BASE
    assert fid["control_artifact"] == "docs/doctrine/control/myravant_relevance_fidelity_aggregation_reconstitution_contract.md"
    assert fid["downstream_handoff"] == ["PR2-BP", "PR2-TEST"]
    assert fid["pull_request"] is None
    assert fid["branch_head"] is None
    assert fid["merge_commit"] is None


def test_downstream_authorization_boundaries_remain_closed():
    data = load_manifest()
    by = rows(data)

    for wid in ("PR2-BP", "PR2-TEST"):
        assert by[wid]["status"] == "blocked"
        assert by[wid]["authorization_reference"] is None
        assert by[wid]["starting_baseline"] is None

    assert data["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert data["r3_conformance_target"]["candidate_count"] == 34
    assert data["r3_conformance_target"]["execution_authorized"] is False


def test_relevance_is_multidimensional_and_non_authoritative():
    text = contract_text()

    assert "Relevance is multidimensional and scoped." in text
    assert (
        "Camera distance, player proximity, visibility, and render "
        "presence are not authority."
    ) in text
    assert "Fidelity is not truth rank." in text
    assert "Fidelity is not identity rank." in text
    assert "Fidelity is not commitment rank." in text


def test_no_universal_fidelity_tiers_or_full_detail_requirement():
    text = contract_text()

    assert "There is no universal fidelity-tier list." in text
    assert "## 8. No full-fidelity-everywhere requirement" in text
    assert (
        "The requirement is semantic preservation, not a specific "
        "simulation architecture."
    ) in " ".join(text.split())


def test_committed_detail_and_unresolved_detail_remain_distinct():
    text = contract_text()

    assert (
        "Previously committed detail may be omitted from an active "
        "representation but is not thereby erased."
    ) in text

    assert "Unresolved detail is not committed detail." in text

    assert (
        "A fidelity transition is not a commitment event."
    ) in text


def test_aggregation_preserves_scope_and_cannot_invent_microstate():
    text = contract_text()

    assert "## 11. Aggregation qualification" in text

    assert (
        "Aggregation must not manufacture a microstate merely because "
        "an aggregate value exists."
    ) in text

    assert "## 13. Aggregation cannot create illegal states" in text

    assert (
        "Approximation is not permission to violate rules."
    ) in text


def test_reconstitution_and_materialization_are_distinct():
    text = contract_text()

    assert (
        "Reconstitution and materialization are not synonyms."
    ) in text

    assert (
        "Reconstitution must not claim to recover detail that was "
        "never retained or committed."
    ) in text

    assert (
        "A fidelity increase alone grants no authority to materialize "
        "new facts."
    ) in text

    assert "## 16. No invented history during promotion" in text


def test_cross_fidelity_commitment_requires_sufficient_detail():
    text = contract_text()

    flat = " ".join(text.split())

    assert (
        "If omitted detail is material to an authoritative decision, "
        "the required scope must be lawfully reconstituted or "
        "materialized before commitment."
    ) in flat

    assert (
        "A low-fidelity approximation must not silently decide an "
        "outcome that requires unavailable higher-resolution facts."
    ) in " ".join(text.split())


def test_background_foreground_reconciliation_keeps_other_owners():
    text = contract_text()

    assert "Lower fidelity does not authorize time passage." in text

    assert (
        "Foreground promotion must reconcile all semantically relevant "
        "background consequences"
    ) in " ".join(text.split())

    assert "PR2-PERSIST owns durable recovery of that basis." in text
    assert "PR2-BP owns performance budgets, overload, and backpressure." in text


def test_player_freedom_survives_fidelity_reduction():
    text = contract_text()

    assert (
        "Fidelity reduction is not a lawful reason to reject a "
        "fictionally coherent player attempt."
    ) in text

    assert (
        "A closed command menu must not be introduced merely to protect "
        "an aggregation shortcut."
    ) in " ".join(text.split())


def test_fidelity_cycle_equivalence_and_topology_separation():
    text = contract_text()

    assert "## 25. Fidelity-cycle equivalence" in text
    assert "## 29. Partitioning and concurrency remain separate" in text
    assert "Fidelity boundaries are not automatically partition boundaries." in text


def test_persist_closure_is_frozen_at_accepted_merge():
    text = read_at(ACCEPTED_MERGE, PERSIST_CLOSURE)

    assert f'ACCEPTED_MERGE = "{BASE}"' in text
    assert "load_at(ACCEPTED_MERGE, MAN)" in text
    assert "read_at(ACCEPTED_MERGE, CONTRACT)" in text
    assert "read_at(ACCEPTED_MERGE, ACTIVATION_TEST)" in text
    assert "read_at(ACCEPTED_MERGE, PROG)" in text
    assert "read_at(ACCEPTED_MERGE, DEC)" in text


def test_program_and_decisions_record_bounded_fid_activation():
    program = read_at(ACCEPTED_MERGE, PROG)
    decisions = read_at(ACCEPTED_MERGE, DEC)

    assert "**Artifact version:** `0.4.37`" in program
    assert (
        "### 5.34 PR2-FID "
        "relevance/fidelity/aggregation/reconstitution activation"
        in program
    )
    assert AUTH in program
    assert BASE in program
    assert "docs/doctrine/control/myravant_relevance_fidelity_aggregation_reconstitution_contract.md" in program
    assert (
        "PR2-FID is the only active runtime successor workstream."
        in program
    )
    assert "PR2-BP remains `blocked` and unauthorized." in program

    assert "PR2-FID-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions


def test_completion_condition_remains_bounded():
    text = contract_text()

    assert "## 35. Completion condition" in text
    assert (
        "PR2-BP, PR2-TEST, R3, and implementation remain "
        "separately authorized."
    ) in text
    assert "Implementation remains separately authorized." in text
