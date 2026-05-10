from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import pytest
jsonschema = pytest.importorskip('jsonschema')


def _init_run(tmp_path: Path):
    pr=tmp_path/'packets'; pr.mkdir(); p=pr/'pkt1'; p.mkdir(); (p/'conversion_prompt.md').write_text('# prompt',encoding='utf-8')
    plan={"plan_id":"x","packets":[{"packet_id":"pkt1","book_match":"book","start_page":1,"end_page":2,"readiness_hint":"ready_candidate"}]}
    planf=tmp_path/'plan.json'; planf.write_text(json.dumps(plan),encoding='utf-8')
    run=tmp_path/'run'
    subprocess.run([sys.executable,'scripts/handoff/init_conversion_intake_run.py','--packet-root',str(pr),'--selected-plan',str(planf),'--output-run-dir',str(run),'--run-id','r1'],check=True)
    return run


def test_scaffold_writes_valid_json(tmp_path: Path):
    run=_init_run(tmp_path)
    md=run/'results/pkt1_conversion_result.md'
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
""",encoding='utf-8')
    subprocess.run([sys.executable,'scripts/handoff/scaffold_conversion_intake_json.py','--run-dir',str(run),'--packet-id','pkt1','--status','drafted'],check=True)
    obj=json.loads((run/'results/pkt1_conversion_result.json').read_text())
    assert obj['result_status']=='drafted'
    assert obj['confidence']==0.77
    assert obj['mapping_ledger'][0]['lawful_outcome'] in ["direct Astra mapping","normalized Astra mapping","source-local retained construct","quarantined construct pending later doctrine","escalated doctrine problem"]
    schema=json.loads((Path('schemas/handoff/conversion_intake_result.schema.json').read_text()))
    jsonschema.validate(obj,schema)


def test_unknown_outcome_fallback_and_default_confidence(tmp_path: Path):
    run=_init_run(tmp_path)
    md=run/'results/pkt1_conversion_result.md'
    md.write_text("## Astra Mapping Ledger\n| A | weird outcome |\n",encoding='utf-8')
    subprocess.run([sys.executable,'scripts/handoff/scaffold_conversion_intake_json.py','--run-dir',str(run),'--packet-id','pkt1'],check=True)
    obj=json.loads((run/'results/pkt1_conversion_result.json').read_text())
    assert obj['confidence']==0.5
    assert obj['mapping_ledger'][0]['lawful_outcome']=='quarantined construct pending later doctrine'


def test_missing_markdown_or_packet_fails(tmp_path: Path):
    run=_init_run(tmp_path)
    (run/'results/pkt1_conversion_result.md').unlink()
    r=subprocess.run([sys.executable,'scripts/handoff/scaffold_conversion_intake_json.py','--run-dir',str(run),'--packet-id','pkt1'],capture_output=True,text=True)
    assert r.returncode!=0
    r2=subprocess.run([sys.executable,'scripts/handoff/scaffold_conversion_intake_json.py','--run-dir',str(run),'--packet-id','missing'],capture_output=True,text=True)
    assert r2.returncode!=0
