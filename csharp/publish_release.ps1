$ErrorActionPreference = "Stop"

Write-Host "== ENIAC Publish Release ==" -ForegroundColor Cyan

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$outputRoot = Join-Path $root "artifacts\release"
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null

$projects = @(
    @{ Name = "app"; Path = "csharp/src/ENIAC.Tuner.App/ENIAC.Tuner.App.csproj" },
    @{ Name = "cli"; Path = "csharp/src/ENIAC.Tuner.Cli/ENIAC.Tuner.Cli.csproj" },
    @{ Name = "installer"; Path = "csharp/src/ENIAC.Tuner.Installer/ENIAC.Tuner.Installer.csproj" }
)

foreach ($p in $projects) {
    $out = Join-Path $outputRoot $p.Name
    Write-Host "Publishing $($p.Name)..." -ForegroundColor Yellow

    dotnet publish $p.Path `
        -c Release `
        -o $out 2>&1
}

Write-Host "Release artifacts generated at: $outputRoot" -ForegroundColor Green
