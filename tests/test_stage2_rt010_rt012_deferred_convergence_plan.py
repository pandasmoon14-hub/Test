from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = REPO_ROOT / "docs" / "doctrine" / "reviews" / "runtime_boundary_generator_ownership_stage2_rt010_rt012_deferred_convergence_plan.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT010-RT012-DEFERRED-CONVERGENCE-PLAN-001"
STAGE2_PR_ID = "STAGE2-PR-H"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

RT010_SCAFFOLD_FILE = "docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md"
RT012_SCAFFOLD_FILE = "docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md"
OWNER_SPEC_FILES = [
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

RT010_FUTURE_ARTIFACTS = [
    "InventoryOwnershipRequirement",
    "ItemAssetStateRequirement",
    "VehiclePlatformStateRequirement",
    "RelicImplantInstallableRequirement",
    "CargoCustodyRequirement",
    "ChargeFuelAmmoRequirement",
    "DurabilityDegradationRequirement",
    "RepairSalvageRequirement",
    "CraftingRequisitionRequirement",
    "AssetVisibilityRequirement",
    "AssetEffectCapabilityRequirement",
    "AssetRewardLossRequirement",
    "RandomLootSalvageRequirement",
    "GeneratedAssetProvenanceRequirement",
    "AssetPersistenceHandoffRequirement",
    "InventoryAssetValidationRequirement",
]

RT012_FUTURE_ARTIFACTS = [
    "DSeriesPromotionBoundaryRequirement",
    "NativeDesignPressureRequirement",
    "SourcePackNonAuthorityRequirement",
    "CanonCandidateBoundaryRequirement",
    "SourcebookCandidateBoundaryRequirement",
    "RuntimeOwnerHandoffRequirement",
    "PromotionReviewRequirement",
    "UnpromotedContentQuarantineRequirement",
    "DoctrineConflictRoutingRequirement",
    "TrainingLivePlayExclusionRequirement",
    "DSeriesBoundaryValidationRequirement",
]

LLM_PROHIBITIONS = [
    "creating inventory state",
    "creating item/vehicle/asset state",
    "assigning ownership, custody, cargo, ammo, charges, fuel, durability, or repair state",
    "deciding item prices, salvage values, requisition values, crafting results, or reward values",
    "applying item or vehicle damage",
    "granting relics, implants, vehicles, companions, or assets as backend truth",
    "revealing hidden item properties or hidden cargo",
    "creating generated assets as durable truth",
    "promoting D-series/native-design content to runtime authority",
    "promoting D-series/native-design content to canon",
    "promoting D-series/native-design content to sourcebook inclusion",
    "treating source packs as authority",
    "treating examples as authority",
    "treating generated content as authority",
    "treating live-play narration as promotion",
    "treating summaries as persistent memory or promotion evidence",
    "bypassing reviewer/backend validation",
    "authorizing training, live play, sourcebook inclusion, pilot conversion, donor audit, or canon promotion",
]

NO_IMPLEMENTATION_GUARDRAILS = [
    "no runtime code",
    "no schema implementation",
    "no command IR implementation",
    "no validator implementation",
    "no generator implementation",
    "no inventory system",
    "no item system",
    "no vehicle system",
    "no asset system",
    "no durability system",
    "no repair system",
    "no salvage system",
    "no crafting system",
    "no requisition system",
    "no cargo/custody system",
    "no ownership system",
    "no persistent asset state",
    "no persistent ID allocator",
    "no D-series promotion system",
    "no native-design promotion system",
    "no canon promotion procedure",
    "no sourcebook inclusion procedure",
    "no training policy",
    "no RNG/dice/table implementation",
    "no event ledger implementation",
    "no database schema",
    "no persistence writer",
    "no retrieval index",
    "no context-packet compiler",
    "no live-play prompt",
    "no training data",
    "no donor-content audit",
    "no sourcebook inclusion authorization",
    "no pilot conversion authorization",
    "no canon promotion",
]

FORBIDDEN_TRUE_CLAIMS = [
    "creates_rt010_owner_specification: true",
    "creates_rt012_owner_specification: true",
    "authorizes_runtime_implementation: true",
    "authorizes_schema_implementation: true",
    "authorizes_validator_implementation: true",
    "authorizes_generator_implementation: true",
    "authorizes_inventory_system: true",
    "authorizes_item_system: true",
    "authorizes_vehicle_system: true",
    "authorizes_asset_system: true",
    "authorizes_persistent_asset_state: true",
    "authorizes_d_series_promotion_system: true",
    "authorizes_native_design_promotion_system: true",
    "authorizes_sourcebook_inclusion: true",
    "authorizes_canon_promotion: true",
    "authorizes_live_play: true",
    "authorizes_training: true",
    "authorizes_pilot_conversion: true",
    "implementation_status: executable",
    "implementation_status: implemented",
    "authority_level: runtime",
    "authority_level: canon",
    "authority_level: live_play",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_convergence_plan_file_exists_and_has_core_tracking() -> None:
    text = read(PLAN_PATH)
    for expected in [TRACKING_ID, STAGE2_PR_ID, "RT-010", "RT-012"]:
        assert expected in text


def test_plan_references_required_audit_remediation_and_owner_sources() -> None:
    text = read(PLAN_PATH)
    for expected in [
        STAGE2_PLAN_ID,
        REMEDIATION_LEDGER_ID,
        RT010_SCAFFOLD_FILE,
        RT012_SCAFFOLD_FILE,
        *OWNER_SPEC_FILES,
        *AUDIT_IDS,
    ]:
        assert expected in text


def test_plan_states_non_owner_spec_and_non_authorization_status() -> None:
    text = read(PLAN_PATH)
    for phrase in [
        "non-executable planning artifact only",
        "not a full RT-010 owner specification",
        "not a full RT-012 owner specification",
        "does not authorize implementation",
        "does not authorize runtime, schemas, validators, generators, persistence, live play, training, sourcebook inclusion, pilot conversion, donor-content audit, or canon promotion",
    ]:
        assert phrase in text


def test_rt010_and_rt012_deferral_rationales_are_explained() -> None:
    text = read(PLAN_PATH)
    assert "## 3. Why RT-010 was deferred" in text
    assert "## 5. Why RT-012 was deferred" in text
    for phrase in [
        "command/event lifecycle and asset-affecting action timing",
        "costs, value pressure, repair cost, loss, degradation, salvage value, upkeep, and economy pressure",
        "item/vehicle/platform damage, repair, exposure, hazards, combat fallout, and recovery implications",
        "D-series/native-design material may pressure future runtime, canon, or sourcebook work",
        "must not become runtime, sourcebook, canon, training, pilot-conversion, or live-play authority by default",
    ]:
        assert phrase in text


def test_future_rt010_and_rt012_requirements_are_defined_without_implementation() -> None:
    text = read(PLAN_PATH)
    assert "## 4. What future RT-010 owner specification should own" in text
    assert "## 6. What future RT-012 owner specification should own" in text
    for phrase in [
        "defines future RT-010 owner-specification requirements without implementing them",
        "does not define final fields, schemas, runtime state, storage model, item economy, durability rules, vehicle rules, repair rules, crafting rules, or event schemas",
        "defines future RT-012 owner-specification requirements without implementing them",
        "does not define final canon-promotion procedure, sourcebook inclusion procedure, training policy, native-design promotion system, canon records, sourcebook records, or runtime promotion implementation",
    ]:
        assert phrase in text


def test_split_recommendation_and_deferred_convergence_matrix_are_present() -> None:
    text = read(PLAN_PATH)
    assert "## 7. Convergence recommendation" in text
    assert "RT-010 and RT-012 should not be combined into one future owner specification" in text
    assert "future STAGE2-PR-H1" in text
    assert "future STAGE2-PR-H2" in text
    assert "## 8. Deferred convergence matrix" in text
    for status in [
        "deferred_pending_convergence_plan",
        "owner_spec_required_later",
        "implementation_blocked",
        "runtime_blocked",
        "schema_blocked",
        "canon_promotion_blocked",
        "sourcebook_inclusion_blocked",
        "live_play_blocked",
        "training_blocked",
    ]:
        assert status in text


def test_future_artifact_inventory_is_future_required_not_implemented() -> None:
    text = read(PLAN_PATH)
    assert "## 9. Future artifact inventory" in text
    for artifact in [*RT010_FUTURE_ARTIFACTS, *RT012_FUTURE_ARTIFACTS]:
        assert artifact in text
    assert text.count("future_required_not_implemented") >= len(RT010_FUTURE_ARTIFACTS) + len(RT012_FUTURE_ARTIFACTS)


def test_llm_non_authority_prohibitions_are_explicit() -> None:
    text = read(PLAN_PATH)
    assert "## 10. LLM non-authority rules" in text
    for phrase in LLM_PROHIBITIONS:
        assert phrase in text


def test_non_implementation_reaffirmation_and_stage2_classification_are_present() -> None:
    text = read(PLAN_PATH)
    assert "## 11. Non-implementation reaffirmation" in text
    for phrase in NO_IMPLEMENTATION_GUARDRAILS:
        assert phrase in text
    assert "## 13. Stage 2 output classification" in text
    for phrase in [
        "stage2_pr_id: STAGE2-PR-H",
        "artifact_type: deferred_convergence_plan",
        "implementation_status: non_executable_planning",
        "creates_rt010_owner_specification: false",
        "creates_rt012_owner_specification: false",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_generator_implementation: false",
        "authorizes_inventory_system: false",
        "authorizes_item_system: false",
        "authorizes_vehicle_system: false",
        "authorizes_asset_system: false",
        "authorizes_persistent_asset_state: false",
        "authorizes_d_series_promotion_system: false",
        "authorizes_native_design_promotion_system: false",
        "authorizes_sourcebook_inclusion: false",
        "authorizes_canon_promotion: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_pilot_conversion: false",
    ]:
        assert phrase in text


def test_registry_and_decision_log_tracking_exists() -> None:
    registry_text = read(REGISTRY_PATH)
    decision_text = read(DECISION_LOG_PATH)
    for text in [registry_text, decision_text]:
        assert TRACKING_ID in text
        assert STAGE2_PR_ID in text
        assert "Stage 2 deferred convergence plan only" in text
        assert "does not create RT-010 owner specification" in text
        assert "does not create RT-012 owner specification" in text
        assert "no runtime implementation" in text
        assert "no schema implementation" in text
        assert "no canon promotion" in text


def test_plan_does_not_claim_forbidden_implementation_authority() -> None:
    text = read(PLAN_PATH)
    lowered = text.lower()
    for forbidden in FORBIDDEN_TRUE_CLAIMS:
        assert forbidden.lower() not in lowered
