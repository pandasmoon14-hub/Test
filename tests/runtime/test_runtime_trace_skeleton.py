"""Focused tests for RUNTIME-IMPL-PR-7: runtime trace skeleton."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from astra_runtime.kernel.runtime_trace import (
    ALLOWED_TRACE_OPERATION_TYPES,
    InvalidRuntimeTraceEntryError,
    RuntimeTraceEntry,
    RuntimeTraceError,
    create_runtime_trace_entry,
    validate_runtime_trace_entry,
)

KERNEL_DIR = Path(__file__).resolve().parent.parent.parent / "src" / "astra_runtime" / "kernel"


class TestRuntimeTraceEntry:
    def test_valid_creation(self):
        entry = create_runtime_trace_entry(
            trace_id="trace-001",
            operation_type="schema_registry",
            subject_ref="astra:schema:type-001",
            sequence=0,
        )
        assert isinstance(entry, RuntimeTraceEntry)

    def test_preserves_fields(self):
        entry = create_runtime_trace_entry(
            trace_id="trace-002",
            operation_type="command_envelope",
            subject_ref="astra:cmd:cmd-001",
            sequence=3,
        )
        assert entry.trace_id == "trace-002"
        assert entry.operation_type == "command_envelope"
        assert entry.subject_ref == "astra:cmd:cmd-001"
        assert entry.sequence == 3

    @pytest.mark.parametrize("op", sorted(ALLOWED_TRACE_OPERATION_TYPES))
    def test_allowed_operation_types(self, op):
        entry = create_runtime_trace_entry(
            trace_id="trace-op",
            operation_type=op,
            subject_ref="astra:test:t-001",
            sequence=0,
        )
        assert entry.operation_type == op

    def test_unsupported_operation_type_rejected(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id="trace-bad",
                operation_type="domain_service",
                subject_ref="astra:test:t-001",
                sequence=0,
            )

    def test_empty_trace_id_rejected(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id="",
                operation_type="schema_registry",
                subject_ref="astra:test:t-001",
                sequence=0,
            )

    def test_empty_subject_ref_rejected(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id="trace-001",
                operation_type="schema_registry",
                subject_ref="",
                sequence=0,
            )

    def test_negative_sequence_rejected(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id="trace-001",
                operation_type="schema_registry",
                subject_ref="astra:test:t-001",
                sequence=-1,
            )

    def test_bool_sequence_rejected(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id="trace-001",
                operation_type="schema_registry",
                subject_ref="astra:test:t-001",
                sequence=False,
            )

    def test_non_mapping_metadata_rejected(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id="trace-001",
                operation_type="schema_registry",
                subject_ref="astra:test:t-001",
                sequence=0,
                metadata="not a mapping",
            )

    def test_metadata_defaults_to_empty_mapping(self):
        entry = create_runtime_trace_entry(
            trace_id="trace-001",
            operation_type="schema_registry",
            subject_ref="astra:test:t-001",
            sequence=0,
        )
        assert dict(entry.metadata) == {}

    def test_metadata_deep_copy_safe(self):
        original = {"nested": {"key": "value"}}
        entry = create_runtime_trace_entry(
            trace_id="trace-001",
            operation_type="schema_registry",
            subject_ref="astra:test:t-001",
            sequence=0,
            metadata=original,
        )
        original["nested"]["key"] = "mutated"
        assert dict(entry.metadata)["nested"]["key"] == "value"

    def test_to_dict_returns_deep_copies(self):
        entry = create_runtime_trace_entry(
            trace_id="trace-001",
            operation_type="schema_registry",
            subject_ref="astra:test:t-001",
            sequence=0,
            metadata={"nested": {"key": "value"}},
        )
        d1 = entry.to_dict()
        d2 = entry.to_dict()
        d1["metadata"]["nested"]["key"] = "mutated"
        assert d2["metadata"]["nested"]["key"] == "value"

    def test_validate_accepts_valid(self):
        entry = create_runtime_trace_entry(
            trace_id="trace-001",
            operation_type="schema_registry",
            subject_ref="astra:test:t-001",
            sequence=0,
        )
        assert validate_runtime_trace_entry(entry) is True

    def test_validate_rejects_invalid(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            validate_runtime_trace_entry("not a trace entry")

    def test_frozen_immutability(self):
        entry = create_runtime_trace_entry(
            trace_id="trace-001",
            operation_type="schema_registry",
            subject_ref="astra:test:t-001",
            sequence=0,
        )
        with pytest.raises(Exception):
            entry.trace_id = "mutated"


class TestRuntimeTraceMalformedDataclass:
    """Tests for manually constructed malformed dataclasses caught by validators."""

    def test_whitespace_only_trace_id_rejected_by_factory(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id="   ",
                operation_type="schema_registry",
                subject_ref="astra:test:t-001",
                sequence=0,
            )

    def test_whitespace_only_subject_ref_rejected_by_factory(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id="trace-001",
                operation_type="schema_registry",
                subject_ref="\t\n",
                sequence=0,
            )

    def test_non_string_trace_id_rejected_by_factory(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id=123,
                operation_type="schema_registry",
                subject_ref="astra:test:t-001",
                sequence=0,
            )

    def test_non_string_subject_ref_rejected_by_factory(self):
        with pytest.raises(InvalidRuntimeTraceEntryError):
            create_runtime_trace_entry(
                trace_id="trace-001",
                operation_type="schema_registry",
                subject_ref=None,
                sequence=0,
            )

    def test_validate_rejects_whitespace_trace_id(self):
        obj = RuntimeTraceEntry(
            trace_id="   ",
            operation_type="schema_registry",
            subject_ref="astra:test:t-001",
            sequence=0,
        )
        with pytest.raises(InvalidRuntimeTraceEntryError):
            validate_runtime_trace_entry(obj)

    def test_validate_rejects_whitespace_subject_ref(self):
        obj = RuntimeTraceEntry(
            trace_id="trace-001",
            operation_type="schema_registry",
            subject_ref="  \t  ",
            sequence=0,
        )
        with pytest.raises(InvalidRuntimeTraceEntryError):
            validate_runtime_trace_entry(obj)

    def test_validate_rejects_non_string_trace_id(self):
        obj = object.__new__(RuntimeTraceEntry)
        object.__setattr__(obj, "trace_id", 999)
        object.__setattr__(obj, "operation_type", "schema_registry")
        object.__setattr__(obj, "subject_ref", "astra:test:t-001")
        object.__setattr__(obj, "sequence", 0)
        object.__setattr__(obj, "metadata", {})
        with pytest.raises(InvalidRuntimeTraceEntryError):
            validate_runtime_trace_entry(obj)

    def test_validate_rejects_bool_sequence(self):
        obj = object.__new__(RuntimeTraceEntry)
        object.__setattr__(obj, "trace_id", "trace-001")
        object.__setattr__(obj, "operation_type", "schema_registry")
        object.__setattr__(obj, "subject_ref", "astra:test:t-001")
        object.__setattr__(obj, "sequence", False)
        object.__setattr__(obj, "metadata", {})
        with pytest.raises(InvalidRuntimeTraceEntryError):
            validate_runtime_trace_entry(obj)

    def test_validate_rejects_invalid_operation_type(self):
        obj = RuntimeTraceEntry(
            trace_id="trace-001",
            operation_type="schema_registry",
            subject_ref="astra:test:t-001",
            sequence=0,
        )
        object.__setattr__(obj, "operation_type", "domain_service")
        with pytest.raises(InvalidRuntimeTraceEntryError):
            validate_runtime_trace_entry(obj)

    def test_validate_rejects_non_mapping_metadata(self):
        obj = object.__new__(RuntimeTraceEntry)
        object.__setattr__(obj, "trace_id", "trace-001")
        object.__setattr__(obj, "operation_type", "schema_registry")
        object.__setattr__(obj, "subject_ref", "astra:test:t-001")
        object.__setattr__(obj, "sequence", 0)
        object.__setattr__(obj, "metadata", "not a mapping")
        with pytest.raises(InvalidRuntimeTraceEntryError):
            validate_runtime_trace_entry(obj)


class TestRuntimeTraceGuardrails:
    def test_no_write_log_emit_methods(self):
        entry = create_runtime_trace_entry(
            trace_id="trace-001",
            operation_type="schema_registry",
            subject_ref="astra:test:t-001",
            sequence=0,
        )
        forbidden = [
            "write", "log", "emit", "send", "telemetry",
            "store", "save", "load",
        ]
        for method_name in forbidden:
            assert not hasattr(entry, method_name), f"{method_name} method must not exist"

    def test_no_context_packet_compiler_module(self):
        assert not (KERNEL_DIR / "context_packet_compiler.py").exists()

    def test_domain_package_contains_only_authorized_modules(self):
        domain_dir = KERNEL_DIR.parent / "domain"
        assert domain_dir.exists(), "Domain package should exist after PR-1A"
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "transaction_lifecycle.py", "event_commitment.py", "__pycache__"}
        actual = {p.name for p in domain_dir.iterdir()}
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized domain modules: {unauthorized}"

    def test_no_model_integration_package(self):
        assert not (KERNEL_DIR.parent / "model").exists()

    def test_no_prompt_template_package(self):
        assert not (KERNEL_DIR.parent / "prompts").exists()

    def test_no_live_play_adapter_package(self):
        assert not (KERNEL_DIR.parent / "live_play").exists()

    def test_no_ui_client_package(self):
        assert not (KERNEL_DIR.parent / "ui").exists()

    def test_no_database_package(self):
        assert not (KERNEL_DIR.parent / "database").exists()

    def test_no_durable_store_package(self):
        assert not (KERNEL_DIR.parent / "store").exists()
