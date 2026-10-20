"""Installed actor scheduling: consent, real custody, and interval boundaries."""
from dataclasses import replace
import pytest
from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain import persistent_world_actor_participation as p
from astra_runtime.domain.persistent_world_material import placement


def fixture(*, willing=True, standing=False):
    original = create_actor_fixture()
    profiles = tuple(replace(profile, willing=willing,
        **({} if standing else dict(standing_kind=None, standing_method=None,
                                   standing_participants=(), standing_place=None)))
        for profile in original.actor_profiles)
    return create_actor_fixture(actor_profiles=profiles)


def app(tmp_path=None, **kwargs):
    return ActorApplication.new(fixture=fixture(**kwargs), checkpoint_path=tmp_path/'actors.json' if tmp_path else None)


def tick(a):
    return a.runtime_state.logical_time_state.logical_position


def workshop(a):
    for direction in ('south', 'west', 'west', 'west'):
        result = a.move(direction)
        assert result.authoritative_changed, result.message


def oren(a):
    return p.selected(a.participation_state, identity('oren'))


def request(a, method=None, tool=None):
    return a.request_cleaning('Oren Kesh', 'practice panel', tool_reference=tool, method=method)


def test_refused_consent_and_busy_request_leave_state_unchanged():
    a=app(willing=False);workshop(a);before=a.authoritative_digest();clock=tick(a)
    result=request(a)
    assert result.failure_class and a.authoritative_digest()==before and tick(a)==clock
    a=app();workshop(a)
    assert request(a).authoritative_changed
    before=a.authoritative_digest()
    assert request(a).failure_class
    assert a.authoritative_digest()==before


def test_acceptance_next_interval_custody_then_own_method_not_instant_goal():
    a=app();workshop(a);clock=tick(a)
    assert request(a).authoritative_changed
    task=oren(a)
    assert tick(a)==clock and task.contributions==()
    assert placement(a.state.representation,identity('cleaning-cloth')).relation_type=='located_at'
    result=a.wait();assert result.authoritative_changed,result.message
    assert tick(a)==clock+1
    assert len(oren(a).contributions)==1
    cloth=placement(a.state.representation,identity('cleaning-cloth'))
    assert (cloth.relation_type,cloth.object_entity_id)==('carried_by',identity('oren'))
    assert dict(a.water_state.adhered)[identity('practice-panel')]>0
    assert oren(a).due_intervals==(a.runtime_state.logical_time_state.committed_transitions[-1].receipt.receipt_id,)


def test_controls_are_zero_time_and_pause_suppresses_due_work():
    a=app();workshop(a);assert request(a).authoritative_changed
    clock=tick(a)
    assert a.participation_control('Oren Kesh','pause').authoritative_changed
    assert tick(a)==clock
    assert a.wait().authoritative_changed
    assert oren(a).contributions==() and oren(a).blocked_due==0
    clock=tick(a)
    assert a.participation_control('Oren Kesh','resume').authoritative_changed
    assert tick(a)==clock
    assert a.wait().authoritative_changed
    assert len(oren(a).contributions)==1
    clock=tick(a)
    assert a.participation_control('Oren Kesh','cancel').authoritative_changed
    assert tick(a)==clock and oren(a).status=='withdrawn'


def test_player_custody_blocks_npc_at_k_minus_one_k_and_k_plus_one_across_restart(tmp_path):
    a=app(tmp_path);workshop(a)
    assert request(a).authoritative_changed
    assert a.pickup('cleaning cloth').authoritative_changed
    assert oren(a).blocked_due==1 and oren(a).contributions==()
    for expected in (2,):
        result=a.wait();assert result.authoritative_changed,result.message
        assert oren(a).blocked_due==expected and oren(a).status=='blocked'
    a=ActorApplication.restore(checkpoint_path=tmp_path/'actors.json',fixture=a.fixture)
    assert oren(a).blocked_due==2
    assert a.wait().authoritative_changed
    assert oren(a).blocked_due==3 and oren(a).status=='withdrawn' and oren(a).contributions==()
    assert a.wait().authoritative_changed
    assert oren(a).blocked_due==3 and oren(a).contributions==()
    assert placement(a.state.representation,identity('cleaning-cloth')).object_entity_id==a.fixture.player_entity_id


def test_goal_only_selects_declared_method_explicit_method_is_not_silently_changed():
    a=app();workshop(a)
    result=request(a,method='scrub',tool='cleaning cloth')
    assert result.failure_class and not a.participation_state.records
    assert request(a).authoritative_changed
    assert oren(a).method=='wipe' and oren(a).participants==(identity('practice-panel'),identity('cleaning-cloth'))


def test_standing_work_runs_without_player_presence_and_remote_status_stays_historical():
    a=app(standing=True)
    assert a.current_place_id()!=identity('work-bench')
    assert a.wait().authoritative_changed
    assert oren(a).source_actor_id==identity('oren') and len(oren(a).contributions)==1
    before=a.authoritative_digest()
    result=a.participation_status('Oren Kesh')
    assert 'No last communicated' in result.message and a.authoritative_digest()==before


@pytest.mark.parametrize('reverse', [False, True])
def test_both_npcs_requalify_shared_custody_in_declared_order(reverse):
    base=fixture()
    order=tuple(reversed(base.actor_order)) if reverse else base.actor_order
    a=ActorApplication.new(fixture=create_actor_fixture(actor_profiles=base.actor_profiles,actor_order=order))
    # Fixture setup places both declared actors at the same real work position.
    rep=a.state.representation
    rep=replace(rep,relations=tuple(replace(r,object_entity_id=identity('work-bench'))
        if r.subject_entity_id==identity('tali') and r.relation_type=='located_at' else r
        for r in rep.relations))
    a._runtime_state=replace(a._runtime_state,movement_state=replace(a.state,representation=rep))
    for actor in order:
        a._accept(actor,'cleaning','wipe',(identity('practice-panel'),identity('cleaning-cloth')),
                  identity('work-bench'),actor)
    result=a.wait();assert result.authoritative_changed,result.message
    assert tick(a)==1
    assert placement(a.state.representation,identity('cleaning-cloth')).object_entity_id==order[0]
    first,second=(p.selected(a.participation_state,actor) for actor in order)
    assert len(first.contributions)==1
    assert second.status=='blocked' and second.contributions==() and second.blocked_due==1
