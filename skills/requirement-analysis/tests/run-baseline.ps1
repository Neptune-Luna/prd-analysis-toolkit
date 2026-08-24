param(
    [string]$RunDir = "$PSScriptRoot/fixtures/sample-run",
    [ValidateSet("parse", "extract", "clarify", "review", "aggregate", "all")]
    [string]$Stage = "all"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$validator = Join-Path $repoRoot "scripts/validate-artifacts.ps1"

if (-not (Test-Path -LiteralPath $validator)) {
    throw "Missing validator: $validator"
}

& $validator -RunDir $RunDir -Stage $Stage
