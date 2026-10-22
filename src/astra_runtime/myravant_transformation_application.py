"""Opt-in #555 material transformation over existing actor, time and RT-010 owners.

No new clock, universal crafting manager, invented yields, or retroactive saves.
"""
from dataclasses import asdict, replace

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_material_application import _transaction
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.domain.persistent_world_material import MaterialError, digest, placement
from astra_runtime.domain.persistent_world_material import (
    TransformationWork, initial_state, role, validate_profile, validate_state, record_stage)
from astra_runtime.domain import persistent_world_actor_participation as participation
from astra_runtime import myravant_actor_knowledge as knowledge
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.transaction_preview import create_transaction_preview
from astra_runtime.kernel.state_delta import create_state_delta_envelope
from astra_runtime.kernel.record_identity import build_record_id


class TransformationApplication(ActorApplication):
    checkpoint_format = "myravant.transformation-actor-time-material-owner-journal"
    replay_methods = (*ActorApplication.replay_methods,
                      "begin_transformation","control_transformation","contribute_transformation")

    @staticmethod
    def default_fixture():
        from astra_runtime.myravant_tarrow_transformation import create_transformation_fixture
        return create_transformation_fixture()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transform_profile = self.fixture.transformation_profile
        self.transform_state = initial_state(self.transform_profile)
        self._validate_transaction()

    def _checkpoint_profile(self):
        return {"actors":super()._checkpoint_profile(),
                "transformation":asdict(self.fixture.transformation_profile),
                "policy":"whole-part-two-routes-one-repurpose-one-clock-1"}

    def authoritative_digest(self):
        previous = super().authoritative_digest()
        if not hasattr(self,"transform_state"):return previous
        return digest({"actors":previous,"transformation":asdict(self.transform_state),
                       "profile":asdict(self.transform_profile)})

    def _capture_transaction(self):
        previous=super()._capture_transaction()
        return (previous,self.transform_state) if hasattr(self,"transform_state") else previous

    def _restore_transaction(self,snapshot):
        previous,self.transform_state=snapshot
        super()._restore_transaction(previous)

    def _replacement_committed(self):
        p=self.transform_profile
        return any(row[0]=="replace" and row[2]==p.old and row[3]==p.spare
                   and row[4]==2 and row[6] is not None
                   for row in self.transform_state.lineage)

    def _validate_transaction(self):
        super()._validate_transaction()
        if not hasattr(self,"transform_state"):return
        p=self.transform_profile
        validate_profile(p,self.state.representation,self.material_profile)
        actors={self.fixture.player_entity_id,*self.fixture.actor_order}
        receipts={a[0] for a in self.actor_events}
        validate_state(self.transform_state,p,actors,receipts)
        for c in self.connections:
            if c.left==p.barrier_board and c.right==p.old and role(self.transform_state,p.old)!="fit":
                raise MaterialError("unfit component cannot form the barrier connection")
            if c.left==p.barrier_board and c.right==p.spare and not self._replacement_committed():
                raise MaterialError("spare barrier connection requires completed physical replacement")
            if c.left==p.repair_board and c.right==p.old and role(self.transform_state,p.old)!="spacer":
                raise MaterialError("unrepurposed component cannot form workshop connection")

    def _accept(self, actor, kind, method, participants, place, source):
        task=self.transform_state.work if hasattr(self,"transform_state") else None
        if task and task.actor==actor and task.status in {"active","paused","blocked"}:
            raise ValueError("The actor has selected transformation work.")
        return super()._accept(actor,kind,method,participants,place,source)

    def material_for_actor(self,actor_id,operation,*references):
        if operation in {"tie","fasten"} and len(references)==3:
            try:
                left,right,_=(self.fixture.resolve_object_reference(x) for x in references)
                p=self.transform_profile
                if left==p.barrier_board and right==p.old and role(self.transform_state,p.old)!="fit":
                    return self._result("This component is not qualified for barrier fastening.",failure="component_unfit")
                if left==p.barrier_board and right==p.spare and not self._replacement_committed():
                    return self._result("Complete the physical replacement before fastening this spare as the restored barrier.",failure="component_unfit")
                if left==p.repair_board and right==p.old and role(self.transform_state,p.old)!="spacer":
                    return self._result("That component has not been repurposed for this connection.",failure="component_unfit")
            except ValueError:
                pass
        return super().material_for_actor(actor_id,operation,*references)

    def _qualified(self,task):
        p=self.transform_profile
        actor=task.actor
        if actor!=self.fixture.player_entity_id:
            if task.method not in dict(self.fixture.transformation_actor_methods).get(actor,()):
                raise MaterialError("This actor has no declared transformation method.")
            if not self.actor_profile(actor).willing:
                raise MaterialError("The actor no longer consents to this work.")
            try:
                other=participation.selected(self.participation_state,actor)
                if other.status in {"active","paused","blocked"}:
                    raise MaterialError("The actor has other selected work.")
            except participation.ParticipationRefusal:
                pass
        at=p.work_place if task.method=="repurpose" else p.barrier_place
        if self._actor_place_id(actor)!=at:
            raise MaterialError("The performer is not at the declared work position.")
        if not self._visible_for_actor(actor,p.old):
            raise MaterialError("The component is not currently accessible.")
        if not self._visible_for_actor(actor,task.resource):
            raise MaterialError("The required tool or part is not accessible.")
        r=placement(self.state.representation,task.resource)
        if (r.relation_type,r.object_entity_id)!=("carried_by",actor):
            raise MaterialError("The performer must carry the declared tool or whole spare.")
        condition=role(self.transform_state,p.old)
        if task.method=="refit":
            needed="unfit" if task.stage==0 else "prepared"
            if condition!=needed or placement(self.state.representation,p.old).relation_type!="supported_by" or placement(self.state.representation,p.old).object_entity_id!=p.trestle:
                raise MaterialError("The staged component is no longer eligible for refitting.")
        elif task.method=="replace":
            old=placement(self.state.representation,p.old)
            if condition!="unfit":
                raise MaterialError("Only the unfit component is replaceable by this method.")
            if task.stage==0 and (old.relation_type,old.object_entity_id)!=("supported_by",p.trestle):
                raise MaterialError("Place the unfit component on the trestle before removal.")
            if task.stage==1 and (old.relation_type,old.object_entity_id)!=("carried_by",actor):
                raise MaterialError("The removed original part is no longer in performer custody.")
        else:
            if condition!="unfit" or placement(self.state.representation,p.old).relation_type!="carried_by" or placement(self.state.representation,p.old).object_entity_id!=actor:
                raise MaterialError("Carry the removed unfit original to repurpose it.")
        if not (self.fixture.ambient_visual_condition_for(at)=="sufficient" or self._actor_local_light_available(actor)):
            raise MaterialError("Work requires qualified local visibility.")

    def begin_transformation(self,method,target,resource,actor_reference=None):
        pre=self.authoritative_digest()
        try:
            p=self.transform_profile
            if method not in {"refit","replace","repurpose"}:
                raise MaterialError("That transformation method is unavailable.")
            actor=self.fixture.player_entity_id if actor_reference is None else self._actor(actor_reference)
            if actor!=self.fixture.player_entity_id:
                self._route(actor,"request")
                if not self.actor_profile(actor).willing:raise MaterialError("The actor declines.")
                if method not in dict(self.fixture.transformation_actor_methods).get(actor,()):
                    raise MaterialError("That actor has not agreed to this declared transformation method.")
                try:
                    other=participation.selected(self.participation_state,actor)
                    if other.status in {"active","blocked","paused"}:raise MaterialError("The actor is busy.")
                except participation.ParticipationRefusal:pass
            actual=self._resolve_visible_for_actor(actor,target)
            available=self._resolve_visible_for_actor(actor,resource)
            required=p.spare if method=="replace" else p.tool
            if actual!=p.old or available!=required:
                raise MaterialError("The selected component or method resource is incompatible.")
            existing=self.transform_state.work
            if existing and existing.status in {"active","blocked","paused"}:
                raise MaterialError("Finish or abandon existing transformation work first.")
            # An abandoned undertaking does not rewind an acknowledged partial
            # component. A fresh same-actor agreement reuses its real receipts.
            if (existing and existing.status=="abandoned" and
                    (existing.method,existing.actor,existing.target,existing.resource)
                    == (method,actor,p.old,required)):
                self.transform_state=replace(self.transform_state,
                    work=replace(existing,status="active"))
                return self._metadata_result(pre,"transformation_renewal",actor,
                    "Renewed transformation; earlier acknowledged stages and resources remain.")
            if method=="refit" and role(self.transform_state,p.old)!="unfit":
                raise MaterialError("That component is not available for refitting.")
            if method in {"replace","repurpose"} and role(self.transform_state,p.old)!="unfit":
                raise MaterialError("Only the declared unfit component supports that method.")
            self.transform_state=replace(self.transform_state,work=TransformationWork(actor,method,p.old,required))
            return self._metadata_result(pre,"transformation_acceptance",actor,
                "Transformation accepted; preparation reserves no tool or material. "
                "Each contribution requalifies the actual world.")
        except ValueError as exc:
            return self._result(str(exc),failure="transformation_acceptance_unavailable")

    def control_transformation(self,operation,actor_reference=None):
        pre=self.authoritative_digest()
        try:
            task=self.transform_state.work
            if task is None:raise MaterialError("No transformation work selected.")
            player=self.fixture.player_entity_id
            if task.actor!=player:
                if actor_reference is None:
                    raise MaterialError("This is the actor's work. Ask that actor through a qualified route.")
                actor=self._actor(actor_reference)
                if actor!=task.actor:
                    raise MaterialError("That actor does not own the selected transformation.")
                self._route(actor,"control")
                if not self.actor_profile(actor).willing:
                    raise MaterialError("The actor declines to change the work.")
            elif actor_reference is not None:
                raise MaterialError("This is player-owned work, not the addressed actor's task.")
            if operation=="pause" and task.status in {"active","blocked"}:state="paused"
            elif operation=="resume" and task.status in {"paused","blocked"}:state="active"
            elif operation=="abandon" and task.status not in {"abandoned","withdrawn","completed"}:state="abandoned"
            else:raise MaterialError("That work transition is unavailable.")
            self.transform_state=replace(self.transform_state,work=replace(task,status=state,reason=None))
            return self._metadata_result(pre,"transformation_"+operation,task.actor,
                "Transformation "+state+" by lawful control; committed work and parts remain.")
        except ValueError as exc:
            return self._result(str(exc),failure="transformation_control_unavailable")

    def transformation_status(self):
        task=self.transform_state.work
        if task is None:return self._result("No transformation is selected.")
        return self._result("Transformation: "+task.method+"; "+task.status+
            "; "+str(task.stage)+"/"+str(1 if task.method=="repurpose" else 2)+
            " contribution(s). Actual component fit: "+str(role(self.transform_state,self.transform_profile.old))+"."+
            (" Work notice: "+task.reason if task.reason else ""))

    def _perform_transformation(self,actor,clock_receipt):
        task=self.transform_state.work
        if task is None or task.actor!=actor or task.status not in {"active","blocked"}:
            return None
        # The caller has committed this one WORLD-1 interval already. Taking an
        # after-clock snapshot lets a subsequently refused owner stage restore
        # all physical/material/evidence effects without erasing elapsed time.
        after_clock=self._capture_transaction()
        try:
            p=self.transform_profile
            if actor!=self.fixture.player_entity_id:
                profile=self.actor_profile(actor)
                if not profile.willing or task.method not in dict(self.fixture.transformation_actor_methods).get(actor,()):
                    raise MaterialError("The actor is unwilling or lacks the declared method.")
                try:
                    other=participation.selected(self.participation_state,actor)
                    if other.status in {"active","paused","blocked"}:
                        raise MaterialError("The actor has other continuing work.")
                except participation.ParticipationRefusal:
                    pass
                if self._actor_place_id(actor)!=(p.work_place if task.method=="repurpose" else p.barrier_place):
                    raise MaterialError("The actor is not at the agreed work position.")
                if not self._visible_for_actor(actor,p.old):
                    raise MaterialError("The work target is not accessible to this actor.")
                if not (self.fixture.ambient_visual_condition_for(self._actor_place_id(actor))=="sufficient"
                        or self._actor_local_light_available(actor)):
                    raise MaterialError("The actor cannot perceive the work.")
                resources=[task.resource]
                if task.method=="repurpose":resources.insert(0,task.target)
                for obj in resources:
                    need=self._need_custody(actor,obj)
                    if need is not None:
                        prepared=self._execute_actor(actor,need)
                        if not prepared.authoritative_changed:
                            raise MaterialError(prepared.message)
                        self._event("transformation_preparation",actor,need,receipt=prepared.receipt_id)
                        self.evidence_state=knowledge.performed(self.evidence_state,actor,obj,
                            "activity","transformation_preparation",prepared.receipt_id,
                            self.runtime_state.logical_time_state.logical_position)
                        self._observe_all(prepared.receipt_id)
                        self.transform_state=replace(self.transform_state,work=replace(task,
                            due_intervals=(*task.due_intervals,clock_receipt),blocked_due=0,
                            status="active",reason=None))
                        return prepared
            self._qualified(task)
            physical=None
            if task.method=="replace":
                op="lift_from" if task.stage==0 else "put_on"
                item=p.old if task.stage==0 else p.spare
                result=self.material_for_actor(actor,op,self.fixture.entity_name(item),
                                               self.fixture.entity_name(p.trestle))
                if not result.authoritative_changed:
                    raise MaterialError(result.message)
                physical=result.receipt_id
            tick=self.runtime_state.logical_time_state.logical_position
            updated,receipt=record_stage(self.transform_state,p,actor,clock_receipt,tick,physical)
            self.transform_state=replace(updated,work=replace(updated.work,
                due_intervals=(*task.due_intervals,clock_receipt),blocked_due=0,reason=None))
            self._event("transformation_contribution",actor,
                        (task.method,updated.work.stage,physical),receipt=receipt)
            self.evidence_state=knowledge.performed(self.evidence_state,actor,p.old,
                 "activity","transformation:"+task.method,receipt,tick)
            self._observe_all(receipt)
            token=digest((receipt,clock_receipt,actor,task.method))[:28]
            command=create_command_envelope(command_id="transform-"+token,command_type="interact",
                source_actor_id=actor,payload={"method":task.method,"stage":updated.work.stage,
                                                "clock_receipt":clock_receipt,"physical_receipt":physical},
                metadata={"package":"PLAY-TARROW-TRANSFORMATION-1"})
            preview=create_transaction_preview(preview_id=build_record_id("transformation_preview",token),
                command=command,metadata={"semantic_owner":"RT-010","opportunity_owner":"AFQR-19",
                                          "mutation_performed":False})
            delta=create_state_delta_envelope(delta_id=build_record_id("transformation_delta",token),
                source_command_id=command.command_id,source_preview_id=preview.preview_id,
                affected_record_ids=(p.old,p.spare),change_type="record_update",
                payload={"method":task.method,"stage":updated.work.stage,"physical_receipt":physical},
                metadata={"semantic_owner":"RT-010","transition_owner":"AFQR-01"})
            return PlayApplicationResult(result_type="transformation_contribution",
                message=("Component "+task.method+" stage "+str(updated.work.stage)+
                         " committed by "+self.fixture.entity_name(actor)+
                         "; verify actual assembly and opportunity separately."),
                authoritative_changed=True,command_id=command.command_id,
                command_fingerprint=digest(command.to_dict()),preview_id=preview.preview_id,
                state_delta_id=delta.delta_id,receipt_id=receipt,
                opportunity_evidence_id=build_record_id("evidence","transformation-"+token))
        except ValueError as exc:
            # No material/actor intermediate step survives a failed contribution.
            # Due WORLD-1 time and passive environmental work are not rewound.
            self._restore_transaction(after_clock)
            current=self.transform_state.work
            limit=self.actor_profile(actor).blocked_limit if actor!=self.fixture.player_entity_id else None
            blocked_due=current.blocked_due+1
            status="withdrawn" if limit is not None and blocked_due>=limit else "blocked"
            self.transform_state=replace(self.transform_state,work=replace(current,
                status=status,blocked_due=blocked_due,
                due_intervals=(*current.due_intervals,clock_receipt),reason=str(exc)))
            return self._result(str(exc),failure="transformation_opportunity_unavailable")

    def _interval(self,name,args=(),kwargs=None,contribution=False):
        before=self.authoritative_digest()
        result=super()._interval(name,args,kwargs,contribution)
        task=self.transform_state.work if hasattr(self,"transform_state") else None
        if (task and result.authoritative_changed and task.actor!=self.fixture.player_entity_id
                and task.status in {"active","blocked"}):
            self._perform_transformation(task.actor,result.due_process_ref)
            return replace(result,pre_state_digest=before,post_state_digest=self.authoritative_digest())
        return result

    def contribute_transformation(self):
        task=self.transform_state.work
        if task is None or task.actor!=self.fixture.player_entity_id or task.status not in {"active","blocked"}:
            return self._result("No active player transformation selected.",failure="transformation_work_unavailable")
        before=self.authoritative_digest()
        clock=self._interval("wait")
        if clock.failure_class or not clock.authoritative_changed:
            return clock
        actual=self._perform_transformation(task.actor,clock.due_process_ref)
        if actual is None:return self._result("No transformation contribution was qualified.",failure="transformation_work_unavailable")
        if actual.failure_class:
            return replace(clock,result_type="timed_action_interrupted",
                message="Time advanced, but transformation was blocked: "+actual.message,
                failure_class="timed_action_interrupted",pre_state_digest=before,
                post_state_digest=self.authoritative_digest())
        return replace(actual,pre_state_digest=before,post_state_digest=self.authoritative_digest(),
                       logical_time_before=clock.logical_time_before,logical_time_after=clock.logical_time_after,
                       due_process_ref=clock.due_process_ref)

    def inspect(self,entity_reference):
        result=super().inspect(entity_reference)
        if result.failure_class:return result
        try:
            obj=self.fixture.resolve_object_reference(entity_reference)
        except ValueError:return result
        if self._visible(obj) and obj==self.transform_profile.old:
            from astra_runtime.myravant_terminal import _render_inspection_view
            base=_render_inspection_view(result.view) if result.view is not None else result.message
            return replace(result,view=None,message=base+
                "\nDeclared component fit: "+str(role(self.transform_state,obj))+
                ". This is profile-specific fit, not strength or universal damage.")
        return result


for _name in ("begin_transformation","control_transformation","contribute_transformation"):
    setattr(TransformationApplication,_name,
            _transaction(getattr(TransformationApplication,_name),_name))
