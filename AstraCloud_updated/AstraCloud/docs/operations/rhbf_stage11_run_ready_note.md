# RHBF Stage 11 run-ready note

This pack should be governed by the following already-installed files in AstraCloud:

- configs/project/sourcebook_profiles/rhbf_merged_primary_donor.yaml
- configs/routing/rhbf_merged_chunk_guidance.yaml
- configs/validation/rhbf_merged_validator_targets.yaml

This Stage 11 pack adds a live-conversion profile/guidance/validator overlay:

- configs/project/sourcebook_profiles/rhbf_stage11_live_conversion.yaml
- configs/routing/rhbf_stage11_live_chunk_guidance.yaml
- configs/validation/rhbf_stage11_live_validator_targets.yaml

## Recommended practical use

1. Use the merged RHBF donor profile as the baseline doctrine.
2. Use this pack’s live-conversion files for packet-oriented conversion runs.
3. Emit lexicon deltas and canon conflict packets for any unresolved reserve, aura, fate, or body-slot language.
4. Treat the four packet files in this pack as the first player-facing Astra conversion outputs, not final immutable canon.
