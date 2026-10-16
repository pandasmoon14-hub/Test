"""PLAY-TRIAL-3: player agency under competing persistent actor evidence.

End-to-end play uses the real C1 actor memory, C2 qualified movement,
C3 contact, COMP-3 world displacement, local perception and E2 replay.
Authored probes are not a substitute for independent unseen #493 scoring.
"""
from __future__ import annotations

import subprocess
import sys
from io import StringIO

import pytest

from astra_runtime.myravant_actor_situated_knowledge import last_actor_evidence
from astra_runtime.myravant_chest_investigation_goal import (
    execute_chest_investigation, parse_chest_investigation,
)
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID, GROUNDSKEEPER_ID, ORCHARD_PATH_ID,
    PLAYER_ID, TOOL_CHEST_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def attempt(app,method=None):
    text="trace chest with groundskeeper"
    if method:
        text+=f" by {method}"
    return execute_chest_investigation(app,text)


def together_in_yard(app):
    assert app.move("south").authoritative_changed
    assert app.wait().authoritative_changed
    assert app.current_place_id()==YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID)==YARD_ID


@pytest.mark.parametrize("raw,method,place",[
    ("trace chest with groundskeeper","compare",None),
    ("I want to investigate the tool chest alongside the groundskeeper","compare",None),
    ("How can I locate chest with groundskeeper?", "compare",None),
    ("trace chest with groundskeeper by comparing the two leads","compare",None),
    ("trace chest with groundskeeper using asking for a firsthand sighting","witness",None),
    ("trace chest with groundskeeper by having groundskeeper witness it","witness",None),
    ("trace chest with groundskeeper by reporting gatehouse","report","gatehouse"),
    ("investigate chest with groundskeeper via reporting it at orchard path","report","orchard path"),
    ("trace chest with groundskeeper by asking what groundskeeper witnessed","recall_witness",None),
    ("trace chest with groundskeeper by asking about the unverified report","recall_report",None),
    ("trace chest with groundskeeper by following the eyewitness lead","follow_witness",None),
    ("trace chest with groundskeeper by following the reported lead","follow_report",None),
    ("trace chest with groundskeeper by checking chest by touch","touch",None),
    ("trace chest with groundskeeper by inspecting the chest myself","player_inspect",None),
    ("trace chest with groundskeeper by pushing chest to orchard","push_east",None),
    ("trace chest with groundskeeper by teleporting the chest","unqualified",None),
])
def test_parser_preserves_distinct_source_method(raw,method,place):
    p=parse_chest_investigation(raw)
    assert p is not None
    assert p.raw_text==raw and p.method==method and p.report_place==place


@pytest.mark.parametrize("raw",[
    "ask groundskeeper where they last saw chest",
    "ask groundskeeper to investigate last witnessed lead of chest",
    "ask groundskeeper to follow reported location of chest",
    "tell groundskeeper chest is at gatehouse",
    "inspect chest",
    "look",
    "get chest to orchard by pushing",
    "prepare chest for orchard by manual service",
    "trace lantern with groundskeeper",
    "trace chest with merchant",
    "trace chest with groundskeeper by witnessing it then pushing it",
    "trace chest with groundskeeper by reporting yard and following it",
    "trace chest with groundskeeper by pushing it afterwards inspecting",
])
def test_no_capture_of_existing_intents_or_compound_actions(raw):
    assert parse_chest_investigation(raw) is None


def test_unqualified_report_place_fails_closed_without_inventing_evidence():
    """A recognizable goal with unsupported content is a refusal, not canon."""
    text="trace chest with groundskeeper by reporting the moon"
    parsed=parse_chest_investigation(text)
    assert parsed is not None
    assert parsed.method=="unqualified"
    assert parsed.report_place is None

    app=MyravantVSM14Application.new()
    before=app.authoritative_digest()
    refusal=execute_chest_investigation(app,text)
    assert refusal.failure_class=="chest_investigation_method_unqualified"
    assert refusal.result_type=="chest_investigation_unavailable"
    assert not refusal.authoritative_changed
    assert refusal.pre_state_digest==refusal.post_state_digest==before
    assert app.authoritative_digest()==before
    assert not app.knowledge_state.events

    together_in_yard(app)
    local_before=app.authoritative_digest()
    refusal=execute_chest_investigation(app,text)
    assert refusal.failure_class=="chest_investigation_method_unqualified"
    assert refusal.pre_state_digest==refusal.post_state_digest==local_before
    assert app.authoritative_digest()==local_before
    assert not app.knowledge_state.events


def test_unseen_leads_remote_dialogue_and_unqualified_method_do_not_mutate():
    app=MyravantVSM14Application.new()
    before=app.authoritative_digest()
    for method in (
        None,"following the eyewitness lead",
        "asking about the unverified report","checking chest by touch",
    ):
        result=attempt(app,method)
        assert result.failure_class=="chest_investigation_actor_not_local"
        assert not result.authoritative_changed
        assert result.pre_state_digest==result.post_state_digest==before
    assert app.authoritative_digest()==before
    together_in_yard(app)
    before=app.authoritative_digest()
    empty=attempt(app)
    assert "no recorded" in empty.message
    assert not empty.authoritative_changed
    assert empty.pre_state_digest==empty.post_state_digest==before
    unknown=attempt(app,"following the eyewitness lead")
    assert unknown.failure_class=="actor_knowledge_unknown"
    unsupported=attempt(app,"teleporting the chest")
    assert unsupported.failure_class=="chest_investigation_method_unqualified"
    assert app.authoritative_digest()==before
    assert not app.knowledge_state.events


def test_conflicting_provenance_chooses_real_npc_route_but_not_world_truth(tmp_path):
    app=MyravantVSM14Application.new(
        checkpoint_path=tmp_path/"contested-leads.json",
    )
    assert app.pickup("lantern").authoritative_changed
    assert app.light_object("lantern").authoritative_changed
    together_in_yard(app)

    seen=attempt(app,"having groundskeeper witness it")
    assert seen.authoritative_changed
    assert seen.result_type=="actor_knowledge_committed"
    assert seen.receipt_id and seen.observation_evidence_id
    firsthand=last_actor_evidence(
        app.knowledge_state,GROUNDSKEEPER_ID,TOOL_CHEST_ID,
        source_kind="witnessed",
    )
    assert firsthand is not None
    assert firsthand.source_actor_id==GROUNDSKEEPER_ID
    assert firsthand.reported_place_id==YARD_ID

    claim=attempt(app,"reporting gatehouse")
    assert claim.authoritative_changed
    assert claim.result_type=="actor_knowledge_committed"
    assert claim.receipt_id and claim.receipt_id!=seen.receipt_id
    report=last_actor_evidence(
        app.knowledge_state,GROUNDSKEEPER_ID,TOOL_CHEST_ID,
        source_kind="reported",
    )
    assert report is not None
    assert report.source_actor_id==PLAYER_ID
    assert report.reported_place_id==GATEHOUSE_ID

    pre=app.authoritative_digest()
    comparison=attempt(app)
    assert comparison.result_type=="chest_investigation_leads_observed"
    assert "Last firsthand sighting: Yard" in comparison.message
    assert "Last player's unverified report: Gatehouse" in comparison.message
    assert "historical sources" in comparison.message
    assert comparison.pre_state_digest==comparison.post_state_digest==pre
    assert app.authoritative_digest()==pre
    recalled=attempt(app,"asking what groundskeeper witnessed")
    heard=attempt(app,"asking about the unverified report")
    assert not recalled.authoritative_changed and not heard.authoritative_changed
    assert "last saw" in recalled.message and "You told me" in heard.message

    # Change authoritative world truth AFTER recording the two contrary
    # memories; neither historical statement magically tracks the Chest.
    pushed=attempt(app,"pushing chest to orchard")
    assert pushed.authoritative_changed
    assert pushed.result_type=="object_displacement_committed"
    assert pushed.receipt_id and pushed.state_delta_id
    assert app.authoritative_digest()!=pre

    follow_report=attempt(app,"following the reported lead")
    assert follow_report.result_type=="actor_memory_followup_committed"
    assert follow_report.authoritative_changed and follow_report.receipt_id
    assert "reported lead" in follow_report.message
    assert app.entity_place_id(GROUNDSKEEPER_ID)==GATEHOUSE_ID
    assert app.current_place_id()==YARD_ID
    assert app.save().checkpoint_digest

    recovered=MyravantVSM14Application.restore(
        checkpoint_path=app.checkpoint_path,
    )
    assert recovered.authoritative_digest()==app.authoritative_digest()
    assert recovered.knowledge_state.events==app.knowledge_state.events
    assert recovered.entity_place_id(GROUNDSKEEPER_ID)==GATEHOUSE_ID
    assert recovered.move("south").authoritative_changed
    follow_witness=attempt(recovered,"following the eyewitness lead")
    assert follow_witness.result_type=="actor_memory_followup_committed"
    assert "witnessed lead" in follow_witness.message
    assert recovered.entity_place_id(GROUNDSKEEPER_ID)==YARD_ID
    assert recovered.move("north").authoritative_changed
    pre=recovered.authoritative_digest()
    touch=attempt(recovered,"checking chest by touch")
    assert touch.failure_class=="actor_contact_opportunity_unavailable"
    assert recovered.authoritative_digest()==pre
    comparison_again=attempt(recovered)
    assert "Last firsthand sighting: Yard" in comparison_again.message
    assert "Last player's unverified report: Gatehouse" in comparison_again.message
    assert comparison_again.pre_state_digest==pre

    # An actual visit with light, not actor hearsay, verifies the moved Chest.
    assert recovered.move("east").authoritative_changed
    local=attempt(recovered,"inspecting the chest myself")
    assert not local.authoritative_changed
    assert local.failure_class is None
    assert local.view is not None
    assert "Tool Chest" in local.view.name
    assert recovered.save().checkpoint_digest
    final=MyravantVSM14Application.restore(
        checkpoint_path=recovered.checkpoint_path,
    )
    assert final.authoritative_digest()==recovered.authoritative_digest()


def test_unverified_report_is_persistent_evidence_not_npc_sight():
    app=MyravantVSM14Application.new()
    together_in_yard(app)
    claim=attempt(app,"reporting orchard path")
    assert claim.authoritative_changed
    assert len(app.knowledge_state.events)==1
    before=app.authoritative_digest()
    compare=attempt(app)
    assert "No firsthand sighting" in compare.message
    assert "Last player's unverified report: Orchard Path" in compare.message
    assert compare.pre_state_digest==compare.post_state_digest==before
    denied=attempt(app,"following the reported lead")
    assert denied.failure_class=="actor_knowledge_followup_route_unavailable"
    assert app.authoritative_digest()==before
    witnessed=attempt(app,"asking what groundskeeper witnessed")
    assert witnessed.failure_class=="actor_knowledge_unknown"
    assert app.authoritative_digest()==before


def test_touch_is_present_contact_not_persistent_witness():
    app=MyravantVSM14Application.new()
    together_in_yard(app)
    before=app.authoritative_digest()
    touched=attempt(app,"checking chest by touch")
    assert touched.result_type=="actor_contact_observed"
    assert touched.observation_evidence_id
    assert not touched.authoritative_changed
    assert touched.pre_state_digest==touched.post_state_digest==before
    assert not app.knowledge_state.events
    compare=attempt(app)
    assert "no recorded" in compare.message
    assert app.authoritative_digest()==before


def test_player_local_inspection_does_not_require_npc_presence():
    app=MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    inspected=attempt(app,"inspecting the chest myself")
    assert inspected.view is not None
    assert not inspected.authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID)!=app.current_place_id()
    assert not app.knowledge_state.events


def test_repeated_history_deterministic_receipts_and_claims():
    timelines=[]
    for _ in range(2):
        app=MyravantVSM14Application.new()
        together_in_yard(app)
        a=attempt(app,"having groundskeeper witness it")
        b=attempt(app,"reporting gatehouse")
        c=attempt(app)
        d=attempt(app,"following the reported lead")
        assert a.authoritative_changed and b.authoritative_changed
        assert d.authoritative_changed
        timelines.append((
            a.receipt_id,b.receipt_id,d.receipt_id,
            c.message,c.pre_state_digest,c.post_state_digest,
            app.authoritative_digest(),app.knowledge_state.events,
        ))
    assert timelines[0]==timelines[1]


def test_public_inquiry_help_renders_actual_line_breaks():
    from astra_runtime.myravant_terminal import _write_help

    stream=StringIO()
    visible=_write_help(stream,"inquiry")
    assert "trace chest with groundskeeper" in visible
    assert "stale.\nFor conflicting local Chest leads" in visible
    assert r"stale.\nFor conflicting" not in visible
    assert visible in stream.getvalue()


def test_installed_client_two_session_contested_investigation(tmp_path):
    checkpoint=tmp_path/"trial3-evidence.json"
    def client(commands,*args):
        return subprocess.run(
            [sys.executable,"-m","astra_runtime.myravant_terminal",*args],
            input="\n".join((*commands,"exit","")),text=True,
            capture_output=True,timeout=120,
        )
    a=client((
        "go south","wait",
        "trace chest with groundskeeper",
        "trace chest with groundskeeper by having groundskeeper witness it",
        "trace chest with groundskeeper by reporting gatehouse",
        "trace chest with groundskeeper",
        "trace chest with groundskeeper by pushing chest to orchard",
        "trace chest with groundskeeper by following the reported lead",
    ),"--checkpoint",str(checkpoint))
    assert a.returncode==0,(a.stdout,a.stderr)
    assert "Last firsthand sighting: Yard" in a.stdout
    assert "Last player's unverified report: Gatehouse" in a.stdout
    assert checkpoint.is_file()
    restored=MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert len(restored.knowledge_state.events)==2
    assert restored.entity_place_id(GROUNDSKEEPER_ID)==GATEHOUSE_ID
    b=client((
        "go south",
        "trace chest with groundskeeper by following the eyewitness lead",
        "go north",
        "trace chest with groundskeeper by checking chest by touch",
        "trace chest with groundskeeper",
        "go east",
    ),"--load",str(checkpoint))
    assert b.returncode==0,(b.stdout,b.stderr)
    assert "cannot establish direct contact" in b.stdout
    final=MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert final.current_place_id()==ORCHARD_PATH_ID
    assert final.entity_place_id(GROUNDSKEEPER_ID)==YARD_ID
    assert len(final.knowledge_state.events)==2
