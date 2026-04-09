"""
ttrpg_extractor.py

Robust text extraction for TTRPG-formatted PDFs using Pixtral via vLLM.

Handles:
  - Any number of pages
  - Two-column layouts (the standard for RPG books)
  - Stat blocks, tables, sidebars, and body text
  - Correct top-to-bottom, left-column-first reading order
  - Output to a plain-text or Markdown file
"""

import PIL.Image
import fitz  # PyMuPDF  (pip install pymupdf)
from vllm import LLM, SamplingParams
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DPI = 200           # Higher = better accuracy, more RAM. 150–250 is the sweet spot.
MIN_CROP_PX = 16    # Crops smaller than this in either dimension are skipped.

# Tailored prompts for each region type found in TTRPG books.
PROMPTS = {
    "general": (
        "Transcribe every word in this image exactly as written. "
        "Preserve paragraph breaks, bullet points, numbered lists, and headers. "
        "Do not summarise, paraphrase, or skip any content."
    ),
    "stat_block": (
        "This is a stat block or monster entry from a tabletop RPG document. "
        "Transcribe ALL text exactly, including ability scores, saving throws, "
        "dice notation (e.g. 2d6+3), action names, and special traits. "
        "Use plain text with line breaks between fields."
    ),
    "table": (
        "This is a table from a tabletop RPG document. "
        "Reproduce it as a Markdown table, preserving every column header and "
        "cell value exactly — including dice notation, numbers, and dashes."
    ),
    "sidebar": (
        "This is a sidebar or callout box from a tabletop RPG rulebook. "
        "Transcribe all text exactly, including the title or header if one is present."
    ),
}


# ---------------------------------------------------------------------------
# PDF → images
# ---------------------------------------------------------------------------

def pdf_to_images(pdf_path: str, dpi: int = DPI) -> list[PIL.Image.Image]:
    """
    Converts every page of a PDF to an RGB PIL Image.

    PyMuPDF renders vector art, embedded fonts, and even scanned pages cleanly,
    making it reliable for the wide variety of TTRPG PDF styles.
    """
    doc = fitz.open(pdf_path)
    scale = dpi / 72  # PyMuPDF's native resolution is 72 DPI
    mat = fitz.Matrix(scale, scale)
    images = []
    for page in doc:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    doc.close()
    print(f"[pdf_to_images] {len(images)} page(s) loaded from '{pdf_path}'")
    return images


# ---------------------------------------------------------------------------
# Layout detection
# ---------------------------------------------------------------------------

def detect_columns(page_image: PIL.Image.Image, cols: int = 2) -> list[tuple]:
    """
    Splits a page into column bounding boxes.

    Most TTRPG rulebooks use a two-column layout; 'cols=1' works for single-
    column introductions or appendices. Each column is returned as
    (x1, y1, x2, y2) in pixel coordinates.
    """
    w, h = page_image.width, page_image.height
    h_margin = int(w * 0.04)   # ~4 % horizontal margin
    v_margin = int(h * 0.04)   # ~4 % vertical margin
    col_gap  = int(w * 0.025)  # gap between columns

    usable_w = w - 2 * h_margin - (cols - 1) * col_gap
    col_w = usable_w // cols

    bboxes = []
    x = h_margin
    for _ in range(cols):
        bboxes.append((x, v_margin, x + col_w, h - v_margin))
        x += col_w + col_gap
    return bboxes


def sort_reading_order(bboxes: list[tuple], page_width: int) -> list[tuple]:
    """
    Sorts bounding boxes into left-column-first, top-to-bottom reading order.

    Boxes whose left edge is in the left half of the page come first (sorted
    by their top edge), then the right-half boxes (also sorted by top edge).
    This matches the standard two-column reading order of most RPG books.
    """
    mid = page_width / 2
    left  = sorted([b for b in bboxes if b[0] <  mid], key=lambda b: b[1])
    right = sorted([b for b in bboxes if b[0] >= mid], key=lambda b: b[1])
    return left + right


# ---------------------------------------------------------------------------
# Crop helpers
# ---------------------------------------------------------------------------

def safe_crop(
    page_image: PIL.Image.Image, bbox: tuple
) -> PIL.Image.Image | None:
    """
    Crops page_image to bbox, clamping coordinates to the image boundary.

    Returns None if the resulting crop is invalid or smaller than MIN_CROP_PX
    in either dimension (these are almost always decorative rules or noise).
    """
    try:
        x1, y1, x2, y2 = map(int, bbox)
        x1 = max(0, min(x1, page_image.width))
        x2 = max(0, min(x2, page_image.width))
        y1 = max(0, min(y1, page_image.height))
        y2 = max(0, min(y2, page_image.height))

        if x2 <= x1 or y2 <= y1:
            return None

        crop = page_image.crop((x1, y1, x2, y2))
        if crop.width < MIN_CROP_PX or crop.height < MIN_CROP_PX:
            return None

        return crop
    except Exception as e:
        print(f"[safe_crop] Unexpected error: {e}")
        return None


def classify_region(crop: PIL.Image.Image) -> str:
    """
    Guesses the content type of a crop from its shape, choosing the prompt
    that will give Pixtral the best transcription result.

    Heuristics (tuned for typical TTRPG layouts):
      - Very wide & short  → table row / horizontal rule
      - Roughly square & small → stat block inset
      - Tall & narrow      → sidebar / callout
      - Everything else    → general body text
    """
    w, h = crop.width, crop.height
    aspect = w / h if h > 0 else 1.0

    if aspect > 5.0 and h < 120:
        return "table"
    if 0.6 < aspect < 1.8 and max(w, h) < 500:
        return "stat_block"
    if aspect < 0.35:
        return "sidebar"
    return "general"


# ---------------------------------------------------------------------------
# Transcription
# ---------------------------------------------------------------------------

def pixtral_transcribe(
    llm: LLM,
    sampling_params: SamplingParams,
    crop: PIL.Image.Image,
    content_type: str = "general",
) -> str:
    """
    Sends a single image crop to Pixtral and returns the transcribed text.

    Uses a content-type-specific prompt so the model understands context
    (stat block vs table vs sidebar vs general prose) and formats accordingly.
    """
    prompt_text = PROMPTS.get(content_type, PROMPTS["general"])
    try:
        messages = [{
            "role": "user",
            "content": [
                {"type": "text",      "text": prompt_text},
                {"type": "image_pil", "image_pil": crop},
            ],
        }]
        result = llm.chat(messages=messages, sampling_params=sampling_params)
        return result[0].outputs[0].text.strip()
    except Exception as e:
        print(f"[pixtral_transcribe] Error: {e}")
        return "[Error: Transcription Failed]"


# ---------------------------------------------------------------------------
# Page processing
# ---------------------------------------------------------------------------

def process_page(
    llm: LLM,
    sampling_params: SamplingParams,
    page_image: PIL.Image.Image,
    detected_bboxes: list[tuple] | None = None,
    cols: int = 2,
) -> str:
    """
    Extracts text from one page.

    If detected_bboxes are provided (e.g. from an external layout detector),
    those are used directly. Otherwise the page is divided into 'cols' columns
    using simple heuristics that work well for standard RPG book layouts.

    Regions are always processed in natural reading order.
    """
    if detected_bboxes:
        bboxes = list(detected_bboxes)
    else:
        bboxes = detect_columns(page_image, cols=cols)

    bboxes = sort_reading_order(bboxes, page_image.width)

    page_chunks = []
    for bbox in bboxes:
        crop = safe_crop(page_image, bbox)
        if crop is None:
            continue

        content_type = classify_region(crop)
        text = pixtral_transcribe(llm, sampling_params, crop, content_type)

        if text and "[Error" not in text:
            page_chunks.append(text)

    return "\n\n".join(page_chunks)


# ---------------------------------------------------------------------------
# Full PDF processing
# ---------------------------------------------------------------------------

def process_pdf(
    llm: LLM,
    sampling_params: SamplingParams,
    pdf_path: str,
    output_path: str | None = None,
    dpi: int = DPI,
    cols: int = 2,
) -> str:
    """
    Converts a TTRPG PDF to plain text / Markdown.

    Parameters
    ----------
    llm            : Initialised vLLM LLM instance running Pixtral.
    sampling_params: vLLM SamplingParams for the transcription.
    pdf_path       : Path to the input PDF.
    output_path    : If given, the full transcription is saved here.
    dpi            : Render resolution. 200 is a good default.
    cols           : Number of columns in the layout (1 or 2).

    Returns
    -------
    The full transcribed text as a single string.
    """
    images = pdf_to_images(pdf_path, dpi=dpi)
    total = len(images)
    all_pages = []

    for i, page_image in enumerate(images, start=1):
        print(f"[process_pdf] Page {i}/{total} …")
        text = process_page(llm, sampling_params, page_image, cols=cols)
        all_pages.append(f"<!-- Page {i} -->\n{text}")
        page_image.close()

    full_text = "\n\n".join(all_pages)

    if output_path:
        Path(output_path).write_text(full_text, encoding="utf-8")
        print(f"[process_pdf] Saved to '{output_path}'")

    return full_text


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ---- Initialise the model (do this once; it's expensive) ----
    llm = LLM(model="mistralai/Pixtral-12B-2409", tokenizer_mode="mistral")
    sampling_params = SamplingParams(temperature=0.0, max_tokens=2048)

    # ---- Process a whole PDF ----
    # text = process_pdf(
    #     llm, sampling_params,
    #     pdf_path="my_ttrpg_book.pdf",
    #     output_path="my_ttrpg_book.txt",
    #     cols=2,          # change to 1 for single-column pages
    # )

    # ---- Process a single pre-rendered page image ----
    # img = PIL.Image.open("page_01.png")
    # text = process_page(llm, sampling_params, img, cols=2)
    # print(text)
    # img.close()
