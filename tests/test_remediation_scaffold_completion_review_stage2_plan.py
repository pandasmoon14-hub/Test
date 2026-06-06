from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md"
)
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
AUDIT_IDS = [
    "AUDIT-001",
    "AUDIT-WAVE1-001",
    "AUDIT-WAVE2-001",
    "REMEDIATION-PRIORITY-LEDGER-001",
]
RT_TRACKS = [f"RT-{index:03d}" for index in range(1, 13)]
RT_SCAFFOLD_FILES = [
    "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md",
    "docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md",
    "docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md",
    "docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md",
    "docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md",
    "docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md",
    "docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md",
    "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md",
    "docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md",
    "docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md",
    "docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md",
    "docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md",
]
ALLOWED_READINESS_CLASSIFICATIONS = {
    "ready_for_owner_spec",
    "needs_scaffold_cleanup_first",
    "blocked_pending_dependency",
    "defer_until_runtime_phase",
    "defer_until_canon_or_sourcebook_phase",
}
GUARDRAIL_PHRASES = [
    "no doctrine rewrite",
    "no runtime implementation",
    "no schema implementation",
    "no command IR implementation",
    "no validator implementation",
    "no generator implementation",
    "no persistence writer implementation",
    "no retrieval index implementation",
    "no context-packet compiler implementation",
    "no live-play prompt implementation",
    "no training authorization",
    "no canon promotion",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    start = text.index(heading)
    next_heading = text.find("\n## ", start + len(heading))
    if next_heading == -1:
        return text[start:]
    return text[start:next_heading]


def markdown_table_rows(section_text: str) -> list[list[str]]:
    rows = []
    for line in section_text.splitlines():
        if not line.startswith("| RT-"):
            continue
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def test_completion_review_file_exists_and_uses_correct_tracking_id() -> None:
    text = read(REVIEW_PATH)
    assert TRACKING_ID in text
    assert "AUDIT-SCAFFOLD-COMPLETION-STAGE2-PLAN-001" not in text


def test_review_references_audit_and_remediation_inputs() -> None:
    text = read(REVIEW_PATH)
    for audit_id in AUDIT_IDS:
        assert audit_id in text


def test_review_references_all_rt_scaffold_files() -> None:
    text = read(REVIEW_PATH)
    for scaffold_file in RT_SCAFFOLD_FILES:
        assert scaffold_file in text


def test_completion_matrix_covers_all_rt_tracks_with_completion_status() -> None:
    text = read(REVIEW_PATH)
    matrix = section(text, "## 3. Scaffold completion matrix")
    assert "completion_status" in matrix

    rows = markdown_table_rows(matrix)
    assert {row[0] for row in rows} == set(RT_TRACKS)

    allowed_statuses = {"complete", "incomplete", "needs_minor_cleanup", "blocked"}
    for row in rows:
        assert row[-2] in allowed_statuses, f"{row[0]} has invalid completion_status: {row[-2]}"


def test_stage2_readiness_classifications_cover_all_tracks_and_use_allowed_values() -> None:
    text = read(REVIEW_PATH)
    readiness = section(text, "## 6. Stage 2 readiness classifications")

    rows = markdown_table_rows(readiness)
    assert {row[0] for row in rows} == set(RT_TRACKS)

    found_classifications = {row[1] for row in rows}
    assert found_classifications <= ALLOWED_READINESS_CLASSIFICATIONS
    for row in rows:
        assert row[1] in ALLOWED_READINESS_CLASSIFICATIONS


def test_stage2_ledger_and_exactly_one_next_pr_recommendation_are_present() -> None:
    text = read(REVIEW_PATH)
    assert "## 7. Second-stage remediation planning ledger" in text
    assert "stage2_pr_id: STAGE2-PR-A" in text

    recommended_lines = [
        line for line in text.splitlines() if line.startswith("Recommended next PR:")
    ]
    assert len(recommended_lines) == 1
    assert "STAGE2-PR-A" in recommended_lines[0]


def test_recommended_next_pr_is_non_implementation() -> None:
    text = read(REVIEW_PATH)
    next_pr_section = section(text, "## 8. Exactly one recommended next PR")
    assert "must be limited to owner-specification planning" in next_pr_section
    assert "must not" in next_pr_section
    for phrase in [
        "runtime code",
        "schemas",
        "command IR implementation",
        "generators",
        "persistence",
        "retrieval",
        "context-packet compilation",
        "live-play prompts",
        "training data",
        "canon promotion",
    ]:
        assert phrase in next_pr_section


def test_registry_and_decision_log_track_review_with_guardrails() -> None:
    registry = read(REGISTRY_PATH)
    decision_log = read(DECISION_LOG_PATH)

    for text in [registry, decision_log]:
        assert TRACKING_ID in text
        assert "completion review" in text or "completion-review" in text
        assert "Stage 2 planning" in text
        assert "RT-001 through RT-012" in text
        assert "recommends exactly one next PR" in text
        for phrase in GUARDRAIL_PHRASES:
            assert phrase in text


def test_review_reaffirms_no_implementation_guardrails() -> None:
    text = read(REVIEW_PATH)
    guardrail_section = section(text, "## 9. Non-implementation reaffirmation")
    for phrase in GUARDRAIL_PHRASES:
        assert phrase in guardrail_section
    assert re.search(r"no donor-content audit", guardrail_section)
