# Astra Ascension / Aether Forge — Project Context for Claude Code

You are working inside the Aether Forge repository, the extraction and
handoff-contract machinery for a larger project called Astra Ascension.

This file is the per-session context surface. Deeper references:
- `docs/project/master_brief_v0_1.md` — full project brief
- `docs/operations/current_decisions_log_v0_1.md` — append-only decisions log
- `docs/architecture/runtime/` — long-term runtime vision (not active work)
- `docs/handoff/` — the conversion handoff contract docs (active)

When this file and the canonical docs disagree, the canonical docs win.
When you make a non-obvious decision worth preserving, append it to the
decisions log using the decision / reason / implication / revisit-trigger
format.

---

## What this project is

Astra Ascension is a doctrine-governed TTRPG conversion and runtime
ecosystem. The donor corpus is large (target ~1,900–2,000 TTRPG PDFs,
legally owned or SRD/OGL/ORC-licensed). The goal is to ingest, extract,
normalize, convert, and eventually consolidate that material into a
coherent Astra-native rules-and-setting framework, then drive a
deterministic persistent-world TTRPG runtime that uses LLMs for
interpretation and narration but never for state.

This repo is **Aether Forge**: the extraction + handoff pipeline.
It is not the conversion brain, and it is not the runtime.

---

## Non-negotiable separations

These are foundational. Do not collapse them.

1. **Extraction truth ≠ conversion permission ≠ canon permission.**
   A page can extract cleanly and still be unsafe for conversion.
   A packet can be conversion-usable and still blocked from canon.
2. **Donor content is not live-play authority.**
   Donors provide pressure, variants, and source-local material —
   never hidden law.
3. **LLMs do not mutate state.** Ever. Prose is downstream of state,
   not its source. LLMs propose; the backend validates and commits.
4. **Aether Forge ≠ Astra Conversion ≠ Astra Runtime.**
   Don't merge their concerns even when convenient.

---

## Current stage: Step 10B (conversion-intake pilot)

Active run:
`C:\AetherForgeRuns\_active\handoff_step10_conversion_intake_run_v0_1`

Loop being proved:
packet bundle → conversion memo → result Markdown → scaffolded JSON →
validation → report

Pilot scope: 12 selected packets covering different donor pressures
(mechanics prose, random tables, adventure sites, statblocks, maps,
spells/powers, etc.). Not the whole corpus. Not scaling until the loop
is clean.

Current state (as of last session):
- 3 packets drafted, 9 placeholders.
- Validation with `--allow-placeholders` returns valid.
- Pressure types completed: Fate mechanics, Random Tables, Pathfinder
  adventure site.

Immediate next technical task: improve
`scripts/handoff/scaffold_conversion_intake_json.py` so it preserves
mapping-ledger rows, lettered/bulleted inventory items, source-local
retentions, rejected imports, canon candidate notes, and confidence
values. The current scaffolder is schema-valid but lossy.

---

## Lawful outcomes (mandatory for every donor construct)

Every donor construct identified in a conversion-intake memo must
receive exactly one:

- `direct Astra mapping`
- `normalized Astra mapping`
- `source-local retained construct`
- `quarantined construct pending later doctrine`
- `escalated doctrine problem`

No floating "maybe useful later." No decorative Astra-sounding invention.

---

## Repo layout (this repository)

- `scripts/handoff/` — handoff pipeline scripts
- `schemas/handoff/` — JSON schemas for handoff artifacts
- `docs/handoff/` — handoff contract documents
- `docs/project/` — master brief, project-level docs
- `docs/operations/` — decisions log, operational notes
- `docs/architecture/runtime/` — long-term runtime vision (not active)
- `tests/` — pytest suite
- `tests/fixtures/` — fixture PDFs and generators

Key handoff scripts already implemented:
- `build_handoff_packet.py`
- `build_handoff_packet_batch.py`
- `generate_handoff_packet_plan.py`
- `validate_handoff_packet.py`
- `validate_handoff_packet_batch.py`
- `report_handoff_plan.py`
- `init_conversion_intake_run.py`
- `validate_conversion_intake_results.py`
- `report_conversion_intake_results.py`
- `scaffold_conversion_intake_json.py`

---

## Run artifact layout (outside the repo)

Run artifacts live at `C:\AetherForgeRuns\`, intentionally separate
from the code repo. Organized as:

- `_active\` — current working runs (e.g. `handoff_step10_conversion_intake_run_v0_1\`)
- `snapshots\` — all `*_snapshot.zip` frozen milestones
- `plans\` — packet plan JSON files
- `helpers\` — one-off `make_*.py` bundle/sample scripts
- `reports\` — review CSVs, candidate rankings, content quality samples
- `fixtures\` — `fixture_input`, `fixture_output`
- `pilots\pilot20\` — 17-book pilot variants
- `pilots\pilot50\` — 50-book pilot scaffolding
- `pilots\real1\` — single-donor gates
- `pilots\real3\` — three-donor gates
- `pilots\ocr_gates\` — OCR gate 1 and gate 2 runs
- `packets\` — built handoff packets and review outputs
- `handoff_test_3\` — original conversion handoff test 3 packets and results

Notes on the helpers folder: the `make_*.py` scripts under
`C:\AetherForgeRuns\helpers\` (e.g. `make_fate_bundle.py`,
`make_random_tables_bundle.py`, `make_pathfinder_adventure_site_bundle.py`,
`make_content_quality_samples*.py`) are one-off scripts that built
specific bundles for the current pilot. They are not under version
control. Their hardcoded paths still reference the pre-reorganization
layout. When this functionality is needed again, prefer creating a
parameterized script under `scripts/handoff/` rather than editing the
old helpers.

---

## Repo conventions

- Python 3.14 on the local machine. Code should remain compatible.
- Tests: pytest. Run with `python -m pytest -q` from repo root.
- All handoff schemas live under `schemas/handoff/`.
- All handoff scripts live under `scripts/handoff/`.
- All handoff docs live under `docs/handoff/`.
- Plan files (JSON) must be readable with `utf-8-sig` to tolerate BOM
  (PowerShell-created JSON often has one).
- Code repo lives at `C:\Dev\AetherForge` (outside OneDrive).
- Run artifacts live at `C:\AetherForgeRuns\` (separate from repo).
- Avoid OneDrive paths for either; OneDrive sync causes pytest cache
  permission errors and file-lock issues on large folders.

---

## What not to do

- **Do not call an LLM from packet builders, validators, or report
  scripts.** Those are deterministic.
- **Do not promote canon from drafted conversion-intake memos.**
  Memos are intake-stage analysis, not canon.
- **Do not bypass schema validation** to make a test pass. Fix the
  schema or fix the producer; don't silence the validator.
- **Do not assume Marker/Docling are available.** AUTO routing should
  fall back to Lane A and record the fallback. This is by design.
- **Do not run forced OCR by default.** `OCR_MODE=skip` is the safe
  pilot setting. Force OCR only when explicitly testing OCR behavior.
- **Do not scale to the full corpus.** Pilot batches only until the
  handoff contract is frozen at v0.2.
- **Do not modify `orchestrator.py`, extraction logic, or OCR
  behavior** when the task is handoff/scaffolder work. Those are
  separate tracks.
- **Do not let donor terminology become Astra doctrine** without
  explicit lexicon review.
- **Do not put run artifacts inside the repo.** They belong under
  `C:\AetherForgeRuns\`.

---

## Local environment

- Windows 11, Intel i7-14700F, 32 GB RAM, RTX 4060 8 GB VRAM, 1.8 TB SSD.
- Local LLM inference is smoke-test scale only (≤8B quantized).
- Larger conversion models (Qwen3-32B+) belong on rented GPU, not
  local. Do not design workflows around local 32B+ assumptions.

---

## Working style

- When asked to make a change, run the existing test suite first to
  establish baseline, then make the change, then re-run tests.
- When fixing a failing test, first determine whether the test is
  wrong or the code is wrong. Don't reflexively weaken tests.
- Snapshot major milestones as zip archives under
  `C:\AetherForgeRuns\snapshots\`.
- When you encounter a non-obvious decision worth preserving, append
  it to `docs/operations/current_decisions_log_v0_1.md` using the
  decision / reason / implication / revisit-trigger format.
- Honest progress reports beat optimistic ones. If something only
  half-works, say so.
- When generating PowerShell commands for the user, paste only the
  command lines — not surrounding prose, `PS C:\>` prompts, or `>>`
  continuation markers. Past sessions have failed when the user
  accidentally pasted prompt text back into the shell.