"""Focused tests for RUNTIME-IMPL-PR-6: hidden-information partition skeleton."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from astra_runtime.kernel.hidden_information import (
    ALLOWED_VISIBILITY_TIERS,
    HiddenInformationError,
    HiddenInformationRecord,
    InvalidHiddenInformationRecordError,
    VisibilityTierError,
    create_hidden_information_record,
    is_visible_to_tiers,
    redacted_copy,
    validate_hidden_information_record,
)

KERNEL_DIR = Path(__file__).resolve().parent.parent.parent / "src" / "astra_runtime" / "kernel"


class TestHiddenInformationRecord:
    def test_valid_creation(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="backend_hidden",
            redaction_label="hidden secret",
        )
        assert isinstance(rec, HiddenInformationRecord)

    def test_preserves_record_id(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
        )
        assert rec.record_id == "astra:secret:item-001"

    def test_preserves_visibility_tier(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="restricted",
            redaction_label="label",
        )
        assert rec.visibility_tier == "restricted"

    def test_preserves_payload(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
            payload={"key": "value"},
        )
        assert dict(rec.payload) == {"key": "value"}

    def test_preserves_redaction_label(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="my label",
        )
        assert rec.redaction_label == "my label"

    def test_preserves_metadata(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
            metadata={"source": "test"},
        )
        assert dict(rec.metadata) == {"source": "test"}

    @pytest.mark.parametrize("tier", sorted(ALLOWED_VISIBILITY_TIERS))
    def test_allowed_visibility_tiers(self, tier):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier=tier,
            redaction_label="label",
        )
        assert rec.visibility_tier == tier

    @pytest.mark.parametrize("tier", ["secret", "hidden", "BACKEND_HIDDEN", "Public", "", 42])
    def test_unsupported_visibility_tier_rejected(self, tier):
        with pytest.raises(VisibilityTierError):
            create_hidden_information_record(
                record_id="astra:secret:item-001",
                visibility_tier=tier,
                redaction_label="label",
            )

    @pytest.mark.parametrize("rid", ["", "   ", "bad-id", "no-prefix", 42, None])
    def test_invalid_record_id_rejected(self, rid):
        with pytest.raises(InvalidHiddenInformationRecordError):
            create_hidden_information_record(
                record_id=rid,
                visibility_tier="public",
                redaction_label="label",
            )

    @pytest.mark.parametrize("label", ["", "   ", 42, None])
    def test_empty_redaction_label_rejected(self, label):
        with pytest.raises(InvalidHiddenInformationRecordError):
            create_hidden_information_record(
                record_id="astra:secret:item-001",
                visibility_tier="public",
                redaction_label=label,
            )

    @pytest.mark.parametrize("payload", ["not a mapping", 42, [1, 2]])
    def test_non_mapping_payload_rejected(self, payload):
        with pytest.raises(InvalidHiddenInformationRecordError):
            create_hidden_information_record(
                record_id="astra:secret:item-001",
                visibility_tier="public",
                redaction_label="label",
                payload=payload,
            )

    @pytest.mark.parametrize("meta", ["not a mapping", 42, [1, 2]])
    def test_non_mapping_metadata_rejected(self, meta):
        with pytest.raises(InvalidHiddenInformationRecordError):
            create_hidden_information_record(
                record_id="astra:secret:item-001",
                visibility_tier="public",
                redaction_label="label",
                metadata=meta,
            )

    def test_payload_defaults_to_empty_mapping(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
        )
        assert dict(rec.payload) == {}

    def test_metadata_defaults_to_empty_mapping(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
        )
        assert dict(rec.metadata) == {}

    def test_payload_deep_copy_safe(self):
        inner = {"nested": [1, 2, 3]}
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
            payload=inner,
        )
        inner["nested"].append(4)
        assert list(rec.payload["nested"]) == [1, 2, 3]

    def test_metadata_deep_copy_safe(self):
        inner = {"nested": [1, 2]}
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
            metadata=inner,
        )
        inner["nested"].append(3)
        assert list(rec.metadata["nested"]) == [1, 2]

    def test_to_dict_returns_deep_copies(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
            payload={"key": [1]},
        )
        d1 = rec.to_dict()
        d2 = rec.to_dict()
        d1["payload"]["key"].append(2)
        assert d2["payload"]["key"] == [1]

    def test_validate_accepts_valid_record(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
        )
        assert validate_hidden_information_record(rec) is True

    def test_validate_rejects_invalid_object(self):
        assert validate_hidden_information_record("not a record") is False
        assert validate_hidden_information_record(42) is False
        assert validate_hidden_information_record(None) is False

    def test_frozen_immutability(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
        )
        with pytest.raises(AttributeError):
            rec.record_id = "changed"


class TestIsVisibleToTiers:
    def test_returns_true_for_allowed_tier(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
        )
        assert is_visible_to_tiers(rec, ["public", "player_visible"]) is True

    def test_returns_false_for_disallowed_tier(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="backend_hidden",
            redaction_label="label",
        )
        assert is_visible_to_tiers(rec, ["public", "player_visible"]) is False

    def test_returns_true_only_for_explicitly_allowed(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="restricted",
            redaction_label="label",
        )
        assert is_visible_to_tiers(rec, ["restricted"]) is True
        assert is_visible_to_tiers(rec, ["public"]) is False


class TestRedactedCopy:
    def test_does_not_expose_payload(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="backend_hidden",
            redaction_label="hidden secret",
            payload={"secret_data": "top-secret"},
        )
        redacted = redacted_copy(rec)
        assert dict(redacted.payload) == {}
        assert "secret_data" not in dict(redacted.payload)

    def test_preserves_record_id(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="backend_hidden",
            redaction_label="label",
            payload={"data": "secret"},
        )
        redacted = redacted_copy(rec)
        assert redacted.record_id == "astra:secret:item-001"

    def test_preserves_visibility_tier(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="restricted",
            redaction_label="label",
        )
        redacted = redacted_copy(rec)
        assert redacted.visibility_tier == "restricted"

    def test_preserves_redaction_label(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="backend_hidden",
            redaction_label="my label",
        )
        redacted = redacted_copy(rec)
        assert redacted.redaction_label == "my label"

    def test_preserves_metadata(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="backend_hidden",
            redaction_label="label",
            metadata={"source": "test"},
        )
        redacted = redacted_copy(rec)
        assert dict(redacted.metadata) == {"source": "test"}


class TestGuardrails:
    def test_no_store_save_load_reveal_permission_database_methods(self):
        rec = create_hidden_information_record(
            record_id="astra:secret:item-001",
            visibility_tier="public",
            redaction_label="label",
        )
        forbidden = ["store", "save", "load", "reveal", "permission", "database", "persist"]
        for method_name in forbidden:
            assert not hasattr(rec, method_name), f"{method_name} method must not exist"

    @pytest.mark.parametrize(
        "module",
        [
            "context_packet_compiler.py",
        ],
    )
    def test_future_module_does_not_exist(self, module):
        assert not (KERNEL_DIR / module).exists(), f"{module} must not exist yet"

    def test_domain_package_contains_only_authorized_modules(self):
        domain_dir = KERNEL_DIR.parent / "domain"
        assert domain_dir.exists(), "Domain package should exist after PR-1A"
        allowed = {"__init__.py", "command_lifecycle.py", "action_legality.py", "state_store.py", "state_projection.py", "transaction_lifecycle.py", "event_commitment.py", "validation_integration.py", "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py", "scene_command_execution_skeleton.py", "command_kind_routing_skeleton.py", "__pycache__"}
        actual = {p.name for p in domain_dir.iterdir()}
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized domain modules: {unauthorized}"

    def test_no_model_integration_package(self):
        model_dir = KERNEL_DIR.parent / "model"
        assert not model_dir.exists(), "model integration package must not exist yet"

    def test_no_prompt_template_package(self):
        prompt_dir = KERNEL_DIR.parent / "prompts"
        assert not prompt_dir.exists(), "prompt template package must not exist yet"

    def test_no_live_play_adapter_package(self):
        live_dir = KERNEL_DIR.parent / "live_play"
        assert not live_dir.exists(), "live-play adapter package must not exist yet"

    def test_no_ui_client_package(self):
        ui_dir = KERNEL_DIR.parent / "ui"
        assert not ui_dir.exists(), "UI/client package must not exist yet"
