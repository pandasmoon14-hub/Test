from __future__ import annotations
import argparse, json, re
from pathlib import Path


def _load_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]


def _parse_pages(md: str):
    pat = re.compile(r"<!--\s*PAGE:(\d+)\s*-->\s*", re.I)
    parts = pat.split(md)
    out = {}
    i=1
    while i < len(parts):
        out[int(parts[i])] = (parts[i+1] if i+1 < len(parts) else '').strip()
        i += 2
    return out


def _slug(s: str):
    s=s.lower()
    s=re.sub(r'[^a-z0-9]+','_',s).strip('_')
    return s or 'book'


def _tags(text: str):
    t=text.lower(); tags=[]
    if re.search(r'\bd(100|20|12|10|8|6|4)\b|roll table|\|',t): tags.append('random_table')
    if any(k in t for k in ['item','equipment','treasure','gear','cargo']): tags.append('item_list')
    if any(k in t for k in ['rule','procedure','check','action','resource','cost']): tags.append('mechanics_prose')
    if any(k in t for k in ['dungeon','location','room','encounter','hook','trap','faction']): tags.append('adventure_site')
    if any(k in t for k in ['map','diagram','hex','grid','keyed location','area']): tags.append('map_dependency')
    if re.search(r'\bac\b|\bhp\b|\bcr\b|attack|damage|stat block',t): tags.append('statblock_pressure')
    if any(k in t for k in ['class','background','ancestry','species','feat','skill','path','progression']): tags.append('character_options')
    if any(k in t for k in ['history','nation','region','god','cosmology']): tags.append('setting_lore')
    if any(k in t for k in ['vehicle','starship','mech','frame','hull','crew']): tags.append('vehicle_platform')
    if any(k in t for k in ['spell','power','technique','ability','maneuver']): tags.append('spell_power_catalog')
    return tags or ['unknown']


def _purpose(tags):
    st=set(tags)
    if 'adventure_site' in st: return 'Auto-selected adventure-site packet for location/scenario conversion-handoff intake.'
    if 'random_table' in st or 'item_list' in st: return 'Auto-selected table/list packet for table-normalization and conversion-handoff intake.'
    if 'mechanics_prose' in st: return 'Auto-selected mechanics-prose packet for conversion-handoff intake.'
    return 'Auto-selected mixed-content packet for conversion-handoff intake.'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-output-root', required=True)
    ap.add_argument('--output-plan', required=True)
    ap.add_argument('--plan-id', required=True)
    ap.add_argument('--mode', default='auto')
    ap.add_argument('--max-pages-per-packet', type=int, default=25)
    ap.add_argument('--min-text-chars', type=int, default=500)
    ap.add_argument('--include-repair-pages', action='store_true')
    a=ap.parse_args()

    root=Path(a.source_output_root)
    warnings=[]; packets=[]
    scanned=0; skipped=0; with_packets=0

    for book in sorted([d for d in root.iterdir() if d.is_dir()]):
        scanned += 1
        manifest=book/'astra_handoff_manifest.json'
        pt_files=list(book.glob('*.page_truth.jsonl'))
        md_files=list(book.glob('*.md'))
        if not manifest.exists() or not pt_files or not md_files:
            skipped += 1
            warnings.append(f'skipped_book_missing_artifacts:{book.name}')
            continue
        pt=_load_jsonl(pt_files[0])
        pages=_parse_pages(md_files[0].read_text(encoding='utf-8'))
        good=[]; repair=[]
        for r in pt:
            p=int(r.get('page',0)); st=str(r.get('page_status',''))
            txt=pages.get(p,'')
            if p<=3 and len(pt)>8: continue
            if st in {'ok','ocr_done'} and len(txt)>=a.min_text_chars:
                good.append(p)
            elif st in {'queued','failed','ocr_needed'}:
                repair.append(p)
            elif st in {'ok','ocr_done'} and len(txt)>=max(80, a.min_text_chars//4):
                good.append(p)
        selected_pages = sorted(set(good))
        if a.include_repair_pages and repair:
            selected_pages = sorted(set(selected_pages) | set(repair))
        if not selected_pages:
            skipped += 1
            warnings.append(f'skipped_book_insufficient_content:{book.name}')
            continue
        good=selected_pages
        # split contiguous + max size
        ranges=[]; s=good[0]; prev=good[0]
        for p in good[1:]:
            if p==prev+1 and (p-s+1)<=a.max_pages_per_packet:
                prev=p
            else:
                ranges.append((s,prev)); s=prev=p
        ranges.append((s,prev))

        for s,e in ranges:
            sel=[pages.get(i,'') for i in range(s,e+1)]
            all_text='\n'.join(sel)
            tags=_tags(all_text)
            repair_near=[p for p in repair if s<=p<=e]
            if repair_near and a.include_repair_pages:
                rh='needs_repair_candidate'; w=['repair_pages_included']
            elif repair_near:
                rh='repair_avoided'; w=['nearby_repair_pages_excluded']
            elif any(len(pages.get(i,''))<a.min_text_chars for i in range(s,e+1)):
                rh='ready_with_warnings_candidate'; w=['sparse_pages_present']
            else:
                rh='ready_candidate'; w=[]
            if any(t in tags for t in ['random_table','item_list','map_dependency','statblock_pressure']):
                rh = 'intake_only_candidate' if rh=='ready_candidate' else rh
            pkt={
                'packet_id': f"{_slug(book.name)}_pages_{s}_{e}",
                'book_match': book.name,
                'start_page': s,
                'end_page': e,
                'packet_purpose': _purpose(tags),
                'content_family_tags': tags,
                'readiness_hint': rh,
                'selection_reason': 'auto_contiguous_usable_pages',
                'warnings': w,
            }
            packets.append(pkt)
        with_packets += 1

    plan={
        'plan_id': a.plan_id,
        'source_output_root': str(root),
        'generator_version': 'handoff_plan_generator_v0_1',
        'mode': a.mode,
        'max_pages_per_packet': a.max_pages_per_packet,
        'min_text_chars': a.min_text_chars,
        'books_scanned': scanned,
        'books_with_packets': with_packets,
        'books_skipped': skipped,
        'warnings': warnings,
        'packets': packets,
    }
    out=Path(a.output_plan)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2), encoding='utf-8')
    print(json.dumps(plan, indent=2))


if __name__=='__main__':
    main()
