"""Contract tests for shared retained-evidence mechanics (no game-state authority)."""
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest


MODULE = Path(__file__).resolve().parents[1] / "scripts" / "_myravant_evidence_runner.py"
SPEC = importlib.util.spec_from_file_location("_myravant_evidence_runner", MODULE)
assert SPEC is not None and SPEC.loader is not None
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def test_installed_session_preserves_public_argv_stdin_and_load_boundary(tmp_path, monkeypatch):
    calls = []

    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    save = tmp_path / "campaign.json"
    trace = tmp_path / "stage.jsonl"
    sha = "a" * 40
    for load in (False, True):
        result = runner.run_installed_session(
            "myravant-play", ("--locality", "generated-worksite"),
            save, trace, sha, ("go north", "wait"),
            load=load, timeout=100,
        )
        assert result.returncode == 0
        argv, kwargs = calls[-1]
        assert argv == [
            "myravant-play", "--locality", "generated-worksite",
            "--checkpoint", str(save), "--trace", str(trace),
            "--repository-sha", sha,
        ] + (["--load", str(save)] if load else [])
        assert kwargs == {
            "input": "go north\nwait\nsave\nexit\n",
            "text": True, "capture_output": True, "timeout": 100,
        }
    assert len(calls) == 2


def test_repository_sha_requires_exact_identity_and_uses_checkout_fallback(monkeypatch):
    sha = "0123456789abcdef" * 2 + "01234567"
    assert len(sha) == 40
    assert runner.resolve_repository_sha(sha) == sha
    for invalid in ("short", "a" * 39, "A" * 40, "g" * 40):
        with pytest.raises(ValueError):
            runner.resolve_repository_sha(invalid)

    def fake_check_output(cmd, **kwargs):
        assert cmd == ["git", "rev-parse", "HEAD"]
        assert kwargs == {"text": True, "timeout": 15}
        return sha + "\n"

    monkeypatch.setattr(runner.subprocess, "check_output", fake_check_output)
    assert runner.resolve_repository_sha(None) == sha


def test_repeated_digest_equality_requires_exact_two_runs_per_case():
    records = [
        {"case": "one", "digest": "x"},
        {"case": "one", "digest": "x"},
        {"case": "two", "digest": "y"},
        {"case": "two", "digest": "y"},
    ]
    runner.assert_repeat_digest_equality(
        records, ("one", "two"), case_field="case", digest_field="digest"
    )
    with pytest.raises(AssertionError):
        runner.assert_repeat_digest_equality(
            records[:-1], ("one", "two"), case_field="case", digest_field="digest"
        )
    with pytest.raises(AssertionError):
        runner.assert_repeat_digest_equality(
            records[:-1] + [{"case": "two", "digest": "z"}],
            ("one", "two"), case_field="case", digest_field="digest",
        )
    with pytest.raises(AssertionError):
        runner.assert_repeat_digest_equality(
            records + [records[0]], ("one", "two"),
            case_field="case", digest_field="digest",
        )


def test_json_report_remains_byte_identical_and_trace_reader_retains_order(tmp_path):
    output = tmp_path / "nested" / "report.json"
    payload = {"z": [2, 1], "a": {"value": True}}
    expected = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    runner.write_json_report(output, payload)
    assert output.read_text() == expected
    trace = tmp_path / "trace.jsonl"
    trace.write_text('{"phase":1}\n{"phase":2,"evidence_complete":true}\n')
    assert runner.trace_rows(trace) == (
        {"phase": 1}, {"phase": 2, "evidence_complete": True},
    )
