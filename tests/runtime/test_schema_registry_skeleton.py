"""Tests for schema registry skeleton — RUNTIME-IMPL-PR-1."""

import pytest

from astra_runtime.kernel.schema_registry import (
    InvalidSchemaDefinitionError,
    SchemaAlreadyRegisteredError,
    SchemaNotFoundError,
    SchemaRegistry,
)


class TestSchemaRegistryEmpty:
    def test_empty_registry_has_no_keys(self):
        reg = SchemaRegistry()
        assert reg.keys() == []

    def test_empty_registry_has_returns_false(self):
        reg = SchemaRegistry()
        assert reg.has("anything") is False


class TestSchemaRegistryFromMapping:
    def test_create_from_mapping(self):
        mapping = {
            "creature": {"name": "creature_record"},
            "item": {"name": "item_record"},
        }
        reg = SchemaRegistry.from_mapping(mapping)
        assert reg.has("creature")
        assert reg.has("item")

    def test_keys_are_sorted(self):
        mapping = {
            "zebra": {"z": 1},
            "alpha": {"a": 1},
            "middle": {"m": 1},
        }
        reg = SchemaRegistry.from_mapping(mapping)
        assert reg.keys() == ["alpha", "middle", "zebra"]


class TestSchemaRegistryGet:
    def test_get_existing_key(self):
        reg = SchemaRegistry.from_mapping({"test": {"field": "value"}})
        result = reg.get("test")
        assert result == {"field": "value"}

    def test_get_missing_key_raises(self):
        reg = SchemaRegistry()
        with pytest.raises(SchemaNotFoundError):
            reg.get("nonexistent")


class TestSchemaRegistryRegister:
    def test_register_valid_schema(self):
        reg = SchemaRegistry()
        reg.register("new_type", {"field": "data"})
        assert reg.has("new_type")
        assert reg.get("new_type") == {"field": "data"}

    def test_register_duplicate_without_replace_raises(self):
        reg = SchemaRegistry()
        reg.register("dup", {"v": 1})
        with pytest.raises(SchemaAlreadyRegisteredError):
            reg.register("dup", {"v": 2})

    def test_register_duplicate_with_replace_succeeds(self):
        reg = SchemaRegistry()
        reg.register("dup", {"v": 1})
        reg.register("dup", {"v": 2}, replace=True)
        assert reg.get("dup") == {"v": 2}

    def test_reject_empty_key(self):
        reg = SchemaRegistry()
        with pytest.raises(InvalidSchemaDefinitionError):
            reg.register("", {"v": 1})

    def test_reject_whitespace_only_key(self):
        reg = SchemaRegistry()
        with pytest.raises(InvalidSchemaDefinitionError):
            reg.register("   ", {"v": 1})

    def test_reject_non_mapping_definition(self):
        reg = SchemaRegistry()
        with pytest.raises(InvalidSchemaDefinitionError):
            reg.register("key", "not a mapping")

    def test_reject_list_definition(self):
        reg = SchemaRegistry()
        with pytest.raises(InvalidSchemaDefinitionError):
            reg.register("key", [1, 2, 3])


class TestSchemaRegistryImmutability:
    def test_get_returns_copy(self):
        reg = SchemaRegistry.from_mapping({"test": {"field": "original"}})
        result = reg.get("test")
        result["field"] = "mutated"
        assert reg.get("test") == {"field": "original"}

    def test_to_mapping_returns_safe_copy(self):
        reg = SchemaRegistry.from_mapping({"test": {"field": "original"}})
        mapping = reg.to_mapping()
        mapping["test"]["field"] = "mutated"
        assert reg.get("test") == {"field": "original"}

    def test_source_mapping_mutation_does_not_affect_registry(self):
        source = {"test": {"field": "original"}}
        reg = SchemaRegistry.from_mapping(source)
        source["test"]["field"] = "mutated"
        assert reg.get("test") == {"field": "original"}
