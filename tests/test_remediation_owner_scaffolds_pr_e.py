from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RT004_PATH = ROOT / "docs" / "doctrine" / "control" / "RT004_ability_effect_skill_binding_owner_scaffold.md"
RT007_PATH = ROOT / "docs" / "doctrine" / "control" / "RT007_social_faction_knowledge_state_owner_scaffold.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_pr_e_owner_scaffold_files_exist() -> None:
    assert RT004_PATH.exists()
    assert RT007_PATH.exists()


def test_both_scaffolds_reference_remediation_priority_ledger() -> None:
    for path in [RT004_PATH, RT007_PATH]:
        text = read(path)
        assert "REMEDIATION-PRIORITY-LEDGER-001" in text
        assert "owner scaffold" in text


def test_rt004_references_dependencies_sources_and_invariants() -> None:
    text = read(RT004_PATH)
    for phrase in [
        "RT-004",
        "RT-001",
        "RT-002",
        "RT-008",
        "RT-011",
        "RT-003",
        "RT-005",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
        "A08",
        "A09",
        "A10",
        "B02",
        "C03",
        "SM00",
        "backend-first language",
        "backend-first model-interchangeability invariant",
    ]:
        assert phrase in text


def test_rt004_states_required_downstream_controls() -> None:
    text = read(RT004_PATH)
    for phrase in [
        "Ability/effect use must remain downstream of RT-001 command lifecycle",
        "Cost/backlash/cooldown pressure must remain downstream of RT-002",
        "Generated abilities or techniques require RT-008 provenance/recurrence controls before persistence",
        "Narration may only describe backend-approved ability/effect outcomes",
    ]:
        assert phrase in text


def test_rt004_prohibits_llm_ability_and_advancement_authority() -> None:
    text = read(RT004_PATH)
    for phrase in [
        "inventing abilities, powers, techniques, skills, perks, or mastery",
        "awarding advancement",
        "changing prerequisites",
        "setting costs or cooldowns",
        "resolving effects as mechanical truth",
        "binding abilities to actions as authority",
        "deciding skill synthesis outputs as persistent state",
        "creating generated abilities or techniques",
        "granting player capability",
        "bypassing validation/reviewer approval",
        "treating ability narration as backend effect resolution",
    ]:
        assert phrase in text


def test_rt004_names_only_conceptual_placeholders() -> None:
    text = read(RT004_PATH)
    for phrase in [
        "ability_record_reference",
        "prerequisite_check_required",
        "acquisition_eligibility_pending",
        "mastery_state_pending",
        "effect_taxonomy_required",
        "cost_binding_required",
        "cooldown_state_pending",
        "action_binding_required",
        "skill_synthesis_review",
        "advancement_trigger_pending",
        "generated_ability_prohibited",
        "conceptual placeholders only",
        "not final schemas",
        "not ability records",
        "not generated powers",
        "not advancement rules",
        "not final formulas",
        "not command IR",
        "not runtime state",
        "not validators",
        "not live-play authorization",
    ]:
        assert phrase in text


def test_rt007_references_dependencies_sources_and_hidden_info() -> None:
    text = read(RT007_PATH)
    for phrase in [
        "RT-007",
        "RT-001",
        "RT-005",
        "RT-008",
        "RT-011",
        "RT-002",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
        "B09",
        "C01",
        "C05",
        "C06/C07 where relevant",
        "C06_location_site_region_record_schema.md",
        "C07_mission_scenario_adventure_record_schema.md",
        "backend-first language",
        "hidden-info language",
        "backend-first model-interchangeability invariant",
    ]:
        assert phrase in text


def test_rt007_states_required_social_faction_controls() -> None:
    text = read(RT007_PATH)
    for phrase in [
        "Dialogue may produce a claim candidate only, not authoritative truth",
        "Social/faction state must remain backend-owned, persistent, auditable, and redacted through RT-005",
        "Recurring factions, NPCs, and contacts require RT-008 provenance/recurrence controls",
        "Narration may describe only backend-approved social/faction facts, visible attitudes, known standing, or authorized rumors",
    ]:
        assert phrase in text


def test_rt007_prohibits_llm_social_faction_authority() -> None:
    text = read(RT007_PATH)
    for phrase in [
        "mutating relationship state",
        "changing faction standing",
        "deciding NPC/faction beliefs as truth",
        "creating actor knowledge records",
        "committing obligations, favors, debts, reputation, or institutional consequences",
        "inventing faction actions as backend events",
        "treating dialogue as durable memory authority",
        "treating summaries as relationship state",
        "revealing hidden agendas",
        "creating recurring factions or contacts without provenance",
        "bypassing backend validation/reviewer approval",
    ]:
        assert phrase in text


def test_rt007_names_only_conceptual_placeholders() -> None:
    text = read(RT007_PATH)
    for phrase in [
        "relationship_state_pending",
        "standing_delta_candidate",
        "faction_memory_partition",
        "actor_belief_partition",
        "contact_access_pending",
        "obligation_or_debt_candidate",
        "institutional_action_pending",
        "hidden_agenda_redaction",
        "dialogue_claim_pending_review",
        "reputation_event_required",
        "faction_recurrence_requires_provenance",
        "conceptual placeholders only",
        "not final schemas",
        "not relationship mechanics",
        "not faction runtime",
        "not actor-knowledge database",
        "not dialogue memory system",
        "not persistence writer",
        "not context-packet compiler",
        "not generator",
        "not live-play authorization",
    ]:
        assert phrase in text


def test_both_files_include_explicit_non_implementation_guardrails() -> None:
    for path in [RT004_PATH, RT007_PATH]:
        text = read(path)
        for phrase in [
            "planning/control only",
            "Explicit non-implementation statement",
            "implements no doctrine rewrite",
            "runtime",
            "schema",
            "command IR",
            "math",
            "validator",
            "generator",
            "persistence writer",
            "retrieval index",
            "context-packet compiler",
            "live-play prompt",
            "training behavior",
            "donor-content audit",
            "canon promotion",
        ]:
            assert phrase in text


def test_registry_tracks_pr_e_owner_scaffolds() -> None:
    registry = read(REGISTRY_PATH)
    for phrase in [
        "REMEDIATION-RT004-ABILITY-EFFECT-SKILL-BINDING-OWNER-SCAFFOLD-001",
        "RT004_ability_effect_skill_binding_owner_scaffold.md",
        "REMEDIATION-RT007-SOCIAL-FACTION-KNOWLEDGE-STATE-OWNER-SCAFFOLD-001",
        "RT007_social_faction_knowledge_state_owner_scaffold.md",
        "owner scaffold only",
        "no doctrine rewrite",
        "no runtime implementation",
        "no schema implementation",
        "no command IR implementation",
        "no math implementation",
        "no validator implementation",
        "no generator implementation",
        "no generated ability creation",
        "no advancement award",
        "no relationship mutation",
        "no faction action commitment",
        "no actor-knowledge database implementation",
        "no persistence writer implementation",
        "no retrieval index implementation",
        "no context-packet compiler implementation",
        "no canon promotion",
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in registry


def test_scaffolds_and_registry_do_not_claim_to_implement_runtime_artifacts() -> None:
    forbidden_claims = [
        "implements abilities",
        "implements powers",
        "implements skills",
        "implements advancement",
        "implements social runtime",
        "implements relationship schemas",
        "implements actor-knowledge database",
        "implements faction actions",
        "implements generators",
        "implements validators",
        "implements runtime",
        "implements persistence writers",
        "implements retrieval indexes",
        "implements context-packet compilers",
        "implements live-play prompts",
        "implements training behavior",
        "abilities implemented",
        "powers implemented",
        "skills implemented",
        "advancement implemented",
        "social runtime implemented",
        "relationship schemas implemented",
        "actor-knowledge database implemented",
        "faction actions implemented",
        "generators implemented",
        "validators implemented",
        "runtime implemented",
        "persistence writers implemented",
        "retrieval indexes implemented",
        "context-packet compilers implemented",
        "live-play prompts implemented",
        "training behavior implemented",
        "runtime-ready",
        "validator-ready",
        "generator-ready",
        "live-play ready",
    ]

    registry_text = read(REGISTRY_PATH)
    pr_e_registry_entry = registry_text.rsplit(
        "REMEDIATION-RT004-ABILITY-EFFECT-SKILL-BINDING-OWNER-SCAFFOLD-001",
        1,
    )[1].lower()

    for text in [read(RT004_PATH).lower(), read(RT007_PATH).lower(), pr_e_registry_entry]:
        for phrase in forbidden_claims:
            assert phrase not in text
