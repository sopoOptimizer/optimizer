# flush_dns_gaming.ps1
Write-Host "Reiniciando configuración de red para gaming..." -ForegroundColor Cyan

ipconfig /flushdns
netsh winsock reset
netsh int ip reset
netsh int ipv6 reset

Write-Host "Optimización de red para gaming completada."
