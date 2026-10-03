from __future__ import annotations

import hashlib
import json
from io import StringIO

import pytest

from astra_runtime.domain.persistent_world_actor_object_handoff import (
    PersistentWorldActorObjectHandoffRetryConflictError,
    execute_persistent_world_actor_object_handoff,
)
from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMP3_COMPONENT_CHECKPOINT_FORMAT_VERSION,
    VSM6_COMPONENT_CHECKPOINT_FORMAT_VERSION,
    WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    ORCHARD_PATH_ID,
    PLAYER_ID,
    TOOL_CHEST_ID,
    YARD_ID,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_terminal import (
    parse_terminal_command,
    run_terminal,
)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _carrier(app: MyravantPlayApplication, object_entity_id: str) -> str | None:
    matches = [
        relation
        for relation in app.state.representation.relations
        if relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
    ]
    if not matches:
        return None
    assert len(matches) == 1
    return matches[0].object_entity_id


def _setup_gatehouse_handoff(app: MyravantPlayApplication):
    assert app.pickup("lantern").authoritative_changed is True
    assert app.light_object("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.current_place_id() == app.entity_place_id(GROUNDSKEEPER_ID)
    return app.give_object("lantern", "groundskeeper")


def test_vsm6_parser_routes_bounded_handoff_forms():
    for raw in (
        "give lantern to groundskeeper",
        "give the lantern to the groundskeeper",
        "hand lantern to groundskeeper",
        "hand the lantern to the groundskeeper",
    ):
        parsed = parse_terminal_command(raw)
        assert parsed.action == "handoff", (raw, parsed)
        assert parsed.argument == "lantern -> groundskeeper", (raw, parsed)

    for raw in (
        "give it to groundskeeper",
        "give lantern to him",
        "give lantern to her",
        "give lantern to them",
        "give lantern to me",
        "give lantern to you",
    ):
        parsed = parse_terminal_command(raw)
        assert parsed.action == "ambiguous", (raw, parsed)
        assert parsed.failure_class == "ambiguous_target_reference"


def test_vsm6_requires_player_custody_and_colocated_recipient():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()
    not_carried = app.give_object("lantern", "groundskeeper")
    assert not_carried.authoritative_changed is False
    assert not_carried.failure_class == "actor_object_handoff_target_unavailable"
    assert app.authoritative_digest() == before

    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    before = app.authoritative_digest()
    not_colocated = app.give_object("lantern", "groundskeeper")
    assert not_colocated.authoritative_changed is False
    assert (
        not_colocated.failure_class
        == "actor_object_handoff_recipient_unavailable"
    )
    assert app.authoritative_digest() == before


def test_vsm6_player_to_groundskeeper_route_remains_bounded_and_qualified():
    app = MyravantPlayApplication.new()
    assert app.move("south").authoritative_changed is True
    assert app.move("south").authoritative_changed is True

    before = app.authoritative_digest()
    unknown = app.give_object("lantern", "waystone")
    assert unknown.authoritative_changed is False
    assert unknown.failure_class == "unknown_or_ambiguous_fixture_actor"
    assert app.authoritative_digest() == before

    tool = app.give_object("tool chest", "groundskeeper")
    assert tool.authoritative_changed is False
    assert tool.failure_class == "actor_object_handoff_target_unavailable"


def test_vsm6_handoff_commits_carrier_change_without_time_or_actor_movement():
    app = MyravantPlayApplication.new()
    time_before = app.runtime_state.logical_time_state.logical_position
    result = _setup_gatehouse_handoff(app)

    assert result.result_type == "actor_object_handoff_committed"
    assert result.authoritative_changed is True
    assert result.receipt_id is not None
    assert result.state_delta_id is not None
    assert result.spatial_evidence_id is not None
    assert result.opportunity_evidence_id is not None
    assert _carrier(app, LANTERN_ID) == GROUNDSKEEPER_ID
    assert app.current_place_id() == app.entity_place_id(GROUNDSKEEPER_ID)
    assert app.runtime_state.logical_time_state.logical_position == time_before
    assert len(
        app.runtime_state.committed_actor_object_handoff_transitions
    ) == 1
    assert app.object_lit_state(LANTERN_ID).state == "lit"


def test_vsm6_npc_carried_object_is_observable_but_not_player_controllable():
    app = MyravantPlayApplication.new()
    result = _setup_gatehouse_handoff(app)
    assert result.authoritative_changed is True

    view = app.look()
    facts = {
        fact.entity_id: fact
        for fact in view.view.observation_facts
    }
    assert LANTERN_ID in facts
    assert facts[LANTERN_ID].carrier_name == "Groundskeeper"
    assert "Brass Lantern" not in view.view.carrying

    before = app.authoritative_digest()
    pickup = app.pickup("lantern")
    assert pickup.authoritative_changed is False
    assert pickup.failure_class == "pickup_placement_unavailable"
    assert app.authoritative_digest() == before


def test_vsm6_lit_npc_carried_lantern_tracks_carrier_locality():
    app = MyravantPlayApplication.new()
    _setup_gatehouse_handoff(app)
    assert app._bounded_local_light_available() is True

    advanced = app.wait()
    assert advanced.authoritative_changed is True
    assert advanced.world_process_actor_id == GROUNDSKEEPER_ID
    assert advanced.world_process_action == "move"
    assert app.current_place_id() != app.entity_place_id(GROUNDSKEEPER_ID)
    assert _carrier(app, LANTERN_ID) == GROUNDSKEEPER_ID
    assert app._bounded_local_light_available() is False

    gatehouse_view = app.look()
    gatehouse_names = {
        fact.entity_id for fact in gatehouse_view.view.observation_facts
    }
    assert LANTERN_ID not in gatehouse_names

    assert app.move("north").authoritative_changed is True
    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert app._bounded_local_light_available() is True
    yard_view = app.look()
    yard_facts = {
        fact.entity_id: fact
        for fact in yard_view.view.observation_facts
    }
    assert yard_facts[LANTERN_ID].carrier_name == "Groundskeeper"


def test_vsm6_fresh_runs_are_deterministic():
    results = []
    for _ in range(2):
        app = MyravantPlayApplication.new()
        result = _setup_gatehouse_handoff(app)
        transition = (
            app.runtime_state.committed_actor_object_handoff_transitions[0]
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


def test_vsm6_same_command_retry_is_idempotent_and_changed_meaning_conflicts():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    fixture = app.fixture
    command_id = "vsm6-retry-000001"
    command = create_command_envelope(
        command_id=command_id,
        command_type="transfer_object",
        source_actor_id=PLAYER_ID,
        payload={
            "object_entity_id": LANTERN_ID,
            "recipient_actor_entity_id": GROUNDSKEEPER_ID,
            "method": "handoff",
        },
        metadata={"client": "vsm6-test"},
    )
    qualification, spatial, opportunity = fixture.actor_object_handoff_evidence(
        command_id=command_id,
        object_entity_id=LANTERN_ID,
        source_actor_entity_id=PLAYER_ID,
        recipient_actor_entity_id=GROUNDSKEEPER_ID,
        place_id=app.current_place_id(),
    )
    pre_digest = app.representation_digest()
    first = execute_persistent_world_actor_object_handoff(
        state=app.handoff_state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    retry = execute_persistent_world_actor_object_handoff(
        state=first.state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    assert retry.technical_retry is True
    assert retry.receipt == first.receipt
    assert retry.state == first.state

    changed = create_command_envelope(
        command_id=command_id,
        command_type="transfer_object",
        source_actor_id=PLAYER_ID,
        payload={
            "object_entity_id": TOOL_CHEST_ID,
            "recipient_actor_entity_id": GROUNDSKEEPER_ID,
            "method": "handoff",
        },
        metadata={"client": "vsm6-test"},
    )
    with pytest.raises(PersistentWorldActorObjectHandoffRetryConflictError):
        execute_persistent_world_actor_object_handoff(
            state=first.state,
            command=changed,
            qualification_evidence=qualification,
            spatial_evidence=spatial,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )


def test_vsm6_save_after_handoff_uses_v4_and_restores_exactly(tmp_path):
    path = tmp_path / "vsm6.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _setup_gatehouse_handoff(app)
    expected_digest = app.authoritative_digest()
    expected_receipt = (
        app.runtime_state.committed_actor_object_handoff_transitions[0]
        .receipt.to_dict()
    )
    app.save()

    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert (
        envelope["format_version"]
        == VSM6_COMPONENT_CHECKPOINT_FORMAT_VERSION
    )
    handoff_component = envelope["authoritative_payload"]["components"][
        "actor_object_handoff"
    ]
    assert (
        handoff_component["actor_object_handoff_transition_summary"]["count"]
        == 1
    )

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == expected_digest
    assert _carrier(restored, LANTERN_ID) == GROUNDSKEEPER_ID
    assert (
        restored.runtime_state.committed_actor_object_handoff_transitions[0]
        .receipt.to_dict()
        == expected_receipt
    )


def test_vsm6_handoff_then_world2_move_restores_combined_placement_chain(
    tmp_path,
):
    path = tmp_path / "vsm6-world2.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _setup_gatehouse_handoff(app)
    app.wait()
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    expected_digest = app.authoritative_digest()
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == expected_digest
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert _carrier(restored, LANTERN_ID) == GROUNDSKEEPER_ID
    assert restored.object_lit_state(LANTERN_ID).state == "lit"


def test_vsm6_semantically_tampered_v4_fails_with_recomputed_integrity(
    tmp_path,
):
    path = tmp_path / "vsm6-tampered.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _setup_gatehouse_handoff(app)
    app.save()

    envelope = json.loads(path.read_text(encoding="utf-8"))
    transition = envelope["authoritative_payload"]["components"][
        "actor_object_handoff"
    ]["committed_actor_object_handoff_transitions"][0]
    transition["receipt"]["post_state_digest"] = "0" * 64
    envelope["integrity_digest"] = hashlib.sha256(
        _canonical_bytes(envelope["authoritative_payload"])
    ).hexdigest()
    path.write_bytes(_canonical_bytes(envelope))

    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantPlayApplication.restore(checkpoint_path=path)


def test_vsm6_preserves_existing_v2_and_v3_writer_selection(tmp_path):
    v2_path = tmp_path / "world1.json"
    v2 = MyravantPlayApplication.new(checkpoint_path=v2_path)
    v2.save()
    assert (
        json.loads(v2_path.read_text(encoding="utf-8"))["format_version"]
        == WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION
    )

    v3_path = tmp_path / "comp3.json"
    v3 = MyravantPlayApplication.new(checkpoint_path=v3_path)
    assert v3.pickup("lantern").authoritative_changed is True
    assert v3.move("south").authoritative_changed is True
    assert v3.throw_object("lantern", "east").authoritative_changed is True
    assert _carrier(v3, LANTERN_ID) is None
    v3.save()
    assert (
        json.loads(v3_path.read_text(encoding="utf-8"))["format_version"]
        == COMP3_COMPONENT_CHECKPOINT_FORMAT_VERSION
    )
    restored = MyravantPlayApplication.restore(checkpoint_path=v3_path)
    assert restored.entity_place_id(PLAYER_ID) == YARD_ID
    assert any(
        relation.subject_entity_id == LANTERN_ID
        and relation.object_entity_id == ORCHARD_PATH_ID
        for relation in restored.state.representation.relations
    )


def test_vsm6_terminal_flow_exposes_handoff_without_social_state(tmp_path):
    checkpoint = tmp_path / "terminal-vsm6.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    output = StringIO()
    run_terminal(
        app,
        input_stream=StringIO(
            "pickup lantern\n"
            "light lantern\n"
            "move south\n"
            "move south\n"
            "give lantern to groundskeeper\n"
            "look\n"
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )
    visible = output.getvalue()
    assert "You hand the Brass Lantern to the Groundskeeper." in visible
    assert "Brass Lantern [lit; carried by Groundskeeper]" in visible

    restored = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert _carrier(restored, LANTERN_ID) == GROUNDSKEEPER_ID
