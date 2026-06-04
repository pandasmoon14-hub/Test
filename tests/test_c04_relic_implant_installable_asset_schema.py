import re

from tests.helpers import ROOT, read_utf8

C04_PATH = ROOT / "docs" / "doctrine" / "schema" / "C04_relic_implant_installable_asset_schema.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What C04 owns",
    "## 4. What C04 must not own",
    "## 5. C00 inheritance and required base posture",
    "## 6. Relic/implant/installable asset family scope and classification",
    "## 7. C04 record grammar, doctrine-level only",
    "## 8. Donor relic, implant, cyberware, biotech, attunement, license, socket, module, upgrade, and field-name handling",
    "## 9. Item, ability, host, installation, crafting, acquisition, vehicle/platform, source-local, and legal/IP handoffs",
    "## 10. C04 cross-family overlap rules",
    "## 11. Composite relic/implant/installable asset record handling",
    "## 12. Parent, child, and satellite record handling",
    "## 13. Source-local and legal/IP handling",
    "## 14. Rejected donor element handling",
    "## 15. Canon eligibility and review routing",
    "## 16. Confidence, validation, and escalation routing",
    "## 17. Hidden-state and protected-truth boundary",
    "## 18. Runtime boundary",
    "## 19. Canon/sourcebook/live-play/training boundary",
    "## 20. Missing-schema fallback",
    "## 21. Examples of good and bad C04 usage",
    "## 22. Minimum tests or assertions",
    "## 23. Acceptance criteria",
    "## 24. Follow-up handoff to C08",
]

HANDOFFS = [
    "C04 -> C01",
    "C04 -> C02",
    "C04 -> C03",
    "C04 -> C05",
    "C04 -> C06",
    "C04 -> C07",
    "C04 -> C08",
    "C04 -> C09",
    "C04 -> C10",
    "C04 -> C11",
    "C04 -> C12",
    "C04 -> C13",
    "C04 -> C14",
    "C04 -> pending_schema",
]

OVERLAPS = [
    "C04 vs C02",
    "C04 vs C03",
    "C04 vs C12/B06",
    "C04 vs C08",
    "C04 vs C01",
    "C04 vs C05/B05",
    "C04 vs C09",
    "C04 vs C14",
    "C04 vs runtime/backend",
    "C04 vs live-play/sourcebook",
    "C04 vs donor source",
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


def c04_text() -> str:
    return read_utf8(C04_PATH)


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


def test_c04_file_exists_at_expected_path() -> None:
    assert C04_PATH.exists()
    assert C04_PATH.is_file()
    assert c04_text().strip()


def test_c04_required_sections_are_present() -> None:
    text = c04_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_c04_declares_owner_scope_and_non_owner_boundaries() -> None:
    lowered = c04_text().lower()
    for phrase in [
        "conversion-stage record-family grammar",
        "relics, implants, cyberware, biotech",
        "attunement-like assets",
        "bonded assets",
        "installed modules",
        "socketed assets",
        "augmentations",
        "host-integrated assets",
        "upgradeable special assets",
        "symbiotes",
        "prosthetics",
        "vehicle/platform modules",
        "classification and routing posture",
    ]:
        assert phrase in lowered

    for phrase in [
        "final mechanics",
        "final relic mechanics",
        "final implant math",
        "cyberware economy",
        "biotech economy",
        "essence systems",
        "cyberpsychosis systems",
        "attunement rules",
        "license rules",
        "pilot-license rules",
        "lancer license default",
        "shadowrun essence default",
        "slot mechanics",
        "socket mechanics",
        "upgrade slot mechanics",
        "hardpoint mechanics",
        "installation procedure",
        "removal procedure",
        "surgery procedure",
        "repair procedure",
        "upgrade procedure",
        "runtime installation state",
        "runtime body-slot state",
        "runtime attunement state",
        "runtime license state",
        "runtime module state",
        "runtime host-integration state",
        "combat balance",
        "sourcebook relic prose",
        "sourcebook implant prose",
        "accepted lexicon",
        "canon acceptance",
        "canon promotion",
        "live-play behavior",
    ]:
        assert phrase in lowered


def test_c04_requires_c00_base_and_provenance_posture() -> None:
    text = c04_text()
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
        "not a final relic statblock",
        "not an implant system",
        "not a cyberware system",
        "not an attunement system",
        "not a license system",
        "not an upgrade-slot system",
        "not an installation-state schema",
        "not sourcebook item prose",
    ]:
        assert marker in lowered


def test_c04_rejects_donor_relic_implant_installable_asset_leakage() -> None:
    lowered = c04_text().lower()
    for marker in [
        "donor relic systems",
        "donor implant systems",
        "donor cyberware systems",
        "donor biotech systems",
        "donor attunement rules",
        "donor license rules",
        "shadowrun essence default",
        "cyberpunk humanity/cyberpsychosis defaults",
        "lancer license default",
        "d&d attunement default",
        "donor slot/hardpoint/socket systems",
        "donor upgrade slots",
        "donor installation procedures",
        "donor surgery procedures",
        "donor costs",
        "donor resource math",
        "donor field names",
        "donor proper nouns",
        "named artifacts",
        "named modules",
        "named implant traditions",
        "named technology laws",
        "donor-world assumptions",
        "as astra defaults",
    ]:
        assert marker in lowered

    for marker in [
        "essence_cost",
        "humanity loss",
        "cyberpsychosis thresholds",
        "attunement limits",
        "license levels",
        "body slots",
        "hardpoints",
        "sockets",
        "upgrade slots",
        "module capacity",
    ]:
        assert marker in lowered


def test_c04_routes_batch_b_handoffs_without_schema_inheritance() -> None:
    text = c04_text()
    lowered = text.lower()
    for marker in ["B03", "B04", "B05", "B06", "B02"]:
        assert marker in text
    for phrase in [
        "b03 is not c04 schema",
        "b04 is not c04 schema",
        "b05 is not c04 schema",
        "b06 is not c04 schema",
        "b02 is not c04 schema",
        "batch b procedure terms must not become c04 schema fields",
        "doctrine-facing pressure only",
    ]:
        assert phrase in lowered


def test_c04_routes_cross_family_handoffs_without_inheritance() -> None:
    text = c04_text()
    for handoff in HANDOFFS:
        assert handoff in text
    for overlap in OVERLAPS:
        assert overlap in text
    lowered = text.lower()
    assert "cross-family references do not imply inheritance" in lowered
    assert "inheritance_allowed: false" in text


def test_c04_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    lowered = c04_text().lower()
    for marker in [
        "source-local and legal/ip handling",
        "protected names",
        "named artifacts",
        "named modules",
        "named implant traditions",
        "cyberware traditions",
        "biotech traditions",
        "donor-world technology law",
        "source-specific metaphysics",
        "proper nouns",
        "protected art",
        "diagrams",
        "schematics",
        "source-specific license systems",
        "c14 containment",
        "legal/ip review",
        "rejected donor element handling",
        "rejected_donor_elements",
        "cannot become astra schema",
    ]:
        assert marker in lowered


def test_c04_preserves_runtime_canon_sourcebook_live_play_boundaries() -> None:
    lowered = c04_text().lower()
    for marker in [
        "canon eligibility",
        "review routing",
        "does not grant canon acceptance",
        "canon promotion",
        "hidden-state and protected-truth boundary",
        "runtime boundary",
        "runtime installation state",
        "runtime body-slot state",
        "runtime attunement state",
        "runtime license state",
        "runtime module state",
        "runtime host-integration state",
        "equipment runtime",
        "save-state nodes",
        "database asset rows",
        "entity/component/event schemas",
        "command lifecycle",
        "context packets",
        "backend equipment schemas",
        "backend implant schemas",
        "live-play installation procedure",
        "not player-facing relic prose",
        "not implant catalog prose",
        "not sourcebook item presentation",
        "not training example authority",
    ]:
        assert marker in lowered


def test_c04_includes_good_and_bad_usage_examples() -> None:
    lowered = c04_text().lower()
    assert "good c04 usage" in lowered
    assert "bad c04 usage" in lowered
    for marker in [
        "donor cybernetic eye",
        "cursed relic sword",
        "mech-mounted experimental module",
        "biotech symbiote",
        "copying shadowrun essence costs",
        "copying cyberpunk humanity loss",
        "treating d&d attunement limits or lancer license levels as astra defaults",
        "making a c04 record into sourcebook implant prose",
    ]:
        assert marker in lowered


def test_c04_registry_posture_is_draft_not_current_or_stable() -> None:
    assert _registry_scalar("C04", "status") == "draft"
    assert _registry_scalar("C04", "authority_level") == "schema-draft"
    assert _registry_scalar("C04", "test_status") == "designed"
    assert _registry_scalar("C04", "review_status") == "not_reviewed"
    block = _registry_record_block("C04")
    assert "blocked_by: []" in block
    for forbidden in FORBIDDEN_PROMOTED_STATUSES:
        assert _registry_scalar("C04", "status") != forbidden
        assert _registry_scalar("C04", "test_status") != forbidden
    for marker in [
        "current: true",
        "stable_for_family: true",
        "stable_cross_family: true",
        "tested_minimum: true",
        "runtime_ready: true",
        "runtime-ready: true",
        "canon: true",
    ]:
        assert marker not in block


def test_c04_does_not_promote_other_c_families_or_regress_existing_drafts() -> None:
    for file_id in ["C01", "C02", "C03", "C05", "C06", "C07", "C09", "C10", "C13", "C14"]:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"

    # Future C08/C11/C12 PRs may intentionally draft those families. This test
    # only guards against accidental current/tested/stable/runtime/canon promotion.
    for file_id in ["C08", "C11", "C12"]:
        block = _registry_record_block(file_id).lower()
        assert _registry_scalar(file_id, "status") not in FORBIDDEN_PROMOTED_STATUSES
        assert _registry_scalar(file_id, "test_status") not in FORBIDDEN_PROMOTED_STATUSES
        for marker in [
            "current: true",
            "stable_for_family: true",
            "stable_cross_family: true",
            "tested_minimum: true",
            "runtime_ready: true",
            "runtime-ready: true",
            "canon: true",
        ]:
            assert marker not in block
