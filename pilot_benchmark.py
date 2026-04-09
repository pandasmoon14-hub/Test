#!/usr/bin/env python3
"""
Pilot benchmark harness for Aether Forge.

Runs sampled pilot jobs and derives real lane throughput + escalation metrics
used to calibrate estimate_runtime assumptions.
"""

from __future__ import annotations

import argparse
import json
import os
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
    manual_review_count: int = 0
    unresolved_table_count: int = 0
    pages_remaining: int = 0


def read_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def count_manifest_pages(manifest: dict[str, Any], output_dir: Path, pdf_stem: str) -> int:
    for key in ("page_count", "total_pages", "pages_audited"):
        value = manifest.get(key)
        if isinstance(value, int) and value > 0:
            return value

    page_meta_path = manifest.get("page_metadata_path")
    candidate_paths = []
    if isinstance(page_meta_path, str) and page_meta_path.strip():
        candidate_paths.append(Path(page_meta_path))
    candidate_paths.append(output_dir / pdf_stem / f"{pdf_stem}.pages.json")
    for path in candidate_paths:
        if path.exists():
            try:
                rows = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(rows, list) and rows:
                    return len(rows)
            except (json.JSONDecodeError, OSError):
                continue

    # Keep an explicit hard floor only after exhausting all real-count sources.
    return 1


def parse_manifest_metrics(manifest: dict[str, Any]) -> dict[str, int]:
    if not manifest:
        return {"manual_review_count": 0, "unresolved_table_count": 0, "pages_remaining": 0}
    required = ["page_count", "pages_remaining", "pages_passed", "pages_audited"]
    missing = [k for k in required if k not in manifest]
    if missing:
        raise ValueError(f"manifest missing required schema fields: {missing}")
    return {
        "manual_review_count": int(manifest.get("manual_review_count", 0) or 0),
        "unresolved_table_count": int(manifest.get("unresolved_table_count", 0) or 0),
        "pages_remaining": int(manifest.get("pages_remaining", 0) or 0),
    }


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
    env = {**os.environ, **extra_env, "INPUT_DIR": str(input_dir), "OUTPUT_DIR": str(output_dir)}

    start = time.perf_counter()
    cmd = [orchestrator_python, orchestrator_script, "--glob", pdf.name, "--limit", "1", "--resume"]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    elapsed = time.perf_counter() - start

    manifest = output_dir / "manifests" / f"{pdf.stem}.manifest.json"
    m = read_manifest(manifest)

    lane = m.get("lane", "unknown")
    pages = int(m.get("total_pages", 0) or m.get("pages_detected", 0) or 0)
    if pages <= 0:
        md_path = Path(m.get("output_md", ""))
        if md_path.exists():
            pages = max(1, sum(1 for line in md_path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip().startswith("<!-- PAGE:")))
    pages = max(1, pages)
    queued = len(m.get("failed_pages", [])) if isinstance(m.get("failed_pages"), list) else 0

    status = "ok" if result.returncode == 0 else "error"
    lane = m.get("lane", "unknown")
    pages = 1
    queued = 0
    metrics = {"manual_review_count": 0, "unresolved_table_count": 0, "pages_remaining": 0}
    if m:
        try:
            pages = count_manifest_pages(m, output_dir, pdf.stem)
        except ValueError:
            status = "error"
        queued = len(m.get("failed_pages", [])) if isinstance(m.get("failed_pages"), list) else 0
        try:
            metrics = parse_manifest_metrics(m)
        except ValueError:
            status = "error"

    return PilotRun(
        book=pdf.name,
        pages=pages,
        lane=lane,
        elapsed_sec=round(elapsed, 3),
        queued_pages=queued,
        status=status,
        manual_review_count=metrics["manual_review_count"],
        unresolved_table_count=metrics["unresolved_table_count"],
        pages_remaining=metrics["pages_remaining"],
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
        "manual_review_total": sum(r.manual_review_count for r in ok_runs),
        "unresolved_table_total": sum(r.unresolved_table_count for r in ok_runs),
        "pages_remaining_total": sum(r.pages_remaining for r in ok_runs),
    }


def estimate_lane_ppm(runs: list[PilotRun]) -> dict[str, float]:
    # throughput estimate from real page counts (manifest total_pages or page marker count)
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
