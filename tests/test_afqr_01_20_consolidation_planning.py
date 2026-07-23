"""Semantic completion gates for source-backed, text-only AFQR R1A planning."""
from __future__ import annotations
import hashlib, json, re, subprocess, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'working/afqr_consolidation_inputs'; REV=ROOT/'docs/doctrine/reviews'
BASE='43a50c3756c4f1ba335956d8224f22b34fc32ab5'
REQUIRED=[WORK/'README.md',WORK/'manifest.yaml',ROOT/'docs/doctrine/control/afqr_01_20_consolidation_program_plan.md',REV/'afqr_01_20_authority_status_index.yaml',REV/'afqr_01_20_dependency_matrix.yaml',REV/'afqr_01_20_shared_term_collision_inventory.md',REV/'afqr_01_20_consolidation_file_manifest.yaml',ROOT/'docs/doctrine/astra_doctrine_registry_v0_1.yaml',ROOT/'docs/decisions/current_decisions_log.md']
def load(p): return json.loads(p.read_text(encoding='utf8'))
def git(*args): return subprocess.run(['git',*args],cwd=ROOT,text=True,check=True,capture_output=True).stdout
def test_required_r1a_files_exist(): assert all(p.is_file() for p in REQUIRED)
def test_machine_yaml_artifacts_parse():
 for p in [WORK/'manifest.yaml',REV/'afqr_01_20_authority_status_index.yaml',REV/'afqr_01_20_dependency_matrix.yaml',REV/'afqr_01_20_consolidation_file_manifest.yaml']: assert isinstance(load(p),dict)
def test_twelve_unchanged_incoming_archives_and_hashes():
 m=load(WORK/'manifest.yaml'); assert len(m['archive_records'])==12
 assert not (WORK/'archives').exists()
 for r in m['archive_records']:
  p=ROOT/r['current_path']; assert p.parent==WORK/'incoming'; assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
  assert hashlib.sha256(subprocess.run(['git','show',f'{BASE}:{p.relative_to(ROOT)}'],cwd=ROOT,check=True,capture_output=True).stdout).hexdigest()==r['sha256']
  with zipfile.ZipFile(p) as z: assert z.testzip() is None
def test_every_archive_member_is_manifest_backed():
 m=load(WORK/'manifest.yaml'); records=m['contained_file_records']; assert len(records)==277
 by_archive={a['archive_record_id']:a for a in m['archive_records']}
 actual=set()
 for r in records: actual.add((r['parent_archive_record_id'],r['original_archive_path']))
 expected=set()
 for aid,a in by_archive.items():
  with zipfile.ZipFile(ROOT/a['current_path']) as z: expected|={(aid,i.filename) for i in z.infolist() if not i.is_dir()}
 assert actual==expected
def test_materialization_contracts_and_checksums():
 m=load(WORK/'manifest.yaml'); allowed={'committed_text_copy','archive_only_binary','archive_only_unsupported'}
 committed=[]
 for r in m['contained_file_records']:
  assert r['materialization_status'] in allowed and r['sha256'] and r['byte_size']>=0 and r['detected_file_type'] and r['parent_archive_record_id']
  if r['materialization_status']=='committed_text_copy':
   assert r['normalized_path']; p=ROOT/r['normalized_path']; data=p.read_bytes(); data.decode('utf-8'); assert b'\0' not in data; assert hashlib.sha256(data).hexdigest()==r['sha256']; committed.append(p)
  else: assert r['normalized_path'] is None
 assert len(committed)==22
 assert {p for p in (WORK/'extracted').rglob('*') if p.is_file()}==set(committed)
def test_exact_afqr_coverage_and_committed_primary_evidence():
 m=load(WORK/'manifest.yaml'); by_id={r['source_record_id']:r for r in m['contained_file_records']}
 a=load(REV/'afqr_01_20_authority_status_index.yaml')['afqr_records']; assert [x['afqr_id'] for x in a]==[f'AFQR-{n:02d}' for n in range(1,21)]
 assert len(a)==len({x['afqr_id'] for x in a})==20 and sum(r['selected_as_primary'] for r in by_id.values())==20
 for x in a:
  assert x['selected_architecture']
  for rid in x['source_evidence_records']: assert by_id[rid]['selected_as_primary'] and by_id[rid]['materialization_status']=='committed_text_copy'
def test_corrected_afqr14_is_explicit_and_materialized():
 m=load(WORK/'manifest.yaml'); recs=m['contained_file_records']; a=load(REV/'afqr_01_20_authority_status_index.yaml')['afqr_records'][13]
 assert 'corrected' in a['corrected_baseline_note'].lower(); assert sum(r['package_kind']=='corrected_answer' for r in recs)==1
 assert any(r['original_archive_path'].endswith('afqr_14_corrected_baseline_note.yaml') and r['materialization_status']=='committed_text_copy' for r in recs)
def test_dependency_edges_and_collision_references_are_valid():
 d=load(REV/'afqr_01_20_dependency_matrix.yaml'); valid={f'AFQR-{n:02d}' for n in range(1,21)}
 for e in d['dependency_edges']: assert e['from_afqr'] in valid and e['to_afqr'] in valid and e['source_evidence']
 existing=set(re.findall(r'COLL-\d\d',(REV/'afqr_01_20_shared_term_collision_inventory.md').read_text()))
 for a in load(REV/'afqr_01_20_authority_status_index.yaml')['afqr_records']: assert set(a['collision_ids'])<=existing
def test_controlled_values_and_temporary_nonauthority():
 statuses={'accepted_architectural_decision_not_implemented','partially_represented_by_narrow_fixture','partially_implemented','implemented_general_contract','tracking_only','conflict_detected','source_input_incomplete'}
 assert {a['repository_implementation_status'] for a in load(REV/'afqr_01_20_authority_status_index.yaml')['afqr_records']}<=statuses
 m=load(WORK/'manifest.yaml'); assert m['authority']=='temporary_non_authoritative_working_evidence_only'; assert all(r['status']=='temporary_non_authoritative_working_input' for r in m['archive_records']+m['contained_file_records'])
def test_pr_delta_has_no_zip_or_binary_changes():
 assert not git('diff','--name-only',BASE,'--','*.zip').strip()
 rows=[line.split('\t',2) for line in git('diff','--numstat',BASE).splitlines()]
 assert all(a!='-' and d!='-' for a,d,_ in rows)
 for path in git('diff','--name-only','--diff-filter=AM',BASE).splitlines():
  data=(ROOT/path).read_bytes(); data.decode('utf-8'); assert b'\0' not in data
def test_no_production_imports_and_later_gates_blocked():
 for p in (ROOT/'src').rglob('*.py'): assert 'afqr_consolidation_inputs' not in p.read_text(encoding='utf8')
 text=(ROOT/'docs/doctrine/control/afqr_01_20_consolidation_program_plan.md').read_text(); assert 'R2–R6' in text and 'RT-002G' in text and 'remain blocked' in text
def test_planned_ownership_and_nonownership_are_explicit():
 files=load(REV/'afqr_01_20_consolidation_file_manifest.yaml')['planned_files']
 assert len({f['file_id'] for f in files})==len(files)
 for f in files: assert f['owner'] and f['must_not_own'] and f['outlier_escalation_path']
