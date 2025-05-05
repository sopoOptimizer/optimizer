$ErrorActionPreference = 'Stop'
# Desactivar Cortana y telemetría, alto rendimiento
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search" -Name "AllowCortana" -Value 0 -Force
New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Force | Out-Null
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name "AllowTelemetry" -Value 0 -Force
powercfg /setactive SCHEME_MIN
Remove-Item -Path $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue
Write-Output "Optimización de trabajo completada. Es posible que necesite reiniciar para aplicar los cambios."
exit 3010
