# Aether Forge (v12)

Local-first, routed PDF-to-Markdown extraction for single-GPU corpora.

## Core lanes
- **Lane A**: PyMuPDF block-sorted extraction with page markers and deheader pass.
- **Lane B**: Marker bridge (chunked + retry + timeout + strict JSON validation).
- **Lane B2**: Docling bridge fallback (including chunk mode and table structure hinting).
- **Lane C**: Pixtral repair lane with adaptive prompt/DPI and atomic write promotion.

## Reliability upgrades
- Scored routing classifier (multi-column/table/sidebar/stat-block/image/scanned/donor-family features).
- Adaptive sampling and optional sample-and-race lane arbitration.
- Page-level audit with per-page reasons and surgical repair queueing.
- Reading-order, table-structure, stat-block continuity, header/footer repetition, glyph checks.
- Per-book manifests + per-page metadata sidecars + table-preservation sidecars.
- Selective OCR policy (`skip`/`redo`/`force`) and subprocess timeouts/retries.
- Repair merge via temporary artifact and atomic promotion.

## Production guarantees
- Page maps are trusted only when emitted from source-grounded page markers or page metadata.
- Markerless/chunk-only outputs are treated as **untrusted page truth** and should be rerouted or quarantined.
- Donor family is inferred from sampled content first, metadata second.
- OCR is page-selective; native-text pages are never force-OCR'd unless explicitly requested.
- Lane C supports high-detail repair with profile-aware rendering and tiled fallback for dense pages.
- Complex tables/forms may emit sidecars (and HTML render paths) when markdown would lose structure.

## New v12 toolchain
- `sqlite_queue.py`: durable SQLite queue/state backend for large runs.
- `table_fixer.py`: post-extraction table normalization and recovery.
- `quality_harness.py`: corpus quality scoring/reporting with page-level checks.
- `pilot_benchmark.py`: sample-run throughput calibration from real lane outcomes.
- `regression_suite.py`: synthetic acceptance/regression checks for extraction quality logic.
- `acceptance_corpus.py`: large rule-bank acceptance scanner for markdown artifact QA.

## Build and run
```bash
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
bash "$REPO_ROOT/build_forge.sh"
/workspace/venvs/orchestrator/bin/python3 "$REPO_ROOT/orchestrator.py"
/workspace/venvs/pixtral/bin/python3 "$REPO_ROOT/surgeon.py"
/workspace/venvs/orchestrator/bin/python3 "$REPO_ROOT/table_fixer.py" --help
/workspace/venvs/orchestrator/bin/python3 "$REPO_ROOT/quality_harness.py" --help
/workspace/venvs/orchestrator/bin/python3 "$REPO_ROOT/regression_suite.py" --report /workspace/ttrpg_output/logs/regression.json
```

## Runtime planning
```bash
python3 /workspace/Test/estimate_runtime.py --books 1895 --avg_pages 320
```

Use pilot outputs (`pilot_benchmark.py`) + manifests + quality reports to continuously tune throughput and lane-mix assumptions.
