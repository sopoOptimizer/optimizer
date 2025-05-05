# flush_dns.ps1
Write-Host "Reiniciando configuración de red (Flush DNS, reset TCP/IP)..." -ForegroundColor Cyan

ipconfig /flushdns
netsh winsock reset
netsh int ip reset
netsh int ipv6 reset

Write-Host "Configuraciones de red reiniciadas. Se recomienda reiniciar el equipo para ver cambios."
