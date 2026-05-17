# Full Corpus Dry-Run Planner Guide

## Why this planner exists

`plan_full_corpus_dry_run.py` provides preflight planning for large donor corpora before extraction.

It generates an immediately reviewable dry-run manifest/report so teams can triage risks and routing gaps before a full orchestrated run.

## Non-goals

This planner does **not**:

- extract content,
- run OCR,
- invoke LLMs,
- run conversion-intake,
- aggregate conversion outputs,
- canonize donor material.

Extraction truth is not conversion permission.

Conversion permission is not canon permission.

## How Step 10 improves usability

The dry-run report now includes:

- run summary,
- issue counts by issue code,
- donor-family candidate counts,
- confidence counts,
- repair-queue candidate counts,
- top unclassified file sample,
- top unusually large file sample,
- top very long path sample,
- top non-ASCII path sample,
- next-step recommendations.

## CSV usability for PowerShell grouping

Outputs remain backward compatible while improving grouping clarity:

- `full_corpus_preflight_issues.csv` keeps `issue_code` and adds alias-friendly shape.
- `full_corpus_donor_family_estimates.csv` keeps `donor_family_candidates`, `confidence`, `repair_queue_candidates` and includes aliases for easy grouping.

These columns are intended for quick `Group-Object` workflows.

## Donor-family routing refinement

Filename/path-only heuristics were expanded across broad families (for example d20 fantasy, sci-fi, adventure, setting, bestiary, random-table, spell/power, gear/catalog, cyberpunk, traveller/starship, narrative/aspect, forged/playbook, OSR, toolkit).

These estimates are weak routing metadata only and may include multiple candidates per file.

Confidence semantics:

- `high`: strong explicit match patterns,
- `medium`: normal keyword match patterns,
- `low`: fallback/unclassified.

## Interaction with other layers

- Donor-family templates: preflight routing candidates for later packet planning.
- Repair queues: preflight risk predictions before extraction.
- Extraction lanes: informed by likely scanned/map/statblock/table pressure.
- Packet planning/conversion-intake/aggregation/review: downstream phases; not executed by this planner.

## How to interpret key issues

- Duplicate names/hashes: dedupe and source hygiene review.
- Giant files: likely runtime/budget pressure.
- Tiny/zero-byte files: likely corruption/placeholders.
- Non-ASCII/long paths: portability and tooling risk.
- Unclassified donors: expected routing gap signal; improve heuristics/templates before extraction.

## Before moving to real extraction

Review:

1. issue concentration and top risk clusters,
2. donor-family distribution and unclassified share,
3. repair-queue estimate concentration,
4. large-file and path portability risk,
5. proposed batch sizes and sequencing.

Only then proceed to extraction packet planning.
