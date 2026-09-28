"""RUNTIME-WORLD-STATE-COMPOSITION-1 regression tests."""

from __future__ import annotations

from dataclasses import fields

from astra_runtime.domain.persistent_world_component_checkpoint import (
    canonical_serialize_persistent_world_component_checkpoint_envelope,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementRuntimeState,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyRuntimeState,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    PersistentWorldObjectLitRuntimeState,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenCloseRuntimeState,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    PersistentWorldObjectStorageRuntimeState,
    digest_persistent_world_object_storage_runtime_state,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    PersistentWorldRuntimeComposition,
    compose_persistent_world_custody_state,
    compose_persistent_world_lit_state,
    compose_persistent_world_open_close_state,
    compose_persistent_world_storage_state,
    create_persistent_world_runtime_composition_from_storage_state,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication


def _root_snapshot(state: PersistentWorldRuntimeComposition) -> dict[str, object]:
    return {
        "movement_state": state.movement_state,
        "committed_custody_transitions": state.committed_custody_transitions,
        "object_open_states": state.object_open_states,
        "committed_object_state_transitions": (
            state.committed_object_state_transitions
        ),
        "object_lit_states": state.object_lit_states,
        "committed_object_lit_transitions": (
            state.committed_object_lit_transitions
        ),
        "committed_storage_transitions": state.committed_storage_transitions,
    }


def test_runtime_composition_has_only_flat_current_state_fields():
    names = {field.name for field in fields(PersistentWorldRuntimeComposition)}

    assert names == {
        "movement_state",
        "committed_custody_transitions",
        "object_open_states",
        "committed_object_state_transitions",
        "object_lit_states",
        "committed_object_lit_transitions",
        "committed_storage_transitions",
    }
    assert "custody_state" not in names
    assert "open_close_state" not in names
    assert "lit_state" not in names
    assert "storage_state" not in names


def test_application_stores_flat_root_and_exposes_legacy_execution_views():
    app = MyravantPlayApplication.new()

    assert isinstance(app.runtime_state, PersistentWorldRuntimeComposition)
    assert isinstance(app.state, PersistentWorldMovementRuntimeState)
    assert isinstance(app.custody_state, PersistentWorldObjectCustodyRuntimeState)
    assert isinstance(app.object_state, PersistentWorldObjectOpenCloseRuntimeState)
    assert isinstance(app.lit_state, PersistentWorldObjectLitRuntimeState)
    assert isinstance(app.storage_state, PersistentWorldObjectStorageRuntimeState)

    assert app.state is app.runtime_state.movement_state
    assert app.custody_state.movement_state == app.runtime_state.movement_state
    assert app.object_state.object_open_states == app.runtime_state.object_open_states
    assert app.lit_state.object_lit_states == app.runtime_state.object_lit_states
    assert (
        app.storage_state.committed_storage_transitions
        == app.runtime_state.committed_storage_transitions
    )


def test_nested_storage_state_round_trips_through_flat_composition_exactly():
    app = MyravantPlayApplication.new()
    app.light_object("lantern")
    app.pickup("lantern")
    app.move("south")
    app.open_object("tool chest")

    nested = app.storage_state
    flat = create_persistent_world_runtime_composition_from_storage_state(nested)
    projected = compose_persistent_world_storage_state(flat)

    assert projected == nested
    assert compose_persistent_world_lit_state(flat) == nested.lit_state
    assert (
        compose_persistent_world_open_close_state(flat)
        == nested.lit_state.open_close_state
    )
    assert (
        compose_persistent_world_custody_state(flat)
        == nested.lit_state.open_close_state.custody_state
    )


def test_movement_updates_only_movement_component_at_composition_root():
    app = MyravantPlayApplication.new()
    before = _root_snapshot(app.runtime_state)

    result = app.move("south")

    assert result.result_type == "movement_committed"
    after = _root_snapshot(app.runtime_state)
    assert after["movement_state"] != before["movement_state"]
    for key in (
        "committed_custody_transitions",
        "object_open_states",
        "committed_object_state_transitions",
        "object_lit_states",
        "committed_object_lit_transitions",
        "committed_storage_transitions",
    ):
        assert after[key] == before[key]


def test_custody_updates_placement_and_custody_without_rewrapping_owner_state():
    app = MyravantPlayApplication.new()
    before = _root_snapshot(app.runtime_state)

    result = app.pickup("lantern")

    assert result.result_type == "custody_committed"
    after = _root_snapshot(app.runtime_state)
    assert after["movement_state"] != before["movement_state"]
    assert len(after["committed_custody_transitions"]) == 1
    assert after["object_open_states"] == before["object_open_states"]
    assert (
        after["committed_object_state_transitions"]
        == before["committed_object_state_transitions"]
    )
    assert after["object_lit_states"] == before["object_lit_states"]
    assert (
        after["committed_object_lit_transitions"]
        == before["committed_object_lit_transitions"]
    )
    assert (
        after["committed_storage_transitions"]
        == before["committed_storage_transitions"]
    )


def test_open_close_updates_only_open_close_owned_material():
    app = MyravantPlayApplication.new()
    before = _root_snapshot(app.runtime_state)

    result = app.open_object("tool chest")

    assert result.result_type == "object_state_committed"
    after = _root_snapshot(app.runtime_state)
    assert after["movement_state"] == before["movement_state"]
    assert (
        after["committed_custody_transitions"]
        == before["committed_custody_transitions"]
    )
    assert after["object_open_states"] != before["object_open_states"]
    assert len(after["committed_object_state_transitions"]) == 1
    assert after["object_lit_states"] == before["object_lit_states"]
    assert (
        after["committed_object_lit_transitions"]
        == before["committed_object_lit_transitions"]
    )
    assert (
        after["committed_storage_transitions"]
        == before["committed_storage_transitions"]
    )


def test_lit_state_updates_only_lit_owned_material():
    app = MyravantPlayApplication.new()
    before = _root_snapshot(app.runtime_state)

    result = app.light_object("lantern")

    assert result.result_type == "object_lit_state_committed"
    after = _root_snapshot(app.runtime_state)
    assert after["movement_state"] == before["movement_state"]
    assert (
        after["committed_custody_transitions"]
        == before["committed_custody_transitions"]
    )
    assert after["object_open_states"] == before["object_open_states"]
    assert (
        after["committed_object_state_transitions"]
        == before["committed_object_state_transitions"]
    )
    assert after["object_lit_states"] != before["object_lit_states"]
    assert len(after["committed_object_lit_transitions"]) == 1
    assert (
        after["committed_storage_transitions"]
        == before["committed_storage_transitions"]
    )


def test_authoritative_digest_remains_existing_storage_composite_digest():
    app = MyravantPlayApplication.new()
    app.light_object("lantern")
    app.pickup("lantern")
    app.move("south")
    app.open_object("tool chest")

    assert app.authoritative_digest() == (
        digest_persistent_world_object_storage_runtime_state(app.storage_state)
    )


def test_component_checkpoint_bytes_are_stable_through_flat_projection():
    app = MyravantPlayApplication.new()
    app.light_object("lantern")
    app.pickup("lantern")
    app.move("south")
    app.open_object("tool chest")

    original_nested = app.storage_state
    flat = create_persistent_world_runtime_composition_from_storage_state(
        original_nested
    )
    projected_nested = compose_persistent_world_storage_state(flat)

    original_bytes = (
        canonical_serialize_persistent_world_component_checkpoint_envelope(
            state=original_nested,
            qualification_evidence=app.fixture.checkpoint_qualification,
        )
    )
    projected_bytes = (
        canonical_serialize_persistent_world_component_checkpoint_envelope(
            state=projected_nested,
            qualification_evidence=app.fixture.checkpoint_qualification,
        )
    )

    assert projected_nested == original_nested
    assert projected_bytes == original_bytes


def test_save_restore_save_preserves_component_checkpoint_bytes(tmp_path):
    path = tmp_path / "composition.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    app.light_object("lantern")
    app.pickup("lantern")
    app.move("south")
    app.open_object("tool chest")

    before_digest = app.authoritative_digest()
    app.save()
    first = path.read_bytes()

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert isinstance(restored.runtime_state, PersistentWorldRuntimeComposition)
    assert restored.authoritative_digest() == before_digest

    restored.save()
    second = path.read_bytes()
    assert second == first


def test_legacy_storage_state_constructor_input_is_immediately_flattened():
    source = MyravantPlayApplication.new()
    source.light_object("lantern")
    nested = source.storage_state

    app = MyravantPlayApplication(
        fixture=source.fixture,
        storage_state=nested,
    )

    assert isinstance(app.runtime_state, PersistentWorldRuntimeComposition)
    assert app.storage_state == nested
    assert app.authoritative_digest() == source.authoritative_digest()
