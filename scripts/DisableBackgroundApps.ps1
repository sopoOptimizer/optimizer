try {
    Write-Host "Desactivando aplicaciones de Microsoft en segundo plano..."
    $regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications"
    $regName = "GlobalUserDisabled"
    $regValue = 1
    
    if (-not (Test-Path $regPath)) {
        New-Item -Path $regPath -Force | Out-Null
    }
    
    Set-ItemProperty -Path $regPath -Name $regName -Value $regValue -Type DWord -Force
    Write-Host "Aplicaciones desactivadas correctamente."
    exit 0
}
catch {
    Write-Host "Error: $_"
    exit 1
}
