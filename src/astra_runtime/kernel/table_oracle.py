"""Table/oracle interface skeleton — backend-owned, deterministic, no content library."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


class TableOracleError(Exception):
    """Base error for table/oracle operations."""


class InvalidTableOracleInvocationError(TableOracleError):
    """Raised when a table/oracle invocation fails validation."""


class InvalidTableOracleResultError(TableOracleError):
    """Raised when a table/oracle result fails validation."""


@dataclass(frozen=True)
class TableOracleInvocation:
    """Immutable table/oracle invocation envelope. Backend-owned; no content library."""

    oracle_id: str
    table_id: str
    seed: str
    roll: int
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "oracle_id": self.oracle_id,
            "table_id": self.table_id,
            "seed": self.seed,
            "roll": self.roll,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class TableOracleResult:
    """Immutable table/oracle result envelope. Backend-owned; no content library."""

    oracle_id: str
    table_id: str
    roll: int
    selected_key: str
    selected_value: Any
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "oracle_id": self.oracle_id,
            "table_id": self.table_id,
            "roll": self.roll,
            "selected_key": self.selected_key,
            "selected_value": copy.deepcopy(self.selected_value),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def _validate_non_empty_string(value: Any, name: str, error_cls: type[Exception]) -> None:
    if not isinstance(value, str) or not value.strip():
        raise error_cls(f"{name} must be a non-empty string")


def _validate_int_not_bool(value: Any, name: str, error_cls: type[Exception]) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise error_cls(f"{name} must be an integer")


def create_table_oracle_invocation(
    oracle_id: str,
    table_id: str,
    seed: str,
    roll: int,
    metadata: Mapping[str, Any] | None = None,
) -> TableOracleInvocation:
    _validate_non_empty_string(oracle_id, "oracle_id", InvalidTableOracleInvocationError)
    _validate_non_empty_string(table_id, "table_id", InvalidTableOracleInvocationError)
    _validate_non_empty_string(seed, "seed", InvalidTableOracleInvocationError)
    _validate_int_not_bool(roll, "roll", InvalidTableOracleInvocationError)

    if metadata is None:
        safe_metadata: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(metadata, Mapping):
        raise InvalidTableOracleInvocationError("metadata must be a mapping")
    else:
        safe_metadata = MappingProxyType(copy.deepcopy(dict(metadata)))

    return TableOracleInvocation(
        oracle_id=oracle_id,
        table_id=table_id,
        seed=seed,
        roll=roll,
        metadata=safe_metadata,
    )


def create_table_oracle_result(
    oracle_id: str,
    table_id: str,
    roll: int,
    selected_key: str,
    selected_value: Any,
    metadata: Mapping[str, Any] | None = None,
) -> TableOracleResult:
    _validate_non_empty_string(oracle_id, "oracle_id", InvalidTableOracleResultError)
    _validate_non_empty_string(table_id, "table_id", InvalidTableOracleResultError)
    _validate_int_not_bool(roll, "roll", InvalidTableOracleResultError)
    _validate_non_empty_string(selected_key, "selected_key", InvalidTableOracleResultError)

    if metadata is None:
        safe_metadata: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(metadata, Mapping):
        raise InvalidTableOracleResultError("metadata must be a mapping")
    else:
        safe_metadata = MappingProxyType(copy.deepcopy(dict(metadata)))

    safe_value = copy.deepcopy(selected_value)

    return TableOracleResult(
        oracle_id=oracle_id,
        table_id=table_id,
        roll=roll,
        selected_key=selected_key,
        selected_value=safe_value,
        metadata=safe_metadata,
    )


def validate_table_oracle_invocation(obj: Any) -> bool:
    if not isinstance(obj, TableOracleInvocation):
        return False
    if not isinstance(obj.oracle_id, str) or not obj.oracle_id.strip():
        return False
    if not isinstance(obj.table_id, str) or not obj.table_id.strip():
        return False
    if not isinstance(obj.seed, str) or not obj.seed.strip():
        return False
    if not isinstance(obj.roll, int) or isinstance(obj.roll, bool):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_table_oracle_result(obj: Any) -> bool:
    if not isinstance(obj, TableOracleResult):
        return False
    if not isinstance(obj.oracle_id, str) or not obj.oracle_id.strip():
        return False
    if not isinstance(obj.table_id, str) or not obj.table_id.strip():
        return False
    if not isinstance(obj.roll, int) or isinstance(obj.roll, bool):
        return False
    if not isinstance(obj.selected_key, str) or not obj.selected_key.strip():
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def select_table_entry(table: Mapping[str, Any], roll: int) -> tuple[str, Any]:
    if not isinstance(table, Mapping):
        raise InvalidTableOracleInvocationError("table must be a mapping")
    if len(table) == 0:
        raise InvalidTableOracleInvocationError("table must not be empty")
    for key in table:
        if not isinstance(key, str):
            raise InvalidTableOracleInvocationError(
                f"table keys must be strings, got: {type(key).__name__}"
            )
    if not isinstance(roll, int) or isinstance(roll, bool):
        raise InvalidTableOracleInvocationError("roll must be an integer")
    sorted_keys = sorted(table.keys())
    index = roll % len(sorted_keys)
    selected_key = sorted_keys[index]
    selected_value = copy.deepcopy(table[selected_key])
    return selected_key, selected_value
