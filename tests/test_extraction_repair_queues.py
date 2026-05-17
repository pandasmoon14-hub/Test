from pathlib import Path
import json


YAML_PATH = Path("configs/handoff/extraction_repair_queues.yaml")
SCHEMA_PATH = Path("schemas/handoff/extraction_repair_queue.schema.json")

REQUIRED_QUEUE_IDS = {
    "ocr_required",
    "scanned_or_image_only",
    "underparsed_page",
    "empty_or_near_empty_page",
    "mojibake_text_cleanup",
    "table_flattening",
    "malformed_random_table",
    "statblock_underparse",
    "map_diagram_review",
    "image_or_visual_dependency",
    "column_merge_or_split_failure",
    "header_footer_noise",
    "sidebar_or_callout_ordering",
    "packet_boundary_ambiguity",
    "missing_page_truth",
    "artifact_validation_error",
    "unreadable_or_corrupt_pdf",
    "duplicate_or_conflicting_page",
    "low_confidence_extraction",
    "source_metadata_gap",
    "conversion_blocked_by_extraction",
    "manual_review_required",
}

REQUIRED_FIELDS = {
    "queue_id",
    "label",
    "description",
    "severity",
    "stage",
    "detection_signals",
    "routing_action",
    "blocks_conversion",
    "allows_intake_only",
    "expected_artifacts",
    "reviewer_action",
    "escalation_owner_hint",
    "notes",
}

VALID_SEVERITIES = {"info", "warning", "repair_required", "blocking"}
VALID_STAGES = {
    "extraction",
    "packet_planning",
    "packet_building",
    "conversion_intake",
    "validation",
    "aggregation",
}

LIST_FIELDS = {"detection_signals", "expected_artifacts"}
BOOL_FIELDS = {"blocks_conversion", "allows_intake_only"}


def _parse_simple_yaml_records(text: str, root_key: str) -> dict:
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    assert lines and lines[0] == f"{root_key}:"
    records = {}
    current_key = None
    current_obj = None

    for ln in lines[1:]:
        if ln.startswith("  ") and not ln.startswith("    ") and ln.endswith(":"):
            current_key = ln.strip()[:-1]
            current_obj = {}
            records[current_key] = current_obj
            continue

        assert current_obj is not None, f"field without record: {ln}"
        assert ln.startswith("    "), f"unexpected indentation: {ln}"
        field, raw = ln.strip().split(":", 1)
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
    return records


def _load_queues() -> dict:
    assert YAML_PATH.exists(), f"missing queue config: {YAML_PATH}"
    return _parse_simple_yaml_records(YAML_PATH.read_text(encoding="utf-8"), "queues")


def test_yaml_parses_successfully():
    queues = _load_queues()
    assert queues


def test_json_schema_parses_successfully():
    assert SCHEMA_PATH.exists(), f"missing schema: {SCHEMA_PATH}"
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert isinstance(schema, dict)
    assert schema.get("type") == "object"


def test_all_required_queue_ids_exist():
    queues = _load_queues()
    missing = REQUIRED_QUEUE_IDS - set(queues.keys())
    assert not missing, f"missing queue ids: {sorted(missing)}"


def test_every_queue_has_all_required_fields():
    queues = _load_queues()
    for key, queue in queues.items():
        missing = REQUIRED_FIELDS - set(queue.keys())
        assert not missing, f"queue {key} missing fields: {sorted(missing)}"


def test_severity_and_stage_are_valid():
    queues = _load_queues()
    for key, queue in queues.items():
        assert queue["severity"] in VALID_SEVERITIES, f"invalid severity for {key}"
        assert queue["stage"] in VALID_STAGES, f"invalid stage for {key}"


def test_list_and_boolean_fields_types_are_correct():
    queues = _load_queues()
    for key, queue in queues.items():
        for field in LIST_FIELDS:
            assert isinstance(queue[field], list), f"queue {key} field {field} must be list"
        for field in BOOL_FIELDS:
            assert isinstance(queue[field], bool), f"queue {key} field {field} must be bool"


def test_queue_id_matches_key_or_declared_id():
    queues = _load_queues()
    for key, queue in queues.items():
        assert queue["queue_id"] == key, f"queue_id mismatch for {key}"


def test_at_least_one_queue_blocks_conversion_and_one_allows_intake_only():
    queues = _load_queues()
    assert any(q["blocks_conversion"] for q in queues.values())
    assert any(q["allows_intake_only"] for q in queues.values())


def test_no_queue_grants_canon_permission():
    queues = _load_queues()
    forbidden_phrases = [
        "promote to canon",
        "canon permission granted",
        "direct canon adoption",
        "merge into canon",
    ]
    for key, queue in queues.items():
        blob = " ".join(str(v) for v in queue.values()).lower()
        for phrase in forbidden_phrases:
            assert phrase not in blob, f"queue {key} contains forbidden phrase: {phrase}"
