"""Executable validation for AFQR R2C formal completion review."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BASE = "5cae79bcdd86c93c6fe77b6492a8a087a83900b0"
CONTINUITY_HEAD = "d94f5e8f40b1b74d6bdb23e2e419e5cb5d6fb34f"
CONTINUITY_PR = 378
R2C_AUTHORIZATION = "owner_directive_2026-09-08_r2c_activation"
R2C_VALIDATED_HEAD = "949575f42f8b4ba1e01963013b35376d49433faf"
R2C_PUBLICATION_HEAD = "ea47efef19e1552f40fee7b7658797b59bd35b7f"
R2C_PR = 379
R2C_MERGE = "843fc89f3769a8e6323fa7b683d3805a9edfc142"

REVIEW = ROOT / "docs/doctrine/reviews/afqr_r2c_formal_completion_review.md"
MANIFEST = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
CONTROL = ROOT / "docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md"
QPM = ROOT / "docs/doctrine/reviews/r2a/question_package_module/index.yaml"
R2A6_INDEX = ROOT / "docs/doctrine/reviews/r2a/dispositions_runtime_schema/index.yaml"

R2A6_SHARDS = (
    ROOT / "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0001.yaml",
    ROOT / "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0002.yaml",
)

EXPECTED_SHARD_SHA256 = {
    "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0001.yaml":
        "7ddb4d6e7e7342c44a9e6e0e574309b1e084743fd469ef4eec3944b668b0cd05",
    "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0002.yaml":
        "e4b1293559231990c0468908c74648ba34c355373857d1b824fd375a648e2569",
}

ALLOWED_R2C_PATHS = {
    "docs/doctrine/reviews/afqr_r2c_formal_completion_review.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md",
    "docs/decisions/current_decisions_log.md",
    "tests/test_afqr_r2c_formal_completion_review.py",
    "tests/test_post_r2a_transition_program.py",
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


def test_r2c_review_records_independent_pass_and_nonauthority():
    text = REVIEW.read_text(encoding="utf-8")

    required = [
        "**Review result:** `PASS`",
        "**Validation state:** `validated`",
        f"**Validated branch head:** `{R2C_VALIDATED_HEAD}`",
        f"**Inspected merged baseline:** `{BASE}`",
        "Every material R2A finding has a lawful outcome",
        "Required R2B packages match the R2A synthesis",
        "No unnecessary package was manufactured",
        "No semantic super-owner was created",
        "No implementation was smuggled into doctrine",
        "Later-phase unresolved items remain explicitly preserved",
        "Exact R3 conformance target",
        "Blocking exceptions\n\nNone.",
        "`R2=complete`",
        "`R2B=complete`",
        "`R2C=complete`",
        "not authorized to execute by this review",
    ]

    for value in required:
        assert value in text


def test_continuity_successor_merge_bookkeeping_is_exact():
    manifest = load(MANIFEST)
    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    continuity = by_id["PR2-R2B-N"]
    assert continuity["status"] == "merged"
    assert continuity["pull_request"] == CONTINUITY_PR
    assert continuity["branch_head"] == CONTINUITY_HEAD
    assert continuity["merge_commit"] == BASE
    assert continuity["residual_gaps"] == []


def test_r2c_authorization_scope_and_gate_transition_are_bounded():
    manifest = load(MANIFEST)
    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    assert manifest["r2_gate_state"] == {
        "R1": "complete",
        "R2": "complete",
        "R2-0": "complete",
        "R2A": "complete",
        "R2B": "complete",
        "R2C": "complete",
        "R3": "ready_pending_authorization",
        "R4-R6": "blocked",
        "RT-002G": "unauthorized",
        "temporary_evidence_deletion": "unauthorized",
    }

    assert manifest["r2b_package_state"] == {
        "R2B-CORE": "merged",
        "R2B-AGENCY": "not_required",
        "R2B-WORLD": "not_required",
        "R2B-CONTINUITY": "merged",
        "R2B-CROSS-PHASE": "merged",
    }

    r2c = by_id["PR2-R2C"]
    assert r2c["status"] == "merged"
    assert r2c["validation_evidence"] == [
        "focused R2C, transition-control, and predecessor validation:63 passed",
        "full repository suite:8922 passed, 10 skipped, 2 xfailed, 1 warning",
        "git diff --check:clean",
        "validated working tree:clean",
    ]
    assert r2c["authorization_reference"] == R2C_AUTHORIZATION
    assert r2c["starting_baseline"] == BASE
    assert r2c["residual_gaps"] == []
    assert r2c["pull_request"] == R2C_PR
    assert r2c["branch_head"] == R2C_PUBLICATION_HEAD
    assert r2c["merge_commit"] == R2C_MERGE
    assert set(r2c["owned_paths"]) == ALLOWED_R2C_PATHS

    prohibited = set(r2c["prohibited_scope"])
    for value in {
        "new_doctrine_invention",
        "semantic_super_owner_creation",
        "runtime_implementation",
        "production_schema_implementation",
        "persistence_or_replay_implementation",
        "source_pipeline_implementation",
        "canon_promotion",
        "myravant_identity_migration",
        "native_content_production",
        "runtime_scalability_implementation",
        "live_play_or_gm_behavior",
        "temporary_evidence_deletion",
    }:
        assert value in prohibited


def test_r3_conformance_target_is_exact_hash_anchored_and_unexecuted():
    manifest = load(MANIFEST)
    target = manifest["r3_conformance_target"]

    assert target["status"] == "ready_pending_authorization"
    assert target["source_index"] == R2A6_INDEX.relative_to(ROOT).as_posix()
    assert target["selector"] == "pressure_route == r3_conformance"
    assert target["candidate_count"] == 34
    assert target["execution_authorized"] is False
    assert set(target["excluded_pressure_routes"]) == {
        "r4_substrate",
        "later_gate",
        "none",
    }

    declared = {
        row["path"]: row["content_sha256"]
        for row in target["frozen_shards"]
    }
    assert declared == EXPECTED_SHARD_SHA256

    records = []
    for shard in R2A6_SHARDS:
        rel = shard.relative_to(ROOT).as_posix()
        raw = shard.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHARD_SHA256[rel]
        records.extend(load(shard)["candidate_file_dispositions"])

    selected = [
        row for row in records
        if row["pressure_route"] == "r3_conformance"
    ]
    assert len(selected) == 34
    assert len({row["candidate_file_id"] for row in selected}) == 34
    assert len({row["path"] for row in selected}) == 34

    index = load(R2A6_INDEX)
    assert index["counts"]["by_pressure_route"]["r3_conformance"] == 34
    assert index["blocking_unresolved_candidates"] == []


def test_known_downstream_routes_remain_outside_r2c():
    text = REVIEW.read_text(encoding="utf-8")

    for value in [
        "expected-version / stale-command pressure → `r5_retrofit`",
        "reservation identity/expiry/release/settlement representation → `r4_substrate`",
        "offline/deferred progression",
        "actor-local / transformed-time representation",
        "alternate-world, cross-reality identity composition, and time-travel rewrite law",
    ]:
        assert value in text


def test_post_r2_workstreams_remain_unstarted():
    manifest = load(MANIFEST)
    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    for workstream_id in {
        "PR2-SRC",
        "PR2-ORG",
        "PR2-CORPUS",
        "PR2-IR",
        "PR2-FICT",
        "PR2-SIMEX",
        "PR2-SCALE",
        "PR2-PART",
        "PR2-CONC",
        "PR2-FID",
        "PR2-EVENT",
        "PR2-PERSIST",
        "PR2-BP",
        "PR2-AUDIT",
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    }:
        assert by_id[workstream_id]["status"] == "blocked"
        assert by_id[workstream_id]["authorization_reference"] is None


def test_r2a_question_package_module_evidence_is_unchanged():
    rel = QPM.relative_to(ROOT).as_posix()
    assert QPM.read_bytes() == git_bytes(BASE, rel)


def test_r2c_changed_file_footprint_is_bounded():
    changed = set(
        git("diff", "--name-only", f"{BASE}...HEAD").splitlines()
    )

    assert changed
    assert changed <= ALLOWED_R2C_PATHS
    assert not any(
        path.startswith(("src/", "schemas/", "tests/runtime/"))
        for path in changed
    )
    assert not git(
        "diff",
        "--name-status",
        "--diff-filter=D",
        f"{BASE}...HEAD",
    )


def test_control_plan_records_same_r2c_result_and_nonauthority():
    text = CONTROL.read_text(encoding="utf-8")

    assert "**Overall R2 status:** `complete`" in text
    assert "## R2C — formal completion review\n\n**Status:** `complete`" in text
    assert R2C_AUTHORIZATION in text
    assert BASE in text
    assert "exactly `34` candidates" in text
    assert "This target definition does not authorize R3 execution or remediation." in text
    assert "`R3` has an exact conformance target but remains `ready_pending_authorization`" in text
    assert "`RT-002G=unauthorized`" in text
    assert "`temporary_evidence_deletion=unauthorized`" in text
