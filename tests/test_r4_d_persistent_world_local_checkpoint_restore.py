"""Executable R4-D local checkpoint/restore tests."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

import astra_runtime.domain.persistent_world_local_checkpoint_restore as checkpoint_module
from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
    create_located_at_relation,
    create_persistent_world_entity,
    create_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    CHECKPOINT_FORMAT_IDENTITY,
    CHECKPOINT_FORMAT_VERSION,
    InvalidPersistentWorldCheckpointRequestError,
    PersistentWorldCheckpointCampaignMismatchError,
    PersistentWorldCheckpointError,
    PersistentWorldCheckpointFormatError,
    PersistentWorldCheckpointIntegrityError,
    PersistentWorldCheckpointQualificationError,
    PersistentWorldCheckpointUnavailableError,
    PersistentWorldCheckpointWriteError,
    canonical_serialize_persistent_world_checkpoint_envelope,
    canonical_serialize_persistent_world_checkpoint_payload,
    restore_persistent_world_checkpoint,
    write_persistent_world_checkpoint,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementRetryConflictError,
    create_movement_opportunity_evidence,
    create_movement_spatial_evidence,
    create_persistent_world_movement_runtime_state,
    digest_persistent_world_entity_location_representation,
    execute_persistent_world_movement,
)
from astra_runtime.kernel.command_envelope import (
    create_command_envelope,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "src/astra_runtime/domain/"
    "persistent_world_local_checkpoint_restore.py"
)

CAMPAIGN = "astra:campaign:r4d-test"
ACTOR = "astra:entity:r4d-traveler"
P1 = "astra:entity:r4d-market-square"
P2 = "astra:entity:r4d-river-gate"
P3 = "astra:entity:r4d-hill-road"


def _qualification(tag: str = "primary"):
    return {
        "qualification_id": (
            f"astra:evidence:r4d-checkpoint-{tag}"
        ),
        "semantic_owner": "AFQR-01",
        "qualified": True,
        "provenance": "r4-d-test-owner-evidence",
    }


def _entity(local: str, classification: str):
    return create_persistent_world_entity(
        entity_id=f"astra:entity:{local}",
        classification=classification,
    )


def _initial_state():
    representation = (
        create_persistent_world_entity_location_representation(
            campaign_id=CAMPAIGN,
            entities=(
                _entity(
                    "r4d-traveler",
                    "character_or_creature",
                ),
                _entity("r4d-market-square", "place"),
                _entity("r4d-river-gate", "place"),
                _entity("r4d-hill-road", "place"),
            ),
            relations=(
                create_located_at_relation(
                    relation_id=(
                        "astra:relation:"
                        "r4d-traveler-in-market-square"
                    ),
                    subject_entity_id=ACTOR,
                    object_entity_id=P1,
                ),
            ),
        )
    )

    return create_persistent_world_movement_runtime_state(
        representation=representation,
    )


def _digest(state):
    return (
        digest_persistent_world_entity_location_representation(
            state.representation
        )
    )


def _actor_location(state):
    relations = [
        relation
        for relation in state.representation.relations
        if (
            relation.relation_type
            == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == ACTOR
        )
    ]

    assert len(relations) == 1
    return relations[0]


def _move(
    state,
    *,
    command_id: str,
    destination: str,
    evidence_tag: str,
):
    source = _actor_location(state).object_entity_id

    command = create_command_envelope(
        command_id=command_id,
        command_type="move",
        source_actor_id=ACTOR,
        payload={
            "destination_entity_id": destination,
        },
    )

    result = execute_persistent_world_movement(
        state=state,
        command=command,
        spatial_evidence=create_movement_spatial_evidence(
            evidence_id=(
                f"astra:evidence:r4d-{evidence_tag}-spatial"
            ),
            actor_entity_id=ACTOR,
            source_place_id=source,
            destination_place_id=destination,
            spatially_permitted=True,
        ),
        opportunity_evidence=(
            create_movement_opportunity_evidence(
                evidence_id=(
                    "astra:evidence:"
                    f"r4d-{evidence_tag}-opportunity"
                ),
                actor_entity_id=ACTOR,
                destination_place_id=destination,
                opportunity_available=True,
                resolution_accepted=True,
            )
        ),
        expected_pre_state_digest=_digest(state),
    )

    return command, result


def _p2_state():
    state = _initial_state()

    command, result = _move(
        state,
        command_id="r4d-move-1",
        destination=P2,
        evidence_tag="move-1",
    )

    return state, command, result


def _p3_state():
    state, command1, first = _p2_state()

    command2, second = _move(
        first.state,
        command_id="r4d-move-2",
        destination=P3,
        evidence_tag="move-2",
    )

    return state, command1, first, command2, second


def _canonical_json(value) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _read_envelope(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write_envelope(path: Path, envelope):
    path.write_text(
        _canonical_json(envelope),
        encoding="utf-8",
    )


def _recompute_integrity(envelope):
    payload = envelope["authoritative_payload"]

    envelope["integrity_digest"] = hashlib.sha256(
        _canonical_json(payload).encode("utf-8")
    ).hexdigest()


def test_same_state_produces_identical_canonical_payload_bytes():
    _, _, committed = _p2_state()

    outputs = {
        canonical_serialize_persistent_world_checkpoint_payload(
            committed.state
        )
        for _ in range(100)
    }

    assert len(outputs) == 1


def test_same_state_and_qualification_produce_identical_envelope_bytes():
    _, _, committed = _p2_state()

    first = (
        canonical_serialize_persistent_world_checkpoint_envelope(
            state=committed.state,
            qualification_evidence=_qualification(),
        )
    )

    second = (
        canonical_serialize_persistent_world_checkpoint_envelope(
            state=committed.state,
            qualification_evidence=_qualification(),
        )
    )

    assert first == second


def test_checkpoint_requires_explicit_afqr01_qualification(tmp_path):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    invalid = (
        {},
        {
            "qualification_id": "astra:evidence:q",
            "semantic_owner": "AFQR-02",
            "qualified": True,
        },
        {
            "qualification_id": "astra:evidence:q",
            "semantic_owner": "AFQR-01",
            "qualified": False,
        },
    )

    for evidence in invalid:
        with pytest.raises(
            PersistentWorldCheckpointQualificationError
        ):
            write_persistent_world_checkpoint(
                state=committed.state,
                checkpoint_path=path,
                qualification_evidence=evidence,
            )

    assert not path.exists()


def test_invalid_runtime_state_fails_closed(tmp_path):
    with pytest.raises(
        InvalidPersistentWorldCheckpointRequestError
    ):
        write_persistent_world_checkpoint(
            state=object(),
            checkpoint_path=tmp_path / "checkpoint.json",
            qualification_evidence=_qualification(),
        )


def test_checkpoint_write_does_not_mutate_runtime_state(tmp_path):
    _, _, committed = _p2_state()

    before = committed.state

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=tmp_path / "checkpoint.json",
        qualification_evidence=_qualification(),
    )

    assert committed.state == before


def test_local_file_round_trip_reconstructs_same_authoritative_state(
    tmp_path,
):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    expected_digest = _digest(committed.state)

    del committed

    restored = restore_persistent_world_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )

    assert _digest(restored) == expected_digest
    assert _actor_location(restored).object_entity_id == P2
    assert len(restored.committed_transitions) == 1


def test_complete_r4c_transition_evidence_survives_restore(
    tmp_path,
):
    _, _, _, _, committed = _p3_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    restored = restore_persistent_world_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )

    assert (
        digest_persistent_world_entity_location_representation(
            restored.representation
        )
        == digest_persistent_world_entity_location_representation(
            committed.state.representation
        )
    )

    assert len(restored.committed_transitions) == 2

    original = {
        transition.command_id: transition
        for transition in committed.state.committed_transitions
    }

    recovered = {
        transition.command_id: transition
        for transition in restored.committed_transitions
    }

    assert set(original) == set(recovered)

    for command_id in original:
        assert (
            recovered[command_id].command_fingerprint
            == original[command_id].command_fingerprint
        )

        assert (
            recovered[command_id].preview.to_dict()
            == original[command_id].preview.to_dict()
        )

        assert (
            recovered[command_id].state_delta.to_dict()
            == original[command_id].state_delta.to_dict()
        )

        assert (
            recovered[command_id].receipt.to_dict()
            == original[command_id].receipt.to_dict()
        )


def test_multiple_committed_transitions_and_final_position_survive(
    tmp_path,
):
    _, _, _, _, committed = _p3_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    restored = restore_persistent_world_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )

    assert len(restored.committed_transitions) == 2
    assert _actor_location(restored).object_entity_id == P3


def test_post_restore_identical_command_is_technical_retry(
    tmp_path,
):
    initial, command, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    restored = restore_persistent_world_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )

    retry = execute_persistent_world_movement(
        state=restored,
        command=command,
        spatial_evidence=create_movement_spatial_evidence(
            evidence_id=(
                "astra:evidence:r4d-retry-spatial"
            ),
            actor_entity_id=ACTOR,
            source_place_id=P1,
            destination_place_id=P2,
            spatially_permitted=True,
        ),
        opportunity_evidence=(
            create_movement_opportunity_evidence(
                evidence_id=(
                    "astra:evidence:"
                    "r4d-retry-opportunity"
                ),
                actor_entity_id=ACTOR,
                destination_place_id=P2,
                opportunity_available=True,
                resolution_accepted=True,
            )
        ),
        expected_pre_state_digest=_digest(initial),
    )

    assert retry.technical_retry is True
    assert retry.state == restored
    assert len(retry.state.committed_transitions) == 1
    assert _actor_location(retry.state).object_entity_id == P2


def test_post_restore_changed_command_same_id_is_retry_conflict(
    tmp_path,
):
    _, command, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    restored = restore_persistent_world_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )

    changed = create_command_envelope(
        command_id=command.command_id,
        command_type="move",
        source_actor_id=ACTOR,
        payload={
            "destination_entity_id": P3,
        },
    )

    with pytest.raises(
        PersistentWorldMovementRetryConflictError
    ):
        execute_persistent_world_movement(
            state=restored,
            command=changed,
            spatial_evidence=create_movement_spatial_evidence(
                evidence_id=(
                    "astra:evidence:"
                    "r4d-conflict-spatial"
                ),
                actor_entity_id=ACTOR,
                source_place_id=P2,
                destination_place_id=P3,
                spatially_permitted=True,
            ),
            opportunity_evidence=(
                create_movement_opportunity_evidence(
                    evidence_id=(
                        "astra:evidence:"
                        "r4d-conflict-opportunity"
                    ),
                    actor_entity_id=ACTOR,
                    destination_place_id=P3,
                    opportunity_available=True,
                    resolution_accepted=True,
                )
            ),
            expected_pre_state_digest=_digest(restored),
        )

    assert _actor_location(restored).object_entity_id == P2
    assert len(restored.committed_transitions) == 1


def test_checkpoint_restore_checkpoint_preserves_authoritative_payload(
    tmp_path,
):
    _, _, _, _, committed = _p3_state()

    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=first,
        qualification_evidence=_qualification("first"),
    )

    restored = restore_persistent_world_checkpoint(
        checkpoint_path=first,
        expected_campaign_id=CAMPAIGN,
    )

    write_persistent_world_checkpoint(
        state=restored,
        checkpoint_path=second,
        qualification_evidence=_qualification("second"),
    )

    assert (
        canonical_serialize_persistent_world_checkpoint_payload(
            committed.state
        )
        == canonical_serialize_persistent_world_checkpoint_payload(
            restored
        )
    )

    assert (
        _read_envelope(first)["authoritative_payload"]
        == _read_envelope(second)["authoritative_payload"]
    )


def test_storage_order_is_preserved_but_not_claimed_as_causal_order(
    tmp_path,
):
    state = _initial_state()

    _, first = _move(
        state,
        command_id="z-first-causal-command",
        destination=P2,
        evidence_tag="z-first",
    )

    _, second = _move(
        first.state,
        command_id="a-second-causal-command",
        destination=P3,
        evidence_tag="a-second",
    )

    ids = [
        transition.command_id
        for transition in second.state.committed_transitions
    ]

    # R4-C deterministically sorts by command identity, which is deliberately
    # different from this test's actual commit sequence.
    assert ids == [
        "a-second-causal-command",
        "z-first-causal-command",
    ]

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=second.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    restored = restore_persistent_world_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )

    assert [
        transition.command_id
        for transition in restored.committed_transitions
    ] == ids

    text = path.read_text(encoding="utf-8")

    assert '"logical_time"' not in text
    assert '"causal_order"' not in text


def test_atomic_replacement_failure_preserves_prior_valid_checkpoint(
    tmp_path,
    monkeypatch,
):
    _, _, first = _p2_state()

    _, _, _, _, second = _p3_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=first.state,
        checkpoint_path=path,
        qualification_evidence=_qualification("p2"),
    )

    prior = path.read_bytes()

    def fail_replace(source, destination):
        raise OSError("injected replace failure")

    monkeypatch.setattr(
        checkpoint_module.os,
        "replace",
        fail_replace,
    )

    with pytest.raises(PersistentWorldCheckpointWriteError):
        write_persistent_world_checkpoint(
            state=second.state,
            checkpoint_path=path,
            qualification_evidence=_qualification("p3"),
        )

    assert path.read_bytes() == prior

    restored = restore_persistent_world_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=CAMPAIGN,
    )

    assert _actor_location(restored).object_entity_id == P2


def test_successful_checkpoint_executes_file_and_directory_fsync(
    tmp_path,
    monkeypatch,
):
    _, _, committed = _p2_state()

    calls = []

    real_fsync = checkpoint_module.os.fsync

    def observing_fsync(descriptor):
        calls.append(descriptor)
        return real_fsync(descriptor)

    monkeypatch.setattr(
        checkpoint_module.os,
        "fsync",
        observing_fsync,
    )

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=tmp_path / "checkpoint.json",
        qualification_evidence=_qualification(),
    )

    assert len(calls) >= 2


def test_missing_checkpoint_does_not_claim_crash_recovery(tmp_path):
    with pytest.raises(
        PersistentWorldCheckpointUnavailableError
    ):
        restore_persistent_world_checkpoint(
            checkpoint_path=tmp_path / "absent.json",
            expected_campaign_id=CAMPAIGN,
        )


def test_truncated_checkpoint_fails_closed(tmp_path):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    material = path.read_bytes()

    path.write_bytes(material[: len(material) // 2])

    with pytest.raises(PersistentWorldCheckpointError):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


def test_malformed_serialization_fails_closed(tmp_path):
    path = tmp_path / "checkpoint.json"
    path.write_bytes(b"{not-json")

    with pytest.raises(PersistentWorldCheckpointFormatError):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


def test_integrity_digest_mismatch_fails_closed(tmp_path):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    envelope = _read_envelope(path)
    envelope["integrity_digest"] = "0" * 64
    _write_envelope(path, envelope)

    with pytest.raises(
        PersistentWorldCheckpointIntegrityError
    ):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("format_identity", "unknown.checkpoint.format"),
        ("format_version", 999),
    ],
)
def test_unsupported_checkpoint_format_fails_closed(
    tmp_path,
    field,
    value,
):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    envelope = _read_envelope(path)
    envelope[field] = value
    _write_envelope(path, envelope)

    with pytest.raises(PersistentWorldCheckpointFormatError):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


def test_wrong_expected_campaign_fails_closed(tmp_path):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    with pytest.raises(
        PersistentWorldCheckpointCampaignMismatchError
    ):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id="astra:campaign:other",
        )


def test_tampered_checkpoint_campaign_identity_fails_closed(
    tmp_path,
):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    envelope = _read_envelope(path)
    envelope["campaign_identity"] = "astra:campaign:other"
    _write_envelope(path, envelope)

    with pytest.raises(
        PersistentWorldCheckpointCampaignMismatchError
    ):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


def test_tampered_qualification_provenance_fails_closed(tmp_path):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    envelope = _read_envelope(path)
    envelope["qualification_provenance"]["qualified"] = False
    _write_envelope(path, envelope)

    with pytest.raises(
        PersistentWorldCheckpointQualificationError
    ):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


def test_extra_checkpoint_envelope_field_fails_closed(tmp_path):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    envelope = _read_envelope(path)
    envelope["unexpected"] = "not-authoritative"
    _write_envelope(path, envelope)

    with pytest.raises(PersistentWorldCheckpointFormatError):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


@pytest.mark.parametrize(
    "case",
    [
        "missing_committed_transition",
        "altered_command_fingerprint",
        "altered_movement_receipt",
        "altered_state_delta",
        "receipt_delta_disagreement",
        "duplicate_command_identity",
        "invalid_entity_location_reference",
    ],
)
def test_semantic_tampering_fails_closed_even_with_recomputed_digest(
    tmp_path,
    case,
):
    _, _, _, _, committed = _p3_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    envelope = _read_envelope(path)

    payload = envelope["authoritative_payload"]
    transitions = payload["committed_transitions"]

    if case == "missing_committed_transition":
        transitions.pop(0)

    elif case == "altered_command_fingerprint":
        transitions[0]["command_fingerprint"] = "0" * 64

    elif case == "altered_movement_receipt":
        transitions[0]["receipt"][
            "destination_place_id"
        ] = P1

    elif case == "altered_state_delta":
        transitions[0]["state_delta"]["payload"][
            "to_place_id"
        ] = P1

    elif case == "receipt_delta_disagreement":
        transitions[0]["receipt"][
            "state_delta_id"
        ] = transitions[1]["state_delta"]["delta_id"]

    elif case == "duplicate_command_identity":
        transitions.append(
            copy.deepcopy(transitions[0])
        )

    elif case == "invalid_entity_location_reference":
        payload["representation"]["relations"][0][
            "object_entity_id"
        ] = "astra:entity:missing-place"

    else:
        raise AssertionError(case)

    _recompute_integrity(envelope)
    _write_envelope(path, envelope)

    with pytest.raises(PersistentWorldCheckpointError):
        restore_persistent_world_checkpoint(
            checkpoint_path=path,
            expected_campaign_id=CAMPAIGN,
        )


def test_true_process_boundary_restore_continues_play_and_persists_again(
    tmp_path,
):
    _, _, committed = _p2_state()

    first_path = tmp_path / "before-process-exit.json"
    second_path = tmp_path / "after-new-play.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=first_path,
        qualification_evidence=_qualification("before-process"),
    )

    child = textwrap.dedent(
        f"""
        from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
            restore_persistent_world_checkpoint,
            write_persistent_world_checkpoint,
        )
        from astra_runtime.domain.persistent_world_movement_integration import (
            create_movement_opportunity_evidence,
            create_movement_spatial_evidence,
            digest_persistent_world_entity_location_representation,
            execute_persistent_world_movement,
        )
        from astra_runtime.kernel.command_envelope import (
            create_command_envelope,
        )

        CAMPAIGN = {CAMPAIGN!r}
        ACTOR = {ACTOR!r}
        P2 = {P2!r}
        P3 = {P3!r}

        state = restore_persistent_world_checkpoint(
            checkpoint_path={str(first_path)!r},
            expected_campaign_id=CAMPAIGN,
        )

        command = create_command_envelope(
            command_id="r4d-new-command-after-process-restore",
            command_type="move",
            source_actor_id=ACTOR,
            payload={{"destination_entity_id": P3}},
        )

        result = execute_persistent_world_movement(
            state=state,
            command=command,
            spatial_evidence=create_movement_spatial_evidence(
                evidence_id="astra:evidence:r4d-child-spatial",
                actor_entity_id=ACTOR,
                source_place_id=P2,
                destination_place_id=P3,
                spatially_permitted=True,
            ),
            opportunity_evidence=create_movement_opportunity_evidence(
                evidence_id="astra:evidence:r4d-child-opportunity",
                actor_entity_id=ACTOR,
                destination_place_id=P3,
                opportunity_available=True,
                resolution_accepted=True,
            ),
            expected_pre_state_digest=(
                digest_persistent_world_entity_location_representation(
                    state.representation
                )
            ),
        )

        write_persistent_world_checkpoint(
            state=result.state,
            checkpoint_path={str(second_path)!r},
            qualification_evidence={{
                "qualification_id":
                    "astra:evidence:r4d-child-checkpoint",
                "semantic_owner": "AFQR-01",
                "qualified": True,
                "provenance": "child-process",
            }},
        )
        """
    )

    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            child,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 0, (
        completed.stdout,
        completed.stderr,
    )

    # The child process has exited. Reconstruction now occurs again from the
    # second checkpoint bytes, not from any child-process Python object.
    restored_again = restore_persistent_world_checkpoint(
        checkpoint_path=second_path,
        expected_campaign_id=CAMPAIGN,
    )

    assert (
        _actor_location(restored_again).object_entity_id
        == P3
    )

    assert len(
        restored_again.committed_transitions
    ) == 2

    assert {
        transition.command_id
        for transition in restored_again.committed_transitions
    } == {
        "r4d-move-1",
        "r4d-new-command-after-process-restore",
    }


def test_checkpoint_format_identity_is_explicit(tmp_path):
    _, _, committed = _p2_state()

    path = tmp_path / "checkpoint.json"

    write_persistent_world_checkpoint(
        state=committed.state,
        checkpoint_path=path,
        qualification_evidence=_qualification(),
    )

    envelope = _read_envelope(path)

    assert (
        envelope["format_identity"]
        == CHECKPOINT_FORMAT_IDENTITY
    )

    assert (
        envelope["format_version"]
        == CHECKPOINT_FORMAT_VERSION
    )

    assert envelope["campaign_identity"] == CAMPAIGN

    assert set(envelope) == {
        "format_identity",
        "format_version",
        "campaign_identity",
        "authoritative_payload",
        "integrity_digest",
        "qualification_provenance",
    }


def test_module_has_no_network_model_database_or_state_store_dependency():
    tree = ast.parse(
        SOURCE.read_text(encoding="utf-8")
    )

    imported = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(
                alias.name
                for alias in node.names
            )

        elif (
            isinstance(node, ast.ImportFrom)
            and node.module
        ):
            imported.add(node.module)

    forbidden = {
        "requests",
        "httpx",
        "urllib",
        "socket",
        "sqlite3",
        "openai",
        "anthropic",
        "state_store",
        "random",
    }

    for module in imported:
        assert not any(
            fragment in module
            for fragment in forbidden
        )
