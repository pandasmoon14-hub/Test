from __future__ import annotations

import json
from io import StringIO

from astra_runtime.domain.persistent_world_component_checkpoint import (
    VSM6_COMPONENT_CHECKPOINT_FORMAT_VERSION,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    FIXTURE_VERSION,
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    PLAYER_ID,
    YARD_ID,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_terminal import (
    parse_terminal_command,
    run_terminal,
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


def _setup_forward_handoff(app: MyravantPlayApplication) -> None:
    assert app.pickup("lantern").authoritative_changed is True
    assert app.light_object("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.current_place_id() == GATEHOUSE_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    forward = app.give_object("lantern", "groundskeeper")
    assert forward.authoritative_changed is True
    assert _carrier(app) == GROUNDSKEEPER_ID


def test_vsm7_parser_routes_request_without_granting_direct_npc_command():
    for raw in (
        "ask groundskeeper for lantern",
        "ask the groundskeeper for the lantern",
    ):
        parsed = parse_terminal_command(raw)
        assert parsed.action == "request_handoff", (raw, parsed)
        assert parsed.argument == "groundskeeper -> lantern", (raw, parsed)

    for raw in (
        "ask him for lantern",
        "ask them for lantern",
        "ask groundskeeper for it",
    ):
        parsed = parse_terminal_command(raw)
        assert parsed.action == "ambiguous", (raw, parsed)
        assert parsed.failure_class == "ambiguous_target_reference"

    direct_npc_command = parse_terminal_command(
        "groundskeeper give lantern to me"
    )
    assert direct_npc_command.action == "unsupported"
    assert (
        direct_npc_command.failure_class
        == "unsupported_input_no_executable_route"
    )


def test_vsm7_fixture_licenses_only_the_bounded_reciprocal_lantern_route():
    fixture = create_terminal_play_fixture()
    assert FIXTURE_VERSION == "0.2.1"
    routes = {
        (
            route.object_entity_id,
            route.source_actor_entity_id,
            route.recipient_actor_entity_id,
            route.method,
        )
        for route in fixture.actor_object_handoff_routes
    }
    assert (
        LANTERN_ID,
        PLAYER_ID,
        GROUNDSKEEPER_ID,
        "handoff",
    ) in routes
    assert (
        LANTERN_ID,
        GROUNDSKEEPER_ID,
        PLAYER_ID,
        "handoff",
    ) in routes
    assert len(routes) == 2


def test_vsm7_request_commits_reverse_handoff_without_time_or_lit_change():
    app = MyravantPlayApplication.new()
    _setup_forward_handoff(app)

    time_before = app.runtime_state.logical_time_state.logical_position
    result = app.request_object_from_actor("groundskeeper", "lantern")

    assert result.result_type == "actor_object_handoff_committed"
    assert result.authoritative_changed is True
    assert result.receipt_id is not None
    assert result.state_delta_id is not None
    assert result.spatial_evidence_id is not None
    assert result.opportunity_evidence_id is not None
    assert result.message == "The Groundskeeper hands you the Brass Lantern."
    assert _carrier(app) == PLAYER_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"
    assert app.runtime_state.logical_time_state.logical_position == time_before

    transitions = app.runtime_state.committed_actor_object_handoff_transitions
    assert len(transitions) == 2
    reverse = transitions[-1].receipt
    assert reverse.source_actor_entity_id == GROUNDSKEEPER_ID
    assert reverse.recipient_actor_entity_id == PLAYER_ID
    assert reverse.object_entity_id == LANTERN_ID


def test_vsm7_request_requires_source_custody_and_colocation_and_repeats_safely():
    app = MyravantPlayApplication.new()

    initial = app.authoritative_digest()
    absent = app.request_object_from_actor("groundskeeper", "lantern")
    assert absent.authoritative_changed is False
    assert absent.failure_class == "actor_object_handoff_target_unavailable"
    assert app.authoritative_digest() == initial

    _setup_forward_handoff(app)
    returned = app.request_object_from_actor("groundskeeper", "lantern")
    assert returned.authoritative_changed is True

    before_repeat = app.authoritative_digest()
    repeated = app.request_object_from_actor("groundskeeper", "lantern")
    assert repeated.authoritative_changed is False
    assert repeated.failure_class == "actor_object_handoff_target_unavailable"
    assert app.authoritative_digest() == before_repeat

    other = MyravantPlayApplication.new()
    _setup_forward_handoff(other)
    advanced = other.wait()
    assert advanced.authoritative_changed is True
    assert other.current_place_id() == GATEHOUSE_ID
    assert other.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    before_separated = other.authoritative_digest()
    separated = other.request_object_from_actor(
        "groundskeeper",
        "lantern",
    )
    assert separated.authoritative_changed is False
    assert separated.failure_class == "actor_object_handoff_source_unavailable"
    assert other.authoritative_digest() == before_separated


def test_vsm7_return_restores_normal_player_custody_actionability():
    app = MyravantPlayApplication.new()
    _setup_forward_handoff(app)
    assert app.request_object_from_actor(
        "groundskeeper",
        "lantern",
    ).authoritative_changed is True
    assert _carrier(app) == PLAYER_ID

    extinguish = app.extinguish_object("lantern")
    assert extinguish.result_type == "object_lit_state_committed"
    assert extinguish.authoritative_changed is True

    drop = app.drop("lantern")
    assert drop.result_type == "custody_committed"
    assert drop.authoritative_changed is True
    assert _carrier(app) is None


def test_vsm7_fresh_runs_are_deterministic():
    results = []
    for _ in range(2):
        app = MyravantPlayApplication.new()
        _setup_forward_handoff(app)
        result = app.request_object_from_actor("groundskeeper", "lantern")
        assert result.authoritative_changed is True
        transition = (
            app.runtime_state.committed_actor_object_handoff_transitions[-1]
        )
        results.append(
            (
                result.command_id,
                result.command_fingerprint,
                result.receipt_id,
                result.state_delta_id,
                result.post_state_digest,
                transition.receipt.to_dict(),
            )
        )
    assert results[0] == results[1]


def test_vsm7_v4_restore_before_and_after_return_is_exact(tmp_path):
    path = tmp_path / "vsm7.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _setup_forward_handoff(app)
    forward_digest = app.authoritative_digest()
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == forward_digest
    assert _carrier(restored) == GROUNDSKEEPER_ID

    returned = restored.request_object_from_actor(
        "groundskeeper",
        "lantern",
    )
    assert returned.authoritative_changed is True
    final_digest = restored.authoritative_digest()
    restored.save()

    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert (
        envelope["format_version"]
        == VSM6_COMPONENT_CHECKPOINT_FORMAT_VERSION
    )
    component = envelope["authoritative_payload"]["components"][
        "actor_object_handoff"
    ]
    assert (
        component["actor_object_handoff_transition_summary"]["count"]
        == 2
    )

    final = MyravantPlayApplication.restore(checkpoint_path=path)
    assert final.authoritative_digest() == final_digest
    assert _carrier(final) == PLAYER_ID
    receipts = [
        item.receipt
        for item in final.runtime_state.committed_actor_object_handoff_transitions
    ]
    assert len(receipts) == 2
    assert receipts[0].source_actor_entity_id == PLAYER_ID
    assert receipts[0].recipient_actor_entity_id == GROUNDSKEEPER_ID
    assert receipts[1].source_actor_entity_id == GROUNDSKEEPER_ID
    assert receipts[1].recipient_actor_entity_id == PLAYER_ID


def test_vsm7_terminal_request_closes_the_handoff_loop(tmp_path):
    checkpoint = tmp_path / "terminal-vsm7.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    output = StringIO()

    rc = run_terminal(
        app,
        input_stream=StringIO(
            "pickup lantern\n"
            "light lantern\n"
            "move south\n"
            "move south\n"
            "give lantern to groundskeeper\n"
            "ask groundskeeper for lantern\n"
            "look\n"
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )

    assert rc == 0
    visible = output.getvalue()
    assert "You hand the Brass Lantern to the Groundskeeper." in visible
    assert "The Groundskeeper hands you the Brass Lantern." in visible
    assert "Carrying: Brass Lantern" in visible

    restored = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert _carrier(restored) == PLAYER_ID
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
