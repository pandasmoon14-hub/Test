import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM02_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md"
)

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Upstream controls and authority boundary",
    "## 3. Existing pilot-readiness posture",
    "## 4. What SM02 owns",
    "## 5. What SM02 must not own",
    "## 6. Minimum pilot conversion readiness definition",
    "## 7. Pilot scope constraints",
    "## 8. Donor-family selection constraints",
    "## 9. Conversion packet readiness gate",
    "## 10. Evidence and provenance readiness gate",
    "## 11. Lawful outcome completeness gate",
    "## 12. C00-C14 routing readiness gate",
    "## 13. `pending_schema` and missing-owner readiness gate",
    "## 14. Rejected-import, source-local, and legal/IP readiness gate",
    "## 15. Confidence, review-routing, and human-review readiness gate",
    "## 16. Repair queue, quarantine, and failure-reporting readiness gate",
    "## 17. Pilot fixtures and test-data readiness gate",
    "## 18. Benchmark and evaluation prerequisites",
    "## 19. Minimum pilot pass/fail criteria",
    "## 20. Large-scale conversion non-readiness boundary",
    "## 21. Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "## 22. Owner map and lawful fallbacks",
    "## 23. Risk register",
    "## 24. Recommended next PR after SM02",
    "## 25. Acceptance criteria",
]

PILOT_READINESS_TERMS = [
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


def sm02_text() -> str:
    return read_utf8(SM02_PATH)


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
    match = re.search(rf"^\s*{re.escape(key)}:\s*['\"]?(?P<value>[^'\"\n#]+)", block, flags=re.MULTILINE)
    return match.group("value").strip() if match else None


def test_sm02_file_exists_and_is_nonempty() -> None:
    assert SM02_PATH.exists()
    assert SM02_PATH.is_file()
    assert sm02_text().strip()


def test_required_section_headings_are_present() -> None:
    text = sm02_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_sm02_names_required_controls_and_families() -> None:
    text = sm02_text()
    for marker in [
        "SM00",
        "SM01",
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
        assert marker in text
    for number in range(1, 15):
        assert f"C{number:02d}" in text


def test_sm02_states_pilot_packet_output_control_only() -> None:
    text = sm02_text()
    assert "SM02 is a pilot readiness and packet/output control file only" in text
    assert "readiness requirements and future validation targets only" in text


def test_sm02_states_no_conversion_or_converted_content() -> None:
    text = sm02_text()
    assert "SM02 does not run conversion and does not create converted donor content" in text
    assert "run conversion" in text
    assert "create converted donor content" in text


def test_sm02_refuses_required_non_goals() -> None:
    text = sm02_text()
    for marker in [
        "create final output schemas",
        "create final executable schemas",
        "create JSON Schema files",
        "create Pydantic models",
        "runtime/backend/database contracts",
        "create runtime schemas",
        "create backend schemas",
        "create database schemas",
        "command lifecycle contracts",
        "context packet contracts",
        "save-state shapes",
        "create final mechanics",
        "create exact math",
        "promote canon",
        "write sourcebook prose",
        "create live-play behavior",
        "create training/evaluation corpora",
        "promote C00-C14 registry statuses",
        "rewrite C00-C14",
        "add C15",
        "treat D00-D19 as authority",
        "use RHBF as hidden law",
    ]:
        assert marker in text


def test_sm02_distinguishes_minimum_pilot_readiness_from_later_readiness() -> None:
    text = sm02_text()
    for marker in [
        "large-scale corpus conversion readiness",
        "canon readiness",
        "sourcebook readiness",
        "runtime readiness",
        "final mechanics readiness",
        "live-play readiness",
        "training readiness",
    ]:
        assert marker in text
    assert "not large-scale readiness" in text
    assert "not unlock large-scale corpus conversion readiness" in text


def test_sm02_lists_recommended_initial_and_deferred_c_family_routes() -> None:
    text = sm02_text()
    for marker in ["C01 creature/NPC", "C02 item/gear", "C03 ability/power/technique", "C10 table/oracle"]:
        assert marker in text
    assert "conditional C14" in text
    assert "legal/IP/source-local routing is ready" in text
    for marker in ["C05", "C06", "C07", "C08", "C11", "C12", "C13"]:
        assert marker in text
    assert "may be deferred unless selected for pressure test" in text


def test_sm02_lists_all_pilot_readiness_gate_terms() -> None:
    text = sm02_text()
    for marker in PILOT_READINESS_TERMS:
        assert marker in text


def test_sm02_includes_minimum_pilot_pass_fail_criteria() -> None:
    text = sm02_text()
    assert "Minimum pilot pass criteria" in text
    assert "Minimum pilot fail criteria" in text
    for marker in [
        "Pass only if every visible donor construct",
        "Pass only if every converted/output record",
        "Fail if donor math/statblocks/economies/classes/dice/cosmology leak as Astra defaults",
        "Fail if final mechanics, runtime schemas, canon, sourcebook prose, live-play behavior, or training data are created",
        "Fail if D-series source packs are treated as authority",
        "Fail if pilot outputs are treated as large-scale readiness",
    ]:
        assert marker in text


def test_sm02_includes_owner_routing_and_lawful_fallbacks() -> None:
    text = sm02_text()
    assert "## 22. Owner map and lawful fallbacks" in text
    for marker in [
        "future pilot conversion owner",
        "future conversion/evidence validation owner",
        "lawful outcome/conversion intake owner",
        "C00/C-family schema owner and future validation/schema implementation owner",
        "C00/future validation/schema implementation owner",
        "C00/C14 plus future review/legal owner",
        "future review owner",
        "extraction readiness and pilot conversion owner",
        "future evaluation/benchmark owner",
        "future mechanics requirements owner only",
        "future runtime/Gate B owner only",
        "appropriate later phase owner only",
        "Lawful fallbacks must be explicit",
    ]:
        assert marker in text


def test_sm02_includes_risk_register() -> None:
    text = sm02_text()
    assert "## 23. Risk register" in text
    for marker in [
        "Pilot scope creep",
        "Donor mechanics leakage",
        "Source-local/legal/IP leakage",
        "Missing schema disguised as implementation",
        "Evidence loss",
        "Over-trusting pilot outputs",
        "Runtime/canon/sourcebook/training creep",
        "D-series authority creep",
        "Evaluation misuse",
    ]:
        assert marker in text


def test_sm02_recommends_next_pr_without_final_mechanics_jump() -> None:
    text = sm02_text()
    assert "## 24. Recommended next PR after SM02" in text
    assert "SM03 pilot packet fixture and dry-run review plan" in text
    assert "should not jump directly to final mechanics" in text
    assert "without running conversion" in text


def test_sm02_has_no_obvious_implementation_artifacts() -> None:
    text = sm02_text()
    forbidden_patterns = [
        r"```\s*json",
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
        assert not re.search(pattern, text, flags=re.IGNORECASE), pattern


def test_c00_c14_registry_records_not_promoted_to_forbidden_states() -> None:
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        for key in ["status", "authority_level", "test_status", "review_status"]:
            value = _scalar_from_block(block, key)
            if value is not None:
                assert value not in FORBIDDEN_C_PROMOTION_VALUES, f"{file_id} {key} was promoted to {value!r}"
