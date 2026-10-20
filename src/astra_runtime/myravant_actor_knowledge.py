"""Shared player/NPC lawful evidence admission and local communication routes.

This adapter consumes existing spatial and sensing qualifications. Its private
history records what was admitted then; reports never refresh from world truth.
"""
from hashlib import sha256
import json
from astra_runtime.domain import persistent_world_actor_evidence as evidence
from astra_runtime.domain.persistent_world_material import placement

FACETS = frozenset(('residue', 'moisture', 'placement', 'assembly', 'trace', 'activity'))


def _identity(parts):
    return 'actor-evidence-' + sha256(json.dumps(parts, sort_keys=True, default=str).encode()).hexdigest()[:32]


def _lit(app, actor_id):
    place = app._actor_place_id(actor_id)
    return (app.fixture.ambient_visual_condition_for(place) == 'sufficient'
            or app._actor_local_light_available(actor_id))


def observe(app, state, actor_id, receipt_id, tick):
    """Admit only declared facets of objects visible to this actor now."""
    app._actor_place_id(actor_id)
    # Carried-object reach alone does not prove visual access in darkness.
    if not _lit(app, actor_id):
        return state
    water = dict(app.water_state.water)
    adhered = dict(app.water_state.adhered)
    suspended = dict(app.water_state.suspended)
    deposits = dict(app.environment_state.deposits)
    admitted = []
    for presentation in app.fixture.object_presentations:
        obj = presentation.entity_id
        if not app._visible_for_actor(actor_id, obj):
            continue
        facets = []
        if obj in water:
            facets.append(('moisture', 'wet' if water[obj] else 'dry'))
        if obj in adhered or obj in deposits or obj in suspended:
            facets.append(('residue', 'present' if adhered.get(obj, 0) + deposits.get(obj, 0) + suspended.get(obj, 0) else 'clear'))
        relation = placement(app.state.representation, obj)
        # Do not expose a hidden carrier, container or support identity.
        if relation.relation_type == 'located_at' or relation.object_entity_id == actor_id or app._visible_for_actor(actor_id, relation.object_entity_id):
            facets.append(('placement', (relation.relation_type, relation.object_entity_id)))
        for assembly in app.fixture.assemblies:
            members = (assembly.left, assembly.right, assembly.fastener)
            if obj != assembly.left or not all(app._visible_for_actor(actor_id, member) for member in members):
                continue
            connections = getattr(app, 'connections', ())
            joined = any((c.left, c.right, c.fastener, c.method) == (*members, assembly.method) for c in connections)
            supports = ((assembly.left, assembly.support_left),) + (((assembly.right, assembly.support_right),) if assembly.support_right else ())
            supported = all(placement(app.state.representation, child).relation_type == 'supported_by'
                            and placement(app.state.representation, child).object_entity_id == support
                            for child, support in supports)
            facets.append(('assembly', (assembly.name, 'joined' if joined and supported else 'separate')))
        traces = tuple(sorted({trace.kind for trace in app.environment_state.traces if trace.subject == obj}))
        if traces:
            facets.append(('trace', traces))
        for facet, value in facets:
            event = evidence.EvidenceEvent(_identity((actor_id, obj, facet, value, receipt_id, tick)),
                actor_id, 'witnessed', actor_id, obj, facet, value, tick, receipt_id,
                'local-visible-object-and-declared-facet')
            admitted.append(event)
    return evidence.record_many(state, tuple(admitted), qualified=True)


def performed(state, actor_id, target_id, facet, value, receipt_id, tick):
    """Admit caller-owned committed performance, never another actor's action."""
    if facet not in FACETS:
        raise ValueError('facet is outside the admitted actor-evidence profile')
    event = evidence.EvidenceEvent(_identity((actor_id, 'performed', target_id, facet, value, receipt_id, tick)),
        actor_id, 'performed', actor_id, target_id, facet, value, tick, receipt_id,
        'actor-owned-committed-contribution')
    return evidence.record(state, event, qualified=True)


def communication_route(app, speaker, listener, communication_class):
    """Qualify this package's declared local visual communication route only."""
    try:
        return (speaker != listener
            and communication_class in app.actor_profile(speaker).communication_classes
            and communication_class in app.actor_profile(listener).communication_classes
            and app._actor_place_id(speaker) == app._actor_place_id(listener)
            and _lit(app, speaker) and _lit(app, listener)
            and placement(app.state.representation, speaker).relation_type == 'located_at'
            and placement(app.state.representation, listener).relation_type == 'located_at')
    except (ValueError, AttributeError):
        return False


def report(state, speaker, listener, target_id, facet, receipt_id, tick, *, qualified):
    """Transfer historical evidence with explicit attribution, never live refresh.

    The reported value includes its original observation tick and evidence kind;
    the event tick records delivery. The retained source remains the speaker.
    """
    if type(qualified) is not bool or not qualified:
        raise ValueError('local communication must be explicitly qualified')
    if facet not in FACETS:
        raise ValueError('facet is outside the admitted actor-evidence profile')
    original = evidence.latest(state, speaker, target_id, facet)
    if original is None:
        return state
    event = evidence.EvidenceEvent(_identity((speaker, listener, target_id, facet, receipt_id, tick)),
        listener, 'reported', speaker, target_id, facet, original.value, tick, receipt_id,
        'qualified-local-delivery', origin_tick=original.origin_tick if original.origin_tick is not None else original.tick,
        source_event_id=original.event_id)
    return evidence.record(state, event, qualified=True)
