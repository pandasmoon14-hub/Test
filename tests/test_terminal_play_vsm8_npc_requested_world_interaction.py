from __future__ import annotations

from io import StringIO

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    TOOL_CHEST_ID,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_terminal import (
    parse_terminal_command,
    run_terminal,
)


def _setup_colocated_yard(app: MyravantPlayApplication) -> None:
    moved = app.move("south")
    assert moved.authoritative_changed is True
    advanced = app.wait()
    assert advanced.authoritative_changed is True
    assert app.entity_place_id(GROUNDSKEEPER_ID) == app.current_place_id()


def test_vsm8_parser_routes_only_explicit_actor_open_close_requests():
    cases = {
        "ask groundskeeper to open chest":
            "groundskeeper -> open -> chest",
        "ask the groundskeeper to open the chest":
            "groundskeeper -> open -> chest",
        "ask groundskeeper to close chest":
            "groundskeeper -> close -> chest",
        "ask the groundskeeper to shut the chest":
            "groundskeeper -> close -> chest",
    }
    for raw, expected in cases.items():
        parsed = parse_terminal_command(raw)
        assert parsed.action == "request_object_state", (raw, parsed)
        assert parsed.argument == expected, (raw, parsed)

    direct = parse_terminal_command("groundskeeper open the chest")
    assert direct.action == "unsupported"
    assert direct.failure_class == "unsupported_input_no_executable_route"

    handoff = parse_terminal_command("ask groundskeeper for lantern")
    assert handoff.action == "request_handoff"

    for raw in (
        "ask him to open chest",
        "ask groundskeeper to open it",
    ):
        parsed = parse_terminal_command(raw)
        assert parsed.action == "ambiguous"
        assert parsed.failure_class == "ambiguous_target_reference"


def test_vsm8_fixture_licenses_only_groundskeeper_tool_chest_open_close():
    fixture = create_terminal_play_fixture()
    routes = {
        (
            route.actor_entity_id,
            route.object_entity_id,
            route.operation,
        )
        for route in fixture.requested_object_state_routes
    }
    assert routes == {
        (GROUNDSKEEPER_ID, TOOL_CHEST_ID, "open"),
        (GROUNDSKEEPER_ID, TOOL_CHEST_ID, "close"),
    }


def test_vsm8_request_open_close_commits_existing_owner_with_npc_actor():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)

    time_before = app.runtime_state.logical_time_state.logical_position
    opened = app.request_object_state_from_actor(
        "groundskeeper",
        "open",
        "tool chest",
    )
    assert opened.result_type == "object_state_committed"
    assert opened.authoritative_changed is True
    assert opened.message == "The Groundskeeper opens the Tool Chest."
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"
    assert app.runtime_state.logical_time_state.logical_position == time_before

    transition = app.object_state.committed_object_state_transitions[-1]
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.object_entity_id == TOOL_CHEST_ID
    assert transition.receipt.operation == "open"

    closed = app.request_object_state_from_actor(
        "groundskeeper",
        "close",
        "tool chest",
    )
    assert closed.result_type == "object_state_committed"
    assert closed.authoritative_changed is True
    assert closed.message == "The Groundskeeper closes the Tool Chest."
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert app.runtime_state.logical_time_state.logical_position == time_before

    transition = app.object_state.committed_object_state_transitions[-1]
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.operation == "close"


def test_vsm8_request_rejects_separation_unknown_and_unlicensed_targets_safely():
    app = MyravantPlayApplication.new()
    assert app.move("south").authoritative_changed is True
    before = app.authoritative_digest()

    separated = app.request_object_state_from_actor(
        "groundskeeper",
        "open",
        "tool chest",
    )
    assert separated.authoritative_changed is False
    assert separated.failure_class == "object_state_request_actor_unavailable"
    assert app.authoritative_digest() == before

    unknown = app.request_object_state_from_actor(
        "blacksmith",
        "open",
        "tool chest",
    )
    assert unknown.authoritative_changed is False
    assert unknown.failure_class == "unknown_or_ambiguous_fixture_actor"
    assert app.authoritative_digest() == before

    assert app.wait().authoritative_changed is True
    before_unlicensed = app.authoritative_digest()
    unlicensed = app.request_object_state_from_actor(
        "groundskeeper",
        "open",
        "lantern",
    )
    assert unlicensed.authoritative_changed is False
    assert unlicensed.failure_class == "object_state_request_route_unavailable"
    assert app.authoritative_digest() == before_unlicensed


def test_vsm8_already_satisfied_requests_are_deterministic_and_nonmutating():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)

    assert app.request_object_state_from_actor(
        "groundskeeper",
        "open",
        "chest",
    ).authoritative_changed is True

    before = app.authoritative_digest()
    count_before = len(app.object_state.committed_object_state_transitions)
    repeated = app.request_object_state_from_actor(
        "groundskeeper",
        "open",
        "chest",
    )
    assert repeated.result_type == "object_state_unchanged"
    assert repeated.authoritative_changed is False
    assert app.authoritative_digest() == before
    assert len(app.object_state.committed_object_state_transitions) == count_before


def test_vsm8_world2_scheduled_open_composes_as_already_satisfied():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)
    assert app.runtime_state.logical_time_state.logical_position == 1

    requested = app.request_object_state_from_actor(
        "groundskeeper",
        "open",
        "chest",
    )
    assert requested.authoritative_changed is True
    count_before = len(app.object_state.committed_object_state_transitions)

    scheduled = app.wait()
    assert scheduled.logical_time_after == 2
    assert scheduled.world_process_actor_id == GROUNDSKEEPER_ID
    assert scheduled.world_process_action == "open_object"
    assert scheduled.world_process_outcome == "already_satisfied"
    assert len(app.object_state.committed_object_state_transitions) == count_before


def test_vsm8_world2_scheduled_close_composes_as_already_satisfied():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)
    assert app.request_object_state_from_actor(
        "groundskeeper",
        "open",
        "chest",
    ).authoritative_changed is True
    assert app.wait().world_process_outcome == "already_satisfied"
    assert app.runtime_state.logical_time_state.logical_position == 2

    requested = app.request_object_state_from_actor(
        "groundskeeper",
        "close",
        "chest",
    )
    assert requested.authoritative_changed is True
    count_before = len(app.object_state.committed_object_state_transitions)

    scheduled = app.wait()
    assert scheduled.logical_time_after == 3
    assert scheduled.world_process_actor_id == GROUNDSKEEPER_ID
    assert scheduled.world_process_action == "close_object"
    assert scheduled.world_process_outcome == "already_satisfied"
    assert len(app.object_state.committed_object_state_transitions) == count_before


def test_vsm8_save_restore_before_and_after_requested_action_is_exact(tmp_path):
    path = tmp_path / "vsm8.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _setup_colocated_yard(app)
    before_request = app.authoritative_digest()
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == before_request

    requested = restored.request_object_state_from_actor(
        "groundskeeper",
        "open",
        "chest",
    )
    assert requested.authoritative_changed is True
    final_digest = restored.authoritative_digest()
    restored.save()

    final = MyravantPlayApplication.restore(checkpoint_path=path)
    assert final.authoritative_digest() == final_digest
    assert final.object_open_state(TOOL_CHEST_ID).state == "open"
    receipt = final.object_state.committed_object_state_transitions[-1].receipt
    assert receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.object_entity_id == TOOL_CHEST_ID
    assert receipt.operation == "open"


def test_vsm8_fresh_runs_are_deterministic():
    results = []
    for _ in range(2):
        app = MyravantPlayApplication.new()
        _setup_colocated_yard(app)
        result = app.request_object_state_from_actor(
            "groundskeeper",
            "open",
            "chest",
        )
        transition = app.object_state.committed_object_state_transitions[-1]
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


def test_vsm8_terminal_request_and_vsm7_handoff_grammar_do_not_cross_route(tmp_path):
    path = tmp_path / "vsm8-terminal.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    output = StringIO()

    rc = run_terminal(
        app,
        input_stream=StringIO(
            "move south\n"
            "wait\n"
            "ask groundskeeper to open chest\n"
            "ask groundskeeper for help\n"
            "ask groundskeeper for a favor\n"
            "look\n"
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )
    assert rc == 0
    visible = output.getvalue()
    assert "The Groundskeeper opens the Tool Chest." in visible
    assert visible.count("That actor cannot return that object") == 2
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"

    transitions = app.object_state.committed_object_state_transitions
    requested = [
        item
        for item in transitions
        if item.receipt.actor_entity_id == GROUNDSKEEPER_ID
        and item.receipt.command_id.startswith("terminal-object-state-")
    ]
    assert len(requested) == 1
