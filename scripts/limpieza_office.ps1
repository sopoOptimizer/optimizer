# limpieza_office.ps1
Write-Host "Limpieza de temporales/caché de Office..." -ForegroundColor Cyan

# Ejemplo de ruta para Office. Varía según versión
$officeTemp = Join-Path $env:TEMP "Office"
if (Test-Path $officeTemp) {
    Get-ChildItem $officeTemp -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "Limpieza de Office completada."
