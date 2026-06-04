import re

from tests.helpers import ROOT, read_utf8

C06_PATH = ROOT / "docs" / "doctrine" / "schema" / "C06_location_site_region_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C06 owns",
    "## 4. What C06 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Location/site/region family scope and classification",
    "## 7. C06 record grammar, doctrine-level only",
    "## 8. Donor map, keyed-area, gazetteer, planar-location, region, and field-name handling",
    "## 9. Travel, exploration, scene, faction, hazard, map, scenario, and source-local handoffs",
    "## 10. C06 cross-family overlap rules",
    "## 11. Composite location/site/region record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C06 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C07",
]

HANDOFFS = [
    "C06 -> C01",
    "C06 -> C02",
    "C06 -> C03",
    "C06 -> C04",
    "C06 -> C05",
    "C06 -> C07",
    "C06 -> C08",
    "C06 -> C09",
    "C06 -> C10",
    "C06 -> C11",
    "C06 -> C12",
    "C06 -> C13",
    "C06 -> C14",
    "C06 -> pending_schema",
]

OVERLAPS = [
    "C06 vs C13",
    "C06 vs C09",
    "C06 vs C07",
    "C06 vs C14",
    "C06 vs C08",
    "C06 vs C05/B09",
    "C06 vs C10/B08",
    "C06 vs runtime/backend",
    "C06 vs Batch A cosmology/world/domain owners",
    "C06 vs B01/B02/B08/B10",
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

FUTURE_C_FAMILIES = ["C04", "C05", "C07", "C08", "C11", "C12", "C13", "C14"]
DRAFT_C_FAMILIES = ["C01", "C02", "C03", "C09", "C10"]


def c06_text() -> str:
    return read_utf8(C06_PATH)


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


def test_c06_file_exists_at_expected_path() -> None:
    assert C06_PATH.exists()
    assert C06_PATH.is_file()
    assert c06_text().strip()


def test_c06_required_sections_are_present() -> None:
    text = c06_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c06_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c06_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "locations",
        "sites",
        "regions",
        "worlds",
        "planes",
        "stations",
        "ruins",
        "megastructures",
        "settlements",
        "biomes",
        "route contexts",
        "keyed areas",
        "spatial containers",
        "place-like constructs",
        "classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final geography",
        "canon map truth",
        "canon geography",
        "accepted setting geography",
        "sourcebook gazetteer prose",
        "runtime map state",
        "runtime navigation state",
        "runtime region state",
        "fog-of-war state",
        "travel procedure",
        "exploration procedure",
        "discovery procedure",
        "scene procedure",
        "encounter procedure",
        "hazard mechanics",
        "environmental damage mechanics",
        "faction control mechanics",
        "settlement economy",
        "route generation",
        "database map schemas",
        "gis-like geometry",
        "coordinate systems",
        "hex-grid defaults",
        "zone system defaults",
        "keyed-map execution",
        "live-play behavior",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
    ]:
        assert phrase in lowered


def test_c06_requires_c00_base_and_provenance_posture() -> None:
    text = c06_text()
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
        "not a map schema",
        "not gis geometry",
        "not final geography",
        "not sourcebook gazetteer prose",
        "not keyed-map execution",
        "not canon geography",
    ]:
        assert marker in lowered


def test_c06_rejects_donor_map_location_and_field_leakage() -> None:
    lowered = c06_text().lower()
    for marker in [
        "donor maps",
        "donor map formats",
        "donor gazetteer formats",
        "donor keyed-area formats",
        "donor room keys",
        "donor coordinates",
        "donor map scales",
        "donor distances",
        "donor travel times",
        "donor encounter rates",
        "donor region modifiers",
        "donor hex/zone assumptions",
        "donor planar traits",
        "donor field names",
        "donor proper nouns",
        "named worlds",
        "named planes",
        "named regions",
        "named cities",
        "donor cosmology",
        "as astra defaults",
    ]:
        assert marker in lowered


def test_c06_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    text = c06_text()
    lowered = text.lower()
    for marker in ["B08", "B01", "B10", "B09", "B05", "B02"]:
        assert marker in text
    for phrase in [
        "b08 is not c06 schema",
        "b01 is not c06 schema",
        "b10 is not c06 schema",
        "b09 is not c06 schema",
        "b05 is not c06 schema",
        "b02 is not c06 schema",
        "batch b procedure terms must not become c06 schema fields",
    ]:
        assert phrase in lowered


def test_c06_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c06_text()
    lowered = text.lower()
    for handoff in HANDOFFS:
        assert handoff in text
    assert "use references and satellite records, not inheritance or merged schemas" in lowered
    for overlap in OVERLAPS:
        assert overlap in text


def test_c06_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c06_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "legal/ip posture",
        "license-specific expressions",
        "verbatim-similar descriptions",
        "protected art/map references",
        "donor proper nouns",
        "source-specific geography",
        "source-specific metaphysics",
        "rejected donor element handling",
        "rejected_import",
        "rejected donor elements include donor maps",
        "donor source-specific map prose",
    ]:
        assert marker in lowered


def test_c06_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c06_text().lower()
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
        "location database rows",
        "navigation graphs",
        "save-state map nodes",
        "gis geometry",
        "entity/component/event schemas",
        "command lifecycle",
        "context packets",
        "backend map schemas",
        "travel trackers",
        "exploration trackers",
        "live map execution",
        "sourcebook gazetteer prose",
        "training examples",
    ]:
        assert marker in lowered


def test_c06_includes_good_and_bad_usage_examples() -> None:
    text = c06_text()
    lowered = text.lower()
    assert "Good C06 usage:" in text
    assert "Bad C06 usage:" in text
    for marker in [
        "preserve a donor ruin",
        "preserve a route context",
        "preserve a settlement",
        "preserve a named plane",
        "convert donor coordinates",
        "treat a donor map as canon geography",
        "use donor map/location/gazetteer/keyed-area field names as c06 schema labels",
    ]:
        assert marker in lowered


def test_c06_registry_posture_is_draft_not_current_or_stable() -> None:
    assert _registry_scalar("C06", "status") == "draft"
    assert _registry_scalar("C06", "authority_level") == "schema-draft"
    assert _registry_scalar("C06", "test_status") == "designed"
    assert _registry_scalar("C06", "review_status") == "not_reviewed"
    assert _registry_scalar("C06", "blocked_by") == "[]"

    block = _registry_record_block("C06")
    for status in FORBIDDEN_PROMOTED_STATUSES:
        assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)


def test_c06_does_not_promote_other_c_families_or_regress_c01_c02_c03_c09_c10() -> None:
    for file_id in DRAFT_C_FAMILIES:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    for file_id in FUTURE_C_FAMILIES:
        block = _registry_record_block(file_id)
        for status in FORBIDDEN_PROMOTED_STATUSES:
            assert not re.search(
                rf"^  (status|authority_level|test_status|review_status): {status}$",
                block,
                re.MULTILINE,
            )
