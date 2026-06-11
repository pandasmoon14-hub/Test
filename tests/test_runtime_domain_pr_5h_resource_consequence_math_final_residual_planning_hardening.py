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

# ---- Exact inherited constant sets (source of truth) ----

RESOURCE_MATH_STAGES = {
    "resource_math_requested",
    "source_declaration_captured",
    "subject_refs_bound",
    "resource_refs_declared",
    "quantity_specs_declared",
    "terms_declared",
    "bundle_structure_declared",
    "policy_refs_declared",
    "dependency_refs_bound",
    "calculation_ready_for_review",
    "blocked_pending_validation",
    "blocked_pending_owner_handoff",
    "quarantined_for_review",
    "escalated_to_doctrine",
}

RESOURCE_MATH_DECISIONS = {
    "accepted_for_planning",
    "normalized_for_planning",
    "source_local_retained",
    "requires_validation_review",
    "requires_owner_handoff",
    "blocked_missing_dependency",
    "blocked_incompatible_policy",
    "blocked_hidden_information",
    "quarantined_for_review",
    "escalated_to_doctrine",
}

RESOURCE_FAMILIES = {
    "pooled_expendable",
    "scene_counter",
    "charge",
    "currency_like",
    "material",
    "asset_integrity",
    "vehicle_integrity",
    "time_window",
    "opportunity",
    "social_capital",
    "faction_standing",
    "clue_information",
    "risk_heat",
    "strain_corruption",
    "injury_recovery",
    "cooldown",
    "debt_obligation",
    "source_local_resource",
}

COST_FAMILIES = {
    "activation",
    "upkeep",
    "maintenance",
    "opportunity",
    "prerequisite_lock",
    "reservation_hold",
    "partial_payment",
    "substitution",
    "overcommitment",
    "debt_creation",
    "success_at_cost",
    "failure_at_cost",
    "cancellation",
    "interruption",
    "refund",
    "reversal",
    "compensation",
    "repair",
    "recovery",
    "crafting",
    "salvage",
    "requisition",
    "validation_blocked",
}

CONSEQUENCE_FAMILIES = {
    "gain",
    "loss",
    "transfer",
    "lock",
    "unlock",
    "exposure",
    "exhaustion",
    "degradation",
    "escalation",
    "cooldown",
    "debt",
    "obligation",
    "harm_pressure",
    "recovery_pressure",
    "visibility_change",
    "mission_route",
    "clue_route",
    "social_faction_change",
    "inventory_asset_change",
    "provenance_recurrence",
    "quarantine_escalation",
}

COST_TIMING_POLICIES = {
    "pay_before_resolution",
    "reserve_before_resolution",
    "pay_on_attempt",
    "pay_on_success",
    "pay_on_failure",
    "pay_on_commitment",
    "pay_over_time",
    "upkeep_interval",
    "refund_on_cancel",
    "no_refund_on_interrupt",
    "compensate_after_rollback",
    "blocked_pending_validation",
}

COST_OUTCOME_POLICIES = {
    "success",
    "failure",
    "partial_success",
    "cancelled",
    "interrupted",
    "invalid",
    "validation_blocked",
    "owner_blocked",
    "quarantined",
    "escalated",
    "rollback_required",
}

QUANTITY_KINDS = {
    "count",
    "pool_amount",
    "delta",
    "ratio",
    "percentage",
    "duration",
    "interval",
    "threshold",
    "capacity",
    "rank",
    "tier",
    "charge_count",
    "currency_amount",
    "material_amount",
    "durability_amount",
    "debt_amount",
    "source_literal_quantity",
    "unknown_pending_review",
}

RESOURCE_MATH_SUBJECT_TYPES = {
    "actor",
    "command",
    "action",
    "item",
    "asset",
    "vehicle",
    "mission",
    "faction",
    "location",
    "state_record",
    "generated_content",
    "resource_owner",
    "source_local_subject",
    "unknown_pending_review",
}

RESOURCE_MATH_OWNER_DOMAINS = {
    "RT001_command_lifecycle_action_legality",
    "RT002_resource_consequence_math",
    "RT003_combat_hazard_damage_recovery",
    "RT004_ability_effect_skill_binding",
    "RT005_context_packet_hidden_information",
    "RT006_mission_reward_clue_routing",
    "RT007_social_faction_actor_knowledge",
    "RT008_generated_content_provenance_recurrence",
    "RT009_runtime_rng_table_oracle",
    "RT010_inventory_item_vehicle_asset",
    "RT011_validation_readiness_tooling",
    "RT012_d_series_promotion_boundary",
    "source_local_owner",
    "doctrine_escalation",
}

DECLARATION_PROGRESS_STAGES = {
    "source_declaration_captured",
    "subject_refs_bound",
    "resource_refs_declared",
    "quantity_specs_declared",
    "terms_declared",
    "bundle_structure_declared",
    "policy_refs_declared",
    "dependency_refs_bound",
    "calculation_ready_for_review",
}

SOURCE_LOCAL_STAGES = {
    "source_declaration_captured",
    "resource_refs_declared",
    "terms_declared",
    "bundle_structure_declared",
    "policy_refs_declared",
}

VALIDATION_BLOCK_STAGES = {"blocked_pending_validation"}
OWNER_HANDOFF_STAGES = {"blocked_pending_owner_handoff"}
MISSING_DEPENDENCY_STAGES = {
    "dependency_refs_bound",
    "blocked_pending_validation",
    "blocked_pending_owner_handoff",
}
POLICY_BLOCK_STAGES = {"policy_refs_declared"}
HIDDEN_INFORMATION_BLOCK_STAGES = {
    "dependency_refs_bound",
    "blocked_pending_validation",
}
QUARANTINE_STAGES = {"quarantined_for_review"}
ESCALATION_STAGES = {"escalated_to_doctrine"}

DONOR_SHAPED_RESOURCE_FAMILIES = {
    "hit_points",
    "spell_slots",
    "experience_points",
    "fate_points",
    "action_points",
    "movement_points",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(number: int) -> str:
    text = read(ARTIFACT)
    pattern = rf"^## {number}\. .*?(?=^## {number + 1}\. |\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    assert match, f"missing section {number}"
    return match.group(0)


def _extract_numbered_set(text: str, heading_pattern: str) -> set[str]:
    m = re.search(heading_pattern, text)
    assert m, f"heading not found: {heading_pattern}"
    block_start = m.end()
    block_end = text.find("\n###", block_start)
    if block_end == -1:
        block_end = text.find("\n---", block_start)
    if block_end == -1:
        block_end = len(text)
    block = text[block_start:block_end]
    return set(re.findall(r"`([a-zA-Z0-9_]+)`", block))


def _extract_stage_subset(text: str, subset_name: str) -> set[str]:
    pattern = rf"\*\*{re.escape(subset_name)}:\*\*\s*\n([^\n]+)"
    m = re.search(pattern, text)
    assert m, f"stage subset '{subset_name}' not found"
    return set(re.findall(r"`([a-zA-Z0-9_]+)`", m.group(1)))


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
    assert ("grants no implementation" in s1) or ("no implementation authority" in s1), \
        "section 1 must state no implementation authority"
    assert ("PR-5H replaces earlier contracts only where it explicitly says so" in s1) or \
           ("replaces earlier contracts only where" in s1) or \
           ("precedence" in s1.lower()), \
        "section 1 must contain precedence language"


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

    assert "precision: int | None = None" in s3 or \
           "precision: int | None" in s3, \
        "section 3 must mention precision field"
    assert "value_mode" in s3, "section 3 must mention value_mode"
    assert "policy_route" in s3, "section 3 must mention policy_route"
    assert "MappingProxyType" in s3, "section 3 must mention MappingProxyType"

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
# 5. Exact RESOURCE_MATH_STAGES members
# ---------------------------------------------------------------------------


def test_exact_resource_math_stages() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### RESOURCE_MATH_STAGES")
    assert found == RESOURCE_MATH_STAGES, \
        f"RESOURCE_MATH_STAGES mismatch.\nMissing: {RESOURCE_MATH_STAGES - found}\nExtra: {found - RESOURCE_MATH_STAGES}"


# ---------------------------------------------------------------------------
# 6. Exact RESOURCE_MATH_DECISIONS members
# ---------------------------------------------------------------------------


def test_exact_resource_math_decisions() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### RESOURCE_MATH_DECISIONS")
    assert found == RESOURCE_MATH_DECISIONS, \
        f"RESOURCE_MATH_DECISIONS mismatch.\nMissing: {RESOURCE_MATH_DECISIONS - found}\nExtra: {found - RESOURCE_MATH_DECISIONS}"


def test_requires_validation_review_present_in_decisions() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### RESOURCE_MATH_DECISIONS")
    assert "requires_validation_review" in found, \
        "requires_validation_review must be present in RESOURCE_MATH_DECISIONS"


def test_validation_blocked_not_a_decision() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### RESOURCE_MATH_DECISIONS")
    assert "validation_blocked" not in found, \
        "validation_blocked must NOT appear in RESOURCE_MATH_DECISIONS"


# ---------------------------------------------------------------------------
# 7. Exact RESOURCE_FAMILIES members (no donor-shaped values)
# ---------------------------------------------------------------------------


def test_exact_resource_families() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### RESOURCE_FAMILIES")
    assert found == RESOURCE_FAMILIES, \
        f"RESOURCE_FAMILIES mismatch.\nMissing: {RESOURCE_FAMILIES - found}\nExtra: {found - RESOURCE_FAMILIES}"


def test_no_donor_shaped_resource_families() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### RESOURCE_FAMILIES")
    leaked = found & DONOR_SHAPED_RESOURCE_FAMILIES
    assert not leaked, \
        f"Donor-shaped values must not appear in RESOURCE_FAMILIES: {leaked}"


# ---------------------------------------------------------------------------
# 8. Exact COST_FAMILIES members
# ---------------------------------------------------------------------------


def test_exact_cost_families() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### COST_FAMILIES")
    assert found == COST_FAMILIES, \
        f"COST_FAMILIES mismatch.\nMissing: {COST_FAMILIES - found}\nExtra: {found - COST_FAMILIES}"


# ---------------------------------------------------------------------------
# 9. Exact CONSEQUENCE_FAMILIES members
# ---------------------------------------------------------------------------


def test_exact_consequence_families() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### CONSEQUENCE_FAMILIES")
    assert found == CONSEQUENCE_FAMILIES, \
        f"CONSEQUENCE_FAMILIES mismatch.\nMissing: {CONSEQUENCE_FAMILIES - found}\nExtra: {found - CONSEQUENCE_FAMILIES}"


# ---------------------------------------------------------------------------
# 10. Exact COST_TIMING_POLICIES members
# ---------------------------------------------------------------------------


def test_exact_cost_timing_policies() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### COST_TIMING_POLICIES")
    assert found == COST_TIMING_POLICIES, \
        f"COST_TIMING_POLICIES mismatch.\nMissing: {COST_TIMING_POLICIES - found}\nExtra: {found - COST_TIMING_POLICIES}"


# ---------------------------------------------------------------------------
# 11. Exact COST_OUTCOME_POLICIES members
# ---------------------------------------------------------------------------


def test_exact_cost_outcome_policies() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### COST_OUTCOME_POLICIES")
    assert found == COST_OUTCOME_POLICIES, \
        f"COST_OUTCOME_POLICIES mismatch.\nMissing: {COST_OUTCOME_POLICIES - found}\nExtra: {found - COST_OUTCOME_POLICIES}"


# ---------------------------------------------------------------------------
# 12. Exact RESOURCE_MATH_SUBJECT_TYPES members
# ---------------------------------------------------------------------------


def test_exact_resource_math_subject_types() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### RESOURCE_MATH_SUBJECT_TYPES")
    assert found == RESOURCE_MATH_SUBJECT_TYPES, \
        f"RESOURCE_MATH_SUBJECT_TYPES mismatch.\nMissing: {RESOURCE_MATH_SUBJECT_TYPES - found}\nExtra: {found - RESOURCE_MATH_SUBJECT_TYPES}"


# ---------------------------------------------------------------------------
# 13. Exact RESOURCE_MATH_OWNER_DOMAINS members
# ---------------------------------------------------------------------------


def test_exact_resource_math_owner_domains() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### RESOURCE_MATH_OWNER_DOMAINS")
    assert found == RESOURCE_MATH_OWNER_DOMAINS, \
        f"RESOURCE_MATH_OWNER_DOMAINS mismatch.\nMissing: {RESOURCE_MATH_OWNER_DOMAINS - found}\nExtra: {found - RESOURCE_MATH_OWNER_DOMAINS}"


# ---------------------------------------------------------------------------
# 14. Exact QUANTITY_KINDS members
# ---------------------------------------------------------------------------


def test_exact_quantity_kinds() -> None:
    s4 = section(4)
    found = _extract_numbered_set(s4, r"### QUANTITY_KINDS")
    assert found == QUANTITY_KINDS, \
        f"QUANTITY_KINDS mismatch.\nMissing: {QUANTITY_KINDS - found}\nExtra: {found - QUANTITY_KINDS}"


# ---------------------------------------------------------------------------
# 15. Stage subsets are subsets of RESOURCE_MATH_STAGES
# ---------------------------------------------------------------------------


def test_stage_subsets_are_subsets_of_stages() -> None:
    s4 = section(4)
    subsets = {
        "DECLARATION_PROGRESS_STAGES": DECLARATION_PROGRESS_STAGES,
        "SOURCE_LOCAL_STAGES": SOURCE_LOCAL_STAGES,
        "VALIDATION_BLOCK_STAGES": VALIDATION_BLOCK_STAGES,
        "OWNER_HANDOFF_STAGES": OWNER_HANDOFF_STAGES,
        "MISSING_DEPENDENCY_STAGES": MISSING_DEPENDENCY_STAGES,
        "POLICY_BLOCK_STAGES": POLICY_BLOCK_STAGES,
        "HIDDEN_INFORMATION_BLOCK_STAGES": HIDDEN_INFORMATION_BLOCK_STAGES,
        "QUARANTINE_STAGES": QUARANTINE_STAGES,
        "ESCALATION_STAGES": ESCALATION_STAGES,
    }
    for name, expected in subsets.items():
        found = _extract_stage_subset(s4, name)
        extra = found - RESOURCE_MATH_STAGES
        assert not extra, \
            f"{name} contains values not in RESOURCE_MATH_STAGES: {extra}"
        assert found == expected, \
            f"{name} mismatch.\nMissing: {expected - found}\nExtra: {found - expected}"


# ---------------------------------------------------------------------------
# 16. Provenance summary table present
# ---------------------------------------------------------------------------


def test_provenance_summary_table_present() -> None:
    s4 = section(4)
    assert "### Provenance summary" in s4 or "### Provenance" in s4, \
        "section 4 must contain a provenance summary table"
    assert "Originating artifact" in s4, \
        "provenance table must mention originating artifact"
    assert "PR-5H changes" in s4, \
        "provenance table must indicate whether PR-5H changes each set"


# ---------------------------------------------------------------------------
# 17. All constant set names present
# ---------------------------------------------------------------------------


def test_all_constant_set_names_present() -> None:
    text = read(ARTIFACT)
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
        "PARTIAL_SETTLEMENT_POLICIES",
        "DECLARATION_PROGRESS_STAGES",
        "SOURCE_LOCAL_STAGES",
    ]
    for name in constant_names:
        assert name in text, f"controlled constant '{name}' not found in artifact"


# ---------------------------------------------------------------------------
# 18. Exhaustive bundle compatibility and unlisted-invalid
# ---------------------------------------------------------------------------


def test_exhaustive_bundle_compatibility_and_unlisted_invalid() -> None:
    s5 = section(5)

    atomicity_tokens = [
        "all_or_nothing_requested",
        "best_effort_requested",
        "ordered_partial_allowed",
        "unordered_partial_allowed",
        "alternative_exactly_one",
        "alternative_at_least_one",
        "alternative_at_most_one",
        "alternative_any",
        "blocked_pending_transaction_policy",
        "invalid_mixed_atomicity",
    ]
    for token in atomicity_tokens:
        assert token in s5, f"atomicity token '{token}' not found in section 5"

    assert "no_partial_settlement" in s5
    assert "partial_settlement_allowed" in s5
    assert "len(term_ids)" in s5
    assert ("not expressly listed" in s5.lower() and "invalid" in s5.lower()) or \
           ("unlisted" in s5.lower() and "invalid" in s5.lower()), \
        "section 5 must state unlisted combinations are invalid"


# ---------------------------------------------------------------------------
# 19. Five dependency lifecycle states
# ---------------------------------------------------------------------------


def test_five_dependency_lifecycle_states() -> None:
    s6 = section(6)
    lower = s6.lower()

    assert "satisfied binding" in lower
    assert "incomplete binding" in lower
    assert "missing binding" in lower
    assert "required but unsatisfied" in lower or \
           ("required" in lower and "unsatisfied" in lower)
    assert "advisory optional unsatisfied" in lower or \
           ("advisory" in lower and "optional" in lower)
    assert "blocked_missing_dependency" in s6


# ---------------------------------------------------------------------------
# 20. Incomplete bindings permit blocked result construction
# ---------------------------------------------------------------------------


def test_incomplete_bindings_permit_blocked_result() -> None:
    s6 = section(6)
    assert "structurally valid" in s6.lower() or "structurally valid" in s6, \
        "section 6 must state incomplete binding is structurally valid"
    assert "not resolution-ready" in s6.lower() or "not resolution-ready" in s6, \
        "section 6 must state incomplete binding is not resolution-ready"
    assert "blocked_missing_dependency" in s6, \
        "section 6 must route incomplete binding to blocked_missing_dependency"


def test_missing_bindings_reject_request() -> None:
    s6 = section(6)
    assert "invalid" in s6.lower(), \
        "section 6 must state missing binding makes request invalid"
    assert "reject" in s6.lower() or "factories" in s6.lower(), \
        "section 6 must state rejection for missing binding"
    assert "No `ResourceMathResult` may be constructed" in s6 or \
           "no result" in s6.lower() or "no `ResourceMathResult`" in s6.lower(), \
        "section 6 must state no result for missing binding"


# ---------------------------------------------------------------------------
# 21. Settlement eligibility requires satisfied dependencies
# ---------------------------------------------------------------------------


def test_settlement_eligibility_requires_satisfied_dependencies() -> None:
    s10 = section(10)
    lower = s10.lower()
    assert "level a" in lower or "Level A" in s10, \
        "section 10 must define Level A (structural validation)"
    assert "level b" in lower or "Level B" in s10, \
        "section 10 must define Level B (proposal-eligibility)"
    assert "structurally valid" in lower, \
        "section 10 Level A must allow structurally valid incomplete requests"
    assert "settlement-eligible" in lower or "settlement eligible" in lower, \
        "section 10 Level B must reference settlement eligibility"
    assert "satisfied" in lower, \
        "section 10 Level B must require satisfied dependencies"


# ---------------------------------------------------------------------------
# 22. ResourceMathResult does not own resource_math_result_ref
# ---------------------------------------------------------------------------


def test_result_does_not_own_resource_math_result_ref() -> None:
    s6 = section(6)
    result_block_m = re.search(
        r"\*\*`ResourceMathResult\.dependencies`\*\*.*?(?=\*\*`SettlementProposal|\Z)",
        s6, flags=re.S,
    )
    assert result_block_m, "section 6 must define ResourceMathResult.dependencies"
    result_block = result_block_m.group(0)
    assert "resource_math_result_ref" not in result_block.split("does not own")[0] or \
           "does not own" in result_block, \
        "ResourceMathResult.dependencies must not own resource_math_result_ref"
    assert "does not own a `resource_math_result_ref` self-binding" in s6, \
        "section 6 must explicitly state no self-binding"


# ---------------------------------------------------------------------------
# 23. Exact request/result/proposal dependency ownership
# ---------------------------------------------------------------------------


def test_exact_dependency_ownership() -> None:
    s6 = section(6)

    request_block_m = re.search(
        r"\*\*`ResourceMathRequest\.dependencies`\*\*.*?(?=\*\*`ResourceMathResult)",
        s6, flags=re.S,
    )
    assert request_block_m, "section 6 must define ResourceMathRequest.dependencies"
    request_block = request_block_m.group(0)

    request_deps = {"subject_ref", "unit_ref", "dimension_ref", "command_ref",
                    "action_legality_ref", "state_projection_ref", "provenance_ref",
                    "rng_result_ref", "table_oracle_result_ref", "owner_handoff_ref",
                    "runtime_trace_ref"}
    for dep in request_deps:
        assert dep in request_block, \
            f"ResourceMathRequest.dependencies must reference {dep}"

    result_block_m = re.search(
        r"\*\*`ResourceMathResult\.dependencies`\*\*.*?(?=`ResourceMathResult` does not own|$)",
        s6, flags=re.S,
    )
    assert result_block_m
    result_block = result_block_m.group(0)
    assert "resource_math_request_ref" in result_block
    assert "validation_request_ref" in result_block
    assert "validation_result_ref" in result_block
    assert "runtime_trace_ref" in result_block

    proposal_block_m = re.search(
        r"\*\*`SettlementProposal\.dependencies`\*\*.*?(?=###|\Z)",
        s6, flags=re.S,
    )
    assert proposal_block_m
    proposal_block = proposal_block_m.group(0)
    assert "resource_math_result_ref" in proposal_block
    assert "validation_result_ref" in proposal_block
    assert "state_delta_ref" in proposal_block
    assert "rollback_accounting_ref" in proposal_block
    assert "runtime_trace_ref" in proposal_block


# ---------------------------------------------------------------------------
# 24. Settlement proposal receives both request and result
# ---------------------------------------------------------------------------


def test_settlement_proposal_receives_both_request_and_result() -> None:
    s10 = section(10)

    assert "request: ResourceMathRequest" in s10 or \
           ("request" in s10 and "ResourceMathRequest" in s10)
    assert "result: ResourceMathResult" in s10 or \
           ("result" in s10 and "ResourceMathResult" in s10)
    assert "create_settlement_proposal" in s10
    assert "validate_settlement_proposal" in s10
    assert ("no certificate" in s10.lower()) or ("direct aggregate" in s10.lower())


# ---------------------------------------------------------------------------
# 25. Exact validation order
# ---------------------------------------------------------------------------


def test_exact_request_result_proposal_validation_order() -> None:
    s10 = section(10)
    assert "No repository lookup" in s10 or "no repository lookup" in s10.lower()
    assert ("no caller-supplied" in s10.lower()) or ("No caller-supplied" in s10)


# ---------------------------------------------------------------------------
# 26. Factory/validator parity
# ---------------------------------------------------------------------------


def test_manual_frozen_dataclass_parity_requirement() -> None:
    s11 = section(11)
    lower = s11.lower()
    assert "frozen dataclass" in lower or "frozen-dataclass" in lower
    assert "manually constructed" in lower or "manual" in lower
    assert "shared private helpers" in lower or "shared helpers" in lower
    assert "factory" in lower or "factories" in lower
    assert "validator" in lower or "validators" in lower


# ---------------------------------------------------------------------------
# 27. Internal-only serialization and RT-005 ownership
# ---------------------------------------------------------------------------


def test_internal_only_serialization_and_rt005_ownership() -> None:
    s12 = section(12)
    assert "to_dict" in s12
    assert ("no `to_public_dict`" in s12) or ("no to_public_dict" in s12)
    assert "defensive copies" in s12.lower() or "defensive copies" in s12
    assert "RT-005" in s12


# ---------------------------------------------------------------------------
# 28. Corpus-scale and RT owner boundaries
# ---------------------------------------------------------------------------


def test_corpus_scale_and_rt_owner_boundaries() -> None:
    s12 = section(12)
    assert "RT-002" in s12
    boundary_keywords = ["combat", "ability", "inventory", "mission", "social",
                         "RNG", "persistence", "event", "canon"]
    found = sum(1 for kw in boundary_keywords if kw in s12 or kw.lower() in s12.lower())
    assert found >= 3, \
        f"section 12 must mention at least 3 RT-002 non-absorbed domains, found {found}"


# ---------------------------------------------------------------------------
# 29. Blocker precedence
# ---------------------------------------------------------------------------


def test_exact_blocker_precedence_order() -> None:
    s8 = section(8)
    lower = s8.lower()
    assert "doctrine escalation" in lower or "escalated_to_doctrine" in s8
    assert "quarantine" in lower or "quarantined_for_review" in s8
    assert "hidden" in lower or "blocked_hidden_information" in s8
    assert "missing" in lower or "blocked_missing_dependency" in s8
    assert ("blocked" in lower and "numeric" in lower) or "blocked_incompatible_policy" in s8
    assert "owner handoff" in lower or "requires_owner_handoff" in s8
    assert "source-supported negative" in lower or "negative" in lower
    assert "no blocker" in lower or "none" in lower
    assert "diagnostics" in lower


# ---------------------------------------------------------------------------
# 30. Source-literal contract
# ---------------------------------------------------------------------------


def test_source_supported_negative_uses_universal_literal_contract() -> None:
    s9 = section(9)
    assert "source_literal" in s9
    assert "negative_values_allowed_by_source" in s9
    assert "one line" in s9.lower() or "single line" in s9.lower()
    assert "Cc" in s9 or "control" in s9.lower()
    assert "Cs" in s9 or "surrogate" in s9.lower()
    assert ("no normalization" in s9.lower()) or ("no parsing" in s9.lower())


# ---------------------------------------------------------------------------
# 31. Typed result-scope cardinality
# ---------------------------------------------------------------------------


def test_no_empty_total_typed_scope() -> None:
    s7 = section(7)
    assert "empty typed result scope" in s7.lower() or "empty typed result scope" in s7
    assert "invalid" in s7.lower()
    assert "non-empty" in s7.lower()


def test_accepted_normalized_and_blocked_scope_cardinality() -> None:
    s7 = section(7)
    assert "accepted_for_planning" in s7 or "accepted" in s7.lower()
    assert "normalized_for_planning" in s7 or "normalized" in s7.lower()
    assert "at least one" in s7.lower()
    assert "blocked_missing_dependency" in s7
    assert "dependency-only" in s7.lower() or "dependency-only" in s7


# ---------------------------------------------------------------------------
# 32. PR-5I next step
# ---------------------------------------------------------------------------


def test_exactly_one_pr_5i_next_step() -> None:
    s14 = section(14)
    text = read(ARTIFACT)
    assert "RUNTIME-DOMAIN-PR-5I" in s14
    assert "review gate" in s14.lower()
    assert "next_step_authorized: RUNTIME-DOMAIN-PR-5A" not in text


# ---------------------------------------------------------------------------
# 33. PR-5A not authorized
# ---------------------------------------------------------------------------


def test_pr_5a_not_authorized() -> None:
    text = read(ARTIFACT)
    assert "pr_5a_authorized: false" in text
    assert "PR-5A" in text and "blocked" in text.lower()
    assert "pr_5a_authorized: true" not in text


# ---------------------------------------------------------------------------
# 34. Registry record exactly once
# ---------------------------------------------------------------------------


def test_registry_record_exactly_once() -> None:
    registry = read(REGISTRY)
    count = registry.count(PR5H_ID)
    assert count == 1, f"PR5H_ID should appear exactly once in registry, found {count}"


# ---------------------------------------------------------------------------
# 35. Decision heading exactly once
# ---------------------------------------------------------------------------


def test_decision_heading_exactly_once() -> None:
    decisions = read(DECISIONS)
    heading = f"## {PR5H_ID}"
    count = decisions.count(heading)
    assert count == 1, f"decision heading should appear exactly once, found {count}"


# ---------------------------------------------------------------------------
# 36. Registry version unchanged
# ---------------------------------------------------------------------------


def test_registry_version_unchanged() -> None:
    registry = read(REGISTRY)
    assert re.search(r"^registry_version: 0\.1\.0$", registry, flags=re.M), \
        "registry_version must remain 0.1.0"


# ---------------------------------------------------------------------------
# 37. No resource_consequence_math.py
# ---------------------------------------------------------------------------


def test_no_resource_consequence_math_py() -> None:
    assert not DOMAIN_RESOURCE_MATH.exists(), \
        "resource_consequence_math.py must not exist"


# ---------------------------------------------------------------------------
# 38. No changes under src/
# ---------------------------------------------------------------------------


def test_no_changes_under_src() -> None:
    changed_paths = {line.split(maxsplit=1)[-1].strip() for line in _git_status_short()}
    domain_changes = [p for p in changed_paths if p.startswith("src/astra_runtime/domain/")]
    kernel_changes = [p for p in changed_paths if p.startswith("src/astra_runtime/kernel/")]
    assert not domain_changes, f"unexpected changes under domain/: {domain_changes}"
    assert not kernel_changes, f"unexpected changes under kernel/: {kernel_changes}"


# ---------------------------------------------------------------------------
# 39. Changed-file footprint
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
# 40. Closure ledger - all eight closed
# ---------------------------------------------------------------------------


def test_closure_ledger_all_eight_closed() -> None:
    s13 = section(13)
    lower = s13.lower()
    closed_count = lower.count("closed")
    assert closed_count >= 8, \
        f"section 13 must contain 'closed' at least 8 times, found {closed_count}"
    assert "effective contract matrix" in lower or "final effective contract" in lower
    assert "atomicity" in lower
    assert "dependency lifecycle" in lower or "unsatisfied binding" in lower
    assert "typed" in lower and "scope" in lower
    assert "blocker" in lower and "precedence" in lower
    assert "source" in lower and "literal" in lower and "negative" in lower
    assert "proposal" in lower and "request" in lower and "validation" in lower
    assert "factory" in lower and "validator" in lower and "parity" in lower


# ---------------------------------------------------------------------------
# 41. All compatibility decisions belong to RESOURCE_MATH_DECISIONS
# ---------------------------------------------------------------------------


def test_compatibility_decisions_in_resource_math_decisions() -> None:
    s8 = section(8)
    rows = re.findall(r"\|\s*\d+\s*\|[^|]+\|[^|]+\|\s*`([^`]+)`\s*\|", s8)
    decisions_in_blocker = {d for d in rows if d != "Per matrix"}
    extra = decisions_in_blocker - RESOURCE_MATH_DECISIONS
    assert not extra, \
        f"Blocker table uses decisions not in RESOURCE_MATH_DECISIONS: {extra}"
    assert len(decisions_in_blocker) >= 5, \
        f"Blocker table should reference at least 5 decisions, found {len(decisions_in_blocker)}"


# ---------------------------------------------------------------------------
# 42. Hidden-info-safe distinction
# ---------------------------------------------------------------------------


def test_hidden_info_safe_distinction() -> None:
    s6 = section(6)
    assert "hidden_info_safe=False" in s6 or "hidden_info_safe=false" in s6.lower()
    assert ("not the same as unsatisfied" in s6.lower()) or \
           ("not the same as" in s6.lower() and "unsatisfied" in s6.lower())
