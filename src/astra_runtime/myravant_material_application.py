"""Opt-in material composition and atomic command checkpoint adapter.

Material v1 replays qualified owner procedures from the exact declared root.
The chronological journal includes both old-owner and material receipts/digests;
no stored final arrangement or unqualified snapshot is trusted on restore.
Legacy checkpoint families and application behavior remain unchanged.
"""
from dataclasses import asdict, replace
from functools import wraps
import json
from pathlib import Path
import re

from astra_runtime.myravant_play_application import MyravantPlayApplication, PlayApplicationResult
from astra_runtime.domain.persistent_world_material import (
    MaterialError, digest, execute_material, validate_joint, placement,
    effective_place, constrained, active_effects,
)
from astra_runtime.domain.persistent_world_entity_location_representation import serialize_persistent_world_entity_location_representation
from astra_runtime.domain.persistent_world_component_checkpoint import _write_envelope
from astra_runtime.domain.persistent_world_local_checkpoint_restore import PersistentWorldCheckpointWriteError

FORMAT = 'myravant.material-owner-journal'


class MaterialApplication(MyravantPlayApplication):
    checkpoint_format = FORMAT

    @staticmethod
    def default_fixture():
        from astra_runtime.myravant_tarrow_material import create_material_fixture
        return create_material_fixture()

    def _checkpoint_profile(self):
        return asdict(self.material_profile)

    def _capture_transaction(self):
        return self._runtime_state, self.connections, self.journal

    def _restore_transaction(self, snapshot):
        self._runtime_state, self.connections, self.journal = snapshot

    def _validate_transaction(self):
        validate_joint(self.state.representation, self.connections, self.material_profile)

    def __init__(self, *, material_profile=None, **kwargs):
        super().__init__(**kwargs)
        self.material_profile = material_profile or self.fixture.material_profile
        if self.material_profile.actor_id != self.fixture.player_entity_id:
            raise MaterialError('material actor differs from the selected player')
        self.connections = ()
        self.journal = ()
        self._in_transaction = False
        self._durability_failed = False
        validate_joint(self.state.representation,self.connections,self.material_profile)

    def authoritative_digest(self):
        return digest({'version':1,'runtime':super().authoritative_digest(),
            'profile':asdict(self.material_profile),'connections':[asdict(c) for c in self.connections]})

    def _result(self, message, *, failure=None, **kwargs):
        d=self.authoritative_digest()
        return PlayApplicationResult(result_type='material_rejected' if failure else 'material_observation',
            message=message,failure_class=failure,pre_state_digest=d,post_state_digest=d,**kwargs)

    def _bounded_local_light_available(self):
        if super()._bounded_local_light_available():
            return True
        lamp=self.fixture.light_source_id
        light=self.object_lit_state(lamp)
        r=placement(self.state.representation,lamp)
        return (r.relation_type=='supported_by' and light is not None and light.state=='lit'
                and effective_place(self.state.representation,lamp)==self.current_place_id())

    def _object_locally_present(self, obj):
        r=placement(self.state.representation,obj)
        if r.relation_type in {'supported_by','reserved_by'}:
            return self._object_locally_present(r.object_entity_id)
        return super()._object_locally_present(obj)

    def _object_currently_available(self, obj):
        r=placement(self.state.representation,obj)
        if r.relation_type in {'supported_by','reserved_by'}:
            return self._visible(obj)
        return super()._object_currently_available(obj)

    def _public_location_objects(self, place):
        base=super()._public_location_objects(place)
        ids={p.entity_id for p in base}
        return (*base,*(p for p in self.fixture.object_presentations
            if p.entity_id not in ids and placement(self.state.representation,p.entity_id).relation_type in {'supported_by','reserved_by'}
            and self._visible(p.entity_id) and effective_place(self.state.representation,p.entity_id)==place))

    def _visible(self, obj):
        # AFQR-20: actual local light, custody and closure. A known ID is not access.
        try:
            r=placement(self.state.representation,obj)
            if r.relation_type == 'carried_by' and r.object_entity_id == self.fixture.player_entity_id:
                return True
            if not (self.fixture.ambient_visual_condition_for(self.current_place_id())=='sufficient' or self._bounded_local_light_available()) or effective_place(self.state.representation,obj)!=self.current_place_id():
                return False
            if r.relation_type == 'contained_by':
                return self._contained_object_accessible(obj)
            if r.relation_type in {'supported_by','reserved_by'}:
                return self._visible(r.object_entity_id)
            return r.relation_type == 'located_at'
        except MaterialError:
            return False

    def _resolve_visible(self, text):
        try:
            obj=self.fixture.resolve_object_reference(text)
        except ValueError as exc:
            raise MaterialError('That object is unavailable or ambiguous.') from exc
        if not self._visible(obj):
            raise MaterialError('That object is not currently accessible.')
        return obj

    def material(self, operation, *references):
        pre=self.authoritative_digest()
        try:
            arities={'put_on':2,'lift_from':2,'tie':3,'fasten':3,'untie':1,'unfasten':1}
            if operation not in arities or len(references)!=arities[operation] or any(type(x) is not str for x in references):
                raise MaterialError('That material method or participant list is not admitted.')
            participants=tuple(self._resolve_visible(x) for x in references)
            if operation in {'untie','unfasten'}:
                matches=[c for c in self.connections if c.fastener==participants[0]]
                if len(matches)!=1:
                    raise MaterialError('No accessible matching connection.')
                c=matches[0]
                participants=(c.fastener,c.left,c.right)
            visible=tuple(p.entity_id for p in self.fixture.object_presentations if self._visible(p.entity_id))
            rep,connections,receipt=execute_material(rep=self.state.representation,connections=self.connections,
                profile=self.material_profile,operation=operation,participants=participants,visible_ids=visible,
                command_id=f'terminal-material-{len(self.journal)+1:06d}',expected_pre_digest=pre,pre_digest=self.authoritative_digest())
            self._runtime_state=replace(self._runtime_state,movement_state=replace(self.state,representation=rep))
            self.connections=connections
        except (MaterialError,ValueError) as exc:
            return self._result(str(exc),failure='material_opportunity_unavailable')
        names=[self.fixture.entity_name(x) for x in participants]
        messages={
            'put_on':lambda:f'You put {names[0]} on {names[1]}.',
            'lift_from':lambda:f'You lift {names[0]} from {names[1]}.',
            'tie':lambda:f'You tie {names[0]} to {names[1]} using {names[2]}.',
            'fasten':lambda:f'You fasten {names[0]} to {names[1]} using {names[2]}.',
            'untie':lambda:f'You untie and recover {names[0]}.',
            'unfasten':lambda:f'You unfasten and recover {names[0]}.',
        }
        return PlayApplicationResult(result_type='material_committed',message=messages[operation](),
            authoritative_changed=True,pre_state_digest=pre,post_state_digest=self.authoritative_digest(),**receipt)

    def _guard(self, reference):
        try:
            obj=self.fixture.resolve_object_reference(reference)
        except ValueError:
            return None
        if constrained(self.state.representation,self.connections,obj) or placement(self.state.representation,obj).relation_type=='reserved_by':
            return self._result('That object is supported, supports other objects, or is fastened. Remove the relevant relationship first.',failure='material_relationship_conflict') if self._visible(obj) else self._result('That object is not currently accessible.',failure='material_target_unavailable')
        return None

    def _custody(self, *, operation, object_reference):
        return self._guard(object_reference) or super()._custody(operation=operation,object_reference=object_reference)

    def _storage(self, *, operation, object_reference, container_reference):
        return self._guard(object_reference) or super()._storage(operation=operation,object_reference=object_reference,container_reference=container_reference)

    def displace_object(self, object_reference, direction, *, method='push'):
        return self._guard(object_reference) or self._passage_block(direction) or super().displace_object(object_reference,direction,method=method)

    def give_object(self, object_reference, recipient_reference):
        return self._guard(object_reference) or super().give_object(object_reference,recipient_reference)

    def _passage_block(self, direction):
        if any(e.source==self.current_place_id() and e.direction==direction.strip().lower() and e.kind=='movement'
               for e in active_effects(self.state.representation,self.connections,self.material_profile)):
            return self._result('The assembled barrier obstructs that passage. Remove a necessary fastening or component to reopen it.',failure='material_passage_obstructed')
        return None

    def move(self, direction, *, method='walk'):
        return self._passage_block(direction) or super().move(direction,method=method)

    def _screened(self, direction):
        return any(e.source==self.current_place_id() and e.direction==direction.strip().lower() and e.kind=='sight'
                   for e in active_effects(self.state.representation,self.connections,self.material_profile))

    def look_direction(self, direction):
        if self._screened(direction):
            return self._result('The assembled screen blocks that sightline.',failure='material_sightline_obstructed')
        return super().look_direction(direction)

    def focused_observation(self, entity_reference, *, direction=None):
        if direction is None:
            try:
                obj=self.fixture.resolve_object_reference(entity_reference)
            except ValueError:
                obj=None
            if obj is not None and placement(self.state.representation,obj).relation_type in {'supported_by','reserved_by'}:
                return self.inspect(entity_reference)
        if direction and self._screened(direction):
            return self._result('The assembled screen blocks that sightline.',failure='material_sightline_obstructed')
        return super().focused_observation(entity_reference,direction=direction)

    def inspect(self, entity_reference):
        try:
            obj=self.fixture.resolve_object_reference(entity_reference)
        except ValueError:
            return super().inspect(entity_reference)
        if not self._visible(obj):
            return self._result('You cannot inspect that in the current state.',failure='material_target_unavailable')
        r=placement(self.state.representation,obj)
        if r.relation_type not in {'supported_by','reserved_by'}:
            result=super().inspect(entity_reference)
        else:
            p=self.fixture.object_presentation(obj)
            result=self._result(p.name+'\n'+p.description)
        lines=[]
        if r.relation_type=='supported_by':
            lines.append('Resting on: '+self.fixture.entity_name(r.object_entity_id)+'.')
        supported=[r.subject_entity_id for r in self.state.representation.relations if r.relation_type=='supported_by' and r.object_entity_id==obj and self._visible(r.subject_entity_id)]
        if supported:
            lines.append('On the exterior surface: '+', '.join(self.fixture.entity_name(x) for x in supported)+'.')
        for c in self.connections:
            if obj in (c.left,c.right,c.fastener) and all(self._visible(x) for x in (c.left,c.right,c.fastener)):
                lines.append('Connection: '+self.fixture.entity_name(c.left)+' to '+self.fixture.entity_name(c.right)+' using '+self.fixture.entity_name(c.fastener)+f' ({c.method}).')
        if lines:
            # Convert the existing audience-qualified inspection to a plain result;
            # the terminal otherwise renders only its structured view.
            from astra_runtime.myravant_terminal import _render_inspection_view
            base=_render_inspection_view(result.view) if result.view is not None else result.message
            result=replace(result,view=None,message=base+'\n'+'\n'.join(lines))
        return result

    def look(self):
        result=super().look()
        extra=[]
        for p in self.fixture.object_presentations:
            if self._visible(p.entity_id):
                r=placement(self.state.representation,p.entity_id)
                if r.relation_type=='supported_by':
                    extra.append(p.name+' on '+self.fixture.entity_name(r.object_entity_id))
        if extra:
            result=replace(result,view=replace(result.view,description=result.view.description+'\nSupported objects: '+', '.join(extra)+'.'))
        return result

    def save(self):
        if self.checkpoint_path is None:
            return self._result('A checkpoint path is required.',failure='checkpoint_path_required')
        d=self.authoritative_digest()
        payload={'campaign':self.fixture.campaign_id,'profile':self._checkpoint_profile(),
                 'root':self.fixture.provenance.initial_state_digest,'journal':list(self.journal),'final':d}
        envelope={'format_identity':self.checkpoint_format,'format_version':1,'payload':payload,'integrity_digest':digest(payload)}
        checkpoint_digest=_write_envelope(envelope=envelope,checkpoint_path=self.checkpoint_path)
        return PlayApplicationResult(result_type='checkpoint_written',message='Checkpoint written.',pre_state_digest=d,post_state_digest=d,checkpoint_digest=checkpoint_digest)

    @classmethod
    def restore(cls, *, checkpoint_path, fixture=None):
        if fixture is None:
            fixture=cls.default_fixture()
        try:
            app=cls.new(fixture=fixture)
            raw=json.loads(Path(checkpoint_path).read_text())
            if set(raw)!={'format_identity','format_version','payload','integrity_digest'} or raw['format_identity']!=app.checkpoint_format or type(raw['format_version']) is not int or raw['format_version']!=1:
                raise MaterialError('incompatible material checkpoint')
            p=raw['payload']
            if set(p)!={'campaign','profile','root','journal','final'} or digest(p)!=raw['integrity_digest'] or p['campaign']!=fixture.campaign_id or p['root']!=fixture.provenance.initial_state_digest or digest(p['profile'])!=digest(app._checkpoint_profile()):
                raise MaterialError('material binding or integrity mismatch')
            for entry in p['journal']:
                if set(entry)!={'method','args','kwargs','result'} or entry['method'] not in app.replay_methods:
                    raise MaterialError('unknown material replay operation')
                result=getattr(app,entry['method'])(*entry['args'],**entry['kwargs'])
                if not result.authoritative_changed or _receipt(result)!=entry['result']:
                    raise MaterialError('material replay receipt or state mismatch')
            if app.authoritative_digest()!=p['final'] or list(app.journal)!=p['journal']:
                raise MaterialError('material final state or chronology mismatch')
            app.checkpoint_path=Path(checkpoint_path)
            return app
        except (KeyError,TypeError,ValueError,AttributeError) as exc:
            raise MaterialError('invalid material checkpoint: '+str(exc)) from exc


def _receipt(result):
    return {k:getattr(result,k) for k in ('result_type','command_id','command_fingerprint','receipt_id','preview_id','state_delta_id','opportunity_evidence_id','pre_state_digest','post_state_digest')}


def _transaction(method, name):
    @wraps(method)
    def run(self,*args,**kwargs):
        if self._durability_failed:
            return self._result('Durability failed. Restart from a validated checkpoint before making further changes.',failure='material_session_halted')
        if self._in_transaction:
            return method(self,*args,**kwargs)
        before=self.authoritative_digest()
        old=self._capture_transaction()
        path=self.checkpoint_path
        self._in_transaction=True
        self.checkpoint_path=None
        try:
            result=method(self,*args,**kwargs)
            self._validate_transaction()
            after=self.authoritative_digest()
            if after!=before:
                result=replace(result,pre_state_digest=before,post_state_digest=after)
                self.journal=(*self.journal,{'method':name,'args':list(args),'kwargs':kwargs,'result':_receipt(result)})
                self.checkpoint_path=path
                if path is not None:
                    checkpoint=self.save()
                    result=replace(result,checkpoint_digest=checkpoint.checkpoint_digest)
            return result
        except Exception as exc:
            self._restore_transaction(old)
            if isinstance(exc,(OSError,PersistentWorldCheckpointWriteError)):
                self._durability_failed=True
                return self._result('The change could not be acknowledged. This session is halted; restart from a validated checkpoint.',failure='material_checkpoint_write_failed')
            raise
        finally:
            self.checkpoint_path=path
            self._in_transaction=False
    return run


# Public mutation paths share one commit boundary. Nested calls remain one step.
JOURNALED=('material','pickup','drop','store_object','retrieve_object','displace_object','throw_object',
           'give_object','open_object','close_object','light_object','extinguish_object','move','approach_place','wait',
           'request_object_from_actor','request_object_state_from_actor')
MaterialApplication.replay_methods = JOURNALED
for _name in JOURNALED:
    setattr(MaterialApplication,_name,_transaction(getattr(MaterialApplication,_name),_name))


_PATTERNS=(
    ('put_on',r'put (.+?) (?:on|onto) (.+)'),
    ('lift_from',r'lift (.+?) from (.+)'),
    ('tie',r'tie (.+?) to (.+?) (?:using|with) (.+)'),
    ('fasten',r'fasten (.+?) to (.+?) (?:using|with) (.+)'),
    ('untie',r'untie (.+)'),('unfasten',r'unfasten (.+)'),
)


def parse_material(raw):
    text=' '.join(raw.strip().casefold().split())
    for operation,pattern in _PATTERNS:
        m=re.fullmatch(pattern,text)
        if m:
            return operation,m.groups()
    return None


def execute_material_request(application,raw):
    parsed=parse_material(raw)
    return None if parsed is None else ('material',application.material(parsed[0],*parsed[1]))
