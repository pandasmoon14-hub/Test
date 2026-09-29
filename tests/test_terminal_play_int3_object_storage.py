"""TERMINAL-PLAY-INT-3 bounded persistent object storage tests."""

from __future__ import annotations

import hashlib
import json
from io import StringIO

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    CONTAINED_BY_RELATION_TYPE,
    CONTAINED_BY_SEMANTIC_OWNER,
    InvalidContainedByRelationError,
    create_contained_by_relation,
)
from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
    WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError,
    write_persistent_world_object_lit_state_checkpoint,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    digest_persistent_world_containment,
    digest_persistent_world_object_storage_runtime_state,
    replay_persistent_world_object_storage,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    FIXTURE_INT2_INITIAL_WORLD_STATE_DIGEST,
    FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST,
    FIXTURE_VERSION,
    LANTERN_ID,
    PLAYER_ID,
    TOOL_CHEST_ID,
)
from astra_runtime.myravant_terminal import parse_terminal_command, run_terminal


def _contained_relation(app):
    matches = [
        relation
        for relation in app.state.representation.relations
        if relation.relation_type == CONTAINED_BY_RELATION_TYPE
        and relation.subject_entity_id == LANTERN_ID
    ]
    return matches[0] if len(matches) == 1 else None


def _prepare_open_chest_with_carried_lantern(app):
    app.pickup("lantern")
    app.move("south")
    app.open_object("chest")


def test_int3_contained_by_relation_is_rt010_owned_and_rejects_self_containment():
    relation = create_contained_by_relation(
        relation_id="astra:relation:test-contained",
        subject_entity_id=LANTERN_ID,
        object_entity_id=TOOL_CHEST_ID,
    )
    assert relation.relation_type == CONTAINED_BY_RELATION_TYPE
    assert relation.semantic_owner == CONTAINED_BY_SEMANTIC_OWNER == "RT-010"
    with pytest.raises(InvalidContainedByRelationError):
        create_contained_by_relation(
            relation_id="astra:relation:test-self-contained",
            subject_entity_id=LANTERN_ID,
            object_entity_id=LANTERN_ID,
        )


def test_int3_fixture_version_and_initial_digest_are_frozen():
    app = MyravantPlayApplication.new()
    assert FIXTURE_VERSION == "0.2.1"
    assert app.lit_state == app.storage_state.lit_state
    assert app.storage_world_digest() == FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST
    assert app.authoritative_digest() != FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST
    assert digest_persistent_world_object_storage_runtime_state(app.storage_state) == (
        FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST
    )
    assert digest_persistent_world_containment(app.state.representation)
    assert app.fixture.provenance.initial_int2_world_state_digest == (
        FIXTURE_INT2_INITIAL_WORLD_STATE_DIGEST
    )
    assert app.fixture.provenance.initial_int3_world_state_digest == (
        FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST
    )


def test_int3_store_and_retrieve_replace_exactly_one_immediate_placement():
    app = MyravantPlayApplication.new()
    _prepare_open_chest_with_carried_lantern(app)

    stored = app.store_object("lantern", "chest")
    assert stored.result_type == "storage_committed"
    assert stored.authoritative_changed is True
    relation = _contained_relation(app)
    assert relation is not None
    assert relation.object_entity_id == TOOL_CHEST_ID
    assert not any(
        r.relation_type == CARRIED_BY_RELATION_TYPE
        and r.subject_entity_id == LANTERN_ID
        for r in app.state.representation.relations
    )

    retrieved = app.retrieve_object("lantern", "chest")
    assert retrieved.result_type == "storage_committed"
    assert _contained_relation(app) is None
    assert any(
        r.relation_type == CARRIED_BY_RELATION_TYPE
        and r.subject_entity_id == LANTERN_ID
        and r.object_entity_id == PLAYER_ID
        for r in app.state.representation.relations
    )


def test_int3_storage_noop_and_closed_container_rejections_are_nonmutating():
    app = MyravantPlayApplication.new()
    app.pickup("lantern")
    app.move("south")

    before = app.authoritative_digest()
    closed = app.store_object("lantern", "chest")
    assert closed.result_type == "storage_rejected"
    assert closed.failure_class == "storage_container_closed"
    assert closed.pre_state_digest == closed.post_state_digest == before
    assert closed.command_id is None

    app.open_object("chest")
    app.store_object("lantern", "chest")
    before_noop = app.authoritative_digest()
    noop = app.store_object("lantern", "chest")
    assert noop.result_type == "storage_unchanged"
    assert noop.command_id is None
    assert noop.pre_state_digest == noop.post_state_digest == before_noop


def test_int3_open_container_exposes_contained_lantern_and_lit_state_owner_accepts_it():
    app = MyravantPlayApplication.new()
    _prepare_open_chest_with_carried_lantern(app)
    app.store_object("lantern", "chest")

    chest = app.inspect("chest")
    assert "Brass Lantern" in chest.view.description
    lantern = app.inspect("lantern")
    assert lantern.result_type == "inspection"
    assert "flame is out" in lantern.view.description.casefold()

    lit = app.light_object("lantern")
    assert lit.result_type == "object_lit_state_committed"
    assert "steady flame burns" in app.inspect("lantern").view.description.casefold()

    app.close_object("chest")
    hidden = app.inspect("lantern")
    assert hidden.result_type == "inspection_unavailable"
    blocked = app.extinguish_object("lantern")
    assert blocked.result_type == "object_lit_state_rejected"
    assert blocked.failure_class == "object_lit_state_target_unavailable"


def test_int3_containment_survives_container_custody_and_movement():
    app = MyravantPlayApplication.new()
    _prepare_open_chest_with_carried_lantern(app)
    app.store_object("lantern", "chest")
    app.close_object("chest")
    app.pickup("chest")
    app.move("north")

    relation = _contained_relation(app)
    assert relation is not None
    assert relation.object_entity_id == TOOL_CHEST_ID
    assert app.current_place_id().endswith(":workshop")
    assert "Brass Lantern" not in app.look().view.carrying

    app.drop("chest")
    app.open_object("chest")
    taken = app.pickup("lantern")
    assert taken.result_type == "storage_committed"
    assert _contained_relation(app) is None


def test_int3_checkpoint_round_trip_preserves_storage_and_lower_state(tmp_path):
    checkpoint = tmp_path / "int3.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.light_object("lantern")
    _prepare_open_chest_with_carried_lantern(app)
    app.store_object("lantern", "chest")
    app.close_object("chest")
    before = app.authoritative_digest()
    app.save()

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert envelope["format_identity"] == COMPONENT_CHECKPOINT_FORMAT_IDENTITY
    assert envelope["format_version"] == WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION
    assert set(envelope["authoritative_payload"]["components"]) == set(
        WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS
    )
    assert "int2_state" not in envelope["authoritative_payload"]

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == before
    assert _contained_relation(restored) is not None
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
    assert restored.object_open_state(TOOL_CHEST_ID).state == "closed"

    restored.open_object("chest")
    assert restored.pickup("lantern").result_type == "storage_committed"


def test_int3_legacy_int2_checkpoint_restores_empty_storage_and_upgrades(tmp_path):
    checkpoint = tmp_path / "legacy-int2.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.light_object("lantern")
    write_persistent_world_object_lit_state_checkpoint(
        state=app.lit_state,
        checkpoint_path=checkpoint,
        qualification_evidence=app.fixture.checkpoint_qualification,
    )

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.storage_state.committed_storage_transitions == ()
    restored.save()
    upgraded = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert upgraded["format_identity"] == COMPONENT_CHECKPOINT_FORMAT_IDENTITY


def test_int3_recomputed_outer_integrity_cannot_hide_storage_evidence_tamper(tmp_path):
    checkpoint = tmp_path / "tampered-int3.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    _prepare_open_chest_with_carried_lantern(app)
    app.store_object("lantern", "chest")
    app.save()

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    receipt = envelope["authoritative_payload"]["components"]["storage"]["committed_storage_transitions"][0]["receipt"]
    receipt["container_entity_id"] = LANTERN_ID
    payload = envelope["authoritative_payload"]
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    envelope["integrity_digest"] = hashlib.sha256(canonical).hexdigest()
    checkpoint.write_text(
        json.dumps(
            envelope,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantPlayApplication.restore(checkpoint_path=checkpoint)


def test_int3_owner_receipt_replays_deterministically():
    app = MyravantPlayApplication.new()
    _prepare_open_chest_with_carried_lantern(app)
    pre = app.state.representation
    result = app.store_object("lantern", "chest")
    transition = app.storage_state.committed_storage_transitions[0]

    replayed = replay_persistent_world_object_storage(
        representation=pre,
        receipt=transition.receipt,
    )
    assert result.post_state_digest == app.authoritative_digest()
    assert replayed == app.state.representation


def test_int3_parser_routes_storage_and_transparent_take_without_compound_collapse():
    for raw, action, argument in (
        ("put lantern in chest", "store", "lantern -> chest"),
        ("put the lantern in the chest", "store", "lantern -> chest"),
        ("place lantern in chest", "store", "lantern -> chest"),
        ("store lantern in chest", "store", "lantern -> chest"),
        ("take lantern from chest", "retrieve", "lantern -> chest"),
        ("remove lantern from chest", "retrieve", "lantern -> chest"),
        ("retrieve lantern from chest", "retrieve", "lantern -> chest"),
    ):
        parsed = parse_terminal_command(raw)
        assert parsed.action == action
        assert parsed.argument == argument

    assert parse_terminal_command("take lantern").action == "pickup"
    assert parse_terminal_command("put it in chest").action == "ambiguous"
    compound = parse_terminal_command("put lantern in chest and close chest")
    assert compound.action == "unsupported"
    assert compound.failure_class == "unsupported_compound_intent_sequencing"


def test_int3_terminal_storage_trace_is_playable_and_persistent(tmp_path):
    checkpoint = tmp_path / "terminal-int3.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    output = StringIO()
    run_terminal(
        app,
        input_stream=StringIO(
            "pickup lantern\nmove south\nopen chest\nput lantern in chest\n"
            "inspect chest\nclose chest\nsave\nexit\n"
        ),
        output_stream=output,
    )
    text = output.getvalue()
    assert "You store the Brass Lantern in the Tool Chest." in text
    assert "Brass Lantern" in text
    assert checkpoint.exists()
