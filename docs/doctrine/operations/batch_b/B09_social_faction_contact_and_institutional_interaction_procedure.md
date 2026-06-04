# B09 Social, Faction Contact, and Institutional Interaction Procedure

## 1. Purpose and status

B09 is the ninth Batch B operational doctrine draft for Astra social contact, faction contact, and institutional interaction handling. It sits after `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md`, `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md`, `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md`, `docs/doctrine/operations/batch_b/B04_inventory_storage_custody_and_burden_procedure.md`, `docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md`, `docs/doctrine/operations/batch_b/B06_project_crafting_salvage_repair_and_upgrade_procedure.md`, `docs/doctrine/operations/batch_b/B07_recovery_training_research_and_preparation_project_procedure.md`, and `docs/doctrine/operations/batch_b/B08_travel_exploration_navigation_and_discovery_procedure.md` as upstream Batch B context and must build on them, not rewrite them.

B09 defines how operational attention is routed when social, factional, legal, institutional, standing, access, claim, obligation, authority, or relationship pressure appears after B01-B08 procedure. It classifies contact, reviews standing/pressure/obligation/claim/access boundaries, identifies risk and visibility checkpoints, routes negotiation/diplomacy/persuasion/intimidation/deception/bribery/blackmail/patronage/institutional response triggers, and hands social/faction/contact state deltas to owner files without defining final social mechanics, final faction schema, reputation math, law codes, faction clocks, runtime relationship state, hidden-truth presentation, canon, live-play dialogue behavior, or sourcebook faction prose.

Status posture:
- This file is Batch B operational-procedure draft material.
- This file is not current canon, not final mechanics, not runtime authority, not sourcebook prose, and not player-facing rule text.
- C00 remains the schema handoff control surface for Batch B to C-family routing.
- D00-D19 source packs are referenced only as draft source-pack/reference material, not final current doctrine authority, final mechanics, runtime authority, canon, live-play GM behavior, or sourcebook prose.
- B09 records, examples, and handoff blocks are doctrine-facing only; they are not runtime state, backend contracts, database contracts, event logs, command lifecycle artifacts, context packet formats, social-state database rows, faction-state rows, relationship ledgers, reputation ledgers, law database rows, faction AI instructions, sourcebook statblocks, canon entries, or live-play scripts.
- B09 does not require, define, create, or promote B10-B11. B09 does not require, define, create, or promote C01-C14.
- No registry status is promoted to current by B09.

Required reference boundaries preserved by B09:
- `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md` for upstream Batch B scene, activity, encounter, pressure, transition, and owner-handoff context; B09 may route to B01 but must not reopen scene cadence.
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` for upstream Batch B action declaration, cost commitment, feasibility, and resolution-trigger context; B09 may route to B02 but must not define final action resolution.
- `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md` for upstream Batch B item, gear, equipment, object-system construct, and asset-use procedure; B09 may route object leverage or restricted object access to B03 but must not redefine object use.
- `docs/doctrine/operations/batch_b/B04_inventory_storage_custody_and_burden_procedure.md` for upstream Batch B inventory, storage, custody, access, burden, lawful loss, and recovery procedure; B09 may route custody/access consequences to B04 but must not redefine inventory or custody.
- `docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md` for upstream Batch B acquisition, reward, requisition, value flow, market access, scarcity, upkeep, and value-sink procedure; B09 may route value, debt, favor, bribe, reward, requisition, permit-fee, or market access issues to B05 but must not define economy law or debt-value math.
- `docs/doctrine/operations/batch_b/B06_project_crafting_salvage_repair_and_upgrade_procedure.md` for upstream Batch B project-centered interval work, crafting, salvage, repair, modification, upgrade, requirements, progress, complications, and project outputs; B09 may route sponsored work or institutional tasks to B06 but must not redefine projects.
- `docs/doctrine/operations/batch_b/B07_recovery_training_research_and_preparation_project_procedure.md` for upstream Batch B recovery, training, research, preparation, readiness, proof routing, desired-outcome routing, and non-object project outputs; B09 may route training/research/petition preparation or proof discovery to B07 but must not redefine recovery, training, or research.
- `docs/doctrine/operations/batch_b/B08_travel_exploration_navigation_and_discovery_procedure.md` for upstream Batch B travel, exploration, navigation, discovery, scouting, mapping, site entry, watches, ambush exposure, travel pressure, and transition handoffs; B09 may route checkpoints, borders, permits, restricted site entry, and travel access pressure to B08 but must not redefine travel/exploration.
- `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` for shared Batch C base fields, `pending_schema`, source-local boundary, rejected donor element, canon eligibility, review routing, provenance, and missing-schema fallback language.
- `docs/doctrine/native_design/d_series/source_packs/astra_d00_doctrine_pack_v0_1/D00-03_state_delta_commit_protocol.md` for the draft source-pack state-delta principle that every meaningful event commits at least one delta to a recognized owner, while B09 does not own every delta format.
- `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-00_resolution_architecture_and_owner_boundaries.md` for draft resolution owner-boundary reference material, while B09 does not define final resolution mechanics.
- `docs/doctrine/native_design/d_series/source_packs/astra_d05_doctrine_pack_v0_1/D05-03_relevance_handling_for_checks.md` for draft relevance-check reference material, while B09 does not define final check math.
- `docs/doctrine/native_design/d_series/source_packs/astra_d08_doctrine_pack_v0_1/D08-00_layered_actor_state_architecture.md` and `docs/doctrine/native_design/d_series/source_packs/astra_d08_doctrine_pack_v0_1/D08-01_identity_continuity_personhood_and_agency.md` as the current equivalent D08 actor identity/personhood/substrate references because the requested `D08-00_actors_identity_body_substrate_and_form_owner_boundaries.md` path is absent; B09 cites the current paths and does not invent the missing path silently.
- `docs/doctrine/native_design/d_series/source_packs/astra_d10_doctrine_pack_v0_1/D10-07_information_state_public_knowledge_rumor_secrecy_records_register.md` for draft information-state, public knowledge, rumor, secrecy, record, and register reference material.
- `docs/doctrine/native_design/d_series/source_packs/astra_d11_doctrine_pack_v0_1/D11-03_hidden_state_rumor_secrecy_misinformation_presentation.md` for draft hidden-state, rumor, secrecy, misinformation, and presentation reference material.
- `docs/doctrine/native_design/d_series/source_packs/D12_time_action_cadence_encounter_and_turn_procedure_doctrine_pack/D12_doctrine_pack/D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md` for draft checkpoint, cost, consequence timing, and handoff source material.
- `docs/doctrine/native_design/d_series/source_packs/D13_downtime_projects_recovery_crafting_and_long_task_doctrine_pack/D13_doctrine_pack/D13-02_project_creation_requirement_discovery_commitment_and_interval_setup.md` for draft project requirement discovery and interval setup source material.
- `docs/doctrine/native_design/d_series/source_packs/D14_exploration_travel_navigation_and_discovery_doctrine_pack/D14_doctrine_pack/D14-05_travel_risk_resource_pressure_hazards_encounters_and_transition_handoffs.md` for draft travel-risk, access pressure, hazard, encounter, and transition-handoff source material.
- `docs/doctrine/native_design/d_series/source_packs/D15_faction_relationship_domain_and_institutional_operations_doctrine_pack/D15_doctrine_pack/D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md` and `docs/doctrine/native_design/d_series/source_packs/D15_faction_relationship_domain_and_institutional_operations_doctrine_pack/D15_doctrine_pack/D15-01_organized_actors_standing_pressure_obligations_claims_and_operation_anatomy.md` for draft organized-actor, standing, pressure, obligation, claim, relationship, domain, and institutional operation source material.
- `docs/doctrine/native_design/d_series/source_packs/D16_opposition_creature_encounter_and_hazard_construction_doctrine_pack/D16_doctrine_pack/D16-00_opposition_creature_encounter_and_hazard_construction_owner_boundaries.md` for draft opposition, hazard, enforcement squad, raid, army, and encounter-construction boundary material.
- `docs/doctrine/native_design/d_series/source_packs/D17_economy_acquisition_inventory_reward_and_requisition_doctrine_pack/D17_doctrine_pack/D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md` for draft requisition, upkeep, consumption, value-sink, and economic-pressure source material.
- `docs/doctrine/native_design/d_series/source_packs/D18_structural_time_campaign_continuity_arc_season_and_horizon_doctrine_pack/D18_doctrine_pack/D18-00_structural_time_campaign_continuity_arc_season_and_horizon_owner_boundaries.md` for draft structural time, campaign continuity, arc, season, and horizon owner-boundary source material.
- `docs/doctrine/native_design/d_series/source_packs/D19_cross_pack_integration_conflict_audit_and_conversion_readiness_capstone_pack/D19_capstone_doctrine_pack/D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md` for draft record-shape registry and schema handoff control source material, while B09 must not invent final schema fields.

## 2. Owner layer

B09 belongs to Batch B operational doctrine. It routes procedure between upstream B01-B08 operational procedure, the C00 schema handoff control surface, future C-family schema families, source-local donor quarantine, and later social, relationship, faction, institution, law, economy, information, hidden-state presentation, opposition, campaign-time, runtime, canon, and training owners.

B09 may identify that social/faction/contact/institution pressure exists and identify a likely owner handoff, but it must not perform that owner's work. When B09 cannot identify a valid owner or schema family, it must mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` instead of inventing Astra schema, final mechanics, runtime social state, runtime faction state, runtime relationship state, runtime law databases, hidden truth, canon, sourcebook faction prose, or live-play narration.

## 3. What B09 owns

B09 owns doctrine-level operational procedure for:
- social/faction/contact/institutional intake after B01-B08 produce social, factional, legal, institutional, standing, access, claim, obligation, authority, or relationship pressure;
- social-contact classification;
- organized-actor and institutional-contact classification;
- individual contact vs organized actor vs institution vs domain authority separation;
- standing review and standing-pressure routing;
- public/private/hidden/source-local relationship-state boundary handling;
- obligation, claim, favor, debt, contract, oath-like duty, patron demand, treaty duty, warrant, permit, license, access right, sanction, and jurisdiction routing;
- social intent and method classification;
- leverage, cost, risk, consequence, and visibility checkpoint procedure;
- negotiation, diplomacy, persuasion, intimidation, deception, mediation, appeal, petition, bargaining, threat, bribe, blackmail, sponsorship, patronage, and source-local contact routing as procedure, not final social mechanics;
- authority, law, permit, license, restricted access, inspection, checkpoint, border, guild/sect/corporate/temple/academy/kingdom/polity/agency contact routing;
- faction/institution response trigger identification;
- institutional operation trigger routing;
- contact escalation to focused scene, structured encounter, project, travel, value-flow, investigation, or campaign-scale owner;
- rumor, propaganda, misinformation, secrecy, public claim, hidden agenda, and safe-presentation handoff to information/presentation owners;
- social/faction/contact state-delta routing and social/faction/contact/institutional state-delta routing;
- B09-to-C00/C-family handoff references when social/faction/contact/institution handling produces conversion records;
- source-local donor reaction-roll/reputation/renown/faction-rank/contact/heat/wanted/standing/kingdom-turn/social-conflict systems quarantine and escalation rules;
- examples of good and bad B09 usage; and
- minimum acceptance criteria for B09.

## 4. What B09 must not own

B09 must not define, create, require, or promote:
- final social schema, final faction schema, final relationship schema, final reputation schema, final law schema, final institution schema, final contact schema, final domain schema, C-family schema fields, or C01-C14 schema contents;
- final social mechanics, final social-combat system, final reputation math, final attitude tables, final reaction rolls, final morale rules, final faction clocks, final influence tracks, final heat/wanted systems, final law code, final license/permit system, final faction rank system, final renown system, final contact rules, final patron rules, final treaty system, final debt economy, final favor economy, final domain-turn procedure, final kingdom-turn procedure, final faction-turn procedure, final institutional AI behavior, final NPC motivation/personhood, final actor substrate, final hidden-agenda truth, final rumor truth, final propaganda truth, or final social narration/presentation behavior;
- final sourcebook faction prose, final faction statblocks, final political map, or final war/army/raid/opposition construction;
- runtime social state, runtime faction state, runtime relationship state, runtime reputation ledger, runtime law database, runtime faction AI, runtime entity/component/event/state schemas, persistent campaign state, command lifecycle implementation, context packet compiler, hidden-information runtime state, runtime state/event/command lifecycle ownership, or live-play narration behavior;
- final canon promotion, accepted lexicon terms, sourcebook prose, or donor social/faction/reputation/law/contact systems as Astra defaults.

## 5. Non-collapse rule

B09 keeps these boundaries separate:
- A social contact is not automatically a social roll.
- A faction is not a giant NPC by default.
- An institution is not arbitrary AI.
- Standing is not a single reputation score.
- Reputation is not truth.
- Public standing is not private standing.
- Legal status is not moral truth.
- A rumor is not confirmed fact.
- Propaganda is not neutral narration.
- A hidden agenda is not player-facing truth.
- A claim is not ownership by default.
- An obligation is not payment by default.
- A favor is not currency by default.
- A permit is not universal access.
- A license is not universal legality.
- A patron is not a vendor.
- A faction response is not automatically a faction clock.
- A social pressure is not automatically a scene.
- A negotiation is not a social-combat system.
- A successful contact is not automatic access.
- Refusal is not automatic hostility.
- Bribery, blackmail, intimidation, and deception must route risk, law, standing, exposure, and hidden-state consequences rather than become generic modifiers.

B09 may identify social/faction/institution pressure, but it must not define final social mechanics, reputation math, law codes, faction AI, faction clocks, reaction rolls, social-combat systems, runtime social state, or sourcebook faction prose. B09 may route scene-level interaction to B01/B02/D12, but it must not own scene cadence, final action resolution, or live-play dialogue behavior. B09 may route value/debt/payment/bribe/reward/requisition questions to B05/D17-style owners, but it must not define final economy law or debt-value math. B09 may route rumor, propaganda, secrecy, hidden agenda, misinformation, and public/private knowledge to D10/D11-style owners, but it must not decide actual hidden truth or presentation. B09 may route opposition, raids, armies, enforcement squads, combat encounter pressure, or institutional force to D16-style owners, but it must not build statblocks, war math, or encounter construction. B09 may route long-horizon faction/institutional consequences to D18-style owners, but it must not define final campaign-scale political pacing.

Every meaningful social/faction/contact/institutional event must route at least one delta to a recognized owner or explicitly produce a no-delta/quarantine/escalation/transition result. Batch B procedure may identify that a C-family handoff is needed, but it must not invent C-family fields. Missing schema coverage must produce `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` rather than improvised schema. Live-play behavior must not consume B09 procedure as runtime authority without later runtime validation.

## 6. Social contact, organized actor, institution, standing, pressure, obligation, claim, and operation definitions

B09 uses doctrine vocabulary only; these terms are not accepted lexicon terms or final schemas.

- `social_contact`: any procedural moment where an actor, group, public, organized actor, or institution is engaged, invoked, avoided, challenged, petitioned, influenced, informed, threatened, deceived, bargained with, or routed around. A social contact is not automatically a social roll.
- `individual_contact`: contact with a person or persona-bearing actor; D08-style actor personhood and actor substrate owners retain personhood, identity, body, substrate, and motivation boundaries.
- `organized_actor`: a structured social body capable of policy, memory, access control, claim enforcement, response, or institutional behavior. A faction is not a giant NPC by default.
- `institution`: an organized actor whose behavior is mediated by office, jurisdiction, rule, role, charter, temple order, guild law, corporate policy, academy procedure, agency mandate, kingdom bureaucracy, market authority, law office, station authority, or comparable structure. An institution is not arbitrary AI.
- `domain_authority`: an organized actor or office that claims jurisdiction over territory, market, law, travel route, site, resource, border, checkpoint, station, polity, or domain-scale procedure.
- `standing`: a relationship posture or recognized status between a subject and a contact, public, faction, institution, or authority. Standing is not a single reputation score, and public standing is not private standing.
- `pressure`: a social, factional, legal, institutional, reputational, access, obligation, claim, or authority tension that may remain latent, surface, escalate, decay, transfer, convert to an operation, or retire.
- `obligation`: a duty, promise, oath-like duty, contract, treaty duty, patron demand, favor owed, debt-like duty, service expectation, permit condition, license condition, sanction condition, or lawful requirement. An obligation is not payment by default.
- `claim`: an asserted, recognized, contested, rejected, enforced, suspended, transferred, settled, violated, escalated, or retired assertion over access, authority, ownership, debt, duty, title, jurisdiction, salvage, reward, custody, privilege, or right. A claim is not ownership by default.
- `favor`: a bounded social or institutional concession or assistance request. A favor is not currency by default.
- `debt`: a routed obligation or value-pressure construct that may require B05/D17-style value flow review. Debt is not final debt economy.
- `operation`: a routed faction/institution/domain/law/market/campaign response trigger whose scope belongs to D15/D18-style owners unless it remains a B01 scene, B02 action, B05 value-flow, B06/B07 project, B08 travel, D10/D11 information, D16 opposition, or C00 schema handoff.

## 7. Social/faction/contact intake procedure

When B01-B08 produce social, factional, legal, institutional, standing, access, claim, obligation, authority, or relationship pressure, B09 intake proceeds:

1. **Confirm upstream trigger**: cite the B01 scene/activity, B02 action declaration, B03 object leverage, B04 custody/access, B05 value/requisition, B06 project, B07 research/training/preparation, or B08 travel/site-entry source that generated contact pressure.
2. **Name the apparent contact**: identify whether the pressure involves an individual, group, organized actor, faction, institution, domain authority, law authority, market authority, public, hidden contact, source-local contact, or unknown contact.
3. **Separate social contact from social roll**: decide whether no roll, owner-routed resolution, focused scene, structured encounter, project, value-flow, travel access, investigation, or campaign-scale handoff is needed.
4. **Identify social intent and method**: classify whether the event is a request, negotiation, diplomacy, persuasion, intimidation, deception, mediation, petition, bargain, threat, bribe, blackmail, sponsorship, patronage, treaty, favor, debt settlement, claim contest, access request, permit request, license request, rumor action, or source-local social action.
5. **Review standing, pressure, obligation, claim, authority, and access** without collapsing them into one reputation score.
6. **Review public/private/hidden/source-local boundaries** before stating any player-facing or doctrine-facing conclusion.
7. **Run leverage, cost, risk, consequence, and visibility checkpoints** before routing to an owner.
8. **Assign outcome state and delta routing status**: produce `no_delta_required`, `owner_routed`, `transition_note`, `source_local_retained_effect`, `quarantined_unresolved_delta`, or `owner_file_escalation`.

## 8. Contact type and organized-actor classification

Use these B09 contact types as doctrine vocabulary, not final contact schema: `individual_contact`, `group_contact`, `organized_actor_contact`, `faction_contact`, `institutional_contact`, `domain_authority_contact`, `law_authority_contact`, `market_authority_contact`, `guild_contact`, `sect_contact`, `corporate_contact`, `temple_contact`, `academy_contact`, `kingdom_polity_contact`, `agency_contact`, `patron_contact`, `crew_or_party_contact`, `public_contact`, `hidden_contact`, `source_local_contact`, `unknown_contact`.

Use these organized-actor types as doctrine vocabulary, not final faction schema: `faction`, `institution`, `guild`, `sect`, `corporation`, `polity`, `kingdom`, `agency`, `order`, `cult`, `clan`, `family`, `academy`, `temple`, `patron_network`, `market_authority`, `law_office`, `station_authority`, `navy_or_military`, `rebel_cell`, `criminal_syndicate`, `player_organization`, `public`, `source_local_organization`, `unknown_organization`.

Classification procedure:
1. If the pressure is face-to-face with one person, classify `individual_contact` but route actor personhood or actor substrate questions away from B09 to D08-style owners.
2. If a group acts informally, classify `group_contact` or `crew_or_party_contact` and avoid treating it as an institution unless office, charter, hierarchy, law, standing, or recognized authority matters.
3. If a structured body acts through policy, memory, access, claim, resource, sanction, or jurisdiction, classify `organized_actor_contact` and assign an organized-actor type.
4. If the contact is an office, checkpoint, border, inspection, permit desk, license authority, temple tribunal, academy board, guild hall, corporation, agency, kingdom, polity, station authority, market authority, or law office, classify the institutional or domain authority contact explicitly.
5. If the donor system names a source-local organization whose Astra equivalent is not defined, classify `source_local_contact` and `source_local_organization`, then quarantine or escalate.

## 9. Standing, pressure, obligation, claim, authority, and access review

B09 reviews but does not calculate final standing, reputation, law, or access systems.

Standing-state vocabulary: `trusted`, `favored`, `allied`, `patronized`, `neutral`, `watched`, `scrutinized`, `indebted`, `obligated`, `rivalrous`, `hostile`, `banned`, `wanted`, `protected`, `sponsored`, `licensed`, `recognized`, `public`, `private`, `hidden`, `conditional`, `temporary`, `revoked`, `source_local`, `unknown`.

Pressure-state vocabulary: `latent`, `active`, `escalating`, `decaying`, `suppressed`, `transferred`, `surfaced`, `converted_to_operation`, `converted_to_scene`, `converted_to_project`, `converted_to_conflict`, `resolved`, `retired`, `source_local`, `unknown`.

Obligation-state vocabulary: `none`, `owed`, `invoked`, `partially_paid`, `paid`, `deferred`, `contested`, `transferred`, `forgiven`, `defaulted`, `escalated`, `retired`, `source_local`, `unknown`.

Claim-state vocabulary: `none`, `asserted`, `recognized`, `contested`, `rejected`, `enforced`, `suspended`, `transferred`, `settled`, `violated`, `escalated`, `retired`, `source_local`, `unknown`.

Review checkpoints:
- separate public standing, private standing, hidden standing, legal status, moral truth, public claim, private motive, hidden agenda, reputation, rumor, propaganda, and misinformation;
- identify whether access is requested, access granted, access limited, access denied, access revoked, or access owner-routed;
- identify whether a warrant, permit, license, access right, sanction, inspection, checkpoint, border, guild rule, sect rule, corporate rule, temple rule, academy rule, kingdom law, polity rule, or agency procedure matters;
- if standing math, reputation math, attitude tables, reaction rolls, heat/wanted systems, faction rank, renown, contact rules, patron rules, treaty systems, debt economy, favor economy, or law code is needed, route to future owners or quarantine as source-local rather than defining it in B09.

## 10. Public/private/hidden/source-local relationship-state handling

B09 must handle relationship-state boundaries without creating runtime relationship state.

- `public` handling: records public standing, public claims, public sanctions, visible access, public rumor, public propaganda, official license/permit outcomes, and public-facing consequences as owner-routed doctrine notes.
- `private` handling: records private standing, private favor/debt pressure, private patronage, private obligation, private negotiation posture, and concealed preference as owner-routed doctrine notes, not player-facing truth by default.
- `hidden` handling: records hidden standing, hidden agenda pressure, hidden relationship facts, hidden authority motive, secret patronage, concealed law enforcement intent, or secret institutional purpose only as protected hidden-state handoff to D10/D11-style owners.
- `source_local` handling: keeps donor relationship, contact, rank, heat, wanted, renown, reputation, reaction, kingdom-turn, faction-turn, or social-conflict artifacts source-local until Astra owners accept or reject them.

Public standing is not private standing, hidden standing is not narration, reputation is not truth, a rumor is not confirmed fact, propaganda is not neutral narration, misinformation may be consequential without being true, and a hidden agenda is not player-facing truth.

## 11. Social intent, method, leverage, cost, risk, and visibility checkpoints

Social-intent vocabulary: `request_access`, `request_information`, `negotiate`, `bargain`, `persuade`, `intimidate`, `deceive`, `mediate`, `petition`, `appeal`, `threaten`, `bribe`, `blackmail`, `call_in_favor`, `settle_debt`, `invoke_obligation`, `contest_claim`, `assert_claim`, `repair_standing`, `worsen_standing`, `seek_patronage`, `offer_sponsorship`, `request_permit`, `request_license`, `pass_checkpoint`, `avoid_scrutiny`, `spread_rumor`, `suppress_rumor`, `expose_scandal`, `recruit_support`, `defect_or_betray`, `formal_diplomacy`, `treaty_or_pact`, `source_local_social_action`, `unknown_intent`.

Risk/exposure families: `social_exposure`, `legal_exposure`, `reputational_exposure`, `faction_attention`, `public_attention`, `hidden_agenda_surface`, `rumor_distortion`, `misinformation_risk`, `obligation_risk`, `claim_dispute`, `debt_escalation`, `favor_complication`, `access_revocation`, `patron_pressure`, `authority_scrutiny`, `sanction_risk`, `enforcement_risk`, `market_access_risk`, `travel_access_risk`, `conflict_escalation`, `source_local_risk`, `owner_file_gap`.

Checkpoint procedure:
1. **Intent checkpoint**: state what the actor wants without converting intent into a final social move.
2. **Method checkpoint**: state whether the method is diplomacy, persuasion, intimidation, deception, mediation, petition, bargaining, threat, bribe, blackmail, appeal, sponsorship, patronage, formal treaty, or source-local contact routing.
3. **Leverage checkpoint**: identify evidence, proof, status, legal authority, market access, object custody, value, favor, debt, claim, obligation, route access, sponsorship, public attention, or hidden information used as leverage; then route that leverage to the relevant owner.
4. **Cost checkpoint**: identify visible cost, committed cost, opportunity cost, value cost, standing cost, obligation cost, legal cost, exposure cost, or hidden-state cost without defining final cost math.
5. **Risk checkpoint**: identify risk/exposure families before any resolution or owner handoff.
6. **Visibility checkpoint**: mark public, private, hidden, split_visibility, protected_hidden, rumor_claim, misinformation_claim, propaganda_claim, source_local, owner_routed, or unknown handling.

## 12. Negotiation, diplomacy, persuasion, intimidation, deception, mediation, petition, bargaining, threat, bribe, and blackmail routing

B09 routes these procedures without creating a social-combat system, attitude table, reaction roll, or universal modifier.

- `negotiate`, `formal_diplomacy`, `mediate`, `petition`, `appeal`, and `bargain` route to B01/B02 when immediate scene/action procedure dominates, to D15-style owners when organized-actor procedure dominates, to D18-style owners when campaign horizon pressure dominates, and to C00 when conversion records are produced.
- `persuade` routes to B02 if an action declaration and resolution trigger are needed; it does not become final persuasion mechanics inside B09.
- `intimidate` and `threaten` must route social exposure, legal exposure, authority scrutiny, sanction risk, enforcement risk, faction attention, hidden agenda surface, and conflict escalation instead of becoming generic modifiers.
- `deceive` must route misinformation risk, hidden-state presentation, proof, rumor distortion, legal exposure, and later truth-record owners.
- `bribe` must route B05/D17-style value flow, law/authority review, standing risk, public/private visibility, exposure, and sanction risk.
- `blackmail` must route hidden-state presentation, information truth/record, legal exposure, standing pressure, claim dispute, faction attention, and fallout review.
- Source-local social moves, donor social-conflict moves, donor reaction rolls, donor contact rolls, or donor reputation checks are quarantined or owner-routed instead of imported as Astra defaults.

## 13. Authority, jurisdiction, law, permit, license, restriction, inspection, and sanction routing

B09 reviews legal and authority pressure without defining final law schema, final law code, final license/permit system, or runtime law database.

Procedure:
1. Identify the authority type: `law_authority_contact`, `domain_authority_contact`, `market_authority_contact`, `guild_contact`, `sect_contact`, `corporate_contact`, `temple_contact`, `academy_contact`, `kingdom_polity_contact`, `agency_contact`, or `station_authority`.
2. Identify jurisdiction: territory, route, station, market, guild hall, temple, academy, polity, border, checkpoint, inspection zone, restricted site, asset, office, claim, contract, treaty, warrant, permit, license, or sanction.
3. Separate legal status from moral truth: legal status is not moral truth.
4. Route permit and license outcomes: a permit is not universal access, and a license is not universal legality.
5. Route restricted access to B04/B05/B08 when custody, market, requisition, route, site entry, inspection, border, or checkpoint procedure dominates.
6. Route enforcement squads, raids, armies, hazards, combat encounter pressure, or war/opposition construction to D16-style owners rather than building statblocks.
7. Route long-horizon law, sanction, policy, treaty, domain, or institution consequences to D15/D18-style owners or to C00 if conversion records are required.

## 14. Patronage, sponsorship, alliance, rivalry, treaty, favor, debt, and obligation routing

B09 treats patronage, sponsorship, alliance, rivalry, treaty, favor, debt, and obligation as routed pressure, not final economies or final relationship mechanics.

- A patron is not a vendor; patronage may create standing, obligation, claim, access, protection, sponsorship, pressure, sanction risk, or hidden agenda review.
- Sponsorship may route to access rights, project sponsorship, market access, travel access, institutional standing, permit/license review, or campaign horizon pressure.
- Alliance and rivalry may route to standing, public/private relationship, faction response, institutional operation, hidden-state review, or D18-style campaign continuity; B09 does not define alliance mechanics.
- Treaty or pact pressure may route obligation, claim, jurisdiction, domain authority, law authority, campaign horizon, and schema review; B09 does not define final treaty system.
- Favor and debt pressure may route to B05/D17-style value flow or D15-style obligation procedure, but B09 does not define final debt economy or final favor economy.
- Obligations may be `owed`, `invoked`, `partially_paid`, `paid`, `deferred`, `contested`, `transferred`, `forgiven`, `defaulted`, `escalated`, `retired`, `source_local`, or `unknown`; B09 does not define final obligation math.

## 15. Faction/institution response trigger procedure

Operation-trigger vocabulary: `standing_change`, `pressure_surface`, `obligation_invoked`, `claim_asserted`, `claim_contested`, `access_requested`, `access_denied`, `law_contact`, `permit_or_license_review`, `sanction_threat`, `faction_response`, `institution_response`, `domain_authority_response`, `rumor_or_propaganda_pressure`, `hidden_agenda_pressure`, `public_scene_pressure`, `project_sponsorship_pressure`, `travel_access_pressure`, `market_access_pressure`, `enforcement_pressure`, `conflict_escalation_pressure`, `campaign_horizon_pressure`, `source_local_operation`, `owner_file_gap`.

Trigger procedure:
1. Identify whether the contact created or changed standing, pressure, obligation, claim, access, authority, legal exposure, public attention, hidden-state pressure, market access pressure, travel access pressure, or enforcement pressure.
2. Decide whether the response remains no_delta_required, becomes a B01 active scene, B02 action, B05 value-flow question, B06/B07 project, B08 travel/site-access transition, D10/D11 information or presentation handoff, D15-style faction/institution operation, D16-style opposition/enforcement construction, D18-style campaign horizon pressure, or C00 schema handoff.
3. Mark a faction response without automatically starting a faction clock.
4. Mark an institutional response without treating the institution as arbitrary AI.
5. If no owner exists, use `owner_file_gap`, quarantine, escalation, `human_review`, or `defer_until_schema_exists`.

## 16. Institutional operation trigger routing

An institutional operation trigger routes to owner files when an institution, authority, market, guild, sect, corporation, temple, academy, kingdom, polity, agency, patron network, law office, station authority, navy_or_military, rebel_cell, criminal_syndicate, player_organization, or public body acts beyond immediate contact.

Institutional operation trigger routing includes:
- `institution_response` for office, policy, procedure, access, sanction, investigation, inspection, or review board actions;
- `domain_authority_response` for territorial, border, route, checkpoint, station, kingdom, polity, market, or jurisdiction actions;
- `law_contact`, `permit_or_license_review`, and `sanction_threat` for law/authority review;
- `project_sponsorship_pressure` for long-task or sponsored work routed to B06/B07/D13-style owners;
- `travel_access_pressure` for border, route, checkpoint, site entry, restricted access, or travel permit pressure routed to B08/D14-style owners;
- `market_access_pressure` for requisition, rationing, scarcity, license, market authority, bribe, or value-sink pressure routed to B05/D17-style owners;
- `enforcement_pressure` and `conflict_escalation_pressure` for D16-style opposition/hazard/enforcement routing;
- `campaign_horizon_pressure` for D18-style structural time and campaign continuity routing.

## 17. Rumor, propaganda, misinformation, secrecy, and hidden-agenda presentation handoff rules

B09 may identify rumor, propaganda, misinformation, secrecy, hidden agenda, public claim, private standing, hidden standing, and social pressure, but it must not decide actual hidden truth or final presentation.

Handoff rules:
- Rumor routes to D10/D11-style information/presentation owners because a rumor is not confirmed fact.
- Propaganda routes to D10/D11-style owners because propaganda is not neutral narration.
- Misinformation routes to information truth/record and hidden-state presentation owners because misinformation may have social consequence without being true.
- Secrecy routes to hidden-state presentation owners and must not reveal hidden agenda, hidden relationship, hidden faction intent, hidden legal motive, or true culprit.
- Public claim routes to information records, standing review, claim review, law/authority review, and C00 if a conversion record is produced.
- Hidden agenda pressure routes to protected hidden handling; a hidden agenda is not player-facing truth.

## 18. Contact escalation, de-escalation, refusal, compliance, compromise, and fallout routing

Outcome-state vocabulary: `no_delta_required`, `contact_established`, `contact_refused`, `access_granted`, `access_limited`, `access_denied`, `standing_improved`, `standing_worsened`, `standing_complicated`, `obligation_created`, `obligation_invoked`, `obligation_settled`, `obligation_defaulted`, `claim_recognized`, `claim_contested`, `claim_rejected`, `favor_created`, `favor_spent`, `debt_created`, `debt_settled`, `scrutiny_increased`, `scrutiny_decreased`, `rumor_spread`, `rumor_suppressed`, `misinformation_routed`, `propaganda_routed`, `hidden_agenda_pressure_routed`, `permit_granted`, `permit_denied`, `license_granted`, `license_denied`, `sanction_triggered`, `enforcement_triggered`, `faction_operation_triggered`, `institutional_operation_triggered`, `active_scene_triggered`, `project_triggered`, `conflict_triggered`, `owner_routed`, `transition_note`, `source_local_retained_effect`, `quarantined_unresolved_delta`, `owner_file_escalation`.

Routing rules:
- Escalation may convert pressure to scene, structured encounter, project, travel access, value-flow, investigation, conflict, faction operation, institutional operation, enforcement, or campaign-horizon owner.
- De-escalation may route to no_delta_required, contact_established, contact_refused, access_limited, scrutiny_decreased, obligation_deferred, claim_contested, compromise, owner_routed, or transition_note.
- Refusal is not automatic hostility; refusal may produce no delta, access denial, standing complication, private pressure, public pressure, legal review, or source-local retained effect.
- Compliance is not automatic success; compliance may still require permit/license review, authority review, payment/requisition review, proof routing, inspection, or hidden-state consequences.
- Compromise may create obligation, favor, debt, claim, limited access, conditional standing, temporary standing, sponsor pressure, or future project owner handoff.
- Fallout must route standing, pressure, law, access, claim, obligation, rumor, propaganda, misinformation, hidden agenda, enforcement, campaign horizon, or schema review to owner files.

## 19. Social/faction/contact state-delta routing

B09 produces doctrine-facing routing, not runtime state. Every meaningful social/faction/contact/institutional event must route at least one delta to a recognized owner or explicitly produce `no_delta_required`, `transition_note`, `source_local_retained_effect`, `quarantined_unresolved_delta`, or `owner_file_escalation`.

State-delta routing procedure:
1. Identify affected construct: contact, standing, pressure, obligation, claim, access, authority, permit, license, sanction, rumor, propaganda, misinformation, hidden agenda, patronage, sponsorship, alliance, rivalry, treaty, favor, debt, or operation trigger.
2. Identify owner: B01, B02, B03, B04, B05, B06, B07, B08, C00/C-family, D08-style actor owner, D10/D11-style information/presentation owner, D12/D13/D14/D15/D16/D17/D18/D19-style draft reference owner, future social/faction/law/runtime/canon owner, source-local review, schema review, canon review, runtime review, or human review.
3. Identify visibility: public, private, hidden, split_visibility, protected_hidden, rumor_claim, misinformation_claim, propaganda_claim, source_local, owner_routed, or unknown.
4. Identify delta routing status: `no_delta_required`, `owner_routed`, `transition_note`, `source_local_retained_effect`, `quarantined_unresolved_delta`, or `owner_file_escalation`.
5. If no safe owner exists, mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists`.

## 20. Owner-file handoff rules

B09 owner handoffs must preserve boundaries:
- B01 handles scene/activity/encounter transitions; B09 must not own scene cadence.
- B02 handles action declaration, cost commitment, and resolution trigger; B09 must not own final action resolution.
- B03 handles item/gear/equipment/object-system construct and asset use; B09 must not own object use.
- B04 handles inventory, storage, custody, access, burden, lawful loss, and recovery; B09 must not own inventory/custody.
- B05 handles acquisition, reward, requisition, value flow, market access, scarcity, upkeep, and value sink; B09 must not own value flow or economy math.
- B06 handles project-centered interval work, crafting, salvage, repair, modification, upgrade, requirements, progress, complications, and project outputs; B09 must not own project procedure.
- B07 handles recovery, training, research, preparation, readiness, proof routing, desired-outcome routing, and non-object project outputs; B09 must not own recovery/training/research.
- B08 handles travel, exploration, navigation, discovery, scouting, mapping, site entry, watches, ambush exposure, travel pressure, and transition handoffs; B09 must not own travel/exploration.
- D08-style owners handle actor personhood, actor substrate, identity, body, form, motivation/personhood boundaries; B09 must not own final NPC motivation/personhood or final actor substrate.
- D10/D11-style owners handle information truth/record, public knowledge, rumor, secrecy, misinformation, propaganda, hidden-state presentation, and safe presentation.
- D15-style owners handle organized-actor, standing, pressure, obligation, claim, operation anatomy, relationship, faction, institution, domain, diplomacy, and institutional operation draft source material.
- D16-style owners handle opposition, hazard, enforcement, raid, army, war, and encounter construction.
- D17-style owners handle value, requisition, upkeep, consumption, value sinks, economic pressure, and debt/favor value routing.
- D18-style owners handle campaign horizon, structural time, campaign continuity, arc, season, and long-horizon institutional consequences.
- D19-style owners handle record-shape registry warnings, schema handoff control, and not-final-schema governance.

## 21. Batch B to C00/C-family handoff rules

C00 remains the schema handoff control surface. B09 may identify that a future C-family handoff is needed, but B09 must not invent C-family fields, C01-C14 schema contents, runtime schemas, backend contracts, database rows, command objects, event logs, context packet formats, persistent campaign state, or final social/faction/contact/law/reputation/domain schemas.

The following block is lightweight and doctrine-facing only. It must not be treated as a runtime schema.

```yaml
batch_b_to_c_handoff:
  target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema
  schema_status: not_started | stub_index_only | minimum_unlock_draft | tested_minimum | stable_for_family | stable_cross_family | superseded | deprecated
  required_c00_base_fields: true
  source_evidence_refs_required: true
  construct_refs_required: true
  outcome_refs_required: true
  provenance_refs_required: true
  source_local_boundary_required_if_applicable: true
  rejected_donor_elements_required_if_applicable: true
  canon_eligibility_required: true
  review_routing_required: true
  unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists
```

This B09-specific block is also lightweight and doctrine-facing only. `social_faction_contact_routing_note` is doctrine-facing only. It is not a runtime schema, not a backend event, not a command object, not a C-family record, not a social-state database row, not a faction-state row, not a relationship ledger, not a reputation ledger, not a law database row, not a faction AI instruction, not a social-combat move, not a reaction table, not a faction clock, not a sourcebook faction entry, not final mechanics, not a database contract, not an event log, not a context packet format, not persistent campaign state, not canon, and not player-facing rule text.

```yaml
social_faction_contact_routing_note:
  contact_type: individual_contact | group_contact | organized_actor_contact | faction_contact | institutional_contact | domain_authority_contact | law_authority_contact | market_authority_contact | guild_contact | sect_contact | corporate_contact | temple_contact | academy_contact | kingdom_polity_contact | agency_contact | patron_contact | crew_or_party_contact | public_contact | hidden_contact | source_local_contact | unknown_contact
  organized_actor_type: faction | institution | guild | sect | corporation | polity | kingdom | agency | order | cult | clan | family | academy | temple | patron_network | market_authority | law_office | station_authority | navy_or_military | rebel_cell | criminal_syndicate | player_organization | public | source_local_organization | unknown_organization | none
  standing_state: trusted | favored | allied | patronized | neutral | watched | scrutinized | indebted | obligated | rivalrous | hostile | banned | wanted | protected | sponsored | licensed | recognized | public | private | hidden | conditional | temporary | revoked | source_local | unknown
  pressure_state: latent | active | escalating | decaying | suppressed | transferred | surfaced | converted_to_operation | converted_to_scene | converted_to_project | converted_to_conflict | resolved | retired | source_local | unknown
  obligation_state: none | owed | invoked | partially_paid | paid | deferred | contested | transferred | forgiven | defaulted | escalated | retired | source_local | unknown
  claim_state: none | asserted | recognized | contested | rejected | enforced | suspended | transferred | settled | violated | escalated | retired | source_local | unknown
  social_intent: request_access | request_information | negotiate | bargain | persuade | intimidate | deceive | mediate | petition | appeal | threaten | bribe | blackmail | call_in_favor | settle_debt | invoke_obligation | contest_claim | assert_claim | repair_standing | worsen_standing | seek_patronage | offer_sponsorship | request_permit | request_license | pass_checkpoint | avoid_scrutiny | spread_rumor | suppress_rumor | expose_scandal | recruit_support | defect_or_betray | formal_diplomacy | treaty_or_pact | source_local_social_action | unknown_intent
  operation_trigger: standing_change | pressure_surface | obligation_invoked | claim_asserted | claim_contested | access_requested | access_denied | law_contact | permit_or_license_review | sanction_threat | faction_response | institution_response | domain_authority_response | rumor_or_propaganda_pressure | hidden_agenda_pressure | public_scene_pressure | project_sponsorship_pressure | travel_access_pressure | market_access_pressure | enforcement_pressure | conflict_escalation_pressure | campaign_horizon_pressure | source_local_operation | owner_file_gap | none
  risk_exposure_families:
    - social_exposure
    - legal_exposure
    - reputational_exposure
    - faction_attention
    - public_attention
    - hidden_agenda_surface
    - rumor_distortion
    - misinformation_risk
    - obligation_risk
    - claim_dispute
    - debt_escalation
    - favor_complication
    - access_revocation
    - patron_pressure
    - authority_scrutiny
    - sanction_risk
    - enforcement_risk
    - market_access_risk
    - travel_access_risk
    - conflict_escalation
    - source_local_risk
    - owner_file_gap
  outcome_state: no_delta_required | contact_established | contact_refused | access_granted | access_limited | access_denied | standing_improved | standing_worsened | standing_complicated | obligation_created | obligation_invoked | obligation_settled | obligation_defaulted | claim_recognized | claim_contested | claim_rejected | favor_created | favor_spent | debt_created | debt_settled | scrutiny_increased | scrutiny_decreased | rumor_spread | rumor_suppressed | misinformation_routed | propaganda_routed | hidden_agenda_pressure_routed | permit_granted | permit_denied | license_granted | license_denied | sanction_triggered | enforcement_triggered | faction_operation_triggered | institutional_operation_triggered | active_scene_triggered | project_triggered | conflict_triggered | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  public_private_hidden_handling: public | private | hidden | split_visibility | protected_hidden | rumor_claim | misinformation_claim | propaganda_claim | source_local | owner_routed | unknown
  owner_handoff_required: boolean
  owner_handoff_reason:
    - scene_or_activity_transition
    - action_cost_or_resolution
    - actor_personhood_or_substrate
    - information_truth_or_record
    - hidden_state_presentation
    - faction_institution_operation
    - law_authority_or_jurisdiction
    - value_debt_favor_or_requisition
    - inventory_custody_or_access
    - travel_route_or_site_access
    - project_sponsorship_or_long_task
    - hazard_opposition_or_enforcement
    - campaign_horizon_or_domain_evolution
    - source_local_review
    - schema_review
    - canon_review
    - runtime_review
    - human_review
  delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  note: string
```

## 22. Missing-schema fallback and quarantine/escalation

If B09 cannot safely route a social/faction/contact/institutional event to an existing owner, it must not improvise schema. Missing schema coverage must produce `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists`.

Fallback procedure:
- use `pending_schema` for future C-family or owner coverage that does not yet exist;
- use quarantine for source-local donor contact/reputation/law/faction/social-conflict systems or unsafe imported mechanics;
- use escalation when a doctrine owner boundary conflict exists;
- use `human_review` when legal, political, hidden-state, canon, runtime, or source-local implications cannot be safely resolved by doctrine routing;
- use `defer_until_schema_exists` when C-family, runtime, law, reputation, relationship, social-state, faction-state, or contact-state schema would otherwise be invented.

## 23. Source-local donor social/faction/reputation/law/contact handling

B09 keeps donor material source-local unless a later owner explicitly accepts it. Donor reaction-roll, reputation, renown, faction-rank, contact, heat, wanted, standing, kingdom-turn, faction-turn, social-conflict, attitude table, influence track, morale, patron, treaty, debt, favor, law, license, permit, legal code, faction AI, institution AI, relationship ledger, faction clock, social-combat, and domain-turn systems are not Astra defaults.

Source-local handling procedure:
1. Classify the donor artifact as `source_local_contact`, `source_local_organization`, `source_local_social_action`, `source_local_operation`, `source_local_risk`, `source_local`, or `source_local_retained_effect` as applicable.
2. Record source evidence, donor element, rejected donor elements if applicable, and source-local boundary for later C00/C-family review.
3. Route safe procedural pressure to B09 owners without importing donor math.
4. Quarantine unsafe donor mechanics, escalate owner-file gaps, use `human_review` for ambiguous conversions, or `defer_until_schema_exists` for missing schema coverage.

## 24. Runtime boundary

B09 is not runtime authority. B09 must not define runtime social state, runtime faction state, runtime relationship state, runtime reputation ledger, runtime law database, runtime faction AI, runtime entity/component/event/state schemas, hidden-information runtime state, persistent campaign state, command lifecycle implementation, context packet compiler, backend contracts, database contracts, event logs, command objects, social backend, faction backend, relationship backend, or live-play GM behavior.

Runtime systems may later validate, compile, reject, or transform B09 doctrine-facing notes, but live-play behavior must not consume B09 procedure as runtime authority without later runtime validation.

## 25. Canon boundary

B09 is not canon. It must not create final canon promotion, accepted lexicon terms, sourcebook faction prose, sourcebook prose, final faction statblocks, final political map, final law code, final faction histories, final institutional rosters, final treaties, final patron networks, final public scandals, final hidden agendas, final rumor truth, final propaganda truth, final war/army/raid/opposition construction, or final world truth.

Canon-facing consequences require canon review, C00/C-family handoff if conversion records are produced, and owner-file routing rather than B09 promotion.

## 26. Live-play/training boundary

B09 is not player-facing rule text, not live-play dialogue behavior, not live-play narration behavior, not social narration/presentation behavior, not a GM script, not a social-combat move list, not a reaction table, not a faction AI instruction, and not a training transcript.

Training or live-play adapters may later use B09 as reference material only after runtime validation and presentation-owner review. B09 examples are doctrine-facing only and must not be presented as final player text.

## 27. Examples of good and bad B09 usage

Good B09 usage:
- A party reaches a city gate after B08 site-entry procedure. B09 classifies `law_authority_contact`, reviews permit/license/access pressure, notes that a permit is not universal access, routes immediate dialogue to B01/B02, routes restricted entry to B08/B04, and routes law/sanction consequences to D15/D18-style owners or C00 if a conversion record is needed.
- A guild offers project sponsorship. B09 classifies `guild_contact`, `institutional_contact`, `seek_patronage`, and `project_sponsorship_pressure`, then routes long-task requirements to B06/B07/D13-style owners and value/favor/debt pressure to B05/D17-style owners without treating the patron as a vendor.
- A rumor about a hidden faction agenda changes public standing. B09 records `rumor_or_propaganda_pressure`, `hidden_agenda_pressure`, `standing_complicated`, and protected hidden handling, then routes truth/presentation to D10/D11-style owners without confirming rumor truth.
- A donor source uses faction rank, heat, wanted level, renown, or reaction rolls. B09 marks source-local donor social/faction/reputation/law/contact handling, quarantines donor math, and escalates for `human_review` or `defer_until_schema_exists` if no owner exists.

Bad B09 usage:
- Defining a final reputation score, social DC table, reaction roll table, or attitude table inside B09.
- Treating a faction as a giant NPC with arbitrary AI motives and immediate faction-clock ticks for every contact.
- Presenting propaganda as neutral narration or revealing a hidden agenda as player-facing truth.
- Treating a permit as universal access, a license as universal legality, a claim as ownership, an obligation as payment, a favor as currency, or a patron as a vendor.
- Creating runtime social state, runtime faction state, runtime relationship state, runtime reputation ledger, runtime law database, runtime faction AI, C-family schema fields, or C01-C14 schema contents.

## 28. Minimum tests or assertions

Minimum B09 tests or assertions should verify that:
- B09 exists at `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md`;
- all required B09 sections are present;
- B09 declares ownership and non-ownership;
- B09 references B01, B02, B03, B04, B05, B06, B07, and B08 as upstream Batch B context;
- B09 includes C00 handoff language, `batch_b_to_c_handoff`, `social_faction_contact_routing_note`, and states that the B09-specific block is doctrine-facing only;
- B09 includes contact types, organized-actor types, standing states, pressure states, obligation states, claim states, social intents, operation triggers, outcome states, and risk/exposure families;
- B09 separates social contact, social roll, individual contact, organized actor, faction, institution, domain authority, actor personhood, public standing, private standing, hidden standing, reputation, rumor, propaganda, misinformation, obligation, claim, favor, debt, permit, license, law, authority, access, social pressure, faction response, institutional operation, runtime state, and canon;
- B09 includes social/faction/contact intake, contact type classification, organized-actor classification, standing/pressure/obligation/claim review, public/private/hidden/source-local handling, social intent/method/leverage/cost/risk/visibility checkpoints, negotiation/diplomacy/persuasion/intimidation/deception/mediation/petition/bargain/threat/bribe/blackmail routing, authority/jurisdiction/law/permit/license/restriction/inspection/sanction routing, patronage/sponsorship/alliance/rivalry/treaty/favor/debt/obligation routing, faction/institution response triggers, institutional operation trigger routing, rumor/propaganda/misinformation/secrecy/hidden-agenda presentation handoff, escalation/de-escalation/refusal/compliance/compromise/fallout routing, and state-delta routing;
- B09 rejects final social schema, final faction schema, final relationship schema, final reputation schema, final law schema, final institution schema, final contact schema, final domain schema, final social mechanics, final social-combat system, final reputation math, final attitude tables, final reaction rolls, final morale rules, final faction clocks, final influence tracks, final heat/wanted systems, final law code, final license/permit system, final faction rank system, final renown system, final contact rules, final patron rules, final treaty system, final debt economy, final favor economy, final domain-turn procedure, final kingdom-turn procedure, final faction-turn procedure, final institutional AI behavior, final NPC motivation/personhood, final actor substrate, final hidden-agenda truth, final rumor truth, final propaganda truth, final social narration/presentation behavior, runtime social state, runtime faction state, runtime relationship state, runtime reputation ledger, runtime law database, and runtime faction AI;
- B09 rejects runtime state/event/command lifecycle ownership;
- B09 rejects C-family field invention and C01-C14 schema-content ownership;
- B09 rejects donor social/faction/reputation/law/contact systems as Astra defaults;
- B09 includes social/faction/contact/institutional state-delta routing;
- B09 includes source-local donor social/faction/reputation/law/contact handling, quarantine, escalation, `human_review`, and `defer_until_schema_exists`;
- B09 references D00/D02/D05/D08/D10/D11/D12/D13/D14/D15/D16/D17/D18/D19 only as draft source-pack/reference material, not final current doctrine authority;
- B09 does not require, define, create, or promote B10-B11;
- B09 does not require, define, create, or promote C01-C14; and
- no registry status is promoted to current.

## 29. Acceptance criteria

B09 is acceptable when it:
- adds a focused social/faction/contact/institutional interaction procedure after B01-B08 without reopening B01-B08 procedure;
- preserves upstream Batch B boundaries and C00 handoff boundaries;
- routes social contact without assuming a social roll;
- separates individual contact, organized actor, faction, institution, domain authority, actor personhood, public/private/hidden standing, reputation, rumor, propaganda, misinformation, obligation, claim, favor, debt, permit, license, law, authority, access, social pressure, faction response, institutional operation, runtime state, and canon;
- identifies faction/institution response triggers and institutional operation trigger routing without defining final faction clocks, faction AI, law codes, reputation math, social-combat systems, or sourcebook faction prose;
- includes doctrine-facing handoff blocks for `batch_b_to_c_handoff` and `social_faction_contact_routing_note` with explicit non-runtime status;
- handles source-local donor social/faction/reputation/law/contact systems through quarantine, escalation, `human_review`, or `defer_until_schema_exists`; and
- passes the focused B09 tests and the Batch B/C00 regression tests without promoting registry status to current.

## 30. Follow-up handoff to B10

B09 does not require, define, create, or promote B10-B11. This heading is only a durable forward handoff marker indicating that any later B10 work must preserve B09 boundaries, avoid importing B09 as final mechanics, and avoid treating B09 doctrine-facing examples as runtime state, canon, C-family schema, player-facing rules, social backend, faction backend, relationship backend, reputation ledger, law database, faction AI, or sourcebook prose.
