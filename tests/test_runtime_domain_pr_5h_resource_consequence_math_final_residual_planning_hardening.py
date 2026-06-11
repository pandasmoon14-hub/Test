from __future__ import annotations

from pathlib import Path
import itertools
import re

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
SRC_DIR = ROOT / "src"

PR5H_ID = "RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001"

DECISION_MATRIX = {
    "accepted_for_planning": {
        "stages": {"resource_math_requested", "calculation_ready_for_review"},
        "blocking": "False",
        "quarantined": "False",
        "escalated": "False",
    },
    "normalized_for_planning": {
        "stages": "DECLARATION_PROGRESS_STAGES",
        "blocking": "False",
        "quarantined": "False",
        "escalated": "False",
    },
    "source_local_retained": {
        "stages": "SOURCE_LOCAL_STAGES",
        "blocking": "False",
        "quarantined": "False",
        "escalated": "False",
    },
    "requires_validation_review": {
        "stages": "VALIDATION_BLOCK_STAGES",
        "blocking": "True",
        "quarantined": "False",
        "escalated": "False",
    },
    "requires_owner_handoff": {
        "stages": "OWNER_HANDOFF_STAGES",
        "blocking": "True",
        "quarantined": "False",
        "escalated": "False",
    },
    "blocked_missing_dependency": {
        "stages": "MISSING_DEPENDENCY_STAGES",
        "blocking": "True",
        "quarantined": "False",
        "escalated": "False",
    },
    "blocked_incompatible_policy": {
        "stages": "POLICY_BLOCK_STAGES",
        "blocking": "True",
        "quarantined": "False",
        "escalated": "False",
    },
    "blocked_hidden_information": {
        "stages": "HIDDEN_INFORMATION_BLOCK_STAGES",
        "blocking": "True",
        "quarantined": "False",
        "escalated": "False",
    },
    "quarantined_for_review": {
        "stages": "QUARANTINE_STAGES",
        "blocking": "True",
        "quarantined": "True",
        "escalated": "False",
    },
    "escalated_to_doctrine": {
        "stages": "ESCALATION_STAGES",
        "blocking": "True",
        "quarantined": "False",
        "escalated": "True",
    },
}

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


def read(path: Path = ARTIFACT) -> str:
    return path.read_text(encoding="utf-8")


def section(number: int) -> str:
    text = read()
    match = re.search(rf"^## {number}\. .*?(?=^## {number + 1}\. |\Z)", text, flags=re.M | re.S)
    assert match, f"missing section {number}"
    return match.group(0)


def subsection(number: str) -> str:
    text = section(int(number.split(".")[0]))
    match = re.search(rf"^### {re.escape(number)} .*?(?=^### \d+\.\d+ |^## \d+\. |\Z)", text, flags=re.M | re.S)
    assert match, f"missing subsection {number}"
    return match.group(0)


def split_markdown_row(line: str) -> list[str]:
    body = line.strip().strip("|")
    cells = re.split(r"(?<!\\)\|", body)
    return [cell.strip().replace(r"\|", "|") for cell in cells]


def markdown_table(block: str, headers: list[str]) -> list[dict[str, str]]:
    lines = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    for i, line in enumerate(lines):
        cells = split_markdown_row(line)
        if cells == headers:
            rows = []
            for data_line in lines[i + 2 :]:
                data_cells = split_markdown_row(data_line)
                if len(data_cells) != len(headers):
                    break
                rows.append(dict(zip(headers, data_cells)))
            return rows
    raise AssertionError(f"table with headers {headers!r} not found")


def parse_inline_set(value: str) -> set[str]:
    match = re.fullmatch(r"`?\{(.+)\}`?", value.strip())
    assert match, value
    return {item.strip().strip("`\"") for item in match.group(1).split(",")}


def stages_for(row_value: str) -> set[str]:
    clean = row_value.strip("`")
    if clean in STAGE_SETS:
        return STAGE_SETS[clean]
    return parse_inline_set(clean)


def test_status_lineage_and_non_implementation_boundary() -> None:
    text = read()
    for token in [
        PR5H_ID,
        "planning-only",
        "PR-5A remains blocked",
        "RUNTIME-DOMAIN-PR-5I resource and consequence math final residual planning hardening review gate",
        "inherited constant vocabularies",
        "donor-shaped leakage",
        "dependency ownership",
        "Level A/Level B validation distinction",
        "implements no code",
        "modifies no `src/` file",
    ]:
        assert token in text
    assert "no `resource_consequence_math.py`" in section(10)
    assert "runtime_code_authorized_by_this_pr: false" in section(10)
    assert "domain_code_authorized_by_this_pr: false" in section(10)
    assert "canon_promotion_authorized_by_this_pr: false" in section(10)


def test_section_3_external_field_bindings_distinguish_complete_incomplete_and_missing() -> None:
    lifecycle = subsection("3.1")
    for exact in [
        "Every external binding field requires exactly one matching dependency record with the correct dependency_type and reference_id.",
        "The matching record must always have required=True.",
        "satisfied=True means the binding is complete.",
        "satisfied=False is permitted only as an incomplete binding dependency under Section 6 state B.",
        "A missing record, wrong dependency type, or wrong reference ID is state C and invalidates the request before result construction.",
        "An incomplete dependency can never support an accepted, normalized, or settlement-eligible result.",
    ]:
        assert exact in lifecycle
    assert "must always be satisfied" not in lifecycle

    matrix = markdown_table(
        subsection("3.2"),
        [
            "shape",
            "external binding field",
            "annotation",
            "default",
            "matching dependency_type",
            "matching reference_id",
            "required flag",
            "satisfied lifecycle",
        ],
    )
    keyed = {(row["shape"].strip("`"), row["external binding field"].strip("`")): row for row in matrix}
    expected = {
        ("ResourceMathSubjectReference", "subject_ref_id"): "subject_ref",
        ("ResourceReference", "unit_ref_id"): "unit_ref",
        ("ResourceReference", "dimension_ref_id"): "dimension_ref",
        ("QuantitySpecification", "unit_ref_id"): "unit_ref",
        ("QuantitySpecification", "dimension_ref_id"): "dimension_ref",
    }
    for key, dep_type in expected.items():
        row = keyed[key]
        assert row["matching dependency_type"] == f"`{dep_type}`"
        assert row["required flag"] == "`required=True`"
        assert "complete when `satisfied=True`" in row["satisfied lifecycle"]
        assert "incomplete when `satisfied=False` under Section 6 state B" in row["satisfied lifecycle"]
        assert "missing/wrong type/wrong reference is Section 6 state C" in row["satisfied lifecycle"]


def test_incomplete_required_bindings_are_structural_but_block_acceptance_normalization_and_proposals() -> None:
    rows = markdown_table(
        section(6),
        ["state", "dependency record posture", "structural validity", "result consequence", "proposal consequence"],
    )
    state_b = {row["state"]: row for row in rows}["B incomplete binding"]
    assert "required=True" in state_b["dependency record posture"]
    assert "satisfied=False" in state_b["dependency record posture"]
    assert "structurally valid incomplete binding" in state_b["structural validity"]
    assert "blocked_missing_dependency" in state_b["result consequence"]
    assert "can never support accepted or normalized results" in state_b["result consequence"]
    assert "never settlement-proposal eligible" in state_b["proposal consequence"]

    state_c = {row["state"]: row for row in rows}["C invalid binding"]
    assert "wrong `dependency_type`" in state_c["dependency record posture"]
    assert "wrong `reference_id`" in state_c["dependency record posture"]
    assert "invalid request before result construction" in state_c["structural validity"]


def test_full_decision_stage_compatibility_matrix_contains_exact_inherited_sets_and_flags() -> None:
    rows = markdown_table(
        section(4),
        ["decision", "lawful stage set", "blocking", "quarantined", "escalated"],
    )
    by_decision = {row["decision"].strip("`"): row for row in rows}
    assert set(by_decision) == set(DECISION_MATRIX)

    for decision, expected in DECISION_MATRIX.items():
        row = by_decision[decision]
        assert stages_for(row["lawful stage set"]) == (
            expected["stages"] if isinstance(expected["stages"], set) else STAGE_SETS[expected["stages"]]
        )
        assert row["blocking"].strip("`") == expected["blocking"]
        assert row["quarantined"].strip("`") == expected["quarantined"]
        assert row["escalated"].strip("`") == expected["escalated"]

    for name, stages in STAGE_SETS.items():
        assert f"`{name} = " in section(4)
        for stage in stages:
            assert stage in section(4)


def test_every_unlisted_decision_stage_pair_is_declared_invalid() -> None:
    matrix_text = section(4)
    assert "Every unlisted decision/stage combination is invalid." in matrix_text

    rows = markdown_table(
        matrix_text,
        ["decision", "lawful stage set", "blocking", "quarantined", "escalated"],
    )
    allowed = {row["decision"].strip("`"): stages_for(row["lawful stage set"]) for row in rows}
    all_stages = set().union(*STAGE_SETS.values(), {"resource_math_requested"})
    invalid_pairs = [
        (decision, stage)
        for decision, stage in itertools.product(allowed, all_stages)
        if stage not in allowed[decision]
    ]
    assert invalid_pairs, "test must exercise unlisted combinations"
    assert ("accepted_for_planning", "source_declaration_captured") in invalid_pairs
    assert ("source_local_retained", "calculation_ready_for_review") in invalid_pairs
    assert ("quarantined_for_review", "calculation_ready_for_review") in invalid_pairs


def test_no_blocker_row_points_to_pr_5h_matrix() -> None:
    rows = markdown_table(
        section(5),
        ["condition", "required result routing", "eligible for accepted/normalized planning", "eligible for SettlementProposal"],
    )
    no_blocker = {row["condition"]: row for row in rows}["no blocker after full aggregate validation"]
    assert "Section 4 matrix" in no_blocker["required result routing"]
    assert "unstated historical matrix" not in section(5)


def test_settlement_proposal_requires_calculation_ready_stage_and_exact_positive_combinations() -> None:
    text = section(7)
    for required in [
        "`stage == calculation_ready_for_review`;",
        "`decision in {accepted_for_planning, normalized_for_planning}`;",
        "`blocking=False`;",
        "`quarantined=False`;",
        "`escalated=False`;",
        "`validation_decision == validation_passed`;",
        "all scoped required bindings satisfied;",
        "no scoped policy-only, blocked-numeric, hidden-information, owner-handoff, quarantine, escalation, or unsatisfied-dependency blocker.",
    ]:
        assert required in text
    assert "`accepted_for_planning` at `calculation_ready_for_review` may be settlement-proposal eligible" in text
    assert "`normalized_for_planning` at `calculation_ready_for_review` may be settlement-proposal eligible" in text


def test_negative_settlement_proposal_stage_decision_combinations_are_exact() -> None:
    text = section(7)
    earlier_stages = [
        "source_declaration_captured",
        "subject_refs_bound",
        "resource_refs_declared",
        "quantity_specs_declared",
        "terms_declared",
        "bundle_structure_declared",
        "policy_refs_declared",
        "dependency_refs_bound",
    ]
    exact_sentence = (
        "`normalized_for_planning` at `source_declaration_captured`, `subject_refs_bound`, "
        "`resource_refs_declared`, `quantity_specs_declared`, `terms_declared`, "
        "`bundle_structure_declared`, `policy_refs_declared`, or `dependency_refs_bound` "
        "is lawful planning state but is not settlement-proposal eligible."
    )
    assert exact_sentence in text
    for stage in earlier_stages:
        assert f"`{stage}`" in exact_sentence
    assert "`source_local_retained` is never `SettlementProposal` eligible." in text
    assert "`accepted_for_planning` at `resource_math_requested` is not `SettlementProposal` eligible." in text


def test_false_only_controlled_surface_lists_all_nineteen_fields_exactly_once() -> None:
    surface = subsection("3.3")
    rows = markdown_table(surface, ["field", "annotation", "default", "invariant"])
    fields = [row["field"].strip("`") for row in rows]
    assert fields == FALSE_ONLY_FIELDS
    assert len(fields) == 19
    assert len(set(fields)) == 19
    for row in rows:
        assert row["annotation"].strip("`") == "bool"
        assert row["default"].strip("`") == "False"
        assert row["invariant"] == "false-only authority field"


def test_request_result_and_proposal_explicitly_include_false_only_surface_without_shape_substring_only() -> None:
    rows = markdown_table(subsection("3.3"), ["shape", "included shared surface", "generation rule"])
    by_shape = {row["shape"].strip("`"): row for row in rows}
    assert set(by_shape) == {"ResourceMathRequest", "ResourceMathResult", "SettlementProposal"}
    for shape, row in by_shape.items():
        assert row["included shared surface"].strip("`") == "FALSE_ONLY_AUTHORITY_FIELDS"
        assert row["generation rule"] == "include all nineteen fields exactly once, each `bool = False`"
    assert "No historical lookup is required to identify a PR-5A field" in subsection("3.3")


def test_factories_and_validators_reject_true_values_including_manual_frozen_dataclasses() -> None:
    text = subsection("3.3") + section(8)
    assert "every factory and validator must reject any `True` value" in text
    assert "manually constructed frozen dataclasses" in text
    assert "every `TRUE` value in `FALSE_ONLY_AUTHORITY_FIELDS` is rejected" in text


def test_registry_and_decision_log_track_pr_5h_without_authorizing_pr_5a() -> None:
    registry = read(REGISTRY)
    decisions = read(DECISIONS)
    for blob in [registry, decisions]:
        assert PR5H_ID in blob
        assert "PR-5A remains blocked" in blob or "pr_5a_remains_blocked: true" in blob
        assert "PR-5I" in blob
        assert "runtime_code_authorized_by_this_pr: false" in blob
        assert "domain_code_authorized_by_this_pr: false" in blob
    assert "registry_version: 0.1.0" in registry
    assert "version: 0.1.90" in registry


def test_final_diff_footprint_guard_mentions_authorized_files_only() -> None:
    text = read()
    assert "modifies no `src/` file" in text
    assert SRC_DIR.exists()
