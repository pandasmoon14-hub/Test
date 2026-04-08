#!/usr/bin/env bash
set -euo pipefail

# Aether Forge (v10) — Environment build script
# Usage:
#   bash /workspace/build_forge.sh                 # fresh build
#   FORCE_REBUILD=1 bash /workspace/build_forge.sh # wipe and rebuild

WORKSPACE_ROOT="${WORKSPACE_ROOT:-/workspace}"
VENVS_DIR="${WORKSPACE_ROOT}/venvs"
OUTPUT_DIR="${OUTPUT_DIR:-${WORKSPACE_ROOT}/ttrpg_output}"
FORCE_REBUILD="${FORCE_REBUILD:-0}"

echo "Building The Aether Forge (Local-Only Architecture)..."

if [[ "$FORCE_REBUILD" == "1" ]]; then
  echo "FORCE_REBUILD=1 — removing prior environments and output."
  rm -rf "$VENVS_DIR" "$OUTPUT_DIR" "${WORKSPACE_ROOT}/quarantine_smoke"
fi

mkdir -p "$VENVS_DIR"
mkdir -p "${OUTPUT_DIR}/failed_queue"
mkdir -p "${OUTPUT_DIR}/repair_queue"
mkdir -p "${OUTPUT_DIR}/logs"

apt-get update && apt-get install -y tesseract-ocr ghostscript

# Orchestrator — PyMuPDF + OCRmyPDF (lightweight, CPU-only routing env)
python3 -m venv "${VENVS_DIR}/orchestrator"
"${VENVS_DIR}/orchestrator/bin/pip" install --upgrade pip
"${VENVS_DIR}/orchestrator/bin/pip" install pymupdf ocrmypdf

# Marker — primary bulk converter (owns its own torch/transformers)
python3 -m venv "${VENVS_DIR}/marker"
"${VENVS_DIR}/marker/bin/pip" install --upgrade pip
"${VENVS_DIR}/marker/bin/pip" install marker-pdf

# Docling — secondary bulk converter / Marker fallback
python3 -m venv "${VENVS_DIR}/docling"
"${VENVS_DIR}/docling/bin/pip" install --upgrade pip
"${VENVS_DIR}/docling/bin/pip" install docling

# Pixtral Surgeon — vLLM + Pixtral-12B (pinned for ABI stability)
# opencv-python-headless is required by vision model internals at runtime.
python3 -m venv "${VENVS_DIR}/pixtral"
"${VENVS_DIR}/pixtral/bin/pip" install --upgrade pip
"${VENVS_DIR}/pixtral/bin/pip" install \
  "vllm==0.6.1.post2" \
  "mistral-common==1.4.4" \
  "transformers>=4.44.0,<5.0.0" \
  "numpy<2.0" \
  "pymupdf" \
  "pillow" \
  "opencv-python-headless"

# Capture exact dependency state for reproducibility.
# Commit or archive these lockfiles after the first successful bakeoff.
echo "Generating dependency lockfiles..."
"${VENVS_DIR}/orchestrator/bin/pip" freeze > "${WORKSPACE_ROOT}/orchestrator.lock"
"${VENVS_DIR}/marker/bin/pip"       freeze > "${WORKSPACE_ROOT}/marker.lock"
"${VENVS_DIR}/docling/bin/pip"      freeze > "${WORKSPACE_ROOT}/docling.lock"
"${VENVS_DIR}/pixtral/bin/pip"      freeze > "${WORKSPACE_ROOT}/pixtral.lock"

echo "Forge Environments Built Successfully."
echo "VENVS_DIR=${VENVS_DIR}  OUTPUT_DIR=${OUTPUT_DIR}"
echo "Lockfiles written to ${WORKSPACE_ROOT}/*.lock"
