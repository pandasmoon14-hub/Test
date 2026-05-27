# AstraCloud / Aether Forge Current Decisions Log v0.1

> Cross-reference: For broader project and governance decision records, see `docs/decisions/current_decisions_log.md`.
> Scope note: this file is the operations log for extraction, handoff, and conversion-intake pipeline execution decisions.

Status: active working log  
Scope: extraction, handoff contract, conversion-intake pipeline, and near-term runtime planning  
Purpose: record project decisions that are not obvious from code, so future sessions do not re-litigate already-settled choices.

---

## 1. Lane A is the current local default extraction lane

Decision:
Lane A is the safe local default for current extraction pilots.

Reason:
The current local machine and dependency state are better suited to deterministic/native-text extraction and audit validation than to heavier OCR/layout/vision pipelines. Lane A gives stable, testable outputs and avoids blocking the project on heavyweight extraction dependencies.

Implication:
If AUTO routing falls back to Lane A, that is acceptable during pilot work unless the test specifically requires advanced layout/OCR behavior.

Revisit when:
- Marker, Docling, Surya, OCR tooling, or a cloud extraction lane is intentionally installed and validated.
- A donor family consistently fails under Lane A.
- Table/map/statblock recovery becomes the next bottleneck.

---

## 2. `OCR_MODE=skip` is the safe pilot setting unless OCR is being tested

Decision:
Use `OCR_MODE=skip` for safe pilot runs unless the explicit goal is OCR gating or OCR repair behavior.

Reason:
OCR introduces more moving parts, slower runs, dependency failures, and repair ambiguity. For current handoff-shape testing, page truth, provenance, and packet validation matter more than maximizing every page’s OCR recovery.

Implication:
A skipped OCR page is not automatically a failed extraction pipeline. It should be queued or marked according to page truth and readiness policy.

Revisit when:
- OCR dependency setup is stable.
- We intentionally run repair-lane tests.
- The selected donor batch is scanned/image-heavy.

---

## 3. `OCR_MODE=force` is only for OCR gate tests, not the default corpus run

Decision:
Forced OCR is used only when testing OCR behavior.

Reason:
Forced OCR can produce empty post-OCR text, false repair pressure, and unnecessary runtime cost on pages that already contain usable native text.

Implication:
Do not use forced OCR as the default extraction mode for broad pilots.

Revisit when:
- OCR quality is benchmarked against native extraction.
- A dedicated scanned-PDF lane is built.

---

## 4. Marker/Docling are not required for the current local pilot

Decision:
Do not block current progress on installing or stabilizing Marker, Docling, or equivalent heavyweight layout tools.

Reason:
The current work is proving the Aether Forge handoff contract and conversion-intake artifact shape. That can proceed with deterministic extraction, page truth, manifests, queues, and packet validation.

Implication:
AUTO fallback to Lane A due to missing external dependencies is acceptable in local pilots, provided the fallback is recorded in manifests and validation summaries.

Revisit when:
- The handoff contract is stable.
- Table/map/statblock repair quality becomes the main limiting factor.
- A rented GPU/cloud extraction phase begins.

---

## 5. Extraction truth is separate from conversion readiness

Decision:
A page or packet can be extraction-valid without being conversion-ready.

Reason:
Extraction truth answers: “What did the pipeline see?”  
Conversion readiness answers: “Can this be safely converted?”  
These are different judgments.

Implication:
Do not collapse `page_status=ok` into “ready for conversion.” A page can be readable and still need table normalization, map review, statblock review, or source-local quarantine.

Revisit when:
Never. This is foundational doctrine.

---

## 6. Conversion readiness is separate from canon permission

Decision:
A packet can be usable for conversion intake while still blocked from canon promotion.

Reason:
Conversion-stage artifacts are analysis outputs, not final Astra canon. Canon requires later review, consolidation, contradiction checks, doctrine ownership, and sourcebook integration.

Implication:
Most current packets should remain `intake_only`, `allowed_with_warnings`, or `review_required` for canon.

Revisit when:
Never. This is foundational doctrine.

---

## 7. Donor content is not live-play authority

Decision:
Original donor rules, setting assumptions, named entities, economies, cosmologies, classes, powers, and stat math are not runtime authority.

Reason:
Astra is a conversion-stable original framework. Donors provide pressure, variants, examples, and source-local constructs, not hidden law.

Implication:
Runtime should resolve through Astra doctrine/canon, not raw donor chunks.

Revisit when:
Never, except for explicitly activated campaign-profile material that remains source-local and authority-gated.

---

## 8. Every donor construct needs exactly one lawful outcome

Decision:
Every donor construct encountered in conversion intake must receive one lawful outcome:

- direct Astra mapping
- normalized Astra mapping
- source-local retained construct
- quarantined construct pending later doctrine
- escalated doctrine problem

Reason:
This prevents vague “maybe useful later” drift and decorative Astra-sounding invention.

Implication:
Conversion memos must account for every visible construct family.

Revisit when:
Only if the lawful-outcome enum is formally revised.

---

## 9. Step 10B is currently a 12-packet conversion-intake pilot

Decision:
Step 10B uses a selected 12-packet pilot rather than the whole corpus.

Reason:
The current goal is to prove the contract loop:

packet bundle → conversion memo → result Markdown → scaffolded JSON → validation → report

The goal is not volume yet.

Implication:
Do not scale to 50, 500, or 1,900 donors until the 12-packet loop proves quality and reporting value.

Revisit when:
- All 12 packets are drafted/scaffolded.
- The report accurately preserves mapping ledgers, retentions, rejected imports, and canon notes.
- Handoff contract v0.2 is frozen.

---

## 10. The 12-packet selection is intentionally pressure-diverse

Decision:
The Step 10B packet set should cover different donor pressures, not only clean prose.

Current completed pressure types:
- Fate packet: mechanics/procedure and table-misclassification pressure.
- Random Tables packet: random-table/list pressure, map/document flags, statblock false positives.
- Pathfinder packet: adventure-site, map/list, statblock, trap, relic, spell, and source-local setting pressure.

Reason:
Astra must survive 1,900 donors, not one clean rulebook.

Implication:
Future selected packets should continue testing different structures: bestiary, equipment, spells/powers, vehicles, factions, travel, economy, horror/stress, lifepath, companions, maps, and adventures.

Revisit when:
After the first 12-packet report is reviewed.

---

## 11. ChatGPT is currently acting as the conversion-intake model for pilot memos

Decision:
For Step 10B, ChatGPT can produce conversion-intake memos from uploaded model-ready packet bundles.

Reason:
Local 8B models are useful for smoke tests but may be too weak for disciplined conversion intake. Cloud model access was blocked by subscription friction. Using ChatGPT allows the workflow to proceed.

Implication:
Upload full packet bundles, not just wrapper prompts. The assistant must use only the uploaded packet bundle.

Revisit when:
- A reliable local or rented-GPU conversion model is selected.
- Qwen/Mistral/other models are evaluated on the same packets.
- A formal conversion-model benchmark exists.

---

## 12. Local `llama3.1:8b-instruct-q4_0` is smoke-test only

Decision:
`llama3.1:8b-instruct-q4_0` may be used locally for workflow smoke tests, not trusted final conversion.

Reason:
It fits the local RTX 4060 8 GB VRAM machine, but it is likely weak on long-context discipline, subtle doctrine boundaries, and complete construct accounting.

Implication:
Do not judge final conversion quality by local 8B results alone.

Revisit when:
- A local Qwen/Gemma/Mistral quantized candidate is benchmarked.
- A rented-GPU model becomes available.

---

## 13. Qwen3/Qwen-class larger models are rented/cloud candidates, not local defaults

Decision:
Qwen3-32B or larger models are candidate serious conversion models for rented/cloud GPU phases, not current local execution.

Reason:
The local machine has RTX 4060 8 GB VRAM and 32 GB RAM. It is suitable for pilots and small local models, not sustained 32B+ conversion.

Implication:
Do not design local workflows around 32B+ assumptions.

Revisit when:
- Renting GPU.
- Using provider-hosted inference.
- Building a model benchmark suite.

---

## 14. The current JSON scaffolder is valid but too lossy

Decision:
`scaffold_conversion_intake_json.py` is accepted as proof that Markdown memos can become schema-valid JSON, but it needs improvement before finishing the full pilot.

Reason:
The report currently shows drafted packets but undercounts lawful outcomes and does not preserve detailed mapping rows, source-local retentions, rejected imports, or canon candidate notes.

Implication:
Improve scaffolder parsing before completing all remaining packets, or at minimum before freezing Step 10B.

Revisit when:
- Mapping-ledger table parsing works.
- Source-local retentions and rejected imports appear in reports.
- Confidence parsing works.
- Multiple mapping entries are preserved.

---

## 15. The current validator result `drafted: 3, placeholder: 9` is expected

Decision:
The Step 10B run is valid with three drafted JSON results and nine placeholders.

Reason:
The pilot is being completed packet by packet.

Implication:
Validation with `--allow-placeholders` is correct until all 12 packets have JSON results.

Revisit when:
All 12 packets are drafted; then run strict validation without placeholders if the schema supports complete status.

---

## 16. Do not run the full corpus yet

Decision:
Do not start full 1,900-donor extraction/conversion yet.

Reason:
The handoff contract, table normalization, map/statblock routing, conversion-result schema, and reporting loops are still being hardened.

Implication:
More pilot batches are acceptable; full corpus processing is premature.

Revisit when:
- Handoff v0.2 is frozen.
- Repair queues and table/map/statblock handling are reliable.
- Conversion-intake reports preserve enough information.
- Snapshot/recovery practices are stable.

---

## 17. Full extraction success is not yet proven for all donor types

Decision:
The project has not yet proven clean extraction for every one of the 1,900 donor PDFs.

Reason:
The current work proves packet shape and selected extraction behavior, not universal donor robustness.

Implication:
Avoid claiming “we can accurately extract all donors” until larger representative batches are tested.

Revisit when:
- Representative donor-family pilots pass.
- OCR-heavy, table-heavy, map-heavy, statblock-heavy, and multilingual donors have dedicated lanes.
- Repair pipeline is validated.

---

## 18. Table/list-heavy donors are a known pressure point

Decision:
Table normalization is a major next improvement area.

Reason:
Random-table packets and misclassified procedure packets show flattened tables, broken numbering, ambiguous row boundaries, and table false positives.

Implication:
Do not directly convert row-level table content until normalization improves.

Revisit when:
- Table sidecars are reliable.
- Row boundaries are reconstructed.
- Table titles, entries, dice expressions, and notes are separated.

---

## 19. Map/diagram references must not be treated as clean text

Decision:
Map/diagram queue flags remain open until validated.

Reason:
Some “map” flags refer to actual visual dependencies; others are item entries like star charts, blueprints, or route maps.

Implication:
Separate actual visual map dependency from information-bearing map-object entries.

Revisit when:
- Map extraction/visual review lane exists.
- Map-object schema is stable.

---

## 20. Statblock queue flags may be true positives or false positives

Decision:
Statblock flags require review.

Reason:
Some packets contain actual creature or trap statblocks. Others trigger statblock queues due to compact numeric formatting or dice-heavy tables.

Implication:
Do not convert statblock math blindly. Route through statblock conversion schema.

Revisit when:
- Statblock detector distinguishes creature statblocks, trap statblocks, spell blocks, item blocks, and false positives.

---

## 21. Source-local retention is not optional

Decision:
Named donor entities, setting history, cosmology, economies, named artifacts, gods, factions, places, and donor-specific mechanics must be retained source-locally unless explicitly promoted.

Reason:
This prevents donor canon leakage into Astra.

Implication:
Conversion memos should explicitly list source-local retentions and rejected imports.

Revisit when:
Never; this is core conversion discipline.

---

## 22. Runtime architecture should become standalone, but not immediately

Decision:
Long-term, Astra should become a standalone runtime/client ecosystem. Short-term, keep KoboldCPP/SillyTavern/model servers as optional adapters.

Reason:
Astra needs a deterministic backend, event ledger, state panels, tool bus, packet compiler, debug UI, and model orchestration beyond what SillyTavern is designed to own.

Implication:
Do not bind final architecture to SillyTavern. Also do not rebuild low-level model inference unnecessarily.

Revisit when:
- Backend runtime prototype exists.
- Debug UI exists.
- Model adapter layer is stable.

---

## 23. LLMs must not own state

Decision:
No LLM should directly mutate canonical state.

Reason:
LLMs can hallucinate, contradict, overgeneralize, or leak hidden information. State must be committed only through validated backend events.

Implication:
LLMs may propose IR, narration, summaries, and candidate actions. The backend validates and commits.

Revisit when:
Never.

---

## 24. Prose never mutates state

Decision:
Narration is downstream of state, not the source of state.

Reason:
If prose can mutate state, replay, validation, hidden information, and consistency all fail.

Implication:
The narrator receives validated visible outcome packets and renders them. State changes happen through StateDeltaIR and event commits.

Revisit when:
Never.

---

## 25. The runtime must support mature and dark play through campaign profiles

Decision:
The final runtime should be capable of serious, dark, romantic, mature, horror, violent, absurd, heroic, tragic, and political play, but controlled through machine-readable campaign profiles and boundaries.

Reason:
The project aims for broad TTRPG possibility, including adult themes and intense violence, but these must be governed by tone, consent, visibility, and content settings rather than improvised by the narrator.

Implication:
Campaign profile doctrine must eventually include romance, adult content, gore, horror, coercion boundaries, PvP, evil actions, fade-to-black, and player-specific filters.

Revisit when:
Runtime doctrine pack begins.

---

## 26. The end-state design target is “classify, route, resolve, persist”

Decision:
The engine should not try to prewrite every possible action.

Reason:
Player creativity is unbounded. The engine survives by decomposing actions into actor, intent, target, method, resources, scope, risk, opposition, affected systems, consequences, and state deltas.

Implication:
Build universal interaction grammar, affordance algebra, consequence compiler, project engine, ontology router, and anti-exploit governors.

Revisit when:
Never; this is the core runtime design law.

---

## 27. Dangerous constructs are contained, not casually refused or accepted

Decision:
Time travel, reality rewriting, infinite clones, public-belief magic, recursive dimensions, god creation, cursed language, and concept deletion should receive lawful containment paths.

Reason:
Donors will contain strange mechanics, and players will attempt extreme actions. The system needs safe outcomes beyond “yes” or “no.”

Allowed dispositions:
- valid action
- valid project
- symbolic action
- branch simulation
- dream/simulation layer
- local reality bubble
- scope-governed action
- campaign-profile-only
- GM/author approval required
- quarantine
- rejected for runtime integrity

Revisit when:
Runtime anti-exploit doctrine is written.

---

## 28. The next immediate technical decision is scaffolder improvement

Decision:
Before drafting the remaining nine Step 10B packets, improve the JSON scaffolder.

Reason:
Three pressure types have proven the loop works. The current bottleneck is information preservation, not proof of concept.

Implication:
Next Claude Code task should improve `scaffold_conversion_intake_json.py` parsing.

Acceptance:
- mapping ledger rows become multiple JSON entries
- lawful outcomes are normalized
- donor construct inventory lists parse into multiple entries
- source-local retentions parse
- rejected imports parse
- canon candidate notes parse
- confidence labels parse
- all tests pass

---

## 29. Snapshot discipline remains required

Decision:
Freeze important milestones as zip snapshots.

Reason:
The project is moving quickly, sometimes outside git, and needs recoverable states.

Implication:
After major steps, archive scripts, schemas, docs, tests, plans, packets, and reports.

Revisit when:
A proper git workflow is restored and stable; even then, frozen run snapshots remain useful.

---

## 30. Current local environment constraints

Known local machine:
- Windows 11
- Intel i7-14700F
- 32 GB RAM
- RTX 4060 8 GB VRAM
- 1.8 TB SSD

Decision:
Design local pilot workloads around these constraints.

Implication:
Use local scripts, small/quantized models for smoke tests, and avoid assuming local 32B+ inference.

Revisit when:
Using rented GPU/cloud instance.

---

## 32. AetherForgeRuns internal layout reorganized into category subfolders

Decision:
`C:\AetherForgeRuns` was reorganized from a flat 50+ item root into category subfolders: `_active`, `snapshots`, `plans`, `helpers`, `reports`, `fixtures`, `pilots\{pilot20,pilot50,real1,real3,ocr_gates}`, `packets`, `handoff_test_3`.

Reason:
The flat root had grown unwieldy. Navigation was slow and the currently active run was hard to locate. Grouping by artifact type makes the layout self-documenting.

Implication:
Any scripts, notes, or commands referencing old top-level paths (e.g. `C:\AetherForgeRuns\handoff_step10_conversion_intake_run_v0_1`) need updating. The current active run is now at `C:\AetherForgeRuns\_active\handoff_step10_conversion_intake_run_v0_1`. Helper scripts under `C:\AetherForgeRuns\helpers\` still have hardcoded pre-reorganization paths; they should be replaced with parameterized versions under `scripts/handoff/` rather than edited in place.

Revisit when:
Categories grow unwieldy themselves, or when archival storage tiering becomes useful (e.g. moving old snapshots to slower disk).

---

## 33. Code repo moved to C:\Dev\AetherForge; Claude Code replaces ChatGPT/Codex as primary assistant

Decision:
The working code repo is now `C:\Dev\AetherForge` (cloned from the GitHub remote), outside OneDrive. Claude Code replaces ChatGPT/Codex as the primary development assistant. `CLAUDE.md` at the repo root provides per-session context.

Reason:
The previous working folder was a zip-extracted OneDrive path, which caused pytest cache permission errors, no git history, and friction with file operations. Claude Code reads `CLAUDE.md` automatically per session, eliminating the long "we completed Step X, current state is Y" preambles that were burning context in every Codex prompt.

Implication:
Future sessions start by reading `CLAUDE.md` and pulling in deeper docs (master brief, decisions log) only when relevant. Run artifacts stay at `C:\AetherForgeRuns\` and are not part of the repo. Entry #11 (ChatGPT as conversion-intake model) is partially superseded: Claude Opus 4.7 via Claude Code is now the primary assistant; ChatGPT may still be used as a secondary conversion-intake model for cross-checking memos until a benchmarked successor is chosen.

Revisit when:
A different assistant or workflow becomes preferable, or `CLAUDE.md` itself needs restructuring.