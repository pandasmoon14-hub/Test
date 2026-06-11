"""PR-4E residual hardening tests for validation integration identity linkage."""

from __future__ import annotations

import pathlib
from types import MappingProxyType

import pytest

import astra_runtime.domain as domain
from astra_runtime.domain import (
    VALIDATION_SUBJECT_RELATIONS,
    InvalidValidationFailureRouteError,
    InvalidValidationIntegrationRequestError,
    InvalidValidationIntegrationResultError,
    ValidationFailureRoute,
    ValidationIntegrationRequest,
    ValidationIntegrationResult,
    create_validation_failure_route,
    create_validation_integration_dependency,
    create_validation_integration_request,
    create_validation_integration_result,
    validate_validation_failure_route,
    validate_validation_integration_request,
    validate_validation_integration_result,
)

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOMAIN_FILE = ROOT / "src" / "astra_runtime" / "domain" / "validation_integration.py"


def dep(dependency_id: str, dependency_type: str, reference_id: str, *, required=True, satisfied=True):
    return create_validation_integration_dependency(
        dependency_id=dependency_id,
        dependency_type=dependency_type,
        reference_id=reference_id,
        required=required,
        satisfied=satisfied,
    )


def base_deps(*, request="vreq-1", trace="trace-1", result="vres-1", provenance=()):
    deps = [
        dep("dep-request", "validation_request_ref", request),
        dep("dep-trace", "runtime_trace_ref", trace),
    ]
    if result is not None:
        deps.append(dep("dep-result", "validation_result_ref", result))
    for index, ref in enumerate(provenance):
        deps.append(dep(f"dep-prov-{index}", "generated_content_provenance_ref", ref))
    return tuple(deps)


def route(**kwargs):
    data = dict(
        route_id="route-1",
        route_type="block_command_before_transaction",
        decision="validation_failed",
        subject_type="command",
        subject_ref_id="cmd-1",
        subject_relation="same_subject",
    )
    data.update(kwargs)
    if data["route_type"].startswith("quarantine_"):
        data["quarantines"] = True
    if data["route_type"] == "escalate_doctrine_gap":
        data["escalates"] = True
    return create_validation_failure_route(**data)


def result(**kwargs):
    data = dict(
        validation_request_id="vreq-1",
        decision="validation_failed",
        final_stage="validation_failed",
        subject_type="command",
        subject_ref_id="cmd-1",
        request_subject_type="command",
        request_subject_ref_id="cmd-1",
        validation_result_ref_id="vres-1",
        dependencies=base_deps(),
        failure_routes=[route()],
        trace_id="trace-1",
    )
    data.update(kwargs)
    return create_validation_integration_result(**data)


def ready_result(**kwargs):
    data = dict(
        decision="validation_ready",
        final_stage="validation_integration_requested",
        validation_result_ref_id=None,
        dependencies=base_deps(result=None),
        failure_routes=[],
        passed=False,
        blocking=True,
        hidden_info_safe=True,
    )
    data.update(kwargs)
    return result(**data)


class TestSubjectRelationVocabulary:
    def test_constant_and_export(self):
        assert set(VALIDATION_SUBJECT_RELATIONS) == {
            "same_subject",
            "blocking_dependency",
            "affected_subject",
            "source_subject",
            "target_subject",
            "authority_source",
            "provenance_source",
        }
        assert domain.VALIDATION_SUBJECT_RELATIONS is VALIDATION_SUBJECT_RELATIONS

    def test_route_shape_and_public_sanitization(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            route(subject_relation="untyped")
        with pytest.raises(InvalidValidationFailureRouteError):
            route(subject_type="vehicle")
        with pytest.raises(InvalidValidationFailureRouteError):
            route(subject_ref_id="")
        r = route(player_visible=True, public_reason_code="validation_blocked")
        assert r.to_dict()["subject_type"] == "command"
        assert r.to_dict()["subject_relation"] == "same_subject"
        public = r.to_public_dict()
        for forbidden in {"subject_type", "subject_relation", "subject_ref_id", "route_id", "route_type", "decision", "metadata"}:
            assert forbidden not in public


class TestRouteResultSubjectRelationships:
    def test_same_subject_matching_accepted_and_mismatches_rejected(self):
        assert result().subject_ref_id == "cmd-1"
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(failure_routes=[route(subject_type="state_record")])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(failure_routes=[route(subject_ref_id="cmd-2")])
        manual = ValidationIntegrationResult(**{
            **result().to_dict(),
            "failure_routes": (route(subject_ref_id="cmd-2"),),
            "dependencies": base_deps(),
            "provenance_ref_ids": (),
            "metadata": MappingProxyType({}),
        })
        assert validate_validation_integration_result(manual) is False

    @pytest.mark.parametrize("relation", [
        "blocking_dependency",
        "affected_subject",
        "source_subject",
        "target_subject",
        "authority_source",
        "provenance_source",
    ])
    def test_explicit_cross_subject_routes_are_accepted(self, relation):
        r = route(subject_type="state_record", subject_ref_id=f"resource-{relation}", subject_relation=relation)
        assert result(failure_routes=[r]).failure_routes[0].subject_relation == relation

    def test_cross_subject_must_be_explicit_and_different(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(failure_routes=[route(subject_type="state_record", subject_ref_id="state-1")])
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(failure_routes=[route(subject_relation="blocking_dependency")])


class TestRequestSubjectBindingAndTypedDependencies:
    def test_request_subject_binding(self):
        assert result().request_subject_ref_id == "cmd-1"
        for kwargs in [
            {"request_subject_type": "state_record"},
            {"request_subject_ref_id": "cmd-2"},
            {"request_subject_type": "bad"},
            {"request_subject_ref_id": ""},
        ]:
            with pytest.raises(InvalidValidationIntegrationResultError):
                result(**kwargs)
        assert result().to_dict()["request_subject_type"] == "command"
        assert result().to_dict()["request_subject_ref_id"] == "cmd-1"
        manual = ValidationIntegrationResult(**{**result().to_dict(), "request_subject_ref_id": "cmd-2", "failure_routes": (route(),), "dependencies": base_deps(), "provenance_ref_ids": (), "metadata": MappingProxyType({})})
        assert validate_validation_integration_result(manual) is False

    @pytest.mark.parametrize("bad_deps", [
        (),
        (dep("dep-request", "validation_request_ref", "other"), dep("dep-trace", "runtime_trace_ref", "trace-1"), dep("dep-result", "validation_result_ref", "vres-1")),
        (dep("dep-request", "validation_request_ref", "vreq-1", satisfied=False), dep("dep-trace", "runtime_trace_ref", "trace-1"), dep("dep-result", "validation_result_ref", "vres-1")),
        (dep("dep-request", "validation_request_ref", "vreq-1", required=False), dep("dep-trace", "runtime_trace_ref", "trace-1"), dep("dep-result", "validation_result_ref", "vres-1")),
    ])
    def test_request_identity_dependency_required(self, bad_deps):
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(dependencies=bad_deps)

    def test_trace_and_validation_result_dependencies_required(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(dependencies=(dep("dep-request", "validation_request_ref", "vreq-1"), dep("dep-result", "validation_result_ref", "vres-1")))
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(dependencies=(dep("dep-request", "validation_request_ref", "vreq-1"), dep("dep-trace", "runtime_trace_ref", "wrong"), dep("dep-result", "validation_result_ref", "vres-1")))
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(dependencies=(dep("dep-request", "validation_request_ref", "vreq-1"), dep("dep-trace", "runtime_trace_ref", "trace-1")))
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(dependencies=(dep("dep-request", "validation_request_ref", "vreq-1"), dep("dep-trace", "runtime_trace_ref", "trace-1"), dep("dep-result", "validation_result_ref", "wrong")))
        assert ready_result().validation_result_ref_id is None
        with pytest.raises(InvalidValidationIntegrationResultError):
            ready_result(dependencies=base_deps(result="vres-1"))
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(validation_result_ref_id="")

    def test_request_trace_dependency(self):
        assert create_validation_integration_request(
            validation_request_id="vreq-1", subject_type="command", subject_ref_id="cmd-1", requesting_service="svc"
        )
        assert create_validation_integration_request(
            validation_request_id="vreq-1", subject_type="command", subject_ref_id="cmd-1", requesting_service="svc", trace_id="trace-1", dependencies=[dep("trace", "runtime_trace_ref", "trace-1")]
        )
        with pytest.raises(InvalidValidationIntegrationRequestError):
            create_validation_integration_request(
                validation_request_id="vreq-1", subject_type="command", subject_ref_id="cmd-1", requesting_service="svc", trace_id="trace-1", dependencies=[dep("trace", "runtime_trace_ref", "wrong")]
            )


class TestProvenanceAndUniqueness:
    def test_generated_content_provenance_exact_linkage(self):
        assert result(
            decision="validation_passed",
            final_stage="validation_passed",
            subject_type="generated_content",
            subject_ref_id="gen-1",
            request_subject_type="generated_content",
            request_subject_ref_id="gen-1",
            failure_routes=[],
            passed=True,
            blocking=False,
            provenance_checked=True,
            provenance_ref_ids=["prov-1"],
            dependencies=base_deps(provenance=("prov-1",)),
        )
        bad = dict(provenance_checked=True, provenance_ref_ids=["prov-1"], dependencies=base_deps())
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(**bad)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(provenance_checked=True, provenance_ref_ids=[], dependencies=base_deps(provenance=("prov-1",)))
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(provenance_checked=True, provenance_ref_ids=["prov-1", "prov-1"], dependencies=base_deps(provenance=("prov-1",)))
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(provenance_checked=True, provenance_ref_ids=["prov-1"], dependencies=(base_deps()[0], base_deps()[1], base_deps()[2], dep("prov", "generated_content_provenance_ref", "prov-1", satisfied=False)))
        assert "persistence_allowed" in result(provenance_checked=True, provenance_ref_ids=["prov-1"], dependencies=base_deps(provenance=("prov-1",))).to_dict()
        assert result(provenance_checked=True, provenance_ref_ids=["prov-1"], dependencies=base_deps(provenance=("prov-1",))).persistence_allowed is False

    def test_dependency_uniqueness_and_invalid_sequences(self):
        duplicate_id = (dep("same", "validation_request_ref", "vreq-1"), dep("same", "runtime_trace_ref", "trace-1"), dep("result", "validation_result_ref", "vres-1"))
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(dependencies=duplicate_id)
        duplicate_pair = (dep("request", "validation_request_ref", "vreq-1"), dep("request-2", "validation_request_ref", "vreq-1"), dep("trace", "runtime_trace_ref", "trace-1"), dep("result", "validation_result_ref", "vres-1"))
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(dependencies=duplicate_pair)
        with pytest.raises(InvalidValidationIntegrationResultError):
            result(dependencies="dep")
        assert validate_validation_integration_result(ValidationIntegrationResult(**{**result().to_dict(), "dependencies": duplicate_pair, "failure_routes": (route(),), "provenance_ref_ids": (), "metadata": MappingProxyType({})})) is False
        assert validate_validation_integration_request(ValidationIntegrationRequest(
            validation_request_id="vreq-1", subject_type="command", subject_ref_id="cmd-1", requesting_service="svc", dependencies=duplicate_pair, metadata=MappingProxyType({})
        )) is False


class TestReadyIntermediateParityAndNonExecution:
    def test_validation_ready_posture_and_routes(self):
        assert ready_result().blocking is True
        assert ready_result().passed is False
        with pytest.raises(InvalidValidationIntegrationResultError):
            ready_result(hidden_info_safe=False)
        ok_route = route(route_type="request_downstream_domain_validation", decision="validation_ready")
        assert ready_result(failure_routes=[ok_route])
        with pytest.raises(InvalidValidationIntegrationResultError):
            ready_result(failure_routes=[route()])

    def test_intermediate_stage_flag_consistency(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            ready_result(final_stage="provenance_checked", provenance_checked=False)
        assert ready_result(final_stage="provenance_checked", provenance_checked=True)
        with pytest.raises(InvalidValidationIntegrationResultError):
            ready_result(
                final_stage="provenance_checked",
                subject_type="generated_content",
                subject_ref_id="gen-1",
                request_subject_type="generated_content",
                request_subject_ref_id="gen-1",
                provenance_checked=True,
            )
        assert ready_result(
            final_stage="provenance_checked",
            subject_type="generated_content",
            subject_ref_id="gen-1",
            request_subject_type="generated_content",
            request_subject_ref_id="gen-1",
            provenance_checked=True,
            provenance_ref_ids=["prov-1"],
            dependencies=base_deps(result=None, provenance=("prov-1",)),
        )
        with pytest.raises(InvalidValidationIntegrationResultError):
            ready_result(final_stage="hidden_info_safety_checked", hidden_info_safe=False)
        assert ready_result(final_stage="hidden_info_safety_checked", hidden_info_safe=True)
        with pytest.raises(InvalidValidationIntegrationResultError):
            ready_result(final_stage="invariant_precheck_passed")
        assert ready_result(final_stage="invariant_precheck_passed", invariant_precheck_ref_id="precheck-1")

    def test_manual_invalid_parity(self):
        assert validate_validation_failure_route(ValidationFailureRoute(route_id="r", route_type="block_command_before_transaction", decision="validation_failed", subject_ref_id="cmd-1", subject_relation="bad")) is False
        assert validate_validation_integration_result(ValidationIntegrationResult(**{**result().to_dict(), "failure_routes": (route(subject_ref_id="cmd-2"),), "dependencies": base_deps(), "provenance_ref_ids": (), "metadata": MappingProxyType({})})) is False
        assert validate_validation_integration_result(ValidationIntegrationResult(**{**ready_result().to_dict(), "hidden_info_safe": False, "dependencies": base_deps(result=None), "failure_routes": (), "provenance_ref_ids": (), "metadata": MappingProxyType({})})) is False

    def test_non_execution_guardrails_remain_absent(self):
        source = DOMAIN_FILE.read_text()
        forbidden = [
            "run_validation_checks", "run_invariant_prechecks", "apply_delta", "append_event", "persist(",
            "replay(", "execute_command", "calculate", "spend", "prompt", "narrate", "random", "table_oracle",
        ]
        assert all(term not in source for term in forbidden)
        assert "state_mutation_allowed must be False" in source
        assert "event_append_allowed must be False" in source
        assert "persistence_allowed must be False" in source
        assert "model_authority_allowed must be False" in source
