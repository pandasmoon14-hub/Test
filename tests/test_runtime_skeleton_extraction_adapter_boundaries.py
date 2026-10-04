from __future__ import annotations

import inspect

import astra_runtime.runtime_skeleton_existing_family_adapters as adapters
from astra_runtime.domain._deterministic_transition_support import TransitionCapabilitySpec


def test_existing_family_adapters_are_specs_not_semantic_registry() -> None:
    specs = (
        adapters.MOVEMENT_TRANSITION_CAPABILITY_SPEC,
        adapters.OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
        adapters.LIT_TRANSITION_CAPABILITY_SPEC,
        adapters.STORAGE_TRANSITION_CAPABILITY_SPEC,
        adapters.DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
        adapters.HANDOFF_TRANSITION_CAPABILITY_SPEC,
    )
    assert all(isinstance(spec, TransitionCapabilitySpec) for spec in specs)
    assert len({spec.capability_id for spec in specs}) == len(specs)
    assert all(spec.semantic_owners for spec in specs)


def test_adapter_module_does_not_define_gameplay_vocabulary_or_checkpoint_format() -> None:
    source = inspect.getsource(adapters)
    assert "class PersistentWorld" not in source
    assert "format_version" not in source
    assert "component_ids" not in source
    assert "dynamic registry" not in source.lower()
