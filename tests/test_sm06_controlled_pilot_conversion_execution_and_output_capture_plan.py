import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM06_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM06_controlled_pilot_conversion_execution_and_output_capture_plan.md"
)

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing execution-planning posture",
    "What SM06 owns",
    "What SM06 must not own",
    "Controlled pilot execution definition",
    "Execution scope constraints",
    "Required SM05 authorization reference",
    "Pre-execution verification checklist",
    "Execution packet boundary controls",
    "Evidence and provenance capture requirements",
    "Construct inventory capture requirements",
    "Lawful outcome ledger capture requirements",
    "Mapping ledger capture requirements",
    "C00-C14 and `pending_schema` output routing capture",
    "Rejected-import, source-local, and legal/IP capture",
    "Confidence, review-routing, and human-review capture",
    "Repair, quarantine, and failure-report capture",
    "Donor leakage capture and hard-fail handling",
    "Pilot output package contents",
    "Post-execution review handoff to SM04",
    "Execution result labels",
    "What controlled execution may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM06",
    "Acceptance criteria",
]

OUTPUT_CAPTURE_TERMS = [
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
    "SM05 authorization reference",
    "SM04 review handoff target",
]

EXECUTION_LABELS = [
    "execution_ready_under_sm05_authorization",
    "execution_blocked_by_missing_authorization",
    "execution_blocked_by_scope_expansion",
    "execution_blocked_by_missing_evidence_path",
    "execution_blocked_by_lawful_outcome_capture_gap",
    "execution_blocked_by_routing_capture_gap",
    "execution_blocked_by_legal_ip_risk",
    "execution_blocked_by_donor_leakage_risk",
    "execution_blocked_by_review_handoff_gap",
    "execution_captured_for_sm04_review",
    "execution_requires_repair",
    "execution_requires_quarantine",
    "execution_not_reviewable",
    "execution_aborted",
]

SM05_AUTHORIZATION_REFERENCE_TERMS = [
    "SM05 authorization decision",
    "authorization label",
    "authorization rationale",
    "exact authorized packet count",
    "exact authorized C-family pressure routes",
    "named authorization owner",
    "SM02 gates were satisfied with no waived minimum gate",
    "SM03 dry-run review passed or failures were routed",
    "SM04 rubric is ready for post-execution review",
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


def sm06_text() -> str:
    return read_utf8(SM06_PATH)


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


def test_sm06_file_exists_and_is_nonempty() -> None:
    assert SM06_PATH.exists()
    assert SM06_PATH.is_file()
    assert sm06_text().strip()


def test_required_section_headings_are_present() -> None:
    text = sm06_text()
    for section in REQUIRED_SECTIONS:
        assert section in text, f"Missing section: {section}"


# --- Identity and purpose ---


def test_sm06_states_controlled_pilot_conversion_execution_and_output_capture_plan_only() -> None:
    text = sm06_text()
    assert (
        "SM06 is a controlled pilot conversion execution and output capture planning/control file only"
        in text
    )


def test_sm06_states_no_conversion_or_converted_content() -> None:
    text = sm06_text()
    assert "SM06 does not run conversion" in text
    assert "does not create converted donor content" in text
    assert "does not create converted donor content or pilot outputs" in text


def test_sm06_refuses_all_non_goals() -> None:
    text = sm06_text()
    for marker in [
        "create benchmark corpora",
        "create evaluation corpora",
        "create training data",
        "create fine-tuning data",
        "create model behavior policy",
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
        "waive SM02 minimum pilot readiness gates",
        "bypass SM05 authorization",
    ]:
        assert marker in text, f"Missing non-goal: {marker}"


def test_sm06_refuses_real_donor_excerpts() -> None:
    text = sm06_text()
    for marker in [
        "select, embed, quote, paraphrase, transform, or convert real copyrighted donor excerpts",
        "donor statblocks",
        "donor tables",
        "donor maps",
        "donor setting prose",
        "donor proper nouns",
    ]:
        assert marker in text, f"Missing donor-refusal marker: {marker}"


# --- Upstream references ---


def test_sm06_names_required_controls_and_families() -> None:
    text = sm06_text()
    for marker in [
        "SM00",
        "SM01",
        "SM02",
        "SM03",
        "SM04",
        "SM05",
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


def test_sm06_states_upstream_authority_for_sm00_through_sm05() -> None:
    text = sm06_text()
    assert "SM00 owns master sequencing" in text
    assert "SM01 owns validation/schema inventory posture" in text
    assert "SM02 owns minimum pilot conversion readiness gates" in text
    assert "SM03 owns" in text
    assert "SM04 owns" in text
    assert "SM05 owns" in text


def test_sm06_states_c00_owns_shared_content_record_base_posture() -> None:
    text = sm06_text()
    assert "C00 owns shared content record base posture" in text
    assert "C01-C14 own conversion-stage/canon-review family grammar" in text


def test_sm06_states_batch_b_b11_are_operational_routing_only() -> None:
    text = sm06_text()
    assert (
        "Batch B/B11 are operational routing doctrine, not final mechanics or runtime validation authority"
        in text
    )


def test_sm06_states_d_series_are_draft_source_material_only() -> None:
    text = sm06_text()
    assert "D00-D19 source packs are draft source material only" in text
    assert "cannot become execution authority" in text


# --- Controlled pilot execution definition ---


def test_sm06_defines_controlled_pilot_execution() -> None:
    text = sm06_text()
    assert (
        "later, separately authorized, tightly bounded conversion attempt whose purpose is to produce reviewable pilot evidence under SM02-SM05 controls"
        in text
    )
    assert "SM06 only defines the plan for such execution; it does not perform it" in text


# --- Execution scope constraints ---


def test_sm06_recommends_tiny_bounded_execution_scope() -> None:
    text = sm06_text()
    assert "3-5 packet candidates" in text
    assert "tiny" in text.lower()
    assert "bounded" in text.lower()


def test_sm06_lists_authorized_pressure_routes() -> None:
    text = sm06_text()
    for marker in [
        "C01 creature/NPC",
        "C02 item/gear",
        "C03 ability/power/technique",
        "C10 table/oracle",
        "conditional C14 source-local setting/cosmology",
    ]:
        assert marker in text, f"Missing authorized pressure route: {marker}"


def test_sm06_lists_deferred_families() -> None:
    text = sm06_text()
    for fam in ["C05", "C06", "C07", "C08", "C11", "C12", "C13"]:
        assert fam in text, f"Missing deferred family: {fam}"
        assert "deferred" in text.lower()
    assert "C04" in text
    assert "C09" in text


# --- SM05 authorization reference ---


def test_sm06_includes_required_sm05_authorization_reference_terms() -> None:
    text = sm06_text()
    for term in SM05_AUTHORIZATION_REFERENCE_TERMS:
        assert term in text, f"Missing SM05 authorization reference term: {term}"


def test_sm06_cannot_waive_sm02_gates() -> None:
    text = sm06_text()
    assert "SM06 cannot waive SM02 gates" in text
    assert "cannot authorize execution without SM05 authorization" in text


def test_sm06_states_no_authority_to_waive_sm02() -> None:
    text = sm06_text()
    assert "no authority to waive SM02 minimum pilot readiness gates" in text


# --- Output capture terms ---


def test_sm06_includes_all_output_capture_terms() -> None:
    text = sm06_text()
    for term in OUTPUT_CAPTURE_TERMS:
        assert term in text, f"Missing output capture term: {term}"


def test_sm06_states_capture_terms_are_not_final_json() -> None:
    text = sm06_text()
    assert "must not turn these into final JSON fields" in text


# --- Execution result labels ---


def test_sm06_includes_all_execution_labels() -> None:
    text = sm06_text()
    for label in EXECUTION_LABELS:
        assert label in text, f"Missing execution label: {label}"


def test_sm06_states_execution_labels_are_not_registry_values() -> None:
    text = sm06_text()
    assert "not registry values" in text
    assert "must not be written into registry fields" in text


# --- Post-execution review handoff ---


def test_sm06_includes_post_execution_review_handoff_to_sm04() -> None:
    text = sm06_text()
    assert "Post-execution review handoff to SM04" in text
    for marker in [
        "captured output package",
        "evidence/provenance artifacts",
        "all ledgers",
        "failure reports",
        "repair/quarantine states",
        "authorization reference",
        "reviewer assignment",
        "explicit non-readiness statement",
    ]:
        assert marker in text, f"Missing handoff requirement: {marker}"


def test_sm06_states_outputs_remain_pilot_evidence_until_sm04_review() -> None:
    text = sm06_text()
    assert "outputs remain pilot evidence only until reviewed under SM04" in text


# --- What controlled execution may and may not prove ---


def test_sm06_states_what_execution_may_prove() -> None:
    text = sm06_text()
    for marker in [
        "the project can execute a bounded pilot under SM02-SM05 controls",
        "output capture requirements can be followed or fail visibly",
        "evidence/provenance can survive or fail visibly",
        "lawful outcome accounting can be captured or fail visibly",
        "donor leakage can be detected or fail to be detected",
        "outputs can be handed to SM04 review",
    ]:
        assert marker in text, f"Missing may-prove marker: {marker}"


def test_sm06_states_what_execution_may_not_prove() -> None:
    text = sm06_text()
    for marker in [
        "pilot output quality",
        "pilot evaluation success",
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


def test_sm06_includes_large_scale_conversion_non_readiness_boundary() -> None:
    text = sm06_text()
    assert "Large-scale conversion non-readiness boundary" in text
    assert "does not prove large-scale corpus conversion readiness" in text


def test_sm06_includes_runtime_canon_sourcebook_non_readiness_boundary() -> None:
    text = sm06_text()
    assert "Runtime/canon/sourcebook/live-play/training non-readiness boundary" in text
    assert "SM06 is not runtime readiness" in text


# --- Owner routing ---


def test_sm06_includes_owner_routing_and_lawful_fallbacks() -> None:
    text = sm06_text()
    assert "Owner map and lawful fallbacks" in text
    for marker in [
        "future pilot conversion owner",
        "future conversion/evidence validation owner",
        "lawful outcome/conversion intake owner",
        "conversion intake owner",
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


def test_sm06_includes_risk_register() -> None:
    text = sm06_text()
    assert "Risk register" in text
    for marker in [
        "Execution plan treated as conversion execution",
        "Execution labels treated as registry values",
        "Scope creep beyond SM05 authorized packet count",
        "Donor content embedded in execution plan artifacts",
        "Donor mechanics leakage",
        "Source-local/legal/IP leakage",
        "Missing schema disguised as implementation",
        "Over-trusting execution results",
        "Runtime/canon/sourcebook/training creep",
        "D-series authority creep",
        "RHBF hidden law",
        "SM05 authorization bypass",
        "SM02 gate waiver",
        "Post-execution review skipped",
    ]:
        assert marker in text, f"Missing risk: {marker}"


# --- Recommended next PR ---


def test_sm06_recommends_next_pr_without_broad_conversion_jump() -> None:
    text = sm06_text()
    assert "Recommended next PR after SM06" in text
    assert (
        "SM07 controlled pilot conversion execution packet scaffold and review harness"
        in text
    )
    assert (
        "SM07 pilot execution plan repair and output-capture gap closure controls"
        in text
    )
    for marker in [
        "broad conversion",
        "final mechanics",
        "runtime schemas",
        "canon consolidation",
        "sourcebook prose",
        "live-play adapter behavior",
        "training corpus creation",
    ]:
        assert marker in text, f"Missing next-PR boundary: {marker}"


# --- No implementation artifacts ---


def test_sm06_does_not_contain_obvious_implementation_artifacts() -> None:
    text = sm06_text()
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
    text = sm06_text()
    assert "SM07" in text
    assert "later owner" in text.lower() or "future owner" in text.lower()
