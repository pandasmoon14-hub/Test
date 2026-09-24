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
    assert summary["cases_total"] >= 50
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
    assert cases["compound"]["primary"]["authoritative_changed"] is False
    assert cases["compound"]["primary"]["command_id"] is None
    assert cases["injection"]["primary"]["failure_class"] == "unsupported_input_no_executable_route"
    assert cases["throwing"]["observed_class"] == "CAPABILITY_FRONTIER"
