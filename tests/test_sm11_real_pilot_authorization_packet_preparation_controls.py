import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM11_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM11_real_pilot_authorization_packet_preparation_controls.md"
)

SCAFFOLD_DIR = ROOT / "tests" / "fixtures" / "pilot_conversion_scaffold"
DRY_TEMPLATE_PATH = SCAFFOLD_DIR / "dry_authorization_packet_template.md"

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing real authorization preparation posture",
    "What SM11 owns",
    "What SM11 must not own",
    "Real pilot authorization packet preparation definition",
    "Real packet versus dry packet boundary",
    "Preparation eligibility prerequisites",
    "Legal/IP and external-reference preparation posture",
    "No-donor-in-repository preparation rule",
    "SM02 no-waiver preparation requirement",
    "SM03 dry-run preparation requirement",
    "SM04 evaluation-rubric preparation requirement",
    "SM05 authorization-slot preparation requirement",
    "SM06 execution/output-capture preparation requirement",
    "SM07 scaffold/review-harness preparation requirement",
    "SM08 no-donor safety preparation requirement",
    "SM09 dry template preparation requirement",
    "SM10 reviewer validation preparation requirement",
    "Packet scope and C-family pressure preparation",
    "Metadata-only packet identity preparation",
    "Evidence/provenance reference preparation",
    "Lawful outcome and mapping ledger preparation",
    "Rejected-import, source-local, legal/IP, and `pending_schema` preparation",
    "Confidence, review-routing, repair, quarantine, and failure-report preparation",
    "Donor leakage hard-fail preparation",
    "Preparation review workflow",
    "Preparation decision labels",
    "Preparation record requirements",
    "What SM11 preparation may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM11",
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
    "SM09",
    "SM10",
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

REFUSAL_TERMS = [
    "real copyrighted donor excerpts",
    "donor statblocks",
    "donor tables",
    "donor maps",
    "donor setting prose",
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
    "rewrite C00-C14",
    "add C15",
    "D00-D19",
    "RHBF",
    "waive SM02",
    "bypass SM05",
    "treat SM11 preparation as execution approval",
    "treat no-donor sentinel checks as legal/IP clearance",
]

HARD_NON_GOALS = [
    "create a real authorization packet",
    "authorize actual execution",
    "approve execution",
    "run conversion",
    "create actual converted donor content",
    "create actual pilot outputs",
    "select, embed, quote, paraphrase, transform, summarize, or convert real copyrighted donor excerpts",
    "embed donor statblocks",
    "embed donor tables",
    "embed donor maps",
    "embed donor setting prose",
    "create final output schemas",
    "create JSON Schema files",
    "create Pydantic models",
    "create runtime schemas",
    "create backend schemas",
    "create database schemas",
    "create entity/component/event schemas",
    "create command lifecycle contracts",
    "create context packet contracts",
    "create save-state shapes",
    "create resolution dice",
    "create damage formulas",
    "create resource formulas",
    "create progression math",
    "donor-statblock validators that treat donor statblocks as Astra defaults",
    "promote C00-C14 registry statuses",
    "create canon/sourcebook/live-play/training content",
]

PREPARATION_LABELS = [
    "preparation_ready_for_real_packet_drafting",
    "preparation_blocked_by_missing_sm02_gate",
    "preparation_blocked_by_missing_sm05_slot",
    "preparation_blocked_by_missing_sm10_validation_posture",
    "preparation_blocked_by_legal_ip_gap",
    "preparation_blocked_by_external_reference_gap",
    "preparation_blocked_by_scope_expansion",
    "preparation_blocked_by_donor_content_risk",
    "preparation_blocked_by_runtime_or_mechanics_creep",
    "preparation_requires_repair",
    "preparation_requires_quarantine",
    "preparation_not_authorization",
    "preparation_not_execution_approval",
]

WORKFLOW_STEPS = [
    "Confirm SM00-SM10 are present and current.",
    "Confirm the future packet is not being created in this PR.",
    "Confirm no real donor content is embedded in this PR.",
    "Confirm metadata-only / external-reference posture is used.",
    "Confirm legal/IP owner is named.",
    "Confirm SM02 no-waiver posture.",
    "Confirm SM03 dry-run posture.",
    "Confirm SM04 rubric and handoff posture.",
    "Confirm SM05 authorization slot posture.",
    "Confirm SM06 output-capture posture.",
    "Confirm SM07 scaffold/review-harness posture.",
    "Confirm SM08 no-donor safety posture.",
    "Confirm SM09 dry template slot posture.",
    "Confirm SM10 reviewer decision-gate posture.",
    "Confirm C-family scope remains bounded.",
    "Confirm lawful outcome, mapping, rejected-import, source-local, legal/IP, `pending_schema`, confidence, review-routing, repair, quarantine, and failure-report preparation.",
    "Confirm donor leakage hard-fail criteria.",
    "Assign document-local preparation label.",
    "Record preparation rationale.",
    "Route failures to repair, quarantine, deferred gap ledger, `pending_schema`, legal/IP review, or appropriate future owner.",
    "State exactly what preparation may and may not prove.",
]

MAY_PROVE = [
    "the project has preparation controls for a future real authorization packet",
    "the packet can be prepared without embedding donor content in the repo",
    "legal/IP and external-reference owner routing can be named",
    "required upstream SM02-SM10 dependencies can be represented",
    "future real packet drafting can be more consistent",
]

MAY_NOT_PROVE = [
    "actual authorization",
    "execution approval",
    "legal/IP clearance",
    "real packet completeness",
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
    r'"type":\s*"object"',
    r"CREATE\s+TABLE",
    r"command lifecycle contract\s*:",
    r"context packet contract\s*:",
    r"save-state shape\s*:",
    r"converted output\s*:",
    r"donor excerpt\s*:",
    r"statblock\s*:",
    r"source table\s*:",
    r"source map\s*:",
    r"donor prose excerpt\s*:",
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

def _content() -> str:
    return read_utf8(SM11_PATH)


def _assert_terms(content: str, terms: list[str], label: str) -> None:
    missing = [term for term in terms if term not in content]
    assert not missing, f"Missing {label}: {missing}"


def test_sm11_file_exists_and_nonempty():
    assert SM11_PATH.exists(), f"SM11 file not found at {SM11_PATH}"
    assert _content().strip(), "SM11 file is empty"


def test_sm11_required_sections_present_in_order():
    content = _content()
    last_index = -1
    for index, section in enumerate(REQUIRED_SECTIONS, start=1):
        heading = f"## {index}. {section}"
        current_index = content.find(heading)
        assert current_index != -1, f"Missing required section heading: {heading}"
        assert current_index > last_index, f"Section heading out of order: {heading}"
        last_index = current_index


def test_sm11_names_required_repo_state_controls():
    content = _content()
    _assert_terms(content, REQUIRED_NAMES, "required control name")
    _assert_terms(content, [f"C{index:02d}" for index in range(15)], "C-family token")


def test_sm11_states_preparation_control_only_and_no_execution_or_conversion():
    content = _content().lower()
    assert "real pilot authorization packet preparation-control file only" in content
    assert "does not create a real authorization packet" in content
    assert "does not make an actual authorization decision" in content
    assert "does not authorize actual execution" in content
    assert "does not approve execution" in content
    assert "does not run conversion" in content
    assert "does not create actual converted donor content or pilot outputs" in content
    assert "not an authorization decision" in content
    assert "not execution approval" in content
    assert "not legal/ip clearance" in content


def test_sm11_refuses_required_non_goals():
    content = _content()
    _assert_terms(content, REFUSAL_TERMS, "refusal/non-goal term")
    _assert_terms(content, HARD_NON_GOALS, "hard non-goal term")


def test_sm11_distinguishes_real_dry_preparation_future_packet_and_execution_pr():
    content = _content()
    boundary_terms = [
        "SM09 dry authorization packet template: placeholder/synthetic/non-donor template.",
        "SM10 dry authorization validation: reviewer gate for dry packets.",
        "SM11 preparation controls: controls for preparing a future real authorization packet.",
        "Future real authorization packet: not created by SM11.",
        "Future execution PR: not created by SM11 and still downstream.",
    ]
    _assert_terms(content, boundary_terms, "real/dry/preparation/future boundary term")


def test_sm11_includes_metadata_external_reference_and_legal_ip_boundaries():
    content = _content()
    _assert_terms(
        content,
        [
            "metadata-only / external-reference preparation posture",
            "Real donor material must not be embedded in this PR",
            "controlled metadata or external-reference posture",
            "Any external reference must be reviewed by a legal/IP owner before execution is proposed",
            "Metadata is not legal/IP clearance",
            "External-reference readiness is not source clearance",
            "No-donor sentinel tests are not legal/IP clearance",
        ],
        "metadata/external-reference/legal-IP boundary",
    )


def test_sm11_includes_preparation_eligibility_prerequisites():
    content = _content()
    prerequisites = [
        "SM02 gates have no waived minimum gate",
        "SM03 dry-run posture is represented",
        "SM04 rubric and handoff are represented",
        "SM05 authorization slots are represented",
        "SM06 output-capture slots are represented",
        "SM07 scaffold/review-harness slots are represented",
        "SM08 no-donor safety posture is represented",
        "SM09 dry template slot structure is available",
        "SM10 reviewer validation posture is available",
        "Legal/IP owner is named",
        "Future review owner is named",
        "Repair/quarantine/failure-report paths are named",
    ]
    _assert_terms(content, prerequisites, "preparation eligibility prerequisite")


def test_sm11_preserves_c_family_pressure_and_deferred_families():
    content = _content()
    pressure_terms = [
        "C01 creature/NPC",
        "C02 item/gear",
        "C03 ability/power/technique",
        "C10 table/oracle",
        "conditional C14 source-local setting/cosmology only if legal/IP/source-local routing is ready",
        "C05, C06, C07, C08, C11, C12, and C13 remain deferred",
        "C04 and C09 may also remain deferred unless needed to disambiguate C01/C02/C03/C10 pressure",
        "normally tiny packet count of 3-5 packet candidates",
        "must not expand beyond authorization",
    ]
    _assert_terms(content, pressure_terms, "C-family pressure/deferred-family term")


def test_sm11_includes_preparation_decision_labels_and_registry_boundary():
    content = _content()
    _assert_terms(content, PREPARATION_LABELS, "preparation decision label")
    lower = content.lower()
    assert "document-local preparation labels only" in lower
    assert "they are not registry values" in lower
    for field in ["status", "authority_level", "test_status", "review_status"]:
        assert field in content


def test_sm11_includes_preparation_review_workflow_steps():
    _assert_terms(_content(), WORKFLOW_STEPS, "preparation workflow step")


def test_sm11_states_what_preparation_may_and_may_not_prove():
    content = _content()
    _assert_terms(content, MAY_PROVE, "may-prove claim")
    _assert_terms(content, MAY_NOT_PROVE, "may-not-prove claim")


def test_sm11_includes_non_readiness_owner_routing_risks_and_next_pr():
    content = _content()
    lower = content.lower()
    assert "large-scale conversion non-readiness boundary" in lower
    assert "runtime/canon/sourcebook/live-play/training non-readiness boundary" in lower
    assert "owner routing" in lower
    assert "lawful fallbacks" in lower
    assert "risk register" in lower
    assert "sm12 real pilot authorization packet external-reference review gate" in lower
    assert "sm12 real packet preparation repair and legal-ip routing controls" in lower
    _assert_terms(
        content,
        [
            "actual donor conversion",
            "broad conversion",
            "final mechanics",
            "runtime schemas",
            "canon consolidation",
            "sourcebook prose",
            "live-play adapter behavior",
            "training corpus creation",
            "real donor-content ingestion",
        ],
        "forbidden next-step jump boundary",
    )


def test_sm11_contains_no_obvious_implementation_or_donor_artifacts():
    content = _content()
    for pattern in IMPLEMENTATION_ARTIFACT_PATTERNS:
        assert not re.search(pattern, content, re.IGNORECASE | re.MULTILINE), (
            f"SM11 appears to contain implementation or donor artifact matching {pattern!r}"
        )
    for sentinel in DONOR_PROPER_NOUN_SENTINELS:
        assert sentinel not in content, f"SM11 contains donor proper-noun sentinel: {sentinel}"


def test_sm09_dry_authorization_packet_template_remains_safe_markdown_direct_child():
    assert DRY_TEMPLATE_PATH.exists(), "SM09 dry authorization packet template is missing"
    assert DRY_TEMPLATE_PATH.suffix == ".md"
    assert DRY_TEMPLATE_PATH.parent == SCAFFOLD_DIR
    content = read_utf8(DRY_TEMPLATE_PATH)
    lower = content.lower()
    assert content.strip()
    for required in ["placeholder", "synthetic", "non-donor"]:
        assert required in lower
    no_donor_terms = [
        "no real donor content",
        "no protected source expression",
        "no copied mechanical blocks",
        "no copied tables",
        "no copied maps",
        "no copied setting prose",
        "no protected source names",
        "not converted content",
        "not training data",
        "not canon",
        "not sourcebook prose",
        "not benchmark corpora",
        "not evaluation corpora",
        "not runtime import data",
    ]
    _assert_terms(content, no_donor_terms, "dry template no-donor safety term")
    _assert_terms(content, REQUIRED_DRY_TEMPLATE_SLOTS, "dry template required slot")
    for sentinel in DONOR_PROPER_NOUN_SENTINELS:
        assert sentinel not in content, f"Dry template contains donor proper-noun sentinel: {sentinel}"


def test_c00_c14_registry_records_not_promoted_to_forbidden_states():
    registry = read_utf8(REGISTRY_PATH)
    forbidden_sm11_promotion_states = {
        "canon-promoted",
        "canon-current",
        "runtime-ready",
        "sourcebook-ready",
        "live-play-ready",
        "training-ready",
        "final-mechanics-ready",
        "execution-authority",
        "authorization-authority",
    }

    for file_id in [f"C{index:02d}" for index in range(15)]:
        match = re.search(
            rf"^- file_id: {file_id}\n(?P<body>.*?)(?=^- file_id: |\Z)",
            registry,
            re.MULTILINE | re.DOTALL,
        )
        assert match, f"Missing registry record for {file_id}"
        body = match.group("body")
        for field in ["status", "test_status", "review_status"]:
            field_match = re.search(rf"^  {field}: ['\"]?(?P<value>[^'\"\n]+)['\"]?", body, re.MULTILINE)
            assert field_match, f"Missing {field} for {file_id}"
            value = field_match.group("value")
            assert value not in forbidden_sm11_promotion_states, (
                f"{file_id} {field} violates SM11 boundaries with {value!r}"
            )
        authority_match = re.search(r"^  authority_level: ['\"]?(?P<value>[^'\"\n]+)['\"]?", body, re.MULTILINE)
        assert authority_match, f"Missing authority_level for {file_id}"
        authority_value = authority_match.group("value")
        assert authority_value not in forbidden_sm11_promotion_states, (
            f"{file_id} authority_level violates SM11 boundaries with {authority_value!r}"
        )
