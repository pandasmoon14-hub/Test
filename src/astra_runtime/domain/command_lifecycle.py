"""Command lifecycle skeleton — backend-owned, immutable, no execution."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    validate_command_envelope,
)


COMMAND_LIFECYCLE_STAGES = frozenset({
    "received",
    "envelope_validated",
    "actor_bound",
    "visibility_checked",
    "legality_prechecked",
    "dependency_declared",
    "preview_requested",
    "confirmation_required",
    "accepted_for_transaction_planning",
    "rejected",
    "quarantined",
    "cancelled",
})

COMMAND_LIFECYCLE_TERMINAL_STAGES = frozenset({
    "accepted_for_transaction_planning",
    "rejected",
    "quarantined",
    "cancelled",
})

_ALLOWED_STATUSES = frozenset({
    "in_progress",
    "accepted",
    "rejected",
    "quarantined",
    "cancelled",
})


class CommandLifecycleError(Exception):
    """Base error for command lifecycle operations."""


class InvalidCommandLifecycleStageError(CommandLifecycleError):
    """Raised when a lifecycle stage is not recognized."""


class InvalidCommandLifecycleResultError(CommandLifecycleError):
    """Raised when a lifecycle result fails validation."""


def _validate_non_empty_string(
    value: Any, name: str, error_cls: type[Exception],
) -> None:
    if not isinstance(value, str) or not value.strip():
        raise error_cls(f"{name} must be a non-empty string")


def _safe_metadata(
    metadata: Mapping[str, Any] | None, error_cls: type[Exception],
) -> Mapping[str, Any]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    return MappingProxyType(copy.deepcopy(dict(metadata)))


@dataclass(frozen=True)
class CommandLifecycleStage:
    """Immutable lifecycle stage descriptor."""

    stage: str
    description: str
    terminal: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "description": self.description,
            "terminal": self.terminal,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class CommandLifecycleResult:
    """Immutable command lifecycle result. Backend-owned; no execution, no state mutation."""

    lifecycle_id: str
    command_id: str
    stage: str
    status: str
    validation_id: str | None
    requires_confirmation: bool
    downstream_dependencies: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "lifecycle_id": self.lifecycle_id,
            "command_id": self.command_id,
            "stage": self.stage,
            "status": self.status,
            "validation_id": self.validation_id,
            "requires_confirmation": self.requires_confirmation,
            "downstream_dependencies": list(self.downstream_dependencies),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_command_lifecycle_result(
    lifecycle_id: str,
    command_id: str,
    stage: str,
    status: str,
    validation_id: str | None = None,
    requires_confirmation: bool = False,
    downstream_dependencies: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CommandLifecycleResult:
    _validate_non_empty_string(
        lifecycle_id, "lifecycle_id", InvalidCommandLifecycleResultError,
    )
    _validate_non_empty_string(
        command_id, "command_id", InvalidCommandLifecycleResultError,
    )
    if stage not in COMMAND_LIFECYCLE_STAGES:
        raise InvalidCommandLifecycleStageError(
            f"stage must be one of {sorted(COMMAND_LIFECYCLE_STAGES)}, got: {stage!r}"
        )
    if status not in _ALLOWED_STATUSES:
        raise InvalidCommandLifecycleResultError(
            f"status must be one of {sorted(_ALLOWED_STATUSES)}, got: {status!r}"
        )
    if validation_id is not None:
        _validate_non_empty_string(
            validation_id, "validation_id", InvalidCommandLifecycleResultError,
        )
    if not isinstance(requires_confirmation, bool):
        raise InvalidCommandLifecycleResultError(
            "requires_confirmation must be a bool"
        )

    if downstream_dependencies is None:
        safe_deps: tuple[str, ...] = ()
    elif isinstance(downstream_dependencies, str):
        raise InvalidCommandLifecycleResultError(
            "downstream_dependencies must not be a string"
        )
    elif not isinstance(downstream_dependencies, Sequence):
        raise InvalidCommandLifecycleResultError(
            "downstream_dependencies must be a sequence"
        )
    else:
        for i, dep in enumerate(downstream_dependencies):
            if not isinstance(dep, str) or not dep.strip():
                raise InvalidCommandLifecycleResultError(
                    f"downstream_dependencies[{i}] must be a non-empty string"
                )
        safe_deps = tuple(downstream_dependencies)

    safe_meta = _safe_metadata(metadata, InvalidCommandLifecycleResultError)

    return CommandLifecycleResult(
        lifecycle_id=lifecycle_id,
        command_id=command_id,
        stage=stage,
        status=status,
        validation_id=validation_id,
        requires_confirmation=requires_confirmation,
        downstream_dependencies=safe_deps,
        metadata=safe_meta,
    )


def validate_command_lifecycle_result(obj: Any) -> bool:
    if not isinstance(obj, CommandLifecycleResult):
        return False
    if not isinstance(obj.lifecycle_id, str) or not obj.lifecycle_id.strip():
        return False
    if not isinstance(obj.command_id, str) or not obj.command_id.strip():
        return False
    if obj.stage not in COMMAND_LIFECYCLE_STAGES:
        return False
    if obj.status not in _ALLOWED_STATUSES:
        return False
    if obj.validation_id is not None:
        if not isinstance(obj.validation_id, str) or not obj.validation_id.strip():
            return False
    if not isinstance(obj.requires_confirmation, bool):
        return False
    if not isinstance(obj.downstream_dependencies, tuple):
        return False
    for dep in obj.downstream_dependencies:
        if not isinstance(dep, str) or not dep.strip():
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def evaluate_command_lifecycle(
    lifecycle_id: str,
    command: CommandEnvelope,
    *,
    stage: str = "received",
    status: str = "in_progress",
    validation_id: str | None = None,
    requires_confirmation: bool = False,
    downstream_dependencies: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CommandLifecycleResult:
    if not validate_command_envelope(command):
        raise CommandLifecycleError(
            "command must be a valid CommandEnvelope"
        )
    return create_command_lifecycle_result(
        lifecycle_id=lifecycle_id,
        command_id=command.command_id,
        stage=stage,
        status=status,
        validation_id=validation_id,
        requires_confirmation=requires_confirmation,
        downstream_dependencies=downstream_dependencies,
        metadata=metadata,
    )


class CommandLifecycleService:
    """Stateless wrapper around evaluate_command_lifecycle."""

    def evaluate(
        self,
        lifecycle_id: str,
        command: CommandEnvelope,
        *,
        stage: str = "received",
        status: str = "in_progress",
        validation_id: str | None = None,
        requires_confirmation: bool = False,
        downstream_dependencies: Sequence[str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> CommandLifecycleResult:
        return evaluate_command_lifecycle(
            lifecycle_id=lifecycle_id,
            command=command,
            stage=stage,
            status=status,
            validation_id=validation_id,
            requires_confirmation=requires_confirmation,
            downstream_dependencies=downstream_dependencies,
            metadata=metadata,
        )
