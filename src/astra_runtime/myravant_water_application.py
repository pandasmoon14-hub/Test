"""Qualified #544 operations composed with material/retained-owner commitment."""
from dataclasses import replace
import re

from astra_runtime.myravant_material_application import MaterialApplication, JOURNALED, _transaction
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.domain.persistent_world_material import digest, placement, validate_joint
from astra_runtime.domain.persistent_world_water_cleaning import execute, validate, canonical_state, WaterCleaningRefusal
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.transaction_preview import create_transaction_preview
from astra_runtime.kernel.state_delta import create_state_delta_envelope


class WaterApplication(MaterialApplication):
    checkpoint_format = 'myravant.water-material-owner-journal'
    replay_methods = (*JOURNALED, 'water')

    @staticmethod
    def default_fixture():
        from astra_runtime.myravant_tarrow_water import create_water_fixture
        return create_water_fixture()

    @classmethod
    def new(cls, *, checkpoint_path=None, fixture=None):
        return super().new(checkpoint_path=checkpoint_path, fixture=fixture or cls.default_fixture())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.water_profile = self.fixture.water_profile
        self.water_state = self.fixture.water_initial
        self._validate_transaction()

    def _checkpoint_profile(self):
        from astra_runtime.myravant_tarrow_water import profile_payload
        return {'material': super()._checkpoint_profile(), 'water': profile_payload(self.water_profile),
                'initial_water': canonical_state(self.fixture.water_initial)}

    def authoritative_digest(self):
        return digest({'version': 1, 'material': super().authoritative_digest(),
                       'binding': self._checkpoint_profile(), 'water': canonical_state(self.water_state)})

    def _capture_transaction(self):
        return super()._capture_transaction(), self.water_state

    def _restore_transaction(self, snapshot):
        old, self.water_state = snapshot
        super()._restore_transaction(old)

    def _validate_transaction(self):
        super()._validate_transaction()
        validate(self.water_state, self.water_profile)
        ids = {e.entity_id for e in self.state.representation.entities if e.classification=='object'}
        if not {a.id for a in self.water_profile.assets} <= ids:
            raise ValueError('water profile references absent objects')
        validate(self.fixture.water_initial, self.water_profile)

    def _prepare_water_transition(self, operation, participants, amount):
        return execute(self.water_state, self.water_profile, operation, participants, amount), None

    def _install_water_transition(self, candidate, auxiliary):
        self.water_state = candidate

    def water(self, operation, *references, amount=None):
        return self.water_for_actor(self.fixture.player_entity_id, operation, *references, amount=amount)

    def water_for_actor(self, actor_id, operation, *references, amount=None):
        """Clock-free qualified execution; caller owns commitment and replay."""
        pre = self.authoritative_digest()
        try:
            if len(references)!=2 or any(type(x) is not str for x in references):
                raise WaterCleaningRefusal('Specify two accessible water or cleaning participants.')
            self._actor_place_id(actor_id)
            participants = tuple(self._resolve_visible_for_actor(actor_id,x) for x in references)
            tracked = {a.id for a in self.water_profile.assets}
            if not set(participants) <= tracked:
                raise WaterCleaningRefusal('That material method is not qualified for these participants.')
            # Reach is narrower than visibility: no remote or contained manipulation.
            for obj in participants:
                if placement(self.state.representation,obj).relation_type not in {'located_at','supported_by','carried_by'}:
                    raise WaterCleaningRefusal('Take the participant out of its container before using it.')
            carried = participants[0] if operation in {'pour','empty','wring','rinse','collect'} else participants[1] if operation in {'soak','wipe','scrub'} else None
            if carried is not None:
                r = placement(self.state.representation, carried)
                if r.relation_type!='carried_by' or r.object_entity_id!=actor_id:
                    raise WaterCleaningRefusal('Carry the source vessel or working tool before using this method.')
            candidate, auxiliary = self._prepare_water_transition(operation,participants,amount)
            command_id = (f'terminal-water-{len(self.journal)+1:06d}' if actor_id == self.fixture.player_entity_id
                          else f'actor-water-{digest(actor_id)[:12]}-{len(self.journal)+1:06d}')
            token = digest([command_id,pre,operation,participants,amount])[:28]
            command = create_command_envelope(command_id=command_id,command_type='interact',source_actor_id=actor_id,
                payload={'operation':operation,'participants':list(participants),'amount':amount}, metadata={'package':'PLAY-TARROW-WATER-1'})
            preview = create_transaction_preview(preview_id=build_record_id('water_preview',token),command=command,
                metadata={'semantic_owner':'RT-010','opportunity_owner':'AFQR-19','mutation_performed':False})
            delta = create_state_delta_envelope(delta_id=build_record_id('water_delta',token),source_command_id=command_id,
                source_preview_id=preview.preview_id,affected_record_ids=participants,change_type='record_update',
                payload={'operation':operation,'participants':list(participants),'amount':amount,'pre_digest':pre},
                metadata={'semantic_owner':'RT-010','transition_owner':'AFQR-01'})
            old = self.water_state
            self._install_water_transition(candidate, auxiliary)
        except ValueError as exc:
            return self._result(str(exc),failure='water_opportunity_unavailable')
        source,target = (self.fixture.entity_name(x) for x in participants)
        moved = abs(dict(candidate.water)[participants[1]]-dict(old.water)[participants[1]])
        message = f'{operation.capitalize()}: {source} to {target}.'
        if operation in {'pour','fill','empty','soak','wring'}:
            message += f' Transferred {moved} water unit(s).'
        elif operation in {'wipe','scrub','rinse','collect'}:
            message += ' Residue transferred; inspect the participants for current condition.'
        return PlayApplicationResult(result_type='water_committed',message=message,authoritative_changed=True,
            command_id=command_id,command_fingerprint=digest(command.to_dict()),preview_id=preview.preview_id,
            state_delta_id=delta.delta_id,receipt_id=build_record_id('water_receipt',token),
            opportunity_evidence_id=build_record_id('evidence','water-opportunity-'+token),
            pre_state_digest=pre,post_state_digest=self.authoritative_digest())

    def inspect(self, entity_reference):
        result = super().inspect(entity_reference)
        try:
            obj = self.fixture.resolve_object_reference(entity_reference)
        except ValueError:
            return result
        if result.failure_class or obj not in dict(self.water_state.water) or not self._visible(obj):
            return result
        from astra_runtime.myravant_terminal import _render_inspection_view
        base = _render_inspection_view(result.view) if result.view is not None else result.message
        asset = next(a for a in self.water_profile.assets if a.id==obj)
        water = dict(self.water_state.water)[obj]
        adhered = dict(self.water_state.adhered)[obj]
        suspended = dict(self.water_state.suspended)[obj]
        lines = [f'Removable residue: {adhered} unit(s).']
        if asset.kind in {'vessel','absorbent'}:
            lines += [f'Water: {water}/{asset.water_capacity} unit(s).', f'Suspended residue: {suspended} unit(s).']
        if asset.kind=='absorbent':
            lines += ['Condition: wet.' if water else 'Condition: dry.']
        return replace(result,view=None,message=base+'\n'+'\n'.join(lines))

    def focused_observation(self, entity_reference, *, direction=None):
        if direction is None:
            try:
                obj = self.fixture.resolve_object_reference(entity_reference)
            except ValueError:
                obj = None
            if obj in dict(self.water_state.water):
                return self.inspect(entity_reference)
        return super().focused_observation(entity_reference,direction=direction)


WaterApplication.water = _transaction(WaterApplication.water, 'water')

# Full-match grammar retains all participants and rejects unsupported modifiers.
_PATTERNS = (
    ('pour', r'pour ([0-9]+) units? from (.+?) into (.+)'),
    ('fill', r'fill (.+?) from (.+)'),
    ('empty', r'empty (.+?) into (.+)'),
    ('soak', r'soak (.+?) from (.+)'),
    ('wipe', r'wipe (.+?) (?:using|with) (.+)'),
    ('scrub', r'scrub (.+?) (?:using|with) (.+)'),
    ('rinse', r'rinse (.+?) in (.+)'),
    ('wring', r'wring (.+?) into (.+)'),
    ('collect', r'collect residue from (.+?) into (.+)'),
)


def parse_water(raw):
    text = ' '.join(raw.strip().casefold().split())
    for operation, pattern in _PATTERNS:
        match = re.fullmatch(pattern, text)
        if match:
            groups = match.groups()
            if operation=='pour':
                # Bounded parser work, including hostile enormous quantities.
                if len(groups[0]) > 9:
                    return operation, groups[1:], 0
                return operation, groups[1:], int(groups[0])
            if operation in {'fill','soak'}:
                groups = (groups[1],groups[0])
            return operation, groups, None
    return None


def execute_water_request(application, raw):
    parsed = parse_water(raw)
    return None if parsed is None else ('water', application.water(parsed[0],*parsed[1],amount=parsed[2]))
