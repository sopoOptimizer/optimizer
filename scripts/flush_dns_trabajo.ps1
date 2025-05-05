# flush_dns_trabajo.ps1
Write-Host "Reiniciando configuración de red para trabajo..." -ForegroundColor Cyan

ipconfig /flushdns
netsh winsock reset
netsh int ip reset
netsh int ipv6 reset
