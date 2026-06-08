"""Tests for RUNTIME-DOMAIN-PR-1 command lifecycle and action legality service plan."""

import os
import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

PLAN_PATH = (
    REPO_ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_domain_pr_1_command_lifecycle_action_legality_service_plan.md"
)

REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"


@pytest.fixture(scope="module")
def plan_text():
    return PLAN_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def registry_text():
    return REGISTRY_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_log_text():
    return DECISION_LOG_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------


class TestPlanFileExists:
    def test_plan_file_exists(self):
        assert PLAN_PATH.exists(), f"Plan file not found at {PLAN_PATH}"


# ---------------------------------------------------------------------------
# PR references
# ---------------------------------------------------------------------------


class TestPRReferences:
    def test_references_runtime_domain_pr_1_id(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001" in plan_text

    def test_references_runtime_domain_pr_0(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-0" in plan_text

    def test_references_runtime_impl_pr_8(self, plan_text):
        assert "RUNTIME-IMPL-PR-8" in plan_text

    def test_references_rt_001(self, plan_text):
        assert "RT-001" in plan_text

    def test_references_rt_011(self, plan_text):
        assert "RT-011" in plan_text

    def test_references_implementation_prs(self, plan_text):
        for n in range(8):
            assert f"RUNTIME-IMPL-PR-{n}" in plan_text, f"Missing reference to RUNTIME-IMPL-PR-{n}"

    def test_references_seq_prs(self, plan_text):
        for letter in "ABCDEF":
            assert f"RUNTIME-SEQ-PR-{letter}" in plan_text, f"Missing reference to RUNTIME-SEQ-PR-{letter}"

    def test_references_rt_owner_specs(self, plan_text):
        for n in range(1, 13):
            tag = f"RT-{n:03d}" if n < 10 else f"RT-0{n}" if n < 100 else f"RT-{n}"
            assert tag in plan_text, f"Missing reference to {tag}"


# ---------------------------------------------------------------------------
# Backend-first invariant
# ---------------------------------------------------------------------------


class TestBackendFirstInvariant:
    def test_model_interchangeability(self, plan_text):
        assert "model-interchangeable" in plan_text.lower() or "model interchangeable" in plan_text.lower()

    def test_llm_not_game_engine(self, plan_text):
        assert "LLM is not the game engine" in plan_text

    def test_backend_owns_truth(self, plan_text):
        assert "backend" in plan_text.lower() and "owns truth" in plan_text.lower()


# ---------------------------------------------------------------------------
# Service ownership
# ---------------------------------------------------------------------------


class TestServiceOwnership:
    def test_service_ownership_section(self, plan_text):
        assert "## 4. Service ownership" in plan_text or "Service ownership" in plan_text

    def test_primary_owner_rt_001(self, plan_text):
        assert "RT-001" in plan_text and "command lifecycle" in plan_text.lower()

    def test_must_not_own_list(self, plan_text):
        assert "must not own" in plan_text.lower()


# ---------------------------------------------------------------------------
# Future service responsibilities
# ---------------------------------------------------------------------------


class TestFutureServiceResponsibilities:
    def test_allowed_responsibilities_section(self, plan_text):
        assert "Allowed future responsibilities" in plan_text or "allowed future responsibilities" in plan_text.lower()

    def test_forbidden_responsibilities_section(self, plan_text):
        assert "Forbidden responsibilities" in plan_text or "forbidden responsibilities" in plan_text.lower()

    def test_accept_command_envelope(self, plan_text):
        assert "command envelope" in plan_text.lower()

    def test_no_command_execution(self, plan_text):
        lower = plan_text.lower()
        assert "execute commands" in lower or "command execution" in lower

    def test_no_state_mutation(self, plan_text):
        assert "Mutate state" in plan_text or "state mutation" in plan_text.lower()


# ---------------------------------------------------------------------------
# Command lifecycle state model
# ---------------------------------------------------------------------------


class TestCommandLifecycleStateModel:
    EXPECTED_STATES = [
        "received",
        "envelope_validated",
        "actor_bound",
        "visibility_checked",
        "legality_prechecked",
        "dependency_declared",
        "preview_requested",
        "confirmation_required",
        "accepted_for_transaction_planning",
        "rejected",
        "quarantined",
        "cancelled",
    ]

    def test_state_model_section(self, plan_text):
        assert "Command lifecycle state model" in plan_text

    @pytest.mark.parametrize("state", EXPECTED_STATES)
    def test_state_present(self, plan_text, state):
        assert state in plan_text, f"Missing lifecycle state: {state}"

    def test_states_have_meaning(self, plan_text):
        assert plan_text.count("**Meaning:**") >= 10

    def test_states_have_prohibited_behavior(self, plan_text):
        assert plan_text.count("**Prohibited behavior:**") >= 10


# ---------------------------------------------------------------------------
# Action legality decision model
# ---------------------------------------------------------------------------


class TestActionLegalityDecisionModel:
    EXPECTED_DECISIONS = [
        "legal",
        "illegal",
        "requires_confirmation",
        "requires_more_information",
        "blocked_by_hidden_information",
        "blocked_by_missing_actor",
        "blocked_by_invalid_target",
        "blocked_by_resource_precheck",
        "blocked_by_timing",
        "blocked_by_scope",
        "quarantined_for_validation",
        "unsupported_command_type",
    ]

    def test_decision_model_section(self, plan_text):
        assert "Action legality decision model" in plan_text

    @pytest.mark.parametrize("decision", EXPECTED_DECISIONS)
    def test_decision_present(self, plan_text, decision):
        assert decision in plan_text, f"Missing legality decision: {decision}"

    def test_decisions_have_hidden_info_safety(self, plan_text):
        assert plan_text.count("**Hidden-info safe:**") >= 10


# ---------------------------------------------------------------------------
# Kernel interface consumption plan
# ---------------------------------------------------------------------------


class TestKernelInterfaceConsumptionPlan:
    KERNEL_MODULES = [
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
    ]

    def test_consumption_plan_section(self, plan_text):
        assert "Kernel interface consumption plan" in plan_text

    @pytest.mark.parametrize("module", KERNEL_MODULES)
    def test_kernel_module_in_matrix(self, plan_text, module):
        assert module in plan_text, f"Missing kernel module in consumption plan: {module}"

    def test_command_envelope_required(self, plan_text):
        assert "command_envelope" in plan_text and "required" in plan_text.lower()

    def test_validation_pipeline_required(self, plan_text):
        assert "validation_pipeline" in plan_text and "required" in plan_text.lower()

    def test_event_ledger_forbidden(self, plan_text):
        assert "event_ledger" in plan_text and "forbidden" in plan_text.lower()


# ---------------------------------------------------------------------------
# Dependency and handoff boundaries
# ---------------------------------------------------------------------------


class TestDependencyHandoffBoundaries:
    HANDOFF_TARGETS = [
        "State store",
        "Transaction lifecycle",
        "Validation integration",
        "Resource",
        "Combat",
        "Ability",
        "Inventory",
        "Mission",
        "Social",
        "Generated-content",
        "Context-packet compiler",
        "Model evaluation",
        "Live-play adapter",
    ]

    def test_handoff_section(self, plan_text):
        assert "Dependency and handoff boundaries" in plan_text

    @pytest.mark.parametrize("target", HANDOFF_TARGETS)
    def test_handoff_target_present(self, plan_text, target):
        assert target in plan_text, f"Missing handoff target: {target}"


# ---------------------------------------------------------------------------
# Future implementation architecture
# ---------------------------------------------------------------------------


class TestFutureImplementationArchitecture:
    def test_architecture_section(self, plan_text):
        assert "Future implementation architecture" in plan_text

    def test_domain_init_module(self, plan_text):
        assert "src/astra_runtime/domain/__init__.py" in plan_text

    def test_command_lifecycle_module(self, plan_text):
        assert "src/astra_runtime/domain/command_lifecycle.py" in plan_text

    def test_action_legality_module(self, plan_text):
        assert "src/astra_runtime/domain/action_legality.py" in plan_text

    def test_proposed_symbols(self, plan_text):
        for sym in [
            "CommandLifecycleStage",
            "ActionLegalityDecision",
            "CommandLifecycleResult",
            "ActionLegalityResult",
            "CommandLifecycleService",
            "ActionLegalityService",
            "evaluate_command_lifecycle",
            "evaluate_action_legality",
        ]:
            assert sym in plan_text, f"Missing proposed symbol: {sym}"

    def test_must_not_create_in_pr_1(self, plan_text):
        assert "must not be created in PR-1" in plan_text


# ---------------------------------------------------------------------------
# Future data shapes
# ---------------------------------------------------------------------------


class TestFutureDataShapes:
    def test_data_shapes_section(self, plan_text):
        assert "Future data shapes" in plan_text

    def test_command_lifecycle_result_shape(self, plan_text):
        assert "Command lifecycle result" in plan_text

    def test_action_legality_result_shape(self, plan_text):
        assert "Action legality result" in plan_text

    def test_dependency_declaration_shape(self, plan_text):
        assert "Dependency declaration" in plan_text

    def test_legality_block_reason_shape(self, plan_text):
        assert "Legality block reason" in plan_text

    def test_confirmation_requirement_shape(self, plan_text):
        assert "Confirmation requirement" in plan_text

    def test_quarantine_result_shape(self, plan_text):
        assert "Quarantine result" in plan_text


# ---------------------------------------------------------------------------
# Implementation PR authorization boundary
# ---------------------------------------------------------------------------


class TestImplementationPRAuthorizationBoundary:
    def test_authorization_boundary_section(self, plan_text):
        assert "Implementation PR authorization boundary" in plan_text

    def test_recommends_pr_1a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-1A" in plan_text

    def test_pr_1a_skeleton_only(self, plan_text):
        assert "Skeleton-only" in plan_text or "skeleton" in plan_text.lower()


# ---------------------------------------------------------------------------
# Test requirements for future implementation
# ---------------------------------------------------------------------------


class TestFutureTestRequirements:
    EXPECTED_FAMILIES = [
        "import/export integrity",
        "command envelope accepted/rejected",
        "invalid envelope quarantine",
        "actor record ID validation",
        "lifecycle state transition",
        "legality decision category",
        "hidden-info-safe rejection",
        "validation result integration",
        "transaction preview handoff",
        "no state mutation guardrail",
        "no event commitment guardrail",
        "no RNG bypass guardrail",
        "no model call guardrail",
        "runtime trace declaration",
        "downstream dependency declaration",
        "adversarial command",
        "corpus-scale donor command vocabulary",
    ]

    def test_test_requirements_section(self, plan_text):
        assert "Test requirements for future implementation" in plan_text

    @pytest.mark.parametrize("family", EXPECTED_FAMILIES)
    def test_test_family_present(self, plan_text, family):
        assert family.lower() in plan_text.lower(), f"Missing test family: {family}"


# ---------------------------------------------------------------------------
# Corpus-scale command pressure review
# ---------------------------------------------------------------------------


class TestCorpusScaleCommandPressureReview:
    PRESSURE_CATEGORIES = [
        "attack",
        "spell",
        "inventory",
        "movement",
        "social",
        "investigation",
        "crafting",
        "vehicle",
        "companion",
        "downtime",
        "meta-action",
        "ambiguous",
        "hidden information",
        "bypass cost",
        "donor-specific action econom",
        "source-local",
    ]

    def test_pressure_review_section(self, plan_text):
        assert "Corpus-scale command pressure review" in plan_text

    @pytest.mark.parametrize("category", PRESSURE_CATEGORIES)
    def test_pressure_category_present(self, plan_text, category):
        assert category.lower() in plan_text.lower(), f"Missing pressure category: {category}"


# ---------------------------------------------------------------------------
# Guardrail review
# ---------------------------------------------------------------------------


class TestGuardrailReview:
    BLOCKED_ITEMS = [
        "LLM state ownership",
        "LLM dice/RNG authority",
        "LLM event commitment",
        "LLM memory authority",
        "narration as state",
        "hidden information exposure",
        "command execution by model output",
        "command legality decided by model output",
        "state mutation without event path",
        "canon promotion",
    ]

    def test_guardrail_section(self, plan_text):
        assert "Guardrail review" in plan_text

    @pytest.mark.parametrize("item", BLOCKED_ITEMS)
    def test_blocked_item_present(self, plan_text, item):
        assert item.lower() in plan_text.lower(), f"Missing guardrail item: {item}"


# ---------------------------------------------------------------------------
# Risk review
# ---------------------------------------------------------------------------


class TestRiskReview:
    RISK_FRAGMENTS = [
        "command lifecycle becomes command execution",
        "action legality becomes domain rule engine",
        "hidden information leaks through rejection",
        "resource",
        "combat assumptions",
        "donor action econom",
        "LLM becomes de facto command parser",
        "transaction preview",
        "validation becomes decorative",
        "state is mutated during legality",
        "live-play loop bypasses",
        "ambiguous commands",
        "unsupported donor commands",
    ]

    def test_risk_review_section(self, plan_text):
        assert "Risk review" in plan_text

    @pytest.mark.parametrize("fragment", RISK_FRAGMENTS)
    def test_risk_present(self, plan_text, fragment):
        assert fragment.lower() in plan_text.lower(), f"Missing risk: {fragment}"


# ---------------------------------------------------------------------------
# Non-implementation reaffirmation
# ---------------------------------------------------------------------------


class TestNonImplementationReaffirmation:
    def test_non_implementation_section(self, plan_text):
        assert "Non-implementation reaffirmation" in plan_text

    def test_no_runtime_code(self, plan_text):
        section_start = plan_text.find("Non-implementation reaffirmation")
        section = plan_text[section_start:section_start + 1000]
        assert "runtime code" in section.lower()

    def test_no_domain_service_code(self, plan_text):
        section_start = plan_text.find("Non-implementation reaffirmation")
        section = plan_text[section_start:section_start + 1000]
        assert "domain-service code" in section.lower()


# ---------------------------------------------------------------------------
# Gate finding
# ---------------------------------------------------------------------------


class TestGateFinding:
    def test_gate_finding_section(self, plan_text):
        assert "gate_finding:" in plan_text

    def test_plan_defined_true(self, plan_text):
        assert "command_lifecycle_action_legality_plan_defined: true" in plan_text

    def test_ready_for_skeleton_true(self, plan_text):
        assert "ready_for_command_lifecycle_skeleton_implementation_pr: true" in plan_text

    def test_command_lifecycle_code_not_authorized(self, plan_text):
        assert "command_lifecycle_code_authorized_by_this_pr: false" in plan_text

    def test_action_legality_engine_not_authorized(self, plan_text):
        assert "action_legality_engine_authorized_by_this_pr: false" in plan_text

    def test_command_execution_not_authorized(self, plan_text):
        assert "command_execution_authorized_by_this_pr: false" in plan_text

    def test_state_store_not_authorized(self, plan_text):
        assert "state_store_authorized_by_this_pr: false" in plan_text

    def test_state_mutation_not_authorized(self, plan_text):
        assert "state_mutation_authorized_by_this_pr: false" in plan_text

    def test_event_commitment_not_authorized(self, plan_text):
        assert "event_commitment_authorized_by_this_pr: false" in plan_text

    def test_model_integration_not_authorized(self, plan_text):
        assert "model_integration_authorized_by_this_pr: false" in plan_text

    def test_live_play_not_authorized(self, plan_text):
        assert "live_play_authorized_by_this_pr: false" in plan_text

    def test_conversion_not_authorized(self, plan_text):
        assert "conversion_authorized_by_this_pr: false" in plan_text

    def test_next_step_is_pr_1a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-1A" in plan_text
        assert "narrow_skeleton_implementation_pending_review" in plan_text


# ---------------------------------------------------------------------------
# Classification block
# ---------------------------------------------------------------------------


class TestClassificationBlock:
    def test_classification_section(self, plan_text):
        assert "runtime_domain_pr_1:" in plan_text

    def test_review_id(self, plan_text):
        assert "review_id: RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001" in plan_text

    def test_artifact_type(self, plan_text):
        assert "artifact_type: command_lifecycle_action_legality_service_plan" in plan_text

    def test_non_executable_status(self, plan_text):
        assert "implementation_status: non_executable_plan" in plan_text

    DENIAL_FIELDS = [
        "authorizes_command_lifecycle_code_by_this_pr: false",
        "authorizes_action_legality_engine_by_this_pr: false",
        "authorizes_command_execution_by_this_pr: false",
        "authorizes_command_parser_by_this_pr: false",
        "authorizes_state_store_by_this_pr: false",
        "authorizes_state_mutation_by_this_pr: false",
        "authorizes_transaction_lifecycle_by_this_pr: false",
        "authorizes_event_commitment_by_this_pr: false",
        "authorizes_resource_math_by_this_pr: false",
        "authorizes_combat_resolution_by_this_pr: false",
        "authorizes_ability_resolution_by_this_pr: false",
        "authorizes_inventory_mutation_by_this_pr: false",
        "authorizes_mission_mutation_by_this_pr: false",
        "authorizes_social_faction_mutation_by_this_pr: false",
        "authorizes_context_packet_compiler_by_this_pr: false",
        "authorizes_prompt_templates_by_this_pr: false",
        "authorizes_model_integration_by_this_pr: false",
        "authorizes_live_play_by_this_pr: false",
        "authorizes_ui_client_by_this_pr: false",
        "authorizes_training_by_this_pr: false",
        "authorizes_pilot_conversion_by_this_pr: false",
        "authorizes_sourcebook_inclusion_by_this_pr: false",
        "authorizes_canon_promotion_by_this_pr: false",
    ]

    @pytest.mark.parametrize("field", DENIAL_FIELDS)
    def test_denial_field(self, plan_text, field):
        assert field in plan_text, f"Missing denial field: {field}"


# ---------------------------------------------------------------------------
# No-implementation claims (forbidden phrases)
# ---------------------------------------------------------------------------


class TestNoImplementationClaims:
    FORBIDDEN_PHRASES = [
        "this PR implements",
        "this PR creates runtime code",
        "this PR creates domain-service code",
        "this PR executes commands",
        "this PR mutates state",
        "this PR commits events",
        "this PR creates a state store",
        "this PR creates a command parser",
        "this PR creates prompt templates",
        "this PR creates model integration",
        "this PR creates a live-play adapter",
        "this PR creates a UI",
        "this PR creates training data",
        "this PR authorizes pilot conversion",
        "this PR authorizes sourcebook inclusion",
        "this PR authorizes canon promotion",
        "this PR creates a database",
        "this PR creates a replay engine",
        "this PR creates a context-packet compiler",
    ]

    @pytest.mark.parametrize("phrase", FORBIDDEN_PHRASES)
    def test_forbidden_phrase_absent(self, plan_text, phrase):
        assert phrase.lower() not in plan_text.lower(), f"Forbidden phrase found: {phrase}"


# ---------------------------------------------------------------------------
# Registry and decision log tracking
# ---------------------------------------------------------------------------


class TestRegistryTracking:
    def test_registry_has_pr_1_entry(self, registry_text):
        assert "RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001" in registry_text


class TestDecisionLogTracking:
    def test_decision_log_has_pr_1_entry(self, decision_log_text):
        assert "RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001" in decision_log_text


# ---------------------------------------------------------------------------
# Runtime guardrails — no premature packages
# ---------------------------------------------------------------------------


class TestRuntimeGuardrails:
    def test_domain_package_contains_only_authorized_modules(self):
        domain_dir = REPO_ROOT / "src" / "astra_runtime" / "domain"
        assert domain_dir.exists(), "Domain package should exist after PR-1A"
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "__pycache__"}
        actual = {p.name for p in domain_dir.iterdir()}
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized domain modules: {unauthorized}"

    def test_no_model_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "model").exists()

    def test_no_prompts_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "prompts").exists()

    def test_no_live_play_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "live_play").exists()

    def test_no_ui_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "ui").exists()

    def test_no_database_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "database").exists()

    def test_no_store_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "store").exists()

    def test_no_context_packet_compiler(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "kernel" / "context_packet_compiler.py").exists()
