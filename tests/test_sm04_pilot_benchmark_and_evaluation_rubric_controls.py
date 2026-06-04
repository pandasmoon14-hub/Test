import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM04_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM04_pilot_benchmark_and_evaluation_rubric_controls.md"
)

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing benchmark/evaluation posture",
    "What SM04 owns",
    "What SM04 must not own",
    "Pilot benchmark/evaluation definition",
    "Evaluable pilot evidence requirements",
    "Evaluation subject boundaries",
    "Rubric interpretation labels",
    "Core evaluation dimensions",
    "Evidence and provenance evaluation",
    "Lawful outcome completeness evaluation",
    "C00-C14 and `pending_schema` routing evaluation",
    "Rejected-import, source-local, and legal/IP containment evaluation",
    "Donor leakage evaluation",
    "Confidence, review-routing, and human-review evaluation",
    "Repair, quarantine, and failure-report evaluation",
    "Failure-class inventory",
    "Benchmark/evaluation question design",
    "Reviewer workflow and decision record",
    "Pilot result interpretation",
    "What pilot evaluation may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM04",
    "Acceptance criteria",
]

EVALUABLE_PILOT_EVIDENCE_TERMS = [
    "packet identity",
    "donor source identity",
    "donor-family classification",
    "extraction run identity",
    "page/range truth",
    "source hash or hash-later policy",
    "evidence references",
    "construct inventory",
    "lawful outcome ledger",
    "mapping ledger",
    "rejected-import ledger",
    "source-local retention ledger",
    "pending_schema ledger",
    "repair queue status",
    "quarantine queue status",
    "confidence/review-routing notes",
    "legal/IP flags",
    "reviewer decision points",
    "C-family routing targets",
    "pilot output review status",
    "failure report shape",
    "benchmark/evaluation prerequisites",
]

RUBRIC_LABELS = [
    "pass_for_pilot_evidence",
    "pass_with_review_notes",
    "blocked_by_missing_evidence",
    "blocked_by_lawful_outcome_gap",
    "blocked_by_routing_gap",
    "blocked_by_legal_ip_risk",
    "blocked_by_donor_leakage",
    "blocked_by_runtime_or_mechanics_creep",
    "quarantine_required",
    "repair_required",
    "human_review_required",
    "not_evaluable",
]

CORE_EVALUATION_DIMENSIONS = [
    "Packet identity and scope discipline",
    "Evidence/provenance completeness",
    "Construct inventory completeness",
    "Lawful outcome completeness",
    "Mapping ledger clarity",
    "pending_schema",
    "Rejected-import containment",
    "Source-local containment",
    "Legal/IP risk containment",
    "Donor math/statblock/economy/class/dice/cosmology leakage prevention",
    "Confidence/review-routing completeness",
    "Repair/quarantine/failure-report completeness",
    "Benchmark/evaluation question answerability",
    "Non-readiness boundary discipline",
    "Reviewer reproducibility",
]

FAILURE_CLASSES = [
    "missing packet identity",
    "missing donor source identity",
    "missing donor-family classification",
    "missing extraction run identity",
    "missing page/range truth",
    "missing source hash or hash-later policy",
    "missing evidence references",
    "incomplete construct inventory",
    "missing lawful outcome",
    "contradictory lawful outcomes",
    "missing mapping ledger entry",
    "rejected-import leakage",
    "source-local leakage",
    "legal/IP unresolved risk",
    "C-family routing gap",
    "pending_schema` misuse",
    "field invention",
    "donor math leakage",
    "donor statblock leakage",
    "donor economy leakage",
    "donor class/progression leakage",
    "donor dice-system leakage",
    "donor cosmology leakage",
    "D-series authority leakage",
    "RHBF hidden law",
    "final mechanics creep",
    "runtime schema creep",
    "canon/sourcebook/live-play/training creep",
    "missing confidence/review-routing notes",
    "missing repair/quarantine path",
    "missing failure report",
    "overclaiming pilot success",
]

REVIEWER_WORKFLOW_STEPS = [
    "Confirm pilot output is eligible for evaluation",
    "Confirm packet identity and scope",
    "Confirm evidence/provenance completeness",
    "Confirm construct inventory completeness",
    "Evaluate lawful outcome accounting",
    "Evaluate mapping ledger clarity",
    "Evaluate C00-C14 and `pending_schema` routing",
    "Evaluate rejected-import/source-local/legal/IP containment",
    "Evaluate donor leakage",
    "Evaluate confidence/review-routing notes",
    "Evaluate repair/quarantine/failure-report completeness",
    "Assign document-local rubric labels",
    "Record reviewer decision and rationale",
    "Route failures to repair, quarantine, deferred gap ledger",
    "State exactly what the pilot result may and may not prove",
]

FORBIDDEN_C_PROMOTION_VALUES = {
    "current",
    "pressure-tested",
    "stable_for_family",
    "stable_cross_family",
    "tested_minimum",
    "accepted_canon",
    "runtime_ready",
    "runtime-ready",
    "canon-ready",
    "schema-current",
    "schema_current",
    "runtime-current",
    "training-current",
}


def sm04_text() -> str:
    return read_utf8(SM04_PATH)


def _registry_record_block(file_id: str) -> str:
    text = read_utf8(REGISTRY_PATH)
    match = re.search(
        rf"^- file_id: {re.escape(file_id)}\n(?P<block>.*?)(?=^- file_id: |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing registry record for {file_id}"
    return match.group(0)


def _scalar_from_block(block: str, key: str) -> str | None:
    match = re.search(
        rf"^\s*{re.escape(key)}:\s*['\"]?(?P<value>[^'\"\n#]+)",
        block,
        flags=re.MULTILINE,
    )
    return match.group("value").strip() if match else None


# --- Existence and structure ---


def test_sm04_file_exists_and_is_nonempty() -> None:
    assert SM04_PATH.exists()
    assert SM04_PATH.is_file()
    assert sm04_text().strip()


def test_required_section_headings_are_present() -> None:
    text = sm04_text()
    for section in REQUIRED_SECTIONS:
        assert section in text, f"Missing section: {section}"


# --- Identity and purpose ---


def test_sm04_states_pilot_benchmark_and_evaluation_rubric_control_only() -> None:
    text = sm04_text()
    assert (
        "SM04 is a pilot benchmark and evaluation rubric control file only" in text
    )


def test_sm04_states_no_conversion_or_converted_content() -> None:
    text = sm04_text()
    assert "SM04 does not run conversion" in text
    assert "does not create converted donor content" in text


def test_sm04_refuses_all_non_goals() -> None:
    text = sm04_text()
    for marker in [
        "create benchmark corpora",
        "create evaluation corpora",
        "create training data",
        "create fine-tuning data",
        "create model behavior policy",
        "embed real copyrighted donor excerpts",
        "embed donor statblocks",
        "embed donor tables",
        "embed donor maps",
        "embed donor setting prose",
        "import donor proper nouns as Astra defaults",
        "create final output schemas",
        "create JSON Schema files",
        "create Pydantic models",
        "create final validators",
        "create runtime schemas",
        "create backend schemas",
        "create database schemas",
        "create entity/component/event schemas",
        "command lifecycle contracts",
        "context packet contracts",
        "save-state shapes",
        "create final mechanics",
        "create exact math",
        "create resolution dice",
        "create damage formulas",
        "create resource formulas",
        "create progression math",
        "donor-statblock validators that treat donor statblocks as Astra defaults",
        "promote C00-C14 registry statuses",
        "rewrite C00-C14",
        "add C15",
        "promote canon",
        "write sourcebook prose",
        "create live-play behavior",
        "create training/evaluation corpora",
        "treat D00-D19 as authority",
        "use RHBF as hidden law",
    ]:
        assert marker in text, f"Missing non-goal: {marker}"


# --- Upstream references ---


def test_sm04_names_required_controls_and_families() -> None:
    text = sm04_text()
    for marker in [
        "SM00",
        "SM01",
        "SM02",
        "SM03",
        "C00",
        "Batch C capstone",
        "B11",
        "Conversion IR",
        "lawful outcome taxonomy",
        "conversion intake",
        "extraction readiness",
        "donor family routing",
        "evaluation/benchmark",
        "runtime/Gate B",
    ]:
        assert marker in text, f"Missing upstream reference: {marker}"
    for number in range(1, 15):
        assert f"C{number:02d}" in text, f"Missing C-family reference: C{number:02d}"


def test_sm04_states_batch_b_b11_are_operational_routing_only() -> None:
    text = sm04_text()
    assert (
        "Batch B/B11 are not final mechanics" in text
        or "B11, remains operational routing doctrine" in text
    )
    assert "not runtime validation authority" in text


def test_sm04_states_d_series_are_draft_source_material_only() -> None:
    text = sm04_text()
    assert "D00-D19 source packs are draft source material only" in text
    assert "cannot become benchmark authority" in text or (
        "cannot become benchmark" in text and "evaluation authority" in text
    )


# --- Pilot benchmark/evaluation definition ---


def test_sm04_defines_pilot_benchmark_evaluation() -> None:
    text = sm04_text()
    assert "bounded review method for future pilot conversion outputs" in text
    assert "not large-scale validation" in text
    assert "not benchmark corpus creation" in text
    assert "not training corpus creation" in text
    assert "not canon review" in text
    assert "not runtime import approval" in text
    assert "not final mechanics approval" in text


# --- Evaluable pilot evidence ---


def test_sm04_includes_all_evaluable_pilot_evidence_terms() -> None:
    text = sm04_text()
    for term in EVALUABLE_PILOT_EVIDENCE_TERMS:
        assert term in text, f"Missing evaluable pilot evidence term: {term}"


def test_sm04_states_evidence_terms_are_not_final_json() -> None:
    text = sm04_text()
    assert "must not turn these into final JSON fields" in text


# --- Rubric interpretation labels ---


def test_sm04_includes_all_rubric_labels() -> None:
    text = sm04_text()
    for label in RUBRIC_LABELS:
        assert label in text, f"Missing rubric label: {label}"


def test_sm04_states_rubric_labels_are_not_registry_values() -> None:
    text = sm04_text()
    assert "not registry values" in text
    assert "must not be written into registry fields" in text


# --- Core evaluation dimensions ---


def test_sm04_includes_all_core_evaluation_dimensions() -> None:
    text = sm04_text()
    for dim in CORE_EVALUATION_DIMENSIONS:
        assert dim in text, f"Missing evaluation dimension: {dim}"


# --- Failure-class inventory ---


def test_sm04_includes_failure_class_inventory() -> None:
    text = sm04_text()
    assert "Failure-class inventory" in text or "failure-class inventory" in text
    for fc in FAILURE_CLASSES:
        assert fc in text, f"Missing failure class: {fc}"


# --- Reviewer workflow ---


def test_sm04_includes_reviewer_workflow_steps() -> None:
    text = sm04_text()
    for step in REVIEWER_WORKFLOW_STEPS:
        assert step in text, f"Missing workflow step: {step}"


# --- Pilot result interpretation ---


def test_sm04_states_what_pilot_evaluation_may_prove() -> None:
    text = sm04_text()
    for marker in [
        "the packet/output loop is reviewable",
        "evidence/provenance survived",
        "lawful outcome accounting worked or failed",
        "C-family routing worked or failed",
        "pending_schema` pressure was identified",
        "donor leakage was contained or occurred",
        "repair/quarantine routes worked or failed",
        "future owners need work",
    ]:
        assert marker in text, f"Missing may-prove marker: {marker}"


def test_sm04_states_what_pilot_evaluation_may_not_prove() -> None:
    text = sm04_text()
    for marker in [
        "large-scale corpus conversion readiness",
        "canon readiness",
        "sourcebook readiness",
        "runtime readiness",
        "final mechanics readiness",
        "live-play readiness",
        "training readiness",
        "benchmark corpus readiness",
        "model adapter readiness",
        "database/schema implementation readiness",
    ]:
        assert marker in text, f"Missing may-not-prove marker: {marker}"


# --- Non-readiness boundaries ---


def test_sm04_includes_large_scale_conversion_non_readiness_boundary() -> None:
    text = sm04_text()
    assert "Large-scale conversion non-readiness boundary" in text
    assert (
        "does not prove large-scale corpus conversion readiness" in text
        or "does not prove large-scale" in text
    )


def test_sm04_includes_runtime_canon_sourcebook_non_readiness_boundary() -> None:
    text = sm04_text()
    assert "Runtime/canon/sourcebook/live-play/training non-readiness boundary" in text
    assert "SM04 is not runtime readiness" in text


# --- Owner routing ---


def test_sm04_includes_owner_routing_and_lawful_fallbacks() -> None:
    text = sm04_text()
    assert "Owner map and lawful fallbacks" in text
    for marker in [
        "future pilot conversion owner",
        "future conversion/evidence validation owner",
        "lawful outcome/conversion intake owner",
        "C00/C-family schema owner and future validation/schema implementation owner",
        "C00/future validation/schema implementation owner",
        "C00/C14 plus future review/legal owner",
        "future conversion integrity owner plus relevant future mechanics/schema owner",
        "future review owner",
        "extraction readiness and pilot conversion owner",
        "future evaluation/benchmark owner",
        "future mechanics requirements owner only",
        "future runtime/Gate B owner only",
        "appropriate later phase owner only",
        "Lawful fallbacks must be explicit",
    ]:
        assert marker in text, f"Missing owner route: {marker}"


# --- Risk register ---


def test_sm04_includes_risk_register() -> None:
    text = sm04_text()
    assert "Risk register" in text
    for marker in [
        "Rubric treated as conversion authority",
        "Evaluation labels treated as registry values",
        "Benchmark corpus creation creep",
        "Donor content embedded in evaluation examples",
        "Donor mechanics leakage",
        "Source-local/legal/IP leakage",
        "Missing schema disguised as implementation",
        "Over-trusting pilot evaluation results",
        "Runtime/canon/sourcebook/training creep",
        "D-series authority creep",
        "Overclaiming pilot success",
        "RHBF hidden law",
    ]:
        assert marker in text, f"Missing risk: {marker}"


# --- Recommended next PR ---


def test_sm04_recommends_next_pr_without_final_mechanics_jump() -> None:
    text = sm04_text()
    assert "Recommended next PR after SM04" in text
    assert "SM05 actual pilot conversion authorization and preflight gate" in text
    assert (
        "SM05 pilot evaluation rubric repair and reviewer calibration controls" in text
    )
    for marker in [
        "must not jump directly to final mechanics",
        "actual broad conversion",
        "runtime schemas",
        "canon consolidation",
        "sourcebook prose",
        "live-play adapter behavior",
        "training corpus creation",
    ]:
        assert marker in text, f"Missing next-PR boundary: {marker}"


# --- No implementation artifacts ---


def test_sm04_does_not_contain_obvious_implementation_artifacts() -> None:
    text = sm04_text()
    forbidden_patterns = [
        r"```\s*json",
        r"```\s*yaml",
        r"\$schema",
        r"\"type\"\s*:\s*\"object\"",
        r"class\s+\w+\(BaseModel\)",
        r"CREATE\s+TABLE",
        r"command_lifecycle\s*[:=]",
        r"context_packet\s*[:=]",
        r"save_state\s*[:=]",
        r"converted_donor_content\s*[:=]",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text, flags=re.IGNORECASE), (
            f"Implementation artifact found: {pattern}"
        )


# --- Registry non-promotion ---


def test_c00_c14_registry_records_not_promoted_to_forbidden_states() -> None:
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        for key in ["status", "authority_level", "test_status", "review_status"]:
            value = _scalar_from_block(block, key)
            if value is not None:
                assert value not in FORBIDDEN_C_PROMOTION_VALUES, (
                    f"{file_id} {key} was promoted to {value!r}"
                )


# --- Future-safe posture ---


def test_future_safe_posture_does_not_block_later_sm_files_or_proper_owner_promotion() -> None:
    text = sm04_text()
    assert "SM05" in text
    assert "later owner" in text.lower() or "future owner" in text.lower()
