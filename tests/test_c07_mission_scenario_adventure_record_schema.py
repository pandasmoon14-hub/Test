import re

from tests.helpers import ROOT, read_utf8

C07_PATH = ROOT / "docs" / "doctrine" / "schema" / "C07_mission_scenario_adventure_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C07 owns",
    "## 4. What C07 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Mission/scenario/adventure family scope and classification",
    "## 7. C07 record grammar, doctrine-level only",
    "## 8. Donor adventure, quest, scene-chain, objective, reward, boxed-text, and field-name handling",
    "## 9. Scene, action, reward, travel, faction, hazard, table, location, and consequence handoffs",
    "## 10. C07 cross-family overlap rules",
    "## 11. Composite mission/scenario/adventure record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C07 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C05",
]

HANDOFFS = [
    "C07 -> C01",
    "C07 -> C02",
    "C07 -> C03",
    "C07 -> C04",
    "C07 -> C05",
    "C07 -> C06",
    "C07 -> C08",
    "C07 -> C09",
    "C07 -> C10",
    "C07 -> C11",
    "C07 -> C12",
    "C07 -> C13",
    "C07 -> C14",
    "C07 -> pending_schema",
]

OVERLAPS = [
    "C07 vs C06",
    "C07 vs C10",
    "C07 vs C05/B09",
    "C07 vs C09/B10",
    "C07 vs C01",
    "C07 vs C02/B05",
    "C07 vs C03/B02",
    "C07 vs C13",
    "C07 vs C14",
    "C07 vs runtime/backend",
    "C07 vs live-play/sourcebook",
    "C07 vs Batch A campaign/world/consequence owners",
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

DRAFT_C_FAMILIES = ["C01", "C02", "C03", "C06", "C09", "C10"]
NOT_PROMOTED_C_FAMILIES = ["C04", "C05", "C08", "C11", "C12", "C13", "C14"]


def c07_text() -> str:
    return read_utf8(C07_PATH)


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


def test_c07_file_exists_at_expected_path() -> None:
    assert C07_PATH.exists()
    assert C07_PATH.is_file()
    assert c07_text().strip()


def test_c07_required_sections_are_present() -> None:
    text = c07_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c07_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c07_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "missions",
        "scenarios",
        "adventures",
        "arcs",
        "hooks",
        "objectives",
        "scene-chains",
        "encounter-chains",
        "reward/consequence structures",
        "branching paths",
        "quest-like structures",
        "adventure-path fragments",
        "scripted scenario functions",
        "classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final adventure design",
        "scene procedure",
        "encounter procedure",
        "action procedure",
        "travel procedure",
        "social/faction procedure",
        "hazard procedure",
        "reward economy",
        "value flow",
        "encounter balance",
        "pacing math",
        "branching runtime logic",
        "railroad procedure",
        "player-choice constraint procedure",
        "runtime quest state",
        "runtime objective state",
        "runtime consequence state",
        "event logs",
        "canon events",
        "accepted canon timeline",
        "sourcebook adventure prose",
        "boxed text",
        "read-aloud text",
        "gm narration",
        "live-play behavior",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
    ]:
        assert phrase in lowered


def test_c07_requires_c00_base_and_provenance_posture() -> None:
    text = c07_text()
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
        "not a quest-state schema",
        "not a final adventure format",
        "not scene execution",
        "not encounter procedure",
        "not sourcebook adventure prose",
        "not boxed text",
        "not canon event timeline",
    ]:
        assert marker in lowered


def test_c07_rejects_donor_adventure_scenario_and_field_leakage() -> None:
    lowered = c07_text().lower()
    for marker in [
        "donor adventures",
        "donor scenario formats",
        "donor quest formats",
        "donor boxed text",
        "donor read-aloud prose",
        "donor scene numbers",
        "donor encounter numbers",
        "donor quest stages",
        "donor objective labels",
        "donor reward values",
        "donor xp awards",
        "donor treasure awards",
        "donor branch labels",
        "donor map keys",
        "donor pacing notes",
        "donor required outcomes",
        "donor railroad assumptions",
        "donor field names",
        "donor proper nouns",
        "named npcs",
        "named places",
        "named factions",
        "named events",
        "named timelines",
        "donor cosmology",
        "as astra defaults",
        "only as source evidence",
        "not as astra schema labels",
    ]:
        assert marker in lowered


def test_c07_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    text = c07_text()
    lowered = text.lower()
    for marker in ["B01", "B02", "B05", "B08", "B09", "B10"]:
        assert marker in text
    for marker in [
        "b01 is not c07 schema",
        "b02 is not c07 schema",
        "b05 is not c07 schema",
        "b08 is not c07 schema",
        "b09 is not c07 schema",
        "b10 is not c07 schema",
        "batch b procedure terms must not become c07 schema fields",
    ]:
        assert marker in lowered


def test_c07_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c07_text()
    lowered = text.lower()
    for handoff in HANDOFFS:
        assert handoff in text
    for overlap in OVERLAPS:
        assert overlap in text
    assert "routing references only" in lowered
    assert "do not allow inheritance from other c-family schemas" in lowered


def test_c07_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c07_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "legal/ip posture",
        "license-specific expressions",
        "verbatim-similar descriptions",
        "protected art/map references",
        "donor proper nouns",
        "source-specific scenario lore",
        "source-specific timeline",
        "rejected donor element handling",
        "rejected_import",
        "rejected donor elements include donor adventures",
        "donor source-specific prose",
    ]:
        assert marker in lowered


def test_c07_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c07_text().lower()
    for marker in [
        "canon eligibility",
        "never promotes canon",
        "does not accept canon",
        "hidden-state and protected-truth boundary",
        "protected truth",
        "runtime quest state",
        "runtime objective state",
        "runtime consequence state",
        "branch state",
        "event logs",
        "save-state nodes",
        "database quest rows",
        "entity/component/event schemas",
        "command lifecycle",
        "context packets",
        "backend quest schemas",
        "scenario execution engines",
        "encounter trackers",
        "live-play scripts",
        "sourcebook adventure prose",
        "training examples",
    ]:
        assert marker in lowered


def test_c07_includes_good_and_bad_usage_examples() -> None:
    text = c07_text()
    lowered = text.lower()
    assert "Good C07 usage:" in text
    assert "Bad C07 usage:" in text
    for marker in [
        "preserve a donor rescue mission",
        "preserve a donor heist hook",
        "preserve a route-based adventure fragment",
        "preserve a faction job",
        "convert donor quest stages into an astra runtime quest state machine",
        "treat donor scene numbers",
        "use donor adventure/quest/scenario field names as c07 schema labels",
    ]:
        assert marker in lowered


def test_c07_registry_posture_is_draft_not_current_or_stable() -> None:
    assert _registry_scalar("C07", "status") == "draft"
    assert _registry_scalar("C07", "authority_level") == "schema-draft"
    assert _registry_scalar("C07", "test_status") == "designed"
    assert _registry_scalar("C07", "review_status") == "not_reviewed"
    assert _registry_scalar("C07", "blocked_by") == "[]"

    block = _registry_record_block("C07")
    for status in FORBIDDEN_PROMOTED_STATUSES:
        assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)
    for marker in ["stable_for_family", "stable_cross_family", "tested_minimum", "runtime-ready"]:
        assert marker not in block


def test_c07_does_not_promote_other_c_families_or_regress_existing_drafts() -> None:
    for file_id in DRAFT_C_FAMILIES:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    for file_id in NOT_PROMOTED_C_FAMILIES:
        block = _registry_record_block(file_id)
        for status in FORBIDDEN_PROMOTED_STATUSES:
            assert not re.search(
                rf"^  (status|authority_level|test_status|review_status): {status}$",
                block,
                re.MULTILINE,
            )
        for marker in ["stable_for_family", "stable_cross_family", "tested_minimum", "runtime-ready", "runtime_ready"]:
            assert marker not in block
