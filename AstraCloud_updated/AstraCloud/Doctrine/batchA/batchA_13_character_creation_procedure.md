# batchA_13_character_creation_procedure

## 1. Purpose and authority

This file defines Astra doctrine for **legal character assembly procedure**.

Its job is to govern:
- assembly order
- dependency awareness
- prerequisite checking
- contradiction handling
- rollback / flagging behavior
- completion-state definitions
- lawful entry paths for native creation and donor conversion

This file is authoritative for:
- procedural order
- minimum valid record requirements
- legal completion states
- assembly-stage validation
- contradiction and rollback doctrine
- partial-record handling
- nonstandard-holder procedural handling

This file is **not** authoritative for the content of the layers it assembles.

This file does **not** own:
- player-chassis ontology
- stat architecture
- capability law
- access law
- ability schema
- resource law
- condition law
- damage-family law
- progression doctrine
- identity-layer content
- package content
- starting loadout law

Those belong to their respective Batch A files.

## 2. Scope boundaries

This file covers:
- how a lawful Astra character record is assembled
- what order of resolution is required
- what fields must exist for different valid record states
- what happens when contradictions or missing prerequisites appear
- how native creation, donor conversion, partial reconstruction, and optional randomized procedures remain lawful
- how bonded, companion-centered, platform-centered, or other nonstandard holders are handled procedurally

This file does not cover:
- option catalogs
- donor-specific chargen mini-games
- detailed package design
- full loadout assignment details
- full advancement progression choices beyond recording their lawful starting state

## 3. Core procedure principles

### 3.1 Procedure owns order, dependency, validation, and completeness

Procedure does not own the content of the layers it assembles.

### 3.2 Assembly occurs by reference to owning files

Astra character creation must assemble by reference to the governing doctrine files rather than restating or silently rewriting their contents.

### 3.3 No procedural backflow

No convenience in assembly order may overwrite or redefine earlier doctrine.

### 3.4 Illegal contradictions must be surfaced

If a later step reveals that an earlier step produced an illegal or incompatible state, the result must be:
- rollback,
- flagged invalidity,
- or quarantined partial status.

It must not be silently normalized away.

### 3.5 Multiple lawful record states exist

Not every lawful record is equally complete.
Astra recognizes conversion-valid, play-valid, and fully annotated records.

### 3.6 Multiple lawful entry paths exist

Native Astra creation is not the only legal creation path.
Astra must also support donor conversion, partial reconstruction, and optional randomized generation where doctrine allows it.

## 4. Character record states

### 4.1 Conversion-valid / assembly-valid

A **conversion-valid** or **assembly-valid** record contains enough structured data to map the donor or concept into Astra lawfully without inventing missing doctrine content.

A conversion-valid record may still be incomplete for table play.

### 4.2 Play-valid

A **play-valid** record contains all data required for lawful play use under current Astra doctrine.

### 4.3 Fully annotated

A **fully annotated** record is play-valid and also contains optional provenance, mapping notes, explanatory tags, conversion notes, or validation metadata.

### 4.4 Invalid or quarantined

A record is **invalid** if its contradictions break doctrine and cannot be lawfully tolerated.

A record is **quarantined** if it preserves useful conversion structure but cannot proceed further without doctrine refinement, missing-source recovery, or correction.

## 5. Entry paths

### 5.1 Native Astra creation

A character is assembled directly from Astra doctrine without donor-source reconstruction.

### 5.2 Donor-to-Astra conversion creation

A donor character, package, species, background, or sheet is translated into Astra form under the conversion-invariant law of `batchA_15_conversion_invariants.md`.

### 5.3 Partial reconstruction

A record is assembled from incomplete donor material, partial notes, damaged sheet data, or limited concept fragments.
Missing fields must be flagged rather than invented.

### 5.4 Optional randomized generation

Randomized selection or rolling is lawful only where doctrine explicitly allows it.
Randomization is a procedural option, not a replacement for doctrine.

## 6. Minimum valid character record

### 6.1 Minimum conversion-valid record

A conversion-valid record must minimally identify:
- actor baseline under `batchA_02_player_chassis_doctrine.md`
- enough identity-layer information to classify body/inheritance and learned/social formation under `11a` and `11b`
- enough current package information to classify present package structure under `12`
- enough progression-state information to identify starting advancement status under `10`
- enough stat-layer information to classify baseline numerical structure under `04`
- enough capability, access, and ability references to preserve donor function without illegal invention
- explicit flags for any missing, quarantined, or unresolved fields

### 6.2 Minimum play-valid record

A play-valid record must minimally include:
- valid actor baseline
- lawful identity-layer selections
- lawful package-layer selections
- lawful starting progression state
- lawful core stat and derived-stat outputs
- lawful capability, access, and ability selections or references
- required defensive / resistance / save outputs where applicable
- loadout-ready or explicitly loadout-pending status
- no unresolved contradictions that would break play

### 6.3 Fully annotated additions

A fully annotated record may additionally include:
- donor provenance
- source references
- mapping notes
- rationale notes
- validation tags
- unresolved watchlist items that do not break play

## 7. Assembly order and dependency rules

Astra uses a **dependency-aware legal order**.
This is not merely a convenience checklist.
Some stages must occur earlier, some can be derived later, and some validations only become possible after multiple layers are present.

### 7.1 Stage 1 — establish actor baseline

Confirm a lawful Astra player-grade actor baseline under `02`.

Required outcome:
- valid actor type
- lawful chassis assumptions
- any nonstandard holder or multi-frame note flagged early

### 7.2 Stage 2 — resolve body / inheritance identity

Resolve kinform, embodiment, substrate, and heritage under `11a`.

Required outcome:
- body / inheritance layers classified
- mutable or discontinuous embodiment flagged if relevant
- non-biological or hybrid origins classified lawfully

### 7.3 Stage 3 — resolve learned / social / formative identity

Resolve culture, homeland / formative environment, upbringing, factional imprint, profession-before-adventure, and event-layer overlays under `11b`.

Required outcome:
- persistent learned/social layers classified
- event-layer overlays separated from persistent identity
- formative affiliation distinguished from current authority

### 7.4 Stage 4 — resolve progression baseline

Record the character’s lawful starting progression state under `10`.

Required outcome:
- primary ascension axis starting state
- relevant supporting-axis starting states
- any package-gated or access-gated progression thresholds flagged

### 7.5 Stage 5 — resolve numerical baseline

Resolve base numerical architecture under `04`.

Required outcome:
- lawful primary stat structure
- required derived-stat inputs
- any multi-frame or platform-linked stat handling flagged

### 7.6 Stage 6 — resolve current package layer

Resolve primary package, grafts, traditions, profession packages, and bond/platform packages under `12`.

Required outcome:
- package function classified
- rigidity / acquisition legality checked
- package relationships recorded
- package hooks into progression, access, capability, and ability lawfully referenced

### 7.7 Stage 7 — resolve capability layer

Resolve practical capability selections and emphases under `05`.

Required outcome:
- lawful capability set or bundle
- profession-before-adventure and current package influence kept distinct
- no illegal collapse into access or ability layers

### 7.8 Stage 8 — resolve access layer

Resolve lawful permissions, qualifications, access tags, and gate conditions under `06`.

Required outcome:
- lawful access profile
- unresolved gating failures flagged
- no access grants inferred solely because a donor or package theme sounds related

### 7.9 Stage 9 — resolve ability layer and resource hooks

Resolve active ability objects under `07` and their relevant cost / cadence / risk surfaces under `07b`.

Required outcome:
- lawful ability object selections
- lawful references to access requirements
- lawful resource/cadence state references
- no ability payload invented to patch missing source data

### 7.10 Stage 10 — derive outputs and validate completion

Derive final outputs and run legality checks.

This includes:
- derived statistics
- defensive outputs
- starting resistance / save profile outputs
- package and bond/platform outputs where required
- record-state classification

## 8. Dependency and prerequisite checks

### 8.1 Dependency-aware, not purely linear

Astra assembly is dependency-aware.
Some steps are ordered; some are cross-validated later.

### 8.2 Earlier-stage ownership remains binding

A later-stage choice may depend on earlier-stage data, but it may not silently rewrite the earlier stage’s meaning.

### 8.3 Prerequisite law

A procedure must check:
- package entry legality
- access prerequisites
- progression thresholds
- identity-package incompatibilities where doctrine defines them
- nonstandard holder requirements
- bond/platform dependencies where applicable

## 9. Validation, contradiction, and rollback rules

### 9.1 Contradiction categories

Contradictions may include:
- missing mandatory layers
- illegal package combinations
- unresolved access failure
- impossible progression state
- package-holder mismatch
- identity/package confusion
- unsupported donor construct requiring invention
- missing required derived outputs

### 9.2 Lawful responses to contradiction

When contradiction is found, the procedure must choose one lawful response:
- rollback to the last stable legal stage
- flag the record invalid
- quarantine the record as partial / unresolved
- escalate for doctrine refinement if classification itself is blocked

### 9.3 Silent cleanup is prohibited

The procedure may not silently normalize a contradiction by inventing missing grants, erasing conflict, or quietly reclassifying donor material without justification.

## 10. Derived-output and completion checks

A final assembly pass must confirm:
- required derived values have been produced from lawful sources
- package references are complete enough for the target record state
- unresolved placeholders are explicitly flagged
- the record has been assigned one of the lawful completion states
- no unresolved contradiction remains hidden

## 11. Nonstandard holders, bonded/platform cases, and partial records

### 11.1 Nonstandard holders

Astra character assembly must support:
- multi-frame actors
- companion-centered packages
- bond / platform packages
- construct or AI holders
- platform-mediated actors
- unusual embodiment or relay structures

Procedure may not assume:
- one humanoid body
- one role package
- one equipment block
- one isolated action center

### 11.2 Bonded and platform-linked assembly

Where bond/platform logic exists, procedure must explicitly check:
- host vs bond/platform identity
- platform-linked stat ownership
- package-holder legality
- ability-source vs delivery-platform distinction
- shared or delegated access / resource handling if required

### 11.3 Partial records

A partial record may remain lawful for conversion if:
- missing fields are explicitly flagged
- no invented data is used to pretend completion
- the record state is clearly marked as conversion-valid, quarantined, or invalid rather than falsely play-valid

## 12. Optional randomization and alternate assembly methods

Random or semi-random procedures are lawful only when:
- doctrine allows them
- resulting choices still map to the owning framework files
- the procedure records that randomization was used
- no contradiction is hidden by the random method

Alternate procedural front-ends may exist, but they must still satisfy the same underlying legality rules.

## 13. Explicit exclusions and downstream ownership

This file does not redefine:
- actor ontology from `02`
- stat architecture from `04`
- capability law from `05`
- access law from `06`
- ability schema from `07`
- resource-cost law from `07b`
- condition or damage architecture from `08`, `09`, or `09b`
- progression law from `10`
- identity content from `11a` or `11b`
- package content from `12`
- loadout law from `14`

This file assembles those layers lawfully.
It does not own their content.
