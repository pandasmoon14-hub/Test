# Production Batch 001 Aggregation Note

This note records the first aggregation pass over Production Batch 001 conversion-intake results.

This is a conversion-stage aggregation artifact only. It does not promote donor material to Astra canon.

## Batch identity

- Conversion-intake run: `C:\AetherForgeRuns\prod_batch_001\conversion_intake_run`
- Aggregation output directory: `C:\AetherForgeRuns\prod_batch_001\conversion_intake_run\reports\aggregation`
- Aggregation report JSON: `C:\AetherForgeRuns\prod_batch_001\conversion_intake_run\reports\aggregation\batch_001_aggregation_report.json`
- Note generated: 2026-05-16T16:38:06

## Aggregation status

- Packets total: 36
- Result status counts: `{"drafted": 36}`
- Human review queue count: 36

## Lawful outcome counts

- normalized Astra mapping: 2130
- source-local retained construct: 828
- direct Astra mapping: 335
- escalated doctrine problem: 238
- quarantined construct pending later doctrine: 143

## Confidence signal

- Confidence average: unknown
- Confidence minimum: unknown
- Confidence maximum: unknown

## Donor-family pressure

- unclassified_or_mixed_donor_family: 16
- wuxia_cultivation_martial: 5
- universal_toolkit_or_generic_engine: 4
- jrpg_heroic_fantasy: 3
- osr_survival_sandbox: 3
- cyberpunk_biotech_transhuman: 2
- traveller_lifepath_trade_starship: 2
- mech_vehicle_tactical_platform: 1

## Top construct-family pressure

- unclassified_or_mixed: 612 mappings; outcomes: `{"direct Astra mapping": 55, "escalated doctrine problem": 44, "normalized Astra mapping": 301, "quarantined construct pending later doctrine": 37, "source-local retained construct": 175}`
- ability_power_spell_technique: 550 mappings; outcomes: `{"direct Astra mapping": 29, "escalated doctrine problem": 49, "normalized Astra mapping": 369, "quarantined construct pending later doctrine": 20, "source-local retained construct": 83}`
- damage_condition_effect_survivability: 300 mappings; outcomes: `{"direct Astra mapping": 13, "escalated doctrine problem": 32, "normalized Astra mapping": 208, "quarantined construct pending later doctrine": 6, "source-local retained construct": 41}`
- scene_mission_adventure_scenario: 267 mappings; outcomes: `{"direct Astra mapping": 52, "escalated doctrine problem": 3, "normalized Astra mapping": 106, "source-local retained construct": 106}`
- resource_cost_recharge_backlash: 257 mappings; outcomes: `{"direct Astra mapping": 10, "escalated doctrine problem": 24, "normalized Astra mapping": 178, "quarantined construct pending later doctrine": 4, "source-local retained construct": 41}`
- vehicle_platform_starship_mech: 242 mappings; outcomes: `{"direct Astra mapping": 18, "escalated doctrine problem": 5, "normalized Astra mapping": 173, "quarantined construct pending later doctrine": 10, "source-local retained construct": 36}`
- competency_skill_profession: 222 mappings; outcomes: `{"direct Astra mapping": 9, "escalated doctrine problem": 5, "normalized Astra mapping": 171, "quarantined construct pending later doctrine": 1, "source-local retained construct": 36}`
- world_region_faction_setting: 174 mappings; outcomes: `{"direct Astra mapping": 6, "escalated doctrine problem": 8, "normalized Astra mapping": 73, "quarantined construct pending later doctrine": 4, "source-local retained construct": 83}`
- extraction_provenance_and_handoff: 163 mappings; outcomes: `{"direct Astra mapping": 70, "escalated doctrine problem": 4, "normalized Astra mapping": 29, "quarantined construct pending later doctrine": 43, "source-local retained construct": 17}`
- gear_item_crafting_loot_economy: 150 mappings; outcomes: `{"direct Astra mapping": 10, "escalated doctrine problem": 10, "normalized Astra mapping": 96, "quarantined construct pending later doctrine": 2, "source-local retained construct": 32}`
- progression_advancement_growth: 133 mappings; outcomes: `{"direct Astra mapping": 15, "escalated doctrine problem": 16, "normalized Astra mapping": 71, "quarantined construct pending later doctrine": 2, "source-local retained construct": 29}`
- creature_npc_bestiary_companion: 117 mappings; outcomes: `{"direct Astra mapping": 7, "escalated doctrine problem": 10, "normalized Astra mapping": 67, "quarantined construct pending later doctrine": 1, "source-local retained construct": 32}`
- player_chassis_and_character_creation: 111 mappings; outcomes: `{"direct Astra mapping": 15, "normalized Astra mapping": 79, "quarantined construct pending later doctrine": 2, "source-local retained construct": 15}`
- origin_kinform_culture_background: 108 mappings; outcomes: `{"direct Astra mapping": 1, "escalated doctrine problem": 4, "normalized Astra mapping": 51, "quarantined construct pending later doctrine": 4, "source-local retained construct": 48}`
- hazard_environment_exploration_travel: 62 mappings; outcomes: `{"direct Astra mapping": 2, "escalated doctrine problem": 2, "normalized Astra mapping": 41, "quarantined construct pending later doctrine": 1, "source-local retained construct": 16}`

## Immediate interpretation

Production Batch 001 confirms that the conversion-intake handoff can scale from the pilot into a 36-packet production-style batch while preserving conversion/canon separation.

The high normalized-mapping count indicates that existing Astra architecture catches a large share of donor constructs, but the 238 escalated doctrine problems and 143 quarantined constructs are large enough to require a formal review pass before any larger production run.

The 828 source-local retained constructs are not a failure. They show that donor-specific names, examples, settings, localized mechanics, and non-canonical details are being contained instead of leaking into Astra doctrine.

The high unclassified-or-mixed donor-family count should be treated as a routing/classification pressure. Before scaling to hundreds of donors, the packet planner and aggregation layer should improve donor-family labeling so later production batches can be compared by structural family rather than only by individual packet.

## Review priorities

1. Review the doctrine-pressure report for repeated escalations that appear across multiple donor families.
2. Review the source-local retention report to verify that donor-specific material is being contained rather than normalized too aggressively.
3. Review the quarantine/escalation queue before Batch 002.
4. Identify extraction/layout issues, especially mojibake, table flattening, map/diagram dependency, and under-parsed statblocks.
5. Create donor-family templates for recurring families before scaling further.
6. Do not promote any construct directly to canon from this aggregation.

## Recommended next phase

Proceed to a Batch 001 aggregation review memo.

That memo should classify recurring pressure into:

- doctrine refinement required now
- doctrine refinement reserved for later batch
- extraction or packet-shape issue
- donor-family template issue
- source-local residue, no doctrine action
- quarantine retained pending more examples

After that review, choose whether Batch 002 should be another mixed-pressure batch or a targeted donor-family-template batch.
