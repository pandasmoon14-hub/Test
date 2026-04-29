import pytest
fitz = pytest.importorskip("fitz")


from extraction_readiness import classify_page_disposition


def _make_pdf(with_text=False, with_image=False):
    doc = fitz.open()
    page = doc.new_page()
    if with_text:
        page.insert_text((72, 72), "This is native text in the PDF page." * 5)
    if with_image:
        pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 20, 20), False)
        pix.clear_with(200)
        page.insert_image(fitz.Rect(100, 100, 200, 200), pixmap=pix)
    return doc


def test_native_text_not_marked_ocr_needed():
    doc = _make_pdf(with_text=True)
    page = doc[0]
    txt = page.get_text("text")
    disp = classify_page_disposition(
        text_chars=len(txt.strip()),
        image_count=len(page.get_images(full=True)),
        drawing_count=len(page.get_drawings()),
        extracted_text=txt,
        ocr_mode="skip",
        lane="A",
    )
    assert disp.status == "ok"
    assert disp.reason_code == "native_text_extracted"


def test_blank_page_empty_not_queued():
    doc = _make_pdf()
    page = doc[0]
    disp = classify_page_disposition(
        text_chars=0,
        image_count=len(page.get_images(full=True)),
        drawing_count=len(page.get_drawings()),
        extracted_text="",
        ocr_mode="skip",
        lane="A",
    )
    assert disp.status == "empty"
    assert disp.reason_code == "blank_source_page"


def test_image_only_ocr_skip_needs_repair_signal():
    doc = _make_pdf(with_image=True)
    page = doc[0]
    disp = classify_page_disposition(
        text_chars=0,
        image_count=len(page.get_images(full=True)),
        drawing_count=len(page.get_drawings()),
        extracted_text="",
        ocr_mode="skip",
        lane="C",
    )
    assert disp.status == "ocr_needed"
    assert disp.reason_code in {"image_only_no_ocr", "ocr_required_but_skipped"}