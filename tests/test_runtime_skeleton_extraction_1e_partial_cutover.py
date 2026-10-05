from __future__ import annotations

import inspect

from astra_runtime import runtime_skeleton_custody_adapter as custody_adapter
from astra_runtime import runtime_skeleton_existing_family_adapters as existing_adapter
from astra_runtime.domain import persistent_world_actor_object_handoff as handoff
from astra_runtime.domain import persistent_world_movement_integration as movement
from astra_runtime.domain import persistent_world_object_custody_transfer as custody
from astra_runtime.domain import persistent_world_object_displacement as displacement
from astra_runtime.domain import persistent_world_object_lit_state as lit_state
from astra_runtime.domain import persistent_world_object_open_close as open_close
from astra_runtime.domain import persistent_world_object_storage_transfer as storage


FAMILIES = (
    (
        movement,
        "execute_persistent_world_movement",
        "commit_prepared_persistent_world_movement",
        "MOVEMENT_TRANSITION_CAPABILITY_SPEC",
        "persistent_world_movement",
    ),
    (
        custody,
        "execute_persistent_world_object_custody",
        "commit_prepared_persistent_world_object_custody",
        "CUSTODY_TRANSITION_CAPABILITY_SPEC",
        "persistent_world_object_custody",
    ),
    (
        open_close,
        "execute_persistent_world_object_open_close",
        "commit_prepared_persistent_world_object_open_close",
        "OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC",
        "persistent_world_object_open_close",
    ),
    (
        lit_state,
        "execute_persistent_world_object_lit_state",
        "commit_prepared_persistent_world_object_lit_state",
        "LIT_TRANSITION_CAPABILITY_SPEC",
        "persistent_world_object_lit_state",
    ),
    (
        storage,
        "execute_persistent_world_object_storage",
        "commit_prepared_persistent_world_object_storage",
        "STORAGE_TRANSITION_CAPABILITY_SPEC",
        "persistent_world_object_storage",
    ),
    (
        displacement,
        "execute_persistent_world_object_displacement",
        "commit_prepared_persistent_world_object_displacement",
        "DISPLACEMENT_TRANSITION_CAPABILITY_SPEC",
        "persistent_world_object_displacement",
    ),
    (
        handoff,
        "execute_persistent_world_actor_object_handoff",
        "commit_prepared_persistent_world_actor_object_handoff",
        "HANDOFF_TRANSITION_CAPABILITY_SPEC",
        "persistent_world_actor_object_handoff",
    ),
)


def test_all_existing_transition_families_are_cut_over_to_shared_lifecycle() -> None:
    for module, execute_name, commit_name, spec_name, capability_id in FAMILIES:
        module_source = inspect.getsource(module)
        execute_source = inspect.getsource(getattr(module, execute_name))
        commit_source = inspect.getsource(getattr(module, commit_name))
        spec = getattr(module, spec_name)

        assert "execute_capability_transition" in execute_source
        assert "commit_prepared_capability_transition" in commit_source
        assert "find_committed_transition" not in module_source
        assert "command_fingerprint_matches" not in module_source
        assert "def _existing_transition" not in module_source
        assert spec.capability_id == capability_id


def test_extraction_adapters_are_compatibility_exports_only() -> None:
    for adapter in (custody_adapter, existing_adapter):
        source = inspect.getsource(adapter)
        assert "TransitionCapabilitySpec(" not in source
        assert "prepare_new_transition=" not in source
        assert "commit_new_transition=" not in source
        assert "def _prepare_" not in source
        assert "def _retry_" not in source
        assert "def _replay_" not in source


def test_compatibility_exports_are_identical_to_production_specs_and_executors() -> None:
    assert custody_adapter.CUSTODY_TRANSITION_CAPABILITY_SPEC is custody.CUSTODY_TRANSITION_CAPABILITY_SPEC
    assert custody_adapter.execute_custody_via_transition_kernel is custody.execute_persistent_world_object_custody

    mappings = (
        (
            existing_adapter.MOVEMENT_TRANSITION_CAPABILITY_SPEC,
            movement.MOVEMENT_TRANSITION_CAPABILITY_SPEC,
            existing_adapter.execute_movement_via_transition_kernel,
            movement.execute_persistent_world_movement,
        ),
        (
            existing_adapter.OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
            open_close.OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
            existing_adapter.execute_open_close_via_transition_kernel,
            open_close.execute_persistent_world_object_open_close,
        ),
        (
            existing_adapter.LIT_TRANSITION_CAPABILITY_SPEC,
            lit_state.LIT_TRANSITION_CAPABILITY_SPEC,
            existing_adapter.execute_lit_via_transition_kernel,
            lit_state.execute_persistent_world_object_lit_state,
        ),
        (
            existing_adapter.STORAGE_TRANSITION_CAPABILITY_SPEC,
            storage.STORAGE_TRANSITION_CAPABILITY_SPEC,
            existing_adapter.execute_storage_via_transition_kernel,
            storage.execute_persistent_world_object_storage,
        ),
        (
            existing_adapter.DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
            displacement.DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
            existing_adapter.execute_displacement_via_transition_kernel,
            displacement.execute_persistent_world_object_displacement,
        ),
        (
            existing_adapter.HANDOFF_TRANSITION_CAPABILITY_SPEC,
            handoff.HANDOFF_TRANSITION_CAPABILITY_SPEC,
            existing_adapter.execute_handoff_via_transition_kernel,
            handoff.execute_persistent_world_actor_object_handoff,
        ),
    )
    for adapter_spec, domain_spec, adapter_execute, domain_execute in mappings:
        assert adapter_spec is domain_spec
        assert adapter_execute is domain_execute


def test_existing_owner_routes_remain_distinct_after_cutover() -> None:
    assert movement.MOVEMENT_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "AFQR-02", "AFQR-03", "AFQR-18", "AFQR-19", "AFQR-01"
    )
    assert custody.CUSTODY_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "RT-010", "AFQR-19", "AFQR-01", "AFQR-18", "AFQR-02"
    )
    for spec in (
        open_close.OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
        lit_state.LIT_TRANSITION_CAPABILITY_SPEC,
        storage.STORAGE_TRANSITION_CAPABILITY_SPEC,
    ):
        assert spec.semantic_owners == ("RT-010", "AFQR-19", "AFQR-01", "AFQR-02")
    for spec in (
        displacement.DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
        handoff.HANDOFF_TRANSITION_CAPABILITY_SPEC,
    ):
        assert spec.semantic_owners == (
            "RT-010", "AFQR-18", "AFQR-19", "AFQR-01", "AFQR-02"
        )
