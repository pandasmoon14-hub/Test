import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM09_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM09_controlled_pilot_execution_dry_authorization_packet_template.md"
)

SCAFFOLD_DIR = ROOT / "tests" / "fixtures" / "pilot_conversion_scaffold"
DRY_TEMPLATE_PATH = SCAFFOLD_DIR / "dry_authorization_packet_template.md"

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing dry authorization posture",
    "What SM09 owns",
    "What SM09 must not own",
    "Dry authorization packet definition",
    "Dry template fixture policy",
    "Placeholder/non-donor content policy",
    "Required authorization packet sections",
    "SM02 readiness gate representation",
    "SM03 dry-run result representation",
    "SM04 rubric readiness representation",
    "SM05 authorization decision representation",
    "SM06 execution and output-capture representation",
    "SM07 scaffold and review-harness representation",
    "SM08 placeholder/no-donor validation representation",
    "Packet scope and C-family pressure representation",
    "Evidence and provenance representation",
    "Lawful outcome and mapping ledger representation",
    "Rejected-import, source-local, legal/IP, and `pending_schema` representation",
    "Confidence, review-routing, repair, quarantine, and failure-report representation",
    "Donor leakage hard-fail representation",
    "Review handoff and owner assignment representation",
    "Dry authorization packet labels",
    "Template validation expectations",
    "What dry authorization template readiness may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM09",
    "Acceptance criteria",
]

REQUIRED_NAMES = [
    "SM00",
    "SM01",
    "SM02",
    "SM03",
    "SM04",
    "SM05",
    "SM06",
    "SM07",
    "SM08",
    "C00-C14",
    "Batch C capstone",
    "B11",
    "Conversion IR",
    "lawful outcome taxonomy",
    "conversion intake",
    "extraction readiness",
    "donor family routing",
    "evaluation",
    "benchmark",
    "runtime",
    "Gate B",
]

REQUIRED_DRY_TEMPLATE_SLOTS = [
    "SM05 authorization decision",
    "authorization label",
    "authorization rationale",
    "exact authorized packet count",
    "exact authorized C-family pressure routes",
    "named authorization owner",
    "statement that SM02 gates were satisfied with no waived minimum gate",
    "statement that SM03 dry-run review passed or failures were routed",
    "statement that SM04 rubric is ready for post-execution review",
    "SM06 output capture plan reference",
    "SM07 scaffold/review harness reference",
    "SM08 placeholder/no-donor validation reference",
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
    "SM04 review handoff target",
    "donor leakage hard-fail criteria",
    "final non-readiness statement",
]

DRY_TEMPLATE_LABELS = [
    "dry_template_ready_for_review",
    "dry_template_blocked_by_missing_sm05_slot",
    "dry_template_blocked_by_missing_sm02_gate_slot",
    "dry_template_blocked_by_missing_sm04_handoff",
    "dry_template_blocked_by_missing_no_donor_validation",
    "dry_template_blocked_by_scope_expansion",
    "dry_template_blocked_by_legal_ip_gap",
    "dry_template_blocked_by_runtime_or_mechanics_creep",
    "dry_template_requires_repair",
    "dry_template_requires_quarantine",
    "dry_template_not_authorization",
    "dry_template_not_execution_approval",
]

DONOR_ARTIFACT_MARKERS = [
    "donor excerpt:",
    "statblock:",
    "source table:",
    "source map:",
    "converted output:",
    "training example:",
    "sourcebook-ready example:",
    "actual pilot output:",
]

DONOR_PROPER_NOUN_SENTINELS = [
    "Golarion",
    "Forgotten Realms",
    "Faerun",
    "Greyhawk",
    "Eberron",
    "Ravenloft",
    "Dragonlance",
    "Mystara",
    "Planescape",
    "Spelljammer",
]

IMPLEMENTATION_ARTIFACT_PATTERNS = [
    r"class\s+\w+\s*\(\s*BaseModel\s*\)",
    r'"type"\s*:\s*"object"',
    r"CREATE\s+TABLE",
    r"command_lifecycle\s*[:=]",
    r"context_packet\s*[:=]",
    r"save_state\s*[:=]",
    r"converted output:\s*\n\s*\S",
    r"donor excerpt:\s*\n\s*\S",
    r"statblock:\s*\n\s*\S",
    r"source table:\s*\n\s*\|",
    r"source map:\s*\n\s*\S",
]


def _content() -> str:
    return read_utf8(SM09_PATH)


def _assert_terms(content: str, terms: list[str], label: str) -> None:
    lower = content.lower()
    for term in terms:
        assert term.lower() in lower, f"Missing {label}: {term}"


def test_sm09_file_exists_and_nonempty():
    assert SM09_PATH.exists(), f"SM09 file not found at {SM09_PATH}"
    assert _content().strip(), "SM09 file is empty"


def test_sm09_required_section_headings_present_and_in_order():
    content = _content()
    last_index = -1
    for index, section in enumerate(REQUIRED_SECTIONS, start=1):
        heading = f"## {index}. {section}"
        current_index = content.find(heading)
        assert current_index != -1, f"Missing required section heading: {heading}"
        assert current_index > last_index, f"Section heading out of order: {heading}"
        last_index = current_index


def test_sm09_names_required_repo_state_controls():
    content = _content()
    _assert_terms(content, REQUIRED_NAMES, "required control name")
    _assert_terms(content, [f"C{index:02d}" for index in range(15)], "C-family token")


def test_sm09_states_dry_template_only_and_no_execution_or_conversion():
    content = _content().lower()
    assert "controlled pilot execution dry authorization packet template file only" in content
    assert "does not authorize actual execution" in content
    assert "does not approve execution" in content
    assert "does not run conversion" in content
    assert "does not create actual converted donor content" in content
    assert "pilot outputs" in content
    assert "not an authorization decision" in content
    assert "not execution approval" in content


def test_sm09_refuses_required_non_goals():
    content = _content()
    refusal_terms = [
        "real copyrighted donor excerpts",
        "donor statblocks",
        "donor tables",
        "donor maps",
        "donor setting prose",
        "donor proper nouns",
        "import donor proper nouns as Astra defaults",
        "benchmark corpora",
        "evaluation corpora",
        "training data",
        "fine-tuning data",
        "model behavior policy",
        "final schemas",
        "JSON Schema",
        "Pydantic models",
        "final validators",
        "runtime/backend/database contracts",
        "final mechanics",
        "canon/sourcebook/live-play/training content",
        "registry promotion",
        "C00-C14 rewrite",
        "C15 creation",
        "D00-D19",
        "RHBF",
        "waive SM02",
        "bypass SM05",
        "execution approval",
        "legal/IP clearance",
    ]
    _assert_terms(content, refusal_terms, "non-goal/refusal term")


def test_sm09_defines_dry_authorization_packet_and_fixture_policy():
    content = _content().lower()
    assert "a dry authorization packet is" in content
    assert "dry template fixture policy" in content
    assert "tests/fixtures/pilot_conversion_scaffold/dry_authorization_packet_template.md" in content
    assert "placeholder/synthetic/non-donor markdown fixture" in content


def test_sm09_includes_required_dry_authorization_packet_slots():
    _assert_terms(_content(), REQUIRED_DRY_TEMPLATE_SLOTS, "dry authorization packet slot")


def test_sm09_preserves_c_family_pressure_and_deferrals():
    content = _content()
    pressure_terms = [
        "C01 creature/NPC",
        "C02 item/gear",
        "C03 ability/power/technique",
        "C10 table/oracle",
        "conditional C14 source-local setting/cosmology",
        "3-5 packet candidates",
        "must not expand beyond authorization",
    ]
    _assert_terms(content, pressure_terms, "pressure-set term")
    _assert_terms(content, ["C05", "C06", "C07", "C08", "C11", "C12", "C13"], "deferred C-family")
    assert "C04 and C09 may also remain deferred" in content


def test_sm09_includes_local_labels_and_registry_boundary():
    content = _content()
    _assert_terms(content, DRY_TEMPLATE_LABELS, "dry template label")
    lower = content.lower()
    assert "local labels only" in lower
    assert "not registry values" in lower
    for registry_field in ["status", "authority_level", "test_status", "review_status"]:
        assert registry_field in content


def test_sm09_states_may_and_may_not_prove():
    content = _content().lower()
    assert "sm09 may prove" in content
    assert "sm09 may not prove" in content
    for term in [
        "dry, non-donor template",
        "required authorization slots",
        "sm02-sm08 dependency slots",
        "actual authorization",
        "execution approval",
        "legal/ip clearance",
        "runtime readiness",
        "training readiness",
        "database/schema implementation readiness",
    ]:
        assert term in content


def test_sm09_has_non_readiness_boundaries_owner_routing_and_risk_register():
    content = _content().lower()
    assert "large-scale conversion non-readiness boundary" in content
    assert "runtime/canon/sourcebook/live-play/training non-readiness boundary" in content
    assert "owner map and lawful fallbacks" in content
    assert "risk register" in content
    for term in ["owner", "lawful fallbacks", "repair", "quarantine", "rejected-import", "source-local", "pending_schema", "failure report"]:
        assert term in content


def test_sm09_recommends_safe_sm10_follow_up_only():
    content = _content()
    assert "SM10 dry authorization packet validation and reviewer decision-gate controls" in content
    assert "SM10 dry authorization template repair and slot-hardening controls" in content
    lower = content.lower()
    assert "must not recommend jumping directly" in lower
    for forbidden_jump in [
        "actual donor conversion",
        "broad conversion",
        "final mechanics",
        "runtime schemas",
        "canon consolidation",
        "sourcebook prose",
        "live-play adapter behavior",
        "training corpus creation",
        "real donor-content ingestion",
    ]:
        assert forbidden_jump in lower


def test_sm09_has_no_obvious_implementation_artifacts_or_actual_donor_content():
    content = _content()
    for pattern in IMPLEMENTATION_ARTIFACT_PATTERNS:
        assert not re.search(pattern, content, flags=re.IGNORECASE), (
            f"SM09 contains implementation artifact or actual-content pattern: {pattern}"
        )


def test_dry_authorization_fixture_exists_and_is_direct_child_markdown():
    assert DRY_TEMPLATE_PATH.exists(), "Dry authorization packet fixture must exist"
    assert DRY_TEMPLATE_PATH.suffix == ".md"
    assert DRY_TEMPLATE_PATH.parent == SCAFFOLD_DIR
    assert DRY_TEMPLATE_PATH.is_file()


def test_dry_authorization_fixture_is_labeled_placeholder_synthetic_non_donor():
    content = read_utf8(DRY_TEMPLATE_PATH).lower()
    for required in [
        "placeholder",
        "synthetic",
        "non-donor",
        "no real donor content",
        "not converted content",
        "not training data",
        "not canon",
        "not sourcebook prose",
        "not runtime import data",
    ]:
        assert required in content, f"Dry template fixture missing label: {required}"


def test_dry_authorization_fixture_contains_required_slots():
    _assert_terms(read_utf8(DRY_TEMPLATE_PATH), REQUIRED_DRY_TEMPLATE_SLOTS, "fixture slot")


def test_dry_authorization_fixture_uses_abstract_placeholder_labels():
    content = read_utf8(DRY_TEMPLATE_PATH)
    for label in [
        "[placeholder packet identity]",
        "[placeholder authorization rationale]",
        "[placeholder evidence reference]",
        "[placeholder review owner]",
    ]:
        assert label in content


def test_dry_authorization_fixture_has_no_donor_artifact_markers_or_sentinels():
    content = read_utf8(DRY_TEMPLATE_PATH)
    lower = content.lower()
    for marker in DONOR_ARTIFACT_MARKERS:
        assert marker not in lower, f"Fixture contains forbidden donor artifact marker: {marker}"
    for sentinel in DONOR_PROPER_NOUN_SENTINELS:
        assert sentinel not in content, f"Fixture contains forbidden donor proper-noun sentinel: {sentinel}"


def test_scaffold_markdown_files_mirror_sm08_no_donor_safety_posture():
    assert SCAFFOLD_DIR.exists(), f"Scaffold fixture directory not found: {SCAFFOLD_DIR}"
    direct_files = {path for path in SCAFFOLD_DIR.iterdir() if path.is_file()}
    assert direct_files, "Scaffold fixture directory must contain files"
    non_markdown = {path.name for path in direct_files if path.suffix != ".md"}
    assert not non_markdown, f"Scaffold fixture directory may only contain Markdown files: {sorted(non_markdown)}"

    for path in direct_files:
        content = read_utf8(path)
        lower = content.lower()
        for required in ["placeholder", "synthetic", "non-donor"]:
            assert required in lower, f"{path} must contain {required}"
        for marker in DONOR_ARTIFACT_MARKERS:
            assert marker not in lower, f"{path} contains forbidden donor artifact marker: {marker}"
        for sentinel in DONOR_PROPER_NOUN_SENTINELS:
            assert sentinel not in content, f"{path} contains forbidden donor proper-noun sentinel: {sentinel}"


def test_registry_c00_c14_records_not_promoted_to_forbidden_states():
    assert REGISTRY_PATH.exists(), f"Registry not found: {REGISTRY_PATH}"
    registry_content = read_utf8(REGISTRY_PATH)
    status_fields = ["status", "authority_level", "test_status", "review_status"]
    forbidden_states = {
        "canon-promoted",
        "runtime-ready",
        "sourcebook-ready",
        "live-play-ready",
        "training-ready",
        "final-mechanics-ready",
    }

    for index in range(15):
        token = f"C{index:02d}"
        block_match = re.search(
            rf"^- file_id: {token}\n(?P<block>.*?)(?=^- file_id: |\Z)",
            registry_content,
            flags=re.MULTILINE | re.DOTALL,
        )
        assert block_match, f"Registry must keep tracking record block for {token}"
        block = block_match.group("block")
        for field in status_fields:
            field_match = re.search(rf"^  {field}:\s*(?P<value>.+?)\s*$", block, re.MULTILINE)
            assert field_match, f"{token} registry block must include {field}"
            value = field_match.group("value").strip().strip("'\"").lower()
            assert value not in forbidden_states, (
                f"{token} registry {field} contains forbidden promotion state: {value}"
            )
