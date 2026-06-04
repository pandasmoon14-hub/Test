import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM01_PATH = ROOT / "docs" / "doctrine" / "schema_math_mechanics" / "SM01_validation_schema_inventory_and_readiness_controls.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Upstream controls and authority boundary",
    "## 3. Existing validation and schema posture",
    "## 4. What SM01 owns",
    "## 5. What SM01 must not own",
    "## 6. Existing file and test inventory",
    "## 7. C00-C14 validation coverage map",
    "## 8. Validation schema class inventory",
    "## 9. Record instance schema inventory",
    "## 10. Cross-record reference validation inventory",
    "## 11. Conversion packet validation inventory",
    "## 12. Evidence and provenance validation inventory",
    "## 13. Source-local, rejected-import, and legal/IP validation inventory",
    "## 14. Canon-review and conflict-ledger validation inventory",
    "## 15. Pilot conversion output validation inventory",
    "## 16. Mechanics I/O validation boundary inventory",
    "## 17. Runtime-prep validation boundary inventory",
    "## 18. Test fixture schema inventory",
    "## 19. Gap classification matrix",
    "## 20. Owner map and lawful fallbacks",
    "## 21. Readiness states for future validation work",
    "## 22. Risk register",
    "## 23. Recommended next PR after SM01",
    "## 24. Acceptance criteria",
]

MAJOR_CLASSES = [
    "validation schemas",
    "record instance schemas",
    "cross-record reference validation",
    "conversion packet validation",
    "evidence/provenance validation",
    "source-local boundary validation",
    "rejected donor element validation",
    "legal/IP validation",
    "canon-review validation",
    "conflict-ledger validation",
    "pilot conversion output validation",
    "mechanics I/O validation boundaries",
    "runtime-prep validation boundaries",
    "test fixture schemas",
    "registry integrity validation",
    "confidence/review-routing validation",
    "parent/child/satellite/composite record validation",
    "pending_schema validation",
]

READINESS_LABELS = [
    "inventory_only",
    "partly_covered",
    "owner_needed",
    "blocked_by_pilot_evidence",
    "blocked_by_mechanics_owner",
    "blocked_by_runtime_gate",
    "defer_with_pending_schema",
    "human_review_required",
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


def sm01_text() -> str:
    return read_utf8(SM01_PATH)


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


def test_sm01_file_exists_and_is_nonempty() -> None:
    assert SM01_PATH.exists()
    assert SM01_PATH.is_file()
    assert sm01_text().strip()


def test_required_section_headings_are_present() -> None:
    text = sm01_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_sm01_names_required_controls_and_families() -> None:
    text = sm01_text()
    for marker in ["SM00", "C00", "Batch C capstone", "B11", "Conversion IR", "lawful outcome taxonomy", "runtime/Gate B"]:
        assert marker in text
    for number in range(1, 15):
        assert f"C{number:02d}" in text


def test_sm01_states_inventory_readiness_control_only() -> None:
    text = sm01_text()
    assert "SM01 is an inventory/readiness-control file only" in text
    assert "what validation and schema artifacts will eventually be needed" in text


def test_sm01_refuses_required_non_goals() -> None:
    text = sm01_text()
    for marker in [
        "not a final schema file",
        "not executable JSON Schema",
        "not a Pydantic model",
        "not a runtime contract",
        "not a backend/database schema",
        "not final mechanics",
        "not canon",
        "not sourcebook prose",
        "not live-play behavior",
        "not training data",
        "does not create JSON Schema files",
        "does not create JSON Schema files, Pydantic models, runtime schemas, backend schemas, database schemas",
        "command lifecycle contracts",
        "context packet contracts",
        "save-state shapes",
        "does not promote C00-C14 registry statuses",
        "does not rewrite C00-C14",
        "does not add C15",
        "does not use RHBF as hidden law",
    ]:
        assert marker in text


def test_all_major_validation_schema_classes_are_listed() -> None:
    text = sm01_text()
    for marker in MAJOR_CLASSES:
        assert marker in text


def test_gap_classification_matrix_owner_routing_and_fallbacks_are_present() -> None:
    text = sm01_text()
    assert "## 19. Gap classification matrix" in text
    for column in ["Existing partial coverage", "Missing coverage", "Future owner", "Blocked dependencies", "Lawful fallback", "Readiness state"]:
        assert column in text
    assert "## 20. Owner map and lawful fallbacks" in text
    for marker in [
        "future validation/schema implementation owner",
        "future SM03 or later schema-validation owner",
        "future pilot conversion readiness owner",
        "future conversion/evidence validation owner",
        "future canon/conflict governance owner",
        "future mechanics requirements owner",
        "future runtime/Gate B owner",
        "future validation test owner",
        "pending_schema",
        "quarantine",
        "deferred gap ledger",
        "Astra Doctrine Council review",
    ]:
        assert marker in text


def test_readiness_states_are_local_planning_labels_not_registry_values() -> None:
    text = sm01_text()
    for label in READINESS_LABELS:
        assert label in text
    assert "local planning labels only and are not registry values" in text
    assert "must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`" in text


def test_sm01_refuses_registry_promotion_and_c15_creation() -> None:
    text = sm01_text()
    assert "does not promote C00-C14 registry statuses" in text
    assert "does not add C15" in text
    assert "no C00-C14 rewrite and no C15" in text


def test_sm01_preserves_d_series_as_draft_source_material_only() -> None:
    text = sm01_text()
    assert "D00-D19 source packs only as draft source material" in text
    assert "D-series source packs are draft source material only and cannot become validation authority" in text
    assert "D00-D19 remain draft source material only" in text


def test_sm01_does_not_contain_obvious_implementation_artifacts() -> None:
    text = sm01_text()
    forbidden_patterns = [
        r'"type"\s*:\s*"object"',
        r"\bproperties\s*:",
        r"\brequired\s*:\s*\[",
        r"\bclass\s+\w+\(\s*BaseModel\s*\)",
        r"\bCREATE\s+TABLE\b",
        r"\bPRIMARY\s+KEY\b",
        r"\binterface\s+CommandLifecycle\b",
        r"\btype\s+CommandLifecycle\b",
        r"\binterface\s+ContextPacket\b",
        r"\btype\s+ContextPacket\b",
        r"\binterface\s+SaveState\b",
        r"\btype\s+SaveState\b",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text, flags=re.IGNORECASE), pattern
    assert "```json" not in text.lower()
    assert "```yaml" not in text.lower()


def test_registry_records_for_c00_c14_are_not_promoted_to_forbidden_states() -> None:
    for number in range(0, 15):
        file_id = f"C{number:02d}"
        block = _registry_record_block(file_id)
        for key in ["status", "authority_level", "test_status", "review_status"]:
            value = _scalar_from_block(block, key)
            assert value not in FORBIDDEN_C_PROMOTION_VALUES, f"{file_id} {key} was promoted to {value}"


def test_recommended_next_pr_is_pilot_conversion_readiness_not_graph_validation() -> None:
    text = sm01_text()
    assert "Recommended next PR: SM02 minimum pilot conversion readiness and packet validation controls" in text
    for marker in [
        "minimum readiness gate for a small pilot conversion packet/output loop",
        "conversion packet validation",
        "evidence/provenance readiness",
        "lawful outcome completeness",
        "C00-C14 routing readiness",
        "rejected-import/source-local/legal/IP routing",
        "review queues",
        "pilot fixtures",
        "failure/quarantine reporting",
        "benchmark/evaluation prerequisites",
        "Cross-record reference validation and graph-readiness should move to SM03 or a later schema-validation owner",
    ]:
        assert marker in text
    assert "Recommended next PR: SM02 cross-record reference validation planning and graph-readiness controls" not in text


def test_future_safe_posture_does_not_block_later_sm_files_or_proper_owner_promotion() -> None:
    text = sm01_text()
    assert "later SM02/SM03/etc. files may be added" in text
    assert "later proper owner-controlled registry promotion may occur outside SM01" in text
