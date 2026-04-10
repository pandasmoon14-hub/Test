#!/usr/bin/env python3
"""
Marker bridge (Lane B)

This wrapper normalizes API differences between marker versions and ensures
JSON-formatted results for orchestrator consumption.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

# No-image policy defaults.
os.environ.setdefault("EXTRACT_IMAGES", "false")
os.environ.setdefault("SAVE_IMAGES", "false")


@dataclass
class MarkerResult:
    status: str
    md_path: str | None = None
    chars: int | None = None
    elapsed_sec: float | None = None
    api_variant: str | None = None
    reason: str | None = None
    path: str | None = None
    details: dict[str, Any] | None = None
    page_map_path: str | None = None
    total_pages_seen: int | None = None
    pages_emitted: int | None = None
    tables_detected: int | None = None
    warnings: list[str] | None = None
    timeout_context: str | None = None
    mode: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Marker API bridge for PDF->Markdown")
    parser.add_argument("input_pdf", help="Path to source PDF")
    parser.add_argument("--output_dir", required=True, help="Output directory")
    parser.add_argument(
        "--batch_multiplier",
        type=int,
        default=2,
        help="GPU batch multiplier for marker model execution",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail when markdown output is empty",
    )
    parser.add_argument(
        "--page_map_json",
        default="",
        help="Optional path to write per-page source-grounded markdown map",
    )
    return parser.parse_args()


def _safe_path(path: Path) -> str:
    try:
        return str(path.resolve())
    except OSError:
        return str(path)


def run_v1_api(pdf_path: Path, batch_multiplier: int) -> tuple[str, str]:
    from marker.convert import convert_single_pdf  # type: ignore
    from marker.models import load_all_models  # type: ignore

    models = load_all_models()
    full_text, _images, _metadata = convert_single_pdf(
        str(pdf_path), models, batch_multiplier=batch_multiplier
    )
    return full_text, "v1"


def run_v2_api(pdf_path: Path, batch_multiplier: int) -> tuple[str, str]:
    from marker.converters.pdf import PdfConverter  # type: ignore
    from marker.models import create_model_dict  # type: ignore
    from marker.config.parser import ConfigParser  # type: ignore

    config_parser = ConfigParser(
        {
            "output_format": "markdown",
            "batch_multiplier": batch_multiplier,
            "extract_images": False,
            "extract_tables": True,
        }
    )
    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
    )
    rendered = converter(str(pdf_path))
    return rendered.markdown, "v2"


def _parse_page_markers(markdown: str) -> dict[int, str]:
    if "<!-- PAGE:" not in markdown:
        return {}
    pages: dict[int, list[str]] = {}
    current: int | None = None
    pages: dict[int, list[str]] = {}
    current = 1
    for line in markdown.splitlines():
        marker = line.strip()
        if marker.startswith("<!-- PAGE:") and marker.endswith("-->"):
            num = marker.replace("<!-- PAGE:", "").replace("-->", "").strip()
            if num.isdigit():
                current = int(num)
                pages.setdefault(current, [])
                continue
        if current is not None:
            pages.setdefault(current, []).append(line)
        pages.setdefault(current, []).append(line)
    return {p: "\n".join(lines).strip() for p, lines in pages.items()}


def write_page_map(markdown: str, page_map_path: Path) -> dict[str, Any]:
    page_map: list[dict[str, Any]] = []
    pages = _parse_page_markers(markdown)
    for idx in sorted(pages):
        text = pages[idx]
        tables_detected = sum(1 for line in text.splitlines() if line.count("|") >= 2)
        page_map.append({
            "source_page": idx,
            "markdown": text.strip(),
            "tables_detected": tables_detected,
        })
    page_map_path.parent.mkdir(parents=True, exist_ok=True)
    page_map_path.write_text(json.dumps(page_map, indent=2, ensure_ascii=False), encoding="utf-8")
    return {
        "path": _safe_path(page_map_path),
        "total_pages_seen": len(page_map),
        "pages_emitted": sum(1 for row in page_map if row["markdown"]),
        "tables_detected": sum(int(row["tables_detected"]) for row in page_map),
    }


def convert_with_marker(pdf_path: Path, output_dir: Path, batch_multiplier: int, page_map_json: str) -> MarkerResult:
    start = time.perf_counter()

    if not pdf_path.exists():
        return MarkerResult(
            status="error",
            reason="pdf_not_found",
            path=_safe_path(pdf_path),
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    warnings: list[str] = []
    try:
        try:
            markdown, api = run_v1_api(pdf_path, batch_multiplier=batch_multiplier)
            mode = "single_file"
        except (ImportError, TypeError, AttributeError):
            markdown, api = run_v2_api(pdf_path, batch_multiplier=batch_multiplier)
            mode = "single_file"
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return MarkerResult(
            status="error",
            reason=str(exc),
            path=_safe_path(pdf_path),
            details={"traceback": traceback.format_exc(limit=8)},
        )

    out_md = output_dir / f"{pdf_path.stem}.md"
    out_md.write_text(markdown, encoding="utf-8")
    page_map_stats: dict[str, Any] = {}
    if page_map_json:
        page_map_stats = write_page_map(markdown, Path(page_map_json))
        if page_map_stats.get("total_pages_seen", 0) == 0:
            warnings.append("no_source_page_markers")
        if page_map_stats["pages_emitted"] == 0:
            warnings.append("page_map_empty")

    elapsed = time.perf_counter() - start
    return MarkerResult(
        status="ok",
        md_path=_safe_path(out_md),
        chars=len(markdown),
        elapsed_sec=round(elapsed, 3),
        api_variant=api,
        path=_safe_path(pdf_path),
        page_map_path=page_map_stats.get("path"),
        total_pages_seen=page_map_stats.get("total_pages_seen"),
        pages_emitted=page_map_stats.get("pages_emitted"),
        tables_detected=page_map_stats.get("tables_detected"),
        warnings=warnings,
        timeout_context="none",
        mode=mode,
    )


def main() -> None:
    args = parse_args()

    result = convert_with_marker(
        Path(args.input_pdf),
        Path(args.output_dir),
        batch_multiplier=args.batch_multiplier,
        page_map_json=args.page_map_json,
    )

    if args.strict and result.status == "ok" and (result.chars or 0) == 0:
        result = MarkerResult(
            status="error",
            reason="empty_markdown",
            md_path=result.md_path,
            chars=result.chars,
            elapsed_sec=result.elapsed_sec,
            api_variant=result.api_variant,
            path=result.path,
            page_map_path=result.page_map_path,
            total_pages_seen=result.total_pages_seen,
            pages_emitted=result.pages_emitted,
            tables_detected=result.tables_detected,
            warnings=result.warnings,
            timeout_context=result.timeout_context,
            mode=result.mode,
        )

    print(json.dumps(asdict(result), ensure_ascii=False))
    if result.status != "ok":
        sys.exit(1)


if __name__ == "__main__":
    main()
