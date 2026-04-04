# Windows First-Run Operator Guide

## 1. Confirm repo health

Run the install verification script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\ops\verify_astracloud_install.ps1
```

If it reports missing files, fix those before doing anything else.

## 2. Create a run workspace

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\ops\new_rhbf_run_workspace.ps1 -Root . -RunId rhbf_prod_run_001
```

This creates a clean workspace under:
`logs\runs\rhbf_prod_run_001`
and a staging area under:
`data\sources\manifests\rhbf_prod_run_001`

## 3. Place donor inputs where you can find them

Keep your RHBF PDFs in a stable folder outside the repo or in a clearly named staging folder.
Do not scatter them around your desktop like cursed confetti.

## 4. Copy the filled example manifest

Use:
`data\templates\manifests\rhbf_first_production_manifest_filled_example.yaml`

Copy it into your run workspace and rename it to:
`rhbf_prod_run_001_manifest.yaml`

Edit:
- date_started
- operator
- actual input paths if you are tracking them manually

## 5. Run in this order

- Batch A first
- review
- Batch B second
- review
- Batch C third
- review
- adjudication last

Do not run all three as one fused mega-pass.

## 6. Record outputs

For each batch, record:
- packet files produced
- lexicon issues
- canon issues
- validator concerns
- any blocked-term leakage

## 7. Use promoted doctrine

Default Astra-facing language should prefer:
- Presence Pressure
- Fate
- Meridian Reserve
- Meridian Channels
- Stronghold Phase
- Technique Repository
- Gate Array

Avoid silently using:
- Aura
- Luck
- Aether
- Essence
- donor proper nouns as canon

## 8. After each batch

Use the production report template from Stage 13 and write a report before moving on.
