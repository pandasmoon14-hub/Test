"""PR-8 Increment 11 — tiny vertical slice closure manifest tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    TinyVerticalSliceClosureManifest,
    TinyVerticalSliceError,
    build_tiny_vertical_slice_closure_manifest,
    create_tiny_vertical_slice_world_state,
    serialize_tiny_vertical_slice_closure_manifest_visible,
)


_REQUIRED_STAGE_NAMES = (
    "world_state",
    "command_intent",
    "command_lifecycle",
    "resource_consequence_planning_preview",
    "context_packet_projection",
    "state_delta_candidate_preview",
    "event_ledger_candidate_preview",
    "commit_dry_run",
    "commit_application",
    "post_commit_narration_packet_projection",
    "model_boundary_evaluation_fixture",
)

_COMMAND_KINDS = (
    "inspect_lever",
    "brace_mechanism",
    "pull_lever",
    "speak_to_npc",
)

_COMMAND_REFS = (
    "tiny-closure-inspect-lever-command",
    "tiny-closure-brace-mechanism-command",
    "tiny-closure-pull-lever-command",
    "tiny-closure-speak-to-npc-command",
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def manifest():
    return build_tiny_vertical_slice_closure_manifest()


@pytest.fixture()
def world():
    return create_tiny_vertical_slice_world_state()


def _make_valid_kwargs():
    m = build_tiny_vertical_slice_closure_manifest()
    stage_refs = {}
    for cmd_ref in m.command_refs:
        stage_refs[cmd_ref] = dict(m.stage_refs_by_command[cmd_ref])
    return {
        "manifest_ref": m.manifest_ref,
        "world_ref": m.world_ref,
        "command_refs": m.command_refs,
        "command_kinds": m.command_kinds,
        "stage_refs_by_command": stage_refs,
        "total_commands": m.total_commands,
        "total_stages_per_command": m.total_stages_per_command,
        "total_stage_refs": m.total_stage_refs,
        "required_stage_names": m.required_stage_names,
        "missing_stage_names": m.missing_stage_names,
        "all_commands_closed": m.all_commands_closed,
        "closure_ready": m.closure_ready,
        "visibility_boundary_preserved": m.visibility_boundary_preserved,
        "hidden_information_excluded": m.hidden_information_excluded,
        "backend_authority_preserved": m.backend_authority_preserved,
        "model_boundary_fixture_passed": m.model_boundary_fixture_passed,
        "model_boundary_fixture_failed_when_expected": m.model_boundary_fixture_failed_when_expected,
        "model_called": m.model_called,
        "narration_generated": m.narration_generated,
        "prose_parsed": m.prose_parsed,
        "state_mutated_by_manifest": m.state_mutated_by_manifest,
        "state_delta_applied_by_manifest": m.state_delta_applied_by_manifest,
        "event_committed_by_manifest": m.event_committed_by_manifest,
        "event_appended_by_manifest": m.event_appended_by_manifest,
        "persistence_authorized": m.persistence_authorized,
        "replay_authorized": m.replay_authorized,
        "rng_or_oracle_called": m.rng_or_oracle_called,
        "arithmetic_executed": m.arithmetic_executed,
        "settlement_authorized": m.settlement_authorized,
        "consequence_application_authorized": m.consequence_application_authorized,
        "backend_only_ref_ids": m.backend_only_ref_ids,
    }


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment11_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceClosureManifest",
            "build_tiny_vertical_slice_closure_manifest",
            "serialize_tiny_vertical_slice_closure_manifest_visible",
        ]
        for sym in expected:
            assert hasattr(domain, sym), f"Missing export: {sym}"
            assert sym in domain.__all__, f"Missing from __all__: {sym}"


# ---------------------------------------------------------------------------
# Dataclass validation
# ---------------------------------------------------------------------------

class TestDataclass:
    def test_frozen(self, manifest):
        assert isinstance(manifest, TinyVerticalSliceClosureManifest)
        with pytest.raises(AttributeError):
            manifest.manifest_ref = "x"

    def test_rejects_empty_manifest_ref(self):
        kw = _make_valid_kwargs()
        kw["manifest_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="manifest_ref"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_empty_world_ref(self):
        kw = _make_valid_kwargs()
        kw["world_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="world_ref"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_empty_command_refs(self):
        kw = _make_valid_kwargs()
        kw["command_refs"] = ()
        with pytest.raises(TinyVerticalSliceError, match="command_refs"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_empty_command_kinds(self):
        kw = _make_valid_kwargs()
        kw["command_kinds"] = ()
        with pytest.raises(TinyVerticalSliceError, match="command_kinds"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_command_refs_kinds_length_mismatch(self):
        kw = _make_valid_kwargs()
        kw["command_refs"] = _COMMAND_REFS[:3]
        with pytest.raises(TinyVerticalSliceError, match="len"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_command_kinds_mismatch(self):
        kw = _make_valid_kwargs()
        kw["command_kinds"] = ("inspect_lever", "brace_mechanism", "pull_lever", "unknown_kind")
        with pytest.raises(TinyVerticalSliceError, match="command_kinds"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_required_stage_names_mismatch(self):
        kw = _make_valid_kwargs()
        kw["required_stage_names"] = ("world_state",)
        with pytest.raises(TinyVerticalSliceError, match="required_stage_names"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_non_mapping_stage_refs(self):
        kw = _make_valid_kwargs()
        kw["stage_refs_by_command"] = "not-a-mapping"
        with pytest.raises(TinyVerticalSliceError, match="stage_refs_by_command"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_missing_command_key_in_stage_refs(self):
        kw = _make_valid_kwargs()
        del kw["stage_refs_by_command"][_COMMAND_REFS[0]]
        with pytest.raises(TinyVerticalSliceError, match=_COMMAND_REFS[0]):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_missing_required_stage_in_command_stage_map(self):
        kw = _make_valid_kwargs()
        del kw["stage_refs_by_command"][_COMMAND_REFS[0]]["world_state"]
        with pytest.raises(TinyVerticalSliceError, match="missing_stage_names"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_empty_stage_ref_value(self):
        kw = _make_valid_kwargs()
        kw["stage_refs_by_command"][_COMMAND_REFS[0]]["world_state"] = ""
        with pytest.raises(TinyVerticalSliceError, match="non-empty string"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_incorrect_missing_stage_names(self):
        kw = _make_valid_kwargs()
        kw["missing_stage_names"] = ("world_state",)
        with pytest.raises(TinyVerticalSliceError, match="missing_stage_names"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_incorrect_total_commands(self):
        kw = _make_valid_kwargs()
        kw["total_commands"] = 99
        with pytest.raises(TinyVerticalSliceError, match="total_commands"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_incorrect_total_stages_per_command(self):
        kw = _make_valid_kwargs()
        kw["total_stages_per_command"] = 99
        with pytest.raises(TinyVerticalSliceError, match="total_stages_per_command"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_incorrect_total_stage_refs(self):
        kw = _make_valid_kwargs()
        kw["total_stage_refs"] = 99
        with pytest.raises(TinyVerticalSliceError, match="total_stage_refs"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_incorrect_all_commands_closed(self):
        kw = _make_valid_kwargs()
        kw["all_commands_closed"] = False
        kw["closure_ready"] = False
        with pytest.raises(TinyVerticalSliceError, match="all_commands_closed"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_incorrect_closure_ready(self):
        kw = _make_valid_kwargs()
        kw["closure_ready"] = False
        with pytest.raises(TinyVerticalSliceError, match="closure_ready"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_visibility_boundary_preserved_false(self):
        kw = _make_valid_kwargs()
        kw["visibility_boundary_preserved"] = False
        kw["closure_ready"] = False
        with pytest.raises(TinyVerticalSliceError, match="visibility_boundary_preserved"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_hidden_information_excluded_false(self):
        kw = _make_valid_kwargs()
        kw["hidden_information_excluded"] = False
        kw["closure_ready"] = False
        with pytest.raises(TinyVerticalSliceError, match="hidden_information_excluded"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_backend_authority_preserved_false(self):
        kw = _make_valid_kwargs()
        kw["backend_authority_preserved"] = False
        kw["closure_ready"] = False
        with pytest.raises(TinyVerticalSliceError, match="backend_authority_preserved"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_model_boundary_fixture_passed_false(self):
        kw = _make_valid_kwargs()
        kw["model_boundary_fixture_passed"] = False
        kw["closure_ready"] = False
        with pytest.raises(TinyVerticalSliceError, match="model_boundary_fixture_passed"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_model_boundary_fixture_failed_when_expected_false(self):
        kw = _make_valid_kwargs()
        kw["model_boundary_fixture_failed_when_expected"] = False
        kw["closure_ready"] = False
        with pytest.raises(TinyVerticalSliceError, match="model_boundary_fixture_failed_when_expected"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_model_called_true(self):
        kw = _make_valid_kwargs()
        kw["model_called"] = True
        with pytest.raises(TinyVerticalSliceError, match="model_called"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_narration_generated_true(self):
        kw = _make_valid_kwargs()
        kw["narration_generated"] = True
        with pytest.raises(TinyVerticalSliceError, match="narration_generated"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_prose_parsed_true(self):
        kw = _make_valid_kwargs()
        kw["prose_parsed"] = True
        with pytest.raises(TinyVerticalSliceError, match="prose_parsed"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_state_mutated_by_manifest_true(self):
        kw = _make_valid_kwargs()
        kw["state_mutated_by_manifest"] = True
        with pytest.raises(TinyVerticalSliceError, match="state_mutated_by_manifest"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_state_delta_applied_by_manifest_true(self):
        kw = _make_valid_kwargs()
        kw["state_delta_applied_by_manifest"] = True
        with pytest.raises(TinyVerticalSliceError, match="state_delta_applied_by_manifest"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_event_committed_by_manifest_true(self):
        kw = _make_valid_kwargs()
        kw["event_committed_by_manifest"] = True
        with pytest.raises(TinyVerticalSliceError, match="event_committed_by_manifest"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_event_appended_by_manifest_true(self):
        kw = _make_valid_kwargs()
        kw["event_appended_by_manifest"] = True
        with pytest.raises(TinyVerticalSliceError, match="event_appended_by_manifest"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_persistence_authorized_true(self):
        kw = _make_valid_kwargs()
        kw["persistence_authorized"] = True
        with pytest.raises(TinyVerticalSliceError, match="persistence_authorized"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_replay_authorized_true(self):
        kw = _make_valid_kwargs()
        kw["replay_authorized"] = True
        with pytest.raises(TinyVerticalSliceError, match="replay_authorized"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_rng_or_oracle_called_true(self):
        kw = _make_valid_kwargs()
        kw["rng_or_oracle_called"] = True
        with pytest.raises(TinyVerticalSliceError, match="rng_or_oracle_called"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_arithmetic_executed_true(self):
        kw = _make_valid_kwargs()
        kw["arithmetic_executed"] = True
        with pytest.raises(TinyVerticalSliceError, match="arithmetic_executed"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_settlement_authorized_true(self):
        kw = _make_valid_kwargs()
        kw["settlement_authorized"] = True
        with pytest.raises(TinyVerticalSliceError, match="settlement_authorized"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_rejects_consequence_application_authorized_true(self):
        kw = _make_valid_kwargs()
        kw["consequence_application_authorized"] = True
        with pytest.raises(TinyVerticalSliceError, match="consequence_application_authorized"):
            TinyVerticalSliceClosureManifest(**kw)

    def test_tuple_list_fields_normalize_to_tuples(self):
        kw = _make_valid_kwargs()
        kw["command_refs"] = list(kw["command_refs"])
        kw["command_kinds"] = list(kw["command_kinds"])
        kw["required_stage_names"] = list(kw["required_stage_names"])
        kw["missing_stage_names"] = list(kw["missing_stage_names"])
        kw["backend_only_ref_ids"] = list(kw["backend_only_ref_ids"])
        result = TinyVerticalSliceClosureManifest(**kw)
        assert isinstance(result.command_refs, tuple)
        assert isinstance(result.command_kinds, tuple)
        assert isinstance(result.required_stage_names, tuple)
        assert isinstance(result.missing_stage_names, tuple)
        assert isinstance(result.backend_only_ref_ids, tuple)

    def test_metadata_deep_copied_and_frozen(self):
        kw = _make_valid_kwargs()
        source = {"key": "value"}
        kw["metadata"] = source
        result = TinyVerticalSliceClosureManifest(**kw)
        assert isinstance(result.metadata, MappingProxyType)
        source["key"] = "changed"
        assert result.metadata["key"] == "value"

    def test_stage_refs_mapping_deep_copied_frozen(self):
        kw = _make_valid_kwargs()
        original_stages = kw["stage_refs_by_command"]
        result = TinyVerticalSliceClosureManifest(**kw)
        original_stages[_COMMAND_REFS[0]]["world_state"] = "mutated"
        assert result.stage_refs_by_command[_COMMAND_REFS[0]]["world_state"] != "mutated"


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilder:
    def test_builds_valid_closure_manifest(self, manifest):
        assert isinstance(manifest, TinyVerticalSliceClosureManifest)

    def test_includes_exactly_4_commands(self, manifest):
        assert len(manifest.command_refs) == 4

    def test_includes_command_kinds_in_exact_order(self, manifest):
        assert manifest.command_kinds == _COMMAND_KINDS

    def test_includes_all_required_stages_for_each_command(self, manifest):
        for cmd_ref in manifest.command_refs:
            stage_map = manifest.stage_refs_by_command[cmd_ref]
            for stage_name in _REQUIRED_STAGE_NAMES:
                assert stage_name in stage_map, f"Missing {stage_name} for {cmd_ref}"
                assert stage_map[stage_name], f"Empty ref for {stage_name} in {cmd_ref}"

    def test_total_commands_is_4(self, manifest):
        assert manifest.total_commands == 4

    def test_total_stages_per_command(self, manifest):
        assert manifest.total_stages_per_command == len(_REQUIRED_STAGE_NAMES)

    def test_total_stage_refs_is_44(self, manifest):
        assert manifest.total_stage_refs == 44

    def test_no_missing_stage_names(self, manifest):
        assert manifest.missing_stage_names == ()

    def test_all_commands_closed(self, manifest):
        assert manifest.all_commands_closed is True

    def test_closure_ready(self, manifest):
        assert manifest.closure_ready is True

    def test_visibility_boundary_preserved(self, manifest):
        assert manifest.visibility_boundary_preserved is True

    def test_hidden_information_excluded(self, manifest):
        assert manifest.hidden_information_excluded is True

    def test_backend_authority_preserved(self, manifest):
        assert manifest.backend_authority_preserved is True

    def test_model_boundary_fixture_passed(self, manifest):
        assert manifest.model_boundary_fixture_passed is True

    def test_model_boundary_fixture_failed_when_expected(self, manifest):
        assert manifest.model_boundary_fixture_failed_when_expected is True

    def test_model_called_false(self, manifest):
        assert manifest.model_called is False

    def test_narration_generated_false(self, manifest):
        assert manifest.narration_generated is False

    def test_prose_parsed_false(self, manifest):
        assert manifest.prose_parsed is False

    def test_state_mutated_by_manifest_false(self, manifest):
        assert manifest.state_mutated_by_manifest is False

    def test_state_delta_applied_by_manifest_false(self, manifest):
        assert manifest.state_delta_applied_by_manifest is False

    def test_event_committed_by_manifest_false(self, manifest):
        assert manifest.event_committed_by_manifest is False

    def test_event_appended_by_manifest_false(self, manifest):
        assert manifest.event_appended_by_manifest is False

    def test_persistence_authorized_false(self, manifest):
        assert manifest.persistence_authorized is False

    def test_replay_authorized_false(self, manifest):
        assert manifest.replay_authorized is False

    def test_rng_or_oracle_called_false(self, manifest):
        assert manifest.rng_or_oracle_called is False

    def test_arithmetic_executed_false(self, manifest):
        assert manifest.arithmetic_executed is False

    def test_settlement_authorized_false(self, manifest):
        assert manifest.settlement_authorized is False

    def test_consequence_application_authorized_false(self, manifest):
        assert manifest.consequence_application_authorized is False

    def test_stage_ref_world_state(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["world_state"]

    def test_stage_ref_command_intent(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["command_intent"]

    def test_stage_ref_command_lifecycle(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["command_lifecycle"]

    def test_stage_ref_resource_consequence_planning_preview(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["resource_consequence_planning_preview"]

    def test_stage_ref_context_packet_projection(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["context_packet_projection"]

    def test_stage_ref_state_delta_candidate_preview(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["state_delta_candidate_preview"]

    def test_stage_ref_event_ledger_candidate_preview(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["event_ledger_candidate_preview"]

    def test_stage_ref_commit_dry_run(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["commit_dry_run"]

    def test_stage_ref_commit_application(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["commit_application"]

    def test_stage_ref_post_commit_narration_packet_projection(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["post_commit_narration_packet_projection"]

    def test_stage_ref_model_boundary_evaluation_fixture(self, manifest):
        for cmd_ref in manifest.command_refs:
            assert manifest.stage_refs_by_command[cmd_ref]["model_boundary_evaluation_fixture"]


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_rejects_non_manifest_input(self):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceClosureManifest"):
            serialize_tiny_vertical_slice_closure_manifest_visible("not-a-manifest")

    def test_exact_top_level_key_order(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        expected_keys = [
            "manifest_ref",
            "world_ref",
            "command_refs",
            "command_kinds",
            "stage_refs_by_command",
            "total_commands",
            "total_stages_per_command",
            "total_stage_refs",
            "required_stage_names",
            "missing_stage_names",
            "all_commands_closed",
            "closure_ready",
            "visibility_boundary_preserved",
            "hidden_information_excluded",
            "backend_authority_preserved",
            "model_boundary_fixture_passed",
            "model_boundary_fixture_failed_when_expected",
            "model_called",
            "narration_generated",
            "prose_parsed",
            "state_mutated_by_manifest",
            "state_delta_applied_by_manifest",
            "event_committed_by_manifest",
            "event_appended_by_manifest",
            "persistence_authorized",
            "replay_authorized",
            "rng_or_oracle_called",
            "arithmetic_executed",
            "settlement_authorized",
            "consequence_application_authorized",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_command_refs_serialized_as_list(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        assert isinstance(serialized["command_refs"], list)

    def test_command_kinds_serialized_as_list(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        assert isinstance(serialized["command_kinds"], list)

    def test_required_stage_names_serialized_as_list(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        assert isinstance(serialized["required_stage_names"], list)

    def test_missing_stage_names_serialized_as_list(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        assert isinstance(serialized["missing_stage_names"], list)

    def test_stage_refs_serialized_as_plain_dict(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        assert isinstance(serialized["stage_refs_by_command"], dict)
        for cmd_ref in serialized["stage_refs_by_command"]:
            assert isinstance(serialized["stage_refs_by_command"][cmd_ref], dict)

    def test_omits_backend_only_ref_ids(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        assert "backend_only_ref_ids" not in serialized

    def test_omits_hidden_fact_ref(self, manifest, world):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_ref not in dumped

    def test_omits_hidden_fact_label(self, manifest, world):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_label not in dumped

    def test_omits_backend_only_description(self, manifest, world):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in dumped

    def test_omits_reveal_condition(self, manifest, world):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.reveal_condition not in dumped

    def test_omits_raw_candidate_outputs(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        assert "safe_candidate_output" not in dumped
        assert "violation_candidate_output" not in dumped

    def test_omits_full_packet_payloads(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        assert "serialized_packet" not in dumped

    def test_omits_full_intermediate_dataclasses(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        assert "TinyVerticalSlice" not in dumped

    def test_does_not_contain_hidden_fact_backend_only_description(self, manifest, world):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in dumped

    def test_does_not_contain_backend_only_refs(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        for ref in manifest.backend_only_ref_ids:
            assert ref not in dumped

    def test_does_not_contain_generated_narration_prose(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        assert "generated_narration" not in dumped
        assert "narration_prose" not in dumped

    def test_shows_all_execution_flags_false(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        assert serialized["model_called"] is False
        assert serialized["narration_generated"] is False
        assert serialized["prose_parsed"] is False
        assert serialized["state_mutated_by_manifest"] is False
        assert serialized["state_delta_applied_by_manifest"] is False
        assert serialized["event_committed_by_manifest"] is False
        assert serialized["event_appended_by_manifest"] is False
        assert serialized["persistence_authorized"] is False
        assert serialized["replay_authorized"] is False
        assert serialized["rng_or_oracle_called"] is False
        assert serialized["arithmetic_executed"] is False
        assert serialized["settlement_authorized"] is False
        assert serialized["consequence_application_authorized"] is False

    def test_shows_closure_ready_true(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        assert serialized["closure_ready"] is True

    def test_metadata_serialized_as_dict(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        assert isinstance(serialized["metadata"], dict)

    def test_json_round_trips(self, manifest):
        serialized = serialize_tiny_vertical_slice_closure_manifest_visible(manifest)
        dumped = json.dumps(serialized)
        loaded = json.loads(dumped)
        assert loaded["manifest_ref"] == manifest.manifest_ref
        assert loaded["closure_ready"] is True
        assert loaded["total_stage_refs"] == 44


# ---------------------------------------------------------------------------
# Source scan
# ---------------------------------------------------------------------------

class TestSourceScan:
    @pytest.fixture(autouse=True)
    def _load_source(self):
        src = Path(__file__).resolve().parent.parent / "src" / "astra_runtime" / "domain" / "tiny_vertical_slice.py"
        self.source_text = src.read_text(encoding="utf-8")

    @pytest.mark.parametrize("forbidden", [
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
        "persist_state",
        "replay_event",
        "state_store.get",
        "event_ledger.get",
        "open(",
        ".read_text(",
        ".write_text(",
    ])
    def test_production_module_does_not_contain_forbidden(self, forbidden):
        assert forbidden not in self.source_text, f"Production module must not contain '{forbidden}'"

    def test_no_generic_apply_delta(self):
        assert "apply_delta(" not in self.source_text
