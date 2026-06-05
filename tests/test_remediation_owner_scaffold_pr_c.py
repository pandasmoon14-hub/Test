from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RT005_PATH = ROOT / "docs" / "doctrine" / "control" / "RT005_context_packet_hidden_information_owner_scaffold.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
B01_REQUESTED_PATH = ROOT / "docs" / "doctrine" / "operations" / "batch_b" / "B01_scene_activity_orchestration_and_runtime_authority_procedure.md"
B09_REQUESTED_PATH = ROOT / "docs" / "doctrine" / "operations" / "batch_b" / "B09_social_faction_relationship_and_actor_knowledge_procedure.md"


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_pr_c_owner_scaffold_file_exists() -> None:
    assert RT005_PATH.exists()


def test_scaffold_references_remediation_priority_ledger_and_rt005() -> None:
    text = read(RT005_PATH)
    for phrase in [
        "REMEDIATION-PRIORITY-LEDGER-001",
        "RT-005",
        "RT-005-scene-activity-context-packets",
        "owner scaffold",
    ]:
        assert phrase in text


def test_scaffold_references_dependencies_and_audit_sources() -> None:
    text = read(RT005_PATH)
    for phrase in [
        "RT-001",
        "RT-002",
        "RT-003",
        "RT-011",
        "RT-007",
        "RT-009",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
    ]:
        assert phrase in text


def test_scaffold_references_source_pressures_and_absent_requested_files_honestly() -> None:
    text = read(RT005_PATH)
    for phrase in [
        "B01",
        "B09",
        "C06",
        "C07",
        "C09",
        "C10",
        "B01_scene_encounter_and_activity_procedure.md",
        "B09_social_faction_contact_and_institutional_interaction_procedure.md",
        "C06_location_site_region_record_schema.md",
        "C07_mission_scenario_adventure_record_schema.md",
        "C09_hazard_environment_record_schema.md",
        "C10_table_oracle_record_schema.md",
        "Roadmap backend-first/context-packet language",
        "SM00",
    ]:
        assert phrase in text

    if not B01_REQUESTED_PATH.exists():
        assert "B01_scene_activity_orchestration_and_runtime_authority_procedure.md` is absent" in text
    if not B09_REQUESTED_PATH.exists():
        assert "B09_social_faction_relationship_and_actor_knowledge_procedure.md` is absent" in text


def test_scaffold_includes_explicit_non_implementation_guardrails() -> None:
    text = read(RT005_PATH)
    for phrase in [
        "planning/control only",
        "Explicit non-implementation statement",
        "implements no",
        "no doctrine rewrite",
        "runtime implementation",
        "schema implementation",
        "command IR implementation",
        "math implementation",
        "validator implementation",
        "generator implementation",
        "persistence writer implementation",
        "retrieval index implementation",
        "context-packet compiler implementation",
        "narration validator implementation",
        "live-play prompt implementation",
        "canon promotion",
        "live-play/training authorization",
        "donor-content audit",
    ]:
        assert phrase in text


def test_context_packets_backend_produced_not_model_memory() -> None:
    text = read(RT005_PATH)
    for phrase in [
        "Context packets are backend-produced projections, not model memory",
        "Narration may only use allowed facts supplied by backend-owned context packets",
        "Narration must remain downstream of backend validation",
    ]:
        assert phrase in text


def test_scaffold_distinguishes_truth_knowledge_claims_transcripts_and_summaries() -> None:
    text = read(RT005_PATH)
    for phrase in [
        "Hidden facts, unverified rumors, false claims, NPC/faction beliefs, player-known facts, and backend truth must remain distinguishable",
        "Dialogue transcripts and summaries are not automatically authoritative truth",
        "Future dialogue-to-claim extraction must be backend/reviewer validated",
    ]:
        assert phrase in text


def test_scaffold_prohibits_llm_hidden_information_and_packet_authority() -> None:
    text = read(RT005_PATH)
    for phrase in [
        "deciding what hidden information exists",
        "revealing hidden state",
        "deciding what a player character knows",
        "deciding NPC/faction knowledge",
        "selecting clues or oracle/table outcomes",
        "inventing backend facts for narration",
        "treating narration as discovery",
        "treating summaries as memory authority",
        "mutating scene state",
        "compiling context packets",
        "bypassing redaction boundaries",
    ]:
        assert phrase in text


def test_scaffold_names_only_conceptual_placeholders() -> None:
    text = read(RT005_PATH)
    for phrase in [
        "scene_state_visible",
        "scene_state_hidden",
        "participant_visibility_partition",
        "location_fact_projection",
        "hazard_redaction_boundary",
        "mission_clue_visibility",
        "faction_or_actor_knowledge_partition",
        "oracle_result_redaction",
        "context_packet_prepared",
        "narration_allowed_fact_set",
        "narration_forbidden_inference_set",
        "conceptual placeholders only",
        "not final packet schema",
        "not context-packet compiler output",
        "not hidden-state database",
        "not retrieval index",
        "not narration validator",
        "not live-play prompt",
        "not runtime implementation",
    ]:
        assert phrase in text


def test_registry_tracks_pr_c_owner_scaffold() -> None:
    registry = read(REGISTRY_PATH)
    for phrase in [
        "REMEDIATION-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SCAFFOLD-001",
        "RT005_context_packet_hidden_information_owner_scaffold.md",
        "owner scaffold only",
        "no doctrine rewrite",
        "no runtime implementation",
        "no schema implementation",
        "no command IR implementation",
        "no math implementation",
        "no validator implementation",
        "no generator implementation",
        "no persistence writer implementation",
        "no retrieval index implementation",
        "no context-packet compiler implementation",
        "no narration validator implementation",
        "no live-play prompt implementation",
        "no canon promotion",
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in registry


def test_scaffold_and_registry_do_not_claim_to_implement_runtime_artifacts() -> None:
    forbidden_claims = [
        "implements packet schemas",
        "implements hidden-state database schemas",
        "implements runtime",
        "implements retrieval indexes",
        "implements validators",
        "implements generators",
        "implements persistence writers",
        "implements context-packet compilers",
        "implements narration validators",
        "implements live-play prompts",
        "implements training behavior",
        "packet schemas implemented",
        "hidden-state database schemas implemented",
        "runtime implemented",
        "retrieval indexes implemented",
        "validators implemented",
        "generators implemented",
        "persistence writers implemented",
        "context-packet compilers implemented",
        "narration validators implemented",
        "live-play prompts implemented",
        "training behavior implemented",
        "runtime-ready",
        "validator-ready",
        "generator-ready",
        "live-play ready",
    ]

    scaffold_text = read(RT005_PATH).lower()
    registry_text = read(REGISTRY_PATH)
    registry_entry = registry_text.rsplit(
        "REMEDIATION-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SCAFFOLD-001",
        1,
    )[1].lower()

    for text in [scaffold_text, registry_entry]:
        for phrase in forbidden_claims:
            assert phrase not in text
