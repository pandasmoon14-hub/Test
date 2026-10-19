"""Clock-free actor preparation through retained physical owners (#548).

This adapter supplies current opportunity, not participation or scheduling.
The caller authorizes the actor's intention and owns the enclosing transaction.
"""
from dataclasses import replace

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.domain.persistent_world_material import placement, constrained, active_effects, digest
from astra_runtime.domain.persistent_world_movement_integration import execute_persistent_world_movement
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    create_custody_qualification_evidence, create_custody_opportunity_evidence,
    execute_persistent_world_object_custody,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    create_object_open_close_qualification_evidence, create_object_open_close_opportunity_evidence,
    execute_persistent_world_object_open_close,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    create_object_storage_qualification_evidence, create_object_storage_opportunity_evidence,
    execute_persistent_world_object_storage,
)
from astra_runtime.domain.persistent_world_actor_object_handoff import (
    create_actor_object_handoff_qualification_evidence, create_actor_object_handoff_spatial_evidence,
    create_actor_object_handoff_opportunity_evidence, execute_persistent_world_actor_object_handoff,
)
from astra_runtime.domain import persistent_world_runtime_composition as composition
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id


def execute_actor_physical(app, actor_id, operation, *ids):
    """Execute one qualified primitive using IDs, without advancing logical time."""
    pre = app.authoritative_digest()
    try:
        here = app._actor_place_id(actor_id)
        arities = {'move': 1, 'pickup': 1, 'drop': 1, 'open': 1, 'close': 1,
                   'retrieve': 2, 'store': 2, 'give': 2}
        if operation not in arities or len(ids) != arities[operation] or any(type(x) is not str for x in ids):
            raise ValueError('That preparation method is not qualified.')
        token = digest([pre, actor_id, operation, ids])[:28]
        command_id = 'actor-physical-' + token
        evidence = lambda suffix: build_record_id('evidence', 'actor-physical-' + token + '-' + suffix)
        common = {'actor_entity_id': actor_id}
        state_digest = app.representation_digest()
        observation_id = None
        if operation == 'move':
            destination = ids[0]
            routes = [r for r in app.fixture.movement_routes
                      if r.source_place_id == here and r.destination_place_id == destination]
            if len(routes) != 1:
                raise ValueError('No single declared passage reaches that place.')
            route = routes[0]
            if any(e.kind == 'movement' and e.source == here and e.direction == route.direction
                   for e in active_effects(app.state.representation, app.connections, app.material_profile)):
                raise ValueError('An assembled barrier obstructs that passage.')
            spatial, opportunity = app.fixture.movement_evidence(
                command_id=command_id, source_place_id=here, direction=route.direction,
                destination_place_id=destination, representation=app.state.representation)
            spatial = replace(spatial, actor_entity_id=actor_id)
            opportunity = replace(opportunity, actor_entity_id=actor_id)
            command_type, payload = 'move', {'destination_entity_id': destination}
            execute, state, install = execute_persistent_world_movement, app.state, 'movement'
            kwargs = {'spatial_evidence': spatial, 'opportunity_evidence': opportunity}
        else:
            obj = ids[0]
            if not any(p.entity_id == obj for p in app.fixture.object_presentations):
                raise ValueError('That object is unavailable.')
            r = placement(app.state.representation, obj)
            held = r.relation_type == 'carried_by' and r.object_entity_id == actor_id
            if operation in {'pickup', 'drop', 'retrieve', 'store', 'give'} and constrained(app.state.representation, app.connections, obj):
                raise ValueError('Remove the material relationship before transferring the object.')
            common.update(object_entity_id=obj, operation=operation)
            if operation in {'pickup', 'drop'}:
                if operation == 'pickup':
                    if obj in app.fixture.fixed_object_ids:
                        raise ValueError('That fixed object has no qualified pickup method.')
                    if r.relation_type != 'located_at' or r.object_entity_id != here or not app._visible_for_actor(actor_id, obj):
                        raise ValueError('The pickup target is not accessible.')
                    observation = app.fixture._qualified_visual_evidence(
                        observer_entity_id=actor_id, target_entity_id=obj, place_id=here,
                        local_light_available=app._actor_local_light_available(actor_id),
                        evidence_prefix='actor-physical-visual')
                    observation_id = observation.evidence_id
                elif not held:
                    raise ValueError('The actor is not carrying that object.')
                qualification = create_custody_qualification_evidence(evidence_id=evidence('qualification'), qualified=True, **common)
                opportunity = create_custody_opportunity_evidence(evidence_id=evidence('opportunity'), opportunity_available=True,
                    resolution_accepted=True, input_evidence_refs=(observation_id,) if observation_id else (), **common)
                command_type, payload = operation + '_object', {'object_entity_id': obj}
                execute, state, install = execute_persistent_world_object_custody, app.custody_state, 'custody'
            elif operation in {'open', 'close'}:
                if not app._visible_for_actor(actor_id, obj):
                    raise ValueError('The closure is not accessible.')
                current = app.object_open_state(obj)
                if current is None or current.state == ('open' if operation == 'open' else 'closed'):
                    raise ValueError('That closure cannot make this transition.')
                qualification = create_object_open_close_qualification_evidence(evidence_id=evidence('qualification'), qualified=True, **common)
                opportunity = create_object_open_close_opportunity_evidence(evidence_id=evidence('opportunity'), opportunity_available=True, resolution_accepted=True, **common)
                command_type, payload = operation + '_object', {'object_entity_id': obj}
                execute, state, install = execute_persistent_world_object_open_close, app.object_state, 'open_close'
                state_digest = app.object_state_digest()
            elif operation in {'retrieve', 'store'}:
                container = ids[1]
                if not app._actor_container_accessible(actor_id, container) or not app._visible_for_actor(actor_id, container):
                    raise ValueError('The container is not accessible.')
                opened = app.object_open_state(container)
                if opened is None or opened.state != 'open':
                    raise ValueError('The container must be open.')
                if (operation == 'store' and not held) or (operation == 'retrieve' and
                        (r.relation_type != 'contained_by' or r.object_entity_id != container or not app._visible_for_actor(actor_id, obj))):
                    raise ValueError('That transfer is not available from current custody.')
                common.update(container_entity_id=container, operation='store' if operation == 'store' else 'retrieve')
                qualification = create_object_storage_qualification_evidence(evidence_id=evidence('qualification'), qualified=True, **common)
                opportunity = create_object_storage_opportunity_evidence(evidence_id=evidence('opportunity'), opportunity_available=True, resolution_accepted=True, **common)
                command_type = 'transfer_to_container' if operation == 'store' else 'transfer_from_container'
                payload = {'object_entity_id': obj, 'container_entity_id': container}
                execute, state, install = execute_persistent_world_object_storage, app.storage_state, 'storage'
            else:
                recipient = ids[1]
                if not held or recipient == actor_id or app._actor_place_id(recipient) != here:
                    raise ValueError('A handoff needs carried custody and a local recipient.')
                handoff = {'source_actor_entity_id': actor_id, 'recipient_actor_entity_id': recipient,
                           'object_entity_id': obj, 'method': 'handoff'}
                qualification = create_actor_object_handoff_qualification_evidence(evidence_id=evidence('qualification'), qualified=True, **handoff)
                spatial = create_actor_object_handoff_spatial_evidence(evidence_id=evidence('spatial'), place_id=here, spatially_permitted=True, **handoff)
                opportunity = create_actor_object_handoff_opportunity_evidence(evidence_id=evidence('opportunity'), place_id=here, opportunity_available=True, resolution_accepted=True, **handoff)
                command_type, payload = 'transfer_object', {'object_entity_id': obj, 'recipient_actor_entity_id': recipient, 'method': 'handoff'}
                execute, state, install = execute_persistent_world_actor_object_handoff, app.handoff_state, 'actor_object_handoff'
            kwargs = {'qualification_evidence': qualification, 'opportunity_evidence': opportunity}
            if operation == 'give':
                kwargs['spatial_evidence'] = spatial
        command = create_command_envelope(command_id=command_id, command_type=command_type,
            source_actor_id=actor_id, payload=payload, metadata={'package': 'PLAY-TARROW-ACTORS-1'})
        result = execute(state=state, command=command, expected_pre_state_digest=state_digest, **kwargs)
        app._runtime_state = getattr(composition, 'replace_persistent_world_runtime_' + install + '_state')(
            state=app._runtime_state, **{install + '_state' if install != 'actor_object_handoff' else 'handoff_state': result.state})
        return PlayApplicationResult(result_type='actor_physical_committed', message=operation.capitalize() + ' completed.',
            authoritative_changed=True, command_id=command_id, command_fingerprint=result.receipt.command_fingerprint,
            receipt_id=result.receipt.receipt_id, preview_id=result.preview.preview_id, state_delta_id=result.state_delta.delta_id,
            opportunity_evidence_id=result.receipt.opportunity_evidence_id, observation_evidence_id=observation_id,
            pre_state_digest=pre, post_state_digest=app.authoritative_digest(), technical_retry=result.technical_retry)
    except ValueError as exc:
        return PlayApplicationResult(result_type='actor_physical_rejected', message=str(exc), failure_class='actor_physical_opportunity_unavailable',
            pre_state_digest=pre, post_state_digest=pre)
