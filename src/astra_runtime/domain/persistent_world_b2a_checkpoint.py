"""Checkpoint v6 only when B-2a fixture servicing has committed history.

V1-v5 formats are not mutated. Reuse all v5 owner serializers and validators,
then independently replay the extra RT-010/AFQR-16 asset condition stream.
"""

from __future__ import annotations

import hashlib
import json

from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMPONENT_CHECKPOINT_FORMAT_IDENTITY, _validate_envelope_common,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError, _canonical_bytes, _checkpoint_path,
    _normalize_qualification, _read_checkpoint_envelope, _sha256_bytes,
)
from astra_runtime.domain.persistent_world_component_checkpoint import _write_envelope
from astra_runtime.domain.persistent_world_vsm14_checkpoint import (
    VSM14_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    _restore_base_components, _restore_follow_component,
    digest_persistent_world_vsm14_authoritative_state,
    serialize_persistent_world_vsm14_checkpoint_payload,
)
from astra_runtime.domain.persistent_world_fixture_service import (
    FixtureServiceError, FixtureServiceState, restore_fixture_service,
    serialize_fixture_service, digest_fixture_service_state,
)
from astra_runtime.myravant_play_fixture import (
    PLAYER_ID, TOOL_CHEST_ID, YARD_ID, WORKSHOP_ID, ORCHARD_PATH_ID,
)

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
