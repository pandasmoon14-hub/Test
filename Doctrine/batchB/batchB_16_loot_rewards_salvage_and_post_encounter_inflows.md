# batchB_16_loot_rewards_salvage_and_post_encounter_inflows.md

## Purpose

This file defines Astra Ascension doctrine for **post-pressure outputs, extraction, disposition, and carry-forward states**.

Its role is to provide Astra with a conversion-stable framework for what becomes newly obtainable, usable, claimable, extractable, reportable, or actionable after pressure resolves, changes state, or is abandoned.

B16 is not a “treasure chapter.”
It is not limited to post-combat loot.
It is not restricted to material drops.

In Astra terms, this file governs how resolved or transformed pressure can generate:
- material inflows,
- informational inflows,
- entity-bearing inflows,
- standing and access outputs,
- progression outputs,
- fallout outputs,
- claim states,
- custody states,
- salvage and harvest opportunities,
- and mixed or contested output states.

This file exists because a large donor corpus will not consistently treat post-encounter output as “defeat enemy, gain coins and items.”
Some donors reward patronage, favor, access rights, reserves, formulas, blessings, licenses, or social standing.
Some donors center harvesting, stripping, salvage rights, and carcass processing.
Some donors enable information extraction through interrogation, corpse questioning, magical probing, sensor capture, or seized records.
Some donors end encounters in surrender, retreat, rescue, claim validation, or partial extraction rather than clean victory.

B16 therefore defines Astra’s doctrine for **what new exploitable states exist after pressure changes state, and how those states are extracted, classified, contested, processed, and carried forward**.

## Authority and scope

This file is authoritative for:
- post-pressure output doctrine;
- source-state doctrine for post-pressure outputs;
- extraction and disposition doctrine;
- inflow-family doctrine;
- loot versus salvage versus harvest versus claim versus capture doctrine;
- information-bearing and entity-bearing output classification;
- standing, access, progression, and fallout output doctrine;
- legality, legitimacy, ownership, and contest-state doctrine for outputs;
- condition, perishability, contamination, and processing-window doctrine for outputs;
- carry-forward-state doctrine for recovered, extracted, secured, claimed, or unresolved outputs;
- non-victory and mixed-outcome output doctrine;
- lawful incomplete mapping for post-pressure outputs;
- and handoff boundaries to adjacent files.

This file is **not** authoritative for:
- item ontology, item profiles, or item-instance object modeling, which belong to `batchB_03_equipment_item_and_gear_object_model.md`;
- wealth, currency, market value, trade law, requisition law, or valuation semantics, which belong to `batchB_04_wealth_currency_requisition_trade_and_value_framework.md`;
- crafting, repair, modification, installation, processing, or transformation procedure, which belong to `batchB_05_crafting_salvage_repair_modification_and_installation.md`;
- truth verification, information interpretation, certainty, contradiction, and clue meaning, which belong to `batchB_09_investigation_research_discovery_clues_and_information_procedure.md`;
- social pressure, bargaining, confession pressure, negotiation, reputation, or standing change procedure, which belong to `batchB_10_social_conflict_influence_reputation_and_negotiation.md`;
- downtime scheduling, project cadence, and service-use timing, which belong to `batchB_11_downtime_rest_training_projects_and_services.md`;
- organizational permission, clearance, custody law, sanction, or institutional service access, which belong to `batchB_12_factions_institutions_clearance_and_service_access.md`;
- auxiliary-entity doctrine, which belongs to `batchB_13_companions_retinues_summons_drones_and_auxiliary_entities.md`;
- platform and vehicle operation doctrine, which belongs to `batchB_14_mounts_vehicles_mechs_ships_and_platform_operations.md`;
- settlement and infrastructure doctrine, which belongs to `batchB_15_settlements_bases_capitals_and_infrastructure_operations.md`;
- or scenario/adventure-path reward scripting, which is reserved for Batch C.

## Core design stance

Astra must support donor material where post-pressure outputs are generated through:
- killing or disabling an adversary,
- forcing surrender,
- capturing a target alive,
- securing a corpse for later questioning,
- stripping a wreck or damaged frame,
- harvesting flora, fauna, occult remains, or body-like residue,
- claiming legal or procedural rights,
- reporting success to a patron or authority,
- looting a cache, convoy, lair, vault, or site,
- acquiring faction favor or official authorization,
- earning blessings, reserves, licenses, formulas, or soul-state rewards,
- extracting intelligence from a witness, prisoner, log, spirit, or memory source,
- rescuing a person or asset,
- or surviving with leverage despite failing to secure conventional treasure.

Astra must therefore treat post-pressure output as a doctrine of **newly actionable state**, not merely of treasure parcels.

A source state is not the same thing as an inflow.
An extraction method is not the same thing as an output class.
An output class is not the same thing as a verified, processed, lawful, marketable, or safely usable reward.

B16 must remain open-ended enough to absorb:
- donor books that add hundreds of items,
- donor books centered on monster harvesting,
- donor books centered on patron rewards or rep,
- donor books centered on access rights and permits,
- donor books centered on magical or psychic information extraction,
- donor books centered on battlefield salvage,
- donor books centered on capture and ransom,
- and donor books where post-pressure fallout matters as much as reward.

B16 must not collapse into “coins and magic items.”
It must also not become a megafile that absorbs verification law, item law, economic law, or institutional permission law.

## Core doctrine terms

### Post-pressure output
A **post-pressure output** is any newly actionable state, resource, right, entity, opportunity, or liability that becomes available because pressure resolved, changed state, or was abandoned.

### Source state
A **source state** is the thing left behind, secured, transformed, preserved, surrendered, or exposed after pressure changes state.

### Extraction
**Extraction** is the act of converting a source state into one or more usable, processed, reportable, secured, or otherwise actionable outputs.

### Disposition
**Disposition** is what is done with a source state or output after extraction or classification: keep, secure, process, exhibit, report, ransom, destroy, defer, surrender to authority, claim, sell, convert, or deny.

### Inflow
An **inflow** is any resource-bearing, information-bearing, entity-bearing, access-bearing, progression-bearing, or fallout-bearing output that enters the actors’ post-pressure state.

### Loot
**Loot** is already-usable, already-possessed, or directly recoverable value taken from a source state without requiring the source to be primarily transformed first.

### Salvage
**Salvage** is recoverable value obtained by stripping, dismantling, reclaiming, repurposing, or otherwise extracting utility from constructed, damaged, or nonorganic sources.

### Harvest
**Harvest** is extraction from organic, body-like, occult, natural, or otherwise harvestable sources whose usable value depends on the source’s type, condition, and processing.

### Claim
A **claim** is a legal, procedural, territorial, contractual, ceremonial, or recognized right over an object, site, bounty, route, permit, body, spoil, or output stream.

### Capture
**Capture** is the retention, custody, or control of a living, active, autonomous, or information-bearing entity or system.

### Carry-forward state
A **carry-forward state** is the ongoing condition created by a post-pressure output after immediate resolution, such as “prisoner secured,” “salvage rights held,” “corpse available for questioning,” or “site partially stripped.”

### Contest state
A **contest state** is any unresolved dispute regarding ownership, custody, legitimacy, division, processing right, or lawful use of an output.

## Core post-pressure output principles

1. **Post-pressure outputs are broader than treasure.**
   Material goods are only one output family among many.

2. **Source state, extraction method, and resulting inflow must stay distinct.**
   A corpse is not automatically loot.
   A surrender is not automatically a captive.
   A disabled mech is not automatically salvage.
   A seized archive is not automatically verified truth.

3. **Outputs may be positive, mixed, contested, temporary, unstable, or harmful.**
   The fact that something was gained does not mean it is immediately beneficial, lawful, safe, stable, or uncontested.

4. **Not all outputs require victory.**
   Retreat, concession, escape, negotiated withdrawal, survival, partial success, and failed extraction can still generate lawful outputs.

5. **Output classification must preserve donor pressure.**
   Systems that emphasize harvesting, rep, permits, blessings, reserves, trophies, bodies, access rights, or fallout must not be flattened into generic treasure.

6. **Processing, verification, and conversion often happen after initial recovery.**
   Immediate pickup is only one form of post-pressure acquisition.

7. **B16 must preserve carry-forward state.**
   Post-pressure outputs matter because they change what is possible next, not merely because they increment a value pool.

## Source-state doctrine

Astra classifies post-pressure source states by what kind of thing now exists after pressure resolves.

### Source-state classes

#### Body or corpse source
A dead body, remains, carcass, severed component, or still-present body-like source that may support looting, harvesting, questioning, ritual use, authentication, trophy extraction, or evidence handling.

#### Living captive source
A living but secured target, prisoner, witness, rescued individual, recruit prospect, surrendering foe, or bound being whose value may be informational, social, legal, economic, or strategic.

#### Surrendered force source
A still-active but no-longer-fighting force, group, or organized body whose post-pressure outputs may include prisoners, negotiated terms, equipment handover, standing shifts, or access changes.

#### Abandoned site or cache source
A lair, camp, vault, bunker, wreck site, stash, convoy remnant, ritual site, or hideout whose contents, records, claims, permissions, or hazards remain after primary opposition has dispersed or been neutralized.

#### Disabled frame or platform source
A vehicle, mech, ship, mount-frame, machine, or platform that has been disabled, stranded, captured, boarded, or rendered inoperative without necessarily being destroyed or lawfully claimable.

#### Damaged item cluster source
A debris field, broken gear set, cargo spill, armory remnant, munitions stock, or other collection of damaged or partial objects that may yield salvage, contamination, or delayed processing opportunities.

#### Environmental residue source
A lingering state left in the environment, such as spoor, spoor-like aura traces, residue, contamination, blood trail, magical imprint, chemical seep, psychic echo, or radiation pocket that can itself be exploited or processed.

#### Legal or administrative claim source
A bounty, permit, writ, sanction, title claim, declaration of salvage, official notice, proof of kill, reportable event, or captured credential whose value lies in lawful recognition rather than material recovery.

#### Social or public aftermath source
A reputation shift, witness network, crowd reaction, scandal opportunity, public narrative, propaganda value, or rescue visibility that becomes actionable after the event.

#### Ritual or anomalous residue source
A blessing site, lingering ward, opened gate, spirit remnant, corrupted heart, living relic, tokenized trial state, or singular residue whose value may be metaphysical, access-bearing, unstable, or progression-linked.

### Source-state doctrine rules

- A single resolved pressure state may create multiple source states.
- Source states may overlap, but they must still be classified separately.
- A source state is not identical to its downstream value.
- Source states can be lawful, unlawful, contested, decaying, hazardous, or latent.
- Some source states exist only briefly unless stabilized, secured, or processed.

## Extraction and disposition doctrine

Astra distinguishes what is **present** from what is **done** with it.

### Extraction families

#### Looting
Immediate recovery of already-usable or directly portable goods.

#### Stripping
Removal of useful components, fittings, modules, or valuables from a constructed or damaged source.

#### Harvesting
Selective recovery from organic, natural, occult, or body-like sources.

#### Questioning
Attempting to obtain information from a living source through speech, pressure, leverage, or conversation.

#### Probing
Attempting to obtain information from a source through magical, psychic, forensic, technical, spiritual, or otherwise nonordinary means.

#### Claiming
Asserting recognized right over a source, site, body, bounty, wreck, route, or reward channel.

#### Securing
Stabilizing possession, quarantine, custody, control, or scene preservation without necessarily using the output yet.

#### Documenting
Recording proof, testimony, evidence, sensor logs, chain of custody, maps, reports, witness records, or legal compliance data.

#### Consecrating or purifying
Ritually or procedurally cleansing, sanctifying, stabilizing, neutralizing, or legitimizing a source or output.

#### Processing or refining
Converting a raw source state into a usable, stable, saleable, craftable, edible, or otherwise actionable form.

#### Ransoming
Converting custody over a living or claimable source into exchange, favor, or negotiated outcome.

#### Transferring custody
Turning the source or output over to an institution, patron, sponsor, authority, buyer, faction, or mediator.

#### Reporting
Submitting proof or claim through the required channel to trigger payment, authorization, standing change, or legal validation.

#### Exhibiting
Displaying trophies, bodies, proof, seized objects, or claims for prestige, legitimacy, fear, memorialization, or civic effect.

#### Converting into civic or organizational use
Turning a source or output into settlement benefit, faction benefit, institutional resource, training input, defensive asset, or public utility.

#### Denial or destruction
Destroying, contaminating, hiding, dispersing, sabotaging, or otherwise preventing others from exploiting the source state.

#### Deferred extraction
Leaving a source state intact but marked, tracked, contained, or reserved for later recovery.

### Disposition doctrine rules

- Extraction method and disposition method may be the same or different.
- The best immediate disposition is not always immediate pickup.
- Some outputs exist only because the actors chose to secure, defer, report, or transfer rather than consume, sell, or destroy.
- Disposition can itself create new carry-forward states, obligations, or contest states.

## Inflow-family doctrine

Astra recognizes several major inflow families.
A single resolved pressure state may generate more than one family at once.

### Material inflows
Physical goods, valuables, components, modules, gear, stores, consumables, cargo, trophies, residue, or resources.

### Informational inflows
Testimony, memories, logs, records, codes, names, maps, route data, research leads, tactical intelligence, blackmail vectors, or doctrinal/ritual knowledge.

### Entity-bearing inflows
Prisoners, rescued persons, recruits, defectors, surrendered foes, bound spirits, liberated auxiliaries, temporary aides, or retained witnesses.

### Standing and access inflows
Rep, favor, permits, introductions, rights of passage, bounty credit, sanctioned claim rights, invitations, licenses, or faction-mediated openings.

### Progression inflows
Essence-like growth resources, blessings, reserves, licenses, soul-state rewards, advancement tokens, doctrinal unlocks, training rights, or other personal or group growth vectors.

### Fallout inflows
Heat, scrutiny, legal exposure, retaliation, curse carryover, contamination, debt, claim dispute, public scandal, hostile attention, or destabilized relations.

## Loot versus salvage versus harvest versus claim versus capture

### Loot
Loot is the direct recovery of already-usable, already-possessed, or immediately transferable value.

### Salvage
Salvage is value recovered through stripping, dismantling, reclaiming, or repurposing something not already in a directly usable reward state.

### Harvest
Harvest is extraction from a body-like, natural, organic, occult, or similarly harvestable source.

### Claim
Claim is not a physical good by default.
It is the recognized right to custody, use, report, possess, redeem, access, exhibit, dismantle, or legally convert a source or output.

### Capture
Capture is the maintained control of an entity, witness, prisoner, recruit prospect, auxiliary, or other active information-bearing or negotiation-bearing source.

### Anti-collapse rule
These five classes must not be merged casually.
A donor system may overlap them, but Astra must still classify which class is primary in each case.

## Information-bearing outputs and truth-status handoff

B16 classifies informational outputs.
It does **not** determine their final truth status.

### Information-bearing source examples
- corpse available for questioning;
- prisoner available for interrogation or bargaining;
- witness secured;
- document cache recovered;
- sensor log captured;
- route key obtained;
- memory source accessed;
- proof collected;
- operational plans seized;
- rumor vector opened.

### Information-bearing output classes
- raw information;
- contested testimony;
- partial memory extraction;
- scene proof;
- chain-of-custody evidence;
- tactical intelligence;
- access-relevant information;
- lead-bearing output;
- falsifiable record;
- or socially mediated allegation.

### Handoff rule
- B16 classifies the source and output.
- `batchB_09_investigation_research_discovery_clues_and_information_procedure.md` owns verification, corroboration, contradiction, interpretation, and truth-status handling.
- `batchB_10_social_conflict_influence_reputation_and_negotiation.md` owns interrogation pressure, bargaining for information, and confession-related social leverage.
- `batchB_12_factions_institutions_clearance_and_service_access.md` owns institutional validity, reporting channels, and permission consequences.

## Entity-bearing outputs and custody states

Some post-pressure outputs are still living, active, autonomous, or legally significant entities.

### Entity-bearing output examples
- prisoner secured;
- surrendered force disarmed but intact;
- rescued civilian or specialist;
- recruit or defector;
- bound or contained spirit;
- living witness under protection;
- auxiliary entity recovered;
- hostile but stabilizable target;
- transferred detainee;
- or escort-bound surrender.

### Custody-state classes
- unsecured;
- secured;
- restrained;
- escorted;
- transferred;
- contested;
- ransomed;
- sanctuary-protected;
- legally held;
- illegally held;
- or unstable and escape-prone.

### Entity-bearing doctrine rules
- Capture is not identical to loyalty.
- Custody is not identical to lawful ownership.
- Rescue is not identical to alliance.
- Surrender is not identical to obedience.
- An entity-bearing output may carry social, legal, informational, or access value even when it has no market value.

## Standing, access, progression, and fallout outputs

### Standing outputs
Standing outputs include rep shifts, faction favor, debt, prestige, rescuer status, public credit, political leverage, or social capital earned through post-pressure resolution.

### Access outputs
Access outputs include permits, safe passage, audience rights, trial entry, route keys, sponsorship, facility use rights, claim validation, legal retrieval rights, or protected custody channels.

### Progression outputs
Progression outputs include blessings, essence-like growth resources, reserves, doctrinal unlocks, advancement tokens, trial marks, soul-state gains, or training rights.

### Fallout outputs
Fallout outputs include heat, legal attention, retaliation, tracking, curse carryover, contamination burden, disputed claim, bounty challenge, scrutiny, blacklisting risk, or new obligation.

### Doctrine rule
B16 must preserve the possibility that one resolved pressure state produces both reward outputs and fallout outputs at the same time.

## Legality, legitimacy, ownership, and contest states

Not every output can be freely kept, sold, used, redeemed, or processed.

### Legality and legitimacy classes
- personal and freely usable;
- personal but nontransferable;
- faction-claimed;
- sponsor-owned;
- treaty-protected;
- site-bound;
- evidence-bearing;
- bounty-valid only if reported;
- lawful to possess but unlawful to use;
- unlawful but valuable;
- emergency-use only;
- or legitimacy-dependent pending review.

### Ownership and contest classes
- undisputed possession;
- disputed ownership;
- shared claim;
- sponsor priority;
- institutional seizure;
- neutral-ground custody;
- escort or patron entitlement;
- pending adjudication;
- public claim pending proof;
- or no recognized lawful owner.

### Doctrine rule
B16 classifies the legal and contest state of the output.
B04 owns value law and exchange consequences.
B12 owns institutional recognition, sanction, reporting channels, and service-access consequences.

## Condition, perishability, contamination, and processing windows

Post-pressure outputs are not always stable.

### Condition classes
- pristine;
- intact but unstable;
- damaged;
- degraded;
- partially extracted;
- contaminated;
- cursed or tainted;
- irradiated or hazardous;
- spiritually volatile;
- expired or spoiled;
- or inert but recoverable.

### Processing-window classes
- immediate use;
- short-window extraction;
- preservation required;
- refinement required;
- quarantine required;
- delayed-safe use;
- perishable with decay;
- or dormant until unlocked.

### Doctrine rules
- Condition must not be assumed from source type alone.
- Perishability and contamination can change output class.
- A valuable output may become worthless, dangerous, or illegal if mishandled.
- Some outputs are only actionable after preservation or processing.
- Some outputs attract pressure simply by being held.

## Carry-forward-state doctrine

The primary job of B16 is not only to state what was gained, but to state what new ongoing condition now exists.

### Carry-forward-state examples
- corpse secured for interrogation;
- prisoner secured;
- witness under protection;
- salvage rights held;
- frame recoverable later;
- cache marked for later extraction;
- trophy available for exhibition;
- blessing gained and slotted;
- proof obtained but not yet authenticated;
- route key obtained;
- bounty claim pending;
- site partially stripped;
- contaminated material quarantined;
- access right acquired but unredeemed;
- aid pledged;
- faction debt created;
- rival claim triggered;
- or public scrutiny increased.

### Carry-forward-state rules
- Every major output should be expressible as an ongoing state, not only as a one-time payout.
- Carry-forward states may persist, decay, expire, transfer, or escalate.
- Carry-forward states are the main bridge from B16 into future scenes, downtime, social pressure, access law, projects, and settlement use.

## Non-victory and mixed-outcome outputs

Astra must support lawful outputs from:
- retreat;
- concession;
- negotiated withdrawal;
- failed extraction;
- partial success;
- rescue without conquest;
- escape with proof but no goods;
- survival with heat or claim rights but no immediate treasure;
- surrender that yields prisoners but not loot;
- or defeat that still leaves leverage, witness testimony, or route knowledge.

### Doctrine rule
Post-pressure output is not limited to clean victory states.
If a donor construct yields useful, dangerous, or contested aftermath despite failure or withdrawal, Astra must preserve that output family.

## Multi-party and contested inflow states

Astra must support post-pressure outputs that are:
- party-shared;
- sponsor-claimed;
- crew-level;
- faction-mediated;
- patron-reported;
- rival-contested;
- neutral-ground held;
- legally seized;
- split by treaty or contract;
- or unresolved pending hearing, review, or proof.

### Doctrine rule
B16 must never assume that immediate possession equals final ownership.

## Anti-collapse invariants

### Preserve donor post-pressure pressure
Do not normalize harvesting-heavy, claim-heavy, rep-heavy, patron-heavy, reserve-heavy, or fallout-heavy donor structures into generic treasure bundles.

### Preserve source-state specificity
Do not skip directly from “pressure ended” to “reward granted” when the donor clearly distinguishes corpse, captive, surrender, wreck, residue, site, proof, or claim source states.

### Preserve extraction burden
Do not treat all outputs as immediate pickup when the donor emphasizes stripping, reporting, questioning, processing, refining, exhibiting, preserving, or converting.

### Preserve mixed value
Do not assume all outputs are purely beneficial, purely material, or purely lawful.

### No false certainty
If the donor clearly implies a source, output, or claim state but does not specify the exact classification, Astra must use lawful incomplete mapping rather than decorative invention.

## Lawful incomplete mapping

When donor material clearly implies post-pressure output structure but does not fully specify it, Astra may classify the construct as:
- **directly mapped**;
- **normalized**;
- **source-class assigned**;
- **output-family assigned**;
- **contest-state assigned**;
- **placeholder classified**;
- or **quarantined pending later doctrine**.

### Use cases for incomplete mapping
- a donor implies bounty law but not the reporting channel;
- a donor implies a valuable corpse but not the exact harvest table;
- a donor implies political favor without explicit mechanics;
- a donor implies a site can be claimed but not whether the claim is legal, customary, or factional;
- a donor implies a relic is recoverable but also dangerous to transport;
- or a donor implies a captured target is useful without specifying whether the value is social, informational, or legal.

## Watch note: possible future split

B16 is one of the most likely Batch B files to grow into a megafile.
If future donor pressure becomes too wide, reserve the possibility of splitting this doctrine into:
- `batchB_16a_material_extraction_salvage_and_claims.md`
- `batchB_16b_rewards_rep_blessings_and_fallout.md`

Do not split immediately.
Only split if the file begins to absorb too much implementation detail or if post-pressure material versus post-pressure standing/fallout become too difficult to maintain in one doctrine layer.

## Mandatory subsystem handoff map

- `batchB_03_equipment_item_and_gear_object_model.md` owns item ontology, item profiles, and item-instance object structure.
- `batchB_04_wealth_currency_requisition_trade_and_value_framework.md` owns valuation, marketability, requisition, and exchange semantics.
- `batchB_05_crafting_salvage_repair_modification_and_installation.md` owns processing, refinement, repair, salvage transformation, and installation procedures.
- `batchB_09_investigation_research_discovery_clues_and_information_procedure.md` owns information verification, interpretation, lead conversion, certainty, contradiction, and falsifiability.
- `batchB_10_social_conflict_influence_reputation_and_negotiation.md` owns bargaining, confession pressure, social extraction, reputation procedure, and standing-change procedure.
- `batchB_11_downtime_rest_training_projects_and_services.md` owns delayed extraction timing, reporting projects, service scheduling, and long-form non-encounter conversion of held outputs.
- `batchB_12_factions_institutions_clearance_and_service_access.md` owns reporting channels, sanction, custody law, claim recognition, permit redemption, and institutional access consequences.
- `batchB_13_companions_retinues_summons_drones_and_auxiliary_entities.md` owns recovered, bound, rescued, or recruited auxiliary entities as entity doctrine rather than reward doctrine.
- `batchB_14_mounts_vehicles_mechs_ships_and_platform_operations.md` owns disabled-frame operational consequences, recovered platform doctrine, and transport/platform state.
- `batchB_15_settlements_bases_capitals_and_infrastructure_operations.md` owns site-scale outputs when trophies, claims, caches, or recovered materials are converted into civic or infrastructure benefit.

## Final doctrine stance

B16 must be treated as Astra’s doctrine for **post-pressure outputs, extraction, and disposition**.

It is the file that explains:
- what can exist after pressure changes state;
- what can be extracted from that state;
- what form the resulting inflow takes;
- what contest, legality, contamination, perishability, and processing burdens remain;
- and what ongoing carry-forward state now exists because of that output.

If B16 is underdesigned, a large donor corpus will collapse into “defeat target, gain money and item.”
If B16 is designed correctly, Astra gains a lawful home for:
- loot,
- salvage,
- harvest,
- capture,
- claim,
- rep,
- blessings,
- reserves,
- patron rewards,
- site rights,
- corpse questioning,
- magical memory extraction,
- trophies,
- contested ownership,
- partial and non-victory outputs,
- and the many mixed aftermath states that donor systems and actual play generate.
