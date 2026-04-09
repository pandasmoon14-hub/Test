#!/usr/bin/env python3
"""
Aether Forge orchestrator (v11)

Key upgrades over v10:
- scored routing classifier (not binary threshold)
- adaptive page sampling with layout hotspots
- page-level audit and per-page failure reasons
- reading-order/header-footer/soft-hyphen/table/stat-block audits
- chunk completeness checks + subprocess timeouts + retries
- selective OCR policy and mode variants
- page markers + per-page metadata manifest
- sample-and-race lane chooser (optional)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import fitz

try:
    from sqlite_queue import QueueDB, queue_item_from_record
except Exception:  # pylint: disable=broad-exception-caught
    QueueDB = None
    queue_item_from_record = None


@dataclass
class RuntimeConfig:
    input_dir: Path
    output_dir: Path
    repair_queue_file: Path
    log_dir: Path
    manifests_dir: Path
    table_sidecar_dir: Path

    marker_python: str
    docling_python: str
    ocrmypdf_bin: str
    marker_runner: Path
    docling_runner: Path

    min_chars_for_native: int = 1000
    weird_char_limit: float = 0.06
    scan_threshold: int = 50
    min_md_chars_per_page: int = 130

    batch_multiplier: int = 2
    chunk_threshold: int = 120
    min_chunk_pages: int = 40
    max_chunk_pages: int = 180

    sample_budget: int = 60
    sample_interval_pages: int = 7

    enforce_full_book_repair: bool = False
    continue_on_error: bool = True
    overwrite_existing: bool = False

    bridge_timeout_sec: int = 3600
    bridge_retries: int = 2

    ocr_mode: str = "selective"
    min_free_disk_gb: int = 5

    sample_and_race: bool = False
    sample_race_pages: int = 8
    use_sqlite_queue: bool = False
    sqlite_queue_path: Path | None = None
    strict_page_truth: bool = False

    @classmethod
    def from_env(cls, repo_root: Path) -> "RuntimeConfig":
        output_dir = Path(os.getenv("OUTPUT_DIR", "/workspace/ttrpg_output"))
        return cls(
            input_dir=Path(os.getenv("INPUT_DIR", "/workspace/ttrpg_input")),
            output_dir=output_dir,
            repair_queue_file=output_dir / "repair_queue" / "queue.json",
            log_dir=output_dir / "logs",
            manifests_dir=output_dir / "manifests",
            table_sidecar_dir=output_dir / "table_sidecars",
            marker_python=os.getenv("MARKER_PYTHON", "/workspace/venvs/marker/bin/python3"),
            docling_python=os.getenv("DOCLING_PYTHON", "/workspace/venvs/docling/bin/python3"),
            ocrmypdf_bin=os.getenv("OCRMYPDF_BIN", "/workspace/venvs/orchestrator/bin/ocrmypdf"),
            marker_runner=repo_root / "marker_runner.py",
            docling_runner=repo_root / "docling_runner.py",
            min_chars_for_native=int(os.getenv("MIN_CHARS_FOR_NATIVE", "1000")),
            weird_char_limit=float(os.getenv("WEIRD_CHAR_LIMIT", "0.06")),
            scan_threshold=int(os.getenv("SCAN_THRESHOLD", "50")),
            min_md_chars_per_page=int(os.getenv("MIN_MD_CHARS_PER_PAGE", "130")),
            batch_multiplier=int(os.getenv("BATCH_MULTIPLIER", "2")),
            chunk_threshold=int(os.getenv("CHUNK_THRESHOLD", "120")),
            min_chunk_pages=int(os.getenv("MIN_CHUNK_PAGES", "40")),
            max_chunk_pages=int(os.getenv("MAX_CHUNK_PAGES", "180")),
            sample_budget=int(os.getenv("SAMPLE_BUDGET", "60")),
            sample_interval_pages=int(os.getenv("SAMPLE_INTERVAL_PAGES", "7")),
            enforce_full_book_repair=(os.getenv("ENFORCE_FULL_BOOK_REPAIR", "0") == "1"),
            continue_on_error=(os.getenv("CONTINUE_ON_ERROR", "1") == "1"),
            overwrite_existing=(os.getenv("OVERWRITE_EXISTING", "0") == "1"),
            bridge_timeout_sec=int(os.getenv("BRIDGE_TIMEOUT_SEC", "3600")),
            bridge_retries=int(os.getenv("BRIDGE_RETRIES", "2")),
            ocr_mode=os.getenv("OCR_MODE", "selective"),
            min_free_disk_gb=int(os.getenv("MIN_FREE_DISK_GB", "5")),
            sample_and_race=(os.getenv("SAMPLE_AND_RACE", "0") == "1"),
            sample_race_pages=int(os.getenv("SAMPLE_RACE_PAGES", "8")),
            use_sqlite_queue=(os.getenv("USE_SQLITE_QUEUE", "0") == "1"),
            sqlite_queue_path=Path(os.getenv("SQLITE_QUEUE_PATH", str(output_dir / "repair_queue" / "queue.db"))),
            strict_page_truth=(os.getenv("STRICT_PAGE_TRUTH", "0") == "1"),
        )


@dataclass
class PageFeatures:
    page_index: int
    char_count: int
    weird_ratio: float
    block_count: int
    image_coverage: float
    vector_text_ratio: float
    is_multicolumn: bool
    table_density: float
    sidebar_density: float
    statblock_density: float


@dataclass
class PdfProfile:
    total_pages: int
    average_chars_per_page: float
    weird_ratio: float
    scanned_ratio: float
    multicolumn_ratio: float
    table_page_ratio: float
    sidebar_page_ratio: float
    statblock_page_ratio: float
    image_dominant_ratio: float
    donor_family: str
    samples: list[int]
    page_features: list[PageFeatures]


@dataclass
class PageAudit:
    page_index: int
    passed: bool
    reasons: list[str] = field(default_factory=list)
    chars: int = 0
    table_score: float = 0.0


@dataclass
class AuditResult:
    passed: bool
    failed_pages: list[int]
    page_audits: list[PageAudit]
    signatures: list[str]


@dataclass
class BookManifest:
    book_id: str
    source_pdf: str
    lane: str
    lane_scores: dict[str, float]
    donor_family: str
    page_count: int
    total_pages: int
    pages_audited: int
    pages_passed: int
    pages_remaining: int
    page_marker_mode: str
    chunk_count: int
    ocr_mode: str
    started_at: str
    finished_at: str
    elapsed_sec: float
    output_md: str
    page_metadata_path: str
    audit_signatures: list[str]
    failed_pages: list[int]
    marker_api_variant: str | None = None


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def ensure_dirs(cfg: RuntimeConfig) -> None:
    for path in [cfg.output_dir, cfg.output_dir / "repair_queue", cfg.output_dir / "failed_queue", cfg.log_dir, cfg.manifests_dir, cfg.table_sidecar_dir]:
        path.mkdir(parents=True, exist_ok=True)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def check_disk_space(cfg: RuntimeConfig) -> None:
    usage = shutil.disk_usage(cfg.output_dir)
    free_gb = usage.free / (1024**3)
    if free_gb < cfg.min_free_disk_gb:
        raise RuntimeError(f"Insufficient disk space: {free_gb:.2f} GB < {cfg.min_free_disk_gb} GB")


def verify_pdf_magic(pdf: Path) -> bool:
    try:
        with open(pdf, "rb") as file:
            return file.read(5) == b"%PDF-"
    except OSError:
        return False


def choose_donor_family(pdf: Path, doc: fitz.Document) -> str:
    meta = doc.metadata or {}
    text = " ".join(filter(None, [meta.get("producer", ""), meta.get("creator", ""), pdf.name]))
    low = text.lower()
    if any(k in low for k in ["adobe indesign", "wizards", "d&d", "forgotten realms"]):
        return "dnd5e"
    if any(k in low for k in ["ogl", "pathfinder", "paizo"]):
        return "ogl"
    return "mixed"


def normalize_text(text: str) -> str:
    text = text.replace("\xad", "")
    text = text.replace("\ufeff", "")
    text = text.replace("\ufffd", "")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text


def detect_multicolumn(blocks: list[tuple]) -> bool:
    if len(blocks) < 8:
        return False
    xs = [b[0] for b in blocks if len(b) >= 4]
    if len(xs) < 8:
        return False
    xs = sorted(xs)
    mid = statistics.median(xs)
    left = [x for x in xs if x < mid]
    right = [x for x in xs if x >= mid]
    if len(left) < 3 or len(right) < 3:
        return False
    return (statistics.mean(right) - statistics.mean(left)) > 90


def detect_table_density(text: str) -> float:
    lines = text.splitlines()
    if not lines:
        return 0.0
    tableish = sum(1 for line in lines if line.count("|") >= 2 or re.search(r"\b\d+\s{2,}\d+\b", line))
    return tableish / len(lines)


def detect_sidebar_density(page: fitz.Page) -> float:
    drawings = page.get_drawings()
    rects = [d for d in drawings if d.get("rect")]
    if not rects:
        return 0.0
    narrow = 0
    for d in rects:
        rect = d["rect"]
        if rect.width < page.rect.width * 0.4 and rect.height > page.rect.height * 0.08:
            narrow += 1
    return min(1.0, narrow / max(1, len(rects)))


def detect_statblock_density(text: str) -> float:
    keys = ["armor class", "hit points", "speed", "saving throw", "spell slots", "challenge rating", "dc ", "initiative", "actions", "bonus action"]
    low = text.lower()
    hits = sum(1 for k in keys if k in low)
    return min(1.0, hits / 6.0)


def image_coverage(page: fitz.Page) -> float:
    imgs = page.get_images(full=True)
    return min(1.0, len(imgs) / 3.0) if imgs else 0.0


def vector_text_ratio(page: fitz.Page, text: str) -> float:
    chars = len(text)
    drawings = len(page.get_drawings())
    if chars == 0:
        return 0.0
    return min(1.0, chars / (chars + drawings * 40 + 1))


def adaptive_sample_pages(doc: fitz.Document, cfg: RuntimeConfig) -> list[int]:
    total = len(doc)
    if total <= 0:
        return []
    candidates = {0, total - 1}
    for i in range(0, total, max(1, cfg.sample_interval_pages)):
        candidates.add(i)
    for i in range(total):
        text = normalize_text(doc[i].get_text("text")[:2000]).lower()
        if any(k in text for k in ["table of contents", "appendix", "index", "spell", "monster", "stat block"]):
            candidates.add(i)
    samples = sorted(candidates)
    if len(samples) > cfg.sample_budget:
        stride = len(samples) / cfg.sample_budget
        reduced, idx = [], 0.0
        while int(idx) < len(samples) and len(reduced) < cfg.sample_budget:
            reduced.append(samples[int(idx)])
            idx += stride
        samples = sorted(set(reduced))
    return samples


def analyze_pdf(pdf: Path, cfg: RuntimeConfig) -> PdfProfile:
    with fitz.open(pdf) as doc:
        donor = choose_donor_family(pdf, doc)
        samples = adaptive_sample_pages(doc, cfg)
        rows: list[PageFeatures] = []
        for idx in samples:
            page = doc[idx]
            text = normalize_text(page.get_text("text"))
            blocks = page.get_text("blocks")
            weird = len(re.findall(r"[^\w\s\.,;:?!'\-()\[\]{}<>/|+=*&%$#@`~“”‘’…–—§°•†‡]", text))
            rows.append(PageFeatures(
                page_index=idx,
                char_count=len(text),
                weird_ratio=weird / max(1, len(text)),
                block_count=len(blocks),
                image_coverage=image_coverage(page),
                vector_text_ratio=vector_text_ratio(page, text),
                is_multicolumn=detect_multicolumn(blocks),
                table_density=detect_table_density(text),
                sidebar_density=detect_sidebar_density(page),
                statblock_density=detect_statblock_density(text),
            ))

    avg_chars = statistics.mean([r.char_count for r in rows]) if rows else 0.0
    weird_ratio = statistics.mean([r.weird_ratio for r in rows]) if rows else 0.0
    scanned_ratio = sum(1 for r in rows if r.char_count < cfg.scan_threshold) / max(1, len(rows))
    multicol_ratio = sum(1 for r in rows if r.is_multicolumn) / max(1, len(rows))
    table_ratio = sum(1 for r in rows if r.table_density > 0.15) / max(1, len(rows))
    sidebar_ratio = sum(1 for r in rows if r.sidebar_density > 0.2) / max(1, len(rows))
    stat_ratio = sum(1 for r in rows if r.statblock_density > 0.3) / max(1, len(rows))
    image_ratio = sum(1 for r in rows if r.image_coverage > 0.4) / max(1, len(rows))

    with fitz.open(pdf) as doc:
        total_pages = len(doc)

    return PdfProfile(total_pages, avg_chars, weird_ratio, scanned_ratio, multicol_ratio, table_ratio, sidebar_ratio, stat_ratio, image_ratio, donor, samples, rows)


def lane_scores(profile: PdfProfile, cfg: RuntimeConfig) -> dict[str, float]:
    a = (1.4 if profile.average_chars_per_page > cfg.min_chars_for_native else -1.0) + (1.2 if profile.weird_ratio < cfg.weird_char_limit else -1.0) - 1.3 * profile.multicolumn_ratio - 1.1 * profile.table_page_ratio - 0.8 * profile.sidebar_page_ratio - 0.8 * profile.statblock_page_ratio
    b = 1.5 * profile.table_page_ratio + 0.9 * profile.statblock_page_ratio + 0.7 * profile.multicolumn_ratio + (0.4 if profile.donor_family in {"dnd5e", "ogl"} else 0.2) - 0.7 * profile.scanned_ratio
    b2 = 1.2 * profile.table_page_ratio + 1.0 * profile.multicolumn_ratio + 0.6 * profile.sidebar_page_ratio + 0.8 * profile.scanned_ratio + (0.5 if profile.donor_family == "mixed" else 0.2)
    return {"A": round(a, 4), "B": round(b, 4), "B2": round(b2, 4)}


def choose_lane(profile: PdfProfile, cfg: RuntimeConfig) -> tuple[str, dict[str, float]]:
    scores = lane_scores(profile, cfg)
    return max(scores, key=scores.get), scores


def route_ocr_mode(profile: PdfProfile, cfg: RuntimeConfig) -> str:
    if cfg.ocr_mode in {"force", "skip", "redo"}:
        return cfg.ocr_mode
    if profile.scanned_ratio > 0.45:
        return "force"
    if profile.scanned_ratio > 0.15:
        return "redo"
    return "skip"


def write_page_markers_from_blocks(pdf: Path, out_md: Path, page_meta_path: Path) -> None:
    meta_rows = []
    with fitz.open(pdf) as doc, open(out_md, "w", encoding="utf-8") as out:
        header_footer_memory: dict[str, int] = {}
        for i, page in enumerate(doc):
            blocks = page.get_text("blocks")
            blocks_sorted = sorted(blocks, key=lambda b: (round(b[1], 1), round(b[0], 1)))
            lines = [normalize_text(b[4]) for b in blocks_sorted if len(b) > 4 and b[4].strip()]
            first = lines[0].strip() if lines else ""
            last = lines[-1].strip() if lines else ""
            for token in [first, last]:
                if token:
                    header_footer_memory[token] = header_footer_memory.get(token, 0) + 1
            out.write(f"\n<!-- PAGE:{i + 1} -->\n")
            cleaned = [line for line in lines if not (header_footer_memory.get(line.strip(), 0) > 3 and len(line.strip()) < 80)]
            out.write("\n".join(cleaned).strip() + "\n")
            meta_rows.append({"page": i + 1, "chars": sum(len(x) for x in cleaned), "blocks": len(blocks_sorted), "tables_detected": sum(1 for x in cleaned if x.count("|") >= 2), "lane": "A"})
    save_json(page_meta_path, meta_rows)


def bridge_call(cmd: list[str], timeout_sec: int, retries: int, log_file: Path, label: str) -> dict[str, Any]:
    last_err = ""
    for attempt in range(1, retries + 1):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
            with open(log_file, "a", encoding="utf-8") as file:
                file.write(f"\n[{label}:attempt_{attempt}]\n")
                file.write(result.stdout or "")
                if result.stderr:
                    file.write(f"\n[stderr]\n{result.stderr}\n")
            if result.returncode != 0:
                last_err = result.stderr[:500]
                continue
            payload = json.loads((result.stdout or "{}").strip().splitlines()[-1])
            if payload.get("status") != "ok" or not payload.get("md_path"):
                last_err = f"invalid payload: {payload}"
                continue
            return payload
        except subprocess.TimeoutExpired:
            last_err = f"timeout {timeout_sec}s"
        except json.JSONDecodeError as exc:
            last_err = f"json decode: {exc}"
    raise RuntimeError(f"bridge call failed [{label}] {last_err}")


def chunk_plan(total_pages: int, cfg: RuntimeConfig, complexity: float) -> int:
    if total_pages <= cfg.chunk_threshold:
        return 1
    target = int(cfg.max_chunk_pages - complexity * 100)
    target = max(cfg.min_chunk_pages, min(cfg.max_chunk_pages, target))
    return max(2, (total_pages + target - 1) // target)


def split_pdf(pdf: Path, out_dir: Path, n_chunks: int, total_pages: int) -> list[tuple[Path, tuple[int, int], int]]:
    size = (total_pages + n_chunks - 1) // n_chunks
    chunks = []
    with fitz.open(pdf) as src:
        for idx in range(n_chunks):
            start = idx * size
            if start >= total_pages:
                break
            end = min(total_pages - 1, start + size - 1)
            cp = out_dir / f"_chunk_{idx:02d}_{start+1}_{end+1}.pdf"
            with fitz.open() as dst:
                dst.insert_pdf(src, from_page=start, to_page=end)
                dst.save(cp)
            chunks.append((cp, (start, end), idx))
    return chunks


def load_page_map(path: Path, start: int, end: int, strict: bool) -> dict[int, str]:
    if not path.exists():
        if strict:
            raise RuntimeError(f"missing page_map_json: {path}")
        return {}
    rows = load_json(path, [])
    page_map: dict[int, str] = {}
    if not isinstance(rows, list):
        if strict:
            raise RuntimeError(f"invalid page_map_json format: {path}")
        return {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        source_page = row.get("source_page")
        markdown = normalize_text(str(row.get("markdown", ""))).strip()
        if not isinstance(source_page, int):
            continue
        abs_page = start + source_page - 1
        if start <= abs_page <= end:
            page_map[abs_page] = markdown
    return page_map


def write_page_map_markdown(out_md: Path, total_pages: int, page_map: dict[int, str]) -> None:
    with open(out_md, "w", encoding="utf-8") as file:
        for page_no in range(1, total_pages + 1):
            file.write(f"<!-- PAGE:{page_no} -->\n")
            file.write(page_map.get(page_no, "").strip() + "\n\n")


def run_marker(cfg: RuntimeConfig, pdf: Path, out_dir: Path, profile: PdfProfile, log_file: Path) -> tuple[Path, str | None, list[dict[str, Any]], str]:
    total_pages = profile.total_pages
    complexity = min(1.0, profile.table_page_ratio + profile.multicolumn_ratio + profile.sidebar_page_ratio)
    n_chunks = chunk_plan(total_pages, cfg, complexity)
    meta: list[dict[str, Any]] = []

    if n_chunks == 1:
        page_map_path = out_dir / f"{pdf.stem}.page_map.json"
        payload = bridge_call([cfg.marker_python, str(cfg.marker_runner), str(pdf), "--output_dir", str(out_dir), "--batch_multiplier", str(cfg.batch_multiplier), "--strict", "--page_map_json", str(page_map_path)], cfg.bridge_timeout_sec, cfg.bridge_retries, log_file, f"marker:{pdf.name}")
        page_map = load_page_map(Path(payload.get("page_map_path", page_map_path)), 1, total_pages, cfg.strict_page_truth)
        if page_map:
            out = out_dir / f"{pdf.stem}.md"
            write_page_map_markdown(out, total_pages, page_map)
            meta.append({"chunk": 0, "page_start": 1, "page_end": total_pages, "lane": "B", "page_map_path": str(page_map_path), "pages_emitted": len(page_map)})
            return out, payload.get("api_variant"), meta, "source_page_map"
        return Path(payload["md_path"]), payload.get("api_variant"), meta, "native_or_fallback"

    chunks = split_pdf(pdf, out_dir, n_chunks, total_pages)
    collected, api_variant = {}, None
    for cp, (start, end), idx in chunks:
        cout = out_dir / f"_chunk_{idx:02d}_out"
        cout.mkdir(parents=True, exist_ok=True)
        page_map_path = cout / f"{cp.stem}.page_map.json"
        payload = bridge_call([cfg.marker_python, str(cfg.marker_runner), str(cp), "--output_dir", str(cout), "--batch_multiplier", str(max(1, cfg.batch_multiplier - 1 if complexity > 0.8 else cfg.batch_multiplier)), "--strict", "--page_map_json", str(page_map_path)], cfg.bridge_timeout_sec, cfg.bridge_retries, log_file, f"marker:chunk_{idx}")
        api_variant = payload.get("api_variant") or api_variant
        md = Path(payload["md_path"])
        text = md.read_text(encoding="utf-8", errors="replace")
        if len(text.strip()) < 50:
            raise RuntimeError(f"empty chunk output {idx}")
        page_map = load_page_map(Path(payload.get("page_map_path", page_map_path)), start + 1, end + 1, cfg.strict_page_truth)
        collected[idx] = {"text": text, "pages": page_map}
        meta.append({"chunk": idx, "page_start": start + 1, "page_end": end + 1, "lane": "B", "page_map_path": str(page_map_path), "pages_emitted": len(page_map)})
    if len(collected) != len(chunks):
        raise RuntimeError("incomplete marker chunks")

    page_map: dict[int, str] = {}
    for _, (_, _), idx in chunks:
        page_map.update(collected[idx]["pages"])
    out = out_dir / f"{pdf.stem}.md"
    if page_map:
        write_page_map_markdown(out, total_pages, page_map)
        marker_mode = "source_page_map"
    else:
        if cfg.strict_page_truth:
            raise RuntimeError("strict_page_truth: missing marker page maps for chunked output")
        with open(out, "w", encoding="utf-8") as f:
            for _, (start, end), idx in chunks:
                f.write(f"\n<!-- CHUNK:{idx} PAGES:{start+1}-{end+1} -->\n{collected[idx]['text'].strip()}\n")
        marker_mode = "chunk_fallback"
    for cp, _, idx in chunks:
        cp.unlink(missing_ok=True)
        shutil.rmtree(out_dir / f"_chunk_{idx:02d}_out", ignore_errors=True)
    return out, api_variant, meta, marker_mode


def run_docling(cfg: RuntimeConfig, pdf: Path, out_dir: Path, profile: PdfProfile, log_file: Path) -> tuple[Path, list[dict[str, Any]], str]:
    complexity = min(1.0, profile.table_page_ratio + profile.multicolumn_ratio)
    n_chunks = chunk_plan(profile.total_pages, cfg, complexity)
    meta: list[dict[str, Any]] = []
    if n_chunks == 1:
        page_map_path = out_dir / f"{pdf.stem}.page_map.json"
        payload = bridge_call([cfg.docling_python, str(cfg.docling_runner), str(pdf), "--output_dir", str(out_dir), "--strict", "--page_map_json", str(page_map_path)], cfg.bridge_timeout_sec, cfg.bridge_retries, log_file, f"docling:{pdf.name}")
        page_map = load_page_map(Path(payload.get("page_map_path", page_map_path)), 1, profile.total_pages, cfg.strict_page_truth)
        if page_map:
            out = out_dir / f"{pdf.stem}.md"
            write_page_map_markdown(out, profile.total_pages, page_map)
            meta.append({"chunk": 0, "page_start": 1, "page_end": profile.total_pages, "lane": "B2", "page_map_path": str(page_map_path), "pages_emitted": len(page_map)})
            return out, meta, "source_page_map"
        return Path(payload["md_path"]), meta, "native_or_fallback"

    chunks = split_pdf(pdf, out_dir, n_chunks, profile.total_pages)
    collected = {}
    for cp, (start, end), idx in chunks:
        cout = out_dir / f"_dchunk_{idx:02d}_out"
        cout.mkdir(parents=True, exist_ok=True)
        page_map_path = cout / f"{cp.stem}.page_map.json"
        payload = bridge_call([cfg.docling_python, str(cfg.docling_runner), str(cp), "--output_dir", str(cout), "--strict", "--page_map_json", str(page_map_path)], cfg.bridge_timeout_sec, cfg.bridge_retries, log_file, f"docling:chunk_{idx}")
        text = Path(payload["md_path"]).read_text(encoding="utf-8", errors="replace")
        page_map = load_page_map(Path(payload.get("page_map_path", page_map_path)), start + 1, end + 1, cfg.strict_page_truth)
        collected[idx] = {"text": text, "pages": page_map}
        meta.append({"chunk": idx, "page_start": start + 1, "page_end": end + 1, "lane": "B2", "page_map_path": str(page_map_path), "pages_emitted": len(page_map)})
    if len(collected) != len(chunks):
        raise RuntimeError("incomplete docling chunks")
    out = out_dir / f"{pdf.stem}.md"
    page_map: dict[int, str] = {}
    for _, (_, _), idx in chunks:
        page_map.update(collected[idx]["pages"])
    if page_map:
        write_page_map_markdown(out, profile.total_pages, page_map)
        marker_mode = "source_page_map"
    else:
        if cfg.strict_page_truth:
            raise RuntimeError("strict_page_truth: missing docling page maps for chunked output")
        with open(out, "w", encoding="utf-8") as f:
            for _, (start, end), idx in chunks:
                f.write(f"\n<!-- CHUNK:{idx} PAGES:{start+1}-{end+1} -->\n{collected[idx]['text'].strip()}\n")
        marker_mode = "chunk_fallback"
    for cp, _, idx in chunks:
        cp.unlink(missing_ok=True)
        shutil.rmtree(out_dir / f"_dchunk_{idx:02d}_out", ignore_errors=True)
    return out, meta, marker_mode


def ensure_page_markers(content: str, total_pages: int) -> str:
    if "<!-- PAGE:" in content:
        return content
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]

    def render_marker_pages(page_numbers: list[int], source_paragraphs: list[str]) -> str:
        if not page_numbers:
            page_numbers = [1]
        buckets = {p: [] for p in page_numbers}
        if source_paragraphs:
            for idx, paragraph in enumerate(source_paragraphs):
                target_page = page_numbers[min(len(page_numbers) - 1, int(idx * len(page_numbers) / len(source_paragraphs)))]
                buckets[target_page].append(paragraph)
        lines: list[str] = []
        for page_no in page_numbers:
            lines.append(f"<!-- PAGE:{page_no} -->")
            body = "\n\n".join(buckets.get(page_no, []))
            if body:
                lines.append(body)
        return "\n".join(lines).strip() + "\n"

    if "<!-- CHUNK:" in content and total_pages > 1:
        chunk_re = re.compile(
            r"<!--\s*CHUNK:(\d+)\s+PAGES:(\d+)-(\d+)\s*-->\s*(.*?)(?=(?:\n<!--\s*CHUNK:\d+\s+PAGES:\d+-\d+\s*-->)|\Z)",
            flags=re.DOTALL,
        )
        pieces: list[str] = []
        seen_pages: set[int] = set()
        for m in chunk_re.finditer(content):
            start, end = int(m.group(2)), int(m.group(3))
            if end < start:
                continue
            page_numbers = [p for p in range(start, min(end, total_pages) + 1) if p >= 1]
            if not page_numbers:
                continue
            seen_pages.update(page_numbers)
            chunk_paragraphs = [p.strip() for p in re.split(r"\n\s*\n", m.group(4)) if p.strip()]
            pieces.append(render_marker_pages(page_numbers, chunk_paragraphs))
        if pieces:
            missing = [p for p in range(1, total_pages + 1) if p not in seen_pages]
            if missing:
                pieces.append(render_marker_pages(missing, []))
            return "\n".join(pieces).strip() + "\n"

    if total_pages <= 1:
        return "<!-- PAGE:1 -->\n" + content
    return render_marker_pages(list(range(1, total_pages + 1)), paragraphs)


def run_ocr(cfg: RuntimeConfig, input_pdf: Path, output_pdf: Path, mode: str, log_file: Path) -> Path:
    if mode == "skip":
        return input_pdf
    cmd = [cfg.ocrmypdf_bin]
    if mode == "redo":
        cmd.append("--redo-ocr")
    elif mode == "force":
        cmd.append("--force-ocr")
    cmd.extend(["--optimize", "1", str(input_pdf), str(output_pdf)])
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=cfg.bridge_timeout_sec)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[ocr:{mode}]\n{res.stdout}\n")
            if res.stderr:
                f.write(f"[stderr]\n{res.stderr}\n")
        if res.returncode == 0 and output_pdf.exists():
            return output_pdf
    except subprocess.TimeoutExpired:
        pass
    return input_pdf


def parse_page_markers(content: str) -> dict[int, str]:
    pages, cur = {}, 1
    for line in content.splitlines():
        m = re.match(r"\s*<!--\s*PAGE:(\d+)\s*-->", line)
        if m:
            cur = int(m.group(1))
            pages.setdefault(cur, [])
            continue
        pages.setdefault(cur, []).append(line)
    return {k: "\n".join(v).strip() for k, v in pages.items()}


def reading_order_score(text: str) -> float:
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    if len(lines) < 4:
        return 1.0
    jumps = sum(1 for i in range(1, len(lines)) if lines[i].startswith("#") and not lines[i-1].startswith("#") and len(lines[i-1]) < 20)
    return max(0.0, 1.0 - jumps / max(1, len(lines) / 10))


def table_structure_score(text: str) -> float:
    lines = [x for x in text.splitlines() if "|" in x]
    if not lines:
        return 1.0
    valid = sum(1 for x in lines if x.count("|") >= 2)
    divs = sum(1 for x in lines if re.search(r"\|\s*[-:]{3,}\s*\|", x))
    if divs == 0 and len(lines) >= 3:
        return 0.2
    return min(1.0, (valid / max(1, len(lines))) * 0.6 + (divs / max(1, len(lines))) * 0.4)


def stat_block_score(text: str) -> float:
    pats = ["armor class", "hit points", "speed", "skills", "saving throws", "actions"]
    low = text.lower()
    hits = sum(1 for p in pats if p in low)
    if hits == 0:
        return 1.0
    sep = len(re.findall(r"\n\s*[-*]\s+", text)) + text.count("|")
    return min(1.0, sep / (hits * 2 + 1))


def audit_markdown(md_path: Path, profile: PdfProfile, cfg: RuntimeConfig) -> AuditResult:
    if not md_path.exists():
        return AuditResult(False, list(range(profile.total_pages)), [], ["missing_markdown"])
    content = normalize_text(md_path.read_text(encoding="utf-8", errors="replace"))
    if "<!-- PAGE:" not in content:
        content = ensure_page_markers(content, profile.total_pages)
    pages = parse_page_markers(content)
    first_lines, last_lines = {}, {}
    for _, t in pages.items():
        lines = [l.strip() for l in t.splitlines() if l.strip()]
        if lines:
            first_lines[lines[0]] = first_lines.get(lines[0], 0) + 1
            last_lines[lines[-1]] = last_lines.get(lines[-1], 0) + 1
    sigs, audits = set(), []
    for idx in sorted(pages):
        t = pages[idx]
        r = []
        if len(t) < cfg.min_md_chars_per_page:
            r.append("thin_output")
        if "\ufffd" in t:
            r.append("glyph_corruption")
        if re.search(r"archdev[^\w]?ils|conse[^\w]?quences", t, flags=re.IGNORECASE):
            r.append("soft_hyphen_split")
        ts = table_structure_score(t)
        if ts < 0.45:
            r.append("table_structure")
        if reading_order_score(t) < 0.6:
            r.append("reading_order")
        if stat_block_score(t) < 0.4:
            r.append("stat_block_integrity")
        lines = [l.strip() for l in t.splitlines() if l.strip()]
        if lines:
            if first_lines.get(lines[0], 0) > max(4, len(pages) * 0.5):
                r.append("header_repetition")
            if last_lines.get(lines[-1], 0) > max(4, len(pages) * 0.5):
                r.append("footer_repetition")
        m = next((p for p in profile.page_features if p.page_index + 1 == idx), None)
        if m and m.image_coverage < 0.5 and len(t) < cfg.min_md_chars_per_page:
            r.append("coverage_drop")
        if r:
            sigs.update(r)
        audits.append(PageAudit(idx, not r, r, len(t), ts))
    failed = [a.page_index - 1 for a in audits if not a.passed]
    return AuditResult(not failed, failed, audits, sorted(sigs))


def sample_and_race(cfg: RuntimeConfig, pdf: Path, out_dir: Path, profile: PdfProfile, log_file: Path) -> str:
    pages = sorted(profile.samples)[:max(2, cfg.sample_race_pages)]
    if not pages:
        return "B"
    micro = out_dir / "_race_sample.pdf"
    with fitz.open(pdf) as src, fitz.open() as dst:
        for p in pages:
            if p < len(src):
                dst.insert_pdf(src, from_page=p, to_page=p)
        dst.save(micro)
    scores = {}
    try:
        md, _, _, _ = run_marker(cfg, micro, out_dir / "_race_marker", profile, log_file)
        scores["B"] = len(audit_markdown(md, profile, cfg).failed_pages)
    except Exception:
        scores["B"] = 999
    try:
        md, _, _ = run_docling(cfg, micro, out_dir / "_race_docling", profile, log_file)
        scores["B2"] = len(audit_markdown(md, profile, cfg).failed_pages)
    except Exception:
        scores["B2"] = 999
    try:
        amd, apm = out_dir / "_race_a.md", out_dir / "_race_a_pages.json"
        write_page_markers_from_blocks(micro, amd, apm)
        scores["A"] = len(audit_markdown(amd, profile, cfg).failed_pages)
    except Exception:
        scores["A"] = 999
    micro.unlink(missing_ok=True)
    return min(scores, key=scores.get) if scores else "B"


def process_book(cfg: RuntimeConfig, pdf: Path, repair_queue: dict[str, Any]) -> BookManifest:
    t0, started_iso = time.perf_counter(), now_iso()
    if not verify_pdf_magic(pdf):
        q = cfg.output_dir / "quarantine" / pdf.name
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(pdf), str(q))
        raise RuntimeError(f"invalid pdf; quarantined {q}")
    check_disk_space(cfg)

    out_dir = cfg.output_dir / pdf.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    log_file, md_out, page_meta = cfg.log_dir / f"{pdf.stem}.log", out_dir / f"{pdf.stem}.md", out_dir / f"{pdf.stem}.pages.json"

    if md_out.exists() and not cfg.overwrite_existing:
        return BookManifest(pdf.stem, str(pdf), "SKIP", {}, "unknown", 0, 0, 0, 0, 0, "skipped", 0, "skip", started_iso, now_iso(), round(time.perf_counter()-t0,3), str(md_out), str(page_meta), [], [])

    profile = analyze_pdf(pdf, cfg)
    lane, scores = choose_lane(profile, cfg)
    if cfg.sample_and_race:
        lane = sample_and_race(cfg, pdf, out_dir, profile, log_file)

    ocr_mode = route_ocr_mode(profile, cfg)
    active_pdf = run_ocr(cfg, pdf, out_dir / f"{pdf.stem}_ocr.pdf", ocr_mode, log_file)

    marker_api_variant, lane_meta = None, []
    page_marker_mode = "native"
    if lane == "A":
        write_page_markers_from_blocks(active_pdf, md_out, page_meta)
        page_marker_mode = "source_blocks"
    elif lane == "B":
        md_out, marker_api_variant, lane_meta, page_marker_mode = run_marker(cfg, active_pdf, out_dir, profile, log_file)
    else:
        md_out, lane_meta, page_marker_mode = run_docling(cfg, active_pdf, out_dir, profile, log_file)

    txt = normalize_text(md_out.read_text(encoding="utf-8", errors="replace"))
    normalized = ensure_page_markers(txt, profile.total_pages)
    if cfg.strict_page_truth and "<!-- PAGE:" not in normalized:
        raise RuntimeError("strict_page_truth: missing PAGE markers after extraction")
    md_out.write_text(normalized, encoding="utf-8")

    audit = audit_markdown(md_out, profile, cfg)

    pages = parse_page_markers(md_out.read_text(encoding="utf-8", errors="replace"))
    sidecar = [{
        "page": p,
        "chunks": [blk for blk in re.split(r"\n\n+", body) if blk.strip()],
        "table_like_chunks": [blk for blk in re.split(r"\n\n+", body) if blk.count("|") >= 2],
    } for p, body in pages.items()]
    save_json(cfg.table_sidecar_dir / f"{pdf.stem}.tables.json", sidecar)

    failed_pages = list(range(len(pages))) if cfg.enforce_full_book_repair and not audit.passed else audit.failed_pages
    if failed_pages:
        key = str(pdf.resolve())
        existing = repair_queue.get(key, {})
        outstanding = sorted(set(existing.get("failed_pages", [])) | set(failed_pages))
        repair_queue[key] = {
            "file": str(pdf.resolve()),
            "failed_pages": outstanding,
            "md_path": str(md_out),
            "full_book_repair": cfg.enforce_full_book_repair,
            "queued_at": now_iso(),
            "audit_signatures": audit.signatures,
            "page_reasons": {str(a.page_index): a.reasons for a in audit.page_audits if a.reasons},
            "page_profiles": {str(p.page_index + 1): asdict(p) for p in profile.page_features},
        }

    ocr_applied_pages = list(range(1, profile.total_pages + 1)) if ocr_mode in {"force", "redo"} else []
    page_rows = [{
        "page": p.page_index + 1,
        "chars": p.char_count,
        "blocks": p.block_count,
        "detected_tables": p.table_density,
        "detected_columns": p.is_multicolumn,
        "table_regions_detected": 1 if p.table_density > 0.15 else 0,
        "statblock_regions_detected": 1 if p.statblock_density > 0.3 else 0,
        "ocr_applied": (p.page_index + 1) in ocr_applied_pages,
        "source_page_hash": f"{pdf.stem}:{p.page_index+1}:{p.char_count}:{p.block_count}",
        "repair": {"repaired": False, "unrepaired": True, "retry_count": 0, "final_dpi": None, "prompt_class": None, "repair_confidence": None},
        "lane": lane,
        "page_marker_mode": page_marker_mode,
        "audit": next((a.reasons for a in audit.page_audits if a.page_index == p.page_index + 1), []),
    } for p in profile.page_features]
    save_json(page_meta, page_rows)

    manifest = BookManifest(
        pdf.stem,
        str(pdf),
        lane,
        scores,
        profile.donor_family,
        profile.total_pages,
        profile.total_pages,
        len(pages),
        len(pages) - len(failed_pages),
        len(failed_pages),
        page_marker_mode,
        len(lane_meta),
        ocr_mode,
        started_iso,
        now_iso(),
        round(time.perf_counter()-t0, 3),
        str(md_out),
        str(page_meta),
        audit.signatures,
        failed_pages,
        marker_api_variant,
    )
    save_json(cfg.manifests_dir / f"{pdf.stem}.manifest.json", asdict(manifest))
    return manifest


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Aether Forge orchestrator v11")
    p.add_argument("--glob", default="*.pdf")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--strict_page_truth", action="store_true")
    return p.parse_args()


def main() -> None:
    cfg = RuntimeConfig.from_env(Path(__file__).parent)
    args = parse_args()
    if args.strict_page_truth:
        cfg.strict_page_truth = True
    ensure_dirs(cfg)

    pdfs = sorted(cfg.input_dir.glob(args.glob))
    if args.limit > 0:
        pdfs = pdfs[: args.limit]

    queue = load_json(cfg.repair_queue_file, {}) if args.resume else {}
    save_json(cfg.repair_queue_file, queue)

    db = None
    if cfg.use_sqlite_queue and QueueDB is not None and cfg.sqlite_queue_path is not None:
        db = QueueDB(cfg.sqlite_queue_path)
        for bid, record in queue.items():
            db.upsert_queue_item(queue_item_from_record(bid, record))

    summary = {"started_at": now_iso(), "books_total": len(pdfs), "books_ok": 0, "books_failed": 0, "books_queued": 0, "lane_counts": {}}

    for i, pdf in enumerate(pdfs, start=1):
        print(f"\n=== [{i}/{len(pdfs)}] {pdf.name} ===")
        try:
            m = process_book(cfg, pdf, queue)
            summary["lane_counts"][m.lane] = summary["lane_counts"].get(m.lane, 0) + 1
            if m.failed_pages:
                summary["books_queued"] += 1
            else:
                summary["books_ok"] += 1
        except Exception as exc:  # pylint: disable=broad-exception-caught
            summary["books_failed"] += 1
            with open(cfg.log_dir / "orchestrator_fatal.log", "a", encoding="utf-8") as f:
                f.write(f"[{pdf.name}] {exc}\n")
            if not cfg.continue_on_error:
                raise
            print(f"  ! error: {exc}")
        finally:
            save_json(cfg.repair_queue_file, queue)
            if db is not None:
                for bid, rec in queue.items():
                    db.upsert_queue_item(queue_item_from_record(bid, rec))

    summary["finished_at"] = now_iso()
    save_json(cfg.log_dir / "run_summary.json", summary)
    if db is not None:
        db.close()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
