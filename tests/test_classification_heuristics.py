from extraction_readiness import classify_page_disposition, summarize_dispositions


def test_native_text_is_ok():
    d = classify_page_disposition(text_chars=120, image_count=0, drawing_count=0, extracted_text="x"*120, ocr_mode="skip", lane="A")
    assert d.status == "ok"


def test_reason_counts_populated_for_degraded_pages():
    rows = [
        {"disposition": "ok", "reason_code": "native_text_extracted"},
        {"disposition": "ocr_needed", "reason_code": "image_only_no_ocr"},
    ]
    summary = summarize_dispositions(rows)
    assert summary["pages_ocr_needed"] == 1
    assert summary["reason_code_counts"]
