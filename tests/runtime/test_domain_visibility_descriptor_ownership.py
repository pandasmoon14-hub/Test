"""Regression tests for the two distinct state visibility contracts.

The state-store descriptor and the RT-001H owner-interface descriptor are
separate, owner-scoped contracts. Tests must import them from their defining
modules rather than treating the generic package-level name as interchangeable.
"""

from __future__ import annotations

import inspect

from astra_runtime.domain.state_owner_interface_contract_skeleton import (
    StateVisibilityDescriptor as StateOwnerVisibilityDescriptor,
    create_state_visibility_descriptor as create_state_owner_visibility_descriptor,
    validate_state_visibility_descriptor as validate_state_owner_visibility_descriptor,
)
from astra_runtime.domain.state_store import (
    StateVisibilityDescriptor as StateStoreVisibilityDescriptor,
    create_state_visibility_descriptor as create_state_store_visibility_descriptor,
    validate_state_visibility_descriptor as validate_state_store_visibility_descriptor,
)


def test_visibility_descriptor_types_are_not_interchangeable() -> None:
    assert StateStoreVisibilityDescriptor is not StateOwnerVisibilityDescriptor


def test_state_store_visibility_contract_owns_hidden_info_safe() -> None:
    parameters = inspect.signature(create_state_store_visibility_descriptor).parameters
    assert "hidden_info_safe" in parameters
    descriptor = create_state_store_visibility_descriptor(
        visibility_id="vis-state-store",
        visibility_tier="backend_hidden",
        hidden_info_safe=True,
        player_visible=False,
    )
    assert validate_state_store_visibility_descriptor(descriptor) is True
    assert isinstance(descriptor.hidden_info_safe, bool)


def test_state_owner_visibility_contract_uses_policy_not_safety_self_certification() -> None:
    parameters = inspect.signature(create_state_owner_visibility_descriptor).parameters
    assert "hidden_info_safe" not in parameters
    descriptor = create_state_owner_visibility_descriptor(
        visibility_id="vis-state-owner",
        visibility_tier="hidden",
        hidden_information_policy="deny_visible_detail",
        player_visible_allowed=False,
        actor_visible_allowed=False,
        backend_visible_allowed=False,
        redaction_required=True,
    )
    assert validate_state_owner_visibility_descriptor(descriptor) is True
    assert not hasattr(descriptor, "hidden_info_safe")
