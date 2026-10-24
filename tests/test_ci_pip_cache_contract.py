"""Guard CI dependency caching without changing certification workload."""
from pathlib import Path


def test_all_full_ci_python_jobs_have_dependency_fingerprinted_pip_cache():
    workflow = (Path(__file__).resolve().parents[1]
                / ".github" / "workflows" / "ci.yml").read_text()
    sections = workflow.split("uses: actions/setup-python@v6")
    assert len(sections) > 1, "full CI must configure Python"
    for section in sections[1:]:
        setup = section.split("      - name:", 1)[0]
        assert "python-version: \"3.12\"" in setup
        assert "cache: pip" in setup
        assert "cache-dependency-path: |" in setup
        for dependency in ("requirements-ci.txt", "requirements-dev.txt",
                           "pyproject.toml"):
            assert dependency in setup


def test_full_ci_keeps_both_owning_platform_suites_and_exact_candidate_checkout():
    workflow = (Path(__file__).resolve().parents[1]
                / ".github" / "workflows" / "ci.yml").read_text()
    assert "name: core-linux" in workflow
    assert "name: core-windows" in workflow
    assert "run: python -m pytest -q -n 2 --dist loadfile" in workflow
    assert "run: python -m pytest -q --durations=50" in workflow
    assert "ref: ${{ github.event.pull_request.head.sha || github.sha }}" in workflow
    assert "timeout-minutes: 40" in workflow
