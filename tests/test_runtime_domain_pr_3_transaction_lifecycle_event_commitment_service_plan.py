"""Tests for RUNTIME-DOMAIN-PR-3 transaction lifecycle and event commitment service plan."""

import os
import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

PLAN_PATH = (
    REPO_ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan.md"
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
    def test_references_pr_3_id(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-3" in plan_text

    def test_references_pr_3_full_id(self, plan_text):
        assert (
            "RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001"
            in plan_text
        )

    def test_references_pr_2b(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-2B" in plan_text

    def test_references_pr_2a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-2A" in plan_text

    def test_references_pr_2(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-2" in plan_text

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
            "transaction_preview",
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


# ── Section 4: Domain module references ──────────────────────────────────────

class TestDomainModuleReferences:
    @pytest.mark.parametrize(
        "module_ref",
        [
            "command_lifecycle",
            "action_legality",
            "state_store.py",
            "state_projection.py",
        ],
    )
    def test_references_domain_module(self, plan_text, module_ref):
        assert module_ref in plan_text, f"Plan must reference domain module {module_ref}"


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

    def test_includes_primary_ownership(self, plan_text):
        assert "Primary ownership" in plan_text or "primary ownership" in plan_text

    def test_includes_transaction_boundary(self, plan_text):
        assert "transaction boundary" in plan_text.lower()

    def test_includes_event_commitment_boundary(self, plan_text):
        assert "event commitment boundary" in plan_text.lower()


# ── Section 7: Future service responsibilities ───────────────────────────────

class TestFutureServiceResponsibilities:
    def test_includes_allowed_responsibilities(self, plan_text):
        assert "Allowed future responsibilities" in plan_text or "allowed future responsibilities" in plan_text

    def test_includes_forbidden_responsibilities(self, plan_text):
        assert "Forbidden responsibilities" in plan_text or "forbidden responsibilities" in plan_text


# ── Section 8: Transaction lifecycle model ───────────────────────────────────

class TestTransactionLifecycleModel:
    def test_includes_lifecycle_model_heading(self, plan_text):
        assert "Transaction lifecycle model" in plan_text

    @pytest.mark.parametrize(
        "stage",
        [
            "transaction_requested",
            "command_reference_bound",
            "actor_reference_bound",
            "state_projection_bound",
            "dependencies_declared",
            "preconditions_declared",
            "domain_resolution_required",
            "proposed_delta_referenced",
            "validation_requested",
            "validation_passed",
            "validation_failed",
            "ready_for_event_commitment",
            "commitment_requested",
            "committed",
            "rejected",
            "quarantined",
            "cancelled",
            "superseded",
        ],
    )
    def test_includes_lifecycle_stage(self, plan_text, stage):
        assert stage in plan_text, f"Transaction lifecycle model must include stage {stage}"


# ── Section 9: Event commitment model ────────────────────────────────────────

class TestEventCommitmentModel:
    def test_includes_event_commitment_heading(self, plan_text):
        assert "Event commitment model" in plan_text

    @pytest.mark.parametrize(
        "decision",
        [
            "commit_ready",
            "committed",
            "rejected_by_validation",
            "rejected_by_scope",
            "rejected_by_missing_state_reference",
            "rejected_by_missing_delta_reference",
            "rejected_by_hidden_information_risk",
            "rejected_by_idempotency_conflict",
            "rejected_by_persistence_boundary",
            "quarantined_for_audit",
            "cancelled_before_commit",
            "unsupported_event_type",
        ],
    )
    def test_includes_commitment_decision(self, plan_text, decision):
        assert decision in plan_text, f"Event commitment model must include decision {decision}"


# ── Section 10: Transaction vs event boundary ────────────────────────────────

class TestTransactionVsEventBoundary:
    def test_includes_boundary_heading(self, plan_text):
        assert "Transaction vs event boundary" in plan_text or "transaction vs event" in plan_text.lower()

    def test_distinguishes_transaction_lifecycle(self, plan_text):
        lower = plan_text.lower()
        assert "does not mutate state" in lower

    def test_distinguishes_event_commitment(self, plan_text):
        lower = plan_text.lower()
        assert "append-only" in lower


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


# ── Section 12: Domain service handoff boundaries ────────────────────────────

class TestDomainServiceHandoffBoundaries:
    def test_includes_handoff_heading(self, plan_text):
        assert (
            "Domain service handoff boundaries" in plan_text
            or "handoff boundaries" in plan_text.lower()
        )

    @pytest.mark.parametrize(
        "service_ref",
        [
            "command lifecycle",
            "action legality",
            "state store",
            "state projection",
            "validation pipeline",
            "persistence boundary",
        ],
    )
    def test_references_handoff_service(self, plan_text, service_ref):
        assert service_ref.lower() in plan_text.lower(), f"Handoff section must reference {service_ref}"


# ── Section 13: Future implementation architecture ───────────────────────────

class TestFutureImplementationArchitecture:
    def test_includes_implementation_architecture(self, plan_text):
        assert "Future implementation architecture" in plan_text

    def test_references_transaction_lifecycle_py(self, plan_text):
        assert "transaction_lifecycle.py" in plan_text

    def test_references_event_commitment_py(self, plan_text):
        assert "event_commitment.py" in plan_text

    def test_proposed_symbols_not_created(self, plan_text):
        assert "proposed future symbols only" in plan_text.lower() or "must not be created in PR-3" in plan_text


# ── Section 14: Future data shapes ───────────────────────────────────────────

class TestFutureDataShapes:
    def test_includes_data_shapes_heading(self, plan_text):
        assert "Future data shapes" in plan_text or "data shape" in plan_text.lower()

    @pytest.mark.parametrize(
        "shape",
        [
            "TransactionDependency",
            "TransactionPrecondition",
            "TransactionRequest",
            "TransactionPlan",
            "TransactionResult",
            "EventCommitmentRequest",
            "EventCommitmentResult",
        ],
    )
    def test_includes_data_shape(self, plan_text, shape):
        assert shape in plan_text, f"Data shapes must include {shape}"


# ── Section 15: Commit-readiness invariants ──────────────────────────────────

class TestCommitReadinessInvariants:
    def test_includes_invariants_heading(self, plan_text):
        assert "Commit-readiness invariants" in plan_text or "commit-readiness" in plan_text.lower()

    @pytest.mark.parametrize(
        "invariant_keyword",
        [
            "accepted command reference",
            "actor reference",
            "validation reference",
            "model text",
            "narration",
            "hidden information",
            "deterministic",
            "replay",
        ],
    )
    def test_includes_invariant(self, plan_text, invariant_keyword):
        assert invariant_keyword.lower() in plan_text.lower(), f"Invariants must address: {invariant_keyword}"


# ── Section 16: Corpus-scale transaction pressure review ─────────────────────

class TestCorpusScaleTransactionPressureReview:
    def test_includes_corpus_scale_heading(self, plan_text):
        assert "Corpus-scale transaction pressure review" in plan_text or "corpus-scale" in plan_text.lower()

    @pytest.mark.parametrize(
        "pressure_category",
        [
            "player actions",
            "combat",
            "inventory",
            "mission",
            "faction",
            "hazard",
        ],
    )
    def test_includes_pressure_category(self, plan_text, pressure_category):
        assert pressure_category.lower() in plan_text.lower(), f"Pressure review must address: {pressure_category}"


# ── Section 17: Risk review ──────────────────────────────────────────────────

class TestRiskReview:
    def test_includes_risk_review(self, plan_text):
        assert "Risk review" in plan_text

    @pytest.mark.parametrize(
        "risk_keyword",
        [
            "universal rule engine",
            "bypasses validation",
            "mutates state",
            "hidden information",
            "narration",
            "donor mechanics",
            "non-deterministic",
            "persistence",
        ],
    )
    def test_includes_risk_category(self, plan_text, risk_keyword):
        assert risk_keyword.lower() in plan_text.lower(), f"Risk review must address: {risk_keyword}"


# ── Section 18: Future hardening ledger ──────────────────────────────────────

class TestFutureHardeningLedger:
    def test_includes_hardening_ledger(self, plan_text):
        assert "hardening ledger" in plan_text.lower() or "future hardening" in plan_text.lower()


# ── Section 19: Implementation PR authorization boundary ─────────────────────

class TestImplementationPRAuthorizationBoundary:
    def test_includes_authorization_boundary(self, plan_text):
        assert (
            "Implementation PR authorization boundary" in plan_text
            or "authorization boundary" in plan_text.lower()
        )

    def test_recommends_pr_3a(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-3A" in plan_text


# ── Section 20: Future implementation test requirements ──────────────────────

class TestFutureImplementationTestRequirements:
    def test_includes_test_requirements_heading(self, plan_text):
        assert "test requirements" in plan_text.lower()


# ── Section 21: Gate finding ─────────────────────────────────────────────────

class TestGateFinding:
    def test_includes_gate_finding(self, plan_text):
        assert "gate_finding" in plan_text

    @pytest.mark.parametrize(
        "gate_field",
        [
            "transaction_lifecycle_event_commitment_plan_defined: true",
            "ready_for_transaction_lifecycle_event_commitment_skeleton_implementation_pr: true",
            "transaction_lifecycle_code_authorized_by_this_pr: false",
            "event_commitment_code_authorized_by_this_pr: false",
            "event_sourcing_authorized_by_this_pr: false",
            "mutable_runtime_state_authorized_by_this_pr: false",
            "state_mutation_authorized_by_this_pr: false",
            "state_delta_application_authorized_by_this_pr: false",
            "event_ledger_append_authorized_by_this_pr: false",
            "durable_persistence_authorized_by_this_pr: false",
            "database_schema_authorized_by_this_pr: false",
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
        ],
    )
    def test_gate_field_present(self, plan_text, gate_field):
        assert gate_field in plan_text, f"Gate finding must include: {gate_field}"

    def test_gate_next_step(self, plan_text):
        assert "RUNTIME-DOMAIN-PR-3A" in plan_text


# ── Section 22: Classification block ─────────────────────────────────────────

class TestClassificationBlock:
    def test_includes_classification_block(self, plan_text):
        assert "runtime_domain_pr_3:" in plan_text

    def test_classification_plan_id(self, plan_text):
        assert (
            "RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001"
            in plan_text
        )

    def test_classification_artifact_type(self, plan_text):
        assert "transaction_lifecycle_event_commitment_service_plan" in plan_text

    def test_classification_non_executable(self, plan_text):
        assert "non_executable_plan" in plan_text

    @pytest.mark.parametrize(
        "field_value",
        [
            "defines_transaction_lifecycle_model: true",
            "defines_event_commitment_model: true",
            "defines_transaction_event_boundary: true",
            "defines_kernel_interface_consumption_plan: true",
            "defines_domain_service_handoffs: true",
            "defines_future_implementation_architecture: true",
            "defines_future_data_shapes: true",
            "defines_commit_readiness_invariants: true",
            "defines_corpus_scale_transaction_pressure_review: true",
            "defines_future_hardening_ledger: true",
            "authorizes_transaction_lifecycle_code_by_this_pr: false",
            "authorizes_event_commitment_code_by_this_pr: false",
            "authorizes_event_sourcing_by_this_pr: false",
            "authorizes_mutable_runtime_state_by_this_pr: false",
            "authorizes_state_mutation_by_this_pr: false",
            "authorizes_model_integration_by_this_pr: false",
            "authorizes_canon_promotion_by_this_pr: false",
        ],
    )
    def test_classification_field(self, plan_text, field_value):
        assert field_value in plan_text, f"Classification must include: {field_value}"


# ── Section 23: Non-implementation reaffirmation ─────────────────────────────

class TestNonImplementationReaffirmation:
    def test_includes_non_implementation_reaffirmation(self, plan_text):
        assert "Non-implementation reaffirmation" in plan_text or "non-implementation" in plan_text.lower()


# ── Section 24: No-implementation claims ─────────────────────────────────────

class TestNoImplementationClaims:
    @pytest.mark.parametrize(
        "forbidden_claim",
        [
            "implements transaction lifecycle code",
            "implements event commitment code",
            "implements event sourcing",
            "implements mutable runtime state",
            "implements state mutation",
            "implements delta application",
            "implements event ledger append",
            "implements durable persistence",
            "implements database schema",
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
            "implements training data",
            "implements canon promotion",
        ],
    )
    def test_plan_does_not_claim_implementation(self, plan_text, forbidden_claim):
        assert forbidden_claim not in plan_text.lower(), (
            f"Plan must not claim: {forbidden_claim}"
        )


# ── Section 25: Registry tracking ────────────────────────────────────────────

class TestRegistryTracking:
    def test_registry_references_pr_3(self, registry_text):
        assert (
            "RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001"
            in registry_text
        )


# ── Section 26: Decision log tracking ────────────────────────────────────────

class TestDecisionLogTracking:
    def test_decision_log_references_pr_3(self, decision_log_text):
        assert (
            "RUNTIME-DOMAIN-PR-3" in decision_log_text
            and "transaction lifecycle" in decision_log_text.lower()
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

    def test_domain_package_contains_state_store(self):
        assert (DOMAIN_PACKAGE_DIR / "state_store.py").exists()

    def test_domain_package_contains_state_projection(self):
        assert (DOMAIN_PACKAGE_DIR / "state_projection.py").exists()

    def test_domain_package_authorized_files_only(self):
        allowed = {
            "__init__.py", "command_lifecycle.py", "action_legality.py",
            "state_store.py", "state_projection.py",
            "transaction_lifecycle.py", "event_commitment.py",
            "validation_integration.py",
            "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py",
            "__pycache__",
        }
        actual = {p.name for p in DOMAIN_PACKAGE_DIR.iterdir() if p.name != "__pycache__"}
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized files in domain package: {unauthorized}"

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
        assert not (DOMAIN_PACKAGE_DIR / forbidden_file).exists(), (
            f"Unauthorized domain module must not exist: {forbidden_file}"
        )


class TestRegistryFileRecordTracking:
    def test_registry_has_pr3_file_id(self, registry_text):
        assert "file_id: RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001" in registry_text

    def test_registry_pr3_file_id_unique(self, registry_text):
        count = registry_text.count("file_id: RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001")
        assert count == 1, f"Expected file_id exactly once, found {count} times"

    def test_registry_pr3_content_type(self, registry_text):
        assert "content_type: service_plan" in registry_text

    def test_registry_pr3_implementation_status(self, registry_text):
        assert "implementation_status: non_executable_plan" in registry_text

    def test_registry_pr3_denies_transaction_lifecycle_code(self, registry_text):
        assert "authorizes_transaction_lifecycle_code_by_this_pr: false" in registry_text

    def test_registry_pr3_denies_event_commitment_code(self, registry_text):
        assert "authorizes_event_commitment_code_by_this_pr: false" in registry_text

    def test_registry_pr3_denies_event_ledger_append(self, registry_text):
        assert "authorizes_event_ledger_append_by_this_pr: false" in registry_text

    def test_registry_pr3_next_allowed_step(self, registry_text):
        assert "next_allowed_step: RUNTIME-DOMAIN-PR-3A transaction lifecycle and event commitment skeleton implementation, pending review" in registry_text


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
