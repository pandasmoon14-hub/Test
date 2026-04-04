# Stage 14 architecture note

AstraCloud currently has three layers:

1. **Doctrine layer**
   - lexicon
   - canon candidates/conflicts
   - promoted and blocked terms
   - donor profiles and guidance

2. **Scaffolding layer**
   - routing configs
   - validator targets
   - manifest templates
   - packet templates
   - helper scripts

3. **Execution layer**
   - currently partial
   - enough for controlled, staged operator-driven runs
   - not yet a sealed end-to-end production robot

That means the correct operator stance is:
- verify
- stage inputs
- execute in batches
- review outputs
- adjudicate
- only then promote
