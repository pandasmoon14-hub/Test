from __future__ import annotations
import argparse, json, re
from pathlib import Path

SUPPORT_DIRS = {"failed_books","failed_queue","logs","manifests","repair_queue","table_sidecars","queues","sidecars"}


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
    return re.sub(r'[^a-z0-9]+','_',s.lower()).strip('_') or 'book'


def _score_tags(text: str):
    t=text.lower(); sc={}
    patterns={
        'random_table': [r'\bd(100|20|12|10|8|6|4)\b', r'roll table', r'\|'],
        'item_list': [r'item|equipment|treasure|gear|cargo'],
        'mechanics_prose': [r'rule|procedure|check|action|resource|cost'],
        'adventure_site': [r'dungeon|location|room|encounter|hook|trap|faction'],
        'map_dependency': [r'map|diagram|hex|grid|keyed location|area'],
        'statblock_pressure': [r'\bac\b|\bhp\b|\bcr\b|attack|damage|stat block'],
        'character_options': [r'class|background|ancestry|species|feat|skill|path|progression'],
        'setting_lore': [r'history|nation|region|god|cosmology'],
        'vehicle_platform': [r'vehicle|starship|mech|frame|hull|crew'],
        'spell_power_catalog': [r'spell|power|technique|ability|maneuver'],
    }
    for k,pats in patterns.items():
        sc[k]=sum(len(re.findall(p,t)) for p in pats)
    return sc


def _purpose(dom):
    m={
        'mechanics_prose':'Auto-selected mechanics-prose packet for conversion-handoff intake.',
        'random_table':'Auto-selected table/list packet for table-normalization and conversion-handoff intake.',
        'item_list':'Auto-selected table/list packet for table-normalization and conversion-handoff intake.',
        'adventure_site':'Auto-selected adventure-site packet for location/scenario conversion-handoff intake.',
        'setting_lore':'Auto-selected setting-lore packet for conversion-handoff intake.',
        'character_options':'Auto-selected character-options packet for conversion-handoff intake.',
        'vehicle_platform':'Auto-selected vehicle/platform packet for conversion-handoff intake.',
        'spell_power_catalog':'Auto-selected spell/power catalog packet for conversion-handoff intake.',
    }
    return m.get(dom,'Auto-selected mixed-content packet for conversion-handoff intake.')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-output-root', required=True)
    ap.add_argument('--output-plan', required=True)
    ap.add_argument('--plan-id', required=True)
    ap.add_argument('--mode', default='auto')
    ap.add_argument('--selection-strategy', default='pilot', choices=['pilot','coverage'])
    ap.add_argument('--max-pages-per-packet', type=int, default=25)
    ap.add_argument('--min-pages-per-packet', type=int, default=3)
    ap.add_argument('--min-text-chars', type=int, default=500)
    ap.add_argument('--max-packets-total', type=int, default=0)
    ap.add_argument('--max-packets-per-book', type=int, default=0)
    ap.add_argument('--max-tags-per-packet', type=int, default=4)
    ap.add_argument('--include-repair-pages', action='store_true')
    a=ap.parse_args()

    root=Path(a.source_output_root)
    warnings=[]; packets=[]; ignored=[]
    scanned=0; skipped=0; with_packets=0
    default_max_per_book = a.max_packets_per_book if a.max_packets_per_book>0 else (3 if a.selection_strategy=='pilot' else 9999)

    for book in sorted([d for d in root.iterdir() if d.is_dir()]):
        if book.name in SUPPORT_DIRS:
            ignored.append(book.name)
            continue
        scanned += 1
        manifest=book/'astra_handoff_manifest.json'; pt_files=list(book.glob('*.page_truth.jsonl')); md_files=list(book.glob('*.md'))
        if not manifest.exists() or not pt_files or not md_files:
            skipped += 1; warnings.append(f'skipped_book_missing_artifacts:{book.name}'); continue
        pt=_load_jsonl(pt_files[0]); pages=_parse_pages(md_files[0].read_text(encoding='utf-8'))

        eligible=[]
        for r in pt:
            p=int(r.get('page',0)); st=str(r.get('page_status','')); txt=pages.get(p,'')
            if p<=3 and len(pt)>8: continue
            if st in {'ok','ocr_done'} and len(txt)>=max(80,a.min_text_chars//4): eligible.append(p)
            elif a.include_repair_pages and st in {'queued','failed','ocr_needed','image_only'}: eligible.append(p)
        eligible=sorted(set(eligible))
        if not eligible:
            skipped += 1; warnings.append(f'skipped_book_insufficient_content:{book.name}'); continue

        ranges=[]; s=eligible[0]; prev=eligible[0]
        for p in eligible[1:]:
            if p==prev+1 and (p-s+1)<=a.max_pages_per_packet: prev=p
            else: ranges.append((s,prev)); s=prev=p
        ranges.append((s,prev))

        candidates=[]
        for s,e in ranges:
            if (e-s+1) < a.min_pages_per_packet and len(ranges)>1:
                continue
            sel_rows=[r for r in pt if s<=int(r.get('page',0))<=e]
            sel_text='\n'.join(pages.get(i,'') for i in range(s,e+1))
            text_char_count=len(sel_text)
            statuses=[str(r.get('page_status','')) for r in sel_rows]
            repair_count=sum(1 for st in statuses if st in {'queued','failed','ocr_needed','image_only'})
            usable_count=sum(1 for st in statuses if st in {'ok','ocr_done'})
            sparse_count=sum(1 for i in range(s,e+1) if len(pages.get(i,''))<a.min_text_chars)
            scores=_score_tags(sel_text)
            top=sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
            tags=[k for k,v in top if v>=2][:a.max_tags_per_packet]
            if not tags: tags=['unknown']
            dom=tags[0]
            if repair_count>0:
                rh='needs_repair_candidate'; w=['repair_pages_included']
            elif sparse_count>0 or any(st=='ocr_done' for st in statuses):
                rh='ready_with_warnings_candidate'; w=['sparse_or_ocr_pages']
            else:
                rh='ready_candidate'; w=[]
            if dom in {'random_table','item_list','map_dependency','statblock_pressure'} and rh=='ready_candidate': rh='intake_only_candidate'
            quality = usable_count*2 - repair_count*3 - sparse_count + text_char_count/1000.0
            candidates.append({
                'packet_id':f"{_slug(book.name)}_pages_{s}_{e}",'book_match':book.name,'start_page':s,'end_page':e,
                'packet_purpose':_purpose(dom),'content_family_tags':tags,'dominant_content_family':dom,
                'readiness_hint':rh,'selection_reason':'auto_contiguous_usable_pages','warnings':w,
                'quality_score':round(quality,3),'text_char_count':text_char_count,'usable_page_count':usable_count,
                'repair_page_count':repair_count,'sparse_page_count':sparse_count,
            })

        if a.selection_strategy=='pilot':
            # reduce near-duplicates by dominant tag
            chosen=[]; seen=set()
            for c in sorted(candidates,key=lambda x:x['quality_score'], reverse=True):
                if c['dominant_content_family'] in seen and len(chosen)>=1:
                    continue
                chosen.append(c); seen.add(c['dominant_content_family'])
                if len(chosen)>=default_max_per_book: break
        else:
            chosen=sorted(candidates,key=lambda x:(x['start_page']))[:default_max_per_book]

        packets.extend(chosen)
        with_packets += 1 if chosen else 0

    if a.max_packets_total and len(packets) > a.max_packets_total:
        packets = sorted(packets, key=lambda x: x['quality_score'], reverse=True)[:a.max_packets_total]

    plan={
        'plan_id':a.plan_id,'source_output_root':str(root),'generator_version':'handoff_plan_generator_v0_1','mode':a.mode,
        'selection_strategy':a.selection_strategy,'max_pages_per_packet':a.max_pages_per_packet,'min_pages_per_packet':a.min_pages_per_packet,
        'min_text_chars':a.min_text_chars,'max_tags_per_packet':a.max_tags_per_packet,
        'books_scanned':scanned,'books_with_packets':with_packets,'books_skipped':skipped,'support_directories_ignored':ignored,
        'warnings':warnings,'packets':packets,
    }
    out=Path(a.output_plan); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(plan,indent=2),encoding='utf-8')
    print(json.dumps(plan, indent=2))


if __name__=='__main__':
    main()
