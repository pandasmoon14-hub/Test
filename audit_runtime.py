from __future__ import annotations
import json
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import re

MARKER_RE = re.compile(r"\s*<!--\s*PAGE:(\d+)\s*-->")

@dataclass
class StrictAuditReport:
    book_id: str
    source_sha256: str
    source_page_count: int
    page_truth_count: int
    markdown_page_marker_count: int
    missing_page_truth_pages: list[int]
    missing_markdown_pages: list[int]
    duplicate_page_truth_pages: list[int]
    duplicate_markdown_pages: list[int]
    disposition_counts: dict[str, int]
    schema_validation: dict[str, Any]
    warnings: list[str]
    errors: list[str]
    strict_audit_status: str
    conversion_readiness: str


def parse_page_markers(md: str) -> list[int]:
    nums=[]
    for ln in md.splitlines():
        m=MARKER_RE.match(ln.strip())
        if m:
            nums.append(int(m.group(1)))
    return nums


def validate_page_truth_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows=[];errs=[]
    for i,line in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row=json.loads(line)
            rows.append(row)
        except Exception as exc:
            errs.append(f"page_truth_jsonl_parse_error:{i}:{exc}")
    return rows, errs


def strict_audit_book(book_id:str, source_sha:str, source_page_count:int, md_path:Path, page_truth_path:Path, page_meta_path:Path, table_sidecar_path:Path) -> StrictAuditReport:
    errors=[]; warnings=[]
    pt_rows, pt_err = validate_page_truth_jsonl(page_truth_path)
    errors.extend(pt_err)
    md_pages=parse_page_markers(md_path.read_text(encoding='utf-8', errors='replace')) if md_path.exists() else []
    pt_pages=[int(r.get('page_number_one_based',-1)) for r in pt_rows]
    mset=set(md_pages); pset=set(pt_pages); expected=set(range(1, source_page_count+1))
    missing_pt=sorted(expected-pset); missing_md=sorted(expected-mset)
    dup_pt=sorted([k for k,v in Counter(pt_pages).items() if v>1])
    dup_md=sorted([k for k,v in Counter(md_pages).items() if v>1])

    schema_validation={"page_truth_jsonl": not bool(pt_err), "page_meta_json": page_meta_path.exists(), "table_sidecar_json": table_sidecar_path.exists()}
    disposition_counts=dict(Counter([r.get('page_status','unknown') for r in pt_rows]))
    if missing_pt: errors.append('missing_page_truth_pages')
    if missing_md: errors.append('missing_markdown_pages')
    if dup_pt: errors.append('duplicate_page_truth_pages')
    if dup_md: errors.append('duplicate_markdown_pages')
    if len(pt_rows)!=source_page_count: errors.append('page_truth_count_mismatch')
    if len(md_pages)!=source_page_count: errors.append('markdown_page_count_mismatch')

    if errors:
        status='fail'; readiness='failed'
    elif disposition_counts.get('failed',0) or disposition_counts.get('queued',0):
        status='pass'; readiness='needs_repair'
    elif disposition_counts.get('image_only',0) or disposition_counts.get('empty',0):
        status='pass'; readiness='ready_with_warnings'
    else:
        status='pass'; readiness='ready'
    return StrictAuditReport(book_id,source_sha,source_page_count,len(pt_rows),len(md_pages),missing_pt,missing_md,dup_pt,dup_md,disposition_counts,schema_validation,warnings,errors,status,readiness)


def write_json(path:Path, data:Any)->None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
