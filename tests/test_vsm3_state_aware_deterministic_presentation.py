# VSM-3 state-aware deterministic presentation regressions.

from __future__ import annotations

from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    PublicLocationView,
)
from astra_runtime.myravant_terminal import _render_view


def _render(app: MyravantPlayApplication) -> str:
    result = app.look()
    assert result.view is not None
    return _render_view(result.view)


def test_vsm3_initial_object_state_is_visible_without_mutation():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    rendered = _render(app)

    assert "Objects: Brass Lantern [unlit]" in rendered
    assert app.authoritative_digest() == before


def test_vsm3_lit_state_changes_render_only_when_owned_state_changes():
    app = MyravantPlayApplication.new()

    before = _render(app)
    assert "Brass Lantern [unlit]" in before

    lit = app.light_object("lantern")
    assert lit.result_type == "object_lit_state_committed"
    after = _render(app)

    assert "Brass Lantern [lit]" in after
    assert "Brass Lantern [unlit]" not in after

    extinguished = app.extinguish_object("lantern")
    assert extinguished.result_type == "object_lit_state_committed"
    final = _render(app)

    assert "Brass Lantern [unlit]" in final
    assert "Brass Lantern [lit]" not in final


def test_vsm3_open_state_and_visible_contents_render_from_vsm2_facts():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.move("south").result_type == "movement_committed"

    closed = _render(app)
    assert "Tool Chest [closed]" in closed

    assert app.open_object("chest").result_type == "object_state_committed"
    opened = _render(app)
    assert "Tool Chest [open]" in opened
    assert "contains Brass Lantern" not in opened

    assert app.store_object("lantern", "chest").result_type == "storage_committed"
    contained = _render(app)
    assert "Tool Chest [open; contains Brass Lantern]" in contained


def test_vsm3_darkness_does_not_disclose_hidden_entity_or_hidden_marker():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.move("east").result_type == "movement_committed"

    dark = _render(app)

    assert "Weathered Waystone" not in dark
    assert "[hidden]" not in dark
    assert "insufficient" not in dark
    assert "observation" not in dark.casefold()

    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    lit = _render(app)

    assert "Weathered Waystone" in lit
    assert "Weathered Waystone [" not in lit


def test_vsm3_world2_current_state_is_visible_without_causal_history():
    app = MyravantPlayApplication.new()

    first = app.wait()
    second = app.wait()
    assert first.world_process_action == "move"
    assert second.world_process_action == "open_object"

    assert app.move("south").result_type == "movement_committed"
    before = app.authoritative_digest()
    rendered = _render(app)

    assert "Tool Chest [open]" in rendered
    assert "Actors: Groundskeeper" in rendered
    assert "Groundskeeper [" not in rendered
    assert "groundskeeper opened" not in rendered.casefold()
    assert "world_process" not in rendered
    assert "command_id" not in rendered
    assert "receipt" not in rendered.casefold()
    assert "routine" not in rendered.casefold()
    assert app.authoritative_digest() == before


def test_vsm3_repeated_identical_state_renders_byte_identically():
    app = MyravantPlayApplication.new()

    first = _render(app)
    second = _render(app)

    assert first == second


def test_vsm3_actor_presentation_remains_name_only_in_location_view():
    app = MyravantPlayApplication.new()
    assert app.move("south").result_type == "movement_committed"
    assert app.move("south").result_type == "movement_committed"

    rendered = _render(app)

    assert "Actors: Groundskeeper" in rendered
    assert "Groundskeeper [" not in rendered
    assert "quiet groundskeeper" not in rendered.casefold()


def test_vsm3_carrying_surface_remains_legacy_name_only():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.light_object("lantern").result_type == "object_lit_state_committed"

    rendered = _render(app)

    assert "Carrying: Brass Lantern" in rendered
    assert "Carrying: Brass Lantern [lit]" not in rendered


def test_vsm3_legacy_view_without_structured_facts_still_renders_names():
    view = PublicLocationView(
        place_id="legacy:place",
        name="Legacy Place",
        description="Legacy presentation.",
        exits=("north",),
        objects=("Legacy Object",),
        actors=("Legacy Actor",),
        carrying=("Legacy Carried Object",),
    )

    rendered = _render_view(view)

    assert "Objects: Legacy Object" in rendered
    assert "Actors: Legacy Actor" in rendered
    assert "Carrying: Legacy Carried Object" in rendered


def test_vsm3_renderer_never_changes_authoritative_digest():
    app = MyravantPlayApplication.new()
    assert app.move("south").result_type == "movement_committed"
    assert app.open_object("chest").result_type == "object_state_committed"
    before = app.authoritative_digest()

    for _ in range(5):
        rendered = _render(app)
        assert "Tool Chest [open]" in rendered
        assert app.authoritative_digest() == before
