from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = REPO_ROOT / "docs/doctrine/reviews/runtime_domain_pr_5d_resource_consequence_math_final_planning_hardening.md"
REGISTRY = REPO_ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = REPO_ROOT / "docs/decisions/current_decisions_log.md"
PR5D_ID = "RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001"
PR5C_ID = "RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001"
PR5B_ID = "RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001"
PR5_ID = "RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001"
PR4F_ID = "RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001"

RESOURCE_MATH_STAGES = [
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
]

RESOURCE_MATH_DECISIONS = [
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
]

DECISION_ALLOWED_STAGES = {
    "accepted_for_planning": {"resource_math_requested", "calculation_ready_for_review"},
    "normalized_for_planning": {
        "source_declaration_captured",
        "subject_refs_bound",
        "resource_refs_declared",
        "quantity_specs_declared",
        "terms_declared",
        "bundle_structure_declared",
        "policy_refs_declared",
        "dependency_refs_bound",
        "calculation_ready_for_review",
    },
    "source_local_retained": {
        "source_declaration_captured",
        "resource_refs_declared",
        "terms_declared",
        "bundle_structure_declared",
        "policy_refs_declared",
    },
    "requires_validation_review": {"blocked_pending_validation"},
    "requires_owner_handoff": {"blocked_pending_owner_handoff"},
    "blocked_missing_dependency": {
        "dependency_refs_bound",
        "blocked_pending_validation",
        "blocked_pending_owner_handoff",
    },
    "blocked_incompatible_policy": {"policy_refs_declared"},
    "blocked_hidden_information": {"dependency_refs_bound", "blocked_pending_validation"},
    "quarantined_for_review": {"quarantined_for_review"},
    "escalated_to_doctrine": {"escalated_to_doctrine"},
}

SHAPES = [
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


def test_lineage_and_planning_only_status() -> None:
    text = read(ARTIFACT)
    for token in [PR5D_ID, PR5C_ID, PR5B_ID, PR5_ID, PR4F_ID, "RT002_resource_consequence_math_owner_specification.md"]:
        assert token in text
    for token in ["planning-only", "implements no code", "authorizes only", "PR-5A blocked", "PR-5E"]:
        assert token in text


def test_backend_first_invariant() -> None:
    text = read(ARTIFACT)
    for phrase in [
        "The LLM is not the game engine",
        "Reference objects are not calculations",
        "Results are not state",
        "Settlement proposals are not transactions",
        "validation_ready` is not `validation_passed",
        "No resource, cost, consequence, or donor term becomes authoritative",
        "No canon authority is granted",
    ]:
        assert phrase in text


def test_pr_5c_closure_ledger_exists_and_closes_blockers() -> None:
    text = read(ARTIFACT)
    assert "## 17. PR-5C closure ledger" in text
    for blocker in [
        "Free-string validation posture",
        "Untyped subject references",
        "Quarantine/escalation non-blocking mismatch",
        "Dependency refs not structurally bound",
        "Consequence defaults not tied to surfaces",
        "Quantity parsing boundary too loose",
        "Bundle bounds ambiguous",
        "Proposal validation linkage incomplete",
        "Public serialization ownership unresolved",
        "Factory/validator gaps",
        "False-only authority bypass risk",
    ]:
        assert blocker in text
    assert text.count("| closed |") >= 10


def test_validation_integration_replaces_free_string_posture() -> None:
    text = read(ARTIFACT)
    validation_section = text.split("## 3. Validation-integration contract", 1)[1].split("## 4.", 1)[0]
    assert "`validation_posture` is removed" in validation_section
    assert "ResourceReference` and `ConsequenceTerm" in validation_section
    assert "VALIDATION_INTEGRATION_DECISIONS" in validation_section
    assert "ResourceMathRequest` | `validation_request_ref_id` | `str | None` | `None`" in validation_section
    assert "ResourceMathResult` | `validation_result_ref_id` | `str | None` | `None`" in validation_section
    assert "SettlementProposal` | `validation_decision` | `str` | required | must be `validation_passed`" in validation_section
    assert "Every other supplied validation decision requires `validation_result_ref_id`" in validation_section


def test_subject_reference_and_roles() -> None:
    text = read(ARTIFACT)
    assert "ResourceMathSubjectReference" in text
    for field in ["subject_binding_id", "subject_type", "subject_ref_id", "subject_role", "owner_domain"]:
        assert field in text
    for role in [
        "primary_subject", "payer_subject", "beneficiary_subject", "resource_owner",
        "affected_subject", "source_subject", "target_subject", "authority_source", "provenance_source",
    ]:
        assert f"`{role}`" in text
    assert "raw untyped subject IDs are not sufficient" in text
    for cardinality_rule in [
        "ResourceMathRequest.subject_refs` is non-empty",
        "exactly one subject reference in each request has `subject_role == \"primary_subject\"`",
        "zero primary subjects is invalid",
        "multiple primary subjects are invalid",
        "every `ResourceReference.subject_binding_id`, `CostTerm.subject_binding_id`, and `ConsequenceTerm.subject_binding_id` resolves",
    ]:
        assert cardinality_rule in text


def test_stage_decision_blocking_matrix() -> None:
    text = read(ARTIFACT)
    stage_section = text.split("## 5. Stage and decision compatibility", 1)[1].split("## 6.", 1)[0]
    assert '`accepted_for_planning` | `{"resource_math_requested", "calculation_ready_for_review"}`' in stage_section
    for forbidden in [
        "any non-terminal planning stage",
        "validation/review stage",
        "owner-handoff stage",
        "matching blocked stage when available",
    ]:
        assert forbidden not in stage_section
    for stage_set in [
        "DECLARATION_PROGRESS_STAGES",
        "SOURCE_LOCAL_STAGES",
        "VALIDATION_BLOCK_STAGES",
        "OWNER_HANDOFF_STAGES",
        "MISSING_DEPENDENCY_STAGES",
        "POLICY_BLOCK_STAGES",
        "HIDDEN_INFORMATION_BLOCK_STAGES",
        "QUARANTINE_STAGES",
        "ESCALATION_STAGES",
    ]:
        assert stage_set in stage_section
    for decision in [
        "accepted_for_planning", "normalized_for_planning", "source_local_retained",
        "requires_validation_review", "requires_owner_handoff", "blocked_missing_dependency",
        "blocked_incompatible_policy", "blocked_hidden_information", "quarantined_for_review",
        "escalated_to_doctrine",
    ]:
        assert f"`{decision}`" in stage_section
    for exact_rule in [
        "exactly one required/satisfied `validation_request_ref` matching `validation_request_ref_id`",
        "exactly one required/satisfied `owner_handoff_ref` for each owner handoff field reference",
        "Every decision/stage pair not admitted by the table is invalid for PR-5A",
    ]:
        assert exact_rule in stage_section


def test_every_stage_and_decision_has_lawful_compatibility() -> None:
    text = read(ARTIFACT)
    stage_section = text.split("## 5. Stage and decision compatibility", 1)[1].split("## 6.", 1)[0]

    assert set(DECISION_ALLOWED_STAGES) == set(RESOURCE_MATH_DECISIONS)
    for decision, stages in DECISION_ALLOWED_STAGES.items():
        assert stages, f"{decision} must have at least one lawful stage"
        assert f"`{decision}`" in stage_section
        for stage in stages:
            assert stage in RESOURCE_MATH_STAGES
            assert stage in stage_section

    covered_stages = set().union(*DECISION_ALLOWED_STAGES.values())
    assert covered_stages == set(RESOURCE_MATH_STAGES)
    assert "resource_math_requested" in DECISION_ALLOWED_STAGES["accepted_for_planning"]



def test_dependency_field_binding_matrix() -> None:
    text = read(ARTIFACT)
    for dep_type in [
        "command_ref", "action_legality_ref", "state_projection_ref", "validation_request_ref",
        "validation_result_ref", "runtime_trace_ref", "owner_handoff_ref", "provenance_ref",
        "rng_result_ref", "table_oracle_result_ref", "state_delta_ref", "transaction_ref", "event_commitment_ref",
        "resource_math_request_ref", "resource_math_result_ref", "rollback_accounting_ref",
    ]:
        assert f"`{dep_type}`" in text
    for rule in [
        "Every external reference field must have exactly one matching required and satisfied",
        "`dependency_id` is unique",
        "`(dependency_type, reference_id)` is unique",
        "`required=True` and `satisfied=False` forces a blocking result",
        "no dependency is executed or dereferenced",
        "`ResourceMathResult.request_id` | `resource_math_request_ref`",
        "`SettlementProposal.result_id` | `resource_math_result_ref`",
        "`SettlementProposal.rollback_accounting_refs` | `rollback_accounting_ref`",
        "`validation_result_ref_id` may not exist without `validation_decision`",
        "any non-None `validation_decision` requires `validation_request_ref_id`",
    ]:
        assert rule in text


def test_consequence_policy_reuse_and_quantity_lexical_contract() -> None:
    text = read(ARTIFACT)
    for token in [
        "ConsequenceTerm` lawfully reuses `COST_TIMING_POLICIES` and `COST_OUTCOME_POLICIES`",
        "timing_policy=\"blocked_pending_validation\"",
        "outcome_policy=\"validation_blocked\"",
        "does not create duplicate consequence timing/outcome surfaces",
        "magnitude_text` and `source_literal` are strings, never floats",
        "Leading/trailing whitespace is rejected",
        "Case-insensitive NaN and infinity tokens are rejected",
        "`integer_exact` | `magnitude_text` | `^[+-]?(0|[1-9][0-9]*)$`",
        "`decimal_exact` | `magnitude_text` | `^[+-]?(0|[1-9][0-9]*)\\.[0-9]+$`",
        "`fraction_exact` | `magnitude_text` | `^[+-]?(0|[1-9][0-9]*)/[1-9][0-9]*$`",
        "no exponent notation, leading decimal point, trailing decimal point",
        "PR-5A must not instantiate `Decimal`, `Fraction`, `float`",
        "negative values must never be implicitly accepted",
    ]:
        assert token in text


def test_bundle_bounds_alternatives_and_compatibility() -> None:
    text = read(ARTIFACT)
    for token in [
        "`term_ids` must be non-empty and unique",
        "`minimum_required_terms` and `maximum_allowed_terms` are `int | None`",
        "`bool` is rejected as an integer",
        "maximum_allowed_terms` is a declaration bound",
        "cannot be below `len(term_ids)`",
        "unique group IDs",
        "no term in more than one alternative group",
        "No settlement or alternative choice is executed",
        "`best_effort_requested`",
        "`ordered_partial_allowed`",
        "`unordered_partial_allowed`",
        "`alternative_at_least_one`",
        "`alternative_at_most_one`",
        "`alternative_any`",
        "`invalid_mixed_atomicity`",
        "`blocked_pending_transaction_policy`",
        "every combination not listed here is invalid for PR-5A",
        "`ALTERNATIVE_ATOMICITY_SET` | `ORDERING_DECLARED_SET` | `{ \"no_partial_settlement\" }` | absent | invalid: alternative groups required",
    ]:
        assert token in text
    bundle_section = text.split("## 9. CostBundle exact semantics", 1)[1].split("## 10.", 1)[0]
    assert " | any | " not in bundle_section


def test_request_result_proposal_linkage_and_validation_passed_requirement() -> None:
    text = read(ARTIFACT)
    for token in [
        "ResourceMathRequest` must bind request ID",
        "non-empty typed subject bindings with exactly one `primary_subject`",
        "optional validation-request ref",
        "ResourceMathResult` must bind result ID",
        "blocking/quarantine/escalation flags",
        "SettlementProposal` must require proposal ID",
        "one or more unique `proposed_state_delta_refs`",
        "`validation_decision == \"validation_passed\"`",
        "An empty `proposed_state_delta_refs` tuple is invalid",
        "non-mutating proposal",
    ]:
        assert token in text


def test_internal_reference_integrity_and_serialization_boundary() -> None:
    text = read(ARTIFACT)
    for token in [
        "subject-binding IDs must exist",
        "resource-reference IDs must exist",
        "quantity IDs must exist",
        "cost-term IDs must exist",
        "bundle term IDs must exist",
        "consequence IDs must exist",
        "dependency IDs named by terms or requests must exist",
        "no external object lookup occurs",
        "internal `to_dict()` only",
        "must not implement `to_public_dict()`",
        "RT-005/context projection owns all public",
        "hidden source literals, quantities, dependencies, provenance, or backend IDs cannot be exposed",
    ]:
        assert token in text


def test_all_ten_future_shape_contracts_and_false_only_fields() -> None:
    text = read(ARTIFACT)
    assert "@dataclass(frozen=True, kw_only=True)" in text
    for shape in SHAPES:
        assert f"### {shape}" in text
    assert "validation_posture` is not a field" in text
    for flag in FALSE_ONLY_FIELDS:
        assert f"`{flag}`" in text
    assert "all false-only fields default `False`" in text


def test_factory_validator_parity_and_corpus_scale_review() -> None:
    text = read(ARTIFACT)
    for shape_snake in [
        "resource_math_subject_reference", "resource_reference", "quantity_specification",
        "resource_math_dependency", "cost_term", "cost_bundle", "consequence_term",
        "resource_math_request", "resource_math_result", "settlement_proposal",
    ]:
        assert f"create_{shape_snake}" in text
        assert f"validate_{shape_snake}" in text
    for donor_area in [
        "fantasy and sci-fi", "cultivation", "class/archetype", "profession/occupation",
        "point-buy", "narrative/aspect", "cyberware/biotech", "psionics",
        "horror/investigation", "vehicles/mechs/ships", "companions/summons",
        "crafting/salvage/requisition", "debt/faction/mission", "source-local cosmologies",
        "generated content", "persistent campaign consequences",
    ]:
        assert donor_area in text
    for route in ["source_local_retained", "quarantined_for_review", "escalated_to_doctrine", "requires_owner_handoff"]:
        assert route in text


def test_exactly_one_gate_and_pr_5e_selected_while_pr_5a_blocked() -> None:
    text = read(ARTIFACT)
    assert text.count("gate_finding:") == 1
    assert "ready_for_pr_5e_review_gate: true" in text
    assert "ready_for_pr_5a_implementation: false" in text
    assert "runtime_code_authorized_by_this_pr: false" in text
    assert "domain_code_authorized_by_this_pr: false" in text
    assert "next_step_authorized: RUNTIME-DOMAIN-PR-5E resource and consequence math final planning hardening review gate" in text


def test_registry_and_decision_log_tracking_are_exact_once() -> None:
    registry = read(REGISTRY)
    decisions = read(DECISIONS)
    assert registry.startswith("registry_version: 0.1.0")
    assert registry.count(f"file_id: {PR5D_ID}") == 1
    assert decisions.count(f"## {PR5D_ID}") == 1
    for token in [
        "Planning hardening only; follows PR-5C; closes PR-5C contract defects; PR-5A remains blocked; PR-5E is the sole next step; no implementation authority.",
        "version: 0.1.86",
    ]:
        assert token in registry


def test_resource_consequence_math_module_remains_absent_and_no_runtime_domain_files_added() -> None:
    assert not (REPO_ROOT / "src/astra_runtime/domain/resource_consequence_math.py").exists()
    result = subprocess.run(
        ["git", "diff", "--name-status", "HEAD"],
        cwd=REPO_ROOT,
        text=True,
        check=True,
        capture_output=True,
    )
    changed = [line.split("\t", 1) for line in result.stdout.splitlines() if line]
    added_paths = {parts[1] for parts in changed if parts[0] == "A" and len(parts) == 2}
    assert "src/astra_runtime/domain/resource_consequence_math.py" not in added_paths
    assert not [path for path in added_paths if path.startswith("src/astra_runtime/domain/") or path.startswith("src/astra_runtime/kernel/")]
