# noNotifications.ps1
# Desactiva el acceso a las notificaciones para todos los usuarios (requiere permisos de administrador)
# Ejecutar como administrador

function Test-Admin {
    $currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentIdentity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-Admin)) {
    Write-Host "[ERROR] Este script debe ejecutarse como administrador." -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] Desactivando el listener de notificaciones para todos los usuarios..."

$regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\userNotificationListener"
New-Item -Path $regPath -Force | Out-Null
Set-ItemProperty -Path $regPath -Name "Value" -Type String -Value "Deny"

# Verificación
$actual = (Get-ItemProperty -Path $regPath -Name "Value").Value
if ($actual -eq "Deny") {
    Write-Host "[OK] El acceso a las notificaciones ha sido denegado correctamente. Los cambios son inmediatos." -ForegroundColor Green
} else {
    Write-Host "[ERROR] No se pudo denegar el acceso a las notificaciones." -ForegroundColor Red
}
