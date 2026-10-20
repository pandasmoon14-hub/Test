"""Noncanonical opt-in investigation cases with version-bound actor roots.

A recipe selects existing actor profiles and ordering only. Its setup does not
assign culprit, private memory, physical outcomes or new rules. Historical facts
are created exclusively when actual owner operations execute during play.
"""
from dataclasses import dataclass, replace
import re

from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_actors import (
    ActorFixture, create_actor_fixture, execute_actor_locality_request,
)


CASES = ("cleanup", "assembly", "relay", "neutral-contended", "neutral-reverse", "neutral-relay")
PROFILE_VERSION = "investigation-1"


@dataclass(frozen=True)
class InvestigationFixture(ActorFixture):
    @property
    def locality_help(self):
        root = ("Investigation: recall <admitted subject> <facet>; "
                "compare reports about <admitted subject> <facet>. "
                "Read-only history never confirms current truth.\n")
        if self.actors_version.startswith("investigation-neutral"):
            return root + ("Neutral case: go east/west/north/south, inspect, "
                           "ask <actor> to clean or assemble, ask <actor> about "
                           "<target> <facet>, tell <actor> that <target> residue is clear/present, wait, save.\n")
        return root + super().locality_help


def create_investigation_fixture(case="cleanup"):
    if case not in CASES or type(case) is not str:
        raise ValueError("unknown noncanonical investigation recipe")
    if case.startswith("neutral-"):
        from astra_runtime.myravant_investigation_neutral import create_neutral_investigation_fixture
        return InvestigationFixture(**create_neutral_investigation_fixture(case).__dict__)
    original = create_actor_fixture()
    oren, tali = original.actor_profiles
    if case == "assembly":
        oren = replace(oren, standing_kind="assembly",
                       standing_method="workshop assembly",
                       standing_participants=(identity("repair-board"),
                                              identity("repair-peg"),
                                              identity("repair-cord")),
                       standing_place=identity("work-bench"))
        order = (tali.actor_id, oren.actor_id)
    elif case == "relay":
        oren = replace(oren, standing_kind=None, standing_method=None,
                       standing_participants=(), standing_place=None)
        tali = replace(tali, standing_kind=None, standing_method=None,
                       standing_participants=(), standing_place=None)
        order = (oren.actor_id, tali.actor_id)
    else:
        order = (oren.actor_id, tali.actor_id)
    fixture = create_actor_fixture(actor_profiles=(oren, tali), actor_order=order)
    # Distinct opt-in replay binding; the inherited owner root also binds the
    # concrete profiles and order. Existing actor checkpoints are unaffected.
    return InvestigationFixture(**replace(fixture, actors_version=PROFILE_VERSION + "-" + case).__dict__)


def parse_investigation_request(raw):
    text = " ".join(raw.strip().casefold().split())
    match = re.fullmatch(r"recall (.+?) (residue|moisture|placement|assembly|trace|activity)", text)
    if match:
        return "recall", match.groups()
    match = re.fullmatch(r"compare (?:reports|accounts|evidence) about (.+?) (residue|moisture|placement|assembly|trace|activity)", text)
    if match:
        return "compare", match.groups()
    return None


def execute_investigation_request(application, raw):
    parsed = parse_investigation_request(raw)
    if parsed is None:
        return execute_actor_locality_request(application, raw)
    operation, (subject, facet) = parsed
    if operation == "recall":
        return "investigation", application.recall_history(subject, facet)
    return "investigation", application.compare_history(subject, facet)
