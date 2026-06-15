"""Validation integration bridge skeleton — backend-owned bridge between
scene command execution assembly surfaces (PR-9A), command-kind routing
results (PR-9C), and existing validation pipeline / validation integration
skeleton surfaces.

RUNTIME-DOMAIN-PR-9D: consumes command-kind routing results and command
envelope data, produces validation integration bridge results without
deciding legality, executing validation rules, blocking/approving actions,
executing commands, mutating state, appending events, persisting,
executing RNG/table/oracle, settling, applying consequences, compiling
packets, calling models, rendering prompts, generating narration,
authorising live play, converting, including sourcebooks, or promoting
canon.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from astra_runtime.domain.command_kind_routing_skeleton import (
    CommandKindRoutingResult,
    validate_command_kind_routing_result,
)
from astra_runtime.domain.scene_command_execution_skeleton import (
    SceneCommandExecutionAssemblyRequest,
    SceneCommandExecutionValidationRef,
)
from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    validate_command_envelope,
)
from astra_runtime.kernel.record_identity import (
    build_record_id,
    is_valid_record_id,
)
from astra_runtime.kernel.validation_pipeline import (
    ValidationResult,
    validate_validation_result,
)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class ValidationIntegrationBridgeSkeletonError(ValueError):
    """Base error for validation integration bridge skeleton operations."""


class InvalidValidationBridgeRequestError(ValidationIntegrationBridgeSkeletonError):
    """Raised when a bridge request fails validation."""


class InvalidValidationBridgeSubjectRefError(ValidationIntegrationBridgeSkeletonError):
    """Raised when a bridge subject reference fails validation."""


class InvalidValidationBridgeRequirementRefError(ValidationIntegrationBridgeSkeletonError):
    """Raised when a bridge requirement reference fails validation."""


class InvalidValidationBridgeResultRefError(ValidationIntegrationBridgeSkeletonError):
    """Raised when a bridge result reference fails validation."""


class InvalidValidationBridgeOwnerRouteRefError(ValidationIntegrationBridgeSkeletonError):
    """Raised when a bridge owner route reference fails validation."""


class InvalidValidationBridgeAuthorityFlagsError(ValidationIntegrationBridgeSkeletonError):
    """Raised when a bridge authority flags record fails validation."""


class InvalidValidationBridgeResultError(ValidationIntegrationBridgeSkeletonError):
    """Raised when a bridge result fails validation."""


# ---------------------------------------------------------------------------
# Constants — owner-route references
# ---------------------------------------------------------------------------

RT005_VALIDATION_INTEGRATION: str = "RT005_VALIDATION_INTEGRATION"

_VALID_OWNER_ROUTES: frozenset[str] = frozenset({
    "RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY",
    "RT002_RESOURCE_CONSEQUENCE_MATH",
    "RT003_STATE_STORE_STATE_PROJECTION",
    "RT004_TRANSACTION_LIFECYCLE_EVENT_COMMITMENT",
    "RT005_VALIDATION_INTEGRATION",
    "RT006_CONTEXT_PACKET_COMPILER",
    "RT007_MODEL_BOUNDARY_EVALUATION",
    "RT008_TINY_VERTICAL_SLICE_REFERENCE_ONLY",
    "RT009_RNG_TABLE_ORACLE_REFERENCE_ONLY",
    "DEFERRED_RUNTIME_OWNER",
    "QUARANTINE_UNKNOWN_COMMAND_KIND",
})

_VALID_REQUIREMENT_KINDS: frozenset[str] = frozenset({
    "command_envelope_ref",
    "command_kind_routing_ref",
    "command_kind_classification_ref",
    "command_dispatch_shell_ref",
    "validation_pipeline_ref",
    "validation_result_ref",
    "validation_integration_ref",
    "scene_command_assembly_ref",
    "scene_command_validation_ref",
})

_VALID_SUBJECT_TYPES: frozenset[str] = frozenset({
    "command",
    "validation_pipeline",
    "validation_integration",
    "scene_command_assembly",
})


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _validate_non_empty_str(value: object, name: str, error_cls: type[Exception]) -> str:
    if not isinstance(value, str) or not value.strip():
        raise error_cls(f"{name} must be a non-empty string, got {value!r}")
    return value


def _validate_record_id(value: object, name: str, error_cls: type[Exception]) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise error_cls(f"{name} must be a valid record ID, got {value!r}")
    return value


def _safe_metadata(
    metadata: Mapping[str, Any] | None, error_cls: type[Exception],
) -> Mapping[str, Any]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls(f"metadata must be a Mapping, got {type(metadata).__name__}")
    return MappingProxyType(copy.deepcopy(dict(metadata)))


def _safe_obj_ref(value: object, name: str, error_cls: type[Exception], expected_type: type) -> Any:
    if value is not None and not isinstance(value, expected_type):
        raise error_cls(f"{name} must be a {expected_type.__name__} or None, got {type(value).__name__}")
    return value


# ---------------------------------------------------------------------------
# Reference dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ValidationBridgeSubjectRef:
    """Immutable reference to a validation bridge subject."""

    subject_type: str
    ref_id: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "subject_type",
            _validate_non_empty_str(self.subject_type, "subject_type", InvalidValidationBridgeSubjectRefError),
        )
        if self.subject_type not in _VALID_SUBJECT_TYPES:
            raise InvalidValidationBridgeSubjectRefError(
                f"subject_type must be one of {sorted(_VALID_SUBJECT_TYPES)}, got {self.subject_type!r}"
            )
        object.__setattr__(
            self, "ref_id",
            _validate_record_id(self.ref_id, "ref_id", InvalidValidationBridgeSubjectRefError),
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidValidationBridgeSubjectRefError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_type": self.subject_type,
            "ref_id": self.ref_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ValidationBridgeRequirementRef:
    """Immutable reference to a validation requirement."""

    requirement_id: str
    requirement_kind: str
    requirement_ref: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "requirement_id",
            _validate_record_id(self.requirement_id, "requirement_id", InvalidValidationBridgeRequirementRefError),
        )
        if self.requirement_kind not in _VALID_REQUIREMENT_KINDS:
            raise InvalidValidationBridgeRequirementRefError(
                f"requirement_kind must be one of {sorted(_VALID_REQUIREMENT_KINDS)}, "
                f"got {self.requirement_kind!r}"
            )
        object.__setattr__(
            self, "requirement_ref",
            _validate_non_empty_str(self.requirement_ref, "requirement_ref", InvalidValidationBridgeRequirementRefError),
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidValidationBridgeRequirementRefError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "requirement_kind": self.requirement_kind,
            "requirement_ref": self.requirement_ref,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ValidationBridgeOwnerRouteRef:
    """Immutable reference to a validation bridge owner route."""

    owner_route: str
    route_label: str = ""
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if self.owner_route not in _VALID_OWNER_ROUTES:
            raise InvalidValidationBridgeOwnerRouteRefError(
                f"owner_route must be one of {sorted(_VALID_OWNER_ROUTES)}, got {self.owner_route!r}"
            )
        if not isinstance(self.route_label, str):
            raise InvalidValidationBridgeOwnerRouteRefError(
                f"route_label must be a string, got {type(self.route_label).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidValidationBridgeOwnerRouteRefError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "owner_route": self.owner_route,
            "route_label": self.route_label,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ValidationBridgeResultRef:
    """Immutable reference to a validation result — may carry a ValidationResult by reference."""

    result_ref_id: str
    validation_result: ValidationResult | None = None
    pending: bool = False
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "result_ref_id",
            _validate_record_id(self.result_ref_id, "result_ref_id", InvalidValidationBridgeResultRefError),
        )
        if self.validation_result is not None and not validate_validation_result(self.validation_result):
            raise InvalidValidationBridgeResultRefError(
                "validation_result must be a valid ValidationResult if provided"
            )
        if not isinstance(self.pending, bool):
            raise InvalidValidationBridgeResultRefError(
                f"pending must be a bool, got {type(self.pending).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidValidationBridgeResultRefError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_ref_id": self.result_ref_id,
            "validation_result": self.validation_result.to_dict() if self.validation_result is not None else None,
            "pending": self.pending,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Bridge request
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ValidationIntegrationBridgeRequest:
    """Immutable bridge request referencing inputs for validation integration.

    Accepts a CommandEnvelope, a PR-9C CommandKindRoutingResult, and optional
    PR-9A surfaces. Does not resolve legality, execute validation rules, or
    block/approve actions.
    """

    request_ref: str
    command_envelope: CommandEnvelope
    routing_result: CommandKindRoutingResult
    assembly_request: SceneCommandExecutionAssemblyRequest | None = None
    validation_ref: SceneCommandExecutionValidationRef | None = None
    validation_result: ValidationResult | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "request_ref",
            _validate_record_id(self.request_ref, "request_ref", InvalidValidationBridgeRequestError),
        )
        if not validate_command_envelope(self.command_envelope):
            raise InvalidValidationBridgeRequestError(
                "command_envelope failed validation"
            )
        if not validate_command_kind_routing_result(self.routing_result):
            raise InvalidValidationBridgeRequestError(
                "routing_result failed validation"
            )
        if self.routing_result.command_ref != self.command_envelope.command_id:
            raise InvalidValidationBridgeRequestError(
                "routing_result.command_ref must match command_envelope.command_id"
            )
        _safe_obj_ref(
            self.assembly_request,
            "assembly_request",
            InvalidValidationBridgeRequestError,
            SceneCommandExecutionAssemblyRequest,
        )
        _safe_obj_ref(
            self.validation_ref,
            "validation_ref",
            InvalidValidationBridgeRequestError,
            SceneCommandExecutionValidationRef,
        )
        if self.validation_result is not None and not validate_validation_result(self.validation_result):
            raise InvalidValidationBridgeRequestError(
                "validation_result must be a valid ValidationResult if provided"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidValidationBridgeRequestError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_ref": self.request_ref,
            "command_envelope": self.command_envelope.to_dict(),
            "routing_result": self.routing_result.to_dict(),
            "assembly_request": self.assembly_request.to_dict() if self.assembly_request is not None else None,
            "validation_ref": self.validation_ref.to_dict() if self.validation_ref is not None else None,
            "validation_result": self.validation_result.to_dict() if self.validation_result is not None else None,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Bridge authority flags — all must be False
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ValidationIntegrationBridgeAuthorityFlags:
    """All authority flags default to False. Constructing with any True flag raises an error.

    Explicitly denies legality resolution, validation rule execution, command
    execution, runtime action execution, state mutation, event append,
    persistence write, RNG/table/oracle execution, settlement authorization,
    PR-5 arithmetic execution, consequence application, packet compilation,
    model authority, prompt rendering, prompt execution, prose parsing,
    narration generation, live-play/session authority, UI/client authority,
    conversion, sourcebook inclusion, and canon promotion.
    """

    legality_resolution: bool = False
    validation_rule_execution: bool = False
    command_execution: bool = False
    runtime_action_execution: bool = False
    state_mutation: bool = False
    event_append: bool = False
    persistence_write: bool = False
    rng_table_oracle_execution: bool = False
    settlement_authorization: bool = False
    pr5_arithmetic_execution: bool = False
    consequence_application: bool = False
    packet_compilation: bool = False
    model_authority: bool = False
    prompt_rendering: bool = False
    prompt_execution: bool = False
    prose_parsing: bool = False
    narration_generation: bool = False
    live_play_session_authority: bool = False
    ui_client_authority: bool = False
    conversion: bool = False
    sourcebook_inclusion: bool = False
    canon_promotion: bool = False

    def __post_init__(self) -> None:
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if value is not False:
                raise InvalidValidationBridgeAuthorityFlagsError(
                    f"authority flag '{field_name}' must be False in PR-9D bridge skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


# ---------------------------------------------------------------------------
# Bridge result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ValidationIntegrationBridgeResult:
    """Immutable validation integration bridge result.

    Includes bridge result id, bridge request id, command reference, command
    family from PR-9C routing, command kind from PR-9C routing, owner route
    from PR-9C dispatch shell, validation subject reference, validation
    requirement references, validation result reference, validation pipeline
    reference (if available), false-only authority flags, and metadata.
    """

    result_ref: str
    request_ref: str
    command_ref: str
    command_family: str
    command_kind: str
    owner_route: ValidationBridgeOwnerRouteRef
    subject_ref: ValidationBridgeSubjectRef
    requirement_refs: tuple[ValidationBridgeRequirementRef, ...]
    validation_result_ref: ValidationBridgeResultRef
    validation_pipeline_ref: str | None = None
    authority_flags: ValidationIntegrationBridgeAuthorityFlags = field(
        default_factory=ValidationIntegrationBridgeAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "result_ref",
            _validate_record_id(self.result_ref, "result_ref", InvalidValidationBridgeResultError),
        )
        object.__setattr__(
            self, "request_ref",
            _validate_record_id(self.request_ref, "request_ref", InvalidValidationBridgeResultError),
        )
        object.__setattr__(
            self, "command_ref",
            _validate_non_empty_str(self.command_ref, "command_ref", InvalidValidationBridgeResultError),
        )
        object.__setattr__(
            self, "command_family",
            _validate_non_empty_str(self.command_family, "command_family", InvalidValidationBridgeResultError),
        )
        object.__setattr__(
            self, "command_kind",
            _validate_non_empty_str(self.command_kind, "command_kind", InvalidValidationBridgeResultError),
        )
        if not isinstance(self.owner_route, ValidationBridgeOwnerRouteRef):
            raise InvalidValidationBridgeResultError(
                f"owner_route must be a ValidationBridgeOwnerRouteRef, "
                f"got {type(self.owner_route).__name__}"
            )
        if not isinstance(self.subject_ref, ValidationBridgeSubjectRef):
            raise InvalidValidationBridgeResultError(
                f"subject_ref must be a ValidationBridgeSubjectRef, "
                f"got {type(self.subject_ref).__name__}"
            )
        if not isinstance(self.requirement_refs, tuple):
            raise InvalidValidationBridgeResultError(
                "requirement_refs must be a tuple"
            )
        for i, req in enumerate(self.requirement_refs):
            if not isinstance(req, ValidationBridgeRequirementRef):
                raise InvalidValidationBridgeResultError(
                    f"requirement_refs[{i}] must be a ValidationBridgeRequirementRef, "
                    f"got {type(req).__name__}"
                )
        if not isinstance(self.validation_result_ref, ValidationBridgeResultRef):
            raise InvalidValidationBridgeResultError(
                f"validation_result_ref must be a ValidationBridgeResultRef, "
                f"got {type(self.validation_result_ref).__name__}"
            )
        if self.validation_pipeline_ref is not None:
            object.__setattr__(
                self, "validation_pipeline_ref",
                _validate_non_empty_str(
                    self.validation_pipeline_ref,
                    "validation_pipeline_ref",
                    InvalidValidationBridgeResultError,
                ),
            )
        if not isinstance(self.authority_flags, ValidationIntegrationBridgeAuthorityFlags):
            raise InvalidValidationBridgeResultError(
                f"authority_flags must be a ValidationIntegrationBridgeAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidValidationBridgeResultError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_ref": self.result_ref,
            "request_ref": self.request_ref,
            "command_ref": self.command_ref,
            "command_family": self.command_family,
            "command_kind": self.command_kind,
            "owner_route": self.owner_route.to_dict(),
            "subject_ref": self.subject_ref.to_dict(),
            "requirement_refs": [r.to_dict() for r in self.requirement_refs],
            "validation_result_ref": self.validation_result_ref.to_dict(),
            "validation_pipeline_ref": self.validation_pipeline_ref,
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def create_validation_bridge_subject_ref(
    *,
    subject_type: str,
    ref_id: str,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationBridgeSubjectRef:
    """Create a validation bridge subject reference."""
    return ValidationBridgeSubjectRef(
        subject_type=subject_type,
        ref_id=ref_id,
        metadata=metadata,
    )


def create_validation_bridge_requirement_ref(
    *,
    requirement_id: str,
    requirement_kind: str,
    requirement_ref: str,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationBridgeRequirementRef:
    """Create a validation bridge requirement reference."""
    return ValidationBridgeRequirementRef(
        requirement_id=requirement_id,
        requirement_kind=requirement_kind,
        requirement_ref=requirement_ref,
        metadata=metadata,
    )


def create_validation_bridge_owner_route_ref(
    *,
    owner_route: str = RT005_VALIDATION_INTEGRATION,
    route_label: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> ValidationBridgeOwnerRouteRef:
    """Create a validation bridge owner route reference."""
    return ValidationBridgeOwnerRouteRef(
        owner_route=owner_route,
        route_label=route_label,
        metadata=metadata,
    )


def create_validation_bridge_result_ref(
    *,
    result_ref_id: str,
    validation_result: ValidationResult | None = None,
    pending: bool = True,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationBridgeResultRef:
    """Create a validation bridge result reference.

    If no ValidationResult is provided, produces a pending/reference-only
    validation result ref (pending=True by default).
    """
    return ValidationBridgeResultRef(
        result_ref_id=result_ref_id,
        validation_result=validation_result,
        pending=pending,
        metadata=metadata,
    )


def create_validation_integration_bridge_authority_flags() -> ValidationIntegrationBridgeAuthorityFlags:
    """Return the default PR-9D anti-authority flag set (all False)."""
    return ValidationIntegrationBridgeAuthorityFlags()


def create_validation_integration_bridge_request(
    *,
    request_ref: str,
    command_envelope: CommandEnvelope,
    routing_result: CommandKindRoutingResult,
    assembly_request: SceneCommandExecutionAssemblyRequest | None = None,
    validation_ref: SceneCommandExecutionValidationRef | None = None,
    validation_result: ValidationResult | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationIntegrationBridgeRequest:
    """Create a validation integration bridge request.

    Validates the command envelope, routing result, and ensures the routing
    result command reference matches the command envelope command id. Does not
    call PR-9C route functions (consumes a pre-computed routing result).
    Does not call PR-9A `assemble_scene_command_execution_result`.
    Does not resolve legality, execute validation rules, or block/approve actions.
    """
    return ValidationIntegrationBridgeRequest(
        request_ref=request_ref,
        command_envelope=command_envelope,
        routing_result=routing_result,
        assembly_request=assembly_request,
        validation_ref=validation_ref,
        validation_result=validation_result,
        metadata=metadata,
    )


def build_validation_integration_bridge_result(
    *,
    request: ValidationIntegrationBridgeRequest,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationIntegrationBridgeResult:
    """Build a validation integration bridge result from a bridge request.

    Produces a deterministic, immutable result with false-only authority
    flags. Validates inputs, extracts command family/kind/owner route from
    the PR-9C routing result without reclassifying, and creates validation
    surface references.

    Does not:
    - decide legality
    - execute validation rules
    - block or approve actions
    - mutate any input object
    - call PR-9A assemble_scene_command_execution_result
    - call PR-9C route functions inside this function
    """
    if not isinstance(request, ValidationIntegrationBridgeRequest):
        raise InvalidValidationBridgeResultError(
            f"request must be a ValidationIntegrationBridgeRequest, "
            f"got {type(request).__name__}"
        )

    # Extract command family and kind from the PR-9C routing result
    # (by reference only, no reclassification)
    command_family = request.routing_result.classification.family
    command_kind = request.routing_result.classification.kind

    # Extract owner route from the PR-9C dispatch shell
    dispatch_owner_route = request.routing_result.dispatch_shell.owner_route

    # Build owner route ref
    owner_route_ref = create_validation_bridge_owner_route_ref(
        owner_route=dispatch_owner_route,
        route_label=f"from_PR_9C_dispatch_shell:{dispatch_owner_route}",
    )

    # Build subject ref
    safe_local = request.command_envelope.command_id.replace(":", "_")
    subject_ref = create_validation_bridge_subject_ref(
        subject_type="command",
        ref_id=request.command_envelope.command_id,
    )

    # Build requirement refs from routing result and envelope
    requirement_refs: list[ValidationBridgeRequirementRef] = [
        create_validation_bridge_requirement_ref(
            requirement_id=build_record_id("bridge_req", f"{safe_local}_envelope"),
            requirement_kind="command_envelope_ref",
            requirement_ref=request.command_envelope.command_id,
        ),
        create_validation_bridge_requirement_ref(
            requirement_id=build_record_id("bridge_req", f"{safe_local}_routing"),
            requirement_kind="command_kind_routing_ref",
            requirement_ref=request.routing_result.result_ref,
        ),
        create_validation_bridge_requirement_ref(
            requirement_id=build_record_id("bridge_req", f"{safe_local}_classification"),
            requirement_kind="command_kind_classification_ref",
            requirement_ref=request.routing_result.classification.classification_ref,
        ),
        create_validation_bridge_requirement_ref(
            requirement_id=build_record_id("bridge_req", f"{safe_local}_dispatch"),
            requirement_kind="command_dispatch_shell_ref",
            requirement_ref=request.routing_result.dispatch_shell.dispatch_ref,
        ),
    ]

    # If a PR-9A validation ref is provided, add a requirement for it
    if request.validation_ref is not None:
        requirement_refs.append(
            create_validation_bridge_requirement_ref(
                requirement_id=build_record_id("bridge_req", f"{safe_local}_val_ref"),
                requirement_kind="scene_command_validation_ref",
                requirement_ref=request.validation_ref.validation_ref,
            ),
        )

    # Build validation result ref
    if request.validation_result is not None:
        validation_result_ref = create_validation_bridge_result_ref(
            result_ref_id=build_record_id("bridge_val_result", safe_local),
            validation_result=request.validation_result,
            pending=False,
        )
    else:
        validation_result_ref = create_validation_bridge_result_ref(
            result_ref_id=build_record_id("bridge_val_result", safe_local),
            pending=True,
        )

    # Determine validation pipeline ref
    validation_pipeline_ref: str | None = None
    if request.validation_ref is not None and request.validation_ref.validation_result is not None:
        validation_pipeline_ref = request.validation_ref.validation_result.validation_id
    elif request.validation_result is not None:
        validation_pipeline_ref = request.validation_result.validation_id

    # Build the result ref id
    result_ref_id = build_record_id("bridge_result", safe_local)

    return ValidationIntegrationBridgeResult(
        result_ref=result_ref_id,
        request_ref=request.request_ref,
        command_ref=request.command_envelope.command_id,
        command_family=command_family,
        command_kind=command_kind,
        owner_route=owner_route_ref,
        subject_ref=subject_ref,
        requirement_refs=tuple(requirement_refs),
        validation_result_ref=validation_result_ref,
        validation_pipeline_ref=validation_pipeline_ref,
        authority_flags=create_validation_integration_bridge_authority_flags(),
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_validation_bridge_subject_ref(obj: Any) -> bool:
    """Validate a ValidationBridgeSubjectRef."""
    if not isinstance(obj, ValidationBridgeSubjectRef):
        return False
    if obj.subject_type not in _VALID_SUBJECT_TYPES:
        return False
    if not is_valid_record_id(obj.ref_id):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_validation_bridge_requirement_ref(obj: Any) -> bool:
    """Validate a ValidationBridgeRequirementRef."""
    if not isinstance(obj, ValidationBridgeRequirementRef):
        return False
    if not is_valid_record_id(obj.requirement_id):
        return False
    if obj.requirement_kind not in _VALID_REQUIREMENT_KINDS:
        return False
    if not isinstance(obj.requirement_ref, str) or not obj.requirement_ref.strip():
        return False
    return isinstance(obj.metadata, Mapping)


def validate_validation_bridge_owner_route_ref(obj: Any) -> bool:
    """Validate a ValidationBridgeOwnerRouteRef."""
    if not isinstance(obj, ValidationBridgeOwnerRouteRef):
        return False
    if obj.owner_route not in _VALID_OWNER_ROUTES:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_validation_bridge_result_ref(obj: Any) -> bool:
    """Validate a ValidationBridgeResultRef."""
    if not isinstance(obj, ValidationBridgeResultRef):
        return False
    if not is_valid_record_id(obj.result_ref_id):
        return False
    if obj.validation_result is not None and not validate_validation_result(obj.validation_result):
        return False
    if not isinstance(obj.pending, bool):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_validation_integration_bridge_authority_flags(obj: Any) -> bool:
    """Validate that all authority flags are False."""
    if not isinstance(obj, ValidationIntegrationBridgeAuthorityFlags):
        return False
    for field_name in obj.__dataclass_fields__:
        if getattr(obj, field_name) is not False:
            return False
    return True


def validate_validation_integration_bridge_request(obj: Any) -> bool:
    """Validate a ValidationIntegrationBridgeRequest."""
    if not isinstance(obj, ValidationIntegrationBridgeRequest):
        return False
    if not is_valid_record_id(obj.request_ref):
        return False
    if not validate_command_envelope(obj.command_envelope):
        return False
    if not validate_command_kind_routing_result(obj.routing_result):
        return False
    if obj.routing_result.command_ref != obj.command_envelope.command_id:
        return False
    if obj.assembly_request is not None and not isinstance(obj.assembly_request, SceneCommandExecutionAssemblyRequest):
        return False
    if obj.validation_ref is not None and not isinstance(obj.validation_ref, SceneCommandExecutionValidationRef):
        return False
    if obj.validation_result is not None and not validate_validation_result(obj.validation_result):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_validation_integration_bridge_result(obj: Any) -> bool:
    """Validate a ValidationIntegrationBridgeResult."""
    if not isinstance(obj, ValidationIntegrationBridgeResult):
        return False
    if not is_valid_record_id(obj.result_ref):
        return False
    if not is_valid_record_id(obj.request_ref):
        return False
    if not isinstance(obj.command_ref, str) or not obj.command_ref.strip():
        return False
    if not isinstance(obj.command_family, str) or not obj.command_family.strip():
        return False
    if not isinstance(obj.command_kind, str) or not obj.command_kind.strip():
        return False
    if not isinstance(obj.owner_route, ValidationBridgeOwnerRouteRef):
        return False
    if not isinstance(obj.subject_ref, ValidationBridgeSubjectRef):
        return False
    if not isinstance(obj.requirement_refs, tuple):
        return False
    for req in obj.requirement_refs:
        if not isinstance(req, ValidationBridgeRequirementRef):
            return False
    if not isinstance(obj.validation_result_ref, ValidationBridgeResultRef):
        return False
    if obj.validation_pipeline_ref is not None and (
        not isinstance(obj.validation_pipeline_ref, str) or not obj.validation_pipeline_ref.strip()
    ):
        return False
    if not isinstance(obj.authority_flags, ValidationIntegrationBridgeAuthorityFlags):
        return False
    if not validate_validation_integration_bridge_authority_flags(obj.authority_flags):
        return False
    return isinstance(obj.metadata, Mapping)


# ---------------------------------------------------------------------------
# Deterministic serialization
# ---------------------------------------------------------------------------


def serialize_validation_integration_bridge_result(
    result: ValidationIntegrationBridgeResult,
) -> dict[str, Any]:
    """Full deterministic serialization of a bridge result."""
    return result.to_dict()


def serialize_validation_integration_bridge_result_visible(
    result: ValidationIntegrationBridgeResult,
) -> dict[str, Any]:
    """Visible-only serialization — omits backend-internal metadata."""
    return {
        "result_ref": result.result_ref,
        "request_ref": result.request_ref,
        "command_ref": result.command_ref,
        "command_family": result.command_family,
        "command_kind": result.command_kind,
        "owner_route": result.owner_route.owner_route,
        "subject_ref": result.subject_ref.to_dict(),
        "requirement_refs": [r.requirement_kind for r in result.requirement_refs],
        "validation_result_ref": result.validation_result_ref.to_dict(),
        "validation_pipeline_ref": result.validation_pipeline_ref,
        "authority_flags": result.authority_flags.to_dict(),
    }
