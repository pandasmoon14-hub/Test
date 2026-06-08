"""Action legality skeleton — backend-owned, immutable, no domain rules."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    validate_command_envelope,
)
from astra_runtime.domain.command_lifecycle import COMMAND_LIFECYCLE_STAGES


ACTION_LEGALITY_DECISIONS = frozenset({
    "legal",
    "illegal",
    "requires_confirmation",
    "requires_more_information",
    "blocked_by_hidden_information",
    "blocked_by_missing_actor",
    "blocked_by_invalid_target",
    "blocked_by_resource_precheck",
    "blocked_by_timing",
    "blocked_by_scope",
    "quarantined_for_validation",
    "unsupported_command_type",
})

ACTION_LEGALITY_BLOCKING_DECISIONS = frozenset({
    "illegal",
    "blocked_by_hidden_information",
    "blocked_by_missing_actor",
    "blocked_by_invalid_target",
    "blocked_by_resource_precheck",
    "blocked_by_timing",
    "blocked_by_scope",
    "quarantined_for_validation",
    "unsupported_command_type",
})

_ALLOWED_DEPENDENCY_TYPES = frozenset({
    "state_projection",
    "transaction_lifecycle",
    "validation_integration",
    "resource_math",
    "combat_resolution",
    "ability_resolution",
    "inventory_service",
    "mission_service",
    "social_faction_service",
    "generated_content_provenance",
    "context_projection",
    "model_evaluation",
    "live_play_gate",
})

_MAY_PROCEED_DECISIONS = frozenset({"legal", "requires_confirmation"})


class ActionLegalityError(Exception):
    """Base error for action legality operations."""


class InvalidActionLegalityDecisionError(ActionLegalityError):
    """Raised when a legality decision is not recognized."""


class InvalidActionLegalityResultError(ActionLegalityError):
    """Raised when a legality result fails validation."""


class InvalidDependencyDeclarationError(ActionLegalityError):
    """Raised when a dependency declaration is invalid."""


class InvalidLegalityBlockReasonError(ActionLegalityError):
    """Raised when a legality block reason is invalid."""


class InvalidConfirmationRequirementError(ActionLegalityError):
    """Raised when a confirmation requirement is invalid."""


class InvalidCommandQuarantineResultError(ActionLegalityError):
    """Raised when a command quarantine result is invalid."""


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
class ActionLegalityDecision:
    """Immutable legality decision descriptor."""

    decision: str
    player_visible: bool
    hidden_info_safe: bool
    may_proceed_to_preview: bool
    requires_validation_issue: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "player_visible": self.player_visible,
            "hidden_info_safe": self.hidden_info_safe,
            "may_proceed_to_preview": self.may_proceed_to_preview,
            "requires_validation_issue": self.requires_validation_issue,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class DependencyDeclaration:
    """Immutable dependency declaration."""

    dependency_id: str
    dependency_type: str
    required: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "dependency_id": self.dependency_id,
            "dependency_type": self.dependency_type,
            "required": self.required,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_dependency_declaration(
    dependency_id: str,
    dependency_type: str,
    required: bool,
    metadata: Mapping[str, Any] | None = None,
) -> DependencyDeclaration:
    _validate_non_empty_string(
        dependency_id, "dependency_id", InvalidDependencyDeclarationError,
    )
    if dependency_type not in _ALLOWED_DEPENDENCY_TYPES:
        raise InvalidDependencyDeclarationError(
            f"dependency_type must be one of {sorted(_ALLOWED_DEPENDENCY_TYPES)}, got: {dependency_type!r}"
        )
    if not isinstance(required, bool):
        raise InvalidDependencyDeclarationError("required must be a bool")
    safe_meta = _safe_metadata(metadata, InvalidDependencyDeclarationError)
    return DependencyDeclaration(
        dependency_id=dependency_id,
        dependency_type=dependency_type,
        required=required,
        metadata=safe_meta,
    )


@dataclass(frozen=True)
class LegalityBlockReason:
    """Immutable legality block reason."""

    reason_id: str
    reason_code: str
    message: str
    player_visible: bool
    hidden_info_safe: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "reason_id": self.reason_id,
            "reason_code": self.reason_code,
            "message": self.message,
            "player_visible": self.player_visible,
            "hidden_info_safe": self.hidden_info_safe,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_legality_block_reason(
    reason_id: str,
    reason_code: str,
    message: str,
    player_visible: bool,
    hidden_info_safe: bool,
    metadata: Mapping[str, Any] | None = None,
) -> LegalityBlockReason:
    _validate_non_empty_string(reason_id, "reason_id", InvalidLegalityBlockReasonError)
    _validate_non_empty_string(
        reason_code, "reason_code", InvalidLegalityBlockReasonError,
    )
    _validate_non_empty_string(message, "message", InvalidLegalityBlockReasonError)
    if not isinstance(player_visible, bool):
        raise InvalidLegalityBlockReasonError("player_visible must be a bool")
    if not isinstance(hidden_info_safe, bool):
        raise InvalidLegalityBlockReasonError("hidden_info_safe must be a bool")
    safe_meta = _safe_metadata(metadata, InvalidLegalityBlockReasonError)
    return LegalityBlockReason(
        reason_id=reason_id,
        reason_code=reason_code,
        message=message,
        player_visible=player_visible,
        hidden_info_safe=hidden_info_safe,
        metadata=safe_meta,
    )


@dataclass(frozen=True)
class ConfirmationRequirement:
    """Immutable confirmation requirement."""

    confirmation_id: str
    reason: str
    required: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "confirmation_id": self.confirmation_id,
            "reason": self.reason,
            "required": self.required,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_confirmation_requirement(
    confirmation_id: str,
    reason: str,
    required: bool,
    metadata: Mapping[str, Any] | None = None,
) -> ConfirmationRequirement:
    _validate_non_empty_string(
        confirmation_id, "confirmation_id", InvalidConfirmationRequirementError,
    )
    _validate_non_empty_string(
        reason, "reason", InvalidConfirmationRequirementError,
    )
    if not isinstance(required, bool):
        raise InvalidConfirmationRequirementError("required must be a bool")
    safe_meta = _safe_metadata(metadata, InvalidConfirmationRequirementError)
    return ConfirmationRequirement(
        confirmation_id=confirmation_id,
        reason=reason,
        required=required,
        metadata=safe_meta,
    )


@dataclass(frozen=True)
class CommandQuarantineResult:
    """Immutable command quarantine result."""

    quarantine_id: str
    reason_code: str
    message: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "quarantine_id": self.quarantine_id,
            "reason_code": self.reason_code,
            "message": self.message,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_command_quarantine_result(
    quarantine_id: str,
    reason_code: str,
    message: str,
    metadata: Mapping[str, Any] | None = None,
) -> CommandQuarantineResult:
    _validate_non_empty_string(
        quarantine_id, "quarantine_id", InvalidCommandQuarantineResultError,
    )
    _validate_non_empty_string(
        reason_code, "reason_code", InvalidCommandQuarantineResultError,
    )
    _validate_non_empty_string(
        message, "message", InvalidCommandQuarantineResultError,
    )
    safe_meta = _safe_metadata(metadata, InvalidCommandQuarantineResultError)
    return CommandQuarantineResult(
        quarantine_id=quarantine_id,
        reason_code=reason_code,
        message=message,
        metadata=safe_meta,
    )


@dataclass(frozen=True)
class ActionLegalityResult:
    """Immutable action legality result. Backend-owned; no domain rules, no state mutation."""

    legality_id: str
    command_id: str
    decision: str
    lifecycle_stage: str
    may_proceed_to_preview: bool
    requires_confirmation: bool
    dependencies: tuple[DependencyDeclaration, ...]
    block_reasons: tuple[LegalityBlockReason, ...]
    confirmation_requirement: ConfirmationRequirement | None
    quarantine_result: CommandQuarantineResult | None
    validation_id: str | None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "legality_id": self.legality_id,
            "command_id": self.command_id,
            "decision": self.decision,
            "lifecycle_stage": self.lifecycle_stage,
            "may_proceed_to_preview": self.may_proceed_to_preview,
            "requires_confirmation": self.requires_confirmation,
            "dependencies": [d.to_dict() for d in self.dependencies],
            "block_reasons": [b.to_dict() for b in self.block_reasons],
            "confirmation_requirement": (
                self.confirmation_requirement.to_dict()
                if self.confirmation_requirement is not None
                else None
            ),
            "quarantine_result": (
                self.quarantine_result.to_dict()
                if self.quarantine_result is not None
                else None
            ),
            "validation_id": self.validation_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_action_legality_result(
    legality_id: str,
    command_id: str,
    decision: str,
    lifecycle_stage: str,
    may_proceed_to_preview: bool,
    requires_confirmation: bool,
    dependencies: Sequence[DependencyDeclaration] | None = None,
    block_reasons: Sequence[LegalityBlockReason] | None = None,
    confirmation_requirement: ConfirmationRequirement | None = None,
    quarantine_result: CommandQuarantineResult | None = None,
    validation_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityResult:
    _validate_non_empty_string(
        legality_id, "legality_id", InvalidActionLegalityResultError,
    )
    _validate_non_empty_string(
        command_id, "command_id", InvalidActionLegalityResultError,
    )
    if decision not in ACTION_LEGALITY_DECISIONS:
        raise InvalidActionLegalityDecisionError(
            f"decision must be one of {sorted(ACTION_LEGALITY_DECISIONS)}, got: {decision!r}"
        )
    if lifecycle_stage not in COMMAND_LIFECYCLE_STAGES:
        raise InvalidActionLegalityResultError(
            f"lifecycle_stage must be one of {sorted(COMMAND_LIFECYCLE_STAGES)}, got: {lifecycle_stage!r}"
        )
    if not isinstance(may_proceed_to_preview, bool):
        raise InvalidActionLegalityResultError(
            "may_proceed_to_preview must be a bool"
        )
    if not isinstance(requires_confirmation, bool):
        raise InvalidActionLegalityResultError(
            "requires_confirmation must be a bool"
        )

    if dependencies is None:
        safe_deps: tuple[DependencyDeclaration, ...] = ()
    else:
        for i, dep in enumerate(dependencies):
            if not isinstance(dep, DependencyDeclaration):
                raise InvalidActionLegalityResultError(
                    f"dependencies[{i}] must be a DependencyDeclaration, got: {type(dep).__name__}"
                )
        safe_deps = tuple(dependencies)

    if block_reasons is None:
        safe_blocks: tuple[LegalityBlockReason, ...] = ()
    else:
        for i, br in enumerate(block_reasons):
            if not isinstance(br, LegalityBlockReason):
                raise InvalidActionLegalityResultError(
                    f"block_reasons[{i}] must be a LegalityBlockReason, got: {type(br).__name__}"
                )
        safe_blocks = tuple(block_reasons)

    if confirmation_requirement is not None and not isinstance(
        confirmation_requirement, ConfirmationRequirement,
    ):
        raise InvalidActionLegalityResultError(
            f"confirmation_requirement must be a ConfirmationRequirement or None, got: {type(confirmation_requirement).__name__}"
        )

    if quarantine_result is not None and not isinstance(
        quarantine_result, CommandQuarantineResult,
    ):
        raise InvalidActionLegalityResultError(
            f"quarantine_result must be a CommandQuarantineResult or None, got: {type(quarantine_result).__name__}"
        )

    if validation_id is not None:
        _validate_non_empty_string(
            validation_id, "validation_id", InvalidActionLegalityResultError,
        )

    safe_meta = _safe_metadata(metadata, InvalidActionLegalityResultError)

    return ActionLegalityResult(
        legality_id=legality_id,
        command_id=command_id,
        decision=decision,
        lifecycle_stage=lifecycle_stage,
        may_proceed_to_preview=may_proceed_to_preview,
        requires_confirmation=requires_confirmation,
        dependencies=safe_deps,
        block_reasons=safe_blocks,
        confirmation_requirement=confirmation_requirement,
        quarantine_result=quarantine_result,
        validation_id=validation_id,
        metadata=safe_meta,
    )


def validate_action_legality_result(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityResult):
        return False
    if not isinstance(obj.legality_id, str) or not obj.legality_id.strip():
        return False
    if not isinstance(obj.command_id, str) or not obj.command_id.strip():
        return False
    if obj.decision not in ACTION_LEGALITY_DECISIONS:
        return False
    if obj.lifecycle_stage not in COMMAND_LIFECYCLE_STAGES:
        return False
    if not isinstance(obj.may_proceed_to_preview, bool):
        return False
    if not isinstance(obj.requires_confirmation, bool):
        return False
    if not isinstance(obj.dependencies, tuple):
        return False
    for dep in obj.dependencies:
        if not isinstance(dep, DependencyDeclaration):
            return False
    if not isinstance(obj.block_reasons, tuple):
        return False
    for br in obj.block_reasons:
        if not isinstance(br, LegalityBlockReason):
            return False
    if obj.confirmation_requirement is not None and not isinstance(
        obj.confirmation_requirement, ConfirmationRequirement,
    ):
        return False
    if obj.quarantine_result is not None and not isinstance(
        obj.quarantine_result, CommandQuarantineResult,
    ):
        return False
    if obj.validation_id is not None:
        if not isinstance(obj.validation_id, str) or not obj.validation_id.strip():
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def evaluate_action_legality(
    legality_id: str,
    command: CommandEnvelope,
    *,
    decision: str,
    lifecycle_stage: str = "legality_prechecked",
    may_proceed_to_preview: bool | None = None,
    requires_confirmation: bool = False,
    dependencies: Sequence[DependencyDeclaration] | None = None,
    block_reasons: Sequence[LegalityBlockReason] | None = None,
    confirmation_requirement: ConfirmationRequirement | None = None,
    quarantine_result: CommandQuarantineResult | None = None,
    validation_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityResult:
    if not validate_command_envelope(command):
        raise ActionLegalityError(
            "command must be a valid CommandEnvelope"
        )
    if may_proceed_to_preview is None:
        may_proceed_to_preview = decision in _MAY_PROCEED_DECISIONS
    return create_action_legality_result(
        legality_id=legality_id,
        command_id=command.command_id,
        decision=decision,
        lifecycle_stage=lifecycle_stage,
        may_proceed_to_preview=may_proceed_to_preview,
        requires_confirmation=requires_confirmation,
        dependencies=dependencies,
        block_reasons=block_reasons,
        confirmation_requirement=confirmation_requirement,
        quarantine_result=quarantine_result,
        validation_id=validation_id,
        metadata=metadata,
    )


class ActionLegalityService:
    """Stateless wrapper around evaluate_action_legality."""

    def evaluate(
        self,
        legality_id: str,
        command: CommandEnvelope,
        *,
        decision: str,
        lifecycle_stage: str = "legality_prechecked",
        may_proceed_to_preview: bool | None = None,
        requires_confirmation: bool = False,
        dependencies: Sequence[DependencyDeclaration] | None = None,
        block_reasons: Sequence[LegalityBlockReason] | None = None,
        confirmation_requirement: ConfirmationRequirement | None = None,
        quarantine_result: CommandQuarantineResult | None = None,
        validation_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> ActionLegalityResult:
        return evaluate_action_legality(
            legality_id=legality_id,
            command=command,
            decision=decision,
            lifecycle_stage=lifecycle_stage,
            may_proceed_to_preview=may_proceed_to_preview,
            requires_confirmation=requires_confirmation,
            dependencies=dependencies,
            block_reasons=block_reasons,
            confirmation_requirement=confirmation_requirement,
            quarantine_result=quarantine_result,
            validation_id=validation_id,
            metadata=metadata,
        )
