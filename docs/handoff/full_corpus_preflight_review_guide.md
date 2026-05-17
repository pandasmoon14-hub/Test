# Full Corpus Preflight Review Guide

## Purpose

`review_full_corpus_preflight.py` reviews Step 10 dry-run outputs and produces triage + routing overlay proposals for large corpus readiness.

This is a review/refinement layer only.

## Scope boundaries

This step does not run extraction, OCR, conversion, or canon workflows.

- Dry-run routing metadata is not extraction truth.
- Extraction truth is not conversion permission.
- Conversion permission is not canon permission.

## Inputs

Expected Step 10 dry-run inputs:

- `full_corpus_dry_run_manifest.json`
- `full_corpus_dry_run_manifest.csv`
- `full_corpus_preflight_issues.csv`
- `full_corpus_donor_family_estimates.csv`
- optional `full_corpus_dry_run_report.md`

## Outputs

- `full_corpus_preflight_review_report.md`
- `full_corpus_unclassified_clusters.csv`
- `full_corpus_issue_triage.csv`
- `full_corpus_preflight_review_summary.json`
- optional `donor_family_routing_overlay_proposal.yaml`

## What it analyzes

1. Dry-run artifact integrity and parseability.
2. Issue triage counts by code/severity.
3. Unclassified donor routing clusters from filename/path patterns.
4. Overlay proposal records for recurring unclassified series.

## Overlay proposal semantics

Overlay records are review proposals, not authoritative doctrine.

Each record includes pattern id, match terms, suggested donor-family candidates, confidence hint, rationale, sample files, and `review_required: true`.

## Readiness interpretation

Use this review to decide whether the corpus is ready to move from dry-run planning into extraction packet planning.

High unclassified clusters or concentrated issue groups indicate routing/template refinement work before extraction.
