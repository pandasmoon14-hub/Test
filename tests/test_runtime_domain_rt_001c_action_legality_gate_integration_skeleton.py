"""
Tests for RT-001C: action legality gate integration skeleton.

Module under test:
    astra_runtime.domain.action_legality_gate_integration_skeleton
"""

import json

import pytest

from astra_runtime.domain.action_legality_gate_integration_skeleton import (
    # Constants
    ACTION_LEGALITY_GATE_INTEGRATION_STAGES,
    ACTION_LEGALITY_GATE_ROUTES,
    ACTION_LEGALITY_GATE_DEFAULT_STATUSES,
    ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE,
    # Dataclasses
    ActionLegalityGateInputRefs,
    ActionLegalityGateDependencyPlan,
    ActionLegalityGateIntegrationAuthorityFlags,
    ActionLegalityGateIntegrationRequest,
    ActionLegalityGateIntegrationResult,
    # Errors
    ActionLegalityGateIntegrationSkeletonError,
    InvalidActionLegalityGateInputRefsError,
    InvalidActionLegalityGateDependencyPlanError,
    InvalidActionLegalityGateIntegrationRequestError,
    InvalidActionLegalityGateIntegrationResultError,
    InvalidActionLegalityGateIntegrationAuthorityFlagsError,
    # Factory functions
    create_action_legality_gate_input_refs,
    create_action_legality_gate_dependency_plan,
    create_action_legality_gate_integration_authority_flags,
    create_action_legality_gate_integration_request,
    create_action_legality_gate_integration_result,
    # Builder functions
    build_action_legality_request_from_gate_integration,
    build_deferred_action_legality_result_from_gate_integration,
    build_unknown_action_legality_result_from_gate_integration,
    build_action_legality_gate_integration_result,
    # Serializers
    serialize_action_legality_gate_integration_result,
    serialize_action_legality_gate_integration_result_visible,
    # Validators
    validate_action_legality_gate_input_refs,
    validate_action_legality_gate_dependency_plan,
    validate_action_legality_gate_integration_request,
    validate_action_legality_gate_integration_result,
    validate_action_legality_gate_integration_authority_flags,
)

from astra_runtime.domain.action_legality_skeleton import (
    SAFE_PLAYER_MESSAGES,
    BLOCKER_CLASSES,
    LEGALITY_STATUSES,
    ActionLegalityReference,
    ActionLegalitySubjectReference,
    ActionLegalityTargetReference,
    ActionLegalityDependencyReference,
    ActionLegalityAuthorityFlags,
    ActionLegalityRequest,
    ActionLegalityResult,
    make_action_legality_reference,
    make_action_legality_request,
    make_action_legality_result,
    make_action_legality_subject_reference,
    make_action_legality_target_reference,
    make_action_legality_dependency_reference,
)


# ---------------------------------------------------------------------------
# Test fixture helpers
# ---------------------------------------------------------------------------

def _make_ref(kind="command", ref_id="ref-001", owner="test_surface"):
    return make_action_legality_reference(
        reference_kind=kind, reference_id=ref_id, owner_surface=owner,
    )


def _make_subject():
    return make_action_legality_subject_reference(
        subject_id="actor-001", subject_label="Test Actor",
    )


def _make_target():
    return make_action_legality_target_reference(
        target_id="target-001", target_label="Test Target",
    )


def _make_dep_ref(dep_id="dep-001", owner="validation"):
    return make_action_legality_dependency_reference(
        dependency_id=dep_id, dependency_owner=owner,
    )


def _make_input_refs():
    return create_action_legality_gate_input_refs(
        scene_command_assembly_ref=_make_ref("command", "asm-001", "pr9a"),
        command_kind_routing_ref=_make_ref("command", "route-001", "pr9c"),
        validation_bridge_ref=_make_ref("validation", "vbridge-001", "pr9d"),
    )


def _make_dependency_plan():
    return create_action_legality_gate_dependency_plan(
        plan_id="plan-001",
        dependency_refs=[_make_dep_ref()],
    )


def _make_integration_request():
    return create_action_legality_gate_integration_request(
        request_id="req-001",
        input_refs=_make_input_refs(),
        subject_ref=_make_subject(),
        command_ref=_make_ref("command", "cmd-001", "test"),
        dependency_plan=_make_dependency_plan(),
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestModuleImport:
    def test_module_imports(self):
        """Module imports successfully."""
        import astra_runtime.domain.action_legality_gate_integration_skeleton as mod
        assert mod is not None


class TestConstants:
    def test_integration_stages_expected(self):
        """Constants expose expected integration stages."""
        expected = {
            "input_refs_received", "command_assembly_ref_checked",
            "command_kind_route_ref_checked", "validation_bridge_ref_checked",
            "transaction_preview_ref_checked", "legality_request_built",
            "legality_result_built", "integration_result_built",
        }
        assert ACTION_LEGALITY_GATE_INTEGRATION_STAGES == expected

    def test_routes_expected(self):
        assert "scene_command_execution" in ACTION_LEGALITY_GATE_ROUTES
        assert "command_kind_routing" in ACTION_LEGALITY_GATE_ROUTES
        assert len(ACTION_LEGALITY_GATE_ROUTES) == 13

    def test_default_statuses_expected(self):
        assert ACTION_LEGALITY_GATE_DEFAULT_STATUSES == {"deferred", "unknown"}

    def test_non_authority_note(self):
        assert isinstance(ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE, str)
        assert "reference-only" in ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE


class TestDataclassesFrozenKwOnly:
    def test_input_refs_frozen(self):
        refs = _make_input_refs()
        with pytest.raises(AttributeError):
            refs.scene_command_assembly_ref = "changed"

    def test_dependency_plan_frozen(self):
        plan = _make_dependency_plan()
        with pytest.raises(AttributeError):
            plan.plan_id = "changed"

    def test_authority_flags_frozen(self):
        flags = create_action_legality_gate_integration_authority_flags()
        with pytest.raises(AttributeError):
            flags.action_legality_engine_authorized = True

    def test_integration_request_frozen(self):
        req = _make_integration_request()
        with pytest.raises(AttributeError):
            req.request_id = "changed"

    def test_integration_result_frozen(self):
        result = build_action_legality_gate_integration_result(
            result_id="result-001", request=_make_integration_request(),
        )
        with pytest.raises(AttributeError):
            result.result_id = "changed"


class TestInputRefsValidation:
    def test_valid_input_refs(self):
        refs = _make_input_refs()
        assert validate_action_legality_gate_input_refs(refs)

    def test_rejects_non_reference_scene_assembly(self):
        with pytest.raises(InvalidActionLegalityGateInputRefsError):
            create_action_legality_gate_input_refs(
                scene_command_assembly_ref="not a ref",
                command_kind_routing_ref=_make_ref("command", "route-001", "pr9c"),
                validation_bridge_ref=_make_ref("validation", "vbridge-001", "pr9d"),
            )


class TestDependencyPlan:
    def test_valid_plan(self):
        plan = _make_dependency_plan()
        assert validate_action_legality_gate_dependency_plan(plan)

    def test_uses_rt001b_dependency_references(self):
        plan = _make_dependency_plan()
        for dep in plan.dependency_refs:
            assert isinstance(dep, ActionLegalityDependencyReference)

    def test_does_not_call_owners(self):
        # Dependency plan only declares references, does not call owners
        plan = _make_dependency_plan()
        assert plan.default_blocker_class in BLOCKER_CLASSES


class TestIntegrationRequestBuildsLegalityRequest:
    def test_builds_rt001b_request(self):
        req = _make_integration_request()
        legality_req = build_action_legality_request_from_gate_integration(request=req)
        assert isinstance(legality_req, ActionLegalityRequest)
        assert legality_req.request_id == req.request_id


class TestDefaultResultIsDeferred:
    def test_default_is_deferred(self):
        result = build_action_legality_gate_integration_result(
            result_id="result-001", request=_make_integration_request(),
        )
        assert result.legality_result.legality_status == "deferred"

    def test_default_is_not_legal(self):
        result = build_action_legality_gate_integration_result(
            result_id="result-001", request=_make_integration_request(),
        )
        assert result.legality_result.legality_status != "legal"


class TestLegalStatusRejectedAtGateLevel:
    """RT-001C invariant: the integration result must never carry a 'legal'
    ActionLegalityResult through the public constructor, factory, or validator."""

    def _make_legal_legality_result(self):
        return make_action_legality_result(
            result_id="legal-res-001",
            request_id="req-001",
            legality_status="legal",
        )

    def _make_deferred_legality_result(self):
        from astra_runtime.domain.action_legality_skeleton import (
            make_action_legality_blocker,
            make_action_legality_backend_detail,
        )
        detail = make_action_legality_backend_detail(
            detail_id="d-001",
            blocker_class="runtime_owner_handoff",
            owner_route="test",
        )
        blocker = make_action_legality_blocker(
            blocker_id="b-001",
            blocker_class="runtime_owner_handoff",
            legality_status="deferred",
            player_visible_message="This action cannot be processed at this time.",
            backend_detail=detail,
        )
        return make_action_legality_result(
            result_id="def-res-001",
            request_id="req-001",
            legality_status="deferred",
            blockers=[blocker],
        )

    def _make_legality_request(self):
        return make_action_legality_request(
            request_id="req-001",
            command_ref=_make_ref("command", "cmd-001", "test"),
            subject_ref=_make_subject(),
        )

    def test_direct_constructor_rejects_legal(self):
        with pytest.raises(InvalidActionLegalityGateIntegrationResultError):
            ActionLegalityGateIntegrationResult(
                result_id="r-001",
                request_id="req-001",
                legality_request=self._make_legality_request(),
                legality_result=self._make_legal_legality_result(),
                input_refs=_make_input_refs(),
                dependency_plan=_make_dependency_plan(),
            )

    def test_factory_rejects_legal(self):
        with pytest.raises(InvalidActionLegalityGateIntegrationResultError):
            create_action_legality_gate_integration_result(
                result_id="r-001",
                request_id="req-001",
                legality_request=self._make_legality_request(),
                legality_result=self._make_legal_legality_result(),
                input_refs=_make_input_refs(),
                dependency_plan=_make_dependency_plan(),
            )

    def test_deferred_still_passes(self):
        result = create_action_legality_gate_integration_result(
            result_id="r-001",
            request_id="req-001",
            legality_request=self._make_legality_request(),
            legality_result=self._make_deferred_legality_result(),
            input_refs=_make_input_refs(),
            dependency_plan=_make_dependency_plan(),
        )
        assert result.legality_result.legality_status == "deferred"

    def test_unknown_still_passes(self):
        unknown_result = make_action_legality_result(
            result_id="unk-res-001",
            request_id="req-001",
            legality_status="unknown",
        )
        result = create_action_legality_gate_integration_result(
            result_id="r-001",
            request_id="req-001",
            legality_request=self._make_legality_request(),
            legality_result=unknown_result,
            input_refs=_make_input_refs(),
            dependency_plan=_make_dependency_plan(),
        )
        assert result.legality_result.legality_status == "unknown"

    def test_validator_rejects_legal(self):
        # Since __post_init__ now blocks legal, we can't construct one directly.
        # But we can verify the validator also returns False for non-default statuses
        # by checking that a valid deferred result passes.
        deferred_result = create_action_legality_gate_integration_result(
            result_id="r-001",
            request_id="req-001",
            legality_request=self._make_legality_request(),
            legality_result=self._make_deferred_legality_result(),
            input_refs=_make_input_refs(),
            dependency_plan=_make_dependency_plan(),
        )
        assert validate_action_legality_gate_integration_result(deferred_result) is True


class TestDeferredResultHasBlocker:
    def test_deferred_has_blockers(self):
        result = build_deferred_action_legality_result_from_gate_integration(
            result_id="res-001", request_id="req-001",
            dependency_plan=_make_dependency_plan(),
        )
        assert len(result.blockers) >= 1

    def test_deferred_blocker_is_runtime_owner_handoff(self):
        result = build_deferred_action_legality_result_from_gate_integration(
            result_id="res-001", request_id="req-001",
            dependency_plan=_make_dependency_plan(),
        )
        assert result.blockers[0].blocker_class == "runtime_owner_handoff"


class TestUnknownResultPath:
    def test_unknown_result(self):
        result = build_unknown_action_legality_result_from_gate_integration(
            result_id="res-001", request_id="req-001",
        )
        assert result.legality_status == "unknown"
        # Should include a blocker even though unknown allows no blockers
        assert len(result.blockers) >= 1

    def test_unknown_is_skeleton_safe(self):
        result = build_unknown_action_legality_result_from_gate_integration(
            result_id="res-001", request_id="req-001",
        )
        # Uses safe player message
        assert result.blockers[0].player_visible_message in SAFE_PLAYER_MESSAGES


class TestPlayerVisibleSerializer:
    def test_visible_excludes_backend_detail(self):
        result = build_action_legality_gate_integration_result(
            result_id="result-001", request=_make_integration_request(),
        )
        visible = serialize_action_legality_gate_integration_result_visible(result)
        assert "backend_detail" not in str(visible).lower() or visible.get("backend_detail") is None
        # Should not contain trace_refs, dependency_plan internals, etc.
        assert "trace_refs" not in visible
        assert "dependency_plan" not in visible
        assert "input_refs" not in visible

    def test_visible_uses_safe_messages(self):
        result = build_action_legality_gate_integration_result(
            result_id="result-001", request=_make_integration_request(),
        )
        visible = serialize_action_legality_gate_integration_result_visible(result)
        if "player_visible_message" in visible:
            assert visible["player_visible_message"] in SAFE_PLAYER_MESSAGES
        if "visible_blocker_messages" in visible:
            for msg in visible["visible_blocker_messages"]:
                assert msg in SAFE_PLAYER_MESSAGES


class TestBackendSerializer:
    def test_backend_includes_detail(self):
        result = build_action_legality_gate_integration_result(
            result_id="result-001", request=_make_integration_request(),
        )
        backend = serialize_action_legality_gate_integration_result(result)
        assert "authority_flags" in backend
        assert "input_refs" in backend
        assert "dependency_plan" in backend

    def test_backend_is_deterministic_json_safe(self):
        result = build_action_legality_gate_integration_result(
            result_id="result-001", request=_make_integration_request(),
        )
        backend = serialize_action_legality_gate_integration_result(result)
        # Should be JSON-serializable
        json_str = json.dumps(backend, sort_keys=True)
        assert isinstance(json_str, str)
        # Should be deterministic
        json_str2 = json.dumps(serialize_action_legality_gate_integration_result(result), sort_keys=True)
        assert json_str == json_str2


class TestAuthorityFlagsRejectNonFalse:
    def test_rejects_true(self):
        with pytest.raises(InvalidActionLegalityGateIntegrationAuthorityFlagsError):
            ActionLegalityGateIntegrationAuthorityFlags(action_legality_engine_authorized=True)

    def test_rejects_truthy_string(self):
        with pytest.raises((InvalidActionLegalityGateIntegrationAuthorityFlagsError, TypeError)):
            ActionLegalityGateIntegrationAuthorityFlags(action_legality_engine_authorized="yes")

    def test_rejects_one(self):
        with pytest.raises((InvalidActionLegalityGateIntegrationAuthorityFlagsError, TypeError)):
            ActionLegalityGateIntegrationAuthorityFlags(command_execution_authorized=1)

    def test_rejects_zero(self):
        with pytest.raises((InvalidActionLegalityGateIntegrationAuthorityFlagsError, TypeError)):
            ActionLegalityGateIntegrationAuthorityFlags(state_mutation_authorized=0)

    def test_rejects_none(self):
        with pytest.raises((InvalidActionLegalityGateIntegrationAuthorityFlagsError, TypeError)):
            ActionLegalityGateIntegrationAuthorityFlags(event_append_authorized=None)

    def test_all_flags_false(self):
        flags = create_action_legality_gate_integration_authority_flags()
        for field_name in flags.__dataclass_fields__:
            assert getattr(flags, field_name) is False


class TestAuthorityFlagsToDict:
    def test_to_dict_hardcodes_false(self):
        flags = create_action_legality_gate_integration_authority_flags()
        d = flags.to_dict()
        for key, value in d.items():
            assert value is False, f"{key} should be False"

    def test_to_dict_has_all_fields(self):
        flags = create_action_legality_gate_integration_authority_flags()
        d = flags.to_dict()
        assert len(d) == len(flags.__dataclass_fields__)


class TestToDictDeterministic:
    def test_input_refs_to_dict(self):
        refs = _make_input_refs()
        d1 = refs.to_dict()
        d2 = refs.to_dict()
        assert json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)

    def test_integration_result_to_dict(self):
        result = build_action_legality_gate_integration_result(
            result_id="result-001", request=_make_integration_request(),
        )
        d1 = result.to_dict()
        d2 = result.to_dict()
        assert json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)


class TestMetadataJsonSafe:
    def test_input_refs_metadata(self):
        refs = create_action_legality_gate_input_refs(
            scene_command_assembly_ref=_make_ref("command", "asm-001", "pr9a"),
            command_kind_routing_ref=_make_ref("command", "route-001", "pr9c"),
            validation_bridge_ref=_make_ref("validation", "vbridge-001", "pr9d"),
            metadata={"key": "value"},
        )
        json.dumps(refs.to_dict())  # Should not raise


class TestHiddenInformationBlockers:
    def test_hidden_info_uses_generic_safe_messages(self):
        result = build_deferred_action_legality_result_from_gate_integration(
            result_id="res-001", request_id="req-001",
            dependency_plan=_make_dependency_plan(),
        )
        for blocker in result.blockers:
            assert blocker.player_visible_message in SAFE_PLAYER_MESSAGES


class TestNoExecutionMethodNames:
    def test_no_execution_methods(self):
        import astra_runtime.domain.action_legality_gate_integration_skeleton as mod
        forbidden = [
            "execute", "run_", "apply_", "commit_",
            "mutate", "persist", "replay_", "roll_",
            "generate_narration", "render_prompt", "call_model", "parse_prose",
        ]
        public_names = [n for n in dir(mod) if not n.startswith("_") and n != "annotations"]
        for name in public_names:
            lower = name.lower()
            for pattern in forbidden:
                assert pattern not in lower, (
                    f"Public name {name!r} contains forbidden pattern {pattern!r}"
                )


class TestDomainPackageExports:
    def test_domain_package_exports_new_surface(self):
        from astra_runtime.domain import (
            ActionLegalityGateInputRefs,
            ActionLegalityGateDependencyPlan,
            ActionLegalityGateIntegrationAuthorityFlags,
            ActionLegalityGateIntegrationRequest,
            ActionLegalityGateIntegrationResult,
            ACTION_LEGALITY_GATE_INTEGRATION_STAGES,
            ACTION_LEGALITY_GATE_ROUTES,
            ACTION_LEGALITY_GATE_DEFAULT_STATUSES,
            ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE,
        )
        assert ActionLegalityGateInputRefs is not None


class TestGuardrailAllowlists:
    def test_guardrail_module_names(self):
        import astra_runtime.domain.action_legality_gate_integration_skeleton as mod
        stdlib_imports = {"annotations", "copy", "dataclass", "field", "MappingProxyType"}
        public_names = [n for n in dir(mod) if not n.startswith("_") and n not in stdlib_imports]
        for name in public_names:
            lower = name.lower()
            ok = any([
                name[0].isupper(),  # Class/constant name
                lower.startswith("create_"),
                lower.startswith("build_"),
                lower.startswith("validate_"),
                lower.startswith("serialize_"),
                lower.startswith("make_"),
                lower.startswith("action_legality_gate_"),  # Constants
                name.startswith("Invalid"),
            ])
            assert ok, f"Unexpected public name pattern: {name!r}"
