# Conversion Run Integrity Validator Guide

## Purpose

`validate_conversion_run_integrity.py` exists to enforce strict packet/result/report integrity before aggregation and corpus-level continuation.

It detects malformed packets, duplicate IDs, missing prompt/result artifacts, unresolved placeholders, invalid lawful outcomes, stale backup artifacts, non-index result leakage, and canon-permission leakage patterns.

## Position in the pipeline

This validator sits after run initialization and packet/result generation, and before relying on aggregation outputs for governance decisions.

It complements existing schema/quality validation and audit steps by adding run-integrity checks across:

- run directory structure,
- packet index consistency,
- prompt/result pairing,
- result JSON semantic constraints,
- anti-canon-leakage language,
- report placeholder leakage,
- aggregation summary consistency.

## Boundary principles

- Extraction truth is not conversion permission.
- Conversion permission is not canon permission.
- Validator success does not mean canon approval.

Passing integrity validation only means the run artifacts are internally coherent enough for downstream review and aggregation workflows.

## Strict mode behavior

Run with:

`python scripts/handoff/validate_conversion_run_integrity.py --run-dir <RUN_DIR> --strict`

In strict mode, validation failures produce nonzero exit status and should block corpus-level continuation until repaired.

## Output contract

The validator emits JSON with:

- `valid`
- `strict`
- `run_dir`
- `checked_at`
- `error_count`
- `warning_count`
- `errors`
- `warnings`
- `summary`

Use `--output-json PATH` to persist the report.

## Why this supports the eventual ~1900-donor orchestrated run

The eventual single top-level orchestrated run must be resumable and fail safely. This validator supports that by failing early on integrity defects that would otherwise cause:

- silent data loss,
- mixed packet/result contamination,
- invalid aggregation statistics,
- unsafe canon-language leakage,
- unreliable continuation signals.

## What to do when strict mode fails

1. Treat failures as actionable queue items (extraction, packet planning/building, conversion-intake, validation, or review).
2. Repair artifacts at the source stage (do not patch downstream summaries as a substitute).
3. Re-run strict integrity validation.
4. Continue only when the run is valid.

## Step boundary note

Generated-report mojibake scanning is intentionally reserved for Step 8 and is not implemented in this Step 7 validator.
