import re

from tests.helpers import ROOT, read_utf8

C05_PATH = ROOT / "docs" / "doctrine" / "schema" / "C05_faction_institution_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C05 owns",
    "## 4. What C05 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Faction/institution family scope and classification",
    "## 7. C05 record grammar, doctrine-level only",
    "## 8. Donor faction, institution, reputation, standing, rank, relationship, and field-name handling",
    "## 9. Social, acquisition, location, scenario, actor, item, hazard, table, and source-local handoffs",
    "## 10. C05 cross-family overlap rules",
    "## 11. Composite faction/institution record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C05 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C13",
]

HANDOFFS = [
    "C05 -> C01",
    "C05 -> C02",
    "C05 -> C03",
    "C05 -> C04",
    "C05 -> C06",
    "C05 -> C07",
    "C05 -> C08",
    "C05 -> C09",
    "C05 -> C10",
    "C05 -> C11",
    "C05 -> C12",
    "C05 -> C13",
    "C05 -> C14",
    "C05 -> pending_schema",
]

OVERLAPS = [
    "C05 vs C07",
    "C05 vs B09",
    "C05 vs B05",
    "C05 vs C01",
    "C05 vs C06",
    "C05 vs C10",
    "C05 vs C14",
    "C05 vs runtime/backend",
    "C05 vs live-play/sourcebook",
    "C05 vs Batch A campaign/world/social/consequence owners",
    "C05 vs C02/C03/C04/C08/C09/C11/C12/C13",
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

EXISTING_DRAFT_C_FAMILIES = ["C01", "C02", "C03", "C06", "C07", "C09", "C10"]
NOT_PROMOTED_C_FAMILIES = ["C04", "C08", "C11", "C12", "C13", "C14"]


def c05_text() -> str:
    return read_utf8(C05_PATH)


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


def test_c05_file_exists_at_expected_path() -> None:
    assert C05_PATH.exists()
    assert C05_PATH.is_file()
    assert c05_text().strip()


def test_c05_required_sections_are_present() -> None:
    text = c05_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c05_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c05_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "factions",
        "institutions",
        "sects",
        "guilds",
        "corporations",
        "empires",
        "courts",
        "cults",
        "orders",
        "governments",
        "authorities",
        "organizations",
        "rank structures",
        "standing/reputation structures",
        "relationship structures",
        "patronage structures",
        "jurisdictions",
        "allegiances",
        "institutional roles",
        "classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final faction mechanics",
        "final social procedure",
        "final reputation math",
        "final standing math",
        "faction clock procedure",
        "runtime faction clocks",
        "runtime faction state",
        "faction ai",
        "relationship ai",
        "institutional simulation",
        "faction turn procedure",
        "diplomacy procedure",
        "social encounter procedure",
        "acquisition/requisition procedure",
        "reward economy",
        "jurisdiction enforcement procedure",
        "canon faction histories",
        "accepted canon politics",
        "sourcebook faction prose",
        "live-play behavior",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
    ]:
        assert phrase in lowered


def test_c05_requires_c00_base_and_provenance_posture() -> None:
    text = c05_text()
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
        "not a faction-clock schema",
        "not a reputation system",
        "not a relationship simulation",
        "not final social mechanics",
        "not sourcebook faction prose",
        "not canon political history",
    ]:
        assert marker in lowered


def test_c05_rejects_donor_faction_institution_and_field_leakage() -> None:
    lowered = c05_text().lower()
    for marker in [
        "donor exact faction structures",
        "donor institution formats",
        "donor reputation systems",
        "donor standing systems",
        "donor rank structures",
        "donor relationship scores",
        "donor faction clocks",
        "donor influence/favor values",
        "donor faction turns",
        "donor patron rules",
        "donor membership benefits",
        "donor requisition rules",
        "donor reaction tables",
        "donor organization charts",
        "donor field names",
        "donor proper nouns",
        "named factions",
        "named institutions",
        "named leaders",
        "named histories",
        "named wars",
        "named cultures",
        "named locations",
        "named gods",
        "named cosmology",
        "donor cosmology",
        "not as astra schema labels or final mechanics",
        "as astra defaults",
    ]:
        assert marker in lowered


def test_c05_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    text = c05_text()
    lowered = text.lower()
    for marker in ["C05 references B09", "C05 references B05", "C05 references B08", "C05 references B10"]:
        assert marker in text
    for marker in ["C05 may reference B01", "C05 may reference B02"]:
        assert marker in text
    for marker in [
        "b09 is not c05 schema",
        "b05 is not c05 schema",
        "b08 is not c05 schema",
        "b10 is not c05 schema",
        "b01 is not c05 schema",
        "b02 is not c05 schema",
        "batch b procedure terms must not become c05 schema fields",
    ]:
        assert marker in lowered


def test_c05_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c05_text()
    lowered = text.lower()
    for handoff in HANDOFFS:
        assert handoff in text
    assert "use references and satellite records, not inheritance or merged schemas" in lowered
    assert "must use references and provenance rather than c05 inheritance or merged schemas" in lowered


def test_c05_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    text = c05_text()
    lowered = text.lower()
    assert "Source-local and legal/IP handling" in text
    assert "Rejected donor element handling" in text
    for marker in [
        "source_local_boundary",
        "legal/ip posture",
        "source-local/legal/ip/c14 review",
        "c14/source-local/legal/ip review",
        "rejected_donor_elements",
        "rejected donor element",
        "audit evidence",
        "does not authorize silent import",
    ]:
        assert marker in lowered


def test_c05_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c05_text().lower()
    for marker in [
        "canon eligibility is a review signal only",
        "never promotes canon",
        "does not accept canon",
        "hidden-state and protected-truth boundary",
        "not runtime hidden-information state",
        "runtime faction state",
        "runtime faction clocks",
        "relationship trackers",
        "diplomacy trackers",
        "save-state nodes",
        "database faction rows",
        "entity/component/event schemas",
        "command lifecycle",
        "context packets",
        "backend faction schemas",
        "institutional simulation",
        "faction ai",
        "live-play social behavior",
        "not canon/sourcebook/live-play/training authority",
        "sourcebook faction prose",
        "canon political history",
    ]:
        assert marker in lowered


def test_c05_includes_good_and_bad_usage_examples() -> None:
    text = c05_text()
    lowered = text.lower()
    assert "Good C05 usage:" in text
    assert "Bad C05 usage:" in text
    for marker in [
        "preserve a donor guild",
        "preserve a donor reputation track",
        "preserve a patron institution",
        "preserve a government jurisdiction claim",
        "convert donor rank names",
        "treat a donor faction",
        "use donor faction/institution/reputation/standing/rank/relationship/patron/requisition/reaction/organization-chart field names",
        "turn social/faction/contact/institutional interaction procedure",
    ]:
        assert marker in lowered


def test_c05_registry_posture_is_draft_not_current_or_stable() -> None:
    assert _registry_scalar("C05", "status") == "draft"
    assert _registry_scalar("C05", "authority_level") == "schema-draft"
    assert _registry_scalar("C05", "test_status") == "designed"
    assert _registry_scalar("C05", "review_status") == "not_reviewed"
    assert _registry_scalar("C05", "blocked_by") == "[]"

    block = _registry_record_block("C05")
    for status in FORBIDDEN_PROMOTED_STATUSES:
        assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)


def test_c05_does_not_promote_other_c_families_or_regress_existing_drafts() -> None:
    for file_id in EXISTING_DRAFT_C_FAMILIES:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    for file_id in NOT_PROMOTED_C_FAMILIES:
        block = _registry_record_block(file_id)
        for status in FORBIDDEN_PROMOTED_STATUSES:
            assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)
        for marker in ["stable_for_family", "stable_cross_family", "tested_minimum", "runtime-ready"]:
            assert marker not in block
