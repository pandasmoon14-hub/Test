import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/handoff/plan_full_corpus_dry_run.py")


def _run(corpus: Path, out: Path, strict=True, extra=None):
    cmd = [sys.executable, str(SCRIPT), "--corpus-dir", str(corpus), "--output-dir", str(out)]
    if strict:
        cmd.append("--strict")
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p, json.loads(p.stdout)


def _mk_min_corpus(tmp_path: Path) -> Path:
    c = tmp_path / "corpus"
    c.mkdir()
    (c / "core_rulebook.pdf").write_bytes(b"abc")
    return c


def test_minimal_valid_synthetic_corpus(tmp_path: Path):
    c = _mk_min_corpus(tmp_path)
    p, r = _run(c, tmp_path / "out")
    assert p.returncode == 0
    assert r["valid"] is True


def test_recursive_discovery(tmp_path: Path):
    c = tmp_path / "corpus"
    (c / "a" / "b").mkdir(parents=True)
    (c / "a" / "b" / "book.pdf").write_bytes(b"x")
    p, r = _run(c, tmp_path / "out")
    assert p.returncode == 0
    assert r["files_discovered"] == 1


def test_duplicate_filename_detection(tmp_path: Path):
    c = tmp_path / "corpus"
    (c / "x").mkdir(parents=True)
    (c / "y").mkdir(parents=True)
    (c / "x" / "same.pdf").write_bytes(b"a")
    (c / "y" / "same.pdf").write_bytes(b"b")
    _, r = _run(c, tmp_path / "out")
    assert any("duplicate_file_name" in w for w in r["warnings"])


def test_duplicate_content_hash_detection(tmp_path: Path):
    c = tmp_path / "corpus"
    c.mkdir()
    (c / "a.pdf").write_bytes(b"same")
    (c / "b.pdf").write_bytes(b"same")
    _, r = _run(c, tmp_path / "out")
    assert any("duplicate_content_hash" in w for w in r["warnings"])


def test_zero_byte_file_issue(tmp_path: Path):
    c = tmp_path / "corpus"
    c.mkdir()
    (c / "z.pdf").write_bytes(b"")
    _, r = _run(c, tmp_path / "out")
    assert any("zero_byte_file" in w for w in r["warnings"])


def test_unsupported_extension_handling(tmp_path: Path):
    c = tmp_path / "corpus"
    c.mkdir()
    (c / "a.exe").write_bytes(b"x")
    p, r = _run(c, tmp_path / "out")
    assert p.returncode != 0
    assert r["unsupported_files"] == 1


def test_donor_family_fallback_to_unclassified(tmp_path: Path):
    c = tmp_path / "corpus"
    c.mkdir()
    (c / "weirdname.pdf").write_bytes(b"x")
    _, r = _run(c, tmp_path / "out")
    assert r["donor_family_estimate_counts"].get("unclassified_or_mixed_donor_family", 0) >= 1


def test_donor_family_template_config_loading(tmp_path: Path):
    c = _mk_min_corpus(tmp_path)
    _, r = _run(c, tmp_path / "out", extra=["--donor-family-templates", "configs/handoff/donor_family_templates.yaml"])
    assert r["valid"] is True


def test_repair_queue_config_loading(tmp_path: Path):
    c = _mk_min_corpus(tmp_path)
    _, r = _run(c, tmp_path / "out", extra=["--repair-queues", "configs/handoff/extraction_repair_queues.yaml"])
    assert r["valid"] is True


def test_output_files_are_written(tmp_path: Path):
    c = _mk_min_corpus(tmp_path)
    _, r = _run(c, tmp_path / "out")
    for p in r["output_files"]:
        assert Path(p).exists()


def test_strict_mode_fails_for_missing_corpus_dir(tmp_path: Path):
    p, r = _run(tmp_path / "missing", tmp_path / "out")
    assert p.returncode != 0
    assert "missing_corpus_dir" in r["errors"]


def test_max_files_limits_discovery_deterministically(tmp_path: Path):
    c = tmp_path / "corpus"
    c.mkdir()
    for i in range(5):
        (c / f"{i}.pdf").write_bytes(b"x")
    _, r = _run(c, tmp_path / "out", extra=["--max-files", "2"])
    assert r["files_discovered"] == 2
