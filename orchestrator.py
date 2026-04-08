#!/usr/bin/env python3
"""
Aether Forge (v10) — Master Orchestrator (Lanes A, B, B2)
"""

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import fitz  # PyMuPDF

INPUT_DIR = Path(os.getenv("INPUT_DIR", "/workspace/ttrpg_input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/workspace/ttrpg_output"))
REPAIR_QUEUE_FILE = OUTPUT_DIR / "repair_queue" / "queue.json"
LOG_DIR = OUTPUT_DIR / "logs"

_REPO = Path(__file__).parent
MARKER_PYTHON = os.getenv("MARKER_PYTHON", "/workspace/venvs/marker/bin/python3")
DOCLING_PYTHON = os.getenv("DOCLING_PYTHON", "/workspace/venvs/docling/bin/python3")
OCRMYPDF_BIN = os.getenv("OCRMYPDF_BIN", "/workspace/venvs/orchestrator/bin/ocrmypdf")
MARKER_RUNNER = _REPO / "marker_runner.py"
DOCLING_RUNNER = _REPO / "docling_runner.py"

MIN_CHARS_FOR_NATIVE = int(os.getenv("MIN_CHARS_FOR_NATIVE", "1000"))
WEIRD_CHAR_LIMIT = float(os.getenv("WEIRD_CHAR_LIMIT", "0.03"))
SCAN_THRESHOLD = int(os.getenv("SCAN_THRESHOLD", "50"))
MIN_MD_CHARS_PER_PAGE = int(os.getenv("MIN_MD_CHARS_PER_PAGE", "150"))

# A6000 production defaults — conservative for 1,876-book unattended run.
# Two parallel workers consume ~20-24 GB peak, leaving 24 GB headroom.
# Raise NUM_CHUNKS/BATCH_MULTIPLIER after validating GPU stability on a bakeoff.
BATCH_MULTIPLIER = int(os.getenv("BATCH_MULTIPLIER", "2"))   # was 4 during dev
CHUNK_THRESHOLD = int(os.getenv("CHUNK_THRESHOLD", "100"))   # was 150 during dev
NUM_CHUNKS = int(os.getenv("NUM_CHUNKS", "2"))               # was 3 during dev


def _log(log_file: Path, label: str, stdout: str, stderr: str) -> None:
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"\n[{label}]\n")
        if stdout:
            file.write(stdout)
        if stderr:
            file.write(f"\n[stderr]\n{stderr}")


def analyze_pdf(pdf_path: Path) -> tuple[float, float, int]:
    with fitz.open(pdf_path) as doc:
        total_pages = len(doc)
        total_chars = 0
        weird_chars = 0
        for page in doc:
            text = page.get_text("text").replace("\x00", "")
            total_chars += len(text)
            weird_chars += len(re.findall(r"[^A-Za-z0-9\s.,?!;:()'\"\\-]", text))
    avg_chars = total_chars / max(1, total_pages)
    weird_ratio = weird_chars / max(1, total_chars)
    return avg_chars, weird_ratio, total_pages


def audit_markdown(md_path: Path | None, total_pages: int) -> list[int]:
    """
    Granular structural audit.  Returns list(range(total_pages)) on any failure
    so Lane C always receives a clean full-book repair job — partial patch-in-
    place is unsafe at corpus scale due to alignment fragility without page markers.

    Checks (in order of cheapness):
      1. Whole-book density gate            — catastrophic total failure
      2. [EMPTY] span frequency             — Marker generation failures
      3. Malformed markdown tables          — pipe rows without --- dividers
      4. Control character / mojibake count — encoding corruption
    """
    if md_path is None or not md_path.exists():
        return list(range(total_pages))

    content = md_path.read_text(encoding="utf-8", errors="replace")

    # 1. Whole-book density gate
    if len(content) / max(1, total_pages) < MIN_MD_CHARS_PER_PAGE:
        print("  -> [AUDIT] Density too low — full-book failure")
        return list(range(total_pages))

    failure_signatures: list[str] = []

    # 2. [EMPTY] span frequency (>10 % of page count)
    empty_count = len(re.findall(r"\[EMPTY\]", content, re.IGNORECASE))
    if empty_count > total_pages * 0.10:
        failure_signatures.append(f"high_empty_spans({empty_count})")

    # 3. Malformed markdown tables — pipes exist but no valid header dividers
    table_lines = [ln for ln in content.split("\n") if "|" in ln]
    valid_dividers = [ln for ln in table_lines if re.search(r"\|[-:]+\|", ln)]
    if len(table_lines) > 20 and not valid_dividers:
        failure_signatures.append("corrupted_tables")

    # 4. Control character / mojibake (C0 range, excluding \t \n \r)
    weird_char_count = len(re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", content))
    if weird_char_count > 50:
        failure_signatures.append(f"encoding_corruption({weird_char_count})")

    if failure_signatures:
        print(f"  -> [AUDIT FAIL] Signatures: {', '.join(failure_signatures)}")
        return list(range(total_pages))

    return []


def locate_markdown(directory: Path, stem: str) -> Path | None:
    primary = directory / f"{stem}.md"
    if primary.exists():
        return primary
    candidates = sorted(directory.rglob("*.md"))
    return candidates[0] if candidates else None


def split_pdf(pdf: Path, out_dir: Path, num_chunks: int, total_pages: int) -> list[tuple[Path, int]]:
    chunk_size = (total_pages + num_chunks - 1) // num_chunks
    chunks: list[tuple[Path, int]] = []
    with fitz.open(pdf) as src:
        for idx in range(num_chunks):
            start = idx * chunk_size
            if start >= total_pages:
                break
            end = min(start + chunk_size - 1, total_pages - 1)
            chunk_path = out_dir / f"_chunk_{idx:02d}.pdf"
            with fitz.open() as dst:
                dst.insert_pdf(src, from_page=start, to_page=end)
                dst.save(str(chunk_path))
            chunks.append((chunk_path, idx))
    return chunks


def _marker_cmd(pdf: Path, out_dir: Path) -> list[str]:
    return [
        MARKER_PYTHON,
        str(MARKER_RUNNER),
        str(pdf),
        "--output_dir",
        str(out_dir),
        "--batch_multiplier",
        str(BATCH_MULTIPLIER),
    ]


def run_marker_single(pdf: Path, out_dir: Path, log_file: Path) -> Path:
    result = subprocess.run(_marker_cmd(pdf, out_dir), capture_output=True, text=True)
    _log(log_file, f"marker:{pdf.name}", result.stdout, result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"marker_runner exit {result.returncode}: {result.stderr[:300]}")
    md = locate_markdown(out_dir, pdf.stem)
    if md is None:
        raise RuntimeError("marker_runner produced no .md output")
    return md


def run_marker_chunked(pdf: Path, out_dir: Path, total_pages: int, log_file: Path) -> Path:
    chunks = split_pdf(pdf, out_dir, NUM_CHUNKS, total_pages)
    procs: list[tuple[subprocess.Popen, Path, int]] = []

    for chunk_pdf, idx in chunks:
        chunk_out = out_dir / f"_chunk_{idx:02d}_out"
        chunk_out.mkdir(exist_ok=True)
        process = subprocess.Popen(
            _marker_cmd(chunk_pdf, chunk_out),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        procs.append((process, chunk_out, idx))

    texts: dict[int, str] = {}
    for process, chunk_out, idx in procs:
        stdout, stderr = process.communicate()
        _log(log_file, f"marker:chunk_{idx}", stdout, stderr)
        if process.returncode != 0:
            raise RuntimeError(f"chunk {idx} exit {process.returncode}: {stderr[:200]}")
        md = locate_markdown(chunk_out, f"_chunk_{idx:02d}")
        if md:
            texts[idx] = md.read_text(encoding="utf-8")

    if not texts:
        raise RuntimeError("all Marker chunks produced no output")

    combined = "\n\n".join(texts[idx] for idx in sorted(texts))
    out_md = out_dir / f"{pdf.stem}.md"
    out_md.write_text(combined, encoding="utf-8")

    for chunk_pdf, idx in chunks:
        chunk_pdf.unlink(missing_ok=True)
        shutil.rmtree(out_dir / f"_chunk_{idx:02d}_out", ignore_errors=True)

    return out_md


def run_marker(pdf: Path, out_dir: Path, total_pages: int, log_file: Path) -> Path:
    if total_pages > CHUNK_THRESHOLD:
        print(f"  -> [LANE B] Chunked Marker ({NUM_CHUNKS} workers, {total_pages} pages)")
        return run_marker_chunked(pdf, out_dir, total_pages, log_file)
    print(f"  -> [LANE B] Single-pass Marker ({total_pages} pages)")
    return run_marker_single(pdf, out_dir, log_file)


def run_docling(pdf: Path, out_dir: Path, log_file: Path) -> Path:
    cmd = [DOCLING_PYTHON, str(DOCLING_RUNNER), str(pdf), "--output_dir", str(out_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    _log(log_file, f"docling:{pdf.name}", result.stdout, result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"docling_runner exit {result.returncode}: {result.stderr[:300]}")
    md = locate_markdown(out_dir, pdf.stem)
    if md is None:
        raise RuntimeError("docling_runner produced no .md output")
    return md


def process_book(pdf: Path, repair_queue: dict) -> None:
    print(f"\n[PREFLIGHT] {pdf.name}")
    avg_chars, weird_ratio, total_pages = analyze_pdf(pdf)
    print(f"            avg_chars={avg_chars:.0f} weird_ratio={weird_ratio:.3f} pages={total_pages}")

    out_dir = OUTPUT_DIR / pdf.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{pdf.stem}.log"
    md_out = out_dir / f"{pdf.stem}.md"

    if avg_chars > MIN_CHARS_FOR_NATIVE and weird_ratio < WEIRD_CHAR_LIMIT:
        print("  -> [LANE A] Native extraction (PyMuPDF)")
        with fitz.open(pdf) as doc, open(md_out, "w", encoding="utf-8") as file:
            for page in doc:
                file.write(page.get_text("text") + "\n\n")
        return

    active_pdf = pdf
    if avg_chars < SCAN_THRESHOLD:
        print("  -> [PREPROCESS] OCRmyPDF")
        optimized = out_dir / f"{pdf.stem}_optimized.pdf"
        try:
            result = subprocess.run(
                [OCRMYPDF_BIN, "--optimize", "1", "--force-ocr", str(pdf), str(optimized)],
                capture_output=True,
                text=True,
                check=True,
            )
            _log(log_file, "ocrmypdf", result.stdout, result.stderr)
            if optimized.exists():
                active_pdf = optimized
        except subprocess.CalledProcessError as exc:
            _log(log_file, "ocrmypdf:error", exc.stdout or "", exc.stderr or "")
            print(f"  ! [PREPROCESS] OCRmyPDF failed (exit {exc.returncode}); using original")

    failed_pages: list[int] = list(range(total_pages))
    try:
        marker_md = run_marker(active_pdf, out_dir, total_pages, log_file)
        failed_pages = audit_markdown(marker_md, total_pages)
        if not failed_pages:
            print("  -> [AUDIT] Marker passed")
            return
    except RuntimeError as exc:
        print(f"  ! [LANE B] {exc}")

    if len(failed_pages) == total_pages:
        print("  -> [LANE B2] Docling fallback")
        try:
            docling_md = run_docling(active_pdf, out_dir, log_file)
            failed_pages = audit_markdown(docling_md, total_pages)
            if not failed_pages:
                print("  -> [AUDIT] Docling passed")
                return
        except RuntimeError as exc:
            print(f"  ! [LANE B2] {exc}")

    # Always route as full_book_repair=True.  Partial patch-in-place requires
    # page-level markers that Marker does not emit; fuzzy insertion at corpus
    # scale will corrupt adjacent lore/mechanics text.  Pixtral re-renders the
    # entire book from scratch, guaranteeing a clean continuous document.
    print(f"  -> [ROUTE] Full-book repair: {len(failed_pages)} pages -> surgeon")
    repair_queue[str(active_pdf)] = {
        "file": str(active_pdf),
        "failed_pages": list(range(total_pages)),
        "md_path": str(md_out),
        "full_book_repair": True,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "repair_queue").mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if REPAIR_QUEUE_FILE.exists():
        with open(REPAIR_QUEUE_FILE, "r", encoding="utf-8") as file:
            repair_queue = json.load(file)
    else:
        repair_queue = {}

    for pdf in sorted(INPUT_DIR.glob("*.pdf")):
        process_book(pdf, repair_queue)
        with open(REPAIR_QUEUE_FILE, "w", encoding="utf-8") as file:
            json.dump(repair_queue, file, indent=2)


if __name__ == "__main__":
    main()
