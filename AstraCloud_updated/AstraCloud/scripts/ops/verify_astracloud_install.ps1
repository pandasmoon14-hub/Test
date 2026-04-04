param(
    [string]$Root = (Get-Location).Path
)

$CriticalFiles = @(
    "README.md",
    "configs\routing\routes.yaml",
    "data\lexicon\canonical\astra_terms.yaml",
    "data\lexicon\canonical\mechanics_map.yaml",
    "data\lexicon\canonical\stage12_promoted_astra_terms.yaml",
    "data\lexicon\canonical\stage12_blocked_terms.yaml",
    "configs\project\run_profiles\rhbf_first_production_run.yaml",
    "data\templates\manifests\rhbf_first_production_manifest_template.yaml",
    "data\distillation\rulebook\astra_live_player_core_packet_v0_1.md",
    "data\distillation\mechanics_bible\astra_live_paths_and_techniques_packet_v0_1.md",
    "data\distillation\setting_bible\astra_live_activity_engine_packet_v0_1.md",
    "data\distillation\mechanics_bible\astra_live_creatures_and_bound_relics_packet_v0_1.md"
)

$Missing = foreach ($rel in $CriticalFiles) {
    $p = Join-Path $Root $rel
    if (-not (Test-Path $p -PathType Leaf)) { $rel }
}

Write-Host ""
Write-Host "AstraCloud verification root: $Root" -ForegroundColor Cyan
Write-Host ""

if ($Missing.Count -eq 0) {
    Write-Host "PASS: critical Stage 14 prerequisites are present." -ForegroundColor Green
}
else {
    Write-Host "FAIL: missing critical files." -ForegroundColor Yellow
    $Missing | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
}
