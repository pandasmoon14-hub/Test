import re

from tests.helpers import ROOT, read_utf8

C02_PATH = ROOT / "docs" / "doctrine" / "schema" / "C02_item_gear_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C02 owns",
    "## 4. What C02 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Item/gear family scope and classification",
    "## 7. C02 record grammar, doctrine-level only",
    "## 8. Donor item-table, equipment-entry, and field-name handling",
    "## 9. Use, custody, acquisition, value, crafting, salvage, repair, and upgrade handoffs",
    "## 10. C02 cross-family overlap rules",
    "## 11. Composite item/gear record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C02 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C03",
]

HANDOFFS = [
    "C02 -> C01",
    "C02 -> C03",
    "C02 -> C04",
    "C02 -> C05",
    "C02 -> C06",
    "C02 -> C07",
    "C02 -> C08",
    "C02 -> C09",
    "C02 -> C10",
    "C02 -> C12",
    "C02 -> C13",
    "C02 -> C14",
    "C02 -> pending_schema",
]

OVERLAPS = [
    "C02 vs C04",
    "C02 vs C12",
    "C02 vs C03",
    "C02 vs C08",
    "C02 vs C01",
    "C02 vs C05/B05",
    "C02 vs C09",
    "C02 vs C14",
]

FORBIDDEN_PROMOTED_STATUSES = {"current", "tested_minimum", "stable_for_family", "stable_cross_family"}


def c02_text() -> str:
    return read_utf8(C02_PATH)


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


def test_c02_file_exists_at_expected_path() -> None:
    assert C02_PATH.exists()
    assert C02_PATH.is_file()
    assert c02_text().strip()


def test_c02_required_sections_are_present() -> None:
    text = c02_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c02_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c02_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "practical item, gear, tool, weapon, armor, consumable, kit, equipment",
        "portable object",
        "carried object",
        "enhanced gear pending review",
        "donor item-table containment as evidence",
        "donor equipment-entry containment as evidence",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final equipment math",
        "combat balance",
        "economy balance",
        "price curves",
        "rarity math",
        "load math",
        "inventory state",
        "runtime custody state",
        "runtime item ids",
        "database contracts",
        "shop systems",
        "loot systems",
        "crafting procedure",
        "salvage procedure",
        "repair procedure",
        "upgrade procedure",
        "requisition procedure",
        "acquisition procedure",
        "sourcebook gear tables",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
        "live-play behavior",
    ]:
        assert phrase in lowered


def test_c02_requires_c00_base_and_provenance_posture() -> None:
    text = c02_text()
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
    assert "not a final item statblock" in lowered
    assert "not an equipment table" in lowered
    assert "not sourcebook gear prose" in lowered


def test_c02_rejects_donor_item_table_and_field_leakage() -> None:
    lowered = c02_text().lower()
    for marker in [
        "donor item tables",
        "donor equipment entries",
        "donor field names",
        "donor item categories",
        "donor math",
        "donor prices",
        "donor rarity",
        "donor weight/bulk/encumbrance",
        "donor damage/armor values",
        "donor charges/ammunition/durability",
        "donor crafting costs",
        "donor upgrade slots/hardpoints",
        "donor economy assumptions",
        "donor proper nouns",
        "as astra defaults",
    ]:
        assert marker in lowered
    for forbidden_mechanic in [
        "damage",
        "armor",
        "defense",
        "weight",
        "encumbrance",
        "bulk",
        "price",
        "rarity",
        "item level",
        "attunement",
        "charges",
        "ammunition",
        "durability",
        "repair dc",
        "crafting cost",
        "upgrade slots",
        "hardpoints",
        "capacity",
        "consumable counts",
        "equipment math",
    ]:
        assert forbidden_mechanic in lowered


def test_c02_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    lowered = c02_text().lower()
    for marker in [
        "c02 references b03",
        "b03 is not c02 schema",
        "c02 references b04",
        "b04 is not c02 schema",
        "c02 references b05",
        "b05 is not c02 schema",
        "c02 references b06",
        "b06 is not c02 schema",
        "b03 procedure terms must not become c02 schema fields",
        "b04 custody/burden procedure terms must not become c02 schema fields",
        "b05 value-flow, economy, reward, or requisition procedure terms must not become c02 schema fields",
        "b06 project/crafting/salvage/repair/upgrade procedure terms must not become c02 schema fields",
        "b01/b02 are not c02 schema fields",
    ]:
        assert marker in lowered


def test_c02_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c02_text()
    for handoff in HANDOFFS:
        assert handoff in text
    for overlap in OVERLAPS:
        assert overlap in text
    assert "C02 vs C06/C07/C10/C13" in text
    assert "use references and satellite records, not inheritance or merged schemas" in text
    assert "inheritance_allowed: false" in text
    assert "Vehicle-mounted gear should use references, not inheritance" in text
    assert "Do not embed donor weapon actions, spell effects, powers, item charges, or passive effects" in text


def test_c02_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c02_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "donor item names",
        "named artifacts",
        "trademark-like labels",
        "named materials",
        "named factions",
        "named locations",
        "named technologies",
        "named manufacturers",
        "named cosmology",
        "source-specific item lore",
        "source-specific item law",
        "rejected donor element handling",
        "rejected donor elements include donor item tables",
        "prevents accidental import",
    ]:
        assert marker in lowered


def test_c02_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c02_text().lower()
    for marker in [
        "hidden-state and protected-truth boundary",
        "must not expose protected truth",
        "runtime boundary",
        "runtime inventory state",
        "entity/component schemas",
        "event schemas",
        "command lifecycle",
        "context packets",
        "save-state",
        "database contracts",
        "shop systems",
        "loot systems",
        "backend item schemas",
        "canon/sourcebook/live-play/training boundary",
        "c02 never promotes canon",
        "does not accept canon",
        "sourcebook gear tables",
        "equipment tables",
        "live-play equipment behavior",
    ]:
        assert marker in lowered


def test_c02_includes_good_and_bad_usage_examples() -> None:
    text = c02_text()
    assert "Good C02 usage:" in text
    assert "Bad C02 usage:" in text
    assert "Convert a donor item-like entry" in text
    assert "Copy a donor item table with price, rarity, weight" in text


def test_c02_registry_posture_is_draft_not_current_or_stable() -> None:
    block = _registry_record_block("C02")
    assert _registry_scalar("C02", "status") == "draft"
    assert _registry_scalar("C02", "authority_level") == "schema-draft"
    assert _registry_scalar("C02", "test_status") == "designed"
    assert _registry_scalar("C02", "review_status") == "not_reviewed"
    assert _registry_scalar("C02", "status") not in FORBIDDEN_PROMOTED_STATUSES
    assert _registry_scalar("C02", "test_status") not in FORBIDDEN_PROMOTED_STATUSES
    for forbidden in [
        "status: current",
        "stable_for_family",
        "stable_cross_family",
        "tested_minimum",
        "canon-current",
        "runtime-ready",
    ]:
        assert forbidden not in block


def test_c02_does_not_promote_c03_c14_or_regress_c01() -> None:
    assert _registry_scalar("C01", "status") == "draft"
    assert _registry_scalar("C01", "authority_level") == "schema-draft"
    assert _registry_scalar("C01", "test_status") == "designed"
    assert _registry_scalar("C01", "review_status") == "not_reviewed"

    for file_id in [f"C{number:02d}" for number in range(3, 15)]:
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
