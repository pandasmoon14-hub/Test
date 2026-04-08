#!/usr/bin/env python3
"""
Docling bridge — runs inside /workspace/venvs/docling/bin/python3
"""
import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf")
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()

    pdf_path = Path(args.input_pdf)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not pdf_path.exists():
        print(json.dumps({"status": "error", "reason": "pdf_not_found", "path": str(pdf_path)}))
        sys.exit(1)

    try:
        from docling.document_converter import DocumentConverter  # type: ignore

        # Try the full pipeline-options API first (docling >= 1.x).
        # Fall back to a bare converter if the imports don't exist.
        try:
            from docling.datamodel.pipeline_options import PdfPipelineOptions  # type: ignore
            from docling.datamodel.base_models import InputFormat               # type: ignore
            from docling.document_converter import PdfFormatOption              # type: ignore

            opts = PdfPipelineOptions()
            opts.generate_page_images    = False   # no page renders saved to disk
            opts.generate_picture_images = False   # no figure images saved to disk

            converter = DocumentConverter(
                format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
            )
        except (ImportError, AttributeError):
            converter = DocumentConverter()

        result = converter.convert(str(pdf_path))
        md = result.document.export_to_markdown()

    except Exception as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}))
        sys.exit(1)

    out_md = output_dir / f"{pdf_path.stem}.md"
    out_md.write_text(md, encoding="utf-8")

    print(json.dumps({
        "status": "ok",
        "md_path": str(out_md),
        "chars": len(md),
    }))


if __name__ == "__main__":
    main()
