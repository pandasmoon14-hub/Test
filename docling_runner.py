#!/usr/bin/env python3
"""
Docling bridge (Lane B2)

Runs inside a dedicated docling virtual environment and exposes a stable CLI for
orchestrator integration. The bridge intentionally keeps image-generation disabled
to enforce a no-image-output policy for extraction lanes.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class RunnerResult:
    status: str
    md_path: str | None = None
    chars: int | None = None
    elapsed_sec: float | None = None
    reason: str | None = None
    path: str | None = None
    details: dict[str, Any] | None = None


def _print(result: RunnerResult) -> None:
    print(json.dumps(asdict(result), ensure_ascii=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Docling bridge for PDF->Markdown conversion with stable JSON output"
    )
    parser.add_argument("input_pdf", help="Path to source PDF")
    parser.add_argument("--output_dir", required=True, help="Directory for markdown output")
    parser.add_argument(
        "--disable_images",
        action="store_true",
        default=True,
        help="Disable image generation in docling pipeline options",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if markdown output is empty",
    )
    return parser.parse_args()


def _build_converter(disable_images: bool):
    from docling.document_converter import DocumentConverter  # type: ignore

    if not disable_images:
        return DocumentConverter()

    try:
        from docling.datamodel.pipeline_options import PdfPipelineOptions  # type: ignore
        from docling.datamodel.base_models import InputFormat  # type: ignore
        from docling.document_converter import PdfFormatOption  # type: ignore

        opts = PdfPipelineOptions()
        opts.generate_page_images = False
        opts.generate_picture_images = False
        if hasattr(opts, "do_table_structure"):
            opts.do_table_structure = True

        return DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
        )
    except (ImportError, AttributeError):
        return DocumentConverter()


def _safe_readable_path(path: Path) -> str:
    try:
        return str(path.resolve())
    except OSError:
        return str(path)


def convert_pdf(input_pdf: Path, output_dir: Path, disable_images: bool) -> RunnerResult:
    start = time.perf_counter()

    if not input_pdf.exists():
        return RunnerResult(
            status="error",
            reason="pdf_not_found",
            path=_safe_readable_path(input_pdf),
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        converter = _build_converter(disable_images)
        result = converter.convert(str(input_pdf))
        markdown = result.document.export_to_markdown()
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return RunnerResult(
            status="error",
            reason=str(exc),
            path=_safe_readable_path(input_pdf),
            details={
                "traceback": traceback.format_exc(limit=8),
            },
        )

    out_md = output_dir / f"{input_pdf.stem}.md"
    out_md.write_text(markdown, encoding="utf-8")

    elapsed = time.perf_counter() - start
    return RunnerResult(
        status="ok",
        md_path=_safe_readable_path(out_md),
        chars=len(markdown),
        elapsed_sec=round(elapsed, 3),
        path=_safe_readable_path(input_pdf),
    )


def main() -> None:
    args = parse_args()

    input_pdf = Path(args.input_pdf)
    output_dir = Path(args.output_dir)

    result = convert_pdf(input_pdf, output_dir, disable_images=args.disable_images)

    if args.strict and result.status == "ok" and (result.chars or 0) == 0:
        result = RunnerResult(
            status="error",
            reason="empty_markdown",
            md_path=result.md_path,
            chars=result.chars,
            elapsed_sec=result.elapsed_sec,
            path=result.path,
        )

    _print(result)
    if result.status != "ok":
        sys.exit(1)


if __name__ == "__main__":
    main()
