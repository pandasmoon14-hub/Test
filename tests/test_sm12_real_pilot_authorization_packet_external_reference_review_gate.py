import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM12_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM12_real_pilot_authorization_packet_external_reference_review_gate.md"
)

SCAFFOLD_DIR = ROOT / "tests" / "fixtures" / "pilot_conversion_scaffold"
DRY_TEMPLATE_PATH = SCAFFOLD_DIR / "dry_authorization_packet_template.md"

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing external-reference review posture",
    "What SM12 owns",
    "What SM12 must not own",
    "External-reference review gate definition",
    "Real packet, preparation, review gate, and execution boundary",
    "External-reference eligibility requirements",
    "Metadata-only reference posture",
    "No-donor-in-repository review rule",
    "Legal/IP owner review requirement",
    "Source access and source-clearance boundary",
    "SM02 no-waiver review requirement",
    "SM03 dry-run review requirement",
    "SM04 evaluation-rubric review requirement",
    "SM05 authorization-slot review requirement",
    "SM06 execution/output-capture review requirement",
    "SM07 scaffold/review-harness review requirement",
    "SM08 no-donor safety review requirement",
    "SM09 dry template review requirement",
    "SM10 reviewer validation review requirement",
    "SM11 preparation-control review requirement",
    "Packet scope and C-family pressure review",
    "External-reference metadata review checklist",
    "Evidence/provenance pointer review",
    "Lawful outcome and mapping reference review",
    "Rejected-import, source-local, legal/IP, and `pending_schema` reference review",
    "Confidence, review-routing, repair, quarantine, and failure-report review",
    "Donor leakage hard-fail review",
    "External-reference review workflow",
    "External-reference review labels",
    "External-reference review record requirements",
    "What SM12 review may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM12",
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
    "SM11",
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
    "treat SM12 external-reference review as execution approval",
    "treat no-donor sentinel checks as legal/IP clearance",
    "treat external-reference readiness as source clearance",
    "treat metadata as donor content or conversion evidence",
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
    "rewrite C00-C14",
    "add C15",
    "create canon/sourcebook/live-play/training content",
]

METADATA_CATEGORIES = [
    "internal packet candidate id",
    "donor-family category",
    "source access status",
    "legal/IP review status",
    "source hash or hash-later policy",
    "page/range reference posture",
    "external-reference pointer status",
    "extraction-readiness route",
    "review owner",
    "legal/IP owner",
    "C-family pressure target",
    "lawful outcome route",
    "source-local / rejected-import / quarantine route",
    "failure-report route",
]

EXTERNAL_REFERENCE_LABELS = [
    "external_reference_review_ready_for_real_packet_review",
    "external_reference_blocked_by_missing_legal_ip_owner",
    "external_reference_blocked_by_source_clearance_gap",
    "external_reference_blocked_by_embedded_donor_content",
    "external_reference_blocked_by_missing_sm02_gate",
    "external_reference_blocked_by_missing_sm05_slot",
    "external_reference_blocked_by_missing_sm11_preparation_posture",
    "external_reference_blocked_by_scope_expansion",
    "external_reference_blocked_by_donor_content_risk",
    "external_reference_blocked_by_runtime_or_mechanics_creep",
    "external_reference_requires_repair",
    "external_reference_requires_quarantine",
    "external_reference_not_authorization",
    "external_reference_not_execution_approval",
]

WORKFLOW_STEPS = [
    "Confirm SM00-SM11 are present and current.",
    "Confirm no real authorization packet is created in this PR.",
    "Confirm no real donor content is embedded in this PR.",
    "Confirm external references are metadata-only.",
    "Confirm legal/IP owner is named.",
    "Confirm future review owner is named.",
    "Confirm metadata is not treated as legal/IP clearance.",
    "Confirm external-reference readiness is not treated as source clearance.",
    "Confirm SM02 no-waiver posture.",
    "Confirm SM03 dry-run posture.",
    "Confirm SM04 rubric and handoff posture.",
    "Confirm SM05 authorization slot posture.",
    "Confirm SM06 output-capture posture.",
    "Confirm SM07 scaffold/review-harness posture.",
    "Confirm SM08 no-donor safety posture.",
    "Confirm SM09 dry template slot posture.",
    "Confirm SM10 reviewer decision-gate posture.",
    "Confirm SM11 preparation-control posture.",
    "Confirm C-family scope remains bounded.",
    "Confirm lawful outcome, mapping, rejected-import, source-local, legal/IP, `pending_schema`, confidence, review-routing, repair, quarantine, and failure-report reference posture.",
    "Confirm donor leakage hard-fail criteria.",
    "Assign document-local external-reference review label.",
    "Record review rationale.",
    "Route failures to repair, quarantine, deferred gap ledger, `pending_schema`, legal/IP review, source-local retention, rejected import, or appropriate future owner.",
    "State exactly what external-reference review may and may not prove.",
]

MAY_PROVE = [
    "the project has a review gate for metadata-only external references",
    "future packet references can be reviewed without embedding donor content in the repo",
    "legal/IP and external-reference owner routing can be checked",
    "required upstream SM02-SM11 dependencies can be represented",
    "obvious reference-safety failures can be routed before execution is proposed",
]

MAY_NOT_PROVE = [
    "actual authorization",
    "execution approval",
    "legal/IP clearance",
    "source clearance",
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

IMPLEMENTATION_ARTIFACT_PATTERNS = [
    r'"\$schema"\s*:',
    r'"type"\s*:\s*"object"',
    r"^\s*class\s+\w+\([^)]*BaseModel[^)]*\):",
    r"^\s*CREATE\s+TABLE\s+",
    r"^\s*ALTER\s+TABLE\s+",
    r"command lifecycle contract\s*:",
    r"context packet contract\s*:",
    r"save-state shape\s*:",
    r"converted donor content\s*:",
    r"donor statblock\s*:",
    r"donor table\s*:",
    r"donor map\s*:",
    r"donor prose excerpt\s*:",
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
]

REQUIRED_DRY_TEMPLATE_SLOTS = [
    "SM05 authorization decision",
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
    "source hash or hash-later policy",
    "lawful outcome ledger",
    "mapping ledger",
    "rejected-import ledger",
    "source-local retention ledger",
    "pending_schema ledger",
    "repair queue status",
    "quarantine queue status",
    "confidence/review-routing notes",
    "legal/IP flags",
    "failure report shape",
    "final non-readiness statement",
]


def _content() -> str:
    return read_utf8(SM12_PATH)


def _assert_terms(content: str, terms: list[str], label: str) -> None:
    missing = [term for term in terms if term not in content]
    assert not missing, f"Missing {label}: {missing}"


def test_sm12_file_exists_and_is_nonempty():
    assert SM12_PATH.exists(), "SM12 doctrine/control file is missing"
    assert SM12_PATH.is_file()
    assert _content().strip()


def test_sm12_required_section_headings_are_present_and_in_order():
    content = _content()
    previous = -1
    for index, heading in enumerate(REQUIRED_SECTIONS, start=1):
        marker = f"## {index}. {heading}"
        position = content.find(marker)
        assert position != -1, f"Missing required heading: {marker}"
        assert position > previous, f"Heading out of order: {marker}"
        previous = position


def test_sm12_names_required_upstream_and_boundary_doctrine():
    _assert_terms(_content(), REQUIRED_NAMES, "required doctrine/control name")


def test_sm12_states_review_gate_only_and_core_non_authority_boundaries():
    content = _content()
    _assert_terms(
        content,
        [
            "SM12 is a real pilot authorization packet external-reference review gate only",
            "SM12 does not create a real authorization packet",
            "SM12 does not make an actual authorization decision",
            "SM12 does not authorize actual execution",
            "SM12 does not approve execution",
            "SM12 does not run conversion",
            "SM12 does not create actual converted donor content or pilot outputs",
        ],
        "core SM12 boundary",
    )


def test_sm12_refuses_required_non_goals_and_authority_creep():
    content = _content()
    _assert_terms(content, REFUSAL_TERMS, "refusal term")
    _assert_terms(content, HARD_NON_GOALS, "hard non-goal")


def test_sm12_distinguishes_packet_preparation_review_and_execution_boundaries():
    content = _content()
    _assert_terms(
        content,
        [
            "Real packet: a future metadata-only authorization packet shell that is not created by SM12.",
            "Preparation: SM11 controls how the future packet is prepared for review without creating converted content.",
            "Review gate: SM12 controls how reviewers assess the future packet's metadata-only external references before any execution proposal.",
            "Future execution PR: a later owner-controlled proposal",
            "Passing SM12 review does not create a real packet",
        ],
        "boundary distinction",
    )


def test_sm12_includes_metadata_only_external_reference_posture_and_boundaries():
    content = _content()
    _assert_terms(
        content,
        [
            "metadata-only review of whether a future real authorization packet can identify candidate source material without copying donor content into the repository",
            "metadata-only external-reference posture",
            "Metadata is not donor content",
            "not legal/IP clearance",
            "not source clearance",
            "not conversion evidence",
            "not canon evidence",
            "not execution approval",
            "External-reference readiness is not source clearance",
            "No-donor sentinel checks are not legal/IP clearance",
        ],
        "metadata-only/external-reference posture",
    )


def test_sm12_includes_external_reference_eligibility_requirements():
    content = _content()
    requirements = [
        "legal/IP owner is named",
        "future review owner is named",
        "source access posture is reviewable",
        "source-clearance posture is not assumed",
        "reference metadata is sufficient for reviewers without copying protected expression",
        "no raw donor excerpts, statblocks, tables, maps, setting prose, protected expression, or donor proper nouns are embedded",
        "source-local and rejected-import routing are available",
        "quarantine route is available for unsafe references",
        "failure-report route is available",
        "SM02 gates have no waived minimum gate",
        "SM03-SM11 dependency posture is represented",
        "C-family pressure stays bounded",
    ]
    _assert_terms(content, requirements, "external-reference eligibility requirement")


def test_sm12_includes_metadata_categories_without_creating_final_schema_fields():
    content = _content()
    _assert_terms(content, METADATA_CATEGORIES, "external-reference metadata category")
    _assert_terms(
        content,
        [
            "must not create final schema fields",
            "not final schema fields",
            "not database fields",
            "not runtime contracts",
            "not final validators",
        ],
        "metadata category non-schema boundary",
    )


def test_sm12_preserves_c_family_pressure_and_deferred_families():
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


def test_sm12_includes_external_reference_review_labels_and_registry_boundary():
    content = _content()
    _assert_terms(content, EXTERNAL_REFERENCE_LABELS, "external-reference review label")
    lower = content.lower()
    assert "document-local external-reference review labels only" in lower
    assert "they are not registry values" in lower
    for field in ["status", "authority_level", "test_status", "review_status"]:
        assert field in content


def test_sm12_includes_external_reference_review_workflow_steps():
    _assert_terms(_content(), WORKFLOW_STEPS, "external-reference review workflow step")


def test_sm12_states_what_external_reference_review_may_and_may_not_prove():
    content = _content()
    _assert_terms(content, MAY_PROVE, "may-prove claim")
    _assert_terms(content, MAY_NOT_PROVE, "may-not-prove claim")


def test_sm12_includes_non_readiness_owner_routing_risks_and_next_pr():
    content = _content()
    lower = content.lower()
    assert "large-scale conversion non-readiness boundary" in lower
    assert "runtime/canon/sourcebook/live-play/training non-readiness boundary" in lower
    assert "owner routing" in lower
    assert "lawful fallbacks" in lower
    assert "risk register" in lower
    assert "sm13 real pilot authorization packet metadata-only assembly controls" in lower
    assert "sm13 external-reference review repair and legal-ip gate hardening controls" in lower
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


def test_sm12_contains_no_obvious_implementation_or_donor_artifacts():
    content = _content()
    for pattern in IMPLEMENTATION_ARTIFACT_PATTERNS:
        assert not re.search(pattern, content, re.IGNORECASE | re.MULTILINE), (
            f"SM12 appears to contain implementation or donor artifact matching {pattern!r}"
        )
    for sentinel in DONOR_PROPER_NOUN_SENTINELS:
        assert sentinel not in content, f"SM12 contains donor proper-noun sentinel: {sentinel}"


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
    forbidden_sm12_promotion_states = {
        "canon-promoted",
        "canon-current",
        "runtime-ready",
        "sourcebook-ready",
        "live-play-ready",
        "training-ready",
        "final-mechanics-ready",
        "execution-authority",
        "authorization-authority",
        "external-reference-review-authority",
        "real-pilot-authority",
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
            assert value not in forbidden_sm12_promotion_states, (
                f"{file_id} {field} violates SM12 boundaries with {value!r}"
            )
        authority_match = re.search(r"^  authority_level: ['\"]?(?P<value>[^'\"\n]+)['\"]?", body, re.MULTILINE)
        assert authority_match, f"Missing authority_level for {file_id}"
        authority_value = authority_match.group("value")
        assert authority_value not in forbidden_sm12_promotion_states, (
            f"{file_id} authority_level violates SM12 boundaries with {authority_value!r}"
        )
