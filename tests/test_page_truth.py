import json
from pathlib import Path

from page_truth import PageTruthRecord, write_page_truth_jsonl


def test_page_truth_record_shape_and_writer(tmp_path: Path):
    rec = PageTruthRecord(
        book_id="book",
        source_path="/tmp/book.pdf",
        source_sha256="abc",
        page_index_zero_based=0,
        page_number_one_based=1,
        width=612,
        height=792,
        rotation=0,
        text_chars=100,
        extracted_chars=90,
        blocks=5,
        image_count=1,
        drawing_count=0,
        extraction_backend="pymupdf",
        extraction_lane="A",
    )
    out = tmp_path / "pt.jsonl"
    write_page_truth_jsonl(out, [rec])
    line = out.read_text(encoding="utf-8").strip()
    payload = json.loads(line)
    assert payload["book_id"] == "book"
    assert payload["page_number_one_based"] == 1
    assert payload["warnings"] == []
