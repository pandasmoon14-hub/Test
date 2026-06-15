"""RT-001B — action legality skeleton tests.

Tests the frozen, keyword-only, reference-only action legality skeleton
dataclasses, controlled constants, validators, and deterministic serializers
defined in RUNTIME-DOMAIN-RT-001B.
"""

from __future__ import annotations

import copy
import json
from types import MappingProxyType

import pytest

from astra_runtime.domain.action_legality_skeleton import (
    BLOCKER_CLASSES,
    DEPENDENCY_OWNERS,
    LEGALITY_STATUSES,
    REFERENCE_KINDS,
    SAFE_PLAYER_MESSAGES,
    ActionLegalityAuthorityFlags,
    ActionLegalityBackendDetail,
    ActionLegalityBlocker,
    ActionLegalityDependencyReference,
    ActionLegalityReference,
    ActionLegalityRequest,
    ActionLegalityResult,
    ActionLegalitySkeletonError,
    ActionLegalitySubjectReference,
    ActionLegalityTargetReference,
    ActionLegalityVisibilityEnvelope,
    InvalidActionLegalityAuthorityFlagsError,
    InvalidActionLegalityBackendDetailError,
    InvalidActionLegalityBlockerError,
    InvalidActionLegalityDependencyReferenceError,
    InvalidActionLegalityReferenceError,
    InvalidActionLegalityRequestError,
    InvalidActionLegalityResultError,
    InvalidActionLegalitySubjectReferenceError,
    InvalidActionLegalityTargetReferenceError,
    InvalidActionLegalityVisibilityEnvelopeError,
    make_action_legality_backend_detail,
    make_action_legality_blocker,
    make_action_legality_dependency_reference,
    make_action_legality_reference,
    make_action_legality_request,
    make_action_legality_result,
    make_action_legality_subject_reference,
    make_action_legality_target_reference,
    make_action_legality_visibility_envelope,
    validate_action_legality_backend_detail,
    validate_action_legality_blocker,
    validate_action_legality_dependency_reference,
    validate_action_legality_reference,
    validate_action_legality_request,
    validate_action_legality_result,
    validate_action_legality_subject_reference,
    validate_action_legality_target_reference,
    validate_action_legality_visibility_envelope,
)


# ---------------------------------------------------------------------------
# 1. Module imports successfully
# ---------------------------------------------------------------------------


class TestModuleImport:
    def test_module_imports(self):
        import astra_runtime.domain.action_legality_skeleton as mod
        assert mod is not None

    def test_public_surface_accessible(self):
        from astra_runtime.domain.action_legality_skeleton import (
            LEGALITY_STATUSES,
            BLOCKER_CLASSES,
            SAFE_PLAYER_MESSAGES,
        )
        assert isinstance(LEGALITY_STATUSES, frozenset)
        assert isinstance(BLOCKER_CLASSES, frozenset)
        assert isinstance(SAFE_PLAYER_MESSAGES, frozenset)


# ---------------------------------------------------------------------------
# 2. Constants expose exactly the RT-001A legality statuses
# ---------------------------------------------------------------------------


class TestLegalityStatuses:
    def test_exact_statuses(self):
        expected = {
            "legal", "illegal", "blocked", "deferred",
            "quarantined", "unknown", "escalated",
        }
        assert LEGALITY_STATUSES == expected

    def test_frozenset(self):
        assert isinstance(LEGALITY_STATUSES, frozenset)

    def test_count(self):
        assert len(LEGALITY_STATUSES) == 7


# ---------------------------------------------------------------------------
# 3. Constants expose the RT-001A blocker classes
# ---------------------------------------------------------------------------


class TestBlockerClasses:
    def test_exact_blocker_classes(self):
        expected = {
            "actor_existence_reference",
            "actor_authority_capability",
            "access_permission",
            "target_existence_reference",
            "target_reachability_scope",
            "scene_location_boundary",
            "command_kind_routing",
            "validation_integration",
            "resource_prerequisite",
            "timing_cooldown_phase",
            "hidden_information",
            "ambiguity_clarification",
            "unsupported_command_family",
            "source_local_donor_specific",
            "doctrine_gap",
            "schema_gap",
            "runtime_owner_handoff",
            "policy_safety_meta_action",
            "anti_authority",
        }
        assert BLOCKER_CLASSES == expected

    def test_frozenset(self):
        assert isinstance(BLOCKER_CLASSES, frozenset)

    def test_count(self):
        assert len(BLOCKER_CLASSES) == 19


# ---------------------------------------------------------------------------
# 4. Safe player-visible messages are controlled
# ---------------------------------------------------------------------------


class TestSafePlayerMessages:
    def test_contains_required_messages(self):
        required = [
            "Invalid actor.",
            "Cannot currently attempt this action.",
            "Access denied.",
            "Requires permission.",
            "Invalid target.",
            "Target is not reachable.",
            "Target is out of range.",
            "This action is not available here.",
            "This type of action is not supported.",
            "Action could not be validated.",
            "Required resources are not available.",
            "This action cannot be taken right now.",
            "Not enough information to attempt this action.",
            "Please clarify your intended action.",
            "This action uses rules that are not currently active.",
            "This action requires further development.",
            "This action references unsupported game elements.",
            "This action cannot be processed at this time.",
            "This action is not permitted.",
            "This action has been referred for review.",
            "Action accepted.",
        ]
        for msg in required:
            assert msg in SAFE_PLAYER_MESSAGES, f"Missing: {msg}"

    def test_frozenset(self):
        assert isinstance(SAFE_PLAYER_MESSAGES, frozenset)

    def test_count(self):
        assert len(SAFE_PLAYER_MESSAGES) == 21


# ---------------------------------------------------------------------------
# 5. Dataclasses are frozen and keyword-only
# ---------------------------------------------------------------------------


class TestFrozenAndKwOnly:
    def test_reference_frozen(self):
        ref = ActionLegalityReference(
            reference_kind="command",
            reference_id="cmd-001",
            owner_surface="test",
        )
        with pytest.raises(AttributeError):
            ref.reference_id = "new"  # type: ignore[misc]

    def test_subject_ref_frozen(self):
        sub = ActionLegalitySubjectReference(
            subject_id="actor-001",
            subject_label="Hero",
        )
        with pytest.raises(AttributeError):
            sub.subject_id = "new"  # type: ignore[misc]

    def test_target_ref_frozen(self):
        tgt = ActionLegalityTargetReference(
            target_id="target-001",
            target_label="Enemy",
        )
        with pytest.raises(AttributeError):
            tgt.target_id = "new"  # type: ignore[misc]

    def test_dependency_ref_frozen(self):
        dep = ActionLegalityDependencyReference(
            dependency_id="dep-001",
            dependency_owner="validation",
        )
        with pytest.raises(AttributeError):
            dep.dependency_id = "new"  # type: ignore[misc]

    def test_backend_detail_frozen(self):
        bd = ActionLegalityBackendDetail(
            detail_id="det-001",
            blocker_class="hidden_information",
            owner_route="rt-001",
        )
        with pytest.raises(AttributeError):
            bd.detail_id = "new"  # type: ignore[misc]

    def test_blocker_frozen(self):
        blk = ActionLegalityBlocker(
            blocker_id="blk-001",
            blocker_class="hidden_information",
            legality_status="blocked",
            player_visible_message="Not enough information to attempt this action.",
        )
        with pytest.raises(AttributeError):
            blk.blocker_id = "new"  # type: ignore[misc]

    def test_visibility_envelope_frozen(self):
        env = ActionLegalityVisibilityEnvelope(
            player_visible_message="Action accepted.",
        )
        with pytest.raises(AttributeError):
            env.player_visible_message = "new"  # type: ignore[misc]

    def test_authority_flags_frozen(self):
        flags = ActionLegalityAuthorityFlags()
        with pytest.raises(AttributeError):
            flags.model_call_authorized = True  # type: ignore[misc]

    def test_request_frozen(self):
        req = _make_sample_request()
        with pytest.raises(AttributeError):
            req.request_id = "new"  # type: ignore[misc]

    def test_result_frozen(self):
        res = _make_sample_legal_result()
        with pytest.raises(AttributeError):
            res.result_id = "new"  # type: ignore[misc]

    def test_kw_only_reference(self):
        with pytest.raises(TypeError):
            ActionLegalityReference("command", "id", "surface")  # type: ignore[misc]

    def test_kw_only_subject(self):
        with pytest.raises(TypeError):
            ActionLegalitySubjectReference("id", "label")  # type: ignore[misc]

    def test_kw_only_target(self):
        with pytest.raises(TypeError):
            ActionLegalityTargetReference("id", "label")  # type: ignore[misc]

    def test_kw_only_authority_flags(self):
        with pytest.raises(TypeError):
            ActionLegalityAuthorityFlags(False)  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 6. to_dict() output is deterministic and JSON-safe
# ---------------------------------------------------------------------------


class TestToDictDeterministic:
    def test_reference_to_dict(self):
        ref = ActionLegalityReference(
            reference_kind="command",
            reference_id="cmd-001",
            owner_surface="test",
            summary="test ref",
        )
        d = ref.to_dict()
        assert d == ref.to_dict()
        json.dumps(d)

    def test_subject_to_dict(self):
        sub = ActionLegalitySubjectReference(
            subject_id="actor-001",
            subject_label="Hero",
        )
        d = sub.to_dict()
        assert d == sub.to_dict()
        json.dumps(d)

    def test_target_to_dict(self):
        tgt = ActionLegalityTargetReference(
            target_id="target-001",
            target_label="Enemy",
        )
        d = tgt.to_dict()
        assert d == tgt.to_dict()
        json.dumps(d)

    def test_dependency_to_dict(self):
        dep = ActionLegalityDependencyReference(
            dependency_id="dep-001",
            dependency_owner="validation",
        )
        d = dep.to_dict()
        assert d == dep.to_dict()
        json.dumps(d)

    def test_blocker_to_dict(self):
        blk = _make_sample_blocker()
        d = blk.to_dict()
        assert d == blk.to_dict()
        json.dumps(d)

    def test_backend_detail_to_dict(self):
        bd = ActionLegalityBackendDetail(
            detail_id="det-001",
            blocker_class="hidden_information",
            owner_route="rt-001",
        )
        d = bd.to_dict()
        assert d == bd.to_dict()
        json.dumps(d)

    def test_visibility_envelope_to_dict(self):
        env = ActionLegalityVisibilityEnvelope(
            player_visible_message="Action accepted.",
        )
        d = env.to_dict()
        assert d == env.to_dict()
        json.dumps(d)

    def test_authority_flags_to_dict(self):
        flags = ActionLegalityAuthorityFlags()
        d = flags.to_dict()
        assert d == flags.to_dict()
        json.dumps(d)

    def test_request_to_dict(self):
        req = _make_sample_request()
        d = req.to_dict()
        assert d == req.to_dict()
        json.dumps(d)

    def test_result_to_dict(self):
        res = _make_sample_legal_result()
        d = res.to_dict()
        assert d == res.to_dict()
        json.dumps(d)

    def test_to_dict_returns_plain_dict(self):
        ref = ActionLegalityReference(
            reference_kind="command",
            reference_id="cmd-001",
            owner_surface="test",
        )
        d = ref.to_dict()
        assert isinstance(d, dict)
        assert isinstance(d["metadata"], dict)


# ---------------------------------------------------------------------------
# 7. Invalid legality status raises
# ---------------------------------------------------------------------------


class TestInvalidLegalityStatus:
    def test_invalid_status_in_result(self):
        with pytest.raises(InvalidActionLegalityResultError):
            ActionLegalityResult(
                result_id="r-001",
                request_id="req-001",
                legality_status="fake_status",
            )

    def test_invalid_status_in_blocker(self):
        with pytest.raises(InvalidActionLegalityBlockerError):
            ActionLegalityBlocker(
                blocker_id="blk-001",
                blocker_class="hidden_information",
                legality_status="fake_status",
                player_visible_message="Not enough information to attempt this action.",
            )


# ---------------------------------------------------------------------------
# 8. Invalid blocker class raises
# ---------------------------------------------------------------------------


class TestInvalidBlockerClass:
    def test_invalid_blocker_class_in_blocker(self):
        with pytest.raises(InvalidActionLegalityBlockerError):
            ActionLegalityBlocker(
                blocker_id="blk-001",
                blocker_class="fake_class",
                legality_status="blocked",
                player_visible_message="Action accepted.",
            )

    def test_invalid_blocker_class_in_backend_detail(self):
        with pytest.raises(InvalidActionLegalityBackendDetailError):
            ActionLegalityBackendDetail(
                detail_id="det-001",
                blocker_class="fake_class",
                owner_route="rt-001",
            )


# ---------------------------------------------------------------------------
# 9. Invalid player-visible message raises
# ---------------------------------------------------------------------------


class TestInvalidPlayerVisibleMessage:
    def test_invalid_message_in_blocker(self):
        with pytest.raises(InvalidActionLegalityBlockerError):
            ActionLegalityBlocker(
                blocker_id="blk-001",
                blocker_class="hidden_information",
                legality_status="blocked",
                player_visible_message="You can't see the invisible enemy!",
            )

    def test_invalid_message_in_visibility_envelope(self):
        with pytest.raises(InvalidActionLegalityVisibilityEnvelopeError):
            ActionLegalityVisibilityEnvelope(
                player_visible_message="Secret backend info leak",
            )

    def test_invalid_blocker_message_in_visibility_envelope(self):
        with pytest.raises(InvalidActionLegalityVisibilityEnvelopeError):
            ActionLegalityVisibilityEnvelope(
                player_visible_message="Action accepted.",
                player_visible_blockers=("Not a safe message",),
            )


# ---------------------------------------------------------------------------
# 10. ActionLegalityAuthorityFlags rejects non-False
# ---------------------------------------------------------------------------


class TestAuthorityFlagsRejectNonFalse:
    def test_rejects_true(self):
        with pytest.raises(InvalidActionLegalityAuthorityFlagsError):
            ActionLegalityAuthorityFlags(
                action_legality_engine_authorized=True,
            )

    def test_rejects_truthy_string(self):
        with pytest.raises(InvalidActionLegalityAuthorityFlagsError):
            ActionLegalityAuthorityFlags(
                model_call_authorized="yes",  # type: ignore[arg-type]
            )

    def test_rejects_one(self):
        with pytest.raises(InvalidActionLegalityAuthorityFlagsError):
            ActionLegalityAuthorityFlags(
                state_mutation_authorized=1,  # type: ignore[arg-type]
            )

    def test_rejects_none(self):
        with pytest.raises(InvalidActionLegalityAuthorityFlagsError):
            ActionLegalityAuthorityFlags(
                persistence_write_authorized=None,  # type: ignore[arg-type]
            )

    def test_rejects_zero(self):
        with pytest.raises(InvalidActionLegalityAuthorityFlagsError):
            ActionLegalityAuthorityFlags(
                rng_execution_authorized=0,  # type: ignore[arg-type]
            )

    def test_rejects_empty_string(self):
        with pytest.raises(InvalidActionLegalityAuthorityFlagsError):
            ActionLegalityAuthorityFlags(
                combat_resolution_authorized="",  # type: ignore[arg-type]
            )

    def test_all_false_accepted(self):
        flags = ActionLegalityAuthorityFlags()
        for field_name in flags.__dataclass_fields__:
            assert getattr(flags, field_name) is False


# ---------------------------------------------------------------------------
# 11. Authority flag to_dict() always serializes all flags as False
# ---------------------------------------------------------------------------


class TestAuthorityFlagsSerialization:
    def test_to_dict_all_false(self):
        flags = ActionLegalityAuthorityFlags()
        d = flags.to_dict()
        for key, value in d.items():
            assert value is False, f"{key} is not False"

    def test_to_dict_has_all_fields(self):
        flags = ActionLegalityAuthorityFlags()
        d = flags.to_dict()
        expected_fields = {
            "action_legality_engine_authorized",
            "command_execution_authorized",
            "state_mutation_authorized",
            "event_append_authorized",
            "event_commitment_authorized",
            "persistence_write_authorized",
            "replay_authorized",
            "rng_execution_authorized",
            "table_oracle_execution_authorized",
            "resource_math_execution_authorized",
            "affordability_calculation_authorized",
            "reservation_authorized",
            "settlement_authorized",
            "consequence_application_authorized",
            "combat_resolution_authorized",
            "ability_resolution_authorized",
            "inventory_mutation_authorized",
            "mission_mutation_authorized",
            "social_faction_mutation_authorized",
            "context_packet_compilation_authorized",
            "model_call_authorized",
            "prompt_rendering_authorized",
            "prompt_execution_authorized",
            "prose_parsing_authorized",
            "narration_generation_authorized",
            "live_play_authorized",
            "ui_client_authorized",
            "conversion_authorized",
            "sourcebook_inclusion_authorized",
            "canon_promotion_authorized",
        }
        assert set(d.keys()) == expected_fields

    def test_to_dict_is_hardcoded_not_user_supplied(self):
        flags = ActionLegalityAuthorityFlags()
        d = flags.to_dict()
        assert all(v is False for v in d.values())


# ---------------------------------------------------------------------------
# 12. Legal result rejects non-empty blockers
# ---------------------------------------------------------------------------


class TestLegalResultRejectsBlockers:
    def test_legal_with_blockers_raises(self):
        blocker = _make_sample_blocker()
        with pytest.raises(InvalidActionLegalityResultError, match="legal result must have empty blockers"):
            ActionLegalityResult(
                result_id="r-001",
                request_id="req-001",
                legality_status="legal",
                blockers=(blocker,),
            )

    def test_legal_with_empty_blockers_ok(self):
        res = ActionLegalityResult(
            result_id="r-001",
            request_id="req-001",
            legality_status="legal",
        )
        assert res.legality_status == "legal"
        assert len(res.blockers) == 0


# ---------------------------------------------------------------------------
# 13. Non-legal result requires blockers (except unknown/escalated)
# ---------------------------------------------------------------------------


class TestNonLegalRequiresBlockers:
    @pytest.mark.parametrize("status", ["illegal", "blocked", "deferred", "quarantined"])
    def test_non_legal_without_blockers_raises(self, status: str):
        with pytest.raises(InvalidActionLegalityResultError, match="must have at least one blocker"):
            ActionLegalityResult(
                result_id="r-001",
                request_id="req-001",
                legality_status=status,
            )

    def test_unknown_without_blockers_ok(self):
        res = ActionLegalityResult(
            result_id="r-001",
            request_id="req-001",
            legality_status="unknown",
        )
        assert res.legality_status == "unknown"
        assert len(res.blockers) == 0

    def test_escalated_without_blockers_ok(self):
        res = ActionLegalityResult(
            result_id="r-001",
            request_id="req-001",
            legality_status="escalated",
        )
        assert res.legality_status == "escalated"
        assert len(res.blockers) == 0

    def test_blocked_with_blocker_ok(self):
        blocker = _make_sample_blocker()
        res = ActionLegalityResult(
            result_id="r-001",
            request_id="req-001",
            legality_status="blocked",
            blockers=(blocker,),
        )
        assert len(res.blockers) == 1


# ---------------------------------------------------------------------------
# 14. Hidden-information blocker must use only safe generic messages
# ---------------------------------------------------------------------------


class TestHiddenInfoBlockerSafeMessages:
    def test_hidden_info_safe_message_ok(self):
        blk = ActionLegalityBlocker(
            blocker_id="blk-001",
            blocker_class="hidden_information",
            legality_status="blocked",
            player_visible_message="Not enough information to attempt this action.",
        )
        assert blk.player_visible_message == "Not enough information to attempt this action."

    def test_hidden_info_alternative_safe_message_ok(self):
        blk = ActionLegalityBlocker(
            blocker_id="blk-002",
            blocker_class="hidden_information",
            legality_status="blocked",
            player_visible_message="This action cannot be taken right now.",
        )
        assert blk.player_visible_message == "This action cannot be taken right now."

    def test_hidden_info_specific_message_rejected(self):
        with pytest.raises(InvalidActionLegalityBlockerError, match="safe generic"):
            ActionLegalityBlocker(
                blocker_id="blk-003",
                blocker_class="hidden_information",
                legality_status="blocked",
                player_visible_message="Invalid target.",
            )

    def test_hidden_info_action_accepted_rejected(self):
        with pytest.raises(InvalidActionLegalityBlockerError, match="safe generic"):
            ActionLegalityBlocker(
                blocker_id="blk-004",
                blocker_class="hidden_information",
                legality_status="blocked",
                player_visible_message="Action accepted.",
            )


# ---------------------------------------------------------------------------
# 15. Backend-only detail must not appear in player-visible envelope
# ---------------------------------------------------------------------------


class TestBackendOnlyNotInPlayerVisible:
    def test_player_visible_dict_excludes_backend(self):
        bd = ActionLegalityBackendDetail(
            detail_id="det-001",
            blocker_class="hidden_information",
            owner_route="rt-001",
            resolution_path_summary="secret resolution path",
        )
        env = ActionLegalityVisibilityEnvelope(
            player_visible_message="Action accepted.",
            backend_only_detail=bd,
        )
        pv = env.to_player_visible_dict()
        assert "backend_only_detail" not in pv
        assert "backend_only_refs" not in pv
        assert pv["player_visible_message"] == "Action accepted."

    def test_full_to_dict_includes_backend(self):
        bd = ActionLegalityBackendDetail(
            detail_id="det-001",
            blocker_class="hidden_information",
            owner_route="rt-001",
        )
        env = ActionLegalityVisibilityEnvelope(
            player_visible_message="Action accepted.",
            backend_only_detail=bd,
        )
        d = env.to_dict()
        assert d["backend_only_detail"] is not None
        assert d["backend_only_detail"]["detail_id"] == "det-001"


# ---------------------------------------------------------------------------
# 16. Factory and direct constructor validation are equivalent
# ---------------------------------------------------------------------------


class TestFactoryEquivalence:
    def test_reference_factory(self):
        direct = ActionLegalityReference(
            reference_kind="command",
            reference_id="cmd-001",
            owner_surface="test",
        )
        factory = make_action_legality_reference(
            reference_kind="command",
            reference_id="cmd-001",
            owner_surface="test",
        )
        assert direct.to_dict() == factory.to_dict()

    def test_subject_factory(self):
        direct = ActionLegalitySubjectReference(
            subject_id="actor-001",
            subject_label="Hero",
        )
        factory = make_action_legality_subject_reference(
            subject_id="actor-001",
            subject_label="Hero",
        )
        assert direct.to_dict() == factory.to_dict()

    def test_target_factory(self):
        direct = ActionLegalityTargetReference(
            target_id="target-001",
            target_label="Enemy",
        )
        factory = make_action_legality_target_reference(
            target_id="target-001",
            target_label="Enemy",
        )
        assert direct.to_dict() == factory.to_dict()

    def test_dependency_factory(self):
        direct = ActionLegalityDependencyReference(
            dependency_id="dep-001",
            dependency_owner="validation",
        )
        factory = make_action_legality_dependency_reference(
            dependency_id="dep-001",
            dependency_owner="validation",
        )
        assert direct.to_dict() == factory.to_dict()

    def test_blocker_factory(self):
        direct = ActionLegalityBlocker(
            blocker_id="blk-001",
            blocker_class="hidden_information",
            legality_status="blocked",
            player_visible_message="Not enough information to attempt this action.",
        )
        factory = make_action_legality_blocker(
            blocker_id="blk-001",
            blocker_class="hidden_information",
            legality_status="blocked",
            player_visible_message="Not enough information to attempt this action.",
        )
        assert direct.to_dict() == factory.to_dict()

    def test_backend_detail_factory(self):
        direct = ActionLegalityBackendDetail(
            detail_id="det-001",
            blocker_class="hidden_information",
            owner_route="rt-001",
        )
        factory = make_action_legality_backend_detail(
            detail_id="det-001",
            blocker_class="hidden_information",
            owner_route="rt-001",
        )
        assert direct.to_dict() == factory.to_dict()

    def test_visibility_envelope_factory(self):
        direct = ActionLegalityVisibilityEnvelope(
            player_visible_message="Action accepted.",
        )
        factory = make_action_legality_visibility_envelope(
            player_visible_message="Action accepted.",
        )
        assert direct.to_dict() == factory.to_dict()

    def test_request_factory(self):
        cmd_ref = make_action_legality_reference(
            reference_kind="command",
            reference_id="cmd-001",
            owner_surface="test",
        )
        sub_ref = make_action_legality_subject_reference(
            subject_id="actor-001",
            subject_label="Hero",
        )
        direct = ActionLegalityRequest(
            request_id="req-001",
            command_ref=cmd_ref,
            subject_ref=sub_ref,
        )
        factory = make_action_legality_request(
            request_id="req-001",
            command_ref=cmd_ref,
            subject_ref=sub_ref,
        )
        assert direct.to_dict() == factory.to_dict()

    def test_result_factory(self):
        direct = ActionLegalityResult(
            result_id="r-001",
            request_id="req-001",
            legality_status="legal",
        )
        factory = make_action_legality_result(
            result_id="r-001",
            request_id="req-001",
            legality_status="legal",
        )
        assert direct.to_dict() == factory.to_dict()

    def test_factory_invalid_blocker_class_raises(self):
        with pytest.raises(InvalidActionLegalityBlockerError):
            make_action_legality_blocker(
                blocker_id="blk-001",
                blocker_class="fake_class",
                legality_status="blocked",
                player_visible_message="Action accepted.",
            )

    def test_factory_invalid_status_raises(self):
        with pytest.raises(InvalidActionLegalityResultError):
            make_action_legality_result(
                result_id="r-001",
                request_id="req-001",
                legality_status="fake_status",
            )


# ---------------------------------------------------------------------------
# 17. Domain package exports include the new public surface
# ---------------------------------------------------------------------------


class TestDomainPackageExports:
    def test_skeleton_importable_from_domain(self):
        from astra_runtime.domain import (
            ActionLegalitySkeletonError as _ASE,
            LEGALITY_STATUSES as LS,
            BLOCKER_CLASSES as BC,
            SAFE_PLAYER_MESSAGES as SPM,
            ActionLegalityReference as ALR,
            ActionLegalitySubjectReference as ALSR,
            ActionLegalityTargetReference as ALTR,
            ActionLegalityDependencyReference as ALDR,
            ActionLegalityBlocker as ALB,
            ActionLegalityBackendDetail as ALBD,
            ActionLegalityVisibilityEnvelope as ALVE,
            ActionLegalityAuthorityFlags as ALAF,
            ActionLegalitySkeletonRequest as ALReq,
            ActionLegalitySkeletonResult as ALRes,
        )
        assert LS is LEGALITY_STATUSES
        assert BC is BLOCKER_CLASSES
        assert SPM is SAFE_PLAYER_MESSAGES

    def test_skeleton_in_all(self):
        import astra_runtime.domain as dom
        expected_names = [
            "LEGALITY_STATUSES",
            "BLOCKER_CLASSES",
            "SAFE_PLAYER_MESSAGES",
            "ActionLegalitySkeletonError",
            "ActionLegalityReference",
            "ActionLegalitySubjectReference",
            "ActionLegalityTargetReference",
            "ActionLegalityDependencyReference",
            "ActionLegalityBlocker",
            "ActionLegalityBackendDetail",
            "ActionLegalityVisibilityEnvelope",
            "ActionLegalityAuthorityFlags",
            "ActionLegalitySkeletonRequest",
            "ActionLegalitySkeletonResult",
        ]
        for name in expected_names:
            assert name in dom.__all__, f"{name} not in domain __all__"


# ---------------------------------------------------------------------------
# 18. Guardrail allowlists updated narrowly
# ---------------------------------------------------------------------------


class TestGuardrailNarrow:
    def test_skeleton_module_exists(self):
        import astra_runtime.domain.action_legality_skeleton
        assert True

    def test_no_execution_methods(self):
        import astra_runtime.domain.action_legality_skeleton as mod
        public_names = [n for n in dir(mod) if not n.startswith("_")]
        forbidden_patterns = [
            "execute", "run_", "apply_", "commit_",
            "mutate", "persist", "replay_", "roll_",
            "generate_narration", "render_prompt",
            "call_model", "parse_prose",
        ]
        for name in public_names:
            for pat in forbidden_patterns:
                assert pat not in name.lower(), (
                    f"Public name {name!r} contains forbidden pattern {pat!r}"
                )


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


class TestValidators:
    def test_validate_reference_valid(self):
        ref = make_action_legality_reference(
            reference_kind="command",
            reference_id="cmd-001",
            owner_surface="test",
        )
        assert validate_action_legality_reference(ref) is True

    def test_validate_reference_invalid(self):
        assert validate_action_legality_reference("not a ref") is False

    def test_validate_subject_valid(self):
        sub = make_action_legality_subject_reference(
            subject_id="actor-001",
            subject_label="Hero",
        )
        assert validate_action_legality_subject_reference(sub) is True

    def test_validate_target_valid(self):
        tgt = make_action_legality_target_reference(
            target_id="target-001",
            target_label="Enemy",
        )
        assert validate_action_legality_target_reference(tgt) is True

    def test_validate_dependency_valid(self):
        dep = make_action_legality_dependency_reference(
            dependency_id="dep-001",
            dependency_owner="validation",
        )
        assert validate_action_legality_dependency_reference(dep) is True

    def test_validate_blocker_valid(self):
        blk = _make_sample_blocker()
        assert validate_action_legality_blocker(blk) is True

    def test_validate_backend_detail_valid(self):
        bd = make_action_legality_backend_detail(
            detail_id="det-001",
            blocker_class="hidden_information",
            owner_route="rt-001",
        )
        assert validate_action_legality_backend_detail(bd) is True

    def test_validate_visibility_envelope_valid(self):
        env = make_action_legality_visibility_envelope(
            player_visible_message="Action accepted.",
        )
        assert validate_action_legality_visibility_envelope(env) is True

    def test_validate_request_valid(self):
        req = _make_sample_request()
        assert validate_action_legality_request(req) is True

    def test_validate_result_valid(self):
        res = _make_sample_legal_result()
        assert validate_action_legality_result(res) is True

    def test_validate_result_invalid_type(self):
        assert validate_action_legality_result("not a result") is False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_sample_blocker() -> ActionLegalityBlocker:
    return ActionLegalityBlocker(
        blocker_id="blk-001",
        blocker_class="hidden_information",
        legality_status="blocked",
        player_visible_message="Not enough information to attempt this action.",
    )


def _make_sample_request() -> ActionLegalityRequest:
    cmd_ref = ActionLegalityReference(
        reference_kind="command",
        reference_id="cmd-001",
        owner_surface="test",
    )
    sub_ref = ActionLegalitySubjectReference(
        subject_id="actor-001",
        subject_label="Hero",
    )
    return ActionLegalityRequest(
        request_id="req-001",
        command_ref=cmd_ref,
        subject_ref=sub_ref,
    )


def _make_sample_legal_result() -> ActionLegalityResult:
    return ActionLegalityResult(
        result_id="r-001",
        request_id="req-001",
        legality_status="legal",
    )
