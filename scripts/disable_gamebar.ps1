# disable_gamebar.ps1
Write-Host "Desactivando GameBar y grabación de fondo..." -ForegroundColor Cyan

New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\GameDVR" -Name "AppCaptureEnabled" -Value 0 -PropertyType DWORD -Force | Out-Null
New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\GameDVR" -Name "GameDVR_Enabled" -Value 0 -PropertyType DWORD -Force | Out-Null

Write-Host "GameBar desactivada."
