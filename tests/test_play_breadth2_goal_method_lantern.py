"""PLAY-BREADTH-2: one goal, distinct authoritatively qualified methods.

No new object relocation authority or automatic multi-step executor.
Exercise source location/control, actor cooperation, exact owner receipts,
physical downstream consequences, installed play and deterministic replay.
"""
from __future__ import annotations

import subprocess
import sys

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_goal_method_lantern import (
    parse_lantern_destination_goal, execute_lantern_destination_goal,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, LANTERN_ID, ORCHARD_PATH_ID, PLAYER_ID, YARD_ID,
)
from astra_runtime.myravant_terminal_capabilities import (
    execute_bounded_terminal_request,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _at_yard_carrying(app):
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.current_place_id() == YARD_ID


def _placement(app):
    matches = [
        (r.relation_type, r.object_entity_id)
        for r in app.state.representation.relations
        if r.subject_entity_id == LANTERN_ID
        and r.relation_type in {LOCATED_AT_RELATION_TYPE, CARRIED_BY_RELATION_TYPE}
    ]
    assert len(matches) == 1
    return matches[0]


def _last_displacement(app):
    return app.displacement_state.committed_object_displacement_transitions[-1].receipt


@pytest.mark.parametrize("expression,expected", [
    ("get lantern to orchard", None),
    ("send the lantern to orchard path", None),
    ("How do I get lantern to orchard?", None),
    ("I want to deliver lantern onto the orchard path", None),
    ("move brass lantern to orchard by pushing", "push"),
    ("send lantern to orchard by pushing it", "push"),
    ("bring lantern to orchard with a push", "push"),
    ("put lantern onto orchard path using shove", "push"),
    ("get lantern to orchard via throw", "throw"),
    ("send the brass lantern to the orchard by tossing it", "throw"),
    ("take lantern to orchard path by throwing it", "throw"),
    ("I need to get lantern to orchard by asking groundskeeper", "actor_throw"),
    ("deliver lantern to orchard using groundskeeper", "actor_throw"),
    ("send lantern to orchard by asking the groundskeeper to throw it", "actor_throw"),
    ("bring lantern to orchard via having the groundskeeper throw it", "actor_throw"),
    ("send lantern to orchard by rolling it", "unqualified"),
])
def test_structured_goal_and_explicit_method_probes(expression, expected):
    parsed = parse_lantern_destination_goal(expression)
    assert parsed is not None
    assert parsed.destination == "orchard_path"
    assert parsed.method == expected
    assert parsed.raw_text == expression


@pytest.mark.parametrize("other", [
    "ask groundskeeper to bring lantern to orchard",
    "ask groundskeeper for lantern",
    "push lantern east",
    "throw lantern east",
    "go east",
    "take lantern",
    "deliver a chest to orchard by pushing",
    "send lantern to workshop by throwing",
    "ask the town council for a charter",
    "get that to orchard",
    "get lantern to orchard and wait",
])
def test_interpretation_does_not_capture_other_goals_or_commands(other):
    assert parse_lantern_destination_goal(other) is None


def test_contextual_goal_query_changes_with_custody_without_mutation():
    app = MyravantVSM14Application.new()
    at_workshop = execute_lantern_destination_goal(
        app, "How do I get lantern to orchard?"
    )
    assert at_workshop.failure_class == "destination_goal_worksite_not_local"
    _at_yard_carrying(app)
    before = app.authoritative_digest()
    held = execute_lantern_destination_goal(app, "get lantern to orchard")
    assert held.result_type == "destination_goal_methods_observed"
    assert "You carry the Lantern" in held.message
    assert "throwing it" in held.message
    assert "first put it down" in held.message
    assert held.pre_state_digest == held.post_state_digest == before
    assert not held.authoritative_changed

    assert app.drop("lantern").authoritative_changed
    pre_ground = app.authoritative_digest()
    grounded = execute_lantern_destination_goal(app, "send lantern to orchard")
    assert "grounded here" in grounded.message
    assert "pushing it" in grounded.message
    assert "first take it" in grounded.message
    assert grounded.pre_state_digest == grounded.post_state_digest == pre_ground
    assert app.authoritative_digest() == pre_ground


def test_player_push_and_throw_reach_same_real_goal_with_distinct_owner_evidence(tmp_path):
    receipts = []
    for method in ("push", "throw"):
        app = MyravantVSM14Application.new(
            checkpoint_path=tmp_path / (method + ".json")
        )
        _at_yard_carrying(app)
        if method == "push":
            assert app.drop("lantern").authoritative_changed
        before = app.authoritative_digest()
        result = execute_lantern_destination_goal(
            app, f"get lantern to orchard by {method}"
        )
        assert result.authoritative_changed
        assert result.result_type == "object_displacement_committed"
        assert result.receipt_id and result.command_id
        assert result.state_delta_id and result.preview_id
        assert result.post_state_digest == app.authoritative_digest()
        assert result.post_state_digest != before
        receipt = _last_displacement(app)
        assert receipt.receipt_id == result.receipt_id
        assert receipt.method == method
        assert receipt.actor_entity_id == PLAYER_ID
        assert receipt.destination_place_id == ORCHARD_PATH_ID
        assert receipt.source_relation_type == (
            LOCATED_AT_RELATION_TYPE if method == "push"
            else CARRIED_BY_RELATION_TYPE
        )
        assert _placement(app) == (LOCATED_AT_RELATION_TYPE, ORCHARD_PATH_ID)

        assert app.save().checkpoint_digest
        restored = MyravantVSM14Application.restore(
            checkpoint_path=app.checkpoint_path
        )
        assert restored.authoritative_digest() == app.authoritative_digest()
        assert _last_displacement(restored) == receipt
        receipts.append(receipt)
    assert receipts[0].method != receipts[1].method
    assert receipts[0].command_fingerprint != receipts[1].command_fingerprint


def test_willing_npc_method_preserves_control_and_performing_actor_identity(tmp_path):
    app = MyravantVSM14Application.new(
        checkpoint_path=tmp_path / "npc-goal.json"
    )
    _at_yard_carrying(app)
    denied = execute_lantern_destination_goal(
        app, "deliver lantern to orchard with groundskeeper"
    )
    assert denied.failure_class == "vsm13_requested_actor_not_local"
    assert not denied.authoritative_changed

    assert app.wait().authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    still_player_held = execute_lantern_destination_goal(
        app, "send lantern to orchard by asking groundskeeper"
    )
    assert still_player_held.failure_class == "vsm13_comp3_opportunity_unavailable"
    assert _placement(app) == (CARRIED_BY_RELATION_TYPE, PLAYER_ID)

    assert app.give_object("lantern", "groundskeeper").authoritative_changed
    before = app.authoritative_digest()
    successful = execute_lantern_destination_goal(
        app, "send lantern to orchard by asking groundskeeper"
    )
    assert successful.authoritative_changed
    assert successful.result_type == "actor_mediated_displacement_committed"
    assert successful.post_state_digest == app.authoritative_digest()
    assert successful.post_state_digest != before
    receipt = _last_displacement(app)
    assert receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.method == "throw"
    assert receipt.source_relation_type == CARRIED_BY_RELATION_TYPE
    assert receipt.destination_place_id == ORCHARD_PATH_ID
    assert _placement(app) == (LOCATED_AT_RELATION_TYPE, ORCHARD_PATH_ID)
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(
        checkpoint_path=app.checkpoint_path,
    )
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _last_displacement(restored) == receipt


def test_explicit_wrong_method_and_unavailable_control_never_commit():
    app = MyravantVSM14Application.new()
    _at_yard_carrying(app)
    before = app.authoritative_digest()
    roll = execute_lantern_destination_goal(
        app, "send lantern to orchard by rolling it"
    )
    assert roll.failure_class == "destination_goal_method_unqualified"
    assert roll.pre_state_digest == roll.post_state_digest == before
    assert app.authoritative_digest() == before

    denied = execute_lantern_destination_goal(
        app, "get lantern to orchard by pushing"
    )
    assert denied.failure_class == "object_displacement_target_unavailable"
    assert app.authoritative_digest() == before
    assert app.drop("lantern").authoritative_changed
    before_ground = app.authoritative_digest()
    denied_throw = execute_lantern_destination_goal(
        app, "get lantern to orchard by throwing"
    )
    assert denied_throw.failure_class == "object_displacement_target_unavailable"
    assert app.authoritative_digest() == before_ground


def test_cross_domain_lit_asset_recovered_after_goal_and_return(tmp_path):
    app = MyravantVSM14Application.new(
        checkpoint_path=tmp_path / "return.json",
    )
    _at_yard_carrying(app)
    assert app.light_object("lantern").authoritative_changed
    assert execute_lantern_destination_goal(
        app, "move lantern to orchard via throw"
    ).authoritative_changed
    assert app.move("east").authoritative_changed
    inspected = app.inspect("lantern")
    assert inspected.result_type == "inspection"
    assert "lit" in inspected.view.description
    recovered = app.pickup("lantern")
    assert recovered.authoritative_changed
    assert _placement(app) == (CARRIED_BY_RELATION_TYPE, PLAYER_ID)
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(
        checkpoint_path=app.checkpoint_path,
    )
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _placement(restored) == (CARRIED_BY_RELATION_TYPE, PLAYER_ID)


def test_two_identical_adaptive_goal_paths_are_deterministic():
    traces = []
    for _ in range(2):
        app = MyravantVSM14Application.new()
        assert app.pickup("lantern").authoritative_changed
        assert app.move("south").authoritative_changed
        choice = execute_lantern_destination_goal(
            app, "how do i get lantern to orchard"
        )
        assert not choice.authoritative_changed
        assert "throw" in choice.message
        outcome = execute_lantern_destination_goal(
            app, "send lantern to orchard by tossing it"
        )
        assert outcome.authoritative_changed
        assert app.move("east").authoritative_changed
        traces.append((
            outcome.receipt_id, outcome.state_delta_id,
            _last_displacement(app), app.authoritative_digest(),
        ))
    assert traces[0] == traces[1]


def test_installed_client_goal_choice_and_two_session_resume(tmp_path):
    checkpoint = tmp_path / "goal-client.json"

    def run(commands, *flags):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal", *flags],
            input="\n".join((*commands, "exit", "")), text=True,
            capture_output=True, timeout=120,
        )

    first = run((
        "take lantern", "go south",
        "How do I get lantern to orchard?",
        "send lantern to orchard by rolling it",
        "send lantern to orchard by throwing",
    ), "--checkpoint", str(checkpoint))
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "You carry the Lantern" in first.stdout
    assert "no qualified local way" in first.stdout
    assert "You throw the Brass Lantern east." in first.stdout
    assert checkpoint.is_file()

    resumed = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert _placement(resumed) == (LOCATED_AT_RELATION_TYPE, ORCHARD_PATH_ID)
    later = run((
        "go east", "look", "send lantern to orchard by pushing",
    ), "--load", str(checkpoint))
    assert later.returncode == 0, (later.stdout, later.stderr)
    assert "You need to reach the Yard" in later.stdout
    after = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert after.current_place_id() == ORCHARD_PATH_ID
    assert _placement(after) == (LOCATED_AT_RELATION_TYPE, ORCHARD_PATH_ID)
