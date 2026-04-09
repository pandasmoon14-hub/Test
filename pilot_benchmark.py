#!/usr/bin/env python3
"""
Pilot benchmark harness for Aether Forge.

Runs sampled pilot jobs and derives real lane throughput + escalation metrics
used to calibrate estimate_runtime assumptions.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class PilotRun:
    book: str
    pages: int
    lane: str
    elapsed_sec: float
    queued_pages: int
    status: str


def read_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run pilot benchmark for Aether Forge")
    parser.add_argument("--orchestrator_python", required=True)
    parser.add_argument("--orchestrator_script", required=True)
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--sample_size", type=int, default=10)
    parser.add_argument("--glob", default="*.pdf")
    parser.add_argument("--report", required=True)
    parser.add_argument("--env", nargs="*", default=[])
    return parser.parse_args()


def collect_candidates(input_dir: Path, glob: str, sample_size: int) -> list[Path]:
    files = [p for p in sorted(input_dir.glob(glob)) if p.is_file()]
    return files[:sample_size]


def run_single(
    orchestrator_python: str,
    orchestrator_script: str,
    input_dir: Path,
    output_dir: Path,
    pdf: Path,
    extra_env: dict[str, str],
) -> PilotRun:
    env = {**extra_env}
    env["INPUT_DIR"] = str(input_dir)
    env["OUTPUT_DIR"] = str(output_dir)

    start = time.perf_counter()
    cmd = [orchestrator_python, orchestrator_script, "--glob", pdf.name, "--limit", "1", "--resume"]
    result = subprocess.run(cmd, capture_output=True, text=True, env={**extra_env, **env})
    elapsed = time.perf_counter() - start

    manifest = output_dir / "manifests" / f"{pdf.stem}.manifest.json"
    m = read_manifest(manifest)

    lane = m.get("lane", "unknown")
    pages = int(m.get("chunk_count", 0))
    queued = len(m.get("failed_pages", [])) if isinstance(m.get("failed_pages"), list) else 0

    status = "ok" if result.returncode == 0 else "error"

    return PilotRun(
        book=pdf.name,
        pages=pages,
        lane=lane,
        elapsed_sec=round(elapsed, 3),
        queued_pages=queued,
        status=status,
    )


def summarize(runs: list[PilotRun]) -> dict[str, Any]:
    lanes: dict[str, int] = {}
    lane_time: dict[str, float] = {}
    ok_runs = [r for r in runs if r.status == "ok"]

    for run in ok_runs:
        lanes[run.lane] = lanes.get(run.lane, 0) + 1
        lane_time[run.lane] = lane_time.get(run.lane, 0.0) + run.elapsed_sec

    avg_time = sum(r.elapsed_sec for r in ok_runs) / max(1, len(ok_runs))

    return {
        "runs_total": len(runs),
        "runs_ok": len(ok_runs),
        "runs_error": len(runs) - len(ok_runs),
        "avg_book_sec": round(avg_time, 3),
        "lane_distribution": lanes,
        "lane_elapsed_sec": {k: round(v, 3) for k, v in lane_time.items()},
        "queued_pages_total": sum(r.queued_pages for r in ok_runs),
    }


def estimate_lane_ppm(runs: list[PilotRun]) -> dict[str, float]:
    # rough estimate using chunk_count proxy if page counts unavailable in manifest
    lane_pages: dict[str, float] = {}
    lane_seconds: dict[str, float] = {}
    for run in runs:
        if run.status != "ok":
            continue
        lane_pages[run.lane] = lane_pages.get(run.lane, 0.0) + max(1, run.pages)
        lane_seconds[run.lane] = lane_seconds.get(run.lane, 0.0) + max(0.001, run.elapsed_sec)

    ppm: dict[str, float] = {}
    for lane in lane_pages:
        ppm[lane] = round((lane_pages[lane] / lane_seconds[lane]) * 60.0, 4)
    return ppm


def main() -> None:
    args = parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    extra_env: dict[str, str] = {}
    for item in args.env:
        if "=" in item:
            k, v = item.split("=", 1)
            extra_env[k] = v

    candidates = collect_candidates(input_dir, args.glob, args.sample_size)

    runs: list[PilotRun] = []
    for pdf in candidates:
        run = run_single(
            args.orchestrator_python,
            args.orchestrator_script,
            input_dir,
            output_dir,
            pdf,
            extra_env,
        )
        runs.append(run)

    summary = summarize(runs)
    summary["lane_ppm_estimate"] = estimate_lane_ppm(runs)

    payload = {
        "summary": summary,
        "runs": [asdict(r) for r in runs],
    }

    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({"report": str(report), **summary}, indent=2))


if __name__ == "__main__":
    main()
