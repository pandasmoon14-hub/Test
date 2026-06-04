import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM08_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM08_controlled_pilot_packet_placeholder_validation_and_no_donor_safety_harness.md"
)

SCAFFOLD_DIR = ROOT / "tests" / "fixtures" / "pilot_conversion_scaffold"

REQUIRED_SECTIONS = [
    "Purpose and status",
    "Upstream controls and authority boundary",
    "Existing placeholder scaffold posture",
    "What SM08 owns",
    "What SM08 must not own",
    "Placeholder validation harness definition",
    "No-donor safety harness definition",
    "Scaffold fixture validation scope",
    "Required placeholder labeling checks",
    "Required no-donor safety checks",
    "Required capture-slot checks",
    "SM05 authorization reference checks",
    "SM06 output-capture posture checks",
    "SM04 review-handoff checks",
    "Scope-expansion blocking checks",
    "Runtime/canon/sourcebook/live-play/training/final-mechanics leakage checks",
    "Implementation-artifact checks",
    "Donor-marker sentinel posture",
    "Harness pass/block labels",
    "Harness limitations",
    "What SM08 validation may and may not prove",
    "Large-scale conversion non-readiness boundary",
    "Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "Owner map and lawful fallbacks",
    "Risk register",
    "Recommended next PR after SM08",
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
    "placeholder_validation_passed",
    "placeholder_validation_blocked_by_missing_fixture",
    "placeholder_validation_blocked_by_missing_label",
    "placeholder_validation_blocked_by_missing_capture_slot",
    "no_donor_safety_passed",
    "no_donor_safety_blocked_by_donor_marker",
    "no_donor_safety_blocked_by_converted_content_marker",
    "no_donor_safety_blocked_by_runtime_or_mechanics_creep",
    "no_donor_safety_blocked_by_training_or_canon_creep",
    "harness_requires_repair",
    "harness_requires_quarantine",
    "harness_not_execution_approval",
]

DONOR_ARTIFACT_MARKERS = [
    "converted output:",
    "donor excerpt:",
    "statblock:",
    "source table:",
    "source map:",
    "training example:",
    "sourcebook-ready example:",
    "actual pilot output:",
]

DONOR_PROPER_NOUN_SENTINELS = [
    # Small sentinel list of known donor proper-noun markers
    # This is not exhaustive and does not replace legal/IP review
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
    r"class\s+\w+\s*\(\s*BaseModel\s*\)",  # Pydantic class definitions
    r'"type":\s*"object"',  # JSON Schema object definitions
    r"CREATE\s+TABLE",  # Database table definitions
    r"contract\s+\w+\s*is",  # Solidity-style contracts
    r"interface\s+\w+",  # Interface definitions
]


def test_sm08_file_exists_and_nonempty():
    """Assert SM08 file exists and is nonempty."""
    assert SM08_PATH.exists(), f"SM08 file not found at {SM08_PATH}"
    content = read_utf8(SM08_PATH)
    assert len(content.strip()) > 0, "SM08 file is empty"


def test_sm08_required_sections_present():
    """Assert all required numbered section headings are present in order."""
    content = read_utf8(SM08_PATH)
    last_index = -1
    for index, section in enumerate(REQUIRED_SECTIONS, start=1):
        heading = f"## {index}. {section}"
        current_index = content.find(heading)
        assert current_index != -1, f"Missing required section heading: {heading}"
        assert current_index > last_index, f"Section heading out of order: {heading}"
        last_index = current_index


def test_sm08_names_upstream_controls():
    """Assert SM08 names required upstream controls."""
    content = read_utf8(SM08_PATH)
    
    # Required named references
    required_names = [
        "SM00",
        "SM01",
        "SM02",
        "SM03",
        "SM04",
        "SM05",
        "SM06",
        "SM07",
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
    
    for name in required_names:
        assert name in content, f"SM08 must name {name}"
    
    c_family_tokens = [f"C{index:02d}" for index in range(15)]
    assert "C00-C14" in content, "SM08 must name the collective C00-C14 range"
    assert all(token in content for token in c_family_tokens), (
        "SM08 must name each C-family identifier from C00 through C14"
    )


def test_sm08_states_placeholder_validation_only():
    """Assert SM08 states it is a controlled pilot packet placeholder validation and no-donor safety harness file only."""
    content = read_utf8(SM08_PATH)
    assert "controlled pilot packet placeholder validation and no-donor safety harness" in content.lower() or \
           "placeholder validation and no-donor safety harness" in content.lower(), \
           "SM08 must state it is a controlled pilot packet placeholder validation and no-donor safety harness file only"


def test_sm08_states_validates_scaffold_posture_only():
    """Assert SM08 states it validates placeholder scaffold posture only."""
    content = read_utf8(SM08_PATH)
    assert "validates placeholder scaffold posture" in content.lower() or \
           "placeholder scaffold posture" in content.lower(), \
           "SM08 must state it validates placeholder scaffold posture only"


def test_sm08_states_does_not_run_conversion():
    """Assert SM08 states it does not run conversion and does not create actual converted donor content or pilot outputs."""
    content = read_utf8(SM08_PATH)
    assert "does not run conversion" in content.lower(), \
           "SM08 must state it does not run conversion"
    assert "does not create actual converted donor content" in content.lower() or \
           "not create actual converted donor content" in content.lower(), \
           "SM08 must state it does not create actual converted donor content"
    assert "pilot outputs" in content.lower(), \
           "SM08 must reference pilot outputs"


def test_sm08_refuses_donor_content():
    """Assert SM08 refuses real donor excerpts, donor statblocks, donor tables, donor maps, donor setting prose, etc."""
    content = read_utf8(SM08_PATH)
    
    refusal_terms = [
        "donor excerpt",
        "donor statblock",
        "donor table",
        "donor map",
        "donor setting prose",
        "donor proper noun",
        "benchmark corpora",
        "evaluation corpora",
        "training data",
        "fine-tuning data",
        "model behavior",
        "final schema",
        "JSON Schema",
        "Pydantic",
        "final validator",
        "runtime",
        "backend",
        "database",
        "contract",
        "final mechanics",
        "canon",
        "sourcebook",
        "live-play",
        "registry promotion",
        "C00",
        "C14",
        "C15",
        "D00",
        "D19",
        "RHBF",
        "SM02",
        "SM05",
        "execution approval",
        "legal",
        "IP",
    ]
    
    for term in refusal_terms:
        assert term in content, f"SM08 must refuse {term}"


def test_sm08_defines_placeholder_validation_harness():
    """Assert SM08 defines placeholder validation harness."""
    content = read_utf8(SM08_PATH)
    assert "placeholder validation harness" in content.lower(), \
           "SM08 must define placeholder validation harness"


def test_sm08_defines_no_donor_safety_harness():
    """Assert SM08 defines no-donor safety harness."""
    content = read_utf8(SM08_PATH)
    assert "no-donor safety harness" in content.lower() or \
           "no donor safety harness" in content.lower(), \
           "SM08 must define no-donor safety harness"


def test_sm08_validates_scaffold_directory():
    """Assert SM08 validates the expected SM07 fixture directory."""
    content = read_utf8(SM08_PATH)
    assert "tests/fixtures/pilot_conversion_scaffold" in content, \
           "SM08 must validate the tests/fixtures/pilot_conversion_scaffold directory"


def test_scaffold_files_exist():
    """Assert expected scaffold fixture files exist and no extra scaffold files are added."""
    expected_files = {
        SCAFFOLD_DIR / "README.md",
        SCAFFOLD_DIR / "placeholder_packet_manifest.md",
        SCAFFOLD_DIR / "placeholder_review_harness.md",
    }

    assert SCAFFOLD_DIR.exists(), f"Scaffold fixture directory not found: {SCAFFOLD_DIR}"
    actual_md_files = set(SCAFFOLD_DIR.glob("*.md"))
    assert actual_md_files == expected_files, (
        "Scaffold fixture directory must contain exactly the expected markdown files"
    )
    for filepath in expected_files:
        assert filepath.exists(), f"Scaffold fixture file not found: {filepath}"


def test_scaffold_files_labeled_placeholder_synthetic_non_donor():
    """Assert every scaffold fixture is clearly labeled placeholder/synthetic/non-donor."""
    md_files = list(SCAFFOLD_DIR.glob("*.md"))
    
    for filepath in md_files:
        content = read_utf8(filepath).lower()
        assert "placeholder" in content, f"{filepath} must contain 'placeholder' label"
        assert "synthetic" in content, f"{filepath} must contain 'synthetic' label"
        assert "non-donor" in content or "non donor" in content, \
            f"{filepath} must contain 'non-donor' label"


def test_scaffold_files_no_donor_artifact_markers():
    """Assert every scaffold fixture contains no obvious donor-content artifact markers."""
    md_files = list(SCAFFOLD_DIR.glob("*.md"))
    
    for filepath in md_files:
        content = read_utf8(filepath)
        for marker in DONOR_ARTIFACT_MARKERS:
            assert marker.lower() not in content.lower(), \
                f"{filepath} contains forbidden donor artifact marker: {marker}"


def test_scaffold_files_no_donor_proper_noun_sentinels():
    """Assert every scaffold fixture contains no known donor-proper-noun sentinel markers."""
    md_files = list(SCAFFOLD_DIR.glob("*.md"))
    
    for filepath in md_files:
        content = read_utf8(filepath)
        for sentinel in DONOR_PROPER_NOUN_SENTINELS:
            assert sentinel not in content, \
                f"{filepath} contains forbidden donor proper-noun sentinel: {sentinel}"


def test_scaffold_contains_sm05_authorization_reference_terms():
    """Assert the scaffold collectively contains required SM05 authorization reference placeholder terms."""
    # Read all scaffold files collectively
    all_content = ""
    for filepath in SCAFFOLD_DIR.glob("*.md"):
        all_content += read_utf8(filepath)
    
    for term in SM05_AUTHORIZATION_REFERENCE_TERMS:
        assert term in all_content or term.lower() in all_content.lower(), \
            f"Scaffold must contain SM05 authorization reference term: {term}"


def test_scaffold_contains_sm06_output_capture_terms():
    """Assert the scaffold collectively contains required SM06 output-capture placeholder terms."""
    # Read all scaffold files collectively
    all_content = ""
    for filepath in SCAFFOLD_DIR.glob("*.md"):
        all_content += read_utf8(filepath)
    
    for term in SM06_OUTPUT_CAPTURE_TERMS:
        assert term in all_content or term.lower() in all_content.lower(), \
            f"Scaffold must contain SM06 output-capture term: {term}"


def test_sm08_includes_harness_labels():
    """Assert SM08 includes document-local harness labels."""
    content = read_utf8(SM08_PATH)
    
    for label in SCAFFOLD_LABELS:
        assert label in content, f"SM08 must include harness label: {label}"


def test_sm08_states_labels_are_not_registry_values():
    """Assert SM08 states harness labels are not registry values."""
    content = read_utf8(SM08_PATH)
    assert "not registry values" in content.lower() or \
           "not registry value" in content.lower() or \
           "local labels only" in content.lower(), \
           "SM08 must state harness labels are not registry values"


def test_sm08_states_harness_limitations():
    """Assert SM08 states harness limitations."""
    content = read_utf8(SM08_PATH)
    
    limitation_terms = [
        "not legal review",
        "not a complete copyright detector",
        "not proof",
        "does not authorize",
        "does not validate actual conversion",
    ]
    
    found_count = 0
    for term in limitation_terms:
        if term in content.lower():
            found_count += 1
    
    assert found_count >= 3, "SM08 must state multiple harness limitations"


def test_sm08_states_what_may_and_may_not_prove():
    """Assert SM08 states what validation may and may not prove."""
    content = read_utf8(SM08_PATH)
    assert "may prove" in content.lower() and "may not prove" in content.lower(), \
           "SM08 must state what validation may and may not prove"


def test_sm08_states_large_scale_conversion_non_readiness():
    """Assert SM08 states large-scale conversion non-readiness boundary."""
    content = read_utf8(SM08_PATH)
    assert "large-scale conversion" in content.lower() or \
           "large scale conversion" in content.lower(), \
           "SM08 must state large-scale conversion non-readiness boundary"


def test_sm08_states_runtime_canon_sourcebook_live_play_training_non_readiness():
    """Assert SM08 states runtime/canon/sourcebook/live-play/training non-readiness boundary."""
    content = read_utf8(SM08_PATH)
    
    non_readiness_terms = ["runtime", "canon", "sourcebook", "live-play", "training"]
    found_count = 0
    for term in non_readiness_terms:
        if term in content.lower():
            found_count += 1
    
    assert found_count >= 4, "SM08 must state runtime/canon/sourcebook/live-play/training non-readiness boundary"


def test_sm08_includes_owner_routing():
    """Assert SM08 includes owner routing and lawful fallbacks."""
    content = read_utf8(SM08_PATH)
    assert "owner" in content.lower() and ("routing" in content.lower() or "fallback" in content.lower()), \
           "SM08 must include owner routing and lawful fallbacks"


def test_sm08_includes_risk_register():
    """Assert SM08 includes a risk register."""
    content = read_utf8(SM08_PATH)
    assert "risk register" in content.lower() or "risk" in content.lower(), \
           "SM08 must include a risk register"


def test_sm08_recommends_sm09():
    """Assert SM08 recommends SM09 controlled pilot execution dry authorization packet template or SM09 placeholder safety repair/scaffold hardening controls."""
    content = read_utf8(SM08_PATH)
    assert "SM09" in content, "SM08 must recommend SM09 as next PR"
    assert "controlled pilot execution dry authorization packet template" in content.lower() or \
           "placeholder safety repair" in content.lower() or \
           "scaffold hardening" in content.lower(), \
           "SM08 must recommend appropriate SM09 follow-up"


def test_sm08_does_not_recommend_jumping_to_donor_conversion():
    """Assert SM08 does not recommend jumping directly to actual donor conversion, broad conversion, final mechanics, etc."""
    content = read_utf8(SM08_PATH)
    
    # Check that SM08 explicitly states it must NOT recommend these
    assert "must not recommend" in content.lower() or "cannot recommend" in content.lower(), \
           "SM08 must state what it must not recommend"
    
    forbidden_recommendations = [
        "actual donor conversion",
        "broad conversion",
        "final mechanics",
        "runtime schemas",
        "canon consolidation",
        "sourcebook prose",
        "live-play",
        "training corpus",
    ]
    
    # The document should mention these as things NOT to do
    found_forbidden_context = False
    for rec in forbidden_recommendations:
        if rec in content.lower():
            found_forbidden_context = True
            break
    
    # It's okay if these terms appear in the context of "must not"
    assert found_forbidden_context or "jumping directly" in content.lower(), \
           "SM08 must address forbidden recommendations"


def test_sm08_no_implementation_artifacts():
    """Assert SM08 does not contain obvious implementation artifacts."""
    content = read_utf8(SM08_PATH)
    
    for pattern in IMPLEMENTATION_ARTIFACT_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        assert len(matches) == 0, f"SM08 contains implementation artifact matching pattern: {pattern}"
    
    # Also check for specific forbidden content types
    forbidden_content = [
        "class.*BaseModel",
        '"type".*"object"',
        "CREATE TABLE",
    ]
    
    for forbidden in forbidden_content:
        matches = re.findall(forbidden, content, re.IGNORECASE)
        assert len(matches) == 0, f"SM08 contains forbidden implementation content: {forbidden}"


def test_sm08_no_converted_donor_content():
    """Assert SM08 does not contain converted donor content, donor statblocks, donor tables, donor maps, or donor prose excerpts."""
    content = read_utf8(SM08_PATH)
    
    # These should be mentioned as things SM08 does NOT do, not as actual content
    # Check that the document doesn't contain actual donor content patterns
    donor_content_patterns = [
        r"donor excerpt:\s*\n\s*[A-Z]",  # Actual donor excerpt following marker
        r"statblock:\s*\n\s*[A-Z]",  # Actual statblock following marker
        r"source table:\s*\n\s*\|",  # Actual table following marker
        r"source map:\s*\n\s*[A-Z]",  # Actual map following marker
    ]
    
    for pattern in donor_content_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        assert len(matches) == 0, f"SM08 contains potential donor content matching pattern: {pattern}"


def test_registry_records_not_promoted_to_forbidden_states():
    """Assert registry records for C00-C14 are not promoted to forbidden states by this PR."""
    assert REGISTRY_PATH.exists(), f"Registry not found: {REGISTRY_PATH}"
    registry_content = read_utf8(REGISTRY_PATH)
    registry_lower = registry_content.lower()

    for index in range(15):
        token = f"C{index:02d}"
        assert token in registry_content, f"Registry must keep tracking record for {token}"

    forbidden_states = [
        "canon-promoted",
        "runtime-ready",
        "sourcebook-ready",
        "live-play-ready",
        "training-ready",
        "final-mechanics-ready",
    ]

    for state in forbidden_states:
        assert state not in registry_lower, (
            f"Registry contains forbidden C00-C14 promotion state: {state}"
        )


def test_sm08_future_safe_test_posture():
    """Assert tests are durable and future-safe."""
    # This test verifies that SM08 doesn't block legitimate future registry promotion
    content = read_utf8(SM08_PATH)
    
    # SM08 should allow future legitimate registry promotion through proper owner-controlled PRs
    assert "proper owner" in content.lower() or "owner-controlled" in content.lower() or \
           "owner routing" in content.lower(), \
           "SM08 should reference proper owner-controlled processes for future changes"
