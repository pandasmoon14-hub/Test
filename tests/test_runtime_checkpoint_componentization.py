"""RUNTIME-CHECKPOINT-COMPONENTIZATION-1 regression tests."""

from __future__ import annotations

import hashlib
import json

import pytest

from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
    COMPONENT_CHECKPOINT_FORMAT_VERSION,
    canonical_serialize_persistent_world_component_checkpoint_envelope,
    restore_persistent_world_component_checkpoint,
    serialize_persistent_world_component_checkpoint_payload,
    write_persistent_world_component_checkpoint,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    OBJECT_STORAGE_CHECKPOINT_FORMAT_IDENTITY,
    PersistentWorldCheckpointEvidenceError,
    PersistentWorldCheckpointFormatError,
    restore_persistent_world_object_storage_checkpoint,
    serialize_persistent_world_object_storage_checkpoint_payload,
    write_persistent_world_object_storage_checkpoint,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    digest_persistent_world_object_storage_runtime_state,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication


def _rich_app(checkpoint_path):
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint_path)
    app.light_object("lantern")
    app.pickup("lantern")
    app.move("south")
    app.open_object("tool chest")
    app.store_object("lantern", "tool chest")
    return app


def _restore_direct(path, app):
    return restore_persistent_world_component_checkpoint(
        checkpoint_path=path,
        expected_campaign_id=app.fixture.campaign_id,
        expected_initial_open_states=app.fixture.initial_object_open_states,
        expected_initial_lit_states=app.fixture.initial_object_lit_states,
        expected_initial_representation_digest=(
            app.fixture.provenance.initial_state_digest
        ),
    )


def _rewrite_with_valid_outer_integrity(path, envelope):
    payload = envelope["authoritative_payload"]
    canonical_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    envelope["integrity_digest"] = hashlib.sha256(canonical_payload).hexdigest()
    path.write_text(
        json.dumps(
            envelope,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ),
        encoding="utf-8",
    )


def test_component_payload_is_flat_exact_projection_of_int3_material(tmp_path):
    app = _rich_app(tmp_path / "unused.json")
    payload = serialize_persistent_world_component_checkpoint_payload(
        app.storage_state
    )
    legacy = serialize_persistent_world_object_storage_checkpoint_payload(
        app.storage_state
    )

    assert set(payload) == {"components"}
    components = payload["components"]
    assert set(components) == set(COMPONENT_CHECKPOINT_COMPONENT_KEYS)

    int2 = legacy["int2_state"]
    int1 = int2["int1_state"]
    r4e = int1["r4e_state"]

    assert components["placement"] == {
        "representation": r4e["representation"],
        "representation_digest": r4e["representation_digest"],
        "committed_movement_transitions": r4e["committed_movement_transitions"],
        "movement_transition_summary": r4e["movement_transition_summary"],
    }
    assert components["custody"] == {
        "committed_custody_transitions": r4e["committed_custody_transitions"],
        "custody_transition_summary": r4e["custody_transition_summary"],
    }
    assert components["open_close"] == {
        "object_open_states": int1["object_open_states"],
        "object_state_digest": int1["object_state_digest"],
        "world_state_digest": int1["world_state_digest"],
        "committed_object_state_transitions": (
            int1["committed_object_state_transitions"]
        ),
        "object_state_transition_summary": (
            int1["object_state_transition_summary"]
        ),
    }
    assert components["lit_state"] == {
        "object_lit_states": int2["object_lit_states"],
        "object_lit_state_digest": int2["object_lit_state_digest"],
        "world_state_digest": int2["world_state_digest"],
        "committed_object_lit_transitions": (
            int2["committed_object_lit_transitions"]
        ),
        "object_lit_transition_summary": int2["object_lit_transition_summary"],
    }
    assert components["storage"] == {
        "containment_digest": legacy["containment_digest"],
        "world_state_digest": legacy["world_state_digest"],
        "committed_storage_transitions": legacy["committed_storage_transitions"],
        "storage_transition_summary": legacy["storage_transition_summary"],
    }

    serialized = json.dumps(payload, sort_keys=True)
    assert '"r4e_state"' not in serialized
    assert '"int1_state"' not in serialized
    assert '"int2_state"' not in serialized


def test_component_checkpoint_is_deterministic_for_same_state_and_qualification(
    tmp_path,
):
    app = _rich_app(tmp_path / "unused.json")
    first = canonical_serialize_persistent_world_component_checkpoint_envelope(
        state=app.storage_state,
        qualification_evidence=app.fixture.checkpoint_qualification,
    )
    second = canonical_serialize_persistent_world_component_checkpoint_envelope(
        state=app.storage_state,
        qualification_evidence=app.fixture.checkpoint_qualification,
    )
    assert first == second


def test_component_checkpoint_round_trip_preserves_authoritative_state(tmp_path):
    path = tmp_path / "component.json"
    app = _rich_app(path)
    before = app.authoritative_digest()

    write_persistent_world_component_checkpoint(
        state=app.storage_state,
        checkpoint_path=path,
        qualification_evidence=app.fixture.checkpoint_qualification,
    )
    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert envelope["format_identity"] == COMPONENT_CHECKPOINT_FORMAT_IDENTITY
    assert envelope["format_version"] == COMPONENT_CHECKPOINT_FORMAT_VERSION

    restored = _restore_direct(path, app)
    assert digest_persistent_world_object_storage_runtime_state(restored) == before
    assert len(restored.lit_state.open_close_state.custody_state.movement_state.committed_transitions) == 1
    assert len(restored.lit_state.open_close_state.custody_state.committed_custody_transitions) == 1
    assert len(restored.lit_state.open_close_state.committed_object_state_transitions) == 1
    assert len(restored.lit_state.committed_object_lit_transitions) == 1
    assert len(restored.committed_storage_transitions) == 1


@pytest.mark.parametrize("mutation", ["missing", "unknown", "malformed"])
def test_component_set_is_exact_and_fails_closed(tmp_path, mutation):
    path = tmp_path / f"{mutation}.json"
    app = _rich_app(path)
    app.save()
    envelope = json.loads(path.read_text(encoding="utf-8"))
    components = envelope["authoritative_payload"]["components"]

    if mutation == "missing":
        del components["custody"]
    elif mutation == "unknown":
        components["future_unknown_component"] = {}
    else:
        components["custody"]["unexpected_field"] = "not-authorized"

    _rewrite_with_valid_outer_integrity(path, envelope)

    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantPlayApplication.restore(checkpoint_path=path)


def test_semantic_tamper_fails_after_outer_integrity_is_recomputed(tmp_path):
    path = tmp_path / "semantic-tamper.json"
    app = _rich_app(path)
    app.save()
    envelope = json.loads(path.read_text(encoding="utf-8"))
    states = (
        envelope["authoritative_payload"]["components"]["open_close"]
        ["object_open_states"]
    )
    states[0]["state"] = "closed"
    _rewrite_with_valid_outer_integrity(path, envelope)

    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantPlayApplication.restore(checkpoint_path=path)


def test_legacy_int3_loads_and_next_save_upgrades_to_component_format(tmp_path):
    path = tmp_path / "legacy-int3.json"
    app = _rich_app(path)
    before = app.authoritative_digest()

    write_persistent_world_object_storage_checkpoint(
        state=app.storage_state,
        checkpoint_path=path,
        qualification_evidence=app.fixture.checkpoint_qualification,
    )
    legacy = json.loads(path.read_text(encoding="utf-8"))
    assert legacy["format_identity"] == OBJECT_STORAGE_CHECKPOINT_FORMAT_IDENTITY
    legacy_bytes = path.read_bytes()

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == before
    assert path.read_bytes() == legacy_bytes
    restored.save()

    upgraded = json.loads(path.read_text(encoding="utf-8"))
    assert upgraded["format_identity"] == COMPONENT_CHECKPOINT_FORMAT_IDENTITY


def test_new_and_legacy_readers_keep_distinct_format_identities(tmp_path):
    legacy_path = tmp_path / "legacy.json"
    component_path = tmp_path / "component.json"
    app = _rich_app(component_path)

    write_persistent_world_object_storage_checkpoint(
        state=app.storage_state,
        checkpoint_path=legacy_path,
        qualification_evidence=app.fixture.checkpoint_qualification,
    )
    with pytest.raises(PersistentWorldCheckpointFormatError):
        _restore_direct(legacy_path, app)

    app.save()
    with pytest.raises(PersistentWorldCheckpointFormatError):
        restore_persistent_world_object_storage_checkpoint(
            checkpoint_path=component_path,
            expected_campaign_id=app.fixture.campaign_id,
            expected_initial_open_states=app.fixture.initial_object_open_states,
            expected_initial_lit_states=app.fixture.initial_object_lit_states,
            expected_initial_representation_digest=(
                app.fixture.provenance.initial_state_digest
            ),
        )
