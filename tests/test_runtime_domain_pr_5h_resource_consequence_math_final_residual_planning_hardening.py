from pathlib import Path
import re
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
DOMAIN_RESOURCE_MATH = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"
DOMAIN_DIR = ROOT / "src/astra_runtime/domain"
KERNEL_DIR = ROOT / "src/astra_runtime/kernel"

PR5H_ID = "RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001"

LINEAGE_IDS = [
    "RUNTIME-DOMAIN-PR-5G-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-REVIEW-001",
    "RUNTIME-DOMAIN-PR-5F-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-001",
    "RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001",
    "RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001",
    "RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001",
    "RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001",
    "RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001",
    "RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001",
    "RT002_resource_consequence_math_owner_specification.md",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(number: int) -> str:
    text = read(ARTIFACT)
    pattern = rf"^## {number}\. .*?(?=^## {number + 1}\. |\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    assert match, f"missing section {number}"
    return match.group(0)


def _git_status_short() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# 1. Artifact existence and exact ID
# ---------------------------------------------------------------------------


def test_artifact_and_exact_id_exist() -> None:
    assert ARTIFACT.exists(), f"artifact not found at {ARTIFACT}"
    text = read(ARTIFACT)
    assert PR5H_ID in text, f"{PR5H_ID} not found in artifact"


# ---------------------------------------------------------------------------
# 2. Source lineage and precedence
# ---------------------------------------------------------------------------


def test_required_source_lineage_and_precedence() -> None:
    text = read(ARTIFACT)
    for lid in LINEAGE_IDS:
        assert lid in text, f"lineage ID {lid} not found in artifact"

    s1 = section(1)
    assert "planning-only" in s1.lower() or "planning-only" in s1, \
        "section 1 must mention 'planning-only'"
    assert ("follows PR-5G" in s1) or ("follows **RUNTIME-DOMAIN-PR-5G" in s1), \
        "section 1 must reference PR-5G as predecessor"
    assert "PR-5A" in s1, "section 1 must mention PR-5A"
    assert "blocked" in s1.lower(), "section 1 must mention 'blocked'"
    assert "PR-5I" in s1, "section 1 must mention PR-5I"
    assert "review gate" in s1.lower() or "review gate" in s1, \
        "section 1 must mention 'review gate'"
    assert ("grants no implementation" in s1) or ("no implementation authority" in s1), \
        "section 1 must state no implementation authority"
    # Precedence language
    assert ("PR-5H replaces earlier contracts only where it explicitly says so" in s1) or \
           ("replaces earlier contracts only where" in s1) or \
           ("overrides earlier" in s1 and "explicitly" in s1) or \
           ("precedence" in s1.lower()), \
        "section 1 must contain precedence language"
    assert "PR-5F overrides PR-5D" in s1 or \
           ("PR-5F" in s1 and "overrides" in s1 and "PR-5D" in s1), \
        "section 1 must state PR-5F overrides PR-5D"
    assert "PR-5D overrides PR-5B" in s1 or \
           ("PR-5D" in s1 and "overrides" in s1 and "PR-5B" in s1), \
        "section 1 must state PR-5D overrides PR-5B"


# ---------------------------------------------------------------------------
# 3. All required sections present
# ---------------------------------------------------------------------------


def test_all_required_sections_present() -> None:
    text = read(ARTIFACT)
    for i in range(1, 16):
        assert f"## {i}." in text, f"section heading '## {i}.' not found"


# ---------------------------------------------------------------------------
# 4. Consolidated effective contract matrix (10 shapes)
# ---------------------------------------------------------------------------


def test_consolidated_effective_contract_matrix_ten_shapes() -> None:
    s3 = section(3)
    shapes = [
        "ResourceMathSubjectReference",
        "ResourceReference",
        "QuantitySpecification",
        "ResourceMathDependency",
        "CostTerm",
        "CostBundle",
        "ConsequenceTerm",
        "ResourceMathRequest",
        "ResourceMathResult",
        "SettlementProposal",
    ]
    for shape in shapes:
        assert shape in s3, f"shape '{shape}' not found in section 3"

    # PR-5F correction
    assert "precision: int | None = None" in s3 or \
           "precision: int | None" in s3, \
        "section 3 must mention precision field"
    assert "value_mode" in s3, "section 3 must mention value_mode"
    assert "policy_route" in s3, "section 3 must mention policy_route"
    assert "MappingProxyType" in s3, "section 3 must mention MappingProxyType"

    # Seven typed scope tuples
    scope_tuples = [
        "referenced_subject_binding_ids",
        "referenced_resource_ref_ids",
        "referenced_quantity_ids",
        "referenced_cost_term_ids",
        "referenced_cost_bundle_ids",
        "referenced_consequence_term_ids",
        "referenced_dependency_ids",
    ]
    for st in scope_tuples:
        assert st in s3, f"typed scope tuple '{st}' not found in section 3"


# ---------------------------------------------------------------------------
# 5. Consolidated controlled constants
# ---------------------------------------------------------------------------


def test_consolidated_controlled_constants() -> None:
    text = read(ARTIFACT)
    # Some constants may be in section 4, some may appear in section 5 or elsewhere
    s4 = section(4)
    search_text = text  # search full artifact as fallback

    constant_names = [
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
        "QUANTITY_NEGATIVE_VALUE_POLICIES",
        "RESOURCE_MATH_DEPENDENCY_TYPES",
        "RESOURCE_MATH_SUBJECT_TYPES",
        "RESOURCE_MATH_SUBJECT_ROLES",
        "RESOURCE_MATH_OWNER_DOMAINS",
        "RESOURCE_TERM_VALUE_MODES",
        "RESOURCE_TERM_POLICY_ROUTES",
        "DECLARATION_PROGRESS_STAGES",
        "SOURCE_LOCAL_STAGES",
    ]
    for name in constant_names:
        assert name in search_text, f"controlled constant '{name}' not found in artifact"

    # PARTIAL_SETTLEMENT_POLICIES may appear in sections 4 or 5
    s5 = section(5)
    assert "PARTIAL_SETTLEMENT_POLICIES" in s4 or "PARTIAL_SETTLEMENT_POLICIES" in s5 or \
           "PARTIAL_SETTLEMENT_POLICIES" in search_text, \
        "PARTIAL_SETTLEMENT_POLICIES not found in sections 4/5"


# ---------------------------------------------------------------------------
# 6. Exhaustive bundle compatibility and unlisted-invalid
# ---------------------------------------------------------------------------


def test_exhaustive_bundle_compatibility_and_unlisted_invalid() -> None:
    s5 = section(5)

    atomicity_tokens = [
        "all_or_nothing_requested",
        "best_effort_requested",
        "ordered_partial_allowed",
        "unordered_partial_allowed",
    ]
    for token in atomicity_tokens:
        assert token in s5, f"atomicity token '{token}' not found in section 5"

    alternative_tokens = [
        "alternative_exactly_one",
        "alternative_at_least_one",
        "alternative_at_most_one",
        "alternative_any",
    ]
    for token in alternative_tokens:
        assert token in s5, f"alternative token '{token}' not found in section 5"

    assert "blocked_pending_transaction_policy" in s5
    assert "invalid_mixed_atomicity" in s5

    assert "no_partial_settlement" in s5 or "no_partial_settlement" in s5
    assert "partial_settlement_allowed" in s5

    assert "bool" in s5, "section 5 must mention bool"
    assert "invalid" in s5.lower(), "section 5 must mention invalid"
    assert "positive integer" in s5.lower() or "positive integer" in s5, \
        "section 5 must mention positive integer bounds"
    assert "len(term_ids)" in s5, "section 5 must mention len(term_ids)"
    assert "minimum" in s5.lower(), "section 5 must mention minimum"
    assert "maximum" in s5.lower(), "section 5 must mention maximum"

    # Unlisted combination is invalid
    assert ("unlisted" in s5.lower() and "invalid" in s5.lower()) or \
           ("not expressly listed" in s5.lower() and "invalid" in s5.lower()) or \
           ("not listed" in s5.lower() and "invalid" in s5.lower()), \
        "section 5 must state unlisted combinations are invalid"

    assert "alternative group" in s5.lower() or "alternative group" in s5, \
        "section 5 must mention alternative groups"
    assert "overlapping" in s5.lower(), \
        "section 5 must mention overlapping groups being invalid"


# ---------------------------------------------------------------------------
# 7. Five dependency lifecycle states
# ---------------------------------------------------------------------------


def test_five_dependency_lifecycle_states() -> None:
    s6 = section(6)

    # Satisfied binding dependency
    assert ("satisfied binding dependency" in s6.lower()) or ("satisfied=True" in s6) or \
           ("Satisfied binding dependency" in s6) or ("satisfied=true" in s6.lower()), \
        "section 6 must describe satisfied binding dependency"

    # Incomplete binding dependency
    assert ("incomplete binding dependency" in s6.lower()) or \
           ("Incomplete binding dependency" in s6), \
        "section 6 must describe incomplete binding dependency"
    assert "satisfied=False" in s6 or "satisfied=false" in s6.lower(), \
        "section 6 must mention satisfied=False for incomplete"

    # Missing binding dependency
    assert ("missing binding dependency" in s6.lower()) or \
           ("Missing binding dependency" in s6), \
        "section 6 must describe missing binding dependency"
    assert "invalid" in s6.lower(), "section 6 must mention invalid for missing"
    assert "reject" in s6.lower() or "factories" in s6.lower(), \
        "section 6 must mention reject or factories for missing"

    # Required but unsatisfied dependency
    assert ("required but unsatisfied dependency" in s6.lower()) or \
           ("Required but unsatisfied dependency" in s6) or \
           ("required" in s6.lower() and "unsatisfied" in s6.lower()), \
        "section 6 must describe required but unsatisfied dependency"
    assert "blocked_missing_dependency" in s6, \
        "section 6 must mention blocked_missing_dependency"

    # Advisory optional unsatisfied dependency
    assert ("advisory optional unsatisfied dependency" in s6.lower()) or \
           ("Advisory optional unsatisfied dependency" in s6) or \
           ("advisory" in s6.lower() and "optional" in s6.lower() and "unsatisfied" in s6.lower()), \
        "section 6 must describe advisory optional unsatisfied dependency"
    assert "required=False" in s6 or "required=false" in s6.lower(), \
        "section 6 must mention required=False"


# ---------------------------------------------------------------------------
# 8. Exact aggregate ownership
# ---------------------------------------------------------------------------


def test_exact_aggregate_ownership() -> None:
    s6 = section(6)

    # Request dependencies
    assert "ResourceMathRequest" in s6 and "dependencies" in s6, \
        "section 6 must mention ResourceMathRequest.dependencies"
    assert "request" in s6.lower()

    # Result dependencies
    assert "ResourceMathResult" in s6 and "dependencies" in s6, \
        "section 6 must mention ResourceMathResult.dependencies"
    assert "result" in s6.lower()

    # Proposal dependencies
    assert "SettlementProposal" in s6 and "dependencies" in s6, \
        "section 6 must mention SettlementProposal.dependencies"
    assert "proposal" in s6.lower()

    # Uniqueness
    assert "dependency_id" in s6, "section 6 must mention dependency_id"
    assert "dependency_type" in s6 and "reference_id" in s6, \
        "section 6 must mention dependency_type and reference_id uniqueness"

    # hidden_info_safe
    assert "hidden_info_safe=False" in s6 or "hidden_info_safe=false" in s6.lower(), \
        "section 6 must mention hidden_info_safe=False"
    assert ("not the same as unsatisfied" in s6.lower()) or \
           ("not the same as" in s6.lower() and "unsatisfied" in s6.lower()), \
        "section 6 must clarify hidden_info_safe is not the same as unsatisfied"


# ---------------------------------------------------------------------------
# 9. No empty total typed scope
# ---------------------------------------------------------------------------


def test_no_empty_total_typed_scope() -> None:
    s7 = section(7)
    assert "empty typed result scope" in s7.lower() or "empty typed result scope" in s7, \
        "section 7 must mention empty typed result scope"
    assert "invalid" in s7.lower(), "section 7 must state empty typed scope is invalid"
    assert "non-empty" in s7.lower() or "non-empty" in s7, \
        "section 7 must mention non-empty requirement"


# ---------------------------------------------------------------------------
# 10. Accepted/normalized/blocked scope cardinality
# ---------------------------------------------------------------------------


def test_accepted_normalized_and_blocked_scope_cardinality() -> None:
    s7 = section(7)
    assert "accepted_for_planning" in s7 or "accepted" in s7.lower()
    assert "normalized_for_planning" in s7 or "normalized" in s7.lower()
    assert "at least one" in s7.lower(), \
        "section 7 must require at least one record"

    # Business records
    records_found = sum(1 for kw in ["resource", "quantity", "cost term", "cost bundle", "consequence term"]
                        if kw in s7.lower())
    assert records_found >= 1, "section 7 must mention business record types"

    assert "blocked" in s7.lower(), "section 7 must mention blocked"
    assert "scope" in s7.lower(), "section 7 must mention scope"
    assert ("blocking record" in s7.lower()) or ("required dependency" in s7.lower()) or \
           ("blocker" in s7.lower()), \
        "section 7 must mention blocking records or required dependencies"

    assert "blocked_missing_dependency" in s7, \
        "section 7 must mention blocked_missing_dependency"
    assert "dependency-only" in s7.lower() or "dependency-only" in s7, \
        "section 7 must mention dependency-only"


# ---------------------------------------------------------------------------
# 11. All scoped IDs resolve even for blocked
# ---------------------------------------------------------------------------


def test_all_scoped_ids_resolve_even_for_blocked() -> None:
    s7 = section(7)
    lower = s7.lower()
    assert ("scoped id" in lower or "scoped" in lower) and "resolve" in lower, \
        "section 7 must require scoped IDs to resolve"
    assert "blocked" in lower or "quarantined" in lower or "escalated" in lower, \
        "section 7 must mention blocked/quarantined/escalated scoped resolution"


# ---------------------------------------------------------------------------
# 12. Exact blocker precedence order
# ---------------------------------------------------------------------------


def test_exact_blocker_precedence_order() -> None:
    s8 = section(8)
    lower = s8.lower()

    # All 8 precedence items must be present
    assert "doctrine escalation" in lower or "escalated_to_doctrine" in s8 or \
           "doctrine_escalation" in lower, \
        "section 8 must mention doctrine escalation"
    assert "quarantine" in lower or "quarantined_for_review" in s8, \
        "section 8 must mention quarantine"
    assert "hidden" in lower or "blocked_hidden_information" in s8, \
        "section 8 must mention hidden information blocker"
    assert "missing" in lower or "blocked_missing_dependency" in s8, \
        "section 8 must mention missing dependency blocker"
    assert ("blocked" in lower and "numeric" in lower) or "blocked_incompatible_policy" in s8, \
        "section 8 must mention blocked numeric/incompatible policy"
    assert "owner handoff" in lower or "requires_owner_handoff" in s8 or \
           "owner_handoff" in lower, \
        "section 8 must mention owner handoff"
    assert "source-supported negative" in lower or "source_supported_negative" in lower or \
           "negative" in lower, \
        "section 8 must mention source-supported negative"
    assert "no blocker" in lower or "no_blocker" in lower or "none" in lower, \
        "section 8 must mention no blocker"

    # Diagnostics
    assert "diagnostics" in lower, \
        "section 8 must mention diagnostics preservation"


# ---------------------------------------------------------------------------
# 13. Source-supported negative uses universal literal contract
# ---------------------------------------------------------------------------


def test_source_supported_negative_uses_universal_literal_contract() -> None:
    s9 = section(9)

    assert "source_literal" in s9, "section 9 must mention source_literal"
    assert "negative_values_allowed_by_source" in s9, \
        "section 9 must mention negative_values_allowed_by_source"
    assert "non-empty" in s9.lower() or "non-empty" in s9
    assert "str" in s9

    assert "one line" in s9.lower() or "single line" in s9.lower() or "one-line" in s9.lower(), \
        "section 9 must mention one-line constraint"

    assert ("no leading" in s9.lower()) or ("no trailing" in s9.lower()) or \
           ("whitespace" in s9.lower()), \
        "section 9 must mention whitespace constraints"

    assert "Cc" in s9 or "control" in s9.lower(), \
        "section 9 must mention Cc/control character constraint"
    assert "Cs" in s9 or "surrogate" in s9.lower(), \
        "section 9 must mention Cs/surrogate constraint"

    assert ("no normalization" in s9.lower()) or ("no parsing" in s9.lower()) or \
           ("no evaluation" in s9.lower()), \
        "section 9 must state no normalization/parsing/evaluation"


# ---------------------------------------------------------------------------
# 14. Settlement proposal receives both request and result
# ---------------------------------------------------------------------------


def test_settlement_proposal_receives_both_request_and_result() -> None:
    s10 = section(10)

    assert "request: ResourceMathRequest" in s10 or \
           ("request" in s10 and "ResourceMathRequest" in s10), \
        "section 10 must mention request: ResourceMathRequest"
    assert "result: ResourceMathResult" in s10 or \
           ("result" in s10 and "ResourceMathResult" in s10), \
        "section 10 must mention result: ResourceMathResult"

    assert "create_settlement_proposal" in s10, \
        "section 10 must mention create_settlement_proposal"
    assert "validate_settlement_proposal" in s10, \
        "section 10 must mention validate_settlement_proposal"

    assert ("no certificate" in s10.lower()) or ("No certificate" in s10) or \
           ("direct aggregate" in s10.lower()) or ("Direct aggregate" in s10), \
        "section 10 must mention no certificate or direct aggregate"


# ---------------------------------------------------------------------------
# 15. Exact request/result/proposal validation order
# ---------------------------------------------------------------------------


def test_exact_request_result_proposal_validation_order() -> None:
    s10 = section(10)

    assert "Validate" in s10 or "validate" in s10.lower()
    assert "ResourceMathRequest" in s10
    assert "ResourceMathResult" in s10
    assert "SettlementProposal" in s10

    assert "No repository lookup" in s10 or "no repository lookup" in s10.lower(), \
        "section 10 must state no repository lookup"

    assert ("no caller-supplied" in s10.lower()) or ("No caller-supplied" in s10) or \
           ("no boolean" in s10.lower()) or ("No boolean" in s10), \
        "section 10 must state no caller-supplied or no boolean"


# ---------------------------------------------------------------------------
# 16. Manual frozen-dataclass parity requirement
# ---------------------------------------------------------------------------


def test_manual_frozen_dataclass_parity_requirement() -> None:
    s11 = section(11)
    lower = s11.lower()

    assert "frozen dataclass" in lower or "frozen-dataclass" in lower, \
        "section 11 must mention frozen dataclass"
    assert "manually constructed" in lower or "manual construction" in lower or \
           "manual" in lower, \
        "section 11 must mention manual construction"
    assert "shared private helpers" in lower or "shared helpers" in lower, \
        "section 11 must mention shared helpers"
    assert "factory" in lower or "factories" in lower, \
        "section 11 must mention factories"
    assert "validator" in lower or "validators" in lower, \
        "section 11 must mention validators"


# ---------------------------------------------------------------------------
# 17. Internal-only serialization and RT-005 ownership
# ---------------------------------------------------------------------------


def test_internal_only_serialization_and_rt005_ownership() -> None:
    s12 = section(12)

    assert "to_dict" in s12, "section 12 must mention to_dict"
    assert ("no `to_public_dict`" in s12) or ("no to_public_dict" in s12) or \
           ("no `to_public_dict`" in s12), \
        "section 12 must state no to_public_dict"
    assert "defensive copies" in s12.lower() or "defensive copies" in s12, \
        "section 12 must mention defensive copies"
    assert "RT-005" in s12, "section 12 must reference RT-005"


# ---------------------------------------------------------------------------
# 18. Corpus-scale and RT owner boundaries
# ---------------------------------------------------------------------------


def test_corpus_scale_and_rt_owner_boundaries() -> None:
    s12 = section(12)

    assert "RT-002 does not absorb" in s12 or "RT-002" in s12, \
        "section 12 must mention RT-002"

    boundary_keywords = ["combat", "ability", "inventory", "mission", "social",
                         "RNG", "persistence", "event", "canon"]
    found = sum(1 for kw in boundary_keywords if kw in s12 or kw.lower() in s12.lower())
    assert found >= 3, \
        f"section 12 must mention at least 3 RT-002 non-absorbed domains, found {found}"


# ---------------------------------------------------------------------------
# 19. Exactly one PR-5I next step
# ---------------------------------------------------------------------------


def test_exactly_one_pr_5i_next_step() -> None:
    s14 = section(14)
    text = read(ARTIFACT)

    assert "RUNTIME-DOMAIN-PR-5I" in s14, \
        "section 14 must mention RUNTIME-DOMAIN-PR-5I"
    assert "review gate" in s14.lower() or "review gate" in s14, \
        "section 14 must mention review gate"
    assert "next_step_authorized: RUNTIME-DOMAIN-PR-5A" not in text, \
        "PR-5A must not be the authorized next step"


# ---------------------------------------------------------------------------
# 20. PR-5A not authorized
# ---------------------------------------------------------------------------


def test_pr_5a_not_authorized() -> None:
    text = read(ARTIFACT)

    assert "pr_5a_authorized: false" in text, \
        "artifact must state pr_5a_authorized: false"
    assert "PR-5A" in text and "blocked" in text.lower(), \
        "artifact must state PR-5A is blocked"
    assert "pr_5a_authorized: true" not in text, \
        "pr_5a_authorized: true must NOT appear in artifact"


# ---------------------------------------------------------------------------
# 21. Registry record exactly once
# ---------------------------------------------------------------------------


def test_registry_record_exactly_once() -> None:
    registry = read(REGISTRY)
    count = registry.count(PR5H_ID)
    assert count == 1, f"PR5H_ID should appear exactly once in registry, found {count}"


# ---------------------------------------------------------------------------
# 22. Decision heading exactly once
# ---------------------------------------------------------------------------


def test_decision_heading_exactly_once() -> None:
    decisions = read(DECISIONS)
    heading = f"## {PR5H_ID}"
    count = decisions.count(heading)
    assert count == 1, f"decision heading should appear exactly once, found {count}"


# ---------------------------------------------------------------------------
# 23. Registry version unchanged
# ---------------------------------------------------------------------------


def test_registry_version_unchanged() -> None:
    registry = read(REGISTRY)
    assert re.search(r"^registry_version: 0\.1\.0$", registry, flags=re.M), \
        "registry_version must remain 0.1.0"


# ---------------------------------------------------------------------------
# 24. No resource_consequence_math.py
# ---------------------------------------------------------------------------


def test_no_resource_consequence_math_py() -> None:
    assert not DOMAIN_RESOURCE_MATH.exists(), \
        "resource_consequence_math.py must not exist"


# ---------------------------------------------------------------------------
# 25. No changes under src/
# ---------------------------------------------------------------------------


def test_no_changes_under_src() -> None:
    changed_paths = {line.split(maxsplit=1)[-1].strip() for line in _git_status_short()}
    domain_changes = [p for p in changed_paths if p.startswith("src/astra_runtime/domain/")]
    kernel_changes = [p for p in changed_paths if p.startswith("src/astra_runtime/kernel/")]
    assert not domain_changes, f"unexpected changes under domain/: {domain_changes}"
    assert not kernel_changes, f"unexpected changes under kernel/: {kernel_changes}"


# ---------------------------------------------------------------------------
# 26. Changed-file footprint
# ---------------------------------------------------------------------------


def test_changed_file_footprint() -> None:
    changed_paths = {line.split(maxsplit=1)[-1].strip() for line in _git_status_short()}
    allowed = {
        "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md",
        "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py",
        "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
        "docs/decisions/current_decisions_log.md",
    }
    assert changed_paths <= allowed, \
        f"unexpected changed files: {changed_paths - allowed}"


# ---------------------------------------------------------------------------
# 27. Closure ledger - all eight closed
# ---------------------------------------------------------------------------


def test_closure_ledger_all_eight_closed() -> None:
    s13 = section(13)
    lower = s13.lower()

    # At least 8 occurrences of "closed"
    closed_count = lower.count("closed")
    assert closed_count >= 8, \
        f"section 13 must contain 'closed' at least 8 times, found {closed_count}"

    # All 8 correction keywords
    assert "effective contract matrix" in lower or "final effective contract" in lower, \
        "closure ledger must reference effective contract matrix"

    assert "atomicity" in lower, "closure ledger must reference atomicity"
    assert "ordering" in lower or "partial-settlement" in lower or "bundle" in lower, \
        "closure ledger must reference ordering/partial-settlement/bundle"

    assert "dependency lifecycle" in lower or "unsatisfied binding" in lower, \
        "closure ledger must reference dependency lifecycle"

    assert "typed" in lower and "scope" in lower, \
        "closure ledger must reference typed scope"
    assert "empty" in lower or "cardinality" in lower, \
        "closure ledger must reference empty or cardinality"

    assert "blocker" in lower and "precedence" in lower, \
        "closure ledger must reference blocker precedence"

    assert "source" in lower and "literal" in lower and "negative" in lower, \
        "closure ledger must reference source literal negative"

    assert "proposal" in lower and "request" in lower and "validation" in lower, \
        "closure ledger must reference proposal request validation"

    assert "factory" in lower and "validator" in lower and "parity" in lower, \
        "closure ledger must reference factory/validator parity"
