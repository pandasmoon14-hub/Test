from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT011_validation_readiness_tooling_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT011-VALIDATION-READINESS-OWNER-SPEC-001"
STAGE2_PR_ID = "STAGE2-PR-B"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
RT011_SCAFFOLD_FILE = "docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md"
RT001_OWNER_SPEC_FILE = "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

READINESS_TERMS = [
    "prose_readiness",
    "owner_spec_readiness",
    "schema_readiness",
    "executable_validation",
    "runtime_readiness",
    "live_play_readiness",
]

READINESS_LABELS = [
    "doctrine_only",
    "scaffold_ready",
    "owner_spec_ready",
    "schema_required",
    "validator_required",
    "runtime_required",
    "generator_required",
    "context_packet_required",
    "persistence_required",
    "blocked_pending_dependency",
    "blocked_pending_review",
    "deferred_to_runtime_phase",
    "deferred_to_canon_or_sourcebook_phase",
    "implementation_authorized_separately_only",
]

CONCEPTUAL_LAYERS = [
    "artifact_presence_check",
    "registry_tracking_check",
    "decision_log_tracking_check",
    "audit_source_linkage_check",
    "owner_boundary_check",
    "non_implementation_guardrail_check",
    "llm_non_authority_check",
    "dependency_handoff_check",
    "readiness_classification_check",
    "future_required_output_inventory_check",
    "reviewer_decision_record_check",
    "blocked_status_routing_check",
    "implementation_authorization_check",
]

FUTURE_ARTIFACTS = [
    "ArtifactPresenceCheck",
    "RegistryTrackingCheck",
    "DecisionLogTrackingCheck",
    "AuditSourceLinkageCheck",
    "OwnerBoundaryCheck",
    "NonImplementationGuardrailCheck",
    "LLMNonAuthorityCheck",
    "DependencyHandoffCheck",
    "ReadinessClassificationCheck",
    "ReviewerDecisionRecord",
    "BlockedStatusRoutingRecord",
    "ImplementationAuthorizationRecord",
    "ValidationResultSummary",
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
    "no sourcebook inclusion authorization",
    "no pilot conversion authorization",
    "no canon promotion",
]

FORBIDDEN_TRUE_CLAIMS = [
    "authorizes_runtime_implementation: true",
    "authorizes_schema_implementation: true",
    "authorizes_validator_implementation: true",
    "authorizes_live_play: true",
    "authorizes_training: true",
    "authorizes_canon_promotion: true",
    "authorizes_pilot_conversion: true",
    "implementation_status: executable",
    "implementation_status: implemented",
    "authority_level: runtime",
    "authority_level: canon",
    "authority_level: live_play",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_owner_specification_file_exists_and_has_core_tracking() -> None:
    text = read(SPEC_PATH)
    for expected in [TRACKING_ID, STAGE2_PR_ID, "RT-011"]:
        assert expected in text


def test_owner_spec_references_required_stage2_audit_and_owner_sources() -> None:
    text = read(SPEC_PATH)
    for expected in [
        STAGE2_PLAN_ID,
        REMEDIATION_LEDGER_ID,
        RT011_SCAFFOLD_FILE,
        RT001_OWNER_SPEC_FILE,
        *AUDIT_IDS,
    ]:
        assert expected in text


def test_scope_and_must_not_own_boundaries_are_defined() -> None:
    text = read(SPEC_PATH)
    for heading in ["## 2. Scope", "## 3. Must-not-own boundaries"]:
        assert heading in text
    for phrase in [
        "validation/readiness ownership boundaries",
        "future validator requirement inventory",
        "registry tracking requirements",
        "file-presence and artifact-linkage check requirements",
        "non-implementation guardrail check requirements",
        "owner-boundary check requirements",
        "reviewer decision record requirements",
        "blocked and deferred status routing requirements",
        "dependency handoffs to RT-001 through RT-012",
        "executable validator implementation",
        "runtime code",
        "schema implementation",
        "automated reviewer replacement",
    ]:
        assert phrase in text


def test_prose_owner_schema_executable_runtime_and_live_play_readiness_are_separated() -> None:
    text = read(SPEC_PATH)
    assert "## 4. Prose readiness versus executable validation" in text
    for term in READINESS_TERMS:
        assert term in text
    assert "no prose file may claim executable validation by itself" in text


def test_readiness_classification_vocabulary_is_non_executable_planning_only() -> None:
    text = read(SPEC_PATH)
    assert "## 5. Readiness classification contract" in text
    for label in READINESS_LABELS:
        assert label in text
    assert "not executable gates" in text
    assert "not final schema statuses" in text


def test_conceptual_validation_layers_are_placeholder_only_and_not_automation() -> None:
    text = read(SPEC_PATH)
    assert "## 6. Conceptual validation layers" in text
    for phrase in [
        "placeholders only",
        "not executable validators",
        "not final test implementation",
        "not CI implementation",
        "not schema",
        "not runtime gates",
        "not approval automation",
    ]:
        assert phrase in text
    for layer in CONCEPTUAL_LAYERS:
        assert layer in text
    assert text.count("future_required_not_implemented") >= len(CONCEPTUAL_LAYERS)


def test_reviewer_decision_record_requirements_are_present() -> None:
    text = read(SPEC_PATH)
    assert "## 7. Reviewer decision record contract" in text
    for phrase in [
        "reviewer decision records must be explicit",
        "model confidence",
        "cannot replace reviewer approval",
        "skipped dependencies must be recorded",
        "dependency-related skips must be distinguished from pass/fail",
        "missing-file substitutions must be disclosed",
        "guardrail deviations must block advancement",
        "implementation authorization must require a separate decision",
        "canon authorization must require a separate decision",
        "sourcebook inclusion authorization must require a separate decision",
        "training authorization must require a separate decision",
        "live-play authorization must require a separate decision",
    ]:
        assert phrase in text


def test_validation_handoffs_cover_rt001_through_rt010_and_rt012() -> None:
    text = read(SPEC_PATH)
    assert "## 8. Validation and readiness handoffs" in text
    for index in list(range(1, 11)) + [12]:
        assert f"RT-{index:03d}:" in text
    assert "Unresolved handoffs must be labeled" in text


def test_llm_non_authority_prohibitions_are_explicit() -> None:
    text = read(SPEC_PATH)
    assert "## 9. LLM non-authority rules" in text
    for phrase in [
        "declaring a file executable-ready",
        "declaring runtime readiness",
        "declaring schema readiness",
        "declaring validator readiness",
        "approving pilot conversion outputs",
        "authorizing live play",
        "authorizing training data",
        "authorizing canon promotion",
        "authorizing sourcebook inclusion",
        "replacing reviewer decisions",
        "treating prose as executable validation",
        "treating tests as passed without actual execution and reporting",
        "hiding dependency-related skips",
        "inventing missing registry tracking",
        "inventing missing decision-log tracking",
        "bypassing backend/reviewer validation",
    ]:
        assert phrase in text


def test_future_validation_artifacts_are_inventoried_as_not_implemented() -> None:
    text = read(SPEC_PATH)
    assert "## 10. Future validation artifact inventory" in text
    assert "semantic requirements only" in text
    assert "not implemented validators" in text
    assert "not JSON schema" in text
    assert "not database schema" in text
    assert "not CI jobs" in text
    assert "not validator code" in text
    for artifact in FUTURE_ARTIFACTS:
        assert artifact in text
    assert text.count("future_required_not_implemented") >= len(CONCEPTUAL_LAYERS) + len(FUTURE_ARTIFACTS)


def test_non_implementation_reaffirmation_and_stage2_classification_are_present() -> None:
    text = read(SPEC_PATH)
    assert "## 13. Non-implementation reaffirmation" in text
    for phrase in GUARDRAIL_PHRASES:
        assert phrase in text
    assert "## 14. Stage 2 output classification" in text
    for phrase in [
        "stage2_output:",
        "stage2_pr_id: STAGE2-PR-B",
        "track: RT-011",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_canon_promotion: false",
        "authorizes_pilot_conversion: false",
    ]:
        assert phrase in text


def test_registry_and_decision_log_track_stage2_rt011_owner_spec() -> None:
    registry = read(REGISTRY_PATH)
    decision_log = read(DECISION_LOG_PATH)
    for text in [registry, decision_log]:
        assert TRACKING_ID in text
        assert SPEC_PATH.relative_to(ROOT).as_posix() in text
        assert STAGE2_PR_ID in text
    for phrase in GUARDRAIL_PHRASES:
        assert phrase in registry
        assert phrase in decision_log


def test_stage2_rt011_files_do_not_claim_forbidden_implementation_authority() -> None:
    combined = "\n".join([read(SPEC_PATH), read(REGISTRY_PATH), read(DECISION_LOG_PATH)]).lower()
    combined_lines = {line.strip() for line in combined.splitlines()}
    for claim in FORBIDDEN_TRUE_CLAIMS:
        if claim.startswith("authority_level:"):
            assert claim not in combined_lines
        else:
            assert claim not in combined
    for phrase in GUARDRAIL_PHRASES:
        assert phrase.lower() in combined
