import re

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM00_PATH = ROOT / "docs" / "doctrine" / "schema_math_mechanics" / "SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Current repository posture",
    "## 3. What Batch C unlocks",
    "## 4. What Batch C does not solve",
    "## 5. Workstream scope definition",
    "## 6. Full schema gap inventory",
    "## 7. Full math/mechanics gap inventory",
    "## 8. Conversion-readiness checklist",
    "## 9. V1 runtime-readiness checklist",
    "## 10. Doctrine/mechanics owner map",
    "## 11. Risk register",
    "## 12. Recommended sequencing",
    "## 13. Proposed first follow-up PRs",
    "## 14. Testing strategy",
    "## 15. Deferred gap ledger",
    "## 16. Non-goals and hard refusals",
    "## 17. Acceptance criteria",
]

C_FAMILY_MARKERS = ["C00"] + [f"C{i:02d}" for i in range(1, 15)]
C_FAMILY_NAMES = [
    "creature/NPC",
    "item/gear",
    "ability/power/technique",
    "relic/implant/installable asset",
    "faction/institution",
    "location/site/region",
    "mission/scenario/adventure",
    "vehicle/ship/platform",
    "hazard/environment",
    "table/oracle",
    "companion/summon",
    "crafting/salvage/recipe",
    "map/diagram annotation",
    "source-local setting/cosmology",
]

SCHEMA_GAPS = [
    "validation schemas",
    "record instance schemas",
    "cross-record references",
    "conversion packet schemas",
    "evidence/provenance schemas",
    "canon-review schemas",
    "conflict ledger schemas",
    "pilot conversion output schemas",
    "mechanics I/O schemas",
    "runtime-prep schemas",
    "test fixture schemas",
]

MATH_MECHANICS_GAPS = [
    "resolution math",
    "difficulty bands",
    "action economy",
    "timing/cadence",
    "cost commitment",
    "partial outcome states",
    "damage",
    "injury",
    "conditions",
    "resources",
    "recovery/recharge",
    "progression",
    "thresholds",
    "character scaling",
    "opposition scaling",
    "hazards",
    "gear/relic scaling",
    "abilities/techniques",
    "crafting/salvage/requisition",
    "faction/social pressure",
    "travel/exploration",
    "vehicle/platform mechanics",
    "companion/summon control",
    "table/oracle probability",
    "map/spatial abstraction",
    "hidden-state handling",
    "balance benchmarks",
]

RISK_MARKERS = [
    "donor math leakage",
    "donor statblock leakage",
    "donor economy leakage",
    "donor class/progression leakage",
    "donor dice-system leakage",
    "donor cosmology leakage",
    "RHBF overfitting",
    "C-family schema drift",
    "Batch B procedure mistaken for final mechanics",
    "Batch C records mistaken for runtime schemas",
    "D-series authority leakage",
    "premature canon/sourcebook/live-play/runtime promotion",
    "hidden-state leakage",
    "unvalidated math",
    "brittle tests",
    "insufficient benchmarks",
    "megafile risk",
    "underdesigned mechanics",
]

HARD_REFUSALS = [
    "final mechanics",
    "exact math",
    "final resolution dice",
    "runtime schema",
    "runtime schemas",
    "backend schema",
    "database schema",
    "backend/database contracts",
    "entity/component/event schema",
    "command lifecycle",
    "context packet contract",
    "save-state shape",
    "canon promotion",
    "accepted lexicon promotion",
    "sourcebook prose",
    "live-play/GM behavior",
    "training/evaluation corpus creation",
    "donor math defaults",
    "donor statblock defaults",
    "donor economy defaults",
    "donor class/progression defaults",
    "donor dice-system defaults",
    "donor cosmology defaults",
    "donor proper noun import",
    "donor defaults",
    "RHBF hidden law",
    "D-series authority promotion",
]

FORBIDDEN_PROMOTED_STATUSES = {
    "current",
    "stable_for_family",
    "stable_cross_family",
    "tested_minimum",
    "accepted_canon",
    "runtime_ready",
    "runtime-ready",
    "canon-ready",
    "schema_math_mechanics_current",
    "post_batch_c_current",
    "planning-promoted",
    "schema-planning-promoted",
    "sm00-promoted",
}


def sm00_text() -> str:
    return read_utf8(SM00_PATH)


def registry_record_block(file_id: str) -> str:
    text = read_utf8(REGISTRY_PATH)
    match = re.search(
        rf"^- file_id: {re.escape(file_id)}\n(?P<block>.*?)(?=^- file_id: |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing registry record for {file_id}"
    return match.group(0)



def test_sm00_exists_and_is_nonempty() -> None:
    assert SM00_PATH.exists()
    assert SM00_PATH.is_file()
    assert sm00_text().strip()


def test_required_section_headings_are_present() -> None:
    text = sm00_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_sm00_names_required_batches_controls_and_families() -> None:
    text = sm00_text()
    for marker in C_FAMILY_MARKERS:
        assert marker in text
    for family_name in C_FAMILY_NAMES:
        assert family_name in text
    for marker in [
        "pending_schema",
        "B11",
        "Batch C capstone",
        "Conversion IR",
        "lawful outcome taxonomy",
        "runtime/Gate B",
    ]:
        assert marker in text


def test_batch_c_readiness_is_not_other_readiness_types() -> None:
    text = sm00_text()
    for marker in [
        "Batch C readiness is not canon readiness",
        "runtime readiness",
        "sourcebook readiness",
        "final mechanics readiness",
        "live-play readiness",
        "training readiness",
    ]:
        assert marker in text


def test_d_series_source_packs_are_draft_source_material_only_and_not_authority() -> None:
    text = sm00_text()
    assert "D00-D19 source packs are draft source material only" in text
    assert "not current doctrine, final mechanics, runtime authority, canon, sourcebook prose, live-play behavior, or training authority" in text
    assert "D-series authority promotion" in text


def test_schema_gap_inventory_terms_are_present() -> None:
    text = sm00_text()
    for marker in SCHEMA_GAPS:
        assert marker in text


def test_math_mechanics_gap_inventory_terms_are_present() -> None:
    text = sm00_text()
    for marker in MATH_MECHANICS_GAPS:
        assert marker in text


def test_conversion_readiness_separates_pilot_from_large_scale() -> None:
    text = sm00_text()
    assert "Minimum pilot conversion readiness" in text
    assert "Large-scale corpus conversion readiness" in text
    assert text.index("Minimum pilot conversion readiness") < text.index("Large-scale corpus conversion readiness")


def test_v1_runtime_readiness_scope_and_dependencies_without_implementation_design() -> None:
    text = sm00_text()
    assert "V1 runtime-readiness scope is downstream of schema/math planning" in text
    assert "depends on audited schema inventories, validated conversion outputs, benchmarked math proposals" in text
    assert "This checklist does not design implementation" in text
    for forbidden_design in [
        "does not define runtime schema",
        "backend schema",
        "database schema",
        "entity/component/event schema",
        "command lifecycle",
        "context packet contract",
        "save-state shape",
    ]:
        assert forbidden_design in text


def test_required_risks_are_registered() -> None:
    text = sm00_text()
    assert "## 11. Risk register" in text
    for marker in RISK_MARKERS:
        assert marker in text


def test_deferred_gaps_route_to_future_owners_or_lawful_fallbacks() -> None:
    text = sm00_text()
    assert "## 15. Deferred gap ledger" in text
    for owner in ["proposed SM01", "proposed SM02", "proposed SM03", "proposed SM04", "proposed SM05"]:
        assert owner in text
    for fallback in ["pending_schema", "quarantine", "deferred gap ledger", "Astra Doctrine Council review"]:
        assert fallback in text


def test_hard_refusals_are_explicit() -> None:
    text = sm00_text()
    assert "SM00 explicitly refuses" in text
    for marker in HARD_REFUSALS:
        assert marker in text
    for grouped in [
        "canon/sourcebook/live-play/training promotion",
        "donor defaults of any kind",
        "RHBF hidden law",
    ]:
        assert grouped in text


def test_registry_records_for_c00_c14_are_not_promoted_by_this_pr() -> None:
    for file_id in C_FAMILY_MARKERS:
        block = registry_record_block(file_id)
        for forbidden in FORBIDDEN_PROMOTED_STATUSES:
            assert forbidden not in block
