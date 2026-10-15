"""PLAY-E1 opt-in checkpoint v9 for fixture-specific NPC latch duty.

v1-v8 are never rewritten. This adapter reconstructs existing owners through
their established replay paths, then validates new E1 commitment/service joins.
It is not a replacement general-purpose checkpoint authority.
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
    serialize_persistent_world_vsm14_checkpoint_payload,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    FixtureServiceError, restore_fixture_service, serialize_fixture_service,
)
from astra_runtime.myravant_actor_situated_knowledge import (
    ActorKnowledgeError, restore_actor_knowledge, serialize_actor_knowledge,
)
from astra_runtime.myravant_fixture_brace import (
    FixtureBraceError, restore_fixture_brace, serialize_fixture_brace,
)
from astra_runtime.myravant_d1_checkpoint import digest_d1_authoritative_state
from astra_runtime.myravant_e1_latch_duty import (
    FixtureDutyError, FixtureDutyState,
    digest_fixture_duty, restore_fixture_duty, serialize_fixture_duty,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, PLAYER_ID, TOOL_CHEST_ID, YARD_ID, WORKSHOP_ID,
    ORCHARD_PATH_ID,
)

E1_VERSION = 9


def digest_e1_authoritative_state(
    *, runtime_state, follow_intent_state, service_state,
    knowledge_state, brace_state, duty_state: FixtureDutyState,
) -> str:
    base = digest_d1_authoritative_state(
        runtime_state=runtime_state, follow_intent_state=follow_intent_state,
        service_state=service_state, knowledge_state=knowledge_state,
        brace_state=brace_state,
    )
    if not duty_state.events:
        return base
    return _sha256_bytes(_canonical_bytes({
        "family": "myravant-e1-latch-duty-v9",
        "base": base, "duty": digest_fixture_duty(duty_state),
    }))


def write_e1_checkpoint(
    *, runtime_state, follow_intent_state, service_state,
    knowledge_state, brace_state, duty_state, checkpoint_path,
    qualification_evidence,
) -> str:
    if not duty_state.events:
        raise PersistentWorldCheckpointEvidenceError(
            "v9 requires a committed fixture duty"
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
    payload["components"]["fixture_duty"] = serialize_fixture_duty(duty_state)
    return _write_envelope(
        envelope={
            "format_identity": COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
            "format_version": E1_VERSION,
            "campaign_identity":
                runtime_state.movement_state.representation.campaign_id,
            "authoritative_payload": payload,
            "integrity_digest": _sha256_bytes(_canonical_bytes(payload)),
            "qualification_provenance":
                _normalize_qualification(qualification_evidence),
        }, checkpoint_path=checkpoint_path,
    )


def restore_e1_checkpoint(
    *, checkpoint_path, expected_campaign_id, expected_initial_open_states,
    expected_initial_lit_states, expected_initial_representation,
    expected_initial_representation_digest,
):
    envelope = _read_checkpoint_envelope(_checkpoint_path(checkpoint_path))
    payload = _validate_envelope_common(
        envelope=envelope, expected_campaign_id=expected_campaign_id,
        expected_version=E1_VERSION,
    )
    components = _require_exact_dict(
        payload["components"],
        expected_keys={
            *VSM14_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
            "fixture_service", "actor_situated_knowledge",
            "fixture_brace", "fixture_duty",
        },
        name="E1 checkpoint components",
        error_cls=PersistentWorldCheckpointEvidenceError,
    )
    base_components = {
        k: v for k, v in components.items()
        if k not in {
            "fixture_service", "actor_situated_knowledge",
            "fixture_brace", "fixture_duty",
        }
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
        duty = restore_fixture_duty(components["fixture_duty"])
    except (FixtureServiceError, FixtureBraceError, FixtureDutyError) as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "E1 owner-local histories cannot replay"
        ) from exc

    physical_owners = (
        runtime.movement_state.committed_transitions,
        runtime.committed_custody_transitions,
        runtime.committed_object_state_transitions,
        runtime.committed_object_lit_transitions,
        runtime.committed_storage_transitions,
        runtime.committed_object_displacement_transitions,
        runtime.committed_actor_object_handoff_transitions,
        runtime.logical_time_state.committed_transitions,
        follow.committed_transitions,
    )
    ids = {x.command_id for family in physical_owners for x in family}
    time_receipts = {
        t.receipt.receipt_id: t.receipt
        for t in runtime.logical_time_state.committed_transitions
    }
    used_work_ticks = set()
    npc_services = {}
    previous_service_step = -1
    for event in service.events:
        if (
            event.command_id in ids
            or event.target_id != TOOL_CHEST_ID
            or event.logical_before < previous_service_step
            or event.logical_after > runtime.logical_time_state.logical_position
        ):
            raise PersistentWorldCheckpointEvidenceError(
                "E1 service lacks distinct, chronological owner identity"
            )
        ids.add(event.command_id)
        previous_service_step = event.logical_after
        if event.actor_id == PLAYER_ID:
            if (
                event.operation == "release"
                and event.place_id not in {YARD_ID, WORKSHOP_ID, ORCHARD_PATH_ID}
            ) or (
                event.operation != "release" and event.place_id != YARD_ID
            ):
                raise PersistentWorldCheckpointEvidenceError(
                    "E1 player service escaped fixture"
                )
        elif event.actor_id == GROUNDSKEEPER_ID:
            if (
                event.operation != "secure" or event.method != "none"
                or event.place_id != YARD_ID
                or event.logical_before != event.logical_after
            ):
                raise PersistentWorldCheckpointEvidenceError(
                    "E1 NPC service action is not a licensed latch duty"
                )
            npc_services[event.receipt_id] = event
        else:
            raise PersistentWorldCheckpointEvidenceError(
                "E1 unlicensed service actor"
            )
        if event.operation == "work":
            tick = time_receipts.get(event.time_receipt_id)
            if (
                tick is None
                or tick.pre_position != event.logical_before
                or tick.post_position != event.logical_after
                or event.time_receipt_id in used_work_ticks
            ):
                raise PersistentWorldCheckpointEvidenceError(
                    "E1 work has no unique WORLD-2 tick"
                )
            used_work_ticks.add(event.time_receipt_id)
    try:
        knowledge = restore_actor_knowledge(
            components["actor_situated_knowledge"],
            maximum_step=runtime.logical_time_state.logical_position,
            existing_command_ids=ids,
        )
    except ActorKnowledgeError as exc:
        raise PersistentWorldCheckpointEvidenceError(
            "E1 actor knowledge cannot replay"
        ) from exc
    ids.update(x.command_id for x in knowledge.events)

    last_brace_step = -1
    for event in brace.events:
        tick = time_receipts.get(event.time_receipt_id)
        if (
            event.command_id in ids
            or event.time_receipt_id in used_work_ticks
            or tick is None
            or tick.pre_position != event.logical_before
            or tick.post_position != event.logical_after
            or event.logical_before < last_brace_step
            or event.logical_after > runtime.logical_time_state.logical_position
        ):
            raise PersistentWorldCheckpointEvidenceError(
                "E1 brace cannot join distinct WORLD-2 evidence"
            )
        ids.add(event.command_id)
        used_work_ticks.add(event.time_receipt_id)
        last_brace_step = event.logical_after

    fulfilled_services = set()
    latest_request_step = None
    for event in duty.events:
        if (
            event.command_id in ids
            or event.logical_step > runtime.logical_time_state.logical_position
        ):
            raise PersistentWorldCheckpointEvidenceError(
                "E1 duty identity or time collides with existing owners"
            )
        ids.add(event.command_id)
        if event.operation == "request":
            latest_request_step = event.logical_step
        if event.operation == "fulfill":
            service_event = npc_services.get(event.service_receipt_id)
            tick = time_receipts.get(event.time_receipt_id)
            if (
                service_event is None or tick is None
                or latest_request_step is None
                # Fulfilling a duty requires a fresh advancement, not an
                # earlier receipt relabeled as a later NPC consequence.
                or tick.pre_position < latest_request_step
                or tick.post_position <= latest_request_step
                or event.time_receipt_id in used_work_ticks
                or tick.post_position != event.logical_step
                or service_event.logical_after != event.logical_step
                or event.service_receipt_id in fulfilled_services
            ):
                raise PersistentWorldCheckpointEvidenceError(
                    "E1 fulfillment has no causal NPC service and WORLD-2 tick"
                )
            used_work_ticks.add(event.time_receipt_id)
            fulfilled_services.add(event.service_receipt_id)
    if set(npc_services) != fulfilled_services:
        raise PersistentWorldCheckpointEvidenceError(
            "E1 NPC service lacks a voluntary committed duty"
        )
    if service.secured and brace.condition != "attached":
        raise PersistentWorldCheckpointEvidenceError(
            "E1 secured chest has incompatible brace condition"
        )
    return runtime, follow, service, knowledge, brace, duty
