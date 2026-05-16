from __future__ import annotations

import json
from pathlib import Path

from scripts.handoff.aggregate_conversion_intake_results import aggregate_run


def write_result(path: Path, packet_id: str, book_id: str, mappings: list[dict], confidence: float = 0.75) -> None:
    obj = {
        "result_id": f"{packet_id}_conversion_result",
        "packet_id": packet_id,
        "book_id": book_id,
        "source_packet_dir": f"C:/fake/packets/{packet_id}",
        "page_range": {"start_page": 1, "end_page": 2},
        "result_status": "drafted",
        "extraction_readiness_assessment": "usable for conversion-stage intake only",
        "donor_construct_inventory": [{"text": "inventory"}],
        "mapping_ledger": mappings,
        "queue_actions": [{"text": "queue one"}],
        "lexicon_delta": [{"text": "lexicon one"}],
        "doctrine_escalations": [{"text": "escalation one"}],
        "source_local_retentions": [{"text": "retention one"}],
        "rejected_imports": [{"text": "reject one"}],
        "canon_candidate_notes": "No canon candidates should be emitted at this stage.",
        "conversion_notes": "notes",
        "reviewer_notes": "reviewer notes",
        "confidence": confidence,
    }
    path.write_text(json.dumps(obj), encoding="utf-8")


def mapping(construct: str, outcome: str, target: str = "Ability / power framework") -> dict:
    return {
        "donor_construct": construct,
        "source_pages": [1],
        "source_unit_ids": ["unit_1"],
        "astra_target_family": target,
        "lawful_outcome": outcome,
        "rationale": "test rationale",
        "must_not_import": outcome in {"source-local retained construct", "quarantined construct pending later doctrine", "escalated doctrine problem"},
        "doctrine_owner": "batchA_07_ability_object_model.md",
        "canon_candidate_permission": "none",
        "confidence": 0.8,
    }


def test_aggregate_run_writes_reports(tmp_path: Path) -> None:
    run_dir = tmp_path / "conversion_intake_run"
    results = run_dir / "results"
    results.mkdir(parents=True)
    out_dir = tmp_path / "aggregation"

    write_result(
        results / "one_conversion_result.json",
        "one_pages_1_2",
        "Fate Core",
        [
            mapping("aspect tags", "normalized Astra mapping", "Narrative tag/aspect framework"),
            mapping("proper noun setting", "source-local retained construct", "Source-local setting material"),
        ],
    )
    write_result(
        results / "two_conversion_result.json",
        "two_pages_1_2",
        "Traveller Core",
        [
            mapping("jump drive cosmology", "quarantined construct pending later doctrine", "Starship/platform doctrine"),
            mapping("trade law", "escalated doctrine problem", "Trade/economy doctrine"),
        ],
        confidence=0.5,
    )

    report = aggregate_run(run_dir=run_dir, output_dir=out_dir, confidence_review_threshold=0.67)

    assert report["packets_total"] == 2
    assert report["lawful_outcome_counts"]["normalized Astra mapping"] == 1
    assert report["lawful_outcome_counts"]["source-local retained construct"] == 1
    assert report["lawful_outcome_counts"]["quarantined construct pending later doctrine"] == 1
    assert report["lawful_outcome_counts"]["escalated doctrine problem"] == 1
    assert len(report["doctrine_pressure"]["quarantined_mapping_entries"]) == 1
    assert len(report["doctrine_pressure"]["escalated_mapping_entries"]) == 1
    assert len(report["human_review_queue"]) >= 1
    assert (out_dir / "batch_001_aggregation_report.json").exists()
    assert (out_dir / "batch_001_aggregation_report.md").exists()
    assert (out_dir / "batch_001_quarantine_escalation_queue.csv").exists()

