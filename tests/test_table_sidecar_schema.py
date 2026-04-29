import json
from pathlib import Path

from table_fixer import build_table_sidecars


def test_table_sidecar_contract_has_schema_fields():
    md = """<!-- PAGE:1 -->\n| A | B |\n|---|---|\n| 1 | 2 |\n"""
    rows = build_table_sidecars(md)
    assert rows
    row = rows[0]
    assert "strategy" in row
    assert "sidecar_written" in row


def test_schema_loads():
    schema_path = Path("schemas/table_sidecar.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert schema["items"]["additionalProperties"] is False
