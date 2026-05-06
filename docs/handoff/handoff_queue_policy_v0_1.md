# Handoff Queue Policy v0.1

## Queue catalog
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

## Queue semantics
Each queued unit must include: blocking reason, allowed interim use, recommended action, owner, priority, status.

## Queue routing defaults
- OCR empty/failure -> `ocr_empty_queue` or `repair_queue`
- Broken table structure -> `table_normalization_queue`
- Map-dependent unresolved references -> `map_diagram_queue`
- Stat/math/economy ambiguities -> `statblock_queue` and/or `doctrine_escalation_queue`
- Donor-local but valid constructs -> `source_local_retention_queue`
- Promotion candidates after doctrine checks -> `canon_candidate_queue`
