# Executable validation for PR2-PERSIST activation.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_persistence_snapshot_replay_recovery_contract.md"
EVENT_CLOSURE = ROOT / "tests/test_pr2_event_post_merge_closure.py"

BASE = "56a5cf065bc37588ee6b62b3a51f1576d0168d6e"
AUTH = "owner_directive_2026-09-15_pr2_persist_activation"
EFFECT = "runtime_persistence_contract_only"
MERGE = "e53e64f92fe2639d68c96bfa70825c6f6ec39f03"


def read_at(ref, path):
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        text=True,
    )


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def load_manifest():
    return load_at(MERGE, MAN)


def rows(data):
    return {row["workstream_id"]: row for row in data["workstreams"]}


def contract_text():
    return read_at(MERGE, CONTRACT)


def test_persist_is_only_active_workstream():
    data = load_manifest()
    by = rows(data)
    persist = by["PR2-PERSIST"]

    assert data["artifact_version"] == "0.4.35"

    assert {
        row["workstream_id"]
        for row in data["workstreams"]
        if row["status"] == "active"
    } == {"PR2-PERSIST"}

    assert persist["status"] == "active"
    assert persist["authorization_reference"] == AUTH
    assert persist["authority_effect"] == EFFECT
    assert persist["starting_baseline"] == BASE
    assert persist["control_artifact"] == "docs/doctrine/control/myravant_persistence_snapshot_replay_recovery_contract.md"
    assert persist["downstream_handoff"] == ["PR2-FID", "PR2-TEST"]
    assert persist["pull_request"] is None
    assert persist["branch_head"] is None
    assert persist["merge_commit"] is None


def test_downstream_authorization_boundaries_remain_closed():
    data = load_manifest()
    by = rows(data)

    for wid in ("PR2-FID", "PR2-BP"):
        assert by[wid]["status"] == "blocked"
        assert by[wid]["authorization_reference"] is None
        assert by[wid]["starting_baseline"] is None

    assert data["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert data["r3_conformance_target"]["candidate_count"] == 34
    assert data["r3_conformance_target"]["execution_authorized"] is False


def test_existing_semantic_owners_are_preserved():
    text = contract_text()

    for required in (
        "AFQR-01 retains qualified state/write ownership",
        "AFQR-02 retains command identity",
        "AFQR-04 retains logical time",
        "R2B-CORE remains authoritative",
        "R2B-CROSS-PHASE retains version identity",
        "R2B-CONTINUITY retains timeline identity",
        "PR2-EVENT retains runtime representation",
    ):
        assert required in text


def test_persistence_never_acquires_semantic_authority():
    text = contract_text()

    for required in (
        "Storage durability is not semantic ownership.",
        "Durability is not semantic commitment.",
        "Snapshot materialization is not canonicality.",
        "Replay reconstruction is not semantic re-execution.",
        "Recovery is not correction.",
        "Replica majority is not semantic authority.",
        "Backup restoration is not branch promotion.",
    ):
        assert required in text


def test_recovery_preserves_randomness_versions_and_audit():
    text = contract_text()

    assert "## 11. Replay reconstruction is not new semantic execution" in text
    assert "## 12. Recovery does not reroll or refresh history" in text
    assert "must not reroll or replace randomness already committed" in text
    assert "cannot claim exact historical reconstruction" in " ".join(text.split())
    assert "Missing durable material does not authorize invented state." in text
    assert "Detected corruption must not be repaired by inventing semantic content." in text


def test_persistence_remains_technology_neutral_and_offline_capable():
    text = contract_text()

    assert "## 26. Local and offline operation remain first-class" in text
    assert "## 27. Topology independence is preserved" in text
    assert "## 30. No storage architecture is mandated" in text

    for required in (
        "event sourcing;",
        "a relational database;",
        "a write-ahead log;",
        "consensus;",
        "cloud storage;",
    ):
        assert required in text


def test_event_closure_is_frozen_at_accepted_merge():
    text = read_at(MERGE, EVENT_CLOSURE)

    assert f'ACCEPTED_MERGE = "{BASE}"' in text
    assert "load_at(ACCEPTED_MERGE, MAN)" in text
    assert "read_at(ACCEPTED_MERGE, CONTRACT)" in text
    assert "read_at(ACCEPTED_MERGE, PROG)" in text
    assert "read_at(ACCEPTED_MERGE, DEC)" in text


def test_program_and_decision_record_bounded_activation():
    program = read_at(MERGE, PROG)
    decisions = read_at(MERGE, DEC)

    assert "**Artifact version:** `0.4.35`" in program
    assert "### 5.32 PR2-PERSIST persistence/recovery activation" in program
    assert AUTH in program
    assert BASE in program
    assert "PR2-PERSIST is the only active runtime successor workstream." in program
    assert "PR2-FID remains `blocked` and unauthorized." in program
    assert "PR2-BP remains `blocked` and unauthorized." in program

    assert "PR2-PERSIST-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions


def test_completion_condition_remains_bounded():
    text = contract_text()

    assert "## 34. Completion condition" in text
    assert "local and offline authoritative continuity remain possible" in text
    assert "PR2-FID and PR2-BP remain separate downstream owners" in text
    assert "R3 remains separately authorized" in text
    assert "Implementation remains separately authorized." in text
