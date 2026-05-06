# Handoff Readiness Policy v0.1

Readiness is assigned independently at four scopes: book, packet, page, and content-unit.

## Classes and usage
- ready: clean for conversion at current scope.
- ready_with_warnings: usable now, with declared caveats.
- intake_only: retain for indexing/traceability; not final conversion-grade.
- partial_conversion_allowed: only subset of fields/constructs may convert.
- needs_repair: blocked pending repair (OCR/layout/normalization/etc.).
- quarantined: blocked for doctrine/semantic/legal ambiguity.
- failed_extraction: extraction failed; unit/page not reliable.

## Scope guidance
- Book-level: summarize overall donor usability.
- Packet-level: summarize handoff packet conversion posture.
- Page-level: represent technical extraction condition per source page.
- Content-unit level: authoritative conversion decision unit.

## Permission coupling
- non-ready classes require queue, quarantine note, or explicit failure reason.
- needs_repair and failed_extraction cannot be canon candidates.
