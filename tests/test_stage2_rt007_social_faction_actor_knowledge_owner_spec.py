from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT007_social_faction_actor_knowledge_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT007-SOCIAL-FACTION-ACTOR-KNOWLEDGE-OWNER-SPEC-001"
STAGE2_PR_ID = "STAGE2-PR-G4"
PARENT_STAGE2_PR_ID = "STAGE2-PR-G"
TRACK = "RT-007"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

REQUIRED_REFS = [
    "docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md",
    "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md",
    "docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md",
    "docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md",
    "docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md",
    "docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md",
    "docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md",
    "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md",
    "docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md",
    "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md",
]

ROUTING_PLACEHOLDERS = [
    "actor_knowledge_route_required",
    "faction_knowledge_route_required",
    "verified_fact_route_required",
    "rumor_route_required",
    "false_claim_partition_required",
    "witness_state_pending",
    "relationship_state_pending",
    "reputation_pressure_pending",
    "standing_shift_pending",
    "influence_dependency_pending",
    "contact_availability_pending",
    "patron_rival_dependency_pending",
    "obligation_or_debt_dependency",
    "favor_or_oath_dependency",
    "threat_or_blackmail_dependency",
    "social_consequence_pending",
    "faction_response_pending",
    "institutional_response_pending",
    "hidden_motive_visibility_required",
    "secret_agenda_visibility_required",
    "random_social_or_faction_dependency",
    "generated_faction_or_contact_provenance_required",
    "social_state_event_pending",
    "social_resolution_quarantined",
]

FUTURE_ARTIFACTS = [
    "ActorKnowledgeRequirement",
    "FactionKnowledgeRequirement",
    "VerifiedFactRequirement",
    "RumorRequirement",
    "FalseClaimRequirement",
    "WitnessStateRequirement",
    "RelationshipStateRequirement",
    "ReputationPressureRequirement",
    "StandingShiftRequirement",
    "InfluenceRequirement",
    "ContactAvailabilityRequirement",
    "PatronRivalRequirement",
    "ObligationDebtRequirement",
    "FavorOathRequirement",
    "ThreatBlackmailRequirement",
    "SocialConsequenceRequirement",
    "FactionResponseRequirement",
    "InstitutionalResponseRequirement",
    "HiddenMotiveVisibilityRequirement",
    "SecretAgendaVisibilityRequirement",
    "RandomSocialFactionRequirement",
    "GeneratedFactionContactProvenanceRequirement",
    "SocialStateEventRequirement",
    "SocialFactionKnowledgeValidationRequirement",
]

GUARDRAILS = [
    "runtime code",
    "schema implementation",
    "command IR implementation",
    "validator implementation",
    "generator implementation",
    "social system",
    "faction system",
    "reputation system",
    "relationship engine",
    "influence system",
    "contact system",
    "dialogue system",
    "actor-knowledge database",
    "faction-knowledge database",
    "rumor system",
    "belief-state engine",
    "deception rules",
    "witness system",
    "obligation/debt economy",
    "favor economy",
    "faction clocks",
    "institutional clocks",
    "patron/rival system",
    "social schema",
    "faction state schema",
    "actor-knowledge schema",
    "reputation schema",
    "relationship schema",
    "contact schema",
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
        "social/faction/actor-knowledge ownership boundaries",
        "actor knowledge, belief, rumor, false claim, verified fact, witness state, and institutional knowledge routing requirement boundaries",
        "faction standing, reputation, relationship, influence, contact, patron, rival, institution, debt, obligation, favor, oath, threat, blackmail, and leverage requirement boundaries",
        "social consequence, faction response, institutional response, witness response, relationship shift, contact availability, and reputation pressure boundaries",
        "Must-not-own boundaries",
    ]:
        assert phrase in text
    for guardrail in GUARDRAILS:
        assert guardrail in text


def test_defines_authority_model() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "RT-001 owns command/action timing, legality, social action declaration",
        "RT-002 owns social costs, debts, obligations, favors, reputation pressure",
        "RT-003 owns combat/hazard consequences that affect social/faction/witness/institutional state",
        "RT-004 owns social abilities, influence effects, faction effects, relationship effects",
        "RT-005 owns hidden motives, secret agendas, rumors, false claims",
        "RT-006 owns mission/contact/faction consequences",
        "RT-008 owns generated NPC/faction/contact/institution provenance",
        "RT-009 owns random table/oracle dependencies for faction reactions",
        "RT-010 owns item/asset/bribe/requisition/custody/blackmail-material handoffs",
        "RT-011 owns validation/readiness requirements",
        "Future backend runtime must own social/faction/actor-knowledge state",
        "The LLM may only narrate backend-approved visible social/faction/knowledge outcomes",
    ]:
        assert phrase in text


def test_includes_routing_contract_and_placeholder_disclaimer() -> None:
    text = read(SPEC_PATH)
    assert "Social/faction/actor-knowledge routing contract" in text
    for placeholder in ROUTING_PLACEHOLDERS:
        assert placeholder in text
    for phrase in [
        "planning placeholders only",
        "not final schemas",
        "not database fields",
        "not social rules",
        "not faction rules",
        "not relationship engines",
        "not reputation systems",
        "not actor-knowledge databases",
        "not rumor systems",
        "not belief engines",
        "not clocks",
        "not runtime state",
        "not event records",
        "not validators",
        "not live-play prompts",
    ]:
        assert phrase in text


def test_includes_actor_knowledge_consequence_and_commitment_contracts() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "Actor-knowledge, rumor, and belief-state routing contract",
        "actor knowledge is not model memory",
        "faction knowledge is not narration",
        "dialogue transcripts are not durable truth",
        "rumors, false claims, unverified claims, and verified facts must remain distinct",
        "Social consequence, reputation, and faction response routing contract",
        "reputation labels are not reputation mechanics",
        "relationship labels are not relationship engine",
        "faction standing labels are not faction state",
        "social success/failure declaration is not event commitment",
        "Social/faction commitment contract",
        "social declaration is not social resolution",
        "faction interaction proposal is not faction state mutation",
        "relationship proposal is not relationship state mutation",
        "rumor proposal is not verified fact",
        "dialogue is not durable memory",
        "narration is not event commitment",
        "rejected/quarantined social/faction/knowledge actions must not mutate state",
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
        "social/faction/actor-knowledge owner-boundary validation",
        "actor/faction knowledge coverage validation",
        "rumor/false-claim/unverified/verified-fact separation validation",
        "witness-state routing validation",
        "relationship/reputation/standing coverage validation",
        "obligation/debt/favor/influence routing validation",
        "hidden motive/secret agenda redaction routing validation",
        "mission/clue/faction consequence handoff validation",
        "cost/consequence handoff validation",
        "combat/hazard/social fallout handoff validation",
        "ability/effect/social-skill handoff validation",
        "generated faction/contact provenance validation",
        "random social/faction dependency validation",
        "item/asset/bribe/custody handoff validation",
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
        "RT-002 for social costs",
        "RT-003 for combat/hazard social fallout",
        "RT-004 for social abilities",
        "RT-005 for hidden motives",
        "RT-006 for mission contacts",
        "RT-008 for generated NPCs",
        "RT-009 for random rumors",
        "RT-010 for item, gear, relic, vehicle, asset, bribe",
        "RT-011 for validation/readiness governance",
        "RT-012 for D-series/native-design social",
    ]:
        assert phrase in text


def test_llm_non_authority_prohibitions_are_explicit() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "creating social state as backend truth",
        "creating faction state as backend truth",
        "deciding what an actor knows",
        "deciding what a faction knows",
        "converting rumors into facts",
        "converting false claims into verified facts",
        "deciding witness state",
        "assigning reputation",
        "assigning faction standing",
        "assigning relationship state",
        "creating obligations, debts, favors, oaths, threats, or blackmail as mechanical truth",
        "determining social success or failure as mechanical truth",
        "choosing faction responses",
        "choosing institutional responses",
        "selecting random rumors, contacts, reaction outcomes, or faction complications",
        "creating generated NPCs, factions, contacts, institutions, or relationship content as durable backend truth",
        "mutating social state",
        "mutating faction state",
        "mutating actor knowledge",
        "mutating relationship state",
        "committing reputation/standing events",
        "treating dialogue as durable memory",
        "treating summaries as actor-knowledge authority",
        "treating social narration as event commitment",
        "inventing schemas, fields, state machines, clocks, routes, tables, or formulas",
        "bypassing RT-001, RT-002, RT-005, RT-006, RT-008, RT-009, or RT-011",
        "authorizing canon/sourcebook/training/live-play use",
    ]:
        assert phrase in text


def test_non_implementation_reaffirmation_and_classification_block() -> None:
    text = read(SPEC_PATH)
    assert "Non-implementation reaffirmation" in text
    assert "stage2_output:" in text
    for phrase in [
        "stage2_pr_id: STAGE2-PR-G4",
        "parent_stage2_pr_id: STAGE2-PR-G",
        "track: RT-007",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_generator_implementation: false",
        "authorizes_social_system: false",
        "authorizes_faction_system: false",
        "authorizes_reputation_system: false",
        "authorizes_relationship_engine: false",
        "authorizes_actor_knowledge_database: false",
        "authorizes_faction_knowledge_database: false",
        "authorizes_rumor_system: false",
        "authorizes_belief_state_engine: false",
        "authorizes_faction_clocks: false",
        "authorizes_dialogue_system: false",
        "authorizes_rng_implementation: false",
        "authorizes_event_ledger: false",
        "authorizes_context_packet_compiler: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_sourcebook_inclusion: false",
        "authorizes_canon_promotion: false",
        "authorizes_pilot_conversion: false",
        "next_allowed_step: RT-010 and RT-012 deferred convergence planning, pending review",
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
