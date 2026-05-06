# Handoff Readiness Policy v0.1

## Intent
Define how units are classified for conversion without conflating extraction correctness and canon eligibility.

## Readiness classes
- `ready`: conversion-safe with no known blockers.
- `ready_with_warnings`: conversion-safe but flagged for review.
- `intake_only`: indexed/retained, not suitable for direct conversion output.
- `partial_conversion_allowed`: some fields may convert; others must be omitted or queued.
- `needs_repair`: blocked pending OCR/layout/text repair.
- `quarantined`: doctrinal/legal/semantic uncertainty requires hold.
- `failed_extraction`: technical extraction failure prevents reliable use.

## Permission coupling
- `ready`/`ready_with_warnings` may allow `conversion_permission=allowed`.
- `needs_repair`, `quarantined`, `failed_extraction` cannot be canon candidates.
- `canon_permission=allowed` requires doctrine ownership and review trail.

## Scale posture
Policies must remain deterministic and automatable for 200–400+ donors and mixed families.
