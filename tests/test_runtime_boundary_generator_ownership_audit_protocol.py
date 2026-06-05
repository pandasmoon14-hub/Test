from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "docs" / "doctrine" / "control" / "runtime_boundary_generator_ownership_audit_protocol.md"
ROADMAP_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_roadmap_v0_1.md"
DECISIONS_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

ALLOWED_LABELS = [
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
]

REQUIRED_OUTPUT_FIELDS = [
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


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_runtime_boundary_generator_ownership_protocol_exists_and_is_preparation_only() -> None:
    text = read(PROTOCOL_PATH)

    assert "Status: audit-preparation protocol only" in text
    assert "This protocol does not perform the audit" in text
    assert "This preparation file does not classify any subsystem" in text
    assert "backend code without relying on the LLM to improvise missing mechanics, state, validation, memory, persistence, generators, or consequences" in text


def test_runtime_boundary_generator_ownership_protocol_scope_uses_existing_repo_conventions() -> None:
    text = read(PROTOCOL_PATH)

    for required in [
        "docs/doctrine/setting/",
        "docs/doctrine/advancement/",
        "docs/doctrine/world/",
        "docs/doctrine/operations/batch_b/",
        "docs/doctrine/schema/",
        "docs/doctrine/native_design/d_series/source_packs/",
        "docs/doctrine/schema_math_mechanics/",
        "docs/doctrine/control/",
        "docs/decisions/current_decisions_log.md",
        "docs/operations/current_decisions_log_v0_1.md",
    ]:
        assert required in text

    for scope_marker in [
        "Batch A doctrine",
        "Batch B operational doctrine",
        "Batch C schema-family files",
        "D00-D19 native-design source-pack material",
        "schema/math/mechanics workstream files",
        "roadmap/control files",
        "runtime/training files",
    ]:
        assert scope_marker in text

    assert "Do not audit donor PDFs, donor books, or donor content directly." in text
    assert "do not invent paths or file contents" in text


def test_runtime_boundary_generator_ownership_protocol_labels_match_roadmap() -> None:
    protocol = read(PROTOCOL_PATH)
    roadmap = read(ROADMAP_PATH)

    for label in ALLOWED_LABELS:
        assert label in protocol
        assert label in roadmap

    assert "Audit preparation protocol: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`" in roadmap


def test_runtime_boundary_generator_ownership_protocol_output_schema_and_review_process_are_complete() -> None:
    text = read(PROTOCOL_PATH)

    for field in REQUIRED_OUTPUT_FIELDS:
        assert field in text

    for step in [
        "Inventory pass",
        "Boundary extraction pass",
        "Subsystem slicing pass",
        "Classification pass",
        "LLM overreach pass",
        "Generator ownership pass",
        "Validator/context/persistence pass",
        "Escalation pass",
        "Evidence pass",
        "No-implementation pass",
    ]:
        assert step in text


def test_runtime_boundary_generator_ownership_protocol_is_tracked_without_claiming_audit_execution() -> None:
    decisions = read(DECISIONS_PATH)
    registry = read(REGISTRY_PATH)

    assert "CTRL-RUNTIME-GENERATOR-AUDIT-PROTOCOL-001" in decisions
    assert "file_id: AUDIT-001" in registry
    assert "protocol cannot perform the audit it prepares" in registry
    assert "does not classify subsystems" in decisions
