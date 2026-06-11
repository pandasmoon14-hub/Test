from __future__ import annotations

from pathlib import Path
import itertools
import re

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
DOMAIN_RESOURCE_MATH = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"

PR5H_ID = "RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001"

STAGE_SETS = {
    "DECLARATION_PROGRESS_STAGES": {
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
    "SOURCE_LOCAL_STAGES": {
        "source_declaration_captured",
        "resource_refs_declared",
        "terms_declared",
        "bundle_structure_declared",
        "policy_refs_declared",
    },
    "VALIDATION_BLOCK_STAGES": {"blocked_pending_validation"},
    "OWNER_HANDOFF_STAGES": {"blocked_pending_owner_handoff"},
    "MISSING_DEPENDENCY_STAGES": {
        "dependency_refs_bound",
        "blocked_pending_validation",
        "blocked_pending_owner_handoff",
    },
    "POLICY_BLOCK_STAGES": {"policy_refs_declared"},
    "HIDDEN_INFORMATION_BLOCK_STAGES": {"dependency_refs_bound", "blocked_pending_validation"},
    "QUARANTINE_STAGES": {"quarantined_for_review"},
    "ESCALATION_STAGES": {"escalated_to_doctrine"},
}

DECISION_MATRIX = {
    "accepted_for_planning": ({"resource_math_requested", "calculation_ready_for_review"}, "False", "False", "False"),
    "normalized_for_planning": (STAGE_SETS["DECLARATION_PROGRESS_STAGES"], "False", "False", "False"),
    "source_local_retained": (STAGE_SETS["SOURCE_LOCAL_STAGES"], "False", "False", "False"),
    "requires_validation_review": (STAGE_SETS["VALIDATION_BLOCK_STAGES"], "True", "False", "False"),
    "requires_owner_handoff": (STAGE_SETS["OWNER_HANDOFF_STAGES"], "True", "False", "False"),
    "blocked_missing_dependency": (STAGE_SETS["MISSING_DEPENDENCY_STAGES"], "True", "False", "False"),
    "blocked_incompatible_policy": (STAGE_SETS["POLICY_BLOCK_STAGES"], "True", "False", "False"),
    "blocked_hidden_information": (STAGE_SETS["HIDDEN_INFORMATION_BLOCK_STAGES"], "True", "False", "False"),
    "quarantined_for_review": (STAGE_SETS["QUARANTINE_STAGES"], "True", "True", "False"),
    "escalated_to_doctrine": (STAGE_SETS["ESCALATION_STAGES"], "True", "False", "True"),
}

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

TEN_SHAPES = {
    "ResourceMathDependency",
    "ResourceMathSubjectReference",
    "ResourceReference",
    "QuantitySpecification",
    "CostTerm",
    "ConsequenceTerm",
    "CostBundle",
    "ResourceMathRequest",
    "ResourceMathResult",
    "SettlementProposal",
}


def read(path: Path = ARTIFACT) -> str:
    return path.read_text(encoding="utf-8")


def section(number: int) -> str:
    text = read()
    match = re.search(rf"^## {number}\. .*?(?=^## {number + 1}\. |\Z)", text, flags=re.M | re.S)
    assert match, f"missing section {number}"
    return match.group(0)


def subsection(number: str) -> str:
    parent = section(int(number.split(".")[0]))
    match = re.search(rf"^### {re.escape(number)} .*?(?=^### \d+\.\d+ |^## \d+\. |\Z)", parent, flags=re.M | re.S)
    assert match, f"missing subsection {number}"
    return match.group(0)


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def markdown_table(block: str, headers: list[str]) -> list[dict[str, str]]:
    lines = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    for i, line in enumerate(lines):
        if split_markdown_row(line) == headers:
            rows: list[dict[str, str]] = []
            for data_line in lines[i + 2 :]:
                cells = split_markdown_row(data_line)
                if len(cells) != len(headers):
                    break
                rows.append(dict(zip(headers, cells)))
            return rows
    raise AssertionError(f"table with headers {headers!r} not found")


def parse_set(value: str) -> set[str]:
    clean = value.strip().strip("`")
    if clean in STAGE_SETS:
        return STAGE_SETS[clean]
    assert clean.startswith("{") and clean.endswith("}"), clean
    return {part.strip().strip('"') for part in clean[1:-1].split(",")}


def field_rows() -> list[dict[str, str]]:
    return markdown_table(
        subsection("3.2"),
        ["shape", "field", "annotation", "default", "controlled surface", "invariant"],
    )


def field_names_by_shape() -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for row in field_rows():
        result.setdefault(row["shape"].strip("`"), set()).add(row["field"].strip("`"))
    return result


def test_artifact_preserves_pr_278_comprehensive_shape_and_non_implementation_boundary() -> None:
    text = read()
    assert PR5H_ID in text
    assert len(re.findall(r"^## \d+\. ", text, flags=re.M)) == 15
    for phrase in [
        "complete ten-shape effective field matrix",
        "complete CostBundle compatibility matrix",
        "five-state dependency lifecycle",
        "dependency aggregate ownership",
        "typed result-scope cardinality and closure",
        "exact eight-level simultaneous blocker precedence",
        "source-literal contract",
        "direct request/result/proposal validation architecture",
        "serialization and hidden-information ownership",
        "PR-5G closure ledger",
        "PR-5A remains blocked",
        "RUNTIME-DOMAIN-PR-5I resource and consequence math final residual planning hardening review gate",
        "PR #279 is not merged, cherry-picked, or wholesale copied",
    ]:
        assert phrase in text
    assert "no `resource_consequence_math.py`" in section(15)
    assert "runtime_code_authorized_by_this_pr: false" in section(15)
    assert "domain_code_authorized_by_this_pr: false" in section(15)
    assert "canon_promotion_authorized_by_this_pr: false" in section(15)
    assert not DOMAIN_RESOURCE_MATH.exists()


def test_complete_ten_shape_effective_field_matrix_and_constants_are_present() -> None:
    shapes = {row["shape"].strip("`") for row in field_rows()}
    assert shapes == TEN_SHAPES
    constants = subsection("3.1")
    for token in [
        "RESOURCE_MATH_SUBJECT_TYPES",
        "RESOURCE_MATH_SUBJECT_ROLES",
        "RESOURCE_MATH_OWNER_DOMAINS",
        "RESOURCE_MATH_DEPENDENCY_TYPES",
        "QUANTITY_REPRESENTATION_KINDS",
        "NEGATIVE_VALUE_POLICIES",
        "TERM_VALUE_MODES",
        "POLICY_ONLY_ROUTES",
        "COST_BUNDLE_POLICIES",
        "VALIDATION_INTEGRATION_DECISIONS",
        "subject_ref",
        "unit_ref",
        "dimension_ref",
    ]:
        assert token in constants


def test_exact_effective_field_names_and_rejected_pr_279_field_names() -> None:
    fields = field_names_by_shape()
    assert "owner_handoff_ref_ids" in fields["ResourceMathRequest"]
    assert "trace_ref_id" in fields["ResourceMathRequest"]
    assert "trace_ref_id" in fields["ResourceMathResult"]
    assert "trace_ref_id" in fields["SettlementProposal"]
    assert "rollback_accounting_refs" in fields["SettlementProposal"]
    assert "request_id" not in fields["SettlementProposal"]

    all_exact_fields = {field for names in fields.values() for field in names}
    assert "owner_handoff_ref" + "_id" not in all_exact_fields
    assert "runtime_trace_ref" + "_id" not in all_exact_fields
    assert "rollback_accounting_ref" + "_id" not in all_exact_fields
    assert "The proposal shape has no stored request identifier field" in subsection("3.2")


def test_complete_incomplete_and_missing_external_bindings_are_distinct() -> None:
    text = subsection("3.3")
    for phrase in [
        "Every external binding field requires exactly one matching dependency record with the correct `dependency_type` and `reference_id`.",
        "The record must have `required=True`.",
        "`satisfied=True` means complete binding.",
        "`satisfied=False` is permitted only as a structurally valid incomplete binding.",
        "An incomplete binding remains linked to the field, is not resolution-ready, and forces `blocked_missing_dependency` for every scoped result that reaches it.",
        "Missing record, wrong type, wrong reference ID, duplicate matching records, or `required=False` invalidates the aggregate before result construction.",
        "Incomplete bindings cannot support accepted, normalized, or proposal-eligible results.",
    ]:
        assert phrase in text
    for field in [
        "ResourceMathSubjectReference.subject_ref_id",
        "ResourceReference.unit_ref_id",
        "ResourceReference.dimension_ref_id",
        "QuantitySpecification.unit_ref_id",
        "QuantitySpecification.dimension_ref_id",
        "ResourceMathRequest.owner_handoff_ref_ids",
        "trace_ref_id",
        "SettlementProposal.rollback_accounting_refs",
    ]:
        assert field in text


def test_five_state_dependency_lifecycle_and_aggregate_ownership() -> None:
    text = section(6)
    assert "`ResourceMathRequest.dependencies` is the sole aggregate owner" in text
    rows = markdown_table(text, ["state", "name", "dependency posture", "aggregate validity", "result/proposal consequence"])
    by_state = {row["state"]: row for row in rows}
    assert set(by_state) == {"A", "B", "C", "D", "E"}
    assert "satisfied=True" in by_state["A"]["dependency posture"]
    assert "satisfied=False" in by_state["B"]["dependency posture"]
    assert "structurally valid but incomplete" in by_state["B"]["aggregate validity"]
    assert "blocked_missing_dependency" in by_state["B"]["result/proposal consequence"]
    assert "never accepted, normalized, or proposal-eligible" in by_state["B"]["result/proposal consequence"]
    assert "missing record" in by_state["C"]["dependency posture"]
    assert "invalid aggregate before result construction" in by_state["C"]["aggregate validity"]
    assert "advisory optional unsatisfied" in by_state["D"]["name"]
    assert "contradictory dependency aggregate" in by_state["E"]["name"]


def test_authoritative_decision_stage_matrix_complete_and_flags_exact() -> None:
    rows = markdown_table(section(5), ["decision", "lawful stage set", "blocking", "quarantined", "escalated"])
    by_decision = {row["decision"].strip("`"): row for row in rows}
    assert set(by_decision) == set(DECISION_MATRIX)
    for decision, (stages, blocking, quarantined, escalated) in DECISION_MATRIX.items():
        row = by_decision[decision]
        assert parse_set(row["lawful stage set"]) == stages
        assert row["blocking"].strip("`") == blocking
        assert row["quarantined"].strip("`") == quarantined
        assert row["escalated"].strip("`") == escalated
    for name, stages in STAGE_SETS.items():
        assert f"`{name} = " in section(5)
        for stage in stages:
            assert stage in section(5)


def test_every_unlisted_decision_stage_pair_is_declared_invalid() -> None:
    text = section(5)
    assert "Every unlisted decision/stage pair is invalid." in text
    all_stages = set().union(*STAGE_SETS.values(), {"resource_math_requested"})
    invalid_pairs = [
        (decision, stage)
        for decision, (allowed, *_flags) in DECISION_MATRIX.items()
        for stage in all_stages
        if stage not in allowed
    ]
    assert ("accepted_for_planning", "source_declaration_captured") in invalid_pairs
    assert ("source_local_retained", "calculation_ready_for_review") in invalid_pairs
    assert ("blocked_hidden_information", "policy_refs_declared") in invalid_pairs


def test_eight_level_blocker_precedence_ordering_and_no_blocker_matrix_pointer_are_preserved() -> None:
    rows = markdown_table(section(8), ["precedence", "condition", "required result route", "notes"])
    assert [row["precedence"] for row in rows] == [str(i) for i in range(1, 10)]
    route_by_precedence = {row["precedence"]: row["required result route"] for row in rows}
    assert "reject before result construction" in route_by_precedence["1"]
    assert "escalated_to_doctrine" in route_by_precedence["2"]
    assert "quarantined_for_review" in route_by_precedence["3"]
    assert "blocked_hidden_information" in route_by_precedence["4"]
    assert "requires_owner_handoff" in route_by_precedence["5"]
    assert "requires_validation_review" in route_by_precedence["6"]
    assert "blocked_missing_dependency" in route_by_precedence["7"]
    assert "blocked_incompatible_policy" in route_by_precedence["8"]
    assert "Section 5" in route_by_precedence["9"]


def test_exact_policy_only_routes_and_hidden_information_route_are_preserved() -> None:
    text = section(4) + section(8) + section(6)
    for phrase in [
        "`doctrine_escalation_required` → `escalated_to_doctrine`",
        "`quarantine_required` → `quarantined_for_review`",
        "`owner_handoff_required` → `requires_owner_handoff`",
        "`validation_review_required` → `requires_validation_review`",
        "`source_local_retained` → `source_local_retained`",
        "PR-5H does not replace exact policy-only routing with a generic `blocked_incompatible_policy` route.",
        "PR-5H does not introduce an alternate unspecified RT-005 handoff result route",
    ]:
        assert phrase in text


def test_cost_bundle_matrix_scope_and_source_literal_contract_are_preserved() -> None:
    bundle = section(9)
    bundle_rows = markdown_table(
        bundle,
        ["bundle_policy", "minimum_required_terms", "maximum_allowed_terms", "term ordering", "partial settlement", "compatibility invariant"],
    )
    assert {row["bundle_policy"].strip("`") for row in bundle_rows} == {
        "all_required",
        "any_one",
        "at_least_minimum",
        "at_most_maximum",
        "exactly_one",
        "ordered_sequence",
        "partial_settlement_allowed",
        "partial_settlement_forbidden",
    }
    assert "No bundle policy can bypass blocker precedence or incomplete binding lifecycle." in bundle

    source = section(10)
    for token in [
        "Leading or trailing whitespace is rejected",
        "Multiline values are rejected",
        "carriage return",
        "line feed",
        "tab",
        "NUL",
        "category `Cc`",
        "category `Cs`",
        "No normalization, tokenization, parsing, arithmetic, or evaluation occurs",
    ]:
        assert token in source


def test_typed_result_scope_cardinality_and_closure_are_preserved() -> None:
    text = section(7)
    for phrase in [
        "`scoped_subject_binding_ids` is non-empty",
        "closed subset of the request aggregate",
        "Scoped terms pull in their `resource_ref_id`, `quantity_id`, and `dependency_refs` closure.",
        "Scoped bundles pull in all `term_ids` and their dependency closure.",
        "Every external binding reached by the typed scope must be state A complete",
        "Empty typed scope is not lawful for accepted, normalized, or settlement-eligible results.",
    ]:
        assert phrase in text


def test_settlement_proposal_eligibility_exact_positive_and_negative_cases() -> None:
    text = section(12)
    for phrase in [
        '`result.stage == "calculation_ready_for_review"`;',
        '`result.decision in {"accepted_for_planning", "normalized_for_planning"}`;',
        "`result.blocking is False`;",
        "`result.quarantined is False`;",
        "`result.escalated is False`;",
        '`result.validation_decision == "validation_passed"`;',
        "all scoped required dependencies are satisfied;",
        "no scoped policy-only, blocked-numeric, hidden-information, missing-dependency, owner-handoff, quarantine, or escalation blocker.",
        "`accepted_for_planning` at `resource_math_requested` is not proposal-eligible.",
        "`source_local_retained` is never proposal-eligible.",
        "Only `accepted_for_planning` or `normalized_for_planning` at `calculation_ready_for_review` may proceed",
    ]:
        assert phrase in text
    for stage in STAGE_SETS["DECLARATION_PROGRESS_STAGES"] - {"calculation_ready_for_review"}:
        assert f"`{stage}`" in text


def test_false_only_fields_and_inclusion_surface_are_complete() -> None:
    rows = markdown_table(subsection("3.4"), ["field", "annotation", "default", "invariant"])
    assert [row["field"].strip("`") for row in rows] == FALSE_ONLY_FIELDS
    assert len(rows) == 19
    for row in rows:
        assert row["annotation"].strip("`") == "bool"
        assert row["default"].strip("`") == "False"
        assert "rejects `True`" in row["invariant"]
        assert "manually constructed frozen dataclasses" in row["invariant"]

    inclusion = markdown_table(subsection("3.4"), ["shape", "included shared surface", "generation rule"])
    assert {row["shape"].strip("`") for row in inclusion} == {
        "ResourceMathRequest",
        "ResourceMathResult",
        "SettlementProposal",
    }
    for row in inclusion:
        assert row["included shared surface"].strip("`") == "FALSE_ONLY_AUTHORITY_FIELDS"
        assert row["generation rule"] == "include all nineteen fields exactly once, each `bool = False`"


def test_direct_validation_architecture_and_serialization_boundary_are_preserved() -> None:
    validation = section(11)
    for phrase in [
        "create_settlement_proposal(*, request: ResourceMathRequest, result: ResourceMathResult, ...)",
        "validate_settlement_proposal(proposal: SettlementProposal, *, request: ResourceMathRequest, result: ResourceMathResult)",
        "There is no repository lookup",
        "stored proposal request identifier",
        "Level A structural validation",
        "Level B aggregate validation",
    ]:
        assert phrase in validation
    serialization = section(13)
    for phrase in [
        "manually constructed frozen dataclasses",
        "Serialization is internal-only",
        "no `to_public_dict`",
        "RT-005",
        "redaction",
        "projection",
    ]:
        assert phrase in serialization


def test_pr_5g_closure_ledger_and_gate_classification_are_preserved() -> None:
    ledger = section(14)
    for phrase in [
        "effective contract inventory could force PR-5A invention",
        "external binding language conflicted with incomplete lifecycle",
        "normal stage/decision matrix was referenced but not present",
        "settlement proposal eligibility was too broad",
        "false-only fields were collapsed",
        "comprehensive_pr_278_contract_preserved: true",
        "pr_5a_authorized: false",
        "next_step_authorized: RUNTIME-DOMAIN-PR-5I resource and consequence math final residual planning hardening review gate",
    ]:
        assert phrase in ledger


def test_registry_and_decision_log_have_single_pr_5h_tracking_entries() -> None:
    registry = read(REGISTRY)
    decisions = read(DECISIONS)
    assert registry.count("version: 0.1.90") == 1
    assert registry.count(f"file_id: {PR5H_ID}") == 1
    assert decisions.count(f"## {PR5H_ID}") == 1
    assert read(REGISTRY).startswith("registry_version: 0.1.0")
    for blob in [registry, decisions]:
        assert PR5H_ID in blob
        assert "PR-5I" in blob
        assert "runtime_code_authorized_by_this_pr: false" in blob
        assert "domain_code_authorized_by_this_pr: false" in blob
        assert "canon_promotion_authorized_by_this_pr: false" in blob
        assert "pr_5a_remains_blocked: true" in blob or "PR-5A remains blocked" in blob
