"""Regression tests for Myravant adversarial-attempt evaluation tooling."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "myravant_adversarial_attempt_harness.py"


def _run(report: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(HARNESS), "--report", str(report), "--repository-sha", "a" * 40],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    return json.loads(report.read_text(encoding="utf-8"))


def test_harness_is_deterministic_and_has_no_invariant_failures(tmp_path):
    first = _run(tmp_path / "first.json")
    second = _run(tmp_path / "second.json")
    assert first == second
    assert first["harness_id"] == "myravant.adversarial_attempt_harness"
    assert first["model_mode"] == "MODEL-NONE"
    assert first["authority_effect"] == "none"
    summary = first["summary"]
    assert summary["cases_total"] == 105
    assert summary["cases_failed"] == 0
    assert summary["deterministic_replay_failures"] == 0
    assert summary["canonical_equivalence_failures"] == 0
    assert summary["canonical_equivalence_cases"] >= 40


def test_harness_surfaces_actionable_pressure_classes(tmp_path):
    report = _run(tmp_path / "coverage.json")
    classes = report["summary"]["observed_class_counts"]
    for expected in (
        "ROUTED_COMMIT", "OWNER_REJECTION", "AMBIGUITY_HANDLED",
        "UNINTERPRETABLE_HANDLED", "COMPOUND_PRESSURE", "CAPABILITY_FRONTIER",
        "GENERIC_UNSUPPORTED", "NONMUTATING_OBSERVATION",
    ):
        assert classes.get(expected, 0) > 0, expected

    cases = {row["case"]["case_id"]: row for row in report["cases"]}
    assert cases["light-02"]["primary"]["result_type"] == "object_lit_state_committed"
    assert cases["activation"]["primary"]["failure_class"] == "unsupported_capability_object_activation"
    assert cases["compound"]["primary"]["authoritative_changed"] is False
    assert cases["compound"]["primary"]["command_id"] is None
    assert cases["injection"]["primary"]["failure_class"] == "unsupported_input_no_executable_route"
    assert cases["throwing"]["observed_class"] == "CAPABILITY_FRONTIER"

def test_obs1_harness_covers_targeted_inspection_without_directional_collapse(tmp_path):
    report = _run(tmp_path / "obs1-coverage.json")
    cases = {row["case"]["case_id"]: row for row in report["cases"]}

    for case_id in (
        "inspect-01",
        "inspect-02",
        "inspect-03",
        "inspect-04",
        "inspect-05",
    ):
        row = cases[case_id]
        assert row["primary"]["result_type"] == "inspection"
        assert row["primary"]["authoritative_changed"] is False
        assert row["primary"]["command_id"] is None
        assert row["observed_class"] == "NONMUTATING_OBSERVATION"

    remote = cases["object-inspection-remote"]["primary"]
    unknown = cases["object-inspection-unknown"]["primary"]
    assert remote["result_type"] == unknown["result_type"] == "inspection_unavailable"
    assert remote["failure_class"] == unknown["failure_class"] == "inspection_target_unavailable"
    assert remote["authoritative_changed"] is unknown["authoritative_changed"] is False

    directional = cases["directional-look"]["primary"]
    assert directional["result_type"] == "unsupported_input"
    assert directional["failure_class"] == "unsupported_input_no_executable_route"

    assert cases["inspection-compound"]["observed_class"] == "COMPOUND_PRESSURE"
    assert cases["inspection-injection"]["primary"]["result_type"] == "unsupported_input"
def test_int1_harness_covers_persistent_object_state_without_frontier_collapse(tmp_path):
    report = _run(tmp_path / "int1-coverage.json")
    cases = {row["case"]["case_id"]: row for row in report["cases"]}

    for case_id in ("open-01", "open-02", "close-01", "close-02"):
        row = cases[case_id]
        assert row["primary"]["result_type"] == "object_state_committed"
        assert row["primary"]["authoritative_changed"] is True
        assert row["primary"]["command_id"] is not None
        assert row["observed_class"] == "ROUTED_COMMIT"

    remote = cases["object-state-remote"]["primary"]
    unknown = cases["object-state-unknown"]["primary"]
    assert remote["result_type"] == unknown["result_type"] == "object_state_rejected"
    assert remote["failure_class"] == unknown["failure_class"] == "object_state_target_unavailable"
    assert cases["object-state-remote"]["canonical_equivalence_match"] is True
    assert cases["object-state-unknown"]["canonical_equivalence_match"] is True

    assert cases["object-state-noop"]["observed_class"] == "NOOP_HANDLED"
    assert cases["object-state-compound"]["observed_class"] == "COMPOUND_PRESSURE"
    assert cases["object-state-injection"]["primary"]["result_type"] == "unsupported_input"

    activation = cases["activation"]["primary"]
    assert activation["result_type"] == "unsupported_input"
    assert activation["failure_class"] == "unsupported_capability_object_activation"

    directional = cases["directional-look"]["primary"]
    assert directional["result_type"] == "unsupported_input"
    assert directional["failure_class"] == "unsupported_input_no_executable_route"

def test_int3_harness_covers_bounded_storage_without_generalization(tmp_path):
    report = _run(tmp_path / "int3-coverage.json")
    cases = {row["case"]["case_id"]: row for row in report["cases"]}
    for case_id in (
        "store-01", "store-02", "store-03", "store-04",
        "retrieve-01", "retrieve-02", "retrieve-03",
        "retrieve-transparent-take",
    ):
        assert cases[case_id]["primary"]["result_type"] == "storage_committed"
        assert cases[case_id]["observed_class"] == "ROUTED_COMMIT"
    assert cases["storage-noop"]["observed_class"] == "NOOP_HANDLED"
    assert cases["storage-closed-store"]["primary"]["failure_class"] == "storage_container_closed"
    assert cases["storage-remote"]["primary"]["failure_class"] == "storage_target_unavailable"
    assert cases["storage-not-supported"]["primary"]["failure_class"] == "storage_not_supported"
    assert cases["storage-compound"]["observed_class"] == "COMPOUND_PRESSURE"

def test_comp2_harness_covers_observation_qualified_pickup(tmp_path):
    report = _run(tmp_path / "comp2-coverage.json")
    cases = {row["case"]["case_id"]: row for row in report["cases"]}

    for case_id in (
        "comp2-dark-waystone-01",
        "comp2-dark-waystone-02",
        "comp2-dark-waystone-03",
    ):
        row = cases[case_id]
        primary = row["primary"]
        assert primary["result_type"] == "custody_rejected"
        assert primary["failure_class"] == "PersistentWorldObjectCustodyEvidenceError"
        assert primary["authoritative_changed"] is False
        assert primary["receipt_id"] is None
        assert primary["state_delta_id"] is None
        assert primary["observation_evidence_id"] is not None
        assert primary["opportunity_evidence_id"] is not None
        assert row["deterministic_replay_match"] is True
        assert row["canonical_equivalence_match"] is True

    lit = cases["comp2-lit-waystone-pickup"]
    assert lit["primary"]["result_type"] == "custody_committed"
    assert lit["primary"]["authoritative_changed"] is True
    assert lit["primary"]["observation_evidence_id"] is not None
    assert lit["primary"]["opportunity_evidence_id"] is not None
