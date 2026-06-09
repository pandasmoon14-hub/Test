"""Focused tests for RUNTIME-IMPL-PR-7: replay/hash audit skeleton."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from astra_runtime.kernel.replay_audit import (
    ALLOWED_HASH_ALGORITHMS,
    HashAuditRecord,
    InvalidHashAuditRecordError,
    InvalidReplayAuditRecordError,
    ReplayAuditError,
    ReplayAuditRecord,
    canonical_payload_hash,
    create_hash_audit_record,
    create_replay_audit_record,
    validate_hash_audit_record,
    validate_replay_audit_record,
)

KERNEL_DIR = Path(__file__).resolve().parent.parent.parent / "src" / "astra_runtime" / "kernel"


class TestReplayAuditRecord:
    def test_valid_creation(self):
        rec = create_replay_audit_record(
            replay_id="replay-001",
            source_ref="astra:event:ev-001",
            sequence=0,
            expected_hash="abc123",
        )
        assert isinstance(rec, ReplayAuditRecord)

    def test_preserves_fields(self):
        rec = create_replay_audit_record(
            replay_id="replay-002",
            source_ref="astra:event:ev-002",
            sequence=5,
            expected_hash="def456",
        )
        assert rec.replay_id == "replay-002"
        assert rec.source_ref == "astra:event:ev-002"
        assert rec.sequence == 5
        assert rec.expected_hash == "def456"

    def test_empty_replay_id_rejected(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id="",
                source_ref="astra:event:ev-001",
                sequence=0,
                expected_hash="abc123",
            )

    def test_empty_source_ref_rejected(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id="replay-001",
                source_ref="",
                sequence=0,
                expected_hash="abc123",
            )

    def test_negative_sequence_rejected(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id="replay-001",
                source_ref="astra:event:ev-001",
                sequence=-1,
                expected_hash="abc123",
            )

    def test_bool_sequence_rejected(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id="replay-001",
                source_ref="astra:event:ev-001",
                sequence=True,
                expected_hash="abc123",
            )

    def test_empty_expected_hash_rejected(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id="replay-001",
                source_ref="astra:event:ev-001",
                sequence=0,
                expected_hash="",
            )

    def test_metadata_defaults_to_empty_mapping(self):
        rec = create_replay_audit_record(
            replay_id="replay-001",
            source_ref="astra:event:ev-001",
            sequence=0,
            expected_hash="abc123",
        )
        assert dict(rec.metadata) == {}

    def test_metadata_deep_copy_safe(self):
        original = {"nested": {"key": "value"}}
        rec = create_replay_audit_record(
            replay_id="replay-001",
            source_ref="astra:event:ev-001",
            sequence=0,
            expected_hash="abc123",
            metadata=original,
        )
        original["nested"]["key"] = "mutated"
        assert dict(rec.metadata)["nested"]["key"] == "value"

    def test_to_dict_returns_deep_copies(self):
        rec = create_replay_audit_record(
            replay_id="replay-001",
            source_ref="astra:event:ev-001",
            sequence=0,
            expected_hash="abc123",
            metadata={"nested": {"key": "value"}},
        )
        d1 = rec.to_dict()
        d2 = rec.to_dict()
        d1["metadata"]["nested"]["key"] = "mutated"
        assert d2["metadata"]["nested"]["key"] == "value"

    def test_validate_accepts_valid(self):
        rec = create_replay_audit_record(
            replay_id="replay-001",
            source_ref="astra:event:ev-001",
            sequence=0,
            expected_hash="abc123",
        )
        assert validate_replay_audit_record(rec) is True

    def test_validate_rejects_invalid(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            validate_replay_audit_record("not a record")

    def test_frozen_immutability(self):
        rec = create_replay_audit_record(
            replay_id="replay-001",
            source_ref="astra:event:ev-001",
            sequence=0,
            expected_hash="abc123",
        )
        with pytest.raises(Exception):
            rec.replay_id = "mutated"


class TestHashAuditRecord:
    def test_valid_creation(self):
        rec = create_hash_audit_record(
            hash_id="hash-001",
            source_ref="astra:event:ev-001",
            hash_algorithm="sha256",
            payload_hash="abc123def456",
        )
        assert isinstance(rec, HashAuditRecord)

    def test_preserves_fields(self):
        rec = create_hash_audit_record(
            hash_id="hash-002",
            source_ref="astra:event:ev-002",
            hash_algorithm="sha256",
            payload_hash="xyz789",
        )
        assert rec.hash_id == "hash-002"
        assert rec.source_ref == "astra:event:ev-002"
        assert rec.hash_algorithm == "sha256"
        assert rec.payload_hash == "xyz789"

    def test_empty_hash_id_rejected(self):
        with pytest.raises(InvalidHashAuditRecordError):
            create_hash_audit_record(
                hash_id="",
                source_ref="astra:event:ev-001",
                hash_algorithm="sha256",
                payload_hash="abc123",
            )

    def test_empty_source_ref_rejected(self):
        with pytest.raises(InvalidHashAuditRecordError):
            create_hash_audit_record(
                hash_id="hash-001",
                source_ref="",
                hash_algorithm="sha256",
                payload_hash="abc123",
            )

    def test_unsupported_algorithm_rejected(self):
        with pytest.raises(InvalidHashAuditRecordError):
            create_hash_audit_record(
                hash_id="hash-001",
                source_ref="astra:event:ev-001",
                hash_algorithm="md5",
                payload_hash="abc123",
            )

    def test_empty_payload_hash_rejected(self):
        with pytest.raises(InvalidHashAuditRecordError):
            create_hash_audit_record(
                hash_id="hash-001",
                source_ref="astra:event:ev-001",
                hash_algorithm="sha256",
                payload_hash="",
            )

    def test_metadata_defaults_to_empty_mapping(self):
        rec = create_hash_audit_record(
            hash_id="hash-001",
            source_ref="astra:event:ev-001",
            hash_algorithm="sha256",
            payload_hash="abc123",
        )
        assert dict(rec.metadata) == {}

    def test_metadata_deep_copy_safe(self):
        original = {"nested": {"key": "value"}}
        rec = create_hash_audit_record(
            hash_id="hash-001",
            source_ref="astra:event:ev-001",
            hash_algorithm="sha256",
            payload_hash="abc123",
            metadata=original,
        )
        original["nested"]["key"] = "mutated"
        assert dict(rec.metadata)["nested"]["key"] == "value"

    def test_to_dict_returns_deep_copies(self):
        rec = create_hash_audit_record(
            hash_id="hash-001",
            source_ref="astra:event:ev-001",
            hash_algorithm="sha256",
            payload_hash="abc123",
            metadata={"nested": {"key": "value"}},
        )
        d1 = rec.to_dict()
        d2 = rec.to_dict()
        d1["metadata"]["nested"]["key"] = "mutated"
        assert d2["metadata"]["nested"]["key"] == "value"

    def test_validate_accepts_valid(self):
        rec = create_hash_audit_record(
            hash_id="hash-001",
            source_ref="astra:event:ev-001",
            hash_algorithm="sha256",
            payload_hash="abc123",
        )
        assert validate_hash_audit_record(rec) is True

    def test_validate_rejects_invalid(self):
        with pytest.raises(InvalidHashAuditRecordError):
            validate_hash_audit_record("not a record")


class TestCanonicalPayloadHash:
    def test_deterministic_same_mapping_different_key_order(self):
        h1 = canonical_payload_hash({"b": 2, "a": 1})
        h2 = canonical_payload_hash({"a": 1, "b": 2})
        assert h1 == h2

    def test_changes_when_payload_changes(self):
        h1 = canonical_payload_hash({"key": "value1"})
        h2 = canonical_payload_hash({"key": "value2"})
        assert h1 != h2

    def test_rejects_unsupported_algorithm(self):
        with pytest.raises(ReplayAuditError):
            canonical_payload_hash({"key": "value"}, algorithm="md5")

    def test_rejects_non_json_serializable(self):
        with pytest.raises(ReplayAuditError):
            canonical_payload_hash({"key": object()})

    def test_accepts_string(self):
        h = canonical_payload_hash("hello")
        assert isinstance(h, str) and len(h) == 64

    def test_accepts_int(self):
        h = canonical_payload_hash(42)
        assert isinstance(h, str) and len(h) == 64

    def test_accepts_list(self):
        h = canonical_payload_hash([1, 2, 3])
        assert isinstance(h, str) and len(h) == 64

    def test_accepts_none(self):
        h = canonical_payload_hash(None)
        assert isinstance(h, str) and len(h) == 64

    def test_accepts_nested_mapping(self):
        h = canonical_payload_hash({"a": {"b": [1, 2]}})
        assert isinstance(h, str) and len(h) == 64


class TestReplayAuditMalformedDataclass:
    """Tests for manually constructed malformed dataclasses caught by validators."""

    def test_whitespace_only_replay_id_rejected_by_factory(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id="   ",
                source_ref="astra:event:ev-001",
                sequence=0,
                expected_hash="abc123",
            )

    def test_whitespace_only_source_ref_rejected_by_factory(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id="replay-001",
                source_ref="\t\n",
                sequence=0,
                expected_hash="abc123",
            )

    def test_whitespace_only_expected_hash_rejected_by_factory(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id="replay-001",
                source_ref="astra:event:ev-001",
                sequence=0,
                expected_hash="   ",
            )

    def test_non_string_replay_id_rejected_by_factory(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id=42,
                source_ref="astra:event:ev-001",
                sequence=0,
                expected_hash="abc123",
            )

    def test_non_string_source_ref_rejected_by_factory(self):
        with pytest.raises(InvalidReplayAuditRecordError):
            create_replay_audit_record(
                replay_id="replay-001",
                source_ref=None,
                sequence=0,
                expected_hash="abc123",
            )

    def test_validate_replay_rejects_whitespace_replay_id(self):
        obj = ReplayAuditRecord(
            replay_id="   ",
            source_ref="astra:event:ev-001",
            sequence=0,
            expected_hash="abc123",
        )
        with pytest.raises(InvalidReplayAuditRecordError):
            validate_replay_audit_record(obj)

    def test_validate_replay_rejects_non_string_replay_id(self):
        obj = object.__new__(ReplayAuditRecord)
        object.__setattr__(obj, "replay_id", 123)
        object.__setattr__(obj, "source_ref", "astra:event:ev-001")
        object.__setattr__(obj, "sequence", 0)
        object.__setattr__(obj, "expected_hash", "abc123")
        object.__setattr__(obj, "metadata", {})
        with pytest.raises(InvalidReplayAuditRecordError):
            validate_replay_audit_record(obj)

    def test_validate_replay_rejects_bool_sequence(self):
        obj = object.__new__(ReplayAuditRecord)
        object.__setattr__(obj, "replay_id", "replay-001")
        object.__setattr__(obj, "source_ref", "astra:event:ev-001")
        object.__setattr__(obj, "sequence", True)
        object.__setattr__(obj, "expected_hash", "abc123")
        object.__setattr__(obj, "metadata", {})
        with pytest.raises(InvalidReplayAuditRecordError):
            validate_replay_audit_record(obj)

    def test_validate_replay_rejects_non_mapping_metadata(self):
        obj = object.__new__(ReplayAuditRecord)
        object.__setattr__(obj, "replay_id", "replay-001")
        object.__setattr__(obj, "source_ref", "astra:event:ev-001")
        object.__setattr__(obj, "sequence", 0)
        object.__setattr__(obj, "expected_hash", "abc123")
        object.__setattr__(obj, "metadata", "not a mapping")
        with pytest.raises(InvalidReplayAuditRecordError):
            validate_replay_audit_record(obj)

    def test_whitespace_only_hash_id_rejected_by_factory(self):
        with pytest.raises(InvalidHashAuditRecordError):
            create_hash_audit_record(
                hash_id="   ",
                source_ref="astra:event:ev-001",
                hash_algorithm="sha256",
                payload_hash="abc123",
            )

    def test_whitespace_only_payload_hash_rejected_by_factory(self):
        with pytest.raises(InvalidHashAuditRecordError):
            create_hash_audit_record(
                hash_id="hash-001",
                source_ref="astra:event:ev-001",
                hash_algorithm="sha256",
                payload_hash="\t  ",
            )

    def test_non_string_hash_id_rejected_by_factory(self):
        with pytest.raises(InvalidHashAuditRecordError):
            create_hash_audit_record(
                hash_id=99,
                source_ref="astra:event:ev-001",
                hash_algorithm="sha256",
                payload_hash="abc123",
            )

    def test_validate_hash_rejects_whitespace_hash_id(self):
        obj = HashAuditRecord(
            hash_id="   ",
            source_ref="astra:event:ev-001",
            hash_algorithm="sha256",
            payload_hash="abc123",
        )
        with pytest.raises(InvalidHashAuditRecordError):
            validate_hash_audit_record(obj)

    def test_validate_hash_rejects_non_string_hash_id(self):
        obj = object.__new__(HashAuditRecord)
        object.__setattr__(obj, "hash_id", 42)
        object.__setattr__(obj, "source_ref", "astra:event:ev-001")
        object.__setattr__(obj, "hash_algorithm", "sha256")
        object.__setattr__(obj, "payload_hash", "abc123")
        object.__setattr__(obj, "metadata", {})
        with pytest.raises(InvalidHashAuditRecordError):
            validate_hash_audit_record(obj)

    def test_validate_hash_rejects_non_mapping_metadata(self):
        obj = object.__new__(HashAuditRecord)
        object.__setattr__(obj, "hash_id", "hash-001")
        object.__setattr__(obj, "source_ref", "astra:event:ev-001")
        object.__setattr__(obj, "hash_algorithm", "sha256")
        object.__setattr__(obj, "payload_hash", "abc123")
        object.__setattr__(obj, "metadata", [1, 2])
        with pytest.raises(InvalidHashAuditRecordError):
            validate_hash_audit_record(obj)


class TestReplayAuditGuardrails:
    def test_no_replay_restore_rebuild_methods(self):
        rec = create_replay_audit_record(
            replay_id="replay-001",
            source_ref="astra:event:ev-001",
            sequence=0,
            expected_hash="abc123",
        )
        forbidden = [
            "replay", "restore", "rebuild", "verify_stream",
            "hash_chain", "store", "save", "load",
        ]
        for method_name in forbidden:
            assert not hasattr(rec, method_name), f"{method_name} method must not exist"

    def test_no_context_packet_compiler_module(self):
        assert not (KERNEL_DIR / "context_packet_compiler.py").exists()

    def test_domain_package_contains_only_authorized_modules(self):
        domain_dir = KERNEL_DIR.parent / "domain"
        assert domain_dir.exists(), "Domain package should exist after PR-1A"
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "__pycache__"}
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
