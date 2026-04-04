#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from astra_cloud.routing.classifier import classify_chunk
from astra_cloud.routing.policies import assign_route


def iter_chunks(text: str, chunk_size: int = 4000) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for para in paragraphs:
        if current_len + len(para) + 2 > chunk_size and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = len(para)
        else:
            current.append(para)
            current_len += len(para) + 2
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Chunk and classify a normalized markdown file.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--sourcebook-id", default="sourcebook")
    parser.add_argument("--chunk-size", type=int, default=4000)
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8", errors="ignore")
    chunks = iter_chunks(text, chunk_size=args.chunk_size)

    with args.output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "chunk_id",
            "chunk_type",
            "size_class",
            "char_count",
            "artifact_score",
            "ambiguity_score",
            "predicted_validator_risk",
            "assigned_route",
            "final_route",
            "rationale",
        ])
        for idx, chunk in enumerate(chunks, start=1):
            chunk_id = f"chunk_{idx:04d}"
            features = classify_chunk(chunk_id=chunk_id, sourcebook_id=args.sourcebook_id, text=chunk)
            decision = assign_route(features)
            writer.writerow([
                chunk_id,
                features.chunk_type.value,
                features.chunk_size_class.value,
                features.char_count,
                f"{features.artifact_score:.2f}",
                f"{features.ambiguity_score:.2f}",
                f"{features.predicted_validator_risk:.2f}",
                decision.assigned_route.value,
                decision.final_route.value,
                decision.rationale,
            ])


if __name__ == "__main__":
    main()
