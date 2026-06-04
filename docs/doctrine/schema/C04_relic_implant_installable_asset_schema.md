# C04 Relic/Implant/Installable Asset Record Schema Doctrine

## 1. Purpose and status

C04 defines Batch C conversion-stage and canon-review record-family schema doctrine for relic/implant/installable asset records. It covers relics, implants, cyberware, biotech, attunement-like assets, bonded assets, installed modules, socketed assets, augmentations, host-integrated assets, upgradeable special assets, symbiotes, prosthetics, vehicle/platform modules, and similar special installed-asset records extracted from donor material and converted into Astra-facing review records.

Status posture:
- C04 is a schema-draft doctrine file.
- C04 is not current canon, not accepted lexicon, not sourcebook relic prose, not sourcebook implant prose, not sourcebook item prose, not live-play authority, not live-play behavior, and not runtime-ready.
- C04 is not final relic mechanics, final implant math, cyberware economy, biotech economy, essence systems, cyberpsychosis systems, attunement rules, license rules, pilot-license rules, Lancer license default, Shadowrun essence default, slot mechanics, socket mechanics, upgrade slot mechanics, hardpoint mechanics, installation procedure, removal procedure, surgery procedure, repair procedure, upgrade procedure, combat balance, runtime installation state, runtime body-slot state, runtime attunement state, runtime license state, runtime module state, runtime host-integration state, donor implant/relic/cyberware-system import, or canon promotion procedure.
- C04 records are conversion-stage/canon-review artifacts only; they preserve evidence, boundaries, routing, and review posture until appropriate owners decide what can become canon, final mechanics, or runtime implementation.

## 2. Owner layer

C04 belongs to Batch C schema-family doctrine under the Astra Doctrine Council - Schema Working Group. It sits below C00 and must obey the Batch C unlock/index/readiness gate. C04 uses Batch A asset, actor, resource, cost, consequence, technology/metaphysics, vehicle/platform, source-local, and legal/IP doctrine as upstream conceptual guardrails and Batch B operations only as handoff pressure, not as schema-field authority.

## 3. What C04 owns

C04 owns conversion-stage record-family grammar for:
- relics, implants, cyberware, biotech, attunement-like assets, bonded assets, installed modules, socketed assets, augmentations, host-integrated assets, upgradeable special assets, symbiotes, prosthetics, vehicle/platform modules, and similar special installed-asset records;
- relic/implant/installable asset conversion records whose main identity is a special installed, bonded, socketed, integrated, carried-as-relic, or host/interface asset rather than the actor, ordinary item, granted ability, faction, location, scenario, platform, hazard, table row, recipe/process, diagram, or source-local setting assertion that carries, grants, places, installs, restricts, or contextualizes it;
- C04-specific relic/implant/installable asset classification and routing posture for conversion and canon review;
- C04 parent, child, composite, and satellite handling when the central record remains a special asset record;
- references from the special asset record to host creatures/NPCs, item/gear objects, ability/power/technique records, factions, locations, scenarios, vehicle/platform records, hazards, table/oracle rows, recipes/processes, map/diagram records, companions/summons, and source-local owners;
- donor relic, implant, cyberware, biotech, module, socket, upgrade, attunement, license, and field-name containment as evidence, donor tags, rejected donor elements, or source-local context, not Astra defaults.

## 4. What C04 must not own

C04 must not own or define:
- final mechanics, final relic mechanics, final implant math, cyberware economy, biotech economy, essence systems, cyberpsychosis systems, attunement rules, license rules, pilot-license rules, combat balance, final numerical values, body slots, implant slots, essence costs, humanity costs, corruption costs, attunement limits, license levels, rank gates, upgrade slots, hardpoints, socket counts, module capacity, repair DCs, installation DCs, surgery costs, crafting costs, removal risks, cyberpsychosis thresholds, biotech rejection chance, backlash values, cooldowns, charges, damage values, defensive values, resource math, or economy math;
- Shadowrun essence default, Cyberpunk humanity/cyberpsychosis defaults, D&D attunement default, Lancer license default, slot/hardpoint/socket systems, source-specific implant economies, donor rank/license tracks, donor resource systems, donor installation procedures, donor surgery procedures, donor repair rules, donor upgrade rules, donor crafting costs, donor repair values, donor module capacities, donor field names, donor costs, or donor resource math as Astra defaults;
- runtime installation state, runtime body-slot state, runtime attunement state, runtime license state, runtime module state, runtime host-integration state, runtime actor state, runtime item state, equipment runtime, entity/component schemas, event schemas, command lifecycle, context packets, save-state nodes, database asset rows, database contracts, backend equipment schemas, backend implant schemas, combat trackers, persistence models, or live runtime behavior;
- sourcebook relic prose, sourcebook implant prose, implant catalog prose, player-facing relic prose, player-facing implant entries, live-play installation procedure, GM equipment execution, accepted lexicon, canon acceptance, canon promotion, training examples, or donor implant/relic/cyberware-system import;
- donor exact relic names, implant names, cyberware names, biotech names, module names, slot names, license names, named artifacts, named modules, named implant traditions, protected proper nouns, donor-world technology laws, source-specific metaphysics, donor-world assumptions, trademark-like asset names, or source-specific lore as Astra defaults;
- actor/host identity, ordinary item/gear identity, ability/effect identity, faction access law, location-bound placement, scenario scripts, vehicle/platform identity, hazard/environment pressure, table/oracle generation, crafting/salvage/recipe/install/removal processes, map/diagram evidence, companion/summon relation posture, or source-local setting law except by reference to their owner families.

## 5. C00 inheritance and required base posture

Every durable C04 conversion-stage record must inherit/include `AstraContentRecordBase` from C00 before any C04-specific shaping. C04 may add family-specific doctrine grammar, but it must not remove, rename, or weaken C00 base posture.

C04 must preserve these C00 requirements:
- `packet_refs`, `source_evidence_refs`, `construct_refs`, `outcome_refs`, and `provenance_refs`;
- `source_local_boundary`, `rejected_donor_elements`, `canon_eligibility`, `confidence`, `validation`, `lineage`, `composition`, cross-reference, legal/IP posture, review routing, and source-local boundary posture;
- parent/child/satellite links, cross-family references with `inheritance_allowed: false`, and escalation routes for low confidence, source-local pressure, hidden/protected truth, missing schema coverage, and legal/IP risk;
- C00 record status and review status language, including conversion-stage, source-local, canon-candidate, quarantined, rejected-import, and human-review routing.

C04-specific doctrine can classify special asset records, but it cannot bypass C00 provenance, evidence, legal/IP, source-local, rejected-import, canon-eligibility, confidence, validation, lineage, composition, or cross-reference controls.

## 6. Relic/implant/installable asset family scope and classification

C04 classifies special installed-asset records by conversion/review role, not by final mechanics. Neutral Astra-facing categories include:
- asset classification posture: relic-like, implant-like, cyberware-like, biotech-like, attunement-like, bonded-asset-like, module-like, socketed-asset-like, augmentation-like, prosthetic-like, symbiote-like, platform-module-like, unknown special asset;
- host/interface posture: no host asserted, actor-host reference required, platform-host reference required, item-shell reference required, companion-host reference required, protected or source-local host claim;
- installation/bonding posture: carried-as-relic evidence, installed evidence, bonded evidence, socketed evidence, grafted evidence, integrated evidence, removable evidence, unknown installation/bonding evidence;
- integration depth posture: external interface, worn interface, carried focus, body-integrated, mind/spirit-integrated, machine-integrated, vehicle/platform-integrated, source-local integration claim, protected-hidden integration claim;
- capability-reference posture, item/reference posture, crafting/upgrade/reference posture, acquisition/access reference posture, vehicle/platform reference posture, hazard/backlash reference posture, source-local/canon-review posture, hidden/protected-truth posture, legal/IP posture, and rejection/containment posture.

These categories are routing labels for conversion review only. They do not create final body slots, implant slots, essence costs, humanity costs, license levels, hardpoints, sockets, attunement caps, module capacities, upgrade mechanics, or runtime state.

## 7. C04 record grammar, doctrine-level only

The following YAML-like block is doctrine grammar only. It is not a runtime schema, not a database schema, not a final relic statblock, not an implant system, not a cyberware system, not a biotech system, not an attunement system, not a license system, not an upgrade-slot system, not an installation-state schema, and not sourcebook item prose.

```yaml
C04RelicImplantInstallableAssetRecord:
  extends: AstraContentRecordBase
  schema_family: C04
  asset_classification_posture: relic_like | implant_like | cyberware_like | biotech_like | attunement_like | bonded_asset_like | installed_module_like | socketed_asset_like | augmentation_like | prosthetic_like | symbiote_like | platform_module_like | unknown_special_asset
  host_interface_posture: none_asserted | actor_host_ref_required | platform_host_ref_required | item_shell_ref_required | companion_host_ref_required | protected_or_source_local_host_claim | unknown
  installation_bonding_posture: carried_relic_evidence | installed_evidence | bonded_evidence | socketed_evidence | grafted_evidence | integrated_evidence | removable_evidence | unknown
  integration_depth_posture: external_interface | worn_interface | carried_focus | body_integrated | mind_spirit_integrated | machine_integrated | vehicle_platform_integrated | source_local_claim | protected_hidden_claim | unknown
  capability_reference_posture:
    c03_refs: [string]
    note: doctrine references only; no embedded donor action, effect, power, damage, cooldown, charge, or resource math
  item_reference_posture:
    c02_refs: [string]
    note: practical object shell or ordinary gear evidence remains with C02
  host_reference_posture:
    c01_refs: [string]
    c11_refs: [string]
    note: host, wearer, user, recipient, bonded actor, companion, or summon identity remains outside C04
  crafting_upgrade_reference_posture:
    c12_refs: [string]
    b06_pressure_note: doctrine-facing only; not a C04 schema field and not project procedure inheritance
  acquisition_access_reference_posture:
    c05_refs: [string]
    b05_pressure_note: doctrine-facing only; not a C04 schema field and not value-flow procedure inheritance
  vehicle_platform_reference_posture:
    c08_refs: [string]
    note: platform modules use references, not inheritance
  hazard_backlash_reference_posture:
    c09_refs: [string]
    note: hazardous, cursed, corrupting, unstable, or backlash pressure routes to C09/A10 review
  source_local_canon_review_posture:
    c14_refs: [string]
    donor_tag_refs: [string]
    note: source-local names, metaphysics, technology laws, and license systems remain contained
  hidden_protected_truth_posture: none | protected_truth | hidden_from_player | spoiler_sensitive | legal_sensitive | unknown
  legal_ip_posture: clear | needs_review | source_local_only | protected_name | protected_art_or_diagram | rejected_or_quarantined
  rejection_containment_posture: none | donor_system_rejected | donor_field_rejected | donor_math_rejected | donor_name_contained | source_local_only | pending_schema
```

The block avoids donor relic/implant/cyberware/biotech/module/license field names as Astra labels. It uses neutral posture names and references instead of importing donor statblocks, install rules, body-slot rules, license tracks, attunement limits, hardpoints, socket counts, or upgrade math.

## 8. Donor relic, implant, cyberware, biotech, attunement, license, socket, module, upgrade, and field-name handling

Donor exact relic names, donor implant names, donor cyberware names, donor biotech names, donor module names, donor slot names, donor license names, donor attunement rules, donor essence costs, donor humanity costs, donor rank/license tracks, donor upgrade slots, donor socket rules, donor hardpoint labels, donor installation procedures, donor surgery rules, donor crafting costs, donor repair values, donor module capacities, donor field labels, donor proper nouns, donor-world technology laws, and donor-world assumptions may be preserved only as source evidence, donor tags, source-local notes, legal/IP review notes, C14 containment records, or rejected donor elements.

C04 explicitly blocks donor systems from becoming Astra defaults without later doctrine/canon review, including:
- donor relic systems, donor implant systems, donor cyberware systems, donor biotech systems, donor attunement rules, donor license rules, donor slot/hardpoint/socket systems, donor upgrade slots, donor installation procedures, donor surgery procedures, donor costs, donor resource math, donor field names, donor proper nouns, named artifacts, named modules, named implant traditions, named technology laws, and donor-world assumptions;
- Shadowrun essence default and Shadowrun essence costs;
- Cyberpunk humanity/cyberpsychosis defaults, humanity costs, and cyberpsychosis thresholds;
- D&D attunement default, D&D attunement limits, and source-specific attunement rules;
- Lancer license default, Lancer license levels, rank/license tracks, and source-specific pilot-license rules;
- source-specific implant economies, cyberware economies, biotech rejection rules, module-capacity systems, socket counts, hardpoint systems, upgrade-slot mechanics, and body-slot systems.

If donor material supplies an attractive field label such as essence, humanity, attunement, license, slot, hardpoint, socket, capacity, module rank, install DC, surgery cost, graft rejection, cyberpsychosis, or equivalent source-specific term, C04 stores it as evidence or rejection/containment data. C04 does not normalize it into an Astra schema field or accepted lexicon term.

## 9. Item, ability, host, installation, crafting, acquisition, vehicle/platform, source-local, and legal/IP handoffs

Batch B handoffs are doctrine-facing pressure only and are not C04 schema fields:
- C04 references B03 when relic/implant/installable asset use creates item/gear/equipment/asset use pressure, but B03 is not C04 schema.
- C04 references B04 when custody, storage, burden, wearing, carrying, body-placement, or containment pressure appears, but B04 is not C04 schema.
- C04 references B05 when acquisition, requisition, reward, restricted access, license-like access, faction supply, value flow, purchase, or patronage pressure appears, but B05 is not C04 schema.
- C04 references B06 when crafting, salvage, repair, installation, removal, upgrade, modification, tuning, socketing, bonding, surgery-like work, or project procedure pressure appears, but B06 is not C04 schema.
- C04 may reference B02 when asset use affects action declaration, cost commitment, or resolution trigger pressure, but B02 is not C04 schema.
- Batch B procedure terms must not become C04 schema fields, inherited properties, runtime commands, or database rows.

Cross-family handoffs:
- C04 -> C01 for host creatures/NPCs, users, wearers, implant recipients, bonded actors, symbiote hosts, prosthetic users, or asset-bearing actors.
- C04 -> C02 for practical item/gear object evidence, carried or worn gear, mundane equipment component, consumable interface, object shell, or asset treated primarily as ordinary gear.
- C04 -> C03 for relic-granted abilities, implant-granted capabilities, active effects, passive effects, bonded powers, module powers, augmentation effects, interface routines, or special actions.
- C04 -> C05 for faction/institution access, restricted license, guild/sect/corporate manufacture, ownership, legal authority, rank-gated access, requisition body, or institutional doctrine.
- C04 -> C06 for installation sites, laboratories, relic sites, workshops, biotech clinics, shipyards, temples, ruins, vaults, stations, or place-bound assets.
- C04 -> C07 for scenario/adventure/mission use, quest relics, implant objectives, cursed assets, mission-critical modules, reward placement, or story-role assets.
- C04 -> C08 for vehicle/ship/platform modules, ship systems, mech modules, station modules, hardpoint-like assets, platform-integrated systems, onboard assets, or vehicle-scale installable assets.
- C04 -> C09 for hazardous implants, cursed relics, unstable biotech, radiation/corruption/contamination pressure, dangerous modules, backlash hazards, failure hazards, or environmental interactions.
- C04 -> C10 for relic/implant/installable asset tables, module generators, upgrade tables, random artifact tables, cyberware/biotech tables, or source-specific asset generators.
- C04 -> C11 for companion/summon bonded assets, pet implants, spirit-bound relics, controlled symbiotes, minion augmentations, or follower equipment that changes companion/summon posture.
- C04 -> C12 for crafting/salvage/recipe/repair/upgrade/installation/removal/modification records, blueprints, schematics, recipes, materials, salvage patterns, or transformation processes.
- C04 -> C13 for relic diagrams, implant schematics, installation diagrams, cyberware diagrams, biotech diagrams, module diagrams, socket diagrams, upgrade schematics, visual asset evidence, or protected art.
- C04 -> C14 for source-local relic names, implant systems, cyberware traditions, biotech traditions, named artifacts, named modules, license systems, donor-world technology law, source-specific metaphysics, protected proper nouns, and donor-world assumptions.
- C04 -> pending_schema when no stable C-family owner exists.

## 10. C04 cross-family overlap rules

- C04 vs C02: C04 owns relic/implant/installable/bonded/host-integrated/special assets. C02 owns ordinary item/gear objects. If an asset is both practical gear and special installable/relic asset, split C02 object evidence from C04 installation/relic posture.
- C04 vs C03: C04 owns the special asset record. C03 owns granted or activated capabilities. Do not embed donor power/action/effect math as C04 final mechanics.
- C04 vs C12/B06: C04 owns the asset record. C12 owns recipe/crafting/salvage/repair/upgrade/install/removal process records; B06 owns project procedure pressure.
- C04 vs C08: C04 owns special installable module/asset evidence. C08 owns vehicle/ship/platform records. Platform modules should use references, not inheritance.
- C04 vs C01: C04 owns the implant/relic/installable asset. C01 owns the actor/host/wearer/user.
- C04 vs C05/B05: C04 owns the asset. C05 owns faction/institution access and B05 owns acquisition/requisition/value-flow procedure.
- C04 vs C09: C04 owns the asset. C09 owns hazard/environment/backlash pressure.
- C04 vs C14: C14 owns source-local proper nouns, donor-world technology law, source-specific metaphysics, named artifacts, donor implant traditions, license systems, and donor-world assumptions. C04 may reference them but must not generalize them.
- C04 vs runtime/backend: C04 records conversion-stage asset evidence and routing. Runtime/backend owners decide later whether anything becomes installed state, attunement state, body-slot state, license state, module state, host integration state, save-state node, database row, or equipment runtime.
- C04 vs live-play/sourcebook: C04 is not player-facing relic prose, not implant catalog prose, not live-play installation procedure, not sourcebook item presentation, and not GM equipment execution.
- C04 vs donor source: donor essence systems, humanity systems, attunement rules, license levels, implant slots, hardpoints, upgrade sockets, cyberware economies, biotech rejection rules, and source-specific technology laws remain evidence, source-local containment, or rejected material until later doctrine/canon review.

Cross-family references do not imply inheritance. C04 must keep `inheritance_allowed: false` unless a later accepted owner explicitly changes the rule.

## 11. Composite relic/implant/installable asset record handling

Composite donor entries often bundle an object shell, a named relic, host requirements, installed module behavior, granted powers, acquisition restrictions, upgrade tracks, hazard/backlash, diagrams, source-local law, and story placement. C04 may keep a composite C04 parent only when the special asset identity remains central and the bundled elements are referenced outward.

Composite handling rules:
- split ordinary object evidence to C02 while preserving a C04 reference to the special asset posture;
- split granted abilities, active effects, passive effects, module powers, augmentation effects, and interface routines to C03;
- split host actor, wearer, implant recipient, bonded actor, symbiote host, or prosthetic user identity to C01 or C11 as appropriate;
- split crafting, salvage, recipe, repair, upgrade, installation, removal, modification, blueprint, schematic, and transformation process records to C12, with B06 only as procedure pressure;
- split faction access, license-like restrictions, manufacture, ownership, requisition, and legal authority to C05, with B05 only as value-flow/acquisition pressure;
- split platform/vehicle/ship/mech/station records to C08 and use references for platform modules rather than inheritance;
- split hazardous implants, cursed relics, unstable biotech, contamination, radiation, corruption, backlash, failure hazards, and environmental interactions to C09;
- split tables/oracles/generators to C10, diagrams/schematics/protected art to C13, and source-local names/laws/metaphysics/proper nouns to C14.

## 12. Parent, child, and satellite record handling

C04 parent records represent the main special asset. C04 child records may represent doctrine-level sub-assets only when they are independently reviewable special assets, such as a removable integrated module, separate bonded fragment, or distinct prosthetic subsystem. C04 satellite records may capture evidence packets, legal/IP notes, rejected donor elements, source-local notes, or pending-schema routing.

Parent, child, and satellite handling must preserve C00 lineage, composition, provenance, and cross-reference posture. A child record cannot inherit final mechanics, host state, slot state, attunement state, license state, module capacity, upgrade state, or donor field labels from the parent. Satellite notes cannot become canon or runtime fields.

## 13. Source-local and legal/IP handling

C04 must preserve source-local and legal/IP handling for protected names, named artifacts, named modules, named implant traditions, cyberware traditions, biotech traditions, donor-world technology law, source-specific metaphysics, proper nouns, protected art, diagrams, schematics, and source-specific license systems. Source-local material routes to C14 containment or legal/IP review and may be referenced by C04 only as evidence or boundary context.

C04 must mark legal/IP posture when donor terms resemble protected product identity, trademark-like relic names, named cyberware lines, named biotech lineages, named modules, named licenses, proprietary field labels, or diagram/art evidence. Legal/IP posture is review routing; it is not canon approval and not permission to generalize source-local law.

## 14. Rejected donor element handling

C04 uses `rejected_donor_elements` for donor systems, field names, math, rules, assumptions, and names that must not become Astra defaults. Rejected donor element handling includes donor essence systems, humanity systems, cyberpsychosis systems, attunement rules, license systems, slot systems, hardpoint systems, socket systems, upgrade-slot systems, installation procedures, surgery procedures, crafting costs, repair values, implant economies, cyberware economies, biotech economies, named artifacts/modules, donor implant traditions, technology laws, donor field labels, donor costs, and donor resource math.

A rejected donor element may still carry source evidence and legal/IP review notes. Rejection means it cannot become Astra schema, canon, accepted lexicon, sourcebook prose, runtime state, or final mechanics without later doctrine/canon review.

## 15. Canon eligibility and review routing

C04 may set canon eligibility routing signals inherited from C00, but C04 does not grant canon acceptance, canon promotion, accepted lexicon status, final mechanics, runtime readiness, or sourcebook approval. C04 canon eligibility asks whether the special asset evidence is clear enough for later review, whether source-local/legal/IP containment is adequate, whether rejected donor elements are documented, and whether cross-family references are routed.

C04 records that contain protected proper nouns, donor-world technology law, source-specific metaphysics, donor license systems, named artifacts, named modules, or donor implant/cyberware traditions must route to C14 and legal/IP review before any canon decision. Records with low provenance, hidden truths, or unresolved owner gaps route to human review, quarantine, or pending_schema.

## 16. Confidence, validation, and escalation routing

C04 confidence and validation posture must distinguish extraction confidence, boundary confidence, conversion confidence, legal/IP confidence, source-local confidence, and cross-family routing confidence. Escalate when:
- an asset may be ordinary gear rather than a special asset;
- an asset may be a granted ability, process/recipe, platform record, hazard, companion/summon relation, diagram, or source-local setting law rather than C04;
- donor field names or donor math are needed to understand the record but cannot be safely normalized;
- host/interface, installation/bonding, integration depth, acquisition, crafting/upgrade, hazard/backlash, or vehicle/platform pressure is unclear;
- legal/IP or protected proper-noun risk is present;
- hidden-state or protected-truth evidence would leak spoilers or GM-only truth;
- no stable C-family owner exists and pending_schema may be required.

## 17. Hidden-state and protected-truth boundary

C04 may identify hidden/protected-truth posture for cursed relics, disguised implants, secret symbiotes, hidden modules, concealed prosthetics, dormant bonded assets, false license claims, unknown host integration, spoiler-sensitive origin, protected art/diagram evidence, or GM-only asset truth. This posture is evidence routing only.

C04 must not expose hidden truth as runtime state, player-facing sourcebook prose, live-play reveal procedure, command lifecycle, context packet content, database visibility flag, or canon fact. Hidden-state and protected-truth records route through C00 review fields, C09 hazard review where applicable, C14 source-local containment where applicable, and human/legal review where required.

## 18. Runtime boundary

C04 forbids runtime installation state, runtime body-slot state, runtime attunement state, runtime license state, runtime module state, runtime host-integration state, runtime actor state, runtime item state, equipment runtime, save-state nodes, database asset rows, entity/component/event schemas, command lifecycle, context packets, backend equipment schemas, backend implant schemas, backend cyberware schemas, backend attunement schemas, backend license schemas, persistence models, combat trackers, live-play installation procedure, and runtime removal/surgery/repair/upgrade procedures.

Runtime/backend owners decide later whether any C04 evidence becomes installed state, body-slot state, attunement state, license state, module state, host integration state, equipment runtime, save-state node, database row, entity/component/event schema, command lifecycle element, context packet, backend equipment schema, or backend implant schema. C04 supplies conversion-stage asset evidence and routing only.

## 19. Canon/sourcebook/live-play/training boundary

C04 is not player-facing relic prose, not implant catalog prose, not sourcebook item presentation, not sourcebook relic prose, not sourcebook implant prose, not live-play installation procedure, not live-play surgery procedure, not GM equipment execution, not accepted lexicon, not canon acceptance, not canon promotion, and not training example authority.

Training or example records may demonstrate safe routing only. They cannot promote donor relic systems, implant systems, cyberware systems, biotech systems, attunement rules, essence systems, humanity/cyberpsychosis systems, license systems, slot/hardpoint/socket systems, upgrade mechanics, installation procedures, surgery rules, donor costs, resource math, field labels, proper nouns, named artifacts/modules/implant traditions/technology laws, or donor-world assumptions into Astra doctrine.

## 20. Missing-schema fallback

When C04 encounters special asset evidence that no stable C-family owner can safely hold, it must route to `pending_schema`, quarantine, escalation, or human review rather than inventing fields. Missing-schema fallback is especially important for ambiguous living artifacts, AI-bound implants, soul-bound modules, vehicle-scale organs, companion-integrated symbiotes, legal license ledgers, unknown socket systems, donor-specific hardpoints, or source-local technology laws that blend multiple families.

`pending_schema` is a routing posture, not a permanent owner and not permission to create runtime/backend/database/live-play fields.

## 21. Examples of good and bad C04 usage

Good C04 usage:
- A donor cybernetic eye is recorded as an implant-like special asset with C01 host references, C03 capability references for vision effects, C02 object-shell evidence, C12 installation/removal process references, B06 installation pressure note, and rejected donor field labels for essence/humanity costs.
- A cursed relic sword is split into C02 sword object evidence, C04 relic/bonding posture, C03 granted power references, C09 curse/backlash hazard references, C07 story-role references, and C14 protected proper-noun containment.
- A mech-mounted experimental module is a C04 platform-module-like asset with C08 platform references, C03 interface routine references, C09 failure hazard references, and no inherited hardpoint, socket count, license level, or module capacity.
- A biotech symbiote is a C04 symbiote-like asset with C01 or C11 host references, C09 contamination/rejection pressure, C12 grafting/removal process references, and donor biotech rejection chance rejected as donor math.

Bad C04 usage:
- Copying Shadowrun essence costs into an Astra `essence_cost` field.
- Copying Cyberpunk humanity loss or cyberpsychosis thresholds into an Astra implant balance table.
- Treating D&D attunement limits or Lancer license levels as Astra defaults.
- Embedding body slots, hardpoints, sockets, upgrade slots, module capacity, installation DCs, surgery costs, damage values, cooldowns, charges, or resource math in the C04 record.
- Making a C04 record into sourcebook implant prose, player-facing relic catalog prose, live-play installation procedure, equipment runtime, database asset row, or backend implant schema.
- Generalizing donor proper nouns, named artifacts, named modules, named implant traditions, or donor-world technology laws as Astra canon.

## 22. Minimum tests or assertions

Minimum C04 tests should assert that:
- the C04 file exists at `docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md`;
- all required sections are present;
- C04 declares ownership and non-ownership boundaries;
- C04 must inherit/include `AstraContentRecordBase` and preserve C00 provenance, source-local, rejected donor element, canon eligibility, confidence, validation, lineage, composition, cross-reference, legal/IP, and review routing posture;
- C04 record grammar is doctrine grammar only and not a runtime schema, not a database schema, not a final relic statblock, not an implant system, not a cyberware system, not an attunement system, not a license system, not an upgrade-slot system, not an installation-state schema, and not sourcebook item prose;
- donor relic/implant/cyberware/biotech/attunement/license/essence/humanity/cyberpsychosis/slot/hardpoint/socket/upgrade/install/surgery/cost/resource/field-name/proper-noun leakage is rejected as Astra default;
- B03, B04, B05, B06, and relevant B02 handoffs are present without converting Batch B procedure into schema fields;
- C01, C02, C03, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14, and pending_schema handoffs are present;
- source-local/legal/IP handling, rejected donor elements, canon eligibility without promotion, hidden/protected-truth boundary, runtime boundary, and good/bad examples are present;
- registry C04 posture is draft/schema-draft/designed/not_reviewed without current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum promotion.

## 23. Acceptance criteria

C04 is acceptable when:
- C04 exists at the exact registry path;
- C04 remains conversion-stage/canon-review schema doctrine only;
- C04 includes C00 base inheritance requirements;
- C04 does not import donor relic systems, implant systems, cyberware systems, biotech systems, attunement rules, essence systems, humanity/cyberpsychosis systems, license systems, slot/hardpoint/socket systems, upgrade mechanics, installation procedures, surgery rules, donor costs, resource math, field labels, proper nouns, named artifacts/modules/implant traditions/technology laws, or donor-world assumptions as Astra schema;
- C04 does not define final relic mechanics, implant math, cyberware economy, attunement rules, license rules, runtime installation/body-slot/attunement/license/module/host-integration state, database schema, live-play installation procedure, canon, sourcebook item prose, or accepted lexicon;
- C04 has clear Batch B handoffs and cross-family handoffs;
- C04 includes source-local/legal/IP and rejected-import handling;
- C04 registry posture is updated to draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03/C05/C06/C07/C09/C10/C13/C14 registry posture is preserved;
- C08, C11, and C12 are not promoted;
- focused tests pass and the full suite passes.

## 24. Follow-up handoff to C08

C04 leaves a focused follow-up handoff to C08 for vehicle/ship/platform modules, ship systems, mech modules, station modules, hardpoint-like assets, platform-integrated systems, onboard assets, vehicle-scale installable assets, and other platform-scale records. Until C08 is drafted, C04 may record special installable asset evidence and C08 references, but it must not define vehicle/ship/platform records, hardpoint mechanics, module capacity, runtime platform state, backend platform schemas, or platform inheritance.
