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
import json
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


class ContextPacketSelectionError(ContextPacketCompilerError):
    """Raised for selection, dispatch, or serialization failures."""


class InvalidSingleEventNarrationPacketError(ContextPacketCompilerError):
    """Raised when a SingleEventNarrationPacket fails validation."""


class InvalidNoCommitIntentPacketError(ContextPacketCompilerError):
    """Raised when a NoCommitIntentPacket fails validation."""


class InvalidVisibleSummaryPacketError(ContextPacketCompilerError):
    """Raised when a VisibleSummaryPacket fails validation."""


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




@dataclass(frozen=True, kw_only=True)
class VisibleSummaryPacket:
    """Immutable visibility-safe packet for a committed-state summary.

    This packet carries a visibility-safe summary of already-committed
    visible facts and state for narrator context. It must not expose
    hidden information, alter state, commit events, resolve uncertainty,
    execute chance, or generate narration.
    """

    packet_kind: str
    summary_ref: str
    summary_scope: str
    summary_timestamp: str
    visible_fact_refs: tuple[str, ...]
    actor_refs: tuple[str, ...] = field(default_factory=tuple)
    location_refs: tuple[str, ...] = field(default_factory=tuple)
    faction_refs: tuple[str, ...] = field(default_factory=tuple)
    item_refs: tuple[str, ...] = field(default_factory=tuple)
    condition_refs: tuple[str, ...] = field(default_factory=tuple)
    unresolved_visible_refs: tuple[str, ...] = field(default_factory=tuple)
    forbidden_claims: tuple[str, ...] = field(default_factory=tuple)
    hidden_information_excluded: bool = True
    committed_state_only: bool = True
    non_authority_seal: tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass.

        Uses object.__setattr__ because the dataclass is frozen.
        """
        error_cls = InvalidVisibleSummaryPacketError

        # Validate and normalize packet_kind
        if not isinstance(self.packet_kind, str) or not self.packet_kind.strip():
            raise error_cls("packet_kind must be a non-empty string")
        if self.packet_kind != "visible_summary":
            raise error_cls(
                f"packet_kind must be 'visible_summary', got: {self.packet_kind!r}"
            )

        # Validate summary_ref
        if not isinstance(self.summary_ref, str) or not self.summary_ref.strip():
            raise error_cls("summary_ref must be a non-empty string")

        # Validate summary_scope
        if not isinstance(self.summary_scope, str) or not self.summary_scope.strip():
            raise error_cls("summary_scope must be a non-empty string")

        # Validate summary_timestamp
        if not isinstance(self.summary_timestamp, str) or not self.summary_timestamp.strip():
            raise error_cls("summary_timestamp must be a non-empty string")

        # Validate hidden_information_excluded — must be exactly True
        if self.hidden_information_excluded is not True:
            raise error_cls("hidden_information_excluded must be exactly True")

        # Validate committed_state_only — must be exactly True
        if self.committed_state_only is not True:
            raise error_cls("committed_state_only must be exactly True")

        # Normalize visible_fact_refs (must be non-empty)
        normalized_visible = _normalize_string_tuple(
            self.visible_fact_refs, "visible_fact_refs", error_cls
        )
        if len(normalized_visible) == 0:
            raise error_cls("visible_fact_refs must not be empty")

        # Normalize tuple fields
        safe_actor_refs = _normalize_string_tuple(
            self.actor_refs, "actor_refs", error_cls
        )
        safe_location_refs = _normalize_string_tuple(
            self.location_refs, "location_refs", error_cls
        )
        safe_faction_refs = _normalize_string_tuple(
            self.faction_refs, "faction_refs", error_cls
        )
        safe_item_refs = _normalize_string_tuple(
            self.item_refs, "item_refs", error_cls
        )
        safe_condition_refs = _normalize_string_tuple(
            self.condition_refs, "condition_refs", error_cls
        )
        safe_unresolved_visible_refs = _normalize_string_tuple(
            self.unresolved_visible_refs, "unresolved_visible_refs", error_cls
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
        object.__setattr__(self, "location_refs", safe_location_refs)
        object.__setattr__(self, "faction_refs", safe_faction_refs)
        object.__setattr__(self, "item_refs", safe_item_refs)
        object.__setattr__(self, "condition_refs", safe_condition_refs)
        object.__setattr__(self, "unresolved_visible_refs", safe_unresolved_visible_refs)
        object.__setattr__(self, "forbidden_claims", safe_forbidden_claims)
        object.__setattr__(self, "non_authority_seal", safe_non_authority_seal)
        object.__setattr__(self, "metadata", safe_metadata)

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic plain-dict serialization."""
        return {
            "packet_kind": self.packet_kind,
            "summary_ref": self.summary_ref,
            "summary_scope": self.summary_scope,
            "summary_timestamp": self.summary_timestamp,
            "visible_fact_refs": list(self.visible_fact_refs),
            "actor_refs": list(self.actor_refs),
            "location_refs": list(self.location_refs),
            "faction_refs": list(self.faction_refs),
            "item_refs": list(self.item_refs),
            "condition_refs": list(self.condition_refs),
            "unresolved_visible_refs": list(self.unresolved_visible_refs),
            "forbidden_claims": list(self.forbidden_claims),
            "hidden_information_excluded": self.hidden_information_excluded,
            "committed_state_only": self.committed_state_only,
            "non_authority_seal": list(self.non_authority_seal),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_visible_summary_packet(
    *,
    packet_kind: str = "visible_summary",
    summary_ref: str,
    summary_scope: str,
    summary_timestamp: str,
    visible_fact_refs: Sequence[str],
    actor_refs: Sequence[str] | None = None,
    location_refs: Sequence[str] | None = None,
    faction_refs: Sequence[str] | None = None,
    item_refs: Sequence[str] | None = None,
    condition_refs: Sequence[str] | None = None,
    unresolved_visible_refs: Sequence[str] | None = None,
    forbidden_claims: Sequence[str] | None = None,
    hidden_information_excluded: bool = True,
    committed_state_only: bool = True,
    non_authority_seal: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> VisibleSummaryPacket:
    """Construct and validate a VisibleSummaryPacket.

    Raises InvalidVisibleSummaryPacketError on invalid input.

    This is the canonical public construction helper. It pre-validates
    inputs and delegates final normalization to __post_init__.
    """
    error_cls = InvalidVisibleSummaryPacketError

    # Pre-validate packet_kind
    if not isinstance(packet_kind, str) or not packet_kind.strip():
        raise error_cls("packet_kind must be a non-empty string")
    if packet_kind != "visible_summary":
        raise error_cls(
            f"packet_kind must be 'visible_summary', got: {packet_kind!r}"
        )

    # Pre-validate summary_ref
    if not isinstance(summary_ref, str) or not summary_ref.strip():
        raise error_cls("summary_ref must be a non-empty string")

    # Pre-validate summary_scope
    if not isinstance(summary_scope, str) or not summary_scope.strip():
        raise error_cls("summary_scope must be a non-empty string")

    # Pre-validate summary_timestamp
    if not isinstance(summary_timestamp, str) or not summary_timestamp.strip():
        raise error_cls("summary_timestamp must be a non-empty string")

    # Pre-validate visible_fact_refs — must be non-empty
    if not isinstance(visible_fact_refs, Sequence) or isinstance(visible_fact_refs, str):
        raise error_cls("visible_fact_refs must be a sequence")
    if len(visible_fact_refs) == 0:
        raise error_cls("visible_fact_refs must not be empty")

    # Pre-validate hidden_information_excluded — must be exactly True
    if hidden_information_excluded is not True:
        raise error_cls("hidden_information_excluded must be exactly True")

    # Pre-validate committed_state_only — must be exactly True
    if committed_state_only is not True:
        raise error_cls("committed_state_only must be exactly True")

    # Pre-validate optional tuple fields are sequences (not bare strings)
    for field_name, field_value in (
        ("actor_refs", actor_refs),
        ("location_refs", location_refs),
        ("faction_refs", faction_refs),
        ("item_refs", item_refs),
        ("condition_refs", condition_refs),
        ("unresolved_visible_refs", unresolved_visible_refs),
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
    kwargs: dict[str, Any] = {
        "packet_kind": packet_kind,
        "summary_ref": summary_ref,
        "summary_scope": summary_scope,
        "summary_timestamp": summary_timestamp,
        "visible_fact_refs": list(visible_fact_refs),
        "actor_refs": list(actor_refs) if actor_refs is not None else (),
        "location_refs": list(location_refs) if location_refs is not None else (),
        "faction_refs": list(faction_refs) if faction_refs is not None else (),
        "item_refs": list(item_refs) if item_refs is not None else (),
        "condition_refs": list(condition_refs) if condition_refs is not None else (),
        "unresolved_visible_refs": (
            list(unresolved_visible_refs) if unresolved_visible_refs is not None else ()
        ),
        "forbidden_claims": (
            list(forbidden_claims) if forbidden_claims is not None else ()
        ),
        "hidden_information_excluded": hidden_information_excluded,
        "committed_state_only": committed_state_only,
        "non_authority_seal": (
            list(non_authority_seal) if non_authority_seal is not None else ()
        ),
        "metadata": dict(metadata) if metadata is not None else {},
    }

    return VisibleSummaryPacket(**kwargs)


def validate_visible_summary_packet(value: Any) -> bool:
    """Return True for a valid VisibleSummaryPacket instance.

    Raises InvalidVisibleSummaryPacketError for invalid values.
    """
    error_cls = InvalidVisibleSummaryPacketError

    if not isinstance(value, VisibleSummaryPacket):
        raise error_cls("value must be a VisibleSummaryPacket instance")

    # Validate packet_kind
    if not isinstance(value.packet_kind, str) or not value.packet_kind.strip():
        raise error_cls("packet_kind must be a non-empty string")
    if value.packet_kind != "visible_summary":
        raise error_cls(
            f"packet_kind must be 'visible_summary', got: {value.packet_kind!r}"
        )

    # Validate summary_ref
    if not isinstance(value.summary_ref, str) or not value.summary_ref.strip():
        raise error_cls("summary_ref must be a non-empty string")

    # Validate summary_scope
    if not isinstance(value.summary_scope, str) or not value.summary_scope.strip():
        raise error_cls("summary_scope must be a non-empty string")

    # Validate summary_timestamp
    if not isinstance(value.summary_timestamp, str) or not value.summary_timestamp.strip():
        raise error_cls("summary_timestamp must be a non-empty string")

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
        ("location_refs", value.location_refs),
        ("faction_refs", value.faction_refs),
        ("item_refs", value.item_refs),
        ("condition_refs", value.condition_refs),
        ("unresolved_visible_refs", value.unresolved_visible_refs),
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

    # Validate committed_state_only — must be exactly True
    if value.committed_state_only is not True:
        raise error_cls("committed_state_only must be exactly True")

    # Validate metadata is MappingProxyType
    if not isinstance(value.metadata, MappingProxyType):
        raise error_cls("metadata must be a MappingProxyType")

    return True


# ---------------------------------------------------------------------------
# Slice 4 — context packet selection and serialization helpers
# ---------------------------------------------------------------------------

_KNOWN_PACKET_TYPES = frozenset({
    SingleEventNarrationPacket,
    NoCommitIntentPacket,
    VisibleSummaryPacket,
})

_PACKET_KIND_TO_CLASS: dict[str, type] = {
    "single_event_narration": SingleEventNarrationPacket,
    "no_commit_intent": NoCommitIntentPacket,
    "visible_summary": VisibleSummaryPacket,
}


def get_context_packet_kind(value: Any) -> str:
    """Return the packet_kind string for a known context packet instance.

    Accepts exactly one of SingleEventNarrationPacket, NoCommitIntentPacket,
    or VisibleSummaryPacket. Rejects all other values.
    """
    for cls in _KNOWN_PACKET_TYPES:
        if isinstance(value, cls):
            return value.packet_kind
    raise ContextPacketSelectionError(
        f"unsupported context packet type: {type(value)!r}"
    )


def select_context_packet_validator(kind: str) -> Any:
    """Return the validator function for the given known packet kind.

    Does not call the validator. Raises ContextPacketSelectionError
    for empty, non-string, or unknown kinds.
    """
    if not isinstance(kind, str) or not kind.strip():
        raise ContextPacketSelectionError(
            "packet kind must be a non-empty string"
        )
    if kind not in PACKET_KINDS:
        raise ContextPacketSelectionError(
            f"unknown packet kind: {kind!r}; "
            f"expected one of {sorted(PACKET_KINDS)}"
        )
    _validator_map: dict[str, Any] = {
        "single_event_narration": validate_single_event_narration_packet,
        "no_commit_intent": validate_no_commit_intent_packet,
        "visible_summary": validate_visible_summary_packet,
    }
    return _validator_map[kind]


def select_context_packet_serializer(kind: str) -> Any:
    """Return a callable that serializes a matching packet via to_dict().

    Does not serialize anything by itself. Raises ContextPacketSelectionError
    for empty, non-string, or unknown kinds.
    """
    if not isinstance(kind, str) or not kind.strip():
        raise ContextPacketSelectionError(
            "packet kind must be a non-empty string"
        )
    if kind not in PACKET_KINDS:
        raise ContextPacketSelectionError(
            f"unknown packet kind: {kind!r}; "
            f"expected one of {sorted(PACKET_KINDS)}"
        )

    def _serialize(packet: Any) -> dict[str, Any]:
        return packet.to_dict()

    return _serialize


def validate_context_packet(value: Any) -> bool:
    """Return True for a valid known context packet instance.

    Uses get_context_packet_kind to select the type, then delegates
    to the matching packet-specific validator. Raises
    ContextPacketSelectionError for unsupported types. Allows
    packet-specific validators to raise their own errors.
    """
    kind = get_context_packet_kind(value)
    validator = select_context_packet_validator(kind)
    return validator(value)


def serialize_context_packet(value: Any) -> dict[str, Any]:
    """Return a deterministic deep-copied plain-dict serialization.

    Validates the packet before serialization. Returns a deep copy
    so mutating the result cannot affect the original packet metadata.
    Raises ContextPacketSelectionError for unsupported values. Allows
    packet-specific validators to raise their own errors.
    """
    validate_context_packet(value)
    raw = value.to_dict()
    return copy.deepcopy(raw)


# ---------------------------------------------------------------------------
# Slice 5 — context packet single-packet assembly shell
# ---------------------------------------------------------------------------

FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS = frozenset({
    "runtime_state",
    "state_store",
    "event_ledger",
    "hidden_state",
    "hidden_fact_refs",
    "hidden_payload",
    "secret_refs",
    "unrevealed_refs",
    "state_delta",
    "commit_event",
    "mutation",
    "rng_result",
    "roll_result",
    "model_output",
    "narration_output",
})


class ContextPacketAssemblyError(ContextPacketCompilerError):
    """Raised for assembly-request and assembly-dispatch failures."""


@dataclass(frozen=True, kw_only=True)
class ContextPacketAssemblyRequest:
    """Frozen request to assemble exactly one context packet from an explicit payload mapping.

    This is a backend-owned, deterministic, stateless assembly request.
    It must not read runtime state, compile packets from stores, aggregate
    packets, execute transactions, call models, or generate narration.
    """

    request_ref: str
    packet_kind: str
    packet_payload: Mapping[str, Any]
    assembly_timestamp: str
    hidden_information_excluded: bool = True
    explicit_payload_only: bool = True
    no_runtime_state_source: bool = True
    non_authority_seal: tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass.

        Uses object.__setattr__ because the dataclass is frozen.
        """
        error_cls = ContextPacketAssemblyError

        # Validate request_ref
        if not isinstance(self.request_ref, str) or not self.request_ref.strip():
            raise error_cls("request_ref must be a non-empty string")

        # Validate assembly_timestamp
        if not isinstance(self.assembly_timestamp, str) or not self.assembly_timestamp.strip():
            raise error_cls("assembly_timestamp must be a non-empty string")

        # Validate packet_kind is a known kind
        if not isinstance(self.packet_kind, str) or not self.packet_kind.strip():
            raise error_cls("packet_kind must be a non-empty string")
        if self.packet_kind not in PACKET_KINDS:
            raise error_cls(
                f"unknown packet_kind: {self.packet_kind!r}; "
                f"expected one of {sorted(PACKET_KINDS)}"
            )

        # Validate packet_payload is a mapping
        if not isinstance(self.packet_payload, Mapping):
            raise error_cls("packet_payload must be a mapping")

        # Check for forbidden payload keys
        payload_keys = set(self.packet_payload.keys())
        forbidden_found = payload_keys & FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS
        if forbidden_found:
            raise error_cls(
                f"packet_payload contains forbidden keys: {sorted(forbidden_found)}"
            )

        # Require safety flags are exactly True
        if self.hidden_information_excluded is not True:
            raise error_cls("hidden_information_excluded must be exactly True")
        if self.explicit_payload_only is not True:
            raise error_cls("explicit_payload_only must be exactly True")
        if self.no_runtime_state_source is not True:
            raise error_cls("no_runtime_state_source must be exactly True")

        # Deep-copy and freeze packet_payload
        safe_payload: dict[str, Any] = {}
        for key, value in self.packet_payload.items():
            safe_payload[key] = copy.deepcopy(value)
        object.__setattr__(self, "packet_payload", MappingProxyType(safe_payload))

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
        object.__setattr__(self, "non_authority_seal", safe_non_authority_seal)
        object.__setattr__(self, "metadata", safe_metadata)


def create_context_packet_assembly_request(
    *,
    request_ref: str,
    packet_kind: str,
    packet_payload: Mapping[str, Any],
    assembly_timestamp: str,
    hidden_information_excluded: bool = True,
    explicit_payload_only: bool = True,
    no_runtime_state_source: bool = True,
    non_authority_seal: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ContextPacketAssemblyRequest:
    """Construct and validate a ContextPacketAssemblyRequest.

    Raises ContextPacketAssemblyError on invalid input.
    """
    error_cls = ContextPacketAssemblyError

    # Pre-validate request_ref
    if not isinstance(request_ref, str) or not request_ref.strip():
        raise error_cls("request_ref must be a non-empty string")

    # Pre-validate assembly_timestamp
    if not isinstance(assembly_timestamp, str) or not assembly_timestamp.strip():
        raise error_cls("assembly_timestamp must be a non-empty string")

    # Pre-validate packet_kind
    if not isinstance(packet_kind, str) or not packet_kind.strip():
        raise error_cls("packet_kind must be a non-empty string")
    if packet_kind not in PACKET_KINDS:
        raise error_cls(
            f"unknown packet_kind: {packet_kind!r}; "
            f"expected one of {sorted(PACKET_KINDS)}"
        )

    # Pre-validate packet_payload is a mapping
    if not isinstance(packet_payload, Mapping):
        raise error_cls("packet_payload must be a mapping")

    # Check for forbidden payload keys
    payload_keys = set(packet_payload.keys())
    forbidden_found = payload_keys & FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS
    if forbidden_found:
        raise error_cls(
            f"packet_payload contains forbidden keys: {sorted(forbidden_found)}"
        )

    # Require safety flags
    if hidden_information_excluded is not True:
        raise error_cls("hidden_information_excluded must be exactly True")
    if explicit_payload_only is not True:
        raise error_cls("explicit_payload_only must be exactly True")
    if no_runtime_state_source is not True:
        raise error_cls("no_runtime_state_source must be exactly True")

    # Pre-validate optional tuple fields
    if non_authority_seal is not None:
        if isinstance(non_authority_seal, str):
            raise error_cls("non_authority_seal must not be a bare string")
        if not isinstance(non_authority_seal, Sequence):
            raise error_cls("non_authority_seal must be a sequence")

    # Pre-validate metadata type if provided
    if metadata is not None and not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")

    # Build kwargs — __post_init__ handles normalization
    kwargs: dict[str, Any] = {
        "request_ref": request_ref,
        "packet_kind": packet_kind,
        "packet_payload": dict(packet_payload),
        "assembly_timestamp": assembly_timestamp,
        "hidden_information_excluded": hidden_information_excluded,
        "explicit_payload_only": explicit_payload_only,
        "no_runtime_state_source": no_runtime_state_source,
        "non_authority_seal": (
            list(non_authority_seal) if non_authority_seal is not None else ()
        ),
        "metadata": dict(metadata) if metadata is not None else {},
    }

    return ContextPacketAssemblyRequest(**kwargs)


def assemble_context_packet(request: Any) -> Any:
    """Assemble exactly one context packet from an explicit assembly request.

    Dispatches to the correct packet factory based on packet_kind.
    Validates the resulting packet before returning.
    Raises ContextPacketAssemblyError for invalid request objects or unknown
    packet kinds. Allows packet-specific factory/validator errors to pass
    through for invalid packet payload content.
    """
    if not isinstance(request, ContextPacketAssemblyRequest):
        raise ContextPacketAssemblyError(
            "request must be a ContextPacketAssemblyRequest instance"
        )

    _factory_map: dict[str, Any] = {
        "single_event_narration": create_single_event_narration_packet,
        "no_commit_intent": create_no_commit_intent_packet,
        "visible_summary": create_visible_summary_packet,
    }

    if request.packet_kind not in _factory_map:
        raise ContextPacketAssemblyError(
            f"unknown packet_kind: {request.packet_kind!r}"
        )

    factory = _factory_map[request.packet_kind]
    packet = factory(**request.packet_payload)
    validate_context_packet(packet)
    return packet


def assemble_and_serialize_context_packet(request: Any) -> dict[str, Any]:
    """Assemble and serialize exactly one context packet from an assembly request.

    Calls assemble_context_packet then serialize_context_packet.
    Returns a deep copy so mutating the result cannot affect the request
    or packet. Does not aggregate packets or read runtime state.
    """
    packet = assemble_context_packet(request)
    return serialize_context_packet(packet)


# ---------------------------------------------------------------------------
# Slice 6 — context packet audit and size estimate helpers
# ---------------------------------------------------------------------------

# Audit forbidden keys reuse the same boundary set defined for assembly payloads.
# The literals are intentionally isolated in FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS so
# prior source-scan tests can exclude them; aliasing avoids duplicating them here.
_AUDIT_FORBIDDEN_SERIALIZED_KEYS = FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS


class ContextPacketAuditError(ContextPacketCompilerError):
    """Raised for unsupported audit inputs or malformed serialized packet mappings."""


@dataclass(frozen=True, kw_only=True)
class ContextPacketAuditReport:
    """Immutable audit/report object for an already-serialized context packet.

    Reports deterministic size estimates and structural/boundary risk flags.
    This object does not enforce token caps or packet budgets.
    """

    packet_kind: str
    estimated_chars: int
    estimated_words: int
    estimated_top_level_keys: int
    hidden_information_excluded: bool
    non_authority_seal_present: bool
    committed_state_only: bool | None
    forbidden_claims_count: int | None
    forbidden_key_hits: tuple[str, ...]
    warnings: tuple[str, ...]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass.

        Uses object.__setattr__ because the dataclass is frozen.
        """
        error_cls = ContextPacketAuditError

        # Validate packet_kind
        if not isinstance(self.packet_kind, str) or not self.packet_kind.strip():
            raise error_cls("packet_kind must be a non-empty string")
        if self.packet_kind not in PACKET_KINDS:
            raise error_cls(
                f"packet_kind must be one of {sorted(PACKET_KINDS)}; "
                f"got: {self.packet_kind!r}"
            )

        # Validate non-negative integer size estimates
        for name in (
            "estimated_chars",
            "estimated_words",
            "estimated_top_level_keys",
        ):
            val = getattr(self, name)
            if not isinstance(val, int) or isinstance(val, bool) or val < 0:
                raise error_cls(f"{name} must be a non-negative integer")

        # Validate boolean flags
        if not isinstance(self.hidden_information_excluded, bool):
            raise error_cls("hidden_information_excluded must be a bool")
        if not isinstance(self.non_authority_seal_present, bool):
            raise error_cls("non_authority_seal_present must be a bool")

        # Validate committed_state_only is bool or None
        if self.committed_state_only is not None and not isinstance(
            self.committed_state_only, bool
        ):
            raise error_cls("committed_state_only must be a bool or None")

        # Validate forbidden_claims_count is non-negative int or None
        if self.forbidden_claims_count is not None:
            if (
                not isinstance(self.forbidden_claims_count, int)
                or isinstance(self.forbidden_claims_count, bool)
                or self.forbidden_claims_count < 0
            ):
                raise error_cls(
                    "forbidden_claims_count must be a non-negative integer or None"
                )

        # Normalize forbidden_key_hits to sorted tuple of strings
        safe_hits = _normalize_string_tuple(
            self.forbidden_key_hits, "forbidden_key_hits", error_cls
        )
        safe_hits = tuple(sorted(safe_hits))

        # Normalize warnings to tuple of strings
        safe_warnings = _normalize_string_tuple(
            self.warnings, "warnings", error_cls
        )

        # Deep-copy and freeze metadata
        safe_metadata = _safe_metadata(self.metadata, error_cls)

        # Use object.__setattr__ to update frozen fields
        object.__setattr__(self, "forbidden_key_hits", safe_hits)
        object.__setattr__(self, "warnings", safe_warnings)
        object.__setattr__(self, "metadata", safe_metadata)


def estimate_context_packet_size(value: Any) -> dict[str, int]:
    """Estimate packet size from a packet instance or serialized mapping.

    Returns a deterministic dict with character, word, and top-level-key
    estimates. Uses JSON serialization with sorted keys for the character
    estimate and a simple whitespace split for the word estimate. Does not
    enforce limits or modify the input.
    """
    if isinstance(value, Mapping):
        serialized = copy.deepcopy(dict(value))
    else:
        try:
            serialized = serialize_context_packet(value)
        except ContextPacketSelectionError as exc:
            raise ContextPacketAuditError(
                f"unsupported context packet value: {exc}"
            ) from exc

    packet_kind = serialized.get("packet_kind")
    if not isinstance(packet_kind, str) or packet_kind not in PACKET_KINDS:
        raise ContextPacketAuditError(
            f"packet_kind must be a known kind; got {packet_kind!r}"
        )

    json_str = json.dumps(serialized, sort_keys=True)
    return {
        "estimated_chars": len(json_str),
        "estimated_words": len(json_str.split()),
        "estimated_top_level_keys": len(serialized),
    }


def audit_context_packet(value: Any) -> ContextPacketAuditReport:
    """Audit a known context packet instance.

    Serializes the packet and delegates to audit_serialized_context_packet.
    Raises ContextPacketAuditError for unsupported values.
    """
    try:
        serialized = serialize_context_packet(value)
    except ContextPacketSelectionError as exc:
        raise ContextPacketAuditError(
            f"unsupported context packet value: {exc}"
        ) from exc
    return audit_serialized_context_packet(serialized)


def audit_serialized_context_packet(value: Any) -> ContextPacketAuditReport:
    """Audit an already-serialized context packet mapping.

    Requires a known packet_kind. Estimates size and reports structural
    warnings without rejecting packets for warnings. Only malformed inputs
    or unknown packet kinds are rejected.
    """
    if not isinstance(value, Mapping):
        raise ContextPacketAuditError("value must be a mapping")

    serialized = copy.deepcopy(dict(value))
    packet_kind = serialized.get("packet_kind")
    if not isinstance(packet_kind, str) or packet_kind not in PACKET_KINDS:
        raise ContextPacketAuditError(
            f"unknown packet kind: {packet_kind!r}; "
            f"expected one of {sorted(PACKET_KINDS)}"
        )

    size = estimate_context_packet_size(serialized)
    warnings_list: list[str] = []

    # hidden_information_excluded must be exactly True
    hidden_information_excluded = serialized.get("hidden_information_excluded") is True
    if not hidden_information_excluded:
        warnings_list.append("hidden_information_excluded_missing_or_false")

    # non_authority_seal must exist and be non-empty
    non_authority_seal = serialized.get("non_authority_seal")
    non_authority_seal_present = bool(
        isinstance(non_authority_seal, Sequence)
        and not isinstance(non_authority_seal, str)
        and len(non_authority_seal) > 0
    )
    if not non_authority_seal_present:
        warnings_list.append("non_authority_seal_missing_or_empty")

    # committed_state_only if present; otherwise None
    committed_state_only: bool | None = None
    if "committed_state_only" in serialized:
        val = serialized["committed_state_only"]
        if isinstance(val, bool):
            committed_state_only = val
        if val is False:
            warnings_list.append("committed_state_only_false")

    # forbidden_claims_count when a forbidden-claim list exists
    forbidden_claims_count: int | None = None
    for key in (
        "narrator_forbidden_claims",
        "forbidden_claim_refs",
        "forbidden_claims",
    ):
        if key in serialized:
            claims = serialized[key]
            if isinstance(claims, Sequence) and not isinstance(claims, str):
                forbidden_claims_count = len(claims)
            else:
                forbidden_claims_count = 0
            break

    # forbidden serialized key hits
    forbidden_key_hits = sorted(
        set(serialized.keys()) & _AUDIT_FORBIDDEN_SERIALIZED_KEYS
    )
    if forbidden_key_hits:
        warnings_list.append("forbidden_serialized_keys_present")

    metadata = serialized.get("metadata")
    if not isinstance(metadata, Mapping):
        metadata = {}

    return ContextPacketAuditReport(
        packet_kind=packet_kind,
        estimated_chars=size["estimated_chars"],
        estimated_words=size["estimated_words"],
        estimated_top_level_keys=size["estimated_top_level_keys"],
        hidden_information_excluded=hidden_information_excluded,
        non_authority_seal_present=non_authority_seal_present,
        committed_state_only=committed_state_only,
        forbidden_claims_count=forbidden_claims_count,
        forbidden_key_hits=tuple(forbidden_key_hits),
        warnings=tuple(warnings_list),
        metadata=metadata,
    )
