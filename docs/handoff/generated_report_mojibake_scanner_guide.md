# Generated Report Mojibake Scanner Guide

## Purpose

`scan_generated_report_mojibake.py` checks generated report artifacts for mojibake/encoding corruption before batch continuation.

Report-layer mojibake matters because it can corrupt status summaries, confidence lines, tables, and review outputs used for governance decisions.

## Generated-report corruption vs source-text extraction corruption

- **Generated-report corruption** is a tooling output defect and should be treated as a pipeline quality failure.
- **Source-text extraction corruption** can be legitimate evidence of source extraction quality problems and may appear in quoted examples/snippets.

This scanner distinguishes those cases via classification:

- `generated_scaffold_mojibake`
- `likely_source_text_mojibake`
- `ambiguous_mojibake`

## Relationship to Step 6 and Step 7

- Step 6 extraction repair queues route extraction defects (OCR, table flattening, statblock under-parse, etc.).
- Step 7 run-integrity validator enforces packet/result/report structural integrity.
- Step 8 scanner adds report-layer encoding integrity checks for generated markdown/csv/json/txt outputs.

## Strict behavior

In strict mode:

- `generated_scaffold_mojibake` fails.
- `likely_source_text_mojibake` warns when `--allow-source-examples` is set, otherwise fails.
- `ambiguous_mojibake` fails unless `--allow-source-examples` is set and the content appears under source/example sections.

## CLI

- `--path <file-or-dir>`
- `--strict`
- `--output-json <path>`
- `--include "*.md" "*.csv" "*.json"` (defaults include `.md/.csv/.json/.txt`)
- `--allow-source-examples`

## Governance boundaries

- Scanner success does not mean canon approval.
- Extraction truth is not conversion permission.
- Conversion permission is not canon permission.

## Full-corpus readiness impact

The eventual single top-level ~1900-donor orchestrated run depends on trustworthy generated reports.

This scanner reduces risk of silent encoding corruption in corpus-scale reporting and supports fail-safe resumability with explicit findings.
