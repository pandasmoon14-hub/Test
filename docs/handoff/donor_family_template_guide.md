# Donor Family Template Guide

## Purpose

Donor-family templates exist to provide stable, reusable routing metadata for packet planning, extraction review, conversion-intake prompting, and aggregation.

They reduce overuse of `unclassified_or_mixed_donor_family` by classifying donor material by structural family patterns instead of donor-specific naming.

## Why this exists

Without templates, teams can overfit to one donor at a time and lose cross-donor comparability.

Templates prevent that by:

- grounding classification in shared structural signals;
- standardizing expected construct-family pressure;
- documenting known extraction risks and quarantine triggers;
- keeping routing logic consistent across batches.

## Scope and non-authority boundaries

Donor-family classification is routing metadata only.

- Extraction truth is not conversion permission.
- Conversion permission is not canon permission.
- Donor-family classification is not canon.
- Canon promotion requires separate explicit review and authorization.

## How templates support full-corpus readiness

The eventual goal is a single top-level ~1900-donor orchestrated run with internal batching, checkpoints, repair queues, validation gates, aggregation, review ledgers, and resumability.

Donor-family templates support that goal by making batch behavior predictable before scale-up:

1. Packet planning can select representative sections by family template.
2. Extraction review can pre-flag family-typical risks (e.g., OCR, tables, statblocks, map dependency).
3. Conversion-intake prompts can include family-specific guardrails and normalization hints.
4. Aggregation can report pressure by family, reducing ambiguous mixed routing.
5. Review and quarantine can assign escalation owners based on family hints.

## Interaction with pipeline stages

### Extraction lanes

Templates indicate risk signatures that can influence extraction lane selection and repair routing (for example OCR-heavy vs table-heavy vs map-heavy shapes).

### Packet planning

Templates define packet-selection targets so planners sample structurally meaningful sections rather than arbitrary excerpts.

### Conversion-intake prompts

Templates provide conversion prompt additions that improve consistency while avoiding donor-canon adoption.

### Aggregation and review

Templates provide expected construct-family pressure and likely quarantine reasons, improving cross-batch review quality and doctrine owner assignment.

### Quarantine and escalation

Templates define likely quarantine causes and escalation owner hints so unresolved pressure is routed deliberately.

### Canon promotion boundary

Template outputs are never direct canon promotion signals. They are only conversion-stage and review-stage inputs.

## Fallback policy

`unclassified_or_mixed_donor_family` must exist as fallback coverage, but it is not a normal target.

When fallback usage rises, treat it as evidence to refine or add explicit templates rather than as an acceptable steady state.

## Operational guidance

- Prefer the most specific matching template with sufficient detection confidence.
- Use fallback only when no family template meets threshold.
- Keep template language structural and non-proprietary.
- Avoid donor IP import in template examples and notes.
- Keep conversion outputs and generated reports immutable during template-hardening steps.
