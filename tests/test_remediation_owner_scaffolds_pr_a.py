from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RT001_PATH = ROOT / "docs" / "doctrine" / "control" / "RT001_command_lifecycle_action_legality_owner_scaffold.md"
RT011_PATH = ROOT / "docs" / "doctrine" / "control" / "RT011_validation_readiness_tooling_owner_scaffold.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_pr_a_owner_scaffold_files_exist() -> None:
    assert RT001_PATH.exists()
    assert RT011_PATH.exists()


def test_scaffolds_reference_remediation_priority_ledger() -> None:
    for path in [RT001_PATH, RT011_PATH]:
        text = read(path)
        assert "REMEDIATION-PRIORITY-LEDGER-001" in text
        assert "owner scaffold" in text


def test_rt001_references_track_and_key_source_pressures() -> None:
    text = read(RT001_PATH)

    for phrase in [
        "RT-001",
        "RT-001-command-lifecycle-action-legality",
        "B02",
        "A10",
        "D02",
        "C03",
        "C10",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
    ]:
        assert phrase in text


def test_rt011_references_track_and_key_source_pressures() -> None:
    text = read(RT011_PATH)

    for phrase in [
        "RT-011",
        "RT-011-validation-readiness-tooling",
        "AUDIT-001",
        "SM00",
        "SM01",
        "SM02",
    ]:
        assert phrase in text


def test_scaffolds_include_explicit_non_implementation_guardrails() -> None:
    for path in [RT001_PATH, RT011_PATH]:
        text = read(path)
        for phrase in [
            "planning/control only",
            "Explicit non-implementation statement",
            "implements no",
            "no doctrine rewrite",
            "runtime implementation",
            "schema implementation",
            "validator implementation",
            "generator implementation",
            "persistence writer",
            "context-packet compiler",
            "canon promotion",
            "live-play",
            "training data",
            "donor-content audit",
        ]:
            assert phrase in text


def test_rt001_prohibits_llm_runtime_authority() -> None:
    text = read(RT001_PATH)

    for phrase in [
        "validate action legality",
        "spend or refund costs",
        "roll dice or select random results",
        "decide hidden modifiers",
        "commit state deltas",
        "invent consequences",
        "write files",
        "alter canon",
        "treat narration as event commit",
    ]:
        assert phrase in text


def test_rt011_distinguishes_prose_readiness_from_executable_validation() -> None:
    text = read(RT011_PATH)

    for phrase in [
        "Prose readiness versus executable validation",
        "A prose file is not executable validation",
        "Readiness prose is not a runtime gate",
        "Model assertions are not reviewer decisions",
        "not executable validators",
        "not final schemas",
        "not approval automation",
        "not runtime gates",
        "not pilot conversion authorization",
    ]:
        assert phrase in text


def test_rt011_prohibits_live_play_training_and_canon_authorization() -> None:
    text = read(RT011_PATH)

    for phrase in [
        "authorizing live play",
        "authorizing training data",
        "promoting canon",
        "approving pilot conversion outputs",
        "replacing reviewer decisions with model assertions",
    ]:
        assert phrase in text


def test_registry_tracks_both_owner_scaffolds() -> None:
    registry = read(REGISTRY_PATH)

    for phrase in [
        "REMEDIATION-RT001-COMMAND-LIFECYCLE-OWNER-SCAFFOLD-001",
        "REMEDIATION-RT011-VALIDATION-READINESS-OWNER-SCAFFOLD-001",
        "RT001_command_lifecycle_action_legality_owner_scaffold.md",
        "RT011_validation_readiness_tooling_owner_scaffold.md",
        "owner scaffold only",
        "no doctrine rewrite",
        "no runtime implementation",
        "no schema implementation",
        "no command IR implementation",
        "no validator implementation",
        "no generator implementation",
        "no persistence writer implementation",
        "no context-packet compiler implementation",
        "no canon promotion",
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in registry


def test_scaffolds_do_not_claim_to_implement_runtime_artifacts() -> None:
    forbidden_claims = [
        "implements command ir",
        "implements schemas",
        "implements runtime",
        "implements validators",
        "implements generators",
        "implements persistence writers",
        "implements context-packet compilers",
        "implementation complete",
        "runtime-ready",
        "validator-ready",
        "generator-ready",
    ]

    for path in [RT001_PATH, RT011_PATH]:
        text = read(path).lower()
        for phrase in forbidden_claims:
            assert phrase not in text
