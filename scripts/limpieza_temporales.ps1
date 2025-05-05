# limpieza_temporales.ps1

Write-Host "=== LIMPIEZA DE TEMPORALES INICIADA ===" -ForegroundColor Cyan

# Comprobar si es admin
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ADVERTENCIA: PowerShell NO se está ejecutando como Administrador." -ForegroundColor Yellow
} else {
    Write-Host "PowerShell con privilegios de administrador."
}

Write-Host "`nLimpieza de carpeta TEMP del usuario..."
$tempPath = $env:TEMP
if (Test-Path $tempPath) {
    $antesUser = Get-ChildItem -Path $tempPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Archivos/carpetas antes de borrar: $($antesUser.Count)"
    
    try {
        $antesUser | Remove-Item -Force -Recurse -ErrorAction Stop
        Write-Host "Archivos borrados correctamente en $tempPath."
    } catch {
        Write-Host "Error borrando en $tempPath: $($_.Exception.Message)"
    }
    
    $despuesUser = Get-ChildItem -Path $tempPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Archivos/carpetas restantes: $($despuesUser.Count)"
} else {
    Write-Host "No existe la carpeta $tempPath."
}


Write-Host "`nLimpieza de carpeta C:\\Windows\\Temp..."
$windowsTemp = Join-Path $env:WINDIR "Temp"
if (Test-Path $windowsTemp) {
    $antesWin = Get-ChildItem -Path $windowsTemp -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Archivos/carpetas antes de borrar: $($antesWin.Count)"
    
    try {
        $antesWin | Remove-Item -Force -Recurse -ErrorAction Stop
        Write-Host "Archivos borrados correctamente en $windowsTemp."
    } catch {
        Write-Host "Error borrando en $windowsTemp: $($_.Exception.Message)"
    }
    
    $despuesWin = Get-ChildItem -Path $windowsTemp -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Archivos/carpetas restantes: $($despuesWin.Count)"
} else {
    Write-Host "No existe la carpeta $windowsTemp."
}


Write-Host "`nLimpieza de carpeta Prefetch..."
$prefetchPath = Join-Path $env:WINDIR "Prefetch"
if (Test-Path $prefetchPath) {
    $antesPref = Get-ChildItem -Path $prefetchPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Archivos/carpetas antes de borrar: $($antesPref.Count)"
    
    try {
        $antesPref | Remove-Item -Force -Recurse -ErrorAction Stop
        Write-Host "Archivos borrados correctamente en $prefetchPath."
    } catch {
        Write-Host "Error borrando en $prefetchPath: $($_.Exception.Message)"
    }
    
    $despuesPref = Get-ChildItem -Path $prefetchPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Archivos/carpetas restantes: $($despuesPref.Count)"
} else {
    Write-Host "No existe la carpeta $prefetchPath."
}

Write-Host "`n=== LIMPIEZA DE TEMPORALES FINALIZADA ==="
