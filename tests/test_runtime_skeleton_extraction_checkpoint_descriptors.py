from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
    COMPONENT_CHECKPOINT_FORMAT_VERSION,
    COMP3_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    COMP3_COMPONENT_CHECKPOINT_FORMAT_VERSION,
    VSM6_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    VSM6_COMPONENT_CHECKPOINT_FORMAT_VERSION,
    WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION,
)
from astra_runtime.domain.persistent_world_vsm14_checkpoint import (
    VSM14_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    VSM14_COMPONENT_CHECKPOINT_FORMAT_VERSION,
)
from astra_runtime.runtime_skeleton_checkpoint_descriptors import (
    CHECKPOINT_FORMAT_DESCRIPTORS,
    COMPONENT_DESCRIPTORS,
    FORMAT_IDENTITY,
    checkpoint_component_ids_for_version,
    checkpoint_descriptor_for_version,
)


def test_frozen_descriptors_match_all_existing_checkpoint_versions_exactly() -> None:
    assert FORMAT_IDENTITY == COMPONENT_CHECKPOINT_FORMAT_IDENTITY
    expected = {
        COMPONENT_CHECKPOINT_FORMAT_VERSION: COMPONENT_CHECKPOINT_COMPONENT_KEYS,
        WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION: WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
        COMP3_COMPONENT_CHECKPOINT_FORMAT_VERSION: COMP3_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
        VSM6_COMPONENT_CHECKPOINT_FORMAT_VERSION: VSM6_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
        VSM14_COMPONENT_CHECKPOINT_FORMAT_VERSION: VSM14_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    }
    assert set(CHECKPOINT_FORMAT_DESCRIPTORS) == set(expected)
    for version, component_keys in expected.items():
        descriptor = checkpoint_descriptor_for_version(version)
        assert descriptor.format_identity == COMPONENT_CHECKPOINT_FORMAT_IDENTITY
        assert descriptor.format_version == version
        assert checkpoint_component_ids_for_version(version) == component_keys


def test_component_introduction_is_monotonic_and_exact() -> None:
    assert COMPONENT_DESCRIPTORS["placement"].introduced_in_version == 1
    assert COMPONENT_DESCRIPTORS["custody"].introduced_in_version == 1
    assert COMPONENT_DESCRIPTORS["open_close"].introduced_in_version == 1
    assert COMPONENT_DESCRIPTORS["lit_state"].introduced_in_version == 1
    assert COMPONENT_DESCRIPTORS["storage"].introduced_in_version == 1
    assert COMPONENT_DESCRIPTORS["logical_time"].introduced_in_version == 2
    assert COMPONENT_DESCRIPTORS["object_displacement"].introduced_in_version == 3
    assert COMPONENT_DESCRIPTORS["actor_object_handoff"].introduced_in_version == 4
    assert COMPONENT_DESCRIPTORS["follow_intent"].introduced_in_version == 5

    assert checkpoint_component_ids_for_version(1) < checkpoint_component_ids_for_version(2)
    assert checkpoint_component_ids_for_version(2) < checkpoint_component_ids_for_version(3)
    assert checkpoint_component_ids_for_version(3) < checkpoint_component_ids_for_version(4)
    assert checkpoint_component_ids_for_version(4) < checkpoint_component_ids_for_version(5)


def test_descriptors_are_immutable_and_not_dynamic_registry_state() -> None:
    descriptor = checkpoint_descriptor_for_version(5)
    with pytest.raises(FrozenInstanceError):
        descriptor.format_version = 6  # type: ignore[misc]
    with pytest.raises(TypeError):
        CHECKPOINT_FORMAT_DESCRIPTORS[6] = descriptor  # type: ignore[index]
    with pytest.raises(TypeError):
        COMPONENT_DESCRIPTORS["future"] = COMPONENT_DESCRIPTORS["placement"]  # type: ignore[index]


def test_unknown_checkpoint_version_fails_closed() -> None:
    with pytest.raises(ValueError, match="unsupported frozen checkpoint version"):
        checkpoint_descriptor_for_version(6)


def test_descriptor_layer_does_not_reassign_semantic_ownership() -> None:
    assert COMPONENT_DESCRIPTORS["logical_time"].semantic_owner_routes == ("AFQR-04",)
    assert "RT-010" in COMPONENT_DESCRIPTORS["custody"].semantic_owner_routes
    assert "AFQR-19" in COMPONENT_DESCRIPTORS["custody"].semantic_owner_routes
    assert "AFQR-01" in COMPONENT_DESCRIPTORS["custody"].semantic_owner_routes
    assert "AFQR-02" in COMPONENT_DESCRIPTORS["custody"].semantic_owner_routes
    assert COMPONENT_DESCRIPTORS["follow_intent"].semantic_owner_routes[0] == "AFQR-12"
    assert "AFQR-18" in COMPONENT_DESCRIPTORS["follow_intent"].semantic_owner_routes
    assert "AFQR-19" in COMPONENT_DESCRIPTORS["follow_intent"].semantic_owner_routes
    assert "AFQR-01" in COMPONENT_DESCRIPTORS["follow_intent"].semantic_owner_routes
    assert "AFQR-02" in COMPONENT_DESCRIPTORS["follow_intent"].semantic_owner_routes
