"""Record identity skeleton — backend-owned, deterministic, no persistence."""

from __future__ import annotations

import re
from dataclasses import dataclass

_ALLOWED_SEGMENT = re.compile(r"^[a-z0-9_-]+$")
_RECORD_ID_PATTERN = re.compile(r"^astra:([a-z0-9_-]+):([a-z0-9_-]+)$")


class RecordIdentityError(Exception):
    """Base error for record identity operations."""


class InvalidRecordIdError(RecordIdentityError):
    """Raised when a record ID or its components are invalid."""


@dataclass(frozen=True)
class RecordId:
    """Parsed record identity."""

    record_type: str
    local_id: str

    @property
    def full_id(self) -> str:
        return f"astra:{self.record_type}:{self.local_id}"


def _validate_segment(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidRecordIdError(f"{label} must be a non-empty string")
    if value != value.strip():
        raise InvalidRecordIdError(f"{label} must not have leading/trailing whitespace")
    if not _ALLOWED_SEGMENT.match(value):
        raise InvalidRecordIdError(
            f"{label} contains invalid characters: {value!r} "
            f"(allowed: lowercase ASCII letters, digits, underscores, hyphens)"
        )
    return value


def build_record_id(record_type: str, local_id: str) -> str:
    _validate_segment(record_type, "record_type")
    _validate_segment(local_id, "local_id")
    return f"astra:{record_type}:{local_id}"


def parse_record_id(record_id: str) -> RecordId:
    if not isinstance(record_id, str) or not record_id.strip():
        raise InvalidRecordIdError("record_id must be a non-empty string")
    match = _RECORD_ID_PATTERN.match(record_id)
    if not match:
        raise InvalidRecordIdError(f"Malformed record ID: {record_id!r}")
    return RecordId(record_type=match.group(1), local_id=match.group(2))


def is_valid_record_id(record_id: str) -> bool:
    try:
        parse_record_id(record_id)
        return True
    except (InvalidRecordIdError, TypeError):
        return False
