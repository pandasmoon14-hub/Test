"""Profile-scoped whole-component fit and lineage for approved #555.

RT-010 material state; not universal durability, damage, mass, or crafting yields.
"""
from dataclasses import dataclass, replace
from astra_runtime.domain.persistent_world_material import MaterialError, digest
from astra_runtime.kernel.record_identity import build_record_id


@dataclass(frozen=True)
class TransformationProfile:
    old: str
    spare: str
    tool: str
    barrier_board: str
    trestle: str
    repair_board: str
    repair_cord: str
    barrier_place: str
    work_place: str
    version: str = "whole-component-fit-1"


@dataclass(frozen=True)
class TransformationWork:
    actor: str
    method: str
    target: str
    resource: str
    stage: int = 0
    status: str = "active"
    receipts: tuple[str, ...] = ()


@dataclass(frozen=True)
class TransformationState:
    roles: tuple[tuple[str, str], ...]
    work: TransformationWork | None = None
    lineage: tuple[tuple[str, str, str, str, int, str, str | None], ...] = ()


def initial_state(profile):
    return TransformationState(((profile.old, "unfit"), (profile.spare, "fit")))


def role(state, entity):
    return dict(state.roles).get(entity)


def validate_profile(profile, representation, material):
    objects = {e.entity_id for e in representation.entities if e.classification == "object"}
    places = {e.entity_id for e in representation.entities if e.classification == "place"}
    participants = (profile.old, profile.spare, profile.tool, profile.barrier_board,
                    profile.trestle, profile.repair_board, profile.repair_cord)
    if (len(set(participants)) != len(participants) or not set(participants) <= objects or
            profile.barrier_place not in places or profile.work_place not in places or
            profile.version != "whole-component-fit-1"):
        raise MaterialError("invalid whole-component profile")
    expected = ((profile.barrier_board, profile.old, "tie"),
                (profile.barrier_board, profile.spare, "tie"),
                (profile.repair_board, profile.old, "tie"))
    if any(not any(a == left and b == right and method == verb
                   for a, b, _, method in material.fastening_pairs)
           for left, right, verb in expected):
        raise MaterialError("missing owner fastening qualification")
    if any((part, profile.trestle) not in material.support_pairs
           for part in (profile.old, profile.spare)):
        raise MaterialError("missing owner support qualification")


def validate_state(state, profile, actors, receipts):
    roles = dict(state.roles)
    if (len(state.roles) != 2 or set(roles) != {profile.old, profile.spare} or
            roles[profile.old] not in {"unfit", "prepared", "fit", "spacer"} or
            roles[profile.spare] != "fit"):
        raise MaterialError("component fit or identity mismatch")
    work = state.work
    if work is not None:
        required = profile.spare if work.method == "replace" else profile.tool
        max_steps = 1 if work.method == "repurpose" else 2
        if (work.actor not in actors or work.method not in {"refit", "replace", "repurpose"} or
                work.target != profile.old or work.resource != required or
                type(work.stage) is not int or work.stage not in range(max_steps+1) or
                work.status not in {"active", "blocked", "paused", "abandoned", "completed"} or
                len(work.receipts) != work.stage or
                (work.status == "completed") != (work.stage == max_steps)):
            raise MaterialError("invalid transformation task")
    if len(set(row[5] for row in state.lineage)) != len(state.lineage):
        raise MaterialError("duplicate transformation receipts")
    expected_role = "unfit"
    for index,row in enumerate(state.lineage):
        if (len(row) != 7 or row[0] not in {"refit", "replace", "repurpose"} or
                row[1] not in actors or row[2] != profile.old or
                row[3] != (profile.spare if row[0]=="replace" and row[4]==2 else profile.old) or
                row[5] not in receipts or
                (row[0]=="replace") != (row[6] is not None) or
                type(row[4]) is not int or row[4] not in {1,2} or
                (row[4]==2 and
                 (index==0 or state.lineage[index-1][0]!=row[0] or state.lineage[index-1][4]!=1)) or
                (row[0]=="repurpose" and row[4]!=1)):
            raise MaterialError("invalid component provenance or stage order")
        if row[0]=="refit":
            expected_role="prepared" if row[4]==1 else "fit"
        elif row[0]=="repurpose":
            expected_role="spacer"
    if roles[profile.old] != expected_role:
        raise MaterialError("component fit differs from acknowledged owner lineage")
    if work and work.stage and tuple(row[5] for row in state.lineage[-work.stage:]) != work.receipts:
        raise MaterialError("lost acknowledged work")


def record_stage(state, profile, actor, clock_receipt, tick, physical_receipt=None):
    task = state.work
    if task is None or task.actor != actor or task.status not in {"active", "blocked"}:
        raise MaterialError("no eligible transformation")
    stage = task.stage + 1
    end = 1 if task.method == "repurpose" else 2
    if stage > end:
        raise MaterialError("already complete")
    token = digest((state.roles, state.lineage, task.method, actor,
                    stage, tick, clock_receipt, physical_receipt))[:28]
    receipt = build_record_id("transformation_receipt", token)
    roles = dict(state.roles)
    if task.method == "refit":
        roles[profile.old] = "prepared" if stage == 1 else "fit"
    if task.method == "repurpose":
        roles[profile.old] = "spacer"
    output = profile.spare if task.method == "replace" and stage == 2 else profile.old
    after = replace(state,
        roles=tuple(sorted(roles.items())),
        work=replace(task,stage=stage,status="completed" if stage == end else "active",
                     receipts=(*task.receipts,receipt)),
        lineage=(*state.lineage,(task.method,actor,profile.old,output,stage,receipt,physical_receipt)))
    return after,receipt
