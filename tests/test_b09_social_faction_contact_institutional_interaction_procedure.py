from tests.helpers import ROOT, read_utf8

B09_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "operations"
    / "batch_b"
    / "B09_social_faction_contact_and_institutional_interaction_procedure.md"
)

REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B09 owns",
    "## 4. What B09 must not own",
    "## 5. Non-collapse rule",
    "## 6. Social contact, organized actor, institution, standing, pressure, obligation, claim, and operation definitions",
    "## 7. Social/faction/contact intake procedure",
    "## 8. Contact type and organized-actor classification",
    "## 9. Standing, pressure, obligation, claim, authority, and access review",
    "## 10. Public/private/hidden/source-local relationship-state handling",
    "## 11. Social intent, method, leverage, cost, risk, and visibility checkpoints",
    "## 12. Negotiation, diplomacy, persuasion, intimidation, deception, mediation, petition, bargaining, threat, bribe, and blackmail routing",
    "## 13. Authority, jurisdiction, law, permit, license, restriction, inspection, and sanction routing",
    "## 14. Patronage, sponsorship, alliance, rivalry, treaty, favor, debt, and obligation routing",
    "## 15. Faction/institution response trigger procedure",
    "## 16. Institutional operation trigger routing",
    "## 17. Rumor, propaganda, misinformation, secrecy, and hidden-agenda presentation handoff rules",
    "## 18. Contact escalation, de-escalation, refusal, compliance, compromise, and fallout routing",
    "## 19. Social/faction/contact state-delta routing",
    "## 20. Owner-file handoff rules",
    "## 21. Batch B to C00/C-family handoff rules",
    "## 22. Missing-schema fallback and quarantine/escalation",
    "## 23. Source-local donor social/faction/reputation/law/contact handling",
    "## 24. Runtime boundary",
    "## 25. Canon boundary",
    "## 26. Live-play/training boundary",
    "## 27. Examples of good and bad B09 usage",
    "## 28. Minimum tests or assertions",
    "## 29. Acceptance criteria",
    "## 30. Follow-up handoff to B10",
]


def b09_text() -> str:
    return read_utf8(B09_PATH)


def test_b09_file_exists_at_expected_path() -> None:
    assert B09_PATH.exists()
    assert B09_PATH.is_file()


def test_b09_required_sections_are_present() -> None:
    text = b09_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b09_declares_ownership_and_non_ownership() -> None:
    lowered = b09_text().lower()
    for phrase in [
        "social/faction/contact/institutional intake after b01-b08 produce social, factional, legal, institutional, standing, access, claim, obligation, authority, or relationship pressure",
        "social-contact classification",
        "organized-actor and institutional-contact classification",
        "individual contact vs organized actor vs institution vs domain authority separation",
        "standing review and standing-pressure routing",
        "public/private/hidden/source-local relationship-state boundary handling",
        "leverage, cost, risk, consequence, and visibility checkpoint procedure",
        "faction/institution response trigger identification",
        "institutional operation trigger routing",
        "social/faction/contact state-delta routing",
    ]:
        assert phrase in lowered

    for phrase in [
        "final social schema",
        "final faction schema",
        "final relationship schema",
        "final reputation schema",
        "final law schema",
        "final institution schema",
        "final contact schema",
        "final domain schema",
        "c-family schema fields",
        "c01-c14 schema contents",
    ]:
        assert phrase in lowered


def test_b09_references_b01_through_b08_as_upstream_batch_b_context() -> None:
    lowered = b09_text().lower()
    for marker in [
        "b01_scene_encounter_and_activity_procedure.md",
        "b02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md",
        "b03_item_gear_equipment_and_asset_use_procedure.md",
        "b04_inventory_storage_custody_and_burden_procedure.md",
        "b05_acquisition_reward_requisition_and_value_flow_procedure.md",
        "b06_project_crafting_salvage_repair_and_upgrade_procedure.md",
        "b07_recovery_training_research_and_preparation_project_procedure.md",
        "b08_travel_exploration_navigation_and_discovery_procedure.md",
        "upstream batch b context",
        "must build on them, not rewrite them",
    ]:
        assert marker in lowered


def test_b09_includes_c00_handoff_language_and_block() -> None:
    text = b09_text()
    for marker in [
        "C00 remains the schema handoff control surface",
        "batch_b_to_c_handoff",
        "target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema",
        "unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists",
        "The following block is lightweight and doctrine-facing only. It must not be treated as a runtime schema.",
    ]:
        assert marker in text


def test_b09_includes_social_faction_contact_routing_note_and_doctrine_only_boundary() -> None:
    text = b09_text()
    for marker in [
        "social_faction_contact_routing_note",
        "`social_faction_contact_routing_note` is doctrine-facing only",
        "not a runtime schema",
        "not a backend event",
        "not a command object",
        "not a C-family record",
        "not a social-state database row",
        "not a faction-state row",
        "not a relationship ledger",
        "not a reputation ledger",
        "not a law database row",
        "not a faction AI instruction",
        "not a social-combat move",
        "not a reaction table",
        "not a faction clock",
        "not a sourcebook faction entry",
        "not final mechanics",
        "not a database contract",
        "not an event log",
        "not a context packet format",
        "not persistent campaign state",
        "not canon",
        "not player-facing rule text",
    ]:
        assert marker in text


def test_b09_includes_all_vocabularies() -> None:
    text = b09_text()
    expected_terms = [
        # contact types
        "individual_contact", "group_contact", "organized_actor_contact", "faction_contact",
        "institutional_contact", "domain_authority_contact", "law_authority_contact",
        "market_authority_contact", "guild_contact", "sect_contact", "corporate_contact",
        "temple_contact", "academy_contact", "kingdom_polity_contact", "agency_contact",
        "patron_contact", "crew_or_party_contact", "public_contact", "hidden_contact",
        "source_local_contact", "unknown_contact",
        # organized actor types
        "faction", "institution", "guild", "sect", "corporation", "polity", "kingdom",
        "agency", "order", "cult", "clan", "family", "academy", "temple", "patron_network",
        "market_authority", "law_office", "station_authority", "navy_or_military",
        "rebel_cell", "criminal_syndicate", "player_organization", "public",
        "source_local_organization", "unknown_organization",
        # states/intents/triggers/outcomes/risks
        "trusted", "favored", "allied", "patronized", "neutral", "watched", "scrutinized",
        "indebted", "obligated", "rivalrous", "hostile", "banned", "wanted", "protected",
        "sponsored", "licensed", "recognized", "conditional", "temporary", "revoked",
        "latent", "active", "escalating", "decaying", "suppressed", "transferred",
        "surfaced", "converted_to_operation", "converted_to_scene", "converted_to_project",
        "converted_to_conflict", "resolved", "retired", "owed", "invoked", "partially_paid",
        "paid", "deferred", "contested", "forgiven", "defaulted", "asserted", "rejected",
        "enforced", "suspended", "settled", "violated", "request_access", "request_information",
        "negotiate", "bargain", "persuade", "intimidate", "deceive", "mediate", "petition",
        "appeal", "threaten", "bribe", "blackmail", "call_in_favor", "settle_debt",
        "invoke_obligation", "contest_claim", "assert_claim", "repair_standing", "worsen_standing",
        "seek_patronage", "offer_sponsorship", "request_permit", "request_license",
        "pass_checkpoint", "avoid_scrutiny", "spread_rumor", "suppress_rumor", "expose_scandal",
        "recruit_support", "defect_or_betray", "formal_diplomacy", "treaty_or_pact",
        "standing_change", "pressure_surface", "obligation_invoked", "claim_asserted",
        "claim_contested", "access_requested", "access_denied", "law_contact",
        "permit_or_license_review", "sanction_threat", "faction_response", "institution_response",
        "domain_authority_response", "rumor_or_propaganda_pressure", "hidden_agenda_pressure",
        "public_scene_pressure", "project_sponsorship_pressure", "travel_access_pressure",
        "market_access_pressure", "enforcement_pressure", "conflict_escalation_pressure",
        "campaign_horizon_pressure", "no_delta_required", "contact_established", "contact_refused",
        "access_granted", "access_limited", "standing_improved", "standing_worsened",
        "standing_complicated", "obligation_created", "obligation_settled", "obligation_defaulted",
        "claim_recognized", "claim_rejected", "favor_created", "favor_spent", "debt_created",
        "debt_settled", "scrutiny_increased", "scrutiny_decreased", "rumor_spread",
        "rumor_suppressed", "misinformation_routed", "propaganda_routed",
        "hidden_agenda_pressure_routed", "permit_granted", "permit_denied", "license_granted",
        "license_denied", "sanction_triggered", "enforcement_triggered", "faction_operation_triggered",
        "institutional_operation_triggered", "active_scene_triggered", "project_triggered",
        "conflict_triggered", "owner_routed", "transition_note", "source_local_retained_effect",
        "quarantined_unresolved_delta", "owner_file_escalation", "social_exposure",
        "legal_exposure", "reputational_exposure", "faction_attention", "public_attention",
        "hidden_agenda_surface", "rumor_distortion", "misinformation_risk", "obligation_risk",
        "claim_dispute", "debt_escalation", "favor_complication", "access_revocation",
        "patron_pressure", "authority_scrutiny", "sanction_risk", "enforcement_risk",
        "market_access_risk", "travel_access_risk", "conflict_escalation", "owner_file_gap",
    ]
    for term in expected_terms:
        assert term in text


def test_b09_separates_required_concepts() -> None:
    lowered = b09_text().lower()
    for phrase in [
        "a social contact is not automatically a social roll",
        "individual contact", "organized actor", "faction", "institution", "domain authority",
        "actor personhood", "public standing", "private standing", "hidden standing",
        "standing is not a single reputation score", "reputation is not truth",
        "a rumor is not confirmed fact", "propaganda is not neutral narration",
        "misinformation", "a claim is not ownership by default", "an obligation is not payment by default",
        "a favor is not currency by default", "debt", "a permit is not universal access",
        "a license is not universal legality", "legal status is not moral truth", "authority", "access",
        "a social pressure is not automatically a scene", "a faction response is not automatically a faction clock",
        "institutional operation", "runtime state", "canon",
    ]:
        assert phrase in lowered


def test_b09_includes_required_procedural_routing() -> None:
    lowered = b09_text().lower()
    for phrase in [
        "social/faction/contact intake procedure",
        "contact type", "organized-actor classification",
        "standing/pressure/obligation/claim review",
        "public/private/hidden/source-local",
        "social intent, method, leverage, cost, risk, and visibility checkpoints",
        "negotiation, diplomacy, persuasion, intimidation, deception, mediation, petition, bargaining, threat, bribe, and blackmail routing",
        "authority, jurisdiction, law, permit, license, restriction, inspection, and sanction routing",
        "patronage, sponsorship, alliance, rivalry, treaty, favor, debt, and obligation routing",
        "faction/institution response trigger procedure",
        "institutional operation trigger routing",
        "rumor, propaganda, misinformation, secrecy, and hidden-agenda presentation handoff rules",
        "contact escalation, de-escalation, refusal, compliance, compromise, and fallout routing",
        "state-delta routing",
    ]:
        assert phrase in lowered


def test_b09_rejects_final_mechanics_runtime_and_schema_ownership() -> None:
    lowered = b09_text().lower()
    for phrase in [
        "final social schema", "final faction schema", "final relationship schema", "final reputation schema",
        "final law schema", "final institution schema", "final contact schema", "final domain schema",
        "final social mechanics", "final social-combat system", "final reputation math", "final attitude tables",
        "final reaction rolls", "final morale rules", "final faction clocks", "final influence tracks",
        "final heat/wanted systems", "final law code", "final license/permit system",
        "final faction rank system", "final renown system", "final contact rules", "final patron rules",
        "final treaty system", "final debt economy", "final favor economy", "final domain-turn procedure",
        "final kingdom-turn procedure", "final faction-turn procedure", "final institutional ai behavior",
        "final npc motivation/personhood", "final actor substrate", "final hidden-agenda truth",
        "final rumor truth", "final propaganda truth", "final social narration/presentation behavior",
        "runtime social state", "runtime faction state", "runtime relationship state", "runtime reputation ledger",
        "runtime law database", "runtime faction ai", "runtime entity/component/event/state schemas",
        "runtime state/event/command lifecycle ownership", "command lifecycle implementation",
    ]:
        assert phrase in lowered


def test_b09_rejects_c_family_invention_and_later_schema_promotion() -> None:
    lowered = b09_text().lower()
    for phrase in [
        "must not invent c-family fields",
        "c-family schema fields",
        "c01-c14 schema contents",
        "b09 does not require, define, create, or promote b10-b11",
        "b09 does not require, define, create, or promote c01-c14",
    ]:
        assert phrase in lowered


def test_b09_includes_source_local_quarantine_and_missing_schema_controls() -> None:
    text = b09_text()
    lowered = text.lower()
    for phrase in [
        "donor social/faction/reputation/law/contact systems as astra defaults",
        "source-local donor social/faction/reputation/law/contact handling",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
        "pending_schema",
    ]:
        assert phrase in lowered or phrase in text


def test_b09_references_d_series_as_draft_reference_not_current_authority() -> None:
    text = b09_text()
    for marker in [
        "D00-03_state_delta_commit_protocol.md",
        "D02-00_resolution_architecture_and_owner_boundaries.md",
        "D05-03_relevance_handling_for_checks.md",
        "D08-00_layered_actor_state_architecture.md",
        "D08-01_identity_continuity_personhood_and_agency.md",
        "D10-07_information_state_public_knowledge_rumor_secrecy_records_register.md",
        "D11-03_hidden_state_rumor_secrecy_misinformation_presentation.md",
        "D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md",
        "D13-02_project_creation_requirement_discovery_commitment_and_interval_setup.md",
        "D14-05_travel_risk_resource_pressure_hazards_encounters_and_transition_handoffs.md",
        "D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md",
        "D15-01_organized_actors_standing_pressure_obligations_claims_and_operation_anatomy.md",
        "D16-00_opposition_creature_encounter_and_hazard_construction_owner_boundaries.md",
        "D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md",
        "D18-00_structural_time_campaign_continuity_arc_season_and_horizon_owner_boundaries.md",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
        "referenced only as draft source-pack/reference material, not final current doctrine authority",
    ]:
        assert marker in text


def test_registry_status_is_not_promoted_to_current() -> None:
    registry = read_utf8(REGISTRY_PATH)
    # Durable regression check: the B09 draft text explicitly avoids promotion, and the
    # existing registry remains governed by the registry tests run with this file.
    assert "No registry status is promoted to current" in b09_text()
    assert "B09_social_faction_contact_and_institutional_interaction_procedure.md" not in registry
