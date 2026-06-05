from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "doctrine" / "reviews" / "runtime_boundary_generator_ownership_audit_wave1.md"
PROTOCOL_RELATIVE_PATH = "docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

ALLOWED_LABELS = {
    "doctrine_only",
    "schema_ready",
    "runtime_ready",
    "generator_ready",
    "validator_ready",
    "context_packet_ready",
    "narration_only",
    "blocked_pending_schema",
    "blocked_pending_math",
    "blocked_pending_runtime",
}

REQUIRED_FIELDS = [
    "subsystem_id",
    "source_area",
    "source_files",
    "classification",
    "doctrine_owner",
    "backend_truth_owner",
    "missing_backend_pieces",
    "required_schemas",
    "required_math_mechanics",
    "required_generators_templates",
    "required_command_ir",
    "required_state_event_fields",
    "required_context_packet_projection",
    "required_narration_contract",
    "required_tests",
    "llm_overreach_risk",
    "blocked_by",
    "recommended_next_action",
    "notes",
]

RISK_LEVELS = {"none", "low", "medium", "high", "critical"}


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def audit_record_blocks(text: str) -> list[str]:
    return re.findall(r"```yaml\n(.*?)\n```", text, flags=re.DOTALL)


def field_names(block: str) -> set[str]:
    return set(re.findall(r"^([a-z_]+):", block, flags=re.MULTILINE))


def classification_labels(block: str) -> list[str]:
    match = re.search(
        r"^classification:\n(?P<body>(?:  - [a-z_]+\n)+)",
        block,
        flags=re.MULTILINE,
    )
    assert match, f"Missing classification list in block:\n{block}"
    return re.findall(r"  - ([a-z_]+)", match.group("body"))


def test_wave1_audit_report_exists_and_references_audit_001_protocol() -> None:
    text = read(REPORT_PATH)

    assert "Wave 1 audit report only" in text
    assert "This is Wave 1 only" in text
    assert "AUDIT-001" in text
    assert PROTOCOL_RELATIVE_PATH in text


def test_wave1_audit_report_uses_canonical_schema_for_8_to_12_records() -> None:
    text = read(REPORT_PATH)
    blocks = audit_record_blocks(text)

    assert 8 <= len(blocks) <= 12

    for block in blocks:
        missing = set(REQUIRED_FIELDS) - field_names(block)
        assert not missing, f"Audit record missing required fields: {sorted(missing)}\n{block}"
        risk_match = re.search(r"^llm_overreach_risk: ([a-z]+)$", block, flags=re.MULTILINE)
        assert risk_match, f"Missing llm_overreach_risk in block:\n{block}"
        assert risk_match.group(1) in RISK_LEVELS


def test_wave1_audit_report_uses_only_allowed_classification_labels() -> None:
    text = read(REPORT_PATH)

    for block in audit_record_blocks(text):
        labels = classification_labels(block)
        assert labels, f"Expected at least one classification label in block:\n{block}"
        unexpected = set(labels) - ALLOWED_LABELS
        assert not unexpected, f"Unexpected classification labels: {sorted(unexpected)}"


def test_wave1_audit_report_states_no_unauthorized_implementation_or_authorization() -> None:
    text = read(REPORT_PATH)

    for phrase in [
        "no doctrine rewrite",
        "no runtime implementation",
        "no generator implementation",
        "no validator implementation",
        "no canon promotion",
        "no live-play/training authorization",
    ]:
        assert phrase in text


def test_wave1_registry_tracking_exists() -> None:
    registry = read(REGISTRY_PATH)

    assert "AUDIT-WAVE1-001" in registry
    assert "runtime_boundary_generator_ownership_audit_wave1.md" in registry
    assert "Wave 1 audit report only" in registry
    assert "no doctrine rewrite" in registry
    assert "runtime implementation" in registry
    assert "generator implementation" in registry
    assert "validator implementation" in registry
    assert "canon promotion" in registry
    assert "live-play authorization" in registry
    assert "training authorization" in registry
