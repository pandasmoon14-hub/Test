"""Approved #546 opt-in timing/exposure/work development profiles."""
from dataclasses import asdict, dataclass, replace
from fractions import Fraction

from astra_runtime.myravant_tarrow import create_tarrow_fixture, identity
from astra_runtime.myravant_tarrow_water import WaterFixture, water_layout, execute_water_locality_request
from astra_runtime.domain.persistent_world_material import digest
from astra_runtime.domain.persistent_world_timed_environment import TimedEnvironmentProfile, canonical_profile


@dataclass(frozen=True)
class AssemblyProfile:
    name: str
    place: str
    left: str
    right: str
    support_left: str
    support_right: str | None
    fastener: str
    method: str


@dataclass(frozen=True)
class TimedFixture(WaterFixture):
    environment_profile: TimedEnvironmentProfile | None = None
    assemblies: tuple[AssemblyProfile, ...] = ()
    trace_subjects: tuple[str, ...] = ()
    timing_version: str = 'physical-interval-1'

    @property
    def locality_help(self):
        return ('Time and work: wait [N steps]; start cleaning <surface> using <tool> by wiping/scrubbing; '
                'start assembling workshop assembly/passage barrier/visual screen; work [N steps]; '
                'pause work; resume work; abandon work; inspect work. Durations are 1..32 separately durable intervals.\n'
                'Physical changes take one development interval; observations and work declarations take none. '
                'Gather assembly materials first. Work contributes only when explicitly requested. '
                'Aired/sheltered exposure dries qualified cloth; closed containers pause drying. '
                'Inspect local objects for physical traces; they do not identify a culprit or an event time.\n' + super().locality_help)


def create_timed_fixture():
    layout, material, water, initial = water_layout()
    environment = TimedEnvironmentProfile((identity('cleaning-cloth'),),
        tuple((identity(p.key),Fraction(1,2) if p.key=='yard-tools' else Fraction(1,4),
               'aired' if p.key=='yard-tools' else 'sheltered') for p in layout.places),
        ((12,identity('yard-tools'),Fraction(1,4),'sheltered'),))
    rows=(('workshop assembly','work-bench','repair-board','repair-peg','bench','bench','repair-cord','tie'),
          ('passage barrier','yard-tools','barrier-board','barrier-crossbar','trestle','trestle','barrier-cord','tie'),
          ('visual screen','notice-recess','screen-cloth','notice-board','document-box',None,'screen-cord','tie'))
    assemblies=tuple(AssemblyProfile(name,identity(place),identity(left),identity(right),identity(sl),identity(sr) if sr else None,identity(fastener),method)
                     for name,place,left,right,sl,sr,fastener,method in rows)
    subjects=tuple(identity(k) for k in ('practice-panel','sorting-board','repair-board','barrier-board','screen-cloth','cleaning-cloth'))
    witness={'environment':canonical_profile(environment),'assemblies':[asdict(a) for a in assemblies],
             'trace_subjects':subjects,'timing':'physical-interval-1','water_binding':layout.version}
    layout=replace(layout,version='time-1-'+digest(witness)[:16],specialists=(*layout.specialists,'timed'))
    fixture=create_tarrow_fixture(layout=layout)
    return TimedFixture(**fixture.__dict__,material_profile=material,water_profile=water,water_initial=initial,
                        environment_profile=environment,assemblies=assemblies,trace_subjects=subjects)


def execute_timed_locality_request(application,raw):
    from astra_runtime.myravant_timed_application import execute_timed_request
    return execute_timed_request(application,raw) or execute_water_locality_request(application,raw)
