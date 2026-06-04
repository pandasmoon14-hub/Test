import re

from tests.helpers import ROOT, read_utf8

C01_PATH = ROOT / "docs" / "doctrine" / "schema" / "C01_creature_npc_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C01 owns",
    "## 4. What C01 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Creature/NPC family scope and classification",
    "## 7. C01 record grammar, doctrine-level only",
    "## 8. Donor statblock and donor field-name handling",
    "## 9. Actor capability, ability, item, hazard, faction, location, and scenario handoffs",
    "## 10. C01 cross-family overlap rules",
    "## 11. Composite creature record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C01 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C02",
]

HANDOFFS = [
    "C01 -> C02",
    "C01 -> C03",
    "C01 -> C04",
    "C01 -> C05",
    "C01 -> C06",
    "C01 -> C07",
    "C01 -> C09",
    "C01 -> C10",
    "C01 -> C11",
    "C01 -> C13",
    "C01 -> C14",
    "C01 -> pending_schema",
]

OVERLAPS = ["C01 vs C11", "C01 vs C03", "C01 vs C09", "C01 vs C07", "C01 vs C14"]

FORBIDDEN_PROMOTED_STATUSES = {"current", "tested_minimum", "stable_for_family", "stable_cross_family"}


def c01_text() -> str:
    return read_utf8(C01_PATH)


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


def test_c01_file_exists_at_expected_path() -> None:
    assert C01_PATH.exists()
    assert C01_PATH.is_file()
    assert c01_text().strip()


def test_c01_required_sections_are_present() -> None:
    text = c01_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c01_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c01_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "creatures, npcs, adversaries, monsters, spirits, ai actors, swarms",
        "non-player beings",
        "actor-like constructs",
        "donor-statblock containment as evidence",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final math",
        "combat balance",
        "runtime actor state",
        "encounter procedure",
        "action procedure",
        "live-play behavior",
        "sourcebook prose",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
    ]:
        assert phrase in lowered


def test_c01_requires_c00_base_and_provenance_posture() -> None:
    text = c01_text()
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
        "legal/ip posture",
    ]:
        assert marker.lower() in lowered
    assert "doctrine grammar only" in lowered
    assert "not a runtime schema" in lowered
    assert "not a database schema" in lowered
    assert "not a final statblock format" in lowered
    assert "not sourcebook statblock prose" in lowered


def test_c01_rejects_donor_statblock_and_donor_field_leakage() -> None:
    lowered = c01_text().lower()
    for marker in [
        "donor statblock formats",
        "donor field names",
        "donor math",
        "donor challenge ratings",
        "donor cr",
        "donor xp",
        "donor hit points",
        "donor hp equivalents",
        "donor armor classes",
        "donor ac equivalents",
        "donor action economies",
        "donor saving throw formats",
        "donor senses formats",
        "donor skill lists",
        "donor spell lists",
        "donor action lists",
        "donor alignment/cosmology",
        "donor proper nouns",
        "as astra defaults",
    ]:
        assert marker in lowered
    for forbidden_mechanic in [
        "hit points",
        "armor",
        "defense",
        "challenge rating",
        "proficiency",
        "level",
        "initiative",
        "damage dice",
        "legendary actions",
        "lair actions",
        "monster math",
    ]:
        assert forbidden_mechanic in lowered


def test_c01_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c01_text()
    for handoff in HANDOFFS:
        assert handoff in text
    for overlap in OVERLAPS:
        assert overlap in text
    assert "use references and satellite records, not inheritance or merged schemas" in text
    assert "inheritance_allowed: false" in text
    assert "split into C01, C03, and C11 references" in text
    assert "Do not embed donor spell/action lists as C01 schema" in text


def test_c01_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c01_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "proper nouns",
        "named species",
        "named gods",
        "named worlds",
        "named factions",
        "named locations",
        "named cosmology",
        "rejected donor element handling",
        "rejected donor elements include donor field names",
        "prevents accidental import",
    ]:
        assert marker in lowered


def test_c01_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c01_text().lower()
    for marker in [
        "hidden-state and protected-truth boundary",
        "must not expose protected truth",
        "runtime boundary",
        "runtime actor state",
        "entity/component schemas",
        "event schemas",
        "command lifecycle",
        "context packets",
        "save-state",
        "database contracts",
        "canon/sourcebook/live-play/training boundary",
        "c01 never promotes canon",
        "does not accept canon",
        "does not write final bestiary entries",
        "live-play statblocks",
    ]:
        assert marker in lowered


def test_c01_includes_good_and_bad_usage_examples() -> None:
    text = c01_text()
    assert "Good C01 usage:" in text
    assert "Bad C01 usage:" in text
    assert "Convert a donor monster-like entity" in text
    assert "Copy a donor statblock with HP, AC, CR" in text


def test_c01_registry_posture_is_draft_not_current_or_stable() -> None:
    block = _registry_record_block("C01")
    assert _registry_scalar("C01", "status") == "draft"
    assert _registry_scalar("C01", "authority_level") == "schema-draft"
    assert _registry_scalar("C01", "test_status") == "designed"
    assert _registry_scalar("C01", "review_status") == "not_reviewed"
    assert _registry_scalar("C01", "status") not in FORBIDDEN_PROMOTED_STATUSES
    assert _registry_scalar("C01", "test_status") not in FORBIDDEN_PROMOTED_STATUSES
    for forbidden in [
        "status: current",
        "stable_for_family",
        "stable_cross_family",
        "tested_minimum",
        "canon-current",
        "runtime-ready",
    ]:
        assert forbidden not in block


def test_c01_does_not_promote_c02_c14() -> None:
    for file_id in [f"C{number:02d}" for number in range(2, 15)]:
        assert _registry_record_block(file_id)
        assert _registry_scalar(file_id, "status") not in FORBIDDEN_PROMOTED_STATUSES
        assert _registry_scalar(file_id, "authority_level") != "schema-current"
        assert _registry_scalar(file_id, "test_status") not in FORBIDDEN_PROMOTED_STATUSES
