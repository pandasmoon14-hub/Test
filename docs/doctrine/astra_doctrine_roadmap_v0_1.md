# Astra Doctrine Master Roadmap v0.1

```yaml
file_id: ROADMAP-001
filename: astra_doctrine_master_roadmap_v0_1.md
proposed_path: docs/doctrine/astra_doctrine_roadmap_v0_1.md
status: roadmap-current
authority_level: planning
layer: 0_control
phase: 0
version: 0.1
created: 2026-05-18
last_reviewed: 2026-06-05
maintained_by: Astra Doctrine Council
depends_on:
  - phase1_scope_model_and_construct_granularity_doctrine_v0_2_1_final.md
  - phase1_conversion_ir_doctrine_v0_3_1_final.md
  - batch_b_minimum_operational_doctrine_unlock_plan_v0_2_1_final.md
  - batch_c_minimum_schema_doctrine_unlock_plan_v0_4_1_final.md
```

## 1. Status and Authority Statement

This roadmap is the active planning document for Astra doctrine, schema, canon, runtime, and training execution.

It is not setting canon. It is not mechanics doctrine. It is not runtime specification. It is not a training dataset guide. It is not a donor conversion artifact.

It governs what must be drafted, in what order, with what gates, so Astra can absorb a roughly 1,900-donor TTRPG corpus without donor-law creep, doctrine fragmentation, schema chaos, premature runtime construction, or training-as-authority drift.

This roadmap is planning authority. If this roadmap conflicts with the existing Scope Model, Conversion IR, Batch B unlock plan, or Batch C unlock plan, those active control files win and this roadmap must be revised.

### Current State After PR #204

PR #204 is treated as merged for roadmap-control purposes. It completed the public identity and backend-first invariant alignment for Astra Ascension by making the repository posture explicit: Astra Ascension is the project identity, the backend runtime must own truth/state/dice/persistence/file writers in any future live-play architecture, and Aether Forge remains subordinate extraction/handoff developer tooling rather than the project identity.

The repository currently represents the following state:

- ROADMAP-001 and REGISTRY-001 already exist and are tracked as control files. Do not follow any older instruction that says to create them from scratch.
- A01-A15 draft doctrine files are present in the repo. Their existence does not mean every item is current, pressure-tested, or final; use the registry and owner files for exact status.
- Batch B operational doctrine files, Batch C schema-family files, schema/math/mechanics control files, and D-series native-design source-pack material are present. This reconciliation does not rewrite Batch A/B/C/D content or change their authority.
- Runtime implementation remains planned but not started by this roadmap-control layer. No runtime database, event kernel, writer, generator, live-play adapter, or training set is authorized here.
- The Runtime Boundary + Generator Ownership Audit is planned as a later audit item. It is not performed by this current-state reconciliation.
- Extraction/handoff tooling, including Aether Forge references, is current developer infrastructure for source-grounded packets and validation. It is subordinate to Astra doctrine and may not be treated as canon, runtime authority, or project identity.
- The local test environment may be incomplete unless PyYAML and other test dependencies from `requirements-dev.txt` are installed. Any validation run must report dependency failures honestly instead of marking registry tests as passed.

If a future model or reviewer finds roadmap text that appears to restart bootstrap work already represented in the repo, treat that text as superseded by this current-state section and inspect the actual files and registry before acting.

## 2. Purpose

This roadmap exists to produce a controlled, executable doctrine unlock sequence for Astra Ascension.

It answers:

1. Which doctrine files must exist before broad conversion?
2. Which schemas must exist before conversion records can scale?
3. Which canon and lexicon files must exist before sourcebook consolidation?
4. Which runtime files must wait until doctrine and canon stabilize?
5. Which training and evaluation files must wait until runtime and canon exist?
6. What gates prevent unstable doctrine from being scaled into the 1,900-donor corpus?

The operating rule is:

**Doctrine first. Schema second. Pilot third. Scale fourth. Runtime later. Training last.**

## 3. Scope

This roadmap governs:

- Astra-native setting doctrine
- Astra-native advancement and action doctrine
- Astra-native operational and world doctrine
- Batch C content-family schema doctrine
- canon and lexicon governance
- runtime and backend doctrine
- live-play, training, and evaluation doctrine
- file status promotion
- pressure tests
- pilot gates
- broad conversion gates
- runtime gates
- training gates

This roadmap does not govern:

- PDF extraction implementation
- OCR mechanics
- handoff packet code internals
- specific donor PDF contents
- specific canon facts
- specific runtime database implementation
- fine-tuning procedure details

## 4. Non-Negotiable Setting Premise

Astra Ascension is a **high-tech, high-magic, space-faring, multi-planet, multiplanar, sci-fantasy cultivation setting**.

This premise is structural, not decorative.

Every doctrine file, schema, canon protocol, runtime model, and training example must remain compatible with:

- cultivation and ascension as core progression
- Dao, domain, element, and concept interaction as metaphysical infrastructure
- high technology and high magic as integrated systems
- starships, void travel, orbital scale, stellar scale, and multiplanar movement
- relics, implants, cyberware, biotech, mechs, drones, living weapons, constructs, stations, and dimensional anchors
- organic beings, spiritual beings, AIs, companions, summons, factions, planets, planes, and macro-scale actors
- personal, factional, planetary, orbital, stellar, planar, and cosmic scale
- sects, guilds, corporations, empires, planar courts, trade networks, law, logistics, war, diplomacy, colonization, and reputation
- deterministic backend state later, where the backend owns truth, dice, state mutation, clocks, persistence, and event commits

Hard refusals:

- Astra is not D&D in space.
- Astra is not generic fantasy.
- Astra is not generic cyberpunk.
- Astra is not generic space opera.
- Astra is not cultivation with lasers.
- Astra does not inherit D&D classes, Great Wheel cosmology, Vancian spell slots, Shadowrun essence, Traveller jumps, Lancer licenses, Fate aspects, or any other donor defaults unless explicitly normalized by Astra doctrine.

## 5. Authority Hierarchy

Authority flows downward.

```text
Tier 0 — Active Control Files
  phase1_scope_model_and_construct_granularity_doctrine
  phase1_conversion_ir_doctrine
  batch_b_minimum_operational_doctrine_unlock_plan
  batch_c_minimum_schema_doctrine_unlock_plan
  lawful_outcome_taxonomy

Tier 1 — Planning Control
  ROADMAP-001: this roadmap
  REGISTRY-001: doctrine registry
  current decisions logs

Tier 2 — Astra Doctrine
  A01–A15
  K01–K06

Tier 3 — Schema Doctrine
  C00–C14

Tier 4 — Runtime Doctrine
  R01–R08

Tier 5 — Training / Evaluation Doctrine
  T01–T07

Tier 6 — Conversion Artifacts
  handoff packets
  conversion-intake memos
  lawful outcome ledgers
  source-local retention records
  canon candidate notes

Tier 7 — Donor Source Material
  raw donor PDFs
  extracted donor packets
  donor terminology
  donor mechanics
```

Rules:

- Donor material is evidence, not authority.
- Conversion output is not canon.
- Canon is not runtime state.
- Runtime state is not model memory.
- Training examples are not doctrine.
- Schemas validate structure; they do not create canon.
- Runtime implements doctrine; it does not redefine doctrine.
- Examples illustrate doctrine; they do not override doctrine.

## 6. Active Control Files

The following are already treated as active control files and this roadmap depends on them:

```text
phase1_scope_model_and_construct_granularity_doctrine_v0_2_1_final.md
phase1_conversion_ir_doctrine_v0_3_1_final.md
batch_b_minimum_operational_doctrine_unlock_plan_v0_2_1_final.md
batch_c_minimum_schema_doctrine_unlock_plan_v0_4_1_final.md
lawful_outcome_taxonomy
```

These files control construct boundaries, Conversion IR routing, lawful outcomes, Batch B operational unlocks, and Batch C schema unlocks.

This roadmap coordinates the execution sequence. It does not replace those control files.

## 7. Phase Separation Rules

These rules are absolute.

| Boundary | Rule |
|---|---|
| Extraction → Conversion | Extraction truth is technical evidence, not conversion permission. |
| Conversion → Canon | Conversion output is analysis, not canon. |
| Canon → Runtime | Canon describes what is true; runtime tracks what is currently actual. |
| Runtime → Model | Runtime state is backend-owned; LLM context is not persistent truth. |
| Training → Doctrine | Training examples are illustrative; they cannot amend doctrine. |
| Schema → Doctrine | Schemas structure records; they do not define mechanics. |
| Donor → Astra | Donors pressure doctrine; they do not become doctrine. |


## 7A. Backend-First Model Interchangeability Invariant

Astra Ascension is model-interchangeable by design. Astra may use any one interchangeable LLM, local or cloud, but no Astra subsystem may depend on that model as the holder of truth. The model is replaceable. The backend is authoritative. The runtime kernel, schemas, generators, validators, event logs, memory system, retrieval system, persistence writers, and file/export writers are the game. The LLM is only the voice at the table.

Binding rules:

- LLMs are interchangeable presentation adapters.
- The backend owns truth, state, rules, dice, validation, persistence, retrieval, clocks, memory, consequences, generated content, and event commits.
- No feature is runtime-ready if it depends on model memory, model-side hidden state, model-side dice, model-side file writing, model-side canon authority, or model-side unvalidated consequence commits.
- Every runtime-relevant subsystem must eventually have doctrine owner, schema representation, runtime state representation when persistent, command/IR representation when interactive, validator, generator/template pathway when procedurally creatable, context-packet projection, narration contract, and tests.
- Runtime state is never model memory, and model context is never authoritative persistence.
- Conversion output remains evidence until canon promotion and conflict review are complete.

## 8. Anti-Fragmentation Doctrine

The project must avoid two equal failures:

1. Megafile collapse: one enormous doctrine file owning too much.
2. Microfile fragmentation: dozens of overlapping files creating authority drift.

Rules:

- Prefer fused spine files over many narrow files.
- Each file must own a coherent conceptual domain.
- Every file must state what it owns.
- Every file must state what it must not own.
- Every file must list donor pressure absorbed.
- Every file must list hard refusals.
- Every file must list escalation triggers.
- Every file must list dependencies and downstream consumers.
- New files require registry entries before review.
- Splitting a file requires a roadmap and registry update.

A spine file may split only if:

1. pressure tests show incompatible review cycles;
2. downstream consumers require independent gate status;
3. the file becomes too large to govern;
4. the split reduces contradiction risk;
5. migration references are updated.

## 9. High-Level Layer Map

```text
Layer 0 — Control and Registry
  ROADMAP-001
  REGISTRY-001
  active control files

Layer 1 — Core Setting / Metaphysics Spine
  A01–A05

Layer 2 — Advancement / Action Spine
  A06–A10

Layer 3 — World / Asset / Conflict Spine
  A11–A15

Layer 4 — Content-Family Schema Doctrine
  C00–C14

Layer 5 — Canon / Lexicon Governance
  K01–K06

Layer 6 — Runtime / Backend Doctrine
  R01–R08

Layer 7 — Live-Play / Training / Evaluation Doctrine
  T01–T07
```

Dependency direction:

```text
control → setting spine → advancement/action spine → operational spine → schemas → canon/lexicon → runtime → training
```

Upper layers may pressure lower layers through escalation, but they may not redefine them.

## 10. File Status Lifecycle

```yaml
status_values:
  todo:
    meaning: Planned but not started.
  draft:
    meaning: Initial complete draft exists.
  review:
    meaning: Under structured review.
  pressure-tested:
    meaning: Passed assigned contradiction and donor-pressure tests.
  current:
    meaning: Active authority for its layer.
  blocked:
    meaning: Cannot proceed due to unresolved dependency or contradiction.
  deprecated:
    meaning: Superseded by a newer current file.
```

Promotion criteria:

```text
todo → draft
  registry entry exists
  owner assigned
  dependencies identified
  file has required structure

draft → review
  all required sections present
  owns/must_not_own boundaries declared
  mapping rules present
  hard refusals present
  no obvious contradiction with active control files

review → pressure-tested
  assigned pressure tests executed
  contradiction tests passed or escalated
  donor-law creep review passed
  dependency review passed

pressure-tested → current
  downstream consumers confirm usability
  no unresolved high-severity conflict-ledger entries
  registry updated
  council/reviewer acceptance recorded

current → deprecated
  replacement file current
  migration path recorded
  downstream references updated
```

## 11. Required Structure for Doctrine Files

Every A, K, R, and T doctrine file must contain:

```text
1. Purpose and status
2. What this file owns
3. What this file must not own
4. Required definitions
5. Core doctrine rules
6. Conversion mapping rules
7. Source-local handling
8. Donor pressure absorbed
9. Hard refusals / rejected imports
10. Escalation triggers
11. Dependencies
12. Handoff to downstream layers
13. Test cases / pressure examples
14. Versioning and review protocol
```

Every C schema file must contain:

```text
1. Purpose and status
2. What this schema owns
3. What this schema must not own
4. Record identity and provenance fields
5. Required fields
6. Optional fields
7. Validation rules
8. Source-local and rejected-import fields
9. Canon eligibility fields
10. Confidence and review fields
11. Donor pressure absorbed
12. Hard refusals
13. Escalation triggers
14. Test records
```

## 12. Phase 0 — Control and Registry

Goal: establish governance before drafting new doctrine.

Files:

```text
ROADMAP-001 — docs/doctrine/astra_doctrine_roadmap_v0_1.md
REGISTRY-001 — docs/doctrine/astra_doctrine_registry_v0_1.yaml
```

Phase 0 must not:

- define setting content;
- define mechanics;
- create canon;
- create schemas;
- begin runtime implementation.

Gate to Phase 1:

```text
ROADMAP-001 exists and is accepted as roadmap-current.
REGISTRY-001 exists with records for ROADMAP, REGISTRY, A01–A15, C00–C14, K01–K06, R01–R08, T01–T07.
Status values and dependency locks are encoded.
```

## 13. Phase 1A — Setting Spine

Goal: define the container of Astra reality.

Files:

```text
A01_cosmology_and_dimensional_architecture.md
A02_source_fields_magic_technology_relation.md
A03_soul_body_mind_spirit_ontology.md
A04_dao_domain_element_architecture.md
A05_civilization_scale_and_power_scale_doctrine.md
```

Execution order:

```text
A01 → A02 → A03 → A04 → A05
```

A01 owns:

```text
worlds
planes
dimensions
voids
interplanar adjacency
dimensional ecology
cosmic topology
source-local cosmology handling
```

A02 owns:

```text
source fields
magic/technology relation
high-tech/high-magic interaction
psionics/divine/cultivation/biotech interface
source field manifestation
magic-tech pressure matrix
```

A03 owns:

```text
body
soul
mind
spirit
identity continuity
AI personhood
uploads
possession
augmentation metaphysics
death and persistence boundaries
```

A04 owns:

```text
Dao
domain
element
conceptual law
resonance
antagonism
synthesis
Astra-native metaphysical interaction rules
```

A05 owns:

```text
personal scale
group scale
factional scale
planetary scale
orbital scale
stellar scale
void scale
planar scale
cosmic scale
scale transition principles
power-scale boundaries
```

Phase 1A must not:

- define cultivation stages;
- define final techniques;
- define skill lists;
- define starship rules;
- define combat rules;
- define factions;
- import donor cosmology;
- import donor Dao;
- import donor magic/tech assumptions.

Gate to Phase 1B:

```text
A01–A05 are at least review status.
A01–A05 have no unresolved internal contradictions.
A01–A05 pass initial contradiction review.
K01 has a placeholder registry entry for reserved terms.
```

## 14. Phase 1B — Advancement / Action Spine

Goal: define how beings advance, act, train, synthesize, and pay costs.

Files:

```text
A06_cultivation_and_ascension_stage_architecture.md
A07_advancement_axes_and_progression_pressure.md
A08_path_domain_and_technique_mastery_doctrine.md
A09_skill_competency_and_synthesis_doctrine.md
A10_resource_cost_backlash_and_corruption_doctrine.md
```

Execution order:

```text
A06 → A07 → A08 → A09 → A10
```

A06 owns:

```text
cultivation stages
ascension stages
breakthroughs
bottlenecks
tribulations
stage thresholds
advancement permission logic
```

A07 owns:

```text
multiple advancement axes
body refinement
soul refinement
mind refinement
path mastery
technique mastery
social/institutional rank
asset/relic/platform growth
companion advancement
factional advancement
```

A08 owns:

```text
paths
domains
technique taxonomy
spell/power/art/maneuver normalization
mastery stages
learning and training permissions
technique evolution
```

A09 owns:

```text
skills
competencies
proficiencies
training vectors
cross-skill synthesis
multi-domain checks
non-active capability translation
professional and cultural competency mapping
```

A10 owns:

```text
resource models
costs
reserves
cooldowns
recharge
backlash
corruption
overload
heat
strain
fatigue
debt
sacrifice
spiritual damage
dimensional contamination
divine favor and disfavor
```

Phase 1B must not:

- import donor level systems;
- import donor cultivation realm names;
- default to Vancian spell slots;
- default to Shadowrun essence;
- define final item stats;
- define final combat math;
- define final runtime state.

Gate to Phase 1C:

```text
A06–A10 are at least review status.
A06–A10 successfully route class-based, point-buy, lifepath, cultivation, psionic, cybernetic, and narrative-tag advancement pressure.
No donor advancement system is silently adopted.
```

## 15. Phase 1C — World / Asset / Conflict Spine

Goal: define the material, social, operational, and conflict-facing world.

Files:

```text
A11_actor_ontology_and_player_grade_actor_doctrine.md
A12_asset_relic_implant_platform_doctrine.md
A13_combat_hazard_damage_and_consequence_doctrine.md
A14_travel_exploration_and_scale_transition_doctrine.md
A15_faction_society_economy_and_institution_doctrine.md
```

Execution order:

```text
A11 → A12 → A13 → A14 → A15
```

A11 owns:

```text
player-grade actors
NPCs
monsters
spirits
AIs
drones
companions
summons
factional actors
macro-actors
planets or planes as actors where doctrine permits
```

A12 owns:

```text
gear
relics
artifacts
implants
cyberware
biotech
starships
mechs
drones
constructs
stations
living weapons
cultivation tools
dimensional anchors
platform assets
asset advancement
```

A13 owns:

```text
combat across scales
hazards
damage families
resistance
immunity
injury
death
recovery
transformation
ship conflict
fleet conflict
planar conflict
psychic conflict
cosmic conflict
environmental consequence
```

A14 owns:

```text
local travel
regional travel
planetary travel
orbital travel
stellar travel
void travel
planar travel
dimensional routes
gates
portals
jump routes
ruins
megastructures
exploration procedure
scale transitions
```

A15 owns:

```text
sects
guilds
corporations
empires
planetary governments
planar courts
trade networks
currency
value
requisition
law
standing
reputation
logistics
war
diplomacy
colonization
institutional advancement
```

Phase 1C must not:

- import donor combat systems;
- import donor starship travel systems;
- import donor economy assumptions;
- import donor faction mechanics;
- define specific planets, empires, or named factions;
- replace canon consolidation.

Gate to Phase 2:

```text
A01–A15 are at least pressure-tested.
A01–A15 have no unresolved high-severity contradiction.
All required pressure tests have either passed or produced escalation records.
```

## 16. Phase 2 — Schema Base and Content-Family Schemas

Goal: define structured record contracts for conversion output.

Files:

```text
C00_shared_content_record_base_and_schema_registry.md
C01_creature_npc_record_schema.md
C02_item_gear_record_schema.md
C03_ability_power_technique_record_schema.md
C04_relic_implant_installable_asset_schema.md
C05_faction_institution_record_schema.md
C06_location_site_region_record_schema.md
C07_mission_scenario_adventure_record_schema.md
C08_vehicle_ship_platform_record_schema.md
C09_hazard_environment_record_schema.md
C10_table_oracle_record_schema.md
C11_companion_summon_record_schema.md
C12_crafting_salvage_recipe_record_schema.md
C13_map_diagram_record_schema.md
C14_source_local_setting_cosmology_record_schema.md
```

Execution order:

```text
C00 first.
Then C03, C02, C01, C10.
Then C09, C06, C07, C13.
Then C04, C08, C05, C14, C11, C12 as pressure requires.
```

C00 owns:

```text
record identity
source provenance
donor source references
source-local flags
rejected-import flags
canon eligibility
confidence fields
review routing
schema versioning
cross-record references
```

Phase 2 must not:

- define mechanics;
- create canon;
- validate truth;
- import donor terminology through enum values;
- bypass doctrine ownership.

Gate to Phase 3:

```text
C00 is current.
C01, C02, C03, and C10 are at least pressure-tested.
Schema records validate pilot conversion output.
Schemas preserve source-local, rejected import, canon eligibility, confidence, and review routing.
```

## 17. Phase 3 — Canon and Lexicon Governance

Goal: define term control, source-local boundaries, canon promotion, conflict handling, and bible structure.

Files:

```text
K01_lexicon_governance_and_reserved_terms.md
K02_source_local_boundary_and_rejected_import_doctrine.md
K03_canon_promotion_protocol.md
K04_conflict_ledger_and_cross_donor_pressure_protocol.md
K05_mechanics_bible_structure.md
K06_setting_bible_structure.md
```

Execution order:

```text
K01 → K02 → K03 → K04 → K05 → K06
```

K01 owns:

```text
reserved terms
accepted Astra terms
provisional terms
donor term handling
aliases
forbidden imports
term promotion
term deprecation
```

K02 owns:

```text
source-local boundaries
retained donor constructs
rejected imports
quarantine rules
boundary confidence
review routing
```

K03 owns:

```text
canon promotion criteria
canon candidate review
acceptance protocol
reversal protocol
canon status values
```

K04 owns:

```text
cross-donor contradictions
conflict ledger
severity levels
resolution routes
reopened conflicts
pressure trends
```

K05 owns:

```text
mechanics bible structure
rules consolidation
mechanical precedence
core rulebook extraction targets
```

K06 owns:

```text
setting bible structure
setting consolidation
lore hierarchy
accepted setting facts
source-local exclusions
```

Phase 3 must not:

- invent new mechanics;
- redefine A-layer doctrine;
- create schemas;
- implement runtime;
- promote donor content without K03 review;
- treat conversion frequency as canon truth.

Gate to Phase 4:

```text
K01–K04 are current.
K05–K06 are at least review.
Canon promotion has been tested on pilot candidates.
Conflict ledger has no unresolved high-severity issues blocking runtime.
```

## 18. Phase 4 — Runtime and Backend Doctrine

Goal: define deterministic backend architecture for persistent play.

Files:

```text
R01_deterministic_event_kernel.md
R02_state_model_and_entity_component_schema.md
R03_command_lifecycle_and_state_delta_validation.md
R04_dice_rng_and_randomness_authority.md
R05_context_packet_compiler.md
R06_hidden_information_partitioning.md
R07_faction_world_clocks_and_economy_state.md
R08_campaign_persistence_replay_and_hash_verification.md
```

Execution order:

```text
R01 → R02 → R03 → R04 → R05 → R06 → R07 → R08
```

R-layer doctrine owns:

```text
event kernel
state model
entity/component structure
command lifecycle
state delta validation
dice/RNG authority
context packet compilation
hidden information partitioning
world clocks
faction clocks
economy state
campaign persistence
replay
migration
hash verification
PersistenceOrchestrator
EventLedgerWriter
StateStoreWriter
EntityRecordWriter
GeneratedContentRecordWriter
KnowledgeClaimWriter
DialogueTranscriptWriter
ConversationSummaryWriter
RetrievalIndexWriter
FileExportWriter
```

Persistence and world-memory rules for R01-R08:

- Primary persistence is database/event-log/state-store backed.
- Markdown, JSON, YAML, or other files are materialized exports, not the source of truth.
- The LLM writes no files directly and never serves as the durable memory store.
- Generated creatures, NPCs, factions, locations, hazards, items, rumors, missions, table results, and other records become durable only through backend-owned schema, validation, provenance, and event/state commit pathways.
- File exports are emitted by backend-owned writers after validation and commit; they are not model-side authored truth.

Runtime must not:

- redefine doctrine;
- create canon;
- let LLMs mutate state;
- let LLMs roll dice;
- let LLMs write files directly;
- use model memory as authoritative persistence;
- treat generated narration as durable world memory;
- implement donor mechanics as backend defaults.

Gate to Phase 5:

```text
R01–R08 are at least pressure-tested.
Runtime prototype passes state-delta validation.
Context packets preserve hidden information boundaries.
Dice/RNG authority belongs to backend only.
```


## 18A. Runtime Memory, Generated Content, and Narration Control Amendments

These amendments are planning controls for future R01-R08 doctrine. They are not runtime implementation and do not create a database, runtime kernel, or live-play adapter in this roadmap revision.

### Generated-content lifecycle

Generated content is not disposable narration once the campaign may need to recur, retrieve, audit, or promote it. Future runtime doctrine must support lifecycle statuses including:

```text
ephemeral_proposal
committed_instance
source_local_record
generator_candidate
canon_candidate
accepted_canon
deprecated
quarantined
```

Rules:

- A generated creature, NPC, location, faction, relic, hazard, table result, rumor, or mission hook must receive persistent IDs and provenance before it can recur.
- Recurrence and retrieval must be backend-owned through schemas, validators, committed state, event logs, and retrieval indexes.
- Canon promotion remains separate from generated-content persistence; a durable campaign instance is not automatically Astra canon.
- Generated-content persistence requires backend-owned schema, validation, provenance, and event/state commit pathways.
- The LLM may propose generated content, but it cannot make that content durable or canonical by narration alone.

### Knowledge and dialogue memory distinction

Future runtime doctrine must distinguish narrated conversation from authoritative campaign truth. Required future support includes:

- actor knowledge records;
- player-known facts;
- NPC/faction beliefs;
- rumors;
- unverified claims;
- false claims;
- hidden truths;
- dialogue transcript records;
- conversation summaries;
- dialogue-to-claim extraction.

Critical rule: narrated dialogue may be stored as transcript, but only validated claims, knowledge records, relationship changes, and state deltas become authoritative campaign state. Dialogue-to-claim extraction must route through backend-owned validation before a claim can affect truth, beliefs, retrieval, clocks, faction state, or consequences.

### Narration Validator requirement

Future runtime doctrine must require a Narration Validator for LLM output. The validator must check for:

- unsupported factual claims;
- hidden information leakage;
- uncommitted state mutation;
- unauthorized NPC knowledge;
- invented rewards;
- invented injuries;
- invented locations;
- invented factions;
- donor terminology leakage;
- tone/format violations.

Narration happens after backend commitment, except when clearly labeled as proposal, clarification, or non-authoritative flavor. Player-facing narration must be derived from committed backend outcomes and context packets, not from model-side hidden state or unsupported invention.

### Persistence and writer ownership

Future runtime doctrine must define the following backend-owned responsibilities clearly enough that no model or adapter assumes the LLM writes files or remembers the world:

```text
PersistenceOrchestrator
EventLedgerWriter
StateStoreWriter
EntityRecordWriter
GeneratedContentRecordWriter
KnowledgeClaimWriter
DialogueTranscriptWriter
ConversationSummaryWriter
RetrievalIndexWriter
FileExportWriter
```

These writers materialize committed truth, validated memory records, retrieval indexes, transcripts, summaries, and exports after backend validation. They do not transfer authority to Markdown, JSON, YAML, or model memory.

## 19. Phase 5 — Live-Play, Training, and Evaluation Doctrine

Goal: define adapter behavior, evaluation, examples, failure labels, benchmark packs, and hard-fail safety.

Files:

```text
T01_conversion_adapter_evaluation_protocol.md
T02_live_play_adapter_behavior_contract.md
T03_context_packet_example_pack.md
T04_failure_label_taxonomy.md
T05_gold_example_selection_protocol.md
T06_benchmark_pack_design.md
T07_unsafe_behavior_hard_fail_matrix.md
```

Execution order:

```text
T01 → T02 → T03 → T04 → T05 → T06 → T07
```

T-layer doctrine owns:

```text
conversion adapter evaluation
live-play adapter behavior
context packet examples
failure labels
gold example selection
benchmark packs
unsafe behavior hard-fail matrix
```

Training must not:

- define doctrine;
- create canon;
- override runtime;
- teach examples that contradict current doctrine;
- train on uncanonized conversion output as if it were truth.

Gate to live-play training:

```text
T01–T07 are current.
R01–R08 are current or pressure-tested.
Gold examples derive only from current doctrine and accepted canon.
Unsafe behavior hard-fails are active.
Benchmark pack validates doctrine compliance.
```

## 20. Dependency Locks

Hard locks:

```text
REGISTRY-001 locks all drafting beyond roadmap.
A01 locks A02–A05.
A01–A05 lock A06–A10.
A01–A10 lock A11–A15.
A01–A15 lock C00.
C00 locks C01–C14.
A01–A15 and C00 lock K01–K04.
K01–K04 lock K05–K06.
A01–A15, C00–C14, K01–K06 lock R01.
R01 locks R02–R08.
R01–R08 lock T01–T07.
```

Soft locks:

```text
K01 may begin as a placeholder after A01–A03 have stable terminology.
C10 may draft early after C00 because table/oracle structure is high-pressure and less doctrine-specific.
K04 conflict ledger may begin as a draft during pressure testing if contradictions need tracking before full canon governance.
Runtime brainstorming may occur before R01, but no implementation doctrine may be current before canon/schema gates.
```

## 21. Pressure-Test Requirements

Every A-layer file must pass deliberate contradiction tests before becoming current.

Minimum contradiction test categories:

```text
cosmology contradiction
magic-technology contradiction
soul/body/mind/AI contradiction
Dao/domain/element contradiction
cultivation-stage contradiction
advancement-system contradiction
resource/backlash contradiction
asset-system contradiction
combat-scale contradiction
travel-scale contradiction
faction/economy contradiction
```

A test passes only if:

- donor pressure is mapped, normalized, source-local retained, quarantined, or escalated;
- no donor assumption silently becomes Astra law;
- hard refusals are honored;
- lexicon risk is identified;
- schema implications are recorded;
- canon implications are not prematurely promoted.

## 22. Pilot Requirements Before Scale

Before broad conversion, run controlled pilots.

### Pilot 1 — Doctrine Pressure Pilot

Size:

```text
12–18 packets
```

Purpose:

```text
Test A01–A05 against contradictory cosmology, source field, ontology, Dao, and scale pressure.
```

### Pilot 2 — Advancement / Action Pilot

Size:

```text
24–36 packets
```

Purpose:

```text
Test A06–A10 against class, level, cultivation, psionic, cyberware, skill, and resource systems.
```

### Pilot 3 — Operational / Schema Pilot

Size:

```text
48–72 packets
```

Purpose:

```text
Test A11–A15 and C00/C01/C02/C03/C10 against actors, assets, combat, travel, factions, tables, statblocks, and maps.
```

Pilot selection must include:

- fantasy class-level packets
- sci-fi lifepath or skill packets
- cultivation realm packets
- cyberware/implant packets
- starship/platform packets
- mech packets
- random table packets
- bestiary/statblock packets
- faction/economy packets
- cosmology/plane packets
- map/diagram packets
- deliberate contradiction packets

## 23. Broad Conversion Gate

Do not proceed to broad conversion of the 1,900-donor corpus until all of the following are true:

```text
A01–A15 are pressure-tested or current.
C00 is current.
C01, C02, C03, and C10 are pressure-tested or current.
K01–K04 are current.
The 48–72 packet operational/schema pilot passes.
The conflict ledger has no unresolved high-severity doctrine blockers.
The schema violation rate is below the accepted threshold.
The source-local retention process is functioning.
The quarantine process is functioning.
The review queue is functioning.
No donor-law creep is detected in pilot conversion outputs.
```

Broad conversion can proceed in expanding stages:

```text
50-donor controlled batch
200-donor expansion batch
500-donor stabilization batch
full 1,900-donor corpus
```

Each expansion requires aggregation review before the next expansion.

## 24. Runtime Gate

Do not proceed to runtime implementation until all of the following are true:

```text
A01–A15 are current.
C00–C14 are pressure-tested or current.
K01–K06 are current or pressure-tested.
At least 500 valid, quarantined conversion-intake memos exist.
K04 has processed major cross-donor contradictions.
K05 and K06 have draft tables of contents.
R01–R04 are drafted and reviewed before implementation begins.
```

Runtime implementation must prove:

- backend owns state;
- backend owns dice/RNG;
- backend owns validation;
- backend owns persistence through PersistenceOrchestrator, EventLedgerWriter, StateStoreWriter, EntityRecordWriter, GeneratedContentRecordWriter, KnowledgeClaimWriter, DialogueTranscriptWriter, ConversationSummaryWriter, RetrievalIndexWriter, and FileExportWriter responsibilities;
- primary persistence is database/event-log/state-store backed, with files as materialized exports only;
- LLMs cannot mutate state directly;
- LLMs cannot write files directly;
- context packets do not leak hidden information;
- generated content becomes durable only through backend-owned schema, validation, provenance, and commit pathways;
- dialogue transcripts remain distinct from validated authoritative claims and state deltas;
- replay and hash verification work.


## 24A. Future Runtime Boundary + Generator Ownership Audit

This roadmap adds a future audit item only. This PR does not perform the audit, rewrite Batch A/B/C doctrine, modify D00-D19 draft source material, implement runtime code, or create generator/runtime schemas.

Audit preparation protocol: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`. The protocol is control scaffolding only and does not contain audit findings.

Audit scope:

- Batch A;
- Batch B;
- Batch C;
- D00-D19;
- schema/math/mechanics workstream files.

The audit must classify each subsystem as one or more of:

```text
doctrine_only
schema_ready
runtime_ready
generator_ready
validator_ready
context_packet_ready
narration_only
blocked_pending_schema
blocked_pending_math
blocked_pending_runtime
```

The audit output must identify, for each subsystem:

- missing backend pieces;
- required schemas;
- required math/mechanics;
- required generators/templates;
- required command IR;
- required state/event fields;
- required tests;
- whether the LLM is currently being asked to do too much.

Required output shape:

```yaml
subsystem_id: <stable identifier>
source_area: <Batch A | Batch B | Batch C | D00-D19 | schema/math/mechanics>
classification:
  - <one or more allowed classification labels>
doctrine_owner: <file or pending owner>
missing_backend_pieces:
  - <piece>
required_schemas:
  - <schema or field family>
required_math_mechanics:
  - <math/mechanics requirement>
required_generators_templates:
  - <generator/template requirement>
required_command_ir:
  - <command/IR requirement>
required_state_event_fields:
  - <state/event field requirement>
required_tests:
  - <test requirement>
llm_overreach_risk: <none | low | medium | high | critical>
notes: <short rationale>
```

This audit must preserve the backend-first model interchangeability invariant: if a subsystem requires persistent truth, rules, dice, validation, generated content, retrieval, memory, or consequences, the backend must own the authoritative pathway and the LLM may only narrate, summarize, interpret, or propose within contract.

## 25. Live-Play / Training Gate

Do not proceed to live-play training until all of the following are true:

```text
R01–R08 are current or pressure-tested.
T01–T07 are current or pressure-tested.
Gold examples derive only from current doctrine and accepted canon.
Benchmark packs test all major doctrine domains.
Unsafe behavior hard-fail matrix is active.
At least 10 live pilot sessions exist with state deltas, transcripts, and review notes.
No training example contradicts doctrine or runtime authority.
```

## 26. Highest-Risk Missing Files

If only five files can be drafted next, draft these:

```text
A01_cosmology_and_dimensional_architecture.md
A02_source_fields_magic_technology_relation.md
A04_dao_domain_element_architecture.md
A06_cultivation_and_ascension_stage_architecture.md
K01_lexicon_governance_and_reserved_terms.md
```

Why:

- A01 prevents donor cosmology from defining Astra reality.
- A02 prevents magic and technology from becoming incompatible silos.
- A04 prevents donor Dao/domain/element systems from becoming Astra metaphysics.
- A06 prevents donor classes, levels, or cultivation realms from defining advancement.
- K01 prevents donor vocabulary from becoming Astra vocabulary.

Secondary risk files:

```text
A03_soul_body_mind_spirit_ontology.md
A05_civilization_scale_and_power_scale_doctrine.md
A10_resource_cost_backlash_and_corruption_doctrine.md
C00_shared_content_record_base_and_schema_registry.md
K04_conflict_ledger_and_cross_donor_pressure_protocol.md
```

## 27. Immediate Next Actions After PR #204

The previous bootstrap-oriented instructions for committing ROADMAP-001, creating REGISTRY-001, adding the initial registry records, and drafting A01-A05 are superseded. Those instructions must not be followed as the current next-action list because the repository has already advanced through multiple doctrine, schema, and control PRs.

Current immediate actions are:

1. Reconcile roadmap, registry, and current-state language after PR #204 so future work starts from the actual repository state.
2. Repair the local/test dependency setup so PyYAML-backed registry validation can run from the documented dependency instructions.
3. Run focused doctrine and registry validation tests before broad test runs.
4. Produce or update a current-state ledger entry that summarizes completed Batch A/B/C/D/control status as represented by the repo, without promoting uncertain files beyond their registry status.
5. Add or maintain explicit notes warning future models and reviewers not to follow obsolete roadmap-bootstrap sections.
6. Prepare the Runtime Boundary + Generator Ownership Audit as a later work item, but do not perform the audit in this reconciliation patch.
7. Identify stale references that present Aether Forge as the project identity and demote them to extraction/handoff subsystem references.
8. Confirm registry records added by PR #204 remain planning/control records and do not claim runtime implementation, generator implementation, persistence writers, or live-play behavior.
9. Confirm that this cleanup creates no runtime code, database schemas, file writers, generated-content records, generators, live-play adapters, donor content, training sets, or canon promotion.
10. Record test results honestly, including missing dependencies or environment limitations.

Standing gates remain unchanged: runtime implementation is not authorized; live-play training is not authorized; broad conversion scale remains gated by current doctrine, schema, evaluation, and pilot readiness; extraction and handoff remain subordinate developer tooling.

## 28. Explicit Contradiction Test Pack

Minimum donor pressure types for Phase 1–3 pressure tests:

```text
monotheistic divine-order cosmology
scientific-materialist cosmology
cultivation-realm cosmology
magic-opposes-technology model
magic-is-technology model
technology-is-mundane model
class-and-level advancement
skill-based advancement
cultivation-realm advancement
cyberware-heavy asset system
relic/cultivation-tool asset system
mech-focused asset system
starship-focused asset system
personal combat system
fleet combat system
planar travel system
stellar travel system
faction/economy system
random-table heavy system
```

## 29. Failure Modes and Mitigation

| Failure Mode | Symptoms | Mitigation |
|---|---|---|
| Donor-law creep | donor terms or mechanics become Astra defaults | hard refusals, K01, contradiction tests |
| Fragmentation | many files claim overlapping authority | registry, anti-fragmentation doctrine |
| Schema-first chaos | schemas invent mechanics | C00, schema must_not_own rules |
| Runtime contamination | backend defaults redefine doctrine | runtime gate, R01–R08 authority limits |
| Training-as-doctrine | examples override rules | T07, examples marked illustrative |
| Scale-before-structure | full corpus converted too early | pilot gates and expansion batches |
| Lexicon drift | donor terms become entrenched | K01 early placeholder and term review |
| Cultivation collapse | cultivation becomes flavor or donor stages | A06 hard refusals and tests |
| Magic-tech siloing | magic and tech become unrelated systems | A02 pressure matrix |
| Scale collapse | everything resolves at personal scale | A05, A13, A14 |

## 30. How This Roadmap Prevents Donor-Law Creep

This roadmap prevents donor-law creep by requiring:

- Astra-native setting spine before broad conversion;
- lawful outcome assignment for every donor construct;
- source-local retention for unmapped donor constructs;
- hard refusals in every doctrine file;
- lexicon governance before canon consolidation;
- conflict ledger review for contradictions;
- schema validation after doctrine, not before;
- pilot pressure tests before scale;
- canon promotion only through K03;
- runtime implementation only after doctrine/canon/schema stability;
- training only after runtime and accepted canon.

## 31. How This Roadmap Supports a 1,900-Donor Corpus

The roadmap supports 1,900-donor scale through:

- fused spine files that reduce authority surface area;
- schema records that make conversion output machine-reviewable;
- source-local retention for outliers;
- quarantine and escalation queues;
- conflict ledger for cross-donor contradictions;
- pilot batches before full scale;
- expansion sequence from 50 → 200 → 500 → 1,900 donors;
- registry-based gating;
- status promotion rules;
- explicit broad conversion gate.

The goal is not to pre-solve every donor edge case. The goal is to ensure every donor construct has a lawful landing zone or escalation route.

## 32. How This Roadmap Preserves Astra Identity

Astra identity is preserved by:

- making high-tech/high-magic, space-faring, multiplanar cultivation the explicit premise;
- drafting cosmology, source fields, ontology, Dao architecture, and scale before advancement;
- drafting cultivation and ascension before asset/combat/faction systems;
- integrating starships, mechs, cyberware, relics, magic, cultivation, psionics, and planar travel as central systems;
- refusing donor defaults unless normalized by Astra doctrine;
- preventing examples, runtime, or schemas from overriding doctrine.

## 33. Versioning and Review Protocol

Versioning:

```text
major.minor.patch
```

- Major: authority hierarchy, phase order, or gate changes.
- Minor: new file records, changed dependency locks, new gates.
- Patch: wording, typos, formatting, reference updates.

Review cadence:

```text
weekly during Phase 0–1B
biweekly during Phase 1C–3
monthly after Phase 4 begins
immediate review after any failed pressure test
```

Amendment process:

1. propose change;
2. identify affected files;
3. update registry;
4. run affected pressure tests;
5. record decision;
6. version bump;
7. commit updated roadmap.

Deprecation process:

1. replacement file reaches current;
2. downstream references migrate;
3. deprecated file remains in registry;
4. migration note recorded;
5. no deleted doctrine without archive.

## 34. File List by Phase

### Phase 0 — Control

```text
ROADMAP-001 — docs/doctrine/astra_doctrine_roadmap_v0_1.md
REGISTRY-001 — docs/doctrine/astra_doctrine_registry_v0_1.yaml
```

### Phase 1A — Setting Spine

```text
A01 — doctrine/core/A01_cosmology_and_dimensional_architecture.md
A02 — doctrine/core/A02_source_fields_magic_technology_relation.md
A03 — doctrine/core/A03_soul_body_mind_spirit_ontology.md
A04 — doctrine/core/A04_dao_domain_element_architecture.md
A05 — doctrine/core/A05_civilization_scale_and_power_scale_doctrine.md
```

### Phase 1B — Advancement / Action Spine

```text
A06 — doctrine/core/A06_cultivation_and_ascension_stage_architecture.md
A07 — doctrine/core/A07_advancement_axes_and_progression_pressure.md
A08 — doctrine/core/A08_path_domain_and_technique_mastery_doctrine.md
A09 — doctrine/core/A09_skill_competency_and_synthesis_doctrine.md
A10 — doctrine/core/A10_resource_cost_backlash_and_corruption_doctrine.md
```

### Phase 1C — World / Asset / Conflict Spine

```text
A11 — doctrine/core/A11_actor_ontology_and_player_grade_actor_doctrine.md
A12 — doctrine/core/A12_asset_relic_implant_platform_doctrine.md
A13 — doctrine/core/A13_combat_hazard_damage_and_consequence_doctrine.md
A14 — doctrine/core/A14_travel_exploration_and_scale_transition_doctrine.md
A15 — doctrine/core/A15_faction_society_economy_and_institution_doctrine.md
```

### Phase 2 — Schema Base

```text
C00 — doctrine/schema/C00_shared_content_record_base_and_schema_registry.md
C01 — doctrine/schema/C01_creature_npc_record_schema.md
C02 — doctrine/schema/C02_item_gear_record_schema.md
C03 — doctrine/schema/C03_ability_power_technique_record_schema.md
C04 — doctrine/schema/C04_relic_implant_installable_asset_schema.md
C05 — doctrine/schema/C05_faction_institution_record_schema.md
C06 — doctrine/schema/C06_location_site_region_record_schema.md
C07 — doctrine/schema/C07_mission_scenario_adventure_record_schema.md
C08 — doctrine/schema/C08_vehicle_ship_platform_record_schema.md
C09 — doctrine/schema/C09_hazard_environment_record_schema.md
C10 — doctrine/schema/C10_table_oracle_record_schema.md
C11 — doctrine/schema/C11_companion_summon_record_schema.md
C12 — doctrine/schema/C12_crafting_salvage_recipe_record_schema.md
C13 — doctrine/schema/C13_map_diagram_record_schema.md
C14 — doctrine/schema/C14_source_local_setting_cosmology_record_schema.md
```

### Phase 3 — Canon / Lexicon

```text
K01 — doctrine/canon/K01_lexicon_governance_and_reserved_terms.md
K02 — doctrine/canon/K02_source_local_boundary_and_rejected_import_doctrine.md
K03 — doctrine/canon/K03_canon_promotion_protocol.md
K04 — doctrine/canon/K04_conflict_ledger_and_cross_donor_pressure_protocol.md
K05 — doctrine/canon/K05_mechanics_bible_structure.md
K06 — doctrine/canon/K06_setting_bible_structure.md
```

### Phase 4 — Runtime

```text
R01 — doctrine/runtime/R01_deterministic_event_kernel.md
R02 — doctrine/runtime/R02_state_model_and_entity_component_schema.md
R03 — doctrine/runtime/R03_command_lifecycle_and_state_delta_validation.md
R04 — doctrine/runtime/R04_dice_rng_and_randomness_authority.md
R05 — doctrine/runtime/R05_context_packet_compiler.md
R06 — doctrine/runtime/R06_hidden_information_partitioning.md
R07 — doctrine/runtime/R07_faction_world_clocks_and_economy_state.md
R08 — doctrine/runtime/R08_campaign_persistence_replay_and_hash_verification.md
```

### Phase 5 — Training / Evaluation

```text
T01 — doctrine/training/T01_conversion_adapter_evaluation_protocol.md
T02 — doctrine/training/T02_live_play_adapter_behavior_contract.md
T03 — doctrine/training/T03_context_packet_example_pack.md
T04 — doctrine/training/T04_failure_label_taxonomy.md
T05 — doctrine/training/T05_gold_example_selection_protocol.md
T06 — doctrine/training/T06_benchmark_pack_design.md
T07 — doctrine/training/T07_unsafe_behavior_hard_fail_matrix.md
```

## 35. Closing Rule

This roadmap is not successful because it lists many files.

It is successful only if it prevents these outcomes:

- donor assumptions becoming Astra law;
- schemas validating donor-shaped records as Astra-native;
- canon absorbing conversion output without review;
- runtime redefining doctrine through implementation defaults;
- training examples becoming authority;
- the full 1,900-donor corpus being processed before the doctrine spine can survive contradiction.

The project proceeds in this order:

```text
roadmap and registry
→ A01–A05 setting spine
→ A06–A10 advancement/action spine
→ A11–A15 operational spine
→ C00 and high-pressure schemas
→ K01–K04 canon/lexicon gates
→ pilots
→ expansion batches
→ runtime
→ live-play training
```

**End of ROADMAP-001 v0.1**
