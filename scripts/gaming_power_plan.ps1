# gaming_power_plan.ps1
Write-Host "Activando plan de energía High Performance / Ultimate Performance..." -ForegroundColor Cyan

# Prueba con Ultimate Performance si existe:
$ultimateGuid = "ded574b5-45a0-4f42-8737-46345c09c238"
$highPerfGuid = "8c5e7fda-e8bf-4a96-9a85-4f20e7a82598"

$allPlans = powercfg /list
if ($allPlans -match $ultimateGuid) {
    powercfg /setactive $ultimateGuid
    Write-Host "Plan 'Ultimate Performance' activado."
} else {
    powercfg /setactive $highPerfGuid
    Write-Host "Plan 'Alto Rendimiento' activado (Ultimate no disponible)."
}
