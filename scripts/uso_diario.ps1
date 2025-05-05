$ErrorActionPreference = 'Stop'
# Optimización de uso diario: desactivar animaciones y limpiar Prefetch
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop\WindowMetrics" -Name "MinAnimate" -Value 0 -Force
Reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v "VisualFXSetting" /t REG_DWORD /d 2 /f
Remove-Item -Path C:\Windows\Prefetch\* -Force -ErrorAction SilentlyContinue
Write-Output "Optimización de uso diario completada. Es posible que necesite reiniciar para aplicar los cambios."
exit 3010
