"""Concrete review regressions for preparation, recovery and causal attribution."""
from dataclasses import replace
from fractions import Fraction
import pytest
from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.myravant_tarrow import identity as i
from astra_runtime.domain import persistent_world_actor_participation as participation
from astra_runtime.domain import persistent_world_actor_evidence as evidence
from astra_runtime.domain.persistent_world_continuing_work import WorkTask
from astra_runtime.domain.persistent_world_material import placement


def app():
    base=create_actor_fixture()
    profiles=tuple(replace(p,standing_kind=None,standing_method=None,standing_participants=(),standing_place=None) for p in base.actor_profiles)
    return ActorApplication.new(fixture=create_actor_fixture(actor_profiles=profiles))


def locate(a,key,place,relation='located_at'):
    """Declare a review initial context; production methods remain unmodified."""
    rep=a.state.representation
    rep=replace(rep,relations=tuple(replace(r,relation_type=relation,object_entity_id=i(place),semantic_owner='AFQR-18' if relation=='located_at' else 'RT-010') if r.subject_entity_id==i(key) else r for r in rep.relations))
    a._runtime_state=replace(a._runtime_state,movement_state=replace(a.state,representation=rep))


def quantity(rows,key,value):return tuple((k,value if k==i(key) else v) for k,v in rows)


def task(a,method='wipe',tool='cleaning-cloth'):
    return WorkTask('review-candidate',i('oren'),'cleaning',method,(i('practice-panel'),i(tool)),i('work-bench'))


def workshop(a):
    for d in ('south','west','west','west'):
        r=a.move(d);assert r.authoritative_changed,r.message


def test_goal_only_dry_cloth_without_water_selects_viable_brush():
    a=app();workshop(a);locate(a,'cleaning-brush','work-bench')
    # The finite supply exists but is unavailable in this actor's context.
    locate(a,'wash-bucket','yard-tools')
    result=a.request_cleaning('Oren Kesh','practice panel')
    assert result.authoritative_changed,result.message
    selected=participation.selected(a.participation_state,i('oren'))
    assert selected.method=='scrub' and selected.participants[1]==i('cleaning-brush')


def test_dried_deposits_fill_capacity_and_select_real_recovery():
    a=app();locate(a,'cleaning-cloth','oren','carried_by');locate(a,'debris-tray','work-bench')
    a.water_state=replace(a.water_state,water=quantity(quantity(a.water_state.water,'cleaning-cloth',1),'wash-bucket',11),adhered=quantity(a.water_state.adhered,'practice-panel',1))
    a.environment_state=replace(a.environment_state,deposits=quantity(a.environment_state.deposits,'cleaning-cloth',Fraction(2)))
    outcome,intent=a._prepare_actor(task(a))
    assert outcome=='action' and intent==('water','collect',(i('cleaning-cloth'),i('debris-tray')))


def test_soak_skips_empty_first_source_for_qualified_second_source():
    a=app();locate(a,'cleaning-cloth','oren','carried_by')
    a.water_state=replace(a.water_state,water=quantity(quantity(a.water_state.water,'wash-bucket',0),'rinse-basin',6))
    a.environment_state=replace(a.environment_state,evaporated=quantity(a.environment_state.evaporated,'work-bench',6))
    outcome,intent=a._prepare_actor(task(a))
    assert outcome=='action' and intent==('water','soak',(i('rinse-basin'),i('cleaning-cloth')))


def test_player_physical_action_retains_performed_evidence():
    a=app();workshop(a)
    result=a.pickup('cleaning cloth');assert result.authoritative_changed,result.message
    event=evidence.latest(a.evidence_state,a.fixture.player_entity_id,i('cleaning-cloth'),'activity')
    assert event.kind=='performed' and event.value=='pickup' and event.receipt_id==result.receipt_id


def test_paused_task_tool_return_is_real_handoff_and_no_second_actor_step():
    a=app();workshop(a)
    assert a.request_cleaning('Oren Kesh','practice panel',tool_reference='cleaning cloth',method='wipe').authoritative_changed
    assert a.wait().authoritative_changed
    assert a.participation_control('Oren Kesh','pause').authoritative_changed
    before=participation.selected(a.participation_state,i('oren'))
    tick=a.runtime_state.logical_time_state.logical_position
    result=a.request_object_from_actor('Oren Kesh','cleaning cloth')
    assert result.authoritative_changed,result.message
    assert a.runtime_state.logical_time_state.logical_position==tick+1
    assert placement(a.state.representation,i('cleaning-cloth')).object_entity_id==a.fixture.player_entity_id
    assert participation.selected(a.participation_state,i('oren')).contributions==before.contributions
    events=[e for e in a.actor_events if e[4]==tick+1 and e[2]==i('oren')]
    assert [e[1] for e in events]==['physical_return']


def test_temporarily_ineligible_standing_activity_can_start_later():
    a=ActorApplication.new(fixture=create_actor_fixture())
    locate(a,'cleaning-cloth','yard-tools')
    assert a.wait().authoritative_changed
    assert not any(t.actor_id==i('oren') for t in a.participation_state.records)
    locate(a,'cleaning-cloth','work-bench')
    assert a.wait().authoritative_changed
    assert participation.selected(a.participation_state,i('oren')).source_actor_id==i('oren')


def test_unknown_standing_assembly_fails_closed():
    base=create_actor_fixture();oren=base.actor_profiles[0]
    invalid=replace(oren,standing_kind='assembly',standing_method='missing arrangement',standing_participants=(i('repair-board'),i('repair-peg'),i('repair-cord')),standing_place=i('work-bench'))
    with pytest.raises(ValueError):
        ActorApplication.new(fixture=create_actor_fixture(actor_profiles=(invalid,base.actor_profiles[1])))


def test_full_collection_sink_is_skipped_for_qualified_rinse_destination():
    base=app().fixture
    limited=replace(base.water_profile,assets=tuple(replace(asset,residue_capacity=Fraction(1)) if asset.id==i('debris-tray') else asset for asset in base.water_profile.assets))
    a=ActorApplication.new(fixture=replace(base,water_profile=limited));locate(a,'cleaning-cloth','oren','carried_by');locate(a,'debris-tray','work-bench')
    a.water_state=replace(a.water_state,
        water=quantity(quantity(a.water_state.water,'cleaning-cloth',1),'wash-bucket',11),
        adhered=quantity(quantity(quantity(quantity(a.water_state.adhered,'cleaning-cloth',2),'debris-tray',1),'practice-panel',1),'sorting-board',3))
    outcome,intent=a._prepare_actor(task(a))
    assert outcome=='action' and intent==('water','rinse',(i('cleaning-cloth'),i('wash-bucket')))


def test_player_reopens_satisfied_assembly_before_npc_resolution_records_blocked():
    a=app();workshop(a)
    for obj in ('repair board','repair peg'):
        assert a.pickup(obj).authoritative_changed
        assert a.material('put_on',obj,'workroom bench').authoritative_changed
    assert a.pickup('repair cord').authoritative_changed
    assert a.material('tie','repair board','repair peg','repair cord').authoritative_changed
    assert a.request_assembly('Oren Kesh','workshop assembly').authoritative_changed
    result=a.material('untie','repair cord')
    assert result.authoritative_changed,result.message
    selected=participation.selected(a.participation_state,i('oren'))
    assert selected.status=='blocked' and selected.blocked_due==1 and selected.contributions==()
    assert not a.connections
