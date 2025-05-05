# disable_win_tips.ps1
Write-Host "Desactivando consejos de Windows..." -ForegroundColor Cyan

New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" -Name "SubscribedContent-310093Enabled" -Value 0 -PropertyType DWORD -Force | Out-Null
New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" -Name "SubscribedContent-338388Enabled" -Value 0 -PropertyType DWORD -Force | Out-Null

Write-Host "Consejos de Windows desactivados."
