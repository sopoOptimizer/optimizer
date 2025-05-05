Write-Host "Activando Modo Juego de Windows..." -ForegroundColor Green

# Habilitar el Modo Juego
Set-ItemProperty -Path "HKCU:\Software\Microsoft\GameBar" -Name "AutoGameModeEnabled" -Type DWord -Value 1 -Force
Set-ItemProperty -Path "HKCU:\System\GameConfigStore" -Name "GameMode_UserGameModeEnabled" -Type DWord -Value 1 -Force

Write-Host "Modo Juego activado correctamente." -ForegroundColor Green
Write-Host "Presiona cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")