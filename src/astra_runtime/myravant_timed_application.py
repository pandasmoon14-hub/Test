"""#546 interval composition over existing logical-time and material owners.

Speculative owner execution uses a shallow isolated holder over immutable state,
with persistence disabled; it supplies current qualification without committing
on the live holder. After the passive interval the original owner requalifies.
"""
from copy import copy
from dataclasses import asdict, replace
from functools import wraps
from fractions import Fraction
import re

from astra_runtime.myravant_water_application import WaterApplication
from astra_runtime.myravant_material_application import _transaction, JOURNALED
from astra_runtime.myravant_play_application import MyravantPlayApplication, PlayApplicationResult
from astra_runtime.domain.persistent_world_material import placement, effective_place, digest
from astra_runtime.domain import persistent_world_continuing_work as work
from astra_runtime.domain import persistent_world_timed_environment as env
from astra_runtime.domain.persistent_world_water_cleaning import total_water,total_residue
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.transaction_preview import create_transaction_preview
from astra_runtime.kernel.state_delta import create_state_delta_envelope

PHYSICAL=tuple(name for name in (*JOURNALED,'water') if name!='wait')
CONTROL=('start_cleaning','start_assembly','task_control')


class TimedApplication(WaterApplication):
    checkpoint_format='myravant.timed-material-owner-journal'
    replay_methods=(*PHYSICAL,'wait','work_step',*CONTROL)

    @staticmethod
    def default_fixture():
        from astra_runtime.myravant_tarrow_time import create_timed_fixture
        return create_timed_fixture()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.environment_profile=self.fixture.environment_profile
        self.environment_state=env.initial_environment(self.environment_profile)
        self.work_state=work.WorkState()
        self.intervals=()
        self.condition_events=()
        self._timed_inside=False
        self._validate_transaction()

    def _checkpoint_profile(self):
        p=super()._checkpoint_profile()
        return {'water_binding':p,'environment':env.canonical_profile(self.fixture.environment_profile),
                'assemblies':[asdict(a) for a in self.fixture.assemblies],
                'trace_subjects':self.fixture.trace_subjects,'timing_version':self.fixture.timing_version}

    def authoritative_digest(self):
        return digest({'water':super().authoritative_digest(),'environment':env.canonical_environment(self.environment_state),
                       'work':work.canonical_state(self.work_state),'intervals':self.intervals,'conditions':self.condition_events})

    def _capture_transaction(self):
        return super()._capture_transaction(),self.environment_state,self.work_state,self.intervals,self.condition_events

    def _restore_transaction(self,snapshot):
        old,self.environment_state,self.work_state,self.intervals,self.condition_events=snapshot
        super()._restore_transaction(old)

    def _validate_transaction(self):
        super()._validate_transaction()
        if not hasattr(self,'environment_state'):
            return
        env.validate_environment(self.water_state,self.environment_state,self.environment_profile)
        rep=self.state.representation
        ids={e.entity_id for e in rep.entities}
        objects={e.entity_id for e in rep.entities if e.classification=='object'}
        places={e.entity_id for e in rep.entities if e.classification=='place'}
        if not set(self.environment_profile.absorbents)<=objects or {p for p,_,_ in self.environment_profile.exposures}!=places:
            raise ValueError('environment profile must bind current objects and positions')
        if not set(self.fixture.trace_subjects)<=objects or len(set(self.fixture.trace_subjects))!=len(self.fixture.trace_subjects):
            raise ValueError('invalid trace declaration')
        for a in self.fixture.assemblies:
            if a.place not in places or a.method not in {'tie','fasten'} or not {a.left,a.right,a.support_left,a.fastener}<=objects or (a.support_right is not None and a.support_right not in objects):
                raise ValueError('invalid assembly declaration')
            if (a.left,a.right,a.fastener,a.method) not in self.material_profile.fastening_pairs or (a.left,a.support_left) not in self.material_profile.support_pairs or (a.support_right is not None and (a.right,a.support_right) not in self.material_profile.support_pairs):
                raise ValueError('assembly differs from owner qualifications')
        if len({a.name for a in self.fixture.assemblies})!=len(self.fixture.assemblies):raise ValueError('duplicate assembly names')
        clock=self.runtime_state.logical_time_state
        receipts={t.receipt.receipt_id for t in clock.committed_transitions}
        receipts.update(i[4] for i in self.intervals if i[4])
        receipts.update(getattr(self,'_additional_owner_receipts',lambda:())())
        work.canonical_state(self.work_state,participant_ids=ids,receipt_ids=receipts)
        for task in self.work_state.tasks:
            if task.actor_id!=self.fixture.player_entity_id or task.place_id not in places:
                raise ValueError('unqualified work actor or position')
            if task.kind=='cleaning':
                if len(task.participants)!=2 or (task.method,*task.participants) not in self.water_profile.allowed_pairs or task.method not in {'wipe','scrub'}:
                    raise ValueError('unqualified cleaning declaration')
            else:
                a=self._assembly(task.method)
                if task.participants!=(a.left,a.right,a.fastener) or task.place_id!=a.place:
                    raise ValueError('assembly declaration differs from profile')
        if len(self.intervals)!=clock.logical_position or tuple(i[0] for i in self.intervals)!=tuple(range(1,clock.logical_position+1)):
            raise ValueError('interval history differs from clock')
        previous=digest(env.canonical_environment(env.initial_environment(self.environment_profile)))
        for interval,transition in zip(self.intervals,clock.committed_transitions):
            if interval[1]!=transition.receipt.receipt_id or interval[2]!=previous:
                raise ValueError('interval owner receipt or environment chronology mismatch')
            previous=interval[3]
        if previous!=digest(env.canonical_environment(self.environment_state)):
            raise ValueError('final environment lacks interval attribution')
        expected=[]
        for transition in clock.committed_transitions:
            for due,place,rate,label in self.environment_profile.schedule:
                if due==transition.receipt.post_position:
                    rid=build_record_id('environment_condition',digest([transition.receipt.receipt_id,due,place,str(rate),label])[:28])
                    expected.append((due,place,str(rate),label,rid,transition.receipt.receipt_id))
        if tuple(expected)!=self.condition_events:raise ValueError('condition history differs from time/profile')
        for t in self.environment_state.traces:
            if t.subject not in objects or t.place not in places or not 1<=t.tick<=clock.logical_position or t.receipt not in receipts or t.kind not in {'wet','wiped','brushed','fastened','drying'}:
                raise ValueError('unattributed physical trace')
        water=total_water(self.water_state)+sum(dict(self.environment_state.evaporated).values())
        soil=total_residue(self.water_state)+sum(dict(self.environment_state.deposits).values())
        if water!=total_water(self.fixture.water_initial) or soil!=total_residue(self.fixture.water_initial):
            raise ValueError('combined material conservation failed')

    def _prepare_water_transition(self,operation,participants,amount):
        return env.execute_with_deposits(self.water_state,self.environment_state,self.water_profile,operation,participants,amount)

    def _install_water_transition(self,candidate,auxiliary):
        self.water_state,self.environment_state=candidate,auxiliary

    def _fork(self):
        staged=copy(self)
        staged.checkpoint_path=None
        staged._in_transaction=True
        staged._timed_inside=True
        return staged

    def _raw(self,name,*args,**kwargs):
        return getattr(WaterApplication,name)(self,*args,**kwargs)

    def _exposures(self):
        rep=self.state.representation
        def exposed(obj,seen=()):
            if obj in seen:raise ValueError('cyclic exposure placement')
            r=placement(rep,obj)
            if r.relation_type=='located_at':return r.object_entity_id
            if r.relation_type=='contained_by':
                opened=self.object_open_state(r.object_entity_id)
                if opened is None or opened.state!='open':return None
            if r.relation_type in {'carried_by','supported_by','contained_by','reserved_by'}:
                return exposed(r.object_entity_id,(*seen,obj))
            return None
        return {obj:exposed(obj) for obj in self.environment_profile.absorbents}

    def _clock_interval(self):
        exposures=self._exposures()
        before=digest(env.canonical_environment(self.environment_state))
        result=MyravantPlayApplication.wait(self)
        if not result.authoritative_changed:raise ValueError('qualified logical interval failed')
        tick=self.runtime_state.logical_time_state.logical_position
        self.water_state,self.environment_state=env.advance_environment(self.water_state,self.environment_state,self.environment_profile,exposures,tick,result.receipt_id)
        for due,place,rate,label in self.environment_profile.schedule:
            if due==tick:
                rid=build_record_id('environment_condition',digest([result.receipt_id,due,place,str(rate),label])[:28])
                self.condition_events=(*self.condition_events,(due,place,str(rate),label,rid,result.receipt_id))
        return result,before

    def _trace_action(self,name,args,result):
        kind=None;subject=None
        if name=='water' and args:
            operation=args[0]
            if operation in {'wipe','scrub'}:
                subject=self.fixture.resolve_object_reference(args[1]);kind='wiped' if operation=='wipe' else 'brushed'
            elif operation in {'soak','spill','blot','press'}:
                subject=self.fixture.resolve_object_reference(args[2]);kind='wet'
        elif name=='material' and args and args[0] in {'tie','fasten'}:
            subject=self.fixture.resolve_object_reference(args[1]);kind='fastened'
        if kind and subject in self.fixture.trace_subjects:
            self.environment_state=env.add_trace(self.environment_state,subject,kind,result.receipt_id,
                self.runtime_state.logical_time_state.logical_position,effective_place(self.state.representation,subject))

    def _interval(self,name,args=(),kwargs=None,contribution=False):
        kwargs=kwargs or {}
        before=self.authoritative_digest()
        if name!='wait':
            probe=self._fork()._raw(name,*args,**kwargs)
            if not probe.authoritative_changed:
                return probe
        clock,environment_before=self._clock_interval()
        actual=clock if name=='wait' else self._raw(name,*args,**kwargs)
        interrupted=name!='wait' and not actual.authoritative_changed
        if interrupted:
            if contribution:self.work_state=work.block(self.work_state,actual.message)
            # Time/passive effects happened even though the active contribution lost opportunity.
            token=digest([clock.receipt_id,name,args,kwargs,'interrupted'])[:28]
            actual=replace(clock,result_type='timed_action_interrupted',message='Time passed, but the action was interrupted: '+actual.message,
                failure_class='timed_action_interrupted',receipt_id=build_record_id('interval_receipt',token))
            action_receipt=None
        else:
            action_receipt=None if name=='wait' else actual.receipt_id
            if name!='wait':self._trace_action(name,args,actual)
            if contribution:
                self.work_state=work.record_contribution(self.work_state,actual.receipt_id,completed=self._task_complete(work.selected(self.work_state)))
        self.work_state=work.move_outside(self.work_state,self.current_place_id())
        tick=self.runtime_state.logical_time_state.logical_position
        environment_after=digest(env.canonical_environment(self.environment_state))
        self.intervals=(*self.intervals,(tick,clock.receipt_id,environment_before,environment_after,action_receipt,name,interrupted))
        return replace(actual,authoritative_changed=True,pre_state_digest=before,post_state_digest=self.authoritative_digest(),
                       logical_time_before=tick-1,logical_time_after=tick,due_process_ref=clock.receipt_id)

    def wait(self):
        return self._interval('wait')

    def _assembly(self,name):
        matches=[a for a in self.fixture.assemblies if a.name==name.strip().casefold()]
        if len(matches)!=1:raise ValueError('Specify a declared assembly arrangement.')
        return matches[0]

    def _task_action(self,task):
        if task.place_id!=self.current_place_id():raise ValueError('Return to the work position before continuing.')
        if task.kind=='cleaning':
            return 'water',(task.method,*(self.fixture.entity_name(x) for x in task.participants)),{}
        a=self._assembly(task.method)
        rep=self.state.representation
        for obj,support in ((a.left,a.support_left),(a.right,a.support_right)):
            if support is not None:
                r=placement(rep,obj)
                if (r.relation_type,r.object_entity_id)!=('supported_by',support):
                    return 'material',('put_on',self.fixture.entity_name(obj),self.fixture.entity_name(support)),{}
        if any((c.left,c.right,c.fastener,c.method)==(a.left,a.right,a.fastener,a.method) for c in self.connections):
            raise ValueError('The actual arrangement is already complete.')
        return 'material',(a.method,self.fixture.entity_name(a.left),self.fixture.entity_name(a.right),self.fixture.entity_name(a.fastener)),{}

    def _task_complete(self,task):
        if task.kind=='cleaning':return dict(self.water_state.adhered)[task.participants[0]]==0
        a=self._assembly(task.method)
        supports=all(s is None or (placement(self.state.representation,o).relation_type,placement(self.state.representation,o).object_entity_id)==('supported_by',s)
                     for o,s in ((a.left,a.support_left),(a.right,a.support_right)))
        return supports and any((c.left,c.right,c.fastener,c.method)==(a.left,a.right,a.fastener,a.method) for c in self.connections)

    def _qualified_task(self,task):
        name,args,kwargs=self._task_action(task)
        probe=self._fork()._raw(name,*args,**kwargs)
        if not probe.authoritative_changed:raise ValueError(probe.message)
        return name,args,kwargs

    def _control_receipt(self,operation,pre,message):
        command_id=f'terminal-work-{len(self.journal)+1:06d}'
        payload={'operation':operation,'work':work.canonical_state(self.work_state)}
        token=digest([command_id,pre,payload])[:28]
        command=create_command_envelope(command_id=command_id,command_type='interact',source_actor_id=self.fixture.player_entity_id,payload=payload)
        preview=create_transaction_preview(preview_id=build_record_id('work_preview',token),command=command,metadata={'semantic_owner':'AFQR-03'})
        delta=create_state_delta_envelope(delta_id=build_record_id('work_delta',token),source_command_id=command_id,
            source_preview_id=preview.preview_id,affected_record_ids=(self.fixture.player_entity_id,),change_type='record_update',payload=payload,metadata={'semantic_owner':'AFQR-03'})
        return PlayApplicationResult(result_type='work_declaration',message=message,authoritative_changed=True,
            command_id=command_id,command_fingerprint=digest(command.to_dict()),preview_id=preview.preview_id,state_delta_id=delta.delta_id,
            receipt_id=build_record_id('work_receipt',token),opportunity_evidence_id=build_record_id('evidence','work-opportunity-'+token),
            pre_state_digest=pre,post_state_digest=self.authoritative_digest())

    def start_cleaning(self,surface_reference,tool_reference,*,method='wipe'):
        pre=self.authoritative_digest()
        try:
            participants=tuple(self._resolve_visible(x) for x in (surface_reference,tool_reference))
            if method not in {'wipe','scrub'}:raise ValueError('Choose wiping or scrubbing explicitly.')
            task=work.WorkTask(build_record_id('work_task',digest([pre,len(self.journal),'cleaning',participants,method])[:28]),self.fixture.player_entity_id,'cleaning',method,participants,self.current_place_id())
            self._qualified_task(task)
            candidate=work.start(self.work_state,task)
        except ValueError as exc:return self._result(str(exc),failure='work_declaration_unavailable')
        self.work_state=candidate
        return self._control_receipt('start_cleaning',pre,'Cleaning work started; no material has changed yet.')

    def start_assembly(self,arrangement_reference):
        pre=self.authoritative_digest()
        try:
            a=self._assembly(arrangement_reference)
            if self.current_place_id()!=a.place:raise ValueError('That arrangement is not available at this work position.')
            for obj in (a.left,a.right,a.fastener):self._resolve_visible(self.fixture.entity_name(obj))
            participants=(a.left,a.right,a.fastener)
            task=work.WorkTask(build_record_id('work_task',digest([pre,len(self.journal),'assembly',a.name])[:28]),self.fixture.player_entity_id,'assembly',a.name,participants,a.place)
            self._qualified_task(task)
            candidate=work.start(self.work_state,task)
        except ValueError as exc:return self._result(str(exc),failure='work_declaration_unavailable')
        self.work_state=candidate
        return self._control_receipt('start_assembly',pre,'Assembly work started; contribute one missing material step at a time.')

    def task_control(self,operation):
        pre=self.authoritative_digest()
        try:
            if operation=='pause':candidate=work.pause(self.work_state)
            elif operation=='abandon':candidate=work.abandon(self.work_state)
            elif operation=='resume':
                task=work.selected(self.work_state);self._qualified_task(task)
                candidate=work.resume(self.work_state,qualified=True)
            else:raise ValueError('Choose pause, resume or abandon.')
        except ValueError as exc:return self._result(str(exc),failure='work_control_unavailable')
        self.work_state=candidate
        return self._control_receipt(operation,pre,f'Work {operation} committed; actual material progress is preserved.')

    def work_step(self):
        try:
            task=work.selected(self.work_state)
            if task.status!='active':raise ValueError('Resume eligible work before contributing.')
            name,args,kwargs=self._qualified_task(task)
        except ValueError as exc:return self._result(str(exc),failure='work_opportunity_unavailable')
        return self._interval(name,args,kwargs,contribution=True)

    def task_status(self):
        try:
            task=work.selected(self.work_state)
        except ValueError:return self._result('No work is selected.')
        actual='goal satisfied' if self._task_complete(task) else 'goal unfinished'
        return self._result(f'Work: {task.kind}; {task.status}; {actual}; {len(task.contributions)} contributed step(s).')

    def advance_duration(self,*,kind,steps):
        results=list(self.duration_results(kind,steps))
        return results[-1] if results else self._result('The selected work is already complete.')

    def duration_results(self,kind,steps):
        if kind not in {'wait','work'} or type(steps) is not int or not 1<=steps<=32:
            yield self._result('Choose wait/work with a whole duration of 1..32 steps.',failure='duration_unavailable');return
        for _ in range(steps):
            if kind=='work':
                try:
                    if work.selected(self.work_state).status=='completed':return
                except ValueError:pass
            result=self.wait() if kind=='wait' else self.work_step()
            yield result
            if result.failure_class:return

    def interval_results_for_request(self,raw):
        parsed=parse_timed(raw)
        return self.duration_results(parsed[1][0],parsed[1][1]) if parsed and parsed[0]=='duration' else None

    def inspect(self,entity_reference):
        if entity_reference.strip().casefold()=='work':return self.task_status()
        result=super().inspect(entity_reference)
        try:obj=self.fixture.resolve_object_reference(entity_reference)
        except ValueError:return result
        if result.failure_class or not self._visible(obj):return result
        from astra_runtime.myravant_terminal import _render_inspection_view
        text=_render_inspection_view(result.view) if result.view is not None else result.message
        if obj in dict(self.environment_state.deposits):text+=f'\nDeposited residue: {dict(self.environment_state.deposits)[obj]} unit(s).'
        kinds=tuple(dict.fromkeys(t.kind for t in self.environment_state.traces if t.subject==obj))
        descriptions={'wiped':'A wiped patch is visible.','brushed':'Brush patterns are visible.','fastened':'A declared fastening mark is visible.','wet':'A moisture trace is visible.','drying':'A drying trace is visible.'}
        visible=[descriptions[k] for k in kinds if k in descriptions]
        if visible:text+='\nPhysical traces: '+' '.join(visible)
        return replace(result,view=None,message=text)

    def look(self):
        result=super().look()
        place=self.current_place_id();rates={p:(r,label) for p,r,label in self.environment_profile.exposures}
        tick=self.runtime_state.logical_time_state.logical_position
        for due,p,r,label in self.environment_profile.schedule:
            if due<=tick:rates[p]=(r,label)
        # Existing visual owner decides whether this position can be observed.
        if self.fixture.ambient_visual_condition_for(place)=='sufficient' or self._bounded_local_light_available():
            result=replace(result,view=replace(result.view,description=result.view.description+'\nExposure: '+rates[place][1]+'.'))
        return result


def _timed_physical(method,name):
    @wraps(method)
    def run(self,*args,**kwargs):
        if self._timed_inside:return method(self,*args,**kwargs)
        self._timed_inside=True
        try:return self._interval(name,args,kwargs)
        finally:self._timed_inside=False
    return _transaction(run,name)


for _name in PHYSICAL:
    setattr(TimedApplication,_name,_timed_physical(getattr(WaterApplication,_name),_name))
for _name in ('wait','work_step',*CONTROL):
    _original=getattr(TimedApplication,_name)
    if _name in {'wait','work_step'}:
        def _inside(method):
            @wraps(method)
            def call(self,*args,**kwargs):
                previous=self._timed_inside;self._timed_inside=True
                try:return method(self,*args,**kwargs)
                finally:self._timed_inside=previous
            return call
        _original=_inside(_original)
    setattr(TimedApplication,_name,_transaction(_original,_name))


def parse_timed(raw):
    text=' '.join(raw.strip().casefold().split())
    m=re.fullmatch(r'(wait|work)(?: ([0-9]+) steps?)?',text)
    if m:return 'duration',(m[1],int(m[2]) if m[2] and len(m[2])<4 else 1 if m[2] is None else 0)
    m=re.fullmatch(r'start cleaning (.+?) using (.+?)(?: by (wiping|scrubbing))?',text)
    if m:return 'start_cleaning',(m[1],m[2], 'scrub' if m[3]=='scrubbing' else 'wipe')
    m=re.fullmatch(r'start assembling (.+)',text)
    if m:return 'start_assembly',(m[1],)
    m=re.fullmatch(r'(pause|resume|abandon) work',text)
    if m:return 'control',(m[1],)
    if text=='inspect work':return 'status',()
    return None


def execute_timed_request(application,raw):
    parsed=parse_timed(raw)
    if parsed is None:return None
    op,args=parsed
    if op=='duration':result=application.advance_duration(kind=args[0],steps=args[1])
    elif op=='start_cleaning':result=application.start_cleaning(args[0],args[1],method=args[2])
    elif op=='start_assembly':result=application.start_assembly(*args)
    elif op=='control':result=application.task_control(*args)
    else:result=application.task_status()
    return 'timed',result
