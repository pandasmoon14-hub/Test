"""Executable validation for PR2-ID-T2C noncurrent identity-surface retention."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
T2B_HEAD = "e00bf6d6a8b7180dff34202a5602d69cab151d7f"
T2C_AUTH = "owner_directive_2026-09-09_pr2_id_t2c_recording_activation"
T2C_EFFECT = "noncurrent_identity_surface_retention_recording_only"

RECORD = ROOT / "docs/doctrine/control/myravant_identity_noncurrent_surface_retention_record.yaml"
LEDGER = ROOT / "docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml"
MANIFEST = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"

FAMILIES = [{'family_id': 'batch_a_draft_doctrine', 'file_count': 7, 'high_recall_occurrence_lines': 7, 'authority_basis': ['registry status=draft', 'registry authority_level=doctrine-draft'], 'paths': ['docs/doctrine/setting/A03_soul_body_mind_spirit_ontology.md', 'docs/doctrine/setting/A04_dao_domain_element_architecture.md', 'docs/doctrine/advancement/A06_cultivation_and_ascension_stage_architecture.md', 'docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md', 'docs/doctrine/world/A12_asset_relic_implant_platform_doctrine.md', 'docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md', 'docs/doctrine/world/A14_travel_exploration_and_scale_transition_doctrine.md']}, {'family_id': 'batch_b_operational_drafts', 'file_count': 5, 'high_recall_occurrence_lines': 7, 'authority_basis': ['file-local status posture=Batch B operational-procedure draft material', 'not current canon, final mechanics, runtime authority, or sourcebook prose'], 'paths': ['docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md', 'docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md', 'docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md', 'docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md', 'docs/doctrine/operations/batch_b/B08_travel_exploration_navigation_and_discovery_procedure.md']}, {'family_id': 'batch_c_schema_drafts', 'file_count': 10, 'high_recall_occurrence_lines': 15, 'authority_basis': ['registry status=draft', 'registry authority_level=schema-draft', 'conversion-stage/canon-review schema material only'], 'paths': ['docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md', 'docs/doctrine/schema/C01_creature_npc_record_schema.md', 'docs/doctrine/schema/C02_item_gear_record_schema.md', 'docs/doctrine/schema/C03_ability_power_technique_record_schema.md', 'docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md', 'docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md', 'docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md', 'docs/doctrine/schema/C09_hazard_environment_record_schema.md', 'docs/doctrine/schema/C10_table_oracle_record_schema.md', 'docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md']}, {'family_id': 'schema_math_mechanics_planning_controls', 'file_count': 6, 'high_recall_occurrence_lines': 8, 'authority_basis': ['planning/readiness/control material only', 'not final mechanics, canon, runtime, sourcebook, or live-play authority'], 'paths': ['docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md', 'docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md', 'docs/doctrine/schema_math_mechanics/SM03_pilot_packet_fixture_and_dry_run_review_plan.md', 'docs/doctrine/schema_math_mechanics/SM04_pilot_benchmark_and_evaluation_rubric_controls.md', 'docs/doctrine/schema_math_mechanics/SM05_actual_pilot_conversion_authorization_and_preflight_gate.md', 'docs/doctrine/schema_math_mechanics/SM06_controlled_pilot_conversion_execution_and_output_capture_plan.md']}, {'family_id': 'noncurrent_control_and_scaffold_artifacts', 'file_count': 5, 'high_recall_occurrence_lines': 7, 'authority_basis': ['draft, owner-specification-only, scaffold-only, planning/tracking-only, or audit-preparation-only', 'superseded/current-state-inaccurate control posture must not be cosmetically refreshed'], 'paths': ['docs/doctrine/control/A00_mechanical_posture_and_ruleset_non_adoption.md', 'docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md', 'docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md', 'docs/doctrine/control/afqr_01_20_consolidation_program_plan.md', 'docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md']}]
UNRESOLVED = ['roadmap_and_registry_currentness_and_identity_roles', 'Astra_Doctrine_Council_governance_role_name', 'r1b_shared_vocabulary_identity_and_exact_parity', 'software_namespace_future_alias_or_deprecation_policy']


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_show(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{T2B_HEAD}:{path}"],
        cwd=ROOT,
        text=True,
    )


def test_t2c_record_is_exact_and_has_no_content_edit_targets():
    data = load(RECORD)
    assert data["artifact_id"] == "PR2-ID-T2C-NONCURRENT-SURFACE-RETENTION-001"
    assert data["artifact_version"] == "0.1.0"
    assert data["status"] == "completed"
    assert data["workstream_id"] == "PR2-ID"
    assert data["tranche_id"] == "PR2-ID-T2C"
    assert data["starting_branch_head"] == T2B_HEAD
    assert data["authorization_reference"] == T2C_AUTH
    assert data["authority_effect"] == T2C_EFFECT
    assert data["audit_basis"]["residual_files"] == 33
    assert data["audit_basis"]["high_recall_identity_occurrence_lines"] == 44
    assert data["audit_basis"]["content_edit_targets"] == 0
    assert data["audit_basis"]["disposition"] == "retain_historical"


def test_t2c_families_are_exact_and_sum_to_33_files_44_lines():
    data = load(RECORD)
    families = data["retention_families"]
    assert families == FAMILIES
    assert sum(row["file_count"] for row in families) == 33
    assert sum(row["high_recall_occurrence_lines"] for row in families) == 44

    paths = [path for row in families for path in row["paths"]]
    assert len(paths) == 33
    assert len(paths) == len(set(paths))
    assert data["protected_paths"] == paths


def test_all_33_retained_source_files_are_byte_exact_to_published_t2b_head():
    data = load(RECORD)
    for path in data["protected_paths"]:
        assert (ROOT / path).read_text(encoding="utf-8") == git_show(path), path


def test_high_recall_metric_and_raw_astra_counts_are_distinct_and_exact():
    data = load(RECORD)

    # The 44-line figure is the selector-derived T2C residual inventory metric.
    # It is deliberately not recomputed as a plain substring search.
    assert data["audit_basis"]["high_recall_identity_occurrence_lines"] == 44
    assert (
        sum(
            row["high_recall_occurrence_lines"]
            for row in data["retention_families"]
        )
        == 44
    )

    raw_by_family = {}
    for family in data["retention_families"]:
        count = 0
        for path in family["paths"]:
            text = (ROOT / path).read_text(encoding="utf-8")
            count += sum("Astra" in line for line in text.splitlines())
        raw_by_family[family["family_id"]] = count

    assert data["audit_basis"]["raw_astra_line_counts_by_family"] == raw_by_family
    assert data["audit_basis"]["raw_astra_line_count"] == sum(raw_by_family.values())

    semantics = data["audit_basis"]["measurement_semantics"]
    assert "Selector-derived" in semantics["high_recall_identity_occurrence_lines"]
    assert "not a raw substring count" in semantics[
        "high_recall_identity_occurrence_lines"
    ]
    assert "Diagnostic count" in semantics["raw_astra_line_count"]


def test_only_four_separately_bounded_identity_classes_remain():
    record = load(RECORD)
    ledger = load(LEDGER)
    classes = [row["class_id"] for row in record["unresolved_identity_classes"]]
    assert classes == UNRESOLVED
    assert ledger["t2c_recording_tranche"]["status"] == "completed"


def test_manifest_records_t2c_without_downstream_authority():
    manifest = load(MANIFEST)
    pr2id = next(
        row for row in manifest["workstreams"] if row["workstream_id"] == "PR2-ID"
    )
    version = tuple(int(part) for part in manifest["artifact_version"].split("."))
    assert version >= (0, 4, 7)
    assert pr2id["status"] == "active"
    assert pr2id["next_tranche_authorized"] is False

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["execution_authorized"] is False

    by_id = {row["workstream_id"]: row for row in manifest["workstreams"]}
    for wid in ["PR2-SRC", "PR2-ORG", "PR2-IR", "PR2-SCALE"]:
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None


def test_t2c_record_explicitly_preserves_software_and_governance_boundaries():
    data = load(RECORD)
    by_id = {row["class_id"]: row for row in data["unresolved_identity_classes"]}

    assert by_id["Astra_Doctrine_Council_governance_role_name"]["disposition"] == "escalate"
    assert by_id["r1b_shared_vocabulary_identity_and_exact_parity"]["disposition"] == "escalate"
    assert (
        by_id["software_namespace_future_alias_or_deprecation_policy"]["disposition"]
        == "retain_compatibility"
    )
    assert by_id["software_namespace_future_alias_or_deprecation_policy"]["literals_or_paths"] == [
        "astra-runtime",
        "astra_runtime",
        "src/astra_runtime/",
    ]
