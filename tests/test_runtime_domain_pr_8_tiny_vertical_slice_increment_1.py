"""PR-8 Increment 1 — tiny vertical slice static state fixture and visibility boundary tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    TinyVerticalSliceError,
    TinyVerticalSliceScene,
    TinyVerticalSliceActor,
    TinyVerticalSliceNpc,
    TinyVerticalSliceHazardClock,
    TinyVerticalSliceLever,
    TinyVerticalSliceInjury,
    TinyVerticalSliceHiddenFact,
    TinyVerticalSliceWorldState,
    create_tiny_vertical_slice_world_state,
    serialize_tiny_vertical_slice_visible_state,
    serialize_tiny_vertical_slice_hidden_state_for_backend,
)


# ---------------------------------------------------------------------------
# Export smoke
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment1_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceError",
            "TinyVerticalSliceScene",
            "TinyVerticalSliceActor",
            "TinyVerticalSliceNpc",
            "TinyVerticalSliceHazardClock",
            "TinyVerticalSliceLever",
            "TinyVerticalSliceInjury",
            "TinyVerticalSliceHiddenFact",
            "TinyVerticalSliceWorldState",
            "create_tiny_vertical_slice_world_state",
            "serialize_tiny_vertical_slice_visible_state",
            "serialize_tiny_vertical_slice_hidden_state_for_backend",
        ]
        for name in expected:
            assert hasattr(domain, name), f"Missing export: {name}"


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------

class TestErrorHierarchy:
    def test_tiny_vertical_slice_error_is_value_error(self):
        assert issubclass(TinyVerticalSliceError, ValueError)

    def test_tiny_vertical_slice_error_raises(self):
        with pytest.raises(TinyVerticalSliceError):
            raise TinyVerticalSliceError("test")


# ---------------------------------------------------------------------------
# Frozen dataclasses
# ---------------------------------------------------------------------------

class TestFrozenDataclasses:
    @pytest.mark.parametrize("cls", [
        TinyVerticalSliceScene,
        TinyVerticalSliceActor,
        TinyVerticalSliceNpc,
        TinyVerticalSliceHazardClock,
        TinyVerticalSliceLever,
        TinyVerticalSliceInjury,
        TinyVerticalSliceHiddenFact,
        TinyVerticalSliceWorldState,
    ])
    def test_dataclass_is_frozen(self, cls):
        assert cls.__dataclass_params__.frozen is True


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

class TestFactory:
    def test_factory_returns_world_state(self):
        ws = create_tiny_vertical_slice_world_state()
        assert isinstance(ws, TinyVerticalSliceWorldState)

    def test_default_world_has_one_of_each(self):
        ws = create_tiny_vertical_slice_world_state()
        assert isinstance(ws.scene, TinyVerticalSliceScene)
        assert isinstance(ws.actor, TinyVerticalSliceActor)
        assert isinstance(ws.npc, TinyVerticalSliceNpc)
        assert isinstance(ws.hazard_clock, TinyVerticalSliceHazardClock)
        assert isinstance(ws.lever, TinyVerticalSliceLever)
        assert isinstance(ws.injury, TinyVerticalSliceInjury)
        assert isinstance(ws.hidden_fact, TinyVerticalSliceHiddenFact)

    def test_actor_condition_refs_include_injury_ref(self):
        ws = create_tiny_vertical_slice_world_state()
        assert ws.injury.injury_ref in ws.actor.visible_condition_refs

    def test_factory_accepts_custom_world_ref(self):
        ws = create_tiny_vertical_slice_world_state(world_ref="custom-ref")
        assert ws.world_ref == "custom-ref"

    def test_factory_accepts_custom_metadata(self):
        ws = create_tiny_vertical_slice_world_state(metadata={"key": "value"})
        assert ws.metadata["key"] == "value"


# ---------------------------------------------------------------------------
# Hazard clock validation
# ---------------------------------------------------------------------------

class TestHazardClockValidation:
    def _make_clock(self, **overrides):
        defaults = {
            "clock_ref": "c",
            "clock_label": "C",
            "visible_description": "desc",
            "current_tick": 1,
            "max_ticks": 4,
        }
        defaults.update(overrides)
        return TinyVerticalSliceHazardClock(**defaults)

    def test_rejects_bool_current_tick(self):
        with pytest.raises(TinyVerticalSliceError, match="current_tick"):
            self._make_clock(current_tick=True)

    def test_rejects_bool_max_ticks(self):
        with pytest.raises(TinyVerticalSliceError, match="max_ticks"):
            self._make_clock(max_ticks=False)

    def test_rejects_negative_current_tick(self):
        with pytest.raises(TinyVerticalSliceError, match="current_tick"):
            self._make_clock(current_tick=-1)

    def test_rejects_zero_max_ticks(self):
        with pytest.raises(TinyVerticalSliceError, match="max_ticks"):
            self._make_clock(max_ticks=0)

    def test_rejects_current_tick_greater_than_max_ticks(self):
        with pytest.raises(TinyVerticalSliceError, match="current_tick"):
            self._make_clock(current_tick=5, max_ticks=4)

    def test_accepts_current_tick_equal_to_max_ticks(self):
        clock = self._make_clock(current_tick=4, max_ticks=4)
        assert clock.current_tick == 4


# ---------------------------------------------------------------------------
# Injury severity validation
# ---------------------------------------------------------------------------

class TestInjurySeverityValidation:
    def _make_injury(self, severity):
        return TinyVerticalSliceInjury(
            injury_ref="i",
            injury_label="I",
            visible_description="desc",
            severity=severity,
        )

    @pytest.mark.parametrize("sev", ["minor", "moderate", "severe"])
    def test_accepts_valid_severity(self, sev):
        inj = self._make_injury(sev)
        assert inj.severity == sev

    def test_rejects_unknown_severity(self):
        with pytest.raises(TinyVerticalSliceError, match="severity"):
            self._make_injury("critical")


# ---------------------------------------------------------------------------
# Tuple normalization
# ---------------------------------------------------------------------------

class TestTupleNormalization:
    def test_scene_tags_normalized_to_tuple(self):
        scene = TinyVerticalSliceScene(
            scene_ref="s",
            scene_label="S",
            visible_description="desc",
            visible_tags=["a", "b"],
        )
        assert isinstance(scene.visible_tags, tuple)
        assert scene.visible_tags == ("a", "b")

    def test_actor_condition_refs_normalized_to_tuple(self):
        actor = TinyVerticalSliceActor(
            actor_ref="a",
            actor_label="A",
            visible_description="desc",
            visible_condition_refs=["x", "y"],
        )
        assert isinstance(actor.visible_condition_refs, tuple)
        assert actor.visible_condition_refs == ("x", "y")


# ---------------------------------------------------------------------------
# Metadata deep-copy and freeze
# ---------------------------------------------------------------------------

class TestMetadataFreeze:
    def test_metadata_is_mapping_proxy(self):
        ws = create_tiny_vertical_slice_world_state()
        assert isinstance(ws.metadata, MappingProxyType)
        assert isinstance(ws.scene.metadata, MappingProxyType)

    def test_metadata_deep_copied(self):
        source = {"nested": {"key": "value"}}
        ws = create_tiny_vertical_slice_world_state(metadata=source)
        source["nested"]["key"] = "changed"
        assert ws.metadata["nested"]["key"] == "value"

    def test_metadata_is_frozen(self):
        ws = create_tiny_vertical_slice_world_state(metadata={"k": "v"})
        with pytest.raises(TypeError):
            ws.metadata["new_key"] = "nope"


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_returns_exact_top_level_key_order(self):
        ws = create_tiny_vertical_slice_world_state()
        result = serialize_tiny_vertical_slice_visible_state(ws)
        expected_keys = [
            "world_ref",
            "world_label",
            "scene",
            "actor",
            "npc",
            "hazard_clock",
            "lever",
            "injury",
            "metadata",
        ]
        assert list(result.keys()) == expected_keys

    def test_omits_hidden_fact_keys(self):
        ws = create_tiny_vertical_slice_world_state()
        result = serialize_tiny_vertical_slice_visible_state(ws)
        assert "hidden_fact" not in result
        assert "hidden_fact_ref" not in result
        assert "hidden_fact_label" not in result
        assert "backend_only_description" not in result
        assert "reveal_condition" not in result

    def test_does_not_contain_hidden_fact_description_text(self):
        ws = create_tiny_vertical_slice_world_state()
        result = serialize_tiny_vertical_slice_visible_state(ws)
        serialized_text = json.dumps(result)
        assert ws.hidden_fact.backend_only_description not in serialized_text

    def test_tuple_fields_serialize_as_lists(self):
        ws = create_tiny_vertical_slice_world_state()
        result = serialize_tiny_vertical_slice_visible_state(ws)
        assert isinstance(result["scene"]["visible_tags"], list)
        assert isinstance(result["actor"]["visible_condition_refs"], list)

    def test_mapping_fields_serialize_as_dicts(self):
        ws = create_tiny_vertical_slice_world_state()
        result = serialize_tiny_vertical_slice_visible_state(ws)
        assert isinstance(result["metadata"], dict)
        assert not isinstance(result["metadata"], MappingProxyType)
        assert isinstance(result["scene"]["metadata"], dict)
        assert not isinstance(result["scene"]["metadata"], MappingProxyType)

    def test_rejects_non_world_state_input(self):
        with pytest.raises(TinyVerticalSliceError):
            serialize_tiny_vertical_slice_visible_state("not a world state")

    def test_rejects_dict_input(self):
        with pytest.raises(TinyVerticalSliceError):
            serialize_tiny_vertical_slice_visible_state({})


# ---------------------------------------------------------------------------
# Backend hidden serializer
# ---------------------------------------------------------------------------

class TestBackendHiddenSerializer:
    def test_returns_exact_top_level_key_order(self):
        ws = create_tiny_vertical_slice_world_state()
        result = serialize_tiny_vertical_slice_hidden_state_for_backend(ws)
        assert list(result.keys()) == ["world_ref", "hidden_fact"]

    def test_includes_hidden_fact_fields(self):
        ws = create_tiny_vertical_slice_world_state()
        result = serialize_tiny_vertical_slice_hidden_state_for_backend(ws)
        hf = result["hidden_fact"]
        assert "hidden_fact_ref" in hf
        assert "hidden_fact_label" in hf
        assert "backend_only_description" in hf
        assert "reveal_condition" in hf
        assert "metadata" in hf

    def test_hidden_fact_values_match_source(self):
        ws = create_tiny_vertical_slice_world_state()
        result = serialize_tiny_vertical_slice_hidden_state_for_backend(ws)
        hf = result["hidden_fact"]
        assert hf["hidden_fact_ref"] == ws.hidden_fact.hidden_fact_ref
        assert hf["hidden_fact_label"] == ws.hidden_fact.hidden_fact_label
        assert hf["backend_only_description"] == ws.hidden_fact.backend_only_description
        assert hf["reveal_condition"] == ws.hidden_fact.reveal_condition

    def test_rejects_non_world_state_input(self):
        with pytest.raises(TinyVerticalSliceError):
            serialize_tiny_vertical_slice_hidden_state_for_backend("not a world state")

    def test_rejects_dict_input(self):
        with pytest.raises(TinyVerticalSliceError):
            serialize_tiny_vertical_slice_hidden_state_for_backend({})


# ---------------------------------------------------------------------------
# Source scan — forbidden patterns
# ---------------------------------------------------------------------------

class TestSourceScan:
    _FORBIDDEN_PATTERNS = [
        "openai",
        "anthropic",
        "ollama",
        "claude",
        "call_model",
        "invoke_model",
        "generate_narration",
        "json.loads",
        "ast.literal_eval",
        "re.search",
        "re.match",
        "roll_dice",
        "commit_event(",
        "apply_delta(",
        "mutate_state",
        "persist_state",
        "replay_event",
        "state_store.get",
        "event_ledger.get",
        "open(",
        ".read_text(",
        ".write_text(",
    ]

    def test_production_module_has_no_forbidden_patterns(self):
        source_path = Path(__file__).resolve().parent.parent / "src" / "astra_runtime" / "domain" / "tiny_vertical_slice.py"
        source = source_path.read_text(encoding="utf-8")
        for pattern in self._FORBIDDEN_PATTERNS:
            assert pattern not in source, f"Forbidden pattern found in production module: {pattern!r}"
