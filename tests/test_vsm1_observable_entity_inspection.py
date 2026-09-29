# VSM-1 regressions for bounded observable object-or-actor inspection.

from __future__ import annotations

from dataclasses import replace
from io import StringIO

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_terminal import (
    parse_terminal_command,
    run_terminal,
)


def _move_player_to_gatehouse(app: MyravantPlayApplication) -> None:
    first = app.move("south")
    second = app.move("south")
    assert first.result_type == second.result_type == "movement_committed"
    assert app.current_place_id() == GATEHOUSE_ID


def test_vsm1_fixture_inspection_reference_resolves_objects_and_actor():
    fixture = create_terminal_play_fixture()

    assert fixture.resolve_inspection_reference("lantern") == LANTERN_ID
    assert (
        fixture.resolve_inspection_reference("groundskeeper")
        == GROUNDSKEEPER_ID
    )


def test_vsm1_visible_actor_is_inspectable_without_authoritative_change():
    app = MyravantPlayApplication.new()
    _move_player_to_gatehouse(app)
    before = app.authoritative_digest()
    movement_count = len(app.state.committed_transitions)

    result = app.inspect("groundskeeper")

    assert result.result_type == "inspection"
    assert result.authoritative_changed is False
    assert result.view is not None
    assert result.view.name == "Groundskeeper"
    assert (
        result.view.description
        == "A quiet groundskeeper tends the bounded test grounds."
    )
    assert result.pre_state_digest == before == result.post_state_digest
    assert result.command_id is None
    assert result.command_fingerprint is None
    assert result.preview_id is None
    assert result.receipt_id is None
    assert result.state_delta_id is None
    assert app.authoritative_digest() == before
    assert len(app.state.committed_transitions) == movement_count


def test_vsm1_remote_actor_and_unknown_reference_are_nonrevealing_equivalents():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    remote = app.inspect("groundskeeper")
    unknown = app.inspect("steward")

    assert remote.result_type == unknown.result_type == "inspection_unavailable"
    assert (
        remote.failure_class
        == unknown.failure_class
        == "inspection_target_unavailable"
    )
    assert remote.message == unknown.message
    assert remote.pre_state_digest == remote.post_state_digest == before
    assert unknown.pre_state_digest == unknown.post_state_digest == before
    assert app.authoritative_digest() == before


def test_vsm1_actor_inspection_remains_gated_by_existing_visual_observation():
    base = create_terminal_play_fixture()
    conditions = dict(base.ambient_visual_conditions)
    conditions[GATEHOUSE_ID] = "insufficient"
    dark_fixture = replace(
        base,
        ambient_visual_conditions=conditions,
    )
    app = MyravantPlayApplication.new(fixture=dark_fixture)
    _move_player_to_gatehouse(app)
    before = app.authoritative_digest()

    result = app.inspect("groundskeeper")

    assert result.result_type == "inspection_unavailable"
    assert result.failure_class == "inspection_target_unavailable"
    assert result.pre_state_digest == before == result.post_state_digest
    assert app.authoritative_digest() == before


def test_vsm1_existing_object_inspection_behavior_remains_available():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.inspect("lantern")

    assert result.result_type == "inspection"
    assert result.view is not None
    assert result.view.name == "Brass Lantern"
    assert "well-handled surface" in result.view.description
    assert "Its flame is out." in result.view.description
    assert result.pre_state_digest == before == result.post_state_digest
    assert app.authoritative_digest() == before


def test_vsm1_parser_already_routes_actor_inspection_without_new_action_family():
    cases = (
        ("inspect groundskeeper", "groundskeeper"),
        ("examine groundskeeper", "groundskeeper"),
        ("look at groundskeeper", "groundskeeper"),
        ("look closely at the groundskeeper", "groundskeeper"),
    )
    for raw, argument in cases:
        parsed = parse_terminal_command(raw)
        assert parsed.action == "inspect"
        assert parsed.argument == argument


def test_vsm1_terminal_actor_inspection_is_player_visible_and_nonmutating():
    app = MyravantPlayApplication.new()
    output = StringIO()

    run_terminal(
        app,
        input_stream=StringIO(
            "move south\n"
            "move south\n"
            "inspect groundskeeper\n"
            "exit\n"
        ),
        output_stream=output,
    )

    text = output.getvalue()
    assert "Groundskeeper" in text
    assert "A quiet groundskeeper tends the bounded test grounds." in text
    assert len(app.state.committed_transitions) == 2
    assert app.custody_state.committed_custody_transitions == ()
    assert app.object_state.committed_object_state_transitions == ()
    assert app.lit_state.committed_object_lit_transitions == ()
    assert app.storage_state.committed_storage_transitions == ()
