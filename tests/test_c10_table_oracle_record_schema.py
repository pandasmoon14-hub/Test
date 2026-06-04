import re

from tests.helpers import ROOT, read_utf8

C10_PATH = ROOT / "docs" / "doctrine" / "schema" / "C10_table_oracle_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C10 owns",
    "## 4. What C10 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Table/oracle family scope and classification",
    "## 7. C10 record grammar, doctrine-level only",
    "## 8. Donor table, oracle, generator, roll-range, weighting, row, and field-name handling",
    "## 9. Random selection, instantiation, reward, travel, social, hazard, and scenario handoffs",
    "## 10. C10 cross-family overlap rules",
    "## 11. Composite table/oracle record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C10 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C06",
]

HANDOFFS = [
    "C10 -> C01",
    "C10 -> C02",
    "C10 -> C03",
    "C10 -> C04",
    "C10 -> C05",
    "C10 -> C06",
    "C10 -> C07",
    "C10 -> C08",
    "C10 -> C09",
    "C10 -> C11",
    "C10 -> C12",
    "C10 -> C13",
    "C10 -> C14",
    "C10 -> pending_schema",
]

OVERLAPS = [
    "C10 vs C01",
    "C10 vs C02",
    "C10 vs C03",
    "C10 vs C05/B09",
    "C10 vs C06/B08",
    "C10 vs C07",
    "C10 vs C09/B10",
    "C10 vs C12/B06",
    "C10 vs C14",
    "C10 vs runtime/backend",
]

FORBIDDEN_PROMOTED_STATUSES = {
    "current",
    "tested_minimum",
    "stable_for_family",
    "stable_cross_family",
    "runtime-ready",
    "runtime_ready",
    "canon",
    "accepted_canon",
}


def c10_text() -> str:
    return read_utf8(C10_PATH)


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


def test_c10_file_exists_at_expected_path() -> None:
    assert C10_PATH.exists()
    assert C10_PATH.is_file()
    assert c10_text().strip()


def test_c10_required_sections_are_present() -> None:
    text = c10_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c10_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c10_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "tables",
        "oracles",
        "generators",
        "random-roll lists",
        "weighted option lists",
        "prompt lists",
        "keyed result lists",
        "result families",
        "table-row provenance",
        "procedural-selection evidence",
        "classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final random-generation procedure",
        "runtime random selection",
        "runtime encounter generation",
        "runtime loot generation",
        "runtime oracle state",
        "probability math",
        "reward economy",
        "encounter balance",
        "table execution",
        "procedural content generation implementation",
        "database table schemas",
        "sourcebook table prose",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
        "live-play behavior",
    ]:
        assert phrase in lowered


def test_c10_requires_c00_base_and_provenance_posture() -> None:
    text = c10_text()
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
    for marker in [
        "doctrine grammar only",
        "not a runtime schema",
        "not a database schema",
        "not a final random generator",
        "not an executable oracle",
        "not an encounter table implementation",
        "not a loot table implementation",
        "not a final roll procedure",
        "not sourcebook table prose",
    ]:
        assert marker in lowered


def test_c10_rejects_donor_table_oracle_generator_and_field_leakage() -> None:
    lowered = c10_text().lower()
    for marker in [
        "donor tables",
        "donor oracles",
        "donor generators",
        "donor random-roll lists",
        "donor roll ranges",
        "donor d100 defaults",
        "donor d20 defaults",
        "donor d66 defaults",
        "donor card-draw defaults",
        "donor row formatting",
        "donor column headers",
        "donor weights/probabilities",
        "donor encounter frequencies",
        "donor loot frequencies",
        "donor reward values",
        "donor table execution rules",
        "donor procedural generation assumptions",
        "donor field names",
        "donor proper nouns",
        "donor cosmology",
        "as astra defaults",
    ]:
        assert marker in lowered


def test_c10_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    text = c10_text()
    lowered = text.lower()
    for marker in ["B05", "B08", "B09", "B10", "B01", "B02"]:
        assert marker in text
    for phrase in [
        "b05 is not c10 schema",
        "b08 is not c10 schema",
        "b09 is not c10 schema",
        "b10 is not c10 schema",
        "b01 is not c10 schema",
        "b02 is not c10 schema",
        "batch b procedure terms must not become c10 schema fields",
    ]:
        assert phrase in lowered


def test_c10_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c10_text()
    lowered = text.lower()
    for handoff in HANDOFFS:
        assert handoff in text
    assert "use references and satellite records, not inheritance or merged schemas" in lowered
    for overlap in OVERLAPS:
        assert overlap in text


def test_c10_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c10_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "legal/ip posture",
        "license-specific expressions",
        "verbatim-similar descriptions",
        "protected art/map references",
        "rejected donor element handling",
        "rejected_import",
        "rejected donor elements include donor tables",
        "donor source-specific prompt language",
    ]:
        assert marker in lowered


def test_c10_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c10_text().lower()
    for marker in [
        "canon eligibility",
        "never promotes canon",
        "does not accept canon",
        "hidden-state and protected-truth boundary",
        "protected truth",
        "runtime random selection",
        "runtime generator state",
        "executable oracle behavior",
        "random seed behavior",
        "database table schemas",
        "entity/component/event schemas",
        "command lifecycle",
        "context packets",
        "save-state",
        "backend generator schemas",
        "encounter generators",
        "loot generators",
        "procedural content generation implementation",
        "live-play table execution",
        "sourcebook table prose",
        "training examples",
    ]:
        assert marker in lowered


def test_c10_includes_good_and_bad_usage_examples() -> None:
    text = c10_text()
    lowered = text.lower()
    assert "Good C10 usage:" in text
    assert "Bad C10 usage:" in text
    for marker in [
        "preserve a donor wilderness event table",
        "preserve a treasure generator",
        "preserve a faction rumor oracle",
        "convert a donor d100 table into an astra default d100 mechanic",
        "turn an encounter table into runtime encounter generation",
        "use donor column headers or donor field names as c10 schema labels",
    ]:
        assert marker in lowered


def test_c10_registry_posture_is_draft_not_current_or_stable() -> None:
    assert _registry_scalar("C10", "status") == "draft"
    assert _registry_scalar("C10", "authority_level") == "schema-draft"
    assert _registry_scalar("C10", "test_status") == "designed"
    assert _registry_scalar("C10", "review_status") == "not_reviewed"
    assert _registry_scalar("C10", "blocked_by") == "[]"

    block = _registry_record_block("C10")
    for status in FORBIDDEN_PROMOTED_STATUSES:
        assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)


def test_c10_does_not_promote_other_c_families_or_regress_c01_c02_c03_c09() -> None:
    for file_id in ["C01", "C02", "C03", "C09"]:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    for file_id in ["C04", "C05", "C06", "C07", "C08", "C11", "C12", "C13", "C14"]:
        block = _registry_record_block(file_id)
        for status in FORBIDDEN_PROMOTED_STATUSES:
            assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)
        for marker in ["stable_for_family", "stable_cross_family", "tested_minimum", "runtime-ready"]:
            assert marker not in block
