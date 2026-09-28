"""Static componentized checkpoint format for the Myravant playable runtime.

This module changes checkpoint composition, not semantic ownership. It flattens
the already-authoritative R4-E / INT-1 / INT-2 / INT-3 checkpoint material into
five fixed components, then reconstructs the exact INT-3 payload for the
existing semantic restore validator.

There is intentionally no dynamic component registry, plugin discovery,
generic property store, reducer dispatch, or new replay authority here.
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
from astra_runtime.domain.persistent_world_object_lit_state import (
    PersistentWorldObjectLitState,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenState,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    PersistentWorldObjectStorageRuntimeState,
)


COMPONENT_CHECKPOINT_FORMAT_IDENTITY = (
    "myravant.componentized.persistent_world_checkpoint"
)
COMPONENT_CHECKPOINT_FORMAT_VERSION = 1

COMPONENT_CHECKPOINT_COMPONENT_KEYS = frozenset(
    {
        "placement",
        "custody",
        "open_close",
        "lit_state",
        "storage",
    }
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
    {
        "committed_custody_transitions",
        "custody_transition_summary",
    }
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


__all__ = [
    "COMPONENT_CHECKPOINT_FORMAT_IDENTITY",
    "COMPONENT_CHECKPOINT_FORMAT_VERSION",
    "COMPONENT_CHECKPOINT_COMPONENT_KEYS",
    "serialize_persistent_world_component_checkpoint_payload",
    "canonical_serialize_persistent_world_component_checkpoint_payload",
    "build_persistent_world_component_checkpoint_envelope",
    "canonical_serialize_persistent_world_component_checkpoint_envelope",
    "write_persistent_world_component_checkpoint",
    "restore_persistent_world_component_checkpoint",
]


def _select(
    source: Mapping[str, Any],
    keys: frozenset[str],
) -> dict[str, Any]:
    return {key: source[key] for key in keys}


def serialize_persistent_world_component_checkpoint_payload(
    state: PersistentWorldObjectStorageRuntimeState,
) -> dict[str, object]:
    """Flatten the existing validated INT-3 serialization into fixed components."""

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


def canonical_serialize_persistent_world_component_checkpoint_payload(
    state: PersistentWorldObjectStorageRuntimeState,
) -> bytes:
    return _canonical_bytes(
        serialize_persistent_world_component_checkpoint_payload(state)
    )


def build_persistent_world_component_checkpoint_envelope(
    *,
    state: PersistentWorldObjectStorageRuntimeState,
    qualification_evidence: Mapping[str, Any],
) -> dict[str, object]:
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
    *,
    state: PersistentWorldObjectStorageRuntimeState,
    qualification_evidence: Mapping[str, Any],
) -> bytes:
    return _canonical_bytes(
        build_persistent_world_component_checkpoint_envelope(
            state=state,
            qualification_evidence=qualification_evidence,
        )
    )


def write_persistent_world_component_checkpoint(
    *,
    state: PersistentWorldObjectStorageRuntimeState,
    checkpoint_path: str | os.PathLike[str],
    qualification_evidence: Mapping[str, Any],
) -> str:
    path = _checkpoint_path(checkpoint_path)
    parent = path.parent
    if not parent.exists() or not parent.is_dir():
        raise PersistentWorldCheckpointWriteError(
            "caller-supplied checkpoint parent directory does not exist"
        )

    envelope = build_persistent_world_component_checkpoint_envelope(
        state=state,
        qualification_evidence=qualification_evidence,
    )
    material = _canonical_bytes(envelope)
    temporary_path: str | None = None

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
            except FileNotFoundError:
                pass
            except OSError:
                pass
        raise PersistentWorldCheckpointWriteError(
            "component checkpoint durability operation failed"
        ) from exc

    return str(envelope["integrity_digest"])


def _reconstruct_int3_payload(
    payload_material: object,
) -> dict[str, object]:
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


def restore_persistent_world_component_checkpoint(
    *,
    checkpoint_path: str | os.PathLike[str],
    expected_campaign_id: str,
    expected_initial_open_states: tuple[PersistentWorldObjectOpenState, ...],
    expected_initial_lit_states: tuple[PersistentWorldObjectLitState, ...],
    expected_initial_representation_digest: str,
) -> PersistentWorldObjectStorageRuntimeState:
    path = _checkpoint_path(checkpoint_path)
    expected_campaign_id = _require_record_id(
        expected_campaign_id,
        name="expected_campaign_id",
    )
    envelope = _read_checkpoint_envelope(path)

    if envelope["format_identity"] != COMPONENT_CHECKPOINT_FORMAT_IDENTITY:
        raise PersistentWorldCheckpointFormatError(
            "unsupported component checkpoint format identity"
        )
    if (
        type(envelope["format_version"]) is not int
        or envelope["format_version"] != COMPONENT_CHECKPOINT_FORMAT_VERSION
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
