from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5i_resource_consequence_math_final_residual_planning_hardening_review.md"
PR5H_DOC = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
ARTIFACT_ID = "RUNTIME-DOMAIN-PR-5I-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-REVIEW-001"
TITLE = "RUNTIME-DOMAIN-PR-5I: Resource and Consequence Math Final Residual Planning Hardening Review Gate"
REVIEWED_ID = "RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001"
REVIEWED_FILE = "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md"
NEXT_STEP = "RUNTIME-DOMAIN-PR-5A Resource and Consequence Math Skeleton Implementation"
NEXT_STATUS = "narrow_reference_only_skeleton_authorized"
AUTHORIZED_FILES = [
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
    "docs/doctrine/reviews/runtime_domain_pr_5i_resource_consequence_math_final_residual_planning_hardening_review.md",
    "tests/test_runtime_domain_pr_5i_resource_consequence_math_final_residual_planning_hardening_review.py",
]
DEFECTS = [
    "consolidated effective contract inventory",
    "complete CostBundle compatibility surface",
    "exact dependency lifecycle",
    "exact typed-result-scope cardinality and closure",
    "simultaneous blocker precedence",
    "universal source-literal consistency",
    "request/result/proposal validation architecture",
    "factory/validator parity",
]
SHAPES = [
    "ResourceMathSubjectReference",
    "ResourceReference",
    "QuantitySpecification",
    "CostTerm",
    "CostBundle",
    "ConsequenceTerm",
    "ResourceMathDependency",
    "ResourceMathRequest",
    "ResourceMathResult",
    "SettlementProposal",
]
PR5H_TEST_NAMES = {
    "test_exact_ten_shape_complete_contract_matrix",
    "test_absence_of_aliases_and_exact_typed_scope_fields",
    "test_all_controlled_surfaces_exact",
    "test_exact_stage_decision_flag_matrix",
    "test_all_nineteen_false_only_fields_on_three_aggregate_shapes",
    "test_dependency_ownership_lifecycle_and_bindings",
    "test_typed_scope_cardinality_and_closure_rules_are_exact",
    "test_exact_simultaneous_blocker_table",
    "test_quantity_lexical_grammars_and_execution_bans_exact",
    "test_complete_costbundle_matrix_and_corrected_bounds",
    "test_binding_state_matrix_reconciles_field_invariants",
    "test_external_binding_invariants_allow_structural_incomplete_states",
    "test_dependency_hidden_information_collision_matrix_exact_cases",
    "test_hidden_information_collision_cross_section_consistency",
    "test_source_literals_negative_policies_and_no_evaluation",
    "test_direct_request_result_proposal_architecture_and_eligibility",
    "test_factory_validator_parity_and_private_helper_responsibilities",
    "test_classification_authority_fields_match_registry_and_are_complete",
    "test_corpus_pressure_review_is_explicit",
    "test_resource_math_result_has_no_resource_math_result_ref_self_binding",
}

CRITICAL_IMPLEMENTATION_DERIVABILITY_TESTS = {
    "test_exact_ten_shape_complete_contract_matrix",
    "test_all_controlled_surfaces_exact",
    "test_dependency_ownership_lifecycle_and_bindings",
    "test_typed_scope_cardinality_and_closure_rules_are_exact",
    "test_exact_simultaneous_blocker_table",
    "test_complete_costbundle_matrix_and_corrected_bounds",
    "test_direct_request_result_proposal_architecture_and_eligibility",
    "test_factory_validator_parity_and_private_helper_responsibilities",
}
CRITICAL_IMPLEMENTATION_SOURCE_KEYS = {
    "future_shapes",
    "constants",
    "public_helpers",
    "private_helper_responsibilities",
    "direct_validation_signatures",
    "cost_bundle_matrix",
    "dependency_lifecycle_states",
    "simultaneous_blocker_table",
}


def text() -> str:
    return DOC.read_text(encoding="utf-8")


def fenced_yaml(path: Path, fence_name: str) -> dict:
    match = re.search(rf"```yaml {re.escape(fence_name)}\n(.*?)\n```", path.read_text(encoding="utf-8"), re.DOTALL)
    assert match, f"Missing fenced YAML block {fence_name}."
    data = yaml.safe_load(match.group(1))
    assert isinstance(data, dict)
    return data


def contract() -> dict:
    return fenced_yaml(DOC, "pr5i_review_contract")


def pr5h_contract() -> dict:
    return fenced_yaml(PR5H_DOC, "pr5h_effective_contract")


def registry_records() -> list[dict]:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return records


def pr5i_registry_record() -> dict:
    records = [record for record in registry_records() if record.get("file_id") == ARTIFACT_ID]
    assert len(records) == 1
    return records[0]


def raw_pr5i_registry_record_text() -> str:
    registry = REGISTRY.read_text(encoding="utf-8")
    start = registry.index(f"- file_id: {ARTIFACT_ID}")
    following = registry.find("\n- file_id:", start + 1)
    return registry[start:] if following == -1 else registry[start:following]


def decision_yaml() -> dict:
    body = DECISIONS.read_text(encoding="utf-8")
    section = body.split(f"## {ARTIFACT_ID}", 1)[1]
    match = re.search(r"```yaml\n(.*?)\n```", section, re.DOTALL)
    assert match
    data = yaml.safe_load(match.group(1))
    assert isinstance(data, dict)
    return data["runtime_domain_pr_5i_decision"]


def field_signatures(shape: str) -> list[list[str]]:
    return [[field["field"], field["annotation"], field["default"]] for field in pr5h_contract()["future_shapes"][shape]]


def assert_surface(surface_name: str, expected_keys: set[str]) -> dict:
    surface = contract()[surface_name]
    assert surface["finding"] == "closed"
    assert surface["authoritative_source_file"] == REVIEWED_FILE
    assert surface["authoritative_source_block"] == "pr5h_effective_contract"
    assert set(surface["authoritative_source_keys"]) >= expected_keys
    assert set(surface["authoritative_source_keys"]).issubset(pr5h_contract().keys())
    assert set(surface["focused_test_functions"]).issubset(PR5H_TEST_NAMES)
    assert surface["material_contradictions_remaining"] is False
    assert surface["pr_5a_invention_required"] is False
    return surface


def test_01_pr5i_file_exists_and_identity() -> None:
    assert DOC.exists()
    data = contract()
    assert data["artifact"] == {
        "artifact_id": ARTIFACT_ID,
        "artifact_title": TITLE,
        "artifact_type": "final_residual_planning_hardening_review_gate",
        "implementation_status": "review_only",
        "owner": "RT-002",
    }


def test_02_review_only_status_and_pr5h_review_target_identity() -> None:
    reviewed = contract()["reviewed_artifact"]
    assert reviewed["artifact_id"] == REVIEWED_ID
    assert reviewed["file"] == REVIEWED_FILE
    assert reviewed["source_block"] == "pr5h_effective_contract"
    assert "does not itself implement PR-5A" in text()


def test_03_exact_source_ledger_paths_exist() -> None:
    for source in contract()["source_ledger"]:
        assert (ROOT / source).exists(), source
    assert REVIEWED_FILE in contract()["source_ledger"]


def test_04_pr5h_exact_four_file_scope_review() -> None:
    footprint = contract()["pr_5h_footprint_finding"]
    assert footprint["changed_files_exact"] == [
        "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md",
        "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py",
        "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
        "docs/decisions/current_decisions_log.md",
    ]
    assert footprint["no_src_changed"] is True
    assert footprint["resource_consequence_math_py_created"] is False
    assert footprint["executable_behavior_introduced"] is False
    assert footprint["pr_5a_remained_blocked"] is True
    assert footprint["pr_5i_selected_as_sole_next_step"] is True


def test_05_pr5i_footprint_contract_is_future_stable() -> None:
    footprint = contract()["pr_5i_footprint_finding"]
    assert footprint["changed_files_exact"] == AUTHORIZED_FILES
    assert footprint["src_files_changed"] is False
    assert footprint["reviewed_pr_5h_files_modified"] is False
    assert footprint["resource_consequence_math_module_created_by_pr_5i"] is False
    assert footprint["runtime_or_domain_implementation_added"] is False
    assert not any(path.startswith("src/") for path in footprint["changed_files_exact"])


def test_06_all_eight_pr5g_defects_are_unique_with_distinct_evidence() -> None:
    rows = contract()["pr_5g_closure_matrix"]
    assert len(rows) == 8
    assert [row["defect"] for row in rows] == DEFECTS
    assert len({row["defect"] for row in rows}) == 8
    assert Counter(row["defect"] for row in rows) == Counter({defect: 1 for defect in DEFECTS})
    evidence_key_sets = [tuple(row["evidence"]["authoritative_source_keys"]) for row in rows]
    assert len(set(evidence_key_sets)) == 8
    for row in rows:
        evidence = row["evidence"]
        assert row["finding"] in {"closed", "partially_closed", "open"}
        assert row["finding"] == "closed"
        assert row["pr_5a_would_need_to_invent_behavior"] is False
        assert evidence["authoritative_source_keys"]
        assert evidence["focused_test_functions"]
        assert set(evidence["authoritative_source_keys"]).issubset(pr5h_contract().keys())
        assert set(evidence["focused_test_functions"]).issubset(PR5H_TEST_NAMES)


def test_07_allowed_outcomes_and_selected_gate_are_consistent() -> None:
    data = contract()
    assert data["allowed_gate_outcomes"] == ["AUTHORIZE_PR_5A", "HARDENING_REQUIRED"]
    assert data["selected_gate_outcome"] == "AUTHORIZE_PR_5A"
    assert data["pr_5h_accepted"] is True
    assert data["pr_5a_authorized_as_sole_next_step"] is True
    assert data["pr_5a_blocked"] is False
    assert data["pr_5a_implementation_part_of_this_pr"] is False
    assert data["next_step_authorized"] == NEXT_STEP
    assert data["next_step_status"] == NEXT_STATUS


def test_08_ten_shape_inventory_is_concise_and_cross_checked_against_pr5h() -> None:
    surface = assert_surface("ten_shape_contract_finding", {"future_shapes", "typed_scope_fields"})
    assert surface["reviewed_shape_order"] == SHAPES
    assert set(surface["reviewed_field_signatures"]) == set(SHAPES)
    for shape in SHAPES:
        assert surface["reviewed_field_signatures"][shape] == field_signatures(shape)
    assert surface["resource_math_request_has_no_stage"] is True
    assert surface["settlement_proposal_has_no_request_id"] is True
    assert surface["resource_math_result_has_no_resource_math_result_ref"] is True
    assert surface["cost_bundle_policy_fields"] == ["atomicity_policy", "ordering_policy", "partial_settlement_policy"]
    assert surface["bundle_policy_replacement_exists"] is False


def test_09_constant_surfaces_are_reviewed_without_republishing_values() -> None:
    surface = assert_surface("constant_surface_finding", {"constants", "constant_provenance"})
    assert surface["constant_surface_names"] == list(pr5h_contract()["constants"].keys())
    assert surface["constant_surface_count"] == len(pr5h_contract()["constants"])
    assert "RESOURCE_FAMILIES" in surface["constant_surface_names"]
    assert surface["no_donor_specific_pool_or_economy"] is True


def test_10_stage_decision_compatibility_is_reviewed_by_key_and_count() -> None:
    surface = assert_surface("stage_decision_finding", {"stage_decision_matrix", "false_only_fields"})
    assert surface["decision_names"] == list(pr5h_contract()["stage_decision_matrix"].keys())
    assert surface["decision_count"] == len(pr5h_contract()["stage_decision_matrix"])
    assert surface["validation_blocked_is_resource_math_result_decision"] is False


def test_11_dependency_states_and_binding_matrix_are_reviewed() -> None:
    surface = assert_surface("dependency_lifecycle_finding", {"dependency_lifecycle_states", "binding_state_matrix", "dependency_ownership"})
    assert surface["state_names"] == list(pr5h_contract()["dependency_lifecycle_states"].keys())
    assert surface["binding_state_matrix_rows"] == len(pr5h_contract()["binding_state_matrix"])
    assert surface["ownership_aggregates"] == list(pr5h_contract()["dependency_ownership"].keys())
    assert surface["no_result_self_binding"] is True


def test_12_hidden_information_collision_and_blocker_precedence_are_reviewed() -> None:
    surface = assert_surface("blocker_precedence_finding", {"simultaneous_blocker_table", "dependency_hidden_information_collision_matrix"})
    assert surface["simultaneous_blocker_rows"] == len(pr5h_contract()["simultaneous_blocker_table"])
    assert surface["hidden_information_collision_cases"] == len(pr5h_contract()["dependency_hidden_information_collision_matrix"])
    assert surface["dependency_derived_hidden_information_requires"] == {"required": True, "satisfied": True, "hidden_info_safe": False}


def test_13_typed_scope_cardinality_and_closure_are_reviewed() -> None:
    surface = assert_surface("typed_scope_finding", {"typed_scope_fields", "future_shapes"})
    assert surface["typed_scope_fields"] == pr5h_contract()["typed_scope_fields"]
    assert surface["typed_scope_count"] == 7
    assert surface["normalized_reference_ids_diagnostic_only"] is True


def test_14_quantity_and_source_literal_rules_are_reviewed_by_names() -> None:
    surface = assert_surface("quantity_source_literal_finding", {"quantity_lexical_grammars", "quantity_execution_bans", "constants"})
    assert surface["quantity_grammar_names"] == list(pr5h_contract()["quantity_lexical_grammars"].keys())
    assert surface["execution_ban_count"] == len(pr5h_contract()["quantity_execution_bans"])
    assert surface["lexical_negative_examples"] == ["-0", "-0.0", "-0/1"]
    assert surface["no_source_literal_parsing_or_normalization"] is True


def test_15_cost_bundle_compatibility_is_reviewed_by_names_and_counts() -> None:
    surface = assert_surface("cost_bundle_finding", {"cost_bundle_sets", "cost_bundle_matrix", "cost_bundle_bound_corrections"})
    assert surface["cost_bundle_set_names"] == list(pr5h_contract()["cost_bundle_sets"].keys())
    assert surface["cost_bundle_matrix_rows"] == len(pr5h_contract()["cost_bundle_matrix"])
    assert surface["bound_correction_count"] == len(pr5h_contract()["cost_bundle_bound_corrections"])
    assert surface["no_selection_affordability_reservation_or_settlement_execution"] is True


def test_16_direct_validation_signatures_are_reviewed_concisely() -> None:
    surface = assert_surface("validation_architecture_finding", {"direct_validation_signatures", "settlement_eligibility"})
    assert surface["direct_validation_signature_count"] == len(pr5h_contract()["direct_validation_signatures"])
    assert surface["signature_names"] == ["create_resource_math_result", "validate_resource_math_result", "create_settlement_proposal", "validate_settlement_proposal"]
    assert surface["no_certificate_object"] is True
    assert surface["no_repository_lookup_or_cached_valid_flag"] is True


def test_17_settlement_proposal_eligibility_is_reviewed_without_full_copy() -> None:
    surface = assert_surface("settlement_proposal_finding", {"settlement_eligibility", "future_shapes"})
    assert surface["eligibility_requires_count"] == len(pr5h_contract()["settlement_eligibility"]["requires"])
    assert surface["eligibility_rejects_count"] == len(pr5h_contract()["settlement_eligibility"]["rejects"])
    assert surface["future_pr_5a_may_create_reference_only_module"] is True


def test_18_public_private_helper_parity_is_reviewed() -> None:
    surface = assert_surface("parity_finding", {"public_helpers", "private_helper_responsibilities"})
    assert surface["public_helper_names"] == pr5h_contract()["public_helpers"]
    assert surface["public_helper_count"] == 20
    assert surface["private_responsibility_names"] == pr5h_contract()["private_helper_responsibilities"]


def test_19_serialization_and_rt005_boundaries_are_reviewed() -> None:
    surface = assert_surface("serialization_finding", {"future_shapes", "quantity_execution_bans"})
    assert surface["internal_to_dict_only"] is True
    assert surface["to_public_dict_exists"] is False
    assert surface["rt_005_remains_public_projection_redaction_owner"] is True
    assert surface["no_calculation_during_serialization"] is True


def test_20_owner_boundaries_are_reviewed() -> None:
    surface = assert_surface("owner_boundary_finding", {"authority_false_fields", "false_only_fields"})
    assert surface["rt_002_does_not_absorb_count"] >= 16
    assert surface["owner_boundaries_preserved"] is True


def test_21_corpus_family_pressure_is_reviewed() -> None:
    surface = assert_surface("corpus_pressure_finding", {"constants", "future_shapes"})
    assert len(surface["families_reviewed"]) >= 19
    assert surface["lawful_destinations"] == ["direct Astra mapping", "normalized Astra mapping", "source-local retention", "owner handoff", "quarantine", "doctrine escalation"]
    assert surface["no_donor_default_law_promoted"] is True


def test_22_implementation_derivability_is_reviewed() -> None:
    data = contract()["implementation_derivability_finding"]
    assert data["finding"] == "derivable_without_new_doctrine_decision"
    assert data["authoritative_source_file"] == REVIEWED_FILE
    assert data["authoritative_source_block"] == "pr5h_effective_contract"
    assert set(data["authoritative_source_keys"]).issubset(pr5h_contract().keys())
    assert CRITICAL_IMPLEMENTATION_SOURCE_KEYS.issubset(set(data["authoritative_source_keys"]))
    assert data["focused_test_functions"]
    assert set(data["focused_test_functions"]).issubset(PR5H_TEST_NAMES)
    assert CRITICAL_IMPLEMENTATION_DERIVABILITY_TESTS.issubset(set(data["focused_test_functions"]))
    assert data["pr_5a_can_derive_reference_only_skeleton"] is True
    assert data["material_contradictions_remaining"] is False
    assert data["pr_5a_invention_required"] is False
    assert data["gate_effect"] == "supports_AUTHORIZE_PR_5A"
    assert data["guessed_behavior_required"] is False


def test_23_risk_ledger_exists_and_has_no_omitted_pr5g_defect() -> None:
    ledger = contract()["risk_ledger"]
    assert [row["risk_or_defect"] for row in ledger] == DEFECTS
    for row in ledger:
        assert row["pr_5i_finding"] == "closed"
        assert row["severity"] == "none_remaining"
        assert row["pr_5a_would_need_invention"] is False
        assert row["owner"] == "RT-002"


def test_24_pr5h_tests_are_substantive_not_prose_only() -> None:
    data = contract()["test_coverage_finding"]
    assert data["pr_5h_tests_are_substantive_not_prose_only"] is True
    assert set(data["focused_test_functions"]).issubset(PR5H_TEST_NAMES)
    assert len(data["focused_test_functions"]) >= 10
    assert data["material_contradictions_remaining"] is False


def test_25_authorized_pr5a_future_scope_is_reference_only_and_non_calculating() -> None:
    scope = contract()["future_pr_5a_scope_if_authorized"]
    assert "narrow reference-only resource_consequence_math.py module" in scope["may_create"]
    for allowed in ["immutable frozen keyword-only shapes", "exact constants", "exact factories and validators", "internal defensive serialization", "domain exports", "focused tests"]:
        assert allowed in scope["may_create"]
    forbidden = set(scope["must_not_create"])
    for item in ["formulas", "arithmetic", "settlement", "state mutation or delta application", "conversion", "canon promotion"]:
        assert item in forbidden


def test_26_hardening_outcome_shape_would_keep_pr5a_blocked_if_selected() -> None:
    data = contract()
    if data["selected_gate_outcome"] == "HARDENING_REQUIRED":
        assert data["pr_5a_blocked"] is True
        assert [row for row in data["risk_ledger"] if row["pr_5i_finding"] != "closed"]
    else:
        assert data["pr_5a_blocked"] is False


def test_27_every_pr5i_false_only_authority_field_is_false() -> None:
    block = contract()["false_only_authority_block"]
    assert block
    assert all(value is False for value in block.values())
    for required in ["runtime_code_authorized_by_this_pr", "domain_code_authorized_by_this_pr", "calculation_authorized_by_this_pr", "settlement_authorized_by_this_pr", "state_delta_application_authorized_by_this_pr", "transaction_execution_authorized_by_this_pr", "event_commitment_authorized_by_this_pr", "persistence_authorized_by_this_pr", "replay_authorized_by_this_pr", "rng_execution_authorized_by_this_pr", "model_integration_authorized_by_this_pr", "live_play_authorized_by_this_pr", "ui_authorized_by_this_pr", "conversion_authorized_by_this_pr", "canon_promotion_authorized_by_this_pr"]:
        assert block[required] is False


def test_28_pr5i_did_not_create_src_module_but_future_pr5a_may() -> None:
    data = contract()
    footprint = data["pr_5i_footprint_finding"]
    assert footprint["resource_consequence_math_module_created_by_pr_5i"] is False
    assert not any(path == "src/astra_runtime/domain/resource_consequence_math.py" for path in footprint["changed_files_exact"])
    assert data["pr_5a_implementation_part_of_this_pr"] is False
    assert "narrow reference-only resource_consequence_math.py module" in data["future_pr_5a_scope_if_authorized"]["may_create"]
    assert footprint["src_files_changed"] is False


def test_29_review_contract_is_compact_manifest_not_pr5h_republication() -> None:
    data = contract()
    assert "future_shapes" not in data["ten_shape_contract_finding"]
    assert "constants" not in data["constant_surface_finding"]
    assert "stage_decision_matrix" not in data["stage_decision_finding"]
    assert "simultaneous_blocker_table" not in data["blocker_precedence_finding"]
    assert "cost_bundle_matrix" not in data["cost_bundle_finding"]
    assert len(text().splitlines()) < 2600


def test_30_registry_contains_exactly_one_complete_pr5i_record() -> None:
    record = pr5i_registry_record()
    required = {"file_id", "filename", "proposed_path", "layer", "phase", "status", "authority_level", "owner", "purpose", "owns", "must_not_own", "dependencies", "blocked_by", "unlocks", "downstream_consumers", "donor_pressure_absorbed", "hard_refusals", "escalation_triggers", "required_tests", "test_status", "review_status", "promotion_requirements", "scale_gate_relevance", "broad_conversion_relevance", "canon_relevance", "runtime_relevance", "live_play_relevance", "notes"}
    assert not (required - set(record))
    assert record["implementation_status"] == "review_only"
    assert record["reviewed_pr_5h_artifact"] == REVIEWED_ID
    assert record["reviewed_pr_5h_file"] == REVIEWED_FILE
    raw_record = raw_pr5i_registry_record_text()
    assert "reviewed_pr_5h_artifact:" in raw_record
    assert "*pr5h_artifact" not in raw_record
    assert "&pr5h_artifact" not in REGISTRY.read_text(encoding="utf-8")
    assert "*pr5h_artifact" not in REGISTRY.read_text(encoding="utf-8")


def test_31_registry_lists_are_non_empty_strings() -> None:
    record = pr5i_registry_record()
    for key in ["owns", "must_not_own", "dependencies", "unlocks", "downstream_consumers", "donor_pressure_absorbed", "hard_refusals", "escalation_triggers", "required_tests", "promotion_requirements"]:
        assert isinstance(record[key], list), key
        assert record[key], key
        assert all(isinstance(item, str) and item.strip() for item in record[key]), key


def test_32_registry_next_step_fields_match_review_outcome() -> None:
    record = pr5i_registry_record()
    data = contract()
    assert record["gate_outcome"] == data["selected_gate_outcome"]
    assert record["pr_5a_status"] == data["next_step_status"]
    assert record["next_step_authorized"] == data["next_step_authorized"]
    assert record["exactly_one_next_step"] is True


def test_33_decision_log_contains_exactly_one_parseable_pr5i_entry() -> None:
    decisions = DECISIONS.read_text(encoding="utf-8")
    assert decisions.count(f"## {ARTIFACT_ID}") == 1
    assert decisions.count("runtime_domain_pr_5i_decision:") == 1
    data = decision_yaml()
    assert data["selected_gate_outcome"] == "AUTHORIZE_PR_5A"
    assert data["implementation_status"] == "review_only"


def test_34_registry_decision_log_and_contract_agree_exactly() -> None:
    record = pr5i_registry_record()
    review = contract()
    decision = decision_yaml()
    assert review["reviewed_artifact"]["artifact_id"] == REVIEWED_ID
    assert record["reviewed_pr_5h_artifact"] == REVIEWED_ID
    assert decision["reviewed_pr_5h_artifact"] == REVIEWED_ID
    assert review["reviewed_artifact"]["file"] == REVIEWED_FILE
    assert record["reviewed_pr_5h_file"] == REVIEWED_FILE
    assert decision["reviewed_pr_5h_file"] == REVIEWED_FILE
    assert record["gate_outcome"] == review["selected_gate_outcome"] == decision["selected_gate_outcome"]
    assert record["next_step_authorized"] == review["next_step_authorized"] == decision["next_step_authorized"]
    assert record["pr_5a_status"] == review["next_step_status"] == decision["pr_5a_status"]


def test_35_forbidden_phrase_absent_from_pr5i_registry_record() -> None:
    record_text = json.dumps(pr5i_registry_record(), sort_keys=True)
    assert "implements runtime" not in record_text.lower()


def test_36_permanent_tests_validate_declared_footprint_not_git_branch_diff() -> None:
    footprint = contract()["pr_5i_footprint_finding"]
    assert footprint["changed_files_exact"] == AUTHORIZED_FILES
    forbidden_git_phrase = "git diff" + " --name-only"
    assert forbidden_git_phrase not in Path(__file__).read_text(encoding="utf-8")
    forbidden_ref_phrase = "origin/main" + "...HEAD"
    assert forbidden_ref_phrase not in Path(__file__).read_text(encoding="utf-8")


def test_37_complete_non_implementation_boundaries_are_present() -> None:
    body = text()
    for phrase in ["The LLM is not the game engine", "References are not calculations", "Results are not state", "Settlement proposals are not transactions", "validation_ready` is not `validation_passed", "Internal serialization is not player-visible projection", "Proposed state-delta references do not apply deltas"]:
        assert phrase in body


def test_38_review_contract_cross_checks_multiple_pr5h_machine_surfaces() -> None:
    data = contract()
    source = pr5h_contract()
    assert data["ten_shape_contract_finding"]["reviewed_shape_order"] == list(data["ten_shape_contract_finding"]["reviewed_field_signatures"].keys())
    assert data["constant_surface_finding"]["constant_surface_names"] == list(source["constants"].keys())
    assert data["blocker_precedence_finding"]["simultaneous_blocker_rows"] == len(source["simultaneous_blocker_table"])
    assert data["parity_finding"]["public_helper_names"] == source["public_helpers"]


def test_39_review_sections_are_present_and_non_boilerplate() -> None:
    body = text()
    section_bodies: list[str] = []
    for number in range(1, 21):
        assert f"## {number}." in body
    for number in range(4, 20):
        match = re.search(rf"## {number}\. .*?\n(.*?)(?=\n## {number + 1}\. )", body, re.DOTALL)
        assert match, f"Missing section {number}"
        section = match.group(1).strip()
        section_bodies.append(section)
        assert re.search(r"Examined PR-5H `[^`]+`", section), section
        focused = re.search(r"Focused tests reviewed: ([^.]+)\.", section)
        assert focused, section
        assert focused.group(1).strip(), section
        assert "Finding:" in section or "Doctrine, machine data, and tests agree" in section
        assert "Gate effect:" in section
        for placeholder in ["Focused tests reviewed: .", "Focused tests reviewed:\n", "TBD", "TODO"]:
            assert placeholder not in section
    assert len(set(section_bodies)) == len(section_bodies)
    assert "## Machine-readable review contract" in body
    assert "## Gate decision" in body


def test_40_review_declares_pr5h_unmodified_without_branch_sensitive_git_check() -> None:
    footprint = contract()["pr_5i_footprint_finding"]
    assert footprint["reviewed_pr_5h_files_modified"] is False
    assert REVIEWED_FILE not in footprint["changed_files_exact"]
    assert "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py" not in footprint["changed_files_exact"]
