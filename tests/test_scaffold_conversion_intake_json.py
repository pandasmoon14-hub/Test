from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

jsonschema = pytest.importorskip('jsonschema')


# ---------------------------------------------------------------------------
# Module loader — imports parsing helpers directly for unit tests
# ---------------------------------------------------------------------------

_sjs = None


def _get_sjs():
    global _sjs
    if _sjs is None:
        mod_path = Path(__file__).resolve().parent.parent / 'scripts' / 'handoff' / 'scaffold_conversion_intake_json.py'
        spec = importlib.util.spec_from_file_location('scaffold_conversion_intake_json', mod_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _sjs = mod
    return _sjs


# ---------------------------------------------------------------------------
# Integration helpers
# ---------------------------------------------------------------------------

def _init_run(tmp_path: Path):
    pr = tmp_path / 'packets'
    pr.mkdir()
    p = pr / 'pkt1'
    p.mkdir()
    (p / 'conversion_prompt.md').write_text('# prompt', encoding='utf-8')
    plan = {
        "plan_id": "x",
        "packets": [{"packet_id": "pkt1", "book_match": "book", "start_page": 1, "end_page": 2, "readiness_hint": "ready_candidate"}],
    }
    planf = tmp_path / 'plan.json'
    planf.write_text(json.dumps(plan), encoding='utf-8')
    run = tmp_path / 'run'
    subprocess.run(
        [sys.executable, 'scripts/handoff/init_conversion_intake_run.py',
         '--packet-root', str(pr), '--selected-plan', str(planf),
         '--output-run-dir', str(run), '--run-id', 'r1'],
        check=True,
    )
    return run


# ---------------------------------------------------------------------------
# Existing integration tests (unchanged)
# ---------------------------------------------------------------------------

def test_scaffold_writes_valid_json(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text("""# Conversion
## Extraction Readiness Assessment
ready-ish
## Donor Construct Inventory
- construct A
## Astra Mapping Ledger
| donor | outcome | family | rationale |
|---|---|---|---|
| A | direct mapping | fam | reason |
## Queue and Quarantine Actions
- none
## Lexicon Delta
- term
## Doctrine Escalations
- esc
## Source-Local Retentions
- ret
## Rejected Imports
- rej
## Canon Candidate Notes
candidate maybe
## Conversion Notes
notes
## Confidence and Reviewer Notes
confidence: 0.77
""", encoding='utf-8')
    subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'pkt1', '--status', 'drafted'],
        check=True,
    )
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    assert obj['result_status'] == 'drafted'
    assert obj['confidence'] == 0.77
    assert obj['mapping_ledger'][0]['lawful_outcome'] in [
        "direct Astra mapping", "normalized Astra mapping", "source-local retained construct",
        "quarantined construct pending later doctrine", "escalated doctrine problem",
    ]
    schema = json.loads(Path('schemas/handoff/conversion_intake_result.schema.json').read_text())
    jsonschema.validate(obj, schema)


def test_unknown_outcome_fallback_and_default_confidence(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text("## Astra Mapping Ledger\n| A | weird outcome |\n", encoding='utf-8')
    subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'pkt1'],
        check=True,
    )
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    assert obj['confidence'] == 0.5
    assert obj['mapping_ledger'][0]['lawful_outcome'] == 'quarantined construct pending later doctrine'


def test_missing_markdown_or_packet_fails(tmp_path: Path):
    run = _init_run(tmp_path)
    (run / 'results/pkt1_conversion_result.md').unlink()
    r = subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'pkt1'],
        capture_output=True, text=True,
    )
    assert r.returncode != 0
    r2 = subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'missing'],
        capture_output=True, text=True,
    )
    assert r2.returncode != 0


# ---------------------------------------------------------------------------
# Unit tests — section heading parsing
# ---------------------------------------------------------------------------

def test_parse_sections_hash_heading():
    sjs = _get_sjs()
    md = "## Extraction Readiness Assessment\ngood\n## Donor Construct Inventory\n- item"
    sec = sjs.parse_sections(md)
    assert sec['Extraction Readiness Assessment'] == 'good'
    assert '- item' in sec['Donor Construct Inventory']


def test_parse_sections_numbered_no_hash():
    sjs = _get_sjs()
    md = "1. Extraction Readiness Assessment\ngood\n2. Donor Construct Inventory\n- item"
    sec = sjs.parse_sections(md)
    assert sec['Extraction Readiness Assessment'] == 'good'
    assert '- item' in sec['Donor Construct Inventory']


def test_parse_sections_numbered_with_hash():
    sjs = _get_sjs()
    md = "## 1. Extraction Readiness Assessment\ngood\n## 2. Donor Construct Inventory\n- item"
    sec = sjs.parse_sections(md)
    assert sec['Extraction Readiness Assessment'] == 'good'
    assert '- item' in sec['Donor Construct Inventory']


# ---------------------------------------------------------------------------
# Unit tests — lawful outcome normalization
# ---------------------------------------------------------------------------

def test_norm_outcome_display_strings():
    sjs = _get_sjs()
    assert sjs.norm_outcome('direct Astra mapping') == 'direct Astra mapping'
    assert sjs.norm_outcome('normalized Astra mapping') == 'normalized Astra mapping'
    assert sjs.norm_outcome('source-local retained construct') == 'source-local retained construct'
    assert sjs.norm_outcome('quarantined construct pending later doctrine') == 'quarantined construct pending later doctrine'
    assert sjs.norm_outcome('escalated doctrine problem') == 'escalated doctrine problem'


def test_norm_outcome_underscore_strings():
    sjs = _get_sjs()
    assert sjs.norm_outcome('direct_astra_mapping') == 'direct Astra mapping'
    assert sjs.norm_outcome('normalized_astra_mapping') == 'normalized Astra mapping'
    assert sjs.norm_outcome('source_local_retained_construct') == 'source-local retained construct'
    assert sjs.norm_outcome('quarantined_construct_pending_later_doctrine') == 'quarantined construct pending later doctrine'
    assert sjs.norm_outcome('escalated_doctrine_problem') == 'escalated doctrine problem'


def test_norm_outcome_unknown_fallback():
    sjs = _get_sjs()
    assert sjs.norm_outcome('') == 'quarantined construct pending later doctrine'
    assert sjs.norm_outcome('garbled text') == 'quarantined construct pending later doctrine'
    assert sjs.norm_outcome('weird outcome') == 'quarantined construct pending later doctrine'


# ---------------------------------------------------------------------------
# Unit tests — mapping table parsing
# ---------------------------------------------------------------------------

def test_parse_mapping_table_header_detection():
    sjs = _get_sjs()
    text = (
        "| donor construct | lawful outcome | astra target family | rationale |\n"
        "|---|---|---|---|\n"
        "| Stress Track | direct Astra mapping | stress | fits well |"
    )
    rows = sjs.parse_mapping_table(text, 1, 'pkt1')
    assert len(rows) == 1
    assert rows[0]['donor_construct'] == 'Stress Track'
    assert rows[0]['lawful_outcome'] == 'direct Astra mapping'
    assert rows[0]['astra_target_family'] == 'stress'
    assert rows[0]['rationale'] == 'fits well'


def test_parse_mapping_table_multiple_rows():
    sjs = _get_sjs()
    text = (
        "| construct | outcome | family | notes |\n"
        "|---|---|---|---|\n"
        "| A | direct Astra mapping | fam1 | r1 |\n"
        "| B | normalized Astra mapping | fam2 | r2 |"
    )
    rows = sjs.parse_mapping_table(text, 1, 'pkt1')
    assert len(rows) == 2
    assert rows[0]['lawful_outcome'] == 'direct Astra mapping'
    assert rows[1]['lawful_outcome'] == 'normalized Astra mapping'


def test_parse_mapping_table_unknown_outcome_adds_note():
    sjs = _get_sjs()
    text = (
        "| construct | outcome | family | notes |\n"
        "|---|---|---|---|\n"
        "| X | gibberish | fam | orig |"
    )
    rows = sjs.parse_mapping_table(text, 1, 'pkt1')
    assert len(rows) == 1
    assert rows[0]['lawful_outcome'] == 'quarantined construct pending later doctrine'
    assert 'fallback' in rows[0]['rationale'].lower()


def test_parse_mapping_table_underscore_outcome():
    sjs = _get_sjs()
    text = (
        "| construct | outcome | family | notes |\n"
        "|---|---|---|---|\n"
        "| Y | normalized_astra_mapping | fam | note |"
    )
    rows = sjs.parse_mapping_table(text, 1, 'pkt1')
    assert rows[0]['lawful_outcome'] == 'normalized Astra mapping'


# ---------------------------------------------------------------------------
# Unit tests — donor construct inventory
# ---------------------------------------------------------------------------

def test_parse_inventory_lettered():
    sjs = _get_sjs()
    text = "A. First construct\nB. Second construct\nC. Third construct"
    items = sjs.parse_inventory(text)
    assert len(items) == 3
    assert items[0]['text'] == 'First construct'
    assert items[1]['text'] == 'Second construct'
    assert items[2]['text'] == 'Third construct'


def test_parse_inventory_bullets():
    sjs = _get_sjs()
    text = "- item one\n- item two"
    items = sjs.parse_inventory(text)
    assert len(items) == 2
    assert items[0]['text'] == 'item one'


def test_parse_inventory_mixed():
    sjs = _get_sjs()
    text = "- bullet item\nA. lettered item"
    items = sjs.parse_inventory(text)
    assert len(items) == 2
    assert items[0]['text'] == 'bullet item'
    assert items[1]['text'] == 'lettered item'


# ---------------------------------------------------------------------------
# Unit tests — list section parsing
# ---------------------------------------------------------------------------

def test_parse_list_section_bullets():
    sjs = _get_sjs()
    text = "- Retention A\n- Retention B"
    items = sjs.parse_list_section(text)
    assert len(items) == 2
    assert items[0]['text'] == 'Retention A'
    assert items[1]['text'] == 'Retention B'


def test_parse_list_section_lettered():
    sjs = _get_sjs()
    text = "A. First item\nB. Second item"
    items = sjs.parse_list_section(text)
    assert len(items) == 2
    assert items[0]['text'] == 'First item'


def test_parse_list_section_table_row():
    sjs = _get_sjs()
    text = "| Construct X | reason |"
    items = sjs.parse_list_section(text)
    assert len(items) == 1
    assert items[0]['text'] == 'Construct X'


# ---------------------------------------------------------------------------
# Unit tests — confidence parsing
# ---------------------------------------------------------------------------

def test_parse_confidence_numeric():
    sjs = _get_sjs()
    assert sjs.parse_confidence("confidence: 0.77") == 0.77


def test_parse_confidence_labels():
    sjs = _get_sjs()
    assert sjs.parse_confidence("confidence: high") == 0.8
    assert sjs.parse_confidence("confidence: medium-high") == 0.7
    assert sjs.parse_confidence("confidence: medium") == 0.5
    assert sjs.parse_confidence("confidence: medium-low") == 0.35
    assert sjs.parse_confidence("confidence: low") == 0.2


def test_parse_confidence_averaging():
    sjs = _get_sjs()
    val = sjs.parse_confidence("confidence: high\nconfidence: medium")
    assert abs(val - 0.65) < 1e-9


def test_parse_confidence_no_signal():
    sjs = _get_sjs()
    assert sjs.parse_confidence("reviewer notes only") == 0.5
    assert sjs.parse_confidence("") == 0.5


# ---------------------------------------------------------------------------
# Integration tests — richer sections
# ---------------------------------------------------------------------------

def test_scaffold_source_local_retentions_non_empty(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text(
        "## Astra Mapping Ledger\n"
        "## Source-Local Retentions\n"
        "- Fate-specific fate point bidding\n"
        "- Conflict framing step\n",
        encoding='utf-8',
    )
    subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'pkt1'],
        check=True,
    )
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    assert len(obj['source_local_retentions']) >= 2
    assert any('Fate' in item['text'] for item in obj['source_local_retentions'])


def test_scaffold_rejected_imports_non_empty(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text(
        "## Astra Mapping Ledger\n"
        "## Rejected Imports\n"
        "- Stunts as written\n"
        "- Skill list as-is\n",
        encoding='utf-8',
    )
    subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'pkt1'],
        check=True,
    )
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    assert len(obj['rejected_imports']) >= 2


def test_scaffold_canon_notes_non_empty_no_promotion(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text(
        "## Astra Mapping Ledger\n"
        "## Canon Candidate Notes\n"
        "Aspect framing may be candidate only after review.\n",
        encoding='utf-8',
    )
    subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'pkt1'],
        check=True,
    )
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    assert obj['canon_candidate_notes'].strip()
    for entry in obj['mapping_ledger']:
        assert entry['canon_candidate_permission'] in ('none', 'candidate_only_after_review')


def test_scaffold_multiple_confidence_labels_average(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text(
        "## Astra Mapping Ledger\n"
        "## Confidence and Reviewer Notes\n"
        "confidence: high\n"
        "confidence: medium\n",
        encoding='utf-8',
    )
    subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'pkt1'],
        check=True,
    )
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    assert abs(obj['confidence'] - 0.65) < 1e-9


def test_scaffold_fallback_no_table(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text(
        "## Astra Mapping Ledger\nSee conversion memo for details.\n",
        encoding='utf-8',
    )
    subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'pkt1'],
        check=True,
    )
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    assert len(obj['mapping_ledger']) == 1
    assert obj['mapping_ledger'][0]['lawful_outcome'] == 'quarantined construct pending later doctrine'


def test_scaffold_donor_inventory_lettered_list(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text(
        "## Donor Construct Inventory\n"
        "A. Stress Track\n"
        "B. Consequence Slots\n"
        "C. Fate Points\n"
        "## Astra Mapping Ledger\n",
        encoding='utf-8',
    )
    subprocess.run(
        [sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py',
         '--run-dir', str(run), '--packet-id', 'pkt1'],
        check=True,
    )
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    assert len(obj['donor_construct_inventory']) == 3
    texts = [item['text'] for item in obj['donor_construct_inventory']]
    assert 'Stress Track' in texts
    assert 'Consequence Slots' in texts
    assert 'Fate Points' in texts


def test_escaped_pipes_in_mapping_cells_preserved():
    sjs = _get_sjs()
    warns = []
    text = (
        "| donor construct | lawful outcome | astra target family | rationale |\n"
        "|---|---|---|---|\n"
        "| Arcane \\| Burst | normalized Astra mapping | spell | uses \\| escaped |"
    )
    rows = sjs.parse_mapping_table(text, 1, 'pkt1', warns)
    assert rows[0]['donor_construct'] == 'Arcane | Burst'
    assert 'uses | escaped' in rows[0]['rationale']


def test_source_local_and_rejected_structured_entries():
    sjs = _get_sjs()
    warns = []
    src = sjs.parse_source_local("- Local Name\n", warns)
    rej = sjs.parse_rejected("- Forbidden Import\n")
    assert src[0]['retained_construct'] == 'Local Name'
    assert src[0]['review_required'] is True
    assert rej[0]['must_not_import'] is True


def test_inventory_items_missing_from_mapping_emit_warning(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text("""## Donor Construct Inventory
A. Thing A
- Thing B
## Astra Mapping Ledger
| donor construct | lawful outcome |
|---|---|
| Thing A | direct Astra mapping |
## Confidence and Reviewer Notes
""", encoding='utf-8')
    subprocess.run([sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py', '--run-dir', str(run), '--packet-id', 'pkt1'], check=True)
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    assert 'inventory_not_in_mapping:Thing B' in obj['conversion_notes']


def test_unknown_lawful_outcome_warning_and_quarantine():
    sjs = _get_sjs()
    warns = []
    rows = sjs.parse_mapping_table(
        "| donor | outcome |\n|---|---|\n| X | nonsense |\n", 1, 'pkt1', warns
    )
    assert rows[0]['lawful_outcome'] == 'quarantined construct pending later doctrine'
    assert any('unknown_outcome' in w for w in warns)


def test_mapping_row_lossless_fields_schema_valid(tmp_path: Path):
    run = _init_run(tmp_path)
    md = run / 'results/pkt1_conversion_result.md'
    md.write_text("""## Donor Construct Inventory
- X
## Astra Mapping Ledger
| donor construct | lawful outcome | rationale |
|---|---|---|
| X | normalized Astra mapping | reason |
## Confidence and Reviewer Notes
confidence: 0.7
""", encoding='utf-8')
    subprocess.run([sys.executable, 'scripts/handoff/scaffold_conversion_intake_json.py', '--run-dir', str(run), '--packet-id', 'pkt1'], check=True)
    obj = json.loads((run / 'results/pkt1_conversion_result.json').read_text())
    row = obj['mapping_ledger'][0]
    assert 'raw_markdown_row' in row
    assert isinstance(row.get('parse_warnings'), list)


def test_parse_mapping_table_old_signature_still_works():
    sjs = _get_sjs()
    rows = sjs.parse_mapping_table("| A | direct Astra mapping |\n", 1, 'pkt1')
    assert isinstance(rows, list)


def test_parse_confidence_old_signature_still_works():
    sjs = _get_sjs()
    assert sjs.parse_confidence('') == 0.5


def test_supplied_parse_warnings_receives_warning():
    sjs = _get_sjs()
    warns = []
    sjs.parse_confidence('', warns)
    assert any('missing_confidence' in w for w in warns)
