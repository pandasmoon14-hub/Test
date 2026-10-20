"""Independent assertions for isolated actor negative controls."""
from dataclasses import replace
import json
import pytest
from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_material import placement, digest, MaterialError
from astra_runtime.domain.persistent_world_actor_evidence import latest


def make(*, willing=True, standing=False, path=None):
    base=create_actor_fixture()
    profiles=tuple(replace(p,willing=willing,**({} if standing else dict(standing_kind=None,standing_method=None,standing_participants=(),standing_place=None))) for p in base.actor_profiles)
    return ActorApplication.new(fixture=create_actor_fixture(actor_profiles=profiles),checkpoint_path=path)


def workshop(a):
    for d in ('south','west','west','west'):
        r=a.move(d);assert r.authoritative_changed,r.message


def test_consent_is_not_execution_authority():
    a=make(willing=False);workshop(a)
    r=a.request_cleaning('Oren Kesh','practice panel',method='wipe')
    assert r.failure_class and not a.participation_state.records


def test_contribution_performer_is_npc_not_selected_player():
    a=make(standing=True)
    r=a.wait();assert r.authoritative_changed,r.message
    assert placement(a.state.representation,identity('cleaning-cloth')).object_entity_id==identity('oren')
    assert a.current_place_id()!=identity('work-bench')


def test_single_world_interval_for_two_actors():
    a=make(standing=True)
    r=a.wait();assert r.authoritative_changed,r.message
    assert a.runtime_state.logical_time_state.logical_position==1
    assert len(a.intervals)==1 and len(a.fixture.actor_order)==2


def test_player_claim_requalifies_prepared_npc_intent():
    a=make();workshop(a)
    r=a.request_cleaning('Oren Kesh','practice panel');assert r.authoritative_changed,r.message
    r=a.pickup('cleaning cloth');assert r.authoritative_changed,r.message
    assert placement(a.state.representation,identity('cleaning-cloth')).object_entity_id==a.fixture.player_entity_id
    task=a.participation_state.records[-1]
    assert task.status=='blocked' and task.contributions==()


def test_remote_player_does_not_inherit_npc_witness():
    a=make(standing=True)
    r=a.wait();assert r.authoritative_changed,r.message
    assert latest(a.evidence_state,identity('oren'),identity('cleaning-cloth'),'moisture') is not None
    assert latest(a.evidence_state,a.fixture.player_entity_id,identity('cleaning-cloth'),'moisture') is None


def test_replay_rejects_changed_actor_attribution_profile(tmp_path):
    path=tmp_path/'actors.json';a=make(standing=True,path=path)
    r=a.wait();assert r.authoritative_changed,r.message
    envelope=json.loads(path.read_text())
    envelope['payload']['profile']['actors'][0]['actor_id']=a.fixture.player_entity_id
    envelope['integrity_digest']=digest(envelope['payload'])
    path.write_text(json.dumps(envelope))
    with pytest.raises(MaterialError):
        ActorApplication.restore(fixture=a.fixture,checkpoint_path=path)
