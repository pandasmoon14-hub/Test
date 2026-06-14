from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs/doctrine/reviews/runtime_domain_pr_4f_validation_integration_residual_hardening_review.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
DOMAIN = ROOT / "src/astra_runtime/domain"

PR4F_ID = "RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001"
PR4E_ID = "RUNTIME-DOMAIN-PR-4E-VALIDATION-INTEGRATION-RESIDUAL-SKELETON-HARDENING-001"
PR4D_ID = "RUNTIME-DOMAIN-PR-4D-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-REVIEW-001"
PR4B_ID = "RUNTIME-DOMAIN-PR-4B-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-REVIEW-001"
PR4_ID = "RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_review_file_exists_and_records_required_ids() -> None:
    assert REVIEW.exists()
    text = read(REVIEW)
    for required in (PR4F_ID, PR4E_ID, PR4D_ID, PR4B_ID, PR4_ID):
        assert required in text


def test_review_contains_required_sections_and_backend_first_invariant() -> None:
    text = read(REVIEW)
    required_phrases = [
        "BACKEND-FIRST VALIDATION INVARIANT",
        "LLM is not the game engine",
        "PR-4D BLOCKER-CLOSURE MATRIX",
        "SUBJECT-RELATION VOCABULARY REVIEW",
        "FAILURE-ROUTE SUBJECT REVIEW",
        "ROUTE-SUBJECT DEPENDENCY LINKAGE REVIEW",
        "RESULT / REQUEST SUBJECT-BINDING REVIEW",
        "TYPED DEPENDENCY REVIEW",
        "PROVENANCE-LINKAGE REVIEW",
        "DEPENDENCY-UNIQUENESS REVIEW",
        "VALIDATION-READY REVIEW",
        "INTERMEDIATE-STAGE CONSISTENCY REVIEW",
        "FAILURE-ROUTE AGGREGATE REVIEW",
        "FACTORY / VALIDATOR PARITY REVIEW",
        "IMMUTABILITY AND SERIALIZATION REVIEW",
        "NON-EXECUTION REVIEW",
        "RESOURCE / CONSEQUENCE MATH READINESS",
        "CORPUS-SCALE PRESSURE REVIEW",
        "DOMAIN AND KERNEL HANDOFF REVIEW",
        "RISK REVIEW",
        "HARDENING LEDGER",
        "NON-IMPLEMENTATION REAFFIRMATION",
        "CLASSIFICATION BLOCK",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_gate_finding_selects_exactly_one_next_step() -> None:
    text = read(REVIEW)
    assert text.count("gate_finding:") == 1
    assert text.count("next_step_authorized:") == 1
    assert "requires_pr_4g_hardening_before_pr_5: false" in text
    assert "ready_for_runtime_domain_pr_5_planning: true" in text
    assert "next_step_authorized: RUNTIME-DOMAIN-PR-5 resource and consequence math service planning" in text
    assert "next_step_authorized: RUNTIME-DOMAIN-PR-4G" not in text


def test_gate_fields_authorize_no_runtime_behavior() -> None:
    text = read(REVIEW)
    blocked_fields = [
        "runtime_code_authorized_by_this_pr: false",
        "domain_code_authorized_by_this_pr: false",
        "validation_execution_authorized_by_this_pr: false",
        "invariant_evaluation_authorized_by_this_pr: false",
        "state_mutation_authorized_by_this_pr: false",
        "state_delta_application_authorized_by_this_pr: false",
        "event_ledger_append_authorized_by_this_pr: false",
        "transaction_execution_authorized_by_this_pr: false",
        "actual_event_commitment_authorized_by_this_pr: false",
        "persistence_authorized_by_this_pr: false",
        "replay_authorized_by_this_pr: false",
        "command_execution_authorized_by_this_pr: false",
        "resource_math_authorized_by_this_pr: false",
        "consequence_application_authorized_by_this_pr: false",
        "combat_authorized_by_this_pr: false",
        "model_integration_authorized_by_this_pr: false",
        "live_play_authorized_by_this_pr: false",
        "conversion_authorized_by_this_pr: false",
        "canon_promotion_authorized_by_this_pr: false",
    ]
    for field in blocked_fields:
        assert field in text


def test_registry_records_pr4f_once() -> None:
    registry = read(REGISTRY)
    assert registry.count(f"file_id: {PR4F_ID}") == 1
    assert "runtime_domain_pr_4f_validation_integration_residual_hardening_review" in registry
    assert "reviews_pr_4e: true" in registry
    assert "reviews_pr_5_planning_readiness: true" in registry
    assert "selects_exactly_one_next_step: true" in registry
    assert "authorizes_code_or_runtime_behavior: false" in registry


def test_decision_log_records_pr4f_once() -> None:
    decisions = read(DECISIONS)
    assert decisions.count(f"## {PR4F_ID}") == 1
    assert "PR-4D blockers are closed for PR-5 planning" in decisions
    assert "PR-4G is not required before PR-5 planning" in decisions
    assert "PR-5 planning is authorized" in decisions
    assert "no runtime code" in decisions
    assert "no validation execution" in decisions
    assert "no canon promotion" in decisions


def test_authorized_domain_files_remain_exactly_expected() -> None:
    expected = {
        "__init__.py",
        "command_lifecycle.py",
        "action_legality.py",
        "state_store.py",
        "state_projection.py",
        "transaction_lifecycle.py",
        "event_commitment.py",
        "validation_integration.py",
        "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py",
        "__pycache__",
    }
    assert {path.name for path in DOMAIN.iterdir()} == expected


def test_forbidden_runtime_surfaces_absent() -> None:
    absent = [
        "src/astra_runtime/domain/resource_math.py",
        "src/astra_runtime/domain/combat.py",
        "src/astra_runtime/domain/ability_effects.py",
        "src/astra_runtime/domain/inventory.py",
        "src/astra_runtime/domain/mission.py",
        "src/astra_runtime/domain/social_faction.py",
        "src/astra_runtime/domain/generated_content.py",
        "src/astra_runtime/kernel/context_packet_compiler.py",
        "src/astra_runtime/model",
        "src/astra_runtime/prompts",
        "src/astra_runtime/live_play",
        "src/astra_runtime/ui",
        "src/astra_runtime/database",
        "src/astra_runtime/store",
    ]
    for relative in absent:
        assert not (ROOT / relative).exists()
