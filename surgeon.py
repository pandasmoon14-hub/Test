"""
Aether Forge (v10) - Pixtral Surgeon (Lane C)
VLM-powered page repair for books that defeated Lanes A & B.

Run in the pixtral environment:
    /workspace/venvs/pixtral/bin/python3 /workspace/surgeon.py

Environment variables:
    OUTPUT_DIR  - Root output directory (default: /workspace/ttrpg_output)

This script:
1. Loads the repair queue written by orchestrator.py
2. Spins up Pixtral-12B once via vLLM (shared across all books)
3. Renders each failed page at 220 DPI → base64 PNG
4. Submits each page image to Pixtral with a structured transcription prompt
5. Appends the VLM output into the book's existing markdown file
6. Removes completed entries from the queue so the run is resumable
"""

import base64
import json
import os
import sys
from io import BytesIO
from pathlib import Path

import fitz          # PyMuPDF (available in the pixtral venv)
import PIL.Image
from vllm import LLM, SamplingParams

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/workspace/ttrpg_output"))
QUEUE_FILE  = OUTPUT_DIR / "repair_queue" / "queue.json"

MODEL_NAME = "mistralai/Pixtral-12B-2409"

# vLLM / GPU knobs
# 0.85 leaves ~3 GB headroom on a 48 GB A6000 for system/CUDA overhead.
GPU_MEMORY_UTILIZATION = 0.85
MAX_MODEL_LEN          = 16384    # fits full-page OCR comfortably within context
ONE_IMAGE_PER_CALL     = 1        # Pixtral-12B performs best with one image per call

# Image rendering
DPI               = 220    # high enough for crisp OCR without OOM on large pages
MIN_CROP_SIZE     = 96     # skip pathologically tiny pages (px in either dimension)
MAX_TOKENS        = 2048   # generous ceiling for dense tables / formulae

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def pil_to_b64(img: PIL.Image.Image) -> str:
    """Encode a PIL image as a base64 PNG string."""
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def page_to_pil(page: fitz.Page, dpi: int = DPI) -> PIL.Image.Image:
    """Render a PyMuPDF page to a PIL RGB image at the given DPI."""
    pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB)
    return PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)


def build_repair_prompt(page_number: int) -> str:
    return (
        "You are a precise document transcription engine. "
        "Your only task is to transcribe the content of this page exactly as it appears. "
        "Rules:\n"
        "- Reproduce all headings, paragraphs, lists, captions, and footnotes verbatim.\n"
        "- Reconstruct every table as a valid GitHub-Flavored Markdown table.\n"
        "- Render equations in LaTeX inside $...$ (inline) or $$...$$ (block) delimiters.\n"
        "- Do NOT summarise, interpret, or add commentary.\n"
        "- Do NOT include page numbers or running headers in the output.\n"
        "- Output only the transcribed content in Markdown. No preamble.\n"
        f"This is page {page_number}."
    )


# ---------------------------------------------------------------------------
# Core repair routine
# ---------------------------------------------------------------------------

def repair_book(llm: LLM, pdf_path_str: str, data: dict) -> None:
    """
    Open the PDF, render each failed page, and append Pixtral's output to
    the book's existing markdown file.
    """
    pdf_path    = Path(pdf_path_str)
    failed_pages: list[int] = data["failed_pages"]
    md_path     = Path(data["md_path"])
    md_path.parent.mkdir(parents=True, exist_ok=True)

    if not pdf_path.exists():
        print(f"  [SKIP] PDF not found on disk: {pdf_path}. Skipping.")
        return

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)

    sampling_params = SamplingParams(
        temperature=0.0,
        max_tokens=MAX_TOKENS,
    )

    salvaged = 0
    skipped  = 0

    with open(md_path, "a", encoding="utf-8") as out_file:
        out_file.write("\n\n---\n## LANE C: PIXTRAL VLM REPAIR\n---\n\n")

        for pg_num in failed_pages:
            if pg_num >= total_pages:
                print(f"      [SKIP] Page {pg_num+1} out of range ({total_pages} pages total).")
                skipped += 1
                continue

            page = doc[pg_num]
            img  = page_to_pil(page)

            if img.width < MIN_CROP_SIZE or img.height < MIN_CROP_SIZE:
                print(f"      [SKIP] Page {pg_num+1} image too small ({img.width}×{img.height}px).")
                skipped += 1
                continue

            print(f"      [REPAIR] Salvaging page {pg_num+1}/{total_pages}  "
                  f"({img.width}×{img.height}px)...")

            b64 = pil_to_b64(img)

            # vLLM chat interface expects a list-of-conversations; we send one.
            messages = [[{
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": build_repair_prompt(pg_num + 1)},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/png;base64,{b64}"}},
                ],
            }]]

            try:
                outputs = llm.chat(
                    messages=messages,
                    sampling_params=sampling_params,
                    use_tqdm=False,
                )
                text = outputs[0].outputs[0].text.strip()
                out_file.write(f"\n### Page {pg_num + 1}\n\n{text}\n")
                salvaged += 1
            except Exception as exc:
                print(f"         [WARN] Pixtral failed on page {pg_num+1}: {exc}")
                out_file.write(f"\n### Page {pg_num + 1}\n\n<!-- REPAIR FAILED: {exc} -->\n")

    doc.close()
    print(f"  [DONE] {salvaged} pages repaired, {skipped} skipped → {md_path.name}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if not QUEUE_FILE.exists():
        print("[INFO]  No repair queue found. Pipeline is clean.")
        return

    with open(QUEUE_FILE, "r") as fh:
        queue: dict = json.load(fh)

    if not queue:
        print("[INFO]  Repair queue is empty. Pipeline is clean.")
        return

    total_books  = len(queue)
    total_pages  = sum(len(v["failed_pages"]) for v in queue.values())
    print(f"[INFO]  Repair queue: {total_books} book(s), {total_pages} page(s) total.")

    # Load Pixtral-12B once; keep it resident for the entire queue.
    print(f"\n[LOAD]  Initialising {MODEL_NAME}...")
    print(f"        gpu_memory_utilization={GPU_MEMORY_UTILIZATION}  "
          f"max_model_len={MAX_MODEL_LEN}")
    llm = LLM(
        model=MODEL_NAME,
        tokenizer_mode="mistral",
        limit_mm_per_prompt={"image": ONE_IMAGE_PER_CALL},
        max_model_len=MAX_MODEL_LEN,
        gpu_memory_utilization=GPU_MEMORY_UTILIZATION,
        enforce_eager=True,          # avoids CUDA graph compilation overhead
    )
    print("[LOAD]  Model ready.\n")

    for pdf_path_str, data in list(queue.items()):
        book_name = Path(pdf_path_str).name
        pages     = data["failed_pages"]
        print(f"\n[BOOK]  {book_name}  ({len(pages)} page(s) to repair)")

        repair_book(llm, pdf_path_str, data)

        # Remove from queue and checkpoint immediately; if the run is killed
        # mid-corpus we don't re-process books that were already finished.
        del queue[pdf_path_str]
        with open(QUEUE_FILE, "w") as fh:
            json.dump(queue, fh, indent=2)

    print("\n[SUMMARY] All repairs complete. Repair queue cleared.")


if __name__ == "__main__":
    main()
