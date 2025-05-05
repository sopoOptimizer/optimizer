# disable_telemetry_tasks.ps1
Write-Host "Deshabilitando tareas de telemetría..." -ForegroundColor Cyan

$tasks = @(
    "\Microsoft\Windows\Customer Experience Improvement Program\Consolidator",
    "\Microsoft\Windows\Customer Experience Improvement Program\KernelCeip",
    "\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip"
)
foreach ($task in $tasks) {
    schtasks /Change /TN $task /Disable | Out-Null
    Write-Host "Tarea $task deshabilitada."
}
