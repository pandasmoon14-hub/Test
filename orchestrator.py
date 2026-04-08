"""
Aether Forge (v10) - Master Orchestrator
Lanes A & B: Preflight routing, bulk conversion, quality audit, repair queuing.

Run in the orchestrator environment:
    /workspace/venvs/orchestrator/bin/python3 /workspace/orchestrator.py

Environment variables:
    INPUT_DIR   - Directory containing input PDFs  (default: /workspace/ttrpg_input)
    OUTPUT_DIR  - Root output directory            (default: /workspace/ttrpg_output)
"""

import os
import json
import re
import subprocess
import sys
from pathlib import Path

import fitz  # PyMuPDF

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_DIR = Path(os.getenv("INPUT_DIR", "/workspace/ttrpg_input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/workspace/ttrpg_output"))
REPAIR_QUEUE_FILE = OUTPUT_DIR / "repair_queue" / "queue.json"

# Absolute paths into isolated venvs — no PATH manipulation needed.
ENV_MARKER   = "/workspace/venvs/marker/bin/marker_single"
ENV_DOCLING  = "/workspace/venvs/docling/bin/docling"
ENV_OCRMYPDF = "/workspace/venvs/orchestrator/bin/ocrmypdf"

# ---------------------------------------------------------------------------
# Routing thresholds
# ---------------------------------------------------------------------------
# Lane A (native fast path): born-digital text with strong embedded chars.
MIN_CHARS_FOR_NATIVE = 1000   # avg chars/page required to skip bulk OCR
WEIRD_CHAR_LIMIT     = 0.03   # fraction of non-ASCII/punctuation before we distrust native text

# Pre-processing trigger: raw image scans have almost no embedded text.
SCAN_THRESHOLD = 50           # avg chars/page below this → run OCRmyPDF first

# Quality audit: markdown output this sparse means conversion failed.
MIN_MD_CHARS_PER_PAGE = 150   # chars/page in output markdown to be considered "passing"


# ---------------------------------------------------------------------------
# Step 1: PDF Analysis / Preflight
# ---------------------------------------------------------------------------

def analyze_pdf(pdf_path: Path) -> tuple[float, float, int]:
    """
    Return (avg_chars_per_page, weird_char_ratio, total_pages).

    avg_chars_per_page  — proxy for native text richness
    weird_char_ratio    — fraction of chars outside standard ASCII range;
                          high values indicate garbled/encoded text
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    total_chars = 0
    weird_chars = 0

    for page in doc:
        text = page.get_text("text").replace("\x00", "")
        total_chars += len(text)
        # Count characters outside normal prose + punctuation
        weird_chars += len(re.findall(r"[^A-Za-z0-9\s.,?!;:()'\"@#$%&\-_+=/\\|<>\[\]{}]", text))

    doc.close()

    avg_chars    = total_chars / max(1, total_pages)
    weird_ratio  = weird_chars / max(1, total_chars)
    return avg_chars, weird_ratio, total_pages


# ---------------------------------------------------------------------------
# Step 2: Quality Audit
# ---------------------------------------------------------------------------

def audit_markdown(md_path: Path, total_pages: int) -> list[int]:
    """
    Return a list of zero-indexed page numbers that appear to have failed.

    Heuristic: if the entire markdown file is below the per-page density
    threshold we treat every page as failed and route the whole book to the
    next lane.  A future version can map markdown sections back to individual
    PDF page numbers for finer-grained routing.
    """
    if not md_path.exists():
        return list(range(total_pages))

    with open(md_path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    density = len(content) / max(1, total_pages)
    if density < MIN_MD_CHARS_PER_PAGE:
        return list(range(total_pages))

    # Output density is acceptable; treat as a full pass.
    return []


# ---------------------------------------------------------------------------
# Lane A: Native text extraction (PyMuPDF direct)
# ---------------------------------------------------------------------------

def lane_a_native(pdf: Path, md_out: Path) -> None:
    """Extract embedded text directly with PyMuPDF. Fast, zero GPU."""
    doc = fitz.open(pdf)
    with open(md_out, "w", encoding="utf-8") as fh:
        for page in doc:
            fh.write(page.get_text("text") + "\n\n")
    doc.close()


# ---------------------------------------------------------------------------
# Pre-processing: OCRmyPDF scan normalization
# ---------------------------------------------------------------------------

def preprocess_scan(pdf: Path, out_dir: Path) -> Path:
    """
    Run OCRmyPDF to embed a searchable text layer into raw image scans.
    Returns the path to the optimized PDF, or the original if the run fails.
    """
    optimized = out_dir / f"{pdf.stem}_optimized.pdf"
    result = subprocess.run(
        [ENV_OCRMYPDF, "--optimize", "1", "--force-ocr", str(pdf), str(optimized)],
        capture_output=True,
    )
    if result.returncode == 0 and optimized.exists():
        print(f"      [PRE-PROCESS] OCRmyPDF succeeded → {optimized.name}")
        return optimized
    else:
        print(f"      [PRE-PROCESS] OCRmyPDF returned {result.returncode}; continuing with original.")
        return pdf


# ---------------------------------------------------------------------------
# Lane B: Marker bulk conversion (primary)
# ---------------------------------------------------------------------------

def lane_b_marker(pdf: Path, output_dir: Path, md_out: Path, total_pages: int) -> list[int]:
    """
    Run Marker on `pdf`.  Marker writes output under `output_dir/<stem>/`.
    Returns failed page list from audit.
    """
    result = subprocess.run(
        [ENV_MARKER, str(pdf), "--output_dir", str(output_dir)],
        capture_output=True,
    )
    if result.returncode != 0:
        err = result.stderr.decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Marker exited {result.returncode}: {err}")

    # Marker writes the markdown to <output_dir>/<pdf_stem>/<pdf_stem>.md
    marker_md = output_dir / pdf.stem / f"{pdf.stem}.md"
    if not marker_md.exists():
        # Fallback: search for any .md in the expected subdir
        candidates = list((output_dir / pdf.stem).glob("*.md"))
        if candidates:
            marker_md = candidates[0]
        else:
            raise RuntimeError("Marker produced no .md output file.")

    # Ensure md_out points at the correct location for downstream stages
    if marker_md != md_out:
        md_out.write_bytes(marker_md.read_bytes())

    return audit_markdown(md_out, total_pages)


# ---------------------------------------------------------------------------
# Lane B2: Docling fallback (secondary bulk)
# ---------------------------------------------------------------------------

def lane_b2_docling(pdf: Path, out_dir: Path, total_pages: int) -> tuple[Path | None, list[int]]:
    """
    Run Docling on `pdf`.  Returns (md_path, failed_pages).
    Raises RuntimeError if Docling itself fails.
    """
    result = subprocess.run(
        [ENV_DOCLING, str(pdf), "--to", "md", "--output", str(out_dir)],
        capture_output=True,
    )
    if result.returncode != 0:
        err = result.stderr.decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Docling exited {result.returncode}: {err}")

    docling_md = out_dir / f"{pdf.stem}.md"
    if not docling_md.exists():
        candidates = list(out_dir.glob("*.md"))
        if candidates:
            docling_md = candidates[0]
        else:
            raise RuntimeError("Docling produced no .md output file.")

    return docling_md, audit_markdown(docling_md, total_pages)


# ---------------------------------------------------------------------------
# Main per-book routing logic
# ---------------------------------------------------------------------------

def process_book(pdf: Path, repair_queue: dict) -> None:
    print(f"\n[PREFLIGHT] {pdf.name}")
    avg_chars, weird_ratio, total_pages = analyze_pdf(pdf)
    print(f"            avg_chars/page={avg_chars:.0f}  weird_ratio={weird_ratio:.3f}  pages={total_pages}")

    out_dir = OUTPUT_DIR / pdf.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    md_out = out_dir / f"{pdf.stem}.md"

    # ------------------------------------------------------------------
    # LANE A: born-digital fast path
    # ------------------------------------------------------------------
    if avg_chars > MIN_CHARS_FOR_NATIVE and weird_ratio < WEIRD_CHAR_LIMIT:
        print(f"  -> [LANE A] Native text is clean. Extracting with PyMuPDF...")
        lane_a_native(pdf, md_out)
        print(f"  -> [DONE]   {md_out.name} written ({md_out.stat().st_size:,} bytes).")
        return

    # ------------------------------------------------------------------
    # PRE-PROCESSING: embed OCR text layer into raw image scans
    # ------------------------------------------------------------------
    active_pdf = pdf
    if avg_chars < SCAN_THRESHOLD:
        print(f"  -> [PRE-PROCESS] Raw image scan detected (avg_chars={avg_chars:.0f}).")
        active_pdf = preprocess_scan(pdf, out_dir)

    # ------------------------------------------------------------------
    # LANE B: Marker (primary bulk)
    # ------------------------------------------------------------------
    print(f"  -> [LANE B] Running Marker on {active_pdf.name}...")
    marker_failed = list(range(total_pages))   # pessimistic default
    try:
        marker_failed = lane_b_marker(active_pdf, OUTPUT_DIR, md_out, total_pages)
        if not marker_failed:
            print(f"  -> [AUDIT]  Marker passed. Archive sealed ({md_out.name}).")
            return
        else:
            print(f"  -> [AUDIT]  Marker output thin ({len(marker_failed)} pages below threshold).")
    except RuntimeError as exc:
        print(f"  ! [LANE B]  Marker error: {exc}")

    # ------------------------------------------------------------------
    # LANE B2: Docling fallback (only if all pages failed or Marker errored)
    # ------------------------------------------------------------------
    if len(marker_failed) == total_pages:
        print(f"  -> [LANE B2] Trying Docling as fallback...")
        try:
            docling_md, docling_failed = lane_b2_docling(active_pdf, out_dir, total_pages)
            if not docling_failed:
                # Promote Docling output to the canonical md_out path if needed
                if docling_md != md_out:
                    md_out.write_bytes(docling_md.read_bytes())
                print(f"  -> [AUDIT]  Docling recovery succeeded. Archive sealed.")
                return
            else:
                print(f"  -> [AUDIT]  Docling output thin ({len(docling_failed)} pages below threshold).")
                marker_failed = docling_failed   # use the more refined list
        except RuntimeError as exc:
            print(f"  ! [LANE B2] Docling error: {exc}")

    # ------------------------------------------------------------------
    # LANE C: Route to Pixtral VLM repair
    # ------------------------------------------------------------------
    print(f"  -> [QUEUE]  {len(marker_failed)} pages routed to Pixtral surgeon.")
    repair_queue[str(active_pdf)] = {
        "original_pdf": str(pdf),
        "failed_pages": marker_failed,
        "md_path": str(md_out),
        "total_pages": total_pages,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if not INPUT_DIR.exists():
        print(f"[ERROR] Input directory not found: {INPUT_DIR}")
        sys.exit(1)

    pdfs = sorted(INPUT_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"[INFO]  No PDFs found in {INPUT_DIR}. Nothing to do.")
        return

    # Load existing repair queue so we can resume interrupted runs.
    if REPAIR_QUEUE_FILE.exists():
        with open(REPAIR_QUEUE_FILE, "r") as fh:
            repair_queue = json.load(fh)
        print(f"[INFO]  Loaded existing repair queue ({len(repair_queue)} entries).")
    else:
        repair_queue = {}

    print(f"[INFO]  Processing {len(pdfs)} PDF(s) from {INPUT_DIR}\n")

    for pdf in pdfs:
        process_book(pdf, repair_queue)
        # Checkpoint after every book so a crash doesn't lose progress.
        REPAIR_QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REPAIR_QUEUE_FILE, "w") as fh:
            json.dump(repair_queue, fh, indent=2)

    if repair_queue:
        print(f"\n[SUMMARY] {len(repair_queue)} book(s) queued for Pixtral repair.")
        print(f"          Run surgeon.py next:  /workspace/venvs/pixtral/bin/python3 /workspace/surgeon.py")
    else:
        print(f"\n[SUMMARY] All books extracted cleanly. No repair pass needed.")


if __name__ == "__main__":
    main()
