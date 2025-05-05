$ErrorActionPreference = 'Stop'
$benchmarkDir = "C:\SOPO_Benchmarks"
if (!(Test-Path $benchmarkDir)) { New-Item -ItemType Directory -Path $benchmarkDir | Out-Null }
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$benchmarkFile = Join-Path $benchmarkDir "benchmark_$timestamp.txt"

# Info básica de sistema
$cpu = Get-WmiObject Win32_Processor | Select-Object -ExpandProperty Name
$ram = [math]::Round((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)
$os = (Get-WmiObject Win32_OperatingSystem).Caption
$gpu = (Get-WmiObject Win32_VideoController | Select-Object -First 1).Name

# Uso actual
$cpuLoad = (Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
$ramFree = [math]::Round((Get-WmiObject Win32_OperatingSystem).FreePhysicalMemory / 1MB, 2)
$ramUsed = $ram - $ramFree
$ramPerc = [math]::Round(($ramUsed / $ram) * 100, 2)

# Procesos top RAM
$topRAM = Get-Process | Sort-Object -Property WorkingSet -Descending | Select-Object -First 5 | Select-Object ProcessName,Id,@{N='RAM_MB';E={[math]::Round($_.WorkingSet/1MB,2)}}
# Procesos top CPU
$topCPU = Get-Process | Sort-Object -Property CPU -Descending | Select-Object -First 5 | Select-Object ProcessName,Id,CPU
# Procesos top GPU (requiere Windows 10 17063+ y puede no estar en todos los sistemas)
try {
    $topGPU = Get-Process | Where-Object { $_.Path } | ForEach-Object {
        $gpuUsage = (Get-Counter "\\Process($_.ProcessName)\\% GPU Time" -ErrorAction SilentlyContinue).CounterSamples[0].CookedValue
        [PSCustomObject]@{ ProcessName = $_.ProcessName; Id = $_.Id; GPU = [math]::Round($gpuUsage,2) }
    } | Sort-Object -Property GPU -Descending | Select-Object -First 5
} catch {
    $topGPU = @()
}

# Guardar resultados
Add-Content $benchmarkFile "SOPO Benchmark ejecutado el $timestamp"
Add-Content $benchmarkFile "CPU: $cpu"
Add-Content $benchmarkFile "RAM total: $ram GB"
Add-Content $benchmarkFile "RAM usada: $ramUsed GB ($ramPerc`%)"
Add-Content $benchmarkFile "CPU uso actual: $cpuLoad %"
Add-Content $benchmarkFile "GPU: $gpu"
Add-Content $benchmarkFile "Sistema operativo: $os"
Add-Content $benchmarkFile "-------------------------------------"
Add-Content $benchmarkFile "Top 5 procesos por RAM:"
$topRAM | ForEach-Object { Add-Content $benchmarkFile \" - $($_.ProcessName) (PID $($_.Id)): $($_.RAM_MB) MB\" }
Add-Content $benchmarkFile \"Top 5 procesos por CPU:\"
$topCPU | ForEach-Object { Add-Content $benchmarkFile \" - $($_.ProcessName) (PID $($_.Id)): $($_.CPU) s\" }
Add-Content $benchmarkFile \"Top 5 procesos por GPU:\"
if ($topGPU.Count -gt 0) {
    $topGPU | ForEach-Object { Add-Content $benchmarkFile \" - $($_.ProcessName) (PID $($_.Id)): $($_.GPU) %\" }
} else {
    Add-Content $benchmarkFile \" - No disponible en este sistema\"
}
Add-Content $benchmarkFile \"-------------------------------------\"
Add-Content $benchmarkFile \"Benchmark finalizado correctamente.\"
Write-Output \"Benchmark ejecutado y guardado en $benchmarkFile\"