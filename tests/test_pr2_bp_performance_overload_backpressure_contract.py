# Executable validation for PR2-BP activation.
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_performance_budget_overload_backpressure_contract.md"
FID_CLOSURE = ROOT / "tests/test_pr2_fid_post_merge_closure.py"

BASE = "59520af5f2a68a5979091c00bb632f0cb5d2600e"
AUTH = "owner_directive_2026-09-16_pr2_bp_activation"
EFFECT = "runtime_performance_contract_only"


def manifest():
    return json.loads(MAN.read_text(encoding="utf-8"))


def rows(data):
    return {
        row["workstream_id"]: row
        for row in data["workstreams"]
    }


def contract_text():
    return CONTRACT.read_text(encoding="utf-8")


def flat_contract():
    return " ".join(contract_text().split())


def test_bp_is_only_active_runtime_workstream():
    data = manifest()
    by = rows(data)
    bp = by["PR2-BP"]

    assert data["artifact_version"] == "0.4.39"

    assert {
        row["workstream_id"]
        for row in data["workstreams"]
        if row["status"] == "active"
    } == {"PR2-BP"}

    assert bp["status"] == "active"
    assert bp["authorization_reference"] == AUTH
    assert bp["authority_effect"] == EFFECT
    assert bp["starting_baseline"] == BASE
    assert bp["control_artifact"] == "docs/doctrine/control/myravant_performance_budget_overload_backpressure_contract.md"
    assert bp["downstream_handoff"] == ["PR2-TEST"]
    assert bp["pull_request"] is None
    assert bp["branch_head"] is None
    assert bp["merge_commit"] is None


def test_downstream_boundaries_remain_closed():
    data = manifest()
    by = rows(data)

    for wid in (
        "PR2-AUDIT",
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    ):
        assert by[wid]["status"] == "blocked"
        assert by[wid]["authorization_reference"] is None

    assert data["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert data["r3_conformance_target"]["candidate_count"] == 34
    assert data["r3_conformance_target"]["execution_authorized"] is False


def test_performance_remains_non_authoritative():
    flat = flat_contract()

    for required in (
        "Performance pressure may change how and when lawful work is serviced, but may not silently change authoritative world meaning.",
        "Performance is not authority.",
        "Queue position does not create world priority.",
        "Worker availability does not create legality.",
    ):
        assert required in flat


def test_budgets_require_measured_context():
    flat = flat_contract()

    assert "A performance budget is meaningful only relative to a declared workload envelope." in flat
    assert "Numeric values must retain their measurement context." in flat
    assert "Performance numbers are not correctness proofs" in flat


def test_unbounded_queue_assumption_is_rejected():
    flat = flat_contract()

    assert "## 9. No infinite-capacity assumption" in flat
    assert "## 10. Bounded buffering law" in flat
    assert "What happens when the bound is reached must be explicit." in flat
    assert "Overflow cannot mean silent disappearance" in flat


def test_admission_commitment_and_deferral_remain_distinct():
    flat = flat_contract()

    assert "Admission is not commitment" in flat
    assert "Deferred work remains attributable" in flat
    assert "Once existing doctrine says an attempt, command, obligation, or committed effect exists, overload may not pretend it never existed." in flat


def test_backpressure_does_not_become_world_semantics():
    flat = flat_contract()

    assert "Backpressure is operational, not world truth" in flat
    assert "Wall-clock delay is not logical time" in flat
    assert "Physical queue order is not authoritative order" in flat
    assert "Operational priority is not gameplay value" in flat


def test_degradation_remains_lawful_and_fid_owned():
    flat = flat_contract()

    assert "Performance pressure does not authorize:" in flat
    assert "PR2-FID determines whether that transition is semantically lawful." in flat
    assert "BP does not acquire authority to aggregate, omit, materialize, or reconstitute detail" in flat


def test_hotspot_and_recovery_boundaries_are_explicit():
    flat = flat_contract()

    assert "Hotspots are scoped pressure, not semantic regions" in flat
    assert "Hotspot status does not create:" in flat
    assert "Recovery from overload" in flat
    assert "Backlog replay is not semantic replay" in flat
    assert "Retry storms must be bounded" in flat


def test_hidden_information_and_player_freedom_are_preserved():
    flat = flat_contract()

    assert "Backpressure must not leak hidden information" in flat
    assert "A fictionally coherent attempt does not become fictionally incoherent because the runtime is busy." in flat
    assert "It may not invent a gameplay prohibition solely to conceal capacity limits." in flat


def test_local_offline_and_technology_neutrality_are_preserved():
    flat = flat_contract()

    assert "Local and offline operation remain first-class" in flat
    assert "A cloud service is not required for campaign continuity." in flat
    assert "PR2-BP mandates none of the following:" in flat
    assert "Implementation follows evidence" in flat


def test_r3_and_implementation_remain_separate():
    flat = flat_contract()

    assert "PR2-BP does not execute R3." in flat
    assert "R3 remains separately authorized against its exact 34-record target." in flat
    assert "PR2-TEST remains separately unauthorized." in flat
    assert "Implementation remains unauthorized pending separate owner authorization." in flat


def test_fid_closure_is_frozen_at_accepted_merge():
    text = FID_CLOSURE.read_text(encoding="utf-8")

    assert f'ACCEPTED_MERGE = "{BASE}"' in text
    assert "load_at(ACCEPTED_MERGE, MAN)" in text
    assert "read_at(ACCEPTED_MERGE, CONTRACT)" in text
    assert "read_at(ACCEPTED_MERGE, ACTIVATION_TEST)" in text
    assert "read_at(ACCEPTED_MERGE, PROG)" in text
    assert "read_at(ACCEPTED_MERGE, DEC)" in text


def test_program_and_decisions_record_bounded_bp_activation():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.39`" in program
    assert (
        "### 5.36 PR2-BP performance budgets, "
        "overload, and backpressure activation"
        in program
    )

    assert AUTH in program
    assert BASE in program
    assert "docs/doctrine/control/myravant_performance_budget_overload_backpressure_contract.md" in program
    assert "PR2-BP is the only active runtime successor workstream." in program
    assert "PR2-TEST remains blocked and unauthorized." in program

    assert "PR2-BP-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions


def test_completion_condition_remains_bounded():
    flat = flat_contract()

    assert "## 44. Completion condition" in flat
    assert "PR2-TEST, R3, and implementation remain unauthorized pending separate owner authorization." in flat
    assert "Implementation remains unauthorized pending separate owner authorization." in flat
