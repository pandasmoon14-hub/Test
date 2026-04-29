# Aether Forge v13 Stabilization Notes

## Run tests
`pytest -q`

## Generate fixtures
`python3 tests/fixtures/generate_fixture_pdfs.py`

## Pilot extraction (10-20 books)
`INPUT_DIR=/path/to/pilot OUTPUT_DIR=/workspace/ttrpg_output FORCE_LANE=A python3 orchestrator.py --strict_page_truth`

## Validate outputs
`python3 validate_outputs.py --output-dir /workspace/ttrpg_output --strict`

## Resume run
`INPUT_DIR=/path/to/pilot OUTPUT_DIR=/workspace/ttrpg_output python3 orchestrator.py --resume --strict_page_truth`

## strict_audit.json
Per-book coverage and artifact accounting. Fails on missing page truth rows, missing page markers, duplicate page numbers, or mismatched page counts.

## astra_handoff_manifest.json
Extraction-only readiness/provenance manifest. Does not perform Astra rules conversion.

## OCR truthfulness
Manifest reports `whole_book_ocr_used` based on current mode. Selective per-page OCR remains a future hardening task.
