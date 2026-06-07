"""Focused tests for RUNTIME-IMPL-PR-7: persistence boundary skeleton."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from astra_runtime.kernel.persistence_boundary import (
    ALLOWED_OPERATION_TYPES,
    ALLOWED_RESULT_STATUSES,
    InvalidPersistenceBoundaryRequestError,
    InvalidPersistenceBoundaryResultError,
    PersistenceBoundaryError,
    PersistenceBoundaryRequest,
    PersistenceBoundaryResult,
    create_persistence_boundary_request,
    create_persistence_boundary_result,
    validate_persistence_boundary_request,
    validate_persistence_boundary_result,
)

KERNEL_DIR = Path(__file__).resolve().parent.parent.parent / "src" / "astra_runtime" / "kernel"


class TestPersistenceBoundaryRequest:
    def test_valid_creation(self):
        req = create_persistence_boundary_request(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:entity:hero-001",
        )
        assert isinstance(req, PersistenceBoundaryRequest)

    def test_preserves_request_id(self):
        req = create_persistence_boundary_request(
            request_id="req-002",
            operation_type="event_append_prepare",
            subject_ref="astra:event:ev-001",
        )
        assert req.request_id == "req-002"

    def test_preserves_operation_type(self):
        req = create_persistence_boundary_request(
            request_id="req-003",
            operation_type="trace_capture_prepare",
            subject_ref="astra:trace:tr-001",
        )
        assert req.operation_type == "trace_capture_prepare"

    def test_preserves_subject_ref(self):
        req = create_persistence_boundary_request(
            request_id="req-004",
            operation_type="audit_snapshot_prepare",
            subject_ref="astra:audit:aud-001",
        )
        assert req.subject_ref == "astra:audit:aud-001"

    @pytest.mark.parametrize("op", sorted(ALLOWED_OPERATION_TYPES))
    def test_allowed_operation_types(self, op):
        req = create_persistence_boundary_request(
            request_id="req-op",
            operation_type=op,
            subject_ref="astra:test:t-001",
        )
        assert req.operation_type == op

    def test_unsupported_operation_type_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            create_persistence_boundary_request(
                request_id="req-bad",
                operation_type="write_to_disk",
                subject_ref="astra:test:t-001",
            )

    def test_empty_request_id_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            create_persistence_boundary_request(
                request_id="",
                operation_type="record_snapshot_prepare",
                subject_ref="astra:test:t-001",
            )

    def test_empty_subject_ref_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            create_persistence_boundary_request(
                request_id="req-001",
                operation_type="record_snapshot_prepare",
                subject_ref="",
            )

    def test_non_mapping_payload_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            create_persistence_boundary_request(
                request_id="req-001",
                operation_type="record_snapshot_prepare",
                subject_ref="astra:test:t-001",
                payload="not a mapping",
            )

    def test_non_mapping_metadata_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            create_persistence_boundary_request(
                request_id="req-001",
                operation_type="record_snapshot_prepare",
                subject_ref="astra:test:t-001",
                metadata=["not", "a", "mapping"],
            )

    def test_payload_defaults_to_empty_mapping(self):
        req = create_persistence_boundary_request(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:test:t-001",
        )
        assert dict(req.payload) == {}

    def test_metadata_defaults_to_empty_mapping(self):
        req = create_persistence_boundary_request(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:test:t-001",
        )
        assert dict(req.metadata) == {}

    def test_payload_deep_copy_safe(self):
        original = {"nested": {"key": "value"}}
        req = create_persistence_boundary_request(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:test:t-001",
            payload=original,
        )
        original["nested"]["key"] = "mutated"
        assert dict(req.payload)["nested"]["key"] == "value"

    def test_metadata_deep_copy_safe(self):
        original = {"nested": {"key": "value"}}
        req = create_persistence_boundary_request(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:test:t-001",
            metadata=original,
        )
        original["nested"]["key"] = "mutated"
        assert dict(req.metadata)["nested"]["key"] == "value"

    def test_to_dict_returns_deep_copies(self):
        req = create_persistence_boundary_request(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:test:t-001",
            payload={"nested": {"key": "value"}},
        )
        d1 = req.to_dict()
        d2 = req.to_dict()
        d1["payload"]["nested"]["key"] = "mutated"
        assert d2["payload"]["nested"]["key"] == "value"

    def test_validate_accepts_valid(self):
        req = create_persistence_boundary_request(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:test:t-001",
        )
        assert validate_persistence_boundary_request(req) is True

    def test_validate_rejects_invalid(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            validate_persistence_boundary_request("not a request")

    def test_frozen_immutability(self):
        req = create_persistence_boundary_request(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:test:t-001",
        )
        with pytest.raises(Exception):
            req.request_id = "mutated"


class TestPersistenceBoundaryResult:
    def test_valid_creation(self):
        res = create_persistence_boundary_result(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            status="prepared",
            subject_ref="astra:entity:hero-001",
        )
        assert isinstance(res, PersistenceBoundaryResult)

    @pytest.mark.parametrize("status", sorted(ALLOWED_RESULT_STATUSES))
    def test_allowed_statuses(self, status):
        res = create_persistence_boundary_result(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            status=status,
            subject_ref="astra:test:t-001",
        )
        assert res.status == status

    def test_unsupported_status_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            create_persistence_boundary_result(
                request_id="req-001",
                operation_type="record_snapshot_prepare",
                status="committed",
                subject_ref="astra:test:t-001",
            )

    def test_unsupported_operation_type_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            create_persistence_boundary_result(
                request_id="req-001",
                operation_type="save_to_disk",
                status="prepared",
                subject_ref="astra:test:t-001",
            )

    def test_empty_request_id_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            create_persistence_boundary_result(
                request_id="",
                operation_type="record_snapshot_prepare",
                status="prepared",
                subject_ref="astra:test:t-001",
            )

    def test_empty_subject_ref_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            create_persistence_boundary_result(
                request_id="req-001",
                operation_type="record_snapshot_prepare",
                status="prepared",
                subject_ref="",
            )

    def test_non_mapping_metadata_rejected(self):
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            create_persistence_boundary_result(
                request_id="req-001",
                operation_type="record_snapshot_prepare",
                status="prepared",
                subject_ref="astra:test:t-001",
                metadata=42,
            )

    def test_metadata_defaults_to_empty_mapping(self):
        res = create_persistence_boundary_result(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            status="prepared",
            subject_ref="astra:test:t-001",
        )
        assert dict(res.metadata) == {}

    def test_to_dict_returns_deep_copies(self):
        res = create_persistence_boundary_result(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            status="prepared",
            subject_ref="astra:test:t-001",
            metadata={"nested": {"key": "value"}},
        )
        d1 = res.to_dict()
        d2 = res.to_dict()
        d1["metadata"]["nested"]["key"] = "mutated"
        assert d2["metadata"]["nested"]["key"] == "value"

    def test_validate_accepts_valid(self):
        res = create_persistence_boundary_result(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            status="prepared",
            subject_ref="astra:test:t-001",
        )
        assert validate_persistence_boundary_result(res) is True

    def test_validate_rejects_invalid(self):
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            validate_persistence_boundary_result("not a result")

    def test_frozen_immutability(self):
        res = create_persistence_boundary_result(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            status="prepared",
            subject_ref="astra:test:t-001",
        )
        with pytest.raises(Exception):
            res.status = "mutated"


class TestPersistenceBoundaryMalformedDataclass:
    """Tests for manually constructed malformed dataclasses caught by validators."""

    def test_whitespace_only_request_id_rejected_by_factory(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            create_persistence_boundary_request(
                request_id="   ",
                operation_type="record_snapshot_prepare",
                subject_ref="astra:test:t-001",
            )

    def test_whitespace_only_subject_ref_rejected_by_factory(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            create_persistence_boundary_request(
                request_id="req-001",
                operation_type="record_snapshot_prepare",
                subject_ref="  \t  ",
            )

    def test_non_string_request_id_rejected_by_factory(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            create_persistence_boundary_request(
                request_id=123,
                operation_type="record_snapshot_prepare",
                subject_ref="astra:test:t-001",
            )

    def test_non_string_subject_ref_rejected_by_factory(self):
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            create_persistence_boundary_request(
                request_id="req-001",
                operation_type="record_snapshot_prepare",
                subject_ref=None,
            )

    def test_validate_request_rejects_whitespace_request_id(self):
        obj = PersistenceBoundaryRequest(
            request_id="   ",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:test:t-001",
        )
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            validate_persistence_boundary_request(obj)

    def test_validate_request_rejects_whitespace_subject_ref(self):
        obj = PersistenceBoundaryRequest(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="\n\t",
        )
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            validate_persistence_boundary_request(obj)

    def test_validate_request_rejects_non_string_request_id(self):
        obj = object.__new__(PersistenceBoundaryRequest)
        object.__setattr__(obj, "request_id", 999)
        object.__setattr__(obj, "operation_type", "record_snapshot_prepare")
        object.__setattr__(obj, "subject_ref", "astra:test:t-001")
        object.__setattr__(obj, "payload", {})
        object.__setattr__(obj, "metadata", {})
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            validate_persistence_boundary_request(obj)

    def test_validate_request_rejects_invalid_operation_type(self):
        obj = PersistenceBoundaryRequest(
            request_id="req-001",
            operation_type="write_to_disk",
            subject_ref="astra:test:t-001",
        )
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            validate_persistence_boundary_request(obj)

    def test_validate_request_rejects_non_mapping_payload(self):
        obj = object.__new__(PersistenceBoundaryRequest)
        object.__setattr__(obj, "request_id", "req-001")
        object.__setattr__(obj, "operation_type", "record_snapshot_prepare")
        object.__setattr__(obj, "subject_ref", "astra:test:t-001")
        object.__setattr__(obj, "payload", "not a mapping")
        object.__setattr__(obj, "metadata", {})
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            validate_persistence_boundary_request(obj)

    def test_validate_request_rejects_non_mapping_metadata(self):
        obj = object.__new__(PersistenceBoundaryRequest)
        object.__setattr__(obj, "request_id", "req-001")
        object.__setattr__(obj, "operation_type", "record_snapshot_prepare")
        object.__setattr__(obj, "subject_ref", "astra:test:t-001")
        object.__setattr__(obj, "payload", {})
        object.__setattr__(obj, "metadata", [1, 2, 3])
        with pytest.raises(InvalidPersistenceBoundaryRequestError):
            validate_persistence_boundary_request(obj)

    def test_validate_result_rejects_whitespace_request_id(self):
        obj = PersistenceBoundaryResult(
            request_id="   ",
            operation_type="record_snapshot_prepare",
            status="prepared",
            subject_ref="astra:test:t-001",
        )
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            validate_persistence_boundary_result(obj)

    def test_validate_result_rejects_invalid_operation_type(self):
        obj = PersistenceBoundaryResult(
            request_id="req-001",
            operation_type="bad_op",
            status="prepared",
            subject_ref="astra:test:t-001",
        )
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            validate_persistence_boundary_result(obj)

    def test_validate_result_rejects_invalid_status(self):
        obj = PersistenceBoundaryResult(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            status="committed",
            subject_ref="astra:test:t-001",
        )
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            validate_persistence_boundary_result(obj)

    def test_validate_result_rejects_non_mapping_metadata(self):
        obj = object.__new__(PersistenceBoundaryResult)
        object.__setattr__(obj, "request_id", "req-001")
        object.__setattr__(obj, "operation_type", "record_snapshot_prepare")
        object.__setattr__(obj, "status", "prepared")
        object.__setattr__(obj, "subject_ref", "astra:test:t-001")
        object.__setattr__(obj, "metadata", 42)
        with pytest.raises(InvalidPersistenceBoundaryResultError):
            validate_persistence_boundary_result(obj)


class TestPersistenceBoundaryGuardrails:
    def test_no_write_read_save_load_methods(self):
        req = create_persistence_boundary_request(
            request_id="req-001",
            operation_type="record_snapshot_prepare",
            subject_ref="astra:test:t-001",
        )
        forbidden = [
            "write", "read", "save", "load", "connect", "database",
            "file", "path", "append", "persist", "store", "serialize",
        ]
        for method_name in forbidden:
            assert not hasattr(req, method_name), f"{method_name} method must not exist"

    def test_no_context_packet_compiler_module(self):
        assert not (KERNEL_DIR / "context_packet_compiler.py").exists()

    def test_no_domain_service_package(self):
        assert not (KERNEL_DIR.parent / "domain").exists()

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
