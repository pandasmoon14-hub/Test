"""Deterministic RNG interface skeleton — backend-owned, no global random state."""

from __future__ import annotations

import copy
import hashlib
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


class RNGInterfaceError(Exception):
    """Base error for RNG interface operations."""


class InvalidRNGInvocationError(RNGInterfaceError):
    """Raised when an RNG invocation fails validation."""


class InvalidRNGResultError(RNGInterfaceError):
    """Raised when an RNG result fails validation."""


@dataclass(frozen=True)
class RNGInvocation:
    """Immutable RNG invocation envelope. Backend-owned; no global random state."""

    rng_id: str
    seed: str
    purpose: str
    range_min: int
    range_max: int
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "rng_id": self.rng_id,
            "seed": self.seed,
            "purpose": self.purpose,
            "range_min": self.range_min,
            "range_max": self.range_max,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class RNGResult:
    """Immutable RNG result envelope. Backend-owned; no global random state."""

    rng_id: str
    seed: str
    value: int
    range_min: int
    range_max: int
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "rng_id": self.rng_id,
            "seed": self.seed,
            "value": self.value,
            "range_min": self.range_min,
            "range_max": self.range_max,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def _validate_non_empty_string(value: Any, name: str, error_cls: type[Exception]) -> None:
    if not isinstance(value, str) or not value.strip():
        raise error_cls(f"{name} must be a non-empty string")


def _validate_int_not_bool(value: Any, name: str, error_cls: type[Exception]) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise error_cls(f"{name} must be an integer")


def create_rng_invocation(
    rng_id: str,
    seed: str,
    purpose: str,
    range_min: int,
    range_max: int,
    metadata: Mapping[str, Any] | None = None,
) -> RNGInvocation:
    _validate_non_empty_string(rng_id, "rng_id", InvalidRNGInvocationError)
    _validate_non_empty_string(seed, "seed", InvalidRNGInvocationError)
    _validate_non_empty_string(purpose, "purpose", InvalidRNGInvocationError)
    _validate_int_not_bool(range_min, "range_min", InvalidRNGInvocationError)
    _validate_int_not_bool(range_max, "range_max", InvalidRNGInvocationError)

    if range_min > range_max:
        raise InvalidRNGInvocationError(
            f"range_min ({range_min}) must be <= range_max ({range_max})"
        )

    if metadata is None:
        safe_metadata: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(metadata, Mapping):
        raise InvalidRNGInvocationError("metadata must be a mapping")
    else:
        safe_metadata = MappingProxyType(copy.deepcopy(dict(metadata)))

    return RNGInvocation(
        rng_id=rng_id,
        seed=seed,
        purpose=purpose,
        range_min=range_min,
        range_max=range_max,
        metadata=safe_metadata,
    )


def create_rng_result(
    rng_id: str,
    seed: str,
    value: int,
    range_min: int,
    range_max: int,
    metadata: Mapping[str, Any] | None = None,
) -> RNGResult:
    _validate_non_empty_string(rng_id, "rng_id", InvalidRNGResultError)
    _validate_non_empty_string(seed, "seed", InvalidRNGResultError)
    _validate_int_not_bool(value, "value", InvalidRNGResultError)
    _validate_int_not_bool(range_min, "range_min", InvalidRNGResultError)
    _validate_int_not_bool(range_max, "range_max", InvalidRNGResultError)

    if range_min > range_max:
        raise InvalidRNGResultError(
            f"range_min ({range_min}) must be <= range_max ({range_max})"
        )

    if value < range_min or value > range_max:
        raise InvalidRNGResultError(
            f"value ({value}) must be within range [{range_min}, {range_max}]"
        )

    if metadata is None:
        safe_metadata: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(metadata, Mapping):
        raise InvalidRNGResultError("metadata must be a mapping")
    else:
        safe_metadata = MappingProxyType(copy.deepcopy(dict(metadata)))

    return RNGResult(
        rng_id=rng_id,
        seed=seed,
        value=value,
        range_min=range_min,
        range_max=range_max,
        metadata=safe_metadata,
    )


def validate_rng_invocation(obj: Any) -> bool:
    if not isinstance(obj, RNGInvocation):
        return False
    if not isinstance(obj.rng_id, str) or not obj.rng_id.strip():
        return False
    if not isinstance(obj.seed, str) or not obj.seed.strip():
        return False
    if not isinstance(obj.purpose, str) or not obj.purpose.strip():
        return False
    if not isinstance(obj.range_min, int) or isinstance(obj.range_min, bool):
        return False
    if not isinstance(obj.range_max, int) or isinstance(obj.range_max, bool):
        return False
    if obj.range_min > obj.range_max:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_rng_result(obj: Any) -> bool:
    if not isinstance(obj, RNGResult):
        return False
    if not isinstance(obj.rng_id, str) or not obj.rng_id.strip():
        return False
    if not isinstance(obj.seed, str) or not obj.seed.strip():
        return False
    if not isinstance(obj.value, int) or isinstance(obj.value, bool):
        return False
    if not isinstance(obj.range_min, int) or isinstance(obj.range_min, bool):
        return False
    if not isinstance(obj.range_max, int) or isinstance(obj.range_max, bool):
        return False
    if obj.range_min > obj.range_max:
        return False
    if obj.value < obj.range_min or obj.value > obj.range_max:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def deterministic_int(seed: str, range_min: int, range_max: int) -> int:
    if not isinstance(seed, str) or not seed.strip():
        raise InvalidRNGInvocationError("seed must be a non-empty string")
    if not isinstance(range_min, int) or isinstance(range_min, bool):
        raise InvalidRNGInvocationError("range_min must be an integer")
    if not isinstance(range_max, int) or isinstance(range_max, bool):
        raise InvalidRNGInvocationError("range_max must be an integer")
    if range_min > range_max:
        raise InvalidRNGInvocationError(
            f"range_min ({range_min}) must be <= range_max ({range_max})"
        )
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    raw = int.from_bytes(digest[:8], "big")
    span = range_max - range_min + 1
    return range_min + (raw % span)
