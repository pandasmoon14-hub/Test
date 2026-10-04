from __future__ import annotations

import hashlib
import json
from io import StringIO

import pytest

from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMP3_COMPONENT_CHECKPOINT_FORMAT_VERSION,
    WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID,
    ORCHARD_PATH_ID,
    YARD_ID,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_terminal import (
    parse_terminal_command,
    run_terminal,
)


def _setup_throwable(app: MyravantPlayApplication) -> None:
    assert app.pickup("lantern").authoritative_changed is True
    assert app.light_object("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True


def _setup_unlit_throwable(app: MyravantPlayApplication) -> None:
    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True


def _placement_target(
    app: MyravantPlayApplication,
    object_id: str,
) -> tuple[str, str]:
    matches = [
        relation
        for relation in app.state.representation.relations
        if relation.subject_entity_id == object_id
        and relation.relation_type
        in {CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE}
    ]
    assert len(matches) == 1
    return matches[0].relation_type, matches[0].object_entity_id


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def test_comp3_parser_routes_bounded_throw_without_generalizing_frontier():
    for raw in (
        "throw lantern east",
        "throw the lantern east",
        "toss lantern east",
        "hurl lantern east",
    ):
        parsed = parse_terminal_command(raw)
        assert parsed.action == "throw", (raw, parsed)
        assert parsed.argument == "lantern -> east", (raw, parsed)

    deictic = parse_terminal_command("throw it east")
    assert deictic.action == "ambiguous"
    assert deictic.failure_class == "ambiguous_target_reference"

    frontier = parse_terminal_command("throw the lantern over the wall")
    assert frontier.action == "unsupported"
    assert frontier.failure_class == "unsupported_capability_throwing"


def test_comp3_route_is_independent_of_movement_and_directional_sensing():
    fixture = create_terminal_play_fixture()
    assert fixture.destination_for(
        source_place_id=YARD_ID,
        direction="east",
    ) == ORCHARD_PATH_ID
    directional = fixture.directional_observation_evidence(
        observer_entity_id=fixture.player_entity_id,
        source_place_id=YARD_ID,
        direction="east",
    )
    assert directional.observable is False
    assert directional.target_place_id is None
    assert fixture.object_displacement_destination_for(
        object_entity_id=LANTERN_ID,
        source_place_id=YARD_ID,
        direction="east",
        method="throw",
    ) == ORCHARD_PATH_ID


def test_comp3_throw_requires_carried_object_and_explicit_route():
    app = MyravantPlayApplication.new()
    assert app.move("south").authoritative_changed is True
    before = app.authoritative_digest()
    unavailable = app.throw_object("lantern", "east")
    assert unavailable.result_type == "object_displacement_rejected"
    assert unavailable.failure_class == "object_displacement_target_unavailable"
    assert unavailable.authoritative_changed is False
    assert app.authoritative_digest() == before

    app2 = MyravantPlayApplication.new()
    assert app2.pickup("lantern").authoritative_changed is True
    before2 = app2.authoritative_digest()
    wrong_source = app2.throw_object("lantern", "south")
    assert wrong_source.failure_class == "object_displacement_route_unavailable"
    assert app2.authoritative_digest() == before2


def test_comp3_lit_throw_exposes_only_bounded_directional_light_signal():
    app = MyravantPlayApplication.new()
    _setup_throwable(app)
    assert app.current_place_id() == YARD_ID
    time_before = app.runtime_state.logical_time_state.logical_position

    pre_look = app.look_direction("east")
    assert pre_look.result_type == "directional_observation_unavailable"
    assert pre_look.failure_class == "directional_observation_unlicensed"
    pre_digest = app.authoritative_digest()

    result = app.throw_object("lantern", "east")

    assert result.result_type == "object_displacement_committed"
    assert result.authoritative_changed is True
    assert result.spatial_evidence_id is not None
    assert result.opportunity_evidence_id is not None
    assert result.receipt_id is not None
    assert result.state_delta_id is not None
    assert result.pre_state_digest == pre_digest
    assert result.post_state_digest == app.authoritative_digest()
    assert app.current_place_id() == YARD_ID
    assert app.runtime_state.logical_time_state.logical_position == time_before
    assert _placement_target(app, LANTERN_ID) == (
        LOCATED_AT_RELATION_TYPE,
        ORCHARD_PATH_ID,
    )
    assert len(
        app.runtime_state.committed_object_displacement_transitions
    ) == 1

    signal_pre_digest = app.authoritative_digest()
    post_look = app.look_direction("east")
    assert post_look.result_type == "directional_light_signal"
    assert post_look.message == "You can see the Brass Lantern's light to the east."
    assert post_look.view is None
    assert post_look.observation_evidence_id is not None
    assert post_look.failure_class is None
    assert post_look.authoritative_changed is False
    assert post_look.pre_state_digest == signal_pre_digest
    assert post_look.post_state_digest == signal_pre_digest
    assert app.authoritative_digest() == signal_pre_digest
    assert "Orchard Path" not in post_look.message


def test_comp3_unlit_throw_does_not_create_directional_light_signal():
    app = MyravantPlayApplication.new()
    _setup_unlit_throwable(app)
    result = app.throw_object("lantern", "east")
    assert result.authoritative_changed is True
    assert app.object_lit_state(LANTERN_ID).state == "unlit"

    before = app.authoritative_digest()
    post_look = app.look_direction("east")
    assert post_look.result_type == "directional_observation_unavailable"
    assert post_look.failure_class == "directional_observation_unlicensed"
    assert post_look.view is None
    assert app.authoritative_digest() == before


def test_comp3_success_message_does_not_reveal_unobserved_destination_identity():
    app = MyravantPlayApplication.new()
    _setup_throwable(app)
    result = app.throw_object("lantern", "east")
    assert result.message == "You throw the Brass Lantern east."
    assert "Orchard Path" not in result.message


def test_comp3_lit_state_survives_throw_and_becomes_local_after_player_moves():
    app = MyravantPlayApplication.new()
    _setup_throwable(app)
    app.throw_object("lantern", "east")

    assert app.object_lit_state(LANTERN_ID).state == "lit"
    assert app.move("east").authoritative_changed is True
    view = app.look()
    assert view.result_type == "look"
    assert view.view is not None
    names = [fact.name for fact in view.view.observation_facts]
    assert "Brass Lantern" in names


def test_comp3_repeated_fresh_runs_are_deterministic():
    results = []
    for _ in range(2):
        app = MyravantPlayApplication.new()
        _setup_throwable(app)
        result = app.throw_object("lantern", "east")
        signal = app.look_direction("east")
        transition = (
            app.runtime_state.committed_object_displacement_transitions[0]
        )
        results.append(
            (
                result.command_id,
                result.command_fingerprint,
                result.receipt_id,
                result.state_delta_id,
                result.post_state_digest,
                transition.receipt.to_dict(),
                signal.result_type,
                signal.observation_evidence_id,
                signal.message,
            )
        )
    assert results[0] == results[1]


def test_comp3_legacy_save_without_displacement_remains_world1_v2(tmp_path):
    path = tmp_path / "legacy-current.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    app.save()
    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert (
        envelope["format_version"]
        == WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION
    )
    assert (
        "object_displacement"
        not in envelope["authoritative_payload"]["components"]
    )


def test_comp3_save_after_throw_uses_v3_component_and_restores_exactly(
    tmp_path,
):
    path = tmp_path / "comp3.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _setup_throwable(app)
    app.throw_object("lantern", "east")
    expected_digest = app.authoritative_digest()
    expected_receipt = (
        app.runtime_state.committed_object_displacement_transitions[0]
        .receipt.to_dict()
    )

    save = app.save()
    assert save.authoritative_changed is False

    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert (
        envelope["format_version"]
        == COMP3_COMPONENT_CHECKPOINT_FORMAT_VERSION
    )
    component = envelope["authoritative_payload"]["components"][
        "object_displacement"
    ]
    assert (
        component["object_displacement_transition_summary"]["count"]
        == 1
    )

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == expected_digest
    assert _placement_target(restored, LANTERN_ID) == (
        LOCATED_AT_RELATION_TYPE,
        ORCHARD_PATH_ID,
    )
    assert (
        restored.runtime_state.committed_object_displacement_transitions[0]
        .receipt.to_dict()
        == expected_receipt
    )
    restored_signal = restored.look_direction("east")
    assert restored_signal.result_type == "directional_light_signal"
    assert restored_signal.message == "You can see the Brass Lantern's light to the east."
    assert restored_signal.view is None
    assert restored_signal.observation_evidence_id is not None
    assert restored.authoritative_digest() == expected_digest


def test_comp3_semantically_tampered_v3_fails_even_with_new_outer_integrity(
    tmp_path,
):
    path = tmp_path / "tampered.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _setup_throwable(app)
    app.throw_object("lantern", "east")
    app.save()

    envelope = json.loads(path.read_text(encoding="utf-8"))
    transition = envelope["authoritative_payload"]["components"][
        "object_displacement"
    ]["committed_object_displacement_transitions"][0]
    transition["receipt"]["post_state_digest"] = "0" * 64
    envelope["integrity_digest"] = hashlib.sha256(
        _canonical_bytes(envelope["authoritative_payload"])
    ).hexdigest()
    path.write_bytes(_canonical_bytes(envelope))

    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantPlayApplication.restore(checkpoint_path=path)


def test_comp3_terminal_flow_persists_consequence_without_destination_leak(
    tmp_path,
):
    checkpoint = tmp_path / "terminal-comp3.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    output = StringIO()
    run_terminal(
        app,
        input_stream=StringIO(
            "pickup lantern\n"
            "light lantern\n"
            "move south\n"
            "look east\n"
            "throw lantern east\n"
            "look east\n"
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )
    visible = output.getvalue()
    assert "You throw the Brass Lantern east." in visible
    assert visible.count(
        "You cannot make out a distinct place in that direction from here."
    ) == 1
    assert "You can see the Brass Lantern's light to the east." in visible
    assert "To the east: Orchard Path" not in visible
    assert "Orchard Path" not in visible

    restored = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert _placement_target(restored, LANTERN_ID) == (
        LOCATED_AT_RELATION_TYPE,
        ORCHARD_PATH_ID,
    )
    restored_signal = restored.look_direction("east")
    assert restored_signal.result_type == "directional_light_signal"


def test_comp3_unlicensed_throw_is_side_effect_free():
    app = MyravantPlayApplication.new()
    _setup_throwable(app)
    before = app.authoritative_digest()

    result = app.throw_object("lantern", "north")
    assert result.authoritative_changed is False
    assert result.failure_class == "object_displacement_route_unavailable"
    assert app.authoritative_digest() == before
    assert len(
        app.runtime_state.committed_object_displacement_transitions
    ) == 0
