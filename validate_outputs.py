from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path


def load_manifest(p: Path):
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    out = Path(args.output_dir)
    manifests = list((out / 'manifests').glob('*.manifest.json'))
    summary = {
        'total_books': len(manifests),
        'books_artifact_valid': 0,
        'books_artifact_invalid': 0,
        'books_conversion_ready': 0,
        'books_ready_with_warnings': 0,
        'books_needing_repair': 0,
        'books_failed_extraction': 0,
        'total_pages': 0,
        'pages_ok': 0,
        'pages_empty': 0,
        'pages_image_only': 0,
        'pages_ocr_needed': 0,
        'pages_ocr_done': 0,
        'pages_queued': 0,
        'pages_failed': 0,
        'invalid_artifact_count': 0,
        'missing_artifact_count': 0,
        'top_error_codes': [],
    }
    errors = Counter()
    for mf in manifests:
        m = load_manifest(mf)
        if not m:
            summary['books_artifact_invalid'] += 1
            summary['invalid_artifact_count'] += 1
            continue
        summary['books_artifact_valid'] += 1
        for k in ['pages_ok','pages_empty','pages_image_only','pages_ocr_needed','pages_ocr_done','pages_queued','pages_failed','total_pages']:
            summary[k] += int(m.get(k,0))
        rc = m.get('reason_code_counts', {}) or {}
        errors.update(rc)
        if m.get('pages_ocr_needed',0) or m.get('pages_queued',0) or m.get('pages_failed',0) or m.get('pages_image_only',0):
            summary['books_needing_repair'] += 1
        elif m.get('pages_empty',0):
            summary['books_ready_with_warnings'] += 1
        else:
            summary['books_conversion_ready'] += 1
    summary['top_error_codes'] = [k for k,_ in errors.most_common(10)]
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
