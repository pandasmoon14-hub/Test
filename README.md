# Astra Ascension

Astra Ascension is a doctrine-controlled TTRPG conversion and canon-distillation project, a schema-governed content and rules architecture, and a future deterministic backend runtime for persistent text-based TTRPG play. The repository currently contains doctrine, schema, extraction/handoff, and validation-hardening work, but the long-term project identity is not an extraction engine: extraction exists to produce reviewable evidence that can later be promoted, rejected, quarantined, or retained as source-local material under Astra doctrine.

The extraction and conversion toolchain is strictly outside the runtime trust boundary. It must remain detachable from the runtime codebase, runtime package, runtime data stores, model context, and player-facing outputs. Runtime-consumable material must be promoted through a one-way canon boundary into newly identified Astra-native artifacts that contain no donor names, source paths, page references, extraction metadata, conversion records, mapping rationale, or other origin-revealing fields.

## Current repository status

This repository is in a foundation-building stage:

- **Doctrine and roadmap alignment** define what Astra may own, what donors may pressure, and what must remain source-local.
- **Schema work** defines machine-checkable conversion records and review pathways.
- **Extraction/handoff tooling** prepares source-grounded packets for review and validation.
- **Validation hardening** protects page truth, routing, handoff packet integrity, and doctrine/registry consistency.
- **Runtime design remains future work** until doctrine, canon, schemas, and pilots satisfy the roadmap gates.
- **Runtime-origin separation is mandatory**: extraction and conversion artifacts are authoring evidence only and may not become runtime dependencies or runtime-readable provenance.

Aether Forge is the current extraction/handoff toolchain in this repository. It is useful developer infrastructure, not the whole Astra Ascension project. Extraction and conversion components may later be detached, archived, or replaced after corpus processing.

## Recommended GitHub About description

Recommended GitHub repo description:

> Doctrine-controlled TTRPG conversion, canon, schema, and deterministic backend-runtime architecture for Astra Ascension; extraction tooling is a temporary developer subsystem.

If the About field is too short, use:

> Backend-owned TTRPG runtime/canon/schema architecture for Astra Ascension; extraction tooling is temporary developer infrastructure.

## Architecture invariants

- **Doctrine first; schema second; pilot third; scale fourth; runtime later; training last.**
- **Conversion output is evidence, not canon.** Canon requires explicit promotion, conflict review, lexicon control, and source-local boundary checks.
- **Extraction and conversion end before runtime begins.** Runtime code may not import, call, query, bundle, or depend on extraction or conversion tooling.
- **Canon promotion is one-way and identity-breaking.** A promoted runtime artifact receives a new Astra-native identity and a sanitized Astra-native payload; conversion-record identity does not cross the boundary.
- **Runtime is origin-blind.** Runtime-accessible schemas and payloads may not expose donor titles, authors, publishers, filenames, paths, page or line references, OCR or extraction details, conversion IDs, mapping notes, donor-family labels, provenance tags, or source-derived namespaces.
- **Offline provenance is retained but isolated.** Source lineage remains only in an access-controlled governance ledger for audit, conflict review, rights review, and reproducibility. It is not shipped to, imported by, queried by, or disclosed through runtime.
- **Astra is model-interchangeable.** Astra may use any one interchangeable LLM, local or cloud, but no Astra subsystem may depend on that model as the holder of truth.
- **The LLM is not the game engine.** The LLM is only the player-facing narration, summarization, interpretation, and constrained proposal layer.
- **The backend runtime kernel owns truth.** Runtime state is not model memory.
- **The backend is authoritative.** The runtime kernel, schemas, generators, validators, event logs, memory system, retrieval system, persistence writers, and file/export writers are the game. The LLM is only the voice at the table.
- **Mature live play requires backend-owned state, dice, validation, persistence, context packets, and event commits.** Narration is allowed only inside the contracts provided by the backend.

## Extraction/conversion–runtime firewall

The project uses a one-way promotion path:

```text
source files and extraction evidence
→ conversion candidates and review records
→ doctrine, conflict, lexicon, originality, and rights review
→ explicit canon promotion
→ sanitized Astra-native canonical artifact with a new identity
→ runtime package and campaign state
```

The reverse path does not exist. Runtime systems must not inspect conversion packets, extraction manifests, donor mappings, page truth, source citations, or offline provenance ledgers.

### Runtime-forbidden origin data

Runtime code, runtime schemas, packaged content, persistence records, retrieval indexes, context packets, model prompts, logs exposed to live-play tooling, and player-facing exports must not contain:

- donor or source names, titles, authors, publishers, product identifiers, or external namespace labels;
- source filenames, directory paths, archive names, page numbers, line references, OCR state, extraction lane, or page-truth metadata;
- conversion intake IDs, mapping ledgers, lawful-outcome notes, rejected-import records, quarantine rationales, or canon-promotion deliberation;
- copied source passages, source-format stat blocks, source-specific boilerplate, or attribution-like text unless separately authorized as original Astra canon;
- stable IDs, hashes, or tokens derived from source or conversion identifiers in a way that permits runtime-to-source correlation.

### Runtime-allowed provenance

Runtime may retain only Astra-native lifecycle provenance, such as:

- Astra canonical artifact ID and version;
- Astra module or rules-family identity;
- campaign creation, installation, migration, event, and mutation records;
- runtime generator and validator versions;
- runtime audit and replay evidence.

These records describe the artifact’s life inside Astra. They must not reveal its pre-canon extraction or conversion history.

### Offline lineage ledger

The project must retain a separate, access-controlled, non-runtime lineage ledger that records source evidence, conversion history, review decisions, rights status, and canon-promotion lineage. This ledger exists for governance and auditability and must not be bundled into runtime builds, indexed by runtime retrieval, exposed to the LLM, or included in player-facing exports.

This separation is not permission to bypass originality, licensing, attribution, or rights review. Material that cannot be lawfully and coherently promoted as Astra-native canon must remain quarantined, rejected, or confined to the offline conversion environment.

The controlling doctrine is `docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md`.

## Phase map

1. **Doctrine spine**: establish Astra-native setting, advancement, action, world, asset, and conflict doctrine.
2. **Schema base**: define source-grounded conversion record structures and review metadata.
3. **Canon and lexicon governance**: promote only reviewed Astra material; quarantine or source-localize donor pressure.
4. **Controlled pilots and expansion batches**: validate doctrine and schemas before full-corpus processing.
5. **Runtime/backend doctrine**: design deterministic event kernel, entity state, command lifecycle, dice authority, context packets, hidden information, clocks, persistence, replay, and auditability.
6. **Live-play, training, and evaluation doctrine**: define adapter behavior, benchmarks, failure labels, and hard-fail boundaries after runtime authority exists.

## Current toolchain: Aether Forge extraction/handoff subsystem

The Aether Forge tooling currently present in this repo supports local-first, routed PDF-to-Markdown extraction for single-GPU corpora. It is a temporary and detachable developer subsystem whose outputs feed review, schema validation, handoff packets, and canon-candidate workflows.

Aether Forge and all conversion-stage tooling are prohibited runtime dependencies. Their packages, manifests, queues, temporary artifacts, provenance ledgers, and identifiers must not be imported into or deployed with the Astra runtime.

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
- schemas, generators, templates, Astra-native canonical provenance, generated-content records, and validators;
- context-packet compilation, retrieval, hidden-information partitioning, and persistence;
- event logs, state stores, replay, migration, hash verification, and file/export writers.

The runtime backend must not own or access extraction provenance, donor lineage, conversion ledgers, source-page evidence, or canon-promotion deliberation.

Markdown, JSON, YAML, or other files may be materialized exports, audit artifacts, or handoff products. They are not the source of truth for mature live play unless the backend explicitly commits them through schema, validation, Astra-native provenance, and event/state pathways.

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
- access extraction or conversion artifacts, donor provenance, source mappings, or offline lineage ledgers;
- promote conversion output to canon;
- decide that a generated creature, NPC, faction, location, hazard, item, rumor, mission, or relationship is durable without backend validation and commit;
- leak hidden information, invent rewards or injuries, or make unvalidated consequence commits.

## Current roadmap priorities

- Keep Astra Ascension's public identity centered on doctrine, canon, schema, deterministic runtime architecture, and model-interchangeable live play.
- Preserve Aether Forge as subordinate extraction/handoff tooling while it remains useful.
- Enforce a one-way sanitized canon-promotion boundary so runtime remains independent of extraction, conversion, and donor provenance.
- Harden doctrine and registry tracking so conversion, canon, runtime, and live-play behavior stay separated.
- Add and enforce backend-first runtime invariants before any runtime kernel implementation begins.
- Ensure generated content, knowledge claims, dialogue transcripts, retrieval, persistence, and narration validation become explicit future runtime control areas.

## Development notes / tests

Install the development/test dependencies before running validation commands. Doctrine registry validation requires PyYAML from `requirements-dev.txt`; if a local environment cannot download packages because of network or package-index restrictions, make PyYAML available by another approved local mechanism before treating registry validation as runnable.

```bash
python3 -m pip install -r requirements-dev.txt
```

Run the focused doctrine/registry validation tests when changing roadmap or registry files:

```bash
python3 -m pytest tests/test_astra_doctrine_registry.py
python3 -m pytest tests/test_conversion_runtime_origin_firewall.py
```

Run the broader suite when changing extraction, handoff, schemas, or validation logic:

```bash
python3 -m pytest
```
