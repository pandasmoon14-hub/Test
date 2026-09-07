"""Executable validation for AFQR R2A-12 independent completion."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BASE = "f48bba1bab9fc8b597ab0e96920853485f26a6bb"
R2A11_CERTIFIED_HEAD = "d3a5c7f17a4709e2422661d8063e6a134a857798"

REVIEW = (
    ROOT
    / "docs/doctrine/reviews/afqr_r2a_independent_completion_review.md"
)
MANIFEST = (
    ROOT
    / "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml"
)
CONTROL = (
    ROOT
    / "docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md"
)
QPM = (
    ROOT
    / "docs/doctrine/reviews/r2a/question_package_module/index.yaml"
)

AUTHORIZED = {
    "docs/doctrine/reviews/afqr_r2a_independent_completion_review.md",
    "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
    "docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md",
    "tests/test_afqr_r2a11_question_package_module.py",
    "tests/test_afqr_r2a12_independent_completion_review.py",
    "tests/test_afqr_r2a7_deterministic_stream_repair.py",
    "tests/test_afqr_r2a_inventory_contract.py",
}


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def git_bytes(ref: str, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
    )


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_r2a12_review_records_independent_pass_and_limits():
    text = REVIEW.read_text(encoding="utf-8")

    required = [
        "**Review result:** `PASS`",
        "partition-chain integrity",
        "inventory-contract integrity",
        "semantic-surface integrity",
        "Thirty-one claim assessments",
        "Eleven unresolved owner questions",
        "Independent package challenge",
        "Authority-layer separation",
        "Corpus-scale robustness",
        "`R2A=complete`",
        "`R2B=ready`",
        "`R2C=blocked`",
        "No required R2B package or module is authorized by this review.",
    ]

    for value in required:
        assert value in text


def test_r2a12_manifest_transition_is_exact():
    predecessor = json.loads(git_bytes(BASE, MANIFEST.relative_to(ROOT).as_posix()))
    current = load(MANIFEST)

    assert predecessor["artifact_version"] == "0.2.18"
    assert current["artifact_version"] == "0.2.19"

    assert predecessor["status"] == "active_incomplete"
    assert current["status"] == "complete"

    before = {row["partition_id"]: row for row in predecessor["partitions"]}
    after = {row["partition_id"]: row for row in current["partitions"]}

    assert all(before[f"R2A-{n}"]["status"] == "complete" for n in range(1, 12))
    assert all(after[f"R2A-{n}"]["status"] == "complete" for n in range(1, 13))

    assert before["R2A-12"]["status"] == "planned_not_present"
    assert after["R2A-12"]["status"] == "complete"

    normalized = json.loads(json.dumps(current))
    normalized["artifact_version"] = predecessor["artifact_version"]
    normalized["status"] = predecessor["status"]

    normalized_by_id = {
        row["partition_id"]: row
        for row in normalized["partitions"]
    }
    normalized_by_id["R2A-12"]["status"] = "planned_not_present"

    assert normalized == predecessor


def test_r2a12_gate_update_is_bounded_and_does_not_authorize_r2b():
    text = CONTROL.read_text(encoding="utf-8")

    assert "## R2A — authority-surface and drift inventory\n\n**Status:** `complete`" in text
    assert "## R2B — modular doctrine resolution\n\n**Status:** `ready`" in text
    assert "## R2C — formal completion review\n\n**Status:** `blocked`" in text

    assert "`R2A=complete`; `R2B=ready`; `R2C=blocked`" in text
    assert "`R2=active_incomplete`" in text
    assert "`R3–R6=blocked`" in text
    assert "`RT-002G=unauthorized`" in text
    assert "`temporary_evidence_deletion=unauthorized`" in text

    assert "R2B remains unstarted." in text
    assert "No R2B package or module may begin until separately" in text


def test_r2a12_preserves_r2a11_package_and_module_assessment_bytes():
    path = QPM.relative_to(ROOT).as_posix()
    assert QPM.read_bytes() == git_bytes(BASE, path)

    qpm = load(QPM)

    outcomes = {
        row["package_id"]: row["assessment_outcome"]
        for row in qpm["package_assessments"]
    }

    assert outcomes == {
        "R2B-CORE": "required_pending_authorization",
        "R2B-AGENCY": "not_required",
        "R2B-WORLD": "not_required",
        "R2B-CONTINUITY": "required_pending_authorization",
        "R2B-CROSS-PHASE": "required_pending_authorization",
    }


def test_r2a11_successor_sensitive_boundary_is_historicalized():
    path = ROOT / "tests/test_afqr_r2a11_question_package_module.py"
    text = path.read_text(encoding="utf-8")

    assert (
        f'R2A11_CERTIFIED_HEAD = "{R2A11_CERTIFIED_HEAD}"'
        in text
    )
    assert (
        "git_bytes(R2A11_CERTIFIED_HEAD, MANIFEST_PATH)"
        in text
    )
    assert (
        "git_bytes(R2A11_CERTIFIED_HEAD, CONTRACT_PATH)"
        in text
    )


def test_r2a12_scope_caps_and_prohibited_runtime_schema_work():
    changed = set(
        git("diff", "--name-only", BASE).splitlines()
    )
    untracked = set(
        git("ls-files", "--others", "--exclude-standard").splitlines()
    )
    changed |= untracked

    assert changed == AUTHORIZED

    assert not any(
        path.startswith(("src/", "schemas/", "tests/runtime/"))
        for path in changed
    )

    assert not git(
        "diff",
        "--name-status",
        "--diff-filter=D",
        BASE,
    )

    additions = 0

    for row in git("diff", "--numstat", BASE).splitlines():
        if not row:
            continue
        added = row.split("\t", 1)[0]
        assert added != "-"
        additions += int(added)

    for path in untracked:
        additions += len(
            (ROOT / path).read_text(encoding="utf-8").splitlines()
        )

    assert len(changed) <= 7
    assert additions <= 2500
