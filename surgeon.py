#!/usr/bin/env python3
"""
Aether Forge (v10) — Pixtral Surgeon (Lane C)

Loads Pixtral-12B once via vLLM, repairs every page in the queue,
then checkpoints after each book so the run is resumable.

Images are rendered into memory (PIL/BytesIO) and never written to disk.

Key correctness fix: each page is a single vLLM conversation — a flat
list of message dicts [{"role": ..., "content": ...}].  The old double-
nested form [[{...}]] caused vLLM's message parser to call message["role"]
on a list instead of a dict, producing a hard TypeError.

For throughput: failed pages are sent to vLLM in mini-batches.  Each
batch element is one conversation list, so the batch wire format is
[[msg_dict], [msg_dict], ...] — a List[List[dict]] which vLLM's chat()
API accepts as a parallel batch of independent requests.

Run in the pixtral environment:
    /workspace/venvs/pixtral/bin/python3 /workspace/surgeon.py
"""
import base64
import json
import os
from io import BytesIO
from pathlib import Path

import fitz  # PyMuPDF
import PIL.Image
from vllm import LLM, SamplingParams

OUTPUT_DIR      = Path(os.getenv("OUTPUT_DIR",      "/workspace/ttrpg_output"))
QUEUE_FILE      = OUTPUT_DIR / "repair_queue" / "queue.json"
MODEL_NAME      = os.getenv("PIXTRAL_MODEL",        "mistralai/Pixtral-12B-2409")
MIN_CROP_SIZE   = int(os.getenv("MIN_CROP_SIZE",    "96"))
MAX_PAGE_TOKENS = int(os.getenv("MAX_PAGE_TOKENS",  "2048"))
REPAIR_BATCH    = int(os.getenv("REPAIR_BATCH",     "8"))   # pages per vLLM batch call
RENDER_DPI      = int(os.getenv("RENDER_DPI",       "220"))

PROMPT = (
    "Transcribe this page to Markdown exactly as it appears. "
    "Preserve all headings, paragraphs, and list structure verbatim. "
    "Reconstruct every table as a valid GitHub-Flavored Markdown table. "
    "Render equations as LaTeX ($...$ inline, $$...$$ block). "
    "Do NOT summarise, interpret, or add commentary. "
    "Output only the transcribed content. No preamble."
)


# ---------------------------------------------------------------------------
# Image helpers — in-memory only, nothing touches disk
# ---------------------------------------------------------------------------

def render_page(page: fitz.Page) -> PIL.Image.Image | None:
    """Render one PDF page to an in-memory RGB image. Returns None if too small."""
    pix = page.get_pixmap(dpi=RENDER_DPI, colorspace=fitz.csRGB)
    img = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if img.width < MIN_CROP_SIZE or img.height < MIN_CROP_SIZE:
        return None
    return img


def pil_to_b64(img: PIL.Image.Image) -> str:
    """Encode PIL image as base64 PNG entirely in memory."""
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


# ---------------------------------------------------------------------------
# vLLM message builder
# ---------------------------------------------------------------------------

def make_conversation(img: PIL.Image.Image) -> list[dict]:
    """
    Build one vLLM conversation for a single page image.

    Returns a flat list of message dicts — the correct format for one
    conversation in vLLM's chat() API.  When batching, the caller wraps
    multiple conversations: [make_conversation(img1), make_conversation(img2), ...]
    which gives [[msg], [msg], ...] — a valid List[List[dict]] batch.
    """
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{pil_to_b64(img)}"},
                },
            ],
        }
    ]


# ---------------------------------------------------------------------------
# Core repair routine
# ---------------------------------------------------------------------------

def repair_book(llm: LLM, record: dict) -> bool:
    pdf_path        = Path(record["file"])
    failed_pages: list[int] = record.get("failed_pages", [])
    md_path         = Path(record.get("md_path") or
                           OUTPUT_DIR / pdf_path.stem / "repair_log.md")
    full_book_repair: bool = record.get("full_book_repair", False)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    if not pdf_path.exists():
        print(f"  [SKIP] {pdf_path.name}: source PDF missing.")
        return False

    sampling = SamplingParams(temperature=0.0, max_tokens=MAX_PAGE_TOKENS)

    # Render all queued pages into memory up front.
    page_images: list[tuple[int, PIL.Image.Image]] = []
    with fitz.open(str(pdf_path)) as doc:
        for pg_num in failed_pages:
            if pg_num >= len(doc):
                continue
            img = render_page(doc[pg_num])
            if img is not None:
                page_images.append((pg_num, img))

    if not page_images:
        print(f"  [SKIP] {pdf_path.name}: no renderable pages in repair set.")
        return False

    # Process in mini-batches; each batch is a List[List[dict]] (vLLM batch API).
    results: dict[int, str] = {}
    for batch_start in range(0, len(page_images), REPAIR_BATCH):
        batch = page_images[batch_start : batch_start + REPAIR_BATCH]
        first, last = batch[0][0] + 1, batch[-1][0] + 1
        print(f"  [REPAIR] Pages {first}–{last} ({len(batch)} in batch)...")
        conversations = [make_conversation(img) for _, img in batch]
        try:
            outputs = llm.chat(conversations, sampling_params=sampling, use_tqdm=False)
            for (pg_num, _), out in zip(batch, outputs):
                results[pg_num] = out.outputs[0].text.strip()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(f"    [WARN] Batch {first}–{last} failed: {exc}")

    if not results:
        return False

    # Write output:
    #   full_book_repair=True  → overwrite the sparse bulk-lane file with a fresh document
    #   full_book_repair=False → append a clearly labelled repair section
    mode = "w" if full_book_repair else "a"
    with open(md_path, mode, encoding="utf-8") as f:
        if not full_book_repair:
            f.write("\n\n---\n## LANE C: PIXTRAL VLM REPAIR\n---\n\n")
        for pg_num in sorted(results):
            f.write(f"\n### Page {pg_num + 1}\n\n{results[pg_num]}\n")

    print(f"  [DONE] {len(results)}/{len(page_images)} pages written -> {md_path.name}")
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if not QUEUE_FILE.exists():
        print("Repair queue empty. Pipeline clear.")
        return

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue: dict = json.load(f)

    if not queue:
        print("Repair queue empty. Pipeline clear.")
        return

    total_pages = sum(len(v.get("failed_pages", [])) for v in queue.values())
    print(f"Loading {MODEL_NAME}  ({len(queue)} book(s), {total_pages} page(s))...")

    llm = LLM(
        model=MODEL_NAME,
        tokenizer_mode="mistral",
        limit_mm_per_prompt={"image": 1},
        max_model_len=16384,
        gpu_memory_utilization=0.85,
        enforce_eager=True,
    )

    for book_id, record in list(queue.items()):
        print(f"\n[BOOK] {Path(record.get('file', book_id)).name}  "
              f"({len(record.get('failed_pages', []))} pages, "
              f"{'full' if record.get('full_book_repair') else 'partial'} repair)")
        success = repair_book(llm, record)
        if success:
            del queue[book_id]
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)

    remaining = sum(1 for _ in queue)
    if remaining:
        print(f"\n[SUMMARY] {remaining} book(s) still in queue (check logs).")
    else:
        print("\n[SUMMARY] All repairs complete. Queue cleared.")


if __name__ == "__main__":
    main()
