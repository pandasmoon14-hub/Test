import re

from tests.helpers import ROOT, read_utf8

C14_PATH = ROOT / "docs" / "doctrine" / "schema" / "C14_source_local_setting_cosmology_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C14 owns",
    "## 4. What C14 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Source-local setting/cosmology family scope and classification",
    "## 7. C14 record grammar, doctrine-level only",
    "## 8. Donor proper noun, setting, cosmology, metaphysics, local law, history, culture, and field-name handling",
    "## 9. Canon eligibility, source-local containment, legal/IP, lexicon, and cross-family handoffs",
    "## 10. C14 cross-family overlap rules",
    "## 11. Composite source-local record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C14 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to Batch C remaining families or Batch C capstone",
]

HANDOFFS = [
    "C14 -> C01",
    "C14 -> C02",
    "C14 -> C03",
    "C14 -> C04",
    "C14 -> C05",
    "C14 -> C06",
    "C14 -> C07",
    "C14 -> C08",
    "C14 -> C09",
    "C14 -> C10",
    "C14 -> C11",
    "C14 -> C12",
    "C14 -> C13",
    "C14 -> pending_schema",
]

OVERLAPS = [
    "C14 vs all C01-C13",
    "C14 vs canon review",
    "C14 vs lexicon governance",
    "C14 vs legal/IP review",
    "C14 vs runtime/backend",
    "C14 vs live-play/sourcebook",
    "C14 vs Batch A doctrine",
    "C14 vs donor source",
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

EXISTING_DRAFT_C_FAMILIES = ["C01", "C02", "C03", "C05", "C06", "C07", "C09", "C10", "C13"]
UNPROMOTED_PENDING_FAMILIES = ["C04", "C08", "C11", "C12"]


def c14_text() -> str:
    return read_utf8(C14_PATH)


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


def test_c14_file_exists_at_expected_path() -> None:
    assert C14_PATH.exists()
    assert C14_PATH.is_file()
    assert c14_text().strip()


def test_c14_required_sections_are_present() -> None:
    text = c14_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c14_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c14_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "source-local setting records",
        "cosmology records",
        "metaphysics records",
        "proper noun records",
        "local law records",
        "local faction context records",
        "local culture records",
        "local history records",
        "named entity records",
        "named world records",
        "named plane records",
        "named deity records",
        "donor-world assumption records",
        "source-specific identity records",
        "source-specific lore records",
        "world-specific containment records",
        "containment and review routing",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "canon acceptance",
        "canon promotion",
        "astra-wide cosmology",
        "astra-wide metaphysics",
        "final setting law",
        "final sourcebook lore",
        "accepted canon history",
        "accepted canon geography",
        "final lexicon",
        "runtime world state",
        "runtime cosmology state",
        "runtime faction state",
        "runtime deity state",
        "sourcebook prose",
        "live-play behavior",
        "donor setting import",
        "donor cosmology import",
        "donor metaphysics import",
        "donor pantheon import",
        "donor proper noun import",
        "donor field names as astra defaults",
    ]:
        assert phrase in lowered


def test_c14_requires_c00_base_and_provenance_posture() -> None:
    text = c14_text()
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
        "not a canon setting model",
        "not sourcebook lore",
        "not lexicon acceptance",
        "not astra-wide cosmology",
        "not final metaphysics",
        "not donor setting import",
    ]:
        assert marker in lowered


def test_c14_rejects_donor_source_local_setting_cosmology_and_proper_noun_leakage() -> None:
    lowered = c14_text().lower()
    for marker in [
        "donor proper nouns",
        "donor setting law",
        "donor cosmology",
        "donor metaphysics",
        "donor pantheons",
        "donor named worlds",
        "donor named planes",
        "donor named gods",
        "donor named factions",
        "donor named cultures",
        "donor named histories",
        "donor named wars",
        "donor named events",
        "donor named places",
        "donor named species",
        "donor named schools",
        "donor named magic systems",
        "donor named technologies",
        "donor field names",
        "donor identity fields",
        "donor alignment/cosmology labels",
        "donor world assumptions",
        "astra defaults",
    ]:
        assert marker in lowered
    assert "explicitly blocks source-local material from becoming astra baseline" in lowered


def test_c14_routes_cross_family_handoffs_without_schema_inheritance() -> None:
    text = c14_text()
    lowered = text.lower()
    for handoff in HANDOFFS:
        assert handoff in text
    for overlap in OVERLAPS:
        assert overlap in text
    assert "not schema inheritance" in lowered
    assert "not inheritance or merged schemas" in lowered


def test_c14_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c14_text().lower()
    for phrase in [
        "source-local and legal/ip handling",
        "source-local boundaries",
        "legal/ip review notes",
        "legal/ip posture",
        "does not decide legal clearance",
        "rejected donor element handling",
        "rejected donor elements remain linked to source evidence",
        "rejection is not deletion",
        "blocks donor leakage into astra defaults",
    ]:
        assert phrase in lowered


def test_c14_preserves_canon_review_lexicon_runtime_and_batch_a_boundaries() -> None:
    lowered = c14_text().lower()
    for phrase in [
        "canon eligibility and review routing without canon promotion",
        "does not promote canon",
        "does not accept lexicon entries or create astra vocabulary",
        "preserves legal/ip posture and source-local boundaries",
        "runtime/backend owners decide later",
        "cannot override batch a ontology",
        "astra-wide metaphysical constraints",
        "source-local containment, or rejected material until canon promotion",
    ]:
        assert phrase in lowered


def test_c14_preserves_runtime_sourcebook_live_play_boundaries() -> None:
    lowered = c14_text().lower()
    for phrase in [
        "runtime world state",
        "runtime cosmology state",
        "runtime faction state",
        "runtime deity state",
        "lore database rows",
        "save-state nodes",
        "context packets",
        "hidden-state packets",
        "entity/component/event schemas",
        "command lifecycle",
        "backend lore schemas",
        "canon setting models",
        "live-play world truth",
        "hidden-state and protected-truth boundary",
        "protected truth must remain protected",
        "not canon sourcebook lore",
        "not sourcebook setting presentation",
        "not live-play behavior",
    ]:
        assert phrase in lowered


def test_c14_includes_good_and_bad_usage_examples() -> None:
    text = c14_text()
    lowered = text.lower()
    assert "Good C14 usage:" in text
    assert "Bad C14 usage:" in text
    for phrase in [
        "preserve a donor named world as source evidence",
        "preserve a donor pantheon as a c14 containment record",
        "preserve a local faction custom",
        "promote donor named worlds",
        "define astra-wide cosmology",
        "treat legal/ip review notes",
    ]:
        assert phrase in lowered


def test_c14_registry_posture_is_draft_not_current_or_stable() -> None:
    assert _registry_scalar("C14", "status") == "draft"
    assert _registry_scalar("C14", "authority_level") == "schema-draft"
    assert _registry_scalar("C14", "test_status") == "designed"
    assert _registry_scalar("C14", "review_status") == "not_reviewed"
    assert re.search(r"^  blocked_by: \[\]$", _registry_record_block("C14"), flags=re.MULTILINE)

    c14_block = _registry_record_block("C14")
    for forbidden in FORBIDDEN_PROMOTED_STATUSES:
        assert not re.search(rf"^  (status|authority_level|test_status|review_status): {re.escape(forbidden)}$", c14_block, flags=re.MULTILINE)


def test_c14_does_not_promote_other_c_families_or_regress_existing_drafts() -> None:
    for file_id in EXISTING_DRAFT_C_FAMILIES:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    for file_id in UNPROMOTED_PENDING_FAMILIES:
        block = _registry_record_block(file_id)
        for forbidden in FORBIDDEN_PROMOTED_STATUSES:
            assert not re.search(rf"^  (status|authority_level|test_status|review_status): {re.escape(forbidden)}$", block, flags=re.MULTILINE)
