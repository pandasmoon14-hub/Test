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
    # "## 1. Foo" or "## Foo"
    m = re.match(r"^#+\s*(?:\d+\.\s+)?(.+?)\s*$", s)
    if m:
        return m.group(1)
    # "1. Foo" (numbered, no #)
    m = re.match(r"^\d+\.\s+(.+?)\s*$", s)
    if m:
        return m.group(1)
    return None


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
    return not any(kw in t2 for kw in [
        'direct', 'normalized', 'source-local', 'source local', 'source_local',
        'escalated', 'quarantine',
    ])


def _build_col_map(header_cells: list[str]) -> dict[str, int]:
    col_map: dict[str, int] = {}
    for i, h in enumerate(header_cells):
        hl = h.lower().strip()
        if 'donor' not in col_map and ('donor' in hl or hl == 'construct'):
            col_map['donor'] = i
        elif 'outcome' not in col_map and 'outcome' in hl:
            col_map['outcome'] = i
        elif 'pages' not in col_map and ('source pages' in hl or hl == 'units'):
            col_map['pages'] = i
        elif 'family' not in col_map and ('target family' in hl or 'astra target' in hl or hl == 'family'):
            col_map['family'] = i
        elif 'rationale' not in col_map and ('rationale' in hl or 'notes' in hl):
            col_map['rationale'] = i
    return col_map


def _get_cell(cells: list[str], idx: int, default: str) -> str:
    if 0 <= idx < len(cells) and cells[idx]:
        return cells[idx]
    return default


def _is_separator(ln: str) -> bool:
    return bool(re.match(r"^\|?[\s\-:|]+\|?$", ln.strip()) and '--' in ln)


def parse_mapping_table(section_text: str, start_page: int, packet_id: str) -> list[dict]:
    table_lines = [ln for ln in section_text.splitlines() if '|' in ln]
    if not table_lines:
        return []

    sep_idx = next((i for i, ln in enumerate(table_lines) if _is_separator(ln)), None)
    col_map: dict[str, int] = {}
    data_start = 0

    if sep_idx is not None and sep_idx > 0:
        header_cells = [c.strip().lower() for c in table_lines[sep_idx - 1].strip('|').split('|')]
        col_map = _build_col_map(header_cells)
        data_start = sep_idx + 1

    mappings = []
    for ln in table_lines[data_start:]:
        if _is_separator(ln):
            continue
        cells = [c.strip() for c in ln.strip('|').split('|')]
        if not any(cells):
            continue

        donor = _get_cell(cells, col_map.get('donor', 0), 'unparsed_construct')
        outcome_text = _get_cell(cells, col_map.get('outcome', 1), '')
        family = _get_cell(cells, col_map.get('family', 2), 'unknown')
        rationale = _get_cell(cells, col_map.get('rationale', 3), 'scaffolded from markdown memo')

        outcome = norm_outcome(outcome_text)
        if _outcome_is_unknown(outcome_text):
            note = f'fallback normalization: unrecognized outcome "{outcome_text.strip()}"'
            rationale = f"{note}; original: {rationale}" if rationale != 'scaffolded from markdown memo' else note

        canon = (
            'candidate_only_after_review'
            if re.search(r'candidate only after review|candidate after review|review required', ln, re.I)
            else 'none'
        )

        mappings.append({
            'donor_construct': donor or 'unparsed_construct',
            'source_pages': [start_page],
            'source_unit_ids': [f"{packet_id}_unit"],
            'astra_target_family': family or 'unknown',
            'lawful_outcome': outcome,
            'rationale': rationale or 'scaffolded from markdown memo',
            'must_not_import': False,
            'doctrine_owner': None,
            'canon_candidate_permission': canon,
            'confidence': 0.5,
        })

    return mappings


def parse_inventory(text: str) -> list[dict]:
    items = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        m = re.match(r"^[A-Za-z]\.\s+(.+)$", ln)
        if m:
            items.append({"text": m.group(1)})
            continue
        m = re.match(r"^\d+\.\s+(.+)$", ln)
        if m:
            items.append({"text": m.group(1)})
            continue
        m = re.match(r"^[-*]\s+(.+)$", ln)
        if m:
            items.append({"text": m.group(1)})
            continue
        items.append({"text": ln})
    return items


def parse_list_section(text: str) -> list[dict]:
    items = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        if '|' in ln and not _is_separator(ln):
            cells = [c.strip() for c in ln.strip('|').split('|') if c.strip()]
            if cells:
                items.append({"text": cells[0]})
                continue
        m = re.match(r"^(?:[A-Za-z]\.|[-*]|\d+\.)\s+(.+)$", ln)
        items.append({"text": m.group(1) if m else ln})
    return items


def parse_confidence(text: str) -> float:
    values = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = re.search(r"confidence\s*[:=]\s*([0-9]*\.?[0-9]+)", s, re.I)
        if m:
            values.append(float(m.group(1)))
            continue
        m = re.search(r"confidence\s*[:=]\s*(medium-high|medium-low|high|medium|low)\b", s, re.I)
        if m:
            label = m.group(1).lower()
            values.append(CONFIDENCE_LABELS[label])
    return sum(values) / len(values) if values else 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--packet-id', required=True)
    ap.add_argument('--status', default='drafted')
    a = ap.parse_args()
    run = Path(a.run_dir)
    idx_path = run / 'packet_index.json'
    if not idx_path.exists():
        print('missing packet_index.json', file=sys.stderr)
        sys.exit(1)
    idx = json.loads(idx_path.read_text(encoding='utf-8'))
    rec = next((r for r in idx if r.get('packet_id') == a.packet_id), None)
    if rec is None:
        print('packet id not found', file=sys.stderr)
        sys.exit(1)
    md_path = run / 'results' / f"{a.packet_id}_conversion_result.md"
    if not md_path.exists():
        print('missing markdown result', file=sys.stderr)
        sys.exit(1)
    sections = parse_sections(md_path.read_text(encoding='utf-8'))

    start_page = int(rec['page_range']['start_page'])
    inv = parse_inventory(sections['Donor Construct Inventory'])

    mappings = parse_mapping_table(sections['Astra Mapping Ledger'], start_page, a.packet_id)
    if not mappings:
        mappings = [{
            'donor_construct': 'memo_summary_construct',
            'source_pages': [start_page],
            'source_unit_ids': [f"{a.packet_id}_unit"],
            'astra_target_family': 'unknown',
            'lawful_outcome': 'quarantined construct pending later doctrine',
            'rationale': 'No parseable mapping table; conservative fallback',
            'must_not_import': False,
            'doctrine_owner': None,
            'canon_candidate_permission': 'none',
            'confidence': 0.5,
        }]

    conf = parse_confidence(sections['Confidence and Reviewer Notes'])

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
        'queue_actions': parse_list_section(sections['Queue and Quarantine Actions']),
        'lexicon_delta': parse_list_section(sections['Lexicon Delta']),
        'doctrine_escalations': parse_list_section(sections['Doctrine Escalations']),
        'source_local_retentions': parse_list_section(sections['Source-Local Retentions']),
        'rejected_imports': parse_list_section(sections['Rejected Imports']),
        'canon_candidate_notes': sections['Canon Candidate Notes'],
        'conversion_notes': sections['Conversion Notes'],
        'reviewer_notes': sections['Confidence and Reviewer Notes'],
        'confidence': conf,
    }

    schema = json.loads(
        (Path(__file__).resolve().parents[2] / 'schemas/handoff/conversion_intake_result.schema.json')
        .read_text(encoding='utf-8')
    )
    jsonschema.validate(obj, schema)
    out = run / 'results' / f"{a.packet_id}_conversion_result.json"
    out.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    print(json.dumps({'packet_id': a.packet_id, 'written': str(out)}, indent=2))


if __name__ == '__main__':
    main()
