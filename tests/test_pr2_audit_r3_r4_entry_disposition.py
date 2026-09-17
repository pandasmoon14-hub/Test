# Executable validation for PR2-AUDIT-A R3/R4-entry disposition.
from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE = "b8c00ed48f2859eeef4a9229b3aec0ea4cd1405c"
AUTH = "owner_directive_2026-09-16_pr2_audit_a_r3_r4_entry_disposition"
EFFECT = "inventory_and_disposition_only"
AUDIT_A_ACCEPTED_MERGE = "503cd04e69225398d32d3ad4848c05522b96e83c"

AUDIT = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_audit_r3_promotion_blocker_r4_entry_disposition.yaml"
)
R3_REVIEW = (
    ROOT
    / "docs/doctrine/reviews/r3_initial_conformance_review.yaml"
)
INDEX = (
    ROOT
    / "docs/doctrine/reviews/r2a/"
    "dispositions_runtime_schema/index.yaml"
)
MAN = (
    ROOT
    / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
)

RETAIN = "retain_nonauthoritative_until_separately_authorized_promotion"
MIGRATE = "bounded_migration_required_before_authoritative_promotion"


def git_text_at(ref, path):
    rel = path.relative_to(ROOT).as_posix()

    return subprocess.check_output(
        ["git", "show", f"{ref}:{rel}"],
        cwd=ROOT,
    ).decode("utf-8")


def load(path):
    if path == MAN:
        return json.loads(
            git_text_at(AUDIT_A_ACCEPTED_MERGE, path)
        )

    return json.loads(path.read_text(encoding="utf-8"))


def blob_at(ref, path):
    return subprocess.check_output(
        ["git", "rev-parse", f"{ref}:{path}"],
        cwd=ROOT,
        text=True,
    ).strip()


def test_audit_scope_is_exact_and_nonauthoritative():
    audit = load(AUDIT)

    assert audit["status"] == "validated_complete"
    assert audit["workstream_id"] == "PR2-AUDIT"
    assert audit["tranche_id"] == "PR2-AUDIT-A"
    assert audit["authorization_reference"] == AUTH
    assert audit["authority_effect"] == EFFECT
    assert audit["starting_baseline"] == BASE

    scope = audit["scope"]

    assert scope["r3_promotion_blocker_count"] == 19
    assert scope["r4_substrate_context_count"] == 16
    assert (
        scope["r3_blocker_r4_substrate_path_overlap_count"]
        == 0
    )

    for key in (
        "repository_wide_audit_complete",
        "remediation_authorized",
        "pr2_mig_authorized",
        "pr2_test_authorized",
        "pr2_impl_authorized",
        "r4_activation_authorized",
        "runtime_implementation_authorized",
        "production_schema_implementation_authorized",
    ):
        assert scope[key] is False


def test_exact_19_r3_promotion_blockers_are_consumed():
    audit = load(AUDIT)
    r3 = load(R3_REVIEW)

    expected = {
        row["candidate_file_id"]
        for row in r3["candidate_dispositions"]
        if row["promotion_blocking"]
    }

    actual = {
        row["candidate_file_id"]
        for row in audit["audit_dispositions"]
    }

    assert len(expected) == 19
    assert actual == expected

    for row in audit["audit_dispositions"]:
        assert (
            blob_at(BASE, row["path"])
            == row["audit_baseline_blob_sha"]
        )
        assert row["current_file_edit_authorized"] is False
        assert row["promotion_blocking"] is True


def test_audit_disposition_partition_is_exact():
    audit = load(AUDIT)
    rows = audit["audit_dispositions"]

    counts = Counter(
        row["audit_disposition"]
        for row in rows
    )

    assert counts == {
        RETAIN: 17,
        MIGRATE: 2,
    }

    migrate_ids = {
        row["candidate_file_id"]
        for row in rows
        if row["migration_required_now"]
    }

    assert migrate_ids == {
        "R2A-DISPOSITION-RS-0028",
        "R2A-DISPOSITION-RS-0030",
    }

    retained = [
        row
        for row in rows
        if row["audit_disposition"] == RETAIN
    ]

    assert len(retained) == 17
    assert all(
        row["migration_required_now"] is False
        for row in retained
    )


def test_r4_context_is_exact_16_and_disjoint():
    audit = load(AUDIT)
    index = load(INDEX)

    records = []

    for shard_ref in index["shards"]:
        shard = load(ROOT / shard_ref["path"])

        records.extend(
            row
            for row in shard["candidate_file_dispositions"]
            if row["pressure_route"] == "r4_substrate"
        )

    assert len(records) == 16

    expected_ids = {
        row["candidate_file_id"]
        for row in records
    }

    context = audit["r4_substrate_context"]

    assert {
        row["candidate_file_id"]
        for row in context
    } == expected_ids

    blocker_paths = {
        row["path"]
        for row in audit["audit_dispositions"]
    }

    r4_paths = {
        row["path"]
        for row in context
    }

    assert blocker_paths.isdisjoint(r4_paths)


def test_r4_0_read_only_eligibility_does_not_activate_r4():
    audit = load(AUDIT)
    manifest = load(MAN)

    summary = audit["summary"]

    assert (
        summary[
            "r4_0_read_only_reconciliation_"
            "ready_pending_authorization"
        ]
        is True
    )

    assert summary["r4_activation_authorized"] is False
    assert (
        summary["r4_substrate_implementation_authorized"]
        is False
    )
    assert summary["runtime_promotion_clear"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    assert by_id["PR2-AUDIT"]["status"] == "active"

    for wid in (
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    ):
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None


def test_pr2_audit_is_not_falsely_terminalized():
    audit = load(AUDIT)
    manifest = load(MAN)

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    row = by_id["PR2-AUDIT"]

    assert audit["summary"]["repository_wide_pr2_audit_complete"] is False
    assert row["status"] == "active"
    assert row["current_tranche"] == "PR2-AUDIT-A"
    assert (
        row["current_tranche_state"]
        == "validated_complete"
    )
    assert row["current_tranche_next_tranche_authorized"] is False

def test_audit_a_validation_is_terminal_for_tranche_not_workstream():
    audit = load(AUDIT)
    manifest = load(MAN)

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    row = by_id["PR2-AUDIT"]

    assert manifest["artifact_version"] == "0.4.44"
    assert audit["artifact_version"] == "0.1.1"

    assert audit["status"] == "validated_complete"
    assert audit["validation_state"] == "validated"

    assert set(audit["validation_evidence"]) == {
        "PR2-AUDIT-A focused validation:31 passed",
        (
            "PR2-AUDIT-A full local repository suite:"
            "9218 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        "PR2-AUDIT-A git diff --check:clean",
        "PR2-AUDIT-A exact seven-file footprint:PASS",
        "PR2-AUDIT-A runtime/schema noninterference audit:PASS",
    }

    assert audit["summary"]["current_tranche_validated"] is True
    assert (
        audit["summary"]["repository_wide_pr2_audit_complete"]
        is False
    )

    assert row["status"] == "active"
    assert row["current_tranche"] == "PR2-AUDIT-A"
    assert row["current_tranche_state"] == "validated_complete"
    assert row["current_tranche_completion_state"] == (
        "validated_complete_with_bounded_dispositions"
    )

    assert (
        row[
            "current_tranche_r4_0_read_only_reconciliation_"
            "ready_pending_authorization"
        ]
        is True
    )

    assert row["current_tranche_r4_activation_authorized"] is False
    assert row["current_tranche_remediation_authorized"] is False
    assert row["current_tranche_next_tranche_authorized"] is False

    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

    for wid in (
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    ):
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None
