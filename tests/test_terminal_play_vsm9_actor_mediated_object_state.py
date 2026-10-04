from __future__ import annotations

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    PLAYER_ID,
    TOOL_CHEST_ID,
)
from astra_runtime.myravant_vsm9_actor_mediated_object_state import (
    execute_vsm9_request,
    parse_vsm9_request,
    vsm9_legality_snapshot,
)


def _setup_colocated_yard(app: MyravantPlayApplication) -> None:
    moved = app.move("south")
    assert moved.authoritative_changed is True
    advanced = app.wait()
    assert advanced.authoritative_changed is True
    assert app.current_place_id() == app.entity_place_id(GROUNDSKEEPER_ID)


def _bring_player_carried_lantern_to_yard(app: MyravantPlayApplication) -> None:
    assert app.pickup("lantern").authoritative_changed is True
    _setup_colocated_yard(app)


def test_vsm9_parser_is_intentionally_bounded_to_groundskeeper_lantern_state_requests():
    accepted = {
        "ask groundskeeper to light lantern": ("groundskeeper", "light", "lantern"),
        "ask the groundskeeper to light the brass lantern": (
            "groundskeeper",
            "light",
            "brass lantern",
        ),
        "ask groundskeeper to ignite lantern": (
            "groundskeeper",
            "light",
            "lantern",
        ),
        "ask groundskeeper to extinguish lantern": (
            "groundskeeper",
            "extinguish",
            "lantern",
        ),
    }
    for raw, expected in accepted.items():
        parsed = parse_vsm9_request(raw)
        assert parsed.parsed is True, raw
        assert (
            parsed.actor_reference,
            parsed.operation,
            parsed.object_reference,
        ) == expected

    for raw in (
        "ask groundskeeper to open chest",
        "ask blacksmith to light lantern",
        "ask groundskeeper to light chest",
        "groundskeeper light lantern",
        "ask groundskeeper to activate lantern",
        "ask him to light it",
    ):
        parsed = parse_vsm9_request(raw)
        assert parsed.parsed is False, raw


def test_vsm9_request_is_nonmutating_until_fixture_acceptance_and_int2_commit():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    absent_actor = execute_vsm9_request(
        app,
        "ask groundskeeper to light lantern",
    )
    assert absent_actor.result.authoritative_changed is False
    assert absent_actor.request_receipt.acceptance == "refused"
    assert absent_actor.request_receipt.performing_actor_entity_id is None
    assert app.authoritative_digest() == before
    assert app.object_lit_state(LANTERN_ID).state == "unlit"

    outside = execute_vsm9_request(app, "ask groundskeeper to light chest")
    assert outside.result.authoritative_changed is False
    assert outside.request_receipt.acceptance == "not_accepted"
    assert outside.request_receipt.legality_result == "not_evaluated"
    assert app.authoritative_digest() == before


def test_vsm9_player_carried_lantern_is_meaningful_bounded_legality_rejection():
    app = MyravantPlayApplication.new()
    _bring_player_carried_lantern_to_yard(app)
    snapshot = vsm9_legality_snapshot(app)
    assert snapshot["actor_local_to_requester"] is True
    assert snapshot["actor_can_reach_target"] is False

    before = app.authoritative_digest()
    rejected = execute_vsm9_request(
        app,
        "ask groundskeeper to light the brass lantern",
    )
    assert rejected.request_receipt.acceptance == "accepted"
    assert rejected.request_receipt.legality_result == "rejected"
    assert rejected.request_receipt.performing_actor_entity_id is None
    assert rejected.result.failure_class == "vsm9_int2_opportunity_unavailable"
    assert rejected.result.authoritative_changed is False
    assert app.authoritative_digest() == before
    assert app.object_lit_state(LANTERN_ID).state == "unlit"


def test_vsm9_nearby_lantern_commits_with_groundskeeper_as_performer_and_full_provenance():
    app = MyravantPlayApplication.new()
    _bring_player_carried_lantern_to_yard(app)
    assert app.drop("lantern").authoritative_changed is True

    before = app.authoritative_digest()
    executed = execute_vsm9_request(
        app,
        "ask the groundskeeper to light the lantern",
    )
    result = executed.result
    receipt = executed.request_receipt

    assert result.authoritative_changed is True
    assert result.result_type == "actor_mediated_object_lit_state_committed"
    assert result.message == "The Groundskeeper lights the Brass Lantern."
    assert app.object_lit_state(LANTERN_ID).state == "lit"
    assert app.authoritative_digest() != before

    assert receipt.requester_entity_id == PLAYER_ID
    assert receipt.requested_actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.target_entity_id == LANTERN_ID
    assert receipt.requested_operation == "light"
    assert receipt.acceptance == "accepted"
    assert receipt.legality_result == "allowed"
    assert receipt.authoritative_outcome == "committed"
    assert receipt.command_id == result.command_id
    assert receipt.command_fingerprint == result.command_fingerprint
    assert receipt.authoritative_receipt_id == result.receipt_id
    assert receipt.state_delta_id == result.state_delta_id
    assert receipt.qualification_evidence_id is not None
    assert receipt.opportunity_evidence_id == result.opportunity_evidence_id

    transition = app.lit_state.committed_object_lit_transitions[-1]
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.object_entity_id == LANTERN_ID
    assert transition.receipt.operation == "light"


def test_vsm9_groundskeeper_carried_lantern_is_legal_and_player_behavior_is_unchanged():
    app = MyravantPlayApplication.new()
    _bring_player_carried_lantern_to_yard(app)
    given = app.give_object("lantern", "groundskeeper")
    assert given.authoritative_changed is True
    assert vsm9_legality_snapshot(app)["actor_can_reach_target"] is True

    lit = execute_vsm9_request(app, "ask groundskeeper to light lantern")
    assert lit.result.authoritative_changed is True
    assert lit.request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    returned = app.request_object_from_actor("groundskeeper", "lantern")
    assert returned.authoritative_changed is True
    direct = app.extinguish_object("lantern")
    assert direct.authoritative_changed is True
    assert direct.message == "You extinguish the Brass Lantern."
    transition = app.lit_state.committed_object_lit_transitions[-1]
    assert transition.receipt.actor_entity_id == PLAYER_ID


def test_vsm9_open_container_is_legal_closed_container_is_atomic_rejection():
    app = MyravantPlayApplication.new()
    _bring_player_carried_lantern_to_yard(app)

    opened = app.open_object("chest")
    assert opened.authoritative_changed is True
    stored = app.store_object("lantern", "chest")
    assert stored.authoritative_changed is True
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"
    assert vsm9_legality_snapshot(app)["actor_can_reach_target"] is True

    lit = execute_vsm9_request(app, "ask groundskeeper to light lantern")
    assert lit.result.authoritative_changed is True
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    closed = app.close_object("chest")
    assert closed.authoritative_changed is True
    before = app.authoritative_digest()
    count_before = len(app.lit_state.committed_object_lit_transitions)
    rejected = execute_vsm9_request(
        app,
        "ask groundskeeper to extinguish lantern",
    )
    assert rejected.request_receipt.acceptance == "accepted"
    assert rejected.request_receipt.legality_result == "rejected"
    assert rejected.result.authoritative_changed is False
    assert app.authoritative_digest() == before
    assert len(app.lit_state.committed_object_lit_transitions) == count_before
    assert app.object_lit_state(LANTERN_ID).state == "lit"


def test_vsm9_redundant_state_is_nonmutating_and_does_not_fabricate_commit_receipt():
    app = MyravantPlayApplication.new()
    _bring_player_carried_lantern_to_yard(app)
    assert app.drop("lantern").authoritative_changed is True
    first = execute_vsm9_request(app, "ask groundskeeper to light lantern")
    assert first.result.authoritative_changed is True

    before = app.authoritative_digest()
    count_before = len(app.lit_state.committed_object_lit_transitions)
    repeated = execute_vsm9_request(app, "ask groundskeeper to light lantern")
    assert repeated.result.result_type == "actor_mediated_object_lit_state_unchanged"
    assert repeated.result.authoritative_changed is False
    assert repeated.request_receipt.acceptance == "accepted"
    assert repeated.request_receipt.legality_result == "allowed_no_change"
    assert repeated.request_receipt.authoritative_outcome == "unchanged"
    assert repeated.request_receipt.authoritative_receipt_id is None
    assert app.authoritative_digest() == before
    assert len(app.lit_state.committed_object_lit_transitions) == count_before


def test_vsm9_save_restore_preserves_actor_attribution_and_exact_authoritative_state(tmp_path):
    path = tmp_path / "vsm9.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _bring_player_carried_lantern_to_yard(app)
    assert app.drop("lantern").authoritative_changed is True

    committed = execute_vsm9_request(app, "ask groundskeeper to light lantern")
    assert committed.result.authoritative_changed is True
    final_digest = app.authoritative_digest()
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == final_digest
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
    transition = restored.lit_state.committed_object_lit_transitions[-1]
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.operation == "light"
    assert transition.receipt.receipt_id == committed.result.receipt_id


def test_vsm9_fresh_runs_are_deterministic():
    evidence = []
    for _ in range(2):
        app = MyravantPlayApplication.new()
        _bring_player_carried_lantern_to_yard(app)
        assert app.drop("lantern").authoritative_changed is True
        executed = execute_vsm9_request(app, "ask groundskeeper to light lantern")
        transition = app.lit_state.committed_object_lit_transitions[-1]
        evidence.append(
            (
                executed.request_receipt,
                executed.result.command_id,
                executed.result.command_fingerprint,
                executed.result.receipt_id,
                executed.result.state_delta_id,
                executed.result.post_state_digest,
                transition.receipt.to_dict(),
            )
        )
    assert evidence[0] == evidence[1]


def test_vsm9_world2_interleaving_preserves_lit_state_and_owner_attribution():
    app = MyravantPlayApplication.new()
    _bring_player_carried_lantern_to_yard(app)
    assert app.drop("lantern").authoritative_changed is True
    lit = execute_vsm9_request(app, "ask groundskeeper to light lantern")
    assert lit.result.authoritative_changed is True
    count_before = len(app.lit_state.committed_object_lit_transitions)

    advanced = app.wait()
    assert advanced.authoritative_changed is True
    assert app.object_lit_state(LANTERN_ID).state == "lit"
    assert len(app.lit_state.committed_object_lit_transitions) == count_before
    assert app.lit_state.committed_object_lit_transitions[-1].receipt.actor_entity_id == GROUNDSKEEPER_ID


def test_vsm9_sustained_play_campaign_contains_success_and_meaningful_rejection(tmp_path):
    path = tmp_path / "vsm9-sustained.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    outcomes: list[tuple[str, str, bool]] = []

    # Request cannot reach an absent actor.
    absent = execute_vsm9_request(app, "ask groundskeeper to light lantern")
    outcomes.append((
        absent.request_receipt.acceptance,
        absent.request_receipt.legality_result,
        absent.result.authoritative_changed,
    ))

    # Bring the unlit lantern into the shared yard while it remains player-carried.
    assert app.pickup("lantern").authoritative_changed is True
    _setup_colocated_yard(app)
    carried_rejection = execute_vsm9_request(
        app, "ask groundskeeper to light lantern"
    )
    outcomes.append((
        carried_rejection.request_receipt.acceptance,
        carried_rejection.request_receipt.legality_result,
        carried_rejection.result.authoritative_changed,
    ))

    # Nearby object: accepted, legal, and committed by the requested actor.
    assert app.drop("lantern").authoritative_changed is True
    nearby_success = execute_vsm9_request(
        app, "ask groundskeeper to light lantern"
    )
    outcomes.append((
        nearby_success.request_receipt.acceptance,
        nearby_success.request_receipt.legality_result,
        nearby_success.result.authoritative_changed,
    ))

    # Repeated state request is accepted but produces no duplicate mutation.
    redundant = execute_vsm9_request(app, "ask groundskeeper to light lantern")
    outcomes.append((
        redundant.request_receipt.acceptance,
        redundant.request_receipt.legality_result,
        redundant.result.authoritative_changed,
    ))

    # Persist, restore, and continue the same world.
    app.save()
    app = MyravantPlayApplication.restore(checkpoint_path=path)
    app.checkpoint_path = path
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    # Player direct INT-2 remains lawful and remains player-attributed.
    assert app.pickup("lantern").authoritative_changed is True
    direct = app.extinguish_object("lantern")
    assert direct.authoritative_changed is True
    assert app.lit_state.committed_object_lit_transitions[-1].receipt.actor_entity_id == PLAYER_ID

    # Open container composition remains accessible to the Groundskeeper.
    assert app.open_object("chest").authoritative_changed is True
    assert app.store_object("lantern", "chest").authoritative_changed is True
    contained_success = execute_vsm9_request(
        app, "ask groundskeeper to light lantern"
    )
    outcomes.append((
        contained_success.request_receipt.acceptance,
        contained_success.request_receipt.legality_result,
        contained_success.result.authoritative_changed,
    ))

    # Closing the same container converts the same accepted request into a
    # meaningful legality rejection without changing authoritative lit state.
    assert app.close_object("chest").authoritative_changed is True
    digest_before_closed = app.authoritative_digest()
    closed_rejection = execute_vsm9_request(
        app, "ask groundskeeper to extinguish lantern"
    )
    outcomes.append((
        closed_rejection.request_receipt.acceptance,
        closed_rejection.request_receipt.legality_result,
        closed_rejection.result.authoritative_changed,
    ))
    assert app.authoritative_digest() == digest_before_closed
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    app.save()
    final_digest = app.authoritative_digest()
    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == final_digest
    assert restored.object_lit_state(LANTERN_ID).state == "lit"

    assert ("accepted", "allowed", True) in outcomes
    assert ("accepted", "rejected", False) in outcomes
    assert ("accepted", "allowed_no_change", False) in outcomes
    assert ("refused", "not_evaluated", False) in outcomes
