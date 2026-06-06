from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT012_d_series_promotion_boundary_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT012-D-SERIES-PROMOTION-BOUNDARY-OWNER-SPEC-001"
PARENT_ID = "REMEDIATION-STAGE2-RT010-RT012-DEFERRED-CONVERGENCE-PLAN-001"
CLOSURE_ID = "REMEDIATION-STAGE2-COMPLETION-REVIEW-CLOSURE-LEDGER-001"
RT010_SPEC_ID = "REMEDIATION-STAGE2-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SPEC-001"
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
    "docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md",
    "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md",
]

SCAFFOLD_REF = "docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md"

PRESSURE_TERMS = [
    "d_series_pressure_detected",
    "native_design_claim_pending",
    "source_pack_non_authority_required",
    "source_pack_pressure_record_required",
    "doctrine_conflict_route_required",
    "rt_owner_handoff_required",
    "runtime_owner_handoff_pending",
    "schema_owner_handoff_pending",
    "sourcebook_candidate_pending_review",
    "canon_candidate_pending_review",
    "promotion_review_required",
    "reviewer_decision_pending",
    "unpromoted_content_quarantined",
    "rejected_design_pressure_recorded",
    "source_local_pressure_only",
    "example_pack_non_authority_required",
    "converted_content_non_authority_required",
    "generated_content_non_authority_required",
    "live_play_narration_non_authority_required",
    "training_exclusion_required",
    "sourcebook_inclusion_blocked",
    "canon_promotion_blocked",
]

FUTURE_ARTIFACTS = [
    "DSeriesPromotionBoundaryRequirement",
    "NativeDesignPressureRequirement",
    "SourcePackNonAuthorityRequirement",
    "SourcePackPressureRecordRequirement",
    "NativeDesignClaimRoutingRequirement",
    "DoctrineConflictRoutingRequirement",
    "RTOwnerHandoffRequirement",
    "RuntimeOwnerHandoffRequirement",
    "SourcebookCandidateBoundaryRequirement",
    "CanonCandidateBoundaryRequirement",
    "PromotionReviewRequirement",
    "ReviewerDecisionRequirement",
    "UnpromotedContentQuarantineRequirement",
    "RejectedDesignPressureRequirement",
    "SourceLocalPressureRequirement",
    "ExamplePackNonAuthorityRequirement",
    "ConvertedContentNonAuthorityRequirement",
    "GeneratedContentNonAuthorityRequirement",
    "LivePlayNarrationNonAuthorityRequirement",
    "TrainingExclusionRequirement",
    "SourcebookInclusionBlockedRequirement",
    "CanonPromotionBlockedRequirement",
    "DSeriesBoundaryValidationRequirement",
]

GUARDRAIL_PHRASES = [
    "no runtime implementation",
    "no schema implementation",
    "no command IR implementation",
    "no validator implementation",
    "no generator implementation",
    "no D-series promotion system",
    "no native-design promotion system",
    "no canon promotion procedure",
    "no sourcebook inclusion procedure",
    "no training policy",
    "no live-play policy",
    "no doctrine rewrite procedure",
    "no source-pack ingestion procedure",
    "no example-pack promotion procedure",
    "no converted-content promotion procedure",
    "no generated-content promotion procedure",
    "no promotion records",
    "no canon records",
    "no sourcebook records",
    "no reviewer workflow implementation",
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
    for expected in [TRACKING_ID, "STAGE2-PR-H2", "STAGE2-PR-H", "RT-012"]:
        assert expected in text


def test_references_required_stage2_and_audit_sources() -> None:
    text = read(SPEC_PATH)
    for expected in [PARENT_ID, CLOSURE_ID, RT010_SPEC_ID, STAGE2_PLAN_ID, REMEDIATION_LEDGER_ID, *AUDIT_IDS]:
        assert expected in text


def test_references_scaffold_and_owner_specs() -> None:
    text = read(SPEC_PATH)
    assert SCAFFOLD_REF in text
    for ref in RT_SPEC_REFS:
        assert ref in text


def test_defines_required_sections_and_contracts() -> None:
    text = read(SPEC_PATH)
    for heading in [
        "## 2. Scope",
        "## 3. Must-not-own boundaries",
        "## 4. Authority model",
        "## 5. D-series/native-design pressure contract",
        "## 6. Promotion-boundary contract",
        "## 7. Runtime-owner handoff contract",
        "## 8. Sourcebook/canon/training/live-play exclusion contract",
        "## 9. Future D-series/native-design promotion-boundary artifact inventory",
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


def test_pressure_contract_includes_planning_placeholders_and_disclaimer() -> None:
    text = read(SPEC_PATH)
    for term in PRESSURE_TERMS:
        assert term in text
    for phrase in [
        "planning terms only",
        "not final schemas",
        "not database fields",
        "not promotion states",
        "not canon states",
        "not sourcebook states",
        "not reviewer workflows",
        "not runtime state",
        "not event records",
        "not validators",
        "not training policy",
        "not live-play prompts",
    ]:
        assert phrase in text


def test_promotion_boundary_contract_present() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "cannot become authority by existence",
        "Source-pack material is pressure, not doctrine",
        "Source-pack material is not canon",
        "Source-pack material is not sourcebook content",
        "Source-pack material is not training data unless separately authorized",
        "must route to the relevant RT owner",
        "Repeated use in play, examples, summaries, generated content, or conversion output does not promote content",
        "Unpromoted design pressure must remain rejected, quarantined, or source-local pressure",
    ]:
        assert phrase in text


def test_runtime_owner_handoff_contract_present() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "proposes command/action procedure must route through RT-001",
        "proposes costs, resources, rewards, losses, consequences, economy, or recovery pressure must route through RT-002",
        "proposes combat, hazards, damage, injury, healing, recovery, mitigation, or threats must route through RT-003",
        "proposes abilities, effects, techniques, powers, skills, prerequisites, targeting, cooldowns, or scaling must route through RT-004",
        "proposes hidden information, reveal boundaries, context packets, claims, rumors, redaction, or narrator fact sets must route through RT-005",
        "proposes missions, rewards, clues, objectives, branches, scenarios, failure, or hidden truths must route through RT-006",
        "proposes social state, faction state, actor knowledge, reputation, relationships, contacts, rumors, or institutional response must route through RT-007",
        "proposes generated content, recurrence, provenance, durable generation, or source-local generated records must route through RT-008",
        "proposes RNG, tables, oracles, random outputs, seed/replay, or result domains must route through RT-009",
        "proposes items, inventory, gear, vehicles, assets, relics, implants, companions, cargo, ownership, custody, repair, salvage, crafting, or requisition must route through RT-010",
        "proposes validation/readiness, tests, gates, benchmark checks, or implementation readiness must route through RT-011",
    ]:
        assert phrase in text
    assert "routing only" in text
    assert "does not authorize implementation" in text


def test_exclusion_contract_present() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "Sourcebook inclusion is blocked until separate sourcebook governance authorizes it",
        "Canon promotion is blocked until separate canon governance authorizes it",
        "Training use is blocked until separate training/data governance authorizes it",
        "Live-play use is blocked until separate live-play adapter governance authorizes it",
        "Summaries are not promotion evidence",
        "Narration is not promotion evidence",
        "Examples are not promotion evidence",
    ]:
        assert phrase in text


def test_future_artifact_inventory_is_future_only() -> None:
    text = read(SPEC_PATH)
    for artifact in FUTURE_ARTIFACTS:
        assert artifact in text
    assert text.count("future_required_not_implemented") >= len(FUTURE_ARTIFACTS)
    assert "not implemented schemas, records, validators, services, workflows, or runtime code" in text


def test_validation_readiness_requirements_are_future_only() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "source linkage validation",
        "RT-012 owner-boundary validation",
        "D-series/native-design non-authority validation",
        "source-pack pressure versus authority separation validation",
        "native-design claim routing validation",
        "doctrine conflict routing validation",
        "RT owner handoff validation",
        "sourcebook candidate boundary validation",
        "canon candidate boundary validation",
        "training exclusion validation",
        "live-play exclusion validation",
        "example-pack non-authority validation",
        "converted-content non-authority validation",
        "generated-content non-authority validation",
        "live-play narration non-authority validation",
        "unpromoted-content quarantine validation",
        "reviewer-decision requirement validation",
        "LLM non-authority validation",
        "non-implementation guardrail validation",
        "coordinate with RT-011 without implementing validators",
    ]:
        assert phrase in text


def test_llm_non_authority_prohibitions_are_representative() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "promoting D-series/native-design content to doctrine",
        "promoting D-series/native-design content to canon",
        "promoting D-series/native-design content to sourcebook inclusion",
        "treating source packs as authority",
        "treating examples as authority",
        "treating converted content as authority",
        "treating generated content as authority",
        "treating summaries as promotion evidence",
        "treating live-play narration as promotion evidence",
        "authorizing training use",
        "authorizing live-play use",
        "authorizing sourcebook inclusion",
        "authorizing canon promotion",
        "authorizing pilot conversion",
        "resolving doctrine conflicts",
        "deciding reviewer outcomes",
        "bypassing RT owner handoffs",
        "creating promotion records as backend truth",
        "mutating authority hierarchy",
        "inventing promotion state",
        "inventing canon state",
        "inventing sourcebook state",
        "rewriting doctrine",
        "treating repeated use as promotion",
        "bypassing RT-001 through RT-011",
        "authorizing runtime/schema/validator/generator implementation",
    ]:
        assert phrase in text


def test_non_implementation_reaffirmation_and_classification_block() -> None:
    text = read(SPEC_PATH)
    for phrase in GUARDRAIL_PHRASES:
        assert phrase in text
    for phrase in [
        "stage2_output:",
        "stage2_pr_id: STAGE2-PR-H2",
        "parent_stage2_pr_id: STAGE2-PR-H",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "resolves_deferred_owner_spec_gap: true",
        "creates_runtime_implementation: false",
        "authorizes_d_series_promotion_system: false",
        "authorizes_native_design_promotion_system: false",
        "authorizes_canon_promotion: false",
        "authorizes_sourcebook_inclusion: false",
        "authorizes_training: false",
        "authorizes_live_play: false",
        "authorizes_pilot_conversion: false",
        "next_allowed_step: Runtime/schema implementation sequencing review, pending review",
    ]:
        assert phrase in text


def test_registry_and_decision_log_tracking_exists() -> None:
    registry = read(REGISTRY_PATH)
    decision_log = read(DECISION_LOG_PATH)
    for text in [registry, decision_log]:
        assert TRACKING_ID in text
        assert "STAGE2-PR-H2" in text
        assert "resolves RT-012 deferred owner-specification gap" in text
        for phrase in [
            "no runtime implementation",
            "no schema implementation",
            "no validator implementation",
            "no generator implementation",
            "no D-series promotion system",
            "no native-design promotion system",
            "no canon promotion procedure",
            "no sourcebook inclusion procedure",
            "no sourcebook inclusion authorization",
            "no pilot conversion authorization",
            "no canon promotion",
        ]:
            assert phrase.lower() in text.lower()


def test_no_file_claims_implementation_authority_for_rt012() -> None:
    combined = "\n".join([read(SPEC_PATH), read(REGISTRY_PATH), read(DECISION_LOG_PATH)])
    forbidden_claims = [
        "creates runtime implementation: true",
        "authorizes_runtime_implementation: true",
        "authorizes_schema_implementation: true",
        "authorizes_validator_implementation: true",
        "authorizes_generator_implementation: true",
        "authorizes_command_ir: true",
        "authorizes_d_series_promotion_system: true",
        "authorizes_native_design_promotion_system: true",
        "authorizes_canon_promotion_procedure: true",
        "authorizes_sourcebook_inclusion_procedure: true",
        "authorizes_training_policy: true",
        "authorizes_live_play_policy: true",
        "authorizes_sourcebook_inclusion: true",
        "authorizes_canon_promotion: true",
        "authorizes_pilot_conversion: true",
    ]
    lowered = combined.lower()
    for forbidden in forbidden_claims:
        assert forbidden not in lowered
