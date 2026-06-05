from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RT010_PATH = ROOT / "docs" / "doctrine" / "control" / "RT010_inventory_item_vehicle_asset_owner_scaffold.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_pr_g_owner_scaffold_file_exists() -> None:
    assert RT010_PATH.exists()


def test_scaffold_references_remediation_priority_ledger() -> None:
    text = read(RT010_PATH)
    assert "REMEDIATION-PRIORITY-LEDGER-001" in text
    assert "owner scaffold" in text


def test_rt010_references_dependencies_sources_and_invariants() -> None:
    text = read(RT010_PATH)
    for phrase in [
        "RT-010",
        "RT-001",
        "RT-002",
        "RT-003",
        "RT-004",
        "RT-005",
        "RT-006",
        "RT-008",
        "RT-009",
        "RT-011",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
        "B03",
        "C02",
        "C04",
        "C08",
        "C03",
        "C12",
        "SM00",
        "backend-first language",
        "hidden-info language",
        "backend-first model-interchangeability invariant",
    ]:
        assert phrase in text


def test_rt010_states_required_downstream_controls() -> None:
    text = read(RT010_PATH)
    for phrase in [
        "Item/gear/vehicle records are not persistent owned instances until backend-owned state, identity, custody, provenance, validation, and event paths exist",
        "Asset use must remain downstream of RT-001 command lifecycle",
        "Resource spend, loss, damage, repair, fuel, ammo, charge, durability, cost, reward, and consequence pressure remains downstream of RT-002 and RT-003 as applicable",
        "Ability/effect-bearing assets must coordinate with RT-004 before mechanical effects can be resolved",
        "Visible inventory/loadout/cargo/vehicle facts must route through RT-005 before narration",
        "Generated assets require RT-008 provenance/recurrence controls before persistence",
        "Random loot/table/oracle asset outputs require RT-009 authority before commitment",
    ]:
        assert phrase in text


def test_rt010_prohibits_llm_inventory_item_vehicle_authority() -> None:
    text = read(RT010_PATH)
    for phrase in [
        "create item instances as backend truth",
        "resolve equipment effects",
        "determine slot/loadout authority",
        "track charges or durability or cooldowns or ammunition",
        "manage cargo or crew or capacity state",
        "decide vehicle movement or damage or repair",
        "transfer custody or ownership",
        "commit acquisition or crafting or salvage results",
        "invent item properties as durable facts",
        "generate items or vehicles as persistent records",
        "promote item or vehicle canon",
        "bypass backend validation/reviewer approval",
        "treat inventory narration as backend state commitment",
    ]:
        assert phrase in text


def test_rt010_names_only_conceptual_placeholders() -> None:
    text = read(RT010_PATH)
    for phrase in [
        "item_instance_pending",
        "equipment_slot_candidate",
        "custody_state_pending",
        "loadout_authority_required",
        "charge_durability_tracking_pending",
        "cooldown_state_pending",
        "ammunition_tracking_pending",
        "cargo_capacity_pending",
        "crew_state_pending",
        "vehicle_movement_pending",
        "vehicle_damage_state_pending",
        "repair_authority_pending",
        "item_effect_validation_required",
        "asset_provenance_required",
        "inventory_projection_pending",
        "conceptual placeholders only",
        "not final schemas",
        "not inventory runtime",
        "not item instance models",
        "not equipment effect resolution",
        "not slot/loadout mechanics",
        "not charge/durability/cooldown math",
        "not vehicle movement",
        "not cargo/crew/capacity state",
        "not damage/repair math",
        "not generator",
        "not validator",
        "not event model",
        "not live-play authorization",
    ]:
        assert phrase in text


def test_scaffold_includes_explicit_non_implementation_guardrails() -> None:
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
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in text


def test_registry_tracks_pr_g_scaffold_and_guardrails() -> None:
    text = read(REGISTRY_PATH)
    for phrase in [
        "REMEDIATION-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SCAFFOLD-001",
        "owner scaffold only",
        "no doctrine rewrite",
        "no runtime implementation",
        "no schema implementation",
        "no command IR implementation",
        "no math implementation",
        "no validator implementation",
        "no generator implementation",
        "no inventory runtime",
        "no item instance creation",
        "no equipment effect resolution",
        "no vehicle movement implementation",
        "no cargo state implementation",
        "no damage/repair implementation",
        "no persistence writer implementation",
        "no retrieval index implementation",
        "no context-packet compiler implementation",
        "no canon promotion",
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in text


def test_no_file_claims_to_implement_runtime_or_training_behavior() -> None:
    text = read(RT010_PATH).lower()
    for forbidden in [
        "this scaffold implements inventory runtime",
        "this scaffold implements item instance",
        "this scaffold implements equipment effect",
        "this scaffold implements slot mechanics",
        "this scaffold implements vehicle movement",
        "this scaffold implements cargo state",
        "this scaffold implements damage math",
        "this scaffold implements repair math",
        "this scaffold implements validators",
        "this scaffold implements runtime",
        "this scaffold implements event models",
        "this scaffold implements persistence writers",
        "this scaffold implements retrieval indexes",
        "this scaffold implements context-packet compilers",
        "this scaffold implements live-play prompts",
        "this scaffold implements training behavior",
    ]:
        assert forbidden not in text
