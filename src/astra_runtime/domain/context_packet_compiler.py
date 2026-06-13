"""PR-6 context packet compiler skeleton — backend-owned visibility-safe packet contract.

This module provides the packet shape definitions and validation infrastructure
for the PR-6 context packet compiler. It defines the first packet
shape (SingleEventNarrationPacket) and supporting constants, exceptions, and
validation functions.

Design constraints:

* No model authority — packets are backend projections, not model outputs.
* No narration generation — this module does not produce narrative text.
* No hidden-information release — packets carry only visibility-safe content.
* No state mutation — packets describe state projections, not mutations.
* No event commitment — packets reference committed events but do not commit them.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence


PACKET_KINDS = frozenset({
    "single_event_narration",
    "no_commit_intent",
    "visible_summary",
})

PACKET_PURPOSE_LABELS = MappingProxyType({
    "single_event_narration": "visibility-safe committed-event narration input",
    "no_commit_intent": "uncommitted player-intent parsing input",
    "visible_summary": "visibility-safe committed-state summary input",
})

NON_AUTHORITY_SEAL = frozenset({
    "backend_projection_not_authoritative_state",
    "no_model_authority",
    "no_hidden_information_release",
    "no_state_mutation",
    "no_event_commitment",
})


class ContextPacketCompilerError(Exception):
    """Base error for context packet compiler operations."""


class InvalidSingleEventNarrationPacketError(ContextPacketCompilerError):
    """Raised when a SingleEventNarrationPacket fails validation."""


class InvalidNoCommitIntentPacketError(ContextPacketCompilerError):
    """Raised when a NoCommitIntentPacket fails validation."""


def _normalize_string_tuple(
    values: Sequence[str] | None,
    name: str,
    error_cls: type[Exception],
) -> tuple[str, ...]:
    """Normalize a sequence of strings into a tuple, rejecting empty strings."""
    if values is None:
        return ()
    if isinstance(values, str):
        raise error_cls(f"{name} must not be a bare string")
    if not isinstance(values, Sequence):
        raise error_cls(f"{name} must be a sequence")
    result: list[str] = []
    for i, item in enumerate(values):
        if not isinstance(item, str) or not item.strip():
            raise error_cls(f"{name}[{i}] must be a non-empty string")
        result.append(item)
    return tuple(result)


def _safe_metadata(
    metadata: Mapping[str, Any] | None,
    error_cls: type[Exception],
) -> Mapping[str, Any]:
    """Deep-copy and freeze metadata into an immutable MappingProxyType."""
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    copied: dict[str, Any] = {}
    for key, value in metadata.items():
        if callable(value):
            raise error_cls("metadata values must not be callable")
        copied[key] = copy.deepcopy(value)
    return MappingProxyType(copied)


@dataclass(frozen=True, kw_only=True)
class SingleEventNarrationPacket:
    """Immutable visibility-safe packet for a single committed event.

    This packet carries the minimum projection needed for narration input.
    It is backend-owned and guarantees no hidden-information release, no
    state mutation authority, and no event commitment authority.
    """

    packet_kind: str
    event_ref: str
    event_kind: str
    visible_fact_refs: tuple[str, ...]
    actor_refs: tuple[str, ...] = field(default_factory=tuple)
    target_refs: tuple[str, ...] = field(default_factory=tuple)
    sensory_cues: tuple[str, ...] = field(default_factory=tuple)
    forbidden_claims: tuple[str, ...] = field(default_factory=tuple)
    non_authority_seal: tuple[str, ...] = field(default_factory=tuple)
    hidden_information_excluded: bool = True
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass.

        Uses object.__setattr__ because the dataclass is frozen.
        """
        error_cls = InvalidSingleEventNarrationPacketError

        # Validate and normalize packet_kind
        if not isinstance(self.packet_kind, str) or not self.packet_kind.strip():
            raise error_cls("packet_kind must be a non-empty string")
        if self.packet_kind != "single_event_narration":
            raise error_cls(
                f"packet_kind must be 'single_event_narration', got: {self.packet_kind!r}"
            )

        # Validate event_ref
        if not isinstance(self.event_ref, str) or not self.event_ref.strip():
            raise error_cls("event_ref must be a non-empty string")

        # Validate event_kind
        if not isinstance(self.event_kind, str) or not self.event_kind.strip():
            raise error_cls("event_kind must be a non-empty string")

        # Validate hidden_information_excluded — must be exactly True
        if self.hidden_information_excluded is not True:
            raise error_cls("hidden_information_excluded must be exactly True")

        # Normalize visible_fact_refs (reject empty strings inside, must be non-empty)
        normalized_visible = _normalize_string_tuple(
            self.visible_fact_refs, "visible_fact_refs", error_cls
        )
        if len(normalized_visible) == 0:
            raise error_cls("visible_fact_refs must not be empty")

        # Normalize tuple fields
        safe_actor_refs = _normalize_string_tuple(
            self.actor_refs, "actor_refs", error_cls
        )
        safe_target_refs = _normalize_string_tuple(
            self.target_refs, "target_refs", error_cls
        )
        safe_sensory_cues = _normalize_string_tuple(
            self.sensory_cues, "sensory_cues", error_cls
        )
        safe_forbidden_claims = _normalize_string_tuple(
            self.forbidden_claims, "forbidden_claims", error_cls
        )

        # Normalize non_authority_seal — default to sorted NON_AUTHORITY_SEAL if empty
        if len(self.non_authority_seal) == 0:
            safe_non_authority_seal = tuple(sorted(NON_AUTHORITY_SEAL))
        else:
            safe_non_authority_seal = _normalize_string_tuple(
                self.non_authority_seal, "non_authority_seal", error_cls
            )

        # Deep-copy and freeze metadata
        safe_metadata = _safe_metadata(self.metadata, error_cls)

        # Use object.__setattr__ to update frozen fields
        object.__setattr__(self, "visible_fact_refs", normalized_visible)
        object.__setattr__(self, "actor_refs", safe_actor_refs)
        object.__setattr__(self, "target_refs", safe_target_refs)
        object.__setattr__(self, "sensory_cues", safe_sensory_cues)
        object.__setattr__(self, "forbidden_claims", safe_forbidden_claims)
        object.__setattr__(self, "non_authority_seal", safe_non_authority_seal)
        object.__setattr__(self, "metadata", safe_metadata)

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic plain-dict serialization."""
        return {
            "packet_kind": self.packet_kind,
            "event_ref": self.event_ref,
            "event_kind": self.event_kind,
            "visible_fact_refs": list(self.visible_fact_refs),
            "actor_refs": list(self.actor_refs),
            "target_refs": list(self.target_refs),
            "sensory_cues": list(self.sensory_cues),
            "forbidden_claims": list(self.forbidden_claims),
            "non_authority_seal": list(self.non_authority_seal),
            "hidden_information_excluded": self.hidden_information_excluded,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class NoCommitIntentPacket:
    """Immutable packet representing uncommitted player intent input.

    This packet carries parsing/preview data for player intent. It must not
    imply resolution, event commitment, state mutation, hidden-information
    release, or narration generation. It is backend-owned and carries no
    authority beyond its declared purpose.
    """

    packet_kind: str
    intent_ref: str
    actor_ref: str
    proposed_action_kind: str
    intent_timestamp: str
    target_refs: tuple[str, ...] = field(default_factory=tuple)
    declared_resource_refs: tuple[str, ...] = field(default_factory=tuple)
    declared_cost_refs: tuple[str, ...] = field(default_factory=tuple)
    visible_context_refs: tuple[str, ...] = field(default_factory=tuple)
    confirmation_required: bool = True
    hidden_information_excluded: bool = True
    no_commit_marker: bool = True
    non_authority_seal: tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass.

        Uses object.__setattr__ because the dataclass is frozen.
        """
        error_cls = InvalidNoCommitIntentPacketError

        # Validate and normalize packet_kind
        if not isinstance(self.packet_kind, str) or not self.packet_kind.strip():
            raise error_cls("packet_kind must be a non-empty string")
        if self.packet_kind != "no_commit_intent":
            raise error_cls(
                f"packet_kind must be 'no_commit_intent', got: {self.packet_kind!r}"
            )

        # Validate intent_ref
        if not isinstance(self.intent_ref, str) or not self.intent_ref.strip():
            raise error_cls("intent_ref must be a non-empty string")

        # Validate actor_ref
        if not isinstance(self.actor_ref, str) or not self.actor_ref.strip():
            raise error_cls("actor_ref must be a non-empty string")

        # Validate proposed_action_kind
        if not isinstance(self.proposed_action_kind, str) or not self.proposed_action_kind.strip():
            raise error_cls("proposed_action_kind must be a non-empty string")

        # Validate intent_timestamp
        if not isinstance(self.intent_timestamp, str) or not self.intent_timestamp.strip():
            raise error_cls("intent_timestamp must be a non-empty string")

        # Validate confirmation_required — must be a bool
        if not isinstance(self.confirmation_required, bool):
            raise error_cls("confirmation_required must be a bool")

        # Validate hidden_information_excluded — must be exactly True
        if self.hidden_information_excluded is not True:
            raise error_cls("hidden_information_excluded must be exactly True")

        # Validate no_commit_marker — must be exactly True
        if self.no_commit_marker is not True:
            raise error_cls("no_commit_marker must be exactly True")

        # Normalize tuple fields
        safe_target_refs = _normalize_string_tuple(
            self.target_refs, "target_refs", error_cls
        )
        safe_declared_resource_refs = _normalize_string_tuple(
            self.declared_resource_refs, "declared_resource_refs", error_cls
        )
        safe_declared_cost_refs = _normalize_string_tuple(
            self.declared_cost_refs, "declared_cost_refs", error_cls
        )
        safe_visible_context_refs = _normalize_string_tuple(
            self.visible_context_refs, "visible_context_refs", error_cls
        )

        # Normalize non_authority_seal — default to sorted NON_AUTHORITY_SEAL if empty
        if len(self.non_authority_seal) == 0:
            safe_non_authority_seal = tuple(sorted(NON_AUTHORITY_SEAL))
        else:
            safe_non_authority_seal = _normalize_string_tuple(
                self.non_authority_seal, "non_authority_seal", error_cls
            )

        # Deep-copy and freeze metadata
        safe_metadata = _safe_metadata(self.metadata, error_cls)

        # Use object.__setattr__ to update frozen fields
        object.__setattr__(self, "target_refs", safe_target_refs)
        object.__setattr__(self, "declared_resource_refs", safe_declared_resource_refs)
        object.__setattr__(self, "declared_cost_refs", safe_declared_cost_refs)
        object.__setattr__(self, "visible_context_refs", safe_visible_context_refs)
        object.__setattr__(self, "non_authority_seal", safe_non_authority_seal)
        object.__setattr__(self, "metadata", safe_metadata)

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic plain-dict serialization."""
        return {
            "packet_kind": self.packet_kind,
            "intent_ref": self.intent_ref,
            "actor_ref": self.actor_ref,
            "proposed_action_kind": self.proposed_action_kind,
            "intent_timestamp": self.intent_timestamp,
            "target_refs": list(self.target_refs),
            "declared_resource_refs": list(self.declared_resource_refs),
            "declared_cost_refs": list(self.declared_cost_refs),
            "visible_context_refs": list(self.visible_context_refs),
            "confirmation_required": self.confirmation_required,
            "hidden_information_excluded": self.hidden_information_excluded,
            "no_commit_marker": self.no_commit_marker,
            "non_authority_seal": list(self.non_authority_seal),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_no_commit_intent_packet(
    *,
    packet_kind: str = "no_commit_intent",
    intent_ref: str,
    actor_ref: str,
    proposed_action_kind: str,
    intent_timestamp: str,
    target_refs: Sequence[str] | None = None,
    declared_resource_refs: Sequence[str] | None = None,
    declared_cost_refs: Sequence[str] | None = None,
    visible_context_refs: Sequence[str] | None = None,
    confirmation_required: bool = True,
    hidden_information_excluded: bool = True,
    no_commit_marker: bool = True,
    non_authority_seal: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> NoCommitIntentPacket:
    """Construct and validate a NoCommitIntentPacket.

    Raises InvalidNoCommitIntentPacketError on invalid input.

    This is the canonical public construction helper. It pre-validates
    inputs and delegates final normalization to __post_init__.
    """
    error_cls = InvalidNoCommitIntentPacketError

    # Pre-validate packet_kind
    if not isinstance(packet_kind, str) or not packet_kind.strip():
        raise error_cls("packet_kind must be a non-empty string")
    if packet_kind != "no_commit_intent":
        raise error_cls(
            f"packet_kind must be 'no_commit_intent', got: {packet_kind!r}"
        )

    # Pre-validate intent_ref
    if not isinstance(intent_ref, str) or not intent_ref.strip():
        raise error_cls("intent_ref must be a non-empty string")

    # Pre-validate actor_ref
    if not isinstance(actor_ref, str) or not actor_ref.strip():
        raise error_cls("actor_ref must be a non-empty string")

    # Pre-validate proposed_action_kind
    if not isinstance(proposed_action_kind, str) or not proposed_action_kind.strip():
        raise error_cls("proposed_action_kind must be a non-empty string")

    # Pre-validate intent_timestamp
    if not isinstance(intent_timestamp, str) or not intent_timestamp.strip():
        raise error_cls("intent_timestamp must be a non-empty string")

    # Pre-validate optional tuple fields are sequences (not bare strings)
    for field_name, field_value in (
        ("target_refs", target_refs),
        ("declared_resource_refs", declared_resource_refs),
        ("declared_cost_refs", declared_cost_refs),
        ("visible_context_refs", visible_context_refs),
        ("non_authority_seal", non_authority_seal),
    ):
        if field_value is not None:
            if isinstance(field_value, str):
                raise error_cls(f"{field_name} must not be a bare string")
            if not isinstance(field_value, Sequence):
                raise error_cls(f"{field_name} must be a sequence")

    # Pre-validate metadata type if provided
    if metadata is not None and not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")

    # Build kwargs for direct construction — __post_init__ handles normalization
    kwargs: dict[str, Any] = {
        "packet_kind": packet_kind,
        "intent_ref": intent_ref,
        "actor_ref": actor_ref,
        "proposed_action_kind": proposed_action_kind,
        "intent_timestamp": intent_timestamp,
        "target_refs": list(target_refs) if target_refs is not None else (),
        "declared_resource_refs": list(declared_resource_refs) if declared_resource_refs is not None else (),
        "declared_cost_refs": list(declared_cost_refs) if declared_cost_refs is not None else (),
        "visible_context_refs": list(visible_context_refs) if visible_context_refs is not None else (),
        "confirmation_required": confirmation_required,
        "hidden_information_excluded": hidden_information_excluded,
        "no_commit_marker": no_commit_marker,
        "non_authority_seal": list(non_authority_seal) if non_authority_seal is not None else (),
        "metadata": dict(metadata) if metadata is not None else {},
    }

    return NoCommitIntentPacket(**kwargs)


def validate_no_commit_intent_packet(value: Any) -> bool:
    """Return True for a valid NoCommitIntentPacket instance.

    Raises InvalidNoCommitIntentPacketError for invalid values.
    """
    error_cls = InvalidNoCommitIntentPacketError

    if not isinstance(value, NoCommitIntentPacket):
        raise error_cls("value must be a NoCommitIntentPacket instance")

    # Validate packet_kind
    if not isinstance(value.packet_kind, str) or not value.packet_kind.strip():
        raise error_cls("packet_kind must be a non-empty string")
    if value.packet_kind != "no_commit_intent":
        raise error_cls(
            f"packet_kind must be 'no_commit_intent', got: {value.packet_kind!r}"
        )

    # Validate intent_ref
    if not isinstance(value.intent_ref, str) or not value.intent_ref.strip():
        raise error_cls("intent_ref must be a non-empty string")

    # Validate actor_ref
    if not isinstance(value.actor_ref, str) or not value.actor_ref.strip():
        raise error_cls("actor_ref must be a non-empty string")

    # Validate proposed_action_kind
    if not isinstance(value.proposed_action_kind, str) or not value.proposed_action_kind.strip():
        raise error_cls("proposed_action_kind must be a non-empty string")

    # Validate intent_timestamp
    if not isinstance(value.intent_timestamp, str) or not value.intent_timestamp.strip():
        raise error_cls("intent_timestamp must be a non-empty string")

    # Validate tuple fields
    for field_name, field_value in (
        ("target_refs", value.target_refs),
        ("declared_resource_refs", value.declared_resource_refs),
        ("declared_cost_refs", value.declared_cost_refs),
        ("visible_context_refs", value.visible_context_refs),
    ):
        if not isinstance(field_value, tuple):
            raise error_cls(f"{field_name} must be a tuple")
        for item in field_value:
            if not isinstance(item, str) or not item.strip():
                raise error_cls(f"{field_name} items must be non-empty strings")

    # Validate non_authority_seal — must be non-empty tuple of non-empty strings
    if not isinstance(value.non_authority_seal, tuple):
        raise error_cls("non_authority_seal must be a tuple")
    if len(value.non_authority_seal) == 0:
        raise error_cls("non_authority_seal must not be empty")
    for item in value.non_authority_seal:
        if not isinstance(item, str) or not item.strip():
            raise error_cls("non_authority_seal items must be non-empty strings")

    # Validate confirmation_required — must be a bool
    if not isinstance(value.confirmation_required, bool):
        raise error_cls("confirmation_required must be a bool")

    # Validate hidden_information_excluded — must be exactly True
    if value.hidden_information_excluded is not True:
        raise error_cls("hidden_information_excluded must be exactly True")

    # Validate no_commit_marker — must be exactly True
    if value.no_commit_marker is not True:
        raise error_cls("no_commit_marker must be exactly True")

    # Validate metadata is MappingProxyType
    if not isinstance(value.metadata, MappingProxyType):
        raise error_cls("metadata must be a MappingProxyType")

    return True


def create_single_event_narration_packet(
    *,
    packet_kind: str = "single_event_narration",
    event_ref: str,
    event_kind: str,
    visible_fact_refs: Sequence[str],
    actor_refs: Sequence[str] | None = None,
    target_refs: Sequence[str] | None = None,
    sensory_cues: Sequence[str] | None = None,
    forbidden_claims: Sequence[str] | None = None,
    non_authority_seal: Sequence[str] | None = None,
    hidden_information_excluded: bool = True,
    metadata: Mapping[str, Any] | None = None,
) -> SingleEventNarrationPacket:
    """Construct and validate a SingleEventNarrationPacket.

    Raises InvalidSingleEventNarrationPacketError on invalid input.

    This is the canonical public construction helper. It pre-validates
    inputs and delegates final normalization to __post_init__.
    """
    error_cls = InvalidSingleEventNarrationPacketError

    # Pre-validate packet_kind
    if not isinstance(packet_kind, str) or not packet_kind.strip():
        raise error_cls("packet_kind must be a non-empty string")
    if packet_kind != "single_event_narration":
        raise error_cls(
            f"packet_kind must be 'single_event_narration', got: {packet_kind!r}"
        )

    # Pre-validate event_ref
    if not isinstance(event_ref, str) or not event_ref.strip():
        raise error_cls("event_ref must be a non-empty string")

    # Pre-validate event_kind
    if not isinstance(event_kind, str) or not event_kind.strip():
        raise error_cls("event_kind must be a non-empty string")

    # Pre-validate visible_fact_refs — must be non-empty
    if not isinstance(visible_fact_refs, Sequence) or isinstance(visible_fact_refs, str):
        raise error_cls("visible_fact_refs must be a sequence")
    if len(visible_fact_refs) == 0:
        raise error_cls("visible_fact_refs must not be empty")

    # Pre-validate hidden_information_excluded — must be exactly True
    if hidden_information_excluded is not True:
        raise error_cls("hidden_information_excluded must be exactly True")

    # Pre-validate optional tuple fields are sequences (not bare strings)
    for field_name, field_value in (
        ("actor_refs", actor_refs),
        ("target_refs", target_refs),
        ("sensory_cues", sensory_cues),
        ("forbidden_claims", forbidden_claims),
        ("non_authority_seal", non_authority_seal),
    ):
        if field_value is not None:
            if isinstance(field_value, str):
                raise error_cls(f"{field_name} must not be a bare string")
            if not isinstance(field_value, Sequence):
                raise error_cls(f"{field_name} must be a sequence")

    # Pre-validate metadata type if provided
    if metadata is not None and not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")

    # Build kwargs for direct construction — __post_init__ handles normalization
    # For non_authority_seal, pass () if None so __post_init__ can default it
    kwargs: dict[str, Any] = {
        "packet_kind": packet_kind,
        "event_ref": event_ref,
        "event_kind": event_kind,
        "visible_fact_refs": list(visible_fact_refs),
        "actor_refs": list(actor_refs) if actor_refs is not None else (),
        "target_refs": list(target_refs) if target_refs is not None else (),
        "sensory_cues": list(sensory_cues) if sensory_cues is not None else (),
        "forbidden_claims": (
            list(forbidden_claims) if forbidden_claims is not None else ()
        ),
        "non_authority_seal": (
            list(non_authority_seal) if non_authority_seal is not None else ()
        ),
        "hidden_information_excluded": hidden_information_excluded,
        "metadata": dict(metadata) if metadata is not None else {},
    }

    return SingleEventNarrationPacket(**kwargs)


def validate_single_event_narration_packet(value: Any) -> bool:
    """Return True for a valid SingleEventNarrationPacket instance.

    Raises InvalidSingleEventNarrationPacketError for invalid values.
    """
    error_cls = InvalidSingleEventNarrationPacketError

    if not isinstance(value, SingleEventNarrationPacket):
        raise error_cls("value must be a SingleEventNarrationPacket instance")

    # Validate packet_kind
    if not isinstance(value.packet_kind, str) or not value.packet_kind.strip():
        raise error_cls("packet_kind must be a non-empty string")
    if value.packet_kind != "single_event_narration":
        raise error_cls(
            f"packet_kind must be 'single_event_narration', got: {value.packet_kind!r}"
        )

    # Validate event_ref
    if not isinstance(value.event_ref, str) or not value.event_ref.strip():
        raise error_cls("event_ref must be a non-empty string")

    # Validate event_kind
    if not isinstance(value.event_kind, str) or not value.event_kind.strip():
        raise error_cls("event_kind must be a non-empty string")

    # Validate visible_fact_refs — must be non-empty tuple of non-empty strings
    if not isinstance(value.visible_fact_refs, tuple):
        raise error_cls("visible_fact_refs must be a tuple")
    if len(value.visible_fact_refs) == 0:
        raise error_cls("visible_fact_refs must not be empty")
    for item in value.visible_fact_refs:
        if not isinstance(item, str) or not item.strip():
            raise error_cls("visible_fact_refs items must be non-empty strings")

    # Validate tuple fields
    for field_name, field_value in (
        ("actor_refs", value.actor_refs),
        ("target_refs", value.target_refs),
        ("sensory_cues", value.sensory_cues),
        ("forbidden_claims", value.forbidden_claims),
    ):
        if not isinstance(field_value, tuple):
            raise error_cls(f"{field_name} must be a tuple")
        for item in field_value:
            if not isinstance(item, str) or not item.strip():
                raise error_cls(f"{field_name} items must be non-empty strings")

    # Validate non_authority_seal — must be non-empty tuple of non-empty strings
    if not isinstance(value.non_authority_seal, tuple):
        raise error_cls("non_authority_seal must be a tuple")
    if len(value.non_authority_seal) == 0:
        raise error_cls("non_authority_seal must not be empty")
    for item in value.non_authority_seal:
        if not isinstance(item, str) or not item.strip():
            raise error_cls("non_authority_seal items must be non-empty strings")

    # Validate hidden_information_excluded — must be exactly True
    if value.hidden_information_excluded is not True:
        raise error_cls("hidden_information_excluded must be exactly True")

    # Validate metadata is MappingProxyType
    if not isinstance(value.metadata, MappingProxyType):
        raise error_cls("metadata must be a MappingProxyType")

    return True


def validate_packet_kind(kind: str) -> bool:
    """Return True if kind is a known packet kind.

    Raises ContextPacketCompilerError for unknown values.
    """
    if not isinstance(kind, str) or not kind.strip():
        raise ContextPacketCompilerError("packet kind must be a non-empty string")
    if kind not in PACKET_KINDS:
        raise ContextPacketCompilerError(
            f"unknown packet kind: {kind!r}; "
            f"expected one of {sorted(PACKET_KINDS)}"
        )
    return True
