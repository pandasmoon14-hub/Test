"""Tests for action legality skeleton — RUNTIME-DOMAIN-PR-1A."""

import copy
import os

import pytest

from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    create_command_envelope,
)
from astra_runtime.domain.command_lifecycle import COMMAND_LIFECYCLE_STAGES
from astra_runtime.domain.action_legality import (
    ACTION_LEGALITY_BLOCKING_DECISIONS,
    ACTION_LEGALITY_DECISIONS,
    ActionLegalityDecision,
    ActionLegalityError,
    ActionLegalityResult,
    ActionLegalityService,
    CommandQuarantineResult,
    ConfirmationRequirement,
    DependencyDeclaration,
    InvalidActionLegalityDecisionError,
    InvalidActionLegalityResultError,
    InvalidCommandQuarantineResultError,
    InvalidConfirmationRequirementError,
    InvalidDependencyDeclarationError,
    InvalidLegalityBlockReasonError,
    LegalityBlockReason,
    create_action_legality_result,
    create_command_quarantine_result,
    create_confirmation_requirement,
    create_dependency_declaration,
    create_legality_block_reason,
    evaluate_action_legality,
    validate_action_legality_result,
)

VALID_ACTOR = "astra:actor:player-01"


def _make_envelope(**overrides):
    defaults = {"command_id": "cmd-1", "command_type": "move", "source_actor_id": VALID_ACTOR}
    defaults.update(overrides)
    return create_command_envelope(**defaults)


def _make_dep(**overrides):
    defaults = {"dependency_id": "dep-1", "dependency_type": "state_projection", "required": True}
    defaults.update(overrides)
    return create_dependency_declaration(**defaults)


def _make_block(**overrides):
    defaults = {
        "reason_id": "br-1", "reason_code": "missing_actor",
        "message": "Actor not found", "player_visible": True, "hidden_info_safe": True,
    }
    defaults.update(overrides)
    return create_legality_block_reason(**defaults)


def _make_confirmation(**overrides):
    defaults = {"confirmation_id": "conf-1", "reason": "Risky action", "required": True}
    defaults.update(overrides)
    return create_confirmation_requirement(**defaults)


def _make_quarantine(**overrides):
    defaults = {"quarantine_id": "q-1", "reason_code": "suspicious", "message": "Flagged for review"}
    defaults.update(overrides)
    return create_command_quarantine_result(**defaults)


class TestAllDecisionCategories:
    EXPECTED_DECISIONS = [
        "legal",
        "illegal",
        "requires_confirmation",
        "requires_more_information",
        "blocked_by_hidden_information",
        "blocked_by_missing_actor",
        "blocked_by_invalid_target",
        "blocked_by_resource_precheck",
        "blocked_by_timing",
        "blocked_by_scope",
        "quarantined_for_validation",
        "unsupported_command_type",
    ]

    @pytest.mark.parametrize("decision", EXPECTED_DECISIONS)
    def test_decision_accepted(self, decision):
        result = create_action_legality_result(
            legality_id="al-1", command_id="cmd-1", decision=decision,
            lifecycle_stage="legality_prechecked",
            may_proceed_to_preview=(decision == "legal"),
            requires_confirmation=False,
        )
        assert result.decision == decision

    def test_unsupported_decision_rejected(self):
        with pytest.raises(InvalidActionLegalityDecisionError):
            create_action_legality_result(
                legality_id="al-1", command_id="cmd-1", decision="nonexistent",
                lifecycle_stage="legality_prechecked",
                may_proceed_to_preview=False, requires_confirmation=False,
            )

    def test_all_12_decisions_present(self):
        assert len(ACTION_LEGALITY_DECISIONS) == 12


class TestActionLegalityDecision:
    def test_valid_creation(self):
        d = ActionLegalityDecision(
            decision="legal", player_visible=True, hidden_info_safe=True,
            may_proceed_to_preview=True, requires_validation_issue=False,
        )
        assert d.decision == "legal"

    def test_frozen(self):
        d = ActionLegalityDecision(
            decision="legal", player_visible=True, hidden_info_safe=True,
            may_proceed_to_preview=True, requires_validation_issue=False,
        )
        with pytest.raises(AttributeError):
            d.decision = "illegal"  # type: ignore[misc]


class TestDependencyDeclaration:
    EXPECTED_TYPES = [
        "state_projection", "transaction_lifecycle", "validation_integration",
        "resource_math", "combat_resolution", "ability_resolution",
        "inventory_service", "mission_service", "social_faction_service",
        "generated_content_provenance", "context_projection",
        "model_evaluation", "live_play_gate",
    ]

    def test_valid_creation(self):
        dep = _make_dep()
        assert isinstance(dep, DependencyDeclaration)
        assert dep.dependency_id == "dep-1"

    @pytest.mark.parametrize("dep_type", EXPECTED_TYPES)
    def test_dependency_type_accepted(self, dep_type):
        dep = _make_dep(dependency_type=dep_type)
        assert dep.dependency_type == dep_type

    def test_unsupported_dependency_type_rejected(self):
        with pytest.raises(InvalidDependencyDeclarationError):
            _make_dep(dependency_type="nonexistent")

    def test_non_bool_required_rejected(self):
        with pytest.raises(InvalidDependencyDeclarationError):
            _make_dep(required=1)  # type: ignore[arg-type]

    def test_empty_id_rejected(self):
        with pytest.raises(InvalidDependencyDeclarationError):
            _make_dep(dependency_id="")

    def test_to_dict(self):
        dep = _make_dep(metadata={"k": "v"})
        d = dep.to_dict()
        assert d["dependency_id"] == "dep-1"
        assert d["metadata"] == {"k": "v"}


class TestLegalityBlockReason:
    def test_valid_creation(self):
        br = _make_block()
        assert isinstance(br, LegalityBlockReason)

    def test_empty_reason_id_rejected(self):
        with pytest.raises(InvalidLegalityBlockReasonError):
            _make_block(reason_id="")

    def test_non_bool_player_visible_rejected(self):
        with pytest.raises(InvalidLegalityBlockReasonError):
            _make_block(player_visible=1)  # type: ignore[arg-type]

    def test_non_bool_hidden_info_safe_rejected(self):
        with pytest.raises(InvalidLegalityBlockReasonError):
            _make_block(hidden_info_safe="yes")  # type: ignore[arg-type]

    def test_to_dict(self):
        br = _make_block()
        d = br.to_dict()
        assert d["reason_code"] == "missing_actor"


class TestConfirmationRequirement:
    def test_valid_creation(self):
        c = _make_confirmation()
        assert isinstance(c, ConfirmationRequirement)

    def test_empty_confirmation_id_rejected(self):
        with pytest.raises(InvalidConfirmationRequirementError):
            _make_confirmation(confirmation_id="")

    def test_non_bool_required_rejected(self):
        with pytest.raises(InvalidConfirmationRequirementError):
            _make_confirmation(required="yes")  # type: ignore[arg-type]

    def test_to_dict(self):
        c = _make_confirmation()
        d = c.to_dict()
        assert d["reason"] == "Risky action"


class TestCommandQuarantineResult:
    def test_valid_creation(self):
        q = _make_quarantine()
        assert isinstance(q, CommandQuarantineResult)

    def test_empty_quarantine_id_rejected(self):
        with pytest.raises(InvalidCommandQuarantineResultError):
            _make_quarantine(quarantine_id="")

    def test_to_dict(self):
        q = _make_quarantine()
        d = q.to_dict()
        assert d["reason_code"] == "suspicious"


class TestCreateActionLegalityResult:
    def test_valid_creation(self):
        result = create_action_legality_result(
            legality_id="al-1", command_id="cmd-1", decision="legal",
            lifecycle_stage="legality_prechecked",
            may_proceed_to_preview=True, requires_confirmation=False,
        )
        assert isinstance(result, ActionLegalityResult)

    def test_preserves_all_fields(self):
        dep = _make_dep()
        br = _make_block()
        conf = _make_confirmation()
        qr = _make_quarantine()
        result = create_action_legality_result(
            legality_id="al-99", command_id="cmd-42", decision="requires_confirmation",
            lifecycle_stage="confirmation_required",
            may_proceed_to_preview=True, requires_confirmation=True,
            dependencies=[dep], block_reasons=[br],
            confirmation_requirement=conf, quarantine_result=qr,
            validation_id="val-7", metadata={"origin": "test"},
        )
        assert result.legality_id == "al-99"
        assert result.command_id == "cmd-42"
        assert result.decision == "requires_confirmation"
        assert result.lifecycle_stage == "confirmation_required"
        assert result.may_proceed_to_preview is True
        assert result.requires_confirmation is True
        assert len(result.dependencies) == 1
        assert len(result.block_reasons) == 1
        assert result.confirmation_requirement is conf
        assert result.quarantine_result is qr
        assert result.validation_id == "val-7"
        assert dict(result.metadata) == {"origin": "test"}

    def test_non_bool_may_proceed_rejected(self):
        with pytest.raises(InvalidActionLegalityResultError):
            create_action_legality_result(
                legality_id="al-1", command_id="cmd-1", decision="legal",
                lifecycle_stage="legality_prechecked",
                may_proceed_to_preview="yes",  # type: ignore[arg-type]
                requires_confirmation=False,
            )

    def test_non_bool_requires_confirmation_rejected(self):
        with pytest.raises(InvalidActionLegalityResultError):
            create_action_legality_result(
                legality_id="al-1", command_id="cmd-1", decision="legal",
                lifecycle_stage="legality_prechecked",
                may_proceed_to_preview=True, requires_confirmation=1,  # type: ignore[arg-type]
            )

    def test_invalid_dependency_entry_rejected(self):
        with pytest.raises(InvalidActionLegalityResultError):
            create_action_legality_result(
                legality_id="al-1", command_id="cmd-1", decision="legal",
                lifecycle_stage="legality_prechecked",
                may_proceed_to_preview=True, requires_confirmation=False,
                dependencies=[{"not": "a DependencyDeclaration"}],  # type: ignore[list-item]
            )

    def test_invalid_block_reason_entry_rejected(self):
        with pytest.raises(InvalidActionLegalityResultError):
            create_action_legality_result(
                legality_id="al-1", command_id="cmd-1", decision="legal",
                lifecycle_stage="legality_prechecked",
                may_proceed_to_preview=True, requires_confirmation=False,
                block_reasons=["not a LegalityBlockReason"],  # type: ignore[list-item]
            )

    def test_invalid_confirmation_type_rejected(self):
        with pytest.raises(InvalidActionLegalityResultError):
            create_action_legality_result(
                legality_id="al-1", command_id="cmd-1", decision="legal",
                lifecycle_stage="legality_prechecked",
                may_proceed_to_preview=True, requires_confirmation=False,
                confirmation_requirement="wrong",  # type: ignore[arg-type]
            )

    def test_invalid_quarantine_type_rejected(self):
        with pytest.raises(InvalidActionLegalityResultError):
            create_action_legality_result(
                legality_id="al-1", command_id="cmd-1", decision="legal",
                lifecycle_stage="legality_prechecked",
                may_proceed_to_preview=True, requires_confirmation=False,
                quarantine_result={"wrong": True},  # type: ignore[arg-type]
            )

    def test_empty_legality_id_rejected(self):
        with pytest.raises(InvalidActionLegalityResultError):
            create_action_legality_result(
                legality_id="", command_id="cmd-1", decision="legal",
                lifecycle_stage="legality_prechecked",
                may_proceed_to_preview=True, requires_confirmation=False,
            )

    def test_validation_id_none_accepted(self):
        result = create_action_legality_result(
            legality_id="al-1", command_id="cmd-1", decision="legal",
            lifecycle_stage="legality_prechecked",
            may_proceed_to_preview=True, requires_confirmation=False,
            validation_id=None,
        )
        assert result.validation_id is None

    def test_validation_id_empty_rejected(self):
        with pytest.raises(InvalidActionLegalityResultError):
            create_action_legality_result(
                legality_id="al-1", command_id="cmd-1", decision="legal",
                lifecycle_stage="legality_prechecked",
                may_proceed_to_preview=True, requires_confirmation=False,
                validation_id="",
            )

    def test_metadata_deep_copy_safe(self):
        original = {"nested": {"key": "value"}}
        result = create_action_legality_result(
            legality_id="al-1", command_id="cmd-1", decision="legal",
            lifecycle_stage="legality_prechecked",
            may_proceed_to_preview=True, requires_confirmation=False,
            metadata=original,
        )
        original["nested"]["key"] = "changed"
        assert result.metadata["nested"]["key"] == "value"

    def test_to_dict_returns_deep_copy(self):
        result = create_action_legality_result(
            legality_id="al-1", command_id="cmd-1", decision="legal",
            lifecycle_stage="legality_prechecked",
            may_proceed_to_preview=True, requires_confirmation=False,
            metadata={"nested": {"key": True}},
        )
        d = result.to_dict()
        d["metadata"]["nested"]["key"] = False
        assert result.metadata["nested"]["key"] is True

    def test_frozen_immutability(self):
        result = create_action_legality_result(
            legality_id="al-1", command_id="cmd-1", decision="legal",
            lifecycle_stage="legality_prechecked",
            may_proceed_to_preview=True, requires_confirmation=False,
        )
        with pytest.raises(AttributeError):
            result.legality_id = "al-2"  # type: ignore[misc]

    def test_invalid_lifecycle_stage_rejected(self):
        with pytest.raises(InvalidActionLegalityResultError):
            create_action_legality_result(
                legality_id="al-1", command_id="cmd-1", decision="legal",
                lifecycle_stage="nonexistent",
                may_proceed_to_preview=True, requires_confirmation=False,
            )


class TestValidateActionLegalityResult:
    def test_accepts_valid_result(self):
        result = create_action_legality_result(
            legality_id="al-1", command_id="cmd-1", decision="legal",
            lifecycle_stage="legality_prechecked",
            may_proceed_to_preview=True, requires_confirmation=False,
        )
        assert validate_action_legality_result(result) is True

    def test_rejects_non_result_object(self):
        assert validate_action_legality_result({"legality_id": "al-1"}) is False

    def test_rejects_none(self):
        assert validate_action_legality_result(None) is False


class TestEvaluateActionLegality:
    def test_accepts_valid_envelope(self):
        env = _make_envelope()
        result = evaluate_action_legality("al-1", env, decision="legal")
        assert isinstance(result, ActionLegalityResult)
        assert result.command_id == "cmd-1"
        assert result.decision == "legal"

    def test_rejects_invalid_envelope(self):
        with pytest.raises(ActionLegalityError):
            evaluate_action_legality("al-1", "not-an-envelope", decision="legal")  # type: ignore[arg-type]

    def test_does_not_mutate_command_payload(self):
        payload = {"target": "north"}
        env = _make_envelope(payload=payload)
        payload_before = dict(env.payload)
        evaluate_action_legality("al-1", env, decision="legal")
        assert dict(env.payload) == payload_before

    def test_does_not_mutate_command_metadata(self):
        meta = {"session": "s1"}
        env = _make_envelope(metadata=meta)
        meta_before = dict(env.metadata)
        evaluate_action_legality("al-1", env, decision="legal")
        assert dict(env.metadata) == meta_before

    def test_does_not_inspect_payload_for_execution(self):
        env = _make_envelope(payload={"action": "cast_fireball", "target": "dragon"})
        result = evaluate_action_legality("al-1", env, decision="legal")
        assert result.decision == "legal"

    def test_default_may_proceed_for_legal(self):
        env = _make_envelope()
        result = evaluate_action_legality("al-1", env, decision="legal")
        assert result.may_proceed_to_preview is True

    def test_default_may_proceed_for_blocked(self):
        env = _make_envelope()
        result = evaluate_action_legality("al-1", env, decision="blocked_by_timing")
        assert result.may_proceed_to_preview is False

    def test_explicit_may_proceed_overrides_default(self):
        env = _make_envelope()
        result = evaluate_action_legality(
            "al-1", env, decision="blocked_by_timing", may_proceed_to_preview=True,
        )
        assert result.may_proceed_to_preview is True


class TestActionLegalityService:
    def test_stateless_no_instance_state(self):
        svc = ActionLegalityService()
        assert not hasattr(svc, "_state") and not hasattr(svc, "_cache")

    def test_evaluate_works(self):
        svc = ActionLegalityService()
        env = _make_envelope()
        result = svc.evaluate("al-1", env, decision="legal")
        assert isinstance(result, ActionLegalityResult)

    def test_no_forbidden_methods(self):
        forbidden = [
            "execute", "run", "commit", "mutate", "apply",
            "save", "load", "model", "prompt",
        ]
        svc_methods = [m for m in dir(ActionLegalityService) if not m.startswith("_")]
        for method_name in forbidden:
            assert method_name not in svc_methods, f"Forbidden method found: {method_name}"
