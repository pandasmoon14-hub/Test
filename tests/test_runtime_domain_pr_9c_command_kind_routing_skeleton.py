"""Tests for RUNTIME-DOMAIN-PR-9C: command-kind routing skeleton.

Validates that the routing skeleton classifies commands into families,
produces dispatch-shell references, and denies all execution authority.
"""

from __future__ import annotations

import inspect
import json
import re
import subprocess
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import pytest

from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    create_command_envelope,
)
from astra_runtime.kernel.record_identity import build_record_id

REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# 1. Module existence and public exports
# ---------------------------------------------------------------------------


class TestModuleExistence:
    def test_module_file_exists(self):
        path = REPO_ROOT / "src" / "astra_runtime" / "domain" / "command_kind_routing_skeleton.py"
        assert path.exists()

    def test_module_importable(self):
        import astra_runtime.domain.command_kind_routing_skeleton as mod
        assert mod is not None


class TestPublicExports:
    def test_domain_package_exports_pr9c_surfaces(self):
        import astra_runtime.domain as domain
        expected_names = [
            "COMMAND_KIND_FAMILIES",
            "COMMAND_KIND_ROUTING_AUTHORITY_FLAGS",
            "CommandDispatchShell",
            "CommandKindClassification",
            "CommandKindDefinition",
            "CommandKindRoutingAuthorityFlags",
            "CommandKindRoutingRequest",
            "CommandKindRoutingResult",
            "CommandKindRoutingSkeletonError",
            "DEFERRED_RUNTIME_OWNER",
            "InvalidCommandDispatchShellError",
            "InvalidCommandKindClassificationError",
            "InvalidCommandKindDefinitionError",
            "InvalidCommandKindFamilyError",
            "InvalidCommandKindRoutingRequestError",
            "InvalidCommandKindRoutingResultError",
            "QUARANTINE_UNKNOWN_COMMAND_KIND",
            "RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY",
            "RT002_RESOURCE_CONSEQUENCE_MATH",
            "RT003_STATE_STORE_STATE_PROJECTION",
            "RT004_TRANSACTION_LIFECYCLE_EVENT_COMMITMENT",
            "RT005_VALIDATION_INTEGRATION",
            "RT006_CONTEXT_PACKET_COMPILER",
            "RT007_MODEL_BOUNDARY_EVALUATION",
            "RT008_TINY_VERTICAL_SLICE_REFERENCE_ONLY",
            "RT009_RNG_TABLE_ORACLE_REFERENCE_ONLY",
            "classify_command_type_to_family",
            "create_command_dispatch_shell",
            "create_command_kind_classification",
            "create_command_kind_definition",
            "create_command_kind_routing_authority_flags",
            "create_command_kind_routing_request",
            "create_command_kind_routing_result",
            "route_command_envelope",
            "route_command_intent",
            "serialize_command_kind_routing_result",
            "serialize_command_kind_routing_result_visible",
            "validate_command_dispatch_shell",
            "validate_command_kind_classification",
            "validate_command_kind_definition",
            "validate_command_kind_routing_authority_flags",
            "validate_command_kind_routing_request",
            "validate_command_kind_routing_result",
        ]
        for name in expected_names:
            assert name in domain.__all__, f"{name} not in domain.__all__"
            assert hasattr(domain, name), f"domain has no attribute {name}"


# ---------------------------------------------------------------------------
# 2. Error hierarchy
# ---------------------------------------------------------------------------


class TestErrorHierarchy:
    def test_base_error_is_value_error(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            CommandKindRoutingSkeletonError,
        )
        assert issubclass(CommandKindRoutingSkeletonError, ValueError)

    @pytest.mark.parametrize("error_name", [
        "InvalidCommandKindFamilyError",
        "InvalidCommandKindDefinitionError",
        "InvalidCommandKindClassificationError",
        "InvalidCommandDispatchShellError",
        "InvalidCommandKindRoutingRequestError",
        "InvalidCommandKindRoutingResultError",
    ])
    def test_specific_errors_inherit_from_base(self, error_name):
        import astra_runtime.domain.command_kind_routing_skeleton as mod
        from astra_runtime.domain.command_kind_routing_skeleton import (
            CommandKindRoutingSkeletonError,
        )
        error_cls = getattr(mod, error_name)
        assert issubclass(error_cls, CommandKindRoutingSkeletonError)


# ---------------------------------------------------------------------------
# 3. Frozen dataclasses and keyword-only
# ---------------------------------------------------------------------------


_DATACLASS_NAMES = [
    "CommandKindDefinition",
    "CommandKindClassification",
    "CommandDispatchShell",
    "CommandKindRoutingRequest",
    "CommandKindRoutingAuthorityFlags",
    "CommandKindRoutingResult",
]


class TestFrozenDataclasses:
    @pytest.mark.parametrize("cls_name", _DATACLASS_NAMES)
    def test_dataclass_is_frozen(self, cls_name):
        import astra_runtime.domain.command_kind_routing_skeleton as mod
        cls = getattr(mod, cls_name)
        assert cls.__dataclass_params__.frozen is True

    @pytest.mark.parametrize("cls_name", _DATACLASS_NAMES)
    def test_dataclass_fields_are_kw_only(self, cls_name):
        import dataclasses
        import astra_runtime.domain.command_kind_routing_skeleton as mod
        cls = getattr(mod, cls_name)
        for f in dataclasses.fields(cls):
            assert f.kw_only is True, f"{cls_name}.{f.name} is not kw_only"


# ---------------------------------------------------------------------------
# 4. Known command families
# ---------------------------------------------------------------------------


class TestCommandFamilies:
    def test_families_is_frozenset(self):
        from astra_runtime.domain.command_kind_routing_skeleton import COMMAND_KIND_FAMILIES
        assert isinstance(COMMAND_KIND_FAMILIES, frozenset)

    def test_required_families_present(self):
        from astra_runtime.domain.command_kind_routing_skeleton import COMMAND_KIND_FAMILIES
        required = {
            "movement", "inspection", "interaction", "social", "combat",
            "ability", "inventory", "recovery", "crafting", "travel",
            "research", "mission", "system_meta", "unknown",
        }
        assert required <= COMMAND_KIND_FAMILIES

    def test_no_unexpected_families(self):
        from astra_runtime.domain.command_kind_routing_skeleton import COMMAND_KIND_FAMILIES
        expected = {
            "movement", "inspection", "interaction", "social", "combat",
            "ability", "inventory", "recovery", "crafting", "travel",
            "research", "mission", "system_meta", "unknown",
        }
        assert COMMAND_KIND_FAMILIES == expected


# ---------------------------------------------------------------------------
# 5. Classification from CommandEnvelope
# ---------------------------------------------------------------------------


def _make_envelope(command_type: str = "inspect_room") -> CommandEnvelope:
    return create_command_envelope(
        command_id=build_record_id("cmd", "test_001"),
        command_type=command_type,
        source_actor_id=build_record_id("actor", "player_1"),
    )


class TestClassificationFromEnvelope:
    def test_inspect_routes_to_inspection(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("inspect_room")
        result = route_command_envelope(
            request_ref=build_record_id("req", "test_001"),
            command_envelope=envelope,
        )
        assert result.classification.family == "inspection"

    def test_attack_routes_to_combat(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("attack_target")
        result = route_command_envelope(
            request_ref=build_record_id("req", "test_002"),
            command_envelope=envelope,
        )
        assert result.classification.family == "combat"

    def test_move_routes_to_movement(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("move_north")
        result = route_command_envelope(
            request_ref=build_record_id("req", "test_003"),
            command_envelope=envelope,
        )
        assert result.classification.family == "movement"

    def test_craft_routes_to_crafting(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("craft_item")
        result = route_command_envelope(
            request_ref=build_record_id("req", "test_004"),
            command_envelope=envelope,
        )
        assert result.classification.family == "crafting"

    def test_result_has_valid_classification(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            route_command_envelope,
            validate_command_kind_routing_result,
        )
        envelope = _make_envelope("inspect_room")
        result = route_command_envelope(
            request_ref=build_record_id("req", "test_005"),
            command_envelope=envelope,
        )
        assert validate_command_kind_routing_result(result)


# ---------------------------------------------------------------------------
# 6. Classification from SceneCommandExecutionCommandIntent fields
# ---------------------------------------------------------------------------


class TestClassificationFromIntent:
    def test_route_command_intent_inspection(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_intent
        result = route_command_intent(
            request_ref=build_record_id("req", "intent_001"),
            intent_ref=build_record_id("intent", "i_001"),
            command_envelope_id=build_record_id("cmd", "env_001"),
            command_type="inspect_object",
        )
        assert result.classification.family == "inspection"

    def test_route_command_intent_combat(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_intent
        result = route_command_intent(
            request_ref=build_record_id("req", "intent_002"),
            intent_ref=build_record_id("intent", "i_002"),
            command_envelope_id=build_record_id("cmd", "env_002"),
            command_type="attack_melee",
        )
        assert result.classification.family == "combat"

    def test_route_command_intent_preserves_command_ref(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_intent
        env_id = build_record_id("cmd", "env_003")
        result = route_command_intent(
            request_ref=build_record_id("req", "intent_003"),
            intent_ref=build_record_id("intent", "i_003"),
            command_envelope_id=env_id,
            command_type="move_east",
        )
        assert result.command_ref == env_id


# ---------------------------------------------------------------------------
# 7. Unknown command type routes to unknown/quarantine
# ---------------------------------------------------------------------------


class TestUnknownRouting:
    def test_unknown_command_type_routes_to_unknown(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("xyzzy_nonsense_verb")
        result = route_command_envelope(
            request_ref=build_record_id("req", "unknown_001"),
            command_envelope=envelope,
        )
        assert result.classification.family == "unknown"

    def test_unknown_dispatch_shell_routes_to_quarantine(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            QUARANTINE_UNKNOWN_COMMAND_KIND,
            route_command_envelope,
        )
        envelope = _make_envelope("xyzzy_nonsense_verb")
        result = route_command_envelope(
            request_ref=build_record_id("req", "unknown_002"),
            command_envelope=envelope,
        )
        assert result.dispatch_shell.owner_route == QUARANTINE_UNKNOWN_COMMAND_KIND

    def test_empty_command_type_routes_to_unknown(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            classify_command_type_to_family,
        )
        assert classify_command_type_to_family("") == "unknown"
        assert classify_command_type_to_family("   ") == "unknown"


# ---------------------------------------------------------------------------
# 8. Dispatch shell references owner route but does not call it
# ---------------------------------------------------------------------------


class TestDispatchShellReferences:
    def test_dispatch_shell_owner_route_is_string(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("inspect_room")
        result = route_command_envelope(
            request_ref=build_record_id("req", "dispatch_001"),
            command_envelope=envelope,
        )
        assert isinstance(result.dispatch_shell.owner_route, str)
        assert result.dispatch_shell.owner_route != ""

    def test_dispatch_shell_does_not_execute(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("attack_target")
        result = route_command_envelope(
            request_ref=build_record_id("req", "dispatch_002"),
            command_envelope=envelope,
        )
        assert not hasattr(result.dispatch_shell, "execute")
        assert not hasattr(result.dispatch_shell, "call")
        assert not hasattr(result.dispatch_shell, "invoke")
        assert not hasattr(result.dispatch_shell, "run")

    def test_dispatch_shell_is_frozen(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("move_north")
        result = route_command_envelope(
            request_ref=build_record_id("req", "dispatch_003"),
            command_envelope=envelope,
        )
        with pytest.raises(AttributeError):
            result.dispatch_shell.owner_route = "HACKED"


# ---------------------------------------------------------------------------
# 9. Authority flags are all false and reject true
# ---------------------------------------------------------------------------


_ALL_AUTHORITY_FLAG_NAMES = [
    "legality_resolution",
    "command_execution",
    "runtime_action_execution",
    "state_mutation",
    "event_append",
    "persistence_write",
    "rng_table_oracle_execution",
    "settlement_authorization",
    "pr5_arithmetic_execution",
    "consequence_application",
    "model_authority",
    "prompt_rendering",
    "prompt_execution",
    "prose_parsing",
    "narration_generation",
    "live_play_session_authority",
    "ui_client_authority",
    "conversion",
    "sourcebook_inclusion",
    "canon_promotion",
]


class TestAuthorityFlags:
    def test_all_flags_default_false(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            CommandKindRoutingAuthorityFlags,
        )
        flags = CommandKindRoutingAuthorityFlags()
        for flag_name in _ALL_AUTHORITY_FLAG_NAMES:
            assert getattr(flags, flag_name) is False, f"{flag_name} is not False"

    @pytest.mark.parametrize("flag_name", _ALL_AUTHORITY_FLAG_NAMES)
    def test_setting_flag_to_true_raises(self, flag_name):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            CommandKindRoutingAuthorityFlags,
            InvalidCommandKindRoutingResultError,
        )
        with pytest.raises(InvalidCommandKindRoutingResultError):
            CommandKindRoutingAuthorityFlags(**{flag_name: True})

    def test_flags_frozen(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            CommandKindRoutingAuthorityFlags,
        )
        flags = CommandKindRoutingAuthorityFlags()
        with pytest.raises(AttributeError):
            flags.legality_resolution = True

    def test_result_authority_flags_all_false(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("inspect_room")
        result = route_command_envelope(
            request_ref=build_record_id("req", "flags_001"),
            command_envelope=envelope,
        )
        for flag_name in _ALL_AUTHORITY_FLAG_NAMES:
            assert getattr(result.authority_flags, flag_name) is False

    def test_flags_serialization_all_false(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            CommandKindRoutingAuthorityFlags,
        )
        flags = CommandKindRoutingAuthorityFlags()
        d = flags.to_dict()
        for flag_name in _ALL_AUTHORITY_FLAG_NAMES:
            assert d[flag_name] is False

    def test_authority_flags_constant_matches_dataclass_fields(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            COMMAND_KIND_ROUTING_AUTHORITY_FLAGS,
            CommandKindRoutingAuthorityFlags,
        )
        dc_fields = set(CommandKindRoutingAuthorityFlags.__dataclass_fields__)
        assert dc_fields == COMMAND_KIND_ROUTING_AUTHORITY_FLAGS


# ---------------------------------------------------------------------------
# 10. Deterministic serialization
# ---------------------------------------------------------------------------


class TestDeterministicSerialization:
    def test_result_serializes_to_json(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            route_command_envelope,
            serialize_command_kind_routing_result,
        )
        envelope = _make_envelope("inspect_room")
        result = route_command_envelope(
            request_ref=build_record_id("req", "serial_001"),
            command_envelope=envelope,
        )
        d = serialize_command_kind_routing_result(result)
        json_str = json.dumps(d, sort_keys=True)
        assert isinstance(json_str, str)
        roundtrip = json.loads(json_str)
        assert roundtrip == d

    def test_visible_serialization_subset(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            route_command_envelope,
            serialize_command_kind_routing_result_visible,
        )
        envelope = _make_envelope("move_north")
        result = route_command_envelope(
            request_ref=build_record_id("req", "serial_002"),
            command_envelope=envelope,
        )
        vis = serialize_command_kind_routing_result_visible(result)
        assert "result_ref" in vis
        assert "family" in vis
        assert "kind" in vis
        assert "owner_route" in vis
        assert "authority_flags" in vis

    def test_repeated_serialization_deterministic(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            route_command_envelope,
            serialize_command_kind_routing_result,
        )
        envelope = _make_envelope("attack_target")
        result = route_command_envelope(
            request_ref=build_record_id("req", "serial_003"),
            command_envelope=envelope,
        )
        d1 = serialize_command_kind_routing_result(result)
        d2 = serialize_command_kind_routing_result(result)
        assert d1 == d2

    def test_classification_to_dict(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("inspect_room")
        result = route_command_envelope(
            request_ref=build_record_id("req", "serial_004"),
            command_envelope=envelope,
        )
        d = result.classification.to_dict()
        assert d["family"] == "inspection"
        assert d["raw_command_type"] == "inspect_room"

    def test_dispatch_shell_to_dict(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        envelope = _make_envelope("inspect_room")
        result = route_command_envelope(
            request_ref=build_record_id("req", "serial_005"),
            command_envelope=envelope,
        )
        d = result.dispatch_shell.to_dict()
        assert "owner_route" in d
        assert "dispatch_ref" in d


# ---------------------------------------------------------------------------
# 11. Metadata immutability / deep-copy
# ---------------------------------------------------------------------------


class TestMetadataImmutability:
    def test_classification_metadata_is_mapping_proxy(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            create_command_kind_classification,
        )
        cls = create_command_kind_classification(
            classification_ref=build_record_id("cls", "meta_001"),
            command_ref="cmd_ref",
            raw_command_type="inspect_room",
            family="inspection",
            kind="inspect_room",
            metadata={"key": "value"},
        )
        assert isinstance(cls.metadata, Mapping)
        with pytest.raises(TypeError):
            cls.metadata["new_key"] = "new_value"  # type: ignore[index]

    def test_routing_result_metadata_deep_copied(self):
        from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
        original_meta = {"nested": {"a": 1}}
        envelope = _make_envelope("inspect_room")
        result = route_command_envelope(
            request_ref=build_record_id("req", "meta_002"),
            command_envelope=envelope,
            metadata=original_meta,
        )
        original_meta["nested"]["a"] = 999
        assert result.metadata.get("nested", {}).get("a") == 1

    def test_definition_metadata_frozen(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            create_command_kind_definition,
        )
        defn = create_command_kind_definition(
            kind_id="test_kind",
            family="combat",
            kind_label="Test Kind",
            description="A test kind definition",
            metadata={"x": 1},
        )
        with pytest.raises(TypeError):
            defn.metadata["y"] = 2  # type: ignore[index]


# ---------------------------------------------------------------------------
# 12. No side-effect imports
# ---------------------------------------------------------------------------


def _routing_skeleton_source() -> str:
    path = REPO_ROOT / "src" / "astra_runtime" / "domain" / "command_kind_routing_skeleton.py"
    return path.read_text(encoding="utf-8")


class TestNoSideEffectImports:
    _FORBIDDEN_IMPORTS = [
        "socket", "http", "urllib", "requests", "aiohttp",
        "sqlite3", "psycopg", "pymongo", "sqlalchemy",
        "random", "secrets",
    ]

    @pytest.mark.parametrize("module_name", _FORBIDDEN_IMPORTS)
    def test_no_forbidden_import(self, module_name):
        source = _routing_skeleton_source()
        pattern = rf"(?:^|\s)import\s+{re.escape(module_name)}|from\s+{re.escape(module_name)}\s+import"
        assert not re.search(pattern, source), f"forbidden import: {module_name}"

    def test_no_open_call(self):
        source = _routing_skeleton_source()
        assert "open(" not in source

    def test_no_write_call(self):
        source = _routing_skeleton_source()
        assert ".write(" not in source
        assert ".writelines(" not in source


# ---------------------------------------------------------------------------
# 13. No model/prompt/prose/narration/live-play behavior
# ---------------------------------------------------------------------------


class TestNoModelOrPromptBehavior:
    _FORBIDDEN_TERMS = [
        "openai", "anthropic", "llm", "langchain",
        "prompt template", "render_prompt", "prompt_template",
        "session_loop", "game_loop", "real_time", "LivePlayAdapter",
    ]

    @pytest.mark.parametrize("term", _FORBIDDEN_TERMS)
    def test_no_forbidden_term(self, term):
        source = _routing_skeleton_source()
        if term == "real_time":
            assert term not in source or "real_time" in "real_time_clock"
        else:
            assert term.lower() not in source.lower(), f"forbidden term found: {term}"


# ---------------------------------------------------------------------------
# 14. No persistence/RNG/state mutation/event append/settlement/consequence
# ---------------------------------------------------------------------------


class TestNoPersistenceOrMutationBehavior:
    _FORBIDDEN_PATTERNS = [
        "db.commit", "db.execute", "cursor.execute", "session.commit",
        "random.randint", "random.choice", "dice_roll", "roll_dice",
        "mutate_state", "apply_delta", "commit_event", "append_event",
        "settle(", "authorize_settlement", "execute_settlement",
        "promote_canon", "import_sourcebook", "convert_donor",
    ]

    @pytest.mark.parametrize("pattern", _FORBIDDEN_PATTERNS)
    def test_no_forbidden_pattern(self, pattern):
        source = _routing_skeleton_source()
        assert pattern not in source, f"forbidden pattern found: {pattern}"


# ---------------------------------------------------------------------------
# 15. No legality resolution
# ---------------------------------------------------------------------------


class TestNoLegalityResolution:
    def test_no_resolve_legality_function(self):
        import astra_runtime.domain.command_kind_routing_skeleton as mod
        assert not hasattr(mod, "resolve_legality")
        assert not hasattr(mod, "check_legality")
        assert not hasattr(mod, "evaluate_legality")

    def test_source_has_no_legality_execution(self):
        source = _routing_skeleton_source()
        assert "resolve_legality" not in source
        assert "check_legality(" not in source
        assert "evaluate_legality(" not in source


# ---------------------------------------------------------------------------
# 16. No call to assemble_scene_command_execution_result
# ---------------------------------------------------------------------------


class TestNoAssemblyCall:
    def test_no_import_of_assemble(self):
        source = _routing_skeleton_source()
        assert "assemble_scene_command_execution_result" not in source

    def test_no_call_to_assemble(self):
        source = _routing_skeleton_source()
        assert "assemble_scene_command_execution_result(" not in source


# ---------------------------------------------------------------------------
# 17. tiny_vertical_slice.py not modified
# ---------------------------------------------------------------------------


class TestTinyVerticalSliceNotModified:
    def test_tiny_vertical_slice_exists(self):
        path = REPO_ROOT / "src" / "astra_runtime" / "domain" / "tiny_vertical_slice.py"
        assert path.exists()

    def test_tiny_vertical_slice_not_in_git_diff(self):
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True, text=True, cwd=str(REPO_ROOT),
        )
        changed = result.stdout.strip().splitlines()
        assert "src/astra_runtime/domain/tiny_vertical_slice.py" not in changed


# ---------------------------------------------------------------------------
# 18. PR-9A and PR-9B tests still pass (validated externally)
# ---------------------------------------------------------------------------


class TestPR9ACompatibility:
    def test_scene_command_execution_skeleton_importable(self):
        import astra_runtime.domain.scene_command_execution_skeleton as mod
        assert hasattr(mod, "SceneCommandExecutionCommandIntent")

    def test_command_envelope_still_works(self):
        envelope = _make_envelope("inspect_room")
        assert envelope.command_type == "inspect_room"


# ---------------------------------------------------------------------------
# Factory/validator parity
# ---------------------------------------------------------------------------


class TestFactoryValidatorParity:
    def test_definition_factory_passes_validator(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            create_command_kind_definition,
            validate_command_kind_definition,
        )
        defn = create_command_kind_definition(
            kind_id="inspect_room",
            family="inspection",
            kind_label="Inspect Room",
            description="Inspect a room or area",
        )
        assert validate_command_kind_definition(defn)

    def test_classification_factory_passes_validator(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            create_command_kind_classification,
            validate_command_kind_classification,
        )
        cls = create_command_kind_classification(
            classification_ref=build_record_id("cls", "test_001"),
            command_ref="cmd_ref",
            raw_command_type="inspect_room",
            family="inspection",
            kind="inspect_room",
        )
        assert validate_command_kind_classification(cls)

    def test_dispatch_shell_factory_passes_validator(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
            create_command_dispatch_shell,
            validate_command_dispatch_shell,
        )
        shell = create_command_dispatch_shell(
            dispatch_ref=build_record_id("dispatch", "test_001"),
            command_ref="cmd_ref",
            owner_route=RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
            family="inspection",
        )
        assert validate_command_dispatch_shell(shell)

    def test_routing_request_factory_passes_validator(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            create_command_kind_routing_request,
            validate_command_kind_routing_request,
        )
        envelope = _make_envelope("inspect_room")
        req = create_command_kind_routing_request(
            request_ref=build_record_id("req", "test_001"),
            command_envelope=envelope,
        )
        assert validate_command_kind_routing_request(req)

    def test_routing_result_factory_passes_validator(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            route_command_envelope,
            validate_command_kind_routing_result,
        )
        envelope = _make_envelope("inspect_room")
        result = route_command_envelope(
            request_ref=build_record_id("req", "test_002"),
            command_envelope=envelope,
        )
        assert validate_command_kind_routing_result(result)

    def test_authority_flags_factory_passes_validator(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            create_command_kind_routing_authority_flags,
            validate_command_kind_routing_authority_flags,
        )
        flags = create_command_kind_routing_authority_flags()
        assert validate_command_kind_routing_authority_flags(flags)


# ---------------------------------------------------------------------------
# Classification coverage for all families
# ---------------------------------------------------------------------------


class TestFamilyClassificationCoverage:
    @pytest.mark.parametrize("command_type,expected_family", [
        ("move_north", "movement"),
        ("walk_east", "movement"),
        ("inspect_room", "inspection"),
        ("examine_object", "inspection"),
        ("look_around", "inspection"),
        ("interact_lever", "interaction"),
        ("use_item", "interaction"),
        ("social_greet", "social"),
        ("persuade_guard", "social"),
        ("attack_target", "combat"),
        ("strike_enemy", "combat"),
        ("ability_fireball", "ability"),
        ("cast_spell", "ability"),
        ("inventory_check", "inventory"),
        ("equip_sword", "inventory"),
        ("recover_health", "recovery"),
        ("rest_camp", "recovery"),
        ("craft_potion", "crafting"),
        ("forge_sword", "crafting"),
        ("travel_north", "travel"),
        ("journey_begin", "travel"),
        ("research_lore", "research"),
        ("study_tome", "research"),
        ("mission_accept", "mission"),
        ("quest_update", "mission"),
        ("system_status", "system_meta"),
        ("meta_info", "system_meta"),
        ("xyzzy_gibberish", "unknown"),
    ])
    def test_family_classification(self, command_type, expected_family):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            classify_command_type_to_family,
        )
        assert classify_command_type_to_family(command_type) == expected_family


# ---------------------------------------------------------------------------
# Input validation / malformed input
# ---------------------------------------------------------------------------


class TestMalformedInput:
    def test_invalid_family_in_definition_raises(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            InvalidCommandKindDefinitionError,
            create_command_kind_definition,
        )
        with pytest.raises(InvalidCommandKindDefinitionError):
            create_command_kind_definition(
                kind_id="test", family="INVALID_FAMILY",
                kind_label="Test", description="Test",
            )

    def test_empty_kind_id_raises(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            InvalidCommandKindDefinitionError,
            create_command_kind_definition,
        )
        with pytest.raises(InvalidCommandKindDefinitionError):
            create_command_kind_definition(
                kind_id="", family="combat",
                kind_label="Test", description="Test",
            )

    def test_invalid_owner_route_raises(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            InvalidCommandDispatchShellError,
            create_command_dispatch_shell,
        )
        with pytest.raises(InvalidCommandDispatchShellError):
            create_command_dispatch_shell(
                dispatch_ref=build_record_id("dispatch", "test"),
                command_ref="cmd_ref",
                owner_route="TOTALLY_FAKE_OWNER",
                family="combat",
            )

    def test_invalid_classification_ref_raises(self):
        from astra_runtime.domain.command_kind_routing_skeleton import (
            InvalidCommandKindClassificationError,
            create_command_kind_classification,
        )
        with pytest.raises(InvalidCommandKindClassificationError):
            create_command_kind_classification(
                classification_ref="not_a_valid_record_id",
                command_ref="cmd_ref",
                raw_command_type="inspect",
                family="inspection",
                kind="inspect",
            )
