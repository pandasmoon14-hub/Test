"""Tests for RUNTIME-DOMAIN-PR-4 validation integration and invariant enforcement service plan."""

from tests.runtime_domain_package_manifest import (
    AUTHORIZED_RUNTIME_DOMAIN_ENTRIES,
    AUTHORIZED_RUNTIME_DOMAIN_FILES,
)

import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

PLAN_PATH = (
    REPO_ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_domain_pr_4_validation_integration_invariant_enforcement_service_plan.md"
)

REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"

DOMAIN_PACKAGE_DIR = REPO_ROOT / "src" / "astra_runtime" / "domain"
KERNEL_PACKAGE_DIR = REPO_ROOT / "src" / "astra_runtime" / "kernel"


@pytest.fixture(scope="module")
def plan_text() -> str:
    return PLAN_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def registry_text() -> str:
    return REGISTRY_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_log_text() -> str:
    return DECISION_LOG_PATH.read_text(encoding="utf-8")


# ── Section 1: Plan file exists ──────────────────────────────────────────────

class TestPlanFileExists:
    def test_plan_file_exists(self):
        assert PLAN_PATH.exists(), f"Plan file not found at {PLAN_PATH}"

    def test_plan_file_nonempty(self, plan_text):
        assert len(plan_text.strip()) > 0


# ── Section 2: ID and lineage references ─────────────────────────────────────

class TestIDReferences:
    def test_references_pr_4_full_id(self, plan_text):
        assert (
            "RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001"
            in plan_text
        )

    def test_references_pr_3b_full_id(self, plan_text):
        assert (
            "RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001"
            in plan_text
        )

    def test_references_pr_3a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-3A" in plan_text

    def test_references_pr_3(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-3" in plan_text

    def test_references_pr_2b(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-2B" in plan_text

    def test_references_pr_2a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-2A" in plan_text

    def test_references_pr_1b(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-1B" in plan_text

    def test_references_pr_1a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-1A" in plan_text

    def test_references_pr_0(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-0" in plan_text


# ── Section 3: Kernel module references ──────────────────────────────────────

class TestKernelModuleReferences:
    @pytest.mark.parametrize(
        "module_name",
        [
            "schema_registry",
            "record_identity",
            "command_envelope",
            "transaction_preview",
            "state_delta",
            "event_ledger",
            "rng_interface",
            "table_oracle",
            "validation_pipeline",
            "hidden_information",
            "context_projection",
            "persistence_boundary",
            "replay_audit",
            "runtime_trace",
        ],
    )
    def test_references_kernel_module(self, plan_text, module_name):
        assert module_name in plan_text, f"Plan must reference kernel module {module_name}"


# ── Section 4: Domain module references ──────────────────────────────────────

class TestDomainModuleReferences:
    @pytest.mark.parametrize(
        "module_ref",
        [
            "command_lifecycle.py",
            "action_legality.py",
            "state_store.py",
            "state_projection.py",
            "transaction_lifecycle.py",
            "event_commitment.py",
        ],
    )
    def test_references_domain_module(self, plan_text, module_ref):
        assert module_ref in plan_text, f"Plan must reference domain module {module_ref}"


# ── Section 5: Backend-first invariant ───────────────────────────────────────

class TestBackendFirstInvariant:
    def test_states_llm_not_game_engine(self, plan_text):
        assert "LLM is not the game engine" in plan_text

    def test_states_backend_owns_truth(self, plan_text):
        assert "backend owns truth" in plan_text.lower()

    def test_states_validation_backend_owned(self, plan_text):
        assert "backend-owned authority layer" in plan_text

    def test_states_no_self_validation_override(self, plan_text):
        lower = plan_text.lower()
        assert "cannot validate themselves" in lower or "can never validate themselves" in lower


# ── Section 6: Service ownership ─────────────────────────────────────────────

class TestServiceOwnership:
    def test_includes_service_ownership_heading(self, plan_text):
        assert "Service ownership" in plan_text or "service ownership" in plan_text

    def test_includes_primary_ownership(self, plan_text):
        assert "Primary ownership" in plan_text

    def test_includes_validation_integration_surface(self, plan_text):
        assert "validation integration surface" in plan_text.lower()

    def test_includes_invariant_declaration_routing(self, plan_text):
        assert "invariant declaration routing" in plan_text.lower()

    def test_includes_explicit_non_ownership(self, plan_text):
        assert "non-ownership" in plan_text.lower()


# ── Section 7: Validation integration model ──────────────────────────────────

class TestValidationIntegrationModel:
    def test_includes_model_heading(self, plan_text):
        assert "Validation integration model" in plan_text

    @pytest.mark.parametrize(
        "stage",
        [
            "validation_integration_requested",
            "validation_scope_declared",
            "dependency_refs_bound",
            "state_refs_bound",
            "transaction_refs_bound",
            "event_commitment_refs_bound",
            "invariant_set_declared",
            "invariant_precheck_requested",
            "invariant_precheck_passed",
            "invariant_precheck_failed",
            "domain_validation_required",
            "domain_validation_referenced",
            "hidden_info_safety_checked",
            "provenance_checked",
            "validation_passed",
            "validation_failed",
            "validation_quarantined",
            "validation_escalated",
            "validation_cancelled",
            "validation_superseded",
        ],
    )
    def test_includes_integration_stage(self, plan_text, stage):
        assert stage in plan_text, f"Validation integration model must include stage {stage}"


# ── Section 8: Validation decision model ─────────────────────────────────────

class TestValidationDecisionModel:
    def test_includes_decision_model_heading(self, plan_text):
        assert "Validation decision model" in plan_text

    @pytest.mark.parametrize(
        "decision",
        [
            "validation_ready",
            "validation_passed",
            "validation_failed",
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
            "quarantined_for_review",
            "escalated_to_doctrine",
            "unsupported_validation_scope",
        ],
    )
    def test_includes_validation_decision(self, plan_text, decision):
        assert decision in plan_text, f"Validation decision model must include {decision}"


# ── Section 9: Invariant family model ────────────────────────────────────────

class TestInvariantFamilyModel:
    def test_includes_family_model_heading(self, plan_text):
        assert "Invariant family model" in plan_text

    @pytest.mark.parametrize(
        "family",
        [
            "command_authority_invariant",
            "action_legality_invariant",
            "state_reference_invariant",
            "state_projection_visibility_invariant",
            "transaction_lifecycle_invariant",
            "event_commitment_invariant",
            "state_delta_shape_invariant",
            "event_ledger_shape_invariant",
            "validation_result_authority_invariant",
            "hidden_information_partition_invariant",
            "context_projection_visibility_invariant",
            "persistence_boundary_invariant",
            "replay_audit_invariant",
            "runtime_trace_invariant",
            "schema_record_shape_invariant",
            "source_local_authority_invariant",
            "generated_content_provenance_invariant",
            "canon_boundary_invariant",
            "conversion_boundary_invariant",
            "model_non_authority_invariant",
            "live_play_non_authority_invariant",
        ],
    )
    def test_includes_invariant_family(self, plan_text, family):
        assert family in plan_text, f"Invariant family model must include {family}"


# ── Section 10: Kernel interface consumption plan ────────────────────────────

class TestKernelInterfaceConsumptionPlan:
    def test_includes_kernel_consumption_heading(self, plan_text):
        assert "Kernel interface consumption plan" in plan_text

    def test_validation_pipeline_primary(self, plan_text):
        assert "primary dependency" in plan_text.lower()

    def test_no_delta_application(self, plan_text):
        assert "Must not apply deltas" in plan_text

    def test_no_ledger_append(self, plan_text):
        assert "Must not append to any ledger" in plan_text


# ── Section 11: Domain service handoff boundaries ────────────────────────────

class TestDomainServiceHandoffBoundaries:
    def test_includes_handoff_heading(self, plan_text):
        assert "Domain service handoff boundaries" in plan_text

    @pytest.mark.parametrize(
        "service_ref",
        [
            "command_lifecycle",
            "action_legality",
            "state_store",
            "state_projection",
            "transaction_lifecycle",
            "event_commitment",
            "resource / consequence math",
            "combat / hazard / damage / recovery",
            "ability / effect / skill binding",
            "inventory / item / vehicle / asset",
            "mission / reward / clue routing",
            "social / faction / actor knowledge",
            "generated-content provenance",
            "context-packet compiler",
            "model evaluation harness",
            "live-play adapter",
        ],
    )
    def test_references_handoff_service(self, plan_text, service_ref):
        assert service_ref.lower() in plan_text.lower(), (
            f"Handoff section must reference {service_ref}"
        )


# ── Section 12: Validation failure routing ───────────────────────────────────

class TestValidationFailureRouting:
    def test_includes_failure_routing_heading(self, plan_text):
        assert "Validation failure routing" in plan_text

    @pytest.mark.parametrize(
        "route",
        [
            "block_command_before_transaction",
            "block_transaction_before_commitment",
            "block_event_commitment",
            "quarantine_transaction",
            "quarantine_event_commitment",
            "quarantine_generated_content",
            "escalate_doctrine_gap",
            "reject_source_local_authority",
            "reject_hidden_info_leak",
            "reject_schema_mismatch",
            "reject_phase_boundary_violation",
            "request_downstream_domain_validation",
        ],
    )
    def test_includes_failure_route(self, plan_text, route):
        assert route in plan_text, f"Failure routing must include {route}"


# ── Section 13: Hidden-information and provenance safety ─────────────────────

class TestHiddenInformationAndProvenanceSafety:
    def test_includes_safety_heading(self, plan_text):
        assert "Hidden-information and provenance safety" in plan_text

    def test_internal_reference_no_exposure(self, plan_text):
        assert (
            "may reference hidden information internally but must not expose hidden values"
            in plan_text.lower()
        )

    def test_generated_content_provenance_rule(self, plan_text):
        assert (
            "must not become durable or authoritative without provenance validation"
            in plan_text.lower()
        )

    def test_source_local_canon_rule(self, plan_text):
        assert (
            "must not become canon by passing runtime validation" in plan_text.lower()
        )

    @pytest.mark.parametrize(
        "info_class",
        [
            "Backend-hidden information",
            "GM-visible information",
            "Actor-visible information",
            "Player-visible information",
            "Model-facing projections",
            "UI/client projections",
            "Generated content",
            "Source-local converted content",
            "Canon sourcebook content",
            "Donor assumptions",
        ],
    )
    def test_includes_information_class(self, plan_text, info_class):
        assert info_class in plan_text, f"Safety section must address {info_class}"


# ── Section 14: Future implementation architecture ───────────────────────────

class TestFutureImplementationArchitecture:
    def test_includes_implementation_architecture(self, plan_text):
        assert "Future implementation architecture" in plan_text

    def test_references_validation_integration_py(self, plan_text):
        assert "src/astra_runtime/domain/validation_integration.py" in plan_text

    @pytest.mark.parametrize(
        "symbol",
        [
            "VALIDATION_INTEGRATION_STAGES",
            "VALIDATION_INTEGRATION_DECISIONS",
            "VALIDATION_INVARIANT_FAMILIES",
            "VALIDATION_FAILURE_ROUTES",
            "ValidationIntegrationError",
            "InvalidValidationIntegrationDependencyError",
            "InvalidValidationInvariantDeclarationError",
            "InvalidValidationIntegrationRequestError",
            "InvalidValidationIntegrationResultError",
            "InvalidValidationFailureRouteError",
            "ValidationIntegrationDependency",
            "ValidationInvariantDeclaration",
            "ValidationIntegrationRequest",
            "ValidationIntegrationResult",
            "ValidationFailureRoute",
            "ValidationIntegrationService",
            "create_validation_integration_dependency",
            "create_validation_invariant_declaration",
            "create_validation_integration_request",
            "create_validation_integration_result",
            "create_validation_failure_route",
            "validate_validation_integration_dependency",
            "validate_validation_invariant_declaration",
            "validate_validation_integration_request",
            "validate_validation_integration_result",
            "validate_validation_failure_route",
        ],
    )
    def test_includes_proposed_symbol(self, plan_text, symbol):
        assert symbol in plan_text, f"Architecture must propose symbol {symbol}"

    def test_proposed_symbols_not_created(self, plan_text):
        assert "must not be created in PR-4" in plan_text


# ── Section 15: Future data shapes ───────────────────────────────────────────

class TestFutureDataShapes:
    def test_includes_data_shapes_heading(self, plan_text):
        assert "Future data shapes" in plan_text


# ── Section 16: Commit-readiness validation invariants ───────────────────────

class TestCommitReadinessValidationInvariants:
    def test_includes_invariants_heading(self, plan_text):
        assert "Commit-readiness validation invariants" in plan_text

    @pytest.mark.parametrize(
        "invariant_keyword",
        [
            "No event commitment without validation reference",
            "No validation pass from model text",
            "No validation pass from narration",
            "No validation pass from UI text",
            "No validation pass from donor assumptions",
            "No state mutation from validation result",
            "No event append from validation result",
            "No persistence write from validation result",
            "No replay from validation result",
            "deterministic and replay-auditable",
        ],
    )
    def test_includes_invariant(self, plan_text, invariant_keyword):
        assert invariant_keyword in plan_text, (
            f"Commit-readiness invariants must include: {invariant_keyword}"
        )


# ── Section 17: Corpus-scale validation pressure review ──────────────────────

class TestCorpusScaleValidationPressureReview:
    def test_includes_corpus_scale_heading(self, plan_text):
        assert "Corpus-scale validation pressure review" in plan_text

    @pytest.mark.parametrize(
        "pressure_category",
        [
            "player actions",
            "Interrupts",
            "Combat",
            "Resources",
            "Abilities",
            "Skills",
            "Inventory",
            "Vehicles",
            "faction",
            "Missions",
            "Companions",
            "Crafting",
            "Hazards",
            "Downtime",
            "Generated content",
            "hidden information",
            "oracle",
            "Source-local constructs",
            "Cross-book converted content",
            "sourcebook references",
        ],
    )
    def test_includes_pressure_category(self, plan_text, pressure_category):
        assert pressure_category.lower() in plan_text.lower(), (
            f"Pressure review must address: {pressure_category}"
        )


# ── Section 18: Risk review ──────────────────────────────────────────────────

class TestRiskReview:
    def test_includes_risk_review(self, plan_text):
        assert "Risk review" in plan_text

    @pytest.mark.parametrize(
        "risk_keyword",
        [
            "universal rule engine",
            "bypasses transaction lifecycle",
            "mutates state directly",
            "appends events directly",
            "donor-rule importer",
            "Model text becomes validation authority",
            "durable without provenance",
            "under-modeled schemas",
            "too-broad schemas",
            "Persistence implemented too early",
            "Context-packet compiler built too early",
        ],
    )
    def test_includes_risk_category(self, plan_text, risk_keyword):
        assert risk_keyword.lower() in plan_text.lower(), (
            f"Risk review must address: {risk_keyword}"
        )


# ── Section 19: Required hardening ledger ────────────────────────────────────

class TestRequiredHardeningLedger:
    def test_includes_hardening_ledger(self, plan_text):
        assert "hardening ledger" in plan_text.lower()

    @pytest.mark.parametrize(
        "ledger_item",
        [
            "Invariant family completeness",
            "Hidden-info summary safety",
            "Generated-content provenance validation",
            "Schema mismatch handling",
            "Authority mismatch handling",
            "Phase-boundary validation",
            "Validator parity with factories",
            "No-model-authority tests",
            "No-state-mutation tests",
            "No-event-append tests",
            "No-persistence tests",
            "No-universal-rule-engine tests",
        ],
    )
    def test_includes_ledger_item(self, plan_text, ledger_item):
        assert ledger_item in plan_text, f"Hardening ledger must include: {ledger_item}"


# ── Section 20: Implementation PR authorization boundary ─────────────────────

class TestImplementationPRAuthorizationBoundary:
    def test_includes_authorization_boundary(self, plan_text):
        assert "Implementation PR authorization boundary" in plan_text

    def test_recommends_pr_4a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-4A" in plan_text

    def test_pr_4a_allowed_file(self, plan_text):
        assert "validation_integration.py" in plan_text


# ── Section 21: Future implementation test requirements ──────────────────────

class TestFutureImplementationTestRequirements:
    def test_includes_test_requirements_heading(self, plan_text):
        assert "test requirements" in plan_text.lower()


# ── Section 22: Gate finding ─────────────────────────────────────────────────

class TestGateFinding:
    def test_includes_gate_finding(self, plan_text):
        assert "gate_finding" in plan_text

    @pytest.mark.parametrize(
        "gate_field",
        [
            "validation_integration_invariant_enforcement_plan_defined: true",
            "ready_for_validation_integration_skeleton_implementation_pr: true",
            "requires_pr_4b_hardening_before_pr_4a: false",
            "validation_integration_code_authorized_by_this_pr: false",
            "invariant_enforcement_code_authorized_by_this_pr: false",
            "domain_validation_rules_authorized_by_this_pr: false",
            "runtime_code_authorized_by_this_pr: false",
            "domain_code_authorized_by_this_pr: false",
            "transaction_execution_authorized_by_this_pr: false",
            "actual_event_commitment_authorized_by_this_pr: false",
            "event_sourcing_authorized_by_this_pr: false",
            "mutable_runtime_state_authorized_by_this_pr: false",
            "state_mutation_authorized_by_this_pr: false",
            "state_delta_application_authorized_by_this_pr: false",
            "event_ledger_append_authorized_by_this_pr: false",
            "durable_persistence_authorized_by_this_pr: false",
            "replay_engine_authorized_by_this_pr: false",
            "command_execution_authorized_by_this_pr: false",
            "command_parser_authorized_by_this_pr: false",
            "resource_math_authorized_by_this_pr: false",
            "combat_resolution_authorized_by_this_pr: false",
            "ability_resolution_authorized_by_this_pr: false",
            "inventory_mutation_authorized_by_this_pr: false",
            "mission_mutation_authorized_by_this_pr: false",
            "social_faction_mutation_authorized_by_this_pr: false",
            "generated_content_persistence_authorized_by_this_pr: false",
            "context_packet_compiler_authorized_by_this_pr: false",
            "prompt_templates_authorized_by_this_pr: false",
            "model_integration_authorized_by_this_pr: false",
            "live_play_authorized_by_this_pr: false",
            "ui_client_authorized_by_this_pr: false",
            "conversion_authorized_by_this_pr: false",
            "canon_promotion_authorized_by_this_pr: false",
            "next_step_status: narrow_skeleton_implementation_pending_review",
        ],
    )
    def test_gate_field_present(self, plan_text, gate_field):
        assert gate_field in plan_text, f"Gate finding must include: {gate_field}"


# ── Section 23: Recommended next PR ──────────────────────────────────────────

class TestRecommendedNextPR:
    def test_includes_recommended_next_pr(self, plan_text):
        assert "Recommended next PR" in plan_text

    def test_recommends_pr_4a_skeleton(self, plan_text):
        assert (
            "RUNTIME-DOMAIN-PR-4A: Validation Integration and Invariant Enforcement "
            "Skeleton Implementation" in plan_text
        )


# ── Section 24: Non-implementation reaffirmation ─────────────────────────────

class TestNonImplementationReaffirmation:
    def test_includes_non_implementation_reaffirmation(self, plan_text):
        assert "Non-implementation reaffirmation" in plan_text


# ── Section 25: No-implementation claims ─────────────────────────────────────

class TestNoImplementationClaims:
    @pytest.mark.parametrize(
        "forbidden_claim",
        [
            "implements validation integration code",
            "implements invariant enforcement code",
            "implements domain validation rules",
            "implements executable validators",
            "implements transaction execution",
            "implements event commitment code",
            "implements state mutation",
            "implements delta application",
            "implements event ledger append",
            "implements durable persistence",
            "implements replay engine",
            "implements command execution",
            "implements resource math",
            "implements combat resolution",
            "implements ability resolution",
            "implements inventory mutation",
            "implements context-packet compiler",
            "implements prompt templates",
            "implements model integration",
            "implements live play",
            "implements canon promotion",
        ],
    )
    def test_plan_does_not_claim_implementation(self, plan_text, forbidden_claim):
        assert forbidden_claim not in plan_text.lower(), (
            f"Plan must not claim: {forbidden_claim}"
        )


# ── Section 26: Classification block ─────────────────────────────────────────

class TestClassificationBlock:
    def test_includes_classification_block(self, plan_text):
        assert "runtime_domain_pr_4:" in plan_text

    def test_classification_artifact_type(self, plan_text):
        assert "validation_integration_invariant_enforcement_service_plan" in plan_text

    def test_classification_non_executable(self, plan_text):
        assert "non_executable_plan" in plan_text

    @pytest.mark.parametrize(
        "field_value",
        [
            "defines_validation_integration_model: true",
            "defines_invariant_enforcement_model: true",
            "defines_validation_decision_model: true",
            "defines_invariant_family_model: true",
            "defines_validation_failure_routing: true",
            "defines_hidden_information_validation_safety: true",
            "defines_generated_content_provenance_validation: true",
            "defines_kernel_interface_consumption_plan: true",
            "defines_domain_service_handoff_boundaries: true",
            "defines_future_implementation_architecture: true",
            "defines_future_data_shapes: true",
            "defines_corpus_scale_validation_pressure_review: true",
            "defines_future_hardening_ledger: true",
            "authorizes_validation_integration_code_by_this_pr: false",
            "authorizes_invariant_enforcement_code_by_this_pr: false",
            "authorizes_domain_validation_rules_by_this_pr: false",
            "authorizes_runtime_code_by_this_pr: false",
            "authorizes_domain_code_by_this_pr: false",
            "authorizes_state_mutation_by_this_pr: false",
            "authorizes_event_ledger_append_by_this_pr: false",
            "authorizes_model_integration_by_this_pr: false",
            "authorizes_canon_promotion_by_this_pr: false",
        ],
    )
    def test_classification_field(self, plan_text, field_value):
        assert field_value in plan_text, f"Classification must include: {field_value}"

    @pytest.mark.parametrize(
        "derived_id",
        [
            "RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001",
            "RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001",
            "RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001",
            "RT-001",
            "RT-005",
            "RT-008",
            "RT-011",
        ],
    )
    def test_classification_derives_from(self, plan_text, derived_id):
        assert derived_id in plan_text, f"Classification must derive from: {derived_id}"


# ── Section 27: Registry tracking ────────────────────────────────────────────

class TestRegistryTracking:
    def test_registry_has_pr4_file_id(self, registry_text):
        assert (
            "file_id: RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001"
            in registry_text
        )

    def test_registry_pr4_file_id_unique(self, registry_text):
        count = registry_text.count(
            "file_id: RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001"
        )
        assert count == 1, f"Expected file_id exactly once, found {count} times"

    def test_registry_pr4_denies_validation_integration_code(self, registry_text):
        assert "authorizes_validation_integration_code_by_this_pr: false" in registry_text

    def test_registry_pr4_denies_invariant_enforcement_code(self, registry_text):
        assert "authorizes_invariant_enforcement_code_by_this_pr: false" in registry_text

    def test_registry_pr4_denies_domain_validation_rules(self, registry_text):
        assert "authorizes_domain_validation_rules_by_this_pr: false" in registry_text

    def test_registry_pr4_next_allowed_step(self, registry_text):
        assert (
            "next_allowed_step: RUNTIME-DOMAIN-PR-4A validation integration and invariant "
            "enforcement skeleton implementation, pending review" in registry_text
        )


# ── Section 28: Decision log tracking ────────────────────────────────────────

class TestDecisionLogTracking:
    def test_decision_log_references_pr_4(self, decision_log_text):
        assert (
            "RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001"
            in decision_log_text
        )

    def test_decision_log_states_planning_only(self, decision_log_text):
        assert "Planning-only validation integration" in decision_log_text

    def test_decision_log_authorizes_only_pr_4a(self, decision_log_text):
        assert "RUNTIME-DOMAIN-PR-4A" in decision_log_text


# ── Section 29: Runtime guardrail tests — domain package contents ────────────

class TestDomainPackageGuardrails:
    def test_domain_package_exists(self):
        assert DOMAIN_PACKAGE_DIR.exists(), "Domain package must exist"

    def test_domain_package_authorized_files_only(self):
        allowed = set(AUTHORIZED_RUNTIME_DOMAIN_ENTRIES)
        actual = {p.name for p in DOMAIN_PACKAGE_DIR.iterdir()}
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized files in domain package: {unauthorized}"

    @pytest.mark.parametrize(
        "forbidden_file",
        [
            "invariant_enforcement.py",
            "resource_math.py",
            "combat.py",
            "ability_effects.py",
            "inventory.py",
            "mission.py",
            "social_faction.py",
            "generated_content.py",
        ],
    )
    def test_no_unauthorized_domain_module(self, forbidden_file):
        assert not (DOMAIN_PACKAGE_DIR / forbidden_file).exists(), (
            f"Unauthorized domain module must not exist: {forbidden_file}"
        )


class TestNoUnauthorizedPackages:
    @pytest.mark.parametrize(
        "forbidden_path",
        [
            "src/astra_runtime/kernel/context_packet_compiler.py",
            "src/astra_runtime/model",
            "src/astra_runtime/prompts",
            "src/astra_runtime/live_play",
            "src/astra_runtime/ui",
            "src/astra_runtime/database",
            "src/astra_runtime/store",
        ],
    )
    def test_no_unauthorized_package(self, forbidden_path):
        full_path = REPO_ROOT / forbidden_path
        assert not full_path.exists(), (
            f"Unauthorized path must not exist: {forbidden_path}"
        )
