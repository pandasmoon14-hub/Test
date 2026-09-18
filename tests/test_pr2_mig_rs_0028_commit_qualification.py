from __future__ import annotations

import ast
import inspect

import pytest

import astra_runtime.domain.object_lever_event_commit_state_delta_path as e
import astra_runtime.domain.object_lever_replay_audit_check as f
import astra_runtime.domain.object_lever_transaction_preview_bridge as b
from astra_runtime.domain.object_lever_interaction_legality_reader import (
    create_object_lever_legality_reading,
    create_object_lever_legality_reader_result,
)


def preview():
    reading=create_object_lever_legality_reading(
        reading_id="read-1",
        reader_status="legality_read_available",
        legality_decision="permitted_for_preview",
        command_family=(
            b.OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY
        ),
        requirement_readings=(),
        block_reasons=(),
        safe_reference_ids=(
            "scene:1",
            "actor:1",
            "object_lever:1",
        ),
    )

    result=create_object_lever_legality_reader_result(
        result_id="res-1",
        reader_status="legality_read_available",
        legality_decision="permitted_for_preview",
        legality_reading=reading,
    )

    return (
        b.bridge_object_lever_legality_to_transaction_preview(
            result,
            result_id="bridge-1",
            preview_candidate_id="pc-1",
        )
    )


def test_rs0028_preview_ready_is_not_commitment():
    result=(
        e.commit_object_lever_preview_to_event_and_state_delta(
            preview()
        )
    )

    assert result.commit_status == "commit_ready"

    assert (
        result.commit_decision
        == "awaiting_qualified_transition"
    )

    assert result.committed_event_record is None
    assert result.state_delta_receipt is None
    assert result.block_reasons == ()

    assert e.validate_object_lever_event_commit_result(
        result
    )


def test_ready_result_cannot_claim_committed_decision():
    with pytest.raises(
        e.InvalidObjectLeverEventCommitResultError
    ):
        e.ObjectLeverEventCommitResult(
            result_id="commit:1",
            commit_status="commit_ready",
            commit_decision="object_lever_event_committed",
        )



def test_rs0030_remains_separately_gated_for_commit_ready_result():
    commit_result=(
        e.commit_object_lever_preview_to_event_and_state_delta(
            preview()
        )
    )

    assert commit_result.commit_status == "commit_ready"

    assert (
        commit_result.commit_decision
        == "awaiting_qualified_transition"
    )

    assert commit_result.committed_event_record is None
    assert commit_result.state_delta_receipt is None

    # RS-0030 remains the next separately gated migration.
    # Its historical private commit-status map does not yet
    # understand the newly lawful RT-002E proposal state.
    #
    # PR2-MIG-A must not edit RS-0030 merely to conceal that
    # remaining dependency.
    with pytest.raises(
        f.InvalidObjectLeverReplayAuditSourceRefError,
        match="commit_status and commit_decision are not coherent",
    ):
        f.audit_object_lever_event_commit_result(
            commit_result
        )


def test_rs0028_does_not_implement_afqr01_commit_owner():
    source=inspect.getsource(e)
    tree=ast.parse(source)

    imports=[]

    for node in ast.walk(tree):
        if isinstance(node,ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node,ast.Import):
            imports.extend(
                alias.name
                for alias in node.names
            )

    assert (
        "astra_runtime.domain.event_commitment"
        not in imports
    )

    assert (
        "astra_runtime.kernel.event_ledger"
        not in imports
    )

    assert (
        "astra_runtime.kernel.persistence_boundary"
        not in imports
    )

    assert "TransitionCommitReceipt(" not in source
    assert "event_store_append(" not in source
    assert "apply_state_delta(" not in source


def test_negative_preview_dispositions_remain_representable():
    bad=b.ObjectLeverTransactionPreviewBridgeResult(
        result_id="bridge-bad",
        bridge_status="preview_bridge_available",
        bridge_decision="preview_candidate_prepared",
        preview_candidate=None,
    )

    result=(
        e.commit_object_lever_preview_to_event_and_state_delta(
            bad
        )
    )

    assert result.commit_status == "commit_blocked"
    assert result.commit_decision == "blocked"

    assert "missing_preview_candidate" in (
        result.block_reasons
    )

    assert result.committed_event_record is not None
    assert result.state_delta_receipt is not None


def test_historical_guard_updates_are_snapshot_only():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]

    manifest = json.loads(
        (
            root
            / "docs/doctrine/control/"
            "post_r2a_transition_manifest.yaml"
        ).read_text(encoding="utf-8")
    )

    mig = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }["PR2-MIG"]

    scope = mig["current_tranche_scope"]

    assert scope["historical_guard_test_file_count"] == 10

    assert (
        scope["historical_guard_test_updates_authorized"]
        is True
    )

    assert (
        scope["historical_guard_test_update_kind"]
        == "accepted_merge_snapshot_only"
    )

    assert (
        scope[
            "historical_guard_runtime_allowlist_expansion_authorized"
        ]
        is False
    )

    expected = {
        "tests/test_afqr_r1b_shared_vocabulary_and_type_owners.py",
        (
            "tests/test_runtime_domain_pr_5g_"
            "resource_consequence_math_residual_"
            "planning_hardening_review.py"
        ),
        (
            "tests/test_runtime_domain_rt_001g_"
            "state_owner_interface_prerequisite_review.py"
        ),
        "tests/test_afqr_r1c_cross_invariants_and_dependencies.py",
        "tests/test_afqr_r1d_core_transaction_identity_relation.py",
        (
            "tests/test_afqr_r1d_agency_"
            "epistemic_social_communication.py"
        ),
        "tests/test_afqr_r1d_world_action_sensing.py",
        (
            "tests/test_runtime_domain_rt_001d_"
            "action_legality_integration_hardening_review.py"
        ),
        (
            "tests/test_runtime_domain_rt_001i_"
            "state_owner_interface_contract_hardening_review.py"
        ),
        (
            "tests/test_runtime_domain_rt_002a_"
            "read_only_vertical_slice_state_owner_facade.py"
        ),
    }

    assert expected <= set(mig["owned_paths"])



def test_ci_historical_guard_correction_scope():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    manifest = json.loads(
        (
            root
            / "docs/doctrine/control/"
            "post_r2a_transition_manifest.yaml"
        ).read_text(encoding="utf-8")
    )
    mig = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }["PR2-MIG"]

    scope = mig["current_tranche_scope"]
    correction = mig["current_tranche_ci_guard_correction"]

    assert scope["historical_guard_test_file_count"] == 10
    assert scope["ci_historical_guard_test_file_count"] == 7
    assert scope["ci_historical_guard_repair_authorized"] is True
    assert (
        scope["ci_historical_guard_repair_kind"]
        == "accepted_merge_snapshot_only"
    )
    assert (
        scope[
            "ci_historical_guard_repair_runtime_allowlist_expansion_authorized"
        ]
        is False
    )

    assert correction["source_workflow_run"] == 233
    assert correction["source_workflow_run_id"] == 35394370006
    assert correction["root_stale_historical_guard_failures"] == 7
    assert correction["cascading_failures"] == 3
    assert correction["accepted_merge_snapshot_only"] is True
    assert correction["runtime_implementation_files_added_by_correction"] == 0
    assert correction["legacy_runtime_allowlist_expanded"] is False
    assert correction["resulting_pr_changed_path_count"] == 18
    assert correction["replacement_ci_required_before_merge"] is True

def test_rs0028_terminal_validation_evidence():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]

    manifest = json.loads(
        (
            root
            / "docs/doctrine/control/"
            "post_r2a_transition_manifest.yaml"
        ).read_text(encoding="utf-8")
    )

    mig = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }["PR2-MIG"]

    assert (
        mig["current_tranche_state"]
        == "validated_complete_pending_merge"
    )

    assert (
        mig["current_tranche_completion_state"]
        == "validated_complete_pending_merge"
    )

    assert mig["current_tranche_validation_state"] == "validated"
    assert mig["current_tranche_candidate_validated"] is True

    evidence = mig["current_tranche_validation_evidence"]

    full = next(
        item
        for item in evidence
        if item["evidence_type"] == "full_repository_suite"
    )

    assert full["result"] == "pass"
    assert full["passed"] == 9251
    assert full["skipped"] == 10
    assert full["xfailed"] == 2
    assert full["warnings"] == 1

    assert mig["remaining_candidate_ids"] == [
        "R2A-DISPOSITION-RS-0030"
    ]

    assert mig["next_candidate_authorized"] is False
    assert mig["next_tranche_authorized"] is False
    assert (
        mig["current_tranche_runtime_promotion_authorized"]
        is False
    )
