"""Tests for transaction preview skeleton — RUNTIME-IMPL-PR-2."""

import pytest

from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.transaction_preview import (
    InvalidTransactionPreviewError,
    TransactionPreview,
    create_transaction_preview,
    validate_transaction_preview,
)

VALID_ACTOR = "astra:actor:player-01"


@pytest.fixture
def sample_envelope():
    return create_command_envelope("cmd-1", "move", VALID_ACTOR, payload={"direction": "north"})


class TestCreateTransactionPreview:
    def test_valid_creation(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        assert isinstance(preview, TransactionPreview)

    def test_preserves_command_id(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        assert preview.command_id == "cmd-1"

    def test_default_status_is_preview_created(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        assert preview.status == "preview_created"

    def test_preview_rejected_status_accepted(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope, status="preview_rejected")
        assert preview.status == "preview_rejected"

    def test_preview_quarantined_status_accepted(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope, status="preview_quarantined")
        assert preview.status == "preview_quarantined"

    def test_unsupported_status_rejected(self, sample_envelope):
        with pytest.raises(InvalidTransactionPreviewError):
            create_transaction_preview("prev-1", sample_envelope, status="committed")

    def test_messages_normalized_to_tuple(self, sample_envelope):
        preview = create_transaction_preview(
            "prev-1", sample_envelope, messages=["msg1", "msg2"]
        )
        assert isinstance(preview.messages, tuple)
        assert preview.messages == ("msg1", "msg2")

    def test_messages_default_empty_tuple(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        assert preview.messages == ()

    def test_non_string_message_rejected(self, sample_envelope):
        with pytest.raises(InvalidTransactionPreviewError):
            create_transaction_preview("prev-1", sample_envelope, messages=["ok", 42])

    def test_metadata_defaults_to_empty_mapping(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        assert dict(preview.metadata) == {}

    def test_metadata_copy_safe(self, sample_envelope):
        original = {"note": "alpha"}
        preview = create_transaction_preview("prev-1", sample_envelope, metadata=original)
        original["note"] = "beta"
        assert preview.metadata["note"] == "alpha"

    def test_metadata_nested_copy_safe(self, sample_envelope):
        original = {"context": {"key": "val"}}
        preview = create_transaction_preview("prev-1", sample_envelope, metadata=original)
        original["context"]["key"] = "changed"
        assert preview.metadata["context"]["key"] == "val"

    def test_non_mapping_metadata_rejected(self, sample_envelope):
        with pytest.raises(InvalidTransactionPreviewError):
            create_transaction_preview("prev-1", sample_envelope, metadata="bad")

    def test_reject_empty_preview_id(self, sample_envelope):
        with pytest.raises(InvalidTransactionPreviewError):
            create_transaction_preview("", sample_envelope)

    def test_reject_whitespace_preview_id(self, sample_envelope):
        with pytest.raises(InvalidTransactionPreviewError):
            create_transaction_preview("   ", sample_envelope)

    def test_requires_confirmation_default_false(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        assert preview.requires_confirmation is False

    def test_requires_confirmation_set_true(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope, requires_confirmation=True)
        assert preview.requires_confirmation is True

    def test_creation_does_not_mutate_command_envelope(self, sample_envelope):
        payload_before = dict(sample_envelope.payload)
        metadata_before = dict(sample_envelope.metadata)
        create_transaction_preview("prev-1", sample_envelope, metadata={"x": 1})
        assert dict(sample_envelope.payload) == payload_before
        assert dict(sample_envelope.metadata) == metadata_before


class TestTransactionPreviewToDict:
    def test_to_dict_returns_dict(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        result = preview.to_dict()
        assert isinstance(result, dict)
        assert result["preview_id"] == "prev-1"
        assert result["command_id"] == "cmd-1"
        assert result["status"] == "preview_created"
        assert result["messages"] == []
        assert result["requires_confirmation"] is False
        assert result["metadata"] == {}

    def test_to_dict_with_messages(self, sample_envelope):
        preview = create_transaction_preview(
            "prev-1", sample_envelope, messages=["hello"]
        )
        result = preview.to_dict()
        assert result["messages"] == ["hello"]

    def test_to_dict_returns_deep_copy(self, sample_envelope):
        preview = create_transaction_preview(
            "prev-1", sample_envelope, metadata={"nested": {"b": 2}}
        )
        result = preview.to_dict()
        result["metadata"]["nested"]["b"] = 999
        assert preview.metadata["nested"]["b"] == 2


class TestValidateTransactionPreview:
    def test_valid_preview_accepted(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        assert validate_transaction_preview(preview) is True

    def test_invalid_object_rejected(self):
        assert validate_transaction_preview("not-a-preview") is False

    def test_none_rejected(self):
        assert validate_transaction_preview(None) is False

    def test_dict_rejected(self):
        assert validate_transaction_preview({"preview_id": "prev-1"}) is False


class TestTransactionPreviewImmutability:
    def test_frozen_dataclass(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        with pytest.raises(AttributeError):
            preview.preview_id = "changed"


class TestNoStateDeltaOrEventFields:
    """Preview must not contain state delta or event commitment fields."""

    def test_no_state_delta_field(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        assert not hasattr(preview, "state_delta")
        assert "state_delta" not in preview.to_dict()

    def test_no_event_commit_field(self, sample_envelope):
        preview = create_transaction_preview("prev-1", sample_envelope)
        assert not hasattr(preview, "event_commit")
        assert "event_commit" not in preview.to_dict()
        assert not hasattr(preview, "events")
        assert "events" not in preview.to_dict()
