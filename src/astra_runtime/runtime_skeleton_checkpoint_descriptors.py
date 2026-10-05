"""Static immutable descriptors for committed Myravant checkpoint formats.

This module records component membership for componentized checkpoint versions
1 through 5. It does not own checkpoint serialization, restore semantics,
migration, state ownership, or format evolution. Versions 1 through 4 remain
frozen historical contracts; version 5 appends the VSM-14 AFQR-12 follow-intent
component after explicit owner authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, kw_only=True)
class CheckpointComponentDescriptor:
    component_id: str
    introduced_in_version: int
    semantic_owner_routes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.component_id or not isinstance(self.component_id, str):
            raise ValueError("component_id must be a non-empty string")
        if type(self.introduced_in_version) is not int or self.introduced_in_version < 1:
            raise ValueError("introduced_in_version must be a positive integer")
        if (
            not isinstance(self.semantic_owner_routes, tuple)
            or not self.semantic_owner_routes
            or any(not isinstance(x, str) or not x for x in self.semantic_owner_routes)
        ):
            raise ValueError("semantic_owner_routes must be a non-empty tuple")


@dataclass(frozen=True, kw_only=True)
class CheckpointFormatDescriptor:
    format_identity: str
    format_version: int
    component_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.format_identity or not isinstance(self.format_identity, str):
            raise ValueError("format_identity must be a non-empty string")
        if type(self.format_version) is not int or self.format_version < 1:
            raise ValueError("format_version must be a positive integer")
        if (
            not isinstance(self.component_ids, tuple)
            or not self.component_ids
            or len(self.component_ids) != len(set(self.component_ids))
            or any(not isinstance(x, str) or not x for x in self.component_ids)
        ):
            raise ValueError("component_ids must be unique non-empty strings")


FORMAT_IDENTITY = "myravant.componentized.persistent_world_checkpoint"

_COMPONENTS = (
    CheckpointComponentDescriptor(
        component_id="placement",
        introduced_in_version=1,
        semantic_owner_routes=("AFQR-18", "R4-C", "RT-010"),
    ),
    CheckpointComponentDescriptor(
        component_id="custody",
        introduced_in_version=1,
        semantic_owner_routes=("RT-010", "AFQR-19", "AFQR-01", "AFQR-02"),
    ),
    CheckpointComponentDescriptor(
        component_id="open_close",
        introduced_in_version=1,
        semantic_owner_routes=("RT-010", "AFQR-19", "AFQR-01", "AFQR-02"),
    ),
    CheckpointComponentDescriptor(
        component_id="lit_state",
        introduced_in_version=1,
        semantic_owner_routes=("RT-010", "AFQR-19", "AFQR-01", "AFQR-02"),
    ),
    CheckpointComponentDescriptor(
        component_id="storage",
        introduced_in_version=1,
        semantic_owner_routes=("RT-010", "AFQR-19", "AFQR-01", "AFQR-02"),
    ),
    CheckpointComponentDescriptor(
        component_id="logical_time",
        introduced_in_version=2,
        semantic_owner_routes=("AFQR-04",),
    ),
    CheckpointComponentDescriptor(
        component_id="object_displacement",
        introduced_in_version=3,
        semantic_owner_routes=("RT-010", "AFQR-18", "AFQR-19", "AFQR-01"),
    ),
    CheckpointComponentDescriptor(
        component_id="actor_object_handoff",
        introduced_in_version=4,
        semantic_owner_routes=("RT-010", "AFQR-18", "AFQR-19", "AFQR-01"),
    ),
    CheckpointComponentDescriptor(
        component_id="follow_intent",
        introduced_in_version=5,
        semantic_owner_routes=(
            "AFQR-12",
            "AFQR-18",
            "AFQR-19",
            "AFQR-01",
            "AFQR-02",
        ),
    ),
)

COMPONENT_DESCRIPTORS: Mapping[str, CheckpointComponentDescriptor] = MappingProxyType(
    {item.component_id: item for item in _COMPONENTS}
)


def _members(version: int) -> tuple[str, ...]:
    return tuple(
        item.component_id
        for item in _COMPONENTS
        if item.introduced_in_version <= version
    )


_FORMATS = tuple(
    CheckpointFormatDescriptor(
        format_identity=FORMAT_IDENTITY,
        format_version=version,
        component_ids=_members(version),
    )
    for version in (1, 2, 3, 4, 5)
)

CHECKPOINT_FORMAT_DESCRIPTORS: Mapping[int, CheckpointFormatDescriptor] = MappingProxyType(
    {item.format_version: item for item in _FORMATS}
)


def checkpoint_descriptor_for_version(version: int) -> CheckpointFormatDescriptor:
    try:
        return CHECKPOINT_FORMAT_DESCRIPTORS[version]
    except KeyError as exc:
        raise ValueError(f"unsupported frozen checkpoint version: {version!r}") from exc


def checkpoint_component_ids_for_version(version: int) -> frozenset[str]:
    return frozenset(checkpoint_descriptor_for_version(version).component_ids)
