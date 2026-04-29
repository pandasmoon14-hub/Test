import pytest
fitz = pytest.importorskip("fitz")

from orchestrator import write_page_markers_from_blocks, parse_page_markers


def test_marker_writer_emits_all_source_pages(tmp_path: Path):
    pdf = tmp_path / "fixture.pdf"
    doc = fitz.open()
    for i in range(10):
        p = doc.new_page()
        p.insert_text((72,72), f"Page {i+1}")
    doc.save(pdf)
    doc.close()

    md_out = tmp_path / "out.md"
    page_json = tmp_path / "pages.json"
    write_page_markers_from_blocks(pdf, md_out, page_json)
    pages = parse_page_markers(md_out.read_text(encoding="utf-8"))
    assert len(pages) == 10
    assert sorted(pages) == list(range(1,11))