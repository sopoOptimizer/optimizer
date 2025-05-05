# verificar_noNotifications.ps1
# Script para comprobar si las notificaciones están desactivadas

$regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\userNotificationListener"

try {
    $valor = (Get-ItemProperty -Path $regPath -Name "Value" -ErrorAction Stop).Value
    if ($valor -eq "Deny") {
        Write-Host "[VERIFICACIÓN OK] Las notificaciones están desactivadas (Valor: Deny)" -ForegroundColor Green
    } else {
        Write-Host "[ATENCIÓN] Las notificaciones NO están desactivadas (Valor: $valor)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] No se encontró la clave de registro. Las notificaciones pueden estar activas o no se aplicó el script correctamente." -ForegroundColor Red
}
