# batchA_00_manifest.md

## Status
Draft — Core Now

## Authority
This file is the authoritative governance file for the **Batch A doctrine stack map**.

It defines:
- the official Batch A file roster,
- the intended scope of each file,
- the current dependency map,
- the recommended build order,
- the naming and status conventions for Batch A files,
- and the authoritative file ownership map for major doctrine questions.

It does **not** define:
- player-facing mechanics,
- setting lore,
- character options,
- numerical systems,
- progression values,
- conversion examples,
- or operational rules that belong to later doctrine files.

If any later Batch A file appears to contradict this file on **stack structure, file ownership, or boundary assignment**, this file governs unless the manifest is deliberately revised.

---

## 1. Purpose

Batch A is being built as a **modular doctrine stack**, not as one merged player-core chapter.

This file exists to prevent three common failure modes:
- file-boundary drift,
- duplicated authority,
- and silent reassignment of doctrine questions to the wrong file.

Its function is stack governance. It tells Astra doctrine where each kind of question belongs before the stack grows large enough to contradict itself.

---

## 2. Scope Boundaries

### 2.1 This file must include
- the official Batch A file roster,
- current file status labels,
- the intended scope of each file,
- dependency relationships,
- build order guidance,
- file naming rules,
- authority ownership by subject,
- and reserved or conditional file splits already recognized by doctrine.

### 2.2 This file must not include
- full mechanical rules,
- chassis doctrine details,
- resolution procedures,
- stat definitions,
- skill architecture,
- ability schema content,
- damage taxonomy content,
- progression logic content,
- origin package details,
- character creation steps,
- loadout rules,
- or donor conversion examples.

### 2.3 Interpretation rule
If a question asks **which Batch A file owns a concept, when that file should be built, or how it relates to neighboring files**, it belongs here.

If a question asks **how a rule itself works**, it belongs in the relevant doctrine file, not in this manifest.

---

## 3. Batch A Stack Role

Batch A is the foundational **player/chassis doctrine layer** of Astra Ascension.

Its job is to define stable player-facing framework architecture that can survive later conversion pressure from:
- fantasy systems,
- sci-fi systems,
- hybrid systems,
- cultivation systems,
- class and archetype systems,
- profession and background systems,
- skill and proficiency systems,
- spell, power, technique, maneuver, cyberware, biotech, psionic, relic, and tool-based systems,
- and unusual or esoteric donor subsystems.

Batch A is therefore not a donor summary packet. It is a conversion-stable doctrine layer.

---

## 4. Official Batch A File Roster

### 4.1 Core now
- `batchA_00_manifest.md`
- `batchA_01_lexicon_and_reserved_terms.md`
- `batchA_02_player_chassis_doctrine.md`
- `batchA_03_resolution_framework.md`
- `batchA_04_attribute_and_derived_stat_architecture.md`
- `batchA_05_competency_and_skill_translation_architecture.md`
- `batchA_06_access_tags_permissions_and_proficiency_gates.md`
- `batchA_07_ability_object_model.md`
- `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`
- `batchA_08_status_condition_and_effect_architecture.md`
- `batchA_09_damage_family_and_resistance_taxonomy.md`
- `batchA_10_progression_axes.md`

### 4.2 Soon after
- `batchA_11_origin_kinform_culture_and_background_framework.md`
- `batchA_12_path_archetype_and_profession_framework.md`
- `batchA_13_character_creation_procedure.md`
- `batchA_14_starting_loadout_and_kit_framework.md`
- `batchA_15_conversion_invariants.md`

### 4.3 Later expansion / reserve
- `batchA_09b_damage_fusion_and_compound_interactions.md`
- `batchA_16_translation_pattern_library_and_edge_cases.md`

### 4.4 Conditional split to watch
If file 11 expands beyond safe governance size or begins collapsing distinct identity layers into one document, split it into:
- `batchA_11a_biology_kinform_and_heritage_framework.md`
- `batchA_11b_culture_background_and_pre_ascendant_life_framework.md`

---

## 5. Recommended Build Order

Batch A build order is not identical to file-number order.

The current recommended build order is:
1. `batchA_02_player_chassis_doctrine.md`
2. `batchA_00_manifest.md`
3. `batchA_01_lexicon_and_reserved_terms.md`
4. `batchA_03_resolution_framework.md`
5. `batchA_04_attribute_and_derived_stat_architecture.md`
6. `batchA_05_competency_and_skill_translation_architecture.md`
7. `batchA_06_access_tags_permissions_and_proficiency_gates.md`
8. `batchA_07_ability_object_model.md`
9. `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`
10. `batchA_08_status_condition_and_effect_architecture.md`
11. `batchA_09_damage_family_and_resistance_taxonomy.md`
12. `batchA_10_progression_axes.md`
13. `batchA_15_conversion_invariants.md`
14. `batchA_11_origin_kinform_culture_and_background_framework.md`
15. `batchA_12_path_archetype_and_profession_framework.md`
16. `batchA_13_character_creation_procedure.md`
17. `batchA_14_starting_loadout_and_kit_framework.md`
18. `batchA_16_translation_pattern_library_and_edge_cases.md`

### Build-order doctrine note
Build order exists to reduce contradiction pressure. It does not by itself change file authority. A later-built file may still own a distinct doctrine question more authoritatively than an earlier file.

---

## 6. Scope Summary by File

### 6.1 `batchA_00_manifest.md`
Owns the Batch A file map itself: roster, scope boundaries, dependencies, naming rules, status flags, and authority ownership.

### 6.2 `batchA_01_lexicon_and_reserved_terms.md`
Owns controlled vocabulary, reserved meanings, deprecated donor terms, synonym rules, collision rules, and term-introduction discipline.

### 6.3 `batchA_02_player_chassis_doctrine.md`
Owns the definition of the Astra player-grade actor, valid routes into that state, mandatory chassis interfaces, and downstream assumptions about a valid player entity.

### 6.4 `batchA_03_resolution_framework.md`
Owns universal action-resolution doctrine, including tests, contests, opposed procedures, difficulties, outcome bands, criticals, and donor-resolution translation hooks.

### 6.5 `batchA_04_attribute_and_derived_stat_architecture.md`
Owns the stat skeleton: primary attributes, derived stats, defensive stats, initiative/speed/perception-style structures, and legal handling of donor stat imports.

### 6.6 `batchA_05_competency_and_skill_translation_architecture.md`
Owns the non-power competency layer: skills, proficiencies, expertises, knowledges, trades, disciplines, tool use, research competencies, and similar donor structures.

### 6.7 `batchA_06_access_tags_permissions_and_proficiency_gates.md`
Owns permission logic: domains, licenses, training tags, schools, traditions, armament permissions, armor permissions, implant clearance, relic access, and other lawful gate structures.

### 6.8 `batchA_07_ability_object_model.md`
Owns the universal schema for active abilities: fields, activation, targets, effect template, range, scaling, failure state hooks, upkeep hooks, recharge hooks, and upgrade hooks.

### 6.9 `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`
Owns resource economy doctrine: costs, expenditure structures, recharge models, cooldowns, charges, slots, fuel, stamina, heat, corruption, overcast, backlash, depletion, recovery, and similar donor economies.

### 6.10 `batchA_08_status_condition_and_effect_architecture.md`
Owns condition and non-damage effect logic: duration models, stacking, cleanse/remove/suppress logic, control states, buffs, debuffs, hazards, and persistent effect translation.

### 6.11 `batchA_09_damage_family_and_resistance_taxonomy.md`
Owns the core harm taxonomy: damage families, resistance/vulnerability/immunity/absorption/recovery interactions, and donor mapping for unusual harm categories.

### 6.12 `batchA_09b_damage_fusion_and_compound_interactions.md`
Owns later-stage compound damage behavior: fused families, catalytic interactions, layered secondary families, and other higher-complexity damage interactions if and when needed.

### 6.13 `batchA_10_progression_axes.md`
Owns advancement-lane doctrine: level/tier/rank equivalents, horizontal vs vertical growth, lineage or heritage growth, cultivation growth, role mastery, gear-linked growth, unlock cadence, and donor progression mapping.

### 6.14 `batchA_11_origin_kinform_culture_and_background_framework.md`
Owns the identity-layer framework below package selection: biology or kinform, ancestry or heritage, culture, homeland, upbringing, faction imprint, profession-before-adventure, and background events.

### 6.15 `batchA_12_path_archetype_and_profession_framework.md`
Owns package architecture for class, path, archetype, profession, vocation, and similar donor package layers.

### 6.16 `batchA_13_character_creation_procedure.md`
Owns legal assembly order: pick order, validation checkpoints, contradiction checks, and minimum data required for a valid Astra character build.

### 6.17 `batchA_14_starting_loadout_and_kit_framework.md`
Owns starter material doctrine: baseline starting wealth logic, kit categories, package-linked kits, scarcity assumptions, and starter legality rules.

### 6.18 `batchA_15_conversion_invariants.md`
Owns hard donor-conversion guardrails: what cannot be overwritten, what questions must be asked during mapping, what gets split or renamed, and what donor assumptions never become automatic Astra law.

### 6.19 `batchA_16_translation_pattern_library_and_edge_cases.md`
Owns non-authoritative worked mappings and weird-case examples for difficult donor subsystems.

---

## 7. Dependency Map

### 7.1 Foundational base
- `batchA_00_manifest.md` depends on no prior doctrine file for its existence, but it should reflect accepted project direction.
- `batchA_02_player_chassis_doctrine.md` is the first substantive doctrine anchor for the player entity.

### 7.2 Core dependency sequence
- `batchA_01_lexicon_and_reserved_terms.md` should be drafted after file 02 is stable enough to anchor player-facing terminology.
- `batchA_03_resolution_framework.md` depends on 02.
- `batchA_04_attribute_and_derived_stat_architecture.md` depends on 02 and 03.
- `batchA_05_competency_and_skill_translation_architecture.md` depends on 02, 03, and 04.
- `batchA_06_access_tags_permissions_and_proficiency_gates.md` depends on 02, 03, 04, and 05.
- `batchA_07_ability_object_model.md` depends on 03, 04, 05, and 06.
- `batchA_07b_resource_cost_recharge_and_backlash_architecture.md` depends on 03, 04, 06, and 07.
- `batchA_08_status_condition_and_effect_architecture.md` depends on 03, 04, and 07.
- `batchA_09_damage_family_and_resistance_taxonomy.md` depends on 03, 04, and 08.
- `batchA_10_progression_axes.md` depends on 02, 03, 04, 05, 06, 07, 07b, 08, and 09.

### 7.3 Secondary dependency sequence
- `batchA_15_conversion_invariants.md` depends on the prior core-now files because it governs conversion pressure across the established doctrine stack.
- `batchA_11_origin_kinform_culture_and_background_framework.md` depends on 02, 04, 05, 06, and 10.
- `batchA_12_path_archetype_and_profession_framework.md` depends on 05, 06, 07, 07b, 10, and 11.
- `batchA_13_character_creation_procedure.md` depends on 02 through 12 and on 15 where relevant for legality guardrails.
- `batchA_14_starting_loadout_and_kit_framework.md` depends on 04, 05, 06, 11, 12, and 13.

### 7.4 Reserve dependency sequence
- `batchA_09b_damage_fusion_and_compound_interactions.md` depends on 09 and usually on 08.
- `batchA_16_translation_pattern_library_and_edge_cases.md` depends on 15 and practically on the full stack.

### Dependency doctrine note
Dependencies indicate what a file must rely on for stable drafting. They do not permit a dependent file to redefine its parent file’s doctrine ownership.

---

## 8. Authoritative File for X Map

Use the following map whenever a doctrine question arises.

- “What is an Astra player-grade actor?” → `batchA_02_player_chassis_doctrine.md`
- “What words are legal, reserved, deprecated, or collision-prone?” → `batchA_01_lexicon_and_reserved_terms.md`
- “How are actions resolved?” → `batchA_03_resolution_framework.md`
- “What is the stat skeleton?” → `batchA_04_attribute_and_derived_stat_architecture.md`
- “What counts as a competency or skill-like structure?” → `batchA_05_competency_and_skill_translation_architecture.md`
- “How do permissions, proficiencies, or access gates work?” → `batchA_06_access_tags_permissions_and_proficiency_gates.md`
- “What fields define an active ability?” → `batchA_07_ability_object_model.md`
- “How do resource costs, recharge models, and backlash logic work?” → `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`
- “How do conditions and non-damage effects work?” → `batchA_08_status_condition_and_effect_architecture.md`
- “What are the core damage families and resistance relationships?” → `batchA_09_damage_family_and_resistance_taxonomy.md`
- “How do fused or compound damage interactions work?” → `batchA_09b_damage_fusion_and_compound_interactions.md`
- “How does advancement work across one or more axes?” → `batchA_10_progression_axes.md`
- “How are identity layers such as kinform, heritage, culture, and background separated?” → `batchA_11_origin_kinform_culture_and_background_framework.md`
- “How do classes, paths, archetypes, professions, or package layers work?” → `batchA_12_path_archetype_and_profession_framework.md`
- “What is the legal order for building a character?” → `batchA_13_character_creation_procedure.md`
- “What can a starting character legally begin with materially?” → `batchA_14_starting_loadout_and_kit_framework.md`
- “What donor assumptions may never overwrite Astra doctrine?” → `batchA_15_conversion_invariants.md`
- “How do edge-case donor subsystems map into Astra?” → `batchA_16_translation_pattern_library_and_edge_cases.md`
- “Which file owns which doctrine question?” → `batchA_00_manifest.md`

---

## 9. Naming Rules

### 9.1 Core naming pattern
Batch A doctrine files use the pattern:
`batchA_XX_descriptive_name.md`

Where:
- `batchA` identifies the doctrine batch,
- `XX` is the file index,
- and `descriptive_name` is a concise lower-case underscore-separated scope label.

### 9.2 Reserve and inserted files
When a later file must be inserted without destabilizing the numbering map, use suffix insertion such as:
- `07b`
- `09b`
- `11a`
- `11b`

### 9.3 Naming restrictions
File names must not:
- use donor system names unless the file is donor-specific by design,
- use vague poetic labels,
- collapse multiple unrelated doctrine domains into one label,
- or use synonyms that conflict with the lexicon once file 01 is formalized.

### 9.4 Stability rule
Once a file name becomes part of the active stack, rename it only when its scope is demonstrably wrong. Cosmetic renaming churn is clerical goblin energy and should be avoided.

---

## 10. Status Flags

Batch A files may use the following status labels.

### 10.1 `Draft — Core Now`
A current-priority foundational doctrine file actively being built.

### 10.2 `Planned — Core Now`
A current-priority foundational doctrine file whose scope is accepted but whose draft is not yet written.

### 10.3 `Draft — Soon After`
A file accepted for near-term construction after the core-now layer is stable enough.

### 10.4 `Planned — Soon After`
A near-term file whose role is accepted but not yet drafted.

### 10.5 `Reserved — Later Expansion`
A recognized future file that should not be treated as active core doctrine yet.

### 10.6 `Conditional Split`
A file or file pair that should only be activated if scope pressure makes the current combined file unstable.

### 10.7 `Superseded`
A file or version no longer authoritative because its scope has been replaced, split, or deliberately retired.

### 10.8 `Canonical`
A status only appropriate once a later formal Astra sourcebook process has ratified doctrine into canon. Batch A working doctrine should not casually self-label as canonical during active framework drafting.

---

## 11. Current File-State Snapshot

### 11.1 Drafted now
- `batchA_00_manifest.md` — Draft — Core Now
- `batchA_02_player_chassis_doctrine.md` — Draft — Core Now

### 11.2 Accepted but not yet drafted
- `batchA_01_lexicon_and_reserved_terms.md` — Planned — Core Now
- `batchA_03_resolution_framework.md` — Planned — Core Now
- `batchA_04_attribute_and_derived_stat_architecture.md` — Planned — Core Now
- `batchA_05_competency_and_skill_translation_architecture.md` — Planned — Core Now
- `batchA_06_access_tags_permissions_and_proficiency_gates.md` — Planned — Core Now
- `batchA_07_ability_object_model.md` — Planned — Core Now
- `batchA_07b_resource_cost_recharge_and_backlash_architecture.md` — Planned — Core Now
- `batchA_08_status_condition_and_effect_architecture.md` — Planned — Core Now
- `batchA_09_damage_family_and_resistance_taxonomy.md` — Planned — Core Now
- `batchA_10_progression_axes.md` — Planned — Core Now
- `batchA_11_origin_kinform_culture_and_background_framework.md` — Planned — Soon After
- `batchA_12_path_archetype_and_profession_framework.md` — Planned — Soon After
- `batchA_13_character_creation_procedure.md` — Planned — Soon After
- `batchA_14_starting_loadout_and_kit_framework.md` — Planned — Soon After
- `batchA_15_conversion_invariants.md` — Planned — Soon After
- `batchA_09b_damage_fusion_and_compound_interactions.md` — Reserved — Later Expansion
- `batchA_16_translation_pattern_library_and_edge_cases.md` — Reserved — Later Expansion
- `batchA_11a_biology_kinform_and_heritage_framework.md` — Conditional Split
- `batchA_11b_culture_background_and_pre_ascendant_life_framework.md` — Conditional Split

---

## 12. Governance Rules

### 12.1 No file may silently annex a neighboring scope
If a doctrine file begins answering questions assigned elsewhere, either move that content or deliberately revise the manifest.

### 12.2 Examples do not outrank doctrine
Worked examples, conversion outputs, and edge-case mappings may illustrate doctrine, but they do not redefine file ownership.

### 12.3 Donor pressure does not override the stack map
Strong donor structure may justify creating, splitting, or reordering files. It does not justify silently importing donor chapter structure as Astra doctrine law.

### 12.4 New files require boundary justification
If a new Batch A file is proposed, it must justify:
- what doctrine question it owns,
- why that question cannot be stably housed in an existing file,
- and what new dependency or authority consequences the addition creates.

### 12.5 Manifest revisions must be explicit
When the Batch A stack changes, revise this file directly rather than allowing the project to drift through chat memory and wishful fog.

---

## 13. Manifest-Specific Anti-Drift Rules

This manifest exists to actively resist:
- donor cosmology leakage,
- vocabulary drift,
- competency/access/ability collapse,
- damage-family underdesign,
- resource-economy underdesign,
- progression-axis collapse,
- identity-layer collapse,
- canon hierarchy confusion,
- and conversion/play contamination.

If future drafting pressure threatens one of those boundaries, revise the stack deliberately rather than pretending the issue will solve itself through vibes and bold formatting.

---

## 14. Immediate Next-Step Guidance

With `batchA_02_player_chassis_doctrine.md` established and this manifest now in place, the next file in the recommended build order is:

`batchA_01_lexicon_and_reserved_terms.md`

That file should formalize the controlled vocabulary needed to stop later Batch A files from using terms such as path, domain, skill, technique, kit, permission, proficiency, and Ascendant as soft interchangeable mush.

