from __future__ import annotations

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import LANTERN_ID, ORCHARD_PATH_ID, YARD_ID
from astra_runtime.myravant_vsm10_terminal import execute_vsm10_terminal_input


def _execute(app: MyravantPlayApplication, command: str):
    return execute_vsm10_terminal_input(app, command)


def test_orchard_path_lit_throw_exposes_only_derived_directional_signal(tmp_path):
    checkpoint = tmp_path / "orchard-path-repair.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    assert _execute(app, "pickup lantern").result.authoritative_changed
    assert _execute(app, "light lantern").result.authoritative_changed
    assert _execute(app, "move south").result.authoritative_changed
    assert app.current_place_id() == YARD_ID

    before = _execute(app, "look east")
    assert before.route == "existing_terminal"
    assert before.result.result_type == "directional_observation_unavailable"
    assert before.result.failure_class == "directional_observation_unlicensed"

    thrown = _execute(app, "throw lantern east")
    assert thrown.route == "existing_terminal"
    assert thrown.result.result_type == "object_displacement_committed"
    assert thrown.result.authoritative_changed is True
    authoritative_after_throw = app.authoritative_digest()

    observed = _execute(app, "look east")
    assert observed.route == "orchard_path_directional_light_signal"
    assert observed.result.result_type == "directional_signal_observation"
    assert observed.result.authoritative_changed is False
    assert observed.result.observation_evidence_id is not None
    assert "Brass Lantern glow" in observed.result.message
    assert "east" in observed.result.message
    assert "Orchard Path" in observed.result.message
    assert observed.result.pre_state_digest == authoritative_after_throw
    assert observed.result.post_state_digest == authoritative_after_throw
    assert app.authoritative_digest() == authoritative_after_throw

    saved = _execute(app, "save")
    assert saved.result.result_type == "checkpoint_written"
    assert app.authoritative_digest() == authoritative_after_throw

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == authoritative_after_throw
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
    assert restored.entity_place_id(LANTERN_ID) == ORCHARD_PATH_ID

    replayed_observation = _execute(restored, "look east")
    assert replayed_observation.route == "orchard_path_directional_light_signal"
    assert (
        replayed_observation.result.observation_evidence_id
        == observed.result.observation_evidence_id
    )
    assert replayed_observation.result.authoritative_changed is False
    assert restored.authoritative_digest() == authoritative_after_throw


def test_orchard_path_signal_requires_current_lit_state_and_destination_placement():
    unlit = MyravantPlayApplication.new()
    assert _execute(unlit, "pickup lantern").result.authoritative_changed
    assert _execute(unlit, "move south").result.authoritative_changed
    assert _execute(unlit, "throw lantern east").result.authoritative_changed

    no_light = _execute(unlit, "look east")
    assert no_light.route == "existing_terminal"
    assert no_light.result.result_type == "directional_observation_unavailable"
    assert no_light.result.failure_class == "directional_observation_unlicensed"

    app = MyravantPlayApplication.new()
    assert _execute(app, "pickup lantern").result.authoritative_changed
    assert _execute(app, "light lantern").result.authoritative_changed
    assert _execute(app, "move south").result.authoritative_changed
    assert _execute(app, "throw lantern east").result.authoritative_changed
    assert _execute(app, "look east").route == "orchard_path_directional_light_signal"

    assert _execute(app, "move east").result.authoritative_changed
    assert app.current_place_id() == ORCHARD_PATH_ID
    assert _execute(app, "extinguish lantern").result.authoritative_changed
    assert _execute(app, "move west").result.authoritative_changed

    extinguished = _execute(app, "look east")
    assert extinguished.route == "existing_terminal"
    assert extinguished.result.result_type == "directional_observation_unavailable"
    assert extinguished.result.failure_class == "directional_observation_unlicensed"


def test_orchard_path_repair_does_not_create_generic_directional_visibility():
    app = MyravantPlayApplication.new()
    assert _execute(app, "pickup lantern").result.authoritative_changed
    assert _execute(app, "light lantern").result.authoritative_changed
    assert _execute(app, "move south").result.authoritative_changed
    assert _execute(app, "throw lantern east").result.authoritative_changed

    east = _execute(app, "look east")
    assert east.route == "orchard_path_directional_light_signal"

    north = _execute(app, "look north")
    assert north.route == "existing_terminal"
    assert north.result.result_type == "directional_observation_unavailable"
    assert north.result.failure_class == "directional_observation_unlicensed"

    south = _execute(app, "look south")
    assert south.route == "existing_terminal"
    assert south.result.result_type == "directional_observation"
    assert south.result.authoritative_changed is False
