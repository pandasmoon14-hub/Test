"""PLAY-BREADTH-3: source-local multi-target method, condition and consequence.

These examples exercise different declared objects and places without
manufacturing a new universal object physics or goal owner.
"""
from __future__ import annotations

import subprocess
import sys

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CONTAINED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    containment_relation_for,
)
from astra_runtime.myravant_physical_placement_goal import (
    execute_physical_placement_goal, parse_physical_placement_goal,
)
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID, ORCHARD_PATH_ID, TOOL_CHEST_ID, WAYSTONE_ID,
    WORKSHOP_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _place(app, entity_id):
    links = [
        rel.object_entity_id for rel in app.state.representation.relations
        if rel.subject_entity_id == entity_id
        and rel.relation_type == LOCATED_AT_RELATION_TYPE
    ]
    assert len(links) == 1
    return links[0]


def _last(app):
    return app.displacement_state.committed_object_displacement_transitions[-1].receipt


def _orchard_with_lit_lantern(app):
    assert app.pickup("lantern").authoritative_changed
    assert app.light_object("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    assert app.current_place_id() == ORCHARD_PATH_ID


@pytest.mark.parametrize("raw,target,destination,method,clear", [
    ("get waystone to yard", WAYSTONE_ID, YARD_ID, None, False),
    ("move the weathered waystone into the yard by dragging",
     WAYSTONE_ID, YARD_ID, "drag", False),
    ("I need to get waystone to workshop by pushing",
     WAYSTONE_ID, WORKSHOP_ID, "push", False),
    ("send chest to orchard with a push",
     TOOL_CHEST_ID, ORCHARD_PATH_ID, "unqualified", False),
    ("put the tool chest onto orchard path using pushing it",
     TOOL_CHEST_ID, ORCHARD_PATH_ID, "push", False),
    ("how can I get chest to workshop", TOOL_CHEST_ID, WORKSHOP_ID, None, False),
    ("get chest to gatehouse by dragging", TOOL_CHEST_ID,
     "astra:entity:gatehouse", "drag", False),
    ("clear the yard east exit", WAYSTONE_ID, WORKSHOP_ID, None, True),
    ("clear east passage by pushing the waystone north",
     WAYSTONE_ID, WORKSHOP_ID, "push", True),
    ("I want to clear yard east route by dragging", WAYSTONE_ID,
     WORKSHOP_ID, "drag", True),
])
def test_goal_parser_retains_target_destination_method_and_goal(
    raw, target, destination, method, clear,
):
    parsed = parse_physical_placement_goal(raw)
    assert parsed is not None
    assert parsed.raw_text == raw
    assert (parsed.target_id, parsed.destination_id, parsed.method) == (
        target, destination, method,
    )
    assert parsed.clearance is clear


@pytest.mark.parametrize("raw", [
    "get lantern to orchard",
    "ask groundskeeper to bring lantern to orchard",
    "take chest",
    "move north",
    "push chest east",
    "drag waystone west",
    "put lantern in chest",
    "get that to the yard",
    "move the broken cart to workshop by pushing",
    "move chest to yard and wait",
    "clear the yard north exit",
    "clear yard east exit and then go east",
    "get waystone to unknown place",
])
def test_new_interpreter_never_claims_unrelated_semantics(raw):
    assert parse_physical_placement_goal(raw) is None


def test_illuminated_orchard_drag_then_clear_waystone_unblocks_real_exit(tmp_path):
    app = MyravantVSM14Application.new(checkpoint_path=tmp_path / "route.json")
    _orchard_with_lit_lantern(app)

    before = app.authoritative_digest()
    inquiry = execute_physical_placement_goal(app, "get waystone to yard")
    assert inquiry.result_type == "physical_goal_methods_observed"
    assert "drag west" in inquiry.message
    assert inquiry.pre_state_digest == inquiry.post_state_digest == before
    assert app.authoritative_digest() == before

    moved = execute_physical_placement_goal(
        app, "move waystone to yard by dragging",
    )
    assert moved.result_type == "object_displacement_committed"
    assert moved.receipt_id and moved.state_delta_id
    assert _place(app, WAYSTONE_ID) == YARD_ID
    drag = _last(app)
    assert drag.method == "drag"
    assert drag.source_place_id == ORCHARD_PATH_ID
    assert drag.destination_place_id == YARD_ID
    assert drag.receipt_id == moved.receipt_id

    assert app.move("west").authoritative_changed
    blocked_before = app.authoritative_digest()
    blocked = app.move("east")
    assert blocked.failure_class
    assert not blocked.authoritative_changed
    assert "obstructs" in blocked.message
    assert app.authoritative_digest() == blocked_before

    clearing = execute_physical_placement_goal(
        app, "clear yard east exit by pushing waystone north",
    )
    assert clearing.authoritative_changed
    assert _place(app, WAYSTONE_ID) == WORKSHOP_ID
    push = _last(app)
    assert push.method == "push"
    assert push.destination_place_id == WORKSHOP_ID
    assert push.receipt_id == clearing.receipt_id
    assert push.receipt_id != drag.receipt_id
    assert app.move("east").authoritative_changed
    assert app.current_place_id() == ORCHARD_PATH_ID
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _place(restored, WAYSTONE_ID) == WORKSHOP_ID
    assert restored.current_place_id() == ORCHARD_PATH_ID


def test_chest_open_condition_and_contained_lantern_migrate_lawfully(tmp_path):
    app = MyravantVSM14Application.new(checkpoint_path=tmp_path / "chest.json")
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.open_object("chest").authoritative_changed
    stored = app.store_object("lantern", "chest")
    assert stored.authoritative_changed
    containment = containment_relation_for(app.storage_state, LANTERN_ID)
    assert containment is not None
    assert containment.relation_type == CONTAINED_BY_RELATION_TYPE
    assert containment.object_entity_id == TOOL_CHEST_ID

    inspect = execute_physical_placement_goal(app, "how do i get chest to orchard")
    assert not inspect.authoritative_changed
    assert "push east" in inspect.message
    assert "requires the object to be closed" in inspect.message

    before_open = app.authoritative_digest()
    rejected = execute_physical_placement_goal(
        app, "move chest to orchard by pushing"
    )
    assert not rejected.authoritative_changed
    assert rejected.failure_class == "object_displacement_opportunity_unavailable"
    assert app.authoritative_digest() == before_open
    assert _place(app, TOOL_CHEST_ID) == YARD_ID

    assert app.close_object("chest").authoritative_changed
    moved = execute_physical_placement_goal(
        app, "move the tool chest to orchard path by pushing it",
    )
    assert moved.authoritative_changed and moved.receipt_id
    assert _place(app, TOOL_CHEST_ID) == ORCHARD_PATH_ID
    assert _last(app).method == "push"
    assert _last(app).receipt_id == moved.receipt_id
    assert containment_relation_for(app.storage_state, LANTERN_ID) == containment
    assert app.save().checkpoint_digest

    restored = MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _place(restored, TOOL_CHEST_ID) == ORCHARD_PATH_ID
    assert containment_relation_for(restored.storage_state, LANTERN_ID) == containment
    assert _last(restored) == _last(app)


def test_unsupported_and_remote_goals_refuse_without_revealing_remote_placement():
    app = MyravantVSM14Application.new()
    initial = app.authoritative_digest()
    for phrase, failure in [
        ("get waystone to yard", "physical_goal_local_evidence_unavailable"),
        ("move chest to orchard by pushing", "physical_goal_local_placement_unavailable"),
        ("get chest to workshop by teleporting it", "physical_goal_method_unqualified"),
    ]:
        result = execute_physical_placement_goal(app, phrase)
        assert result.failure_class == failure
        assert not result.authoritative_changed
        assert result.pre_state_digest == result.post_state_digest == initial
        assert app.authoritative_digest() == initial

    assert app.move("south").authoritative_changed
    before = app.authoritative_digest()
    for phrase, failure in [
        ("get chest to gatehouse by pushing", "physical_goal_route_unavailable"),
        ("move chest to orchard by dragging", "physical_goal_route_unavailable"),
        ("clear the yard east exit", "physical_goal_local_evidence_unavailable"),
    ]:
        rejected = execute_physical_placement_goal(app, phrase)
        assert rejected.failure_class == failure
        assert rejected.pre_state_digest == rejected.post_state_digest == before
        assert app.authoritative_digest() == before


def test_dark_waystone_drag_requires_existing_visual_opportunity():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    baseline = app.authoritative_digest()
    query = execute_physical_placement_goal(app, "get waystone to yard")
    assert query.failure_class == "physical_goal_local_evidence_unavailable"
    dragged = execute_physical_placement_goal(
        app, "get waystone to yard by dragging"
    )
    assert not dragged.authoritative_changed
    assert dragged.failure_class == "object_displacement_target_unavailable"
    assert app.authoritative_digest() == baseline


def test_two_identical_waystone_goal_histories_replay_deterministically():
    timelines = []
    for _ in range(2):
        app = MyravantVSM14Application.new()
        _orchard_with_lit_lantern(app)
        a = execute_physical_placement_goal(app, "get waystone to yard by dragging")
        assert a.authoritative_changed
        assert app.move("west").authoritative_changed
        b = execute_physical_placement_goal(
            app, "clear yard east exit by pushing the waystone north",
        )
        assert b.authoritative_changed
        timelines.append((a.receipt_id, b.receipt_id, _last(app),
                          app.authoritative_digest()))
    assert timelines[0] == timelines[1]


def test_installed_client_resumes_waystone_recovery_and_clearing(tmp_path):
    save_path = tmp_path / "multi-goal.json"

    def run(commands, *args):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal", *args],
            input="\n".join((*commands, "exit", "")), text=True,
            capture_output=True, timeout=120,
        )

    first = run((
        "take lantern", "light lantern", "go south", "go east",
        "get waystone to yard", "get waystone to yard by dragging",
    ), "--checkpoint", str(save_path))
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "drag west" in first.stdout
    assert "You drag the Weathered Waystone west." in first.stdout
    loaded = MyravantVSM14Application.restore(checkpoint_path=save_path)
    assert _place(loaded, WAYSTONE_ID) == YARD_ID
    assert loaded.current_place_id() == ORCHARD_PATH_ID

    second = run((
        "go west", "go east",
        "clear the yard east exit by pushing the waystone north", "go east",
    ), "--load", str(save_path))
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "Something obstructs that passage" in second.stdout
    assert "You push the Weathered Waystone north." in second.stdout
    after = MyravantVSM14Application.restore(checkpoint_path=save_path)
    assert _place(after, WAYSTONE_ID) == WORKSHOP_ID
    assert after.current_place_id() == ORCHARD_PATH_ID
