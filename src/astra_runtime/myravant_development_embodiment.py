"""Noncanonical body and course declarations for the existing posture owner."""

from dataclasses import replace

from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_play_fixture import (
    EmbodimentPresentation,
    FixtureMovementMethodRoute,
    FixtureMovementObstructionLicense,
    WAYSTONE_ID,
    WORKSHOP_ID,
    YARD_ID,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_posture import PostureMovementLicense


DEVELOPMENT_BODIES = {
    "low-frame": (
        "Low frame",
        (("stand", "standing"), ("stand up", "standing"),
         ("crouch", "crouching"), ("crouch down", "crouching")),
        "crouching",
        True,
    ),
    "folding-frame": (
        "Folding frame",
        (("fold", "folded"), ("folded", "folded"),
         ("extend", "extended"), ("extended", "extended")),
        "folded",
        False,
    ),
}
DEVELOPMENT_COURSES = {"orchard": "east", "gatehouse": "south"}


def create_development_embodiment_fixture(body: str, course: str = "orchard"):
    """Use the same initial world for both bodies and both declared corridors."""
    if body not in DEVELOPMENT_BODIES or course not in DEVELOPMENT_COURSES:
        raise ValueError("Unknown development body or course.")
    name, commands, clearance, can_crawl = DEVELOPMENT_BODIES[body]
    direction = DEVELOPMENT_COURSES[course]
    fixture = create_terminal_play_fixture()
    profile = replace(
        fixture.posture_profile,
        profile_id=f"noncanonical-development-{body}",
        version=1,
        configurations=tuple(dict.fromkeys(pose for _, pose in commands)),
    )
    return replace(
        fixture,
        provenance=replace(
            fixture.provenance,
            fixture_id=build_record_id("fixture", f"development-embodiment-{course}"),
            fixture_version="1",
            origin_workstream="development-embodiment",
            origin_merge_commit="0" * 40,
            origin_merged_at="",
        ),
        embodiment=EmbodimentPresentation(name=name, configuration_commands=commands),
        posture_profile=profile,
        posture_movement_licenses=(PostureMovementLicense(
            source_place_id=YARD_ID,
            profile_id=profile.profile_id,
            version=profile.version,
            direction=direction,
            method="walk",
            configurations=(clearance,),
        ),),
        movement_obstruction_licenses=(FixtureMovementObstructionLicense(
            source_place_id=YARD_ID,
            direction=direction,
            blocking_object_entity_id=WAYSTONE_ID,
            blocking_object_place_id=YARD_ID,
        ),),
        movement_method_routes=(
            FixtureMovementMethodRoute(source_place_id=WORKSHOP_ID, direction="south", method="crawl"),
            FixtureMovementMethodRoute(
                source_place_id=YARD_ID, direction=direction, method="crawl", bypass_obstruction=True,
            ),
        ) if can_crawl else (),
    )
