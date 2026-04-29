from __future__ import annotations
import json
from pathlib import Path


def load_run_summary(output_dir: str):
    p = Path(output_dir) / 'logs' / 'run_summary.json'
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding='utf-8'))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', required=True)
    args = ap.parse_args()
    print(json.dumps(load_run_summary(args.output_dir), indent=2))
