#!/usr/bin/env python3
"""
Runtime estimator for large TTRPG extraction batches.

Estimates total wall time for a corpus of PDFs by modeling lane distribution,
average pages/book, and effective throughput per lane.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class ThroughputAssumptions:
    lane_a_pages_per_min: float
    lane_b_pages_per_min: float
    lane_b2_pages_per_min: float
    lane_c_pages_per_min: float


@dataclass
class MixAssumptions:
    lane_a_ratio: float
    lane_b_ratio: float
    lane_b2_ratio: float
    lane_c_ratio: float


@dataclass
class EstimateInputs:
    books: int
    min_pages: int
    max_pages: int
    avg_pages: float
    assumptions: ThroughputAssumptions
    mix: MixAssumptions


@dataclass
class EstimateResult:
    total_pages: float
    lane_pages: dict[str, float]
    lane_minutes: dict[str, float]
    total_minutes: float
    total_hours: float
    total_days_continuous: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Estimate runtime for Aether Forge")
    parser.add_argument("--books", type=int, default=1876)
    parser.add_argument("--min_pages", type=int, default=100)
    parser.add_argument("--max_pages", type=int, default=700)
    parser.add_argument("--avg_pages", type=float, default=320.0)

    parser.add_argument("--lane_a_ratio", type=float, default=0.35)
    parser.add_argument("--lane_b_ratio", type=float, default=0.40)
    parser.add_argument("--lane_b2_ratio", type=float, default=0.15)
    parser.add_argument("--lane_c_ratio", type=float, default=0.10)

    parser.add_argument("--lane_a_ppm", type=float, default=160.0)
    parser.add_argument("--lane_b_ppm", type=float, default=42.0)
    parser.add_argument("--lane_b2_ppm", type=float, default=28.0)
    parser.add_argument("--lane_c_ppm", type=float, default=7.5)

    return parser.parse_args()


def normalize_mix(mix: MixAssumptions) -> MixAssumptions:
    total = mix.lane_a_ratio + mix.lane_b_ratio + mix.lane_b2_ratio + mix.lane_c_ratio
    if total <= 0:
        raise ValueError("Lane mix ratio total must be > 0")
    return MixAssumptions(
        lane_a_ratio=mix.lane_a_ratio / total,
        lane_b_ratio=mix.lane_b_ratio / total,
        lane_b2_ratio=mix.lane_b2_ratio / total,
        lane_c_ratio=mix.lane_c_ratio / total,
    )


def estimate(inputs: EstimateInputs) -> EstimateResult:
    total_pages = inputs.books * inputs.avg_pages

    lane_pages = {
        "A": total_pages * inputs.mix.lane_a_ratio,
        "B": total_pages * inputs.mix.lane_b_ratio,
        "B2": total_pages * inputs.mix.lane_b2_ratio,
        "C": total_pages * inputs.mix.lane_c_ratio,
    }

    lane_minutes = {
        "A": lane_pages["A"] / max(0.001, inputs.assumptions.lane_a_pages_per_min),
        "B": lane_pages["B"] / max(0.001, inputs.assumptions.lane_b_pages_per_min),
        "B2": lane_pages["B2"] / max(0.001, inputs.assumptions.lane_b2_pages_per_min),
        "C": lane_pages["C"] / max(0.001, inputs.assumptions.lane_c_pages_per_min),
    }

    total_minutes = sum(lane_minutes.values())
    total_hours = total_minutes / 60.0
    total_days = total_hours / 24.0

    return EstimateResult(
        total_pages=total_pages,
        lane_pages=lane_pages,
        lane_minutes=lane_minutes,
        total_minutes=total_minutes,
        total_hours=total_hours,
        total_days_continuous=total_days,
    )


def render_human_summary(inputs: EstimateInputs, result: EstimateResult) -> dict:
    return {
        "inputs": asdict(inputs),
        "result": asdict(result),
        "human_summary": {
            "books": inputs.books,
            "avg_pages_per_book": inputs.avg_pages,
            "estimated_total_pages": round(result.total_pages),
            "estimated_total_hours": round(result.total_hours, 2),
            "estimated_total_days_24x7": round(result.total_days_continuous, 2),
            "estimated_total_days_16h_day": round(result.total_hours / 16.0, 2),
            "low_high_page_bounds": {
                "low_total_pages": inputs.books * inputs.min_pages,
                "high_total_pages": inputs.books * inputs.max_pages,
            },
        },
    }


def main() -> None:
    args = parse_args()

    mix = normalize_mix(
        MixAssumptions(
            lane_a_ratio=args.lane_a_ratio,
            lane_b_ratio=args.lane_b_ratio,
            lane_b2_ratio=args.lane_b2_ratio,
            lane_c_ratio=args.lane_c_ratio,
        )
    )

    assumptions = ThroughputAssumptions(
        lane_a_pages_per_min=args.lane_a_ppm,
        lane_b_pages_per_min=args.lane_b_ppm,
        lane_b2_pages_per_min=args.lane_b2_ppm,
        lane_c_pages_per_min=args.lane_c_ppm,
    )

    inputs = EstimateInputs(
        books=args.books,
        min_pages=args.min_pages,
        max_pages=args.max_pages,
        avg_pages=args.avg_pages,
        assumptions=assumptions,
        mix=mix,
    )

    result = estimate(inputs)
    payload = render_human_summary(inputs, result)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
