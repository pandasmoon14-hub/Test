import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM07_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM07_controlled_pilot_conversion_execution_packet_scaffold_and_review_harness.md"
)

SCAFFOLD_DIR = ROOT / "tests" / "fixtures" / "pilot_conversion_scaffold"

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing scaffold posture",
    "What SM07 owns",
    "What SM07 must not own",
    "Controlled pilot packet scaffold definition",
    "Review harness definition",
    "Scaffold scope constraints",
    "Placeholder/non-donor content policy",
    "Required SM05 authorization reference scaffold",
    "Required SM06 output-capture scaffold",
    "Packet manifest scaffold requirements",
    "Evidence and provenance scaffold requirements",
    "Construct inventory scaffold requirements",
    "Lawful outcome ledger scaffold requirements",
    "Mapping ledger scaffold requirements",
    "C00-C14 and `pending_schema` routing scaffold requirements",
    "Rejected-import, source-local, and legal/IP scaffold requirements",
    "Confidence, review-routing, and human-review scaffold requirements",
    "Repair, quarantine, and failure-report scaffold requirements",
    "Donor leakage review scaffold requirements",
    "SM04 review handoff scaffold requirements",
    "Review harness pass/block labels",
    "Scaffold validation expectations",
    "What scaffold readiness may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM07",
    "Acceptance criteria",
]

SM05_AUTHORIZATION_REFERENCE_TERMS = [
    "SM05 authorization decision",
    "authorization label",
    "authorization rationale",
    "exact authorized packet count",
    "exact authorized C-family pressure routes",
    "named authorization owner",
    "statement that SM02 gates were satisfied with no waived minimum gate",
    "statement that SM03 dry-run review passed or failures were routed",
    "statement that SM04 rubric is ready for post-execution review",
]

SM06_OUTPUT_CAPTURE_TERMS = [
    "packet identity",
    "donor source identity",
    "donor-family classification",
    "extraction run identity",
    "page/range truth",
    "source hash or hash-later policy",
    "evidence references",
    "construct inventory",
    "lawful outcome ledger",
    "mapping ledger",
    "rejected-import ledger",
    "source-local retention ledger",
    "pending_schema ledger",
    "repair queue status",
    "quarantine queue status",
    "confidence/review-routing notes",
    "legal/IP flags",
    "reviewer decision points",
    "C-family routing targets",
    "pilot output review status",
    "failure report shape",
    "benchmark/evaluation prerequisites",
    "SM05 authorization reference",
    "SM04 review handoff target",
]

SCAFFOLD_LABELS = [
    "scaffold_ready_for_authorized_pilot_packet",
    "scaffold_blocked_by_missing_sm05_authorization",
    "scaffold_blocked_by_scope_expansion",
    "scaffold_blocked_by_donor_content_leakage",
    "scaffold_blocked_by_missing_capture_slot",
    "scaffold_blocked_by_missing_review_handoff",
    "scaffold_blocked_by_legal_ip_risk",
    "scaffold_blocked_by_runtime_or_mechanics_creep",
    "scaffold_requires_repair",
    "scaffold_requires_quarantine",
    "scaffold_not_reviewable",
    "placeholder_only_not_execution_ready",
]

FORBIDDEN_C_PROMOTION_VALUES = {
    "current",
    "pressure-tested",
    "stable_for_family",
    "stable_cross_family",
    "tested_minimum",
    "accepted_canon",
    "runtime_ready",
    "runtime-ready",
    "canon-ready",
    "schema-current",
    "schema_current",
    "runtime-current",
    "training-current",
}

KNOWN_DONOR_MARKERS = [
    "Forgotten Realms",
    "Waterdeep",
    "Baldur's Gate",
    "Strahd",
    "Ravenloft",
    "Mordenkainen",
    "Vecna",
    "Tasha",
    "Beholder",
    "Mind Flayer",
    "Drow",
    "Warhammer",
    "Space Marine",
    "Adeptus",
    "Pathfinder",
    "Golarion",
]


def sm07_text() -> str:
    return read_utf8(SM07_PATH)


def _registry_record_block(file_id: str) -> str:
    text = read_utf8(REGISTRY_PATH)
    match = re.search(
        rf"^- file_id: {re.escape(file_id)}\n(?P<block>.*?)(?=^- file_id: |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing registry record for {file_id}"
    return match.group(0)


def _scalar_from_block(block: str, key: str) -> str | None:
    match = re.search(
        rf"^\s*{re.escape(key)}:\s*['\"]?(?P<value>[^'\"\n#]+)",
        block,
        flags=re.MULTILINE,
    )
    return match.group("value").strip() if match else None


# --- Existence and structure ---


def test_sm07_file_exists_and_is_nonempty() -> None:
    assert SM07_PATH.exists()
    assert SM07_PATH.is_file()
    assert sm07_text().strip()


def test_required_section_headings_are_present() -> None:
    text = sm07_text()
    for section in REQUIRED_SECTIONS:
        assert section in text, f"Missing section: {section}"


# --- Identity and required controls ---


def test_sm07_names_required_controls_and_families() -> None:
    text = sm07_text()
    for marker in [
        "SM00",
        "SM01",
        "SM02",
        "SM03",
        "SM04",
        "SM05",
        "SM06",
        "C00",
        "Batch C capstone",
        "B11",
        "Conversion IR",
        "lawful outcome taxonomy",
        "conversion intake",
        "extraction readiness",
        "donor family routing",
        "evaluation/benchmark",
        "runtime/Gate B",
    ]:
        assert marker in text, f"Missing upstream reference: {marker}"
    for number in range(1, 15):
        assert f"C{number:02d}" in text, f"Missing C-family reference: C{number:02d}"


def test_sm07_states_controlled_pilot_packet_scaffold_only() -> None:
    text = sm07_text()
    assert (
        "SM07 is a controlled pilot conversion execution packet scaffold and review harness file only"
        in text
    )


def test_sm07_states_no_conversion_or_outputs() -> None:
    text = sm07_text()
    assert "SM07 does not run conversion" in text
    assert "SM07 does not create actual converted donor content or pilot outputs" in text


def test_sm07_refuses_real_donor_content_and_non_goals() -> None:
    text = sm07_text()
    for marker in [
        "real copyrighted donor excerpts",
        "donor statblocks",
        "donor tables",
        "donor maps",
        "donor setting prose",
        "import donor proper nouns as Astra defaults",
        "create benchmark corpora",
        "create evaluation corpora",
        "create training data",
        "create fine-tuning data",
        "create model behavior policy",
        "create final output schemas",
        "create JSON Schema files",
        "create Pydantic models",
        "create final validators",
        "runtime/backend/database contracts",
        "create final mechanics",
        "canon/sourcebook/live-play/training content",
        "registry promotion",
        "rewrite C00-C14",
        "add C15",
        "treat D00-D19 as authority",
        "use RHBF as hidden law",
        "waive SM02 minimum pilot readiness gates",
        "bypass SM05 authorization",
        "treat SM07 scaffold as execution approval",
    ]:
        assert marker in text, f"Missing non-goal marker: {marker}"


def test_sm07_states_upstream_authority_boundaries() -> None:
    text = sm07_text()
    assert "SM00 owns master sequencing" in text
    assert "SM01 owns validation/schema inventory posture" in text
    assert "SM02 owns minimum pilot readiness gates" in text
    assert "SM03 owns dry-run review planning" in text
    assert "SM04 owns pilot benchmark/evaluation rubric controls" in text
    assert "SM05 owns authorization/preflight gate posture" in text
    assert "SM06 owns controlled execution/output capture planning" in text
    assert "SM07 cannot waive SM02 gates" in text
    assert "cannot bypass SM05 authorization" in text
    assert "C00 owns shared content record base posture" in text
    assert "C01-C14 own conversion-stage/canon-review family grammar" in text
    assert (
        "Batch B/B11 are operational routing doctrine, not final mechanics or runtime validation authority"
        in text
    )
    assert "D00-D19 source packs are draft source material only" in text


# --- Definitions and scope ---


def test_sm07_defines_scaffold_and_review_harness() -> None:
    text = sm07_text()
    assert (
        "A controlled pilot packet scaffold is repo-local placeholder/test structure for organizing future authorized pilot packet metadata and output-capture expectations"
        in text
    )
    assert (
        "A review harness is repo-local placeholder/test structure for checking whether future pilot packet outputs can be routed to SM04 review, repair, quarantine, or lawful fallback"
        in text
    )


def test_sm07_recommends_tiny_bounded_scaffold_scope() -> None:
    text = sm07_text()
    assert "3-5 packet candidates" in text
    assert "tiny" in text.lower()
    assert "bounded" in text.lower()
    assert "unless SM05 authorization narrows further" in text


def test_sm07_lists_authorized_pressure_routes_and_deferred_families() -> None:
    text = sm07_text()
    for marker in [
        "C01 creature/NPC",
        "C02 item/gear",
        "C03 ability/power/technique",
        "C10 table/oracle",
        "conditional C14 source-local setting/cosmology",
    ]:
        assert marker in text, f"Missing pressure route: {marker}"
    for fam in ["C05", "C06", "C07", "C08", "C11", "C12", "C13"]:
        assert fam in text, f"Missing deferred family: {fam}"
    assert "C04" in text
    assert "C09" in text
    assert "remain deferred" in text


# --- Required terms and labels ---


def test_sm07_includes_sm05_authorization_and_sm06_capture_terms() -> None:
    text = sm07_text()
    for term in SM05_AUTHORIZATION_REFERENCE_TERMS:
        assert term in text, f"Missing SM05 authorization term: {term}"
    for term in SM06_OUTPUT_CAPTURE_TERMS:
        assert term in text, f"Missing SM06 output capture term: {term}"


def test_sm07_labels_are_document_local_not_registry_values() -> None:
    text = sm07_text()
    for label in SCAFFOLD_LABELS:
        assert label in text, f"Missing scaffold label: {label}"
    assert "local labels only, not registry values" in text
    assert "must not be written into registry fields" in text
    for registry_field in ["status", "authority_level", "test_status", "review_status"]:
        assert registry_field in text


def test_sm07_includes_placeholder_policy_and_validation_expectations() -> None:
    text = sm07_text()
    for marker in [
        "be synthetic",
        "be non-donor",
        "be clearly labeled as placeholder",
        "contain no real donor excerpts",
        "contain no real donor statblocks",
        "contain no donor tables",
        "contain no donor maps",
        "contain no donor setting prose",
        "contain no donor proper nouns",
        "contain no protected expression",
        "not function as converted content",
        "not function as training data",
        "not function as canon",
        "not function as sourcebook prose",
        "not function as runtime import data",
        "scaffold files exist if created",
        "scaffold includes required capture slots",
        "scaffold references SM05 authorization and SM06 output capture posture",
        "scaffold routes future output review to SM04",
        "scaffold blocks scope expansion",
        "scaffold blocks donor content leakage",
        "scaffold blocks runtime/canon/sourcebook/live-play/training/final-mechanics claims",
        "scaffold does not include implementation artifacts",
    ]:
        assert marker in text, f"Missing policy/validation marker: {marker}"


# --- Readiness boundaries, owner routing, risks, next PR ---


def test_sm07_states_what_scaffold_readiness_may_and_may_not_prove() -> None:
    text = sm07_text()
    for marker in [
        "the repo has a placeholder structure for a future controlled pilot packet",
        "review handoff expectations can be represented",
        "required capture slots can be listed",
        "no-donor placeholder policy can be enforced by tests",
        "future execution can be scoped more safely",
        "conversion execution readiness",
        "conversion success",
        "pilot output quality",
        "pilot evaluation success",
        "large-scale corpus conversion readiness",
        "canon readiness",
        "sourcebook readiness",
        "runtime readiness",
        "final mechanics readiness",
        "live-play readiness",
        "training readiness",
        "benchmark corpus readiness",
        "model adapter readiness",
        "database/schema implementation readiness",
    ]:
        assert marker in text, f"Missing readiness marker: {marker}"


def test_sm07_includes_non_readiness_boundaries() -> None:
    text = sm07_text()
    assert "Large-scale conversion non-readiness boundary" in text
    assert "SM07 does not prove large-scale corpus conversion readiness" in text
    assert "Runtime/canon/sourcebook/live-play/training non-readiness boundary" in text
    assert "SM07 is not runtime readiness" in text


def test_sm07_includes_owner_routing_and_lawful_fallbacks() -> None:
    text = sm07_text()
    for marker in [
        "future pilot conversion owner",
        "future pilot conversion owner plus test owner",
        "authorization owner",
        "pilot conversion owner",
        "future conversion/evidence validation owner",
        "conversion intake owner",
        "lawful outcome/conversion intake owner",
        "C00/C-family schema owner and future validation/schema implementation owner",
        "C00/future validation/schema implementation owner",
        "C00/C14 plus future review/legal owner",
        "future conversion integrity owner plus relevant future mechanics/schema owner",
        "future review owner",
        "extraction readiness and pilot conversion owner",
        "future evaluation/benchmark owner",
        "future mechanics requirements owner only",
        "future runtime/Gate B owner only",
        "appropriate later phase owner only",
        "Lawful fallbacks must be explicit",
    ]:
        assert marker in text, f"Missing owner route: {marker}"


def test_sm07_includes_risk_register() -> None:
    text = sm07_text()
    for marker in [
        "Risk register",
        "Scaffold treated as conversion execution",
        "Scaffold treated as execution approval",
        "SM02 gate waiver",
        "Scope creep beyond SM05 authorized packet count",
        "Donor content embedded in scaffold",
        "Donor mechanics leakage",
        "Source-local/legal/IP leakage",
        "Missing capture slot",
        "Missing SM04 handoff",
        "Scaffold labels treated as registry values",
        "Runtime/canon/sourcebook/training creep",
        "D-series authority creep",
        "RHBF hidden law",
        "Review bypass",
    ]:
        assert marker in text, f"Missing risk: {marker}"


def test_sm07_recommends_next_pr_without_broad_jump() -> None:
    text = sm07_text()
    assert "SM08 controlled pilot packet placeholder validation and no-donor safety harness" in text
    assert "SM08 scaffold repair and review-harness gap closure controls" in text
    for marker in [
        "broad conversion",
        "final mechanics",
        "runtime schemas",
        "canon consolidation",
        "sourcebook prose",
        "live-play adapter behavior",
        "training corpus creation",
    ]:
        assert marker in text, f"Missing next-PR boundary: {marker}"


# --- No implementation artifacts or donor content ---


def test_sm07_does_not_contain_obvious_implementation_artifacts() -> None:
    text = sm07_text()
    forbidden_patterns = [
        r"```\s*json",
        r"```\s*yaml",
        r"\$schema",
        r"\"type\"\s*:\s*\"object\"",
        r"class\s+\w+\(BaseModel\)",
        r"CREATE\s+TABLE",
        r"command_lifecycle\s*[:=]",
        r"context_packet\s*[:=]",
        r"save_state\s*[:=]",
        r"converted_donor_content\s*[:=]",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text, flags=re.IGNORECASE), (
            f"Implementation artifact found: {pattern}"
        )


def test_placeholder_scaffold_fixtures_are_labeled_and_non_donor_if_created() -> None:
    if not SCAFFOLD_DIR.exists():
        return
    fixture_files = sorted(path for path in SCAFFOLD_DIR.glob("*.md") if path.is_file())
    assert fixture_files, "Scaffold fixture directory exists but has no markdown fixtures"
    for path in fixture_files:
        text = read_utf8(path)
        lowered = text.lower()
        for marker in ["placeholder", "synthetic", "non-donor"]:
            assert marker in lowered, f"{path} lacks {marker} label"
        for marker in KNOWN_DONOR_MARKERS:
            assert marker.lower() not in lowered, f"{path} contains donor marker: {marker}"
        for artifact_marker in ["converted output:", "donor excerpt:", "statblock:", "source table:", "source map:"]:
            assert artifact_marker not in lowered, f"{path} contains content artifact marker: {artifact_marker}"


# --- Registry non-promotion ---


def test_c00_c14_registry_records_not_promoted_to_forbidden_states() -> None:
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        for key in ["status", "authority_level", "test_status", "review_status"]:
            value = _scalar_from_block(block, key)
            if value is not None:
                assert value not in FORBIDDEN_C_PROMOTION_VALUES, (
                    f"{file_id} {key} was promoted to {value!r}"
                )


# --- Future-safe posture ---


def test_future_safe_posture_does_not_block_later_sm_files_or_proper_owner_promotion() -> None:
    text = sm07_text()
    assert "future-safe" in text
    assert "proper owner-controlled PRs" in text
    assert "later legitimate registry promotion" in text
