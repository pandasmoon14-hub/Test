# Page-truth-first flow

1. Source PDF is never visibly mutated.
2. `orchestrator.py` writes `*.page_truth.jsonl` using source geometry, metadata, and per-page counts.
3. Lanes produce markdown with explicit `<!-- PAGE:N -->` markers when available.
4. If chunk markers exist without page markers, chunk payload is retained without paragraph spreading.
5. Audit marks uncertain pages for quarantine/repair queue rather than fabricating confidence.
