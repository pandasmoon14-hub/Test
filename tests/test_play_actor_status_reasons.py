"""Local explanations and stale agreement records never become remote live status."""
from dataclasses import replace

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_actor_participation import selected


def test_blocker_reason_is_disclosed_locally_then_remains_historical_remotely(tmp_path):
    base=create_actor_fixture()
    profiles=tuple(replace(p,standing_kind=None,standing_method=None,
        standing_participants=(),standing_place=None) for p in base.actor_profiles)
    fixture=create_actor_fixture(actor_profiles=profiles)
    a=ActorApplication.new(fixture=fixture,checkpoint_path=tmp_path/'state.json')
    for direction in ('south','west','west','west'):
        assert a.move(direction).authoritative_changed
    assert a.request_cleaning('Oren Kesh','practice panel',method='wipe').authoritative_changed
    assert a.pickup('cleaning cloth').authoritative_changed
    task=selected(a.participation_state,identity('oren'))
    assert task.status=='blocked' and task.reason
    clock=a.runtime_state.logical_time_state.logical_position
    report=a.participation_status('Oren Kesh')
    assert task.reason in report.message and 'Reason:' in report.message
    assert a.runtime_state.logical_time_state.logical_position==clock
    assert 'astra:entity:' not in report.message
    assert a.move('east').authoritative_changed
    assert a.wait().authoritative_changed
    assert selected(a.participation_state,identity('oren')).status=='withdrawn'
    a=ActorApplication.restore(fixture=fixture,checkpoint_path=a.checkpoint_path)
    before=a.authoritative_digest()
    remote=a.participation_status('Oren Kesh')
    assert 'Last communicated status: blocked' in remote.message
    assert task.reason in remote.message and 'Current status is unavailable' in remote.message
    assert 'withdrawn' not in remote.message and 'at interval' not in remote.message
    assert a.authoritative_digest()==before
