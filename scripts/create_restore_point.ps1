Write-Host "Comprobando protección del sistema en C: ..."
$vss = Get-ComputerRestorePoint -ErrorAction SilentlyContinue
if ($vss -eq $null) {
    Write-Host "No hay puntos de restauración existentes o la protección no está habilitada."
} else {
    Write-Host "Puntos de restauración existentes encontrados."
}

# Intentar crear el punto de restauración
try {
    Write-Host "Intentando crear punto de restauración..."
    Checkpoint-Computer -Description "Punto de Restauración SOPO" -RestorePointType "MODIFY_SETTINGS" -ErrorAction Stop
    Write-Host "Punto de restauración creado correctamente."
} catch {
    Write-Host "Error al crear punto de restauración: $_"
}