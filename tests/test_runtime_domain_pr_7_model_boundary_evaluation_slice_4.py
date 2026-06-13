"""Tests for PR-7 Slice 4 — Captured Output Fixture Adapter."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType
from typing import Any

import pytest

from astra_runtime.domain import (
    ModelBoundaryCapturedOutputFixture,
    ModelBoundaryCapturedOutputFixtureError,
    ModelBoundaryEvaluationCase,
    ModelBoundaryEvaluationError,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
    create_model_boundary_case_from_captured_output_fixture,
    create_model_boundary_captured_output_fixture,
)
from astra_runtime.domain.context_packet_compiler import (
    ContextPacketCompilerResult,
)
from astra_runtime.domain.model_boundary_evaluation import (
    MODEL_BOUNDARY_OUTPUT_FAMILIES,
)


def _make_packet_result(warnings: tuple[str, ...] = ()) -> ContextPacketCompilerResult:
    """Build a valid ContextPacketCompilerResult through the PR-6 route."""
    request = create_context_packet_assembly_request(
        request_ref="req-1",
        packet_kind="single_event_narration",
        packet_payload={
            "event_ref": "evt-1",
            "event_kind": "move",
            "visible_fact_refs": ["fact-1"],
        },
        assembly_timestamp="2026-06-13T12:00:00Z",
    )
    result = compile_context_packet_from_request(request)
    if warnings:
        return ContextPacketCompilerResult(
            request_ref=result.request_ref,
            packet_kind=result.packet_kind,
            serialized_packet=dict(result.serialized_packet),
            audit_report=result.audit_report,
            assembly_succeeded=result.assembly_succeeded,
            serialization_succeeded=result.serialization_succeeded,
            audit_succeeded=result.audit_succeeded,
            hidden_information_excluded=result.hidden_information_excluded,
            non_authority_seal_present=result.non_authority_seal_present,
            warnings=warnings,
        )
    return result


def _make_fixture(
    *,
    fixture_ref: str = "fixture-1",
    capture_ref: str = "capture-1",
    candidate_model_ref: str = "model-1",
    expected_output_family: str = "narration_display",
    packet_result: ContextPacketCompilerResult | None = None,
    candidate_output: dict[str, Any] | None = None,
    raw_captured_text: str | None = "The knight moves forward.",
    evaluator_notes: tuple[str, ...] = ("note-1",),
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryCapturedOutputFixture:
    """Build a valid ModelBoundaryCapturedOutputFixture."""
    return create_model_boundary_captured_output_fixture(
        fixture_ref=fixture_ref,
        capture_ref=capture_ref,
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
        packet_result=packet_result if packet_result is not None else _make_packet_result(),
        candidate_output=candidate_output if candidate_output is not None else {"display": "The knight moves forward."},
        raw_captured_text=raw_captured_text,
        evaluator_notes=evaluator_notes,
        metadata=metadata if metadata is not None else {"source": "manual"},
    )


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------

def test_package_exports() -> None:
    """All PR-7 Slice 4 public symbols are exported from astra_runtime.domain."""
    from astra_runtime.domain import (
        ModelBoundaryCapturedOutputFixture,
        ModelBoundaryCapturedOutputFixtureError,
        create_model_boundary_case_from_captured_output_fixture,
        create_model_boundary_captured_output_fixture,
    )

    assert issubclass(ModelBoundaryCapturedOutputFixtureError, ModelBoundaryEvaluationError)
    assert ModelBoundaryCapturedOutputFixture is not None
    assert callable(create_model_boundary_captured_output_fixture)
    assert callable(create_model_boundary_case_from_captured_output_fixture)


# ---------------------------------------------------------------------------
# ModelBoundaryCapturedOutputFixtureError
# ---------------------------------------------------------------------------

def test_captured_output_fixture_error_subclasses_model_boundary_evaluation_error() -> None:
    """ModelBoundaryCapturedOutputFixtureError subclasses ModelBoundaryEvaluationError."""
    assert issubclass(ModelBoundaryCapturedOutputFixtureError, ModelBoundaryEvaluationError)
    assert issubclass(ModelBoundaryCapturedOutputFixtureError, ValueError)


# ---------------------------------------------------------------------------
# ModelBoundaryCapturedOutputFixture
# ---------------------------------------------------------------------------

def test_captured_output_fixture_is_frozen() -> None:
    """ModelBoundaryCapturedOutputFixture instances are immutable."""
    fixture = _make_fixture()
    with pytest.raises(FrozenInstanceError):
        fixture.fixture_ref = "other"  # type: ignore[misc]


def test_captured_output_fixture_deep_copies_and_freezes_candidate_output() -> None:
    """Candidate output is deep-copied and frozen."""
    mutable_output: dict[str, Any] = {"items": ["a", "b"]}
    fixture = _make_fixture(candidate_output=mutable_output)

    assert isinstance(fixture.candidate_output, MappingProxyType)
    mutable_output["items"].append("c")
    assert list(fixture.candidate_output["items"]) == ["a", "b"]


def test_captured_output_fixture_deep_copies_and_freezes_metadata() -> None:
    """Metadata is deep-copied and frozen."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    fixture = _make_fixture(metadata=mutable_meta)

    assert isinstance(fixture.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(fixture.metadata["tags"]) == ["a", "b"]


def test_captured_output_fixture_normalizes_evaluator_notes_to_tuple() -> None:
    """Evaluator notes are normalized to a tuple of strings."""
    fixture = _make_fixture(evaluator_notes=["note-a", "note-b"])
    assert fixture.evaluator_notes == ("note-a", "note-b")


def test_captured_output_fixture_accepts_non_empty_raw_captured_text() -> None:
    """Non-empty raw captured text is accepted as inert evidence."""
    fixture = _make_fixture(raw_captured_text="  captured model text  ")
    assert fixture.raw_captured_text == "  captured model text  "


def test_captured_output_fixture_rejects_blank_raw_captured_text() -> None:
    """Blank or whitespace-only raw captured text is rejected."""
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        _make_fixture(raw_captured_text="")
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        _make_fixture(raw_captured_text="   ")


def test_captured_output_fixture_accepts_none_raw_captured_text() -> None:
    """None raw captured text is accepted."""
    fixture = _make_fixture(raw_captured_text=None)
    assert fixture.raw_captured_text is None


def test_captured_output_fixture_rejects_empty_fixture_ref() -> None:
    """Empty fixture_ref is rejected."""
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        _make_fixture(fixture_ref="")


def test_captured_output_fixture_rejects_empty_capture_ref() -> None:
    """Empty capture_ref is rejected."""
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        _make_fixture(capture_ref="")


def test_captured_output_fixture_rejects_empty_candidate_model_ref() -> None:
    """Empty candidate_model_ref is rejected."""
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        _make_fixture(candidate_model_ref="")


def test_captured_output_fixture_rejects_unknown_output_family() -> None:
    """Unknown expected_output_family is rejected."""
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        _make_fixture(expected_output_family="not_a_family")


def test_captured_output_fixture_rejects_non_context_packet_compiler_result() -> None:
    """Non-ContextPacketCompilerResult packet_result is rejected."""
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        create_model_boundary_captured_output_fixture(
            fixture_ref="fixture-1",
            capture_ref="capture-1",
            candidate_model_ref="model-1",
            expected_output_family="narration_display",
            packet_result="not-a-result",  # type: ignore[arg-type]
            candidate_output={"display": "text"},
        )


def test_captured_output_fixture_rejects_non_mapping_candidate_output() -> None:
    """Non-mapping candidate_output is rejected."""
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        create_model_boundary_captured_output_fixture(
            fixture_ref="fixture-1",
            capture_ref="capture-1",
            candidate_model_ref="model-1",
            expected_output_family="narration_display",
            packet_result=_make_packet_result(),
            candidate_output=["not", "a", "mapping"],  # type: ignore[arg-type]
        )


def test_captured_output_fixture_rejects_callable_candidate_output_values() -> None:
    """Callable values in candidate_output are rejected."""
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        create_model_boundary_captured_output_fixture(
            fixture_ref="fixture-1",
            capture_ref="capture-1",
            candidate_model_ref="model-1",
            expected_output_family="narration_display",
            packet_result=_make_packet_result(),
            candidate_output={"display": lambda: "text"},  # type: ignore[dict-item]
        )


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def test_factory_creates_valid_fixture() -> None:
    """Factory creates a valid, fully-populated fixture."""
    packet_result = _make_packet_result()
    fixture = create_model_boundary_captured_output_fixture(
        fixture_ref="fixture-1",
        capture_ref="capture-1",
        candidate_model_ref="model-1",
        expected_output_family="narration_display",
        packet_result=packet_result,
        candidate_output={"display": "The knight moves forward."},
        raw_captured_text="raw text",
        evaluator_notes=["note-1"],
        metadata={"source": "manual"},
    )

    assert fixture.fixture_ref == "fixture-1"
    assert fixture.capture_ref == "capture-1"
    assert fixture.candidate_model_ref == "model-1"
    assert fixture.expected_output_family == "narration_display"
    assert fixture.packet_result is packet_result
    assert fixture.candidate_output == {"display": "The knight moves forward."}
    assert fixture.raw_captured_text == "raw text"
    assert fixture.evaluator_notes == ("note-1",)
    assert dict(fixture.metadata) == {"source": "manual"}


def test_factory_uses_empty_metadata_when_none_supplied() -> None:
    """Factory uses empty mapping when metadata is None."""
    fixture = create_model_boundary_captured_output_fixture(
        fixture_ref="fixture-1",
        capture_ref="capture-1",
        candidate_model_ref="model-1",
        expected_output_family="narration_display",
        packet_result=_make_packet_result(),
        candidate_output={"display": "text"},
        metadata=None,
    )
    assert fixture.metadata == MappingProxyType({})


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

def test_adapter_rejects_non_fixture_input() -> None:
    """Adapter rejects input that is not a ModelBoundaryCapturedOutputFixture."""
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        create_model_boundary_case_from_captured_output_fixture("not-a-fixture")  # type: ignore[arg-type]


def test_adapter_creates_case_with_default_case_ref() -> None:
    """Adapter creates a case defaulting case_ref to fixture.fixture_ref."""
    fixture = _make_fixture(fixture_ref="fixture-1")
    case = create_model_boundary_case_from_captured_output_fixture(fixture)

    assert isinstance(case, ModelBoundaryEvaluationCase)
    assert case.case_ref == "fixture-1"


def test_adapter_accepts_explicit_case_ref() -> None:
    """Adapter accepts an explicit case_ref override."""
    fixture = _make_fixture(fixture_ref="fixture-1")
    case = create_model_boundary_case_from_captured_output_fixture(
        fixture, case_ref="explicit-case"
    )

    assert case.case_ref == "explicit-case"


def test_adapter_rejects_blank_explicit_case_ref() -> None:
    """Adapter rejects a blank explicit case_ref."""
    fixture = _make_fixture()
    with pytest.raises(ModelBoundaryCapturedOutputFixtureError):
        create_model_boundary_case_from_captured_output_fixture(
            fixture, case_ref=""
        )


def test_adapter_preserves_candidate_model_ref() -> None:
    """Adapter preserves candidate_model_ref from the fixture."""
    fixture = _make_fixture(candidate_model_ref="model-alpha")
    case = create_model_boundary_case_from_captured_output_fixture(fixture)
    assert case.candidate_model_ref == "model-alpha"


def test_adapter_preserves_expected_output_family() -> None:
    """Adapter preserves expected_output_family from the fixture."""
    family = "visible_summary"
    fixture = _make_fixture(expected_output_family=family)
    case = create_model_boundary_case_from_captured_output_fixture(fixture)
    assert case.expected_output_family == family


def test_adapter_preserves_packet_result_identity() -> None:
    """Adapter passes through the packet_result object identity."""
    packet_result = _make_packet_result()
    fixture = _make_fixture(packet_result=packet_result)
    case = create_model_boundary_case_from_captured_output_fixture(fixture)
    assert case.packet_result is packet_result


def test_adapter_preserves_candidate_output_values_without_sharing_mutability() -> None:
    """Adapter candidate output is frozen and isolated from external mutation."""
    fixture = _make_fixture(candidate_output={"display": "original"})
    case = create_model_boundary_case_from_captured_output_fixture(fixture)

    assert case.candidate_output == {"display": "original"}
    assert isinstance(case.candidate_output, MappingProxyType)


def test_adapter_preserves_evaluator_notes() -> None:
    """Adapter preserves evaluator notes from the fixture."""
    fixture = _make_fixture(evaluator_notes=["note-a", "note-b"])
    case = create_model_boundary_case_from_captured_output_fixture(fixture)
    assert case.evaluator_notes == ("note-a", "note-b")


def test_adapter_metadata_includes_fixture_ref_capture_ref_and_has_raw_text() -> None:
    """Default case metadata carries fixture identity and raw-text presence flag."""
    fixture = _make_fixture(
        fixture_ref="fixture-1",
        capture_ref="capture-1",
        raw_captured_text="raw text",
    )
    case = create_model_boundary_case_from_captured_output_fixture(fixture)

    assert case.metadata["fixture_ref"] == "fixture-1"
    assert case.metadata["capture_ref"] == "capture-1"
    assert case.metadata["has_raw_captured_text"] is True


def test_adapter_metadata_has_raw_text_false_when_no_raw_text() -> None:
    """has_raw_captured_text is False when fixture has no raw captured text."""
    fixture = _make_fixture(raw_captured_text=None)
    case = create_model_boundary_case_from_captured_output_fixture(fixture)
    assert case.metadata["has_raw_captured_text"] is False


def test_adapter_uses_supplied_metadata_override() -> None:
    """Adapter uses caller-supplied metadata instead of fixture metadata."""
    fixture = _make_fixture(metadata={"source": "manual"})
    case = create_model_boundary_case_from_captured_output_fixture(
        fixture, metadata={"override": True}
    )

    assert dict(case.metadata) == {"override": True}
    assert "fixture_ref" not in case.metadata


def test_adapter_does_not_include_raw_captured_text_in_case_metadata() -> None:
    """Raw captured text is never copied into case metadata."""
    fixture = _make_fixture(raw_captured_text="sensitive raw text")
    case = create_model_boundary_case_from_captured_output_fixture(fixture)

    for value in case.metadata.values():
        assert value != "sensitive raw text"
    assert "raw_captured_text" not in case.metadata


def test_adapter_does_not_evaluate_the_case() -> None:
    """Adapter does not evaluate the case; result fields are not populated."""
    fixture = _make_fixture()
    case = create_model_boundary_case_from_captured_output_fixture(fixture)

    assert not hasattr(case, "status")
    assert not hasattr(case, "passed")
    assert not hasattr(case, "violation_codes")


# ---------------------------------------------------------------------------
# Source scan
# ---------------------------------------------------------------------------

_FORBIDDEN_PATTERNS = (
    "roll_dice",
    "commit_event(",
    "apply_delta(",
    "mutate_state",
    "persist_state",
    "replay_event",
    "state_store.get",
    "event_ledger.get",
    "generate_narration",
    "call_model",
    "invoke_model",
    "openai",
    "anthropic",
    "json.loads",
    "ast.literal_eval",
    "re.search",
    "re.match",
)


def test_module_source_does_not_import_or_call_forbidden_systems() -> None:
    """Module source contains no forbidden runtime/model/prose-parsing imports or calls."""
    import pathlib

    source = pathlib.Path("src/astra_runtime/domain/model_boundary_evaluation.py").read_text()
    for pattern in _FORBIDDEN_PATTERNS:
        assert pattern not in source, f"forbidden pattern found: {pattern!r}"
