"""Tests for PR-6 Slice 5 — context packet single-packet assembly shell."""

from __future__ import annotations

import copy
import inspect
import types
from types import MappingProxyType
from typing import Any, Mapping, get_type_hints

import pytest

from astra_runtime.domain import (
    ContextPacketAssemblyError,
    ContextPacketAssemblyRequest,
    assemble_and_serialize_context_packet,
    assemble_context_packet,
    create_context_packet_assembly_request,
)
from astra_runtime.domain.context_packet_compiler import (
    FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS,
    NON_AUTHORITY_SEAL,
    PACKET_KINDS,
    ContextPacketCompilerError,
    NoCommitIntentPacket,
    SingleEventNarrationPacket,
    VisibleSummaryPacket,
    create_no_commit_intent_packet,
    create_single_event_narration_packet,
    create_visible_summary_packet,
    serialize_context_packet,
)


# ---------------------------------------------------------------------------
# Minimal explicit payload mappings
# ---------------------------------------------------------------------------

_SINGLE_EVENT_PAYLOAD: dict[str, Any] = {
    "event_ref": "evt-001",
    "event_kind": "dialogue",
    "visible_fact_refs": ["fact-1"],
}

_NO_COMMIT_PAYLOAD: dict[str, Any] = {
    "intent_ref": "intent-001",
    "actor_ref": "actor-1",
    "proposed_action_kind": "attack",
    "intent_timestamp": "2025-01-01T00:00:00Z",
}

_VISIBLE_SUMMARY_PAYLOAD: dict[str, Any] = {
    "summary_ref": "summary-001",
    "summary_scope": "scene",
    "summary_timestamp": "2025-01-01T00:00:00Z",
    "visible_fact_refs": ["fact-a"],
}


def _make_assembly_request(
    packet_kind: str = "single_event_narration",
    packet_payload: Mapping[str, Any] | None = None,
    **kwargs: Any,
) -> ContextPacketAssemblyRequest:
    if packet_payload is None:
        if packet_kind == "single_event_narration":
            packet_payload = dict(_SINGLE_EVENT_PAYLOAD)
        elif packet_kind == "no_commit_intent":
            packet_payload = dict(_NO_COMMIT_PAYLOAD)
        elif packet_kind == "visible_summary":
            packet_payload = dict(_VISIBLE_SUMMARY_PAYLOAD)
        else:
            packet_payload = {}
    return create_context_packet_assembly_request(
        request_ref="req-001",
        packet_kind=packet_kind,
        packet_payload=packet_payload,
        assembly_timestamp="2025-01-01T00:00:00Z",
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Export tests
# ---------------------------------------------------------------------------


class TestExports:
    """Verify that all Slice 5 symbols are exported from astra_runtime.domain."""

    def test_context_packet_assembly_error_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "ContextPacketAssemblyError")

    def test_context_packet_assembly_request_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "ContextPacketAssemblyRequest")

    def test_create_context_packet_assembly_request_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "create_context_packet_assembly_request")

    def test_assemble_context_packet_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "assemble_context_packet")

    def test_assemble_and_serialize_context_packet_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "assemble_and_serialize_context_packet")


# ---------------------------------------------------------------------------
# Error hierarchy tests
# ---------------------------------------------------------------------------


class TestErrorHierarchy:
    """Verify ContextPacketAssemblyError inherits from ContextPacketCompilerError."""

    def test_assembly_error_is_compiler_error(self) -> None:
        assert issubclass(ContextPacketAssemblyError, ContextPacketCompilerError)

    def test_assembly_error_is_exception(self) -> None:
        assert issubclass(ContextPacketAssemblyError, Exception)

    def test_assembly_error_instance(self) -> None:
        err = ContextPacketAssemblyError("test")
        assert isinstance(err, ContextPacketCompilerError)
        assert str(err) == "test"


# ---------------------------------------------------------------------------
# ContextPacketAssemblyRequest dataclass tests
# ---------------------------------------------------------------------------


class TestContextPacketAssemblyRequest:
    """Verify request dataclass behavior: frozen, deep-copies, validates."""

    def test_factory_creates_frozen_dataclass(self) -> None:
        req = _make_assembly_request()
        assert isinstance(req, ContextPacketAssemblyRequest)
        with pytest.raises(AttributeError):
            req.request_ref = "changed"  # type: ignore[misc]

    def test_request_freezes_and_deep_copies_packet_payload(self) -> None:
        mutable_payload = {
            "event_ref": "evt-002",
            "event_kind": "combat",
            "visible_fact_refs": ["fact-2"],
        }
        req = create_context_packet_assembly_request(
            request_ref="req-002",
            packet_kind="single_event_narration",
            packet_payload=mutable_payload,
            assembly_timestamp="2025-02-02T00:00:00Z",
        )
        # Mutating original should not affect the request
        mutable_payload["event_ref"] = "mutated"
        assert req.packet_payload["event_ref"] == "evt-002"
        # Packet payload should be a MappingProxyType (frozen)
        assert isinstance(req.packet_payload, MappingProxyType)

    def test_request_freezes_and_deep_copies_metadata(self) -> None:
        mutable_meta: dict[str, Any] = {"key": "value"}
        req = create_context_packet_assembly_request(
            request_ref="req-003",
            packet_kind="single_event_narration",
            packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
            assembly_timestamp="2025-03-03T00:00:00Z",
            metadata=mutable_meta,
        )
        mutable_meta["key"] = "mutated"
        assert req.metadata["key"] == "value"
        assert isinstance(req.metadata, MappingProxyType)

    def test_request_defaults_non_authority_seal(self) -> None:
        req = _make_assembly_request()
        expected = tuple(sorted(NON_AUTHORITY_SEAL))
        assert req.non_authority_seal == expected

    def test_request_rejects_empty_request_ref(self) -> None:
        with pytest.raises(ContextPacketAssemblyError, match="request_ref"):
            create_context_packet_assembly_request(
                request_ref="",
                packet_kind="single_event_narration",
                packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
                assembly_timestamp="2025-01-01T00:00:00Z",
            )

    def test_request_rejects_empty_assembly_timestamp(self) -> None:
        with pytest.raises(ContextPacketAssemblyError, match="assembly_timestamp"):
            create_context_packet_assembly_request(
                request_ref="req-004",
                packet_kind="single_event_narration",
                packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
                assembly_timestamp="",
            )

    def test_request_rejects_unknown_packet_kind(self) -> None:
        with pytest.raises(ContextPacketAssemblyError, match="unknown packet_kind"):
            create_context_packet_assembly_request(
                request_ref="req-005",
                packet_kind="unknown_kind",
                packet_payload={},
                assembly_timestamp="2025-01-01T00:00:00Z",
            )

    def test_request_rejects_empty_packet_kind(self) -> None:
        with pytest.raises(ContextPacketAssemblyError, match="packet_kind"):
            create_context_packet_assembly_request(
                request_ref="req-006",
                packet_kind="",
                packet_payload={},
                assembly_timestamp="2025-01-01T00:00:00Z",
            )

    def test_request_rejects_non_mapping_packet_payload(self) -> None:
        with pytest.raises(ContextPacketAssemblyError, match="packet_payload"):
            create_context_packet_assembly_request(
                request_ref="req-007",
                packet_kind="single_event_narration",
                packet_payload="not a mapping",  # type: ignore[arg-type]
                assembly_timestamp="2025-01-01T00:00:00Z",
            )

    def test_request_rejects_each_forbidden_payload_key(self) -> None:
        for forbidden_key in FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS:
            payload: dict[str, Any] = {
                "event_ref": "evt-001",
                "event_kind": "dialogue",
                "visible_fact_refs": ["fact-1"],
                forbidden_key: "value",
            }
            with pytest.raises(ContextPacketAssemblyError, match="forbidden keys"):
                create_context_packet_assembly_request(
                    request_ref="req-forbidden",
                    packet_kind="single_event_narration",
                    packet_payload=payload,
                    assembly_timestamp="2025-01-01T00:00:00Z",
                )

    def test_request_rejects_hidden_information_excluded_false(self) -> None:
        with pytest.raises(
            ContextPacketAssemblyError, match="hidden_information_excluded"
        ):
            create_context_packet_assembly_request(
                request_ref="req-008",
                packet_kind="single_event_narration",
                packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
                assembly_timestamp="2025-01-01T00:00:00Z",
                hidden_information_excluded=False,
            )

    def test_request_rejects_explicit_payload_only_false(self) -> None:
        with pytest.raises(
            ContextPacketAssemblyError, match="explicit_payload_only"
        ):
            create_context_packet_assembly_request(
                request_ref="req-009",
                packet_kind="single_event_narration",
                packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
                assembly_timestamp="2025-01-01T00:00:00Z",
                explicit_payload_only=False,
            )

    def test_request_rejects_no_runtime_state_source_false(self) -> None:
        with pytest.raises(
            ContextPacketAssemblyError, match="no_runtime_state_source"
        ):
            create_context_packet_assembly_request(
                request_ref="req-010",
                packet_kind="single_event_narration",
                packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
                assembly_timestamp="2025-01-01T00:00:00Z",
                no_runtime_state_source=False,
            )


# ---------------------------------------------------------------------------
# assemble_context_packet tests
# ---------------------------------------------------------------------------


class TestAssembleContextPacket:
    """Verify assembly dispatch returns correct packet types and handles errors."""

    def test_assemble_single_event_narration(self) -> None:
        req = _make_assembly_request(
            packet_kind="single_event_narration",
            packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
        )
        packet = assemble_context_packet(req)
        assert isinstance(packet, SingleEventNarrationPacket)
        assert packet.packet_kind == "single_event_narration"
        assert packet.event_ref == "evt-001"

    def test_assemble_no_commit_intent(self) -> None:
        req = _make_assembly_request(
            packet_kind="no_commit_intent",
            packet_payload=dict(_NO_COMMIT_PAYLOAD),
        )
        packet = assemble_context_packet(req)
        assert isinstance(packet, NoCommitIntentPacket)
        assert packet.packet_kind == "no_commit_intent"
        assert packet.intent_ref == "intent-001"

    def test_assemble_visible_summary(self) -> None:
        req = _make_assembly_request(
            packet_kind="visible_summary",
            packet_payload=dict(_VISIBLE_SUMMARY_PAYLOAD),
        )
        packet = assemble_context_packet(req)
        assert isinstance(packet, VisibleSummaryPacket)
        assert packet.packet_kind == "visible_summary"
        assert packet.summary_ref == "summary-001"

    def test_assemble_rejects_non_request(self) -> None:
        with pytest.raises(ContextPacketAssemblyError, match="ContextPacketAssemblyRequest"):
            assemble_context_packet("not a request")  # type: ignore[arg-type]

    def test_assemble_rejects_dict(self) -> None:
        with pytest.raises(ContextPacketAssemblyError, match="ContextPacketAssemblyRequest"):
            assemble_context_packet({"packet_kind": "single_event_narration"})  # type: ignore[arg-type]

    def test_assemble_preserves_packet_specific_errors(self) -> None:
        """Invalid payload content should raise the packet-specific error, not assembly error."""
        bad_payload = {
            "event_ref": "",  # invalid — empty event_ref
            "event_kind": "dialogue",
            "visible_fact_refs": ["fact-1"],
        }
        req = create_context_packet_assembly_request(
            request_ref="req-bad",
            packet_kind="single_event_narration",
            packet_payload=bad_payload,
            assembly_timestamp="2025-01-01T00:00:00Z",
        )
        # The packet-specific error should propagate (InvalidSingleEventNarrationPacketError)
        from astra_runtime.domain.context_packet_compiler import (
            InvalidSingleEventNarrationPacketError,
        )

        with pytest.raises(InvalidSingleEventNarrationPacketError):
            assemble_context_packet(req)


# ---------------------------------------------------------------------------
# assemble_and_serialize_context_packet tests
# ---------------------------------------------------------------------------


class TestAssembleAndSerializeContextPacket:
    """Verify assembly + serialization returns correct dicts and deep copies."""

    def test_serialize_single_event_narration(self) -> None:
        req = _make_assembly_request(
            packet_kind="single_event_narration",
            packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
        )
        result = assemble_and_serialize_context_packet(req)
        assert isinstance(result, dict)
        assert result["packet_kind"] == "single_event_narration"
        assert result["event_ref"] == "evt-001"
        assert result["event_kind"] == "dialogue"
        assert result["visible_fact_refs"] == ["fact-1"]
        assert result["hidden_information_excluded"] is True
        assert isinstance(result["non_authority_seal"], list)
        assert len(result["non_authority_seal"]) > 0
        assert isinstance(result["metadata"], dict)

    def test_serialize_no_commit_intent(self) -> None:
        req = _make_assembly_request(
            packet_kind="no_commit_intent",
            packet_payload=dict(_NO_COMMIT_PAYLOAD),
        )
        result = assemble_and_serialize_context_packet(req)
        assert isinstance(result, dict)
        assert result["packet_kind"] == "no_commit_intent"
        assert result["intent_ref"] == "intent-001"
        assert result["actor_ref"] == "actor-1"
        assert result["proposed_action_kind"] == "attack"

    def test_serialize_visible_summary(self) -> None:
        req = _make_assembly_request(
            packet_kind="visible_summary",
            packet_payload=dict(_VISIBLE_SUMMARY_PAYLOAD),
        )
        result = assemble_and_serialize_context_packet(req)
        assert isinstance(result, dict)
        assert result["packet_kind"] == "visible_summary"
        assert result["summary_ref"] == "summary-001"
        assert result["summary_scope"] == "scene"
        assert result["visible_fact_refs"] == ["fact-a"]

    def test_returns_deep_copy(self) -> None:
        req = _make_assembly_request(
            packet_kind="single_event_narration",
            packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
        )
        result1 = assemble_and_serialize_context_packet(req)
        result2 = assemble_and_serialize_context_packet(req)
        assert result1 == result2
        # Mutating one should not affect the other
        result1["event_ref"] = "mutated"
        assert result2["event_ref"] == "evt-001"

    def test_metadata_is_plain_dict(self) -> None:
        req = _make_assembly_request(
            packet_kind="single_event_narration",
            packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
            metadata={"custom_key": "custom_value"},
        )
        # Request-level metadata is metadata about the request, not the packet.
        assert isinstance(req.metadata, MappingProxyType)
        assert req.metadata["custom_key"] == "custom_value"
        # Assembled and serialized packet metadata is the packet's own metadata.
        result = assemble_and_serialize_context_packet(req)
        assert isinstance(result["metadata"], dict)


# ---------------------------------------------------------------------------
# Source content constraint tests
# ---------------------------------------------------------------------------


class TestSourceConstraints:
    """Verify the assembly shell does not contain forbidden runtime authority terms.

    Checks only the Slice 5 assembly functions' source, excluding the
    FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS frozenset definition which intentionally
    contains terms like rng_result, model_output, narration_output as keys
    to reject.
    """

    _ASSEMBLY_FUNCTION_NAMES = [
        "assemble_context_packet",
        "assemble_and_serialize_context_packet",
        "create_context_packet_assembly_request",
    ]

    FORBIDDEN_EXECUTION_TERMS: list[str] = [
        "compile_from_runtime_state",
        "read_runtime_state",
        "commit_event(",
        "apply_delta",
        "mutate_state",
        "roll_dice",
        "generate_narration",
        "persist_state",
        "replay_event",
    ]

    def test_forbidden_execution_terms_absent_from_assembly_functions(self) -> None:
        import astra_runtime.domain.context_packet_compiler as mod

        for name in self._ASSEMBLY_FUNCTION_NAMES:
            func = getattr(mod, name)
            func_source = inspect.getsource(func)
            for term in self.FORBIDDEN_EXECUTION_TERMS:
                assert term not in func_source, (
                    f"assembly function {name} contains forbidden term: {term!r}"
                )

    def test_forbidden_assembly_payload_keys_is_frozenset(self) -> None:
        assert isinstance(FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS, frozenset)
        assert len(FORBIDDEN_ASSEMBLY_PAYLOAD_KEYS) > 0


# ---------------------------------------------------------------------------
# Public name constraint tests
# ---------------------------------------------------------------------------


class TestPublicNameConstraints:
    """Verify no public helper name contains forbidden runtime terms."""

    _FORBIDDEN_NAME_PARTS = [
        "batch",
        "aggregate",
        "runtime_state",
        "state_store",
        "event_ledger",
        "model",
        "narration",
    ]

    _PUBLIC_NAMES = [
        "ContextPacketAssemblyError",
        "ContextPacketAssemblyRequest",
        "create_context_packet_assembly_request",
        "assemble_context_packet",
        "assemble_and_serialize_context_packet",
    ]

    def test_no_public_name_contains_forbidden_parts(self) -> None:
        for name in self._PUBLIC_NAMES:
            for part in self._FORBIDDEN_NAME_PARTS:
                assert part not in name.lower(), (
                    f"public name {name!r} contains forbidden part {part!r}"
                )

    def test_assemble_context_packet_is_callable(self) -> None:
        assert callable(assemble_context_packet)

    def test_assemble_and_serialize_context_packet_is_callable(self) -> None:
        assert callable(assemble_and_serialize_context_packet)

    def test_create_context_packet_assembly_request_is_callable(self) -> None:
        assert callable(create_context_packet_assembly_request)
