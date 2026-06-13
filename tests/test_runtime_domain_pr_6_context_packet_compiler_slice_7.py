"""Tests for PR-6 Slice 7 — explicit single-packet compiler result shell."""

from __future__ import annotations

import copy
import inspect
from types import MappingProxyType
from typing import Any, Mapping

import pytest

from astra_runtime.domain import (
    ContextPacketCompilerResult,
    ContextPacketCompilerResultError,
    compile_and_audit_context_packet,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
)
from astra_runtime.domain.context_packet_compiler import (
    NON_AUTHORITY_SEAL,
    PACKET_KINDS,
    ContextPacketAuditReport,
    ContextPacketCompilerError,
    InvalidSingleEventNarrationPacketError,
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
) -> Any:
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


def _make_audit_report(
    packet_kind: str = "single_event_narration",
    **kwargs: Any,
) -> ContextPacketAuditReport:
    defaults: dict[str, Any] = {
        "packet_kind": packet_kind,
        "estimated_chars": 100,
        "estimated_words": 20,
        "estimated_top_level_keys": 10,
        "hidden_information_excluded": True,
        "non_authority_seal_present": True,
        "committed_state_only": None,
        "forbidden_claims_count": None,
        "forbidden_key_hits": (),
        "warnings": (),
    }
    defaults.update(kwargs)
    return ContextPacketAuditReport(**defaults)


def _make_result(**kwargs: Any) -> ContextPacketCompilerResult:
    defaults: dict[str, Any] = {
        "request_ref": "req-001",
        "packet_kind": "single_event_narration",
        "serialized_packet": {"packet_kind": "single_event_narration"},
        "audit_report": _make_audit_report(),
        "assembly_succeeded": True,
        "serialization_succeeded": True,
        "audit_succeeded": True,
        "hidden_information_excluded": True,
        "non_authority_seal_present": True,
        "warnings": (),
    }
    defaults.update(kwargs)
    return ContextPacketCompilerResult(**defaults)


# ---------------------------------------------------------------------------
# Export tests
# ---------------------------------------------------------------------------


class TestExports:
    """Verify Slice 7 symbols are exported from astra_runtime.domain."""

    def test_context_packet_compiler_result_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "ContextPacketCompilerResult")

    def test_context_packet_compiler_result_error_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "ContextPacketCompilerResultError")

    def test_compile_context_packet_from_request_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "compile_context_packet_from_request")

    def test_compile_and_audit_context_packet_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "compile_and_audit_context_packet")


# ---------------------------------------------------------------------------
# Error hierarchy tests
# ---------------------------------------------------------------------------


class TestErrorHierarchy:
    """Verify ContextPacketCompilerResultError inherits from ContextPacketCompilerError."""

    def test_result_error_is_compiler_error(self) -> None:
        assert issubclass(
            ContextPacketCompilerResultError, ContextPacketCompilerError
        )

    def test_result_error_is_exception(self) -> None:
        assert issubclass(ContextPacketCompilerResultError, Exception)

    def test_result_error_instance(self) -> None:
        err = ContextPacketCompilerResultError("test")
        assert isinstance(err, ContextPacketCompilerError)
        assert str(err) == "test"


# ---------------------------------------------------------------------------
# ContextPacketCompilerResult dataclass tests
# ---------------------------------------------------------------------------


class TestContextPacketCompilerResult:
    """Verify result dataclass behavior: frozen, deep-copies, validates."""

    def test_result_is_frozen(self) -> None:
        result = _make_result()
        with pytest.raises(AttributeError):
            result.request_ref = "changed"  # type: ignore[misc]

    def test_result_freezes_and_deep_copies_serialized_packet(self) -> None:
        mutable_serialized: dict[str, Any] = {
            "packet_kind": "single_event_narration",
            "nested": ["a", "b"],
        }
        result = _make_result(serialized_packet=mutable_serialized)
        mutable_serialized["nested"].append("c")
        mutable_serialized["extra"] = "added"
        assert result.serialized_packet["nested"] == ["a", "b"]
        assert "extra" not in result.serialized_packet
        assert isinstance(result.serialized_packet, MappingProxyType)

    def test_result_freezes_and_deep_copies_metadata(self) -> None:
        mutable_meta: dict[str, Any] = {"key": "value", "list": [1, 2]}
        result = _make_result(metadata=mutable_meta)
        mutable_meta["key"] = "mutated"
        mutable_meta["list"].append(3)
        assert result.metadata["key"] == "value"
        assert result.metadata["list"] == [1, 2]
        assert isinstance(result.metadata, MappingProxyType)

    def test_result_defaults_empty_non_authority_seal(self) -> None:
        result = _make_result()
        expected = tuple(sorted(NON_AUTHORITY_SEAL))
        assert result.non_authority_seal == expected

    def test_result_normalizes_warnings_to_tuple(self) -> None:
        result = _make_result(warnings=["warn-1", "warn-2"])
        assert result.warnings == ("warn-1", "warn-2")

    def test_result_rejects_empty_request_ref(self) -> None:
        with pytest.raises(ContextPacketCompilerResultError, match="request_ref"):
            _make_result(request_ref="")

    def test_result_rejects_unknown_packet_kind(self) -> None:
        with pytest.raises(ContextPacketCompilerResultError, match="packet_kind"):
            _make_result(packet_kind="unknown_kind")

    def test_result_rejects_non_mapping_serialized_packet(self) -> None:
        with pytest.raises(
            ContextPacketCompilerResultError, match="serialized_packet"
        ):
            _make_result(serialized_packet="not a mapping")  # type: ignore[arg-type]

    def test_result_rejects_non_audit_report(self) -> None:
        with pytest.raises(ContextPacketCompilerResultError, match="audit_report"):
            _make_result(audit_report={})  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "flag_name",
        [
            "assembly_succeeded",
            "serialization_succeeded",
            "audit_succeeded",
            "hidden_information_excluded",
            "non_authority_seal_present",
        ],
    )
    def test_result_rejects_non_bool_success_flags(self, flag_name: str) -> None:
        kwargs = {flag_name: "not-a-bool"}
        with pytest.raises(ContextPacketCompilerResultError, match=flag_name):
            _make_result(**kwargs)


# ---------------------------------------------------------------------------
# compile_context_packet_from_request tests
# ---------------------------------------------------------------------------


class TestCompileContextPacketFromRequest:
    """Verify the single-packet compiler result shell."""

    def test_rejects_non_request_values(self) -> None:
        with pytest.raises(
            ContextPacketCompilerResultError, match="ContextPacketAssemblyRequest"
        ):
            compile_context_packet_from_request("not a request")  # type: ignore[arg-type]

    def test_rejects_dict(self) -> None:
        with pytest.raises(
            ContextPacketCompilerResultError, match="ContextPacketAssemblyRequest"
        ):
            compile_context_packet_from_request(  # type: ignore[arg-type]
                {"packet_kind": "single_event_narration"}
            )

    def test_compiles_single_event_narration(self) -> None:
        req = _make_assembly_request(
            packet_kind="single_event_narration",
            packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
        )
        result = compile_context_packet_from_request(req)
        assert isinstance(result, ContextPacketCompilerResult)
        assert result.request_ref == "req-001"
        assert result.packet_kind == "single_event_narration"
        assert result.assembly_succeeded is True
        assert result.serialization_succeeded is True
        assert result.audit_succeeded is True
        assert result.hidden_information_excluded is True
        assert result.non_authority_seal_present is True
        assert result.warnings == ()
        assert result.serialized_packet["packet_kind"] == "single_event_narration"
        assert result.serialized_packet["event_ref"] == "evt-001"

    def test_compiles_no_commit_intent(self) -> None:
        req = _make_assembly_request(
            packet_kind="no_commit_intent",
            packet_payload=dict(_NO_COMMIT_PAYLOAD),
        )
        result = compile_context_packet_from_request(req)
        assert isinstance(result, ContextPacketCompilerResult)
        assert result.packet_kind == "no_commit_intent"
        assert result.assembly_succeeded is True
        assert result.serialization_succeeded is True
        assert result.audit_succeeded is True
        assert result.hidden_information_excluded is True
        assert result.non_authority_seal_present is True
        assert result.warnings == ()
        assert result.serialized_packet["packet_kind"] == "no_commit_intent"
        assert result.serialized_packet["intent_ref"] == "intent-001"

    def test_compiles_visible_summary(self) -> None:
        req = _make_assembly_request(
            packet_kind="visible_summary",
            packet_payload=dict(_VISIBLE_SUMMARY_PAYLOAD),
        )
        result = compile_context_packet_from_request(req)
        assert isinstance(result, ContextPacketCompilerResult)
        assert result.packet_kind == "visible_summary"
        assert result.assembly_succeeded is True
        assert result.serialization_succeeded is True
        assert result.audit_succeeded is True
        assert result.hidden_information_excluded is True
        assert result.non_authority_seal_present is True
        assert result.warnings == ()
        assert result.serialized_packet["packet_kind"] == "visible_summary"
        assert result.serialized_packet["summary_ref"] == "summary-001"

    def test_packet_specific_errors_pass_through(self) -> None:
        bad_payload = {
            "event_ref": "",  # invalid — empty event_ref
            "event_kind": "dialogue",
            "visible_fact_refs": ["fact-1"],
        }
        req = _make_assembly_request(
            packet_kind="single_event_narration",
            packet_payload=bad_payload,
        )
        with pytest.raises(InvalidSingleEventNarrationPacketError):
            compile_context_packet_from_request(req)


# ---------------------------------------------------------------------------
# compile_and_audit_context_packet tests
# ---------------------------------------------------------------------------


class TestCompileAndAuditContextPacket:
    """Verify compile_and_audit_context_packet delegates to compile_context_packet_from_request."""

    def test_delegates_and_returns_equivalent_result(self) -> None:
        req = _make_assembly_request(
            packet_kind="single_event_narration",
            packet_payload=dict(_SINGLE_EVENT_PAYLOAD),
        )
        result_a = compile_context_packet_from_request(req)
        result_b = compile_and_audit_context_packet(req)
        assert result_a == result_b
        assert isinstance(result_b, ContextPacketCompilerResult)


# ---------------------------------------------------------------------------
# Source content constraint tests
# ---------------------------------------------------------------------------


class TestSourceConstraints:
    """Verify the result shell does not contain forbidden runtime authority calls."""

    _RESULT_FUNCTION_NAMES = [
        "compile_context_packet_from_request",
        "compile_and_audit_context_packet",
    ]

    FORBIDDEN_EXECUTION_TERMS: list[str] = [
        "commit_event(",
        "apply_delta",
        "mutate_state",
        "roll_dice",
        "generate_narration",
        "persist_state",
        "replay_event",
        "state_store.get",
        "event_ledger.get",
        "model_output",
        "narration_output",
    ]

    def test_forbidden_execution_terms_absent_from_result_functions(self) -> None:
        import astra_runtime.domain.context_packet_compiler as mod

        for name in self._RESULT_FUNCTION_NAMES:
            func = getattr(mod, name)
            func_source = inspect.getsource(func)
            for term in self.FORBIDDEN_EXECUTION_TERMS:
                assert term not in func_source, (
                    f"result function {name} contains forbidden term: {term!r}"
                )
