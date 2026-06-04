import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

CAPSTONE_PATH = ROOT / "docs" / "doctrine" / "schema" / "Batch_C_schema_family_integration_conflict_audit_and_readiness_gate.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Repository posture after C01-C14",
    "## 3. Batch C readiness definition",
    "## 4. What this capstone owns",
    "## 5. What this capstone must not own",
    "## 6. C00 inheritance audit",
    "## 7. C-family registry posture audit",
    "## 8. Cross-family owner boundary audit",
    "## 9. Required overlap matrix audit",
    "## 10. Parent/child/satellite/composite record audit",
    "## 11. Source-local and legal/IP audit",
    "## 12. Rejected donor element audit",
    "## 13. Donor leakage audit",
    "## 14. pending_schema discipline audit",
    "## 15. Confidence, validation, and review-routing audit",
    "## 16. Hidden-state and protected-truth audit",
    "## 17. Batch B handoff audit",
    "## 18. Runtime/backend boundary audit",
    "## 19. Canon/sourcebook/live-play/training boundary audit",
    "## 20. Testing posture audit",
    "## 21. Brittle-test and future-addition risk audit",
    "## 22. Deferred gap ledger",
    "## 23. Batch C readiness verdict",
    "## 24. Acceptance criteria",
    "## 25. Handoff to next schema/math/mechanics workstream",
]

C_FAMILY_FILES = {
    "C01": "C01_creature_npc_record_schema.md",
    "C02": "C02_item_gear_record_schema.md",
    "C03": "C03_ability_power_technique_record_schema.md",
    "C04": "C04_relic_implant_installable_asset_schema.md",
    "C05": "C05_faction_institution_record_schema.md",
    "C06": "C06_location_site_region_record_schema.md",
    "C07": "C07_mission_scenario_adventure_record_schema.md",
    "C08": "C08_vehicle_ship_platform_record_schema.md",
    "C09": "C09_hazard_environment_record_schema.md",
    "C10": "C10_table_oracle_record_schema.md",
    "C11": "C11_companion_summon_record_schema.md",
    "C12": "C12_crafting_salvage_recipe_record_schema.md",
    "C13": "C13_map_diagram_record_schema.md",
    "C14": "C14_source_local_setting_cosmology_record_schema.md",
}

C_FAMILY_LABELS = [
    "C01 creature/NPC",
    "C02 item/gear",
    "C03 ability/power/technique",
    "C04 relic/implant/installable asset",
    "C05 faction/institution",
    "C06 location/site/region",
    "C07 mission/scenario/adventure",
    "C08 vehicle/ship/platform",
    "C09 hazard/environment",
    "C10 table/oracle",
    "C11 companion/summon",
    "C12 crafting/salvage/recipe",
    "C13 map/diagram annotation",
    "C14 source-local setting/cosmology",
    "pending_schema",
]

OVERLAP_PAIRS = [
    "C01 vs C11",
    "C02 vs C04",
    "C02 vs C12",
    "C03 vs C04",
    "C05 vs C07",
    "C06 vs C13",
    "C06 vs C09",
    "C07 vs C10",
    "C08 vs C02/C04/C09",
    "C09 vs C10",
    "C14 vs every other family",
    "C04 vs C12",
    "C08 vs C13",
    "C11 vs C03",
    "C12 vs B06/B05",
]

DEFERRED_GAPS = [
    "final mechanics and math",
    "runtime/backend schema",
    "entity/component/event/command lifecycle",
    "context packet/save-state/database contracts",
    "canon promotion",
    "sourcebook prose",
    "live-play/GM behavior",
    "training/evaluation packs",
    "accepted lexicon promotion",
    "damage/resource/action-economy math",
    "economy/value/requisition math",
    "vehicle/starship/mech combat math",
    "companion/summon control mechanics",
    "crafting/salvage/recipe economy math",
    "map/GIS/coordinate/runtime navigation systems",
    "hidden-state management and protected-truth runtime handling",
    "corpus-scale pilot conversion validation",
]

FORBIDDEN_PROMOTED_STATUSES = {
    "current",
    "canon",
    "accepted_canon",
    "runtime-ready",
    "runtime_ready",
    "stable_for_family",
    "stable_cross_family",
    "tested_minimum",
}


def capstone_text() -> str:
    return read_utf8(CAPSTONE_PATH)


def _registry_record_block(file_id: str) -> str:
    registry_text = read_utf8(REGISTRY_PATH)
    match = re.search(
        rf"^- file_id: {re.escape(file_id)}\n(?P<block>.*?)(?=^- file_id: |\Z)",
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


def test_batch_c_capstone_file_exists() -> None:
    assert CAPSTONE_PATH.exists()
    assert CAPSTONE_PATH.is_file()
    assert capstone_text().strip()


def test_batch_c_capstone_required_sections_are_present() -> None:
    text = capstone_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_batch_c_capstone_declares_readiness_not_canon_runtime_or_sourcebook() -> None:
    text = capstone_text()
    lower_text = text.lower()
    assert "audit/readiness/control file" in lower_text
    assert "not a c-family schema" in lower_text
    assert "does not mean canon readiness" in lower_text
    for marker in [
        "sourcebook readiness",
        "runtime readiness",
        "final mechanics readiness",
        "live-play readiness",
        "training-corpus readiness",
    ]:
        assert marker in lower_text


def test_batch_c_capstone_lists_all_c_families_and_pending_schema() -> None:
    text = capstone_text()
    for label in C_FAMILY_LABELS:
        assert label in text


def test_batch_c_capstone_requires_c00_inheritance_and_provenance_posture() -> None:
    text = capstone_text()
    for marker in [
        "Every durable C-family record must inherit/include `AstraContentRecordBase`",
        "C00 bypass risk is prohibited",
        "provenance",
        "source evidence",
        "construct refs",
        "outcome refs",
        "source-local boundary",
        "rejected donor elements",
        "canon eligibility",
        "confidence/review/validation routing",
        "lineage/composition/cross-reference",
        "legal/IP posture",
    ]:
        assert marker in text


def test_batch_c_capstone_audits_registry_without_promotion() -> None:
    text = capstone_text()
    lower_text = text.lower()
    assert "registry posture" in lower_text
    assert "c01-c14 must remain draft/schema-draft/designed/not_reviewed" in lower_text
    for status in FORBIDDEN_PROMOTED_STATUSES:
        assert status in text
    assert "must not be promoted by this capstone" in lower_text
    assert "newly invented status vocabulary" in lower_text


def test_batch_c_capstone_audits_required_overlap_pairs_without_inheritance() -> None:
    text = capstone_text()
    for pair in OVERLAP_PAIRS:
        assert pair in text
    assert text.count("references/satellites/child records and explicit owner routing are not inheritance") >= len(OVERLAP_PAIRS)
    assert "not inheritance or merged schemas" in text


def test_batch_c_capstone_preserves_source_local_legal_ip_and_rejected_import_handling() -> None:
    text = capstone_text()
    for marker in [
        "Source-local and legal/IP posture remains mandatory",
        "Source-local material must not become Astra baseline",
        "Legal/IP evidence failure",
        "proper-noun containment",
        "trademark/license/copyright/verbatim-similarity review",
        "Rejected donor element handling must remain explicit",
        "Rejected-import evidence handling",
    ]:
        assert marker in text


def test_batch_c_capstone_rejects_donor_leakage_and_donor_system_defaults() -> None:
    text = capstone_text()
    for marker in [
        "Donor leakage is prohibited",
        "Donor field names",
        "donor math",
        "donor statblocks",
        "donor spell structures",
        "donor item formats",
        "donor vehicle formats",
        "donor crafting economies",
        "donor faction systems",
        "donor table formats",
        "donor map formats",
        "donor pet/summon systems",
        "donor cosmology",
        "donor proper nouns",
        "donor source-specific setting law",
        "donor systems",
    ]:
        assert marker in text


def test_batch_c_capstone_preserves_batch_b_runtime_canon_sourcebook_live_play_boundaries() -> None:
    text = capstone_text()
    lower_text = text.lower()
    assert "batch b handoffs remain doctrine-facing pressure only" in lower_text
    assert "they are not schema fields" in lower_text
    for marker in [
        "runtime commands",
        "event schemas",
        "context packets",
        "database rows",
        "entity/component schemas",
        "command lifecycle",
        "final mechanics",
        "runtime state",
        "runtime schemas",
        "backend schemas",
        "database schemas",
        "save-state shape",
        "canon/sourcebook/runtime/final-mechanics/live-play/training readiness",
        "sourcebook prose",
        "live-play/GM behavior",
        "training/evaluation packs",
        "D-series material remains draft source material only",
    ]:
        assert marker in text


def test_batch_c_capstone_includes_pending_schema_and_hidden_state_boundaries() -> None:
    text = capstone_text()
    for marker in [
        "`pending_schema` is lawful fallback routing only",
        "not a permission bucket for new fields",
        "donor imports",
        "runtime state",
        "canon shortcuts",
        "Hidden-state and protected-truth material must remain bounded",
        "Hidden-state truth leakage is prohibited",
        "protected-truth runtime handling",
    ]:
        assert marker in text


def test_batch_c_capstone_includes_deferred_gap_ledger_and_next_handoff() -> None:
    text = capstone_text()
    assert "Verdict: Batch C is ready with deferred gaps" in text
    for gap in DEFERRED_GAPS:
        assert gap in text
    assert "named owner or lawful fallback" in text
    assert "next schema/math/mechanics workstream" in text
    assert "later pilot conversion testing" in text


def test_all_c01_c14_files_exist() -> None:
    schema_dir = ROOT / "docs" / "doctrine" / "schema"
    for file_name in C_FAMILY_FILES.values():
        path = schema_dir / file_name
        assert path.exists(), f"Missing {path}"
        assert path.is_file(), f"Not a file: {path}"
        assert read_utf8(path).strip(), f"Empty file: {path}"


def test_all_c_family_registry_entries_remain_draft_not_current_or_stable() -> None:
    for file_id in C_FAMILY_FILES:
        assert _registry_scalar(file_id, "status") == "draft"
        assert _registry_scalar(file_id, "authority_level") == "schema-draft"
        assert _registry_scalar(file_id, "test_status") == "designed"
        assert _registry_scalar(file_id, "review_status") == "not_reviewed"
        block = _registry_record_block(file_id)
        for forbidden_status in FORBIDDEN_PROMOTED_STATUSES:
            assert re.search(rf"^\s*(status|authority_level|test_status|review_status): {re.escape(forbidden_status)}$", block, flags=re.MULTILINE) is None


def test_capstone_does_not_mutate_c_family_statuses_to_current_canon_runtime_stable_or_tested() -> None:
    # Future non-family files may be added. This test scopes only C01-C14 and
    # verifies this capstone did not promote them while adding a readiness audit.
    for file_id in C_FAMILY_FILES:
        for key in ["status", "authority_level", "test_status", "review_status"]:
            assert _registry_scalar(file_id, key) not in FORBIDDEN_PROMOTED_STATUSES
