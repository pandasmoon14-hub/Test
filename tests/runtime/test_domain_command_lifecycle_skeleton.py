"""Tests for command lifecycle skeleton — RUNTIME-DOMAIN-PR-1A."""

import copy
import os

import pytest

from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    create_command_envelope,
)
from astra_runtime.domain.command_lifecycle import (
    COMMAND_LIFECYCLE_STAGES,
    COMMAND_LIFECYCLE_TERMINAL_STAGES,
    CommandLifecycleError,
    CommandLifecycleResult,
    CommandLifecycleService,
    CommandLifecycleStage,
    InvalidCommandLifecycleResultError,
    InvalidCommandLifecycleStageError,
    create_command_lifecycle_result,
    evaluate_command_lifecycle,
    validate_command_lifecycle_result,
)

VALID_ACTOR = "astra:actor:player-01"


def _make_envelope(**overrides):
    defaults = {"command_id": "cmd-1", "command_type": "move", "source_actor_id": VALID_ACTOR}
    defaults.update(overrides)
    return create_command_envelope(**defaults)


class TestDomainPackageImports:
    def test_import_from_domain_package(self):
        from astra_runtime.domain import (
            COMMAND_LIFECYCLE_STAGES,
            CommandLifecycleResult,
            create_command_lifecycle_result,
            evaluate_command_lifecycle,
            validate_command_lifecycle_result,
        )
        assert len(COMMAND_LIFECYCLE_STAGES) == 12


class TestCommandLifecycleStage:
    def test_valid_creation(self):
        stage = CommandLifecycleStage(
            stage="received", description="Command received", terminal=False,
        )
        assert stage.stage == "received"
        assert stage.terminal is False

    def test_frozen(self):
        stage = CommandLifecycleStage(
            stage="received", description="Command received", terminal=False,
        )
        with pytest.raises(AttributeError):
            stage.stage = "rejected"  # type: ignore[misc]

    def test_to_dict_returns_deep_copy(self):
        meta = {"key": {"nested": True}}
        stage = CommandLifecycleStage(
            stage="received", description="desc", terminal=False, metadata=meta,
        )
        d = stage.to_dict()
        d["metadata"]["key"]["nested"] = False
        assert stage.metadata["key"]["nested"] is True


class TestAllLifecycleStages:
    EXPECTED_STAGES = [
        "received",
        "envelope_validated",
        "actor_bound",
        "visibility_checked",
        "legality_prechecked",
        "dependency_declared",
        "preview_requested",
        "confirmation_required",
        "accepted_for_transaction_planning",
        "rejected",
        "quarantined",
        "cancelled",
    ]

    @pytest.mark.parametrize("stage", EXPECTED_STAGES)
    def test_stage_accepted(self, stage):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage=stage, status="in_progress",
        )
        assert result.stage == stage

    def test_unsupported_stage_rejected(self):
        with pytest.raises(InvalidCommandLifecycleStageError):
            create_command_lifecycle_result(
                lifecycle_id="lc-1", command_id="cmd-1", stage="nonexistent", status="in_progress",
            )

    def test_all_12_stages_present(self):
        assert len(COMMAND_LIFECYCLE_STAGES) == 12


class TestAllowedStatuses:
    EXPECTED_STATUSES = ["in_progress", "accepted", "rejected", "quarantined", "cancelled"]

    @pytest.mark.parametrize("status", EXPECTED_STATUSES)
    def test_status_accepted(self, status):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status=status,
        )
        assert result.status == status

    def test_unsupported_status_rejected(self):
        with pytest.raises(InvalidCommandLifecycleResultError):
            create_command_lifecycle_result(
                lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="unknown",
            )


class TestCreateCommandLifecycleResult:
    def test_valid_creation(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
        )
        assert isinstance(result, CommandLifecycleResult)

    def test_preserves_lifecycle_id(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-42", command_id="cmd-1", stage="received", status="in_progress",
        )
        assert result.lifecycle_id == "lc-42"

    def test_preserves_command_id(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-99", stage="received", status="in_progress",
        )
        assert result.command_id == "cmd-99"

    def test_preserves_stage(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="actor_bound", status="in_progress",
        )
        assert result.stage == "actor_bound"

    def test_preserves_status(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="accepted",
        )
        assert result.status == "accepted"

    def test_preserves_validation_id(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
            validation_id="val-1",
        )
        assert result.validation_id == "val-1"

    def test_preserves_requires_confirmation(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
            requires_confirmation=True,
        )
        assert result.requires_confirmation is True

    def test_preserves_dependencies(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
            downstream_dependencies=["state_service", "event_service"],
        )
        assert result.downstream_dependencies == ("state_service", "event_service")

    def test_preserves_metadata(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
            metadata={"source": "test"},
        )
        assert dict(result.metadata) == {"source": "test"}

    def test_empty_lifecycle_id_rejected(self):
        with pytest.raises(InvalidCommandLifecycleResultError):
            create_command_lifecycle_result(
                lifecycle_id="", command_id="cmd-1", stage="received", status="in_progress",
            )

    def test_whitespace_lifecycle_id_rejected(self):
        with pytest.raises(InvalidCommandLifecycleResultError):
            create_command_lifecycle_result(
                lifecycle_id="   ", command_id="cmd-1", stage="received", status="in_progress",
            )

    def test_empty_command_id_rejected(self):
        with pytest.raises(InvalidCommandLifecycleResultError):
            create_command_lifecycle_result(
                lifecycle_id="lc-1", command_id="", stage="received", status="in_progress",
            )

    def test_non_bool_requires_confirmation_rejected(self):
        with pytest.raises(InvalidCommandLifecycleResultError):
            create_command_lifecycle_result(
                lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
                requires_confirmation=1,  # type: ignore[arg-type]
            )

    def test_validation_id_none_accepted(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
            validation_id=None,
        )
        assert result.validation_id is None

    def test_validation_id_empty_rejected(self):
        with pytest.raises(InvalidCommandLifecycleResultError):
            create_command_lifecycle_result(
                lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
                validation_id="",
            )

    def test_dependency_defaults_to_empty_tuple(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
        )
        assert result.downstream_dependencies == ()

    def test_dependency_list_normalizes_to_tuple(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
            downstream_dependencies=["a", "b"],
        )
        assert isinstance(result.downstream_dependencies, tuple)

    def test_dependency_string_container_rejected(self):
        with pytest.raises(InvalidCommandLifecycleResultError):
            create_command_lifecycle_result(
                lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
                downstream_dependencies="not-a-list",  # type: ignore[arg-type]
            )

    def test_empty_dependency_entry_rejected(self):
        with pytest.raises(InvalidCommandLifecycleResultError):
            create_command_lifecycle_result(
                lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
                downstream_dependencies=["valid", ""],
            )

    def test_metadata_defaults_to_empty_mapping(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
        )
        assert dict(result.metadata) == {}

    def test_metadata_deep_copy_safe(self):
        original = {"nested": {"key": "value"}}
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
            metadata=original,
        )
        original["nested"]["key"] = "changed"
        assert result.metadata["nested"]["key"] == "value"

    def test_to_dict_returns_deep_copy(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
            metadata={"nested": {"key": True}},
        )
        d = result.to_dict()
        d["metadata"]["nested"]["key"] = False
        assert result.metadata["nested"]["key"] is True

    def test_frozen_immutability(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
        )
        with pytest.raises(AttributeError):
            result.lifecycle_id = "lc-2"  # type: ignore[misc]


class TestValidateCommandLifecycleResult:
    def test_accepts_valid_result(self):
        result = create_command_lifecycle_result(
            lifecycle_id="lc-1", command_id="cmd-1", stage="received", status="in_progress",
        )
        assert validate_command_lifecycle_result(result) is True

    def test_rejects_non_result_object(self):
        assert validate_command_lifecycle_result({"lifecycle_id": "lc-1"}) is False

    def test_rejects_none(self):
        assert validate_command_lifecycle_result(None) is False


class TestEvaluateCommandLifecycle:
    def test_accepts_valid_envelope(self):
        env = _make_envelope()
        result = evaluate_command_lifecycle("lc-1", env)
        assert isinstance(result, CommandLifecycleResult)
        assert result.command_id == "cmd-1"
        assert result.stage == "received"
        assert result.status == "in_progress"

    def test_rejects_invalid_envelope(self):
        with pytest.raises(CommandLifecycleError):
            evaluate_command_lifecycle("lc-1", "not-an-envelope")  # type: ignore[arg-type]

    def test_does_not_mutate_command_payload(self):
        payload = {"target": "north"}
        env = _make_envelope(payload=payload)
        payload_before = dict(env.payload)
        evaluate_command_lifecycle("lc-1", env, stage="received", metadata={"x": 1})
        assert dict(env.payload) == payload_before

    def test_does_not_mutate_command_metadata(self):
        meta = {"session": "s1"}
        env = _make_envelope(metadata=meta)
        meta_before = dict(env.metadata)
        evaluate_command_lifecycle("lc-1", env, stage="received")
        assert dict(env.metadata) == meta_before

    def test_passes_explicit_stage(self):
        env = _make_envelope()
        result = evaluate_command_lifecycle("lc-1", env, stage="actor_bound", status="accepted")
        assert result.stage == "actor_bound"
        assert result.status == "accepted"


class TestCommandLifecycleService:
    def test_stateless_no_instance_state(self):
        svc = CommandLifecycleService()
        assert not hasattr(svc, "_state") and not hasattr(svc, "_cache")

    def test_evaluate_works(self):
        svc = CommandLifecycleService()
        env = _make_envelope()
        result = svc.evaluate("lc-1", env)
        assert isinstance(result, CommandLifecycleResult)

    def test_no_forbidden_methods(self):
        forbidden = [
            "execute", "run", "commit", "mutate", "apply",
            "save", "load", "model", "prompt",
        ]
        svc_methods = [m for m in dir(CommandLifecycleService) if not m.startswith("_")]
        for method_name in forbidden:
            assert method_name not in svc_methods, f"Forbidden method found: {method_name}"


class TestGuardrails:
    def test_state_store_module_authorized(self):
        assert os.path.exists("src/astra_runtime/domain/state_store.py")

    def test_no_transaction_lifecycle_module(self):
        assert not os.path.exists("src/astra_runtime/domain/transaction_lifecycle.py")

    def test_no_event_commitment_module(self):
        assert not os.path.exists("src/astra_runtime/domain/event_commitment.py")

    def test_no_resource_math_module(self):
        assert not os.path.exists("src/astra_runtime/domain/resource_math.py")

    def test_no_combat_module(self):
        assert not os.path.exists("src/astra_runtime/domain/combat.py")

    def test_no_ability_effects_module(self):
        assert not os.path.exists("src/astra_runtime/domain/ability_effects.py")

    def test_no_inventory_module(self):
        assert not os.path.exists("src/astra_runtime/domain/inventory.py")

    def test_no_mission_module(self):
        assert not os.path.exists("src/astra_runtime/domain/mission.py")

    def test_no_social_faction_module(self):
        assert not os.path.exists("src/astra_runtime/domain/social_faction.py")

    def test_no_generated_content_module(self):
        assert not os.path.exists("src/astra_runtime/domain/generated_content.py")

    def test_no_context_packet_compiler(self):
        assert not os.path.exists("src/astra_runtime/kernel/context_packet_compiler.py")

    def test_no_model_package(self):
        assert not os.path.exists("src/astra_runtime/model")

    def test_no_prompts_package(self):
        assert not os.path.exists("src/astra_runtime/prompts")

    def test_no_live_play_package(self):
        assert not os.path.exists("src/astra_runtime/live_play")

    def test_no_ui_package(self):
        assert not os.path.exists("src/astra_runtime/ui")
