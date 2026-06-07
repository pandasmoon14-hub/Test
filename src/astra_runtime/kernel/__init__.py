"""Kernel subsystem — schema registry, record identity, command envelope, transaction preview, state delta, event ledger."""

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
from astra_runtime.kernel.state_delta import (
    InvalidStateDeltaError,
    StateDeltaEnvelope,
    StateDeltaError,
    create_state_delta_envelope,
    validate_state_delta_envelope,
)
from astra_runtime.kernel.event_ledger import (
    EventLedgerEntry,
    EventLedgerError,
    InvalidEventLedgerEntryError,
    create_event_ledger_entry,
    validate_event_ledger_entry,
)

__all__ = [
    "CommandEnvelope",
    "CommandEnvelopeError",
    "EventLedgerEntry",
    "EventLedgerError",
    "InvalidCommandEnvelopeError",
    "InvalidEventLedgerEntryError",
    "InvalidRecordIdError",
    "InvalidSchemaDefinitionError",
    "InvalidStateDeltaError",
    "InvalidTransactionPreviewError",
    "RecordId",
    "RecordIdentityError",
    "SchemaAlreadyRegisteredError",
    "SchemaNotFoundError",
    "SchemaRegistry",
    "SchemaRegistryError",
    "StateDeltaEnvelope",
    "StateDeltaError",
    "TransactionPreview",
    "TransactionPreviewError",
    "build_record_id",
    "create_command_envelope",
    "create_event_ledger_entry",
    "create_state_delta_envelope",
    "create_transaction_preview",
    "is_valid_record_id",
    "parse_record_id",
    "validate_command_envelope",
    "validate_event_ledger_entry",
    "validate_state_delta_envelope",
    "validate_transaction_preview",
]
