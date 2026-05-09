from __future__ import annotations
import argparse, json, sys, importlib.util
from pathlib import Path


def _load_local(fn: str, attr: str):
    here = Path(__file__).resolve().parent
    p = here / fn
    spec = importlib.util.spec_from_file_location(f"_handoff_{fn}", p)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {fn}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return getattr(mod, attr)


def _resolve_book(packet: dict, source_root: Path):
    warns=[]
    if packet.get('book_dir'):
        p=Path(packet['book_dir'])
        return p, warns
    bm = str(packet.get('book_match',''))
    matches = sorted([d for d in source_root.iterdir() if d.is_dir() and bm.lower() in d.name.lower()])
    if len(matches)==0:
        return None, warns
    if len(matches)>1:
        warns.append(f"multiple_book_matches:{bm}:{matches[0].name}")
    return matches[0], warns


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--plan-file', required=True)
    ap.add_argument('--output-root', required=True)
    ap.add_argument('--strict', action='store_true')
    a=ap.parse_args()

    build_main = _load_local('build_handoff_packet.py', 'main')
    validate_packet = None
    try:
        validate_packet = _load_local('validate_handoff_packet.py', 'validate_packet')
    except Exception:
        validate_packet = None

    plan_file = Path(a.plan_file)
    out_root = Path(a.output_root)
    out_root.mkdir(parents=True, exist_ok=True)

    errors=[]; warnings=[]
    plan = json.loads(plan_file.read_text(encoding='utf-8-sig'))
    for f in ['plan_id','source_output_root','packets']:
        if f not in plan:
            errors.append(f"missing_plan_field:{f}")
    packets = plan.get('packets', []) if isinstance(plan.get('packets', []), list) else []

    summary={"plan_id":plan.get('plan_id','unknown'),"plan_file":str(plan_file),"output_root":str(out_root),"strict":bool(a.strict),"valid":False,
             "packets_total":len(packets),"packets_built":0,"packets_failed":0,"packets_validated":0,"packets_validation_failed":0,
             "packet_ids":[],"failed_packet_ids":[],"warnings":warnings,"errors":errors,"packet_results":[]}

    source_root = Path(plan.get('source_output_root',''))
    for p in packets:
        pid=p.get('packet_id','unknown')
        res={"packet_id":pid,"book_dir":"","output_dir":str(out_root/pid),"built":False,"validated":False,"valid":False,"errors":[],"warnings":[]}
        summary['packet_ids'].append(pid)
        for f in ['packet_id','start_page','end_page']:
            if f not in p: res['errors'].append(f"missing_packet_field:{f}")
        purpose = p.get('packet-purpose', p.get('packet_purpose'))
        if not purpose: res['errors'].append('missing_packet_field:packet-purpose')
        if not (p.get('book_match') or p.get('book_dir')): res['errors'].append('missing_packet_field:book_match_or_book_dir')

        book_dir=None
        if not res['errors']:
            book_dir, w = _resolve_book(p, source_root)
            res['warnings'].extend(w)
            if book_dir is None:
                res['errors'].append('book_resolution_failed')
            else:
                res['book_dir']=str(book_dir)

        if not res['errors']:
            old_argv = sys.argv
            sys.argv = ['build_handoff_packet.py','--book-dir',str(book_dir),'--start-page',str(p['start_page']),'--end-page',str(p['end_page']),'--packet-id',pid,'--packet-purpose',str(purpose),'--output-dir',str(out_root/pid)]
            try:
                build_main()
                res['built']=True
                summary['packets_built'] += 1
            except Exception as exc:  # pylint: disable=broad-exception-caught
                res['errors'].append(f'build_failed:{exc}')
            finally:
                sys.argv = old_argv

        if res['built'] and validate_packet is not None:
            summary['packets_validated'] += 1
            try:
                rep, _ = validate_packet(out_root/pid, strict=a.strict)
                res['validated']=True
                res['valid']=bool(rep.get('valid',False))
                if not res['valid']:
                    summary['packets_validation_failed'] += 1
                    res['errors'].extend(rep.get('errors',[]))
            except Exception as exc:  # pylint: disable=broad-exception-caught
                summary['packets_validation_failed'] += 1
                res['errors'].append(f'validation_failed:{exc}')

        if res['errors']:
            summary['packets_failed'] += 1
            summary['failed_packet_ids'].append(pid)
        else:
            res['valid'] = True if res['validated'] else res['built']

        summary['packet_results'].append(res)

    summary['valid'] = len(summary['errors']) == 0 and summary['packets_failed'] == 0 and (summary['packets_validation_failed'] == 0)
    (out_root/'handoff_batch_build_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))

    if a.strict and (summary['errors'] or summary['packets_failed'] or summary['packets_validation_failed']):
        sys.exit(1)


if __name__ == '__main__':
    main()
