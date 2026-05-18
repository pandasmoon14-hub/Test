# Full Corpus Readiness Gate Guide

## Purpose

`validate_full_corpus_readiness_gate.py` is the final readiness validation/reporting layer before full-corpus extraction planning.

It verifies that dry-run and preflight review infrastructure is present, coherent, and review-ready.

## Boundaries

This gate does not run extraction, OCR, conversion, or canon promotion.

- Dry-run routing metadata is not extraction truth.
- Extraction truth is not conversion permission.
- Conversion permission is not canon permission.

## Inputs

From dry-run and preflight review directories:

- dry-run manifest/report CSV/JSON artifacts
- preflight review summary/report/triage/clusters
- optional routing overlay proposal YAML

## Checks

The gate reports pass/warn/fail for:

- dry-run validity and parseability
- preflight review validity and parseability
- strict error state
- supported-file baseline
- issue triage presence
- repair queue estimate presence
- unclassified cluster reporting
- routing overlay presence (optional or required)
- separation reminders
- canon-language safety
- no-extraction behavior of the gate itself

## Thresholds

Unclassified counts are warnings by default.

`--allow-unclassified-threshold` can enforce strict failure when exceeded.

Use this to block progression only when policy requires tighter routing maturity.

## Outputs

- `full_corpus_readiness_gate_report.md`
- `full_corpus_readiness_gate_summary.json`
- `full_corpus_readiness_gate_checks.csv`
- `full_corpus_next_action_plan.md`

Readiness status values:

- `ready`
- `ready_with_warnings`
- `blocked`
