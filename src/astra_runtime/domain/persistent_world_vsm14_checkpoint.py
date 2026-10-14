"""VSM-14 checkpoint v5: existing persistent world plus AFQR-12 follow intent.

Versions 1 through 4 remain byte/meaning frozen in their existing module. Version
5 appends one `follow_intent` component and reuses the existing v4 component
serializers and restore validators without changing historical formats.
"""

from __future__ import annotations

import hashlib
import json
from types import MappingProxyType

from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
    VSM6_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    _DISPLACEMENT_COMPONENT_KEYS,
    _HANDOFF_COMPONENT_KEYS,
    _reconstruct_int3_payload,
    _restore_actor_object_handoff_transition,
    _restore_object_displacement_transition,
    _validate_comp3_placement_replay,
    _validate_envelope_common,
    _validate_vsm6_placement_replay,
    _write_envelope,
    serialize_persistent_world_vsm6_checkpoint_payload,
)
from astra_runtime.domain.persistent_world_follow_intent import (
    PersistentWorldFollowIntent,
    PersistentWorldFollowIntentCommitReceipt,
    PersistentWorldFollowIntentCommittedTransition,
    PersistentWorldFollowIntentRuntimeState,
    create_persistent_world_follow_intent_runtime_state,
    digest_persistent_world_follow_intent_runtime_state,
    replay_persistent_world_follow_intents,
    serialize_persistent_world_follow_intent_commit_receipt,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError,
    _canonical_bytes,
    _checkpoint_path,
    _normalize_qualification,
    _read_checkpoint_envelope,
    _require_exact_dict,
    _require_sha256,
    _restore_persistent_world_object_storage_payload,
    _sha256_bytes,
)
from astra_runtime.domain.persistent_world_logical_time import (
    InvalidPersistentWorldLogicalTimeRequestError,
    restore_persistent_world_logical_time_state,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    PersistentWorldRuntimeComposition,
    create_persistent_world_runtime_composition_from_storage_state,
    digest_persistent_world_runtime_composition,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    FixtureServiceError, FixtureServiceState, restore_fixture_service,
    serialize_fixture_service, digest_fixture_service_state,
)
from astra_runtime.myravant_play_fixture import (
    PLAYER_ID, TOOL_CHEST_ID, YARD_ID, WORKSHOP_ID, ORCHARD_PATH_ID,
)

from astra_runtime.kernel.state_delta import StateDeltaEnvelope
from astra_runtime.kernel.transaction_preview import TransactionPreview


VSM14_COMPONENT_CHECKPOINT_FORMAT_VERSION = 5
VSM14_COMPONENT_CHECKPOINT_COMPONENT_KEYS = frozenset(
    {*VSM6_COMPONENT_CHECKPOINT_COMPONENT_KEYS, "follow_intent"}
)

_FOLLOW_COMPONENT_KEYS = frozenset(
    {
        "active_intents",
        "committed_follow_intent_transitions",
        "follow_intent_transition_summary",
    }
)
_FOLLOW_INTENT_KEYS = frozenset(
    {"follower_entity_id", "leader_entity_id", "semantic_owner"}
)
_FOLLOW_TRANSITION_KEYS = frozenset(
    {"command_id", "command_fingerprint", "preview", "state_delta", "receipt"}
)
_FOLLOW_PREVIEW_KEYS = frozenset(
    {
        "preview_id",
        "command_id",
        "status",
        "messages",
        "requires_confirmation",
        "metadata",
    }
)
_FOLLOW_DELTA_KEYS = frozenset(
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
_FOLLOW_RECEIPT_KEYS = frozenset(
    {
        "receipt_id",
        "command_id",
        "command_fingerprint",
        "follower_entity_id",
        "leader_entity_id",
        "operation",
        "pre_status",
        "post_status",
        "place_id",
        "pre_state_digest",
        "post_state_digest",
        "preview_id",
        "state_delta_id",
        "qualification_evidence_id",
        "spatial_evidence_id",
        "opportunity_evidence_id",
        "status",
    }
)
_SUMMARY_KEYS = frozenset({"count", "command_ids"})


def digest_persistent_world_vsm14_authoritative_state(
    *,
    runtime_state: PersistentWorldRuntimeComposition,
    follow_intent_state: PersistentWorldFollowIntentRuntimeState,
) -> str:
    material = {
        "state_family": "persistent_world_vsm14_runtime",
        "base_runtime_digest": digest_persistent_world_runtime_composition(
            runtime_state
        ),
        "follow_intent_state_digest": (
            digest_persistent_world_follow_intent_runtime_state(
                follow_intent_state
            )
        ),
    }
    canonical = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _serialize_follow_transition(
    transition: PersistentWorldFollowIntentCommittedTransition,
) -> dict[str, object]:
    if not isinstance(
        transition, PersistentWorldFollowIntentCommittedTransition
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent transition has invalid type"
        )
    return {
        "command_id": transition.command_id,
        "command_fingerprint": transition.command_fingerprint,
        "preview": transition.preview.to_dict(),
        "state_delta": transition.state_delta.to_dict(),
        "receipt": serialize_persistent_world_follow_intent_commit_receipt(
            transition.receipt
        ),
    }


def serialize_persistent_world_vsm14_checkpoint_payload(
    *,
    runtime_state: PersistentWorldRuntimeComposition,
    follow_intent_state: PersistentWorldFollowIntentRuntimeState,
) -> dict[str, object]:
    if not isinstance(runtime_state, PersistentWorldRuntimeComposition):
        raise PersistentWorldCheckpointEvidenceError(
            "VSM-14 base runtime has invalid type"
        )
    if not isinstance(
        follow_intent_state, PersistentWorldFollowIntentRuntimeState
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "VSM-14 follow-intent state has invalid type"
        )
    payload = serialize_persistent_world_vsm6_checkpoint_payload(runtime_state)
    transitions = [
        _serialize_follow_transition(item)
        for item in follow_intent_state.committed_transitions
    ]
    payload["components"]["follow_intent"] = {
        "active_intents": [
            item.to_dict() for item in follow_intent_state.active_intents
        ],
        "committed_follow_intent_transitions": transitions,
        "follow_intent_transition_summary": {
            "count": len(transitions),
            "command_ids": sorted(
                item["command_id"] for item in transitions
            ),
        },
    }
    return payload


def build_persistent_world_vsm14_checkpoint_envelope(
    *,
    runtime_state: PersistentWorldRuntimeComposition,
    follow_intent_state: PersistentWorldFollowIntentRuntimeState,
    qualification_evidence,
) -> dict[str, object]:
    payload = serialize_persistent_world_vsm14_checkpoint_payload(
        runtime_state=runtime_state,
        follow_intent_state=follow_intent_state,
    )
    return {
        "format_identity": COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
        "format_version": VSM14_COMPONENT_CHECKPOINT_FORMAT_VERSION,
        "campaign_identity": runtime_state.movement_state.representation.campaign_id,
        "authoritative_payload": payload,
        "integrity_digest": _sha256_bytes(_canonical_bytes(payload)),
        "qualification_provenance": _normalize_qualification(
            qualification_evidence
        ),
    }


def write_persistent_world_vsm14_checkpoint(
    *,
    runtime_state: PersistentWorldRuntimeComposition,
    follow_intent_state: PersistentWorldFollowIntentRuntimeState,
    checkpoint_path,
    qualification_evidence,
) -> str:
    return _write_envelope(
        envelope=build_persistent_world_vsm14_checkpoint_envelope(
            runtime_state=runtime_state,
            follow_intent_state=follow_intent_state,
            qualification_evidence=qualification_evidence,
        ),
        checkpoint_path=checkpoint_path,
    )


def _restore_follow_transition(
    material,
) -> PersistentWorldFollowIntentCommittedTransition:
    transition = _require_exact_dict(
        material,
        expected_keys=_FOLLOW_TRANSITION_KEYS,
        name="follow-intent transition",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    receipt_material = _require_exact_dict(
        transition["receipt"],
        expected_keys=_FOLLOW_RECEIPT_KEYS,
        name="follow-intent receipt",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    try:
        receipt = PersistentWorldFollowIntentCommitReceipt(**receipt_material)
    except Exception as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent receipt is invalid"
        ) from exc

    command_id = transition["command_id"]
    command_fingerprint = transition["command_fingerprint"]
    if (
        not isinstance(command_id, str)
        or not command_id
        or command_id != receipt.command_id
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent command identity is inconsistent"
        )
    _require_sha256(
        command_fingerprint,
        name="follow-intent transition.command_fingerprint",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    if command_fingerprint != receipt.command_fingerprint:
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent fingerprint is inconsistent"
        )

    preview_material = _require_exact_dict(
        transition["preview"],
        expected_keys=_FOLLOW_PREVIEW_KEYS,
        name="follow-intent preview",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    preview_metadata = {
        "package": "TERMINAL-PLAY-VSM-14",
        "command_family": "behavior",
        "mutation_performed": False,
    }
    if (
        preview_material["command_id"] != command_id
        or preview_material["preview_id"] != receipt.preview_id
        or preview_material["status"] != "preview_created"
        or preview_material["messages"]
        != ["bounded persistent follow intent prepared"]
        or preview_material["requires_confirmation"] is not False
        or preview_material["metadata"] != preview_metadata
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent preview is inconsistent"
        )
    preview = TransactionPreview(
        preview_id=receipt.preview_id,
        command_id=command_id,
        status="preview_created",
        messages=("bounded persistent follow intent prepared",),
        requires_confirmation=False,
        metadata=MappingProxyType(dict(preview_metadata)),
    )

    delta_material = _require_exact_dict(
        transition["state_delta"],
        expected_keys=_FOLLOW_DELTA_KEYS,
        name="follow-intent state delta",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    expected_affected = [
        receipt.follower_entity_id,
        receipt.leader_entity_id,
    ]
    expected_payload = {
        "intent_type": "follow",
        "follower_entity_id": receipt.follower_entity_id,
        "leader_entity_id": receipt.leader_entity_id,
        "operation": receipt.operation,
        "pre_status": receipt.pre_status,
        "post_status": receipt.post_status,
    }
    expected_metadata = {
        "package": "TERMINAL-PLAY-VSM-14",
        "behavioral_intent_semantic_owner": "AFQR-12",
        "spatial_semantic_owner": "AFQR-18",
        "opportunity_semantic_owner": "AFQR-19",
        "qualified_transition_owner": "AFQR-01",
    }
    if (
        delta_material["source_command_id"] != command_id
        or delta_material["source_preview_id"] != receipt.preview_id
        or delta_material["delta_id"] != receipt.state_delta_id
        or delta_material["affected_record_ids"] != expected_affected
        or delta_material["change_type"] != "record_update"
        or delta_material["payload"] != expected_payload
        or delta_material["metadata"] != expected_metadata
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent state delta is inconsistent"
        )
    state_delta = StateDeltaEnvelope(
        delta_id=receipt.state_delta_id,
        source_command_id=command_id,
        source_preview_id=receipt.preview_id,
        affected_record_ids=tuple(expected_affected),
        change_type="record_update",
        payload=MappingProxyType(dict(expected_payload)),
        metadata=MappingProxyType(dict(expected_metadata)),
    )
    return PersistentWorldFollowIntentCommittedTransition(
        command_id=command_id,
        command_fingerprint=command_fingerprint,
        preview=preview,
        state_delta=state_delta,
        receipt=receipt,
    )


def _restore_follow_component(
    material,
) -> PersistentWorldFollowIntentRuntimeState:
    component = _require_exact_dict(
        material,
        expected_keys=_FOLLOW_COMPONENT_KEYS,
        name="follow-intent component",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    intents_material = component["active_intents"]
    if type(intents_material) is not list:
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent active_intents must be a list"
        )
    intents = []
    for item in intents_material:
        intent_material = _require_exact_dict(
            item,
            expected_keys=_FOLLOW_INTENT_KEYS,
            name="follow-intent active intent",
            error_cls=PersistentWorldCheckpointEvidenceError,
        )
        try:
            intents.append(PersistentWorldFollowIntent(**intent_material))
        except Exception as exc:
            raise PersistentWorldCheckpointEvidenceError(
                "follow-intent active intent is invalid"
            ) from exc

    transitions_material = component["committed_follow_intent_transitions"]
    if type(transitions_material) is not list:
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent transitions must be a list"
        )
    transitions = tuple(
        _restore_follow_transition(item) for item in transitions_material
    )
    summary = _require_exact_dict(
        component["follow_intent_transition_summary"],
        expected_keys=_SUMMARY_KEYS,
        name="follow-intent transition summary",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    if (
        type(summary["count"]) is not int
        or summary["count"] != len(transitions)
        or summary["command_ids"]
        != sorted(item.command_id for item in transitions)
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent transition summary is inconsistent"
        )

    replayed: tuple[PersistentWorldFollowIntent, ...] = ()
    for transition in transitions:
        try:
            replayed = replay_persistent_world_follow_intents(
                active_intents=replayed,
                receipt=transition.receipt,
            )
        except Exception as exc:
            raise PersistentWorldCheckpointEvidenceError(
                "follow-intent replay failed"
            ) from exc

    state = create_persistent_world_follow_intent_runtime_state(
        active_intents=intents,
        committed_transitions=transitions,
    )
    if replayed != state.active_intents:
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent replay differs from restored active state"
        )
    return state


def _restore_base_components(
    *,
    components,
    expected_campaign_id,
    expected_initial_open_states,
    expected_initial_lit_states,
    expected_initial_representation,
    expected_initial_representation_digest,
) -> PersistentWorldRuntimeComposition:
    displacement_component = _require_exact_dict(
        components["object_displacement"],
        expected_keys=_DISPLACEMENT_COMPONENT_KEYS,
        name="VSM-14 object displacement component",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    displacement_material = displacement_component[
        "committed_object_displacement_transitions"
    ]
    if type(displacement_material) is not list:
        raise PersistentWorldCheckpointEvidenceError(
            "VSM-14 object displacement transitions must be a list"
        )
    displacement_transitions = tuple(
        _restore_object_displacement_transition(item)
        for item in displacement_material
    )
    displacement_summary = _require_exact_dict(
        displacement_component["object_displacement_transition_summary"],
        expected_keys=_SUMMARY_KEYS,
        name="VSM-14 object displacement transition summary",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    if (
        type(displacement_summary["count"]) is not int
        or displacement_summary["count"] != len(displacement_transitions)
        or displacement_summary["command_ids"]
        != sorted(item.command_id for item in displacement_transitions)
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "VSM-14 object displacement transition summary is inconsistent"
        )

    handoff_component = _require_exact_dict(
        components["actor_object_handoff"],
        expected_keys=_HANDOFF_COMPONENT_KEYS,
        name="VSM-14 actor-object handoff component",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    handoff_material = handoff_component[
        "committed_actor_object_handoff_transitions"
    ]
    if type(handoff_material) is not list:
        raise PersistentWorldCheckpointEvidenceError(
            "VSM-14 actor-object handoff transitions must be a list"
        )
    handoff_transitions = tuple(
        _restore_actor_object_handoff_transition(item)
        for item in handoff_material
    )
    handoff_summary = _require_exact_dict(
        handoff_component["actor_object_handoff_transition_summary"],
        expected_keys=_SUMMARY_KEYS,
        name="VSM-14 actor-object handoff transition summary",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    if (
        type(handoff_summary["count"]) is not int
        or handoff_summary["count"] != len(handoff_transitions)
        or handoff_summary["command_ids"]
        != sorted(item.command_id for item in handoff_transitions)
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "VSM-14 actor-object handoff transition summary is inconsistent"
        )

    base_payload = {
        "components": {
            key: value
            for key, value in components.items()
            if key
            not in {
                "logical_time",
                "object_displacement",
                "actor_object_handoff",
                "follow_intent",
            }
        }
    }
    has_extended_placement = bool(
        displacement_transitions or handoff_transitions
    )
    storage_state = _restore_persistent_world_object_storage_payload(
        payload_material=_reconstruct_int3_payload(base_payload),
        expected_campaign_id=expected_campaign_id,
        expected_initial_open_states=expected_initial_open_states,
        expected_initial_lit_states=expected_initial_lit_states,
        expected_initial_representation_digest=(
            expected_initial_representation_digest
        ),
        defer_combined_attribution=has_extended_placement,
    )
    try:
        logical_time_state = restore_persistent_world_logical_time_state(
            components["logical_time"]
        )
    except InvalidPersistentWorldLogicalTimeRequestError as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "VSM-14 logical-time checkpoint component is invalid"
        ) from exc

    final_representation = (
        storage_state.lit_state.open_close_state.custody_state
        .movement_state.representation
    )
    if handoff_transitions:
        _validate_vsm6_placement_replay(
            initial_representation=expected_initial_representation,
            final_representation=final_representation,
            storage_state=storage_state,
            displacement_transitions=displacement_transitions,
            handoff_transitions=handoff_transitions,
            expected_initial_representation_digest=(
                expected_initial_representation_digest
            ),
        )
    elif displacement_transitions:
        _validate_comp3_placement_replay(
            initial_representation=expected_initial_representation,
            final_representation=final_representation,
            storage_state=storage_state,
            displacement_transitions=displacement_transitions,
            expected_initial_representation_digest=(
                expected_initial_representation_digest
            ),
        )

    return create_persistent_world_runtime_composition_from_storage_state(
        storage_state,
        logical_time_state=logical_time_state,
        committed_object_displacement_transitions=displacement_transitions,
        committed_actor_object_handoff_transitions=handoff_transitions,
    )


def restore_persistent_world_vsm14_checkpoint(
    *,
    checkpoint_path,
    expected_campaign_id,
    expected_initial_open_states,
    expected_initial_lit_states,
    expected_initial_representation,
    expected_initial_representation_digest,
) -> tuple[
    PersistentWorldRuntimeComposition,
    PersistentWorldFollowIntentRuntimeState,
]:
    path = _checkpoint_path(checkpoint_path)
    envelope = _read_checkpoint_envelope(path)
    payload = _validate_envelope_common(
        envelope=envelope,
        expected_campaign_id=expected_campaign_id,
        expected_version=VSM14_COMPONENT_CHECKPOINT_FORMAT_VERSION,
    )
    components = _require_exact_dict(
        payload["components"],
        expected_keys=VSM14_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
        name="VSM-14 checkpoint components",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    runtime_state = _restore_base_components(
        components=components,
        expected_campaign_id=expected_campaign_id,
        expected_initial_open_states=expected_initial_open_states,
        expected_initial_lit_states=expected_initial_lit_states,
        expected_initial_representation=expected_initial_representation,
        expected_initial_representation_digest=(
            expected_initial_representation_digest
        ),
    )
    follow_state = _restore_follow_component(components["follow_intent"])

    base_ids = {
        item.command_id
        for item in runtime_state.movement_state.committed_transitions
    }
    base_ids.update(
        item.command_id
        for item in runtime_state.committed_custody_transitions
    )
    base_ids.update(
        item.command_id
        for item in runtime_state.committed_object_state_transitions
    )
    base_ids.update(
        item.command_id
        for item in runtime_state.committed_object_lit_transitions
    )
    base_ids.update(
        item.command_id
        for item in runtime_state.committed_storage_transitions
    )
    base_ids.update(
        item.command_id
        for item in runtime_state.committed_object_displacement_transitions
    )
    base_ids.update(
        item.command_id
        for item in runtime_state.committed_actor_object_handoff_transitions
    )
    base_ids.update(
        item.command_id
        for item in runtime_state.logical_time_state.committed_transitions
    )
    follow_ids = {
        item.command_id for item in follow_state.committed_transitions
    }
    if base_ids & follow_ids:
        raise PersistentWorldCheckpointEvidenceError(
            "follow-intent command IDs collide with existing runtime commands"
        )
    return runtime_state, follow_state


# Version 6 is opt-in and additive; above V1–V5 logic is frozen.
B2A_CHECKPOINT_VERSION = 6


def digest_b2a_authoritative_state(*, runtime_state, follow_intent_state,
                                   service_state: FixtureServiceState) -> str:
    # Existing v5 tests and historical receipts remain meaningful until
    # the first genuinely new asset-condition transition is committed.
    old = digest_persistent_world_vsm14_authoritative_state(
        runtime_state=runtime_state, follow_intent_state=follow_intent_state,
    )
    if not service_state.events:
        return old
    data = json.dumps({
        "family": "myravant-b2a-v6",
        "base": old,
        "asset": digest_fixture_service_state(service_state),
    }, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def write_b2a_checkpoint(*, runtime_state, follow_intent_state,
                         service_state, checkpoint_path,
                         qualification_evidence) -> str:
    if not service_state.events:
        raise PersistentWorldCheckpointEvidenceError(
            "new checkpoint version requires a service transition"
        )
    payload = serialize_persistent_world_vsm14_checkpoint_payload(
        runtime_state=runtime_state, follow_intent_state=follow_intent_state,
    )
    payload["components"]["fixture_service"] = serialize_fixture_service(
        service_state
    )
    return _write_envelope(
        envelope={
            "format_identity": COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
            "format_version": B2A_CHECKPOINT_VERSION,
            "campaign_identity": runtime_state.movement_state.representation.campaign_id,
            "authoritative_payload": payload,
            "integrity_digest": _sha256_bytes(_canonical_bytes(payload)),
            "qualification_provenance": _normalize_qualification(qualification_evidence),
        },
        checkpoint_path=checkpoint_path,
    )


def restore_b2a_checkpoint(*, checkpoint_path, expected_campaign_id,
                           expected_initial_open_states,
                           expected_initial_lit_states,
                           expected_initial_representation,
                           expected_initial_representation_digest):
    envelope = _read_checkpoint_envelope(_checkpoint_path(checkpoint_path))
    payload = _validate_envelope_common(
        envelope=envelope, expected_campaign_id=expected_campaign_id,
        expected_version=B2A_CHECKPOINT_VERSION,
    )
    components = payload["components"]
    if type(components) is not dict or set(components) != (
        set(VSM14_COMPONENT_CHECKPOINT_COMPONENT_KEYS) | {"fixture_service"}
    ):
        raise PersistentWorldCheckpointEvidenceError(
            "B-2a component inventory is invalid"
        )
    # The frozen v5 base restorer accepts only its historical components.
    # Strip the v6 extension before reconstructing the legacy base payload.
    base_components = {
        key: value for key, value in components.items()
        if key != "fixture_service"
    }
    runtime = _restore_base_components(
        components=base_components, expected_campaign_id=expected_campaign_id,
        expected_initial_open_states=expected_initial_open_states,
        expected_initial_lit_states=expected_initial_lit_states,
        expected_initial_representation=expected_initial_representation,
        expected_initial_representation_digest=expected_initial_representation_digest,
    )
    follow = _restore_follow_component(components["follow_intent"])
    try:
        service = restore_fixture_service(components["fixture_service"])
    except FixtureServiceError as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "B-2a service events do not replay"
        ) from exc
    if not service.events:
        raise PersistentWorldCheckpointEvidenceError(
            "empty service history must use historical v5 format"
        )

    # Time is owned separately: each work record must cite an actual committed
    # AFQR-04 advancement, and the receipt's positions must be identical.
    by_receipt = {
        tr.receipt.receipt_id: tr.receipt
        for tr in runtime.logical_time_state.committed_transitions
    }
    seen_time: set[str] = set()
    used_commands = {
        tr.command_id for tr in runtime.logical_time_state.committed_transitions
    }
    used_commands.update(
        tr.command_id for tr in follow.committed_transitions
    )
    for tr in service.events:
        if tr.command_id in used_commands:
            raise PersistentWorldCheckpointEvidenceError(
                "B-2a command identity collides with existing owner"
            )
        used_commands.add(tr.command_id)
        if (
            tr.actor_id != PLAYER_ID or tr.target_id != TOOL_CHEST_ID
            or (
                tr.operation == "release"
                and tr.place_id not in {YARD_ID, WORKSHOP_ID, ORCHARD_PATH_ID}
            )
            or (tr.operation != "release" and tr.place_id != YARD_ID)
        ):
            raise PersistentWorldCheckpointEvidenceError(
                "service event escaped declared fixture"
            )
        if tr.logical_after > runtime.logical_time_state.logical_position:
            raise PersistentWorldCheckpointEvidenceError(
                "service event refers to future world time"
            )
        if tr.operation == "work":
            receipt = by_receipt.get(tr.time_receipt_id)
            if (
                receipt is None or
                receipt.pre_position != tr.logical_before or
                receipt.post_position != tr.logical_after or
                tr.time_receipt_id in seen_time
            ):
                raise PersistentWorldCheckpointEvidenceError(
                    "labor lacks distinct matching AFQR-04 receipt"
                )
            seen_time.add(tr.time_receipt_id)
    return runtime, follow, service
