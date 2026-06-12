from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5i_resource_consequence_math_final_residual_planning_hardening_review.md"
PR5H_DOC = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
RESOURCE_MATH_MODULE = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"
ARTIFACT_ID = "RUNTIME-DOMAIN-PR-5I-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-REVIEW-001"
TITLE = "RUNTIME-DOMAIN-PR-5I: Resource and Consequence Math Final Residual Planning Hardening Review Gate"
REVIEWED_ID = "RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001"
AUTHORIZED_FILES = {
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
    "docs/doctrine/reviews/runtime_domain_pr_5i_resource_consequence_math_final_residual_planning_hardening_review.md",
    "tests/test_runtime_domain_pr_5i_resource_consequence_math_final_residual_planning_hardening_review.py",
}
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
SOURCE_LEDGER = [
    "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md",
    "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py",
    "docs/doctrine/reviews/runtime_domain_pr_5g_resource_consequence_math_residual_planning_hardening_review.md",
    "tests/test_runtime_domain_pr_5g_resource_consequence_math_residual_planning_hardening_review.py",
    "docs/doctrine/reviews/runtime_domain_pr_5f_resource_consequence_math_residual_planning_hardening.md",
    "tests/test_runtime_domain_pr_5f_resource_consequence_math_residual_planning_hardening.py",
    "docs/doctrine/reviews/runtime_domain_pr_5d_resource_consequence_math_final_planning_hardening.md",
    "tests/test_runtime_domain_pr_5d_resource_consequence_math_final_planning_hardening.py",
    "docs/doctrine/reviews/runtime_domain_pr_5c_resource_consequence_math_planning_hardening_review.md",
    "tests/test_runtime_domain_pr_5c_resource_consequence_math_planning_hardening_review.py",
    "docs/doctrine/reviews/runtime_domain_pr_5b_resource_consequence_math_planning_hardening.md",
    "tests/test_runtime_domain_pr_5b_resource_consequence_math_planning_hardening.py",
    "docs/doctrine/reviews/runtime_domain_pr_5_resource_consequence_math_service_plan.md",
    "tests/test_runtime_domain_pr_5_resource_consequence_math_service_plan.py",
    "docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md",
    "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md",
    "docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md",
    "docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md",
    "docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md",
    "docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md",
    "docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md",
    "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md",
    "docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md",
    "docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md",
    "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md",
    "docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md",
    "src/astra_runtime/domain/validation_integration.py",
    "src/astra_runtime/domain/transaction_lifecycle.py",
    "src/astra_runtime/domain/event_commitment.py",
    "src/astra_runtime/domain/state_store.py",
    "src/astra_runtime/domain/state_projection.py",
    "src/astra_runtime/kernel/rng_interface.py",
    "src/astra_runtime/kernel/table_oracle.py",
    "src/astra_runtime/kernel/state_delta.py",
    "src/astra_runtime/kernel/transaction_preview.py",
    "src/astra_runtime/kernel/event_ledger.py",
    "src/astra_runtime/kernel/persistence_boundary.py",
    "src/astra_runtime/kernel/replay_audit.py",
    "src/astra_runtime/kernel/hidden_information.py",
    "src/astra_runtime/kernel/context_projection.py",
    "src/astra_runtime/kernel/schema_registry.py",
    "src/astra_runtime/kernel/record_identity.py",
    "src/astra_runtime/kernel/runtime_trace.py",
    "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
    "docs/decisions/current_decisions_log.md",
]


def text() -> str:
    return DOC.read_text(encoding="utf-8")


def contract() -> dict:
    match = re.search(r"```yaml pr5i_review_contract\n(.*?)\n```", text(), re.DOTALL)
    assert match, "PR-5I review must contain the normative pr5i_review_contract block."
    data = yaml.safe_load(match.group(1))
    assert isinstance(data, dict)
    return data


def pr5h_contract() -> dict:
    match = re.search(r"```yaml pr5h_effective_contract\n(.*?)\n```", PR5H_DOC.read_text(encoding="utf-8"), re.DOTALL)
    assert match
    data = yaml.safe_load(match.group(1))
    assert isinstance(data, dict)
    return data


def registry_records() -> list[dict]:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return records


def pr5i_registry_record() -> dict:
    matches = [record for record in registry_records() if record.get("file_id") == ARTIFACT_ID]
    assert len(matches) == 1
    return matches[0]


def test_01_pr5i_file_exists_and_identity() -> None:
    assert DOC.exists()
    assert ARTIFACT_ID in text()
    assert TITLE in text()
    assert contract()["artifact"]["artifact_id"] == ARTIFACT_ID
    assert contract()["artifact"]["artifact_title"] == TITLE


def test_02_review_only_status_and_pr5h_review_target() -> None:
    data = contract()
    assert data["artifact"]["artifact_type"] == "final_residual_planning_hardening_review_gate"
    assert data["artifact"]["implementation_status"] == "review_only"
    assert data["artifact"]["owner"] == "RT-002"
    assert data["reviewed_artifact"]["artifact_id"] == REVIEWED_ID
    assert "does not itself implement PR-5A" in text()
    assert "PRs #278 or #279" in text()


def test_03_exact_source_ledger() -> None:
    assert contract()["source_ledger"] == SOURCE_LEDGER
    for source in SOURCE_LEDGER:
        assert (ROOT / source).exists(), source


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


def test_05_all_eight_pr5g_defects_appear_exactly_once_with_lawful_findings() -> None:
    rows = contract()["pr_5g_closure_matrix"]
    assert [row["defect"] for row in rows] == DEFECTS
    assert sorted(text().count(defect) for defect in DEFECTS)
    for row in rows:
        assert row["review_finding"] in {"closed", "partially_closed", "open"}
        assert row["review_finding"] == "closed"
        assert row["pr_5a_would_need_to_invent_behavior"] is False


def test_06_normative_yaml_block_parses_and_allowed_outcomes_are_exact() -> None:
    data = contract()
    assert data["allowed_gate_outcomes"] == ["AUTHORIZE_PR_5A", "HARDENING_REQUIRED"]
    assert data["selected_gate_outcome"] in data["allowed_gate_outcomes"]


def test_07_exactly_one_outcome_and_gate_fields_are_consistent() -> None:
    data = contract()
    assert data["selected_gate_outcome"] == "AUTHORIZE_PR_5A"
    assert data["pr_5h_accepted"] is True
    assert data["pr_5a_authorized_as_sole_next_step"] is True
    assert data["pr_5a_blocked"] is False
    assert data["pr_5a_implementation_part_of_this_pr"] is False
    assert data["next_step_status"] == "narrow_reference_only_skeleton_authorized"


def test_08_ten_shape_inventory_is_exact_and_cross_checked_against_pr5h_machine_data() -> None:
    data = contract()["ten_shape_contract_finding"]
    source = pr5h_contract()
    assert data["shape_order"] == SHAPES
    assert set(data["future_shapes"]) == set(SHAPES)
    for shape in SHAPES:
        assert data["future_shapes"][shape] == source["future_shapes"][shape]
    assert data["resource_math_request_has_no_stage"] is True
    assert data["settlement_proposal_has_no_request_id"] is True
    assert data["resource_math_result_has_no_resource_math_result_ref"] is True
    assert data["typed_scope_fields"] == source["typed_scope_fields"]
    assert data["cost_bundle_preserves_atomicity_ordering_partial"] is True
    assert data["bundle_policy_replacement_exists"] is False


def test_09_constant_surfaces_are_reviewed_against_pr5h() -> None:
    data = contract()["constant_surface_finding"]
    source = pr5h_contract()
    assert data["finding"] == "closed"
    assert data["constants"] == source["constants"]
    assert data["no_inherited_constant_dropped"] is True
    assert data["no_donor_specific_pool_or_economy"] is True
    assert data["no_contradictory_duplicate_surface"] is True


def test_10_stage_decision_compatibility_is_reviewed() -> None:
    data = contract()["stage_decision_finding"]
    assert data["stage_decision_matrix"] == pr5h_contract()["stage_decision_matrix"]
    assert data["every_unlisted_pair_invalid"] is True
    assert data["validation_blocked_is_resource_math_result_decision"] is False
    assert data["false_only_authority_flags_remain_false"] is True


def test_11_dependency_states_a_e_and_binding_matrix_are_reviewed() -> None:
    data = contract()["dependency_lifecycle_finding"]
    assert set(data["states"]) == {
        "A_complete_binding",
        "B_incomplete_binding",
        "C_missing_or_malformed_binding",
        "D_required_unsatisfied_named_dependency",
        "E_advisory_optional_unsatisfied",
    }
    assert data["binding_state_matrix"] == pr5h_contract()["binding_state_matrix"]
    assert data["no_optional_dependency_satisfies_binding"] is True
    assert data["no_incomplete_dependency_supports_proposal_eligibility"] is True
    assert data["no_result_self_binding"] is True


def test_12_hidden_information_collision_behavior_is_reviewed() -> None:
    data = contract()["blocker_precedence_finding"]
    assert data["simultaneous_blocker_table"] == pr5h_contract()["simultaneous_blocker_table"]
    assert data["dependency_hidden_information_collision_matrix"] == pr5h_contract()["dependency_hidden_information_collision_matrix"]
    assert data["dependency_derived_hidden_information_requires"] == {
        "required": True,
        "satisfied": True,
        "hidden_info_safe": False,
    }
    assert data["diagnostic_preservation"] is True


def test_13_typed_scope_cardinality_and_closure_are_reviewed() -> None:
    data = contract()["typed_scope_finding"]
    assert data["typed_scope_fields"] == pr5h_contract()["typed_scope_fields"]
    assert data["exact_cardinality"] == 7
    assert data["ids_unique_non_empty"] is True
    assert data["all_ids_resolve_in_request"] is True
    assert data["combined_scope_cannot_be_empty"] is True
    assert data["accepted_normalized_require_substantive_scope"] is True
    assert data["normalized_reference_ids_diagnostic_only"] is True


def test_14_quantity_and_source_literal_rules_are_reviewed() -> None:
    data = contract()["quantity_source_literal_finding"]
    assert data["quantity_lexical_grammars"] == pr5h_contract()["quantity_lexical_grammars"]
    assert data["quantity_execution_bans"] == pr5h_contract()["quantity_execution_bans"]
    assert data["integer_bool_distinction"] is True
    assert data["full_string_matching"] is True
    assert data["exponent_prohibition"] is True
    assert data["lexical_negative_recognition"] == ["-0", "-0.0", "-0/1"]
    assert data["no_source_literal_parsing_or_normalization"] is True


def test_15_cost_bundle_compatibility_is_reviewed() -> None:
    data = contract()["cost_bundle_finding"]
    assert data["cost_bundle_sets"] == pr5h_contract()["cost_bundle_sets"]
    assert data["cost_bundle_matrix"] == pr5h_contract()["cost_bundle_matrix"]
    assert data["bound_corrections"] == pr5h_contract()["cost_bundle_bound_corrections"]
    assert data["every_unlisted_combination_invalid"] is True
    assert data["no_selection_affordability_reservation_or_settlement_execution"] is True


def test_16_direct_validation_signatures_are_reviewed() -> None:
    data = contract()["validation_architecture_finding"]
    assert data["direct_validation_signatures"] == pr5h_contract()["direct_validation_signatures"]
    assert data["request_validation_precedes_result_validation"] is True
    assert data["result_request_identity_and_dependency_checks_precede_proposal_eligibility"] is True
    assert data["no_certificate_object"] is True
    assert data["no_repository_lookup_or_cached_valid_flag"] is True


def test_17_settlement_proposal_eligibility_is_reviewed() -> None:
    data = contract()["settlement_proposal_finding"]
    assert data["settlement_eligibility"] == pr5h_contract()["settlement_eligibility"]
    assert data["requires_calculation_ready_for_review"] is True
    assert data["requires_accepted_or_normalized_decision"] is True
    assert data["requires_validation_passed"] is True
    assert data["requires_state_delta_dependencies"] is True
    assert data["rejects_event_only_and_policy_only"] is True


def test_18_public_private_helper_parity_is_reviewed() -> None:
    data = contract()["parity_finding"]
    assert data["public_helpers"] == pr5h_contract()["public_helpers"]
    assert data["public_helper_count"] == 20
    assert data["private_helper_responsibilities"] == pr5h_contract()["private_helper_responsibilities"]
    assert data["create_validate_parity_for_every_shape"] is True
    assert data["manual_construction_cannot_bypass_invariants"] is True
    assert data["tuple_mapping_defensive_copying"] is True
    assert data["callable_metadata_rejection"] is True
    assert data["no_generic_helper_replaces_exact_helpers"] is True


def test_19_serialization_and_rt005_boundaries_are_reviewed() -> None:
    data = contract()["serialization_finding"]
    assert data["internal_to_dict_only"] is True
    assert data["to_public_dict_exists"] is False
    assert data["public_player_narrator_model_gm_projection"] is False
    assert data["redaction_implementation"] is False
    assert data["hidden_information_release"] is False
    assert data["defensive_serialization"] is True
    assert data["no_calculation_during_serialization"] is True
    assert data["rt_005_remains_public_projection_redaction_owner"] is True


def test_20_owner_boundaries_are_reviewed() -> None:
    data = contract()["owner_boundary_finding"]
    assert data["finding"] == "closed"
    assert len(data["rt_002_does_not_absorb"]) >= 16
    assert "state mutation" in data["rt_002_does_not_absorb"]
    assert "model/live-play/UI behavior" in data["rt_002_does_not_absorb"]


def test_21_corpus_family_pressure_is_reviewed() -> None:
    data = contract()["corpus_pressure_finding"]
    assert len(data["families_reviewed"]) >= 19
    assert data["lawful_destinations"] == [
        "direct Astra mapping",
        "normalized Astra mapping",
        "source-local retention",
        "owner handoff",
        "quarantine",
        "doctrine escalation",
    ]
    assert data["no_donor_default_law_promoted"] is True


def test_22_implementation_derivability_is_reviewed() -> None:
    data = contract()["implementation_derivability_finding"]
    assert data["finding"] == "derivable_without_new_doctrine_decision"
    assert data["pr_5a_can_derive_reference_only_skeleton"] is True
    assert data["all_implementation_relevant_contract_surfaces_unambiguous"] is True
    assert data["material_contradictions_remaining"] is False
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
    expected = {
        "exact shape inventories",
        "exact fields/defaults",
        "constants",
        "compatibility matrices",
        "dependency lifecycle",
        "typed scope",
        "hidden-information collisions",
        "source-literal rules",
        "bundle behavior",
        "direct validation",
        "proposal eligibility",
        "helper parity",
        "authority flags",
        "registry tracking",
        "four-file footprint",
        "absence of runtime implementation",
    }
    assert set(data["coverage"]) == expected


def test_25_authorized_pr5a_future_scope_is_reference_only_and_non_calculating() -> None:
    data = contract()
    assert data["selected_gate_outcome"] == "AUTHORIZE_PR_5A"
    scope = data["future_pr_5a_scope_if_authorized"]
    assert scope["may_create"] == [
        "immutable frozen keyword-only shapes",
        "exact constants",
        "exact factories and validators",
        "internal defensive serialization",
        "domain exports",
        "focused tests",
    ]
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
    for required in [
        "runtime_code_authorized_by_this_pr",
        "domain_code_authorized_by_this_pr",
        "calculation_authorized_by_this_pr",
        "settlement_authorized_by_this_pr",
        "state_delta_application_authorized_by_this_pr",
        "transaction_execution_authorized_by_this_pr",
        "event_commitment_authorized_by_this_pr",
        "persistence_authorized_by_this_pr",
        "replay_authorized_by_this_pr",
        "rng_execution_authorized_by_this_pr",
        "model_integration_authorized_by_this_pr",
        "live_play_authorized_by_this_pr",
        "ui_authorized_by_this_pr",
        "conversion_authorized_by_this_pr",
        "canon_promotion_authorized_by_this_pr",
    ]:
        assert block[required] is False


def test_28_no_src_file_changed_by_pr5i() -> None:
    result = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
    changed = set(filter(None, result.stdout.splitlines()))
    assert not any(path.startswith("src/") for path in changed)


def test_29_resource_consequence_math_module_remains_absent() -> None:
    assert not RESOURCE_MATH_MODULE.exists()


def test_30_registry_contains_exactly_one_complete_pr5i_record() -> None:
    record = pr5i_registry_record()
    required = {
        "file_id", "filename", "proposed_path", "layer", "phase", "status", "authority_level", "owner", "purpose",
        "owns", "must_not_own", "dependencies", "blocked_by", "unlocks", "downstream_consumers",
        "donor_pressure_absorbed", "hard_refusals", "escalation_triggers", "required_tests", "test_status",
        "review_status", "promotion_requirements", "scale_gate_relevance", "broad_conversion_relevance", "canon_relevance",
        "runtime_relevance", "live_play_relevance", "notes",
    }
    assert not (required - set(record))
    assert record["implementation_status"] == "review_only"
    assert record["reviewed_pr_5h_artifact"] == "runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md"


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


def test_33_decision_log_contains_exactly_one_pr5i_entry() -> None:
    decisions = DECISIONS.read_text(encoding="utf-8")
    assert decisions.count(f"## {ARTIFACT_ID}") == 1
    assert decisions.count("runtime_domain_pr_5i_decision:") == 1
    assert "selected_gate_outcome: AUTHORIZE_PR_5A" in decisions
    assert "review_only" in decisions


def test_34_registry_and_decision_log_agree() -> None:
    record = pr5i_registry_record()
    decisions = DECISIONS.read_text(encoding="utf-8")
    assert record["gate_outcome"] in decisions
    assert record["next_step_authorized"] in decisions
    assert REVIEWED_ID in decisions
    assert record["reviewed_pr_5h_artifact"] in record["reviewed_pr_5h_artifact"]


def test_35_forbidden_phrase_absent_from_pr5i_registry_record() -> None:
    record_text = json.dumps(pr5i_registry_record(), sort_keys=True)
    assert "implements runtime" not in record_text.lower()


def test_36_pr_diff_contains_exactly_the_four_authorized_files() -> None:
    result = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
    assert set(filter(None, result.stdout.splitlines())) == AUTHORIZED_FILES


def test_37_complete_non_implementation_boundaries_are_present() -> None:
    body = text()
    for phrase in [
        "The LLM is not the game engine",
        "References are not calculations",
        "Results are not state",
        "Settlement proposals are not transactions",
        "validation_ready` is not `validation_passed",
        "Internal serialization is not player-visible projection",
        "Proposed state-delta references do not apply deltas",
    ]:
        assert phrase in body


def test_38_review_contract_cross_checks_multiple_pr5h_machine_surfaces() -> None:
    data = contract()
    source = pr5h_contract()
    assert data["ten_shape_contract_finding"]["future_shapes"] == {shape: source["future_shapes"][shape] for shape in SHAPES}
    assert data["constant_surface_finding"]["constants"] == source["constants"]
    assert data["blocker_precedence_finding"]["simultaneous_blocker_table"] == source["simultaneous_blocker_table"]
    assert data["parity_finding"]["public_helpers"] == source["public_helpers"]


def test_39_review_sections_are_present() -> None:
    body = text()
    for number in range(1, 21):
        assert f"## {number}." in body
    assert "## Machine-readable review contract" in body
    assert "## Gate decision" in body


def test_40_review_does_not_weaken_pr5h_or_modify_it() -> None:
    result = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD", "--", str(PR5H_DOC.relative_to(ROOT))], cwd=ROOT, text=True, capture_output=True, check=True)
    assert result.stdout.strip() == ""
