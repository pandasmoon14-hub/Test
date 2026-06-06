from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT003_combat_hazard_damage_recovery_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT003-COMBAT-HAZARD-DAMAGE-RECOVERY-OWNER-SPEC-001"
STAGE2_PR_ID = "STAGE2-PR-G1"
PARENT_STAGE2_PR_ID = "STAGE2-PR-G"
TRACK = "RT-003"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

REQUIRED_SCAFFOLD_REF = "docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md"
RT001_SPEC_REF = "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md"
RT002_SPEC_REF = "docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md"
RT005_SPEC_REF = "docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md"
RT008_SPEC_REF = "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md"
RT009_SPEC_REF = "docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md"
RT011_SPEC_REF = "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md"

PRESSURE_PLACEHOLDERS = [
    "combat_resolution_required",
    "active_threat_contact_pending",
    "hazard_contact_pending",
    "damage_family_required",
    "injury_family_required",
    "mitigation_requirement_pending",
    "recovery_requirement_pending",
    "exposure_tick_pending",
    "ongoing_harm_pending",
    "resistance_or_vulnerability_dependency",
    "armor_or_soak_dependency",
    "condition_dependency_pending",
    "vehicle_or_asset_damage_dependency",
    "hidden_hazard_visibility_required",
    "random_damage_or_hazard_dependency",
    "consequence_event_pending",
    "encounter_state_quarantined",
]

FUTURE_ARTIFACTS = [
    "CombatResolutionRequirement",
    "HazardContactRequirement",
    "ActiveThreatRequirement",
    "DamageFamilyRequirement",
    "InjuryFamilyRequirement",
    "MitigationRequirement",
    "RecoveryRequirement",
    "ExposureRequirement",
    "OngoingHarmRequirement",
    "ResistanceVulnerabilityRequirement",
    "ArmorSoakRequirement",
    "ConditionDependencyRequirement",
    "VehicleAssetDamageRequirement",
    "HiddenHazardVisibilityRequirement",
    "RandomDamageHazardRequirement",
    "ConsequenceEventRequirement",
    "CombatHazardValidationRequirement",
]

GUARDRAILS = [
    "runtime code",
    "schema implementation",
    "command IR implementation",
    "validator implementation",
    "generator implementation",
    "combat rules",
    "hazard rules",
    "damage formulas",
    "injury tables",
    "condition system",
    "healing/recovery formulas",
    "mitigation math",
    "exposure clocks",
    "active-threat runtime",
    "initiative/action economy",
    "encounter runtime",
    "vehicle/platform damage system",
    "item durability system",
    "armor/resistance/soak rules",
    "death/dying rules",
    "monster/NPC combat schema",
    "hazard schema",
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
    for expected in [TRACKING_ID, STAGE2_PR_ID, TRACK]:
        assert expected in text


def test_references_parent_stage2_pr() -> None:
    text = read(SPEC_PATH)
    assert PARENT_STAGE2_PR_ID in text


def test_references_stage2_plan_and_ledger() -> None:
    text = read(SPEC_PATH)
    assert STAGE2_PLAN_ID in text
    assert REMEDIATION_LEDGER_ID in text


def test_references_rt003_scaffold() -> None:
    text = read(SPEC_PATH)
    assert REQUIRED_SCAFFOLD_REF in text


def test_references_rt001_owner_specification() -> None:
    text = read(SPEC_PATH)
    assert RT001_SPEC_REF in text


def test_references_rt002_owner_specification() -> None:
    text = read(SPEC_PATH)
    assert RT002_SPEC_REF in text


def test_references_rt005_owner_specification() -> None:
    text = read(SPEC_PATH)
    assert RT005_SPEC_REF in text


def test_references_rt008_owner_specification() -> None:
    text = read(SPEC_PATH)
    assert RT008_SPEC_REF in text


def test_references_rt009_owner_specification() -> None:
    text = read(SPEC_PATH)
    assert RT009_SPEC_REF in text


def test_references_rt011_owner_specification() -> None:
    text = read(SPEC_PATH)
    assert RT011_SPEC_REF in text


def test_references_audit_sources() -> None:
    text = read(SPEC_PATH)
    for audit_id in AUDIT_IDS:
        assert audit_id in text


def test_defines_scope_and_must_not_own_boundaries() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "combat/hazard/damage/recovery ownership boundaries",
        "active-threat and hazard-contact boundary requirements",
        "damage-family and injury-family requirement boundaries",
        "recovery, mitigation, exposure, and ongoing-harm requirement boundaries",
        "combat/hazard consequence handoff requirements",
        "encounter-state pressure boundaries",
        "combat/hazard visibility handoff to RT-005",
        "cost/consequence math handoff to RT-002",
        "action legality and command/event timing handoff to RT-001",
        "generated hazard/threat provenance handoff to RT-008",
        "random hazard/combat/table/oracle dependency handoff to RT-009",
        "item/vehicle/platform damage and repair handoff to RT-010",
        "## 3. Must-not-own boundaries",
    ]:
        assert phrase in text


def test_defines_authority_model() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "RT-001 owns command/action timing, legality, resolution-trigger handoff, rejection/quarantine, and event-commit boundaries",
        "RT-002 owns resource, cost, damage-as-resource-pressure, recovery cost, mitigation cost, consequence math, reward/loss pressure, and failed-command cost outcomes",
        "RT-005 owns hidden/visible hazard, threat, damage, consequence, and recovery visibility",
        "RT-009 owns RNG/table/oracle dependency authority for random damage, random hazards, random encounters, random exposure, and random recovery outcomes",
        "RT-011 owns validation/readiness requirements",
        "future backend runtime must own combat/hazard resolution, state deltas, event commits, and persistence if separately authorized",
        "the LLM may only narrate backend-approved visible outcomes and may not resolve combat, apply damage, reveal hidden hazards, or commit recovery",
    ]:
        assert phrase in text


def test_pressure_contract_includes_planning_placeholders() -> None:
    text = read(SPEC_PATH)
    for state in PRESSURE_PLACEHOLDERS:
        assert state in text


def test_pressure_contract_states_planning_only() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "not final schemas",
        "not database fields",
        "not combat rules",
        "not damage formulas",
        "not injury tables",
        "not conditions",
        "not encounter runtime",
        "not event records",
        "not validators",
        "not runtime state",
        "not live-play prompts",
    ]:
        assert phrase in text


def test_damage_injury_recovery_mitigation_contract() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "damage-family labels are not formulas",
        "injury-family labels are not injury tables",
        "recovery requirements are not healing formulas",
        "mitigation requirements are not armor/resistance/soak rules",
        "persistent harm requires future state/event/persistence ownership",
        "hidden harm or hidden hazard information must route through RT-005",
        "cost-bearing damage/recovery/mitigation must route through RT-002",
        "random damage/hazard/recovery requires RT-009",
        "generated hazards or threats require RT-008 provenance",
        "item/vehicle/platform damage or repair requires RT-010",
        "abilities/effects that cause or prevent damage require RT-004",
        "mission/scenario consequences require RT-006",
        "social/faction consequences require RT-007",
        "validation/readiness requires RT-011",
    ]:
        assert phrase in text


def test_combat_hazard_commitment_contract() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "combat/hazard contact is not resolution",
        "damage declaration is not damage commitment",
        "mitigation declaration is not mitigation commitment",
        "recovery declaration is not recovery commitment",
        "random damage or hazard dependency is not random outcome selection",
        "narration is not event commitment",
        "rejected/quarantined combat or hazard actions must not mutate state",
        "event/state/persistence commitment requires future separately authorized backend systems",
    ]:
        assert phrase in text


def test_future_artifact_inventory_is_future_only() -> None:
    text = read(SPEC_PATH)
    for artifact in FUTURE_ARTIFACTS:
        assert artifact in text
    assert text.count("future_required_not_implemented") >= len(FUTURE_ARTIFACTS)


def test_validation_readiness_requirements() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "source linkage validation",
        "combat/hazard owner-boundary validation",
        "damage-family coverage validation",
        "injury-family coverage validation",
        "recovery/mitigation coverage validation",
        "hidden-hazard routing validation",
        "random-dependency routing validation",
        "cost/consequence handoff validation",
        "generated-hazard provenance validation",
        "item/vehicle/platform damage handoff validation",
        "command/event boundary validation",
        "LLM non-authority validation",
        "non-implementation guardrail validation",
    ]:
        assert phrase in text


def test_downstream_handoffs_cover_all_tracks() -> None:
    text = read(SPEC_PATH)
    for rt in [f"RT-{i:03d}" for i in range(1, 13)]:
        assert rt in text


def test_llm_non_authority_prohibitions() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "resolving combat",
        "deciding hazard contact",
        "applying damage",
        "assigning injuries",
        "clearing injuries",
        "healing characters",
        "choosing mitigation outcomes",
        "applying resistance, vulnerability, armor, or soak as mechanical truth",
        "applying conditions as mechanical truth",
        "ticking exposure clocks",
        "mutating active threat state",
        "selecting random damage or hazard results",
        "revealing hidden hazards",
        "deciding hidden damage or hidden consequences",
        "mutating item, vehicle, or platform damage state",
        "committing recovery",
        "committing consequence events",
        "treating combat narration as event commitment",
        "inventing formulas, tables, thresholds, or state fields",
        "bypassing RT-001, RT-002, RT-005, RT-009, or RT-011",
        "authorizing canon/sourcebook/training/live-play use",
    ]:
        assert phrase in text


def test_non_implementation_reaffirmation() -> None:
    text = read(SPEC_PATH)
    for phrase in GUARDRAILS:
        assert phrase in text


def test_stage2_output_classification_block() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "stage2_output:",
        "stage2_pr_id: STAGE2-PR-G1",
        "parent_stage2_pr_id: STAGE2-PR-G",
        "track: RT-003",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_generator_implementation: false",
        "authorizes_combat_rules: false",
        "authorizes_hazard_rules: false",
        "authorizes_damage_formulas: false",
        "authorizes_injury_tables: false",
        "authorizes_condition_system: false",
        "authorizes_recovery_formulas: false",
        "authorizes_encounter_runtime: false",
        "authorizes_rng_implementation: false",
        "authorizes_event_ledger: false",
        "authorizes_context_packet_compiler: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_sourcebook_inclusion: false",
        "authorizes_canon_promotion: false",
        "authorizes_pilot_conversion: false",
        "next_allowed_step: RT-004 owner specification, pending review",
    ]:
        assert phrase in text


def test_registry_tracking_exists() -> None:
    text = read(REGISTRY_PATH)
    assert TRACKING_ID in text
    assert "Stage 2 owner" in text or "Stage 2 owner-specification" in text


def test_decision_log_tracking_exists() -> None:
    text = read(DECISION_LOG_PATH)
    assert TRACKING_ID in text
    assert "Stage 2 owner" in text or "Stage 2 owner-specification" in text


def test_registry_and_decision_log_contain_guardrails() -> None:
    for path in [REGISTRY_PATH, DECISION_LOG_PATH]:
        text = read(path)
        for phrase in GUARDRAILS:
            assert phrase in text, f"Guardrail '{phrase}' missing from {path.name}"


def test_no_file_claims_implementation() -> None:
    for path in [SPEC_PATH, REGISTRY_PATH, DECISION_LOG_PATH]:
        text = read(path)
        for claim in [
            "implements combat rules",
            "implements hazard rules",
            "implements damage formulas",
            "implements injury tables",
            "implements condition system",
            "implements healing/recovery formulas",
            "implements mitigation math",
            "implements exposure clocks",
            "implements active-threat runtime",
            "implements encounter runtime",
            "implements vehicle/platform damage system",
            "implements item durability system",
            "implements armor/resistance/soak rules",
            "implements death/dying rules",
            "implements monster/NPC combat schema",
            "implements hazard schema",
            "implements runtime",
            "implements schemas",
            "creates database schema",
            "creates live-play prompt",
            "creates training data",
            "authorizes canon promotion",
            "authorizes pilot conversion",
            "authorizes sourcebook inclusion",
        ]:
            assert claim not in text, f"Implementation claim '{claim}' found in {path.name}"
