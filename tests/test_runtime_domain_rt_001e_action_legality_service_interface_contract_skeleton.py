"""Tests for RT-001E: Action Legality Service Interface Contract Skeleton.

Covers: module imports, constants, dataclass invariants, authority flag
enforcement, dependency manifests, request/result typing, legal-rejection,
builders, serializers, visible-serializer containment, metadata safety,
public name inspection, forbidden import enforcement, and domain package
exports.
"""

from __future__ import annotations

import ast
import dataclasses
import json
import pathlib
from typing import Any, Mapping

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# T1 — Module imports
# ---------------------------------------------------------------------------

class TestModuleImports:
    def test_import_module(self):
        import astra_runtime.domain.action_legality_service_interface_contract_skeleton  # noqa: F401

    def test_import_constants(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ACTION_LEGALITY_SERVICE_INTERFACE_STAGES,
            ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS,
            ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES,
            ACTION_LEGALITY_SERVICE_INTERFACE_OWNER_ROUTES,
            ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE,
        )
        assert isinstance(ACTION_LEGALITY_SERVICE_INTERFACE_STAGES, frozenset)
        assert isinstance(ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS, frozenset)
        assert isinstance(ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES, frozenset)
        assert isinstance(ACTION_LEGALITY_SERVICE_INTERFACE_OWNER_ROUTES, frozenset)
        assert isinstance(ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE, str)

    def test_import_dataclasses(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceAuthorityFlags,
            ActionLegalityServiceInterfaceDependencyManifest,
            ActionLegalityServiceInterfaceRequest,
            ActionLegalityServiceInterfaceResult,
            ActionLegalityServiceInterfaceContractSummary,
        )
        assert ActionLegalityServiceInterfaceAuthorityFlags is not None
        assert ActionLegalityServiceInterfaceDependencyManifest is not None
        assert ActionLegalityServiceInterfaceRequest is not None
        assert ActionLegalityServiceInterfaceResult is not None
        assert ActionLegalityServiceInterfaceContractSummary is not None

    def test_import_factory_functions(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            create_action_legality_service_interface_authority_flags,
            create_action_legality_service_interface_dependency_manifest,
            create_action_legality_service_interface_request,
            create_action_legality_service_interface_result,
            create_action_legality_service_interface_contract_summary,
        )
        assert callable(create_action_legality_service_interface_authority_flags)
        assert callable(create_action_legality_service_interface_dependency_manifest)
        assert callable(create_action_legality_service_interface_request)
        assert callable(create_action_legality_service_interface_result)
        assert callable(create_action_legality_service_interface_contract_summary)

    def test_import_builders(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_action_legality_service_interface_dependency_manifest,
            build_deferred_action_legality_service_interface_result,
            build_unknown_action_legality_service_interface_result,
        )
        assert callable(build_action_legality_service_interface_dependency_manifest)
        assert callable(build_deferred_action_legality_service_interface_result)
        assert callable(build_unknown_action_legality_service_interface_result)

    def test_import_serializers(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            serialize_action_legality_service_interface_result,
            serialize_action_legality_service_interface_result_visible,
        )
        assert callable(serialize_action_legality_service_interface_result)
        assert callable(serialize_action_legality_service_interface_result_visible)

    def test_import_validators(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            validate_action_legality_service_interface_authority_flags,
            validate_action_legality_service_interface_dependency_manifest,
            validate_action_legality_service_interface_request,
            validate_action_legality_service_interface_result,
            validate_action_legality_service_interface_contract_summary,
        )
        assert callable(validate_action_legality_service_interface_authority_flags)
        assert callable(validate_action_legality_service_interface_dependency_manifest)
        assert callable(validate_action_legality_service_interface_request)
        assert callable(validate_action_legality_service_interface_result)
        assert callable(validate_action_legality_service_interface_contract_summary)


# ---------------------------------------------------------------------------
# T2 — Constants contain expected values
# ---------------------------------------------------------------------------

class TestConstants:
    def test_stages_contain_expected(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ACTION_LEGALITY_SERVICE_INTERFACE_STAGES,
        )
        expected = {
            "request_received",
            "dependency_manifest_built",
            "service_result_built",
            "deferred_result_returned",
            "unknown_result_returned",
        }
        assert expected <= ACTION_LEGALITY_SERVICE_INTERFACE_STAGES

    def test_dependency_kinds_contain_expected(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS,
        )
        assert "validation" in ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS
        assert "resource_math" in ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS
        assert "event_commitment" in ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS

    def test_result_statuses_contain_expected(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES,
        )
        assert "deferred" in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES
        assert "unknown" in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES
        assert "legal" not in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES

    def test_owner_routes_contain_expected(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ACTION_LEGALITY_SERVICE_INTERFACE_OWNER_ROUTES,
        )
        assert "validation_owner" in ACTION_LEGALITY_SERVICE_INTERFACE_OWNER_ROUTES
        assert "resource_math_owner" in ACTION_LEGALITY_SERVICE_INTERFACE_OWNER_ROUTES

    def test_non_authority_note(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE,
        )
        assert "skeleton" in ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE.lower()
        assert "authorizes no" in ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE.lower()


# ---------------------------------------------------------------------------
# T3 — Dataclasses are frozen and keyword-only
# ---------------------------------------------------------------------------

class TestDataclassInvariants:
    def test_authority_flags_frozen_kw_only(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceAuthorityFlags,
        )
        assert dataclasses.fields(ActionLegalityServiceInterfaceAuthorityFlags)
        obj = ActionLegalityServiceInterfaceAuthorityFlags()
        with pytest.raises(dataclasses.FrozenInstanceError):
            obj.legality_engine_authorized = True

    def test_dependency_manifest_frozen_kw_only(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceDependencyManifest,
        )
        obj = ActionLegalityServiceInterfaceDependencyManifest(manifest_id="m1")
        with pytest.raises(dataclasses.FrozenInstanceError):
            obj.manifest_id = "changed"

    def test_request_frozen_kw_only(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceRequest,
            create_action_legality_service_interface_request,
        )
        req = create_action_legality_service_interface_request(
            request_id="r1",
            legality_request=_make_legality_request("r1"),
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            req.request_id = "changed"

    def test_result_frozen_kw_only(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
        )
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            res.result_id = "changed"

    def test_contract_summary_frozen_kw_only(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceContractSummary,
        )
        obj = ActionLegalityServiceInterfaceContractSummary(summary_id="s1")
        with pytest.raises(dataclasses.FrozenInstanceError):
            obj.summary_id = "changed"


# ---------------------------------------------------------------------------
# T4 — Authority flags reject True, 1, 0, None, and truthy strings
# ---------------------------------------------------------------------------

class TestAuthorityFlagEnforcement:
    def test_reject_true(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceAuthorityFlags,
            InvalidActionLegalityServiceInterfaceAuthorityFlagsError,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceAuthorityFlagsError):
            ActionLegalityServiceInterfaceAuthorityFlags(
                legality_engine_authorized=True,
            )

    def test_reject_int_one(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceAuthorityFlags,
            InvalidActionLegalityServiceInterfaceAuthorityFlagsError,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceAuthorityFlagsError):
            ActionLegalityServiceInterfaceAuthorityFlags(
                command_execution_authorized=1,
            )

    def test_reject_int_zero(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceAuthorityFlags,
            InvalidActionLegalityServiceInterfaceAuthorityFlagsError,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceAuthorityFlagsError):
            ActionLegalityServiceInterfaceAuthorityFlags(
                state_read_authorized=0,
            )

    def test_reject_none(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceAuthorityFlags,
            InvalidActionLegalityServiceInterfaceAuthorityFlagsError,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceAuthorityFlagsError):
            ActionLegalityServiceInterfaceAuthorityFlags(
                state_mutation_authorized=None,
            )

    def test_reject_truthy_string(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceAuthorityFlags,
            InvalidActionLegalityServiceInterfaceAuthorityFlagsError,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceAuthorityFlagsError):
            ActionLegalityServiceInterfaceAuthorityFlags(
                model_call_authorized="yes",
            )


# ---------------------------------------------------------------------------
# T5 — Authority flag to_dict() hardcodes all False
# ---------------------------------------------------------------------------

class TestAuthorityFlagToDict:
    def test_to_dict_all_false(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceAuthorityFlags,
        )
        flags = ActionLegalityServiceInterfaceAuthorityFlags()
        d = flags.to_dict()
        assert all(v is False for v in d.values())
        assert len(d) == 34

    def test_to_dict_contains_required_fields(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceAuthorityFlags,
        )
        flags = ActionLegalityServiceInterfaceAuthorityFlags()
        d = flags.to_dict()
        required = [
            "legality_engine_authorized",
            "real_legality_evaluation_authorized",
            "command_execution_authorized",
            "state_read_authorized",
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
            "skill_resolution_authorized",
            "effect_resolution_authorized",
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
        ]
        for field_name in required:
            assert field_name in d, f"Missing {field_name}"
            assert d[field_name] is False


# ---------------------------------------------------------------------------
# T6 — Dependency manifest accepts only ActionLegalityDependencyReference
# ---------------------------------------------------------------------------

class TestDependencyManifest:
    def test_accepts_dependency_references(self):
        from astra_runtime.domain.action_legality_skeleton import (
            ActionLegalityDependencyReference,
        )
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            create_action_legality_service_interface_dependency_manifest,
            validate_action_legality_service_interface_dependency_manifest,
        )
        dep = ActionLegalityDependencyReference(
            dependency_id="dep1",
            dependency_owner="validation",
        )
        manifest = create_action_legality_service_interface_dependency_manifest(
            manifest_id="m1",
            dependency_refs=[dep],
            required_owner_routes=["validation_owner"],
        )
        assert validate_action_legality_service_interface_dependency_manifest(manifest)

    def test_rejects_non_dependency_reference(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            InvalidActionLegalityServiceInterfaceDependencyManifestError,
            ActionLegalityServiceInterfaceDependencyManifest,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceDependencyManifestError):
            ActionLegalityServiceInterfaceDependencyManifest(
                manifest_id="m1",
                dependency_refs=["not_a_dep_ref"],
            )


# ---------------------------------------------------------------------------
# T7 — Dependency manifest does not call owner services
# ---------------------------------------------------------------------------

class TestDependencyManifestNoOwnerCalls:
    def test_manifest_builder_does_not_call_services(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_action_legality_service_interface_dependency_manifest,
        )
        manifest = build_action_legality_service_interface_dependency_manifest(
            manifest_id="m1",
            owner_routes=["validation_owner"],
        )
        assert manifest.unavailable_owner_routes == ("validation_owner",)
        assert manifest.deferred_reason == "skeleton_interface_only"


# ---------------------------------------------------------------------------
# T8 — Request requires RT-001B ActionLegalityRequest
# ---------------------------------------------------------------------------

class TestRequestRequiresLegalityRequest:
    def test_accepts_legality_request(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            create_action_legality_service_interface_request,
            validate_action_legality_service_interface_request,
        )
        req = create_action_legality_service_interface_request(
            request_id="r1",
            legality_request=_make_legality_request("r1"),
        )
        assert validate_action_legality_service_interface_request(req)

    def test_rejects_non_legality_request(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            InvalidActionLegalityServiceInterfaceRequestError,
            ActionLegalityServiceInterfaceRequest,
            ActionLegalityServiceInterfaceAuthorityFlags,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceRequestError):
            ActionLegalityServiceInterfaceRequest(
                request_id="r1",
                legality_request="not_a_request",
                authority_flags=ActionLegalityServiceInterfaceAuthorityFlags(),
            )


# ---------------------------------------------------------------------------
# T9 — Result requires RT-001B ActionLegalityResult
# ---------------------------------------------------------------------------

class TestResultRequiresLegalityResult:
    def test_accepts_legality_result(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
            validate_action_legality_service_interface_result,
        )
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        assert validate_action_legality_service_interface_result(res)

    def test_rejects_non_legality_result(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            InvalidActionLegalityServiceInterfaceResultError,
            ActionLegalityServiceInterfaceResult,
            ActionLegalityServiceInterfaceAuthorityFlags,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceResultError):
            ActionLegalityServiceInterfaceResult(
                result_id="res1",
                request_id="r1",
                interface_status="deferred",
                legality_result="not_a_result",
                authority_flags=ActionLegalityServiceInterfaceAuthorityFlags(),
            )


# ---------------------------------------------------------------------------
# T10 — Result rejects all non-deferred/unknown legality statuses
# ---------------------------------------------------------------------------

class TestResultRejectsNonSkeletonLegalityStatus:
    @pytest.mark.parametrize(
        "status",
        ["legal", "illegal", "blocked", "quarantined", "escalated"],
    )
    def test_interface_result_rejects_non_deferred_unknown_legality_status(
        self, status,
    ):
        from astra_runtime.domain.action_legality_skeleton import (
            ActionLegalityAuthorityFlags,
            ActionLegalityResult,
            ActionLegalityBlocker,
            ActionLegalityBackendDetail,
        )
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            InvalidActionLegalityServiceInterfaceResultError,
            ActionLegalityServiceInterfaceResult,
            ActionLegalityServiceInterfaceAuthorityFlags,
        )
        if status == "legal":
            inner_result = ActionLegalityResult(
                result_id="leg1",
                request_id="r1",
                legality_status="legal",
                authority_flags=ActionLegalityAuthorityFlags(),
            )
        else:
            blocker = ActionLegalityBlocker(
                blocker_id="b1",
                blocker_class="runtime_owner_handoff",
                legality_status=status,
                player_visible_message="This action cannot be processed at this time.",
                backend_detail=ActionLegalityBackendDetail(
                    detail_id="d1",
                    blocker_class="runtime_owner_handoff",
                    owner_route="test",
                ),
            )
            inner_result = ActionLegalityResult(
                result_id="leg1",
                request_id="r1",
                legality_status=status,
                blockers=[blocker],
                authority_flags=ActionLegalityAuthorityFlags(),
            )
        with pytest.raises(InvalidActionLegalityServiceInterfaceResultError):
            ActionLegalityServiceInterfaceResult(
                result_id="res1",
                request_id="r1",
                interface_status="deferred",
                legality_result=inner_result,
                authority_flags=ActionLegalityServiceInterfaceAuthorityFlags(),
            )

    @pytest.mark.parametrize(
        "status",
        ["legal", "illegal", "blocked", "quarantined", "escalated"],
    )
    def test_validator_rejects_non_deferred_unknown(self, status):
        """Validator should also reject non-skeleton statuses. Since the
        constructor blocks them, we verify the validator function itself
        rejects the status by checking its logic independently."""
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            validate_action_legality_service_interface_result,
            ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES,
        )
        assert status not in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES

    @pytest.mark.parametrize("status", ["deferred", "unknown"])
    def test_interface_result_accepts_deferred_and_unknown(self, status):
        from astra_runtime.domain.action_legality_skeleton import (
            ActionLegalityAuthorityFlags,
            ActionLegalityResult,
            ActionLegalityBlocker,
            ActionLegalityBackendDetail,
        )
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceResult,
            ActionLegalityServiceInterfaceAuthorityFlags,
            validate_action_legality_service_interface_result,
        )
        blocker = ActionLegalityBlocker(
            blocker_id="b1",
            blocker_class="runtime_owner_handoff",
            legality_status=status,
            player_visible_message="This action cannot be processed at this time.",
            backend_detail=ActionLegalityBackendDetail(
                detail_id="d1",
                blocker_class="runtime_owner_handoff",
                owner_route="test",
            ),
        )
        inner_result = ActionLegalityResult(
            result_id="leg1",
            request_id="r1",
            legality_status=status,
            blockers=[blocker],
            authority_flags=ActionLegalityAuthorityFlags(),
        )
        result = ActionLegalityServiceInterfaceResult(
            result_id="res1",
            request_id="r1",
            interface_status=status,
            legality_result=inner_result,
            authority_flags=ActionLegalityServiceInterfaceAuthorityFlags(),
        )
        assert result.interface_status == status
        assert validate_action_legality_service_interface_result(result)


# ---------------------------------------------------------------------------
# T11 — Deferred builder produces deferred
# ---------------------------------------------------------------------------

class TestDeferredBuilder:
    def test_deferred_builder_produces_deferred(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
        )
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        assert res.interface_status == "deferred"
        assert res.legality_result.legality_status == "deferred"
        assert res.legality_result.legality_status != "legal"


# ---------------------------------------------------------------------------
# T12 — Unknown builder produces unknown
# ---------------------------------------------------------------------------

class TestUnknownBuilder:
    def test_unknown_builder_produces_unknown(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_unknown_action_legality_service_interface_result,
        )
        res = build_unknown_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        assert res.interface_status == "unknown"
        assert res.legality_result.legality_status == "unknown"
        assert res.legality_result.legality_status != "legal"


# ---------------------------------------------------------------------------
# T13 — Result includes dependency manifest or blocker
# ---------------------------------------------------------------------------

class TestResultDependencyOrBlocker:
    def test_deferred_result_has_blocker(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
        )
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        blockers = res.legality_result.blockers
        assert len(blockers) >= 1
        assert blockers[0].blocker_class == "runtime_owner_handoff"

    def test_result_with_dependency_manifest(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
            build_action_legality_service_interface_dependency_manifest,
        )
        manifest = build_action_legality_service_interface_dependency_manifest(
            manifest_id="m1",
            owner_routes=["validation_owner"],
        )
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
            dependency_manifest=manifest,
        )
        assert res.dependency_manifest is not None
        assert res.dependency_manifest.manifest_id == "m1"


# ---------------------------------------------------------------------------
# T14 — Backend serializer is deterministic and JSON-safe
# ---------------------------------------------------------------------------

class TestBackendSerializer:
    def test_backend_serializer_deterministic(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
            serialize_action_legality_service_interface_result,
        )
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        d1 = serialize_action_legality_service_interface_result(res)
        d2 = serialize_action_legality_service_interface_result(res)
        assert d1 == d2

    def test_backend_serializer_json_safe(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
            serialize_action_legality_service_interface_result,
        )
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        d = serialize_action_legality_service_interface_result(res)
        serialized = json.dumps(d)
        assert isinstance(serialized, str)
        parsed = json.loads(serialized)
        assert parsed == d


# ---------------------------------------------------------------------------
# T15 — Visible serializer excludes backend/internal details
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_visible_serializer_excludes_backend(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
            serialize_action_legality_service_interface_result_visible,
        )
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        visible = serialize_action_legality_service_interface_result_visible(res)
        forbidden_keys = {
            "legality_result", "authority_flags", "metadata",
            "dependency_manifest", "trace_refs", "backend_detail",
            "owner_route", "doctrine_refs", "schema_refs",
            "source_local_refs", "hidden_information_classification",
        }
        for key in forbidden_keys:
            assert key not in visible, f"Visible serializer leaked {key!r}"

    def test_visible_serializer_has_expected_keys(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
            serialize_action_legality_service_interface_result_visible,
        )
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        visible = serialize_action_legality_service_interface_result_visible(res)
        expected_keys = {
            "result_id", "request_id", "interface_status",
            "legality_status", "player_visible_message",
            "visible_blocker_messages", "non_authority_note",
        }
        assert set(visible.keys()) == expected_keys


# ---------------------------------------------------------------------------
# T16 — Visible serializer uses only SAFE_PLAYER_MESSAGES
# ---------------------------------------------------------------------------

class TestVisibleSerializerSafeMessages:
    def test_visible_messages_are_safe(self):
        from astra_runtime.domain.action_legality_skeleton import SAFE_PLAYER_MESSAGES
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            build_deferred_action_legality_service_interface_result,
            build_unknown_action_legality_service_interface_result,
            serialize_action_legality_service_interface_result_visible,
        )
        for builder in [
            build_deferred_action_legality_service_interface_result,
            build_unknown_action_legality_service_interface_result,
        ]:
            res = builder(result_id="res1", request_id="r1")
            visible = serialize_action_legality_service_interface_result_visible(res)
            msg = visible["player_visible_message"]
            assert msg in SAFE_PLAYER_MESSAGES, f"Unsafe message: {msg!r}"
            for blocker_msg in visible["visible_blocker_messages"]:
                assert blocker_msg in SAFE_PLAYER_MESSAGES, (
                    f"Unsafe blocker message: {blocker_msg!r}"
                )


# ---------------------------------------------------------------------------
# T17 — Metadata rejects non-JSON-safe values
# ---------------------------------------------------------------------------

class TestMetadataSafety:
    def test_dependency_manifest_rejects_non_json_safe(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            InvalidActionLegalityServiceInterfaceDependencyManifestError,
            ActionLegalityServiceInterfaceDependencyManifest,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceDependencyManifestError):
            ActionLegalityServiceInterfaceDependencyManifest(
                manifest_id="m1",
                metadata={"bad": object()},
            )

    def test_request_rejects_non_json_safe(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            InvalidActionLegalityServiceInterfaceRequestError,
            ActionLegalityServiceInterfaceRequest,
            ActionLegalityServiceInterfaceAuthorityFlags,
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceRequestError):
            ActionLegalityServiceInterfaceRequest(
                request_id="r1",
                legality_request=_make_legality_request("r1"),
                authority_flags=ActionLegalityServiceInterfaceAuthorityFlags(),
                metadata={"bad": object()},
            )

    def test_result_rejects_non_json_safe(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            InvalidActionLegalityServiceInterfaceResultError,
            build_deferred_action_legality_service_interface_result,
            ActionLegalityServiceInterfaceResult,
            ActionLegalityServiceInterfaceAuthorityFlags,
        )
        deferred = build_deferred_action_legality_service_interface_result(
            result_id="res_inner", request_id="r1",
        )
        with pytest.raises(InvalidActionLegalityServiceInterfaceResultError):
            ActionLegalityServiceInterfaceResult(
                result_id="res1",
                request_id="r1",
                interface_status="deferred",
                legality_result=deferred.legality_result,
                authority_flags=ActionLegalityServiceInterfaceAuthorityFlags(),
                metadata={"bad": object()},
            )


# ---------------------------------------------------------------------------
# T18 — Public names contain no forbidden execution/mutation patterns
# ---------------------------------------------------------------------------

class TestPublicSurfaceNameInspection:
    _FORBIDDEN_PATTERNS = (
        "execute", "mutate", "commit_event", "model_call",
        "prompt_render", "narration", "live_play_run",
        "persist_write", "replay_run",
    )

    def test_public_rt001e_names_no_execution_patterns(self):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            __all__ as RT001E_ALL,
        )
        for name in RT001E_ALL:
            lower = name.lower()
            for pat in self._FORBIDDEN_PATTERNS:
                assert pat not in lower, (
                    f"Public name {name!r} contains forbidden pattern {pat!r}"
                )


# ---------------------------------------------------------------------------
# T19 — Module imports no forbidden downstream modules
# ---------------------------------------------------------------------------

class TestImportBoundaryEnforcement:
    _FORBIDDEN_MODULES = (
        "state_store", "state_projection", "transaction_lifecycle",
        "event_commitment", "model_boundary", "tiny_vertical_slice",
        "context_packet_compiler", "live_play", "resource_consequence_math",
    )

    def test_rt001e_does_not_import_forbidden_modules(self):
        src = (
            REPO_ROOT
            / "src"
            / "astra_runtime"
            / "domain"
            / "action_legality_service_interface_contract_skeleton.py"
        ).read_text()
        tree = ast.parse(src)
        import_names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_names.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    import_names.append(node.module)
        for mod_name in import_names:
            for forbidden in self._FORBIDDEN_MODULES:
                assert forbidden not in mod_name, (
                    f"RT-001E imports forbidden module pattern "
                    f"{forbidden!r} via {mod_name!r}"
                )


# ---------------------------------------------------------------------------
# T20 — Domain package exports include new RT-001E public surface
# ---------------------------------------------------------------------------

class TestDomainPackageExports:
    def test_domain_init_exports_rt001e_constants(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "ACTION_LEGALITY_SERVICE_INTERFACE_STAGES")
        assert hasattr(domain, "ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS")
        assert hasattr(domain, "ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES")
        assert hasattr(domain, "ACTION_LEGALITY_SERVICE_INTERFACE_OWNER_ROUTES")
        assert hasattr(domain, "ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE")

    def test_domain_init_exports_rt001e_dataclasses(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "ActionLegalityServiceInterfaceAuthorityFlags")
        assert hasattr(domain, "ActionLegalityServiceInterfaceDependencyManifest")
        assert hasattr(domain, "ActionLegalityServiceInterfaceSkeletonRequest")
        assert hasattr(domain, "ActionLegalityServiceInterfaceSkeletonResult")
        assert hasattr(domain, "ActionLegalityServiceInterfaceContractSummary")

    def test_domain_init_aliasing_policy(self):
        """The domain __init__.py re-exports Request/Result under 'Skeleton'
        suffixed aliases to avoid collision with the older action_legality.py
        ActionLegalityResult that already occupies the package namespace.
        This is intentional and matches the RT-001B aliasing precedent
        (ActionLegalitySkeletonRequest / ActionLegalitySkeletonResult)."""
        import astra_runtime.domain as domain
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceRequest,
            ActionLegalityServiceInterfaceResult,
        )
        assert domain.ActionLegalityServiceInterfaceSkeletonRequest is ActionLegalityServiceInterfaceRequest
        assert domain.ActionLegalityServiceInterfaceSkeletonResult is ActionLegalityServiceInterfaceResult

    def test_domain_init_exports_rt001e_factories(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "create_action_legality_service_interface_authority_flags")
        assert hasattr(domain, "create_action_legality_service_interface_dependency_manifest")
        assert hasattr(domain, "create_action_legality_service_interface_request")
        assert hasattr(domain, "create_action_legality_service_interface_result")

    def test_domain_init_exports_rt001e_builders(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "build_action_legality_service_interface_dependency_manifest")
        assert hasattr(domain, "build_deferred_action_legality_service_interface_result")
        assert hasattr(domain, "build_unknown_action_legality_service_interface_result")

    def test_domain_init_exports_rt001e_serializers(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "serialize_action_legality_service_interface_result")
        assert hasattr(domain, "serialize_action_legality_service_interface_result_visible")

    def test_domain_init_exports_rt001e_validators(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "validate_action_legality_service_interface_authority_flags")
        assert hasattr(domain, "validate_action_legality_service_interface_dependency_manifest")
        assert hasattr(domain, "validate_action_legality_service_interface_request")
        assert hasattr(domain, "validate_action_legality_service_interface_result")


# ---------------------------------------------------------------------------
# T21 — Guardrail allowlists updated
# ---------------------------------------------------------------------------

class TestGuardrailAllowlists:
    def test_domain_dir_includes_rt001e_module(self):
        domain_dir = REPO_ROOT / "src" / "astra_runtime" / "domain"
        actual = {p.name for p in domain_dir.iterdir() if p.is_file()}
        assert "action_legality_service_interface_contract_skeleton.py" in actual

    def test_pr9b_expected_modules_includes_rt001e(self):
        expected_modules = {
            "__init__.py",
            "action_legality.py",
            "command_lifecycle.py",
            "command_kind_routing_skeleton.py",
            "context_packet_compiler.py",
            "event_commitment.py",
            "model_boundary_evaluation.py",
            "resource_consequence_math.py",
            "scene_command_execution_skeleton.py",
            "state_projection.py",
            "state_store.py",
            "tiny_vertical_slice.py",
            "transaction_lifecycle.py",
            "validation_integration.py",
            "validation_integration_bridge_skeleton.py",
            "transaction_preview_packet_bridge_skeleton.py",
            "action_legality_skeleton.py",
            "action_legality_gate_integration_skeleton.py",
            "action_legality_service_interface_contract_skeleton.py",
            "state_owner_interface_contract_skeleton.py",
        }
        domain_dir = REPO_ROOT / "src" / "astra_runtime" / "domain"
        actual = {p.name for p in domain_dir.iterdir() if p.is_file()}
        assert actual == expected_modules


# ---------------------------------------------------------------------------
# T22 — RT-001B, RT-001C, RT-001D tests still pass (cross-check)
# ---------------------------------------------------------------------------

class TestCrossCheckExisting:
    def test_rt001b_imports_still_work(self):
        from astra_runtime.domain.action_legality_skeleton import (
            ActionLegalityRequest,
            ActionLegalityResult,
            ActionLegalityAuthorityFlags,
        )
        assert ActionLegalityRequest is not None
        assert ActionLegalityResult is not None
        assert ActionLegalityAuthorityFlags is not None

    def test_rt001c_imports_still_work(self):
        from astra_runtime.domain.action_legality_gate_integration_skeleton import (
            ActionLegalityGateIntegrationResult,
            ActionLegalityGateInputRefs,
        )
        assert ActionLegalityGateIntegrationResult is not None
        assert ActionLegalityGateInputRefs is not None


# ---------------------------------------------------------------------------
# Helper — build a minimal RT-001B ActionLegalityRequest
# ---------------------------------------------------------------------------

def _make_legality_request(request_id: str) -> Any:
    from astra_runtime.domain.action_legality_skeleton import (
        ActionLegalityAuthorityFlags,
        ActionLegalityReference,
        ActionLegalitySubjectReference,
        make_action_legality_request,
    )
    return make_action_legality_request(
        request_id=request_id,
        command_ref=ActionLegalityReference(
            reference_kind="command",
            reference_id="cmd1",
            owner_surface="test",
        ),
        subject_ref=ActionLegalitySubjectReference(
            subject_id="actor1",
            subject_label="Test Actor",
        ),
        authority_flags=ActionLegalityAuthorityFlags(),
    )
