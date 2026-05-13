# Current Decisions Log

This file records project decisions that are not obvious from code alone. Its purpose is to prevent re-litigating settled pilot choices across ChatGPT, Claude, Claude Code, Grok, Codex, and manual PowerShell sessions.

## Current working repo and run layout

- Active repo path: `C:\Dev\Test-main-git`
- Active Step 10 run path: `C:\AetherForgeRuns\_active\handoff_step10_conversion_intake_run_v0_1`
- Step 10B final frozen snapshot: `C:\AetherForgeRuns\handoff_step10b_12_packet_conversion_intake_run_20260513_153357.zip`
- Step 10C final snapshot should be created after under-parsed packet repair and final strict validation.

## Handoff contract principles

- Extraction truth is not conversion permission.
- Conversion permission is not canon permission.
- Canon permission requires review and promotion.
- Donor content is not live-play authority.
- Donor constructs must receive one lawful outcome:
  - direct Astra mapping
  - normalized Astra mapping
  - source-local retained construct
  - quarantined construct pending later doctrine
  - escalated doctrine problem

## Local extraction and handoff decisions

- Lane A is accepted as the safe local default for the pilot cycle.
- AUTO / higher lanes may fall back to Lane A when external dependencies are unavailable.
- Missing Marker/Docling-style local dependencies are not blockers for this pilot.
- OCR may be attempted/applied, but OCR output is not automatically higher authority than native text.
- Page truth, manifest data, defects, queues, and conversion permissions must be preserved separately.
- `OCR_MODE=skip` remains the safe pilot default unless a targeted OCR repair pass is explicitly being tested.

## Step 10B packet selection rationale

The 12-packet Step 10B selection was intentionally broad. It tested:
- Fate mechanics/procedure
- Fate worksheet/character setup
- Random tables/list material
- Pathfinder adventure-site/dungeon/statblock pressure
- GURPS Bio-Tech biotechnology/body modification/living-platform pressure
- Cities Without Number urban/cyberpunk/combat/gear pressure
- CthulhuTech vehicle/platform/horror/investigation pressure
- Numenera/Jade Colossus procedural ruin/random-table/anomaly pressure
- Anima character options/combat modules/statblock pressure
- Colostle credits/backmatter false-positive pressure
- Heroines of the Last Age macro-region/travel/threat-hook pressure
- Sword World replay/character-sheet/party/crafting pressure

## Step 10B / Step 10C findings

- Step 10B produced 12 drafted packets and 0 placeholders.
- Two Markdown memos were rich but under-parsed in JSON because section headings were escaped as `1\.` instead of `1.`:
  - Pathfinder Dungeons of Golarion pages 19-37
  - Book of Random Tables Fantasy Space pages 8-17
- The scaffolder should tolerate escaped numbered headings.
- Report tooling should detect fallback-level parses.
- Colostle was a low-value but useful negative-control packet. It should be retained as a credits/backmatter false-positive case.
- Credits, backer names, acknowledgements, supporter lists, and publication backmatter should be classified as non-convertible source-local material.
- Dense name lists should not be treated as random tables, statblocks, factions, NPCs, or setting canon.

## Final Step 10B aggregate result before Step 10C repair

- packets_total: 12
- drafted: 12
- placeholder: 0
- source-local retained construct: 113
- normalized Astra mapping: 328
- direct Astra mapping: 6
- quarantined construct pending later doctrine: 40
- escalated doctrine problem: 10
- doctrine_escalation_count: 118
- source_local_retention_count: 148
- rejected_import_count: 157
- canon_candidate_note_count: 10

## Step 11 purpose

Step 11 applies Step 10C findings to the repo:
- add escaped-heading parser tolerance
- add under-parsed result detection
- add false-positive/backmatter classification notes
- add tests for the known Step 10C failure cases
- update handoff docs so future runs do not repeat these manual fixes
