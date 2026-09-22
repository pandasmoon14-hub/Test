"""Executable R4-E persistent-world object custody-transfer tests."""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
    create_located_at_relation,
    create_persistent_world_entity,
    create_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    CHECKPOINT_FORMAT_IDENTITY,
    OBJECT_CUSTODY_CHECKPOINT_FORMAT_IDENTITY,
    OBJECT_CUSTODY_CHECKPOINT_FORMAT_VERSION,
    PersistentWorldCheckpointEvidenceError,
    PersistentWorldCheckpointFormatError,
    canonical_serialize_persistent_world_object_custody_checkpoint_payload,
    restore_persistent_world_checkpoint,
    restore_persistent_world_object_custody_checkpoint,
    write_persistent_world_checkpoint,
    write_persistent_world_object_custody_checkpoint,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    create_movement_opportunity_evidence,
    create_movement_spatial_evidence,
    create_persistent_world_movement_runtime_state,
    digest_persistent_world_entity_location_representation,
    execute_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyEvidenceError,
    PersistentWorldObjectCustodyPlacementError,
    PersistentWorldObjectCustodyRetryConflictError,
    create_custody_opportunity_evidence,
    create_custody_qualification_evidence,
    create_persistent_world_object_custody_runtime_state,
    execute_persistent_world_object_custody,
    replay_persistent_world_object_custody,
    replace_persistent_world_object_custody_movement_state,
)
from astra_runtime.kernel.command_envelope import create_command_envelope

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/astra_runtime/domain/persistent_world_object_custody_transfer.py"

CAMPAIGN = "astra:campaign:r4e-test"
ACTOR = "astra:entity:r4e-actor"
OBJECT = "astra:entity:r4e-object"
P1 = "astra:entity:r4e-p1"
P2 = "astra:entity:r4e-p2"


def _entity(local: str, classification: str):
    return create_persistent_world_entity(
        entity_id=f"astra:entity:{local}",
        classification=classification,
    )


def _initial_state(*, object_place=P1):
    representation = create_persistent_world_entity_location_representation(
        campaign_id=CAMPAIGN,
        entities=(
            _entity("r4e-actor", "character_or_creature"),
            _entity("r4e-object", "object"),
            _entity("r4e-p1", "place"),
            _entity("r4e-p2", "place"),
        ),
        relations=(
            create_located_at_relation(
                relation_id="astra:relation:r4e-actor-at-p1",
                subject_entity_id=ACTOR,
                object_entity_id=P1,
            ),
            create_located_at_relation(
                relation_id="astra:relation:r4e-object-at-start",
                subject_entity_id=OBJECT,
                object_entity_id=object_place,
            ),
        ),
    )
    return create_persistent_world_object_custody_runtime_state(
        movement_state=create_persistent_world_movement_runtime_state(
            representation=representation
        )
    )


def _digest(state):
    return digest_persistent_world_entity_location_representation(
        state.movement_state.representation
    )


def _command(operation: str, command_id: str):
    return create_command_envelope(
        command_id=command_id,
        command_type=f"{operation}_object",
        source_actor_id=ACTOR,
        payload={"object_entity_id": OBJECT},
    )


def _qualification(operation: str, tag: str, *, qualified=True):
    return create_custody_qualification_evidence(
        evidence_id=f"astra:evidence:r4e-{tag}-rt010",
        actor_entity_id=ACTOR,
        object_entity_id=OBJECT,
        operation=operation,
        qualified=qualified,
    )


def _opportunity(operation: str, tag: str, *, accepted=True):
    return create_custody_opportunity_evidence(
        evidence_id=f"astra:evidence:r4e-{tag}-afqr19",
        actor_entity_id=ACTOR,
        object_entity_id=OBJECT,
        operation=operation,
        opportunity_available=True,
        resolution_accepted=accepted,
    )


def _execute(state, operation: str, command_id: str, tag: str):
    return execute_persistent_world_object_custody(
        state=state,
        command=_command(operation, command_id),
        qualification_evidence=_qualification(operation, tag),
        opportunity_evidence=_opportunity(operation, tag),
        expected_pre_state_digest=_digest(state),
    )


def _relations(state, relation_type, subject):
    return [
        r for r in state.movement_state.representation.relations
        if r.relation_type == relation_type and r.subject_entity_id == subject
    ]


def _move_to_p2(state):
    moved = execute_persistent_world_movement(
        state=state.movement_state,
        command=create_command_envelope(
            command_id="r4e-move-p1-p2",
            command_type="move",
            source_actor_id=ACTOR,
            payload={"destination_entity_id": P2},
        ),
        spatial_evidence=create_movement_spatial_evidence(
            evidence_id="astra:evidence:r4e-move-spatial",
            actor_entity_id=ACTOR,
            source_place_id=P1,
            destination_place_id=P2,
            spatially_permitted=True,
        ),
        opportunity_evidence=create_movement_opportunity_evidence(
            evidence_id="astra:evidence:r4e-move-opportunity",
            actor_entity_id=ACTOR,
            destination_place_id=P2,
            opportunity_available=True,
            resolution_accepted=True,
        ),
        expected_pre_state_digest=_digest(state),
    )
    return replace_persistent_world_object_custody_movement_state(
        state=state,
        movement_state=moved.state,
    )


def _checkpoint_qualification(tag: str):
    return {
        "qualification_id": f"astra:evidence:r4e-checkpoint-{tag}",
        "semantic_owner": "AFQR-01",
        "qualified": True,
        "provenance": "r4-e-test",
    }


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _recompute_integrity(envelope):
    envelope["integrity_digest"] = hashlib.sha256(
        _canonical(envelope["authoritative_payload"]).encode("utf-8")
    ).hexdigest()


def test_pickup_commits_carried_by_and_removes_direct_location():
    result = _execute(_initial_state(), "pickup", "r4e-pickup-1", "pickup")
    assert result.technical_retry is False
    assert _relations(result.state, LOCATED_AT_RELATION_TYPE, OBJECT) == []
    carried = _relations(result.state, CARRIED_BY_RELATION_TYPE, OBJECT)
    assert len(carried) == 1
    assert carried[0].object_entity_id == ACTOR
    assert result.state_delta.metadata["custody_semantic_owner"] == "RT-010"


def test_pickup_requires_colocation():
    with pytest.raises(PersistentWorldObjectCustodyPlacementError):
        _execute(
            _initial_state(object_place=P2),
            "pickup",
            "r4e-pickup-not-colocated",
            "not-colocated",
        )


def test_owner_evidence_fails_closed():
    state = _initial_state()
    command = _command("pickup", "r4e-pickup-evidence")
    with pytest.raises(PersistentWorldObjectCustodyEvidenceError):
        execute_persistent_world_object_custody(
            state=state,
            command=command,
            qualification_evidence=_qualification("pickup", "reject", qualified=False),
            opportunity_evidence=_opportunity("pickup", "reject"),
            expected_pre_state_digest=_digest(state),
        )
    with pytest.raises(PersistentWorldObjectCustodyEvidenceError):
        execute_persistent_world_object_custody(
            state=state,
            command=command,
            qualification_evidence=_qualification("pickup", "accept"),
            opportunity_evidence=_opportunity("pickup", "reject2", accepted=False),
            expected_pre_state_digest=_digest(state),
        )


def test_identical_retry_is_idempotent_and_changed_meaning_conflicts():
    first = _execute(
        _initial_state(), "pickup", "r4e-pickup-retry", "retry"
    )
    retry = execute_persistent_world_object_custody(
        state=first.state,
        command=_command("pickup", "r4e-pickup-retry"),
        qualification_evidence=_qualification("pickup", "retry"),
        opportunity_evidence=_opportunity("pickup", "retry"),
        expected_pre_state_digest=_digest(first.state),
    )
    assert retry.technical_retry is True
    assert retry.receipt == first.receipt
    changed = create_command_envelope(
        command_id="r4e-pickup-retry",
        command_type="pickup_object",
        source_actor_id=ACTOR,
        payload={"object_entity_id": OBJECT, "changed": True},
    )
    with pytest.raises(PersistentWorldObjectCustodyRetryConflictError):
        execute_persistent_world_object_custody(
            state=first.state,
            command=changed,
            qualification_evidence=_qualification("pickup", "retry"),
            opportunity_evidence=_opportunity("pickup", "retry"),
            expected_pre_state_digest=_digest(first.state),
        )


def test_r4c_movement_preserves_carried_by():
    pickup = _execute(
        _initial_state(), "pickup", "r4e-pickup-before-move", "before-move"
    )
    moved = _move_to_p2(pickup.state)
    assert _relations(moved, LOCATED_AT_RELATION_TYPE, ACTOR)[0].object_entity_id == P2
    assert _relations(moved, CARRIED_BY_RELATION_TYPE, OBJECT)[0].object_entity_id == ACTOR


def test_drop_uses_carrier_current_place():
    pickup = _execute(
        _initial_state(), "pickup", "r4e-pickup-before-drop", "before-drop"
    )
    moved = _move_to_p2(pickup.state)
    dropped = _execute(moved, "drop", "r4e-drop-after-move", "drop")
    assert _relations(dropped.state, CARRIED_BY_RELATION_TYPE, OBJECT) == []
    assert _relations(dropped.state, LOCATED_AT_RELATION_TYPE, OBJECT)[0].object_entity_id == P2
    assert dropped.receipt.place_id == P2


def test_drop_requires_carried_by_source_actor():
    with pytest.raises(PersistentWorldObjectCustodyPlacementError):
        _execute(_initial_state(), "drop", "r4e-drop-not-carried", "drop-not-carried")


def test_replay_uses_committed_receipt():
    initial = _initial_state()
    pickup = _execute(initial, "pickup", "r4e-pickup-replay", "replay")
    replayed = replay_persistent_world_object_custody(
        pre_state_representation=initial.movement_state.representation,
        receipt=pickup.receipt,
    )
    assert (
        digest_persistent_world_entity_location_representation(replayed)
        == pickup.receipt.post_state_digest
    )


def test_checkpoint_round_trip_preserves_carried_state_and_evidence(tmp_path):
    pickup = _execute(
        _initial_state(), "pickup", "r4e-pickup-checkpoint", "checkpoint"
    )
    moved = _move_to_p2(pickup.state)
    path = tmp_path / "r4e.json"
    write_persistent_world_object_custody_checkpoint(
        state=moved,
        checkpoint_path=path,
        qualification_evidence=_checkpoint_qualification("carried"),
    )
    expected = _digest(moved)
    del pickup, moved
    restored = restore_persistent_world_object_custody_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )
    assert _digest(restored) == expected
    assert len(restored.movement_state.committed_transitions) == 1
    assert len(restored.committed_custody_transitions) == 1
    assert _relations(restored, CARRIED_BY_RELATION_TYPE, OBJECT)[0].object_entity_id == ACTOR


def test_restored_pickup_retry_remains_idempotent(tmp_path):
    pickup = _execute(
        _initial_state(), "pickup", "r4e-pickup-restored-retry", "restored-retry"
    )
    moved = _move_to_p2(pickup.state)
    path = tmp_path / "retry.json"
    write_persistent_world_object_custody_checkpoint(
        state=moved,
        checkpoint_path=path,
        qualification_evidence=_checkpoint_qualification("retry"),
    )
    restored = restore_persistent_world_object_custody_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )
    retry = execute_persistent_world_object_custody(
        state=restored,
        command=_command("pickup", "r4e-pickup-restored-retry"),
        qualification_evidence=_qualification("pickup", "restored-retry"),
        opportunity_evidence=_opportunity("pickup", "restored-retry"),
        expected_pre_state_digest=_digest(restored),
    )
    assert retry.technical_retry is True
    assert retry.state == restored


def test_full_pickup_move_restore_drop_checkpoint_restore_sequence(tmp_path):
    pickup = _execute(
        _initial_state(), "pickup", "r4e-sequence-pickup", "sequence-pickup"
    )
    moved = _move_to_p2(pickup.state)
    first = tmp_path / "carried.json"
    write_persistent_world_object_custody_checkpoint(
        state=moved,
        checkpoint_path=first,
        qualification_evidence=_checkpoint_qualification("first"),
    )
    del pickup, moved
    restored = restore_persistent_world_object_custody_checkpoint(
        checkpoint_path=first,
        expected_campaign_id=CAMPAIGN,
    )
    dropped = _execute(restored, "drop", "r4e-sequence-drop", "sequence-drop")
    second = tmp_path / "dropped.json"
    write_persistent_world_object_custody_checkpoint(
        state=dropped.state,
        checkpoint_path=second,
        qualification_evidence=_checkpoint_qualification("second"),
    )
    del restored, dropped
    final = restore_persistent_world_object_custody_checkpoint(
        checkpoint_path=second,
        expected_campaign_id=CAMPAIGN,
    )
    assert _relations(final, LOCATED_AT_RELATION_TYPE, ACTOR)[0].object_entity_id == P2
    assert _relations(final, LOCATED_AT_RELATION_TYPE, OBJECT)[0].object_entity_id == P2
    assert _relations(final, CARRIED_BY_RELATION_TYPE, OBJECT) == []
    assert len(final.movement_state.committed_transitions) == 1
    assert len(final.committed_custody_transitions) == 2


def test_true_process_boundary_restores_then_drops_and_checkpoints(tmp_path):
    pickup = _execute(
        _initial_state(), "pickup", "r4e-process-pickup", "process-pickup"
    )
    moved = _move_to_p2(pickup.state)
    first = tmp_path / "before-process.json"
    second = tmp_path / "after-process.json"
    write_persistent_world_object_custody_checkpoint(
        state=moved,
        checkpoint_path=first,
        qualification_evidence=_checkpoint_qualification("process-first"),
    )
    child = textwrap.dedent(
        f"""
        from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
            restore_persistent_world_object_custody_checkpoint,
            write_persistent_world_object_custody_checkpoint,
        )
        from astra_runtime.domain.persistent_world_movement_integration import (
            digest_persistent_world_entity_location_representation,
        )
        from astra_runtime.domain.persistent_world_object_custody_transfer import (
            create_custody_opportunity_evidence,
            create_custody_qualification_evidence,
            execute_persistent_world_object_custody,
        )
        from astra_runtime.kernel.command_envelope import create_command_envelope

        state = restore_persistent_world_object_custody_checkpoint(
            checkpoint_path={str(first)!r},
            expected_campaign_id={CAMPAIGN!r},
        )
        result = execute_persistent_world_object_custody(
            state=state,
            command=create_command_envelope(
                command_id="r4e-process-drop",
                command_type="drop_object",
                source_actor_id={ACTOR!r},
                payload={{"object_entity_id": {OBJECT!r}}},
            ),
            qualification_evidence=create_custody_qualification_evidence(
                evidence_id="astra:evidence:r4e-process-drop-rt010",
                actor_entity_id={ACTOR!r},
                object_entity_id={OBJECT!r},
                operation="drop",
                qualified=True,
            ),
            opportunity_evidence=create_custody_opportunity_evidence(
                evidence_id="astra:evidence:r4e-process-drop-afqr19",
                actor_entity_id={ACTOR!r},
                object_entity_id={OBJECT!r},
                operation="drop",
                opportunity_available=True,
                resolution_accepted=True,
            ),
            expected_pre_state_digest=(
                digest_persistent_world_entity_location_representation(
                    state.movement_state.representation
                )
            ),
        )
        write_persistent_world_object_custody_checkpoint(
            state=result.state,
            checkpoint_path={str(second)!r},
            qualification_evidence={{
                "qualification_id": "astra:evidence:r4e-process-checkpoint",
                "semantic_owner": "AFQR-01",
                "qualified": True,
                "provenance": "child-process",
            }},
        )
        """
    )
    completed = subprocess.run(
        [sys.executable, "-c", child],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    final = restore_persistent_world_object_custody_checkpoint(
        checkpoint_path=second,
        expected_campaign_id=CAMPAIGN,
    )
    assert _relations(final, LOCATED_AT_RELATION_TYPE, OBJECT)[0].object_entity_id == P2
    assert _relations(final, CARRIED_BY_RELATION_TYPE, OBJECT) == []


def test_r4e_checkpoint_identity_is_distinct_and_r4d_reader_rejects_it(tmp_path):
    pickup = _execute(
        _initial_state(), "pickup", "r4e-format-pickup", "format"
    )
    path = tmp_path / "r4e-format.json"
    write_persistent_world_object_custody_checkpoint(
        state=pickup.state,
        checkpoint_path=path,
        qualification_evidence=_checkpoint_qualification("format"),
    )
    envelope = _read(path)
    assert envelope["format_identity"] == OBJECT_CUSTODY_CHECKPOINT_FORMAT_IDENTITY
    assert envelope["format_version"] == OBJECT_CUSTODY_CHECKPOINT_FORMAT_VERSION
    assert envelope["format_identity"] != CHECKPOINT_FORMAT_IDENTITY
    with pytest.raises(PersistentWorldCheckpointFormatError):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


def test_r4d_checkpoint_explicitly_composes_with_empty_custody_history(tmp_path):
    state = _initial_state()
    path = tmp_path / "r4d.json"
    write_persistent_world_checkpoint(
        state=state.movement_state,
        checkpoint_path=path,
        qualification_evidence=_checkpoint_qualification("r4d"),
    )
    movement = restore_persistent_world_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )
    composed = create_persistent_world_object_custody_runtime_state(
        movement_state=movement
    )
    assert composed.committed_custody_transitions == ()


def test_r4e_checkpoint_payload_is_deterministic():
    pickup = _execute(
        _initial_state(), "pickup", "r4e-deterministic-pickup", "deterministic"
    )
    outputs = {
        canonical_serialize_persistent_world_object_custody_checkpoint_payload(
            pickup.state
        )
        for _ in range(100)
    }
    assert len(outputs) == 1


def test_semantic_checkpoint_tamper_fails_closed_even_with_recomputed_integrity(tmp_path):
    pickup = _execute(
        _initial_state(), "pickup", "r4e-tamper-pickup", "tamper"
    )
    path = tmp_path / "tamper.json"
    write_persistent_world_object_custody_checkpoint(
        state=pickup.state,
        checkpoint_path=path,
        qualification_evidence=_checkpoint_qualification("tamper"),
    )
    envelope = _read(path)
    transition = envelope["authoritative_payload"]["committed_custody_transitions"][0]
    transition["receipt"]["destination_relation_id"] = "astra:relation:tampered"
    transition["state_delta"]["payload"]["destination_relation_id"] = "astra:relation:tampered"
    transition["state_delta"]["affected_record_ids"][-1] = "astra:relation:tampered"
    _recompute_integrity(envelope)
    path.write_text(_canonical(envelope), encoding="utf-8")
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        restore_persistent_world_object_custody_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


def test_module_has_no_network_model_database_rng_or_state_store_dependency():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    forbidden = {
        "requests", "httpx", "urllib", "socket", "sqlite3",
        "openai", "anthropic", "random", "state_store",
    }
    for module in imported:
        assert not any(fragment in module for fragment in forbidden)
