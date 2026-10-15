"""D-1 opt-in checkpoint v8: conserved RT-010 brace plus v7-compatible owners.

Formats v1-v7 remain unchanged. v8 is used only when the explicitly
noncanonical component has a committed physical alteration. It is not a
new persistence owner; its envelope uses the existing atomic writer.
"""
from __future__ import annotations

from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMPONENT_CHECKPOINT_FORMAT_IDENTITY, _validate_envelope_common,
    _write_envelope,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError,
    _canonical_bytes, _checkpoint_path, _normalize_qualification,
    _read_checkpoint_envelope, _require_exact_dict, _sha256_bytes,
)
from astra_runtime.domain.persistent_world_vsm14_checkpoint import (
    VSM14_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    _restore_base_components, _restore_follow_component,
    _validate_fixture_service_cross_owner,
    digest_c1_authoritative_state, serialize_persistent_world_vsm14_checkpoint_payload,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    FixtureServiceError, restore_fixture_service, serialize_fixture_service,
)
from astra_runtime.domain.persistent_world_fixture_brace import (
    FixtureBraceError, FixtureBraceState,
    digest_fixture_brace, restore_fixture_brace, serialize_fixture_brace,
)
from astra_runtime.myravant_actor_situated_knowledge import (
    ActorKnowledgeError, restore_actor_knowledge,
    serialize_actor_knowledge,
)

D1_VERSION = 8


def digest_d1_authoritative_state(*, runtime_state, follow_intent_state,
                                  service_state, knowledge_state,
                                  brace_state: FixtureBraceState) -> str:
    base = digest_c1_authoritative_state(
        runtime_state=runtime_state, follow_intent_state=follow_intent_state,
        service_state=service_state, knowledge_state=knowledge_state,
    )
    if not brace_state.events:
        return base
    return _sha256_bytes(_canonical_bytes({
        "family": "myravant-d1-brace-v8",
        "base": base, "brace": digest_fixture_brace(brace_state),
    }))


def write_d1_checkpoint(*, runtime_state, follow_intent_state, service_state,
                        knowledge_state, brace_state, checkpoint_path,
                        qualification_evidence) -> str:
    if not brace_state.events:
        raise PersistentWorldCheckpointEvidenceError(
            "brace checkpoint requires committed alteration"
        )
    payload = serialize_persistent_world_vsm14_checkpoint_payload(
        runtime_state=runtime_state, follow_intent_state=follow_intent_state,
    )
    payload["components"]["fixture_service"] = serialize_fixture_service(
        service_state
    )
    payload["components"]["actor_situated_knowledge"] = (
        serialize_actor_knowledge(knowledge_state)
    )
    payload["components"]["fixture_brace"] = serialize_fixture_brace(brace_state)
    return _write_envelope(
        envelope={
            "format_identity": COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
            "format_version": D1_VERSION,
            "campaign_identity":
                runtime_state.movement_state.representation.campaign_id,
            "authoritative_payload": payload,
            "integrity_digest": _sha256_bytes(_canonical_bytes(payload)),
            "qualification_provenance":
                _normalize_qualification(qualification_evidence),
        }, checkpoint_path=checkpoint_path,
    )


def restore_d1_checkpoint(*, checkpoint_path, expected_campaign_id,
                          expected_initial_open_states,
                          expected_initial_lit_states,
                          expected_initial_representation,
                          expected_initial_representation_digest):
    envelope = _read_checkpoint_envelope(_checkpoint_path(checkpoint_path))
    payload = _validate_envelope_common(
        envelope=envelope, expected_campaign_id=expected_campaign_id,
        expected_version=D1_VERSION,
    )
    components = _require_exact_dict(
        payload["components"],
        expected_keys={
            *VSM14_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
            "fixture_service", "actor_situated_knowledge", "fixture_brace",
        },
        name="D-1 checkpoint components",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    base_components = {
        k: v for k, v in components.items()
        if k not in {"fixture_service", "actor_situated_knowledge", "fixture_brace"}
    }
    runtime = _restore_base_components(
        components=base_components,
        expected_campaign_id=expected_campaign_id,
        expected_initial_open_states=expected_initial_open_states,
        expected_initial_lit_states=expected_initial_lit_states,
        expected_initial_representation=expected_initial_representation,
        expected_initial_representation_digest=expected_initial_representation_digest,
    )
    follow = _restore_follow_component(components["follow_intent"])
    try:
        service = restore_fixture_service(components["fixture_service"])
        brace = restore_fixture_brace(components["fixture_brace"])
    except (FixtureServiceError, FixtureBraceError) as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "D-1 asset components cannot replay"
        ) from exc
    if not brace.events:
        raise PersistentWorldCheckpointEvidenceError(
            "empty brace history must use v1-v7 checkpoint"
        )
    if service.events:
        _validate_fixture_service_cross_owner(
            service=service, runtime=runtime, follow=follow,
        )
    if service.secured and brace.condition != "attached":
        raise PersistentWorldCheckpointEvidenceError(
            "secured latch has an absent or loosened structural brace"
        )
    all_owners = (
        runtime.movement_state.committed_transitions,
        runtime.committed_custody_transitions,
        runtime.committed_object_state_transitions,
        runtime.committed_object_lit_transitions,
        runtime.committed_storage_transitions,
        runtime.committed_object_displacement_transitions,
        runtime.committed_actor_object_handoff_transitions,
        runtime.logical_time_state.committed_transitions,
        follow.committed_transitions, service.events,
    )
    ids = {event.command_id for transitions in all_owners for event in transitions}
    try:
        knowledge = restore_actor_knowledge(
            components["actor_situated_knowledge"],
            maximum_step=runtime.logical_time_state.logical_position,
            existing_command_ids=ids,
        )
    except ActorKnowledgeError as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "D-1 actor knowledge cannot replay"
        ) from exc
    time_receipts = {
        x.receipt.receipt_id: x.receipt
        for x in runtime.logical_time_state.committed_transitions
    }
    used_times = {
        x.time_receipt_id for x in service.events if x.time_receipt_id
    }
    last_time = -1
    for event in brace.events:
        receipt = time_receipts.get(event.time_receipt_id)
        if (
            event.command_id in ids
            or event.time_receipt_id in used_times
            or receipt is None
            or receipt.pre_position != event.logical_before
            or receipt.post_position != event.logical_after
            or event.logical_before < last_time
            or event.logical_after > runtime.logical_time_state.logical_position
        ):
            raise PersistentWorldCheckpointEvidenceError(
                "brace event lacks unique, causal WORLD-2 time evidence"
            )
        used_times.add(event.time_receipt_id)
        ids.add(event.command_id)
        last_time = event.logical_after
    return runtime, follow, service, knowledge, brace
