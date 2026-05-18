# Full Corpus Extraction Plan Guide

## Purpose

`build_full_corpus_extraction_plan.py` composes a reviewable extraction plan from dry-run, preflight-review, and readiness-gate outputs.

It is planning/reporting only for the eventual single 1917-file orchestrated run.

## Scope boundaries

This step does not:

- run extraction,
- run OCR,
- invoke LLMs,
- build packets,
- convert donor content,
- canonize donor content.

Dry-run routing metadata is not extraction truth.

Extraction planning is not extraction truth.

Extraction truth is not conversion permission.

Conversion permission is not canon permission.

## Inputs

- Dry-run artifacts (manifest/issues/family estimates/report)
- Preflight review artifacts (summary/report/triage/clusters/optional overlay)
- Readiness gate artifacts (summary/report/checks/next action plan)

## What it builds

Per supported file, one planning record including:

- lane assignment,
- wave assignment,
- donor-family confidence,
- issue and repair-queue metadata,
- review-required flags,
- optional overlay-derived tentative routing suggestions.

## Lanes

- lane_a_standard_native_candidate
- lane_b_large_or_layout_risk
- lane_c_visual_map_or_scan_review
- lane_d_table_statblock_catalog_risk
- lane_e_manual_review_hold

## Waves

- wave_00_manual_triage
- wave_01_pilot_review_batch
- wave_02_donor_family_template_batch
- wave_03_mixed_pressure_batch
- wave_04_full_corpus_orchestrated_run

## Outputs

- `full_corpus_extraction_plan_manifest.json`
- `full_corpus_extraction_plan_manifest.csv`
- `full_corpus_extraction_batches.csv`
- `full_corpus_extraction_lane_summary.csv`
- `full_corpus_extraction_review_queue.csv`
- `full_corpus_extraction_plan_report.md`
- `full_corpus_extraction_plan_summary.json`

## Overlay behavior

When `--use-routing-overlay` is enabled and overlay proposal exists:

- overlay suggestions are tentative only,
- applied only to unclassified donor-family rows,
- review remains required for overlay-applied records.
