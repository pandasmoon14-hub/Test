"""Kernel subsystem — schema registry, record identity, and future kernel services."""

from astra_runtime.kernel.schema_registry import (
    InvalidSchemaDefinitionError,
    SchemaAlreadyRegisteredError,
    SchemaNotFoundError,
    SchemaRegistry,
    SchemaRegistryError,
)
from astra_runtime.kernel.record_identity import (
    InvalidRecordIdError,
    RecordId,
    RecordIdentityError,
    build_record_id,
    is_valid_record_id,
    parse_record_id,
)

__all__ = [
    "InvalidRecordIdError",
    "InvalidSchemaDefinitionError",
    "RecordId",
    "RecordIdentityError",
    "SchemaAlreadyRegisteredError",
    "SchemaNotFoundError",
    "SchemaRegistry",
    "SchemaRegistryError",
    "build_record_id",
    "is_valid_record_id",
    "parse_record_id",
]
