import re

from tests.helpers import ROOT, read_utf8

C12_PATH = ROOT / "docs" / "doctrine" / "schema" / "C12_crafting_salvage_recipe_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C12 owns",
    "## 4. What C12 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Crafting/salvage/recipe family scope and classification",
    "## 7. C12 record grammar, doctrine-level only",
    "## 8. Donor crafting, salvage, repair, recipe, installation, modification, extraction, requisition, blueprint, schematic, economy, and field-name handling",
    "## 9. Item, relic, platform, companion, location, faction, acquisition, project, hazard, table, map, source-local, and runtime-review handoffs",
    "## 10. C12 cross-family overlap rules",
    "## 11. Composite crafting/salvage/recipe record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C12 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to Batch C capstone/readiness gate",
]

HANDOFFS = [
    "C12 -> C01",
    "C12 -> C02",
    "C12 -> C03",
    "C12 -> C04",
    "C12 -> C05",
    "C12 -> C06",
    "C12 -> C07",
    "C12 -> C08",
    "C12 -> C09",
    "C12 -> C10",
    "C12 -> C11",
    "C12 -> C13",
    "C12 -> C14",
    "C12 -> pending_schema",
]

OVERLAPS = [
    "C12 vs C02",
    "C12 vs C04",
    "C12 vs C08",
    "C12 vs C11/B07",
    "C12 vs B06",
    "C12 vs B05",
    "C12 vs C09",
    "C12 vs C10",
    "C12 vs C13",
    "C12 vs C14",
    "C12 vs runtime/backend",
    "C12 vs live-play/sourcebook",
    "C12 vs donor source",
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

EXISTING_DRAFTS = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C13", "C14"]


def c12_text() -> str:
    return read_utf8(C12_PATH)


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


def test_c12_file_exists_at_expected_path() -> None:
    assert C12_PATH.exists()
    assert C12_PATH.is_file()
    assert c12_text().strip()


def test_c12_required_sections_are_present() -> None:
    text = c12_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c12_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c12_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "crafting records",
        "salvage records",
        "repair records",
        "recipe records",
        "installation-process records",
        "modification-process records",
        "extraction records",
        "requisition-process evidence records",
        "blueprints",
        "schematics",
        "formulas",
        "upgrade processes",
        "refit processes",
        "recovery processes",
        "material-processing records",
        "resource-extraction records",
        "transformation-process records",
        "crafting/salvage/recipe classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final crafting mechanics",
        "final salvage mechanics",
        "repair procedure",
        "installation procedure",
        "requisition procedure",
        "acquisition procedure",
        "project procedure",
        "downtime procedure",
        "training procedure",
        "research procedure",
        "reward economy",
        "item economy",
        "material economy",
        "crafting economy",
        "salvage economy",
        "donor crafting economy default",
        "value-flow procedure",
        "recipe canon acceptance",
        "final recipe list",
        "sourcebook crafting prose",
        "sourcebook recipe catalog",
        "runtime crafting state",
        "runtime project state",
        "runtime recipe state",
        "runtime inventory state",
        "runtime installation state",
        "runtime repair state",
        "runtime salvage state",
        "runtime requisition state",
        "database recipe rows",
        "backend crafting schemas",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
        "live-play behavior",
    ]:
        assert phrase in lowered


def test_c12_requires_c00_base_and_provenance_posture() -> None:
    text = c12_text()
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
        "not final crafting procedure",
        "not salvage economy",
        "not repair procedure",
        "not installation procedure",
        "not requisition procedure",
        "not project tracker",
        "not sourcebook recipe prose",
        "not canon recipe acceptance",
        "C12CraftingSalvageRecipeRecord",
    ]:
        assert marker.lower() in lowered


def test_c12_rejects_donor_crafting_salvage_recipe_leakage() -> None:
    lowered = c12_text().lower()
    for marker in [
        "donor crafting systems",
        "donor salvage systems",
        "donor repair systems",
        "donor installation procedures",
        "donor extraction procedures",
        "donor requisition systems",
        "donor crafting economies",
        "donor material economies",
        "donor item-price economies",
        "donor downtime systems",
        "donor recipe catalogs",
        "donor blueprint systems",
        "donor upgrade-slot systems",
        "donor crafting economy defaults",
        "donor costs",
        "donor yields",
        "donor dcs",
        "donor project clocks",
        "donor field names",
        "donor proper nouns",
        "named recipes/materials/blueprints/technologies/production laws",
        "donor-world assumptions",
        "becoming astra defaults",
    ]:
        assert marker in lowered


def test_c12_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    text = c12_text()
    lowered = text.lower()
    for marker in ["B06", "B05", "B03", "B04", "B07", "B08", "B10"]:
        assert marker in text
    for phrase in [
        "b06 is not c12 schema",
        "b05 is not c12 schema",
        "b03 is not c12 schema",
        "b04 is not c12 schema",
        "b07 is not c12 schema",
        "b08 is not c12 schema",
        "b10 is not c12 schema",
        "batch b procedure terms must not become c12 schema fields",
    ]:
        assert phrase in lowered


def test_c12_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c12_text()
    lowered = text.lower()
    for handoff in HANDOFFS:
        assert handoff in text
    assert "use references and satellite records, not inheritance or merged schemas" in lowered
    for overlap in OVERLAPS:
        assert overlap in text


def test_c12_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c12_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "legal/ip posture",
        "proper nouns",
        "protected recipe names",
        "formula names",
        "blueprint names",
        "schematic names",
        "named materials",
        "named technologies",
        "donor-world production laws",
        "source-specific crafting traditions",
        "license-specific expressions",
        "verbatim-similar descriptions",
        "rejected donor element handling",
        "rejected_import",
        "donor source-specific prompt language",
    ]:
        assert marker in lowered


def test_c12_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c12_text().lower()
    for marker in [
        "canon eligibility",
        "never promotes canon",
        "does not accept canon",
        "hidden-state and protected-truth boundary",
        "protected truth",
        "runtime crafting state",
        "runtime project state",
        "runtime recipe state",
        "runtime inventory state",
        "runtime installation state",
        "runtime repair state",
        "runtime salvage state",
        "runtime requisition state",
        "project trackers",
        "crafting queues",
        "save-state nodes",
        "database recipe rows",
        "entity/component/event schemas",
        "command lifecycle",
        "context packets",
        "backend crafting schemas",
        "backend inventory schemas",
        "live-play crafting/project execution",
        "sourcebook recipe prose",
        "sourcebook recipe catalog",
        "training examples",
    ]:
        assert marker in lowered


def test_c12_includes_good_and_bad_usage_examples() -> None:
    text = c12_text()
    lowered = text.lower()
    assert "Good C12 usage:" in text
    assert "Bad C12 usage:" in text
    for marker in [
        "preserve a donor crafting recipe",
        "preserve a salvage procedure",
        "preserve a ship refit blueprint",
        "preserve a companion bonding ritual",
        "convert donor crafting costs",
        "convert donor salvage tables",
        "turn a process record into runtime crafting state",
        "use donor crafting/salvage/recipe/repair/economy field names as c12 schema labels",
        "promote named recipes",
    ]:
        assert marker in lowered


def test_c12_registry_posture_is_draft_not_current_or_stable() -> None:
    assert _registry_scalar("C12", "status") == "draft"
    assert _registry_scalar("C12", "authority_level") == "schema-draft"
    assert _registry_scalar("C12", "test_status") == "designed"
    assert _registry_scalar("C12", "review_status") == "not_reviewed"
    assert _registry_scalar("C12", "blocked_by") == "[]"

    block = _registry_record_block("C12")
    for status in FORBIDDEN_PROMOTED_STATUSES:
        assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)
    for marker in [
        "stable_for_family",
        "stable_cross_family",
        "tested_minimum",
        "runtime-ready",
        "runtime_ready",
        "canon-promoted",
        "accepted_canon",
    ]:
        assert marker not in block


def test_c12_does_not_regress_existing_c_family_drafts() -> None:
    for file_id in EXISTING_DRAFTS:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"
        block = _registry_record_block(file_id)
        for status in FORBIDDEN_PROMOTED_STATUSES:
            assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)
        for marker in ["stable_for_family", "stable_cross_family", "tested_minimum", "runtime-ready", "runtime_ready"]:
            assert marker not in block
