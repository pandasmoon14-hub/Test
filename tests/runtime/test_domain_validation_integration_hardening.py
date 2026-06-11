"""PR-4C hardening tests for validation integration cross-field invariants."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    VALIDATION_PUBLIC_REASON_CODES,
    InvalidValidationFailureRouteError,
    InvalidValidationIntegrationRequestError,
    InvalidValidationIntegrationResultError,
    ValidationFailureRoute,
    ValidationIntegrationRequest,
    ValidationIntegrationResult,
    ValidationIntegrationService,
    create_validation_failure_route,
    create_validation_integration_dependency,
    create_validation_integration_request,
    create_validation_integration_result,
    validate_validation_failure_route,
    validate_validation_integration_request,
    validate_validation_integration_result,
)

REQUIRED_PUBLIC_CODES = {
    "validation_pending",
    "validation_blocked",
    "validation_rejected",
    "validation_quarantined",
    "validation_escalated",
    "unsupported_validation_scope",
}

ROUTE_DECISION_COMPATIBILITY = {
    "block_command_before_transaction": {
        "validation_failed",
        "rejected_by_missing_command_ref",
        "rejected_by_authority_mismatch",
        "rejected_by_phase_boundary",
    },
    "block_transaction_before_commitment": {
        "validation_failed",
        "rejected_by_missing_state_ref",
        "rejected_by_missing_transaction_ref",
        "rejected_by_missing_invariant_set",
        "rejected_by_schema_mismatch",
        "rejected_by_authority_mismatch",
        "rejected_by_phase_boundary",
    },
    "block_event_commitment": {
        "validation_failed",
        "rejected_by_missing_event_commitment_ref",
        "rejected_by_missing_state_ref",
        "rejected_by_missing_invariant_set",
        "rejected_by_hidden_information_risk",
        "rejected_by_provenance_gap",
        "rejected_by_schema_mismatch",
        "rejected_by_authority_mismatch",
        "rejected_by_phase_boundary",
    },
    "quarantine_transaction": {"quarantined_for_review"},
    "quarantine_event_commitment": {"quarantined_for_review"},
    "quarantine_generated_content": {"quarantined_for_review"},
    "escalate_doctrine_gap": {"escalated_to_doctrine"},
    "reject_source_local_authority": {"rejected_by_authority_mismatch", "rejected_by_phase_boundary"},
    "reject_hidden_info_leak": {"rejected_by_hidden_information_risk"},
    "reject_schema_mismatch": {"rejected_by_schema_mismatch"},
    "reject_phase_boundary_violation": {"rejected_by_phase_boundary"},
    "request_downstream_domain_validation": {"validation_ready", "unsupported_validation_scope"},
}

REQUESTABLE_STAGES = {
    "validation_integration_requested",
    "validation_scope_declared",
    "dependency_refs_bound",
    "state_refs_bound",
    "transaction_refs_bound",
    "event_commitment_refs_bound",
    "invariant_set_declared",
    "invariant_precheck_requested",
    "domain_validation_required",
    "domain_validation_referenced",
}

OUTCOME_STAGES = {
    "invariant_precheck_passed",
    "invariant_precheck_failed",
    "hidden_info_safety_checked",
    "provenance_checked",
    "validation_passed",
    "validation_failed",
    "validation_quarantined",
    "validation_escalated",
    "validation_cancelled",
    "validation_superseded",
}

READY_STAGES = {
    "validation_integration_requested",
    "validation_scope_declared",
    "dependency_refs_bound",
    "state_refs_bound",
    "transaction_refs_bound",
    "event_commitment_refs_bound",
    "invariant_set_declared",
    "invariant_precheck_requested",
    "invariant_precheck_passed",
    "domain_validation_required",
    "domain_validation_referenced",
    "hidden_info_safety_checked",
    "provenance_checked",
}

REJECTED_DECISIONS = {
    "rejected_by_missing_command_ref",
    "rejected_by_missing_state_ref",
    "rejected_by_missing_transaction_ref",
    "rejected_by_missing_event_commitment_ref",
    "rejected_by_missing_invariant_set",
    "rejected_by_hidden_information_risk",
    "rejected_by_provenance_gap",
    "rejected_by_schema_mismatch",
    "rejected_by_authority_mismatch",
    "rejected_by_phase_boundary",
}


def _route_kwargs(route_type="block_command_before_transaction", decision="validation_failed", **kwargs):
    data = {
        "route_id": f"route-{route_type}-{decision}",
        "route_type": route_type,
        "decision": decision,
        "subject_ref_id": "cmd-1",
        "quarantines": route_type.startswith("quarantine_"),
        "escalates": route_type == "escalate_doctrine_gap",
    }
    data.update(kwargs)
    return data


def route(route_type="block_command_before_transaction", decision="validation_failed", **kwargs):
    return create_validation_failure_route(**_route_kwargs(route_type, decision, **kwargs))


def dep(dependency_id, dependency_type, reference_id, *, required=True, satisfied=True):
    return create_validation_integration_dependency(
        dependency_id=dependency_id,
        dependency_type=dependency_type,
        reference_id=reference_id,
        required=required,
        satisfied=satisfied,
    )


def result_deps(validation_request_id="vreq-1", trace_id="trace-1", validation_result_ref_id="vres-1", provenance_ref_ids=()):
    deps = [
        dep("dep-request", "validation_request_ref", validation_request_id),
    ]
    if isinstance(trace_id, str) and trace_id.strip():
        deps.append(dep("dep-trace", "runtime_trace_ref", trace_id))
    if isinstance(validation_result_ref_id, str) and validation_result_ref_id.strip():
        deps.append(dep("dep-result", "validation_result_ref", validation_result_ref_id))
    for index, ref in enumerate(provenance_ref_ids or ()):
        if isinstance(ref, str) and ref.strip():
            deps.append(dep(f"dep-provenance-{index}", "generated_content_provenance_ref", ref))
    return tuple(deps)


def _result_kwargs(decision="validation_failed", final_stage=None, **kwargs):
    if final_stage is None:
        final_stage = {
            "validation_passed": "validation_passed",
            "validation_failed": "validation_failed",
            "quarantined_for_review": "validation_quarantined",
            "escalated_to_doctrine": "validation_escalated",
            "unsupported_validation_scope": "domain_validation_required",
            "validation_ready": "validation_integration_requested",
        }.get(decision, "validation_failed")
    data = {
        "validation_request_id": "vreq-1",
        "decision": decision,
        "final_stage": final_stage,
        "subject_type": "command",
        "subject_ref_id": "cmd-1",
        "request_subject_type": "command",
        "request_subject_ref_id": "cmd-1",
        "validation_result_ref_id": "vres-1",
        "failure_routes": [route(decision=decision)] if decision == "validation_failed" else [],
        "trace_id": "trace-1",
    }
    if decision in REJECTED_DECISIONS:
        route_type = next(rt for rt, decisions in ROUTE_DECISION_COMPATIBILITY.items() if decision in decisions)
        data["failure_routes"] = [route(route_type, decision)]
    if decision == "validation_passed":
        data.update({"passed": True, "blocking": False, "failure_routes": []})
    if decision == "quarantined_for_review":
        data.update({
            "quarantined": True,
            "failure_routes": [route("quarantine_transaction", decision)],
        })
    if decision == "escalated_to_doctrine":
        data.update({
            "escalated": True,
            "failure_routes": [route("escalate_doctrine_gap", decision)],
        })
    if decision == "unsupported_validation_scope":
        data.update({
            "failure_routes": [route("request_downstream_domain_validation", decision)],
        })
    if decision == "validation_ready":
        data.update({
            "validation_result_ref_id": None,
            "failure_routes": [],
        })
    data.update(kwargs)
    if "request_subject_type" not in kwargs:
        data["request_subject_type"] = data["subject_type"]
    if "request_subject_ref_id" not in kwargs:
        data["request_subject_ref_id"] = data["subject_ref_id"]
    data.setdefault(
        "dependencies",
        result_deps(
            data["validation_request_id"],
            data.get("trace_id"),
            data.get("validation_result_ref_id"),
            data.get("provenance_ref_ids", ()),
        ),
    )
    return data


def result(decision="validation_failed", final_stage=None, **kwargs):
    return create_validation_integration_result(**_result_kwargs(decision, final_stage, **kwargs))


class TestPublicReasonSafety:
    def test_public_reason_codes_are_exported_and_complete(self):
        assert REQUIRED_PUBLIC_CODES == set(VALIDATION_PUBLIC_REASON_CODES)

    def test_player_visible_requires_safe_reasoned_route(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            route(player_visible=True, hidden_info_safe=False, public_reason_code="validation_blocked")
        with pytest.raises(InvalidValidationFailureRouteError):
            route(player_visible=True)
        with pytest.raises(InvalidValidationFailureRouteError):
            route(public_reason_code="raw_hidden_detail")
        ok = route(player_visible=True, public_reason_code="validation_blocked")
        assert ok.to_public_dict() == {
            "reason_code": "validation_blocked",
            "blocking": True,
            "quarantines": False,
            "escalates": False,
        }

    def test_public_dict_excludes_backend_fields(self):
        r = route(
            player_visible=True,
            public_reason_code="validation_blocked",
            metadata={"raw_hidden_reason": "do-not-show"},
        )
        public = r.to_public_dict()
        for forbidden in {"route_id", "route_type", "subject_ref_id", "metadata", "trace_id"}:
            assert forbidden not in public
        with pytest.raises(InvalidValidationFailureRouteError):
            route().to_public_dict()

    def test_reason_decision_compatibility(self):
        route(decision="validation_failed", public_reason_code="validation_rejected")
        route("quarantine_transaction", "quarantined_for_review", public_reason_code="validation_quarantined")
        with pytest.raises(InvalidValidationFailureRouteError):
            route(decision="validation_failed", public_reason_code="validation_escalated")


class TestRouteConsistency:
    def test_blocking_trace_and_flag_exactness(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            route(blocking=False)
        with pytest.raises(InvalidValidationFailureRouteError):
            route(trace_required=False)
        with pytest.raises(InvalidValidationFailureRouteError):
            route("quarantine_transaction", "quarantined_for_review", quarantines=False)
        with pytest.raises(InvalidValidationFailureRouteError):
            route(quarantines=True)
        with pytest.raises(InvalidValidationFailureRouteError):
            route("escalate_doctrine_gap", "escalated_to_doctrine", escalates=False)
        with pytest.raises(InvalidValidationFailureRouteError):
            route(escalates=True)
        with pytest.raises(InvalidValidationFailureRouteError):
            route(decision="validation_passed")

    @pytest.mark.parametrize("route_type,decisions", ROUTE_DECISION_COMPATIBILITY.items())
    def test_every_route_decision_compatibility_combination(self, route_type, decisions):
        for decision in decisions:
            assert validate_validation_failure_route(route(route_type, decision)) is True

    @pytest.mark.parametrize(
        "route_type,decision",
        [
            ("quarantine_transaction", "validation_failed"),
            ("escalate_doctrine_gap", "validation_failed"),
            ("block_command_before_transaction", "quarantined_for_review"),
        ],
    )
    def test_incompatible_route_decision_pairs_rejected(self, route_type, decision):
        with pytest.raises(InvalidValidationFailureRouteError):
            route(route_type, decision)


class TestRequestStages:
    @pytest.mark.parametrize("stage", sorted(REQUESTABLE_STAGES))
    def test_allowed_request_stages(self, stage):
        assert create_validation_integration_request(
            validation_request_id=f"req-{stage}",
            subject_type="command",
            subject_ref_id="cmd-1",
            requesting_service="svc",
            requested_stage=stage,
        ).requested_stage == stage

    @pytest.mark.parametrize("stage", sorted(OUTCOME_STAGES))
    def test_outcome_request_stages_rejected(self, stage):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            create_validation_integration_request(
                validation_request_id=f"req-{stage}",
                subject_type="command",
                subject_ref_id="cmd-1",
                requesting_service="svc",
                requested_stage=stage,
            )
        manual = ValidationIntegrationRequest(
            validation_request_id="req-manual",
            subject_type="command",
            subject_ref_id="cmd-1",
            requesting_service="svc",
            requested_stage=stage,
        )
        assert validate_validation_integration_request(manual) is False


class TestSubjectTraceAndProvenance:
    def test_subject_identity_and_trace_required(self):
        with pytest.raises(TypeError):
            create_validation_integration_result(  # type: ignore[call-arg]
                validation_request_id="vreq", decision="validation_ready", final_stage="validation_integration_requested", trace_id="trace"
            )
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(subject_type="bad")
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(subject_ref_id="")
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(trace_id=None)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(trace_id="")

    def test_result_references_required_except_ready(self):
        assert result("validation_ready", "validation_integration_requested", validation_result_ref_id=None).validation_result_ref_id is None
        for decision in ["validation_passed", "validation_failed", "quarantined_for_review", "escalated_to_doctrine", "unsupported_validation_scope"]:
            with pytest.raises(InvalidValidationIntegrationResultError):
                result(decision, _result_kwargs(decision)["final_stage"], validation_result_ref_id=None)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(validation_result_ref_id="")

    def test_provenance_sequence_and_linkage(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(provenance_ref_ids="prov-1")
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(provenance_ref_ids=[""])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(provenance_ref_ids=["prov-1"], provenance_checked=False)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(
                "validation_passed",
                "validation_passed",
                subject_type="generated_content",
                subject_ref_id="gen-1",
                provenance_checked=False,
                provenance_ref_ids=[],
            )
        ordinary = result("validation_passed", "validation_passed")
        assert ordinary.provenance_checked is False
        generated = result(
            "validation_passed",
            "validation_passed",
            subject_type="generated_content",
            subject_ref_id="gen-1",
            provenance_checked=True,
            provenance_ref_ids=["prov-1"],
        )
        assert generated.provenance_ref_ids == ("prov-1",)
        assert generated.to_dict()["provenance_ref_ids"] == ["prov-1"]


class TestDecisionStageAndResultInvariants:
    @pytest.mark.parametrize(
        "decision,stage",
        [
            ("validation_passed", "validation_passed"),
            ("validation_failed", "validation_failed"),
            ("quarantined_for_review", "validation_quarantined"),
            ("escalated_to_doctrine", "validation_escalated"),
            ("unsupported_validation_scope", "domain_validation_required"),
            *[(d, "validation_failed") for d in sorted(REJECTED_DECISIONS)],
        ],
    )
    def test_decision_stage_matrix_accepts_allowed_terminal_families(self, decision, stage):
        assert result(decision, stage).final_stage == stage

    @pytest.mark.parametrize("stage", sorted(READY_STAGES))
    def test_validation_ready_allowed_stages(self, stage):
        kwargs = {"invariant_precheck_ref_id": "precheck-1"} if stage == "invariant_precheck_passed" else {}
        if stage == "provenance_checked":
            kwargs["provenance_checked"] = True
        assert result("validation_ready", stage, **kwargs).final_stage == stage

    @pytest.mark.parametrize(
        "decision,stage",
        [
            ("validation_passed", "validation_failed"),
            ("validation_failed", "validation_passed"),
            ("rejected_by_missing_command_ref", "validation_quarantined"),
            ("quarantined_for_review", "validation_failed"),
            ("escalated_to_doctrine", "validation_quarantined"),
            ("unsupported_validation_scope", "validation_failed"),
            ("validation_ready", "validation_passed"),
            ("validation_ready", "validation_failed"),
            ("validation_ready", "validation_quarantined"),
            ("validation_ready", "validation_escalated"),
        ],
    )
    def test_representative_invalid_stage_pairs(self, decision, stage):
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(decision, stage)

    @pytest.mark.parametrize(
        "bad_kwargs",
        [
            {"passed": False},
            {"blocking": True},
            {"validation_result_ref_id": None},
            {"trace_id": None},
            {"failure_routes": [route()]},
            {"quarantined": True},
            {"escalated": True},
            {"hidden_info_safe": False},
            {"final_stage": "validation_failed"},
            {"state_mutation_allowed": True},
            {"event_append_allowed": True},
            {"persistence_allowed": True},
            {"model_authority_allowed": True},
        ],
    )
    def test_passed_result_invariants(self, bad_kwargs):
        data = {"decision": "validation_passed", "final_stage": "validation_passed", **bad_kwargs}
        with pytest.raises(InvalidValidationIntegrationResultError):
            create_validation_integration_result(**_result_kwargs(**data))

    def test_failure_quarantine_escalation_unsupported_and_ready_invariants(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("validation_failed", "validation_failed", failure_routes=[])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("validation_failed", "validation_failed", failure_routes=[route(decision="rejected_by_missing_command_ref")])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("rejected_by_missing_command_ref", "validation_failed", failure_routes=[])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("rejected_by_missing_command_ref", "validation_failed", failure_routes=[route(decision="validation_failed")])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("validation_failed", "validation_failed", blocking=False)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("validation_failed", "validation_failed", quarantined=True)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("validation_failed", "validation_failed", escalated=True)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("quarantined_for_review", "validation_quarantined", quarantined=False)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("quarantined_for_review", "validation_quarantined", failure_routes=[route()])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("escalated_to_doctrine", "validation_escalated", escalated=False)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("escalated_to_doctrine", "validation_escalated", failure_routes=[route()])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("unsupported_validation_scope", "domain_validation_required", failure_routes=[])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("unsupported_validation_scope", "domain_validation_required", failure_routes=[route()])
        assert result("validation_ready", "validation_integration_requested", failure_routes=[]).validation_result_ref_id is None
        assert result("validation_ready", "domain_validation_required", failure_routes=[route("request_downstream_domain_validation", "validation_ready")])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("validation_ready", "validation_integration_requested", failure_routes=[route()])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("validation_ready", "validation_integration_requested", quarantined=True)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("validation_ready", "validation_integration_requested", escalated=True)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result("validation_ready", "validation_integration_requested", blocking=False)


class TestManualObjectParityAndNonExecution:
    def test_manual_invalid_objects_rejected(self):
        valid_route = route()
        base = _result_kwargs()
        manual_missing_trace = ValidationIntegrationResult(**{**base, "trace_id": None})
        assert validate_validation_integration_result(manual_missing_trace) is False
        manual_missing_ref = ValidationIntegrationResult(**{**base, "validation_result_ref_id": None})
        assert validate_validation_integration_result(manual_missing_ref) is False
        manual_bad_stage = ValidationIntegrationResult(**{**base, "final_stage": "validation_passed"})
        assert validate_validation_integration_result(manual_bad_stage) is False
        manual_blocking_pass = ValidationIntegrationResult(**_result_kwargs("validation_passed", "validation_passed", blocking=True))
        assert validate_validation_integration_result(manual_blocking_pass) is False
        manual_gen_no_prov = ValidationIntegrationResult(**_result_kwargs("validation_passed", "validation_passed", subject_type="generated_content"))
        assert validate_validation_integration_result(manual_gen_no_prov) is False
        assert validate_validation_failure_route(ValidationFailureRoute(**_route_kwargs(decision="validation_passed"))) is False
        assert validate_validation_failure_route(ValidationFailureRoute(**_route_kwargs("quarantine_transaction", "quarantined_for_review", quarantines=False))) is False
        assert validate_validation_failure_route(ValidationFailureRoute(**_route_kwargs("escalate_doctrine_gap", "escalated_to_doctrine", escalates=False))) is False
        assert validate_validation_failure_route(ValidationFailureRoute(**_route_kwargs(player_visible=True))) is False
        assert validate_validation_integration_request(ValidationIntegrationRequest(
            validation_request_id="vreq", subject_type="command", subject_ref_id="cmd", requesting_service="svc", requested_stage="validation_passed"
        )) is False
        assert valid_route.blocking is True

    def test_service_remains_stateless_and_non_executing(self):
        svc = ValidationIntegrationService()
        assert svc.__dict__ == {}
        forbidden = {
            "execute", "run", "enforce", "evaluate", "evaluate_rules", "run_validation_checks",
            "run_invariant_prechecks", "mutate", "apply", "apply_delta", "append", "commit",
            "persist", "save", "load", "replay", "rollback", "resolve", "roll", "prompt",
            "model", "narrate",
        }
        public_names = {name for name in dir(ValidationIntegrationService) if not name.startswith("_")}
        assert forbidden.isdisjoint(public_names)
        import astra_runtime.domain.validation_integration as module

        assert not hasattr(module, "run_validation_checks")
        assert not hasattr(module, "run_invariant_prechecks")
