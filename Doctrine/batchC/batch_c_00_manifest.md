# batchC_00_manifest.md

## Purpose and authority

Batch C is the **content-schema doctrine layer** for Astra Ascension.

Its job is to define how Batch A and Batch B doctrine are composed into reusable, instantiable content schemas for later donor conversion. Batch C does **not** merge Batch A and Batch B, replace them, or reopen their ownership. It composes them.

Batch C exists to prevent later conversion work from inventing ad hoc record shapes, entry formats, dependency logic, and content-container structures on the fly.

This file is the authority map for:
- Batch C scope
- Batch C file ownership
- Batch C build order
- cross-stack dependency logic
- anti-collapse rules
- schema discipline for later conversion work

Batch C remains **doctrine**, not conversion output.

## Why Batch C exists after Batch A and Batch B

Batch A established the player/chassis and translation-core grammars.
Batch B established the operational/world-interaction grammars.
Batch C exists because converted donor books do not consist only of chassis doctrine and operational procedures. They also consist of **content objects, overlays, compositions, and containers**.

Batch C is where doctrine becomes instantiable.

Batch A tells Astra what kinds of player/chassis constructs exist.
Batch B tells Astra how the world and procedures work.
Batch C tells Astra how to build actual world-content entries and content structures out of those doctrines.

That is how Batch C unites Batch A and Batch B **compositionally** without collapsing them.

## Scope boundaries

Batch C owns reusable **content schemas**.

Batch C does **not** own:
- new player/chassis doctrine already owned by Batch A
- new operational/world-interaction doctrine already owned by Batch B
- donor conversion output instances
- canon decisions
- live-play or GM-facing behavior
- bestiaries, gazetteers, adventures, or item catalogs as final content products

Batch C defines the schema for those later outputs. It does not itself become those outputs.

## Batch C layer definition

Batch C governs four content classes.

### 1. Atomic content objects
Single instantiable things:
- actors
- items/assets
- sites/locales
- factions/institutions
- hazards/challenges
- reward parcels

### 2. Overlay content objects
Content that modifies other content:
- elite/weak variants
- corruption overlays
- environmental overlays
- faction overlays
- mounted variants
- rank variants
- advanced forms
- role packages
- template modifiers

### 3. Composition content objects
Content that assembles lower-level objects into play structures:
- encounters
- scene packets
- missions
- scenarios
- investigation structures
- adventure paths
- campaign arcs
- generator outputs

### 4. Container content objects
Content packages for later conversion outputs:
- gazetteers
- bestiary packs
- city guides
- faction dossiers
- item compendia
- world profiles
- converted sourcebook bundles
- reference containers

## Batch C core design principles

1. **Batch C is still doctrine.**
   It defines schemas, not converted instances.

2. **Batch C is compositional.**
   It references lower-level doctrine rather than re-owning it.

3. **Schema is not instance.**
   Instance is not converted output.
   Converted output is not canon.

4. **Atomic, overlay, composition, and container schemas must remain distinct.**
   If they collapse, Batch C will become a junk drawer.

5. **Dominant-function routing remains mandatory.**
   Hybrid content must be routed by primary doctrinal job first, then by secondary dependencies.

6. **A content schema must never become:**
   - a catalog
   - a donor conversion output repository
   - a lore encyclopedia
   - a mini-sourcebook

7. **A composition schema must reference lower-level schemas rather than duplicating their fields.**

8. **A container schema must package content rather than redefining it.**

## Batch C anti-collapse rules

Batch C files must not:
- restate Batch A or Batch B rules as if Batch C owned them
- absorb donor examples into schema law
- treat a converted entry as doctrine
- collapse place, actor, item, faction, and mission structures into one generic content blob
- treat overlays as full independent content families when they are actually modifiers
- treat containers as if they were atomic entries
- smuggle campaign subsystems into unrelated files
- replace cross-file references with duplicated local fields unless Batch C explicitly owns those fields

## Schema discipline

### Schema vs instance vs converted output vs canon

- **Schema:** the structural doctrine for what a content family must contain and how it routes into Astra.
- **Instance:** one actual content entry using that schema.
- **Converted output:** donor material rendered into Astra-native content entries.
- **Canon:** material explicitly consolidated into the formal Astra sourcebook.

Authority order remains:
1. Current Astra doctrine files
2. Canonical Core Astra Ascension sourcebook
3. Converted Astra-native donor content
4. Examples and demonstrations
5. Original donor assumptions

Batch C files define schemas. They do not raise converted entries to doctrine or canon.

## What Batch C should look like compositionally

A creature entry should compose lower doctrine such as:
- A04 stat architecture
- A07 ability objects
- A08 condition references
- A09 damage families
- B02 survivability hooks
- B08 perception/awareness hooks
- B10 social posture hooks
- B13/B14/B15 dependencies where relevant
- B16 inflow outputs

A site entry should compose lower doctrine such as:
- B06 traversal links
- B07 environmental states
- B11 service availability hooks
- B12 access channels
- B15 civic infrastructure outputs
- relevant encounter, faction, and challenge references

A mission entry should compose lower doctrine through lower schemas such as:
- sites
- factions
- hazards/challenges
- encounters
- reward parcels
- generators
- and relevant A/B doctrine through those lower schemas

## Active Batch C stack

### batchC_00_manifest.md
Authority file for Batch C scope, ownership, build order, anti-collapse rules, and cross-stack dependency logic.

### batchC_01_common_content_schema_conventions_and_record_grammar.md
Shared record grammar for all Batch C files.

Defines:
- canonical IDs
- provenance fields
- dependency references
- relationship links
- state fields
- scaling references
- tag families
- container semantics
- instance-vs-schema rules

This is the file that makes Batch C compositional instead of hand-written and inconsistent.

### batchC_02_actor_creature_npc_and_adversary_schema.md
Content schema for:
- creatures
- NPCs
- named adversaries
- squads
- swarms
- elite units
- actor-content entries generally

### batchC_03_template_variant_overlay_and_modifier_schema.md
Schema for overlays that modify existing content entries rather than standing alone.

Includes:
- elite/weak forms
- corruption overlays
- rank variants
- faction variants
- mounted variants
- environmental variants
- summoned variants
- advanced-form templates
- similar recurring donor overlay patterns

### batchC_04_item_relic_resource_and_asset_content_schema.md
Content-entry schema for:
- gear entries
- relics
- consumables
- resources
- crafting components
- natural treasures
- economic assets
- item-based exceptional content

Batch B03/B04/B05 define doctrine.
Batch C04 defines content-entry shape.

### batchC_05_mount_vehicle_mech_ship_and_platform_entry_schema.md
Content-entry schema for operational frames:
- mounts
- vehicles
- mechs
- ships
- stations
- mobile platforms
- platform-scale entries

Batch B14 defines how frames work.
Batch C05 defines how actual frame entries are represented.

### batchC_06_site_region_settlement_and_locale_schema.md
Content-entry schema for places:
- regions
- sites
- dungeons
- settlements
- districts
- capitals
- habitats
- forts
- enclaves
- hunting grounds
- trial locations
- civic-platform hybrids

Must explicitly support nested sites and district partitions.

### batchC_07_faction_institution_polity_and_social_body_schema.md
Content-entry schema for:
- factions
- institutions
- cults
- guilds
- agencies
- embassies
- sects
- houses
- polities
- treaty bodies
- patron structures

Batch B12 defines organized-access doctrine.
Batch C07 defines actual organization entries.

### batchC_08_traps_hazards_puzzles_trials_and_setpiece_challenge_schema.md
Content schema for challenge objects that are not normal actors or sites.

Includes:
- traps
- hazards
- puzzles
- trials
- challenge structures
- setpiece procedural obstacles

### batchC_09_encounter_scene_packet_and_composition_schema.md
Schema for packaged encounters and scene packets.

This is separate from mission/adventure structure.
A single encounter packet is not the same thing as a whole scenario.

### batchC_10_mission_scenario_adventure_path_and_campaign_arc_schema.md
Schema for larger narrative and operational containers.

Defines how:
- missions
- investigations
- heists
- crawls
- trials
- scenarios
- modules
- longer arcs

are composed from lower-level content objects.

### batchC_11_reward_loot_salvage_claim_and_inflow_parcel_schema.md
Schema for packaged post-pressure outputs.

Batch B16 defines doctrine.
Batch C11 defines how actual reward packets, salvage bundles, claim states, blessing grants, rep outputs, faction payments, and mixed inflow parcels are represented.

### batchC_12_random_tables_events_oracles_and_generator_schema.md
Schema for:
- roll tables
- event tables
- generator structures
- oracle outputs
- encounter tables
- mission complications
- sector events
- other generation-heavy content

### batchC_13_sourcebook_bundle_gazetteer_and_reference_container_schema.md
Schema for content containers that are not themselves one scenario or one actor entry:
- gazetteers
- location chapters
- bestiary packs
- city guides
- world profiles
- item compendia
- faction dossiers
- converted sourcebook bundles

### Reserved later file
#### batchC_14_subsystem_packet_and_campaign_overlay_schema.md
Reserve only.

If needed, this file would hold donor subsystem packets that are too content-shaped to live in A/B doctrine but too structurally distinct to live inside normal scenario files:
- kingdom turns
- investigation packet overlays
- heist overlays
- faction-war packets
- expedition overlays
- domain subsystems
- similar campaign modules

Do not activate unless normal Batch C schemas prove insufficient.

## Why this expanded stack exists

The original narrow Batch C list is not broad enough for a 500+ donor pipeline.

It misses:
- a shared content grammar file
- templates and overlays
- item and asset entry schemas
- site and locale schemas
- organization and polity schemas
- encounter packet schemas
- reward parcel schemas
- bundle/container schemas

Without these, later conversion work will either:
- improvise inconsistent formats
- contaminate neighboring files with overflow duties
- or collapse unlike content into generic blobs

## Build order

The build order Batch C should follow is:

1. `batchC_00_manifest.md`
2. `batchC_01_common_content_schema_conventions_and_record_grammar.md`
3. `batchC_02_actor_creature_npc_and_adversary_schema.md`
4. `batchC_03_template_variant_overlay_and_modifier_schema.md`
5. `batchC_04_item_relic_resource_and_asset_content_schema.md`
6. `batchC_05_mount_vehicle_mech_ship_and_platform_entry_schema.md`
7. `batchC_06_site_region_settlement_and_locale_schema.md`
8. `batchC_07_faction_institution_polity_and_social_body_schema.md`
9. `batchC_08_traps_hazards_puzzles_trials_and_setpiece_challenge_schema.md`
10. `batchC_09_encounter_scene_packet_and_composition_schema.md`
11. `batchC_10_mission_scenario_adventure_path_and_campaign_arc_schema.md`
12. `batchC_11_reward_loot_salvage_claim_and_inflow_parcel_schema.md`
13. `batchC_12_random_tables_events_oracles_and_generator_schema.md`
14. `batchC_13_sourcebook_bundle_gazetteer_and_reference_container_schema.md`

This order matters because Batch C should start with:
- common grammar
- atomic objects
- overlays
- then composition and container schemas

## Cross-stack dependency logic

### Batch A feeds Batch C with:
- chassis grammar
- stat architecture
- skill/competency translation logic
- access/proficiency gates
- ability object model
- resource/cost/backlash grammar
- status/effect taxonomy
- damage family taxonomy
- progression axes
- conversion invariants
- translation pattern library and edge-case routing

### Batch B feeds Batch C with:
- scene/conflict procedure
- survivability framework
- item/equipment doctrine
- value/exchange doctrine
- crafting/transformation doctrine
- traversal doctrine
- environmental pressure doctrine
- uncertain perception doctrine
- information-pressure doctrine
- social pressure doctrine
- non-encounter time doctrine
- organized-access doctrine
- auxiliary entity doctrine
- operational frame doctrine
- civic environment doctrine
- post-pressure inflow doctrine

### Batch C outputs for later conversion work:
- instantiable content schemas
- composition-ready content records
- reusable container formats
- lawful overlay structures
- cross-file content dependency standards

## Content-schema ownership map

### Batch C01
Owns common record grammar.
Must not own any content family itself.

### Batch C02
Owns actor-content record structure.
Must not own missions, sites, or reward parcels.

### Batch C03
Owns overlay structures.
Must not become a second actor or item file.

### Batch C04
Owns item/resource/asset entry shape.
Must not redefine B03/B04/B05 doctrine.

### Batch C05
Owns frame entry shape.
Must not absorb B14 operations or B15 site shells.

### Batch C06
Owns place entry shape.
Must not absorb missions, factions, or encounter packets.

### Batch C07
Owns organization entry shape.
Must not absorb social procedure or site doctrine.

### Batch C08
Owns challenge-object schemas.
Must not become a scenario file.

### Batch C09
Owns packaged encounter/scene composition.
Must not become a campaign file.

### Batch C10
Owns mission/scenario/arc composition.
Must not absorb all lower schemas into flat modules.

### Batch C11
Owns reward/inflow parcel schemas.
Must not redefine B16 doctrine or B04/B12 legality/value doctrine.

### Batch C12
Owns generator and table schemas.
Must not become a content dump.

### Batch C13
Owns bundle/container schemas.
Must not redefine atomic entry structures.

## Batch C handoff discipline

Batch C files must hand off to lower doctrine rather than rewriting it.

Examples:
- survivability hooks -> B02
- social leverage and standing logic -> B10 / B12
- access and legality -> B12 and B04
- frame operation -> B14
- site infrastructure behavior -> B15
- item ontology -> B03
- crafting behavior -> B05
- information truth-status -> B09
- uncertain perception -> B08

## Status flags

### Immediate active drafting sequence
- C00 through C13 as listed above

### Reserved watch note
If Batch C begins swelling around subsystem packets, activate C14 rather than smuggling subsystem overlays into unrelated schemas.

## Batch C handoff to conversion work

Conversion work begins **after** Batch C schema doctrine is sufficiently stable.

When conversion begins:
- donor material should be instantiated through Batch C schemas
- converted entries should cite governing A/B/C doctrine
- converted outputs must remain lower authority than doctrine
- schema exceptions should be classified, not improvised
- repeated schema strain should be reported for doctrine review rather than patched silently in conversion output

## Final doctrine statement

Batch C is the composition layer where Batch A and Batch B converge into reusable content schemas.

It does not merge them.
It does not replace them.
It does not authorize donor outputs as canon.

It provides the structural language by which actual converted content can later exist without collapsing the Astra doctrine stack.