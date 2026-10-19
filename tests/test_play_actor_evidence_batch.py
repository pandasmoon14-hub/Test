"""Ordered evidence batching preserves single-admission identity and history rules."""
from dataclasses import replace
import pytest
from astra_runtime.domain import persistent_world_actor_evidence as e


def event(name='first',tick=1):
    return e.EvidenceEvent(name,'worker','witnessed','worker','cloth','moisture','wet',tick,'receipt','local')


def sequential(state,events):
    for item in events:
        old=next((prior for prior in state.events if prior.event_id==item.event_id),None)
        if old is not None:
            if old!=item:raise ValueError('evidence identity reused with different provenance')
        else:state=e.EvidenceState(state.events+(item,))
    return state


@pytest.mark.parametrize('events',[(event(),event('second',2)),(event(),event()),(event(),event('second',2),event())])
def test_ordered_batch_matches_retained_single_admission(events):
    initial=e.EvidenceState()
    assert e.record_many(initial,events,qualified=True)==sequential(initial,events)
    assert e.canonical_state(e.record_many(initial,events,qualified=True))==e.canonical_state(sequential(initial,events))


def test_batch_duplicate_provenance_failure_is_atomic():
    initial=e.EvidenceState((event(),))
    with pytest.raises(ValueError,match='provenance'):
        e.record_many(initial,(event('second',2),replace(event(),value='dry')),qualified=True)
    assert initial.events==(event(),)
    assert e.record_many(initial,(event(),),qualified=True) is initial


@pytest.mark.parametrize('events',[(event('late',2),event('earlier',1)),(event('prior',0),)])
def test_batch_cannot_backdate_new_history(events):
    initial=e.EvidenceState((event(),))
    with pytest.raises(ValueError,match='chronological'):
        e.record_many(initial,events,qualified=True)


@pytest.mark.parametrize('qualified',[False,None,1])
def test_batch_retains_explicit_qualification(qualified):
    with pytest.raises(ValueError):e.record_many(e.EvidenceState(),(),qualified=qualified)


@pytest.mark.parametrize('field,value', [('event_id',''),('actor_id',None),('kind','invented'),('source_actor_id','other'),('target_id',[]),('facet',''),('value',['mutable']),('tick',True),('receipt_id',''),('qualification',''),('origin_tick',99),('source_event_id','')])
def test_canonical_still_rejects_corruption_of_previously_valid_event(field,value):
    item=event()
    state=e.EvidenceState((item,))
    object.__setattr__(item,field,value)
    with pytest.raises((ValueError,TypeError)):
        e.canonical_state(state)


def test_canonical_projection_is_fresh_and_ignores_nonfield_attributes():
    item=event();state=e.EvidenceState((item,))
    expected=e.canonical_state(state)
    object.__setattr__(item,'injected_private_attribute','not-a-domain-field')
    assert e.canonical_state(state)==expected
    projected=e.canonical_state(state)
    projected['events'][0]['value']='changed'
    assert e.canonical_state(state)==expected
