# batchA_01_lexicon_and_reserved_terms.md

## Status
Draft — Core Now (Revised)

## Authority
This file is the authoritative terminology-control file for the **Batch A player/chassis doctrine stack**.

It governs:
- approved Astra terms,
- reserved terms,
- deprecated donor terms,
- collision and synonym rules,
- term-admission rules,
- and the distinction between doctrine vocabulary, table vocabulary, and metadata/tooling vocabulary.

It does **not** govern:
- full setting lore,
- full subsystem rules,
- complete donor glossaries,
- or final operational details owned by later doctrine files.

If a later Batch A file uses a governed term in a way that conflicts with this file, this file controls unless deliberately revised.

---

## 1. Purpose

Astra Ascension needs a controlled vocabulary because conversion drift usually begins as language drift.

When one term is used for multiple jobs, or multiple terms are used for one job, a framework starts collapsing identity, access, capability, ability, progression, and metadata into one blurred mass. This file exists to stop that collapse.

This file is therefore not a lore glossary and not a decorative dictionary. It is a terminology-control instrument.

Its job is to answer six questions:
- Which terms are approved for Astra use now?
- Which terms are reserved until their owning files define them more sharply?
- Which donor terms are recognized but not approved as Astra-native doctrine?
- Which terms are allowed at the table but should not govern doctrine?
- Which metadata terms are allowed for retrieval and tooling without becoming rules objects?
- How are new terms admitted without bloating the lexicon or muddying later conversion work?

---

## 2. Scope Boundaries

This file covers:
- term control,
- approved vocabulary,
- reserved vocabulary,
- donor deprecations,
- collision and synonym rules,
- tag subtype control,
- capitalization and formatting rules,
- and metadata/tooling terminology boundaries.

This file does **not** cover:
- complete mechanics for capability, access, abilities, progression, tags, or resources,
- complete ancestry, kinform, culture, or background catalogs,
- complete loadout or equipment doctrine,
- full lore definitions,
- or exhaustive one-to-one donor mappings.

Where a later file owns the operational rules for a concept, this file controls the term's guarded meaning while the later file controls its procedures.

---

## 3. Terminology Registers

Astra terminology is governed through three separate registers.

### 3.1 Table / common language
These are short, human-usable terms intended for ordinary rule text, examples, play guidance, and natural discussion.

These terms should be readable, stable, and not needlessly mechanical.

### 3.2 Doctrine / system language
These are controlled architecture terms used when precision matters.

These terms may be narrower and more technical than table language, but they must still earn their place.

### 3.3 Metadata / tooling language
These are indexing, routing, provenance, and retrieval terms.

These terms may be used by storage, search, reranking, or dataset pipelines. They are **not** rules objects unless a later doctrine file explicitly says so.

A term may appear in more than one register only if the overlap is deliberate and controlled.

---

## 4. Term Classes

All entries must belong to one of the following classes.

### 4.1 Approved term
Approved for Astra use now.

### 4.2 Reserved term
Recognized, but meaning is deliberately held narrow until later doctrine files define it more fully.

### 4.3 Deprecated donor term
Recognized during donor conversion, but not approved as Astra-native doctrine language.

### 4.4 Generic allowed term
Permitted as ordinary prose when precision is not required, provided it does not displace a controlled term.

### 4.5 Discouraged construction
A term or phrase whose use is likely to cause drift, donor leakage, false precision, or architecture confusion.

---

## 5. Core Governance Laws

### 5.1 One controlled term, one primary job
A controlled Astra term should have one primary doctrine job.

### 5.2 Do not invent Astra-sounding filler
A term is not justified because it sounds mystical, sleek, or branded. New vocabulary must solve a real problem.

### 5.3 Donor frequency does not create canon
A word used often in a donor system does not become Astra-native by repetition.

### 5.4 Table language and doctrine language are related, not identical
A readable table term may exist without becoming the most technical doctrine term.

### 5.5 Metadata language is never a rules object by default
A retrieval label, provenance marker, or routing field does not become a mechanic unless a later doctrine file explicitly says so.

### 5.6 A tag grants nothing by default
A tag classifies, marks, or describes. It grants no bonus, permission, effect, authority, or narrative force unless its subtype and behavior are explicitly defined.

### 5.7 Conditions and effects are not tags by default
Tags may reference conditions or effects, but they do not replace them unless a later subsystem deliberately says so.

### 5.8 Proper nouns are not framework nouns
Donor factions, places, cosmologies, regimes, events, and proprietary labels are not Astra framework terms unless deliberately adopted.

---

## 6. Approved Terms — First Pass

This first-pass approval list is intentionally conservative.

Each entry must define:
- what the term refers to,
- what job it performs,
- and what it explicitly does not include.

### 6.1 Table / common language approved terms

#### player
**Class:** approved  
**Register:** table/common  
**Owner file:** cross-stack usage

The human participant at the table or in play.
Use when referring to the real person making choices for a character.
Do not use as a synonym for character or actor.

#### character
**Class:** approved  
**Register:** table/common  
**Owner file:** `batchA_02_player_chassis_doctrine.md`

A fictional entity represented within play.
Use as the default natural-language term for a person, being, construct, or similar in-world figure.
Do not use as a synonym for player.

#### player character
**Class:** approved  
**Register:** table/common  
**Owner file:** `batchA_02_player_chassis_doctrine.md`

A character primarily controlled by a player during play.
Use as the default term for the player's in-world entity.
Do not use as a synonym for player.

#### Ascendant
**Class:** approved  
**Register:** table/common  
**Owner file:** `batchA_02_player_chassis_doctrine.md`

An Astra-native player-facing designation for a being that has crossed into advancement-relevant existence.
Use as an in-setting or player-facing term when Astra needs a distinct identity word beyond plain "character."
Do not use as proof of any single cosmological origin, resource model, or donor metaphysic.

### 6.2 Doctrine / system approved terms

#### actor
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_02_player_chassis_doctrine.md`

A rules-bearing entity that can take actions, receive effects, hold conditions, or interact with mechanics.
Use when a rule applies broadly across player characters, non-player characters, summons, hazards, constructs, zones, or similar entities.
Do not use as a synonym for player.

#### capability
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_05_competency_and_skill_translation_architecture.md`

A non-activated capacity such as a skill, proficiency, knowledge area, trade, practiced expertise, or learned know-how used during tasks and checks.
Use when referring to what an actor knows, can do, or is trained in outside discrete activated powers.
Do not use as a synonym for ability or access.

#### access
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_06_access_tags_permissions_and_proficiency_gates.md`

Lawful qualification or eligibility to use, equip, invoke, learn, attune to, or otherwise interact with a governed object, subsystem, or option.
Use when a rules layer is determining whether an actor may interact with something.
Do not use as a synonym for capability.

#### access tag
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_06_access_tags_permissions_and_proficiency_gates.md`

A controlled rules-side label used in access or gating logic.
Use to mark objects, actors, traditions, items, implants, relics, or other governed entities for access checking.
Do not use as a retrieval tag, narrative tag, or freeform donor keyword bucket.

#### proficiency gate
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_06_access_tags_permissions_and_proficiency_gates.md`

A threshold, requirement, or rule object that must be satisfied before lawful access is granted.
Use when a system needs explicit minimum qualification rather than loose permission language.
Do not use as a synonym for access itself.

#### ability
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_07_ability_object_model.md`

An activated expression such as a spell, technique, maneuver, stance, power, module, invocation, or similar rules object.
Use when referring to a discrete action-capable or activation-capable object.
Do not use as a synonym for attribute, capability, or access.

#### condition
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_08_status_condition_and_effect_architecture.md`

A defined state attached to an actor, object, zone, or similar target that changes how rules apply.
Use when the state has recognized rules meaning, duration, removal logic, or interaction logic.
Do not use as a synonym for tag or effect.

#### effect
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_08_status_condition_and_effect_architecture.md`

A rules outcome or ongoing rules-bearing result produced by an ability, condition, hazard, item, zone, or other source.
Use when referring to the operative consequence rather than the classifier attached to it.
Do not use as a synonym for condition or tag.

#### damage family
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_09_damage_family_and_resistance_taxonomy.md`

A controlled category of harm used for resistance, vulnerability, immunity, recovery, interaction, and conversion logic.
Use when classifying harm into stable Astra-recognized families.
Do not use as a synonym for weapon type, ability type, or narrative flavor text.

#### progression axis
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_10_progression_axes.md`

A distinct lane of advancement through which an actor can change over time.
Use when a system tracks growth through level, rank, cultivation stage, lineage development, mastery, augmentation, or similar advancement channels.
Do not use as a synonym for progression as a whole.

#### kinform
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_11_origin_kinform_culture_and_background_framework.md`

The biology-facing or form-facing identity layer of a being.
Use when referring to what kind of embodied being something is in structural terms.
Do not use as a synonym for culture, background, profession, or faction.

#### culture
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_11_origin_kinform_culture_and_background_framework.md`

The socially learned identity layer shaped by customs, norms, institutions, and inherited practice.
Use when referring to learned collective context rather than biology.
Do not use as a synonym for kinform or lineage.

#### background
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_11_origin_kinform_culture_and_background_framework.md`

The pre-adventure or pre-current-play life history layer that informs training, exposure, and starting context.
Use when referring to formative prior experience.
Do not use as a synonym for class, profession, or culture.

#### loadout
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_14_starting_loadout_and_kit_framework.md`

The equipped, carried, attached, or otherwise prepared material support state of an actor.
Use when referring to what an actor begins with or currently has ready for use.
Do not use as a synonym for wealth, inventory as a whole, or background.

#### resource model
**Class:** approved  
**Register:** doctrine/system  
**Owner file:** `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`

The structured economy governing costs, charges, replenishment, recharge, expenditure, or backlash for abilities and related systems.
Use when referring to the governing logic behind resource use.
Do not use as a synonym for any one donor resource such as mana, stamina, psi points, essence, or aether.

### 6.3 Metadata / tooling approved terms

#### retrieval tag
**Class:** approved  
**Register:** metadata/tooling  
**Owner file:** cross-stack retrieval layer

Metadata used for indexing, filtering, routing, retrieval, or reranking.
Use when marking records for search or pipeline behavior.
Never treat as a rules object.

#### doctrine tag
**Class:** approved  
**Register:** metadata/tooling  
**Owner file:** stack governance

Metadata describing framework ownership, scope, layer, authority, or file relationship.
Use when marking records for doctrine maintenance or corpus organization.
Never treat as a play mechanic.

#### donor tag
**Class:** approved  
**Register:** metadata/tooling  
**Owner file:** conversion pipeline

Metadata identifying donor provenance, source family, or conversion context.
Use when preserving source awareness during conversion and consolidation.
Never treat as a play mechanic.

---

## 7. Reserved Terms

These terms are recognized, but their meanings are not yet stable enough for broad Astra approval. They remain controlled and narrow until their owning files define them more sharply.

### 7.1 Reserved umbrella terms
- `tag`
- `keyword`

### 7.2 Reserved progression / identity / metaphysic terms
- `path`
- `domain`
- `skill`
- `technique`
- `school`
- `tradition`
- `archetype`
- `profession`
- `lineage`
- `heritage`
- `soul`
- `spirit`
- `essence`
- `aether`
- `rank`

### 7.3 Reserved narrative or descriptive tag terms
- `narrative tag`
- `scene tag`
- `trait tag`
- `keyword tag`

A reserved term is not free for loose use. It is being held in controlled suspension until its owning doctrine file exists.

---

## 8. Deprecated Donor Terms

Deprecated donor terms may appear in donor-bound conversion contexts, notes, and mappings, but they are not approved as Astra-native default vocabulary.

Examples include donor-specific proper nouns, donor-specific cosmological regimes, donor-specific resource names, donor-specific faction labels, and donor-specific proprietary subsystem labels.

Examples from RHBF or RHBF-adjacent donor pressure include:
- `Path of Ascendancy`
- `Engineers` when used as a metaphysical category rather than a plain profession label
- donor-specific place names
- donor-specific faction names
- donor-exclusive resource pairings such as `Essence` and `Aether` when treated as universal law
- donor-exclusive event or regime names

These terms may be preserved where fidelity to a donor text requires them, but they do not become Astra doctrine by repetition.

---

## 9. Discouraged or Demoted Constructions

These terms are not approved core terminology at this stage because they are either too abstract, too vague, or trying to solve the wrong problem too early.

### 9.1 Demoted for now
- `player-grade actor`
- `chassis`
- `interface`
- `permission`
- `origin layer`
- `path package`

### 9.2 Why they are demoted
- `player-grade actor` collapses player, character, and actor into one muddy label.
- `chassis` is a useful concept but not yet a necessary approved noun.
- `interface` is too vague to control reliably.
- `permission` is serviceable but less clear and less readable than `access`.
- `origin layer` is premature until later files define origin structure more fully.
- `path package` is too early to stabilize before the package framework exists.

A demoted term may re-enter later if a future file proves it is necessary and can define it sharply.

---

## 10. Collision and Synonym Rules

### 10.1 Player / character / actor
- `player` means the human participant.
- `character` means the fictional entity.
- `player character` means the character primarily controlled by a player.
- `actor` means the generalized rules-bearing entity.

Do not use these interchangeably.

### 10.2 Capability / ability / access
- `capability` covers non-activated practical capacity and learned know-how.
- `ability` covers activated powers or discrete activation-capable objects.
- `access` covers eligibility, authorization, and lawful qualification.

Do not use one as a synonym for the others.

### 10.3 Access tag / retrieval tag / doctrine tag / donor tag
- `access tag` is a rules-side gating label.
- `retrieval tag` is metadata for search and routing.
- `doctrine tag` is metadata for framework ownership and maintenance.
- `donor tag` is metadata for provenance and conversion context.

Do not collapse metadata tags into rules tags.

### 10.4 Kinform / culture / background
- `kinform` is biology-facing or embodiment-facing.
- `culture` is socially learned.
- `background` is formative prior life experience.

Do not let species, upbringing, social norms, and professional history collapse into one bucket.

### 10.5 Condition / effect / tag
- `condition` is a defined state with rules meaning.
- `effect` is the operative rules consequence.
- `tag` is a reserved umbrella that may later classify or describe, depending on subtype.

Do not treat conditions or effects as generic tags by default.

### 10.6 Resource model / donor resource name
Use `resource model` for the governing structure.
Do not use donor resource nouns as if they are Astra-universal framework words.

### 10.7 Path / profession / archetype / school / tradition
These are reserved because donor systems use them for different jobs.
Do not treat them as synonyms until their owning files define them.

---

## 11. Tag Taxonomy — First-Pass Control

`tag` is not an approved operational core term at this stage. It is a reserved umbrella that requires subtype control.

Astra currently recognizes the following tag classes in principle:

### 11.1 Metadata / tooling tag classes
- `retrieval tag`
- `doctrine tag`
- `donor tag`

These are never play mechanics by default.

### 11.2 Rules-side tag classes
- `access tag`
- `keyword` / `keyword tag`

These may participate in mechanics when their owning files define their behavior.

### 11.3 Narrative / descriptive tag classes
- `narrative tag`
- `scene tag`
- `trait tag`

These may describe truths, situations, or descriptors, but they do not create mechanics by default.

### 11.4 Hard law for all tag classes
A tag grants nothing by default unless its subtype and mechanical behavior are explicitly defined.

---

## 12. Metadata / Tooling Language Rules

### 12.1 Metadata must remain metadata
Tooling terms exist to support indexing, filtering, routing, retrieval, reranking, provenance control, and corpus maintenance.

They must not quietly become rules objects.

### 12.2 Lexicon entries should remain exportable
Where lexicon entries are represented in retrieval infrastructure, prefer stable, simple fields such as:
- `term_id`
- `canonical_term`
- `term_class`
- `register`
- `owner_file`
- `status`
- `allowed_aliases`
- `disallowed_aliases`
- `doctrine_tags`
- `retrieval_tags`
- `donor_tags`

### 12.3 Flat fallback rule
Metadata should remain portable enough to survive systems that prefer simple key-value records over nested structures.

---

## 13. Allowed Aliases and Continuity Notes

### 13.1 capability / competency
`capability` is the preferred Astra term.
`competency` may remain as a controlled continuity alias where existing filenames, drafting history, or legacy notes still use it.

This allows `batchA_05_competency_and_skill_translation_architecture.md` to keep its filename for stability while preferring `capability` in doctrine text.

### 13.2 access / permission
`access` is the preferred Astra term.
`permission` may be used sparingly as a generic descriptive word, but not as the preferred controlled doctrine term.

---

## 14. Formatting Rules

### 14.1 Capitalization
Use lowercase for framework nouns unless a term is a proper noun or a deliberately capitalized in-setting title.

### 14.2 Plurals
Pluralize naturally unless a later file defines a controlled plural form.

### 14.3 First-use rule
On first important use in a doctrine file, prefer the canonical approved term rather than an alias.

---

## 15. Term Admission Rule

A new term may be admitted only if it does at least one of the following:
- resolves a real collision,
- prevents donor leakage,
- names a necessary concept not already covered,
- or improves precision without reducing readability.

A new term must not be admitted merely because it sounds more Astra.

When proposing a new term, specify:
- the proposed term,
- its register,
- its owner file,
- the concept it names,
- the term it is replacing or refining,
- and the confusion it prevents.

---

## 16. Future File Reservation

The current lexicon reserves space for a future file:

`batchA_08b_tag_keyword_and_descriptor_architecture.md`

Expected purpose:
- define Astra-recognized tag classes,
- distinguish metadata tags from rules tags,
- distinguish keyword tags from narrative tags,
- define whether tags are descriptive, invoked, spent, compelled, stacked, or purely classificatory,
- define which tags may exist on actors, items, scenes, zones, abilities, and conditions,
- and define default interaction law for tag-heavy donor systems.

This future file is not required before `batchA_02`, but the lexicon acknowledges the gap now so later donor conversions do not improvise through it.

---

## 17. Summary Constraint

This lexicon is intentionally stricter and smaller than a full glossary.

Its purpose is not to finalize every future Astra equivalent in advance.
Its purpose is to stabilize the terms Astra needs now, reserve the terms Astra cannot safely finalize yet, and keep metadata language from pretending to be rules language.

---

## 18. Cosmology-Local Quarantine Tag

### 18.1 Tag definition

**Tag:** `[cosmology-local]`

**Register:** metadata/tooling (never a rules object)

**Owner file:** `batchA_01_lexicon_and_reserved_terms.md`

**Purpose:** Marks any conversion output text that contains donor-specific metaphysical explanation of advancement, power source, cosmic agency, or origin narrative. Tagged content is retained for reference but must not be promoted to Astra doctrine without explicit adjudication.

### 18.2 When to apply

Apply `[cosmology-local]` to any passage or block that:
- explains **how** a donor system's cosmological framework works (not merely that something is powerful or advanced),
- attributes a character's power, growth, or nature to a specific donor-cosmological source (e.g., "bounded to the dying star's will," "ascendant through planetary resonance," "chosen by the Eternal Court"),
- names donor-proprietary cosmological regimes, agencies, forces, or laws as if they were Astra-universal structural law,
- or explains the metaphysical origin of game mechanics in donor-specific terms.

### 18.3 When not to apply

Do **not** apply `[cosmology-local]` to:
- plain mechanical descriptions that happen to mention setting flavor,
- Astra-native terminology already approved in Section 6 of this file,
- world-building notes that do not purport to be structural doctrine,
- or content already tagged `[source-local]` (no double-tagging needed if source-local already applies).

### 18.4 Enforcement

The lexicon validator (`astra_cloud.validators.LexiconValidator`) scans conversion output for known cosmological signal phrases. If signals are found without a `[cosmology-local]` tag present in the text, the validator returns a `FAIL` outcome on the `cosmology_untagged` check.

Conversion operators may apply the tag manually during review, or prompts may be instructed to auto-tag passages that match cosmological explanation patterns.

### 18.5 Promotion rule

A passage tagged `[cosmology-local]` may only be promoted to Astra structural doctrine through explicit adjudication logged in `data/canon/adjudicated/`. Repetition alone does not promote a cosmology-local passage — no matter how many donor conversions contain similar content.

### 18.6 Relationship to batchA_15

Section 18 supplements batchA_15's prohibition on donor cosmology becoming Astra default law. `batchA_15` states the rule; this section provides the tagging instrument by which conversion outputs declare compliance.

If a conversion produces cosmologically explanatory text without tagging it `[cosmology-local]`, it is in potential violation of batchA_15's source-local containment requirement and must be reviewed before canon promotion.
