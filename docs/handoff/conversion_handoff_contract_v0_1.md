# Conversion Handoff Contract v0.1

## Scope
This contract defines the stable envelope between Aether Forge extraction outputs and Astra Ascension conversion intake. It does **not** guarantee source cleanliness. It guarantees lawful disposition for every page/unit/defect.

## Core principles
- Strict audit pass is not canon readiness.
- Extraction truth, conversion permission, and canon permission are separate axes.
- Every source artifact receives one lawful state: usable, usable-with-warnings, queued, quarantined, or failed.
- Supports mixed donor families at 200–400+ donor scale.

## Packet folder shape
```
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

## Required distinctions
- `extraction_status`: technical extraction outcome.
- `content_readiness`: practical usability for conversion.
- `conversion_permission`: whether Astra conversion may consume the unit.
- `canon_permission`: whether unit may enter canon-candidate review.

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

## Required page provenance fields (minimum)
- `book_id`, `page_number_one_based`
- `source_sha256`
- `extraction_lane`, `extraction_backend`
- `page_status`, `reason_code`
- `ocr_attempted`, `ocr_applied`, `ocr_error`, `ocr_artifact_path`

## Required content-unit fields (minimum)
- `unit_id`, `book_id`, `source_page_start`, `source_page_end`
- `unit_type`, `text`
- `extraction_status`, `content_readiness`, `conversion_permission`, `canon_permission`
- `defects`, `confidence`, `recommended_queue`, `lawful_outcome`, `notes`

## Lifecycle separation
1. Extraction stage (technical truth)
2. Conversion intake stage (readiness + queueing)
3. Canon candidate review (doctrine-governed promotion)
4. Live-play use (post-canon/approved local retention)
