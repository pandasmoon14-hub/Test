from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = ROOT / "docs" / "doctrine" / "reviews" / "runtime_boundary_generator_ownership_stage2_completion_review_and_closure_ledger.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-COMPLETION-REVIEW-CLOSURE-LEDGER-001"
STAGE2_CLOSURE_ID = "STAGE2-CLOSURE-REVIEW"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]
PLANNING_IDS = [
    "REMEDIATION-PRIORITY-LEDGER-001",
    "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001",
    "REMEDIATION-STAGE2-RT010-RT012-DEFERRED-CONVERGENCE-PLAN-001",
]
STAGE2_PR_IDS = [
    "STAGE2-PR-A",
    "STAGE2-PR-B",
    "STAGE2-PR-C",
    "STAGE2-PR-D",
    "STAGE2-PR-E",
    "STAGE2-PR-F",
    "STAGE2-PR-G1",
    "STAGE2-PR-G2",
    "STAGE2-PR-G3",
    "STAGE2-PR-G4",
    "STAGE2-PR-H",
]
RT_IDS = [f"RT-{i:03d}" for i in range(1, 13)]
OWNER_SPEC_COMPLETE = ["RT-001", "RT-002", "RT-003", "RT-004", "RT-005", "RT-006", "RT-007", "RT-008", "RT-009", "RT-011"]

GUARDRAIL_PHRASES = [
    "no runtime implementation",
    "no schema implementation",
    "no command IR implementation",
    "no validator implementation",
    "no generator implementation",
    "no inventory system",
    "no item system",
    "no vehicle system",
    "no asset system",
    "no D-series promotion system",
    "no native-design promotion system",
    "no canon promotion procedure",
    "no sourcebook inclusion procedure",
    "no training policy",
    "no RNG/dice/table implementation",
    "no event ledger implementation",
    "no database schema",
    "no persistence writer implementation",
    "no retrieval index implementation",
    "no context-packet compiler implementation",
    "no live-play prompt implementation",
    "no training authorization",
    "no donor-content audit",
    "no sourcebook inclusion authorization",
    "no pilot conversion authorization",
    "no canon promotion",
]

FORBIDDEN_TRUE_CLAIMS = [
    "creates_rt010_owner_specification: true",
    "creates_rt012_owner_specification: true",
    "authorizes_runtime_implementation: true",
    "authorizes_schema_implementation: true",
    "authorizes_validator_implementation: true",
    "authorizes_generator_implementation: true",
    "authorizes_command_ir: true",
    "authorizes_event_ledger: true",
    "authorizes_persistence_writer: true",
    "authorizes_context_packet_compiler: true",
    "authorizes_rng_implementation: true",
    "authorizes_live_play: true",
    "authorizes_training: true",
    "authorizes_pilot_conversion: true",
    "authorizes_sourcebook_inclusion: true",
    "authorizes_canon_promotion: true",
    "implementation_status: executable",
    "implementation_status: implemented",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_completion_review_file_exists_and_core_ids_are_present() -> None:
    text = read(REVIEW_PATH)
    for expected in [TRACKING_ID, STAGE2_CLOSURE_ID, "completion review and closure ledger"]:
        assert expected in text


def test_required_audit_planning_stage2_and_rt_ids_are_referenced() -> None:
    text = read(REVIEW_PATH)
    for expected in [*AUDIT_IDS, *PLANNING_IDS, *STAGE2_PR_IDS, *RT_IDS]:
        assert expected in text


def test_owner_specification_planning_completion_finding_is_explicit() -> None:
    text = read(REVIEW_PATH)
    assert "Stage 2 owner-specification planning is complete" in text
    for rt_id in OWNER_SPEC_COMPLETE:
        assert rt_id in text
    assert "RT-010 and RT-012 are not complete owner specifications" in text
    assert "deferred through the STAGE2-PR-H convergence plan" in text
    assert "owner_spec_required_later" in text
    assert "does not claim final runtime readiness" in text


def test_coverage_matrix_and_representative_statuses_exist() -> None:
    text = read(REVIEW_PATH)
    assert "## 4. Coverage matrix" in text
    for heading in [
        "Track ID",
        "Current artifact",
        "Current status",
        "Stage 2 PR ID",
        "Owner-spec status",
        "Implementation status",
        "Blocked claims",
        "Next recommended action",
    ]:
        assert heading in text
    for status in [
        "owner_spec_ready_non_executable",
        "deferred_convergence_plan_only",
        "owner_spec_required_later",
        "implementation_blocked",
        "schema_blocked",
        "runtime_blocked",
        "validation_blocked_until_implementation",
        "live_play_blocked",
        "training_blocked",
        "canon_promotion_blocked",
        "sourcebook_inclusion_blocked",
    ]:
        assert status in text


def test_guardrail_verification_and_llm_non_authority_are_present() -> None:
    text = read(REVIEW_PATH)
    assert "## 5. Guardrail verification" in text
    for phrase in [
        "did not authorize runtime implementation",
        "schema implementation",
        "command IR implementation",
        "validator implementation",
        "generator implementation",
        "persistence writer implementation",
        "retrieval index implementation",
        "context-packet compiler implementation",
        "RNG/dice/table implementation",
        "event ledger implementation",
        "database schema",
        "live-play prompt implementation",
        "training data",
        "donor-content audit",
        "sourcebook inclusion",
        "pilot conversion",
        "canon promotion",
        "LLM remains non-authoritative",
        "cannot mutate state",
        "cannot roll dice",
        "cannot commit events",
        "cannot own memory",
        "cannot reveal hidden information",
        "cannot create durable generated content",
        "cannot promote source packs",
    ]:
        assert phrase in text


def test_remaining_blocked_statuses_are_recorded() -> None:
    text = read(REVIEW_PATH)
    assert "## 6. Remaining blocked statuses after Stage 2" in text
    for phrase in [
        "RT-010 owner specification required later",
        "RT-012 owner specification required later",
        "runtime implementation blocked",
        "schema implementation blocked",
        "validator implementation blocked",
        "generator implementation blocked",
        "persistent state blocked",
        "persistence writers blocked",
        "context-packet compiler blocked",
        "event ledger blocked",
        "RNG/table implementation blocked",
        "live-play adapter blocked",
        "training blocked",
        "pilot conversion authorization blocked",
        "sourcebook inclusion blocked",
        "canon promotion blocked",
    ]:
        assert phrase in text


def test_recommended_next_sequence_puts_rt010_before_rt012() -> None:
    text = read(REVIEW_PATH)
    assert "## 7. Recommended next sequencing" in text
    rt010_pos = text.index("STAGE2-PR-H1")
    rt012_pos = text.index("STAGE2-PR-H2")
    assert rt010_pos < rt012_pos
    assert "RT-010 should come before RT-012" in text
    assert "runtime-adjacent" in text
    assert "promotion-boundary governance" in text


def test_non_implementation_reaffirmation_and_classification_block_exist() -> None:
    text = read(REVIEW_PATH)
    assert "## 8. Non-implementation reaffirmation" in text
    for phrase in GUARDRAIL_PHRASES:
        assert phrase.lower() in text.lower()
    assert "## 9. Stage 2 closure classification" in text
    assert "stage2_output:" in text
    assert "artifact_type: completion_review_and_closure_ledger" in text
    assert "implementation_status: non_executable_review" in text
    assert "creates_rt010_owner_specification: false" in text
    assert "creates_rt012_owner_specification: false" in text
    assert "next_allowed_step: RT-010 owner specification sequencing decision, pending review" in text


def test_registry_and_decision_log_tracking_exist() -> None:
    registry = read(REGISTRY_PATH)
    decision_log = read(DECISION_LOG_PATH)
    for text in [registry, decision_log]:
        assert TRACKING_ID in text
        assert "Stage 2 completion review" in text
        assert "no rt-010 owner specification" in text.lower()
        assert "no rt-012 owner specification" in text.lower()
        for phrase in GUARDRAIL_PHRASES:
            assert phrase.lower() in text.lower()


def test_closure_artifacts_do_not_claim_forbidden_authorization_or_implementation() -> None:
    combined = "\n".join(read(path) for path in [REVIEW_PATH, REGISTRY_PATH, DECISION_LOG_PATH])
    for forbidden in FORBIDDEN_TRUE_CLAIMS:
        assert forbidden not in combined
