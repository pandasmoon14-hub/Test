"""Approved #563 finite, noncanonical actor activity profile over existing work.

These stage declarations do not create canon, reservations, transport shortcuts,
a planner authority or a second logical clock.
"""
from dataclasses import dataclass
import re

from astra_runtime.myravant_actor_activity import ActivityMethod, ActivityStage, ActivityProgram
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_structures import StructuresFixture, create_structures_fixture
from astra_runtime.myravant_structures_application import execute_structures_request


@dataclass(frozen=True)
class ActivityFixture(StructuresFixture):
    activity_case: str = "standard"
    activity_programs: tuple[ActivityProgram, ...] = ()

    @property
    def locality_help(self):
        return ("Actor activities (noncanonical): ask Oren Kesh to undertake bench upkeep; "
                "ask Tali Ren to undertake yard upkeep (or bench upkeep in the contended case); "
                "ask <actor> about activity; ask <actor> to cancel activity. "
                "Each admitted finite activity performs real cleaning, assembly, and a "
                "qualified tool-drop recovery stage over separate world intervals. "
                "The actor may be blocked or withdraw; acceptance reserves nothing. "
                "Reports require present local communication and reveal only disclosed "
                "work state. Status does not advance time; remote actor truth is private.\n"
                + super().locality_help)


def _method(kind, name, participants, place):
    return ActivityMethod(kind, name, tuple(identity(x) for x in participants), identity(place))


def create_activity_fixture(*, activity_case="standard", structures_case="standard", shared_campaign=False):
    if activity_case not in {"standard", "contended"}:
        raise ValueError("unknown approved activity case")
    base = create_structures_fixture(structures_case=structures_case, activity_case=activity_case,
                                     shared_campaign=shared_campaign)
    if activity_case == "standard":
        profiles = (
            ActivityProgram("bench upkeep", identity("oren"), (
                ActivityStage((_method("cleaning", "wipe", ("practice-panel", "cleaning-cloth"), "work-bench"),
                               _method("cleaning", "scrub", ("practice-panel", "cleaning-brush"), "work-bench"))),
                ActivityStage((_method("assembly", "workshop assembly",
                                       ("repair-board", "repair-peg", "repair-cord"), "work-bench"),)),
                ActivityStage((_method("recovery", "drop", ("cleaning-cloth",), "work-bench"),
                               _method("recovery", "drop", ("cleaning-brush",), "work-bench"))),
            )),
            ActivityProgram("yard upkeep", identity("tali"), (
                ActivityStage((_method("cleaning", "scrub", ("sorting-board", "cleaning-brush"), "yard-tools"),
                               _method("cleaning", "wipe", ("sorting-board", "cleaning-cloth"), "yard-tools"))),
                ActivityStage((_method("assembly", "work partition",
                                       ("work-panel", "barrier-crossbar", "work-cord"), "yard-tools"),)),
                ActivityStage((_method("recovery", "drop", ("cleaning-brush",), "yard-tools"),
                               _method("recovery", "drop", ("cleaning-cloth",), "yard-tools"))),
            )),
        )
    else:
        # Both actors share finite board/tool/fastener state; reverse actor order
        # is part of this distinct immutable root, not a universal fairness rule.
        profiles = tuple(ActivityProgram("bench upkeep", identity(key), (
            ActivityStage((_method("cleaning", "wipe", ("practice-panel", "cleaning-cloth"), "work-bench"),
                           _method("cleaning", "scrub", ("practice-panel", "cleaning-brush"), "work-bench"))),
            ActivityStage((_method("assembly", "workshop assembly",
                                   ("repair-board", "repair-peg", "repair-cord"), "work-bench"),)),
            ActivityStage((_method("recovery", "drop", ("cleaning-cloth",), "work-bench"),
                               _method("recovery", "drop", ("cleaning-brush",), "work-bench"))),
        )) for key in ("oren", "tali"))
    return ActivityFixture(**base.__dict__, activity_case=activity_case, activity_programs=profiles)


def execute_activity_request(application, raw):
    text = " ".join(raw.strip().casefold().split())
    match = re.fullmatch(r"ask (.+?) to undertake (.+)", text)
    if match:
        return "activity", application.request_activity(*match.groups())
    match = re.fullmatch(r"ask (.+?) about activity", text)
    if match:
        return "activity", application.activity_status(match.group(1))
    match = re.fullmatch(r"ask (.+?) to cancel activity", text)
    if match:
        return "activity", application.cancel_activity(match.group(1))
    return execute_structures_request(application, raw)
