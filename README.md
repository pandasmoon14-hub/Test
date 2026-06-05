# Astra Ascension

Astra Ascension is a doctrine-controlled TTRPG conversion and canon-distillation project, a schema-governed content and rules architecture, and a future deterministic backend runtime for persistent text-based TTRPG play. The repository currently contains doctrine, schema, extraction/handoff, and validation-hardening work, but the long-term project identity is not an extraction engine: extraction exists to produce reviewable evidence that can later be promoted, rejected, quarantined, or retained as source-local material under Astra doctrine.

## Current repository status

This repository is in a foundation-building stage:

- **Doctrine and roadmap alignment** define what Astra may own, what donors may pressure, and what must remain source-local.
- **Schema work** defines machine-checkable conversion records and review pathways.
- **Extraction/handoff tooling** prepares source-grounded packets for review and validation.
- **Validation hardening** protects page truth, routing, handoff packet integrity, and doctrine/registry consistency.
- **Runtime design remains future work** until doctrine, canon, schemas, and pilots satisfy the roadmap gates.

Aether Forge is the current extraction/handoff toolchain in this repository. It is useful developer infrastructure, not the whole Astra Ascension project. Extraction and conversion components may later be detached, archived, or replaced after corpus processing.

## Recommended GitHub About description

Recommended GitHub repo description:

> Doctrine-controlled TTRPG conversion, canon, schema, and deterministic backend-runtime architecture for Astra Ascension; extraction tooling is a temporary developer subsystem.

If the About field is too short, use:

> Backend-owned TTRPG runtime/canon/schema architecture for Astra Ascension; extraction tooling is temporary developer infrastructure.

## Architecture invariants

- **Doctrine first; schema second; pilot third; scale fourth; runtime later; training last.**
- **Conversion output is evidence, not canon.** Canon requires explicit promotion, conflict review, lexicon control, and source-local boundary checks.
- **Astra is model-interchangeable.** Astra may use any one interchangeable LLM, local or cloud, but no Astra subsystem may depend on that model as the holder of truth.
- **The LLM is not the game engine.** The LLM is only the player-facing narration, summarization, interpretation, and constrained proposal layer.
- **The backend runtime kernel owns truth.** Runtime state is not model memory.
- **The backend is authoritative.** The runtime kernel, schemas, generators, validators, event logs, memory system, retrieval system, persistence writers, and file/export writers are the game. The LLM is only the voice at the table.
- **Mature live play requires backend-owned state, dice, validation, persistence, context packets, and event commits.** Narration is allowed only inside the contracts provided by the backend.

## Phase map

1. **Doctrine spine**: establish Astra-native setting, advancement, action, world, asset, and conflict doctrine.
2. **Schema base**: define source-grounded conversion record structures and review metadata.
3. **Canon and lexicon governance**: promote only reviewed Astra material; quarantine or source-localize donor pressure.
4. **Controlled pilots and expansion batches**: validate doctrine and schemas before full-corpus processing.
5. **Runtime/backend doctrine**: design deterministic event kernel, entity state, command lifecycle, dice authority, context packets, hidden information, clocks, persistence, replay, and auditability.
6. **Live-play, training, and evaluation doctrine**: define adapter behavior, benchmarks, failure labels, and hard-fail boundaries after runtime authority exists.

## Current toolchain: Aether Forge extraction/handoff subsystem

The Aether Forge tooling currently present in this repo supports local-first, routed PDF-to-Markdown extraction for single-GPU corpora. It is a temporary and detachable developer subsystem whose outputs feed review, schema validation, handoff packets, and canon-candidate workflows.

### Core extraction lanes

- **Lane A**: PyMuPDF block-sorted extraction with page markers and deheader pass.
- **Lane B**: Marker bridge with chunking, retry, timeout, and strict JSON validation.
- **Lane B2**: Docling bridge fallback, including chunk mode and table-structure hinting.
- **Lane C**: Pixtral repair lane with adaptive prompt/DPI and atomic write promotion.

### Reliability and validation features

- Scored routing classifier for multi-column, table, sidebar, stat-block, image, scanned, and donor-family features.
- Adaptive sampling and optional sample-and-race lane arbitration.
- Page-level audit with per-page reasons and surgical repair queueing.
- Reading-order, table-structure, stat-block continuity, header/footer repetition, and glyph checks.
- Per-book manifests, per-page metadata sidecars, and table-preservation sidecars.
- Selective OCR policy (`skip`/`redo`/`force`) and subprocess timeouts/retries.
- Repair merge via temporary artifact and atomic promotion.

### Developer tooling currently present in this repo

- `sqlite_queue.py`: durable SQLite queue/state backend for large extraction runs.
- `table_fixer.py`: post-extraction table normalization and recovery.
- `quality_harness.py`: corpus quality scoring/reporting with page-level checks.
- `pilot_benchmark.py`: sample-run throughput calibration from real lane outcomes.
- `regression_suite.py`: synthetic acceptance/regression checks for extraction quality logic.
- `acceptance_corpus.py`: large rule-bank acceptance scanner for Markdown artifact QA.

### Build and extraction/handoff commands

```bash
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
bash "$REPO_ROOT/build_forge.sh"
/workspace/venvs/orchestrator/bin/python3 "$REPO_ROOT/orchestrator.py"
/workspace/venvs/pixtral/bin/python3 "$REPO_ROOT/surgeon.py"
/workspace/venvs/orchestrator/bin/python3 "$REPO_ROOT/table_fixer.py" --help
/workspace/venvs/orchestrator/bin/python3 "$REPO_ROOT/quality_harness.py" --help
/workspace/venvs/orchestrator/bin/python3 "$REPO_ROOT/regression_suite.py" --report /workspace/ttrpg_output/logs/regression.json
```

### Extraction runtime planning

```bash
python3 /workspace/Test/estimate_runtime.py --books 1895 --avg_pages 320
```

Use pilot outputs (`pilot_benchmark.py`), manifests, and quality reports to continuously tune throughput and lane-mix assumptions. These extraction estimates are operational planning inputs, not runtime doctrine.

## What the backend will own

The future Astra runtime must be backend-owned and deterministic. The backend will own, at minimum:

- truth, campaign state, entity state, and authoritative memory records;
- dice/RNG authority, clocks, consequences, and event commits;
- command lifecycle, intermediate representation, validation, and state-delta application;
- schemas, generators, templates, provenance, generated-content records, and validators;
- context-packet compilation, retrieval, hidden-information partitioning, and persistence;
- event logs, state stores, replay, migration, hash verification, and file/export writers.

Markdown, JSON, YAML, or other files may be materialized exports, audit artifacts, or handoff products. They are not the source of truth for mature live play unless the backend explicitly commits them through schema, validation, provenance, and event/state pathways.

## What the LLM may and may not do

The LLM may:

- narrate committed backend outcomes to players;
- summarize visible facts and validated dialogue history;
- interpret player intent into constrained proposals or command drafts;
- ask clarifying questions;
- provide non-authoritative flavor when clearly labeled as flavor or proposal.

The LLM may not:

- own truth, campaign state, dice, clocks, hidden state, or persistence;
- directly mutate state or write files as authoritative records;
- promote conversion output to canon;
- decide that a generated creature, NPC, faction, location, hazard, item, rumor, mission, or relationship is durable without backend validation and commit;
- leak hidden information, invent rewards or injuries, or make unvalidated consequence commits.

## Current roadmap priorities

- Keep Astra Ascension's public identity centered on doctrine, canon, schema, deterministic runtime architecture, and model-interchangeable live play.
- Preserve Aether Forge as subordinate extraction/handoff tooling while it remains useful.
- Harden doctrine and registry tracking so conversion, canon, runtime, and live-play behavior stay separated.
- Add and enforce backend-first runtime invariants before any runtime kernel implementation begins.
- Ensure generated content, knowledge claims, dialogue transcripts, retrieval, persistence, and narration validation become explicit future runtime control areas.

## Development notes / tests

Run the focused doctrine/registry validation tests when changing roadmap or registry files:

```bash
python3 -m pytest tests/test_astra_doctrine_registry.py
```

Run the broader suite when changing extraction, handoff, schemas, or validation logic:

```bash
python3 -m pytest
```
