"""Compatibility exports for the cut-over R4-E custody lifecycle.

RUNTIME-SKELETON-EXTRACTION-1E moved production retry/identity sequencing into
the shared deterministic lifecycle shell while preserving custody semantics in
the custody owner module. This module remains only so extraction-era imports
continue to resolve; it owns no gameplay, state, persistence, or vocabulary.
"""

from astra_runtime.domain.persistent_world_object_custody_transfer import (
    CUSTODY_TRANSITION_CAPABILITY_SPEC,
    execute_persistent_world_object_custody as execute_custody_via_transition_kernel,
)

__all__ = [
    "CUSTODY_TRANSITION_CAPABILITY_SPEC",
    "execute_custody_via_transition_kernel",
]
