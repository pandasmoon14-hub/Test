from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
A00_PATH = REPO_ROOT / "docs" / "doctrine" / "control" / "A00_mechanical_posture_and_ruleset_non_adoption.md"
PREA01_PATH = REPO_ROOT / "docs" / "doctrine" / "control" / "pre_a01_control_layer_patch_v0_1.md"
DECISIONS_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"


def _read_text(path: Path) -> str:
    assert path.exists(), f"Missing required file: {path}"
    return path.read_text(encoding="utf-8")


def test_control_layer_docs_exist_and_reference_invariants():
    a00 = _read_text(A00_PATH)
    prea01 = _read_text(PREA01_PATH)

    assert "A01_cosmology_and_dimensional_architecture.md" in prea01
    assert "K01_lexicon_governance_and_reserved_terms.md" in prea01

    required_sections = [
        "## 1. Purpose and status",
        "## 2. What this file owns",
        "## 3. What this file must not own",
        "## 4. Required definitions",
        "## 5. Core doctrine rules",
        "## 6. Conversion mapping rules",
        "## 7. Source-local handling",
        "## 8. Donor pressure absorbed",
        "## 9. Hard refusals / rejected imports",
        "## 10. Escalation triggers",
        "## 11. Dependencies",
        "## 12. Handoff to downstream layers",
        "## 13. Test cases / pressure examples",
        "## 14. Versioning and review protocol",
    ]
    for section in required_sections:
        assert section in a00

    control_spine_terms = [
        "lexicon status gate",
        "term status lifecycle",
        "source-local record",
        "rejected import record",
        "reserved term family",
        "tag namespace separation",
        "state mutation gate",
        "state-change digest",
        "actor state ledger",
        "hidden-information boundary",
    ]
    lower_prea01 = prea01.lower()
    for term in control_spine_terms:
        assert term in lower_prea01

    assert "not authoritative state" in lower_prea01
    assert "source-local" in lower_prea01
    assert "rejected import" in lower_prea01
    assert "tag namespace" in lower_prea01


def test_decision_log_contains_2026_05_26_prea01_entry():
    decisions = _read_text(DECISIONS_PATH)

    assert "## 2026-05-26 decision log - pre-A01 control layer patch" in decisions
    assert "Decision ID: PREA01-001" in decisions
    assert "A01 remains `A01_cosmology_and_dimensional_architecture.md`" in decisions
    assert "K01 remains `K01_lexicon_governance_and_reserved_terms.md`" in decisions
    assert "Stage 5 lexicon-control entries route to K01/pre-A01 ledgers/work orders" in decisions
    assert "state-change digest is a report from committed backend events" in decisions.lower()
    assert "Registry entries are tracking/work-order records" in decisions
