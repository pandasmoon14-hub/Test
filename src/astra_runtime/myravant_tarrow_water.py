"""Approved #544 development water profiles; not canonical Tarrow resources."""
from dataclasses import asdict, dataclass, replace
from fractions import Fraction

from astra_runtime.myravant_tarrow import create_tarrow_fixture, identity
from astra_runtime.myravant_tarrow_material import MaterialFixture, material_layout, execute_material_locality_request
from astra_runtime.domain.persistent_world_material import digest
from astra_runtime.domain.persistent_world_water_cleaning import WaterCleaningAsset, WaterCleaningProfile, WaterCleaningState, canonical_state, validate


def profile_payload(profile):
    return {'assets': [{'id': a.id, 'kind': a.kind, 'water_capacity': a.water_capacity,
            'residue_capacity': [a.residue_capacity.numerator, a.residue_capacity.denominator],
            'transfer_rate': [a.transfer_rate.numerator, a.transfer_rate.denominator]} for a in profile.assets],
            'allowed_pairs': profile.allowed_pairs}


@dataclass(frozen=True)
class WaterFixture(MaterialFixture):
    water_profile: WaterCleaningProfile | None = None
    water_initial: WaterCleaningState | None = None

    @property
    def locality_help(self):
        return ('Water and cleaning: pour <N> units from <vessel> into <vessel>; fill <vessel> from <vessel>; '
                'empty <vessel> into <vessel>; soak <cloth> from <vessel>; wipe <surface> using <cloth>; '
                'scrub <surface> using <brush>; rinse <tool> in <vessel>; wring <cloth> into <vessel>; '
                'collect residue from <tool> into <tray>.\n'
                'Carry a pouring source or working tool. Fill draws from an accessible vessel. Inspect accessible supplies for current quantities. '
                'Wet cloth wipes; brushes scrub dry; rinsing transfers residue into wash water. Wringing leaves adhered residue on the cloth. '
                'Water is finite; no disposal into scenery or passive drying is qualified.\n' + super().locality_help)


def create_water_fixture():
    layout, material = material_layout()
    rows = (
        ('wash-bucket', 'Wash Bucket', 'An open development water vessel; inspect its actual contents.', 'work-bench'),
        ('rinse-basin', 'Rinse Basin', 'An open wash basin with a declared liquid capacity.', 'work-bench'),
        ('pouring-jug', 'Pouring Jug', 'A portable open jug for measured water transfers.', 'work-bench'),
        ('cleaning-cloth', 'Cleaning Cloth', 'An absorbent working cloth; retained water and residue are tracked separately.', 'work-bench'),
        ('cleaning-brush', 'Cleaning Brush', 'A dry working brush for compatible removable residue.', 'yard-tools'),
        ('debris-tray', 'Debris Tray', 'An open collecting tray for declared loose residue.', 'yard-tools'),
        ('practice-panel', 'Practice Panel', 'A loose washable development panel. Surface wear is distinct from removable residue.', 'work-bench'),
        ('sorting-board', 'Sorting Board', 'A loose development board with compatible removable residue.', 'yard-tools'),
    )
    specifications = (
        ('wash-bucket','vessel',12,0,0), ('rinse-basin','vessel',6,0,0),
        ('pouring-jug','vessel',3,0,0), ('cleaning-cloth','absorbent',2,2,1),
        ('cleaning-brush','brush',0,4,2), ('debris-tray','tray',0,7,0),
        ('practice-panel','surface',0,3,0), ('sorting-board','surface',0,4,0),
    )
    assets = tuple(WaterCleaningAsset(identity(k),kind,cap,residue,rate) for k,kind,cap,residue,rate in specifications)
    vessels = ('wash-bucket','rinse-basin','pouring-jug')
    pairs = [(op,identity(a),identity(b)) for op in ('pour','fill','empty') for a in vessels for b in vessels if a != b]
    pairs += [('soak',identity(v),identity('cleaning-cloth')) for v in vessels]
    pairs += [(op,identity(surface),identity(tool)) for surface in ('practice-panel','sorting-board')
              for op,tool in (('wipe','cleaning-cloth'),('scrub','cleaning-brush'))]
    pairs += [('rinse',identity(t),identity(v)) for t in ('cleaning-cloth','cleaning-brush') for v in vessels]
    pairs += [('wring',identity('cleaning-cloth'),identity(v)) for v in vessels]
    pairs += [('collect',identity(t),identity('debris-tray')) for t in ('cleaning-cloth','cleaning-brush')]
    profile = WaterCleaningProfile(assets, tuple(pairs))
    initial = WaterCleaningState(tuple((a.id,12 if a.id==identity('wash-bucket') else 0) for a in assets),
        tuple((a.id,3 if a.id==identity('practice-panel') else 4 if a.id==identity('sorting-board') else 0) for a in assets),
        tuple((a.id,0) for a in assets))
    validate(initial,profile)
    # New content identity binds profile AND initial quantities; old saves keep their roots.
    containers = ('coffer','basket','sorting-tray','parts-tray','document-box','guest-box','delivery-box')
    surfaces = ('bench','trestle','document-box','tool-shelf','guest-bench')
    material = replace(material, support_pairs=material.support_pairs + tuple((identity(k),identity(s)) for k,_,_,_ in rows for s in surfaces))
    witness = {'water': profile_payload(profile), 'initial': canonical_state(initial), 'material': asdict(material)}
    layout = replace(layout, version='water-1-'+digest(witness)[:16], objects=layout.objects+rows,
        storage=layout.storage+tuple((k,c) for k,_,_,_ in rows for c in containers), specialists=(*layout.specialists,'water'))
    fixture = create_tarrow_fixture(layout=layout)
    return WaterFixture(**fixture.__dict__, material_profile=material, water_profile=profile, water_initial=initial)


def execute_water_locality_request(application, raw):
    from astra_runtime.myravant_water_application import execute_water_request
    return execute_water_request(application, raw) or execute_material_locality_request(application, raw)
