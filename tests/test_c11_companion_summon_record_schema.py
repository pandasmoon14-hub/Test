import re

from tests.helpers import ROOT, read_utf8

C11_PATH = ROOT / "docs" / "doctrine" / "schema" / "C11_companion_summon_record_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C11 owns",
    "## 4. What C11 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Companion/summon family scope and classification",
    "## 7. C11 record grammar, doctrine-level only",
    "## 8. Donor companion, summon, pet, familiar, cohort, minion, drone, spirit, contract, bond, control, and field-name handling",
    "## 9. Actor, ability, faction, item, relic, vehicle/platform, scenario, recovery/training, social, hazard, table, map, source-local, and runtime-review handoffs",
    "## 10. C11 cross-family overlap rules",
    "## 11. Composite companion/summon record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C11 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C12",
]

HANDOFFS = [
    "C11 -> C01",
    "C11 -> C02",
    "C11 -> C03",
    "C11 -> C04",
    "C11 -> C05",
    "C11 -> C06",
    "C11 -> C07",
    "C11 -> C08",
    "C11 -> C09",
    "C11 -> C10",
    "C11 -> C12",
    "C11 -> C13",
    "C11 -> C14",
    "C11 -> pending_schema",
]

OVERLAPS = [
    "C11 vs C01",
    "C11 vs C03",
    "C11 vs C05/B09",
    "C11 vs C07",
    "C11 vs C08",
    "C11 vs C04",
    "C11 vs C12/B07",
    "C11 vs C09",
    "C11 vs C14",
    "C11 vs runtime/backend",
    "C11 vs live-play/sourcebook",
    "C11 vs donor source",
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

EXISTING_DRAFTS = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C13", "C14"]


def c11_text() -> str:
    return read_utf8(C11_PATH)


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


def test_c11_file_exists_at_expected_path() -> None:
    assert C11_PATH.exists()
    assert C11_PATH.is_file()
    assert c11_text().strip()


def test_c11_required_sections_are_present() -> None:
    text = c11_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c11_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c11_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "companions",
        "summons",
        "bonded beasts",
        "drone companions",
        "spirit allies",
        "contract entities",
        "familiar-like entities",
        "pets",
        "cohorts",
        "followers",
        "minions",
        "dependent actors",
        "controlled allies",
        "temporary allies",
        "bound entities",
        "relationship/control-dependent actor records",
        "classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final companion mechanics",
        "final summon mechanics",
        "pet rules",
        "familiar rules",
        "follower rules",
        "minion economy",
        "disposable summon default",
        "donor pet rules as canon",
        "animal-companion class mechanics",
        "summon duration math",
        "command action economy",
        "loyalty math",
        "bond math",
        "relationship math",
        "control math",
        "cohort progression",
        "minion scaling",
        "runtime companion state",
        "runtime summon state",
        "runtime control state",
        "runtime bond state",
        "runtime loyalty state",
        "runtime command state",
        "runtime follower roster",
        "sourcebook companion prose",
        "sourcebook summon lists",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
        "live-play behavior",
    ]:
        assert phrase in lowered


def test_c11_requires_c00_base_and_provenance_posture() -> None:
    text = c11_text()
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
        "not a final companion statblock",
        "not a summon system",
        "not a pet system",
        "not a follower roster",
        "not command/control state",
        "not relationship simulation",
        "not sourcebook companion prose",
    ]:
        assert marker in lowered


def test_c11_rejects_donor_companion_summon_pet_leakage() -> None:
    lowered = c11_text().lower()
    for marker in [
        "donor companion systems",
        "donor summon systems",
        "donor pet systems",
        "donor familiar systems",
        "donor cohort systems",
        "donor minion systems",
        "donor follower systems",
        "animal companion class mechanics",
        "disposable summon default",
        "donor pet rules as canon",
        "summon duration defaults",
        "command action defaults",
        "loyalty/bond mechanics",
        "control procedures",
        "donor field names",
        "donor proper nouns",
        "named companions/summons/pets/familiars/cohorts/spirits/contracts",
        "donor-world assumptions",
        "are not astra defaults",
    ]:
        assert marker in lowered


def test_c11_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    text = c11_text()
    lowered = text.lower()
    for marker in ["B01", "B02", "B07", "B09", "B03", "B10"]:
        assert marker in text
    for phrase in [
        "b01 is not c11 schema",
        "b02 is not c11 schema",
        "b07 is not c11 schema",
        "b09 is not c11 schema",
        "b03 is not c11 schema",
        "b10 is not c11 schema",
        "batch b procedure terms must not become c11 schema fields",
    ]:
        assert phrase in lowered


def test_c11_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c11_text()
    lowered = text.lower()
    for handoff in HANDOFFS:
        assert handoff in text
    assert "use references and satellite records, not inheritance or merged schemas" in lowered
    for overlap in OVERLAPS:
        assert overlap in text


def test_c11_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c11_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "source-local/legal/ip/c14 review",
        "legal/ip posture",
        "proper nouns",
        "named companions",
        "named summons",
        "named pets",
        "named familiars",
        "named cohorts",
        "named spirits",
        "named contracts",
        "donor-world species",
        "license-specific expressions",
        "verbatim-similar descriptions",
        "rejected donor element handling",
        "rejected_import",
        "donor companion systems",
        "donor source-specific prompt language",
    ]:
        assert marker in lowered


def test_c11_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c11_text().lower()
    for marker in [
        "canon eligibility",
        "never promotes canon",
        "does not accept canon",
        "hidden-state and protected-truth boundary",
        "protected truth",
        "runtime companion state",
        "runtime summon state",
        "runtime control state",
        "runtime bond state",
        "runtime loyalty state",
        "runtime command state",
        "runtime follower roster",
        "command queues",
        "relationship trackers",
        "loyalty trackers",
        "save-state nodes",
        "database companion rows",
        "entity/component/event schemas",
        "command lifecycle",
        "context packets",
        "backend companion schemas",
        "backend summon schemas",
        "live-play companion ai or command procedure",
        "sourcebook companion prose",
        "training examples",
    ]:
        assert marker in lowered


def test_c11_includes_good_and_bad_usage_examples() -> None:
    text = c11_text()
    lowered = text.lower()
    assert "Good C11 usage:" in text
    assert "Bad C11 usage:" in text
    for marker in [
        "preserve a donor bonded beast",
        "preserve a temporary summoned ally",
        "preserve a drone companion relationship record",
        "preserve a spirit contract",
        "convert donor pet rules into astra default pet slots",
        "convert donor summon durations into astra summon duration defaults",
        "turn a companion record into runtime companion state",
        "use donor companion/summon/pet/familiar/cohort/minion/control field names as c11 schema labels",
        "promote named companions",
    ]:
        assert marker in lowered


def test_c11_registry_posture_is_draft_not_current_or_stable() -> None:
    assert _registry_scalar("C11", "status") == "draft"
    assert _registry_scalar("C11", "authority_level") == "schema-draft"
    assert _registry_scalar("C11", "test_status") == "designed"
    assert _registry_scalar("C11", "review_status") == "not_reviewed"
    assert _registry_scalar("C11", "blocked_by") == "[]"

    block = _registry_record_block("C11")
    for status in FORBIDDEN_PROMOTED_STATUSES:
        assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", block, re.MULTILINE)
    for marker in ["stable_for_family", "stable_cross_family", "tested_minimum", "runtime-ready"]:
        assert marker not in block


def test_c11_does_not_promote_c12_or_regress_existing_drafts() -> None:
    for file_id in EXISTING_DRAFTS:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    c12_block = _registry_record_block("C12")
    for status in FORBIDDEN_PROMOTED_STATUSES:
        assert not re.search(rf"^  (status|authority_level|test_status|review_status): {status}$", c12_block, re.MULTILINE)
    for marker in [
        "stable_for_family",
        "stable_cross_family",
        "tested_minimum",
        "runtime-ready",
        "runtime_ready",
        "canon-promoted",
        "accepted_canon",
    ]:
        assert marker not in c12_block
