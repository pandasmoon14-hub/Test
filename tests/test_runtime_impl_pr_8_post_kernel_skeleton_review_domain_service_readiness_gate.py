"""Tests for RUNTIME-IMPL-PR-8: Post-Kernel Skeleton Review and Domain-Service Readiness Gate."""

import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

REVIEW_PATH = (
    REPO_ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_impl_pr_8_post_kernel_skeleton_review_domain_service_readiness_gate.md"
)

REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"


@pytest.fixture(scope="module")
def review_text() -> str:
    assert REVIEW_PATH.exists(), f"Review file missing: {REVIEW_PATH}"
    return REVIEW_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def registry_text() -> str:
    assert REGISTRY_PATH.exists(), f"Registry file missing: {REGISTRY_PATH}"
    return REGISTRY_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_log_text() -> str:
    assert DECISION_LOG_PATH.exists(), f"Decision log missing: {DECISION_LOG_PATH}"
    return DECISION_LOG_PATH.read_text(encoding="utf-8")


# --- Review file existence ---


class TestReviewFileExists:
    def test_review_file_exists(self):
        assert REVIEW_PATH.exists()


# --- PR ID references ---


class TestPRReferences:
    def test_references_pr_8_id(self, review_text: str):
        assert "RUNTIME-IMPL-PR-8" in review_text

    @pytest.mark.parametrize(
        "pr_id",
        [
            "RUNTIME-IMPL-PR-0",
            "RUNTIME-IMPL-PR-1",
            "RUNTIME-IMPL-PR-2",
            "RUNTIME-IMPL-PR-3",
            "RUNTIME-IMPL-PR-4",
            "RUNTIME-IMPL-PR-5",
            "RUNTIME-IMPL-PR-6",
            "RUNTIME-IMPL-PR-7",
        ],
    )
    def test_references_impl_prs(self, review_text: str, pr_id: str):
        assert pr_id in review_text

    def test_references_seq_pr_f(self, review_text: str):
        assert "RUNTIME-SEQ-PR-F" in review_text

    @pytest.mark.parametrize(
        "rt_id",
        [
            "RT-001",
            "RT-002",
            "RT-003",
            "RT-004",
            "RT-005",
            "RT-006",
            "RT-007",
            "RT-008",
            "RT-009",
            "RT-010",
            "RT-011",
            "RT-012",
        ],
    )
    def test_references_rt_owner_specs(self, review_text: str, rt_id: str):
        assert rt_id in review_text


# --- Core invariants ---


class TestBackendFirstInvariant:
    def test_states_model_interchangeability(self, review_text: str):
        assert "model-interchangeable" in review_text

    def test_states_llm_not_game_engine(self, review_text: str):
        assert "LLM is not the game engine" in review_text

    def test_states_backend_owns_truth(self, review_text: str):
        assert "backend" in review_text.lower() and "owns truth" in review_text.lower()


# --- Required sections ---


class TestRequiredSections:
    def test_includes_kernel_skeleton_coverage_review(self, review_text: str):
        assert "Kernel skeleton coverage review" in review_text

    def test_includes_interface_completeness_matrix(self, review_text: str):
        assert "Interface completeness matrix" in review_text

    def test_includes_domain_service_readiness_finding(self, review_text: str):
        assert "Domain-service readiness finding" in review_text

    def test_includes_domain_service_family_sequencing_proposal(self, review_text: str):
        assert "Domain-service family sequencing proposal" in review_text

    def test_recommends_runtime_domain_pr_0(self, review_text: str):
        assert "RUNTIME-DOMAIN-PR-0" in review_text

    def test_includes_guardrail_integrity_review(self, review_text: str):
        assert "Guardrail integrity review" in review_text

    def test_includes_domain_service_dependency_rules(self, review_text: str):
        assert "Domain-service dependency rules" in review_text

    def test_includes_blocked_until_ledger(self, review_text: str):
        assert "Blocked-until ledger" in review_text

    def test_includes_risk_review(self, review_text: str):
        assert "Risk review" in review_text

    def test_includes_future_integration_test_families(self, review_text: str):
        assert "Future integration test families" in review_text

    def test_includes_non_implementation_reaffirmation(self, review_text: str):
        assert "Non-implementation reaffirmation" in review_text

    def test_includes_classification_block(self, review_text: str):
        assert "Classification block" in review_text


# --- Gate finding statuses ---


class TestGateFinding:
    def test_minimum_kernel_skeleton_complete(self, review_text: str):
        assert "minimum_backend_kernel_skeleton_complete: true" in review_text

    def test_ready_for_domain_service_planning(self, review_text: str):
        assert "ready_for_domain_service_planning: true" in review_text

    def test_domain_service_implementation_not_authorized(self, review_text: str):
        assert (
            "direct_domain_service_implementation_authorized_by_this_pr: false"
            in review_text
        )

    def test_live_play_not_authorized(self, review_text: str):
        assert "direct_live_play_authorized_by_this_pr: false" in review_text

    def test_conversion_not_authorized(self, review_text: str):
        assert (
            "direct_conversion_execution_authorized_by_this_pr: false" in review_text
        )

    def test_next_step_is_domain_pr_0(self, review_text: str):
        assert "next_step_id: RUNTIME-DOMAIN-PR-0" in review_text


# --- Classification block ---


class TestClassificationBlock:
    def test_review_id(self, review_text: str):
        assert (
            "RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001"
            in review_text
        )

    def test_artifact_type(self, review_text: str):
        assert "post_kernel_skeleton_review_and_domain_service_readiness_gate" in review_text

    def test_non_executable(self, review_text: str):
        assert "non_executable_review_gate" in review_text

    @pytest.mark.parametrize(
        "field",
        [
            "authorizes_domain_service_code_by_this_pr: false",
            "authorizes_command_execution_by_this_pr: false",
            "authorizes_state_store_by_this_pr: false",
            "authorizes_state_mutation_by_this_pr: false",
            "authorizes_event_commitment_by_this_pr: false",
            "authorizes_durable_persistence_by_this_pr: false",
            "authorizes_context_packet_compiler_by_this_pr: false",
            "authorizes_prompt_templates_by_this_pr: false",
            "authorizes_model_integration_by_this_pr: false",
            "authorizes_live_play_by_this_pr: false",
            "authorizes_ui_client_by_this_pr: false",
            "authorizes_training_by_this_pr: false",
            "authorizes_pilot_conversion_by_this_pr: false",
            "authorizes_sourcebook_inclusion_by_this_pr: false",
            "authorizes_canon_promotion_by_this_pr: false",
        ],
    )
    def test_classification_denials(self, review_text: str, field: str):
        assert field in review_text


# --- Representative blocked items ---


class TestBlockedItems:
    @pytest.mark.parametrize(
        "item",
        [
            "LLM state ownership",
            "LLM dice/RNG authority",
            "LLM event commitment",
            "Narration as state",
            "Hidden information exposure",
            "Prompt templates",
            "Model integration",
            "Live-play adapter",
            "Canon promotion",
        ],
    )
    def test_guardrail_blocked_items(self, review_text: str, item: str):
        assert item in review_text


# --- No-implementation claims ---


class TestNoImplementationClaims:
    @pytest.mark.parametrize(
        "forbidden",
        [
            "implements domain service",
            "implements command execution",
            "implements state store",
            "implements state mutation",
            "implements event commitment",
            "implements durable persistence",
            "implements database schema",
            "implements replay engine",
            "implements context-packet compiler",
            "implements prompt template",
            "implements model integration",
            "implements live-play",
            "implements UI/client",
            "implements training",
            "implements conversion",
            "implements sourcebook inclusion",
            "implements canon promotion",
        ],
    )
    def test_does_not_claim_implementation(self, review_text: str, forbidden: str):
        assert forbidden.lower() not in review_text.lower()


# --- Registry tracking ---


class TestRegistryTracking:
    def test_registry_has_pr_8_entry(self, registry_text: str):
        assert (
            "RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001"
            in registry_text
        )


# --- Decision log tracking ---


class TestDecisionLogTracking:
    def test_decision_log_has_pr_8_entry(self, decision_log_text: str):
        assert (
            "RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001"
            in decision_log_text
        )


# --- Runtime guardrail checks ---


class TestRuntimeGuardrails:
    def test_domain_package_contains_only_authorized_modules(self):
        domain_path = REPO_ROOT / "src" / "astra_runtime" / "domain"
        assert domain_path.exists(), "Domain package should exist after PR-1A"
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "transaction_lifecycle.py", "event_commitment.py", "validation_integration.py", "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py", "scene_command_execution_skeleton.py", "__pycache__"}
        actual = {p.name for p in domain_path.iterdir()}
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized domain modules: {unauthorized}"

    def test_no_model_integration_package(self):
        model_path = REPO_ROOT / "src" / "astra_runtime" / "model"
        assert not model_path.exists(), "Model integration package must not exist yet"

    def test_no_prompt_template_package(self):
        prompt_path = REPO_ROOT / "src" / "astra_runtime" / "prompts"
        assert not prompt_path.exists(), "Prompt template package must not exist yet"

    def test_no_live_play_adapter_package(self):
        lp_path = REPO_ROOT / "src" / "astra_runtime" / "live_play"
        assert not lp_path.exists(), "Live-play adapter package must not exist yet"

    def test_no_ui_client_package(self):
        ui_path = REPO_ROOT / "src" / "astra_runtime" / "ui"
        assert not ui_path.exists(), "UI/client package must not exist yet"

    def test_no_database_package(self):
        db_path = REPO_ROOT / "src" / "astra_runtime" / "database"
        assert not db_path.exists(), "Database package must not exist yet"

    def test_no_durable_store_package(self):
        store_path = REPO_ROOT / "src" / "astra_runtime" / "store"
        assert not store_path.exists(), "Durable store package must not exist yet"

    def test_no_context_packet_compiler(self):
        compiler_path = (
            REPO_ROOT / "src" / "astra_runtime" / "kernel" / "context_packet_compiler.py"
        )
        assert not compiler_path.exists(), "context_packet_compiler.py must not exist yet"
