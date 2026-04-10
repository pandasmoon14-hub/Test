#!/usr/bin/env python3
"""
Aether Forge Pixtral surgeon (Lane C, v11)

Upgrades:
- repair output written to temp artifact then atomically promoted
- queue shrinks incrementally on partial success
- adaptive DPI and prompt specialization by page profile
- output validation + retry path
- prefix caching enabled
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import time
from dataclasses import asdict, dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Any

import fitz
import PIL.Image
VLLM_AVAILABLE = True
try:
    from vllm import LLM, SamplingParams
except ImportError:  # pragma: no cover - enables unit tests without vLLM installed
    VLLM_AVAILABLE = False
    LLM = Any  # type: ignore
    SamplingParams = Any  # type: ignore


@dataclass
class SurgeonConfig:
    output_dir: Path
    queue_file: Path
    model_name: str = "mistralai/Pixtral-12B-2409"
    min_crop_size: int = 96
    max_page_tokens: int = 4096
    repair_batch: int = 12
    render_dpi: int = 180
    gpu_memory_utilization: float = 0.92
    max_model_len: int = 28672
    tokenizer_mode: str = "mistral"
    gpu_profile: str = "default"

    @classmethod
    def from_env(cls, gpu_profile: str = "default") -> "SurgeonConfig":
        if gpu_profile == "default":
            try:
                import torch  # type: ignore
                if torch.cuda.is_available():
                    vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                    if vram > 40:
                        gpu_profile = "a6000"
            except Exception:
                pass
        output_dir = Path(os.getenv("OUTPUT_DIR", "/workspace/ttrpg_output"))
        defaults = {
            "default": {"max_page_tokens": "4096", "repair_batch": "12", "gpu_memory_utilization": "0.92", "max_model_len": "28672"},
            "a6000": {"max_page_tokens": "4096", "repair_batch": "12", "gpu_memory_utilization": "0.92", "max_model_len": "24576"},
        }
        prof = defaults.get(gpu_profile, defaults["default"])
        return cls(
            output_dir=output_dir,
            queue_file=output_dir / "repair_queue" / "queue.json",
            model_name=os.getenv("PIXTRAL_MODEL", "mistralai/Pixtral-12B-2409"),
            min_crop_size=int(os.getenv("MIN_CROP_SIZE", "96")),
            max_page_tokens=int(os.getenv("MAX_PAGE_TOKENS", prof["max_page_tokens"])),
            repair_batch=int(os.getenv("REPAIR_BATCH", prof["repair_batch"])),
            render_dpi=int(os.getenv("RENDER_DPI", "180")),
            gpu_memory_utilization=float(os.getenv("GPU_MEMORY_UTILIZATION", prof["gpu_memory_utilization"])),
            max_model_len=int(os.getenv("MAX_MODEL_LEN", prof["max_model_len"])),
            tokenizer_mode=os.getenv("TOKENIZER_MODE", "mistral"),
            gpu_profile=gpu_profile,
        )


@dataclass
class RepairStats:
    book_id: str
    source_pdf: str
    output_md: str
    attempted_pages: int
    successful_pages: int
    failed_pages: int
    full_book_repair: bool
    elapsed_sec: float
    warnings: list[str] = field(default_factory=list)


def prompt_for_layout(profile: dict[str, Any]) -> str:
    base = (
        "Transcribe this page to Markdown exactly as it appears. "
        "Preserve headings, paragraphs, and list structure verbatim. "
        "Do NOT summarise, interpret, or add commentary. Output only content. "
    )
    if profile.get("table_density", 0) > 0.15:
        return base + (
            "You must format all tables as strict GitHub Markdown with a header separator row. "
            "Preserve every row and column, including continuation rows. "
            "If table is malformed, output best-faith table with consistent columns."
        )
    if profile.get("sidebar_density", 0) > 0.2:
        return base + "Preserve sidebars/callout boxes as blockquotes (`>`), maintaining order."
    if profile.get("statblock_density", 0) > 0.3:
        return base + "Preserve stat-block key/value fields and indentation exactly."
    if profile.get("image_coverage", 0) > 0.4 or all(profile.get(k, 0.0) < 0.01 for k in ("table_density", "statblock_density", "sidebar_density")):
        return base + (
            "If you see ANY tables, format them as strict GitHub Markdown with header separator rows. "
            "If you see stat blocks or key/value game data, preserve field names and values exactly. "
            "If you see sidebars or callout boxes, format them as blockquotes in reading order."
        )
    return base + "Render equations as LaTeX where obvious."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aether Forge Pixtral surgeon")
    parser.add_argument("--max_books", type=int, default=0)
    parser.add_argument("--dry_run", action="store_true")
    parser.add_argument("--summary_json", default="")
    parser.add_argument("--gpu_profile", choices=["default", "a6000"], default="default")
    return parser.parse_args()


def load_queue(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_queue(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)


def render_page(page: fitz.Page, dpi: int, min_crop_size: int, gpu_profile: str = "default") -> PIL.Image.Image | None:
    pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB)
    image = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    max_dim = 1536 if gpu_profile == "a6000" else 1280
    max_dim = 1280
    if max(image.width, image.height) > max_dim:
        image.thumbnail((max_dim, max_dim))
    if image.width < min_crop_size or image.height < min_crop_size:
        return None
    # skip nearly blank renderings
    hist = image.convert("L").histogram()
    bright_ratio = hist[255] / max(1, sum(hist))
    if bright_ratio > 0.985:
        return None
    return image


def pil_to_b64(img: PIL.Image.Image) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def make_conversation(img: PIL.Image.Image, prompt: str) -> list[dict[str, Any]]:
    return [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{pil_to_b64(img)}"}}]}]


def iter_tiles(img: PIL.Image.Image, tile_w: int, tile_h: int, overlap: int = 64):
    step_x = max(1, tile_w - overlap)
    step_y = max(1, tile_h - overlap)
    for y in range(0, img.height, step_y):
        for x in range(0, img.width, step_x):
            yield (x, y), img.crop((x, y, min(img.width, x + tile_w), min(img.height, y + tile_h)))


def init_llm(cfg: SurgeonConfig) -> LLM:
    if not VLLM_AVAILABLE:
        raise RuntimeError("vLLM is not installed in this environment")
    return LLM(
        model=cfg.model_name,
        tokenizer_mode=cfg.tokenizer_mode,
        limit_mm_per_prompt={"image": 1},
        max_model_len=cfg.max_model_len,
        gpu_memory_utilization=cfg.gpu_memory_utilization,
        enforce_eager=True,
        enable_prefix_caching=True,
    )


def validate_output(text: str, profile: dict[str, Any]) -> bool:
    if not text or len(text.strip()) < 20:
        return False
    if profile.get("table_density", 0) > 0.15 and "|" not in text:
        return False
    if profile.get("statblock_density", 0) > 0.3:
        kv_count = len(re.findall(r"\w+:\s*\S+", text))
        if kv_count < 3:
            return False
    if "\ufffd" in text:
        return False
    return True


def adaptive_dpi(cfg: SurgeonConfig, profile: dict[str, Any]) -> int:
    if profile.get("table_density", 0) > 0.15:
        return max(cfg.render_dpi, 260)
    if profile.get("image_coverage", 0) > 0.5:
        return max(cfg.render_dpi, 220)
    if all(profile.get(k, 0) < 0.01 for k in ("table_density", "statblock_density", "sidebar_density")):
        return max(cfg.render_dpi, 220)
    return cfg.render_dpi


def repair_confidence(text: str, profile: dict[str, Any]) -> float:
    score = 0.5
    if len(text.strip()) > 200:
        score += 0.2
    if profile.get("table_density", 0) > 0.15 and "|" in text:
        score += 0.15
    if re.search(r"^#+\s+", text, re.MULTILINE):
        score += 0.1
    if "\ufffd" in text:
        score -= 0.3
    return max(0.0, min(1.0, score))


def write_merged_markdown(base_md: Path, repaired_pages: dict[int, str], temp_path: Path) -> bool:
    if not base_md.exists():
        base = ""
    else:
        base = base_md.read_text(encoding="utf-8", errors="replace")
    if "<!-- PAGE:" not in base:
        raise ValueError("Cannot merge repaired pages into markdown without trusted page markers")

    parts = {}
    page = 1
    for line in base.splitlines():
        if line.strip().startswith("<!-- PAGE:"):
            m = line.strip().replace("<!-- PAGE:", "").replace("-->", "").strip()
            if m.isdigit():
                page = int(m)
                parts.setdefault(page, [])
            continue
        parts.setdefault(page, []).append(line)

    for p, text in repaired_pages.items():
        # Replacement is intentional: page failed audit and repair output becomes canonical page text.
        parts[p + 1] = [text.strip()]

    with open(temp_path, "w", encoding="utf-8") as file:
        for p in sorted(parts):
            file.write(f"\n<!-- PAGE:{p} -->\n")
            file.write("\n".join(parts[p]).strip() + "\n")

    if repaired_pages:
        max_repaired = max(repaired_pages) + 1
        if len(parts) < max_repaired:
            return False
        for repaired_idx in repaired_pages:
            target_page = repaired_idx + 1
            merged = "\n".join(parts.get(target_page, [])).strip()
            if not merged:
                return False

    ordered = sorted(parts)
    if ordered and ordered != list(range(ordered[0], ordered[-1] + 1)):
        return False
    return True


def repair_book(llm: LLM, cfg: SurgeonConfig, book_id: str, record: dict[str, Any]) -> tuple[RepairStats, list[int]]:
    start = time.perf_counter()
    source_pdf = Path(record["file"])
    failed_pages = list(record.get("failed_pages", []))
    page_profiles = record.get("page_profiles", {})
    full_book_repair = bool(record.get("full_book_repair", False))
    md_path = Path(record.get("md_path") or cfg.output_dir / source_pdf.stem / "repair_log.md")

    warnings: list[str] = []
    if not source_pdf.exists():
        return RepairStats(book_id, str(source_pdf), str(md_path), len(failed_pages), 0, len(failed_pages), full_book_repair, round(time.perf_counter()-start, 3), ["source PDF missing"]), failed_pages

    sampling = SamplingParams(temperature=0.0, top_p=0.0, max_tokens=cfg.max_page_tokens)

    repaired: dict[int, str] = {}
    unresolved = []

    with fitz.open(str(source_pdf)) as doc:
        for batch_start in range(0, len(failed_pages), cfg.repair_batch):
            batch_pages = failed_pages[batch_start: batch_start + cfg.repair_batch]
            total_batches = (len(failed_pages) + cfg.repair_batch - 1) // cfg.repair_batch
            pct = round(100 * batch_start / max(1, len(failed_pages)))
            print(f"  [{book_id}] batch {batch_start // cfg.repair_batch + 1}/{total_batches} ({pct}%)")
            batch_imgs, batch_prompts, page_ids = [], [], []
            for pg in batch_pages:
                if pg >= len(doc):
                    unresolved.append(pg)
                    continue
                profile = page_profiles.get(str(pg + 1), {})
                dpi = adaptive_dpi(cfg, profile)
                img = render_page(doc[pg], dpi=dpi, min_crop_size=cfg.min_crop_size, gpu_profile=cfg.gpu_profile)
                if img is None:
                    unresolved.append(pg)
                    continue
                if profile.get("table_density", 0.0) > 0.25 and max(img.size) > 1400:
                    tile_prompt = batch_prompts[-1] if batch_prompts else prompt_for_layout(profile)
                    tiles = []
                    for (_, _), tile in iter_tiles(img, tile_w=1200, tile_h=1200, overlap=96):
                        if tile.width >= cfg.min_crop_size and tile.height >= cfg.min_crop_size:
                            tiles.append(tile)
                    if not tiles:
                        unresolved.append(pg)
                        continue
                    try:
                        tile_out = llm.chat([make_conversation(tile, tile_prompt) for tile in tiles], sampling_params=sampling, use_tqdm=False)
                        stitched = "\n\n".join((out.outputs[0].text.strip() if out.outputs else "") for out in tile_out).strip()
                        if validate_output(stitched, profile):
                            repaired[pg] = stitched
                            continue
                    except Exception:
                        pass
                batch_imgs.append(img)
                batch_prompts.append(prompt_for_layout(profile))
                page_ids.append(pg)

            if not batch_imgs:
                continue

            conversations = [make_conversation(img, prm) for img, prm in zip(batch_imgs, batch_prompts)]
            try:
                outputs = llm.chat(conversations, sampling_params=sampling, use_tqdm=False)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                warnings.append(f"batch failure {page_ids[0]+1}-{page_ids[-1]+1}: {exc}")
                unresolved.extend(page_ids)
                continue

            for pg, out in zip(page_ids, outputs):
                txt = out.outputs[0].text.strip() if out.outputs else ""
                if not validate_output(txt, page_profiles.get(str(pg + 1), {})):
                    # one retry with stricter table prompt and higher dpi
                    try:
                        prompt = prompt_for_layout({"table_density": 0.5, **page_profiles.get(str(pg + 1), {})})
                        img2 = render_page(doc[pg], dpi=max(cfg.render_dpi, 300), min_crop_size=cfg.min_crop_size, gpu_profile=cfg.gpu_profile)
                        if img2 is not None:
                            retry = llm.chat([make_conversation(img2, prompt)], sampling_params=sampling, use_tqdm=False)
                            txt = retry[0].outputs[0].text.strip() if retry and retry[0].outputs else ""
                    except Exception:
                        pass
                if validate_output(txt, page_profiles.get(str(pg + 1), {})):
                    repaired[pg] = txt
                else:
                    unresolved.append(pg)

        # Targeted second pass for pages that look table-like but missed markdown divider.
        for pg, txt in list(repaired.items()):
            lines = txt.splitlines()
            pipe_count = sum(1 for ln in lines if ln.count("|") >= 2)
            has_divider = any(re.search(r"\|\s*[-:]{3,}\s*\|", ln) for ln in lines)
            if pipe_count >= 3 and not has_divider and pg < len(doc):
                profile = page_profiles.get(str(pg + 1), {})
                retry_prompt = prompt_for_layout({"table_density": 0.6, **profile})
                img = render_page(doc[pg], dpi=max(cfg.render_dpi, 260), min_crop_size=cfg.min_crop_size, gpu_profile=cfg.gpu_profile)
                if img is None:
                    continue
                try:
                    retry = llm.chat([make_conversation(img, retry_prompt)], sampling_params=sampling, use_tqdm=False)
                    retry_txt = retry[0].outputs[0].text.strip() if retry and retry[0].outputs else ""
                    if validate_output(retry_txt, profile):
                        repaired[pg] = retry_txt
                except Exception:
                    continue

    temp_md = md_path.with_suffix(".repair.tmp.md")
    promoted = write_merged_markdown(md_path, repaired, temp_md)
    if promoted:
        temp_md.replace(md_path)
    else:
        warnings.append("atomic promotion skipped due to completeness guard")
        temp_md.unlink(missing_ok=True)

    elapsed = round(time.perf_counter() - start, 3)
    stats = RepairStats(
        book_id=book_id,
        source_pdf=str(source_pdf),
        output_md=str(md_path),
        attempted_pages=len(failed_pages),
        successful_pages=len(repaired),
        failed_pages=len(unresolved),
        full_book_repair=full_book_repair,
        elapsed_sec=elapsed,
        warnings=warnings,
    )
    return stats, sorted(set(unresolved))


def summarize(stats: list[RepairStats]) -> dict[str, Any]:
    total_elapsed = sum(s.elapsed_sec for s in stats)
    return {
        "books_processed": len(stats),
        "pages_attempted": sum(s.attempted_pages for s in stats),
        "pages_repaired": sum(s.successful_pages for s in stats),
        "pages_unrepaired": sum(s.failed_pages for s in stats),
        "elapsed_sec": round(total_elapsed, 3),
        "avg_pages_per_sec": round(sum(s.successful_pages for s in stats) / max(1e-6, total_elapsed), 4),
        "books_with_warnings": sum(1 for s in stats if s.warnings),
    }


def main() -> None:
    args = parse_args()
    cfg = SurgeonConfig.from_env(gpu_profile=args.gpu_profile)

    queue = load_queue(cfg.queue_file)
    if not queue:
        print("Repair queue empty. Pipeline clear.")
        return

    records = list(queue.items())
    if args.max_books > 0:
        records = records[: args.max_books]

    if args.dry_run:
        for key, record in records:
            print(f"- {Path(record.get('file', key)).name}: {len(record.get('failed_pages', []))} pages")
        return

    llm = init_llm(cfg)
    all_stats: list[RepairStats] = []

    for key, record in records:
        print(f"[BOOK] {Path(record.get('file', key)).name}")
        stats, unresolved = repair_book(llm, cfg, key, record)
        all_stats.append(stats)
        if unresolved:
            record["failed_pages"] = unresolved
            record["updated_at"] = time.time()
            queue[key] = record
        else:
            queue.pop(key, None)
        save_queue(cfg.queue_file, queue)

    payload = {"summary": summarize(all_stats), "books": [asdict(s) for s in all_stats]}
    out = Path(args.summary_json) if args.summary_json else (cfg.output_dir / "logs" / "repair_summary.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
