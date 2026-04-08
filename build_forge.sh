#!/usr/bin/env bash
set -euo pipefail

# Save as /workspace/build_forge.sh and run: bash /workspace/build_forge.sh

echo "Building The Aether Forge (Local-Only Architecture)..."

# 1. Clean previous monolithic states
rm -rf /workspace/venvs /workspace/ttrpg_output /workspace/quarantine_smoke
mkdir -p /workspace/venvs
mkdir -p /workspace/ttrpg_output/failed_queue
mkdir -p /workspace/ttrpg_output/repair_queue

# 2. System-level dependencies for OCRmyPDF and PyMuPDF
apt-get update && apt-get install -y tesseract-ocr ghostscript

# 3. The Orchestrator Environment (PyMuPDF & OCRmyPDF)
python3 -m venv /workspace/venvs/orchestrator
/workspace/venvs/orchestrator/bin/pip install --upgrade pip
/workspace/venvs/orchestrator/bin/pip install pymupdf ocrmypdf

# 4. The Marker Environment (Lane B - Primary Bulk)
python3 -m venv /workspace/venvs/marker
/workspace/venvs/marker/bin/pip install --upgrade pip
/workspace/venvs/marker/bin/pip install marker-pdf

# 5. The Docling Environment (Lane B - Secondary Bulk / Fallback)
python3 -m venv /workspace/venvs/docling
/workspace/venvs/docling/bin/pip install --upgrade pip
/workspace/venvs/docling/bin/pip install docling

# 6. The Pixtral Surgeon Environment (Lane C - VLM Repair)
python3 -m venv /workspace/venvs/pixtral
/workspace/venvs/pixtral/bin/pip install --upgrade pip
/workspace/venvs/pixtral/bin/pip install "vllm==0.6.1.post2" "mistral-common==1.4.4" "transformers>=4.44.0,<5.0.0" "numpy<2.0" "pymupdf" "pillow"

echo "Forge Environments Built Successfully."
