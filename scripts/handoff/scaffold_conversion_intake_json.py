from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import jsonschema

HEADERS = [
    "Extraction Readiness Assessment", "Donor Construct Inventory", "Astra Mapping Ledger",
    "Queue and Quarantine Actions", "Lexicon Delta", "Doctrine Escalations",
    "Source-Local Retentions", "Rejected Imports", "Canon Candidate Notes",
    "Conversion Notes", "Confidence and Reviewer Notes",
]
OUTCOMES = [
    "direct Astra mapping", "normalized Astra mapping", "source-local retained construct",
    "quarantined construct pending later doctrine", "escalated doctrine problem",
]
CONFIDENCE_LABELS = {
    'high': 0.8, 'medium-high': 0.7, 'medium': 0.5, 'medium-low': 0.35, 'low': 0.2,
}
_OUTCOME_UNDER_MAP = {
    'direct_astra_mapping': 'direct Astra mapping',
    'normalized_astra_mapping': 'normalized Astra mapping',
    'source_local_retained_construct': 'source-local retained construct',
    'quarantined_construct_pending_later_doctrine': 'quarantined construct pending later doctrine',
    'escalated_doctrine_problem': 'escalated doctrine problem',
}


def _extract_heading(ln: str) -> str | None:
    s = ln.strip()
    m = re.match(r"^#+\s*(?:\d+\.\s+)?(.+?)\s*$", s)
    if m:
        return m.group(1)
    m = re.match(r"^\d+\.\s+(.+?)\s*$", s)
    return m.group(1) if m else None


def parse_sections(md: str) -> dict[str, str]:
    lines = md.splitlines()
    sections = {h: "" for h in HEADERS}
    cur = None
    buf: list[str] = []
    for ln in lines:
        heading = _extract_heading(ln)
        if heading is not None and heading in sections:
            if cur is not None:
                sections[cur] = "\n".join(buf).strip()
            cur = heading
            buf = []
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        sections[cur] = "\n".join(buf).strip()
    return sections


def norm_outcome(t: str) -> str:
    t2 = t.strip().lower()
    under = t2.replace(' ', '_').replace('-', '_')
    if under in _OUTCOME_UNDER_MAP:
        return _OUTCOME_UNDER_MAP[under]
    if 'direct' in t2: return OUTCOMES[0]
    if 'normalized' in t2: return OUTCOMES[1]
    if 'source-local' in t2 or 'source local' in t2 or 'source_local' in t2: return OUTCOMES[2]
    if 'escalated' in t2: return OUTCOMES[4]
    if 'quarantine' in t2: return OUTCOMES[3]
    return OUTCOMES[3]


def _outcome_is_unknown(t: str) -> bool:
    t2 = t.strip().lower()
    under = t2.replace(' ', '_').replace('-', '_')
    if under in _OUTCOME_UNDER_MAP:
        return False
    return not any(kw in t2 for kw in ['direct', 'normalized', 'source-local', 'source local', 'source_local', 'escalated', 'quarantine'])


def split_markdown_row(ln: str) -> list[str]:
    s = ln.strip().strip('|')
    out, cur, esc = [], [], False
    for ch in s:
        if esc:
            cur.append(ch); esc = False; continue
        if ch == '\\':
            esc = True; continue
        if ch == '|':
            out.append(''.join(cur).strip()); cur = []; continue
        cur.append(ch)
    out.append(''.join(cur).strip())
    return out


def _build_col_map(header_cells: list[str]) -> dict[str, int]:
    col_map: dict[str, int] = {}
    for i, h in enumerate(header_cells):
        hl = h.lower().strip()
        if 'donor' not in col_map and ('donor' in hl or hl == 'construct' or 'label' in hl): col_map['donor'] = i
        elif 'outcome' not in col_map and 'outcome' in hl: col_map['outcome'] = i
        elif 'pages' not in col_map and ('source pages' in hl or 'page ref' in hl): col_map['pages'] = i
        elif 'unit_ids' not in col_map and ('unit id' in hl or 'source unit' in hl): col_map['unit_ids'] = i
        elif 'family' not in col_map and ('target family' in hl or 'astra target' in hl or hl == 'family'): col_map['family'] = i
        elif 'rationale' not in col_map and ('rationale' in hl or 'notes' in hl): col_map['rationale'] = i
        elif 'owner' not in col_map and ('owner' in hl): col_map['owner'] = i
        elif 'canon' not in col_map and ('canon' in hl and 'permission' in hl): col_map['canon'] = i
        elif 'confidence' not in col_map and 'confidence' in hl: col_map['confidence'] = i
    return col_map


def _is_separator(ln: str) -> bool:
    return bool(re.match(r"^\|?[\s\-:|]+\|?$", ln.strip()) and '--' in ln)


def _parse_conf(v: str) -> float | None:
    s = v.strip().lower()
    if not s: return None
    m = re.search(r"([0-9]*\.?[0-9]+)\s*%", s)
    if m: return max(0.0, min(1.0, float(m.group(1))/100.0))
    m = re.search(r"([0-9]*\.?[0-9]+)", s)
    if m:
        x = float(m.group(1))
        return x/100.0 if x > 1.0 else x
    if s in CONFIDENCE_LABELS: return CONFIDENCE_LABELS[s]
    return None


def parse_mapping_table(section_text: str, start_page: int, packet_id: str, parse_warnings: list[str] | None = None) -> list[dict]:
    if parse_warnings is None:
        parse_warnings = []
    table_lines = [ln for ln in section_text.splitlines() if '|' in ln]
    if not table_lines: return []
    sep_idx = next((i for i, ln in enumerate(table_lines) if _is_separator(ln)), None)
    col_map, data_start = {}, 0
    if sep_idx is not None and sep_idx > 0:
        col_map = _build_col_map([c.strip().lower() for c in split_markdown_row(table_lines[sep_idx - 1])])
        data_start = sep_idx + 1

    mappings = []
    for ln in table_lines[data_start:]:
        if _is_separator(ln): continue
        cells = split_markdown_row(ln)
        if not any(cells): continue
        donor = cells[col_map.get('donor', 0)] if col_map.get('donor', 0) < len(cells) else 'unparsed_construct'
        outcome_text = cells[col_map.get('outcome', 1)] if col_map.get('outcome', 1) < len(cells) else ''
        family = cells[col_map.get('family', 2)] if col_map.get('family', 2) < len(cells) else 'unknown'
        rationale = cells[col_map.get('rationale', 3)] if col_map.get('rationale', 3) < len(cells) else 'scaffolded from markdown memo'
        pages_text = cells[col_map['pages']] if 'pages' in col_map and col_map['pages'] < len(cells) else ''
        unit_text = cells[col_map['unit_ids']] if 'unit_ids' in col_map and col_map['unit_ids'] < len(cells) else ''
        owner = cells[col_map['owner']] if 'owner' in col_map and col_map['owner'] < len(cells) else None
        canon_text = cells[col_map['canon']] if 'canon' in col_map and col_map['canon'] < len(cells) else ''
        conf_text = cells[col_map['confidence']] if 'confidence' in col_map and col_map['confidence'] < len(cells) else ''

        outcome = norm_outcome(outcome_text)
        if _outcome_is_unknown(outcome_text):
            parse_warnings.append(f"unknown_outcome:{donor}:{outcome_text}")
            rationale = f"fallback normalization from unknown outcome ({outcome_text}); {rationale}"

        canon = 'candidate_only_after_review' if re.search(r'candidate|review required|review_required', canon_text + ' ' + ln, re.I) else 'none'
        if re.search(r'approved|final|canonized', canon_text, re.I):
            parse_warnings.append(f"canon_permission_downgraded:{donor}")
            canon = 'candidate_only_after_review'

        conf = _parse_conf(conf_text)
        if conf is None:
            conf = 0.5
            parse_warnings.append(f"missing_confidence_mapping:{donor}")

        source_pages = [start_page]
        if pages_text:
            nums = [int(x) for x in re.findall(r"\d+", pages_text)]
            if nums: source_pages = nums
        source_unit_ids = [f"{packet_id}_unit"] if not unit_text else [u.strip() for u in re.split(r"[,;|]", unit_text) if u.strip()]

        must_not = outcome in ('source-local retained construct', 'quarantined construct pending later doctrine', 'escalated doctrine problem')
        mappings.append({
            'donor_construct': donor or 'unparsed_construct',
            'source_pages': source_pages,
            'source_unit_ids': source_unit_ids,
            'astra_target_family': family or 'unknown',
            'lawful_outcome': outcome,
            'rationale': rationale or 'scaffolded from markdown memo',
            'must_not_import': must_not,
            'doctrine_owner': owner or None,
            'canon_candidate_permission': canon,
            'confidence': conf,
            'raw_markdown_row': ln.strip(),
            'parse_warnings': [],
        })
    return mappings


def parse_inventory(text: str) -> list[dict]:
    items = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln: continue
        m = re.match(r"^[A-Za-z]\.\s+(.+)$", ln) or re.match(r"^\d+\.\s+(.+)$", ln) or re.match(r"^[-*]\s+(.+)$", ln)
        items.append({"text": m.group(1) if m else ln})
    return items


def parse_list_section(text: str) -> list[dict]:
    items = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln: continue
        if '|' in ln and not _is_separator(ln):
            cells = [c for c in split_markdown_row(ln) if c]
            if cells:
                items.append({"text": cells[0], "raw": ln}); continue
        m = re.match(r"^(?:[A-Za-z]\.|[-*]|\d+\.)\s+(.+)$", ln)
        items.append({"text": m.group(1) if m else ln, "raw": ln})
    return items


def parse_confidence(text: str, parse_warnings: list[str] | None = None) -> float:
    if parse_warnings is None:
        parse_warnings = []
    vals = []
    for ln in text.splitlines():
        c = _parse_conf(ln)
        if c is not None: vals.append(c)
    if not vals:
        parse_warnings.append("missing_confidence_global_default_0.5")
        return 0.5
    return sum(vals) / len(vals)


def parse_source_local(text: str, parse_warnings: list[str]) -> list[dict]:
    out = []
    for it in parse_list_section(text):
        t = it.get("text", "")
        out.append({
            "retained_construct": t,
            "boundary_scope_note": "source-local retention from memo section",
            "rationale": t,
            "source_reference": None,
            "review_required": True,
            "raw": it.get("raw", t),
        })
    return out


def parse_rejected(text: str) -> list[dict]:
    out = []
    for it in parse_list_section(text):
        t = it.get("text", "")
        out.append({
            "rejected_donor_construct": t,
            "reason": t,
            "must_not_import": True,
            "raw": it.get("raw", t),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--packet-id', required=True)
    ap.add_argument('--status', default='drafted')
    a = ap.parse_args()
    run = Path(a.run_dir)
    idx_path = run / 'packet_index.json'
    if not idx_path.exists(): print('missing packet_index.json', file=sys.stderr); sys.exit(1)
    idx = json.loads(idx_path.read_text(encoding='utf-8'))
    rec = next((r for r in idx if r.get('packet_id') == a.packet_id), None)
    if rec is None: print('packet id not found', file=sys.stderr); sys.exit(1)
    md_path = run / 'results' / f"{a.packet_id}_conversion_result.md"
    if not md_path.exists(): print('missing markdown result', file=sys.stderr); sys.exit(1)
    sections = parse_sections(md_path.read_text(encoding='utf-8'))

    parse_warnings: list[str] = []
    start_page = int(rec['page_range']['start_page'])
    inv = parse_inventory(sections['Donor Construct Inventory'])
    inv_texts = [i.get('text', '').strip() for i in inv if i.get('text')]

    mappings = parse_mapping_table(sections['Astra Mapping Ledger'], start_page, a.packet_id, parse_warnings)
    if not mappings:
        parse_warnings.append('no_mapping_table_fallback_row_created')
        mappings = [{
            'donor_construct': 'memo_summary_construct', 'source_pages': [start_page], 'source_unit_ids': [f"{a.packet_id}_unit"],
            'astra_target_family': 'unknown', 'lawful_outcome': 'quarantined construct pending later doctrine',
            'rationale': 'No parseable mapping table; conservative fallback', 'must_not_import': True,
            'doctrine_owner': None, 'canon_candidate_permission': 'none', 'confidence': 0.5,
            'raw_markdown_row': '', 'parse_warnings': ['fallback_row']
        }]

    mapped = {m['donor_construct'].strip().lower() for m in mappings}
    for t in inv_texts:
        if t.lower() not in mapped:
            parse_warnings.append(f"inventory_not_in_mapping:{t}")

    for m in mappings:
        if m['lawful_outcome'] in ('quarantined construct pending later doctrine', 'escalated doctrine problem'):
            pass

    queue_actions = parse_list_section(sections['Queue and Quarantine Actions'])
    for m in mappings:
        if m['lawful_outcome'] in ('quarantined construct pending later doctrine', 'escalated doctrine problem'):
            queue_actions.append({'text': f"auto-queue:{m['donor_construct']}:{m['lawful_outcome']}", 'source': 'scaffold_auto'})

    source_local = parse_source_local(sections['Source-Local Retentions'], parse_warnings)
    rejected = parse_rejected(sections['Rejected Imports'])

    canon_notes = sections['Canon Candidate Notes']
    if re.search(r'approved|final|canonized', canon_notes, re.I):
        parse_warnings.append('canon_candidate_notes_downgraded_to_review_required')

    conf = parse_confidence(sections['Confidence and Reviewer Notes'], parse_warnings)

    obj = {
        'result_id': f"{a.packet_id}_conversion_result",
        'packet_id': a.packet_id,
        'book_id': rec.get('book_id', 'unknown'),
        'source_packet_dir': rec.get('packet_dir', ''),
        'page_range': rec.get('page_range', {'start_page': 1, 'end_page': 1}),
        'result_status': a.status,
        'extraction_readiness_assessment': sections['Extraction Readiness Assessment'] or rec.get('readiness_class', 'unknown'),
        'donor_construct_inventory': inv,
        'mapping_ledger': mappings,
        'queue_actions': queue_actions,
        'lexicon_delta': parse_list_section(sections['Lexicon Delta']),
        'doctrine_escalations': parse_list_section(sections['Doctrine Escalations']),
        'source_local_retentions': source_local,
        'rejected_imports': rejected,
        'canon_candidate_notes': canon_notes,
        'conversion_notes': ((sections['Conversion Notes'] + "\n\n" if sections['Conversion Notes'] else "") + "Parse warnings:\n- " + "\n- ".join(parse_warnings)) if parse_warnings else sections['Conversion Notes'],
        'reviewer_notes': sections['Confidence and Reviewer Notes'],
        'confidence': conf,
    }

    schema = json.loads((Path(__file__).resolve().parents[2] / 'schemas/handoff/conversion_intake_result.schema.json').read_text(encoding='utf-8'))
    jsonschema.validate(obj, schema)
    out = run / 'results' / f"{a.packet_id}_conversion_result.json"
    out.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    print(json.dumps({'packet_id': a.packet_id, 'written': str(out)}, indent=2))


if __name__ == '__main__':
    main()
