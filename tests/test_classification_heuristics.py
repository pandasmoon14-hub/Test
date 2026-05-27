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


import sys
import types
import pytest


@pytest.mark.xfail(
    strict=True,
    reason="Known Lane A gap: multi-column gear-table/D66 layouts can lose row association in block-sorted extraction.",
)
def test_lane_a_multicolumn_d66_blocks_should_preserve_row_association():
    if "fitz" not in sys.modules:
        sys.modules["fitz"] = types.ModuleType("fitz")
    import orchestrator

    # Known gap: Lane A column/table detection can mangle multi-column, gear, or D66 table layouts.
    # Simulate blocks where left column has (d66, item) and right column has matching cost at same y.
    blocks = [
        (40, 100, 260, 112, "11  Rusted Lockpick", 0, 0),
        (320, 100, 520, 112, "5 sp", 0, 1),
        (40, 120, 260, 132, "12  Coil of Wire", 0, 2),
        (320, 120, 520, 132, "1 gp", 0, 3),
        (40, 140, 260, 152, "13  Glowcap Vial", 0, 4),
        (320, 140, 520, 152, "8 sp", 0, 5),
    ]

    sorted_blocks = orchestrator.column_sorted_blocks(blocks, page_width=600)
    lines = [b[4] for b in sorted_blocks]

    # Desired future behavior: per-row left/right values stay adjacent enough for conversion handoff reconstruction.
    assert lines == [
        "11  Rusted Lockpick", "5 sp",
        "12  Coil of Wire", "1 gp",
        "13  Glowcap Vial", "8 sp",
    ]
