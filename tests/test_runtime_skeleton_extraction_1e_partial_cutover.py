from __future__ import annotations

import inspect

from astra_runtime.domain import persistent_world_movement_integration as movement
from astra_runtime.domain import persistent_world_object_custody_transfer as custody
from astra_runtime.domain import persistent_world_object_open_close as open_close
from astra_runtime import runtime_skeleton_custody_adapter as custody_adapter


def test_cut_over_families_use_shared_lifecycle_without_local_retry_lookup() -> None:
    for module, execute_name, commit_name in (
        (movement, "execute_persistent_world_movement", "commit_prepared_persistent_world_movement"),
        (custody, "execute_persistent_world_object_custody", "commit_prepared_persistent_world_object_custody"),
        (open_close, "execute_persistent_world_object_open_close", "commit_prepared_persistent_world_object_open_close"),
    ):
        execute_source = inspect.getsource(getattr(module, execute_name))
        commit_source = inspect.getsource(getattr(module, commit_name))
        assert "execute_capability_transition" in execute_source
        assert "commit_prepared_capability_transition" in commit_source
        assert "find_committed_transition" not in inspect.getsource(module)
        assert "def _existing_transition" not in inspect.getsource(module)


def test_custody_extraction_adapter_is_compatibility_export_only() -> None:
    source = inspect.getsource(custody_adapter)
    assert "TransitionCapabilitySpec(" not in source
    assert "prepare_new_transition=" not in source
    assert custody_adapter.CUSTODY_TRANSITION_CAPABILITY_SPEC is custody.CUSTODY_TRANSITION_CAPABILITY_SPEC
    assert custody_adapter.execute_custody_via_transition_kernel is custody.execute_persistent_world_object_custody
