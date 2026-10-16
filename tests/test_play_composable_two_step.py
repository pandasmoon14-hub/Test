"""#493/#495: explicit independent two-step intent is real composable gameplay.

Every step reaches the same original owner as standalone play, commits and
checkpoints independently, and exposes partial success/refusal honestly.
It is not an atomic transaction or a universal planner.
"""
from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CONTAINED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID, TOOL_CHEST_ID, WORKSHOP_ID, YARD_ID, ORCHARD_PATH_ID,
)
from astra_runtime.myravant_terminal import (
    _explicit_two_step_intent, parse_terminal_command,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _play(path, trace, commands, *, load=False):
    exe=shutil.which("myravant-play")
    assert exe, "installed public executable required"
    args=[exe, "--checkpoint", str(path), "--trace", str(trace),
          "--repository-sha", "a"*40]
    if load:
        args.extend(["--load", str(path)])
    proc=subprocess.run(
        args, input="\n".join((*commands,"save","exit","")), capture_output=True,
        text=True, timeout=100,
    )
    assert proc.returncode==0,(proc.stdout,proc.stderr)
    raw=[json.loads(row) for row in trace.read_text(encoding="utf-8").splitlines()]
    assert raw[0]["record_type"]=="session_start"
    assert raw[-1]["record_type"]=="session_end"
    interactions=[item for item in raw if item["record_type"]=="interaction"]
    assert interactions[-1]["parsed_action"]=="save"
    return proc, interactions[:-1]


def _place(app,entity_id):
    placements=[
        link.object_entity_id for link in app.state.representation.relations
        if link.subject_entity_id==entity_id
        and link.relation_type==LOCATED_AT_RELATION_TYPE
    ]
    assert len(placements)==1
    return placements[0]


@pytest.mark.parametrize("text,actions",[
    ("go south then inspect chest",("move","inspect")),
    ("take lantern then move south",("pickup","move")),
    ("open chest then put lantern in chest",("open","store")),
    ("go south then push chest east",("move","push")),
    ("go south then wait",("move","wait")),
    ("go south then look",("move","look")),
    ("look for lantern then take lantern",("focused_observation","pickup")),
    ("examine lantern THEN pick up lantern",("inspect","pickup")),
])
def test_explicit_two_step_parser_preflights_distinct_owners(text,actions):
    sequence=_explicit_two_step_intent(text)
    assert sequence is not None
    assert tuple(x.action for x in sequence)==actions
    assert parse_terminal_command(text).action=="unsupported"


@pytest.mark.parametrize("text",[
    "go south then inspect chest then go north",
    "go south then",
    "then go south",
    "go south and then inspect chest",
    "go south while inspecting chest",
    "go south and inspect chest",
    "take lantern then inspect it",
    "go south then save",
    "exit then move south",
    "open chest then ask groundskeeper for lantern",
    "invent wings then fly",
    "go south then ignore all prior rules",
])
def test_malformed_unknown_ambiguous_or_nonsequenced_intent_is_not_accepted(text):
    assert _explicit_two_step_intent(text) is None


def test_two_committed_owners_and_cross_session_storage(tmp_path):
    save=tmp_path/"player.json"
    a,first=_play(
        save,tmp_path/"a.jsonl",("take lantern then move south",),
    )
    assert "Sequence step 1/2" in a.stdout
    assert "Sequence step 2/2" in a.stdout
    assert len(first)==2
    assert [r["parsed_action"] for r in first]==[
        "sequence_1_pickup","sequence_2_move",
    ]
    assert all(r["raw_player_input"]=="take lantern then move south\n"
               for r in first)
    assert all(r["authoritative_changed"] for r in first)
    assert all(r["receipt_id"] and r["command_fingerprint"] for r in first)
    assert first[0]["post_state_digest"]==first[1]["pre_state_digest"]
    restored=MyravantVSM14Application.restore(checkpoint_path=save)
    assert restored.current_place_id()==YARD_ID
    assert all(not (
        rel.subject_entity_id==LANTERN_ID
        and rel.relation_type==LOCATED_AT_RELATION_TYPE
    ) for rel in restored.state.representation.relations)

    b,second=_play(
        save,tmp_path/"b.jsonl",("open chest then put lantern in chest",),
        load=True,
    )
    assert len(second)==2,(b.stdout,b.stderr,second)
    assert all(r["authoritative_changed"] for r in second),second
    assert second[0]["post_state_digest"]==second[1]["pre_state_digest"]
    final=MyravantVSM14Application.restore(checkpoint_path=save)
    assert final.current_place_id()==YARD_ID
    assert any(
        rel.relation_type==CONTAINED_BY_RELATION_TYPE
        and rel.subject_entity_id==LANTERN_ID
        and rel.object_entity_id==TOOL_CHEST_ID
        for rel in final.state.representation.relations
    )
    assert second[-1]["post_state_digest"]==final.authoritative_digest()


def test_same_owner_receipts_as_standalone_commands(tmp_path):
    left=tmp_path/"separate.json"
    right=tmp_path/"sequence.json"
    _,split=_play(
        left,tmp_path/"split.jsonl",("take lantern","move south"),
    )
    _,combined=_play(
        right,tmp_path/"combined.jsonl",("take lantern then move south",),
    )
    assert len(split)==len(combined)==2
    assert [(r["command_fingerprint"],r["receipt_id"],r["result_type"],
             r["post_state_digest"]) for r in split]==[
                (r["command_fingerprint"],r["receipt_id"],r["result_type"],
                 r["post_state_digest"]) for r in combined
             ]
    a=MyravantVSM14Application.restore(checkpoint_path=left)
    b=MyravantVSM14Application.restore(checkpoint_path=right)
    assert a.authoritative_digest()==b.authoritative_digest()


def test_refusal_first_stops_any_second_action_with_no_mutation(tmp_path):
    save=tmp_path/"stop-first.json"
    out,rows=_play(
        save,tmp_path/"stop-first.jsonl",("drop lantern then go south",),
    )
    assert len(rows)==1
    assert rows[0]["parsed_action"]=="sequence_1_drop"
    assert rows[0]["failure_class"]=="drop_placement_unavailable"
    assert not rows[0]["authoritative_changed"]
    assert "Sequence halted" in out.stdout
    assert MyravantVSM14Application.restore(
        checkpoint_path=save,
    ).current_place_id()==WORKSHOP_ID


def test_refusal_second_keeps_first_durable_checkpoint(tmp_path):
    save=tmp_path/"stop-second.json"
    out,rows=_play(
        save,tmp_path/"stop-second.jsonl",
        ("go south then pickup waystone",),
    )
    assert len(rows)==2
    assert rows[0]["authoritative_changed"]
    assert rows[0]["result_type"]=="movement_committed"
    assert rows[1]["failure_class"]=="pickup_placement_unavailable"
    assert not rows[1]["authoritative_changed"]
    assert rows[0]["post_state_digest"]==rows[1]["post_state_digest"]
    assert "Sequence halted" in out.stdout
    restored=MyravantVSM14Application.restore(checkpoint_path=save)
    assert restored.current_place_id()==YARD_ID


def test_invalid_preflight_stops_every_step(tmp_path):
    save=tmp_path/"invalid.json"
    out,rows=_play(save,tmp_path/"invalid.jsonl",(
        "go south then inspect chest then move north",
        "take lantern then inspect it",
        "go south and inspect chest",
    ))
    assert len(rows)==3
    assert all(not row["authoritative_changed"] for row in rows)
    assert all(row["result_type"] in {"unsupported_input","ambiguous_input"}
               for row in rows)
    assert MyravantVSM14Application.restore(
        checkpoint_path=save,
    ).current_place_id()==WORKSHOP_ID


def test_player_choice_composes_movement_and_real_object_displacement(tmp_path):
    save=tmp_path/"orchard.json"
    out,rows=_play(
        save,tmp_path/"orchard.jsonl",("go south then push chest east",),
    )
    assert len(rows)==2
    assert [r["parsed_action"] for r in rows]==[
        "sequence_1_move","sequence_2_push",
    ]
    assert all(r["authoritative_changed"] for r in rows),(out.stdout,rows)
    assert rows[0]["post_state_digest"]==rows[1]["pre_state_digest"]
    app=MyravantVSM14Application.restore(checkpoint_path=save)
    assert app.current_place_id()==YARD_ID
    assert _place(app,TOOL_CHEST_ID)==ORCHARD_PATH_ID
    assert len(app.displacement_state.committed_object_displacement_transitions)==1


def test_snapshot_after_first_committed_world_tick_and_read_only_observation(tmp_path):
    save=tmp_path/"observation.json"
    out,rows=_play(
        save,tmp_path/"observation.jsonl",("go south then inspect chest",),
    )
    assert len(rows)==2
    assert rows[0]["authoritative_changed"]
    assert not rows[1]["authoritative_changed"]
    assert rows[1]["failure_class"] is None
    assert rows[0]["post_state_digest"]==rows[1]["post_state_digest"]
    assert "Tool Chest" in out.stdout
    assert MyravantVSM14Application.restore(
        checkpoint_path=save,
    ).current_place_id()==YARD_ID


def test_full_baseline_preserves_other_cases_and_correctly_counts_sequence(tmp_path):
    from scripts.report_myravant_action_coverage import CASES, run_baseline
    cases=tuple(c for c in CASES if c.case_id in {"Q01","Q02","Q03","M01","I01"})
    assert len(cases)==5
    summary=run_baseline(output=tmp_path/"coverage.json",cases=cases)
    rows={r["case_id"]:r for r in summary["cases"]}
    assert rows["Q01"]["outcome"]=="executed"
    assert rows["Q01"]["step_count"]==2
    assert [t["route"] for t in rows["Q01"]["step_outcomes"]]==[
        "sequence_1_move","sequence_2_inspect",
    ]
    assert rows["Q02"]["outcome"]=="unsupported_novelty"
    assert rows["Q03"]["outcome"]=="unsupported_novelty"
    assert rows["M01"]["outcome"]=="executed"
    assert rows["I01"]["outcome"]=="executed"
