"""PLAY-TRIAL-2: choose player/NPC restoration and dispatch as one goal.

The goal interpreter never owns service/brace/duty/time/displacement state.
Test actual owner receipts, play constraints, unseen attempts, installed
checkpoint continuity and whole-campaign cross-capability consequences.
"""
from __future__ import annotations

import subprocess
import sys

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    containment_relation_for,
)
from astra_runtime.myravant_chest_readiness_goal import (
    execute_chest_readiness_goal, parse_chest_readiness_goal,
)
from astra_runtime.myravant_orchard_supply_goal import (
    execute_orchard_supply_attempt,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, LANTERN_ID, ORCHARD_PATH_ID,
    PLAYER_ID, TOOL_CHEST_ID, WORKSHOP_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def goal(app,method=None):
    phrase="prepare tool chest for orchard"
    if method is not None:
        phrase+=f" by {method}"
    return execute_chest_readiness_goal(app,phrase)


def yard(app):
    assert app.move("south").authoritative_changed
    assert app.current_place_id()==YARD_ID


def placed(app,target,place):
    return any(
        r.relation_type==LOCATED_AT_RELATION_TYPE
        and r.subject_entity_id==target and r.object_entity_id==place
        for r in app.state.representation.relations
    )


@pytest.mark.parametrize("phrase,expected",[
    ("prepare chest for orchard",None),
    ("I want to ready the tool chest for transport",None),
    ("How do I restore chest for delivery?",None),
    ("make ready chest for shipment by manual service","manual"),
    ("prepare tool chest for orchard by servicing the latch by hand","manual"),
    ("ready chest for transport with using a lit lantern for latch work","lantern"),
    ("restore chest for journey using lantern service","lantern"),
    ("prepare chest for orchard by asking groundskeeper to service the latch","npc_service"),
    ("prepare chest for orchard via asking the groundskeeper to repair with lantern","npc_service"),
    ("ready chest for transport by refitting the brace","refit"),
    ("prepare chest for orchard by closing chest","close"),
    ("prepare chest for orchard by securing the latch myself","secure"),
    ("prepare chest for orchard by asking groundskeeper to secure later","request_duty"),
    ("prepare chest for orchard by waiting for groundskeeper to finish","wait_duty"),
    ("prepare chest for orchard by cancelling groundskeeper duty","cancel_duty"),
    ("prepare chest for orchard by pushing it east","transport"),
    ("prepare chest for orchard by teleporting chest","unqualified"),
])
def test_parser_distinguishes_goal_and_method(phrase,expected):
    parsed=parse_chest_readiness_goal(phrase)
    assert parsed is not None
    assert parsed.method==expected
    assert parsed.raw_text==phrase


@pytest.mark.parametrize("phrase",[
    "open chest","secure chest","go east",
    "service chest latch","remove chest brace",
    "ask groundskeeper to service chest latch with lantern",
    "prepare lantern for orchard by manual service",
    "prepare chest for tower by manual service",
    "ready the gatehouse for shipment",
    "prepare chest for orchard by manual service then push it",
    "prepare chest for orchard by manual service and securing it",
    "prepare chest for orchard while repairing and carrying a lantern",
    "prepare chest for orchard by waiting and then securing",
])
def test_interpreter_does_not_swallow_other_or_compound_actions(phrase):
    assert parse_chest_readiness_goal(phrase) is None


def test_manual_latch_and_direct_secure_then_real_delivery(tmp_path):
    app=MyravantVSM14Application.new(
        checkpoint_path=tmp_path/"manual-ready.json",
    )
    yard(app)
    before=app.authoritative_digest()
    advice=goal(app)
    assert advice.result_type=="chest_readiness_methods_observed"
    assert "0/2" in advice.message
    assert "manual latch work" in advice.message
    assert advice.pre_state_digest==advice.post_state_digest==before
    assert app.authoritative_digest()==before

    first=goal(app,"manual service")
    second=goal(app,"manual service")
    assert first.authoritative_changed and second.authoritative_changed
    assert first.receipt_id and second.receipt_id
    assert first.receipt_id!=second.receipt_id
    assert first.consequence_receipt_id and second.consequence_receipt_id
    assert app.service_state.progress==2
    assert len(app.service_state.events)==2
    assert all(x.actor_id==PLAYER_ID for x in app.service_state.events)
    assert all(x.method=="manual" for x in app.service_state.events)
    advice=goal(app)
    assert "2/2" in advice.message
    assert "Close the Chest" in advice.message
    assert goal(app,"closing chest").authoritative_changed
    sec=goal(app,"securing the latch myself")
    assert sec.authoritative_changed
    assert sec.receipt_id and sec.preview_id and sec.state_delta_id
    assert app.service_state.secured
    assert app.service_state.events[-1].actor_id==PLAYER_ID
    assert "secured" in goal(app).message
    pushed=goal(app,"pushing it east")
    assert pushed.authoritative_changed
    assert pushed.result_type=="object_displacement_committed"
    assert pushed.receipt_id and pushed.state_delta_id
    assert placed(app,TOOL_CHEST_ID,ORCHARD_PATH_ID)
    assert app.service_state.secured
    assert app.save().checkpoint_digest
    restored=MyravantVSM14Application.restore(
        checkpoint_path=app.checkpoint_path,
    )
    assert restored.authoritative_digest()==app.authoritative_digest()
    assert restored.service_state.events==app.service_state.events
    assert placed(restored,TOOL_CHEST_ID,ORCHARD_PATH_ID)
    assert restored.move("east").authoritative_changed
    # Local repair requirements cannot be bypassed by calling a goal remotely.
    pre=restored.authoritative_digest()
    denied=goal(restored,"manual service")
    assert denied.failure_class=="chest_readiness_worksite_not_local"
    assert restored.authoritative_digest()==pre


def test_brace_damage_blocks_finish_until_conserved_refit(tmp_path):
    app=MyravantVSM14Application.new(checkpoint_path=tmp_path/"brace.json")
    yard(app)
    assert app.alter_chest_brace("manual").authoritative_changed
    assert app.alter_chest_brace("manual").authoritative_changed
    assert app.brace_state.condition=="detached_at_yard"
    assert "must be refitted" in goal(app).message
    assert goal(app,"manual service").authoritative_changed
    assert goal(app,"manual service").authoritative_changed
    before=app.authoritative_digest()
    refusal=goal(app,"securing the latch myself")
    assert refusal.failure_class=="fixture_service_brace_not_attached"
    assert refusal.pre_state_digest==refusal.post_state_digest==before
    assert app.authoritative_digest()==before
    # Open state independently prevents an immediate structural refit.
    if app.object_open_state(TOOL_CHEST_ID).state=="closed":
        assert app.open_object("chest").authoritative_changed
    before=app.authoritative_digest()
    refused=goal(app,"refitting the brace")
    assert refused.failure_class=="fixture_brace_chest_not_closed"
    assert app.authoritative_digest()==before
    assert goal(app,"closing chest").authoritative_changed
    fitting=goal(app,"refitting the brace")
    assert fitting.authoritative_changed
    assert fitting.receipt_id and fitting.consequence_receipt_id
    assert app.brace_state.condition=="attached"
    assert len(app.brace_state.events)==3
    assert goal(app,"securing the latch myself").authoritative_changed
    assert app.service_state.secured
    assert app.save().checkpoint_digest
    restored=MyravantVSM14Application.restore(
        checkpoint_path=app.checkpoint_path,
    )
    assert restored.authoritative_digest()==app.authoritative_digest()
    assert restored.brace_state.condition=="attached"
    assert restored.service_state.secured


def test_player_lantern_work_changes_required_time_and_opportunity(tmp_path):
    app=MyravantVSM14Application.new(checkpoint_path=tmp_path/"tool.json")
    yard(app)
    before=app.authoritative_digest()
    refused=goal(app,"lantern service")
    assert refused.failure_class=="fixture_service_tool_unavailable"
    assert app.authoritative_digest()==before
    assert app.move("north").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    # Carried Lantern is not a ground-placed worksite resource.
    before=app.authoritative_digest()
    assert goal(app,"lantern service").failure_class=="fixture_service_tool_unavailable"
    assert app.authoritative_digest()==before
    assert app.drop("lantern").authoritative_changed
    assert app.light_object("lantern").authoritative_changed
    work=goal(app,"lantern service")
    assert work.authoritative_changed
    assert work.consequence_receipt_id
    assert app.service_state.progress==2
    assert len(app.service_state.events)==1
    assert app.service_state.events[0].actor_id==PLAYER_ID
    assert app.service_state.events[0].method=="lantern"
    assert app.save().checkpoint_digest
    restored=MyravantVSM14Application.restore(
        checkpoint_path=app.checkpoint_path,
    )
    assert restored.authoritative_digest()==app.authoritative_digest()


def test_actor_service_and_delayed_secure_persist_without_remote_report(tmp_path):
    app=MyravantVSM14Application.new(checkpoint_path=tmp_path/"npc.json")
    yard(app)
    pre=app.authoritative_digest()
    absent=goal(app,"asking groundskeeper to service the latch")
    assert absent.failure_class=="actor_service_actor_not_local"
    assert app.authoritative_digest()==pre
    assert app.wait().authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID)==YARD_ID
    assert app.move("north").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.drop("lantern").authoritative_changed
    assert app.light_object("lantern").authoritative_changed
    work=goal(app,"asking groundskeeper to service the latch")
    assert work.result_type=="actor_service_committed"
    assert work.authoritative_changed
    assert work.receipt_id and work.consequence_receipt_id
    assert app.service_state.progress==2
    assert app.service_state.events[-1].actor_id==GROUNDSKEEPER_ID
    assert app.service_state.events[-1].method=="lantern"
    assert goal(app,"closing chest").authoritative_changed
    accepted=goal(app,"asking groundskeeper to secure later")
    assert accepted.authoritative_changed
    assert accepted.receipt_id
    assert app.duty_state.status=="pending"
    assert "pending" in goal(app).message
    assert app.save().checkpoint_digest
    restored=MyravantVSM14Application.restore(
        checkpoint_path=app.checkpoint_path,
    )
    assert restored.authoritative_digest()==app.authoritative_digest()
    assert restored.duty_state.status=="pending"

    # Independent player relocation, then WORLD-2 time; no remote omniscient
    # completion message from the goal interpreter.
    assert restored.move("north").authoritative_changed
    remotely=goal(restored)
    assert remotely.failure_class=="chest_readiness_worksite_not_local"
    assert not remotely.authoritative_changed
    assert remotely.pre_state_digest==remotely.post_state_digest
    waited=restored.wait()
    assert waited.authoritative_changed
    assert waited.message=="Time passes."
    assert restored.duty_state.status=="fulfilled"
    assert restored.service_state.secured
    assert restored.service_state.events[-1].actor_id==GROUNDSKEEPER_ID
    assert restored.move("south").authoritative_changed
    assert "fulfilled" in goal(restored).message
    before=restored.authoritative_digest()
    denied=restored.open_object("chest")
    assert denied.failure_class=="fixture_service_latch_secured"
    assert restored.authoritative_digest()==before
    assert restored.save().checkpoint_digest
    final=MyravantVSM14Application.restore(checkpoint_path=restored.checkpoint_path)
    assert final.authoritative_digest()==restored.authoritative_digest()


def test_cancel_agreement_and_no_automatic_latch_completion():
    app=MyravantVSM14Application.new()
    yard(app)
    pre=app.authoritative_digest()
    refused=goal(app,"waiting for groundskeeper to finish")
    assert refused.failure_class=="chest_readiness_no_pending_duty"
    assert app.authoritative_digest()==pre
    assert goal(app,"manual service").authoritative_changed
    assert goal(app,"manual service").authoritative_changed
    assert goal(app,"closing chest").authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID)==YARD_ID
    assert goal(app,"asking groundskeeper to secure later").authoritative_changed
    assert app.duty_state.status=="pending"
    assert goal(app,"cancelling groundskeeper duty").authoritative_changed
    assert app.duty_state.status=="cancelled"
    assert app.wait().authoritative_changed
    assert not app.service_state.secured
    assert app.duty_state.status=="cancelled"


def test_goal_based_wait_uses_same_owner_duty_receipts():
    app=MyravantVSM14Application.new()
    yard(app)
    assert goal(app,"manual service").authoritative_changed
    assert goal(app,"manual service").authoritative_changed
    assert goal(app,"closing chest").authoritative_changed
    assert goal(app,"asking groundskeeper to secure later").authoritative_changed
    before=app.authoritative_digest()
    tick=goal(app,"waiting for groundskeeper to finish")
    assert tick.authoritative_changed
    assert tick.receipt_id
    assert tick.pre_state_digest==before
    assert app.duty_state.status=="fulfilled"
    assert app.service_state.secured
    assert app.duty_state.events[-1].service_receipt_id==app.service_state.events[-1].receipt_id
    assert app.duty_state.events[-1].time_receipt_id==tick.receipt_id


def test_remote_absent_unknown_refusals_do_not_mutate():
    app=MyravantVSM14Application.new()
    before=app.authoritative_digest()
    for method in (None,"manual service","lantern service","pushing it east"):
        refused=goal(app,method)
        assert refused.failure_class=="chest_readiness_worksite_not_local"
        assert refused.pre_state_digest==refused.post_state_digest==before
        assert app.authoritative_digest()==before
    yard(app)
    before=app.authoritative_digest()
    for method in ("teleporting","sawing it apart magically","asking a stranger"):
        refused=goal(app,method)
        assert refused.failure_class=="chest_readiness_method_unqualified"
        assert refused.pre_state_digest==refused.post_state_digest==before
        assert app.authoritative_digest()==before
    assert goal(app,"pushing it east").authoritative_changed
    before=app.authoritative_digest()
    for method in (None,"manual service","securing the latch myself"):
        refused=goal(app,method)
        assert refused.failure_class=="chest_readiness_chest_not_local"
        assert not refused.authoritative_changed
        assert app.authoritative_digest()==before


def test_secured_real_cargo_ships_without_creating_contents(tmp_path):
    app=MyravantVSM14Application.new(checkpoint_path=tmp_path/"ship.json")
    assert app.pickup("lantern").authoritative_changed
    yard(app)
    assert app.open_object("chest").authoritative_changed
    assert app.store_object("lantern","chest").authoritative_changed
    contents=containment_relation_for(app.storage_state,LANTERN_ID)
    assert contents is not None and contents.object_entity_id==TOOL_CHEST_ID
    assert goal(app,"closing chest").authoritative_changed
    assert goal(app,"manual service").authoritative_changed
    assert goal(app,"manual service").authoritative_changed
    # At this point an autonomous phase may re-open the Chest: secure must
    # still use actual current state, not a stale goal plan.
    if app.object_open_state(TOOL_CHEST_ID).state!="closed":
        assert goal(app,"closing chest").authoritative_changed
    assert goal(app,"securing the latch myself").authoritative_changed
    pushed=goal(app,"pushing it east")
    assert pushed.authoritative_changed
    assert placed(app,TOOL_CHEST_ID,ORCHARD_PATH_ID)
    assert containment_relation_for(app.storage_state,LANTERN_ID)==contents
    assert app.service_state.secured
    assert app.save().checkpoint_digest
    restored=MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest()==app.authoritative_digest()
    assert restored.move("east").authoritative_changed
    inquiry=execute_orchard_supply_attempt(restored,"check orchard supply")
    assert not inquiry.authoritative_changed
    assert "No presently observable Lantern supply" in inquiry.message
    assert restored.open_object("chest").failure_class=="fixture_service_latch_secured"
    assert restored.service_chest_latch("release").authoritative_changed
    assert restored.open_object("chest").authoritative_changed
    assert restored.retrieve_object("lantern","chest").authoritative_changed
    assert containment_relation_for(restored.storage_state,LANTERN_ID) is None
    assert restored.save().checkpoint_digest
    reread=MyravantVSM14Application.restore(checkpoint_path=restored.checkpoint_path)
    assert reread.authoritative_digest()==restored.authoritative_digest()


def test_equal_goal_histories_identical_replay():
    histories=[]
    for _ in range(2):
        app=MyravantVSM14Application.new()
        yard(app)
        query=goal(app)
        a=goal(app,"manual service")
        b=goal(app,"manual service")
        c=goal(app,"closing chest")
        d=goal(app,"securing the latch myself")
        assert all(x.authoritative_changed for x in (a,b,c,d))
        histories.append((
            query.message,*(x.receipt_id for x in (a,b,c,d)),
            app.authoritative_digest(),app.service_state.events,
        ))
    assert histories[0]==histories[1]


def test_installed_two_sessions_resume_multi_method_chest_restoration(tmp_path):
    checkpoint=tmp_path/"chest-trial2.json"
    def play(commands,*args):
        return subprocess.run(
            [sys.executable,"-m","astra_runtime.myravant_terminal",*args],
            input="\n".join((*commands,"exit","")),text=True,
            capture_output=True,timeout=120,
        )
    first=play((
        "go south",
        "prepare chest for orchard",
        "prepare chest for orchard by manual service",
        "prepare chest for orchard by manual service",
        "prepare chest for orchard by closing chest",
    ),"--checkpoint",str(checkpoint))
    assert first.returncode==0,(first.stdout,first.stderr)
    assert "0/2" in first.stdout
    assert "latch is now serviceable" in first.stdout
    assert checkpoint.is_file()
    resumed=MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert resumed.service_state.progress==2
    assert not resumed.service_state.secured
    second=play((
        "prepare chest for orchard by securing the latch myself",
        "prepare chest for orchard by pushing it east",
        "go east",
    ),"--load",str(checkpoint))
    assert second.returncode==0,(second.stdout,second.stderr)
    assert "latch now secures" in second.stdout
    assert "You push the Tool Chest east." in second.stdout
    final=MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert final.service_state.secured
    assert placed(final,TOOL_CHEST_ID,ORCHARD_PATH_ID)
    assert final.current_place_id()==ORCHARD_PATH_ID
