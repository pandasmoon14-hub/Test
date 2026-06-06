from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT004_ability_effect_skill_binding_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT004-ABILITY-EFFECT-SKILL-BINDING-OWNER-SPEC-001"
STAGE2_PR_ID = "STAGE2-PR-G2"
PARENT_STAGE2_PR_ID = "STAGE2-PR-G"
TRACK = "RT-004"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

REQUIRED_REFS = [
    "docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md",
    "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md",
    "docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md",
    "docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md",
    "docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md",
    "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md",
    "docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md",
    "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md",
]

BINDING_PLACEHOLDERS = [
    "ability_binding_required",
    "effect_family_required",
    "effect_output_pending",
    "skill_binding_required",
    "competency_binding_required",
    "prerequisite_check_pending",
    "access_gate_pending",
    "target_scope_pending",
    "range_area_dependency_pending",
    "duration_dependency_pending",
    "cooldown_or_recharge_dependency",
    "sustain_or_concentration_dependency",
    "interrupt_or_counter_dependency",
    "resistance_or_save_dependency",
    "scaling_rank_tier_dependency",
    "advancement_unlock_dependency",
    "item_relic_implant_effect_dependency",
    "companion_or_summon_effect_dependency",
    "vehicle_or_platform_effect_dependency",
    "hidden_capability_visibility_required",
    "random_effect_dependency",
    "generated_effect_provenance_required",
    "effect_resolution_quarantined",
]

FUTURE_ARTIFACTS = [
    "AbilityBindingRequirement",
    "EffectFamilyRequirement",
    "EffectOutputRequirement",
    "SkillBindingRequirement",
    "CompetencyBindingRequirement",
    "PrerequisiteRequirement",
    "AccessGateRequirement",
    "TargetScopeRequirement",
    "RangeAreaRequirement",
    "DurationRequirement",
    "CooldownRechargeRequirement",
    "SustainInterruptRequirement",
    "ResistanceSaveRequirement",
    "ScalingRankTierRequirement",
    "AdvancementUnlockRequirement",
    "ItemRelicImplantEffectRequirement",
    "CompanionSummonEffectRequirement",
    "VehiclePlatformEffectRequirement",
    "HiddenCapabilityVisibilityRequirement",
    "RandomEffectDependencyRequirement",
    "GeneratedEffectProvenanceRequirement",
    "AbilityEffectValidationRequirement",
]

GUARDRAILS = [
    "runtime code",
    "schema implementation",
    "command IR implementation",
    "validator implementation",
    "generator implementation",
    "ability system",
    "effect taxonomy",
    "skill system",
    "proficiency/competency system",
    "prerequisite system",
    "targeting rules",
    "range/area rules",
    "duration rules",
    "cooldown/recharge/sustain rules",
    "interrupt/counter rules",
    "resistance/save/check rules",
    "scaling/rank/tier rules",
    "advancement unlock rules",
    "item/relic/implant effect rules",
    "companion/summon effect rules",
    "vehicle/platform effect rules",
    "ability schema",
    "skill schema",
    "effect schema",
    "condition schema",
    "damage formulas",
    "resource formulas",
    "RNG/dice/table implementation",
    "event ledger implementation",
    "database schema",
    "persistence writer",
    "retrieval index",
    "context-packet compiler",
    "live-play prompt",
    "training data",
    "donor-content audit",
    "sourcebook inclusion authorization",
    "pilot conversion authorization",
    "canon promotion",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_owner_specification_file_exists_and_has_core_tracking() -> None:
    text = read(SPEC_PATH)
    for expected in [TRACKING_ID, STAGE2_PR_ID, PARENT_STAGE2_PR_ID, TRACK]:
        assert expected in text


def test_references_stage2_plan_ledger_rt_specs_and_audits() -> None:
    text = read(SPEC_PATH)
    for expected in [STAGE2_PLAN_ID, REMEDIATION_LEDGER_ID, *AUDIT_IDS, *REQUIRED_REFS]:
        assert expected in text


def test_defines_scope_and_must_not_own_boundaries() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "ability/effect/skill binding ownership boundaries",
        "effect-family and effect-output requirement boundaries",
        "skill/proficiency/competency/access binding requirement boundaries",
        "prerequisite and eligibility requirement boundaries",
        "targeting, range, area, duration, cooldown, recharge, sustain, interrupt, and resistance requirement boundaries",
        "scaling, rank/tier, advancement-linked, and unlock requirement boundaries",
        "item/relic/implant/vehicle/asset effect handoff through RT-010",
        "Must-not-own boundaries",
    ]:
        assert phrase in text
    for guardrail in GUARDRAILS:
        assert guardrail in text


def test_defines_authority_model() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "RT-001 owns command/action timing, legality, candidate command binding",
        "RT-002 owns resource costs, backlash, corruption, strain",
        "RT-003 owns combat, hazard, damage, healing, mitigation",
        "RT-005 owns hidden prerequisites, hidden capabilities",
        "RT-008 owns generated ability/effect/skill provenance",
        "RT-009 owns random table/oracle dependencies",
        "RT-011 owns validation/readiness requirements",
        "future backend runtime must own ability/effect resolution",
        "The LLM may only describe backend-approved visible ability/effect outcomes",
    ]:
        assert phrase in text


def test_includes_binding_contract_and_placeholder_disclaimer() -> None:
    text = read(SPEC_PATH)
    assert "Ability/effect/skill binding contract" in text
    for placeholder in BINDING_PLACEHOLDERS:
        assert placeholder in text
    for phrase in [
        "planning placeholders only",
        "not final schemas",
        "not database fields",
        "not ability rules",
        "not effect rules",
        "not skill rules",
        "not prerequisites",
        "not targeting rules",
        "not cooldown rules",
        "not runtime state",
        "not event records",
        "not validators",
        "not live-play prompts",
    ]:
        assert phrase in text


def test_includes_resolution_and_commitment_contracts() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "Effect resolution and binding contract",
        "ability labels are not executable effects",
        "effect-family labels are not final effect taxonomy",
        "prerequisites are not eligibility validators by themselves",
        "Ability/effect commitment contract",
        "ability declaration is not effect resolution",
        "effect proposal is not state mutation",
        "target declaration is not target legality",
        "cost declaration is not cost commitment",
        "narration is not event commitment",
        "rejected/quarantined ability/effect actions must not mutate state",
    ]:
        assert phrase in text


def test_inventories_future_artifacts_as_not_implemented() -> None:
    text = read(SPEC_PATH)
    for artifact in FUTURE_ARTIFACTS:
        assert artifact in text
    assert text.count("future_required_not_implemented") >= len(FUTURE_ARTIFACTS)
    assert "semantic requirements only" in text


def test_validation_readiness_requirements_are_future_only() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "Validation and readiness requirements",
        "future requirements only",
        "source linkage validation",
        "ability/effect/skill owner-boundary validation",
        "effect-family coverage validation",
        "skill/competency binding validation",
        "prerequisite/access-gate validation",
        "target/range/area/duration/cooldown/sustain coverage validation",
        "resistance/save/check routing validation",
        "cost/consequence handoff validation",
        "combat/hazard/damage/recovery handoff validation",
        "hidden-capability visibility routing validation",
        "generated-effect provenance validation",
        "random-effect dependency validation",
        "item/relic/implant/vehicle effect handoff validation",
        "command/event boundary validation",
        "LLM non-authority validation",
        "non-implementation guardrail validation",
    ]:
        assert phrase in text


def test_downstream_handoffs_cover_rt001_through_rt012() -> None:
    text = read(SPEC_PATH)
    for rt_id in [f"RT-{i:03d}" for i in range(1, 13)]:
        assert rt_id in text
    for phrase in [
        "RT-006 for mission abilities",
        "RT-007 for social abilities",
        "RT-010 for item, gear, relic, implant, vehicle, platform, companion",
        "RT-012 for D-series/native-design ability, effect, skill, technique, or power patterns",
    ]:
        assert phrase in text


def test_llm_non_authority_prohibitions_are_explicit() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "deciding ability legality",
        "deciding target legality",
        "validating prerequisites",
        "granting abilities",
        "granting skills",
        "granting techniques",
        "applying effects as mechanical truth",
        "choosing effect outputs",
        "spending or refunding costs",
        "revealing hidden prerequisites or hidden capabilities",
        "selecting random effect outcomes",
        "committing state deltas",
        "committing events",
        "treating ability narration as mechanical resolution",
        "inventing formulas, tables, thresholds, tags, fields, or schemas",
        "authorizing canon/sourcebook/training/live-play use",
    ]:
        assert phrase in text


def test_non_implementation_reaffirmation_and_classification_block() -> None:
    text = read(SPEC_PATH)
    assert "Non-implementation reaffirmation" in text
    assert "stage2_output:" in text
    for phrase in [
        "stage2_pr_id: STAGE2-PR-G2",
        "parent_stage2_pr_id: STAGE2-PR-G",
        "track: RT-004",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_generator_implementation: false",
        "authorizes_ability_system: false",
        "authorizes_effect_taxonomy: false",
        "authorizes_skill_system: false",
        "authorizes_prerequisite_system: false",
        "authorizes_targeting_rules: false",
        "authorizes_cooldown_rules: false",
        "authorizes_duration_rules: false",
        "authorizes_scaling_rules: false",
        "authorizes_item_effects: false",
        "authorizes_condition_system: false",
        "authorizes_rng_implementation: false",
        "authorizes_event_ledger: false",
        "authorizes_context_packet_compiler: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_sourcebook_inclusion: false",
        "authorizes_canon_promotion: false",
        "authorizes_pilot_conversion: false",
        "next_allowed_step: RT-006 owner specification, pending review",
    ]:
        assert phrase in text


def test_registry_and_decision_log_tracking_exist_with_guardrails() -> None:
    for path in [REGISTRY_PATH, DECISION_LOG_PATH]:
        text = read(path)
        assert TRACKING_ID in text
        assert "Stage 2 owner specification" in text or "Stage 2 owner-specification" in text
        assert "split from the original STAGE2-PR-G downstream-domain bundle for review safety" in text
        for guardrail in GUARDRAILS:
            assert guardrail in text


def test_changed_files_do_not_authorize_implementation() -> None:
    for path in [SPEC_PATH, REGISTRY_PATH, DECISION_LOG_PATH]:
        text = read(path)
        assert "authorizes_runtime_implementation: false" in text or "no runtime implementation" in text
        assert "authorizes_schema_implementation: false" in text or "no schema implementation" in text
        assert "authorizes_validator_implementation: false" in text or "no validator implementation" in text
        assert "authorizes_generator_implementation: false" in text or "no generator implementation" in text
        assert "no sourcebook inclusion authorization" in text
        assert "no pilot conversion authorization" in text
        assert "no canon promotion" in text
