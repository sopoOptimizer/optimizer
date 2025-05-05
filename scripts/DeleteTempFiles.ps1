try {
    Write-Host "Limpiando archivos temporales..."
    $paths = @("C:\\Windows\\Temp", $env:TEMP)
    foreach ($p in $paths) {
        try {
            Get-ChildItem -Path $p -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
                try {
                    Remove-Item $_.FullName -Force -Recurse -ErrorAction Stop
                } catch {
                    # Ignora archivos en uso
                }
            }
        } catch {
            # Ignora errores de acceso al directorio
        }
    }
    Write-Host "Limpieza completada."
    exit 0
}
catch {
    Write-Host "Error: $_"
    exit 1
}
