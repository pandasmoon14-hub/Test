from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT005_context_packet_hidden_information_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SPEC-001"
STAGE2_PR_ID = "STAGE2-PR-D"
TRACK = "RT-005"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
RT005_SCAFFOLD_FILE = "docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md"
RT001_OWNER_SPEC_FILE = "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md"
RT002_OWNER_SPEC_FILE = "docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md"
RT011_OWNER_SPEC_FILE = "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

REPRESENTATIVE_PARTITION_TERMS = [
    "backend_truth_partition",
    "player_known_fact_partition",
    "character_known_fact_partition",
    "npc_known_fact_partition",
    "faction_known_fact_partition",
    "rumor_or_unverified_claim_partition",
    "false_claim_partition",
    "hidden_truth_partition",
    "secret_agenda_partition",
    "hidden_hazard_partition",
    "hidden_random_result_partition",
    "redacted_fact_partition",
    "derived_inference_partition",
    "narrator_allowed_fact_set",
    "narrator_forbidden_inference_set",
    "reviewer_only_partition",
    "dialogue_transcript_candidate",
    "summary_not_memory_authority",
    "durable_claim_pending_review",
]

REPRESENTATIVE_FUTURE_ARTIFACTS = [
    "ContextPacketRequirement",
    "VisibleFactRequirement",
    "HiddenFactRequirement",
    "RedactedFactRequirement",
    "PlayerKnownFactRequirement",
    "CharacterKnownFactRequirement",
    "ActorKnowledgeRequirement",
    "FactionKnowledgeRequirement",
    "RumorClaimRequirement",
    "FalseClaimRequirement",
    "DialogueTranscriptRequirement",
    "SummaryBoundaryRequirement",
    "DurableClaimReviewRequirement",
    "NarrationAllowedFactSetRequirement",
    "NarrationForbiddenInferenceRequirement",
    "HiddenTruthRevealRequirement",
    "ClueVisibilityRequirement",
    "HiddenRandomResultRedactionRequirement",
    "SourceProvenanceProjectionRequirement",
    "ContextPacketValidationRequirement",
]

REPRESENTATIVE_LLM_PROHIBITIONS = [
    "deciding what hidden information exists",
    "revealing hidden state",
    "deciding what a player, character, NPC, or faction knows",
    "deciding NPC/faction beliefs as truth",
    "selecting or revealing clues",
    "selecting or revealing hidden truths",
    "selecting oracle/table outcomes",
    "inventing backend facts for narration",
    "treating narration as discovery",
    "treating summaries as memory authority",
    "treating dialogue as durable truth",
    "mutating scene state",
    "compiling context packets",
    "choosing redaction boundaries",
    "bypassing redaction",
    "inferring hidden information from absence or pattern",
    "overriding backend validators",
    "authorizing canon/sourcebook/training/live-play use",
]

GUARDRAIL_PHRASES = [
    "runtime code",
    "schema implementation",
    "command IR implementation",
    "validator implementation",
    "generator implementation",
    "persistence writer",
    "retrieval index",
    "context-packet compiler",
    "redaction algorithm",
    "narration validator",
    "hidden-state database",
    "actor-knowledge database",
    "memory system",
    "RNG/dice/table implementation",
    "event ledger implementation",
    "database schema",
    "live-play prompt",
    "training data",
    "donor-content audit",
    "pilot conversion authorization",
    "sourcebook inclusion authorization",
    "canon promotion",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "authorizes_runtime_implementation: true",
    "authorizes_schema_implementation: true",
    "authorizes_validator_implementation: true",
    "authorizes_context_packet_compiler: true",
    "authorizes_redaction_algorithm: true",
    "authorizes_retrieval_index: true",
    "authorizes_memory_system: true",
    "authorizes_live_play: true",
    "authorizes_training: true",
    "authorizes_canon_promotion: true",
    "authorizes_pilot_conversion: true",
    "implementation_status: executable",
    "implementation_status: implemented",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_owner_specification_file_exists_and_has_core_tracking() -> None:
    text = read(SPEC_PATH)
    for expected in [TRACKING_ID, STAGE2_PR_ID, TRACK]:
        assert expected in text


def test_owner_spec_references_required_stage2_audit_and_owner_sources() -> None:
    text = read(SPEC_PATH)
    for expected in [
        STAGE2_PLAN_ID,
        REMEDIATION_LEDGER_ID,
        RT005_SCAFFOLD_FILE,
        RT001_OWNER_SPEC_FILE,
        RT002_OWNER_SPEC_FILE,
        RT011_OWNER_SPEC_FILE,
        *AUDIT_IDS,
    ]:
        assert expected in text


def test_scope_and_must_not_own_boundaries_are_defined() -> None:
    text = read(SPEC_PATH)
    for heading in ["## 2. Scope", "## 3. Must-not-own boundaries"]:
        assert heading in text
    for phrase in [
        "hidden-information ownership boundaries",
        "context-packet projection boundary requirements",
        "visible/hidden/redacted/derived/reviewer-only information partition requirements",
        "player-known fact requirements",
        "NPC/faction-known belief and knowledge requirements",
        "dialogue transcript versus summary versus durable claim boundary requirements",
        "narrator-facing allowed fact-set requirements",
        "narrator-facing forbidden inference-set requirements",
        "clue visibility and hidden-truth exposure boundary requirements",
        "validation/readiness handoff to RT-011",
        "final context-packet schema",
        "final actor-knowledge schema",
        "final rumor/claim schema",
        "final memory system",
    ]:
        assert phrase in text


def test_authority_model_is_defined() -> None:
    text = read(SPEC_PATH)
    assert "## 4. Authority model" in text
    for phrase in [
        "RT-001 owns command/event lifecycle and when context/narration handoffs occur",
        "RT-002 owns resource/consequence math, while RT-005 owns whether cost/consequence information is visible, redacted, hidden, or narrator-projected",
        "RT-011 owns validation/readiness requirements",
        "Future backend owners own all hidden truth, visibility partitioning, packet production, redaction, retrieval eligibility, reveal authorization, durable memory authority, and persistence authority",
        "The LLM may only narrate from backend-approved allowed fact sets",
        "LLM memory, summaries, and fluent narration are not state, truth, discovery, or persistence",
    ]:
        assert phrase in text


def test_information_partition_contract_is_placeholder_only() -> None:
    text = read(SPEC_PATH)
    assert "## 5. Information partition contract" in text
    for term in REPRESENTATIVE_PARTITION_TERMS:
        assert term in text
    for phrase in [
        "planning placeholders only",
        "not final schemas",
        "not database fields",
        "not retrieval index records",
        "not context-packet compiler output",
        "not redaction algorithms",
        "not memory implementation",
        "not runtime state",
        "not live-play prompts",
    ]:
        assert phrase in text


def test_context_packet_handoff_contract_is_defined() -> None:
    text = read(SPEC_PATH)
    assert "## 6. Context-packet handoff contract" in text
    for phrase in [
        "Context packets are backend-produced projections, not model memory",
        "Allowed fact sets must be distinguishable from hidden backend truth",
        "bounded by scene, actor, visibility, authority, and redaction status",
        "Missing context should trigger clarification or backend lookup, not invention",
        "Packet outputs must preserve source/provenance references where required by RT-008",
        "Packet outputs involving RNG/table/oracle results must route through RT-009",
        "Packet outputs involving command lifecycle or event commitment must route through RT-001",
        "Durable context/memory writes require future persistence ownership and reviewer/backend validation",
    ]:
        assert phrase in text


def test_hidden_information_and_claim_contract_is_defined() -> None:
    text = read(SPEC_PATH)
    assert "## 7. Hidden-information and claim contract" in text
    for phrase in [
        "Backend truth, player-known facts, character-known facts, NPC/faction beliefs, rumors, false claims, dialogue transcripts, summaries, and generated prose must remain distinguishable",
        "Dialogue may produce a claim candidate only, not authoritative truth",
        "Summaries are not memory authority",
        "Clues and hidden truths require backend-owned reveal/visibility authorization",
        "False or unverified information must not be auto-corrected by the model unless the backend provides correction authority",
        "Hidden NPC/faction agendas must remain redacted unless backend context authorizes projection",
        "Hidden random results require RT-009",
        "Generated recurring facts require RT-008",
        "Social/faction belief state requires RT-007",
        "Validation/readiness routes through RT-011",
    ]:
        assert phrase in text


def test_future_context_visibility_artifact_inventory_is_future_only() -> None:
    text = read(SPEC_PATH)
    assert "## 8. Future context/visibility artifact inventory" in text
    for artifact in REPRESENTATIVE_FUTURE_ARTIFACTS:
        assert artifact in text
    assert text.count("future_required_not_implemented") >= len(REPRESENTATIVE_FUTURE_ARTIFACTS)
    for phrase in [
        "semantic requirements only, not implemented schemas or compilers",
        "not implemented schemas or compilers",
        "not final fields",
        "not runtime code",
    ]:
        assert phrase in text


def test_validation_readiness_requirements_are_future_only() -> None:
    text = read(SPEC_PATH)
    assert "## 9. Validation and readiness requirements" in text
    for phrase in [
        "source linkage validation",
        "context/source availability validation",
        "visibility partition coverage validation",
        "hidden/visible/redacted partition validation",
        "narrator allowed/forbidden fact-set validation",
        "claim/rumor/false-claim separation validation",
        "dialogue-summary non-authority validation",
        "clue/hidden-truth reveal boundary validation",
        "hidden random result routing validation",
        "generated-content provenance handoff validation",
        "LLM non-authority validation",
        "non-implementation guardrail validation",
        "does not implement validators",
    ]:
        assert phrase in text


def test_downstream_handoffs_cover_rt001_through_rt012() -> None:
    text = read(SPEC_PATH)
    assert "## 10. Downstream handoffs" in text
    for rt in [f"RT-{index:03d}" for index in range(1, 13)]:
        assert rt in text
    for phrase in [
        "RT-001: command lifecycle, event commitment, rejection/quarantine",
        "RT-002: hidden or visible resource, cost, consequence, reward, loss, recovery",
        "RT-003: hidden/visible combat, hazard, damage, injury, recovery, exposure",
        "RT-004: visible/hidden ability, effect, skill, capability",
        "RT-006: mission clues, hidden truths, objectives, branches",
        "RT-007: actor knowledge, relationship state, NPC/faction beliefs",
        "RT-008: generated-content provenance, recurrence, durable generated facts",
        "RT-009: hidden random results, table/oracle outcomes",
        "RT-010: inventory/item/vehicle/asset visibility",
        "RT-011: validation/readiness governance",
        "RT-012: D-series/native-design material",
    ]:
        assert phrase in text


def test_llm_non_authority_prohibitions_are_explicit() -> None:
    text = read(SPEC_PATH)
    assert "## 11. LLM non-authority rules" in text
    for phrase in REPRESENTATIVE_LLM_PROHIBITIONS:
        assert phrase in text


def test_non_implementation_reaffirmation_and_stage2_classification_are_present() -> None:
    text = read(SPEC_PATH)
    assert "## 12. Non-implementation reaffirmation" in text
    assert "## 13. Stage 2 output classification" in text
    for phrase in GUARDRAIL_PHRASES:
        assert phrase in text
    for phrase in [
        "stage2_output:",
        "stage2_pr_id: STAGE2-PR-D",
        "track: RT-005",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_context_packet_compiler: false",
        "authorizes_redaction_algorithm: false",
        "authorizes_retrieval_index: false",
        "authorizes_memory_system: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_canon_promotion: false",
        "authorizes_pilot_conversion: false",
        "next_allowed_step: RT-008 owner specification or RT-009 owner specification, pending review",
    ]:
        assert phrase in text


def test_registry_and_decision_log_tracking_exists() -> None:
    registry_text = read(REGISTRY_PATH)
    decision_text = read(DECISION_LOG_PATH)
    for text in [registry_text, decision_text]:
        assert TRACKING_ID in text
        assert "Stage 2 owner" in text or "Stage 2 owner-specification" in text
        for phrase in [
            "no runtime implementation",
            "no schema implementation",
            "no command IR implementation",
            "no validator implementation",
            "no generator implementation",
            "no persistence writer implementation",
            "no retrieval index implementation",
            "no context-packet compiler implementation",
            "no redaction algorithm implementation",
            "no narration validator implementation",
            "no hidden-state database",
            "no actor-knowledge database",
            "no memory system",
            "no RNG/dice/table implementation",
            "no event ledger implementation",
            "no database schema",
            "no live-play prompt implementation",
            "no training authorization",
            "no donor-content audit",
            "no canon promotion",
            "no sourcebook inclusion authorization",
            "no pilot conversion authorization",
        ]:
            assert phrase in text


def test_no_positive_implementation_authorization_claims() -> None:
    combined = "\n".join(read(path) for path in [SPEC_PATH, REGISTRY_PATH, DECISION_LOG_PATH])
    for forbidden in FORBIDDEN_POSITIVE_CLAIMS:
        assert forbidden not in combined
