# Handoff Queue Policy v0.1

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

## Ownership and record requirements
Each queue record must define queue owner, priority, status, blocking effect, allowed interim use, and recommended action.

## Routing rules
- OCR-empty or OCR-unresolved pages -> `ocr_empty_queue` or `repair_queue`.
- Table/list defects -> `table_normalization_queue` before row-faithful conversion.
- Map-dependent unresolved spatial references -> `map_diagram_queue`.
- Statblock parsing/mechanical ambiguity -> `statblock_queue` and/or `doctrine_escalation_queue`.
- Donor-local valid constructs not promotable to canon -> `source_local_retention_queue`.
- Canon promotion candidates after checks only -> `canon_candidate_queue`.

## Canon safety
Queued and repair-required units cannot be promoted as canon candidates.
