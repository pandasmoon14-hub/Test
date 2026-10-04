from __future__ import annotations

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    PLAYER_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm11_actor_mediated_custody import (
    execute_vsm11_request,
    parse_vsm11_request,
)


def _relation_target(app: MyravantPlayApplication, relation_type: str) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if relation.relation_type == relation_type
        and relation.subject_entity_id == LANTERN_ID
    ]
    assert len(matches) <= 1
    return matches[0] if matches else None


def test_vsm11_parser_is_bounded_to_groundskeeper_lantern_custody_requests():
    assert parse_vsm11_request("ask groundskeeper to pick up lantern").parsed
    assert parse_vsm11_request("ask the groundskeeper to pickup the brass lantern").parsed
    assert parse_vsm11_request("I ask groundskeeper to drop lantern").parsed

    assert not parse_vsm11_request("ask groundskeeper to light lantern").parsed
    assert not parse_vsm11_request("ask groundskeeper to pick up chest").parsed
    assert not parse_vsm11_request("ask traveler to pick up lantern").parsed
    assert not parse_vsm11_request("pickup lantern").parsed


def test_vsm11_refuses_request_when_actor_is_not_local_without_mutation():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    execution = execute_vsm11_request(
        app,
        "ask groundskeeper to pick up lantern",
    )

    assert execution.result.result_type == "actor_mediated_custody_rejected"
    assert execution.result.authoritative_changed is False
    assert execution.result.failure_class == "vsm11_requested_actor_not_local"
    assert execution.request_receipt.requester_entity_id == PLAYER_ID
    assert execution.request_receipt.requested_actor_entity_id == GROUNDSKEEPER_ID
    assert execution.request_receipt.performing_actor_entity_id is None
    assert execution.request_receipt.acceptance == "refused"
    assert execution.request_receipt.legality_result == "not_evaluated"
    assert execution.request_receipt.authoritative_outcome == "no_commit"
    assert app.authoritative_digest() == before


def test_vsm11_acceptance_does_not_override_r4e_custody_opportunity():
    app = MyravantPlayApplication.new()
    assert app.move("south").authoritative_changed is True
    assert app.wait().authoritative_changed is True
    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    before = app.authoritative_digest()

    execution = execute_vsm11_request(
        app,
        "ask groundskeeper to pick up lantern",
    )

    assert execution.request_receipt.acceptance == "accepted"
    assert execution.request_receipt.legality_result == "rejected"
    assert execution.request_receipt.authoritative_outcome == "no_commit"
    assert execution.request_receipt.qualification_evidence_id is not None
    assert execution.request_receipt.opportunity_evidence_id is not None
    assert execution.result.failure_class == "vsm11_r4e_opportunity_unavailable"
    assert execution.result.authoritative_changed is False
    assert app.authoritative_digest() == before
    assert _relation_target(app, LOCATED_AT_RELATION_TYPE) is not None
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) is None


def test_vsm11_pickup_and_drop_commit_as_groundskeeper_actions():
    app = MyravantPlayApplication.new()

    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.drop("lantern").authoritative_changed is True
    assert app.wait().authoritative_changed is True
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID

    pickup = execute_vsm11_request(
        app,
        "ask groundskeeper to pick up lantern",
    )
    assert pickup.result.result_type == "actor_mediated_custody_committed"
    assert pickup.result.authoritative_changed is True
    assert pickup.request_receipt.requester_entity_id == PLAYER_ID
    assert pickup.request_receipt.requested_actor_entity_id == GROUNDSKEEPER_ID
    assert pickup.request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert pickup.request_receipt.target_entity_id == LANTERN_ID
    assert pickup.request_receipt.requested_operation == "pickup"
    assert pickup.request_receipt.acceptance == "accepted"
    assert pickup.request_receipt.legality_result == "allowed"
    assert pickup.request_receipt.authoritative_outcome == "committed"
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) == GROUNDSKEEPER_ID
    assert _relation_target(app, LOCATED_AT_RELATION_TYPE) is None
    assert app.custody_state.committed_custody_transitions[-1].receipt.actor_entity_id == GROUNDSKEEPER_ID

    before_repeat = app.authoritative_digest()
    repeat = execute_vsm11_request(
        app,
        "ask groundskeeper to pick up lantern",
    )
    assert repeat.request_receipt.acceptance == "accepted"
    assert repeat.request_receipt.legality_result == "rejected"
    assert repeat.result.authoritative_changed is False
    assert app.authoritative_digest() == before_repeat

    drop = execute_vsm11_request(
        app,
        "ask groundskeeper to drop lantern",
    )
    assert drop.result.result_type == "actor_mediated_custody_committed"
    assert drop.request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert drop.request_receipt.requested_operation == "drop"
    assert drop.request_receipt.legality_result == "allowed"
    assert _relation_target(app, LOCATED_AT_RELATION_TYPE) == YARD_ID
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) is None
    assert app.custody_state.committed_custody_transitions[-1].receipt.actor_entity_id == GROUNDSKEEPER_ID


def test_vsm11_direct_player_custody_remains_player_attributed():
    app = MyravantPlayApplication.new()
    result = app.pickup("lantern")
    assert result.authoritative_changed is True
    assert app.custody_state.committed_custody_transitions[-1].receipt.actor_entity_id == PLAYER_ID
