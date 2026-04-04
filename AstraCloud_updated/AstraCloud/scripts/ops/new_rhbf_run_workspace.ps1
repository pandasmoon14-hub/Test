param(
    [string]$Root = (Get-Location).Path,
    [Parameter(Mandatory=$true)][string]$RunId
)

$Dirs = @(
    "logs\runs\$RunId",
    "logs\runs\$RunId\reports",
    "logs\runs\$RunId\lexicon",
    "logs\runs\$RunId\canon",
    "logs\runs\$RunId\packets",
    "data\sources\manifests\$RunId"
)

foreach ($rel in $Dirs) {
    $path = Join-Path $Root $rel
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

Write-Host ""
Write-Host "Created workspace for run: $RunId" -ForegroundColor Green
$Dirs | ForEach-Object { Write-Host "  $(Join-Path $Root $_)" }
Write-Host ""
Write-Host "Next:" -ForegroundColor Cyan
Write-Host "1. Copy the filled manifest example into the run workspace."
Write-Host "2. Edit run metadata and source references."
Write-Host "3. Execute Batch A first."
