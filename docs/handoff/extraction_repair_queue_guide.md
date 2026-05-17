# Extraction Repair Queue Guide

## Purpose

Extraction repair queues exist to route extraction defects, packet-shape defects, and conversion-blocking artifacts into lawful operational handling paths.

They prevent full-corpus runs from collapsing on ugly PDFs by replacing crash-or-drop behavior with explicit queue routing, repair actions, and audit records.

## Authority and boundary rules

Repair queues are operational routing metadata, not canon.

- Extraction truth is not conversion permission.
- Conversion permission is not canon permission.
- Queue routing outcomes never grant canon permission.

## Why this matters for full-corpus hardening

The eventual single top-level ~1900-donor orchestrated run must continue past repairable failures while preserving auditability.

Repair queues enable this by:

1. capturing defect type and severity,
2. deciding whether conversion is blocked,
3. recording expected artifacts and reviewer actions,
4. routing unresolved issues to quarantine or human review,
5. preserving lineage between defects and downstream outcomes.

## Pipeline interactions

### Extraction lanes

Queue signals such as OCR-needed, table flattening, statblock under-parse, and column merge/split failure route documents into specialized extraction lanes or repair reruns.

### Page-truth artifacts

Queues like `missing_page_truth` and `underparsed_page` depend on page-truth comparison to verify extraction completeness before conversion.

### Packet planning and packet building

Queues such as `packet_boundary_ambiguity`, `source_metadata_gap`, `sidebar_or_callout_ordering`, and `duplicate_or_conflicting_page` stabilize packet scope and ordering so content is not duplicated, dropped, or mis-sequenced.

### Conversion-intake

`conversion_blocked_by_extraction` explicitly blocks conversion until upstream extraction defects are resolved. Non-blocking queues may allow intake-only handling with uncertainty flags.

### Validation

`artifact_validation_error` and malformed table/stat artifacts are repaired before validators are rerun. Validation must fail closed for blocking defects.

### Aggregation and review

`manual_review_required` captures unresolved mixed defects for human adjudication and preserves review ledger traceability.

## Severity model

- `info`: low-risk operational cleanup.
- `warning`: non-fatal issue requiring reviewer attention.
- `repair_required`: repair must occur before reliable conversion.
- `blocking`: fail-closed condition; conversion cannot proceed.

## repair_required vs intake_only

- `repair_required` means the defect must be corrected before reliable conversion outcomes can be trusted.
- `allows_intake_only` means the system may preserve intake artifacts for review while explicitly avoiding unsafe conversion decisions.

These flags can coexist with different severities depending on risk and stage.

## Reviewer handling guidance for common failure modes

- **OCR-needed pages**: run OCR lane; verify against page truth; rerun extraction validation.
- **Table flattening / malformed random tables**: reconstruct table structure and roll ranges before conversion.
- **Statblock under-parsing**: require complete stat fields before downstream mapping.
- **Map/diagram or visual dependencies**: capture context; quarantine unresolved mechanics rather than guessing.
- **Mojibake**: repair encoding only where semantic confidence is defensible.
- **Packet-boundary ambiguity**: replan packet manifests to prevent duplicate/drop contamination.

## Continuation policy for the eventual ~1900-donor run

The orchestrated run should continue past repairable failures by queuing defects, checkpointing progress, and preserving queue-linked audit artifacts.

It should only halt conversion for defects marked blocking (or equivalent policy conditions), while still recording affected packets for resumable repair and later reintegration.
