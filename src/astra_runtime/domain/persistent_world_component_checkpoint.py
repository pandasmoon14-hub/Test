"""Static componentized checkpoint formats for the Myravant playable runtime.

Version 1 preserves the five-component RUNTIME-CHECKPOINT-COMPONENTIZATION-1
format. WORLD-1 adds version 2 with one typed logical-time component.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointCampaignMismatchError,
    PersistentWorldCheckpointEvidenceError,
    PersistentWorldCheckpointFormatError,
    PersistentWorldCheckpointIntegrityError,
    PersistentWorldCheckpointWriteError,
    _canonical_bytes,
    _checkpoint_path,
    _normalize_qualification,
    _read_checkpoint_envelope,
    _replace_checkpoint_durably,
    _require_exact_dict,
    _require_record_id,
    _require_sha256,
    _restore_persistent_world_object_storage_payload,
    _sha256_bytes,
    serialize_persistent_world_object_storage_checkpoint_payload,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    PersistentWorldEntityLocationRepresentation,
    canonical_serialize_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementCommitReceipt,
    digest_persistent_world_entity_location_representation,
    replay_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyCommitReceipt,
    replay_persistent_world_object_custody,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    PersistentWorldObjectDisplacementCommitReceipt,
    PersistentWorldObjectDisplacementCommittedTransition,
    replay_persistent_world_object_displacement,
    serialize_persistent_world_object_displacement_commit_receipt,
)
from astra_runtime.domain.persistent_world_logical_time import (
    InvalidPersistentWorldLogicalTimeRequestError,
    restore_persistent_world_logical_time_state,
    serialize_persistent_world_logical_time_state,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    PersistentWorldObjectLitState,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenState,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    PersistentWorldObjectStorageCommitReceipt,
    PersistentWorldObjectStorageRuntimeState,
    replay_persistent_world_object_storage,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    PersistentWorldRuntimeComposition,
    compose_persistent_world_storage_state,
    create_persistent_world_runtime_composition_from_storage_state,
)
from astra_runtime.kernel.state_delta import StateDeltaEnvelope
from astra_runtime.kernel.transaction_preview import TransactionPreview

COMPONENT_CHECKPOINT_FORMAT_IDENTITY = (
    "myravant.componentized.persistent_world_checkpoint"
)
COMPONENT_CHECKPOINT_FORMAT_VERSION = 1
WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION = 2
COMP3_COMPONENT_CHECKPOINT_FORMAT_VERSION = 3

COMPONENT_CHECKPOINT_COMPONENT_KEYS = frozenset(
    {"placement", "custody", "open_close", "lit_state", "storage"}
)
WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS = frozenset(
    {*COMPONENT_CHECKPOINT_COMPONENT_KEYS, "logical_time"}
)
COMP3_COMPONENT_CHECKPOINT_COMPONENT_KEYS = frozenset(
    {*WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS, "object_displacement"}
)
_PAYLOAD_KEYS = frozenset({"components"})
_PLACEMENT_COMPONENT_KEYS = frozenset(
    {
        "representation",
        "representation_digest",
        "committed_movement_transitions",
        "movement_transition_summary",
    }
)
_CUSTODY_COMPONENT_KEYS = frozenset(
    {"committed_custody_transitions", "custody_transition_summary"}
)
_OPEN_CLOSE_COMPONENT_KEYS = frozenset(
    {
        "object_open_states",
        "object_state_digest",
        "world_state_digest",
        "committed_object_state_transitions",
        "object_state_transition_summary",
    }
)
_LIT_STATE_COMPONENT_KEYS = frozenset(
    {
        "object_lit_states",
        "object_lit_state_digest",
        "world_state_digest",
        "committed_object_lit_transitions",
        "object_lit_transition_summary",
    }
)
_STORAGE_COMPONENT_KEYS = frozenset(
    {
        "containment_digest",
        "world_state_digest",
        "committed_storage_transitions",
        "storage_transition_summary",
    }
)
_DISPLACEMENT_COMPONENT_KEYS = frozenset(
    {
        "committed_object_displacement_transitions",
        "object_displacement_transition_summary",
    }
)
_DISPLACEMENT_TRANSITION_KEYS = frozenset(
    {"command_id", "command_fingerprint", "preview", "state_delta", "receipt"}
)
_DISPLACEMENT_PREVIEW_KEYS = frozenset(
    {
        "preview_id",
        "command_id",
        "status",
        "messages",
        "requires_confirmation",
        "metadata",
    }
)
_DISPLACEMENT_DELTA_KEYS = frozenset(
    {
        "delta_id",
        "source_command_id",
        "source_preview_id",
        "affected_record_ids",
        "change_type",
        "payload",
        "metadata",
    }
)
_DISPLACEMENT_RECEIPT_KEYS = frozenset(
    {
        "receipt_id",
        "command_id",
        "command_fingerprint",
        "actor_entity_id",
        "object_entity_id",
        "method",
        "source_place_id",
        "destination_place_id",
        "source_relation_id",
        "source_relation_type",
        "destination_relation_id",
        "destination_relation_type",
        "pre_state_digest",
        "post_state_digest",
        "preview_id",
        "state_delta_id",
        "rt010_qualification_id",
        "spatial_evidence_id",
        "opportunity_evidence_id",
        "status",
    }
)


def _select(source: Mapping[str, Any], keys: frozenset[str]):
    return {key: source[key] for key in keys}


def serialize_persistent_world_component_checkpoint_payload(state):
    legacy = serialize_persistent_world_object_storage_checkpoint_payload(state)
    int2 = legacy["int2_state"]
    int1 = int2["int1_state"]
    r4e = int1["r4e_state"]
    return {
        "components": {
            "placement": _select(r4e, _PLACEMENT_COMPONENT_KEYS),
            "custody": _select(r4e, _CUSTODY_COMPONENT_KEYS),
            "open_close": _select(int1, _OPEN_CLOSE_COMPONENT_KEYS),
            "lit_state": _select(int2, _LIT_STATE_COMPONENT_KEYS),
            "storage": _select(legacy, _STORAGE_COMPONENT_KEYS),
        }
    }


def canonical_serialize_persistent_world_component_checkpoint_payload(state):
    return _canonical_bytes(
        serialize_persistent_world_component_checkpoint_payload(state)
    )


def build_persistent_world_component_checkpoint_envelope(
    *, state, qualification_evidence
):
    payload = serialize_persistent_world_component_checkpoint_payload(state)
    qualification = _normalize_qualification(qualification_evidence)
    campaign_id = (
        state.lit_state.open_close_state.custody_state.movement_state
        .representation.campaign_id
    )
    return {
        "format_identity": COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
        "format_version": COMPONENT_CHECKPOINT_FORMAT_VERSION,
        "campaign_identity": campaign_id,
        "authoritative_payload": payload,
        "integrity_digest": _sha256_bytes(_canonical_bytes(payload)),
        "qualification_provenance": qualification,
    }


def canonical_serialize_persistent_world_component_checkpoint_envelope(
    *, state, qualification_evidence
):
    return _canonical_bytes(
        build_persistent_world_component_checkpoint_envelope(
            state=state,
            qualification_evidence=qualification_evidence,
        )
    )


def _write_envelope(*, envelope, checkpoint_path):
    path = _checkpoint_path(checkpoint_path)
    parent = path.parent
    if not parent.exists() or not parent.is_dir():
        raise PersistentWorldCheckpointWriteError(
            "caller-supplied checkpoint parent directory does not exist"
        )
    material = _canonical_bytes(envelope)
    temporary_path = None
    try:
        descriptor, temporary_path = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".component-tmp",
            dir=parent,
        )
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(material)
            handle.flush()
            os.fsync(handle.fileno())
        _replace_checkpoint_durably(Path(temporary_path), path)
        temporary_path = None
    except OSError as exc:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except (FileNotFoundError, OSError):
                pass
        raise PersistentWorldCheckpointWriteError(
            "component checkpoint durability operation failed"
        ) from exc
    return str(envelope["integrity_digest"])


def write_persistent_world_component_checkpoint(
    *, state, checkpoint_path, qualification_evidence
):
    return _write_envelope(
        envelope=build_persistent_world_component_checkpoint_envelope(
            state=state,
            qualification_evidence=qualification_evidence,
        ),
        checkpoint_path=checkpoint_path,
    )


def _reconstruct_int3_payload(payload_material):
    payload = _require_exact_dict(
        payload_material,
        expected_keys=_PAYLOAD_KEYS,
        name="component checkpoint authoritative payload",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    components = _require_exact_dict(
        payload["components"],
        expected_keys=COMPONENT_CHECKPOINT_COMPONENT_KEYS,
        name="component checkpoint components",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    placement = _require_exact_dict(
        components["placement"],
        expected_keys=_PLACEMENT_COMPONENT_KEYS,
        name="placement component",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    custody = _require_exact_dict(
        components["custody"],
        expected_keys=_CUSTODY_COMPONENT_KEYS,
        name="custody component",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    open_close = _require_exact_dict(
        components["open_close"],
        expected_keys=_OPEN_CLOSE_COMPONENT_KEYS,
        name="open_close component",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    lit_state = _require_exact_dict(
        components["lit_state"],
        expected_keys=_LIT_STATE_COMPONENT_KEYS,
        name="lit_state component",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    storage = _require_exact_dict(
        components["storage"],
        expected_keys=_STORAGE_COMPONENT_KEYS,
        name="storage component",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    r4e = {**placement, **custody}
    int1 = {"r4e_state": r4e, **open_close}
    int2 = {"int1_state": int1, **lit_state}
    return {"int2_state": int2, **storage}


def _validate_envelope_common(
    *, envelope, expected_campaign_id, expected_version
):
    if envelope["format_identity"] != COMPONENT_CHECKPOINT_FORMAT_IDENTITY:
        raise PersistentWorldCheckpointFormatError(
            "unsupported component checkpoint format identity"
        )
    if (
        type(envelope["format_version"]) is not int
        or envelope["format_version"] != expected_version
    ):
        raise PersistentWorldCheckpointFormatError(
            "unsupported component checkpoint format version"
        )
    campaign_identity = _require_record_id(
        envelope["campaign_identity"],
        name="checkpoint campaign_identity",
    )
    if campaign_identity != expected_campaign_id:
        raise PersistentWorldCheckpointCampaignMismatchError(
            "checkpoint campaign identity does not match caller expectation"
        )
    _normalize_qualification(envelope["qualification_provenance"])
    payload = _require_exact_dict(
        envelope["authoritative_payload"],
        expected_keys=_PAYLOAD_KEYS,
        name="component checkpoint authoritative payload",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    integrity = _require_sha256(
        envelope["integrity_digest"],
        name="integrity_digest",
        error_cls=PersistentWorldCheckpointIntegrityError,
    )
    if _sha256_bytes(_canonical_bytes(payload)) != integrity:
        raise PersistentWorldCheckpointIntegrityError(
            "component checkpoint authoritative payload integrity mismatch"
        )
    return payload


def restore_persistent_world_component_checkpoint(
    *,
    checkpoint_path,
    expected_campaign_id,
    expected_initial_open_states,
    expected_initial_lit_states,
    expected_initial_representation_digest,
):
    path = _checkpoint_path(checkpoint_path)
    expected_campaign_id = _require_record_id(
        expected_campaign_id, name="expected_campaign_id"
    )
    envelope = _read_checkpoint_envelope(path)
    payload = _validate_envelope_common(
        envelope=envelope,
        expected_campaign_id=expected_campaign_id,
        expected_version=COMPONENT_CHECKPOINT_FORMAT_VERSION,
    )
    int3_payload = _reconstruct_int3_payload(payload)
    return _restore_persistent_world_object_storage_payload(
        payload_material=int3_payload,
        expected_campaign_id=expected_campaign_id,
        expected_initial_open_states=expected_initial_open_states,
        expected_initial_lit_states=expected_initial_lit_states,
        expected_initial_representation_digest=(
            expected_initial_representation_digest
        ),
    )


def serialize_persistent_world_world1_checkpoint_payload(state):
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise PersistentWorldCheckpointEvidenceError(
            "WORLD-1 checkpoint state must be PersistentWorldRuntimeComposition"
        )
    payload = serialize_persistent_world_component_checkpoint_payload(
        compose_persistent_world_storage_state(state)
    )
    payload["components"]["logical_time"] = (
        serialize_persistent_world_logical_time_state(
            state.logical_time_state
        )
    )
    return payload


def build_persistent_world_world1_checkpoint_envelope(
    *, state, qualification_evidence
):
    payload = serialize_persistent_world_world1_checkpoint_payload(state)
    return {
        "format_identity": COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
        "format_version": WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION,
        "campaign_identity": state.movement_state.representation.campaign_id,
        "authoritative_payload": payload,
        "integrity_digest": _sha256_bytes(_canonical_bytes(payload)),
        "qualification_provenance": _normalize_qualification(
            qualification_evidence
        ),
    }


def canonical_serialize_persistent_world_world1_checkpoint_envelope(
    *, state, qualification_evidence
):
    return _canonical_bytes(
        build_persistent_world_world1_checkpoint_envelope(
            state=state,
            qualification_evidence=qualification_evidence,
        )
    )


def write_persistent_world_world1_checkpoint(
    *, state, checkpoint_path, qualification_evidence
):
    return _write_envelope(
        envelope=build_persistent_world_world1_checkpoint_envelope(
            state=state,
            qualification_evidence=qualification_evidence,
        ),
        checkpoint_path=checkpoint_path,
    )


def restore_persistent_world_world1_checkpoint(
    *,
    checkpoint_path,
    expected_campaign_id,
    expected_initial_open_states,
    expected_initial_lit_states,
    expected_initial_representation_digest,
):
    path = _checkpoint_path(checkpoint_path)
    expected_campaign_id = _require_record_id(
        expected_campaign_id, name="expected_campaign_id"
    )
    envelope = _read_checkpoint_envelope(path)
    payload = _validate_envelope_common(
        envelope=envelope,
        expected_campaign_id=expected_campaign_id,
        expected_version=WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION,
    )
    components = _require_exact_dict(
        payload["components"],
        expected_keys=WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
        name="WORLD-1 checkpoint components",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    base_payload = {
        "components": {
            key: value
            for key, value in components.items()
            if key != "logical_time"
        }
    }
    storage_state = _restore_persistent_world_object_storage_payload(
        payload_material=_reconstruct_int3_payload(base_payload),
        expected_campaign_id=expected_campaign_id,
        expected_initial_open_states=expected_initial_open_states,
        expected_initial_lit_states=expected_initial_lit_states,
        expected_initial_representation_digest=(
            expected_initial_representation_digest
        ),
    )
    try:
        logical_time_state = restore_persistent_world_logical_time_state(
            components["logical_time"]
        )
    except InvalidPersistentWorldLogicalTimeRequestError as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "WORLD-1 logical-time checkpoint component is invalid"
        ) from exc
    return create_persistent_world_runtime_composition_from_storage_state(
        storage_state,
        logical_time_state=logical_time_state,
    )
def _serialize_object_displacement_transition(transition):
    if not isinstance(
        transition,
        PersistentWorldObjectDisplacementCommittedTransition,
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "object displacement transition has invalid type"
        )
    return {
        "command_id": transition.command_id,
        "command_fingerprint": transition.command_fingerprint,
        "preview": transition.preview.to_dict(),
        "state_delta": transition.state_delta.to_dict(),
        "receipt": (
            serialize_persistent_world_object_displacement_commit_receipt(
                transition.receipt
            )
        ),
    }


def serialize_persistent_world_comp3_checkpoint_payload(state):
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise PersistentWorldCheckpointEvidenceError(
            "COMP-3 checkpoint state must be PersistentWorldRuntimeComposition"
        )
    payload = serialize_persistent_world_world1_checkpoint_payload(state)
    transitions = [
        _serialize_object_displacement_transition(item)
        for item in state.committed_object_displacement_transitions
    ]
    payload["components"]["object_displacement"] = {
        "committed_object_displacement_transitions": transitions,
        "object_displacement_transition_summary": {
            "count": len(transitions),
            "command_ids": sorted(
                item["command_id"] for item in transitions
            ),
        },
    }
    return payload


def build_persistent_world_comp3_checkpoint_envelope(
    *, state, qualification_evidence
):
    payload = serialize_persistent_world_comp3_checkpoint_payload(state)
    return {
        "format_identity": COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
        "format_version": COMP3_COMPONENT_CHECKPOINT_FORMAT_VERSION,
        "campaign_identity": state.movement_state.representation.campaign_id,
        "authoritative_payload": payload,
        "integrity_digest": _sha256_bytes(_canonical_bytes(payload)),
        "qualification_provenance": _normalize_qualification(
            qualification_evidence
        ),
    }


def write_persistent_world_comp3_checkpoint(
    *, state, checkpoint_path, qualification_evidence
):
    return _write_envelope(
        envelope=build_persistent_world_comp3_checkpoint_envelope(
            state=state,
            qualification_evidence=qualification_evidence,
        ),
        checkpoint_path=checkpoint_path,
    )


def _restore_object_displacement_transition(material):
    transition = _require_exact_dict(
        material,
        expected_keys=_DISPLACEMENT_TRANSITION_KEYS,
        name="object displacement transition",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    receipt_material = _require_exact_dict(
        transition["receipt"],
        expected_keys=_DISPLACEMENT_RECEIPT_KEYS,
        name="object displacement receipt",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    try:
        receipt = PersistentWorldObjectDisplacementCommitReceipt(
            **receipt_material
        )
    except Exception as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "object displacement receipt is invalid"
        ) from exc

    command_id = transition["command_id"]
    command_fingerprint = transition["command_fingerprint"]
    if (
        not isinstance(command_id, str)
        or not command_id
        or command_id != receipt.command_id
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "object displacement transition command identity is inconsistent"
        )
    _require_sha256(
        command_fingerprint,
        name="object displacement transition.command_fingerprint",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    if command_fingerprint != receipt.command_fingerprint:
        raise PersistentWorldCheckpointEvidenceError(
            "object displacement transition fingerprint is inconsistent"
        )

    preview_material = _require_exact_dict(
        transition["preview"],
        expected_keys=_DISPLACEMENT_PREVIEW_KEYS,
        name="object displacement preview",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    expected_preview_metadata = {
        "package": "TERMINAL-PLAY-COMP-3",
        "command_family": "inventory",
        "mutation_performed": False,
    }
    if (
        preview_material["command_id"] != command_id
        or preview_material["preview_id"] != receipt.preview_id
        or preview_material["status"] != "preview_created"
        or preview_material["messages"]
        != ["bounded thrown-object displacement prepared"]
        or preview_material["requires_confirmation"] is not False
        or preview_material["metadata"] != expected_preview_metadata
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "object displacement preview is inconsistent"
        )
    preview = TransactionPreview(
        preview_id=preview_material["preview_id"],
        command_id=command_id,
        status="preview_created",
        messages=("bounded thrown-object displacement prepared",),
        requires_confirmation=False,
        metadata=MappingProxyType(dict(expected_preview_metadata)),
    )

    delta_material = _require_exact_dict(
        transition["state_delta"],
        expected_keys=_DISPLACEMENT_DELTA_KEYS,
        name="object displacement state delta",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    expected_affected = [
        receipt.actor_entity_id,
        receipt.object_entity_id,
        receipt.source_place_id,
        receipt.destination_place_id,
        receipt.source_relation_id,
        receipt.destination_relation_id,
    ]
    expected_payload = {
        "method": receipt.method,
        "actor_entity_id": receipt.actor_entity_id,
        "object_entity_id": receipt.object_entity_id,
        "source_place_id": receipt.source_place_id,
        "destination_place_id": receipt.destination_place_id,
        "source_relation_id": receipt.source_relation_id,
        "source_relation_type": receipt.source_relation_type,
        "destination_relation_id": receipt.destination_relation_id,
        "destination_relation_type": receipt.destination_relation_type,
    }
    expected_metadata = {
        "package": "TERMINAL-PLAY-COMP-3",
        "placement_semantic_owner": "RT-010",
        "spatial_semantic_owner": "AFQR-18",
        "opportunity_semantic_owner": "AFQR-19",
        "qualified_transition_owner": "AFQR-01",
    }
    if (
        delta_material["source_command_id"] != command_id
        or delta_material["source_preview_id"] != receipt.preview_id
        or delta_material["delta_id"] != receipt.state_delta_id
        or delta_material["affected_record_ids"] != expected_affected
        or delta_material["change_type"] != "relationship_update"
        or delta_material["payload"] != expected_payload
        or delta_material["metadata"] != expected_metadata
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "object displacement state delta is inconsistent"
        )
    state_delta = StateDeltaEnvelope(
        delta_id=delta_material["delta_id"],
        source_command_id=command_id,
        source_preview_id=receipt.preview_id,
        affected_record_ids=tuple(expected_affected),
        change_type="relationship_update",
        payload=MappingProxyType(dict(expected_payload)),
        metadata=MappingProxyType(dict(expected_metadata)),
    )
    return PersistentWorldObjectDisplacementCommittedTransition(
        command_id=command_id,
        command_fingerprint=command_fingerprint,
        preview=preview,
        state_delta=state_delta,
        receipt=receipt,
    )


def _validate_comp3_placement_replay(
    *,
    initial_representation,
    final_representation,
    storage_state,
    displacement_transitions,
    expected_initial_representation_digest,
):
    if not isinstance(
        initial_representation,
        PersistentWorldEntityLocationRepresentation,
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "COMP-3 initial representation has invalid type"
        )
    initial_digest = digest_persistent_world_entity_location_representation(
        initial_representation
    )
    if initial_digest != expected_initial_representation_digest:
        raise PersistentWorldCheckpointEvidenceError(
            "COMP-3 initial representation digest disagrees with fixture"
        )

    movement = (
        storage_state.lit_state.open_close_state.custody_state
        .movement_state.committed_transitions
    )
    custody = (
        storage_state.lit_state.open_close_state.custody_state
        .committed_custody_transitions
    )
    storage = storage_state.committed_storage_transitions
    transitions = [
        *movement,
        *custody,
        *storage,
        *displacement_transitions,
    ]
    if not displacement_transitions:
        raise PersistentWorldCheckpointEvidenceError(
            "COMP-3 checkpoint requires displacement history"
        )

    ids = [item.command_id for item in transitions]
    if len(ids) != len(set(ids)):
        raise PersistentWorldCheckpointEvidenceError(
            "COMP-3 placement command identities collide"
        )

    outgoing = {}
    incoming = {}
    for item in transitions:
        pre_digest = item.receipt.pre_state_digest
        post_digest = item.receipt.post_state_digest
        if pre_digest == post_digest:
            raise PersistentWorldCheckpointEvidenceError(
                "COMP-3 placement transition may not self-loop"
            )
        if pre_digest in outgoing or post_digest in incoming:
            raise PersistentWorldCheckpointEvidenceError(
                "COMP-3 placement history is ambiguous"
            )
        outgoing[pre_digest] = item
        incoming[post_digest] = item

    roots = [digest for digest in outgoing if digest not in incoming]
    terminals = [digest for digest in incoming if digest not in outgoing]
    final_digest = digest_persistent_world_entity_location_representation(
        final_representation
    )
    if (
        roots != [initial_digest]
        or len(terminals) != 1
        or terminals[0] != final_digest
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "COMP-3 placement history does not form the fixture-to-current chain"
        )

    representation = initial_representation
    cursor = initial_digest
    visited = set()
    while cursor in outgoing:
        if cursor in visited:
            raise PersistentWorldCheckpointEvidenceError(
                "COMP-3 placement history contains a cycle"
            )
        visited.add(cursor)
        transition = outgoing[cursor]
        receipt = transition.receipt
        try:
            if isinstance(receipt, PersistentWorldMovementCommitReceipt):
                representation = replay_persistent_world_movement(
                    pre_state_representation=representation,
                    receipt=receipt,
                )
            elif isinstance(
                receipt,
                PersistentWorldObjectCustodyCommitReceipt,
            ):
                representation = replay_persistent_world_object_custody(
                    pre_state_representation=representation,
                    receipt=receipt,
                )
            elif isinstance(
                receipt,
                PersistentWorldObjectStorageCommitReceipt,
            ):
                representation = replay_persistent_world_object_storage(
                    representation=representation,
                    receipt=receipt,
                )
            elif isinstance(
                receipt,
                PersistentWorldObjectDisplacementCommitReceipt,
            ):
                representation = replay_persistent_world_object_displacement(
                    pre_state_representation=representation,
                    receipt=receipt,
                )
            else:
                raise PersistentWorldCheckpointEvidenceError(
                    "COMP-3 placement receipt type is unsupported"
                )
        except PersistentWorldCheckpointEvidenceError:
            raise
        except Exception as exc:
            raise PersistentWorldCheckpointEvidenceError(
                "COMP-3 placement transition replay failed"
            ) from exc
        cursor = digest_persistent_world_entity_location_representation(
            representation
        )

    replay_canonical = (
        canonical_serialize_persistent_world_entity_location_representation(
            representation
        )
    )
    final_canonical = (
        canonical_serialize_persistent_world_entity_location_representation(
            final_representation
        )
    )
    if (
        len(visited) != len(transitions)
        or cursor != final_digest
        or replay_canonical != final_canonical
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "COMP-3 replayed placement differs from restored representation"
        )


def restore_persistent_world_comp3_checkpoint(
    *,
    checkpoint_path,
    expected_campaign_id,
    expected_initial_open_states,
    expected_initial_lit_states,
    expected_initial_representation,
    expected_initial_representation_digest,
):
    path = _checkpoint_path(checkpoint_path)
    expected_campaign_id = _require_record_id(
        expected_campaign_id,
        name="expected_campaign_id",
    )
    envelope = _read_checkpoint_envelope(path)
    payload = _validate_envelope_common(
        envelope=envelope,
        expected_campaign_id=expected_campaign_id,
        expected_version=COMP3_COMPONENT_CHECKPOINT_FORMAT_VERSION,
    )
    components = _require_exact_dict(
        payload["components"],
        expected_keys=COMP3_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
        name="COMP-3 checkpoint components",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    base_payload = {
        "components": {
            key: value
            for key, value in components.items()
            if key not in {"logical_time", "object_displacement"}
        }
    }
    storage_state = _restore_persistent_world_object_storage_payload(
        payload_material=_reconstruct_int3_payload(base_payload),
        expected_campaign_id=expected_campaign_id,
        expected_initial_open_states=expected_initial_open_states,
        expected_initial_lit_states=expected_initial_lit_states,
        expected_initial_representation_digest=(
            expected_initial_representation_digest
        ),
        defer_combined_attribution=True,
    )
    try:
        logical_time_state = restore_persistent_world_logical_time_state(
            components["logical_time"]
        )
    except InvalidPersistentWorldLogicalTimeRequestError as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "COMP-3 logical-time checkpoint component is invalid"
        ) from exc

    displacement_component = _require_exact_dict(
        components["object_displacement"],
        expected_keys=_DISPLACEMENT_COMPONENT_KEYS,
        name="object displacement component",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    transition_material = displacement_component[
        "committed_object_displacement_transitions"
    ]
    if type(transition_material) is not list:
        raise PersistentWorldCheckpointEvidenceError(
            "object displacement transitions must be a list"
        )
    transitions = tuple(
        _restore_object_displacement_transition(item)
        for item in transition_material
    )
    summary = _require_exact_dict(
        displacement_component["object_displacement_transition_summary"],
        expected_keys=frozenset({"count", "command_ids"}),
        name="object displacement transition summary",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    if (
        type(summary["count"]) is not int
        or summary["count"] != len(transitions)
        or summary["command_ids"]
        != sorted(item.command_id for item in transitions)
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "object displacement transition summary is inconsistent"
        )

    final_representation = (
        storage_state.lit_state.open_close_state.custody_state
        .movement_state.representation
    )
    _validate_comp3_placement_replay(
        initial_representation=expected_initial_representation,
        final_representation=final_representation,
        storage_state=storage_state,
        displacement_transitions=transitions,
        expected_initial_representation_digest=(
            expected_initial_representation_digest
        ),
    )
    return create_persistent_world_runtime_composition_from_storage_state(
        storage_state,
        logical_time_state=logical_time_state,
        committed_object_displacement_transitions=transitions,
    )
