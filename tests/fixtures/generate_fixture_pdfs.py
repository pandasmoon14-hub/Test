#!/usr/bin/env python3
from pathlib import Path
import fitz

def make(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    def one(name, draw):
        d=fitz.open(); draw(d); d.save(out/name); d.close()
    one('single_column_prose.pdf', lambda d: d.new_page().insert_text((72,72), 'Prose page '*80))
    one('two_column_rules.pdf', lambda d: [d.new_page().insert_text((50,72),'L '*80), d[-1].insert_text((320,72),'R '*80)])
    one('stat_block_d20_style.pdf', lambda d: d.new_page().insert_text((72,72), 'Armor Class 15\nHit Points 30\nActions: Slam +5'))
    one('action_list_lancer_cloudbreaker_style.pdf', lambda d: d.new_page().insert_text((72,72), 'Quick Action: Boost\nProtocol: Scan\nSystem: Brace'))
    one('dense_table.pdf', lambda d: d.new_page().insert_text((72,72), '|A|B|\n|--|--|\n|1|2|\n|3|4|'))
    one('landscape_rotated.pdf', lambda d: d.new_page(width=842, height=595).insert_text((72,72), 'Landscape'))
    one('image_only_scan_like.pdf', lambda d: d.new_page())
    one('mixed_text_images.pdf', lambda d: d.new_page().insert_text((72,72), 'text plus image placeholder'))
    one('character_sheet_form_like.pdf', lambda d: d.new_page().insert_text((72,72), 'Name:_____\nClass:_____\nHP:_____'))
    one('blank_page.pdf', lambda d: d.new_page())
    def multi(d):
        for i in range(10):
            p=d.new_page();
            if i in (2,6):
                continue
            p.insert_text((72,72), f'Mixed page {i+1}')
    one('multi_page_mixed_10_pages.pdf', multi)

if __name__=='__main__':
    make(Path(__file__).resolve().parent)
