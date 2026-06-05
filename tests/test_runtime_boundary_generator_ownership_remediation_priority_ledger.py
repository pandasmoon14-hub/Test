from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_boundary_generator_ownership_remediation_priority_ledger.md"
)

REQUIRED_INPUTS = {
    "AUDIT-001",
    "AUDIT-WAVE1-001",
    "AUDIT-WAVE2-001",
}

REQUIRED_TRACK_FIELDS = {
    "track_id",
    "priority",
    "title",
    "risk_level",
    "source_audit_records",
    "affected_source_files",
    "problem_summary",
    "why_backend_owned",
    "required_owner_files_or_workstreams",
    "required_outputs",
    "dependencies",
    "blocked_by",
    "recommended_first_pr",
    "must_not_do_in_first_pr",
    "acceptance_tests_needed",
    "notes",
}

REQUIRED_THEMES = [
    "Command lifecycle / action legality / cost commitment",
    "Resource, backlash, corruption, strain, and consequence math",
    "Combat, damage, injury, hazard exposure, and recovery",
    "Ability/effect/cost/cooldown/action binding",
    "Mission, reward, clue, hidden-truth, and consequence routing",
    "Social, faction, relationship, actor knowledge, and institutional state",
    "Generated-content recurrence/provenance",
    "Runtime RNG/table/oracle ownership",
    "Scene/activity orchestration and hidden-information/context-packet boundaries",
    "Validation/readiness tooling versus prose-only governance",
    "D-series/native-design material promotion boundaries",
]


def read_ledger() -> str:
    assert LEDGER_PATH.exists(), f"Missing expected ledger: {LEDGER_PATH}"
    return LEDGER_PATH.read_text(encoding="utf-8")


def yaml_blocks(text: str) -> list[str]:
    return re.findall(r"```yaml\n(.*?)\n```", text, flags=re.DOTALL)


def field_names(block: str) -> set[str]:
    return set(re.findall(r"^([a-z_]+):", block, flags=re.MULTILINE))


def test_remediation_priority_ledger_exists_and_is_planning_only() -> None:
    text = read_ledger()

    assert "remediation-priority planning ledger only" in text
    assert "This ledger intentionally does not perform Wave 3" in text
    for phrase in [
        "does not implement remediation",
        "rewrite doctrine",
        "create runtime code",
        "create schemas",
        "create command IR",
        "create generators",
        "create validators",
        "create persistence writers",
        "create context-packet compilers",
        "authorize live play",
        "create training data",
        "audit donor content",
        "promote canon",
    ]:
        assert phrase in text


def test_remediation_priority_ledger_lists_controlling_inputs() -> None:
    text = read_ledger()

    for input_id in REQUIRED_INPUTS:
        assert input_id in text
    assert "docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md" in text
    assert "docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md" in text
    assert "docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md" in text


def test_remediation_priority_ledger_includes_required_risk_themes() -> None:
    text = read_ledger()

    for theme in REQUIRED_THEMES:
        assert theme in text


def test_remediation_tracks_use_canonical_shape_and_ranked_priorities() -> None:
    text = read_ledger()
    blocks = yaml_blocks(text)

    assert len(blocks) >= 10
    assert "priority: P0" in text
    assert "priority: P1" in text
    assert "priority: P2" in text

    track_ids: list[str] = []
    for block in blocks:
        missing = REQUIRED_TRACK_FIELDS - field_names(block)
        assert not missing, f"Track record missing fields {sorted(missing)}:\n{block}"
        track_match = re.search(r"^track_id: (.+)$", block, flags=re.MULTILINE)
        assert track_match, f"Missing track_id:\n{block}"
        track_ids.append(track_match.group(1))
        priority_match = re.search(r"^priority: (P[0-3])$", block, flags=re.MULTILINE)
        assert priority_match, f"Missing valid priority:\n{block}"
        risk_match = re.search(r"^risk_level: (critical|high|medium|low)$", block, flags=re.MULTILINE)
        assert risk_match, f"Missing valid risk_level:\n{block}"

    assert len(track_ids) == len(set(track_ids))


def test_remediation_sequence_preserves_non_implementation_scope() -> None:
    text = read_ledger()

    assert "Recommended next safe PR sequence" in text
    assert "Do not define final IR, schemas, validators, math, runtime, or generators" in text
    assert "Do not create generators, generated records, retrieval indexes, canon promotion decisions, or D-series adoption" in text
    assert "Do not implement inventory, item effects, vehicle movement, cargo, or damage" in text
