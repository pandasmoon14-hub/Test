import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / 'docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml'
MATRIX = ROOT / 'docs/doctrine/reviews/afqr_01_20_dependency_matrix.yaml'
R1B = ROOT / 'docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml'


def load(path):
    return json.loads(path.read_text())


def afqr_ok(value):
    return isinstance(value, str) and re.fullmatch(r'AFQR-(0[1-9]|1[0-9]|20)', value) is not None


def committed_diff(data, *args):
    base = data['verified_repository_baseline']['current_main_sha']
    assert re.fullmatch(r'[0-9a-f]{40}', base), 'verified R1C base must be a full commit SHA'
    subprocess.run(['git', 'cat-file', '-e', f'{base}^{{commit}}'], cwd=ROOT, check=True)
    return subprocess.run(
        ['git', 'diff', *args, f'{base}...HEAD'], cwd=ROOT, text=True,
        capture_output=True, check=True,
    ).stdout


def test_primary_artifact_parses_and_ids_unique():
    data = load(ARTIFACT)
    assert data['artifact_id']
    ids = []
    collections = [
        ('cross_afqr_invariants', 'invariant_id'), ('handoff_contracts', 'handoff_id'),
        ('cycle_risk_resolutions', 'cycle_id'), ('cycle_risk_reclassifications', 'reclassification_id'),
        ('missing_substrate_classifications', 'substrate_id'),
        ('cross_phase_prohibitions', 'prohibition_id'), ('preserved_escalations', 'escalation_id'),
    ]
    for key, field in collections:
        vals = [item[field] for item in data[key]]
        assert len(vals) == len(set(vals))
        ids.extend(vals)
    assert len(ids) == len(set(ids))


def test_afqr_references_are_within_01_20():
    data = load(ARTIFACT)
    assert all(afqr_ok(node['afqr_id']) for node in data['afqr_node_registry'])
    for edge in data['dependency_edge_dispositions']:
        assert afqr_ok(edge['producer_afqr']) and afqr_ok(edge['consumer_afqr'])
        owner = edge['semantic_type_owner']
        if owner['owner_kind'] == 'afqr':
            assert afqr_ok(owner['owner_id'])


def test_every_r1a_dependency_edge_has_exactly_one_r1c_disposition():
    data, matrix = load(ARTIFACT), load(MATRIX)
    source_ids = [e['edge_id'] for e in matrix['dependency_edges']]
    disp_ids = [e['edge_id'] for e in data['dependency_edge_dispositions']]
    assert sorted(disp_ids) == sorted(source_ids)
    assert len(disp_ids) == len(set(disp_ids)) == len(source_ids)
    assert all(e['r1a_edge_preserved'] for e in data['dependency_edge_dispositions'])


def test_edge_owners_match_merged_r1b_authority():
    data, r1b = load(ARTIFACT), load(R1B)
    terms = {term['term_id']: term for term in r1b['term_records']}
    for edge in data['dependency_edge_dispositions']:
        semantic_owner = edge['semantic_type_owner']
        bindings = semantic_owner['r1b_term_bindings']
        assert {b['term_id'] for b in bindings} == set(semantic_owner['r1b_terms'])
        for binding in bindings:
            term = terms[binding['term_id']]
            disposition = term['vocabulary_disposition']
            if disposition == 'qualified_canonical_family':
                assert binding.get('qualified_form'), 'qualified family must name its exact form'
                qualified = {q['qualified_form']: q for q in term['qualified_forms']}
                assert binding['qualified_form'] in qualified
                authority = qualified[binding['qualified_form']]
            else:
                assert 'qualified_form' not in binding
                authority = term['type_owner']
            assert (binding['owner_kind'], binding['owner_id']) == (authority['owner_kind'], authority['owner_id'])
            if disposition == 'escalated_unresolved':
                assert binding['owner_kind'] == 'unresolved_escalation'
            assert (semantic_owner['owner_kind'], semantic_owner['owner_id']) == (binding['owner_kind'], binding['owner_id'])
        assert edge['consumer_not_semantic_owner_by_consumption'] is True
        assert edge['ownership_does_not_transfer'] is True
        if semantic_owner['owner_id'] == edge['producer_afqr']:
            assert semantic_owner['ownership_basis'] in {'merged_r1b_term_owner', 'direct_source_contract_not_producer_status'}


def test_dispositions_have_direct_evidence_or_explicit_unresolved_status():
    for edge in load(ARTIFACT)['dependency_edge_dispositions']:
        assert edge['source_evidence_records'] or edge['r1c_status'] in {'escalated', 'unresolved', 'conditional'}
        assert edge['source_evidence_paths'] or edge['r1c_status'] in {'escalated', 'unresolved', 'conditional'}


def test_dep_094_is_a_typed_contact_to_target_handoff():
    edge = next(e for e in load(ARTIFACT)['dependency_edge_dispositions'] if e['edge_id'] == 'DEP-094')
    assert edge['producer_afqr'] == 'AFQR-20' and edge['consumer_afqr'] == 'AFQR-19'
    assert edge['semantic_type_owner']['owner_id'] == 'AFQR-19'
    assert edge['semantic_type_owner']['r1b_terms'] == ['TERM-011']
    assert 'AFQR-20 retains sensing/contact ownership' in edge['postconditions']
    assert 'detection does not itself establish a valid target' in edge['postconditions']


def test_cycles_have_exact_source_backed_edge_coverage_and_direction():
    data, matrix = load(ARTIFACT), load(MATRIX)
    r1a = {e['edge_id']: e for e in matrix['dependency_edges']}
    r1c = {e['edge_id']: e for e in data['dependency_edge_dispositions']}
    assert {tuple(c['afqrs']) for c in data['cycle_risk_resolutions']} == {tuple(g) for g in matrix['cycle_risk_groups']}
    expected_groups = {
        'CYCLE-001': {'DEP-008', 'DEP-061'}, 'CYCLE-002': {'DEP-021', 'DEP-024'},
        'CYCLE-003': {'DEP-048', 'DEP-052'}, 'CYCLE-004': {'DEP-089', 'DEP-091'},
    }
    coverage = {}
    for record in data['cycle_risk_resolutions'] + data['cycle_risk_reclassifications']:
        assert record['edge_ids']
        for edge_id in record['edge_ids']:
            assert edge_id in r1a and edge_id in r1c
            assert r1c[edge_id]['producer_afqr'] == r1a[edge_id]['from_afqr']
            assert r1c[edge_id]['consumer_afqr'] == r1a[edge_id]['to_afqr']
            coverage.setdefault(edge_id, []).append(record)
    for cycle in data['cycle_risk_resolutions']:
        assert set(cycle['edge_ids']) == expected_groups[cycle['cycle_id']]
        assert cycle['valid_edges_preserved'] is True
        assert cycle['resolution'] in {'bounded_feedback_rule', 'phase_ordering', 'escalation'}
        assert cycle['breaker']
    marked = {e['edge_id'] for e in r1c.values() if e['cycle_participation']}
    review = {e['edge_id'] for e in r1a.values() if e['cycle_risk'] == 'review_required'}
    assert marked == review == set(coverage)
    assert all(len(records) == 1 for records in coverage.values()), 'cycle-risk edge has incompatible duplicate treatments'


def test_corrected_cycle_owner_boundaries():
    cycles = {c['cycle_id']: c for c in load(ARTIFACT)['cycle_risk_resolutions']}
    command = cycles['CYCLE-002']['breaker'].lower()
    assert all(x in command for x in ['command identity', 'logical time', 'cannot create or redefine command identity', 'cannot author logical time'])
    assert 'truth/evidence' not in command
    identity = cycles['CYCLE-003']['breaker'].lower()
    assert all(x in identity for x in ['evidence admissibility', 'identity and continuity', 'cannot create identity', 'cannot self-certify admissibility or truth'])
    assert not any(x in identity for x in ['capability', 'opportunity', 'target ownership'])


def test_missing_substrates_are_individually_sourced_and_non_template():
    data, matrix = load(ARTIFACT), load(MATRIX)
    substrates = data['missing_substrate_classifications']
    assert {s['name'] for s in substrates} == set(matrix['dependencies_missing_from_repository'])
    signatures = set()
    for substrate in substrates:
        assert substrate['requiring_afqrs'] and substrate['source_evidence_records'] and substrate['source_evidence_paths']
        assert substrate['future_doctrine_owner'] and substrate['later_gate']
        assert 'must_not_implement' in substrate['r1c_must_not_implement']
        assert substrate['status'] == 'classified_unimplemented'
        signatures.add((substrate['why_required'], tuple(substrate['requiring_afqrs']), substrate['failure_or_collapse_risk']))
    assert len(signatures) == 5, 'substrates must not be identical template copies'
    by_id = {s['substrate_id']: s for s in substrates}
    assert {'AFQR-09', 'AFQR-13', 'AFQR-15'} <= set(by_id['SUB-001']['requiring_afqrs'])
    assert {'AFQR-04', 'AFQR-06', 'AFQR-10', 'AFQR-20'} <= set(by_id['SUB-002']['requiring_afqrs'])
    assert {'AFQR-01', 'AFQR-02', 'AFQR-04', 'AFQR-09'} <= set(by_id['SUB-003']['requiring_afqrs'])
    assert by_id['SUB-004']['requiring_afqrs'] == ['AFQR-05']
    assert {r['domain'] for r in by_id['SUB-005']['domain_owner_requirements']} == {'spatial/topology', 'signal/sensing', 'embodiment', 'institution/jurisdiction', 'social state'}


def test_cross_phase_prohibitions_and_hidden_truth_boundary():
    data, matrix = load(ARTIFACT), load(MATRIX)
    assert {p['risk'] for p in data['cross_phase_prohibitions']} == set(matrix['cross_phase_handoffs_at_risk'])
    assert all(p['governed_nonautomatic'] for p in data['cross_phase_prohibitions'])
    assert any(p.get('hidden_truth_direct_promotion_forbidden') for p in data['cross_phase_prohibitions'])
    assert any('hidden truth cannot leak' in i['summary'].lower() for i in data['cross_afqr_invariants'])


def test_preserved_escalations_no_downstream_authority_and_gates():
    data = load(ARTIFACT)
    assert {e['collision_id'] for e in data['preserved_escalations']} == {'COLL-03', 'COLL-08', 'COLL-10'}
    assert all(e['status'] == 'open' for e in data['preserved_escalations'])
    lower = data['authority_boundary'].lower()
    assert all(f'no {x}' in lower for x in ['runtime implementation', 'conversion execution', 'canon/sourcebook', 'model-facing', 'live-play'])
    gates = data['r1d_handoff_requirements']
    assert gates['r1d_must_not_be_marked_complete'] is True and gates['r1e_status'] == 'blocked'
    assert gates['r2_to_r6_status'] == 'blocked' and 'blocked' in gates['rt_002g_status']
    assert gates['temporary_evidence_deletion'] == 'unauthorized'


def test_committed_pr_diff_has_no_src_zip_binary_or_temporary_deletions():
    data = load(ARTIFACT)
    names = [line for line in committed_diff(data, '--name-only').splitlines() if line]
    assert not any(path.startswith('src/') for path in names)
    assert not any(path.lower().endswith('.zip') for path in names)
    numstat = committed_diff(data, '--numstat')
    assert not any(line.startswith('-\t-\t') for line in numstat.splitlines())
    status = committed_diff(data, '--name-status', '--diff-filter=D')
    deleted = [line.split('\t', 1)[1] for line in status.splitlines() if '\t' in line]
    assert not any(path.startswith('working/afqr_consolidation_inputs/') for path in deleted)


def test_production_code_does_not_import_temporary_evidence_or_r1c_reviews():
    needles = ['working/afqr_consolidation_inputs', 'afqr_r1c_invariant_dependency_resolution_report', 'afqr_r1c_unresolved_dependency_escalation_ledger']
    for path in (ROOT / 'src').rglob('*.py'):
        assert not any(n in path.read_text(errors='ignore') for n in needles)


def test_corpus_pressure_and_no_donor_defaults():
    findings = load(ARTIFACT)['corpus_pressure_findings']
    assert len(findings['covered_donor_families']) >= 18
    assert 'vehicles, mechs, ships, and platforms' in findings['covered_donor_families']
    expected = ['one cosmology', 'one anatomy', 'one identity model', 'one action economy', 'one resolution style', 'one progression model', 'one resource economy', 'one map topology', 'one sensing model', 'one legal or social system', 'one actor scale', 'one vehicle/operator relationship']
    assert set(expected) <= set(findings['forbidden_default_assumptions'])
    assert 'does not promote' in findings['finding']
