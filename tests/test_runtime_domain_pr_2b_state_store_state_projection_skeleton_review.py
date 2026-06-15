"""Tests for RUNTIME-DOMAIN-PR-2B state store / state projection skeleton review gate."""

from __future__ import annotations

import os

import pytest


REVIEW_PATH = "docs/doctrine/reviews/runtime_domain_pr_2b_state_store_state_projection_skeleton_review.md"
REGISTRY_PATH = "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = "docs/decisions/current_decisions_log.md"


@pytest.fixture(scope="module")
def review_content():
    with open(REVIEW_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def registry_content():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def decision_log_content():
    with open(DECISION_LOG_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestReviewFileExists:
    def test_review_file_exists(self):
        assert os.path.isfile(REVIEW_PATH), f"Review file not found: {REVIEW_PATH}"


class TestReviewReferences:
    def test_references_pr_2b_id(self, review_content):
        assert "RUNTIME-DOMAIN-PR-2B" in review_content

    def test_references_pr_2a(self, review_content):
        assert "RUNTIME-DOMAIN-PR-2A" in review_content

    def test_references_pr_2_plan(self, review_content):
        assert "RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001" in review_content

    def test_references_pr_1b(self, review_content):
        assert "RUNTIME-DOMAIN-PR-1B" in review_content

    def test_references_state_store_py(self, review_content):
        assert "state_store.py" in review_content

    def test_references_state_projection_py(self, review_content):
        assert "state_projection.py" in review_content

    def test_references_validate_state_record_ref(self, review_content):
        assert "validate_state_record_ref" in review_content

    def test_references_validate_state_projection_request(self, review_content):
        assert "validate_state_projection_request" in review_content


class TestBackendFirstInvariant:
    def test_states_model_interchangeability(self, review_content):
        assert "model-interchangeable" in review_content

    def test_states_llm_not_game_engine(self, review_content):
        assert "LLM is not the game engine" in review_content

    def test_states_backend_owns_truth(self, review_content):
        assert "backend runtime kernel owns truth" in review_content


class TestReviewSections:
    def test_includes_pr_2a_implementation_review(self, review_content):
        assert "## 4. PR-2A implementation review" in review_content

    def test_includes_state_store_skeleton_review(self, review_content):
        assert "## 5. State store skeleton review" in review_content

    def test_includes_state_projection_skeleton_review(self, review_content):
        assert "## 6. State projection skeleton review" in review_content

    def test_includes_validator_parity_review(self, review_content):
        assert "## 7. Validator parity review" in review_content

    def test_includes_guardrail_transition_review(self, review_content):
        assert "## 8. Guardrail transition review" in review_content

    def test_includes_kernel_dependency_review(self, review_content):
        assert "## 9. Kernel dependency review" in review_content

    def test_includes_corpus_scale_pressure_review(self, review_content):
        assert "## 10. Corpus-scale state/projection pressure review" in review_content

    def test_includes_risk_review(self, review_content):
        assert "## 11. Risk review" in review_content

    def test_includes_hardening_ledger(self, review_content):
        assert "## 12. Required future hardening ledger" in review_content

    def test_includes_gate_finding(self, review_content):
        assert "## 13. Gate finding" in review_content

    def test_includes_recommended_next_pr(self, review_content):
        assert "## 14. Recommended next PR" in review_content

    def test_includes_non_implementation_reaffirmation(self, review_content):
        assert "## 15. Non-implementation reaffirmation" in review_content

    def test_includes_classification_block(self, review_content):
        assert "## 16. Classification block" in review_content


class TestGateFinding:
    def test_gate_finding_review_complete(self, review_content):
        assert "state_store_state_projection_skeleton_review_complete: true" in review_content

    def test_gate_finding_pr_2a_confirmed(self, review_content):
        assert "pr_2a_scope_confirmed: true" in review_content

    def test_gate_finding_guardrail_safe(self, review_content):
        assert "guardrail_transition_safe: true" in review_content

    def test_gate_finding_validator_acceptable(self, review_content):
        assert "validator_surface_acceptable_for_later_services: true" in review_content

    def test_gate_finding_ready_for_pr3(self, review_content):
        assert "ready_for_runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan: true" in review_content

    def test_gate_finding_no_pr2c_required(self, review_content):
        assert "requires_pr_2c_hardening_before_pr_3: false" in review_content

    def test_gate_finding_no_code_authorized(self, review_content):
        assert "domain_code_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_mutable_state(self, review_content):
        assert "mutable_runtime_state_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_state_mutation(self, review_content):
        assert "state_mutation_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_transaction_lifecycle(self, review_content):
        assert "transaction_lifecycle_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_event_commitment(self, review_content):
        assert "event_commitment_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_model_integration(self, review_content):
        assert "model_integration_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_live_play(self, review_content):
        assert "live_play_authorized_by_this_pr: false" in review_content

    def test_gate_finding_next_step(self, review_content):
        assert "next_step_authorized: RUNTIME-DOMAIN-PR-3 transaction lifecycle and event commitment service plan" in review_content


class TestClassificationBlock:
    def test_review_id(self, review_content):
        assert "review_id: RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001" in review_content

    def test_artifact_type(self, review_content):
        assert "artifact_type: state_store_state_projection_skeleton_review_gate" in review_content

    def test_non_executable(self, review_content):
        assert "implementation_status: non_executable_review_gate" in review_content

    def test_derives_from_pr_2a(self, review_content):
        assert "RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001" in review_content

    def test_reviews_state_store(self, review_content):
        assert "reviews_state_store_skeleton: true" in review_content

    def test_reviews_state_projection(self, review_content):
        assert "reviews_state_projection_skeleton: true" in review_content

    def test_reviews_validator_parity(self, review_content):
        assert "reviews_validator_parity: true" in review_content

    def test_reviews_guardrail_transition(self, review_content):
        assert "reviews_guardrail_transition: true" in review_content

    def test_reviews_kernel_dependency(self, review_content):
        assert "reviews_kernel_dependency_usage: true" in review_content

    def test_reviews_corpus_scale(self, review_content):
        assert "reviews_corpus_scale_state_pressure: true" in review_content

    def test_defines_hardening_ledger(self, review_content):
        assert "defines_future_hardening_ledger: true" in review_content

    def test_no_code_authorized(self, review_content):
        assert "authorizes_code_by_this_pr: false" in review_content


class TestNonImplementationGuardrails:
    """Verify the review does not claim to implement prohibited items."""

    PROHIBITED_CLAIMS = [
        "implements mutable runtime state",
        "implements state mutation",
        "implements state delta application",
        "implements transaction lifecycle",
        "implements event commitment",
        "implements event sourcing",
        "implements durable persistence",
        "implements database schema",
        "implements replay engine",
        "implements command execution",
        "implements command parser",
        "implements action legality expansion",
        "implements resource math",
        "implements combat resolution",
        "implements ability resolution",
        "implements inventory mutation",
        "implements mission mutation",
        "implements social mutation",
        "implements context-packet compiler",
        "implements prompt templates",
        "implements model integration",
        "implements live-play adapter",
        "implements UI/client",
        "implements training data",
        "implements conversion",
        "implements sourcebook inclusion",
        "implements canon promotion",
    ]

    @pytest.mark.parametrize("claim", PROHIBITED_CLAIMS)
    def test_no_prohibited_implementation_claim(self, review_content, claim):
        assert claim not in review_content


class TestRegistryTracking:
    def test_pr2b_file_id_appears(self, registry_content):
        assert "RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001" in registry_content

    def test_pr2b_changelog_version(self, registry_content):
        assert "version: 0.1.72" in registry_content


class TestDecisionLogTracking:
    def test_pr2b_id_appears(self, decision_log_content):
        assert "RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001" in decision_log_content


class TestRuntimeGuardrailsDomainPackage:
    """Verify domain package contains only authorized files."""

    def test_domain_package_exists(self):
        assert os.path.isdir("src/astra_runtime/domain")

    def test_domain_package_contains_only_authorized_files(self):
        domain_dir = "src/astra_runtime/domain"
        authorized = {
            "__init__.py",
            "command_lifecycle.py",
            "action_legality.py",
            "state_store.py",
            "state_projection.py",
            "transaction_lifecycle.py",
            "event_commitment.py",
            "validation_integration.py",
            "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py", "scene_command_execution_skeleton.py", "command_kind_routing_skeleton.py",
            "__pycache__",
        }
        entries = set(os.listdir(domain_dir))
        unauthorized = entries - authorized
        assert not unauthorized, f"Unauthorized domain files found: {unauthorized}"

    def test_transaction_lifecycle_authorized(self):
        assert os.path.exists("src/astra_runtime/domain/transaction_lifecycle.py")

    def test_event_commitment_authorized(self):
        assert os.path.exists("src/astra_runtime/domain/event_commitment.py")

    def test_validation_integration_authorized(self):
        assert os.path.exists("src/astra_runtime/domain/validation_integration.py")

    def test_no_resource_math(self):
        assert not os.path.exists("src/astra_runtime/domain/resource_math.py")

    def test_no_combat(self):
        assert not os.path.exists("src/astra_runtime/domain/combat.py")

    def test_no_ability_effects(self):
        assert not os.path.exists("src/astra_runtime/domain/ability_effects.py")

    def test_no_inventory(self):
        assert not os.path.exists("src/astra_runtime/domain/inventory.py")

    def test_no_mission(self):
        assert not os.path.exists("src/astra_runtime/domain/mission.py")

    def test_no_social_faction(self):
        assert not os.path.exists("src/astra_runtime/domain/social_faction.py")

    def test_no_generated_content(self):
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

    def test_no_database_package(self):
        assert not os.path.exists("src/astra_runtime/database")

    def test_no_store_package(self):
        assert not os.path.exists("src/astra_runtime/store")
