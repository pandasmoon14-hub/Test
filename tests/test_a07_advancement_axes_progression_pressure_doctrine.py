from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
A07_PATH = REPO_ROOT / "docs" / "doctrine" / "advancement" / "A07_advancement_axes_and_progression_pressure.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def test_a07_required_sections_present():
    text = _read(A07_PATH)
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


def test_a07_required_axis_terms_present():
    text = _read(A07_PATH).lower()
    for phrase in [
        "body axis",
        "soul axis",
        "mind axis",
        "path axis",
        "technique axis",
        "social/institutional axis",
        "asset/relic/platform axis",
        "companion axis",
        "factional axis",
        "cross-axis dependency",
        "cross-axis contradiction",
        "progression pressure",
        "quarantined axis construct",
        "escalated axis contradiction",
    ]:
        assert phrase in text


def test_a07_forbidden_specificity_and_runtime_definitions_absent():
    text = _read(A07_PATH).lower()
    for phrase in [
        "specific skill lists",
        "faction ranks",
        "point-buy costs",
        "karma costs",
        "license ranks",
        "class features",
        "techniques, spells, or powers",
        "stat bonuses",
        "xp tables or level tables",
        "resources, costs, recharge, or backlash",
        "actor stat blocks",
        "combat math",
        "action economy",
        "progression math",
        "runtime progression state",
        "runtime event commits",
        "runtime actor state",
        "hidden-information behavior",
    ]:
        assert phrase in text


def test_registry_a07_posture_and_blocking_updated_for_a06_prereq():
    records = _registry_records()

    a06 = records["A06"]
    a07 = records["A07"]
    k01 = records["K01"]

    assert a06["status"] in {"draft", "review", "pressure-tested", "current"}

    assert a07["status"] == "draft"
    assert a07["status"] != "current"
    assert a07["authority_level"] == "doctrine-draft"
    assert a07["test_status"] == "designed"
    assert a07["review_status"] == "not_reviewed"
    assert a07["proposed_path"] == "docs/doctrine/advancement/A07_advancement_axes_and_progression_pressure.md"
    assert a07["dependencies"] == ["A05", "A06"]
    assert a07["blocked_by"] == []

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a07["filename"] != k01["filename"]

    for idx in range(8, 16):
        rec = records[f"A{idx:02d}"]
        assert rec["status"] == "todo"
        assert rec["authority_level"] == "doctrine-todo"
        assert rec["test_status"] == "not_started"
