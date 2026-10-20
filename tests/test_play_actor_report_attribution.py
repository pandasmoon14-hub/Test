"""A repeated false assertion remains publicly attributed through restart."""
from dataclasses import replace

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_actor_evidence import latest


def test_false_report_names_original_speaker_without_refresh_or_truth_change(tmp_path):
    base = create_actor_fixture()
    profiles = tuple(replace(p, standing_kind=None, standing_method=None,
                             standing_participants=(), standing_place=None)
                     for p in base.actor_profiles)
    fixture = create_actor_fixture(actor_profiles=profiles)
    app = ActorApplication.new(fixture=fixture, checkpoint_path=tmp_path / 'actors.json')
    for direction in ('south', 'west', 'west', 'west'):
        assert app.move(direction).authoritative_changed
    target = identity('practice-panel')
    initial_material = app.water_state
    tick = app.runtime_state.logical_time_state.logical_position
    assert dict(initial_material.adhered)[target] > 0
    assert app.tell_actor('Oren Kesh', 'practice panel', 'residue', 'clear').authoritative_changed
    app = ActorApplication.restore(fixture=fixture, checkpoint_path=app.checkpoint_path)
    result = app.ask_report('Oren Kesh', 'practice panel', 'residue')
    assert result.authoritative_changed, result.message
    assert 'a statement from ' + fixture.entity_name(fixture.player_entity_id) in result.message
    assert 'reported evidence' in result.message and 'clear' in result.message
    assert app.water_state == initial_material
    assert app.runtime_state.logical_time_state.logical_position == tick
    received = latest(app.evidence_state, fixture.player_entity_id, target, 'residue')
    original = latest(app.evidence_state, identity('oren'), target, 'residue')
    assert received.kind == 'reported' and received.source_event_id == original.event_id
    assert original.kind == 'reported' and original.source_actor_id == fixture.player_entity_id
