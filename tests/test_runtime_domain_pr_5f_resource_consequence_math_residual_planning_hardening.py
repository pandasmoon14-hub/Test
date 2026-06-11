import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5f_resource_consequence_math_residual_planning_hardening.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
RESOURCE_MATH_MODULE = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"
DOMAIN_DIR = ROOT / "src/astra_runtime/domain"

PR5F_ID = "RUNTIME-DOMAIN-PR-5F-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-001"
LINEAGE_IDS = [
    PR5F_ID,
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


def section(text: str, heading: str) -> str:
    start = text.index(heading)
    next_start = text.find("\n## ", start + 1)
    return text[start:] if next_start == -1 else text[start:next_start]


def test_lineage_and_planning_only_boundary() -> None:
    text = read(ARTIFACT)
    for token in LINEAGE_IDS:
        assert token in text
    for phrase in [
        "planning-only",
        "closes PR-5E residual blockers",
        "implements no code",
        "authorizes only **RUNTIME-DOMAIN-PR-5G",
        "PR-5A remains blocked",
        "PR-5F overrides PR-5D only for the corrections explicitly defined here",
    ]:
        assert phrase in text


def test_backend_first_invariant() -> None:
    text = section(read(ARTIFACT), "## 2. Backend-first invariant")
    for phrase in [
        "The LLM is not the game engine",
        "References are not calculations",
        "Results are not state",
        "Settlement proposals are not transactions",
        "`validation_ready` is not `validation_passed`",
        "No resource change occurs because a record exists",
        "No donor term, source-local construct, generated content, narration, or UI text has resource authority",
        "No canon promotion is authorized",
    ]:
        assert phrase in text


def test_pr_5e_closure_matrix_closes_required_defects() -> None:
    text = section(read(ARTIFACT), "## 3. PR-5E blocker-closure matrix")
    for defect in [
        "missing subject_ref dependency binding",
        "missing unit_ref dependency binding",
        "missing dimension_ref dependency binding",
        "optional-unsatisfied dependency semantics",
        "precision semantics",
        "source-literal control-character and multiline posture",
        "negative-value-policy behavior",
        "blocked-pending-numeric-choice result behavior",
        "CostTerm resource/quantity combinations",
        "ConsequenceTerm resource/quantity combinations",
        "maximum_allowed_terms semantics",
        "proposal validation-result equality",
        "proposal result eligibility",
        "event-only consequence routing",
        "result request/quantity aggregate validation",
        "factory/validator parity",
    ]:
        assert defect in text
    assert "| PR-5E defect | exact PR-5F correction | affected future shape | future validator rule | future test requirement | closure status |" in text
    assert text.count("| closed |") >= 15
    assert "none are left for PR-5A invention" in text


def test_external_dependency_types_and_aggregate_bindings() -> None:
    text = section(read(ARTIFACT), "## 4. External reference dependency completion")
    for dep_type in [
        "`command_ref`",
        "`action_legality_ref`",
        "`state_projection_ref`",
        "`validation_request_ref`",
        "`validation_result_ref`",
        "`runtime_trace_ref`",
        "`owner_handoff_ref`",
        "`provenance_ref`",
        "`rng_result_ref`",
        "`table_oracle_result_ref`",
        "`state_delta_ref`",
        "`transaction_ref`",
        "`event_commitment_ref`",
        "`resource_math_request_ref`",
        "`resource_math_result_ref`",
        "`rollback_accounting_ref`",
        "`subject_ref`",
        "`unit_ref`",
        "`dimension_ref`",
    ]:
        assert dep_type in text
    for binding in [
        "every `ResourceMathSubjectReference.subject_ref_id`: exactly one `subject_ref` dependency",
        "every non-None `ResourceReference.unit_ref_id`: exactly one `unit_ref` dependency",
        "every non-None `ResourceReference.dimension_ref_id`: exactly one `dimension_ref` dependency",
        "every non-None `QuantitySpecification.unit_ref_id`: exactly one `unit_ref` dependency",
        "every non-None `QuantitySpecification.dimension_ref_id`: exactly one `dimension_ref` dependency",
        "enclosing `ResourceMathRequest.dependencies` aggregate",
        "Standalone leaf validators validate only field shape and controlled vocabulary",
        "aggregate `ResourceMathRequest` validator enforces external typed bindings",
        "`required=True`",
        "`satisfied=True`",
        "unique by `dependency_id`",
        "unique by `(dependency_type, reference_id)`",
        "No dependency is dereferenced, looked up, or executed",
    ]:
        assert binding in text


def test_optional_unsatisfied_dependency_semantics() -> None:
    text = section(read(ARTIFACT), "## 5. Optional and unsatisfied dependency semantics")
    for phrase in [
        "Any dependency matching an external field is a binding dependency and must be `required=True` and `satisfied=True`",
        "Any dependency ID named by a term, request field, result field, or proposal field is binding",
        "`required=True` plus `satisfied=False` forces `decision=blocked_missing_dependency`, `blocking=True`, and a lawful stage from `MISSING_DEPENDENCY_STAGES`",
        "`required=False` plus `satisfied=False` is lawful only when no field is bound to it",
        "advisory only",
        "may never satisfy a required binding",
        "`hidden_info_safe=False` requires `blocked_hidden_information` or an RT-005 owner handoff",
        "reject contradictory dependency states",
    ]:
        assert phrase in text


def test_precision_and_scale_rules() -> None:
    text = section(read(ARTIFACT), "## 6. Quantity precision contract")
    for phrase in [
        "precision: int | None = None",
        "`bool` is rejected",
        "positive integer",
        "permitted only when `representation_kind == decimal_exact`",
        "Precision must be `None` for `integer_exact`, `fraction_exact`, `fixed_point_scaled`, `source_literal_only`, and `blocked_pending_numeric_choice`",
        "declaration metadata only",
        "does not compare precision to `magnitude_text`",
        "does not round, truncate, parse, or calculate",
        "`scale: int | None`",
        "`fixed_point_scaled` requires non-bool, non-negative scale",
        "every other representation requires `scale=None`",
    ]:
        assert phrase in text


def test_source_literal_character_rules() -> None:
    text = section(read(ARTIFACT), "## 7. Source-literal character contract")
    for phrase in [
        "`source_literal` must be a non-empty `str`",
        "Leading or trailing whitespace is rejected",
        "Multiline values are rejected",
        "carriage return",
        "line feed",
        "tab",
        "NUL",
        "category `Cc`",
        "category `Cs`",
        "Ordinary Unicode letters, numbers, punctuation, symbols, and spaces are permitted",
        "preserved exactly",
        "No normalization, tokenization, parsing, arithmetic, or evaluation occurs",
        "internal-only",
        "exact ASCII grammars from PR-5D",
    ]:
        assert phrase in text


def test_negative_policy_behavior_including_lexical_minus_zero() -> None:
    text = section(read(ARTIFACT), "## 8. Negative-value policy contract")
    for phrase in [
        "`negative_values_forbidden`",
        "`negative_values_allowed_by_source`",
        "`negative_values_require_owner_handoff`",
        "begins with `-`",
        "`-0`, `-0.0`, and `-0/1` are lexically negative",
        "leading `+` is not negative",
        "rejects any lexically negative `magnitude_text`",
        "`source_literal` is non-empty",
        "`provenance_refs` is non-empty",
        "required/satisfied `provenance_ref` dependency",
        "`decision=requires_owner_handoff`",
        "`stage=blocked_pending_owner_handoff`",
        "`blocking=True`",
        "required/satisfied `owner_handoff_ref` dependency",
        "cannot appear in `accepted_for_planning`, `normalized_for_planning`, or a `SettlementProposal`",
    ]:
        assert phrase in text


def test_blocked_pending_numeric_choice_result_rule() -> None:
    text = section(read(ARTIFACT), "## 9. Blocked numeric choice contract")
    for phrase in [
        "`representation_kind == blocked_pending_numeric_choice`",
        "`decision=blocked_incompatible_policy`",
        "`stage=policy_refs_declared`",
        "`blocking=True`",
        "`quarantined=False`",
        "`escalated=False`",
        "terminal quarantine/escalation pairs",
        "may not appear in `accepted_for_planning`, `normalized_for_planning`, `source_local_retained`, or `SettlementProposal`",
        "No numeric choice is made in PR-5A",
        "ResourceMathResult request aggregate validation and typed scope",
        "create_resource_math_result(",
        "request: ResourceMathRequest",
        "validate_resource_math_result(",
        "result: ResourceMathResult",
        "`result.request_id == request.request_id`",
        "required/satisfied `resource_math_request_ref` dependency",
        "`normalized_reference_ids` remains diagnostic only",
        "referenced_quantity_ids: tuple[str, ...] = ()",
        "Result quantity scope is the union",
        "scoped cost bundles and their scoped `term_ids`",
        "value_mode` is `resource_quantity` or `quantity_only`",
        "not in the typed scope is not inspected",
        "Any scoped required dependency with `satisfied=False`",
        "Any scoped quantity with `representation_kind == blocked_pending_numeric_choice`",
        "Any scoped lexically negative quantity using `negative_values_require_owner_handoff`",
        "Any scoped `CostTerm` or `ConsequenceTerm` with `value_mode=policy_only`",
        "aggregate-only; leaf validators do not inspect request contents",
    ]:
        assert phrase in text


def test_term_value_modes_and_copresence_matrix() -> None:
    text = section(read(ARTIFACT), "## 10. Term value-mode contract")
    for phrase in [
        "`RESOURCE_TERM_VALUE_MODES`",
        "`resource_quantity`",
        "`resource_reference_only`",
        "`quantity_only`",
        "`policy_only`",
        "value_mode: str",
        "No default",
        "| `resource_quantity` | required | required |",
        "| `resource_reference_only` | required | must be `None` |",
        "| `quantity_only` | must be `None` | required |",
        "| `policy_only` | must be `None` | must be `None` |",
        "all supplied internal IDs must resolve",
        "no value mode calculates affordability or applies a consequence",
        "policy_only` only with an explicit owner handoff, quarantine, or doctrine-escalation route",
    ]:
        assert phrase in text


def test_corrected_bundle_min_max_rules() -> None:
    text = section(read(ARTIFACT), "## 11. Cost-bundle bound semantics")
    for phrase in [
        "minimum_required_terms: int | None = None",
        "maximum_allowed_terms: int | None = None",
        "`bool` is rejected",
        "positive integers",
        "future downstream settlement policy may select",
        "No selection occurs in PR-5A",
        "`minimum_required_terms <= len(term_ids)`",
        "`maximum_allowed_terms <= len(term_ids)`",
        "`minimum_required_terms <= maximum_allowed_terms`",
        "`atomicity_policy == all_or_nothing_requested`",
        "bounds may both be `None`, or both must equal `len(term_ids)`",
        "alternative groups remain subject to unique-group, contained-member, and no-overlap rules",
        "replaces the prior rule requiring `maximum_allowed_terms` to be at least `len(term_ids)`",
    ]:
        assert phrase in text
    inherited_atomicity_literals = {
        "all_or_nothing_requested",
        "best_effort_requested",
        "ordered_partial_allowed",
        "unordered_partial_allowed",
        "alternative_settlement_requested",
    }
    referenced_atomicity_literals = set(
        re.findall(
            r"(?:all_or_nothing|best_effort|ordered_partial|unordered_partial|alternative_settlement)_[a-z_]+",
            text,
        )
    )
    assert referenced_atomicity_literals
    assert referenced_atomicity_literals <= inherited_atomicity_literals
    assert "all_or_nothing_required" not in read(ARTIFACT)


def test_settlement_proposal_result_equality_and_eligibility() -> None:
    text = section(read(ARTIFACT), "## 12. Settlement-proposal result eligibility")
    for phrase in [
        "constructed only against a supplied `ResourceMathResult` object",
        "create_settlement_proposal(*, result: ResourceMathResult, ...)",
        "validate_settlement_proposal(",
        "No repository lookup or dereference occurs",
        "`proposal.result_id == result.result_id`",
        "`proposal.validation_result_ref_id == result.validation_result_ref_id`",
        "`proposal.validation_decision == result.validation_decision`",
        "`result.validation_decision == validation_passed`",
        "`result.validation_result_ref_id` is non-empty",
        "`result.stage == calculation_ready_for_review`",
        "`accepted_for_planning` or `normalized_for_planning`",
        "`result.blocking is False`",
        "`result.quarantined is False`",
        "`result.escalated is False`",
        "No false-only authority field is true",
        "`validation_ready`",
        "`validation_failed`",
        "blocked",
        "quarantined",
        "escalated",
        "source_local_retained",
        "awaiting owner handoff",
        "awaiting validation review",
        "missing dependencies",
        "non-mutating and non-authoritative",
    ]:
        assert phrase in text


def test_state_delta_and_event_only_route() -> None:
    text = section(read(ARTIFACT), "## 13. State-delta requirement and event-only routing")
    for phrase in [
        "`SettlementProposal.proposed_state_delta_refs` must be non-empty and unique",
        "required/satisfied `state_delta_ref` dependency",
        "only for proposed resource/consequence state changes",
        "purely event-only consequence with no proposed state delta does not create a `SettlementProposal`",
        "`ConsequenceTerm` using `value_mode=policy_only`",
        "route through `requires_owner_handoff`, quarantine, or doctrine escalation",
        "RT-001, RT-003, RT-006, RT-007, RT-010",
        "RT-002 does not append or commit events",
        "PR-5A does not add a proposed-event shape",
    ]:
        assert phrase in text


def test_internal_external_reference_integrity() -> None:
    text = section(read(ARTIFACT), "## 14. Internal and external reference integrity")
    for phrase in [
        "`subject_binding_id`",
        "`resource_ref_id`",
        "`quantity_id`",
        "`cost_term_id`",
        "`cost_bundle_id`",
        "`consequence_term_id`",
        "`dependency_id`",
        "must be unique and every internal reference must resolve",
        "subject, unit, dimension, command, action legality, state projection, validation, trace, provenance, owner handoff, RNG/table, request/result, state delta, transaction, event commitment, and rollback accounting",
        "exact typed dependency binding",
        "No external object existence is checked in PR-5A",
    ]:
        assert phrase in text


def test_factory_validator_parity_and_serialization() -> None:
    text = read(ARTIFACT)
    parity = section(text, "## 15. Factory / validator parity")
    for phrase in [
        "all ten inherited shapes",
        "external field/dependency binding",
        "optional-unsatisfied dependency classification",
        "precision and scale",
        "source-literal characters",
        "negative-value policies",
        "blocked numeric choice",
        "term value modes",
        "bundle bounds",
        "proposal/result compatibility",
        "result/request aggregate validation",
        "non-empty state-delta refs",
        "internal-reference resolution",
        "false-only authority fields",
        "Factories and validators must enforce the same rules",
        "Manual construction of a frozen dataclass must not bypass them",
    ]:
        assert phrase in parity
    serialization = section(text, "## 16. Serialization and hidden information")
    for phrase in [
        "internal `to_dict()` only",
        "no `to_public_dict`",
        "defensive copies",
        "tuple-to-list conversion only in returned copies",
        "no calculations during serialization",
        "no public/model/player/GM projection",
        "RT-005 owns later projection and redaction",
        "source literals, quantities, dependencies, provenance, backend IDs, and hidden owner information remain internal",
    ]:
        assert phrase in serialization


def test_corpus_scale_review_and_gate() -> None:
    text = read(ARTIFACT)
    corpus = section(text, "## 17. Corpus-scale pressure review")
    for phrase in [
        "200-400 mixed donor sources",
        "Fantasy and sci-fi",
        "Cultivation and breakthrough resources",
        "Class/archetype and profession resources",
        "Point-buy and narrative currencies",
        "Cyberware/biotech capacity and psionic fatigue",
        "Horror stress, sanity, corruption",
        "Ammunition, fuel, charges, durability, vehicles, mechs, ships, companions, and summons",
        "Crafting, salvage, requisition, time, opportunity, position, reputation, debt, and obligation",
        "Mission, faction, world, generated-content, persistent campaign, and source-local cosmological consequences",
        "without making donor assumptions Astra defaults",
    ]:
        assert phrase in corpus
    gate = section(text, "## 20. Gate finding")
    assert text.count("gate_finding:") == 1
    for phrase in [
        "resource_consequence_math_residual_planning_hardening_defined: true",
        "pr_5e_blockers_addressed: true",
        "ready_for_pr_5g_review_gate: true",
        "ready_for_pr_5a_implementation: false",
        "runtime_code_authorized_by_this_pr: false",
        "domain_code_authorized_by_this_pr: false",
        "next_step_authorized: RUNTIME-DOMAIN-PR-5G resource and consequence math residual planning hardening review gate",
        "next_step_status: review_gate_only",
    ]:
        assert phrase in gate


def test_pr_5e_closure_ledger_and_non_implementation() -> None:
    text = read(ARTIFACT)
    ledger = section(text, "## 18. PR-5E closure ledger")
    assert ledger.count("| closed |") >= 15
    assert "Every PR-5E blocker is closed" in ledger
    non_impl = section(text, "## 21. Non-implementation reaffirmation")
    for phrase in [
        "runtime/domain implementation",
        "calculations or formulas",
        "expression evaluator",
        "affordability execution",
        "reservation",
        "settlement execution",
        "state mutation",
        "delta application",
        "event append or commitment",
        "persistence or replay",
        "RNG/table execution",
        "combat, ability, inventory, mission, or social mechanics",
        "model, prompt, UI, or live-play behavior",
        "conversion",
        "sourcebook inclusion",
        "canon promotion",
        "implementation_authority: false",
    ]:
        assert phrase in non_impl


def test_registry_and_decision_tracking() -> None:
    registry = read(REGISTRY)
    decisions = read(DECISIONS)
    assert "registry_version: 0.1.0" in registry
    assert registry.count(f"file_id: {PR5F_ID}") == 1
    assert "version: 0.1.88" in registry
    for phrase in [
        "planning hardening only",
        "follows PR-5E",
        "closes PR-5E residual blockers",
        "PR-5A remains blocked",
        "PR-5G is the sole next step",
        "no implementation authority",
    ]:
        assert phrase in registry
    assert decisions.count(f"## {PR5F_ID}") == 1
    for phrase in [
        "planning-hardening-only status is recorded for PR-5F",
        "follows PR-5E",
        "closes PR-5E residual blockers",
        "PR-5A remains blocked",
        "PR-5G is the sole next step",
        "no implementation authority",
    ]:
        assert phrase in decisions


def test_no_runtime_domain_implementation_file_added() -> None:
    assert not RESOURCE_MATH_MODULE.exists()
    assert not any(path.name == "resource_consequence_math.py" for path in DOMAIN_DIR.glob("*.py"))
