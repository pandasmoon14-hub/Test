"""VSM-5 focused/directional observation regressions."""

from __future__ import annotations

from io import StringIO

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    ORCHARD_PATH_ID,
    YARD_ID,
)
from astra_runtime.myravant_terminal import (
    parse_terminal_command,
    run_terminal,
)


def _yard_app(*, checkpoint_path=None) -> MyravantPlayApplication:
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint_path)
    moved = app.move("south")
    assert moved.result_type == "movement_committed"
    assert app.current_place_id() == YARD_ID
    return app


def test_vsm5_directional_sensing_is_not_movement_adjacency():
    app = _yard_app()

    assert app.fixture.destination_for(
        source_place_id=YARD_ID,
        direction="east",
    ) == ORCHARD_PATH_ID

    south = app.fixture.directional_observation_evidence(
        observer_entity_id=app.fixture.player_entity_id,
        source_place_id=YARD_ID,
        direction="south",
    )
    east = app.fixture.directional_observation_evidence(
        observer_entity_id=app.fixture.player_entity_id,
        source_place_id=YARD_ID,
        direction="east",
    )

    assert south.observable is True
    assert south.target_place_id == GATEHOUSE_ID
    assert south.basis == "explicit_fixture_directional_observation"

    assert east.observable is False
    assert east.target_place_id is None
    assert east.basis == "no_explicit_fixture_directional_observation"


def test_vsm5_yard_look_south_exposes_gatehouse_without_state_or_time_change():
    app = _yard_app()
    before_digest = app.authoritative_digest()
    before_place = app.current_place_id()
    before_time = app.runtime_state.logical_time_state.logical_position

    result = app.look_direction("south")

    assert result.result_type == "directional_observation"
    assert result.authoritative_changed is False
    assert result.pre_state_digest == before_digest
    assert result.post_state_digest == before_digest
    assert result.observation_evidence_id is not None
    assert result.view is not None
    assert result.view.source_place_id == YARD_ID
    assert result.view.direction == "south"
    assert result.view.target_place_id == GATEHOUSE_ID
    assert result.view.name == "Gatehouse"
    assert app.current_place_id() == before_place
    assert app.runtime_state.logical_time_state.logical_position == before_time
    assert app.authoritative_digest() == before_digest


def test_vsm5_yard_look_east_does_not_expose_orchard_despite_route():
    app = _yard_app()
    before = app.authoritative_digest()

    result = app.look_direction("east")

    assert result.result_type == "directional_observation_unavailable"
    assert result.authoritative_changed is False
    assert result.failure_class == "directional_observation_unlicensed"
    assert result.observation_evidence_id is not None
    assert result.view is None
    assert "Orchard" not in result.message
    assert app.current_place_id() == YARD_ID
    assert app.authoritative_digest() == before


def test_vsm5_carried_lit_lantern_does_not_grant_remote_east_visibility():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    assert app.move("south").result_type == "movement_committed"
    before = app.authoritative_digest()

    result = app.look_direction("east")

    assert result.result_type == "directional_observation_unavailable"
    assert result.failure_class == "directional_observation_unlicensed"
    assert result.view is None
    assert "Orchard" not in result.message
    assert app.authoritative_digest() == before


def test_vsm5_invalid_direction_rejects_safely_without_evidence_invention():
    app = _yard_app()
    before = app.authoritative_digest()

    result = app.look_direction("up")

    assert result.result_type == "directional_observation_unavailable"
    assert result.authoritative_changed is False
    assert result.failure_class == "directional_observation_invalid_direction"
    assert result.observation_evidence_id is None
    assert result.view is None
    assert app.authoritative_digest() == before


def test_vsm5_parser_adds_only_cardinal_directional_look_route():
    bare = parse_terminal_command("look")
    south = parse_terminal_command("look south")
    east = parse_terminal_command("look east")
    inspect = parse_terminal_command("look at the lantern")
    unsupported = parse_terminal_command("look southeast")

    assert bare.action == "look"
    assert south.action == "look_direction"
    assert south.argument == "south"
    assert east.action == "look_direction"
    assert east.argument == "east"
    assert inspect.action == "inspect"
    assert unsupported.action == "unsupported"


def test_vsm5_terminal_renders_gatehouse_directionally_without_moving_player():
    app = _yard_app()
    before = app.authoritative_digest()
    output = StringIO()

    code = run_terminal(
        app,
        input_stream=StringIO("look south\nexit\n"),
        output_stream=output,
    )

    assert code == 0
    rendered = output.getvalue()
    assert "To the south: Gatehouse" in rendered
    assert "A small gatehouse marks the southern edge" in rendered
    assert app.current_place_id() == YARD_ID
    assert app.authoritative_digest() == before


def test_vsm5_unlicensed_terminal_direction_does_not_leak_target_place():
    app = _yard_app()
    before = app.authoritative_digest()
    output = StringIO()

    code = run_terminal(
        app,
        input_stream=StringIO("look east\nexit\n"),
        output_stream=output,
    )

    assert code == 0
    rendered = output.getvalue()
    assert (
        "You cannot make out a distinct place in that direction from here."
        in rendered
    )
    assert "Orchard Path" not in rendered
    assert app.current_place_id() == YARD_ID
    assert app.authoritative_digest() == before


def test_vsm5_repeated_directional_observation_is_deterministic():
    app = _yard_app()
    before = app.authoritative_digest()

    first = app.look_direction("south")
    second = app.look_direction("south")
    east_first = app.look_direction("east")
    east_second = app.look_direction("east")

    assert first == second
    assert east_first == east_second
    assert app.authoritative_digest() == before


def test_vsm5_save_restore_does_not_change_directional_observation(tmp_path):
    checkpoint = tmp_path / "vsm5.json"
    app = _yard_app(checkpoint_path=checkpoint)

    south_before = app.look_direction("south")
    east_before = app.look_direction("east")
    digest_before = app.authoritative_digest()
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)

    assert restored.authoritative_digest() == digest_before
    assert restored.current_place_id() == YARD_ID
    assert restored.look_direction("south") == south_before
    assert restored.look_direction("east") == east_before
    assert restored.authoritative_digest() == digest_before


def test_vsm5_bare_look_and_inspect_behavior_remain_available():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    look = app.look()
    inspect = app.inspect("lantern")

    assert look.result_type == "look"
    assert inspect.result_type == "inspection"
    assert app.authoritative_digest() == before
