"""Compatibility exports for cut-over deterministic transition families.

RUNTIME-SKELETON-EXTRACTION-1E moved production retry/identity sequencing into
the shared deterministic lifecycle shell and moved each immutable capability
spec beside its existing semantic implementation. This module remains only so
1D-era imports continue to resolve. It owns no gameplay, state, persistence,
receipt, replay, qualification, opportunity, or semantic vocabulary.
"""

from astra_runtime.domain.persistent_world_actor_object_handoff import (
    HANDOFF_TRANSITION_CAPABILITY_SPEC,
    execute_persistent_world_actor_object_handoff as execute_handoff_via_transition_kernel,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    MOVEMENT_TRANSITION_CAPABILITY_SPEC,
    execute_persistent_world_movement as execute_movement_via_transition_kernel,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
    execute_persistent_world_object_displacement as execute_displacement_via_transition_kernel,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    LIT_TRANSITION_CAPABILITY_SPEC,
    execute_persistent_world_object_lit_state as execute_lit_via_transition_kernel,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
    execute_persistent_world_object_open_close as execute_open_close_via_transition_kernel,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    STORAGE_TRANSITION_CAPABILITY_SPEC,
    execute_persistent_world_object_storage as execute_storage_via_transition_kernel,
)

__all__ = [
    "MOVEMENT_TRANSITION_CAPABILITY_SPEC",
    "OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC",
    "LIT_TRANSITION_CAPABILITY_SPEC",
    "STORAGE_TRANSITION_CAPABILITY_SPEC",
    "DISPLACEMENT_TRANSITION_CAPABILITY_SPEC",
    "HANDOFF_TRANSITION_CAPABILITY_SPEC",
    "execute_movement_via_transition_kernel",
    "execute_open_close_via_transition_kernel",
    "execute_lit_via_transition_kernel",
    "execute_storage_via_transition_kernel",
    "execute_displacement_via_transition_kernel",
    "execute_handoff_via_transition_kernel",
]
