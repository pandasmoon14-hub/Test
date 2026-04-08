#!/bin/bash
# Aether Forge (v10) - Environment Matrix Builder
# Run as: bash /workspace/build_forge.sh

set -euo pipefail

echo "=============================================="
echo " Building The Aether Forge (v10)"
echo " 100% Local | A6000-Optimized Architecture"
echo "=============================================="

# 1. Clean previous monolithic states
echo "[1/6] Cleaning previous environments..."
rm -rf /workspace/venvs /workspace/ttrpg_output /workspace/quarantine_smoke
mkdir -p /workspace/venvs
mkdir -p /workspace/ttrpg_output/failed_queue
mkdir -p /workspace/ttrpg_output/repair_queue
mkdir -p /workspace/ttrpg_input

# 2. System-level dependencies for OCRmyPDF and PyMuPDF
echo "[2/6] Installing system dependencies (Tesseract, Ghostscript)..."
apt-get update -qq && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    ghostscript \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    > /tmp/apt_install.log 2>&1
echo "      System deps installed."

# 3. Orchestrator Environment: PyMuPDF + OCRmyPDF
# Lightweight, CPU-only, runs the routing/preflight/audit logic.
echo "[3/6] Building Orchestrator environment (PyMuPDF + OCRmyPDF)..."
python3 -m venv /workspace/venvs/orchestrator
/workspace/venvs/orchestrator/bin/pip install --upgrade pip --quiet
/workspace/venvs/orchestrator/bin/pip install --quiet \
    pymupdf \
    ocrmypdf
echo "      Orchestrator environment ready."

# 4. Marker Environment: Primary bulk PDF-to-Markdown converter
# Handles markdown/JSON/chunks/HTML output, tables, equations, images, reading order.
# Marker manages its own torch/transformers internally.
echo "[4/6] Building Marker environment (Lane B - Primary Bulk)..."
python3 -m venv /workspace/venvs/marker
/workspace/venvs/marker/bin/pip install --upgrade pip --quiet
/workspace/venvs/marker/bin/pip install --quiet marker-pdf
echo "      Marker environment ready."

# 5. Docling Environment: Secondary bulk converter / Marker fallback
# Provides an independent layout engine if Marker fails on a given PDF.
echo "[5/6] Building Docling environment (Lane B2 - Secondary Bulk / Fallback)..."
python3 -m venv /workspace/venvs/docling
/workspace/venvs/docling/bin/pip install --upgrade pip --quiet
/workspace/venvs/docling/bin/pip install --quiet docling
echo "      Docling environment ready."

# 6. Pixtral Surgeon Environment: VLM repair via vLLM
# Pinned numpy<2.0 to prevent vLLM/numpy ABI conflicts.
# Pinned vllm version for mistral tokenizer compatibility.
echo "[6/6] Building Pixtral Surgeon environment (Lane C - VLM Repair)..."
python3 -m venv /workspace/venvs/pixtral
/workspace/venvs/pixtral/bin/pip install --upgrade pip --quiet
/workspace/venvs/pixtral/bin/pip install --quiet \
    "vllm==0.6.1.post2" \
    "mistral-common==1.4.4" \
    "transformers>=4.44.0,<5.0.0" \
    "numpy<2.0" \
    "pymupdf" \
    "pillow"
echo "      Pixtral Surgeon environment ready."

echo ""
echo "=============================================="
echo " Aether Forge (v10) Environments Built."
echo ""
echo " Run order:"
echo "   Phase 1 (CPU/Light):  /workspace/venvs/orchestrator/bin/python3 /workspace/orchestrator.py"
echo "   Phase 2 (Heavy GPU):  /workspace/venvs/pixtral/bin/python3 /workspace/surgeon.py"
echo ""
echo " Input PDFs:  /workspace/ttrpg_input/"
echo " Output:      /workspace/ttrpg_output/"
echo "=============================================="
