"""Actor-qualified owner calls preserve legacy defaults and use actual opportunity."""
from dataclasses import replace

import pytest

from astra_runtime.domain.persistent_world_material import placement, digest
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_water_application import WaterApplication


def relocate(app, key, target, kind='located_at'):
    rep = app.state.representation
    obj = identity(key)
    old = placement(rep, obj)
    rel = replace(old, relation_type=kind, object_entity_id=identity(target),
                  semantic_owner='RT-010' if kind == 'carried_by' else 'AFQR-18')
    app._runtime_state = replace(app._runtime_state, movement_state=replace(
        app.state, representation=replace(rep, relations=tuple(
            rel if r.subject_entity_id == obj else r for r in rep.relations))))


def workshop(app):
    for direction in ('south', 'west', 'west', 'west'):
        assert app.move(direction).authoritative_changed


@pytest.mark.parametrize('method,args', [
    ('material', ('put_on', 'repair board', 'workroom bench')),
    ('water', ('soak', 'wash bucket', 'cleaning cloth')),
])
def test_explicit_player_owner_path_matches_default_receipts_and_state(method, args):
    left, right = WaterApplication.new(), WaterApplication.new()
    for app in (left, right):
        workshop(app)
        assert app.pickup('repair board' if method == 'material' else 'cleaning cloth').authoritative_changed
    before = left.authoritative_digest()
    a = getattr(left, method)(*args)
    b = getattr(right, method + '_for_actor')(right.fixture.player_entity_id, *args)
    assert a == b
    assert a.authoritative_changed and a.pre_state_digest == before
    assert left.authoritative_digest() == right.authoritative_digest()
    assert len(left.journal) == len(right.journal) + 1
    assert left.fixture == right.fixture


def test_other_actor_executes_at_own_place_with_own_custody_and_attribution():
    app = WaterApplication.new()
    actor = identity('oren')
    relocate(app, 'oren', 'work-bench')
    relocate(app, 'cleaning-cloth', 'oren', 'carried_by')
    selected = app.fixture.player_entity_id
    profile = app.material_profile
    before = app.authoritative_digest()
    assert not app.water('soak', 'wash bucket', 'cleaning cloth').authoritative_changed
    assert app.authoritative_digest() == before
    result = app.water_for_actor(actor, 'soak', 'wash bucket', 'cleaning cloth')
    assert result.authoritative_changed, result.message
    assert result.command_id.startswith('actor-water-')
    expected_command = create_command_envelope(
        command_id=result.command_id, command_type='interact', source_actor_id=actor,
        payload={'operation': 'soak', 'participants': [identity('wash-bucket'), identity('cleaning-cloth')], 'amount': None},
        metadata={'package': 'PLAY-TARROW-WATER-1'})
    assert result.command_fingerprint == digest(expected_command.to_dict())
    assert app.fixture.player_entity_id == selected and app.material_profile == profile
    relocate(app, 'repair-board', 'oren', 'carried_by')
    result = app.material_for_actor(actor, 'put_on', 'repair board', 'workroom bench')
    assert result.authoritative_changed, result.message
    assert result.command_id.startswith('actor-material-')
    assert placement(app.state.representation, identity('repair-board')).relation_type == 'supported_by'
    assert app.fixture.player_entity_id == selected and app.material_profile == profile


@pytest.mark.parametrize('actor', ['oren', 'missing'])
def test_actor_known_ids_never_grant_remote_access(actor):
    app = WaterApplication.new()
    before = app.authoritative_digest()
    result = app.water_for_actor(identity(actor), 'soak', 'wash bucket', 'cleaning cloth')
    assert not result.authoritative_changed
    assert app.authoritative_digest() == before


def test_actor_cannot_borrow_player_custody_or_light():
    app = WaterApplication.new()
    workshop(app)
    assert app.pickup('cleaning cloth').authoritative_changed
    relocate(app, 'oren', 'work-bench')
    assert not app.water_for_actor(identity('oren'), 'soak', 'wash bucket', 'cleaning cloth').authoritative_changed
    # Lamp held elsewhere cannot illuminate an actor in a dark place.
    dark = next(p.entity_id for p in app.fixture.place_presentations
                if app.fixture.ambient_visual_condition_for(p.entity_id) == 'insufficient')
    relocate(app, 'oren', dark.removeprefix('astra:entity:tarrow-'))
    relocate(app, 'practice-panel', dark.removeprefix('astra:entity:tarrow-'))
    assert not app._visible_for_actor(identity('oren'), identity('practice-panel'))
