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
    """
    error_cls = InvalidSingleEventNarrationPacketError

    # Validate packet_kind
    if not isinstance(packet_kind, str) or not packet_kind.strip():
        raise error_cls("packet_kind must be a non-empty string")
    if packet_kind != "single_event_narration":
        raise error_cls(
            f"packet_kind must be 'single_event_narration', got: {packet_kind!r}"
        )

    # Validate event_ref
    if not isinstance(event_ref, str) or not event_ref.strip():
        raise error_cls("event_ref must be a non-empty string")

    # Validate event_kind
    if not isinstance(event_kind, str) or not event_kind.strip():
        raise error_cls("event_kind must be a non-empty string")

    # Validate visible_fact_refs — must be non-empty
    if not isinstance(visible_fact_refs, Sequence) or isinstance(visible_fact_refs, str):
        raise error_cls("visible_fact_refs must be a sequence")
    if len(visible_fact_refs) == 0:
        raise error_cls("visible_fact_refs must not be empty")

    # Validate hidden_information_excluded — must be exactly True
    if hidden_information_excluded is not True:
        raise error_cls("hidden_information_excluded must be exactly True")

    # Normalize tuple fields
    safe_actor_refs = _normalize_string_tuple(actor_refs, "actor_refs", error_cls)
    safe_target_refs = _normalize_string_tuple(target_refs, "target_refs", error_cls)
    safe_sensory_cues = _normalize_string_tuple(sensory_cues, "sensory_cues", error_cls)
    safe_forbidden_claims = _normalize_string_tuple(
        forbidden_claims, "forbidden_claims", error_cls
    )

    # Normalize visible_fact_refs (reject empty strings inside)
    normalized_visible_fact_refs = _normalize_string_tuple(
        list(visible_fact_refs), "visible_fact_refs", error_cls
    )

    # Default non_authority_seal if not provided
    if non_authority_seal is None:
        safe_non_authority_seal = tuple(sorted(NON_AUTHORITY_SEAL))
    else:
        safe_non_authority_seal = _normalize_string_tuple(
            non_authority_seal, "non_authority_seal", error_cls
        )

    safe_metadata = _safe_metadata(metadata, error_cls)

    return SingleEventNarrationPacket(
        packet_kind=packet_kind,
        event_ref=event_ref,
        event_kind=event_kind,
        visible_fact_refs=normalized_visible_fact_refs,
        actor_refs=safe_actor_refs,
        target_refs=safe_target_refs,
        sensory_cues=safe_sensory_cues,
        forbidden_claims=safe_forbidden_claims,
        non_authority_seal=safe_non_authority_seal,
        hidden_information_excluded=hidden_information_excluded,
        metadata=safe_metadata,
    )


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
        ("non_authority_seal", value.non_authority_seal),
    ):
        if not isinstance(field_value, tuple):
            raise error_cls(f"{field_name} must be a tuple")
        for item in field_value:
            if not isinstance(item, str) or not item.strip():
                raise error_cls(f"{field_name} items must be non-empty strings")

    # Validate hidden_information_excluded — must be exactly True
    if value.hidden_information_excluded is not True:
        raise error_cls("hidden_information_excluded must be exactly True")

    # Validate metadata
    if not isinstance(value.metadata, Mapping):
        raise error_cls("metadata must be a Mapping")

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
