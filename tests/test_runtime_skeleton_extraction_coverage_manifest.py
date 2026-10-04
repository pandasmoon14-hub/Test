from __future__ import annotations

from astra_runtime.runtime_skeleton_checkpoint_descriptors import (
    CHECKPOINT_FORMAT_DESCRIPTORS,
)
from astra_runtime.runtime_skeleton_custody_adapter import (
    CUSTODY_TRANSITION_CAPABILITY_SPEC,
)
from astra_runtime.runtime_skeleton_existing_family_adapters import (
    DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
    HANDOFF_TRANSITION_CAPABILITY_SPEC,
    LIT_TRANSITION_CAPABILITY_SPEC,
    MOVEMENT_TRANSITION_CAPABILITY_SPEC,
    OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
    STORAGE_TRANSITION_CAPABILITY_SPEC,
)


EXPECTED_EXTRACTED_CAPABILITY_IDS = frozenset(
    {
        "persistent_world_movement",
        "persistent_world_object_custody",
        "persistent_world_object_open_close",
        "persistent_world_object_lit_state",
        "persistent_world_object_storage",
        "persistent_world_object_displacement",
        "persistent_world_actor_object_handoff",
    }
)


def test_all_existing_transition_families_are_explicitly_covered() -> None:
    specs = (
        MOVEMENT_TRANSITION_CAPABILITY_SPEC,
        CUSTODY_TRANSITION_CAPABILITY_SPEC,
        OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
        LIT_TRANSITION_CAPABILITY_SPEC,
        STORAGE_TRANSITION_CAPABILITY_SPEC,
        DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
        HANDOFF_TRANSITION_CAPABILITY_SPEC,
    )
    assert frozenset(spec.capability_id for spec in specs) == EXPECTED_EXTRACTED_CAPABILITY_IDS
    assert len({spec.capability_id for spec in specs}) == 7
    assert all(spec.semantic_owners for spec in specs)


def test_all_existing_componentized_checkpoint_versions_remain_frozen() -> None:
    assert frozenset(CHECKPOINT_FORMAT_DESCRIPTORS) == frozenset({1, 2, 3, 4})
    assert CHECKPOINT_FORMAT_DESCRIPTORS[1].component_ids == (
        "placement",
        "custody",
        "open_close",
        "lit_state",
        "storage",
    )
    assert CHECKPOINT_FORMAT_DESCRIPTORS[4].component_ids[-3:] == (
        "logical_time",
        "object_displacement",
        "actor_object_handoff",
    )
