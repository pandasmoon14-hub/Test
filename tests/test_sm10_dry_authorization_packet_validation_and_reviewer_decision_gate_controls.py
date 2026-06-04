import re
from pathlib import Path


from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM10_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM10_dry_authorization_packet_validation_and_reviewer_decision_gate_controls.md"
)

SCAFFOLD_DIR = ROOT / "tests" / "fixtures" / "pilot_conversion_scaffold"
DRY_TEMPLATE_PATH = SCAFFOLD_DIR / "dry_authorization_packet_template.md"

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing dry authorization validation posture",
    "What SM10 owns",
    "What SM10 must not own",
    "Dry authorization validation definition",
    "Reviewer decision-gate definition",
    "Completed dry packet eligibility requirements",
    "Placeholder and no-donor safety validation",
    "SM02 readiness gate validation",
    "SM03 dry-run result validation",
    "SM04 rubric readiness validation",
    "SM05 authorization decision-slot validation",
    "SM06 execution/output-capture validation",
    "SM07 scaffold/review-harness validation",
    "SM08 no-donor safety validation",
    "SM09 dry template compliance validation",
    "Packet scope and C-family pressure validation",
    "Evidence/provenance and construct-inventory validation",
    "Lawful outcome, mapping, rejected-import, source-local, legal/IP, and `pending_schema` validation",
    "Confidence, review-routing, repair, quarantine, and failure-report validation",
    "Donor leakage hard-fail validation",
    "Reviewer decision workflow",
    "Reviewer decision labels",
    "Decision record requirements",
    "What SM10 validation may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM10",
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
    "treat SM10 validation as execution approval",
    "treat no-donor sentinel checks as legal/IP clearance",
]

REVIEWER_LABELS = [
    "dry_packet_valid_for_reviewer_consideration",
    "dry_packet_blocked_by_missing_sm02_gate",
    "dry_packet_blocked_by_missing_sm05_decision_slot",
    "dry_packet_blocked_by_missing_sm04_handoff",
    "dry_packet_blocked_by_no_donor_failure",
    "dry_packet_blocked_by_scope_expansion",
    "dry_packet_blocked_by_legal_ip_gap",
    "dry_packet_blocked_by_donor_leakage_risk",
    "dry_packet_blocked_by_runtime_or_mechanics_creep",
    "dry_packet_requires_repair",
    "dry_packet_requires_quarantine",
    "dry_packet_not_authorization",
    "dry_packet_not_execution_approval",
]

WORKFLOW_STEPS = [
    "Confirm the packet is dry, placeholder/synthetic/non-donor, and not real donor content.",
    "Confirm all SM09 required template slots are present.",
    "Confirm SM02 no-waiver posture is represented.",
    "Confirm SM03 dry-run result slot is represented.",
    "Confirm SM04 rubric readiness and handoff slot are represented.",
    "Confirm SM05 authorization-decision slot is represented, while not treating the dry packet as actual authorization.",
    "Confirm SM06 output-capture slots are represented.",
    "Confirm SM07 scaffold/review harness slots are represented.",
    "Confirm SM08 no-donor validation posture is represented.",
    "Confirm packet scope and C-family pressure limits are represented.",
    "Confirm evidence/provenance, construct inventory, lawful outcome, mapping, rejected-import, source-local, legal/IP, `pending_schema`, confidence/review-routing, repair/quarantine, and failure-report slots are represented.",
    "Confirm donor leakage hard-fail criteria are represented.",
    "Assign document-local reviewer decision label.",
    "Record decision rationale.",
    "Route failures to repair, quarantine, deferred gap ledger, `pending_schema`, legal/IP review, or appropriate future owner.",
    "State exactly what the dry validation may and may not prove.",
]

MAY_PROVE = [
    "a dry authorization packet can be reviewed for completeness",
    "the SM09 dry template can be checked against reviewer criteria",
    "missing slots and owner gaps can be detected",
    "no-donor scaffold safety can be enforced at sentinel level",
    "reviewer decision records can be standardized",
]

MAY_NOT_PROVE = [
    "actual authorization",
    "execution approval",
    "conversion execution readiness",
    "conversion success",
    "pilot output quality",
    "pilot evaluation success",
    "legal/IP clearance",
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
    r"^\s*command_lifecycle\s*[:=]",
    r"^\s*context_packet\s*[:=]",
    r"^\s*save_state\s*[:=]",
    r"converted output:\s*\n\s*\S",
    r"donor excerpt:\s*\n\s*\S",
    r"statblock:\s*\n\s*\S",
    r"source table:\s*\n\s*\|",
    r"source map:\s*\n\s*\S",
    r"donor prose excerpt:\s*\n\s*\S",
]



def _content() -> str:
    return read_utf8(SM10_PATH)


def _assert_terms(content: str, terms: list[str], label: str) -> None:
    lower = content.lower()
    for term in terms:
        assert term.lower() in lower, f"Missing {label}: {term}"


def test_sm10_file_exists_and_nonempty():
    assert SM10_PATH.exists(), f"SM10 file not found at {SM10_PATH}"
    assert _content().strip(), "SM10 file is empty"


def test_sm10_required_section_headings_present_and_in_order():
    content = _content()
    last_index = -1
    for index, section in enumerate(REQUIRED_SECTIONS, start=1):
        heading = f"## {index}. {section}"
        current_index = content.find(heading)
        assert current_index != -1, f"Missing required section heading: {heading}"
        assert current_index > last_index, f"Section heading out of order: {heading}"
        last_index = current_index


def test_sm10_names_required_repo_state_controls():
    content = _content()
    _assert_terms(content, REQUIRED_NAMES, "required control name")
    _assert_terms(content, [f"C{index:02d}" for index in range(15)], "C-family token")


def test_sm10_states_dry_validation_gate_only_and_no_execution_or_conversion():
    content = _content().lower()
    assert "dry authorization packet validation and reviewer decision-gate control file only" in content
    assert "does not make an actual authorization decision" in content
    assert "does not authorize actual execution" in content
    assert "does not approve execution" in content
    assert "does not run conversion" in content
    assert "does not create actual converted donor content or pilot outputs" in content
    assert "not an authorization decision" in content
    assert "not execution approval" in content
    assert "not legal/ip clearance" in content


def test_sm10_refuses_required_non_goals():
    content = _content()
    _assert_terms(content, REFUSAL_TERMS, "refusal/non-goal term")
    hard_non_goal_terms = [
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
    _assert_terms(content, hard_non_goal_terms, "hard non-goal term")


def test_sm10_includes_reviewer_decision_labels_and_registry_boundary():
    content = _content()
    _assert_terms(content, REVIEWER_LABELS, "reviewer decision label")
    lower = content.lower()
    assert "document-local reviewer decision labels only" in lower
    assert "they are not registry values" in lower
    for field in ["status", "authority_level", "test_status", "review_status"]:
        assert field in content


def test_sm10_includes_reviewer_workflow_steps():
    content = _content()
    _assert_terms(content, WORKFLOW_STEPS, "reviewer workflow step")


def test_sm10_states_what_validation_may_and_may_not_prove():
    content = _content()
    _assert_terms(content, MAY_PROVE, "may-prove claim")
    _assert_terms(content, MAY_NOT_PROVE, "may-not-prove claim")


def test_sm10_includes_non_readiness_owner_routing_risks_and_next_pr():
    content = _content()
    lower = content.lower()
    assert "large-scale conversion non-readiness boundary" in lower
    assert "runtime/canon/sourcebook/live-play/training non-readiness boundary" in lower
    assert "owner routing" in lower
    assert "lawful fallbacks" in lower
    assert "risk register" in lower
    assert "sm11 real pilot authorization packet preparation controls" in lower
    assert "sm11 dry authorization review repair and reviewer calibration controls" in lower
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


def test_sm10_contains_no_obvious_implementation_or_donor_artifacts():
    content = _content()
    for pattern in IMPLEMENTATION_ARTIFACT_PATTERNS:
        assert not re.search(pattern, content, re.IGNORECASE | re.MULTILINE), (
            f"SM10 appears to contain implementation or donor artifact matching {pattern!r}"
        )
    for sentinel in DONOR_PROPER_NOUN_SENTINELS:
        assert sentinel not in content, f"SM10 contains donor proper-noun sentinel: {sentinel}"


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
    # SM10 must not freeze generic future owner-controlled registry progress.
    # This guard blocks only states that directly violate SM10 boundaries by
    # implying canon/sourcebook/live-play/training/runtime/final-mechanics or
    # execution/authorization authority.
    forbidden_sm10_promotion_states = {
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
        match = re.search(rf"^- file_id: {file_id}\n(?P<body>.*?)(?=^- file_id: |\Z)", registry, re.MULTILINE | re.DOTALL)
        assert match, f"Missing registry record for {file_id}"
        body = match.group("body")
        for field in ["status", "test_status", "review_status"]:
            field_match = re.search(rf"^  {field}: ['\"]?(?P<value>[^'\"\n]+)['\"]?", body, re.MULTILINE)
            assert field_match, f"Missing {field} for {file_id}"
            value = field_match.group("value")
            assert value not in forbidden_sm10_promotion_states, (
                f"{file_id} {field} violates SM10 boundaries with {value!r}"
            )
        authority_match = re.search(r"^  authority_level: ['\"]?(?P<value>[^'\"\n]+)['\"]?", body, re.MULTILINE)
        assert authority_match, f"Missing authority_level for {file_id}"
        authority_value = authority_match.group("value")
        assert authority_value not in forbidden_sm10_promotion_states, (
            f"{file_id} authority_level violates SM10 boundaries with {authority_value!r}"
        )
