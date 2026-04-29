from __future__ import annotations
from pathlib import Path

try:
    import fitz
except Exception as exc:
    raise SystemExit(f"PyMuPDF required: {exc}")

OUT = Path(__file__).parent / "pdfs"
OUT.mkdir(parents=True, exist_ok=True)


def save(name, build):
    doc = fitz.open()
    build(doc)
    doc.save(OUT / name)


def native(doc):
    p = doc.new_page()
    p.insert_text((72, 72), "Native text page. " * 100)


def blank(doc):
    doc.new_page()


def image_only(doc):
    p = doc.new_page()
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 100, 100), False)
    pix.clear_with(180)
    p.insert_image(fitz.Rect(72, 72, 250, 250), pixmap=pix)


def mixed10(doc):
    for i in range(10):
        p = doc.new_page()
        if i % 3 == 0:
            p.insert_text((72, 72), f"Page {i+1} native text " * 60)
        elif i % 3 == 1:
            pass
        else:
            pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 100, 100), False)
            pix.clear_with(200)
            p.insert_image(fitz.Rect(72, 72, 250, 250), pixmap=pix)


save("single_column_prose.pdf", native)
save("two_column_rules.pdf", native)
save("dense_table.pdf", native)
save("blank_page.pdf", blank)
save("image_only_scan_like.pdf", image_only)
save("multi_page_mixed_10_pages.pdf", mixed10)
print(f"Generated fixtures in {OUT}")
