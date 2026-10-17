"""Opt-in v11 posture component and AFQR-16/19 movement evidence joins.

Legacy histories keep their existing digest and writer. v11 reuses existing
owner replay and adds checks against placement prestates, not a second world.
"""
from __future__ import annotations

from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMPONENT_CHECKPOINT_FORMAT_IDENTITY, _validate_envelope_common, _write_envelope,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError, _canonical_bytes, _checkpoint_path,
    _normalize_qualification, _read_checkpoint_envelope, _sha256_bytes,
)
from astra_runtime.domain.persistent_world_vsm14_checkpoint import (
    serialize_persistent_world_vsm14_checkpoint_payload,
)
from astra_runtime.domain.persistent_world_object_open_close import serialize_fixture_service
from astra_runtime.myravant_actor_situated_knowledge import serialize_actor_knowledge
from astra_runtime.myravant_fixture_brace import serialize_fixture_brace
from astra_runtime.myravant_e1_latch_duty import serialize_fixture_duty
from astra_runtime.myravant_e1_checkpoint import digest_e2_authoritative_state, _restore_e1_payload
from astra_runtime.myravant_posture import (
    PostureError, digest_posture, restore_posture, serialize_posture,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.domain.persistent_world_movement_integration import (
    fingerprint_persistent_world_movement_command,
    digest_persistent_world_entity_location_representation,
    replay_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import replay_persistent_world_object_custody
from astra_runtime.domain.persistent_world_object_storage_transfer import replay_persistent_world_object_storage
from astra_runtime.domain.persistent_world_object_displacement import replay_persistent_world_object_displacement
from astra_runtime.domain.persistent_world_actor_object_handoff import replay_persistent_world_actor_object_handoff

POSTURE_CHECKPOINT_VERSION = 11


def has_posture_movement(runtime):
    return any(":posture-opportunity-" in t.receipt.opportunity_evidence_id
               for t in runtime.movement_state.committed_transitions)


def digest_posture_authoritative_state(*, posture_state, **kwargs):
    base = digest_e2_authoritative_state(**kwargs)
    if not posture_state.events:
        return base
    return _sha256_bytes(_canonical_bytes({
        "family": "myravant-posture-v11", "base": base,
        "posture": digest_posture(posture_state),
        "provenance": serialize_posture(posture_state),
    }))


def write_posture_checkpoint(
    *, runtime_state, follow_intent_state, service_state, knowledge_state,
    brace_state, duty_state, posture_state, checkpoint_path, qualification_evidence,
):
    if not posture_state.events:
        raise PersistentWorldCheckpointEvidenceError("v11 requires recorded posture")
    payload = serialize_persistent_world_vsm14_checkpoint_payload(
        runtime_state=runtime_state, follow_intent_state=follow_intent_state,
    )
    payload["components"].update(
        fixture_service=serialize_fixture_service(service_state),
        actor_situated_knowledge=serialize_actor_knowledge(knowledge_state),
        fixture_brace=serialize_fixture_brace(brace_state),
        fixture_duty=serialize_fixture_duty(duty_state),
        actor_posture=serialize_posture(posture_state),
    )
    return _write_envelope(envelope={
        "format_identity": COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
        "format_version": POSTURE_CHECKPOINT_VERSION,
        "campaign_identity": runtime_state.movement_state.representation.campaign_id,
        "authoritative_payload": payload,
        "integrity_digest": _sha256_bytes(_canonical_bytes(payload)),
        "qualification_provenance": _normalize_qualification(qualification_evidence),
    }, checkpoint_path=checkpoint_path)


def _placement_prestates(runtime, initial):
    """Replay the already validated placement chain, retaining owner join points."""
    families = (
        (runtime.movement_state.committed_transitions, replay_persistent_world_movement),
        (runtime.committed_custody_transitions, replay_persistent_world_object_custody),
        (runtime.committed_storage_transitions, replay_persistent_world_object_storage),
        (runtime.committed_object_displacement_transitions, replay_persistent_world_object_displacement),
        (runtime.committed_actor_object_handoff_transitions, replay_persistent_world_actor_object_handoff),
    )
    outgoing = {}
    for transitions, replay in families:
        for t in transitions:
            if t.receipt.pre_state_digest in outgoing:
                raise PersistentWorldCheckpointEvidenceError("ambiguous posture placement anchor")
            outgoing[t.receipt.pre_state_digest] = (t, replay)
    representation = initial
    count = 0
    snapshots = {}
    movement_prestates = {}
    for _ in range(len(outgoing) + 1):
        digest = digest_persistent_world_entity_location_representation(representation)
        snapshots[(digest, count)] = representation
        if digest not in outgoing:
            break
        t, replay = outgoing[digest]
        if replay is replay_persistent_world_movement:
            movement_prestates[t.command_id] = (representation, count)
            count += 1
        if replay is replay_persistent_world_object_storage:
            representation = replay(representation=representation, receipt=t.receipt)
        else:
            representation = replay(pre_state_representation=representation, receipt=t.receipt)
    if len(movement_prestates) != len(runtime.movement_state.committed_transitions):
        raise PersistentWorldCheckpointEvidenceError("incomplete posture placement chain")
    return snapshots, movement_prestates


def _validate_posture_joins(*, runtime, posture, fixture):
    snapshots, movement_prestates = _placement_prestates(runtime, fixture.initial_state.representation)
    for event in posture.events:
        representation = snapshots.get((event.representation_digest, event.movement_count))
        if (
            representation is None
            or event.logical_step > runtime.logical_time_state.logical_position
            or not any(r.relation_type == "located_at"
                       and r.subject_entity_id == event.actor_id
                       and r.object_entity_id == event.place_id
                       for r in representation.relations)
        ):
            raise PostureError("posture lacks its actual placement or time anchor")
    for t in runtime.movement_state.committed_transitions:
        receipt = t.receipt
        reserved = ":posture-opportunity-" in receipt.opportunity_evidence_id
        representation, count = movement_prestates[t.command_id]
        eligible = [e for e in posture.events if e.movement_count <= count]
        if receipt.actor_entity_id != fixture.player_entity_id:
            if reserved:
                raise PostureError("NPC movement cannot inherit player posture")
            continue
        if not eligible:
            if reserved:
                raise PostureError("movement has no preceding posture provenance")
            continue
        if not t.command_id.startswith("terminal-move-"):
            if reserved:
                raise PostureError("unrecognized posture movement producer")
            continue
        event = eligible[-1]
        routes = [r for r in fixture.movement_routes
                  if r.source_place_id == receipt.source_place_id
                  and r.destination_place_id == receipt.destination_place_id]
        if len(routes) != 1:
            raise PostureError("posture movement route is ambiguous")
        direction = routes[0].direction
        matches = 0
        for method in ("walk", "crawl"):
            qualified = fixture.posture_movement_qualified(
                event=event, source_place_id=receipt.source_place_id,
                direction=direction, method=method, representation=representation,
            )
            _, opportunity = fixture.movement_evidence(
                command_id=t.command_id, source_place_id=receipt.source_place_id,
                direction=direction, destination_place_id=receipt.destination_place_id,
                representation=representation, method=method,
                posture_event=event if qualified else None,
            )
            metadata = {"client": "myravant-terminal-g1"}
            if method != "walk":
                metadata["traversal_method"] = method
            if qualified:
                metadata["posture_receipt_id"] = event.receipt_id
            command = create_command_envelope(
                command_id=t.command_id, command_type="move",
                source_actor_id=fixture.player_entity_id,
                payload={"destination_entity_id": receipt.destination_place_id},
                metadata=metadata,
            )
            matches += bool(
                opportunity.opportunity_available
                and opportunity.evidence_id == receipt.opportunity_evidence_id
                and fingerprint_persistent_world_movement_command(command) == t.command_fingerprint
            )
        if matches != 1:
            raise PostureError("movement posture reference, opportunity or fingerprint differs")


def restore_posture_checkpoint(*, checkpoint_path, fixture):
    envelope = _read_checkpoint_envelope(_checkpoint_path(checkpoint_path))
    payload = _validate_envelope_common(
        envelope=envelope, expected_campaign_id=fixture.campaign_id,
        expected_version=POSTURE_CHECKPOINT_VERSION,
    )
    if type(payload["components"]) is not dict:
        raise PersistentWorldCheckpointEvidenceError("v11 components must be an object")
    components = dict(payload["components"])
    if "actor_posture" not in components:
        raise PersistentWorldCheckpointEvidenceError("v11 posture component missing")
    material = components.pop("actor_posture")
    values = _restore_e1_payload(
        payload={**payload, "components": components}, checkpoint_version=POSTURE_CHECKPOINT_VERSION,
        expected_campaign_id=fixture.campaign_id,
        expected_initial_open_states=fixture.initial_object_open_states,
        expected_initial_lit_states=fixture.initial_object_lit_states,
        expected_initial_representation=fixture.initial_state.representation,
        expected_initial_representation_digest=fixture.provenance.initial_state_digest,
    )
    try:
        posture = restore_posture(material, profile=fixture.posture_profile)
        runtime, follow, service, knowledge, brace, duty = values
        owners = (
            runtime.movement_state.committed_transitions,
            runtime.committed_custody_transitions, runtime.committed_object_state_transitions,
            runtime.committed_object_lit_transitions, runtime.committed_storage_transitions,
            runtime.committed_object_displacement_transitions,
            runtime.committed_actor_object_handoff_transitions,
            runtime.logical_time_state.committed_transitions, follow.committed_transitions,
            service.events, knowledge.events, brace.events, duty.events,
        )
        existing_ids = {e.command_id for family in owners for e in family}
        if any(e.command_id in existing_ids for e in posture.events):
            raise PostureError("posture command collides with another owner")
        _validate_posture_joins(runtime=runtime, posture=posture, fixture=fixture)
    except (PostureError, TypeError, ValueError) as exc:
        raise PersistentWorldCheckpointEvidenceError("posture component or movement joins cannot replay") from exc
    return values, posture
