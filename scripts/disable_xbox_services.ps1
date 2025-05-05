# disable_xbox_services.ps1
Write-Host "Desactivando servicios de Xbox Live y Maps..." -ForegroundColor Cyan

Set-Service Xbgm -StartupType Disabled -ErrorAction SilentlyContinue
Stop-Service Xbgm -ErrorAction SilentlyContinue

Set-Service MapsBroker -StartupType Disabled -ErrorAction SilentlyContinue
Stop-Service MapsBroker -ErrorAction SilentlyContinue

Write-Host "Servicios de Xbox y Maps desactivados."
