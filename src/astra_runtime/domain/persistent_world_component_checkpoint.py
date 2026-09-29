"""Static componentized checkpoint formats for the Myravant playable runtime.

Version 1 preserves the five-component RUNTIME-CHECKPOINT-COMPONENTIZATION-1
format. WORLD-1 adds version 2 with one typed logical-time component.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
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
    PersistentWorldObjectStorageRuntimeState,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    PersistentWorldRuntimeComposition,
    compose_persistent_world_storage_state,
    create_persistent_world_runtime_composition_from_storage_state,
)

COMPONENT_CHECKPOINT_FORMAT_IDENTITY = (
    "myravant.componentized.persistent_world_checkpoint"
)
COMPONENT_CHECKPOINT_FORMAT_VERSION = 1
WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION = 2

COMPONENT_CHECKPOINT_COMPONENT_KEYS = frozenset(
    {"placement", "custody", "open_close", "lit_state", "storage"}
)
WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS = frozenset(
    {*COMPONENT_CHECKPOINT_COMPONENT_KEYS, "logical_time"}
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
