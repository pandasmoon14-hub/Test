"""TERMINAL-PLAY-COMP-1 illumination-gated observation tests."""

from __future__ import annotations

from io import StringIO

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    AFQR17_FIXTURE_ENVIRONMENT_OWNER,
    AFQR20_FIXTURE_SENSING_OWNER,
    FIXTURE_AMBIENT_VISUAL_CONDITION_DIGEST,
    FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION,
    FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST,
    FIXTURE_PLAYABLE_NEED_REFS,
    FIXTURE_VERSION,
    ORCHARD_PATH_ID,
    WAYSTONE_ID,
    create_terminal_play_fixture,
    digest_fixture_ambient_visual_conditions,
)
from astra_runtime.myravant_terminal import run_terminal


def _move_to_orchard_with_lantern(app: MyravantPlayApplication) -> None:
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.move("east").result_type == "movement_committed"


def _waystone_relation(app: MyravantPlayApplication):
    matches = [
        relation
        for relation in app.state.representation.relations
        if (
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == WAYSTONE_ID
        )
    ]
    assert len(matches) == 1
    return matches[0]


def test_comp1_fixture_environment_input_is_versioned_and_owner_routed():
    fixture = create_terminal_play_fixture()
    app = MyravantPlayApplication.new(fixture=fixture)

    assert FIXTURE_VERSION == "0.1.5"
    assert "TERMINAL-PLAY-COMP-1" in FIXTURE_PLAYABLE_NEED_REFS
    assert fixture.ambient_visual_profile_version == (
        FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION
    )
    assert fixture.provenance.ambient_visual_profile_version == (
        FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION
    )
    assert fixture.provenance.ambient_visual_condition_digest == (
        FIXTURE_AMBIENT_VISUAL_CONDITION_DIGEST
    )
    assert digest_fixture_ambient_visual_conditions(
        fixture.ambient_visual_conditions
    ) == FIXTURE_AMBIENT_VISUAL_CONDITION_DIGEST

    orchard = fixture.ambient_visual_condition_for(ORCHARD_PATH_ID)
    assert orchard.condition == "insufficient"
    assert orchard.semantic_owner == AFQR17_FIXTURE_ENVIRONMENT_OWNER

    for condition in fixture.ambient_visual_conditions:
        assert condition.semantic_owner == AFQR17_FIXTURE_ENVIRONMENT_OWNER

    assert app.authoritative_digest() == FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST


def test_comp1_lantern_state_changes_observation_without_changing_waystone_truth():
    app = MyravantPlayApplication.new()
    _move_to_orchard_with_lantern(app)

    relation_before = _waystone_relation(app)
    assert relation_before.object_entity_id == ORCHARD_PATH_ID

    dark_digest = app.authoritative_digest()
    dark_look = app.look()
    assert "Weathered Waystone" not in dark_look.view.objects
    assert app.authoritative_digest() == dark_digest

    dark_evidence = app.visual_observation_evidence(WAYSTONE_ID)
    assert dark_evidence == app.visual_observation_evidence(WAYSTONE_ID)
    assert dark_evidence.semantic_owner == AFQR20_FIXTURE_SENSING_OWNER
    assert dark_evidence.ambient_condition == "insufficient"
    assert dark_evidence.local_light_available is False
    assert dark_evidence.observable is False
    assert dark_evidence.basis == "insufficient_visual_signal"

    dark_inspect = app.inspect("waystone")
    assert dark_inspect.result_type == "inspection_unavailable"
    assert dark_inspect.message == "You cannot inspect that from the current state."
    assert dark_inspect.pre_state_digest == dark_inspect.post_state_digest
    assert dark_inspect.post_state_digest == dark_digest

    lit = app.light_object("lantern")
    assert lit.result_type == "object_lit_state_committed"
    lit_digest = app.authoritative_digest()

    lit_look = app.look()
    assert "Weathered Waystone" in lit_look.view.objects
    assert app.authoritative_digest() == lit_digest

    lit_evidence = app.visual_observation_evidence(WAYSTONE_ID)
    assert lit_evidence.semantic_owner == AFQR20_FIXTURE_SENSING_OWNER
    assert lit_evidence.local_light_available is True
    assert lit_evidence.observable is True
    assert lit_evidence.basis == "local_light_source"

    visible = app.inspect("waystone")
    assert visible.result_type == "inspection"
    assert visible.view.name == "Weathered Waystone"
    assert app.authoritative_digest() == lit_digest

    extinguished = app.extinguish_object("lantern")
    assert extinguished.result_type == "object_lit_state_committed"
    assert "Weathered Waystone" not in app.look().view.objects
    assert app.inspect("waystone").result_type == "inspection_unavailable"

    relation_after = _waystone_relation(app)
    assert relation_after == relation_before
    assert relation_after.object_entity_id == ORCHARD_PATH_ID


def test_comp1_remote_lit_lantern_does_not_illuminate_orchard():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    assert app.drop("lantern").result_type == "custody_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.move("east").result_type == "movement_committed"

    evidence = app.visual_observation_evidence(WAYSTONE_ID)
    assert evidence.local_light_available is False
    assert evidence.observable is False
    assert "Weathered Waystone" not in app.look().view.objects


def test_comp1_closed_container_blocks_and_open_container_exposes_local_light():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.open_object("chest").result_type == "object_state_committed"
    assert app.store_object("lantern", "chest").result_type == "storage_committed"
    assert app.close_object("chest").result_type == "object_state_committed"
    assert app.pickup("chest").result_type == "custody_committed"
    assert app.move("east").result_type == "movement_committed"

    hidden = app.visual_observation_evidence(WAYSTONE_ID)
    assert hidden.local_light_available is False
    assert hidden.observable is False
    assert "Weathered Waystone" not in app.look().view.objects

    opened = app.open_object("chest")
    assert opened.result_type == "object_state_committed"
    exposed = app.visual_observation_evidence(WAYSTONE_ID)
    assert exposed.local_light_available is True
    assert exposed.observable is True
    assert "Weathered Waystone" in app.look().view.objects

    closed = app.close_object("chest")
    assert closed.result_type == "object_state_committed"
    assert "Weathered Waystone" not in app.look().view.objects


def test_comp1_observation_recomputes_after_checkpoint_restore(tmp_path):
    checkpoint = tmp_path / "comp1.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    _move_to_orchard_with_lantern(app)
    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    before_save = app.authoritative_digest()
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == before_save
    assert restored.visual_observation_evidence(WAYSTONE_ID).observable is True
    assert "Weathered Waystone" in restored.look().view.objects

    assert restored.extinguish_object("lantern").result_type == (
        "object_lit_state_committed"
    )
    after_extinguish = restored.authoritative_digest()
    restored.save()

    restored_again = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored_again.authoritative_digest() == after_extinguish
    assert restored_again.visual_observation_evidence(WAYSTONE_ID).observable is False
    assert "Weathered Waystone" not in restored_again.look().view.objects


def test_comp1_darkness_does_not_collapse_availability_into_observation():
    app = MyravantPlayApplication.new()
    _move_to_orchard_with_lantern(app)

    assert app.inspect("lantern").result_type == "inspection_unavailable"
    lit = app.light_object("lantern")
    assert lit.result_type == "object_lit_state_committed"
    assert app.inspect("lantern").result_type == "inspection"


def test_comp1_terminal_exact_name_probes_do_not_reveal_unobserved_waystone():
    app = MyravantPlayApplication.new()
    output = StringIO()
    run_terminal(
        app,
        input_stream=StringIO(
            "pickup lantern\nmove south\nmove east\n"
            "inspect waystone\nexamine waystone\nlook at waystone\nexit\n"
        ),
        output_stream=output,
    )

    text = output.getvalue()
    assert text.count("You cannot inspect that from the current state.") == 3
    assert "Weathered Waystone" not in text
