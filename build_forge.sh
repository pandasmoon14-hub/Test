#!/usr/bin/env bash
set -euo pipefail

# Aether Forge (v10+) — deterministic local build for routed PDF->Markdown extraction.
#
# Goals:
# - Keep every lane isolated in its own venv to avoid dependency collisions.
# - Produce lockfiles for reproducibility.
# - Include optional smoke checks so failures surface before long unattended runs.
#
# Usage:
#   bash /workspace/Test/build_forge.sh
#   FORCE_REBUILD=1 bash /workspace/Test/build_forge.sh
#   RUN_SMOKE=1 bash /workspace/Test/build_forge.sh
#
# Inputs (env vars):
#   WORKSPACE_ROOT   default: /workspace
#   VENVS_DIR        default: $WORKSPACE_ROOT/venvs
#   OUTPUT_DIR       default: $WORKSPACE_ROOT/ttrpg_output
#   FORCE_REBUILD    default: 0
#   RUN_SMOKE        default: 0
#   PYTHON_BIN       default: python3
#   APT_PACKAGES     default: "tesseract-ocr ghostscript"

WORKSPACE_ROOT="${WORKSPACE_ROOT:-/workspace}"
VENVS_DIR="${VENVS_DIR:-${WORKSPACE_ROOT}/venvs}"
OUTPUT_DIR="${OUTPUT_DIR:-${WORKSPACE_ROOT}/ttrpg_output}"
FORCE_REBUILD="${FORCE_REBUILD:-0}"
RUN_SMOKE="${RUN_SMOKE:-0}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
APT_PACKAGES="${APT_PACKAGES:-tesseract-ocr ghostscript}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SMOKE_DIR="${WORKSPACE_ROOT}/quarantine_smoke"

ORCH_VENV="${VENVS_DIR}/orchestrator"
MARKER_VENV="${VENVS_DIR}/marker"
DOCLING_VENV="${VENVS_DIR}/docling"
PIXTRAL_VENV="${VENVS_DIR}/pixtral"

LOG_DIR="${OUTPUT_DIR}/logs"
FAILED_DIR="${OUTPUT_DIR}/failed_queue"
REPAIR_DIR="${OUTPUT_DIR}/repair_queue"

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m"

say() {
  printf "%b\n" "${BLUE}[forge]${NC} $*"
}

ok() {
  printf "%b\n" "${GREEN}[ok]${NC} $*"
}

warn() {
  printf "%b\n" "${YELLOW}[warn]${NC} $*"
}

die() {
  printf "%b\n" "${RED}[err]${NC} $*" >&2
  exit 1
}

check_prereqs() {
  command -v "${PYTHON_BIN}" >/dev/null 2>&1 || die "Missing ${PYTHON_BIN}"
  command -v apt-get >/dev/null 2>&1 || die "Missing apt-get (required for OCR deps)"
}

prepare_dirs() {
  mkdir -p "${VENVS_DIR}" "${OUTPUT_DIR}" "${LOG_DIR}" "${FAILED_DIR}" "${REPAIR_DIR}"
}

reset_if_requested() {
  if [[ "${FORCE_REBUILD}" == "1" ]]; then
    warn "FORCE_REBUILD=1 set; removing venvs + output + smoke directories"
    rm -rf "${VENVS_DIR}" "${OUTPUT_DIR}" "${SMOKE_DIR}"
    mkdir -p "${VENVS_DIR}" "${OUTPUT_DIR}" "${LOG_DIR}" "${FAILED_DIR}" "${REPAIR_DIR}"
  fi
}

apt_install() {
  say "Installing apt packages: ${APT_PACKAGES}"
  apt-get update -y
  apt-get install -y ${APT_PACKAGES}
  ok "APT dependencies installed"
}

create_venv() {
  local target="$1"
  say "Creating venv: ${target}"
  "${PYTHON_BIN}" -m venv "${target}"
  "${target}/bin/pip" install --upgrade pip setuptools wheel
}

install_orchestrator_deps() {
  say "Installing orchestrator dependencies"
  "${ORCH_VENV}/bin/pip" install \
    pymupdf \
    ocrmypdf \
    pydantic \
    python-dateutil
}

install_marker_deps() {
  say "Installing marker dependencies"
  "${MARKER_VENV}/bin/pip" install \
    marker-pdf
}

install_docling_deps() {
  say "Installing docling dependencies"
  "${DOCLING_VENV}/bin/pip" install \
    docling \
    pymupdf
}

install_pixtral_deps() {
  say "Installing pixtral dependencies"
  "${PIXTRAL_VENV}/bin/pip" install \
    "vllm==0.6.1.post2" \
    "mistral-common==1.4.4" \
    "transformers==4.45.2" \
    "numpy<2.0" \
    "pymupdf" \
    "pillow" \
    "opencv-python-headless"
}

freeze_lockfiles() {
  say "Writing lockfiles"
  "${ORCH_VENV}/bin/pip" freeze > "${WORKSPACE_ROOT}/orchestrator.lock"
  "${MARKER_VENV}/bin/pip" freeze > "${WORKSPACE_ROOT}/marker.lock"
  "${DOCLING_VENV}/bin/pip" freeze > "${WORKSPACE_ROOT}/docling.lock"
  "${PIXTRAL_VENV}/bin/pip" freeze > "${WORKSPACE_ROOT}/pixtral.lock"
  ok "Lockfiles generated"
}

smoke_python_imports() {
  say "Running Python import smoke checks"

  "${ORCH_VENV}/bin/python" - <<'PY'
import fitz
import ocrmypdf
from mechanics_vocab import statblock_density
print("orchestrator imports ok", fitz.__doc__ is not None, ocrmypdf.__name__)
print("mechanics_vocab ok", statblock_density("Armor Class: 15") > 0.0)
PY

  "${MARKER_VENV}/bin/python" - <<'PY'
import marker
print("marker imports ok", marker.__name__)
PY

  "${DOCLING_VENV}/bin/python" - <<'PY'
import docling
print("docling imports ok", docling.__name__)
PY

  "${PIXTRAL_VENV}/bin/python" - <<'PY'
import fitz
from PIL import Image
print("pixtral env imports ok", fitz.__doc__ is not None, Image.__name__)
PY

  ok "Smoke imports complete"
}

smoke_pipeline_scripts() {
  say "Running script-level smoke checks"
  mkdir -p "${SMOKE_DIR}"

  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/orchestrator.py" --help >/dev/null
  "${MARKER_VENV}/bin/python" "${SCRIPT_DIR}/marker_runner.py" --help >/dev/null
  "${DOCLING_VENV}/bin/python" "${SCRIPT_DIR}/docling_runner.py" --help >/dev/null
  "${PIXTRAL_VENV}/bin/python" "${SCRIPT_DIR}/surgeon.py" --help >/dev/null
  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/lorebook_splitter.py" --help >/dev/null
  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/estimate_runtime.py" --help >/dev/null
  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/table_fixer.py" --help >/dev/null
  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/quality_harness.py" --help >/dev/null
  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/pilot_benchmark.py" --help >/dev/null
  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/regression_suite.py" --help >/dev/null
  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/sqlite_queue.py" --help >/dev/null
  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/acceptance_corpus.py" --help >/dev/null
  "${ORCH_VENV}/bin/python" "${SCRIPT_DIR}/layout_analyzer.py" --help >/dev/null

  ok "Script help smoke checks complete"
}

write_runtime_env_file() {
  local env_file="${WORKSPACE_ROOT}/aether_forge.env"
  say "Writing env template to ${env_file}"
  cat > "${env_file}" <<ENV
# Aether Forge runtime environment template
INPUT_DIR=${WORKSPACE_ROOT}/ttrpg_input
OUTPUT_DIR=${OUTPUT_DIR}
MARKER_PYTHON=${MARKER_VENV}/bin/python3
DOCLING_PYTHON=${DOCLING_VENV}/bin/python3
OCRMYPDF_BIN=${ORCH_VENV}/bin/ocrmypdf
PIXTRAL_MODEL=mistralai/Pixtral-12B-2409
BATCH_MULTIPLIER=2
CHUNK_THRESHOLD=100
NUM_CHUNKS=2
MIN_CHARS_FOR_NATIVE=1000
WEIRD_CHAR_LIMIT=0.03
SCAN_THRESHOLD=50
MIN_MD_CHARS_PER_PAGE=150
REPAIR_BATCH=6
RENDER_DPI=180
MAX_PAGE_TOKENS=3072
ENFORCE_FULL_BOOK_REPAIR=0
BRIDGE_TIMEOUT_SEC=3600
BRIDGE_RETRIES=2
OCR_MODE=selective
SAMPLE_AND_RACE=0
ENV
  ok "Environment template generated"
}

print_summary() {
  cat <<MSG

Aether Forge build completed.

Next commands:
  source ${WORKSPACE_ROOT}/aether_forge.env
  ${ORCH_VENV}/bin/python3 ${SCRIPT_DIR}/orchestrator.py
  ${PIXTRAL_VENV}/bin/python3 ${SCRIPT_DIR}/surgeon.py
  ${ORCH_VENV}/bin/python3 ${SCRIPT_DIR}/lorebook_splitter.py \
    --input_root ${OUTPUT_DIR} \
    --output_jsonl ${OUTPUT_DIR}/lorebook_chunks.jsonl

Artifacts:
  venvs: ${VENVS_DIR}
  locks: ${WORKSPACE_ROOT}/*.lock
  output: ${OUTPUT_DIR}
MSG
}

main() {
  say "Building The Aether Forge (local-first architecture)..."
  check_prereqs
  reset_if_requested
  prepare_dirs
  apt_install

  create_venv "${ORCH_VENV}"
  install_orchestrator_deps

  create_venv "${MARKER_VENV}"
  install_marker_deps

  create_venv "${DOCLING_VENV}"
  install_docling_deps

  create_venv "${PIXTRAL_VENV}"
  install_pixtral_deps

  freeze_lockfiles
  write_runtime_env_file

  if [[ "${RUN_SMOKE}" == "1" ]]; then
    smoke_python_imports
    smoke_pipeline_scripts
  else
    warn "Skipping smoke checks (RUN_SMOKE=0)."
  fi

  print_summary
}

main "$@"
