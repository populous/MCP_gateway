# OpenClaw Gateway monitor console
# Launched at logon by "OpenClaw Monitor.lnk" in the Windows Startup folder.
# Closing this window does NOT stop the gateway (the gateway runs as the
# "OpenClaw Gateway" scheduled task via gateway.vbs).

$ErrorActionPreference = 'Continue'
$Host.UI.RawUI.WindowTitle = 'OpenClaw Gateway Monitor'
try { [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false) } catch {}
$env:OPENCLAW_MONITOR = '1'

function Write-Banner {
    Write-Host ''
    Write-Host '=== OpenClaw Gateway Monitor ===' -ForegroundColor Cyan
    Write-Host ("  dashboard : http://127.0.0.1:18789/")
    Write-Host ("  started   : {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
    Write-Host '  Ctrl+C / closing this window stops only the log tail.' -ForegroundColor DarkGray
    Write-Host ''
}

function Test-GatewayPort {
    $c = New-Object System.Net.Sockets.TcpClient
    try {
        $c.Connect('127.0.0.1', 18789)
        return $c.Connected
    } catch { return $false } finally { $c.Dispose() }
}

function Wait-Gateway {
    # The scheduled task and this window start at the same time, so give the
    # gateway a chance to bind its port before the first RPC attempt.
    for ($i = 1; $i -le 60; $i++) {
        if (Test-GatewayPort) { return $true }
        Write-Host ("  waiting for gateway on port 18789 ... ({0}/60)" -f $i) -ForegroundColor DarkYellow
        Start-Sleep -Seconds 2
    }
    return $false
}

Write-Banner

while ($true) {
    if (-not (Wait-Gateway)) {
        Write-Host '  gateway did not come up within 2 minutes.' -ForegroundColor Red
        Write-Host '  check: openclaw daemon status' -ForegroundColor Red
        Start-Sleep -Seconds 30
        continue
    }

    Write-Host ("--- tail started {0} ---" -f (Get-Date -Format 'HH:mm:ss')) -ForegroundColor Green
    & openclaw logs --follow --local-time --limit 50

    # `openclaw logs --follow` only returns when the gateway drops the RPC
    # connection (restart, update, shutdown). Reconnect instead of exiting so
    # the window keeps monitoring across gateway restarts.
    Write-Host ("--- tail ended {0} (exit {1}), reconnecting in 5s ---" -f (Get-Date -Format 'HH:mm:ss'), $LASTEXITCODE) -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}
