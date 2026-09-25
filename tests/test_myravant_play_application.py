"""Focused tests for the bounded Myravant terminal application adapter."""

from __future__ import annotations

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    write_persistent_world_checkpoint,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID,
    TOOL_CHEST_ID,
    WORKSHOP_ID,
    YARD_ID,
    create_terminal_play_fixture,
)


def test_look_reads_authoritative_location_without_mutation():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.look()

    assert result.result_type == "look"
    assert result.view is not None
    assert result.view.place_id == WORKSHOP_ID
    assert "Brass Lantern" in result.view.objects
    assert app.authoritative_digest() == before


def test_move_routes_through_r4_c_and_exposes_existing_evidence():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.move("south")

    assert result.result_type == "movement_committed"
    assert result.authoritative_changed is True
    assert result.command_id == "terminal-move-000001"
    assert result.command_fingerprint is not None
    assert result.preview_id is not None
    assert result.receipt_id is not None
    assert result.state_delta_id is not None
    assert result.spatial_evidence_id is not None
    assert result.opportunity_evidence_id is not None
    assert result.technical_retry is False
    assert result.pre_state_digest == before
    assert result.post_state_digest == app.authoritative_digest()
    assert result.post_state_digest != before
    assert app.current_place_id() == YARD_ID

    transition = app.state.committed_transitions[-1]
    assert result.command_fingerprint == transition.command_fingerprint
    assert result.preview_id == transition.preview.preview_id
    assert result.receipt_id == transition.receipt.receipt_id
    assert result.state_delta_id == transition.state_delta.delta_id
    assert (
        result.spatial_evidence_id
        == transition.receipt.spatial_evidence_id
    )
    assert (
        result.opportunity_evidence_id
        == transition.receipt.opportunity_evidence_id
    )


def test_undeclared_route_fails_without_authoritative_change():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.move("east")

    assert result.result_type == "movement_rejected"
    assert result.failure_class == "unavailable_fixture_route"
    assert result.authoritative_changed is False
    assert result.pre_state_digest == before
    assert result.post_state_digest == before
    assert result.command_id is None
    assert result.receipt_id is None
    assert app.authoritative_digest() == before
    assert app.current_place_id() == WORKSHOP_ID


def test_save_restore_and_new_play_cross_process_shape(tmp_path):
    checkpoint = tmp_path / "myravant-g1.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    first = app.move("south")
    saved = app.save()

    assert checkpoint.exists()
    assert saved.checkpoint_digest is not None

    del app

    restored = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert restored.current_place_id() == YARD_ID

    second = restored.move("north")
    assert second.command_id == "terminal-move-000002"
    assert second.command_id != first.command_id
    assert restored.current_place_id() == WORKSHOP_ID

    restored.save()
    del restored

    restored_again = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert restored_again.current_place_id() == WORKSHOP_ID
    assert len(restored_again.state.committed_transitions) == 2


def test_pickup_routes_through_r4_e_and_look_reports_carried_object():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.pickup("lantern")

    assert result.result_type == "custody_committed"
    assert result.authoritative_changed is True
    assert result.command_id == "terminal-custody-000001"
    assert result.receipt_id is not None
    assert result.state_delta_id is not None
    assert result.opportunity_evidence_id is not None
    assert result.pre_state_digest == before
    assert result.post_state_digest == app.authoritative_digest()
    assert result.post_state_digest != before

    relations = app.state.representation.relations
    carried = [
        relation
        for relation in relations
        if (
            relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == LANTERN_ID
        )
    ]
    direct = [
        relation
        for relation in relations
        if (
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == LANTERN_ID
        )
    ]

    assert len(carried) == 1
    assert carried[0].object_entity_id == app.fixture.player_entity_id
    assert direct == []

    view = app.look().view
    assert view is not None
    assert "Brass Lantern" in view.carrying
    assert "Brass Lantern" not in view.objects


def test_movement_preserves_r4_e_custody_relation():
    app = MyravantPlayApplication.new()

    app.pickup("brass lantern")
    movement = app.move("south")

    assert movement.result_type == "movement_committed"
    assert app.current_place_id() == YARD_ID

    carried = [
        relation
        for relation in app.state.representation.relations
        if (
            relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == LANTERN_ID
        )
    ]
    assert len(carried) == 1
    assert carried[0].object_entity_id == app.fixture.player_entity_id


def test_remote_pickup_is_rejected_before_command_without_state_change():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.pickup("tool chest")

    assert result.result_type == "custody_rejected"
    assert result.failure_class == "pickup_placement_unavailable"
    assert result.command_id is None
    assert result.authoritative_changed is False
    assert result.pre_state_digest == before
    assert result.post_state_digest == before
    assert app.authoritative_digest() == before


def test_r4e_pickup_move_save_restore_drop_save_restore_sequence(tmp_path):
    checkpoint = tmp_path / "myravant-g2.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    pickup = app.pickup("lantern")
    movement = app.move("south")
    first_save = app.save()

    assert pickup.command_id == "terminal-custody-000001"
    assert movement.command_id == "terminal-move-000001"
    assert first_save.checkpoint_digest is not None

    del app

    restored = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert restored.current_place_id() == YARD_ID
    assert restored.look().view is not None
    assert "Brass Lantern" in restored.look().view.carrying

    dropped = restored.drop("brass lantern")
    second_save = restored.save()

    assert dropped.result_type == "custody_committed"
    assert dropped.command_id == "terminal-custody-000002"
    assert second_save.checkpoint_digest is not None

    del restored

    final = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert final.current_place_id() == YARD_ID
    assert len(final.state.committed_transitions) == 1
    assert len(final.custody_state.committed_custody_transitions) == 2

    lantern_direct = [
        relation
        for relation in final.state.representation.relations
        if (
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == LANTERN_ID
        )
    ]
    lantern_carried = [
        relation
        for relation in final.state.representation.relations
        if (
            relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == LANTERN_ID
        )
    ]
    assert len(lantern_direct) == 1
    assert lantern_direct[0].object_entity_id == YARD_ID
    assert lantern_carried == []


def test_existing_g1_r4d_checkpoint_remains_loadable_and_can_upgrade_on_save(
    tmp_path,
):
    fixture = create_terminal_play_fixture()
    checkpoint = tmp_path / "g1-r4d.json"

    write_persistent_world_checkpoint(
        state=fixture.initial_state,
        checkpoint_path=checkpoint,
        qualification_evidence=fixture.checkpoint_qualification,
    )

    restored = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint,
        fixture=fixture,
    )

    assert restored.current_place_id() == WORKSHOP_ID
    assert restored.custody_state.committed_custody_transitions == ()

    restored.checkpoint_path = checkpoint
    restored.save()

    upgraded = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint,
        fixture=fixture,
    )
    assert upgraded.current_place_id() == WORKSHOP_ID
    assert upgraded.custody_state.committed_custody_transitions == ()

def test_obs1_targeted_inspection_reads_public_presentation_without_mutation():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.inspect("lantern")

    assert result.result_type == "inspection"
    assert result.authoritative_changed is False
    assert result.view is not None
    assert result.view.name == "Brass Lantern"
    assert "workbench" not in result.view.description.casefold()
    assert result.pre_state_digest == before
    assert result.post_state_digest == before
    assert result.command_id is None
    assert result.command_fingerprint is None
    assert result.preview_id is None
    assert result.receipt_id is None
    assert result.state_delta_id is None
    assert app.authoritative_digest() == before


def test_obs1_carried_and_moved_object_remains_inspectable_without_new_transition():
    app = MyravantPlayApplication.new()
    app.pickup("lantern")
    app.move("south")
    before = app.authoritative_digest()
    movement_count = len(app.state.committed_transitions)
    custody_count = len(app.custody_state.committed_custody_transitions)

    result = app.inspect("brass lantern")

    assert result.result_type == "inspection"
    assert result.view is not None
    assert result.view.name == "Brass Lantern"
    assert "workbench" not in result.view.description.casefold()
    assert result.pre_state_digest == before == result.post_state_digest
    assert app.authoritative_digest() == before
    assert len(app.state.committed_transitions) == movement_count
    assert len(app.custody_state.committed_custody_transitions) == custody_count


def test_obs1_remote_and_unknown_targets_are_player_indistinguishable():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    remote = app.inspect("tool chest")
    unknown = app.inspect("sword")

    assert remote.result_type == unknown.result_type == "inspection_unavailable"
    assert remote.failure_class == unknown.failure_class == "inspection_target_unavailable"
    assert remote.message == unknown.message == "You cannot inspect that from the current state."
    assert remote.pre_state_digest == remote.post_state_digest == before
    assert unknown.pre_state_digest == unknown.post_state_digest == before
    assert remote.command_id is unknown.command_id is None
    assert remote.receipt_id is unknown.receipt_id is None
    assert remote.state_delta_id is unknown.state_delta_id is None
    assert app.authoritative_digest() == before


def test_obs1_local_targets_become_inspectable_from_current_authoritative_location():
    app = MyravantPlayApplication.new()

    app.move("south")
    chest = app.inspect("tool chest")
    assert chest.result_type == "inspection"
    assert chest.view is not None
    assert chest.view.name == "Tool Chest"
    assert "yard wall" not in chest.view.description.casefold()

    app.move("east")
    waystone = app.inspect("weathered waystone")
    assert waystone.result_type == "inspection"
    assert waystone.view is not None
    assert waystone.view.name == "Weathered Waystone"
    assert "orchard path" not in waystone.view.description.casefold()
