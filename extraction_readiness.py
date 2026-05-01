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
    ocr_attempted: bool = False,
    ocr_applied: bool = False,
    ocr_error: str | None = None,
    ocr_skip_reason: str | None = None,
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
            if (ocr_applied or ocr_attempted) and extracted_chars == 0:
                return PageDisposition(
                    status="queued",
                    reason_code="post_ocr_text_extraction_empty",
                    errors=["OCR artifact was produced, but post-OCR extraction did not recover usable text for this page."],
                    warnings=["page_missing_from_extraction_output"],
                )
            if ocr_applied or extracted_chars > 0:
                return PageDisposition(status="ocr_done", reason_code="ocr_applied")
            if ocr_error:
                return PageDisposition(status="queued", reason_code="ocr_failed", errors=[ocr_error])
            if ocr_skip_reason == "dependency_missing":
                return PageDisposition(status="ocr_needed", reason_code="ocr_dependency_missing")
            if ocr_skip_reason == "page_cap_reached":
                return PageDisposition(status="queued", reason_code="ocr_page_cap_reached")
            if ocr_skip_reason:
                return PageDisposition(status="queued", reason_code="ocr_skipped_by_policy", warnings=[ocr_skip_reason])
            return PageDisposition(status="ocr_needed", reason_code="ocr_dependency_missing")
        return PageDisposition(status="ocr_needed", reason_code="image_only_no_ocr")

    if extracted_chars == 0:
        if ocr_mode == "skip":
            return PageDisposition(status="queued", reason_code="ocr_required_but_skipped")
        if ocr_applied or ocr_attempted:
            return PageDisposition(
                status="queued",
                reason_code="post_ocr_text_extraction_empty",
                errors=["OCR artifact was produced, but post-OCR extraction did not recover usable text for this page."],
                warnings=["page_missing_from_extraction_output"],
            )
        if ocr_error:
            return PageDisposition(status="queued", reason_code="ocr_failed", errors=[ocr_error])
        if ocr_skip_reason == "dependency_missing":
            return PageDisposition(status="ocr_needed", reason_code="ocr_dependency_missing")
        if ocr_skip_reason == "page_cap_reached":
            return PageDisposition(status="queued", reason_code="ocr_page_cap_reached")
        return PageDisposition(status="queued", reason_code="ocr_skipped_by_policy")

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
