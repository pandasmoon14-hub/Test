from pathlib import Path


TEMPLATE_PATH = Path("configs/handoff/donor_family_templates.yaml")

REQUIRED_TEMPLATE_IDS = {
    "d20_class_level_fantasy",
    "d20_scifi_science_fantasy",
    "universal_toolkit_or_generic_engine",
    "point_buy_anime_supers",
    "narrative_tag_aspect",
    "forged_pbta_clock_playbook",
    "osr_survival_sandbox",
    "lifepath_trade_starship",
    "tactical_mech_vehicle_platform",
    "cyberpunk_biotech_transhuman",
    "cultivation_wuxia_martial",
    "horror_investigation_social",
    "bestiary_statblock_heavy",
    "setting_world_guide",
    "adventure_path_scenario",
    "random_table_loot",
    "crafting_economy_salvage",
    "solo_procedure_heavy",
    "companion_summon_pet",
    "domain_faction_kingdom_management",
    "mass_battle_war_campaign",
    "magic_spell_power_compendium",
    "gear_item_catalog",
    "map_diagram_heavy",
    "scanned_or_ocr_heavy",
    "unclassified_or_mixed_donor_family",
}

REQUIRED_FIELDS = {
    "template_id",
    "label",
    "description",
    "priority",
    "detection_signals",
    "expected_construct_families",
    "packet_selection_targets",
    "extraction_risks",
    "likely_quarantine_reasons",
    "conversion_prompt_additions",
    "review_notes",
    "escalation_owner_hint",
}

LIST_FIELDS = {
    "detection_signals",
    "expected_construct_families",
    "packet_selection_targets",
    "extraction_risks",
    "likely_quarantine_reasons",
    "conversion_prompt_additions",
    "review_notes",
}


def _parse_simple_yaml_templates(text: str) -> dict:
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    assert lines and lines[0] == "templates:"
    templates = {}
    current_key = None
    current_obj = None

    for ln in lines[1:]:
        if ln.startswith("  ") and not ln.startswith("    ") and ln.endswith(":"):
            current_key = ln.strip()[:-1]
            current_obj = {}
            templates[current_key] = current_obj
            continue

        assert current_obj is not None, f"field without template: {ln}"
        assert ln.startswith("    "), f"unexpected indentation: {ln}"
        field_line = ln.strip()
        field, raw = field_line.split(":", 1)
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            value = [] if not inner else [item.strip() for item in inner.split(",")]
        elif raw == "true":
            value = True
        elif raw == "false":
            value = False
        elif raw.isdigit():
            value = int(raw)
        else:
            value = raw
        current_obj[field] = value
    return templates


def _load_templates():
    assert TEMPLATE_PATH.exists(), f"missing template file: {TEMPLATE_PATH}"
    return _parse_simple_yaml_templates(TEMPLATE_PATH.read_text(encoding="utf-8"))


def test_yaml_parses_successfully():
    templates = _load_templates()
    assert templates


def test_required_template_ids_exist():
    templates = _load_templates()
    missing = REQUIRED_TEMPLATE_IDS - set(templates.keys())
    assert not missing, f"missing template ids: {sorted(missing)}"


def test_every_template_has_required_fields():
    templates = _load_templates()
    for key, template in templates.items():
        assert isinstance(template, dict), f"template {key} must be a mapping"
        missing = REQUIRED_FIELDS - set(template.keys())
        assert not missing, f"template {key} missing fields: {sorted(missing)}"


def test_list_fields_are_lists_not_strings():
    templates = _load_templates()
    for key, template in templates.items():
        for field in LIST_FIELDS:
            value = template[field]
            assert isinstance(value, list), f"template {key} field {field} must be list"


def test_template_id_matches_key_or_declared_id():
    templates = _load_templates()
    for key, template in templates.items():
        assert template["template_id"] == key, (
            f"template_id mismatch for {key}: {template['template_id']}"
        )


def test_unclassified_template_marked_fallback_not_normal_target():
    templates = _load_templates()
    fallback = templates["unclassified_or_mixed_donor_family"]
    assert fallback.get("fallback_only") is True
    review_notes = " ".join(fallback.get("review_notes", [])).lower()
    assert "not a normal target" in review_notes


def test_no_template_promotes_donor_content_to_canon():
    templates = _load_templates()
    forbidden_phrases = [
        "promote to canon",
        "direct canon adoption",
        "donor canon adoption",
        "merge into canon",
    ]
    for key, template in templates.items():
        blob = " ".join(str(v) for v in template.values()).lower()
        for phrase in forbidden_phrases:
            assert phrase not in blob, f"template {key} contains forbidden phrase: {phrase}"
