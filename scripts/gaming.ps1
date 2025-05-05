$ErrorActionPreference = 'Stop'

function Ensure-RegistryKey {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -Path $Path -Force | Out-Null
    }
}

Ensure-RegistryKey "HKCU:\SOFTWARE\Microsoft\Windows\GameBar"
Ensure-RegistryKey "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR"
Ensure-RegistryKey "HKCU:\System\GameConfigStore"
Ensure-RegistryKey "HKLM:\SOFTWARE\Policies\Microsoft\Windows\GameDVR"

Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR" -Name "AppCaptureEnabled" -Value 0 -Force
Set-ItemProperty -Path "HKCU:\System\GameConfigStore" -Name "GameDVR_Enabled" -Value 0 -Force
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\GameBar" -Name "AllowAutoGameMode" -Value 0 -Force
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\GameBar" -Name "ShowStartupPanel" -Value 0 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\GameDVR" -Name "AllowGameDVR" -Value 0 -Force

Get-Process GameBar -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Output "Game Bar desactivado. Es posible que necesite reiniciar para aplicar los cambios."
exit 3010
