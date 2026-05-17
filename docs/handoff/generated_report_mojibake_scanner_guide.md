# Generated Report Mojibake Scanner Guide

## Purpose

`scan_generated_report_mojibake.py` detects mojibake in generated report artifacts before continuation.

It distinguishes **generated scaffold corruption** from **source-derived payload text**.

## Strict policy

- `generated_scaffold_mojibake` is a strict failure.
- `likely_source_text_mojibake` is warning-level with `--allow-source-examples`.
- `ambiguous_mojibake` fails unless it is recognized as source-derived under `--allow-source-examples`.

## Generated scaffold zones (must fail)

Examples:

- Markdown headings/report titles/section labels
- Run Summary lines
- Confidence range lines
- Packets total lines
- Result status counts lines
- Lawful outcome counts lines
- Generated table headers
- CSV headers
- JSON keys

## Source-derived payload zones (warn with --allow-source-examples)

Examples:

- Markdown packet/example bullets like `- `packet_id` - ...` (including indented variants)
- Doctrine pressure/source-local/quarantine/rejected import/mapping example payload rows
- CSV data rows with donor/source sample text
- JSON payload values for donor/source/rationale/notes/example/reviewer/conversion fields

Batch 001 aggregation outputs can contain source-derived mojibake in payload text. The scanner should preserve this as extraction evidence (warnings) while still failing true scaffold corruption.

## Relationship to Step 6 and Step 7

- Step 6 routes extraction defects via repair queues.
- Step 7 validates run integrity structure.
- Step 8 validates report-layer encoding integrity.

## CLI

- `--path <file-or-dir>`
- `--strict`
- `--allow-source-examples`
- `--include` globs (default `*.md *.csv *.json *.txt`)
- `--output-json PATH`

## Governance boundaries

- Scanner success does not mean canon approval.
- Extraction truth is not conversion permission.
- Conversion permission is not canon permission.
