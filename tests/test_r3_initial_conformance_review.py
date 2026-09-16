# Executable validation for Myravant R3 initial conformance review.
from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE = "a92e47bb2e0d5ffd853da2c1bbf6425efc8c659c"
AUTH = "owner_directive_2026-09-16_r3_initial_conformance"
EFFECT = "r3_conformance_review_only"

REVIEW = ROOT / "docs/doctrine/reviews/r3_initial_conformance_review.yaml"
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
INDEX = ROOT / "docs/doctrine/reviews/r2a/dispositions_runtime_schema/index.yaml"

OUTCOME_CLEAR = "conformant_as_nonauthoritative_surface"
OUTCOME_QUALIFY = "conformant_with_required_remediation_before_promotion"
OUTCOME_FAIL = "nonconformant_requires_remediation"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path):
    return subprocess.check_output(
        ["git", "hash-object", path],
        cwd=ROOT,
        text=True,
    ).strip()


def frozen_target():
    manifest = load(MAN)
    target = manifest["r3_conformance_target"]
    index = load(INDEX)

    records = []

    for shard_ref in target["frozen_shards"]:
        path = ROOT / shard_ref["path"]
        raw = path.read_bytes()

        assert hashlib.sha256(raw).hexdigest() == (
            shard_ref["content_sha256"]
        )

        shard = json.loads(raw.decode("utf-8"))

        for row in shard["candidate_file_dispositions"]:
            if row["pressure_route"] == "r3_conformance":
                records.append(row)

    assert index["counts"]["by_pressure_route"]["r3_conformance"] == 34
    return records


def test_review_metadata_and_scope_are_exact():
    review = load(REVIEW)

    assert review["artifact_id"] == (
        "MYRAVANT-R3-INITIAL-CONFORMANCE-REVIEW-001"
    )
    assert review["status"] == "validated_complete"
    assert review["review_result"] == (
        "complete_with_nonconformances_routed"
    )
    assert review["authorization_reference"] == AUTH
    assert review["authority_effect"] == EFFECT
    assert review["starting_baseline"] == BASE

    scope = review["scope"]

    assert scope["candidate_count"] == 34
    assert scope["selector"] == "pressure_route == r3_conformance"
    assert set(scope["excluded_pressure_routes"]) == {
        "r4_substrate",
        "later_gate",
        "none",
    }

    for key in (
        "runtime_implementation_authorized",
        "production_schema_implementation_authorized",
        "r4_activation_authorized",
        "pr2_test_authorized",
        "pr2_audit_authorized",
        "pr2_mig_authorized",
        "pr2_impl_authorized",
    ):
        assert scope[key] is False


def test_review_has_exact_frozen_34_record_population():
    review = load(REVIEW)
    frozen = frozen_target()

    frozen_ids = {
        row["candidate_file_id"]
        for row in frozen
    }

    review_ids = {
        row["candidate_file_id"]
        for row in review["candidate_dispositions"]
    }

    assert len(frozen_ids) == 34
    assert review_ids == frozen_ids

    assert all(
        row["pressure_route"] == "r3_conformance"
        for row in review["candidate_dispositions"]
    )


def test_all_34_current_files_still_match_frozen_r2a_blobs():
    review = load(REVIEW)

    for row in review["candidate_dispositions"]:
        path = ROOT / row["path"]

        assert path.is_file()
        assert row["r3_blob_state"] == "unchanged_since_r2a"
        assert row["frozen_r2a_blob_sha"] == row["r3_baseline_blob_sha"]
        assert git_blob(row["path"]) == row["frozen_r2a_blob_sha"]


def test_outcome_partition_is_complete_and_exact():
    review = load(REVIEW)
    rows = review["candidate_dispositions"]

    counts = Counter(row["outcome"] for row in rows)

    assert counts == {
        OUTCOME_CLEAR: 15,
        OUTCOME_QUALIFY: 17,
        OUTCOME_FAIL: 2,
    }

    assert review["summary"]["outcome_counts"] == dict(
        sorted(counts.items())
    )

    direct = [
        row["candidate_file_id"]
        for row in rows
        if row["outcome"] == OUTCOME_FAIL
    ]

    assert direct == [
        "R2A-DISPOSITION-RS-0028",
        "R2A-DISPOSITION-RS-0030",
    ]

    assert review["summary"]["direct_nonconformance_ids"] == direct
    assert review["summary"]["promotion_blocking_candidate_count"] == 19
    assert review["summary"]["runtime_promotion_clear"] is False


def test_rs0028_records_unqualified_commitment_defect():
    review = load(REVIEW)

    row = next(
        row
        for row in review["candidate_dispositions"]
        if row["candidate_file_id"] == "R2A-DISPOSITION-RS-0028"
    )

    assert row["outcome"] == OUTCOME_FAIL
    assert row["finding_code"] == (
        "unauthorized_preview_to_commit_transition"
    )

    source = (
        ROOT / row["path"]
    ).read_text(encoding="utf-8")

    assert (
        "commit_object_lever_preview_to_event_and_state_delta"
        in source
    )
    assert "object_lever_event_committed" in source
    assert "ObjectLeverCommittedEventRecord" in source
    assert "ObjectLeverStateDeltaReceipt" in source

    assert row["downstream_route"] == [
        "PR2-AUDIT",
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    ]


def test_rs0030_is_downstream_of_the_unqualified_commitment():
    review = load(REVIEW)

    row = next(
        row
        for row in review["candidate_dispositions"]
        if row["candidate_file_id"] == "R2A-DISPOSITION-RS-0030"
    )

    assert row["outcome"] == OUTCOME_FAIL
    assert row["finding_code"] == (
        "audit_depends_on_unqualified_commitment"
    )

    source = (
        ROOT / row["path"]
    ).read_text(encoding="utf-8")

    assert "ObjectLeverEventCommitResult" in source
    assert "already-committed RT-002E" in source
    assert "object_lever_audit_verified" in source


def test_fixed_command_vocabularies_are_not_cleared_for_promotion():
    review = load(REVIEW)

    by_id = {
        row["candidate_file_id"]: row
        for row in review["candidate_dispositions"]
    }

    for candidate_id in (
        "R2A-DISPOSITION-RS-0022",
        "R2A-DISPOSITION-RS-0023",
        "R2A-DISPOSITION-RS-0039",
    ):
        assert by_id[candidate_id]["outcome"] == OUTCOME_QUALIFY
        assert by_id[candidate_id]["promotion_blocking"] is True


def test_legacy_astra_runtime_identity_is_not_misclassified_as_failure():
    review = load(REVIEW)

    row = next(
        row
        for row in review["candidate_dispositions"]
        if row["candidate_file_id"] == "R2A-DISPOSITION-RS-0050"
    )

    assert row["outcome"] == OUTCOME_CLEAR
    assert row["finding_code"] == (
        "record_identifier_compatibility_surface"
    )

    identity_contract = (
        ROOT
        / "docs/doctrine/control/myravant_identity_migration_contract.md"
    ).read_text(encoding="utf-8")

    assert "astra_runtime" in identity_contract


def test_r3_does_not_authorize_downstream_work():
    manifest = load(MAN)
    review = load(REVIEW)

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    assert manifest["r2_gate_state"]["R3"] == "complete"
    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

    for wid in (
        "PR2-AUDIT",
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    ):
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None

    assert review["summary"]["r4_activation_authorized"] is False
    assert review["summary"]["downstream_remediation_authorized"] is False
    assert review["validation_state"] == "validated"
    assert set(review["validation_evidence"]) == {
    "R3 focused conformance validation:39 passed",
    (
        "R3 full local repository suite:"
        "9211 passed, 10 skipped, 2 xfailed, 1 warning"
    ),
    "R3 git diff --check:clean",
    "R3 exact eight-file review footprint:PASS",
    "R3 runtime/schema noninterference audit:PASS",
}

def test_r3_terminal_validation_state_preserves_promotion_block():
    manifest = load(MAN)
    review = load(REVIEW)
    target = manifest["r3_conformance_target"]

    assert manifest["artifact_version"] == "0.4.42"
    assert review["artifact_version"] == "0.1.1"

    assert manifest["r2_gate_state"]["R3"] == "complete"
    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"

    assert target["status"] == "validated"
    assert target["review_state"] == "validated_complete"
    assert target["completion_state"] == (
        "validated_complete_with_nonconformances_routed"
    )

    assert review["status"] == "validated_complete"
    assert review["validation_state"] == "validated"

    assert target["runtime_promotion_clear"] is False
    assert target["r4_activation_authorized"] is False
    assert target["downstream_remediation_authorized"] is False

    assert review["summary"]["r3_gate_complete"] is True
    assert review["summary"]["runtime_promotion_clear"] is False
