"""Bounded persistent follow-intent state for TERMINAL-PLAY-VSM-14.

This module introduces the first authoritative AFQR-12 behavioral-intent family
in the playable Myravant runtime. It owns only whether one bounded follower has
an active immediate-follow intent toward one bounded leader.

It does not own movement, topology, opportunity, player control, obedience,
delegation, social relations, planning, pathfinding, guarding, dialogue,
knowledge, or delayed/conditional task semantics.

Actual movement remains R4-C / AFQR-18 / AFQR-19 / AFQR-01 / AFQR-02 owned.
This family uses the shared deterministic transition lifecycle shell for command
identity, retry sequencing, preparation, commitment, and replay.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Sequence

from astra_runtime.domain._deterministic_transition_support import (
    TransitionCapabilitySpec,
    commit_prepared_capability_transition,
    execute_capability_transition,
    fingerprint_command_envelope,
)
from astra_runtime.kernel.command_envelope import CommandEnvelope, validate_command_envelope
from astra_runtime.kernel.record_identity import build_record_id, is_valid_record_id
from astra_runtime.kernel.state_delta import StateDeltaEnvelope, create_state_delta_envelope
from astra_runtime.kernel.transaction_preview import TransactionPreview, create_transaction_preview


AFQR12_FOLLOW_INTENT_OWNER = "AFQR-12"
AFQR18_FOLLOW_INTENT_SPATIAL_OWNER = "AFQR-18"
AFQR19_FOLLOW_INTENT_OPPORTUNITY_OWNER = "AFQR-19"
AFQR01_FOLLOW_INTENT_COMMIT_OWNER = "AFQR-01"
AFQR02_FOLLOW_INTENT_COMMAND_OWNER = "AFQR-02"

FOLLOW_INTENT_OPERATIONS = frozenset({"activate", "deactivate"})
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class PersistentWorldFollowIntentError(ValueError):
    """Base bounded follow-intent failure."""


class InvalidPersistentWorldFollowIntentRequestError(PersistentWorldFollowIntentError):
    pass


class PersistentWorldFollowIntentEvidenceError(PersistentWorldFollowIntentError):
    pass


class PersistentWorldFollowIntentNoChangeError(PersistentWorldFollowIntentError):
    pass


class PersistentWorldFollowIntentStaleStateError(PersistentWorldFollowIntentError):
    pass


class PersistentWorldFollowIntentRetryConflictError(PersistentWorldFollowIntentError):
    pass


class PersistentWorldFollowIntentReplayError(PersistentWorldFollowIntentError):
    pass


def _require_record_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise InvalidPersistentWorldFollowIntentRequestError(
            f"{label} must be a valid record ID"
        )
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise InvalidPersistentWorldFollowIntentRequestError(
            f"{label} must be a lowercase SHA-256 digest"
        )
    return value


@dataclass(frozen=True, kw_only=True)
class FollowIntentQualificationEvidence:
    evidence_id: str
    follower_entity_id: str
    leader_entity_id: str
    operation: str
    qualified: bool
    semantic_owner: str = AFQR12_FOLLOW_INTENT_OWNER

    def __post_init__(self) -> None:
        for name in ("evidence_id", "follower_entity_id", "leader_entity_id"):
            _require_record_id(getattr(self, name), name)
        if self.follower_entity_id == self.leader_entity_id:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "follower and leader must differ"
            )
        if self.operation not in FOLLOW_INTENT_OPERATIONS:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "operation must be activate or deactivate"
            )
        if type(self.qualified) is not bool:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "qualified must be bool"
            )
        if self.semantic_owner != AFQR12_FOLLOW_INTENT_OWNER:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "qualification semantic_owner must be AFQR-12"
            )


@dataclass(frozen=True, kw_only=True)
class FollowIntentSpatialEvidence:
    evidence_id: str
    follower_entity_id: str
    leader_entity_id: str
    place_id: str
    co_located: bool
    semantic_owner: str = AFQR18_FOLLOW_INTENT_SPATIAL_OWNER

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "follower_entity_id",
            "leader_entity_id",
            "place_id",
        ):
            _require_record_id(getattr(self, name), name)
        if self.follower_entity_id == self.leader_entity_id:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "follower and leader must differ"
            )
        if type(self.co_located) is not bool:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "co_located must be bool"
            )
        if self.semantic_owner != AFQR18_FOLLOW_INTENT_SPATIAL_OWNER:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "spatial semantic_owner must be AFQR-18"
            )


@dataclass(frozen=True, kw_only=True)
class FollowIntentOpportunityEvidence:
    evidence_id: str
    follower_entity_id: str
    leader_entity_id: str
    operation: str
    opportunity_available: bool
    resolution_accepted: bool
    semantic_owner: str = AFQR19_FOLLOW_INTENT_OPPORTUNITY_OWNER

    def __post_init__(self) -> None:
        for name in ("evidence_id", "follower_entity_id", "leader_entity_id"):
            _require_record_id(getattr(self, name), name)
        if self.follower_entity_id == self.leader_entity_id:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "follower and leader must differ"
            )
        if self.operation not in FOLLOW_INTENT_OPERATIONS:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "operation must be activate or deactivate"
            )
        if (
            type(self.opportunity_available) is not bool
            or type(self.resolution_accepted) is not bool
        ):
            raise InvalidPersistentWorldFollowIntentRequestError(
                "opportunity flags must be bool"
            )
        if self.semantic_owner != AFQR19_FOLLOW_INTENT_OPPORTUNITY_OWNER:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "opportunity semantic_owner must be AFQR-19"
            )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldFollowIntent:
    follower_entity_id: str
    leader_entity_id: str
    semantic_owner: str = AFQR12_FOLLOW_INTENT_OWNER

    def __post_init__(self) -> None:
        _require_record_id(self.follower_entity_id, "follower_entity_id")
        _require_record_id(self.leader_entity_id, "leader_entity_id")
        if self.follower_entity_id == self.leader_entity_id:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "follower and leader must differ"
            )
        if self.semantic_owner != AFQR12_FOLLOW_INTENT_OWNER:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "follow intent semantic_owner must be AFQR-12"
            )

    def to_dict(self) -> dict[str, str]:
        return {
            "follower_entity_id": self.follower_entity_id,
            "leader_entity_id": self.leader_entity_id,
            "semantic_owner": self.semantic_owner,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldFollowIntentCommitReceipt:
    receipt_id: str
    command_id: str
    command_fingerprint: str
    follower_entity_id: str
    leader_entity_id: str
    operation: str
    pre_status: str
    post_status: str
    place_id: str
    pre_state_digest: str
    post_state_digest: str
    preview_id: str
    state_delta_id: str
    qualification_evidence_id: str
    spatial_evidence_id: str
    opportunity_evidence_id: str
    status: str = "committed"

    def __post_init__(self) -> None:
        for name in (
            "receipt_id",
            "follower_entity_id",
            "leader_entity_id",
            "place_id",
            "preview_id",
            "state_delta_id",
            "qualification_evidence_id",
            "spatial_evidence_id",
            "opportunity_evidence_id",
        ):
            _require_record_id(getattr(self, name), name)
        if not isinstance(self.command_id, str) or not self.command_id:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "command_id must be non-empty"
            )
        _require_sha256(self.command_fingerprint, "command_fingerprint")
        _require_sha256(self.pre_state_digest, "pre_state_digest")
        _require_sha256(self.post_state_digest, "post_state_digest")
        if self.operation not in FOLLOW_INTENT_OPERATIONS:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "operation must be activate or deactivate"
            )
        expected = (
            ("inactive", "active")
            if self.operation == "activate"
            else ("active", "inactive")
        )
        if (self.pre_status, self.post_status) != expected:
            raise InvalidPersistentWorldFollowIntentRequestError(
                "receipt statuses disagree with operation"
            )
        if self.status != "committed":
            raise InvalidPersistentWorldFollowIntentRequestError(
                "receipt status must be committed"
            )

    def to_dict(self) -> dict[str, str]:
        return {
            "receipt_id": self.receipt_id,
            "command_id": self.command_id,
            "command_fingerprint": self.command_fingerprint,
            "follower_entity_id": self.follower_entity_id,
            "leader_entity_id": self.leader_entity_id,
            "operation": self.operation,
            "pre_status": self.pre_status,
            "post_status": self.post_status,
            "place_id": self.place_id,
            "pre_state_digest": self.pre_state_digest,
            "post_state_digest": self.post_state_digest,
            "preview_id": self.preview_id,
            "state_delta_id": self.state_delta_id,
            "qualification_evidence_id": self.qualification_evidence_id,
            "spatial_evidence_id": self.spatial_evidence_id,
            "opportunity_evidence_id": self.opportunity_evidence_id,
            "status": self.status,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldFollowIntentCommittedTransition:
    command_id: str
    command_fingerprint: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    receipt: PersistentWorldFollowIntentCommitReceipt


@dataclass(frozen=True, kw_only=True)
class PersistentWorldFollowIntentRuntimeState:
    active_intents: tuple[PersistentWorldFollowIntent, ...] = ()
    committed_transitions: tuple[
        PersistentWorldFollowIntentCommittedTransition, ...
    ] = ()

    def __post_init__(self) -> None:
        intents = tuple(
            sorted(self.active_intents, key=lambda item: item.follower_entity_id)
        )
        if any(not isinstance(item, PersistentWorldFollowIntent) for item in intents):
            raise InvalidPersistentWorldFollowIntentRequestError(
                "active_intents contains an invalid value"
            )
        follower_ids = [item.follower_entity_id for item in intents]
        if len(follower_ids) != len(set(follower_ids)):
            raise InvalidPersistentWorldFollowIntentRequestError(
                "a follower may have at most one active bounded follow intent"
            )

        transitions = tuple(self.committed_transitions)
        if any(
            not isinstance(item, PersistentWorldFollowIntentCommittedTransition)
            for item in transitions
        ):
            raise InvalidPersistentWorldFollowIntentRequestError(
                "committed_transitions contains an invalid value"
            )
        command_ids = [item.command_id for item in transitions]
        if len(command_ids) != len(set(command_ids)):
            raise InvalidPersistentWorldFollowIntentRequestError(
                "follow-intent command IDs must be unique"
            )
        object.__setattr__(self, "active_intents", intents)
        object.__setattr__(self, "committed_transitions", transitions)


@dataclass(frozen=True, kw_only=True)
class PersistentWorldFollowIntentPreparedTransition:
    command_id: str
    command_fingerprint: str
    follower_entity_id: str
    leader_entity_id: str
    operation: str
    pre_status: str
    post_status: str
    place_id: str
    pre_state_digest: str
    post_state_digest: str
    qualification_evidence_id: str
    spatial_evidence_id: str
    opportunity_evidence_id: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    post_active_intents: tuple[PersistentWorldFollowIntent, ...]


@dataclass(frozen=True, kw_only=True)
class PersistentWorldFollowIntentExecutionResult:
    state: PersistentWorldFollowIntentRuntimeState
    receipt: PersistentWorldFollowIntentCommitReceipt
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    technical_retry: bool


def create_follow_intent_qualification_evidence(
    *,
    evidence_id: str,
    follower_entity_id: str,
    leader_entity_id: str,
    operation: str,
    qualified: bool,
) -> FollowIntentQualificationEvidence:
    return FollowIntentQualificationEvidence(
        evidence_id=evidence_id,
        follower_entity_id=follower_entity_id,
        leader_entity_id=leader_entity_id,
        operation=operation,
        qualified=qualified,
    )


def create_follow_intent_spatial_evidence(
    *,
    evidence_id: str,
    follower_entity_id: str,
    leader_entity_id: str,
    place_id: str,
    co_located: bool,
) -> FollowIntentSpatialEvidence:
    return FollowIntentSpatialEvidence(
        evidence_id=evidence_id,
        follower_entity_id=follower_entity_id,
        leader_entity_id=leader_entity_id,
        place_id=place_id,
        co_located=co_located,
    )


def create_follow_intent_opportunity_evidence(
    *,
    evidence_id: str,
    follower_entity_id: str,
    leader_entity_id: str,
    operation: str,
    opportunity_available: bool,
    resolution_accepted: bool,
) -> FollowIntentOpportunityEvidence:
    return FollowIntentOpportunityEvidence(
        evidence_id=evidence_id,
        follower_entity_id=follower_entity_id,
        leader_entity_id=leader_entity_id,
        operation=operation,
        opportunity_available=opportunity_available,
        resolution_accepted=resolution_accepted,
    )


def create_persistent_world_follow_intent_runtime_state(
    *,
    active_intents: Sequence[PersistentWorldFollowIntent] = (),
    committed_transitions: Sequence[
        PersistentWorldFollowIntentCommittedTransition
    ] = (),
) -> PersistentWorldFollowIntentRuntimeState:
    return PersistentWorldFollowIntentRuntimeState(
        active_intents=tuple(active_intents),
        committed_transitions=tuple(committed_transitions),
    )


def active_follow_intent_for(
    state: PersistentWorldFollowIntentRuntimeState,
    follower_entity_id: str,
) -> PersistentWorldFollowIntent | None:
    for item in state.active_intents:
        if item.follower_entity_id == follower_entity_id:
            return item
    return None


def serialize_persistent_world_follow_intent(
    intent: PersistentWorldFollowIntent,
) -> dict[str, str]:
    if not isinstance(intent, PersistentWorldFollowIntent):
        raise InvalidPersistentWorldFollowIntentRequestError(
            "intent must be PersistentWorldFollowIntent"
        )
    return intent.to_dict()


def canonical_serialize_persistent_world_follow_intents(
    intents: Sequence[PersistentWorldFollowIntent],
) -> str:
    ordered = tuple(sorted(intents, key=lambda item: item.follower_entity_id))
    material = {
        "state_family": "afqr12_bounded_follow_intent",
        "active_intents": [
            serialize_persistent_world_follow_intent(item) for item in ordered
        ],
    }
    return json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def digest_persistent_world_follow_intents(
    intents: Sequence[PersistentWorldFollowIntent],
) -> str:
    return hashlib.sha256(
        canonical_serialize_persistent_world_follow_intents(intents).encode("utf-8")
    ).hexdigest()


def digest_persistent_world_follow_intent_runtime_state(
    state: PersistentWorldFollowIntentRuntimeState,
) -> str:
    if not isinstance(state, PersistentWorldFollowIntentRuntimeState):
        raise InvalidPersistentWorldFollowIntentRequestError(
            "state must be PersistentWorldFollowIntentRuntimeState"
        )
    return digest_persistent_world_follow_intents(state.active_intents)


def fingerprint_persistent_world_follow_intent_command(
    command: CommandEnvelope,
) -> str:
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldFollowIntentRequestError(
            "command failed CommandEnvelope validation"
        )
    return fingerprint_command_envelope(command, allow_nan=False)


def _operation_from_command(command: CommandEnvelope) -> str:
    operation = command.payload.get("operation")
    if operation in FOLLOW_INTENT_OPERATIONS:
        return operation
    raise InvalidPersistentWorldFollowIntentRequestError(
        "VSM-14 follow intent supports only activate/deactivate"
    )


def _validate_evidence(
    *,
    qualification_evidence: FollowIntentQualificationEvidence,
    spatial_evidence: FollowIntentSpatialEvidence,
    opportunity_evidence: FollowIntentOpportunityEvidence,
    follower_entity_id: str,
    leader_entity_id: str,
    operation: str,
) -> None:
    if not isinstance(qualification_evidence, FollowIntentQualificationEvidence):
        raise PersistentWorldFollowIntentEvidenceError(
            "invalid AFQR-12 qualification evidence"
        )
    if not isinstance(spatial_evidence, FollowIntentSpatialEvidence):
        raise PersistentWorldFollowIntentEvidenceError(
            "invalid AFQR-18 spatial evidence"
        )
    if not isinstance(opportunity_evidence, FollowIntentOpportunityEvidence):
        raise PersistentWorldFollowIntentEvidenceError(
            "invalid AFQR-19 opportunity evidence"
        )
    if (
        qualification_evidence.follower_entity_id != follower_entity_id
        or qualification_evidence.leader_entity_id != leader_entity_id
        or qualification_evidence.operation != operation
    ):
        raise PersistentWorldFollowIntentEvidenceError(
            "qualification evidence does not match command"
        )
    if (
        spatial_evidence.follower_entity_id != follower_entity_id
        or spatial_evidence.leader_entity_id != leader_entity_id
    ):
        raise PersistentWorldFollowIntentEvidenceError(
            "spatial evidence does not match command"
        )
    if (
        opportunity_evidence.follower_entity_id != follower_entity_id
        or opportunity_evidence.leader_entity_id != leader_entity_id
        or opportunity_evidence.operation != operation
    ):
        raise PersistentWorldFollowIntentEvidenceError(
            "opportunity evidence does not match command"
        )
    if not qualification_evidence.qualified:
        raise PersistentWorldFollowIntentEvidenceError(
            "AFQR-12 rejected follow-intent transition"
        )
    if not spatial_evidence.co_located:
        raise PersistentWorldFollowIntentEvidenceError(
            "follow-intent request requires co-located actors"
        )
    if (
        not opportunity_evidence.opportunity_available
        or not opportunity_evidence.resolution_accepted
    ):
        raise PersistentWorldFollowIntentEvidenceError(
            "AFQR-19 rejected follow-intent transition"
        )


def _replace_intent(
    intents: Sequence[PersistentWorldFollowIntent],
    *,
    follower_entity_id: str,
    leader_entity_id: str,
    operation: str,
) -> tuple[PersistentWorldFollowIntent, ...]:
    current = [
        item for item in intents if item.follower_entity_id != follower_entity_id
    ]
    if operation == "activate":
        current.append(
            PersistentWorldFollowIntent(
                follower_entity_id=follower_entity_id,
                leader_entity_id=leader_entity_id,
            )
        )
    return tuple(sorted(current, key=lambda item: item.follower_entity_id))


def prepare_persistent_world_follow_intent(
    *,
    state: PersistentWorldFollowIntentRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: FollowIntentQualificationEvidence,
    spatial_evidence: FollowIntentSpatialEvidence,
    opportunity_evidence: FollowIntentOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldFollowIntentPreparedTransition:
    if not isinstance(state, PersistentWorldFollowIntentRuntimeState):
        raise InvalidPersistentWorldFollowIntentRequestError(
            "invalid follow-intent runtime state"
        )
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldFollowIntentRequestError(
            "invalid command envelope"
        )
    fingerprint = fingerprint_persistent_world_follow_intent_command(command)
    operation = _operation_from_command(command)
    follower_entity_id = command.source_actor_id
    leader_entity_id = _require_record_id(
        command.payload.get("leader_entity_id"),
        "command.payload.leader_entity_id",
    )
    if follower_entity_id == leader_entity_id:
        raise InvalidPersistentWorldFollowIntentRequestError(
            "follower and leader must differ"
        )

    _validate_evidence(
        qualification_evidence=qualification_evidence,
        spatial_evidence=spatial_evidence,
        opportunity_evidence=opportunity_evidence,
        follower_entity_id=follower_entity_id,
        leader_entity_id=leader_entity_id,
        operation=operation,
    )

    actual_digest = digest_persistent_world_follow_intents(state.active_intents)
    if expected_pre_state_digest != actual_digest:
        raise PersistentWorldFollowIntentStaleStateError(
            "owner-local follow-intent state changed before preparation"
        )
    existing = active_follow_intent_for(state, follower_entity_id)
    if operation == "activate":
        if existing is not None:
            raise PersistentWorldFollowIntentNoChangeError(
                "follower already has an active follow intent"
            )
        pre_status, post_status = "inactive", "active"
    else:
        if existing is None or existing.leader_entity_id != leader_entity_id:
            raise PersistentWorldFollowIntentNoChangeError(
                "matching active follow intent does not exist"
            )
        pre_status, post_status = "active", "inactive"

    post_intents = _replace_intent(
        state.active_intents,
        follower_entity_id=follower_entity_id,
        leader_entity_id=leader_entity_id,
        operation=operation,
    )
    post_digest = digest_persistent_world_follow_intents(post_intents)
    preview = create_transaction_preview(
        build_record_id("follow_intent_preview", fingerprint[:24]),
        command,
        messages=("bounded persistent follow intent prepared",),
        requires_confirmation=False,
        metadata={
            "package": "TERMINAL-PLAY-VSM-14",
            "command_family": "behavior",
            "mutation_performed": False,
        },
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("follow_intent_delta", fingerprint[:24]),
        source_command_id=command.command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(follower_entity_id, leader_entity_id),
        change_type="record_update",
        payload={
            "intent_type": "follow",
            "follower_entity_id": follower_entity_id,
            "leader_entity_id": leader_entity_id,
            "operation": operation,
            "pre_status": pre_status,
            "post_status": post_status,
        },
        metadata={
            "package": "TERMINAL-PLAY-VSM-14",
            "behavioral_intent_semantic_owner": AFQR12_FOLLOW_INTENT_OWNER,
            "spatial_semantic_owner": AFQR18_FOLLOW_INTENT_SPATIAL_OWNER,
            "opportunity_semantic_owner": AFQR19_FOLLOW_INTENT_OPPORTUNITY_OWNER,
            "qualified_transition_owner": AFQR01_FOLLOW_INTENT_COMMIT_OWNER,
        },
    )
    return PersistentWorldFollowIntentPreparedTransition(
        command_id=command.command_id,
        command_fingerprint=fingerprint,
        follower_entity_id=follower_entity_id,
        leader_entity_id=leader_entity_id,
        operation=operation,
        pre_status=pre_status,
        post_status=post_status,
        place_id=spatial_evidence.place_id,
        pre_state_digest=actual_digest,
        post_state_digest=post_digest,
        qualification_evidence_id=qualification_evidence.evidence_id,
        spatial_evidence_id=spatial_evidence.evidence_id,
        opportunity_evidence_id=opportunity_evidence.evidence_id,
        preview=preview,
        state_delta=delta,
        post_active_intents=post_intents,
    )


def _commit_new_persistent_world_follow_intent(
    *,
    state: PersistentWorldFollowIntentRuntimeState,
    prepared: PersistentWorldFollowIntentPreparedTransition,
) -> PersistentWorldFollowIntentExecutionResult:
    if digest_persistent_world_follow_intents(
        state.active_intents
    ) != prepared.pre_state_digest:
        raise PersistentWorldFollowIntentStaleStateError(
            "owner-local follow-intent state changed after preparation"
        )
    receipt = PersistentWorldFollowIntentCommitReceipt(
        receipt_id=build_record_id(
            "follow_intent_receipt", prepared.command_fingerprint[:24]
        ),
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        follower_entity_id=prepared.follower_entity_id,
        leader_entity_id=prepared.leader_entity_id,
        operation=prepared.operation,
        pre_status=prepared.pre_status,
        post_status=prepared.post_status,
        place_id=prepared.place_id,
        pre_state_digest=prepared.pre_state_digest,
        post_state_digest=prepared.post_state_digest,
        preview_id=prepared.preview.preview_id,
        state_delta_id=prepared.state_delta.delta_id,
        qualification_evidence_id=prepared.qualification_evidence_id,
        spatial_evidence_id=prepared.spatial_evidence_id,
        opportunity_evidence_id=prepared.opportunity_evidence_id,
    )
    transition = PersistentWorldFollowIntentCommittedTransition(
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        receipt=receipt,
    )
    post_state = PersistentWorldFollowIntentRuntimeState(
        active_intents=prepared.post_active_intents,
        committed_transitions=(*state.committed_transitions, transition),
    )
    return PersistentWorldFollowIntentExecutionResult(
        state=post_state,
        receipt=receipt,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        technical_retry=False,
    )


def commit_prepared_persistent_world_follow_intent(
    *,
    state: PersistentWorldFollowIntentRuntimeState,
    prepared: PersistentWorldFollowIntentPreparedTransition,
) -> PersistentWorldFollowIntentExecutionResult:
    if not isinstance(state, PersistentWorldFollowIntentRuntimeState):
        raise InvalidPersistentWorldFollowIntentRequestError(
            "invalid follow-intent runtime state"
        )
    if not isinstance(prepared, PersistentWorldFollowIntentPreparedTransition):
        raise InvalidPersistentWorldFollowIntentRequestError(
            "invalid prepared transition"
        )
    return commit_prepared_capability_transition(
        spec=FOLLOW_INTENT_TRANSITION_CAPABILITY_SPEC,
        state=state,
        prepared=prepared,
    )


def execute_persistent_world_follow_intent(
    *,
    state: PersistentWorldFollowIntentRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: FollowIntentQualificationEvidence,
    spatial_evidence: FollowIntentSpatialEvidence,
    opportunity_evidence: FollowIntentOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldFollowIntentExecutionResult:
    return execute_capability_transition(
        spec=FOLLOW_INTENT_TRANSITION_CAPABILITY_SPEC,
        state=state,
        command=command,
        context={
            "qualification_evidence": qualification_evidence,
            "spatial_evidence": spatial_evidence,
            "opportunity_evidence": opportunity_evidence,
            "expected_pre_state_digest": expected_pre_state_digest,
        },
    )


def replay_persistent_world_follow_intents(
    *,
    active_intents: Sequence[PersistentWorldFollowIntent],
    receipt: PersistentWorldFollowIntentCommitReceipt,
) -> tuple[PersistentWorldFollowIntent, ...]:
    if not isinstance(receipt, PersistentWorldFollowIntentCommitReceipt):
        raise PersistentWorldFollowIntentReplayError("receipt has invalid type")
    current = tuple(active_intents)
    if digest_persistent_world_follow_intents(current) != receipt.pre_state_digest:
        raise PersistentWorldFollowIntentReplayError(
            "follow-intent replay pre-state digest mismatch"
        )
    existing = next(
        (
            item
            for item in current
            if item.follower_entity_id == receipt.follower_entity_id
        ),
        None,
    )
    if receipt.operation == "activate" and existing is not None:
        raise PersistentWorldFollowIntentReplayError(
            "follow-intent replay activation starts from active state"
        )
    if receipt.operation == "deactivate" and (
        existing is None or existing.leader_entity_id != receipt.leader_entity_id
    ):
        raise PersistentWorldFollowIntentReplayError(
            "follow-intent replay deactivation lacks matching active state"
        )
    post = _replace_intent(
        current,
        follower_entity_id=receipt.follower_entity_id,
        leader_entity_id=receipt.leader_entity_id,
        operation=receipt.operation,
    )
    if digest_persistent_world_follow_intents(post) != receipt.post_state_digest:
        raise PersistentWorldFollowIntentReplayError(
            "follow-intent replay post-state digest mismatch"
        )
    return post


FOLLOW_INTENT_TRANSITION_CAPABILITY_SPEC = TransitionCapabilitySpec(
    capability_id="persistent_world_follow_intent",
    semantic_owners=(
        AFQR12_FOLLOW_INTENT_OWNER,
        AFQR18_FOLLOW_INTENT_SPATIAL_OWNER,
        AFQR19_FOLLOW_INTENT_OPPORTUNITY_OWNER,
        AFQR01_FOLLOW_INTENT_COMMIT_OWNER,
        AFQR02_FOLLOW_INTENT_COMMAND_OWNER,
    ),
    state_type=PersistentWorldFollowIntentRuntimeState,
    replay_state_type=tuple,
    receipt_prefix="follow_intent_receipt",
    state_digest=digest_persistent_world_follow_intent_runtime_state,
    fingerprint_command=fingerprint_persistent_world_follow_intent_command,
    committed_transitions=lambda state: state.committed_transitions,
    prepare_new_transition=lambda state, command, context: prepare_persistent_world_follow_intent(
        state=state,
        command=command,
        qualification_evidence=context["qualification_evidence"],
        spatial_evidence=context["spatial_evidence"],
        opportunity_evidence=context["opportunity_evidence"],
        expected_pre_state_digest=context["expected_pre_state_digest"],
    ),
    commit_new_transition=lambda state, prepared: _commit_new_persistent_world_follow_intent(
        state=state,
        prepared=prepared,
    ),
    build_retry_result=lambda state, committed: PersistentWorldFollowIntentExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    ),
    retry_conflict_error=lambda message: PersistentWorldFollowIntentRetryConflictError(
        message
    ),
    replay_committed_transition=lambda pre_state, receipt: replay_persistent_world_follow_intents(
        active_intents=pre_state,
        receipt=receipt,
    ),
)


def serialize_persistent_world_follow_intent_commit_receipt(
    receipt: PersistentWorldFollowIntentCommitReceipt,
) -> dict[str, str]:
    if not isinstance(receipt, PersistentWorldFollowIntentCommitReceipt):
        raise InvalidPersistentWorldFollowIntentRequestError(
            "receipt must be PersistentWorldFollowIntentCommitReceipt"
        )
    return receipt.to_dict()
