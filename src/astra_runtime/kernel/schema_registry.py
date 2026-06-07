"""Schema registry skeleton — backend-owned, no LLM authority, no persistence."""

from __future__ import annotations

import copy
from typing import Mapping


class SchemaRegistryError(Exception):
    """Base error for schema registry operations."""


class SchemaNotFoundError(SchemaRegistryError):
    """Raised when a requested schema type key is not registered."""


class SchemaAlreadyRegisteredError(SchemaRegistryError):
    """Raised when registering a duplicate type key without replace=True."""


class InvalidSchemaDefinitionError(SchemaRegistryError):
    """Raised when a schema definition fails basic validity checks."""


class SchemaRegistry:
    """Minimal in-memory schema registry. Backend-owned utility; no LLM authority."""

    def __init__(self) -> None:
        self._registry: dict[str, dict] = {}

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, dict]) -> SchemaRegistry:
        registry = cls()
        for key, definition in mapping.items():
            registry.register(key, definition)
        return registry

    def register(
        self, type_key: str, definition: dict, *, replace: bool = False
    ) -> None:
        if not isinstance(type_key, str) or not type_key.strip():
            raise InvalidSchemaDefinitionError("type_key must be a non-empty string")
        if not isinstance(definition, Mapping):
            raise InvalidSchemaDefinitionError("definition must be a mapping")
        if type_key in self._registry and not replace:
            raise SchemaAlreadyRegisteredError(
                f"Schema already registered for key: {type_key!r}"
            )
        self._registry[type_key] = copy.deepcopy(dict(definition))

    def get(self, type_key: str) -> dict:
        if type_key not in self._registry:
            raise SchemaNotFoundError(f"No schema registered for key: {type_key!r}")
        return copy.deepcopy(self._registry[type_key])

    def has(self, type_key: str) -> bool:
        return type_key in self._registry

    def keys(self) -> list[str]:
        return sorted(self._registry.keys())

    def to_mapping(self) -> dict[str, dict]:
        return copy.deepcopy(self._registry)
