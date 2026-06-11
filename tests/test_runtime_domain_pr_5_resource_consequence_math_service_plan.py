from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5_resource_consequence_math_service_plan.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
DOMAIN = ROOT / "src/astra_runtime/domain"
RESOURCE_MATH = DOMAIN / "resource_consequence_math.py"

PR5_ID = "RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001"
PR4F_ID = "RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001"
NEXT_STEP = "RUNTIME-DOMAIN-PR-5B: Resource and Consequence Math Planning Hardening"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_file_exists_and_records_required_ids() -> None:
    assert PLAN.exists()
    text = read(PLAN)
    required = [
        PR5_ID,
        PR4F_ID,
        "RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001",
        "RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001",
        "RT002_resource_consequence_math_owner_specification.md",
        "RT011_validation_readiness_tooling_owner_specification.md",
    ]
    for item in required:
        assert item in text


def test_plan_contains_required_sections_and_backend_first_invariant() -> None:
    text = read(PLAN)
    required_phrases = [
        "Purpose, status, and source ledger",
        "Backend-first invariant",
        "LLM is not the game engine",
        "RT-002 ownership and explicit non-ownership",
        "Resource-model requirements without final pools",
        "Planning taxonomies for resource, cost, and consequence families",
        "Cost lifecycle and decision models",
        "Separation of declaration, calculation, affordability, reservation, settlement, commitment, and persistence",
        "Cost timing and outcome policies",
        "Multi-term bundles, alternatives, atomicity, and partial settlement",
        "Overcommitment, partial payment, substitution, debt, and success/failure-at-cost boundaries",
        "Refund, reversal, compensation, and rollback-accounting boundaries",
        "Reward, loss, recovery, repair, salvage, crafting, upkeep, and requisition handoffs",
        "Deterministic numeric representation requirements",
        "integer",
        "Decimal",
        "Fraction",
        "fixed-point",
        "Units, dimensions, aliases, conversion policies, rounding, and audit lineage",
        "Safe future expression architecture",
        "no `eval`",
        "RNG/table-oracle handoff to RT-009",
        "Hidden-information and visibility requirements",
        "Validation-integration handoff",
        "`validation_ready` is not `validation_passed`",
        "State-delta, transaction, event, persistence, replay, and audit handoffs",
        "Future reference-only architecture for `src/astra_runtime/domain/resource_consequence_math.py`",
        "Proposed immutable future shapes",
        "ResourceReference",
        "QuantitySpecification",
        "CostTerm",
        "CostBundle",
        "ConsequenceTerm",
        "ResourceMathRequest",
        "ResourceMathResult",
        "SettlementProposal",
        "Resource-math invariant requirements",
        "Corpus-scale donor pressure review",
        "200-400 mixed donor sources",
        "Lawful donor outcomes",
        "direct mapping",
        "normalized mapping",
        "source-local retention",
        "quarantine",
        "doctrine escalation",
        "Risk review",
        "Hardening and decision ledger",
        "Future test requirements",
        "Exact proposed planning vocabularies",
        "Stage vocabulary",
        "Decision vocabulary",
        "Family vocabulary",
        "Policy vocabulary",
        "Quantity-kind vocabulary",
        "Atomicity vocabulary",
        "Dependency vocabulary",
        "Dataclass field contracts for future reference-only shapes",
        "Factory and validator invariants",
        "Decision/stage compatibility",
        "Linkage requirements",
        "Bundle linkage",
        "Term linkage",
        "Subject linkage",
        "Unit linkage",
        "Provenance linkage",
        "Trace linkage",
        "Validation linkage",
        "Dependency linkage",
        "False-only authority flags",
        "mutation_authorized: false",
        "commitment_authorized: false",
        "persistence_authorized: false",
        "rng_execution_authorized: false",
        "model_authority_authorized: false",
        "Detailed resource/cost/consequence family matrices",
        "Resource family matrix",
        "Cost family matrix",
        "Consequence family matrix",
        "Real decision ledger",
        "Required before PR-5A",
        "Required before executable calculation",
        "Required before settlement or commitment",
        "PR-5B authorization boundary",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_gate_finding_is_exactly_one_and_selects_pr5b() -> None:
    text = read(PLAN)
    assert text.count("gate_finding:") == 1
    assert text.count("next_step_authorized:") == 1
    assert "gate_finding: ready_for_runtime_domain_pr_5b_planning_hardening" in text
    assert f"selected_next_step: {NEXT_STEP}" in text
    assert "pr_5b_must_be_planning_only_and_non_implementing: true" in text


def test_non_implementation_boundaries_are_explicit() -> None:
    text = read(PLAN)
    blocked_fields = [
        "runtime_code_authorized_by_this_pr: false",
        "domain_code_authorized_by_this_pr: false",
        "resource_consequence_math_file_created_by_this_pr: false",
        "resource_math_authorized_by_this_pr: false",
        "consequence_application_authorized_by_this_pr: false",
        "formulas_or_values_authorized_by_this_pr: false",
        "final_resource_pools_authorized_by_this_pr: false",
        "final_currencies_or_economies_authorized_by_this_pr: false",
        "affordability_execution_authorized_by_this_pr: false",
        "reservation_or_settlement_authorized_by_this_pr: false",
        "expression_parsing_or_evaluation_authorized_by_this_pr: false",
        "rng_or_table_execution_authorized_by_this_pr: false",
        "state_mutation_authorized_by_this_pr: false",
        "state_delta_application_authorized_by_this_pr: false",
        "event_append_or_commitment_authorized_by_this_pr: false",
        "persistence_or_replay_authorized_by_this_pr: false",
        "combat_authorized_by_this_pr: false",
        "abilities_authorized_by_this_pr: false",
        "inventory_authorized_by_this_pr: false",
        "mission_authorized_by_this_pr: false",
        "social_authorized_by_this_pr: false",
        "model_live_play_ui_authorized_by_this_pr: false",
        "conversion_authorized_by_this_pr: false",
        "sourcebook_inclusion_authorized_by_this_pr: false",
        "canon_promotion_authorized_by_this_pr: false",
    ]
    for field in blocked_fields:
        assert field in text


def test_registry_records_pr5_once() -> None:
    registry = read(REGISTRY)
    assert registry.count(f"file_id: {PR5_ID}") == 1
    assert "version: 0.1.83" in registry
    assert "runtime_domain_pr_5_resource_consequence_math_service_plan" in registry
    assert "selects_exactly_one_next_step: true" in registry
    assert "next_allowed_step: RUNTIME-DOMAIN-PR-5B Resource and Consequence Math Planning Hardening, pending review" in registry
    assert "authorizes_resource_math_by_this_pr: false" in registry
    assert "authorizes_consequence_application_by_this_pr: false" in registry
    assert "exact_stage_decision_family_policy_quantity_atomicity_dependency_vocabularies: true" in registry
    assert "dataclass_field_contracts: true" in registry
    assert "factory_validator_invariants: true" in registry
    assert "decision_stage_compatibility: true" in registry
    assert "false_only_mutation_commitment_persistence_rng_model_authority_flags: true" in registry
    assert "decision_ledger_required_before_pr_5a: true" in registry


def test_decision_log_records_pr5_heading_once() -> None:
    decisions = read(DECISIONS)
    assert decisions.count(f"## {PR5_ID}") == 1
    assert "planning-only status recorded for PR-5" in decisions
    assert "PR-5B must be planning-only and non-implementing" in decisions
    assert "exact proposed stage, decision, family, policy, quantity-kind, atomicity, and dependency vocabularies" in decisions
    assert "required before PR-5A" in decisions
    assert "before executable calculation" in decisions
    assert "before settlement or commitment" in decisions
    assert "validation_ready is not validation_passed" in decisions
    assert "no resource math" in decisions
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
        "__pycache__",
    }
    assert {path.name for path in DOMAIN.iterdir() if path.is_file()} == (expected - {"__pycache__"})


def test_resource_consequence_math_module_absent() -> None:
    assert not RESOURCE_MATH.exists()
    assert "resource_consequence_math.py" in read(PLAN)
