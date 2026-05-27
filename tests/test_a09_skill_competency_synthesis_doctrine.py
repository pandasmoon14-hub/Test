from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
A09_PATH = REPO_ROOT / "docs" / "doctrine" / "advancement" / "A09_skill_competency_and_synthesis_doctrine.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _file_record(file_id: str) -> str:
    text = _read(REGISTRY_PATH)
    marker = f"- file_id: {file_id}\n"
    start = text.index(marker)
    next_idx = text.find("\n- file_id:", start + 1)
    return text[start:] if next_idx == -1 else text[start:next_idx]


def test_a09_file_exists():
    assert A09_PATH.exists()


def test_a09_required_sections_present():
    text = _read(A09_PATH)
    for heading in [
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
    ]:
        assert heading in text


def test_a09_boundary_language_present():
    lowered = _read(A09_PATH).lower()
    for phrase in [
        "must not define",
        "canon skill list",
        "specific skill names",
        "proficiency bonus math",
        "point-buy costs",
        "training time formulas",
        "crafting recipes",
        "faction reputation systems",
        "technique mastery",
        "resource costs or resource pools",
        "action economy",
        "damage formulas",
        "conditions",
        "actor stat blocks",
        "xp tables or level tables",
        "runtime skill/progression state",
        "a09 cannot absorb k01 ownership",
        "source-local",
        "quarantined",
        "escalated",
    ]:
        assert phrase in lowered


def test_a09_dependencies_and_non_redefinition_posture_present():
    text = _read(A09_PATH)
    lowered = text.lower()

    assert "A07_advancement_axes_and_progression_pressure.md" in text
    assert "A08_path_domain_and_technique_mastery_doctrine.md" in text

    for phrase in [
        "a07 advancement-axis taxonomy",
        "a08 technique mastery",
        "a08 activation/targeting grammar",
        "resource systems",
        "damage families",
        "condition/status rules",
        "actor stats",
        "runtime event commits",
        "runtime actor state",
        "hidden-information behavior",
    ]:
        assert phrase in lowered


def test_registry_a09_posture_and_downstream_not_promoted():
    a09 = _file_record("A09")
    k01 = _file_record("K01")

    assert "status: draft" in a09
    assert "status: current" not in a09
    assert "authority_level: doctrine-draft" in a09
    assert "test_status: designed" in a09
    assert "review_status: not_reviewed" in a09
    assert "proposed_path: docs/doctrine/advancement/A09_skill_competency_and_synthesis_doctrine.md" in a09
    assert "dependencies:" in a09
    assert "- A07" in a09
    assert "- A08" in a09
    assert "blocked_by: []" in a09

    assert "proposed_path: docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md" in k01
    assert "filename: A09_skill_competency_and_synthesis_doctrine.md" in a09
    assert "filename: K01_lexicon_governance_and_reserved_terms.md" in k01

    for idx in range(10, 16):
        rec = _file_record(f"A{idx:02d}")
        assert "status: todo" in rec
        assert "authority_level: doctrine-todo" in rec
        assert "test_status: not_started" in rec
