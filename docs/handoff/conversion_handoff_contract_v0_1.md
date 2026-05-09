# Conversion Handoff Contract v0.1

This contract defines the formal boundary between extraction truth and Astra conversion intake.

## Non-goals and boundaries
- A strict extraction audit pass is **not** canon readiness.
- Conversion output is **not** final canon.
- Live-play adjudication is out of scope for this contract.

## Core distinction model
The following fields are separate and must never be conflated:
- `extraction_status`: technical extraction result.
- `content_readiness`: practical usability for conversion.
- `conversion_permission`: whether conversion may consume the unit.
- `canon_permission`: whether content may enter canon-candidate review.

## Packet purpose
A packet is a provenance-preserving exchange artifact that guarantees lawful disposition for each source page, content unit, table, map, stat block, OCR defect, extraction defect, and doctrine ambiguity.

## Packet shape (expected)
```text
<packet_root>/
  packet_manifest.json
  pages/page_truth.jsonl
  units/content_units.jsonl
  units/table_units.jsonl
  units/map_units.jsonl
  units/statblock_units.jsonl
  queues/queue_records.jsonl
  conversion/conversion_result.json
  conversion/mapping_ledger.jsonl
  conversion/construct_inventory.json
  conversion/lexicon_delta.json
  conversion/canon_candidates.jsonl
  conversion/quarantine_notes.md
  conversion/doctrine_escalations.jsonl
  conversion/rejected_imports.jsonl
```

## Required lifecycle separation
1. Extraction capture (technical truth)
2. Conversion-stage intake and routing
3. Canon review and doctrine ownership
4. Post-canon operational use (outside contract)

## Routing obligations
- Every non-ready unit must route to queue, quarantine, or explicit failure.
- Queued/repair units cannot be canon candidates.
- Table/list-heavy donors require table normalization before row-faithful conversion.
- Map-heavy donors require map validation before spatial canon promotion.
- Stat blocks require quarantine/statblock conversion before Astra mechanics import.
