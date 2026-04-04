# Legacy findings and extracted evidence

## Notable evidence from the extracted package

- `Astra_V6_Markdown_First_Architecture_Analysis.md` documents that the old system remained heavily shaped by text/PDF assumptions even after markdown became the real substrate.
- `FASTLOCAL_UPGRADE_PLAN.md` shows that routing plus postcheck was already recognized as the highest-impact optimization path.
- `Logs/master_pipeline.log` records a failed preprocessor call and later converter failure during a Starfinder GM Core test run.

## Interpretation

The reboot is not guessing in the dark. The old framework already told us:

1. Not all chunks deserve LLM work.
2. Markdown structure must be treated as first-class.
3. Table and stat block handling need guarded paths.
4. Postcheck/validation is not optional.
5. The local orchestration layer is not a scalable production architecture.
