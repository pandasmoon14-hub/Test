from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

B05_PATH = ROOT / "docs" / "doctrine" / "operations" / "batch_b" / "B05_acquisition_reward_requisition_and_value_flow_procedure.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B05 owns",
    "## 4. What B05 must not own",
    "## 5. Non-collapse rule",
    "## 6. Value, acquisition, reward, requisition, and value-flow definitions",
    "## 7. Acquisition/value-flow intake procedure",
    "## 8. Value-form classification",
    "## 9. Acquisition-channel classification",
    "## 10. Market access, availability, scarcity, and restricted-access procedure",
    "## 11. Exchange, barter, purchase, sale, trade, favor, obligation, and claim routing",
    "## 12. Reward, loot, salvage, and claim-entry procedure",
    "## 13. Requisition, rationing, license, permit, authority, and institutional access procedure",
    "## 14. Upkeep, consumption, maintenance cost, value sink, and economic pressure routing",
    "## 15. Value conversion and abstraction procedure",
    "## 16. Ownership, custody, legality, burden, and inventory handoff rules",
    "## 17. World, faction, institution, law, and market-disruption handoff rules",
    "## 18. Value-flow state-delta routing",
    "## 19. Owner-file handoff rules",
    "## 20. Batch B to C00/C-family handoff rules",
    "## 21. Missing-schema fallback and quarantine/escalation",
    "## 22. Source-local donor economy/reward/requisition handling",
    "## 23. Runtime boundary",
    "## 24. Canon boundary",
    "## 25. Live-play/training boundary",
    "## 26. Examples of good and bad B05 usage",
    "## 27. Minimum tests or assertions",
    "## 28. Acceptance criteria",
    "## 29. Follow-up handoff to B06",
]


def b05_text() -> str:
    return read_utf8(B05_PATH)


def test_b05_file_exists_at_expected_path() -> None:
    assert B05_PATH.exists()
    assert B05_PATH.is_file()


def test_b05_required_sections_are_present() -> None:
    text = b05_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b05_declares_ownership_and_non_ownership() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "acquisition intake procedure after b01, b02, b03, or b04 produce acquisition, value, reward, requisition, exchange, upkeep, consumption, scarcity, availability, or value-sink pressure",
        "value-form classification",
        "acquisition-channel classification",
        "market access and availability procedure",
        "scarcity-state identification",
        "value conversion procedure as routing, not math",
        "reward, loot, salvage, and claim-entry procedure",
        "lawful reward and salvage ownership/custody separation",
        "requisition request and intake procedure",
        "upkeep, consumption, maintenance cost, value sink, and economic pressure routing",
        "value-flow state-delta routing",
    ]:
        assert phrase in lowered

    for phrase in [
        "final economy schema",
        "final inventory schema",
        "final object schema",
        "c-family schema fields",
        "c01-c14 schema contents",
        "final currency math",
        "final price lists",
        "final shop lists",
        "final market tables",
        "final economy law",
        "final reward tables",
        "final loot tables",
        "final treasure tables",
        "final wealth-by-level math",
        "final requisition rating system",
        "final ownership database",
        "runtime economy state",
        "runtime inventory ledger",
        "command lifecycle implementation",
        "context packet compiler",
        "sourcebook prose",
        "donor economy, reward, market, rationing, scarcity, loot, salvage, requisition, upkeep, or value-conversion systems as astra defaults",
    ]:
        assert phrase in lowered


def test_b05_references_b01_b02_b03_and_b04_as_upstream_batch_b_context() -> None:
    lowered = b05_text().lower()
    for marker in [
        "b01_scene_encounter_and_activity_procedure.md",
        "b02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md",
        "b03_item_gear_equipment_and_asset_use_procedure.md",
        "b04_inventory_storage_custody_and_burden_procedure.md",
        "upstream batch b context",
        "must build on them, not rewrite them",
    ]:
        assert marker in lowered


def test_b05_includes_c00_handoff_language_and_block() -> None:
    text = b05_text()
    for marker in [
        "C00 remains the schema handoff control surface",
        "batch_b_to_c_handoff",
        "target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema",
        "schema_status: not_started | stub_index_only | minimum_unlock_draft | tested_minimum | stable_for_family | stable_cross_family | superseded | deprecated",
        "required_c00_base_fields: true",
        "source_evidence_refs_required: true",
        "construct_refs_required: true",
        "outcome_refs_required: true",
        "provenance_refs_required: true",
        "source_local_boundary_required_if_applicable: true",
        "rejected_donor_elements_required_if_applicable: true",
        "canon_eligibility_required: true",
        "review_routing_required: true",
        "unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists",
    ]:
        assert marker in text


def test_b05_includes_value_flow_routing_note_as_doctrine_facing_only() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "value_flow_routing_note",
        "doctrine-facing only",
        "not a runtime schema",
        "not a backend event",
        "not a command object",
        "not a c-family record",
        "not an economy database row",
        "not an inventory ledger entry",
        "not final mechanics",
        "not canon",
        "not player-facing rule text",
    ]:
        assert phrase in lowered


def test_b05_includes_value_vocabularies() -> None:
    text = b05_text()
    for marker in [
        "currency",
        "barter_good",
        "service",
        "favor",
        "obligation",
        "claim",
        "license",
        "permit",
        "ration",
        "requisition_credit",
        "faction_scrip",
        "reputation_access",
        "material_component",
        "strategic_resource",
        "consumable_supply",
        "source_local_value",
        "unknown_value",
        "purchase",
        "sale",
        "barter",
        "trade",
        "reward",
        "loot",
        "salvage",
        "requisition",
        "market_exchange",
        "black_market_exchange",
        "source_local_acquisition",
        "unknown_acquisition",
        "abundant",
        "available",
        "limited",
        "rationed",
        "restricted",
        "licensed",
        "illegal",
        "controlled",
        "black_market_only",
        "source_local_scarcity",
        "unknown_scarcity",
        "acquisition_declared",
        "reward_offered",
        "loot_identified",
        "salvage_identified",
        "requisition_requested",
        "value_conversion_needed",
        "value_sink_triggered",
        "value_flow_quarantined_gap",
        "no_delta_required",
        "value_obtained",
        "value_spent",
        "value_disputed",
        "value_converted_to_claim",
        "value_converted_to_obligation",
        "value_converted_to_access",
        "quarantined_unresolved_delta",
        "owner_file_escalation",
    ]:
        assert marker in text


def test_b05_separates_core_value_and_custody_concepts() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "money is not the default form of value",
        "price is not access",
        "availability is not ownership",
        "possession is not ownership",
        "ownership is not legality",
        "loot is not lawful property by default",
        "salvage is not free wealth",
        "reward is not automatic power",
        "requisition is not free supply",
        "burden means carrying, storage, security, trace, upkeep, transport, access, concealment, audit, maintenance, spoilage, or support pressure",
    ]:
        assert phrase in lowered


def test_b05_includes_market_reward_requisition_sink_and_conversion_procedure() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "market access, availability, scarcity, and restricted-access procedure",
        "exchange, barter, purchase, sale, trade, favor, obligation, and claim routing",
        "reward, loot, salvage, and claim-entry procedure",
        "requisition, rationing, license, permit, authority, and institutional access procedure",
        "upkeep, consumption, maintenance cost, value sink, and economic pressure routing",
        "value conversion and abstraction procedure",
        "b05 value conversion is routing, not math",
        "a market is not a guaranteed shop list",
        "a black market is not guaranteed access",
        "scarcity is contextual, not universal",
    ]:
        assert phrase in lowered


def test_b05_rejects_final_economy_and_runtime_systems() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "final economy schema",
        "final currency math",
        "final price lists",
        "final shop lists",
        "final market tables",
        "final reward tables",
        "final loot tables",
        "final treasure tables",
        "final wealth-by-level math",
        "final requisition rating system",
        "final ownership database",
        "final economy law",
        "final legal code",
        "runtime economy state",
        "runtime inventory ledger",
    ]:
        assert phrase in lowered


def test_b05_rejects_runtime_state_event_command_lifecycle_ownership() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "b05 rejects runtime state/event/command lifecycle ownership",
        "runtime entity/component/event/state schemas",
        "persistent campaign state",
        "command lifecycle implementation",
        "context packet compiler",
        "hidden-information runtime state",
        "live-play behavior must not consume b05 procedure as runtime authority",
    ]:
        assert phrase in lowered


def test_b05_rejects_c_family_field_invention_and_schema_content_ownership() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "must not invent c-family fields",
        "c-family schema fields",
        "c01-c14 schema contents",
        "c-family field invention",
        "c01-c14 schema-content ownership",
        "batch b procedure may identify that a c-family handoff is needed, but it must not invent c-family fields",
        "target_schema_family: c01 | c02 | c03 | c04 | c05 | c06 | c07 | c08 | c09 | c10 | c11 | c12 | c13 | c14 | pending_schema",
    ]:
        assert phrase in lowered


def test_b05_rejects_donor_economy_reward_requisition_systems_as_astra_defaults() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "donor economy, reward, market, rationing, scarcity, loot, salvage, requisition, upkeep, or value-conversion systems as astra defaults",
        "b05 rejects donor economy/reward/requisition systems as astra defaults",
        "source-local donor economy/reward/requisition handling",
        "must not become astra defaults through b05",
        "source-local or rejected donor elements",
    ]:
        assert phrase in lowered


def test_b05_includes_acquisition_reward_requisition_value_flow_state_delta_routing() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "value-flow state-delta routing",
        "every meaningful acquisition/reward/requisition/value-flow event must route at least one delta to a recognized owner",
        "acquisition_declared",
        "reward_claimed",
        "requisition_requested",
        "owner_handoff_required",
        "no_delta_required",
        "owner_routed",
        "transition_note",
        "source_local_retained_effect",
        "quarantined_unresolved_delta",
        "owner_file_escalation",
    ]:
        assert phrase in lowered


def test_b05_includes_source_local_quarantine_escalation_and_review() -> None:
    text = b05_text()
    lowered = text.lower()
    for marker in [
        "Source-local donor economy/reward/requisition handling",
        "pending_schema",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
        "source_local_review",
        "source-local boundary",
    ]:
        assert marker in text
    assert "missing-schema fallback and quarantine/escalation" in lowered
    assert "route unsafe material to quarantine, escalation, `human_review`, or `defer_until_schema_exists`" in lowered


def test_b05_references_d_series_only_as_draft_source_pack_reference_material() -> None:
    text = b05_text()
    lowered = text.lower()
    for marker in [
        "D00-03_state_delta_commit_protocol.md",
        "D09-06_crafting_repair_salvage_modification_upgrade_and_requisition_interface.md",
        "D10-05_economy_scarcity_strategic_resources_market_requisition_register.md",
        "D15-01_organized_actors_standing_pressure_obligations_claims_and_operation_anatomy.md",
        "D16-00_opposition_creature_encounter_and_hazard_construction_owner_boundaries.md",
        "D17-00_economy_acquisition_inventory_reward_and_requisition_owner_boundaries.md",
        "D17-01_value_forms_access_channels_scarcity_ownership_custody_and_burden_states.md",
        "D17-02_acquisition_exchange_market_access_availability_and_value_conversion.md",
        "D17-03_reward_loot_salvage_claim_and_value_entry_procedure.md",
        "D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md",
        "D17-06_source_local_economy_donor_value_mapping_quarantine_and_escalation.md",
        "D17-07_records_not_final_schema_and_conversion_handoff_shapes.md",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
    ]:
        assert marker in text
    assert "d00, d09, d10, d15, d16, d17, and d19 source-pack files are referenced only as draft source-pack/reference material" in lowered
    assert "not current doctrine authority" in lowered


def test_b05_does_not_require_define_create_or_promote_b06_b11() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "does not require, define, create, or promote b06-b11",
        "b05 does not create b06-b11, does not define b06-b11 content, does not require b06-b11, does not promote b06-b11",
        "does not make b06-b11 current doctrine",
    ]:
        assert phrase in lowered


def test_b05_does_not_require_define_create_or_promote_c01_c14() -> None:
    lowered = b05_text().lower()
    for phrase in [
        "does not require, define, create, or promote c01-c14",
        "future c01-c14 schema families may receive conversion handoffs but b05 must not invent their fields",
        "c01-c14 schema-content ownership",
    ]:
        assert phrase in lowered


def _registry_record_block(file_id: str) -> str:
    registry_text = read_utf8(REGISTRY_PATH)
    marker = f"- file_id: {file_id}\n"
    start = registry_text.index(marker)
    next_record = registry_text.find("\n- file_id:", start + len(marker))
    if next_record == -1:
        return registry_text[start:]
    return registry_text[start:next_record]


def test_registry_status_is_not_promoted_to_current() -> None:
    registry_text = read_utf8(REGISTRY_PATH)
    assert "- file_id: B05\n" not in registry_text
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        assert "  status: current" not in block
    assert "  status: draft" in _registry_record_block("C00")
    for number in range(1, 15):
        assert "  status: todo" in _registry_record_block(f"C{number:02d}")
