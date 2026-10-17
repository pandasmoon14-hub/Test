"""PLAY-CONTACT-AFFORDANCE-COMPOSITION-1: actual sensing/manipulation gameplay.

Implementation-authored acceptance, not blind independent held-out acceptance.
Existing AFQR-20 contact evidence is never persisted as knowledge or mistaken
for AFQR-18/19 authority. All transitions use existing COMP-3 contracts.
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
    LANTERN_ID, TOOL_CHEST_ID, WAYSTONE_ID, YARD_ID, WORKSHOP_ID, ORCHARD_PATH_ID,
)
from astra_runtime.myravant_terminal import (
    _explicit_two_step_intent, parse_terminal_command,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _place(app, target):
    return tuple(
        rel.object_entity_id for rel in app.state.representation.relations
        if rel.relation_type == LOCATED_AT_RELATION_TYPE
        and rel.subject_entity_id == target
    )


def _dark_orchard(app):
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    assert app.current_place_id() == ORCHARD_PATH_ID
    assert app.inspect("waystone").failure_class == "inspection_target_unavailable"


def _scenario(tmp_path, suffix):
    path = tmp_path / (suffix + ".json")
    app = MyravantVSM14Application.new(checkpoint_path=path)
    _dark_orchard(app)
    before = app.authoritative_digest()
    contact = app.feel_for_local_object("waystone")
    assert contact.result_type == "player_contact_observed"
    assert contact.observation_evidence_id
    assert contact.pre_state_digest == contact.post_state_digest == before
    assert not contact.authoritative_changed
    assert app.authoritative_digest() == before
    assert app.knowledge_state.events == ()

    moved = app.displace_object("waystone", "west", method="drag")
    assert moved.result_type == "object_displacement_committed"
    assert moved.authoritative_changed and moved.receipt_id and moved.state_delta_id
    assert moved.observation_evidence_id == contact.observation_evidence_id
    assert _place(app, WAYSTONE_ID) == (YARD_ID,)
    assert app.knowledge_state.events == ()

    # Prior contact becomes stale as soon as authoritative placement changes.
    digest = app.authoritative_digest()
    stale = app.displace_object("waystone", "west", method="drag")
    assert stale.failure_class == "object_displacement_target_unavailable"
    assert stale.pre_state_digest == stale.post_state_digest == digest
    assert stale.receipt_id is None
    assert app.authoritative_digest() == digest

    assert app.move("west").authoritative_changed
    digest = app.authoritative_digest()
    blocked = app.move("east")
    assert not blocked.authoritative_changed
    assert blocked.failure_class and "obstructs" in blocked.message
    assert blocked.pre_state_digest == blocked.post_state_digest == digest
    assert app.authoritative_digest() == digest
    cleared = app.displace_object("waystone", "north", method="push")
    assert cleared.authoritative_changed and cleared.receipt_id != moved.receipt_id
    assert _place(app, WAYSTONE_ID) == (WORKSHOP_ID,)
    assert app.move("east").authoritative_changed
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _place(restored, WAYSTONE_ID) == (WORKSHOP_ID,)
    assert restored.current_place_id() == ORCHARD_PATH_ID
    return moved.receipt_id, cleared.receipt_id, app.authoritative_digest()


def test_dark_contact_drag_changes_real_corridor_and_replays(tmp_path):
    assert _scenario(tmp_path, "first") == _scenario(tmp_path, "second")


@pytest.mark.parametrize("target,expected_failure", (
    ("chest", "object_displacement_target_unavailable"),
    ("waystone", "object_displacement_target_unavailable"),
    ("unknown trinket", "object_displacement_target_unavailable"),
))
def test_remote_or_unknown_target_cannot_be_dragged_from_name(target, expected_failure):
    app = MyravantVSM14Application.new()
    initial = app.authoritative_digest()
    refused = app.displace_object(target, "west", method="drag")
    assert refused.failure_class == expected_failure
    assert refused.pre_state_digest == refused.post_state_digest == initial
    assert refused.receipt_id is None and refused.state_delta_id is None
    assert "Yard" not in refused.message and "Orchard" not in refused.message


def test_chest_contact_in_darkness_does_not_qualify_unlicensed_route():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    assert app.displace_object("chest", "east", method="slide").authoritative_changed
    assert app.move("east").authoritative_changed
    assert app.inspect("chest").failure_class == "inspection_target_unavailable"
    pre = app.authoritative_digest()
    sensed = app.feel_for_local_object("chest")
    assert sensed.result_type == "player_contact_observed"
    assert sensed.pre_state_digest == sensed.post_state_digest == pre

    refused = app.displace_object("chest", "west", method="drag")
    assert refused.failure_class == "object_displacement_route_unavailable"
    assert refused.observation_evidence_id == sensed.observation_evidence_id
    assert refused.receipt_id is None
    assert refused.pre_state_digest == refused.post_state_digest == pre
    assert app.authoritative_digest() == pre
    assert _place(app, TOOL_CHEST_ID) == (ORCHARD_PATH_ID,)
    assert app.knowledge_state.events == ()


def test_chest_visible_drag_preserves_open_state_condition_and_old_receipts():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    seen = app.visual_observation_evidence(TOOL_CHEST_ID)
    assert seen.observable
    assert app.feel_for_local_object("chest").result_type == "player_contact_observed"
    assert app.open_object("chest").authoritative_changed
    pre = app.authoritative_digest()
    refused = app.displace_object("chest", "north", method="drag")
    assert refused.failure_class == "object_displacement_opportunity_unavailable"
    assert refused.pre_state_digest == refused.post_state_digest == pre
    assert app.close_object("chest").authoritative_changed
    moved = app.displace_object("chest", "north", method="drag")
    assert moved.authoritative_changed and moved.receipt_id
    assert moved.observation_evidence_id is None
    assert _place(app, TOOL_CHEST_ID) == (WORKSHOP_ID,)


def test_unqualified_lantern_contact_and_contained_drag_do_not_bypass_targeting():
    app = MyravantVSM14Application.new()
    denied = app.feel_for_local_object("lantern")
    assert denied.failure_class == "player_contact_affordance_unavailable"
    assert app.light_object("lantern").authoritative_changed
    assert app.displace_object("lantern", "south", method="slide").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.open_object("chest").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    assert app.store_object("lantern", "chest").authoritative_changed
    assert app.close_object("chest").authoritative_changed
    assert any(
        r.relation_type == CONTAINED_BY_RELATION_TYPE
        and r.subject_entity_id == LANTERN_ID
        and r.object_entity_id == TOOL_CHEST_ID
        for r in app.state.representation.relations
    )
    before = app.authoritative_digest()
    refused = app.displace_object("lantern", "south", method="drag")
    assert refused.failure_class == "object_displacement_target_unavailable"
    assert refused.pre_state_digest == refused.post_state_digest == before
    assert app.authoritative_digest() == before


@pytest.mark.parametrize("utterance,steps", (
    ("feel for waystone then drag waystone west", ("player_sense", "drag")),
    ("touch the chest then drag chest north", ("player_sense", "drag")),
    ("search by touch for waystone then drag waystone west", ("player_sense", "drag")),
    ("check my hands then go south", ("player_sense", "move")),
))
def test_bounded_two_step_reuses_existing_sensory_parser(utterance, steps):
    result = _explicit_two_step_intent(utterance)
    assert result is not None
    assert tuple(s.action for s in result) == steps
    assert parse_terminal_command(utterance).action == "unsupported"


@pytest.mark.parametrize("utterance", (
    "feel for it then drag it west",
    "feel for waystone then drag waystone west then go west",
    "touch waystone then save",
    "touch waystone and drag waystone west",
    "touch waystone then invent wings",
))
def test_unbounded_or_ambiguous_two_step_is_not_accepted(utterance):
    assert _explicit_two_step_intent(utterance) is None


def _play(tmp_path, name, commands, *, resume=False):
    launcher = shutil.which("myravant-play")
    assert launcher is not None, "installed myravant-play launcher required"
    save = tmp_path / f"{name}.json"
    trace = tmp_path / f"{name}{'-resume' if resume else ''}.jsonl"
    args = [launcher, "--checkpoint", str(save), "--trace", str(trace),
            "--repository-sha", "c" * 40]
    if resume:
        args.extend(["--load", str(save)])
    run = subprocess.run(
        args, input="\n".join((*commands, "save", "exit", "")),
        text=True, capture_output=True, timeout=100,
    )
    assert run.returncode == 0, (run.stdout, run.stderr)
    records = [json.loads(x) for x in trace.read_text(encoding="utf-8").splitlines()]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    assert records[-1]["evidence_complete"] is True
    actions = [x for x in records if x["record_type"] == "interaction"]
    assert actions[-1]["result_type"] == "checkpoint_written"
    for first, second in zip(actions, actions[1:]):
        assert first["post_state_digest"] == second["pre_state_digest"]
    return run, actions[:-1], MyravantVSM14Application.restore(checkpoint_path=save)


def test_installed_client_two_step_sense_drag_obstruction_and_persistence(tmp_path):
    executions = []
    for name in ("one", "two"):
        output, rows, restored = _play(
            tmp_path, name,
            (
                "go south", "go east", "inspect waystone",
                "feel for waystone then drag waystone west",
                "go west", "go east", "push waystone north then go east",
            ),
        )
        assert "Sequence step 1/2" in output.stdout
        assert "Sequence step 2/2" in output.stdout
        assert "You make direct contact with Weathered Waystone" in output.stdout
        assert "You drag the Weathered Waystone west." in output.stdout
        assert "obstructs" in output.stdout
        assert [r["parsed_action"] for r in rows if r["parsed_action"].startswith("sequence_")] == [
            "sequence_1_player_sense", "sequence_2_drag",
            "sequence_1_push", "sequence_2_move",
        ]
        read = next(r for r in rows if r["parsed_action"] == "sequence_1_player_sense")
        drag = next(r for r in rows if r["parsed_action"] == "sequence_2_drag")
        assert read["result_type"] == "player_contact_observed"
        assert not read["authoritative_changed"]
        assert read["pre_state_digest"] == read["post_state_digest"]
        assert read["observation_evidence_id"]
        assert drag["authoritative_changed"] and drag["receipt_id"] and drag["state_delta_id"]
        assert drag["observation_evidence_id"] == read["observation_evidence_id"]
        assert drag["pre_state_digest"] == read["post_state_digest"]
        assert _place(restored, WAYSTONE_ID) == (WORKSHOP_ID,)
        assert restored.current_place_id() == ORCHARD_PATH_ID
        assert restored.knowledge_state.events == ()
        executions.append(tuple(
            (r["parsed_action"], r["result_type"], r["receipt_id"],
             r["pre_state_digest"], r["post_state_digest"])
            for r in rows
        ))
        follow, newrows, again = _play(
            tmp_path, name, ("look for waystone",), resume=True,
        )
        assert again.authoritative_digest() == restored.authoritative_digest()
        assert newrows[0]["pre_state_digest"] == newrows[0]["post_state_digest"]
    assert executions[0] == executions[1]


def test_installed_contact_refusal_halts_sequence_and_preserves_digest(tmp_path):
    _, records, restored = _play(
        tmp_path, "failed-contact",
        ("feel for waystone then drag waystone west",),
    )
    assert len(records) == 1
    assert records[0]["parsed_action"] == "sequence_1_player_sense"
    assert records[0]["failure_class"] == "player_contact_opportunity_unavailable"
    assert not records[0]["authoritative_changed"]
    assert records[0]["pre_state_digest"] == records[0]["post_state_digest"]
    assert _place(restored, WAYSTONE_ID) == (ORCHARD_PATH_ID,)
    assert restored.current_place_id() == WORKSHOP_ID


def test_installed_contact_success_does_not_license_chest_route(tmp_path):
    _, records, restored = _play(
        tmp_path, "denied-chest-route",
        ("go south", "touch chest then drag chest east"),
    )
    assert [r["parsed_action"] for r in records][-2:] == [
        "sequence_1_player_sense", "sequence_2_drag",
    ]
    touch, denied = records[-2:]
    assert touch["result_type"] == "player_contact_observed"
    assert not touch["authoritative_changed"]
    assert denied["failure_class"] == "object_displacement_route_unavailable"
    assert denied["pre_state_digest"] == denied["post_state_digest"]
    assert not denied["authoritative_changed"]
    assert _place(restored, TOOL_CHEST_ID) == (YARD_ID,)
