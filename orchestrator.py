#!/usr/bin/env python3
import json
import os
import re
import subprocess
from pathlib import Path

import fitz  # PyMuPDF

# --- CONFIGURATION ---
INPUT_DIR = Path(os.getenv("INPUT_DIR", "/workspace/ttrpg_input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/workspace/ttrpg_output"))
REPAIR_QUEUE_FILE = OUTPUT_DIR / "repair_queue" / "queue.json"

ENV_MARKER = "/workspace/venvs/marker/bin/marker_single"
ENV_DOCLING = "/workspace/venvs/docling/bin/docling"
ENV_OCRMYPDF = "/workspace/venvs/orchestrator/bin/ocrmypdf"

# Routing Thresholds
MIN_CHARS_FOR_NATIVE = 1000
WEIRD_CHAR_LIMIT = 0.03
SCAN_THRESHOLD = 50  # If chars per page < 50, it's a raw image scan


def analyze_pdf(pdf_path: Path):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    total_chars = 0
    weird_chars = 0

    for page in doc:
        text = page.get_text("text").replace("\x00", "")
        total_chars += len(text)
        weird_chars += len(re.findall(r"[^A-Za-z0-9\s.,?!;:()'\"]", text))
    doc.close()

    avg_chars = total_chars / max(1, total_pages)
    weird_ratio = weird_chars / max(1, total_chars)
    return avg_chars, weird_ratio, total_pages


def audit_markdown(md_path: Path, total_pages: int):
    if not md_path.exists():
        return list(range(total_pages))

    with open(md_path, "r", encoding="utf-8") as file:
        content = file.read()

    # If markdown output is severely underweight, flag all pages for fallback/repair.
    if len(content) / max(1, total_pages) < 150:
        return list(range(total_pages))

    # In a full implementation, markdown chunks should be mapped back to page ids.
    return []


def process_book(pdf: Path, repair_queue: dict):
    print(f"\n[PREFLIGHT] Analyzing {pdf.name}...")
    avg_chars, weird_ratio, total_pages = analyze_pdf(pdf)
    out_dir = OUTPUT_DIR / pdf.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    md_out = out_dir / f"{pdf.stem}.md"

    # --- LANE A: NATIVE FAST PATH ---
    if avg_chars > MIN_CHARS_FOR_NATIVE and weird_ratio < WEIRD_CHAR_LIMIT:
        print("  -> [LANE A] Native text is pristine. Extracting directly...")
        doc = fitz.open(pdf)
        with open(md_out, "w", encoding="utf-8") as file:
            for page in doc:
                file.write(page.get_text("text") + "\n\n")
        doc.close()
        return

    # --- PRE-PROCESSING: SCAN NORMALIZATION ---
    active_pdf = pdf
    if avg_chars < SCAN_THRESHOLD:
        print("  -> [PRE-PROCESS] Detected raw scan. Running OCRmyPDF normalization...")
        optimized_pdf = out_dir / f"{pdf.stem}_optimized.pdf"
        subprocess.run(
            [
                ENV_OCRMYPDF,
                "--optimize",
                "1",
                "--force-ocr",
                str(pdf),
                str(optimized_pdf),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if optimized_pdf.exists():
            active_pdf = optimized_pdf

    # --- LANE B: MARKER BULK CONVERSION ---
    print("  -> [LANE B] Executing Marker...")
    try:
        subprocess.run(
            [ENV_MARKER, str(active_pdf), "--output_dir", str(OUTPUT_DIR)],
            check=True,
            capture_output=True,
            text=True,
        )
        failed_pages = audit_markdown(md_out, total_pages)
        if not failed_pages:
            print("  -> [AUDIT] Passed. Archive Sealed.")
            return
    except subprocess.CalledProcessError:
        print("  ! [LANE B] Marker failed. Falling back to Docling...")
        failed_pages = list(range(total_pages))

    # --- LANE B2: DOCLING FALLBACK ---
    if failed_pages and len(failed_pages) == total_pages:
        print("  -> [LANE B2] Executing Docling...")
        try:
            subprocess.run(
                [ENV_DOCLING, str(active_pdf), "--to", "md", "--output", str(out_dir)],
                check=True,
                capture_output=True,
                text=True,
            )
            docling_md = out_dir / f"{active_pdf.stem}.md"
            failed_pages = audit_markdown(docling_md, total_pages)
            if not failed_pages:
                print("  -> [AUDIT] Docling recovery successful. Archive Sealed.")
                return
        except subprocess.CalledProcessError:
            print("  ! [LANE B2] Docling failed.")

    # --- ROUTE TO LANE C (PIXTRAL REPAIR) ---
    if failed_pages:
        print(
            f"  -> [ROUTING] Book requires VLM intervention. Queuing {len(failed_pages)} pages for Lane C."
        )
        repair_queue[str(active_pdf)] = {
            "failed_pages": failed_pages,
            "md_path": str(md_out),
        }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "repair_queue").mkdir(parents=True, exist_ok=True)

    if REPAIR_QUEUE_FILE.exists():
        with open(REPAIR_QUEUE_FILE, "r", encoding="utf-8") as file:
            repair_queue = json.load(file)
    else:
        repair_queue = {}

    pdfs = sorted(INPUT_DIR.glob("*.pdf"))
    for pdf in pdfs:
        process_book(pdf, repair_queue)
        # Checkpoint the queue after every book.
        with open(REPAIR_QUEUE_FILE, "w", encoding="utf-8") as file:
            json.dump(repair_queue, file, indent=2)


if __name__ == "__main__":
    main()
