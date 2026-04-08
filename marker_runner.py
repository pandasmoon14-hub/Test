#!/usr/bin/env python3
"""
Marker bridge — runs inside /workspace/venvs/marker/bin/python3

Uses the Python API directly so we can:
  1. Set EXTRACT_IMAGES=false before any marker import (env-level flag)
  2. Pass batch_multiplier for A6000 throughput tuning
  3. Never write image files to disk

Called by orchestrator.py via subprocess.  Writes one .md file to
--output_dir and emits a JSON status line on stdout so the orchestrator
can parse the result path without path-guessing.

Usage:
    /workspace/venvs/marker/bin/python3 marker_runner.py \\
        /path/to/file.pdf \\
        --output_dir /path/to/out \\
        [--batch_multiplier 4]
"""
import argparse
import json
import os
import sys
from pathlib import Path

# Set before any marker import — suppresses image extraction at the env level.
os.environ.setdefault("EXTRACT_IMAGES", "false")


def run_v1_api(pdf_path: Path, output_dir: Path, batch_multiplier: int) -> str:
    """marker-pdf v0.2.x / v1.x API (convert_single_pdf + load_all_models)."""
    from marker.convert import convert_single_pdf  # type: ignore
    from marker.models import load_all_models       # type: ignore

    models = load_all_models()
    full_text, _images, _metadata = convert_single_pdf(
        str(pdf_path),
        models,
        batch_multiplier=batch_multiplier,
    )
    # _images dict stays in memory; we never write it to disk.
    return full_text


def run_v2_api(pdf_path: Path, output_dir: Path, batch_multiplier: int) -> str:
    """marker-pdf v2.x API (PdfConverter + create_model_dict)."""
    from marker.converters.pdf import PdfConverter   # type: ignore
    from marker.models import create_model_dict       # type: ignore
    from marker.config.parser import ConfigParser     # type: ignore

    config_parser = ConfigParser({
        "output_format": "markdown",
        "batch_multiplier": batch_multiplier,
    })
    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
    )
    rendered = converter(str(pdf_path))
    return rendered.markdown


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf")
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--batch_multiplier", type=int, default=4,
                        help="GPU batch multiplier — 4 is well-suited to A6000 48 GB")
    args = parser.parse_args()

    pdf_path = Path(args.input_pdf)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not pdf_path.exists():
        print(json.dumps({"status": "error", "reason": "pdf_not_found", "path": str(pdf_path)}))
        sys.exit(1)

    full_text: str = ""
    try:
        full_text = run_v1_api(pdf_path, output_dir, args.batch_multiplier)
    except (ImportError, TypeError):
        try:
            full_text = run_v2_api(pdf_path, output_dir, args.batch_multiplier)
        except Exception as exc:
            print(json.dumps({"status": "error", "reason": str(exc)}))
            sys.exit(1)
    except Exception as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}))
        sys.exit(1)

    out_md = output_dir / f"{pdf_path.stem}.md"
    out_md.write_text(full_text, encoding="utf-8")

    print(json.dumps({
        "status": "ok",
        "md_path": str(out_md),
        "chars": len(full_text),
    }))


if __name__ == "__main__":
    main()
