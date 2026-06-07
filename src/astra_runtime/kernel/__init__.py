"""Kernel subsystem — schema registry, record identity, command envelope, transaction preview."""

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
from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    CommandEnvelopeError,
    InvalidCommandEnvelopeError,
    create_command_envelope,
    validate_command_envelope,
)
from astra_runtime.kernel.transaction_preview import (
    InvalidTransactionPreviewError,
    TransactionPreview,
    TransactionPreviewError,
    create_transaction_preview,
    validate_transaction_preview,
)

__all__ = [
    "CommandEnvelope",
    "CommandEnvelopeError",
    "InvalidCommandEnvelopeError",
    "InvalidRecordIdError",
    "InvalidSchemaDefinitionError",
    "InvalidTransactionPreviewError",
    "RecordId",
    "RecordIdentityError",
    "SchemaAlreadyRegisteredError",
    "SchemaNotFoundError",
    "SchemaRegistry",
    "SchemaRegistryError",
    "TransactionPreview",
    "TransactionPreviewError",
    "build_record_id",
    "create_command_envelope",
    "create_transaction_preview",
    "is_valid_record_id",
    "parse_record_id",
    "validate_command_envelope",
    "validate_transaction_preview",
]
