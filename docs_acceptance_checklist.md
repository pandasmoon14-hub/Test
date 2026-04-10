# Acceptance checklist

1. No visible source-PDF mutation: **Implemented**.
2. No synthetic page mapping: **Implemented for chunk expansion path**.
3. Provenance for page/table/stat fields: **Implemented via page metadata + page truth + sidecars**.
4. Simple tables render as Markdown: **Implemented in table fixer**.
5. Complex structures sidecar-first: **Partially implemented (table sidecar enriched)**.
6. Rotation normalized before repair: **Partially implemented (orientation metadata + adaptive render path)**.
7. Gridless/sparse handling improved: **Implemented (pseudo-table alignment + row padding)**.
8. Hard pages rerouted/retried per page: **Implemented**.
9. Queue retries deterministic/auditable: **Improved with WAL + checkpoint cadence**.
10. Regression coverage for hard layouts: **Expanded synthetic coverage**.
