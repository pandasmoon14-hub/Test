from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT009_runtime_rng_table_oracle_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT009-RNG-TABLE-ORACLE-OWNER-SPEC-001"
STAGE2_PR_ID = "STAGE2-PR-F"
TRACK = "RT-009"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

REQUIRED_SCAFFOLD_REF = "docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md"
RT001_SPEC_REF = "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md"
RT005_SPEC_REF = "docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md"
RT008_SPEC_REF = "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md"
RT011_SPEC_REF = "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md"

DEPENDENCY_STATES = [
    "rng_authority_required",
    "seed_reference_pending",
    "replay_reference_pending",
    "table_record_reference_required",
    "table_weight_validation_pending",
    "table_result_domain_pending",
    "oracle_invocation_candidate",
    "random_dependency_declared",
    "hidden_result_redaction_required",
    "visible_result_projection_pending",
    "random_result_commit_pending",
    "random_result_rejected",
    "random_result_quarantined",
    "narration_result_projection",
]

FUTURE_ARTIFACTS = [
    "RandomAuthorityRequirement",
    "RandomInvocationRequirement",
    "SeedReferenceRequirement",
    "ReplayReferenceRequirement",
    "TableRecordReferenceRequirement",
    "TableWeightValidationRequirement",
    "TableResultDomainRequirement",
    "OracleInvocationRequirement",
    "HiddenResultRedactionRequirement",
    "VisibleResultProjectionRequirement",
    "RandomResultCommitmentRequirement",
    "RandomResultRejectionRequirement",
    "RandomResultQuarantineRequirement",
    "RandomDependencyDisclosureRequirement",
    "RandomOutcomeValidationRequirement",
    "RandomAuditTrailRequirement",
]

GUARDRAILS = [
    "runtime code",
    "schema implementation",
    "command IR implementation",
    "validator implementation",
    "generator implementation",
    "RNG implementation",
    "dice roller",
    "table roller",
    "oracle engine",
    "table data",
    "table schema",
    "result-domain schema",
    "seed service",
    "replay verifier",
    "table-weight validator",
    "random-result event schema",
    "persistence writer",
    "retrieval index",
    "context-packet compiler",
    "redaction algorithm",
    "event ledger implementation",
    "database schema",
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


def test_references_stage2_plan_and_ledger() -> None:
    text = read(SPEC_PATH)
    assert STAGE2_PLAN_ID in text
    assert REMEDIATION_LEDGER_ID in text


def test_references_rt009_scaffold() -> None:
    text = read(SPEC_PATH)
    assert REQUIRED_SCAFFOLD_REF in text


def test_references_rt001_owner_specification() -> None:
    text = read(SPEC_PATH)
    assert RT001_SPEC_REF in text


def test_references_rt005_owner_specification() -> None:
    text = read(SPEC_PATH)
    assert RT005_SPEC_REF in text


def test_references_rt008_owner_specification() -> None:
    text = read(SPEC_PATH)
    assert RT008_SPEC_REF in text


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
        "backend-owned random authority boundary requirements",
        "RNG/table/oracle invocation ownership boundaries",
        "table/oracle record reference requirements",
        "seed reference and replay reference requirement boundaries",
        "result-domain validation requirements",
        "table-weight validation requirements",
        "hidden-result redaction handoff requirements",
        "random-result commitment boundaries",
        "oracle/table outcome narration projection requirements",
        "random dependency disclosure requirements",
        "## 3. Must-not-own boundaries",
    ]:
        assert phrase in text


def test_defines_authority_model() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "RT-001 owns command/event lifecycle",
        "RT-005 owns hidden-result visibility, redaction, and context/narration projection",
        "RT-008 owns generated-content provenance/recurrence implications",
        "RT-011 owns validation/readiness requirements",
        "backend runtime, once separately implemented, must own all random authority",
        "the LLM may describe backend-selected visible results only",
    ]:
        assert phrase in text


def test_dependency_contract_includes_planning_placeholders() -> None:
    text = read(SPEC_PATH)
    for state in DEPENDENCY_STATES:
        assert state in text


def test_dependency_contract_states_planning_only() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "not final schemas",
        "not database fields",
        "not RNG implementation",
        "not dice rolls",
        "not table data",
        "not oracle output",
        "not event records",
        "not replay verifier output",
        "not runtime state",
        "not live-play prompts",
    ]:
        assert phrase in text


def test_random_result_commitment_contract() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "random dependency declaration is not outcome selection",
        "table/oracle record reference is not table execution",
        "seed/replay reference requirement is not seed service implementation",
        "validation requirement is not validator implementation",
        "hidden result preparation is not player/model visibility",
        "random result commitment must be backend-owned",
        "narrated chance, model sampling, prose uncertainty, or LLM wording cannot serve as RNG authority",
    ]:
        assert phrase in text


def test_table_oracle_record_contract() -> None:
    text = read(SPEC_PATH)
    assert "table/oracle records are evidence/record structures, not executable RNG systems by themselves" in text
    for phrase in [
        "table weights, ranges, result domains, visibility status, source-local status, and provenance require validation before use",
        "donor table formats are not Astra runtime law",
        "table/oracle outputs that create generated content require RT-008",
        "hidden table/oracle results require RT-005",
        "validation/readiness routes through RT-011",
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
        "RNG authority boundary validation",
        "table/oracle record reference validation",
        "table weight/range/domain validation",
        "seed/replay requirement validation",
        "hidden-result redaction routing validation",
        "visible-result projection validation",
        "random-result commitment boundary validation",
        "generated-content random dependency validation",
        "mission/reward/clue random dependency validation",
        "hazard/combat random dependency validation",
        "loot/item/asset random dependency validation",
        "donor table format non-authority validation",
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
        "rolling dice",
        "choosing random results",
        "selecting table rows",
        "selecting oracle outcomes",
        "creating hidden random results",
        "revealing hidden random results",
        "setting table weights",
        "validating result domains",
        "inventing table rows as truth",
        "using model randomness as RNG authority",
        "treating narrated chance as backend randomness",
        "committing random-result events",
        "creating seed or replay references",
        "treating donor table formats as Astra runtime law",
        "generating loot/rewards/hazards/missions/items as committed outcomes",
        "bypassing RT-005 redaction",
        "bypassing RT-008 provenance for generated outcomes",
        "bypassing RT-011 validation",
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
        "stage2_pr_id: STAGE2-PR-F",
        "track: RT-009",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_generator_implementation: false",
        "authorizes_rng_implementation: false",
        "authorizes_dice_roller: false",
        "authorizes_table_roller: false",
        "authorizes_oracle_engine: false",
        "authorizes_seed_service: false",
        "authorizes_replay_verifier: false",
        "authorizes_event_ledger: false",
        "authorizes_context_packet_compiler: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_sourcebook_inclusion: false",
        "authorizes_canon_promotion: false",
        "authorizes_pilot_conversion: false",
        "next_allowed_step: downstream domain owner-spec bundle for RT-003, RT-004, RT-006, and RT-007, pending review",
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
            "implements runtime",
            "implements RNG",
            "implements dice roller",
            "implements table roller",
            "implements oracle engine",
            "implements seed service",
            "implements replay verifier",
            "creates table data",
            "creates table schema",
            "creates result-domain schema",
            "creates random-result event schema",
            "creates database schema",
            "creates live-play prompt",
            "creates training data",
            "authorizes canon promotion",
            "authorizes pilot conversion",
            "authorizes sourcebook inclusion",
        ]:
            assert claim not in text, f"Implementation claim '{claim}' found in {path.name}"
