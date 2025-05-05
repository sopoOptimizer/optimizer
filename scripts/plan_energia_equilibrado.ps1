# plan_energia_equilibrado.ps1
Write-Host "Activando plan de energía Equilibrado..." -ForegroundColor Cyan

powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e

Write-Host "Plan de energía equilibrado aplicado."
