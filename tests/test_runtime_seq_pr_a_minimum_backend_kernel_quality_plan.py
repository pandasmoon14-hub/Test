"""Tests for RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001."""

import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

PLAN_PATH = REPO_ROOT / "docs" / "doctrine" / "reviews" / "runtime_seq_pr_a_minimum_backend_kernel_runtime_quality_contract_plan.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISIONS_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"


@pytest.fixture(scope="module")
def plan_text():
    return PLAN_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def registry_text():
    return REGISTRY_PATH.read_text(encoding="utf-8-sig")


@pytest.fixture(scope="module")
def decisions_text():
    return DECISIONS_PATH.read_text(encoding="utf-8")


# --- File existence ---

def test_plan_file_exists():
    assert PLAN_PATH.is_file(), f"Plan file missing: {PLAN_PATH}"


# --- Review ID ---

def test_references_review_id(plan_text):
    assert "RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001" in plan_text


# --- Derives from sequencing review ---

def test_references_sequencing_review(plan_text):
    assert "RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001" in plan_text


# --- RT-001 through RT-012 ---

@pytest.mark.parametrize("rt_id", [f"RT-{str(i).zfill(3)}" for i in range(1, 13)])
def test_references_rt_owner_specs(plan_text, rt_id):
    assert rt_id in plan_text, f"Plan must reference {rt_id}"


# --- Backend-first / model-interchangeability invariant ---

def test_references_backend_first_invariant(plan_text):
    assert "model-interchangeable" in plan_text.lower() or "model interchangeable" in plan_text.lower()


def test_llm_is_not_game_engine(plan_text):
    assert "LLM is not the game engine" in plan_text


# --- Minimum backend kernel spine ---

KERNEL_SPINE_CONTRACTS = [
    "SchemaRegistryContract",
    "RecordIdentityContract",
    "CommandIREnvelope",
    "CommandLifecycleContract",
    "TransactionPreviewContract",
    "StateStoreContract",
    "StateDeltaEnvelope",
    "EventLedgerEnvelope",
    "DeterministicRNGInterface",
    "TableOracleInvocationInterface",
    "ValidationPipelineInterface",
    "ContextProjectionBoundary",
    "HiddenInformationPartitionContract",
    "PersistenceBoundaryContract",
    "ReplayHashAuditContract",
    "RuntimeTraceContract",
]


def test_includes_minimum_backend_kernel_spine(plan_text):
    assert "Minimum backend kernel spine" in plan_text


@pytest.mark.parametrize("contract", KERNEL_SPINE_CONTRACTS)
def test_kernel_spine_contract_present(plan_text, contract):
    assert contract in plan_text, f"Kernel spine must include {contract}"


# --- Runtime-quality contract layer ---

QUALITY_CONTRACTS = [
    "NarrationRenderPacketContract",
    "NarratorOutputContract",
    "PacketBudgetPolicy",
    "SoftStateMutationDetectionContract",
    "CanonicalSilencePolicy",
    "WorldInvariantRegistry",
    "CorrectionEventProtocol",
    "SessionTraceObservabilityContract",
    "AdversarialPlayerCommandCorpus",
    "MetamorphicRuntimeTestPlan",
    "ModelBehaviorFingerprint",
    "TruncationSafeStructuredOutputPolicy",
    "SchemaKeyBehaviorEvaluationPolicy",
    "SourceLocalCapsuleBoundary",
    "StoryCapableStructurePrinciple",
]


def test_includes_runtime_quality_contract_layer(plan_text):
    assert "Runtime-quality contract layer" in plan_text or "runtime-quality contract layer" in plan_text


@pytest.mark.parametrize("contract", QUALITY_CONTRACTS)
def test_quality_contract_present(plan_text, contract):
    assert contract in plan_text, f"Quality layer must include {contract}"


# --- Local 8B reliability requirements ---

def test_includes_local_8b_reliability_requirements(plan_text):
    assert "Local 8B reliability" in plan_text or "local 8B reliability" in plan_text


def test_8b_bounded_packets(plan_text):
    assert "bounded" in plan_text.lower() and "packet" in plan_text.lower()


def test_8b_no_dice(plan_text):
    assert "does not roll dice" in plan_text.lower() or "not roll dice" in plan_text.lower()


# --- Transaction preview and correction policy ---

def test_includes_transaction_preview_and_correction(plan_text):
    assert "Transaction preview and correction" in plan_text or "transaction preview and correction" in plan_text


def test_narration_is_never_commitment(plan_text):
    assert "Narration is never commitment" in plan_text or "narration is never commitment" in plan_text


def test_correction_events_append_only(plan_text):
    assert "append-only" in plan_text


# --- World invariant and canonical silence ---

def test_includes_world_invariant_requirements(plan_text):
    assert "WorldInvariantRegistry" in plan_text


def test_includes_canonical_silence_requirements(plan_text):
    assert "CanonicalSilencePolicy" in plan_text


# --- Observability and replay/debug ---

def test_includes_observability_requirements(plan_text):
    assert "Observability and replay" in plan_text or "observability and replay" in plan_text


def test_replay_hash_reference(plan_text):
    assert "replay" in plan_text.lower() and "hash" in plan_text.lower()


# --- Minimum backend kernel target boundary ---

def test_includes_kernel_target_boundary(plan_text):
    assert "Minimum backend kernel target boundary" in plan_text or "minimum backend kernel target boundary" in plan_text


# --- Implementation wave alignment ---

def test_includes_implementation_wave_alignment(plan_text):
    assert "Implementation wave alignment" in plan_text or "implementation wave alignment" in plan_text


def test_wave_0_through_wave_6(plan_text):
    for wave_num in range(7):
        assert f"Wave {wave_num}" in plan_text, f"Plan must reference Wave {wave_num}"


def test_does_not_start_wave_7(plan_text):
    assert "does not start" in plan_text.lower() and "Wave 7" in plan_text


# --- Blocked-until ledger ---

def test_includes_blocked_until_ledger(plan_text):
    assert "Blocked-until ledger" in plan_text or "blocked-until ledger" in plan_text


BLOCKED_ITEMS = [
    "Runtime implementation",
    "Schema implementation",
    "Command IR implementation",
    "Validator implementation",
    "Generator implementation",
    "State store",
    "Event ledger",
    "Deterministic RNG service",
    "Persistence writer",
    "Context-packet compiler",
    "Domain services",
    "Live-play adapter",
    "Training",
    "Canon promotion",
]


@pytest.mark.parametrize("item", BLOCKED_ITEMS)
def test_blocked_item_present(plan_text, item):
    assert item in plan_text, f"Blocked-until ledger must include {item}"


# --- Next recommended planning PRs ---

@pytest.mark.parametrize("pr_id", [
    "RUNTIME-SEQ-PR-B",
    "RUNTIME-SEQ-PR-C",
    "RUNTIME-SEQ-PR-D",
    "RUNTIME-SEQ-PR-E",
])
def test_recommends_follow_up_prs(plan_text, pr_id):
    assert pr_id in plan_text, f"Plan must recommend {pr_id}"


# --- Non-implementation reaffirmation ---

def test_includes_non_implementation_reaffirmation(plan_text):
    assert "Non-implementation reaffirmation" in plan_text or "non-implementation reaffirmation" in plan_text


# --- Classification block ---

def test_includes_classification_block(plan_text):
    assert "runtime_seq_pr_a:" in plan_text
    assert "non_executable_planning" in plan_text
    assert "confirms_backend_first_invariant: true" in plan_text
    assert "confirms_llm_is_not_game_engine: true" in plan_text
    assert "defines_minimum_kernel_spine: true" in plan_text
    assert "defines_runtime_quality_contract_layer: true" in plan_text
    assert "authorizes_runtime_implementation: false" in plan_text
    assert "authorizes_canon_promotion: false" in plan_text


# --- Registry tracking ---

def test_registry_tracking_exists(registry_text):
    assert "RUNTIME-SEQ-PR-A" in registry_text


# --- Decision log tracking ---

def test_decision_log_tracking_exists(decisions_text):
    assert "RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001" in decisions_text


# --- future_required_not_implemented status ---

def test_all_contracts_marked_future(plan_text):
    assert plan_text.count("future_required_not_implemented") >= 16, \
        "All 16 kernel spine contracts must be marked future_required_not_implemented"


# --- No implementation claims ---

FORBIDDEN_IMPLEMENTATIONS = [
    "implements runtime",
    "implements schema",
    "implements command IR",
    "implements validator",
    "implements generator",
    "implements state store",
    "implements state delta",
    "implements event ledger",
    "implements deterministic RNG",
    "implements table/oracle",
    "implements persistence writer",
    "implements retrieval index",
    "implements context-packet compiler",
    "implements redaction algorithm",
    "implements hidden-state database",
    "implements domain runtime",
    "implements campaign memory",
    "implements live-play prompt",
    "implements training",
    "implements donor-content audit",
    "authorizes pilot conversion",
    "authorizes sourcebook inclusion",
    "authorizes canon promotion",
]


@pytest.mark.parametrize("forbidden", FORBIDDEN_IMPLEMENTATIONS)
def test_no_implementation_claims(plan_text, forbidden):
    text_lower = plan_text.lower()
    if "authorizes" in forbidden:
        key = forbidden.replace("authorizes ", "authorizes_").replace(" ", "_")
        assert f"{key}: false" in plan_text or forbidden not in text_lower, \
            f"Plan must not claim: {forbidden}"
    else:
        assert forbidden not in text_lower, f"Plan must not claim: {forbidden}"
