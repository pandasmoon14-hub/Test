"""Focused tests for RUNTIME-IMPL-PR-6: context projection skeleton."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from astra_runtime.kernel.hidden_information import (
    ALLOWED_VISIBILITY_TIERS,
    HiddenInformationRecord,
    create_hidden_information_record,
)
from astra_runtime.kernel.context_projection import (
    ContextProjection,
    ContextProjectionError,
    ContextProjectionItem,
    InvalidContextProjectionError,
    InvalidContextProjectionItemError,
    create_context_projection,
    create_context_projection_item,
    project_hidden_records,
    validate_context_projection,
    validate_context_projection_item,
)

KERNEL_DIR = Path(__file__).resolve().parent.parent.parent / "src" / "astra_runtime" / "kernel"


class TestContextProjectionItem:
    def test_valid_creation(self):
        item = create_context_projection_item(
            record_id="astra:info:rec-001",
            visibility_tier="public",
            redacted=False,
        )
        assert isinstance(item, ContextProjectionItem)

    def test_invalid_record_id_rejected(self):
        with pytest.raises(InvalidContextProjectionItemError):
            create_context_projection_item(
                record_id="bad-id",
                visibility_tier="public",
                redacted=False,
            )

    def test_invalid_visibility_tier_rejected(self):
        with pytest.raises(InvalidContextProjectionItemError):
            create_context_projection_item(
                record_id="astra:info:rec-001",
                visibility_tier="invalid_tier",
                redacted=False,
            )

    @pytest.mark.parametrize("payload", ["not a mapping", 42, [1, 2]])
    def test_non_mapping_payload_rejected(self, payload):
        with pytest.raises(InvalidContextProjectionItemError):
            create_context_projection_item(
                record_id="astra:info:rec-001",
                visibility_tier="public",
                redacted=False,
                payload=payload,
            )

    @pytest.mark.parametrize("redacted", [1, 0, "true", None])
    def test_non_bool_redacted_rejected(self, redacted):
        with pytest.raises(InvalidContextProjectionItemError):
            create_context_projection_item(
                record_id="astra:info:rec-001",
                visibility_tier="public",
                redacted=redacted,
            )

    def test_item_payload_deep_copy_safe(self):
        inner = {"nested": [1, 2, 3]}
        item = create_context_projection_item(
            record_id="astra:info:rec-001",
            visibility_tier="public",
            redacted=False,
            payload=inner,
        )
        inner["nested"].append(4)
        assert list(item.payload["nested"]) == [1, 2, 3]

    def test_item_metadata_deep_copy_safe(self):
        inner = {"nested": [1, 2]}
        item = create_context_projection_item(
            record_id="astra:info:rec-001",
            visibility_tier="public",
            redacted=False,
            metadata=inner,
        )
        inner["nested"].append(3)
        assert list(item.metadata["nested"]) == [1, 2]

    def test_to_dict_returns_deep_copies(self):
        item = create_context_projection_item(
            record_id="astra:info:rec-001",
            visibility_tier="public",
            redacted=False,
            payload={"key": [1]},
        )
        d1 = item.to_dict()
        d2 = item.to_dict()
        d1["payload"]["key"].append(2)
        assert d2["payload"]["key"] == [1]

    def test_validate_accepts_valid_item(self):
        item = create_context_projection_item(
            record_id="astra:info:rec-001",
            visibility_tier="public",
            redacted=False,
        )
        assert validate_context_projection_item(item) is True

    def test_validate_rejects_invalid_object(self):
        assert validate_context_projection_item("not an item") is False
        assert validate_context_projection_item(42) is False

    def test_frozen_immutability(self):
        item = create_context_projection_item(
            record_id="astra:info:rec-001",
            visibility_tier="public",
            redacted=False,
        )
        with pytest.raises(AttributeError):
            item.record_id = "changed"


class TestContextProjection:
    def test_valid_creation(self):
        proj = create_context_projection(
            projection_id="proj-001",
            subject_ref="player-1",
            allowed_visibility_tiers=["public", "player_visible"],
        )
        assert isinstance(proj, ContextProjection)

    @pytest.mark.parametrize("pid", ["", "   ", 42, None])
    def test_invalid_projection_id_rejected(self, pid):
        with pytest.raises(InvalidContextProjectionError):
            create_context_projection(
                projection_id=pid,
                subject_ref="player-1",
                allowed_visibility_tiers=["public"],
            )

    @pytest.mark.parametrize("sref", ["", "   ", 42, None])
    def test_invalid_subject_ref_rejected(self, sref):
        with pytest.raises(InvalidContextProjectionError):
            create_context_projection(
                projection_id="proj-001",
                subject_ref=sref,
                allowed_visibility_tiers=["public"],
            )

    def test_invalid_allowed_tier_entries_rejected(self):
        with pytest.raises(InvalidContextProjectionError):
            create_context_projection(
                projection_id="proj-001",
                subject_ref="player-1",
                allowed_visibility_tiers=["public", "invalid_tier"],
            )

    def test_invalid_item_entries_rejected(self):
        with pytest.raises(InvalidContextProjectionError):
            create_context_projection(
                projection_id="proj-001",
                subject_ref="player-1",
                allowed_visibility_tiers=["public"],
                items=["not an item"],
            )

    def test_projection_metadata_deep_copy_safe(self):
        inner = {"nested": [1, 2]}
        proj = create_context_projection(
            projection_id="proj-001",
            subject_ref="player-1",
            allowed_visibility_tiers=["public"],
            metadata=inner,
        )
        inner["nested"].append(3)
        assert list(proj.metadata["nested"]) == [1, 2]

    def test_to_dict_returns_deep_copies(self):
        proj = create_context_projection(
            projection_id="proj-001",
            subject_ref="player-1",
            allowed_visibility_tiers=["public"],
            metadata={"key": [1]},
        )
        d1 = proj.to_dict()
        d2 = proj.to_dict()
        d1["metadata"]["key"].append(2)
        assert d2["metadata"]["key"] == [1]

    def test_validate_accepts_valid_projection(self):
        proj = create_context_projection(
            projection_id="proj-001",
            subject_ref="player-1",
            allowed_visibility_tiers=["public"],
        )
        assert validate_context_projection(proj) is True

    def test_validate_rejects_invalid_object(self):
        assert validate_context_projection("not a projection") is False
        assert validate_context_projection(42) is False

    def test_frozen_immutability(self):
        proj = create_context_projection(
            projection_id="proj-001",
            subject_ref="player-1",
            allowed_visibility_tiers=["public"],
        )
        with pytest.raises(AttributeError):
            proj.projection_id = "changed"


class TestProjectHiddenRecords:
    def _make_record(self, record_id, tier, payload=None):
        return create_hidden_information_record(
            record_id=record_id,
            visibility_tier=tier,
            redaction_label="test-label",
            payload=payload,
        )

    def test_includes_payload_for_allowed_tiers(self):
        rec = self._make_record("astra:info:rec-001", "public", {"data": "visible"})
        proj = project_hidden_records(
            projection_id="proj-001",
            subject_ref="player-1",
            records=[rec],
            allowed_visibility_tiers=["public"],
        )
        assert len(proj.items) == 1
        assert proj.items[0].redacted is False
        assert dict(proj.items[0].payload) == {"data": "visible"}

    def test_redacts_payload_for_disallowed_tiers(self):
        rec = self._make_record("astra:secret:item-001", "backend_hidden", {"secret": "data"})
        proj = project_hidden_records(
            projection_id="proj-001",
            subject_ref="player-1",
            records=[rec],
            allowed_visibility_tiers=["public", "player_visible"],
        )
        assert len(proj.items) == 1
        assert proj.items[0].redacted is True
        assert dict(proj.items[0].payload) == {}

    def test_never_leaks_backend_hidden_payload(self):
        rec = self._make_record(
            "astra:secret:item-001",
            "backend_hidden",
            {"top_secret": "never_leak"},
        )
        proj = project_hidden_records(
            projection_id="proj-001",
            subject_ref="player-1",
            records=[rec],
            allowed_visibility_tiers=["public", "player_visible", "restricted", "redacted"],
        )
        assert proj.items[0].redacted is True
        assert "top_secret" not in dict(proj.items[0].payload)

    def test_preserves_item_order(self):
        records = [
            self._make_record("astra:info:a-001", "public"),
            self._make_record("astra:info:b-002", "backend_hidden"),
            self._make_record("astra:info:c-003", "player_visible"),
        ]
        proj = project_hidden_records(
            projection_id="proj-001",
            subject_ref="player-1",
            records=records,
            allowed_visibility_tiers=["public", "player_visible"],
        )
        assert [item.record_id for item in proj.items] == [
            "astra:info:a-001",
            "astra:info:b-002",
            "astra:info:c-003",
        ]

    def test_preserves_record_ids(self):
        rec = self._make_record("astra:info:rec-001", "public")
        proj = project_hidden_records(
            projection_id="proj-001",
            subject_ref="player-1",
            records=[rec],
            allowed_visibility_tiers=["public"],
        )
        assert proj.items[0].record_id == "astra:info:rec-001"

    def test_preserves_redacted_flags(self):
        records = [
            self._make_record("astra:info:a-001", "public"),
            self._make_record("astra:info:b-002", "backend_hidden"),
        ]
        proj = project_hidden_records(
            projection_id="proj-001",
            subject_ref="player-1",
            records=records,
            allowed_visibility_tiers=["public"],
        )
        assert proj.items[0].redacted is False
        assert proj.items[1].redacted is True

    def test_rejects_non_hidden_record_inputs(self):
        with pytest.raises(InvalidContextProjectionError):
            project_hidden_records(
                projection_id="proj-001",
                subject_ref="player-1",
                records=["not a record"],
                allowed_visibility_tiers=["public"],
            )

    def test_mixed_visibility_projection(self):
        records = [
            self._make_record("astra:info:pub-001", "public", {"pub": "data"}),
            self._make_record("astra:info:pv-002", "player_visible", {"pv": "data"}),
            self._make_record("astra:info:res-003", "restricted", {"res": "data"}),
            self._make_record("astra:info:hid-004", "backend_hidden", {"hid": "secret"}),
        ]
        proj = project_hidden_records(
            projection_id="proj-001",
            subject_ref="player-1",
            records=records,
            allowed_visibility_tiers=["public", "player_visible"],
        )
        assert proj.items[0].redacted is False
        assert dict(proj.items[0].payload) == {"pub": "data"}
        assert proj.items[1].redacted is False
        assert dict(proj.items[1].payload) == {"pv": "data"}
        assert proj.items[2].redacted is True
        assert dict(proj.items[2].payload) == {}
        assert proj.items[3].redacted is True
        assert dict(proj.items[3].payload) == {}


class TestGuardrails:
    def test_no_packet_compiler_prompt_model_ui_methods(self):
        item = create_context_projection_item(
            record_id="astra:info:rec-001",
            visibility_tier="public",
            redacted=False,
        )
        forbidden = ["compile", "render", "prompt", "model", "ui", "narrate", "template"]
        for method_name in forbidden:
            assert not hasattr(item, method_name), f"{method_name} method must not exist"

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
