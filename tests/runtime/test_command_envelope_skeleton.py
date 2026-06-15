"""Tests for command envelope skeleton — RUNTIME-IMPL-PR-2."""

import os

import pytest

from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    InvalidCommandEnvelopeError,
    create_command_envelope,
    validate_command_envelope,
)

VALID_ACTOR = "astra:actor:player-01"


class TestCreateCommandEnvelope:
    def test_valid_creation(self):
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR)
        assert isinstance(env, CommandEnvelope)

    def test_preserves_command_id(self):
        env = create_command_envelope("cmd-42", "attack", VALID_ACTOR)
        assert env.command_id == "cmd-42"

    def test_preserves_command_type(self):
        env = create_command_envelope("cmd-1", "cast_spell", VALID_ACTOR)
        assert env.command_type == "cast_spell"

    def test_preserves_source_actor_id(self):
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR)
        assert env.source_actor_id == VALID_ACTOR

    def test_payload_defaults_to_empty_mapping(self):
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR)
        assert dict(env.payload) == {}

    def test_metadata_defaults_to_empty_mapping(self):
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR)
        assert dict(env.metadata) == {}

    def test_payload_copy_safe(self):
        original = {"target": "north"}
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR, payload=original)
        original["target"] = "south"
        assert env.payload["target"] == "north"

    def test_payload_nested_copy_safe(self):
        original = {"options": {"verbose": True}}
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR, payload=original)
        original["options"]["verbose"] = False
        assert env.payload["options"]["verbose"] is True

    def test_metadata_copy_safe(self):
        original = {"timestamp": "t0"}
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR, metadata=original)
        original["timestamp"] = "t1"
        assert env.metadata["timestamp"] == "t0"

    def test_metadata_nested_copy_safe(self):
        original = {"context": {"session": "s1"}}
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR, metadata=original)
        original["context"]["session"] = "s2"
        assert env.metadata["context"]["session"] == "s1"

    def test_reject_empty_command_id(self):
        with pytest.raises(InvalidCommandEnvelopeError):
            create_command_envelope("", "move", VALID_ACTOR)

    def test_reject_whitespace_command_id(self):
        with pytest.raises(InvalidCommandEnvelopeError):
            create_command_envelope("   ", "move", VALID_ACTOR)

    def test_reject_empty_command_type(self):
        with pytest.raises(InvalidCommandEnvelopeError):
            create_command_envelope("cmd-1", "", VALID_ACTOR)

    def test_reject_whitespace_command_type(self):
        with pytest.raises(InvalidCommandEnvelopeError):
            create_command_envelope("cmd-1", "   ", VALID_ACTOR)

    def test_reject_invalid_source_actor_id(self):
        with pytest.raises(InvalidCommandEnvelopeError):
            create_command_envelope("cmd-1", "move", "bad-id")

    def test_reject_non_mapping_payload(self):
        with pytest.raises(InvalidCommandEnvelopeError):
            create_command_envelope("cmd-1", "move", VALID_ACTOR, payload="not-a-mapping")

    def test_reject_non_mapping_metadata(self):
        with pytest.raises(InvalidCommandEnvelopeError):
            create_command_envelope("cmd-1", "move", VALID_ACTOR, metadata=42)

    def test_custom_payload_preserved(self):
        env = create_command_envelope(
            "cmd-1", "move", VALID_ACTOR, payload={"direction": "north", "speed": 5}
        )
        assert env.payload["direction"] == "north"
        assert env.payload["speed"] == 5

    def test_custom_metadata_preserved(self):
        env = create_command_envelope(
            "cmd-1", "move", VALID_ACTOR, metadata={"session": "s-1"}
        )
        assert env.metadata["session"] == "s-1"


class TestCommandEnvelopeToDict:
    def test_to_dict_returns_dict(self):
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR)
        result = env.to_dict()
        assert isinstance(result, dict)
        assert result["command_id"] == "cmd-1"
        assert result["command_type"] == "move"
        assert result["source_actor_id"] == VALID_ACTOR
        assert result["payload"] == {}
        assert result["metadata"] == {}

    def test_to_dict_with_payload(self):
        env = create_command_envelope(
            "cmd-1", "move", VALID_ACTOR, payload={"x": 1}
        )
        result = env.to_dict()
        assert result["payload"] == {"x": 1}

    def test_to_dict_returns_deep_copy(self):
        env = create_command_envelope(
            "cmd-1", "move", VALID_ACTOR, payload={"nested": {"a": 1}}
        )
        result = env.to_dict()
        result["payload"]["nested"]["a"] = 999
        assert env.payload["nested"]["a"] == 1


class TestValidateCommandEnvelope:
    def test_valid_envelope_accepted(self):
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR)
        assert validate_command_envelope(env) is True

    def test_invalid_object_rejected(self):
        assert validate_command_envelope("not-an-envelope") is False

    def test_none_rejected(self):
        assert validate_command_envelope(None) is False

    def test_dict_rejected(self):
        assert validate_command_envelope({"command_id": "cmd-1"}) is False


class TestCommandEnvelopeImmutability:
    def test_frozen_dataclass(self):
        env = create_command_envelope("cmd-1", "move", VALID_ACTOR)
        with pytest.raises(AttributeError):
            env.command_id = "changed"


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
            "validation_integration_bridge_skeleton.py",
            "transaction_preview_packet_bridge_skeleton.py", "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py", "scene_command_execution_skeleton.py", "command_kind_routing_skeleton.py", "__pycache__"}
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
