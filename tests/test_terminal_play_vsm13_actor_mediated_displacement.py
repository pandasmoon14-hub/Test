from __future__ import annotations

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    ORCHARD_PATH_ID,
    PLAYER_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm13_actor_mediated_displacement import (
    execute_vsm13_request,
    parse_vsm13_request,
)


def _carrier(app: MyravantPlayApplication) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == LANTERN_ID
    ]
    assert len(matches) <= 1
    return matches[0] if matches else None


def _direct_place(app: MyravantPlayApplication) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == LANTERN_ID
    ]
    assert len(matches) <= 1
    return matches[0] if matches else None


def _groundskeeper_carried_lantern_app() -> MyravantPlayApplication:
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    world = app.wait()
    assert world.authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    handoff = app.give_object("lantern", "groundskeeper")
    assert handoff.authoritative_changed
    assert _carrier(app) == GROUNDSKEEPER_ID
    return app


def test_vsm13_parser_is_exact_and_does_not_claim_prior_requests():
    exact = parse_vsm13_request("ask groundskeeper to throw lantern east")
    assert exact.parsed
    assert exact.actor_reference == "groundskeeper"
    assert exact.object_reference == "lantern"
    assert exact.direction == "east"

    expanded = parse_vsm13_request(
        "I ask the groundskeeper to throw the brass lantern east"
    )
    assert expanded.parsed
    assert expanded.object_reference == "brass lantern"

    assert not parse_vsm13_request("ask groundskeeper to throw lantern west").parsed
    assert not parse_vsm13_request("ask groundskeeper to drop lantern").parsed
    assert not parse_vsm13_request("throw lantern east").parsed


def test_vsm13_absent_actor_refuses_before_comp3_legality():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    execution = execute_vsm13_request(
        app,
        "ask groundskeeper to throw lantern east",
    )

    assert execution.result.result_type == "actor_mediated_displacement_rejected"
    assert execution.result.authoritative_changed is False
    assert execution.result.failure_class == "vsm13_requested_actor_not_local"
    assert execution.request_receipt.acceptance == "refused"
    assert execution.request_receipt.legality_result == "not_evaluated"
    assert execution.request_receipt.command_id is None
    assert app.authoritative_digest() == before


def test_vsm13_local_acceptance_does_not_override_comp3_carrying_requirement():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.wait().authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert _carrier(app) == PLAYER_ID
    before = app.authoritative_digest()

    execution = execute_vsm13_request(
        app,
        "ask groundskeeper to throw lantern east",
    )

    assert execution.request_receipt.acceptance == "accepted"
    assert execution.request_receipt.legality_result == "rejected"
    assert execution.request_receipt.performing_actor_entity_id is None
    assert execution.result.failure_class == "vsm13_comp3_opportunity_unavailable"
    assert execution.result.authoritative_changed is False
    assert execution.result.command_id is not None
    assert execution.request_receipt.qualification_evidence_id is not None
    assert execution.request_receipt.spatial_evidence_id is not None
    assert execution.request_receipt.opportunity_evidence_id is not None
    assert _carrier(app) == PLAYER_ID
    assert app.authoritative_digest() == before


def test_vsm13_commits_existing_comp3_as_groundskeeper_action():
    app = _groundskeeper_carried_lantern_app()
    before = app.authoritative_digest()

    execution = execute_vsm13_request(
        app,
        "ask groundskeeper to throw the brass lantern east",
    )

    assert execution.result.result_type == "actor_mediated_displacement_committed"
    assert execution.result.authoritative_changed is True
    assert execution.request_receipt.acceptance == "accepted"
    assert execution.request_receipt.legality_result == "allowed"
    assert execution.request_receipt.authoritative_outcome == "committed"
    assert execution.request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert execution.request_receipt.target_entity_id == LANTERN_ID
    assert execution.request_receipt.source_place_id == YARD_ID
    assert execution.request_receipt.destination_place_id == ORCHARD_PATH_ID
    assert execution.result.pre_state_digest == before
    assert execution.result.post_state_digest == app.authoritative_digest()
    assert execution.result.post_state_digest != before
    assert _carrier(app) is None
    assert _direct_place(app) == ORCHARD_PATH_ID

    transition = app.runtime_state.committed_object_displacement_transitions[-1]
    assert transition.receipt.receipt_id == execution.result.receipt_id
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.object_entity_id == LANTERN_ID
    assert transition.receipt.source_place_id == YARD_ID
    assert transition.receipt.destination_place_id == ORCHARD_PATH_ID
    assert transition.receipt.method == "throw"


def test_vsm13_does_not_change_direct_player_comp3_attribution():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed

    result = app.throw_object("lantern", "east")
    assert result.authoritative_changed
    transition = app.runtime_state.committed_object_displacement_transitions[-1]
    assert transition.receipt.actor_entity_id == PLAYER_ID
    assert transition.receipt.destination_place_id == ORCHARD_PATH_ID


def test_vsm13_repeated_fresh_runs_are_deterministic():
    snapshots = []
    for _ in range(2):
        app = _groundskeeper_carried_lantern_app()
        execution = execute_vsm13_request(
            app,
            "ask groundskeeper to throw lantern east",
        )
        transition = app.runtime_state.committed_object_displacement_transitions[-1]
        snapshots.append(
            (
                execution.request_receipt,
                execution.result.command_fingerprint,
                execution.result.receipt_id,
                execution.result.state_delta_id,
                transition.receipt.to_dict(),
                app.authoritative_digest(),
            )
        )

    assert snapshots[0] == snapshots[1]
