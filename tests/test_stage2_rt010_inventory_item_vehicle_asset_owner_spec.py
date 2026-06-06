from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT010_inventory_item_vehicle_asset_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SPEC-001"
PARENT_ID = "REMEDIATION-STAGE2-RT010-RT012-DEFERRED-CONVERGENCE-PLAN-001"
CLOSURE_ID = "REMEDIATION-STAGE2-COMPLETION-REVIEW-CLOSURE-LEDGER-001"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

RT_SPEC_REFS = [
    "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md",
    "docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md",
    "docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md",
    "docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md",
    "docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md",
    "docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md",
    "docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md",
    "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md",
    "docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md",
    "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md",
]

SCAFFOLD_REFS = [
    "docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md",
    "docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md",
]

STATE_TERMS = [
    "inventory_state_required",
    "item_asset_state_required",
    "vehicle_ship_platform_state_required",
    "custody_state_pending",
    "ammo_fuel_charge_dependency",
    "durability_degradation_dependency",
    "hidden_asset_property_visibility_required",
    "random_loot_salvage_dependency",
    "generated_asset_provenance_required",
    "persistent_asset_state_pending",
    "asset_event_commit_pending",
    "asset_resolution_quarantined",
]

FUTURE_ARTIFACTS = [
    "InventoryOwnershipRequirement",
    "ItemAssetStateRequirement",
    "VehiclePlatformStateRequirement",
    "CargoCustodyRequirement",
    "OwnershipTransferRequirement",
    "RepairSalvageRequirement",
    "CraftingRequisitionRequirement",
    "RandomLootSalvageRequirement",
    "GeneratedAssetProvenanceRequirement",
    "PersistentAssetStateRequirement",
    "AssetEventCommitRequirement",
    "InventoryAssetValidationRequirement",
]

GUARDRAIL_PHRASES = [
    "no runtime implementation",
    "no schema implementation",
    "no command IR implementation",
    "no validator implementation",
    "no generator implementation",
    "no inventory system",
    "no item system",
    "no gear system",
    "no relic/implant/installable system",
    "no vehicle/ship/platform system",
    "no companion/summon asset system",
    "no cargo/custody system",
    "no ownership system",
    "no loadout/storage/transfer system",
    "no ammo/fuel/charge system",
    "no durability/degradation system",
    "no repair/salvage system",
    "no crafting/requisition system",
    "no asset economy",
    "no price/value/salvage/requisition tables",
    "no persistent asset state",
    "no persistent ID allocator",
    "no asset event schema",
    "no item schema",
    "no vehicle schema",
    "no cargo schema",
    "no crafting schema",
    "no RNG/dice/table implementation",
    "no event ledger implementation",
    "no database schema",
    "no persistence writer",
    "no retrieval index",
    "no context-packet compiler",
    "no live-play prompt",
    "no training",
    "no donor-content audit",
    "no sourcebook inclusion authorization",
    "no pilot conversion authorization",
    "no canon promotion",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_owner_specification_file_exists_and_has_core_tracking() -> None:
    text = read(SPEC_PATH)
    for expected in [TRACKING_ID, "STAGE2-PR-H1", "STAGE2-PR-H", "RT-010"]:
        assert expected in text


def test_references_required_stage2_and_audit_sources() -> None:
    text = read(SPEC_PATH)
    for expected in [PARENT_ID, CLOSURE_ID, STAGE2_PLAN_ID, REMEDIATION_LEDGER_ID, *AUDIT_IDS]:
        assert expected in text


def test_references_scaffolds_and_owner_specs() -> None:
    text = read(SPEC_PATH)
    for expected in [*SCAFFOLD_REFS, *RT_SPEC_REFS]:
        assert expected in text


def test_defines_required_sections_and_contracts() -> None:
    text = read(SPEC_PATH)
    for heading in [
        "## 2. Scope",
        "## 3. Must-not-own boundaries",
        "## 4. Authority model",
        "## 5. Inventory/item/vehicle/asset state contract",
        "## 6. Asset visibility, custody, and hidden-property contract",
        "## 7. Damage, repair, salvage, crafting, requisition, and value contract",
        "## 8. Asset commitment contract",
        "## 9. Future inventory/item/vehicle/asset artifact inventory",
        "## 10. Validation and readiness requirements",
        "## 11. Downstream handoffs",
        "## 12. LLM non-authority rules",
        "## 13. Non-implementation reaffirmation",
        "## 14. Stage 2 output classification",
    ]:
        assert heading in text


def test_authority_model_and_handoffs_cover_rt001_through_rt012() -> None:
    text = read(SPEC_PATH)
    for rt in ["RT-001", "RT-002", "RT-003", "RT-004", "RT-005", "RT-006", "RT-007", "RT-008", "RT-009", "RT-010", "RT-011", "RT-012"]:
        assert rt in text
    for phrase in [
        "RT-001 owns command/action timing",
        "RT-002 owns costs, value pressure",
        "RT-003 owns item/vehicle/platform damage",
        "RT-004 owns item/relic/implant/vehicle/companion effects",
        "RT-005 owns hidden properties",
        "RT-008 owns generated items",
        "RT-009 owns loot tables",
        "Future backend runtime must own persistent asset state",
        "The LLM may only describe backend-approved visible asset outcomes",
    ]:
        assert phrase in text


def test_state_contract_includes_planning_placeholders_and_disclaimer() -> None:
    text = read(SPEC_PATH)
    for term in STATE_TERMS:
        assert term in text
    for phrase in [
        "planning terms only",
        "not final schemas",
        "not database fields",
        "not inventory rules",
        "not item rules",
        "not vehicle rules",
        "not custody rules",
        "not durability rules",
        "not repair rules",
        "not crafting rules",
        "not economy values",
        "not runtime state",
        "not event records",
        "not validators",
        "not live-play prompts",
    ]:
        assert phrase in text


def test_visibility_damage_and_commitment_contracts_use_guardrail_phrases() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "Visible inventory is not full backend inventory truth",
        "Dialogue or narration cannot transfer ownership or custody",
        "Durability labels are not durability mechanics",
        "Repair labels are not repair formulas",
        "Price/value labels are not economy tables",
        "Asset declaration is not asset state mutation",
        "Inventory listing is not ownership truth unless backend-approved",
        "Narration is not event commitment",
        "Rejected/quarantined asset actions must not mutate state",
    ]:
        assert phrase in text


def test_future_artifact_inventory_is_future_only() -> None:
    text = read(SPEC_PATH)
    for artifact in FUTURE_ARTIFACTS:
        assert artifact in text
    assert text.count("future_required_not_implemented") >= len(FUTURE_ARTIFACTS)
    assert "not implemented schemas, records, validators, services, formulas, generators, or runtime code" in text


def test_validation_readiness_requirements_are_future_only() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "source linkage validation",
        "RT-010 owner-boundary validation",
        "inventory/item/vehicle/asset coverage validation",
        "visible/hidden asset-state routing validation",
        "custody/ownership transfer boundary validation",
        "generated asset provenance validation",
        "random loot/salvage/cargo dependency validation",
        "persistent asset state handoff validation",
        "LLM non-authority validation",
        "non-implementation guardrail validation",
        "coordinate with RT-011 without implementing validators",
    ]:
        assert phrase in text


def test_llm_non_authority_prohibitions_are_representative() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "creating inventory state as backend truth",
        "assigning ownership",
        "assigning custody",
        "transferring ownership",
        "deciding item prices",
        "applying item damage",
        "applying vehicle/platform damage",
        "repairing assets",
        "salvaging assets",
        "crafting assets",
        "revealing hidden item properties",
        "selecting random loot",
        "mutating persistent asset state",
        "committing asset events",
        "inventing schemas, fields, state machines, tables, prices, values, formulas, or event records",
        "authorizing canon/sourcebook/training/live-play use",
    ]:
        assert phrase in text


def test_non_implementation_reaffirmation_and_classification_block() -> None:
    text = read(SPEC_PATH)
    for phrase in GUARDRAIL_PHRASES:
        assert phrase in text
    for phrase in [
        "stage2_output:",
        "stage2_pr_id: STAGE2-PR-H1",
        "parent_stage2_pr_id: STAGE2-PR-H",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "resolves_deferred_owner_spec_gap: true",
        "creates_runtime_implementation: false",
        "authorizes_inventory_system: false",
        "authorizes_persistent_asset_state: false",
        "next_allowed_step: RT-012 owner specification sequencing decision, pending review",
    ]:
        assert phrase in text


def test_registry_and_decision_log_tracking_exists() -> None:
    registry = read(REGISTRY_PATH)
    decision_log = read(DECISION_LOG_PATH)
    for text in [registry, decision_log]:
        assert TRACKING_ID in text
        assert "STAGE2-PR-H1" in text
        assert "resolves RT-010 deferred owner-specification gap" in text
        for phrase in [
            "no runtime implementation",
            "no schema implementation",
            "no validator implementation",
            "no generator implementation",
            "no inventory system",
            "no persistent asset state",
            "no sourcebook inclusion authorization",
            "no pilot conversion authorization",
            "no canon promotion",
        ]:
            assert phrase.lower() in text.lower()


def test_no_file_claims_implementation_authority_for_rt010() -> None:
    combined = "\n".join([read(SPEC_PATH), read(REGISTRY_PATH), read(DECISION_LOG_PATH)])
    forbidden_claims = [
        "creates runtime implementation: true",
        "authorizes_runtime_implementation: true",
        "authorizes_schema_implementation: true",
        "authorizes_validator_implementation: true",
        "authorizes_generator_implementation: true",
        "authorizes_command_ir: true",
        "authorizes_inventory_system: true",
        "authorizes_item_system: true",
        "authorizes_vehicle_system: true",
        "authorizes_asset_system: true",
        "authorizes_persistent_asset_state: true",
        "authorizes_persistent_id_allocator: true",
        "authorizes_sourcebook_inclusion: true",
        "authorizes_canon_promotion: true",
        "authorizes_pilot_conversion: true",
    ]
    lowered = combined.lower()
    for forbidden in forbidden_claims:
        assert forbidden not in lowered
