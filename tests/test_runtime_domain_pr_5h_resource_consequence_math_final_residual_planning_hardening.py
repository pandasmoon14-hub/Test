from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
RESOURCE_MATH_MODULE = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"

ARTIFACT_ID = "RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001"
AUTHORIZED_FILES = {
    "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md",
    "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py",
    "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
    "docs/decisions/current_decisions_log.md",
}
FALSE_ONLY = [
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


def doc_text() -> str:
    return DOC.read_text()


def contract() -> dict:
    text = doc_text()
    match = re.search(r"```yaml pr5h_effective_contract\n(.*?)\n```", text, re.S)
    assert match, "machine-readable PR-5H contract block is missing"
    return json.loads(match.group(1))


def field_map(shape: str) -> dict[str, tuple[str, str]]:
    return {
        item["field"]: (item["annotation"], item["default"])
        for item in contract()["future_shapes"][shape]
    }


def test_exact_ten_shape_field_inventory_annotations_and_defaults() -> None:
    shapes = contract()["future_shapes"]
    assert list(shapes) == [
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
    assert field_map("QuantitySpecification")["precision"] == ("int | None", "None")
    assert field_map("CostTerm")["value_mode"] == ("str", "required")
    assert field_map("CostTerm")["policy_route"] == ("str | None", "None")
    assert field_map("ConsequenceTerm")["value_mode"] == ("str", "required")
    assert field_map("ConsequenceTerm")["policy_route"] == ("str | None", "None")
    assert "stage" not in field_map("ResourceMathRequest")
    assert "request_id" not in field_map("SettlementProposal")
    assert "bundle_policy" not in field_map("CostBundle")
    assert {"atomicity_policy", "ordering_policy", "partial_settlement_policy"} <= set(field_map("CostBundle"))


def test_absence_of_invented_aliases_and_exact_typed_scope_fields() -> None:
    text = doc_text()
    assert "scoped_" not in text
    expected = [
        "referenced_subject_binding_ids",
        "referenced_resource_ref_ids",
        "referenced_quantity_ids",
        "referenced_cost_term_ids",
        "referenced_cost_bundle_ids",
        "referenced_consequence_term_ids",
        "referenced_dependency_ids",
    ]
    assert contract()["typed_scope_fields"] == expected
    result_fields = field_map("ResourceMathResult")
    for field in expected:
        assert result_fields[field] == ("tuple[str, ...]", "()")


def test_exact_effective_constants_and_no_donor_shaped_resource_families() -> None:
    constants = contract()["constants"]
    assert constants["RESOURCE_TERM_VALUE_MODES"] == [
        "resource_quantity",
        "resource_reference_only",
        "quantity_only",
        "policy_only",
    ]
    assert constants["RESOURCE_TERM_POLICY_ROUTES"] == [
        "owner_handoff_required",
        "quarantine_required",
        "doctrine_escalation_required",
    ]
    assert constants["QUANTITY_NEGATIVE_VALUE_POLICIES"] == [
        "negative_values_forbidden",
        "negative_values_allowed_by_source",
        "negative_values_require_owner_handoff",
    ]
    assert "validation_passed" in constants["VALIDATION_INTEGRATION_DECISIONS"]
    forbidden = {"hit_points", "spell_slots", "experience_points", "fate_points", "action_points", "movement_points"}
    assert not forbidden & set(constants["RESOURCE_FAMILIES"])
    assert constants["ATOMICITY_POLICIES"] == [
        "all_or_nothing_requested",
        "best_effort_requested",
        "ordered_partial_allowed",
        "unordered_partial_allowed",
        "alternative_exactly_one",
        "alternative_at_least_one",
        "alternative_at_most_one",
        "alternative_any",
        "invalid_mixed_atomicity",
        "blocked_pending_transaction_policy",
    ]


def test_exact_stage_decision_flag_matrix() -> None:
    matrix = contract()["stage_decision_matrix"]
    assert matrix["accepted_for_planning"] == {
        "allowed_stages": ["resource_math_requested", "calculation_ready_for_review"],
        "blocking": False,
        "quarantined": False,
        "escalated": False,
    }
    assert matrix["normalized_for_planning"]["allowed_stages"] == contract()["constants"]["DECLARATION_PROGRESS_STAGES"]
    assert matrix["quarantined_for_review"] == {
        "allowed_stages": ["quarantined_for_review"],
        "blocking": True,
        "quarantined": True,
        "escalated": False,
    }
    assert matrix["escalated_to_doctrine"] == {
        "allowed_stages": ["escalated_to_doctrine"],
        "blocking": True,
        "quarantined": False,
        "escalated": True,
    }


def test_all_nineteen_false_only_fields_on_three_aggregate_shapes() -> None:
    assert contract()["false_only_fields"] == FALSE_ONLY
    for shape in ["ResourceMathRequest", "ResourceMathResult", "SettlementProposal"]:
        fmap = field_map(shape)
        assert {name: fmap[name] for name in FALSE_ONLY} == {name: ("bool", "False") for name in FALSE_ONLY}
    text = doc_text()
    assert "manually constructed frozen dataclasses" in text
    assert "reject any true false-only field" in text


def test_separate_dependency_ownership_and_five_dependency_states() -> None:
    ownership = contract()["dependency_ownership"]
    assert ownership == {
        "request.dependencies": "request/input references",
        "result.dependencies": "request binding, result validation, trace, and result-specific references",
        "proposal.dependencies": "result binding, validation result, state deltas, trace, rollback accounting, and proposal-specific references",
    }
    states = contract()["dependency_lifecycle_states"]
    assert list(states) == [
        "A_complete_binding",
        "B_incomplete_binding",
        "C_missing_or_malformed_binding",
        "D_required_unsatisfied_named_dependency",
        "E_advisory_optional_unsatisfied",
    ]
    assert "required=True, satisfied=True" in states["A_complete_binding"]
    assert "required=True, satisfied=False" in states["B_incomplete_binding"]
    assert "required=False" in states["C_missing_or_malformed_binding"]
    assert "forces blocked_missing_dependency" in states["D_required_unsatisfied_named_dependency"]
    assert "satisfies nothing" in states["E_advisory_optional_unsatisfied"]
    assert "No result self-binding is added" in doc_text()


def test_typed_scope_cardinality_and_closure_rules_are_exact() -> None:
    text = doc_text()
    required_phrases = [
        "Each tuple contains unique non-empty IDs",
        "every ID resolves in the supplied request",
        "combined typed scope cannot be entirely empty",
        "accepted and normalized results require at least one scoped resource, quantity, cost term, cost bundle, or consequence term",
        "subject or advisory dependency scope alone is insufficient",
        "blocked results must scope an actual blocker",
        "blocked_missing_dependency may be dependency-only",
        "bundle scope includes all contained terms",
        "term scope includes applicable quantities and dependencies",
        "all scoped references resolve even for blocked, quarantined, or escalated results",
        "normalized_reference_ids remains diagnostic only",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_blocker_precedence_and_diagnostics_preservation() -> None:
    assert contract()["blocker_precedence"] == [
        "doctrine_escalation",
        "quarantine",
        "hidden_information_block",
        "missing_or_unsatisfied_required_dependency",
        "blocked_numeric_choice_or_incompatible_policy",
        "owner_handoff",
        "validation_review",
        "lawful_source_supported_negative_non_blocking",
        "no_blocker_apply_normal_compatibility_matrix",
    ]
    assert "Preserve every detected blocker in diagnostics" in doc_text()


def test_term_value_modes_policy_routes_and_copresence_matrix() -> None:
    assert contract()["term_value_mode_matrix"] == {
        "resource_quantity": {"resource_ref_id": "required", "quantity_id": "required", "policy_route": "None"},
        "resource_reference_only": {"resource_ref_id": "required", "quantity_id": "None", "policy_route": "None"},
        "quantity_only": {"resource_ref_id": "None", "quantity_id": "required", "policy_route": "None"},
        "policy_only": {"resource_ref_id": "None", "quantity_id": "None", "policy_route": "required RESOURCE_TERM_POLICY_ROUTES"},
    }


def test_complete_costbundle_matrix_and_corrected_bounds() -> None:
    c = contract()
    assert c["cost_bundle_sets"] == {
        "ORDERING_DECLARED_SET": ["unordered_terms", "source_ordered_terms", "dependency_ordered_terms", "priority_ordered_terms"],
        "ORDERING_ORDERED_SET": ["source_ordered_terms", "dependency_ordered_terms", "priority_ordered_terms"],
        "PARTIAL_REVIEW_SET": ["partial_settlement_requires_owner_review", "partial_settlement_requires_validation"],
        "ALTERNATIVE_ATOMICITY_SET": ["alternative_exactly_one", "alternative_at_least_one", "alternative_at_most_one", "alternative_any"],
    }
    rows = c["cost_bundle_matrix"]
    assert len(rows) == 19
    assert any(row[0] == "all_or_nothing_requested" and row[3] == "absent" for row in rows)
    assert any(row[0] == "ALTERNATIVE_ATOMICITY_SET" and "alternative groups required" in row[4] for row in rows)
    text = doc_text()
    for phrase in [
        "Bool bounds are invalid",
        "supplied bounds are positive integers",
        "minimum and maximum are each `<= len(term_ids)`",
        "all-or-nothing bounds are both `None` or both equal to `len(term_ids)`",
        "no term selection or alternative selection",
        "every unlisted atomicity/ordering/partial-settlement combination is invalid",
    ]:
        assert phrase in text


def test_source_literals_negative_policies_and_no_evaluation() -> None:
    text = doc_text()
    for phrase in [
        "non-empty `str`",
        "one line",
        "no leading/trailing whitespace",
        "no CR, LF, tab, NUL, Unicode `Cc`, or Unicode `Cs`",
        "ordinary Unicode text and interior spaces allowed",
        "preserve exactly",
        "no parsing, normalization, arithmetic, or evaluation",
        "including support for `negative_values_allowed_by_source`",
        "`-0`, `-0.0`, and `-0/1`",
    ]:
        assert phrase in text


def test_direct_request_result_proposal_architecture() -> None:
    assert contract()["direct_validation_signatures"] == [
        "create_resource_math_result(*, request: ResourceMathRequest, ...) -> ResourceMathResult",
        "validate_resource_math_result(result: ResourceMathResult, *, request: ResourceMathRequest) -> bool",
        "create_settlement_proposal(*, request: ResourceMathRequest, result: ResourceMathResult, ...) -> SettlementProposal",
        "validate_settlement_proposal(proposal: SettlementProposal, *, request: ResourceMathRequest, result: ResourceMathResult) -> bool",
    ]
    text = doc_text()
    assert "No certificate object, repository lookup, global registry, or `already_validated` boolean" in text
    assert "structurally validate request" in text
    assert "validate proposal against that exact result and request" in text


def test_exact_proposal_eligibility() -> None:
    eligibility = contract()["settlement_eligibility"]
    assert eligibility["requires"] == [
        "result.stage == calculation_ready_for_review",
        "result.decision in {accepted_for_planning, normalized_for_planning}",
        "validation_decision == validation_passed",
        "non-blocking",
        "non-quarantined",
        "non-escalated",
        "every scoped dependency satisfied",
        "no scoped blocker",
        "non-empty unique proposed_state_delta_refs",
        "matching required/satisfied state_delta_ref dependencies",
    ]
    assert eligibility["rejects"] == [
        "accepted_for_planning at resource_math_requested",
        "normalized_for_planning at earlier declaration stages",
        "source_local_retained",
        "blocked, handoff, review, quarantine, or escalation results",
        "event-only consequences",
        "policy-only terms",
    ]


def test_factory_validator_parity_and_internal_only_serialization() -> None:
    text = doc_text()
    for shape in contract()["future_shapes"]:
        snake = re.sub(r"(?<!^)(?=[A-Z])", "_", shape).lower()
        assert f"create_{snake}" in text or "Create/validate parity is required for all ten shapes" in text
        assert f"validate_{snake}" in text or "Create/validate parity is required for all ten shapes" in text
    for phrase in [
        "frozen keyword-only future dataclasses",
        "tuple copying",
        "MappingProxyType",
        "no callable metadata",
        "internal `to_dict()` only",
        "no `to_public_dict`",
        "defensive serialization",
        "no calculation during serialization",
        "RT-005 owns public projection and redaction",
    ]:
        assert phrase in text


def test_tracking_uniqueness_registry_decision_log_and_authority() -> None:
    registry = REGISTRY.read_text()
    decisions = DECISIONS.read_text()
    assert registry.count(ARTIFACT_ID) == 1
    assert decisions.count(f"## {ARTIFACT_ID}") == 1
    assert "version: 0.1.90" in registry
    assert "planning_only" in registry
    assert "pr_5a_authorized: false" in registry
    assert "pr_5a_blocked: true" in registry
    assert "RUNTIME-DOMAIN-PR-5I" in registry
    assert "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py" in registry
    assert "PRs #278 and #279 were abandoned" in decisions
    assert "no implementation authority" in decisions


def test_four_file_footprint_and_absence_of_implementation_module() -> None:
    # The path check intentionally encodes the authorized footprint for review-time enforcement.
    assert AUTHORIZED_FILES == {
        "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md",
        "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py",
        "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
        "docs/decisions/current_decisions_log.md",
    }
    assert not RESOURCE_MATH_MODULE.exists()
