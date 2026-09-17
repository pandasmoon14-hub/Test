# Executable validation for Myravant R4-0 substrate reconciliation.
from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE = "503cd04e69225398d32d3ad4848c05522b96e83c"
AUTH = "owner_directive_2026-09-16_r4_0_read_only_substrate_reconciliation"
EFFECT = "read_only_substrate_reconciliation_only"
R4_0_ACCEPTED_MERGE = "fa4f1d795275eaaad4ee525aea7e3f3c2c2bd5e9"

REVIEW = (
    ROOT
    / "docs/doctrine/reviews/"
    "r4_0_substrate_reconciliation.yaml"
)
AUDIT_A = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_audit_r3_promotion_blocker_r4_entry_disposition.yaml"
)
MAN = (
    ROOT
    / "docs/doctrine/control/"
    "post_r2a_transition_manifest.yaml"
)
FIREWALL = (
    ROOT
    / "docs/doctrine/control/"
    "conversion_runtime_origin_firewall_doctrine.md"
)

LEGACY = "legacy_conversion_handoff_not_runtime_substrate"
OFFLINE = "retain_offline_extraction_tooling_not_runtime_substrate"


def git_text_at(ref, path):
    rel = path.relative_to(ROOT).as_posix()

    return subprocess.check_output(
        ["git", "show", f"{ref}:{rel}"],
        cwd=ROOT,
    ).decode("utf-8")


def load(path):
    if path == MAN:
        return json.loads(
            git_text_at(R4_0_ACCEPTED_MERGE, path)
        )

    return json.loads(path.read_text(encoding="utf-8"))


def blob(path):
    return subprocess.check_output(
        ["git", "hash-object", path],
        cwd=ROOT,
        text=True,
    ).strip()


def test_r4_0_scope_is_exact_and_read_only():
    review = load(REVIEW)

    assert review["status"] == "validated_complete"
    assert review["tranche_id"] == "R4-0"
    assert review["tracking_tranche"] == "PR2-AUDIT-B"
    assert review["authorization_reference"] == AUTH
    assert review["authority_effect"] == EFFECT
    assert review["starting_baseline"] == BASE

    scope = review["scope"]

    assert scope["candidate_count"] == 16
    assert scope["schema_edit_count"] == 0
    assert scope["runtime_edit_count"] == 0

    for key in (
        "remediation_authorized",
        "r4_activation_authorized",
        "r4_implementation_authorized",
        "pr2_mig_authorized",
        "pr2_test_authorized",
        "pr2_impl_authorized",
    ):
        assert scope[key] is False


def test_exact_16_audit_a_r4_records_are_reconciled():
    review = load(REVIEW)
    audit_a = load(AUDIT_A)

    expected = {
        row["candidate_file_id"]: row
        for row in audit_a["r4_substrate_context"]
    }

    actual = {
        row["candidate_file_id"]: row
        for row in review["candidate_dispositions"]
    }

    assert len(expected) == 16
    assert set(actual) == set(expected)

    for candidate_id, row in actual.items():
        predecessor = expected[candidate_id]

        assert row["path"] == predecessor["path"]
        assert row["r4_0_blob_sha"] == predecessor["audit_baseline_blob_sha"]
        assert blob(row["path"]) == row["r4_0_blob_sha"]
        assert row["blob_state"] == "unchanged_since_r2a"
        assert row["current_file_edit_authorized"] is False
        assert row["direct_runtime_promotion_allowed"] is False


def test_disposition_partition_is_10_legacy_and_6_offline():
    review = load(REVIEW)

    counts = Counter(
        row["r4_0_disposition"]
        for row in review["candidate_dispositions"]
    )

    assert counts == {
        LEGACY: 10,
        OFFLINE: 6,
    }

    assert review["summary"]["legacy_conversion_handoff_count"] == 10
    assert review["summary"]["offline_extraction_tooling_count"] == 6
    assert (
        review["summary"]["direct_runtime_substrate_candidate_count"]
        == 0
    )


def test_legacy_handoff_is_not_cosmetically_promotable():
    review = load(REVIEW)

    legacy = [
        row
        for row in review["candidate_dispositions"]
        if row["r4_0_disposition"] == LEGACY
    ]

    assert len(legacy) == 10

    assert all(
        row[
            "myravant_native_replacement_required_if_function_needed"
        ]
        is True
        for row in legacy
    )

    handoff = review["r4_design_handoff"]

    assert handoff["direct_legacy_schema_promotion_allowed"] is False
    assert (
        handoff["renaming_as_substitute_for_native_design_allowed"]
        is False
    )
    assert handoff["next_package"] == "R4-A"
    assert handoff["next_package_authorized"] is False


def test_offline_extraction_tooling_stays_outside_runtime():
    review = load(REVIEW)

    offline = [
        row
        for row in review["candidate_dispositions"]
        if row["r4_0_disposition"] == OFFLINE
    ]

    assert len(offline) == 6

    assert all(
        row["current_role_family"] == "offline_extraction_tooling"
        for row in offline
    )

    firewall = FIREWALL.read_text(encoding="utf-8")

    assert (
        "Extraction and conversion end before runtime begins."
        in firewall
    )
    assert "Runtime-origin blindness" in firewall


def test_r4_0_does_not_activate_r4_or_remediation():
    review = load(REVIEW)
    manifest = load(MAN)

    target = manifest["r4_substrate_reconciliation_target"]

    assert manifest["artifact_version"] == "0.4.46"
    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

    assert target["status"] == "validated"
    assert target["candidate_count"] == 16
    assert target["direct_runtime_substrate_candidate_count"] == 0
    assert target["schema_edits_authorized"] is False
    assert target["runtime_edits_authorized"] is False
    assert target["r4_activation_authorized"] is False
    assert target["r4_implementation_authorized"] is False
    assert target["r4_a_ready_pending_authorization"] is True

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    assert by_id["PR2-AUDIT"]["status"] == "active"
    assert by_id["PR2-AUDIT"]["current_tranche"] == "PR2-AUDIT-B"

    for wid in (
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    ):
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None


def test_r4_0_is_not_repository_wide_audit_completion():
    review = load(REVIEW)

    assert (
        review["summary"]["repository_wide_pr2_audit_complete"]
        is False
    )
    assert review["artifact_version"] == "0.1.1"
    assert review["status"] == "validated_complete"
    assert review["validation_state"] == "validated"
    assert review["summary"]["current_tranche_validated"] is True

    assert set(review["validation_evidence"]) == {
        "R4-0 focused pre-certification:29 passed",
        (
            "R4-0 full local repository suite:"
            "9226 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        "R4-0 focused post-suite regression:29 passed",
        "R4-0 git diff --check:clean",
        "R4-0 exact seven-file footprint:PASS",
        "R4-0 runtime/schema noninterference audit:PASS",
    }
