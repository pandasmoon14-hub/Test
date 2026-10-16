"""#493 / #495: actual two-step player intentions over existing owners.

No workflow engine is authoritative here: the public client parses *exactly*
two independent methods and resolves each with normal owner validation and
durable acknowledgement. Unsupported or ambiguous step plans fail before the
first mutation; contextual refusal after a lawful first step is not rollback.
"""
from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.myravant_terminal import (
    _parse_explicit_two_step_intent, parse_terminal_command,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID, TOOL_CHEST_ID, WORKSHOP_ID, YARD_ID,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE, CONTAINED_BY_RELATION_TYPE,
)


def launch(tmp_path, label, commands, *, load=False):
    executable = shutil.which("myravant-play")
    assert executable is not None
    checkpoint=tmp_path/f"{label}.json"
    trace=tmp_path/f"{label}.jsonl"
    opts=(["--load",str(checkpoint)] if load else
          ["--checkpoint",str(checkpoint)])
    p=subprocess.run(
        [executable,*opts,"--trace",str(trace),"--repository-sha","a"*40],
        input="\n".join((*commands,"save","exit","")),
        capture_output=True,text=True,timeout=120,
    )
    assert p.returncode==0,(p.stdout,p.stderr)
    records=[json.loads(x) for x in trace.read_text(encoding="utf-8").splitlines()]
    assert records[0]["record_type"]=="session_start"
    assert records[-1]["record_type"]=="session_end"
    steps=[x for x in records if x["record_type"]=="interaction"]
    return p.stdout,checkpoint,steps


@pytest.mark.parametrize("raw,actions",[
    ("go south then inspect chest",("move","inspect")),
    ("take lantern then go south",("pickup","move")),
    ("open chest then put lantern in chest",("open","store")),
    ("look then wait",("look","wait")),
    ("move south then inspect myself",("move","inspect_self")),
    ("go south then look east",("move","look_direction")),
    ("wait then go south",("wait","move")),
])
def test_two_simple_steps_use_original_parser_contract(raw,actions):
    pieces=_parse_explicit_two_step_intent(raw)
    assert pieces is not None
    assert tuple(x.action for x in pieces)==actions
    assert parse_terminal_command(raw).action=="unsupported"


@pytest.mark.parametrize("raw",[
    "go south then cast a spell",
    "go south then save",
    "go south then ask groundskeeper to follow me",
    "go south then",
    "then inspect chest",
    "go south then inspect chest then wait",
    "pickup it then move south",
    "go south then look around then attack",
])
def test_unsupported_or_ambiguous_plans_never_half_execute(raw):
    assert _parse_explicit_two_step_intent(raw)==()


@pytest.mark.parametrize("raw",[
    "go south while inspecting chest",
    "take lantern and go south",
    "go south",
    "do that again",
])
def test_nonsequential_intents_are_not_hijacked(raw):
    assert _parse_explicit_two_step_intent(raw) is None


def test_two_owner_transitions_match_equivalent_independent_inputs(tmp_path):
    combo_output,combo_cp,combined=launch(
        tmp_path,"combined",("take lantern then go south",),
    )
    separate_output,separate_cp,separate=launch(
        tmp_path,"separate",("take lantern","go south"),
    )
    combined_state=MyravantVSM14Application.restore(checkpoint_path=combo_cp)
    separate_state=MyravantVSM14Application.restore(checkpoint_path=separate_cp)
    assert combined_state.authoritative_digest()==separate_state.authoritative_digest()
    assert combined_state.current_place_id()==YARD_ID
    assert "Step 1/2 (pickup):" in combo_output
    assert "Step 2/2 (move):" in combo_output
    assert len(combined)==3 and len(separate)==3
    assert combined[0]["parsed_action"]=="sequential_step_1_pickup"
    assert combined[1]["parsed_action"]=="sequential_step_2_move"
    assert combined[0]["raw_player_input"]==combined[1]["raw_player_input"]==(
        "take lantern then go south\n"
    )
    assert all(x["authoritative_changed"] for x in combined[:2])
    assert combined[0]["post_state_digest"]==combined[1]["pre_state_digest"]
    assert combined[1]["post_state_digest"]==combined_state.authoritative_digest()
    assert [x["post_state_digest"] for x in combined[:2]]==[
        x["post_state_digest"] for x in separate[:2]
    ]


def test_multisystem_lantern_to_chest_two_session_replay(tmp_path):
    output,path,first=launch(
        tmp_path,"multi",("take lantern then go south",),
    )
    assert all(x["authoritative_changed"] for x in first[:2])
    staged=MyravantVSM14Application.restore(checkpoint_path=path)
    assert staged.current_place_id()==YARD_ID
    assert any(
        x.subject_entity_id==LANTERN_ID
        and x.relation_type==CARRIED_BY_RELATION_TYPE
        for x in staged.state.representation.relations
    )
    second_output,path,second=launch(
        tmp_path,"multi",("open chest then put lantern in chest",),load=True,
    )
    assert "Step 1/2 (open):" in second_output
    assert "Step 2/2 (store):" in second_output
    assert len(second)==3 and all(x["authoritative_changed"] for x in second[:2])
    assert second[0]["post_state_digest"]==second[1]["pre_state_digest"]
    final=MyravantVSM14Application.restore(checkpoint_path=path)
    assert final.current_place_id()==YARD_ID
    assert any(
        x.subject_entity_id==LANTERN_ID
        and x.object_entity_id==TOOL_CHEST_ID
        and x.relation_type==CONTAINED_BY_RELATION_TYPE
        for x in final.state.representation.relations
    )
    assert final.authoritative_digest()==second[1]["post_state_digest"]
    assert final.authoritative_digest()!=staged.authoritative_digest()


def test_second_step_contextual_failure_does_not_rewind_movement(tmp_path):
    output,path,steps=launch(
        tmp_path,"failed-second",("go south then take nonexistent artifact",),
    )
    assert len(steps)==3
    assert steps[0]["authoritative_changed"]
    assert not steps[1]["authoritative_changed"]
    assert steps[1]["failure_class"]
    assert steps[0]["post_state_digest"]==steps[1]["pre_state_digest"]
    assert steps[1]["pre_state_digest"]==steps[1]["post_state_digest"]
    restored=MyravantVSM14Application.restore(checkpoint_path=path)
    assert restored.current_place_id()==YARD_ID
    assert "Step 2/2" in output


def test_first_step_contextual_failure_stops_before_next_action(tmp_path):
    output,path,steps=launch(tmp_path,"failed-first",(
        "go north then take lantern",
    ))
    assert len(steps)==2 # failed first step, then explicit save
    assert steps[0]["failure_class"]=="unavailable_fixture_route"
    assert not steps[0]["authoritative_changed"]
    assert "The second step was not attempted" in output
    app=MyravantVSM14Application.restore(checkpoint_path=path)
    assert app.current_place_id()==WORKSHOP_ID
    assert not any(
        x.subject_entity_id==LANTERN_ID
        and x.relation_type==CARRIED_BY_RELATION_TYPE
        for x in app.state.representation.relations
    )


def test_unqualified_plan_preserves_world_and_one_refusal_trace(tmp_path):
    output,path,records=launch(
        tmp_path,"unqualified",("go south then invent a flying castle",),
    )
    assert "no step was attempted" in output
    assert len(records)==2
    assert records[0]["result_type"]=="sequential_intent_refused"
    assert records[0]["failure_class"]=="sequential_intent_step_unqualified"
    assert records[0]["pre_state_digest"]==records[0]["post_state_digest"]
    assert MyravantVSM14Application.restore(checkpoint_path=path).current_place_id()==WORKSHOP_ID


def test_hidden_remote_information_not_invented_by_sequence(tmp_path):
    output,path,records=launch(
        tmp_path,"hidden",("go south then inspect waystone",),
    )
    assert records[0]["authoritative_changed"]
    assert not records[1]["authoritative_changed"]
    assert records[1]["failure_class"]
    assert records[1]["pre_state_digest"]==records[1]["post_state_digest"]
    assert "Orchard Path" not in records[1]["player_visible_output"]
    assert MyravantVSM14Application.restore(checkpoint_path=path).current_place_id()==YARD_ID


def test_repeated_two_step_world_time_is_deterministic(tmp_path):
    results=[]
    for which in ("a","b"):
        _,cp,rows=launch(tmp_path,which,("go south then wait",))
        assert rows[0]["authoritative_changed"]
        assert rows[1]["authoritative_changed"]
        assert rows[0]["post_state_digest"]==rows[1]["pre_state_digest"]
        results.append((
            rows[0]["post_state_digest"],rows[1]["post_state_digest"],
            MyravantVSM14Application.restore(checkpoint_path=cp).authoritative_digest(),
        ))
    assert results[0]==results[1]
