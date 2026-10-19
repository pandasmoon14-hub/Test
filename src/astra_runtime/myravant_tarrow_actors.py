"""Approved #548 opt-in, noncanonical two-actor participation declarations.

Profiles declare bounded opportunity/policy; role labels do not grant access,
consent, custody or knowledge. Parsing proposes typed requests only.
"""
from dataclasses import asdict, dataclass, replace
import re

from astra_runtime.myravant_tarrow import create_tarrow_fixture, identity
from astra_runtime.myravant_tarrow_time import TimedFixture, create_timed_fixture, execute_timed_locality_request
from astra_runtime.myravant_tarrow_water import water_layout
from astra_runtime.domain.persistent_world_material import digest
from astra_runtime.domain.persistent_world_timed_environment import canonical_profile


@dataclass(frozen=True)
class ActorProfile:
    actor_id: str
    willing: bool = True
    returns_task_materials: bool = True
    blocked_limit: int = 3
    communication_classes: tuple[str, ...] = ('request', 'status', 'report', 'control')
    methods: tuple[str, ...] = ('wipe', 'scrub')
    cleaning_pairs: tuple[tuple[str, str, str], ...] = ()
    routes: tuple[tuple[str, str], ...] = ()
    assembly_names: tuple[str, ...] = ('workshop assembly', 'passage barrier', 'visual screen')
    standing_kind: str | None = None
    standing_method: str | None = None
    standing_participants: tuple[str, ...] = ()
    standing_place: str | None = None

    def __post_init__(self):
        if type(self.actor_id) is not str or not self.actor_id.strip() or type(self.willing) is not bool or type(self.returns_task_materials) is not bool:
            raise ValueError('invalid actor participation identity/policy')
        if type(self.blocked_limit) is not int or not 1 <= self.blocked_limit <= 32:
            raise ValueError('blocked limit must be a whole value in 1..32')
        for name in ('communication_classes', 'methods', 'standing_participants', 'assembly_names'):
            values = getattr(self, name)
            if type(values) is not tuple or any(type(v) is not str or not v.strip() for v in values) or len(set(values)) != len(values):
                raise ValueError('distinct immutable actor profile values required')
        if not set(self.communication_classes) <= {'request', 'status', 'report', 'control'} or not set(self.methods) <= {'wipe', 'scrub'}:
            raise ValueError('unknown communication class or cleaning method')
        for name, size in (('cleaning_pairs', 3), ('routes', 2)):
            rows = getattr(self, name)
            if type(rows) is not tuple or any(type(row) is not tuple or len(row) != size or any(type(v) is not str or not v.strip() for v in row) for row in rows) or len(set(rows)) != len(rows):
                raise ValueError('invalid immutable actor qualification rows')
        if any(method not in self.methods for _, _, method in self.cleaning_pairs):
            raise ValueError('cleaning pair uses an undeclared method')
        if self.standing_kind is None:
            if self.standing_method is not None or self.standing_participants or self.standing_place is not None:
                raise ValueError('absent standing activity cannot have participants')
        elif self.standing_kind not in {'cleaning', 'assembly'} or not self.standing_method or not self.standing_participants or not self.standing_place:
            raise ValueError('complete declared standing activity required')
        elif self.standing_kind == 'cleaning' and (len(self.standing_participants) != 2 or (*self.standing_participants, self.standing_method) not in self.cleaning_pairs):
            raise ValueError('standing cleaning must match declared scope')


@dataclass(frozen=True)
class ActorFixture(TimedFixture):
    actor_profiles: tuple[ActorProfile, ...] = ()
    actor_order: tuple[str, ...] = ()
    actors_version: str = 'actors-1'

    @property
    def locality_help(self):
        return ('Voluntary cooperation: ask <actor> to clean <surface> [using <tool>] [by wiping/scrubbing]; '
                'ask <actor> to assemble <arrangement>; ask <actor> to pause/resume/cancel work; '
                'ask <actor> about work; ask <actor> about <target> <facet>; ask <actor> for <object>.\n'
                'Tell <actor> that <target> residue is clear/present or moisture is wet/dry; statements remain attributed reports, not truth.\n'
                'Returning a task material requires the actor’s agreement and idle or paused work; active work may be busy. '
                'Requests require local communication and willingness. Acceptance does no physical work; '
                'eligible actors take at most one physical step during each later world interval. '
                'An agreement shows last communicated status; it is not remote live knowledge.\n' + super().locality_help)


def create_actor_fixture(*, actor_profiles=None, actor_order=None):
    timed = create_timed_fixture()
    layout, _, _, _ = water_layout()
    layout = replace(layout, people=tuple((*row[:3], 'work-bench' if row[0] == 'oren' else 'yard-tools' if row[0] == 'tali' else row[3]) for row in layout.people),
                     specialists=(*layout.specialists, 'timed', 'actors'))
    pairs = tuple((source, tool, method) for method, source, tool in timed.water_profile.allowed_pairs if method in {'wipe', 'scrub'})
    routes = tuple((identity(source), identity(target)) for source, _, target in layout.edges)
    if actor_profiles is None:
        actor_profiles = (
            ActorProfile(identity('oren'), cleaning_pairs=pairs, routes=routes,
                         standing_kind='cleaning', standing_method='wipe',
                         standing_participants=(identity('practice-panel'), identity('cleaning-cloth')), standing_place=identity('work-bench')),
            ActorProfile(identity('tali'), cleaning_pairs=pairs, routes=routes,
                         standing_kind='cleaning', standing_method='scrub',
                         standing_participants=(identity('sorting-board'), identity('cleaning-brush')), standing_place=identity('yard-tools')),
        )
    if type(actor_profiles) is not tuple or any(type(p) is not ActorProfile for p in actor_profiles):
        raise ValueError('immutable actor profiles required')
    ids = tuple(p.actor_id for p in actor_profiles)
    if len(set(ids)) != len(ids):
        raise ValueError('duplicate participation actor')
    actor_order = ids if actor_order is None else actor_order
    if type(actor_order) is not tuple or len(actor_order) != len(ids) or set(actor_order) != set(ids):
        raise ValueError('actor order must name each admitted actor once')
    actor_ids = {identity(row[0]) for row in layout.people}
    object_ids = {identity(row[0]) for row in layout.objects}
    places = {identity(p.key) for p in layout.places}
    for profile in actor_profiles:
        if profile.actor_id not in actor_ids or any(s not in object_ids or t not in object_ids or (m, s, t) not in timed.water_profile.allowed_pairs for s, t, m in profile.cleaning_pairs):
            raise ValueError('actor scope differs from declared people/materials')
        if not set(profile.assembly_names) <= {a.name for a in timed.assemblies}:
            raise ValueError('unknown assembly scope')
        if not set(profile.routes) <= set(routes) or (profile.standing_place is not None and profile.standing_place not in places):
            raise ValueError('actor route/activity place is not admitted')
    witness = {'actors': [asdict(p) for p in actor_profiles], 'order': actor_order,
               'actors_version': 'actors-1', 'timed_binding': timed.provenance.initial_state_digest,
               'environment': canonical_profile(timed.environment_profile), 'assemblies': [asdict(a) for a in timed.assemblies],
               'timing_version': timed.timing_version, 'trace_subjects': timed.trace_subjects}
    layout = replace(layout, version='actors-1-' + digest(witness)[:16])
    root = create_tarrow_fixture(layout=layout)
    inherited = {name: getattr(timed, name) for name in ('material_profile', 'water_profile', 'water_initial', 'environment_profile', 'assemblies', 'trace_subjects', 'timing_version')}
    return ActorFixture(**root.__dict__, **inherited, actor_profiles=actor_profiles, actor_order=actor_order)


def parse_actor_request(raw):
    text = ' '.join(raw.strip().casefold().split())
    match = re.fullmatch(r'tell (.+?) that (.+?) (residue|moisture) is (present|clear|wet|dry)', text)
    if match:
        return 'assertion', (match[1], match[2], match[3], match[4])
    match = re.fullmatch(r'ask (.+?) to clean (.+?)(?: using (.+?))?(?: by (wiping|scrubbing))?', text)
    if match:
        return 'cleaning', (match[1], match[2], match[3], {'wiping': 'wipe', 'scrubbing': 'scrub'}.get(match[4]))
    match = re.fullmatch(r'ask (.+?) to assemble (.+)', text)
    if match:
        return 'assembly', (match[1], match[2])
    match = re.fullmatch(r'ask (.+?) to (pause|resume|cancel) work', text)
    if match:
        return 'control', (match[1], match[2])
    match = re.fullmatch(r'ask (.+?) about work', text)
    if match:
        return 'status', (match[1],)
    match = re.fullmatch(r'ask (.+?) about (.+?) (residue|moisture|placement|assembly|trace|activity)', text)
    if match:
        return 'report', (match[1], match[2], match[3])
    return None


def execute_actor_locality_request(application, raw):
    parsed = parse_actor_request(raw)
    if parsed is None:
        return execute_timed_locality_request(application, raw)
    kind, args = parsed
    if kind == 'assertion':
        result = application.tell_actor(*args)
    elif kind == 'cleaning':
        result = application.request_cleaning(args[0], args[1], tool_reference=args[2], method=args[3])
    elif kind == 'assembly':
        result = application.request_assembly(*args)
    elif kind == 'control':
        result = application.participation_control(*args)
    elif kind == 'status':
        result = application.participation_status(*args)
    else:
        result = application.ask_report(*args)
    return 'actors', result
