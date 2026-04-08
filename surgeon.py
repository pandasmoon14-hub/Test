#!/usr/bin/env python3
import base64
import json
import os
from io import BytesIO
from pathlib import Path

import fitz  # PyMuPDF
import PIL.Image
from vllm import LLM, SamplingParams

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/workspace/ttrpg_output"))
QUEUE_FILE = OUTPUT_DIR / "repair_queue" / "queue.json"
MODEL_NAME = "mistralai/Pixtral-12B-2409"
MIN_CROP_SIZE = 96


def pil_to_b64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def repair_book(llm, pdf_path_str, data):
    doc = fitz.open(pdf_path_str)
    failed_pages = data["failed_pages"]
    sampling_params = SamplingParams(temperature=0.0, max_tokens=1024)

    md_path = (
        Path(data["md_path"])
        if data.get("md_path")
        else Path(OUTPUT_DIR) / Path(pdf_path_str).stem / "repair_log.md"
    )
    md_path.parent.mkdir(parents=True, exist_ok=True)

    with open(md_path, "a", encoding="utf-8") as out_file:
        out_file.write("\n\n---\n## LANE C: PIXTRAL VLM REPAIR LOG\n---\n")

        for pg_num in failed_pages:
            if pg_num >= len(doc):
                continue

            page = doc[pg_num]
            pix = page.get_pixmap(dpi=220)
            img = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            if img.width < MIN_CROP_SIZE or img.height < MIN_CROP_SIZE:
                continue

            print(f"       -> Salvaging Page {pg_num + 1}...")
            b64 = pil_to_b64(img)
            messages = [
                [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Transcribe this page exactly. Reconstruct any tables into clean Markdown.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{b64}"},
                            },
                        ],
                    }
                ]
            ]

            try:
                out = llm.chat(messages=messages, sampling_params=sampling_params, use_tqdm=False)
                out_file.write(f"\n### Page {pg_num + 1}\n{out[0].outputs[0].text}\n")
            except Exception as exc:  # pylint: disable=broad-exception-caught
                print(f"         [WARN] Pixtral failed on page {pg_num + 1}: {exc}")

    doc.close()


def main():
    if not QUEUE_FILE.exists():
        print("No repair queue found. Pipeline clear.")
        return

    with open(QUEUE_FILE, "r", encoding="utf-8") as file:
        queue = json.load(file)

    if not queue:
        print("Repair queue empty. Pipeline clear.")
        return

    print(f"Loading {MODEL_NAME} as Surgeon (Context: 16384)...")
    llm = LLM(
        model=MODEL_NAME,
        tokenizer_mode="mistral",
        limit_mm_per_prompt={"image": 1},
        max_model_len=16384,
        gpu_memory_utilization=0.85,
        enforce_eager=True,
    )

    for pdf, data in list(queue.items()):
        print(f"\n--- Operating on: {Path(pdf).name} ---")
        repair_book(llm, pdf, data)
        del queue[pdf]
        with open(QUEUE_FILE, "w", encoding="utf-8") as file:
            json.dump(queue, file, indent=2)


if __name__ == "__main__":
    main()
