# optimize_startup.ps1
Write-Host "Optimizando inicio de Windows..." -ForegroundColor Cyan

# Ejemplo: desactivar apps de inicio. Cada app varía en su ruta
# Basta con mostrar un ejemplo:
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v OneDrive /f 2>$null
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Spotify /f 2>$null

Write-Host "Inicio de Windows optimizado."
