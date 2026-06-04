import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM05_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM05_actual_pilot_conversion_authorization_and_preflight_gate.md"
)

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing authorization posture",
    "What SM05 owns",
    "What SM05 must not own",
    "Pilot conversion authorization definition",
    "Authorization scope constraints",
    "Required upstream completion evidence",
    "Packet set authorization gate",
    "Evidence and provenance authorization gate",
    "Lawful outcome authorization gate",
    "C00-C14 and `pending_schema` authorization gate",
    "Rejected-import, source-local, and legal/IP authorization gate",
    "Confidence, review-routing, and human-review authorization gate",
    "Repair, quarantine, and failure-report authorization gate",
    "Benchmark/evaluation authorization gate",
    "Donor leakage preflight gate",
    "Runtime/canon/sourcebook/live-play/training non-readiness gate",
    "Authorization decision labels",
    "Go/no-go decision workflow",
    "Required contents of a later pilot conversion execution PR",
    "What authorization may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM05",
    "Acceptance criteria",
]

AUTHORIZATION_GATE_TERMS = [
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

AUTHORIZATION_LABELS = [
    "authorized_for_controlled_pilot_execution",
    "authorized_with_required_preflight_notes",
    "blocked_by_missing_packet_evidence",
    "blocked_by_dry_run_failure",
    "blocked_by_rubric_gap",
    "blocked_by_legal_ip_risk",
    "blocked_by_donor_leakage_risk",
    "blocked_by_missing_owner",
    "blocked_by_runtime_or_mechanics_creep",
    "repair_required_before_authorization",
    "quarantine_required_before_authorization",
    "human_review_required_before_authorization",
    "not_authorizable",
]

GO_NO_GO_WORKFLOW_STEPS = [
    "Confirm SM00-SM04 exist and are current planning controls",
    "Confirm the pilot packet set is tiny, bounded, and owner-approved",
    "Confirm no real donor content is embedded in SM05",
    "Confirm SM02 readiness gates are satisfied",
    "Confirm SM03 dry-run review is complete or failures are routed",
    "Confirm SM04 evaluation rubric is available",
    "Confirm packet metadata and evidence/provenance preservation path",
    "Confirm lawful outcome, mapping, rejected-import, source-local, and `pending_schema` ledgers can be produced and reviewed after execution",
    "Confirm legal/IP and source-local review routes",
    "Confirm confidence/human-review routes",
    "Confirm repair/quarantine/failure-report routes",
    "Confirm benchmark/evaluation reviewer and result interpretation owner",
    "Confirm donor leakage hard-fail criteria",
    "Confirm no runtime/canon/sourcebook/live-play/training/final-mechanics claims will be made",
    "Assign document-local authorization label",
    "Record authorization decision and rationale",
    "If authorized, permit a later, separate pilot conversion execution PR with strict scope",
    "If blocked, route failures to repair, quarantine, deferred gap ledger",
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


def sm05_text() -> str:
    return read_utf8(SM05_PATH)


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


def test_sm05_file_exists_and_is_nonempty() -> None:
    assert SM05_PATH.exists()
    assert SM05_PATH.is_file()
    assert sm05_text().strip()


def test_required_section_headings_are_present() -> None:
    text = sm05_text()
    for section in REQUIRED_SECTIONS:
        assert section in text, f"Missing section: {section}"


# --- Identity and purpose ---


def test_sm05_states_actual_pilot_conversion_authorization_and_preflight_gate_only() -> None:
    text = sm05_text()
    assert (
        "SM05 is an actual pilot conversion authorization and preflight gate only"
        in text
    )


def test_sm05_states_no_conversion_or_converted_content() -> None:
    text = sm05_text()
    assert "SM05 does not run conversion" in text
    assert "does not create converted donor content" in text


def test_sm05_refuses_all_non_goals() -> None:
    text = sm05_text()
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
    ]:
        assert marker in text, f"Missing non-goal: {marker}"


# --- Upstream references ---


def test_sm05_names_required_controls_and_families() -> None:
    text = sm05_text()
    for marker in [
        "SM00",
        "SM01",
        "SM02",
        "SM03",
        "SM04",
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


def test_sm05_states_batch_b_b11_are_operational_routing_only() -> None:
    text = sm05_text()
    assert (
        "Batch B/B11 are not final mechanics" in text
        or "B11, remains operational routing doctrine" in text
    )
    assert "not runtime validation authority" in text


def test_sm05_states_d_series_are_draft_source_material_only() -> None:
    text = sm05_text()
    assert "D00-D19 source packs are draft source material only" in text
    assert "cannot become authorization authority" in text


# --- Pilot conversion authorization definition ---


def test_sm05_defines_pilot_conversion_authorization() -> None:
    text = sm05_text()
    assert (
        "bounded go/no-go control decision that allows or blocks a later, separate controlled pilot conversion execution PR"
        in text
    )
    assert "not the pilot conversion itself" in text


# --- Authorization scope constraints ---


def test_sm05_recommends_tiny_bounded_packet_set() -> None:
    text = sm05_text()
    assert "3-5 packet candidates" in text
    assert "tiny" in text.lower()
    assert "bounded" in text.lower()


def test_sm05_lists_authorized_pressure_routes() -> None:
    text = sm05_text()
    for marker in [
        "C01 creature/NPC",
        "C02 item/gear",
        "C03 ability/power/technique",
        "C10 table/oracle",
        "conditional C14 source-local setting/cosmology",
    ]:
        assert marker in text, f"Missing authorized pressure route: {marker}"


def test_sm05_lists_deferred_families() -> None:
    text = sm05_text()
    for fam in ["C05", "C06", "C07", "C08", "C11", "C12", "C13"]:
        assert fam in text, f"Missing deferred family: {fam}"
        assert "deferred" in text.lower()
    assert "C04" in text
    assert "C09" in text


# --- Authorization gate/evidence terms ---


def test_sm05_includes_all_authorization_gate_terms() -> None:
    text = sm05_text()
    for term in AUTHORIZATION_GATE_TERMS:
        assert term in text, f"Missing authorization gate term: {term}"


def test_sm05_states_gate_terms_are_not_final_json() -> None:
    text = sm05_text()
    assert "must not turn these into final JSON fields" in text


# --- Authorization decision labels ---


def test_sm05_includes_all_authorization_labels() -> None:
    text = sm05_text()
    for label in AUTHORIZATION_LABELS:
        assert label in text, f"Missing authorization label: {label}"


def test_sm05_states_authorization_labels_are_not_registry_values() -> None:
    text = sm05_text()
    assert "not registry values" in text
    assert "must not be written into registry fields" in text


# --- Go/no-go workflow ---


def test_sm05_includes_go_no_go_workflow_steps() -> None:
    text = sm05_text()
    for step in GO_NO_GO_WORKFLOW_STEPS:
        assert step in text, f"Missing workflow step: {step}"


# --- Later execution PR contents ---


def test_sm05_includes_required_contents_of_later_execution_pr() -> None:
    text = sm05_text()
    assert "Required contents of a later pilot conversion execution PR" in text
    for marker in [
        "explicit reference to SM05 authorization decision",
        "exact packet set and scope",
        "no expansion beyond authorized packet count",
        "post-execution review against SM04",
    ]:
        assert marker in text, f"Missing later PR requirement: {marker}"


# --- Authorize/block criteria ---


def test_sm05_includes_authorize_criteria() -> None:
    text = sm05_text()
    for marker in [
        "packet scope is tiny and bounded",
        "SM02 gates are satisfied",
        "SM04 rubric is ready",
        "legal/IP path exists",
        "source-local containment path exists",
        "donor leakage hard-fail criteria are known",
        "review owner exists",
        "repair/quarantine/failure-report paths exist",
    ]:
        assert marker in text or marker.lower() in text.lower(), (
            f"Missing authorize criterion: {marker}"
        )


def test_sm05_includes_block_criteria() -> None:
    text = sm05_text()
    for marker in [
        "blocked_by_missing_packet_evidence",
        "blocked_by_dry_run_failure",
        "blocked_by_rubric_gap",
        "blocked_by_legal_ip_risk",
        "blocked_by_donor_leakage_risk",
        "blocked_by_missing_owner",
        "blocked_by_runtime_or_mechanics_creep",
        "not_authorizable",
    ]:
        assert marker in text, f"Missing block criterion: {marker}"


# --- What authorization may and may not prove ---


def test_sm05_states_what_authorization_may_prove() -> None:
    text = sm05_text()
    for marker in [
        "the project has a bounded pilot execution scope",
        "preflight review is complete enough to permit a controlled attempt",
        "output review criteria exist",
        "owner routing exists for expected failures",
        "the project can attempt a pilot without claiming finality",
    ]:
        assert marker in text, f"Missing may-prove marker: {marker}"


def test_sm05_states_what_authorization_may_not_prove() -> None:
    text = sm05_text()
    for marker in [
        "conversion success",
        "pilot output quality",
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


def test_sm05_includes_large_scale_conversion_non_readiness_boundary() -> None:
    text = sm05_text()
    assert "Large-scale conversion non-readiness boundary" in text
    assert (
        "does not prove large-scale corpus conversion readiness" in text
        or "does not prove large-scale" in text
    )


def test_sm05_includes_runtime_canon_sourcebook_non_readiness_boundary() -> None:
    text = sm05_text()
    assert "Runtime/canon/sourcebook/live-play/training non-readiness boundary" in text
    assert "SM05 is not runtime readiness" in text


# --- Owner routing ---


def test_sm05_includes_owner_routing_and_lawful_fallbacks() -> None:
    text = sm05_text()
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


def test_sm05_includes_risk_register() -> None:
    text = sm05_text()
    assert "Risk register" in text
    for marker in [
        "Authorization treated as conversion permission",
        "Authorization labels treated as registry values",
        "Scope creep beyond authorized packet count",
        "Donor content embedded in authorization artifacts",
        "Donor mechanics leakage",
        "Source-local/legal/IP leakage",
        "Missing schema disguised as implementation",
        "Over-trusting authorization results",
        "Runtime/canon/sourcebook/training creep",
        "D-series authority creep",
        "RHBF hidden law",
    ]:
        assert marker in text, f"Missing risk: {marker}"


# --- Recommended next PR ---


def test_sm05_recommends_next_pr_without_broad_conversion_jump() -> None:
    text = sm05_text()
    assert "Recommended next PR after SM05" in text
    assert "SM06 controlled pilot conversion execution and output capture plan" in text
    assert (
        "SM06 pilot authorization repair and preflight gap closure controls" in text
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


# --- SM02 waiver prohibition ---


def test_sm05_does_not_contain_explicitly_waived() -> None:
    text = sm05_text()
    assert "explicitly waived" not in text


def test_sm05_states_no_authority_to_waive_sm02_gates() -> None:
    text = sm05_text()
    assert "SM05 has no authority to waive SM02 minimum pilot readiness gates" in text


def test_sm05_blocks_authorization_when_sm02_gates_unsatisfied() -> None:
    text = sm05_text()
    assert "unsatisfied SM02 gate must block authorization" in text


# --- No implementation artifacts ---


def test_sm05_does_not_contain_obvious_implementation_artifacts() -> None:
    text = sm05_text()
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
    text = sm05_text()
    assert "SM06" in text
    assert "later owner" in text.lower() or "future owner" in text.lower()
