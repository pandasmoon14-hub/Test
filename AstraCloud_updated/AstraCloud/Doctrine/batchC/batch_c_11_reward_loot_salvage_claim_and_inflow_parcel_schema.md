# batchC_11_reward_loot_salvage_claim_and_inflow_parcel_schema.md

## Purpose and authority

This file defines the **post-pressure inflow parcel schema** for Astra Ascension.

Its job is to define how Astra represents **packaged outputs that become available, transferred, granted, claimed, recognized, extracted, awarded, unlocked, or conferred** after pressure, resolution, completion, failure, survival, discovery, adjudication, salvage, extraction, recognition, or structured progression.

This file is doctrine for **parcel-shaped inflow outputs in content-schema form**.
It does **not** define the full doctrine for value.
It does **not** define the full doctrine for legality.
It does **not** define the full doctrine for post-pressure inflow as a system.
It does **not** define the underlying item, frame, site, faction, or mission entries that a parcel may reference.

C11 exists because a large donor corpus does not produce one reward family.
It produces money, salvage, claims, rights, titles, favors, access, licenses, blessings, legal recognitions, faction payments, support packages, future-delivery promises, and mixed inflow bundles that cannot safely be collapsed into “loot” without structural loss.

C11 therefore owns the schema grammar for:
- packaged inflow outputs
- source-state family reflection at parcel scale
- parcel vs payload distinction
- direct possession vs claim vs entitlement distinction
- delivery-state grammar
- realization-state grammar
- transferability grammar
- divisibility and allocation grammar
- burden-bearing inflow grammar
- mixed inflow parcel grammar
- authored, normalized, generated, and instantiated parcel distinctions

C11 remains **schema doctrine**, not converted output, not canon, not a treasure chapter, and not a market-value or legality rules chapter.

## Relationship to Batch C authority

This file inherits:
- `batchC_00_manifest.md`
- `batchC_01_common_content_schema_conventions_and_record_grammar.md`

This file must remain consistent with the established Batch C family boundaries for:
- `batchC_04_item_relic_resource_and_asset_content_schema.md`
- `batchC_05_mount_vehicle_mech_ship_and_platform_entry_schema.md`
- `batchC_06_site_region_settlement_and_locale_schema.md`
- `batchC_07_faction_institution_polity_and_social_body_schema.md`
- `batchC_10_mission_scenario_arc_and_adventure_path_conversion_schema.md`
- `batchC_12_random_tables_events_oracles_and_generator_schema.md`
- `batchC_13_sourcebook_bundle_gazetteer_and_reference_container_schema.md`

This file must also remain subordinate to Batch B doctrine, especially:
- post-pressure inflow doctrine
- value and exchange doctrine
- access, legality, recognition, and authorization doctrine
- crafting, salvage processing, repair, and transformation doctrine

C11 must consume those doctrines through schema hooks rather than restating them as if C11 owned them.

## Why C11 must exist

A parcel-scale inflow schema is mandatory for corpus-scale conversion.

Astra must be able to represent donor outputs such as:
- treasure bundles
- direct payments
- salvage bundles
- extraction rights
- legal claims
- contested claims
- faction reputation outputs
- public honors and titles
- service or maintenance privileges
- requisition rights
- docking, travel, or access clearance
- blessing or boon grants
- sponsorship packages
- deferred compensation
- contingent payouts
- recurring stipends
- mixed mission payouts combining money, salvage, recognition, and access
- burdensome or double-edged rewards that carry obligations or exposure

These are not interchangeable.
A bag of coin is not the same as a salvage claim.
A salvage claim is not the same as direct possession of recovered assets.
Direct possession is not the same as legal recognition.
Legal recognition is not the same as faction standing.
Faction standing is not the same as a title grant.
A title grant is not the same as an access authorization.
A maintenance privilege is not the same as a service-support package.

Without C11, later conversion work will tend to fail in one of seven ways:
1. treat all inflows as item entries
2. treat all inflows as economic value lines
3. treat mission-success notes as if they already define parcel structure
4. treat legal or social recognition as if it were direct possession
5. collapse mixed inflows into one vague reward line
6. offload reward-shape logic into generator tables, mission entries, or faction files
7. confuse source-state, parcel identity, payload identity, and realization state

C11 exists to stop those failures.

## Core doctrinal center

The doctrinal center of C11 is:

**C11 owns the schema by which Astra represents packaged inflow outcomes after pressure.**

In Astra terms, C11 owns the structure of:
- what kind of parcel this is
- what kind of source-state produced it
- what it delivers, references, confers, recognizes, unlocks, or claims
- when it becomes available
- under what conditions it becomes available
- to whom it applies
- who may hold, administer, certify, dispute, or escrow it
- in what divisibility or transfer form it exists
- what restrictions, visibility states, burden states, or claim states attend it
- how it may be distributed, deferred, split, realized, blocked, processed, or escalated

C11 is therefore about **parcel-shaped post-pressure outputs**.
It is not about the full doctrines that make those outputs valuable, legal, recognized, or usable.

## What C11 owns

C11 owns:
- inflow parcel family distinctions
- source-state family reflection at parcel scale
- parcel vs payload distinctions
- parcel granularity distinctions
- material vs non-material inflow distinctions
- direct possession vs claim vs entitlement distinctions
- grant vs recognition vs authorization distinctions
- delivery-state architecture
- realization-state architecture
- divisibility and allocation architecture
- transferability architecture
- holder, bearer, custodian, and escrow topology at parcel scale
- visibility and disclosure posture at parcel scale
- legality-hook and recognition-hook grammar at parcel scale
- burden-bearing inflow grammar
- mixed inflow parcel grammar
- deferred, contingent, escrowed, recurring, and successor-bound inflow parcel grammar
- template, archetypal, instance, and generated parcel distinctions

## What C11 does not own

C11 does **not** own:
- full value doctrine
- full exchange or pricing doctrine
- full legality doctrine
- full access doctrine
- full post-pressure inflow doctrine
- item ontology
- frame ontology
- site ontology
- organization ontology
- mission or success doctrine
- salvage-processing procedure
- crafting-transformation procedure
- random reward generation procedure
- sourcebook packaging
- publication appendices
- loot catalogs as setting content repositories

## Scale ladder and parcel place in Batch C

For Batch C routing discipline, Astra should recognize the following scale relation for post-pressure outputs:

1. **Underlying payload entry**
   One item, resource, frame, site target, organization relation target, or other content object referenced by an inflow.

2. **Parcel component**
   One direct payload line, claim line, entitlement line, recognition line, restriction line, burden line, or delivery line within a parcel.

3. **Parcel record**
   One packaged inflow output owned by C11.

4. **Parcel bundle**
   Several linked parcels that remain distinct because they differ in delivery state, claim state, holder topology, burden profile, or source-state relation.

5. **Mission/scenario integration**
   A C10 structure that references one or more parcels through triggers and successor conditions.

6. **Generator emission**
   A C12 structure that emits parcel instances, parcel components, or parcel templates.

7. **Container packaging**
   A C13 structure that groups parcels into appendices, catalogs, bundles, mission kits, or sourcebook packaging.

C11 owns level 3 directly and defines level-2 parcel component logic where needed.
C11 may acknowledge level 4 as linked parcel aggregation, may reference level 1, be triggered by level 5, be emitted by level 6, and be packaged by level 7, but it does not own those other layers.

## Dominant-function routing rules

All candidate C11 content must be routed by **dominant structural job**, not by donor flavor text.

A record belongs in C11 when its main job is to define:
- a packaged inflow output
- a claimable or distributable output package
- a grant, recognition, authorization, or support package
- a mixed bundle of post-pressure outcomes
- a deferred or conditional inflow package

A record does **not** belong in C11 merely because it is valuable, desirable, prestigious, or awarded after a scenario.

If the dominant job is defining the thing itself, route to the correct underlying content file.
If the dominant job is defining how inflows work generally, route to Batch B doctrine.
If the dominant job is defining mission completion or successor logic, route to C10.
If the dominant job is defining random emission logic, route to C12.
If the dominant job is packaging a set of rewards for publication or reference, route to C13.

## Source-state, parcel, payload, and realization chain

C11 must preserve four distinct layers that donors often blur together.

### Source-state

A **source-state** is the structural condition out of which the parcel arises.
Examples include:
- patron or employer transfer
- salvageable remains or wreckage
- recognized claim target
- site clearance or occupation result
- tribunal or adjudication result
- faction conferment
- ceremonial or trial outcome
- surrender or custody result
- discovered cache or reserve
- recurring stipend or service channel

Source-state is not parcel family.
A parcel may be a claim parcel because it comes from a site-clearance source-state, a tribunal source-state, or a salvage source-state.

### Parcel

A **parcel** is the packaged schema unit by which one or more inflow components are represented together.

### Payload

A **payload** is the thing, reference, right, support package, or status output that the parcel delivers or points to.

### Realization or enforcement state

A **realization or enforcement state** describes whether the parcel or parcel component has become practically usable, redeemable, extractable, enforceable, or merely recognized in principle.

### Chain principles

1. Source-state is not parcel identity.
2. Parcel identity is not payload identity.
3. Recognized parcel existence is not the same thing as practical realization.
4. Realization is not the same thing as enforceability.
5. Converters must be able to say not just what a parcel is, but what produced it and whether it can actually be used yet.

## Inflow, parcel, payload, claim, and entitlement distinctions

### Inflow

An **inflow** is any structured post-pressure gain, grant, recognition, claim, authorization, support package, or other output that enters Astra play-state or Astra content-state after a relevant trigger.

“Reward” is one inflow family, not the universal umbrella term.

### Parcel

A **parcel** is the packaged schema unit by which one or more inflow components are represented together.

A parcel may contain:
- direct payloads
- claim components
- entitlement components
- recognition components
- delivery components
- distribution constraints
- burden components
- visibility constraints
- legality hooks
- processing requirements

### Payload

A **payload** is the thing, reference, right, support package, or status output that the parcel delivers or points to.

A payload may be:
- direct and present
- deferred
- conditional
- contested
- reference-based rather than physically transferred
- consumable or persistent
- divisible or indivisible

### Claim

A **claim** is a recognized, provisional, contested, or otherwise structured relationship asserting a right to later possession, recovery, occupation, salvage, study, extraction, jurisdiction, or benefit.

A claim is not automatically possession.
A claim is not automatically enforcement.
A claim is not automatically transferability.

### Entitlement

An **entitlement** is a structured right to receive, access, draw upon, requisition, enter, request, use, maintain, or be served, whether immediately or under specified conditions.

An entitlement is not automatically a physical payload.

### Recognition output

A **recognition output** is a parcel component that changes formal status, standing, title, legitimacy, favor, warrant, sponsorship, or authorized relation without necessarily transferring a physical object.

Recognition output is not the same as underlying organization doctrine.

## Direct possession, claim, entitlement, authorization, recognition, and support

C11 must preserve distinct parcel-output modes.

### Direct possession output
A payload is transferred into immediate possession, custody, or holding.

### Claim output
A recipient gains a structured right to later recover, possess, control, occupy, or sell something, subject to defined claim state.

### Entitlement output
A recipient gains a right to draw upon services, support, access, maintenance, transport, requisition, or recurring supply.

### Authorization output
A recipient gains recognized permission, clearance, legal channel, or bounded operational allowance.

### Recognition output
A recipient gains standing, title, favor, sponsorship, legitimacy, official notice, or relational status.

### Support output
A recipient gains practical support such as escort promises, maintenance support, shelter rights, repair allocations, emergency aid, or processing privileges.

These output modes may coexist inside one parcel.
They must not be collapsed into one flat reward line.

## Parcel family, function, posture, and source-state family

C11 must distinguish several different kinds of classification.

### Parcel family

Parcel family identifies **what kind of packaged inflow** the record is.
Examples include:
- material parcel
- payment parcel
- salvage parcel
- claim parcel
- access parcel
- recognition parcel
- support parcel
- conferment parcel
- mixed inflow parcel
- deferred/contingent parcel
- corrosive or poisoned-benefit parcel

### Parcel function

Parcel function identifies **what the parcel is for**.
Examples include:
- compensation
- restitution
- salvage distribution
- claim recognition
- access opening
- sponsorship
- conferment
- survival carry-out
- proof reward
- authority settlement
- upkeep support
- legitimacy repair
- faction binding
- appeasement
- hush compensation
- public commendation

### Parcel posture

Parcel posture identifies **how the parcel behaves** with respect to certainty, transfer, burden, and timing.
Examples include:
- immediate and clean
- immediate but burden-bearing
- deferred
- contingent
- escrowed
- disputed
- publicly recognized
- covert
- recurring
- non-transferable
- divisible-share
- mixed-recognition-and-material
- poisoned-benefit

### Source-state family

Source-state family identifies **what kind of structural condition produced the parcel**.
Examples include:
- direct transfer source-state
- salvage source-state
- claim-target source-state
- site-clearance or occupation source-state
- adjudication source-state
- conferment source-state
- trial or ceremonial source-state
- surrender or custody source-state
- discovered cache source-state
- recurring service-channel source-state

Family, function, posture, and source-state family must not be collapsed into one label.

## Core C11 parcel families

C11 should support the following major parcel families.
These are not all interchangeable and should not be flattened into one universal loot schema.

### 1. Material parcel

A parcel delivering direct tangible payloads such as items, resources, relics, components, stores, or other material holdings.

### 2. Payment parcel

A parcel delivering direct compensation, currency-equivalent compensation, vouchers, stipends, or settlement outputs.

### 3. Salvage parcel

A parcel delivering recovered materials, damaged holdings, extraction outputs, salvage bundles, wreck components, biological harvests, or salvage claims tied to condition and processing state.

### 4. Claim parcel

A parcel delivering structured rights over objects, sites, caches, wrecks, bodies, routes, titles, licenses, or recoverable holdings.

### 5. Access or authorization parcel

A parcel delivering permits, warrants, passes, recognition tokens, route access, docking clearance, requisition eligibility, protected channels, or bounded-use authorization.

### 6. Recognition parcel

A parcel delivering standing, favor, title, legitimacy, honors, sponsorship, rank marks, public commendations, or relational status outputs.

### 7. Conferment parcel

A parcel delivering blessings, boons, patron marks, rights of inheritance, sect recognition, ritual acknowledgment, succession confirmation, or other formal conferments not reducible to ordinary material transfer.

### 8. Support or service parcel

A parcel delivering maintenance rights, escort allocations, safe harbor, aid commitments, processing privileges, supply lines, repair time, transport support, or similar bounded services.

### 9. Mixed inflow parcel

A parcel combining two or more materially distinct output modes, such as payment plus access plus claim plus recognition.

### 10. Deferred or contingent parcel

A parcel whose delivery, claim realization, public recognition, or activation depends on later proof, later extraction, later adjudication, milestone completion, or successor-state confirmation.

### 11. Corrosive or poisoned-benefit parcel

A parcel that is structurally beneficial or gain-bearing but also carries hazard, obligation, public burden, surveillance, retaliation risk, curse-like burden, or politically dangerous exposure as an intrinsic part of the parcel rather than as a merely incidental side note.

## Parcel granularity doctrine

C11 must preserve parcel granularity explicitly.

### Granularity classes
- atomic parcel
- multi-component parcel
- linked parcel bundle
- container or appendix grouping

### Granularity principles

1. One donor “reward” may actually normalize into several parcels.
2. A multi-component parcel remains one parcel when its components share one delivery and structural identity line.
3. A linked parcel bundle should remain plural when components differ materially in claim state, delivery state, holder topology, or burden profile.
4. Container or appendix grouping is not parcel identity and belongs to C13.

## Common parcel-record grammar for C11

All C11 records should inherit common Batch C record grammar from C01 and then add the following parcel groups as needed.

### A. Structural identity group
- parcel_family
- parcel_function_profile
- parcel_posture
- source_state_family
- parcel_granularity
- parcel_scale
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

### C. Trigger and source group
- inflow_trigger_profile
- source_state_profile
- mission_or_scenario_trigger_refs
- objective_or_successor_trigger_refs
- salvage_or_extraction_trigger_refs
- adjudication_trigger_refs
- recognition_trigger_refs
- generator_emission_trigger_refs
- authority_source_refs
- sponsor_source_refs
- claimant_source_refs
- predecessor_parcel_refs

### D. Recipient, holder, and eligibility group
- recipient_profile
- recipient_scope
- holder_topology
- bearer_or_custodian_profile
- claimant_profile
- beneficiary_profile
- escrow_holder_refs
- certifier_or_witness_refs
- enforcement_body_refs
- eligibility_conditions
- priority_order_rules
- exclusion_conditions
- successor_recipient_rules

### E. Payload composition group
- direct_payload_refs
- indirect_payload_refs
- claim_components
- entitlement_components
- authorization_components
- recognition_components
- support_components
- burden_components
- processing_required_refs
- dependency_refs
- payload_condition_profile

### F. Claim, realization, and recognition group
- claim_state
- claim_realizability_state
- claim_enforceability_state
- recognition_state
- realization_state
- enforcing_authority_refs
- disputing_party_refs
- evidence_or_proof_hooks
- custody_status
- extraction_status
- occupancy_or_control_status
- transfer_restriction_profile

### G. Delivery and distribution group
- delivery_state
- release_conditions
- activation_requirements
- installment_profile
- recurrence_profile
- recurrence_topology
- escrow_profile
- divisibility_profile
- competition_topology
- distribution_profile
- role_based_share_rules
- negotiated_share_rules
- mandatory_carveout_rules

### H. Visibility, legality-hook, and use-boundary group
- visibility_profile
- audience_or_disclosure_topology
- disclosure_requirements
- legality_hook_profile
- access_hook_profile
- authorization_duration_profile
- use_boundaries
- time_limit_profile
- expiration_or_decay_profile
- public_record_profile

### I. Burden and consequence group
- maintenance_burden_profile
- obligation_profile
- surveillance_or_exposure_profile
- political_or_faction_burden_profile
- contamination_or_processing_risk_profile
- inheritance_of_burden_rules
- downstream_consequence_hooks

C11 does not require every parcel to use every field group.
It does require every parcel to use the groups justified by its structure family and posture.

## Payload architecture

C11 payload logic must remain more rigorous than casual reward prose.

### Payload classes
At minimum, Astra should recognize the following payload classes when relevant:
- direct material payload
- direct compensation payload
- salvage payload
- biological harvest payload
- damaged or partial payload
- claim payload
- entitlement payload
- authorization payload
- recognition payload
- conferment payload
- service/support payload
- deferred payload
- contingent payload
- mixed payload
- burden-bearing payload

### Payload principles

1. A parcel may contain multiple payload classes.
2. Payload identity is not the same as parcel identity.
3. A parcel may reference an external payload entry rather than reproducing it.
4. A claim payload must not be rewritten as direct possession unless the donor or normalization basis explicitly supports that.
5. A support or recognition payload must not be rewritten as an item merely because it has high value.
6. A salvage payload may require condition, processing, proof, custody, or extraction notes that a clean material payload does not.

## Source-role doctrine

Many parcels are shaped not only by what they contain, but by who issues, confers, certifies, disputes, or administers them.

### Source roles
When relevant, Astra should distinguish:
- issuer
- sponsor
- payer
- adjudicator
- conferring body
- escrow holder
- claimant source
- enforcement body
- witness or certifier
- service provider
- challenge or trial source
- site-of-origin

### Source-role principles

1. Source roles describe parcel origin and administration, not full organization or site ontology.
2. One parcel may involve several source roles simultaneously.
3. Source role difference materially affects parcel behavior even when payload type is similar.
4. Source roles must not be collapsed into generic “source” when donor structure distinguishes them.

## Claim-state doctrine

Claim-state is one of the most important C11 distinctions.
A large donor corpus will repeatedly use claims that are neither clean possession nor pure narrative suggestion.

### Claim-state classes
When relevant, Astra should distinguish:
- recognized uncontested claim
- provisional claim
- disputed claim
- shared claim
- escrowed claim
- authority-pending claim
- proof-pending claim
- extraction-contingent claim
- custody-contingent claim
- time-limited claim
- non-transferable claim
- revocable claim
- inherited claim

### Claim realization classes
When relevant, Astra should distinguish:
- unrealized claim
- realizable but unclaimed
- realized through custody
- realized through extraction
- realized through registration or certification
- blocked realization
- partially realized claim

### Claim enforceability classes
When relevant, Astra should distinguish:
- unenforced assertion
- recognized but weakly enforceable
- operationally enforceable
- authority-backed enforceable
- locally enforceable only
- conditionally enforceable
- disputed and practically unenforceable

### Claim principles

1. Claim is not possession.
2. Claim is not automatically enforceable.
3. Claim may exist without present custody.
4. Claim realizability and claim enforceability are separate axes.
5. Multiple parties may hold competing claim relations to the same target.
6. Claim state may change after adjudication, proof, extraction, registration, or public recognition.
7. Claim records must distinguish the target of the claim from the state of the claim.

## Recognition and standing doctrine

Recognition outputs are common and must not be collapsed into either faction ontology or generic reputation prose.

### Recognition classes
When relevant, Astra should distinguish:
- standing change
- formal honor
- title or rank conferment
- sponsor acknowledgment
- credential issuance
- faction trust output
- patron favor output
- public commendation
- protected status recognition
- succession recognition
- apology or restitution recognition

### Recognition principles

1. Recognition is not a physical payload.
2. Standing change is not identical to title conferment.
3. Title conferment is not identical to credential issuance.
4. Credential issuance is not identical to protected status.
5. Recognition is not automatically transferable.
6. Recognition may be public, private, sealed, deniable, or conditional.
7. Recognition may open access channels without itself defining those channels fully.
8. Recognition parcel shape is owned by C11; underlying social, organizational, or legality doctrine remains elsewhere.

## Authorization and entitlement doctrine

Many donors reward with permission, eligibility, or recurring access rather than objects.

### Authorization or entitlement classes
When relevant, Astra should distinguish:
- permit or pass
- warrant or official writ
- access license
- route clearance
- docking or harbor authorization
- requisition eligibility
- sanctuary or asylum access
- service entitlement
- maintenance priority
- research or study rights
- extraction rights
- recurring stipend eligibility
- protected channel use rights

### Authorization duration classes
When relevant, Astra should distinguish:
- single-use
- repeat-use bounded
- recurring renewal
- revocable at will
- office-bound duration
- token-bound duration
- site-bound duration
- route-bound duration
- season-bound duration
- emergency-bound duration

### Authorization principles

1. Authorization is not ownership.
2. Authorization is not always public.
3. Authorization may be time-bound, site-bound, issuer-bound, token-bound, or use-bound.
4. Entitlement may be recurring without being freely exchangeable.
5. C11 may encode authorization shape, but not the full doctrine of how access systems operate generally.

## Parcel condition and condition-of-payload doctrine

C11 must preserve that parcel validity and payload condition are not always the same thing.

### Condition distinctions
When relevant, Astra should distinguish:
- valid parcel with clean payload
- valid parcel with damaged payload
- valid parcel with contaminated payload
- valid parcel with disputed target state
- released parcel with partially extracted payload
- immediate parcel with not-yet-usable payload
- recognized parcel with blocked realization state

### Condition principles

1. Parcel condition and payload condition are not the same axis.
2. A parcel may be structurally valid while its payload remains damaged, contaminated, incomplete, disputed, or unrealized.
3. Salvage and biological-harvest donors especially pressure this distinction.
4. Converters must not flatten payload condition into parcel nonexistence.

## Delivery-state, activation, and realization doctrine

C11 must preserve when and how inflows arrive, and when they actually become usable.
Many donor outputs do not arrive immediately or all at once.

### Delivery-state classes
A parcel may be:
- immediate
- staged
- delayed
- contingent
- escrowed
- recurring
- milestone-based
- successor-bound
- proof-triggered
- extraction-triggered
- authority-release-triggered
- hidden-until-triggered

### Activation or realization classes
A parcel or parcel component may require:
- claiming
- redemption
- registration
- certification
- extraction
- installation
- attunement or formal acceptance
- public recognition
- authority release
- successor-state confirmation

### Delivery and realization principles

1. Delivery state is separate from payload type.
2. A parcel may exist before it is fully released.
3. Delayed or contingent delivery is not the same as nonexistence.
4. Recurring delivery should be represented as parcel posture, not improvised later in mission prose.
5. Escrowed delivery should preserve release conditions and holding structure explicitly when relevant.
6. Realization posture should be represented explicitly whenever “you got it” is not yet the same as “you can use or enforce it.”
7. Deferred parcel, contingent parcel, and successor-bound parcel are not the same thing.
   - Deferred means it arrives later if nothing else materially changes.
   - Contingent means it depends on later conditions being met.
   - Successor-bound means it becomes relevant only in a later successor structure or successor-state.

## Divisibility, distribution, allocation, and competition doctrine

Not every parcel splits the same way.
A large donor corpus will repeatedly pressure this distinction.

### Divisibility classes
When relevant, Astra should distinguish:
- indivisible parcel
- divisible parcel
- share-structured parcel
- role-bound parcel
- claimant-priority parcel
- issuer-retained-share parcel
- mandatory-carveout parcel
- pooled-distribution parcel

### Competition topology classes
When relevant, Astra should distinguish:
- single-recipient
- multi-recipient
- share-based
- claimant-competitive
- authority-awarded
- performance-ranked
- role-based
- sponsor-directed
- survivor-based
- public lottery or distributed pool

### Distribution principles

1. Divisibility describes what can be split.
2. Distribution describes how a parcel is actually allocated.
3. Competition topology describes how recipient contention is structured.
4. An indivisible parcel may still produce layered recognition or support side outputs.
5. Distribution rules may depend on role, proof, custody, contribution, standing, contract, or adjudication.
6. Divisible material output and non-transferable recognition output may coexist inside one parcel.

## Transferability and control doctrine

Parcel outputs differ sharply in whether they can be sold, assigned, inherited, gifted, or delegated.

### Transferability classes
When relevant, Astra should distinguish:
- freely transferable
- conditionally transferable
- authority-approved transfer only
- assignment-only
- inheritable but not saleable
- non-transferable
- issuer-bound
- recipient-bound
- site-bound
- time-bound

### Transfer principles

1. Transferability is not the same as divisibility.
2. Control or custody may shift without full transfer of claim.
3. Non-transferable recognition or authorization outputs are common and must not be treated like generic loot.
4. Transfer restrictions should be attached to parcel components when only part of a parcel is restricted.

## Holder, bearer, custodian, and escrow topology

Many parcels do not sit cleanly in one person’s inventory or possession state.

### Holder topology classes
When relevant, Astra should distinguish:
- individual-held
- party-held
- faction-held
- site-authority-held
- escrow-held
- claimant-class-held
- mixed-holder arrangement

### Holder principles

1. Recipient is not always the same as holder.
2. Holder is not always the same as beneficiary.
3. Custodian is not always the same as claimant.
4. Escrow structures must preserve who holds, who benefits, and who may release the parcel.
5. Team claims, institutional grants, and public recognitions must not be rewritten into single-person ownership for convenience.

## Visibility, audience, legality-hook, and recognition-hook doctrine

C11 must preserve visibility and legality-relevant status without stealing full legality doctrine.

### Visibility classes
When relevant, Astra should distinguish:
- public
- sealed but recognized
- private and recognized
- covert
- deniable
- hidden-until-claimed
- hidden-until-proofed
- hidden-until-delivered

### Audience or disclosure classes
When relevant, Astra should distinguish whether disclosure matters to:
- recipient only
- claimants
- authorities
- the public
- stakeholders
- rivals
- institutions providing service or enforcement

### Legality-hook or recognition-hook classes
When relevant, Astra should distinguish:
- licit-recognized
- licit-restricted
- disputed-recognition
- contraband-exposed
- deniable-offer
- irregular-but-tolerated
- unofficial-but-functional
- authority-pending

### Visibility and legality principles

1. C11 may record these hook states without owning the doctrines that govern them.
2. Visibility posture materially affects parcel behavior and downstream consequences.
3. A covert parcel is not the same as an illegal parcel.
4. A recognized parcel is not automatically publicly visible.
5. Hook states should be used to connect to B04/B12 rather than replace them.
6. Audience or disclosure topology should be represented when who knows materially changes enforcement, use, burden, or contestation.

## Burden-bearing and negative-output doctrine

A parcel may be beneficial without being cleanly positive.
Some donor outputs carry duties, upkeep, enemies, publicity, debt, hazard, or exposure.

### Burden classes
When relevant, Astra should distinguish:
- maintenance burden
- custody burden
- contamination or hazard burden
- surveillance burden
- political burden
- factional obligation burden
- public-duty burden
- secrecy burden
- inheritance or succession burden
- processing burden
- debt-linked burden
- retaliation-risk burden

### Negative or corrosive parcel examples
C11 should explicitly support parcels such as:
- hush compensation
- cursed inheritance
- legally binding honor
- poisoned gift
- surveillance-laced access
- politically radioactive commendation
- bounty payment that creates enemies
- title that forces obligation
- reward that operates as a structural trap

### Burden principles

1. Burden-bearing output is still an inflow parcel if it is structurally a gain or grant.
2. Burden must not be erased merely because a donor frames the parcel as a reward.
3. Burden components may be attached to only part of a mixed parcel.
4. Burden profile is not the same thing as mission consequence, though the two may interact.
5. Some parcels are structurally double-edged or corrosive rather than merely positive-with-extra-cost.

## Mixed parcel doctrine

Mixed parcels are first-class schema families, not edge cases.
A large donor corpus will repeatedly package unlike outputs together.

### Mixed parcel examples
A parcel may combine:
- money plus recognition
- salvage claim plus extraction rights
- title plus service entitlement
- direct possession plus future stipend
- access authorization plus faction obligation
- material prize plus public burden
- payment plus hush conditions plus route clearance

### Mixed parcel principles

1. Mixed parcel identity should be explicit.
2. Component-level restrictions must be preserved when the parcel combines unlike outputs.
3. Mixed parcels must not flatten all components into one generic value line.
4. Mixed parcels may contain both direct and deferred components.
5. Mixed parcels may contain both positive and burden-bearing components.

## Sparse-shell versus dense-parcel doctrine

Some donor outputs are sparse shells with only a few declared anchors.
Others are densely specified with many conditions, shares, restrictions, and references.

### Density classes
- sparse shell parcel
- medium-density parcel
- dense authored parcel

### Density principles

1. Sparse parcels should not be artificially inflated.
2. Dense parcels should not be flattened into one-line summaries if the donor relies on internal structure.
3. Density is structural, not stylistic.
4. Generated parcels may be sparse even when the surrounding reward framework is dense.

## Recurrence doctrine

Recurring parcel behavior needs more precision than a simple yes-or-no recurrence flag.

### Recurrence topology classes
When relevant, Astra should distinguish:
- fixed recurring parcel
- renewable recurring parcel
- contingent recurring parcel
- milestone-refresh parcel
- service-window parcel
- office-bound recurring parcel
- claim-income parcel

### Recurrence principles

1. Recurrence topology is part of parcel posture, not a mere prose note.
2. Recurring parcels should preserve what refreshes them, what can interrupt them, and whether they depend on office, claim, access, or continued recognition.
3. Recurring parcel posture must not be mistaken for general economy doctrine.

## Template, archetype, instance, and generated parcel doctrine

C11 must support both reusable parcel patterns and specific converted parcel instances.

### Reusable parcel templates
Examples of template-level parcel patterns include:
- employer payment plus equipment reimbursement
- salvage claim with proof and extraction contingencies
- recognition plus access opening plus sponsor obligation
- title grant with public-duty burden
- mixed success parcel with immediate payout and deferred sponsor backing

These are templates, not converted parcel instances.

### Normalized archetypal parcels
A normalized archetypal parcel is Astra’s stable doctrinal skeleton for a recurring donor reward family, narrower than a pure template and broader than one converted instance.

### Instantiated parcels
An instantiated parcel is a specific reward, claim, salvage, conferment, or mixed inflow package created during donor conversion.

### Generated parcels
Generated parcels may enter C11 in two distinct ways:
- as parcel instances emitted by an external generator
- as persistent parcel shells that repeatedly accept generated inserts or generated payout components

These are not the same schema situation and must not be conflated.

### Normalization rules

1. Preserve donor parcel distinctions whenever Astra can represent them lawfully.
2. Normalize donor presentation into Astra parcel structure only as far as needed for cross-corpus stability.
3. Do not invent clean market logic where the donor only supplies parcel shape.
4. Do not erase genuine parcel complexity simply to make a donor look simpler.
5. Mark authored parcel structure and normalized parcel structure separately when they differ materially.

## Publication-unit warning

A donor publication unit may normalize into:
- one parcel instance
- several linked parcel instances
- one parcel template plus one or more instances
- one generator relation plus parcel instances
- one persistent parcel shell plus generated inserts
- mixed C11 and C13 structures

One donor chapter may normalize into zero, one, or many C11 records, and may also normalize partly into C13 packaging without one-to-one correspondence.
Reward appendices, treasure chapters, and payout lists are especially misleading publication forms and must not be mistaken for parcel family granularity.

Publication layout is not parcel identity.

## Cross-file composition discipline

### Batch B16 inflow handoff

C11 must not redefine what counts as post-pressure inflow generally, how inflows are earned as doctrine, or how inflow categories are systemically governed.
C11 consumes B16 through parcel hooks, source-state reflection, and trigger references.

### Batch B04/B12 value, legality, and access handoff

C11 may define:
- legality-hook profiles
- recognition-hook profiles
- access-hook profiles
- value-relevant posture notes

C11 must not define full value doctrine, market logic, legality procedure, or access-system doctrine.

### C04 item/resource handoff

C11 may reference items, resources, components, permits, claim-bearing objects, or service-enabling tokens as payloads.
C11 must not redefine the underlying atomic entries.

**If the dominant function is the atomic thing itself, route to C04.**
**If the dominant function is the packaged inflow relationship around one or more things, route to C11.**

### C05 frame handoff

C11 may reference vehicles, ships, mechs, stations, or platforms as payloads, salvage targets, or claim targets.
C11 must not redefine those frame entries.

### C06 site handoff

C11 may reference sites as claim targets, authorization targets, service targets, extraction zones, occupancy targets, or burden targets.
C11 must not absorb site ontology.

### C07 faction handoff

C11 may reference organizations as issuers, recognizers, disputing bodies, sponsors, enforcers, or beneficiaries.
C11 must not redefine organization ontology, mandate, or jurisdiction.

### C10 mission/scenario handoff

C10 may define when parcels trigger, change, become available, become blocked, or advance into successor states.
C11 defines the parcel structure itself once that happens.
C11 must not redefine mission completion or successor logic.

### C12 generator handoff

C11 may define parcel shapes that a generator emits.
C11 must not define roll logic, event logic, loot tables, payout tables, or generator procedure.

### C13 container handoff

C11 parcels may be packaged in catalogs, appendices, sourcebook bundles, mission kits, or reward lists.
C11 must not define publication packaging.

## Anti-collapse rules

C11 must not:
- treat all inflows as treasure
- treat all valuable things as parcel records
- treat a parcel as an item entry
- treat claim recognition as direct possession
- treat direct possession as proof of legal recognition
- treat faction standing as if it were a faction record
- treat mission-success prose as if it already defines parcel structure
- treat mixed parcels as one flat value line
- treat random reward tables as parcel schemas
- treat legality-hook fields as permission to redefine legality doctrine
- treat salvage bundles as if they were only item lists without condition, extraction, or claim posture
- treat conferments, titles, or blessings as if they were ordinary currency payouts
- confuse source-state with parcel family
- confuse recognized claim with realizable claim or enforceable claim
- confuse holder, beneficiary, claimant, and custodian topology

## Anti-hallucination rules for future conversion

Future conversion working from C11 must obey the following:

1. Do not treat every post-pressure gain as treasure.
2. Do not infer market value merely because a parcel is important.
3. Do not infer legal enforceability merely because a claim is asserted.
4. Do not rewrite claim, entitlement, authorization, or recognition into direct possession for convenience.
5. Do not rewrite direct possession into fully recognized legal ownership unless the donor or normalization basis supports that.
6. Do not treat salvage potential as guaranteed extracted payload without extraction, proof, custody, or processing support.
7. Do not infer transferability from divisibility.
8. Do not infer public recognition from formal recognition.
9. Do not invent a clean reward split when the donor presents ambiguity, dispute, hierarchy, or claimant priority.
10. Do not treat burden-bearing parcels as clean positive payouts.
11. Do not mistake a generator-emitted parcel instance for a persistent parcel shell or vice versa.
12. Do not confuse parcel identity with underlying payload identity.
13. Do not confuse claim state with possession state.
14. Do not confuse successor trigger with delivery release.
15. Do not let one donor family, whether treasure-centric fantasy or salvage-centric sci-fi, define the universal parcel model.
16. Do not mistake a donor publication unit for parcel family granularity.
17. Do not mistake recognized claim for realizable claim or enforceable claim.
18. Do not rewrite team-held, escrow-held, or claimant-class-held parcels into single-recipient ownership for convenience.

## Validation stress list

C11 validation should repeatedly pressure-test the following failure modes:
- direct item reward mistaken for complete parcel doctrine
- salvage bundle flattened into item list without condition or claim posture
- legal claim mistaken for direct ownership
- recognition output mistaken for faction entry
- access authorization mistaken for site or faction doctrine
- mixed payout collapsed into one value line
- delayed parcel mistaken for absent parcel
- divisibility confused with transferability
- mission success notes mistaken for parcel schema
- generator payout table mistaken for parcel structure
- blessing or title grant mistaken for ordinary loot
- burden-bearing reward normalized into clean positive gain
- publication appendix mistaken for one parcel record
- direct mission completion note mistaken for a parcel
- atomic permit or token mistaken for a parcel
- salvageable wreck or site mistaken for parcel rather than source-state
- title or office mistaken for C07 rather than recognition parcel or vice versa
- recurring stipend mistaken for general economy rather than parcel posture
- public honor mistaken for faction entry
- access opening mistaken for one-time authorization token

## File outcome

If C11 is functioning correctly, Astra should be able to do all of the following without collapse:
- represent direct material rewards
- represent salvage bundles and salvage claims
- represent legal or social claims without rewriting them as possession
- represent access grants, warrants, licenses, and service entitlements
- represent faction payments, honors, titles, and standing outputs without absorbing faction doctrine
- represent mixed parcels combining money, access, recognition, and burden
- represent delayed, contingent, escrowed, recurring, and successor-bound inflows
- distinguish source-state, parcel shape, payload identity, and realization or enforcement state
- distinguish parcel shape from value doctrine and legality doctrine
- distinguish underlying payload entries from parcel records
- integrate lawfully with C10 mission structures, C12 generators, and C13 packaging

That is the doctrinal job of this file.

