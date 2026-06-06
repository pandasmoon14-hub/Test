from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT006_mission_reward_clue_routing_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT006-MISSION-REWARD-CLUE-ROUTING-OWNER-SPEC-001"
STAGE2_PR_ID = "STAGE2-PR-G3"
PARENT_STAGE2_PR_ID = "STAGE2-PR-G"
TRACK = "RT-006"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

REQUIRED_REFS = [
    "docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md",
    "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md",
    "docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md",
    "docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md",
    "docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md",
    "docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md",
    "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md",
    "docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md",
    "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md",
]

ROUTING_PLACEHOLDERS = [
    "mission_route_required",
    "scenario_state_pending",
    "objective_state_pending",
    "objective_completion_pending",
    "branch_resolution_pending",
    "escalation_dependency_pending",
    "clue_route_required",
    "clue_visibility_required",
    "clue_cost_dependency",
    "hidden_truth_reveal_pending",
    "false_clue_or_rumor_partition_required",
    "reward_route_pending",
    "penalty_or_loss_route_pending",
    "failure_outcome_pending",
    "success_outcome_pending",
    "complication_dependency_pending",
    "faction_response_dependency",
    "reputation_consequence_dependency",
    "item_or_asset_reward_dependency",
    "ability_or_effect_reward_dependency",
    "random_mission_or_clue_dependency",
    "generated_mission_provenance_required",
    "scenario_consequence_event_pending",
    "mission_resolution_quarantined",
]

FUTURE_ARTIFACTS = [
    "MissionRoutingRequirement",
    "ScenarioStateRequirement",
    "ObjectiveStateRequirement",
    "ObjectiveCompletionRequirement",
    "ScenarioBranchRequirement",
    "EscalationRequirement",
    "ClueRoutingRequirement",
    "ClueVisibilityRequirement",
    "HiddenTruthRevealRequirement",
    "FalseClueRumorRequirement",
    "InvestigationBoundaryRequirement",
    "RewardRoutingRequirement",
    "PenaltyLossRoutingRequirement",
    "SuccessFailureOutcomeRequirement",
    "ComplicationRequirement",
    "FactionResponseRequirement",
    "ReputationConsequenceRequirement",
    "ItemAssetRewardRequirement",
    "AbilityEffectRewardRequirement",
    "RandomMissionClueRequirement",
    "GeneratedMissionProvenanceRequirement",
    "ScenarioConsequenceEventRequirement",
    "MissionRewardClueValidationRequirement",
]

GUARDRAILS = [
    "runtime code",
    "schema implementation",
    "command IR implementation",
    "validator implementation",
    "generator implementation",
    "mission system",
    "quest system",
    "scenario engine",
    "adventure runtime",
    "objective state machine",
    "branch engine",
    "clue reveal algorithm",
    "investigation rules",
    "hidden-truth reveal procedure",
    "reward economy",
    "mission reward tables",
    "failure/success tables",
    "route planner",
    "escalation clocks",
    "campaign clocks",
    "mission schema",
    "clue schema",
    "reward schema",
    "objective schema",
    "scenario state schema",
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
        "mission/reward/clue routing ownership boundaries",
        "mission, scenario, adventure, objective, branch, route, escalation, reward, penalty, success, failure, clue, and hidden-truth routing requirement boundaries",
        "objective-state and scenario-branch requirement boundaries without implementing objective state machines or branch engines",
        "clue visibility, clue routing, clue-cost, hidden-truth reveal, and investigation handoff requirements",
        "reward, penalty, loss, compensation, debt, obligation, reputation, item, asset, ability, and faction consequence routing requirements",
        "Must-not-own boundaries",
    ]:
        assert phrase in text
    for guardrail in GUARDRAILS:
        assert guardrail in text


def test_defines_authority_model() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "RT-001 owns command/action timing, legality, mission action declaration",
        "RT-002 owns resource costs, mission rewards, penalties, losses",
        "RT-003 owns combat, hazard, damage, opposition, active-threat",
        "RT-004 owns ability, effect, skill, clue-gated capability",
        "RT-005 owns hidden clues, hidden truths, redacted objectives",
        "RT-007 owns social/faction/reputation/institutional consequences",
        "RT-008 owns generated mission/scenario/clue/provenance",
        "RT-009 owns random table/oracle dependencies",
        "RT-010 owns item, vehicle, relic, asset, cargo",
        "RT-011 owns validation/readiness requirements",
        "Future backend runtime must own mission/scenario state",
        "The LLM may only narrate backend-approved visible mission/clue/reward outcomes",
    ]:
        assert phrase in text


def test_includes_routing_contract_and_placeholder_disclaimer() -> None:
    text = read(SPEC_PATH)
    assert "Mission/reward/clue routing contract" in text
    for placeholder in ROUTING_PLACEHOLDERS:
        assert placeholder in text
    for phrase in [
        "planning placeholders only",
        "not final schemas",
        "not database fields",
        "not mission rules",
        "not quest rules",
        "not clue reveal algorithms",
        "not reward tables",
        "not branch engines",
        "not objective state machines",
        "not clocks",
        "not runtime state",
        "not event records",
        "not validators",
        "not live-play prompts",
    ]:
        assert phrase in text


def test_includes_clue_reward_and_commitment_contracts() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "Clue, hidden-truth, and investigation routing contract",
        "clues are not automatically revealed by narration",
        "clue candidates are not player-known facts until backend visibility authorizes them",
        "false clues, rumors, and unverified claims must remain distinct from verified facts",
        "Reward, penalty, success, and failure routing contract",
        "reward labels are not reward economy",
        "penalty labels are not consequence math",
        "objective completion is not reward commitment",
        "mission success/failure declaration is not event commitment",
        "Mission/scenario commitment contract",
        "Mission declaration is not mission creation",
        "Branch proposal is not branch resolution",
        "Reward proposal is not reward commitment",
        "Narration is not event commitment",
        "Rejected/quarantined mission/scenario/clue/reward actions must not mutate state",
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
        "mission/reward/clue owner-boundary validation",
        "objective/branch/route coverage validation",
        "clue visibility and hidden-truth routing validation",
        "rumor/false-clue/unverified-claim separation validation",
        "reward/penalty/success/failure routing validation",
        "cost/consequence handoff validation",
        "combat/hazard/opposition handoff validation",
        "ability/effect/skill reward handoff validation",
        "social/faction/reputation handoff validation",
        "generated-mission provenance validation",
        "random mission/clue/reward dependency validation",
        "item/asset reward/loss handoff validation",
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
        "RT-001 for command lifecycle",
        "RT-002 for resource rewards",
        "RT-003 for combat, hazard, active-threat",
        "RT-004 for mission abilities",
        "RT-005 for hidden clues",
        "RT-007 for social/faction/reputation/institutional consequences",
        "RT-008 for generated missions",
        "RT-009 for random missions",
        "RT-010 for item, gear, relic, implant, vehicle",
        "RT-011 for validation/readiness governance",
        "RT-012 for D-series/native-design mission",
    ]:
        assert phrase in text


def test_llm_non_authority_prohibitions_are_explicit() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "creating missions as backend truth",
        "deciding objective completion",
        "choosing scenario branches",
        "selecting clues",
        "revealing hidden truths",
        "revealing hidden clues",
        "converting rumors or false clues into verified facts",
        "deciding player-known, character-known, NPC-known, or faction-known mission facts",
        "assigning rewards",
        "assigning penalties",
        "determining mission success or failure as mechanical truth",
        "creating reward values",
        "creating reward tables",
        "choosing random mission, clue, reward, or penalty outcomes",
        "creating generated missions, clues, or scenario branches as durable backend truth",
        "mutating mission state",
        "mutating objective state",
        "mutating scenario state",
        "committing reward/loss events",
        "treating mission narration as event commitment",
        "treating summaries as mission memory authority",
        "inventing schemas, fields, state machines, clocks, routes, tables, or formulas",
        "bypassing RT-001, RT-002, RT-005, RT-008, RT-009, or RT-011",
        "authorizing canon/sourcebook/training/live-play use",
    ]:
        assert phrase in text


def test_non_implementation_reaffirmation_and_classification_block() -> None:
    text = read(SPEC_PATH)
    assert "Non-implementation reaffirmation" in text
    assert "stage2_output:" in text
    for phrase in [
        "stage2_pr_id: STAGE2-PR-G3",
        "parent_stage2_pr_id: STAGE2-PR-G",
        "track: RT-006",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_generator_implementation: false",
        "authorizes_mission_system: false",
        "authorizes_quest_system: false",
        "authorizes_scenario_engine: false",
        "authorizes_objective_state_machine: false",
        "authorizes_branch_engine: false",
        "authorizes_clue_reveal_algorithm: false",
        "authorizes_investigation_rules: false",
        "authorizes_reward_economy: false",
        "authorizes_reward_tables: false",
        "authorizes_mission_clocks: false",
        "authorizes_rng_implementation: false",
        "authorizes_event_ledger: false",
        "authorizes_context_packet_compiler: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_sourcebook_inclusion: false",
        "authorizes_canon_promotion: false",
        "authorizes_pilot_conversion: false",
        "next_allowed_step: RT-007 owner specification, pending review",
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
