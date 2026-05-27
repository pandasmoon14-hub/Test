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
  source_manifest.json
  strict_audit.json
  page_truth.jsonl
  extracted.md
  content_units.jsonl
  extraction_defects.jsonl
  conversion_prompt.md
  packet_readme.md
  queues/
    repair_queue.jsonl
    table_normalization_queue.jsonl
    map_diagram_queue.jsonl
    statblock_queue.jsonl
    ocr_empty_queue.jsonl
    mojibake_cleanup_queue.jsonl
    layout_reconstruction_queue.jsonl
    lexicon_review_queue.jsonl
    doctrine_escalation_queue.jsonl
    source_local_retention_queue.jsonl
    canon_candidate_queue.jsonl
```

Notes:
- `pages/page_truth.jsonl`, `units/content_units.jsonl`, and conversion-stage output files are **not** required as nested packet-root paths in this contract version.
- Conversion/intake outputs (for example conversion result bundles and mapping ledgers) are downstream conversion-stage artifacts unless a later contract explicitly embeds them into packet roots.

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
