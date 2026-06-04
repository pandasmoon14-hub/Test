import re

from tests.helpers import ROOT, read_utf8

C03_PATH = ROOT / "docs" / "doctrine" / "schema" / "C03_ability_power_technique_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C03 owns",
    "## 4. What C03 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Ability/power/technique family scope and classification",
    "## 7. C03 record grammar, doctrine-level only",
    "## 8. Donor spell, feature, power, maneuver, technique, and field-name handling",
    "## 9. Action, cost, resource, damage, backlash, duration, recharge, and effect handoffs",
    "## 10. C03 cross-family overlap rules",
    "## 11. Composite ability/power/technique record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C03 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C09",
]

HANDOFFS = [
    "C03 -> C01",
    "C03 -> C02",
    "C03 -> C04",
    "C03 -> C05",
    "C03 -> C06",
    "C03 -> C07",
    "C03 -> C08",
    "C03 -> C09",
    "C03 -> C10",
    "C03 -> C11",
    "C03 -> C12",
    "C03 -> C13",
    "C03 -> C14",
    "C03 -> pending_schema",
]

OVERLAPS = [
    "C03 vs C01",
    "C03 vs C02",
    "C03 vs C04",
    "C03 vs C09",
    "C03 vs C11",
    "C03 vs C14",
    "C03 vs B02",
    "C03 vs Batch A resource/damage/effect owners",
]

FORBIDDEN_PROMOTED_STATUSES = {"current", "tested_minimum", "stable_for_family", "stable_cross_family"}


def c03_text() -> str:
    return read_utf8(C03_PATH)


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


def test_c03_file_exists_at_expected_path() -> None:
    assert C03_PATH.exists()
    assert C03_PATH.is_file()
    assert c03_text().strip()


def test_c03_required_sections_are_present() -> None:
    text = c03_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c03_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c03_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "abilities, powers, techniques, maneuvers, routines, invocations",
        "spell-like effects",
        "psionic effects",
        "active effects",
        "passive effects",
        "item-granted effects",
        "creature-granted capabilities",
        "classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final ability math",
        "action economy",
        "resource economy",
        "cost math",
        "damage math",
        "condition math",
        "duration math",
        "recharge rules",
        "cooldown rules",
        "backlash rules",
        "spell slots",
        "vancian casting",
        "power points",
        "ki/qi/essence economies",
        "class feature progression",
        "feat/talent systems",
        "runtime ability instances",
        "runtime cooldown state",
        "runtime buff/debuff state",
        "combat balance",
        "sourcebook power lists",
        "accepted lexicon",
        "canon acceptance",
        "live-play behavior",
    ]:
        assert phrase in lowered


def test_c03_requires_c00_base_and_provenance_posture() -> None:
    text = c03_text()
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
    assert "not a final ability statblock" in lowered
    assert "not a spell list" in lowered
    assert "not a class feature table" in lowered
    assert "not a technique list" in lowered
    assert "not sourcebook power prose" in lowered


def test_c03_rejects_donor_spell_power_technique_and_feature_leakage() -> None:
    lowered = c03_text().lower()
    for marker in [
        "donor spells",
        "donor spell lists",
        "donor class features",
        "donor feat/talent features",
        "donor maneuvers",
        "donor powers",
        "donor techniques",
        "donor power ranks",
        "donor spell levels",
        "donor slots",
        "vancian casting",
        "donor resource systems",
        "donor action economies",
        "donor damage/healing math",
        "donor save dcs",
        "donor ranges/areas/durations",
        "donor recharge/cooldown rules",
        "donor field names",
        "donor proper nouns",
        "donor cosmology",
        "as astra defaults",
    ]:
        assert marker in lowered
    for forbidden_mechanic in [
        "final numerical values",
        "action costs",
        "target counts",
        "ranges",
        "areas",
        "damage dice",
        "healing values",
        "save dcs",
        "attack bonuses",
        "spell levels",
        "class levels",
        "power ranks",
        "resource costs",
        "slot levels",
        "cooldowns",
        "charges",
        "duration counts",
        "condition severities",
        "critical rules",
        "scaling formulas",
        "effect math",
    ]:
        assert forbidden_mechanic in lowered


def test_c03_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    lowered = c03_text().lower()
    for marker in [
        "c03 references b02",
        "b02 is not c03 schema",
        "c03 references b10",
        "b10 is not c03 schema",
        "c03 may reference b01",
        "b01 is not c03 schema",
        "c03 may reference b03",
        "b03 is not c03 schema",
        "c03 may reference b07",
        "b07 is not c03 schema",
        "batch b procedure terms must not become c03 schema fields",
        "doctrine-facing pressure only",
    ]:
        assert marker in lowered


def test_c03_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c03_text()
    for handoff in HANDOFFS:
        assert handoff in text
    for overlap in OVERLAPS:
        assert overlap in text
    assert "C03 vs C05/C06/C07/C08/C10/C12/C13" in text
    assert "use references and satellite records, not inheritance or merged schemas" in text
    assert "inheritance_allowed: false" in text
    assert "Cross-family references do not make the target family inherit C03 grammar" in text
    assert "table rows do not become C03 records unless converted with provenance" in text


def test_c03_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c03_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "donor spell names",
        "class feature names",
        "named techniques",
        "trademark-like power names",
        "named schools",
        "named elements",
        "named deities",
        "named disciplines",
        "named factions",
        "named cosmology",
        "named source-specific metaphysics",
        "source-specific magic systems",
        "psionic systems",
        "cultivation systems",
        "rejected donor element handling",
        "rejected donor elements include donor spells",
        "prevents accidental import",
    ]:
        assert marker in lowered


def test_c03_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c03_text().lower()
    for marker in [
        "hidden-state and protected-truth boundary",
        "must not expose protected truth",
        "runtime boundary",
        "runtime ability instances",
        "runtime cooldown state",
        "runtime buff/debuff state",
        "entity/component schemas",
        "event schemas",
        "command lifecycle",
        "context packets",
        "save-state",
        "database contracts",
        "backend ability schemas",
        "combat trackers",
        "canon/sourcebook/live-play/training boundary",
        "c03 never promotes canon",
        "does not accept canon",
        "sourcebook power prose",
        "spell lists",
        "class feature tables",
        "technique lists",
        "live-play behavior",
    ]:
        assert marker in lowered


def test_c03_includes_good_and_bad_usage_examples() -> None:
    text = c03_text()
    assert "Good C03 usage:" in text
    assert "Bad C03 usage:" in text
    assert "Convert a donor ability-like entry" in text
    assert "Copy a donor spell list, class feature table" in text


def test_c03_registry_posture_is_draft_not_current_or_stable() -> None:
    block = _registry_record_block("C03")
    assert _registry_scalar("C03", "status") == "draft"
    assert _registry_scalar("C03", "authority_level") == "schema-draft"
    assert _registry_scalar("C03", "test_status") == "designed"
    assert _registry_scalar("C03", "review_status") == "not_reviewed"
    assert _registry_scalar("C03", "status") not in FORBIDDEN_PROMOTED_STATUSES
    assert _registry_scalar("C03", "test_status") not in FORBIDDEN_PROMOTED_STATUSES
    for forbidden in [
        "status: current",
        "stable_for_family",
        "stable_cross_family",
        "tested_minimum",
        "canon-current",
        "runtime-ready",
    ]:
        assert forbidden not in block


def test_c03_does_not_promote_c04_c14_or_regress_c01_c02() -> None:
    for file_id in ["C01", "C02"]:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    for file_id in [f"C{number:02d}" for number in range(4, 15)]:
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
