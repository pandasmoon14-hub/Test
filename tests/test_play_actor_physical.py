"""Real actor preparation uses retained owners with no player substitution."""
from dataclasses import replace

import pytest

from astra_runtime.myravant_actor_physical import execute_actor_physical
from astra_runtime.myravant_water_application import WaterApplication
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_material import placement


def act(app, operation, *keys, actor='oren'):
    result = execute_actor_physical(app, identity(actor), operation, *(identity(k) for k in keys))
    assert result.authoritative_changed, result.message
    assert result.receipt_id and result.command_fingerprint
    return result


def test_actor_walk_pickup_drop_without_clock_or_selected_player_change():
    app = WaterApplication.new()
    player = app.fixture.player_entity_id
    player_place = app.current_place_id()
    profile = app.material_profile
    act(app, 'move', 'work-bench')
    result = act(app, 'pickup', 'cleaning-cloth')
    assert result.observation_evidence_id
    assert placement(app.state.representation, identity('cleaning-cloth')).object_entity_id == identity('oren')
    act(app, 'drop', 'cleaning-cloth')
    assert placement(app.state.representation, identity('cleaning-cloth')).object_entity_id == identity('work-bench')
    assert app.fixture.player_entity_id == player and app.current_place_id() == player_place
    assert app.material_profile == profile
    assert not app.journal


@pytest.mark.parametrize('operation,keys', [
    ('move', ('notice-recess',)), ('pickup', ('cleaning-cloth',)),
    ('drop', ('cleaning-cloth',)), ('open', ('document-box',)),
    ('give', ('cleaning-cloth', 'mira')), ('bad', ('cleaning-cloth',)),
])
def test_unqualified_actor_preparation_never_mutates(operation, keys):
    app = WaterApplication.new()
    before = app.authoritative_digest()
    result = execute_actor_physical(app, identity('oren'), operation, *(identity(k) for k in keys))
    assert result.failure_class and not result.authoritative_changed
    assert app.authoritative_digest() == before


def test_actor_storage_and_local_handoff():
    app = WaterApplication.new()
    actor = identity('mira')
    # At the common room, travel along real edges to the notice recess.
    for key in ('common-threshold', 'notice-recess'):
        act(app, 'move', key, actor='mira')
    act(app, 'pickup', 'screen-cloth', actor='mira')
    act(app, 'open', 'document-box', actor='mira')
    act(app, 'store', 'screen-cloth', 'document-box', actor='mira')
    act(app, 'close', 'document-box', actor='mira')
    before = app.authoritative_digest()
    assert not execute_actor_physical(app, actor, 'retrieve', identity('screen-cloth'), identity('document-box')).authoritative_changed
    assert app.authoritative_digest() == before
    act(app, 'open', 'document-box', actor='mira')
    act(app, 'retrieve', 'screen-cloth', 'document-box', actor='mira')
    # Place the selected player with the actor solely as test fixture setup.
    rep = app.state.representation
    app._runtime_state = replace(app._runtime_state, movement_state=replace(app.state, representation=replace(rep,
        relations=tuple(replace(r, object_entity_id=identity('notice-recess')) if r.subject_entity_id == app.fixture.player_entity_id else r for r in rep.relations))))
    result = execute_actor_physical(app, actor, 'give', identity('screen-cloth'), app.fixture.player_entity_id)
    assert result.authoritative_changed, result.message
    assert placement(app.state.representation, identity('screen-cloth')).object_entity_id == app.fixture.player_entity_id


def test_actor_cannot_pick_up_supported_material_or_walk_through_barrier():
    app = WaterApplication.new()
    # Player assembles the existing barrier through ordinary retained methods.
    for direction in ('south', 'west'):
        assert app.move(direction).authoritative_changed
    for name in ('barrier board', 'barrier crossbar'):
        assert app.pickup(name).authoritative_changed
        assert app.material('put_on', name, 'yard work trestle').authoritative_changed
    assert app.pickup('barrier cord').authoritative_changed
    assert app.material('tie', 'barrier board', 'barrier crossbar', 'barrier cord').authoritative_changed
    act(app, 'move', 'yard-tools', actor='tali')
    before = app.authoritative_digest()
    assert not execute_actor_physical(app, identity('tali'), 'pickup', identity('barrier-board')).authoritative_changed
    effect = next(e for e in app.material_profile.effects if e.kind == 'movement' and e.source == identity('yard-tools'))
    route = next(r for r in app.fixture.movement_routes if r.source_place_id == effect.source and r.direction == effect.direction)
    result = execute_actor_physical(app, identity('tali'), 'move', route.destination_place_id)
    assert result.failure_class and not result.authoritative_changed
    assert app.authoritative_digest() == before


def test_actor_cannot_pick_up_declared_fixed_objects():
    app = WaterApplication.new()
    act(app, 'move', 'work-bench')
    before = app.authoritative_digest()
    result = execute_actor_physical(app, identity('oren'), 'pickup', identity('bench'))
    assert result.failure_class and not result.authoritative_changed
    assert app.authoritative_digest() == before
