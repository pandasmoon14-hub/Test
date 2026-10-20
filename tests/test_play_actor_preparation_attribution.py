"""Preparation can discover a satisfied goal without claiming its achievement."""
from dataclasses import replace

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_actor_participation import selected


def test_arrival_at_already_clean_goal_keeps_preparation_without_completion_credit():
    base=create_actor_fixture()
    profiles=tuple(replace(p,standing_kind=None,standing_method=None,
        standing_participants=(),standing_place=None) for p in base.actor_profiles)
    app=ActorApplication.new(fixture=create_actor_fixture(actor_profiles=profiles))
    actor=identity('oren');surface=identity('practice-panel');place=identity('work-bench')
    app._accept(actor,'cleaning','wipe',(surface,identity('cleaning-cloth')),place,actor)
    # A valid review context after the performer has left: the goal is satisfied
    # elsewhere, with every residue unit retained. The actor has not observed it.
    source=next(a for a,b in app.actor_profile(actor).routes if b==place)
    rep=app.state.representation
    app._runtime_state=replace(app._runtime_state,movement_state=replace(app.state,
        representation=replace(rep,relations=tuple(replace(r,object_entity_id=source)
            if r.subject_entity_id==actor else r for r in rep.relations))))
    original=dict(app.water_state.adhered)[surface]
    app.water_state=replace(app.water_state,adhered=tuple((key,
        0 if key==surface else value+original if key==identity('debris-tray') else value)
        for key,value in app.water_state.adhered))
    app._validate_transaction()
    task=selected(app.participation_state,actor)
    assert app._task_complete(task) and not app._goal_visible_complete(task)
    result=app.wait()
    assert result.authoritative_changed and app._actor_place_id(actor)==place
    task=selected(app.participation_state,actor)
    assert len(task.contributions)==1  # the actual movement remains attributed
    assert task.status=='externally_satisfied'
    assert dict(app.water_state.adhered)[surface]==0
    assert app.runtime_state.logical_time_state.logical_position==1
