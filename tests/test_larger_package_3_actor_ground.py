"""Larger package 3 — actor-local physical assistance + owner replay.

The fixture-limited Groundskeeper is a performing actor, not an extension
of the player's custody or movement authority. No native content is defined.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    PersistentWorldObjectDisplacementReplayError,
    replay_persistent_world_object_displacement,
)
from astra_runtime.myravant_actor_ground_assistance import (
    execute_ground_contact_request,
    parse_ground_contact_request,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    TOOL_CHEST_ID,
    WORKSHOP_ID,
    YARD_ID,
    ORCHARD_PATH_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_terminal import execute_vsm14_terminal_input
from astra_runtime.myravant_terminal_capabilities import execute_bounded_terminal_request


@pytest.mark.parametrize(
    ("words", "is_parsed", "method", "target"),
    (
        ("ask groundskeeper to slide lantern south", True, "slide", "lantern"),
        ("I ask the groundskeeper to push the tool chest north", True, "push", "tool chest"),
        ("ask groundskeeper to push chest east", True, "push", "chest"),
        ("ask groundskeeper to push lantern east", True, "push", "lantern"),
        ("ask groundskeeper to throw lantern east", False, None, None),
        ("ask groundskeeper to follow me", False, None, None),
        ("ask town council for charter", False, None, None),
        ("ask groundskeeper to push chest upwards", False, None, None),
        ("ask groundskeeper to slide the hill south", False, None, "hill"),
        ("push chest north", False, None, None),
        ("ask groundskeeper to push it east", False, None, "it"),
    ),
)
def test_actor_physical_request_parser_preserves_other_owners(
    words, is_parsed, method, target
):
    result = parse_ground_contact_request(words)
    assert result.parsed is is_parsed
    assert result.method == method
    assert result.object_reference == target
    assert result.raw_text == words


@pytest.mark.parametrize(
    "raw_attempt",
    (
        "ask groundskeeper to slide the hill south",
        "ask groundskeeper to push it east",
    ),
)
def test_unqualified_referent_preserved_without_hijacking_owner(raw_attempt):
    # A rejected parse preserves the player's referent for capability
    # pressure, but cannot take ownership of the command or mutate state.
    app = MyravantVSM14Application.new()
    before = app.authoritative_digest()
    parsed = parse_ground_contact_request(raw_attempt)
    assert parsed.parsed is False
    assert parsed.object_reference in {"hill", "it"}
    assert execute_bounded_terminal_request(app, raw_attempt) is None
    assert app.authoritative_digest() == before
    assert not app.runtime_state.committed_object_displacement_transitions


def _meet(app):
    assert app.move("south").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == app.current_place_id()


def _with_follower_in_yard():
    app = MyravantVSM14Application.new()
    _meet(app)
    follow = execute_vsm14_terminal_input(
        app, "ask groundskeeper to follow me"
    )
    assert follow.result.authoritative_changed
    returned = app.move("north")
    assert returned.world_process_outcome == "committed"
    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    return app


def _read_only(app, outcome):
    assert outcome.authoritative_changed is False
    assert outcome.pre_state_digest == outcome.post_state_digest
    assert outcome.pre_state_digest == app.authoritative_digest()


def test_actor_not_present_rejects_without_affecting_world_or_follow():
    app = MyravantVSM14Application.new()
    before = app.authoritative_digest()
    result = execute_ground_contact_request(
        app, "ask groundskeeper to slide lantern south"
    )
    assert result.result.failure_class == "ground_request_actor_not_local"
    assert result.request_receipt.acceptance == "refused"
    assert result.request_receipt.authoritative_outcome == "no_commit"
    _read_only(app, result.result)
    assert app.authoritative_digest() == before


def test_ground_method_accepted_but_wrong_route_cannot_override_legality():
    app = _with_follower_in_yard()
    before = app.authoritative_digest()
    bad = execute_ground_contact_request(
        app, "ask groundskeeper to slide chest north"
    )
    assert bad.result.failure_class == "ground_request_route_unavailable"
    assert bad.request_receipt.acceptance == "accepted"
    assert bad.request_receipt.legality_result == "rejected"
    assert bad.request_receipt.performing_actor_entity_id is None
    _read_only(app, bad.result)
    assert app.authoritative_digest() == before
    permitted = execute_ground_contact_request(
        app, "ask groundskeeper to push chest north"
    )
    assert permitted.result.result_type == "actor_mediated_ground_displacement_committed"
    assert permitted.result.authoritative_changed
    assert permitted.request_receipt.requested_method == "push"
    assert permitted.request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert permitted.request_receipt.requester_entity_id != GROUNDSKEEPER_ID
    assert permitted.request_receipt.authoritative_outcome == "committed"
    assert permitted.result.receipt_id and permitted.result.state_delta_id
    assert permitted.request_receipt.authoritative_receipt_id == permitted.result.receipt_id
    receipt = app.runtime_state.committed_object_displacement_transitions[-1].receipt
    assert receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.object_entity_id == TOOL_CHEST_ID
    assert receipt.method == "push"
    assert receipt.destination_place_id == WORKSHOP_ID
    assert app.focused_observation("chest").result_type == "focused_observation_unavailable"
    _read_only(app, app.focused_observation("chest"))


def test_grounded_actor_and_player_method_reuse_same_owner_with_distinct_attribution():
    app = _with_follower_in_yard()
    # On the ground in the Yard, the lantern is not initially present.
    before = app.authoritative_digest()
    rejection = execute_ground_contact_request(
        app, "ask groundskeeper to push lantern east"
    )
    assert rejection.result.failure_class == "ground_request_object_not_grounded"
    assert rejection.request_receipt.acceptance == "accepted"
    assert rejection.request_receipt.legality_result == "rejected"
    _read_only(app, rejection.result)
    assert app.authoritative_digest() == before

    # Bring the actor to the Workshop; slide requires a directly grounded
    # source, whereas throw requires custody and remains VSM-13-owned.
    assert app.move("north").world_process_outcome == "committed"
    first_source = app.state.representation
    slide = execute_ground_contact_request(
        app, "I ask the groundskeeper to slide the brass lantern south"
    )
    assert slide.result.authoritative_changed
    assert slide.result.message == "The Groundskeeper slides the Brass Lantern south."
    assert slide.request_receipt.requested_method == "slide"
    t1 = app.runtime_state.committed_object_displacement_transitions[-1]
    assert t1.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert t1.receipt.method == "slide"
    assert replay_persistent_world_object_displacement(
        pre_state_representation=first_source, receipt=t1.receipt
    ) == app.state.representation
    assert app.focused_observation("lantern").result_type == "focused_observation_unavailable"

    assert app.move("south").world_process_outcome == "committed"
    assert app.focused_observation("lantern").result_type == "focused_sighting"
    second_source = app.state.representation
    pushed = execute_ground_contact_request(
        app, "ask groundskeeper to push the lantern east"
    )
    assert pushed.result.authoritative_changed
    t2 = app.runtime_state.committed_object_displacement_transitions[-1]
    assert t2.receipt.method == "push"
    assert t2.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert t2.receipt.object_entity_id == LANTERN_ID
    assert t2.receipt.destination_place_id == ORCHARD_PATH_ID
    assert replay_persistent_world_object_displacement(
        pre_state_representation=second_source, receipt=t2.receipt
    ) == app.state.representation
    forged_actor = replace(t2.receipt, source_place_id=WORKSHOP_ID)
    with pytest.raises(PersistentWorldObjectDisplacementReplayError):
        replay_persistent_world_object_displacement(
            pre_state_representation=second_source, receipt=forged_actor
        )
    assert app.focused_observation("lantern").result_type == "focused_observation_unavailable"
    assert app.move("east").world_process_outcome == "committed"
    # The Orchard is dark, so grounded position alone is not visibility.
    not_visible = app.focused_observation("lantern")
    assert not_visible.failure_class == "focused_target_not_observed"
    _read_only(app, not_visible)


def test_held_object_cannot_be_pushed_even_if_method_and_route_exist():
    app = _with_follower_in_yard()
    assert app.move("north").world_process_outcome == "committed"
    assert app.pickup("lantern").authoritative_changed
    before = app.authoritative_digest()
    result = execute_ground_contact_request(
        app, "ask groundskeeper to slide lantern south"
    )
    assert result.request_receipt.acceptance == "accepted"
    assert result.result.failure_class == "ground_request_object_not_grounded"
    _read_only(app, result.result)
    assert app.authoritative_digest() == before


def test_checkpoint_preserves_ground_results_and_follow_continuity(tmp_path):
    cp = tmp_path / "ground-world.json"
    app = MyravantVSM14Application.new(checkpoint_path=cp)
    assert app.light_object("lantern").authoritative_changed
    _meet(app)
    assert execute_vsm14_terminal_input(
        app, "ask groundskeeper to follow me"
    ).result.authoritative_changed
    assert app.move("north").world_process_outcome == "committed"
    assert app.move("north").world_process_outcome == "committed"
    assert execute_ground_contact_request(
        app, "ask groundskeeper to slide lantern south"
    ).result.authoritative_changed
    assert app.move("south").world_process_outcome == "committed"
    assert execute_ground_contact_request(
        app, "ask groundskeeper to push lantern east"
    ).result.authoritative_changed
    assert app.move("east").world_process_outcome == "committed"
    assert app.focused_observation("waystone").result_type == "focused_sighting"
    before = app.authoritative_digest()
    snapshot = app.look()
    search = app.focused_observation("lantern")
    assert search.result_type == "focused_sighting"
    assert app.save().result_type == "checkpoint_written"
    restored = MyravantVSM14Application.restore(checkpoint_path=cp)
    assert restored.authoritative_digest() == before
    assert restored.look() == snapshot
    assert restored.focused_observation("lantern") == search
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == ORCHARD_PATH_ID
    assert restored.runtime_state.committed_object_displacement_transitions[-1].receipt.actor_entity_id == GROUNDSKEEPER_ID
