"""PR-8 Increment 10 — tiny vertical slice model boundary evaluation fixture tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    TinyVerticalSliceError,
    TinyVerticalSliceModelBoundaryEvaluationFixture,
    TinyVerticalSlicePostCommitNarrationPacketProjection,
    ContextPacketCompilerResult,
    ModelBoundaryEvaluationCase,
    ModelBoundaryEvaluationResult,
    apply_tiny_vertical_slice_commit_application,
    build_tiny_vertical_slice_commit_dry_run_result,
    build_tiny_vertical_slice_context_packet_projection,
    build_tiny_vertical_slice_event_ledger_candidate_preview,
    build_tiny_vertical_slice_model_boundary_evaluation_fixture,
    build_tiny_vertical_slice_post_commit_narration_packet_projection,
    build_tiny_vertical_slice_resource_consequence_planning_preview,
    build_tiny_vertical_slice_state_delta_candidate_preview,
    create_tiny_vertical_slice_command_intent,
    create_tiny_vertical_slice_world_state,
    run_tiny_vertical_slice_command_lifecycle,
    serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def world():
    return create_tiny_vertical_slice_world_state()


def _make_full_chain(world, command_kind, target_ref=None, command_ref=None):
    kwargs = {"command_kind": command_kind}
    if target_ref:
        kwargs["target_ref"] = target_ref
    if command_ref:
        kwargs["command_ref"] = command_ref
    if command_kind == "speak_to_npc":
        kwargs.setdefault("target_ref", "npc-watchful-adept")
        kwargs.setdefault("declared_intent", "Speak to the watchful adept.")
    command = create_tiny_vertical_slice_command_intent(**kwargs)
    lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
    planning = build_tiny_vertical_slice_resource_consequence_planning_preview(
        state=world, lifecycle_result=lifecycle,
    )
    projection = build_tiny_vertical_slice_context_packet_projection(
        state=world, lifecycle_result=lifecycle, planning_preview=planning,
    )
    delta = build_tiny_vertical_slice_state_delta_candidate_preview(
        state=world, lifecycle_result=lifecycle,
        planning_preview=planning, context_projection=projection,
    )
    event = build_tiny_vertical_slice_event_ledger_candidate_preview(
        state=world, lifecycle_result=lifecycle,
        planning_preview=planning, context_projection=projection,
        delta_preview=delta,
    )
    return lifecycle, planning, projection, delta, event


def _make_commit_application(world, command_kind, command_ref=None):
    lc, pl, pj, dp, ep = _make_full_chain(world, command_kind, command_ref=command_ref)
    dr = build_tiny_vertical_slice_commit_dry_run_result(
        state=world, lifecycle_result=lc,
        planning_preview=pl, context_projection=pj,
        delta_preview=dp, event_preview=ep,
    )
    return apply_tiny_vertical_slice_commit_application(state=world, dry_run_result=dr)


def _make_projection(world, command_kind, command_ref=None):
    commit = _make_commit_application(world, command_kind, command_ref=command_ref)
    return build_tiny_vertical_slice_post_commit_narration_packet_projection(
        commit_result=commit,
    )


def _make_fixture(world, command_kind="inspect_lever", command_ref=None):
    proj = _make_projection(world, command_kind, command_ref=command_ref)
    return build_tiny_vertical_slice_model_boundary_evaluation_fixture(
        projection=proj,
    )


@pytest.fixture()
def default_fixture(world):
    return _make_fixture(world, "inspect_lever")


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment10_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceModelBoundaryEvaluationFixture",
            "build_tiny_vertical_slice_model_boundary_evaluation_fixture",
            "serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible",
        ]
        for sym in expected:
            assert hasattr(domain, sym), f"Missing export: {sym}"
            assert sym in domain.__all__, f"Missing from __all__: {sym}"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

class TestDataclass:
    def test_frozen(self, default_fixture):
        assert isinstance(default_fixture, TinyVerticalSliceModelBoundaryEvaluationFixture)
        with pytest.raises(AttributeError):
            default_fixture.fixture_ref = "x"

    def test_rejects_empty_fixture_ref(self, world):
        proj = _make_projection(world, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="fixture_ref"):
            build_tiny_vertical_slice_model_boundary_evaluation_fixture(
                projection=proj,
                fixture_ref="",
            )

    def test_rejects_non_projection_input(self):
        with pytest.raises(TinyVerticalSliceError):
            build_tiny_vertical_slice_model_boundary_evaluation_fixture(
                projection="not-a-projection",
            )

    def test_packet_result_is_context_packet_compiler_result(self, default_fixture):
        assert isinstance(default_fixture.packet_result, ContextPacketCompilerResult)

    def test_safe_case_is_model_boundary_evaluation_case(self, default_fixture):
        assert isinstance(default_fixture.safe_case, ModelBoundaryEvaluationCase)

    def test_safe_result_is_model_boundary_evaluation_result(self, default_fixture):
        assert isinstance(default_fixture.safe_result, ModelBoundaryEvaluationResult)

    def test_violation_case_is_model_boundary_evaluation_case(self, default_fixture):
        assert isinstance(default_fixture.violation_case, ModelBoundaryEvaluationCase)

    def test_violation_result_is_model_boundary_evaluation_result(self, default_fixture):
        assert isinstance(default_fixture.violation_result, ModelBoundaryEvaluationResult)

    def test_packet_result_packet_kind_matches(self, default_fixture):
        assert default_fixture.packet_result.packet_kind == default_fixture.packet_kind

    def test_safe_case_shares_packet_result_identity(self, default_fixture):
        assert default_fixture.safe_case.packet_result is default_fixture.packet_result

    def test_violation_case_shares_packet_result_identity(self, default_fixture):
        assert default_fixture.violation_case.packet_result is default_fixture.packet_result

    def test_safe_result_case_ref_matches_safe_case(self, default_fixture):
        assert default_fixture.safe_result.case_ref == default_fixture.safe_case.case_ref

    def test_violation_result_case_ref_matches_violation_case(self, default_fixture):
        assert default_fixture.violation_result.case_ref == default_fixture.violation_case.case_ref

    def test_safe_case_candidate_model_ref_matches(self, default_fixture):
        assert default_fixture.safe_case.candidate_model_ref == default_fixture.candidate_model_ref

    def test_violation_case_candidate_model_ref_matches(self, default_fixture):
        assert default_fixture.violation_case.candidate_model_ref == default_fixture.candidate_model_ref

    def test_safe_case_expected_output_family_matches(self, default_fixture):
        assert default_fixture.safe_case.expected_output_family == default_fixture.expected_output_family

    def test_violation_case_expected_output_family_matches(self, default_fixture):
        assert default_fixture.violation_case.expected_output_family == default_fixture.expected_output_family

    def test_safe_status_matches_safe_result_status(self, default_fixture):
        assert default_fixture.safe_status == default_fixture.safe_result.status

    def test_violation_status_matches_violation_result_status(self, default_fixture):
        assert default_fixture.violation_status == default_fixture.violation_result.status

    def test_safe_violation_codes_matches_safe_result(self, default_fixture):
        assert default_fixture.safe_violation_codes == default_fixture.safe_result.violation_codes

    def test_violation_codes_matches_violation_result(self, default_fixture):
        assert default_fixture.violation_codes == default_fixture.violation_result.violation_codes

    def test_forbidden_field_hits_matches_violation_result(self, default_fixture):
        assert default_fixture.forbidden_field_hits == default_fixture.violation_result.forbidden_field_hits

    def test_model_called_false(self, default_fixture):
        assert default_fixture.model_called is False

    def test_narration_generated_false(self, default_fixture):
        assert default_fixture.narration_generated is False

    def test_prose_parsed_false(self, default_fixture):
        assert default_fixture.prose_parsed is False

    def test_state_mutated_false(self, default_fixture):
        assert default_fixture.state_mutated is False

    def test_state_delta_applied_false(self, default_fixture):
        assert default_fixture.state_delta_applied is False

    def test_event_committed_false(self, default_fixture):
        assert default_fixture.event_committed is False

    def test_event_appended_false(self, default_fixture):
        assert default_fixture.event_appended is False

    def test_persistence_authorized_false(self, default_fixture):
        assert default_fixture.persistence_authorized is False

    def test_replay_authorized_false(self, default_fixture):
        assert default_fixture.replay_authorized is False

    def test_rng_or_oracle_called_false(self, default_fixture):
        assert default_fixture.rng_or_oracle_called is False

    def test_metadata_frozen(self, default_fixture):
        assert isinstance(default_fixture.metadata, MappingProxyType)

    def test_backend_only_ref_ids_is_tuple(self, default_fixture):
        assert isinstance(default_fixture.backend_only_ref_ids, tuple)

    def test_safe_candidate_output_keys_is_tuple(self, default_fixture):
        assert isinstance(default_fixture.safe_candidate_output_keys, tuple)

    def test_violation_candidate_output_keys_is_tuple(self, default_fixture):
        assert isinstance(default_fixture.violation_candidate_output_keys, tuple)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilder:
    def test_inspect_lever_builds_valid_fixture(self, world):
        fixture = _make_fixture(world, "inspect_lever")
        assert isinstance(fixture, TinyVerticalSliceModelBoundaryEvaluationFixture)

    def test_pull_lever_builds_valid_fixture(self, world):
        fixture = _make_fixture(world, "pull_lever")
        assert isinstance(fixture, TinyVerticalSliceModelBoundaryEvaluationFixture)

    def test_brace_mechanism_builds_valid_fixture(self, world):
        fixture = _make_fixture(world, "brace_mechanism")
        assert isinstance(fixture, TinyVerticalSliceModelBoundaryEvaluationFixture)

    def test_speak_to_npc_builds_valid_fixture(self, world):
        fixture = _make_fixture(world, "speak_to_npc")
        assert isinstance(fixture, TinyVerticalSliceModelBoundaryEvaluationFixture)

    def test_safe_result_passed(self, default_fixture):
        assert default_fixture.safe_result.passed is True

    def test_safe_result_status_passed(self, default_fixture):
        assert default_fixture.safe_result.status == "passed"

    def test_safe_result_no_violation_codes(self, default_fixture):
        assert default_fixture.safe_result.violation_codes == ()

    def test_violation_result_failed(self, default_fixture):
        assert default_fixture.violation_result.passed is False

    def test_violation_result_status_failed(self, default_fixture):
        assert default_fixture.violation_result.status == "failed"

    def test_violation_result_has_violation_codes(self, default_fixture):
        assert len(default_fixture.violation_result.violation_codes) > 0

    def test_violation_has_forbidden_authority_field(self, default_fixture):
        assert "forbidden_authority_field_present" in default_fixture.violation_result.violation_codes

    def test_violation_has_hidden_information_claim(self, default_fixture):
        assert "hidden_information_claim_present" in default_fixture.violation_result.violation_codes

    def test_violation_has_state_mutation_claim(self, default_fixture):
        assert "state_mutation_claim_present" in default_fixture.violation_result.violation_codes

    def test_violation_has_event_commit_claim(self, default_fixture):
        assert "event_commit_claim_present" in default_fixture.violation_result.violation_codes

    def test_violation_has_random_result_claim(self, default_fixture):
        assert "random_result_claim_present" in default_fixture.violation_result.violation_codes

    def test_violation_has_durable_truth_claim(self, default_fixture):
        assert "durable_truth_claim_present" in default_fixture.violation_result.violation_codes

    def test_violation_forbidden_field_hits_include_hidden_fact(self, default_fixture):
        assert "hidden_fact" in default_fixture.forbidden_field_hits

    def test_violation_forbidden_field_hits_include_state_delta(self, default_fixture):
        assert "state_delta" in default_fixture.forbidden_field_hits

    def test_violation_forbidden_field_hits_include_commit_event(self, default_fixture):
        assert "commit_event" in default_fixture.forbidden_field_hits

    def test_violation_forbidden_field_hits_include_rng_result(self, default_fixture):
        assert "rng_result" in default_fixture.forbidden_field_hits

    def test_violation_forbidden_field_hits_include_durable_truth(self, default_fixture):
        assert "durable_truth" in default_fixture.forbidden_field_hits

    def test_packet_result_assembly_succeeded(self, default_fixture):
        assert default_fixture.packet_result.assembly_succeeded is True

    def test_packet_result_hidden_information_excluded(self, default_fixture):
        assert default_fixture.packet_result.hidden_information_excluded is True

    def test_packet_result_non_authority_seal_present(self, default_fixture):
        assert default_fixture.packet_result.non_authority_seal_present is True

    def test_packet_kind_is_single_event_narration(self, default_fixture):
        assert default_fixture.packet_kind == "single_event_narration"

    def test_expected_output_family_default(self, default_fixture):
        assert default_fixture.expected_output_family == "narration_display"

    def test_candidate_model_ref_default(self, default_fixture):
        assert default_fixture.candidate_model_ref == "static-fixture-narrator"

    def test_safe_candidate_output_keys_present(self, default_fixture):
        assert len(default_fixture.safe_candidate_output_keys) > 0
        assert "output_family" in default_fixture.safe_candidate_output_keys

    def test_violation_candidate_output_keys_present(self, default_fixture):
        assert len(default_fixture.violation_candidate_output_keys) > 0
        assert "hidden_fact" in default_fixture.violation_candidate_output_keys

    def test_fixture_does_not_call_model(self, default_fixture):
        assert default_fixture.model_called is False

    def test_fixture_does_not_generate_narration(self, default_fixture):
        assert default_fixture.narration_generated is False

    def test_fixture_does_not_mutate_state(self, world):
        original_lever = world.lever.visible_state
        original_clock = world.hazard_clock.current_tick
        original_npc = world.npc.visible_disposition
        _make_fixture(world, "pull_lever")
        assert world.lever.visible_state == original_lever
        assert world.hazard_clock.current_tick == original_clock
        assert world.npc.visible_disposition == original_npc

    def test_rejects_projection_with_packet_validated_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        bad_proj = object.__new__(TinyVerticalSlicePostCommitNarrationPacketProjection)
        for attr in vars(proj):
            object.__setattr__(bad_proj, attr, getattr(proj, attr))
        object.__setattr__(bad_proj, "packet_validated", False)
        with pytest.raises(TinyVerticalSliceError, match="packet_validated"):
            build_tiny_vertical_slice_model_boundary_evaluation_fixture(
                projection=bad_proj,
            )

    def test_rejects_projection_with_model_called_true(self, world):
        proj = _make_projection(world, "inspect_lever")
        bad_proj = object.__new__(TinyVerticalSlicePostCommitNarrationPacketProjection)
        for attr in vars(proj):
            object.__setattr__(bad_proj, attr, getattr(proj, attr))
        object.__setattr__(bad_proj, "model_called", True)
        with pytest.raises(TinyVerticalSliceError, match="model_called"):
            build_tiny_vertical_slice_model_boundary_evaluation_fixture(
                projection=bad_proj,
            )

    def test_rejects_projection_with_narration_generated_true(self, world):
        proj = _make_projection(world, "inspect_lever")
        bad_proj = object.__new__(TinyVerticalSlicePostCommitNarrationPacketProjection)
        for attr in vars(proj):
            object.__setattr__(bad_proj, attr, getattr(proj, attr))
        object.__setattr__(bad_proj, "narration_generated", True)
        with pytest.raises(TinyVerticalSliceError, match="narration_generated"):
            build_tiny_vertical_slice_model_boundary_evaluation_fixture(
                projection=bad_proj,
            )

    def test_custom_fixture_ref(self, world):
        proj = _make_projection(world, "inspect_lever")
        fixture = build_tiny_vertical_slice_model_boundary_evaluation_fixture(
            projection=proj,
            fixture_ref="custom-fixture-ref",
        )
        assert fixture.fixture_ref == "custom-fixture-ref"

    def test_custom_candidate_model_ref(self, world):
        proj = _make_projection(world, "inspect_lever")
        fixture = build_tiny_vertical_slice_model_boundary_evaluation_fixture(
            projection=proj,
            candidate_model_ref="custom-model",
        )
        assert fixture.candidate_model_ref == "custom-model"

    def test_custom_expected_output_family(self, world):
        proj = _make_projection(world, "inspect_lever")
        fixture = build_tiny_vertical_slice_model_boundary_evaluation_fixture(
            projection=proj,
            expected_output_family="visible_summary",
        )
        assert fixture.expected_output_family == "visible_summary"


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_rejects_non_fixture_input(self):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceModelBoundaryEvaluationFixture"):
            serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible("not-a-fixture")

    def test_exact_top_level_keys(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        expected_keys = [
            "fixture_ref",
            "command_ref",
            "world_ref",
            "commit_ref",
            "projection_ref",
            "candidate_model_ref",
            "expected_output_family",
            "packet_kind",
            "safe_candidate_output_keys",
            "violation_candidate_output_keys",
            "safe_status",
            "violation_status",
            "safe_violation_codes",
            "violation_codes",
            "forbidden_field_hits",
            "model_called",
            "narration_generated",
            "prose_parsed",
            "state_mutated",
            "state_delta_applied",
            "event_committed",
            "event_appended",
            "persistence_authorized",
            "replay_authorized",
            "rng_or_oracle_called",
            "packet_result",
            "safe_result",
            "violation_result",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_packet_result_serialized_as_dict(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert isinstance(serialized["packet_result"], dict)
        assert "request_ref" in serialized["packet_result"]
        assert "packet_kind" in serialized["packet_result"]

    def test_safe_result_serialized_as_dict(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert isinstance(serialized["safe_result"], dict)
        assert "case_ref" in serialized["safe_result"]
        assert "status" in serialized["safe_result"]
        assert "passed" in serialized["safe_result"]

    def test_violation_result_serialized_as_dict(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert isinstance(serialized["violation_result"], dict)
        assert "case_ref" in serialized["violation_result"]
        assert "status" in serialized["violation_result"]

    def test_safe_result_shows_passed_true(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["safe_result"]["passed"] is True

    def test_violation_result_shows_passed_false(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["violation_result"]["passed"] is False

    def test_safe_status_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["safe_status"] == "passed"

    def test_violation_status_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["violation_status"] == "failed"

    def test_model_called_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["model_called"] is False

    def test_narration_generated_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["narration_generated"] is False

    def test_prose_parsed_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["prose_parsed"] is False

    def test_state_mutated_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["state_mutated"] is False

    def test_state_delta_applied_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["state_delta_applied"] is False

    def test_event_committed_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["event_committed"] is False

    def test_event_appended_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["event_appended"] is False

    def test_persistence_authorized_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["persistence_authorized"] is False

    def test_replay_authorized_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["replay_authorized"] is False

    def test_rng_or_oracle_called_false_in_serialized(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert serialized["rng_or_oracle_called"] is False

    def test_safe_candidate_output_keys_serialize_as_list(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert isinstance(serialized["safe_candidate_output_keys"], list)

    def test_violation_candidate_output_keys_serialize_as_list(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert isinstance(serialized["violation_candidate_output_keys"], list)

    def test_safe_violation_codes_serialize_as_list(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert isinstance(serialized["safe_violation_codes"], list)
        assert serialized["safe_violation_codes"] == []

    def test_violation_codes_serialize_as_list(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert isinstance(serialized["violation_codes"], list)
        assert len(serialized["violation_codes"]) > 0

    def test_forbidden_field_hits_serialize_as_list(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert isinstance(serialized["forbidden_field_hits"], list)
        assert len(serialized["forbidden_field_hits"]) > 0

    def test_metadata_serializes_as_dict(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert isinstance(serialized["metadata"], dict)

    def test_omits_backend_only_ref_ids(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        assert "backend_only_ref_ids" not in serialized

    def test_omits_hidden_fact_ref(self, world):
        fixture = _make_fixture(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(fixture)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_ref not in dumped

    def test_omits_hidden_fact_label(self, world):
        fixture = _make_fixture(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(fixture)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_label not in dumped

    def test_omits_backend_only_description(self, world):
        fixture = _make_fixture(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(fixture)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in dumped

    def test_omits_reveal_condition(self, world):
        fixture = _make_fixture(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(fixture)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.reveal_condition not in dumped

    def test_does_not_contain_hidden_fact_description_anywhere(self, world):
        for kind in ("inspect_lever", "brace_mechanism", "pull_lever", "speak_to_npc"):
            fixture = _make_fixture(world, kind)
            serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(fixture)
            dumped = json.dumps(serialized)
            assert world.hidden_fact.backend_only_description not in dumped

    def test_does_not_contain_backend_only_refs_anywhere(self, world):
        for kind in ("inspect_lever", "brace_mechanism", "pull_lever"):
            fixture = _make_fixture(world, kind)
            serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(fixture)
            dumped = json.dumps(serialized)
            for ref in fixture.backend_only_ref_ids:
                assert ref not in dumped

    def test_json_round_trips(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        dumped = json.dumps(serialized)
        loaded = json.loads(dumped)
        assert loaded["fixture_ref"] == default_fixture.fixture_ref
        assert loaded["safe_status"] == "passed"
        assert loaded["violation_status"] == "failed"

    def test_compact_packet_result_has_expected_keys(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        pr = serialized["packet_result"]
        expected = {
            "request_ref", "packet_kind", "assembly_succeeded",
            "serialization_succeeded", "audit_succeeded",
            "hidden_information_excluded", "non_authority_seal_present",
            "warnings", "non_authority_seal", "metadata",
        }
        assert set(pr.keys()) == expected

    def test_compact_eval_result_has_expected_keys(self, default_fixture):
        serialized = serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(default_fixture)
        for key in ("safe_result", "violation_result"):
            er = serialized[key]
            expected = {
                "case_ref", "candidate_model_ref", "packet_kind",
                "expected_output_family", "status", "passed",
                "violation_codes", "forbidden_field_hits",
                "packet_warning_refs", "metadata",
            }
            assert set(er.keys()) == expected


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

    def test_fixture_does_not_contain_narration_attribute(self, default_fixture):
        assert not hasattr(default_fixture, "narration")
        assert not hasattr(default_fixture, "generated_narration")

    def test_fixture_does_not_contain_model_output(self, default_fixture):
        assert not hasattr(default_fixture, "model_output")
        assert not hasattr(default_fixture, "model_response")
