"""Carried reach does not establish visual awareness of a satisfied goal."""
from dataclasses import replace

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_continuing_work import WorkTask
from astra_runtime import myravant_actor_knowledge as knowledge
from astra_runtime.domain.persistent_world_actor_evidence import latest
from astra_runtime.domain import persistent_world_actor_participation as participation


def test_dark_carried_clean_surface_does_not_grant_satisfaction_awareness():
    app = ActorApplication.new(fixture=create_actor_fixture())
    actor = identity('oren')
    surface = identity('practice-panel')
    dark = next(p.entity_id for p in app.fixture.place_presentations
                if app.fixture.ambient_visual_condition_for(p.entity_id) == 'insufficient')
    rep = app.state.representation
    # A lawful review context: portable surface in the actor's custody, actor
    # at an existing dark place, conserved residue transferred to the tray.
    relations = tuple(
        replace(r, relation_type='located_at', object_entity_id=dark, semantic_owner='AFQR-18')
        if r.subject_entity_id == actor else
        replace(r, relation_type='carried_by', object_entity_id=actor, semantic_owner='RT-010')
        if r.subject_entity_id == surface else r for r in rep.relations)
    app._runtime_state = replace(app._runtime_state, movement_state=replace(
        app.state, representation=replace(rep, relations=relations)))
    original = dict(app.water_state.adhered)[surface]
    app.water_state = replace(app.water_state, adhered=tuple(
        (key, 0 if key == surface else value + original if key == identity('debris-tray') else value)
        for key, value in app.water_state.adhered))
    app._validate_transaction()
    task = WorkTask('dark-goal-review', actor, 'cleaning', 'wipe',
                    (surface, identity('cleaning-cloth')), dark)
    assert app._task_complete(task)
    assert app._visible_for_actor(actor, surface)  # retained custody/reach qualification
    assert not knowledge._lit(app, actor)
    observed = knowledge.observe(app, app.evidence_state, actor, 'review-observation', 0)
    assert latest(observed, actor, surface, 'residue') is None
    assert not app._goal_visible_complete(task)


def test_player_extinguishes_light_before_prepared_scrub_requalification():
    base = create_actor_fixture()
    profiles = tuple(replace(p, standing_kind=None, standing_method=None,
                             standing_participants=(), standing_place=None)
                     for p in base.actor_profiles)
    app = ActorApplication.new(fixture=create_actor_fixture(actor_profiles=profiles))
    actor, player = identity('oren'), app.fixture.player_entity_id
    surface, brush, lamp = (identity(key) for key in ('practice-panel', 'cleaning-brush', 'lamp'))
    dark = next(p.entity_id for p in app.fixture.place_presentations
                if app.fixture.ambient_visual_condition_for(p.entity_id) == 'insufficient')
    locations = {actor: ('located_at', dark), player: ('located_at', dark),
                 surface: ('carried_by', actor), brush: ('carried_by', actor),
                 lamp: ('carried_by', player)}
    rep = app.state.representation
    relations = tuple(replace(r, relation_type=locations[r.subject_entity_id][0],
                              object_entity_id=locations[r.subject_entity_id][1],
                              semantic_owner='AFQR-18' if locations[r.subject_entity_id][0] == 'located_at' else 'RT-010')
                      if r.subject_entity_id in locations else r for r in rep.relations)
    app._runtime_state = replace(app._runtime_state, movement_state=replace(
        app.state, representation=replace(rep, relations=relations)))
    app._validate_transaction()
    assert app.light_object('lamp').authoritative_changed
    assert knowledge._lit(app, actor)
    accepted = app.request_cleaning('Oren Kesh', 'practice panel',
                                    tool_reference='cleaning brush', method='scrub')
    assert accepted.authoritative_changed, accepted.message
    task = participation.selected(app.participation_state, actor)
    outcome, intent = app._prepare_actor(task)
    assert outcome == 'action' and intent[:2] == ('water', 'scrub')
    material_before = app.water_state
    tick = app.runtime_state.logical_time_state.logical_position
    result = app.extinguish_object('lamp')
    assert result.authoritative_changed, result.message
    assert app.runtime_state.logical_time_state.logical_position == tick + 1
    assert not knowledge._lit(app, actor)
    assert app.water_state == material_before
    task = participation.selected(app.participation_state, actor)
    assert task.status == 'blocked' and task.blocked_due == 1
    assert task.contributions == ()
    assert not any(event[1] == 'physical_contribution' and event[2] == actor
                   for event in app.actor_events)
