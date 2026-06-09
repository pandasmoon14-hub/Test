"""Tests for RUNTIME-DOMAIN-PR-2 state store and state projection service plan."""

import os
import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

PLAN_PATH = (
    REPO_ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_domain_pr_2_state_store_state_projection_service_plan.md"
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
    def test_references_pr_2_id(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-2" in plan_text

    def test_references_pr_2_full_id(self, plan_text):
        assert (
            "RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001"
            in plan_text
        )

    def test_references_pr_1b(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-1B" in plan_text

    def test_references_pr_1a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-1A" in plan_text

    def test_references_pr_1(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-1" in plan_text

    def test_references_pr_0(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-0" in plan_text

    def test_references_impl_pr_8(self, plan_text):
        assert "RUNTIME-IMPL-PR-8" in plan_text


# ── Section 3: Kernel module references ──────────────────────────────────────


class TestKernelModuleReferences:
    @pytest.mark.parametrize(
        "module_name",
        [
            "state_delta",
            "event_ledger",
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


# ── Section 4: RT owner references ──────────────────────────────────────────


class TestRTOwnerReferences:
    @pytest.mark.parametrize(
        "rt_id",
        ["RT-001", "RT-005", "RT-011"],
    )
    def test_references_primary_rt_owner(self, plan_text, rt_id):
        assert rt_id in plan_text, f"Plan must reference {rt_id}"

    def test_references_at_least_one_consumer_rt(self, plan_text):
        consumer_rts = ["RT-002", "RT-003", "RT-004", "RT-006", "RT-007", "RT-008", "RT-010"]
        found = [rt for rt in consumer_rts if rt in plan_text]
        assert len(found) >= 1, "Plan must reference at least one consumer RT owner"

    def test_references_rt_012(self, plan_text):
        assert "RT-012" in plan_text, "Plan must reference RT-012 promotion boundary"


# ── Section 5: Backend-first invariant ───────────────────────────────────────


class TestBackendFirstInvariant:
    def test_states_model_interchangeability(self, plan_text):
        assert "model-interchangeable" in plan_text.lower() or "model interchangeable" in plan_text.lower()

    def test_states_llm_not_game_engine(self, plan_text):
        assert "LLM is not the game engine" in plan_text

    def test_states_backend_owns_truth(self, plan_text):
        assert "backend" in plan_text.lower() and "owns truth" in plan_text.lower()


# ── Section 6: Service ownership ─────────────────────────────────────────────


class TestServiceOwnership:
    def test_includes_service_ownership_heading(self, plan_text):
        assert "Service ownership" in plan_text or "service ownership" in plan_text

    def test_includes_primary_owner(self, plan_text):
        assert "Primary owner" in plan_text or "primary owner" in plan_text


# ── Section 7: Future service responsibilities ───────────────────────────────


class TestFutureServiceResponsibilities:
    def test_includes_allowed_responsibilities(self, plan_text):
        assert "Allowed future responsibilities" in plan_text or "allowed future responsibilities" in plan_text

    def test_includes_forbidden_responsibilities(self, plan_text):
        assert "Forbidden responsibilities" in plan_text or "forbidden responsibilities" in plan_text


# ── Section 8: State ownership model ─────────────────────────────────────────


class TestStateOwnershipModel:
    def test_includes_state_ownership_model(self, plan_text):
        assert "State ownership model" in plan_text

    @pytest.mark.parametrize(
        "category",
        [
            "Authoritative runtime state",
            "Projected state",
            "Visible state",
            "Hidden",
            "Derived state",
            "Cached",
            "Source-local",
            "Canon",
            "Generated content pending provenance",
            "Persisted snapshot boundary",
        ],
    )
    def test_includes_state_category(self, plan_text, category):
        assert category in plan_text, f"State ownership model must include {category}"


# ── Section 9: State projection model ────────────────────────────────────────


class TestStateProjectionModel:
    def test_includes_state_projection_model(self, plan_text):
        assert "State projection model" in plan_text

    @pytest.mark.parametrize(
        "projection_type",
        [
            "Full backend projection",
            "Player-visible projection",
            "Actor-scoped projection",
            "Scene-scoped projection",
            "Combat",
            "Inventory",
            "Mission",
            "Hidden-info redacted projection",
            "Audit",
            "Model-facing projection candidate",
        ],
    )
    def test_includes_projection_type(self, plan_text, projection_type):
        assert projection_type in plan_text, f"Projection model must include {projection_type}"

    def test_pr_2_does_not_authorize_context_packet_compiler(self, plan_text):
        assert "PR-2 does not authorize a context-packet compiler" in plan_text


# ── Section 10: Future state lifecycle model ─────────────────────────────────


class TestFutureStateLifecycleModel:
    def test_includes_lifecycle_heading(self, plan_text):
        assert "Future state lifecycle model" in plan_text or "state lifecycle" in plan_text.lower()

    @pytest.mark.parametrize(
        "stage",
        [
            "registered",
            "loaded_as_reference",
            "projection_requested",
            "projection_validated",
            "projection_materialized",
            "projection_redacted",
            "projection_rejected",
            "mutation_requested",
            "mutation_deferred_to_transaction",
            "event_commit_pending",
            "event_committed_by_future_service",
            "snapshot_prepare_requested",
            "archived_or_superseded",
        ],
    )
    def test_includes_lifecycle_stage(self, plan_text, stage):
        assert stage in plan_text, f"Lifecycle model must include stage {stage}"


# ── Section 11: Kernel interface consumption plan ────────────────────────────


class TestKernelInterfaceConsumptionPlan:
    def test_includes_kernel_consumption_heading(self, plan_text):
        assert (
            "Kernel interface consumption plan" in plan_text
            or "kernel interface consumption" in plan_text.lower()
        )

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
    def test_kernel_module_in_consumption_plan(self, plan_text, module_name):
        assert module_name in plan_text, f"Consumption plan must reference {module_name}"


# ── Section 12: Dependency and handoff boundaries ────────────────────────────


class TestDependencyHandoffBoundaries:
    def test_includes_handoff_heading(self, plan_text):
        assert (
            "Dependency and handoff boundaries" in plan_text
            or "handoff boundaries" in plan_text.lower()
        )


# ── Section 13: Future implementation architecture ───────────────────────────


class TestFutureImplementationArchitecture:
    def test_includes_implementation_architecture(self, plan_text):
        assert "Future implementation architecture" in plan_text

    def test_references_state_store_py(self, plan_text):
        assert "state_store.py" in plan_text

    def test_references_state_projection_py(self, plan_text):
        assert "state_projection.py" in plan_text

    def test_proposed_symbols_not_created(self, plan_text):
        assert "proposed future symbols only" in plan_text.lower() or "must not be created in PR-2" in plan_text


# ── Section 14: Future data shapes ───────────────────────────────────────────


class TestFutureDataShapes:
    def test_includes_data_shapes_heading(self, plan_text):
        assert "Future data shapes" in plan_text or "data shape" in plan_text.lower()

    @pytest.mark.parametrize(
        "shape",
        [
            "State record reference",
            "State snapshot reference",
            "State projection request",
            "State projection result",
            "State visibility descriptor",
            "State projection dependency declaration",
            "projection rejection",
        ],
    )
    def test_includes_data_shape(self, plan_text, shape):
        assert shape in plan_text, f"Data shapes must include {shape}"


# ── Section 15: Implementation PR authorization boundary ─────────────────────


class TestImplementationPRAuthorizationBoundary:
    def test_includes_authorization_boundary(self, plan_text):
        assert (
            "Implementation PR authorization boundary" in plan_text
            or "authorization boundary" in plan_text.lower()
        )

    def test_recommends_pr_2a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-2A" in plan_text


# ── Section 16: Test requirements ────────────────────────────────────────────


class TestTestRequirements:
    def test_includes_test_requirements_heading(self, plan_text):
        assert "Test requirements" in plan_text or "test requirements" in plan_text.lower()


# ── Section 17: Corpus-scale state pressure review ───────────────────────────


class TestCorpusScaleStatePressureReview:
    def test_includes_corpus_scale_heading(self, plan_text):
        assert "Corpus-scale state pressure review" in plan_text or "corpus-scale" in plan_text.lower()


# ── Section 18: Guardrail review ────────────────────────────────────────────


class TestGuardrailReview:
    def test_includes_guardrail_review(self, plan_text):
        assert "Guardrail review" in plan_text


# ── Section 19: Risk review ─────────────────────────────────────────────────


class TestRiskReview:
    def test_includes_risk_review(self, plan_text):
        assert "Risk review" in plan_text

    @pytest.mark.parametrize(
        "risk_keyword",
        [
            "god object",
            "hidden-info leak",
            "authoritative state",
            "applying deltas",
            "commits events",
            "bypasses validation",
            "persistence",
            "runtime trace",
            "generated content",
            "model summaries",
        ],
    )
    def test_includes_risk_category(self, plan_text, risk_keyword):
        assert risk_keyword.lower() in plan_text.lower(), f"Risk review must address: {risk_keyword}"


# ── Section 20: Future hardening ledger ──────────────────────────────────────


class TestFutureHardeningLedger:
    def test_includes_hardening_ledger(self, plan_text):
        assert "hardening ledger" in plan_text.lower() or "future hardening" in plan_text.lower()


# ── Section 21: Non-implementation reaffirmation ─────────────────────────────


class TestNonImplementationReaffirmation:
    def test_includes_non_implementation_reaffirmation(self, plan_text):
        assert "Non-implementation reaffirmation" in plan_text or "non-implementation" in plan_text.lower()


# ── Section 22: Gate finding ─────────────────────────────────────────────────


class TestGateFinding:
    def test_includes_gate_finding(self, plan_text):
        assert "gate_finding" in plan_text

    @pytest.mark.parametrize(
        "gate_field",
        [
            "state_store_state_projection_plan_defined: true",
            "ready_for_state_store_state_projection_skeleton_implementation_pr: true",
            "state_store_code_authorized_by_this_pr: false",
            "state_projection_code_authorized_by_this_pr: false",
            "state_mutation_authorized_by_this_pr: false",
            "state_delta_application_authorized_by_this_pr: false",
            "transaction_lifecycle_authorized_by_this_pr: false",
            "event_commitment_authorized_by_this_pr: false",
            "durable_persistence_authorized_by_this_pr: false",
            "replay_engine_authorized_by_this_pr: false",
            "command_execution_authorized_by_this_pr: false",
            "resource_math_authorized_by_this_pr: false",
            "combat_resolution_authorized_by_this_pr: false",
            "model_integration_authorized_by_this_pr: false",
            "live_play_authorized_by_this_pr: false",
            "conversion_authorized_by_this_pr: false",
        ],
    )
    def test_gate_field_present(self, plan_text, gate_field):
        assert gate_field in plan_text, f"Gate finding must include: {gate_field}"

    def test_gate_next_step(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-2A" in plan_text


# ── Section 23: Classification block ────────────────────────────────────────


class TestClassificationBlock:
    def test_includes_classification_block(self, plan_text):
        assert "runtime_domain_pr_2:" in plan_text

    def test_classification_review_id(self, plan_text):
        assert (
            "RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001"
            in plan_text
        )

    def test_classification_artifact_type(self, plan_text):
        assert "state_store_state_projection_service_plan" in plan_text

    def test_classification_non_executable(self, plan_text):
        assert "non_executable_plan" in plan_text

    @pytest.mark.parametrize(
        "field_value",
        [
            "defines_state_ownership_model: true",
            "defines_state_projection_model: true",
            "defines_state_lifecycle_model: true",
            "defines_kernel_interface_consumption_plan: true",
            "defines_handoff_boundaries: true",
            "defines_future_implementation_architecture: true",
            "defines_future_data_shapes: true",
            "defines_future_test_requirements: true",
            "defines_corpus_scale_state_pressure_review: true",
            "defines_future_hardening_ledger: true",
            "authorizes_state_store_code_by_this_pr: false",
            "authorizes_state_projection_code_by_this_pr: false",
            "authorizes_mutable_runtime_state_by_this_pr: false",
            "authorizes_state_mutation_by_this_pr: false",
            "authorizes_model_integration_by_this_pr: false",
            "authorizes_canon_promotion_by_this_pr: false",
        ],
    )
    def test_classification_field(self, plan_text, field_value):
        assert field_value in plan_text, f"Classification must include: {field_value}"


# ── Section 24: No-implementation claims ─────────────────────────────────────


class TestNoImplementationClaims:
    @pytest.mark.parametrize(
        "forbidden_claim",
        [
            "implements state-store code",
            "implements state-projection code",
            "implements mutable runtime state",
            "implements state mutation",
            "implements state delta application",
            "implements transaction lifecycle",
            "implements event commitment",
            "implements durable persistence",
            "implements database schema",
            "implements replay engine",
            "implements command execution",
            "implements resource math",
            "implements combat",
            "implements abilities",
            "implements inventory",
            "implements mission",
            "implements context-packet compiler",
            "implements prompts",
            "implements model integration",
            "implements live play",
            "implements UI",
            "implements training",
            "implements pilot conversion",
            "implements sourcebook inclusion",
            "implements canon promotion",
        ],
    )
    def test_plan_does_not_claim_implementation(self, plan_text, forbidden_claim):
        assert forbidden_claim not in plan_text.lower(), (
            f"Plan must not claim: {forbidden_claim}"
        )


# ── Section 25: Registry tracking ───────────────────────────────────────────


class TestRegistryTracking:
    def test_registry_references_pr_2(self, registry_text):
        assert (
            "RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001"
            in registry_text
        )


# ── Section 26: Decision log tracking ───────────────────────────────────────


class TestDecisionLogTracking:
    def test_decision_log_references_pr_2(self, decision_log_text):
        assert (
            "RUNTIME-DOMAIN-PR-2" in decision_log_text
            and "state store" in decision_log_text.lower()
        )


# ── Section 27: Runtime guardrail tests — domain package contents ────────────


class TestDomainPackageGuardrails:
    def test_domain_package_exists(self):
        assert DOMAIN_PACKAGE_DIR.exists(), "Domain package must exist"

    def test_domain_package_contains_init(self):
        assert (DOMAIN_PACKAGE_DIR / "__init__.py").exists()

    def test_domain_package_contains_command_lifecycle(self):
        assert (DOMAIN_PACKAGE_DIR / "command_lifecycle.py").exists()

    def test_domain_package_contains_action_legality(self):
        assert (DOMAIN_PACKAGE_DIR / "action_legality.py").exists()

    def test_domain_package_authorized_files_only(self):
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "__pycache__"}
        actual = {p.name for p in DOMAIN_PACKAGE_DIR.iterdir() if p.name != "__pycache__"}
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized files in domain package: {unauthorized}"

    @pytest.mark.parametrize(
        "forbidden_file",
        [
            "transaction_lifecycle.py",
            "event_commitment.py",
            "validation_integration.py",
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
