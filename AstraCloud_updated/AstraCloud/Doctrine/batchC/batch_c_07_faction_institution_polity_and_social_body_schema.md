# batchC_07_faction_institution_polity_and_social_body_schema.md

## Purpose and authority

This file is the **organization/social-body content family schema authority** for Batch C.

Its job is to define the Astra-native entry structure for factions, institutions, cults, guilds, agencies, embassies, sects, houses, polities, treaty bodies, patron structures, and organization-content entries generally. It is the family file that turns the common record grammar from C01 into a reusable organization schema that can survive mixed donor pressure at corpus scale without collapsing into site doctrine, social procedure, mission trees, or lore-heavy political summaries.

C07 is not an access-procedure file. It is not a diplomacy-procedure file. It is not a political history chapter. It is not a mission structure file. It is not a site file merely because organizations occupy places.

It owns:
- organization/social-body content record structure
- organizationhood/social-body doctrine for Batch C
- organization-family payload blocks on top of C01
- organization modes and routing classes
- organization scale doctrine
- organization topology doctrine
- organization class versus function versus authority-posture versus governance-model distinction
- internal structure and subordinate-body doctrine
- office, seat, portfolio, vessel, mandate, and representation posture fields
- membership topology, affiliation, and internal-access posture fields
- entry-pathway posture
- legitimacy, recognition, charter, and mandate-basis doctrine
- legitimacy-source and recognition-source posture
- jurisdiction, claim, territorial reach, reach type, and service-reach posture fields
- diplomacy/conflict/alignment and inter-body posture hooks at entry-shape level
- patronage, sponsorship, clientage, and dependent-body posture
- public posture versus internal posture versus actual operational posture
- secrecy, transparency, and disclosure posture
- resource-base posture
- service-body versus authority-body versus identity-body distinction
- nonterritorial and distributed-polity support
- organizational continuity, succession, split/merge, schism, and successor-body doctrine
- organization-site dependence and paired organization-site doctrine
- mission-generation posture
- authority-output posture and dependency-output distinction
- external embodiment posture
- organization memory/archive posture
- organization-specific derivative-threshold and boundary-control doctrine
- relationship-discipline and validation-stress doctrine for organization entries
- organization-family relationship expectations
- organization-family anti-collapse rules
- minimal abstract organization/social-body template

It does **not** own:
- organized-access procedure doctrine already owned by B12
- site/place entry structure already owned by C06
- actor-content entry structure already owned by C02
- mission/scenario structure already owned by C10
- encounter composition already owned by C09
- challenge-object schema already owned by C08
- live-play presentation behavior
- donor conversion instances as doctrine

## Why this file exists

Large donor corpora do not present social bodies in one uniform shape. Some donors pressure toward factions and guilds. Others pressure toward confederacies, councils, churches, houses, corporations, sects, agencies, embassies, capitals with representative seats, treaty bodies, patron structures, symbolic authority networks, distributed polities, or mixed umbrella organizations with subordinate branches.

Those constructs are neither:
- all simple “factions,”
- all just collections of actors,
- nor all reducible to the places they occupy.

C07 exists because Astra requires one lawful family schema for organizations and social bodies that can:
- distinguish social bodies from the sites they inhabit and the actors who represent them,
- preserve umbrella, branch, seat, mandate, legitimacy, and recognition structure,
- expose access, authority, claim, service, jurisdiction, output, and dependency posture without re-owning B12 procedure,
- support both territorial and nonterritorial social bodies,
- and route correctly when a construct is actually a place, actor, mission, or patron-linked abstract authority structure instead of an organization entry.

This file therefore treats the family center as **organizationhood and social-bodyhood**, not as donor labels like faction, guild, state, church, company, embassy, clan, or council.

## Scope boundaries and exclusions

C07 covers content entries whose dominant doctrinal function is to exist as a social body, institution, polity, representative structure, patron network, office-holding organization, or collective authority body that can claim members, offices, sites, mandates, service reach, jurisdiction, legitimacy, alliances, or conflicts while remaining a reusable content object.

That includes, where they remain organization-family content rather than actors, sites, or missions:
- factions
- guilds and institutions
- agencies and offices
- sects, cults, churches, and orders
- clans, houses, confederacies, and collectives
- cities or regional governments only insofar as the governing body itself is the record rather than the place
- embassies and representative bodies
- treaty bodies, alliances, councils, and umbrella organizations
- patron structures and sponsor-linked power bodies
- service or access-governing organizations
- organization-based exceptional content

C07 excludes:
- a building, district, guild hall, port, archive, shrine, or capital merely because an organization operates there -> C06
- a leader, representative, boss, or official merely because they embody an organization in a scene -> C02
- mission trees, campaign fronts, or scenario networks produced by an organization -> C10
- packaged encounters involving organization members -> C09
- access law, legality procedure, rank procedure, or bureaucracy procedure as such -> B12

## Organizationhood and social-body doctrine

An **organization-family record** is a content record whose primary job is to represent a social body, institution, polity, or collective authority structure that can:
- maintain membership, affiliation, office, patronage, or representational relationships
- claim, govern, contest, license, administer, sponsor, or coordinate sites, people, services, routes, or mandates
- persist as a reusable content object independent from any one site, leader, or mission
- support internal structure, branches, seats, portfolios, or subordinate bodies
- maintain legitimacy, mandate, sponsorship, or recognition posture over time

Organizationhood does not require formal legality.
Organizationhood does not require territorial sovereignty.
Organizationhood does not require that every member know every other member.
Organizationhood does not require that the body control a site directly.

Organizationhood is established by dominant function, not by donor naming convention.

## Organization modes and routing classes

C07 must support different social-body types without splitting them into unrelated families.

### Core organization modes

An organization-family record may declare one or more organization modes, with one marked primary where needed:
- `informal_faction`
- `guild_or_institution`
- `agency_or_office`
- `sect_cult_church_or_order`
- `house_clan_or_confederacy`
- `company_corporation_or_enterprise_body`
- `polity_or_governing_body`
- `treaty_council_alliance_or_umbrella_body`
- `embassy_representative_or_diplomatic_body`
- `patron_or_sponsorship_structure`
- `exceptional_social_body`

### Mode guidance

- **informal_faction**: a meaningful social body without strong formal structure.
- **guild_or_institution**: a service, profession, research, education, or mission-oriented institutional body.
- **agency_or_office**: a bureaucratic, enforcement, adjudicative, or administrative body.
- **sect_cult_church_or_order**: a belief, rite, doctrine, or oath-linked body.
- **house_clan_or_confederacy**: a kin, lineage, alliance, or aggregated sub-body structure.
- **company_corporation_or_enterprise_body**: a commercial or economically structured organization.
- **polity_or_governing_body**: a governing, state-like, or formally administrative body.
- **treaty_council_alliance_or_umbrella_body**: a multi-body alliance, council, or chartered umbrella structure.
- **embassy_representative_or_diplomatic_body**: a body whose function is representation, mediation, or foreign interface.
- **patron_or_sponsorship_structure**: a body or structure defined by sponsorship, patronage, proxy backing, or indirect authority.
- **exceptional_social_body**: a significance-bearing organization record with unusual continuity, scale, or legitimacy pressure.

## Organization scale doctrine

C07 must distinguish organizational scale from jurisdiction and reach.

### Scale families

Useful organization scales include:
- `cell_or_chapter_scale`
- `local_body`
- `district_or_city_body`
- `regional_body`
- `transregional_network`
- `polity_scale_body`
- `umbrella_or_multibody_confederation`
- `route_spanning_or_extralocal_body`

### Doctrine note

Scale answers how large the body is as a social structure. Jurisdiction answers where authority is claimed. Reach answers how far action, services, or representation extend. These are related but not identical.

## Organization topology doctrine

Large donor corpora repeatedly pressure organizational structure beyond simple hierarchy.

### Topology families

Useful organization topologies include:
- `hierarchical`
- `federal_or_confederated`
- `distributed_or_cellular`
- `chapter_based`
- `franchise_like`
- `seat_based`
- `patron_client`
- `proxy_mediated`
- `networked_without_clear_center`
- `ritual_lineage_or_transmission_chain`

### Doctrine note

A guild chapter network, cult cell web, hereditary house confederacy, translocal company, treaty council, and ritual lineage do not have the same structural failure modes or succession pressures. Topology should therefore remain explicit.

## Organization class versus function versus authority posture versus governance model doctrine

C07 must distinguish what kind of organization this is from what it primarily does, how its authority is constituted, and how its will is internally produced.

### Distinction doctrine

- **organization mode** answers what broad kind of social body this is.
- **organization function** answers what the body primarily does.
- **authority posture** answers how its authority, legitimacy, or recognized power is actually grounded.
- **governance model** answers how organizational decisions, continuity, or command are internally produced.

These axes must not be collapsed.

### Function families

Useful organizational function families include:
- `governance`
- `defense_or_security`
- `trade_or_exchange`
- `research_or_knowledge`
- `exploration_or_expansion`
- `religious_or_ritual`
- `education_or_training`
- `logistics_or_supply`
- `service_provision`
- `adjudication_or_regulation`
- `representation_or_diplomacy`
- `patronage_or_sponsorship`
- `criminal_or_shadow_operation`

### Authority posture families

Useful authority-posture families include:
- `formal_chartered`
- `customary`
- `contested`
- `recognized_but_unmandated`
- `patron_backed`
- `de_facto`
- `sovereign`
- `subordinate_charter`
- `religious_or_sacral`
- `client_or_franchise_based`

### Governance model families

Useful governance-model families include:
- `autocratic`
- `collegial`
- `elected`
- `hereditary`
- `portfolio_based`
- `rotating`
- `consensus_based`
- `ritual_or_sacral`
- `corporate_board_like`
- `opaque_or_shadow_managed`

## Service-body versus authority-body versus identity-body distinction

Not every organization should be interpreted through the same social logic.

### Body orientation classes

Useful body-orientation classes include:
- `service_body`
- `authority_body`
- `identity_body`
- `patronage_body`
- `representation_body`
- `coercive_or_security_body`
- `mixed_hybrid_body`

This prevents Astra from flattening every social body into a generic “faction that wants things.”

## Internal structure and subordinate-body doctrine

Large donor corpora repeatedly pressure umbrella bodies, branches, seat structures, subordinate arms, and representative hierarchies.

### Structure fields

Organization-family records should support:
- `internal_structure_profile`
- `parent_body_hooks`
- `subordinate_body_hooks`
- `parallel_body_hooks`
- `branch_or_division_hooks`
- `office_or_seat_topology`
- `representation_model`
- `umbrella_constituent_profile`

### Umbrella and constituent doctrine

Useful distinctions include:
- `umbrella_body`
- `constituent_body`
- `chartered_subordinate`
- `affiliate_body`
- `observer_body_or_seat`
- `provisional_member_body`
- `schismatic_rival_body`
- `absorbed_or_successor_body`

### Doctrine note

An alliance may contain branches.
A confederacy may contain constituent bands or houses.
A council may contain seats or portfolios.
A guild may contain chapters, facilities, or officer arms.
A church may contain orders, dioceses, or emissary lines.

These are not mere lore notes. They are structural organization pressures that C07 must represent lawfully.

## Office, seat, portfolio, mandate, and representation posture

Organizations are often defined not only by membership, but by who can speak or act on behalf of whom.

### Office and representation fields

Organization-family records should support:
- `office_or_role_hooks`
- `seat_structure_profile`
- `portfolio_or_domain_hooks`
- `representative_vessel_or_proxy_profile`
- `mandate_basis`
- `representation_scope`
- `representational_claim_hooks`
- `delegation_or_proxy_hooks`
- `representation_asymmetry_profile`

### Distinction doctrine

- An **office** is not always a **seat**.
- A **seat** is not always a **portfolio**.
- A **representative vessel or proxy** is not always a conventional officeholder.

### Mandate doctrine

Mandate may be:
- elected
- hereditary
- appointed
- chartered
- ritualized
- conquest-based
- customary
- provisional
- indirect
- unmandated_but_socially_accepted

This matters because large donor corpora frequently include representatives, councils, proxies, patrons, vessel-mediated offices, or advisory bodies whose legitimacy is socially real but structurally irregular.

## Membership topology, affiliation, and internal-access posture

C07 must expose organizational belonging without becoming B12 procedure.

### Membership and affiliation fields

Organization-family records should support:
- `membership_profile`
- `membership_topology_profile`
- `rank_or_status_profile`
- `entry_pathway_profile`
- `entry_requirements_hooks`
- `internal_access_tiers`
- `affiliate_or_client_hooks`
- `patronage_or_dependency_hooks`
- `expulsion_or_exclusion_hooks`

### Membership-topology doctrine

Useful membership classes include:
- `core_members`
- `officeholders`
- `initiates`
- `dependents`
- `clients`
- `franchise_holders`
- `contractors`
- `retainers`
- `protected_affiliates`
- `subordinate_bodies`
- `ceremonial_members`
- `dormant_members`
- `coerced_or_captive_members`

### Entry-pathway doctrine

Useful entry pathways include:
- `birth_or_lineage`
- `election`
- `appointment`
- `purchase_or_franchise`
- `initiation_or_rite`
- `contract`
- `conquest`
- `sponsorship`
- `patronage`
- `co_option`
- `recognition_by_peers`
- `audience_with_seat_or_office`
- `merit_or_examination`
- `emergency_or_provisional_admission`

### Doctrine note

Organizations may differentiate members, officers, affiliates, clients, retainers, initiates, representatives, franchise holders, or protected dependents. C07 should expose those postures at entry-shape level while leaving access procedure itself to B12.

## Legitimacy, recognition, charter, and mandate-basis doctrine

This is one of the most important C07 ownership zones.

### Legitimacy and recognition fields

Organization-family records should support:
- `legitimacy_profile`
- `legitimacy_source_profile`
- `recognition_profile`
- `recognition_source_profile`
- `charter_or_foundation_basis`
- `public_acceptance_posture`
- `mandate_contestation_hooks`
- `juridical_or_customary_basis`

### Legitimacy-source doctrine

Legitimacy may be grounded in:
- charter
- law
- treaty
- conquest
- custom
- sacral sanction
- hereditary recognition
- factional recognition
- public acceptance
- patron backing
- capability_or_enforcement_only
- legacy_or_continuity_claim

### Recognition-source doctrine

Recognition may come from:
- sovereign bodies
- peers
- subordinate communities
- patrons
- treaty systems
- markets
- ritual authorities
- local public acceptance

### Doctrine note

An organization may be legally chartered, tolerated, ritually accepted, regionally recognized, publicly distrusted, formally unmandated, or partially contested while still functioning as a real power body. C07 must preserve those distinctions structurally rather than flattening every organization into a neat bureaucratic institution.

## Public posture, internal posture, actual operational posture, and secrecy doctrine

Organizations are not always what they publicly claim to be.

### Posture fields

Organization-family records should support:
- `public_positioning_profile`
- `internal_self_conception_profile`
- `actual_operational_posture`
- `secrecy_transparency_disclosure_profile`

### Secrecy and disclosure doctrine

Useful secrecy/transparency classes include:
- `public_and_legible`
- `public_but_internally_opaque`
- `officially_secret`
- `deniable`
- `compartmentalized`
- `ritual_obscured`
- `partially_open_through_fronts`
- `covert_but_widely_rumored`

This allows C07 to represent shadow hierarchies, nominal republics, covert sects, front organizations, and symbolic shells without turning the file into a spy-procedure chapter.

## Jurisdiction, claim, reach type, and service reach doctrine

Organizations often matter because of where and how far they can act.

### Jurisdiction and reach fields

Organization-family records should support:
- `jurisdiction_profile`
- `reach_type_profile`
- `claim_or_stake_hooks`
- `claim_object_classes`
- `territorial_or_site_reach_hooks`
- `service_reach_profile`
- `representation_reach_profile`
- `enforcement_or_intervention_hooks`

### Reach-type doctrine

Useful reach types include:
- `territorial`
- `site_based`
- `route_based`
- `service_based`
- `symbolic_or_sacral`
- `legal_or_bureaucratic`
- `networked_or_distributed`
- `patronage_mediated`
- `diplomatic_or_representative`
- `covert_or_shadow`

### Claim-object doctrine

Organizations commonly claim:
- territory
- office
- population
- service monopoly
- route
- ritual authority
- representation mandate
- extraction rights
- legitimacy to adjudicate
- custody of relic_archive_or_resource
- protection duty
- site stewardship

### Doctrine note

A guild may serve many regions.
A confederacy may claim a seat.
A house may hold estates.
A council may speak for several territories.
A pact may claim trial grounds.
A church may exercise sacral reach far beyond its temples.

C07 should expose those organization-side reach and claim pressures without re-owning the sites themselves.

## Resource-base posture

C07 should not absorb B04, but it does need a lawful way to declare what materially sustains an organization.

### Resource-base fields

Organization-family records should support:
- `resource_base_profile`
- `continuity_support_hooks`

### Useful resource-base classes

Useful classes include:
- `dues`
- `taxation`
- `patron_subsidy`
- `conquest_or_extraction`
- `service_revenue`
- `trade`
- `donations_or_tithes`
- `tribute`
- `state_allotment`
- `black_market_revenue`
- `ritual_or_resource_conversion`
- `inheritance_or_estate_basis`

This matters because many organizations are structurally defined by how they sustain themselves.

## Diplomacy, conflict, alignment, and inter-body posture

Organizations relate to one another in structured ways.

### Inter-body fields

Organization-family records should support:
- `alliance_posture`
- `rivalry_or_conflict_hooks`
- `neutrality_or_nonalignment_profile`
- `treaty_or_obligation_hooks`
- `cooperation_or_dependency_hooks`
- `public_positioning_profile`
- `inter_body_posture_profile`

### Inter-body posture doctrine

Relations may include:
- `patron_client`
- `protector_protected`
- `suzerain_vassal`
- `franchise_franchisor`
- `recognition_dispute`
- `proxy_competition`
- `formal_noninterference`
- `tolerated_opposition`
- `embargo_or_ostracism`
- `ritual_or_doctrinal_incompatibility`
- `covert_dependence`
- `public_alliance_private_rivalry`

C07 does not need to own diplomacy procedure. It does need lawful places to declare these relations.

## Patronage, sponsorship, and dependent-body posture

Not every organization is fully sovereign in itself.

### Patronage fields

Organization-family records should support:
- `patron_structure_profile`
- `sponsorship_hooks`
- `client_body_hooks`
- `proxy_body_hooks`
- `resource_or_authority_dependency_hooks`

### Doctrine note

This section exists for organizations whose power is materially mediated by patrons, sponsors, vessel structures, symbolic authorities, indirect backers, or dependent clients. It is especially important for bodies that do not fit neatly into conventional state/guild/corporation models.

## Nonterritorial and distributed-polity doctrine

A large donor corpus will produce sovereign-like or polity-like bodies that are not cleanly territorial states.

### Nonterritorial polity fields

Organization-family records should support:
- `nonterritorial_polity_profile`
- `distributed_sovereignty_hooks`

### Doctrine note

This is important for:
- fleet polities
- nomadic confederacies
- church-states without fixed territory
- corporate-sovereign bodies
- extradimensional jurisdictions
- route- or gate-based authorities
- embassy-consortium governance
- ritual mandate bodies

C07 should visibly support these so “polity” does not quietly collapse into “territorial state.”

## External embodiment posture

Organizations often act in the world through some structured embodiment.

### External embodiment fields

Organization-family records should support:
- `external_embodiment_profile`
- `representative_channel_hooks`

### Useful embodiment classes

Useful classes include:
- `named_representatives`
- `anonymous_agents`
- `councils`
- `vessel_or_host_structures`
- `offices_rather_than_persons`
- `automated_or_symbolic_channels`
- `heralds_embassies_or_franchise_agents`

This makes the actor-organization seam easier to route consistently.

## Organization-site dependence and paired organization-site doctrine

Organizations and places are linked often, but they are not identical.

### Site-dependence fields

Organization-family records should support:
- `organization_site_dependence_profile`
- `seat_site_hooks`
- `ritual_node_hooks`
- `distributed_site_hooks`
- `mobile_platform_dependence_hooks`

### Site-dependence classes

Useful classes include:
- `site_independent`
- `site_anchored`
- `multi_site`
- `chapter_distributed`
- `seat_dependent`
- `habitat_bound`
- `route_bound`
- `symbolic_only`
- `represented_abroad`
- `transiently_housed`
- `coextensive_in_practice_but_not_identity`

### Paired organization-site doctrine

Some constructs are best represented not by forcing a single winner between C07 and C06, but by using paired linked records:
- an **organization/social-body record** in C07
- and a **site/place record** in C06

This paired-record approach is appropriate when:
- the organization is independently load-bearing,
- the site is also independently load-bearing,
- and either side would be distorted if reduced to a thin note.

This is not multi-owner collapse. It is a controlled paired-representation pattern for embassy bodies, churches and temple complexes, guilds and guild hall networks, city governments and cities, trade commissions and market districts, or academies and campuses.

## Mission-generation posture

Organizations are one of the main sources of scenario pressure, but C07 must not become C10.

### Mission-generation fields

Organization-family records should support:
- `mission_generation_profile`
- `commission_or_task_output_hooks`

### Useful mission-generation classes

Useful classes include:
- `commissions`
- `contracts`
- `hunts`
- `trials`
- `enforcement_operations`
- `diplomatic_missions`
- `relief_tasks`
- `extraction_orders`
- `purges_or_investigations`
- `task_board_style_work`

This is a hook, not a mission-tree subsystem.

## Authority outputs versus organization dependencies

Organizations should not be defined only by what they depend on or only by what they emit.

### Output and dependency fields

Organization-family records should support:
- `authority_output_classes`
- `organizational_dependency_profile`

### Authority output classes

Useful outputs include:
- `licenses_or_permissions`
- `offices_or_appointments`
- `protections_or_guarantees`
- `services`
- `obligations_taxes_or_dues`
- `mission_commissions`
- `sanctions`
- `recognition`
- `treaties_or_accords`
- `legal_rulings`
- `public_positions_or_mobilizations`

This distinction helps keep later mission, access, and reward files from improvising organizational outputs from scratch.

## Organization memory and archive posture

C07 should not become an investigation file, but organizations are often defined by how they preserve continuity and legitimacy.

### Memory fields

Organization-family records should support:
- `organization_memory_profile`
- `archive_or_record_hooks`
- `succession_registry_hooks`
- `claim_evidence_hooks`
- `intelligence_or_secret_archive_hooks`

### Useful memory classes

Useful classes include:
- `formal_records`
- `ritual_memory`
- `oral_tradition`
- `compartmentalized_intelligence`
- `public_archives`
- `secret_archives`
- `succession_registries`
- `claim_or_charter_evidence`

## Organizational continuity, succession, split, merge, and successor-body doctrine

Organizations change over time without ceasing to be meaningful records.

### Continuity and succession fields

Organization-family records should support:
- `continuity_profile`
- `succession_posture`
- `succession_threshold_profile`
- `fragmentation_or_split_hooks`
- `merger_or_absorption_hooks`
- `successor_body_hooks`
- `dormancy_or_reactivation_profile`

### Succession-threshold doctrine

Useful distinctions include:
- `leadership_succession_without_identity_break`
- `charter_revision_without_identity_break`
- `formal_schism_with_dual_continuity_claims`
- `dissolution_with_successor_claim`
- `merger_into_umbrella_continuity`
- `partial_merger_with_retained_local_identity`
- `dormant_continuity`
- `revived_continuity`
- `usurpation_or_hostile_successor_claim`

### Doctrine note

A house can fracture.
A confederacy can absorb bands.
A guild can split into chapters or rival branches.
A treaty body can collapse and leave successor institutions.
A church can schism.
An alliance can persist while its members change.

C07 therefore needs continuity grammar broad enough for organization persistence without becoming a political-history file.

## Organization versus site, actor, mission, access, and quasi-organization boundary control

This is the most important routing section in the file.

### Organization versus site rule

If the content’s dominant identity is a place, facility, district, capital, habitat, or locale shell, route pressure first to C06 even if an organization runs it.

A guild hall is a site.
The guild is not.

### Organization versus actor rule

If the content’s dominant identity is a person, official, boss, representative, emissary, patron-vessel, or embodied authority figure, route pressure first to C02.

A representative may speak for an organization.
They are not identical to it.

### Organization versus mission rule

If the content’s dominant identity is an objective structure, campaign front, mission chain, investigation flow, or scenario container, route pressure first to C10.

Organizations can generate missions.
They are not mission records.

### Organization versus access-procedure rule

If the content’s dominant identity is the procedural logic of who can enter, use, redeem, license, command, register, or clear something, route pressure first to B12.

C07 may expose rank, membership, mandate, legitimacy, and clearance-facing entry hooks. It must not absorb organized-access procedure as if it owned it.

### Quasi-organization doctrine

High-pressure quasi-organizations include:
- market networks without formal membership
- reputational cartels
- distributed ideology swarms
- cults without central administration
- symbolic patron systems
- platform-maintained societies
- AI-administered civic bodies
- ritual lineages with no clean institution shell

These should receive deliberate routing rather than being flattened into “faction” by convenience.

### High-risk edge classes

Examples of organization-adjacent edge cases include:
- embassy-site hybrids
- council chambers mistaken for councils
- divine or symbolic patron structures
- representative seats without formal mandate
- quasi-state guilds
- city governments versus cities
- church complexes versus the church as a body
- criminal syndicates embedded in trade districts
- social bodies maintained by a platform or locale shell

C07 should preserve routing discipline for these cases rather than accepting donor shorthand at face value.

## Required relationship patterns and relationship-discipline doctrine

C07 inherits C01 relationship grammar and must use explicit relationship structure rather than prose-only implication.

### Organization-family relationship guidance

Organization-family records should be prepared to use relationships such as:
- `controls`
- `represents`
- `member_of`
- `contains`
- `gated_by`
- `anchored_to`
- `located_in`
- `claims`
- `licenses`
- `opposed_by`
- `allied_with`
- `variant_of`
- `supersedes`
- and other C01-governed relationship forms as needed for parent bodies, branches, seats, jurisdictions, patrons, client bodies, or site claims

### Relationship-discipline rule

Any organization-side relationship preference must either:
- use existing C01 relationship verbs and grammar,
- or escalate upstream if a genuinely new constitutional relationship is required.

C07 must not quietly become a second relationship-grammar file.

## Required lower-doctrine handoffs

C07 must hand off to lower doctrine rather than rewriting it.

At minimum, organization-family entries should compose or reference:
- `C01` common record grammar
- `B12` organized-access doctrine
- `B10` social pressure/posture doctrine where public standing or leverage materially matters
- `B11` service availability doctrine where organization-controlled services materially matter
- the appropriate Batch C family file when the organization interfaces with sites, actors, frames, challenge objects, encounter packets, or missions

C07 may define entry-shape hooks for these interfaces. It may not restate the governing doctrine as if C07 owns it.

## Organization-family validation stress list

The most common routing and interpretation failure modes for this family include:
- body versus site confusion
- body versus actor confusion
- body versus mission confusion
- body versus patron abstraction confusion
- body versus access procedure confusion
- umbrella versus subordinate confusion
- charter versus recognition confusion
- continuity versus successor confusion

These should be treated as recurring validation checks rather than rare exceptions.

## Anti-collapse rules specific to organization-family records

C07 must not:
- become a political-history chapter or lore encyclopedia
- become a site file because organizations occupy buildings or capitals
- become an actor file because organizations have leaders or representatives
- become a mission tree because organizations commission operations
- become an access-procedure file by restating B12 as local doctrine
- flatten guilds, churches, agencies, clans, councils, houses, corporations, and polities into one undifferentiated faction blob
- absorb neighboring family ownership merely because donor material uses the same noun for a body, its headquarters, and its representatives

### Anti-lore-encyclopedia doctrine

Repeated history, doctrine, symbolism, and politics belong in C07 only insofar as they materially define structure, continuity, legitimacy, mandate, reach, dependency, output, or relationship posture. Otherwise they remain descriptive payload, not schema expansion.

This rule exists to stop C07 from slowly bloating into a world-politics encyclopedia.

## Reserved split note

Do not split C07 now.

If later corpus pressure proves the file genuinely unwieldy, the preferred reserved split pattern would be:
- `C07a_organization_core_and_authority_schema`
- `C07b_membership_structure_and_reach_schema`
- `C07c_legitimacy_patronage_and_boundary_control_schema`

That split is reserved, not active.

## Minimal abstract organization/social-body template

The following template extends the C01 grammar with organization-family payload blocks. It is a family abstract template, not a converted instance.

```yaml
record:
  identity:
    canonical_id: ""
    record_name: ""
    display_name: ""
    record_class: "atomic_record"
    family_owner: "C07"
    alias_set: []
    visibility_stratum: ""
    field_visibility_overrides: []

  classification:
    ontology_state: "instantiated_record"
    lifecycle_state: "draft"
    dominant_function: "organization_content"
    secondary_functions: []
    content_family: "organization"

  provenance:
    source_origin: ""
    source_reference: []
    donor_construct_type: ""
    conversion_method: ""
    normalization_level: ""
    authority_basis: []
    fragment_aggregation_status: ""
    conversion_confidence: ""
    interpretation_confidence: ""
    evidence_completeness: ""

  governance:
    primary_owner: "C07"
    secondary_dependencies: []
    authority_rank: "family_schema"
    governing_files: ["C01", "C07"]
    forbidden_owner_drift: []
    escalation_flags: []

  dependencies:
    structural_dependencies: ["C01"]
    doctrinal_dependencies: []
    payload_dependencies: []
    overlay_dependencies: []
    scaling_dependencies: []
    container_dependencies: []
    validation_dependencies: []

  relationships: []

  state:
    record_revision_id: ""
    version_line: ""
    revision_status: ""
    validation_status: ""
    structural_validation_status: ""
    doctrinal_validation_status: ""
    provenance_validation_status: ""
    payload_completeness_status: ""
    canon_review_status: ""
    supersedes: []
    superseded_by: []
    merged_from: []
    split_from: []
    identity_preservation_note: ""

  scale_and_applicability:
    scaling_axes: []
    applicability_scope: ["organization_scale"]
    domains_of_use: []
    accepted_overlays: []
    emitted_overlays: []
    compatible_containers: []
    incompatible_contexts: []

  tags_and_indexing:
    family_tags: ["organization"]
    function_tags: []
    retrieval_tags: []
    donor_alias_tags: []
    context_tags: []
    reserved_name_flags: []

  container_placement:
    home_container: ""
    additional_containers: []
    pinned_bundle_membership: []
    multi_anchor_status: ""
    local_override_status: ""

  audit_and_validation:
    conversion_notes: []
    warnings: []
    unresolved_questions: []
    doctrine_conflict_flags: []
    review_log: []

  organization_profile:
    organization_modes: []
    organization_scale: ""
    organization_topology_profile: ""
    dominant_function_profile: []
    authority_posture_profile: []
    governance_model_profile: []
    body_orientation_profile: []
    internal_structure_profile: ""
    representation_model: ""
    continuity_profile: ""

  office_and_representation:
    office_or_role_hooks: []
    seat_structure_profile: ""
    portfolio_or_domain_hooks: []
    representative_vessel_or_proxy_profile: ""
    mandate_basis: ""
    representation_scope: []
    representational_claim_hooks: []
    delegation_or_proxy_hooks: []
    representation_asymmetry_profile: ""

  membership_and_affiliation:
    membership_profile: ""
    membership_topology_profile: []
    rank_or_status_profile: ""
    entry_pathway_profile: []
    entry_requirements_hooks: []
    internal_access_tiers: []
    affiliate_or_client_hooks: []
    patronage_or_dependency_hooks: []
    expulsion_or_exclusion_hooks: []

  legitimacy_and_recognition:
    legitimacy_profile: ""
    legitimacy_source_profile: []
    recognition_profile: ""
    recognition_source_profile: []
    charter_or_foundation_basis: ""
    public_acceptance_posture: ""
    mandate_contestation_hooks: []
    juridical_or_customary_basis: ""

  public_internal_and_secrecy_posture:
    public_positioning_profile: ""
    internal_self_conception_profile: ""
    actual_operational_posture: ""
    secrecy_transparency_disclosure_profile: ""

  structure_and_reach:
    parent_body_hooks: []
    subordinate_body_hooks: []
    parallel_body_hooks: []
    branch_or_division_hooks: []
    umbrella_constituent_profile: []
    jurisdiction_profile: ""
    reach_type_profile: []
    claim_or_stake_hooks: []
    claim_object_classes: []
    territorial_or_site_reach_hooks: []
    service_reach_profile: ""
    representation_reach_profile: ""
    enforcement_or_intervention_hooks: []

  resource_base_and_outputs:
    resource_base_profile: []
    continuity_support_hooks: []
    authority_output_classes: []
    organizational_dependency_profile: []

  diplomacy_and_alignment:
    alliance_posture: ""
    rivalry_or_conflict_hooks: []
    neutrality_or_nonalignment_profile: ""
    treaty_or_obligation_hooks: []
    cooperation_or_dependency_hooks: []
    inter_body_posture_profile: []

  patronage_and_dependency:
    patron_structure_profile: ""
    sponsorship_hooks: []
    client_body_hooks: []
    proxy_body_hooks: []
    resource_or_authority_dependency_hooks: []

  nonterritorial_and_site_dependence:
    nonterritorial_polity_profile: ""
    distributed_sovereignty_hooks: []
    organization_site_dependence_profile: ""
    seat_site_hooks: []
    ritual_node_hooks: []
    distributed_site_hooks: []
    mobile_platform_dependence_hooks: []

  mission_generation_and_embodiment:
    mission_generation_profile: []
    commission_or_task_output_hooks: []
    external_embodiment_profile: ""
    representative_channel_hooks: []

  memory_and_archive:
    organization_memory_profile: []
    archive_or_record_hooks: []
    succession_registry_hooks: []
    claim_evidence_hooks: []
    intelligence_or_secret_archive_hooks: []

  succession_and_change:
    succession_posture: ""
    succession_threshold_profile: []
    fragmentation_or_split_hooks: []
    merger_or_absorption_hooks: []
    successor_body_hooks: []
    dormancy_or_reactivation_profile: ""
```

## Final doctrine statement

C07 is the organization/social-body-family constitutional schema for Batch C.

It does not reduce the family to generic factions.
It does not collapse organizations into sites, actors, missions, or access procedures.
It does not become a stealth political-history chapter.
It does not absorb neighboring ownership merely because donor material uses one noun for a body, its headquarters, and its representatives.

Its purpose is to let Astra represent guilds, institutions, houses, agencies, polities, councils, patron structures, and organization-content entries lawfully across a mixed donor corpus while preserving scale, topology, authority posture, governance model, legitimacy pressure, reach, succession, outputs, and cross-file interoperability.

