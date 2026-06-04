import re

from tests.helpers import ROOT, read_utf8

C13_PATH = ROOT / "docs" / "doctrine" / "schema" / "C13_map_diagram_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C13 owns",
    "## 4. What C13 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Map/diagram family scope and classification",
    "## 7. C13 record grammar, doctrine-level only",
    "## 8. Donor map, diagram, keyed-area, symbol, label, layout, image, and field-name handling",
    "## 9. Location, scenario, hazard, vehicle/platform, faction, table, source-local, and visual-review handoffs",
    "## 10. C13 cross-family overlap rules",
    "## 11. Composite map/diagram record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C13 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C14",
]

HANDOFFS = [
    "C13 -> C01",
    "C13 -> C02",
    "C13 -> C03",
    "C13 -> C04",
    "C13 -> C05",
    "C13 -> C06",
    "C13 -> C07",
    "C13 -> C08",
    "C13 -> C09",
    "C13 -> C10",
    "C13 -> C11",
    "C13 -> C12",
    "C13 -> C14",
    "C13 -> pending_schema",
]

OVERLAPS = [
    "C13 vs C06",
    "C13 vs C07",
    "C13 vs C09",
    "C13 vs C08",
    "C13 vs C05/B09",
    "C13 vs C10",
    "C13 vs C14",
    "C13 vs runtime/backend",
    "C13 vs live-play/sourcebook",
    "C13 vs image/OCR/CV pipeline",
    "C13 vs C01/C02/C03/C04/C11/C12",
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


def c13_text() -> str:
    return read_utf8(C13_PATH)


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


def test_c13_file_exists_at_expected_path() -> None:
    assert C13_PATH.exists()
    assert C13_PATH.is_file()
    assert c13_text().strip()


def test_c13_required_sections_are_present() -> None:
    text = c13_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c13_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c13_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "maps, diagrams, annotations, keyed areas",
        "visual dependencies",
        "route diagrams",
        "ship/station layouts",
        "tactical diagrams",
        "symbolic diagrams",
        "image-review records",
        "spatial overlays",
        "visual evidence records",
        "annotation-provenance records",
        "classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final geography",
        "canon geography",
        "canon map truth",
        "visual truth without review",
        "runtime map state",
        "runtime navigation state",
        "runtime region state",
        "fog-of-war state",
        "player map state",
        "token state",
        "encounter map execution",
        "tactical-grid procedure",
        "travel procedure",
        "exploration procedure",
        "scene procedure",
        "hazard procedure",
        "gis geometry",
        "coordinate systems",
        "map scale doctrine",
        "hex-grid defaults",
        "zone-system defaults",
        "image generation",
        "ocr implementation",
        "computer vision implementation",
        "database map schemas",
        "backend map schemas",
        "sourcebook map prose",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
        "live-play behavior",
    ]:
        assert phrase in lowered


def test_c13_requires_c00_base_and_provenance_posture() -> None:
    text = c13_text()
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
        "not gis geometry",
        "not a final map schema",
        "not visual truth",
        "not sourcebook map prose",
        "not live map execution",
        "not canon geography",
    ]:
        assert marker in lowered


def test_c13_rejects_donor_map_diagram_visual_and_field_leakage() -> None:
    lowered = c13_text().lower()
    for marker in [
        "donor maps",
        "donor diagrams",
        "donor annotations",
        "donor keyed-area formats",
        "donor map symbols",
        "donor legends",
        "donor room keys",
        "donor coordinates",
        "donor map scales",
        "donor grid/hex/zone assumptions",
        "donor layout formats",
        "donor route diagrams",
        "donor ship/station layouts",
        "donor visual styles",
        "donor field names",
        "donor proper nouns",
        "named locations",
        "named regions",
        "named worlds",
        "named planes",
        "named ships",
        "named stations",
        "named factions",
        "protected artwork",
        "donor cosmology",
        "astra defaults",
    ]:
        assert marker in lowered


def test_c13_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    text = c13_text()
    lowered = text.lower()
    for marker in ["B08", "B01", "B10", "B02", "B09"]:
        assert marker in text
    for phrase in [
        "b08 is not c13 schema",
        "b01 is not c13 schema",
        "b10 is not c13 schema",
        "b02 is not c13 schema",
        "b09 is not c13 schema",
        "batch b procedure terms must not become c13 schema fields",
    ]:
        assert phrase in lowered


def test_c13_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c13_text()
    lowered = text.lower()
    for handoff in HANDOFFS:
        assert handoff in text
    assert "use references and satellite records, not inheritance or merged schemas" in lowered
    for overlap in OVERLAPS:
        assert overlap in text


def test_c13_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c13_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "legal/ip posture",
        "license-specific expressions",
        "protected art/map references",
        "protected artwork",
        "trade dress",
        "rejected donor element handling",
        "rejected_import",
        "rejected donor elements include donor maps",
        "donor source-specific visual meanings",
    ]:
        assert marker in lowered


def test_c13_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c13_text().lower()
    for marker in [
        "canon eligibility",
        "never promotes canon",
        "does not accept canon",
        "hidden-state and protected-truth boundary",
        "protected truth",
        "runtime map state",
        "runtime navigation state",
        "runtime region state",
        "fog-of-war state",
        "player map state",
        "token state",
        "encounter map execution",
        "live map execution",
        "navigation graphs",
        "save-state map nodes",
        "image asset database rows",
        "entity/component/event schemas",
        "command lifecycle",
        "context packets",
        "backend map schemas",
        "gis geometry",
        "ocr implementation",
        "computer vision implementation",
        "coordinate extraction",
        "image generation",
        "visual truth algorithms",
        "sourcebook map prose",
        "live-play visual state",
        "training examples",
    ]:
        assert marker in lowered


def test_c13_includes_good_and_bad_usage_examples() -> None:
    text = c13_text()
    lowered = text.lower()
    assert "Good C13 usage:" in text
    assert "Bad C13 usage:" in text
    for marker in [
        "preserve a donor dungeon map",
        "preserve a route diagram",
        "preserve a ship/station layout",
        "preserve a hazard overlay",
        "preserve a faction jurisdiction map",
        "convert donor coordinates",
        "treat donor map art",
        "visual truth without review",
        "turn a tactical diagram into encounter map execution",
        "implement ocr",
    ]:
        assert marker in lowered


def test_c13_registry_posture_is_draft_not_current_or_stable() -> None:
    assert _registry_scalar("C13", "status") == "draft"
    assert _registry_scalar("C13", "authority_level") == "schema-draft"
    assert _registry_scalar("C13", "test_status") == "designed"
    assert _registry_scalar("C13", "review_status") == "not_reviewed"
    assert _registry_scalar("C13", "blocked_by") == "[]"

    block = _registry_record_block("C13")
    for status in FORBIDDEN_PROMOTED_STATUSES:
        assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)
    for marker in ["stable_for_family", "stable_cross_family", "tested_minimum", "runtime-ready"]:
        assert marker not in block


def test_c13_does_not_promote_other_c_families_or_regress_existing_drafts() -> None:
    for file_id in ["C01", "C02", "C03", "C05", "C06", "C07", "C09", "C10"]:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    for file_id in ["C04", "C08", "C11", "C12", "C14"]:
        block = _registry_record_block(file_id)
        for status in FORBIDDEN_PROMOTED_STATUSES:
            assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)
        for marker in ["stable_for_family", "stable_cross_family", "tested_minimum", "runtime-ready"]:
            assert marker not in block
