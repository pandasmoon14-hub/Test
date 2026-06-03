# D19-05 — Lawful Outcome Consistency, Source-Local Governance, Quarantine, and Escalation Audit

> **Status:** Phase 1 capstone doctrine. This file is a control-layer artifact for Astra Ascension doctrine integration. It is not final sourcebook prose, not a live-play GM adapter, not a runtime/backend schema, and not a donor conversion output. Any record shapes in this pack are lightweight doctrine-facing / conversion-facing / audit-facing shapes only and may be replaced or formalized later by Batch C schema doctrine, Runtime Gate B, canon consolidation, or playtest calibration.


## Core question

How does Astra ensure that every donor construct, doctrine ambiguity, cross-pack conflict, unsupported subsystem, source-local procedure, and deferred mechanic receives one lawful outcome rather than being improvised, silently normalized, canonized by repetition, or resolved through donor assumptions?

## Construct–Outcome–Boundary–Escalation Model

D19 uses this procedure:

```text
1. Identify the construct.
2. Identify the donor/source/context evidence.
3. Identify the relevant Astra owner file or files.
4. Determine whether current doctrine supports the construct.
5. Assign exactly one primary lawful outcome.
6. Record source-local boundary, quarantine blocker, or escalation trigger if applicable.
7. Record rejected assumptions.
8. Record whether the construct can be revisited later.
```

Mixed constructs may split into subconstructs. Each subconstruct receives its own lawful outcome and owner-file route.

## The five lawful outcomes

### 1. Direct Astra mapping

Use when the construct already fits an existing Astra owner without importing unsupported donor assumptions.

Requirements:

```text
clear owner file
no unsupported donor math
no unsupported donor metaphysics
no unsupported economy, advancement, harm, or campaign assumption
no hidden source-local law
no schema gap blocking use
no canon conflict
no owner boundary conflict
```

Direct mapping still uses Astra terminology and owner boundaries. It does not copy donor wording by default.

### 2. Normalized Astra mapping

Use when the construct has a valid function but donor packaging must be stripped.

Examples:

```text
donor spell -> Technique / expression pressure, not copied spell law
donor monster ability -> opposition capability pressure with owner-file handoffs
donor loot table -> D17 value-entry evidence, not automatic reward law
donor faction clock -> unresolved pressure / D15/D10/D18 handoff, not universal clock doctrine
donor level band -> power-envelope evidence, not campaign phase law
donor currency -> value form, not Astra default money
```

Normalized mapping preserves function, not donor structure.

### 3. Source-local retained construct

Use when the construct is useful inside a bounded converted source but unsafe to generalize.

Requires:

```text
explicit boundary
source or scenario scope
owner-file handoffs
rejected-import notes
statement that it is not Astra baseline
closure, archive, or later-review condition
canon-candidate status if any
```

Source-local retention is lawful. Silent generalization is not.

### 4. Quarantined construct pending later doctrine

Use when the construct is understandable enough to preserve but not safe to convert yet.

Triggers include:

```text
missing owner file support
missing schema support
missing math/calibration
missing source-local boundary
missing extraction data
missing table/sidecar
unclear donor function
unclear state mutation
unclear authority level
unclear canon status
owner-file conflict
hidden-state risk
unsupported advancement, economy, harm, actor, object, faction, or campaign assumption
risk of donor metaphysics becoming Astra law
risk of player-facing or runtime-facing leakage
```

Quarantine preserves evidence and names the blocker. It is not a dumping ground.

### 5. Escalated doctrine problem

Use when the construct reveals a missing or unstable Astra doctrine distinction.

Triggers include:

```text
repeated donor pressure across multiple sources
high-impact construct needed for many families
core owner conflict
canon authority conflict
no lawful landing place
existing doctrine too narrow
deferred item now blocking conversion
source-local retention would fragment Astra if repeated
quarantine would only postpone an unavoidable architecture decision
runtime/schema requirement is now structurally necessary
```

Escalation identifies likely future owner: owner-file patch, new doctrine pack, Batch C schema doctrine, conversion IR update, canon review, runtime Gate B, source-local registry, playtest calibration, benchmark, or example pack.

## Forbidden informal outcomes

D19 explicitly forbids:

```text
convert loosely
use donor version
treat as flavor
let GM decide
assume nearest Astra equivalent
make a temporary rule
canonize by repetition
ignore unless it matters later
translate the label directly
```

These create contradiction at corpus scale.

## Source-local governance checklist

Every source-local retained construct records:

```text
source identifier
construct name
construct function
owner files affected
source-local boundary
what is retained
what is stripped
what assumptions are rejected
what can and cannot generalize
closure condition
archive condition
canon-candidate status if any
quarantine/escalation trigger if repeated or expanded
```

## Quarantine governance checklist

Every quarantine records:

```text
construct name
blocked owner file
blocked doctrine area
blocked schema/math/runtime/canon issue
evidence preserved
why direct/normalized/source-local handling is unsafe
what would unlock conversion
whether repeated donor pressure should escalate
current allowed handling
```

## Escalation governance checklist

Every escalation records:

```text
construct or pressure
why existing doctrine is insufficient
donor families affected
frequency or impact
owner file likely responsible
whether it needs patch, new pack, schema, runtime, canon review, examples, benchmark, or playtest
risk if ignored
risk if solved prematurely
recommended next action
```

## Canon-candidate distinction

A source-local construct may become a canon candidate only when it recurs across donor families, solves a real Astra-native need, avoids unreviewed donor metaphysics/math, has owner-file support, can be expressed in Astra terminology, survives conflict review, and belongs in sourcebook-facing canon rather than conversion-only doctrine.

Canon-candidate status is review status only. It is not canon promotion.

## Outcome consistency rules

```text
One construct may split into multiple subconstructs, each with its own lawful outcome.
A donor label does not determine the outcome.
A donor table is evidence, not authority.
A source-local retained construct is not canon.
A quarantined construct is not converted.
An escalated construct is not solved by decorative doctrine language.
A normalized mapping does not preserve donor mechanics unless owner files support them.
A direct mapping still uses Astra terminology and owner boundaries.
Repeated source-local use creates escalation pressure, not automatic canon.
Canon promotion requires canon process, not conversion usefulness.
Runtime usefulness does not make a doctrine record a runtime schema.
```

## Acceptance criteria

D19-05 is accepted if every construct must receive a lawful route, source-local/quarantine/escalation governance is actionable, canon-candidate status is separated from canon, and informal outcomes are explicitly forbidden.
