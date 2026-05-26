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

    assert "does **not** adopt donor rulesets" in a00
    assert "lexicon governance and reserved terms policy (K01)" in a00


def test_decision_log_contains_2026_05_26_prea01_entry():
    decisions = _read_text(DECISIONS_PATH)

    assert "## 2026-05-26 decision log - pre-A01 control layer patch" in decisions
    assert "Decision ID: PREA01-001" in decisions
    assert "A01 remains `A01_cosmology_and_dimensional_architecture.md`" in decisions
    assert "K01 remains `K01_lexicon_governance_and_reserved_terms.md`" in decisions
