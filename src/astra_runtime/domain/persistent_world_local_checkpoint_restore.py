"""R4-D bounded local checkpoint/restore for persistent-world movement state.

This module materializes and restores one R4-C
PersistentWorldMovementRuntimeState through a caller-supplied local path.

Authority remains with existing semantic owners. This module does not define
semantic commitment, command identity, logical time, timeline identity,
spatial semantics, version applicability, correction, canonicality, or
generalized persistence/replay infrastructure.

The initial R4-D format is deliberately local/offline and bounded.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
    PersistentWorldEntity,
    PersistentWorldEntityLocationRepresentationError,
    PersistentWorldRelation,
    create_persistent_world_entity_location_representation,
    serialize_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementCommitReceipt,
    PersistentWorldMovementCommittedTransition,
    PersistentWorldMovementRuntimeState,
    digest_persistent_world_entity_location_representation,
    serialize_persistent_world_movement_commit_receipt,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyCommitReceipt,
    PersistentWorldObjectCustodyCommittedTransition,
    PersistentWorldObjectCustodyRuntimeState,
    serialize_persistent_world_object_custody_commit_receipt,
)
from astra_runtime.kernel.record_identity import is_valid_record_id
from astra_runtime.kernel.state_delta import (
    StateDeltaEnvelope,
    StateDeltaError,
    create_state_delta_envelope,
)
from astra_runtime.kernel.transaction_preview import TransactionPreview


CHECKPOINT_FORMAT_IDENTITY = (
    "myravant.r4d.persistent_world_movement_checkpoint"
)
CHECKPOINT_FORMAT_VERSION = 1
OBJECT_CUSTODY_CHECKPOINT_FORMAT_IDENTITY = (
    "myravant.r4e.persistent_world_object_custody_checkpoint"
)
OBJECT_CUSTODY_CHECKPOINT_FORMAT_VERSION = 1
AFQR01_CHECKPOINT_OWNER = "AFQR-01"

_MOVEFILE_REPLACE_EXISTING = 0x00000001
_MOVEFILE_WRITE_THROUGH = 0x00000008

_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

_ENVELOPE_KEYS = frozenset(
    {
        "format_identity",
        "format_version",
        "campaign_identity",
        "authoritative_payload",
        "integrity_digest",
        "qualification_provenance",
    }
)

_PAYLOAD_KEYS = frozenset(
    {
        "representation",
        "representation_digest",
        "committed_transitions",
        "transition_summary",
    }
)

_REPRESENTATION_KEYS = frozenset(
    {
        "campaign_id",
        "entities",
        "relations",
    }
)

_ENTITY_KEYS = frozenset(
    {
        "entity_id",
        "classification",
    }
)

_RELATION_KEYS = frozenset(
    {
        "relation_id",
        "relation_type",
        "subject_entity_id",
        "object_entity_id",
        "semantic_owner",
    }
)

_TRANSITION_KEYS = frozenset(
    {
        "command_id",
        "command_fingerprint",
        "preview",
        "state_delta",
        "receipt",
    }
)

_PREVIEW_KEYS = frozenset(
    {
        "preview_id",
        "command_id",
        "status",
        "messages",
        "requires_confirmation",
        "metadata",
    }
)

_STATE_DELTA_KEYS = frozenset(
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

_RECEIPT_KEYS = frozenset(
    {
        "receipt_id",
        "command_id",
        "command_fingerprint",
        "actor_entity_id",
        "source_place_id",
        "destination_place_id",
        "source_relation_id",
        "destination_relation_id",
        "pre_state_digest",
        "post_state_digest",
        "preview_id",
        "state_delta_id",
        "spatial_evidence_id",
        "opportunity_evidence_id",
        "status",
    }
)

_TRANSITION_SUMMARY_KEYS = frozenset(
    {
        "count",
        "command_ids",
        "terminal_state_digest",
    }
)
_R4E_PAYLOAD_KEYS = frozenset(
    {
        "representation",
        "representation_digest",
        "committed_movement_transitions",
        "movement_transition_summary",
        "committed_custody_transitions",
        "custody_transition_summary",
    }
)

_R4E_TRANSITION_SUMMARY_KEYS = frozenset(
    {
        "count",
        "command_ids",
    }
)

_CUSTODY_RECEIPT_KEYS = frozenset(
    {
        "receipt_id",
        "command_id",
        "command_fingerprint",
        "actor_entity_id",
        "object_entity_id",
        "operation",
        "place_id",
        "source_relation_id",
        "source_relation_type",
        "destination_relation_id",
        "destination_relation_type",
        "pre_state_digest",
        "post_state_digest",
        "preview_id",
        "state_delta_id",
        "rt010_qualification_id",
        "opportunity_evidence_id",
        "status",
    }
)



class PersistentWorldCheckpointError(ValueError):
    """Base R4-D local checkpoint/restore failure."""


class InvalidPersistentWorldCheckpointRequestError(
    PersistentWorldCheckpointError
):
    """Raised when a checkpoint request has invalid bounded input."""


class PersistentWorldCheckpointQualificationError(
    PersistentWorldCheckpointError
):
    """Raised when explicit AFQR-01 qualification evidence is absent."""


class PersistentWorldCheckpointFormatError(
    PersistentWorldCheckpointError
):
    """Raised when checkpoint structure or format identity is invalid."""


class PersistentWorldCheckpointIntegrityError(
    PersistentWorldCheckpointError
):
    """Raised when authoritative checkpoint payload integrity fails."""


class PersistentWorldCheckpointCampaignMismatchError(
    PersistentWorldCheckpointError
):
    """Raised when checkpoint campaign identity does not match caller intent."""


class PersistentWorldCheckpointEvidenceError(
    PersistentWorldCheckpointError
):
    """Raised when restored bounded authoritative evidence is inconsistent."""


class PersistentWorldCheckpointUnavailableError(
    PersistentWorldCheckpointError
):
    """Raised when no accepted local checkpoint exists at the supplied path."""


class PersistentWorldCheckpointWriteError(
    PersistentWorldCheckpointError
):
    """Raised when the bounded local durability operation fails."""


__all__ = [
    "CHECKPOINT_FORMAT_IDENTITY",
    "CHECKPOINT_FORMAT_VERSION",
    "OBJECT_CUSTODY_CHECKPOINT_FORMAT_IDENTITY",
    "OBJECT_CUSTODY_CHECKPOINT_FORMAT_VERSION",
    "AFQR01_CHECKPOINT_OWNER",
    "PersistentWorldCheckpointError",
    "InvalidPersistentWorldCheckpointRequestError",
    "PersistentWorldCheckpointQualificationError",
    "PersistentWorldCheckpointFormatError",
    "PersistentWorldCheckpointIntegrityError",
    "PersistentWorldCheckpointCampaignMismatchError",
    "PersistentWorldCheckpointEvidenceError",
    "PersistentWorldCheckpointUnavailableError",
    "PersistentWorldCheckpointWriteError",
    "serialize_persistent_world_checkpoint_payload",
    "canonical_serialize_persistent_world_checkpoint_payload",
    "build_persistent_world_checkpoint_envelope",
    "canonical_serialize_persistent_world_checkpoint_envelope",
    "write_persistent_world_checkpoint",
    "restore_persistent_world_checkpoint",
    "serialize_persistent_world_object_custody_checkpoint_payload",
    "canonical_serialize_persistent_world_object_custody_checkpoint_payload",
    "build_persistent_world_object_custody_checkpoint_envelope",
    "canonical_serialize_persistent_world_object_custody_checkpoint_envelope",
    "write_persistent_world_object_custody_checkpoint",
    "restore_persistent_world_object_custody_checkpoint",
]


def _canonical_json(value: object) -> str:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise InvalidPersistentWorldCheckpointRequestError(
            "checkpoint material must be canonical JSON-compatible data"
        ) from exc


def _canonical_bytes(value: object) -> bytes:
    return _canonical_json(value).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_exact_dict(
    value: object,
    *,
    expected_keys: frozenset[str],
    name: str,
    error_cls: type[PersistentWorldCheckpointError],
) -> dict[str, Any]:
    if type(value) is not dict:
        raise error_cls(f"{name} must be a JSON object")

    keys = frozenset(value)

    if keys != expected_keys:
        raise error_cls(
            f"{name} keys must be exactly "
            f"{sorted(expected_keys)}, got {sorted(keys)}"
        )

    return value


def _require_non_empty_str(
    value: object,
    *,
    name: str,
    error_cls: type[PersistentWorldCheckpointError],
) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
    ):
        raise error_cls(f"{name} must be a non-empty trimmed string")

    return value


def _require_record_id(
    value: object,
    *,
    name: str,
) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise PersistentWorldCheckpointEvidenceError(
            f"{name} must be a valid record ID"
        )

    return value


def _require_sha256(
    value: object,
    *,
    name: str,
    error_cls: type[PersistentWorldCheckpointError],
) -> str:
    if (
        not isinstance(value, str)
        or _SHA256_PATTERN.fullmatch(value) is None
    ):
        raise error_cls(f"{name} must be a lowercase SHA-256 digest")

    return value


def _normalize_qualification(
    evidence: object,
) -> dict[str, Any]:
    if not isinstance(evidence, Mapping):
        raise PersistentWorldCheckpointQualificationError(
            "qualification_evidence must be a mapping"
        )

    material = dict(evidence)

    required = {
        "qualification_id",
        "semantic_owner",
        "qualified",
    }

    missing = required - set(material)

    if missing:
        raise PersistentWorldCheckpointQualificationError(
            "qualification_evidence is missing required keys: "
            f"{sorted(missing)}"
        )

    _require_non_empty_str(
        material["qualification_id"],
        name="qualification_id",
        error_cls=PersistentWorldCheckpointQualificationError,
    )

    if material["semantic_owner"] != AFQR01_CHECKPOINT_OWNER:
        raise PersistentWorldCheckpointQualificationError(
            "checkpoint qualification semantic_owner must be AFQR-01"
        )

    if material["qualified"] is not True:
        raise PersistentWorldCheckpointQualificationError(
            "checkpoint requires explicit qualified=true evidence"
        )

    try:
        normalized = json.loads(_canonical_json(material))
    except InvalidPersistentWorldCheckpointRequestError as exc:
        raise PersistentWorldCheckpointQualificationError(
            "qualification_evidence must be canonical JSON-compatible"
        ) from exc

    if type(normalized) is not dict:
        raise PersistentWorldCheckpointQualificationError(
            "qualification_evidence must normalize to an object"
        )

    return normalized


def _serialize_transition(
    transition: PersistentWorldMovementCommittedTransition,
) -> dict[str, object]:
    if not isinstance(
        transition,
        PersistentWorldMovementCommittedTransition,
    ):
        raise InvalidPersistentWorldCheckpointRequestError(
            "committed transition has invalid type"
        )

    if not isinstance(transition.preview, TransactionPreview):
        raise InvalidPersistentWorldCheckpointRequestError(
            "committed transition preview has invalid type"
        )

    if not isinstance(transition.state_delta, StateDeltaEnvelope):
        raise InvalidPersistentWorldCheckpointRequestError(
            "committed transition state delta has invalid type"
        )

    if not isinstance(
        transition.receipt,
        PersistentWorldMovementCommitReceipt,
    ):
        raise InvalidPersistentWorldCheckpointRequestError(
            "committed transition receipt has invalid type"
        )

    return {
        "command_id": transition.command_id,
        "command_fingerprint": transition.command_fingerprint,
        "preview": transition.preview.to_dict(),
        "state_delta": transition.state_delta.to_dict(),
        "receipt": (
            serialize_persistent_world_movement_commit_receipt(
                transition.receipt
            )
        ),
    }


def serialize_persistent_world_checkpoint_payload(
    state: PersistentWorldMovementRuntimeState,
) -> dict[str, object]:
    """Serialize only the bounded authoritative R4-C runtime state."""

    if not isinstance(state, PersistentWorldMovementRuntimeState):
        raise InvalidPersistentWorldCheckpointRequestError(
            "state must be PersistentWorldMovementRuntimeState"
        )

    if any(
        relation.relation_type != LOCATED_AT_RELATION_TYPE
        for relation in state.representation.relations
    ):
        raise InvalidPersistentWorldCheckpointRequestError(
            "R4-D checkpoint format version 1 remains movement/location-only"
        )

    representation_digest = (
        digest_persistent_world_entity_location_representation(
            state.representation
        )
    )

    transitions = [
        _serialize_transition(transition)
        for transition in state.committed_transitions
    ]

    return {
        "representation": (
            serialize_persistent_world_entity_location_representation(
                state.representation
            )
        ),
        "representation_digest": representation_digest,
        "committed_transitions": transitions,
        "transition_summary": {
            "count": len(transitions),
            "command_ids": sorted(
                transition["command_id"]
                for transition in transitions
            ),
            "terminal_state_digest": representation_digest,
        },
    }


def canonical_serialize_persistent_world_checkpoint_payload(
    state: PersistentWorldMovementRuntimeState,
) -> bytes:
    """Return canonical authoritative checkpoint payload bytes."""

    return _canonical_bytes(
        serialize_persistent_world_checkpoint_payload(state)
    )


def build_persistent_world_checkpoint_envelope(
    *,
    state: PersistentWorldMovementRuntimeState,
    qualification_evidence: Mapping[str, Any],
) -> dict[str, object]:
    """Build one bounded qualified checkpoint envelope in memory."""

    payload = serialize_persistent_world_checkpoint_payload(state)

    qualification = _normalize_qualification(
        qualification_evidence
    )

    return {
        "format_identity": CHECKPOINT_FORMAT_IDENTITY,
        "format_version": CHECKPOINT_FORMAT_VERSION,
        "campaign_identity": state.representation.campaign_id,
        "authoritative_payload": payload,
        "integrity_digest": _sha256_bytes(
            _canonical_bytes(payload)
        ),
        "qualification_provenance": qualification,
    }


def canonical_serialize_persistent_world_checkpoint_envelope(
    *,
    state: PersistentWorldMovementRuntimeState,
    qualification_evidence: Mapping[str, Any],
) -> bytes:
    return _canonical_bytes(
        build_persistent_world_checkpoint_envelope(
            state=state,
            qualification_evidence=qualification_evidence,
        )
    )


def _checkpoint_path(
    checkpoint_path: str | os.PathLike[str],
) -> Path:
    if not isinstance(checkpoint_path, (str, os.PathLike)):
        raise InvalidPersistentWorldCheckpointRequestError(
            "checkpoint_path must be a filesystem path"
        )

    raw = os.fspath(checkpoint_path)

    if not isinstance(raw, str) or not raw.strip():
        raise InvalidPersistentWorldCheckpointRequestError(
            "checkpoint_path must not be empty"
        )

    path = Path(raw)

    if path.exists() and path.is_dir():
        raise InvalidPersistentWorldCheckpointRequestError(
            "checkpoint_path must identify a file, not a directory"
        )

    return path


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY

    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY

    descriptor = os.open(path, flags)

    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _uses_windows_durability_path() -> bool:
    return os.name == "nt"


def _windows_replace_with_write_through(
    source: str | os.PathLike[str],
    destination: str | os.PathLike[str],
) -> None:
    """Replace one checkpoint through the Windows write-through move API."""

    if os.name != "nt":
        raise OSError(
            "Windows write-through replacement is unavailable "
            "on this platform"
        )

    import ctypes
    from ctypes import wintypes

    move_file_ex = ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    ).MoveFileExW

    move_file_ex.argtypes = [
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        wintypes.DWORD,
    ]
    move_file_ex.restype = wintypes.BOOL

    flags = (
        _MOVEFILE_REPLACE_EXISTING
        | _MOVEFILE_WRITE_THROUGH
    )

    source_path = os.path.abspath(
        os.fspath(source)
    )

    destination_path = os.path.abspath(
        os.fspath(destination)
    )

    succeeded = move_file_ex(
        source_path,
        destination_path,
        flags,
    )

    if succeeded:
        return

    error_code = ctypes.get_last_error()

    raise OSError(
        error_code,
        ctypes.FormatError(error_code),
        destination_path,
    )


def _replace_checkpoint_durably(
    source: Path,
    destination: Path,
) -> None:
    """Perform the platform-specific bounded durable replacement step."""

    if _uses_windows_durability_path():
        _windows_replace_with_write_through(
            source,
            destination,
        )
        return

    os.replace(
        source,
        destination,
    )

    _fsync_directory(
        destination.parent
    )


def write_persistent_world_checkpoint(
    *,
    state: PersistentWorldMovementRuntimeState,
    checkpoint_path: str | os.PathLike[str],
    qualification_evidence: Mapping[str, Any],
) -> str:
    """Durably replace one caller-selected local checkpoint.

    Success means the canonical bytes have been flushed and fsynced, then
    the platform-specific durable replacement operation has completed.
    POSIX uses same-directory replacement plus parent-directory fsync.
    Windows uses MoveFileExW with replace-existing and write-through flags.
    """

    path = _checkpoint_path(checkpoint_path)

    parent = path.parent

    if not parent.exists() or not parent.is_dir():
        raise PersistentWorldCheckpointWriteError(
            "caller-supplied checkpoint parent directory does not exist"
        )

    envelope = build_persistent_world_checkpoint_envelope(
        state=state,
        qualification_evidence=qualification_evidence,
    )

    material = _canonical_bytes(envelope)

    temporary_path: str | None = None

    try:
        descriptor, temporary_path = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".r4d-tmp",
            dir=parent,
        )

        with os.fdopen(descriptor, "wb") as handle:
            handle.write(material)
            handle.flush()
            os.fsync(handle.fileno())

        _replace_checkpoint_durably(
            Path(temporary_path),
            path,
        )

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
            "local checkpoint durability operation failed"
        ) from exc

    return str(envelope["integrity_digest"])


def _read_checkpoint_envelope(path: Path) -> dict[str, Any]:
    try:
        material = path.read_bytes()
    except FileNotFoundError as exc:
        raise PersistentWorldCheckpointUnavailableError(
            "no accepted checkpoint exists at the supplied path"
        ) from exc
    except OSError as exc:
        raise PersistentWorldCheckpointUnavailableError(
            "checkpoint bytes could not be read"
        ) from exc

    if not material:
        raise PersistentWorldCheckpointFormatError(
            "checkpoint file is empty"
        )

    try:
        text = material.decode("utf-8")
        envelope = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PersistentWorldCheckpointFormatError(
            "checkpoint is not valid UTF-8 canonical JSON"
        ) from exc

    envelope = _require_exact_dict(
        envelope,
        expected_keys=_ENVELOPE_KEYS,
        name="checkpoint envelope",
        error_cls=PersistentWorldCheckpointFormatError,
    )

    if material != _canonical_bytes(envelope):
        raise PersistentWorldCheckpointFormatError(
            "checkpoint envelope is not in canonical serialized form"
        )

    return envelope


def _restore_representation(
    material: object,
    *,
    expected_campaign_id: str,
) -> object:
    representation = _require_exact_dict(
        material,
        expected_keys=_REPRESENTATION_KEYS,
        name="authoritative representation",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    campaign_id = _require_record_id(
        representation["campaign_id"],
        name="representation campaign_id",
    )

    if campaign_id != expected_campaign_id:
        raise PersistentWorldCheckpointCampaignMismatchError(
            "representation campaign identity differs from checkpoint"
        )

    entities_material = representation["entities"]
    relations_material = representation["relations"]

    if type(entities_material) is not list:
        raise PersistentWorldCheckpointEvidenceError(
            "representation entities must be a list"
        )

    if type(relations_material) is not list:
        raise PersistentWorldCheckpointEvidenceError(
            "representation relations must be a list"
        )

    entities = []

    for index, item in enumerate(entities_material):
        item = _require_exact_dict(
            item,
            expected_keys=_ENTITY_KEYS,
            name=f"entities[{index}]",
            error_cls=PersistentWorldCheckpointEvidenceError,
        )

        entity_id = _require_record_id(
            item["entity_id"],
            name=f"entities[{index}].entity_id",
        )

        classification = _require_non_empty_str(
            item["classification"],
            name=f"entities[{index}].classification",
            error_cls=PersistentWorldCheckpointEvidenceError,
        )

        try:
            entities.append(
                PersistentWorldEntity(
                    entity_id=entity_id,
                    classification=classification,
                )
            )
        except PersistentWorldEntityLocationRepresentationError as exc:
            raise PersistentWorldCheckpointEvidenceError(
                "checkpoint entity representation is invalid"
            ) from exc

    relations = []

    for index, item in enumerate(relations_material):
        item = _require_exact_dict(
            item,
            expected_keys=_RELATION_KEYS,
            name=f"relations[{index}]",
            error_cls=PersistentWorldCheckpointEvidenceError,
        )

        values = {
            name: _require_non_empty_str(
                item[name],
                name=f"relations[{index}].{name}",
                error_cls=PersistentWorldCheckpointEvidenceError,
            )
            for name in _RELATION_KEYS
        }

        for record_field in (
            "relation_id",
            "subject_entity_id",
            "object_entity_id",
        ):
            _require_record_id(
                values[record_field],
                name=f"relations[{index}].{record_field}",
            )

        try:
            relations.append(
                PersistentWorldRelation(
                    relation_id=values["relation_id"],
                    relation_type=values["relation_type"],
                    subject_entity_id=values[
                        "subject_entity_id"
                    ],
                    object_entity_id=values[
                        "object_entity_id"
                    ],
                    semantic_owner=values["semantic_owner"],
                )
            )
        except PersistentWorldEntityLocationRepresentationError as exc:
            raise PersistentWorldCheckpointEvidenceError(
                "checkpoint relation representation is invalid"
            ) from exc

    try:
        return create_persistent_world_entity_location_representation(
            campaign_id=campaign_id,
            entities=entities,
            relations=relations,
        )
    except PersistentWorldEntityLocationRepresentationError as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "checkpoint entity/location representation is invalid"
        ) from exc


def _restore_preview(material: object) -> TransactionPreview:
    preview = _require_exact_dict(
        material,
        expected_keys=_PREVIEW_KEYS,
        name="movement preview",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    preview_id = _require_record_id(
        preview["preview_id"],
        name="preview.preview_id",
    )

    command_id = _require_non_empty_str(
        preview["command_id"],
        name="preview.command_id",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    if preview["status"] != "preview_created":
        raise PersistentWorldCheckpointEvidenceError(
            "restored movement preview must remain preview_created"
        )

    if preview["messages"] != [
        "bounded persistent-world movement prepared"
    ]:
        raise PersistentWorldCheckpointEvidenceError(
            "restored movement preview messages differ from R4-C evidence"
        )

    if preview["requires_confirmation"] is not False:
        raise PersistentWorldCheckpointEvidenceError(
            "restored R4-C movement preview unexpectedly requires confirmation"
        )

    expected_metadata = {
        "package": "R4-C",
        "movement_family": "movement",
        "mutation_performed": False,
    }

    if preview["metadata"] != expected_metadata:
        raise PersistentWorldCheckpointEvidenceError(
            "restored movement preview metadata is inconsistent"
        )

    return TransactionPreview(
        preview_id=preview_id,
        command_id=command_id,
        status="preview_created",
        messages=(
            "bounded persistent-world movement prepared",
        ),
        requires_confirmation=False,
        metadata=MappingProxyType(
            dict(expected_metadata)
        ),
    )


def _restore_state_delta(
    material: object,
) -> StateDeltaEnvelope:
    delta = _require_exact_dict(
        material,
        expected_keys=_STATE_DELTA_KEYS,
        name="movement state delta",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    affected = delta["affected_record_ids"]

    if type(affected) is not list:
        raise PersistentWorldCheckpointEvidenceError(
            "state_delta.affected_record_ids must be a list"
        )

    if type(delta["payload"]) is not dict:
        raise PersistentWorldCheckpointEvidenceError(
            "state_delta.payload must be an object"
        )

    if type(delta["metadata"]) is not dict:
        raise PersistentWorldCheckpointEvidenceError(
            "state_delta.metadata must be an object"
        )

    try:
        return create_state_delta_envelope(
            delta_id=delta["delta_id"],
            source_command_id=delta["source_command_id"],
            source_preview_id=delta["source_preview_id"],
            affected_record_ids=affected,
            change_type=delta["change_type"],
            payload=delta["payload"],
            metadata=delta["metadata"],
        )
    except (StateDeltaError, TypeError) as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "restored movement state delta is invalid"
        ) from exc


def _restore_receipt(
    material: object,
) -> PersistentWorldMovementCommitReceipt:
    receipt = _require_exact_dict(
        material,
        expected_keys=_RECEIPT_KEYS,
        name="movement receipt",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    command_id = _require_non_empty_str(
        receipt["command_id"],
        name="receipt.command_id",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    command_fingerprint = _require_sha256(
        receipt["command_fingerprint"],
        name="receipt.command_fingerprint",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    pre_state_digest = _require_sha256(
        receipt["pre_state_digest"],
        name="receipt.pre_state_digest",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    post_state_digest = _require_sha256(
        receipt["post_state_digest"],
        name="receipt.post_state_digest",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    record_fields = (
        "receipt_id",
        "actor_entity_id",
        "source_place_id",
        "destination_place_id",
        "source_relation_id",
        "destination_relation_id",
        "preview_id",
        "state_delta_id",
        "spatial_evidence_id",
        "opportunity_evidence_id",
    )

    normalized = {}

    for field in record_fields:
        normalized[field] = _require_record_id(
            receipt[field],
            name=f"receipt.{field}",
        )

    if receipt["status"] != "committed":
        raise PersistentWorldCheckpointEvidenceError(
            "movement receipt status must remain committed"
        )

    return PersistentWorldMovementCommitReceipt(
        receipt_id=normalized["receipt_id"],
        command_id=command_id,
        command_fingerprint=command_fingerprint,
        actor_entity_id=normalized["actor_entity_id"],
        source_place_id=normalized["source_place_id"],
        destination_place_id=normalized[
            "destination_place_id"
        ],
        source_relation_id=normalized[
            "source_relation_id"
        ],
        destination_relation_id=normalized[
            "destination_relation_id"
        ],
        pre_state_digest=pre_state_digest,
        post_state_digest=post_state_digest,
        preview_id=normalized["preview_id"],
        state_delta_id=normalized["state_delta_id"],
        spatial_evidence_id=normalized[
            "spatial_evidence_id"
        ],
        opportunity_evidence_id=normalized[
            "opportunity_evidence_id"
        ],
        status="committed",
    )


def _restore_transition(
    material: object,
) -> PersistentWorldMovementCommittedTransition:
    transition = _require_exact_dict(
        material,
        expected_keys=_TRANSITION_KEYS,
        name="committed movement transition",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    command_id = _require_non_empty_str(
        transition["command_id"],
        name="transition.command_id",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    command_fingerprint = _require_sha256(
        transition["command_fingerprint"],
        name="transition.command_fingerprint",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    preview = _restore_preview(
        transition["preview"]
    )

    state_delta = _restore_state_delta(
        transition["state_delta"]
    )

    receipt = _restore_receipt(
        transition["receipt"]
    )

    if preview.command_id != command_id:
        raise PersistentWorldCheckpointEvidenceError(
            "preview command identity disagrees with transition"
        )

    if state_delta.source_command_id != command_id:
        raise PersistentWorldCheckpointEvidenceError(
            "state delta command identity disagrees with transition"
        )

    if receipt.command_id != command_id:
        raise PersistentWorldCheckpointEvidenceError(
            "receipt command identity disagrees with transition"
        )

    if receipt.command_fingerprint != command_fingerprint:
        raise PersistentWorldCheckpointEvidenceError(
            "receipt command fingerprint disagrees with transition"
        )

    if state_delta.source_preview_id != preview.preview_id:
        raise PersistentWorldCheckpointEvidenceError(
            "state delta preview identity disagrees with preview"
        )

    if receipt.preview_id != preview.preview_id:
        raise PersistentWorldCheckpointEvidenceError(
            "receipt preview identity disagrees with preview"
        )

    if receipt.state_delta_id != state_delta.delta_id:
        raise PersistentWorldCheckpointEvidenceError(
            "receipt state-delta identity disagrees with delta"
        )

    if state_delta.change_type != "relationship_update":
        raise PersistentWorldCheckpointEvidenceError(
            "R4-C movement state delta must remain relationship_update"
        )

    expected_affected = (
        receipt.actor_entity_id,
        receipt.source_place_id,
        receipt.destination_place_id,
        receipt.source_relation_id,
        receipt.destination_relation_id,
    )

    if state_delta.affected_record_ids != expected_affected:
        raise PersistentWorldCheckpointEvidenceError(
            "movement receipt and affected-record evidence disagree"
        )

    expected_payload = {
        "relation_type": LOCATED_AT_RELATION_TYPE,
        "subject_entity_id": receipt.actor_entity_id,
        "from_place_id": receipt.source_place_id,
        "to_place_id": receipt.destination_place_id,
        "source_relation_id": receipt.source_relation_id,
        "destination_relation_id": (
            receipt.destination_relation_id
        ),
    }

    if dict(state_delta.payload) != expected_payload:
        raise PersistentWorldCheckpointEvidenceError(
            "movement receipt and state-delta payload disagree"
        )

    expected_metadata = {
        "package": "R4-C",
        "semantic_owner": "AFQR-18",
        "qualified_transition_owner": "AFQR-01",
    }

    if dict(state_delta.metadata) != expected_metadata:
        raise PersistentWorldCheckpointEvidenceError(
            "movement state-delta owner metadata is inconsistent"
        )

    return PersistentWorldMovementCommittedTransition(
        command_id=command_id,
        command_fingerprint=command_fingerprint,
        preview=preview,
        state_delta=state_delta,
        receipt=receipt,
    )


def _validate_restored_state_attribution(
    state: PersistentWorldMovementRuntimeState,
) -> None:
    representation = state.representation

    entities = {
        entity.entity_id: entity
        for entity in representation.entities
    }

    for transition in state.committed_transitions:
        receipt = transition.receipt

        for entity_id in (
            receipt.actor_entity_id,
            receipt.source_place_id,
            receipt.destination_place_id,
        ):
            if entity_id not in entities:
                raise PersistentWorldCheckpointEvidenceError(
                    "committed transition references an absent entity"
                )

        if entities[receipt.source_place_id].classification != "place":
            raise PersistentWorldCheckpointEvidenceError(
                "committed movement source no longer identifies a place"
            )

        if (
            entities[
                receipt.destination_place_id
            ].classification
            != "place"
        ):
            raise PersistentWorldCheckpointEvidenceError(
                "committed movement destination no longer identifies a place"
            )

    if not state.committed_transitions:
        return

    terminal_digest = (
        digest_persistent_world_entity_location_representation(
            representation
        )
    )

    terminal_matches = [
        transition
        for transition in state.committed_transitions
        if transition.receipt.post_state_digest
        == terminal_digest
    ]

    if len(terminal_matches) != 1:
        raise PersistentWorldCheckpointEvidenceError(
            "current authoritative representation is not attributable "
            "to exactly one preserved committed movement result"
        )

    terminal = terminal_matches[0].receipt

    actor_relations = [
        relation
        for relation in representation.relations
        if (
            relation.relation_type
            == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id
            == terminal.actor_entity_id
        )
    ]

    if len(actor_relations) != 1:
        raise PersistentWorldCheckpointEvidenceError(
            "terminal movement actor must have exactly one current location"
        )

    current = actor_relations[0]

    if (
        current.object_entity_id
        != terminal.destination_place_id
        or current.relation_id
        != terminal.destination_relation_id
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "current authoritative location disagrees with terminal "
            "committed movement evidence"
        )


def _restore_payload(
    material: object,
    *,
    expected_campaign_id: str,
) -> PersistentWorldMovementRuntimeState:
    payload = _require_exact_dict(
        material,
        expected_keys=_PAYLOAD_KEYS,
        name="authoritative payload",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    representation_digest = _require_sha256(
        payload["representation_digest"],
        name="representation_digest",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    representation = _restore_representation(
        payload["representation"],
        expected_campaign_id=expected_campaign_id,
    )

    if any(
        relation.relation_type != LOCATED_AT_RELATION_TYPE
        for relation in representation.relations
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "R4-D checkpoint format version 1 remains movement/location-only"
        )

    actual_representation_digest = (
        digest_persistent_world_entity_location_representation(
            representation
        )
    )

    if (
        actual_representation_digest
        != representation_digest
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "representation digest disagrees with restored R4-B state"
        )

    transitions_material = payload[
        "committed_transitions"
    ]

    if type(transitions_material) is not list:
        raise PersistentWorldCheckpointEvidenceError(
            "committed_transitions must be a list"
        )

    transitions = tuple(
        _restore_transition(item)
        for item in transitions_material
    )

    summary = _require_exact_dict(
        payload["transition_summary"],
        expected_keys=_TRANSITION_SUMMARY_KEYS,
        name="transition_summary",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )

    if type(summary["count"]) is not int:
        raise PersistentWorldCheckpointEvidenceError(
            "transition_summary.count must be an integer"
        )

    if summary["count"] != len(transitions):
        raise PersistentWorldCheckpointEvidenceError(
            "transition summary count disagrees with preserved evidence"
        )

    expected_command_ids = sorted(
        transition.command_id
        for transition in transitions
    )

    if summary["command_ids"] != expected_command_ids:
        raise PersistentWorldCheckpointEvidenceError(
            "transition summary command identities disagree with evidence"
        )

    if (
        summary["terminal_state_digest"]
        != actual_representation_digest
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "transition summary terminal digest disagrees with current state"
        )

    try:
        state = PersistentWorldMovementRuntimeState(
            representation=representation,
            committed_transitions=transitions,
        )
    except Exception as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "restored R4-C runtime state is invalid"
        ) from exc

    _validate_restored_state_attribution(state)

    return state


def restore_persistent_world_checkpoint(
    *,
    checkpoint_path: str | os.PathLike[str],
    expected_campaign_id: str,
) -> PersistentWorldMovementRuntimeState:
    """Restore exactly one accepted bounded R4-D local checkpoint."""

    path = _checkpoint_path(checkpoint_path)

    expected_campaign_id = _require_record_id(
        expected_campaign_id,
        name="expected_campaign_id",
    )

    envelope = _read_checkpoint_envelope(path)

    if (
        envelope["format_identity"]
        != CHECKPOINT_FORMAT_IDENTITY
    ):
        raise PersistentWorldCheckpointFormatError(
            "unsupported checkpoint format identity"
        )

    if (
        type(envelope["format_version"]) is not int
        or envelope["format_version"]
        != CHECKPOINT_FORMAT_VERSION
    ):
        raise PersistentWorldCheckpointFormatError(
            "unsupported checkpoint format version"
        )

    campaign_identity = _require_record_id(
        envelope["campaign_identity"],
        name="checkpoint campaign_identity",
    )

    if campaign_identity != expected_campaign_id:
        raise PersistentWorldCheckpointCampaignMismatchError(
            "checkpoint campaign identity does not match caller expectation"
        )

    _normalize_qualification(
        envelope["qualification_provenance"]
    )

    payload = envelope["authoritative_payload"]

    integrity_digest = _require_sha256(
        envelope["integrity_digest"],
        name="integrity_digest",
        error_cls=PersistentWorldCheckpointIntegrityError,
    )

    actual_integrity = _sha256_bytes(
        _canonical_bytes(payload)
    )

    if actual_integrity != integrity_digest:
        raise PersistentWorldCheckpointIntegrityError(
            "checkpoint authoritative payload integrity mismatch"
        )

    return _restore_payload(
        payload,
        expected_campaign_id=expected_campaign_id,
    )

def _serialize_custody_transition(
    transition: PersistentWorldObjectCustodyCommittedTransition,
) -> dict[str, object]:
    if not isinstance(
        transition,
        PersistentWorldObjectCustodyCommittedTransition,
    ):
        raise InvalidPersistentWorldCheckpointRequestError(
            "custody transition has invalid type"
        )
    if not isinstance(transition.preview, TransactionPreview):
        raise InvalidPersistentWorldCheckpointRequestError(
            "custody transition preview has invalid type"
        )
    if not isinstance(transition.state_delta, StateDeltaEnvelope):
        raise InvalidPersistentWorldCheckpointRequestError(
            "custody transition state delta has invalid type"
        )
    if not isinstance(
        transition.receipt,
        PersistentWorldObjectCustodyCommitReceipt,
    ):
        raise InvalidPersistentWorldCheckpointRequestError(
            "custody transition receipt has invalid type"
        )
    return {
        "command_id": transition.command_id,
        "command_fingerprint": transition.command_fingerprint,
        "preview": transition.preview.to_dict(),
        "state_delta": transition.state_delta.to_dict(),
        "receipt": serialize_persistent_world_object_custody_commit_receipt(
            transition.receipt
        ),
    }


def serialize_persistent_world_object_custody_checkpoint_payload(
    state: PersistentWorldObjectCustodyRuntimeState,
) -> dict[str, object]:
    """Serialize one bounded R4-E composed movement/custody state."""
    if not isinstance(state, PersistentWorldObjectCustodyRuntimeState):
        raise InvalidPersistentWorldCheckpointRequestError(
            "state must be PersistentWorldObjectCustodyRuntimeState"
        )
    representation = state.movement_state.representation
    representation_digest = (
        digest_persistent_world_entity_location_representation(representation)
    )
    movement = [
        _serialize_transition(item)
        for item in state.movement_state.committed_transitions
    ]
    custody = [
        _serialize_custody_transition(item)
        for item in state.committed_custody_transitions
    ]
    return {
        "representation": (
            serialize_persistent_world_entity_location_representation(
                representation
            )
        ),
        "representation_digest": representation_digest,
        "committed_movement_transitions": movement,
        "movement_transition_summary": {
            "count": len(movement),
            "command_ids": sorted(item["command_id"] for item in movement),
        },
        "committed_custody_transitions": custody,
        "custody_transition_summary": {
            "count": len(custody),
            "command_ids": sorted(item["command_id"] for item in custody),
        },
    }


def canonical_serialize_persistent_world_object_custody_checkpoint_payload(
    state: PersistentWorldObjectCustodyRuntimeState,
) -> bytes:
    return _canonical_bytes(
        serialize_persistent_world_object_custody_checkpoint_payload(state)
    )


def build_persistent_world_object_custody_checkpoint_envelope(
    *,
    state: PersistentWorldObjectCustodyRuntimeState,
    qualification_evidence: Mapping[str, Any],
) -> dict[str, object]:
    payload = serialize_persistent_world_object_custody_checkpoint_payload(
        state
    )
    qualification = _normalize_qualification(qualification_evidence)
    return {
        "format_identity": OBJECT_CUSTODY_CHECKPOINT_FORMAT_IDENTITY,
        "format_version": OBJECT_CUSTODY_CHECKPOINT_FORMAT_VERSION,
        "campaign_identity": state.movement_state.representation.campaign_id,
        "authoritative_payload": payload,
        "integrity_digest": _sha256_bytes(_canonical_bytes(payload)),
        "qualification_provenance": qualification,
    }


def canonical_serialize_persistent_world_object_custody_checkpoint_envelope(
    *,
    state: PersistentWorldObjectCustodyRuntimeState,
    qualification_evidence: Mapping[str, Any],
) -> bytes:
    return _canonical_bytes(
        build_persistent_world_object_custody_checkpoint_envelope(
            state=state,
            qualification_evidence=qualification_evidence,
        )
    )


def write_persistent_world_object_custody_checkpoint(
    *,
    state: PersistentWorldObjectCustodyRuntimeState,
    checkpoint_path: str | os.PathLike[str],
    qualification_evidence: Mapping[str, Any],
) -> str:
    """Durably replace one caller-selected bounded R4-E checkpoint."""
    path = _checkpoint_path(checkpoint_path)
    parent = path.parent
    if not parent.exists() or not parent.is_dir():
        raise PersistentWorldCheckpointWriteError(
            "caller-supplied checkpoint parent directory does not exist"
        )
    envelope = build_persistent_world_object_custody_checkpoint_envelope(
        state=state,
        qualification_evidence=qualification_evidence,
    )
    material = _canonical_bytes(envelope)
    temporary_path: str | None = None
    try:
        descriptor, temporary_path = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".r4e-tmp",
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
            "local R4-E checkpoint durability operation failed"
        ) from exc
    return str(envelope["integrity_digest"])


def _restore_custody_preview(material: object) -> TransactionPreview:
    preview = _require_exact_dict(
        material,
        expected_keys=_PREVIEW_KEYS,
        name="custody preview",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    preview_id = _require_record_id(
        preview["preview_id"],
        name="custody preview.preview_id",
    )
    command_id = _require_non_empty_str(
        preview["command_id"],
        name="custody preview.command_id",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    expected_metadata = {
        "package": "R4-E",
        "command_family": "inventory",
        "mutation_performed": False,
    }
    if preview["status"] != "preview_created":
        raise PersistentWorldCheckpointEvidenceError(
            "custody preview must remain preview_created"
        )
    if preview["messages"] != [
        "bounded persistent-world object custody prepared"
    ]:
        raise PersistentWorldCheckpointEvidenceError(
            "custody preview messages are inconsistent"
        )
    if preview["requires_confirmation"] is not False:
        raise PersistentWorldCheckpointEvidenceError(
            "custody preview unexpectedly requires confirmation"
        )
    if preview["metadata"] != expected_metadata:
        raise PersistentWorldCheckpointEvidenceError(
            "custody preview metadata is inconsistent"
        )
    return TransactionPreview(
        preview_id=preview_id,
        command_id=command_id,
        status="preview_created",
        messages=("bounded persistent-world object custody prepared",),
        requires_confirmation=False,
        metadata=MappingProxyType(dict(expected_metadata)),
    )


def _restore_custody_receipt(
    material: object,
) -> PersistentWorldObjectCustodyCommitReceipt:
    receipt = _require_exact_dict(
        material,
        expected_keys=_CUSTODY_RECEIPT_KEYS,
        name="custody receipt",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    command_id = _require_non_empty_str(
        receipt["command_id"],
        name="custody receipt.command_id",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    fingerprint = _require_sha256(
        receipt["command_fingerprint"],
        name="custody receipt.command_fingerprint",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    pre_digest = _require_sha256(
        receipt["pre_state_digest"],
        name="custody receipt.pre_state_digest",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    post_digest = _require_sha256(
        receipt["post_state_digest"],
        name="custody receipt.post_state_digest",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    record_fields = (
        "receipt_id",
        "actor_entity_id",
        "object_entity_id",
        "place_id",
        "source_relation_id",
        "destination_relation_id",
        "preview_id",
        "state_delta_id",
        "rt010_qualification_id",
        "opportunity_evidence_id",
    )
    ids = {
        field: _require_record_id(
            receipt[field],
            name=f"custody receipt.{field}",
        )
        for field in record_fields
    }
    try:
        return PersistentWorldObjectCustodyCommitReceipt(
            receipt_id=ids["receipt_id"],
            command_id=command_id,
            command_fingerprint=fingerprint,
            actor_entity_id=ids["actor_entity_id"],
            object_entity_id=ids["object_entity_id"],
            operation=receipt["operation"],
            place_id=ids["place_id"],
            source_relation_id=ids["source_relation_id"],
            source_relation_type=receipt["source_relation_type"],
            destination_relation_id=ids["destination_relation_id"],
            destination_relation_type=receipt["destination_relation_type"],
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
            preview_id=ids["preview_id"],
            state_delta_id=ids["state_delta_id"],
            rt010_qualification_id=ids["rt010_qualification_id"],
            opportunity_evidence_id=ids["opportunity_evidence_id"],
            status=receipt["status"],
        )
    except Exception as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "custody receipt is invalid"
        ) from exc


def _restore_custody_transition(
    material: object,
) -> PersistentWorldObjectCustodyCommittedTransition:
    transition = _require_exact_dict(
        material,
        expected_keys=_TRANSITION_KEYS,
        name="committed custody transition",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    command_id = _require_non_empty_str(
        transition["command_id"],
        name="custody transition.command_id",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    fingerprint = _require_sha256(
        transition["command_fingerprint"],
        name="custody transition.command_fingerprint",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    preview = _restore_custody_preview(transition["preview"])
    delta = _restore_state_delta(transition["state_delta"])
    receipt = _restore_custody_receipt(transition["receipt"])
    if preview.command_id != command_id:
        raise PersistentWorldCheckpointEvidenceError(
            "custody preview command identity disagrees with transition"
        )
    if delta.source_command_id != command_id:
        raise PersistentWorldCheckpointEvidenceError(
            "custody state delta command identity disagrees with transition"
        )
    if receipt.command_id != command_id:
        raise PersistentWorldCheckpointEvidenceError(
            "custody receipt command identity disagrees with transition"
        )
    if receipt.command_fingerprint != fingerprint:
        raise PersistentWorldCheckpointEvidenceError(
            "custody receipt fingerprint disagrees with transition"
        )
    if delta.source_preview_id != preview.preview_id:
        raise PersistentWorldCheckpointEvidenceError(
            "custody state delta preview identity disagrees with preview"
        )
    if receipt.preview_id != preview.preview_id:
        raise PersistentWorldCheckpointEvidenceError(
            "custody receipt preview identity disagrees with preview"
        )
    if receipt.state_delta_id != delta.delta_id:
        raise PersistentWorldCheckpointEvidenceError(
            "custody receipt state-delta identity disagrees with delta"
        )
    expected_affected = (
        receipt.actor_entity_id,
        receipt.object_entity_id,
        receipt.place_id,
        receipt.source_relation_id,
        receipt.destination_relation_id,
    )
    if delta.affected_record_ids != expected_affected:
        raise PersistentWorldCheckpointEvidenceError(
            "custody affected-record evidence disagrees with receipt"
        )
    expected_payload = {
        "operation": receipt.operation,
        "actor_entity_id": receipt.actor_entity_id,
        "object_entity_id": receipt.object_entity_id,
        "place_id": receipt.place_id,
        "source_relation_id": receipt.source_relation_id,
        "source_relation_type": receipt.source_relation_type,
        "destination_relation_id": receipt.destination_relation_id,
        "destination_relation_type": receipt.destination_relation_type,
    }
    if dict(delta.payload) != expected_payload:
        raise PersistentWorldCheckpointEvidenceError(
            "custody state-delta payload disagrees with receipt"
        )
    expected_metadata = {
        "package": "R4-E",
        "custody_semantic_owner": "RT-010",
        "direct_location_semantic_owner": "AFQR-18",
        "opportunity_semantic_owner": "AFQR-19",
        "qualified_transition_owner": "AFQR-01",
    }
    if dict(delta.metadata) != expected_metadata:
        raise PersistentWorldCheckpointEvidenceError(
            "custody state-delta owner metadata is inconsistent"
        )
    if delta.change_type != "relationship_update":
        raise PersistentWorldCheckpointEvidenceError(
            "custody state delta must remain relationship_update"
        )
    return PersistentWorldObjectCustodyCommittedTransition(
        command_id=command_id,
        command_fingerprint=fingerprint,
        preview=preview,
        state_delta=delta,
        receipt=receipt,
    )


def _restore_r4e_summary(
    material: object,
    *,
    transitions: tuple[object, ...],
    name: str,
) -> None:
    summary = _require_exact_dict(
        material,
        expected_keys=_R4E_TRANSITION_SUMMARY_KEYS,
        name=name,
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    if type(summary["count"]) is not int:
        raise PersistentWorldCheckpointEvidenceError(
            f"{name}.count must be integer"
        )
    if summary["count"] != len(transitions):
        raise PersistentWorldCheckpointEvidenceError(
            f"{name}.count disagrees with evidence"
        )
    if summary["command_ids"] != sorted(item.command_id for item in transitions):
        raise PersistentWorldCheckpointEvidenceError(
            f"{name}.command_ids disagree with evidence"
        )


def _validate_r4e_restored_attribution(
    state: PersistentWorldObjectCustodyRuntimeState,
) -> None:
    representation = state.movement_state.representation
    entities = {
        entity.entity_id: entity
        for entity in representation.entities
    }
    movement = state.movement_state.committed_transitions
    custody = state.committed_custody_transitions
    all_ids = [item.command_id for item in movement] + [
        item.command_id for item in custody
    ]
    if len(all_ids) != len(set(all_ids)):
        raise PersistentWorldCheckpointEvidenceError(
            "movement/custody command identities collide"
        )
    for transition in movement:
        receipt = transition.receipt
        for entity_id in (
            receipt.actor_entity_id,
            receipt.source_place_id,
            receipt.destination_place_id,
        ):
            if entity_id not in entities:
                raise PersistentWorldCheckpointEvidenceError(
                    "movement evidence references an absent entity"
                )
        if entities[receipt.source_place_id].classification != "place":
            raise PersistentWorldCheckpointEvidenceError(
                "movement source evidence no longer identifies a place"
            )
        if entities[receipt.destination_place_id].classification != "place":
            raise PersistentWorldCheckpointEvidenceError(
                "movement destination evidence no longer identifies a place"
            )
    for transition in custody:
        receipt = transition.receipt
        actor = entities.get(receipt.actor_entity_id)
        target = entities.get(receipt.object_entity_id)
        place = entities.get(receipt.place_id)
        if actor is None or actor.classification != "character_or_creature":
            raise PersistentWorldCheckpointEvidenceError(
                "custody evidence actor is absent or ineligible"
            )
        if target is None or target.classification != "object":
            raise PersistentWorldCheckpointEvidenceError(
                "custody evidence object is absent or ineligible"
            )
        if place is None or place.classification != "place":
            raise PersistentWorldCheckpointEvidenceError(
                "custody evidence place is absent or ineligible"
            )
    transitions = [*movement, *custody]
    if not transitions:
        return
    digest = digest_persistent_world_entity_location_representation(
        representation
    )
    terminal = [
        item
        for item in transitions
        if item.receipt.post_state_digest == digest
    ]
    if len(terminal) != 1:
        raise PersistentWorldCheckpointEvidenceError(
            "current R4-E representation is not attributable to exactly one "
            "preserved committed transition"
        )
    receipt = terminal[0].receipt
    if isinstance(receipt, PersistentWorldObjectCustodyCommitReceipt):
        destination = [
            relation
            for relation in representation.relations
            if relation.relation_id == receipt.destination_relation_id
        ]
        if len(destination) != 1:
            raise PersistentWorldCheckpointEvidenceError(
                "terminal custody destination relation is absent"
            )
        relation = destination[0]
        if (
            relation.relation_type != receipt.destination_relation_type
            or relation.subject_entity_id != receipt.object_entity_id
        ):
            raise PersistentWorldCheckpointEvidenceError(
                "terminal custody relation disagrees with receipt"
            )
        expected_target = (
            receipt.actor_entity_id
            if receipt.operation == "pickup"
            else receipt.place_id
        )
        if relation.object_entity_id != expected_target:
            raise PersistentWorldCheckpointEvidenceError(
                "terminal custody destination disagrees with receipt target"
            )
    else:
        actor_locations = [
            relation
            for relation in representation.relations
            if relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == receipt.actor_entity_id
        ]
        if len(actor_locations) != 1:
            raise PersistentWorldCheckpointEvidenceError(
                "terminal movement actor must have one current location"
            )
        current = actor_locations[0]
        if (
            current.relation_id != receipt.destination_relation_id
            or current.object_entity_id != receipt.destination_place_id
        ):
            raise PersistentWorldCheckpointEvidenceError(
                "terminal movement relation disagrees with receipt"
            )


def _restore_r4e_payload(
    material: object,
    *,
    expected_campaign_id: str,
) -> PersistentWorldObjectCustodyRuntimeState:
    payload = _require_exact_dict(
        material,
        expected_keys=_R4E_PAYLOAD_KEYS,
        name="R4-E authoritative payload",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    expected_digest = _require_sha256(
        payload["representation_digest"],
        name="R4-E representation_digest",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    representation = _restore_representation(
        payload["representation"],
        expected_campaign_id=expected_campaign_id,
    )
    actual_digest = digest_persistent_world_entity_location_representation(
        representation
    )
    if actual_digest != expected_digest:
        raise PersistentWorldCheckpointEvidenceError(
            "R4-E representation digest disagrees with restored state"
        )
    movement_material = payload["committed_movement_transitions"]
    custody_material = payload["committed_custody_transitions"]
    if (
        type(movement_material) is not list
        or type(custody_material) is not list
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "R4-E committed transition collections must be lists"
        )
    movement = tuple(
        _restore_transition(item)
        for item in movement_material
    )
    custody = tuple(
        _restore_custody_transition(item)
        for item in custody_material
    )
    _restore_r4e_summary(
        payload["movement_transition_summary"],
        transitions=movement,
        name="movement_transition_summary",
    )
    _restore_r4e_summary(
        payload["custody_transition_summary"],
        transitions=custody,
        name="custody_transition_summary",
    )
    try:
        movement_state = PersistentWorldMovementRuntimeState(
            representation=representation,
            committed_transitions=movement,
        )
        state = PersistentWorldObjectCustodyRuntimeState(
            movement_state=movement_state,
            committed_custody_transitions=custody,
        )
    except Exception as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "restored R4-E runtime state is invalid"
        ) from exc
    _validate_r4e_restored_attribution(state)
    return state


def restore_persistent_world_object_custody_checkpoint(
    *,
    checkpoint_path: str | os.PathLike[str],
    expected_campaign_id: str,
) -> PersistentWorldObjectCustodyRuntimeState:
    """Restore exactly one accepted bounded R4-E local checkpoint."""
    path = _checkpoint_path(checkpoint_path)
    expected_campaign_id = _require_record_id(
        expected_campaign_id,
        name="expected_campaign_id",
    )
    envelope = _read_checkpoint_envelope(path)
    if (
        envelope["format_identity"]
        != OBJECT_CUSTODY_CHECKPOINT_FORMAT_IDENTITY
    ):
        raise PersistentWorldCheckpointFormatError(
            "unsupported R4-E checkpoint format identity"
        )
    if (
        type(envelope["format_version"]) is not int
        or envelope["format_version"]
        != OBJECT_CUSTODY_CHECKPOINT_FORMAT_VERSION
    ):
        raise PersistentWorldCheckpointFormatError(
            "unsupported R4-E checkpoint format version"
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
    payload = envelope["authoritative_payload"]
    integrity = _require_sha256(
        envelope["integrity_digest"],
        name="integrity_digest",
        error_cls=PersistentWorldCheckpointIntegrityError,
    )
    actual = _sha256_bytes(_canonical_bytes(payload))
    if actual != integrity:
        raise PersistentWorldCheckpointIntegrityError(
            "R4-E checkpoint authoritative payload integrity mismatch"
        )
    return _restore_r4e_payload(
        payload,
        expected_campaign_id=expected_campaign_id,
    )
