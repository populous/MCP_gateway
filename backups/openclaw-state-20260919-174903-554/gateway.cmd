@echo off
rem OpenClaw Gateway
set "PATH=C:\Program Files\GitHub CLI;%PATH%"
set "TMPDIR=C:\Users\popul\AppData\Local\Temp"
set "NODE_OPTIONS="
set "OPENCLAW_GATEWAY_PORT=18789"
set "OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service"
set "OPENCLAW_WINDOWS_TASK_NAME=OpenClaw Gateway"
set "OPENCLAW_SERVICE_MARKER=openclaw"
set "OPENCLAW_SERVICE_KIND=gateway"
"C:\Program Files\nodejs\node.exe" --max-old-space-size=8163 C:\Users\popul\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789 --task-supervisor < NUL
