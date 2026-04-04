# batchC_12_random_tables_events_oracles_and_generator_schema.md

## Purpose and authority

This file defines the **generator, table, oracle, and structured emission schema** for Astra Ascension.

Its job is to define how Astra represents **roll tables, event tables, oracle structures, selector structures, generator shells, encounter emitters, mission-complication emitters, travel event emitters, region or sector event emitters, pre-play prompt emitters, and other generation-heavy content forms** that produce, select, vary, prompt, assemble, mutate, route, chain, or procedurally surface content.

This file is doctrine for **generation-shaped schema structures**.
It does **not** define the full content family being emitted.
It does **not** define mission/scenario structure.
It does **not** define reward parcel structure.
It does **not** define site, faction, challenge, actor, or item ontology.
It does **not** define sourcebook appendix packaging.
It does **not** define campaign-overlay engines that exceed ordinary generator scope.

C12 exists because a large donor corpus does not merely contain authored content entries.
It also contains structured systems that emit content, prompts, inserts, complications, events, distributions, and state-reactive variations.
These systems cannot safely be collapsed into the content families they emit, nor into one generic “random table” category.

C12 therefore owns the schema grammar for:
- generator shells
- table structures
- oracle structures
- selector media and selection structures
- consult-input grammar
- generator job distinctions such as selector, assembler, mutator, and router
- emission units and emission topologies
- generated instance distinctions
- emission validity, rejection, fallback, substitution, and suppression behavior
- advisory vs mandatory insert posture
- informational truth-status and bias posture at generator scale
- state-reactive emission grammar
- depletion and refresh grammar
- consult authority and interpretation authority
- chaining and nested generator grammar
- attachment and context-scope grammar
- authored, normalized, generated, and instantiated generator distinctions

C12 remains **schema doctrine**, not converted output, not canon, not a table appendix, and not a junk drawer for every list-shaped donor artifact.

## Relationship to Batch C authority

This file inherits:
- `batchC_00_manifest.md`
- `batchC_01_common_content_schema_conventions_and_record_grammar.md`

This file must remain consistent with the established Batch C family boundaries for:
- `batchC_02_actor_creature_npc_and_adversary_schema.md`
- `batchC_03_template_variant_overlay_and_modifier_schema.md`
- `batchC_04_item_relic_resource_and_asset_content_schema.md`
- `batchC_06_site_region_settlement_and_locale_schema.md`
- `batchC_07_faction_institution_polity_and_social_body_schema.md`
- `batchC_08_traps_hazards_puzzles_trials_and_setpiece_challenge_schema.md`
- `batchC_09_encounter_scene_packet_and_composition_schema.md`
- `batchC_10_mission_scenario_arc_and_adventure_path_conversion_schema.md`
- `batchC_11_reward_loot_salvage_claim_and_inflow_parcel_schema.md`
- `batchC_13_sourcebook_bundle_gazetteer_and_reference_container_schema.md`

If a donor structure cannot be represented cleanly as an ordinary generator, oracle, or event-emitter without hiding a distinct campaign overlay or repeatable subsystem packet, that strain should be escalated toward the reserved `batchC_14_subsystem_packet_and_campaign_overlay_schema.md` rather than hidden inside C12.

C12 must also remain consistent with C01 identity, revision, derivative, and pinned-history discipline. Generator records are especially vulnerable to quiet drift because small changes to result weights, refresh behavior, state-reactivity, or chain rules can materially alter emitted content behavior. This file must therefore preserve distinctions such as:
- template identity vs generator instance identity
- shell identity vs emitted-result identity
- revision-in-place vs derivative generator line
- pinned historical generator variant vs current normalized variant
- attachment-local override vs new generator derivative

If local overrides materially alter weighting, result space, depletion scope, chain behavior, consult authority, or state-reactivity, those overrides should be reviewed for promotion into a distinct derivative generator rather than left indefinitely as silent attachment-local tweaks.

## Why C12 must exist

A generator schema is mandatory for corpus-scale conversion.

Astra must be able to represent donor structures such as:
- wandering encounter tables
- rumor tables
- clue or discovery oracles
- mission complication tables
- job or contract generators
- salvage-yield tables
- region or sector events
- weather and hazard emission tables
- travel event tables
- downtime event structures
- faction incident emitters
- restock or repopulation tables
- layered oracle prompts
- multi-roll assembled result generators
- nested or chained event structures
- state-reactive event systems
- bounded procedural shells that repeatedly emit inserts
- lifepath or origin generators
- pre-play setup prompt structures
- schedule, ranking, draw, or matrix selectors that are generator-shaped without looking like ordinary row/range tables

These are not interchangeable.
A wandering encounter table is not the same as an encounter packet.
A mission complication table is not the same as a mission.
A salvage-yield generator is not the same as a reward parcel.
A region event table is not the same as a site record.
A faction rumor table is not the same as a faction entry.
A procedural mission board is not the same as an authored scenario.
An oracle prompt engine is not the same as a deterministic lookup table.
A lifepath selector is not the same as a background content instance.
A calendar selector is not the same as an authored timeline.

Without C12, later conversion work will tend to fail in one of ten ways:
1. treat generators as if they were the content families they emit
2. treat all generation-heavy material as simple tables
3. treat a generated result as if it were the generator schema itself
4. collapse mission, encounter, or reward generation into C10, C09, or C11
5. treat appendix collections as generator identity
6. hide state-reactive or chained emission logic in prose without schema ownership
7. flatten oracle-style ambiguity into determinate lookup structures
8. mistake selector media for mere presentation style
9. mistake pre-play or lifepath generators for flavor appendices or authored setup prose
10. smuggle campaign overlays into C12 under the label of “event generators”

C12 exists to stop those failures.

## Core doctrinal center

The doctrinal center of C12 is:

**C12 owns the schema by which Astra represents structured content emission.**

In Astra terms, C12 owns the structure of:
- what kind of generator this is
- what procedural job it performs
- what selector medium it uses
- what context it attaches to
- what activates it
- what inputs it consults against
- how it emits
- how it validates, suppresses, falls back, substitutes, or defers results
- what kinds of output it can produce
- what state changes, depletion states, or refresh rules affect it
- whether it produces prompts, references, inserts, bundles, or chained consults
- what later content family receives the emitted result
- whether the generated result is advisory, mandatory, additive, replacement, escalating, or null

C12 is therefore about **generator-shaped structures and their emission behavior**.
It is not about the fully defined content family that receives the emission.

## What C12 owns

C12 owns:
- generator family distinctions
- generator shell vs generated instance distinctions
- table vs oracle vs generator distinctions
- selector media distinctions
- selector vs assembler vs mutator vs router distinctions
- consult-input grammar
- emission-unit grammar
- emission topology grammar
- output-target grammar
- attachment and context-scope grammar
- consult-mode grammar
- consult-authority and interpretation-authority grammar
- weighting, range, and selection-structure grammar
- state-reactive emission grammar
- truth-status and bias posture for informational outputs at generator scale
- emission validity, invalidity, rejection, fallback, substitution, and suppression grammar
- depletion, exhaustion, uniqueness, memory-scope, and refresh grammar
- chaining and nested-consult grammar
- advisory vs mandatory insertion posture
- density distinctions for generated outputs
- template, archetypal, instance, and generated generator distinctions

## What C12 does not own

C12 does **not** own:
- actor ontology
- item ontology
- site ontology
- organization ontology
- challenge-object ontology
- encounter packet ontology
- mission/scenario architecture
- reward parcel architecture
- sourcebook appendix packaging
- campaign-overlay engines that dominate play through their own turn structure
- donor content dumps consisting only of raw copied tables without schema discipline

## Scale ladder and generator place in Batch C

For Batch C routing discipline, Astra should recognize the following scale relation for generation-heavy structures:

1. **Underlying target entry or target family**
   One actor, site, packet, parcel, modifier, mission hook, challenge object, identity seed, or other target content family that a generator can emit toward.

2. **Emission unit**
   One result, band, row, branch, prompt, modifier output, chained consult, or generated insert produced by a generator consult.

3. **Generator record**
   One generator shell, table, oracle, event emitter, selector, or chained generator owned by C12.

4. **Generator cluster**
   Several linked generators that remain distinct because they differ in scope, activation, output target, refresh profile, consult authority, or chain role.

5. **Composition consumer**
   A C09 packet, C10 mission/scenario structure, C11 parcel, or other schema family that receives generator output.

6. **Container packaging**
   A C13 structure that groups generators into appendices, travel kits, rumor packs, event chapters, GM toolkits, or sourcebook bundles.

C12 owns level 3 directly and defines level-2 emission-unit logic where needed.
C12 may acknowledge level 4 as linked generator aggregation, may reference level 1 target families, may feed level 5 consumers, and may be packaged by level 6, but it does not own those other layers.

## Dominant-function routing rules

All candidate C12 content must be routed by **dominant structural job**, not by donor presentation style.

A record belongs in C12 when its main job is to define:
- structured emission
- random or conditional selection
- oracle prompting
- event emission
- generator chaining
- state-reactive content surfacing
- repeatable content-intake or content-variation shells

A record does **not** belong in C12 merely because it is presented in list form or because it contains numbered results.

If the dominant job is defining the underlying content family, route to that content file.
If the dominant job is defining encounter composition, route to C09.
If the dominant job is defining mission or scenario structure, route to C10.
If the dominant job is defining reward parcel structure, route to C11.
If the dominant job is packaging tables or generators as a publication collection, route to C13.
If the dominant job is a distinct overlay engine with turn logic, escalation cycles, domain management, faction-war turns, or comparable campaign packet behavior, escalate toward C14.

## Generator shell, table, oracle, emission unit, and generated instance distinctions

C12 must preserve several distinct layers that donors often blur together.

### Generator shell

A **generator shell** is the persistent schema structure that defines how emission occurs.

### Table

A **table** is a generator form whose emission is organized through enumerated rows, ranges, weighted entries, indexed results, or other lookup-like structures.

### Oracle

An **oracle** is a generator form that produces prompts, interpretive guidance, answer-bands, directional cues, or ambiguity-shaped outputs rather than only determinate enumerated results.

### Emission unit

An **emission unit** is the immediate output of one consult or one stage of a consult.
An emission unit may be a row result, a band result, a prompt, a content reference, a modifier, a chained consult instruction, a null, or a generated insert bundle.

### Generated instance

A **generated instance** is the concrete output created by consulting a generator shell.

### Distinction principles

1. Generator shell is not generated instance.
2. Table is one generator form, not the entire class.
3. Oracle is not merely a “fuzzy table.”
4. Emission unit is not automatically a fully formed content record.
5. A generated instance may remain sparse, advisory, or partial rather than fully compositional.

## Selector media doctrine

C12 must explicitly support selector media broader than ordinary dice-index tables.
A 500+ donor corpus will include many structures that are generator-shaped without presenting as conventional row/range tables.

### Selector media classes
When relevant, Astra should distinguish:
- dice or index lookup
- repeated-entry weighting
- matrix or cross-reference lookup
- draw-without-replacement
- card or deck style draw
- token or pool draw
- schedule or calendar selector
- ranked-band selector
- choose-list with constraints
- state-filtered option set

### Selector media principles

1. Selector medium is not the same as generator family.
2. Strange presentation forms must not be flattened into ordinary lookup tables merely because they are easier to parse.
3. A schedule selector is not automatically a timeline.
4. A ranked-band selector is not automatically a deterministic lookup.
5. A choose-list with constraints is still generator-shaped when it structures emission from a bounded option space.

## Generator jobs: selector, assembler, mutator, and router

Many donor generators differ more by procedural job than by visible format.
C12 should preserve this.

### Selector
A generator that chooses one or more results from a result space.

### Assembler
A generator that composes several selected pieces into one larger generated bundle.

### Mutator
A generator that changes an existing result, state, packet, or content relation rather than selecting a wholly new one.

### Router
A generator that sends the user toward another generator, result space, content family, or branch path.

### Job principles

1. One generator may perform more than one job, but one job often dominates.
2. A rumor table often acts as a selector.
3. A lifepath engine often acts as an assembler.
4. A weather escalation table often acts as a mutator.
5. A “consult subtable if...” structure often acts as a router.
6. Job difference is important for later conversion even when visible presentation looks similar.

## Generator family, function, posture, and source-state relation

C12 must distinguish several different kinds of classification.

### Generator family

Generator family identifies **what kind of generator** the record is.
Examples include:
- lookup table
- weighted table
- event table
- encounter table
- oracle
- nested generator
- chained generator
- state-reactive generator
- depletion or refresh generator
- attachment-bound generator
- campaign-scope event emitter
- mixed-output generator

### Generator function

Generator function identifies **what the generator is for**.
Examples include:
- complication emission
- pacing variation
- discovery prompting
- atmospheric variation
- travel disruption
- reward shaping
- encounter surfacing
- rumor surfacing
- clue seeding
- escalation pulsing
- replenishment or restock
- contract generation
- pressure mutation
- faction incident surfacing
- identity or origin seeding
- relationship seeding
- pre-play setup prompting

### Generator posture

Generator posture identifies **how the generator behaves** with respect to determinacy, reuse, insertion force, and volatility.
Examples include:
- determinate lookup
- weighted variable
- interpretive oracle
- advisory promptive
- mandatory insertive
- optional additive
- replacement-emissive
- escalating
- depleting
- refreshable
- once-per-context
- persistent shell with repeated consults

### Source-state relation

Source-state relation identifies **what contextual condition or state relation the generator expects to consult against**.
Examples include:
- travel-state relation
- site-state relation
- alert-state relation
- scarcity-state relation
- faction-posture relation
- mission-stage relation
- rest-cycle relation
- successor-state relation
- region-condition relation
- legitimacy-state relation
- audience or visibility-state relation

Family, function, posture, and source-state relation must not be collapsed into one label.

## Core C12 generator families

C12 should support the following major generator families.
These are not all interchangeable and should not be flattened into one universal table schema.

### 1. Lookup table

A generator structured primarily through determinate indexed or ranged lookup results.

### 2. Weighted table

A generator whose structure depends materially on weighting, repeated entries, probability bands, or uneven distribution.

### 3. Event table

A generator that emits events, incidents, developments, interruptions, or situational changes at a defined scope.

### 4. Encounter table

A generator that emits encounter candidates, encounter prompts, encounter references, or encounter modifiers.
It does not itself define encounter packet structure.

### 5. Oracle

A generator that emits promptive, interpretive, answer-band, directional, thematic, or ambiguity-preserving outputs.

### 6. Nested generator

A generator whose results direct the user to consult one or more additional generators or generator branches.

### 7. Chained generator

A generator whose outputs accumulate across ordered or conditional consult stages to assemble a more complex result.

### 8. State-reactive generator

A generator whose available outputs, weights, or consult behavior change based on tracked state.

### 9. Depletion or refresh generator

A generator whose results exhaust, rotate, recycle, refresh, or otherwise change over repeated use.

### 10. Attachment-bound generator

A generator that exists primarily as a subordinate emission structure attached to a site, mission, packet, region, faction, travel shell, downtime shell, or other parent structure.

### 11. Mixed-output generator

A generator that may emit prompts, references, modifiers, parcels, packets, or chained consults in one structured shell.

### 12. Procedural shell emitter

A bounded reusable shell that repeatedly emits content inserts, missions, complications, prompts, or events without itself becoming full scenario architecture.

## Generator granularity doctrine

C12 must preserve generator granularity explicitly.

### Granularity classes
- atomic generator
- multi-stage generator
- linked generator cluster
- container or appendix grouping

### Granularity principles

1. One donor “table” may actually normalize into several generators.
2. A multi-stage generator remains one generator when its consult stages share one structural identity line.
3. A linked generator cluster should remain plural when components differ materially in activation profile, scope, target profile, refresh profile, consult authority, or chain role.
4. Container or appendix grouping is not generator identity and belongs to C13.

## Common generator-record grammar for C12

All C12 records should inherit common Batch C record grammar from C01 and then add the following generator groups as needed.

### A. Structural identity group
- generator_family
- generator_function_profile
- generator_posture
- source_state_relation
- selector_medium
- generator_job_profile
- generator_granularity
- generator_scale
- template_status
- archetypal_normalization_status
- authored_normalized_generated_status
- structure_identity_line
- derivative_or_revision_status
- pinned_variant_status

### B. Provenance and normalization group
- donor_presented_form
- normalization_basis
- compression_or_expansion_notes
- omitted_or_externalized_components
- unresolved_conversion_strains

### C. Attachment and scope group
- attachment_profile
- attachment_target_refs
- attachment_host_topology
- consult_scope
- context_scope
- target_context_requirements
- parent_structure_dependency_refs

### D. Activation and consult group
- activation_profile
- consult_mode
- consult_trigger_refs
- consult_input_profile
- consult_input_refs
- consult_authority_profile
- interpretation_authority_profile
- optional_or_mandatory_status
- consult_frequency_profile
- entry_consult_rules
- repeat_consult_rules
- lockout_rules

### E. Emission structure group
- emission_unit_type
- emission_topology
- result_band_structure
- weighting_profile
- range_or_index_structure
- null_or_empty_result_rules
- validity_rejection_rules
- fallback_or_substitution_rules
- replacement_or_additive_rules
- escalation_or_mutation_rules

### F. Output-target group
- output_target_profile
- output_target_refs
- output_density_profile
- output_force_profile
- prompt_vs_reference_profile
- generated_insert_profile
- chained_consult_refs
- downstream_consumer_refs

### G. State-reactivity and refresh group
- reactivity_profile
- state_input_refs
- depletion_profile
- exhaustion_profile
- uniqueness_scope
- refresh_profile
- reset_conditions
- result_removal_or_rotation_rules
- persistent_memory_profile

### H. Interpretation and ambiguity group
- interpretive_band_profile
- answer_band_profile
- ambiguity_preservation_profile
- informational_truth_status_profile
- provenance_or_bias_profile
- user_inference_requirements
- open_cue_burden_profile
- free_prompt_constraints

### I. Generated-instance group
- generated_instance_status
- generated_instance_density
- generated_instance_duration_or_persistence
- generated_instance_binding_rules
- generated_instance_cleanup_rules

C12 does not require every generator to use every field group.
It does require every generator to use the groups justified by its family and posture.

## Attachment and context-scope doctrine

Generators rarely float free of context.
C12 must preserve how a generator attaches to the structures that consult it.

### Attachment classes
When relevant, Astra should distinguish:
- free-standing generator
- site-attached generator
- region-attached generator
- faction-attached generator
- challenge-attached generator
- packet-attached generator
- mission-attached generator
- scenario-shell-attached generator
- travel-shell-attached generator
- downtime-shell-attached generator
- sector-attached generator
- successor-state-attached generator

### Attachment host topology classes
When relevant, Astra should distinguish:
- single host attachment
- host-plus-state attachment
- mission-plus-stage attachment
- packet-plus-alert posture attachment
- region-plus-condition band attachment
- faction-plus-public-standing attachment
- successor-state-plus-continuity-burden attachment
- mixed host attachment

### Context-scope classes
When relevant, Astra should distinguish:
- local scene scope
- packet scope
- mission scope
- scenario scope
- regional scope
- route or travel scope
- settlement scope
- sector scope
- campaign-shell scope

### Attachment principles

1. Attachment target is not the same as emitted content family.
2. A site-attached generator is not a site entry.
3. A mission-attached complication emitter is not mission structure.
4. Context scope materially affects consult frequency, output force, refresh logic, and downstream consumer behavior.
5. Attachment is not always to one static parent record; host topology may include state, stage, posture, condition band, or continuity burden.

## Selector and consult-input doctrine

C12 must preserve not only how results are selected, but what the generator is allowed to consult against.
A large donor corpus will repeatedly use generators filtered or modified by context rather than only by randomizer.

### Consult-input classes
When relevant, Astra should distinguish:
- prior result memory
- state flags
- actor tags or roles
- site or region tags
- mission stage
- alert level
- scarcity or depletion state
- time unit, watch, day, or cycle
- route or travel condition
- claim or legitimacy state
- player choice input
- held assets or permits
- audience or visibility state
- prior generator output

### Consult-input principles

1. Randomizer input is not the only valid consult input.
2. Input profile should preserve both required inputs and optional modifiers.
3. Input grammar should make it clear when a generator is filtered, gated, weighted, or routed by context.
4. Player choice may be part of a legal selector medium without making the structure non-generator-shaped.
5. Context-conditioned selectors should not be flattened into ordinary unfiltered lookup tables.

## Activation and consult doctrine

C12 must preserve when a generator is consulted and whether consultation is optional, periodic, triggered, or mandatory.

### Activation classes
When relevant, Astra should distinguish:
- on-entry
- on-travel
- on-rest
- on-clearance
- on-failure
- on-success
- on-escalation
- periodic
- per-cycle
- per-zone or per-node
- per-stage
- per-successor-state
- user-invoked oracle consult
- event-threshold triggered
- pre-play setup consult
- chargen-adjacent consult

### Consult-mode classes
When relevant, Astra should distinguish:
- single consult
- repeated consult
- consult until non-null result
- consult until exit condition
- multi-axis consult
- consult one then consult another
- selective consult by state gate
- draw without replacement until reset

### Consult principles

1. Activation profile is not the same as attachment profile.
2. Mandatory consult is not the same as mandatory insertion.
3. Repeated consult behavior must be explicitly represented when donor structure depends on it.
4. Event threshold consultation should not be flattened into “roll every time” when donor logic is more specific.

## Emission-unit doctrine

C12 must preserve what a single consult can actually emit.

### Emission-unit classes
When relevant, Astra should distinguish:
- determinate result row
- weighted result row
- promptive cue
- answer band
- content reference
- modifier or overlay reference
- packet reference
- parcel reference
- mission complication hook
- escalation event
- replacement result
- additive insert
- chained consult instruction
- null result
- generated bundle result

### Emission principles

1. An emission unit is not automatically a complete content entry.
2. A promptive cue and a packet reference are not the same output form.
3. Null results must be representable when donor structures rely on them.
4. Additive, replacement, and escalation results are structurally different and must not be conflated.

## Emission validity, rejection, fallback, and suppression doctrine

A large donor corpus will repeatedly present generators whose raw output is not always valid in the current context.
C12 must preserve how invalid or context-forbidden results are handled.

### Validity outcome classes
When relevant, Astra should distinguish:
- null because nothing happens
- invalid because the result cannot apply here
- suppressed because current state forbids it
- deferred because the result becomes relevant later
- fallback because the primary result failed validation
- substitute result because a more specific variant is required
- reroll required

### Validity principles

1. Null is not the same as invalid.
2. Invalid is not the same as suppressed.
3. Deferred is not the same as absent.
4. Fallback and substitution should be represented explicitly when donor logic depends on them.
5. Travel events, encounter tables, rumor engines, salvage yields, and mission-complication emitters often rely on this distinction.

## Table doctrine

Tables are common but should not monopolize C12.

### Table structure classes
When relevant, Astra should distinguish:
- simple lookup table
- weighted table
- range table
- repeated-entry table
- two-axis or matrix table
- staged lookup table
- depletion table
- roll-and-hold table
- consult-and-reroll table
- schedule or calendar selector
- ranked-band selector

### Table principles

1. Table schema should preserve weighting and repeated entries when they matter.
2. Indexed presentation in the donor is not enough to prove that a structure is only a table.
3. Table form should not erase chain behavior, null behavior, or state-reactive conditions.
4. Matrix, ranking, and calendar selectors must not be over-normalized into ordinary row/range layouts when their selector logic matters.

## Oracle doctrine

Oracles are not merely imprecise tables.
They often preserve ambiguity, interpretation, or directional prompting as a core feature.

### Oracle classes
When relevant, Astra should distinguish:
- yes/no oracle
- answer-band oracle
- directional oracle
- thematic oracle
- motive or intent oracle
- clue or revelation oracle
- complication oracle
- atmosphere oracle
- interpretation matrix oracle

### Oracle principles

1. Oracle outputs may be promptive rather than determinate.
2. Ambiguity preservation may be intentional and must not always be normalized away.
3. Oracle schemas must preserve when user inference is required.
4. Oracle structures should not be forced into hard lookup rows when donor ambiguity is doctrinally relevant.

## Informational truth-status and bias doctrine

Informational generators are not only ambiguous; they may also be distorted, partial, outdated, or socially biased.
C12 must preserve this without stealing Batch B information procedure.

### Informational truth-status classes
When relevant, Astra should distinguish:
- true
- partially true
- biased
- misleading
- outdated
- forged
- symbolic rather than literal
- noisy or low-confidence
- socially distorted
- intentionally false but structurally useful

### Truth-status principles

1. Informational truth-status is not the same as interpretive openness.
2. A generator may emit socially distorted or intentionally false information while still functioning lawfully as a clue, rumor, or pressure source.
3. C12 may encode truth-status posture, provenance posture, and interpretation burden without replacing Batch B information doctrine.
4. Rumor generators, clue prompts, incident reports, prophecy prompts, and socially mediated outputs especially pressure this distinction.

## Chaining and nested-consult doctrine

Many donor generators work by passing one consult into another.

### Chain classes
When relevant, Astra should distinguish:
- sequential chain
- branching chain
- conditional chain
- assembled multi-roll chain
- nested parent-child consult
- fallback consult
- escalation consult
- mutation consult

### Chain principles

1. A chain is not automatically one generator if the linked consults retain distinct identities.
2. A nested generator should preserve parent-child relation explicitly.
3. Fallback or escalation consults should not be flattened into ordinary repeated rolls.
4. Generated chain behavior is often one of the most important doctrinal features of donor procedural content.

## State-reactivity, depletion, uniqueness, and refresh doctrine

Many generators change over time, by state, or by prior use.
C12 must preserve this instead of flattening all generators into endlessly repeatable static tables.

### State-reactivity classes
When relevant, Astra should distinguish:
- alert-state reactive
- scarcity-state reactive
- site-condition reactive
- faction-posture reactive
- mission-stage reactive
- successor-state reactive
- pressure-threshold reactive
- prior-result reactive

### Depletion and refresh classes
When relevant, Astra should distinguish:
- depleting
- exhaustible
- rotating
- refresh-on-reset
- refresh-on-time
- refresh-on-state-change
- non-refreshing historical draw
- persistent memory-driven

### Uniqueness and memory-scope classes
When relevant, Astra should distinguish:
- per consult
- per scene or packet
- per mission
- per route or travel leg
- per site visit
- per downtime cycle
- per campaign continuity line
- once globally unless reset

### Reactivity principles

1. State-reactive behavior is part of generator identity, not a side note.
2. Depletion is not the same as null results.
3. Refresh profile materially changes generator behavior and must be represented explicitly.
4. Prior-result memory must be preserved when repeated draws alter later output.
5. Memory, uniqueness, and depletion scope should be explicit because reuse at one scale is not the same as reuse at another.

## Output-target doctrine

C12 must preserve what kinds of content a generator emits toward without turning the generator into that content family.

### Output-target classes
When relevant, Astra should distinguish:
- actor-targeting output
- site-targeting output
- challenge-targeting output
- packet-targeting output
- mission-complication output
- parcel-targeting output
- overlay-targeting output
- identity or origin-seed output
- pre-play setup output
- prompt-only output
- mixed-output target

### Output-force classes
When relevant, Astra should distinguish:
- advisory prompt
- optional insert
- mandatory insert
- replacement output
- additive output
- escalation output
- cancellation or null output

### Output-density classes
When relevant, Astra should distinguish:
- sparse prompt
- moderate structured insert
- dense generated bundle

### Output-target principles

1. Output target is not emitted content identity.
2. Packet-targeting output is not a packet schema.
3. Parcel-targeting output is not a parcel schema.
4. Prompt-only outputs should not be inflated into artificial content records.
5. Dense generated bundles may require downstream consumer references without making the generator itself a mission, packet, or parcel file.

## Dense generated bundle doctrine

Some generators emit not merely one result, but a cross-family structured bundle.
C12 must preserve this explicitly.

### Dense generated bundle examples
A generator may emit a bundle containing:
- a packet reference
- an overlay
- a parcel hook
- a site-state change
- an information prompt
- a chained consult instruction

### Dense bundle principles

1. Cross-family generated bundles do not turn the generator into those downstream files.
2. Dense bundles should declare downstream consumer expectations explicitly.
3. Job boards, event engines, modular mission emitters, and complication chains especially pressure this distinction.
4. Dense bundle output must not be flattened into one vague “event result” when donor structure depends on internal composition.

## Generated-instance doctrine

C12 must preserve the difference between reusable generators and the concrete outputs they produce.

### Generated-instance classes
When relevant, Astra should distinguish:
- ephemeral consult result
- persistent generated insert
- session-bounded generated state
- successor-bound generated state
- replaceable generated instance
- cumulative generated instance

### Generated-instance principles

1. Generator shell is not generated instance.
2. One generator may emit many instances over time.
3. A persistent generated shell that repeatedly accepts generated inserts is not the same as a one-shot generated instance.
4. Generated instance density must be explicit when a result becomes more than a simple prompt.
5. Cleanup and persistence rules must be represented when donor structures rely on them.

## User authority and consult authority doctrine

Not every generator is consulted by the same participant or with the same interpretation burden.
C12 must preserve who is expected to consult the generator and who is expected to interpret it.

### Consult authority classes
When relevant, Astra should distinguish:
- adjudicator-only hidden consult
- player-facing consult
- shared-table consult
- automated background emitter
- fallback-only consult

### Authority principles

1. Consult authority is not the same as output target.
2. Interpretation authority may differ from consult authority.
3. Hidden consult generators and player-facing prompt generators should not be collapsed into one generic usage pattern.
4. Distributed interpretation burden matters for oracle-style and promptive generators.

## Advisory burden versus closed emission doctrine

C12 must preserve whether a generator emits near-closed results or open cues requiring substantial user assembly.

### Advisory burden classes
When relevant, Astra should distinguish:
- closed result with low interpretation burden
- bounded prompt with moderate interpretation burden
- open cue with high interpretation burden

### Advisory burden principles

1. Advisory burden is not the same as output density.
2. A sparse result may still have high interpretation burden.
3. A dense bundle may still be relatively closed if the generator assembles it narrowly.
4. This distinction helps prevent inspiration prompts from being over-normalized into fake determinate results.

## Procedural-shell doctrine

Some generators form bounded procedural shells that repeatedly emit content without becoming full scenario architecture.

### Procedural-shell examples
When relevant, Astra should support shells such as:
- mission-board intake shell
- rumor circulation shell
- travel-event shell
- downtime incident shell
- region-event shell
- bounded clue-web prompt shell
- settlement trouble shell

### Procedural-shell principles

1. A procedural shell is still a generator family when its dominant job is repeated structured emission.
2. A procedural shell is not automatically a scenario.
3. If the structure’s dominant job is to emit inserts, incidents, prompts, or bounded variations into another structure, it remains in C12.
4. If the structure imposes its own recurring turn sequence, governance loop, campaign-phase economy, or autonomous progression engine, it should escalate toward C14.

## Pre-play and chargen-adjacent generator doctrine

Some generators emit toward pre-play setup, identity seeding, or initial relationship structures without becoming Batch A doctrine.
C12 must preserve these generator-shaped structures rather than routing them away simply because they occur before ordinary play begins.

### Pre-play generator targets
When relevant, Astra should distinguish:
- identity, background, or origin hooks
- pre-play setup prompts
- relationship seeds
- starting complications
- social or reputation seeds
- role or package prompts

### Pre-play principles

1. A pre-play or lifepath generator is still a generator when its dominant job is structured emission.
2. These generators do not become Batch A doctrine merely because they influence player-facing setup.
3. They should still emit toward the correct downstream content families rather than becoming content instances themselves.
4. Lifepath, origin, background, and campaign-seed donor pressures make this distinction non-optional.

## Sparse-shell versus dense-generator doctrine

Some donor generators are sparse and promptive.
Others are dense, stateful, and multi-layered.

### Density classes
- sparse promptive generator
- medium-density structured generator
- dense authored generator

### Density principles

1. Sparse generators should not be artificially inflated.
2. Dense generators should not be flattened into one-line consult notes if donor behavior relies on internal structure.
3. Density is structural, not stylistic.
4. A sparse generator may still be state-reactive.
5. A dense generator may still emit only small advisory results.

## Template, archetype, instance, and generated-generator doctrine

C12 must support both reusable generator patterns and specific converted generator instances.

### Reusable generator templates
Examples of template-level generator patterns include:
- weighted wandering encounter table
- state-reactive region event emitter
- two-stage rumor oracle
- mission complication chain
- travel hazard emitter with refresh windows
- salvage-yield consult tree
- origin or lifepath chain

These are templates, not converted generator instances.

### Normalized archetypal generators
A normalized archetypal generator is Astra’s stable doctrinal skeleton for a recurring donor procedural family, narrower than a pure template and broader than one converted instance.

### Instantiated generators
An instantiated generator is a specific converted table, oracle, event emitter, selector, or procedural shell created during donor conversion.

### Generated-generator relation
Generated content may appear in C12 in two distinct ways:
- as generated instances emitted by a generator
- as persistent generator shells with their own repeated consult behavior

These are not the same schema situation and must not be conflated.

### Normalization rules

1. Preserve donor generator distinctions whenever Astra can represent them lawfully.
2. Normalize donor presentation into Astra generator structure only as far as needed for cross-corpus stability.
3. Do not invent heavy subsystem behavior where the donor only supplies a bounded generator.
4. Do not erase genuine chain logic, reactivity, or ambiguity simply to make a donor look simpler.
5. Mark authored generator structure and normalized generator structure separately when they differ materially.

## Donor-presentation normalization warnings

Donor presentation frequently disguises generator structure.
C12 must explicitly warn against flattening presentation into schema identity.

### Common misleading presentation forms
When relevant, Astra should watch for:
- infographic tables
- sidebars that hide nested consult logic
- d100, d66, d20, or similar engines whose formatting obscures chain structure
- chapter-level “GM tools” that are actually several separate generators
- list-like donor text that is not generator content at all

### Warning principles

1. Presentation format is not structural identity.
2. One page or one chapter may contain multiple generator records.
3. Numeric formatting may conceal routing, mutation, or nested consult behavior.
4. Graphic or infographic presentation should not cause a non-dice selector to be misrouted as mere layout.

## Publication-unit warning

A donor publication unit may normalize into:
- one generator instance
- several linked generator instances
- one generator template plus one or more instances
- one procedural shell plus emitted-result examples
- mixed C12 and C13 structures

One donor chapter may normalize into zero, one, or many C12 records, and may also normalize partly into C13 packaging without one-to-one correspondence.
Table appendices, event chapters, rumor sections, and GM toolkits are especially misleading publication forms and must not be mistaken for generator family granularity.

Publication layout is not generator identity.

## Cross-file composition discipline

### C02 actor handoff

C12 may emit actor references, actor prompts, actor modifiers, or actor-generation cues.
C12 must not redefine actor entries.

### C03 overlay handoff

C12 may emit overlay references or modifier prompts.
C12 must not redefine overlay ontology.

### C04 item/resource handoff

C12 may emit item references, resource yields, or item-prompt outputs.
C12 must not redefine the underlying item or resource entries.

### C06 site handoff

C12 may emit site events, site modifiers, region incidents, site-state prompts, or route disruptions.
C12 must not absorb site ontology.

### C07 faction handoff

C12 may emit rumors, incidents, posture shifts, or faction-linked prompts.
C12 must not redefine faction ontology.

### C08 challenge handoff

C12 may emit challenge references, challenge prompts, hazard events, or obstacle injections.
C12 must not redefine challenge-object structure.

### C09 packet handoff

C12 may emit packet references, packet prompts, packet insertions, or packet modifiers.
C12 must not redefine encounter or scene packet structure.
An encounter table is not an encounter packet.

### C10 mission/scenario handoff

C10 owns the macro structure that tells you **when** a generator matters.
C12 owns the generator that tells you **what gets emitted** when consulted.
C12 may attach to, trigger from, or feed mission/scenario structures, but it must not redefine mission or scenario architecture.
A mission complication generator is not a mission.

### C11 parcel handoff

C11 owns the parcel or inflow structure itself.
C12 owns only the generator that may select, vary, or surface such a parcel.
C12 may emit parcel references, parcel prompts, or parcel-generation consults, but it must not redefine reward or inflow parcel structure.
A loot table or payout table is not a parcel schema.

### C13 container handoff

C12 generators may be packaged in appendices, kits, bundles, and chapters.
C12 must not define publication packaging.

### C14 reserve handoff

If a generator becomes a dominant campaign engine with overlay turns, domain governance, warfare phases, faction-war loops, expedition cycles, or similarly controlling subsystem behavior, escalate toward C14 rather than hiding that engine inside C12.

## Anti-collapse rules

C12 must not:
- treat all generators as simple tables
- treat all list-shaped content as generator schema
- treat a generated result as the generator schema itself
- treat a site-attached generator as a site entry
- treat an encounter table as an encounter packet
- treat a mission complication table as a mission
- treat a reward generator as a parcel schema
- treat appendix collections as generator identity
- flatten oracle ambiguity into determinate lookup when ambiguity is structurally relevant
- smuggle campaign overlay engines into ordinary generator files
- become a content dump of copied donor tables
- mistake selector media for mere visual presentation
- mistake lifepath, origin, or pre-play generators for flavor appendices or authored setup prose

## Anti-hallucination rules for future conversion

Future conversion working from C12 must obey the following:

1. Do not treat a generated result as the generator schema.
2. Do not treat a site-attached generator as a site entry.
3. Do not treat an encounter table as an encounter packet.
4. Do not treat a mission complication table as a mission.
5. Do not treat a reward table or loot table as a parcel schema.
6. Do not infer full scenario structure from a seed generator or complication generator.
7. Do not flatten an oracle into a hard lookup when donor ambiguity is the point.
8. Do not mistake a generator appendix for one generator family or one generator instance.
9. Do not invent heavy subsystem turns where the donor only provides bounded emission logic.
10. Do not hide actual subsystem overlays inside “state-reactive event generator” language.
11. Do not let one donor family, whether d100 appendices or mission-board procedural supplements, define the universal generator model.
12. Do not confuse output target with emitted content identity.
13. Do not confuse mandatory consult with mandatory insertion.
14. Do not confuse a persistent procedural shell with one generated instance.
15. Do not rewrite linked generator clusters into one flat table when chain identity materially matters.
16. Do not mistake a non-dice selector for mere visual presentation.
17. Do not mistake a pre-play, lifepath, or origin generator for a content instance or flavor appendix.
18. Do not collapse informational truth-status, bias, and ambiguity into one generic “rumor” label.

## Validation stress list

C12 validation should repeatedly pressure-test the following failure modes:
- encounter table mistaken for encounter packet
- mission complication table mistaken for scenario structure
- loot generator mistaken for parcel schema
- site event table mistaken for site entry
- faction rumor table mistaken for faction entry
- oracle flattened into determinate lookup despite interpretive donor design
- dense chained generator flattened into one static table
- state-reactive generator normalized into endlessly repeatable flat results
- appendix grouping mistaken for generator identity
- procedural mission board mistaken for authored scenario
- campaign overlay engine hidden inside “event generator” language
- generated instance mistaken for reusable shell
- mandatory consult mistaken for mandatory output insertion
- sparse prompt generator overinflated into heavy content record
- dense generator underrepresented as a one-line note
- non-dice selector mistaken for mere visual presentation
- lifepath or origin generator mistaken for flavor appendix
- promptive identity generator mistaken for a background content instance
- schedule or calendar selector mistaken for authored timeline
- ranked-band chooser mistaken for deterministic lookup

## File outcome

If C12 is functioning correctly, Astra should be able to do all of the following without collapse:
- represent lookup tables, weighted tables, and event tables
- represent oracle-style prompt structures without erasing ambiguity
- represent non-dice selector media such as matrices, draws, calendars, ranked selectors, and filtered option sets
- represent nested and chained generators
- represent selector, assembler, mutator, and router generator jobs distinctly where needed
- represent consult-input-conditioned generators lawfully
- represent informational outputs with truth-status and bias posture when donor structure depends on them
- represent state-reactive, depleting, refreshable, and memory-scoped generators
- represent generators attached to sites, missions, travel shells, regions, factions, and successor states without absorbing those files
- represent generated instances distinctly from generator shells
- represent promptive, advisory, additive, replacement, escalation, fallback, suppression, and null outputs
- represent pre-play and lifepath-style generators without misrouting them into non-generator files
- distinguish generator identity from publication packaging
- distinguish emitted content families from the generator structures that surface them
- route subsystem-heavy procedural engines toward later overlay handling when needed

That is the doctrinal job of this file.
