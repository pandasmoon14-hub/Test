import re

from tests.helpers import ROOT, read_utf8

C09_PATH = ROOT / "docs" / "doctrine" / "schema" / "C09_hazard_environment_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C09 owns",
    "## 4. What C09 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Hazard/environment family scope and classification",
    "## 7. C09 record grammar, doctrine-level only",
    "## 8. Donor hazard, trap, environmental table, weather, affliction, and field-name handling",
    "## 9. Contact, exposure, trigger, travel, location, damage, condition, and effect handoffs",
    "## 10. C09 cross-family overlap rules",
    "## 11. Composite hazard/environment record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C09 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C10",
]

HANDOFFS = [
    "C09 -> C01",
    "C09 -> C02",
    "C09 -> C03",
    "C09 -> C04",
    "C09 -> C05",
    "C09 -> C06",
    "C09 -> C07",
    "C09 -> C08",
    "C09 -> C10",
    "C09 -> C11",
    "C09 -> C12",
    "C09 -> C13",
    "C09 -> C14",
    "C09 -> pending_schema",
]

OVERLAPS = [
    "C09 vs C06",
    "C09 vs C03",
    "C09 vs C02",
    "C09 vs C01",
    "C09 vs C10",
    "C09 vs C08",
    "C09 vs C07",
    "C09 vs C14",
    "C09 vs B10/B08/B02",
    "C09 vs Batch A damage/condition/resource owners",
]

FORBIDDEN_PROMOTED_STATUSES = {"current", "tested_minimum", "stable_for_family", "stable_cross_family"}


def c09_text() -> str:
    return read_utf8(C09_PATH)


def _registry_record_block(file_id: str) -> str:
    registry_text = read_utf8(REGISTRY_PATH)
    match = re.search(
        rf"^- file_id: {file_id}\n(?P<block>.*?)(?=^- file_id: |\Z)",
        registry_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing registry record for {file_id}"
    return match.group(0)


def _registry_scalar(file_id: str, key: str) -> str:
    block = _registry_record_block(file_id)
    match = re.search(rf"^  {key}: ([^\n]+)$", block, flags=re.MULTILINE)
    assert match, f"Missing {key} for {file_id}"
    return match.group(1).strip().strip("'\"")


def test_c09_file_exists_at_expected_path() -> None:
    assert C09_PATH.exists()
    assert C09_PATH.is_file()
    assert c09_text().strip()


def test_c09_required_sections_are_present() -> None:
    text = c09_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c09_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c09_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "hazards, environments, weather, region pressure, terrain pressure",
        "planar conditions",
        "afflictions",
        "exposure records",
        "contamination",
        "disease-like pressure",
        "poison-like pressure",
        "radiation-like pressure",
        "corruption-like pressure",
        "trap-like pressure",
        "unstable material pressure",
        "ambient danger",
        "classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final damage math",
        "condition math",
        "exposure math",
        "trap procedure",
        "travel procedure",
        "exploration procedure",
        "action procedure",
        "hazard trigger procedure",
        "weather simulation",
        "environmental canon truth",
        "encounter balance",
        "runtime damage resolution",
        "runtime hazard instances",
        "runtime environmental state",
        "runtime region state",
        "runtime affliction trackers",
        "sourcebook hazard prose",
        "accepted lexicon",
        "canon acceptance",
        "live-play behavior",
    ]:
        assert phrase in lowered


def test_c09_requires_c00_base_and_provenance_posture() -> None:
    text = c09_text()
    lowered = text.lower()
    assert "inherit/include `AstraContentRecordBase`" in text
    assert "extends: AstraContentRecordBase" in text
    for marker in [
        "packet_refs",
        "source_evidence_refs",
        "construct_refs",
        "outcome_refs",
        "provenance_refs",
        "source_local_boundary",
        "rejected_donor_elements",
        "canon_eligibility",
        "confidence",
        "validation",
        "lineage",
        "composition",
        "cross-reference",
        "legal/IP posture",
    ]:
        assert marker.lower() in lowered
    assert "doctrine grammar only" in lowered
    assert "not a runtime schema" in lowered
    assert "not a database schema" in lowered
    assert "not a final hazard statblock" in lowered
    assert "not a trap statblock" in lowered
    assert "not a weather simulation" in lowered
    assert "not a damage/condition table" in lowered
    assert "not sourcebook hazard prose" in lowered


def test_c09_rejects_donor_hazard_environment_and_field_leakage() -> None:
    lowered = c09_text().lower()
    for marker in [
        "donor hazards",
        "donor traps",
        "donor hazard tables",
        "donor weather tables",
        "donor environmental tables",
        "donor field names",
        "donor damage math",
        "donor condition math",
        "donor save dcs",
        "donor difficulty dcs",
        "donor exposure intervals",
        "donor weather probabilities",
        "donor terrain modifiers",
        "donor disease/poison/corruption/radiation stages",
        "donor trigger procedures",
        "donor proper nouns",
        "donor cosmology",
        "as astra defaults",
    ]:
        assert marker in lowered
    for forbidden_mechanic in [
        "final numerical values",
        "damage dice",
        "damage thresholds",
        "save dcs",
        "difficulty dcs",
        "condition severities",
        "exposure intervals",
        "travel speeds",
        "weather probabilities",
        "regional modifiers",
        "trap attack bonuses",
        "recharge values",
        "duration counts",
        "disease stages",
        "poison stages",
        "corruption stages",
        "radiation doses",
        "hazard math",
    ]:
        assert forbidden_mechanic in lowered


def test_c09_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    lowered = c09_text().lower()
    for marker in [
        "c09 references b10",
        "b10 is not c09 schema",
        "c09 references b08",
        "b08 is not c09 schema",
        "c09 references b01",
        "b01 is not c09 schema",
        "c09 references b02",
        "b02 is not c09 schema",
        "c09 may reference b03",
        "b03 is not c09 schema",
        "batch b procedure terms must not become c09 schema fields",
        "doctrine-facing pressure only",
    ]:
        assert marker in lowered


def test_c09_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c09_text()
    for handoff in HANDOFFS:
        assert handoff in text
    for overlap in OVERLAPS:
        assert overlap in text
    assert "C09 vs C04/C05/C11/C12/C13" in text
    assert "use references and satellite records, not inheritance or merged schemas" in text
    assert "inheritance_allowed: false" in text
    assert "Cross-family references do not make the target family inherit C09 grammar" in text
    assert "table rows do not become C09 records unless converted with provenance" in text


def test_c09_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c09_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "donor hazard names",
        "trap names",
        "named planes",
        "named regions",
        "named weather systems",
        "named diseases",
        "named poisons",
        "named magical effects",
        "named environmental rules",
        "named cosmology",
        "source-specific metaphysics",
        "rejected donor element handling",
        "rejected donor elements include donor hazards",
        "prevents accidental import",
    ]:
        assert marker in lowered


def test_c09_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c09_text().lower()
    for marker in [
        "hidden-state and protected-truth boundary",
        "must not expose protected truth",
        "runtime boundary",
        "runtime hazard instances",
        "runtime environmental state",
        "runtime region state",
        "runtime affliction trackers",
        "runtime damage resolution",
        "entity/component schemas",
        "event schemas",
        "command lifecycle",
        "context packets",
        "save-state",
        "database contracts",
        "backend hazard schemas",
        "weather simulation systems",
        "combat trackers",
        "travel trackers",
        "canon/sourcebook/live-play/training boundary",
        "c09 never promotes canon",
        "does not accept canon",
        "sourcebook hazard prose",
        "live-play behavior",
    ]:
        assert marker in lowered


def test_c09_includes_good_and_bad_usage_examples() -> None:
    text = c09_text()
    assert "Good C09 usage:" in text
    assert "Bad C09 usage:" in text
    assert "Convert a donor hazard-like entry" in text
    assert "Copy a donor hazard table, trap statblock" in text


def test_c09_registry_posture_is_draft_not_current_or_stable() -> None:
    block = _registry_record_block("C09")
    assert _registry_scalar("C09", "status") == "draft"
    assert _registry_scalar("C09", "authority_level") == "schema-draft"
    assert _registry_scalar("C09", "test_status") == "designed"
    assert _registry_scalar("C09", "review_status") == "not_reviewed"
    assert _registry_scalar("C09", "status") not in FORBIDDEN_PROMOTED_STATUSES
    assert _registry_scalar("C09", "test_status") not in FORBIDDEN_PROMOTED_STATUSES
    for forbidden in [
        "status: current",
        "stable_for_family",
        "stable_cross_family",
        "tested_minimum",
        "canon-current",
        "runtime-ready",
    ]:
        assert forbidden not in block


def test_c09_does_not_promote_other_c_families_or_regress_c01_c02_c03() -> None:
    for file_id in ["C01", "C02", "C03"]:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    for file_id in [f"C{number:02d}" for number in list(range(4, 9)) + list(range(10, 15))]:
        block = _registry_record_block(file_id)
        assert _registry_scalar(file_id, "status") not in FORBIDDEN_PROMOTED_STATUSES
        assert _registry_scalar(file_id, "authority_level") != "schema-current"
        assert _registry_scalar(file_id, "test_status") not in FORBIDDEN_PROMOTED_STATUSES
        for forbidden in [
            "status: current",
            "stable_for_family",
            "stable_cross_family",
            "tested_minimum",
            "canon-current",
            "runtime-ready",
        ]:
            assert forbidden not in block
