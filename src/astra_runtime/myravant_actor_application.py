"""Approved #548 opt-in participation over retained physical and time owners.

This adapter orders owner procedures; it grants neither custody nor knowledge.
Prepared intents remain fixed for an interval, and every owner requalifies them.
"""
from dataclasses import asdict, replace
from types import SimpleNamespace

from astra_runtime.myravant_timed_application import TimedApplication
from astra_runtime.myravant_material_application import _transaction
from astra_runtime.domain.persistent_world_material import digest, placement
from astra_runtime.domain import persistent_world_actor_participation as participation
from astra_runtime.domain import persistent_world_actor_evidence as evidence
from astra_runtime.domain import persistent_world_continuing_work as work
from astra_runtime.domain import persistent_world_timed_environment as env
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.transaction_preview import create_transaction_preview
from astra_runtime.kernel.state_delta import create_state_delta_envelope
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime import myravant_actor_knowledge as knowledge
from astra_runtime.myravant_actor_physical import execute_actor_physical

CONTROLS=('request_cleaning','request_assembly','participation_control','participation_status','ask_report','tell_actor','look','inspect')
COMMUNICATION_CLASSES=('request','status','report','control')
ASSERTIONS={'residue':('present','clear'),'moisture':('wet','dry')}


class ActorApplication(TimedApplication):
    checkpoint_format='myravant.actor-time-material-owner-journal'
    replay_methods=(*TimedApplication.replay_methods,*CONTROLS)

    @staticmethod
    def default_fixture():
        from astra_runtime.myravant_tarrow_actors import create_actor_fixture
        return create_actor_fixture()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.participation_state=participation.ParticipationState()
        self.evidence_state=evidence.EvidenceState()
        self.actor_events=()
        self.communicated=()
        self.standing_considered=()
        self._validate_transaction()

    def _checkpoint_profile(self):
        return {'timed':super()._checkpoint_profile(),'actors':[asdict(p) for p in self.fixture.actor_profiles],
                'order':self.fixture.actor_order,'version':self.fixture.actors_version,
                'interval_policy':'prepare-at-start;passive;player;ordered-npcs;one-physical-step-1',
                'communication_policy':'same-lit-place;direct-character-placement;declared-class-1',
                'player_communication_classes':COMMUNICATION_CLASSES,'evidence_facets':tuple(sorted(knowledge.FACETS)),
                'reported_assertions':ASSERTIONS}

    def authoritative_digest(self):
        base=super().authoritative_digest()
        if not hasattr(self,'participation_state'):return base
        return digest({'timed':base,'participation':participation.canonical_state(self.participation_state),
                       'evidence':evidence.canonical_state(self.evidence_state),'events':self.actor_events,
                       'communicated':self.communicated,'standing':self.standing_considered})

    def _capture_transaction(self):
        return (super()._capture_transaction(),self.participation_state,self.evidence_state,
                self.actor_events,self.communicated,self.standing_considered)

    def _restore_transaction(self,snapshot):
        old,self.participation_state,self.evidence_state,self.actor_events,self.communicated,self.standing_considered=snapshot
        super()._restore_transaction(old)

    def _validate_transaction(self):
        super()._validate_transaction()
        if not hasattr(self,'participation_state'):return
        actors={p.actor_id for p in self.fixture.actor_profiles}
        if len(actors)!=len(self.fixture.actor_profiles) or set(self.fixture.actor_order)!=actors or len(self.fixture.actor_order)!=len(actors):
            raise ValueError('actor order must cover distinct declared profiles')
        ids={e.entity_id for e in self.state.representation.entities}
        known_actors={e.entity_id for e in self.state.representation.entities if e.classification=='character_or_creature'}
        if not actors<=known_actors:raise ValueError('unknown actor profile')
        receipts={e[0] for e in self.actor_events}
        receipts.update(t.receipt.receipt_id for t in self.runtime_state.logical_time_state.committed_transitions)
        receipts.update(i[4] for i in self.intervals if i[4])
        participation.canonical_state(self.participation_state,actor_ids=known_actors,participant_ids=ids,receipt_ids=receipts)
        evidence.canonical_state(self.evidence_state,actor_ids=known_actors,target_ids=ids,receipt_ids=receipts)
        for p in self.fixture.actor_profiles:
            participation.ParticipationProfile(p.actor_id,p.blocked_limit)
            if p.standing_kind:
                self._scope(p,p.standing_kind,p.standing_method,p.standing_participants,p.standing_place)
        for task in self.participation_state.records:
            self._scope(self.actor_profile(task.actor_id),task.kind,task.method,task.participants,task.place_id)
        tick=self.runtime_state.logical_time_state.logical_position
        if any(e.tick>tick for e in self.evidence_state.events):raise ValueError('future evidence')
        if len({e[0] for e in self.actor_events})!=len(self.actor_events):raise ValueError('duplicate actor receipt')

    def actor_profile(self,actor_id):
        if actor_id==self.fixture.player_entity_id:
            return SimpleNamespace(communication_classes=COMMUNICATION_CLASSES)
        found=[p for p in self.fixture.actor_profiles if p.actor_id==actor_id]
        if len(found)!=1:raise ValueError('That actor has no admitted participation profile.')
        return found[0]

    def _additional_owner_receipts(self):
        return tuple(e[0] for e in getattr(self,'actor_events',()))

    def _actor(self,reference):
        actor=self.fixture.resolve_actor_reference(reference)
        self.actor_profile(actor)
        return actor

    def _event(self,operation,actor,payload,*,receipt=None):
        token=digest([self.authoritative_digest(),len(self.actor_events),operation,actor,payload])[:28]
        rid=receipt or build_record_id('actor_receipt',token)
        self.actor_events=(*self.actor_events,(rid,operation,actor,payload,self.runtime_state.logical_time_state.logical_position))
        return rid

    def _metadata_result(self,pre,operation,actor,message):
        rid=self._event(operation,actor,message)
        token=digest([rid,pre])[:28]
        command=create_command_envelope(command_id='actor-control-'+token,command_type='interact',
            source_actor_id=self.fixture.player_entity_id,payload={'operation':operation,'addressed_actor_id':actor,'message':message})
        owner=('AFQR-10' if operation=='look' or operation.startswith('inspect:') else
               'AFQR-14' if operation in {'ask_report','tell_actor','participation_status'} else 'AFQR-11')
        preview=create_transaction_preview(preview_id=build_record_id('actor_preview',token),command=command,
            metadata={'semantic_owner':owner,'mutation_performed':False})
        delta=create_state_delta_envelope(delta_id=build_record_id('actor_delta',token),source_command_id=command.command_id,
            source_preview_id=preview.preview_id,affected_record_ids=(actor,),change_type='record_update',
            payload={'operation':operation,'receipt_id':rid},metadata={'semantic_owner':owner,'transition_owner':'AFQR-01'})
        return PlayApplicationResult(result_type='actor_participation',message=message,authoritative_changed=True,
            command_id=command.command_id,command_fingerprint=digest(command.to_dict()),
            receipt_id=rid,preview_id=preview.preview_id,state_delta_id=delta.delta_id,
            opportunity_evidence_id=build_record_id('evidence',token),pre_state_digest=pre,post_state_digest=self.authoritative_digest())

    def _scope(self,profile,kind,method,participants,place):
        if kind=='cleaning':
            if len(participants)!=2 or (*participants,method) not in profile.cleaning_pairs or method not in profile.methods:
                raise ValueError('That cleaning method or scope is unsupported by this profile.')
        elif kind=='assembly':
            a=self._assembly(method)
            if method not in profile.assembly_names or participants!=(a.left,a.right,a.fastener) or place!=a.place:
                raise ValueError('That arrangement is unsupported by this profile.')
        else:raise ValueError('Unsupported participation goal.')

    def _route(self,actor,kind):
        if not knowledge.communication_route(self,self.fixture.player_entity_id,actor,kind):
            raise ValueError('No qualified local communication route is available.')

    def _accept(self,actor,kind,method,participants,place,source):
        profile=self.actor_profile(actor)
        self._scope(profile,kind,method,participants,place)
        if not profile.willing:raise ValueError('The actor declines this scope of work.')
        try:
            previous=participation.selected(self.participation_state,actor)
            if previous.status in {'active','paused','blocked'}:raise ValueError('The actor is busy with selected work.')
        except participation.ParticipationRefusal:pass
        token=digest([self.authoritative_digest(),actor,source,kind,method,participants,len(self.actor_events)])[:28]
        rid=self._event('acceptance',actor,(source,kind,method,participants))
        clock=self.runtime_state.logical_time_state
        predecessor=clock.committed_transitions[-1].receipt.receipt_id if clock.committed_transitions else 'actor-genesis-'+self.fixture.actors_version
        record=participation.Participation(build_record_id('actor_task',token),actor,source,kind,method,participants,place,rid,predecessor,clock.logical_position)
        self.participation_state=participation.accept(self.participation_state,record,'accept-'+token,qualified=True)
        return record

    def _communicate_status(self,actor):
        task=participation.selected(self.participation_state,actor)
        self.communicated=(*self.communicated,(self.fixture.player_entity_id,task.task_id,task.status,len(task.contributions),self.runtime_state.logical_time_state.logical_position))
        return f'{self.fixture.entity_name(actor)} reports {task.status}: {task.kind}, {task.method}; {len(task.contributions)} own committed step(s).'

    def request_cleaning(self,actor_reference,surface_reference,tool_reference=None,method=None):
        pre=self.authoritative_digest()
        try:
            actor=self._actor(actor_reference);self._route(actor,'request')
            surface=self._resolve_visible_for_actor(actor,surface_reference)
            profile=self.actor_profile(actor)
            if method is not None and method not in {'wipe','scrub'}:raise ValueError('Unsupported explicit cleaning method.')
            tools=[self._resolve_visible_for_actor(actor,tool_reference)] if tool_reference else [t for s,t,m in profile.cleaning_pairs if s==surface and (method is None or method==m) and self._visible_for_actor(actor,t)]
            options=[(t,m) for s,t,m in profile.cleaning_pairs if s==surface and t in tools and (method is None or method==m)]
            if not options:raise ValueError('No declared visible method is available for that goal.')
            if method is None:
                qualified=[]
                for candidate_tool,candidate_method in options:
                    candidate=work.WorkTask('candidate',actor,'cleaning',candidate_method,(surface,candidate_tool),self._actor_place_id(actor))
                    try:
                        staged=self._fork()
                        for _ in range(8):
                            outcome,intent=staged._prepare_actor(candidate)
                            if outcome=='satisfied':qualified.append((candidate_tool,candidate_method));break
                            if outcome!='action':break
                            probe=staged._execute_actor(actor,intent)
                            if not probe.authoritative_changed:break
                            if intent[:2]==('water',candidate_method):
                                qualified.append((candidate_tool,candidate_method));break
                    except ValueError:pass
                if not qualified:raise ValueError('No currently qualified declared method is available for that goal.')
                options=qualified
            tool,chosen=options[0]
            self._accept(actor,'cleaning',chosen,(surface,tool),self._actor_place_id(actor),self.fixture.player_entity_id)
            message=self._communicate_status(actor)+f' Selected {chosen} using {self.fixture.entity_name(tool)}; no material has changed and no tool is reserved.'
        except ValueError as exc:return self._result(str(exc),failure='actor_request_unavailable')
        return self._metadata_result(pre,'request_cleaning',actor,message)

    def request_assembly(self,actor_reference,arrangement_reference):
        pre=self.authoritative_digest()
        try:
            actor=self._actor(actor_reference);self._route(actor,'request');a=self._assembly(arrangement_reference)
            if self._actor_place_id(actor)!=a.place:raise ValueError('The actor must inspect the local arrangement first.')
            for obj in (a.left,a.right,a.fastener):
                if not self._visible_for_actor(actor,obj):raise ValueError('Assembly participants are not perceptible.')
            self._accept(actor,'assembly',a.name,(a.left,a.right,a.fastener),a.place,self.fixture.player_entity_id)
            message=self._communicate_status(actor)+' Acceptance reserves no materials.'
        except ValueError as exc:return self._result(str(exc),failure='actor_request_unavailable')
        return self._metadata_result(pre,'request_assembly',actor,message)

    def participation_control(self,actor_reference,operation):
        pre=self.authoritative_digest()
        try:
            actor=self._actor(actor_reference);self._route(actor,'control')
            task=participation.selected(self.participation_state,actor)
            if task.source_actor_id!=self.fixture.player_entity_id:raise ValueError('This is the actor’s own activity; this request has no control grant.')
            if not self.actor_profile(actor).willing:raise ValueError('The actor no longer agrees to that participation.')
            if operation=='pause':self.participation_state=participation.pause(self.participation_state,actor)
            elif operation=='resume':self.participation_state=participation.resume(self.participation_state,actor,qualified=True)
            elif operation in {'cancel','abandon'}:self.participation_state=participation.withdraw(self.participation_state,actor,reason='actor accepted local cancellation')
            else:raise ValueError('Choose pause, resume or cancel.')
            message=self._communicate_status(actor)
        except ValueError as exc:return self._result(str(exc),failure='actor_control_unavailable')
        return self._metadata_result(pre,'participation_control',actor,message)

    def participation_status(self,actor_reference):
        pre=self.authoritative_digest()
        try:
            actor=self._actor(actor_reference)
            try:self._route(actor,'status')
            except ValueError:
                records=[r for r in self.communicated if r[0]==self.fixture.player_entity_id and any(t.task_id==r[1] and t.actor_id==actor for t in self.participation_state.records)]
                if not records:return self._result('No last communicated status is available.')
                r=records[-1]
                return self._result(f'Last communicated status: {r[2]}; {r[3]} own step(s), at interval {r[4]}. Current status is unavailable here.')
            message=self._communicate_status(actor)
        except ValueError as exc:return self._result(str(exc),failure='actor_status_unavailable')
        return self._metadata_result(pre,'participation_status',actor,message)

    def ask_report(self,actor_reference,target_reference,facet):
        pre=self.authoritative_digest()
        try:
            actor=self._actor(actor_reference);self._route(actor,'report')
            if facet not in {'residue','moisture','placement','assembly','trace','activity'}:raise ValueError('That topic is unsupported by this evidence profile.')
            target=self.fixture.resolve_object_reference(target_reference)
            event=evidence.latest(self.evidence_state,actor,target,facet)
            if event is None:return self._result('No retained evidence for that admitted topic; this does not describe the person’s wider knowledge.')
            rid=self._event('communication',actor,(target,facet,event.event_id))
            self.evidence_state=knowledge.report(self.evidence_state,actor,self.fixture.player_entity_id,target,facet,rid,self.runtime_state.logical_time_state.logical_position,qualified=True)
            origin=event.origin_tick if event.origin_tick is not None else event.tick
            value=event.value
            if facet=='placement' and isinstance(value,tuple):
                labels={'located_at':'at','carried_by':'carried by','contained_by':'inside','supported_by':'resting on','reserved_by':'reserved by'}
                value=labels.get(value[0],'related to')+' '+self.fixture.entity_name(value[1])
            elif isinstance(value,tuple):value=', '.join(value)
            source=(' (a statement from '+self.fixture.entity_name(event.source_actor_id)+')') if event.kind=='reported' else ''
            message=f'{self.fixture.entity_name(actor)} reports {event.kind} evidence{source} from interval {origin}: {value}. This is a report, not a fresh inspection.'
        except ValueError as exc:return self._result(str(exc),failure='actor_report_unavailable')
        return self._metadata_result(pre,'ask_report',actor,message)

    def tell_actor(self,actor_reference,target_reference,facet,value):
        pre=self.authoritative_digest()
        try:
            actor=self._actor(actor_reference);self._route(actor,'report')
            if value not in ASSERTIONS.get(facet,()):raise ValueError('That assertion is unsupported by this communication profile.')
            target=self.fixture.resolve_object_reference(target_reference)
            rid=self._event('player_assertion',self.fixture.player_entity_id,(actor,target,facet,value))
            event=evidence.EvidenceEvent(build_record_id('actor_evidence',digest([rid,actor])[:28]),actor,'reported',
                self.fixture.player_entity_id,target,facet,value,self.runtime_state.logical_time_state.logical_position,rid,
                'qualified-local-assertion;not-sensing-or-truth')
            self.evidence_state=evidence.record(self.evidence_state,event,qualified=True)
        except ValueError as exc:return self._result(str(exc),failure='actor_assertion_unavailable')
        return self._metadata_result(pre,'tell_actor',actor,'The actor received your statement as an attributed report; the material state is unchanged.')

    def _observe_all(self,receipt):
        tick=self.runtime_state.logical_time_state.logical_position
        for actor in (self.fixture.player_entity_id,*self.fixture.actor_order):
            self.evidence_state=knowledge.observe(self,self.evidence_state,actor,receipt,tick)

    def _standing(self):
        for actor in self.fixture.actor_order:
            if actor in self.standing_considered:continue
            # A request already selected this actor; no competing root job is queued.
            if any(t.actor_id==actor for t in self.participation_state.records):
                self.standing_considered=(*self.standing_considered,actor);continue
            p=self.actor_profile(actor)
            if not p.standing_kind:
                self.standing_considered=(*self.standing_considered,actor);continue
            if not p.willing:continue
            if not all(self._visible_for_actor(actor,o) for o in p.standing_participants):continue
            self._accept(actor,p.standing_kind,p.standing_method,p.standing_participants,p.standing_place,actor)
            self.standing_considered=(*self.standing_considered,actor)

    def _raw(self,name,*args,**kwargs):
        if name!='request_object_from_actor':return super()._raw(name,*args,**kwargs)
        try:
            actor=self._actor(args[0]);self._route(actor,'request')
            profile=self.actor_profile(actor)
            task=participation.selected(self.participation_state,actor)
            obj=self.fixture.resolve_object_reference(args[1])
            if not profile.willing or not profile.returns_task_materials:
                raise ValueError('The actor declines the return request.')
            if task.status in {'active','blocked'}:raise ValueError('The actor is busy; agree to pause or end the work first.')
            if obj not in task.participants:raise ValueError('That return is outside the agreed task-material scope.')
            return execute_actor_physical(self,actor,'give',obj,self.fixture.player_entity_id)
        except ValueError as exc:return self._result(str(exc),failure='actor_return_unavailable')

    def _goal_visible_complete(self,task):
        needed=task.participants[:1] if task.kind=='cleaning' else task.participants
        if self._actor_place_id(task.actor_id)!=task.place_id or not all(self._visible_for_actor(task.actor_id,x) for x in needed):return False
        return self._task_complete(task)

    def _need_custody(self,actor,obj):
        r=placement(self.state.representation,obj)
        if r.relation_type=='carried_by' and r.object_entity_id==actor:return None
        if self._visible_for_actor(actor,obj):
            if r.relation_type=='supported_by':return 'material','lift_from',(obj,r.object_entity_id)
            return ('physical','retrieve',(obj,r.object_entity_id)) if r.relation_type=='contained_by' else ('physical','pickup',(obj,))
        # Knowledge can select a known container, but never locate hidden supplies.
        last=evidence.latest(self.evidence_state,actor,obj,'placement')
        if last and isinstance(last.value,tuple) and len(last.value)==2 and last.value[0]=='contained_by':
            container=last.value[1]
            if self._visible_for_actor(actor,container):return 'physical','open',(container,)
        raise ValueError('The required material is not available in this actor’s context.')

    def _prepare_actor(self,task):
        actor=task.actor_id;p=self.actor_profile(actor)
        if not p.willing:return 'invalidated',None
        self._scope(p,task.kind,task.method,task.participants,task.place_id)
        here=self._actor_place_id(actor)
        if here!=task.place_id:
            if (here,task.place_id) in p.routes:return 'action',('physical','move',(task.place_id,))
            return 'blocked','No declared one-edge route reaches the task position.'
        if self._goal_visible_complete(task):return 'satisfied',None
        if task.kind=='cleaning':
            surface,tool=task.participants
            need=self._need_custody(actor,tool)
            if need:return 'action',need
            if task.method=='wipe' and dict(self.water_state.water)[tool]==0:
                vessels=[b for op,b,t in self.water_profile.allowed_pairs if op=='soak' and t==tool and self._visible_for_actor(actor,b)]
                for vessel in vessels:
                    intent=('water','soak',(vessel,tool))
                    if self._fork()._execute_actor(actor,intent).authoritative_changed:return 'action',intent
                raise ValueError('No qualified declared water source is available.')
            capacity=next(a.residue_capacity for a in self.water_profile.assets if a.id==tool)
            if dict(self.water_state.adhered)[tool]+dict(self.environment_state.deposits).get(tool,0)>=capacity:
                trays=[b for op,t,b in self.water_profile.allowed_pairs if op=='collect' and t==tool and self._visible_for_actor(actor,b)]
                for tray in trays:
                    intent=('water','collect',(tool,tray))
                    if self._fork()._execute_actor(actor,intent).authoritative_changed:return 'action',intent
                vessels=[b for op,t,b in self.water_profile.allowed_pairs if op=='rinse' and t==tool and self._visible_for_actor(actor,b)]
                for vessel in vessels:
                    intent=('water','rinse',(tool,vessel))
                    if self._fork()._execute_actor(actor,intent).authoritative_changed:return 'action',intent
                raise ValueError('No qualified residue recovery destination is available.')
            return 'action',('water',task.method,(surface,tool))
        a=self._assembly(task.method)
        for obj,support in ((a.left,a.support_left),(a.right,a.support_right)):
            if support is not None:
                r=placement(self.state.representation,obj)
                if (r.relation_type,r.object_entity_id)!=('supported_by',support):
                    need=self._need_custody(actor,obj)
                    return 'action',need or ('material','put_on',(obj,support))
        need=self._need_custody(actor,a.fastener)
        return 'action',need or ('material',a.method,(a.left,a.right,a.fastener))

    def _execute_actor(self,actor,intent):
        owner,operation,ids=intent
        if owner=='physical':return execute_actor_physical(self,actor,operation,*ids)
        names=tuple(self.fixture.entity_name(i) for i in ids)
        return getattr(self,owner+'_for_actor')(actor,operation,*names)

    def _interval(self,name,args=(),kwargs=None,contribution=False):
        kwargs=kwargs or {};before=self.authoritative_digest()
        if name!='wait':
            probe=self._fork()._raw(name,*args,**kwargs)
            if not probe.authoritative_changed:return probe
        self._standing()
        # Initial observation is qualified under each observer's actual context.
        start_receipt=self._event('interval_preparation',self.fixture.player_entity_id,(name,args))
        self._observe_all(start_receipt)
        prepared=[]
        returning_actor=self._actor(args[0]) if name=='request_object_from_actor' else None
        for actor in self.fixture.actor_order:
            if actor==returning_actor:continue
            try:task=participation.selected(self.participation_state,actor)
            except ValueError:continue
            if task.status not in {'active','blocked'}:continue
            try:outcome,intent=self._prepare_actor(task)
            except ValueError as exc:outcome,intent='blocked',str(exc)
            prepared.append((actor,outcome,intent))
        clock,environment_before=self._clock_interval()
        self._observe_all(clock.receipt_id)
        actual=clock if name=='wait' else self._raw(name,*args,**kwargs)
        interrupted=name!='wait' and not actual.authoritative_changed
        action_receipt=None
        if interrupted:
            if contribution:self.work_state=work.block(self.work_state,actual.message)
            actual=replace(clock,result_type='timed_action_interrupted',message='Time passed, but the action was interrupted: '+actual.message,
                           failure_class='timed_action_interrupted',receipt_id=build_record_id('interval_receipt',digest([clock.receipt_id,name,args])[:28]))
        elif name!='wait':
            action_receipt=actual.receipt_id;self._trace_action(name,args,actual)
            if contribution:self.work_state=work.record_contribution(self.work_state,actual.receipt_id,completed=self._task_complete(work.selected(self.work_state)))
            target=self.fixture.player_entity_id
            for reference in args:
                if type(reference) is str:
                    try:target=self.fixture.resolve_object_reference(reference);break
                    except ValueError:pass
            performer=returning_actor or self.fixture.player_entity_id
            self.evidence_state=knowledge.performed(self.evidence_state,performer,target,'activity',name,actual.receipt_id,self.runtime_state.logical_time_state.logical_position)
            if returning_actor:self._event('physical_return',returning_actor,(target,self.fixture.player_entity_id),receipt=actual.receipt_id)
            self._observe_all(actual.receipt_id)
        tick=self.runtime_state.logical_time_state.logical_position
        for actor,outcome,intent in prepared:
            task=participation.selected(self.participation_state,actor);p=self.actor_profile(actor)
            receipt=None;complete=False;reason=None
            if not p.willing:outcome='invalidated';reason='continued consent is unavailable'
            elif self._goal_visible_complete(task):outcome='satisfied';reason='qualified local goal is already satisfied'
            elif outcome=='satisfied':outcome='blocked';reason='The prepared satisfied goal changed before resolution.'
            elif outcome=='action':
                result=self._execute_actor(actor,intent)
                if result.authoritative_changed:
                    outcome='contributed';receipt=result.receipt_id;complete=self._goal_visible_complete(task)
                    self._event('physical_contribution',actor,intent,receipt=receipt)
                    target=task.participants[0]
                    self.evidence_state=knowledge.performed(self.evidence_state,actor,target,'activity',intent[1],receipt,tick)
                    owner,op,ids=intent
                    if owner in {'water','material'}:self._trace_action(owner,(op,*(self.fixture.entity_name(x) for x in ids)),result)
                    self._observe_all(receipt)
                else:outcome='blocked';reason=result.message
            elif outcome=='blocked':reason=intent
            self.participation_state=participation.resolve_due(self.participation_state,actor,clock.receipt_id,tick,
                outcome=outcome,qualified=True,profile=participation.ParticipationProfile(actor,p.blocked_limit),
                receipt_id=receipt,completed=complete,reason=reason)
            self._event('due_resolution',actor,(task.task_id,clock.receipt_id,outcome,receipt,reason))
        self.work_state=work.move_outside(self.work_state,self.current_place_id())
        self.intervals=(*self.intervals,(tick,clock.receipt_id,environment_before,digest(env.canonical_environment(self.environment_state)),action_receipt,name,interrupted))
        return replace(actual,authoritative_changed=True,pre_state_digest=before,post_state_digest=self.authoritative_digest(),
                       logical_time_before=tick-1,logical_time_after=tick,due_process_ref=clock.receipt_id)

    def _observed_result(self,result,operation):
        if result.failure_class:return result
        pre=self.authoritative_digest();rid=self._event('player_observation',self.fixture.player_entity_id,operation)
        self.evidence_state=knowledge.observe(self,self.evidence_state,self.fixture.player_entity_id,rid,self.runtime_state.logical_time_state.logical_position)
        receipt=self._metadata_result(pre,operation,self.fixture.player_entity_id,'Qualified observation retained.')
        return replace(receipt,message=result.message,view=result.view,result_type=result.result_type)

    def look(self):return self._observed_result(super().look(),'look')
    def inspect(self,reference):return self._observed_result(super().inspect(reference),'inspect:'+reference)


for _name in CONTROLS:
    setattr(ActorApplication,_name,_transaction(getattr(ActorApplication,_name),_name))
