from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

B03_PATH = ROOT / "docs" / "doctrine" / "operations" / "batch_b" / "B03_item_gear_equipment_and_asset_use_procedure.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B03 owns",
    "## 4. What B03 must not own",
    "## 5. Non-collapse rule",
    "## 6. Object-system construct and operational object-use definitions",
    "## 7. Object-use intake procedure",
    "## 8. Holding, access, readiness, and custody triage",
    "## 9. Function-family classification",
    "## 10. Use-mode declaration procedure",
    "## 11. Compatibility and permission checks",
    "## 12. Depletion, charge, ammunition, fuel, use-limit, and support-burden routing",
    "## 13. Object condition, failure, breakage, overload, contamination, and loss routing",
    "## 14. Inventory, storage, quick-access, custody, and burden handoff rules",
    "## 15. Object-use resolution trigger routing",
    "## 16. Object-use state-delta routing",
    "## 17. Owner-file handoff rules",
    "## 18. Batch B to C00/C-family handoff rules",
    "## 19. Missing-schema fallback and quarantine/escalation",
    "## 20. Source-local donor equipment/object-system handling",
    "## 21. Runtime boundary",
    "## 22. Canon boundary",
    "## 23. Live-play/training boundary",
    "## 24. Examples of good and bad B03 usage",
    "## 25. Minimum tests or assertions",
    "## 26. Acceptance criteria",
    "## 27. Follow-up handoff to B04",
]


def b03_text() -> str:
    return read_utf8(B03_PATH)


def test_b03_file_exists_at_expected_path() -> None:
    assert B03_PATH.exists()
    assert B03_PATH.is_file()


def test_b03_required_sections_are_present() -> None:
    text = b03_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b03_declares_ownership_and_non_ownership() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "object-use intake procedure after b02 action declaration",
        "object-system construct classification for operational use",
        "equipped, worn, carried, held, installed, quick-access, stored, bound, mounted, platform-held, and source-local holding checks",
        "readiness/access/use-state triage",
        "object access and compatibility checks",
        "consumable/depletion/charge/ammunition/fuel/use-limit routing as owner handoff",
        "object failure, breakage, depletion, overload, contamination, jam, misalignment, or rejection routing",
        "object use to resolution-owner trigger routing",
        "object use to state-delta owner routing",
    ]:
        assert phrase in lowered

    for phrase in [
        "final object schema",
        "c-family schema fields",
        "c01-c14 schema contents",
        "final weapon stats",
        "final armor stats",
        "final item stats",
        "final damage dice",
        "final attack math",
        "final defense math",
        "final armor class logic",
        "final skill bonuses",
        "final equipment bonus math",
        "final item rarity/tier economy",
        "final inventory capacity math",
        "final weight/slot/encumbrance rules",
        "final quick-access action economy",
        "final ammunition/fuel/charge/reload math",
        "final crafting, repair, salvage, upgrade, or modification procedure",
        "final market price, treasure, reward, requisition, or economy law",
        "runtime inventory state",
        "runtime entity/component/event/state schemas",
        "persistent campaign state",
        "command lifecycle implementation",
        "context packet compiler",
        "hidden-information runtime state",
        "live-play narration behavior",
        "final canon promotion",
        "accepted lexicon terms",
        "sourcebook prose",
        "donor equipment systems as astra defaults",
    ]:
        assert phrase in lowered


def test_b03_references_b01_and_b02_as_upstream_batch_b_context() -> None:
    lowered = b03_text().lower()
    assert "b01_scene_encounter_and_activity_procedure.md" in lowered
    assert "b02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md" in lowered
    assert "upstream batch b context" in lowered
    assert "upstream batch b scene, activity, encounter" in lowered
    assert "must build on them, not rewrite them" in lowered


def test_b03_includes_c00_handoff_language_and_block() -> None:
    text = b03_text()
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


def test_b03_includes_object_use_routing_note_as_doctrine_facing_only() -> None:
    text = b03_text()
    lowered = text.lower()
    for marker in [
        "object_use_routing_note",
        "object_use_state: object_use_declared | object_use_clarified | object_access_confirmed | object_access_blocked | object_ready | object_not_ready | object_equipped | object_worn | object_carried | object_stored | object_quick_access | object_bound_to_actor | object_installed | object_mounted | object_platform_held | object_source_local | object_use_resolution_triggered | object_use_owner_handoff_required | object_use_no_roll_required | object_use_no_delta_required | object_use_delta_routed | object_use_quarantined_gap",
        "actor_ref: string | null",
        "object_ref: string | null",
        "object_function_family: weapon | armor_protection | tool_instrument | focus_channel | consumable | material_component | catalyst | implant_prosthetic | vehicle_platform | anchor_vessel | intelligent_object | source_local_object | mixed | unknown",
        "use_mode: wield | wear | activate | consume | expend | install | channel_through | repair_with | modify_with | throw | deploy | reload | charge | discharge | mount | unmount | store | retrieve | conceal | reveal | hand_off | requisition | source_local_use | other",
        "holding_or_access_state: carried_on_person | equipped | worn | quick_access | packed | container_stored | vehicle_stored | platform_stored | facility_stored | hidden | faction_held | requisition_held | impounded | bound_to_actor | source_local_holding | unknown",
        "readiness_status: ready | not_ready | access_blocked | permission_blocked | compatibility_blocked | depleted | damaged | unstable | contaminated | overloaded | jammed | misaligned | source_local_only | unknown",
        "delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation",
    ]:
        assert marker in text
    for phrase in [
        "b03-specific lightweight doctrine-facing block",
        "not a runtime schema",
        "not a backend event",
        "not a command object",
        "not a c-family record",
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


def test_b03_includes_object_system_construct_and_object_use_definitions() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "an `object-system construct` is any doctrine-facing construct",
        "an `operational object-use` is a declared use",
        "physical, digital, spiritual, biological, technological, social, legal, metaphysical, platform, vehicle, container, implant, relic, material, or source-local object",
        "begins only after upstream batch b context",
        "these terms are b03 doctrine vocabulary only",
    ]:
        assert phrase in lowered


def test_b03_includes_holding_access_readiness_custody_function_and_use_mode_procedure() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "holding triage asks where and how the object is held now",
        "readiness triage asks whether the object can be used",
        "custody triage asks who may hold, access, transfer",
        "function-family classification",
        "weapon",
        "armor_protection",
        "tool_instrument",
        "focus_channel",
        "consumable",
        "material_component",
        "catalyst",
        "implant_prosthetic",
        "vehicle_platform",
        "anchor_vessel",
        "intelligent_object",
        "source_local_object",
        "use-mode procedure",
        "wield",
        "wear",
        "activate",
        "consume",
        "expend",
        "install",
        "channel_through",
        "repair_with",
        "modify_with",
        "throw",
        "deploy",
        "reload",
        "charge",
        "discharge",
        "mount",
        "unmount",
        "store",
        "retrieve",
        "conceal",
        "reveal",
        "hand_off",
        "requisition",
        "source_local_use",
    ]:
        assert phrase in lowered


def test_b03_rejects_final_item_equipment_math_and_runtime_inventory_state() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "final object schema",
        "final item stats",
        "final weapon stats",
        "final armor stats",
        "final damage dice",
        "final attack math",
        "final defense math",
        "final armor class logic",
        "final inventory capacity math",
        "final market price, treasure, reward, requisition, or economy law",
        "final crafting, repair, salvage, upgrade, or modification procedure",
        "runtime inventory state",
        "must not define final ammunition/fuel/charge/reload math",
        "must not define final inventory capacity math",
        "must not define final market price, treasure, reward, requisition, or economy law",
        "must not define final harm consequences from object use or object failure",
    ]:
        assert phrase in lowered


def test_b03_rejects_runtime_state_event_command_lifecycle_ownership() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "b03 rejects runtime state/event/command lifecycle ownership",
        "runtime entity/component/event/state schemas",
        "runtime state/schema/event/command lifecycle ownership",
        "event-sourced state model",
        "state delta validator",
        "command lifecycle implementation",
        "context packet compiler",
        "backend validation",
        "database contracts",
        "event logs",
        "hidden-information runtime state",
        "persistent campaign state",
        "live-play behavior must not consume b03 procedure as runtime authority",
    ]:
        assert phrase in lowered


def test_b03_rejects_c_family_field_invention_and_schema_content_ownership() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "must not invent c-family fields",
        "must not require, define, create, or promote c01-c14 schemas or c01-c14 schema contents",
        "c-family schema fields",
        "c01-c14 schema contents",
        "missing schema coverage must produce `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` rather than improvised schema",
        "must not invent c-family fields, donor field names, donor record formats, object item schemas",
    ]:
        assert phrase in lowered


def test_b03_rejects_donor_equipment_object_system_formats_as_astra_defaults() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "donor equipment systems are evidence only",
        "donor weapon damage dice, armor class rules, item rarity, attunement slots, item slots, cyberware capacity, humanity loss, starship statblocks, mech hardpoints, drone caps, crafting dcs, treasure tables, and requisition ratings are donor evidence only",
        "source-local donor object system detected",
        "do not import donor item/equipment/object systems as astra defaults through b03",
        "repeated donor pressure does not promote donor equipment/object-system formats to astra law",
    ]:
        assert phrase in lowered


def test_b03_includes_resolution_trigger_and_state_delta_routing() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "a declared object use is not automatically a roll",
        "b03 follows b02 no-roll and resolution-trigger procedure",
        "object_use_resolution_triggered",
        "object_resolution_needed",
        "when uncertainty/consequence requires resolution",
        "every meaningful object use must route at least one delta to a recognized owner",
        "object_use_delta_routed",
        "object_use_no_delta_required",
        "quarantined_unresolved_delta",
        "owner_file_escalation",
    ]:
        assert phrase in lowered


def test_b03_includes_burden_custody_quick_access_storage_principles() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "possessed does not mean accessible",
        "accessible does not mean owned",
        "owned does not mean legal to carry",
        "stored does not mean safe",
        "quick access is not general capacity",
        "containers do not erase burden unless an owner file or source-local rule supports it",
        "quick access is not general capacity and does not decide final action timing",
        "inventory, storage, quick-access, custody, and burden handoff rules",
    ]:
        assert phrase in lowered


def test_b03_includes_source_local_quarantine_escalation_and_review() -> None:
    text = b03_text()
    lowered = text.lower()
    for marker in [
        "Source-local donor equipment/object-system handling",
        "pending_schema",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
        "object_use_quarantined_gap",
        "source_local_review",
        "source-local boundary",
    ]:
        assert marker in text
    assert "unclassifiable object-use records are quarantined or escalated, not normalized by invention" in lowered


def test_b03_references_d_series_only_as_draft_source_pack_reference_material() -> None:
    text = b03_text()
    lowered = text.lower()
    for marker in [
        "D00-03_state_delta_commit_protocol.md",
        "D02-00_resolution_architecture_and_owner_boundaries.md",
        "D03_01_power_economy_lattice.md",
        "D09-00_layered_object_state_architecture.md",
        "D09-02_weapons_armor_tools_foci_consumables_and_materials.md",
        "D17-04_inventory_storage_carrying_custody_quick_access_and_burden_procedure.md",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
    ]:
        assert marker in text
    assert "d00, d02, d03, d09, d17, and d19 source-pack files are referenced only as draft source-pack/reference material" in lowered
    assert "not current doctrine authority" in lowered


def test_b03_does_not_require_define_create_or_promote_b04_b11() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "b03 does not require, define, create, or promote b04-b11",
        "does not require, define, create, or promote b04-b11",
        "rather than drafting or assuming b04-b11 content",
    ]:
        assert phrase in lowered


def test_b03_does_not_require_define_create_or_promote_c01_c14() -> None:
    lowered = b03_text().lower()
    for phrase in [
        "must not require, define, create, or promote c01-c14 schemas or c01-c14 schema contents",
        "b03 does not require, define, create, or promote c01-c14",
        "does not require, define, create, or promote c01-c14",
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
    assert "- file_id: B03\n" not in registry_text
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        assert "  status: current" not in block
    assert "  status: draft" in _registry_record_block("C00")
    for number in range(1, 15):
        assert "  status: todo" in _registry_record_block(f"C{number:02d}")
