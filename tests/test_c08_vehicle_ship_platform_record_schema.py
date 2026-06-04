import re

from tests.helpers import ROOT, read_utf8

C08_PATH = ROOT / "docs" / "doctrine" / "schema" / "C08_vehicle_ship_platform_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C08 owns",
    "## 4. What C08 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Vehicle/ship/platform family scope and classification",
    "## 7. C08 record grammar, doctrine-level only",
    "## 8. Donor vehicle, ship, mech, platform, station, frame, jump, module, hardpoint, cargo, crew, and field-name handling",
    "## 9. Travel, item, module, ability, actor, location, scenario, faction, hazard, table, map, source-local, and runtime-review handoffs",
    "## 10. C08 cross-family overlap rules",
    "## 11. Composite vehicle/ship/platform record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C08 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C11",
]

HANDOFFS = [
    "C08 -> C01",
    "C08 -> C02",
    "C08 -> C03",
    "C08 -> C04",
    "C08 -> C05",
    "C08 -> C06",
    "C08 -> C07",
    "C08 -> C09",
    "C08 -> C10",
    "C08 -> C11",
    "C08 -> C12",
    "C08 -> C13",
    "C08 -> C14",
    "C08 -> pending_schema",
]

OVERLAPS = [
    "C08 vs C06",
    "C08 vs C04",
    "C08 vs C02",
    "C08 vs C03",
    "C08 vs C09",
    "C08 vs C13",
    "C08 vs C05/B05",
    "C08 vs C07/B08/B10",
    "C08 vs C14",
    "C08 vs runtime/backend",
    "C08 vs live-play/sourcebook",
    "C08 vs donor source",
]

FORBIDDEN_PROMOTED_STATUSES = {"current", "tested_minimum", "stable_for_family", "stable_cross_family"}
EXISTING_DRAFT_C_FAMILIES = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C09", "C10", "C13", "C14"]


def c08_text() -> str:
    return read_utf8(C08_PATH)


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


def test_c08_file_exists_at_expected_path() -> None:
    assert C08_PATH.exists()
    assert C08_PATH.is_file()
    assert c08_text().strip()


def test_c08_required_sections_are_present() -> None:
    text = c08_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c08_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c08_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "vehicles, ships, starships, mechs, platforms, stations",
        "drone platforms",
        "bases, mobile bases",
        "modular platforms",
        "platform-scale systems",
        "conveyances",
        "mount-like platforms",
        "fleet units",
        "large persistent equipment-platform records",
        "vehicle/ship/platform classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final vehicle mechanics",
        "final starship mechanics",
        "final mech mechanics",
        "final platform mechanics",
        "movement math",
        "travel procedure",
        "navigation procedure",
        "chase procedure",
        "starship combat",
        "mech combat",
        "dogfighting rules",
        "ship-to-ship combat",
        "vehicle damage systems",
        "crew action economy",
        "station economy",
        "cargo economy",
        "fuel economy",
        "jump/ftl doctrine",
        "traveller jump default",
        "lancer frame default",
        "hardpoint mechanics",
        "module mechanics",
        "license mechanics",
        "frame mechanics",
        "mount rules",
        "vehicle scale math",
        "platform inventory state",
        "runtime vehicle state",
        "sourcebook vehicle prose",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
        "live-play behavior",
    ]:
        assert phrase in lowered


def test_c08_requires_c00_base_and_provenance_posture() -> None:
    text = c08_text()
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
        "review routing",
        "source-local boundary posture",
    ]:
        assert marker.lower() in lowered
    for marker in [
        "doctrine grammar only",
        "not a runtime schema",
        "not a database schema",
        "not a final vehicle statblock",
        "not a starship system",
        "not a mech system",
        "not a platform module system",
        "not a travel/navigation procedure",
        "not a combat procedure",
        "not a cargo/fuel economy",
        "not sourcebook vehicle prose",
    ]:
        assert marker in lowered


def test_c08_rejects_donor_vehicle_ship_platform_leakage() -> None:
    lowered = c08_text().lower()
    for marker in [
        "donor vehicle systems",
        "donor starship systems",
        "donor mech systems",
        "donor platform systems",
        "traveller jump default",
        "lancer frame/license defaults",
        "starfinder starship roles",
        "mechwarrior/battletech-like frame assumptions",
        "ship-to-ship combat defaults",
        "vehicle statblock defaults",
        "cargo/fuel economy defaults",
        "hardpoint defaults",
        "module-slot defaults",
        "donor field names",
        "donor proper nouns",
        "named vehicles/ships/mechs/stations/fleets/manufacturers/technologies",
        "donor-world assumptions",
        "as astra defaults",
    ]:
        assert marker in lowered
    for forbidden_value in [
        "final numerical values",
        "hull points",
        "armor",
        "structure",
        "speed",
        "thrust",
        "jump ratings",
        "range bands",
        "maneuver ratings",
        "fuel costs",
        "cargo capacity",
        "crew counts",
        "passenger capacity",
        "hardpoints",
        "module slots",
        "frame licenses",
        "mech size",
        "weapon mounts",
        "station scale",
        "damage thresholds",
        "repair dcs",
        "travel speeds",
        "navigation dcs",
        "upkeep costs",
        "acquisition costs",
        "vehicle prices",
        "cargo values",
        "vehicle scale math",
    ]:
        assert forbidden_value in lowered


def test_c08_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    lowered = c08_text().lower()
    for marker in [
        "c08 references b08",
        "b08 is not c08 schema",
        "c08 references b03",
        "b03 is not c08 schema",
        "c08 references b04",
        "b04 is not c08 schema",
        "c08 references b06",
        "b06 is not c08 schema",
        "c08 references b10",
        "b10 is not c08 schema",
        "c08 may reference b02",
        "b02 is not c08 schema",
        "batch b procedure terms must not become c08 schema fields",
        "doctrine-facing pressure only",
    ]:
        assert marker in lowered


def test_c08_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c08_text()
    for handoff in HANDOFFS:
        assert handoff in text
    for overlap in OVERLAPS:
        assert overlap in text
    assert "use references and satellite records, not inheritance or merged schemas" in text
    assert "inheritance_allowed: false" in text
    assert "Cross-family references do not make the target family inherit C08 grammar" in text


def test_c08_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c08_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "donor vehicle names",
        "ship names",
        "mech names",
        "station names",
        "named fleets",
        "named manufacturers",
        "named technologies",
        "donor ftl/jump laws",
        "source-specific frame systems",
        "source-specific vehicle lore",
        "protected proper nouns",
        "trademark-like terms",
        "license text",
        "verbatim-similarity risk",
        "donor-world assumptions",
        "rejected donor element handling",
        "rejected donor elements include donor vehicle systems",
        "prevents accidental import",
    ]:
        assert marker in lowered


def test_c08_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c08_text().lower()
    for marker in [
        "canon eligibility and review routing",
        "c08 never promotes canon",
        "does not accept canon",
        "hidden-state and protected-truth boundary",
        "must not expose protected truth",
        "runtime boundary",
        "runtime vehicle state",
        "runtime crew state",
        "runtime fuel state",
        "runtime cargo state",
        "runtime module state",
        "runtime station state",
        "runtime navigation state",
        "runtime map state",
        "equipment runtime",
        "save-state nodes",
        "database platform rows",
        "entity/component/event schemas",
        "command lifecycle",
        "context packets",
        "backend vehicle schemas",
        "backend navigation schemas",
        "live-play travel/starship/mech combat procedure",
        "canon/sourcebook/live-play/training boundary",
        "sourcebook vehicle prose",
        "live-play vehicle procedure",
    ]:
        assert marker in lowered


def test_c08_includes_good_and_bad_usage_examples() -> None:
    text = c08_text()
    assert "Good C08 usage:" in text
    assert "Bad C08 usage:" in text
    assert "Convert a donor starship-like entry" in text
    assert "Copy a donor vehicle statblock" in text


def test_c08_registry_posture_is_draft_not_current_or_stable() -> None:
    block = _registry_record_block("C08")
    assert _registry_scalar("C08", "status") == "draft"
    assert _registry_scalar("C08", "authority_level") == "schema-draft"
    assert _registry_scalar("C08", "test_status") == "designed"
    assert _registry_scalar("C08", "review_status") == "not_reviewed"
    assert _registry_scalar("C08", "status") not in FORBIDDEN_PROMOTED_STATUSES
    assert _registry_scalar("C08", "test_status") not in FORBIDDEN_PROMOTED_STATUSES
    assert "blocked_by: []" in block
    for forbidden in [
        "status: current",
        "stable_for_family",
        "stable_cross_family",
        "tested_minimum",
        "canon-current",
        "runtime-ready",
    ]:
        assert forbidden not in block


def test_c08_does_not_promote_other_c_families_or_regress_existing_drafts() -> None:
    for file_id in EXISTING_DRAFT_C_FAMILIES:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    for file_id in ["C11", "C12"]:
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
