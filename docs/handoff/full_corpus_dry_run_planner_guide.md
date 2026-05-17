# Full Corpus Dry-Run Planner Guide

## Why this planner exists

`plan_full_corpus_dry_run.py` provides a preflight planning pass for large donor corpora before extraction/conversion.

It builds a stable manifest, detects corpus-level risks, and produces reviewable reports without running extraction, OCR, conversion-intake, aggregation, or canon decisions.

## What it does not do

- It does **not** implement the full 1900-donor runner.
- It does **not** extract content.
- It does **not** run OCR.
- It does **not** invoke LLMs.
- It does **not** convert or canonize donor material.

Extraction truth is not conversion permission.

Conversion permission is not canon permission.

## How it supports future orchestration

The eventual single top-level ~1900-donor orchestrated run needs resumable, auditable input planning.

This planner supports that by producing:

- corpus manifest JSON/CSV,
- preflight issue lists,
- donor-family estimate summaries,
- repair-queue estimate summaries,
- suggested batch sizing guidance.

## Inputs and heuristic scope

The planner uses filesystem metadata and filename/path hints only.

Donor-family estimation is weak routing metadata, not doctrine truth.

Repair-queue estimation is preflight prediction, not extraction truth.

## Interaction with other layers

- Donor-family templates: help route files into later family-focused planning/review.
- Repair queues: flag likely risk lanes before extraction starts.
- Extraction lanes and packet planning: informed by preflight risks and estimates.
- Conversion-intake, aggregation, and review: explicitly downstream and not executed by dry-run.

## How to interpret common issues

- Duplicate files (name/hash): likely corpus hygiene issues; review for dedupe policy.
- Giant files: may require special extraction controls or timeout budgeting.
- Tiny/zero-byte files: likely corrupt/incomplete metadata or placeholder artifacts.
- Non-ASCII paths/very long paths: potential tooling/runtime portability risks.
- Unclassified donors: expected in early preflight; signals need for expanded template coverage.

## Before moving from dry-run to extraction

Review:

1. manifest completeness and file counts,
2. duplicate/hash clusters,
3. unsupported extensions,
4. likely scanned/image-heavy candidates,
5. donor-family estimate distribution,
6. repair-queue estimate concentrations,
7. batch-size proposal reasonableness.

Only after preflight review should actual extraction planning begin.
