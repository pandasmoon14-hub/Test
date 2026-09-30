# VSM-2 structured public observation fact regressions.

from __future__ import annotations

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    TOOL_CHEST_ID,
    WAYSTONE_ID,
)


def _fact_by_id(view, entity_id):
    matches = tuple(
        fact
        for fact in view.observation_facts
        if fact.entity_id == entity_id
    )
    assert len(matches) == 1
    return matches[0]


def test_vsm2_look_projects_existing_object_state_into_public_fact_without_mutation():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.look()

    assert result.authoritative_changed is False
    assert result.pre_state_digest == before == result.post_state_digest
    assert app.authoritative_digest() == before

    lantern = _fact_by_id(result.view, LANTERN_ID)
    assert lantern.entity_kind == "object"
    assert lantern.name == "Brass Lantern"
    assert "well-handled surface" in lantern.description
    assert lantern.open_state is None
    assert lantern.lit_state == "unlit"
    assert lantern.visible_contents == ()
    assert result.view.objects == ("Brass Lantern",)


def test_vsm2_look_and_inspect_share_the_same_public_fact_for_one_entity():
    app = MyravantPlayApplication.new()

    look = app.look()
    inspect = app.inspect("lantern")

    assert inspect.result_type == "inspection"
    assert inspect.view.observation_fact == _fact_by_id(
        look.view,
        LANTERN_ID,
    )
    assert "Its flame is out." in inspect.view.description


def test_vsm2_open_container_fact_exposes_only_existing_public_contents():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.open_object("chest").result_type == "object_state_committed"
    assert app.store_object("lantern", "chest").result_type == "storage_committed"
    before = app.authoritative_digest()

    look = app.look()
    chest = _fact_by_id(look.view, TOOL_CHEST_ID)

    assert chest.open_state == "open"
    assert chest.lit_state is None
    assert chest.visible_contents == ("Brass Lantern",)
    assert app.authoritative_digest() == before

    inspection = app.inspect("tool chest")
    assert inspection.view.observation_fact == chest
    assert "Its heavy lid is open." in inspection.view.description
    assert "Inside: Brass Lantern." in inspection.view.description


def test_vsm2_actor_fact_uses_existing_public_presentation_only():
    app = MyravantPlayApplication.new()
    assert app.move("south").result_type == "movement_committed"
    assert app.move("south").result_type == "movement_committed"
    before = app.authoritative_digest()

    look = app.look()
    actor = _fact_by_id(look.view, GROUNDSKEEPER_ID)

    assert actor.entity_kind == "actor"
    assert actor.name == "Groundskeeper"
    assert actor.description == (
        "A quiet groundskeeper tends the bounded test grounds."
    )
    assert actor.open_state is None
    assert actor.lit_state is None
    assert actor.visible_contents == ()
    assert not hasattr(actor, "knowledge")
    assert not hasattr(actor, "goals")
    assert not hasattr(actor, "relationships")
    assert not hasattr(actor, "routine_phase")
    assert app.authoritative_digest() == before

    inspection = app.inspect("groundskeeper")
    assert inspection.view.observation_fact == actor


def test_vsm2_darkness_excludes_unobservable_fact_and_light_reveals_same_truth():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.move("east").result_type == "movement_committed"

    dark_before = app.authoritative_digest()
    dark_look = app.look()
    assert all(
        fact.entity_id != WAYSTONE_ID
        for fact in dark_look.view.observation_facts
    )
    assert app.inspect("waystone").result_type == "inspection_unavailable"
    assert app.authoritative_digest() == dark_before

    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    lit_before = app.authoritative_digest()
    lit_look = app.look()
    waystone = _fact_by_id(lit_look.view, WAYSTONE_ID)

    assert waystone.entity_kind == "object"
    assert waystone.name == "Weathered Waystone"
    assert waystone.open_state is None
    assert waystone.lit_state is None
    assert not hasattr(waystone, "ambient_condition")
    assert not hasattr(waystone, "observation_basis")
    assert app.authoritative_digest() == lit_before


def test_vsm2_identical_state_produces_identical_public_observation_facts():
    left = MyravantPlayApplication.new()
    right = MyravantPlayApplication.new()

    assert left.look().view.observation_facts == (
        right.look().view.observation_facts
    )

    assert left.pickup("lantern").result_type == "custody_committed"
    assert right.pickup("lantern").result_type == "custody_committed"
    assert left.light_object("lantern").result_type == "object_lit_state_committed"
    assert right.light_object("lantern").result_type == "object_lit_state_committed"
    assert left.move("south").result_type == "movement_committed"
    assert right.move("south").result_type == "movement_committed"

    assert left.authoritative_digest() == right.authoritative_digest()
    assert left.look().view.observation_facts == (
        right.look().view.observation_facts
    )


def test_vsm2_autonomous_existing_state_is_reflected_without_world_process_metadata():
    app = MyravantPlayApplication.new()
    first = app.wait()
    second = app.wait()
    assert first.world_process_action == "move"
    assert second.world_process_action == "open_object"

    assert app.move("south").result_type == "movement_committed"
    before = app.authoritative_digest()
    look = app.look()

    chest = _fact_by_id(look.view, TOOL_CHEST_ID)
    groundskeeper = _fact_by_id(look.view, GROUNDSKEEPER_ID)

    assert chest.open_state == "open"
    assert groundskeeper.entity_kind == "actor"
    for fact in (chest, groundskeeper):
        assert not hasattr(fact, "world_process_action")
        assert not hasattr(fact, "world_process_outcome")
        assert not hasattr(fact, "world_process_command_id")
    assert app.authoritative_digest() == before


def test_vsm2_location_compatibility_fields_remain_derived_from_structured_facts():
    app = MyravantPlayApplication.new()

    view = app.look().view

    assert view.objects == tuple(
        fact.name
        for fact in view.observation_facts
        if fact.entity_kind == "object"
    )
    assert view.actors == tuple(
        fact.name
        for fact in view.observation_facts
        if fact.entity_kind == "actor"
    )
