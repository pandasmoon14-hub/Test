"""Tests for PR-6 Slice 6 — context packet audit and size estimate helpers."""

from __future__ import annotations

import inspect
from types import MappingProxyType
from typing import Any, Mapping

import pytest

from astra_runtime.domain import (
    ContextPacketAuditError,
    ContextPacketAuditReport,
    audit_context_packet,
    audit_serialized_context_packet,
    estimate_context_packet_size,
)
from astra_runtime.domain.context_packet_compiler import (
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
# Factory helpers
# ---------------------------------------------------------------------------


def _make_single_event_packet() -> SingleEventNarrationPacket:
    return create_single_event_narration_packet(
        event_ref="evt-001",
        event_kind="dialogue",
        visible_fact_refs=["fact-1"],
    )


def _make_no_commit_packet() -> NoCommitIntentPacket:
    return create_no_commit_intent_packet(
        intent_ref="intent-001",
        actor_ref="actor-1",
        proposed_action_kind="attack",
        intent_timestamp="2025-01-01T00:00:00Z",
    )


def _make_visible_summary_packet() -> VisibleSummaryPacket:
    return create_visible_summary_packet(
        summary_ref="summary-001",
        summary_scope="scene",
        summary_timestamp="2025-01-01T00:00:00Z",
        visible_fact_refs=["fact-a"],
    )


# ---------------------------------------------------------------------------
# Export tests
# ---------------------------------------------------------------------------


class TestExports:
    """Verify Slice 6 symbols are exported from astra_runtime.domain."""

    def test_context_packet_audit_error_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "ContextPacketAuditError")

    def test_context_packet_audit_report_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "ContextPacketAuditReport")

    def test_estimate_context_packet_size_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "estimate_context_packet_size")

    def test_audit_context_packet_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "audit_context_packet")

    def test_audit_serialized_context_packet_exported(self) -> None:
        from astra_runtime import domain as mod

        assert hasattr(mod, "audit_serialized_context_packet")


# ---------------------------------------------------------------------------
# Error hierarchy tests
# ---------------------------------------------------------------------------


class TestErrorHierarchy:
    """Verify ContextPacketAuditError inherits from ContextPacketCompilerError."""

    def test_audit_error_is_compiler_error(self) -> None:
        assert issubclass(ContextPacketAuditError, ContextPacketCompilerError)

    def test_audit_error_is_exception(self) -> None:
        assert issubclass(ContextPacketAuditError, Exception)

    def test_audit_error_instance(self) -> None:
        err = ContextPacketAuditError("test")
        assert isinstance(err, ContextPacketCompilerError)
        assert str(err) == "test"


# ---------------------------------------------------------------------------
# ContextPacketAuditReport dataclass tests
# ---------------------------------------------------------------------------


class TestContextPacketAuditReport:
    """Verify report is frozen and normalizes fields."""

    def test_report_is_frozen(self) -> None:
        report = ContextPacketAuditReport(
            packet_kind="single_event_narration",
            estimated_chars=10,
            estimated_words=2,
            estimated_top_level_keys=3,
            hidden_information_excluded=True,
            non_authority_seal_present=True,
            committed_state_only=None,
            forbidden_claims_count=None,
            forbidden_key_hits=(),
            warnings=(),
        )
        with pytest.raises(AttributeError):
            report.packet_kind = "mutated"  # type: ignore[misc]

    def test_report_normalizes_forbidden_key_hits_to_sorted_tuple(self) -> None:
        report = ContextPacketAuditReport(
            packet_kind="single_event_narration",
            estimated_chars=10,
            estimated_words=2,
            estimated_top_level_keys=3,
            hidden_information_excluded=True,
            non_authority_seal_present=True,
            committed_state_only=None,
            forbidden_claims_count=None,
            forbidden_key_hits=["z_key", "a_key"],
            warnings=["warn-1"],
        )
        assert report.forbidden_key_hits == ("a_key", "z_key")

    def test_report_normalizes_warnings_to_tuple(self) -> None:
        report = ContextPacketAuditReport(
            packet_kind="single_event_narration",
            estimated_chars=10,
            estimated_words=2,
            estimated_top_level_keys=3,
            hidden_information_excluded=True,
            non_authority_seal_present=True,
            committed_state_only=None,
            forbidden_claims_count=None,
            forbidden_key_hits=(),
            warnings=["warn-1", "warn-2"],
        )
        assert report.warnings == ("warn-1", "warn-2")

    def test_report_freezes_metadata(self) -> None:
        mutable_meta: dict[str, Any] = {"key": "value"}
        report = ContextPacketAuditReport(
            packet_kind="single_event_narration",
            estimated_chars=10,
            estimated_words=2,
            estimated_top_level_keys=3,
            hidden_information_excluded=True,
            non_authority_seal_present=True,
            committed_state_only=None,
            forbidden_claims_count=None,
            forbidden_key_hits=(),
            warnings=(),
            metadata=mutable_meta,
        )
        assert isinstance(report.metadata, MappingProxyType)
        assert report.metadata["key"] == "value"
        mutable_meta["key"] = "mutated"
        assert report.metadata["key"] == "value"

    def test_report_rejects_unknown_packet_kind(self) -> None:
        with pytest.raises(ContextPacketAuditError, match="packet_kind"):
            ContextPacketAuditReport(
                packet_kind="unknown_kind",
                estimated_chars=10,
                estimated_words=2,
                estimated_top_level_keys=3,
                hidden_information_excluded=True,
                non_authority_seal_present=True,
                committed_state_only=None,
                forbidden_claims_count=None,
                forbidden_key_hits=(),
                warnings=(),
            )

    def test_report_rejects_negative_size(self) -> None:
        with pytest.raises(ContextPacketAuditError, match="estimated_chars"):
            ContextPacketAuditReport(
                packet_kind="single_event_narration",
                estimated_chars=-1,
                estimated_words=2,
                estimated_top_level_keys=3,
                hidden_information_excluded=True,
                non_authority_seal_present=True,
                committed_state_only=None,
                forbidden_claims_count=None,
                forbidden_key_hits=(),
                warnings=(),
            )

    def test_report_rejects_invalid_forbidden_claims_count(self) -> None:
        with pytest.raises(ContextPacketAuditError, match="forbidden_claims_count"):
            ContextPacketAuditReport(
                packet_kind="single_event_narration",
                estimated_chars=10,
                estimated_words=2,
                estimated_top_level_keys=3,
                hidden_information_excluded=True,
                non_authority_seal_present=True,
                committed_state_only=None,
                forbidden_claims_count=-1,
                forbidden_key_hits=(),
                warnings=(),
            )


# ---------------------------------------------------------------------------
# estimate_context_packet_size tests
# ---------------------------------------------------------------------------


class TestEstimateContextPacketSize:
    """Verify size estimation works on packets, dicts, and rejects bad input."""

    def test_estimate_on_single_event_narration_packet(self) -> None:
        packet = _make_single_event_packet()
        result = estimate_context_packet_size(packet)
        assert isinstance(result, dict)
        assert set(result.keys()) == {
            "estimated_chars",
            "estimated_words",
            "estimated_top_level_keys",
        }
        assert result["estimated_chars"] > 0
        assert result["estimated_words"] > 0
        assert result["estimated_top_level_keys"] > 0

    def test_estimate_on_no_commit_intent_packet(self) -> None:
        packet = _make_no_commit_packet()
        result = estimate_context_packet_size(packet)
        assert result["estimated_chars"] > 0
        assert result["estimated_words"] > 0
        assert result["estimated_top_level_keys"] > 0

    def test_estimate_on_visible_summary_packet(self) -> None:
        packet = _make_visible_summary_packet()
        result = estimate_context_packet_size(packet)
        assert result["estimated_chars"] > 0
        assert result["estimated_words"] > 0
        assert result["estimated_top_level_keys"] > 0

    def test_estimate_on_serialized_dict(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        result = estimate_context_packet_size(serialized)
        assert result["estimated_top_level_keys"] == len(serialized)

    def test_size_estimate_is_deterministic(self) -> None:
        packet = _make_single_event_packet()
        result1 = estimate_context_packet_size(packet)
        result2 = estimate_context_packet_size(packet)
        assert result1 == result2

    def test_mapping_input_not_mutated(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        original = dict(serialized)
        estimate_context_packet_size(serialized)
        assert serialized == original

    def test_rejects_unsupported_input(self) -> None:
        with pytest.raises(ContextPacketAuditError):
            estimate_context_packet_size("not a packet or mapping")

    def test_rejects_missing_packet_kind(self) -> None:
        with pytest.raises(ContextPacketAuditError, match="packet_kind"):
            estimate_context_packet_size({"event_ref": "evt-001"})

    def test_rejects_unknown_packet_kind(self) -> None:
        with pytest.raises(ContextPacketAuditError, match="packet_kind"):
            estimate_context_packet_size({"packet_kind": "unknown_kind"})


# ---------------------------------------------------------------------------
# audit_context_packet tests
# ---------------------------------------------------------------------------


class TestAuditContextPacket:
    """Verify audit_context_packet works on all three packet instances."""

    def test_audit_single_event_narration(self) -> None:
        packet = _make_single_event_packet()
        report = audit_context_packet(packet)
        assert isinstance(report, ContextPacketAuditReport)
        assert report.packet_kind == "single_event_narration"
        assert report.hidden_information_excluded is True
        assert report.non_authority_seal_present is True

    def test_audit_no_commit_intent(self) -> None:
        packet = _make_no_commit_packet()
        report = audit_context_packet(packet)
        assert isinstance(report, ContextPacketAuditReport)
        assert report.packet_kind == "no_commit_intent"
        assert report.hidden_information_excluded is True
        assert report.non_authority_seal_present is True

    def test_audit_visible_summary(self) -> None:
        packet = _make_visible_summary_packet()
        report = audit_context_packet(packet)
        assert isinstance(report, ContextPacketAuditReport)
        assert report.packet_kind == "visible_summary"
        assert report.hidden_information_excluded is True
        assert report.non_authority_seal_present is True
        assert report.committed_state_only is True

    def test_rejects_unsupported_value(self) -> None:
        with pytest.raises(ContextPacketAuditError):
            audit_context_packet("not a packet")


# ---------------------------------------------------------------------------
# audit_serialized_context_packet tests
# ---------------------------------------------------------------------------


class TestAuditSerializedContextPacket:
    """Verify serialized packet audit behavior and warnings."""

    def test_audit_serialized_dict(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        report = audit_serialized_context_packet(serialized)
        assert isinstance(report, ContextPacketAuditReport)
        assert report.packet_kind == "single_event_narration"

    def test_valid_factory_packets_produce_no_warnings(self) -> None:
        for packet in (
            _make_single_event_packet(),
            _make_no_commit_packet(),
            _make_visible_summary_packet(),
        ):
            report = audit_context_packet(packet)
            assert report.warnings == ()

    def test_missing_hidden_information_excluded_warns(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        del serialized["hidden_information_excluded"]
        report = audit_serialized_context_packet(serialized)
        assert "hidden_information_excluded_missing_or_false" in report.warnings
        assert report.hidden_information_excluded is False

    def test_false_hidden_information_excluded_warns(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        serialized["hidden_information_excluded"] = False
        report = audit_serialized_context_packet(serialized)
        assert "hidden_information_excluded_missing_or_false" in report.warnings
        assert report.hidden_information_excluded is False

    def test_missing_non_authority_seal_warns(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        del serialized["non_authority_seal"]
        report = audit_serialized_context_packet(serialized)
        assert "non_authority_seal_missing_or_empty" in report.warnings
        assert report.non_authority_seal_present is False

    def test_empty_non_authority_seal_warns(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        serialized["non_authority_seal"] = []
        report = audit_serialized_context_packet(serialized)
        assert "non_authority_seal_missing_or_empty" in report.warnings
        assert report.non_authority_seal_present is False

    def test_forbidden_serialized_keys_sorted_and_warn(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        serialized["rng_result"] = {"roll": 5}
        serialized["model_output"] = "text"
        report = audit_serialized_context_packet(serialized)
        assert report.forbidden_key_hits == ("model_output", "rng_result")
        assert "forbidden_serialized_keys_present" in report.warnings

    def test_committed_state_only_false_warns(self) -> None:
        serialized = serialize_context_packet(_make_visible_summary_packet())
        serialized["committed_state_only"] = False
        report = audit_serialized_context_packet(serialized)
        assert report.committed_state_only is False
        assert "committed_state_only_false" in report.warnings

    def test_committed_state_only_absent_is_none(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        report = audit_serialized_context_packet(serialized)
        assert report.committed_state_only is None

    def test_forbidden_claims_counted_when_list_exists(self) -> None:
        serialized = serialize_context_packet(_make_single_event_packet())
        serialized["forbidden_claims"] = ["claim-a", "claim-b", "claim-c"]
        report = audit_serialized_context_packet(serialized)
        assert report.forbidden_claims_count == 3

    def test_forbidden_claims_count_none_when_no_list(self) -> None:
        serialized = serialize_context_packet(_make_no_commit_packet())
        report = audit_serialized_context_packet(serialized)
        assert report.forbidden_claims_count is None

    def test_rejects_non_mapping(self) -> None:
        with pytest.raises(ContextPacketAuditError, match="mapping"):
            audit_serialized_context_packet("not a mapping")

    def test_rejects_missing_packet_kind(self) -> None:
        with pytest.raises(ContextPacketAuditError, match="packet kind"):
            audit_serialized_context_packet({"event_ref": "evt-001"})

    def test_rejects_unknown_packet_kind(self) -> None:
        with pytest.raises(ContextPacketAuditError, match="unknown packet kind"):
            audit_serialized_context_packet({"packet_kind": "unknown_kind"})


# ---------------------------------------------------------------------------
# Source constraint tests
# ---------------------------------------------------------------------------


class TestSourceConstraints:
    """Verify audit helpers do not contain forbidden runtime authority calls."""

    _AUDIT_FUNCTION_NAMES = [
        "ContextPacketAuditReport",
        "estimate_context_packet_size",
        "audit_context_packet",
        "audit_serialized_context_packet",
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
    ]

    def test_forbidden_execution_terms_absent_from_audit_helpers(self) -> None:
        import astra_runtime.domain.context_packet_compiler as mod

        for name in self._AUDIT_FUNCTION_NAMES:
            obj = getattr(mod, name)
            if inspect.isclass(obj):
                source = inspect.getsource(obj)
            else:
                source = inspect.getsource(obj)
            for term in self.FORBIDDEN_EXECUTION_TERMS:
                assert term not in source, (
                    f"audit helper {name} contains forbidden term: {term!r}"
                )


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
        "ContextPacketAuditError",
        "ContextPacketAuditReport",
        "estimate_context_packet_size",
        "audit_context_packet",
        "audit_serialized_context_packet",
    ]

    def test_no_public_name_contains_forbidden_parts(self) -> None:
        for name in self._PUBLIC_NAMES:
            for part in self._FORBIDDEN_NAME_PARTS:
                assert part not in name.lower(), (
                    f"public name {name!r} contains forbidden part {part!r}"
                )

    def test_estimate_context_packet_size_is_callable(self) -> None:
        assert callable(estimate_context_packet_size)

    def test_audit_context_packet_is_callable(self) -> None:
        assert callable(audit_context_packet)

    def test_audit_serialized_context_packet_is_callable(self) -> None:
        assert callable(audit_serialized_context_packet)
