import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / 'docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml'
MATRIX = ROOT / 'docs/doctrine/reviews/afqr_01_20_dependency_matrix.yaml'
R1B = ROOT / 'docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml'


def load(path):
    return json.loads(path.read_text())


def afqr_ok(value):
    return isinstance(value, str) and value.startswith('AFQR-') and 1 <= int(value.split('-')[1]) <= 20


def test_primary_artifact_parses_and_ids_unique():
    data = load(ARTIFACT)
    assert data['artifact_id']
    ids = []
    for key, field in [('cross_afqr_invariants','invariant_id'), ('handoff_contracts','handoff_id'), ('cycle_risk_resolutions','cycle_id'), ('missing_substrate_classifications','substrate_id'), ('cross_phase_prohibitions','prohibition_id'), ('preserved_escalations','escalation_id')]:
        vals = [item[field] for item in data[key]]
        assert len(vals) == len(set(vals))
        ids.extend(vals)
    assert len(ids) == len(set(ids))


def test_afqr_references_are_within_01_20():
    data = load(ARTIFACT)
    for node in data['afqr_node_registry']:
        assert afqr_ok(node['afqr_id'])
    for edge in data['dependency_edge_dispositions']:
        assert afqr_ok(edge['producer_afqr'])
        assert afqr_ok(edge['consumer_afqr'])
        owner = edge['semantic_type_owner']
        if owner['owner_kind'] == 'afqr':
            assert afqr_ok(owner['owner_id'])


def test_every_r1a_dependency_edge_has_exactly_one_r1c_disposition():
    data = load(ARTIFACT)
    matrix = load(MATRIX)
    source_ids = [e['edge_id'] for e in matrix['dependency_edges']]
    disp_ids = [e['edge_id'] for e in data['dependency_edge_dispositions']]
    assert sorted(disp_ids) == sorted(source_ids)
    assert len(disp_ids) == len(set(disp_ids)) == len(source_ids)
    assert all(e['r1a_edge_preserved'] for e in data['dependency_edge_dispositions'])


def test_dispositions_have_evidence_or_unresolved_status_and_preserve_nonownership():
    data = load(ARTIFACT)
    for edge in data['dependency_edge_dispositions']:
        assert edge['source_evidence_records'] or edge['r1c_status'] in {'escalated','unresolved','conditional'}
        assert edge['ownership_does_not_transfer'] is True
        assert edge['consumer_not_semantic_owner_by_consumption'] is True
        assert edge['semantic_type_owner']['owner_id'] != edge['consumer_afqr'] or edge['producer_afqr'] == edge['consumer_afqr'] or edge['semantic_type_owner']['owner_kind'] != 'afqr' or edge['relation_or_handoff_kind'] not in {'commit','handoff','communication_handoff','environment_handoff','space_handoff'}


def test_referenced_r1b_terms_exist():
    data = load(ARTIFACT)
    r1b = load(R1B)
    terms = {t['term_id'] for t in r1b['term_records']}
    for inv in data['cross_afqr_invariants']:
        assert set(inv['r1b_terms']) <= terms
    for edge in data['dependency_edge_dispositions']:
        assert set(edge['semantic_type_owner']['r1b_terms']) <= terms


def test_cycle_risk_groups_explicit_and_edges_preserved():
    data = load(ARTIFACT)
    matrix = load(MATRIX)
    expected = {tuple(g) for g in matrix['cycle_risk_groups']}
    actual = {tuple(c['afqrs']) for c in data['cycle_risk_resolutions']}
    assert actual == expected
    review_edges = {e['edge_id'] for e in matrix['dependency_edges'] if e.get('cycle_risk') == 'review_required'}
    disposed_review_edges = {e['edge_id'] for e in data['dependency_edge_dispositions'] if e['cycle_participation']}
    assert disposed_review_edges == review_edges
    for cycle in data['cycle_risk_resolutions']:
        assert cycle['resolution'] in {'bounded_feedback_rule','phase_ordering','escalation'}
        assert cycle['breaker']
        assert cycle['valid_edges_preserved'] is True


def test_missing_substrates_and_cross_phase_prohibitions():
    data = load(ARTIFACT)
    matrix = load(MATRIX)
    assert {s['name'] for s in data['missing_substrate_classifications']} == set(matrix['dependencies_missing_from_repository'])
    for substrate in data['missing_substrate_classifications']:
        assert 'must_not_implement' in substrate['r1c_must_not_implement']
        assert substrate['status'] == 'classified_unimplemented'
    assert {p['risk'] for p in data['cross_phase_prohibitions']} == set(matrix['cross_phase_handoffs_at_risk'])
    assert all(p['governed_nonautomatic'] for p in data['cross_phase_prohibitions'])


def test_preserved_escalations_and_hidden_truth_boundary():
    data = load(ARTIFACT)
    assert {e['collision_id'] for e in data['preserved_escalations']} == {'COLL-03','COLL-08','COLL-10'}
    assert all(e['status'] == 'open' for e in data['preserved_escalations'])
    assert any(p.get('hidden_truth_direct_promotion_forbidden') for p in data['cross_phase_prohibitions'])
    assert any('hidden truth cannot leak' in i['summary'].lower() for i in data['cross_afqr_invariants'])


def test_no_downstream_authority_and_gates():
    data = load(ARTIFACT)
    lower = data['authority_boundary'].lower()
    for forbidden in ['runtime implementation','conversion execution','canon/sourcebook','model-facing','live-play']:
        assert f'no {forbidden}' in lower
    gates = data['r1d_handoff_requirements']
    assert gates['r1d_must_not_be_marked_complete'] is True
    assert gates['r1e_status'] == 'blocked'
    assert gates['r2_to_r6_status'] == 'blocked'
    assert 'blocked' in gates['rt_002g_status']
    assert gates['temporary_evidence_deletion'] == 'unauthorized'


def test_no_src_or_binary_or_zip_changes():
    result = subprocess.run(['git','diff','--name-only','HEAD'], cwd=ROOT, text=True, capture_output=True, check=True)
    changed = [line for line in result.stdout.splitlines() if line]
    assert not any(path.startswith('src/') for path in changed)
    assert not any(path.lower().endswith('.zip') for path in changed)
    numstat = subprocess.run(['git','diff','--numstat','HEAD'], cwd=ROOT, text=True, capture_output=True, check=True).stdout
    assert not any(line.startswith('-\t-\t') for line in numstat.splitlines())


def test_production_code_does_not_import_temporary_evidence_or_r1c_reviews():
    src = ROOT / 'src'
    if not src.exists():
        return
    needles = ['working/afqr_consolidation_inputs', 'afqr_r1c_invariant_dependency_resolution_report', 'afqr_r1c_unresolved_dependency_escalation_ledger']
    for path in src.rglob('*.py'):
        text = path.read_text(errors='ignore')
        assert not any(n in text for n in needles)


def test_corpus_pressure_and_no_donor_defaults():
    data = load(ARTIFACT)
    families = data['corpus_pressure_findings']['covered_donor_families']
    assert len(families) >= 18
    assert 'vehicles, mechs, ships, and platforms' in families
    forbidden = data['corpus_pressure_findings']['forbidden_default_assumptions']
    for expected in ['one cosmology','one anatomy','one identity model','one action economy','one resolution style','one progression model','one resource economy','one map topology','one sensing model','one legal or social system','one actor scale','one vehicle/operator relationship']:
        assert expected in forbidden
    assert 'does not promote' in data['corpus_pressure_findings']['finding']
