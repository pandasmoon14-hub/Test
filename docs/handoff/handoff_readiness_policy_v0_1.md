# Handoff Readiness Policy v0.1

Readiness may be assigned at book, packet, page, and content-unit levels. Content-unit level is authoritative for conversion intake.

## Classes
- `ready`: conversion-safe, no unresolved blockers.
- `ready_with_warnings`: conversion-safe with explicit caveats.
- `intake_only`: retain/index only; not conversion-final.
- `partial_conversion_allowed`: subset is convertible; residual defects remain.
- `needs_repair`: blocked pending OCR/layout/normalization repair.
- `quarantined`: blocked for doctrine/legal/semantic reasons.
- `failed_extraction`: extraction could not produce a reliable unit.

## Policy coupling
- `needs_repair`, `quarantined`, `failed_extraction` cannot be canon candidates.
- `canon_permission=allowed` requires doctrine ownership and review trace.
- `conversion_permission` may be broader than `canon_permission`.

## Required behavior
Every non-ready assignment must include queue/quarantine/failure reason and recommended disposition path.
