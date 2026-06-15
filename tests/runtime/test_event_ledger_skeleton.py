"""Tests for event ledger entry skeleton — RUNTIME-IMPL-PR-3."""

import os

import pytest

from astra_runtime.kernel.event_ledger import (
    EventLedgerEntry,
    InvalidEventLedgerEntryError,
    create_event_ledger_entry,
    validate_event_ledger_entry,
)

VALID_ACTOR = "astra:actor:player-01"
VALID_TARGET = "astra:entity:npc-01"


class TestCreateEventLedgerEntry:
    def test_valid_creation(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1"
        )
        assert isinstance(entry, EventLedgerEntry)

    def test_preserves_event_id(self):
        entry = create_event_ledger_entry(
            "evt-42", "command_event", 0, "cmd-1", "prev-1"
        )
        assert entry.event_id == "evt-42"

    def test_preserves_event_type(self):
        entry = create_event_ledger_entry(
            "evt-1", "transaction_event", 0, "cmd-1", "prev-1"
        )
        assert entry.event_type == "transaction_event"

    def test_preserves_sequence(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 7, "cmd-1", "prev-1"
        )
        assert entry.sequence == 7

    def test_preserves_source_command_id(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-99", "prev-1"
        )
        assert entry.source_command_id == "cmd-99"

    def test_preserves_source_preview_id(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-77"
        )
        assert entry.source_preview_id == "prev-77"

    def test_allowed_event_types_accepted(self):
        for et in ["command_event", "transaction_event", "state_delta_event",
                    "validation_event", "system_audit_event"]:
            entry = create_event_ledger_entry("evt-1", et, 0, "cmd-1", "prev-1")
            assert entry.event_type == et

    def test_unsupported_event_type_rejected(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry("evt-1", "unknown_event", 0, "cmd-1", "prev-1")

    def test_sequence_must_be_non_negative(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry("evt-1", "command_event", -1, "cmd-1", "prev-1")

    def test_sequence_zero_accepted(self):
        entry = create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "prev-1")
        assert entry.sequence == 0

    def test_sequence_rejects_float(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry("evt-1", "command_event", 1.5, "cmd-1", "prev-1")

    def test_sequence_rejects_bool(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry("evt-1", "command_event", True, "cmd-1", "prev-1")

    def test_state_delta_ids_normalize_to_tuple(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1",
            state_delta_ids=["d-1", "d-2"],
        )
        assert isinstance(entry.state_delta_ids, tuple)
        assert entry.state_delta_ids == ("d-1", "d-2")

    def test_empty_state_delta_id_rejected(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry(
                "evt-1", "command_event", 0, "cmd-1", "prev-1",
                state_delta_ids=["d-1", ""],
            )

    def test_whitespace_state_delta_id_rejected(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry(
                "evt-1", "command_event", 0, "cmd-1", "prev-1",
                state_delta_ids=["   "],
            )

    def test_actor_ids_normalize_to_tuple(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1",
            actor_ids=[VALID_ACTOR],
        )
        assert isinstance(entry.actor_ids, tuple)
        assert entry.actor_ids == (VALID_ACTOR,)

    def test_target_ids_normalize_to_tuple(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1",
            target_ids=[VALID_TARGET],
        )
        assert isinstance(entry.target_ids, tuple)
        assert entry.target_ids == (VALID_TARGET,)

    def test_valid_actor_ids_accepted(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1",
            actor_ids=[VALID_ACTOR],
        )
        assert entry.actor_ids == (VALID_ACTOR,)

    def test_invalid_actor_ids_rejected(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry(
                "evt-1", "command_event", 0, "cmd-1", "prev-1",
                actor_ids=["bad-id"],
            )

    def test_valid_target_ids_accepted(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1",
            target_ids=[VALID_TARGET],
        )
        assert entry.target_ids == (VALID_TARGET,)

    def test_invalid_target_ids_rejected(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry(
                "evt-1", "command_event", 0, "cmd-1", "prev-1",
                target_ids=["invalid"],
            )

    def test_metadata_defaults_to_empty_mapping(self):
        entry = create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "prev-1")
        assert dict(entry.metadata) == {}

    def test_metadata_copy_safe(self):
        original = {"note": "alpha"}
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1", metadata=original
        )
        original["note"] = "beta"
        assert entry.metadata["note"] == "alpha"

    def test_metadata_nested_copy_safe(self):
        original = {"ctx": {"k": "v"}}
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1", metadata=original
        )
        original["ctx"]["k"] = "changed"
        assert entry.metadata["ctx"]["k"] == "v"

    def test_reject_empty_event_id(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry("", "command_event", 0, "cmd-1", "prev-1")

    def test_reject_whitespace_event_id(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry("   ", "command_event", 0, "cmd-1", "prev-1")

    def test_reject_empty_source_command_id(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry("evt-1", "command_event", 0, "", "prev-1")

    def test_reject_empty_source_preview_id(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "")

    def test_reject_non_mapping_metadata(self):
        with pytest.raises(InvalidEventLedgerEntryError):
            create_event_ledger_entry(
                "evt-1", "command_event", 0, "cmd-1", "prev-1", metadata="bad"
            )

    def test_default_state_delta_ids_empty_tuple(self):
        entry = create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "prev-1")
        assert entry.state_delta_ids == ()

    def test_default_actor_ids_empty_tuple(self):
        entry = create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "prev-1")
        assert entry.actor_ids == ()

    def test_default_target_ids_empty_tuple(self):
        entry = create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "prev-1")
        assert entry.target_ids == ()


class TestEventLedgerEntryToDict:
    def test_to_dict_returns_dict(self):
        entry = create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "prev-1")
        result = entry.to_dict()
        assert isinstance(result, dict)
        assert result["event_id"] == "evt-1"
        assert result["event_type"] == "command_event"
        assert result["sequence"] == 0
        assert result["source_command_id"] == "cmd-1"
        assert result["source_preview_id"] == "prev-1"
        assert result["state_delta_ids"] == []
        assert result["actor_ids"] == []
        assert result["target_ids"] == []
        assert result["metadata"] == {}

    def test_to_dict_with_ids(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1",
            state_delta_ids=["d-1"],
            actor_ids=[VALID_ACTOR],
            target_ids=[VALID_TARGET],
        )
        result = entry.to_dict()
        assert result["state_delta_ids"] == ["d-1"]
        assert result["actor_ids"] == [VALID_ACTOR]
        assert result["target_ids"] == [VALID_TARGET]

    def test_to_dict_returns_deep_copy(self):
        entry = create_event_ledger_entry(
            "evt-1", "command_event", 0, "cmd-1", "prev-1",
            metadata={"nested": {"b": 2}},
        )
        result = entry.to_dict()
        result["metadata"]["nested"]["b"] = 999
        assert entry.metadata["nested"]["b"] == 2


class TestValidateEventLedgerEntry:
    def test_valid_entry_accepted(self):
        entry = create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "prev-1")
        assert validate_event_ledger_entry(entry) is True

    def test_invalid_object_rejected(self):
        assert validate_event_ledger_entry("not-an-entry") is False

    def test_none_rejected(self):
        assert validate_event_ledger_entry(None) is False

    def test_dict_rejected(self):
        assert validate_event_ledger_entry({"event_id": "evt-1"}) is False


class TestEventLedgerEntryImmutability:
    def test_frozen_dataclass(self):
        entry = create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "prev-1")
        with pytest.raises(AttributeError):
            entry.event_id = "changed"


class TestNoAppendStoreReplayMethod:
    """Event ledger entry must not contain append/store/replay/hash methods."""

    def test_no_append_method(self):
        entry = create_event_ledger_entry("evt-1", "command_event", 0, "cmd-1", "prev-1")
        assert not hasattr(entry, "append")
        assert not hasattr(entry, "store")
        assert not hasattr(entry, "replay")
        assert not hasattr(entry, "hash")
        assert not hasattr(entry, "persist")
        assert not hasattr(entry, "save")


class TestNoUnauthorizedModules:
    """Guardrail tests — future modules must not exist yet."""

    KERNEL_DIR = os.path.join(
        os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "kernel"
    )

    def test_domain_package_contains_only_authorized_modules(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "domain"
        )
        assert os.path.isdir(path), "Domain package should exist after PR-1A"
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "transaction_lifecycle.py", "event_commitment.py", "validation_integration.py",
            "validation_integration_bridge_skeleton.py", "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py", "scene_command_execution_skeleton.py", "command_kind_routing_skeleton.py", "__pycache__"}
        actual = set(os.listdir(path))
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized domain modules: {unauthorized}"

    def test_no_model_integration_package(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "model"
        )
        assert not os.path.isdir(path), "Unauthorized model integration package exists"

    def test_no_prompt_template_package(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "prompts"
        )
        assert not os.path.isdir(path), "Unauthorized prompt template package exists"
