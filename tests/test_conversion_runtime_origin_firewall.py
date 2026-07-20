from __future__ import annotations

import ast
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
DOCTRINE_PATH = (
    REPO_ROOT
    / "docs"
    / "doctrine"
    / "control"
    / "conversion_runtime_origin_firewall_doctrine.md"
)
RUNTIME_ROOT = REPO_ROOT / "src" / "astra_runtime"

FORBIDDEN_RUNTIME_IMPORT_ROOTS = frozenset(
    {
        "acceptance_corpus",
        "audit_runtime",
        "conversion",
        "conversion_intake",
        "extractor",
        "orchestrator",
        "pilot_benchmark",
        "quality_harness",
        "regression_suite",
        "surgeon",
        "table_fixer",
        "validate_outputs",
    }
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(_read(path), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def test_readme_declares_conversion_runtime_firewall() -> None:
    text = _read(README_PATH)
    assert "## Extraction/conversion–runtime firewall" in text
    assert "Extraction and conversion end before runtime begins." in text
    assert "Runtime is origin-blind." in text
    assert "Offline provenance is retained but isolated." in text
    assert "conversion_runtime_origin_firewall_doctrine.md" in text


def test_firewall_doctrine_requires_one_way_identity_breaking_promotion() -> None:
    text = _read(DOCTRINE_PATH)
    assert "The flow is one-way." in text
    assert "Identity-breaking promotion boundary" in text
    assert "Runtime-origin blindness" in text
    assert "Offline lineage ledger" in text
    assert "new Astra-native identity" in text
    assert "must not contain the reverse lookup key" in text


def test_firewall_doctrine_preserves_offline_governance_evidence() -> None:
    text = _read(DOCTRINE_PATH)
    assert "does not mean destroying governance evidence" in text
    assert "rights review" in text
    assert "does not" in text
    assert "erase or destroy governance evidence" in text
    assert "permit laundering unapproved material by deleting attribution" in text


def test_runtime_package_does_not_directly_import_extraction_or_conversion_tools() -> None:
    violations: list[str] = []
    for path in sorted(RUNTIME_ROOT.rglob("*.py")):
        for module in sorted(_imported_modules(path)):
            root = module.split(".", 1)[0]
            if root in FORBIDDEN_RUNTIME_IMPORT_ROOTS:
                violations.append(f"{path.relative_to(REPO_ROOT)} imports {module}")

    assert not violations, "Runtime origin-firewall import violations:\n" + "\n".join(
        violations
    )
