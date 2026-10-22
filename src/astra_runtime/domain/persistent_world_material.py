"""Owner-approved #542: AFQR-18 support, RT-010 separable fastening.

No force, load, shape, anatomy, structural repair or automatic group motion.
Profiles are explicit AFQR-19 opportunities; sight/movement effects are derived
from declared live relations, never an authoritative arrangement-success flag.
"""
from dataclasses import asdict, dataclass, replace
import hashlib
import json

from astra_runtime.domain.persistent_world_entity_location_representation import PersistentWorldRelation
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.transaction_preview import create_transaction_preview
from astra_runtime.kernel.state_delta import create_state_delta_envelope


class MaterialError(ValueError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True)
class Connection:
    connection_id: str
    left: str
    right: str
    fastener: str
    method: str


@dataclass(frozen=True)
class MaterialEffect:
    """Conjunction of actual placements/connections with one qualified effect."""
    source: str
    direction: str
    kind: str  # movement or sight; no inferred coupling
    supports: tuple[tuple[str, str], ...]
    connections: tuple[tuple[str, str, str, str], ...]


@dataclass(frozen=True)
class MaterialProfile:
    actor_id: str
    support_pairs: tuple[tuple[str, str], ...]
    # left, right, whole fastener, method
    fastening_pairs: tuple[tuple[str, str, str, str], ...]
    effects: tuple[MaterialEffect, ...] = ()
    version: int = 1

    def validate(self, representation):
        if (type(self.version) is not int or type(self.support_pairs) is not tuple or type(self.fastening_pairs) is not tuple
            or type(self.effects) is not tuple or any(type(e) is not MaterialEffect for e in self.effects)
            or any(type(row) is not tuple or len(row)!=2 for row in self.support_pairs)
            or any(type(row) is not tuple or len(row)!=4 for row in self.fastening_pairs)):
            raise MaterialError('material declarations must be immutable typed rows')
        objects = {e.entity_id for e in representation.entities if e.classification == 'object'}
        actors = {e.entity_id for e in representation.entities if e.classification == 'character_or_creature'}
        places = {e.entity_id for e in representation.entities if e.classification == 'place'}
        if self.version != 1 or self.actor_id not in actors:
            raise MaterialError('invalid actor/profile version')
        if len(set(self.support_pairs)) != len(self.support_pairs) or len(set(self.fastening_pairs)) != len(self.fastening_pairs):
            raise MaterialError('duplicate qualification')
        for obj, surface in self.support_pairs:
            if obj not in objects or surface not in objects or obj == surface:
                raise MaterialError('invalid surface qualification')
        for left, right, fastener, method in self.fastening_pairs:
            if len({left, right, fastener}) != 3 or not {left, right, fastener} <= objects or method not in {'tie', 'fasten'}:
                raise MaterialError('invalid fastening qualification')
        for effect in self.effects:
            if effect.source not in places or effect.kind not in {'movement', 'sight'} or effect.direction not in {'north','south','east','west'}:
                raise MaterialError('invalid effect target')
            if not effect.supports or not effect.connections:
                raise MaterialError('effect requires physical arrangement')
            if not set(effect.supports) <= set(self.support_pairs) or not set(effect.connections) <= set(self.fastening_pairs):
                raise MaterialError('effect references unqualified participants')


def placement(rep, obj):
    found = [r for r in rep.relations if r.subject_entity_id == obj]
    if len(found) != 1:
        raise MaterialError('object must have exactly one immediate placement')
    return found[0]


def effective_place(rep, obj, seen=()):
    if obj in seen:
        raise MaterialError('cyclic placement')
    r = placement(rep, obj)
    if r.relation_type == 'located_at':
        return r.object_entity_id
    return effective_place(rep, r.object_entity_id, (*seen, obj))


def validate_joint(rep, connections, profile):
    profile.validate(rep)
    ids = set()
    fasteners = set()
    for e in rep.entities:
        if e.classification == 'object':
            r = placement(rep, e.entity_id)
            effective_place(rep, e.entity_id)
            if r.relation_type == 'supported_by':
                if (e.entity_id, r.object_entity_id) not in profile.support_pairs:
                    raise MaterialError('unqualified supported placement')
                if placement(rep, r.object_entity_id).relation_type not in {'located_at', 'carried_by'}:
                    raise MaterialError('only one support level is admitted')
    for c in connections:
        if c.connection_id in ids or c.fastener in fasteners or (c.left,c.right,c.fastener,c.method) not in profile.fastening_pairs:
            raise MaterialError('duplicate or unqualified connection')
        ids.add(c.connection_id); fasteners.add(c.fastener)
        r = placement(rep,c.fastener)
        if r.relation_type != 'reserved_by' or r.object_entity_id != c.left:
            raise MaterialError('fastener allocation differs from connection')
        if effective_place(rep,c.left) != effective_place(rep,c.right):
            raise MaterialError('connection endpoints are separated')
    reserved = {r.subject_entity_id for r in rep.relations if r.relation_type == 'reserved_by'}
    if reserved != fasteners:
        raise MaterialError('unattributed reserved material')


def constrained(rep, connections, obj):
    return (any(r.relation_type == 'supported_by' and (r.subject_entity_id == obj or r.object_entity_id == obj) for r in rep.relations)
            or any(obj in (c.left,c.right,c.fastener) for c in connections))


def active_effects(rep, connections, profile):
    supports = {(r.subject_entity_id,r.object_entity_id) for r in rep.relations if r.relation_type == 'supported_by'}
    linked = {(c.left,c.right,c.fastener,c.method) for c in connections}
    return tuple(e for e in profile.effects if set(e.supports) <= supports and set(e.connections) <= linked)


def execute_material(*, rep, connections, profile, operation, participants, visible_ids,
                     command_id, expected_pre_digest, pre_digest):
    """Pure qualified reducer. Caller installs state only after durable commit."""
    validate_joint(rep, connections, profile)
    arities={'put_on':2,'lift_from':2,'tie':3,'fasten':3,'untie':3,'unfasten':3}
    if operation not in arities or type(participants) is not tuple or len(participants)!=arities[operation]:
        raise MaterialError('invalid material operation or participants')
    if expected_pre_digest != pre_digest:
        raise MaterialError('stale material opportunity')
    actor = profile.actor_id
    here = effective_place(rep,actor)
    if not set(participants) <= set(visible_ids):
        raise MaterialError('participants are not currently accessible')
    if any(effective_place(rep,x) != here for x in participants):
        raise MaterialError('participants are not local')
    obj = participants[0]
    subject = obj
    after_connections = connections
    if operation == 'put_on':
        surface = participants[1]
        if (obj,surface) not in profile.support_pairs or constrained(rep,connections,obj):
            raise MaterialError('surface placement is not qualified')
        if placement(rep,obj).relation_type != 'carried_by' or placement(rep,obj).object_entity_id != actor:
            raise MaterialError('carry the object before placing it')
        if placement(rep,surface).relation_type != 'located_at':
            raise MaterialError('surface must be stationary and directly accessible')
        relation_type, target, owner = 'supported_by',surface,'AFQR-18'
    elif operation == 'lift_from':
        surface = participants[1]
        r = placement(rep,obj)
        if r.relation_type != 'supported_by' or r.object_entity_id != surface or any(obj in (c.left,c.right,c.fastener) for c in connections):
            raise MaterialError('remove the relevant fastening before lifting')
        relation_type,target,owner = 'carried_by',actor,'RT-010'
    elif operation in {'tie','fasten'}:
        left,right,fastener = participants
        if (left,right,fastener,operation) not in profile.fastening_pairs:
            raise MaterialError('method and participants are not qualified')
        if placement(rep,fastener).relation_type != 'carried_by' or placement(rep,fastener).object_entity_id != actor:
            raise MaterialError('fastener must be available in carried custody')
        if any(placement(rep,x).relation_type not in {'located_at','supported_by'} for x in (left,right)):
            raise MaterialError('place the endpoints before fastening')
        subject = fastener
        relation_type,target,owner = 'reserved_by',left,'RT-010'
        after_connections = (*connections,Connection(build_record_id('material_connection',digest([command_id,left,right,fastener])[:28]),left,right,fastener,operation))
    elif operation in {'untie','unfasten'}:
        matches = [c for c in connections if c.fastener == obj and (operation == 'untie') == (c.method == 'tie')]
        if len(matches) != 1 or set(participants) != {obj,matches[0].left,matches[0].right}:
            raise MaterialError('no accessible matching connection')
        after_connections = tuple(c for c in connections if c != matches[0])
        relation_type,target,owner = 'carried_by',actor,'RT-010'
    else:
        raise MaterialError('material operation is not admitted')
    token = digest([command_id,pre_digest,operation,participants])[:28]
    relation = PersistentWorldRelation(relation_id=build_record_id('relation','material-'+token),
        relation_type=relation_type,subject_entity_id=subject,object_entity_id=target,semantic_owner=owner)
    after = replace(rep,relations=tuple(r for r in rep.relations if r.subject_entity_id != subject)+(relation,))
    validate_joint(after,after_connections,profile)
    command = create_command_envelope(command_id=command_id,command_type='interact',source_actor_id=actor,
        payload={'operation':operation,'participants':list(participants)},metadata={'package':'PLAY-TARROW-MATERIAL-1'})
    preview = create_transaction_preview(preview_id=build_record_id('material_preview',token),command=command,
        metadata={'semantic_owner':owner,'opportunity_owner':'AFQR-19','mutation_performed':False})
    delta = create_state_delta_envelope(delta_id=build_record_id('material_delta',token),source_command_id=command_id,
        source_preview_id=preview.preview_id,affected_record_ids=participants,change_type='relationship_update',
        payload={'operation':operation,'participants':list(participants),'pre_digest':pre_digest},
        metadata={'semantic_owner':owner,'transition_owner':'AFQR-01'})
    return after,after_connections,dict(command_id=command_id,command_fingerprint=digest(command.to_dict()),
        preview_id=preview.preview_id,state_delta_id=delta.delta_id,receipt_id=build_record_id('material_receipt',token),
        opportunity_evidence_id=build_record_id('evidence','material-opportunity-'+token))


# Approved #555 noncanonical whole-component fit and source-qualified lineage.
# These records extend RT-010 material meaning without installing another
# top-level domain owner or introducing numeric durability, cut yields or mass.


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
    blocked_due: int = 0
    due_intervals: tuple[str, ...] = ()
    reason: str | None = None


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
                work.status not in {"active", "blocked", "paused", "abandoned", "withdrawn", "completed"} or
                type(work.blocked_due) is not int or not 0 <= work.blocked_due <= 32 or
                type(work.due_intervals) is not tuple or
                len(set(work.due_intervals)) != len(work.due_intervals) or
                len(work.due_intervals) < work.stage or
                (work.reason is not None and (type(work.reason) is not str or not work.reason)) or
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
