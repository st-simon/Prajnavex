$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$Url = "http://127.0.0.1:8765"

function Test-PrajnavexServer {
    try {
        $null = Invoke-RestMethod -Uri "$Url/api/status" -TimeoutSec 2
        return $true
    } catch {
        return $false
    }
}

if (-not (Test-PrajnavexServer)) {
    Start-Process -FilePath "python" `
        -ArgumentList @("scripts\prajnavex_web.py") `
        -WorkingDirectory $ProjectRoot `
        -WindowStyle Hidden

    for ($i = 0; $i -lt 20; $i++) {
        Start-Sleep -Milliseconds 500
        if (Test-PrajnavexServer) {
            break
        }
    }
}

Start-Process $Url
