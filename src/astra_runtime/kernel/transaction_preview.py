"""Transaction preview skeleton — backend-owned, immutable, no state deltas."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.kernel.command_envelope import CommandEnvelope

_ALLOWED_STATUSES = frozenset({"preview_created", "preview_rejected", "preview_quarantined"})


class TransactionPreviewError(Exception):
    """Base error for transaction preview operations."""


class InvalidTransactionPreviewError(TransactionPreviewError):
    """Raised when a transaction preview fails validation."""


@dataclass(frozen=True)
class TransactionPreview:
    """Immutable transaction preview. No state deltas, no event commitment."""

    preview_id: str
    command_id: str
    status: str
    messages: tuple[str, ...] = ()
    requires_confirmation: bool = False
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "preview_id": self.preview_id,
            "command_id": self.command_id,
            "status": self.status,
            "messages": list(self.messages),
            "requires_confirmation": self.requires_confirmation,
            "metadata": dict(self.metadata),
        }


def create_transaction_preview(
    preview_id: str,
    command: CommandEnvelope,
    status: str = "preview_created",
    messages: Sequence[str] | None = None,
    requires_confirmation: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionPreview:
    if not isinstance(preview_id, str) or not preview_id.strip():
        raise InvalidTransactionPreviewError("preview_id must be a non-empty string")

    if status not in _ALLOWED_STATUSES:
        raise InvalidTransactionPreviewError(
            f"status must be one of {sorted(_ALLOWED_STATUSES)}, got: {status!r}"
        )

    if messages is None:
        safe_messages: tuple[str, ...] = ()
    else:
        for i, msg in enumerate(messages):
            if not isinstance(msg, str):
                raise InvalidTransactionPreviewError(
                    f"messages[{i}] must be a string, got: {type(msg).__name__}"
                )
        safe_messages = tuple(messages)

    if metadata is None:
        safe_metadata: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(metadata, Mapping):
        raise InvalidTransactionPreviewError("metadata must be a mapping")
    else:
        safe_metadata = MappingProxyType(dict(metadata))

    return TransactionPreview(
        preview_id=preview_id,
        command_id=command.command_id,
        status=status,
        messages=safe_messages,
        requires_confirmation=requires_confirmation,
        metadata=safe_metadata,
    )


def validate_transaction_preview(obj: Any) -> bool:
    if not isinstance(obj, TransactionPreview):
        return False
    if not isinstance(obj.preview_id, str) or not obj.preview_id.strip():
        return False
    if not isinstance(obj.command_id, str) or not obj.command_id.strip():
        return False
    if obj.status not in _ALLOWED_STATUSES:
        return False
    if not isinstance(obj.messages, tuple):
        return False
    if not all(isinstance(m, str) for m in obj.messages):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True
