from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


@dataclass
class PageDisposition:
    status: str
    reason_code: str | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def classify_page_disposition(
    *,
    text_chars: int,
    image_count: int,
    drawing_count: int,
    extracted_text: str,
    ocr_mode: str,
    lane: str,
    text_threshold: int = 40,
) -> PageDisposition:
    extracted_chars = len((extracted_text or "").strip())

    if text_chars >= text_threshold or extracted_chars >= text_threshold:
        warnings: list[str] = []
        if extracted_chars < text_threshold and image_count > 0:
            warnings.append("low_text_image_heavy")
        return PageDisposition(status="ok", reason_code="native_text_extracted", warnings=warnings)

    if text_chars == 0 and image_count == 0 and drawing_count == 0:
        return PageDisposition(status="empty", reason_code="blank_source_page")

    if text_chars == 0 and image_count > 0:
        if ocr_mode in {"force", "redo"}:
            return PageDisposition(status="ocr_done", reason_code="image_only_ocr_required")
        return PageDisposition(status="ocr_needed", reason_code="image_only_no_ocr")

    if extracted_chars == 0:
        return PageDisposition(status="queued" if ocr_mode == "skip" else "ocr_needed", reason_code="ocr_required_but_skipped")

    return PageDisposition(status="ok", reason_code="native_text_extracted")


def summarize_dispositions(rows: list[dict]) -> dict:
    counts = Counter(r.get("disposition", "failed") for r in rows)
    reason_codes = Counter(r.get("reason_code") for r in rows if r.get("reason_code"))
    return {
        "total_pages": len(rows),
        "pages_ok": counts.get("ok", 0),
        "pages_empty": counts.get("empty", 0),
        "pages_image_only": counts.get("image_only", 0),
        "pages_ocr_needed": counts.get("ocr_needed", 0),
        "pages_ocr_done": counts.get("ocr_done", 0),
        "pages_queued": counts.get("queued", 0),
        "pages_failed": counts.get("failed", 0),
        "reason_code_counts": dict(reason_codes),
    }
