from pathlib import Path
import re

from tests.helpers import REGISTRY_PATH, read_utf8


ROOT = Path(__file__).resolve().parents[1]
UNLOCK_PATH = ROOT / "docs" / "doctrine" / "schema" / "Batch_C_schema_family_unlock_index_and_readiness_gate.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Current repository posture",
    "## 3. C00 binding constraints",
    "## 4. Batch B handoff implications",
    "## 5. C-family owner map for C01-C14",
    "## 6. Cross-family overlap and safe-boundary matrix",
    "## 7. Risk register",
    "## 8. Recommended sequencing",
    "## 9. First-wave unlock plan",
    "## 10. Testing strategy",
    "## 11. Registry strategy",
    "## 12. Source-local and legal/IP risk strategy",
    "## 13. Deferred gap ledger",
    "## 14. Acceptance criteria",
    "## 15. Follow-up handoff to C01",
]

C_FAMILIES = [
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
]

RISK_CATEGORIES = [
    "C00 bypass risk",
    "family-specific schema drift",
    "C-family overlap and duplicate ownership",
    "donor-field-name leakage",
    "donor-math/statblock leakage",
    "donor cosmology/proper-noun leakage",
    "source-local material becoming Astra baseline",
    "legal/IP evidence failure",
    "canon eligibility confusion",
    "runtime-state leakage",
    "sourcebook-prose leakage",
    "Batch B operational procedure being misread as schema fields",
    "hidden-state truth leakage",
    "over-broad C-family files becoming megafiles",
    "under-specified C-family files failing conversion pressure",
    "composite records spanning multiple families",
    "parent/child/satellite record handling",
    "pending_schema overuse",
    "rejected-import evidence handling",
    "confidence/review/validation misuse",
    "registry drift",
    "brittle tests that fail when future C-family files are intentionally added",
    "missing focused tests",
    "cross-family references that imply inheritance when inheritance is not allowed",
    "canon/sourcebook/runtime gates being confused with Batch C readiness",
]

FORBIDDEN_PROMOTED_STATUSES = {
    "current",
    "tested_minimum",
    "stable_for_family",
    "stable_cross_family",
}



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

def _unlock_text() -> str:
    return read_utf8(UNLOCK_PATH)


def test_batch_c_unlock_index_readiness_file_exists() -> None:
    assert UNLOCK_PATH.exists()
    assert UNLOCK_PATH.is_file()
    assert _unlock_text().strip()


def test_required_sections_are_present() -> None:
    text = _unlock_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_all_c_families_and_pending_schema_are_named() -> None:
    text = _unlock_text()
    for family in C_FAMILIES:
        assert family in text


def test_overlap_pairs_and_non_inheritance_boundary_are_named() -> None:
    text = _unlock_text()
    for pair in OVERLAP_PAIRS:
        assert pair in text
    assert "Cross-family references do not imply inheritance" in text
    assert "inheritance_allowed` remains false by default" in text


def test_all_required_risk_categories_are_named() -> None:
    text = _unlock_text()
    for risk_category in RISK_CATEGORIES:
        assert risk_category in text


def test_c00_astra_base_and_pending_schema_requirements_are_present() -> None:
    text = _unlock_text()
    required_markers = [
        "Every durable C-family record must inherit/include `AstraContentRecordBase`",
        "`pending_schema` is lawful only as named fallback routing and not as field invention",
        "C00 bypass is prohibited",
        "Missing schema coverage produces quarantine, escalation, human review, or `pending_schema`, not improvised family-specific fields",
    ]
    for marker in required_markers:
        assert marker in text


def test_batch_b_handoff_is_doctrine_facing_only_not_schema_fields() -> None:
    text = _unlock_text()
    assert "Batch B files identify operational pressure and related owners" in text
    assert "Batch B handoff notes are not schema fields" in text
    assert "Batch B handoff records are doctrine-facing only" in text
    assert "they must not be interpreted as:" in text
    assert "C-family schema fields" in text


def test_source_local_and_legal_ip_risk_routing_is_present() -> None:
    text = _unlock_text()
    assert "Source-local and legal/IP flags are mandatory risk-routing concerns" in text
    assert "ip_legal_flags" in text
    assert "source-local containment" in text
    assert "proper-noun, trademark, license, verbatim-similarity, copyright" in text


def test_runtime_schema_creation_is_explicitly_forbidden() -> None:
    text = _unlock_text().lower()
    forbidden_markers = [
        "runtime schema",
        "backend schema",
        "entity/component schema",
        "event schema",
        "command lifecycle",
        "context packet",
        "save-state shape",
        "database contract",
        "database schema",
    ]
    for marker in forbidden_markers:
        assert marker in text
    assert "forbid runtime/entity/component/event/command/context/database schema creation" in text


def test_canon_sourcebook_live_play_and_prose_promotion_is_forbidden() -> None:
    text = _unlock_text().lower()
    for marker in [
        "canon acceptance",
        "canon promotion",
        "sourcebook prose",
        "live-play behavior",
        "prose promotion",
        "canon/sourcebook/runtime readiness is not batch c readiness",
    ]:
        assert marker in text
    assert "forbid canon/sourcebook/live-play/prose promotion" in text


def test_donor_defaults_are_explicitly_rejected() -> None:
    text = _unlock_text()
    for marker in [
        "donor field names",
        "donor math",
        "donor statblocks",
        "donor currency/economy",
        "donor class structures",
        "donor cosmology",
        "donor proper nouns",
        "rejected as Astra defaults",
    ]:
        assert marker in text


def test_unlock_file_does_not_draft_c01_c14_family_content() -> None:
    text = _unlock_text()
    assert "This file does not create, define, draft, or promote C01-C14" in text
    assert "This file does not draft C01" in text
    assert "does not define final family-specific schema fields" in text
    # Future PRs may intentionally add C01-C14 files. This test only ensures
    # the planning file itself has not become a family draft with family
    # heading sections or schema code blocks.
    assert not re.search(r"^##\s+C(?:0[1-9]|1[0-4])\b", text, flags=re.MULTILINE)
    assert "```yaml" not in text


def test_registry_does_not_promote_c00_or_c01_c14_to_current_stable_or_tested_statuses() -> None:
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        assert _registry_scalar(file_id, "status") not in FORBIDDEN_PROMOTED_STATUSES
        assert _registry_scalar(file_id, "test_status") not in {
            "tested_minimum",
            "stable_for_family",
            "stable_cross_family",
            "current",
        }


def test_registry_c_family_records_remain_present_without_forbidden_promotion() -> None:
    # Future C-family PRs may legitimately advance individual C01-C14
    # records beyond their initial todo/not_started posture. This unlock gate
    # only guards against improper current/tested/stable promotion.
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        assert _registry_record_block(file_id)
        assert _registry_scalar(file_id, "status") not in FORBIDDEN_PROMOTED_STATUSES


def test_no_registry_entry_was_added_for_this_control_file_without_convention() -> None:
    registry_text = read_utf8(REGISTRY_PATH)
    assert "Batch_C_schema_family_unlock_index_and_readiness_gate.md" not in registry_text
