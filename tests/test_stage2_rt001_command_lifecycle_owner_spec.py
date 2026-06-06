from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT001_command_lifecycle_action_legality_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT001-COMMAND-LIFECYCLE-OWNER-SPEC-001"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
RT001_SCAFFOLD_FILE = "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]
LIFECYCLE_TERMS = [
    "raw_input_received",
    "intent_parse_proposed",
    "clarification_required",
    "candidate_command_prepared",
    "cost_commitment_pending",
    "costs_committed",
    "resolution_trigger_selected",
    "state_delta_validation_required",
    "event_commit_required",
    "context_packet_update_required",
    "command_rejected",
    "command_quarantined_pending_doctrine_or_runtime",
]
FUTURE_IR_FAMILIES = [
    "RawInputRecord",
    "IntentProposal",
    "ClarificationRequest",
    "CandidateCommand",
    "ActorAuthorityCheck",
    "TargetLegalityCheck",
    "CapabilityAccessCheck",
    "CostCommitmentRecord",
    "ResolutionTriggerRecord",
    "RandomnessDependencyRecord",
    "ProposedStateDelta",
    "ValidationResult",
    "EventCommitReference",
    "RejectionRecord",
    "QuarantineRecord",
    "NarrationPacketReference",
]
GUARDRAIL_PHRASES = [
    "no runtime implementation",
    "no schema implementation",
    "no command IR implementation",
    "no validator implementation",
    "no generator implementation",
    "no persistence writer implementation",
    "no retrieval index implementation",
    "no context-packet compiler implementation",
    "no RNG/dice/table implementation",
    "no event ledger implementation",
    "no database schema",
    "no live-play prompt implementation",
    "no training authorization",
    "no donor-content audit",
    "no canon promotion",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_owner_specification_file_exists_and_has_core_tracking() -> None:
    text = read(SPEC_PATH)
    for expected in [TRACKING_ID, "STAGE2-PR-A", "RT-001"]:
        assert expected in text


def test_owner_spec_references_required_planning_audit_and_scaffold_sources() -> None:
    text = read(SPEC_PATH)
    for expected in [STAGE2_PLAN_ID, REMEDIATION_LEDGER_ID, RT001_SCAFFOLD_FILE, *AUDIT_IDS]:
        assert expected in text


def test_scope_and_must_not_own_boundaries_are_defined() -> None:
    text = read(SPEC_PATH)
    assert "## 3. Scope: what RT-001 owns" in text
    assert "## 4. Must-not-own boundaries" in text
    for phrase in [
        "player intent intake boundary",
        "raw input capture boundary",
        "backend action-legality decision boundary",
        "cost-declaration timing",
        "cost-commitment timing",
        "event-commit handoff",
        "command rejection and quarantine handoff",
        "auditability requirements",
        "final resource formulas",
        "final RNG implementation",
        "final hidden-information redaction algorithm",
    ]:
        assert phrase in text


def test_conceptual_lifecycle_contract_is_placeholder_non_runtime_only() -> None:
    text = read(SPEC_PATH)
    assert "## 6. Conceptual lifecycle contract" in text
    for phrase in [
        "conceptual placeholders only",
        "not final IR",
        "not a final runtime state machine",
        "not executable code",
        "not schema",
        "not runtime code",
    ]:
        assert phrase in text
    for term in LIFECYCLE_TERMS:
        assert term in text


def test_cost_commitment_action_legality_and_command_event_contracts_exist() -> None:
    text = read(SPEC_PATH)
    for heading in [
        "## 7. Cost commitment contract",
        "## 8. Action legality contract",
        "## 9. Command/event boundary",
    ]:
        assert heading in text
    for phrase in [
        "costs must be declared before commitment when knowable",
        "optional overcommitment must be backend-authorized",
        "failed commands require explicit cost outcome handling",
        "RT-002 owns cost math",
        "action legality must be backend-owned",
        "target legality must be backend-owned",
        "the LLM may not",
        "command proposal is not event commitment",
        "validation is not commitment",
        "narration is not commitment",
        "rejected commands must not mutate state",
        "quarantined commands must not mutate state",
    ]:
        assert phrase in text


def test_future_ir_inventory_is_semantic_only_and_not_implemented() -> None:
    text = read(SPEC_PATH)
    assert "## 10. Future IR inventory: semantic requirements only" in text
    assert "semantic requirements only" in text
    assert "not implemented schemas" in text
    assert "not final CommandIR" in text
    for family in FUTURE_IR_FAMILIES:
        assert family in text
    assert text.count("future_required_not_implemented") >= len(FUTURE_IR_FAMILIES)


def test_validation_requirements_and_downstream_handoffs_cover_rt002_through_rt012() -> None:
    text = read(SPEC_PATH)
    assert "## 11. Validation and readiness requirements" in text
    assert "## 12. Downstream handoffs" in text
    for phrase in [
        "file/registry tracking validation",
        "lifecycle-state coverage validation",
        "LLM non-authority validation",
        "cost-commitment boundary validation",
        "command/event boundary validation",
        "downstream dependency validation",
        "non-implementation guardrail validation",
    ]:
        assert phrase in text
    for index in range(2, 13):
        assert f"RT-{index:03d}" in text


def test_llm_non_authority_and_non_implementation_reaffirmation_are_explicit() -> None:
    text = read(SPEC_PATH)
    assert "## 13. LLM non-authority rules" in text
    assert "## 14. Non-implementation reaffirmation" in text
    for phrase in [
        "deciding action legality",
        "deciding target legality",
        "deciding hidden modifiers",
        "spending or refunding resources",
        "committing costs",
        "committing events",
        "writing persistence records",
        "compiling context packets",
        "revealing hidden information",
        "treating narration as backend commitment",
        "treating summaries as memory authority",
        "authorizing canon, sourcebook, donor-content, or training use",
    ]:
        assert phrase in text
    for phrase in GUARDRAIL_PHRASES:
        assert phrase in text


def test_stage2_output_classification_block_is_present() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "stage2_output:",
        "stage2_pr_id: STAGE2-PR-A",
        "track: RT-001",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_canon_promotion: false",
        "next_allowed_step: RT-011 owner specification or RT-002 owner specification, pending review",
    ]:
        assert phrase in text


def test_registry_and_decision_log_track_stage2_owner_spec_with_guardrails() -> None:
    registry = read(REGISTRY_PATH)
    decision_log = read(DECISION_LOG_PATH)
    for text in [registry, decision_log]:
        assert TRACKING_ID in text
        assert "Stage 2 owner" in text or "Stage 2 owner-specification" in text
        for phrase in GUARDRAIL_PHRASES:
            assert phrase in text


def test_stage2_owner_spec_does_not_claim_forbidden_implementation_authority() -> None:
    combined = "\n".join([read(SPEC_PATH), read(REGISTRY_PATH), read(DECISION_LOG_PATH)]).lower()
    combined_lines = {line.strip() for line in combined.splitlines()}
    forbidden_claims = [
        "authorizes_runtime_implementation: true",
        "authorizes_schema_implementation: true",
        "authorizes_live_play: true",
        "authorizes_training: true",
        "authorizes_canon_promotion: true",
        "implementation_status: executable",
        "implementation_status: implemented",
        "authority_level: runtime",
        "authority_level: canon",
        "authority_level: live_play",
    ]
    for claim in forbidden_claims:
        if claim.startswith("authority_level:"):
            assert claim not in combined_lines
        else:
            assert claim not in combined
