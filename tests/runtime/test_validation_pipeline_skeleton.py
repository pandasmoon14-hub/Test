"""Focused tests for RUNTIME-IMPL-PR-5: validation pipeline and invariant precheck skeleton."""

from __future__ import annotations

from tests.runtime_domain_package_manifest import (
    AUTHORIZED_RUNTIME_DOMAIN_ENTRIES,
    AUTHORIZED_RUNTIME_DOMAIN_FILES,
)

import copy
import os
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.kernel.validation_pipeline import (
    InvariantPrecheck,
    InvariantPrecheckError,
    InvalidInvariantPrecheckError,
    InvalidValidationCheckError,
    InvalidValidationIssueError,
    InvalidValidationResultError,
    ValidationIssue,
    ValidationPipelineError,
    ValidationResult,
    create_invariant_precheck,
    create_validation_issue,
    create_validation_result,
    required_keys_check,
    run_invariant_prechecks,
    run_validation_checks,
    validate_invariant_precheck,
    validate_validation_issue,
    validate_validation_result,
)

KERNEL_DIR = Path(__file__).resolve().parent.parent.parent / "src" / "astra_runtime" / "kernel"


class TestValidationIssue:
    def test_valid_creation(self):
        issue = create_validation_issue(
            code="test_code",
            message="test message",
            severity="error",
            source="test_source",
        )
        assert isinstance(issue, ValidationIssue)

    def test_preserves_code(self):
        issue = create_validation_issue(
            code="my_code", message="msg", severity="info", source="src"
        )
        assert issue.code == "my_code"

    def test_preserves_message(self):
        issue = create_validation_issue(
            code="c", message="my message", severity="info", source="src"
        )
        assert issue.message == "my message"

    def test_preserves_severity(self):
        issue = create_validation_issue(
            code="c", message="m", severity="warning", source="src"
        )
        assert issue.severity == "warning"

    def test_preserves_source(self):
        issue = create_validation_issue(
            code="c", message="m", severity="info", source="my_source"
        )
        assert issue.source == "my_source"

    @pytest.mark.parametrize("severity", ["info", "warning", "error", "critical"])
    def test_allowed_severities(self, severity):
        issue = create_validation_issue(
            code="c", message="m", severity=severity, source="s"
        )
        assert issue.severity == severity

    @pytest.mark.parametrize("severity", ["debug", "fatal", "CRITICAL", "Error", "", 42])
    def test_unsupported_severity_rejected(self, severity):
        with pytest.raises(InvalidValidationIssueError):
            create_validation_issue(
                code="c", message="m", severity=severity, source="s"
            )

    @pytest.mark.parametrize("code", ["", "   ", 42, None])
    def test_empty_code_rejected(self, code):
        with pytest.raises(InvalidValidationIssueError):
            create_validation_issue(
                code=code, message="m", severity="info", source="s"
            )

    @pytest.mark.parametrize("message", ["", "   ", 42, None])
    def test_empty_message_rejected(self, message):
        with pytest.raises(InvalidValidationIssueError):
            create_validation_issue(
                code="c", message=message, severity="info", source="s"
            )

    @pytest.mark.parametrize("source", ["", "   ", 42, None])
    def test_empty_source_rejected(self, source):
        with pytest.raises(InvalidValidationIssueError):
            create_validation_issue(
                code="c", message="m", severity="info", source=source
            )

    def test_metadata_defaults_to_empty_mapping(self):
        issue = create_validation_issue(
            code="c", message="m", severity="info", source="s"
        )
        assert dict(issue.metadata) == {}

    def test_metadata_deep_copy_safe(self):
        inner = {"nested": [1, 2, 3]}
        issue = create_validation_issue(
            code="c", message="m", severity="info", source="s", metadata=inner
        )
        inner["nested"].append(4)
        assert list(issue.metadata["nested"]) == [1, 2, 3]

    def test_to_dict_returns_deep_copies(self):
        issue = create_validation_issue(
            code="c", message="m", severity="info", source="s",
            metadata={"key": [1]}
        )
        d1 = issue.to_dict()
        d2 = issue.to_dict()
        d1["metadata"]["key"].append(2)
        assert d2["metadata"]["key"] == [1]

    def test_validate_accepts_valid_issue(self):
        issue = create_validation_issue(
            code="c", message="m", severity="info", source="s"
        )
        assert validate_validation_issue(issue) is True

    def test_validate_rejects_invalid_object(self):
        assert validate_validation_issue("not an issue") is False
        assert validate_validation_issue(42) is False
        assert validate_validation_issue(None) is False

    def test_frozen_immutability(self):
        issue = create_validation_issue(
            code="c", message="m", severity="info", source="s"
        )
        with pytest.raises(AttributeError):
            issue.code = "changed"


class TestValidationResult:
    def test_valid_creation(self):
        result = create_validation_result(
            validation_id="v1",
            subject_ref="subj",
            passed=True,
        )
        assert isinstance(result, ValidationResult)

    def test_preserves_fields(self):
        issue = create_validation_issue(
            code="c", message="m", severity="info", source="s"
        )
        result = create_validation_result(
            validation_id="v1",
            subject_ref="subj",
            passed=False,
            issues=[issue],
        )
        assert result.validation_id == "v1"
        assert result.subject_ref == "subj"
        assert result.passed is False
        assert len(result.issues) == 1
        assert result.issues[0].code == "c"

    @pytest.mark.parametrize("vid", ["", "   ", 42, None])
    def test_rejects_empty_validation_id(self, vid):
        with pytest.raises(InvalidValidationResultError):
            create_validation_result(
                validation_id=vid, subject_ref="s", passed=True
            )

    @pytest.mark.parametrize("sref", ["", "   ", 42, None])
    def test_rejects_empty_subject_ref(self, sref):
        with pytest.raises(InvalidValidationResultError):
            create_validation_result(
                validation_id="v", subject_ref=sref, passed=True
            )

    @pytest.mark.parametrize("passed", [1, 0, "true", None])
    def test_rejects_non_bool_passed(self, passed):
        with pytest.raises(InvalidValidationResultError):
            create_validation_result(
                validation_id="v", subject_ref="s", passed=passed
            )

    def test_rejects_non_validation_issue_entries(self):
        with pytest.raises(InvalidValidationResultError):
            create_validation_result(
                validation_id="v", subject_ref="s", passed=True,
                issues=["not an issue"]
            )

    def test_metadata_deep_copy_safe(self):
        inner = {"nested": [1, 2]}
        result = create_validation_result(
            validation_id="v", subject_ref="s", passed=True,
            metadata=inner,
        )
        inner["nested"].append(3)
        assert list(result.metadata["nested"]) == [1, 2]

    def test_validate_accepts_valid_result(self):
        result = create_validation_result(
            validation_id="v", subject_ref="s", passed=True
        )
        assert validate_validation_result(result) is True

    def test_validate_rejects_invalid_object(self):
        assert validate_validation_result("not a result") is False
        assert validate_validation_result(42) is False

    def test_frozen_immutability(self):
        result = create_validation_result(
            validation_id="v", subject_ref="s", passed=True
        )
        with pytest.raises(AttributeError):
            result.passed = False


class TestRunValidationChecks:
    def test_runs_check_callables(self):
        called = []

        def check(subject):
            called.append(subject)
            return None

        run_validation_checks("v", "s", {"data": 1}, [check])
        assert called == [{"data": 1}]

    def test_returns_passed_when_no_issues(self):
        result = run_validation_checks("v", "s", {}, [lambda _: None])
        assert result.passed is True
        assert result.issues == ()

    def test_returns_passed_for_info_warning_only(self):
        def check(subject):
            return [
                create_validation_issue(
                    code="c", message="m", severity="info", source="s"
                ),
                create_validation_issue(
                    code="c2", message="m2", severity="warning", source="s"
                ),
            ]

        result = run_validation_checks("v", "s", {}, [check])
        assert result.passed is True
        assert len(result.issues) == 2

    def test_returns_failed_for_error_issue(self):
        def check(subject):
            return create_validation_issue(
                code="c", message="m", severity="error", source="s"
            )

        result = run_validation_checks("v", "s", {}, [check])
        assert result.passed is False

    def test_returns_failed_for_critical_issue(self):
        def check(subject):
            return create_validation_issue(
                code="c", message="m", severity="critical", source="s"
            )

        result = run_validation_checks("v", "s", {}, [check])
        assert result.passed is False

    def test_accepts_check_returning_one_issue(self):
        def check(subject):
            return create_validation_issue(
                code="c", message="m", severity="info", source="s"
            )

        result = run_validation_checks("v", "s", {}, [check])
        assert len(result.issues) == 1

    def test_accepts_check_returning_sequence_of_issues(self):
        def check(subject):
            return [
                create_validation_issue(
                    code="c1", message="m1", severity="info", source="s"
                ),
                create_validation_issue(
                    code="c2", message="m2", severity="info", source="s"
                ),
            ]

        result = run_validation_checks("v", "s", {}, [check])
        assert len(result.issues) == 2

    def test_accepts_check_returning_none(self):
        result = run_validation_checks("v", "s", {}, [lambda _: None])
        assert result.passed is True
        assert result.issues == ()

    def test_rejects_non_callable_check_entries(self):
        with pytest.raises(InvalidValidationCheckError):
            run_validation_checks("v", "s", {}, ["not callable"])

    def test_rejects_check_returning_invalid_single_object(self):
        with pytest.raises(InvalidValidationCheckError, match="check must return"):
            run_validation_checks("v", "s", {}, [lambda _: "bad"])

    def test_rejects_check_returning_sequence_with_non_validation_issue(self):
        def check(subject):
            return [
                create_validation_issue(code="c", message="m", severity="info", source="s"),
                "not an issue",
            ]

        with pytest.raises(InvalidValidationCheckError, match="non-ValidationIssue"):
            run_validation_checks("v", "s", {}, [check])

    def test_does_not_mutate_subject(self):
        original = {"key": [1, 2, 3]}
        snapshot = copy.deepcopy(original)

        def check(subject):
            return None

        run_validation_checks("v", "s", original, [check])
        assert original == snapshot


class TestRequiredKeysCheck:
    def test_passes_when_all_keys_exist(self):
        check = required_keys_check(["a", "b"])
        result = check({"a": 1, "b": 2, "c": 3})
        assert result == ()

    def test_returns_one_error_per_missing_key(self):
        check = required_keys_check(["a", "b", "c"])
        result = check({"a": 1})
        assert len(result) == 2
        assert all(issue.severity == "error" for issue in result)

    def test_rejects_non_mapping_subject(self):
        check = required_keys_check(["a"])
        result = check("not a mapping")
        assert len(result) == 1
        assert result[0].code == "not_a_mapping"

    def test_rejects_empty_required_key(self):
        with pytest.raises(InvalidValidationCheckError):
            required_keys_check(["a", ""])

    def test_rejects_non_string_required_key(self):
        with pytest.raises(InvalidValidationCheckError):
            required_keys_check(["a", 42])

    def test_does_not_enforce_nested_shape(self):
        check = required_keys_check(["a"])
        result = check({"a": {"nested": "anything"}})
        assert result == ()


class TestInvariantPrecheck:
    def test_valid_creation(self):
        precheck = create_invariant_precheck(
            invariant_id="inv1",
            description="test invariant",
            severity="error",
            source="test_source",
        )
        assert isinstance(precheck, InvariantPrecheck)

    def test_preserves_fields(self):
        precheck = create_invariant_precheck(
            invariant_id="inv1",
            description="test invariant",
            severity="warning",
            source="test_source",
        )
        assert precheck.invariant_id == "inv1"
        assert precheck.description == "test invariant"
        assert precheck.severity == "warning"
        assert precheck.source == "test_source"

    @pytest.mark.parametrize("severity", ["info", "warning", "error", "critical"])
    def test_allowed_severities(self, severity):
        precheck = create_invariant_precheck(
            invariant_id="inv", description="d", severity=severity, source="s"
        )
        assert precheck.severity == severity

    @pytest.mark.parametrize("severity", ["debug", "fatal", "CRITICAL", "", 42])
    def test_unsupported_severity_rejected(self, severity):
        with pytest.raises(InvalidInvariantPrecheckError):
            create_invariant_precheck(
                invariant_id="inv", description="d", severity=severity, source="s"
            )

    @pytest.mark.parametrize("inv_id", ["", "   ", 42, None])
    def test_empty_invariant_id_rejected(self, inv_id):
        with pytest.raises(InvalidInvariantPrecheckError):
            create_invariant_precheck(
                invariant_id=inv_id, description="d", severity="info", source="s"
            )

    @pytest.mark.parametrize("desc", ["", "   ", 42, None])
    def test_empty_description_rejected(self, desc):
        with pytest.raises(InvalidInvariantPrecheckError):
            create_invariant_precheck(
                invariant_id="inv", description=desc, severity="info", source="s"
            )

    @pytest.mark.parametrize("source", ["", "   ", 42, None])
    def test_empty_source_rejected(self, source):
        with pytest.raises(InvalidInvariantPrecheckError):
            create_invariant_precheck(
                invariant_id="inv", description="d", severity="info", source=source
            )

    def test_metadata_deep_copy_safe(self):
        inner = {"nested": [1, 2]}
        precheck = create_invariant_precheck(
            invariant_id="inv", description="d", severity="info", source="s",
            metadata=inner,
        )
        inner["nested"].append(3)
        assert list(precheck.metadata["nested"]) == [1, 2]

    def test_to_dict_returns_deep_copies(self):
        precheck = create_invariant_precheck(
            invariant_id="inv", description="d", severity="info", source="s",
            metadata={"key": [1]},
        )
        d1 = precheck.to_dict()
        d2 = precheck.to_dict()
        d1["metadata"]["key"].append(2)
        assert d2["metadata"]["key"] == [1]

    def test_validate_accepts_valid_precheck(self):
        precheck = create_invariant_precheck(
            invariant_id="inv", description="d", severity="info", source="s"
        )
        assert validate_invariant_precheck(precheck) is True

    def test_validate_rejects_invalid_object(self):
        assert validate_invariant_precheck("not a precheck") is False
        assert validate_invariant_precheck(42) is False

    def test_frozen_immutability(self):
        precheck = create_invariant_precheck(
            invariant_id="inv", description="d", severity="info", source="s"
        )
        with pytest.raises(AttributeError):
            precheck.invariant_id = "changed"


class TestRunInvariantPrechecks:
    def test_delegates_and_returns_validation_result(self):
        def check(subject):
            return create_validation_issue(
                code="c", message="m", severity="info", source="s"
            )

        result = run_invariant_prechecks("v", "s", {}, [check])
        assert isinstance(result, ValidationResult)
        assert result.passed is True
        assert len(result.issues) == 1

    def test_fails_on_error_issues(self):
        def check(subject):
            return create_validation_issue(
                code="c", message="m", severity="error", source="s"
            )

        result = run_invariant_prechecks("v", "s", {}, [check])
        assert result.passed is False

    def test_fails_on_critical_issues(self):
        def check(subject):
            return create_validation_issue(
                code="c", message="m", severity="critical", source="s"
            )

        result = run_invariant_prechecks("v", "s", {}, [check])
        assert result.passed is False

    def test_rejects_check_returning_invalid_object(self):
        with pytest.raises(InvalidValidationCheckError):
            run_invariant_prechecks("v", "s", {}, [lambda _: 42])

    def test_does_not_mutate_subject(self):
        original = {"key": [1, 2, 3]}
        snapshot = copy.deepcopy(original)

        result = run_invariant_prechecks("v", "s", original, [lambda _: None])
        assert original == snapshot


class TestGuardrails:
    @pytest.mark.parametrize(
        "module",
        [
            "invariant_validator.py",
        ],
    )
    def test_future_module_does_not_exist(self, module):
        assert not (KERNEL_DIR / module).exists(), (
            f"{module} must not exist yet"
        )

    def test_domain_package_contains_only_authorized_modules(self):
        domain_dir = KERNEL_DIR.parent / "domain"
        assert domain_dir.exists(), "Domain package should exist after PR-1A"
        allowed = set(AUTHORIZED_RUNTIME_DOMAIN_ENTRIES)
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
