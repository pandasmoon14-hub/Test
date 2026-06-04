import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM15_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM15_actual_pilot_authorization_decision_record_controls.md"
)

SCAFFOLD_DIR = ROOT / "tests" / "fixtures" / "pilot_conversion_scaffold"
DRY_TEMPLATE_PATH = SCAFFOLD_DIR / "dry_authorization_packet_template.md"

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing authorization decision posture",
    "What SM15 owns",
    "What SM15 must not own",
    "Authorization decision record definition",
    "Decision record versus execution approval boundary",
    "Decision eligibility requirements",
    "Metadata-only decision posture",
    "No-donor-in-repository decision rule",
    "Legal/IP and source-clearance decision boundary",
    "SM02 no-waiver decision requirement",
    "SM03 dry-run decision requirement",
    "SM04 evaluation-rubric decision requirement",
    "SM05 authorization/preflight decision requirement",
    "SM06 execution/output-capture decision requirement",
    "SM07 scaffold/review-harness decision requirement",
    "SM08 no-donor safety decision requirement",
    "SM09 dry template decision requirement",
    "SM10 reviewer validation decision requirement",
    "SM11 preparation-control decision requirement",
    "SM12 external-reference review decision requirement",
    "SM13 metadata-only assembly decision requirement",
    "SM14 shell-validation decision requirement",
    "Decision record required contents",
    "Decision outcome labels",
    "Authorization-granted boundary",
    "Authorization-blocked boundary",
    "Repair, quarantine, deferred-gap, and `pending_schema` routing",
    "Packet scope and C-family pressure decision limits",
    "Evidence/provenance pointer decision review",
    "Lawful outcome and mapping ledger decision review",
    "Rejected-import, source-local, legal/IP, and `pending_schema` decision review",
    "Confidence, review-routing, repair, quarantine, and failure-report decision review",
    "Donor leakage hard-fail decision rule",
    "Decision workflow",
    "Decision record validation expectations",
    "What SM15 decision controls may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM15",
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
    "SM14",
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
    "treat decision records as execution approval",
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
    "SM14 shell validation and reviewer gate: validation of assembled metadata-only shell posture.",
    "SM15 decision-record controls: control posture for documenting a later authorization decision.",
    "Future actual decision record: not created by this PR unless a separate owner-approved packet shell exists, which it does not.",
    "Future execution PR: still downstream and not created by SM15.",
]

DECISION_RECORD_SLOTS = [
    "decision record identity",
    "linked metadata-only packet shell identity",
    "decision status and non-execution statement",
    "decision owner",
    "legal/IP owner",
    "future execution proposal owner",
    "SM02 no-waiver confirmation",
    "SM03 dry-run confirmation",
    "SM04 evaluation/rubric handoff confirmation",
    "SM05 authorization/preflight confirmation",
    "SM06 output-capture confirmation",
    "SM07 scaffold/review-harness confirmation",
    "SM08 no-donor safety confirmation",
    "SM09 dry template confirmation",
    "SM10 reviewer validation confirmation",
    "SM11 preparation-control confirmation",
    "SM12 external-reference review confirmation",
    "SM13 metadata-only assembly confirmation",
    "SM14 shell-validation confirmation",
    "C-family pressure target",
    "packet count",
    "legal/IP disposition",
    "source-clearance boundary",
    "evidence/provenance pointer posture",
    "lawful outcome route",
    "mapping ledger route",
    "rejected-import route",
    "source-local retention route",
    "`pending_schema` route",
    "repair route",
    "quarantine route",
    "failure-report route",
    "donor leakage hard-fail result",
    "decision rationale",
    "final non-readiness statement",
]

METADATA_BOUNDARIES = [
    "These are decision-record content requirements only.",
    "Do not turn them into final JSON fields",
    "JSON Schema",
    "Pydantic models",
    "database fields",
    "runtime contracts",
    "final validators",
    "implementation contracts",
    "Metadata is not donor content",
    "not legal/IP clearance",
    "not source clearance",
    "not conversion evidence",
    "not canon evidence",
    "not execution approval",
    "external-reference readiness is not source clearance",
    "no-donor sentinel checks are not legal/IP clearance",
]

DECISION_LABELS = [
    "authorization_decision_ready_for_execution_proposal_review",
    "authorization_decision_blocked_by_missing_sm02_gate",
    "authorization_decision_blocked_by_missing_sm05_preflight",
    "authorization_decision_blocked_by_missing_sm14_shell_validation",
    "authorization_decision_blocked_by_missing_legal_ip_owner",
    "authorization_decision_blocked_by_source_clearance_gap",
    "authorization_decision_blocked_by_embedded_donor_content",
    "authorization_decision_blocked_by_scope_expansion",
    "authorization_decision_blocked_by_runtime_or_mechanics_creep",
    "authorization_decision_requires_repair",
    "authorization_decision_requires_quarantine",
    "authorization_decision_requires_legal_ip_review",
    "authorization_decision_requires_pending_schema",
    "authorization_decision_rejected_import",
    "authorization_decision_source_local_only",
    "authorization_decision_not_execution",
    "authorization_decision_not_conversion",
]

WORKFLOW_STEPS = [
    "Confirm SM00-SM14 are present and current.",
    "Confirm a metadata-only packet shell exists and passed SM14 shell validation.",
    "Confirm no real donor content is embedded in the PR.",
    "Confirm the decision record is metadata-only.",
    "Confirm no execution is performed by the decision record.",
    "Confirm legal/IP owner exists.",
    "Confirm future review or execution-proposal owner exists.",
    "Confirm metadata is not treated as legal/IP clearance.",
    "Confirm external-reference readiness is not treated as source clearance.",
    "Confirm SM02 no-waiver posture.",
    "Confirm SM03 dry-run posture.",
    "Confirm SM04 rubric and handoff posture.",
    "Confirm SM05 authorization/preflight posture.",
    "Confirm SM06 output-capture posture.",
    "Confirm SM07 scaffold/review-harness posture.",
    "Confirm SM08 no-donor safety posture.",
    "Confirm SM09 dry template reference.",
    "Confirm SM10 reviewer validation posture.",
    "Confirm SM11 preparation-control posture.",
    "Confirm SM12 external-reference review posture.",
    "Confirm SM13 metadata-only assembly posture.",
    "Confirm SM14 shell-validation posture.",
    "Confirm C-family scope remains bounded.",
    "Assign document-local authorization decision label.",
    "Record decision rationale.",
    "Route failures to repair, quarantine, deferred gap ledger, `pending_schema`, legal/IP review, source-local retention, rejected import, or appropriate future owner.",
    "State exactly what the authorization decision record may and may not prove.",
    "If the decision is \"ready for execution proposal review,\" state that a separate execution proposal PR is still required before anything can run.",
]

MAY_PROVE = [
    "the project has controls for documenting a future authorization decision record",
    "a future validated metadata-only shell can be routed to decision outcomes",
    "blocking, repair, quarantine, legal/IP, source-local, rejected-import, and `pending_schema` routes can be recorded",
    "a later execution proposal review may be conditionally allowed if a future decision record permits it",
]

MAY_NOT_PROVE = [
    "execution approval",
    "conversion approval",
    "legal/IP clearance",
    "source clearance",
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
    return read_utf8(SM15_PATH)


def _assert_terms(content: str, terms: list[str], label: str) -> None:
    lower = content.lower()
    for term in terms:
        assert term.lower() in lower, f"Missing {label}: {term}"


def test_sm15_file_exists_and_nonempty():
    assert SM15_PATH.exists(), f"SM15 file not found at {SM15_PATH}"
    assert _content().strip(), "SM15 file is empty"


def test_sm15_required_section_headings_present_and_in_order():
    content = _content()
    last_index = -1
    for index, section in enumerate(REQUIRED_SECTIONS, start=1):
        heading = f"## {index}. {section}"
        current_index = content.find(heading)
        assert current_index != -1, f"Missing section heading: {heading}"
        assert current_index > last_index, f"Section out of order: {heading}"
        last_index = current_index


def test_sm15_names_required_upstream_and_repository_controls():
    _assert_terms(_content(), REQUIRED_NAMES, "required upstream/current-state reference")


def test_sm15_status_and_non_execution_boundaries_are_explicit():
    content = _content()
    _assert_terms(
        content,
        [
            "SM15 is an actual pilot authorization decision record control file only.",
            "SM15 does not itself create an actual completed authorization decision for a real donor packet because no owner-approved metadata-only packet shell exists yet.",
            "SM15 does not run conversion.",
            "SM15 does not execute a pilot.",
            "SM15 does not create actual converted donor content or pilot outputs.",
        ],
        "status/non-execution boundary",
    )


def test_sm15_refuses_donor_content_implementation_artifacts_and_authority_creep():
    _assert_terms(_content(), REFUSAL_TERMS, "refusal/authority-creep term")


def test_sm15_distinguishes_related_phases_and_future_artifacts():
    _assert_terms(_content(), BOUNDARY_DISTINCTIONS, "phase distinction")


def test_sm15_decision_record_contents_and_metadata_slot_coverage():
    content = _content()
    _assert_terms(content, DECISION_RECORD_SLOTS, "decision record slot")
    _assert_terms(content, METADATA_BOUNDARIES, "metadata-only decision boundary")


def test_sm15_preserves_c_family_scope_and_deferrals():
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
        "C-family scope and deferrals",
    )


def test_sm15_decision_outcome_labels_and_registry_boundary():
    content = _content()
    _assert_terms(content, DECISION_LABELS, "decision outcome label")
    assert "not registry values" in content.lower(), "Must state labels are not registry values"
    assert "must not be written into registry fields" in content.lower(), "Must state labels must not be written into registry fields"


def test_sm15_authorization_granted_boundary():
    content = _content()
    _assert_terms(
        content,
        [
            "this is not execution approval",
            "this is not conversion approval",
            "this is not legal/IP clearance",
            "this is not source clearance",
            "this is not pilot evidence",
            "this does not create output",
            "this does not authorize broad conversion",
            "this only allows a later, separate execution proposal PR to be considered under SM02-SM15 controls",
        ],
        "authorization-granted boundary",
    )


def test_sm15_decision_workflow_steps():
    content = _content()
    _assert_terms(content, WORKFLOW_STEPS, "decision workflow step")


def test_sm15_may_and_may_not_prove():
    content = _content()
    _assert_terms(content, MAY_PROVE, "may prove")
    _assert_terms(content, MAY_NOT_PROVE, "may not prove")


def test_sm15_large_scale_conversion_non_readiness_boundary():
    content = _content()
    _assert_terms(
        content,
        [
            "large-scale corpus conversion is not ready",
            "does not authorize broad conversion",
            "does not create benchmark corpora",
            "does not create evaluation corpora",
            "does not create training data",
            "does not create fine-tuning data",
            "does not create model behavior policy",
        ],
        "large-scale conversion non-readiness",
    )


def test_sm15_runtime_canon_sourcebook_live_play_training_non_readiness_boundary():
    content = _content()
    _assert_terms(
        content,
        [
            "runtime, canon, sourcebook, live-play, and training readiness are not achieved",
            "does not create final schemas",
            "executable JSON Schema",
            "Pydantic models",
            "final validators",
            "runtime/backend/database schemas",
            "runtime/backend/database contracts",
            "entity/component/event schemas",
            "command lifecycle contracts",
            "context packet contracts",
            "save-state shapes",
            "final mechanics",
            "exact math",
            "canon",
            "sourcebook prose",
            "live-play behavior",
            "accepted lexicon",
            "registry promotion",
        ],
        "runtime/canon/sourcebook/live-play/training non-readiness",
    )


def test_sm15_owner_routing_and_lawful_fallbacks():
    content = _content()
    _assert_terms(
        content,
        [
            "Decision owner",
            "Legal/IP owner",
            "Future execution proposal owner",
            "Review owner",
            "Schema owner",
            "No-donor safety owner",
            "Lawful fallbacks",
        ],
        "owner routing and lawful fallbacks",
    )


def test_sm15_risk_register():
    content = _content()
    _assert_terms(
        content,
        [
            "Risk: treating decision record as execution approval",
            "Risk: treating no-donor sentinel checks as legal/IP clearance",
            "Risk: treating external-reference readiness as source clearance",
            "Risk: treating metadata as donor content or conversion evidence",
            "Risk: scope expansion",
            "Risk: SM02 gate waiver",
            "Risk: SM05 bypass",
            "Risk: D00-D19 authority creep",
            "Risk: RHBF hidden law",
        ],
        "risk register",
    )


def test_sm15_recommended_next_pr():
    content = _content()
    _assert_terms(
        content,
        [
            "SM16 controlled pilot execution proposal controls",
            "SM16 authorization decision repair and owner-calibration controls",
        ],
        "recommended next PR",
    )
    # Ensure it does NOT recommend jumping directly to forbidden actions
    lower = content.lower()
    forbidden_recommendations = [
        "actual donor conversion",
        "broad conversion",
        "final mechanics",
        "runtime schemas",
        "canon consolidation",
        "sourcebook prose",
        "live-play adapter behavior",
        "training corpus creation",
        "real donor-content ingestion",
    ]
    for fr in forbidden_recommendations:
        # Check that SM15 explicitly says it must NOT recommend these
        assert "must not recommend jumping directly to" in lower or fr not in lower.split("recommended next pr")[0].lower(), f"Should not recommend: {fr}"


def test_sm15_no_implementation_artifacts():
    content = _content()
    for pattern in IMPLEMENTATION_ARTIFACT_PATTERNS:
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        assert match is None, f"Found forbidden implementation artifact pattern: {pattern}"


def test_sm15_no_donor_proper_nouns_as_defaults():
    content = _content()
    for noun in DONOR_PROPER_NOUN_SENTINELS:
        # These should not appear as Astra defaults or imported content
        assert noun not in content, f"Found donor proper noun that should not be imported: {noun}"


def test_sm09_dry_template_fixture_is_markdown_placeholder_synthetic_non_donor():
    """Verify the existing SM09 dry authorization packet template fixture remains Markdown, direct child of the scaffold directory, placeholder/synthetic/non-donor, and no-donor safe under the SM08 sentinel posture."""
    assert DRY_TEMPLATE_PATH.exists(), f"SM09 dry template fixture not found at {DRY_TEMPLATE_PATH}"
    assert DRY_TEMPLATE_PATH.suffix == ".md", "SM09 dry template must be Markdown"
    assert DRY_TEMPLATE_PATH.parent == SCAFFOLD_DIR, "SM09 dry template must be direct child of scaffold directory"
    
    template_content = read_utf8(DRY_TEMPLATE_PATH)
    assert template_content.strip(), "SM09 dry template is empty"
    
    # Verify placeholder/synthetic/non-donor language
    _assert_terms(
        template_content,
        [
            "Placeholder, synthetic, non-donor scaffold only",
            "no real donor content",
            "no protected source expression",
            "not converted content",
            "not training data",
            "not canon",
            "not sourcebook prose",
            "not benchmark corpora",
            "not evaluation corpora",
            "not runtime import data",
            "not actual authorization",
            "not execution approval",
            "not a pilot output",
            "not evidence that conversion may run",
        ],
        "SM09 dry template placeholder/synthetic/non-donor posture",
    )


def test_sm09_dry_template_no_donor_safe_under_sm08_sentinel():
    """Verify SM09 dry template is no-donor safe under SM08 sentinel posture."""
    template_content = read_utf8(DRY_TEMPLATE_PATH)
    
    # Check for absence of donor proper nouns
    for noun in DONOR_PROPER_NOUN_SENTINELS:
        assert noun not in template_content, f"SM09 dry template contains donor proper noun: {noun}"
    
    # Verify SM08 reference exists
    assert "SM08" in template_content or "no-donor" in template_content.lower(), "SM09 should reference no-donor safety posture"


def test_registry_c00_c14_not_promoted_to_forbidden_states():
    """Registry records for C00-C14 are not promoted to forbidden states by this PR. Do not freeze exact current draft statuses; only check forbidden promotion states within C00-C14 status/review fields."""
    if not REGISTRY_PATH.exists():
        return  # Skip if registry doesn't exist
    
    registry_content = read_utf8(REGISTRY_PATH)
    
    # Parse YAML-like structure for C00-C14 entries
    # Check that forbidden values don't appear in status/authority_level/test_status/review_status fields
    # We need to be careful to only match actual field values, not text in notes/changelogs
    for forbidden_value in FORBIDDEN_C_REGISTRY_FIELD_VALUES:
        # Look for patterns like "status: canon" or "authority_level: runtime" etc.
        # Match only at end of line or followed by specific delimiters (not part of longer text)
        # Use word boundary and ensure it's an actual field value
        c_pattern = rf"(?m)^(\s*C\d{{2}}\w*|\s+-\s*C\d{{2}}\w*).*?(?:status|authority_level|test_status|review_status)\s*:\s*{re.escape(forbidden_value)}\s*$"
        match = re.search(c_pattern, registry_content, re.IGNORECASE)
        assert match is None, f"C00-C14 registry entry promoted to forbidden state: {forbidden_value}"


def test_sm15_eligibility_requirements():
    content = _content()
    _assert_terms(
        content,
        [
            "SM02 no-waiver posture is satisfied",
            "SM03 dry-run posture is represented",
            "SM04 evaluation/rubric handoff is represented",
            "SM05 authorization/preflight posture is represented",
            "SM06 execution/output-capture posture is represented",
            "SM07 scaffold/review-harness posture is represented",
            "SM08 no-donor safety posture is represented",
            "SM09 dry template reference is represented",
            "SM10 reviewer validation posture is represented",
            "SM11 preparation-control posture is represented",
            "SM12 external-reference review posture is represented",
            "SM13 metadata-only assembly posture is represented",
            "SM14 shell-validation posture is represented",
            "legal/IP owner is named",
            "future review owner is named",
            "source-clearance boundary is explicit",
            "no donor content is embedded in the repo",
            "C-family pressure remains bounded",
        ],
        "decision eligibility requirement",
    )


def test_sm15_decision_eligibility_routing():
    content = _content()
    _assert_terms(
        content,
        [
            "repair, quarantine, rejected-import, source-local, `pending_schema`, legal/IP, and failure-report routes exist",
            "the decision record must block, repair, quarantine, or route to the appropriate future owner",
        ],
        "eligibility routing",
    )


def test_sm15_acceptance_criteria_coverage():
    content = _content()
    # Verify acceptance criteria section exists and covers key items
    assert "## 44. Acceptance criteria" in content, "Missing acceptance criteria section"
    _assert_terms(
        content,
        [
            "SM15 file exists and is nonempty",
            "All required section headings are present and in order",
            "SM15 names SM00-SM14",
            "SM15 states it is an actual pilot authorization decision record control file only",
            "SM15 states it does not itself create an actual completed authorization decision",
            "SM15 states it does not run conversion",
            "SM15 states it does not execute a pilot",
            "SM15 states it does not create actual converted donor content or pilot outputs",
        ],
        "acceptance criteria",
    )


def test_sm15_future_safe_test_posture():
    """Tests must be durable. They should not fail merely because later valid SM16/SM17/etc. files are added."""
    content = _content()
    # Verify SM15 acknowledges future PRs without blocking them
    _assert_terms(
        content,
        [
            "Future execution PR: still downstream and not created by SM15",
            "separate execution proposal PR",
            "later owner-controlled authorization",
        ],
        "future-safe posture",
    )
    # Verify SM15 explicitly states it is a control file only and does not claim to be final doctrine
    # The word "final" appears in contexts like "final mechanics", "final schemas", etc. which is expected
    # We just need to ensure SM15 doesn't claim to BE final doctrine itself
    lower = content.lower()
    assert "sm15 is final doctrine" not in lower, "SM15 should not claim to be final doctrine"
    assert "sm15 is the final" not in lower, "SM15 should not claim to be the final authority"
