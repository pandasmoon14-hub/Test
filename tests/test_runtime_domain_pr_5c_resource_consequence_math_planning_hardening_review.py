from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5c_resource_consequence_math_planning_hardening_review.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
DOMAIN_RESOURCE_MATH = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"

PR5C_ID = "RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001"
PR5B_ID = "RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001"
PR5_ID = "RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001"
PR4F_ID = "RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_artifact_exists_and_records_lineage() -> None:
    text = read(ARTIFACT)
    for token in (PR5C_ID, PR5B_ID, PR5_ID, PR4F_ID, "RT-002"):
        assert token in text
    assert "non-executable review gate" in text
    assert "reviews PR-5B" in text
    assert "implements no code" in text
    assert "PR-5A blocked" in text


def test_backend_first_invariant_and_non_authority_boundary() -> None:
    text = read(ARTIFACT)
    for token in (
        "the LLM is not the game engine",
        "reference shapes are not calculations",
        "results and settlement proposals are not committed state",
        "validation_ready` is not `validation_passed",
        "no donor resource terminology becomes Astra law",
        "no runtime or canon authority is granted",
        "resource_calculation_by_this_pr: false",
        "consequence_calculation_by_this_pr: false",
        "authorizes_settlement_by_this_pr: false",
        "authorizes_canon_promotion_by_this_pr: false",
    ):
        assert token in text


def test_all_required_review_sections_are_present() -> None:
    text = read(ARTIFACT)
    required_headings = [
        "## 1. Purpose, status, and source ledger",
        "## 2. Backend-first invariant",
        "## 3. PR-5B scope review",
        "## 4. PR-5 requirement-closure matrix",
        "## 5. Constant-surface review",
        "## 6. Stage-model review",
        "## 7. Decision/stage compatibility review",
        "## 8. Exact dataclass-contract review",
        "## 9. Default-value validity matrix",
        "## 10. Validation-posture review",
        "## 11. Subject-identity review",
        "## 12. Dependency-contract review",
        "## 13. Quantity-contract review",
        "## 14. CostTerm and ConsequenceTerm review",
        "## 15. CostBundle review",
        "## 16. Request/result/proposal linkage review",
        "## 17. SettlementProposal boundary review",
        "## 18. False-only authority review",
        "## 19. Factory/validator parity review",
        "## 20. Serialization and hidden-information review",
        "## 21. Family-matrix corpus review",
        "## 22. Numeric/unit/conversion review",
        "## 23. Owner-boundary review",
        "## 24. Risk review",
        "## 25. Hardening ledger",
        "## 26. Gate decision",
        "## 27. Recommended next PR",
        "## 28. Non-implementation reaffirmation",
        "## 29. Classification block",
    ]
    for heading in required_headings:
        assert heading in text


def test_pr5_closure_and_constant_surface_reviews_are_complete() -> None:
    text = read(ARTIFACT)
    for item in (
        "Public constants",
        "Stage model",
        "Decision/stage compatibility",
        "Nine dataclass contracts",
        "factory/validator parity",
        "RESOURCE_MATH_STAGES",
        "RESOURCE_MATH_DECISIONS",
        "RESOURCE_FAMILIES",
        "COST_FAMILIES",
        "CONSEQUENCE_FAMILIES",
        "COST_TIMING_POLICIES",
        "COST_OUTCOME_POLICIES",
        "QUANTITY_KINDS",
        "QUANTITY_REPRESENTATION_KINDS",
        "CONVERSION_POLICIES",
        "ROUNDING_POLICIES",
        "VISIBILITY_POLICIES",
        "ATOMICITY_POLICIES",
        "ORDERING_POLICIES",
        "PARTIAL_SETTLEMENT_POLICIES",
        "RESOURCE_MATH_DEPENDENCY_TYPES",
        "RESOURCE_MATH_SUBJECT_TYPES",
        "RESOURCE_MATH_OWNER_DOMAINS",
    ):
        assert item in text


def test_dataclass_and_default_value_review_covers_required_shapes() -> None:
    text = read(ARTIFACT)
    for shape in (
        "ResourceReference",
        "QuantitySpecification",
        "ResourceMathDependency",
        "CostTerm",
        "CostBundle",
        "ConsequenceTerm",
        "ResourceMathRequest",
        "ResourceMathResult",
        "SettlementProposal",
    ):
        assert shape in text
    for default in (
        "validation_ready",
        "validation_passed",
        "public",
        "no_conversion",
        "no_rounding",
        "all_or_nothing_requested",
        "unordered_terms",
        "no_partial_settlement",
        "hidden_info_safe",
        "blocked_pending_validation",
        "validation_blocked",
    ):
        assert default in text
    assert "Default-value validity matrix" in text
    assert "PR-5D defect" in text


def test_specialized_reviews_and_ledgers_are_present() -> None:
    text = read(ARTIFACT)
    for token in (
        "validation-posture vocabulary",
        "subject typing",
        "required=True` and `satisfied=False",
        "integer, decimal, fraction, fixed point, source literal, and unknown pending review",
        "ConsequenceTerm lawfully permits no resource or no quantity",
        "minimum_required_terms",
        "maximum_allowed_terms",
        "validation_result_ref",
        "to_public_dict()",
        "fantasy, sci-fi, cultivation",
        "PR-5A must perform no arithmetic",
        "RT-002 does not absorb combat/damage",
        "Risk review",
        "Hardening ledger",
    ):
        assert token in text


def test_false_only_authority_review_lists_all_flags() -> None:
    text = read(ARTIFACT)
    for flag in (
        "calculation_executed",
        "affordability_executed",
        "reservation_authorized",
        "settlement_authorized",
        "consequence_application_authorized",
        "mutation_authorized",
        "state_delta_application_authorized",
        "transaction_execution_authorized",
        "event_commitment_authorized",
        "event_append_authorized",
        "persistence_authorized",
        "replay_authorized",
        "rng_execution_authorized",
        "table_oracle_execution_authorized",
        "model_authority_authorized",
        "live_play_authorized",
        "ui_authorized",
        "conversion_authorized",
        "canon_promotion_authorized",
    ):
        assert flag in text


def test_exactly_one_gate_finding_and_selected_next_step() -> None:
    text = read(ARTIFACT)
    assert text.count("gate_finding:") == 1
    assert "requires_pr_5d_before_pr_5a: true" in text
    assert "ready_for_pr_5a_skeleton_implementation: false" in text
    assert text.count("next_step_authorized:") == 1
    assert "RUNTIME-DOMAIN-PR-5D resource and consequence math final planning hardening" in text
    assert "Chosen outcome: **HARDENING**" in text
    assert "Chosen outcome: **PASS**" not in text


def test_registry_records_pr5c_once_and_preserves_version() -> None:
    registry = read(REGISTRY)
    assert re.search(r"^registry_version: 0\.1\.0$", registry, re.MULTILINE)
    assert registry.count(f"file_id: {PR5C_ID}") == 1
    assert registry.count(PR5C_ID) == 1
    assert "version: 0.1.85" in registry
    assert "pr_5d_required_before_pr_5a: true" in registry
    assert "pr_5a_authorized: false" in registry
    assert "next_allowed_step: RUNTIME-DOMAIN-PR-5D resource and consequence math final planning hardening" in registry


def test_decision_heading_once_and_records_non_implementation() -> None:
    decisions = read(DECISIONS)
    assert decisions.count(f"## {PR5C_ID}") == 1
    section = decisions.split(f"## {PR5C_ID}", 1)[1]
    assert "Review-gate-only status" in section
    assert "PR-5D is required before PR-5A" in section
    assert "PR-5A is not authorized" in section
    assert "sole next step is PR-5D" in section
    for token in (
        "runtime_code_authorized_by_this_pr: false",
        "domain_code_authorized_by_this_pr: false",
        "settlement_authorized_by_this_pr: false",
        "persistence_authorized_by_this_pr: false",
        "canon_promotion_authorized_by_this_pr: false",
    ):
        assert token in section


def test_resource_consequence_math_module_and_runtime_domain_file_state() -> None:
    assert DOMAIN_RESOURCE_MATH.exists()
    added_files = set(
        line[3:]
        for line in re.sub(r"\x1b\[[0-9;]*m", "", __import__("subprocess").check_output(
            ["git", "status", "--short"], cwd=ROOT, text=True
        )).splitlines()
        if line.startswith("A  ") or line.startswith("?? ")
    )
    assert not any(
        path.startswith("src/astra_runtime/domain/") for path in added_files
        if path != "src/astra_runtime/domain/resource_consequence_math.py"
    )
    assert not any(path.startswith("src/astra_runtime/kernel/") for path in added_files)
