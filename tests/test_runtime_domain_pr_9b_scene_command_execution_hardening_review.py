"""PR-9B — scene command execution skeleton hardening review tests.

RUNTIME-DOMAIN-PR-9B: review/hardening only. No new runtime behavior.
Validates, audits, and tightens the PR-9A skeleton.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
from pathlib import Path

import pytest

from astra_runtime.domain.scene_command_execution_skeleton import (
    SceneCommandExecutionAssemblyAuthorityFlags,
    SceneCommandExecutionAssemblyResult,
    SceneCommandExecutionHiddenInfoContract,
    SceneCommandExecutionNarrationPacketRef,
    SceneCommandExecutionModelBoundaryFixtureRef,
    SceneCommandExecutionSceneContract,
    SceneCommandExecutionSkeletonError,
    InvalidSceneCommandExecutionAssemblyResultError,
    assemble_scene_command_execution_result,
    create_scene_command_execution_actor_contract,
    create_scene_command_execution_assembly_authority_flags,
    create_scene_command_execution_assembly_request,
    create_scene_command_execution_context_packet_ref,
    create_scene_command_execution_event_ledger_candidate_ref,
    create_scene_command_execution_hidden_info_contract,
    create_scene_command_execution_model_boundary_fixture_ref,
    create_scene_command_execution_narration_packet_ref,
    create_scene_command_execution_object_contract,
    create_scene_command_execution_resource_preview_ref,
    create_scene_command_execution_scene_contract,
    create_scene_command_execution_state_delta_candidate_ref,
    create_scene_command_execution_validation_ref,
    serialize_scene_command_execution_assembly_result_backend,
    serialize_scene_command_execution_assembly_result_visible,
    validate_scene_command_execution_assembly_result,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.persistence_boundary import (
    PersistenceBoundaryRequest,
    create_persistence_boundary_request,
)
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.transaction_preview import create_transaction_preview


REPO_ROOT = Path(__file__).resolve().parent.parent
SKELETON_PATH = REPO_ROOT / "src" / "astra_runtime" / "domain" / "scene_command_execution_skeleton.py"
REVIEW_ARTIFACT_PATH = REPO_ROOT / "docs" / "doctrine" / "reviews" / "runtime_domain_pr_9b_scene_command_execution_hardening_review.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _skeleton_source() -> str:
    return SKELETON_PATH.read_text(encoding="utf-8")


def _build_sample_result(
    *,
    persistence_prepare_ref: PersistenceBoundaryRequest | None = None,
) -> SceneCommandExecutionAssemblyResult:
    cmd_id = build_record_id("command", "harden_1")
    envelope = create_command_envelope(
        command_id=cmd_id,
        command_type="inspect_object",
        source_actor_id=build_record_id("actor", "ascendant_1"),
        payload={"target": build_record_id("object", "lever_1")},
    )
    scene = create_scene_command_execution_scene_contract(
        scene_ref=build_record_id("scene", "chamber_1"),
        scene_label="Test Chamber",
        visible_description="A test chamber.",
        hidden_info=[
            create_scene_command_execution_hidden_info_contract(
                hidden_ref=build_record_id("hidden", "secret_1"),
                hidden_label="Secret Fact",
                backend_only_description="This is backend-only secret content.",
                reveal_condition="never_revealed_in_visible",
            ),
        ],
    )
    request = create_scene_command_execution_assembly_request(
        request_ref=build_record_id("request", "harden_1"),
        scene_contract=scene,
        command_envelope=envelope,
        intent_target_ref=build_record_id("object", "lever_1"),
    )
    preview = create_transaction_preview(
        preview_id=build_record_id("transaction_preview", "harden_1"),
        command=envelope,
        status="preview_created",
    )
    return assemble_scene_command_execution_result(
        result_ref=build_record_id("assembly_result", "harden_1"),
        request=request,
        transaction_preview=preview,
        validation_ref=create_scene_command_execution_validation_ref(
            validation_ref=build_record_id("validation", "harden_1"),
        ),
        resource_preview_ref=create_scene_command_execution_resource_preview_ref(
            preview_ref=build_record_id("resource_preview", "harden_1"),
        ),
        state_delta_candidate_ref=create_scene_command_execution_state_delta_candidate_ref(
            delta_ref=build_record_id("state_delta", "harden_1"),
        ),
        event_ledger_candidate_ref=create_scene_command_execution_event_ledger_candidate_ref(
            event_ref=build_record_id("event", "harden_1"),
        ),
        context_packet_ref=create_scene_command_execution_context_packet_ref(
            packet_ref=build_record_id("context_packet", "harden_1"),
        ),
        narration_packet_ref=create_scene_command_execution_narration_packet_ref(
            packet_ref=build_record_id("narration_packet", "harden_1"),
            visible_summary="",
            backend_only_ref_ids=[build_record_id("hidden", "secret_1")],
        ),
        model_boundary_fixture_ref=create_scene_command_execution_model_boundary_fixture_ref(
            fixture_ref=build_record_id("model_boundary_fixture", "harden_1"),
        ),
        persistence_prepare_ref=persistence_prepare_ref,
    )


# ---------------------------------------------------------------------------
# 1. PR-9B is review/hardening only
# ---------------------------------------------------------------------------


class TestPR9BReviewHardeningOnly:
    def test_review_artifact_exists(self):
        assert REVIEW_ARTIFACT_PATH.exists()

    def test_review_artifact_contains_no_new_runtime_behavior(self):
        text = REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")
        assert "no new runtime behavior" in text.lower()

    def test_review_artifact_references_pr_9a(self):
        text = REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")
        assert "PR-9A" in text
        assert "PR-9B" in text

    def test_no_new_domain_module_added(self):
        domain_dir = REPO_ROOT / "src" / "astra_runtime" / "domain"
        expected_modules = {
            "__init__.py",
            "action_legality.py",
            "command_lifecycle.py",
            "context_packet_compiler.py",
            "event_commitment.py",
            "model_boundary_evaluation.py",
            "resource_consequence_math.py",
            "scene_command_execution_skeleton.py",
            "command_kind_routing_skeleton.py",
            "state_projection.py",
            "state_store.py",
            "tiny_vertical_slice.py",
            "transaction_lifecycle.py",
            "validation_integration.py",
        }
        actual = {p.name for p in domain_dir.iterdir() if p.is_file()}
        assert actual == expected_modules


# ---------------------------------------------------------------------------
# 2. No runtime side effects
# ---------------------------------------------------------------------------


class TestNoRuntimeSideEffects:
    def test_skeleton_module_has_no_side_effect_imports(self):
        source = _skeleton_source()
        forbidden_modules = [
            "socket", "http", "urllib", "requests", "aiohttp",
            "sqlite3", "psycopg", "pymongo", "sqlalchemy",
            "random", "secrets",
        ]
        tree = ast.parse(source)
        imported_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_names.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_names.add(node.module.split(".")[0])
        for mod in forbidden_modules:
            assert mod not in imported_names, f"side-effect module '{mod}' imported"

    def test_skeleton_module_has_no_file_write_calls(self):
        source = _skeleton_source()
        assert "open(" not in source or "open(" in source.split("def ")[0]
        assert ".write(" not in source
        assert ".writelines(" not in source

    def test_skeleton_module_has_no_network_calls(self):
        source = _skeleton_source()
        for term in ["requests.get", "requests.post", "urlopen", "http.client"]:
            assert term not in source

    def test_assembly_function_returns_immutable_result(self):
        result = _build_sample_result()
        with pytest.raises(AttributeError):
            result.result_ref = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 3. No hidden-info backend-only description in visible serialization
# ---------------------------------------------------------------------------


class TestHiddenInfoNotInVisibleSerialization:
    def test_visible_serialization_excludes_backend_only_description(self):
        result = _build_sample_result()
        visible = serialize_scene_command_execution_assembly_result_visible(result)
        visible_str = json.dumps(visible, sort_keys=True)
        assert "backend_only_description" not in visible_str
        assert "backend-only secret content" not in visible_str

    def test_visible_serialization_excludes_backend_only_ref_ids(self):
        result = _build_sample_result()
        visible = serialize_scene_command_execution_assembly_result_visible(result)
        visible_str = json.dumps(visible, sort_keys=True)
        assert "backend_only_ref_ids" not in visible_str

    def test_visible_serialization_excludes_hidden_ref(self):
        result = _build_sample_result()
        visible = serialize_scene_command_execution_assembly_result_visible(result)
        visible_str = json.dumps(visible, sort_keys=True)
        assert "hidden:secret_1" not in visible_str

    def test_backend_serialization_includes_narration_backend_refs(self):
        result = _build_sample_result()
        backend = serialize_scene_command_execution_assembly_result_backend(result)
        narration = backend["narration_packet_ref"]
        assert "backend_only_ref_ids" in narration
        assert len(narration["backend_only_ref_ids"]) > 0


# ---------------------------------------------------------------------------
# 4. PersistenceBoundaryRequest is prepare-only reference surface
# ---------------------------------------------------------------------------


class TestPersistenceBoundaryPrepareOnly:
    def test_persistence_prepare_ref_is_optional(self):
        result = _build_sample_result(persistence_prepare_ref=None)
        assert result.persistence_prepare_ref is None
        assert validate_scene_command_execution_assembly_result(result)

    def test_persistence_prepare_ref_accepted_with_prepare_operation(self):
        prepare_ref = create_persistence_boundary_request(
            request_id=build_record_id("persistence_prepare", "harden_1"),
            operation_type="record_snapshot_prepare",
            subject_ref=build_record_id("assembly_result", "harden_1"),
        )
        result = _build_sample_result(persistence_prepare_ref=prepare_ref)
        assert result.persistence_prepare_ref is not None
        assert isinstance(result.persistence_prepare_ref, PersistenceBoundaryRequest)

    def test_authority_flag_persistence_writes_is_false(self):
        result = _build_sample_result()
        assert result.authority_flags.persistence_writes is False

    def test_visible_serialization_excludes_persistence_prepare_ref(self):
        prepare_ref = create_persistence_boundary_request(
            request_id=build_record_id("persistence_prepare", "harden_1"),
            operation_type="record_snapshot_prepare",
            subject_ref=build_record_id("assembly_result", "harden_1"),
        )
        result = _build_sample_result(persistence_prepare_ref=prepare_ref)
        visible = serialize_scene_command_execution_assembly_result_visible(result)
        assert "persistence_prepare_ref" not in visible


# ---------------------------------------------------------------------------
# 5. Authority flags all false and cannot be set true
# ---------------------------------------------------------------------------


class TestAuthorityFlagsAllFalseCannotBeTrue:
    _ALL_FLAG_NAMES = [
        "implementation_beyond_skeleton",
        "live_play_authority",
        "model_authority",
        "prompt_rendering",
        "prose_parsing",
        "narration_generation",
        "persistence_writes",
        "rng_table_oracle_execution",
        "state_mutation",
        "event_append",
        "settlement_authorization",
        "pr5_arithmetic_execution",
        "consequence_application",
        "conversion",
        "sourcebook_inclusion",
        "canon_promotion",
    ]

    def test_all_flags_default_false(self):
        flags = create_scene_command_execution_assembly_authority_flags()
        for name in self._ALL_FLAG_NAMES:
            assert getattr(flags, name) is False, f"{name} not False"

    @pytest.mark.parametrize("flag_name", _ALL_FLAG_NAMES)
    def test_each_flag_rejects_true(self, flag_name):
        with pytest.raises(
            InvalidSceneCommandExecutionAssemblyResultError, match=flag_name
        ):
            SceneCommandExecutionAssemblyAuthorityFlags(**{flag_name: True})

    def test_flags_frozen(self):
        flags = create_scene_command_execution_assembly_authority_flags()
        with pytest.raises(AttributeError):
            flags.live_play_authority = True  # type: ignore[misc]

    def test_flags_serialization_all_false(self):
        flags = create_scene_command_execution_assembly_authority_flags()
        d = flags.to_dict()
        for name in self._ALL_FLAG_NAMES:
            assert d[name] is False

    def test_assembly_result_carries_all_false_flags(self):
        result = _build_sample_result()
        for name in self._ALL_FLAG_NAMES:
            assert getattr(result.authority_flags, name) is False


# ---------------------------------------------------------------------------
# 6. No forbidden terms as enabled behavior in skeleton source
# ---------------------------------------------------------------------------


class TestNoForbiddenEnabledBehavior:
    def test_no_model_call_imports(self):
        source = _skeleton_source().lower()
        for term in ["openai", "anthropic", "llm", "langchain"]:
            assert term not in source, f"model term '{term}' found in skeleton source"

    def test_no_prompt_template_patterns(self):
        source = _skeleton_source().lower()
        for term in ["prompt template", "render_prompt", "prompt_template", "f-string prompt"]:
            assert term not in source

    def test_no_live_play_patterns(self):
        source = _skeleton_source()
        for term in ["session_loop", "game_loop", "real_time", "LivePlayAdapter"]:
            assert term not in source
        assert "live_play_authority" in source, "authority flag should exist"
        lines_with_live_play = [
            line.strip() for line in source.splitlines()
            if "live_play" in line and "live_play_authority" not in line
        ]
        assert not lines_with_live_play, f"unexpected live_play usage: {lines_with_live_play}"

    def test_no_persistence_write_patterns(self):
        source = _skeleton_source()
        for term in ["db.commit", "db.execute", "cursor.execute", "session.commit"]:
            assert term not in source

    def test_no_rng_patterns(self):
        source = _skeleton_source()
        for term in ["random.randint", "random.choice", "dice_roll", "roll_dice"]:
            assert term not in source

    def test_no_state_mutation_patterns(self):
        source = _skeleton_source()
        for term in ["mutate_state", "apply_delta", "commit_event", "append_event"]:
            assert term not in source

    def test_no_settlement_patterns(self):
        source = _skeleton_source()
        for term in ["settle(", "authorize_settlement", "execute_settlement"]:
            assert term not in source

    def test_no_conversion_or_canon_patterns(self):
        source = _skeleton_source()
        for term in ["promote_canon", "import_sourcebook", "convert_donor"]:
            assert term not in source


# ---------------------------------------------------------------------------
# 7. Guardrail allowlist updates remain narrow
# ---------------------------------------------------------------------------


class TestGuardrailAllowlistNarrow:
    def test_pr5c_allowlist_is_narrow(self):
        path = REPO_ROOT / "tests" / "test_runtime_domain_pr_5c_resource_consequence_math_planning_hardening_review.py"
        source = path.read_text(encoding="utf-8")
        matches = re.findall(r'"(src/astra_runtime/domain/[^"/]+\.py)"', source)
        allowed_domain_paths = set(matches)
        for p in allowed_domain_paths:
            assert p in {
                "src/astra_runtime/domain/resource_consequence_math.py",
                "src/astra_runtime/domain/scene_command_execution_skeleton.py",
                "src/astra_runtime/domain/command_kind_routing_skeleton.py",
            }, f"unexpected domain path in PR-5c allowlist: {p}"

    def test_pr5g_domain_dir_allowlist_does_not_include_unexpected_files(self):
        path = REPO_ROOT / "tests" / "test_runtime_domain_pr_5g_resource_consequence_math_residual_planning_hardening_review.py"
        source = path.read_text(encoding="utf-8")
        expected_domain_files = {
            "__init__.py", "action_legality.py", "command_lifecycle.py",
            "event_commitment.py", "resource_consequence_math.py",
            "context_packet_compiler.py", "model_boundary_evaluation.py",
            "tiny_vertical_slice.py", "scene_command_execution_skeleton.py",
            "command_kind_routing_skeleton.py",
            "state_projection.py", "state_store.py", "transaction_lifecycle.py",
            "validation_integration.py",
        }
        domain_dir = REPO_ROOT / "src" / "astra_runtime" / "domain"
        actual_files = {p.name for p in domain_dir.iterdir() if p.is_file()}
        assert actual_files == expected_domain_files


# ---------------------------------------------------------------------------
# 8. tiny_vertical_slice.py not modified
# ---------------------------------------------------------------------------


class TestTinyVerticalSliceNotModified:
    def test_tiny_vertical_slice_exists(self):
        path = REPO_ROOT / "src" / "astra_runtime" / "domain" / "tiny_vertical_slice.py"
        assert path.exists()

    def test_tiny_vertical_slice_not_in_branch_diff(self):
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True, text=True, check=True,
        )
        assert "src/astra_runtime/domain/tiny_vertical_slice.py" not in result.stdout


# ---------------------------------------------------------------------------
# 9. Existing PR-9A tests still pass (structural smoke check)
# ---------------------------------------------------------------------------


class TestPR9AStructuralSmoke:
    def test_pr9a_test_file_exists(self):
        path = REPO_ROOT / "tests" / "test_runtime_domain_pr_9a_scene_command_execution_skeleton.py"
        assert path.exists()

    def test_skeleton_module_exists(self):
        assert SKELETON_PATH.exists()

    def test_skeleton_module_imports_successfully(self):
        import astra_runtime.domain.scene_command_execution_skeleton as mod
        assert hasattr(mod, "assemble_scene_command_execution_result")
        assert hasattr(mod, "SceneCommandExecutionAssemblyResult")
        assert hasattr(mod, "SceneCommandExecutionAssemblyAuthorityFlags")

    def test_assembly_result_validates(self):
        result = _build_sample_result()
        assert validate_scene_command_execution_assembly_result(result)


# ---------------------------------------------------------------------------
# 10. Full runtime tests structural check
# ---------------------------------------------------------------------------


class TestRuntimeStructuralCheck:
    def test_runtime_test_directory_exists(self):
        assert (REPO_ROOT / "tests" / "runtime").is_dir()

    def test_no_live_play_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "live_play").exists()

    def test_no_ui_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "ui").exists()

    def test_no_database_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "database").exists()

    def test_no_prompt_templates_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "prompts").exists()


# ---------------------------------------------------------------------------
# Additional hardening: serialization completeness
# ---------------------------------------------------------------------------


class TestSerializationCompleteness:
    def test_visible_serialization_is_json_serializable(self):
        result = _build_sample_result()
        visible = serialize_scene_command_execution_assembly_result_visible(result)
        serialized = json.dumps(visible, sort_keys=True)
        roundtrip = json.loads(serialized)
        assert roundtrip == visible

    def test_backend_serialization_is_json_serializable(self):
        result = _build_sample_result()
        backend = serialize_scene_command_execution_assembly_result_backend(result)
        serialized = json.dumps(backend, sort_keys=True)
        roundtrip = json.loads(serialized)
        assert roundtrip == backend

    def test_visible_serialization_has_required_keys(self):
        result = _build_sample_result()
        visible = serialize_scene_command_execution_assembly_result_visible(result)
        required_keys = {
            "result_ref", "request_ref", "command_intent",
            "transaction_preview", "validation_ref", "resource_preview_ref",
            "state_delta_candidate_ref", "event_ledger_candidate_ref",
            "context_packet_ref", "narration_packet_ref",
            "model_boundary_fixture_ref", "authority_flags",
        }
        assert set(visible.keys()) == required_keys

    def test_backend_serialization_includes_all_surfaces(self):
        result = _build_sample_result(
            persistence_prepare_ref=create_persistence_boundary_request(
                request_id=build_record_id("persistence_prepare", "harden_1"),
                operation_type="record_snapshot_prepare",
                subject_ref=build_record_id("assembly_result", "harden_1"),
            ),
        )
        backend = serialize_scene_command_execution_assembly_result_backend(result)
        assert "persistence_prepare_ref" in backend
        assert backend["persistence_prepare_ref"] is not None
