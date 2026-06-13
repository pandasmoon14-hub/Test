"""Tests for PR-6 Slice 4 — context packet selection and serialization helpers."""

from __future__ import annotations

import copy
import inspect
import types
from typing import Any, get_type_hints

import pytest

from astra_runtime.domain import (
    ContextPacketSelectionError,
    get_context_packet_kind,
    serialize_context_packet,
    select_context_packet_serializer,
    select_context_packet_validator,
    validate_context_packet,
)
from astra_runtime.domain.context_packet_compiler import (
    ContextPacketCompilerError,
    InvalidNoCommitIntentPacketError,
    InvalidSingleEventNarrationPacketError,
    InvalidVisibleSummaryPacketError,
    NoCommitIntentPacket,
    SingleEventNarrationPacket,
    VisibleSummaryPacket,
    create_no_commit_intent_packet,
    create_single_event_narration_packet,
    create_visible_summary_packet,
)


# ---------------------------------------------------------------------------
# Fixture helpers — minimal valid packets via canonical factories
# ---------------------------------------------------------------------------


def _make_single_event_narration_packet() -> SingleEventNarrationPacket:
    return create_single_event_narration_packet(
        event_ref="evt-001",
        event_kind="dialogue",
        visible_fact_refs=["fact-1"],
    )


def _make_no_commit_intent_packet() -> NoCommitIntentPacket:
    return create_no_commit_intent_packet(
        intent_ref="intent-001",
        actor_ref="actor-1",
        proposed_action_kind="attack",
        intent_timestamp="2025-01-01T00:00:00Z",
    )


def _make_visible_summary_packet() -> VisibleSummaryPacket:
    return create_visible_summary_packet(
        summary_ref="sum-001",
        summary_scope="scene",
        summary_timestamp="2025-01-01T00:00:00Z",
        visible_fact_refs=["fact-a"],
    )


# ---------------------------------------------------------------------------
# Export tests
# ---------------------------------------------------------------------------


class TestExports:
    """Verify that all Slice 4 symbols are exported from astra_runtime.domain."""

    def test_context_packet_selection_error_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "ContextPacketSelectionError")

    def test_get_context_packet_kind_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "get_context_packet_kind")
        assert callable(mod.get_context_packet_kind)

    def test_validate_context_packet_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "validate_context_packet")
        assert callable(mod.validate_context_packet)

    def test_serialize_context_packet_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "serialize_context_packet")
        assert callable(mod.serialize_context_packet)

    def test_select_context_packet_validator_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "select_context_packet_validator")
        assert callable(mod.select_context_packet_validator)

    def test_select_context_packet_serializer_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "select_context_packet_serializer")
        assert callable(mod.select_context_packet_serializer)


# ---------------------------------------------------------------------------
# get_context_packet_kind
# ---------------------------------------------------------------------------


class TestGetContextPacketKind:
    """get_context_packet_kind() returns correct packet_kind for each packet type."""

    def test_single_event_narration(self) -> None:
        pkt = _make_single_event_narration_packet()
        assert get_context_packet_kind(pkt) == "single_event_narration"

    def test_no_commit_intent(self) -> None:
        pkt = _make_no_commit_intent_packet()
        assert get_context_packet_kind(pkt) == "no_commit_intent"

    def test_visible_summary(self) -> None:
        pkt = _make_visible_summary_packet()
        assert get_context_packet_kind(pkt) == "visible_summary"

    def test_rejects_none(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            get_context_packet_kind(None)

    def test_rejects_string(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            get_context_packet_kind("single_event_narration")

    def test_rejects_int(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            get_context_packet_kind(42)

    def test_rejects_plain_dict(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            get_context_packet_kind({"packet_kind": "single_event_narration"})

    def test_rejects_plain_object(self) -> None:
        class _Fake:
            packet_kind = "single_event_narration"

        with pytest.raises(ContextPacketSelectionError):
            get_context_packet_kind(_Fake())


# ---------------------------------------------------------------------------
# select_context_packet_validator
# ---------------------------------------------------------------------------


class TestSelectContextPacketValidator:
    """select_context_packet_validator() returns correct validator for each kind."""

    def test_single_event_narration_validator(self) -> None:
        fn = select_context_packet_validator("single_event_narration")
        assert fn is validate_context_packet or callable(fn)
        # Should be the specific validator
        from astra_runtime.domain.context_packet_compiler import (
            validate_single_event_narration_packet,
        )

        assert fn is validate_single_event_narration_packet

    def test_no_commit_intent_validator(self) -> None:
        fn = select_context_packet_validator("no_commit_intent")
        from astra_runtime.domain.context_packet_compiler import (
            validate_no_commit_intent_packet,
        )

        assert fn is validate_no_commit_intent_packet

    def test_visible_summary_validator(self) -> None:
        fn = select_context_packet_validator("visible_summary")
        from astra_runtime.domain.context_packet_compiler import (
            validate_visible_summary_packet,
        )

        assert fn is validate_visible_summary_packet

    def test_rejects_empty_string(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_validator("")

    def test_rejects_whitespace_only(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_validator("   ")

    def test_rejects_none(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_validator(None)  # type: ignore[arg-type]

    def test_rejects_unknown_kind(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_validator("unknown_kind")

    def test_rejects_non_string(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_validator(123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# select_context_packet_serializer
# ---------------------------------------------------------------------------


class TestSelectContextPacketSerializer:
    """select_context_packet_serializer() returns a callable for each known kind."""

    def test_single_event_narration_serializer_is_callable(self) -> None:
        fn = select_context_packet_serializer("single_event_narration")
        assert callable(fn)

    def test_no_commit_intent_serializer_is_callable(self) -> None:
        fn = select_context_packet_serializer("no_commit_intent")
        assert callable(fn)

    def test_visible_summary_serializer_is_callable(self) -> None:
        fn = select_context_packet_serializer("visible_summary")
        assert callable(fn)

    def test_rejects_empty_string(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_serializer("")

    def test_rejects_whitespace_only(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_serializer("   ")

    def test_rejects_none(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_serializer(None)  # type: ignore[arg-type]

    def test_rejects_unknown_kind(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_serializer("unknown_kind")

    def test_rejects_non_string(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            select_context_packet_serializer(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# validate_context_packet
# ---------------------------------------------------------------------------


class TestValidateContextPacket:
    """validate_context_packet() returns True for valid instances, rejects others."""

    def test_valid_single_event_narration(self) -> None:
        pkt = _make_single_event_narration_packet()
        assert validate_context_packet(pkt) is True

    def test_valid_no_commit_intent(self) -> None:
        pkt = _make_no_commit_intent_packet()
        assert validate_context_packet(pkt) is True

    def test_valid_visible_summary(self) -> None:
        pkt = _make_visible_summary_packet()
        assert validate_context_packet(pkt) is True

    def test_rejects_none(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            validate_context_packet(None)

    def test_rejects_string(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            validate_context_packet("not a packet")

    def test_rejects_dict(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            validate_context_packet({"packet_kind": "single_event_narration"})

    def test_rejects_int(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            validate_context_packet(123)

    def test_preserves_single_event_narration_validator_error(self) -> None:
        """Corrupted known packet type raises packet-specific error, not selection error."""
        pkt = _make_single_event_narration_packet()
        # Force an invalid field via object.__setattr__
        object.__setattr__(pkt, "event_ref", "")
        with pytest.raises(InvalidSingleEventNarrationPacketError):
            validate_context_packet(pkt)

    def test_preserves_no_commit_intent_validator_error(self) -> None:
        pkt = _make_no_commit_intent_packet()
        object.__setattr__(pkt, "intent_ref", "")
        with pytest.raises(InvalidNoCommitIntentPacketError):
            validate_context_packet(pkt)

    def test_preserves_visible_summary_validator_error(self) -> None:
        pkt = _make_visible_summary_packet()
        object.__setattr__(pkt, "summary_ref", "")
        with pytest.raises(InvalidVisibleSummaryPacketError):
            validate_context_packet(pkt)


# ---------------------------------------------------------------------------
# serialize_context_packet
# ---------------------------------------------------------------------------


class TestSerializeContextPacket:
    """serialize_context_packet() returns correct deep-copied dicts."""

    def test_single_event_narration_dict(self) -> None:
        pkt = _make_single_event_narration_packet()
        result = serialize_context_packet(pkt)
        assert isinstance(result, dict)
        assert result["packet_kind"] == "single_event_narration"
        assert result["event_ref"] == "evt-001"
        assert result["event_kind"] == "dialogue"
        assert result["visible_fact_refs"] == ["fact-1"]

    def test_no_commit_intent_dict(self) -> None:
        pkt = _make_no_commit_intent_packet()
        result = serialize_context_packet(pkt)
        assert isinstance(result, dict)
        assert result["packet_kind"] == "no_commit_intent"
        assert result["intent_ref"] == "intent-001"
        assert result["actor_ref"] == "actor-1"
        assert result["proposed_action_kind"] == "attack"

    def test_visible_summary_dict(self) -> None:
        pkt = _make_visible_summary_packet()
        result = serialize_context_packet(pkt)
        assert isinstance(result, dict)
        assert result["packet_kind"] == "visible_summary"
        assert result["summary_ref"] == "sum-001"
        assert result["summary_scope"] == "scene"
        assert result["visible_fact_refs"] == ["fact-a"]

    def test_validates_before_serialization(self) -> None:
        """validate_context_packet is called; unsupported type raises."""
        with pytest.raises(ContextPacketSelectionError):
            serialize_context_packet("not a packet")

    def test_rejects_none(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            serialize_context_packet(None)

    def test_rejects_dict(self) -> None:
        with pytest.raises(ContextPacketSelectionError):
            serialize_context_packet({"packet_kind": "single_event_narration"})

    def test_returns_deep_copy(self) -> None:
        """Mutating the returned dict must not affect the original packet."""
        pkt = _make_single_event_narration_packet()
        result = serialize_context_packet(pkt)
        original_event_ref = pkt.event_ref
        # Mutate the serialized dict
        result["event_ref"] = "MUTATED"
        # Original must be unaffected
        assert pkt.event_ref == original_event_ref

    def test_returns_deep_copy_metadata(self) -> None:
        """Mutating nested metadata in the result must not affect the packet."""
        pkt = _make_single_event_narration_packet()
        result = serialize_context_packet(pkt)
        # Mutate metadata dict in result
        result["metadata"]["injected"] = True
        # The original metadata should be unaffected
        assert "injected" not in dict(pkt.metadata)

    def test_returns_deep_copy_lists(self) -> None:
        """Mutating list fields in result must not affect the original tuple fields."""
        pkt = _make_visible_summary_packet()
        result = serialize_context_packet(pkt)
        result["visible_fact_refs"].append("injected")
        # Original packet still has its original tuple
        assert "injected" not in pkt.visible_fact_refs

    def test_preserves_single_event_narration_validator_error(self) -> None:
        pkt = _make_single_event_narration_packet()
        object.__setattr__(pkt, "event_ref", "")
        with pytest.raises(InvalidSingleEventNarrationPacketError):
            serialize_context_packet(pkt)

    def test_preserves_no_commit_intent_validator_error(self) -> None:
        pkt = _make_no_commit_intent_packet()
        object.__setattr__(pkt, "intent_ref", "")
        with pytest.raises(InvalidNoCommitIntentPacketError):
            serialize_context_packet(pkt)

    def test_preserves_visible_summary_validator_error(self) -> None:
        pkt = _make_visible_summary_packet()
        object.__setattr__(pkt, "summary_ref", "")
        with pytest.raises(InvalidVisibleSummaryPacketError):
            serialize_context_packet(pkt)


# ---------------------------------------------------------------------------
# Forbidden source-term audit
# ---------------------------------------------------------------------------


class TestForbiddenSourceTerms:
    """Helper implementation must not contain forbidden runtime authority terms."""

    FORBIDDEN = [
        "commit_event(",
        "apply_delta",
        "mutate_state",
        "roll_dice",
        "rng_result",
        "generate_narration",
        "model_output",
        "persist_state",
        "replay_event",
    ]

    def _get_helper_source(self) -> str:
        """Return the source text of the Slice 4 helper area in the compiler module.

        Excludes the FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS frozenset area which
        intentionally contains tokens like rng_result and model_output as
        rejected payload keys.
        """
        from astra_runtime.domain import context_packet_compiler as mod

        source = inspect.getsource(mod)
        # Extract from ContextPacketSelectionError class onward
        idx = source.find("class ContextPacketSelectionError")
        if idx < 0:
            return source
        helper_source = source[idx:]
        # Exclude the FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS block
        marker_start = "FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS"
        marker_idx = helper_source.find(marker_start)
        if marker_idx != -1:
            closing = helper_source.find(")", marker_idx)
            if closing != -1:
                helper_source = helper_source[:marker_idx] + helper_source[closing + 1 :]
        return helper_source

    def test_no_forbidden_terms_in_helper_area(self) -> None:
        source = self._get_helper_source()
        for term in self.FORBIDDEN:
            assert term not in source, (
                f"Forbidden term {term!r} found in Slice 4 helper area"
            )

    def test_no_forbidden_terms_in_module(self) -> None:
        from astra_runtime.domain import context_packet_compiler as mod

        full_source = inspect.getsource(mod)
        # Exclude the FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS block
        marker_start = "FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS"
        marker_idx = full_source.find(marker_start)
        if marker_idx != -1:
            closing = full_source.find(")", marker_idx)
            if closing != -1:
                source = full_source[:marker_idx] + full_source[closing + 1 :]
            else:
                source = full_source
        else:
            source = full_source
        for term in self.FORBIDDEN:
            # Allow no_event_commitment in NON_AUTHORITY_SEAL (it's a seal, not authority)
            if term == "commit_event(":
                # Only check outside NON_AUTHORITY_SEAL and docstring seal mentions
                lines = source.split("\n")
                for i, line in enumerate(lines):
                    if term in line:
                        # Skip if it's part of a seal/constant definition
                        if "no_event_commitment" in line or "NON_AUTHORITY" in line:
                            continue
                        pytest.fail(
                            f"Forbidden term {term!r} found at line {i + 1}: {line.strip()}"
                        )
            else:
                assert term not in source, (
                    f"Forbidden term {term!r} found in module source"
                )
