"""Tests for RUNTIME-DOMAIN-PR-1B command lifecycle/action legality skeleton review."""

import os

import pytest


REVIEW_PATH = os.path.join(
    "docs", "doctrine", "reviews",
    "runtime_domain_pr_1b_command_lifecycle_action_legality_skeleton_review.md",
)
REGISTRY_PATH = os.path.join(
    "docs", "doctrine", "astra_doctrine_registry_v0_1.yaml",
)
DECISIONS_PATH = os.path.join("docs", "decisions", "current_decisions_log.md")


@pytest.fixture(scope="module")
def review_text():
    with open(REVIEW_PATH, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def registry_text():
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def decisions_text():
    with open(DECISIONS_PATH, encoding="utf-8") as f:
        return f.read()


class TestReviewFileExists:
    def test_review_file_exists(self):
        assert os.path.isfile(REVIEW_PATH)


class TestReviewReferences:
    def test_references_pr_1b_id(self, review_text):
        assert "RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001" in review_text

    def test_references_pr_1a(self, review_text):
        assert "RUNTIME-DOMAIN-PR-1A" in review_text

    def test_references_pr_1(self, review_text):
        assert "RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001" in review_text

    def test_references_pr_0(self, review_text):
        assert "RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001" in review_text

    def test_references_rt_001(self, review_text):
        assert "RT-001" in review_text

    def test_references_rt_011(self, review_text):
        assert "RT-011" in review_text


class TestBackendFirstInvariant:
    def test_states_model_interchangeability(self, review_text):
        assert "model-interchangeable" in review_text

    def test_states_llm_not_game_engine(self, review_text):
        assert "LLM is not the game engine" in review_text

    def test_states_backend_owns_truth(self, review_text):
        assert "backend runtime kernel owns truth" in review_text


class TestReviewSections:
    def test_includes_pr_1a_implementation_review(self, review_text):
        assert "## 4. PR-1A implementation review" in review_text

    def test_includes_command_lifecycle_skeleton_review(self, review_text):
        assert "## 5. Command lifecycle skeleton review" in review_text

    def test_includes_action_legality_skeleton_review(self, review_text):
        assert "## 6. Action legality skeleton review" in review_text

    def test_includes_guardrail_transition_review(self, review_text):
        assert "## 7. Guardrail transition review" in review_text

    def test_includes_kernel_dependency_review(self, review_text):
        assert "## 8. Kernel dependency review" in review_text

    def test_includes_corpus_scale_pressure_review(self, review_text):
        assert "## 9. Corpus-scale pressure review" in review_text

    def test_includes_risk_review(self, review_text):
        assert "## 10. Risk review" in review_text

    def test_includes_future_hardening_ledger(self, review_text):
        assert "## 11. Required future hardening ledger" in review_text

    def test_includes_gate_finding(self, review_text):
        assert "## 12. Gate finding" in review_text

    def test_includes_recommended_next_pr(self, review_text):
        assert "## 13. Recommended next PR" in review_text

    def test_includes_non_implementation_reaffirmation(self, review_text):
        assert "## 14. Non-implementation reaffirmation" in review_text

    def test_includes_classification_block(self, review_text):
        assert "## 15. Classification block" in review_text


class TestGateFinding:
    def test_gate_complete(self, review_text):
        assert "command_lifecycle_action_legality_skeleton_review_complete: true" in review_text

    def test_pr_1a_scope_confirmed(self, review_text):
        assert "pr_1a_scope_confirmed: true" in review_text

    def test_guardrail_transition_safe(self, review_text):
        assert "guardrail_transition_safe: true" in review_text

    def test_next_step_authorized(self, review_text):
        assert "next_step_authorized: RUNTIME-DOMAIN-PR-2" in review_text

    def test_state_store_not_authorized(self, review_text):
        assert "state_store_authorized_by_this_pr: false" in review_text

    def test_state_projection_not_authorized(self, review_text):
        assert "state_projection_authorized_by_this_pr: false" in review_text

    def test_event_commitment_not_authorized(self, review_text):
        assert "event_commitment_authorized_by_this_pr: false" in review_text

    def test_live_play_not_authorized(self, review_text):
        assert "live_play_authorized_by_this_pr: false" in review_text

    def test_conversion_not_authorized(self, review_text):
        assert "conversion_authorized_by_this_pr: false" in review_text


class TestClassificationBlock:
    def test_review_id(self, review_text):
        assert "review_id: RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001" in review_text

    def test_artifact_type(self, review_text):
        assert "artifact_type: command_lifecycle_action_legality_skeleton_review_gate" in review_text

    def test_non_executable(self, review_text):
        assert "implementation_status: non_executable_review_gate" in review_text

    def test_reviews_first_domain_package(self, review_text):
        assert "reviews_first_domain_package_creation: true" in review_text

    def test_reviews_command_lifecycle(self, review_text):
        assert "reviews_command_lifecycle_skeleton: true" in review_text

    def test_reviews_action_legality(self, review_text):
        assert "reviews_action_legality_skeleton: true" in review_text

    def test_reviews_guardrail_transition(self, review_text):
        assert "reviews_guardrail_transition: true" in review_text

    def test_reviews_kernel_dependency(self, review_text):
        assert "reviews_kernel_dependency_usage: true" in review_text

    def test_reviews_corpus_scale(self, review_text):
        assert "reviews_corpus_scale_command_pressure: true" in review_text

    def test_defines_hardening_ledger(self, review_text):
        assert "defines_future_hardening_ledger: true" in review_text

    def test_no_code_authorized(self, review_text):
        assert "authorizes_code_by_this_pr: false" in review_text


class TestNonImplementationGuardrails:
    FORBIDDEN_CLAIMS = [
        "implements command execution",
        "implements command parser",
        "implements state store",
        "implements state projection",
        "implements state mutation",
        "implements transaction lifecycle",
        "implements event commitment",
        "implements resource math",
        "implements combat",
        "implements ability",
        "implements inventory",
        "implements mission",
        "implements social",
        "implements context-packet compiler",
        "implements prompt template",
        "implements model integration",
        "implements live play",
        "implements UI",
        "implements training",
        "implements conversion",
        "implements sourcebook inclusion",
        "implements canon promotion",
    ]

    @pytest.mark.parametrize("claim", FORBIDDEN_CLAIMS)
    def test_review_does_not_claim_implementation(self, review_text, claim):
        assert claim not in review_text


class TestRegistryTracking:
    def test_registry_contains_pr_1b_id(self, registry_text):
        assert "RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001" in registry_text


class TestDecisionLogTracking:
    def test_decisions_contain_pr_1b_id(self, decisions_text):
        assert "RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001" in decisions_text


class TestRuntimeGuardrails:
    """Verify domain package contains only authorized modules and forbidden packages/files are absent."""

    def test_domain_package_exists(self):
        assert os.path.isdir("src/astra_runtime/domain")

    def test_domain_init_exists(self):
        assert os.path.isfile("src/astra_runtime/domain/__init__.py")

    def test_command_lifecycle_exists(self):
        assert os.path.isfile("src/astra_runtime/domain/command_lifecycle.py")

    def test_action_legality_exists(self):
        assert os.path.isfile("src/astra_runtime/domain/action_legality.py")

    def test_domain_package_authorized_files_only(self):
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "transaction_lifecycle.py", "event_commitment.py", "__pycache__"}
        contents = set(os.listdir("src/astra_runtime/domain"))
        unauthorized = contents - allowed
        assert not unauthorized, f"Unauthorized domain files: {unauthorized}"

    def test_state_store_authorized(self):
        assert os.path.exists("src/astra_runtime/domain/state_store.py")

    def test_state_projection_authorized(self):
        assert os.path.exists("src/astra_runtime/domain/state_projection.py")

    def test_transaction_lifecycle_authorized(self):
        assert os.path.exists("src/astra_runtime/domain/transaction_lifecycle.py")

    def test_event_commitment_authorized(self):
        assert os.path.exists("src/astra_runtime/domain/event_commitment.py")

    def test_no_validation_integration(self):
        assert not os.path.exists("src/astra_runtime/domain/validation_integration.py")

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
