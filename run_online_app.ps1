$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot ".venv-deep\Scripts\python.exe"
& $python (Join-Path $PSScriptRoot "online_service.py") --host 127.0.0.1 --port 8765
