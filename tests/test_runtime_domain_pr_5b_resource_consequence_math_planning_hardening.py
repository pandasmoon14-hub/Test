from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5b_resource_consequence_math_planning_hardening.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
DOMAIN_RESOURCE_MATH = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"

PR5B_ID = "RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001"
PR5_ID = "RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001"
PR5C = "RUNTIME-DOMAIN-PR-5C resource and consequence math planning hardening review gate"

CONSTANT_SURFACES = {
    "RESOURCE_MATH_STAGES": [
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
    ],
    "RESOURCE_MATH_DECISIONS": [
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
    ],
    "RESOURCE_FAMILIES": ["pooled_expendable", "currency_like", "source_local_resource"],
    "COST_FAMILIES": ["activation", "reservation_hold", "validation_blocked"],
    "CONSEQUENCE_FAMILIES": ["gain", "social_faction_change", "quarantine_escalation"],
    "COST_TIMING_POLICIES": ["pay_before_resolution", "blocked_pending_validation"],
    "COST_OUTCOME_POLICIES": ["success", "rollback_required"],
    "QUANTITY_KINDS": ["count", "source_literal_quantity", "unknown_pending_review"],
    "QUANTITY_REPRESENTATION_KINDS": [
        "integer_exact",
        "decimal_exact",
        "fraction_exact",
        "fixed_point_scaled",
        "source_literal_only",
        "blocked_pending_numeric_choice",
    ],
    "CONVERSION_POLICIES": ["no_conversion", "escalation_required"],
    "ROUNDING_POLICIES": ["no_rounding", "blocked_pending_rounding_choice"],
    "VISIBILITY_POLICIES": ["public", "hidden", "derived_only"],
    "ATOMICITY_POLICIES": ["all_or_nothing_requested", "alternative_exactly_one"],
    "ORDERING_POLICIES": ["unordered_terms", "blocked_pending_ordering_policy"],
    "PARTIAL_SETTLEMENT_POLICIES": ["no_partial_settlement", "partial_settlement_requires_validation"],
    "RESOURCE_MATH_DEPENDENCY_TYPES": [
        "command_ref",
        "validation_result_ref",
        "runtime_trace_ref",
        "table_oracle_ref",
        "decision_log_ref",
    ],
    "RESOURCE_MATH_SUBJECT_TYPES": ["actor", "state_record", "unknown_pending_review"],
    "RESOURCE_MATH_OWNER_DOMAINS": [
        "RT002_resource_consequence_math",
        "RT011_validation_readiness_tooling",
        "doctrine_escalation",
    ],
}

DATACLASSES = [
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

FALSE_ONLY_FIELDS = [
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
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_artifact_and_lineage_ids_exist() -> None:
    text = read(ARTIFACT)
    assert PR5B_ID in text
    assert PR5_ID in text
    assert "RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001" in text
    assert "planning-only" in text
    assert "hardens the PR-5 proposals" in text
    assert "does not implement code" in text


def test_backend_first_invariant_and_pr5a_block() -> None:
    text = read(ARTIFACT)
    for phrase in [
        "the LLM is not the game engine",
        "RT-002 produces reference-only planning contracts at this stage",
        "no resource truth changes because a request, result, or proposal exists",
        "validation_ready is not validation_passed",
        "settlement proposals are not committed state",
        "donor terminology is not Astra authority",
        "PR-5A blocked",
    ]:
        assert phrase in text


def test_all_exact_constant_surfaces_are_present() -> None:
    text = read(ARTIFACT)
    for surface, values in CONSTANT_SURFACES.items():
        assert f"### {surface}" in text
        for column in [
            "exact value",
            "meaning",
            "lawful use",
            "forbidden interpretation",
            "corpus-scale pressure",
            "extension/escalation route",
        ]:
            assert column in text
        for value in values:
            assert f"`{value}`" in text


def test_stage_model_and_compatibility_matrix_are_exact_enough() -> None:
    text = read(ARTIFACT)
    assert "## 4. Exact stage model" in text
    assert "## 5. Exact decision/stage compatibility matrix" in text
    for stage in CONSTANT_SURFACES["RESOURCE_MATH_STAGES"]:
        assert f"`{stage}`" in text
    for decision in CONSTANT_SURFACES["RESOURCE_MATH_DECISIONS"]:
        assert f"`{decision}`" in text
    for phrase in [
        "terminal",
        "allowed decisions",
        "required references",
        "permitted outputs",
        "forbidden behavior",
        "next lawful stages",
        "blocking posture",
        "transaction-handoff eligibility",
        "No result may claim executable affordability",
    ]:
        assert phrase in text


def test_all_nine_dataclass_contracts_and_common_posture() -> None:
    text = read(ARTIFACT)
    for name in DATACLASSES:
        assert f"### {name}" in text
    for phrase in [
        "@dataclass(frozen=True, kw_only=True)",
        "tuples instead of mutable sequences",
        "MappingProxyType",
        "defensive copying",
        "no callable or executable metadata",
        "no binary floats for authoritative quantities",
        "no calculation in constructors, validators, serializers, or services",
        "string/reference fields are not proof that referenced objects exist",
        "representation_kind",
        "magnitude_text",
        "source_literal",
        "precision",
        "scale",
    ]:
        assert phrase in text


def test_dependency_contract_quantity_term_and_bundle_invariants() -> None:
    text = read(ARTIFACT)
    for phrase in [
        "Fields: `dependency_id`, `dependency_type`, `reference_id`, `owner_domain`, `required`, `satisfied`, `hidden_info_safe`, and `metadata`",
        "Duplicate dependency ids are rejected",
        "Duplicate `(dependency_type, reference_id)` pairs are rejected",
        "Dependencies are references only; no dependency is executed",
        "ResourceReference records subject identity",
        "does not select final resource names",
        "NaN and infinity strings are invalid",
        "binary-float authority is forbidden",
        "conversion and rounding are never implicit",
        "PR-5A performs no parsing or arithmetic",
        "They perform no affordability check and no consequence application",
        "CostBundle requires unique bundle ids and unique term ids",
        "no alternative is selected, and no settlement occurs",
    ]:
        assert phrase in text


def test_request_result_proposal_linkage_false_only_factory_and_serialization() -> None:
    text = read(ARTIFACT)
    for phrase in [
        "ResourceMathRequest references command/action legality",
        "ResourceMathResult binds request identity, stage, decision",
        "SettlementProposal binds result",
        "No shape may apply a delta or append an event",
        "Factories and validators must reject manually constructed objects where any false-only field is true",
        "Manual frozen-dataclass construction cannot bypass rules",
        "to_dict",
        "Tuple-to-list conversion is permitted only in returned copies",
        "Public output must omit hidden backend identifiers",
        "Serialization performs no calculations",
    ]:
        assert phrase in text
    for field in FALSE_ONLY_FIELDS:
        assert f"`{field}`: false" in text


def test_family_matrices_and_decision_ledgers() -> None:
    text = read(ARTIFACT)
    for phrase in [
        "RESOURCE_FAMILIES matrix",
        "COST_FAMILIES matrix",
        "CONSEQUENCE_FAMILIES matrix",
        "Treat 200-400 donor sources as mandatory",
        "Required before PR-5A",
        "binary-float prohibition",
        "Required before executable calculation",
        "selection rules among int, Decimal, Fraction, and fixed point",
        "Required before settlement",
        "cross-platform serialization and replay/hash guarantees",
        "No automatic conversion is authorized",
    ]:
        assert phrase in text


def test_validation_handoffs_risk_ledger_and_exact_gate() -> None:
    text = read(ARTIFACT)
    for phrase in [
        "validation integration requires validation request/result refs",
        "command/action legality requires RT-001",
        "state projection requires state snapshot/projection refs",
        "transaction lifecycle requires transaction/preview prerequisite refs",
        "event commitment requires event commitment/record refs",
        "RNG/table authority requires RT-009",
        "hidden-information handling requires RT-005",
        "provenance requires RT-008",
        "resolved for PR-5A",
        "required before executable calculation",
        "required before settlement/commitment",
        "deferred to named RT owner",
        "doctrine escalation",
    ]:
        assert phrase in text
    assert text.count("gate_finding:") == 1
    assert f"next_step_authorized: {PR5C}" in text
    assert "ready_for_pr_5a_implementation: false" in text
    assert "runtime_code_authorized_by_this_pr: false" in text
    assert "domain_code_authorized_by_this_pr: false" in text


def test_registry_and_decision_log_uniqueness() -> None:
    registry = read(REGISTRY)
    decisions = read(DECISIONS)
    assert registry.count(PR5B_ID) == 1
    assert decisions.count(f"## {PR5B_ID}") == 1
    for text in [registry, decisions]:
        assert "Planning hardening only" in text or "planning_hardening_only" in text
        assert "follows PR-5" in text or "follows_pr_5: true" in text
        assert "exact contracts" in text or "exact_contracts_defined: true" in text
        assert "PR-5A remains blocked" in text or "pr_5a_remains_blocked: true" in text
        assert "PR-5C" in text
        assert "no implementation" in text or "no_implementation_authority: true" in text


def test_no_runtime_domain_file_added() -> None:
    assert not DOMAIN_RESOURCE_MATH.exists()
