"""Tests for state delta envelope skeleton — RUNTIME-IMPL-PR-3."""

import os

import pytest

from astra_runtime.kernel.state_delta import (
    InvalidStateDeltaError,
    StateDeltaEnvelope,
    create_state_delta_envelope,
    validate_state_delta_envelope,
)

VALID_RECORD = "astra:entity:npc-01"
VALID_RECORD_2 = "astra:entity:npc-02"


class TestCreateStateDeltaEnvelope:
    def test_valid_creation(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1")
        assert isinstance(env, StateDeltaEnvelope)

    def test_preserves_delta_id(self):
        env = create_state_delta_envelope("d-42", "cmd-1", "prev-1")
        assert env.delta_id == "d-42"

    def test_preserves_source_command_id(self):
        env = create_state_delta_envelope("d-1", "cmd-99", "prev-1")
        assert env.source_command_id == "cmd-99"

    def test_preserves_source_preview_id(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-77")
        assert env.source_preview_id == "prev-77"

    def test_preserves_change_type(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1", change_type="record_create")
        assert env.change_type == "record_create"

    def test_affected_record_ids_normalize_to_tuple(self):
        env = create_state_delta_envelope(
            "d-1", "cmd-1", "prev-1", affected_record_ids=[VALID_RECORD, VALID_RECORD_2]
        )
        assert isinstance(env.affected_record_ids, tuple)
        assert env.affected_record_ids == (VALID_RECORD, VALID_RECORD_2)

    def test_valid_affected_record_ids_accepted(self):
        env = create_state_delta_envelope(
            "d-1", "cmd-1", "prev-1", affected_record_ids=[VALID_RECORD]
        )
        assert env.affected_record_ids == (VALID_RECORD,)

    def test_invalid_affected_record_ids_rejected(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope(
                "d-1", "cmd-1", "prev-1", affected_record_ids=["bad-id"]
            )

    def test_allowed_change_types_accepted(self):
        for ct in ["record_update", "record_create", "record_remove",
                    "relationship_update", "visibility_update"]:
            env = create_state_delta_envelope("d-1", "cmd-1", "prev-1", change_type=ct)
            assert env.change_type == ct

    def test_unsupported_change_type_rejected(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope("d-1", "cmd-1", "prev-1", change_type="delete_all")

    def test_payload_defaults_to_empty_mapping(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1")
        assert dict(env.payload) == {}

    def test_metadata_defaults_to_empty_mapping(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1")
        assert dict(env.metadata) == {}

    def test_payload_copy_safe(self):
        original = {"field": "old"}
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1", payload=original)
        original["field"] = "new"
        assert env.payload["field"] == "old"

    def test_payload_nested_copy_safe(self):
        original = {"nested": {"a": 1}}
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1", payload=original)
        original["nested"]["a"] = 999
        assert env.payload["nested"]["a"] == 1

    def test_metadata_copy_safe(self):
        original = {"ts": "t0"}
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1", metadata=original)
        original["ts"] = "t1"
        assert env.metadata["ts"] == "t0"

    def test_metadata_nested_copy_safe(self):
        original = {"ctx": {"k": "v"}}
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1", metadata=original)
        original["ctx"]["k"] = "changed"
        assert env.metadata["ctx"]["k"] == "v"

    def test_reject_empty_delta_id(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope("", "cmd-1", "prev-1")

    def test_reject_whitespace_delta_id(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope("   ", "cmd-1", "prev-1")

    def test_reject_empty_source_command_id(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope("d-1", "", "prev-1")

    def test_reject_whitespace_source_command_id(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope("d-1", "   ", "prev-1")

    def test_reject_empty_source_preview_id(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope("d-1", "cmd-1", "")

    def test_reject_whitespace_source_preview_id(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope("d-1", "cmd-1", "   ")

    def test_reject_non_mapping_payload(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope("d-1", "cmd-1", "prev-1", payload="not-a-mapping")

    def test_reject_non_mapping_metadata(self):
        with pytest.raises(InvalidStateDeltaError):
            create_state_delta_envelope("d-1", "cmd-1", "prev-1", metadata=42)

    def test_default_affected_record_ids_empty_tuple(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1")
        assert env.affected_record_ids == ()

    def test_custom_payload_preserved(self):
        env = create_state_delta_envelope(
            "d-1", "cmd-1", "prev-1", payload={"hp": 10, "name": "goblin"}
        )
        assert env.payload["hp"] == 10
        assert env.payload["name"] == "goblin"


class TestStateDeltaEnvelopeToDict:
    def test_to_dict_returns_dict(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1")
        result = env.to_dict()
        assert isinstance(result, dict)
        assert result["delta_id"] == "d-1"
        assert result["source_command_id"] == "cmd-1"
        assert result["source_preview_id"] == "prev-1"
        assert result["affected_record_ids"] == []
        assert result["change_type"] == "record_update"
        assert result["payload"] == {}
        assert result["metadata"] == {}

    def test_to_dict_with_affected_records(self):
        env = create_state_delta_envelope(
            "d-1", "cmd-1", "prev-1", affected_record_ids=[VALID_RECORD]
        )
        result = env.to_dict()
        assert result["affected_record_ids"] == [VALID_RECORD]

    def test_to_dict_returns_deep_copy(self):
        env = create_state_delta_envelope(
            "d-1", "cmd-1", "prev-1", payload={"nested": {"b": 2}}
        )
        result = env.to_dict()
        result["payload"]["nested"]["b"] = 999
        assert env.payload["nested"]["b"] == 2

    def test_to_dict_metadata_deep_copy(self):
        env = create_state_delta_envelope(
            "d-1", "cmd-1", "prev-1", metadata={"nested": {"c": 3}}
        )
        result = env.to_dict()
        result["metadata"]["nested"]["c"] = 999
        assert env.metadata["nested"]["c"] == 3


class TestValidateStateDeltaEnvelope:
    def test_valid_envelope_accepted(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1")
        assert validate_state_delta_envelope(env) is True

    def test_invalid_object_rejected(self):
        assert validate_state_delta_envelope("not-an-envelope") is False

    def test_none_rejected(self):
        assert validate_state_delta_envelope(None) is False

    def test_dict_rejected(self):
        assert validate_state_delta_envelope({"delta_id": "d-1"}) is False


class TestStateDeltaEnvelopeImmutability:
    def test_frozen_dataclass(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1")
        with pytest.raises(AttributeError):
            env.delta_id = "changed"


class TestNoStateApplicationMethod:
    """State delta envelope must not contain state application/mutation methods."""

    def test_no_apply_method(self):
        env = create_state_delta_envelope("d-1", "cmd-1", "prev-1")
        assert not hasattr(env, "apply")
        assert not hasattr(env, "apply_delta")
        assert not hasattr(env, "commit")
        assert not hasattr(env, "mutate")
        assert not hasattr(env, "execute")


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
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "transaction_lifecycle.py", "event_commitment.py", "validation_integration.py", "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py", "scene_command_execution_skeleton.py", "__pycache__"}
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
