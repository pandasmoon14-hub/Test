"""Validation pipeline and invariant precheck skeleton — backend-owned, no domain rules."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence
from types import MappingProxyType


class ValidationPipelineError(Exception):
    """Base error for validation pipeline operations."""


class InvalidValidationIssueError(ValidationPipelineError):
    """Raised when a validation issue fails validation."""


class InvalidValidationResultError(ValidationPipelineError):
    """Raised when a validation result fails validation."""


class InvalidValidationCheckError(ValidationPipelineError):
    """Raised when a validation check is invalid."""


class InvariantPrecheckError(ValidationPipelineError):
    """Base error for invariant precheck operations."""


class InvalidInvariantPrecheckError(InvariantPrecheckError):
    """Raised when an invariant precheck descriptor fails validation."""


_ALLOWED_SEVERITIES = frozenset({"info", "warning", "error", "critical"})
_FAILING_SEVERITIES = frozenset({"error", "critical"})


def _validate_non_empty_string(value: Any, name: str, error_cls: type[Exception]) -> None:
    if not isinstance(value, str) or not value.strip():
        raise error_cls(f"{name} must be a non-empty string")


def _validate_severity(value: Any, error_cls: type[Exception]) -> None:
    if value not in _ALLOWED_SEVERITIES:
        raise error_cls(
            f"severity must be one of {sorted(_ALLOWED_SEVERITIES)}, got: {value!r}"
        )


def _safe_metadata(metadata: Mapping[str, Any] | None, error_cls: type[Exception]) -> Mapping[str, Any]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    return MappingProxyType(copy.deepcopy(dict(metadata)))


@dataclass(frozen=True)
class ValidationIssue:
    """Immutable validation issue envelope. Backend-owned; no domain rules."""

    code: str
    message: str
    severity: str
    source: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "source": self.source,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class ValidationResult:
    """Immutable validation result envelope. Backend-owned; no domain rules."""

    validation_id: str
    subject_ref: str
    passed: bool
    issues: tuple[ValidationIssue, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_id": self.validation_id,
            "subject_ref": self.subject_ref,
            "passed": self.passed,
            "issues": [issue.to_dict() for issue in self.issues],
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class InvariantPrecheck:
    """Immutable invariant precheck descriptor. Backend-owned; no domain rules."""

    invariant_id: str
    description: str
    severity: str
    source: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "invariant_id": self.invariant_id,
            "description": self.description,
            "severity": self.severity,
            "source": self.source,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_validation_issue(
    code: str,
    message: str,
    severity: str,
    source: str,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationIssue:
    _validate_non_empty_string(code, "code", InvalidValidationIssueError)
    _validate_non_empty_string(message, "message", InvalidValidationIssueError)
    _validate_non_empty_string(source, "source", InvalidValidationIssueError)
    _validate_severity(severity, InvalidValidationIssueError)
    safe_meta = _safe_metadata(metadata, InvalidValidationIssueError)
    return ValidationIssue(
        code=code,
        message=message,
        severity=severity,
        source=source,
        metadata=safe_meta,
    )


def create_validation_result(
    validation_id: str,
    subject_ref: str,
    passed: bool,
    issues: Sequence[ValidationIssue] = (),
    metadata: Mapping[str, Any] | None = None,
) -> ValidationResult:
    _validate_non_empty_string(validation_id, "validation_id", InvalidValidationResultError)
    _validate_non_empty_string(subject_ref, "subject_ref", InvalidValidationResultError)
    if not isinstance(passed, bool):
        raise InvalidValidationResultError("passed must be a bool")
    for i, issue in enumerate(issues):
        if not isinstance(issue, ValidationIssue):
            raise InvalidValidationResultError(
                f"issues[{i}] must be a ValidationIssue, got: {type(issue).__name__}"
            )
    safe_meta = _safe_metadata(metadata, InvalidValidationResultError)
    return ValidationResult(
        validation_id=validation_id,
        subject_ref=subject_ref,
        passed=passed,
        issues=tuple(issues),
        metadata=safe_meta,
    )


def create_invariant_precheck(
    invariant_id: str,
    description: str,
    severity: str,
    source: str,
    metadata: Mapping[str, Any] | None = None,
) -> InvariantPrecheck:
    _validate_non_empty_string(invariant_id, "invariant_id", InvalidInvariantPrecheckError)
    _validate_non_empty_string(description, "description", InvalidInvariantPrecheckError)
    _validate_non_empty_string(source, "source", InvalidInvariantPrecheckError)
    _validate_severity(severity, InvalidInvariantPrecheckError)
    safe_meta = _safe_metadata(metadata, InvalidInvariantPrecheckError)
    return InvariantPrecheck(
        invariant_id=invariant_id,
        description=description,
        severity=severity,
        source=source,
        metadata=safe_meta,
    )


def validate_validation_issue(obj: Any) -> bool:
    if not isinstance(obj, ValidationIssue):
        return False
    if not isinstance(obj.code, str) or not obj.code.strip():
        return False
    if not isinstance(obj.message, str) or not obj.message.strip():
        return False
    if obj.severity not in _ALLOWED_SEVERITIES:
        return False
    if not isinstance(obj.source, str) or not obj.source.strip():
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_validation_result(obj: Any) -> bool:
    if not isinstance(obj, ValidationResult):
        return False
    if not isinstance(obj.validation_id, str) or not obj.validation_id.strip():
        return False
    if not isinstance(obj.subject_ref, str) or not obj.subject_ref.strip():
        return False
    if not isinstance(obj.passed, bool):
        return False
    if not isinstance(obj.issues, tuple):
        return False
    for issue in obj.issues:
        if not isinstance(issue, ValidationIssue):
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_invariant_precheck(obj: Any) -> bool:
    if not isinstance(obj, InvariantPrecheck):
        return False
    if not isinstance(obj.invariant_id, str) or not obj.invariant_id.strip():
        return False
    if not isinstance(obj.description, str) or not obj.description.strip():
        return False
    if obj.severity not in _ALLOWED_SEVERITIES:
        return False
    if not isinstance(obj.source, str) or not obj.source.strip():
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def run_validation_checks(
    validation_id: str,
    subject_ref: str,
    subject: Any,
    checks: Sequence[Callable[[Any], Sequence[ValidationIssue] | ValidationIssue | None]],
    metadata: Mapping[str, Any] | None = None,
) -> ValidationResult:
    _validate_non_empty_string(validation_id, "validation_id", InvalidValidationCheckError)
    _validate_non_empty_string(subject_ref, "subject_ref", InvalidValidationCheckError)
    for i, check in enumerate(checks):
        if not callable(check):
            raise InvalidValidationCheckError(
                f"checks[{i}] must be callable, got: {type(check).__name__}"
            )

    all_issues: list[ValidationIssue] = []
    for check in checks:
        result = check(subject)
        if result is None:
            continue
        if isinstance(result, ValidationIssue):
            all_issues.append(result)
        else:
            all_issues.extend(result)

    passed = not any(issue.severity in _FAILING_SEVERITIES for issue in all_issues)
    safe_meta = _safe_metadata(metadata, InvalidValidationCheckError)

    return ValidationResult(
        validation_id=validation_id,
        subject_ref=subject_ref,
        passed=passed,
        issues=tuple(all_issues),
        metadata=safe_meta,
    )


def required_keys_check(
    required_keys: Sequence[str],
    *,
    source: str = "required_keys_check",
) -> Callable[[Any], tuple[ValidationIssue, ...]]:
    if not isinstance(required_keys, Sequence) or isinstance(required_keys, (str, bytes)):
        raise InvalidValidationCheckError("required_keys must be a sequence")
    validated_keys: list[str] = []
    for i, key in enumerate(required_keys):
        if not isinstance(key, str):
            raise InvalidValidationCheckError(
                f"required_keys[{i}] must be a string, got: {type(key).__name__}"
            )
        if not key.strip():
            raise InvalidValidationCheckError(
                f"required_keys[{i}] must be a non-empty string"
            )
        validated_keys.append(key)

    def _check(subject: Any) -> tuple[ValidationIssue, ...]:
        if not isinstance(subject, Mapping):
            return (ValidationIssue(
                code="not_a_mapping",
                message="subject is not a mapping",
                severity="error",
                source=source,
                metadata=MappingProxyType({}),
            ),)
        issues: list[ValidationIssue] = []
        for key in validated_keys:
            if key not in subject:
                issues.append(ValidationIssue(
                    code="missing_required_key",
                    message=f"required key missing: {key}",
                    severity="error",
                    source=source,
                    metadata=MappingProxyType({}),
                ))
        return tuple(issues)

    return _check


def run_invariant_prechecks(
    validation_id: str,
    subject_ref: str,
    subject: Any,
    prechecks: Sequence[Callable[[Any], Sequence[ValidationIssue] | ValidationIssue | None]],
    metadata: Mapping[str, Any] | None = None,
) -> ValidationResult:
    return run_validation_checks(
        validation_id=validation_id,
        subject_ref=subject_ref,
        subject=subject,
        checks=prechecks,
        metadata=metadata,
    )
