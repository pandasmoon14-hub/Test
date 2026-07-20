"""Authoritative test manifest for the runtime domain package.

This module is test infrastructure only. It does not grant runtime authority and
must not be imported by ``src/astra_runtime``.
"""

from __future__ import annotations

from pathlib import Path


AUTHORIZED_RUNTIME_DOMAIN_FILES = frozenset(
    {
        "__init__.py",
        "action_legality.py",
        "action_legality_gate_integration_skeleton.py",
        "action_legality_service_interface_contract_skeleton.py",
        "action_legality_skeleton.py",
        "command_kind_routing_skeleton.py",
        "command_lifecycle.py",
        "context_packet_compiler.py",
        "event_commitment.py",
        "model_boundary_evaluation.py",
        "object_lever_event_commit_state_delta_path.py",
        "object_lever_interaction_legality_reader.py",
        "object_lever_replay_audit_check.py",
        "object_lever_transaction_preview_bridge.py",
        "projection_visibility_adapter_v0_1.py",
        "read_only_vertical_slice_state_owner_facade.py",
        "resource_consequence_math.py",
        "scene_command_execution_skeleton.py",
        "state_owner_interface_contract_skeleton.py",
        "state_projection.py",
        "state_store.py",
        "tiny_vertical_slice.py",
        "transaction_lifecycle.py",
        "transaction_preview_packet_bridge_skeleton.py",
        "validation_integration.py",
        "validation_integration_bridge_skeleton.py",
    }
)


def runtime_domain_files(repo_root: Path) -> frozenset[str]:
    """Return ordinary files currently present in ``astra_runtime.domain``."""

    domain_dir = repo_root / "src" / "astra_runtime" / "domain"
    return frozenset(path.name for path in domain_dir.iterdir() if path.is_file())


def unauthorized_runtime_domain_files(repo_root: Path) -> frozenset[str]:
    """Return files present in the domain package but absent from the manifest."""

    return runtime_domain_files(repo_root) - AUTHORIZED_RUNTIME_DOMAIN_FILES


def missing_runtime_domain_files(repo_root: Path) -> frozenset[str]:
    """Return manifest entries missing from the domain package."""

    return AUTHORIZED_RUNTIME_DOMAIN_FILES - runtime_domain_files(repo_root)
