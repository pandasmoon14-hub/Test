import re

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM13_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM13_real_pilot_authorization_packet_metadata_only_assembly_controls.md"
)

SCAFFOLD_DIR = ROOT / "tests" / "fixtures" / "pilot_conversion_scaffold"
DRY_TEMPLATE_PATH = SCAFFOLD_DIR / "dry_authorization_packet_template.md"

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing metadata-only assembly posture",
    "What SM13 owns",
    "What SM13 must not own",
    "Metadata-only assembly definition",
    "Packet shell versus completed packet boundary",
    "Metadata-only assembly eligibility requirements",
    "No-donor-in-repository assembly rule",
    "Legal/IP and external-reference assembly posture",
    "Source access and source-clearance assembly boundary",
    "SM02 no-waiver assembly requirement",
    "SM03 dry-run assembly requirement",
    "SM04 evaluation-rubric assembly requirement",
    "SM05 authorization-slot assembly requirement",
    "SM06 execution/output-capture assembly requirement",
    "SM07 scaffold/review-harness assembly requirement",
    "SM08 no-donor safety assembly requirement",
    "SM09 dry template assembly requirement",
    "SM10 reviewer validation assembly requirement",
    "SM11 preparation-control assembly requirement",
    "SM12 external-reference review assembly requirement",
    "Packet shell section map",
    "Metadata-only reference slot map",
    "Packet scope and C-family pressure assembly",
    "Evidence/provenance pointer assembly",
    "Lawful outcome and mapping ledger assembly",
    "Rejected-import, source-local, legal/IP, and `pending_schema` assembly",
    "Confidence, review-routing, repair, quarantine, and failure-report assembly",
    "Donor leakage hard-fail assembly",
    "Assembly review workflow",
    "Metadata-only assembly labels",
    "Assembly record requirements",
    "What SM13 assembly may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM13",
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
    "SM12",
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
    "treat SM13 metadata-only assembly as execution approval",
    "treat no-donor sentinel checks as legal/IP clearance",
    "treat external-reference readiness as source clearance",
    "treat metadata as donor content or conversion evidence",
]

HARD_NON_GOALS = [
    "create a completed real authorization packet",
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

BOUNDARY_DISTINCTIONS = [
    "SM09 dry template: placeholder/synthetic/non-donor template.",
    "SM10 dry validation gate: validation of dry packets.",
    "SM11 preparation controls: controls for preparing a future real packet.",
    "SM12 external-reference review gate: review of metadata-only external references.",
    "SM13 metadata-only assembly controls: arrangement of shell sections and metadata-only slots.",
    "Future completed real authorization packet: not created by SM13.",
    "Future execution PR: not created by SM13 and still downstream.",
]

PACKET_SHELL_SLOTS = [
    "packet identity metadata",
    "assembly status and non-execution statement",
    "SM02 no-waiver posture",
    "SM03 dry-run posture",
    "SM04 evaluation/rubric handoff",
    "SM05 authorization slot",
    "SM06 execution/output-capture slot",
    "SM07 scaffold/review-harness slot",
    "SM08 no-donor safety slot",
    "SM09 dry template reference",
    "SM10 reviewer validation slot",
    "SM11 preparation-control slot",
    "SM12 external-reference review slot",
    "legal/IP owner",
    "future review owner",
    "source access posture",
    "source-clearance boundary",
    "external-reference metadata",
    "C-family pressure target",
    "lawful outcome route",
    "mapping ledger route",
    "rejected-import route",
    "source-local retention route",
    "legal/IP route",
    "`pending_schema` route",
    "confidence/review-routing notes",
    "repair route",
    "quarantine route",
    "failure-report route",
    "donor leakage hard-fail criteria",
    "final non-readiness statement",
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

ASSEMBLY_LABELS = [
    "metadata_assembly_ready_for_packet_shell_review",
    "metadata_assembly_blocked_by_missing_sm02_gate",
    "metadata_assembly_blocked_by_missing_sm05_slot",
    "metadata_assembly_blocked_by_missing_sm12_review_posture",
    "metadata_assembly_blocked_by_missing_legal_ip_owner",
    "metadata_assembly_blocked_by_source_clearance_gap",
    "metadata_assembly_blocked_by_embedded_donor_content",
    "metadata_assembly_blocked_by_scope_expansion",
    "metadata_assembly_blocked_by_runtime_or_mechanics_creep",
    "metadata_assembly_requires_repair",
    "metadata_assembly_requires_quarantine",
    "metadata_assembly_not_authorization",
    "metadata_assembly_not_execution_approval",
]

WORKFLOW_STEPS = [
    "Confirm SM00-SM12 are present and current.",
    "Confirm no completed real authorization packet is created in this PR.",
    "Confirm no real donor content is embedded in this PR.",
    "Confirm assembly is metadata-only.",
    "Confirm legal/IP owner slot exists.",
    "Confirm future review owner slot exists.",
    "Confirm metadata is not treated as legal/IP clearance.",
    "Confirm external-reference readiness is not treated as source clearance.",
    "Confirm SM02 no-waiver slot.",
    "Confirm SM03 dry-run slot.",
    "Confirm SM04 rubric and handoff slot.",
    "Confirm SM05 authorization slot.",
    "Confirm SM06 output-capture slot.",
    "Confirm SM07 scaffold/review-harness slot.",
    "Confirm SM08 no-donor safety slot.",
    "Confirm SM09 dry template reference.",
    "Confirm SM10 reviewer decision-gate slot.",
    "Confirm SM11 preparation-control slot.",
    "Confirm SM12 external-reference review slot.",
    "Confirm C-family scope remains bounded.",
    "Confirm lawful outcome, mapping, rejected-import, source-local, legal/IP, `pending_schema`, confidence, review-routing, repair, quarantine, and failure-report slot posture.",
    "Confirm donor leakage hard-fail criteria.",
    "Assign document-local metadata-only assembly label.",
    "Record assembly rationale.",
    "Route failures to repair, quarantine, deferred gap ledger, `pending_schema`, legal/IP review, source-local retention, rejected import, or appropriate future owner.",
    "State exactly what metadata-only assembly may and may not prove.",
]

MAY_PROVE = [
    "the project has assembly controls for a metadata-only future authorization packet shell",
    "required packet shell sections and metadata-only slots can be arranged safely",
    "legal/IP and external-reference owner routing can be represented",
    "SM02-SM12 dependency slots can be represented",
    "obvious assembly failures can be routed before a real packet is completed",
]

MAY_NOT_PROVE = [
    "actual authorization",
    "execution approval",
    "legal/IP clearance",
    "source clearance",
    "completed real packet quality",
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
    return read_utf8(SM13_PATH)


def _assert_terms(content: str, terms: list[str], label: str) -> None:
    missing = [term for term in terms if term not in content]
    assert not missing, f"Missing {label}: {missing}"


def test_sm13_file_exists_and_is_nonempty():
    assert SM13_PATH.exists(), "SM13 doctrine/control file is missing"
    assert SM13_PATH.is_file()
    assert _content().strip()


def test_sm13_required_section_headings_are_present_and_in_order():
    content = _content()
    previous = -1
    for index, heading in enumerate(REQUIRED_SECTIONS, start=1):
        marker = f"## {index}. {heading}"
        position = content.find(marker)
        assert position != -1, f"Missing required heading: {marker}"
        assert position > previous, f"Heading out of order: {marker}"
        previous = position


def test_sm13_names_required_upstream_and_boundary_doctrine():
    content = _content()
    _assert_terms(content, REQUIRED_NAMES, "required doctrine/control name")
    _assert_terms(content, [f"C{index:02d}" for index in range(15)], "C-family token")


def test_sm13_states_assembly_only_and_core_non_authority_boundaries():
    _assert_terms(
        _content(),
        [
            "SM13 is a real pilot authorization packet metadata-only assembly-control file only",
            "SM13 does not create a completed real authorization packet",
            "SM13 does not make an actual authorization decision",
            "SM13 does not authorize actual execution",
            "SM13 does not approve execution",
            "SM13 does not run conversion",
            "SM13 does not create actual converted donor content or pilot outputs",
        ],
        "core SM13 boundary",
    )


def test_sm13_refuses_required_non_goals_and_authority_creep():
    content = _content()
    _assert_terms(content, REFUSAL_TERMS, "refusal term")
    _assert_terms(content, HARD_NON_GOALS, "hard non-goal")


def test_sm13_distinguishes_dry_real_review_assembly_and_execution_boundaries():
    _assert_terms(_content(), BOUNDARY_DISTINCTIONS, "boundary distinction")


def test_sm13_includes_packet_shell_section_map_and_reference_slot_map():
    content = _content()
    assert "## 23. Packet shell section map" in content
    assert "## 24. Metadata-only reference slot map" in content
    _assert_terms(content, PACKET_SHELL_SLOTS, "packet shell slot")
    _assert_terms(content, METADATA_CATEGORIES, "metadata-only reference category")


def test_sm13_includes_metadata_categories_without_creating_final_schema_fields():
    content = _content()
    _assert_terms(content, METADATA_CATEGORIES, "metadata category")
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


def test_sm13_states_metadata_and_sentinel_boundaries():
    _assert_terms(
        _content(),
        [
            "Metadata-only assembly is not donor content, not legal/IP clearance, not source clearance, not conversion evidence, not canon evidence, and not execution approval.",
            "Metadata is not legal/IP clearance.",
            "No-donor sentinel checks are not legal/IP clearance.",
            "External-reference readiness is not source clearance.",
        ],
        "metadata/no-donor/external-reference boundary",
    )


def test_sm13_preserves_c_family_pressure_and_deferred_families():
    _assert_terms(
        _content(),
        [
            "C01 creature/NPC",
            "C02 item/gear",
            "C03 ability/power/technique",
            "C10 table/oracle",
            "conditional C14 source-local setting/cosmology only if legal/IP/source-local routing is ready",
            "C05, C06, C07, C08, C11, C12, and C13 remain deferred",
            "C04 and C09 may also remain deferred unless needed to disambiguate C01/C02/C03/C10 pressure",
            "normally tiny packet count of 3-5 packet candidates",
            "must not expand beyond authorization",
        ],
        "C-family pressure/deferred-family term",
    )


def test_sm13_includes_metadata_only_assembly_labels_and_registry_boundary():
    content = _content()
    _assert_terms(content, ASSEMBLY_LABELS, "metadata-only assembly label")
    lower = content.lower()
    assert "document-local metadata-only assembly labels only" in lower
    assert "they are not registry values" in lower
    for field in ["status", "authority_level", "test_status", "review_status"]:
        assert field in content


def test_sm13_includes_assembly_review_workflow_steps():
    _assert_terms(_content(), WORKFLOW_STEPS, "assembly review workflow step")


def test_sm13_states_what_metadata_only_assembly_may_and_may_not_prove():
    content = _content()
    _assert_terms(content, MAY_PROVE, "may-prove claim")
    _assert_terms(content, MAY_NOT_PROVE, "may-not-prove claim")


def test_sm13_includes_non_readiness_owner_routing_risks_and_next_pr():
    content = _content()
    lower = content.lower()
    assert "large-scale conversion non-readiness boundary" in lower
    assert "runtime/canon/sourcebook/live-play/training non-readiness boundary" in lower
    assert "owner routing" in lower
    assert "lawful fallbacks" in lower
    assert "risk register" in lower
    assert "sm14 metadata-only real packet shell validation and reviewer gate" in lower
    assert "sm14 metadata-only assembly repair and slot-hardening controls" in lower
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


def test_sm13_contains_no_obvious_implementation_or_donor_artifacts():
    content = _content()
    for pattern in IMPLEMENTATION_ARTIFACT_PATTERNS:
        assert not re.search(pattern, content, re.IGNORECASE | re.MULTILINE), (
            f"SM13 appears to contain implementation or donor artifact matching {pattern!r}"
        )
    for sentinel in DONOR_PROPER_NOUN_SENTINELS:
        assert sentinel not in content, f"SM13 contains donor proper-noun sentinel: {sentinel}"


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
    forbidden_sm13_promotion_states = {
        "canon-promoted",
        "canon-current",
        "runtime-ready",
        "sourcebook-ready",
        "live-play-ready",
        "training-ready",
        "final-mechanics-ready",
        "execution-authority",
        "authorization-authority",
        "metadata-only-assembly-authority",
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
            assert value not in forbidden_sm13_promotion_states, (
                f"{file_id} {field} violates SM13 boundaries with {value!r}"
            )
        authority_match = re.search(r"^  authority_level: ['\"]?(?P<value>[^'\"\n]+)['\"]?", body, re.MULTILINE)
        assert authority_match, f"Missing authority_level for {file_id}"
        authority_value = authority_match.group("value")
        assert authority_value not in forbidden_sm13_promotion_states, (
            f"{file_id} authority_level violates SM13 boundaries with {authority_value!r}"
        )
