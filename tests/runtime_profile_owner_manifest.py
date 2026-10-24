"""Test-only inventory of profile-local state owners in astra_runtime root.

Unlike tests.runtime_domain_package_manifest, this boundary classifies the
root package; it does not extend domain/ authority or modify its immutable
AUTHORIZED_RUNTIME_DOMAIN_FILES. The exact baseline non-owner census is also
registered, so an *unreviewed* new root Python module always fails closed.

This is a classification guard, NOT an automatic proof of semantic ownership:
a reviewer must inspect each new module's actual responsibilities. Storage,
projection, fixture declarations, and checkpoint transport alone do not confer
semantic ownership. No runtime code may import this test-only registry.
"""
from __future__ import annotations

from pathlib import Path


# Manually reconciled authority-bearing profile-local state owners on main.
# Ownership scope is specific; other authority stays with established domain/.
PROFILE_LOCAL_OWNER_FILES = frozenset({
    "myravant_actor_activity.py",  # actor-owned activity-stage declaration / history; not work/material ownership
    "myravant_actor_situated_knowledge.py",  # actor-scoped admitted sightings and testimony; not world truth
    "myravant_e1_latch_duty.py",  # fixture-local accepted, cancelled, fulfilled duty commitment
    "myravant_posture.py",  # profile-scoped posture event and state transitions; not spatial placement
    "myravant_service_commitment.py",  # accepted terms, consent decision, attribution and settlement eligibility
})

# Existing root Python modules adjudicated as adapters, fixtures, applications,
# checkpoint transport, interpreters, entrypoints, or nonauthoritative evidence.
# No new root file is automatically treated as non-owner.
REGISTERED_ROOT_NON_OWNER_FILES = frozenset({
    "__init__.py",
    "myravant_activity_application.py",
    "myravant_actor_application.py",
    "myravant_actor_ground_assistance.py",
    "myravant_actor_knowledge.py",
    "myravant_actor_physical.py",
    "myravant_b2a_service_goal.py",
    "myravant_b2b_waystone_clearance.py",
    "myravant_bounded_work_goals.py",
    "myravant_c1_investigation_goal.py",
    "myravant_chest_investigation_goal.py",
    "myravant_chest_readiness_goal.py",
    "myravant_cooperative_delivery_goal.py",
    "myravant_d1_brace_goal.py",
    "myravant_d1_checkpoint.py",
    "myravant_e1_checkpoint.py",
    "myravant_e1_duty_goal.py",
    "myravant_e2_actor_service_goal.py",
    "myravant_fixture_brace.py",
    "myravant_generated_locality.py",
    "myravant_goal_method_lantern.py",
    "myravant_investigation_application.py",
    "myravant_investigation_cases.py",
    "myravant_investigation_neutral.py",
    "myravant_live_play_evidence.py",
    "myravant_material_application.py",
    "myravant_orchard_supply_goal.py",
    "myravant_physical_placement_goal.py",
    "myravant_play_application.py",
    "myravant_play_fixture.py",
    "myravant_player_sensory_breadth.py",
    "myravant_posture_checkpoint.py",
    "myravant_service_application.py",
    "myravant_situated_inquiry.py",
    "myravant_structures_application.py",
    "myravant_surface_water_application.py",
    "myravant_tarrow.py",
    "myravant_tarrow_activity.py",
    "myravant_tarrow_actors.py",
    "myravant_tarrow_environment.py",
    "myravant_tarrow_investigation.py",
    "myravant_tarrow_material.py",
    "myravant_tarrow_structures.py",
    "myravant_tarrow_surface_water.py",
    "myravant_tarrow_time.py",
    "myravant_tarrow_transformation.py",
    "myravant_tarrow_water.py",
    "myravant_terminal.py",
    "myravant_terminal_capabilities.py",
    "myravant_timed_application.py",
    "myravant_transformation_application.py",
    "myravant_vsm10_actor_mediated_movement.py",
    "myravant_vsm10_terminal.py",
    "myravant_vsm11_actor_mediated_storage.py",
    "myravant_vsm11_terminal.py",
    "myravant_vsm12_actor_mediated_custody.py",
    "myravant_vsm12_terminal.py",
    "myravant_vsm13_actor_mediated_displacement.py",
    "myravant_vsm13_terminal.py",
    "myravant_vsm14_application.py",
    "myravant_vsm14_follow_intent.py",
    "myravant_vsm14_terminal.py",
    "myravant_vsm9_actor_mediated_object_state.py",
    "myravant_vsm9_terminal.py",
    "myravant_water_application.py",
    "runtime_skeleton_checkpoint_descriptors.py",
    "runtime_skeleton_custody_adapter.py",
    "runtime_skeleton_existing_family_adapters.py",
})

# Static evidence for why these modules are owners. These names must be defined
# in each listed source; changing an owner contract requires review.
PROFILE_OWNER_WITNESSES = {
    "myravant_actor_activity.py": ("ActivityRecord", "replace_record"),
    "myravant_actor_situated_knowledge.py": ("ActorKnowledgeState", "commit_actor_knowledge"),
    "myravant_e1_latch_duty.py": ("FixtureDutyState", "execute_fixture_duty"),
    "myravant_posture.py": ("PostureState", "execute_posture"),
    "myravant_service_commitment.py": ("ServiceState", "decide", "settle"),
}


def runtime_root_python_files(repo_root: Path) -> frozenset[str]:
    root = repo_root / "src" / "astra_runtime"
    return frozenset(p.name for p in root.iterdir()
                     if p.is_file() and p.suffix == ".py")


def unregistered_runtime_root_files(repo_root: Path) -> frozenset[str]:
    """Fail closed on *any* new root module pending owner classification."""
    return runtime_root_python_files(repo_root) - (
        PROFILE_LOCAL_OWNER_FILES | REGISTERED_ROOT_NON_OWNER_FILES
    )


def missing_registered_runtime_root_files(repo_root: Path) -> frozenset[str]:
    return (PROFILE_LOCAL_OWNER_FILES | REGISTERED_ROOT_NON_OWNER_FILES) - (
        runtime_root_python_files(repo_root)
    )
