# Handoff Queue Policy v0.1

## Queue ownership
Each queue record must include owner and status. Owners are accountable for disposition movement.

## Queue set
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

## Queue record requirements
Each record must include queue_id, queue_name, unit_id, book_id, source_pages, reason_code, blocking_effect, allowed_use, recommended_action, priority, owner, status.

## Routing guidance
- OCR empty pages -> ocr_empty_queue (or repair_queue when generalized repair workflow applies).
- Table defects -> table_normalization_queue.
- Map-dependent defects -> map_diagram_queue.
- Statblock/mechanical parsing issues -> statblock_queue.
- Doctrine conflicts -> doctrine_escalation_queue.
- Source-local retained constructs -> source_local_retention_queue.
- Canon review candidates -> canon_candidate_queue.
