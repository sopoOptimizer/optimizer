# disable_telemetry.ps1
Write-Host "Desactivando telemetría básica..." -ForegroundColor Cyan

# Desactivar servicio de DiagTrack
Set-Service DiagTrack -StartupType Disabled -ErrorAction SilentlyContinue
Stop-Service DiagTrack -ErrorAction SilentlyContinue

# Ajustes de registro
New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name "AllowTelemetry" -Value 0 -PropertyType DWORD -Force | Out-Null

Write-Host "Telemetría desactivada."
