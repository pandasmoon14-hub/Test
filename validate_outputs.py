#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--strict', action='store_true')
    args=ap.parse_args()
    out=Path(args.output_dir)
    books=[p for p in out.iterdir() if p.is_dir() and (p/(p.name+'.md')).exists()]
    summary={"total_books":0,"books_passed":0,"books_failed":0,"books_needing_repair":0,"total_pages":0,"pages_ok":0,"pages_queued":0,"pages_failed":0,"pages_image_only":0,"pages_ocr_needed":0,"pages_ocr_done":0,"invalid_artifact_count":0,"missing_artifact_count":0,"top_error_codes":{}}
    errors=Counter()
    for b in books:
        summary['total_books']+=1
        sa=b/'strict_audit.json'; ah=b/'astra_handoff_manifest.json'; pt=b/f'{b.name}.page_truth.jsonl'
        if not sa.exists() or not ah.exists() or not pt.exists():
            summary['missing_artifact_count']+=1; summary['books_failed']+=1; continue
        audit=json.loads(sa.read_text())
        hand=json.loads(ah.read_text())
        for e in audit.get('errors',[]): errors[e]+=1
        if audit.get('strict_audit_status')=='pass': summary['books_passed']+=1
        else: summary['books_failed']+=1
        if hand.get('conversion_readiness')=='needs_repair': summary['books_needing_repair']+=1
        summary['total_pages']+=int(hand.get('page_count',0))
        summary['pages_ok']+=int(hand.get('pages_ok',0)); summary['pages_queued']+=int(hand.get('pages_queued',0))
        summary['pages_failed']+=int(hand.get('pages_failed',0)); summary['pages_image_only']+=int(hand.get('pages_image_only',0))
        summary['pages_ocr_needed']+=int(hand.get('pages_ocr_needed',0)); summary['pages_ocr_done']+=int(hand.get('pages_ocr_done',0))
    summary['top_error_codes']=dict(errors.most_common(20))
    out_path=out/'corpus_validation_summary.json'
    out_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))
    if args.strict and (summary['books_failed']>0 or summary['missing_artifact_count']>0 or summary['invalid_artifact_count']>0):
        raise SystemExit(1)

if __name__=='__main__':
    main()
