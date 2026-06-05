from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RT010_PATH = ROOT / "docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md"
REGISTRY_PATH = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
B03_REQUESTED_PATH = ROOT / "docs/doctrine/operations/batch_b/B03_item_gear_use_and_inventory_interaction_procedure.md"
B03_ACTUAL_PATH = ROOT / "docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md"
C04_REQUESTED_PATH = ROOT / "docs/doctrine/schema/C04_relic_implant_installable_asset_record_schema.md"
C04_ACTUAL_PATH = ROOT / "docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_rt010_owner_scaffold_file_exists() -> None:
    assert RT010_PATH.exists()


def test_rt010_references_ledger_track_dependencies_and_audits() -> None:
    text = read(RT010_PATH)
    for phrase in [
        "REMEDIATION-PRIORITY-LEDGER-001",
        "RT-010",
        "RT-001",
        "RT-002",
        "RT-003",
        "RT-004",
        "RT-005",
        "RT-008",
        "RT-009",
        "RT-011",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
    ]:
        assert phrase in text


def test_rt010_references_sources_and_invariants() -> None:
    text = read(RT010_PATH)
    assert not B03_REQUESTED_PATH.exists()
    assert B03_ACTUAL_PATH.exists()
    assert not C04_REQUESTED_PATH.exists()
    assert C04_ACTUAL_PATH.exists()
    for phrase in [
        "B03_item_gear_use_and_inventory_interaction_procedure.md` is absent",
        "B03_item_gear_equipment_and_asset_use_procedure.md",
        "C02",
        "C03",
        "C04_relic_implant_installable_asset_record_schema.md` is absent",
        "C04_relic_implant_installable_asset_schema.md",
        "C08",
        "C12",
        "SM00",
        "Roadmap backend-first language",
        "backend-first language",
        "Backend-first model-interchangeability invariant",
        "backend-first model-interchangeability invariant",
    ]:
        assert phrase in text


def test_rt010_states_required_dependency_relationships() -> None:
    text = read(RT010_PATH)
    for phrase in [
        "item/gear/vehicle records are not persistent owned instances until backend-owned state, identity, custody, provenance, validation, and event paths exist",
        "Asset use is downstream of RT-001 command lifecycle",
        "resource spend, loss, damage, repair, fuel, ammo, charge, durability, cost, reward, and consequence pressure remains downstream of RT-002 and RT-003 as applicable",
        "Ability/effect-bearing assets coordinate with RT-004 before mechanical effects can be resolved",
        "Visible inventory/loadout/cargo/vehicle facts route through RT-005 before narration",
        "Generated assets require RT-008 provenance/recurrence controls before persistence",
        "Random loot/table/oracle asset outputs require RT-009 authority before commitment",
    ]:
        assert phrase in text


def test_rt010_prohibits_llm_asset_authority() -> None:
    text = read(RT010_PATH)
    for phrase in [
        "create durable item, gear, relic, implant, installable, vehicle, ship, platform, cargo, or asset records as backend truth",
        "assign persistent item or vehicle IDs",
        "change inventory, custody, ownership, equipment, loadout, cargo, crew, or storage state",
        "spend charges, ammo, fuel, uses, durability, or cooldowns",
        "apply item effects as mechanical truth",
        "mutate vehicle/platform integrity, damage, movement, position, cargo, crew, or repair state",
        "decide salvage, crafting, repair, requisition, price, value, reward, or loss outcomes",
        "generate persistent assets without RT-008 provenance/recurrence controls",
        "select random loot/table outputs without RT-009 backend RNG/table authority",
        "bypass backend validation/reviewer approval",
        "treat equipment narration as backend inventory or asset state",
    ]:
        assert phrase in text


def test_rt010_names_only_conceptual_placeholders() -> None:
    text = read(RT010_PATH)
    for phrase in [
        "asset_record_reference",
        "item_instance_pending",
        "custody_state_pending",
        "equipped_slot_pending",
        "loadout_state_pending",
        "charge_state_pending",
        "durability_state_pending",
        "cooldown_or_recharge_pending",
        "cargo_manifest_pending",
        "crew_assignment_pending",
        "vehicle_integrity_pending",
        "movement_state_pending",
        "repair_or_salvage_candidate",
        "installable_attachment_pending",
        "asset_effect_binding_required",
        "asset_generation_prohibited",
        "conceptual placeholders only",
        "not final schemas",
        "not inventory runtime",
        "not item instances",
        "not item effects",
        "not vehicle runtime",
        "not cargo system",
        "not crew system",
        "not repair mechanics",
        "not installable schema",
        "not condition/damage model",
        "not command IR",
        "not persistence writer",
        "not generator",
        "not validator",
        "not live-play authorization",
    ]:
        assert phrase in text


def test_rt010_includes_explicit_non_implementation_guardrails() -> None:
    text = read(RT010_PATH)
    for phrase in [
        "planning/control only",
        "does not implement remediation",
        "Explicit non-implementation statement",
        "no doctrine rewrite",
        "no runtime implementation",
        "no schema implementation",
        "no command IR implementation",
        "no math implementation",
        "no validator implementation",
        "no generator implementation",
        "no inventory implementation",
        "no item instance creation",
        "no durable asset record creation",
        "no item effect implementation",
        "no vehicle/platform runtime implementation",
        "no cargo or crew system implementation",
        "no repair/salvage/crafting implementation",
        "no ownership/custody mutation",
        "no charge/ammo/fuel/durability/cooldown spend",
        "no persistence writer implementation",
        "no retrieval index implementation",
        "no context-packet compiler implementation",
        "no canon promotion",
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in text


def test_registry_tracks_pr_g_scaffold_and_guardrails() -> None:
    text = read(REGISTRY_PATH)
    for phrase in [
        "REMEDIATION-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SCAFFOLD-001",
        "RT010_inventory_item_vehicle_asset_owner_scaffold.md",
        "owner scaffold only",
        "no doctrine rewrite",
        "no runtime implementation",
        "no schema implementation",
        "no command IR implementation",
        "no math implementation",
        "no validator implementation",
        "no generator implementation",
        "no inventory implementation",
        "no item instance creation",
        "no durable asset record creation",
        "no item effect implementation",
        "no vehicle/platform runtime implementation",
        "no cargo or crew system implementation",
        "no repair/salvage/crafting implementation",
        "no ownership/custody mutation",
        "no charge/ammo/fuel/durability/cooldown spend",
        "no persistence writer implementation",
        "no retrieval index implementation",
        "no context-packet compiler implementation",
        "no canon promotion",
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in text


def test_no_file_claims_to_implement_asset_runtime_or_training_behavior() -> None:
    for path in [RT010_PATH, REGISTRY_PATH]:
        text = read(path).lower()
        for forbidden in [
            "this scaffold implements inventory runtime",
            "this scaffold implements item instances",
            "this scaffold implements item effects",
            "this scaffold implements vehicle runtime",
            "this scaffold implements cargo system",
            "this scaffold implements crew system",
            "this scaffold implements repair mechanics",
            "this scaffold implements installable schema",
            "this scaffold implements condition/damage model",
            "this scaffold implements validators",
            "this scaffold implements runtime",
            "this scaffold implements persistence writers",
            "this scaffold implements retrieval indexes",
            "this scaffold implements context-packet compilers",
            "this scaffold implements live-play prompts",
            "this scaffold implements training behavior",
        ]:
            assert forbidden not in text
