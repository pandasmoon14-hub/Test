"""Tests for RUNTIME-DOMAIN-PR-3B transaction lifecycle and event commitment skeleton review gate."""

from __future__ import annotations

import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
REVIEW_PATH = (
    REPO_ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_domain_pr_3b_transaction_lifecycle_event_commitment_skeleton_review.md"
)
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
DOMAIN_PACKAGE_DIR = REPO_ROOT / "src" / "astra_runtime" / "domain"


@pytest.fixture(scope="module")
def review_content() -> str:
    return REVIEW_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def registry_content() -> str:
    return REGISTRY_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_log_content() -> str:
    return DECISION_LOG_PATH.read_text(encoding="utf-8")


class TestReviewFileExists:
    def test_review_file_exists(self):
        assert REVIEW_PATH.exists(), "PR-3B review file must exist"


class TestReviewReferences:
    def test_references_pr_3b_id(self, review_content):
        assert "RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001" in review_content

    def test_references_pr_3a_id(self, review_content):
        assert "RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001" in review_content

    def test_references_pr_3_plan_id(self, review_content):
        assert "RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001" in review_content

    def test_references_transaction_lifecycle_py(self, review_content):
        assert "transaction_lifecycle.py" in review_content

    def test_references_event_commitment_py(self, review_content):
        assert "event_commitment.py" in review_content


class TestBackendFirstInvariant:
    def test_states_backend_first_invariant(self, review_content):
        assert "backend owns truth" in review_content.lower() or "backend-first" in review_content.lower()

    def test_states_llm_not_game_engine(self, review_content):
        assert "LLM is not the game engine" in review_content


class TestReviewSections:
    def test_includes_pr3a_implementation_review(self, review_content):
        assert "PR-3A Implementation Review" in review_content

    def test_includes_transaction_lifecycle_skeleton_review(self, review_content):
        assert "Transaction Lifecycle Skeleton Review" in review_content

    def test_includes_event_commitment_skeleton_review(self, review_content):
        assert "Event Commitment Skeleton Review" in review_content

    def test_includes_validator_parity_review(self, review_content):
        assert "Validator Parity Review" in review_content

    def test_includes_anti_mutation_anti_append_review(self, review_content):
        assert "Anti-Mutation" in review_content and "Anti-Append" in review_content

    def test_includes_domain_package_guardrail_review(self, review_content):
        assert "Domain-Package Guardrail Review" in review_content

    def test_includes_kernel_dependency_review(self, review_content):
        assert "Kernel Dependency Review" in review_content

    def test_includes_corpus_scale_pressure_review(self, review_content):
        assert "Corpus-Scale Pressure Review" in review_content

    def test_includes_risk_review(self, review_content):
        assert "Risk Review" in review_content

    def test_includes_hardening_ledger(self, review_content):
        assert "Hardening Ledger" in review_content

    def test_includes_gate_finding(self, review_content):
        assert "Gate Finding" in review_content

    def test_includes_recommended_next_pr(self, review_content):
        assert "Recommended Next PR" in review_content

    def test_includes_non_implementation_reaffirmation(self, review_content):
        assert "Non-Implementation Reaffirmation" in review_content

    def test_includes_classification_block(self, review_content):
        assert "Classification Block" in review_content


class TestGateFindingContent:
    def test_gate_finding_review_complete(self, review_content):
        assert "transaction_lifecycle_event_commitment_skeleton_review_complete: true" in review_content

    def test_gate_finding_scope_confirmed(self, review_content):
        assert "pr_3a_scope_confirmed: true" in review_content

    def test_gate_finding_no_runtime_code(self, review_content):
        assert "runtime_code_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_domain_code(self, review_content):
        assert "domain_code_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_transaction_execution(self, review_content):
        assert "transaction_execution_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_event_commitment(self, review_content):
        assert "actual_event_commitment_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_event_sourcing(self, review_content):
        assert "event_sourcing_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_state_mutation(self, review_content):
        assert "state_mutation_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_event_ledger_append(self, review_content):
        assert "event_ledger_append_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_persistence(self, review_content):
        assert "durable_persistence_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_model_integration(self, review_content):
        assert "model_integration_authorized_by_this_pr: false" in review_content

    def test_gate_finding_no_live_play(self, review_content):
        assert "live_play_authorized_by_this_pr: false" in review_content

    def test_gate_finding_next_step(self, review_content):
        assert "next_step_authorized: RUNTIME-DOMAIN-PR-4 planning" in review_content


class TestRegistryTracking:
    def test_pr3b_file_id_in_registry(self, registry_content):
        assert "RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001" in registry_content

    def test_pr3b_appears_exactly_once_in_registry(self, registry_content):
        file_id_str = "file_id: RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001"
        count = registry_content.count(file_id_str)
        assert count == 1, f"Expected exactly 1 file_id occurrence, found {count}"


class TestDecisionLogTracking:
    def test_pr3b_id_in_decision_log(self, decision_log_content):
        assert "RUNTIME-DOMAIN-PR-3B" in decision_log_content

    def test_pr3b_heading_appears_exactly_once(self, decision_log_content):
        heading = "## RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001"
        count = decision_log_content.count(heading)
        assert count == 1, f"Expected exactly 1 heading occurrence, found {count}"


class TestDomainPackageGuardrails:
    def test_domain_package_contains_only_authorized_files(self):
        authorized = {
            "__init__.py",
            "command_lifecycle.py",
            "action_legality.py",
            "state_store.py",
            "state_projection.py",
            "transaction_lifecycle.py",
            "event_commitment.py",
            "validation_integration.py",
            "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py",
            "__pycache__",
        }
        entries = {p.name for p in DOMAIN_PACKAGE_DIR.iterdir()}
        unauthorized = entries - authorized
        assert not unauthorized, f"Unauthorized domain files found: {unauthorized}"

    @pytest.mark.parametrize(
        "forbidden_file",
        [
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
        assert not (DOMAIN_PACKAGE_DIR / forbidden_file).exists()

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
        assert not full_path.exists(), f"Unauthorized path must not exist: {forbidden_path}"
