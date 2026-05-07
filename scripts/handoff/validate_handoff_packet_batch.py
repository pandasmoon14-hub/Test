from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from collections import Counter, defaultdict

from scripts.handoff.validate_handoff_packet import validate_packet


def _merge_counter(dst: dict, src: dict):
    c = Counter(dst)
    c.update(src)
    return dict(c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--packet-root', required=True)
    ap.add_argument('--strict', action='store_true')
    a = ap.parse_args()

    root = Path(a.packet_root)
    if not root.exists() or not root.is_dir():
        raise SystemExit('packet root not found')

    candidates = [p for p in root.iterdir() if p.is_dir() and (p / 'packet_manifest.json').exists()]
    errors = []
    warnings = []
    if a.strict and not candidates:
        errors.append('no_packet_folders_found')

    agg = {
        'page_truth_rows': 0,
        'extracted_page_markers': 0,
        'content_units': 0,
        'extraction_defects': 0,
        'queue_records_by_queue': {},
        'page_status_counts': {},
        'content_unit_type_counts': {},
        'readiness_counts': {},
    }

    packet_reports = []
    packet_ids = []
    invalid_packet_ids = []

    for p in candidates:
        try:
            rep, _ = validate_packet(p, strict=a.strict)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            rep = {'packet_id': p.name, 'packet_dir': str(p), 'valid': False, 'errors': [f'packet_validator_exception:{exc}'], 'warnings': [], 'counts': {}}
        packet_reports.append(rep)
        pid = rep.get('packet_id', p.name)
        packet_ids.append(pid)
        if not rep.get('valid', False):
            invalid_packet_ids.append(pid)

        c = rep.get('counts', {})
        agg['page_truth_rows'] += int(c.get('page_truth_rows', 0))
        agg['extracted_page_markers'] += int(c.get('extracted_page_markers', 0))
        agg['content_units'] += int(c.get('content_units', 0))
        agg['extraction_defects'] += int(c.get('extraction_defects', 0))
        agg['queue_records_by_queue'] = _merge_counter(agg['queue_records_by_queue'], c.get('queue_records_by_queue', {}))
        agg['page_status_counts'] = _merge_counter(agg['page_status_counts'], c.get('page_status_counts', {}))
        agg['content_unit_type_counts'] = _merge_counter(agg['content_unit_type_counts'], c.get('content_unit_type_counts', {}))
        agg['readiness_counts'] = _merge_counter(agg['readiness_counts'], c.get('readiness_counts', {}))

    summary = {
        'packet_root': str(root),
        'valid': len(errors) == 0 and len(invalid_packet_ids) == 0,
        'strict': bool(a.strict),
        'packets_total': len(candidates),
        'packets_valid': len(candidates) - len(invalid_packet_ids),
        'packets_invalid': len(invalid_packet_ids),
        'packet_ids': packet_ids,
        'invalid_packet_ids': invalid_packet_ids,
        'errors': errors,
        'warnings': warnings,
        'counts': agg,
        'packet_reports': packet_reports,
    }

    (root / 'handoff_batch_validation_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))

    if a.strict and (errors or invalid_packet_ids):
        sys.exit(1)


if __name__ == '__main__':
    main()
