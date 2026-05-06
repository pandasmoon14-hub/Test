# Conversion Handoff Contract v0.1

## Packet purpose
This contract formalizes the handoff layer between Aether Forge extraction and Astra conversion intake.
It does not promise all donor pages are clean; it guarantees lawful disposition for every page, content unit, table, map, stat block, OCR failure, extraction defect, and doctrine ambiguity.

## Packet folder shape (expected)
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

## Required files
At minimum, packets must include manifest, page truth, content units, queue records, conversion result, and mapping ledger.

## Content unit concept
A content unit is the minimal provenance-preserving conversion atom, carrying source page range and explicit readiness/permission/disposition state.

## Conversion result bundle
A conversion result bundle contains readiness assessment, mapping ledger pointer, construct inventory pointer, lexicon delta pointer, canon candidate pointer, quarantine/doctrine/rejection artifacts, confidence, and reviewer notes.

## Required distinction
- extraction_status: what happened technically
- content_readiness: whether the content is usable
- conversion_permission: whether conversion may use it
- canon_permission: whether it may become a canon candidate

## Stage separation
1. Extraction truth capture.
2. Conversion-stage intake and queueing.
3. Canon candidate review.
4. Live-play use.

## Required readiness classes
- ready
- ready_with_warnings
- intake_only
- partial_conversion_allowed
- needs_repair
- quarantined
- failed_extraction

## Required lawful mapping outcomes
- direct Astra mapping
- normalized Astra mapping
- source-local retained construct
- quarantined construct pending later doctrine
- escalated doctrine problem

## Required queues
- repair_queue
- table_normalization_queue
- map_diagram_queue
- statblock_queue
- ocr_empty_queue
- mojibake_cleanup_queue
- layout_reconstruction_queue
- lexicon_review_queue
- doctrine_escalation_queue
- source_local_retention_queue
- canon_candidate_queue
