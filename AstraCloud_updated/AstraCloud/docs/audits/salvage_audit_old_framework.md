# Salvage audit of legacy Astra framework

## Executive summary

The legacy zip is not trash. It is a **useful quarry** with a bad habit of pretending it is a cathedral.

The good news: several modules encode real project learning around routing, markdown-aware cleaning, deterministic table handling, stat block protection, lexicon extraction, prompt signatures, and postchecks.

The bad news: the framework is still fundamentally shaped around a **Windows + PowerShell + local backend + monolithic converter** worldview. That worldview should not survive the reboot.

## What was found

Top-level legacy assets include:

- PowerShell modules for routing, conversion, cleaning, tables, stat blocks, lexicon, scoring, and orchestration
- Python helper scripts for local HF backend emulation and postchecks
- Profile/config JSON files
- Logs and intermediate processing artifacts
- Internal design notes diagnosing markdown-first gaps

Observed artifact inventory from the extracted zip:

- `Processing/Astra_Chunks`: 2,581 chunk artifacts
- `Processing/JSON_Chunks`: 24 JSON chunk artifacts
- `Logs`: 2 logs totaling about 473 KB
- Main markdown processing artifacts for a Starfinder GM Core test run

## Salvage stance

### Keep and rewrite first

These are the highest-value assets to port into the new Python/cloud architecture:

- `AstraChunkRouter.ps1`
- `AstraSourceCleaner.ps1`
- `AstraBookClassifier.ps1`
- `AstraStatBlockBoundaryDetector.ps1`
- `AstraTablePreprocessor.ps1`
- `astra_postcheck.py`
- `AstraQualityScorerV2.ps1`
- `AstraLexicon.ps1`
- `AstraPromptSignatureHasher.ps1`

### Keep as concept/reference only

These hold useful ideas but should not be copied forward verbatim:

- `AstraConverter-v5.ps1`
- `AstraPassOneReformer.ps1`
- `AstraTableRefiner.ps1`
- `AstraPreFlightSwap.ps1`
- `AstraProfileExtensionLoader.ps1`
- `astra_hf_server.py`
- `AstraInlineFictionClassifier.ps1`
- analytics/audit scripts and later lorebook helpers
- profile/config JSON files
- architecture notes and upgrade plan docs

### Discard from the new architecture

These are legacy shell/orchestration pieces tied to the old operating model:

- `AstraMaster.ps1`
- `run_phase1.ps1`
- `run_phase2.ps1`
- local/Ollama-shaped orchestration assumptions embedded across the old launch flow

## Concrete issues observed

### 1. The legacy repo is monolithic where the new system must be modular

`AstraConverter-v5.ps1` is doing too much at once: profile loading, chunk heuristics, conversion flow, quality logic, cache behavior, and backend interaction. It is useful as an archaeology site, not as a foundation stone.

### 2. PowerShell compatibility hazards exist in critical scripts

`AstraTablePreprocessor.ps1` uses inline conditional assignment patterns such as:

- `$Profile = if (...) { ... } else { ... }`
- `$cleanExt = if (...) { ... } else { ... }`

Those are risky in Windows PowerShell 5.x and line up suspiciously well with the logged runtime failure where the preprocessor blew up with `The term 'if' is not recognized...`.

### 3. The logs confirm real failure modes worth preserving as test cases

The legacy `master_pipeline.log` shows:

- table preprocessor failure before conversion
- converter/profile parse failure during a Starfinder GM Core run
- local backend routing and markdown processing already under test

That means the logs are valuable not as living infrastructure, but as **failure fixtures**.

### 4. Markdown-awareness was already recognized as a structural gap

`Astra_V6_Markdown_First_Architecture_Analysis.md` is useful because it explicitly diagnoses dead OCR-era paths and insufficient markdown awareness across the old pipeline. That diagnosis should directly inform the new ingestion and chunk classification design.

## New repo actions already enacted

The following pieces have been created in the new cloud repo bootstrap:

- repo folder structure under `astra_ascension_cloud/`
- `configs/routing/routes.yaml`
- `configs/routing/chunk_classes.yaml`
- `configs/routing/escalation_policies.yaml`
- `src/astra_cloud/schemas/route.py`
- `src/astra_cloud/schemas/runlog.py`
- `docs/audits/salvage_manifest.csv`

## Recommended migration order

1. Port routing vocabulary and route decision schema.
2. Port chunk classification and markdown-aware normalization logic.
3. Port stat block and table guarding before any broad conversion work.
4. Port postcheck and quality scoring into validator primitives.
5. Port lexicon extraction/delta logic.
6. Only then build the cloud conversion worker around those contracts.
7. Revisit later analytics/distillation helpers after the spine is stable.

## Immediate next implementation targets

The next files to build should be:

- `src/astra_cloud/routing/classifier.py`
- `src/astra_cloud/routing/policies.py`
- `scripts/ingest/normalize_markdown.py`
- `scripts/chunking/classify_chunks.py`
- `scripts/validation/validate_structure.py`

## Bottom line

The salvage answer is not “keep the old framework” and not “throw everything away.”
It is:

**preserve the learned ideas, discard the old operating model, and rebuild the useful pieces as explicit Python modules inside a cloud-first spine.**
