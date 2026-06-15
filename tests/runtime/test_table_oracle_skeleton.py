"""Tests for table/oracle interface skeleton — RUNTIME-IMPL-PR-4."""

import os

import pytest

from astra_runtime.kernel.table_oracle import (
    InvalidTableOracleInvocationError,
    InvalidTableOracleResultError,
    TableOracleInvocation,
    TableOracleResult,
    create_table_oracle_invocation,
    create_table_oracle_result,
    select_table_entry,
    validate_table_oracle_invocation,
    validate_table_oracle_result,
)


SAMPLE_TABLE = {"goblin": "A small green creature", "dragon": "A large fire-breather", "orc": "A brutish warrior"}


class TestCreateTableOracleInvocation:
    def test_valid_creation(self):
        inv = create_table_oracle_invocation("oracle-1", "encounter-table", "seed-a", 5)
        assert isinstance(inv, TableOracleInvocation)

    def test_preserves_oracle_id(self):
        inv = create_table_oracle_invocation("oracle-42", "tbl", "seed-a", 1)
        assert inv.oracle_id == "oracle-42"

    def test_preserves_table_id(self):
        inv = create_table_oracle_invocation("oracle-1", "my-table", "seed-a", 1)
        assert inv.table_id == "my-table"

    def test_preserves_seed(self):
        inv = create_table_oracle_invocation("oracle-1", "tbl", "my-seed", 1)
        assert inv.seed == "my-seed"

    def test_preserves_roll(self):
        inv = create_table_oracle_invocation("oracle-1", "tbl", "seed-a", 77)
        assert inv.roll == 77

    def test_rejects_empty_oracle_id(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            create_table_oracle_invocation("", "tbl", "seed-a", 1)

    def test_rejects_empty_table_id(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            create_table_oracle_invocation("oracle-1", "", "seed-a", 1)

    def test_rejects_empty_seed(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            create_table_oracle_invocation("oracle-1", "tbl", "", 1)

    def test_rejects_non_int_roll(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            create_table_oracle_invocation("oracle-1", "tbl", "seed-a", 1.5)

    def test_rejects_bool_roll(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            create_table_oracle_invocation("oracle-1", "tbl", "seed-a", True)

    def test_metadata_defaults_to_empty_mapping(self):
        inv = create_table_oracle_invocation("oracle-1", "tbl", "seed-a", 1)
        assert dict(inv.metadata) == {}

    def test_metadata_copy_safe(self):
        original = {"context": "encounter"}
        inv = create_table_oracle_invocation("oracle-1", "tbl", "seed-a", 1, metadata=original)
        original["context"] = "changed"
        assert inv.metadata["context"] == "encounter"

    def test_metadata_nested_copy_safe(self):
        original = {"ctx": {"k": "v"}}
        inv = create_table_oracle_invocation("oracle-1", "tbl", "seed-a", 1, metadata=original)
        original["ctx"]["k"] = "changed"
        assert inv.metadata["ctx"]["k"] == "v"

    def test_reject_non_mapping_metadata(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            create_table_oracle_invocation("oracle-1", "tbl", "seed-a", 1, metadata="bad")


class TestTableOracleInvocationToDict:
    def test_to_dict_returns_dict(self):
        inv = create_table_oracle_invocation("oracle-1", "tbl", "seed-a", 5)
        result = inv.to_dict()
        assert isinstance(result, dict)
        assert result["oracle_id"] == "oracle-1"
        assert result["table_id"] == "tbl"
        assert result["seed"] == "seed-a"
        assert result["roll"] == 5

    def test_to_dict_returns_deep_copy(self):
        inv = create_table_oracle_invocation(
            "oracle-1", "tbl", "seed-a", 5,
            metadata={"nested": {"b": 2}},
        )
        result = inv.to_dict()
        result["metadata"]["nested"]["b"] = 999
        assert inv.metadata["nested"]["b"] == 2


class TestValidateTableOracleInvocation:
    def test_valid_invocation_accepted(self):
        inv = create_table_oracle_invocation("oracle-1", "tbl", "seed-a", 5)
        assert validate_table_oracle_invocation(inv) is True

    def test_invalid_object_rejected(self):
        assert validate_table_oracle_invocation("not-an-invocation") is False

    def test_none_rejected(self):
        assert validate_table_oracle_invocation(None) is False

    def test_dict_rejected(self):
        assert validate_table_oracle_invocation({"oracle_id": "oracle-1"}) is False


class TestCreateTableOracleResult:
    def test_valid_creation(self):
        res = create_table_oracle_result("oracle-1", "tbl", 5, "goblin", "A small creature")
        assert isinstance(res, TableOracleResult)

    def test_preserves_fields(self):
        res = create_table_oracle_result("oracle-1", "tbl", 5, "dragon", "Fire-breather")
        assert res.oracle_id == "oracle-1"
        assert res.table_id == "tbl"
        assert res.roll == 5
        assert res.selected_key == "dragon"
        assert res.selected_value == "Fire-breather"

    def test_rejects_empty_selected_key(self):
        with pytest.raises(InvalidTableOracleResultError):
            create_table_oracle_result("oracle-1", "tbl", 5, "", "value")

    def test_rejects_whitespace_selected_key(self):
        with pytest.raises(InvalidTableOracleResultError):
            create_table_oracle_result("oracle-1", "tbl", 5, "   ", "value")

    def test_selected_value_deep_copy_safe(self):
        original_val = {"nested": {"data": 1}}
        res = create_table_oracle_result("oracle-1", "tbl", 5, "key", original_val)
        original_val["nested"]["data"] = 999
        assert res.selected_value["nested"]["data"] == 1

    def test_metadata_defaults_to_empty(self):
        res = create_table_oracle_result("oracle-1", "tbl", 5, "key", "val")
        assert dict(res.metadata) == {}

    def test_to_dict_returns_deep_copy(self):
        res = create_table_oracle_result(
            "oracle-1", "tbl", 5, "key", {"nested": {"x": 1}},
            metadata={"m": {"y": 2}},
        )
        d = res.to_dict()
        d["selected_value"]["nested"]["x"] = 999
        d["metadata"]["m"]["y"] = 999
        assert res.selected_value["nested"]["x"] == 1
        assert res.metadata["m"]["y"] == 2

    def test_rejects_bool_roll(self):
        with pytest.raises(InvalidTableOracleResultError):
            create_table_oracle_result("oracle-1", "tbl", True, "key", "val")


class TestValidateTableOracleResult:
    def test_valid_result_accepted(self):
        res = create_table_oracle_result("oracle-1", "tbl", 5, "key", "val")
        assert validate_table_oracle_result(res) is True

    def test_invalid_object_rejected(self):
        assert validate_table_oracle_result("not-a-result") is False


class TestTableOracleInvocationImmutability:
    def test_frozen_dataclass(self):
        inv = create_table_oracle_invocation("oracle-1", "tbl", "seed-a", 5)
        with pytest.raises(AttributeError):
            inv.oracle_id = "changed"


class TestSelectTableEntry:
    def test_rejects_empty_table(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            select_table_entry({}, 1)

    def test_rejects_non_mapping_table(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            select_table_entry([1, 2, 3], 1)

    def test_rejects_non_string_keys(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            select_table_entry({1: "one", 2: "two"}, 0)

    def test_deterministic_selection(self):
        key1, val1 = select_table_entry(SAMPLE_TABLE, 7)
        key2, val2 = select_table_entry(SAMPLE_TABLE, 7)
        assert key1 == key2
        assert val1 == val2

    def test_returns_valid_key(self):
        key, val = select_table_entry(SAMPLE_TABLE, 0)
        assert key in SAMPLE_TABLE

    def test_returns_deep_copy_safe_value(self):
        table = {"a": {"nested": 1}, "b": {"nested": 2}}
        key, val = select_table_entry(table, 0)
        val["nested"] = 999
        assert table[key]["nested"] != 999

    def test_different_rolls_can_select_different_entries(self):
        keys = {select_table_entry(SAMPLE_TABLE, i)[0] for i in range(10)}
        assert len(keys) > 1

    def test_rejects_bool_roll(self):
        with pytest.raises(InvalidTableOracleInvocationError):
            select_table_entry(SAMPLE_TABLE, True)


class TestNoUnauthorizedTableMethods:
    """Table/oracle must not contain load/parse/generate/weighted methods."""

    def test_no_load_parse_generate(self):
        import astra_runtime.kernel.table_oracle as mod
        for attr in ["load_table", "parse_table", "generate_encounter",
                      "WeightedTable", "weighted_select", "load_markdown_table"]:
            assert not hasattr(mod, attr)


class TestNoUnauthorizedModules:
    """Guardrail tests — future modules must not exist yet."""

    KERNEL_DIR = os.path.join(
        os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "kernel"
    )

    def test_domain_package_contains_only_authorized_modules(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "domain"
        )
        assert os.path.isdir(path), "Domain package should exist after PR-1A"
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "transaction_lifecycle.py", "event_commitment.py", "validation_integration.py", "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py", "scene_command_execution_skeleton.py", "__pycache__"}
        actual = set(os.listdir(path))
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized domain modules: {unauthorized}"

    def test_no_model_integration_package(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "model"
        )
        assert not os.path.isdir(path), "Unauthorized model integration package exists"

    def test_no_prompt_template_package(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "prompts"
        )
        assert not os.path.isdir(path), "Unauthorized prompt template package exists"

    def test_no_live_play_adapter_package(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "live_play"
        )
        assert not os.path.isdir(path), "Unauthorized live-play adapter package exists"
