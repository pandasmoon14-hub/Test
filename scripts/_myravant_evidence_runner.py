"""Shared, presentation-neutral mechanics for retained installed-evidence scripts.

This module owns only developer evidence plumbing. Individual reporters retain
their own playable objectives, fixtures, domain checks, and replay assertions.
"""
import json
from pathlib import Path
import subprocess
from typing import Any, Iterable, Mapping, Sequence


def resolve_repository_sha(explicit: str | None) -> str:
    """Resolve exact checkout identity; do not accept synthetic or partial IDs."""
    sha = explicit if explicit is not None else subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, timeout=15
    ).strip()
    if len(sha) != 40 or any(char not in "0123456789abcdef" for char in sha):
        raise ValueError("retained evidence requires a lowercase 40-character Git SHA")
    return sha


def run_installed_session(
    launcher: str,
    flags: Sequence[str],
    checkpoint: Path,
    trace: Path,
    repository_sha: str,
    commands: Iterable[str],
    *,
    load: bool = False,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    """Run the public installed CLI, preserving argument and input ordering.

    Return the raw result so the owning reporter can assert its own failure
    details and check its checkpoint before reading the trace.
    """
    args = [
        launcher, *flags, "--checkpoint", str(checkpoint),
        "--trace", str(trace), "--repository-sha", repository_sha,
    ]
    if load:
        args.extend(("--load", str(checkpoint)))
    return subprocess.run(
        args, input="\n".join((*commands, "save", "exit", "")),
        text=True, capture_output=True, timeout=timeout,
    )


def trace_rows(path: Path) -> tuple[dict[str, Any], ...]:
    """Read JSON-lines trace without declaring its contents authoritative."""
    return tuple(json.loads(line) for line in path.read_text().splitlines())


def assert_repeat_digest_equality(
    runs: Sequence[Mapping[str, Any]],
    cases: Sequence[str],
    *,
    case_field: str,
    digest_field: str,
) -> None:
    """Require exactly two independent runs and equal final digests per case."""
    for case in cases:
        pair = [run for run in runs if run[case_field] == case]
        assert len(pair) == 2 and pair[0][digest_field] == pair[1][digest_field], (
            case, pair
        )


def write_json_report(path: Path, payload: Mapping[str, Any]) -> None:
    """Retain the established sorted, indented, newline-terminated JSON bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
