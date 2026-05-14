import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "handoff" / "audit_conversion_intake_quality.py"


def write_result(run_dir, packet_id, markdown, obj):
    results = run_dir / "results"
    results.mkdir(parents=True, exist_ok=True)
    (results / f"{packet_id}_conversion_result.md").write_text(markdown, encoding="utf-8")
    payload = {
        "packet_id": packet_id,
        "result_status": "drafted",
        "confidence": 0.5,
        "donor_construct_inventory": [],
        "mapping_ledger": [],
        "doctrine_escalations": [],
        "source_local_retentions": [],
        "rejected_imports": [],
        "canon_candidate_notes": [],
    }
    payload.update(obj)
    (results / f"{packet_id}_conversion_result.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )


def run_audit(run_dir, *extra):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--run-dir", str(run_dir), *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def load_report(run_dir):
    return json.loads((run_dir / "reports" / "conversion_intake_quality_audit.json").read_text(encoding="utf-8"))


def test_quality_audit_passes_for_rich_drafted_result(tmp_path):
    run_dir = tmp_path / "run"
    markdown = """# Memo

1. Extraction Readiness Assessment
Text.

2. Donor Construct Inventory
A. Construct one
B. Construct two

3. Astra Mapping Ledger
| Donor construct | Lawful outcome |
|---|---|
| One | normalized Astra mapping |
| Two | source-local retained construct |

4. Queue and Quarantine Actions
Text.

5. Lexicon Delta
Text.

6. Doctrine Escalations
Text.

7. Source-Local Retentions
- Donor proper nouns

8. Rejected Imports
- Do not import donor canon.

9. Canon Candidate Notes
None.

10. Conversion Notes
Text.

11. Confidence and Reviewer Notes
Confidence: high.
"""
    write_result(run_dir, "rich_packet", markdown, {
        "donor_construct_inventory": ["one", "two"],
        "mapping_ledger": [{"donor_construct": "one"}, {"donor_construct": "two"}],
        "source_local_retentions": ["Donor proper nouns"],
        "rejected_imports": ["Do not import donor canon."],
    })

    proc = run_audit(run_dir, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr

    report = load_report(run_dir)
    assert report["valid_quality_gate"] is True
    assert report["packets_with_errors"] == []


def test_quality_audit_fails_for_underparsed_rich_markdown(tmp_path):
    run_dir = tmp_path / "run"
    markdown = ("1. Extraction Readiness Assessment\nRich text.\n\n" * 250)
    write_result(run_dir, "underparsed_packet", markdown, {
        "donor_construct_inventory": [],
        "mapping_ledger": [{"fallback": True}],
        "source_local_retentions": [],
        "rejected_imports": [],
    })

    proc = run_audit(run_dir, "--strict")
    assert proc.returncode == 1

    report = load_report(run_dir)
    assert report["valid_quality_gate"] is False
    assert "underparsed_packet" in report["packets_with_errors"]
    codes = {
        issue["code"]
        for result in report["packet_results"]
        for issue in result["issues"]
    }
    assert "underparsed_mapping_ledger" in codes
    assert "missing_construct_inventory" in codes


def test_quality_audit_tolerates_backmatter_negative_control(tmp_path):
    run_dir = tmp_path / "run"
    markdown = """1. Extraction Readiness Assessment
This packet is credits/backmatter.

2. Donor Construct Inventory
A. Kickstarter backer list

3. Astra Mapping Ledger
| Donor construct | Lawful outcome |
|---|---|
| Backer names | source-local retained construct |

4. Queue and Quarantine Actions
False-positive table pressure.

5. Lexicon Delta
None.

6. Doctrine Escalations
Pipeline only.

7. Source-Local Retentions
Backer names.

8. Rejected Imports
Do not import as NPCs.

9. Canon Candidate Notes
None.

10. Conversion Notes
Non-convertible backmatter.

11. Confidence and Reviewer Notes
High confidence.
"""
    write_result(run_dir, "backmatter_packet", markdown, {
        "donor_construct_inventory": [],
        "mapping_ledger": [{"donor_construct": "backer names"}],
        "source_local_retentions": [],
        "rejected_imports": [],
    })

    proc = run_audit(run_dir, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr

    report = load_report(run_dir)
    detail = report["packet_results"][0]
    assert detail["low_value_backmatter"] is True
    assert report["valid_quality_gate"] is True


def test_quality_audit_warns_on_escaped_headings_without_failing(tmp_path):
    run_dir = tmp_path / "run"
    markdown = """1\\. Extraction Readiness Assessment
Text.

2\\. Donor Construct Inventory
A. Construct

3\\. Astra Mapping Ledger
| Donor construct | Lawful outcome |
|---|---|
| One | normalized Astra mapping |

4\\. Queue and Quarantine Actions
Text.

5\\. Lexicon Delta
Text.

6\\. Doctrine Escalations
Text.

7\\. Source-Local Retentions
- Donor term.

8\\. Rejected Imports
- Do not import.

9\\. Canon Candidate Notes
None.

10\\. Conversion Notes
Text.

11\\. Confidence and Reviewer Notes
Confidence: medium.
"""
    write_result(run_dir, "escaped_packet", markdown, {
        "donor_construct_inventory": ["one"],
        "mapping_ledger": [{"donor_construct": "one"}, {"donor_construct": "two"}],
        "source_local_retentions": ["Donor term"],
        "rejected_imports": ["Do not import."],
    })

    proc = run_audit(run_dir, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr

    report = load_report(run_dir)
    codes = {
        issue["code"]
        for result in report["packet_results"]
        for issue in result["issues"]
    }
    assert "escaped_numbered_headings" in codes
