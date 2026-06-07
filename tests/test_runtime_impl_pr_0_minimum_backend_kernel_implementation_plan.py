"""Tests for RUNTIME-IMPL-PR-0 minimum backend kernel executable implementation plan."""

import os
import pathlib

PLAN_PATH = pathlib.Path(__file__).resolve().parent.parent / (
    "docs/doctrine/reviews/"
    "runtime_impl_pr_0_minimum_backend_kernel_executable_implementation_plan.md"
)

REGISTRY_PATH = pathlib.Path(__file__).resolve().parent.parent / (
    "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
)

DECISIONS_PATH = pathlib.Path(__file__).resolve().parent.parent / (
    "docs/decisions/current_decisions_log.md"
)


def _read_plan():
    return PLAN_PATH.read_text(encoding="utf-8")


def _read_registry():
    return REGISTRY_PATH.read_text(encoding="utf-8")


def _read_decisions():
    return DECISIONS_PATH.read_text(encoding="utf-8")


# --- File presence ---

def test_plan_file_exists():
    assert PLAN_PATH.exists(), f"Plan file missing: {PLAN_PATH}"


# --- Core ID references ---

def test_references_pr0_id():
    content = _read_plan()
    assert "RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001" in content


def test_references_pr_f():
    content = _read_plan()
    assert "RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001" in content


def test_references_pr_a_through_e():
    content = _read_plan()
    assert "RUNTIME-SEQ-PR-A" in content
    assert "RUNTIME-SEQ-PR-B" in content
    assert "RUNTIME-SEQ-PR-C" in content
    assert "RUNTIME-SEQ-PR-D" in content
    assert "RUNTIME-SEQ-PR-E" in content


def test_references_rt_001_through_012():
    content = _read_plan()
    for i in range(1, 13):
        tag = f"RT-{i:03d}"
        assert tag in content, f"Missing reference to {tag}"


# --- Invariant language ---

def test_states_backend_first_invariant():
    content = _read_plan()
    assert "model-interchangeable" in content
    assert "backend runtime kernel owns truth" in content


def test_states_llm_not_game_engine():
    content = _read_plan()
    assert "LLM is not the game engine" in content


# --- Required sections ---

def test_includes_implementation_stack_decision():
    content = _read_plan()
    assert "## 4. Implementation stack decision" in content


def test_includes_minimum_backend_kernel_target():
    content = _read_plan()
    assert "## 5. Minimum backend kernel implementation target" in content


def test_includes_proposed_package_layout():
    content = _read_plan()
    assert "## 6. Proposed package/module layout" in content
    assert "src/astra_runtime/" in content


def test_includes_interface_boundary_plan():
    content = _read_plan()
    assert "## 7. Interface boundary plan" in content
    assert "SchemaRegistryInterface" in content
    assert "CommandEnvelopeInterface" in content
    assert "EventLedgerInterface" in content
    assert "HiddenInformationPartitionInterface" in content
    assert "PersistenceBoundaryInterface" in content


def test_includes_pr_sequence_1_through_8():
    content = _read_plan()
    assert "## 8. RUNTIME-IMPL-PR sequence" in content
    assert "RUNTIME-IMPL-PR-1" in content
    assert "RUNTIME-IMPL-PR-2" in content
    assert "RUNTIME-IMPL-PR-3" in content
    assert "RUNTIME-IMPL-PR-4" in content
    assert "RUNTIME-IMPL-PR-5" in content
    assert "RUNTIME-IMPL-PR-6" in content
    assert "RUNTIME-IMPL-PR-7" in content
    assert "RUNTIME-IMPL-PR-8" in content


def test_includes_pr1_authorization_boundary():
    content = _read_plan()
    assert "## 9. RUNTIME-IMPL-PR-1 authorization boundary" in content


def test_includes_kernel_skeleton_invariants():
    content = _read_plan()
    assert "## 10. Kernel skeleton invariants" in content
    assert "No LLM state authority" in content


def test_includes_storage_neutral_persistence_plan():
    content = _read_plan()
    assert "## 11. Storage-neutral persistence plan" in content
    assert "storage-neutral" in content


def test_includes_testing_strategy():
    content = _read_plan()
    assert "## 12. Testing strategy" in content


def test_includes_implementation_risk_controls():
    content = _read_plan()
    assert "## 13. Implementation risk controls" in content


def test_includes_documentation_and_registry_alignment():
    content = _read_plan()
    assert "## 14. Documentation and registry alignment" in content


def test_includes_blocked_until_ledger():
    content = _read_plan()
    assert "## 15. Blocked-until ledger" in content
    assert "RUNTIME-IMPL-PR-1 or later" in content


def test_recommends_pr1():
    content = _read_plan()
    assert "## 16. Next recommended PR" in content
    assert "RUNTIME-IMPL-PR-1" in content
    assert "Schema Registry and Record Identity Skeleton" in content


def test_includes_non_implementation_reaffirmation():
    content = _read_plan()
    assert "## 17. Non-implementation reaffirmation" in content


def test_includes_classification_block():
    content = _read_plan()
    assert "## 18. Classification block" in content
    assert "non_executable_plan" in content
    assert "authorizes_code_implementation_by_this_pr: false" in content
    assert "authorizes_runtime_implementation_by_this_pr: false" in content


# --- Representative proposed paths ---

def test_proposed_paths_present():
    content = _read_plan()
    assert "src/astra_runtime/kernel/schema_registry.py" in content
    assert "src/astra_runtime/kernel/record_identity.py" in content
    assert "src/astra_runtime/kernel/command_envelope.py" in content
    assert "src/astra_runtime/kernel/event_ledger.py" in content
    assert "src/astra_runtime/kernel/rng_interface.py" in content
    assert "src/astra_runtime/kernel/persistence_boundary.py" in content
    assert "tests/runtime/test_schema_registry_skeleton.py" in content


# --- Representative blocked statuses ---

def test_blocked_statuses():
    content = _read_plan()
    assert "Domain services" in content and "Post-kernel review" in content
    assert "Canon promotion" in content and "Canon governance exists" in content


# --- Registry tracking ---

def test_registry_tracking_exists():
    content = _read_registry()
    assert "RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001" in content


# --- Decision log tracking ---

def test_decision_log_tracking_exists():
    content = _read_decisions()
    assert "RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001" in content


# --- No-implementation guardrail ---

def test_no_runtime_code_created():
    runtime_src = PLAN_PATH.parent.parent.parent.parent / "src" / "astra_runtime"
    assert not runtime_src.exists(), (
        f"src/astra_runtime/ must not exist in this PR: {runtime_src}"
    )


def test_plan_does_not_claim_implementation():
    content = _read_plan()
    forbidden_claims = [
        "implements runtime code",
        "implements schema",
        "implements command IR",
        "implements validators",
        "implements generators",
        "implements state store",
        "implements state delta",
        "implements event ledger",
        "implements transaction system",
        "implements invariant validator",
        "implements correction event",
        "implements deterministic RNG",
        "implements table/oracle",
        "implements persistence writer",
        "implements database schema",
        "implements context-packet compiler",
        "implements redaction algorithm",
        "implements hidden-state database",
        "implements domain service",
        "implements model evaluation",
        "implements benchmark runner",
        "implements prompt template",
        "implements live-play adapter",
        "implements training",
        "authorizes pilot conversion",
        "authorizes sourcebook inclusion",
        "authorizes canon promotion",
    ]
    for claim in forbidden_claims:
        assert claim not in content.lower(), f"Plan must not claim: {claim}"
