"""PLAY-PHYSICAL-AFFORDANCE-1: distinct licensed placement methods, not physics.

All world changes still execute through existing COMP-3/RT-010 ownership.
These are authored integration tests, not independent held-out acceptance.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from io import StringIO

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    containment_relation_for,
)
from astra_runtime.myravant_physical_placement_goal import (
    execute_physical_placement_goal,
)
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID,
    ORCHARD_PATH_ID,
    TOOL_CHEST_ID,
    WAYSTONE_ID,
    WORKSHOP_ID,
    YARD_ID,
    UnavailableFixtureDisplacementError,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _place(app, object_id: str) -> str:
    matches = [
        rel.object_entity_id
        for rel in app.state.representation.relations
        if rel.relation_type == LOCATED_AT_RELATION_TYPE
        and rel.subject_entity_id == object_id
    ]
    assert len(matches) == 1
    return matches[0]


@pytest.mark.parametrize("object_id,source,direction,method,destination,condition", [
    (LANTERN_ID, WORKSHOP_ID, "south", "drag", YARD_ID, None),
    (TOOL_CHEST_ID, YARD_ID, "north", "drag", WORKSHOP_ID, "closed"),
    (TOOL_CHEST_ID, YARD_ID, "east", "slide", ORCHARD_PATH_ID, "closed"),
    (WAYSTONE_ID, YARD_ID, "north", "slide", WORKSHOP_ID, None),
])
def test_four_new_fixture_qualifications_have_exact_targets_and_conditions(
    object_id, source, direction, method, destination, condition,
):
    fixture = create_terminal_play_fixture()
    routes = [
        route for route in fixture.object_displacement_routes
        if (route.object_entity_id, route.source_place_id,
            route.direction, route.method) == (object_id, source, direction, method)
    ]
    assert len(routes) == 1
    assert routes[0].destination_place_id == destination
    assert routes[0].required_open_state == condition
    assert fixture.object_displacement_destination_for(
        object_entity_id=object_id, source_place_id=source,
        direction=direction, method=method,
    ) == destination
    assert fixture.provenance.canon is False


@pytest.mark.parametrize("object_id,source,direction,method", [
    (WAYSTONE_ID, ORCHARD_PATH_ID, "north", "slide"),
    (TOOL_CHEST_ID, YARD_ID, "east", "drag"),
    (LANTERN_ID, WORKSHOP_ID, "north", "drag"),
])
def test_other_routes_are_not_implicitly_inferred(object_id, source, direction, method):
    with pytest.raises(UnavailableFixtureDisplacementError):
        create_terminal_play_fixture().object_displacement_destination_for(
            object_entity_id=object_id, source_place_id=source,
            direction=direction, method=method,
        )


def test_chest_drag_and_push_have_different_open_state_opportunities(tmp_path):
    app = MyravantVSM14Application.new(
        checkpoint_path=tmp_path / "chest-drag.json",
    )
    assert app.move("south").authoritative_changed
    assert app.open_object("chest").authoritative_changed
    inquiry = execute_physical_placement_goal(app, "get chest to workshop")
    assert not inquiry.authoritative_changed
    assert "push north" in inquiry.message
    assert "drag north (requires the object to be closed)" in inquiry.message

    before = app.authoritative_digest()
    denied = app.displace_object("chest", "north", method="drag")
    assert denied.failure_class == "object_displacement_opportunity_unavailable"
    assert denied.pre_state_digest == denied.post_state_digest == before
    assert app.authoritative_digest() == before
    assert _place(app, TOOL_CHEST_ID) == YARD_ID

    assert app.close_object("chest").authoritative_changed
    moved = app.displace_object("chest", "north", method="drag")
    assert moved.authoritative_changed and moved.receipt_id and moved.state_delta_id
    assert moved.spatial_evidence_id and moved.opportunity_evidence_id
    assert _place(app, TOOL_CHEST_ID) == WORKSHOP_ID
    assert app.displacement_state.committed_object_displacement_transitions[-1].receipt.method == "drag"
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _place(restored, TOOL_CHEST_ID) == WORKSHOP_ID

    other = MyravantVSM14Application.new()
    assert other.move("south").authoritative_changed
    assert other.open_object("chest").authoritative_changed
    still_pushable = other.displace_object("chest", "north", method="push")
    assert still_pushable.authoritative_changed
    assert _place(other, TOOL_CHEST_ID) == WORKSHOP_ID


def _illuminated_waystone_at_yard(app):
    for action in (
        lambda: app.pickup("lantern"),
        lambda: app.light_object("lantern"),
        lambda: app.move("south"),
        lambda: app.move("east"),
        lambda: app.displace_object("waystone", "west", method="drag"),
        lambda: app.move("west"),
    ):
        assert action().authoritative_changed


def test_waystone_slide_changes_a_real_exit_opportunity_and_replays(tmp_path):
    def scenario(path):
        app = MyravantVSM14Application.new(checkpoint_path=path)
        _illuminated_waystone_at_yard(app)
        assert _place(app, WAYSTONE_ID) == YARD_ID
        before = app.authoritative_digest()
        blocked = app.move("east")
        assert blocked.failure_class and not blocked.authoritative_changed
        assert app.authoritative_digest() == before

        moved = execute_physical_placement_goal(
            app, "clear yard east exit by sliding",
        )
        assert moved.authoritative_changed
        assert moved.receipt_id and moved.state_delta_id
        assert _place(app, WAYSTONE_ID) == WORKSHOP_ID
        assert app.displacement_state.committed_object_displacement_transitions[-1].receipt.method == "slide"
        assert app.move("east").authoritative_changed
        assert app.save().checkpoint_digest
        restored = MyravantVSM14Application.restore(checkpoint_path=path)
        assert restored.authoritative_digest() == app.authoritative_digest()
        assert _place(restored, WAYSTONE_ID) == WORKSHOP_ID
        return moved.receipt_id, app.authoritative_digest()

    assert scenario(tmp_path / "route-one.json") == scenario(
        tmp_path / "route-two.json"
    )


def test_lantern_drag_then_chest_slide_preserves_real_containment(tmp_path):
    app = MyravantVSM14Application.new(checkpoint_path=tmp_path / "cargo.json")
    dragged = app.displace_object("lantern", "south", method="drag")
    assert dragged.authoritative_changed
    assert _place(app, LANTERN_ID) == YARD_ID
    assert app.move("south").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    assert app.open_object("chest").authoritative_changed
    assert app.store_object("lantern", "chest").authoritative_changed
    containment = containment_relation_for(app.storage_state, LANTERN_ID)
    assert containment and containment.object_entity_id == TOOL_CHEST_ID

    before = app.authoritative_digest()
    refused = app.displace_object("chest", "east", method="slide")
    assert refused.failure_class == "object_displacement_opportunity_unavailable"
    assert app.authoritative_digest() == before
    assert app.close_object("chest").authoritative_changed

    slid = execute_physical_placement_goal(
        app, "move chest to orchard by sliding",
    )
    assert slid.authoritative_changed and slid.receipt_id
    assert _place(app, TOOL_CHEST_ID) == ORCHARD_PATH_ID
    assert containment_relation_for(app.storage_state, LANTERN_ID) == containment
    assert app.save().checkpoint_digest

    restored = MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _place(restored, TOOL_CHEST_ID) == ORCHARD_PATH_ID
    assert containment_relation_for(restored.storage_state, LANTERN_ID) == containment


def test_existing_two_step_dispatch_executes_new_method_and_durably_restores(tmp_path):
    app = MyravantVSM14Application.new(checkpoint_path=tmp_path / "two-step.json")
    output = StringIO()
    code = run_terminal(
        app, input_stream=StringIO("drag lantern south then go south\nlook\nexit\n"),
        output_stream=output,
    )
    assert code == 0
    assert "Sequence step 1/2:" in output.getvalue()
    assert "Sequence step 2/2:" in output.getvalue()
    assert _place(app, LANTERN_ID) == YARD_ID
    assert app.current_place_id() == YARD_ID
    assert app.checkpoint_path.is_file()
    restored = MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == app.authoritative_digest()


def test_installed_client_adapts_to_refusal_then_restores_new_placement(tmp_path):
    installed = shutil.which("myravant-play")
    assert installed, "real installed myravant-play executable required"
    checkpoint = tmp_path / "adaptive.json"

    def run(commands, *, resume=False, phase=1):
        trace = tmp_path / f"phase-{phase}.jsonl"
        args = ["--load" if resume else "--checkpoint", str(checkpoint)]
        result = subprocess.run(
            [installed, *args, "--trace", str(trace)],
            input="\n".join((*commands, "exit", "")), text=True,
            capture_output=True, timeout=90,
        )
        assert result.returncode == 0, (result.stdout, result.stderr)
        rows = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
        return result.stdout, [
            row for row in rows if row["record_type"] == "interaction"
        ]

    first, rows = run(
        ("go south", "open chest", "drag chest north"), phase=1,
    )
    assert "container must be closed" in first
    assert rows[-1]["failure_class"] == "object_displacement_opportunity_unavailable"
    assert rows[-1]["pre_state_digest"] == rows[-1]["post_state_digest"]
    after_refusal = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert _place(after_refusal, TOOL_CHEST_ID) == YARD_ID

    # The next action is selected from the *observed* refusal, not a
    # preset unobserved success. The two steps remain separately durable.
    next_action = "close chest" if "container must be closed" in first else "look"
    second, second_rows = run(
        (next_action, "drag chest north then go north", "inspect chest"),
        resume=True, phase=2,
    )
    assert "Sequence step 1/2:" in second
    assert "Sequence step 2/2:" in second
    assert any(
        row["receipt_id"] and row["authoritative_changed"]
        for row in second_rows if row["parsed_action"].startswith("sequence_")
    )
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert _place(restored, TOOL_CHEST_ID) == WORKSHOP_ID
    assert restored.current_place_id() == WORKSHOP_ID

    third, third_rows = run(("slide chest south",), resume=True, phase=3)
    assert "cannot slide" in third
    assert third_rows[-1]["failure_class"] == "object_displacement_route_unavailable"
    assert third_rows[-1]["pre_state_digest"] == third_rows[-1]["post_state_digest"]
    after_negative = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert after_negative.authoritative_digest() == restored.authoritative_digest()
