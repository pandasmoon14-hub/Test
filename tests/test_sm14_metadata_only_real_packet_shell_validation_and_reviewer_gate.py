import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM14_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM14_metadata_only_real_packet_shell_validation_and_reviewer_gate.md"
)

SCAFFOLD_DIR = ROOT / "tests" / "fixtures" / "pilot_conversion_scaffold"
DRY_TEMPLATE_PATH = SCAFFOLD_DIR / "dry_authorization_packet_template.md"

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing shell-validation posture",
    "What SM14 owns",
    "What SM14 must not own",
    "Metadata-only shell validation definition",
    "Reviewer gate definition",
    "Packet shell versus completed packet validation boundary",
    "Validation eligibility requirements",
    "No-donor-in-repository validation rule",
    "Legal/IP and external-reference validation posture",
    "Source access and source-clearance validation boundary",
    "SM02 no-waiver validation requirement",
    "SM03 dry-run validation requirement",
    "SM04 evaluation-rubric validation requirement",
    "SM05 authorization-slot validation requirement",
    "SM06 execution/output-capture validation requirement",
    "SM07 scaffold/review-harness validation requirement",
    "SM08 no-donor safety validation requirement",
    "SM09 dry template validation requirement",
    "SM10 reviewer validation dependency requirement",
    "SM11 preparation-control validation requirement",
    "SM12 external-reference review validation requirement",
    "SM13 metadata-only assembly validation requirement",
    "Packet shell section completeness validation",
    "Metadata-only reference slot validation",
    "Packet scope and C-family pressure validation",
    "Evidence/provenance pointer validation",
    "Lawful outcome and mapping ledger validation",
    "Rejected-import, source-local, legal/IP, and `pending_schema` validation",
    "Confidence, review-routing, repair, quarantine, and failure-report validation",
    "Donor leakage hard-fail validation",
    "Shell validation workflow",
    "Reviewer decision labels",
    "Validation record requirements",
    "What SM14 validation may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM14",
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
    "SM13",
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
    "treat shell validation as execution approval",
    "treat no-donor sentinel checks as legal/IP clearance",
    "treat external-reference readiness as source clearance",
    "treat metadata as donor content or conversion evidence",
]

BOUNDARY_DISTINCTIONS = [
    "SM09 dry template: placeholder/synthetic/non-donor template.",
    "SM10 dry validation gate: validation of dry packets.",
    "SM11 preparation controls: controls for preparing a future real packet.",
    "SM12 external-reference review gate: review of metadata-only external references.",
    "SM13 metadata-only assembly controls: arrangement of shell sections and metadata-only slots.",
    "SM14 shell validation and reviewer gate: validation of the assembled metadata-only shell posture.",
    "Future completed real authorization packet: not created by SM14.",
    "Future authorization decision: not made by SM14.",
    "Future execution PR: not created by SM14 and still downstream.",
]

PACKET_SHELL_SLOTS = [
    "packet identity metadata",
    "shell validation status and non-execution statement",
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
    "SM13 metadata-only assembly slot",
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
    "reviewer decision label slot",
    "reviewer rationale slot",
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

REVIEWER_LABELS = [
    "shell_validation_ready_for_authorization_review",
    "shell_validation_blocked_by_missing_sm02_gate",
    "shell_validation_blocked_by_missing_sm05_slot",
    "shell_validation_blocked_by_missing_sm13_assembly_posture",
    "shell_validation_blocked_by_missing_legal_ip_owner",
    "shell_validation_blocked_by_source_clearance_gap",
    "shell_validation_blocked_by_embedded_donor_content",
    "shell_validation_blocked_by_scope_expansion",
    "shell_validation_blocked_by_runtime_or_mechanics_creep",
    "shell_validation_requires_repair",
    "shell_validation_requires_quarantine",
    "shell_validation_not_authorization",
    "shell_validation_not_execution_approval",
]

WORKFLOW_STEPS = [
    "Confirm SM00-SM13 are present and current.",
    "Confirm no completed real authorization packet is created in this PR.",
    "Confirm no actual authorization decision is made in this PR.",
    "Confirm no real donor content is embedded in this PR.",
    "Confirm the shell posture is metadata-only.",
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
    "Confirm SM13 metadata-only assembly slot.",
    "Confirm packet shell section completeness.",
    "Confirm metadata-only reference slot completeness.",
    "Confirm C-family scope remains bounded.",
    "Confirm lawful outcome, mapping, rejected-import, source-local, legal/IP, `pending_schema`, confidence, review-routing, repair, quarantine, and failure-report slot posture.",
    "Confirm donor leakage hard-fail criteria.",
    "Assign document-local shell validation label.",
    "Record validation rationale.",
    "Route failures to repair, quarantine, deferred gap ledger, `pending_schema`, legal/IP review, source-local retention, rejected import, or appropriate future owner.",
    "State exactly what metadata-only shell validation may and may not prove.",
]

MAY_PROVE = [
    "the project has reviewer-gate controls for a metadata-only real packet shell",
    "required shell sections and metadata-only slots can be reviewed for completeness",
    "legal/IP and external-reference owner routing can be checked",
    "SM02-SM13 dependency slots can be checked",
    "obvious shell-validation failures can be routed before authorization is considered",
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
    r"converted donor content:\s*\n\s*\S",
    r"converted output:\s*\n\s*\S",
    r"donor excerpt:\s*\n\s*\S",
    r"statblock:\s*\n\s*\S",
    r"source table:\s*\n\s*\|",
    r"source map:\s*\n\s*\S",
    r"donor prose excerpt:\s*\n\s*\S",
]

FORBIDDEN_C_REGISTRY_FIELD_VALUES = {
    "canon",
    "canon-current",
    "sourcebook",
    "sourcebook-current",
    "runtime",
    "runtime-current",
    "live-play",
    "live_play",
    "training",
    "training-current",
    "registry-current",
    "final-mechanics",
    "final_mechanics",
}


def _content() -> str:
    return read_utf8(SM14_PATH)


def _assert_terms(content: str, terms: list[str], label: str) -> None:
    lower = content.lower()
    for term in terms:
        assert term.lower() in lower, f"Missing {label}: {term}"


def test_sm14_file_exists_and_nonempty():
    assert SM14_PATH.exists(), f"SM14 file not found at {SM14_PATH}"
    assert _content().strip(), "SM14 file is empty"


def test_sm14_required_section_headings_present_and_in_order():
    content = _content()
    last_index = -1
    for index, section in enumerate(REQUIRED_SECTIONS, start=1):
        heading = f"## {index}. {section}"
        current_index = content.find(heading)
        assert current_index != -1, f"Missing section heading: {heading}"
        assert current_index > last_index, f"Section out of order: {heading}"
        last_index = current_index


def test_sm14_names_required_upstream_and_repository_controls():
    _assert_terms(_content(), REQUIRED_NAMES, "required upstream/current-state reference")


def test_sm14_status_and_non_execution_boundaries_are_explicit():
    content = _content()
    _assert_terms(
        content,
        [
            "SM14 is a metadata-only real packet shell validation and reviewer-gate control file only.",
            "SM14 does not create a completed real authorization packet.",
            "SM14 does not make an actual authorization decision.",
            "SM14 does not authorize actual execution.",
            "SM14 does not approve execution.",
            "SM14 does not run conversion.",
            "SM14 does not create actual converted donor content or pilot outputs.",
        ],
        "status/non-execution boundary",
    )


def test_sm14_refuses_donor_content_implementation_artifacts_and_authority_creep():
    _assert_terms(_content(), REFUSAL_TERMS, "refusal/authority-creep term")


def test_sm14_distinguishes_related_phases_and_future_artifacts():
    _assert_terms(_content(), BOUNDARY_DISTINCTIONS, "phase distinction")


def test_sm14_packet_shell_and_metadata_slot_validation_coverage():
    content = _content()
    _assert_terms(content, PACKET_SHELL_SLOTS, "packet shell slot")
    _assert_terms(content, METADATA_CATEGORIES, "metadata category")
    _assert_terms(
        content,
        [
            "These are validation expectations only.",
            "must not create final schema fields",
            "Metadata is not donor content, not legal/IP clearance, not source clearance, not conversion evidence, not canon evidence, and not execution approval.",
            "external-reference readiness is not source clearance",
            "no-donor sentinel checks are not legal/IP clearance",
        ],
        "metadata-only validation boundary",
    )


def test_sm14_preserves_c_family_scope_and_deferrals():
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
            "3-5 packet candidates",
            "must not expand beyond authorization",
        ],
        "C-family pressure or deferral",
    )


def test_sm14_reviewer_labels_are_document_local_not_registry_values():
    content = _content()
    _assert_terms(content, REVIEWER_LABELS, "reviewer decision label")
    _assert_terms(
        content,
        [
            "document-local reviewer decision labels only",
            "They are not registry values",
            "must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`",
        ],
        "document-local label boundary",
    )


def test_sm14_includes_shell_validation_workflow():
    _assert_terms(_content(), WORKFLOW_STEPS, "shell validation workflow step")


def test_sm14_states_what_validation_may_and_may_not_prove():
    content = _content()
    _assert_terms(content, MAY_PROVE, "may-prove statement")
    _assert_terms(content, MAY_NOT_PROVE, "may-not-prove statement")


def test_sm14_non_readiness_boundaries_owner_fallbacks_risk_and_next_pr():
    content = _content()
    _assert_terms(
        content,
        [
            "Large-scale conversion non-readiness boundary",
            "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
            "Owner map and lawful fallbacks",
            "Risk register",
            "SM15 actual pilot authorization decision record controls",
            "SM15 metadata-only shell validation repair and reviewer calibration controls",
            "must not recommend jumping directly to actual donor conversion, broad conversion, final mechanics, runtime schemas, canon consolidation, sourcebook prose, live-play adapter behavior, training corpus creation, or real donor-content ingestion",
        ],
        "non-readiness/owner/risk/next-PR term",
    )


def test_sm14_contains_no_obvious_implementation_or_donor_artifacts():
    content = _content()
    for pattern in IMPLEMENTATION_ARTIFACT_PATTERNS:
        assert not re.search(pattern, content, flags=re.IGNORECASE | re.MULTILINE), (
            f"SM14 appears to contain an implementation or donor artifact matching {pattern!r}"
        )


def test_sm09_dry_template_fixture_remains_markdown_direct_placeholder_and_no_donor_safe():
    assert DRY_TEMPLATE_PATH.exists(), f"Missing dry template fixture: {DRY_TEMPLATE_PATH}"
    assert DRY_TEMPLATE_PATH.parent == SCAFFOLD_DIR, "Dry template must remain a direct child of scaffold directory"
    assert DRY_TEMPLATE_PATH.suffix == ".md", "Dry template must remain Markdown"

    content = read_utf8(DRY_TEMPLATE_PATH)
    _assert_terms(
        content,
        [
            "Placeholder, synthetic, non-donor scaffold only.",
            "no real donor content",
            "no protected source expression",
            "no copied mechanical blocks",
            "no copied tables",
            "no copied maps",
            "no copied setting prose",
            "no protected source names",
            "not actual authorization",
            "not execution approval",
        ],
        "dry template no-donor posture",
    )

    for sentinel in DONOR_PROPER_NOUN_SENTINELS:
        assert sentinel.lower() not in content.lower(), f"Dry template contains donor proper noun sentinel: {sentinel}"

    forbidden_markers = [
        "donor excerpt:",
        "statblock:",
        "source table:",
        "source map:",
        "converted output:",
        "training example:",
        "sourcebook-ready example:",
        "actual pilot output:",
    ]
    for marker in forbidden_markers:
        assert marker.lower() not in content.lower(), f"Dry template contains forbidden donor marker: {marker}"


def _registry_c_record_blocks() -> dict[str, str]:
    text = read_utf8(REGISTRY_PATH)
    blocks: dict[str, str] = {}
    matches = list(re.finditer(r"(?m)^- file_id: (C\d{2})\s*$", text))
    for index, match in enumerate(matches):
        file_id = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks[file_id] = text[match.start() : end]
    return blocks


def _registry_field_value(block: str, field: str) -> str | None:
    match = re.search(rf"(?m)^\s{{2}}{field}:\s*([^\n#]+)", block)
    if not match:
        return None
    return match.group(1).strip().strip("'\"").lower()


def test_c00_c14_registry_records_not_promoted_to_forbidden_runtime_canon_training_states():
    blocks = _registry_c_record_blocks()
    expected_ids = {"C00"} | {f"C{i:02d}" for i in range(1, 15)}
    assert expected_ids <= set(blocks), f"Missing C registry records: {sorted(expected_ids - set(blocks))}"

    for file_id in sorted(expected_ids):
        for field in ("status", "authority_level", "test_status", "review_status"):
            value = _registry_field_value(blocks[file_id], field)
            assert value not in FORBIDDEN_C_REGISTRY_FIELD_VALUES, (
                f"{file_id} registry {field} is forbidden for SM14 non-promotion posture: {value}"
            )
            for label in REVIEWER_LABELS:
                assert value != label, f"{file_id} registry {field} improperly uses SM14 document-local label {label}"
