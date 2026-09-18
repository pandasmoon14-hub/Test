from __future__ import annotations

import ast
import inspect
import json
from types import SimpleNamespace

import pytest

import astra_runtime.domain.object_lever_event_commit_state_delta_path as e
import astra_runtime.domain.object_lever_replay_audit_check as f
import astra_runtime.domain.object_lever_transaction_preview_bridge as b
from astra_runtime.domain.object_lever_interaction_legality_reader import (
    create_object_lever_legality_reading,
    create_object_lever_legality_reader_result,
)


def preview():
    reading = create_object_lever_legality_reading(
        reading_id="read-rs0030",
        reader_status="legality_read_available",
        legality_decision="permitted_for_preview",
        command_family=b.OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY,
        requirement_readings=(),
        block_reasons=(),
        safe_reference_ids=(
            "scene:rs0030",
            "actor:rs0030",
            "object_lever:rs0030",
        ),
    )

    reader_result = create_object_lever_legality_reader_result(
        result_id="reader-rs0030",
        reader_status="legality_read_available",
        legality_decision="permitted_for_preview",
        legality_reading=reading,
    )

    return b.bridge_object_lever_legality_to_transaction_preview(
        reader_result,
        result_id="bridge-rs0030",
        preview_candidate_id="preview-rs0030",
    )


def ready_commit_result():
    return e.commit_object_lever_preview_to_event_and_state_delta(
        preview(),
        result_id="commit-rs0030",
    )


def test_rs0030_accepts_lawful_ready_source_pair():
    commit_result = ready_commit_result()

    assert commit_result.commit_status == "commit_ready"
    assert (
        commit_result.commit_decision
        == "awaiting_qualified_transition"
    )
    assert commit_result.committed_event_record is None
    assert commit_result.state_delta_receipt is None

    source = f.build_object_lever_replay_audit_source_ref(
        commit_result
    )

    assert source.commit_status == "commit_ready"
    assert (
        source.commit_decision
        == "awaiting_qualified_transition"
    )
    assert source.committed_event_id is None
    assert source.state_delta_receipt_id is None

    assert f.validate_object_lever_replay_audit_source_ref(
        source
    )


def test_rs0030_ready_state_is_nonverified_and_nonauditable():
    result = f.audit_object_lever_event_commit_result(
        ready_commit_result()
    )

    assert result.audit_status == "audit_insufficient_commit"
    assert result.audit_decision == "insufficient_commit"
    assert "commit_not_auditable" in result.block_reasons

    assert result.audit_snapshot is None
    assert result.replay_check_receipt is None

    assert result.audit_status != "audit_verified"
    assert (
        result.audit_decision
        != "object_lever_audit_verified"
    )

    assert f.validate_object_lever_replay_audit_result(
        result
    )


def test_rs0030_ready_state_does_not_fabricate_committed_evidence():
    result = f.audit_object_lever_event_commit_result(
        ready_commit_result()
    )

    backend = f.serialize_object_lever_replay_audit_result(
        result
    )

    assert backend["audit_snapshot"] is None
    assert backend["replay_check_receipt"] is None

    serialized = json.dumps(
        backend,
        sort_keys=True,
    )

    assert "object_lever_event_committed" not in serialized
    assert "object_lever_audit_verified" not in serialized


def test_rs0030_malformed_ready_pair_remains_rejected():
    malformed = SimpleNamespace(
        result_id="bad-rs0030",
        command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY,
        commit_status="commit_ready",
        commit_decision="unknown",
        committed_event_record=None,
        state_delta_receipt=None,
        block_reasons=(),
        safe_reference_ids=(
            "scene:rs0030",
            "actor:rs0030",
            "object_lever:rs0030",
        ),
        metadata={},
    )

    with pytest.raises(
        f.InvalidObjectLeverReplayAuditSourceRefError,
        match="commit_status and commit_decision are not coherent",
    ):
        f.build_object_lever_replay_audit_source_ref(
            malformed
        )


def test_rs0030_ready_serialization_is_deterministic():
    first = f.audit_object_lever_event_commit_result(
        ready_commit_result()
    )
    second = f.audit_object_lever_event_commit_result(
        ready_commit_result()
    )

    first_backend = f.serialize_object_lever_replay_audit_result(
        first
    )
    second_backend = f.serialize_object_lever_replay_audit_result(
        second
    )

    assert first_backend == second_backend

    assert (
        json.dumps(first_backend, sort_keys=True)
        == json.dumps(second_backend, sort_keys=True)
    )


def test_rs0030_authority_flags_remain_false_only():
    result = f.audit_object_lever_event_commit_result(
        ready_commit_result()
    )

    assert set(result.authority_flags.to_dict().values()) == {
        False
    }

    source = inspect.getsource(f)
    tree = ast.parse(source)

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, ast.Import):
            imports.extend(
                alias.name
                for alias in node.names
            )

    assert "astra_runtime.domain.event_commitment" not in imports

    forbidden_import_fragments = (
        "event_store",
        "persistence",
        "replay_store",
        "replay_index",
        "state_mutation",
        "transition_manager",
    )

    for fragment in forbidden_import_fragments:
        assert not any(
            fragment in module
            for module in imports
        )


def test_rs0030_does_not_change_rt002e_authority_boundary():
    commit_result = ready_commit_result()

    assert commit_result.commit_status == "commit_ready"
    assert (
        commit_result.commit_decision
        == "awaiting_qualified_transition"
    )
    assert commit_result.committed_event_record is None
    assert commit_result.state_delta_receipt is None

    flags = commit_result.authority_flags.to_dict()
    assert set(flags.values()) == {False}

    assert "does not own AFQR-01" in (
        e.OBJECT_LEVER_COMMIT_NON_AUTHORITY_NOTE
    )
