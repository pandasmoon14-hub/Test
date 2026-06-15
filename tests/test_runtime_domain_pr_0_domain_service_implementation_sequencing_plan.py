"""Tests for RUNTIME-DOMAIN-PR-0: Domain Service Implementation Sequencing Plan."""

import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

PLAN_PATH = (
    REPO_ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md"
)

REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"


@pytest.fixture(scope="module")
def plan_text() -> str:
    assert PLAN_PATH.exists(), f"Plan file missing: {PLAN_PATH}"
    return PLAN_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def registry_text() -> str:
    assert REGISTRY_PATH.exists(), f"Registry file missing: {REGISTRY_PATH}"
    return REGISTRY_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_log_text() -> str:
    assert DECISION_LOG_PATH.exists(), f"Decision log missing: {DECISION_LOG_PATH}"
    return DECISION_LOG_PATH.read_text(encoding="utf-8")


# --- Plan file existence ---


class TestPlanFileExists:
    def test_plan_file_exists(self):
        assert PLAN_PATH.exists()


# --- PR ID references ---


class TestPRReferences:
    def test_references_domain_pr_0_id(self, plan_text: str):
        assert "RUNTIME-DOMAIN-PR-0" in plan_text

    def test_references_impl_pr_8(self, plan_text: str):
        assert "RUNTIME-IMPL-PR-8" in plan_text

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
    def test_references_impl_prs_0_through_7(self, plan_text: str, pr_id: str):
        assert pr_id in plan_text

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
    def test_references_rt_owner_specs(self, plan_text: str, rt_id: str):
        assert rt_id in plan_text


# --- Core invariants ---


class TestBackendFirstInvariant:
    def test_states_model_interchangeability(self, plan_text: str):
        assert "model-interchangeable" in plan_text

    def test_states_llm_not_game_engine(self, plan_text: str):
        assert "LLM is not the game engine" in plan_text

    def test_states_backend_owns_truth(self, plan_text: str):
        assert "backend" in plan_text.lower() and "owns truth" in plan_text.lower()


# --- Domain-service sequencing thesis ---


class TestSequencingThesis:
    def test_includes_sequencing_thesis(self, plan_text: str):
        assert "Domain-service sequencing thesis" in plan_text

    def test_dependency_order_statement(self, plan_text: str):
        assert "dependency order" in plan_text


# --- Domain-service family inventory ---


class TestDomainServiceFamilyInventory:
    def test_includes_family_inventory(self, plan_text: str):
        assert "Domain-service family inventory" in plan_text

    @pytest.mark.parametrize(
        "family",
        [
            "Command lifecycle / action legality",
            "State store / state projection",
            "Transaction lifecycle / event commitment",
            "Validation integration / invariant enforcement",
            "Resource / consequence math",
            "Combat / hazard / damage / recovery",
            "Ability / effect / skill binding",
            "Inventory / item / vehicle / asset",
            "Mission / reward / clue routing",
            "Social / faction / actor knowledge",
            "Generated-content provenance / recurrence",
            "Context-packet compiler",
            "Model evaluation harness",
            "Live-play adapter gate",
        ],
    )
    def test_family_present(self, plan_text: str, family: str):
        assert family in plan_text


# --- Recommended future PR sequence ---


class TestRecommendedPRSequence:
    def test_includes_pr_sequence_section(self, plan_text: str):
        assert "Recommended future PR sequence" in plan_text

    @pytest.mark.parametrize(
        "pr_id",
        [
            "RUNTIME-DOMAIN-PR-1",
            "RUNTIME-DOMAIN-PR-2",
            "RUNTIME-DOMAIN-PR-3",
            "RUNTIME-DOMAIN-PR-4",
            "RUNTIME-DOMAIN-PR-5",
            "RUNTIME-DOMAIN-PR-6",
            "RUNTIME-DOMAIN-PR-7",
            "RUNTIME-DOMAIN-PR-8",
            "RUNTIME-DOMAIN-PR-9",
            "RUNTIME-DOMAIN-PR-10",
            "RUNTIME-DOMAIN-PR-11",
            "RUNTIME-DOMAIN-PR-12",
            "RUNTIME-DOMAIN-PR-13",
            "RUNTIME-DOMAIN-PR-14",
            "RUNTIME-DOMAIN-PR-15",
        ],
    )
    def test_future_pr_listed(self, plan_text: str, pr_id: str):
        assert pr_id in plan_text

    def test_recommends_domain_pr_1(self, plan_text: str):
        assert "RUNTIME-DOMAIN-PR-1" in plan_text


# --- Immediate next PR authorization boundary ---


class TestImmediateNextPRBoundary:
    def test_includes_authorization_boundary_section(self, plan_text: str):
        assert "Immediate next PR authorization boundary" in plan_text

    def test_pr_1_planning_document_allowed(self, plan_text: str):
        assert "planning document for command lifecycle" in plan_text


# --- Domain-service dependency rules ---


class TestDependencyRules:
    def test_includes_dependency_rules_section(self, plan_text: str):
        assert "Domain-service dependency rules" in plan_text

    @pytest.mark.parametrize(
        "rule_fragment",
        [
            "No direct state mutation",
            "No direct event commitment",
            "No RNG/table bypass",
            "No hidden-info exposure outside context projection",
            "No durable persistence outside persistence boundary",
            "No generated content durability without provenance",
            "No LLM output as validation authority",
            "No runtime trace bypass",
            "No source-local content canon promotion",
            "No donor assumptions silently becoming Astra baseline",
        ],
    )
    def test_dependency_rule_present(self, plan_text: str, rule_fragment: str):
        assert rule_fragment in plan_text


# --- Kernel dependency matrix ---


class TestKernelDependencyMatrix:
    def test_includes_matrix_section(self, plan_text: str):
        assert "Kernel dependency matrix" in plan_text

    @pytest.mark.parametrize(
        "status",
        ["required", "optional", "not_applicable"],
    )
    def test_matrix_uses_statuses(self, plan_text: str, status: str):
        assert status in plan_text


# --- Blocked-until ledger ---


class TestBlockedUntilLedger:
    def test_includes_blocked_until_section(self, plan_text: str):
        assert "Blocked-until ledger" in plan_text

    @pytest.mark.parametrize(
        "blocked_item",
        [
            "Command lifecycle implementation",
            "State store implementation",
            "Transaction lifecycle implementation",
            "Event commitment implementation",
            "Validation integration implementation",
            "Live-play adapter implementation",
            "Pilot conversion",
            "Canon promotion",
        ],
    )
    def test_blocked_item_present(self, plan_text: str, blocked_item: str):
        assert blocked_item in plan_text


# --- Risk review ---


class TestRiskReview:
    def test_includes_risk_review_section(self, plan_text: str):
        assert "Risk review" in plan_text

    @pytest.mark.parametrize(
        "risk_fragment",
        [
            "Domain services bypass kernel envelopes",
            "Command/state/event collapse",
            "Hidden info leakage",
            "RNG nondeterminism",
            "Event commitment without validation",
            "State mutation without trace",
            "Persistence side effects before backend choice",
            "Validation becoming decorative",
            "Generated content becoming durable without provenance",
            "Donor assumptions entering runtime services",
            "Context-packet compiler built too early",
            "Model integration becoming authority",
            "Live-play before backend truth is operational",
            "Conversion landing before runtime services are ready",
        ],
    )
    def test_risk_present(self, plan_text: str, risk_fragment: str):
        assert risk_fragment in plan_text


# --- Future integration test plan ---


class TestFutureIntegrationTestPlan:
    def test_includes_integration_test_section(self, plan_text: str):
        assert "Future integration test plan" in plan_text

    @pytest.mark.parametrize(
        "test_family_fragment",
        [
            "Command envelope to action legality result",
            "Command to transaction preview to state delta to event ledger chain",
            "State store projection from event/delta references",
            "Validation result gating transaction/event commitment",
            "Deterministic RNG/table references in events",
            "Hidden-info projection non-leak tests",
            "Persistence boundary no-direct-write tests",
            "Replay/hash audit deterministic chain tests",
            "Runtime trace completeness tests",
            "Generated-content provenance tests",
            "LLM non-authority adversarial tests",
            "Source-local/canon boundary tests",
        ],
    )
    def test_integration_test_family_present(self, plan_text: str, test_family_fragment: str):
        assert test_family_fragment in plan_text


# --- Non-implementation reaffirmation ---


class TestNonImplementationReaffirmation:
    def test_includes_reaffirmation_section(self, plan_text: str):
        assert "Non-implementation reaffirmation" in plan_text


# --- Gate finding ---


class TestGateFinding:
    def test_domain_service_sequence_defined(self, plan_text: str):
        assert "domain_service_sequence_defined: true" in plan_text

    def test_ready_for_pr_1_planning(self, plan_text: str):
        assert "ready_for_runtime_domain_pr_1_planning: true" in plan_text

    def test_domain_service_code_not_authorized(self, plan_text: str):
        assert "domain_service_code_authorized_by_this_pr: false" in plan_text

    def test_command_execution_not_authorized(self, plan_text: str):
        assert "command_execution_authorized_by_this_pr: false" in plan_text

    def test_state_store_not_authorized(self, plan_text: str):
        assert "state_store_authorized_by_this_pr: false" in plan_text

    def test_event_commitment_not_authorized(self, plan_text: str):
        assert "event_commitment_authorized_by_this_pr: false" in plan_text

    def test_live_play_not_authorized(self, plan_text: str):
        assert "live_play_authorized_by_this_pr: false" in plan_text

    def test_conversion_not_authorized(self, plan_text: str):
        assert "conversion_authorized_by_this_pr: false" in plan_text

    def test_next_step_is_domain_pr_1(self, plan_text: str):
        assert (
            "next_step_authorized: RUNTIME-DOMAIN-PR-1 command lifecycle and action legality service plan"
            in plan_text
        )

    def test_next_step_planning_only(self, plan_text: str):
        assert "next_step_status: planning_only" in plan_text


# --- Classification block ---


class TestClassificationBlock:
    def test_includes_classification_section(self, plan_text: str):
        assert "Classification block" in plan_text

    def test_review_id(self, plan_text: str):
        assert (
            "RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001"
            in plan_text
        )

    def test_artifact_type(self, plan_text: str):
        assert "domain_service_implementation_sequencing_plan" in plan_text

    def test_non_executable(self, plan_text: str):
        assert "non_executable_plan" in plan_text

    @pytest.mark.parametrize(
        "field",
        [
            "authorizes_domain_service_code_by_this_pr: false",
            "authorizes_command_execution_by_this_pr: false",
            "authorizes_action_legality_engine_by_this_pr: false",
            "authorizes_state_store_by_this_pr: false",
            "authorizes_state_mutation_by_this_pr: false",
            "authorizes_transaction_lifecycle_by_this_pr: false",
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
    def test_classification_denials(self, plan_text: str, field: str):
        assert field in plan_text


# --- No-implementation claims ---


class TestNoImplementationClaims:
    @pytest.mark.parametrize(
        "forbidden",
        [
            "implements domain service",
            "implements command execution",
            "implements action legality engine",
            "implements state store",
            "implements state mutation",
            "implements transaction lifecycle",
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
    def test_does_not_claim_implementation(self, plan_text: str, forbidden: str):
        assert forbidden.lower() not in plan_text.lower()


# --- Registry tracking ---


class TestRegistryTracking:
    def test_registry_has_domain_pr_0_entry(self, registry_text: str):
        assert (
            "RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001"
            in registry_text
        )


# --- Decision log tracking ---


class TestDecisionLogTracking:
    def test_decision_log_has_domain_pr_0_entry(self, decision_log_text: str):
        assert (
            "RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001"
            in decision_log_text
        )


# --- Runtime guardrail checks ---


class TestRuntimeGuardrails:
    def test_domain_package_contains_only_authorized_modules(self):
        domain_path = REPO_ROOT / "src" / "astra_runtime" / "domain"
        assert domain_path.exists(), "Domain package should exist after PR-1A"
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "transaction_lifecycle.py", "event_commitment.py", "validation_integration.py", "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py", "scene_command_execution_skeleton.py", "command_kind_routing_skeleton.py", "__pycache__"}
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

    def test_no_store_package(self):
        store_path = REPO_ROOT / "src" / "astra_runtime" / "store"
        assert not store_path.exists(), "Durable store package must not exist yet"

    def test_no_context_packet_compiler(self):
        compiler_path = (
            REPO_ROOT / "src" / "astra_runtime" / "kernel" / "context_packet_compiler.py"
        )
        assert not compiler_path.exists(), "context_packet_compiler.py must not exist yet"
