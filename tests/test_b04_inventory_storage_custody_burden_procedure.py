from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

B04_PATH = ROOT / "docs" / "doctrine" / "operations" / "batch_b" / "B04_inventory_storage_custody_and_burden_procedure.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B04 owns",
    "## 4. What B04 must not own",
    "## 5. Non-collapse rule",
    "## 6. Inventory, possession, custody, access, and burden definitions",
    "## 7. Inventory/possession intake procedure",
    "## 8. Holding-mode classification",
    "## 9. Access-state and quick-access procedure",
    "## 10. Possession, ownership, custody, and legal visibility procedure",
    "## 11. Burden-type classification and transport/support pressure",
    "## 12. Storage, container, cache, vault, vehicle, platform, and facility procedure",
    "## 13. Concealment, security, audit trail, trace, and inspection procedure",
    "## 14. Transfer, handoff, requisition, escrow, impoundment, and shared-possession procedure",
    "## 15. Decay, spoilage, maintenance, upkeep, and stability routing",
    "## 16. Inventory loss trigger procedure",
    "## 17. Recovery and retrieval procedure",
    "## 18. Inventory/custody/burden state-delta routing",
    "## 19. Owner-file handoff rules",
    "## 20. Batch B to C00/C-family handoff rules",
    "## 21. Missing-schema fallback and quarantine/escalation",
    "## 22. Source-local donor inventory/storage/economy handling",
    "## 23. Runtime boundary",
    "## 24. Canon boundary",
    "## 25. Live-play/training boundary",
    "## 26. Examples of good and bad B04 usage",
    "## 27. Minimum tests or assertions",
    "## 28. Acceptance criteria",
    "## 29. Follow-up handoff to B05",
]


def b04_text() -> str:
    return read_utf8(B04_PATH)


def test_b04_file_exists_at_expected_path() -> None:
    assert B04_PATH.exists()
    assert B04_PATH.is_file()


def test_b04_required_sections_are_present() -> None:
    text = b04_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b04_declares_ownership_and_non_ownership() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "inventory/possession intake procedure after b03 object-use or acquisition/transfer/loss pressure",
        "possession, access, ownership, custody, legal visibility, readiness, storage, quick-access, and burden separation",
        "holding-mode classification",
        "burden-type classification",
        "access-state classification",
        "possession-scope classification",
        "storage/container/cache/vault/vehicle/platform/facility procedure routing",
        "concealment/security/audit-trail/trace/inspection procedure routing",
        "transfer, handoff, requisition, impoundment, escrow, shared ownership, shared-possession, and faction custody procedure routing",
        "lawful inventory-loss trigger procedure",
    ]:
        assert phrase in lowered

    for phrase in [
        "final inventory schema",
        "final object schema",
        "c-family schema fields",
        "c01-c14 schema contents",
        "final item stats",
        "final equipment stats",
        "final carrying-capacity math",
        "final inventory capacity math",
        "final weight/slot/encumbrance rules",
        "final cargo-capacity math",
        "final container-capacity math",
        "final quick-access action economy",
        "final inventory ui/backend model",
        "final runtime inventory state",
        "final event-sourced inventory ledger",
        "final ownership database",
        "final price, market, reward, treasure, requisition, or economy law",
        "final legal code, faction law, licensing, tax, contraband, or confiscation rules",
        "runtime entity/component/event/state schemas",
        "runtime state/event/command lifecycle ownership",
        "command lifecycle implementation",
        "context packet compiler",
        "hidden-information runtime state",
        "sourcebook prose",
        "donor inventory/equipment/economy systems as astra defaults",
    ]:
        assert phrase in lowered


def test_b04_references_b01_b02_and_b03_as_upstream_batch_b_context() -> None:
    lowered = b04_text().lower()
    assert "b01_scene_encounter_and_activity_procedure.md" in lowered
    assert "b02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md" in lowered
    assert "b03_item_gear_equipment_and_asset_use_procedure.md" in lowered
    assert "upstream batch b context" in lowered
    assert "must build on them, not rewrite them" in lowered


def test_b04_includes_c00_handoff_language_and_block() -> None:
    text = b04_text()
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


def test_b04_includes_inventory_custody_routing_note_as_doctrine_facing_only() -> None:
    text = b04_text()
    lowered = text.lower()
    for marker in [
        "inventory_custody_routing_note",
        "inventory_state: possession_declared | possession_confirmed | possession_disputed | access_confirmed | access_blocked | quick_access_confirmed | storage_confirmed | custody_confirmed | custody_disputed | burden_identified | loss_triggered | recovery_available | owner_handoff_required | source_local_inventory_procedure | inventory_quarantined_gap",
        "actor_ref: string | null",
        "object_or_value_ref: string | null",
        "holding_mode: carried_on_person | equipped | worn | quick_access | packed | container_stored | vehicle_stored | platform_stored | facility_stored | banked | vaulted | cached | hidden | escrowed | faction_held | requisition_held | impounded | leased_storage | digital_or_pattern_stored | bound_to_actor | source_local_holding | unknown",
        "access_state: immediate_access | quick_access | scene_access | interval_access | safe_location_access | facility_access | vehicle_or_platform_access | faction_permission_access | licensed_access | locked_access | hidden_cache_access | delayed_access | blocked_access | source_local_access | unknown_access",
        "possession_scope: individual | party_shared | crew_shared | faction_shared | vehicle_or_platform | facility | domain | escrow | source_local_scope",
        "loss_trigger: none | overburden | flight | defeat | confiscation | tax_seizure | faction_claim | legal_inspection | theft | container_damage | platform_destruction | hazard_exposure | decay | spoilage | abandonment | failed_transport | source_local_trigger",
        "loss_outcome: none | lost | damaged | impounded | stolen | abandoned | claimed_by_other | converted_to_unresolved_pressure | recoverable | recoverable_with_cost | recoverable_with_project | recoverable_with_operation | destroyed | quarantined | source_local_result",
        "delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation",
    ]:
        assert marker in text
    for phrase in [
        "b04-specific lightweight doctrine-facing block",
        "not a runtime schema",
        "not a backend event",
        "not a command object",
        "not a c-family record",
        "not an inventory database row",
        "not an item statblock",
        "not a sourcebook statblock",
        "not final mechanics",
        "not a database contract",
        "not an event log",
        "not a context packet format",
        "not persistent campaign state",
        "not canon",
        "not player-facing rule text",
    ]:
        assert phrase in lowered


def test_b04_includes_classification_vocabularies() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "carried_on_person",
        "equipped",
        "worn",
        "quick_access",
        "packed",
        "container_stored",
        "vehicle_stored",
        "platform_stored",
        "facility_stored",
        "banked",
        "vaulted",
        "cached",
        "hidden",
        "escrowed",
        "faction_held",
        "requisition_held",
        "impounded",
        "leased_storage",
        "digital_or_pattern_stored",
        "bound_to_actor",
        "source_local_holding",
        "weight",
        "bulk",
        "volume",
        "slot",
        "quick_access_limit",
        "container_capacity",
        "transport_capacity",
        "storage_capacity",
        "security_burden",
        "concealment_burden",
        "legal_visibility",
        "social_visibility",
        "faction_trace",
        "custody_risk",
        "maintenance_burden",
        "decay_or_spoilage",
        "fuel_or_power_support",
        "crew_or_labor_support",
        "platform_cargo_burden",
        "access_delay",
        "retrieval_risk",
        "source_local_burden",
        "immediate_access",
        "scene_access",
        "interval_access",
        "safe_location_access",
        "facility_access",
        "vehicle_or_platform_access",
        "faction_permission_access",
        "licensed_access",
        "locked_access",
        "hidden_cache_access",
        "delayed_access",
        "blocked_access",
        "source_local_access",
        "unknown_access",
        "individual",
        "party_shared",
        "crew_shared",
        "faction_shared",
        "vehicle_or_platform",
        "facility",
        "domain",
        "source_local_scope",
        "overburden",
        "flight",
        "defeat",
        "confiscation",
        "tax_seizure",
        "faction_claim",
        "legal_inspection",
        "theft",
        "container_damage",
        "platform_destruction",
        "hazard_exposure",
        "spoilage",
        "abandonment",
        "failed_transport",
        "source_local_trigger",
        "lost",
        "damaged",
        "stolen",
        "claimed_by_other",
        "converted_to_unresolved_pressure",
        "recoverable_with_cost",
        "recoverable_with_project",
        "recoverable_with_operation",
        "destroyed",
        "quarantined",
        "source_local_result",
    ]:
        assert phrase in lowered


def test_b04_separates_possession_access_ownership_legal_readiness_storage_quick_access_custody_and_burden() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "separate possession, access, ownership, legal permission, readiness, storage, quick access, custody, and burden",
        "possessed does not mean accessible",
        "accessible does not mean owned",
        "owned does not mean legal to carry",
        "stored does not mean safe",
        "safe does not mean immediately available",
        "quick access is not general capacity",
        "quick access does not decide final action timing",
        "legal permission does not prove immediate access, safety, or readiness",
    ]:
        assert phrase in lowered


def test_b04_includes_storage_transfer_decay_loss_and_recovery_procedure() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "storage, container, cache, vault, vehicle, platform, and facility procedure",
        "storage procedure applies to container_stored, vehicle_stored, platform_stored, facility_stored, banked, vaulted, cached, hidden, escrowed, leased_storage, digital_or_pattern_stored, and source_local_holding",
        "transfer, handoff, requisition, escrow, impoundment, and shared-possession procedure",
        "shared possession must state who can access, sell, spend, abandon, divide, bear burden, receive trace, or accept responsibility",
        "decay, spoilage, maintenance, upkeep, and stability routing",
        "inventory loss requires a lawful trigger and owner-file support",
        "recovery and retrieval procedure",
        "distinguish recovery from immediate retrieval, quick access, ownership, legality, safety, and final action timing",
    ]:
        assert phrase in lowered


def test_b04_rejects_final_inventory_capacity_economy_legal_runtime_ledger_and_database_ownership() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "final inventory schema",
        "final inventory capacity math",
        "final weight/slot/encumbrance rules",
        "final economy law",
        "final legal code",
        "final runtime inventory state",
        "final event-sourced inventory ledger",
        "final ownership database",
        "must not define final carrying-capacity math",
        "must not define final legal code, faction law, licensing, tax, contraband, confiscation rules, or final economy law",
        "must not invent loss/recovery tables",
    ]:
        assert phrase in lowered


def test_b04_rejects_runtime_state_event_command_lifecycle_ownership() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "b04 rejects runtime state/event/command lifecycle ownership",
        "runtime entity/component/event/state schemas",
        "event-sourced state model",
        "state delta validator",
        "command lifecycle implementation",
        "context packet compiler",
        "backend validation",
        "database contracts",
        "event logs",
        "hidden-information runtime state",
        "persistent campaign state",
        "live-play behavior must not consume b04 procedure as runtime authority",
    ]:
        assert phrase in lowered


def test_b04_rejects_c_family_field_invention_and_schema_content_ownership() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "must not invent c-family fields",
        "c-family schema fields",
        "c01-c14 schema contents",
        "missing schema coverage must produce `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` rather than improvised schema",
        "must not invent c-family fields, donor field names, donor record formats, inventory database rows",
    ]:
        assert phrase in lowered


def test_b04_rejects_donor_inventory_storage_economy_systems_as_astra_defaults() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "donor inventory/storage/economy systems are evidence only",
        "donor weight rules, slot rules, encumbrance systems, coin weight, treasure tables, item rarity economies, attunement slots, magic bags, bags of holding, spatial rings, pocket dimensions, pattern storage, cyberdeck loadouts, cargo statblocks, vehicle cargo ratings, requisition systems, post-scarcity storage systems, bank ledgers, vault rules, tax rules, legal codes, licensing systems, contraband lists, and ownership databases are donor evidence only",
        "source-local donor inventory/storage/economy handling",
        "avoid importing donor inventory/equipment/economy systems as astra defaults through b04",
        "avoid promoting repeated donor pressure into final capacity math, final economy law, final legal code, final runtime inventory state, final event-sourced inventory ledger, final ownership database, or accepted canon",
    ]:
        assert phrase in lowered


def test_b04_includes_inventory_custody_burden_state_delta_routing() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "inventory/custody/burden state-delta routing",
        "every meaningful inventory/custody/burden event must route at least one delta to a recognized owner",
        "no_delta_required",
        "owner_routed",
        "transition_note",
        "source_local_retained_effect",
        "quarantined_unresolved_delta",
        "owner_file_escalation",
    ]:
        assert phrase in lowered


def test_b04_includes_source_local_quarantine_escalation_and_review() -> None:
    text = b04_text()
    lowered = text.lower()
    for marker in [
        "Source-local donor inventory/storage/economy handling",
        "pending_schema",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
        "source_local_review",
        "source-local boundary",
    ]:
        assert marker in text
    assert "unclassifiable inventory/custody/burden records are quarantined or escalated, not normalized by invention" in lowered


def test_b04_references_d_series_only_as_draft_source_pack_reference_material() -> None:
    text = b04_text()
    lowered = text.lower()
    for marker in [
        "D00-03_state_delta_commit_protocol.md",
        "D09-00_layered_object_state_architecture.md",
        "D09-02_weapons_armor_tools_foci_consumables_and_materials.md",
        "D17-04_inventory_storage_carrying_custody_quick_access_and_burden_procedure.md",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
    ]:
        assert marker in text
    assert "d00, d09, d17, and d19 source-pack files are referenced only as draft source-pack/reference material" in lowered
    assert "not current doctrine authority" in lowered


def test_b04_does_not_require_define_create_or_promote_b05_b11() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "b04 does not require, define, create, or promote b05-b11",
        "does not assume b05 content",
        "does not make b05-b11 current doctrine",
    ]:
        assert phrase in lowered


def test_b04_does_not_require_define_create_or_promote_c01_c14() -> None:
    lowered = b04_text().lower()
    for phrase in [
        "does not require, define, create, or promote c01-c14",
        "does not require, define, create, or promote those later files or schemas",
        "rejects c-family field invention and c01-c14 schema-content ownership",
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


def _registry_scalar(file_id: str, key: str) -> str:
    prefix = f"  {key}: "
    for line in _registry_record_block(file_id).splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip().strip("'\"")
    raise AssertionError(f"Missing {key} for {file_id}")


def test_registry_status_is_not_promoted_to_current() -> None:
    registry_text = read_utf8(REGISTRY_PATH)
    assert "- file_id: B04\n" not in registry_text

    forbidden_promoted_statuses = {
        "current",
        "tested_minimum",
        "stable_for_family",
        "stable_cross_family",
    }
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        assert _registry_scalar(file_id, "status") not in forbidden_promoted_statuses
        assert _registry_scalar(file_id, "test_status") not in forbidden_promoted_statuses
        assert _registry_scalar(file_id, "authority_level") not in {"canon-current", "runtime-ready", "schema-current"}
        assert "canon-current" not in block
        assert "runtime-ready" not in block

    assert _registry_scalar("C00", "status") == "draft"
    assert _registry_scalar("C01", "status") == "draft"
    assert _registry_scalar("C01", "authority_level") == "schema-draft"
    assert _registry_scalar("C01", "test_status") == "designed"
    assert _registry_scalar("C01", "review_status") == "not_reviewed"

    for number in range(2, 15):
        file_id = f"C{number:02d}"
        assert _registry_scalar(file_id, "status") not in forbidden_promoted_statuses
        assert _registry_scalar(file_id, "test_status") not in forbidden_promoted_statuses
