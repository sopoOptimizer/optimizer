# noLocationTracking.ps1
# Desactiva el seguimiento de ubicación en Windows

Write-Host "[INFO] Desactivando seguimiento de ubicación..."

# Configurar registros para desactivar localización
$regSettings = @(
    @{Path="HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location"; Name="Value"; Type="String"; Value="Deny"},
    @{Path="HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Sensor\Overrides\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}"; Name="SensorPermissionState"; Type="DWord"; Value="0"},
    @{Path="HKLM:\SYSTEM\CurrentControlSet\Services\lfsvc\Service\Configuration"; Name="Status"; Type="DWord"; Value="0"},
    @{Path="HKLM:\SYSTEM\Maps"; Name="AutoUpdateEnabled"; Type="DWord"; Value="0"}
)

foreach ($setting in $regSettings) {
    try {
        if (-not (Test-Path $setting.Path)) {
            New-Item -Path $setting.Path -Force | Out-Null
        }
        Set-ItemProperty -Path $setting.Path -Name $setting.Name -Value $setting.Value -Type $setting.Type
        Write-Host "[OK] Configurado: $($setting.Path)\\$($setting.Name)" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] No se pudo configurar: $($setting.Path)\\$($setting.Name)" -ForegroundColor Red
        Write-Host "Detalles: $_" -ForegroundColor Yellow
    }
}

Write-Host "[SUCCESS] Seguimiento de ubicación desactivado correctamente" -ForegroundColor Green
