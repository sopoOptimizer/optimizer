$ErrorActionPreference = 'Stop'
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop\WindowMetrics" -Name "MinAnimate" -Value 0 -Force
Reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v "VisualFXSetting" /t REG_DWORD /d 2 /f
Write-Output "Animaciones desactivadas. Es posible que necesite reiniciar para aplicar los cambios."
exit 3010