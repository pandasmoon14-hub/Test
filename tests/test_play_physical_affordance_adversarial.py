"""Supplemental non-blind player probes, authored after PR #531 implementation.

This corpus is NOT independent Set A/B acceptance. It pressures control flow,
false successes, hidden information and cross-system execution via the actual
installed launcher, without editing the original 39-case baseline.
"""
from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID, TOOL_CHEST_ID, WORKSHOP_ID, YARD_ID, ORCHARD_PATH_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


PROBES = (
    # A lawful first step remains committed when its conditional second step
    # fails; the failed second step must not move a currently open Chest.
    (
        "open_then_slide",
        ("go south", "open chest then slide chest east"),
        "object_displacement_opportunity_unavailable", YARD_ID, YARD_ID,
    ),
    # Taking custody does not also grant ground contact for dragging.
    (
        "custody_then_drag",
        ("take lantern then drag lantern south",),
        "object_displacement_target_unavailable", WORKSHOP_ID, YARD_ID,
    ),
    # Naming a remote object never licenses action or subsequent locomotion.
    (
        "remote_slide_then_move",
        ("slide chest east then go east",),
        "object_displacement_target_unavailable", WORKSHOP_ID, YARD_ID,
    ),
    # Same location/destination but differing licensed methods: east drag
    # refuses without changing state, while push then move commits.
    (
        "unsupported_then_qualified",
        ("go south", "drag chest east", "push chest east then go east"),
        "object_displacement_route_unavailable", ORCHARD_PATH_ID, ORCHARD_PATH_ID,
    ),
    # Merely knowing the name/location of a dark target does not grant
    # visual access or dragging opportunity. Both denials are unchanged.
    (
        "dark_name_does_not_license_wrong_route",
        ("go south", "look for waystone", "go east", "drag waystone north"),
        "object_displacement_route_unavailable", ORCHARD_PATH_ID, YARD_ID,
    ),
    # Moving a closed but unlit Chest into Orchard cannot itself reveal
    # the Waystone in the dark.
    (
        "unlit_slide_then_look",
        ("go south", "slide chest east then go east", "look for waystone"),
        "focused_target_not_observed", ORCHARD_PATH_ID, ORCHARD_PATH_ID,
    ),
)


def _relation(app, subject_id, relation_type):
    return tuple(
        item for item in app.state.representation.relations
        if item.subject_entity_id == subject_id
        and item.relation_type == relation_type
    )


@pytest.mark.parametrize(
    "name,commands,expected_failure,player_place,chest_place",
    PROBES, ids=[item[0] for item in PROBES],
)
def test_supplemental_installed_player_adversaries(
    tmp_path, name, commands, expected_failure, player_place, chest_place,
):
    launcher = shutil.which("myravant-play")
    assert launcher is not None, "installed myravant-play is required"
    save = tmp_path / f"{name}.json"
    trace = tmp_path / f"{name}.jsonl"
    run = subprocess.run(
        [launcher, "--checkpoint", str(save), "--trace", str(trace)],
        input="\n".join((*commands, "save", "exit", "")),
        text=True, capture_output=True, timeout=90,
    )
    assert run.returncode == 0, (run.stdout, run.stderr)
    assert save.is_file() and trace.is_file()
    records = [json.loads(row) for row in trace.read_text(encoding="utf-8").splitlines()]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    assert records[-1]["evidence_complete"] is True
    actions = [r for r in records if r["record_type"] == "interaction"]
    assert actions[-1]["result_type"] == "checkpoint_written"
    refusals = [r for r in actions if r["failure_class"] == expected_failure]
    assert refusals, (name, [(r["parsed_action"], r["failure_class"]) for r in actions])
    assert all(
        not r["authoritative_changed"]
        and r["pre_state_digest"] == r["post_state_digest"]
        and r["receipt_id"] is None
        for r in refusals
    )
    for r in actions:
        if r["authoritative_changed"]:
            assert r["receipt_id"] and r["pre_state_digest"] != r["post_state_digest"]
        else:
            assert r["pre_state_digest"] == r["post_state_digest"]
    for earlier, later in zip(actions, actions[1:]):
        assert earlier["post_state_digest"] == later["pre_state_digest"]

    restored = MyravantVSM14Application.restore(checkpoint_path=save)
    assert restored.authoritative_digest() == actions[-1]["post_state_digest"]
    assert restored.current_place_id() == player_place
    assert restored.entity_place_id(TOOL_CHEST_ID) == chest_place

    if name == "open_then_slide":
        assert restored.object_open_state(TOOL_CHEST_ID).state == "open"
        assert not any(
            a["parsed_action"] == "sequence_2_slide" and a["authoritative_changed"]
            for a in actions
        )
    if name == "custody_then_drag":
        assert len(_relation(restored, LANTERN_ID, CARRIED_BY_RELATION_TYPE)) == 1
        assert not _relation(restored, LANTERN_ID, LOCATED_AT_RELATION_TYPE)
    if name in {"unsupported_then_qualified", "unlit_slide_then_look"}:
        assert any(
            a["parsed_action"] in {"sequence_1_push", "sequence_1_slide"}
            and a["authoritative_changed"] and a["receipt_id"]
            for a in actions
        )
    if name.startswith("dark") or name == "unlit_slide_then_look":
        assert any(
            a["failure_class"] in {
                "focused_target_not_observed",
                "object_displacement_target_unavailable",
            } for a in actions
        )

    resumed = subprocess.run(
        [launcher, "--load", str(save), "--checkpoint", str(save)],
        input="inspect myself\nsave\nexit\n", text=True,
        capture_output=True, timeout=90,
    )
    assert resumed.returncode == 0, (resumed.stdout, resumed.stderr)
    assert MyravantVSM14Application.restore(
        checkpoint_path=save,
    ).authoritative_digest() == restored.authoritative_digest()
