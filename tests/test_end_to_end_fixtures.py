import pytest
pytest.importorskip("fitz")
import json, os, subprocess, sys
from pathlib import Path


def test_fixture_e2e_and_validate(tmp_path: Path):
    repo = Path(__file__).resolve().parents[1]
    fixture_dir = repo / "tests" / "fixtures"
    subprocess.check_call([sys.executable, str(fixture_dir / "generate_fixture_pdfs.py")])
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    input_dir.mkdir(); output_dir.mkdir()
    for pdf in fixture_dir.glob("*.pdf"):
        (input_dir / pdf.name).write_bytes(pdf.read_bytes())
    env = os.environ.copy()
    env.update({"INPUT_DIR": str(input_dir), "OUTPUT_DIR": str(output_dir), "FORCE_LANE": "A", "OCR_MODE": "skip"})
    subprocess.check_call([sys.executable, str(repo / "orchestrator.py"), "--strict_page_truth"], env=env)
    book = output_dir / "multi_page_mixed_10_pages"
    assert (book / "strict_audit.json").exists()
    assert (book / "astra_handoff_manifest.json").exists()
    lines = (book / "multi_page_mixed_10_pages.page_truth.jsonl").read_text().strip().splitlines()
    assert len(lines) == 10
    md = (book / "multi_page_mixed_10_pages.md").read_text()
    assert md.count("<!-- PAGE:") == 10
    subprocess.check_call([sys.executable, str(repo / "validate_outputs.py"), "--output-dir", str(output_dir), "--strict"])
    blank = json.loads((output_dir / "blank_page" / "strict_audit.json").read_text())
    assert blank["strict_audit_status"] == "pass"
