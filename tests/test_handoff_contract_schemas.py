from __future__ import annotations

import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    "docs/handoff/conversion_handoff_contract_v0_1.md",
    "docs/handoff/handoff_readiness_policy_v0_1.md",
    "docs/handoff/handoff_queue_policy_v0_1.md",
    "docs/handoff/handoff_validation_rules_v0_1.md",
]

SCHEMAS = [
    "schemas/handoff/packet_manifest.schema.json",
    "schemas/handoff/content_unit.schema.json",
    "schemas/handoff/queue_record.schema.json",
    "schemas/handoff/conversion_result.schema.json",
    "schemas/handoff/mapping_ledger.schema.json",
    "schemas/handoff/readiness_classes.schema.json",
    "schemas/handoff/table_unit.schema.json",
    "schemas/handoff/map_unit.schema.json",
    "schemas/handoff/statblock_unit.schema.json",
    "schemas/handoff/conversion_intake_result.schema.json",
]


def _load_schema(rel: str) -> dict:
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8"))


def test_handoff_docs_exist_and_nonempty() -> None:
    for rel in DOCS:
        p = ROOT / rel
        assert p.exists(), rel
        assert p.stat().st_size > 0, rel


def test_handoff_schemas_exist_nonempty_and_json() -> None:
    for rel in SCHEMAS:
        p = ROOT / rel
        assert p.exists(), rel
        assert p.stat().st_size > 0, rel
        json.loads(p.read_text(encoding="utf-8"))


def test_handoff_schemas_are_valid_draft_2020_12() -> None:
    for rel in SCHEMAS:
        schema = _load_schema(rel)
        jsonschema.Draft202012Validator.check_schema(schema)


def test_packet_manifest_required_fields() -> None:
    s = _load_schema("schemas/handoff/packet_manifest.schema.json")
    req = set(s.get("required", []))
    must = {
        "packet_id", "book_id", "source_filename", "source_sha256", "packet_page_start", "packet_page_end",
        "extraction_version", "strict_audit_status", "readiness_class", "content_family_tags", "required_files",
        "queues_present", "conversion_permissions", "canon_permissions",
    }
    assert must.issubset(req)


def test_content_unit_required_fields() -> None:
    s = _load_schema("schemas/handoff/content_unit.schema.json")
    req = set(s.get("required", []))
    must = {
        "unit_id", "book_id", "source_page_start", "source_page_end", "unit_type", "text", "extraction_status",
        "content_readiness", "conversion_permission", "canon_permission", "defects", "confidence", "recommended_queue",
        "lawful_outcome", "notes",
    }
    assert must.issubset(req)


def test_queue_record_required_fields() -> None:
    s = _load_schema("schemas/handoff/queue_record.schema.json")
    req = set(s.get("required", []))
    must = {
        "queue_id", "queue_name", "unit_id", "book_id", "source_pages", "reason_code", "blocking_effect",
        "allowed_use", "recommended_action", "priority", "owner", "status",
    }
    assert must.issubset(req)


def test_mapping_ledger_required_fields() -> None:
    s = _load_schema("schemas/handoff/mapping_ledger.schema.json")
    req = set(s.get("required", []))
    must = {
        "mapping_id", "donor_construct", "source_pages", "source_unit_ids", "astra_target_family", "lawful_outcome",
        "rationale", "must_not_import", "next_queue", "doctrine_owner", "confidence",
    }
    assert must.issubset(req)


def test_conversion_result_required_fields() -> None:
    s = _load_schema("schemas/handoff/conversion_result.schema.json")
    req = set(s.get("required", []))
    must = {
        "result_id", "source_packet_id", "result_type", "readiness_assessment", "construct_inventory_path",
        "mapping_ledger_path", "lexicon_delta_path", "canon_candidates_path", "quarantine_notes_path",
        "doctrine_escalations_path", "rejected_imports_path", "confidence", "reviewer_notes",
    }
    assert must.issubset(req)


def test_family_schema_specific_fields_present() -> None:
    table = _load_schema("schemas/handoff/table_unit.schema.json")
    map_s = _load_schema("schemas/handoff/map_unit.schema.json")
    stat = _load_schema("schemas/handoff/statblock_unit.schema.json")

    assert {"table_title", "table_format", "row_count_observed", "row_count_expected", "table_normalization_status", "table_defects"}.issubset(set(table.get("properties", {})))
    assert {"map_title", "map_validation_status", "scale_detected", "keyed_locations_detected", "diagram_defects"}.issubset(set(map_s.get("properties", {})))
    assert {"statblock_family", "donor_engine", "statblock_parse_status", "statblock_defects", "mechanical_import_allowed"}.issubset(set(stat.get("properties", {})))


def test_sample_instances_validate() -> None:
    content_unit = {
        "unit_id": "u1", "book_id": "b1", "source_page_start": 1, "source_page_end": 1, "unit_type": "prose", "text": "x",
        "extraction_status": "ok", "content_readiness": "ready", "conversion_permission": "allowed", "canon_permission": "review_required",
        "defects": [], "confidence": 0.9, "recommended_queue": None, "lawful_outcome": "direct_astra_mapping", "notes": "",
    }
    queue_record = {
        "queue_id": "q1", "queue_name": "repair_queue", "unit_id": "u1", "book_id": "b1", "source_pages": [1],
        "reason_code": "ocr_needed", "blocking_effect": "blocks_conversion", "allowed_use": "index_only", "recommended_action": "repair",
        "priority": "medium", "owner": "ops", "status": "open",
    }
    mapping_ledger = {
        "mapping_id": "m1", "donor_construct": "construct_x", "source_pages": [1], "source_unit_ids": ["u1"], "astra_target_family": "family_a",
        "lawful_outcome": "normalized_astra_mapping", "rationale": "safe", "must_not_import": False, "next_queue": None,
        "doctrine_owner": "lore", "confidence": 0.8,
    }
    conversion_result = {
        "result_id": "r1", "source_packet_id": "p1", "result_type": "intake", "readiness_assessment": "ready_with_warnings",
        "construct_inventory_path": "conversion/construct_inventory.json", "mapping_ledger_path": "conversion/mapping_ledger.jsonl",
        "lexicon_delta_path": "conversion/lexicon_delta.json", "canon_candidates_path": "conversion/canon_candidates.jsonl",
        "quarantine_notes_path": "conversion/quarantine_notes.md", "doctrine_escalations_path": "conversion/doctrine_escalations.jsonl",
        "rejected_imports_path": "conversion/rejected_imports.jsonl", "confidence": 0.7, "reviewer_notes": "ok",
    }
    packet_manifest = {
        "packet_id": "p1", "book_id": "b1", "source_filename": "book.pdf", "source_sha256": "abc", "packet_page_start": 1,
        "packet_page_end": 10, "extraction_version": "v13", "strict_audit_status": "pass", "readiness_class": "ready_with_warnings",
        "content_family_tags": ["table"], "required_files": ["packet_manifest.json"], "queues_present": ["repair_queue"],
        "conversion_permissions": ["allowed"], "canon_permissions": ["review_required"],
    }
    table_unit = {**content_unit, "unit_type": "table", "table_title": "T", "table_format": "markdown", "row_count_observed": 2, "row_count_expected": 2, "table_normalization_status": "normalized", "table_defects": []}
    map_unit = {**content_unit, "unit_type": "map", "map_title": "M", "map_validation_status": "validated", "scale_detected": None, "keyed_locations_detected": 3, "diagram_defects": []}
    statblock_unit = {**content_unit, "unit_type": "stat_block", "statblock_family": "npc", "donor_engine": "d20", "statblock_parse_status": "parsed", "statblock_defects": [], "mechanical_import_allowed": False}

    for rel, sample in [
        ("schemas/handoff/content_unit.schema.json", content_unit),
        ("schemas/handoff/queue_record.schema.json", queue_record),
        ("schemas/handoff/mapping_ledger.schema.json", mapping_ledger),
        ("schemas/handoff/conversion_result.schema.json", conversion_result),
        ("schemas/handoff/packet_manifest.schema.json", packet_manifest),
        ("schemas/handoff/table_unit.schema.json", table_unit),
        ("schemas/handoff/map_unit.schema.json", map_unit),
        ("schemas/handoff/statblock_unit.schema.json", statblock_unit),
    ]:
        jsonschema.validate(sample, _load_schema(rel))


def test_enum_coverage() -> None:
    readiness = {"ready", "ready_with_warnings", "intake_only", "partial_conversion_allowed", "needs_repair", "quarantined", "failed_extraction"}
    outcomes = {"direct_astra_mapping", "normalized_astra_mapping", "source_local_retained_construct", "quarantined_construct_pending_later_doctrine", "escalated_doctrine_problem"}
    queues = {"repair_queue", "table_normalization_queue", "map_diagram_queue", "statblock_queue", "ocr_empty_queue", "mojibake_cleanup_queue", "layout_reconstruction_queue", "lexicon_review_queue", "doctrine_escalation_queue", "source_local_retention_queue", "canon_candidate_queue"}

    c = _load_schema("schemas/handoff/content_unit.schema.json")
    m = _load_schema("schemas/handoff/mapping_ledger.schema.json")
    q = _load_schema("schemas/handoff/queue_record.schema.json")

    assert readiness.issubset(set(c["properties"]["content_readiness"]["enum"]))
    assert outcomes.issubset(set(m["properties"]["lawful_outcome"]["enum"]))
    assert queues.issubset(set(q["properties"]["queue_name"]["enum"]))


def _valid_intake_sample() -> dict:
    return {
        "result_id": "r1",
        "packet_id": "p1",
        "book_id": "b1",
        "source_packet_dir": "packets/p1",
        "page_range": {"start_page": 1, "end_page": 2},
        "result_status": "drafted",
        "extraction_readiness_assessment": "ready",
        "donor_construct_inventory": [{"text": "construct", "summary": "summary"}],
        "mapping_ledger": [{
            "donor_construct": "x", "source_pages": [1], "source_unit_ids": ["u1"], "astra_target_family": "fam",
            "lawful_outcome": "normalized Astra mapping", "rationale": "ok", "must_not_import": False,
            "doctrine_owner": None, "canon_candidate_permission": "candidate_only_after_review",
            "confidence": 0.8, "raw_markdown_row": "| x |", "parse_warnings": ["parsed"]
        }],
        "queue_actions": [{"text": "queue item"}],
        "lexicon_delta": [{"text": "lexicon item"}],
        "doctrine_escalations": [{"text": "issue", "reason": "rationale"}],
        "source_local_retentions": [{"text": "retain", "retained_construct": "retain", "boundary_scope_note": "boundary", "rationale": "reason", "review_required": True}],
        "rejected_imports": [{"text": "reject", "reason": "bad", "must_not_import": True}],
        "canon_candidate_notes": [{"text": "candidate", "canon_candidate_permission": "candidate_only_after_review", "review_required": True}],
        "conversion_notes": "c",
        "reviewer_notes": "r",
        "confidence": 0.8,
        "parse_warnings": ["top-level"],
    }


def test_conversion_intake_schema_tightening_rules() -> None:
    schema = _load_schema("schemas/handoff/conversion_intake_result.schema.json")
    obj = _valid_intake_sample()
    jsonschema.validate(obj, schema)

    bad_inv = _valid_intake_sample()
    bad_inv["donor_construct_inventory"] = [{}]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad_inv, schema)

    bad_queue = _valid_intake_sample()
    bad_queue["queue_actions"] = [{}]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad_queue, schema)

    valid_source_local = _valid_intake_sample()
    valid_source_local["source_local_retentions"] = [{"text": "simple text retention"}]
    jsonschema.validate(valid_source_local, schema)

    valid_rejected = _valid_intake_sample()
    valid_rejected["rejected_imports"] = [{"rejected_construct": "x", "reason": "unsafe", "must_not_import": True}]
    jsonschema.validate(valid_rejected, schema)

    bad_canon = _valid_intake_sample()
    bad_canon["canon_candidate_notes"] = [{"text": "bad", "canon_candidate_permission": "approved"}]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad_canon, schema)

    malformed = _valid_intake_sample()
    malformed["mapping_ledger"] = [{"donor_construct": "x"}]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(malformed, schema)
